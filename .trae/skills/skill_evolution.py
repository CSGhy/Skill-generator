#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill进化系统
基于AutoSkill和XSKILL理论，实现Skill的自我进化能力
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SkillEvolution:
    """Skill进化系统"""
    
    def __init__(self, skill_path: str):
        """
        初始化进化系统
        
        Args:
            skill_path: Skill文件路径
        """
        self.skill_path = Path(skill_path)
        self.skill_content = self._load_skill()
        self.version = self._parse_version()
        self.feedback_history = self._load_feedback_history()
    
    def _load_skill(self) -> str:
        """加载Skill内容"""
        with open(self.skill_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_version(self) -> Dict[str, int]:
        """解析当前版本号"""
        version_pattern = r'### v(\d+)\.(\d+)\.(\d+)'
        match = re.search(version_pattern, self.skill_content)
        
        if match:
            return {
                'major': int(match.group(1)),
                'minor': int(match.group(2)),
                'patch': int(match.group(3))
            }
        return {'major': 1, 'minor': 0, 'patch': 0}
    
    def _load_feedback_history(self) -> List[Dict]:
        """加载反馈历史"""
        feedback_file = self.skill_path.parent / 'feedback.json'
        
        if feedback_file.exists():
            with open(feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_feedback(self, feedback: Dict):
        """保存反馈"""
        self.feedback_history.append(feedback)
        
        feedback_file = self.skill_path.parent / 'feedback.json'
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_history, f, ensure_ascii=False, indent=2)
    
    def _analyze_feedback(self) -> Dict:
        """分析反馈，决定进化策略"""
        if not self.feedback_history:
            return {
                'strategy': 'ADD',
                'satisfaction': 0,
                'quality': 0,
                'adjustment_rate': 0,
                'common_issues': []
            }
        
        satisfaction_scores = [f.get('satisfaction', 0) for f in self.feedback_history]
        quality_scores = [f.get('quality', 0) for f in self.feedback_history]
        adjustment_flags = [f.get('needs_adjustment', False) for f in self.feedback_history]
        
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
        avg_quality = sum(quality_scores) / len(quality_scores)
        adjustment_rate = sum(adjustment_flags) / len(adjustment_flags) * 100
        
        common_issues = self._extract_common_issues()
        
        if avg_satisfaction >= 4.5:
            strategy = 'MERGE'
        elif avg_satisfaction >= 3.0:
            strategy = 'ADD'
        else:
            strategy = 'DISCARD'
        
        return {
            'strategy': strategy,
            'satisfaction': avg_satisfaction,
            'quality': avg_quality,
            'adjustment_rate': adjustment_rate,
            'common_issues': common_issues
        }
    
    def _extract_common_issues(self) -> List[str]:
        """提取常见问题"""
        issues = []
        
        for feedback in self.feedback_history:
            suggestions = feedback.get('suggestions', '')
            if suggestions:
                issues.append(suggestions)
        
        from collections import Counter
        issue_counts = Counter(issues)
        
        return [issue for issue, count in issue_counts.most_common(5)]
    
    def _increment_version(self, version_type: str = 'patch'):
        """增加版本号
        
        Args:
            version_type: 版本类型 (major/minor/patch)
        """
        if version_type == 'major':
            self.version['major'] += 1
            self.version['minor'] = 0
            self.version['patch'] = 0
        elif version_type == 'minor':
            self.version['minor'] += 1
            self.version['patch'] = 0
        else:
            self.version['patch'] += 1
        
        return f"v{self.version['major']}.{self.version['minor']}.{self.version['patch']}"
    
    def _update_version_in_skill(self, new_version: str):
        """更新Skill中的版本号"""
        version_pattern = r'### v\d+\.\d+\.\d+'
        new_version_line = f'### {new_version}'
        
        self.skill_content = re.sub(version_pattern, new_version_line, self.skill_content)
        
        with open(self.skill_path, 'w', encoding='utf-8') as f:
            f.write(self.skill_content)
    
    def _add_iteration_count(self):
        """增加迭代次数"""
        iteration_pattern = r'- 迭代次数：(\d+)'
        match = re.search(iteration_pattern, self.skill_content)
        
        if match:
            current_count = int(match.group(1))
            new_count = current_count + 1
            new_line = f'- 迭代次数：{new_count}'
            
            self.skill_content = re.sub(iteration_pattern, new_line, self.skill_content)
            
            with open(self.skill_path, 'w', encoding='utf-8') as f:
                f.write(self.skill_content)
    
    def _update_feedback_analysis(self, analysis: Dict):
        """更新反馈分析"""
        feedback_section = f"""### 反馈分析
- 平均满意度：{analysis['satisfaction']:.1f}分
- 平均质量：{analysis['quality']:.1f}分
- 调整率：{analysis['adjustment_rate']:.0f}%
- 常见问题：{', '.join(analysis['common_issues']) if analysis['common_issues'] else '无'}
"""
        
        analysis_pattern = r'### 反馈分析.*?(?=###|$)'
        self.skill_content = re.sub(analysis_pattern, feedback_section, self.skill_content, flags=re.DOTALL)
        
        with open(self.skill_path, 'w', encoding='utf-8') as f:
            f.write(self.skill_content)
    
    def add_feedback(self, feedback: Dict):
        """添加用户反馈
        
        Args:
            feedback: 反馈字典
                - user: 用户
                - function: 功能描述
                - satisfaction: 满意度 (1-5)
                - quality: 质量 (1-5)
                - needs_adjustment: 是否需要调整
                - suggestions: 调整建议
        """
        feedback['timestamp'] = datetime.now().isoformat()
        self._save_feedback(feedback)
        
        print(f"✅ 反馈已保存：{feedback['function']} - 满意度：{feedback['satisfaction']}分")
    
    def evolve(self):
        """执行进化"""
        analysis = self._analyze_feedback()
        
        print(f"\n📊 反馈分析：")
        print(f"   平均满意度：{analysis['satisfaction']:.1f}分")
        print(f"   平均质量：{analysis['quality']:.1f}分")
        print(f"   调整率：{analysis['adjustment_rate']:.0f}%")
        print(f"   常见问题：{', '.join(analysis['common_issues']) if analysis['common_issues'] else '无'}")
        
        print(f"\n🧬 进化策略：{analysis['strategy']}")
        
        if analysis['strategy'] == 'MERGE':
            new_version = self._increment_version('minor')
            print(f"   合并优化，版本号更新为：{new_version}")
            
            self._update_version_in_skill(new_version)
            self._add_iteration_count()
            self._update_feedback_analysis(analysis)
            
            print(f"   ✅ 进化完成！")
            
        elif analysis['strategy'] == 'ADD':
            new_version = self._increment_version('patch')
            print(f"   添加新能力，版本号更新为：{new_version}")
            
            self._update_version_in_skill(new_version)
            self._add_iteration_count()
            self._update_feedback_analysis(analysis)
            
            print(f"   ✅ 进化完成！")
            
        elif analysis['strategy'] == 'DISCARD':
            print(f"   ⚠️  Skill需要重构，请人工审查")
            print(f"   建议操作：")
            print(f"   1. 分析常见问题：{', '.join(analysis['common_issues'])}")
            print(f"   2. 重新设计Skill架构")
            print(f"   3. 重置版本号为v1.0.0")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Skill进化系统')
    parser.add_argument('--skill', required=True, help='Skill文件路径')
    parser.add_argument('--add-feedback', action='store_true', help='添加反馈')
    parser.add_argument('--evolve', action='store_true', help='执行进化')
    
    args = parser.parse_args()
    
    evolution = SkillEvolution(args.skill)
    
    if args.add_feedback:
        print("\n📝 添加用户反馈")
        print("=" * 50)
        
        user = input("用户：")
        function = input("功能描述：")
        satisfaction = int(input("满意度 (1-5)："))
        quality = int(input("质量 (1-5)："))
        needs_adjustment = input("是否需要调整 (y/n)：").lower() == 'y'
        suggestions = input("调整建议：")
        
        feedback = {
            'user': user,
            'function': function,
            'satisfaction': satisfaction,
            'quality': quality,
            'needs_adjustment': needs_adjustment,
            'suggestions': suggestions
        }
        
        evolution.add_feedback(feedback)
        
    if args.evolve:
        print("\n🧬 执行Skill进化")
        print("=" * 50)
        evolution.evolve()


if __name__ == '__main__':
    main()
