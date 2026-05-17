"""
Heart Rate Utils 测试文件

测试覆盖:
- 最大心率计算（多种公式）
- 心率区间计算
- Karvonen公式
- 燃脂区间计算
- 卡路里消耗估算
- 恢复心率评估
- 心血管健康评估
- 训练强度计算
- 乳酸阈值估算
- 配速估算
- 心率趋势分析
- 边界值测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    HeartRateUtils,
    MaxHrFormula,
    HeartRateZone,
    calculate_max_hr,
    get_zones,
    get_fat_burning_hr,
    get_current_zone,
    estimate_calories,
    assess_fitness
)


class TestResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add_pass(self, name: str):
        self.passed += 1
        self.results.append(("✅ PASS", name))
    
    def add_fail(self, name: str, error: str):
        self.failed += 1
        self.results.append(("❌ FAIL", name, error))
    
    def report(self):
        print("\n" + "=" * 60)
        print("测试结果报告")
        print("=" * 60)
        for r in self.results:
            if len(r) == 2:
                print(f"{r[0]}: {r[1]}")
            else:
                print(f"{r[0]}: {r[1]} - {r[2]}")
        print("=" * 60)
        print(f"总计: {self.passed} 通过, {self.failed} 失败")
        print("=" * 60)
        return self.failed == 0


def run_tests():
    collector = TestResultCollector()
    
    # ========== 最大心率计算测试 ==========
    
    # Test 1: Tanaka公式
    try:
        result = HeartRateUtils.calculate_max_hr(30, MaxHrFormula.TANAKA)
        expected = int(208 - 0.7 * 30)  # 187
        assert result == expected, f"Tanaka公式结果应为{expected}"
        collector.add_pass("Tanaka公式 - 30岁")
    except Exception as e:
        collector.add_fail("Tanaka公式 - 30岁", str(e))
    
    # Test 2: Tanaka公式 - 50岁
    try:
        result = HeartRateUtils.calculate_max_hr(50, MaxHrFormula.TANAKA)
        expected = int(208 - 0.7 * 50)  # 173
        assert result == expected
        collector.add_pass("Tanaka公式 - 50岁")
    except Exception as e:
        collector.add_fail("Tanaka公式 - 50岁", str(e))
    
    # Test 3: 传统公式
    try:
        result = HeartRateUtils.calculate_max_hr(30, MaxHrFormula.STANDARD)
        expected = 220 - 30  # 190
        assert result == expected
        collector.add_pass("传统公式 (220-age) - 30岁")
    except Exception as e:
        collector.add_fail("传统公式 (220-age) - 30岁", str(e))
    
    # Test 4: Gellish公式
    try:
        result = HeartRateUtils.calculate_max_hr(40, MaxHrFormula.GELLISH)
        expected = int(207 - 0.7 * 40)  # 179
        assert result == expected
        collector.add_pass("Gellish公式 - 40岁")
    except Exception as e:
        collector.add_fail("Gellish公式 - 40岁", str(e))
    
    # Test 5: Arena公式
    try:
        result = HeartRateUtils.calculate_max_hr(25, MaxHrFormula.ARENA)
        expected = int(209.3 - 0.72 * 25)  # 191
        assert result == expected
        collector.add_pass("Arena公式 - 25岁")
    except Exception as e:
        collector.add_fail("Arena公式 - 25岁", str(e))
    
    # Test 6: Inbar公式
    try:
        result = HeartRateUtils.calculate_max_hr(35, MaxHrFormula.INBAR)
        expected = int(205.8 - 0.685 * 35)  # 182
        assert result == expected
        collector.add_pass("Inbar公式 - 35岁")
    except Exception as e:
        collector.add_fail("Inbar公式 - 35岁", str(e))
    
    # Test 7: NES公式
    try:
        result = HeartRateUtils.calculate_max_hr(45, MaxHrFormula.NES)
        expected = int(211 - 0.64 * 45)  # 182
        assert result == expected
        collector.add_pass("NES公式 - 45岁")
    except Exception as e:
        collector.add_fail("NES公式 - 45岁", str(e))
    
    # Test 8: Gellish二次公式
    try:
        result = HeartRateUtils.calculate_max_hr(30, MaxHrFormula.GELLISH2)
        expected = int(192 - 0.007 * 30 * 30)  # 185
        assert result == expected
        collector.add_pass("Gellish二次公式 - 30岁")
    except Exception as e:
        collector.add_fail("Gellish二次公式 - 30岁", str(e))
    
    # Test 9: 平均最大心率
    try:
        result = HeartRateUtils.calculate_max_hr_average(30)
        # 多公式平均应该接近187左右
        assert 180 <= result <= 195
        collector.add_pass("平均最大心率 - 30岁")
    except Exception as e:
        collector.add_fail("平均最大心率 - 30岁", str(e))
    
    # Test 10: 最大心率范围（所有公式）
    try:
        result = HeartRateUtils.calculate_max_hr_range(30)
        assert "tanaka" in result
        assert "standard" in result
        assert "average" in result
        assert len(result) == 8
        collector.add_pass("最大心率范围 - 所有公式")
    except Exception as e:
        collector.add_fail("最大心率范围 - 所有公式", str(e))
    
    # ========== 年龄边界测试 ==========
    
    # Test 11: 最小年龄 (1岁)
    try:
        result = HeartRateUtils.calculate_max_hr(1, MaxHrFormula.TANAKA)
        expected = int(208 - 0.7)  # 207
        assert result == expected
        collector.add_pass("最小年龄 (1岁)")
    except Exception as e:
        collector.add_fail("最小年龄 (1岁)", str(e))
    
    # Test 12: 最大年龄 (120岁)
    try:
        result = HeartRateUtils.calculate_max_hr(120, MaxHrFormula.TANAKA)
        expected = int(208 - 0.7 * 120)  # 124
        assert result == expected
        collector.add_pass("最大年龄 (120岁)")
    except Exception as e:
        collector.add_fail("最大年龄 (120岁)", str(e))
    
    # Test 13: 无效年龄 (0岁)
    try:
        HeartRateUtils.calculate_max_hr(0, MaxHrFormula.TANAKA)
        collector.add_fail("无效年龄 (0岁)", "应抛出异常")
    except ValueError:
        collector.add_pass("无效年龄 (0岁) - 正确抛出异常")
    except Exception as e:
        collector.add_fail("无效年龄 (0岁)", f"异常类型错误: {e}")
    
    # Test 14: 无效年龄 (121岁)
    try:
        HeartRateUtils.calculate_max_hr(121, MaxHrFormula.TANAKA)
        collector.add_fail("无效年龄 (121岁)", "应抛出异常")
    except ValueError:
        collector.add_pass("无效年龄 (121岁) - 正确抛出异常")
    except Exception as e:
        collector.add_fail("无效年龄 (121岁)", f"异常类型错误: {e}")
    
    # ========== 心率储备计算测试 ==========
    
    # Test 15: 心率储备计算
    try:
        result = HeartRateUtils.calculate_heart_rate_reserve(190, 60)
        expected = 190 - 60  # 130
        assert result == expected
        collector.add_pass("心率储备计算")
    except Exception as e:
        collector.add_fail("心率储备计算", str(e))
    
    # Test 16: 心率储备 - 静息心率等于最大心率
    try:
        HeartRateUtils.calculate_heart_rate_reserve(180, 180)
        collector.add_fail("心率储备 - 静息等于最大", "应抛出异常")
    except ValueError:
        collector.add_pass("心率储备 - 静息等于最大 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("心率储备 - 静息等于最大", f"异常类型错误: {e}")
    
    # Test 17: 心率储备 - 静息心率过低
    try:
        HeartRateUtils.calculate_heart_rate_reserve(180, 25)
        collector.add_fail("心率储备 - 静息过低", "应抛出异常")
    except ValueError:
        collector.add_pass("心率储备 - 静息过低 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("心率储备 - 静息过低", f"异常类型错误: {e}")
    
    # ========== Karvonen公式测试 ==========
    
    # Test 18: Karvonen目标心率
    try:
        result = HeartRateUtils.calculate_target_hr_karvonen(190, 60, 0.7)
        hrr = 190 - 60  # 130
        expected = int(130 * 0.7 + 60)  # 151
        assert result == expected
        collector.add_pass("Karvonen目标心率 - 70%强度")
    except Exception as e:
        collector.add_fail("Karvonen目标心率 - 70%强度", str(e))
    
    # Test 19: Karvonen - 低强度 (50%)
    try:
        result = HeartRateUtils.calculate_target_hr_karvonen(190, 60, 0.5)
        hrr = 130
        expected = int(130 * 0.5 + 60)  # 125
        assert result == expected
        collector.add_pass("Karvonen目标心率 - 50%强度")
    except Exception as e:
        collector.add_fail("Karvonen目标心率 - 50%强度", str(e))
    
    # Test 20: Karvonen - 高强度 (95%)
    try:
        result = HeartRateUtils.calculate_target_hr_karvonen(190, 60, 0.95)
        hrr = 130
        expected = int(130 * 0.95 + 60)  # 184
        assert result == expected
        collector.add_pass("Karvonen目标心率 - 95%强度")
    except Exception as e:
        collector.add_fail("Karvonen目标心率 - 95%强度", str(e))
    
    # Test 21: Karvonen - 无效强度 (低于50%)
    try:
        HeartRateUtils.calculate_target_hr_karvonen(190, 60, 0.4)
        collector.add_fail("Karvonen无效强度", "应抛出异常")
    except ValueError:
        collector.add_pass("Karvonen无效强度 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("Karvonen无效强度", f"异常类型错误: {e}")
    
    # ========== 简单百分比公式测试 ==========
    
    # Test 22: 简单百分比目标心率
    try:
        result = HeartRateUtils.calculate_target_hr_simple(190, 0.7)
        expected = int(190 * 0.7)  # 133
        assert result == expected
        collector.add_pass("简单百分比目标心率 - 70%")
    except Exception as e:
        collector.add_fail("简单百分比目标心率 - 70%", str(e))
    
    # ========== 心率区间测试 ==========
    
    # Test 23: 心率区间计算 - 30岁
    try:
        result = HeartRateUtils.calculate_zones(30)
        assert result.max_hr == 187  # Tanaka
        assert "Zone 1" in result.zones
        assert "Zone 2" in result.zones
        assert "Zone 5" in result.zones
        collector.add_pass("心率区间计算 - 30岁")
    except Exception as e:
        collector.add_fail("心率区间计算 - 30岁", str(e))
    
    # Test 24: Zone 1 心率范围
    try:
        result = HeartRateUtils.calculate_zones(30)
        zone1 = result.zones["Zone 1"]
        # 187 * 50% = 93, 187 * 60% = 112
        assert zone1.hr_range.min_hr == 93
        assert zone1.hr_range.max_hr == 112
        collector.add_pass("Zone 1 心率范围验证")
    except Exception as e:
        collector.add_fail("Zone 1 心率范围验证", str(e))
    
    # Test 25: Zone 2 心率范围 (燃脂区间)
    try:
        result = HeartRateUtils.calculate_zones(30)
        zone2 = result.zones["Zone 2"]
        # 187 * 60% = 112, 187 * 70% = 130
        assert zone2.hr_range.min_hr == 112
        assert zone2.hr_range.max_hr == 130
        assert zone2.name == "有氧基础"
        collector.add_pass("Zone 2 心率范围验证")
    except Exception as e:
        collector.add_fail("Zone 2 心率范围验证", str(e))
    
    # Test 26: Zone 5 心率范围
    try:
        result = HeartRateUtils.calculate_zones(30)
        zone5 = result.zones["Zone 5"]
        # 187 * 90% = 168, 187 * 100% = 187
        assert zone5.hr_range.min_hr == 168
        assert zone5.hr_range.max_hr == 187
        collector.add_pass("Zone 5 心率范围验证")
    except Exception as e:
        collector.add_fail("Zone 5 心率范围验证", str(e))
    
    # Test 27: Karvonen区间计算
    try:
        result = HeartRateUtils.calculate_zones(30, resting_hr=60, use_karvonen=True)
        assert result.heart_rate_reserve == 127  # 187 - 60
        zone1 = result.zones["Zone 1"]
        # 127 * 50% + 60 = 123, 127 * 60% + 60 = 136
        assert zone1.hr_range.min_hr == 123
        assert zone1.hr_range.max_hr == 136
        collector.add_pass("Karvonen区间计算")
    except Exception as e:
        collector.add_fail("Karvonen区间计算", str(e))
    
    # Test 28: 区间信息完整性
    try:
        result = HeartRateUtils.calculate_zones(30)
        zone1 = result.zones["Zone 1"]
        assert zone1.zone.value == "Zone 1"
        assert zone1.description != ""
        assert len(zone1.benefits) > 0
        assert zone1.percentage_range == (50, 60)
        collector.add_pass("区间信息完整性")
    except Exception as e:
        collector.add_fail("区间信息完整性", str(e))
    
    # ========== 获取当前区间测试 ==========
    
    # Test 29: 获取当前区间 - Zone 2
    try:
        zone = HeartRateUtils.get_zone_for_hr(120, 30)  # 30岁，120 bpm
        assert zone is not None
        assert zone.zone.value == "Zone 2"
        collector.add_pass("获取当前区间 - Zone 2")
    except Exception as e:
        collector.add_fail("获取当前区间 - Zone 2", str(e))
    
    # Test 30: 获取当前区间 - Zone 5
    try:
        zone = HeartRateUtils.get_zone_for_hr(180, 30)  # 30岁，180 bpm
        assert zone is not None
        assert zone.zone.value == "Zone 5"
        collector.add_pass("获取当前区间 - Zone 5")
    except Exception as e:
        collector.add_fail("获取当前区间 - Zone 5", str(e))
    
    # Test 31: 获取当前区间 - 超出范围
    try:
        zone = HeartRateUtils.get_zone_for_hr(50, 30)  # 低于所有区间
        assert zone is None
        collector.add_pass("获取当前区间 - 低于所有区间")
    except Exception as e:
        collector.add_fail("获取当前区间 - 低于所有区间", str(e))
    
    # Test 32: 获取当前区间 - 高于所有区间
    try:
        zone = HeartRateUtils.get_zone_for_hr(200, 30)  # 超过最大心率
        assert zone is None
        collector.add_pass("获取当前区间 - 高于所有区间")
    except Exception as e:
        collector.add_fail("获取当前区间 - 高于所有区间", str(e))
    
    # ========== 燃脂区间测试 ==========
    
    # Test 33: 燃脂区间计算
    try:
        result = HeartRateUtils.calculate_fat_burning_zone(30)
        assert result["percentage"] == (60, 70)
        assert result["zone_name"] == "有氧基础"
        assert "hr_range" in result
        collector.add_pass("燃脂区间计算")
    except Exception as e:
        collector.add_fail("燃脂区间计算", str(e))
    
    # Test 34: 燃脂区间最佳心率
    try:
        result = HeartRateUtils.calculate_fat_burning_zone(30)
        # (93 + 112) / 2 不对，应该是 Zone 2 的中间值
        # Zone 2: 112-130，中间值约121
        optimal = result["optimal_hr"]
        assert 110 <= optimal <= 135
        collector.add_pass("燃脂区间最佳心率")
    except Exception as e:
        collector.add_fail("燃脂区间最佳心率", str(e))
    
    # ========== 有氧区间测试 ==========
    
    # Test 35: 有氧区间计算
    try:
        result = HeartRateUtils.calculate_cardio_zone(30)
        assert result["percentage"] == (70, 80)
        assert "hr_range" in result
        collector.add_pass("有氧区间计算")
    except Exception as e:
        collector.add_fail("有氧区间计算", str(e))
    
    # ========== 无氧区间测试 ==========
    
    # Test 36: 无氧区间计算
    try:
        result = HeartRateUtils.calculate_anaerobic_zone(30)
        assert result["percentage"] == (80, 90)
        assert "hr_range" in result
        collector.add_pass("无氧区间计算")
    except Exception as e:
        collector.add_fail("无氧区间计算", str(e))
    
    # ========== 卡路里消耗测试 ==========
    
    # Test 37: 卡路里消耗 - 男性
    try:
        result = HeartRateUtils.estimate_calories_burned(150, 45, 70, 30, "male")
        assert result["calories"] > 0
        assert result["average_hr"] == 150
        assert result["duration_minutes"] == 45
        collector.add_pass("卡路里消耗 - 男性")
    except Exception as e:
        collector.add_fail("卡路里消耗 - 男性", str(e))
    
    # Test 38: 卡路里消耗 - 女性
    try:
        result = HeartRateUtils.estimate_calories_burned(140, 30, 55, 25, "female")
        assert result["calories"] > 0
        collector.add_pass("卡路里消耗 - 女性")
    except Exception as e:
        collector.add_fail("卡路里消耗 - 女性", str(e))
    
    # Test 39: 卡路里消耗 - 极低心率
    try:
        result = HeartRateUtils.estimate_calories_burned(80, 60, 70, 30, "male")
        assert result["intensity"] == "极轻"
        assert result["calories"] > 0
        collector.add_pass("卡路里消耗 - 极低心率")
    except Exception as e:
        collector.add_fail("卡路里消耗 - 极低心率", str(e))
    
    # Test 40: 卡路里消耗 - 高心率
    try:
        result = HeartRateUtils.estimate_calories_burned(180, 20, 70, 30, "male")
        assert result["intensity"] in ["极高强度", "高强度"]
        collector.add_pass("卡路里消耗 - 高心率")
    except Exception as e:
        collector.add_fail("卡路里消耗 - 高心率", str(e))
    
    # Test 41: 卡路里消耗 - 无效性别
    try:
        HeartRateUtils.estimate_calories_burned(150, 45, 70, 30, "unknown")
        collector.add_fail("卡路里消耗 - 无效性别", "应抛出异常")
    except ValueError:
        collector.add_pass("卡路里消耗 - 无效性别 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("卡路里消耗 - 无效性别", f"异常类型错误: {e}")
    
    # ========== 恢复心率测试 ==========
    
    # Test 42: 恢复心率 - 优秀
    try:
        result = HeartRateUtils.calculate_recovery_hr(160, 130)  # 下降30
        assert result["hr_drop_1min"] == 30
        assert result["recovery_rating"] == "优秀"
        assert result["health_risk"] == "低风险"
        collector.add_pass("恢复心率 - 优秀")
    except Exception as e:
        collector.add_fail("恢复心率 - 优秀", str(e))
    
    # Test 43: 恢复心率 - 良好
    try:
        result = HeartRateUtils.calculate_recovery_hr(160, 142)  # 下降18
        assert result["hr_drop_1min"] == 18
        assert result["recovery_rating"] == "良好"
        collector.add_pass("恢复心率 - 良好")
    except Exception as e:
        collector.add_fail("恢复心率 - 良好", str(e))
    
    # Test 44: 恢复心率 - 一般
    try:
        result = HeartRateUtils.calculate_recovery_hr(160, 148)  # 下降12
        assert result["hr_drop_1min"] == 12
        assert result["recovery_rating"] == "一般"
        collector.add_pass("恢复心率 - 一般")
    except Exception as e:
        collector.add_fail("恢复心率 - 一般", str(e))
    
    # Test 45: 恢复心率 - 较差
    try:
        result = HeartRateUtils.calculate_recovery_hr(160, 155)  # 下降5
        assert result["hr_drop_1min"] == 5
        assert result["recovery_rating"] == "较差"
        collector.add_pass("恢复心率 - 较差")
    except Exception as e:
        collector.add_fail("恢复心率 - 较差", str(e))
    
    # Test 46: 恢复心率 - 2分钟数据
    try:
        result = HeartRateUtils.calculate_recovery_hr(160, 140, 120)
        assert result["hr_drop_1min"] == 20
        assert result["hr_drop_2min"] == 40
        assert result["rating_2min"] == "优秀"
        collector.add_pass("恢复心率 - 2分钟数据")
    except Exception as e:
        collector.add_fail("恢复心率 - 2分钟数据", str(e))
    
    # ========== 心血管健康评估测试 ==========
    
    # Test 47: 男性 - 运动员级别 (45 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(45, 30, "male")
        assert result["fitness_level"] == "运动员级别"
        assert result["rating"] == "优秀"
        collector.add_pass("男性 - 运动员级别静息心率")
    except Exception as e:
        collector.add_fail("男性 - 运动员级别静息心率", str(e))
    
    # Test 48: 男性 - 优秀 (55 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(55, 30, "male")
        assert result["fitness_level"] == "优秀"
        collector.add_pass("男性 - 优秀静息心率")
    except Exception as e:
        collector.add_fail("男性 - 优秀静息心率", str(e))
    
    # Test 49: 男性 - 良好 (65 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(65, 30, "male")
        assert result["fitness_level"] == "良好"
        collector.add_pass("男性 - 良好静息心率")
    except Exception as e:
        collector.add_fail("男性 - 良好静息心率", str(e))
    
    # Test 50: 男性 - 一般 (75 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(75, 30, "male")
        assert result["fitness_level"] == "一般"
        collector.add_pass("男性 - 一般静息心率")
    except Exception as e:
        collector.add_fail("男性 - 一般静息心率", str(e))
    
    # Test 51: 男性 - 较差 (95 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(95, 30, "male")
        assert result["fitness_level"] == "较差"
        collector.add_pass("男性 - 较差静息心率")
    except Exception as e:
        collector.add_fail("男性 - 较差静息心率", str(e))
    
    # Test 52: 女性 - 运动员级别 (50 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(50, 30, "female")
        assert result["fitness_level"] == "运动员级别"
        collector.add_pass("女性 - 运动员级别静息心率")
    except Exception as e:
        collector.add_fail("女性 - 运动员级别静息心率", str(e))
    
    # Test 53: 女性 - 良好 (70 bpm)
    try:
        result = HeartRateUtils.assess_cardiovascular_fitness(70, 30, "female")
        assert result["fitness_level"] == "良好"
        collector.add_pass("女性 - 良好静息心率")
    except Exception as e:
        collector.add_fail("女性 - 良好静息心率", str(e))
    
    # ========== 训练强度计算测试 ==========
    
    # Test 54: 训练强度计算
    try:
        result = HeartRateUtils.calculate_training_intensity(140, 30)
        assert result["current_hr"] == 140
        assert result["max_hr"] == 187
        assert result["percentage_of_max"] > 0
        assert result["intensity_level"] != ""
        collector.add_pass("训练强度计算")
    except Exception as e:
        collector.add_fail("训练强度计算", str(e))
    
    # Test 55: 训练强度 - Karvonen百分比
    try:
        result = HeartRateUtils.calculate_training_intensity(140, 30, resting_hr=60)
        assert result["karvonen_percentage"] is not None
        # (140-60)/127 ≈ 63%
        assert 60 <= result["karvonen_percentage"] <= 70
        collector.add_pass("训练强度 - Karvonen百分比")
    except Exception as e:
        collector.add_fail("训练强度 - Karvonen百分比", str(e))
    
    # Test 56: 训练强度 - 超过最大心率
    try:
        HeartRateUtils.calculate_training_intensity(200, 30)
        collector.add_fail("训练强度 - 超过最大心率", "应抛出异常")
    except ValueError:
        collector.add_pass("训练强度 - 超过最大心率 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("训练强度 - 超过最大心率", f"异常类型错误: {e}")
    
    # Test 57: 训练强度 - 颜色编码
    try:
        result_light = HeartRateUtils.calculate_training_intensity(100, 30)
        assert result_light["color_code"] == "蓝色"  # 轻度
        
        result_high = HeartRateUtils.calculate_training_intensity(170, 30)
        assert result_high["color_code"] in ["橙色", "红色"]
        collector.add_pass("训练强度 - 颜色编码")
    except Exception as e:
        collector.add_fail("训练强度 - 颜色编码", str(e))
    
    # ========== 乳酸阈值测试 ==========
    
    # Test 58: 乳酸阈值 - 百分比法
    try:
        result = HeartRateUtils.calculate_lactate_threshold_hr(30)
        assert result["lactate_threshold_range"]["min"] == int(187 * 0.85)  # 159
        assert result["lactate_threshold_range"]["max"] == int(187 * 0.90)  # 168
        collector.add_pass("乳酸阈值 - 百分比法")
    except Exception as e:
        collector.add_fail("乳酸阈值 - 百分比法", str(e))
    
    # Test 59: 乳酸阈值 - 公式法
    try:
        result = HeartRateUtils.calculate_lactate_threshold_hr(30, method="formula")
        assert result["lactate_threshold_range"]["min"] == int(187 * 0.83)  # 155
        assert result["lactate_threshold_range"]["max"] == int(187 * 0.88)  # 165
        collector.add_pass("乳酸阈值 - 公式法")
    except Exception as e:
        collector.add_fail("乳酸阈值 - 公式法", str(e))
    
    # ========== 配速估算测试 ==========
    
    # Test 60: 跑步配速估算 - 高心率
    try:
        result = HeartRateUtils.hr_to_pace_estimate(180, 30, 70, "running")
        assert result["activity"] == "跑步"
        assert result["intensity"] == "冲刺"
        assert result["estimated_pace_min_per_km"] <= 5
        collector.add_pass("跑步配速估算 - 高心率")
    except Exception as e:
        collector.add_fail("跑步配速估算 - 高心率", str(e))
    
    # Test 61: 跑步配速估算 - 低心率
    try:
        result = HeartRateUtils.hr_to_pace_estimate(100, 30, 70, "running")
        assert result["intensity"] in ["恢复跑", "热身/冷身", "轻松跑"]
        collector.add_pass("跑步配速估算 - 低心率")
    except Exception as e:
        collector.add_fail("跑步配速估算 - 低心率", str(e))
    
    # Test 62: 骑行速度估算
    try:
        result = HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "cycling")
        assert result["activity"] == "骑行"
        assert result["estimated_speed_kmh"] > 0
        collector.add_pass("骑行速度估算")
    except Exception as e:
        collector.add_fail("骑行速度估算", str(e))
    
    # Test 63: 游泳配速估算
    try:
        result = HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "swimming")
        assert result["activity"] == "游泳"
        assert result["estimated_pace_min_per_100m"] > 0
        collector.add_pass("游泳配速估算")
    except Exception as e:
        collector.add_fail("游泳配速估算", str(e))
    
    # Test 64: 配速估算 - 无效活动
    try:
        HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "invalid")
        collector.add_fail("配速估算 - 无效活动", "应抛出异常")
    except ValueError:
        collector.add_pass("配速估算 - 无效活动 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("配速估算 - 无效活动", f"异常类型错误: {e}")
    
    # ========== 心率趋势分析测试 ==========
    
    # Test 65: 心率趋势分析 - 基本统计
    try:
        readings = [120, 125, 130, 135, 140, 135, 130, 125, 120]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["count"] == 9
        assert result["min_hr"] == 120
        assert result["max_hr"] == 140
        collector.add_pass("心率趋势分析 - 基本统计")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 基本统计", str(e))
    
    # Test 66: 心率趋势分析 - 平均值
    try:
        readings = [120, 130, 140]
        result = HeartRateUtils.analyze_hr_trend(readings)
        expected_avg = (120 + 130 + 140) / 3  # 130
        assert result["average_hr"] == 130
        collector.add_pass("心率趋势分析 - 平均值")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 平均值", str(e))
    
    # Test 67: 心率趋势分析 - 中位数
    try:
        readings = [120, 130, 140, 150]
        result = HeartRateUtils.analyze_hr_trend(readings)
        expected_median = (130 + 140) / 2  # 135
        assert result["median_hr"] == 135
        collector.add_pass("心率趋势分析 - 中位数")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 中位数", str(e))
    
    # Test 68: 心率趋势分析 - 标准差
    try:
        readings = [130, 130, 130, 130]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["std_deviation"] == 0
        collector.add_pass("心率趋势分析 - 标准差（恒定值）")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 标准差（恒定值）", str(e))
    
    # Test 69: 心率趋势分析 - 趋势上升
    try:
        readings = [120, 125, 130, 135, 140]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["trend"] == "上升"
        collector.add_pass("心率趋势分析 - 上升趋势")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 上升趋势", str(e))
    
    # Test 70: 心率趋势分析 - 趋势下降
    try:
        readings = [140, 135, 130, 125, 120]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["trend"] == "下降"
        collector.add_pass("心率趋势分析 - 下降趋势")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 下降趋势", str(e))
    
    # Test 71: 心率趋势分析 - 稳定性
    try:
        readings = [130, 131, 132, 129, 130]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["stability"] in ["稳定", "较稳定"]
        collector.add_pass("心率趋势分析 - 稳定性判断")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 稳定性判断", str(e))
    
    # Test 72: 心率趋势分析 - RMSSD
    try:
        readings = [120, 125, 120, 125, 120]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["rmssd_estimate"] > 0
        collector.add_pass("心率趋势分析 - RMSSD")
    except Exception as e:
        collector.add_fail("心率趋势分析 - RMSSD", str(e))
    
    # Test 73: 心率趋势分析 - 空数据
    try:
        HeartRateUtils.analyze_hr_trend([])
        collector.add_fail("心率趋势分析 - 空数据", "应抛出异常")
    except ValueError:
        collector.add_pass("心率趋势分析 - 空数据 - 正确抛出异常")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 空数据", f"异常类型错误: {e}")
    
    # Test 74: 心率趋势分析 - 单个数据
    try:
        result = HeartRateUtils.analyze_hr_trend([130])
        assert result["count"] == 1
        assert result["average_hr"] == 130
        assert result["rmssd_estimate"] == 0
        collector.add_pass("心率趋势分析 - 单个数据")
    except Exception as e:
        collector.add_fail("心率趋势分析 - 单个数据", str(e))
    
    # ========== 便捷函数测试 ==========
    
    # Test 75: calculate_max_hr 便捷函数
    try:
        result = calculate_max_hr(30)
        assert result == 187  # Tanaka默认
        collector.add_pass("calculate_max_hr 便捷函数")
    except Exception as e:
        collector.add_fail("calculate_max_hr 便捷函数", str(e))
    
    # Test 76: calculate_max_hr 便捷函数 - 其他公式
    try:
        result = calculate_max_hr(30, "standard")
        assert result == 190
        collector.add_pass("calculate_max_hr 便捷函数 - standard")
    except Exception as e:
        collector.add_fail("calculate_max_hr 便捷函数 - standard", str(e))
    
    # Test 77: get_zones 便捷函数
    try:
        result = get_zones(30)
        assert "max_hr" in result
        assert "zones" in result
        collector.add_pass("get_zones 便捷函数")
    except Exception as e:
        collector.add_fail("get_zones 便捷函数", str(e))
    
    # Test 78: get_fat_burning_hr 便捷函数
    try:
        result = get_fat_burning_hr(30)
        assert "hr_range" in result
        assert "optimal_hr" in result
        collector.add_pass("get_fat_burning_hr 便捷函数")
    except Exception as e:
        collector.add_fail("get_fat_burning_hr 便捷函数", str(e))
    
    # Test 79: get_current_zone 便捷函数
    try:
        result = get_current_zone(120, 30)
        assert result is not None
        assert "zone" in result
        collector.add_pass("get_current_zone 便捷函数")
    except Exception as e:
        collector.add_fail("get_current_zone 便捷函数", str(e))
    
    # Test 80: estimate_calories 便捷函数
    try:
        result = estimate_calories(150, 45, 70, 30, "male")
        assert result > 0
        collector.add_pass("estimate_calories 便捷函数")
    except Exception as e:
        collector.add_fail("estimate_calories 便捷函数", str(e))
    
    # Test 81: assess_fitness 便捷函数
    try:
        result = assess_fitness(60, 30, "male")
        assert "fitness_level" in result
        assert "rating" in result
        collector.add_pass("assess_fitness 便捷函数")
    except Exception as e:
        collector.add_fail("assess_fitness 便捷函数", str(e))
    
    # ========== 边界值测试 ==========
    
    # Test 82: 极低心率区间 (20岁)
    try:
        result = HeartRateUtils.calculate_zones(20)
        # 20岁最大心率约194 (Tanaka)
        zone1_min = result.zones["Zone 1"].hr_range.min_hr
        assert zone1_min == int(194 * 0.5)  # 97
        collector.add_pass("极低心率区间 - 20岁")
    except Exception as e:
        collector.add_fail("极低心率区间 - 20岁", str(e))
    
    # Test 83: 高龄心率区间 (80岁)
    try:
        result = HeartRateUtils.calculate_zones(80)
        # 80岁最大心率约152 (Tanaka)
        zone5_max = result.zones["Zone 5"].hr_range.max_hr
        assert zone5_max == int(152 * 1.0)  # 152
        collector.add_pass("高龄心率区间 - 80岁")
    except Exception as e:
        collector.add_fail("高龄心率区间 - 80岁", str(e))
    
    # Test 84: 极长运动时间 (180分钟)
    try:
        result = HeartRateUtils.estimate_calories_burned(130, 180, 70, 30, "male")
        assert result["calories"] > 0
        assert result["duration_minutes"] == 180
        collector.add_pass("极长运动时间 (180分钟)")
    except Exception as e:
        collector.add_fail("极长运动时间 (180分钟)", str(e))
    
    # Test 85: 极短运动时间 (1分钟)
    try:
        result = HeartRateUtils.estimate_calories_burned(180, 1, 70, 30, "male")
        assert result["calories"] > 0
        collector.add_pass("极短运动时间 (1分钟)")
    except Exception as e:
        collector.add_fail("极短运动时间 (1分钟)", str(e))
    
    # Test 86: 极高体重 (150kg)
    try:
        result = HeartRateUtils.estimate_calories_burned(150, 30, 150, 30, "male")
        assert result["calories"] > 0
        collector.add_pass("极高体重 (150kg)")
    except Exception as e:
        collector.add_fail("极高体重 (150kg)", str(e))
    
    # Test 87: 极低体重 (30kg)
    try:
        result = HeartRateUtils.estimate_calories_burned(150, 30, 30, 30, "male")
        assert result["calories"] > 0
        collector.add_pass("极低体重 (30kg)")
    except Exception as e:
        collector.add_fail("极低体重 (30kg)", str(e))
    
    # Test 88: 大量心率数据 (1000条)
    try:
        readings = [130 + (i % 20 - 10) for i in range(1000)]
        result = HeartRateUtils.analyze_hr_trend(readings)
        assert result["count"] == 1000
        assert result["min_hr"] == 120
        # The max will be 139 since 130 + (19 % 20 - 10) = 130 + 9 = 139
        assert result["max_hr"] >= 139
        collector.add_pass("大量心率数据 (1000条)")
    except Exception as e:
        collector.add_fail("大量心率数据 (1000条)", str(e))
    
    # Test 89: to_dict 方法
    try:
        result = HeartRateUtils.calculate_zones(30)
        dict_result = result.to_dict()
        assert "max_hr" in dict_result
        assert "zones" in dict_result
        assert isinstance(dict_result["zones"], dict)
        collector.add_pass("to_dict 方法")
    except Exception as e:
        collector.add_fail("to_dict 方法", str(e))
    
    # Test 90: HeartRateRange __contains__ 方法
    try:
        range_obj = result.zones["Zone 2"].hr_range
        assert 120 in range_obj  # 应该在Zone 2范围
        assert 50 not in range_obj  # 不在范围
        collector.add_pass("HeartRateRange __contains__ 方法")
    except Exception as e:
        collector.add_fail("HeartRateRange __contains__ 方法", str(e))
    
    return collector.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)