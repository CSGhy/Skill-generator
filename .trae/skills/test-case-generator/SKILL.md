---
name: "test-case-generator"
description: "测试用例生成器主入口 - 根据用户需求智能选择合适的专门SKILL，包括核心生成器、API测试、自动化指导、测试用例评审、测试报告等"
version: "3.3.1"
last_updated: "2026-09-04"
---

# 测试用例生成器

本 SKILL 遵循 [_shared/standards.md](../_shared/standards.md) 的公共标准。

这个skill是测试用例生成系统的主入口，它会根据您的需求智能选择合适的专门SKILL来完成任务。我们提供了多个专门的SKILL，每个SKILL专注于特定的测试场景，提供更专业、更高效的服务。

**主入口职责**：文档类型识别、SKILL 路由、闭环协调（生成前查 knowledge-base、生成后写 self-improving-helper）。文档类型识别结果会传给被调用的子 SKILL，子 SKILL 不再重复识别。

## 📋 快速参考卡片

### 基本指令格式

```
/test-case-generator [功能描述或文档] [选项]
```

#### 参数说明

**必填参数**：
- `function`：功能描述、需求文档或文档路径（必填）

**可选参数**：
- `--doc-type`：文档类型，可选值：`prd`|`requirement`|`api`|`user-story`|`code`|`auto`（默认：`auto`自动识别）
- `--type`：测试类型，可选值：`functional`|`boundary`|`equivalence`|`negative`|`integration`|`unit`|`e2e`|`compatibility`|`security`|`performance`|`all`（默认：`all`）。注：本 SKILL 是**路由入口**，`security`/`performance` 会被转交专门 SKILL 生成（`security` → test-case-security-generator，`performance` → jmeter-test-script-generator），不在此处直接产出
- `--standard`：测试标准，可选值：`standard`|`api`|`automation`|`custom`（默认：`standard`）
- `--format`：输出格式，可选值：`md`|`csv`|`excel`|`json`|`xml`|`word`（默认：`md`）
- `--priority`：优先级范围，可选值：`p0`|`p1`|`p2`|`p3`|`all`（默认：`all`）
- `--coverage`：测试覆盖率，可选值：`100`|`80`|`60`|`40`（默认：`100`）

#### 参数Schema

```json
{
  "function": {
    "type": "string",
    "minLength": 1,
    "description": "功能描述、需求文档或文档路径"
  },
  "doc-type": {
    "type": "string",
    "enum": ["prd", "requirement", "api", "user-story", "code", "auto"],
    "default": "auto",
    "description": "文档类型"
  },
  "type": {
    "type": "string",
    "enum": ["functional", "boundary", "equivalence", "negative", "integration", "unit", "e2e", "compatibility", "security", "performance", "all"],
    "default": "all",
    "description": "测试类型"
  },
  "standard": {
    "type": "string",
    "enum": ["standard", "api", "automation", "custom"],
    "default": "standard",
    "description": "测试标准"
  },
  "format": {
    "type": "string",
    "enum": ["md", "csv", "excel", "json", "xml", "word"],
    "default": "md",
    "description": "输出格式"
  },
  "priority": {
    "type": "string",
    "enum": ["p0", "p1", "p2", "p3", "all"],
    "default": "all",
    "description": "优先级范围"
  },
  "coverage": {
    "type": "integer",
    "enum": [100, 80, 60, 40],
    "default": 100,
    "description": "测试覆盖率"
  }
}
```

### 常用命令

| 命令 | 说明 |
|------|------|
| "测试[功能名]" | 生成测试用例 |
| "生成[功能名]测试用例" | 从文档生成测试用例 |
| "测试[接口名]API" | 生成API测试用例 |
| "评审测试用例" | 评审测试用例质量 |
| "生成测试报告" | 生成测试报告 |

> 💡 **提示**：您可以直接粘贴PRD、需求文档或接口文档，系统会自动识别文档类型并选择合适的专门SKILL来完成任务。

## 📑 文档目录

