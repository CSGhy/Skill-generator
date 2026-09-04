# AI 测试技能套件 (Testing Skill Suite for Trae)

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/CSGhy/Skill-generator?style=social)
![GitHub forks](https://img.shields.io/github/forks/CSGhy/Skill-generator?style=social)
![GitHub issues](https://img.shields.io/github/issues/CSGhy/Skill-generator)
![GitHub license](https://img.shields.io/github/license/CSGhy/Skill-generator)

**一套面向 [Trae IDE](https://trae.cn) 的 AI 测试技能库：覆盖需求分析、用例生成、评审、执行、缺陷管理、报告、性能/安全/信创专项与自我进化的测试全生命周期**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 项目简介

本仓库是一组可直接在 **Trae IDE（及兼容 WorkBuddy 标准发现路径的 Agent）** 中加载的 AI 测试技能（SKILL）。它从最初的单个「测试用例生成器」演进为一个**完整的测试工程技能套件**：

- 🧩 **21 个技能** + 1 套公共标准（`_shared`），协同覆盖测试全流程
- 📐 **4 条工作区规则**（`rules/`），统一提交规范、用例质量、测试分层与缺陷报告
- 🧬 内置**自我进化**与**多代理对抗审计**能力，让技能从反馈中持续优化
- ✅ 所有用例产物可被 `_shared/validate_test_cases.py` 自动校验，标准可执行、可回归

### 核心特性

- 🎯 **全生命周期覆盖**：需求文档 → 用例生成 → 评审 → 手工/自动化执行 → 缺陷追溯 → 测试报告 → 经验沉淀
- 🧠 **智能主入口路由**：`test-case-generator` 按需求自动分发到 API、安全、性能、信创等专门技能
- 📊 **风险驱动 + 测试金字塔**：用例标注优先级（P0-P3）与测试层级（unit/integration/e2e），E2E 占比 ≤ 15%
- 🛡️ **专项测试**：OWASP Top 10 安全测试、JMeter/PTS/工具包性能压测、信创国产化适配
- 🔧 **多输入多输出**：支持需求文档、OpenAPI、SQL、代码、蓝湖原型；输出 Markdown / CSV / Excel / JSON / .jmx
- ♿ **数据与自动化**：中文区域测试数据生成、Playwright 浏览器自动化、微信小程序自动化
- 📏 **标准即代码**：`_shared/standards.md` 定义 ID/命名/结构/枚举/schema，配套校验器自动把关
- 🔄 **自我进化**：基于反馈自动决定 MERGE / ADD / DISCARD 进化策略，版本化管理

### 技能总览（21 个）

#### 一、测试用例生成与评审（核心链路）

| 技能目录 | 能力说明 |
|----------|----------|
| [`test-case-generator`](.trae/skills/test-case-generator/SKILL.md) | **主入口**。智能识别需求并路由到合适的专门技能，含核心生成器、API、自动化指导、评审、报告等子技能 |
| [`test-case-generator-core`](.trae/skills/test-case-generator-core/SKILL.md) | 核心生成模块，从已识别文档生成基础测试用例，遵循 `_shared/standards.md` 公共标准 |
| [`test-case-api-generator`](.trae/skills/test-case-api-generator/SKILL.md) | 从接口文档/OpenAPI 生成 API 测试用例：参数校验、边界值、错误码、契约测试 |
| [`test-case-security-generator`](.trae/skills/test-case-security-generator/SKILL.md) | 对齐 OWASP Top 10，覆盖注入/越权/SSRF/重放/供应链等攻击面，产出用例与可执行扫描脚本 |
| [`test-case-xinchuang`](.trae/skills/test-case-xinchuang/SKILL.md) | 信创/国产化/政务适配：国产 OS（UOS/麒麟）、数据库（达梦/金仓）、中间件、浏览器、国密算法（SM2/3/4） |
| [`test-case-automation-guide`](.trae/skills/test-case-automation-guide/SKILL.md) | 用例自动化转换指导：框架选型、转换步骤、环境准备、CI/CD 集成 |
| [`test-case-reviewer`](.trae/skills/test-case-reviewer/SKILL.md) | 用例评审：完整性、正确性、可执行性、可维护性检查 |
| [`test-case-report-generator`](.trae/skills/test-case-report-generator/SKILL.md) | 根据执行结果生成专业测试报告：概述、结果、缺陷统计、风险评估 |
| [`test-case-defect-manager`](.trae/skills/test-case-defect-manager/SKILL.md) | 缺陷全生命周期管理，落地缺陷报告规范，建立用例 ↔ 缺陷双向追溯 |
| [`test-case-execution-helper`](.trae/skills/test-case-execution-helper/SKILL.md) | 手工/功能测试执行助手：执行记录、探索式测试（charter）、巡检、偶现问题复现记录 |

#### 二、性能与压力测试

| 技能目录 | 能力说明 |
|----------|----------|
| [`jmeter-test-script-generator`](.trae/skills/jmeter-test-script-generator/SKILL.md) | 一键从接口文档/API 描述生成可运行的 JMeter `.jmx`：HTTP 请求、断言、变量提取、并发配置 |
| [`performance-testing-toolkit`](.trae/skills/performance-testing-toolkit/SKILL.md) | 企业级性能工具包：HTTP 压测、负载测试、基准测试与报告生成（Python 脚本） |
| [`alibabacloud-pts-ops`](.trae/skills/alibabacloud-pts-ops/SKILL.md) | 阿里云 PTS 场景化压测：原生 HTTP/HTTPS 与 JMeter 场景的创建、管理、监控与清理 |

#### 三、测试数据与自动化

| 技能目录 | 能力说明 |
|----------|----------|
| [`qa-test-data-gen`](.trae/skills/qa-test-data-gen/SKILL.md) | 中文区域测试数据生成：姓名/身份证/手机/地址/银行卡，支持 SQL、JSON、CSV 与数据脱敏 |
| [`playwright`](.trae/skills/playwright/SKILL.md) | Playwright 浏览器自动化 / MCP / 爬虫：导航、点击、填表、截图、数据提取、调试 |
| [`weapp-automated-testing`](.trae/skills/weapp-automated-testing/SKILL.md) | 微信小程序自动化：启动 DevTools、页面导航、元素交互、截图、控制台日志读取 |

#### 四、质量审计与持续进化

| 技能目录 | 能力说明 |
|----------|----------|
| [`multi-agent-test-auditor`](.trae/skills/multi-agent-test-auditor/SKILL.md) | 多代理对抗式软件测试：多样化策略家族、变异审计、覆盖率盲点扫描、独立审计闸门 |
| [`multi-agent-research-prover`](.trae/skills/multi-agent-research-prover/SKILL.md) | 多代理对抗式证明/问题求解：研究级数学证明、算法设计、架构论证、形式化验证 |
| [`knowledge-base`](.trae/skills/knowledge-base/SKILL.md) | 测试知识库管理：测试用例知识库与经验积累，提供结构化知识查询 |
| [`self-improving-helper`](.trae/skills/self-improving-helper/SKILL.md) | 自我改进助手：记录反馈、分析错误、提供改进建议，驱动技能系统持续优化 |

#### 五、需求工程

| 技能目录 | 能力说明 |
|----------|----------|
| [`lanhu-requirements-doc`](.trae/skills/lanhu-requirements-doc/SKILL.md) | 蓝湖需求文档生成器：从蓝湖平台拉取原型数据，自动生成标准化需求文档 |

### 公共标准 `_shared/`

所有技能共享同一套可执行标准，位于 [`.trae/skills/_shared/`](.trae/skills/_shared/)：

- **[`standards.md`](.trae/skills/_shared/standards.md)**：测试用例公共标准，共 13 章——用例/缺陷 ID 格式、命名规范、标准用例与 API 用例结构、测试类型英文枚举（`functional`/`boundary`/`negative`/…）、测试策略家族、测试层级与金字塔比例、优先级（P0-P3）、FIRST 原则、必覆盖场景、模块编号、输出 schema 校验、对抗审计契约、完成闸门、反模式清单。
- **[`validate_test_cases.py`](.trae/skills/_shared/validate_test_cases.py)**：用例校验器。逐条校验 ID、前置条件、测试层级、策略家族、测试场景、测试类型枚举、预期结果，并检查批量硬门槛（策略多样性 ≥4、E2E 占比 ≤15%、场景覆盖 ≥3 类）。支持中文值自动归一化兜底。
  ```bash
  python .trae/skills/_shared/validate_test_cases.py <用例文件.md>
  python .trae/skills/_shared/validate_test_cases.py --self-test   # 自测
  ```
- **`feedback/feedback.json`**：自我进化反馈数据存储。

### 工作区规则 `.trae/rules/`

| 规则文件 | 作用 |
|----------|------|
| [`git-commit-message.md`](.trae/rules/git-commit-message.md) | **Git 提交信息规范**：Conventional Commits 风格 `<type>(<scope>): <subject>`，type 用英文枚举（feat/fix/test/docs/refactor/perf/style/chore），subject 用中文；技能改动 scope 用技能目录名，规则改动用 `rules` |
| [`测试用例质量规范.md`](.trae/rules/测试用例质量规范.md) | 生成、编写、评审各类测试用例时自动生效的质量标准 |
| [`测试金字塔原则.md`](.trae/rules/测试金字塔原则.md) | 测试分层与占比（单元 70% / 集成 20% / E2E ≤15%），反模式识别，与技能体系映射 |
| [`缺陷报告规范.md`](.trae/rules/缺陷报告规范.md) | 缺陷标题格式、必含信息、严重程度 P0-P4、优先级、生命周期与附件规范（缺陷 ID：`BUG_{模块}_{序号}`） |

> 规则文件与 `_shared/standards.md` 相互对齐：金字塔原则的分层比例、缺陷规范的 ID 格式均在公共标准中有对应章节。

### 推荐工作流（技能协同）

```
蓝湖原型/需求文档
      │  lanhu-requirements-doc
      ▼
标准化需求 ──► knowledge-base（生成前查经验）
      │
      ▼
test-case-generator（主入口路由）
      ├─► test-case-generator-core   功能/边界/负向用例
      ├─► test-case-api-generator    API/契约用例
      ├─► test-case-security-generator  安全用例
      ├─► test-case-xinchuang        信创适配用例
      ├─► jmeter / performance-toolkit / pts  性能脚本与压测
      └─► qa-test-data-gen           造测试数据
      │
      ▼
test-case-reviewer（评审）──► validate_test_cases.py（自动校验）
      │
      ▼
执行：test-case-execution-helper（手工）/ playwright / weapp（自动化）
      │
      ▼
缺陷：test-case-defect-manager（用例↔缺陷双向追溯）
      │
      ▼
test-case-report-generator（测试报告）
      │
      ▼
self-improving-helper + knowledge-base（复盘沉淀，反哺下一轮）
```

复杂/高风险场景可由 `multi-agent-test-auditor` 编排多代理对抗测试并过独立审计闸门。

### 目录结构

```
AiSkill/
├── README.md
└── .trae/
    ├── rules/                          # 工作区规则（4 条）
    │   ├── git-commit-message.md
    │   ├── 测试用例质量规范.md
    │   ├── 测试金字塔原则.md
    │   └── 缺陷报告规范.md
    └── skills/
        ├── _shared/                    # 公共标准与校验器
        │   ├── standards.md
        │   ├── validate_test_cases.py
        │   └── feedback/feedback.json
        ├── test-case-generator/        # 用例生成主入口
        ├── test-case-generator-core/   # 核心生成模块
        ├── test-case-api-generator/    # API 用例
        ├── test-case-security-generator/  # 安全用例（OWASP Top 10）
        ├── test-case-xinchuang/        # 信创/国产化适配
        ├── test-case-automation-guide/ # 自动化转换指导
        ├── test-case-reviewer/         # 用例评审
        ├── test-case-report-generator/ # 测试报告
        ├── test-case-defect-manager/   # 缺陷管理
        ├── test-case-execution-helper/ # 手工执行助手
        ├── jmeter-test-script-generator/  # JMeter 脚本生成
        ├── performance-testing-toolkit/   # 性能压测工具包
        ├── alibabacloud-pts-ops/       # 阿里云 PTS 压测
        ├── qa-test-data-gen/           # 测试数据生成
        ├── playwright/                 # 浏览器自动化
        ├── weapp-automated-testing/    # 小程序自动化
        ├── multi-agent-test-auditor/   # 多代理对抗测试
        ├── multi-agent-research-prover/  # 多代理对抗证明
        ├── knowledge-base/             # 知识库管理
        ├── self-improving-helper/      # 自我改进
        ├── lanhu-requirements-doc/     # 蓝湖需求文档
        ├── skill_evolution.py          # 技能进化脚本
        ├── SKILL_EVOLUTION_GUIDE.md    # 进化系统指南
        ├── SKILLS_REGISTERED.md        # 技能注册报告
        ├── SKILLS_MIGRATION_GUIDE.md   # 迁移指南
        └── SKILL_REVIEW_2026-09-04.md  # 技能库审查报告
```

### 快速开始

#### 1. 克隆仓库

```bash
git clone https://github.com/CSGhy/Skill-generator.git
```

#### 2. 在 Trae IDE 中使用

将仓库作为项目文件夹打开，`.trae/skills/` 与 `.trae/rules/` 会被 Trae 自动识别为工作区技能与规则；重新加载窗口后即可在对话中调用。

#### 3.（可选）注册到 WorkBuddy 标准发现路径

技能间大量使用相对引用（`../_shared/standards.md`、`../../rules/...`），推荐用**目录 Junction** 把技能映射到标准发现路径，而非移动文件：

```powershell
# 为单个技能建立 junction（真实文件仍在 .trae/skills/）
New-Item -ItemType Junction `
  -Path "C:\Users\Administrator\.workbuddy\skills\<技能名>" `
  -Target "D:\Program Files\Code\AiSkill\.trae\skills\<技能名>" -Force
```

详见 [SKILLS_REGISTERED.md](.trae/skills/SKILLS_REGISTERED.md)。

### 使用示例

**生成功能测试用例**
```
帮我生成用户登录功能的测试用例
```

**API / 契约测试**
```
我有一个 OpenAPI 文档，帮我生成测试用例
```
（随后粘贴 Swagger 文档）

**安全测试**
```
帮我生成登录功能的安全测试用例（对齐 OWASP Top 10）
```

**信创适配测试**
```
这个政务系统要做信创验收，帮我生成国产化适配测试用例
```

**性能压测**
```
根据这个接口文档生成 JMeter 压测脚本 / 用阿里云 PTS 创建压测场景
```

**校验用例产物**
```bash
python .trae/skills/_shared/validate_test_cases.py 测试用例.md
```

### 支持的测试类型

枚举值统一使用英文（见 `_shared/standards.md` 第五章）：

| 类型 | 英文枚举 | 说明 |
|------|----------|------|
| 功能测试 | `functional` | 正常流程功能验证 |
| 边界值测试 | `boundary` | 输入边界值扫描 |
| 等价类测试 | `equivalence` | 等价类划分 |
| 负向/异常测试 | `negative` | 异常与错误处理 |
| 单元测试 | `unit` | 函数/组件级（金字塔底层） |
| 集成测试 | `integration` | 模块间交互与接口 |
| 端到端测试 | `e2e` | 完整业务流程（金字塔顶层，占比 ≤15%） |
| 兼容性测试 | `compatibility` | 浏览器/设备/环境兼容 |
| 安全测试 | `security` | OWASP Top 10（XSS/注入/越权等） |
| 性能测试 | `performance` | 响应时间、并发、吞吐 |

> 「测试类型」与「测试策略家族」（`equivalence_boundary`/`contract_test`/`mutation_test`/`attack_surface` 等）正交，每条用例须同时标注，详见 `_shared/standards.md` 第五章与第五-B 章。

### 自我进化系统

技能库具备基于反馈的自我进化能力（[SKILL_EVOLUTION_GUIDE.md](.trae/skills/SKILL_EVOLUTION_GUIDE.md)）：

- **版本控制**：自动管理 `major.minor.patch` 版本号
- **反馈收集**：收集用户满意度与质量评分，存入 `_shared/feedback/`
- **进化策略**：`MERGE`（满意度 >4.5，合并优化）/ `ADD`（3.0–4.5，新增能力）/ `DISCARD`（<3.0，标记重构）
- **数据驱动**：计算平均满意度、调整率，提取常见问题

```bash
# 添加反馈
python .trae/skills/skill_evolution.py --skill .trae/skills/test-case-generator/SKILL.md --add-feedback
# 执行进化
python .trae/skills/skill_evolution.py --skill .trae/skills/test-case-generator/SKILL.md --evolve
```

### 贡献

欢迎贡献！建议遵循仓库的 [Git 提交信息规范](.trae/rules/git-commit-message.md)：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feat/xxx`
3. 按规范提交：`git commit -m "feat(<scope>): 中文简述"`
4. 推送分支并开启 Pull Request

> 新增技能时，请放在 `.trae/skills/<name>/`，含 `SKILL.md`，并遵循 `_shared/standards.md`；规则文件放 `.trae/rules/`。

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

### 联系方式

- 作者：CSGhy
- GitHub：[CSGhy](https://github.com/CSGhy)
- 问题反馈：[Issues](https://github.com/CSGhy/Skill-generator/issues)

---

## English

### Introduction

A library of **AI testing skills for [Trae IDE](https://trae.cn)** (and agents compatible with the WorkBuddy discovery path). It grew from a single test-case generator into a **full testing-engineering suite**:

- 🧩 **21 skills** + one shared standard (`_shared/`) covering the whole testing lifecycle
- 📐 **4 workspace rules** (`rules/`) for commit messages, case quality, the test pyramid, and defect reporting
- 🧬 Built-in **self-evolution** and **multi-agent adversarial auditing**
- ✅ Artifacts are machine-checked by `_shared/validate_test_cases.py`

### Skill Categories

- **Case authoring & review**: `test-case-generator` (router entry), `test-case-generator-core`, `test-case-api-generator`, `test-case-security-generator` (OWASP Top 10), `test-case-xinchuang` (domestic/localization stack & Chinese cryptography), `test-case-automation-guide`, `test-case-reviewer`, `test-case-report-generator`, `test-case-defect-manager`, `test-case-execution-helper`
- **Performance & load**: `jmeter-test-script-generator`, `performance-testing-toolkit`, `alibabacloud-pts-ops`
- **Data & automation**: `qa-test-data-gen` (Chinese-locale data), `playwright` (browser automation/MCP/scraping), `weapp-automated-testing` (WeChat mini-program)
- **Audit & evolution**: `multi-agent-test-auditor`, `multi-agent-research-prover`, `knowledge-base`, `self-improving-helper`
- **Requirements**: `lanhu-requirements-doc` (Lanhu prototype → requirement doc)

### Shared Standard & Rules

- `_shared/standards.md` — common standard: ID/naming, case & API structures, English test-type enums, strategy families, pyramid ratios (unit 70% / integration 20% / e2e ≤15%), priorities (P0-P3), FIRST principles, output schema, anti-patterns.
- `_shared/validate_test_cases.py` — validates each case and batch-level gates; run `python .trae/skills/_shared/validate_test_cases.py <cases.md>`.
- `.trae/rules/` — Conventional Commits (`<type>(<scope>): <subject>`, English type + Chinese subject), test-case quality spec, test-pyramid principle, defect-reporting spec (`BUG_{MODULE}_{NNN}`).

### Quick Start

```bash
git clone https://github.com/CSGhy/Skill-generator.git
```

Open the folder in Trae IDE; `.trae/skills/` and `.trae/rules/` are auto-loaded. For the WorkBuddy discovery path, create directory junctions (do **not** move files, because skills rely on relative paths) — see [SKILLS_REGISTERED.md](.trae/skills/SKILLS_REGISTERED.md).

### Examples

```
Generate test cases for the user login feature
Generate API test cases from this OpenAPI doc
Generate OWASP Top 10 security cases for login
Generate a JMeter script / an Alibaba Cloud PTS scenario
```

### Contributing

Fork → branch (`feat/xxx`) → commit following the repo's Conventional Commits rule → PR. New skills go under `.trae/skills/<name>/` with a `SKILL.md` and must follow `_shared/standards.md`.

### License

MIT — see [LICENSE](LICENSE).

- Author: CSGhy · [GitHub](https://github.com/CSGhy) · [Issues](https://github.com/CSGhy/Skill-generator/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

**If this project helps you, please give it a ⭐️ Star!**

</div>
