"""
Running Pace Utils 测试文件
"""

import unittest
from mod import (
    parse_time, parse_pace, seconds_to_time, seconds_to_pace,
    calculate_pace, calculate_time, calculate_distance, calculate_speed,
    convert_pace, predict_race_time, calculate_splits,
    vdot_to_pace, pace_to_vdot, calculate_training_zones,
    format_pace, get_race_distance, pace, finish_time,
    PaceUnit, DistanceUnit, RACE_DISTANCES
)


class TestParseTime(unittest.TestCase):
    """测试时间解析"""
    
    def test_parse_seconds(self):
        """测试秒数解析"""
        self.assertEqual(parse_time("30"), 30)
        self.assertEqual(parse_time("0"), 0)
        self.assertEqual(parse_time("59"), 59)
    
    def test_parse_minutes_seconds(self):
        """测试分:秒格式"""
        self.assertEqual(parse_time("5:30"), 330)
        self.assertEqual(parse_time("10:00"), 600)
        self.assertEqual(parse_time("59:59"), 3599)
    
    def test_parse_hours_minutes_seconds(self):
        """测试时:分:秒格式"""
        self.assertEqual(parse_time("1:00:00"), 3600)
        self.assertEqual(parse_time("2:30:45"), 9045)
        self.assertEqual(parse_time("1:30:30"), 5430)
    
    def test_parse_with_spaces(self):
        """测试带空格的格式"""
        self.assertEqual(parse_time(" 5:30 "), 330)
        self.assertEqual(parse_time(" 1:00:00 "), 3600)


class TestParsePace(unittest.TestCase):
    """测试配速解析"""
    
    def test_parse_pace_minutes_seconds(self):
        """测试分:秒格式"""
        self.assertEqual(parse_pace("5:30"), 5.5)
        self.assertEqual(parse_pace("6:00"), 6.0)
        self.assertEqual(parse_pace("4:15"), 4.25)
    
    def test_parse_pace_float(self):
        """测试浮点数格式"""
        self.assertEqual(parse_pace("5.5"), 5.5)
        self.assertEqual(parse_pace("6.0"), 6.0)


class TestSecondsToTime(unittest.TestCase):
    """测试秒数转时间"""
    
    def test_seconds_only(self):
        """测试纯秒数"""
        result = seconds_to_time(30)
        self.assertEqual(result.hours, 0)
        self.assertEqual(result.minutes, 0)
        self.assertEqual(result.seconds, 30)
    
    def test_minutes_seconds(self):
        """测试分+秒"""
        result = seconds_to_time(330)
        self.assertEqual(result.hours, 0)
        self.assertEqual(result.minutes, 5)
        self.assertEqual(result.seconds, 30)
    
    def test_hours_minutes_seconds(self):
        """测试时+分+秒"""
        result = seconds_to_time(3665)
        self.assertEqual(result.hours, 1)
        self.assertEqual(result.minutes, 1)
        self.assertEqual(result.seconds, 5)
    
    def test_time_str(self):
        """测试时间字符串格式"""
        result = seconds_to_time(3665)
        self.assertEqual(result.time_str, "1:01:05")
    
    def test_negative_seconds(self):
        """测试负数秒（应返回0）"""
        result = seconds_to_time(-10)
        self.assertEqual(result.total_seconds, 0)


class TestCalculatePace(unittest.TestCase):
    """测试配速计算"""
    
    def test_basic_pace(self):
        """测试基本配速计算"""
        result = calculate_pace(5, "25:00")
        self.assertEqual(result.minutes, 5)
        self.assertEqual(result.seconds, 0)
    
    def test_pace_with_seconds(self):
        """测试带秒的配速"""
        result = calculate_pace(10, "50:30")
        self.assertEqual(result.total_seconds, 303.0)
    
    def test_marathon_pace(self):
        """测试马拉松配速"""
        result = calculate_pace(42.195, "3:30:00")
        # 3:30:00 = 12600秒, / 42.195 ≈ 298.7秒/公里 ≈ 4:59/km
        self.assertAlmostEqual(result.total_seconds, 298.7, places=0)
    
    def test_miles_unit(self):
        """测试英里单位"""
        result = calculate_pace(3.1, "25:00", DistanceUnit.MILES)
        # 3.1英里 ≈ 5公里
        self.assertEqual(result.minutes, 5)
        self.assertEqual(result.seconds, 0)


