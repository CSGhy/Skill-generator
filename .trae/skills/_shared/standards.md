# 测试用例公共标准（_shared/standards.md）

本文件是测试用例生成系统所有 SKILL 共享的公共配置。各 SKILL 必须引用本文件，不得在各自 SKILL.md 中重复定义以下内容，避免一处改、多处忘。

引用方式：在 SKILL.md 顶部注明「本 SKILL 遵循 [_shared/standards.md](../_shared/standards.md) 的公共标准」。

## 一、用例 ID 格式

格式：`{模块缩写}_{序号}`

- 模块缩写：大写英文，3-6 个字母，由生成时根据功能模块自动确定
- 序号：三位数字，从 001 开始
- 各专门 SKILL 的 ID 前缀如下表，均遵循 `{前缀?}_{模块缩写}_{序号}` 通用格式

| 前缀 | 适用 SKILL | 示例 |
|------|-----------|------|
| （无前缀） | test-case-generator-core | LOGIN_001 |
| `API_` | test-case-api-generator | API_LOGIN_005 |
| `AT_` | test-case-automation-guide | AT_LOGIN_001 |
| `SEC_` | test-case-security-generator | SEC_LOGIN_001 |
| `PERF_` | jmeter-test-script-generator | PERF_LOGIN_001 |
| `XC_` | test-case-xinchuang | XC_LOGIN_001 |
| `EX_` | test-case-execution-helper | EX_LOGIN_001 |
| `BUG_` | test-case-defect-manager | BUG_LOGIN_003 |

> 前缀可叠加，如安全缺陷用 `BUG_SEC_LOGIN_001`。

> ⚠️ 旧的 `TC011001` 纯数字格式已废弃，不再使用。

## 二、用例命名规范

格式：`{模块}_{功能点}_{场景}_{预期结果}`

示例：
- `用户登录_密码正确_正常登录_登录成功`
- `用户登录_密码错误次数超限_账号锁定_账号被锁定`
- `订单创建_库存不足_下单_下单失败提示`

生成测试用例时，"测试场景"字段应按此格式填写。

## 二-B、路径式命名规范（与 ID 格式共存）

除了 `{模块缩写}_{序号}` 的扁平 ID，复杂场景下应同时使用路径式命名组织用例，便于审计日志精确引用：

```
/suite/<策略家族_slug>/<子域>/<功能>/<场景_slug>
```

示例：
- `/suite/equivalence_boundary/user/login/normal_success`
- `/suite/contract_test/user/login/missing_password_field`
- `/suite/mutation_test/user/login/boundary_off_by_one`
- `/suite/attack_surface/user/login/sqli_payload`

> 路径式命名用于**组织和审计引用**，不替代扁平 ID。一条用例同时拥有两者：
> - ID: `LOGIN_001`
> - 路径: `/suite/equivalence_boundary/user/login/normal_success`

> 对齐 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md) 的注册表风格，便于对抗审计代理按路径定位用例集。

## 三、标准用例结构

每条测试用例必须包含以下字段：

| 字段 | 说明 | 必填 | 示例 |
|------|------|------|------|
| 用例ID | 唯一标识，格式 `{模块缩写}_{序号}` | 是 | LOGIN_001 |
| 模块 | 功能模块 | 是 | 用户登录 |
| 功能点 | 具体功能点 | 是 | 密码登录 |
| 测试场景 | 按 `模块_功能点_场景_预期` 格式 | 是 | 用户登录_密码正确_正常登录_登录成功 |
| 前置条件 | 执行用例前必须满足的条件 | 是 | 用户已注册且账号正常 |
| 操作步骤 | 1、2、3... 按步骤描述 | 是 | 1.输入用户名<br>2.输入密码<br>3.点击登录 |
| 预期结果 | 明确、可验证的预期输出 | 是 | 登录成功，跳转到首页，显示用户名 |
| 优先级 | P0/P1/P2/P3 | 是 | P0 |
| 测试类型 | 见「五、测试类型枚举」**须填英文枚举值** | 是 | `functional` |
| 测试层级 | unit/integration/e2e | 是 | e2e |
| 策略家族 | 见「五-B、测试策略家族」 | 是 | equivalence_boundary |
| 能杀死的突变类型 | 该用例能杀死的代码突变（文件:行号 原运算符→突变后） | 否 | login.py:42 的 ≤→< |
| 覆盖的分支 | 该用例覆盖的代码分支（行号或分支编号） | 否 | login.py:38-45 |
| 保护的状态转移 | 该用例保护的状态机转移 | 否 | 未登录 → 已登录 |
| 风险等级 | 高/中/低 | 否 | 高 |
| 关联缺陷ID | 该用例触发并记录的缺陷ID（对齐 [test-case-defect-manager](../test-case-defect-manager/SKILL.md)） | 否 | BUG_LOGIN_003 |

