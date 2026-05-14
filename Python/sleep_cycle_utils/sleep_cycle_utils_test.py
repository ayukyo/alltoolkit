"""
Sleep Cycle Utilities 测试

覆盖:
- 起床时间计算
- 入睡时间计算
- 睡眠质量评估
- 睡眠债务计算
- 小睡建议
- 昼夜节律分析
- 睡眠阶段时间线
- JSON 序列化
- 边界值处理
"""

import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sleep_cycle_utils.mod import (
    SleepCycleCalculator, SleepCycleResult, SleepDebt, NapRecommendation,
    SleepWindow, SleepStage, SleepQuality, NapType,
    calculate_wake_times, calculate_bed_times, get_optimal_sleep_duration,
    format_sleep_duration, get_quality_description, recommend_nap
)
from datetime import datetime, timedelta, time


class ResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}: {message}")
            self.errors.append((name, message))
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败 (共 {total})")
        if self.errors:
            print("\n失败的测试:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}\n")
        return self.failed == 0


def test_calculator_initialization():
    """测试计算器初始化"""
    print("\n[测试] 计算器初始化")
    r = ResultCollector()
    
    # 默认配置
    calc = SleepCycleCalculator()
    r.test("默认周期时长", calc.cycle_duration == 90)
    r.test("默认入睡时间", calc.fall_asleep_time == 15)
    r.test("默认目标睡眠", calc.target_sleep_hours == 8)
    
    # 自定义配置
    calc2 = SleepCycleCalculator(
        cycle_duration=85,
        fall_asleep_time=20,
        target_sleep_hours=7
    )
    r.test("自定义周期时长", calc2.cycle_duration == 85)
    r.test("自定义入睡时间", calc2.fall_asleep_time == 20)
    r.test("自定义目标睡眠", calc2.target_sleep_hours == 7)
    
    return r.summary()


def test_wake_time_calculation():
    """测试起床时间计算"""
    print("\n[测试] 起床时间计算")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    bed_time = datetime(2024, 1, 1, 22, 0)  # 22:00 入睡
    
    # 计算起床时间
    results = calc.calculate_wake_times(bed_time)
    r.test("返回结果不为空", len(results) > 0)
    r.test("默认返回4个结果", len(results) == 4)
    
    # 检查第一个结果（3个周期）
    first = results[0]
    # 22:00 + 15分钟入睡 + 270分钟睡眠 = 285分钟 = 02:45 次日
    r.test("3周期起床时间正确", first.target_time.hour == 2 and first.target_time.minute == 45)
    r.test("3周期数为3", first.cycle_count == 3)
    r.test("3周期总时长正确", first.duration_minutes == 285)  # 15 + 270
    
    # 检查睡眠质量
    r.test("3周期质量为FAIR", first.quality == SleepQuality.FAIR)
    
    # 检查第二个结果（4个周期）
    second = results[1]
    # 22:00 + 15分钟入睡 + 360分钟睡眠 = 375分钟 = 04:15 次日
    r.test("4周期起床时间正确", second.target_time.hour == 4 and second.target_time.minute == 15)
    r.test("4周期质量为GOOD", second.quality == SleepQuality.GOOD)
    
    # 自定义周期范围
    results2 = calc.calculate_wake_times(bed_time, min_cycles=4, max_cycles=6)
    r.test("自定义周期范围", len(results2) == 3)
    r.test("最小周期为4", results2[0].cycle_count == 4)
    
    return r.summary()


def test_bed_time_calculation():
    """测试入睡时间计算"""
    print("\n[测试] 入睡时间计算")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    wake_time = datetime(2024, 1, 1, 7, 0)  # 07:00 起床
    
    # 计算入睡时间
    results = calc.calculate_bed_times(wake_time)
    r.test("返回结果不为空", len(results) > 0)
    r.test("默认返回4个结果", len(results) == 4)
    
    # 检查5周期入睡时间
    five_cycle_result = None
    for res in results:
        if res.cycle_count == 5:
            five_cycle_result = res
            break
    
    r.test("包含5周期结果", five_cycle_result is not None)
    if five_cycle_result:
        expected_bed = wake_time - timedelta(minutes=15 + 5 * 90)  # 07:00 - 465 = 23:15前一天
        r.test("5周期入睡时间正确", five_cycle_result.target_time.hour == 23 or five_cycle_result.target_time.hour == -1)
        r.test("5周期质量为EXCELLENT", five_cycle_result.quality == SleepQuality.EXCELLENT)
    
    # 自定义周期范围
    results2 = calc.calculate_bed_times(wake_time, min_cycles=2, max_cycles=5)
    r.test("自定义周期范围-结果数", len(results2) <= 4)
    
    return r.summary()


