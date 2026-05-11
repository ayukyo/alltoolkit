"""
Fuel Efficiency Utils - 单元测试
=================================

测试燃油效率计算工具的所有功能。

运行: python -m pytest fuel_efficiency_utils_test.py -v
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    FuelEfficiencyCalculator, FuelType,
    mpg_to_lp100k, lp100k_to_mpg,
    calculate_fuel_cost, calculate_co2
)


class TestUnitConversion(unittest.TestCase):
    """单位转换测试"""
    
    def test_mpg_to_lp100k_us_gallon(self):
        """测试 MPG 转 L/100km (美制加仑)"""
        # 30 MPG ≈ 7.84 L/100km
        result = mpg_to_lp100k(30)
        self.assertAlmostEqual(result, 7.84, places=1)
        
        # 25 MPG ≈ 9.41 L/100km
        result = mpg_to_lp100k(25)
        self.assertAlmostEqual(result, 9.41, places=1)
        
        # 50 MPG ≈ 4.70 L/100km
        result = mpg_to_lp100k(50)
        self.assertAlmostEqual(result, 4.70, places=1)
    
    def test_mpg_to_lp100k_uk_gallon(self):
        """测试 MPG 转 L/100km (英制加仑)"""
        # 30 MPG (英制) ≈ 9.42 L/100km
        result = mpg_to_lp100k(30, us_gallon=False)
        self.assertAlmostEqual(result, 9.42, places=1)
    
    def test_lp100k_to_mpg_us_gallon(self):
        """测试 L/100km 转 MPG (美制加仑)"""
        # 7.8 L/100km ≈ 30.2 MPG
        result = lp100k_to_mpg(7.8)
        self.assertAlmostEqual(result, 30.2, places=0)
        
        # 10 L/100km ≈ 23.5 MPG
        result = lp100k_to_mpg(10)
        self.assertAlmostEqual(result, 23.5, places=0)
    
    def test_lp100k_to_mpg_uk_gallon(self):
        """测试 L/100km 转 MPG (英制加仑)"""
        # 7.8 L/100km ≈ 36.3 MPG (英制)
        result = lp100k_to_mpg(7.8, us_gallon=False)
        self.assertAlmostEqual(result, 36.3, places=0)
    
    def test_km_per_liter_conversion(self):
        """测试 km/L 转换"""
        # 12.8 km/L = 7.81 L/100km
        result = FuelEfficiencyCalculator.km_per_liter_to_lp100k(12.8)
        self.assertAlmostEqual(result, 7.81, places=1)
        
        # 7.81 L/100km = 12.8 km/L
        result = FuelEfficiencyCalculator.lp100k_to_km_per_liter(7.81)
        self.assertAlmostEqual(result, 12.8, places=1)
    
    def test_round_trip_conversion(self):
        """测试往返转换精度"""
        mpg_values = [20, 25, 30, 35, 40, 50]
        for mpg in mpg_values:
            lp100k = mpg_to_lp100k(mpg)
            mpg_back = lp100k_to_mpg(lp100k)
            self.assertAlmostEqual(mpg, mpg_back, places=0, 
                                msg=f"Round trip failed for {mpg} MPG")
    
    def test_invalid_mpg(self):
        """测试无效 MPG 值"""
        with self.assertRaises(ValueError):
            mpg_to_lp100k(0)
        with self.assertRaises(ValueError):
            mpg_to_lp100k(-5)
    
    def test_invalid_lp100k(self):
        """测试无效 L/100km 值"""
        with self.assertRaises(ValueError):
            lp100k_to_mpg(0)
        with self.assertRaises(ValueError):
            lp100k_to_mpg(-5)


class TestFuelCostCalculation(unittest.TestCase):
    """燃油成本计算测试"""
    
    def test_basic_fuel_cost(self):
        """测试基本燃油成本计算"""
        # 500公里，8L/100km，8.5元/升 = 340元
        cost = calculate_fuel_cost(500, 8, 8.5)
        self.assertEqual(cost, 340.0)
        
        # 100公里，10L/100km，7元/升 = 70元
        cost = calculate_fuel_cost(100, 10, 7)
        self.assertEqual(cost, 70.0)
    
    def test_fuel_cost_mpg(self):
        """测试 MPG 单位的燃油成本计算"""
        # 注意：fuel_price 参数始终按每升计算，即使使用 MPG 单位
        # 300英里，30 MPG
        # 转换: 300 miles = 482.8 km, 30 MPG = 7.84 L/100km
        # 需燃油: 482.8 * 7.84 / 100 = 37.9 升
        # 成本: 37.9 升 * $3.5/升 = $132.5
        
        # 如果油价是 $3.5/加仑，需先转换为 $0.926/升
        # 实际成本: 37.9 升 * $0.926 = $35
        
        # 测试使用每升价格
        cost = FuelEfficiencyCalculator.calculate_fuel_cost(
            300, 30, 0.926, 'mpg', 'mile'  # $3.5/gallon = $0.926/liter
        )
        self.assertAlmostEqual(cost, 35.0, places=0)
    
    def test_fuel_cost_km_per_liter(self):
        """测试 km/L 单位的燃油成本计算"""
        # 200公里，12.5 km/L，8元/升
        # = 200/12.5 * 8 = 128元
        cost = FuelEfficiencyCalculator.calculate_fuel_cost(
            200, 12.5, 8, 'kmpl'
        )
        self.assertEqual(cost, 128.0)


class TestRangeCalculation(unittest.TestCase):
    """续航里程计算测试"""
    
    def test_basic_range(self):
        """测试基本续航计算"""
        # 50升油箱，8L/100km = 625公里
        result = FuelEfficiencyCalculator.calculate_range(50, 8)
        self.assertEqual(result, 625.0)
        
        # 60升油箱，6L/100km = 1000公里
        result = FuelEfficiencyCalculator.calculate_range(60, 6)
        self.assertEqual(result, 1000.0)
    
    def test_range_with_gallons(self):
        """测试加仑单位的续航计算"""
        # 15美制加仑，30 MPG
        # = 15 * 30 = 450英里 ≈ 724公里
        result = FuelEfficiencyCalculator.calculate_range(
            15, 30, 'mpg', 'us_gallon'
        )
        self.assertAlmostEqual(result, 724, places=0)
    
    def test_range_with_mpg(self):
        """测试 MPG 效率的续航计算"""
        # 50升，30 MPG
        lp100k = mpg_to_lp100k(30)
        expected_range = 50 / lp100k * 100
        
        result = FuelEfficiencyCalculator.calculate_range(50, 30, 'mpg')
        self.assertAlmostEqual(result, expected_range, places=0)


class TestCO2Emissions(unittest.TestCase):
    """碳排放计算测试"""
    
    def test_gasoline_emissions(self):
        """测试汽油车碳排放"""
        # 100公里，8L/100km，汽油
        # = 8升 * 2.31 kg/L = 18.48 kg CO2
        emissions = FuelEfficiencyCalculator.calculate_co2_emissions(
            100, 8, FuelType.GASOLINE
        )
        self.assertAlmostEqual(emissions, 18.48, places=1)
    
    def test_diesel_emissions(self):
        """测试柴油车碳排放"""
        # 100公里，6L/100km，柴油
        # = 6升 * 2.68 kg/L = 16.08 kg CO2
        emissions = FuelEfficiencyCalculator.calculate_co2_emissions(
            100, 6, FuelType.DIESEL
        )
        self.assertAlmostEqual(emissions, 16.08, places=1)
    
    def test_electric_zero_direct_emissions(self):
        """测试电动车直接排放为零"""
        emissions = FuelEfficiencyCalculator.calculate_co2_emissions(
            100, 15, FuelType.ELECTRIC
        )
        self.assertEqual(emissions, 0.0)
    
    def test_electric_indirect_emissions(self):
        """测试电动车间接排放"""
        # 100公里，15 kWh/100km，中国电网
        # = 15 kWh * 0.5839 kg/kWh = 8.76 kg CO2
        emissions = FuelEfficiencyCalculator.calculate_electric_emissions(
            100, 15, 'china'
        )
        self.assertAlmostEqual(emissions, 8.76, places=1)
    
    def test_distance_unit_conversion(self):
        """测试距离单位转换"""
        # 62.14英里 (约100公里)，8L/100km
        emissions_miles = FuelEfficiencyCalculator.calculate_co2_emissions(
            62.14, 8, FuelType.GASOLINE, distance_unit='mile'
        )
        emissions_km = FuelEfficiencyCalculator.calculate_co2_emissions(
            100, 8, FuelType.GASOLINE
        )
        self.assertAlmostEqual(emissions_miles, emissions_km, places=0)


class TestAnnualCostCalculation(unittest.TestCase):
    """年度成本计算测试"""
    
    def test_annual_fuel_cost(self):
        """测试年度燃油成本"""
        # 年行驶15000公里，8L/100km，8.5元/升
        result = FuelEfficiencyCalculator.calculate_annual_fuel_cost(15000, 8, 8.5)
        
        # 年成本 = 15000 * 8 / 100 * 8.5 = 10200元
        self.assertEqual(result['annual_cost'], 10200.0)
        # 月成本
        self.assertEqual(result['monthly_cost'], 850.0)
        # 燃油消耗 = 15000 * 8 / 100 = 1200升
        self.assertEqual(result['fuel_consumed_liters'], 1200.0)
    
    def test_monthly_calculation(self):
        """测试月度计算"""
        result = FuelEfficiencyCalculator.calculate_annual_fuel_cost(12000, 10, 7)
        # 年成本 = 12000 * 10 / 100 * 7 = 8400元
        # 月成本 = 8400 / 12 = 700元
        self.assertEqual(result['monthly_cost'], 700.0)


class TestVehicleComparison(unittest.TestCase):
    """车辆对比测试"""
    
    def test_vehicle_comparison(self):
        """测试车辆对比"""
        result = FuelEfficiencyCalculator.compare_vehicles(
            500, 10, 6, 8.5
        )
        
        # 车辆A: 500 * 10 / 100 * 8.5 = 425元
        self.assertEqual(result['vehicle1_cost'], 425.0)
        # 车辆B: 500 * 6 / 100 * 8.5 = 255元
        self.assertEqual(result['vehicle2_cost'], 255.0)
        # 节省: 425 - 255 = 170元
        self.assertEqual(result['savings'], 170.0)
        self.assertEqual(result['more_efficient'], 'vehicle2')
    
    def test_efficiency_improvement_percentage(self):
        """测试效率提升百分比"""
        result = FuelEfficiencyCalculator.compare_vehicles(1000, 10, 8, 8)
        # 提升百分比 = (800 - 640) / 800 * 100 = 20%
        self.assertEqual(result['percentage_improvement'], 20.0)


class TestEfficiencyRating(unittest.TestCase):
    """效率评级测试"""
    
    def test_excellent_efficiency(self):
        """测试卓越效率评级"""
        rating = FuelEfficiencyCalculator.efficiency_rating(4)
        self.assertEqual(rating[0], 'A+')
        self.assertEqual(rating[1], '卓越')
    
    def test_good_efficiency(self):
        """测试良好效率评级"""
        rating = FuelEfficiencyCalculator.efficiency_rating(8)
        self.assertIn(rating[0], ['A', 'B+', 'B'])
    
    def test_poor_efficiency(self):
        """测试较差效率评级"""
        rating = FuelEfficiencyCalculator.efficiency_rating(15)
        self.assertIn(rating[0], ['D', 'E'])
    
    def test_suv_efficiency(self):
        """测试 SUV 效率评级"""
        # SUV 的评级标准不同
        rating_suv = FuelEfficiencyCalculator.efficiency_rating(9, 'suv')
        rating_car = FuelEfficiencyCalculator.efficiency_rating(9, 'car')
        # SUV 的评级应该比轿车更宽松
        self.assertIn(rating_suv[0], ['A+', 'A', 'B+'])
    
    def test_mpg_efficiency_rating(self):
        """测试 MPG 单位的效率评级"""
        # 50 MPG ≈ 4.7 L/100km，应该是 A+
        rating = FuelEfficiencyCalculator.efficiency_rating(50, efficiency_unit='mpg')
        self.assertEqual(rating[0], 'A+')


class TestBreakEvenAnalysis(unittest.TestCase):
    """回本分析测试"""
    
    def test_break_even_calculation(self):
        """测试回本计算"""
        # 省油车: 20万，5L/100km
        # 普通车: 15万，8L/100km
        # 差价: 5万
        # 每公里节省: (8-5)/100 * 8.5 = 0.255元
        # 回本里程: 50000 / 0.255 ≈ 196078公里
        result = FuelEfficiencyCalculator.calculate_break_even(
            200000, 5, 150000, 8, 8.5
        )
        
        self.assertEqual(result['price_difference'], 50000)
        self.assertGreater(result['break_even_km'], 0)
        self.assertGreater(result['break_even_years'], 0)
        self.assertEqual(result['savings_per_km'], 0.255)
    
    def test_no_break_even(self):
        """测试无法回本的情况"""
        # 如果省油车油耗更高，则无法回本
        result = FuelEfficiencyCalculator.calculate_break_even(
            200000, 10, 150000, 8, 8.5
        )
        
        self.assertEqual(result['break_even_km'], -1)
        self.assertIn('无法回本', result['message'])


class TestTripCalculation(unittest.TestCase):
    """旅行计算测试"""
    
    def test_trip_fuel_calculation(self):
        """测试旅行燃油计算"""
        result = FuelEfficiencyCalculator.calculate_trip_fuel(
            300, 8, 8.5, 4
        )
        
        # 燃油量 = 300 * 8 / 100 = 24升
        self.assertEqual(result['fuel_needed_liters'], 24.0)
        # 总成本 = 24 * 8.5 = 204元
        self.assertEqual(result['total_cost'], 204.0)
        # 人均成本 = 204 / 4 = 51元
        self.assertEqual(result['cost_per_passenger'], 51.0)
        # 每公里成本 = 204 / 300 = 0.68元
        self.assertAlmostEqual(result['cost_per_km'], 0.68, places=2)
    
    def test_trip_distance_conversion(self):
        """测试旅行距离转换"""
        # 186.4英里 ≈ 300公里
        result = FuelEfficiencyCalculator.calculate_trip_fuel(
            186.4, 8, 8.5, distance_unit='mile'
        )
        
        self.assertAlmostEqual(result['distance_km'], 300, places=0)


class TestFullEfficiencyReport(unittest.TestCase):
    """完整效率报告测试"""
    
    def test_report_structure(self):
        """测试报告结构"""
        report = FuelEfficiencyCalculator.full_efficiency_report(8)
        
        self.assertIn('efficiency', report)
        self.assertIn('annual_costs', report)
        self.assertIn('co2_emissions_kg', report)
        self.assertIn('efficiency_rating', report)
        self.assertIn('fuel_info', report)
    
    def test_report_efficiency_conversion(self):
        """测试报告中的效率转换"""
        report = FuelEfficiencyCalculator.full_efficiency_report(8)
        
        # L/100km
        self.assertEqual(report['efficiency']['lp100k'], 8)
        # MPG 转换
        self.assertGreater(report['efficiency']['mpg_us'], 0)
        self.assertGreater(report['efficiency']['mpg_uk'], 0)
        # km/L 转换
        self.assertAlmostEqual(report['efficiency']['km_per_liter'], 12.5, places=1)
    
    def test_report_annual_costs(self):
        """测试报告年度成本"""
        report = FuelEfficiencyCalculator.full_efficiency_report(
            8, 15000, 8.5, FuelType.GASOLINE
        )
        
        # 年成本 = 15000 * 8 / 100 * 8.5 = 10200
        self.assertEqual(report['annual_costs']['annual_cost'], 10200.0)
        self.assertEqual(report['annual_costs']['monthly_cost'], 850.0)
    
    def test_report_diesel(self):
        """测试柴油车报告"""
        report = FuelEfficiencyCalculator.full_efficiency_report(
            6, 15000, 7.5, FuelType.DIESEL
        )
        
        self.assertEqual(report['fuel_info']['type'], 'diesel')
        self.assertEqual(report['fuel_info']['name_cn'], '柴油')
    
    def test_report_efficiency_rating(self):
        """测试报告效率评级"""
        report_a = FuelEfficiencyCalculator.full_efficiency_report(5)
        self.assertEqual(report_a['efficiency_rating']['grade'], 'A+')
        
        # 12 L/100km 落在 D 范围 (11 < 12 < 13)
        report_d = FuelEfficiencyCalculator.full_efficiency_report(12)
        self.assertEqual(report_d['efficiency_rating']['grade'], 'D')


class TestFuelProperties(unittest.TestCase):
    """燃油属性测试"""
    
    def test_fuel_properties_exist(self):
        """测试燃油属性存在"""
        for fuel_type in [FuelType.GASOLINE, FuelType.DIESEL, 
                         FuelType.HYBRID, FuelType.ELECTRIC]:
            props = FuelEfficiencyCalculator.FUEL_PROPERTIES[fuel_type]
            self.assertIn('density', props)
            self.assertIn('co2_per_liter', props)
            self.assertIn('name_cn', props)
    
    def test_grid_emission_factors(self):
        """测试电网排放因子"""
        factors = FuelEfficiencyCalculator.GRID_EMISSION_FACTORS
        
        self.assertIn('china', factors)
        self.assertIn('us', factors)
        self.assertIn('eu', factors)
        self.assertGreater(factors['china'], 0)
        self.assertGreater(factors['us'], 0)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_zero_distance(self):
        """测试零距离"""
        cost = FuelEfficiencyCalculator.calculate_fuel_cost(0, 8, 8.5)
        self.assertEqual(cost, 0)
    
    def test_very_efficient_vehicle(self):
        """测试极高效车辆"""
        rating = FuelEfficiencyCalculator.efficiency_rating(2)
        self.assertEqual(rating[0], 'A+')
    
    def test_very_inefficient_vehicle(self):
        """测试极低效车辆"""
        rating = FuelEfficiencyCalculator.efficiency_rating(25)
        self.assertEqual(rating[0], 'E')
    
    def test_single_passenger_trip(self):
        """测试单人旅行"""
        result = FuelEfficiencyCalculator.calculate_trip_fuel(100, 8, 8.5, 1)
        self.assertEqual(result['cost_per_passenger'], result['total_cost'])


if __name__ == '__main__':
    unittest.main(verbosity=2)