> ⚠️ 「前置条件」「测试层级」「策略家族」是必填字段，缺失视为不合格用例。
> 「能杀死的突变类型」「覆盖的分支」「保护的状态转移」为可选字段，复杂审计场景下应填写（对齐 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md)）。

## 四、API 用例结构

| 字段 | 说明 | 必填 | 示例 |
|------|------|------|------|
| 用例ID | 格式 `API_{模块缩写}_{序号}` | 是 | API_LOGIN_001 |
| 接口名称 | 接口名称 | 是 | 用户登录 |
| 请求方法 | HTTP 方法 | 是 | POST |
| 请求URL | 接口 URL | 是 | /api/v1/login |
| 请求参数 | JSON 格式 | 是 | {"username":"test","password":"123456"} |
| 前置条件 | 调用前必须满足的条件 | 是 | 用户已注册 |
| 预期状态码 | 预期 HTTP 状态码 | 是 | 200 |
| 预期响应 | 预期响应内容 | 是 | {"code":0,"msg":"success"} |
| 测试类型 | 见「五、测试类型枚举」**须填英文枚举值** | 是 | `functional` |
| 测试层级 | unit/integration/e2e | 是 | integration |
| 策略家族 | 见「五-B、测试策略家族」 | 是 | contract_test |
| 能杀死的突变类型 | 该用例能杀死的代码突变 | 否 | auth.py:15 的 ==→= |
| 覆盖的分支 | 该用例覆盖的代码分支 | 否 | auth.py:12-20 |
| 保护的状态转移 | 该用例保护的状态机转移 | 否 | 未认证 → 已认证 |
| 优先级 | P0/P1/P2/P3 | 是 | P0 |
| 关联缺陷ID | 该用例触发并记录的缺陷ID（对齐 [test-case-defect-manager](../test-case-defect-manager/SKILL.md)） | 否 | API_BUG_LOGIN_003 |

> ⚠️ API 用例的「策略家族」最常使用 `contract_test`（契约测试）或 `equivalence_boundary`（等价类+边界值），但也可使用其他家族。

## 五、测试类型枚举

| 类型 | 说明 |
|------|------|
| functional | 功能测试（正常流程） |
| boundary | 边界值测试 |
| equivalence | 等价类测试 |
| negative | 负向/异常测试 |
| integration | 集成测试 |
| unit | 单元测试 |
| e2e | 端到端测试 |
| compatibility | 兼容性测试 |
| security | 安全测试（XSS/SQL注入/越权等） |
| performance | 性能测试 |

所有 SKILL 的 `--type` 参数枚举必须与此表一致。

> ⚠️ **强制：本字段一律使用英文枚举值**。用例产物（Markdown 表格 / CSV / JSON）中的「测试类型」列必须填写左列的英文 slug，
> 不得填写中文（如 ~~功能测试~~ / ~~边界测试~~）。中文仅允许出现在自然语言说明、章节标题中，不作为字段值。
> [_shared/validate_test_cases.py](./validate_test_cases.py) 会对该字段做逐条枚举校验；
> 历史产物中的中文值会经归一化映射自动转换并告警，但新产物不得再使用中文。

## 五-B、测试策略家族（与测试类型正交）

