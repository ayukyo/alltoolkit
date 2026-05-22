"""
Reaction Time Utilities - 使用示例

Examples demonstrating various reaction time analysis features.
"""

from datetime import datetime, timedelta
import random

# 导入模块
from mod import (
    calculate_statistics,
    assess_performance,
    analyze_trend,
    analyze_fatigue,
    generate_reaction_test_data,
    simulate_progressive_improvement,
    compare_groups,
    assess_driving_safety,
    generate_training_plan,
    reaction_time_to_speed_category,
    format_statistics_report,
    PerformanceLevel,
    ActivityType,
    ReactionTestType,
)


def example_basic_statistics():
    """示例1：基本统计计算"""
    print("\n" + "=" * 60)
    print("示例1：基本统计计算")
    print("=" * 60)
    
    # 模拟一组反应时间数据（单位：毫秒）
    reaction_times = [180, 195, 200, 210, 220, 185, 190, 205, 215, 225]
    
    # 计算统计数据
    stats = calculate_statistics(reaction_times)
    
    # 打印结果
    print(f"\n样本数量: {stats.count}")
    print(f"平均值: {stats.mean} ms")
    print(f"中位数: {stats.median} ms")
    print(f"标准差: {stats.std} ms")
    print(f"最小值: {stats.min} ms")
    print(f"最大值: {stats.max} ms")
    print(f"变异系数: {stats.coefficient_of_variation}%")
    print(f"\n百分位数:")
    print(f"  25%: {stats.percentile_25} ms")
    print(f"  75%: {stats.percentile_75} ms")
    print(f"  90%: {stats.percentile_90} ms")
    print(f"  95%: {stats.percentile_95} ms")
    
    return stats


def example_performance_assessment():
    """示例2：表现评估"""
    print("\n" + "=" * 60)
    print("示例2：表现评估")
    print("=" * 60)
    
    # 不同水平的表现数据
    test_cases = [
        {"name": "优秀玩家", "times": [130, 140, 135, 138, 142], "age": 25},
        {"name": "平均水平", "times": [200, 205, 210, 208, 215], "age": 30},
        {"name": "需要改进", "times": [350, 360, 355, 370, 365], "age": 25},
    ]
    
    for case in test_cases:
        assessment = assess_performance(case["times"], age=case["age"])
        
        print(f"\n{case['name']} (年龄: {case['age']}岁):")
        print(f"  表现等级: {assessment.level.value}")
        print(f"  综合得分: {assessment.score}")
        print(f"  百分位排名: {assessment.percentile}%")
        print(f"  与同龄差距: {assessment.age_benchmark_diff} ms")
        print(f"  评估说明: {assessment.classification_reason}")
        
        if assessment.recommendations:
            print(f"  改进建议:")
            for rec in assessment.recommendations[:2]:
                print(f"    - {rec}")


def example_gaming_assessment():
    """示例3：游戏玩家评估"""
    print("\n" + "=" * 60)
    print("示例3：游戏玩家评估")
    print("=" * 60)
    
    # FPS 游戏玩家数据
    fps_times = [150, 155, 148, 160, 152]
    
    assessment = assess_performance(
        fps_times,
        activity_type=ActivityType.GAMING,
        specific_activity="fps"
    )
    
    print(f"\nFPS 游戏玩家评估:")
    print(f"  平均反应时间: {sum(fps_times)/len(fps_times):.1f} ms")
    print(f"  表现等级: {assessment.level.value}")
    print(f"  得分: {assessment.score}")
    
    # 不同游戏类型对比
    game_types = ["fps", "racing", "rhythm", "moba"]
    
    print(f"\n不同游戏类型基准对比:")
    for game in game_types:
        times = [180, 185, 190]
        assessment = assess_performance(
            times,
            activity_type=ActivityType.GAMING,
            specific_activity=game
        )
        print(f"  {game}: 等级 {assessment.level.value}, 得分 {assessment.score}")


