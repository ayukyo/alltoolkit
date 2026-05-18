"""
燃油消耗计算工具测试
"""

import unittest
from mod import (
    mpg_to_liters_per_100km,
    liters_per_100km_to_mpg,
    km_per_liter_to_mpg,
    mpg_to_km_per_liter,
    calculate_consumption,
    calculate_trip_fuel,
    calculate_carbon_emission,
    estimate_range,
    compare_vehicles,
    get_consumption_rating,
    quick_mpg_convert,
    FuelConsumptionResult,
    TripFuelResult,
    CarbonEmissionResult,
    CO2_FACTORS
)


class TestUnitConversion(unittest.TestCase):
    """单位转换测试"""
    
    def test_mpg_to_liters_per_100km(self):
        """MPG 转 L/100km"""
        # 30 MPG ≈ 7.84 L/100km
        result = mpg_to_liters_per_100km(30)
        self.assertAlmostEqual(result, 7.84, places=2)
        
        # 25 MPG ≈ 9.41 L/100km
        result = mpg_to_liters_per_100km(25)
        self.assertAlmostEqual(result, 9.41, places=2)
        
        # 40 MPG ≈ 5.88 L/100km
        result = mpg_to_liters_per_100km(40)
        self.assertAlmostEqual(result, 5.88, places=2)
    
    def test_liters_per_100km_to_mpg(self):
        """L/100km 转 MPG"""
        # 8 L/100km ≈ 29.40 MPG
        result = liters_per_100km_to_mpg(8)
        self.assertAlmostEqual(result, 29.40, places=2)
        
        # 10 L/100km ≈ 23.52 MPG
        result = liters_per_100km_to_mpg(10)
        self.assertAlmostEqual(result, 23.52, places=2)
    
    def test_roundtrip_conversion(self):
        """往返转换验证"""
        original = 30
        converted = mpg_to_liters_per_100km(original)
        back = liters_per_100km_to_mpg(converted)
        self.assertAlmostEqual(original, back, places=1)
    
    def test_km_per_liter_conversions(self):
        """公里每升转换"""
        # 12.5 km/L ≈ 29.40 MPG
        result = km_per_liter_to_mpg(12.5)
        self.assertAlmostEqual(result, 29.40, places=2)
        
        # 30 MPG ≈ 12.75 km/L
        result = mpg_to_km_per_liter(30)
        self.assertAlmostEqual(result, 12.75, places=2)
    
    def test_invalid_values(self):
        """无效值测试"""
        with self.assertRaises(ValueError):
            mpg_to_liters_per_100km(0)
        
        with self.assertRaises(ValueError):
            mpg_to_liters_per_100km(-10)
        
        with self.assertRaises(ValueError):
            liters_per_100km_to_mpg(0)


class TestCalculateConsumption(unittest.TestCase):
    """油耗计算测试"""
    
    def test_calculate_from_miles_gallons(self):
        """从英里和加仑计算"""
        result = calculate_consumption(distance_miles=300, fuel_gallons=10)
        self.assertEqual(result.mpg, 30.0)
        self.assertAlmostEqual(result.liters_per_100km, 7.84, places=2)
    
    def test_calculate_from_km_liters(self):
        """从公里和升计算"""
        # 500公里用40升 = 8 L/100km
        result = calculate_consumption(distance_km=500, fuel_liters=40)
        self.assertAlmostEqual(result.liters_per_100km, 8.0, places=2)
        self.assertAlmostEqual(result.mpg, 29.40, places=2)
    
    def test_calculate_mixed_units(self):
        """混合单位计算"""
        # 用英里距离和升燃油计算
        result = calculate_consumption(distance_miles=186.41, fuel_liters=15)
        # 186.41英里 ≈ 300公里, 15升
        # 300公里/15升 = 20 km/L
        self.assertGreater(result.km_per_liter, 18)
    
    def test_missing_parameters(self):
        """缺少参数测试"""
        with self.assertRaises(ValueError):
            calculate_consumption(distance_miles=300)
        
        with self.assertRaises(ValueError):
            calculate_consumption(fuel_gallons=10)


