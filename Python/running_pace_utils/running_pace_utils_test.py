"""
Running Pace Utilities - 测试套件

覆盖：
- 配速计算（距离+时间 → 配速）
- 时间预测（距离+配速 → 时间）
- 距离计算（时间+配速 → 距离）
- 单位转换（距离/配速）
- 分段计时表
- 比赛预测（Riegel 公式）
- VDOT 跑力值计算
- 年龄分级
- 训练区间
- 跑步经济性
- 比赛配速表
- 间歇训练配速
- 分段预测
- 坡度调整配速
"""

import sys
import os
import math

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 枚举和常量
    DistanceUnit, PaceUnit, RACE_DISTANCES,
    # 数据类
    PaceResult, SplitTime, RacePrediction, TrainingZone,
    # 核心函数
    convert_distance, convert_pace,
    calculate_pace, calculate_time, calculate_distance,
    generate_splits, predict_race_time,
    calculate_vdot, calculate_age_grade,
    calculate_training_zones, calculate_running_economy,
    generate_race_pace_table, calculate_interval_pace,
    estimate_finish_time_from_splits, calculate_grade_adjusted_pace,
    # 便捷函数
    pace_to_speed, speed_to_pace, format_pace, format_time,
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
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望: {expected}\n  实际: {actual}")
    
    def assert_almost_equal(self, actual, expected, delta=0.01, msg=""):
        if abs(actual - expected) <= delta:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"近似断言失败: {msg}\n  期望: {expected}±{delta}\n  实际: {actual}")
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}")
    
    def assert_raises(self, exception_type, func, msg=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"预期异常但未抛出: {msg}")
        except exception_type:
            self.passed += 1
        except Exception as e:
            self.failed += 1
            self.errors.append(f"抛出了错误的异常类型: {msg}\n  预期: {exception_type}\n  实际: {type(e).__name__}")
    
    def summary(self):
        total = self.passed + self.failed
        status = "✅ 通过" if self.failed == 0 else f"❌ 失败 {self.failed} 个"
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed}/{total} 通过 - {status}")
        print('='*60)
        if self.errors:
            for err in self.errors[:10]:  # 只显示前 10 个错误
                print(f"\n{err}")
            if len(self.errors) > 10:
                print(f"\n... 还有 {len(self.errors) - 10} 个错误")
        return self.failed == 0


def test_convert_distance():
    """测试距离单位转换"""
    r = TestResult()
    print("\n测试: 距离单位转换")
    
    # 公里转英里
    r.assert_almost_equal(
        convert_distance(1.0, DistanceUnit.KILOMETERS, DistanceUnit.MILES),
        0.621371, delta=0.001, msg="1 km → miles"
    )
    
    # 英里转公里
    r.assert_almost_equal(
        convert_distance(1.0, DistanceUnit.MILES, DistanceUnit.KILOMETERS),
        1.609344, delta=0.001, msg="1 mile → km"
    )
    
    # 米转公里
    r.assert_equal(
        convert_distance(1000, DistanceUnit.METERS, DistanceUnit.KILOMETERS),
        1.0, msg="1000m → km"
    )
    
    # 码转公里
    r.assert_almost_equal(
        convert_distance(1760, DistanceUnit.YARDS, DistanceUnit.KILOMETERS),
        1.609344, delta=0.01, msg="1760 yards → km (约1英里)"
    )
    
    return r


def test_convert_pace():
    """测试配速单位转换"""
    r = TestResult()
    print("\n测试: 配速单位转换")
    
    # min/km → min/mile
    r.assert_almost_equal(
        convert_pace(5.0, PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_MILE),
        8.0467, delta=0.01, msg="5 min/km → min/mile"
    )
    
    # min/mile → min/km
    r.assert_almost_equal(
        convert_pace(8.0, PaceUnit.MIN_PER_MILE, PaceUnit.MIN_PER_KM),
        4.9709, delta=0.01, msg="8 min/mile → min/km"
    )
    
    # min/km → km/h
    r.assert_almost_equal(
        convert_pace(5.0, PaceUnit.MIN_PER_KM, PaceUnit.KM_PER_HOUR),
        12.0, delta=0.01, msg="5 min/km → km/h"
    )
    
    # km/h → min/km
    r.assert_almost_equal(
        convert_pace(12.0, PaceUnit.KM_PER_HOUR, PaceUnit.MIN_PER_KM),
        5.0, delta=0.01, msg="12 km/h → min/km"
    )
    
    # mph → km/h
    r.assert_almost_equal(
        convert_pace(6.0, PaceUnit.MILE_PER_HOUR, PaceUnit.KM_PER_HOUR),
        9.66, delta=0.1, msg="6 mph → km/h"
    )
    
    return r