def test_sleep_quality_evaluation():
    """测试睡眠质量评估"""
    print("\n[测试] 睡眠质量评估")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 不同周期数的质量
    r.test("6周期为EXCELLENT", calc._evaluate_quality(6) == SleepQuality.EXCELLENT)
    r.test("5周期为EXCELLENT", calc._evaluate_quality(5) == SleepQuality.EXCELLENT)
    r.test("4周期为GOOD", calc._evaluate_quality(4) == SleepQuality.GOOD)
    r.test("3周期为FAIR", calc._evaluate_quality(3) == SleepQuality.FAIR)
    r.test("2周期为POOR", calc._evaluate_quality(2) == SleepQuality.POOR)
    r.test("1周期为INSUFFICIENT", calc._evaluate_quality(1) == SleepQuality.INSUFFICIENT)
    
    # 基于睡眠时长的评估
    r.test("8小时为EXCELLENT", calc._evaluate_sleep_duration(8) == SleepQuality.EXCELLENT)
    r.test("7小时为GOOD", calc._evaluate_sleep_duration(7) == SleepQuality.GOOD)
    r.test("6小时为FAIR", calc._evaluate_sleep_duration(6) == SleepQuality.FAIR)
    r.test("5小时为POOR", calc._evaluate_sleep_duration(5) == SleepQuality.POOR)
    r.test("4小时为INSUFFICIENT", calc._evaluate_sleep_duration(4) == SleepQuality.INSUFFICIENT)
    
    return r.summary()


def test_sleep_window():
    """测试睡眠窗口计算"""
    print("\n[测试] 睡眠窗口计算")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    wake_time = datetime(2024, 1, 1, 7, 0)
    
    window = calc.calculate_optimal_sleep_window(wake_time)
    r.test("睡眠窗口不为空", window is not None)
    r.test("结束时间正确", window.end_time == wake_time)
    r.test("周期数有效", 3 <= window.cycle_count <= 6)
    r.test("评分有效", 0 <= window.score <= 100)
    r.test("质量有效", window.quality in SleepQuality)
    
    # 自定义睡眠时长
    window2 = calc.calculate_optimal_sleep_window(wake_time, preferred_duration_hours=6)
    r.test("自定义时长窗口", window2 is not None)
    
    return r.summary()


def test_sleep_debt():
    """测试睡眠债务计算"""
    print("\n[测试] 睡眠债务计算")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 无债务
    sleep_records = [{"date": "2024-01-01", "hours": 8}]
    debt = calc.calculate_sleep_debt(sleep_records, target_hours=8)
    r.test("充足睡眠无债务", debt.debt_hours == 0)
    r.test("实际睡眠正确", debt.actual_hours == 8)
    
    # 有债务
    sleep_records2 = [
        {"date": "2024-01-01", "hours": 6},
        {"date": "2024-01-02", "hours": 5.5},
        {"date": "2024-01-03", "hours": 7}
    ]
    debt2 = calc.calculate_sleep_debt(sleep_records2, target_hours=8, recovery_days=2)
    total_debt = (8-6) + (8-5.5) + (8-7)  # 2 + 2.5 + 1 = 5.5
    r.test("债务计算正确", debt2.debt_hours == 5.5)
    r.test("债务分钟数正确", debt2.debt_minutes == 330)
    r.test("累计天数正确", debt2.accumulated_days == 3)
    r.test("恢复计划有数据", len(debt2.recovery_plan) == 2)
    
    # 实际睡眠平均值
    avg_actual = (6 + 5.5 + 7) / 3
    r.test("平均睡眠正确", debt2.actual_hours == avg_actual)
    
    return r.summary()