class TestTripFuelCalculation(unittest.TestCase):
    """行程燃油计算测试"""
    
    def test_basic_trip_calculation(self):
        """基本行程计算"""
        result = calculate_trip_fuel(distance_km=500, consumption_liters_per_100km=8, fuel_price_per_liter=7.5)
        
        # 500公里 * 8L/100km / 100 = 40升
        self.assertEqual(result.fuel_needed_liters, 40.0)
        
        # 40升 * 7.5元/升 = 300元
        self.assertEqual(result.estimated_cost_local, 300.0)
    
    def test_long_trip(self):
        """长途行程计算"""
        result = calculate_trip_fuel(distance_km=1500, consumption_liters_per_100km=10)
        
        # 1500公里 * 10L/100km / 100 = 150升
        self.assertEqual(result.fuel_needed_liters, 150.0)
    
    def test_usd_conversion(self):
        """美元转换"""
        result = calculate_trip_fuel(
            distance_km=100,
            consumption_liters_per_100km=10,
            fuel_price_per_liter=8,
            usd_exchange_rate=7.2  # 假设汇率
        )
        
        # 10升 * 8元 = 80元 / 7.2 = 11.11美元
        self.assertAlmostEqual(result.estimated_cost_usd, 11.11, places=2)
    
    def test_invalid_distance(self):
        """无效距离"""
        with self.assertRaises(ValueError):
            calculate_trip_fuel(distance_km=0, consumption_liters_per_100km=8)
        
        with self.assertRaises(ValueError):
            calculate_trip_fuel(distance_km=-100, consumption_liters_per_100km=8)


class TestCarbonEmission(unittest.TestCase):
    """碳排放计算测试"""
    
    def test_gasoline_emission(self):
        """汽油碳排放"""
        result = calculate_carbon_emission(fuel_liters=40, fuel_type='gasoline')
        
        # 40升 * 2.31 kg/L = 92.4 kg
        self.assertEqual(result.co2_kg, 92.4)
        self.assertAlmostEqual(result.co2_tons, 0.0924, places=4)
    
    def test_diesel_emission(self):
        """柴油碳排放"""
        result = calculate_carbon_emission(fuel_liters=100, fuel_type='diesel')
        
        # 100升 * 2.68 kg/L = 268 kg
        self.assertEqual(result.co2_kg, 268.0)
    
    def test_trees_needed(self):
        """需要树木数"""
        result = calculate_carbon_emission(fuel_liters=100, fuel_type='gasoline')
        
        # 100 * 2.31 = 231 kg CO2
        # 231 / 21.77 ≈ 10.6 -> 11棵树
        self.assertEqual(result.trees_needed, 11)
    
    def test_invalid_fuel_type(self):
        """无效燃料类型"""
        with self.assertRaises(ValueError):
            calculate_carbon_emission(fuel_liters=10, fuel_type='unknown')
    
    def test_invalid_fuel_amount(self):
        """无效燃油量"""
        with self.assertRaises(ValueError):
            calculate_carbon_emission(fuel_liters=0)


class TestRangeEstimation(unittest.TestCase):
    """续航里程估算测试"""
    
    def test_full_tank_range(self):
        """满油续航"""
        km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8)
        
        # 50升 / 8L/100km * 100 = 625公里
        self.assertEqual(km, 625.0)
        # 625 * 0.621371 ≈ 388.36 miles
        self.assertAlmostEqual(miles, 388.36, places=2)
    
    def test_half_tank_range(self):
        """半油续航"""
        km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8, current_fuel_percentage=50)
        
        # 25升 / 8L/100km * 100 = 312.5公里
        self.assertEqual(km, 312.5)
    
    def test_low_fuel_range(self):
        """低油量续航"""
        km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=10, current_fuel_percentage=10)
        
        # 5升 / 10L/100km * 100 = 50公里
        self.assertEqual(km, 50.0)
    
    def test_invalid_percentage(self):
        """无效百分比"""
        with self.assertRaises(ValueError):
            estimate_range(50, 8, 150)
        
        with self.assertRaises(ValueError):
            estimate_range(50, 8, -10)


