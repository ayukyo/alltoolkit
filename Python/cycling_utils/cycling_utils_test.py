#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cycling Utils Test - 自行车工具测试

测试模块：cycling_utils
测试用例数：45+
测试覆盖：速度/距离/时间计算、功率估算、卡路里、齿轮比、爬坡指标、训练指标
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CyclingUtils, CyclingResult, GearConfig, RiderProfile,
    TerrainType, RidingPosition,
    calculate_speed, calculate_time, calculate_distance,
    calculate_power, calculate_calories, calculate_gear_ratio,
    calculate_speed_from_cadence
)
from datetime import datetime


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


def test_speed_distance_time(results, add_result):
    """测试速度、距离、时间计算"""
    # test 1: 基础速度计算
    cycling = CyclingUtils()
    result = cycling.calculate_speed(100, 5)  # 100km in 5h
    add_result("calculate_speed basic", result.value == 20.0, f"Expected 20, got {result.value}")
    
    # test 2: 零时间异常
    try:
        cycling.calculate_speed(100, 0)
        add_result("calculate_speed zero_time exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_speed zero_time exception", True)
    
    # test 3: 负时间异常
    try:
        cycling.calculate_speed(100, -1)
        add_result("calculate_speed negative_time exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_speed negative_time exception", True)
    
    # test 4: 时间计算
    result = cycling.calculate_time(100, 20)  # 100km at 20km/h
    add_result("calculate_time basic", result.value == 5.0, f"Expected 5, got {result.value}")
    
    # test 5: 零速度异常
    try:
        cycling.calculate_time(100, 0)
        add_result("calculate_time zero_speed exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_time zero_speed exception", True)
    
    # test 6: 距离计算
    result = cycling.calculate_distance(20, 5)  # 20km/h for 5h
    add_result("calculate_distance basic", result.value == 100.0, f"Expected 100, got {result.value}")
    
    # test 7: 便捷函数
    speed = calculate_speed(60, 2)
    add_result("calculate_speed convenience", speed == 30.0, f"Expected 30, got {speed}")
    
    time_val = calculate_time(60, 30)
    add_result("calculate_time convenience", time_val == 2.0, f"Expected 2, got {time_val}")
    
    dist = calculate_distance(30, 2)
    add_result("calculate_distance convenience", dist == 60.0, f"Expected 60, got {dist}")


def test_pace_conversion(results, add_result):
    """测试配速转换"""
    cycling = CyclingUtils()
    
    # test 8: 配速转速度
    result = cycling.pace_to_speed(6)  # 6 min/km = 10 km/h
    add_result("pace_to_speed basic", result.value == 10.0, f"Expected 10, got {result.value}")
    
    # test 9: 速度转配速
    result = cycling.speed_to_pace(10)  # 10 km/h = 6 min/km
    add_result("speed_to_pace basic", result.value == 6.0, f"Expected 6, got {result.value}")
    
    # test 10: 双向转换一致性
    speed = 25.0
    pace = cycling.speed_to_pace(speed).value
    back_speed = cycling.pace_to_speed(pace).value
    add_result("pace_speed consistency", abs(speed - back_speed) < 0.01, f"Expected {speed}, got {back_speed}")
    
    # test 11: 零配速异常
    try:
        cycling.pace_to_speed(0)
        add_result("pace_to_speed zero exception", False, "Should raise ValueError")
    except ValueError:
        add_result("pace_to_speed zero exception", True)


def test_power_calculations(results, add_result):
    """测试功率计算"""
    rider = RiderProfile(weight_kg=75)
    cycling = CyclingUtils(rider=rider, bike_weight_kg=10)
    
    # test 12: 平路功率估算
    result = cycling.calculate_power(30, gradient_percent=0)
    add_result("calculate_power flat", result.value > 0, f"Expected positive power")
    
    # test 13: 爬坡功率更高
    flat_power = cycling.calculate_power(20, gradient_percent=0).value
    climb_power = cycling.calculate_power(20, gradient_percent=5).value
    add_result("calculate_power climbing higher", climb_power > flat_power * 2, 
               f"Climb {climb_power} should be much higher than flat {flat_power}")
    
    # test 14: 风速影响
    no_wind = cycling.calculate_power(25, wind_speed_kmh=0).value
    headwind = cycling.calculate_power(25, wind_speed_kmh=15).value
    add_result("calculate_power headwind", headwind > no_wind, 
               f"Headwind {headwind} > no wind {no_wind}")
    
    # test 15: 不同骑行姿势
    tops = cycling.calculate_power(30, riding_position=RidingPosition.TOPS).value
    drops = cycling.calculate_power(30, riding_position=RidingPosition.DROPS).value
    add_result("calculate_power position", tops > drops, 
               f"Tops {tops} > drops {drops} (more drag)")
    
    # test 16: 从功率估算速度
    power = 200
    result = cycling.estimate_speed_from_power(power, gradient_percent=0)
    add_result("estimate_speed_from_power", result.value > 0, f"Expected positive speed")
    
    # test 17: 功率体重比
    result = cycling.calculate_power_to_weight_ratio(250)
    expected = 250 / 75  # ~3.33 W/kg
    add_result("power_to_weight_ratio", abs(result.value - expected) < 0.01, 
               f"Expected {expected}, got {result.value}")


