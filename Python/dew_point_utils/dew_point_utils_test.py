"""
Dew Point Utilities 测试套件

测试所有露点计算功能
"""

import unittest
import math
from dew_point_utils import (
    saturation_vapor_pressure,
    vapor_pressure,
    dew_point,
    frost_point,
    absolute_humidity,
    relative_humidity_from_dew_point,
    wet_bulb_temperature,
    heat_index,
    comfort_level,
    ComfortLevel,
    mixing_ratio,
    specific_humidity,
    analyze_humidity,
    HumidityData,
    dew_point_depression,
    fog_risk,
    condensation_prediction,
    temperature_for_target_rh,
    humidity_ratio,
    enthalpy
)


class TestSaturationVaporPressure(unittest.TestCase):
    """测试饱和蒸汽压计算"""
    
    def test_standard_temperature(self):
        """测试标准温度下的饱和蒸汽压"""
        # 20°C 时饱和蒸汽压约为 23.4 hPa (Magnus 公式)
        svp = saturation_vapor_pressure(20)
        self.assertAlmostEqual(svp, 23.3, places=1)
    
    def test_freezing_point(self):
        """测试冰点时的饱和蒸汽压"""
        svp = saturation_vapor_pressure(0)
        self.assertAlmostEqual(svp, 6.11, places=1)
    
    def test_high_temperature(self):
        """测试高温下的饱和蒸汽压"""
        # 100°C 时 Magnus 公式给出的值约 1038 hPa
        svp = saturation_vapor_pressure(100)
        self.assertGreater(svp, 1000)  # 应大于 1000 hPa
        self.assertLess(svp, 1050)  # Magnus 公式在极端温度下略有偏差
    
    def test_negative_temperature(self):
        """测试负温度"""
        svp = saturation_vapor_pressure(-10)
        self.assertGreater(svp, 2)
        self.assertLess(svp, 3)
    
    def test_over_ice(self):
        """测试冰面上的饱和蒸汽压"""
        svp_ice = saturation_vapor_pressure(-10, over_ice=True)
        svp_water = saturation_vapor_pressure(-10, over_ice=False)
        # 冰面饱和蒸汽压应略低
        self.assertLess(svp_ice, svp_water)


class TestVaporPressure(unittest.TestCase):
    """测试水蒸气分压计算"""
    
    def test_fifty_percent_rh(self):
        """测试 50% 相对湿度"""
        vp = vapor_pressure(20, 50)
        svp = saturation_vapor_pressure(20)
        self.assertAlmostEqual(vp, svp * 0.5, places=1)
    
    def test_hundred_percent_rh(self):
        """测试 100% 相对湿度（饱和）"""
        vp = vapor_pressure(20, 100)
        svp = saturation_vapor_pressure(20)
        self.assertAlmostEqual(vp, svp, places=2)
    
    def test_zero_percent_rh(self):
        """测试 0% 相对湿度"""
        vp = vapor_pressure(20, 0)
        self.assertAlmostEqual(vp, 0, places=2)
    
    def test_clamped_values(self):
        """测试超出范围的值被限制"""
        vp1 = vapor_pressure(20, 150)  # 超过 100%
        vp2 = vapor_pressure(20, 100)
        self.assertAlmostEqual(vp1, vp2, places=2)
        
        vp3 = vapor_pressure(20, -10)  # 低于 0%
        vp4 = vapor_pressure(20, 0)
        self.assertAlmostEqual(vp3, vp4, places=2)


class TestDewPoint(unittest.TestCase):
    """测试露点计算"""
    
    def test_standard_case(self):
        """测试标准情况"""
        # 25°C, 50%RH 的露点约为 13.9°C
        dp = dew_point(25, 50)
        self.assertAlmostEqual(dp, 13.9, places=0)
    
    def test_saturated_air(self):
        """测试饱和空气"""
        # 100% RH 时露点等于温度
        dp = dew_point(20, 100)
        self.assertAlmostEqual(dp, 20, places=0)
    
    def test_dry_air(self):
        """测试干燥空气"""
        # 低湿度时露点远低于温度
        dp = dew_point(30, 20)
        self.assertLess(dp, 5)
    
    def test_high_humidity(self):
        """测试高湿度"""
        dp = dew_point(25, 90)
        self.assertGreater(dp, 22)
        self.assertLess(dp, 25)
    
    def test_known_values(self):
        """测试已知值"""
        # 20°C, 50%RH 的露点约为 9.3°C
        dp = dew_point(20, 50)
        self.assertAlmostEqual(dp, 9.3, places=0)


class TestFrostPoint(unittest.TestCase):
    """测试霜点计算"""
    
    def test_subzero_frost_point(self):
        """测试负温下的霜点"""
        fp = frost_point(-5, 80)
        # 霜点应低于同条件下的露点
        self.assertLess(fp, -5)


