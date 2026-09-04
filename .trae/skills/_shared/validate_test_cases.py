#!/usr/bin/env python3
"""
测试用例新标准验证脚本
对齐 _shared/standards.md 的「十一、输出 schema 校验」清单
重点验证策略家族标注是否生效

用法:
  python validate_test_cases.py cases.json          # 验证 JSON 文件
  python validate_test_cases.py --self-test          # 跑内置示例自测
  python validate_test_cases.py --stdin               # 从 stdin 读 JSON
"""

import sys
import json
import re
import csv
import argparse
from dataclasses import dataclass, field
from typing import List

# ============================================================
# 枚举定义（对齐 _shared/standards.md）
# ============================================================

STRATEGY_FAMILIES = {
    "equivalence_boundary",
    "property_based",
    "contract_test",
    "mutation_test",
    "state_model",
    "fuzz_chaos",
    "perf_profile",
    "attack_surface",
    "manual_heuristic",
}

# 测试类型使用英文枚举，对齐 _shared/standards.md 五、测试类型枚举
TEST_TYPES = {
    "functional", "boundary", "equivalence", "negative",
    "integration", "unit", "e2e", "compatibility",
    "security", "performance",
}

# 中文测试类型 → 英文枚举 归一化映射
# 用途：历史产物仍使用中文值时自动转换并告警，避免"覆盖率判 0"这类误导性失败。
# 新产物应直接填写英文枚举值（见 standards.md 五、的强制说明）。
TEST_TYPE_CN_MAP = {
    "功能测试": "functional",
    "正常功能测试": "functional",
    "正常测试": "functional",
    "正向测试": "functional",
    "边界测试": "boundary",
    "边界值测试": "boundary",
    "等价类测试": "equivalence",
    "等价类划分测试": "equivalence",
    "负向测试": "negative",
    "异常测试": "negative",
    "异常场景测试": "negative",
    "错误码测试": "negative",
    "参数验证测试": "negative",
    "兼容性测试": "compatibility",
    "安全测试": "security",
    "认证测试": "security",
    "性能测试": "performance",
    "集成测试": "integration",
    "单元测试": "unit",
    "端到端测试": "e2e",
}


def normalize_test_type(raw: str):
    """把测试类型值归一化为英文枚举。

    返回 (normalized, was_cn)。was_cn=True 表示原值是中文、已被自动转换（应告警）。
    无法识别时返回 (原值去空格, False)，由调用方报枚举错误。
    """
    val = str(raw or "").strip()
    # 去掉括号补充说明，如 "功能测试（functional）"
    core = val.split("（")[0].split("(")[0].strip()
    if core in TEST_TYPE_CN_MAP:
        return TEST_TYPE_CN_MAP[core], True
    return val, False

TEST_LEVELS = {"unit", "integration", "e2e"}

# 必覆盖场景类型（对齐 standards.md 九、必覆盖场景类型：正常/边界/等价类/异常/兼容性）
COVERED_SCENARIO_TYPES = {
    "functional", "boundary", "equivalence", "negative", "compatibility",
}

FUZZY_WORDS = ["可能", "大概", "应该", "一些", "若干", "也许", "或许", "大致"]

FUZZY_PHRASES = [
    "标准做法", "常规覆盖", "覆盖很高", "看起来够", "应该没问题",
    "差不多", "基本上", "一般来说", "通常来说",
]

# 支持多段前缀：LOGIN_001 / API_LOGIN_001 / SEC_LOGIN_001 / PERF_LOGIN_001 / XC_LOGIN_001 / EX_LOGIN_001 / BUG_LOGIN_003
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z][A-Z0-9]*)*_\d+$")
# API_ID_PATTERN 保留向后兼容（已被 ID_PATTERN 覆盖）
API_ID_PATTERN = re.compile(r"^API_[A-Z][A-Z0-9]*_\d+$")
SCENE_PATTERN = re.compile(r"^.+_.+_.+_.+$")

# ============================================================
# 验证结果
# ============================================================

@dataclass
class Violation:
    rule: str
    severity: str  # ERROR / WARN
    message: str
    case_id: str = ""

