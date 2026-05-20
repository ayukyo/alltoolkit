"""
Sleep Utils 测试套件

测试覆盖：
- 睡眠周期计算
- 最佳起床/就寝时间计算
- 睡眠质量评分
- 睡眠负债计算
- 小睡建议
- 昼夜节律分析
- 睡眠效率计算
- 睡眠阶段分布
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import math

from mod import (
    calculate_wake_times, calculate_bedtimes, calculate_quality_score,
    calculate_sleep_debt, suggest_nap, analyze_circadian_rhythm,
    calculate_optimal_sleep_schedule, get_sleep_stage_distribution,
    calculate_sleep_efficiency, when_to_wake, when_to_sleep,
    SleepCycleResult, SleepQuality, CircadianRhythm,
    SLEEP_CYCLE_MINUTES, FALL_ASLEEP_MINUTES, OPTIMAL_CYCLES,
    format_duration
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望: {expected}\n  实际: {actual}")
            return False
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望: True\n  实际: False")
            return False
    
    def assert_false(self, condition, msg=""):
        if not condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望: False\n  实际: True")
            return False
    
    def assert_in_range(self, value, min_val, max_val, msg=""):
        if min_val <= value <= max_val:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望范围: [{min_val}, {max_val}]\n  实际: {value}")
            return False
    
    def assert_greater_equal(self, actual, expected, msg=""):
        if actual >= expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望 >= {expected}\n  实际: {actual}")
            return False
    
    def assert_less_equal(self, actual, expected, msg=""):
        if actual <= expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望 <= {expected}\n  实际: {actual}")
            return False
    
    def assert_raises(self, exception_type, func, msg=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望抛出异常: {exception_type.__name__}\n  实际: 无异常")
            return False
        except exception_type:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望抛出异常: {exception_type.__name__}\n  实际: {type(e).__name__}: {e}")
            return False
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n测试结果: {self.passed}/{total} 通过")
        if self.errors:
            print("\n失败的测试:")
            for error in self.errors[:10]:  # 只显示前10个错误
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个错误未显示")
        return self.failed == 0


def test_calculate_wake_times_basic(r: TestResult):
    """测试基本起床时间计算"""
    print("测试: 基本起床时间计算")
    
    bedtime = datetime(2024, 1, 1, 23, 0)  # 23:00
    results = calculate_wake_times(bedtime)
    
    # 应该返回4-6个周期
    r.assert_equal(len(results), 3, "默认返回3个选项(4-6周期)")
    
    # 检查第一个结果（质量最高的）
    first = results[0]
    r.assert_true(isinstance(first, SleepCycleResult), "返回SleepCycleResult对象")
    
    # 检查时间计算正确性
    # 23:00 + 15分钟入睡 + 4*90分钟 = 23:15 + 6小时 = 5:15
    expected_wake = bedtime + timedelta(minutes=FALL_ASLEEP_MINUTES + 4 * SLEEP_CYCLE_MINUTES)
    four_cycle_result = [r for r in results if r.cycles == 4][0]
    r.assert_equal(four_cycle_result.wake_time.hour, expected_wake.hour, "4周期起床小时正确")
    
    print("  ✓ 基本起床时间计算测试完成")


def test_calculate_wake_times_sorted_by_quality(r: TestResult):
    """测试结果按质量排序"""
    print("测试: 起床时间按质量排序")
    
    bedtime = datetime(2024, 1, 1, 23, 0)
    results = calculate_wake_times(bedtime)
    
    # 检查按质量分数降序排列
    for i in range(len(results) - 1):
        r.assert_greater_equal(
            results[i].quality_score, 
            results[i+1].quality_score,
            f"结果{i}质量 >= 结果{i+1}质量"
        )
    
    print("  ✓ 质量排序测试完成")


def test_calculate_wake_times_with_custom_fall_asleep(r: TestResult):
    """测试自定义入睡时间"""
    print("测试: 自定义入睡时间")
    
    bedtime = datetime(2024, 1, 1, 23, 0)
    custom_fall_asleep = 30  # 30分钟入睡
    results = calculate_wake_times(bedtime, fall_asleep_minutes=custom_fall_asleep)
    
    # 4周期: 23:00 + 30 + 4*90 = 23:30 + 360 = 5:30
    four_cycle = [r for r in results if r.cycles == 4][0]
    expected_wake = bedtime + timedelta(minutes=custom_fall_asleep + 4 * SLEEP_CYCLE_MINUTES)
    
    r.assert_equal(four_cycle.wake_time.hour, expected_wake.hour, "自定义入睡时间小时正确")
    r.assert_equal(four_cycle.wake_time.minute, expected_wake.minute, "自定义入睡时间分钟正确")
    
    print("  ✓ 自定义入睡时间测试完成")


def test_calculate_bedtimes_basic(r: TestResult):
    """测试基本就寝时间计算"""
    print("测试: 基本就寝时间计算")
    
    wake_time = datetime(2024, 1, 1, 7, 0)  # 7:00
    results = calculate_bedtimes(wake_time)
    
    r.assert_equal(len(results), 3, "默认返回3个选项")
    
    # 5周期: 7:00 - 5*90 - 15 = 7:00 - 450 - 15 = 7:00 - 7:45 = 23:15
    five_cycle = [r for r in results if r.cycles == 5][0]
    expected_bed = wake_time - timedelta(minutes=5 * SLEEP_CYCLE_MINUTES + FALL_ASLEEP_MINUTES)
    
    r.assert_equal(five_cycle.bedtime.hour, expected_bed.hour, "就寝小时正确")
    r.assert_equal(five_cycle.bedtime.minute, expected_bed.minute, "就寝分钟正确")
    
    print("  ✓ 基本就寝时间计算测试完成")


def test_calculate_bedtimes_sorted_by_quality(r: TestResult):
    """测试就寝时间按质量排序"""
    print("测试: 就寝时间按质量排序")
    
    wake_time = datetime(2024, 1, 1, 7, 0)
    results = calculate_bedtimes(wake_time)
    
    for i in range(len(results) - 1):
        r.assert_greater_equal(
            results[i].quality_score,
            results[i+1].quality_score,
            f"结果{i}质量 >= 结果{i+1}质量"
        )
    
    print("  ✓ 就寝时间质量排序测试完成")


def test_calculate_quality_score_optimal_cycles(r: TestResult):
    """测试最优周期数评分"""
    print("测试: 最优周期数评分")
    
    # 5个周期 + 6-8点起床 = 最高分
    wake_time = datetime(2024, 1, 1, 7, 0)
    score = calculate_quality_score(5, wake_time)
    
    # 5周期(4分) + 6-8点起床(3分) + 7.5小时睡眠(3分) = 10分
    r.assert_equal(score, 10.0, "最优配置应得满分")
    
    print("  ✓ 最优周期评分测试完成")


def test_calculate_quality_score_suboptimal(r: TestResult):
    """测试次优配置评分"""
    print("测试: 次优配置评分")
    
    # 4周期 + 5点起床
    wake_time = datetime(2024, 1, 1, 5, 0)
    score = calculate_quality_score(4, wake_time)
    
    # 4周期(3.5分) + 5点起床(2分) + 6小时睡眠(2分) = 7.5分
    r.assert_in_range(score, 7.0, 8.0, "次优配置评分范围正确")
    
    print("  ✓ 次优配置评分测试完成")


def test_calculate_quality_score_poor(r: TestResult):
    """测试较差配置评分"""
    print("测试: 较差配置评分")
    
    # 3周期 + 凌晨3点起床
    wake_time = datetime(2024, 1, 1, 3, 0)
    score = calculate_quality_score(3, wake_time)
    
    # 应该得分较低
    r.assert_less_equal(score, 6.0, "较差配置得分应较低")
    
    print("  ✓ 较差配置评分测试完成")


def test_calculate_sleep_debt_no_debt(r: TestResult):
    """测试无睡眠负债"""
    print("测试: 无睡眠负债")
    
    # 每天都睡够7.5小时
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[7.5]*7)
    
    r.assert_equal(debt["debt_hours"], 0.0, "无睡眠负债")
    r.assert_equal(debt["status"], "good", "状态为good")
    r.assert_equal(debt["debt_percentage"], 0.0, "负债百分比为0")
    
    print("  ✓ 无睡眠负债测试完成")


def test_calculate_sleep_debt_mild(r: TestResult):
    """测试轻度睡眠负债"""
    print("测试: 轻度睡眠负债")
    
    # 一周少睡7小时
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[6.5]*7)
    
    r.assert_equal(debt["debt_hours"], 7.0, "轻度负债7小时")
    r.assert_equal(debt["status"], "mild", "状态为mild")
    r.assert_in_range(debt["debt_percentage"], 12, 14, "负债百分比约13%")
    
    print("  ✓ 轻度睡眠负债测试完成")


def test_calculate_sleep_debt_moderate(r: TestResult):
    """测试中度睡眠负债"""
    print("测试: 中度睡眠负债")
    
    # 一周少睡14小时
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[5.5]*7)
    
    r.assert_equal(debt["debt_hours"], 14.0, "中度负债14小时")
    r.assert_equal(debt["status"], "moderate", "状态为moderate")
    
    print("  ✓ 中度睡眠负债测试完成")


def test_calculate_sleep_debt_severe(r: TestResult):
    """测试严重睡眠负债"""
    print("测试: 严重睡眠负债")
    
    # 一周少睡21小时
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[4.5]*7)
    
    r.assert_equal(debt["debt_hours"], 21.0, "严重负债21小时")
    r.assert_equal(debt["status"], "severe", "状态为severe")
    
    print("  ✓ 严重睡眠负债测试完成")


def test_calculate_sleep_debt_partial_data(r: TestResult):
    """测试部分数据的睡眠负债"""
    print("测试: 部分数据睡眠负债")
    
    # 只提供3天数据
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=[6, 7, 8], days=7)
    
    # 应该用平均值填充剩余天数
    r.assert_equal(debt["days_analyzed"], 7, "分析7天")
    r.assert_in_range(debt["average_actual"], 6, 8, "平均睡眠在合理范围")
    
    print("  ✓ 部分数据测试完成")


def test_suggest_nap_power_nap(r: TestResult):
    """测试强力小睡建议"""
    print("测试: 强力小睡建议")
    
    result = suggest_nap(duration_minutes=20)
    
    r.assert_true(len(result["suggestions"]) > 0, "有建议返回")
    r.assert_true(result["suggestions"][0]["recommended"], "20分钟小睡被推荐")
    r.assert_equal(result["suggestions"][0]["type"], "power_nap", "类型为power_nap")
    
    print("  ✓ 强力小睡建议测试完成")


def test_suggest_nap_full_cycle(r: TestResult):
    """测试完整周期小睡建议"""
    print("测试: 完整周期小睡建议")
    
    result = suggest_nap(duration_minutes=90)
    
    r.assert_true(result["suggestions"][0]["recommended"], "90分钟小睡被推荐")
    r.assert_equal(result["suggestions"][0]["type"], "full_cycle_nap", "类型为full_cycle_nap")
    
    print("  ✓ 完整周期小睡建议测试完成")


def test_suggest_nap_moderate_nap(r: TestResult):
    """测试中等时长小睡建议"""
    print("测试: 中等时长小睡建议")
    
    result = suggest_nap(duration_minutes=45)
    
    r.assert_false(result["suggestions"][0]["recommended"], "45分钟小睡不推荐")
    r.assert_equal(result["suggestions"][0]["type"], "moderate_nap", "类型为moderate_nap")
    
    print("  ✓ 中等时长小睡建议测试完成")


def test_suggest_nap_time_advice(r: TestResult):
    """测试小睡时间建议"""
    print("测试: 小睡时间建议")
    
    # 下午2点
    result = suggest_nap(current_hour=14)
    
    time_advice = None
    for s in result["suggestions"]:
        if "time_advice" in s:
            time_advice = s["time_advice"]
            break
    
    r.assert_true(time_advice is not None, "有时间建议")
    r.assert_equal(time_advice[0]["suitability"], "最佳", "下午2点适合小睡")
    
    print("  ✓ 小睡时间建议测试完成")


def test_suggest_nap_fatigue_level(r: TestResult):
    """测试疲劳程度建议"""
    print("测试: 疲劳程度建议")
    
    # 已经醒16小时
    result = suggest_nap(time_since_last_sleep=16)
    
    fatigue_status = None
    for s in result["suggestions"]:
        if "fatigue_status" in s:
            fatigue_status = s
            break
    
    r.assert_true(fatigue_status is not None, "有疲劳状态建议")
    r.assert_equal(fatigue_status["fatigue_status"], "严重疲劳", "16小时后为严重疲劳")
    
    print("  ✓ 疲劳程度建议测试完成")


def test_analyze_circadian_rhythm_early_bird(r: TestResult):
    """测试早鸟型昼夜节律"""
    print("测试: 早鸟型昼夜节律")
    
    wake_time = datetime(2024, 1, 1, 5, 30)
    bedtime = datetime(2024, 1, 1, 21, 30)
    
    result = analyze_circadian_rhythm(wake_time, bedtime)
    
    r.assert_equal(result["chronotype"], "early_bird", "时型为早鸟型")
    r.assert_true(len(result["recommendations"]) > 0, "有建议")
    
    print("  ✓ 早鸟型昼夜节律测试完成")


def test_analyze_circadian_rhythm_night_owl(r: TestResult):
    """测试夜猫子型昼夜节律"""
    print("测试: 夜猫子型昼夜节律")
    
    wake_time = datetime(2024, 1, 1, 10, 0)
    bedtime = datetime(2024, 1, 1, 2, 0)
    
    result = analyze_circadian_rhythm(wake_time, bedtime)
    
    r.assert_equal(result["chronotype"], "night_owl", "时型为夜猫子型")
    
    print("  ✓ 夜猫子型昼夜节律测试完成")


def test_analyze_circadian_rhythm_intermediate(r: TestResult):
    """测试中间型昼夜节律"""
    print("测试: 中间型昼夜节律")
    
    wake_time = datetime(2024, 1, 1, 7, 0)
    bedtime = datetime(2024, 1, 1, 23, 0)
    
    result = analyze_circadian_rhythm(wake_time, bedtime)
    
    r.assert_equal(result["chronotype"], "intermediate", "时型为中间型")
    r.assert_true(len(result["recommendations"]) > 0, "有建议")
    
    print("  ✓ 中间型昼夜节律测试完成")


def test_analyze_circadian_rhythm_age_factors(r: TestResult):
    """测试年龄因素"""
    print("测试: 年龄因素")
    
    wake_time = datetime(2024, 1, 1, 7, 0)
    bedtime = datetime(2024, 1, 1, 23, 0)
    
    # 年轻人
    result_young = analyze_circadian_rhythm(wake_time, bedtime, age=20)
    r.assert_true(len(result_young["alerts"]) > 0, "年轻人有年龄相关提醒")
    
    # 老年人
    result_old = analyze_circadian_rhythm(wake_time, bedtime, age=70)
    r.assert_true(len(result_old["alerts"]) > 0, "老年人有年龄相关提醒")
    
    print("  ✓ 年龄因素测试完成")


def test_get_sleep_stage_distribution(r: TestResult):
    """测试睡眠阶段分布"""
    print("测试: 睡眠阶段分布")
    
    stages = get_sleep_stage_distribution(5)
    
    r.assert_equal(stages["cycles"], 5, "5个周期")
    r.assert_equal(stages["total_minutes"], 450, "总共450分钟")
    r.assert_equal(stages["total_hours"], 7.5, "7.5小时")
    
    # 检查各阶段百分比之和约为100%
    total_percentage = (
        stages["stages"]["light_sleep"]["percentage"] +
        stages["stages"]["deep_sleep"]["percentage"] +
        stages["stages"]["rem_sleep"]["percentage"]
    )
    r.assert_in_range(total_percentage, 99, 101, "百分比之和约100%")
    
    print("  ✓ 睡眠阶段分布测试完成")


def test_get_sleep_stage_distribution_different_cycles(r: TestResult):
    """测试不同周期数的睡眠阶段分布"""
    print("测试: 不同周期数睡眠阶段分布")
    
    for cycles in [4, 5, 6]:
        stages = get_sleep_stage_distribution(cycles)
        r.assert_equal(stages["cycles"], cycles, f"{cycles}周期正确")
        r.assert_equal(stages["total_minutes"], cycles * 90, f"{cycles}周期总分钟数正确")
        
        # 深睡和REM应该都有
        r.assert_greater_equal(stages["stages"]["deep_sleep"]["minutes"], 0, "有深睡时间")
        r.assert_greater_equal(stages["stages"]["rem_sleep"]["minutes"], 0, "有REM时间")
    
    print("  ✓ 不同周期数睡眠阶段分布测试完成")


def test_calculate_sleep_efficiency_excellent(r: TestResult):
    """测试优秀睡眠效率"""
    print("测试: 优秀睡眠效率")
    
    result = calculate_sleep_efficiency(480, 450)  # 8小时在床，7.5小时睡着
    
    r.assert_in_range(result["efficiency_percentage"], 90, 95, "效率90%以上")
    r.assert_equal(result["rating"], "excellent", "评级为优秀")
    
    print("  ✓ 优秀睡眠效率测试完成")


def test_calculate_sleep_efficiency_good(r: TestResult):
    """测试良好睡眠效率"""
    print("测试: 良好睡眠效率")
    
    result = calculate_sleep_efficiency(480, 420)  # 8小时在床，7小时睡着
    
    r.assert_in_range(result["efficiency_percentage"], 85, 90, "效率85-90%")
    r.assert_equal(result["rating"], "good", "评级为良好")
    
    print("  ✓ 良好睡眠效率测试完成")


def test_calculate_sleep_efficiency_fair(r: TestResult):
    """测试一般睡眠效率"""
    print("测试: 一般睡眠效率")
    
    result = calculate_sleep_efficiency(480, 360)  # 8小时在床，6小时睡着
    
    r.assert_in_range(result["efficiency_percentage"], 70, 80, "效率70-80%")
    r.assert_equal(result["rating"], "fair", "评级为一般")
    
    print("  ✓ 一般睡眠效率测试完成")


def test_calculate_sleep_efficiency_poor(r: TestResult):
    """测试较差睡眠效率"""
    print("测试: 较差睡眠效率")
    
    result = calculate_sleep_efficiency(480, 300)  # 8小时在床，5小时睡着
    
    r.assert_less_equal(result["efficiency_percentage"], 75, "效率低于75%")
    r.assert_equal(result["rating"], "poor", "评级为较差")
    
    print("  ✓ 较差睡眠效率测试完成")


def test_calculate_sleep_efficiency_invalid_input(r: TestResult):
    """测试无效输入"""
    print("测试: 无效输入")
    
    r.assert_raises(ValueError, lambda: calculate_sleep_efficiency(0, 100), "在床时间为0应抛出异常")
    r.assert_raises(ValueError, lambda: calculate_sleep_efficiency(-1, 100), "负数在床时间应抛出异常")
    
    print("  ✓ 无效输入测试完成")


def test_calculate_sleep_efficiency_recommendations(r: TestResult):
    """测试睡眠效率建议"""
    print("测试: 睡眠效率建议")
    
    # 低效率应该有更多建议
    low_eff = calculate_sleep_efficiency(480, 300)
    high_eff = calculate_sleep_efficiency(480, 450)
    
    r.assert_true(len(low_eff["recommendations"]) > len(high_eff["recommendations"]), 
                  "低效率有更多建议")
    
    print("  ✓ 睡眠效率建议测试完成")


def test_when_to_wake_convenience(r: TestResult):
    """测试便捷函数when_to_wake"""
    print("测试: when_to_wake便捷函数")
    
    bedtime = datetime(2024, 1, 1, 23, 0)
    results = when_to_wake(bedtime)
    
    r.assert_equal(len(results), 3, "返回3个选项")
    r.assert_true("wake_time" in results[0], "包含wake_time")
    r.assert_true("cycles" in results[0], "包含cycles")
    r.assert_true("quality" in results[0], "包含quality")
    
    print("  ✓ when_to_wake便捷函数测试完成")


def test_when_to_sleep_convenience(r: TestResult):
    """测试便捷函数when_to_sleep"""
    print("测试: when_to_sleep便捷函数")
    
    wake_time = datetime(2024, 1, 1, 7, 0)
    results = when_to_sleep(wake_time)
    
    r.assert_equal(len(results), 3, "返回3个选项")
    r.assert_true("bedtime" in results[0], "包含bedtime")
    r.assert_true("cycles" in results[0], "包含cycles")
    r.assert_true("quality" in results[0], "包含quality")
    
    print("  ✓ when_to_sleep便捷函数测试完成")


def test_calculate_optimal_sleep_schedule_wake_based(r: TestResult):
    """测试基于起床时间的最佳睡眠时间表"""
    print("测试: 基于起床时间的最佳睡眠时间表")
    
    wake_time = datetime(2024, 1, 1, 7, 0)
    result = calculate_optimal_sleep_schedule(wake_time_target=wake_time)
    
    r.assert_true(len(result["options"]) > 0, "有选项")
    r.assert_true(result["recommended"] is not None, "有推荐")
    r.assert_equal(result["options"][0]["type"], "wake_based", "类型正确")
    
    print("  ✓ 基于起床时间的最佳睡眠时间表测试完成")


def test_calculate_optimal_sleep_schedule_bedtime_based(r: TestResult):
    """测试基于就寝时间的最佳睡眠时间表"""
    print("测试: 基于就寝时间的最佳睡眠时间表")
    
    bedtime = datetime(2024, 1, 1, 23, 0)
    result = calculate_optimal_sleep_schedule(bedtime_target=bedtime)
    
    r.assert_true(len(result["options"]) > 0, "有选项")
    r.assert_true(result["recommended"] is not None, "有推荐")
    r.assert_equal(result["options"][0]["type"], "bedtime_based", "类型正确")
    
    print("  ✓ 基于就寝时间的最佳睡眠时间表测试完成")


def test_circadian_rhythm_periods(r: TestResult):
    """测试昼夜节律时间段"""
    print("测试: 昼夜节律时间段")
    
    # 早晨清醒期
    period = CircadianRhythm.get_period(8)
    r.assert_equal(period["name"], "早晨清醒期", "8点为早晨清醒期")
    
    # 高效工作期
    period = CircadianRhythm.get_period(10)
    r.assert_equal(period["name"], "高效工作期", "10点为高效工作期")
    
    # 午后低谷期
    period = CircadianRhythm.get_period(13)
    r.assert_equal(period["name"], "午后低谷期", "13点为午后低谷期")
    
    # 深度睡眠期
    period = CircadianRhythm.get_period(23)
    r.assert_equal(period["name"], "深度睡眠期", "23点为深度睡眠期")
    
    print("  ✓ 昼夜节律时间段测试完成")


def test_sleep_quality_levels(r: TestResult):
    """测试睡眠质量等级"""
    print("测试: 睡眠质量等级")
    
    r.assert_equal(SleepQuality.from_score(9.5), SleepQuality.EXCELLENT, "9.5分为优秀")
    r.assert_equal(SleepQuality.from_score(8.0), SleepQuality.GOOD, "8.0分为良好")
    r.assert_equal(SleepQuality.from_score(6.0), SleepQuality.FAIR, "6.0分为一般")
    r.assert_equal(SleepQuality.from_score(3.5), SleepQuality.POOR, "3.5分为较差")
    r.assert_equal(SleepQuality.from_score(1.0), SleepQuality.VERY_POOR, "1.0分为很差")
    
    print("  ✓ 睡眠质量等级测试完成")


def test_format_duration(r: TestResult):
    """测试时长格式化"""
    print("测试: 时长格式化")
    
    r.assert_equal(format_duration(90), "1小时30分钟", "90分钟格式化正确")
    r.assert_equal(format_duration(60), "1小时", "60分钟格式化正确")
    r.assert_equal(format_duration(45), "45分钟", "45分钟格式化正确")
    r.assert_equal(format_duration(120), "2小时", "120分钟格式化正确")
    
    print("  ✓ 时长格式化测试完成")


def test_edge_case_midnight(r: TestResult):
    """测试午夜边界情况"""
    print("测试: 午夜边界情况")
    
    # 午夜就寝
    bedtime = datetime(2024, 1, 1, 0, 0)
    results = calculate_wake_times(bedtime)
    
    r.assert_true(len(results) > 0, "午夜就寝有结果")
    
    # 午夜起床
    wake_time = datetime(2024, 1, 1, 0, 0)
    results = calculate_bedtimes(wake_time)
    
    r.assert_true(len(results) > 0, "午夜起床有结果")
    
    print("  ✓ 午夜边界情况测试完成")


def test_edge_case_zero_sleep(r: TestResult):
    """测试极端少睡眠"""
    print("测试: 极端少睡眠")
    
    # 3个周期（极少的睡眠）
    wake_time = datetime(2024, 1, 1, 7, 0)
    results = calculate_bedtimes(wake_time, cycles_range=(3, 3))
    
    r.assert_equal(len(results), 1, "只有1个选项")
    r.assert_equal(results[0].cycles, 3, "3个周期")
    r.assert_less_equal(results[0].quality_score, 5.0, "质量分数较低")
    
    print("  ✓ 极端少睡眠测试完成")


def test_edge_case_long_sleep(r: TestResult):
    """测试长睡眠"""
    print("测试: 长睡眠")
    
    # 7个周期（很长的睡眠）
    wake_time = datetime(2024, 1, 1, 10, 0)
    results = calculate_bedtimes(wake_time, cycles_range=(7, 7))
    
    r.assert_equal(len(results), 1, "只有1个选项")
    r.assert_equal(results[0].cycles, 7, "7个周期")
    r.assert_equal(results[0].total_sleep_minutes, 630, "10.5小时")
    
    print("  ✓ 长睡眠测试完成")


def test_consistency_wake_bedtime(r: TestResult):
    """测试起床和就寝计算一致性"""
    print("测试: 起床和就寝计算一致性")
    
    # 如果在某时间起床，根据计算出的就寝时间再计算起床，应该得到相近结果
    wake_time = datetime(2024, 1, 1, 7, 0)
    bed_results = calculate_bedtimes(wake_time)
    
    # 取5周期的结果
    five_cycle = [r for r in bed_results if r.cycles == 5][0]
    
    # 用这个就寝时间再计算起床时间
    wake_results = calculate_wake_times(five_cycle.bedtime)
    
    # 找到5周期的结果
    five_cycle_wake = [r for r in wake_results if r.cycles == 5][0]
    
    # 两个起床时间应该相同
    r.assert_equal(five_cycle_wake.wake_time.hour, wake_time.hour, "起床小时一致")
    r.assert_equal(five_cycle_wake.wake_time.minute, wake_time.minute, "起床分钟一致")
    
    print("  ✓ 起床和就寝计算一致性测试完成")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Sleep Utils 测试套件")
    print("=" * 60)
    
    result = TestResult()
    
    # 基本功能测试
    test_calculate_wake_times_basic(result)
    test_calculate_wake_times_sorted_by_quality(result)
    test_calculate_wake_times_with_custom_fall_asleep(result)
    test_calculate_bedtimes_basic(result)
    test_calculate_bedtimes_sorted_by_quality(result)
    
    # 质量评分测试
    test_calculate_quality_score_optimal_cycles(result)
    test_calculate_quality_score_suboptimal(result)
    test_calculate_quality_score_poor(result)
    
    # 睡眠负债测试
    test_calculate_sleep_debt_no_debt(result)
    test_calculate_sleep_debt_mild(result)
    test_calculate_sleep_debt_moderate(result)
    test_calculate_sleep_debt_severe(result)
    test_calculate_sleep_debt_partial_data(result)
    
    # 小睡建议测试
    test_suggest_nap_power_nap(result)
    test_suggest_nap_full_cycle(result)
    test_suggest_nap_moderate_nap(result)
    test_suggest_nap_time_advice(result)
    test_suggest_nap_fatigue_level(result)
    
    # 昼夜节律测试
    test_analyze_circadian_rhythm_early_bird(result)
    test_analyze_circadian_rhythm_night_owl(result)
    test_analyze_circadian_rhythm_intermediate(result)
    test_analyze_circadian_rhythm_age_factors(result)
    
    # 睡眠阶段测试
    test_get_sleep_stage_distribution(result)
    test_get_sleep_stage_distribution_different_cycles(result)
    
    # 睡眠效率测试
    test_calculate_sleep_efficiency_excellent(result)
    test_calculate_sleep_efficiency_good(result)
    test_calculate_sleep_efficiency_fair(result)
    test_calculate_sleep_efficiency_poor(result)
    test_calculate_sleep_efficiency_invalid_input(result)
    test_calculate_sleep_efficiency_recommendations(result)
    
    # 便捷函数测试
    test_when_to_wake_convenience(result)
    test_when_to_sleep_convenience(result)
    test_calculate_optimal_sleep_schedule_wake_based(result)
    test_calculate_optimal_sleep_schedule_bedtime_based(result)
    
    # 类和常量测试
    test_circadian_rhythm_periods(result)
    test_sleep_quality_levels(result)
    test_format_duration(result)
    
    # 边界情况测试
    test_edge_case_midnight(result)
    test_edge_case_zero_sleep(result)
    test_edge_case_long_sleep(result)
    
    # 一致性测试
    test_consistency_wake_bedtime(result)
    
    # 输出结果
    print("\n" + "=" * 60)
    success = result.summary()
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(run_all_tests())