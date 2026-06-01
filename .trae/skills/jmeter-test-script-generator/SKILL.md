---
name: "jmeter-test-script-generator"
description: "一键生成JMeter测试脚本 - 从接口文档或API描述快速生成可直接运行的JMeter .jmx测试计划，支持HTTP请求、断言、变量提取、并发配置等。Invoke when user asks to create JMeter scripts, performance test plans, or .jmx files."
---

# JMeter测试脚本生成器

这个Skill专门用于从接口文档或API描述快速生成可直接运行的JMeter测试脚本（.jmx格式）。它支持各种常见的性能测试场景，包括单接口测试、多接口流程测试、并发测试、压力测试等。

## 📋 快速参考卡片

### 基本指令格式

```
/jmeter-test-script-generator [API文档或接口描述] [选项]
```

#### 参数说明

**必填参数**：
- `api-doc`：API文档内容或接口描述（必填）

**可选参数**：
- `--test-type`：测试类型，可选值：`single`|`flow`|`baseline`|`load`|`stress`|`soak`（默认：`single`）
- `--threads`：线程数（并发用户数），默认：10
- `--ramp-up`：Ramp-Up时间（秒），默认：1
- `--loops`：循环次数，默认：1
- `--duration`：持续时间（秒），默认：60
- `--assertions`：是否添加断言，可选值：`true`|`false`（默认：`true`）
- `--extractors`：是否添加变量提取器，可选值：`true`|`false`（默认：`true`）
- `--listeners`：监听器类型，可选值：`all`|`minimal`|`performance`（默认：`all`）
- `--base-url`：基础URL，支持环境变量

**性能目标参数**（用于生成带目标验证的脚本）：
- `--target-tps`：目标TPS（每秒事务数），如：`1000`
- `--target-response-time`：目标响应时间P95（毫秒），如：`500`
- `--target-error-rate`：目标错误率阈值（百分比），如：`0.5`
- `--include-security`：是否包含安全测试场景，可选值：`true`|`false`（默认：`false`）

#### 参数Schema

```json
{
  "api-doc": {
    "type": "string",
    "minLength": 1,
    "description": "API文档内容或接口描述"
  },
  "test-type": {
    "type": "string",
    "enum": ["single", "flow", "load", "stress", "soak"],
    "default": "single",
    "description": "测试类型"
  },
  "threads": {
    "type": "integer",
    "minimum": 1,
    "default": 10,
    "description": "线程数（并发用户数）"
  },
  "ramp-up": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Ramp-Up时间（秒）"
  },
  "loops": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "循环次数"
  },
  "duration": {
    "type": "integer",
    "minimum": 1,
    "default": 60,
    "description": "持续时间（秒）"
  },
  "assertions": {
    "type": "boolean",
    "default": true,
    "description": "是否添加响应断言"
  },
  "extractors": {
    "type": "boolean",
    "default": true,
    "description": "是否添加变量提取器"
  },
  "listeners": {
    "type": "string",
    "enum": ["all", "minimal", "performance"],
    "default": "all",
    "description": "监听器类型"
  },
  "base-url": {
    "type": "string",
    "description": "基础URL，如 http://localhost:8080"
  },
  "target-tps": {
    "type": "integer",
    "minimum": 1,
    "description": "目标TPS（每秒事务数）"
  },
  "target-response-time": {
    "type": "integer",
    "minimum": 1,
    "description": "目标响应时间P95（毫秒）"
  },
  "target-error-rate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "description": "目标错误率阈值（百分比）"
  },
  "include-security": {
    "type": "boolean",
    "default": false,
    "description": "是否包含安全测试场景"
  }
}
```

### 常用命令

| 命令 | 说明 |
|------|------|
| "生成JMeter脚本" | 从接口描述生成基础JMeter脚本 |
| "创建性能测试计划" | 创建完整的性能测试计划 |
| "并发测试脚本" | 生成并发测试脚本 |
| "压力测试脚本" | 生成压力测试脚本 |
| "流程测试脚本" | 生成多接口流程测试脚本 |

> 💡 **提示**：你可以直接粘贴接口文档内容，系统会自动识别接口信息并生成相应的JMeter测试脚本。例如："生成用户登录接口JMeter脚本"或"创建购物车流程性能测试计划"。

### 测试类型说明

| 测试类型 | 说明 | 典型场景 | 推荐配置 |
|---------|------|---------|---------|
| single | 单接口测试 | 单个API功能验证 | 1-10线程，1-5次循环 |
| flow | 流程测试 | 多接口业务流程 | 10-50线程，按流程复杂度 |
| baseline | 基准测试 | 建立性能基线 | 1-5线程，多次循环 |
| load | 负载测试 | 预期负载下的性能 | 目标并发数，持续运行 |
| stress | 压力测试 | 系统极限压力 | 阶梯式增加并发 |
| soak | 稳定性测试 | 长时间运行稳定性 | 中等并发，长时间运行 |

### 三维思维模式

生成脚本时，同时从三个维度考虑：

