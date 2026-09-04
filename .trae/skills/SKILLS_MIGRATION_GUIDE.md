# 换电脑技能迁移清单（WorkBuddy Skills Migration Guide）

> 适用对象：`C:\Users\Administrator\.workbuddy\skills` 下的全部技能
> 编写日期：2026-09-04
> 配套文件：`SKILLS_REGISTERED.md`（技能注册表）

---

## 0. 结论速览（换电脑能直接用吗？）

| 类别 | 条目 | 换电脑能否直接用 | 原因 |
|---|---|---|---|
| **A 类** | 22 个（测试套件全家桶 + 新装 SkillHub 技能 + `_shared`） | ❌ **不能直接用，会变死链** | `.workbuddy\skills` 下只是**指向本机绝对路径**的 Junction 指针，新机没有那条路径 |
| **B 类** | 5 个（`attendance-ledger`、`law-skills__skillhub`、`pwa-jsdom-test`、`pwa-playwright-windows-testing`、`pwa-to-apk`） | ✅ **基本能，需配依赖** | 真实完整文件夹，内部**未写死本机路径**，拷走即可（前提是运行环境配齐） |
| 配置文件 | `_bm_skillid_migration.json` | 忽略 | WorkBuddy 自动生成的技能 ID 映射，重新扫描后会自动重建 |

**一句话**：A 类靠「git 同步真实文件 + 重建链接」；B 类靠「来源重装或整文件夹拷贝 + 配依赖」。

---

## 1. 当前技能家底（精确清单）

### A 类 — 链接指针（真身在 `.trae/skills`，该目录是 git 仓库）
- git remote：`https://github.com/CSGhy/Skill-generator.git`
- 分支：`main`，HEAD：`a377f21b10fbf0ce06602d9b2e3210753110329c`
- 链接指向：`D:\Program Files\Code\AiSkill\.trae\skills\<同名>`

| # | 技能名 | 说明 |
|---|---|---|
| 1 | `_shared` | 共享标准 / 校验器，被很多技能用 `../_shared/` 引用 |
| 2 | `alibabacloud-pts-ops` | 阿里云 PTS 云端压测（SkillHub 新装） |
| 3 | `jmeter-test-script-generator` | JMeter 脚本生成 |
| 4 | `knowledge-base` | 测试用例知识库 |
| 5 | `lanhu-requirements-doc` | 蓝湖需求文档生成 |
| 6 | `multi-agent-research-prover` | 数学证明多代理（保留未清理） |
| 7 | `multi-agent-test-auditor` | 测试多代理审计 |
| 8 | `performance-testing-toolkit` | HTTP 压测 / 负载 / 基准（SkillHub 新装） |
| 9 | `playwright` | Playwright 浏览器自动化 / MCP（SkillHub 新装） |
| 10 | `qa-test-data-gen` | 中文测试数据生成（SkillHub 新装） |
| 11 | `self-improving-helper` | 自我改进闭环 |
| 12 | `test-case-api-generator` | API 用例生成 |
| 13 | `test-case-automation-guide` | 自动化指导 |
| 14 | `test-case-defect-manager` | 缺陷管理 |
| 15 | `test-case-execution-helper` | 手工执行助手 |
| 16 | `test-case-generator` | 用例生成主入口 |
| 17 | `test-case-generator-core` | 用例生成核心 |
| 18 | `test-case-report-generator` | 测试报告 |
| 19 | `test-case-reviewer` | 用例评审 |
| 20 | `test-case-security-generator` | 安全用例 |
| 21 | `test-case-xinchuang` | 信创适配用例 |
| 22 | `weapp-automated-testing` | 微信小程序自动化（SkillHub 新装，**注：上游 name 拼写为 `weapp-automatd-testing`，属源库笔误，不影响调用**） |

### B 类 — 真实文件夹（独立安装，不在 `.trae/skills` 内）