### 快速入门
- [📋 快速参考卡片](#快速参考卡片)
- [快速开始](#快速开始)
- [SKILL选择指南](#skill选择指南)

### 专门SKILL
- [test-case-generator-core](#test-case-generator-core) - 核心生成器
- [test-case-api-generator](#test-case-api-generator) - API测试专门
- [test-case-security-generator](#test-case-security-generator) - 安全测试专门
- [test-case-automation-guide](#test-case-automation-guide) - 自动化指导
- [test-case-reviewer](#test-case-reviewer) - 测试用例评审
- [test-case-report-generator](#test-case-report-generator) - 测试报告
- [test-case-defect-manager](#test-case-defect-manager) - 缺陷管理
- [jmeter-test-script-generator](#jmeter-test-script-generator) - 性能测试脚本
- [test-case-xinchuang](#test-case-xinchuang) - 信创/国产化/政务适配
- [test-case-execution-helper](#test-case-execution-helper) - 手工测试执行助手

## 快速开始

### 一句话示例

用户上传文档，系统自动识别文档类型，智能选择合适的专门SKILL，生成专业的测试用例或提供相应的服务。

### 快速使用流程

1. **开场**：智能体自我介绍，说明支持的文档类型和服务
2. **文档接收**：用户粘贴文档内容或上传文档文件
3. **智能分析**：智能体自动识别文档类型和用户需求
4. **SKILL选择**：智能体根据需求选择合适的专门SKILL
5. **服务提供**：专门的SKILL提供专业的服务
6. **后续服务**：根据用户需求提供后续服务（评审、报告、自动化等）

### 典型对话示例

**示例1：从PRD生成测试用例**

**用户**：[粘贴PRD文档]

**智能体**：已识别到这是一份PRD文档，包含以下功能模块：
1. 用户注册/登录
2. 商品浏览
3. 购物车管理
4. 订单支付

建议使用**test-case-generator-core**来生成标准测试用例。是否继续？

**用户**：继续

**智能体**：正在调用**test-case-generator-core**生成测试用例...

[生成测试用例表格]

测试用例已生成，共45条。是否需要：
1. 评审测试用例质量（调用test-case-reviewer）
2. 生成测试报告（调用test-case-report-generator）
3. 转换为自动化测试（调用test-case-automation-guide）

**示例2：从接口文档生成API测试用例**

**用户**：[粘贴接口文档]

**智能体**：已识别到这是一份接口文档，包含以下接口：
1. 用户登录接口
2. 用户注册接口
3. 获取用户信息接口

建议使用**test-case-api-generator**来生成API测试用例。是否继续？

**用户**：继续

**智能体**：正在调用**test-case-api-generator**生成API测试用例...

[生成API测试用例表格]

API测试用例已生成，共15条。是否需要：
1. 导出为Postman格式
2. 评审测试用例质量（调用test-case-reviewer）
3. 生成测试报告（调用test-case-report-generator）

## SKILL选择指南

### 根据文档类型选择

| 文档类型 | 推荐SKILL | 说明 |
|---------|----------|------|
| PRD | test-case-generator-core | 生成标准测试用例（含 unit/integration/e2e 分层） |
| 需求说明 | test-case-generator-core | 生成标准测试用例 |
| 接口文档 | test-case-api-generator | 生成API测试用例 |
| 用户故事 | test-case-generator-core | 生成标准测试用例 |
| 代码 | test-case-generator-core + test-case-automation-guide | core 生成单元测试用例，automation-guide 转换为自动化代码 |
| 安全需求/威胁建模 | test-case-security-generator | 生成 OWASP Top 10 安全测试用例 |
| 性能需求/压测目标 | jmeter-test-script-generator | 生成 JMeter .jmx 性能测试脚本 |
| 信创/国产化/政务需求 | test-case-xinchuang | 生成国产栈兼容/合规/国密用例 |
| 手工执行/探索式/巡检/复现 | test-case-execution-helper | 执行记录与偶现复现辅助 |

### 根据需求选择

| 需求 | 推荐SKILL | 说明 |
|------|----------|------|
| 生成测试用例 | test-case-generator-core | 生成标准测试用例 |
| 生成API测试用例 | test-case-api-generator | 生成API测试用例 |
| 生成安全测试用例 | test-case-security-generator | 生成 OWASP Top 10 / attack_surface 用例 |
| 生成性能测试脚本 | jmeter-test-script-generator | 生成 JMeter .jmx 脚本 |
| 转换为自动化测试 | test-case-automation-guide | 提供自动化指导 |
| 评审测试用例质量 | test-case-reviewer | 评审测试用例 |
| 生成测试报告 | test-case-report-generator | 生成测试报告 |
| 缺陷管理/追溯 | test-case-defect-manager | 缺陷生命周期管理与用例↔缺陷追溯 |
| 信创适配/国产化/政务合规测试 | test-case-xinchuang | 国产OS/数据库/浏览器/国密/专网 |
| 手工测试执行/探索式/巡检/偶现复现 | test-case-execution-helper | 执行记录与复现辅助 |

### 根据测试标准选择

| 测试标准 | 推荐SKILL | 说明 |
|---------|----------|------|
| 标准测试规范 | test-case-generator-core | 标准测试用例 |
| API测试规范 | test-case-api-generator | API测试用例 |
| 自动化测试规范 | test-case-automation-guide | 自动化测试指导 |
| 自定义测试标准 | test-case-generator-core | 支持自定义模板 |

### 复杂审计场景转交（对齐 multi-agent-test-auditor）

本系列生成器面向**单视角 / 中等复杂度**场景。下列复杂审计场景应直接转交 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md)，不要硬塞给本系列：

| 复杂场景 | 转交方 | 理由 |
|---------|--------|------|
| 核心业务流程回归套件设计（支付/风控/订单状态机） | multi-agent-test-auditor | 需要多视角对抗式审计 |
| 安全测试（注入/越权/SSRF/重放/供应链） | multi-agent-test-auditor | 需要攻击面分析+对抗审计 |
| 缺陷根因分析（多假设并存、对抗证伪） | multi-agent-test-auditor | 需要变异驱动+反例证伪 |
| 需要变异分数报告/覆盖率盲点扫描 | multi-agent-test-auditor | 需要计算闸门，本系列不产出 |
| 需要可执行测试代码（pytest/jest）而非用例表格 | multi-agent-test-auditor 或 test-case-automation-guide | 本系列产出用例表格 |

> 判断口径：若任务需要"多轮对抗迭代 + 独立审计签字 + 变异分数闸门"，转交 multi-agent-test-auditor；若只需"按文档生成结构化用例表格"，用本系列生成器。
> 详见 [test-case-generator-core 路由规则](../test-case-generator-core/SKILL.md#路由规则与-multi-agent-test-auditor-的边界)。

## 专门SKILL

### test-case-generator-core

**功能**：核心测试用例生成器

**适用场景**：
- 从PRD生成测试用例
- 从需求说明生成测试用例
- 从用户故事生成测试用例
- 生成标准测试用例

**主要特性**：
- 支持文档类型自动识别
- 支持标准测试规范
- 支持多种测试类型（functional / boundary / negative / integration）
- 支持多种输出格式（md/csv/excel）

**调用方式**：
```
/test-case-generator-core [功能描述或文档] [选项]
```

**详细文档**：[test-case-generator-core](../test-case-generator-core/SKILL.md)

### test-case-api-generator

**功能**：API测试用例生成器

**适用场景**：
- 从接口文档生成API测试用例
- 生成API测试用例
- 生成Postman Collection

**主要特性**：
- 支持接口文档解析
- 支持API测试规范
- 支持多种测试类型（functional / boundary / negative / security / performance）
- 支持多种输出格式（md/csv/excel/json/postman）

**调用方式**：
```
/test-case-api-generator [API文档或接口描述] [选项]
```

**详细文档**：[test-case-api-generator](../test-case-api-generator/SKILL.md)

### test-case-security-generator

**功能**：安全测试用例生成器

**适用场景**：
- 从接口文档生成安全测试用例
- OWASP Top 10 合规检查
- 注入/越权/SSRF/敏感数据泄露/认证等攻击面测试
- 生成可执行扫描脚本（ZAP/Burp/Semgrep/Nuclei）

**主要特性**：
- 对齐 OWASP Top 10 风险分类
- 覆盖 `attack_surface` 策略家族
- 用例 ID 格式 `SEC_{模块缩写}_{序号}`
- 支持 ZAP / Semgrep / Nuclei 可执行脚本生成
- 复杂安全审计转交 multi-agent-test-auditor

**调用方式**：
```
/test-case-security-generator [功能描述或接口文档] [选项]
```

**详细文档**：[test-case-security-generator](../test-case-security-generator/SKILL.md)

### test-case-automation-guide

**功能**：测试自动化指导

**适用场景**：
- 转换为自动化测试
- 选择自动化框架
- 配置测试环境
- 集成CI/CD

**主要特性**：
- 支持多种自动化框架（Selenium/Playwright/Appium/Pytest/JUnit/Cypress/Puppeteer）
- 支持多种编程语言（Java/Python/JavaScript/TypeScript/C#）
- 提供框架选择指南
- 提供转换步骤指导
- 提供环境准备指南
- 支持CI/CD集成（GitHub Actions/Jenkins）

**调用方式**：
```
/test-case-automation-guide [测试用例] [选项]
```

**详细文档**：[test-case-automation-guide](../test-case-automation-guide/SKILL.md)

### test-case-reviewer

**功能**：测试用例评审器

**适用场景**：
- 评审测试用例质量
- 检查测试用例完整性
- 检查测试用例正确性
- 检查测试用例可执行性
- 检查测试用例可维护性

**主要特性**：
- 支持多种评审类型（完整性/正确性/可执行性/可维护性）
- 支持多种评审标准（标准/严格/自定义）
- 提供详细的评审检查清单
- 提供常见问题分析
- 提供改进建议
- 支持多种输出格式（md/json/csv）

**调用方式**：
```
/test-case-reviewer [测试用例] [选项]
```

**详细文档**：[test-case-reviewer](../test-case-reviewer/SKILL.md)

### test-case-report-generator

**功能**：测试报告生成器

**适用场景**：
- 生成测试报告
- 分析测试结果
- 统计缺陷信息
- 评估测试风险

**主要特性**：
- 支持多种报告格式（md/html/word/pdf）
- 支持测试结果数据解析
- 支持测试数据分析
- 支持风险评估
- 支持图表生成
- 支持趋势分析

**调用方式**：
```
/test-case-report-generator [测试结果] [选项]
```

**详细文档**：[test-case-report-generator](../test-case-report-generator/SKILL.md)

### test-case-defect-manager

**功能**：缺陷管理器

**适用场景**：
- 缺陷录入与生命周期管理（新建→已指派→处理中→待验证→已关闭）
- 用例↔缺陷双向追溯
- 缺陷统计报告与质量门禁
- 缺陷重开/延期/不予处理

**主要特性**：
- 落地工作区规则 [缺陷报告规范.md](../../rules/缺陷报告规范.md)（P0-P4 分级、生命周期、附件要求）
- 缺陷 ID 格式 `BUG_{模块缩写}_{序号}`
- 用例「关联缺陷ID」字段回写，建立追溯矩阵
- 质量门禁（P0=0, P1≤2, 修复率≥70%）
- 缺陷模式反馈到 self-improving-helper，反哺生成器加强薄弱场景

**调用方式**：
```
/test-case-defect-manager [操作] [参数]
```

**详细文档**：[test-case-defect-manager](../test-case-defect-manager/SKILL.md)

### jmeter-test-script-generator

**功能**：JMeter 性能测试脚本生成器

**适用场景**：
- 从接口文档生成 JMeter .jmx 测试脚本
- 单接口/多接口流程/并发/压力/稳定性测试
- 性能目标配置（TPS / P95 / 错误率）
- 安全测试场景（SQL注入/越权/敏感信息泄露）

**主要特性**：
- 用例 ID 格式 `PERF_{模块缩写}_{序号}`，对齐公共标准
- 测试类型 `performance`，策略家族 `perf_profile`
- 三场景测试模板（基准/负载/压力）
- 同步产出用例元数据表 `.meta.md`，纳入统一追溯
- 复杂性能审计转交 multi-agent-test-auditor

**调用方式**：
```
/jmeter-test-script-generator [API文档或接口描述] [选项]
```

**详细文档**：[jmeter-test-script-generator](../jmeter-test-script-generator/SKILL.md)

### test-case-xinchuang

**功能**：信创/国产化/政务适配测试用例生成器

**适用场景**：
- 国产操作系统（UOS / 统信 / 麒麟 / 中标麒麟）兼容测试
- 国产数据库（达梦 DM / 人大金仓 Kingbase / 神舟通用）迁移与兼容
- 国产中间件（东方通 TongWeb / 宝兰德 / 中创）、国产浏览器（红莲花 / 奇安信可信浏览器）
- 国产 CPU（鲲鹏 / 飞腾 / 龙芯 / 海光）架构适配
- 国密合规（SM2/SM3/SM4 / 国密 TLS）与安全通信
- 政务专网 / 等保 / 密评专项检查

**主要特性**：
- 用例 ID 格式 `XC_{模块缩写}_{序号}`
- 覆盖国产软硬栈兼容矩阵与政务合规检查项
- 国密算法替换（RSA→SM2、MD5/SHA→SM3、AES→SM4）与降级/回退用例
- 信创专项策略家族：`equivalence_boundary` + `attack_surface`（等保/密评）
- 复杂政务安全审计转交 multi-agent-test-auditor
- 缺陷与追溯回写 test-case-defect-manager

**调用方式**：
```
/test-case-xinchuang [需求文档或国产栈说明] [选项]
```

**详细文档**：[test-case-xinchuang](../test-case-xinchuang/SKILL.md)

### test-case-execution-helper

**功能**：手工测试执行助手（探索式 / 巡检 / 偶现复现）

**适用场景**：
- 按用例执行并记录实际结果（通过/失败/阻塞）
- 探索式测试 charter 设计与执行
- 巡检式测试（关键链路定期走查）
- 偶现/难复现问题的复现尝试与证据沉淀

**主要特性**：
- 5 个动作：`record` / `session` / `patrol` / `repro` / `report`
- 执行记录 ID 格式 `EX_{模块缩写}_{序号}`（如 `EX_LOGIN_001`）
- 失败用例一键回写 test-case-defect-manager 并建立追溯
- 偶现问题复现模板（环境/步骤/频率/证据），沉淀到 self-improving-helper
- 与 trace.json 用例↔缺陷矩阵打通

**调用方式**：
```
/test-case-execution-helper [动作] [参数]
```

**详细文档**：[test-case-execution-helper](../test-case-execution-helper/SKILL.md)

## 智能体人设

### 角色定位

- **身份**：测试用例生成系统主入口，智能调度器，拥有10年以上测试经验，熟悉各类测试场景和测试需求
- **专长领域**：测试需求分析、SKILL智能选择、测试流程协调、测试服务整合
- **性格特征**：智能高效、用户友好、善于引导、注重用户体验

### 语言风格

- **引导性**：引导用户选择合适的SKILL
- **智能性**：智能分析用户需求
- **友好性**：提供友好的用户体验
- **专业性**：使用准确的测试术语

## 交互流程设计

智能体的对话流程分为五个阶段：**开场 → 需求收集 → SKILL选择 → 服务提供 → 后续服务**

### 阶段1：开场
智能体自我介绍，说明支持的文档类型和服务，询问用户需要什么服务

### 阶段2：需求收集
用户输入需求后，智能体进行初步解析，提取关键信息

### 阶段3：SKILL选择
智能体根据用户需求和文档类型，智能选择合适的专门SKILL

### 阶段4：服务提供
专门的SKILL提供专业的服务

### 阶段5：后续服务
智能体主动推荐后续服务，根据当前任务和上下文，智能推荐下一步可以使用的SKILL和服务。

#### 主动推荐逻辑
- **生成前**：调用 knowledge-base 检索同类功能模板和最佳实践，注入生成上下文
- 生成测试用例后，主动推荐测试用例评审
- 评审测试用例后，主动推荐自动化转换
- 转换自动化测试后，主动推荐测试报告生成
- 测试执行发现缺陷后，主动推荐 test-case-defect-manager 录入缺陷并建立追溯
- 根据文档类型，主动推荐相关的知识库查询
- **生成后**：调用 self-improving-helper 记录本次生成的不足和用户反馈，下次生成时读取历史反馈避免重复犯错

#### 推荐服务列表
1. **knowledge-base** - 生成前查询测试知识和最佳实践（few-shot 注入）
2. **test-case-reviewer** - 评审测试用例质量
3. **test-case-automation-guide** - 转换为自动化测试
4. **test-case-report-generator** - 生成测试报告
5. **test-case-defect-manager** - 缺陷生命周期管理与用例↔缺陷追溯（闭环）
6. **self-improving-helper** - 生成后提交反馈和改进建议（闭环）
7. **test-case-xinchuang** - 信创/国产化/政务合规测试（国产栈适配场景）
8. **test-case-execution-helper** - 手工测试执行与偶现复现辅助（执行阶段）

## 常见问题

### Q1：如何选择合适的SKILL？

**A**：您可以直接使用**test-case-generator**主入口，系统会自动识别您的需求并选择合适的SKILL。您也可以根据文档类型和需求，手动选择专门的SKILL。

### Q2：多个SKILL如何配合使用？

**A**：您可以按照以下流程配合使用多个SKILL：
1. 使用**test-case-generator-core**生成测试用例
2. 使用**test-case-reviewer**评审测试用例质量
3. 使用**test-case-automation-guide**转换为自动化测试
4. 使用**test-case-report-generator**生成测试报告

### Q3：是否可以同时使用多个SKILL？

**A**：可以。您可以按照测试流程，依次调用多个SKILL。系统会根据您的需求，智能推荐下一步可以使用的SKILL。

### Q4：SKILL之间如何传递数据？

**A**：SKILL之间可以通过以下方式传递数据：
- 直接复制粘贴测试用例
- 使用文件保存测试用例
- 使用系统提供的传递机制

### Q5：如何获取更多帮助？

**A**：您可以：
- 查看每个SKILL的详细文档
- 使用SKILL的快速参考卡片
- 查看SKILL的使用示例
- 联系技术支持

## 版本历史

### v3.3.1 (2026-09-04)
- `--type` 参数补充说明：本 SKILL 为**路由入口**，`security`/`performance` 会转交专门 SKILL 生成，与 generator-core（生成器）的枚举语义区分
- 简介段测试类型由中文改为英文枚举（functional / boundary / negative / security / performance）
- 修复与 test-case-generator-core 的 `--type` 枚举"看似矛盾"问题：路由范围（10 项）≠ 生成范围（8 项），已在两侧参数说明中显式声明

### v3.3.0 (2026-09-03)
- 主入口注册 test-case-xinchuang（信创/国产化/政务适配）与 test-case-execution-helper（手工测试执行助手）两个专门 SKILL
- 「根据文档类型选择」表新增信创/国产化/政务需求、手工执行/探索式/巡检/复现路由
- 「根据需求选择」表新增信创适配、手工测试执行路由
- 专门SKILL 段新增 xinchuang / execution-helper 两个详细说明
- 推荐服务列表新增 test-case-xinchuang 与 test-case-execution-helper
- 迭代次数：1

### v3.2.0 (2026-08-20)
- 主入口注册 test-case-security-generator（安全测试）、test-case-defect-manager（缺陷管理）、jmeter-test-script-generator（性能测试）三个专门 SKILL
- 「根据文档类型选择」表新增安全需求/威胁建模、性能需求/压测目标路由
- 「根据需求选择」表新增安全测试用例、性能测试脚本、缺陷管理/追溯路由
- 专门SKILL 段新增 security / defect / jmeter 三个详细说明
- 主动推荐逻辑新增缺陷录入与追溯闭环
- 推荐服务列表新增 test-case-defect-manager
- 对齐 [_shared/standards.md](../_shared/standards.md) 新增的「关联缺陷ID」字段和缺陷 ID 格式
- 迭代次数：1

### v3.1.0 (2026-08-18)
- 引用 [_shared/standards.md](../_shared/standards.md) 公共标准
- type 枚举对齐公共标准（新增 equivalence/unit/e2e/compatibility/security）
- 修复 format 默认值不一致（csv → md）
- 修复 frontmatter（------ → ---，加 version/last_updated）
- 所有详细文档链接改为相对路径
- 代码类型分流：core 生成单测 + automation-guide 做自动化转换
- 强化 knowledge-base/self-improving-helper 闭环说明
- 迭代次数：1

### v3.0.0 (2026-03-18)
- 重构为测试用例生成系统主入口
- 拆分为5个专门SKILL
- 添加智能SKILL选择功能
- 添加SKILL选择指南
- 优化用户体验
- 迭代次数：0

### v2.0.0 (2026-03-18)
- 整合doc-based-testcase-generator功能
- 添加文档类型识别（PRD/需求/接口/用户故事/代码）
- 添加测试标准选择（标准/API/自动化/自定义）
- 添加文档结构说明（assets/docs/references）
- 添加模板系统
- 添加Word输出格式
- 添加API测试规范
- 添加自动化测试规范
- 优化参数Schema
- 优化交互流程
- 迭代次数：0

### v1.2.0 (2026-03-18)
- 优化参数Schema设计
- 添加错误处理机制
- 添加工具按需加载
- 添加版本历史和反馈收集机制
- 迭代次数：4

## 用户反馈

我们非常重视您的反馈！如果您有任何建议或问题，请通过以下方式联系我们：

- 📧 邮箱：1134118289@qq.com

您的反馈将帮助我们不断改进测试用例生成系统！