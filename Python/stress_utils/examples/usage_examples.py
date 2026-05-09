#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Stress Utilities Usage Examples
==============================================
Practical examples demonstrating the stress_utils module capabilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stress_utils.mod import (
    calculate_stress_index,
    get_stress_level,
    get_stress_level_info,
    get_relief_recommendations,
    get_dominant_stress_factors,
    perform_full_assessment,
    calculate_burnout_risk_simple,
    calculate_pss_score,
    interpret_pss_score,
    perform_pss_test,
    quick_stress_check,
    analyze_quick_check_breakdown,
    StressHistory,
    analyze_stress_trend,
    assess_burnout,
    suggest_relief_activities,
    get_stress_summary,
    calculate_stress_reduction_potential,
    get_pss_questions,
    format_assessment_report,
    StressLevel,
    StressType,
)


def example_basic_stress_calculation():
    """示例1: 基础压力指数计算"""
    print("\n" + "=" * 60)
    print("示例1: 基础压力指数计算")
    print("=" * 60)
    
    # 计算综合压力指数
    stress_index = calculate_stress_index(
        work_score=65,       # 工作压力 65分
        life_score=40,       # 生活压力 40分
        health_score=35,     # 健康压力 35分
        psychological_score=55,  # 心理压力 55分
        environment_score=25     # 环境压力 25分
    )
    
    print(f"\n压力指数: {stress_index}")
    print(f"压力等级: {get_stress_level(stress_index)}")
    
    # 获取详细信息
    level, label, label_en, desc, action = get_stress_level_info(stress_index)
    print(f"等级标签: {label} ({label_en})")
    print(f"状态描述: {desc}")
    print(f"推荐行动: {action}")
    
    # 获取主要压力因素
    dominant = get_dominant_stress_factors(65, 40, 35, 55, 25)
    print(f"主要压力来源: {', '.join(dominant)}")


def example_full_assessment():
    """示例2: 完整压力评估"""
    print("\n" + "=" * 60)
    print("示例2: 完整压力评估")
    print("=" * 60)
    
    # 执行完整评估
    result = perform_full_assessment(
        work_score=70,
        life_score=50,
        health_score=40,
        psychological_score=60,
        environment_score=30,
        notes="周五下班前评估"
    )
    
    # 打印格式化报告
    print(format_assessment_report(result))
    
    # 访问详细数据
    print("\n详细因素分析:")
    for factor, score in result.factor_breakdown.items():
        print(f"  {factor}: {score}分")
    
    print(f"\n燃尽风险: {result.burnout_risk:.0%}")


def example_custom_weights():
    """示例3: 自定义权重计算"""
    print("\n" + "=" * 60)
    print("示例3: 自定义权重计算")
    print("=" * 60)
    
    # 默认权重计算
    default_index = calculate_stress_index(80, 20, 20, 30, 20)
    print(f"默认权重压力指数: {default_index}")
    
    # 强调工作压力的权重
    work_focus_weights = {
        'work': 0.50,
        'life': 0.15,
        'health': 0.10,
        'psychological': 0.20,
        'environment': 0.05,
    }
    work_index = calculate_stress_index(80, 20, 20, 30, 20, work_focus_weights)
    print(f"强调工作压力权重: {work_index}")
    
    # 强调心理健康的权重
    mental_focus_weights = {
        'work': 0.15,
        'life': 0.20,
        'health': 0.20,
        'psychological': 0.40,
        'environment': 0.05,
    }
    mental_index = calculate_stress_index(80, 20, 20, 30, 20, mental_focus_weights)
    print(f"强调心理健康权重: {mental_index}")