def test_calculate_pace():
    """测试配速计算"""
    r = TestResult()
    print("\n测试: 配速计算")
    
    # 10km 用时 50 分钟
    result = calculate_pace(10, 50 * 60, DistanceUnit.KILOMETERS)
    r.assert_almost_equal(result.pace_min_per_km, 5.0, delta=0.01, msg="10km/50min 配速")
    r.assert_almost_equal(result.speed_kmh, 12.0, delta=0.1, msg="10km/50min 速度")
    
    # 马拉松 3小时
    result = calculate_pace(42195, 3 * 3600, DistanceUnit.METERS)
    r.assert_almost_equal(result.pace_min_per_km, 4.26, delta=0.02, msg="马拉松3小时 配速")
    
    # 1英里 6分钟
    result = calculate_pace(1, 6 * 60, DistanceUnit.MILES)
    r.assert_almost_equal(result.pace_min_per_km, 3.73, delta=0.02, msg="1mile/6min 配速")
    
    # 错误输入
    r.assert_raises(ValueError, lambda: calculate_pace(0, 60), msg="距离为0应报错")
    r.assert_raises(ValueError, lambda: calculate_pace(10, 0), msg="时间为0应报错")
    
    return r


def test_calculate_time():
    """测试时间计算"""
    r = TestResult()
    print("\n测试: 时间计算")
    
    # 10km @ 5:00/km
    time = calculate_time(10, 5.0, DistanceUnit.KILOMETERS, PaceUnit.MIN_PER_KM)
    r.assert_equal(time, 50 * 60, msg="10km @ 5:00/km 时间")
    
    # 马拉松 @ 4:30/km
    time = calculate_time(42.195, 4.5, DistanceUnit.KILOMETERS, PaceUnit.MIN_PER_KM)
    r.assert_almost_equal(time, 189.8775 * 60, delta=1, msg="马拉松@4:30/km 时间")
    
    # 使用 km/h 单位
    time = calculate_time(10, 12.0, DistanceUnit.KILOMETERS, PaceUnit.KM_PER_HOUR)
    r.assert_equal(time, 50 * 60, msg="10km @ 12km/h 时间")
    
    # 错误输入
    r.assert_raises(ValueError, lambda: calculate_time(0, 5.0), msg="距离为0应报错")
    r.assert_raises(ValueError, lambda: calculate_time(10, 0), msg="配速为0应报错")
    
    return r


def test_calculate_distance():
    """测试距离计算"""
    r = TestResult()
    print("\n测试: 距离计算")
    
    # 50分钟 @ 5:00/km
    distance = calculate_distance(50 * 60, 5.0, PaceUnit.MIN_PER_KM, DistanceUnit.KILOMETERS)
    r.assert_equal(distance, 10.0, msg="50min @ 5:00/km 距离")
    
    # 60分钟 @ 10km/h
    distance = calculate_distance(60 * 60, 10.0, PaceUnit.KM_PER_HOUR, DistanceUnit.KILOMETERS)
    r.assert_equal(distance, 10.0, msg="60min @ 10km/h 距离")
    
    # 返回英里
    distance = calculate_distance(60 * 60, 10.0, PaceUnit.KM_PER_HOUR, DistanceUnit.MILES)
    r.assert_almost_equal(distance, 6.21, delta=0.01, msg="60min @ 10km/h 返回英里")
    
    return r


def test_generate_splits():
    """测试分段计时表"""
    r = TestResult()
    print("\n测试: 分段计时表")
    
    # 10km 50分钟，每公里分段
    splits = generate_splits(10, 50 * 60, 1.0)
    r.assert_equal(len(splits), 10, msg="10km 应有 10 个分段")
    r.assert_equal(splits[-1].distance, 10.0, msg="最后分段距离")
    r.assert_equal(splits[-1].cumulative_time, 50 * 60, msg="累计时间")
    
    # 5km 25分钟，每英里分段
    splits = generate_splits(5, 25 * 60, 1.609344)
    r.assert_true(len(splits) > 0, msg="英里分段应生成")
    
    # 边界情况
    splits = generate_splits(0, 60, 1.0)
    r.assert_equal(len(splits), 0, msg="距离为0应返回空列表")
    
    splits = generate_splits(10, 0, 1.0)
    r.assert_equal(len(splits), 0, msg="时间为0应返回空列表")
    
    # 非整数分段
    splits = generate_splits(7.5, 37.5 * 60, 1.0)
    r.assert_equal(len(splits), 8, msg="7.5km 应有 8 个分段（最后不足1km）")
    
    return r


