"""
Battery Utils 测试文件
==========================================

测试电池计算工具的各项功能。
"""

import unittest
from mod import (
    BatteryCalculator,
    BatteryType,
    calculate_charge_time,
    estimate_runtime,
    calculate_battery_health
)


class TestChargeTimeCalculation(unittest.TestCase):
    """充电时间计算测试"""
    
    def test_basic_charge_time(self):
        """测试基本充电时间计算"""
        result = calculate_charge_time(3000, 1000)
        self.assertIn('total_hours', result)
        self.assertIn('formatted', result)
        self.assertTrue(result['total_hours'] > 0)
    
    def test_charge_time_with_current_charge(self):
        """测试考虑当前电量的充电时间"""
        result = BatteryCalculator.calculate_charge_time(3000, 1000, 0.85, 50)
        self.assertTrue(result['total_hours'] > 0)
        # 从50%开始充电，时间应该比从0开始短一半左右
        full_result = calculate_charge_time(3000, 1000)
        self.assertTrue(result['total_hours'] < full_result['total_hours'])
    
    def test_charge_time_efficiency(self):
        """测试充电效率对时间的影响"""
        low_eff = BatteryCalculator.calculate_charge_time(3000, 1000, 0.7)
        high_eff = BatteryCalculator.calculate_charge_time(3000, 1000, 0.95)
        # 低效率时充电时间更长
        self.assertTrue(low_eff['total_hours'] > high_eff['total_hours'])
    
    def test_charge_time_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            calculate_charge_time(0, 1000)
        with self.assertRaises(ValueError):
            calculate_charge_time(3000, 0)
        with self.assertRaises(ValueError):
            BatteryCalculator.calculate_charge_time(3000, 1000, 2.0)  # 效率超过1
    
    def test_charge_time_format(self):
        """测试时间格式化"""
        result = calculate_charge_time(3000, 1000)
        self.assertIn('小时', result['formatted'])
        self.assertIn('分钟', result['formatted'])


class TestRuntimeEstimation(unittest.TestCase):
    """续航估算测试"""
    
    def test_basic_runtime(self):
        """测试基本续航估算"""
        runtime = estimate_runtime(3000, 3.7, 2)
        self.assertTrue(runtime > 0)
    
    def test_runtime_with_low_power(self):
        """测试低功耗续航"""
        high_power = estimate_runtime(3000, 3.7, 5)
        low_power = estimate_runtime(3000, 3.7, 1)
        # 低功耗时续航更长
        self.assertTrue(low_power > high_power)
    
    def test_runtime_efficiency(self):
        """测试效率对续航的影响"""
        low_eff = BatteryCalculator.estimate_runtime(3000, 3.7, 2, 0.7)
        high_eff = BatteryCalculator.estimate_runtime(3000, 3.7, 2, 0.95)
        # 高效率时续航更长
        self.assertTrue(high_eff['total_hours'] > low_eff['total_hours'])
    
    def test_runtime_invalid_power(self):
        """测试无效功耗"""
        with self.assertRaises(ValueError):
            estimate_runtime(3000, 3.7, 0)
    
    def test_runtime_format(self):
        """测试续航格式化"""
        result = BatteryCalculator.estimate_runtime(3000, 3.7, 2)
        self.assertIn('hours', result)
        self.assertIn('minutes', result)
        self.assertIn('formatted', result)


class TestBatteryHealth(unittest.TestCase):
    """电池健康度测试"""
    
    def test_basic_health(self):
        """测试基本健康度计算"""
        health = calculate_battery_health(2400, 3000, 100)
        self.assertTrue(0 <= health <= 100)
    
    def test_full_health(self):
        """测试完全健康"""
        health = BatteryCalculator.calculate_battery_health(3000, 3000, 0)
        self.assertAlmostEqual(health['overall_health_percent'], 100, places=1)
        self.assertEqual(health['grade'], 'A')
    
    def test_degraded_health(self):
        """测试衰减健康度"""
        health = BatteryCalculator.calculate_battery_health(2000, 3000, 300)
        self.assertTrue(health['overall_health_percent'] < 80)
        self.assertTrue(health['grade'] in ['C', 'D', 'E'])
    
    def test_battery_type_health(self):
        """测试不同电池类型的健康度"""
        li_ion = BatteryCalculator.calculate_battery_health(2400, 3000, 200, BatteryType.LI_ION)
        li_fepo4 = BatteryCalculator.calculate_battery_health(2400, 3000, 200, BatteryType.LI_FEPO4)
        # 磷酸铁锂循环寿命更长，健康度评估更宽容
        self.assertTrue(li_fepo4['remaining_cycles'] > li_ion['remaining_cycles'])
    
    def test_health_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            calculate_battery_health(2000, 0, 100)