def example_sports_assessment():
    """示例4：运动员评估"""
    print("\n" + "=" * 60)
    print("示例4：运动员评估")
    print("=" * 60)
    
    sports = {
        "乒乓球": ("table_tennis", [100, 105, 98, 110, 102]),
        "拳击": ("boxing", [120, 125, 118, 130, 122]),
        "网球": ("tennis", [150, 155, 148, 160, 152]),
        "足球": ("soccer", [180, 185, 178, 190, 182]),
    }
    
    for sport_name, (sport_type, times) in sports.items():
        assessment = assess_performance(
            times,
            activity_type=ActivityType.SPORTS,
            specific_activity=sport_type
        )
        
        print(f"\n{sport_name}运动员:")
        print(f"  平均反应时间: {sum(times)/len(times):.1f} ms")
        print(f"  表现等级: {assessment.level.value}")
        print(f"  速度类别: {reaction_time_to_speed_category(sum(times)/len(times))}")


def example_trend_analysis():
    """示例5：趋势分析"""
    print("\n" + "=" * 60)
    print("示例5：训练趋势分析")
    print("=" * 60)
    
    # 模拟14天训练数据
    training_data = simulate_progressive_improvement(
        days=14,
        start_mean=250,
        end_mean=180,
        daily_std=25,
        tests_per_day=5
    )
    
    # 转换为趋势分析格式
    sessions = []
    for date, times in training_data:
        mean_time = sum(times) / len(times)
        sessions.append((date, mean_time))
    
    # 分析趋势
    trend = analyze_trend(sessions)
    
    print(f"\n14天训练趋势:")
    print(f"  趋势方向: {trend.trend_direction}")
    print(f"  改善速率: {trend.improvement_rate:.2f} ms/day")
    print(f"  稳定性得分: {trend.consistency_score}")
    print(f"  预测下次: {trend.predicted_next} ms")
    print(f"  置信度: {trend.confidence_level}")
    
    # 显示每周平均
    print(f"\n每周进展:")
    for week in range(0, 14, 7):
        week_sessions = sessions[week:week+7]
        if week_sessions:
            week_mean = sum(s[1] for s in week_sessions) / len(week_sessions)
            print(f"  第{(week//7)+1}周平均: {week_mean:.1f} ms")


def example_fatigue_analysis():
    """示例6：疲劳分析"""
    print("\n" + "=" * 60)
    print("示例6：疲劳效应分析")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "正常状态",
            "baseline": [180, 185, 190],
            "current": [180, 185, 190]
        },
        {
            "name": "轻微疲劳",
            "baseline": [180, 185, 190],
            "current": [200, 205, 210]
        },
        {
            "name": "中度疲劳",
            "baseline": [180, 185, 190],
            "current": [250, 260, 270]
        },
        {
            "name": "严重疲劳",
            "baseline": [180, 185, 190],
            "current": [300, 310, 320]
        }
    ]
    
    for scenario in scenarios:
        fatigue = analyze_fatigue(scenario["baseline"], scenario["current"])
        
        print(f"\n{scenario['name']}:")
        print(f"  基线平均: {fatigue.baseline_mean} ms")
        print(f"  当前平均: {fatigue.current_mean} ms")
        print(f"  疲劳效应: {fatigue.fatigue_effect} ms")
        print(f"  疲劳程度: {fatigue.fatigue_percentage:.1f}%")
        print(f"  警示等级: {fatigue.alert_level}")
        print(f"  预估恢复: {fatigue.recovery_time_estimate:.1f} 分钟")


def example_driving_safety():
    """示例7：驾驶安全评估"""
    print("\n" + "=" * 60)
    print("示例7：驾驶安全评估")
    print("=" * 60)
    
    drivers = [
        {"name": "年轻司机", "times": [250, 260, 270], "age": 25, "scenario": "normal"},
        {"name": "中年司机", "times": [300, 310, 320], "age": 45, "scenario": "normal"},
        {"name": "夜间驾驶", "times": [350, 360, 370], "age": 30, "scenario": "night"},
        {"name": "高速场景", "times": [280, 290, 300], "age": 30, "scenario": "high_speed"},
    ]
    
    for driver in drivers:
        safety = assess_driving_safety(
            driver["times"],
            driving_scenario=driver["scenario"],
            driver_age=driver["age"]
        )
        
        print(f"\n{driver['name']} ({driver['scenario']}场景):")
        print(f"  安全等级: {safety['safety_rating']}")
        print(f"  评估: {safety['safety_message']}")
        print(f"  平均反应时间: {safety['mean_reaction_time']} ms")
        print(f"  60km/h反应距离: {safety['reaction_distance_at_60kmh']} m")
        
        if safety['recommendations']:
            print(f"  建议: {safety['recommendations'][0]}")


