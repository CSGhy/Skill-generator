# 被测对象示例：用户登录接口

## 接口
- 路径：`POST /api/v1/login`
- Content-Type：`application/json`
- 鉴权：无（这是登录接口本身）

## 请求字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 4-32 字符，仅字母数字下划线 |
| password | string | 是 | 8-64 字符，至少含 1 字母 + 1 数字 |
| captcha | string | 是 | 6 位字符，5 分钟内有效，3 次内正确 |
| device_id | string | 否 | 设备指纹，用于风险评分 |

## 响应

成功 (200):
```json
{"token": "<jwt>", "expires_in": 3600, "user_id": 123}
```

失败 (401):
```json
{"error": "invalid_credentials", "retry_after": 60}
```

锁定 (429):
```json
{"error": "account_locked", "unlock_at": "2026-08-20T15:30:00Z"}
```

## 实现要点
- 数据库：`users` 表（username, password_hash, failed_count, locked_until）
- 密码：bcrypt 验证
- 缓存：Redis 存 captcha 与失败计数
- 审计：每次登录写 `login_log` 表（成功/失败/锁定/IP/UA）