@dataclass
class Report:
    total: int = 0
    violations: List[Violation] = field(default_factory=list)

    @property
    def errors(self):
        return [v for v in self.violations if v.severity == "ERROR"]

    @property
    def warnings(self):
        return [v for v in self.violations if v.severity == "WARN"]

    @property
    def passed(self):
        return len(self.errors) == 0

    def summary(self):
        lines = []
        lines.append(f"总用例数: {self.total}")
        lines.append(f"错误: {len(self.errors)}  警告: {len(self.warnings)}")
        lines.append(f"结论: {'PASS' if self.passed else 'FAIL'}")
        if self.violations:
            lines.append("---")
            for v in self.violations:
                tag = f"[{v.case_id}] " if v.case_id else ""
                lines.append(f"[{v.severity}] {v.rule}: {tag}{v.message}")
        if not self.passed:
            lines.append("")
            lines.append("提示: 使用 --fix-report 查看修复建议报告")
        return "\n".join(lines)

    def fix_report(self) -> str:
        """从 violations 自动生成结构化修复建议报告"""
        if not self.violations:
            return "无需修复——全部校验通过。"

        from collections import defaultdict
        by_rule = defaultdict(list)
        for v in self.violations:
            by_rule[v.rule].append(v)

        lines = []
        lines.append("=" * 60)
        lines.append("  修复建议报告")
        lines.append("=" * 60)
        lines.append(f"总违规: {len(self.violations)} 项（{len(self.errors)} 错误 + {len(self.warnings)} 警告）")
        lines.append("")

        for rule, vs in by_rule.items():
            lines.append("-" * 50)
            lines.append(f"[{rule}] 共 {len(vs)} 项")
            lines.append("-" * 50)

            # 列出受影响的用例
            affected = [v.case_id for v in vs if v.case_id]
            if affected:
                lines.append(f"  受影响用例: {', '.join(affected)}")

            # 生成修复建议
            suggestion = generate_suggestion(rule, vs)
            lines.append(f"  修复建议: {suggestion}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("  修复后请重新运行验证: python validate_test_cases.py <file>")
        lines.append("=" * 60)
        return "\n".join(lines)


# ============================================================
# 修复建议生成（按违规规则类型）
# ============================================================

FAMILY_LIST = (
    "equivalence_boundary / property_based / contract_test / "
    "mutation_test / state_model / fuzz_chaos / perf_profile / "
    "attack_surface / manual_heuristic"
)

FAMILY_MATCHING_GUIDE = """根据用例特征选择策略家族（参考 _shared/standards.md 五-B）：
  划分输入域 + 取边界值     → equivalence_boundary
  找不变式 / 属性保持        → property_based
  从消费者期望反推契约      → contract_test
  反推代码突变找盲点         → mutation_test
  状态机转移覆盖             → state_model
  模糊输入 + 混沌注入        → fuzz_chaos
  阶梯/脉冲/雪崩负载         → perf_profile
  注入/越权/SSRF/重放        → attack_surface
  不属于上述方法论           → manual_heuristic（须注明理由）"""


def generate_suggestion(rule: str, violations: List[Violation]) -> str:
    """根据违规规则类型生成具体的修复建议"""
    v0 = violations[0]
    msg = v0.message

    if rule == "ID约束":
        if "缺少" in msg:
            return "补充用例ID字段，格式 {模块缩写}_{序号}（如 LOGIN_001）或 API_{模块缩写}_{序号}（如 API_LOGIN_001）"
        return f"将旧格式 ID 改为 {{模块缩写}}_{{序号}} 格式（如 LOGIN_001），废弃纯数字格式"

    if rule == "必填字段":
        if "前置条件" in msg:
            return "补充前置条件字段。如'用户已注册且账号正常'；无前置条件时填写'无'，不可留空"
        if "测试层级" in msg:
            return "补充测试层级字段，值为 unit / integration / e2e 之一"
        if "策略家族" in msg:
            return FAMILY_MATCHING_GUIDE
        return "补充缺失的必填字段"

    if rule == "枚举校验":
        if "测试层级" in msg:
            return f"将测试层级改为 unit / integration / e2e 之一"
        return "将值改为合法枚举之一"

    if rule == "策略家族":
        if "为空" in msg:
            return FAMILY_MATCHING_GUIDE
        if "不在枚举" in msg:
            return f"将策略家族替换为合法枚举之一：\n  {FAMILY_LIST}"
        return FAMILY_MATCHING_GUIDE

    if rule == "兜底家族":
        if "括号" in msg or "理由" in msg:
            return "manual_heuristic 必须在括号中注明理由，格式如：\n  manual_heuristic（纯UI对齐检查，不涉及输入域划分）"
        if "占比" in msg or "超过" in msg:
            manual_count = len(violations)
            return (
                f"manual_heuristic 占比超 20% 上限。"
                f"将 {manual_count} 条 manual_heuristic 用例重新匹配到前 8 条方法论家族。"
                f"\n参考策略家族标注指南，按用例特征选择对应家族。"
            )
        return "减少 manual_heuristic 用例数量，重新匹配到前 8 条方法论家族"

    if rule == "命名约束":
        return "按 模块_功能点_场景_预期 格式重写测试场景，如：\n  用户登录_密码正确_正常登录_登录成功"

    if rule == "模糊表述":
        return "将模糊表述替换为具体可验证的描述：\n  '应该提示错误' → '提示密码错误'\n  '可能显示' → '显示用户名和头像'"

    if rule == "预期结果":
        return "将笼统的预期结果改为具体可验证的描述：\n  '正常显示' → '显示用户名和头像'\n  '功能正常' → '返回 code=0 且跳转首页'"

    if rule == "场景覆盖":
        covered = set()
        for v in violations:
            # 从 message 提取已覆盖的类型
            pass
        missing = COVERED_SCENARIO_TYPES
        return (
            f"补充缺少的必覆盖场景类型。5 类必覆盖场景：\n"
            f"  functional / boundary / equivalence / negative / compatibility\n"
            f"参考 _shared/standards.md 九、必覆盖场景类型"
        )

    if rule == "策略家族多样性":
        return (
            f"策略家族多样性不足，需至少覆盖 4 条实质不同的家族。\n"
            f"当前覆盖的家族不够，建议补充以下家族：\n"
            f"  property_based（属性测试）/ contract_test（契约测试）/ "
            f"mutation_test（变异测试）/ state_model（状态机）\n"
            f"参考 _shared/standards.md 五-B 的 9 条策略家族枚举"
        )

    if rule == "金字塔约束":
        if "e2e" in msg:
            return (
                "e2e 用例占比超 15% 上限。将部分 e2e 用例下移到 unit/integration 层：\n"
                "  - 接口级验证 → 移到 integration\n"
                "  - 函数/方法级验证 → 移到 unit\n"
                "  - 只保留真正的完整业务主流程为 e2e\n"
                "参考测试金字塔原则：70% unit / 20% integration / 10% e2e"
            )
        return "调整测试层级分布，符合金字塔比例"

    if rule == "多样性自检":
        families_in_msg = set()
        for v in violations:
            import re
            m = re.search(r"'(\w+)'", v.message)
            if m:
                families_in_msg.add(m.group(1))
        return (
            f"部分策略家族堆积过多。考虑将部分用例重定向到探索不充分的家族：\n"
            f"  property_based / contract_test / mutation_test / state_model / fuzz_chaos\n"
            f"参考 _shared/standards.md 策略家族标注指南的匹配规则"
        )

    if rule == "空集":
        return "检查输入文件格式，确保 JSON 数组非空"

    return "参考 _shared/standards.md 修复对应问题"


# ============================================================
# 单条用例验证
# ============================================================

def validate_case(case: dict) -> List[Violation]:
    violations = []
    cid = case.get("用例ID", case.get("case_id", "<未知>"))

    # 1. ID 格式
    cid_val = case.get("用例ID", "")
    if not cid_val:
        violations.append(Violation("ID约束", "ERROR", "缺少用例ID字段", cid))
    elif not (ID_PATTERN.match(cid_val) or API_ID_PATTERN.match(cid_val)):
        violations.append(Violation(
            "ID约束", "ERROR",
            f"ID格式 '{cid_val}' 不符合 {{模块缩写}}_{{序号}} 或 API_{{模块缩写}}_{{序号}}",
            cid
        ))

    # 2. 前置条件
    pre = case.get("前置条件", "")
    if not pre or not str(pre).strip():
        violations.append(Violation("必填字段", "ERROR", "前置条件为空", cid))

    # 3. 测试层级
    level = case.get("测试层级", "")
    if not level:
        violations.append(Violation("必填字段", "ERROR", "测试层级为空", cid))
    elif level not in TEST_LEVELS:
        violations.append(Violation(
            "枚举校验", "ERROR",
            f"测试层级 '{level}' 不在 {TEST_LEVELS} 中",
            cid
        ))

    # 4. 策略家族（重点验证）
    family = case.get("策略家族", "")
    if not family:
        violations.append(Violation(
            "策略家族", "ERROR",
            "策略家族字段为空——这是必填字段",
            cid
        ))
    else:
        # 去掉括号说明，取主家族名
        family_main = family.split("（")[0].split("(")[0].strip()
        if family_main not in STRATEGY_FAMILIES:
            violations.append(Violation(
                "策略家族", "ERROR",
                f"策略家族 '{family}' 不在枚举 {sorted(STRATEGY_FAMILIES)} 中",
                cid
            ))

        # manual_heuristic 必须注明理由
        if family_main == "manual_heuristic":
            if "（" not in family and "(" not in family:
                violations.append(Violation(
                    "兜底家族", "ERROR",
                    "manual_heuristic 必须在括号中注明无法匹配前 8 条家族的理由",
                    cid
                ))

    # 4-B. 测试类型（逐条枚举校验，对齐 standards.md 五、）
    raw_type = case.get("测试类型", "")
    if not str(raw_type).strip():
        violations.append(Violation(
            "必填字段", "ERROR",
            "测试类型为空——这是必填字段",
            cid
        ))
    else:
        norm_type, was_cn = normalize_test_type(raw_type)
        if was_cn:
            violations.append(Violation(
                "测试类型", "WARN",
                f"测试类型 '{raw_type}' 已使用中文——应按 standards.md 五、改用英文枚举 '{norm_type}'"
                f"（本次已自动归一化，不影响判定）",
                cid
            ))
        if norm_type not in TEST_TYPES:
            violations.append(Violation(
                "测试类型", "ERROR",
                f"测试类型 '{raw_type}' 不在枚举 {sorted(TEST_TYPES)} 中"
                f"（见 _shared/standards.md 五、测试类型枚举）",
                cid
            ))

    # 5. 测试场景格式
    scene = case.get("测试场景", "")
    if not scene:
        violations.append(Violation("必填字段", "ERROR", "测试场景为空", cid))
    elif not SCENE_PATTERN.match(scene):
        violations.append(Violation(
            "命名约束", "ERROR",
            f"测试场景 '{scene}' 不符合 模块_功能点_场景_预期 格式（至少 4 段下划线分隔）",
            cid
        ))

    # 6. 预期结果
    expected = case.get("预期结果", "")
    if not expected or not str(expected).strip():
        violations.append(Violation("必填字段", "ERROR", "预期结果为空", cid))
    else:
        expected_str = str(expected)

        # 模糊词检查
        for word in FUZZY_WORDS:
            if word in expected_str:
                violations.append(Violation(
                    "模糊表述", "WARN",
                    f"预期结果含模糊词 '{word}'",
                    cid
                ))
                break

        # 模糊短语检查（对齐 _shared/standards.md 对抗审计输出契约）
        for phrase in FUZZY_PHRASES:
            if phrase in expected_str:
                violations.append(Violation(
                    "模糊表述", "WARN",
                    f"预期结果含模糊短语 '{phrase}'",
                    cid
                ))
                break

        # 过于笼统
        vague_phrases = ["正常显示", "正常工作", "功能正常", "显示正常"]
        for phrase in vague_phrases:
            if phrase in expected_str:
                violations.append(Violation(
                    "预期结果", "WARN",
                    f"预期结果过于笼统 '{phrase}'，应具体到显示什么内容",
                    cid
                ))
                break

    return violations


# ============================================================
# 批量验证（含多样性检查）
# ============================================================

def validate_batch(cases: List[dict]) -> Report:
    report = Report(total=len(cases))

    if not cases:
        report.violations.append(Violation("空集", "ERROR", "用例列表为空"))
        return report

    # 单条验证
    for case in cases:
        report.violations.extend(validate_case(case))

    # ---- 批量级约束 ----

    # 7. 至少覆盖 5 类必覆盖场景中的 3 类
    #    先做中文→英文归一化，避免历史中文产物被判为 "0 类"
    case_types = set()
    for c in cases:
        t = c.get("测试类型", "")
        norm_t, _ = normalize_test_type(t)
        if norm_t in COVERED_SCENARIO_TYPES:
            case_types.add(norm_t)
    if len(case_types) < 3:
        missing = sorted(COVERED_SCENARIO_TYPES - case_types)
        report.violations.append(Violation(
            "场景覆盖", "ERROR",
            f"仅覆盖 {len(case_types)} 类必覆盖场景（{sorted(case_types)}），需至少 3 类；"
            f"缺少：{missing}"
        ))

    # 8. 至少覆盖 4 条实质不同的策略家族（重点）
    family_counts = {}
    for c in cases:
        fam = c.get("策略家族", "")
        fam_main = fam.split("（")[0].split("(")[0].strip()
        if fam_main:
            family_counts[fam_main] = family_counts.get(fam_main, 0) + 1

    distinct_families = len(family_counts)
    if distinct_families < 4:
        report.violations.append(Violation(
            "策略家族多样性", "ERROR",
            f"仅覆盖 {distinct_families} 条策略家族（{family_counts}），需至少 4 条实质不同"
        ))

    # 9. e2e 占比 ≤ 15%
    e2e_count = sum(1 for c in cases if c.get("测试层级") == "e2e")
    e2e_ratio = e2e_count / len(cases) * 100
    if e2e_ratio > 15:
        report.violations.append(Violation(
            "金字塔约束", "ERROR",
            f"e2e 用例占比 {e2e_ratio:.1f}%（{e2e_count}/{len(cases)}），超过 15% 上限"
        ))

    # 10. manual_heuristic 占比 ≤ 20%
    manual_count = sum(
        1 for c in cases
        if c.get("策略家族", "").split("（")[0].split("(")[0].strip() == "manual_heuristic"
    )
    manual_ratio = manual_count / len(cases) * 100
    if manual_ratio > 20:
        report.violations.append(Violation(
            "兜底家族", "ERROR",
            f"manual_heuristic 占比 {manual_ratio:.1f}%（{manual_count}/{len(cases)}），超过 20% 上限"
        ))

    # 11. ≥ 3 条堆同一家族 → 警告
    for fam, cnt in family_counts.items():
        if cnt >= 3 and distinct_families > 1:
            report.violations.append(Violation(
                "多样性自检", "WARN",
                f"策略家族 '{fam}' 堆积 {cnt} 条，考虑重定向到探索不充分的家族"
            ))

    # 策略家族分布摘要
    print("\n=== 策略家族分布 ===")
    for fam in sorted(STRATEGY_FAMILIES):
        cnt = family_counts.get(fam, 0)
        if cnt > 0:
            bar = "#" * cnt
            print(f"  {fam:25s} {cnt:3d} {bar}")
    missing = [f for f in STRATEGY_FAMILIES if f not in family_counts]
    if missing:
        print(f"  未覆盖: {', '.join(missing)}")
    print()

    return report


# ============================================================
# 内置自测用例
# ============================================================

SELF_TEST_CASES = [
    {
        "用例ID": "LOGIN_001",
        "模块": "用户登录",
        "功能点": "密码登录",
        "测试场景": "用户登录_密码正确_正常登录_登录成功",
        "前置条件": "用户已注册且账号正常",
        "操作步骤": "1.输入用户名 2.输入密码 3.点击登录",
        "预期结果": "登录成功，跳转首页，显示用户名",
        "优先级": "P0",
        "测试类型": "functional",
        "测试层级": "integration",
        "策略家族": "equivalence_boundary",
    },
    {
        "用例ID": "LOGIN_002",
        "模块": "用户登录",
        "功能点": "密码登录",
        "测试场景": "用户登录_密码长度5位_边界校验_提示长度不足",
        "前置条件": "无",
        "操作步骤": "1.输入5位密码 2.点击登录",
        "预期结果": "提示密码长度不足",
        "优先级": "P1",
        "测试类型": "boundary",
        "测试层级": "unit",
        "策略家族": "equivalence_boundary",
    },
    {
        "用例ID": "LOGIN_003",
        "模块": "用户登录",
        "功能点": "密码登录",
        "测试场景": "用户登录_任意合法输入_重试次数_≤5次",
        "前置条件": "无",
        "操作步骤": "1.连续输错密码 2.观察重试次数",
        "预期结果": "重试次数不超过5次",
        "优先级": "P1",
        "测试类型": "equivalence",
        "测试层级": "unit",
        "策略家族": "property_based",
    },
    {
        "用例ID": "LOGIN_004",
        "模块": "用户登录",
        "功能点": "密码登录",
        "测试场景": "用户登录_连续失败5次_账号锁定_锁定15分钟",
        "前置条件": "用户已注册",
        "操作步骤": "1.连续输错5次 2.再次尝试登录",
        "预期结果": "账号被锁定15分钟",
        "优先级": "P0",
        "测试类型": "negative",
        "测试层级": "integration",
        "策略家族": "state_model",
    },
    {
        "用例ID": "LOGIN_005",
        "模块": "用户登录",
        "功能点": "密码登录",
        "测试场景": "用户登录_SQL注入payload_安全校验_登录失败",
        "前置条件": "无",
        "操作步骤": "1.用户名输入SQL注入语句 2.点击登录",
        "预期结果": "登录失败，提示错误，无数据泄露",
        "优先级": "P0",
        "测试类型": "security",
        "测试层级": "unit",
        "策略家族": "attack_surface",
    },
]

# 故意不合规的用例（用于测试验证脚本本身）
BAD_CASES = [
    {
        "用例ID": "TC011001",  # 旧格式
        "测试场景": "正常登录",  # 不符合 4 段格式
        "前置条件": "",  # 空
        "测试层级": "e2e",
        "预期结果": "正常显示",  # 模糊
        "测试类型": "functional",
        # 策略家族缺失
    },
    {
        "用例ID": "LOGIN_002",
        "测试场景": "登录_密码错误",
        "前置条件": "用户已注册",
        "测试层级": "e2e",
        "预期结果": "提示错误",
        "测试类型": "negative",
        "策略家族": "manual_heuristic",  # 没注明理由
    },
    {
        "用例ID": "LOGIN_003",
        "测试场景": "登录_空值_提交_报错",
        "前置条件": "无",
        "测试层级": "e2e",
        "预期结果": "应该提示用户名不能为空",  # 含模糊词"应该"
        "测试类型": "negative",
        "策略家族": "unknown_family",  # 不在枚举内
    },
]


# ============================================================
# 多格式加载（JSON / Markdown 表格 / CSV）
# ============================================================

def _md_table_to_cases(text: str) -> List[dict]:
    """把 Markdown 用例表格解析为校验器所需的用例字典列表。

    兼容单元格内的 <br> 多行；自动跳过分隔行（|----|）。
    列名以表头为准，因此 md 表缺某列（如策略家族）时，
    校验器会如实报「该字段为空」，而非静默通过。
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if not lines:
        return []
    header = [h.strip() for h in lines[0].strip("|").split("|")]
    cases = []
    for ln in lines[1:]:
        # 分隔行：仅由 | - : 空格组成
        if set(ln) <= set("|-: "):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        cases.append(dict(zip(header, cells)))
    return cases


def _csv_to_cases(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(r) for r in reader]


def load_cases(path: str) -> List[dict]:
    """按扩展名自动解析：.md / .csv 走表格解析，其余按 JSON 处理。"""
    lower = path.lower()
    if lower.endswith(".md"):
        with open(path, "r", encoding="utf-8") as f:
            return _md_table_to_cases(f.read())
    if lower.endswith(".csv"):
        return _csv_to_cases(path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "test_cases" in data:
        data = data["test_cases"]
    return data


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="测试用例新标准验证脚本")
    parser.add_argument("file", nargs="?", help="JSON 文件路径")
    parser.add_argument("--self-test", action="store_true", help="跑内置合规示例自测")
    parser.add_argument("--bad-test", action="store_true", help="跑内置不合规示例（应 FAIL）")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读 JSON")
    parser.add_argument("--fix-report", action="store_true", help="检测到错误时输出修复建议报告")
    parser.add_argument("--output", "-o", help="将修复建议报告写入文件")
    args = parser.parse_args()

    if args.self_test:
        print("=== 合规示例自测（应 PASS）===")
        report = validate_batch(SELF_TEST_CASES)
        print(report.summary())
        sys.exit(0 if report.passed else 1)

    if args.bad_test:
        print("=== 不合规示例自测（应 FAIL）===")
        report = validate_batch(BAD_CASES)
        print(report.summary())
        if not report.passed:
            print()
            print(report.fix_report())
        sys.exit(0 if not report.passed else 1)  # 不合规应 FAIL，所以反过来

    if args.stdin:
        data = sys.stdin.read()
        cases = json.loads(data)
    elif args.file:
        cases = load_cases(args.file)
    else:
        parser.print_help()
        print("\n示例:")
        print("  python validate_test_cases.py --self-test       # 跑合规示例")
        print("  python validate_test_cases.py --bad-test        # 跑不合规示例")
        print("  python validate_test_cases.py cases.json        # 验证文件")
        print("  python validate_test_cases.py cases.json --fix-report  # 验证+修复建议")
        sys.exit(1)

    if isinstance(cases, dict) and "test_cases" in cases:
        cases = cases["test_cases"]

    report = validate_batch(cases)
    print(report.summary())

    if not report.passed and (args.fix_report or args.output):
        fix_text = report.fix_report()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(fix_text)
            print(f"\n修复建议报告已写入: {args.output}")
        else:
            print()
            print(fix_text)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
