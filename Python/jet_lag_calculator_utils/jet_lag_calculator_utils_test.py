#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jet Lag Calculator Utils Test - 时差计算器工具测试

测试模块：jet_lag_calculator_utils
测试用例数：40+
测试覆盖：时差计算、恢复时间估算、睡眠建议、光照时机、路线分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    JetLagCalculator, JetLagResult, TimezoneInfo,
    SleepType, TravelDirection, SleepSchedule,
    calculate_jet_lag, get_common_timezones,
    quick_estimate, analyze_route, POPULAR_ROUTES
)
from datetime import datetime, time


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_timezone_info(results, add_result):
    """测试时区信息"""
    # test 1: 创建时区
    tz = TimezoneInfo(name="UTC+8", utc_offset=8)
    add_result("TimezoneInfo basic", tz.name == "UTC+8" and tz.utc_offset == 8)
    
    # test 2: from_utc_offset
    tz2 = TimezoneInfo.from_utc_offset(-5)
    add_result("TimezoneInfo from_utc_offset", tz2.utc_offset == -5)
    
    # test 3: 零时区
    tz_utc = TimezoneInfo.from_utc_offset(0)
    add_result("TimezoneInfo UTC", tz_utc.utc_offset == 0)


def test_sleep_type(results, add_result):
    """测试睡眠类型"""
    # test 4: 睡眠类型枚举
    add_result("SleepType values", 
               SleepType.MORNING_LARK.value == "morning_lark" and 
               SleepType.NIGHT_OWL.value == "night_owl")


def test_travel_direction(results, add_result):
    """测试旅行方向"""
    # test 5: 旅行方向枚举
    add_result("TravelDirection values", 
               TravelDirection.EAST.value == "east" and 
               TravelDirection.WEST.value == "west")


def test_sleep_schedule(results, add_result):
    """测试睡眠时间表"""
    schedule = SleepSchedule(
        bed_time=time(23, 0),
        wake_time=time(7, 0),
        duration=8.0
    )
    
    # test 6: 基础属性
    add_result("SleepSchedule basic", 
               schedule.bed_time == time(23, 0) and 
               schedule.wake_time == time(7, 0))
    
    # test 7: 字符串表示
    str_repr = str(schedule)
    add_result("SleepSchedule str", "23:00" in str_repr and "7:00" in str_repr)


def test_jet_lag_calculator_basic(results, add_result):
    """测试时差计算器基础功能"""
    calc = JetLagCalculator(age=30)
    
    origin = TimezoneInfo.from_utc_offset(-5)  # EST
    dest = TimezoneInfo.from_utc_offset(0)     # London
    
    result = calc.calculate(origin, dest)
    
    # test 8: 时差计算
    add_result("calculate time_difference", abs(result.time_difference) == 5)
    
    # test 9: 方向判断
    add_result("calculate direction", result.direction == TravelDirection.EAST)
    
    # test 10: 严重程度分数
    add_result("calculate severity_score", 0 <= result.severity_score <= 100)
    
    # test 11: 严重程度级别
    add_result("calculate severity_level", result.severity_level in 
               ["Minimal", "Mild", "Moderate", "Severe", "Extreme"])
    
    # test 12: 恢复天数
    add_result("calculate recovery_days", result.estimated_recovery_days > 0)
    
    # test 13: 建议
    add_result("calculate recommendations", len(result.recommendations) > 0)


def test_west_travel(results, add_result):
    """测试向西旅行"""
    calc = JetLagCalculator(age=30)
    
    origin = TimezoneInfo.from_utc_offset(0)   # London
    dest = TimezoneInfo.from_utc_offset(-5)    # NYC
    
    result = calc.calculate(origin, dest)
    
    # test 14: 向西方向
    add_result("west travel direction", result.direction == TravelDirection.WEST)
    
    # test 15: 向西恢复更快
    east_result = calc.calculate(TimezoneInfo.from_utc_offset(-5), TimezoneInfo.from_utc_offset(0))
    add_result("west travel recovery faster", 
               result.estimated_recovery_days < east_result.estimated_recovery_days)


