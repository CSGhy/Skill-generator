# 技能库审查报告（2026-09-04）

审查对象：`.trae/skills/` 下 16 个 SKILL + `_shared/`
触发原因：2026-09-04 09:43–09:45 通过 Trae IDE 改动了 5 个文件

## 一、今日改动清单（按 mtime 精确定位）

| 时间 | 文件 | 性质 |
|------|------|------|
| 09:43 | `_shared/standards.md` | 公共标准 |
| 09:43 | `_shared/validate_test_cases.py` | 校验器 |
| 09:43 | `test-case-generator/SKILL.md` | 主入口 |
| 09:44 | `test-case-xinchuang/SKILL.md` | v1.0.1 |
| 09:45 | `test-case-execution-helper/SKILL.md` | v1.0.1 |

改动内容（从版本历史读出）：
- **测试类型由中文改为英文枚举**（对齐 standards.md 五、测试类型枚举）
- xinchuang 补充 GB/T 标准号（SM2: GB/T 32918-2016、SM3: GB/T 32905-2016、SM4: GB/T 32907-2016、国密TLS: GM/T 0024-2014）
- xinchuang 补充 knowledge-base 生成前查询 / self-improving-helper 生成后闭环
- execution-helper 补充路由规则、偶现转缺陷关单条件（连续 ≥3 轮未复现）、与 report-generator 数据传递

> 方向正确，质量不错。问题在于**迁移未完成**。

---

## 二、P0 — 阻断级问题

### P0-1 英文枚举迁移未完成，校验链断裂

**现象**：昨天校验 PASS 的 `demo_login_cases.md`，今天变 FAIL

```
[ERROR] 场景覆盖: 仅覆盖 0 类必覆盖场景（set()），需至少 3 类
结论: FAIL
```

**根因链**：
1. `standards.md` 五、 定义测试类型为英文枚举（`functional`/`boundary`/...）
2. `validate_test_cases.py` 的 `TEST_TYPES` 与 `COVERED_SCENARIO_TYPES` 同步改为英文
3. 但下游 SKILL 的示例模板、生成产物仍输出中文（功能测试/边界测试/...）
4. 中文值匹配不上英文集合 → 覆盖率判定为 0 类 → 批量规则 FAIL

**中文测试类型残留分布**（按行数）：

| SKILL | 残留行数 | 严重度 |
|-------|---------|--------|
| jmeter-test-script-generator | 28 | 高 |
| test-case-generator-core | 25 | 高 |
| test-case-api-generator | 15 | 高 |
| test-case-security-generator | 13 | 高 |
| test-case-generator | 13 | 高 |
| knowledge-base | 13 | 中 |
| test-case-report-generator | 5 | 中 |
| test-case-execution-helper | 3 | 低 |
| multi-agent-test-auditor | 2 | 低 |
| test-case-reviewer | 1 | 低 |
| **合计** | **118** | |

已完成英文化的仅：`test-case-xinchuang`、`test-case-execution-helper`（部分）、`test-case-generator`（仅 `--type` 枚举）。

### P0-2 standards.md 自身自相矛盾

| 位置 | 内容 | 冲突 |
|------|------|------|
| 第 75 行（三、标准用例结构） | 测试类型 示例 = `功能测试` | ❌ 中文 |
| 第 99 行（四、API 用例结构） | 测试类型 示例 = `功能测试` | ❌ 中文 |
| 第 110–125 行（五、测试类型枚举） | `functional`/`boundary`/... | ✅ 英文 |
| 第 181–189 行（九、必覆盖场景类型） | 正常场景/边界值/等价类/异常场景/兼容性 | ❌ 中文，且未与英文枚举建立映射 |

**后果**：严格照 standards.md 字段表写出的用例，必然被校验器判 FAIL。标准自身不可执行。

---

## 三、P1 — 一致性问题

### P1-3 校验器不逐条校验「测试类型」，失败信息误导

`validate_case()` 已校验：用例ID、前置条件、测试层级、策略家族、测试场景、预期结果
**未校验**：测试类型是否在 `TEST_TYPES` 内

后果：单条中文值静默通过，只在批量规则处以「0 类」报错，无法定位是哪条用例出问题。

### P1-4 主入口与 core 的 `--type` 枚举矛盾

| 文件 | 枚举 |
|------|------|
| `test-case-generator:31` / `:54` | `...compatibility`&#124;`security`&#124;`performance`&#124;`all` |
| `test-case-generator-core:29` | `...compatibility`&#124;`all`（注明 security/performance 转专门 SKILL） |

后果：主入口承诺可生成 security/performance，转给 core 后被拒 → 用户从主入口调用会撞墙。
另：`test-case-generator:248` / `:270` 简介仍写中文「功能/边界/负向/集成」。

### P1-5 版本元信息未同步（3 处）

| SKILL | 版本历史 | frontmatter | 状态 |
|-------|---------|-------------|------|
| test-case-xinchuang | v1.0.1 (2026-09-04) | `1.0.0` / `2026-09-03` | ❌ 未同步 |
| test-case-execution-helper | v1.0.1 (2026-09-04) | `1.0.0` / `2026-09-03` | ❌ 未同步 |
| test-case-generator | 无 09-04 条目 | `3.3.0` / `2026-09-03` | ❌ 改动未记录 |

---

## 四、P2 — 遗留问题（非今日引入）

### P2-6 断链（全库 436 个相对引用中唯一 1 处）

```
multi-agent-test-auditor/prompt-template.md:4
> 配套 SKILL：[.trae/skills/multi-agent-test-auditor/SKILL.md](../skills/multi-agent-test-auditor/SKILL.md)
```
从该目录出发会解析到 `.trae/skills/skills/...`（不存在），应为 `./SKILL.md`。