def test_calories(results, add_result):
    """测试卡路里计算"""
    cycling = CyclingUtils()
    
    # test 18: 基础卡路里计算
    result = cycling.calculate_calories(200, 1)  # 200W for 1h
    add_result("calculate_calories basic", result.value > 0, f"Expected positive calories")
    
    # test 19: 卡路里与功率成正比
    cal1 = cycling.calculate_calories(100, 1).value
    cal2 = cycling.calculate_calories(200, 1).value
    add_result("calculate_calories proportional", cal2 > cal1 * 1.5, 
               f"Higher power should burn more calories")
    
    # test 20: 卡路里与时间成正比
    cal1 = cycling.calculate_calories(200, 1).value
    cal2 = cycling.calculate_calories(200, 2).value
    add_result("calculate_calories time proportional", abs(cal2 - cal1 * 2) < 1, 
               f"Expected ~{cal1*2}, got {cal2}")
    
    # test 21: 无 rider 时心率卡路里异常
    try:
        cycling.estimate_calories_from_hr(150, 1)
        add_result("estimate_calories_from_hr no rider exception", False, "Should raise ValueError")
    except ValueError:
        add_result("estimate_calories_from_hr no rider exception", True)
    
    # test 22: 有 rider 的心率卡路里估算
    rider = RiderProfile(weight_kg=70, age_years=30, gender='male')
    cycling2 = CyclingUtils(rider=rider)
    result = cycling2.estimate_calories_from_hr(140, 1)
    add_result("estimate_calories_from_hr with rider", result.value > 0, f"Expected positive calories")


def test_gear_calculations(results, add_result):
    """测试齿轮计算"""
    cycling = CyclingUtils()
    
    # test 23: 齿轮比计算
    result = cycling.calculate_gear_ratio(50, 11)  # 50T front, 11T rear
    add_result("calculate_gear_ratio", abs(result.value - 50/11) < 0.01, 
               f"Expected ~4.55, got {result.value}")
    
    # test 24: 大齿轮比更高
    ratio1 = cycling.calculate_gear_ratio(50, 28).value
    ratio2 = cycling.calculate_gear_ratio(50, 11).value
    add_result("calculate_gear_ratio larger", ratio2 > ratio1, 
               f"Smaller rear = larger ratio")
    
    # test 25: 齿轮比为零异常
    try:
        cycling.calculate_gear_ratio(50, 0)
        add_result("calculate_gear_ratio zero exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_gear_ratio zero exception", True)
    
    # test 26: Development 计算
    result = cycling.calculate_development(50, 11)
    add_result("calculate_development", result.value > 0, f"Expected positive development")
    
    # test 27: 从踏频计算速度
    result = cycling.calculate_speed_from_cadence(90, 50, 11)
    add_result("calculate_speed_from_cadence", result.value > 30, 
               f"Expected high speed with big gear, got {result.value}")
    
    # test 28: 从速度计算踏频
    speed = cycling.calculate_speed_from_cadence(90, 50, 11).value
    result = cycling.calculate_cadence_from_speed(speed, 50, 11)
    add_result("calculate_cadence_from_speed", abs(result.value - 90) < 1, 
               f"Expected ~90, got {result.value}")
    
    # test 29: 所有齿轮比
    ratios = cycling.get_all_gear_ratios()
    add_result("get_all_gear_ratios", len(ratios) > 0, f"Expected some gear ratios")


def test_climbing_metrics(results, add_result):
    """测试爬坡指标"""
    cycling = CyclingUtils()
    
    # test 30: 坡度计算
    result = cycling.calculate_gradient(10, 500)  # 10km, 500m elevation
    expected = 5.0  # 5%
    add_result("calculate_gradient", abs(result.value - expected) < 0.1, 
               f"Expected ~5%, got {result.value}")
    
    # test 31: 海拔增益计算
    result = cycling.calculate_elevation_gain(10, 5)  # 10km at 5%
    expected = 500  # 500m
    add_result("calculate_elevation_gain", abs(result.value - expected) < 1, 
               f"Expected ~500m, got {result.value}")
    
    # test 32: VAM 计算
    result = cycling.calculate_vam(1000, 1)  # 1000m in 1h
    add_result("calculate_vam", result.value == 1000, f"Expected 1000, got {result.value}")
    
    # test 33: 爬坡难度评分
    result = cycling.calculate_climbing_difficulty(10, 500)
    add_result("calculate_climbing_difficulty", result.value > 0, f"Expected positive score")
    
    # test 34: 零距离异常
    try:
        cycling.calculate_gradient(0, 100)
        add_result("calculate_gradient zero exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_gradient zero exception", True)


