# OWASP Top 10 详解（安全测试用例生成参考）

本文件为 [../SKILL.md](../SKILL.md) 的攻击面知识库，供生成安全测试用例时检索。
每条目给出：典型攻击形态、断言/预期（验证点）、修复要点、推荐策略家族。

> 用例 ID 统一使用 `SEC_{模块缩写}_{序号}`；测试类型固定 `security`；策略家族主用 `attack_surface`，复杂审计可叠加 `fuzz_chaos` / `mutation_test`。

## A01 失效的访问控制（Broken Access Control）

- **典型攻击**：水平越权（用户 A 访问用户 B 资源）、垂直越权（普通用户调管理员接口）、目录遍历、强制浏览隐藏 URL。
- **断言/预期**：
  - 越权请求应返回 `403` / `404`，且不泄露目标用户数据；
  - 服务端日志记录越权尝试；
  - 关键操作需二次鉴权（如改密、删数据）。
- **修复要点**：默认拒绝；服务端做对象级授权校验（非仅前端隐藏）；集中化访问控制中间件。
- **策略家族**：`attack_surface`

## A02 加密机制失效（Cryptographic Failures）

- **典型攻击**：明文传输密码/敏感信息、弱算法（MD5/DES）、硬编码密钥、敏感数据落库未加密。
- **断言/预期**：
  - 登录/支付流量必须 HTTPS（TLS1.2+）；
  - 响应体不含明文密码、身份证、银行卡号；
  - 存储的密码为加盐哈希（bcrypt/argon2）。
- **修复要点**：传输层强制 TLS；敏感字段加密存储；禁用弱算法；密钥走 KMS/配置中心。
- **策略家族**：`attack_surface`

## A03 注入（Injection）

- **典型攻击**：SQL 注入、NoSQL 注入、OS 命令注入、LDAP/XPath 注入、XXE。
- **断言/预期**：
  - 注入 payload 被参数化/转义处理，不进入解释器；
  - 响应不含数据库错误堆栈/内部结构；
  - 返回通用错误，不泄露 SQL 片段。
- **修复要点**：预编译语句（Prepared Statement）、ORM 参数绑定、输入白名单校验、最小数据库账号权限。详见 [payload-library.md](./payload-library.md#sql-注入)。
- **策略家族**：`attack_surface` / `fuzz_chaos`

## A04 不安全设计（Insecure Design）

- **典型攻击**：业务逻辑缺陷（并发下单、越权退款、流程绕过）。
- **断言/预期**：需威胁建模确认；本 SKILL 仅产出用例骨架，深度审计转交 `multi-agent-test-auditor`。
- **修复要点**：安全需求左移、威胁建模（STRIDE）、业务规则完整性校验。
- **策略家族**：`attack_surface`（骨架）/ 转交审计

## A05 安全配置错误（Security Misconfiguration）

- **典型攻击**：默认凭据、目录列举、不必要的 HTTP 方法（PUT/DELETE）、暴露的调试端点、缺失安全响应头。
- **断言/预期**：
  - 默认账号不可登录；
  - 未授权目录返回 `403`；
  - 响应含 `X-Content-Type-Options`、`Content-Security-Policy` 等安全头。
- **修复要点**：安全基线模板、关闭不必要服务、定期配置扫描、错误信息脱敏。
- **策略家族**：`attack_surface`

## A06 脆弱和过时的组件（Vulnerable & Outdated Components）

- **典型攻击**：已知 CVE 依赖（Log4j、Fastjson）、依赖混淆、投毒。
- **断言/预期**：
  - `npm audit` / `pip-audit` / `OWASP Dependency-Check` 零高危；
  - 锁文件完整、来源可信。
- **修复要点**：依赖清单 + 版本钉死 + 定期升级；SCA 工具接入 CI。
- **策略家族**：`attack_surface` / 转交审计（供应链）

## A07 身份认证失败（Identification & Authentication Failures）

- **典型攻击**：暴力破解、弱密码、会话固定、JWT 无失效、密码找回绕过。
- **断言/预期**：
  - 连续失败 N 次后账号/ IP 锁定；
  - 会话空闲超时失效；
  - 找回密码链路带一次性 token，且不可枚举。
- **修复要点**：多因素认证、速率限制、安全会话管理、密码策略。
- **策略家族**：`attack_surface`

## A08 软件和数据完整性失败（Software & Data Integrity Failures）

- **典型攻击**：不安全的反序列化、未签名更新、CI/CD 投毒。
- **断言/预期**：
  - 反序列化输入白名单校验，拒绝非法类型；
  - 更新包有签名校验。
- **修复要点**：签名验证、可信源、隔离构建环境。
- **策略家族**：`attack_surface` / `mutation_test`

## A09 安全日志和监控失败（Security Logging & Monitoring Failures）

- **典型攻击**：攻击无日志、告警无响应、日志被篡改。
- **断言/预期**：需运行时审计；本 SKILL 仅要求「越权/注入等事件必须留痕」，深度审计转交 `multi-agent-test-auditor`。
- **修复要点**：集中日志、关键事件告警、防篡改。
- **策略家族**：转交审计

## A10 服务端请求伪造（SSRF）

- **典型攻击**：内网地址访问、云元数据 `169.254.169.254`、协议走私、DNS rebinding。
- **断言/预期**：
  - 拒绝访问内网/私网地址；
  - 不返回云元数据；
  - 记录 SSRF 尝试。
- **修复要点**：URL 白名单 + 解析后地址校验（阻断私网）、禁用非常用协议、出网代理隔离。
- **策略家族**：`attack_surface`

---

### 一键排查清单（生成用例时对照）

- [ ] 每条 OWASP 类别至少 1 条用例（A04/A09 标注转交审计）
- [ ] 注入类至少覆盖 SQL / NoSQL / 命令 三类
- [ ] 越权类至少覆盖水平 + 垂直
- [ ] 每个用例含可验证断言（状态码/响应特征/日志/行为差异）
- [ ] 风险等级字段已标注（critical/high/medium/low）
