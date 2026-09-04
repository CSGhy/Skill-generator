---
name: "test-case-xinchuang"
description: "信创/国产化/政务适配测试用例生成器 - 面向国产操作系统(UOS/麒麟/统信)、国产数据库(达梦/金仓)、国产中间件、国产浏览器(红莲花/奇安信)、国密算法(SM2/SM3/SM4)、政务专网环境的兼容性、功能与合规测试。Invoke when user mentions 信创、国产化适配、政务系统、国产OS/数据库/浏览器、国密、信创验收。"
version: "1.0.2"
last_updated: "2026-09-04"
---

# 信创 / 国产化 / 政务适配测试用例生成器

本 SKILL 遵循 [_shared/standards.md](../_shared/standards.md) 的公共标准（ID 格式、用例结构、测试类型、层级、金字塔比例、FIRST 原则、必覆盖场景、schema 校验、错误处理）。

本 SKILL 专注于**信创（信息技术应用创新）与政务场景下的适配测试**：在国产软硬件栈上验证系统功能正确、兼容、合规、安全。典型场景：政务 OA/审批、国产化办公、信创验收测试、党政专网系统。

## 📋 快速参考卡片

### 基本指令格式

```
/test-case-xinchuang [功能描述或环境清单] [选项]
```

#### 参数说明

**必填参数**：
- `target`：待测功能描述，或「国产环境清单 + 待测系统」（必填）

**可选参数**：
- `--stack`：国产技术栈筛选，可选值：`os`|`db`|`mw`|`browser`|`crypto`|`all`（默认：`all`）
- `--env`：目标环境，可选值：`信创云`|`政务专网`|`党政内网`|`混合`|`all`（默认：`all`）
- `--check-type`：检查类型，可选值：`compat`|`function`|`compliance`|`security`|`all`（默认：`all`）
- `--format`：输出格式，可选值：`md`|`csv`|`json`（默认：`md`）

#### 参数 Schema

```json
{
  "target": {
    "type": "string",
    "minLength": 1,
    "description": "待测功能描述或国产环境清单+系统"
  },
  "stack": {
    "type": "string",
    "enum": ["os", "db", "mw", "browser", "crypto", "all"],
    "default": "all",
    "description": "国产技术栈维度"
  },
  "env": {
    "type": "string",
    "enum": ["信创云", "政务专网", "党政内网", "混合", "all"],
    "default": "all",
    "description": "目标部署环境"
  },
  "check-type": {
    "type": "string",
    "enum": ["compat", "function", "compliance", "security", "all"],
    "default": "all",
    "description": "检查类型"
  },
  "format": {
    "type": "string",
    "enum": ["md", "csv", "json"],
    "default": "md",
    "description": "输出格式"
  }
}
```

### 常用命令

| 命令 | 说明 |
|------|------|
| "信创适配测试[功能名]" | 生成国产化适配用例 |
| "政务系统兼容测试" | 生成政务专网兼容用例 |
| "国密算法测试" | 生成 SM2/SM3/SM4 合规用例 |
| "国产数据库迁移测试" | 生成达梦/金仓迁移校验用例 |

## 📑 文档目录