def test_predict_race_time():
    """测试比赛预测（Riegel 公式）"""
    r = TestResult()
    print("\n测试: 比赛预测")
    
    # 基于 10km 40分钟预测马拉松
    pred = predict_race_time(42.195, 40 * 60, 10)
    r.assert_true(pred.predicted_time > 2.5 * 3600, msg="马拉松预测应大于 2.5 小时")
    r.assert_true(pred.predicted_time < 3.5 * 3600, msg="马拉松预测应小于 3.5 小时")
    
    # 基于 5km 20分钟预测 10km
    pred = predict_race_time(10, 20 * 60, 5)
    r.assert_true(pred.predicted_time > 40 * 60, msg="10km 预测应大于 40 分钟")
    r.assert_true(pred.predicted_time < 45 * 60, msg="10km 预测应小于 45 分钟")
    
    # 检查格式化输出
    r.assert_true(":" in pred.predicted_time_formatted, msg="时间应格式化")
    r.assert_true("/km" in pred.pace_formatted, msg="配速应格式化")
    
    # 错误输入
    r.assert_raises(ValueError, lambda: predict_race_time(0, 60, 10), msg="距离为0应报错")
    r.assert_raises(ValueError, lambda: predict_race_time(10, 0, 10), msg="时间为0应报错")
    
    return r


def test_calculate_vdot():
    """测试 VDOT 跑力值计算"""
    r = TestResult()
    print("\n测试: VDOT 计算")
    
    # 5km 20分钟（约 VDOT 60+，精英水平）
    vdot = calculate_vdot(5, 20 * 60)
    r.assert_true(vdot > 55, msg="5km 20min VDOT 应大于 55")
    r.assert_true(vdot < 70, msg="5km 20min VDOT 应小于 70")
    
    # 5km 25分钟（中等水平）
    vdot = calculate_vdot(5, 25 * 60)
    r.assert_true(vdot > 40, msg="5km 25min VDOT 应大于 40")
    r.assert_true(vdot < 55, msg="5km 25min VDOT 应小于 55")
    
    # 马拉松 3小时（良好水平）
    vdot = calculate_vdot(42.195, 3 * 3600)
    r.assert_true(vdot > 55, msg="马拉松 3h VDOT 应大于 55")
    r.assert_true(vdot < 65, msg="马拉松 3h VDOT 应小于 65")
    
    # 边界情况
    vdot = calculate_vdot(0, 60)
    r.assert_equal(vdot, 0.0, msg="距离为0应返回0")
    
    return r


def test_calculate_age_grade():
    """测试年龄分级"""
    r = TestResult()
    print("\n测试: 年龄分级")
    
    # 30岁男性，10km 40分钟
    factor, percent = calculate_age_grade(40 * 60, 10, 30, "M")
    r.assert_true(factor > 0.9, msg="30岁年龄系数应大于 0.9")
    r.assert_true(percent > 50, msg="年龄分级百分比应大于 50")
    
    # 60岁男性，10km 50分钟
    factor, percent = calculate_age_grade(50 * 60, 10, 60, "M")
    r.assert_true(factor < 0.8, msg="60岁年龄系数应小于 0.8")
    
    # 25岁（最高系数）
    factor, percent = calculate_age_grade(40 * 60, 10, 25, "M")
    r.assert_almost_equal(factor, 0.99, delta=0.01, msg="25岁年龄系数")
    
    # 年龄小于20
    factor, percent = calculate_age_grade(40 * 60, 10, 18, "M")
    r.assert_equal(factor, 1.0, msg="18岁年龄系数应为 1.0")
    
    return r