def test_nap_recommendation():
    """测试小睡建议"""
    print("\n[测试] 小睡建议")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 默认建议
    now = datetime(2024, 1, 1, 14, 0)  # 下午2点
    nap = calc.get_nap_recommendation(now)
    r.test("小睡建议不为空", nap is not None)
    r.test("时长有效", nap.duration_minutes > 0)
    r.test("类型有效", nap.nap_type in NapType)
    r.test("有好处列表", len(nap.benefits) > 0)
    r.test("有警告列表", len(nap.warnings) > 0)
    
    # 能量小睡
    nap_power = calc.get_nap_recommendation(now, NapType.POWER)
    r.test("能量小睡时长正确", nap_power.duration_minutes == 20)
    r.test("能量小睡类型正确", nap_power.nap_type == NapType.POWER)
    
    # 理想小睡（完整周期）
    nap_ideal = calc.get_nap_recommendation(now, NapType.IDEAL)
    r.test("理想小睡时长正确", nap_ideal.duration_minutes == 90)
    r.test("理想小睡类型正确", nap_ideal.nap_type == NapType.IDEAL)
    
    # 不同时间的默认建议
    morning = datetime(2024, 1, 1, 9, 0)
    nap_morning = calc.get_nap_recommendation(morning)
    r.test("上午默认能量小睡", nap_morning.nap_type == NapType.POWER)
    
    evening = datetime(2024, 1, 1, 18, 0)
    nap_evening = calc.get_nap_recommendation(evening)
    r.test("傍晚只能短睡", nap_evening.nap_type == NapType.POWER)
    
    return r.summary()


def test_circadian_rhythm():
    """测试昼夜节律分析"""
    print("\n[测试] 昼夜节律分析")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 早起型
    wake_time = time(6, 30)
    bed_time = time(22, 30)
    analysis = calc.analyze_circadian_rhythm(wake_time, bed_time, age=30)
    r.test("分析结果不为空", analysis is not None)
    r.test("包含节律类型", "chronotype" in analysis)
    r.test("包含节律名称", "chronotype_name" in analysis)
    r.test("包含睡眠时长", "sleep_duration_hours" in analysis)
    r.test("包含建议", "recommendations" in analysis)
    
    # 睡眠时长计算
    r.test("睡眠时长有效", analysis["sleep_duration_hours"] >= 0)
    
    # 不同起床时间
    early_wake = time(5, 0)
    early_bed = time(21, 0)
    analysis_early = calc.analyze_circadian_rhythm(early_wake, early_bed)
    r.test("早起型判定", analysis_early["chronotype"] == "extreme_early_bird")
    
    late_wake = time(11, 0)
    late_bed = time(2, 0)  # 凌晨2点
    analysis_late = calc.analyze_circadian_rhythm(late_wake, late_bed)
    r.test("晚睡型判定", analysis_late["chronotype"] in ["night_owl", "extreme_night_owl"])
    
    # 年龄调整
    young_analysis = calc.analyze_circadian_rhythm(wake_time, bed_time, age=20)
    r.test("年轻人建议更多睡眠", young_analysis["recommended_hours"] >= 8)
    
    old_analysis = calc.analyze_circadian_rhythm(wake_time, bed_time, age=70)
    r.test("老年人建议", old_analysis["recommended_hours"] <= 8)
    
    return r.summary()


def test_sleep_stages_timeline():
    """测试睡眠阶段时间线"""
    print("\n[测试] 睡眠阶段时间线")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    bed_time = datetime(2024, 1, 1, 22, 0)
    
    timeline = calc.get_sleep_stages_timeline(bed_time, cycle_count=5)
    r.test("时间线不为空", len(timeline) == 5)
    
    # 检查第一个周期
    first_cycle = timeline[0]
    r.test("包含周期编号", "cycle" in first_cycle)
    r.test("包含开始时间", "start_time" in first_cycle)
    r.test("包含结束时间", "end_time" in first_cycle)
    r.test("包含阶段信息", "stages" in first_cycle)
    r.test("包含最佳起床窗口", "best_wake_window" in first_cycle)
    
    # 阶段数据
    stages = first_cycle["stages"]
    r.test("有3个睡眠阶段", len(stages) == 3)
    
    # 检查阶段类型
    stage_types = [s["stage"] for s in stages]
    r.test("包含浅睡阶段", SleepStage.LIGHT.value in stage_types)
    r.test("包含深睡阶段", SleepStage.DEEP.value in stage_types)
    r.test("包含REM阶段", SleepStage.REM.value in stage_types)
    
    # 深睡减少趋势
    deep_percentages = [c["stages"][1]["percentage"] for c in timeline]
    r.test("深睡逐渐减少", deep_percentages[0] > deep_percentages[-1])
    
    # REM增加趋势
    rem_percentages = [c["stages"][2]["percentage"] for c in timeline]
    r.test("REM逐渐增加", rem_percentages[0] < rem_percentages[-1])
    
    return r.summary()


