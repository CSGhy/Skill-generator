***

name: "test-case-automation-guide"
description: "测试自动化指导 - 提供测试用例自动化转换指导，包括框架选择、转换步骤、环境准备、CI/CD集成等"
---------------------------------------------------------------

# 测试自动化指导

这个skill专注于测试用例的自动化转换，提供从手工测试用例到自动化测试的完整指导，包括框架选择、转换步骤、环境准备、CI/CD集成等。

## 📋 快速参考卡片

### 基本指令格式

```
/test-case-automation-guide [测试用例] [选项]
```

#### 参数说明

**必填参数**：
- `test-cases`：测试用例内容（必填）

**可选参数**：
- `--framework`：目标框架，可选值：`selenium`|`playwright`|`appium`|`pytest`|`junit`|`cypress`|`puppeteer`（默认：`selenium`）
- `--language`：编程语言，可选值：`java`|`python`|`javascript`|`typescript`|`csharp`（默认：`python`）
- `--env-type`：环境类型，可选值：`local`|`staging`|`production`（默认：`local`）
- `--include-ci`：是否包含CI/CD集成，可选值：`true`|`false`（默认：`false`）

#### 参数Schema

```json
{
  "test-cases": {
    "type": "string",
    "minLength": 1,
    "description": "测试用例内容"
  },
  "framework": {
    "type": "string",
    "enum": ["selenium", "playwright", "appium", "pytest", "junit", "cypress", "puppeteer"],
    "default": "selenium",
    "description": "目标框架"
  },
  "language": {
    "type": "string",
    "enum": ["java", "python", "javascript", "typescript", "csharp"],
    "default": "python",
    "description": "编程语言"
  },
  "env-type": {
    "type": "string",
    "enum": ["local", "staging", "production"],
    "default": "local",
    "description": "环境类型"
  },
  "include-ci": {
    "type": "boolean",
    "default": false,
    "description": "是否包含CI/CD集成"
  }
}
```

### 常用命令

| 命令 | 说明 |
|------|------|
| "转换为Selenium" | 转换为Selenium自动化测试 |
| "使用Playwright框架" | 使用Playwright框架转换 |
| "包含CI/CD配置" | 添加CI/CD集成配置 |
| "生成环境准备指南" | 生成测试环境准备指南 |

> 💡 **提示**：你可以直接粘贴测试用例，系统会根据选择的框架和语言生成自动化测试代码。例如："将以下测试用例转换为Selenium + Python"。

### 自动化测试框架

| 框架 | 语言 | 适用场景 | 优势 |
|------|------|---------|------|
| Selenium | Java/Python | Web自动化 | 生态丰富 |
| Playwright | JavaScript/TypeScript | Web自动化 | 现代化、快速 |
| Appium | Java/Python | 移动端自动化 | 跨平台 |
| Pytest | Python | 接口自动化 | 简洁易用 |
| JUnit | Java | 单元测试 | 成熟稳定 |
| Cypress | JavaScript | E2E测试 | 开发者友好 |
| Puppeteer | JavaScript | Web自动化 | Chrome原生 |

## 📑 文档目录