| 技能名 | 来源推断 | 关键文件 | 迁移依赖 |
|---|---|---|---|
| `attendance-ledger` | 本地（配套 `D:\考勤台账\tools\`） | `SKILL.md` + `scripts/` | Python 3.11+ + openpyxl；需 `D:\考勤台账\` 台账文件 |
| `law-skills__skillhub` | SkillHub（名含 `__skillhub`） | `SKILL.md` + `_skillhub_meta.json` + `references/` | 用 SkillHub CLI 重装最稳；或整文件夹拷贝 |
| `pwa-to-apk` | 市场安装 | `SKILL.md` | Node.js + Java + Android SDK（TWA/PWABuilder 打包链） |
| `pwa-jsdom-test` | 市场安装 | `SKILL.md` | Node.js + jsdom/fake-indexeddb |
| `pwa-playwright-windows-testing` | 市场安装 | `SKILL.md` + `scripts/` + `references/` | Python + Playwright（需 `playwright install` 下载浏览器） |

---

## 2. A 类迁移（推荐：git 同步 + 重建链接）

### 方式一：git clone（最稳，推荐）
1. 新机上克隆真实文件仓库（**路径任意**，不必和本机一样）：
   ```bash
   git clone https://github.com/CSGhy/Skill-generator.git D:/repos/Skill-generator
   ```
2. 真实技能在 `D:/repos/Skill-generator/skills/`（含全部 22 个目录 + `_shared`）。
3. 运行下方「§4 重建链接脚本」，把 `.workbuddy\skills\<名>` 指向新机真实路径。
4. `../_shared` 相对引用自动成立（因为都在同一 `skills/` 目录下）。

### 方式二：无 git / 离线拷贝
1. 把本机 `D:\Program Files\Code\AiSkill\.trae\skills\` **整个真实目录**（22 个 + `_shared`）拷到新机某路径。
2. ⚠️ 用「跟随链接、复制真实内容」的方式拷贝（见 §3），**不要**把 `.workbuddy\skills` 下的链接指针原样搬过去。
3. 同样运行 §4 脚本重建链接。

---

## 3. 拷贝禁忌（死链陷阱）

> **坑**：用会「保留重解析点」的工具拷贝整个 `.workbuddy\skills`，会把死链一起搬过去，新机上全部失效。

| 做法 | 结果 | 建议 |
|---|---|---|
| `robocopy SRC DST /SL` | 复制链接本身 → 死链 | ❌ 禁用 |
| `xcopy /S`（默认对 junction 行为不确定） | 可能跳过或变死链 | ⚠️ 不推荐整目录拷 |
| **Explorer 直接拖拽** | 默认跟随链接、复制真实内容 → 变成真文件夹 | ✅ 可（仅限 B 类或整 skills 真实目录） |
| **逻辑迁移（git / 来源重装 + 重建链接）** | 干净、可复现 | ✅✅ 最推荐 |

**要点**：A 类走 git + 重建链接，B 类走来源重装或单独拷贝真实文件夹，**不要整目录 `robocopy /SL`**。

---

## 4. 重建链接脚本（PowerShell，新机上运行）

把 `$src` 改成新机上真实 `skills` 目录的路径（即含 22 个技能 + `_shared` 的那个目录）。

```powershell
$src = "D:\repos\Skill-generator\skills"   # ← 改成新机真实路径
$dst = "$env:USERPROFILE\.workbuddy\skills"

$names = @(
  "_shared",
  "alibabacloud-pts-ops",
  "jmeter-test-script-generator",
  "knowledge-base",
  "lanhu-requirements-doc",
  "multi-agent-research-prover",
  "multi-agent-test-auditor",
  "performance-testing-toolkit",
  "playwright",
  "qa-test-data-gen",
  "self-improving-helper",
  "test-case-api-generator",
  "test-case-automation-guide",
  "test-case-defect-manager",
  "test-case-execution-helper",
  "test-case-generator",
  "test-case-generator-core",
  "test-case-report-generator",
  "test-case-reviewer",
  "test-case-security-generator",
  "test-case-xinchuang",
  "weapp-automated-testing"
)

