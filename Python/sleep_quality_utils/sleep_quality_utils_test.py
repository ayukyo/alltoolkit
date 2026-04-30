"""
Sleep Quality Utils 测试

运行: python sleep_quality_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from mod import (
    SleepStage, SleepQuality, SleepSession, SleepAnalysis,
    SleepTracker, SleepQualityError, InvalidSleepSessionError,
    calculate_sleep_quality_score,
    get_quality_level,
    calculate_sleep_debt,
    calculate_sleep_efficiency,
    suggest_optimal_sleep_time,
    analyze_sleep_patterns,
    analyze_sleep_cycles,
    generate_sleep_recommendations,
    analyze_sleep_session,
    calculate_optimal_wake_times,
    format_sleep_duration,
    get_sleep_stage_distribution,
    estimate_sleep_stages,
    calculate_sleep_onset_latency,
    get_nap_recommendation,
    calculate_ideal_nap_time,
    OPTIMAL_SLEEP_HOURS, SLEEP_CYCLE_DURATION
)


def test_sleep_session_creation():
    """测试睡眠记录创建"""
    print("测试 SleepSession 创建...")
    
    start = datetime(2026, 4, 29, 23, 0)
    end = datetime(2026, 4, 30, 7, 0)
    
    session = SleepSession(
        start_time=start,
        end_time=end,
        awakenings=1,
        awakening_duration_minutes=10,
        sleep_stages={
            SleepStage.DEEP: 90,
            SleepStage.LIGHT: 240,
            SleepStage.REM: 100
        }
    )
    
    # 验证基本属性
    assert session.total_time_in_bed == timedelta(hours=8), "在床时间应为8小时"
    assert session.total_sleep_time == timedelta(hours=8) - timedelta(minutes=10), "睡眠时间应减去醒来时间"
    
    efficiency = session.sleep_efficiency
    print(f"  睡眠效率: {efficiency:.2f}%")
    assert 0 <= efficiency <= 100, "睡眠效率应在0-100之间"
    
    print("  ✓ SleepSession 创建测试通过\n")


def test_sleep_quality_score():
    """测试睡眠质量评分"""
    print("测试睡眠质量评分...")
    
    # 创建一个理想的睡眠记录
    start = datetime(2026, 4, 29, 23, 0)
    end = datetime(2026, 4, 30, 7, 0)
    
    session = SleepSession(
        start_time=start,
        end_time=end,
        awakenings=0,
        awakening_duration_minutes=0,
        sleep_stages={
            SleepStage.DEEP: 100,  # 约18%
            SleepStage.LIGHT: 280,  # 约58%
            SleepStage.REM: 90      # 约19%
        }
    )
    
    score = calculate_sleep_quality_score(session, "adult")
    print(f"  理想睡眠评分: {score:.2f}")
    assert 70 <= score <= 100, "理想睡眠评分应在70-100之间"
    
    # 测试较差的睡眠
    poor_session = SleepSession(
        start_time=start,
        end_time=end,
        awakenings=4,
        awakening_duration_minutes=60,
        sleep_stages={
            SleepStage.DEEP: 30,
            SleepStage.LIGHT: 300,
            SleepStage.REM: 30
        }
    )
    
    poor_score = calculate_sleep_quality_score(poor_session, "adult")
    print(f"  较差睡眠评分: {poor_score:.2f}")
    assert poor_score < score, "较差睡眠评分应低于理想睡眠"
    
    print("  ✓ 睡眠质量评分测试通过\n")


def test_quality_level():
    """测试质量等级"""
    print("测试质量等级...")
    
    assert get_quality_level(95) == SleepQuality.EXCELLENT, "95分应为优秀"
    assert get_quality_level(85) == SleepQuality.GOOD, "85分应为良好"
    assert get_quality_level(75) == SleepQuality.FAIR, "75分应为一般"
    assert get_quality_level(65) == SleepQuality.POOR, "65分应为较差"
    assert get_quality_level(50) == SleepQuality.VERY_POOR, "50分应为很差"
    
    print("  ✓ 质量等级测试通过\n")


def test_sleep_debt():
    """测试睡眠债务计算"""
    print("测试睡眠债务计算...")
    
    sessions = []
    base_date = datetime(2026, 4, 23, 23, 0)
    
    # 创建7天的睡眠记录，每天睡7小时（欠1小时）
    for i in range(7):
        start = base_date + timedelta(days=i)
        end = start + timedelta(hours=7)
        sessions.append(SleepSession(start_time=start, end_time=end))
    
    debt = calculate_sleep_debt(sessions, target_hours=8.0, days=7)
    print(f"  7天睡眠债务: {debt:.2f} 小时")
    assert debt > 0, "应有睡眠债务"
    
    # 测试睡眠盈余
    good_sessions = []
    for i in range(7):
        start = base_date + timedelta(days=i)
        end = start + timedelta(hours=9)
        good_sessions.append(SleepSession(start_time=start, end_time=end))
    
    surplus = calculate_sleep_debt(good_sessions, target_hours=8.0, days=7)
    print(f"  7天睡眠盈余: {-surplus:.2f} 小时")
    assert surplus < 0, "应有睡眠盈余"
    
    print("  ✓ 睡眠债务计算测试通过\n")


def test_sleep_efficiency():
    """测试睡眠效率计算"""
    print("测试睡眠效率计算...")
    
    start = datetime(2026, 4, 29, 23, 0)
    end = datetime(2026, 4, 30, 7, 0)
    
    # 高效率
    high_eff = SleepSession(start_time=start, end_time=end, awakenings=0)
    efficiency = calculate_sleep_efficiency(high_eff)
    print(f"  高效率睡眠: {efficiency:.2f}%")
    assert efficiency == 100.0, "无醒来的睡眠效率应为100%"
    
    # 低效率
    low_eff = SleepSession(
        start_time=start, 
        end_time=end, 
        awakening_duration_minutes=120
    )
    efficiency = calculate_sleep_efficiency(low_eff)
    print(f"  低效率睡眠: {efficiency:.2f}%")
    assert efficiency == 75.0, "醒来2小时效率应为75%"
    
    print("  ✓ 睡眠效率计算测试通过\n")


def test_optimal_sleep_time():
    """测试最佳睡眠时间建议"""
    print("测试最佳睡眠时间建议...")
    
    wake_time = datetime(2026, 4, 30, 7, 0)
    bedtime, suggested_wake = suggest_optimal_sleep_time(wake_time, num_cycles=5)
    
    print(f"  目标醒来时间: {wake_time.strftime('%H:%M')}")
    print(f"  建议入睡时间: {bedtime.strftime('%H:%M')}")
    
    # 应该约7.5小时前（5个周期 + 15分钟入睡）
    expected_bedtime = wake_time - timedelta(minutes=5*90+15)
    assert abs((bedtime - expected_bedtime).total_seconds()) < 60, "入睡时间计算应正确"
    
    print("  ✓ 最佳睡眠时间建议测试通过\n")


def test_sleep_patterns():
    """测试睡眠模式分析"""
    print("测试睡眠模式分析...")
    
    sessions = []
    base_date = datetime(2026, 4, 23, 23, 0)
    
    for i in range(7):
        start = base_date + timedelta(days=i, hours=i*0.2)  # 稍微不同的入睡时间
        end = start + timedelta(hours=7.5)
        sessions.append(SleepSession(
            start_time=start, 
            end_time=end,
            sleep_stages={
                SleepStage.DEEP: 80,
                SleepStage.LIGHT: 260,
                SleepStage.REM: 90
            }
        ))
    
    patterns = analyze_sleep_patterns(sessions)
    
    print(f"  平均睡眠时长: {patterns['average_sleep_hours']} 小时")
    print(f"  平均效率: {patterns['average_efficiency']}%")
    print(f"  平均质量分: {patterns['average_quality_score']}")
    print(f"  平均入睡时间: {patterns['average_bedtime']}")
    print(f"  平均醒来时间: {patterns['average_wake_time']}")
    print(f"  一致性评分: {patterns['consistency_score']}")
    
    assert "average_sleep_hours" in patterns
    assert patterns["average_sleep_hours"] > 0
    
    print("  ✓ 睡眠模式分析测试通过\n")


def test_sleep_cycles():
    """测试睡眠周期分析"""
    print("测试睡眠周期分析...")
    
    # 测试8小时睡眠
    analysis = analyze_sleep_cycles(8.0)
    print(f"  8小时睡眠周期数: {analysis['complete_cycles']}")
    print(f"  剩余时间: {analysis['remaining_minutes']} 分钟")
    print(f"  估算深睡眠: {analysis['estimated_deep_minutes']} 分钟")
    print(f"  估算REM: {analysis['estimated_rem_minutes']} 分钟")
    
    assert analysis['complete_cycles'] == 5, "8小时应约5个完整周期"
    assert analysis['cycle_quality'] == "optimal"
    
    # 测试6小时睡眠
    short_analysis = analyze_sleep_cycles(6.0)
    print(f"  6小时睡眠周期数: {short_analysis['complete_cycles']}")
    
    print("  ✓ 睡眠周期分析测试通过\n")


def test_sleep_recommendations():
    """测试睡眠建议生成"""
    print("测试睡眠建议生成...")
    
    # 创建一个需要改进的睡眠分析
    analysis = SleepAnalysis(
        quality_score=55,
        quality_level=SleepQuality.VERY_POOR,
        efficiency=70.0,
        total_sleep_hours=5.5,
        deep_sleep_percentage=8.0,
        rem_sleep_percentage=15.0,
        sleep_debt_hours=8.0,
        recommendations=[],
        optimal_bedtime=None,
        optimal_wake_time=None
    )
    
    recommendations = generate_sleep_recommendations(analysis, "adult")
    
    print(f"  生成 {len(recommendations)} 条建议:")
    for i, rec in enumerate(recommendations, 1):
        print(f"    {i}. {rec[:50]}...")
    
    assert len(recommendations) > 0, "应生成建议"
    
    print("  ✓ 睡眠建议生成测试通过\n")


def test_analyze_sleep_session():
    """测试综合睡眠分析"""
    print("测试综合睡眠分析...")
    
    start = datetime(2026, 4, 29, 23, 0)
    end = datetime(2026, 4, 30, 7, 0)
    
    session = SleepSession(
        start_time=start,
        end_time=end,
        awakenings=1,
        awakening_duration_minutes=15,
        sleep_stages={
            SleepStage.DEEP: 90,
            SleepStage.LIGHT: 250,
            SleepStage.REM: 85
        }
    )
    
    analysis = analyze_sleep_session(session, "adult", 8.0)
    
    print(f"  质量评分: {analysis.quality_score:.2f}")
    print(f"  质量等级: {analysis.quality_level.value}")
    print(f"  睡眠效率: {analysis.efficiency:.2f}%")
    print(f"  睡眠时长: {analysis.total_sleep_hours:.2f} 小时")
    print(f"  深睡眠占比: {analysis.deep_sleep_percentage:.2f}%")
    print(f"  REM占比: {analysis.rem_sleep_percentage:.2f}%")
    print(f"  睡眠债务: {analysis.sleep_debt_hours:.2f} 小时")
    
    assert analysis.quality_score >= 0
    assert analysis.quality_level in SleepQuality
    
    print("  ✓ 综合睡眠分析测试通过\n")


def test_optimal_wake_times():
    """测试最佳醒来时间计算"""
    print("测试最佳醒来时间计算...")
    
    bedtime = datetime(2026, 4, 29, 23, 0)
    wake_times = calculate_optimal_wake_times(bedtime, min_cycles=4, max_cycles=6)
    
    print(f"  入睡时间: {bedtime.strftime('%H:%M')}")
    print("  建议醒来时间:")
    for wake_time, cycles in wake_times:
        print(f"    {wake_time.strftime('%H:%M')} ({cycles}个周期)")
    
    assert len(wake_times) == 3, "应有3个建议时间"
    
    print("  ✓ 最佳醒来时间计算测试通过\n")


def test_format_sleep_duration():
    """测试睡眠时长格式化"""
    print("测试睡眠时长格式化...")
    
    duration1 = timedelta(hours=7, minutes=30)
    assert format_sleep_duration(duration1) == "7小时30分钟"
    
    duration2 = timedelta(hours=8)
    assert format_sleep_duration(duration2) == "8小时"
    
    duration3 = timedelta(minutes=45)
    assert format_sleep_duration(duration3) == "45分钟"
    
    print("  ✓ 睡眠时长格式化测试通过\n")


def test_sleep_stage_distribution():
    """测试睡眠阶段分布"""
    print("测试睡眠阶段分布...")
    
    start = datetime(2026, 4, 29, 23, 0)
    end = datetime(2026, 4, 30, 7, 0)
    
    session = SleepSession(
        start_time=start,
        end_time=end,
        awakening_duration_minutes=10,
        sleep_stages={
            SleepStage.DEEP: 90,
            SleepStage.LIGHT: 280,
            SleepStage.REM: 100
        }
    )
    
    distribution = get_sleep_stage_distribution(session)
    
    print(f"  深睡眠: {distribution['deep']}%")
    print(f"  浅睡眠: {distribution['light']}%")
    print(f"  REM: {distribution['rem']}%")
    print(f"  清醒: {distribution['awake']}%")
    
    total = distribution['deep'] + distribution['light'] + distribution['rem']
    assert abs(total - 100) < 1, "各阶段占比总和应接近100%"
    
    print("  ✓ 睡眠阶段分布测试通过\n")


def test_sleep_tracker():
    """测试睡眠追踪器"""
    print("测试睡眠追踪器...")
    
    tracker = SleepTracker(target_hours=8.0, age_group="adult")
    
    # 添加7天记录
    base_date = datetime(2026, 4, 23, 23, 0)
    for i in range(7):
        start = base_date + timedelta(days=i)
        end = start + timedelta(hours=7.5)
        tracker.add_session(SleepSession(
            start_time=start,
            end_time=end,
            sleep_stages={
                SleepStage.DEEP: 80,
                SleepStage.LIGHT: 260,
                SleepStage.REM: 90
            }
        ))
    
    print(f"  记录天数: {len(tracker.sessions)}")
    print(f"  睡眠债务: {tracker.get_sleep_debt(7):.2f} 小时")
    print(f"  平均质量: {tracker.get_average_quality(7):.2f}")
    print(f"  趋势: {tracker.get_trend(7)}")
    
    weekly = tracker.get_weekly_report()
    print(f"  周平均时长: {weekly['average_sleep_hours']} 小时")
    
    print("  ✓ 睡眠追踪器测试通过\n")


def test_estimate_sleep_stages():
    """测试睡眠阶段估算"""
    print("测试睡眠阶段估算...")
    
    # 8小时睡眠
    stages = estimate_sleep_stages(480, age=30)
    
    print(f"  30岁，8小时睡眠:")
    print(f"    深睡眠: {stages[SleepStage.DEEP]} 分钟")
    print(f"    浅睡眠: {stages[SleepStage.LIGHT]} 分钟")
    print(f"    REM: {stages[SleepStage.REM]} 分钟")
    
    total = stages[SleepStage.DEEP] + stages[SleepStage.LIGHT] + stages[SleepStage.REM]
    assert total == 480, "各阶段时长总和应等于总睡眠时间"
    
    # 测试年龄影响
    young_stages = estimate_sleep_stages(480, age=15)
    old_stages = estimate_sleep_stages(480, age=70)
    
    print(f"  15岁深睡眠: {young_stages[SleepStage.DEEP]} 分钟")
    print(f"  70岁深睡眠: {old_stages[SleepStage.DEEP]} 分钟")
    
    assert young_stages[SleepStage.DEEP] > old_stages[SleepStage.DEEP], \
        "年轻人深睡眠应多于老年人"
    
    print("  ✓ 睡眠阶段估算测试通过\n")


def test_nap_functions():
    """测试小睡相关功能"""
    print("测试小睡功能...")
    
    # 入睡潜伏期
    print("  入睡潜伏期评估:")
    print(f"    10分钟: {calculate_sleep_onset_latency(10/60)}")
    print(f"    25分钟: {calculate_sleep_onset_latency(25/60)}")
    print(f"    45分钟: {calculate_sleep_onset_latency(45/60)}")
    print(f"    70分钟: {calculate_sleep_onset_latency(70/60)}")
    
    # 小睡建议
    print("\n  小睡建议:")
    print(f"    15分钟: {get_nap_recommendation(15)}")
    print(f"    25分钟: {get_nap_recommendation(25)}")
    print(f"    45分钟: {get_nap_recommendation(45)}")
    print(f"    90分钟: {get_nap_recommendation(90)}")
    
    # 理想小睡时长
    print("\n  理想小睡时长:")
    duration, reason = calculate_ideal_nap_time(7.0, 1.0)
    print(f"    睡眠充足: {duration}分钟 - {reason}")
    
    duration, reason = calculate_ideal_nap_time(6.0, 3.0)
    print(f"    睡眠不足: {duration}分钟 - {reason}")
    
    print("  ✓ 小睡功能测试通过\n")


def test_invalid_session():
    """测试无效睡眠记录"""
    print("测试无效睡眠记录...")
    
    start = datetime(2026, 4, 30, 7, 0)
    end = datetime(2026, 4, 29, 23, 0)  # 结束时间早于开始时间
    
    try:
        tracker = SleepTracker()
        tracker.add_session(SleepSession(start_time=start, end_time=end))
        assert False, "应抛出异常"
    except InvalidSleepSessionError as e:
        print(f"  正确捕获异常: {e}")
    
    print("  ✓ 无效睡眠记录测试通过\n")


def test_constants():
    """测试常量定义"""
    print("测试常量定义...")
    
    print(f"  各年龄组最佳睡眠时长:")
    for group, (min_h, max_h) in OPTIMAL_SLEEP_HOURS.items():
        print(f"    {group}: {min_h}-{max_h} 小时")
    
    print(f"  睡眠周期时长: {SLEEP_CYCLE_DURATION} 分钟")
    
    assert SLEEP_CYCLE_DURATION == 90, "睡眠周期应为90分钟"
    
    print("  ✓ 常量定义测试通过\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Sleep Quality Utils 测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        test_sleep_session_creation,
        test_sleep_quality_score,
        test_quality_level,
        test_sleep_debt,
        test_sleep_efficiency,
        test_optimal_sleep_time,
        test_sleep_patterns,
        test_sleep_cycles,
        test_sleep_recommendations,
        test_analyze_sleep_session,
        test_optimal_wake_times,
        test_format_sleep_duration,
        test_sleep_stage_distribution,
        test_sleep_tracker,
        test_estimate_sleep_stages,
        test_nap_functions,
        test_invalid_session,
        test_constants,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败: {test.__name__}")
            print(f"    错误: {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)