「测试类型」描述用例**性质**（功能/边界/异常/兼容/安全/性能）；
「策略家族」描述测试**方法论**（等价类/属性/契约/变异/状态机/模糊/性能形态/攻击面）。
两者正交，每条用例必须同时标注一个测试类型和一个策略家族。

| 策略家族 slug | 核心思想 | 推荐工具 | 我们当前是否原生支持 |
|--------------|---------|---------|---------------------|
| equivalence_boundary | 等价类划分 + 边界值扫描 | pytest-parametrize / jest-each | ✅ 原生支持 |
| property_based | Hypothesis 找不变式 | Hypothesis (Python) / fast-check (JS/TS) | ⚠️ 需 automation-guide 配合 |
| contract_test | Pact 消费者驱动契约 | Pact / Spring Cloud Contract | ⚠️ 需 automation-guide 配合 |
| mutation_test | Stryker 反向驱动盲点 | Stryker / mutmut | ⚠️ 需 automation-guide 配合 |
| state_model | 状态机模型测试 | AltWalker / GraphWalker | ⚠️ 需 automation-guide 配合 |
| fuzz_chaos | 模糊测试 + 混沌工程 | Atheris / Chaos Mesh | ⚠️ 需 automation-guide 配合 |
| perf_profile | 阶梯 + 脉冲 + 雪崩负载 | Locust / k6 / Gatling | ⚠️ 需 automation-guide 配合 |
| attack_surface | 注入 / 越权 / SSRF / 重放 | Semgrep / OWASP ZAP / Burp | ⚠️ 需 automation-guide 配合 |
| manual_heuristic | 手写启发式（不属于上述家族时） | 无 | ✅ 原生支持 |

> 「manual_heuristic」是兜底家族，仅当用例不属于上述 8 条方法论时使用。生成器应优先匹配前 8 条家族，避免滥用兜底。

> 对齐 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md) 的核心约束：每批用例**至少覆盖 4 条实质不同的策略家族**，不允许"用例措辞不同但思路相同"冒充多样性。

## 六、测试层级与金字塔比例

遵循 [测试金字塔原则](../../rules/测试金字塔原则.md)：

| 层级 | 占比目标 | 说明 |
|------|---------|------|
| unit（单元测试） | 70% | 函数/方法/组件级，毫秒级执行 |
| integration（集成测试） | 20% | 模块间调用、接口集成 |
| e2e（端到端测试） | 10% | 完整业务主流程，P0 级核心场景 |

生成用例时必须：
1. 为每条用例标注 `测试层级` 字段
2. 控制 e2e 用例数量在 P0 核心主流程范围内（建议 ≤ 几十条）
3. 优先产出 unit 层用例，避免「倒金字塔」

## 七、优先级定义

| 优先级 | 定义 | 举例 |
|--------|------|------|
| P0 | 阻断级，核心主流程，不通过不能发布 | 支付成功、登录成功 |
| P1 | 重要功能，严重影响用户使用 | 列表查询、表单提交 |
| P2 | 次要功能，不影响核心流程 | 筛选排序、导出功能 |
| P3 | 体验优化、边缘场景 | UI文案、提示语微调 |

## 八、FIRST 原则（用例设计必须遵循）

- **Fast（快速）**：用例执行要快，避免不必要的等待和依赖
- **Independent（独立）**：用例之间互不依赖，可单独执行，执行顺序不影响结果
- **Repeatable（可重复）**：多次执行结果一致，不依赖外部不稳定因素
- **Self-validating（自验证）**：有明确的断言/预期结果，不需要人工判断
- **Timely（及时）**：需求确定后及时编写，与开发同步推进

## 九、必覆盖场景类型

每批生成的用例必须覆盖以下 5 类场景（视文档类型按需侧重），**至少覆盖其中 3 类**：