class TestCycleCount(unittest.TestCase):
    """循环次数计算测试"""
    
    def test_basic_cycle_count(self):
        """测试基本循环次数"""
        result = BatteryCalculator.calculate_cycle_count(100, 3)
        self.assertTrue(result['full_cycles'] > 0)
    
    def test_cycle_count_dod(self):
        """测试放电深度影响"""
        shallow = BatteryCalculator.calculate_cycle_count(100, 3, 0.5)
        deep = BatteryCalculator.calculate_cycle_count(100, 3, 0.9)
        # 深放电时等效循环更多
        self.assertTrue(deep['adjusted_cycles'] > shallow['adjusted_cycles'])
    
    def test_cycle_count_invalid(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            BatteryCalculator.calculate_cycle_count(100, 0)
        with self.assertRaises(ValueError):
            BatteryCalculator.calculate_cycle_count(100, 3, 1.5)


class TestDegradationModel(unittest.TestCase):
    """衰减模型测试"""
    
    def test_basic_degradation(self):
        """测试基本衰减预测"""
        result = BatteryCalculator.model_degradation(2)
        self.assertTrue(result['remaining_capacity_percent'] < 100)
        self.assertIn('prediction', result)
    
    def test_temperature_effect(self):
        """测试温度对衰减的影响"""
        cool = BatteryCalculator.model_degradation(2, BatteryType.LI_ION, 365, 20)
        hot = BatteryCalculator.model_degradation(2, BatteryType.LI_ION, 365, 40)
        # 高温加速衰减
        self.assertTrue(hot['total_degradation_percent'] > cool['total_degradation_percent'])
    
    def test_battery_type_degradation(self):
        """测试不同电池类型衰减"""
        li_ion = BatteryCalculator.model_degradation(5, BatteryType.LI_ION)
        li_fepo4 = BatteryCalculator.model_degradation(5, BatteryType.LI_FEPO4)
        # 磷酸铁锂衰减更慢
        self.assertTrue(li_fepo4['remaining_capacity_percent'] > li_ion['remaining_capacity_percent'])
    
    def test_prediction_values(self):
        """测试预测值"""
        result = BatteryCalculator.model_degradation(1)
        self.assertIn('years_to_80_percent', result['prediction'])
        self.assertTrue(result['prediction']['years_to_80_percent'] > 0)


class TestChargingEfficiency(unittest.TestCase):
    """充电效率测试"""
    
    def test_basic_efficiency(self):
        """测试基本效率计算"""
        result = BatteryCalculator.calculate_charging_efficiency(15, 3000, 3.7, 100)
        self.assertTrue(0 <= result['efficiency_percent'] <= 100)
        self.assertIn('grade', result)
    
    def test_high_efficiency(self):
        """测试高效率场景"""
        # 较低的输入能量表示高效充电
        result = BatteryCalculator.calculate_charging_efficiency(12, 3000, 3.7, 100)
        self.assertTrue(result['efficiency_percent'] > 80)
    
    def test_low_efficiency(self):
        """测试低效率场景"""
        # 较高的输入能量表示低效充电
        result = BatteryCalculator.calculate_charging_efficiency(20, 3000, 3.7, 100)
        self.assertTrue(result['efficiency_percent'] < 70)
    
    def test_partial_charge(self):
        """测试部分充电效率"""
        full = BatteryCalculator.calculate_charging_efficiency(15, 3000, 3.7, 100)
        half = BatteryCalculator.calculate_charging_efficiency(8, 3000, 3.7, 50)
        # 部分充电时存储的能量更少


class TestPowerConsumptionAnalysis(unittest.TestCase):
    """功耗分析测试"""
    
    def test_basic_analysis(self):
        """测试基本功耗分析"""
        pattern = {'active': 4, 'idle': 20}
        result = BatteryCalculator.analyze_power_consumption(3000, 3.7, pattern)
        self.assertIn('runtime_days', result)
        self.assertIn('runtime_hours', result)
    
    def test_high_usage(self):
        """测试高使用率场景"""
        light = BatteryCalculator.analyze_power_consumption(3000, 3.7, {'idle': 24})
        heavy = BatteryCalculator.analyze_power_consumption(3000, 3.7, {'active': 24})
        # 重度使用续航更短
        self.assertTrue(heavy['runtime_hours'] < light['runtime_hours'])
    
    def test_scenario_breakdown(self):
        """测试场景分析"""
        pattern = {'active': 4, 'idle': 20}
        result = BatteryCalculator.analyze_power_consumption(3000, 3.7, pattern)
        self.assertIn('scenario_analysis', result)
        self.assertIn('active', result['scenario_analysis'])
        self.assertIn('idle', result['scenario_analysis'])


class TestChargerRecommendation(unittest.TestCase):
    """充电器推荐测试"""
    
    def test_basic_recommendation(self):
        """测试基本推荐"""
        result = BatteryCalculator.recommend_charger(3000)
        self.assertTrue(result['recommended_current_ma'] > 0)
        self.assertIn('estimated_charge_time', result)
    
    def test_fast_charge(self):
        """测试快充推荐"""
        standard = BatteryCalculator.recommend_charger(3000, BatteryType.LI_ION, False)
        fast = BatteryCalculator.recommend_charger(3000, BatteryType.LI_ION, True)
        # 快充电流更大，时间更短
        self.assertTrue(fast['recommended_current_ma'] > standard['recommended_current_ma'])
    
    def test_battery_type_charger(self):
        """测试不同电池类型推荐"""
        li_ion = BatteryCalculator.recommend_charger(3000, BatteryType.LI_ION, True)
        li_po = BatteryCalculator.recommend_charger(3000, BatteryType.LI_PO, True)
        # 锂聚合物支持更高的快充电流
        self.assertTrue(li_po['recommended_current_ma'] >= li_ion['recommended_current_ma'])


class TestBatteryConfiguration(unittest.TestCase):
    """电池配置测试"""
    
    def test_parallel_config(self):
        """测试并联配置"""
        result = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'parallel')
        self.assertEqual(result['total_capacity_mah'], 6000)
        self.assertEqual(result['total_voltage'], 3.7)
    
    def test_series_config(self):
        """测试串联配置"""
        result = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'series')
        self.assertEqual(result['total_capacity_mah'], 3000)
        self.assertEqual(result['total_voltage'], 7.4)
    
    def test_energy_calculation(self):
        """测试能量计算"""
        parallel = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'parallel')
        series = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'series')
        # 两种配置的总能量应该相同
        self.assertAlmostEqual(parallel['total_energy_wh'], series['total_energy_wh'], places=1)
    
    def test_invalid_cells(self):
        """测试无效电池数量"""
        with self.assertRaises(ValueError):
            BatteryCalculator.calculate_parallel_series(0, 3000, 3.7)