def test_sleep_score():
    """测试睡眠评分"""
    print("\n[测试] 睡眠评分")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 不同周期数的评分
    score_5 = calc._calculate_sleep_score(5, 8)
    r.test("5周期评分有效", 0 <= score_5 <= 100)
    
    score_3 = calc._calculate_sleep_score(3, 8)
    r.test("3周期评分更低", score_3 < score_5)
    
    score_6 = calc._calculate_sleep_score(6, 9)
    r.test("6周期评分高", score_6 > 90)
    
    # 与目标时长匹配
    score_match = calc._calculate_sleep_score(5, 7.5)  # 5周期正好7.5小时
    r.test("匹配目标评分高", score_match > 95)
    
    return r.summary()


def test_json_serialization():
    """测试 JSON 序列化"""
    print("\n[测试] JSON 序列化")
    r = ResultCollector()
    
    calc = SleepCycleCalculator(cycle_duration=85, fall_asleep_time=20)
    
    # 序列化计算器
    json_str = calc.to_json()
    r.test("序列化成功", len(json_str) > 0)
    r.test("JSON包含周期时长", "cycle_duration" in json_str)
    r.test("JSON包含入睡时间", "fall_asleep_time" in json_str)
    
    # 反序列化
    calc2 = SleepCycleCalculator.from_json(json_str)
    r.test("反序列化周期时长", calc2.cycle_duration == 85)
    r.test("反序列化入睡时间", calc2.fall_asleep_time == 20)
    
    # SleepCycleResult 序列化
    bed_time = datetime(2024, 1, 1, 22, 0)
    results = calc.calculate_wake_times(bed_time)
    result_dict = results[0].to_dict()
    r.test("结果序列化包含时间", "target_time" in result_dict)
    r.test("结果序列化包含周期数", "cycle_count" in result_dict)
    r.test("结果序列化包含质量", "quality" in result_dict)
    
    # SleepCycleResult 反序列化
    result2 = SleepCycleResult.from_dict(result_dict)
    r.test("结果反序列化周期数", result2.cycle_count == results[0].cycle_count)
    r.test("结果反序列化质量", result2.quality == results[0].quality)
    
    # SleepDebt 序列化
    sleep_records = [{"date": "2024-01-01", "hours": 6}]
    debt = calc.calculate_sleep_debt(sleep_records)
    debt_dict = debt.to_dict()
    r.test("债务序列化包含债务小时", "debt_hours" in debt_dict)
    
    debt2 = SleepDebt.from_dict(debt_dict)
    r.test("债务反序列化正确", debt2.debt_hours == debt.debt_hours)
    
    # NapRecommendation 序列化
    nap = calc.get_nap_recommendation(datetime.now())
    nap_dict = nap.to_dict()
    r.test("小睡序列化包含类型", "nap_type" in nap_dict)
    r.test("小睡序列化包含时长", "duration_minutes" in nap_dict)
    
    nap2 = NapRecommendation.from_dict(nap_dict)
    r.test("小睡反序列化类型", nap2.nap_type == nap.nap_type)
    r.test("小睡反序列化时长", nap2.duration_minutes == nap.duration_minutes)
    
    # SleepWindow 序列化
    window = calc.calculate_optimal_sleep_window(datetime.now())
    window_dict = window.to_dict()
    r.test("窗口序列化包含评分", "score" in window_dict)
    
    window2 = SleepWindow.from_dict(window_dict)
    r.test("窗口反序列化评分", window2.score == window.score)
    
    return r.summary()


