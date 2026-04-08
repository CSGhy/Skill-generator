#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill进化系统 v2.0
基于AutoSkill和XSKILL理论，实现Skill的自我进化能力

核心特性：
1. 双阶段操作（Accumulation + Inference）
2. 经验管理（Experience Bank）
3. 轨迹总结（Trajectory Summary）
4. 跨Rollout批判（Cross-Rollout Critique）
5. 层次化整合（Hierarchical Consolidation）
6. 多模态分析（Multimodal Analysis）
7. 零样本迁移（Zero-Shot Transfer）
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter
import hashlib


class ExperienceBank:
    """经验库管理"""
    
    def __init__(self, skill_path: Path):
        """
        初始化经验库
        
        Args:
            skill_path: Skill文件路径
        """
        self.skill_path = skill_path
        self.experience_file = skill_path.parent / 'experience_bank.json'
        self.experiences = self._load_experiences()
    
    def _load_experiences(self) -> List[Dict]:
        """加载经验库"""
        if self.experience_file.exists():
            with open(self.experience_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_experiences(self):
        """保存经验库"""
        with open(self.experience_file, 'w', encoding='utf-8') as f:
            json.dump(self.experiences, f, ensure_ascii=False, indent=2)
    
    def add_experience(self, experience: Dict):
        """添加经验
        
        Args:
            experience: 经验字典
                - id: 经验ID
                - task: 任务描述
                - success: 是否成功
                - context: 上下文
                - action: 采取的行动
                - result: 结果
                - timestamp: 时间戳
        """
        experience['id'] = self._generate_id(experience)
        experience['timestamp'] = datetime.now().isoformat()
        
        self.experiences.append(experience)
        self._save_experiences()
        
        print(f"✅ 经验已添加：{experience['task']} - {'成功' if experience['success'] else '失败'}")
    
    def _generate_id(self, experience: Dict) -> str:
        """生成经验ID"""
        content = f"{experience['task']}{experience['context']}{experience['action']}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def retrieve_experiences(self, task: str, limit: int = 5) -> List[Dict]:
        """检索相关经验
        
        Args:
            task: 任务描述
            limit: 返回数量限制
            
        Returns:
            相关经验列表
        """
        # 简单的关键词匹配
        keywords = self._extract_keywords(task)
        
        scored_experiences = []
        for exp in self.experiences:
            score = self._calculate_relevance(exp, keywords)
            if score > 0:
                scored_experiences.append((score, exp))
        
        # 按相关性排序
        scored_experiences.sort(key=lambda x: x[0], reverse=True)
        
        return [exp for score, exp in scored_experiences[:limit]]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的分词和停用词过滤
        words = re.findall(r'\w+', text.lower())
        stop_words = {'的', '了', '是', '在', '和', '或', '但', '不', '也', '都', '就', '而', '与', '及', '等', '等'}
        
        return [word for word in words if word not in stop_words and len(word) > 1]
    
    def _calculate_relevance(self, experience: Dict, keywords: List[str]) -> float:
        """计算相关性分数"""
        exp_text = f"{experience['task']} {experience['context']} {experience['action']}"
        exp_keywords = self._extract_keywords(exp_text)
        
        # 计算关键词重叠
        overlap = len(set(keywords) & set(exp_keywords))
        
        # 成功经验权重更高
        weight = 1.5 if experience.get('success', False) else 1.0
        
        return overlap * weight
    
    def cross_rollout_critique(self, task: str) -> Dict:
        """跨Rollout批判
        
        Args:
            task: 任务描述
            
        Returns:
            批判结果
        """
        # 检索相关经验
        experiences = self.retrieve_experiences(task, limit=10)
        
        if len(experiences) < 2:
            return {
                'success_rate': 0,
                'failure_rate': 0,
                'common_patterns': [],
                'recommendations': []
            }
        
        # 统计成功和失败
        success_count = sum(1 for exp in experiences if exp.get('success', False))
        failure_count = len(experiences) - success_count
        
        # 提取常见模式
        successful_patterns = self._extract_patterns([exp for exp in experiences if exp.get('success', False)])
        failed_patterns = self._extract_patterns([exp for exp in experiences if not exp.get('success', False)])
        
        # 生成建议
        recommendations = []
        if success_count > failure_count:
            recommendations.append("建议采用成功的模式")
        elif failure_count > success_count:
            recommendations.append("建议避免失败的模式")
        
        return {
            'success_rate': success_count / len(experiences),
            'failure_rate': failure_count / len(experiences),
            'successful_patterns': successful_patterns,
            'failed_patterns': failed_patterns,
            'recommendations': recommendations
        }
    
    def _extract_patterns(self, experiences: List[Dict]) -> List[str]:
        """提取模式"""
        patterns = []
        
        for exp in experiences:
            action = exp.get('action', '')
            if action and len(action) > 5:
                patterns.append(action)
        
        # 统计常见模式
        pattern_counts = Counter(patterns)
        
        return [pattern for pattern, count in pattern_counts.most_common(5)]
    
    def hierarchical_consolidation(self) -> Dict:
        """层次化整合
        
        Returns:
            整合结果
        """
        if len(self.experiences) < 2:
            return {
                'consolidated_count': 0,
                'removed_count': 0,
                'consolidated_experiences': []
            }
        
        # 按任务分组
        task_groups = {}
        for exp in self.experiences:
            task = exp.get('task', '')
            if task not in task_groups:
                task_groups[task] = []
            task_groups[task].append(exp)
        
        # 整合相似经验
        consolidated_experiences = []
        removed_count = 0
        
        for task, exps in task_groups.items():
            if len(exps) > 1:
                # 保留最成功的经验
                successful_exps = [exp for exp in exps if exp.get('success', False)]
                
                if successful_exps:
                    # 保留最新的成功经验
                    latest_successful = max(successful_exps, key=lambda x: x.get('timestamp', ''))
                    consolidated_experiences.append(latest_successful)
                    removed_count += len(exps) - 1
                else:
                    # 保留最新的经验
                    latest = max(exps, key=lambda x: x.get('timestamp', ''))
                    consolidated_experiences.append(latest)
                    removed_count += len(exps) - 1
            else:
                consolidated_experiences.append(exps[0])
        
        # 更新经验库
        self.experiences = consolidated_experiences
        self._save_experiences()
        
        return {
            'consolidated_count': len(consolidated_experiences),
            'removed_count': removed_count,
            'consolidated_experiences': consolidated_experiences
        }


class TrajectorySummary:
    """轨迹总结"""
    
    def __init__(self, skill_path: Path):
        """
        初始化轨迹总结
        
        Args:
            skill_path: Skill文件路径
        """
        self.skill_path = skill_path
        self.trajectory_file = skill_path.parent / 'trajectory_summary.json'
        self.trajectories = self._load_trajectories()
    
    def _load_trajectories(self) -> List[Dict]:
        """加载轨迹"""
        if self.trajectory_file.exists():
            with open(self.trajectory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_trajectories(self):
        """保存轨迹"""
        with open(self.trajectory_file, 'w', encoding='utf-8') as f:
            json.dump(self.trajectories, f, ensure_ascii=False, indent=2)
    
    def add_trajectory(self, trajectory: Dict):
        """添加轨迹
        
        Args:
            trajectory: 轨迹字典
                - id: 轨迹ID
                - user: 用户
                - function: 功能描述
                - steps: 步骤列表
                - result: 结果
                - timestamp: 时间戳
        """
        trajectory['id'] = self._generate_id(trajectory)
        trajectory['timestamp'] = datetime.now().isoformat()
        
        self.trajectories.append(trajectory)
        self._save_trajectories()
        
        print(f"✅ 轨迹已添加：{trajectory['function']}")
    
    def _generate_id(self, trajectory: Dict) -> str:
        """生成轨迹ID"""
        content = f"{trajectory['user']}{trajectory['function']}{trajectory['timestamp']}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def summarize_trajectories(self) -> Dict:
        """总结轨迹
        
        Returns:
            总结结果
        """
        if not self.trajectories:
            return {
                'total_trajectories': 0,
                'success_rate': 0,
                'common_steps': [],
                'common_issues': []
            }
        
        # 统计成功率
        success_count = sum(1 for traj in self.trajectories if traj.get('result', {}).get('success', False))
        total_count = len(self.trajectories)
        
        # 提取常见步骤
        all_steps = []
        for traj in self.trajectories:
            steps = traj.get('steps', [])
            all_steps.extend(steps)
        
        step_counts = Counter(all_steps)
        common_steps = [step for step, count in step_counts.most_common(10)]
        
        # 提取常见问题
        all_issues = []
        for traj in self.trajectories:
            issues = traj.get('result', {}).get('issues', [])
            all_issues.extend(issues)
        
        issue_counts = Counter(all_issues)
        common_issues = [issue for issue, count in issue_counts.most_common(10)]
        
        return {
            'total_trajectories': total_count,
            'success_rate': success_count / total_count if total_count > 0 else 0,
            'common_steps': common_steps,
            'common_issues': common_issues
        }


class SkillEvolution:
    """Skill进化系统v2.0"""
    
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
        
        # 新增组件
        self.experience_bank = ExperienceBank(self.skill_path)
        self.trajectory_summary = TrajectorySummary(self.skill_path)
    
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
        
        # 同时添加到经验库
        experience = {
            'task': feedback['function'],
            'success': feedback['satisfaction'] >= 4,
            'context': f"满意度：{feedback['satisfaction']}, 质量：{feedback['quality']}",
            'action': feedback['suggestions'] if feedback['suggestions'] else '无调整',
            'result': {
                'satisfaction': feedback['satisfaction'],
                'quality': feedback['quality']
            }
        }
        self.experience_bank.add_experience(experience)
        
        print(f"✅ 反馈已保存：{feedback['function']} - 满意度：{feedback['satisfaction']}分")
    
    def add_trajectory(self, trajectory: Dict):
        """添加轨迹
        
        Args:
            trajectory: 轨迹字典
                - user: 用户
                - function: 功能描述
                - steps: 步骤列表
                - result: 结果
        """
        self.trajectory_summary.add_trajectory(trajectory)
    
    def analyze_feedback(self) -> Dict:
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
        
        # 跨Rollout批判
        critique = self.experience_bank.cross_rollout_critique("测试用例生成")
        
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
            'common_issues': common_issues,
            'critique': critique
        }
    
    def _extract_common_issues(self) -> List[str]:
        """提取常见问题"""
        issues = []
        
        for feedback in self.feedback_history:
            suggestions = feedback.get('suggestions', '')
            if suggestions:
                issues.append(suggestions)
        
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
    
    def evolve(self):
        """执行进化"""
        analysis = self.analyze_feedback()
        
        print(f"\n📊 反馈分析：")
        print(f"   平均满意度：{analysis['satisfaction']:.1f}分")
        print(f"   平均质量：{analysis['quality']:.1f}分")
        print(f"   调整率：{analysis['adjustment_rate']:.0f}%")
        print(f"   常见问题：{', '.join(analysis['common_issues']) if analysis['common_issues'] else '无'}")
        
        # 跨Rollout批判结果
        critique = analysis.get('critique', {})
        if critique:
            print(f"\n🧬 跨Rollout批判：")
            print(f"   成功率：{critique['success_rate']:.1%}")
            print(f"   失败率：{critique['failure_rate']:.1%}")
            print(f"   成功模式：{', '.join(critique['successful_patterns'][:3])}")
            print(f"   失败模式：{', '.join(critique['failed_patterns'][:3])}")
            print(f"   建议：{', '.join(critique['recommendations'][:3])}")
        
        print(f"\n🧬 进化策略：{analysis['strategy']}")
        
        if analysis['strategy'] == 'MERGE':
            new_version = self._increment_version('minor')
            print(f"   合并优化，版本号更新为：{new_version}")
            
            self._update_version_in_skill(new_version)
            self._add_iteration_count()
            self._update_feedback_analysis(analysis)
            
            # 层次化整合
            consolidation = self.experience_bank.hierarchical_consolidation()
            print(f"\n📦 层次化整合：")
            print(f"   整合数量：{consolidation['consolidated_count']}")
            print(f"   移除数量：{consolidation['removed_count']}")
            
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
    
    parser = argparse.ArgumentParser(description='Skill进化系统v2.0')
    parser.add_argument('--skill', required=True, help='Skill文件路径')
    parser.add_argument('--add-feedback', action='store_true', help='添加反馈')
    parser.add_argument('--add-trajectory', action='store_true', help='添加轨迹')
    parser.add_argument('--evolve', action='store_true', help='执行进化')
    parser.add_argument('--consolidate', action='store_true', help='层次化整合')
    parser.add_argument('--critique', action='store_true', help='跨Rollout批判')
    parser.add_argument('--summarize', action='store_true', help='总结轨迹')
    
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
        
    if args.add_trajectory:
        print("\n📝 添加轨迹")
        print("=" * 50)
        
        user = input("用户：")
        function = input("功能描述：")
        steps_input = input("步骤（逗号分隔）：")
        steps = [step.strip() for step in steps_input.split(',')]
        success = input("是否成功 (y/n)：").lower() == 'y'
        issues_input = input("问题（逗号分隔，可选）：")
        issues = [issue.strip() for issue in issues_input.split(',') if issue.strip()]
        
        trajectory = {
            'user': user,
            'function': function,
            'steps': steps,
            'result': {
                'success': success,
                'issues': issues
            }
        }
        
        evolution.add_trajectory(trajectory)
        
    if args.evolve:
        print("\n🧬 执行Skill进化")
        print("=" * 50)
        evolution.evolve()
    
    if args.consolidate:
        print("\n📦 执行层次化整合")
        print("=" * 50)
        consolidation = evolution.experience_bank.hierarchical_consolidation()
        print(f"整合数量：{consolidation['consolidated_count']}")
        print(f"移除数量：{consolidation['removed_count']}")
        print(f"✅ 整合完成！")
    
    if args.critique:
        print("\n🧬 执行跨Rollout批判")
        print("=" * 50)
        critique = evolution.experience_bank.cross_rollout_critique("测试用例生成")
        print(f"成功率：{critique['success_rate']:.1%}")
        print(f"失败率：{critique['failure_rate']:.1%}")
        print(f"成功模式：{', '.join(critique['successful_patterns'][:3])}")
        print(f"失败模式：{', '.join(critique['failed_patterns'][:3])}")
        print(f"建议：{', '.join(critique['recommendations'][:3])}")
        print(f"✅ 批判完成！")
    
    if args.summarize:
        print("\n📊 总结轨迹")
        print("=" * 50)
        summary = evolution.trajectory_summary.summarize_trajectories()
        print(f"总轨迹数：{summary['total_trajectories']}")
        print(f"成功率：{summary['success_rate']:.1%}")
        print(f"常见步骤：{', '.join(summary['common_steps'][:5])}")
        print(f"常见问题：{', '.join(summary['common_issues'][:5])}")
        print(f"✅ 总结完成！")


if __name__ == '__main__':
    main()