if (-not (Test-Path $src)) { Write-Error "源路径不存在: $src"; exit 1 }
New-Item -ItemType Directory -Path $dst -Force | Out-Null

foreach ($n in $names) {
  $link = Join-Path $dst $n
  $target = Join-Path $src $n
  if (-not (Test-Path $target)) { Write-Warning "跳过(源缺失): $n"; continue }
  if (Test-Path $link) { Remove-Item $link -Force -Recurse }
  New-Item -ItemType Junction -Path $link -Target $target -Force | Out-Null
  Write-Host ("[OK] {0} -> {1}" -f $n, $target)
}
Write-Host "链接重建完成。"
```

---

## 5. B 类迁移（按来源重装 / 拷贝）

| 技能 | 推荐做法 | 备注 |
|---|---|---|
| `attendance-ledger` | 从 `D:\考勤台账\tools\` 重新 install，或直接拷 `.workbuddy\skills\attendance-ledger` 整文件夹 | 新机需 Python 3.11+ + openpyxl，且 `D:\考勤台账\` 台账文件在位 |
| `law-skills__skillhub` | **SkillHub CLI 重装最稳**（带 `_skillhub_meta.json`）；或拷整文件夹 | 重装命令参考 SkillHub 文档 |
| `pwa-to-apk` | 来源重装或拷整文件夹 | 重依赖：Node + Java + Android SDK |
| `pwa-jsdom-test` | 来源重装或拷整文件夹 | Node + jsdom |
| `pwa-playwright-windows-testing` | 来源重装或拷整文件夹 | Python + `playwright install` 下载浏览器二进制 |

> B 类若选择「整文件夹拷贝」，用 Explorer 拖拽（跟随链接复制内容）即可，它们本身就是真实文件夹、无内部绝对路径依赖。

---

## 6. 依赖检查清单（新机环境）

- [ ] **Python 3.11+** + `pip install openpyxl`（attendance-ledger；pwa-jsdom/playwright-windows 视情况）
- [ ] **Node.js 22+**（pwa-to-apk、playwright MCP）
- [ ] **Java + Android SDK**（仅 pwa-to-apk）
- [ ] **Playwright 浏览器**：`playwright install chromium`（playwright / pwa-playwright-windows-testing）
- [ ] **SkillHub CLI**（B 类重装用）
- [ ] **git**（A 类 clone 用）
- [ ] **网络可达**：github.com（clone）、SkillHub 源（重装）

---

## 7. 迁移后验证（必做）

1. **重启 WorkBuddy 会话**（技能加载器启动时扫描 `.workbuddy\skills`）。
2. 调用测试：
   ```
   /test-case-generator
   /qa-test-data-gen
   /playwright
   ```
   能正常加载即成功。
3. 校验 `_shared` 引用：在任一测试技能内触发标准/校验器调用，确认 `../_shared/` 解析正常。
4. B 类抽查：`/attendance-ledger` 等能否加载、脚本路径是否可达。
5. 运行下方自检脚本，批量确认每个技能目录可达且含 `SKILL.md`。

### 迁移自检脚本（PowerShell）
```powershell
$base = "$env:USERPROFILE\.workbuddy\skills"
Get-ChildItem $base -Directory | ForEach-Object {
  $ok = Test-Path (Join-Path $_.FullName "SKILL.md")
  $lt = if ($_.LinkType) { $_.LinkType } else { "RealFolder" }
  Write-Host ("{0,-34} {1,-11} SKILL.md:{2}" -f $_.Name, $lt, $(if($ok){"✅"}else{"❌"}))
}
```

---

## 8. 一句话口诀

> **A 类（22个测试技能）**：git clone 真身 → 跑 §4 脚本建链接。
> **B 类（5个独立技能）**：来源重装最干净 / 或整文件夹拷 + 配依赖。
> **禁忌**：别 `robocopy /SL` 搬整个 `.workbuddy\skills`，会带死链。
> **收尾**：重启会话 → 抽查 `/test-case-generator` 等能调即完工。