def example_training_plan():
    """示例8：训练计划生成"""
    print("\n" + "=" * 60)
    print("示例8：训练计划生成")
    print("=" * 60)
    
    # 为不同等级生成训练计划
    levels = [
        PerformanceLevel.SLOW,
        PerformanceLevel.BELOW_AVERAGE,
        PerformanceLevel.AVERAGE,
    ]
    
    for level in levels:
        plan = generate_training_plan(
            current_level=level,
            target_level=PerformanceLevel.GOOD,
            weeks=4
        )
        
        print(f"\n从 {level.value} 到 GOOD 的4周计划:")
        print(f"  每周训练: {plan['sessions_per_week']} 次")
        print(f"  每次时长: {plan['session_duration_minutes']} 分钟")
        print(f"  总课时: {plan['total_sessions']} 次")
        print(f"  预期改善: {plan['expected_improvement']}")


def example_group_comparison():
    """示例9：组间比较"""
    print("\n" + "=" * 60)
    print("示例9：组间比较分析")
    print("=" * 60)
    
    # 模拟两组玩家数据
    casual_players = [220, 230, 225, 235, 228, 240, 232]
    pro_players = [150, 145, 155, 148, 152, 150, 148]
    
    comparison = compare_groups(
        pro_players,
        casual_players,
        "职业玩家",
        "休闲玩家"
    )
    
    print(f"\n{comparison['group_a_name']} vs {comparison['group_b_name']}:")
    print(f"  平均差异: {abs(comparison['difference'])} ms")
    print(f"  更快组: {comparison['faster_group']}")
    print(f"  是否显著: {comparison['significant_difference']}")
    print(f"  效应量: {comparison['cohens_d']}")
    print(f"  效果解释: {comparison['effect_size_interpretation']}")


def example_simulated_training():
    """示例10：模拟训练进度"""
    print("\n" + "=" * 60)
    print("示例10：模拟训练进度")
    print("=" * 60)
    
    # 模拟30天训练
    training = simulate_progressive_improvement(
        days=30,
        start_mean=250,
        end_mean=180,
        daily_std=25,
        tests_per_day=5
    )
    
    # 计算各周统计
    weekly_stats = []
    for week in range(5):
        start_day = week * 7
        end_day = min(start_day + 7, 30)
        
        week_times = []
        for day_idx in range(start_day, end_day):
            week_times.extend(training[day_idx][1])
        
        stats = calculate_statistics(week_times)
        weekly_stats.append((week + 1, stats))
    
    print(f"\n30天训练进度（每周统计）:")
    for week, stats in weekly_stats:
        print(f"\n第{week}周:")
        print(f"  平均: {stats.mean:.1f} ms")
        print(f"  标准差: {stats.std:.1f} ms")
        print(f"  最优: {stats.min:.1f} ms")
        print(f"  最慢: {stats.max:.1f} ms")


def example_full_report():
    """示例11：完整报告"""
    print("\n" + "=" * 60)
    print("示例11：完整分析报告")
    print("=" * 60)
    
    # 生成模拟数据
    test_results = generate_reaction_test_data(25, 200, 30)
    times = [r.time_ms for r in test_results if r.correct]
    
    # 统计分析
    stats = calculate_statistics(times)
    
    # 表现评估
    assessment = assess_performance(times, age=28)
    
    # 打印完整报告
    print(format_statistics_report(stats))
    print(f"\n表现评估:")
    print(f"  等级: {assessment.level.value}")
    print(f"  得分: {assessment.score}")
    print(f"  百分位: {assessment.percentile}%")
    print(f"  说明: {assessment.classification_reason}")
    
    if assessment.recommendations:
        print(f"\n改进建议:")
        for rec in assessment.recommendations:
            print(f"  • {rec}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("反应时间工具 - 使用示例")
    print("=" * 60)
    
    example_basic_statistics()
    example_performance_assessment()
    example_gaming_assessment()
    example_sports_assessment()
    example_trend_analysis()
    example_fatigue_analysis()
    example_driving_safety()
    example_training_plan()
    example_group_comparison()
    example_simulated_training()
    example_full_report()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()