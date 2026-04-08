# 自动化测试用例规范

## 测试用例结构

| 字段 | 说明 | 必填 | 示例 |
|------|------|------|------|
| 用例ID | 唯一标识 | 是 | AT001 |
| 模块 | 功能模块 | 是 | 用户注册 |
| 测试场景 | 测试场景描述 | 是 | 正常注册 |
| 测试步骤 | 详细测试步骤 | 是 | 1.打开注册页面<br>2.输入用户名<br>3.输入密码<br>4.点击注册 |
| 预期结果 | 预期测试结果 | 是 | 注册成功 |
| 自动化步骤 | 自动化测试步骤 | 是 | page.goto('/register')<br>page.fill('#username', 'test')<br>page.fill('#password', '123456')<br>page.click('#submit') |
| 元素定位 | 元素定位器 | 是 | #username, #password, #submit |
| 优先级 | 测试优先级 | 是 | P0 |
| 可执行性 | 是否可自动化 | 是 | 是 |

## 测试用例类型

### 1. UI自动化测试

#### 1.1 页面元素测试

**测试场景**：验证页面元素

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 元素定位 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|---------|--------|---------|
| AT001 | 用户注册 | 验证注册页面元素 | 1.打开注册页面<br>2.检查页面元素 | 显示所有必要元素 | page.goto('/register')<br>expect(page.locator('#username')).toBeVisible()<br>expect(page.locator('#password')).toBeVisible()<br>expect(page.locator('#submit')).toBeVisible() | #username, #password, #submit | P0 | 是 |
| AT002 | 用户注册 | 验证输入框提示 | 1.打开注册页面<br>2.检查输入框提示 | 显示正确的提示信息 | page.goto('/register')<br>expect(page.locator('#username')).toHaveAttribute('placeholder', '请输入用户名')<br>expect(page.locator('#password')).toHaveAttribute('placeholder', '请输入密码') | #username, #password | P1 | 是 |

#### 1.2 页面交互测试

**测试场景**：验证页面交互

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 元素定位 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|---------|--------|---------|
| AT003 | 用户注册 | 输入用户名 | 1.打开注册页面<br>2.输入用户名 | 用户名输入成功 | page.goto('/register')<br>page.fill('#username', 'testuser')<br>expect(page.locator('#username')).toHaveValue('testuser') | #username | P0 | 是 |
| AT004 | 用户注册 | 输入密码 | 1.打开注册页面<br>2.输入密码 | 密码输入成功 | page.goto('/register')<br>page.fill('#password', '123456')<br>expect(page.locator('#password')).toHaveValue('123456') | #password | P0 | 是 |
| AT005 | 用户注册 | 点击注册按钮 | 1.打开注册页面<br>2.点击注册按钮 | 注册按钮可点击 | page.goto('/register')<br>expect(page.locator('#submit')).toBeEnabled() | #submit | P0 | 是 |

#### 1.3 页面导航测试

**测试场景**：验证页面导航

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 元素定位 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|---------|--------|---------|
| AT006 | 用户注册 | 跳转到注册页面 | 1.打开首页<br>2.点击注册链接 | 跳转到注册页面 | page.goto('/')<br>page.click('#register-link')<br>expect(page).toHaveURL('/register') | #register-link | P0 | 是 |
| AT007 | 用户注册 | 注册成功后跳转 | 1.打开注册页面<br>2.输入用户名<br>3.输入密码<br>4.点击注册<br>5.检查跳转 | 跳转到登录页面 | page.goto('/register')<br>page.fill('#username', 'testuser')<br>page.fill('#password', '123456')<br>page.click('#submit')<br>expect(page).toHaveURL('/login') | #submit | P0 | 是 |

### 2. 接口自动化测试

#### 2.1 接口调用测试

**测试场景**：验证接口调用

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT008 | 用户注册 | 调用注册接口 | 1.发送注册请求<br>2.检查响应 | 返回成功响应 | response = requests.post('/api/user/register', json={'username': 'testuser', 'password': '123456'})<br>assert response.status_code == 200<br>assert response.json()['code'] == 0 | P0 | 是 |
| AT009 | 用户登录 | 调用登录接口 | 1.发送登录请求<br>2.检查响应 | 返回成功响应 | response = requests.post('/api/user/login', json={'username': 'testuser', 'password': '123456'})<br>assert response.status_code == 200<br>assert response.json()['code'] == 0 | P0 | 是 |

#### 2.2 参数验证测试