class TestAbsoluteHumidity(unittest.TestCase):
    """测试绝对湿度计算"""
    
    def test_standard_case(self):
        """测试标准情况"""
        # 20°C, 50%RH 的绝对湿度约为 8.65 g/m³
        ah = absolute_humidity(20, 50)
        self.assertAlmostEqual(ah, 8.65, places=1)
    
    def test_saturated_air(self):
        """测试饱和空气"""
        ah = absolute_humidity(20, 100)
        ah_half = absolute_humidity(20, 50)
        self.assertAlmostEqual(ah, ah_half * 2, places=1)


class TestRelativeHumidityFromDewPoint(unittest.TestCase):
    """测试从露点反算相对湿度"""
    
    def test_round_trip(self):
        """测试往返计算"""
        temp = 25
        rh = 60
        dp = dew_point(temp, rh)
        rh_back = relative_humidity_from_dew_point(temp, dp)
        self.assertAlmostEqual(rh, rh_back, places=0)


class TestWetBulbTemperature(unittest.TestCase):
    """测试湿球温度计算"""
    
    def test_wet_bulb_lower_than_dry(self):
        """湿球温度应低于干球温度"""
        wb = wet_bulb_temperature(25, 50)
        self.assertLess(wb, 25)
    
    def test_saturated_air(self):
        """饱和空气的湿球温度接近干球温度"""
        wb = wet_bulb_temperature(20, 100)
        self.assertAlmostEqual(wb, 20, places=0)
    
    def test_dry_air(self):
        """干燥空气的湿球温度更低"""
        wb_dry = wet_bulb_temperature(25, 20)
        wb_humid = wet_bulb_temperature(25, 80)
        self.assertLess(wb_dry, wb_humid)


class TestHeatIndex(unittest.TestCase):
    """测试热指数计算"""
    
    def test_valid_conditions(self):
        """测试满足条件的热指数"""
        hi = heat_index(30, 70)
        # 30°C, 70%RH 应感觉比 30°C 更热
        self.assertGreater(hi, 30)
    
    def test_invalid_conditions_low_temp(self):
        """测试低温条件返回原温度"""
        hi = heat_index(20, 70)
        self.assertEqual(hi, 20)
    
    def test_invalid_conditions_low_rh(self):
        """测试低湿度条件返回原温度"""
        hi = heat_index(30, 30)
        self.assertEqual(hi, 30)


class TestComfortLevel(unittest.TestCase):
    """测试舒适度评估"""
    
    def test_comfortable(self):
        """测试舒适范围"""
        self.assertEqual(comfort_level(13), ComfortLevel.COMFORTABLE)
        self.assertEqual(comfort_level(15), ComfortLevel.COMFORTABLE)
    
    def test_dry(self):
        """测试干燥"""
        self.assertEqual(comfort_level(11), ComfortLevel.DRY)
        self.assertEqual(comfort_level(12), ComfortLevel.DRY)
    
    def test_very_dry(self):
        """测试非常干燥"""
        self.assertEqual(comfort_level(5), ComfortLevel.VERY_DRY)
    
    def test_humid(self):
        """测试潮湿"""
        self.assertEqual(comfort_level(17), ComfortLevel.HUMID)
    
    def test_very_humid(self):
        """测试非常潮湿"""
        self.assertEqual(comfort_level(20), ComfortLevel.VERY_HUMID)
    
    def test_oppressive(self):
        """测试闷热"""
        self.assertEqual(comfort_level(25), ComfortLevel.OPPRESSIVE)


class TestMixingRatio(unittest.TestCase):
    """测试混合比计算"""
    
    def test_standard_case(self):
        """测试标准情况"""
        mr = mixing_ratio(20, 50)
        # 应约为 7.3 g/kg
        self.assertAlmostEqual(mr, 7.3, places=0)
    
    def test_zero_rh(self):
        """测试零湿度"""
        mr = mixing_ratio(20, 0)
        self.assertAlmostEqual(mr, 0, places=2)


class TestSpecificHumidity(unittest.TestCase):
    """测试比湿计算"""
    
    def test_lower_than_mixing_ratio(self):
        """比湿应略低于混合比"""
        mr = mixing_ratio(20, 50)
        sh = specific_humidity(20, 50)
        self.assertLess(sh, mr)