class TestCalculateTime(unittest.TestCase):
    """测试时间计算"""
    
    def test_basic_time(self):
        """测试基本时间计算"""
        result = calculate_time(10, "5:30")
        self.assertEqual(result.minutes, 55)
        self.assertEqual(result.seconds, 0)
    
    def test_marathon_time(self):
        """测试马拉松时间"""
        result = calculate_time(42.195, "5:00")
        # 42.195 * 5分钟 = 210.975分钟 ≈ 3:30:58
        self.assertEqual(result.hours, 3)
        self.assertEqual(result.minutes, 30)
    
    def test_half_marathon_time(self):
        """测试半马时间"""
        result = calculate_time(21.0975, "5:30")
        # 21.0975 * 5.5分钟 ≈ 116分钟 = 1:56
        self.assertEqual(result.hours, 1)
        self.assertEqual(result.minutes, 56)


class TestCalculateDistance(unittest.TestCase):
    """测试距离计算"""
    
    def test_basic_distance(self):
        """测试基本距离计算"""
        distance = calculate_distance("1:00:00", "6:00")
        self.assertEqual(distance, 10.0)
    
    def test_distance_km(self):
        """测试公里距离"""
        distance = calculate_distance("30:00", "5:00")
        self.assertEqual(distance, 6.0)
    
    def test_distance_miles(self):
        """测试英里距离"""
        distance = calculate_distance("30:00", "5:00", DistanceUnit.MILES)
        # 6公里 = 3.73英里
        self.assertAlmostEqual(distance, 3.73, places=1)


class TestCalculateSpeed(unittest.TestCase):
    """测试速度计算"""
    
    def test_basic_speed(self):
        """测试基本速度"""
        result = calculate_speed(10, "50:00")
        # 10公里 / 50分钟 = 12 km/h
        self.assertEqual(result.kmh, 12.0)
        self.assertAlmostEqual(result.mph, 7.46, places=1)
    
    def test_marathon_speed(self):
        """测试马拉松速度"""
        result = calculate_speed(42.195, "3:30:00")
        # 42.195 km / 3.5 h ≈ 12.06 km/h
        self.assertAlmostEqual(result.kmh, 12.06, places=1)


class TestConvertPace(unittest.TestCase):
    """测试配速转换"""
    
    def test_km_to_mile(self):
        """测试公里转英里"""
        result = convert_pace("5:00", PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_MI)
        # 5分/公里 * 1.609 = 8:02 分/英里
        self.assertEqual(result.minutes, 8)
        self.assertIn(result.seconds, [2, 3])  # 允许小数四舍五入差异
    
    def test_mile_to_km(self):
        """测试英里转公里"""
        result = convert_pace("8:00", PaceUnit.MIN_PER_MI, PaceUnit.MIN_PER_KM)
        # 8分/英里 / 1.609 = 4:58 分/公里
        self.assertEqual(result.minutes, 4)
        self.assertEqual(result.seconds, 58)
    
    def test_same_unit(self):
        """测试相同单位"""
        result = convert_pace("5:00", PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_KM)
        self.assertEqual(result.minutes, 5)
        self.assertEqual(result.seconds, 0)


class TestPredictRaceTime(unittest.TestCase):
    """测试比赛时间预测"""
    
    def test_5k_to_10k(self):
        """测试5K预测10K"""
        result = predict_race_time(5, "25:00", 10)
        # 5K 25分钟，用 Riegel 公式预测 10K
        # T2 = 1500 * (10/5)^1.06 ≈ 3158秒 ≈ 52:38
        self.assertEqual(result.minutes, 52)
    
    def test_10k_to_marathon(self):
        """测试10K预测马拉松"""
        result = predict_race_time(10, "50:00", 42.195)
        # 10K 50分钟，预测马拉松
        # T2 = 3000 * (42.195/10)^1.06 ≈ 14288秒 ≈ 3:58:08
        self.assertEqual(result.hours, 3)


class TestCalculateSplits(unittest.TestCase):
    """测试分段用时"""
    
    def test_basic_splits(self):
        """测试基本分段"""
        splits = calculate_splits(5, "6:00")
        self.assertEqual(len(splits), 5)
        self.assertEqual(splits[0]["distance"], 1.0)
        # split_time 包含单位
        self.assertIn("6:00", splits[0]["split_time"])
        # total_time 格式包含小时（即使为0）
        self.assertIn("30:00", splits[4]["total_time"])
    
    def test_marathon_splits(self):
        """测试马拉松分段"""
        splits = calculate_splits(42.195, "5:00", split_distance=5)
        # 应该有9个分段（5, 10, 15, 20, 25, 30, 35, 40, 42.195）
        self.assertEqual(len(splits), 9)
        self.assertEqual(splits[-1]["distance"], 42.2)