**测试场景**：验证参数验证

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT010 | 用户注册 | 缺少用户名 | 1.发送注册请求（缺少用户名）<br>2.检查响应 | 返回参数错误 | response = requests.post('/api/user/register', json={'password': '123456'})<br>assert response.status_code == 400<br>assert response.json()['code'] == 1001 | P0 | 是 |
| AT011 | 用户注册 | 缺少密码 | 1.发送注册请求（缺少密码）<br>2.检查响应 | 返回参数错误 | response = requests.post('/api/user/register', json={'username': 'testuser'})<br>assert response.status_code == 400<br>assert response.json()['code'] == 1001 | P0 | 是 |

#### 2.3 响应验证测试

**测试场景**：验证响应内容

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT012 | 用户注册 | 验证响应数据 | 1.发送注册请求<br>2.检查响应数据 | 返回正确的用户信息 | response = requests.post('/api/user/register', json={'username': 'testuser', 'password': '123456'})<br>assert response.status_code == 200<br>assert 'user_id' in response.json()['data']<br>assert 'username' in response.json()['data'] | P0 | 是 |
| AT013 | 用户登录 | 验证Token | 1.发送登录请求<br>2.检查Token | 返回有效的Token | response = requests.post('/api/user/login', json={'username': 'testuser', 'password': '123456'})<br>assert response.status_code == 200<br>assert 'token' in response.json()['data'] | P0 | 是 |

### 3. 数据驱动测试

#### 3.1 多组数据测试

**测试场景**：使用多组数据测试

**测试数据**：
```python
test_data = [
    {'username': 'testuser1', 'password': '123456', 'expected': True},
    {'username': 'testuser2', 'password': '123456', 'expected': True},
    {'username': 'testuser3', 'password': '123456', 'expected': True},
]
```

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT014 | 用户注册 | 多组数据测试 | 1.使用多组数据测试<br>2.检查每组的响应 | 所有数据都注册成功 | for data in test_data:<br>  response = requests.post('/api/user/register', json=data)<br>  assert response.status_code == 200<br>  assert response.json()['code'] == 0 | P0 | 是 |

#### 3.2 参数化测试

**测试场景**：使用参数化测试

**测试数据**：
```python
@pytest.mark.parametrize('username,password,expected', [
    ('testuser1', '123456', True),
    ('testuser2', '123456', True),
    ('testuser3', '123456', True),
])
def test_register(username, password, expected):
    response = requests.post('/api/user/register', json={'username': username, 'password': password})
    assert response.status_code == 200
    assert response.json()['code'] == 0
```

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT015 | 用户注册 | 参数化测试 | 1.使用参数化测试<br>2.检查每组的响应 | 所有参数都注册成功 | 使用pytest.mark.parametrize进行参数化测试 | P0 | 是 |

#### 3.3 数据组合测试

**测试场景**：使用数据组合测试

**测试数据**：
```python
test_data = [
    {'username': 'testuser1', 'password': '123456', 'email': 'test1@example.com'},
    {'username': 'testuser2', 'password': '123456', 'email': 'test2@example.com'},
    {'username': 'testuser3', 'password': '123456', 'email': 'test3@example.com'},
]
```

**测试用例**：
| 用例ID | 模块 | 测试场景 | 测试步骤 | 预期结果 | 自动化步骤 | 优先级 | 可执行性 |
|--------|------|---------|---------|---------|-----------|--------|---------|
| AT016 | 用户注册 | 数据组合测试 | 1.使用数据组合测试<br>2.检查每组的响应 | 所有组合都注册成功 | for data in test_data:<br>  response = requests.post('/api/user/register', json=data)<br>  assert response.status_code == 200<br>  assert response.json()['code'] == 0 | P0 | 是 |

## 自动化测试框架

### Playwright框架

#### 特点
- 现代化的Web自动化框架
- 支持多浏览器
- 支持多语言
- 支持并行执行

#### 示例代码

```python
from playwright.sync_api import Page, expect

def test_register(page: Page):
    page.goto('/register')
    page.fill('#username', 'testuser')
    page.fill('#password', '123456')
    page.click('#submit')
    expect(page).toHaveURL('/login')
```

### Pytest框架

#### 特点
- 简洁易用
- 支持参数化
- 支持fixture
- 丰富的插件

#### 示例代码

```python
import pytest
import requests

@pytest.mark.parametrize('username,password,expected', [
    ('testuser1', '123456', True),
    ('testuser2', '123456', True),
    ('testuser3', '123456', True),
])
def test_register(username, password, expected):
    response = requests.post('/api/user/register', json={'username': username, 'password': password})
    assert response.status_code == 200
    assert response.json()['code'] == 0
```