def test_calculate_training_zones():
    """测试训练区间计算"""
    r = TestResult()
    print("\n测试: 训练区间")
    
    zones = calculate_training_zones(180, 4.5)  # 最大心率 180，阈值配速 4:30/km
    
    r.assert_equal(len(zones), 5, msg="应有 5 个训练区间")
    
    # Zone 1 应该是最轻松的
    r.assert_equal(zones[0].zone, 1, msg="第一个区间应为 Zone 1")
    r.assert_true(zones[0].hr_max <= zones[1].hr_min + 10, msg="Zone 1 心率接近 Zone 2")
    
    # Zone 5 应该是最难的
    r.assert_equal(zones[4].zone, 5, msg="最后一个区间应为 Zone 5")
    
    # 检查心率范围
    r.assert_true(zones[0].hr_min >= 90, msg="Zone 1 心率下限")
    r.assert_true(zones[4].hr_max <= 180, msg="Zone 5 心率上限不应超过最大心率")
    
    # Zone 1 配速应该比 Zone 5 慢（min/km 数字更大）
    r.assert_true(
        zones[0].pace_min_per_km[1] > zones[4].pace_min_per_km[0],
        msg="Zone 1 配速应比 Zone 5 慢"
    )
    
    return r


def test_calculate_running_economy():
    """测试跑步经济性计算"""
    r = TestResult()
    print("\n测试: 跑步经济性")
    
    # 10km 40分钟，体重 70kg
    eco = calculate_running_economy(10, 40 * 60, 70)
    
    r.assert_almost_equal(eco["speed_kmh"], 15.0, delta=0.1, msg="速度 15 km/h")
    r.assert_true(eco["vo2_ml_kg_min"] > 30, msg="VO2 应大于 30")
    r.assert_true(eco["total_kcal"] > 300, msg="总消耗应大于 300 kcal")
    r.assert_true(eco["kcal_per_km"] > 50, msg="每公里消耗应大于 50 kcal")
    
    # 带 VO2max
    eco = calculate_running_economy(10, 40 * 60, 70, vo2max=55)
    r.assert_true("intensity_percent_vo2max" in eco, msg="应有相对强度")
    r.assert_true(eco["intensity_percent_vo2max"] > 50, msg="相对强度应大于 50%")
    
    # 边界情况
    eco = calculate_running_economy(0, 60, 70)
    r.assert_equal(len(eco), 0, msg="距离为0应返回空字典")
    
    return r


def test_generate_race_pace_table():
    """测试比赛配速表生成"""
    r = TestResult()
    print("\n测试: 比赛配速表")
    
    # 马拉松 3:30 目标
    table = generate_race_pace_table(42.195, 210)
    
    r.assert_equal(table["distance_km"], 42.195, msg="距离")
    r.assert_equal(table["target_time_minutes"], 210, msg="目标时间")
    r.assert_true(len(table["km_splits"]) > 0, msg="应有公里分段")
    r.assert_true(len(table["mile_splits"]) > 0, msg="应有英里分段")
    
    # 检查最后一个分段
    last_split = table["km_splits"][-1]
    r.assert_almost_equal(last_split["km"], 42.195, delta=0.1, msg="最后分段距离")
    
    # 5km 20分钟
    table = generate_race_pace_table(5, 20)
    r.assert_equal(len(table["km_splits"]), 5, msg="5km 应有 5 个分段")
    
    # 边界情况
    table = generate_race_pace_table(0, 60)
    r.assert_equal(len(table), 0, msg="距离为0应返回空字典")
    
    return r


def test_calculate_interval_pace():
    """测试间歇训练配速"""
    r = TestResult()
    print("\n测试: 间歇训练配速")
    
    paces = calculate_interval_pace(4.5, "threshold")  # 目标 4:30/km
    
    r.assert_true(len(paces) > 5, msg="应有多种训练类型配速")
    
    # 重复跑应该最快（配速数字最小）
    r.assert_true(
        paces["repetition"]["pace_min_per_km"] < paces["easy"]["pace_min_per_km"],
        msg="重复跑应比轻松跑快（配速数字更小）"
    )
    
    # 恢复跑应该最慢（配速数字最大）
    r.assert_true(
        paces["recovery"]["pace_min_per_km"] > paces["easy"]["pace_min_per_km"],
        msg="恢复跑应比轻松跑慢（配速数字更大）"
    )
    
    # 阈值跑应接近目标
    r.assert_almost_equal(
        paces["threshold"]["pace_min_per_km"], 4.5, delta=0.1,
        msg="阈值跑配速应接近目标"
    )
    
    # 边界情况
    paces = calculate_interval_pace(0, "threshold")
    r.assert_equal(len(paces), 0, msg="配速为0应返回空字典")
    
    return r