def test_training_metrics(results, add_result):
    """测试训练指标"""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    cycling = CyclingUtils(rider=rider)
    
    # test 35: NP 计算
    power_samples = [200, 210, 220, 230, 240, 250] * 10  # 60 samples
    result = cycling.calculate_np(power_samples)
    add_result("calculate_np", result.value > 0, f"Expected positive NP")
    
    # test 36: NP 样本数不足异常
    try:
        cycling.calculate_np([100] * 10)  # Only 10 samples
        add_result("calculate_np insufficient samples exception", False, "Should raise ValueError")
    except ValueError:
        add_result("calculate_np insufficient samples exception", True)
    
    # test 37: TSS 计算
    result = cycling.calculate_tss(250, 1)  # NP = FTP for 1h
    expected = 100  # 1h at FTP = 100 TSS
    add_result("calculate_tss", abs(result.value - expected) < 5, 
               f"Expected ~100, got {result.value}")
    
    # test 38: IF 计算
    result = cycling.calculate_if(300, ftp=250)
    expected = 300 / 250  # 1.2
    add_result("calculate_if", abs(result.value - expected) < 0.01, 
               f"Expected {expected}, got {result.value}")
    
    # test 39: 训练区间 (200W / 250W FTP = 0.8 -> zone 3: 0.75-0.90)
    zone, name, desc = cycling.get_training_zone(200)
    add_result("get_training_zone", zone == 3, f"Expected zone 3 (Tempo), got {zone}")
    
    # test 40: 无 FTP 时训练区间异常
    cycling_noftp = CyclingUtils(rider=RiderProfile(weight_kg=75))
    try:
        cycling_noftp.get_training_zone(200)
        add_result("get_training_zone no ftp exception", False, "Should raise ValueError")
    except ValueError:
        add_result("get_training_zone no ftp exception", True)


def test_gear_config(results, add_result):
    """测试齿轮配置"""
    # test 41: 自定义齿轮配置
    config = GearConfig(
        front_teeth=[53, 39],
        rear_teeth=[11, 12, 13, 14, 15, 17, 19, 21, 23, 25],
        crank_length_mm=175,
        wheel_diameter_mm=622,
        tire_width_mm=28
    )
    cycling = CyclingUtils(gear_config=config)
    add_result("GearConfig custom", cycling.gear_config.front_teeth == [53, 39])
    
    # test 42: 所有 development
    developments = cycling.get_all_developments()
    add_result("get_all_developments", len(developments) > 0, f"Expected some developments")


def test_rider_profile(results, add_result):
    """测试骑手档案"""
    rider = RiderProfile(
        weight_kg=80,
        height_cm=180,
        age_years=35,
        gender='male',
        ftp_watts=280
    )
    cycling = CyclingUtils(rider=rider)
    
    # test 43: 总重量
    expected = 80 + 8.5  # rider + bike default
    add_result("total_weight", cycling.total_weight == expected, 
               f"Expected {expected}, got {cycling.total_weight}")
    
    # test 44: 自行车重量
    cycling2 = CyclingUtils(rider=rider, bike_weight_kg=10)
    expected2 = 90
    add_result("bike_weight", cycling2.total_weight == expected2, 
               f"Expected {expected2}, got {cycling2.total_weight}")


def test_enums(results, add_result):
    """测试枚举类型"""
    # test 45: TerrainType
    add_result("TerrainType values", 
               TerrainType.FLAT.value == "flat" and TerrainType.HILLY.value == "hilly")
    
    # test 46: RidingPosition
    add_result("RidingPosition values", 
               RidingPosition.DROPS.value == "drops" and RidingPosition.AERO.value == "aero")


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_speed_distance_time(results, add_result)
    test_pace_conversion(results, add_result)
    test_power_calculations(results, add_result)
    test_calories(results, add_result)
    test_gear_calculations(results, add_result)
    test_climbing_metrics(results, add_result)
    test_training_metrics(results, add_result)
    test_gear_config(results, add_result)
    test_rider_profile(results, add_result)
    test_enums(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Cycling Utils Test Results")
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