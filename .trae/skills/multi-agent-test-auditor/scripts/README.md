# generate_tests.py — 使用说明

## 一、依赖安装

```sh
cd "d:\Program Files\Code\CrouzeixConjecture-main\.trae\skills\multi-agent-test-auditor\scripts"
pip install -r requirements.txt
```

## 二、设置 API Key

### Windows PowerShell
```powershell
$env:OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"
```

### Linux / macOS
```sh
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### 自定义网关（如 Azure、代理）
```sh
export OPENAI_BASE_URL=https://your-gateway.example.com/v1
```

## 三、第一次运行（用示例）

```sh
cd "d:\Program Files\Code\CrouzeixConjecture-main\.trae\skills\multi-agent-test-auditor\scripts"

python generate_tests.py `
    --object-file specs\login_object.md `
    --contract-file specs\login_contract.md `
    --output out_login `
    --stream
```

输出会落在 `scripts\out_login.md` / `out_login.cases.json` / `out_login.meta.json`。

## 四、常用参数

| 参数 | 作用 |
|---|---|
| `--object` | 短文本被测对象描述 |
| `--object-file` | 长文本被测对象（推荐） |
| `--contract` | 短文本契约 |
| `--contract-file` | 长文本契约（推荐） |
| `--stdin` | 从 stdin 读取（对象与契约用 `---` 分隔） |
| `--template` | 自定义模板路径（默认用配套的 prompt-template.md） |
| `--model` | OpenAI 模型（默认 gpt-4o） |
| `--temperature` | 采样温度（默认 0.3） |
| `--max-tokens` | 最大输出 token（默认 16000） |
| `--stream` | 流式输出（推荐，长输出可观察进度） |
| `--output-dir` | 输出目录（默认当前目录） |
| `--name` | 输出文件名前缀 |
| `--dry-run` | 只打印填充后的 prompt，不调用 LLM |

## 五、模型成本对照（公开价格，每百万 token 美元）

| 模型 | 输入 | 输出 |
|---|---|---|
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4-turbo | $10.00 | $30.00 |
| o1 | $15.00 | $60.00 |
| o3-mini | $1.10 | $4.40 |

一次典型调用约 1-3 万 prompt token + 5-15 千 completion token。gpt-4o 单次约 $0.10-$0.30，gpt-4o-mini 约 $0.01。

## 六、dry-run 调试

第一次建议先 `--dry-run` 看填充后的 prompt 是否合理：

```sh
python generate_tests.py `
    --object-file specs\login_object.md `
    --contract-file specs\login_contract.md `
    --dry-run
```

## 七、解析输出说明

`<name>.cases.json` 结构：

```json
[
  {
    "slug": "login_success",
    "strategy": "equivalence_boundary",
    "scenario": "正确用户名密码登录成功",
    "kills_mutants": ["login.py:42 的 ==→!="],
    "covers_branches": ["branch_login_success"],
    "protects_transitions": ["未登录 → 已登录"],
    "code": "def test_login_success():\n    ..."
  }
]
```

可直接喂给 TestRail / Xray 导入脚本（见 SKILL.md 的"工具链映射表"段）。

## 八、与变异测试闭环

跑完一次后，把 LLM 生成的用例代码写入项目测试目录，跑 `mutmut run` 或 `Stryker`，把未杀死突变喂回 LLM 做第二轮：

```sh
mutmut run --paths-to-mutate src/
mutmut results --json > mutation_report.json
```

再用本脚本以 `--object` 传入 mutation_report.json 的内容，让 LLM 针对真实未杀死突变反推用例。

## 九、常见问题

**Q: 报错 "模板中找不到被测对象占位符"**
A: 你改过 prompt-template.md，把 `【在此填入被测对象...】` 占位符删了。回滚或修改脚本中的 `placeholder_object` 常量。

**Q: 报错 "未设置 OPENAI_API_KEY"**
A: 见第二节。

**Q: 输出被截断 / `GOAL_STATE: missing`**
A: 增大 `--max-tokens`（默认 16000），或换用上下文更大的模型。

**Q: 用例解析数 0**
A: LLM 没按 `def test_xxx(): + docstring` 格式输出。脚本兜底会把所有 ` ```python ` 代码块当作一个用例。可手动看 `.md` 原文。

**Q: 想接 Claude / 通义 / 文心**
A: Anthropic 把 `OpenAI()` 换成 `Anthropic()`，调用 `client.messages.create()`；通义/文心使用 OpenAI 兼容网关，设 `OPENAI_BASE_URL` 即可。
