"""
Wind Scale Utilities 测试

全面测试风力等级转换、风向转换、风寒指数等功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wind_scale_utils.mod import (
    WindDirection,
    WindInfo,
    BeaufortLevel,
    HurricaneCategory,
    TyphoonLevel,
    WindScaleConverter,
    BEAUFORT_SCALE,
    SAFFIR_SIMPSON_SCALE,
    TYPHOON_LEVELS,
    WIND_DIRECTION_RANGES,
    WIND_DIRECTION_ENGLISH,
    WIND_DIRECTION_ABBR,
    get_wind_level,
    get_wind_name,
    convert_speed,
    wind_chill,
    get_wind_warning,
)


class TestWindScaleConverter(unittest.TestCase):
    """测试 WindScaleConverter 类"""
    
    def setUp(self):
        """设置测试"""
        self.converter = WindScaleConverter()
    
    def test_ms_to_kmh(self):
        """测试 m/s 转 km/h"""
        self.assertAlmostEqual(self.converter.ms_to_kmh(10.0), 36.0)
        self.assertAlmostEqual(self.converter.ms_to_kmh(0.0), 0.0)
        self.assertAlmostEqual(self.converter.ms_to_kmh(1.0), 3.6)
    
    def test_ms_to_knot(self):
        """测试 m/s 转 节"""
        self.assertAlmostEqual(self.converter.ms_to_knot(10.0), 19.4384, places=2)
        self.assertAlmostEqual(self.converter.ms_to_knot(1.0), 1.94384, places=2)
    
    def test_ms_to_mph(self):
        """测试 m/s 转 mph"""
        self.assertAlmostEqual(self.converter.ms_to_mph(10.0), 22.3694, places=2)
        self.assertAlmostEqual(self.converter.ms_to_mph(1.0), 2.23694, places=2)
    
    def test_kmh_to_ms(self):
        """测试 km/h 转 m/s"""
        self.assertAlmostEqual(self.converter.kmh_to_ms(36.0), 10.0)
        self.assertAlmostEqual(self.converter.kmh_to_ms(3.6), 1.0)
    
    def test_knot_to_ms(self):
        """测试 节 转 m/s"""
        self.assertAlmostEqual(self.converter.knot_to_ms(19.4384), 10.0, places=2)
        self.assertAlmostEqual(self.converter.knot_to_ms(1.94384), 1.0, places=2)
    
    def test_mph_to_ms(self):
        """测试 mph 转 m/s"""
        self.assertAlmostEqual(self.converter.mph_to_ms(22.3694), 10.0, places=2)
        self.assertAlmostEqual(self.converter.mph_to_ms(2.23694), 1.0, places=2)
    
    def test_speed_conversion_roundtrip(self):
        """测试速度转换往返"""
        original = 10.0
        converted = self.converter.ms_to_kmh(original)
        back = self.converter.kmh_to_ms(converted)
        self.assertAlmostEqual(back, original, places=1)
    
    def test_get_beaufort_level_0(self):
        """测试无风等级"""
        level = self.converter.get_beaufort_level(0.0)
        self.assertEqual(level.level, 0)
        self.assertEqual(level.name_cn, "无风")
    
    def test_get_beaufort_level_1(self):
        """测试软风等级"""
        level = self.converter.get_beaufort_level(0.5)
        self.assertEqual(level.level, 1)
        self.assertEqual(level.name_cn, "软风")
    
    def test_get_beaufort_level_5(self):
        """测试清风等级"""
        level = self.converter.get_beaufort_level(9.0)
        self.assertEqual(level.level, 5)
        self.assertEqual(level.name_cn, "清风")
    
    def test_get_beaufort_level_12(self):
        """测试飓风等级"""
        level = self.converter.get_beaufort_level(40.0)
        self.assertEqual(level.level, 12)
        self.assertEqual(level.name_cn, "飓风")
    
    def test_beaufort_scale_count(self):
        """测试蒲福风级数量"""
        self.assertEqual(len(BEAUFORT_SCALE), 13)
    
    def test_beaufort_scale_levels_continuous(self):
        """测试蒲福风级连续性"""
        for i, level in enumerate(BEAUFORT_SCALE):
            self.assertEqual(level.level, i)
    
    def test_get_wind_info(self):
        """测试获取风速信息"""
        info = self.converter.get_wind_info(15.0)
        
        self.assertIsInstance(info, WindInfo)
        self.assertEqual(info.beaufort_level, 7)
        self.assertEqual(info.beaufort_name_cn, "疾风")
        self.assertEqual(info.beaufort_name_en, "Near Gale")
        self.assertAlmostEqual(info.wind_speed_ms, 15.0)
        self.assertAlmostEqual(info.wind_speed_kmh, 54.0, places=1)
        self.assertIn(info.sea_description, BEAUFORT_SCALE[7].sea_description)
    
    def test_angle_to_direction_n(self):
        """测试角度转风向-北风"""
        direction = self.converter.angle_to_direction(0.0)
        self.assertEqual(direction, WindDirection.N)
        
        direction = self.converter.angle_to_direction(350.0)
        self.assertEqual(direction, WindDirection.N)
    
    def test_angle_to_direction_e(self):
        """测试角度转风向-东风"""
        direction = self.converter.angle_to_direction(90.0)
        self.assertEqual(direction, WindDirection.E)
    
    def test_angle_to_direction_s(self):
        """测试角度转风向-南风"""
        direction = self.converter.angle_to_direction(180.0)
        self.assertEqual(direction, WindDirection.S)
    
    def test_angle_to_direction_w(self):
        """测试角度转风向-西风"""
        direction = self.converter.angle_to_direction(270.0)
        self.assertEqual(direction, WindDirection.W)
    
    def test_angle_to_direction_ne(self):
        """测试角度转风向-东北风"""
        direction = self.converter.angle_to_direction(45.0)
        self.assertEqual(direction, WindDirection.NE)
    
    def test_direction_to_angle(self):
        """测试风向转角度"""
        self.assertAlmostEqual(self.converter.direction_to_angle(WindDirection.N), 0.0)
        self.assertAlmostEqual(self.converter.direction_to_angle(WindDirection.E), 90.0)
        self.assertAlmostEqual(self.converter.direction_to_angle(WindDirection.S), 180.0)
        self.assertAlmostEqual(self.converter.direction_to_angle(WindDirection.W), 270.0)
        self.assertAlmostEqual(self.converter.direction_to_angle(WindDirection.NE), 45.0)
    
    def test_direction_roundtrip(self):
        """测试风向角度往返转换"""
        for direction in WindDirection:
            angle = self.converter.direction_to_angle(direction)
            back = self.converter.angle_to_direction(angle)
            self.assertEqual(back, direction)
    
    def test_wind_chill_below_threshold(self):
        """测试风寒指数低于阈值"""
        # 温度 >= 10°C 或风速 <= 1.3 m/s，风寒指数等于气温
        self.assertEqual(self.converter.calculate_wind_chill(15.0, 5.0), 15.0)
        self.assertEqual(self.converter.calculate_wind_chill(5.0, 1.0), 5.0)
    
    def test_wind_chill_normal(self):
        """测试正常风寒指数"""
        chill = self.converter.calculate_wind_chill(0.0, 10.0)
        self.assertLess(chill, 0.0)  # 体感温度应低于实际温度
    
    def test_wind_chill_formula(self):
        """测试风寒指数公式"""
        # 温度 -5°C，风速 10 m/s
        temp = -5.0
        speed = 10.0
        chill = self.converter.calculate_wind_chill(temp, speed)
        # 验证体感温度确实更低
        self.assertLess(chill, temp)
    
    def test_get_hurricane_category_none(self):
        """测试非飓风风速"""
        # 低于飓风级别
        cat = self.converter.get_hurricane_category(20.0)
        self.assertIsNone(cat)
    
    def test_get_hurricane_category_1(self):
        """测试一级飓风"""
        cat = self.converter.get_hurricane_category(35.0)
        self.assertIsNotNone(cat)
        self.assertEqual(cat.category, 1)
    
    def test_get_hurricane_category_5(self):
        """测试五级飓风"""
        cat = self.converter.get_hurricane_category(80.0)
        self.assertIsNotNone(cat)
        self.assertEqual(cat.category, 5)
    
    def test_hurricane_scale_count(self):
        """测试飓风等级数量"""
        self.assertEqual(len(SAFFIR_SIMPSON_SCALE), 5)
    
    def test_get_typhoon_level_none(self):
        """测试非台风风速"""
        level = self.converter.get_typhoon_level(5.0)
        self.assertIsNone(level)
    
    def test_get_typhoon_level_td(self):
        """测试热带低压"""
        level = self.converter.get_typhoon_level(15.0)
        self.assertIsNotNone(level)
        self.assertEqual(level.level, "热带低压")
    
    def test_get_typhoon_level_typhoon(self):
        """测试台风"""
        level = self.converter.get_typhoon_level(35.0)
        self.assertIsNotNone(level)
        self.assertEqual(level.level, "台风")
    
    def test_get_typhoon_level_super(self):
        """测试超强台风"""
        level = self.converter.get_typhoon_level(55.0)
        self.assertIsNotNone(level)
        self.assertEqual(level.level, "超强台风")
    
    def test_typhoon_levels_count(self):
        """测试台风等级数量"""
        self.assertEqual(len(TYPHOON_LEVELS), 6)
    
    def test_generate_wind_rose_data(self):
        """测试风玫瑰图数据生成"""
        wind_data = [
            {'direction': 0, 'speed': 10.0},
            {'direction': 45, 'speed': 15.0},
            {'direction': 90, 'speed': 8.0},
            {'direction': 0, 'speed': 12.0},
            {'direction': 45, 'speed': 20.0},
        ]
        
        result = self.converter.generate_wind_rose_data(wind_data)
        
        # 检查北风统计
        self.assertEqual(result['N']['count'], 2)
        self.assertAlmostEqual(result['N']['avg_speed'], 11.0, places=1)
        
        # 检查东北风统计
        self.assertEqual(result['NE']['count'], 2)
        self.assertAlmostEqual(result['NE']['avg_speed'], 17.5, places=1)
        
        # 检查东风统计
        self.assertEqual(result['E']['count'], 1)
        self.assertAlmostEqual(result['E']['avg_speed'], 8.0, places=1)
    
    def test_generate_wind_rose_data_empty(self):
        """测试空风玫瑰图数据"""
        result = self.converter.generate_wind_rose_data([])
        
        # 所有方向应该有初始值
        for direction in WindDirection:
            self.assertEqual(result[direction.name]['count'], 0)
            self.assertEqual(result[direction.name]['avg_speed'], 0.0)
    
    def test_wind_warning_level_none(self):
        """测试无预警"""
        warning = self.converter.get_wind_warning_level(5.0)
        self.assertEqual(warning['level'], 0)
        self.assertEqual(warning['name'], '无预警')
    
    def test_wind_warning_level_blue(self):
        """测试蓝色预警"""
        warning = self.converter.get_wind_warning_level(12.0)
        self.assertEqual(warning['level'], 1)
        self.assertEqual(warning['name'], '蓝色预警')
    
    def test_wind_warning_level_yellow(self):
        """测试黄色预警"""
        warning = self.converter.get_wind_warning_level(20.0)
        self.assertEqual(warning['level'], 2)
        self.assertEqual(warning['name'], '黄色预警')
    
    def test_wind_warning_level_orange(self):
        """测试橙色预警"""
        warning = self.converter.get_wind_warning_level(28.0)
        self.assertEqual(warning['level'], 3)
        self.assertEqual(warning['name'], '橙色预警')
    
    def test_wind_warning_level_red(self):
        """测试红色预警"""
        warning = self.converter.get_wind_warning_level(35.0)
        self.assertEqual(warning['level'], 4)
        self.assertEqual(warning['name'], '红色预警')
    
    def test_calculate_wind_power(self):
        """测试风能功率计算"""
        power = self.converter.calculate_wind_power(10.0)
        self.assertGreater(power, 0)
        
        # P = 0.5 * 1.225 * 10^3 = 612.5 W
        expected = 0.5 * 1.225 * 1000
        self.assertAlmostEqual(power, expected, places=1)
    
    def test_calculate_wind_power_scaling(self):
        """测试风能功率随风速立方增长"""
        power1 = self.converter.calculate_wind_power(10.0)
        power2 = self.converter.calculate_wind_power(20.0)
        
        # 风速翻倍，功率应该增加8倍
        self.assertAlmostEqual(power2 / power1, 8.0, places=1)
    
    def test_calculate_wind_power_with_area(self):
        """测试不同面积的风能功率"""
        power1 = self.converter.calculate_wind_power(10.0, 1.0)
        power10 = self.converter.calculate_wind_power(10.0, 10.0)
        
        self.assertAlmostEqual(power10 / power1, 10.0, places=1)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_wind_level(self):
        """测试获取风力等级"""
        self.assertEqual(get_wind_level(0.0), 0)
        self.assertEqual(get_wind_level(10.0), 5)
        self.assertEqual(get_wind_level(30.0), 11)
    
    def test_get_wind_name_cn(self):
        """测试获取中文名称"""
        self.assertEqual(get_wind_name(0.0, 'cn'), "无风")
        self.assertEqual(get_wind_name(5.0, 'cn'), "微风")  # 5.0 m/s 是风级3（微风）
        self.assertEqual(get_wind_name(6.0, 'cn'), "和风")  # 6.0 m/s 是风级4（和风）
        self.assertEqual(get_wind_name(30.0, 'cn'), "暴风")
    
    def test_get_wind_name_en(self):
        """测试获取英文名称"""
        self.assertEqual(get_wind_name(0.0, 'en'), "Calm")
        self.assertEqual(get_wind_name(5.0, 'en'), "Gentle Breeze")  # 5.0 m/s 是风级3
        self.assertEqual(get_wind_name(6.0, 'en'), "Moderate Breeze")  # 6.0 m/s 是风级4
        self.assertEqual(get_wind_name(30.0, 'en'), "Violent Storm")
    
    def test_convert_speed(self):
        """测试速度转换"""
        self.assertAlmostEqual(convert_speed(10.0, 'ms', 'kmh'), 36.0, places=1)
        self.assertAlmostEqual(convert_speed(36.0, 'kmh', 'ms'), 10.0, places=1)
        self.assertAlmostEqual(convert_speed(19.44, 'knot', 'ms'), 10.0, places=1)
        self.assertAlmostEqual(convert_speed(10.0, 'ms', 'knot'), 19.44, places=1)
    
    def test_wind_chill(self):
        """测试风寒指数便捷函数"""
        chill = wind_chill(0.0, 10.0)
        self.assertLess(chill, 0.0)
    
    def test_get_wind_warning(self):
        """测试预警便捷函数"""
        warning = get_wind_warning(15.0)
        self.assertIn('level', warning)
        self.assertIn('name', warning)
        self.assertEqual(warning['name'], '蓝色预警')


class TestWindDirectionEnum(unittest.TestCase):
    """测试风向枚举"""
    
    def test_wind_direction_count(self):
        """测试风向数量"""
        self.assertEqual(len(WindDirection), 16)
    
    def test_wind_direction_values(self):
        """测试风向值"""
        self.assertEqual(WindDirection.N.value, "北风")
        self.assertEqual(WindDirection.E.value, "东风")
        self.assertEqual(WindDirection.S.value, "南风")
        self.assertEqual(WindDirection.W.value, "西风")
    
    def test_wind_direction_english(self):
        """测试英文风向名称"""
        self.assertEqual(WIND_DIRECTION_ENGLISH[WindDirection.N], "North")
        self.assertEqual(WIND_DIRECTION_ENGLISH[WindDirection.E], "East")
    
    def test_wind_direction_abbr(self):
        """测试风向缩写"""
        self.assertEqual(WIND_DIRECTION_ABBR[WindDirection.N], "N")
        self.assertEqual(WIND_DIRECTION_ABBR[WindDirection.NE], "NE")


class TestBeaufortLevelDataclass(unittest.TestCase):
    """测试蒲福风级数据类"""
    
    def test_beaufort_level_creation(self):
        """测试蒲福风级创建"""
        level = BeaufortLevel(
            level=5,
            name_cn="清风",
            name_en="Fresh Breeze",
            wind_speed_min=8.0,
            wind_speed_max=10.7,
            wind_speed_min_kmh=29.0,
            wind_speed_max_kmh=38.0,
            wind_speed_min_knot=17.0,
            wind_speed_max_knot=21.0,
            sea_description="中浪",
            land_description="有叶的小树摇摆",
            wave_height_min=1.5,
            wave_height_max=2.5
        )
        
        self.assertEqual(level.level, 5)
        self.assertEqual(level.name_cn, "清风")
        self.assertEqual(level.name_en, "Fresh Breeze")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.converter = WindScaleConverter()
    
    def test_negative_speed(self):
        """测试负风速"""
        level = self.converter.get_beaufort_level(-1.0)
        self.assertEqual(level.level, 0)  # 应返回最小等级
    
    def test_extremely_high_speed(self):
        """测试极高风速"""
        level = self.converter.get_beaufort_level(100.0)
        self.assertEqual(level.level, 12)  # 应返回最大等级
    
    def test_angle_over_360(self):
        """测试超过360度的角度"""
        direction = self.converter.angle_to_direction(450.0)
        self.assertEqual(direction, WindDirection.E)  # 450 - 360 = 90
    
    def test_angle_negative(self):
        """测试负角度"""
        direction = self.converter.angle_to_direction(-90.0)
        self.assertEqual(direction, WindDirection.W)  # -90 + 360 = 270
    
    def test_wind_chill_high_temp(self):
        """测试高温风寒指数"""
        # 高温时不计算风寒指数
        chill = self.converter.calculate_wind_chill(30.0, 20.0)
        self.assertEqual(chill, 30.0)  # 返回原温度
    
    def test_wind_power_zero_speed(self):
        """测试零风速功率"""
        power = self.converter.calculate_wind_power(0.0)
        self.assertEqual(power, 0.0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        self.converter = WindScaleConverter()
    
    def test_full_wind_analysis(self):
        """测试完整风力分析"""
        speed_ms = 25.0
        
        # 获取风级信息
        info = self.converter.get_wind_info(speed_ms)
        
        # 验证各项数据一致
        self.assertEqual(info.beaufort_level, 10)
        
        # 获取台风等级
        typhoon = self.converter.get_typhoon_level(speed_ms)
        self.assertIsNotNone(typhoon)
        
        # 获取预警等级
        warning = self.converter.get_wind_warning_level(speed_ms)
        self.assertGreater(warning['level'], 0)
    
    def test_typical_weather_scenario(self):
        """测试典型天气场景"""
        # 冬天，5°C，风速 10 m/s
        temp = 5.0
        speed = 10.0
        
        # 计算风寒
        chill = self.converter.calculate_wind_chill(temp, speed)
        
        # 验证体感温度更低
        self.assertLess(chill, temp)
        
        # 获取风级
        info = self.converter.get_wind_info(speed)
        
        # 验证是强风等级
        self.assertEqual(info.beaufort_level, 5)
    
    def test_typhoon_analysis(self):
        """测试台风分析"""
        # 强台风风速 45 m/s
        speed = 45.0
        
        # 获取蒲福风级
        info = self.converter.get_wind_info(speed)
        self.assertEqual(info.beaufort_level, 12)
        
        # 获取台风等级
        typhoon = self.converter.get_typhoon_level(speed)
        self.assertEqual(typhoon.level, "强台风")
        
        # 获取飓风等级
        hurricane = self.converter.get_hurricane_category(speed)
        self.assertEqual(hurricane.category, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)