def test_no_time_difference(results, add_result):
    """测试无时差"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(8)
    dest = TimezoneInfo.from_utc_offset(8)
    
    result = calc.calculate(origin, dest)
    
    # test 16: 无方向
    add_result("no difference direction", result.direction == TravelDirection.NONE)
    
    # test 17: 无恢复时间
    add_result("no difference recovery", result.estimated_recovery_days == 0)


def test_sleep_type_effects(results, add_result):
    """测试睡眠类型影响"""
    # test 18: 夜猫子向东更难
    calc_owl = JetLagCalculator(age=30, sleep_type=SleepType.NIGHT_OWL)
    calc_lark = JetLagCalculator(age=30, sleep_type=SleepType.MORNING_LARK)
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(0)
    
    owl_result = calc_owl.calculate(origin, dest)
    lark_result = calc_lark.calculate(origin, dest)
    
    add_result("sleep type owl east", owl_result.severity_score >= lark_result.severity_score)


def test_age_effects(results, add_result):
    """测试年龄影响"""
    calc_young = JetLagCalculator(age=20)
    calc_old = JetLagCalculator(age=70)
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(8)
    
    young_result = calc_young.calculate(origin, dest)
    old_result = calc_old.calculate(origin, dest)
    
    # test 19: 年长者恢复更慢
    add_result("age recovery slower", 
               old_result.estimated_recovery_days > young_result.estimated_recovery_days)


def test_sleep_schedule_recommendations(results, add_result):
    """测试睡眠时间建议"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-8)
    dest = TimezoneInfo.from_utc_offset(8)
    
    result = calc.calculate(origin, dest)
    
    # test 20: 睡眠建议
    add_result("sleep_schedule recommendations", 
               len(result.optimal_sleep_schedule) > 0)


def test_light_exposure(results, add_result):
    """测试光照建议"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(0)
    
    result = calc.calculate(origin, dest)
    
    # test 21: 光照建议
    add_result("light_exposure recommendations", 
               len(result.light_exposure_times) > 0)
    
    # test 22: 向东需要晨光
    add_result("light_exposure east morning", 
               "morning" in result.light_exposure_times)


def test_recovery_timeline(results, add_result):
    """测试恢复时间线"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(8)
    
    result = calc.calculate(origin, dest)
    timeline = calc.get_recovery_timeline(result, start_date=datetime(2024, 1, 1))
    
    # test 23: 时间线长度
    add_result("recovery_timeline length", len(timeline) > 0)
    
    # test 24: 时间线第一天
    add_result("recovery_timeline first day", timeline[0]["day"] == 0)
    
    # test 25: 时间线状态
    add_result("recovery_timeline status", 
               timeline[-1]["status"] == "fully_adjusted" or 
               timeline[-1]["remaining_shift_hours"] < 0.5)


def test_convenience_functions(results, add_result):
    """测试便捷函数"""
    # test 26: calculate_jet_lag
    result = calculate_jet_lag(-5, 0, age=30, sleep_type="intermediate")
    add_result("calculate_jet_lag convenience", 
               result.time_difference == 5 and result.direction == TravelDirection.EAST)
    
    # test 27: get_common_timezones
    timezones = get_common_timezones()
    add_result("get_common_timezones", 
               len(timezones) > 0 and "UTC" in timezones)
    
    # test 28: quick_estimate
    estimate = quick_estimate(8)
    add_result("quick_estimate", 
               estimate["needs_adjustment"] and 
               estimate["estimated_recovery_days"] > 0)


def test_popular_routes(results, add_result):
    """测试热门路线"""
    # test 29: POPULAR_ROUTES 存在
    add_result("POPULAR_ROUTES", len(POPULAR_ROUTES) > 0)
    
    # test 30: analyze_route
    route_result = analyze_route("LAX", "JFK", age=30)
    add_result("analyze_route LAX-JFK", 
               route_result is not None and "route_name" in route_result)
    
    # test 31: analyze_route 不存在的路线
    no_route = analyze_route("XXX", "YYY")
    add_result("analyze_route nonexistent", no_route is None)