def example_quick_stress_check():
    """示例4: 快速压力检查"""
    print("\n" + "=" * 60)
    print("示例4: 快速压力检查 (5分钟自评)")
    print("=" * 60)
    
    # 快速检查 (1-10分评分)
    quick_index = quick_stress_check(
        sleep_quality=6,     # 睡眠质量 6/10
        energy_level=5,      # 精力水平 5/10
        mood_rating=4,       # 心情评分 4/10
        workload_feeling=7,  # 工作负担 7/10 (越高负担越重)
        social_connection=5  # 社交连接 5/10
    )
    
    print(f"\n快速压力指数: {quick_index}")
    print(get_stress_summary(quick_index))
    
    # 分析各项贡献
    breakdown = analyze_quick_check_breakdown(6, 5, 4, 7, 5)
    print("\n各项压力贡献:")
    for factor, score in breakdown.items():
        print(f"  {factor}: {score}分")
    
    # 根据结果获取建议
    level = get_stress_level(quick_index)
    recommendations = get_relief_recommendations(level)
    print("\n建议采取的措施:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec}")


def example_pss_test():
    """示例5: PSS-10 感知压力量表测试"""
    print("\n" + "=" * 60)
    print("示例5: PSS-10 感知压力量表测试")
    print("=" * 60)
    
    # 显示问题列表
    print("\nPSS-10 问题列表:")
    questions = get_pss_questions()
    for i, (q_id, q_text) in enumerate(questions, 1):
        print(f"  {i}. {q_text}")
    
    # 模拟用户响应 (0=从不, 1=几乎不, 2=有时, 3=经常, 4=总是)
    responses = {
        'q1': 3,  # 因意外事件不安: 经常
        'q2': 2,  # 无法控制重要事情: 有时
        'q3': 3,  # 感到紧张和压力: 经常
        'q4': 2,  # 成功处理烦恼: 有时 (反向计分)
        'q5': 1,  # 事情按意愿发展: 几乎不 (反向计分)
        'q6': 3,  # 无法应对必须做的事: 经常
        'q7': 2,  # 能控制烦恼: 有时 (反向计分)
        'q8': 2,  # 事情堆积如山: 有时
        'q9': 2,  # 因无法控制而生气: 有时
        'q10': 2, # 困难堆积如山: 有时
    }
    
    # 执行测试
    result = perform_pss_test(responses)
    
    print(f"\nPSS 总分: {result.total_score} / 40")
    print(f"压力等级: {result.stress_level}")
    print(f"百分位估计: {result.percentile}%")
    print(f"\n结果解释: {result.interpretation}")
    
    print("\n分类分解:")
    print(f"  正向问题得分: {result.category_breakdown['positive_items']}")
    print(f"  反向问题得分: {result.category_breakdown['negative_items']}")


def example_stress_history():
    """示例6: 压力历史追踪"""
    print("\n" + "=" * 60)
    print("示例6: 压力历史追踪与趋势分析")
    print("=" * 60)
    
    # 创建历史记录
    history = StressHistory()
    
    # 添加一周的压力记录 (模拟)
    week_data = [
        (45, "周一", ["工作任务"]),
        (55, "周二", ["会议压力"]),
        (50, "周三", ["项目截止"]),
        (60, "周四", ["加班"]),
        (65, "周五", ["周报"]),
        (35, "周六", ["休息"]),
        (30, "周日", ["休息"]),
    ]
    
    for index, day, triggers in week_data:
        history.add_entry(index, notes=day, triggers=triggers)
    
    print("\n一周压力记录:")
    entries = history.get_entries()
    for entry in entries:
        print(f"  {entry.notes}: {entry.stress_index} - {entry.level}")
        if entry.triggers:
            print(f"    触发因素: {', '.join(entry.triggers)}")
    
    # 分析趋势
    trend = analyze_stress_trend(history)
    
    print("\n趋势分析:")
    print(f"  当前压力: {trend.current_index}")
    print(f"  平均压力: {trend.average_index}")
    print(f"  趋势方向: {trend.trend_direction}")
    if trend.trend_percentage > 0:
        print(f"  变化幅度: {trend.trend_percentage}%")
    print(f"  最高压力: {trend.peak_index}")
    print(f"  最低压力: {trend.lowest_index}")
    print(f"  波动性: {trend.volatility}")
    
    # 导出历史
    print("\n导出历史记录 (JSON):")
    json_data = history.to_json()
    print(json_data[:200] + "...")


