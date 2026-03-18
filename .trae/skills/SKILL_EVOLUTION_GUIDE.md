# Skill进化系统使用指南

## 📖 概述

基于AutoSkill和XSKILL理论，本系统实现了Skill的自我进化能力，让Skill能够从用户反馈中学习，不断优化自身。

## 🎯 核心特性

### 1. 版本控制
- 自动管理版本号（major.minor.patch）
- 记录每次迭代的详细信息
- 支持版本历史追溯

### 2. 反馈收集
- 自动收集用户满意度
- 记录质量评分
- 追踪调整建议
- 分析常见问题

### 3. 智能进化
- **MERGE**：满意度>4.5分，合并优化，版本号+1
- **ADD**：满意度3.0-4.5分，添加新能力，补丁号+1
- **DISCARD**：满意度<3.0分，标记为需要重构

### 4. 数据分析
- 计算平均满意度
- 计算平均质量
- 计算调整率
- 提取常见问题

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/CSGhy/Skill-generator.git

# 进入目录
cd Skill-generator/.trae/skills
```

### 添加反馈

```bash
# 为测试用例生成器添加反馈
python skill_evolution.py --skill test-case-generator/SKILL.md --add-feedback

# 为蓝湖需求文档生成器添加反馈
python skill_evolution.py --skill lanhu-requirements-doc/SKILL.md --add-feedback
```

**交互式输入**：
```
📝 添加用户反馈
==================================================
用户：张三
功能描述：测试登录功能
满意度 (1-5)：5
质量 (1-5)：5
是否需要调整 (y/n)：n
调整建议：无

✅ 反馈已保存：测试登录功能 - 满意度：5分
```

### 执行进化

```bash
# 为测试用例生成器执行进化
python skill_evolution.py --skill test-case-generator/SKILL.md --evolve

# 为蓝湖需求文档生成器执行进化
python skill_evolution.py --skill lanhu-requirements-doc/SKILL.md --evolve
```

**进化输出**：
```
🧬 执行Skill进化
==================================================

📊 反馈分析：
   平均满意度：4.2分
   平均质量：4.5分
   调整率：15%
   常见问题：缺少边界测试, 缺少性能测试

🧬 进化策略：ADD
   添加新能力，版本号更新为：v1.2.1
   ✅ 进化完成！
```

## 📊 进化示例

### 示例1：高质量反馈

**反馈数据**：
```json
[
  {
    "user": "张三",
    "function": "测试登录功能",
    "satisfaction": 5,
    "quality": 5,
    "needs_adjustment": false,
    "suggestions": ""
  },
  {
    "user": "李四",
    "function": "测试购物车功能",
    "satisfaction": 5,
    "quality": 5,
    "needs_adjustment": false,
    "suggestions": ""
  }
]
```

**进化结果**：
- 平均满意度：5.0分
- 进化策略：MERGE
- 版本更新：v1.2.0 → v1.3.0
- 迭代次数：+1

### 示例2：中等质量反馈

**反馈数据**：
```json
[
  {
    "user": "王五",
    "function": "测试注册功能",
    "satisfaction": 4,
    "quality": 4,
    "needs_adjustment": true,
    "suggestions": "缺少边界测试"
  },
  {
    "user": "赵六",
    "function": "测试支付功能",
    "satisfaction": 4,
    "quality": 4,
    "needs_adjustment": true,
    "suggestions": "缺少性能测试"
  }
]
```

**进化结果**：
- 平均满意度：4.0分
- 进化策略：ADD
- 版本更新：v1.2.0 → v1.2.1
- 迭代次数：+1
- 常见问题：缺少边界测试, 缺少性能测试

### 示例3：低质量反馈

**反馈数据**：
```json
[
  {
    "user": "孙七",
    "function": "测试订单功能",
    "satisfaction": 2,
    "quality": 2,
    "needs_adjustment": true,
    "suggestions": "测试用例不完整"
  },
  {
    "user": "周八",
    "function": "测试搜索功能",
    "satisfaction": 2,
    "quality": 2,
    "needs_adjustment": true,
    "suggestions": "缺少负向测试"
  }
]
```

**进化结果**：
- 平均满意度：2.0分
- 进化策略：DISCARD
- 建议：Skill需要重构
- 常见问题：测试用例不完整, 缺少负向测试

## 🔧 高级用法

### 批量添加反馈

```python
from skill_evolution import SkillEvolution