| # | 场景分类 | 对应测试类型枚举值 | 说明 |
|---|---------|------------------|------|
| 1 | 正常场景 | `functional` | 主流程正向验证、常用数据组合 |
| 2 | 边界值 | `boundary` | 数值边界（最大/最小/0/空/null）、长度边界（最短/最长/为空）、集合边界（空集合/单元素/满容量） |
| 3 | 等价类 | `equivalence` | 有效等价类（代表性数据）、无效等价类（各类非法输入） |
| 4 | 异常场景 | `negative` | 网络异常/超时、依赖服务不可用、权限不足、数据冲突/重复提交、资源耗尽 |
| 5 | 兼容性 | `compatibility` | 不同浏览器/设备/操作系统、不同版本兼容、数据迁移兼容 |

> ⚠️ 「场景分类」是**设计视角的分类名**（中文，用于沟通与检查清单）；
> 「测试类型枚举值」是**用例字段的实际取值**（英文 slug，见「五、测试类型枚举」）。
> 二者一一对应，生成产物时一律填写右列的英文值。
> 校验规则由 [_shared/validate_test_cases.py](./validate_test_cases.py) 的 `COVERED_SCENARIO_TYPES` 执行。

## 十、模块编号参考表（可扩展）

生成时根据实际功能模块确定缩写，下表为常用参考：

| 模块 | 缩写 |
|------|------|
| 用户管理 | USER |
| 用户登录 | LOGIN |
| 用户注册 | REG |
| 商品管理 | PROD |
| 购物车 | CART |
| 订单管理 | ORDER |
| 支付管理 | PAY |
| 退款管理 | REFUND |
| 权限管理 | PERM |
| 文件上传 | FILE |

> 实际模块不在表中时，由生成器根据功能名自动确定 3-6 字母大写缩写。

## 十-B、缺陷 ID 格式（对齐 test-case-defect-manager）

格式：`BUG_{模块缩写}_{序号}`

- 模块缩写：与本文件「十、模块编号参考表」一致
- 序号：三位数字，从 001 开始
- 安全缺陷可加 `SEC_` 前缀：`BUG_SEC_LOGIN_001`

示例：
- `BUG_LOGIN_003`：登录模块第 3 个缺陷
- `BUG_CART_012`：购物车模块第 12 个缺陷
- `BUG_SEC_LOGIN_001`：登录模块第 1 个安全缺陷

> 缺陷生命周期管理、用例↔缺陷双向追溯详见 [test-case-defect-manager](../test-case-defect-manager/SKILL.md)。
> 缺陷分级（P0-P4）、生命周期、附件要求遵循 [缺陷报告规范](../../rules/缺陷报告规范.md)。

## 十一、输出 schema 校验

生成用例后必须自检以下事项，任一不通过则重试生成（最多 1 次）：

- [ ] 每条用例 ID 格式符合 `{模块缩写}_{序号}`
- [ ] 每条用例含「前置条件」字段（非空）
- [ ] 每条用例含「测试层级」字段（值为 unit/integration/e2e 之一）
- [ ] 每条用例含「策略家族」字段（值为「五-B」枚举之一）
- [ ] 每条用例的「测试场景」符合 `模块_功能点_场景_预期` 格式
- [ ] 至少覆盖 5 类必覆盖场景中的 3 类
- [ ] 至少覆盖 4 条实质不同的策略家族
- [ ] e2e 用例数量不超过总用例数的 15%
- [ ] 不使用「可能」「大概」「应该」等模糊表述
- [ ] 预期结果具体可验证（不说"正常显示"，要说"显示XX内容"）
- [ ] 用例执行后若触发缺陷，「关联缺陷ID」字段必须回写（格式 `BUG_{模块缩写}_{序号}`，对齐 [test-case-defect-manager](../test-case-defect-manager/SKILL.md)）

## 十一-B、对抗审计输出契约（对齐 multi-agent-test-auditor）

对每个用例集，评审/审计代理**必须**返回下列 5 类结论之一：

1. **未杀死的突变**：含突变位置（文件:行号）、突变类型（如 `≤→<`）、为什么现存用例无法发现
2. **未覆盖的分支/状态转移**：含源码行号或状态图转移编号
3. **具体反例**：输入参数 + 期望行为 + 实际行为 + 复现脚本
4. **契约缺口**：消费者期望未被覆盖的契约字段
5. **无条件通过**：必须附逐用例验证（每个用例杀死哪些突变、覆盖哪些分支、保护哪些状态转移）