def test_estimate_finish_time_from_splits():
    """测试基于分段预测完赛时间"""
    r = TestResult()
    print("\n测试: 分段预测完赛时间")
    
    # 已完成 5km，用时 25 分钟，预测 10km
    splits = [(1, 5 * 60), (1, 5 * 60), (1, 5 * 60), (1, 5 * 60), (1, 5 * 60)]
    result = estimate_finish_time_from_splits(splits, 10)
    
    r.assert_equal(result["status"], "in_progress", msg="状态应为进行中")
    r.assert_equal(result["completed_distance_km"], 5.0, msg="已完成距离")
    r.assert_equal(result["remaining_distance_km"], 5.0, msg="剩余距离")
    r.assert_true("predicted_total_time" in result, msg="应有预测总时间")
    r.assert_equal(result["progress_percent"], 50.0, msg="进度应为 50%")
    
    # 已完成全程
    splits = [(10, 50 * 60)]
    result = estimate_finish_time_from_splits(splits, 10)
    r.assert_equal(result["status"], "finished", msg="状态应为已完成")
    
    # 边界情况
    result = estimate_finish_time_from_splits([], 10)
    r.assert_equal(len(result), 0, msg="空分段应返回空字典")
    
    result = estimate_finish_time_from_splits([(5, 25 * 60)], 0)
    r.assert_equal(len(result), 0, msg="总距离为0应返回空字典")
    
    return r


def test_calculate_grade_adjusted_pace():
    """测试坡度调整配速"""
    r = TestResult()
    print("\n测试: 坡度调整配速")
    
    # 平地（0% 坡度）
    gap = calculate_grade_adjusted_pace(5.0, 0)
    r.assert_almost_equal(gap, 5.0, delta=0.01, msg="平地 GAP 应等于实际配速")
    
    # 上坡 5%
    gap = calculate_grade_adjusted_pace(5.0, 5)
    r.assert_true(gap < 5.0, msg="上坡 GAP 应小于实际配速（等效更快）")
    
    # 下坡 5%
    gap = calculate_grade_adjusted_pace(5.0, -5)
    r.assert_true(gap > 5.0, msg="下坡 GAP 应大于实际配速（等效更慢）")
    
    # 极陡上坡
    gap = calculate_grade_adjusted_pace(5.0, 20)
    r.assert_true(gap < 4.0, msg="20% 上坡 GAP 应明显更小")
    
    # 极陡下坡（有下限）
    gap = calculate_grade_adjusted_pace(5.0, -50)
    r.assert_true(gap > 5.0, msg="极陡下坡 GAP 应更大")
    
    # 边界情况
    gap = calculate_grade_adjusted_pace(0, 5)
    r.assert_equal(gap, 0.0, msg="配速为0应返回0")
    
    return r


def test_convenience_functions():
    """测试便捷函数"""
    r = TestResult()
    print("\n测试: 便捷函数")
    
    # pace_to_speed
    r.assert_almost_equal(pace_to_speed(5.0), 12.0, delta=0.01, msg="5:00/km → 12 km/h")
    r.assert_almost_equal(pace_to_speed(6.0), 10.0, delta=0.01, msg="6:00/km → 10 km/h")
    r.assert_equal(pace_to_speed(0), 0.0, msg="配速为0应返回0")
    
    # speed_to_pace
    r.assert_almost_equal(speed_to_pace(12.0), 5.0, delta=0.01, msg="12 km/h → 5:00/km")
    r.assert_almost_equal(speed_to_pace(10.0), 6.0, delta=0.01, msg="10 km/h → 6:00/km")
    r.assert_true(math.isinf(speed_to_pace(0)), msg="速度为0应返回无穷")
    
    # format_pace
    r.assert_equal(format_pace(5.5), "5:30/km", msg="格式化配速 5:30/km")
    r.assert_equal(format_pace(4.25), "4:15/km", msg="格式化配速 4:15/km")
    r.assert_equal(format_pace(0), "N/A", msg="配速为0应返回 N/A")
    r.assert_equal(format_pace(-1), "N/A", msg="负配速应返回 N/A")
    
    # format_time
    r.assert_equal(format_time(90), "1:30", msg="格式化时间 90秒")
    r.assert_equal(format_time(3661), "1:01:01", msg="格式化时间 1小时")
    r.assert_equal(format_time(-1), "N/A", msg="负时间应返回 N/A")
    
    return r


