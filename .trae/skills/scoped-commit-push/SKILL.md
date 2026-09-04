---
name: "scoped-commit-push"
description: "按类别精确暂存指定文件（绝不 git add -A），按仓库 Conventional Commits 规范提交，经代理重试推送并用 ls-remote 比对哈希核实。当用户要求只提交/推送某一类改动（如只提交技能、规则、README）、或需要安全提交避免夹带无关文件时调用。"
---

# 范围化提交与安全推送 (Scoped Commit & Safe Push)

在工作区 `d:\Program Files\Code\AiSkill` 中执行"**只提交某一类改动并安全推送**"的标准流程。核心目标：**提交内容与用户意图严格一致，绝不夹带无关文件；推送后必须远程核实**。

## 何时使用

- 用户要求"只提交 SKILL / 规则 / README / 某目录的改动，其他都不提交"
- 用户要求提交并推送到远程，且工作区存在大量无关的未跟踪文件（测试脚本、临时文件、数据产物等）
- 任何需要"精确控制提交范围"的 git 提交场景

不适用：用户明确要求提交全部改动（此时仍需先 `git status` 向用户展示清单并确认）。

## 环境事实（本工作区）

- **Git 可执行文件**：`D:\ProgramData\Git\cmd\git.exe`（自定义安装目录，未加入系统 PATH）。终端中若无 `git` 命令，用此全路径调用。
- **远程仓库**：`https://github.com/CSGhy/Skill-generator.git`，分支 `main`。
- **代理**：国内直连 GitHub 443 常超时。本仓库已配置 `http.proxy=http://127.0.0.1:7897`（Clash Verge）。若推送报 `Failed to connect to github.com:443` / `Connection was reset`：
  1. 先探测代理端口：`Test-NetConnection 127.0.0.1 -Port <p>`（常见 7897/7890/10809/9000）；
  2. 代理在监听则配置（**仓库级**，非 --global）：
     ```powershell
     & $git config http.proxy http://127.0.0.1:7897
     & $git config https.proxy http://127.0.0.1:7897
     ```
  3. 代理未运行则告知用户开启，不要反复盲试。
- **中文文件名**：git 默认把中文路径转义为八进制（`\346\265\213...`），会导致路径前缀校验误判。所有查看/核对命令必须加 `-c core.quotepath=false`。
- **PowerShell 执行策略报错**（`无法加载 profile-snapshot.ps1`）是环境噪声，忽略即可，不影响 git 命令。

## 标准流程（7 步，每步有闸门）

### 1. 查看全貌

```powershell
$git = "D:\ProgramData\Git\cmd\git.exe"
& $git -C "d:\Program Files\Code\AiSkill" status
```

向用户明确列出：**哪些属于本次要提交的类别、哪些明确排除**，并说明判断依据（如 `.trae/rules/` 是规则不是技能）。

### 2. 显式暂存（禁止 git add -A / git add .）

只暂存明确路径，按类别给目录或文件：

```powershell
& $git -C "d:\Program Files\Code\AiSkill" add .trae/skills/ .trae/_removed_skills/
```

### 3. 核对暂存区（硬闸门，不过不提交）

```powershell
$staged = & $git -C "d:\Program Files\Code\AiSkill" -c core.quotepath=false diff --cached --name-only
$outside = $staged | Where-Object { $_ -notlike '<允许的路径前缀>/*' }
if ($outside) { Write-Output "中止：发现范围外文件 $outside" } else { Write-Output "✅ 暂存区范围正确，共 $($staged.Count) 个文件" }
```

- 暂存区**有且仅有**目标文件，发现越界文件立即停止并报告。
- 注意：删除/移动的文件也会被 `git add <目录>` 正确暂存（显示为 R/D），核对时用 `diff --cached --name-status` 可看操作类型。

### 4. 按规范提交

遵循仓库规则 [.trae/rules/git-commit-message.md](../../rules/git-commit-message.md)：格式 `<type>(<scope>): <subject>`。

- **type 用英文小写**：`feat` / `fix` / `test` / `docs` / `refactor` / `perf` / `style` / `chore`
- **subject 用中文**，≤50 字，不加句号，不用"修复了/增加了"等冗余前缀
- scope 约定：改技能用技能目录名（如 `test-case-xinchuang`）；改 `_shared/` 用 `shared`；改规则用 `rules`；改 README 用 `readme`
- 示例：
  - `feat(skills): 新增多个测试技能并优化现有技能，归档 skill-cleaner`
  - `docs(rules): 新增测试用例质量规范等三条工作区规则`
  - `docs(readme): 更新为完整测试技能套件说明`

```powershell
& $git -C "d:\Program Files\Code\AiSkill" -c core.quotepath=false commit -m "docs(rules): 中文简述"
```

复杂改动可用多个 `-m` 追加正文（说明"为什么"）。

### 5. 推送（带网络容错）

```powershell
& $git -C "d:\Program Files\Code\AiSkill" push origin main 2>&1 | ForEach-Object { Write-Output $_ }
```

- 失败时最多重试 5 次、每次间隔 5 秒；持续失败则转代理排查（见"环境事实"），不要无限重试。
- git 的进度信息走 stderr，PowerShell 中表现为红色文本但**退出码为 0 即成功**，以 `$LASTEXITCODE` 为准。

### 6. 远程核实（硬闸门）

推送成功必须用 `ls-remote` 直接查远程服务器（不信本地缓存），比对哈希：

```powershell
$local  = & $git -C "d:\Program Files\Code\AiSkill" rev-parse main
$remote = ((& $git -C "d:\Program Files\Code\AiSkill" ls-remote origin refs/heads/main 2>&1) -split "`t")[0]
if ($remote -eq $local) { "✅ 一致：已推送到远程" } else { "⚠️ 不一致：$remote" }
```

### 7. 汇报结果

向用户报告：提交哈希与信息、文件数/增删行、本地与远程哈希一致、**哪些文件按要求保持未提交**。

## 反模式（显式禁止）

- ❌ `git add -A` / `git add .` —— 会把测试脚本、临时文件（`.dl_log*.txt`、`.zip`、`.jmx`、数据产物）一并卷入
- ❌ 不核对暂存区直接 commit
- ❌ 不带 `core.quotepath=false` 核对中文路径（八进制转义会让前缀匹配失效，误报或漏报）
- ❌ 推送后只看 "Everything up-to-date" 或退出码就宣布成功——必须 `ls-remote` 比对哈希
- ❌ 网络失败时不排查代理、盲目反复推送
- ❌ 把规则文件（`.trae/rules/`）当技能提交，或反之——提交前与用户确认类别边界
- ❌ 用 `--global` 写代理配置（影响其他仓库）；代理配置只写当前仓库
- ❌ 未经用户要求执行 `push --force`、重置、删除分支等破坏性操作

## 常用速查

```powershell
$git = "D:\ProgramData\Git\cmd\git.exe"
$repo = "d:\Program Files\Code\AiSkill"

# 状态（中文路径正常显示）
& $git -C $repo -c core.quotepath=false status

# 最近提交
& $git -C $repo log -3 --oneline

# 按类别暂存 + 核对 + 提交（示例：只提交 README）
& $git -C $repo add README.md
& $git -C $repo -c core.quotepath=false diff --cached --name-only
& $git -C $repo -c core.quotepath=false commit -m "docs(readme): 中文简述"

# 推送 + 远程核实
& $git -C $repo push origin main
(& $git -C $repo ls-remote origin refs/heads/main) -split "`t" | Select-Object -First 1
```
