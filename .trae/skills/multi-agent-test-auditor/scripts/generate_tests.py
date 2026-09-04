"""
generate_tests.py — 多代理对抗式测试设计五步法 Prompt 自动填充与 OpenAI 调用脚本

用法示例:
    # 1. 命令行直接传被测对象与契约
    python generate_tests.py \\
        --object "POST /api/login, 输入 username/password/captcha, 返回 token" \\
        --contract "连续失败5次锁定15分钟; token 1小时过期" \\
        --output out_login

    # 2. 从文件读取被测对象与契约（推荐，长文本适用）
    python generate_tests.py \\
        --object-file specs/login_object.md \\
        --contract-file specs/login_contract.md \\
        --output out_login

    # 3. 从 stdin 读取（适合管道）
    cat specs/login_combined.md | python generate_tests.py --stdin --output out_login

    # 4. 使用其他模型与流式输出
    python generate_tests.py \\
        --object-file specs/api.md --contract-file specs/contract.md \\
        --model gpt-4-turbo --stream --output out_api

环境变量:
    OPENAI_API_KEY   必填（或在 ~/.openai/credentials）
    OPENAI_BASE_URL  可选，自定义网关（如 Azure、代理）

输出:
    <output>.md       LLM 原始输出（含五步全过程）
    <output>.cases.json  解析出的测试用例结构化数据，便于导入 TestRail/Xray
    <output>.meta.json   元数据（token、成本、耗时、GOAL_STATE）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    sys.exit("缺少依赖：请运行 `pip install openai` 后重试")


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_PATH = SCRIPT_DIR.parent / "prompt-template.md"

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 16000

MODEL_PRICING_PER_M = {
    "gpt-4o":            {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":        {"input": 0.15,  "output": 0.60},
    "gpt-4-turbo":        {"input": 10.00, "output": 30.00},
    "gpt-4":              {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo":      {"input": 0.50,  "output": 1.50},
    "o1":                 {"input": 15.00, "output": 60.00},
    "o1-mini":            {"input": 3.00,  "output": 12.00},
    "o3-mini":            {"input": 1.10,  "output": 4.40},
}


@dataclass
class TestCase:
    """单个测试用例的结构化表示"""
    slug: str = ""
    strategy: str = ""
    scenario: str = ""
    kills_mutants: list[str] = field(default_factory=list)
    covers_branches: list[str] = field(default_factory=list)
    protects_transitions: list[str] = field(default_factory=list)
    code: str = ""


@dataclass
class GenerationResult:
    """一次调用的完整结果"""
    raw_output: str
    cases: list[TestCase]
    goal_state: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    elapsed_seconds: float
    estimated_cost_usd: float


def load_template(template_path: Path) -> str:
    """从 prompt-template.md 中提取"可直接复制的 Prompt 模板"段"""
    content = template_path.read_text(encoding="utf-8")
    # 模板被 ````markdown 与 ```` 包裹，提取中间内容
    match = re.search(r"````markdown\n(.*?)\n````", content, re.DOTALL)
    if not match:
        # 退而求其次：直接用整篇（用户可能改了结构）
        print(f"[warn] 模板结构异常，使用整文件作为模板: {template_path}",
              file=sys.stderr)
        return content
    return match.group(1)


def fill_template(template: str, object_spec: str, contract_spec: str) -> str:
    """把被测对象与契约填入模板占位符"""
    placeholder_object = "【在此填入被测对象，例如：用户登录接口 POST /api/login，输入字段 username/password/captcha，返回 token，限制 5 次/分钟重试】"
    placeholder_contract = "【在此填入：业务规则、状态转移、性能要求、安全要求、合规约束。例如：连续失败 5 次锁定 15 分钟；token 1 小时过期；登录成功需记录审计日志】"

    if placeholder_object not in template:
        raise ValueError("模板中找不到被测对象占位符，请检查模板文件")
    if placeholder_contract not in template:
        raise ValueError("模板中找不到契约占位符，请检查模板文件")

    return (template
            .replace(placeholder_object, object_spec.strip())
            .replace(placeholder_contract, contract_spec.strip()))


def call_llm(
    client: OpenAI,
    model: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
    stream: bool,
) -> tuple[str, dict]:
    """调用 OpenAI Chat Completions，返回 (文本输出, 用量元数据)"""
    usage_meta: dict = {}
    chunks: list[str] = []

    if stream:
        stream_obj = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            stream_options={"include_usage": True},
        )
        for event in stream_obj:
            if event.choices and event.choices[0].delta.content:
                chunk = event.choices[0].delta.content
                chunks.append(chunk)
                print(chunk, end="", flush=True)
            if getattr(event, "usage", None):
                usage_meta = {
                    "prompt_tokens": event.usage.prompt_tokens,
                    "completion_tokens": event.usage.completion_tokens,
                    "total_tokens": event.usage.total_tokens,
                }
        print()  # 流式输出后换行
        if not usage_meta:
            # 某些版本不在流末尾给 usage，做一次估算
            text = "".join(chunks)
            usage_meta = {
                "prompt_tokens": len(prompt) // 4,
                "completion_tokens": len(text) // 4,
                "total_tokens": (len(prompt) + len(text)) // 4,
            }
            usage_meta["_estimated"] = True
        return "".join(chunks), usage_meta
    else:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = resp.choices[0].message.content or ""
        usage_meta = {
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
            "total_tokens": resp.usage.total_tokens,
        }
        return text, usage_meta


def parse_output(raw_output: str) -> tuple[list[TestCase], str]:
    """从 LLM 输出中解析测试用例与 GOAL_STATE"""
    cases: list[TestCase] = []

    # 匹配 def test_<slug>(): + docstring + 代码体
    # 由于 LLM 输出格式可能不严格，我们容忍 docstring 缺失
    pattern = re.compile(
        r'def\s+test_(\w+)\s*\(\s*\)\s*(?:->\s*\S+\s*)?:\s*\n'
        r'(?:\s*"""(.*?)"""|\s*\'\'\'(.*?)\'\'\')?\s*\n'
        r'(.*?)(?=\ndef\s+test_|\n```|\Z)',
        re.DOTALL,
    )
    for m in pattern.finditer(raw_output):
        slug = m.group(1)
        doc = m.group(2) or m.group(3) or ""
        body = (m.group(4) or "").strip()

        # 从 docstring 提取元数据
        case = TestCase(slug=slug, code=f"def test_{slug}():\n{body}")
        for line in doc.splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip().lower()
            value = value.strip()
            if not value:
                continue
            if key == "策略":
                case.strategy = value
            elif key == "场景":
                case.scenario = value
            elif key in ("杀死突变", "杀死突变类型"):
                case.kills_mutants = [v.strip() for v in value.split(",") if v.strip()]
            elif key in ("覆盖分支", "覆盖的分支"):
                case.covers_branches = [v.strip() for v in value.split(",") if v.strip()]
            elif key in ("保护状态转移", "保护的状态转移"):
                case.protects_transitions = [v.strip() for v in value.split(",") if v.strip()]
        cases.append(case)

    # 兜底：如果正则没匹配到，但 LLM 输出了完整 ```python 代码块，整块当一个用例
    if not cases:
        python_blocks = re.findall(r"```python\n(.*?)\n```", raw_output, re.DOTALL)
        for i, block in enumerate(python_blocks):
            cases.append(TestCase(
                slug=f"block_{i}",
                strategy="(unparsed)",
                code=block,
            ))

    # 提取 GOAL_STATE
    goal_match = re.search(r'GOAL_STATE:\s*(\S+)', raw_output)
    goal_state = goal_match.group(1) if goal_match else "missing"

    return cases, goal_state


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """基于公开价格估算美元成本"""
    pricing = MODEL_PRICING_PER_M.get(model)
    if not pricing:
        return 0.0
    return (prompt_tokens / 1_000_000 * pricing["input"]
            + completion_tokens / 1_000_000 * pricing["output"])


def save_results(result: GenerationResult, output_dir: Path, name: str) -> None:
    """保存三种输出：原始 .md / 解析后的 .cases.json / 元数据 .meta.json"""
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{name}.md"
    md_path.write_text(result.raw_output, encoding="utf-8")
    print(f"[ok] 原始输出已保存: {md_path}")

    cases_path = output_dir / f"{name}.cases.json"
    cases_path.write_text(
        json.dumps([asdict(c) for c in result.cases], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] 用例结构化数据: {cases_path}  (共 {len(result.cases)} 条用例)")

    meta_path = output_dir / f"{name}.meta.json"
    meta = {
        "model": result.model,
        "goal_state": result.goal_state,
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "total_tokens": result.total_tokens,
        "elapsed_seconds": round(result.elapsed_seconds, 2),
        "estimated_cost_usd": round(result.estimated_cost_usd, 4),
        "case_count": len(result.cases),
        "strategies_used": sorted({c.strategy for c in result.cases if c.strategy}),
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"[ok] 元数据: {meta_path}")


def read_input(args: argparse.Namespace) -> tuple[str, str]:
    """根据命令行参数读取被测对象与契约"""
    if args.stdin:
        combined = sys.stdin.read()
        # 期望 stdin 包含两段：第一行是对象，其余是契约；用 --- 分隔
        if "---" in combined:
            obj, _, contract = combined.partition("---")
            return obj, contract
        return combined, ""

    obj = ""
    contract = ""

    if args.object:
        obj = args.object
    elif args.object_file:
        obj = Path(args.object_file).read_text(encoding="utf-8")

    if args.contract:
        contract = args.contract
    elif args.contract_file:
        contract = Path(args.contract_file).read_text(encoding="utf-8")

    if not obj:
        print("[error] 必须提供 --object / --object-file / --stdin 之一", file=sys.stderr)
        sys.exit(2)
    if not contract:
        print("[warn] 未提供契约，将留空占位符让 LLM 自行假设", file=sys.stderr)
        contract = "（未提供契约，请基于通用最佳实践自行假设业务规则与约束）"

    return obj, contract


def main() -> int:
    parser = argparse.ArgumentParser(
        description="多代理对抗式测试设计五步法 Prompt 自动填充与 OpenAI 调用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="详细文档见同目录 prompt-template.md",
    )
    parser.add_argument("--object", help="被测对象描述（短文本）")
    parser.add_argument("--object-file", help="被测对象描述文件（长文本推荐）")
    parser.add_argument("--contract", help="契约与约束描述（短文本）")
    parser.add_argument("--contract-file", help="契约与约束文件（长文本推荐）")
    parser.add_argument("--stdin", action="store_true",
                        help="从 stdin 读取（对象与契约用 --- 分隔）")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE_PATH,
                        help=f"Prompt 模板路径（默认: {DEFAULT_TEMPLATE_PATH}）")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"OpenAI 模型名（默认: {DEFAULT_MODEL}）")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE,
                        help=f"采样温度（默认: {DEFAULT_TEMPERATURE}）")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS,
                        help=f"最大输出 token（默认: {DEFAULT_MAX_TOKENS}）")
    parser.add_argument("--stream", action="store_true",
                        help="流式输出（便于观察长输出）")
    parser.add_argument("--output-dir", type=Path, default=Path("."),
                        help="输出目录（默认: 当前目录）")
    parser.add_argument("--name", default="tests_output",
                        help="输出文件名前缀（默认: tests_output）")
    parser.add_argument("--dry-run", action="store_true",
                        help="只打印填充后的 prompt 不调用 LLM")
    args = parser.parse_args()

    # 1. 加载模板
    if not args.template.exists():
        print(f"[error] 模板不存在: {args.template}", file=sys.stderr)
        return 2
    template = load_template(args.template)

    # 2. 读取被测对象与契约
    object_spec, contract_spec = read_input(args)

    # 3. 填充模板
    filled = fill_template(template, object_spec, contract_spec)

    if args.dry_run:
        print("=" * 70)
        print("填充后的 Prompt（dry-run，未调用 LLM）:")
        print("=" * 70)
        print(filled)
        return 0

    # 4. 调用 OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[error] 未设置 OPENAI_API_KEY 环境变量", file=sys.stderr)
        return 3

    base_url = os.environ.get("OPENAI_BASE_URL")
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    print(f"[info] 调用模型: {args.model}")
    print(f"[info] 温度: {args.temperature}, 最大输出 token: {args.max_tokens}")
    print(f"[info] 流式: {'是' if args.stream else '否'}")
    print("=" * 70)

    start = time.time()
    try:
        raw_output, usage = call_llm(
            client=client,
            model=args.model,
            prompt=filled,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            stream=args.stream,
        )
    except Exception as e:
        print(f"\n[error] LLM 调用失败: {e}", file=sys.stderr)
        return 4
    elapsed = time.time() - start

    # 5. 解析输出
    cases, goal_state = parse_output(raw_output)
    cost = estimate_cost(
        args.model,
        usage.get("prompt_tokens", 0),
        usage.get("completion_tokens", 0),
    )

    result = GenerationResult(
        raw_output=raw_output,
        cases=cases,
        goal_state=goal_state,
        model=args.model,
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        elapsed_seconds=elapsed,
        estimated_cost_usd=cost,
    )

    # 6. 保存
    save_results(result, args.output_dir, args.name)

    # 7. 摘要
    print("=" * 70)
    print("[summary]")
    print(f"  耗时: {elapsed:.1f}s")
    print(f"  token: {result.prompt_tokens} in + {result.completion_tokens} out = {result.total_tokens} total")
    print(f"  估算成本: ${result.estimated_cost_usd:.4f}")
    print(f"  解析用例数: {len(cases)}")
    print(f"  涉及策略: {', '.join(sorted({c.strategy for c in cases if c.strategy})) or '(未解析)'}")
    print(f"  GOAL_STATE: {goal_state}")
    if goal_state not in ("complete",) and not goal_state.startswith("blocked"):
        print(f"  [warn] GOAL_STATE 异常: 期望 complete 或 blocked_<reason>，实际为 {goal_state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