### Selenium框架

#### 特点
- 生态丰富
- 支持多语言
- 支持多浏览器
- 社区活跃

#### 示例代码

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_register():
    driver = webdriver.Chrome()
    driver.get('/register')
    driver.find_element(By.ID, 'username').send_keys('testuser')
    driver.find_element(By.ID, 'password').send_keys('123456')
    driver.find_element(By.ID, 'submit').click()
    assert '/login' in driver.current_url
    driver.quit()
```

## 元素定位策略

### ID定位

```python
page.locator('#username')
```

### Class定位

```python
page.locator('.username-input')
```

### Name定位

```python
page.locator('[name="username"]')
```

### XPath定位

```python
page.locator('//input[@id="username"]')
```

### CSS选择器定位

```python
page.locator('input#username')
```

### 文本定位

```python
page.locator('text=用户名')
```

## 测试数据管理

### 配置文件

```json
{
  "test_data": {
    "username": "testuser",
    "password": "123456",
    "email": "test@example.com"
  }
}
```

### 环境变量

```python
import os

username = os.getenv('TEST_USERNAME')
password = os.getenv('TEST_PASSWORD')
```

### 数据库

```python
import sqlite3

conn = sqlite3.connect('test_data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM test_users')
test_data = cursor.fetchall()
```

## 测试报告

### HTML报告

```bash
pytest --html=report.html
```

### JSON报告

```bash
pytest --json-report --json-report-file=report.json
```

### Allure报告

```bash
pytest --alluredir=allure-results
allure generate allure-results -o allure-report
```

## 测试覆盖率

### 代码覆盖率

```bash
pytest --cov=src --cov-report=html
```

### 接口覆盖率

```bash
pytest --cov=api --cov-report=html
```

### UI覆盖率

```bash
pytest --cov=ui --cov-report=html
```

## 测试优先级划分

| 优先级 | 说明 | 覆盖率 |
|--------|------|--------|
| P0 | 核心功能，必须自动化 | 100% |
| P1 | 重要功能，应该自动化 | 80% |
| P2 | 一般功能，可以自动化 | 60% |
| P3 | 边缘功能，可选自动化 | 40% |

## 测试可执行性评估

### 可执行性标准

| 评估维度 | 说明 | 评分 |
|---------|------|------|
| 元素可定位 | 元素能够准确定位 | 1-5分 |
| 步骤可执行 | 测试步骤能够执行 | 1-5分 |
| 结果可验证 | 测试结果能够验证 | 1-5分 |
| 数据可获得 | 测试数据能够获得 | 1-5分 |
| 环境可搭建 | 测试环境能够搭建 | 1-5分 |

### 可执行性判断

- 总分>=20分：可执行
- 总分15-19分：部分可执行
- 总分<15分：不可执行

## 最佳实践

### 1. 测试用例设计

- 保持测试用例独立性
- 使用有意义的测试用例名称
- 遵循AAA模式（Arrange-Act-Assert）
- 使用数据驱动测试

### 2. 测试代码编写

- 使用Page Object模式
- 使用Wait机制
- 使用Assert断言
- 使用日志记录

### 3. 测试数据管理

- 使用配置文件管理测试数据
- 使用环境变量管理敏感数据
- 使用数据库管理大量数据
- 使用参数化测试

### 4. 测试报告管理

- 生成详细的测试报告
- 保存测试截图
- 记录测试日志
- 分析测试结果

## 常见问题

### Q1：如何选择自动化测试框架？

**A**：根据项目需求选择：
- Web自动化：Playwright、Selenium
- 接口自动化：Pytest、Requests
- 移动端自动化：Appium

### Q2：如何提高测试用例的可执行性？

**A**：采用以下策略：
- 确保元素可定位
- 确保步骤可执行
- 确保结果可验证
- 确保数据可获得
- 确保环境可搭建

### Q3：如何管理测试数据？

**A**：采用以下方式：
- 使用配置文件
- 使用环境变量
- 使用数据库
- 使用参数化测试

### Q4：如何生成测试报告？

**A**：使用以下工具：
- HTML报告
- JSON报告
- Allure报告
- 自定义报告

### Q5：如何提高测试覆盖率？

**A**：采用以下策略：
- 增加测试用例数量
- 增加测试场景
- 增加测试数据
- 使用覆盖率工具