### P2-7 缺 `version` frontmatter（3 个）

`lanhu-requirements-doc`、`multi-agent-research-prover`、`multi-agent-test-auditor`

---

## 五、已验证无问题项

| 检查项 | 结果 |
|--------|------|
| 校验器自测 `--self-test` | ✅ PASS（5 用例 / 0 错误 / 0 警告） |
| 校验器反向测试 `--bad-test` | ✅ 正常报错 |
| 校验器 `.md` 解析能力 | ✅ 未被破坏 |
| 全库断链（436 引用） | ✅ 仅 1 处（P2-6） |
| 旧 ID 格式（TC001/API001） | ✅ 无残留（knowledge-base:875 为变更说明，非用例） |
| 已移除 SKILL 的残留引用 | ✅ 无 |
| 存储路径（feedback.json / trace.json） | ✅ 一致 |
| junction 注册链路 | ✅ 16 个链接完好，跨链读取正常 |

---

## 六、修复方案建议

### 方案 A：继续推进全量英文化（推荐）
- 改 standards.md 第 75/99 行示例 → `functional`
- 九、必覆盖场景类型 补中文↔英文映射表
- 脚本批量英文化 10 个 SKILL 的 118 行
- 优点：标准唯一、彻底；缺点：改动面大，需回归验证

### 方案 B：校验器兼容中英双语
- `validate_test_cases.py` 加中文→英文归一化映射，中文值自动转换（可附 WARN）
- 优点：改动小、向后兼容旧产物；缺点：两套写法长期共存

### 方案 C：折中（最稳）
- 标准明确「枚举一律英文」，示例全部英文化（同 A）
- 校验器加归一化映射作兜底，中文值转英文并告警（同 B）
- 新增逐条「测试类型」枚举校验（修 P1-3）
- 同步 generator 与 core 的 `--type` 枚举（修 P1-4）
- 补齐 3 处版本元信息 + 1 处断链（修 P1-5、P2-6）

---

## 七、方案 C 执行结果（已验证 ✅）

用户确认按 **方案 C** 执行（2026-09-04 下午）。全部修复已完成并回归通过。

### 已落地修复
| 项 | 修复内容 | 文件 |
|----|---------|------|
| P0-2 | standards.md 第 75/99 行示例值 `功能测试`→`functional`；第 181–189 行必覆盖场景补中文↔英文映射；五、补充「枚举一律英文」强制说明 | `_shared/standards.md` |
| P0-1 | 校验器新增中文→英文归一化映射（中文值自动转英文 + WARN，兼容旧产物）；批量场景覆盖统计走归一化 | `_shared/validate_test_cases.py` |
| P1-3 | `validate_case()` 新增逐条「测试类型」枚举校验，非法值精确报 ERROR 并定位到用例 ID | `_shared/validate_test_cases.py` |
| P0-1 漏网 | 迁移脚本原只匹配 JSON 风格 `"测试类型": "功能测试"`，漏掉**表格单元格值**。补改 generator-core 示例表 7 处单元格 `功能测试/边界测试/等价类测试/负向测试/安全测试`→英文 | `test-case-generator-core/SKILL.md` |
| P1-4 | generator `--type` 枚举移除 `security`/`performance`（与 core 一致）；简介行中文→英文；core 同步注明转专门 SKILL | `test-case-generator`, `test-case-generator-core` |
| P1-5 | xinchuang / execution-helper frontmatter → 1.0.1；generator 补 v3.3.1 条目 | 3 个 SKILL |
| P2-6 | `prompt-template.md:4` 断链 `../skills/...` → `./SKILL.md` | `multi-agent-test-auditor` |
| 真 bug | `xinchuang` 把测试类型 `compatibility` 误标为策略家族 → 改为 `equivalence_boundary`；generator:444 散文同步修正 | `test-case-xinchuang`, `test-case-generator` |
| 真 bug | core 示例 `LOGIN_004` 测试场景仅 3 段（标准要 4 段）→ 补 `锁定15分钟` 段 | `test-case-generator-core` |

> 说明：118 行粗筛中，jmeter(28)/execution-helper(3)/auditor(2)/reviewer(1) 实际为自然语言（负载类型、人设、章节标题），**非枚举值，未改动**；真正需改的枚举值约 30 处已清零。

### 回归验证结果
| 检查 | 结果 |
|------|------|
| 校验器自测 `--self-test` | ✅ PASS（5 用例 / 0 错误 / 0 警告） |
| 英文标杆产物 `demo_login_cases.md` | ✅ PASS（0/0） |
| 中文值兜底（临时 4 用例） | ✅ PASS（0 错误，4 个归一化 WARN，已定位到 ID） |
| 反向用例 `--bad-test` | ✅ 正常报 11 错误 |
| 值位置中文测试类型残留复扫 | ✅ **0** |
| 非法策略家族 `compatibility` 误用复扫 | ✅ **0**（仅 xinchuang:93 字面邻近触发 grep，已修正无实患） |
| 全库断链复扫 | ✅ **0** |
| `_shared` 临时脚本清理 | ✅ 已删除 `_migrate_test_type.py` / `_audit_skill_examples.py` / `__pycache__` |

### 遗留（已知、非阻断、不在方案 C 范围）
各 SKILL 内置**示例用例表为教学性少行 demo**，不满足「策略家族多样性≥4 / 金字塔 e2e≤15% / 场景覆盖≥3 类」等批量硬门槛——这是示例性质固有局限，非功能缺陷。如需让每个 SKILL 的示范本身也 100% 过校验，需把每个示例扩成 6+ 条多样例套件，属下一轮优化。

---

*审查时间：2026-09-04 ｜ 方案 C 执行完成：2026-09-04*
