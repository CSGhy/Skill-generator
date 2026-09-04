# 测试技能套件 · 注册完成报告

日期：2026-09-03
操作人：WorkBuddy（Agent 模式）

## 做了什么
**没有移动/复制任何原文件。** 在用户级标准发现路径 `C:\Users\Administrator\.workbuddy\skills\` 下，为 `.trae/skills/` 里的每个 skill 建立**目录 junction（目录联接，等同于符号链接）**，指向原始目录。原文件零改动，相对引用全部保持可解析。

## 为什么用 junction 而不是移动
这些 SKILL.md 内部大量使用相对引用：
- `../_shared/standards.md`、`../test-case-xxx/SKILL.md`（兄弟目录）
- `../../rules/测试金字塔原则.md`（上一级 `.trae/rules/`）

一旦把文件搬走，这些相对路径会全部断裂。junction 让"标准发现路径"直接映射到原目录，引用天然成立。

## 已注册的链接
标准路径 → 原始路径：
- `~/.workbuddy/skills/<每个 skill>` → `D:\Program Files\Code\AiSkill\.trae\skills\<同名>`
  - 共 16 个：jmeter-test-script-generator、knowledge-base、lanhu-requirements-doc、multi-agent-research-prover、multi-agent-test-auditor、self-improving-helper、test-case-api-generator、test-case-automation-guide、test-case-defect-manager、test-case-execution-helper、test-case-generator、test-case-generator-core、test-case-report-generator、test-case-reviewer、test-case-security-generator、test-case-xinchuang
- `~/.workbuddy/skills/_shared` → `…\.trae\skills\_shared`
- `~/.workbuddy/rules` → `D:\Program Files\Code\AiSkill\.trae\rules`（解析 `../../rules` 引用）

## 验证结果
| 检查项 | 结果 |
|---|---|
| junction 指向正确 | ✅ |
| 跨链读 SKILL.md | ✅ 628 行可读取 |
| `../_shared/standards.md` 解析 | ✅ 310 行可读取 |
| `../../rules/` 解析 | ✅ 4 个规范文件可见 |

## 如何让技能真正"可调"
WorkBuddy 的技能加载器在会话启动时扫描 `~/.workbuddy/skills/`。**请重启或刷新一次 WorkBuddy 会话**，让它重新扫描，之后即可通过 `/test-case-generator`、`/test-case-xinchuang` 等命令直接调用。

## 如何还原（可逆）
删除这些 junction 只会移除链接、不会动原文件：
```powershell
# 在 PowerShell 中逐个删除，或批量：
Get-ChildItem "C:\Users\Administrator\.workbuddy\skills" | Where-Object { $_.Attributes -match "ReparsePoint" } | Remove-Item -Force
Remove-Item "C:\Users\Administrator\.workbuddy\rules" -Force
```

## 2026-09-04 新增 5 个外部技能（SkillHub 补充）

背景：盘点 GitHub / Gitee / SkillHub 后，确认原 16 个技能已覆盖功能测试生命周期，但缺"测试数据生成、小程序/移动端自动化、专项性能(k6/PTS)、UI 自动驱动"。本次从 SkillHub 安装 5 个补齐缺口。

新增技能（真实目录在 `.trae/skills/`，并在 `.workbuddy/skills/` 建 junction 同步可见）：

| 技能目录 | 来源 | 补齐的缺口 | 主要能力 |
|---|---|---|---|
| `qa-test-data-gen` | SkillHub (clawhub) | 测试数据生成（原缺失） | 中文区域测试数据：姓名/身份证/手机/地址/银行卡等 |
| `weapp-automated-testing` | SkillHub | 小程序自动化（原缺失） | 微信小程序启动/导航/交互/截图/控制台日志 |
| `performance-testing-toolkit` | SkillHub | 专项性能（原仅 jmeter） | HTTP 压测/负载/基准 + 报告 |
| `alibabacloud-pts-ops` | SkillHub | 云端压测（原缺失） | 阿里云 PTS 场景创建与管理 |
| `playwright` | SkillHub | UI 自动驱动（原仅手工执行 helper） | Playwright 浏览器自动化 / MCP / 爬虫 |

新增后：`.trae/skills/` 共 **21** 个测试相关技能 + `_shared` + 文档。

### 后续新增技能的规范（重要）
本套件标准做法：**真实文件放 `.trae/skills/<name>`，再在 `.workbuddy/skills/<name>` 建 Junction 同步**。
这样既能用 Trae IDE 编辑原文件，又能被 WorkBuddy 标准发现路径扫描到。

PowerShell 建 junction：
```powershell
New-Item -ItemType Junction -Path "C:\Users\Administrator\.workbuddy\skills\<name>" -Target "D:\Program Files\Code\AiSkill\.trae\skills\<name>" -Force
```

从 SkillHub 下载（注意：本沙箱下 `curl -o file` 会报 write error 23 写失败，必须用 shell 重定向 `>`）：
```bash
curl -L -s "https://lightmake.site/api/v1/download?slug=<slug>" > /tmp/<slug>.zip
python3 -c "import zipfile; zipfile.ZipFile('/tmp/<slug>.zip').extractall(r'D:\Program Files\Code\AiSkill\.trae\skills\<slug>')"
```
还原（只删链接不碰原文件）：
```powershell
Get-ChildItem "C:\Users\Administrator\.workbuddy\skills" | Where-Object { $_.Attributes -match "ReparsePoint" } | Remove-Item -Force
```