def test_race_distances():
    """测试标准比赛距离"""
    r = TestResult()
    print("\n测试: 标准比赛距离")
    
    # 检查标准距离
    r.assert_equal(RACE_DISTANCES["100m"], 100, msg="100m 距离")
    r.assert_equal(RACE_DISTANCES["marathon"], 42195, msg="马拉松距离")
    r.assert_almost_equal(RACE_DISTANCES["mile"], 1609.344, delta=0.001, msg="1英里距离")
    
    # 马拉松 2:30 预测
    pred = predict_race_time(42.195, 2.5 * 3600, 42.195)
    r.assert_almost_equal(pred.predicted_time, 2.5 * 3600, delta=1, msg="马拉松距离相同时间应一致")
    
    return r


def test_edge_cases():
    """测试边界情况"""
    r = TestResult()
    print("\n测试: 边界情况")
    
    # 极短距离
    result = calculate_pace(0.1, 10, DistanceUnit.KILOMETERS)
    r.assert_almost_equal(result.pace_min_per_km, 1.67, delta=0.01, msg="100m 配速")
    
    # 极慢配速
    time = calculate_time(1, 30, DistanceUnit.KILOMETERS, PaceUnit.MIN_PER_KM)
    r.assert_equal(time, 30 * 60, msg="极慢配速时间")
    
    # 极快配速
    result = calculate_pace(1.609344, 240, DistanceUnit.KILOMETERS)  # 1英里 4分钟
    r.assert_true(result.speed_kmh > 20, msg="极快配速速度")
    
    # 非常长的比赛
    result = calculate_pace(100, 10 * 3600, DistanceUnit.KILOMETERS)  # 100km 10小时
    r.assert_almost_equal(result.pace_min_per_km, 6.0, delta=0.01, msg="100km 配速")
    
    return r


def test_data_classes():
    """测试数据类"""
    r = TestResult()
    print("\n测试: 数据类")
    
    # PaceResult
    pace = PaceResult(
        pace_min_per_km=5.0,
        pace_min_per_mile=8.05,
        speed_kmh=12.0,
        speed_mph=7.46,
        time_seconds=1800,
        distance_km=6.0
    )
    r.assert_equal(pace.pace_min_per_km, 5.0, msg="PaceResult 配速")
    r.assert_equal(pace.distance_km, 6.0, msg="PaceResult 距离")
    
    # SplitTime
    split = SplitTime(
        distance=1.0,
        cumulative_time=300,
        split_time=300,
        pace_min_per_km=5.0
    )
    r.assert_equal(split.distance, 1.0, msg="SplitTime 距离")
    r.assert_equal(split.pace_min_per_km, 5.0, msg="SplitTime 配速")
    
    # RacePrediction
    pred = RacePrediction(
        distance="5km",
        distance_km=5.0,
        predicted_time=1200,
        predicted_time_formatted="20:00",
        pace_min_per_km=4.0,
        pace_formatted="4:00/km"
    )
    r.assert_equal(pred.distance, "5km", msg="RacePrediction 距离名")
    r.assert_equal(pred.predicted_time_formatted, "20:00", msg="RacePrediction 格式化时间")
    
    return r


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Running Pace Utils - 测试套件")
    print("="*60)
    
    test_functions = [
        test_convert_distance,
        test_convert_pace,
        test_calculate_pace,
        test_calculate_time,
        test_calculate_distance,
        test_generate_splits,
        test_predict_race_time,
        test_calculate_vdot,
        test_calculate_age_grade,
        test_calculate_training_zones,
        test_calculate_running_economy,
        test_generate_race_pace_table,
        test_calculate_interval_pace,
        test_estimate_finish_time_from_splits,
        test_calculate_grade_adjusted_pace,
        test_convenience_functions,
        test_race_distances,
        test_edge_cases,
        test_data_classes,
    ]
    
    total_passed = 0
    total_failed = 0
    all_errors = []
    
    for test_func in test_functions:
        result = test_func()
        total_passed += result.passed
        total_failed += result.failed
        all_errors.extend(result.errors)
    
    # 总结
    total = total_passed + total_failed
    status = "✅ 全部通过" if total_failed == 0 else f"❌ 失败 {total_failed} 个"
    print(f"\n{'='*60}")
    print(f"总测试结果: {total_passed}/{total} 通过 - {status}")
    print('='*60)
    
    if all_errors:
        print(f"\n错误详情 ({len(all_errors)} 个):")
        for err in all_errors[:20]:
            print(f"\n{err}")
        if len(all_errors) > 20:
            print(f"\n... 还有 {len(all_errors) - 20} 个错误")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)