evolution = SkillEvolution('test-case-generator/SKILL.md')

# 批量添加反馈
feedbacks = [
    {
        'user': '张三',
        'function': '测试登录功能',
        'satisfaction': 5,
        'quality': 5,
        'needs_adjustment': False,
        'suggestions': ''
    },
    {
        'user': '李四',
        'function': '测试购物车功能',
        'satisfaction': 4,
        'quality': 4,
        'needs_adjustment': True,
        'suggestions': '缺少边界测试'
    }
]

for feedback in feedbacks:
    evolution.add_feedback(feedback)

# 执行进化
evolution.evolve()
```

### 自动化进化流程

```python
import schedule
import time
from skill_evolution import SkillEvolution

def auto_evolve():
    """自动进化"""
    skills = [
        'test-case-generator/SKILL.md',
        'lanhu-requirements-doc/SKILL.md'
    ]
    
    for skill_path in skills:
        evolution = SkillEvolution(skill_path)
        evolution.evolve()

# 每周执行一次进化
schedule.every().week.do(auto_evolve)

while True:
    schedule.run_pending()
    time.sleep(3600)  # 每小时检查一次
```

### 集成到CI/CD

```yaml
# .github/workflows/skill-evolution.yml
name: Skill Evolution

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日凌晨执行
  workflow_dispatch:

jobs:
  evolve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Execute evolution
        run: |
          python .trae/skills/skill_evolution.py \
            --skill .trae/skills/test-case-generator/SKILL.md \
            --evolve
          python .trae/skills/skill_evolution.py \
            --skill .trae/skills/lanhu-requirements-doc/SKILL.md \
            --evolve
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "chore: 自动进化Skill"
          git push
```

## 📈 进化效果追踪

### 版本历史

每个Skill都会记录详细的版本历史：

```
## 版本历史

### v1.3.0 (2024-01-27)
- 合并优化：添加边界测试
- 合并优化：添加性能测试
- 迭代次数：6

### v1.2.1 (2024-01-20)
- 添加新能力：支持UI测试
- 迭代次数：5

### v1.2.0 (2024-01-15)
- 优化参数Schema设计
- 添加错误处理机制
- 添加工具按需加载
- 迭代次数：4

### v1.1.0 (2024-01-01)
- 初始版本发布
- 迭代次数：0
```

### 反馈分析

系统会自动分析反馈并更新：

```
### 反馈分析
- 平均满意度：4.2分
- 平均质量：4.5分
- 调整率：15%
- 常见问题：缺少边界测试, 缺少性能测试
```

## 🎯 最佳实践

### 1. 定期收集反馈
- 每次使用后收集反馈
- 确保反馈的真实性
- 记录详细的调整建议

### 2. 定期执行进化
- 建议每周执行一次
- 或者收集10条反馈后执行
- 避免频繁进化导致版本混乱

### 3. 监控进化效果
- 跟踪版本变化
- 分析满意度趋势
- 评估质量提升

### 4. 人工审查DISCARD
- 当策略为DISCARD时，人工审查
- 分析常见问题
- 重新设计Skill架构

### 5. 版本发布
- 重要进化后发布新版本
- 记录详细的更新日志
- 通知用户更新

## 🔮 未来规划

### 阶段2：中级进化（1-2个月）

- [ ] 实现自动Skill合并
- [ ] 实现跨场景迁移
- [ ] 实现质量保证机制
- [ ] 添加性能监控

### 阶段3：高级进化（3-6个月）

- [ ] 实现Experience Bank
- [ ] 实现Cross-Rollout Critique
- [ ] 实现Hierarchical Consolidation
- [ ] 实现零样本迁移

## 📞 支持

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- 技术支持邮箱
- 社区论坛

## 📄 许可证

MIT License