禁止的审计输出（视为无效，重新派发审计）：
- "覆盖很高了"
- "看起来够"
- "应该没问题"
- "标准做法"
- "常规覆盖足够"
- 任何没有具体突变/分支/反例/契约缺口的状态报告

> 本契约对齐 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md) 的「对抗审计清单」段。
> 简单评审场景（如本系列生成器）可降级使用——只要求返回 5 类结论之一，不强制逐用例验证；复杂审计场景（核心业务流程/安全测试）必须严格按完整契约执行，建议直接转交 multi-agent-test-auditor。

## 十一-C、完成闸门（复杂场景适用）

简单用例生成场景：通过「十一、输出 schema 校验」即可视为完成。

复杂审计场景（核心业务流程/安全测试/缺陷根因分析）：必须通过下列全部闸门才算完成：

| 闸门 | 阈值 | 说明 |
|------|------|------|
| 变异分数 | ≥ 80% | Stryker / mutmut 全量跑，未杀死突变清单 + 反推补丁用例 |
| 行覆盖率 | ≥ 85% | Coverage.py / Istanbul / JaCoCo |
| 分支覆盖率 | ≥ 75% | — |
| 状态转移覆盖率 | ≥ 90% | 按待测对象的状态图调整 |
| 静态扫描 critical | = 0 | SonarQube / Semgrep / Snyk |
| 性能基线 | 不退化 | P95/P99/错误率不超过基线阈值 |
| 独立审计签字 | ≥ 3 人 | 不是用例作者，每份审计引用具体突变/分支/反例 |
| GOAL_STATE 终行 | 必须输出 | 字面行 `GOAL_STATE: complete` 或 `GOAL_STATE: blocked_<reason>` |

> 任一闸门未过 → 回到生成/审计流程，不允许宣布完成。
> `blocked_<reason>` 也是合法结果——盲点无法补全时诚实标记阻塞，不要假装完成。
> 本闸门对齐 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md) 的「完成闸门」段。

## 十二、错误处理

| 异常情况 | 处理方式 |
|---------|---------|
| 输入文档为空或无法识别类型 | 报告"无法识别文档类型"，请用户明确指定 `--doc-type` |
| LLM 输出用例数为 0 | 重试 1 次；仍为 0 则报告"生成失败"，不输出空表格 |
| 用户指定 `--type` 但当前 SKILL 不支持 | 报告"当前 SKILL 不支持该测试类型"，建议转交对应 SKILL |
| 输出 schema 校验不通过 | 重试 1 次；仍不通过则输出当前结果并标注"未通过 schema 校验" |

## 十三、反模式清单（显式禁止）

下列行为视为不合格输出，必须避免：

### 测试设计反模式（对齐 multi-agent-test-auditor）
- ❌ 把行覆盖率 100% 当成完成（覆盖率不等于质量）
- ❌ 把 happy path 通过当成完成
- ❌ 让用例作者当自己的审计者（必须独立审计）
- ❌ 跳过变异测试就宣布完成
- ❌ 因变异分数低就降低阈值而非补用例
- ❌ flaky 测试置之不理就合入
- ❌ 性能基线退化未触发闸门
- ❌ 静态扫描 critical 未清零就合入
- ❌ 用户要可执行测试代码却返回测试方案描述

### 测试金字塔反模式（对照 [测试金字塔原则](../../rules/测试金字塔原则.md)）
- ❌ 冰淇淋蛋筒模式：单元测试极少 + 大量依赖 UI 自动化
- ❌ 倒金字塔：上层测试比下层多
- ❌ 只有 E2E：啥都想通过 UI 测，跑一次要几小时

### 多样性反模式（对齐 multi-agent-test-auditor）
- ❌ 用例措辞不同但思路相同冒充多样性
- ❌ 所有代理收敛到同一家族（如都堆在路径覆盖）
- ❌ 把"覆盖率已 100%"但变异分数低于阈值标记为完成
- ❌ 滥用 `manual_heuristic` 兜底家族逃避方法论匹配