class TestAnalyzeHumidity(unittest.TestCase):
    """测试综合分析"""
    
    def test_returns_humidity_data(self):
        """测试返回正确类型"""
        data = analyze_humidity(25, 60)
        self.assertIsInstance(data, HumidityData)
    
    def test_all_fields_populated(self):
        """测试所有字段都有值"""
        data = analyze_humidity(25, 60)
        self.assertEqual(data.temperature, 25)
        self.assertEqual(data.relative_humidity, 60)
        self.assertIsInstance(data.dew_point, float)
        self.assertIsInstance(data.absolute_humidity, float)
        self.assertIsInstance(data.vapor_pressure, float)
        self.assertIsInstance(data.saturation_vapor_pressure, float)
        self.assertIsInstance(data.comfort_level, ComfortLevel)
    
    def test_consistency(self):
        """测试数据一致性"""
        data = analyze_humidity(20, 50)
        
        # 露点应与单独计算一致
        expected_dp = dew_point(20, 50)
        self.assertAlmostEqual(data.dew_point, expected_dp, places=2)
        
        # 舒适度应与露点对应
        expected_comfort = comfort_level(expected_dp)
        self.assertEqual(data.comfort_level, expected_comfort)


class TestDewPointDepression(unittest.TestCase):
    """测试露点差计算"""
    
    def test_positive_depression(self):
        """露点差应为正（除非饱和）"""
        dpd = dew_point_depression(20, 50)
        self.assertGreater(dpd, 0)
    
    def test_saturated_air(self):
        """饱和空气露点差接近零"""
        dpd = dew_point_depression(20, 100)
        self.assertAlmostEqual(dpd, 0, places=1)
    
    def test_dry_air(self):
        """干燥空气露点差大"""
        dpd = dew_point_depression(30, 20)
        self.assertGreater(dpd, 15)


class TestFogRisk(unittest.TestCase):
    """测试雾风险评估"""
    
    def test_high_risk(self):
        """测试高风险"""
        risk = fog_risk(15, 98)
        self.assertIn("高", risk)
    
    def test_no_risk(self):
        """测试无风险"""
        risk = fog_risk(25, 40)
        self.assertEqual(risk, "无风险")
    
    def test_medium_risk(self):
        """测试中等风险"""
        risk = fog_risk(20, 85)
        self.assertIn("风险", risk)


class TestCondensationPrediction(unittest.TestCase):
    """测试结露预测"""
    
    def test_will_condense(self):
        """测试会结露"""
        will_cond, msg = condensation_prediction(25, 80, 15)
        self.assertTrue(will_cond)
        self.assertIn("结露", msg)
    
    def test_will_not_condense(self):
        """测试不会结露"""
        will_cond, msg = condensation_prediction(20, 50, 20)
        self.assertFalse(will_cond)
        self.assertIn("不会", msg)
    
    def test_no_surface_temp(self):
        """测试无表面温度时假设等于气温"""
        will_cond, msg = condensation_prediction(20, 50)
        self.assertFalse(will_cond)


class TestTemperatureForTargetRH(unittest.TestCase):
    """测试达到目标湿度的温度计算"""
    
    def test_round_trip(self):
        """测试往返计算"""
        # 从露点 10°C 计算达到 50% RH 的温度
        temp = temperature_for_target_rh(10, 50)
        # 验证该温度下露点确实接近 10°C
        dp = dew_point(temp, 50)
        self.assertAlmostEqual(dp, 10, places=0)


class TestHumidityRatio(unittest.TestCase):
    """测试湿度比计算"""
    
    def test_equals_mixing_ratio_divided(self):
        """湿度比应等于混合比/1000"""
        hr = humidity_ratio(20, 50)
        mr = mixing_ratio(20, 50)
        self.assertAlmostEqual(hr, mr / 1000, places=4)


class TestEnthalpy(unittest.TestCase):
    """测试焓计算"""
    
    def test_positive_value(self):
        """焓值应为正"""
        e = enthalpy(20, 50)
        self.assertGreater(e, 0)
    
    def test_increases_with_temperature(self):
        """焓值随温度增加"""
        e1 = enthalpy(15, 50)
        e2 = enthalpy(25, 50)
        self.assertLess(e1, e2)
    
    def test_increases_with_humidity(self):
        """焓值随湿度增加"""
        e1 = enthalpy(20, 30)
        e2 = enthalpy(20, 70)
        self.assertLess(e1, e2)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_rh(self):
        """测试 0% 湿度"""
        dp = dew_point(20, 0.1)  # 使用很小的值避免 log(0)
        self.assertLess(dp, -50)  # 应该是非常低的值
    
    def test_hundred_rh(self):
        """测试 100% 湿度"""
        dp = dew_point(20, 100)
        self.assertAlmostEqual(dp, 20, places=0)
    
    def test_very_high_temperature(self):
        """测试极高温度"""
        dp = dew_point(50, 50)
        self.assertGreater(dp, 30)
        self.assertLess(dp, 50)
    
    def test_very_low_temperature(self):
        """测试极低温度"""
        svp = saturation_vapor_pressure(-40)
        self.assertGreater(svp, 0)
        self.assertLess(svp, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)