def example_burnout_assessment():
    """示例7: 燃尽风险评估"""
    print("\n" + "=" * 60)
    print("示例7: 燃尽风险评估")
    print("=" * 60)
    
    # 情绪耗竭问题 (0-6分)
    ee_responses = [4, 5, 4, 5, 3]  # 较高耗竭
    
    # 去人格化问题
    dp_responses = [2, 3, 2]  # 中等
    
    # 个人成就感问题
    pa_responses = [1, 2, 1, 2, 1, 2, 1]  # 较低
    
    burnout = assess_burnout(ee_responses, dp_responses, pa_responses)
    
    print("\n燃尽风险评估结果:")
    print(f"  情绪耗竭: {burnout.emotional_exhaustion_score:.0%}")
    print(f"  去人格化: {burnout.depersonalization_score:.0%}")
    print(f"  成就感降低: {burnout.reduced_accomplishment_score:.0%}")
    print(f"\n  总风险: {burnout.overall_risk:.0%}")
    print(f"  风险等级: {burnout.risk_level}")
    
    if burnout.warning_signs:
        print("\n警告信号:")
        for sign in burnout.warning_signs:
            print(f"  - {sign}")
    
    print("\n干预建议:")
    for i, intervention in enumerate(burnout.interventions, 1):
        print(f"  {i}. {intervention}")


def example_relief_activities():
    """示例8: 缓解活动建议"""
    print("\n" + "=" * 60)
    print("示例8: 个性化缓解活动建议")
    print("=" * 60)
    
    # 不同压力等级的活动建议
    levels = ['low', 'moderate', 'high']
    
    for level in levels:
        print(f"\n压力等级: {level}")
        activities = suggest_relief_activities(level, 30)
        
        for activity in activities:
            print(f"  - {activity['name']} ({activity['duration']})")
            print(f"    效果: {activity['effect']} | {activity['description']}")
    
    # 根据偏好和时间定制
    print("\n定制建议 (偏好运动，15分钟):")
    custom_activities = suggest_relief_activities('moderate', 15, ['physical'])
    for activity in custom_activities:
        print(f"  - {activity['name']} ({activity['duration']})")
    
    # 计算缓解潜力
    print("\n压力缓解潜力计算:")
    test_activities = [
        {'effect': 'high'},     # 冥想
        {'effect': 'medium'},   # 散步
        {'effect': 'low'},      # 听音乐
    ]
    reduction = calculate_stress_reduction_potential(70, test_activities)
    print(f"  当前压力: 70")
    print(f"  预估缓解: {reduction} 点")
    print(f"  预估后续压力: {70 - reduction}")


def example_summary_usage():
    """示例9: 简要用法示例"""
    print("\n" + "=" * 60)
    print("示例9: 快速用法示例")
    print("=" * 60)
    
    # 最简单的用法
    index = calculate_stress_index(50, 40, 30, 45, 25)
    print(f"1. 简单计算: {get_stress_summary(index)}")
    
    # 快速检查
    quick = quick_stress_check(7, 6, 6, 4, 7)
    print(f"2. 快速检查: {get_stress_summary(quick)}")
    
    # 获取建议
    level = get_stress_level(50)
    recs = get_relief_recommendations(level)
    print(f"3. 缓解建议: {recs[0]}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("AllToolkit - Stress Utilities 使用示例")
    print("=" * 60)
    
    example_basic_stress_calculation()
    example_full_assessment()
    example_custom_weights()
    example_quick_stress_check()
    example_pss_test()
    example_stress_history()
    example_burnout_assessment()
    example_relief_activities()
    example_summary_usage()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()