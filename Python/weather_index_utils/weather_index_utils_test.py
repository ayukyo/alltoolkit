"""
Weather Index Utils 测试文件
============================

测试所有天气指数计算功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from weather_index_utils.mod import (
    WeatherIndexCalculator,
    heat_index,
    wind_chill,
    dew_point,
    apparent_temperature,
    comfort_index,
    wbgt
)


class TestHeatIndex(unittest.TestCase):
    """热指数测试"""
    
    def test_basic_heat_index(self):
        """测试基本热指数计算"""
        # 35°C, 70% 湿度
        hi = heat_index(35, 70)
        self.assertIsInstance(hi, float)
        self.assertGreater(hi, 35)  # 热指数应该高于实际温度
    
    def test_heat_index_fahrenheit(self):
        """测试华氏度热指数"""
        # 95°F = 35°C, 70% 湿度
        hi_f = heat_index(95, 70, 'fahrenheit')
        self.assertIsInstance(hi_f, float)
        # 转换后应该接近
        hi_c = heat_index(35, 70, 'celsius')
        self.assertAlmostEqual(hi_f, hi_c * 9/5 + 32, places=0)
    
    def test_low_temperature(self):
        """测试低温情况（热指数不适用）"""
        # 20°C, 50% 湿度 - 温度太低，返回原温度
        hi = heat_index(20, 50)
        self.assertEqual(hi, 20.0)
    
    def test_low_humidity_adjustment(self):
        """测试低湿度调整"""
        # 40°C, 10% 湿度 - 应该应用低湿度调整
        hi = heat_index(40, 10)
        self.assertIsInstance(hi, float)
    
    def test_high_humidity_adjustment(self):
        """测试高湿度调整"""
        # 30°C, 90% 湿度 - 高湿度情况
        hi = heat_index(30, 90)
        self.assertIsInstance(hi, float)
        self.assertGreater(hi, 30)
    
    def test_extreme_heat(self):
        """测试极端高温"""
        # 45°C, 80% 湿度 - 极端高温
        hi = heat_index(45, 80)
        self.assertGreater(hi, 45)
    
    def test_invalid_humidity(self):
        """测试无效湿度"""
        with self.assertRaises(ValueError):
            heat_index(30, 150)  # 湿度超过 100
        
        with self.assertRaises(ValueError):
            heat_index(30, -10)  # 湿度为负
    
    def test_boundary_values(self):
        """测试边界值"""
        # 刚好 80°F 边界
        hi_26 = heat_index(26.67, 50)  # 80°F
        self.assertIsInstance(hi_26, float)
        
        # 湿度边界
        hi_0 = heat_index(30, 0)  # 0% 湿度
        hi_100 = heat_index(30, 100)  # 100% 湿度
        self.assertIsInstance(hi_0, float)
        self.assertIsInstance(hi_100, float)


class TestWindChill(unittest.TestCase):
    """风寒指数测试"""
    
    def test_basic_wind_chill(self):
        """测试基本风寒指数"""
        # -10°C, 30 km/h
        wc = wind_chill(-10, 30)
        self.assertLess(wc, -10)  # 风寒应该低于实际温度
    
    def test_wind_chill_fahrenheit(self):
        """测试华氏度风寒指数"""
        # 14°F = -10°C, 18.6 mph ≈ 30 km/h
        wc_f = wind_chill(14, 18.6, 'fahrenheit', 'mph')
        self.assertIsInstance(wc_f, float)
    
    def test_high_temperature(self):
        """测试高温情况（风寒不适用）"""
        # 20°C, 30 km/h - 温度太高
        wc = wind_chill(20, 30)
        self.assertEqual(wc, 20.0)
    
    def test_low_wind(self):
        """测试低风速情况"""
        # -5°C, 2 km/h - 风速太低
        wc = wind_chill(-5, 2)
        self.assertEqual(wc, -5.0)
    
    def test_different_speed_units(self):
        """测试不同风速单位"""
        # -10°C, 30 km/h
        wc_kmh = wind_chill(-10, 30, 'celsius', 'kmh')
        wc_ms = wind_chill(-10, 30/3.6, 'celsius', 'ms')
        wc_mph = wind_chill(-10, 30/1.609344, 'celsius', 'mph')
        
        # 不同单位应该得到相似结果
        self.assertAlmostEqual(wc_kmh, wc_ms, places=0)
        self.assertAlmostEqual(wc_kmh, wc_mph, places=0)
    
    def test_extreme_cold(self):
        """测试极端寒冷"""
        # -30°C, 50 km/h
        wc = wind_chill(-30, 50)
        self.assertLess(wc, -30)


class TestDewPoint(unittest.TestCase):
    """露点测试"""
    
    def test_basic_dew_point(self):
        """测试基本露点计算"""
        # 30°C, 70% 湿度
        dp = dew_point(30, 70)
        self.assertGreater(dp, 0)
        self.assertLess(dp, 30)  # 露点应该低于实际温度
    
    def test_dew_point_saturation(self):
        """测试饱和情况"""
        # 100% 湿度时，露点等于温度
        dp = dew_point(25, 100)
        self.assertAlmostEqual(dp, 25.0, places=0)
    
    def test_dew_point_fahrenheit(self):
        """测试华氏度露点"""
        # 86°F = 30°C, 70% 湿度
        dp_f = dew_point(86, 70, 'fahrenheit')
        dp_c = dew_point(30, 70, 'celsius')
        
        # 转换后应该接近
        self.assertAlmostEqual(dp_f, dp_c * 9/5 + 32, places=0)
    
    def test_low_humidity(self):
        """测试低湿度露点"""
        # 30°C, 20% 湿度
        dp = dew_point(30, 20)
        self.assertLess(dp, 10)  # 低湿度时露点很低
    
    def test_invalid_humidity(self):
        """测试无效湿度"""
        with self.assertRaises(ValueError):
            dew_point(25, 150)
        
        with self.assertRaises(ValueError):
            dew_point(25, -5)


class TestApparentTemperature(unittest.TestCase):
    """体感温度测试"""
    
    def test_hot_humid(self):
        """测试高温高湿"""
        at = apparent_temperature(35, 70, 0)
        self.assertGreater(at, 35)  # 应该使用热指数
    
    def test_cold_windy(self):
        """测试低温有风"""
        at = apparent_temperature(-5, 50, 30)
        self.assertLess(at, -5)  # 应该使用风寒指数
    
    def test_moderate(self):
        """测试适中温度"""
        at = apparent_temperature(20, 50, 5)
        self.assertEqual(at, 20.0)  # 直接返回原温度
    
    def test_transition_temperatures(self):
        """测试过渡温度"""
        # 27°C 边界（热指数）
        at_hot = apparent_temperature(27, 80, 0)
        self.assertGreater(at_hot, 27)
        
        # 10°C 边界（风寒）
        at_cold = apparent_temperature(10, 50, 20)
        self.assertLessEqual(at_cold, 10)


class TestUVIndex(unittest.TestCase):
    """紫外线指数测试"""
    
    def test_basic_uv_index(self):
        """测试基本 UV 指数计算"""
        uvi = WeatherIndexCalculator.uv_index(0.25)  # 250 mW/m²
        self.assertEqual(uvi, 10)
    
    def test_low_uv(self):
        """测试低 UV"""
        uvi = WeatherIndexCalculator.uv_index(0.02)  # 20 mW/m²
        self.assertEqual(uvi, 1)
    
    def test_extreme_uv(self):
        """测试极端 UV"""
        uvi = WeatherIndexCalculator.uv_index(0.35)  # 350 mW/m²
        self.assertEqual(uvi, 11)  # 最大显示 11
    
    def test_uv_category(self):
        """测试 UV 风险等级"""
        low = WeatherIndexCalculator.uv_index_category(2)
        self.assertEqual(low[0], 'Low')
        
        moderate = WeatherIndexCalculator.uv_index_category(5)
        self.assertEqual(moderate[0], 'Moderate')
        
        high = WeatherIndexCalculator.uv_index_category(7)
        self.assertEqual(high[0], 'High')
        
        very_high = WeatherIndexCalculator.uv_index_category(9)
        self.assertEqual(very_high[0], 'Very High')
        
        extreme = WeatherIndexCalculator.uv_index_category(11)
        self.assertEqual(extreme[0], 'Extreme')


class TestComfortIndex(unittest.TestCase):
    """舒适度指数测试"""
    
    def test_basic_comfort_index(self):
        """测试基本舒适度指数"""
        thi = comfort_index(30, 70)
        self.assertGreater(thi, 70)
    
    def test_comfortable_conditions(self):
        """测试舒适条件"""
        # 22°C, 50% 湿度 - 舒适
        thi = comfort_index(22, 50)
        level = WeatherIndexCalculator.comfort_level(thi)
        self.assertIn(level[0], ['Comfortable', 'Cool'])
    
    def test_uncomfortable_conditions(self):
        """测试不适条件"""
        # 35°C, 80% 湿度 - 不适
        thi = comfort_index(35, 80)
        level = WeatherIndexCalculator.comfort_level(thi)
        self.assertIn('Uncomfortable', level[0])
    
    def test_comfort_level_categories(self):
        """测试舒适度等级分类"""
        cool = WeatherIndexCalculator.comfort_level(60)
        self.assertEqual(cool[0], 'Cool')
        
        comfortable = WeatherIndexCalculator.comfort_level(70)
        self.assertEqual(comfortable[0], 'Comfortable')
        
        slight = WeatherIndexCalculator.comfort_level(77)
        self.assertEqual(slight[0], 'Slightly Uncomfortable')
        
        uncomfortable = WeatherIndexCalculator.comfort_level(82)
        self.assertEqual(uncomfortable[0], 'Uncomfortable')
        
        very = WeatherIndexCalculator.comfort_level(88)
        self.assertEqual(very[0], 'Very Uncomfortable')


class TestWetBulbTemperature(unittest.TestCase):
    """湿球温度测试"""
    
    def test_basic_wet_bulb(self):
        """测试基本湿球温度"""
        wb = WeatherIndexCalculator.wet_bulb_temperature(30, 50)
        self.assertLess(wb, 30)  # 湿球温度低于干球温度
        self.assertGreater(wb, 0)
    
    def test_saturation_wet_bulb(self):
        """测试饱和湿球温度"""
        # 100% 湿度时，湿球温度接近干球温度
        wb = WeatherIndexCalculator.wet_bulb_temperature(25, 100)
        self.assertAlmostEqual(wb, 25, places=0)
    
    def test_dry_air_wet_bulb(self):
        """测试干燥空气湿球温度"""
        # 低湿度时，湿球温度显著低于干球温度
        wb = WeatherIndexCalculator.wet_bulb_temperature(35, 20)
        self.assertLess(wb, 25)


class TestWBGT(unittest.TestCase):
    """WBGT 指数测试"""
    
    def test_basic_wbgt(self):
        """测试基本 WBGT"""
        wbgt_val = wbgt(30, 70)
        self.assertLess(wbgt_val, 30)  # WBGT 通常低于干球温度
        self.assertGreater(wbgt_val, 0)
    
    def test_wbgt_with_solar(self):
        """测试有太阳辐射的 WBGT"""
        wbgt_indoor = wbgt(30, 70, 0)
        wbgt_outdoor = wbgt(30, 70, 500)  # 500 W/m² 太阳辐射
        self.assertGreater(wbgt_outdoor, wbgt_indoor)
    
    def test_heat_risk_levels(self):
        """测试热风险等级"""
        white = WeatherIndexCalculator.heat_risk_level(20)
        self.assertEqual(white[0], 'White')
        
        green = WeatherIndexCalculator.heat_risk_level(26)
        self.assertEqual(green[0], 'Green')
        
        yellow = WeatherIndexCalculator.heat_risk_level(29)
        self.assertEqual(yellow[0], 'Yellow')
        
        orange = WeatherIndexCalculator.heat_risk_level(31)
        self.assertEqual(orange[0], 'Orange')
        
        red = WeatherIndexCalculator.heat_risk_level(33)
        self.assertEqual(red[0], 'Red')
        
        black = WeatherIndexCalculator.heat_risk_level(36)
        self.assertEqual(black[0], 'Black')


class TestAbsoluteHumidity(unittest.TestCase):
    """绝对湿度测试"""
    
    def test_basic_absolute_humidity(self):
        """测试基本绝对湿度"""
        ah = WeatherIndexCalculator.absolute_humidity(25, 50)
        self.assertGreater(ah, 0)
        self.assertLess(ah, 30)  # 通常在合理范围内
    
    def test_saturation_absolute_humidity(self):
        """测试饱和绝对湿度"""
        # 100% 湿度时绝对湿度最大
        ah_100 = WeatherIndexCalculator.absolute_humidity(25, 100)
        ah_50 = WeatherIndexCalculator.absolute_humidity(25, 50)
        self.assertGreater(ah_100, ah_50)


class TestVaporPressureDeficit(unittest.TestCase):
    """水汽压差测试"""
    
    def test_basic_vpd(self):
        """测试基本 VPD"""
        vpd = WeatherIndexCalculator.vapor_pressure_deficit(25, 50)
        self.assertGreater(vpd, 0)
        self.assertIsInstance(vpd, float)
    
    def test_saturation_vpd(self):
        """测试饱和 VPD"""
        # 100% 湿度时 VPD 为 0
        vpd = WeatherIndexCalculator.vapor_pressure_deficit(25, 100)
        self.assertAlmostEqual(vpd, 0, places=1)
    
    def test_dry_air_vpd(self):
        """测试干燥空气 VPD"""
        # 低湿度时 VPD 较高
        vpd_dry = WeatherIndexCalculator.vapor_pressure_deficit(30, 20)
        vpd_humid = WeatherIndexCalculator.vapor_pressure_deficit(30, 80)
        self.assertGreater(vpd_dry, vpd_humid)


class TestEvapotranspiration(unittest.TestCase):
    """蒸散量测试"""
    
    def test_basic_et(self):
        """测试基本蒸散量"""
        et = WeatherIndexCalculator.evapotranspiration(25, 60, 2, 20)
        self.assertGreater(et, 0)
        self.assertIsInstance(et, float)
    
    def test_et_factors(self):
        """测试影响蒸散量的因素"""
        # 高温高辐射高风速 = 高蒸散
        et_high = WeatherIndexCalculator.evapotranspiration(30, 40, 5, 25)
        # 低温低辐射低风速 = 低蒸散
        et_low = WeatherIndexCalculator.evapotranspiration(15, 80, 1, 10)
        self.assertGreater(et_high, et_low)


class TestGrowingDegreeDays(unittest.TestCase):
    """生长度日测试"""
    
    def test_basic_gdd(self):
        """测试基本 GDD"""
        gdd = WeatherIndexCalculator.growing_degree_days(15, 28, 10)
        self.assertGreater(gdd, 0)
        self.assertEqual(gdd, 11.5)
    
    def test_gdd_below_base(self):
        """测试低于基准温度的 GDD"""
        # 平均温度低于基准温度
        gdd = WeatherIndexCalculator.growing_degree_days(5, 12, 10)
        self.assertEqual(gdd, 0)  # GDD 不能为负
    
    def test_custom_base_temp(self):
        """测试自定义基准温度"""
        gdd_default = WeatherIndexCalculator.growing_degree_days(15, 25, 10)
        gdd_custom = WeatherIndexCalculator.growing_degree_days(15, 25, 15)
        self.assertGreater(gdd_default, gdd_custom)


class TestPressureAltitude(unittest.TestCase):
    """气压海拔测试"""
    
    def test_sea_level_pressure(self):
        """测试海平面气压"""
        alt = WeatherIndexCalculator.pressure_altitude(1013.25)
        self.assertAlmostEqual(alt, 0, places=0)
    
    def test_mountain_altitude(self):
        """测试高海拔"""
        # 拉萨海拔约 3650m，气压约 650 hPa
        alt = WeatherIndexCalculator.pressure_altitude(650)
        self.assertGreater(alt, 3000)
        self.assertLess(alt, 4000)
    
    def test_sea_level_correction(self):
        """测试海平面气压修正"""
        # 站点气压 1000 hPa，海拔 100m
        slp = WeatherIndexCalculator.sea_level_pressure(1000, 100, 20)
        self.assertGreater(slp, 1000)


class TestAirDensity(unittest.TestCase):
    """空气密度测试"""
    
    def test_basic_air_density(self):
        """测试基本空气密度"""
        rho = WeatherIndexCalculator.air_density(20, 1013.25, 50)
        self.assertGreater(rho, 1.0)
        self.assertLess(rho, 1.3)
    
    def test_humidity_effect(self):
        """测试湿度对空气密度的影响"""
        # 湿空气比干空气轻
        rho_dry = WeatherIndexCalculator.air_density(25, 1013.25, 0)
        rho_humid = WeatherIndexCalculator.air_density(25, 1013.25, 100)
        self.assertGreater(rho_dry, rho_humid)
    
    def test_temperature_effect(self):
        """测试温度对空气密度的影响"""
        # 冷空气密度更大
        rho_cold = WeatherIndexCalculator.air_density(0, 1013.25, 50)
        rho_hot = WeatherIndexCalculator.air_density(40, 1013.25, 50)
        self.assertGreater(rho_cold, rho_hot)


class TestFullWeatherReport(unittest.TestCase):
    """完整天气报告测试"""
    
    def test_basic_report(self):
        """测试基本报告生成"""
        report = WeatherIndexCalculator.full_weather_report(28, 65, 15)
        
        self.assertIn('temperature', report)
        self.assertIn('humidity', report)
        self.assertIn('indices', report)
        self.assertIn('assessments', report)
        
        # 检查索引存在
        self.assertIn('heat_index', report['indices'])
        self.assertIn('wind_chill', report['indices'])
        self.assertIn('apparent_temperature', report['indices'])
        self.assertIn('dew_point', report['indices'])
        self.assertIn('wbgt', report['indices'])
        
        # 检查评估存在
        self.assertIn('comfort_level', report['assessments'])
        self.assertIn('heat_risk', report['assessments'])
    
    def test_report_with_solar(self):
        """测试带太阳辐射的报告"""
        report = WeatherIndexCalculator.full_weather_report(28, 65, 10, 1013.25, 500)
        
        self.assertIsNotNone(report['indices']['uv_index'])
        self.assertIsNotNone(report['assessments']['uv_category'])
    
    def test_report_different_units(self):
        """测试不同单位的报告"""
        report_c = WeatherIndexCalculator.full_weather_report(28, 65, 15)
        report_f = WeatherIndexCalculator.full_weather_report(82.4, 65, 9.32,
                                                             temp_units='fahrenheit',
                                                             speed_units='mph')
        
        # 转换后应该接近
        self.assertAlmostEqual(report_c['indices']['heat_index'],
                              (report_f['indices']['heat_index'] - 32) * 5/9,
                              places=0)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_zero_temperature(self):
        """测试零度"""
        hi = heat_index(0, 50)
        self.assertEqual(hi, 0.0)
        
        wc = wind_chill(0, 30)
        self.assertLess(wc, 0)
        
        dp = dew_point(0, 50)
        self.assertIsInstance(dp, float)
    
    def test_zero_wind(self):
        """测试零风速"""
        wc = wind_chill(-10, 0)
        self.assertEqual(wc, -10.0)  # 无风时风寒指数等于温度
        
        at = apparent_temperature(-10, 50, 0)
        self.assertEqual(at, -10.0)
    
    def test_zero_humidity(self):
        """测试零湿度"""
        dp = dew_point(30, 1)  # 接近零
        self.assertLess(dp, -10)  # 露点应该非常低
    
    def test_high_temperature(self):
        """测试极端高温"""
        hi = heat_index(50, 50)
        self.assertGreater(hi, 50)
    
    def test_negative_temperature(self):
        """测试负温度"""
        wc = wind_chill(-30, 50)
        self.assertLess(wc, -40)


class TestNumericalStability(unittest.TestCase):
    """数值稳定性测试"""
    
    def test_extreme_values(self):
        """测试极端值"""
        # 极端高温高湿
        hi = heat_index(50, 95)
        self.assertIsInstance(hi, float)
        self.assertFalse(math.isnan(hi))
        self.assertFalse(math.isinf(hi))
        
        # 极端低温高风速
        wc = wind_chill(-50, 100)
        self.assertIsInstance(wc, float)
        self.assertFalse(math.isnan(wc))
        self.assertFalse(math.isinf(wc))
    
    def test_precision(self):
        """测试精度"""
        # 多次计算应该得到相同结果
        hi1 = heat_index(35, 70)
        hi2 = heat_index(35, 70)
        self.assertEqual(hi1, hi2)
        
        wc1 = wind_chill(-10, 30)
        wc2 = wind_chill(-10, 30)
        self.assertEqual(wc1, wc2)


if __name__ == '__main__':
    # 运行测试
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # 计算测试数量
    test_count = suite.countTestCases()
    print(f"\n{'='*60}")
    print(f"Weather Index Utils 测试套件")
    print(f"共 {test_count} 个测试用例")
    print(f"{'='*60}\n")
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print(f"\n{'='*60}")
    print(f"测试结果: {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"{'='*60}")
    
    sys.exit(0 if result.wasSuccessful() else 1)