def test_convenience_functions():
    """测试便捷函数"""
    print("\n[测试] 便捷函数")
    r = ResultCollector()
    
    # calculate_wake_times
    bed_time = datetime(2024, 1, 1, 22, 0)
    wake_results = calculate_wake_times(bed_time)
    r.test("便捷计算起床时间", len(wake_results) == 4)
    
    # calculate_bed_times
    wake_time = datetime(2024, 1, 1, 7, 0)
    bed_results = calculate_bed_times(wake_time)
    r.test("便捷计算入睡时间", len(bed_results) == 4)
    
    # get_optimal_sleep_duration
    duration = get_optimal_sleep_duration(5)
    expected = 15 + 5 * 90  # 465分钟
    r.test("最佳睡眠时长正确", duration == expected)
    
    # format_sleep_duration
    formatted = format_sleep_duration(90)
    r.test("格式化90分钟", formatted == "1小时30分钟")
    
    formatted2 = format_sleep_duration(60)
    r.test("格式化60分钟", formatted2 == "1小时")
    
    formatted3 = format_sleep_duration(45)
    r.test("格式化45分钟", formatted3 == "45分钟")
    
    # get_quality_description
    desc = get_quality_description(SleepQuality.EXCELLENT)
    r.test("优秀质量描述", "优秀" in desc)
    
    desc2 = get_quality_description(SleepQuality.POOR)
    r.test("较差质量描述", "较差" in desc2)
    
    # recommend_nap
    nap = recommend_nap(14, "medium")
    r.test("便捷小睡建议", nap is not None)
    r.test("小睡时长有效", nap.duration_minutes > 0)
    
    return r.summary()


def test_dataclasses():
    """测试数据类"""
    print("\n[测试] 数据类")
    r = ResultCollector()
    
    # SleepCycleResult
    result = SleepCycleResult(
        target_time=datetime(2024, 1, 1, 7, 0),
        cycle_count=5,
        duration_minutes=465,
        actual_sleep_minutes=450,
        fall_asleep_minutes=15,
        quality=SleepQuality.EXCELLENT,
        recommendation="测试"
    )
    r.test("创建结果-周期数", result.cycle_count == 5)
    r.test("创建结果-质量", result.quality == SleepQuality.EXCELLENT)
    r.test("创建结果-建议", result.recommendation == "测试")
    
    # SleepDebt
    debt = SleepDebt(
        target_hours=8,
        actual_hours=6,
        debt_hours=2,
        debt_minutes=120,
        accumulated_days=1,
        recovery_hours_needed=2,
        recovery_plan=[{"day": 1, "extra_hours": 2}]
    )
    r.test("创建债务-目标", debt.target_hours == 8)
    r.test("创建债务-债务小时", debt.debt_hours == 2)
    r.test("创建债务-计划", len(debt.recovery_plan) == 1)
    
    # NapRecommendation
    nap = NapRecommendation(
        nap_type=NapType.POWER,
        duration_minutes=20,
        best_time_start=time(13, 0),
        best_time_end=time(15, 0),
        benefits=["快速恢复"],
        warnings=["避免过长"]
    )
    r.test("创建小睡-类型", nap.nap_type == NapType.POWER)
    r.test("创建小睡-时长", nap.duration_minutes == 20)
    r.test("创建小睡-好处", len(nap.benefits) == 1)
    
    # SleepWindow
    window = SleepWindow(
        start_time=datetime(2024, 1, 1, 22, 0),
        end_time=datetime(2024, 1, 2, 7, 0),
        cycle_count=5,
        quality=SleepQuality.EXCELLENT,
        score=95.0
    )
    r.test("创建窗口-周期数", window.cycle_count == 5)
    r.test("创建窗口-评分", window.score == 95.0)
    
    return r.summary()


def test_enums():
    """测试枚举"""
    print("\n[测试] 枚举")
    r = ResultCollector()
    
    # SleepStage
    r.test("SleepStage.AWAKE值", SleepStage.AWAKE.value == "awake")
    r.test("SleepStage.LIGHT值", SleepStage.LIGHT.value == "light")
    r.test("SleepStage.DEEP值", SleepStage.DEEP.value == "deep")
    r.test("SleepStage.REM值", SleepStage.REM.value == "rem")
    
    # SleepQuality
    r.test("SleepQuality.EXCELLENT值", SleepQuality.EXCELLENT.value == "excellent")
    r.test("SleepQuality.GOOD值", SleepQuality.GOOD.value == "good")
    r.test("SleepQuality.FAIR值", SleepQuality.FAIR.value == "fair")
    r.test("SleepQuality.POOR值", SleepQuality.POOR.value == "poor")
    r.test("SleepQuality.INSUFFICIENT值", SleepQuality.INSUFFICIENT.value == "insufficient")
    
    # NapType
    r.test("NapType.POWER值", NapType.POWER.value == "power")
    r.test("NapType.SHORT值", NapType.SHORT.value == "short")
    r.test("NapType.IDEAL值", NapType.IDEAL.value == "ideal")
    r.test("NapType.LONG值", NapType.LONG.value == "long")
    
    return r.summary()