| 维度 | 思考问题 | 验证方式 |
|------|---------|---------|
| **[Test] 功能** | 这个特性是否按预期工作？ | 响应断言、业务逻辑验证 |
| **[Perf] 性能** | 高并发下会不会崩？响应时间是否可接受？ | 响应时间断言、TPS监控 |
| **[Security] 安全** | 有没有注入风险？鉴权是否完善？ | SQL注入测试、越权访问测试 |

## 📑 文档目录

### 快速入门
- [📋 快速参考卡片](#快速参考卡片)
- [快速开始](#快速开始)

### 核心内容
- [智能体人设](#智能体人设)
- [五阶段工作流](#五阶段工作流)
- [JMeter脚本结构](#jmeter脚本结构)
- [测试计划元素](#测试计划元素)
- [断言配置](#断言配置)
- [变量提取](#变量提取)
- [监听器配置](#监听器配置)

### 进阶指南
- [三场景测试模板](#三场景测试模板)
- [性能目标配置](#性能目标配置)
- [安全测试场景](#安全测试场景)
- [脚本评审检查清单](#脚本评审检查清单)
- [运行和分析指导](#运行和分析指导)

### 实战案例
- [使用示例](#使用示例)

### 参考文档
- [JMeter最佳实践指南](./references/jmeter-best-practices.md)
- [性能指标详解](./references/performance-metrics.md)
- [常见陷阱和避坑指南](./references/common-pitfalls.md)

## 快速开始

### 一句话示例

用户上传接口文档或描述接口信息，智能体自动解析接口信息，按照性能测试规范生成完整的JMeter测试脚本（.jmx格式），包含线程组、HTTP请求、断言、变量提取器、监听器等元素。

### 五阶段工作流

1. **Define scope（需求分析）**：理解业务场景、接口信息、性能目标
2. **Create strategy（方案设计）**：确定测试类型、并发模型、监控方案
3. **Write tests（脚本开发）**：生成.jmx脚本、参数化、断言配置
4. **Review checklist（脚本评审）**：检查线程组、参数化、断言、指标采集
5. **Execute & report（执行报告）**：提供运行说明、指标分析、问题排查

### 典型对话示例

**示例1：从接口描述生成单接口测试脚本**

**用户**：
```
生成用户登录接口的JMeter脚本
接口信息：
- 接口名称：用户登录
- 请求方法：POST
- 请求URL：/api/v1/login
- 请求参数：username（必填，字符串），password（必填，字符串）
- 响应：{"code":0,"msg":"success","data":{"token":"xxx"}}
```

**智能体**：
```
正在为"用户登录接口"生成JMeter测试脚本...

生成的测试计划包含：
- 线程组（10线程，1秒Ramp-Up，1次循环）
- HTTP请求（POST /api/v1/login）
- 响应断言（验证code=0）
- JSON提取器（提取token）
- 常用监听器

脚本已生成，请保存为 login.jmx 后在JMeter中打开运行。
```

## 智能体人设

### 角色定位

- **身份**：资深性能测试工程师，拥有8年以上JMeter使用和性能测试经验
- **专长领域**：JMeter脚本开发、性能测试、压力测试、稳定性测试、接口自动化
- **性格特征**：严谨细致、性能导向、注重细节、善于发现性能瓶颈
- **技术栈**：JMeter、Gatling、Locust、New Relic、Grafana、InfluxDB

### 语言风格

- **技术性**：使用准确的JMeter和性能测试术语
- **结构化**：输出清晰的XML格式.jmx脚本
- **专业性**：关注性能指标和脚本优化
- **实用性**：提供可直接运行的测试脚本

## JMeter脚本结构

### 基本结构

一个标准的JMeter测试脚本（.jmx）包含以下结构：

```
Test Plan
├── User Defined Variables（可选）
├── Thread Group
│   ├── HTTP Request Defaults（可选）
│   ├── HTTP Cookie Manager（可选）
│   ├── HTTP Header Manager（可选）
│   ├── Sampler（HTTP Request等）
│   │   ├── Assertions（响应断言等）
│   │   ├── Post Processors（提取器等）
│   │   └── Pre Processors（可选）
│   └── Logic Controllers（可选）
└── Listeners
```

### XML格式说明

JMeter脚本是XML格式，基本结构如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <!-- Thread Group 和其他元素 -->
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

## 测试计划元素

### 1. 线程组（Thread Group）

线程组是测试计划的核心，用于配置并发用户数、Ramp-Up时间、循环次数等。

**配置参数**：
- 线程数（Number of Threads）：并发用户数
- Ramp-Up时间（Ramp-Up Period）：启动所有线程所需时间
- 循环次数（Loop Count）：每个线程执行的次数
- 调度器（Scheduler）：可选，用于设置持续时间

**XML示例**：
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <stringProp name="LoopController.loops">1</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">10</stringProp>
  <stringProp name="ThreadGroup.ramp_time">1</stringProp>
  <boolProp name="ThreadGroup.scheduler">false</boolProp>
  <stringProp name="ThreadGroup.duration">60</stringProp>
  <stringProp name="ThreadGroup.delay">0</stringProp>
  <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
</ThreadGroup>
```

### 2. HTTP请求默认值（HTTP Request Defaults）

用于设置所有HTTP请求的默认值，如服务器名称、端口号、协议等。

**XML示例**：
```xml
<ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP请求默认值" enabled="true">
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <stringProp name="HTTPSampler.port">8080</stringProp>
  <stringProp name="HTTPSampler.protocol">http</stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path"></stringProp>
  <stringProp name="HTTPSampler.concurrentPool">6</stringProp>
  <boolProp name="HTTPSampler.implement">true</boolProp>
</ConfigTestElement>
```

### 3. HTTP请求（HTTP Request）

核心的采样器，用于发送HTTP请求。

**配置参数**：
- 协议（Protocol）：http或https
- 服务器名称或IP（Server Name or IP）
- 端口号（Port Number）
- 请求方法（Method）：GET、POST、PUT、DELETE等
- 路径（Path）
- 请求参数（Parameters）
- 请求体（Body Data）

**XML示例 - GET请求**：
```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="获取用户信息" enabled="true">
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
    <collectionProp name="Arguments.arguments">
      <elementProp name="userId" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">123</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <stringProp name="HTTPSampler.port">8080</stringProp>
  <stringProp name="HTTPSampler.protocol">http</stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path">/api/v1/user/info</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
</HTTPSamplerProxy>
```

**XML示例 - POST请求（JSON Body）**：
```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="用户登录" enabled="true">
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{&quot;username&quot;:&quot;test&quot;,&quot;password&quot;:&quot;123456&quot;}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <stringProp name="HTTPSampler.port">8080</stringProp>
  <stringProp name="HTTPSampler.protocol">http</stringProp>
  <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
  <stringProp name="HTTPSampler.path">/api/v1/login</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
</HTTPSamplerProxy>
```

### 4. HTTP信息头管理器（HTTP Header Manager）

用于设置HTTP请求头，如Content-Type、Authorization等。

**XML示例**：
```xml
<HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
  <collectionProp name="HeaderManager.headers">
    <elementProp name="Content-Type" elementType="Header">
      <stringProp name="Header.name">Content-Type</stringProp>
      <stringProp name="Header.value">application/json</stringProp>
    </elementProp>
    <elementProp name="Authorization" elementType="Header">
      <stringProp name="Header.name">Authorization</stringProp>
      <stringProp name="Header.value">Bearer ${token}</stringProp>
    </elementProp>
  </collectionProp>
</HeaderManager>
```

## 断言配置

断言用于验证响应是否符合预期。

### 1. 响应断言（Response Assertion）

用于验证响应内容、响应代码等。

**XML示例**：
```xml
<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言" enabled="true">
  <collectionProp name="Asserter.test_strings">
    <stringProp name="503201545">&quot;code&quot;:0</stringProp>
  </collectionProp>
  <stringProp name="Assertion.custom_message"></stringProp>
  <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
  <boolProp name="Assertion.assume_success">false</boolProp>
  <intProp name="Assertion.test_type">16</intProp>
</ResponseAssertion>
```

### 2. JSON断言（JSON Assertion）

专门用于验证JSON响应。

**XML示例**：
```xml
<JSONPathAssertion guiclass="JSONPathAssertionGui" testclass="JSONPathAssertion" testname="JSON断言" enabled="true">
  <stringProp name="JSON_PATH">$.code</stringProp>
  <stringProp name="EXPECTED_VALUE">0</stringProp>
  <boolProp name="JSONVALIDATION">true</boolProp>
  <boolProp name="EXPECT_NULL">false</boolProp>
  <boolProp name="ISREGEX">false</boolProp>
  <boolProp name="CONCAT">false</boolProp>
</JSONPathAssertion>
```

### 3. 响应时间断言（Duration Assertion）

用于验证响应时间是否在预期范围内。

**XML示例**：
```xml
<DurationAssertion guiclass="DurationAssertionGui" testclass="DurationAssertion" testname="响应时间断言" enabled="true">
  <stringProp name="DurationAssertion.duration">1000</stringProp>
</DurationAssertion>
```

## 变量提取

变量提取器用于从响应中提取数据，供后续请求使用。

### 1. JSON提取器（JSON Extractor）

从JSON响应中提取数据。

**XML示例**：
```xml
<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="JSON提取器" enabled="true">
  <stringProp name="JSONPostProcessor.referenceNames">token</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.data.token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">NOT_FOUND</stringProp>
</JSONPostProcessor>
```

### 2. 正则表达式提取器（Regular Expression Extractor）

使用正则表达式提取数据。

**XML示例**：
```xml
<RegexExtractor guiclass="RegexExtractorGui" testclass="RegexExtractor" testname="正则表达式提取器" enabled="true">
  <stringProp name="RegexExtractor.useHeaders">false</stringProp>
  <stringProp name="RegexExtractor.refname">userId</stringProp>
  <stringProp name="RegexExtractor.regex">&quot;userId&quot;:&quot;(\d+)&quot;</stringProp>
  <stringProp name="RegexExtractor.template">$1$</stringProp>
  <stringProp name="RegexExtractor.default">NOT_FOUND</stringProp>
  <stringProp name="RegexExtractor.match_number">1</stringProp>
</RegexExtractor>
```

## 监听器配置

监听器用于查看和分析测试结果。

### 常用监听器

| 监听器 | 用途 | 性能影响 |
|--------|------|---------|
| 查看结果树 | 查看详细请求响应 | 高（建议调试时使用） |
| 聚合报告 | 汇总统计信息 | 低 |
| 图形结果 | 响应时间图形 | 中 |
| 用表格察看结果 | 表格形式显示结果 | 中 |
| 后端监听器 | 发送数据到外部系统 | 低 |

**聚合报告XML示例**：
```xml
<ResultCollector guiclass="StatVisualizer" testclass="ResultCollector" testname="聚合报告" enabled="true">
  <boolProp name="ResultCollector.error_logging">false</boolProp>
  <objProp>
    <name>saveConfig</name>
    <value class="SampleSaveConfiguration">
      <time>true</time>
      <latency>true</latency>
      <timestamp>true</timestamp>
      <success>true</success>
      <label>true</label>
      <code>true</code>
      <message>true</message>
      <threadName>true</threadName>
      <dataType>true</dataType>
      <encoding>false</encoding>
      <assertions>true</assertions>
      <subresults>true</subresults>
      <responseData>false</responseData>
      <samplerData>false</samplerData>
      <xml>false</xml>
      <fieldNames>true</fieldNames>
      <responseHeaders>false</responseHeaders>
      <requestHeaders>false</requestHeaders>
      <responseDataOnError>false</responseDataOnError>
      <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
      <assertionsResultsToSave>0</assertionsResultsToSave>
      <bytes>true</bytes>
      <sentBytes>true</sentBytes>
      <url>true</url>
      <threadCounts>true</threadCounts>
      <idleTime>true</idleTime>
      <connectTime>true</connectTime>
    </value>
  </objProp>
  <stringProp name="filename"></stringProp>
</ResultCollector>
```

## 三场景测试模板

完整的性能测试应该包含三个场景：基准测试、负载测试、压力测试。

### 1. 基准测试（Baseline Test）

**目的**：建立系统在低负载下的性能基准，作为后续测试的参考基线。

**配置特点**：
- 线程数：1-5个
- 循环次数：多次（10-50次）
- 持续时间：不使用调度器，完成指定循环
- 断言：完整的功能断言

**使用场景**：
- 新功能上线前的基线建立
- 版本迭代后的性能对比
- 功能正确性验证

**XML模板 - 基准测试线程组**：
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="基准测试" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <stringProp name="LoopController.loops">20</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">3</stringProp>
  <stringProp name="ThreadGroup.ramp_time">1</stringProp>
  <boolProp name="ThreadGroup.scheduler">false</boolProp>
  <stringProp name="ThreadGroup.duration"></stringProp>
  <stringProp name="ThreadGroup.delay"></stringProp>
  <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
</ThreadGroup>
```

### 2. 负载测试（Load Test）

**目的**：验证系统在预期负载下是否满足性能目标。

**配置特点**：
- 线程数：目标并发数（根据TPS目标计算）
- Ramp-Up时间：等于线程数（每秒启动1个线程）或更短
- 持续时间：足够长以达到稳态（10-30分钟）
- 断言：必要的业务断言，避免过多影响性能

**TPS与线程数换算公式**：
```
线程数 ≈ (目标TPS × 平均响应时间秒) / (1 - 目标CPU利用率)

示例：
目标TPS = 800
平均响应时间 = 0.5秒
目标CPU利用率 = 70%
线程数 ≈ (800 × 0.5) / 0.3 ≈ 1333
```

**XML模板 - 负载测试线程组**：
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="负载测试" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
    <boolProp name="LoopController.continue_forever">true</boolProp>
    <stringProp name="LoopController.loops">-1</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">100</stringProp>
  <stringProp name="ThreadGroup.ramp_time">30</stringProp>
  <boolProp name="ThreadGroup.scheduler">true</boolProp>
  <stringProp name="ThreadGroup.duration">600</stringProp>
  <stringProp name="ThreadGroup.delay">0</stringProp>
  <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
</ThreadGroup>
```

### 3. 压力测试（Stress Test）

**目的**：找到系统的极限承载能力，验证系统在高压下的稳定性。

**配置特点**：
- 使用阶梯式线程组（Ultimate Thread Group）或多个普通线程组
- 逐步增加并发，观察系统响应
- 持续时间：每个阶梯5-10分钟
- 关注：错误率、响应时间变化、资源利用率

**阶梯式压力测试配置方案**：

| 阶梯 | 线程数 | 持续时间 | 说明 |
|------|--------|---------|------|
| 1 | 50 | 5分钟 | 预热 |
| 2 | 100 | 5分钟 | 低负载 |
| 3 | 200 | 5分钟 | 中负载 |
| 4 | 400 | 5分钟 | 高负载 |
| 5 | 600 | 5分钟 | 极限负载 |
| 6 | 0 | 5分钟 | 恢复期 |

**XML模板 - 压力测试（单阶梯）**：
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="压力测试 - 阶梯1" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
    <boolProp name="LoopController.continue_forever">true</boolProp>
    <stringProp name="LoopController.loops">-1</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">50</stringProp>
  <stringProp name="ThreadGroup.ramp_time">30</stringProp>
  <boolProp name="ThreadGroup.scheduler">true</boolProp>
  <stringProp name="ThreadGroup.duration">300</stringProp>
  <stringProp name="ThreadGroup.delay">0</stringProp>
  <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
</ThreadGroup>
```

## 性能目标配置

生成脚本时，询问用户的性能目标，并根据目标配置脚本。

### 性能目标参数

| 参数 | 说明 | 常见目标值 |
|------|------|-----------|
| TPS | 每秒事务数 | 100、500、1000、5000 |
| 响应时间P95 | 95%请求的响应时间 | 200ms、500ms、1000ms |
| 错误率 | 失败请求占比 | 0.1%、0.5%、1% |
| 并发用户数 | 同时在线用户数 | 50、100、500、1000 |

### 智能引导问题

如果用户没有明确说明性能目标，应该主动询问：

```
请问您的性能目标是什么？

1. 目标TPS（每秒事务数）：
   - 低：< 100 TPS
   - 中：100-500 TPS
   - 高：500-2000 TPS
   - 超高：> 2000 TPS

2. 目标响应时间（P95）：
   - 极速：< 100ms
   - 快速：100-300ms
   - 正常：300-800ms
   - 可接受：800-2000ms

3. 目标错误率：
   - 严格：< 0.1%
   - 标准：< 0.5%
   - 宽松：< 1%
```

### 根据目标推荐配置

| 目标TPS | 推荐线程数 | 推荐Ramp-Up | 推荐持续时间 |
|---------|-----------|-------------|-------------|
| < 100 | 10-50 | 5-10秒 | 5-10分钟 |
| 100-500 | 50-200 | 10-30秒 | 10-15分钟 |
| 500-2000 | 200-800 | 30-60秒 | 15-30分钟 |
| > 2000 | 800+ | 60-120秒 | 30-60分钟 |

## 安全测试场景

如果用户启用了安全测试（`--include-security true`），应该添加以下测试场景。

### 1. SQL注入测试

**测试目的**：验证接口是否存在SQL注入漏洞。

**测试用例**：
- 在参数中注入SQL语句
- 观察响应是否返回异常信息
- 验证是否能绕过认证

**XML示例 - SQL注入测试请求**：
```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="SQL注入测试" enabled="true">
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{&quot;username&quot;:&quot;admin' OR '1'='1&quot;,&quot;password&quot;:&quot;anything&quot;}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <stringProp name="HTTPSampler.port">8080</stringProp>
  <stringProp name="HTTPSampler.protocol">http</stringProp>
  <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
  <stringProp name="HTTPSampler.path">/api/v1/login</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
</HTTPSamplerProxy>
```

### 2. 越权访问测试

**测试目的**：验证用户是否能访问其权限范围外的资源。

**测试用例**：
- 使用用户A的token访问用户B的资源
- 验证是否返回403或404
- 不应该返回敏感数据

### 3. 敏感信息泄露测试

**测试目的**：验证错误响应中是否泄露敏感信息。

**检查项**：
- 错误信息中是否包含堆栈跟踪
- 是否暴露数据库信息
- 是否暴露内部IP和路径

## 脚本评审检查清单

生成脚本后，提醒用户检查以下项目：

### ✅ 线程组配置检查

- [ ] 线程数是否与目标场景匹配（基准/负载/压力）
- [ ] Ramp-Up时间是否合理（通常等于线程数或更短）
- [ ] 持续时间是否足够（负载测试建议10分钟以上）
- [ ] 循环次数设置正确（持续运行使用-1）
- [ ] 错误处理策略设置正确（continue/stop/start next loop）

### ✅ 参数化检查

- [ ] 用户名/密码是否参数化
- [ ] 动态参数（如商品ID、订单号）是否处理
- [ ] 环境变量（baseUrl、端口）是否可配置
- [ ] CSV数据文件配置是否正确

### ✅ 断言检查

- [ ] 业务成功标识断言（如code=0或success=true）
- [ ] HTTP状态码断言（200/201）
- [ ] 响应时间断言（如P95 < 500ms）
- [ ] 断言是否可量化，不依赖主观判断

### ✅ 指标采集检查

- [ ] 聚合报告是否配置
- [ ] 是否需要查看结果树（调试时开启，性能测试时关闭）
- [ ] 后端监听器是否需要（对接Grafana/InfluxDB）
- [ ] 结果保存配置是否合理（不保存响应数据以节省资源）

### ✅ 优化建议

- [ ] 是否移除了不必要的监听器
- [ ] HTTP请求默认值是否合理配置
- [ ] Cookie管理器是否需要
- [ ] 是否使用了Keep-Alive

## 运行和分析指导

### 一、如何打开和运行脚本

**方法1：通过JMeter GUI**

```
1. 打开JMeter
2. 点击 File -> Open
3. 选择生成的 .jmx 文件
4. 点击绿色三角形按钮运行
5. 查看"聚合报告"监听器
```

**方法2：通过命令行（推荐用于性能测试）**

```bash
# 基本命令
jmeter -n -t test.jmx -l results.jtl

# 生成HTML报告
jmeter -n -t test.jmx -l results.jtl -e -o report/

# 指定JMeter属性
jmeter -n -t test.jmx -l results.jtl -Jthreads=100 -Jduration=600
```

### 二、核心指标解读

运行测试后，重点关注以下指标：

| 指标 | 说明 | 目标 | 警告阈值 |
|------|------|------|---------|
| **样本数** | 总请求数 | 越多越好（统计更准确） | - |
| **平均值** | 平均响应时间（ms） | < 目标值 | > 目标值×1.5 |
| **中位数** | 50%请求响应时间（ms） | < 目标值 | > 目标值×1.2 |
| **90% Line** | 90%请求响应时间（ms） | < 目标值 | > 目标值 |
| **95% Line** | 95%请求响应时间（ms） | < 目标值 | > 目标值 |
| **99% Line** | 99%请求响应时间（ms） | < 目标值×2 | > 目标值×3 |
| **Min** | 最小响应时间（ms） | 低 | - |
| **Max** | 最大响应时间（ms） | < 目标值×5 | > 目标值×10 |
| **异常%** | 错误率 | < 0.5% | > 1% |
| **吞吐量** | 每秒请求数（TPS） | > 目标值 | < 目标值 |
| **接收KB/sec** | 接收数据速率 | 稳定 | 波动大 |
| **发送KB/sec** | 发送数据速率 | 稳定 | 波动大 |

### 三、常见问题排查

#### 问题1：响应时间过高

**可能原因**：
- 服务器CPU/内存已满
- 数据库连接池耗尽
- 网络带宽不足
- 线程数设置过高

**排查步骤**：
```
1. 检查服务器资源利用率（top、nmon、Grafana）
2. 查看数据库慢查询日志
3. 减少线程数重新测试
4. 检查是否有网络瓶颈
```

#### 问题2：错误率过高

**可能原因**：
- 服务器过载（500错误）
- 参数化数据问题
- 接口限流
- 线程数超过系统承载

**排查步骤**：
```
1. 查看"查看结果树"中的失败请求
2. 检查服务器错误日志
3. 验证参数化数据是否正确
4. 检查接口是否有频率限制
```

#### 问题3：TPS达不到目标

**可能原因**：
- 响应时间过长
- 线程数不足
- 服务器性能瓶颈
- 网络瓶颈

**排查步骤**：
```
1. 检查响应时间是否在预期范围内
2. 尝试增加线程数（注意观察响应时间变化）
3. 检查服务器资源是否还有余量
4. 考虑分布式压测
```

### 四、测试报告模板

测试完成后，建议生成以下报告：

```
性能测试报告
============

一、测试概述
- 测试日期：2026-05-29
- 测试环境：测试环境
- 测试目标：TPS >= 800，P95响应时间 <= 500ms

二、测试结果
| 指标 | 实际值 | 目标值 | 是否达标 |
|------|--------|--------|---------|
| TPS | 950 | 800 | ✅ 达标 |
| P95响应时间 | 420ms | 500ms | ✅ 达标 |
| 错误率 | 0.12% | 0.5% | ✅ 达标 |

三、问题发现
- 问题1：XXX（优先级：高/中/低）
- 问题2：XXX（优先级：高/中/低）

四、优化建议
- 建议1：XXX
- 建议2：XXX

五、结论
- 本次测试是否通过：是/否
- 建议：上线/继续优化
```

## 使用示例

### 示例1：单接口性能测试

**用户**：
```
生成用户登录接口的JMeter性能测试脚本
接口信息：
- 接口名称：用户登录
- 请求方法：POST
- 请求URL：http://localhost:8080/api/v1/login
- 请求头：Content-Type: application/json
- 请求体：{"username":"${username}","password":"${password}"}
- 响应：{"code":0,"msg":"success","data":{"token":"xxx","userId":123}}
- 测试要求：100并发，Ramp-Up 10秒，持续60秒
```

**智能体**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="用户登录性能测试" enabled="true">
      <stringProp name="TestPlan.comments">用户登录接口性能测试</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments">
          <elementProp name="baseUrl" elementType="Argument">
            <stringProp name="Argument.name">baseUrl</stringProp>
            <stringProp name="Argument.value">http://localhost:8080</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="username" elementType="Argument">
            <stringProp name="Argument.name">username</stringProp>
            <stringProp name="Argument.value">testuser</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="password" elementType="Argument">
            <stringProp name="Argument.name">password</stringProp>
            <stringProp name="Argument.value">123456</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="登录性能测试线程组" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">true</boolProp>
          <stringProp name="LoopController.loops">-1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">60</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
      <hashTree>
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
          <collectionProp name="HeaderManager.headers">
            <elementProp name="Content-Type" elementType="Header">
              <stringProp name="Header.name">Content-Type</stringProp>
              <stringProp name="Header.value">application/json</stringProp>
            </elementProp>
          </collectionProp>
        </HeaderManager>
        <hashTree/>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="用户登录" enabled="true">
          <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{&quot;username&quot;:&quot;${username}&quot;,&quot;password&quot;:&quot;${password}&quot;}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8080</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
          <stringProp name="HTTPSampler.path">/api/v1/login</stringProp>
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言 - 验证成功" enabled="true">
            <collectionProp name="Asserter.test_strings">
              <stringProp name="503201545">&quot;code&quot;:0</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
          <hashTree/>
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="提取token" enabled="true">
            <stringProp name="JSONPostProcessor.referenceNames">token</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">$.data.token</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
            <stringProp name="JSONPostProcessor.default_values">NOT_FOUND</stringProp>
          </JSONPostProcessor>
          <hashTree/>
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="提取userId" enabled="true">
            <stringProp name="JSONPostProcessor.referenceNames">userId</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">$.data.userId</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
            <stringProp name="JSONPostProcessor.default_values">NOT_FOUND</stringProp>
          </JSONPostProcessor>
          <hashTree/>
        </hashTree>
        <ResultCollector guiclass="StatVisualizer" testclass="ResultCollector" testname="聚合报告" enabled="true">
          <boolProp name="ResultCollector.error_logging">false</boolProp>
          <objProp>
            <name>saveConfig</name>
            <value class="SampleSaveConfiguration">
              <time>true</time>
              <latency>true</latency>
              <timestamp>true</timestamp>
              <success>true</success>
              <label>true</label>
              <code>true</code>
              <message>true</message>
              <threadName>true</threadName>
              <dataType>true</dataType>
              <encoding>false</encoding>
              <assertions>true</assertions>
              <subresults>true</subresults>
              <responseData>false</responseData>
              <samplerData>false</samplerData>
              <xml>false</xml>
              <fieldNames>true</fieldNames>
              <responseHeaders>false</responseHeaders>
              <requestHeaders>false</requestHeaders>
              <responseDataOnError>false</responseDataOnError>
              <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
              <assertionsResultsToSave>0</assertionsResultsToSave>
              <bytes>true</bytes>
              <sentBytes>true</sentBytes>
              <url>true</url>
              <threadCounts>true</threadCounts>
              <idleTime>true</idleTime>
              <connectTime>true</connectTime>
            </value>
          </objProp>
          <stringProp name="filename"></stringProp>
        </ResultCollector>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### 示例2：多接口流程测试

**用户**：
```
生成购物车流程测试脚本，包含以下接口：
1. 用户登录（POST /api/v1/login）
2. 获取商品列表（GET /api/v1/products）
3. 添加商品到购物车（POST /api/v1/cart/add）
4. 查看购物车（GET /api/v1/cart）

要求：
- 登录后提取token供后续接口使用
- 提取商品ID用于添加购物车
- 50并发，持续30秒
```

**智能体**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="购物车流程性能测试" enabled="true">
      <stringProp name="TestPlan.comments">购物车完整流程性能测试</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments">
          <elementProp name="baseUrl" elementType="Argument">
            <stringProp name="Argument.name">baseUrl</stringProp>
            <stringProp name="Argument.value">http://localhost:8080</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="username" elementType="Argument">
            <stringProp name="Argument.name">username</stringProp>
            <stringProp name="Argument.value">testuser</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="password" elementType="Argument">
            <stringProp name="Argument.name">password</stringProp>
            <stringProp name="Argument.value">123456</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="购物车流程测试" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">true</boolProp>
          <stringProp name="LoopController.loops">-1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">50</stringProp>
        <stringProp name="ThreadGroup.ramp_time">5</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">30</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="1. 用户登录" enabled="true">
          <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{&quot;username&quot;:&quot;${username}&quot;,&quot;password&quot;:&quot;${password}&quot;}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8080</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
          <stringProp name="HTTPSampler.path">/api/v1/login</stringProp>
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="请求头 - JSON" enabled="true">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="Content-Type" elementType="Header">
                <stringProp name="Header.name">Content-Type</stringProp>
                <stringProp name="Header.value">application/json</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
          <hashTree/>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言登录成功" enabled="true">
            <collectionProp name="Asserter.test_strings">
              <stringProp name="503201545">&quot;code&quot;:0</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
          <hashTree/>
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="提取token" enabled="true">
            <stringProp name="JSONPostProcessor.referenceNames">token</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">$.data.token</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
            <stringProp name="JSONPostProcessor.default_values">NOT_FOUND</stringProp>
          </JSONPostProcessor>
          <hashTree/>
        </hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="2. 获取商品列表" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8080</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/api/v1/products</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="请求头 - 带Token" enabled="true">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="Authorization" elementType="Header">
                <stringProp name="Header.name">Authorization</stringProp>
                <stringProp name="Header.value">Bearer ${token}</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
          <hashTree/>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言获取商品成功" enabled="true">
            <collectionProp name="Asserter.test_strings">
              <stringProp name="503201545">&quot;code&quot;:0</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
          <hashTree/>
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="提取第一个商品ID" enabled="true">
            <stringProp name="JSONPostProcessor.referenceNames">productId</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">$.data[0].id</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
            <stringProp name="JSONPostProcessor.default_values">1</stringProp>
          </JSONPostProcessor>
          <hashTree/>
        </hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="3. 添加商品到购物车" enabled="true">
          <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{&quot;productId&quot;:${productId},&quot;quantity&quot;:1}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8080</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
          <stringProp name="HTTPSampler.path">/api/v1/cart/add</stringProp>
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="请求头 - JSON+Token" enabled="true">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="Content-Type" elementType="Header">
                <stringProp name="Header.name">Content-Type</stringProp>
                <stringProp name="Header.value">application/json</stringProp>
              </elementProp>
              <elementProp name="Authorization" elementType="Header">
                <stringProp name="Header.name">Authorization</stringProp>
                <stringProp name="Header.value">Bearer ${token}</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
          <hashTree/>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言添加购物车成功" enabled="true">
            <collectionProp name="Asserter.test_strings">
              <stringProp name="503201545">&quot;code&quot;:0</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="4. 查看购物车" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8080</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/api/v1/cart</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="请求头 - Token" enabled="true">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="Authorization" elementType="Header">
                <stringProp name="Header.name">Authorization</stringProp>
                <stringProp name="Header.value">Bearer ${token}</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
          <hashTree/>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言查看购物车成功" enabled="true">
            <collectionProp name="Asserter.test_strings">
              <stringProp name="503201545">&quot;code&quot;:0</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
        <ResultCollector guiclass="StatVisualizer" testclass="ResultCollector" testname="聚合报告" enabled="true">
          <boolProp name="ResultCollector.error_logging">false</boolProp>
          <objProp>
            <name>saveConfig</name>
            <value class="SampleSaveConfiguration">
              <time>true</time>
              <latency>true</latency>
              <timestamp>true</timestamp>
              <success>true</success>
              <label>true</label>
              <code>true</code>
              <message>true</message>
              <threadName>true</threadName>
              <dataType>true</dataType>
              <encoding>false</encoding>
              <assertions>true</assertions>
              <subresults>true</subresults>
              <responseData>false</responseData>
              <samplerData>false</samplerData>
              <xml>false</xml>
              <fieldNames>true</fieldNames>
              <responseHeaders>false</responseHeaders>
              <requestHeaders>false</requestHeaders>
              <responseDataOnError>false</responseDataOnError>
              <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
              <assertionsResultsToSave>0</assertionsResultsToSave>
              <bytes>true</bytes>
              <sentBytes>true</sentBytes>
              <url>true</url>
              <threadCounts>true</threadCounts>
              <idleTime>true</idleTime>
              <connectTime>true</connectTime>
            </value>
          </objProp>
          <stringProp name="filename"></stringProp>
        </ResultCollector>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

## 版本历史

### v1.1.1 (2026-05-29)
- 新增references/参考文档目录
- 新增jmeter-best-practices.md（JMeter最佳实践指南）
  - 脚本设计原则
  - 性能优化技巧
  - 三阶段测试策略
  - 分布式压测指南
  - 监控与分析指南
  - 常见场景模板
- 新增performance-metrics.md（性能指标详解）
  - 核心指标详解（TPS、响应时间、错误率、吞吐量）
  - 指标关系分析
  - 聚合报告解读
  - HTML报告解读
  - 性能瓶颈定位指南
  - 性能目标设定指南
- 新增common-pitfalls.md（常见陷阱和避坑指南）
  - 脚本设计陷阱
  - 性能测试陷阱
  - 结果分析陷阱
  - 环境配置陷阱
  - 避坑检查清单
  - 快速排查表
- 在SKILL.md中添加参考文档引用

### v1.1.0 (2026-05-29)
- 新增三维思维模式（功能/性能/安全）
- 新增性能目标参数配置（TPS、响应时间、错误率）
- 新增三场景测试模板（基准测试、负载测试、压力测试）
- 新增TPS与线程数换算公式
- 新增智能引导问题模板
- 新增安全测试场景（SQL注入、越权访问、敏感信息泄露）
- 新增脚本评审检查清单
- 新增运行和分析指导（小白友好）
- 新增五阶段工作流
- 新增命令行运行方式和HTML报告生成
- 新增核心指标解读表
- 新增常见问题排查指南
- 新增测试报告模板
- 迭代次数：1

### v1.0.0 (2026-05-29)
- 创建JMeter测试脚本生成器
- 支持单接口测试脚本生成
- 支持多接口流程测试脚本生成
- 支持负载测试、压力测试、稳定性测试
- 支持HTTP请求配置（GET/POST/PUT/DELETE）
- 支持响应断言配置
- 支持JSON提取器和正则表达式提取器
- 支持常用监听器配置
- 支持用户定义变量
- 迭代次数：0