### 核心内容
- [与公共标准的对齐](#与公共标准的对齐)
- [国产技术栈覆盖矩阵](#国产技术栈覆盖矩阵)
- [信创测试检查项](#信创测试检查项)
- [政务专网专项](#政务专网专项)
- [国密算法测试](#国密算法测试)
- [输出 Schema 校验](#输出-schema-校验)
- [使用示例](#使用示例)

## 快速开始

### 一句话示例

用户提供「国产环境清单 + 待测功能」，智能体按信创适配清单生成兼容性 + 功能 + 合规用例，每条标注 `XC_{模块缩写}_{序号}` ID、测试类型 `compatibility`/`functional`/`security`、策略家族 `equivalence_boundary`/`manual_heuristic`。

### 生成流程

1. **开场**：说明覆盖国产 OS/数据库/中间件/浏览器/国密/政务专网
2. **环境接收**：解析国产技术栈清单与待测功能
3. **知识库查询（生成前闭环）**：调用 [knowledge-base](../knowledge-base/SKILL.md) 检索同类信创适配模板、历史缺陷、兼容性基线
4. **生成**：按 [信创测试检查项](#信创测试检查项) 生成结构化用例
5. **Schema 校验**：调用 [_shared/validate_test_cases.py](../_shared/validate_test_cases.py) 校验
6. **优化导出**：用户可要求补充某栈或导出
7. **反馈记录（生成后闭环）**：调用 [self-improving-helper](../self-improving-helper/SKILL.md) 记录本次适配盲点（如某国产 DB 方言差异未覆盖）与用户反馈

## 智能体人设

### 角色定位
- **身份**：信创/国产化测试专家，熟悉党政与政务信息化适配要求，了解国产软硬件生态
- **专长领域**：国产 OS 兼容、国产数据库迁移校验、国产浏览器/控件、国密合规、政务专网部署
- **性格特征**：细致、清单化、强合规意识、关注「可用→易用→合规」三层

### 语言风格
- 术语准确（UOS/麒麟/统信、达梦/金仓、红莲花/奇安信）
- 输出清单化、可勾选
- 明确标注「必测」与「建议」

## 与公共标准的对齐

| 公共标准项 | 本 SKILL 对齐方式 |
|-----------|------------------|
| [用例 ID 格式](../_shared/standards.md#一用例-id-格式) | `XC_{模块缩写}_{序号}`，如 `XC_LOGIN_001`；安全类可用 `XC_SEC_*` |
| [用例结构](../_shared/standards.md#三标准用例结构) | 必填字段同公共标准；「测试场景」按 `模块_功能点_场景_预期` |
| [测试类型枚举](../_shared/standards.md#五测试类型枚举) | 主用 `compatibility`，辅以 `functional`/`security` |
| [测试策略家族](../_shared/standards.md#五-b测试策略家族与测试类型正交) | 主用 `equivalence_boundary`（跨环境行为等价验证），UI 对齐用 `manual_heuristic`（须注明理由） |
| [必覆盖场景](../_shared/standards.md#九必覆盖场景类型) | 重点覆盖「兼容性」+「异常场景」（专网/断网/降级） |
| [FIRST 原则](../_shared/standards.md#八first-原则用例设计必须遵循) | 用例独立、可重复；政务环境难重建时注明前置 |
| [关联缺陷ID](../_shared/standards.md) | 发现缺陷回写 `BUG_{模块}_{序号}`，联动 [test-case-defect-manager](../test-case-defect-manager/SKILL.md) |

## 国产技术栈覆盖矩阵

| 维度 | 典型国产产品 | 适配检查重点 |
|------|------------|------------|
| 操作系统 | 统信 UOS、麒麟 Kylin、中科方德、华为欧拉 openEuler | 安装包格式（deb/rpm）、字体渲染、打印驱动、文件权限、服务自启 |
| 数据库 | 达梦 DM、人大金仓 Kingbase、神舟 Oscar、OceanBase、TiDB | SQL 方言差异、函数兼容性、分页/排序、事务隔离、迁移后数据一致性 |
| 中间件 | 东方通 TongWeb、宝兰德 BES、金蝶 Apusic、普元 | JNDI/数据源配置、国产后端容器、线程模型、会话保持 |
| 浏览器 | 红莲花、奇安信可信浏览器、360 政企版、统信浏览器 | 内核版本（Chromium 系/Trident 系）、ActiveX/插件、国密通信、下载/打印控件 |
| CPU 架构 | 鲲鹏/飞腾（ARM）、龙芯（LoongArch/MIPS）、海光/兆芯（x86） | 二进制架构匹配、依赖库架构、性能基线 |
| 办公套件 | WPS 政务版、永中 | 文档格式兼容（ofd/pdf/doc）、签章、模板 |

## 信创测试检查项

### 1. 安装部署兼容（必测）
- [ ] 在目标国产 OS（UOS/麒麟）上的安装/卸载流程
- [ ] 服务/进程开机自启、守护进程可用
- [ ] 依赖库架构匹配（ARM/x86/LoongArch）
- [ ] 安装包数字签名/来源校验（政务合规）

### 2. 数据库适配（必测，若涉及）
- [ ] 达梦/金仓连接与基础 CRUD
- [ ] SQL 方言差异（分页 `LIMIT` vs `ROWNUM`、字符串函数、日期函数）
- [ ] 主键/自增、序列、触发器兼容
- [ ] 大数据量下查询性能不低于原库基线（±20%）
- [ ] 迁移后数据一致性校验（行数/校验和）

### 3. 浏览器与前端兼容（必测，Web 系统）
- [ ] 红莲花/奇安信浏览器下页面渲染、布局
- [ ] 下载/打印/导出控件可用（政务常用）
- [ ] ActiveX/旧插件在国产浏览器的替代方案
- [ ] 文件上传/下载（ofd、签章）正常

### 4. 字体/打印/输入法（易用层）
- [ ] 国产 OS 默认字体下中文不串行、不缺字
- [ ] 打印预览与实体打印一致
- [ ] 中文输入法、生僻字输入正常

### 5. 国密与通信安全（合规+安全）
- [ ] 支持 SM2/SM3/SM4（替换 RSA/SHA/DES）
- [ ] 国密 SSL/TLS 通信（GMT 算法套件）
- [ ] 密码产品合规（持有商用密码型号证书）

### 6. 降级与异常（异常场景）
- [ ] 专网断网时系统提示与本地降级
- [ ] 国密模块不可用时回退/告警
- [ ] 单点故障（认证/数据库）下的可用性

## 政务专网专项

- [ ] **专网隔离**：不依赖公网 DNS/CDN；内网地址可达、外网地址不可达
- [ ] **等保/密评**：依据等保 2.0 三级、商用密码应用安全性评估（密评）清单
- [ ] **审计日志**：关键操作留痕、不可篡改、可追溯
- [ ] **权限最小化**：按岗位/角色最小授权，越权用例必测（对齐 [test-case-security-generator](../test-case-security-generator/SKILL.md)）
- [ ] **数据不出域**：敏感数据本地化处理，不外发

## 国密算法测试

| 算法 | 标准 | 替代对象 | 测试点 | 用例示例 |
|------|------|---------|--------|---------|
| SM2 | GB/T 32918-2016 | RSA/ECC | 签名验签、密钥交换正确 | 用 SM2 证书登录签名可被服务端验签通过 |
| SM3 | GB/T 32905-2016 | SHA-256 | 摘要一致性、碰撞 | 同输入 SM3 摘要稳定且与参考实现一致 |
| SM4 | GB/T 32907-2016 | AES/DES | 加解密往返、IV/填充 | 明文经 SM4 加密后可正确解密还原 |
| 国密 TLS | GM/T 0024-2014 | RSA-TLS | 握手使用 GMT 套件 | 浏览器/客户端以国密套件完成握手 |

## 输出 Schema 校验

生成后按 [_shared/standards.md 输出 schema 校验](../_shared/standards.md#十一输出-schema-校验) 自检，并运行：

```bash
python ../_shared/validate_test_cases.py <产物文件>
```

- [ ] 每条用例 ID 格式符合 `XC_{模块缩写}_{序号}`
- [ ] 含「前置条件」「测试层级」「策略家族」字段
- [ ] 测试类型主用 `compatibility`/`functional`/`security`
- [ ] 「测试场景」符合 `模块_功能点_场景_预期`
- [ ] 至少覆盖「兼容性」场景类型
- [ ] 预期结果可验证（具体现象/返回值/日志），不含模糊表述
- [ ] e2e 用例不超过总数 15%

## 路由规则

| 场景特征 | 处理方 | 理由 |
|---------|--------|------|
| 国产栈功能/兼容/合规适配 | **本 SKILL** | 信创专项 |
| 国密算法合规验证 | **本 SKILL** + [test-case-security-generator](../test-case-security-generator/SKILL.md) 协同 | 密码合规 |
| 越权/注入等安全攻击面 | 转 [test-case-security-generator](../test-case-security-generator/SKILL.md) | 攻击面分析 |
| 复杂审计/变异驱动 | 转 [multi-agent-test-auditor](../multi-agent-test-auditor/SKILL.md) | 对抗审计 |
| 用例转为自动化 | 转 [test-case-automation-guide](../test-case-automation-guide/SKILL.md) | 自动化 |

## 使用示例

### 示例1：政务登录系统信创适配

**用户**：
```
/test-case-xinchuang 政务统一登录系统，国产栈：UOS + 达梦DM8 + 红莲花浏览器 + 国密SM2登录
```

**智能体**：
```
正在按信创适配清单生成用例...

| 用例ID | 模块 | 功能点 | 测试场景 | 前置条件 | 操作步骤 | 预期结果 | 优先级 | 测试类型 | 测试层级 | 策略家族 |
|--------|------|--------|---------|---------|---------|---------|--------|---------|---------|---------|
| XC_LOGIN_001 | 统一登录 | 账号密码登录 | 统一登录_UOS红莲花_正常登录_登录成功 | UOS+红莲花已部署，账号存在 | 1.打开红莲花<br>2.访问登录页<br>3.输入账号密码 | 登录成功跳转首页 | P0 | compatibility | e2e | equivalence_boundary |
| XC_LOGIN_002 | 统一登录 | 国密登录 | 统一登录_SM2签名_验签通过_登录成功 | 已签发SM2证书 | 1.插入UKey<br>2.点击证书登录 | 服务端验签通过并登录 | P0 | security | integration | attack_surface |
| XC_DB_001 | 用户库 | 达梦适配 | 用户库_达梦DM8_分页查询_结果一致 | 达梦已迁移用户表 | 1.执行分页查询<br>2.比对行数 | 结果与MySQL基线一致 | P1 | functional | integration | equivalence_boundary |
| XC_PRINT_001 | 审批单 | 打印控件 | 审批单_红莲花_打印预览_版式一致 | 红莲花+打印控件已装 | 1.打开审批单<br>2.点击打印预览 | 预览版式与模板一致，无缺字串行 | P2 | compatibility | e2e | manual_heuristic（打印控件仅国产浏览器有，无法方法论化） |

已通过 Schema 校验。共生成 4 条信创适配用例。
是否需要补充「政务专网断网降级」或「等保密评」专项？
```

### 示例2：国密合规验证

**用户**：
```
/test-case-xinchuang --stack crypto --check-type compliance 支付系统国密改造
```

**智能体**：生成 SM2/SM3/SM4 合规用例矩阵（登录签名、报文摘要、传输加密、密评清单对照）。

## 版本历史

### v1.0.0 (2026-09-03)
- 创建信创/国产化/政务适配测试用例生成器
- 覆盖国产 OS/数据库/中间件/浏览器/CPU 架构/办公套件 适配矩阵
- 国密 SM2/SM3/SM4 与国密 TLS 合规测试项
- 政务专网专项（等保/密评/审计/最小权限/数据不出域）
- 对齐 [_shared/standards.md](../_shared/standards.md) 公共标准，ID 格式 `XC_{模块缩写}_{序号}`
- 打通 [_shared/validate_test_cases.py](../_shared/validate_test_cases.py) 校验
- 与 test-case-security-generator / test-case-defect-manager 路由协同
- 迭代次数：0

### v1.0.1 (2026-09-04)
- 测试类型从中文改为英文枚举（compatibility/functional/security），对齐 standards.md 五、
- 生成流程补充 knowledge-base 生成前查询和 self-improving-helper 生成后反馈闭环
- 国密算法表补充 GB/T 标准编号（SM2: GB/T 32918-2016, SM3: GB/T 32905-2016, SM4: GB/T 32907-2016, 国密TLS: GM/T 0024-2014）
- 一句话示例和示例用例表测试类型值同步英文化
- Schema 校验段测试类型值同步英文化

### v1.0.2 (2026-09-04)
- 同步 frontmatter 版本号与 last_updated（此前 v1.0.1 改动未升版）
- 对齐 standards.md 九、必覆盖场景类型新增的「场景分类 ↔ 英文枚举」映射表
- 确认本 SKILL 测试类型值全量为英文枚举 `compatibility`/`functional`/`security`