def test_edge_cases():
    """测试边界情况"""
    print("\n[测试] 边界情况")
    r = ResultCollector()
    
    # 极短周期
    calc = SleepCycleCalculator()
    bed_time = datetime(2024, 1, 1, 22, 0)
    short_results = calc.calculate_wake_times(bed_time, min_cycles=1, max_cycles=2)
    r.test("极短周期结果", len(short_results) >= 1)
    r.test("极短周期质量为INSUFFICIENT或POOR", 
           short_results[0].quality in [SleepQuality.INSUFFICIENT, SleepQuality.POOR])
    
    # 极长周期
    long_results = calc.calculate_wake_times(bed_time, min_cycles=10, max_cycles=12, count=3)
    r.test("极长周期结果", len(long_results) >= 1)
    
    # 空睡眠记录
    empty_debt = calc.calculate_sleep_debt([])
    r.test("空记录债务为0", empty_debt.debt_hours == 0)
    
    # 零目标睡眠
    zero_target = calc.calculate_sleep_debt([{"date": "2024-01-01", "hours": 8}], target_hours=0)
    r.test("零目标无债务", zero_target.debt_hours == 0)
    
    # 跨午夜睡眠
    bed_cross = datetime(2024, 1, 1, 23, 30)
    wake_cross = calc.calculate_wake_times(bed_cross)
    r.test("跨午夜计算成功", len(wake_cross) > 0)
    
    # 跨天起床时间
    wake_next_day = datetime(2024, 1, 2, 6, 0)
    bed_prev = calc.calculate_bed_times(wake_next_day)
    r.test("跨天计算成功", len(bed_prev) > 0)
    
    return r.summary()


def test_recommendations():
    """测试建议生成"""
    print("\n[测试] 建议生成")
    r = ResultCollector()
    
    calc = SleepCycleCalculator()
    
    # 不同周期的起床建议
    wake_rec_5 = calc._generate_wake_recommendation(5, SleepQuality.EXCELLENT)
    r.test("5周期起床建议不为空", len(wake_rec_5) > 0)
    r.test("5周期建议包含关键信息", "7.5小时" in wake_rec_5 or "优秀" in wake_rec_5)
    
    wake_rec_3 = calc._generate_wake_recommendation(3, SleepQuality.FAIR)
    r.test("3周期起床建议不为空", len(wake_rec_3) > 0)
    
    # 不同周期的入睡建议
    bed_rec_5 = calc._generate_bed_recommendation(5, SleepQuality.EXCELLENT)
    r.test("5周期入睡建议不为空", len(bed_rec_5) > 0)
    
    # 昼夜节律建议
    chrono_recs = calc._get_chronotype_recommendations("early_bird")
    r.test("早起型建议不为空", len(chrono_recs) > 0)
    
    chrono_recs2 = calc._get_chronotype_recommendations("night_owl")
    r.test("晚睡型建议不为空", len(chrono_recs2) > 0)
    
    return r.summary()


def test_energy_level_nap():
    """测试不同能量水平的小睡建议"""
    print("\n[测试] 能量水平小睡")
    r = ResultCollector()
    
    # 低能量
    nap_low = recommend_nap(14, "low")
    r.test("低能量建议时长更长", nap_low.duration_minutes >= 20)
    
    # 高能量
    nap_high = recommend_nap(14, "high")
    r.test("高能量建议时长短", nap_high.duration_minutes == 20)
    
    # 中等能量
    nap_medium = recommend_nap(14, "medium")
    r.test("中等能量建议有效", nap_medium.duration_minutes > 0)
    
    return r.summary()


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("Sleep Cycle Utilities 测试套件")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_calculator_initialization()
    all_passed &= test_wake_time_calculation()
    all_passed &= test_bed_time_calculation()
    all_passed &= test_sleep_quality_evaluation()
    all_passed &= test_sleep_window()
    all_passed &= test_sleep_debt()
    all_passed &= test_nap_recommendation()
    all_passed &= test_circadian_rhythm()
    all_passed &= test_sleep_stages_timeline()
    all_passed &= test_sleep_score()
    all_passed &= test_json_serialization()
    all_passed &= test_convenience_functions()
    all_passed &= test_dataclasses()
    all_passed &= test_enums()
    all_passed &= test_edge_cases()
    all_passed &= test_recommendations()
    all_passed &= test_energy_level_nap()
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)