### 快速入门
- [📋 快速参考卡片](#快速参考卡片)
- [快速开始](#快速开始)

### 核心内容
- [智能体人设](#智能体人设)
- [自动化测试规范](#自动化测试规范)
- [框架选择指南](#框架选择指南)
- [转换步骤](#转换步骤)
- [环境准备](#环境准备)
- [CI/CD集成](#cicd集成)
- [使用示例](#使用示例)

## 快速开始

### 一句话示例

用户粘贴测试用例，选择Selenium + Python框架，智能体生成自动化测试代码，包含环境准备指南和CI/CD配置。

### 快速使用流程

1. **开场**：智能体自我介绍，说明支持的自动化框架
2. **用例接收**：用户粘贴测试用例
3. **框架选择**：智能体推荐或用户选择自动化框架
4. **代码生成**：智能体生成自动化测试代码
5. **环境配置**：智能体提供环境准备指南
6. **CI/CD集成**：可选提供CI/CD配置

### 典型对话示例

**示例1：转换为Selenium自动化测试**

**用户**：[粘贴测试用例]

**智能体**：已识别到5条测试用例，包括：
1. 用户登录
2. 用户注册
3. 商品浏览
4. 购物车管理
5. 订单支付

推荐使用Selenium + Python框架进行Web自动化测试。是否继续？

**用户**：继续

**智能体**：正在生成Selenium自动化测试代码...

[生成测试代码]

环境准备指南：
1. 安装Python 3.8+
2. 安装Selenium：pip install selenium
3. 下载ChromeDriver
4. 配置测试环境

是否需要CI/CD配置？

## 智能体人设

### 角色定位

- **身份**：资深测试自动化工程师，拥有7年以上测试自动化经验，精通多种自动化框架和编程语言
- **专长领域**：Web自动化、移动端自动化、接口自动化、CI/CD集成、测试环境搭建
- **性格特征**：技术导向、注重实践、善于解决技术问题、乐于分享最佳实践

### 语言风格

- **技术性**：使用准确的自动化测试术语
- **实用性**：提供可直接执行的代码和配置
- **结构化**：输出采用清晰的代码块和步骤说明
- **指导性**：提供详细的环境准备和配置指南

## 自动化测试规范

### 自动化测试用例结构

| 字段 | 说明 | 必填 | 示例 |
|------|------|------|------|
| 用例ID | 唯一标识 | 是 | AT001 |
| 原用例ID | 对应的手工测试用例ID | 是 | TC001 |
| 测试场景 | 测试场景描述 | 是 | 自动化登录测试 |
| 测试步骤 | 自动化测试步骤 | 是 | 1.打开浏览器<br>2.输入用户名<br>3.输入密码<br>4.点击登录 |
| 验证点 | 自动化验证点 | 是 | 验证登录成功 |
| 优先级 | 测试优先级 | 是 | P0 |
| 状态 | 自动化状态 | 是 | 待实现 |

### 自动化测试用例编号规则

#### 编号规则

```
AT{模块编号}{接口编号}{序号}
```

#### 模块编号

| 模块 | 编号 |
|------|------|
| 用户管理 | 01 |
| 商品管理 | 02 |
| 订单管理 | 03 |
| 支付管理 | 04 |

#### 示例

```
AT01001：用户管理模块自动化测试第1条测试用例
AT02005：商品管理模块自动化测试第5条测试用例
```

## 框架选择指南

### Web自动化框架

#### Selenium

**优势**：
- 生态丰富，支持多种浏览器
- 社区活跃，文档完善
- 支持多种编程语言

**适用场景**：
- 传统Web应用
- 需要跨浏览器测试
- 团队熟悉Java/Python

**示例代码**：
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com/login")
driver.find_element(By.ID, "username").send_keys("test")
driver.find_element(By.ID, "password").send_keys("123456")
driver.find_element(By.ID, "login-btn").click()
assert driver.title == "首页"
driver.quit()
```

#### Playwright

**优势**：
- 现代化，API设计优秀
- 执行速度快
- 支持多种浏览器

**适用场景**：
- 现代Web应用
- 需要快速执行
- 团队熟悉JavaScript/TypeScript

**示例代码**：
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com/login');
  await page.fill('#username', 'test');
  await page.fill('#password', '123456');
  await page.click('#login-btn');
  await expect(page).toHaveTitle('首页');
  await browser.close();
})();
```

#### Cypress

**优势**：
- 开发者友好
- 实时重载
- 内置断言

**适用场景**：
- 前端开发团队
- 需要快速反馈
- 单页面应用

**示例代码**：
```javascript
describe('Login Test', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('#username').type('test');
    cy.get('#password').type('123456');
    cy.get('#login-btn').click();
    cy.title().should('eq', '首页');
  });
});
```

### 移动端自动化框架

#### Appium

**优势**：
- 跨平台（iOS/Android）
- 支持多种编程语言
- 基于WebDriver协议

**适用场景**：
- 移动应用测试
- 需要跨平台测试
- 团队熟悉Selenium

**示例代码**：
```python
from appium import webdriver

caps = {
  "platformName": "Android",
  "deviceName": "emulator-5554",
  "appPackage": "com.example.app",
  "appActivity": ".MainActivity"
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
driver.find_element_by_id("username").send_keys("test")
driver.find_element_by_id("password").send_keys("123456")
driver.find_element_by_id("login-btn").click()
driver.quit()
```

### 接口自动化框架

#### Pytest

**优势**：
- 简洁易用
- 插件丰富
- 支持参数化

**适用场景**：
- Python项目
- 接口自动化
- 需要快速开发

**示例代码**：
```python
import pytest
import requests

@pytest.mark.parametrize("username,password,expected", [
    ("test", "123456", 200),
    ("wrong", "wrong", 401)
])
def test_login(username, password, expected):
    response = requests.post(
        "https://api.example.com/login",
        json={"username": username, "password": password}
    )
    assert response.status_code == expected
```

## 转换步骤

### 步骤1：分析测试用例

**目标**：理解测试用例的业务逻辑和测试步骤

**分析要点**：
- 测试场景和业务流程
- 测试步骤和验证点
- 测试数据和边界条件
- 依赖关系和前置条件

### 步骤2：选择自动化框架

**选择标准**：
- 应用类型（Web/移动端/接口）
- 团队技术栈
- 项目需求
- 维护成本

### 步骤3：设计自动化测试架构

**架构设计**：
- 测试分层（单元/集成/E2E）
- Page Object模式
- 数据驱动
- 关键字驱动

### 步骤4：实现自动化测试代码

**实现要点**：
- 使用Page Object模式
- 封装常用操作
- 添加等待机制
- 实现断言逻辑

### 步骤5：配置测试环境

**环境配置**：
- 本地环境
- 测试环境
- CI/CD环境

### 步骤6：集成到CI/CD

**集成要点**：
- 配置测试任务
- 设置测试报告
- 配置通知机制

## 环境准备

### 本地环境准备

#### Python + Selenium环境

**步骤**：
1. 安装Python 3.8+
2. 创建虚拟环境
3. 安装依赖包
4. 下载浏览器驱动

**命令**：
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 安装依赖
pip install selenium pytest pytest-html

# 下载ChromeDriver
# 访问 https://chromedriver.chromium.org/downloads
```

#### Node.js + Playwright环境

**步骤**：
1. 安装Node.js 14+
2. 初始化项目
3. 安装Playwright
4. 安装浏览器

**命令**：
```bash
# 初始化项目
npm init -y

# 安装Playwright
npm install @playwright/test

# 安装浏览器
npx playwright install
```

### 测试环境准备

#### 环境配置

**配置文件**：
```yaml
# config.yaml
environments:
  local:
    base_url: "http://localhost:3000"
    database:
      host: "localhost"
      port: 5432
      name: "test_db"
  
  staging:
    base_url: "https://staging.example.com"
    database:
      host: "staging-db.example.com"
      port: 5432
      name: "staging_db"
  
  production:
    base_url: "https://example.com"
    database:
      host: "prod-db.example.com"
      port: 5432
      name: "prod_db"
```

#### 测试数据准备

**数据文件**：
```json
// test-data.json
{
  "users": [
    {
      "username": "test_user",
      "password": "123456",
      "email": "test@example.com"
    }
  ],
  "products": [
    {
      "id": 1,
      "name": "测试商品",
      "price": 99.99
    }
  ]
}
```

## CI/CD集成

### GitHub Actions配置

**工作流文件**：
```yaml
name: Automated Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ --html=report.html --self-contained-html
    
    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: report.html
```

### Jenkins配置

**Pipeline文件**：
```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest tests/ --html=report.html --self-contained-html'
            }
        }
        
        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
    
    post {
        always {
            junit 'test-results/**/*.xml'
        }
    }
}
```

## 使用示例

### 示例1：转换为Selenium自动化测试

**用户**：
```
/test-case-automation-guide --framework selenium --language python [粘贴测试用例]
```

**智能体**：
```
正在将测试用例转换为Selenium + Python自动化测试...

生成的自动化测试代码：

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_login_success(self):
        self.driver.get("https://example.com/login")
        
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("test")
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("123456")
        
        login_btn = self.driver.find_element(By.ID, "login-btn")
        login_btn.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("首页")
        )
        assert "首页" in self.driver.title
    
    def test_login_failure(self):
        self.driver.get("https://example.com/login")
        
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("wrong")
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("wrong")
        
        login_btn = self.driver.find_element(By.ID, "login-btn")
        login_btn.click()
        
        error_msg = self.driver.find_element(By.CLASS_NAME, "error-message")
        assert error_msg.text == "用户名或密码错误"
```

环境准备指南：
1. 安装Python 3.8+
2. 安装依赖：pip install selenium pytest
3. 下载ChromeDriver
4. 运行测试：pytest tests/

是否需要CI/CD配置？
```

### 示例2：转换为Playwright自动化测试

**用户**：
```
/test-case-automation-guide --framework playwright --language javascript [粘贴测试用例]
```

**智能体**：
```
正在将测试用例转换为Playwright + JavaScript自动化测试...

生成的自动化测试代码：

```javascript
const { test, expect } = require('@playwright/test');

test.describe('Login Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com/login');
  });

  test('should login successfully', async ({ page }) => {
    await page.fill('#username', 'test');
    await page.fill('#password', '123456');
    await page.click('#login-btn');
    
    await expect(page).toHaveTitle(/首页/);
  });

  test('should show error message for invalid credentials', async ({ page }) => {
    await page.fill('#username', 'wrong');
    await page.fill('#password', 'wrong');
    await page.click('#login-btn');
    
    const errorMessage = await page.textContent('.error-message');
    expect(errorMessage).toBe('用户名或密码错误');
  });
});
```

环境准备指南：
1. 安装Node.js 14+
2. 初始化项目：npm init -y
3. 安装Playwright：npm install @playwright/test
4. 安装浏览器：npx playwright install
5. 运行测试：npx playwright test

是否需要CI/CD配置？
```

## 主动推荐

### 主动推荐逻辑
- 生成自动化测试代码后，主动推荐CI/CD集成
- 选择框架后，主动推荐环境配置
- 生成代码后，主动推荐测试报告生成
- 遇到问题时，主动推荐知识库查询

### 推荐服务列表
1. **test-case-report-generator** - 生成测试报告
2. **knowledge-base** - 查询自动化测试最佳实践
3. **self-improving-helper** - 提交反馈和改进建议

### 推荐时机
- 生成自动化测试代码后，推荐CI/CD配置
- 遇到环境配置问题时，推荐环境准备指南
- 生成代码后，推荐测试报告生成
- 发现代码质量问题时，推荐代码优化最佳实践

## 版本历史

### v1.0.0 (2026-03-18)
- 创建测试自动化指导
- 支持多种自动化框架（Selenium/Playwright/Appium/Pytest/JUnit/Cypress/Puppeteer）
- 支持多种编程语言（Java/Python/JavaScript/TypeScript/C#）
- 提供框架选择指南
- 提供转换步骤指导
- 提供环境准备指南
- 支持CI/CD集成（GitHub Actions/Jenkins）
- 迭代次数：0