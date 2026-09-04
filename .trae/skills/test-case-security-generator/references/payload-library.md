# 攻击载荷库（安全测试用例生成参考）

本文件为 [../SKILL.md](../SKILL.md) 的 payload 知识库，供生成注入/越权/SSRF 等安全用例时直接取用。
每个分类给出：典型 payload、触发点、预期（断言/修复验证点）。

> ⚠️ 仅在**授权测试环境**使用本载荷库。禁止对未授权系统发起测试。

## SQL 注入

- **经典联合查询**：`' OR '1'='1` / `admin'--` / `' OR 1=1-- -`
- **报错注入**：`' AND EXTRACTVALUE(1,CONCAT(0x5c,(SELECT version())))-- -`
- **堆叠注入**：`; DROP TABLE users;--`
- **盲注（布尔）**：`' AND SUBSTRING(database(),1,1)='a'-- -`
- **时间盲注**：`' AND SLEEP(5)-- -`
- **预期**：参数化语句生效，响应不含数据库错误；返回通用错误且不泄露结构。

## NoSQL 注入

- **恒真（MongoDB）**：`{"username": {"$ne": null}, "password": {"$ne": null}}`
- **正则注入**：`{"username": {"$regex": ".*"}}`
- **预期**：驱动层做类型与结构校验，无法绕过认证。

## 命令注入

- **拼接**：`127.0.0.1; cat /etc/passwd` / `127.0.0.1 && whoami` / `` `id` ``
- **换行/管道**：`%0a` / `|` / `&`
- **预期**：禁止拼接 shell；输入做白名单与转义；返回「非法输入」。

## XSS（跨站脚本）

- **反射型**：`<script>alert(1)</script>` / `<img src=x onerror=alert(1)>`
- **存储型**：在昵称/评论字段写入以上 payload
- **DOM 型**：`#<script>...</script>`
- **预期**：输出做 HTML 实体编码；CSP 拦截内联脚本；不回显未过滤脚本。

## 越权（IDOR / 水平垂直）

- **水平越权**：用用户 A 的 token 访问 `GET /api/user/B/profile`（B≠A）
- **垂直越权**：普通用户 token 调用 `POST /api/admin/delete`
- **参数遍历**：枚举 `orderId=1001,1002,...`
- **预期**：返回 `403/404`；服务端按当前主体校验资源归属；不泄露他人数据。

## SSRF

- **内网探测**：`http://169.254.169.254/latest/meta-data/`（云元数据）
- **私网段**：`http://10.0.0.1:8080/admin` / `http://192.168.1.1`
- **协议走私**：`file:///etc/passwd` / `gopher://` / `dict://`
- **DNS rebinding**：域名解析在两次请求间切换为内网 IP
- **预期**：仅允许白名单域名/IP；解析后二次校验地址属公网；禁用 file/gopher 等协议。

## 路径遍历 / 任意文件读取

- **payload**：`../../../etc/passwd` / `..%2f..%2f..%2f` / `%2e%2e/`
- **预期**：规范化后限制在项目根目录；拒绝 `..` 跳出；返回 `403`。

## 反序列化

- **Java**：构造恶意 `gadget` 链（如 CommonsCollections）
- **PHP**：`unserialize()` 可控输入触发魔术方法
- **预期**：反序列化类型白名单；禁用危险类；输入签名校验。

## 敏感信息泄露（响应/错误）

- **触发**：提交非法参数使服务端抛栈
- **预期**：返回通用错误页；不回显堆栈/SQL/内部 IP/密钥；错误日志仅服务端可见。

---

### 使用约定

- 生成用例时在「操作步骤」嵌入对应 payload，「预期结果」写明状态码/响应特征/日志要求。
- 复杂组合攻击（如 SSRF + 云元数据 + 提权）归入 `fuzz_chaos` 或转交 `multi-agent-test-auditor`。
- 与 [owasp-top10.md](./owasp-top10.md) 配合：payload 类别 → 映射 OWASP A0x。
