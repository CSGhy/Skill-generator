# 测试用例生成器 (Test Case Generator)

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/CSGhy/Skill-generator?style=social)
![GitHub forks](https://img.shields.io/github/forks/CSGhy/Skill-generator?style=social)
![GitHub issues](https://img.shields.io/github/issues/CSGhy/Skill-generator)
![GitHub license](https://img.shields.io/github/license/CSGhy/Skill-generator)

**一个强大的AI驱动的测试用例生成工具，帮助开发者和测试工程师快速创建全面的测试用例**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 项目简介

测试用例生成器是一个专业的AI技能，能够从代码、需求或用户故事自动生成全面、专业的测试用例。它支持多种测试类型，包括功能测试、边界测试、负向测试、集成测试、性能测试和安全测试，并提供风险分析、测试报告和自动化转换指导。

### 核心特性

- 🎯 **全面的测试覆盖**：支持功能、边界、负向、集成、性能、安全等多种测试类型
- 🧠 **智能需求分析**：自动识别测试需求，智能提问澄清模糊点
- 📊 **基于风险的测试**：提供风险评估和优先级划分（P0-P3）
- 🔧 **多种输入格式**：支持代码、需求文档、OpenAPI、SQL脚本、配置文件等
- 📝 **多种输出格式**：支持Markdown、CSV、Excel、JSON等格式
- 🏭 **行业特定场景**：内置金融、电商、医疗、教育等行业测试场景
- 🛡️ **安全测试**：按OWASP Top 10标准提供安全测试用例
- ♿ **可访问性测试**：支持WCAG 2.1标准的可访问性测试
- 📈 **测试覆盖率分析**：提供代码覆盖率、需求覆盖率等指标
- 🔄 **自动化转换指导**：提供从测试用例到自动化脚本的转换指导

### 适用场景

- 软件测试工程师快速生成测试用例
- 开发者进行代码测试
- 产品经理验证需求完整性
- QA团队制定测试计划
- 教学和学习测试方法

### 快速开始

#### 安装

1. 克隆仓库：
```bash
git clone https://github.com/CSGhy/Skill-generator.git
```

2. 将skill文件复制到Trae IDE的skills目录：
```
.trae/skills/test-case-generator/
├── SKILL.md
└── (其他文件)
```

3. 在Trae IDE中重新加载技能

#### 使用示例

**简单功能测试**：
```
帮我生成用户登录功能的测试用例
```

**API测试**：
```
我有一个OpenAPI文档，帮我生成测试用例
```
（然后粘贴Swagger文档）

**性能测试**：
```
帮我生成购物车功能的性能测试用例
```

**安全测试**：
```
帮我生成登录功能的安全测试用例
```

### 项目结构

```
AiSkill/
├── .gitignore
├── README.md
└── .trae/
    └── skills/
        └── test-case-generator/
            └── SKILL.md
```

### 支持的测试类型

| 类型 | 说明 |
|------|------|
| 功能测试 | 验证功能正常工作 |
| 边界测试 | 测试输入边界值 |
| 负向测试 | 测试异常情况 |
| 集成测试 | 测试模块交互 |
| 性能测试 | 测试响应时间、并发 |
| 安全测试 | 测试安全漏洞 |
| 可访问性测试 | 测试无障碍访问 |

### 支持的输入格式

- 代码片段（函数、类、模块）
- 需求文档（用户故事、功能规格）
- OpenAPI/Swagger文档
- SQL脚本和表结构
- 配置文件（YAML、JSON、INI）
- UI组件代码（React、Vue、Angular）

### 输出格式

- **Markdown**：适合人类阅读和文档
- **CSV**：适合TestRail、Zephyr等工具导入
- **Excel**：适合Excel编辑和分享
- **JSON**：适合自动化框架集成

### 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 赞助

如果您觉得这个项目对您有帮助，欢迎赞助支持项目的持续开发！

#### 赞助方式

**GitHub Sponsors**：
[![Sponsor](https://img.shields.io/badge/-Sponsor-fafb7c?style=for-the-badge&logo=GitHub&logoColor=181717)](https://github.com/sponsors/CSGhy)

**微信支付**：
![微信支付](https://raw.githubusercontent.com/CSGhy/Skill-generator/main/.trae/images/wechat-qr.png)

**支付宝**：
```
[支付宝二维码]
```

**PayPal**：
```
[PayPal链接]
```

#### 赞助者感谢

感谢以下赞助者对本项目的支持！

<!-- 赞助者列表将在这里显示 -->

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 联系方式

- 作者：CSGhy
- GitHub：[CSGhy](https://github.com/CSGhy)
- 问题反馈：[Issues](https://github.com/CSGhy/Skill-generator/issues)

---

## English

### Project Introduction

Test Case Generator is a professional AI-powered skill that automatically generates comprehensive and professional test cases from code, requirements, or user stories. It supports multiple test types including functional, boundary, negative, integration, performance, and security testing, and provides risk analysis, test reports, and automation conversion guidance.

### Core Features

- 🎯 **Comprehensive Test Coverage**: Supports functional, boundary, negative, integration, performance, security, and more test types
- 🧠 **Intelligent Requirement Analysis**: Automatically identifies test requirements and intelligently clarifies ambiguities
- 📊 **Risk-Based Testing**: Provides risk assessment and priority classification (P0-P3)
- 🔧 **Multiple Input Formats**: Supports code, requirement documents, OpenAPI, SQL scripts, config files, etc.
- 📝 **Multiple Output Formats**: Supports Markdown, CSV, Excel, JSON, and more
- 🏭 **Industry-Specific Scenarios**: Built-in test scenarios for finance, e-commerce, healthcare, education, etc.
- 🛡️ **Security Testing**: Provides security test cases based on OWASP Top 10 standards
- ♿ **Accessibility Testing**: Supports WCAG 2.1 standard accessibility testing
- 📈 **Test Coverage Analysis**: Provides metrics like code coverage, requirement coverage, etc.
- 🔄 **Automation Conversion Guidance**: Provides guidance for converting test cases to automation scripts

### Use Cases

- Software test engineers quickly generating test cases
- Developers performing code testing
- Product managers verifying requirement completeness
- QA teams creating test plans
- Teaching and learning testing methodologies

### Quick Start

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/CSGhy/Skill-generator.git
```

2. Copy skill files to Trae IDE's skills directory:
```
.trae/skills/test-case-generator/
├── SKILL.md
└── (other files)
```

3. Reload skills in Trae IDE

#### Usage Examples

**Simple Functional Testing**:
```
Help me generate test cases for user login functionality
```

**API Testing**:
```
I have an OpenAPI document, help me generate test cases
```
(Paste Swagger document)

**Performance Testing**:
```
Help me generate performance test cases for shopping cart functionality
```

**Security Testing**:
```
Help me generate security test cases for login functionality
```

### Project Structure

```
AiSkill/
├── .gitignore
├── README.md
└── .trae/
    └── skills/
        └── test-case-generator/
            └── SKILL.md
```

### Supported Test Types

| Type | Description |
|------|-------------|
| Functional Testing | Verify features work correctly |
| Boundary Testing | Test input boundary values |
| Negative Testing | Test exceptional cases |
| Integration Testing | Test module interactions |
| Performance Testing | Test response time, concurrency |
| Security Testing | Test security vulnerabilities |
| Accessibility Testing | Test barrier-free access |

### Supported Input Formats

- Code snippets (functions, classes, modules)
- Requirement documents (user stories, functional specs)
- OpenAPI/Swagger documents
- SQL scripts and table structures
- Configuration files (YAML, JSON, INI)
- UI component code (React, Vue, Angular)

### Output Formats

- **Markdown**: Suitable for human reading and documentation
- **CSV**: Suitable for importing into TestRail, Zephyr, etc.
- **Excel**: Suitable for Excel editing and sharing
- **JSON**: Suitable for automation framework integration

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Sponsorship

If you find this project helpful, please consider sponsoring to support its continued development!

#### Sponsorship Options

**GitHub Sponsors**:
[![Sponsor](https://img.shields.io/badge/-Sponsor-fafb7c?style=for-the-badge&logo=GitHub&logoColor=181717)](https://github.com/sponsors/CSGhy)

**WeChat Pay**:
```
[WeChat QR Code]
```

**Alipay**:
```
[Alipay QR Code]
```

**PayPal**:
```
[PayPal Link]
```

#### Sponsors

Thank you to the following sponsors for supporting this project!

<!-- Sponsor list will appear here -->

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

### Contact

- Author: CSGhy
- GitHub: [CSGhy](https://github.com/CSGhy)
- Issue Tracker: [Issues](https://github.com/CSGhy/Skill-generator/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

**If this project helps you, please give it a ⭐️ Star!**

</div>