class TestVehicleComparison(unittest.TestCase):
    """车辆比较测试"""
    
    def test_basic_comparison(self):
        """基本比较"""
        result = compare_vehicles(10, 7, 15000, 7.5)
        
        # 车辆1: 15000km * 10L/100km / 100 = 1500升 * 7.5 = 11250元
        self.assertEqual(result['vehicle1_cost'], 11250.0)
        self.assertEqual(result['vehicle1_fuel_liters'], 1500.0)
        
        # 车辆2: 15000km * 7L/100km / 100 = 1050升 * 7.5 = 7875元
        self.assertEqual(result['vehicle2_cost'], 7875.0)
        self.assertEqual(result['vehicle2_fuel_liters'], 1050.0)
        
        # 节省: 11250 - 7875 = 3375元
        self.assertEqual(result['annual_savings'], 3375.0)
        
        # 车辆2更省油
        self.assertEqual(result['better_vehicle'], 2)
    
    def test_mpg_included(self):
        """包含MPG转换"""
        result = compare_vehicles(10, 7)
        
        # 10 L/100km ≈ 23.52 MPG
        self.assertAlmostEqual(result['vehicle1_mpg'], 23.52, places=2)
        
        # 7 L/100km ≈ 33.60 MPG
        self.assertAlmostEqual(result['vehicle2_mpg'], 33.60, places=2)


class TestConsumptionRating(unittest.TestCase):
    """油耗评级测试"""
    
    def test_car_ratings(self):
        """轿车评级"""
        self.assertIn('Excellent', get_consumption_rating(5, 'car'))
        self.assertIn('Good', get_consumption_rating(7, 'car'))
        self.assertIn('Average', get_consumption_rating(9, 'car'))
        self.assertIn('Poor', get_consumption_rating(11, 'car'))
        self.assertIn('Very Poor', get_consumption_rating(15, 'car'))
    
    def test_suv_ratings(self):
        """SUV评级"""
        self.assertIn('Excellent', get_consumption_rating(7, 'suv'))
        self.assertIn('Good', get_consumption_rating(9, 'suv'))
        self.assertIn('Average', get_consumption_rating(11, 'suv'))
    
    def test_truck_ratings(self):
        """卡车评级"""
        self.assertIn('Excellent', get_consumption_rating(9, 'truck'))
        self.assertIn('Good', get_consumption_rating(11, 'truck'))
        self.assertIn('Average', get_consumption_rating(14, 'truck'))
    
    def test_default_vehicle_type(self):
        """默认车辆类型"""
        # 未知类型使用轿车标准
        result = get_consumption_rating(5, 'unknown')
        self.assertIn('Excellent', result)


class TestQuickConvert(unittest.TestCase):
    """快速转换测试"""
    
    def test_mpg_to_l100km(self):
        """MPG转L/100km"""
        result = quick_mpg_convert(30, 'mpg', 'l100km')
        self.assertAlmostEqual(result, 7.84, places=2)
    
    def test_l100km_to_mpg(self):
        """L/100km转MPG"""
        result = quick_mpg_convert(8, 'l100km', 'mpg')
        self.assertAlmostEqual(result, 29.40, places=2)
    
    def test_same_unit(self):
        """相同单位"""
        result = quick_mpg_convert(30, 'mpg', 'mpg')
        self.assertEqual(result, 30)
    
    def test_l100km_to_kml(self):
        """L/100km转km/L"""
        result = quick_mpg_convert(8, 'l100km', 'kml')
        self.assertEqual(result, 12.5)
    
    def test_invalid_conversion(self):
        """无效转换"""
        with self.assertRaises(ValueError):
            quick_mpg_convert(30, 'mpg', 'unknown')


class TestDataClasses(unittest.TestCase):
    """数据类测试"""
    
    def test_fuel_consumption_result(self):
        """FuelConsumptionResult"""
        result = FuelConsumptionResult(mpg=30.0, liters_per_100km=7.84, km_per_liter=12.75)
        self.assertEqual(result.mpg, 30.0)
        self.assertEqual(result.liters_per_100km, 7.84)
        self.assertEqual(result.km_per_liter, 12.75)
    
    def test_trip_fuel_result(self):
        """TripFuelResult"""
        result = TripFuelResult(
            fuel_needed_liters=40.0,
            fuel_needed_gallons=10.57,
            estimated_cost_local=300.0,
            estimated_cost_usd=42.0
        )
        self.assertEqual(result.fuel_needed_liters, 40.0)
        self.assertEqual(result.fuel_needed_gallons, 10.57)
    
    def test_carbon_emission_result(self):
        """CarbonEmissionResult"""
        result = CarbonEmissionResult(co2_kg=92.4, co2_tons=0.0924, trees_needed=5)
        self.assertEqual(result.co2_kg, 92.4)
        self.assertEqual(result.trees_needed, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)