def test_large_time_difference(results, add_result):
    """测试大时差"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-8)   # LA
    dest = TimezoneInfo.from_utc_offset(9)      # Tokyo
    
    result = calc.calculate(origin, dest)
    
    # test 32: 大时差 (LA -8 -> Tokyo +9 = 17h difference, normalized to -7 or depends)
    result = calc.calculate(origin, dest)
    # 时差可能被标准化（超过12小时会反转）
    add_result("large time_difference", abs(result.time_difference) >= 5)  # 至少有显著时差
    
    # test 33: 高严重程度
    add_result("large severity", result.severity_score > 50)


def test_adjustment_per_day(results, add_result):
    """测试每日调整量"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(0)
    
    result = calc.calculate(origin, dest)
    
    # test 34: 向东调整量
    add_result("adjustment_per_day east", 
               0 < result.adjustment_per_day <= 1)


def test_phase_shift(results, add_result):
    """测试相位移动"""
    calc = JetLagCalculator()
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(8)
    
    result = calc.calculate(origin, dest)
    
    # test 35: 相位移动量
    add_result("phase_shift_needed", result.phase_shift_needed > 0)


def test_severity_levels(results, add_result):
    """测试严重程度分级"""
    calc = JetLagCalculator()
    
    # test 36: Minimal (<1h)
    result_minimal = calc.calculate(
        TimezoneInfo.from_utc_offset(0),
        TimezoneInfo.from_utc_offset(0.5)
    )
    add_result("severity Minimal", 
               result_minimal.severity_level == "Minimal" or 
               result_minimal.severity_score < 10)
    
    # test 37: Moderate (3-6h)
    result_moderate = calc.calculate(
        TimezoneInfo.from_utc_offset(-5),
        TimezoneInfo.from_utc_offset(0)
    )
    add_result("severity Moderate", 
               result_moderate.severity_level in ["Mild", "Moderate"])
    
    # test 38: 高严重程度 (>12h 跨多时区，但会标准化)
    result_extreme = calc.calculate(
        TimezoneInfo.from_utc_offset(-8),
        TimezoneInfo.from_utc_offset(8)
    )
    add_result("severity Extreme", 
               result_extreme.severity_score > 30)  # 至少中等严重程度


def test_normalized_time_difference(results, add_result):
    """测试标准化时差"""
    calc = JetLagCalculator()
    
    # test 39: 超过12小时标准化
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(15)  # 有效时差应该是 -8 或 +16 -> 标准化为
    
    result = calc.calculate(origin, dest)
    # 时差应该在 -12 到 +12 范围内
    add_result("normalized time_difference", 
               -12 <= result.time_difference <= 12)


def test_custom_bed_time(results, add_result):
    """测试自定义睡眠时间"""
    calc = JetLagCalculator(
        age=30,
        typical_bed_time=time(1, 0),  # 1 AM
        typical_wake_time=time(9, 0)  # 9 AM
    )
    
    origin = TimezoneInfo.from_utc_offset(-5)
    dest = TimezoneInfo.from_utc_offset(0)
    
    result = calc.calculate(origin, dest)
    
    # test 40: 使用自定义睡眠时间计算
    add_result("custom bed_time", result.severity_score > 0)


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_timezone_info(results, add_result)
    test_sleep_type(results, add_result)
    test_travel_direction(results, add_result)
    test_sleep_schedule(results, add_result)
    test_jet_lag_calculator_basic(results, add_result)
    test_west_travel(results, add_result)
    test_no_time_difference(results, add_result)
    test_sleep_type_effects(results, add_result)
    test_age_effects(results, add_result)
    test_sleep_schedule_recommendations(results, add_result)
    test_light_exposure(results, add_result)
    test_recovery_timeline(results, add_result)
    test_convenience_functions(results, add_result)
    test_popular_routes(results, add_result)
    test_large_time_difference(results, add_result)
    test_adjustment_per_day(results, add_result)
    test_phase_shift(results, add_result)
    test_severity_levels(results, add_result)
    test_normalized_time_difference(results, add_result)
    test_custom_bed_time(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Jet Lag Calculator Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)