class TestBatteryComparison(unittest.TestCase):
    """电池比较测试"""
    
    def test_basic_comparison(self):
        """测试基本比较"""
        batteries = [
            {'name': 'Small', 'capacity_mah': 2000, 'voltage': 3.7},
            {'name': 'Medium', 'capacity_mah': 3000, 'voltage': 3.7},
            {'name': 'Large', 'capacity_mah': 4000, 'voltage': 3.7}
        ]
        result = BatteryCalculator.battery_comparison(batteries)
        self.assertEqual(len(result['rankings']), 3)
        self.assertEqual(result['best']['name'], 'Large')
    
    def test_voltage_comparison(self):
        """测试不同电压比较"""
        batteries = [
            {'name': 'A', 'capacity_mah': 3000, 'voltage': 3.7},
            {'name': 'B', 'capacity_mah': 3000, 'voltage': 7.4}
        ]
        result = BatteryCalculator.battery_comparison(batteries)
        # 高电压电池能量更多
        self.assertEqual(result['best']['name'], 'B')
    
    def test_relative_capacity(self):
        """测试相对容量计算"""
        batteries = [
            {'name': 'A', 'capacity_mah': 3000, 'voltage': 3.7},
            {'name': 'B', 'capacity_mah': 2000, 'voltage': 3.7}
        ]
        result = BatteryCalculator.battery_comparison(batteries)
        self.assertEqual(result['rankings'][0]['relative_capacity_percent'], 100)
        self.assertTrue(result['rankings'][1]['relative_capacity_percent'] < 100)


class TestFullReport(unittest.TestCase):
    """完整报告测试"""
    
    def test_basic_report(self):
        """测试基本报告"""
        report = BatteryCalculator.full_battery_report(3000, 3.7)
        self.assertIn('specs', report)
        self.assertIn('charging', report)
        self.assertIn('runtime', report)
        self.assertIn('tips', report)
    
    def test_report_with_health(self):
        """测试带健康度的报告"""
        report = BatteryCalculator.full_battery_report(3000, 3.7, BatteryType.LI_ION, 100, 2800)
        self.assertIsNotNone(report['health'])
        self.assertTrue(report['health']['overall_health_percent'] < 100)
    
    def test_report_spec_accuracy(self):
        """测试规格准确性"""
        report = BatteryCalculator.full_battery_report(4000, 3.8)
        self.assertEqual(report['specs']['capacity_mah'], 4000)
        self.assertEqual(report['specs']['voltage'], 3.8)
        expected_energy = 4000 / 1000 * 3.8
        self.assertEqual(report['specs']['energy_wh'], expected_energy)


class TestBatteryProperties(unittest.TestCase):
    """电池属性测试"""
    
    def test_battery_type_properties(self):
        """测试电池类型属性"""
        props = BatteryCalculator.BATTERY_PROPERTIES
        self.assertTrue(len(props) > 0)
        
        for battery_type in BatteryType:
            self.assertIn(battery_type, props)
            self.assertIn('nominal_voltage', props[battery_type])
            self.assertIn('energy_density', props[battery_type])
            self.assertIn('cycle_life', props[battery_type])
    
    def test_device_power_consumption(self):
        """测试设备功耗参考"""
        consumption = BatteryCalculator.DEVICE_POWER_CONSUMPTION
        self.assertTrue(len(consumption) > 0)
        self.assertIn('smartphone_idle', consumption)
        self.assertIn('laptop_idle', consumption)


if __name__ == '__main__':
    unittest.main(verbosity=2)