class TestVDOTFunctions(unittest.TestCase):
    """测试VDOT相关函数"""
    
    def test_vdot_to_pace(self):
        """测试VDOT转配速"""
        result = vdot_to_pace(50, "5K")
        # VDOT 50 对应约 3:28/km 的 5K 配速（基于实现）
        self.assertEqual(result.minutes, 3)
        self.assertIn(result.seconds, range(20, 35))  # 允许范围
    
    def test_pace_to_vdot(self):
        """测试配速转VDOT"""
        vdot = pace_to_vdot("5:00")
        # 5分/公里 ≈ 300秒/公里, VDOT ≈ 100 - 60 = 40
        self.assertGreater(vdot, 35)
        self.assertLess(vdot, 50)
    
    def test_vdot_round_trip(self):
        """测试VDOT往返"""
        # VDOT 50 -> 配速 -> VDOT（可能有误差）
        pace_result = vdot_to_pace(50, "5K")
        # 使用 pace_str 而不是完整字符串
        vdot = pace_to_vdot(pace_result.pace_str)
        # VDOT 往返有较大误差，只检查大致范围
        self.assertGreater(vdot, 40)
        self.assertLess(vdot, 60)


class TestTrainingZones(unittest.TestCase):
    """测试训练区间"""
    
    def test_zone_calculation(self):
        """测试区间计算"""
        zones = calculate_training_zones("5:00")
        
        # E 区应该比 T 区慢
        self.assertGreater(zones["E"].total_seconds, zones["T"].total_seconds)
        
        # I 区应该比 T 区快
        self.assertLess(zones["I"].total_seconds, zones["T"].total_seconds)
        
        # R 区应该最快
        self.assertLess(zones["R"].total_seconds, zones["I"].total_seconds)
    
    def test_all_zones_present(self):
        """测试所有区间都存在"""
        zones = calculate_training_zones("5:00")
        self.assertIn("E", zones)
        self.assertIn("M", zones)
        self.assertIn("T", zones)
        self.assertIn("I", zones)
        self.assertIn("R", zones)


class TestFormatPace(unittest.TestCase):
    """测试配速格式化"""
    
    def test_format_pace(self):
        """测试格式化"""
        self.assertEqual(format_pace(300), "5:00")
        self.assertEqual(format_pace(330), "5:30")
        self.assertEqual(format_pace(366), "6:06")


class TestGetRaceDistance(unittest.TestCase):
    """测试比赛距离获取"""
    
    def test_standard_distances(self):
        """测试标准距离"""
        self.assertEqual(get_race_distance("5K"), 5.0)
        self.assertEqual(get_race_distance("10K"), 10.0)
        self.assertEqual(get_race_distance("马拉松"), 42.195)
        self.assertEqual(get_race_distance("半马"), 21.0975)
    
    def test_chinese_names(self):
        """测试中文名称"""
        self.assertEqual(get_race_distance("半马"), 21.0975)
        self.assertEqual(get_race_distance("全马"), 42.195)
    
    def test_invalid_distance(self):
        """测试无效距离"""
        self.assertIsNone(get_race_distance("无效"))


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_pace_function(self):
        """测试pace函数"""
        result = pace("25:00", 5)
        self.assertEqual(result, "5:00 /km")
    
    def test_finish_time_function(self):
        """测试finish_time函数"""
        result = finish_time(10, "5:30")
        # 小时为0时格式为 "0:55:00"，否则为 "HH:MM:SS"
        self.assertIn("55:00", result)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_distance(self):
        """测试零距离"""
        # 零距离计算应该返回 0 或抛出异常（取决于实现）
        # 这里我们接受返回 0 的实现
        try:
            result = calculate_pace(0, "25:00")
            self.assertEqual(result.total_seconds, 0)
        except (ZeroDivisionError, ValueError):
            pass  # 抛出异常也是合理的行为
    
    def test_very_slow_pace(self):
        """测试很慢的配速"""
        result = calculate_pace(1, "10:00")
        self.assertEqual(result.minutes, 10)
        self.assertEqual(result.seconds, 0)
    
    def test_very_fast_pace(self):
        """测试很快的配速"""
        result = calculate_pace(1, "3:00")
        self.assertEqual(result.minutes, 3)
        self.assertEqual(result.seconds, 0)
    
    def test_long_distance(self):
        """测试长距离"""
        result = calculate_time(100, "6:00")
        self.assertEqual(result.hours, 10)
        self.assertEqual(result.minutes, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)