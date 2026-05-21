"""
Ventilation Utils 测试文件

测试室内通风计算工具的各项功能
"""

import unittest
import math
from mod import (
    RoomInfo,
    VentilationResult,
    VentilationType,
    AirQualityLevel,
    CO2Prediction,
    calculate_ach,
    calculate_airflow_for_ach,
    calculate_co2_steady_state,
    calculate_required_ventilation,
    predict_co2_decay,
    calculate_ventilation_time,
    get_air_quality_level,
    analyze_room_ventilation,
    calculate_pollutant_decay,
    calculate_natural_ventilation,
    calculate_fresh_air_duct_size,
    estimate_occupancy_from_co2,
    calculate_hvac_requirements,
    quick_ventilation_check,
    CO2_OUTDOOR,
    CO2_EXCELLENT_LIMIT,
    CO2_GOOD_LIMIT,
    CO2_MODERATE_LIMIT,
    CO2_POOR_LIMIT,
    STANDARD_ACH,
    FRESH_AIR_PER_PERSON,
)


class TestRoomInfo(unittest.TestCase):
    """测试房间信息类"""
    
    def test_volume_calculation(self):
        """测试体积计算"""
        room = RoomInfo(length=10, width=5, height=3)
        self.assertEqual(room.volume, 150)
    
    def test_floor_area_calculation(self):
        """测试面积计算"""
        room = RoomInfo(length=10, width=5, height=3)
        self.assertEqual(room.floor_area, 50)
    
    def test_room_with_occupants(self):
        """测试带人数的房间"""
        room = RoomInfo(length=8, width=6, height=2.8, occupants=10)
        self.assertAlmostEqual(room.volume, 134.4, places=1)
        self.assertEqual(room.occupants, 10)


class TestACHCalculations(unittest.TestCase):
    """测试换气次数计算"""
    
    def test_calculate_ach(self):
        """测试换气次数计算"""
        # 100m³房间，200m³/h风量 = 2 ACH
        ach = calculate_ach(volume=100, airflow=200)
        self.assertEqual(ach, 2.0)
    
    def test_calculate_ach_fractional(self):
        """测试小数换气次数"""
        ach = calculate_ach(volume=150, airflow=300)
        self.assertEqual(ach, 2.0)
    
    def test_calculate_ach_zero_volume(self):
        """测试零体积异常"""
        with self.assertRaises(ValueError):
            calculate_ach(volume=0, airflow=100)
    
    def test_calculate_ach_negative_volume(self):
        """测试负体积异常"""
        with self.assertRaises(ValueError):
            calculate_ach(volume=-10, airflow=100)
    
    def test_calculate_airflow_for_ach(self):
        """测试根据ACH计算风量"""
        airflow = calculate_airflow_for_ach(volume=100, ach=2)
        self.assertEqual(airflow, 200)


class TestCO2Calculations(unittest.TestCase):
    """测试CO2相关计算"""
    
    def test_co2_steady_state_empty_room(self):
        """测试空房间的稳态CO2"""
        room = RoomInfo(length=10, width=5, height=3, occupants=0)
        co2 = calculate_co2_steady_state(room, airflow=100)
        # 空房间应该接近室外浓度
        self.assertAlmostEqual(co2, CO2_OUTDOOR, delta=1)
    
    def test_co2_steady_state_with_occupants(self):
        """测试有人的稳态CO2"""
        room = RoomInfo(length=10, width=5, height=3, occupants=10)
        co2 = calculate_co2_steady_state(room, airflow=500)
        # 应该高于室外浓度
        self.assertGreater(co2, CO2_OUTDOOR)
    
    def test_co2_steady_state_high_ventilation(self):
        """测试高通风量下的CO2"""
        room = RoomInfo(length=10, width=5, height=3, occupants=5)
        co2_low = calculate_co2_steady_state(room, airflow=100)
        co2_high = calculate_co2_steady_state(room, airflow=1000)
        # 更高的通风量应该导致更低的CO2
        self.assertLess(co2_high, co2_low)
    
    def test_co2_steady_state_zero_airflow(self):
        """测试零通风量"""
        room = RoomInfo(length=10, width=5, height=3, occupants=10)
        co2 = calculate_co2_steady_state(room, airflow=0)
        self.assertEqual(co2, float('inf'))
    
    def test_calculate_required_ventilation(self):
        """测试所需通风量计算"""
        room = RoomInfo(length=10, width=5, height=3, occupants=10)
        airflow = calculate_required_ventilation(room, target_co2=800)
        self.assertGreater(airflow, 0)
    
    def test_calculate_required_ventilation_empty_room(self):
        """测试空房间的通风需求"""
        room = RoomInfo(length=10, width=5, height=3, occupants=0)
        airflow = calculate_required_ventilation(room, target_co2=800)
        # 空房间应该需要很少或不需要通风
        self.assertGreaterEqual(airflow, 0)


class TestCO2Decay(unittest.TestCase):
    """测试CO2衰减预测"""
    
    def test_predict_co2_decay(self):
        """测试CO2衰减"""
        prediction = predict_co2_decay(
            volume=100,
            initial_co2=1500,
            airflow=200,
            time_minutes=60
        )
        # 浓度应该下降
        self.assertLess(prediction.final_ppm, prediction.initial_ppm)
        # 最终浓度应该高于室外
        self.assertGreater(prediction.final_ppm, CO2_OUTDOOR)
        # ACH应该正确计算
        self.assertEqual(prediction.ach_used, 2.0)
    
    def test_predict_co2_decay_no_ventilation(self):
        """测试无通风时的衰减"""
        prediction = predict_co2_decay(
            volume=100,
            initial_co2=1500,
            airflow=0,
            time_minutes=60
        )
        # 无通风时浓度应该几乎不变
        self.assertAlmostEqual(prediction.final_ppm, prediction.initial_ppm, delta=1)
    
    def test_predict_co2_decay_with_generation(self):
        """测试有产生源时的衰减"""
        room = RoomInfo(length=10, width=5, height=3, occupants=10)
        co2_gen = room.occupants * 0.02 * 3600
        
        prediction_no_gen = predict_co2_decay(
            volume=room.volume,
            initial_co2=1000,
            airflow=200,
            time_minutes=60,
            co2_generation=0
        )
        
        prediction_with_gen = predict_co2_decay(
            volume=room.volume,
            initial_co2=1000,
            airflow=200,
            time_minutes=60,
            co2_generation=co2_gen
        )
        
        # 有产生源时最终浓度应该更高
        self.assertGreater(prediction_with_gen.final_ppm, prediction_no_gen.final_ppm)


class TestVentilationTime(unittest.TestCase):
    """测试通风时间计算"""
    
    def test_calculate_ventilation_time(self):
        """测试通风时间计算"""
        time_minutes = calculate_ventilation_time(
            volume=100,
            initial_co2=1500,
            target_co2=600,
            airflow=200
        )
        # 应该有合理的通风时间
        self.assertGreater(time_minutes, 0)
        self.assertLess(time_minutes, 120)  # 不应该太长
    
    def test_calculate_ventilation_time_target_higher(self):
        """测试目标浓度高于初始时"""
        time_minutes = calculate_ventilation_time(
            volume=100,
            initial_co2=600,
            target_co2=1500,
            airflow=200
        )
        # 应该不需要通风
        self.assertEqual(time_minutes, 0)
    
    def test_calculate_ventilation_time_zero_airflow(self):
        """测试零通风量"""
        time_minutes = calculate_ventilation_time(
            volume=100,
            initial_co2=1500,
            target_co2=600,
            airflow=0
        )
        # 无通风应该是无穷大
        self.assertEqual(time_minutes, float('inf'))


class TestAirQualityLevel(unittest.TestCase):
    """测试空气质量等级"""
    
    def test_excellent_level(self):
        """测试优秀等级"""
        level = get_air_quality_level(500)
        self.assertEqual(level, AirQualityLevel.EXCELLENT)
    
    def test_good_level(self):
        """测试良好等级"""
        level = get_air_quality_level(700)
        self.assertEqual(level, AirQualityLevel.GOOD)
    
    def test_moderate_level(self):
        """测试中等等级"""
        level = get_air_quality_level(900)
        self.assertEqual(level, AirQualityLevel.MODERATE)
    
    def test_poor_level(self):
        """测试较差等级"""
        level = get_air_quality_level(1200)
        self.assertEqual(level, AirQualityLevel.POOR)
    
    def test_very_poor_level(self):
        """测试很差等级"""
        level = get_air_quality_level(2000)
        self.assertEqual(level, AirQualityLevel.VERY_POOR)


class TestRoomVentilationAnalysis(unittest.TestCase):
    """测试房间通风分析"""
    
    def test_analyze_office_room(self):
        """测试办公室通风分析"""
        room = RoomInfo(length=10, width=8, height=3, occupants=20)
        result = analyze_room_ventilation(room, room_type="office")
        
        self.assertIsInstance(result, VentilationResult)
        self.assertGreater(result.required_ach, 0)
        self.assertGreater(result.required_airflow, 0)
        self.assertGreater(result.recommended_airflow, result.required_airflow)
        self.assertIn(result.ventilation_type, [VentilationType.NATURAL, VentilationType.MECHANICAL, VentilationType.HYBRID])
        self.assertIn(result.quality_level, list(AirQualityLevel))
    
    def test_analyze_empty_room(self):
        """测试空房间分析"""
        room = RoomInfo(length=5, width=5, height=3, occupants=0)
        result = analyze_room_ventilation(room)
        
        # 空房间应该是自然通风
        self.assertEqual(result.ventilation_type, VentilationType.NATURAL)
    
    def test_analyze_different_standards(self):
        """测试不同标准"""
        room = RoomInfo(length=10, width=8, height=3, occupants=10)
        
        result_minimal = analyze_room_ventilation(room, standard="minimal")
        result_premium = analyze_room_ventilation(room, standard="premium")
        
        # 高端标准应该需要更多风量
        self.assertGreater(result_premium.required_airflow, result_minimal.required_airflow)
    
    def test_analyze_different_room_types(self):
        """测试不同房间类型"""
        room = RoomInfo(length=10, width=8, height=3, occupants=10)
        
        result_bedroom = analyze_room_ventilation(room, room_type="bedroom")
        result_hospital = analyze_room_ventilation(room, room_type="hospital")
        
        # 医院需要更高的换气次数
        self.assertGreater(result_hospital.required_ach, result_bedroom.required_ach)


class TestPollutantDecay(unittest.TestCase):
    """测试污染物衰减计算"""
    
    def test_pollutant_decay(self):
        """测试污染物衰减"""
        result = calculate_pollutant_decay(
            volume=100,
            initial_concentration=100,
            airflow=200,
            time_hours=1
        )
        
        # 浓度应该下降
        self.assertLess(result["final_concentration"], result["initial_concentration"])
        self.assertGreater(result["removal_percentage"], 0)
        self.assertGreater(result["half_life_hours"], 0)
    
    def test_pollutant_decay_with_natural_decay(self):
        """测试带自然衰减的污染物"""
        result_no_decay = calculate_pollutant_decay(
            volume=100,
            initial_concentration=100,
            airflow=200,
            decay_rate=0,
            time_hours=1
        )
        
        result_with_decay = calculate_pollutant_decay(
            volume=100,
            initial_concentration=100,
            airflow=200,
            decay_rate=0.5,
            time_hours=1
        )
        
        # 有自然衰减时应该衰减更快
        self.assertLess(result_with_decay["final_concentration"], result_no_decay["final_concentration"])


class TestNaturalVentilation(unittest.TestCase):
    """测试自然通风计算"""
    
    def test_wind_driven_ventilation(self):
        """测试风压通风"""
        result = calculate_natural_ventilation(
            opening_area=2.0,
            wind_speed=3.0,
            temperature_diff=0
        )
        
        self.assertGreater(result["wind_airflow"], 0)
        self.assertEqual(result["primary_driver"], "wind")
    
    def test_stack_driven_ventilation(self):
        """测试热压通风"""
        result = calculate_natural_ventilation(
            opening_area=2.0,
            wind_speed=0.5,  # 低风速
            temperature_diff=10,
            height=3.0
        )
        
        self.assertGreater(result["stack_airflow"], 0)
    
    def test_combined_ventilation(self):
        """测试混合通风"""
        result = calculate_natural_ventilation(
            opening_area=2.0,
            wind_speed=2.0,
            temperature_diff=5,
            height=3.0
        )
        
        self.assertGreater(result["total_airflow"], 0)


class TestDuctSize(unittest.TestCase):
    """测试管道尺寸计算"""
    
    def test_duct_size_calculation(self):
        """测试管道尺寸计算"""
        result = calculate_fresh_air_duct_size(airflow=500)
        
        self.assertGreater(result["area_m2"], 0)
        self.assertGreater(result["diameter_mm"], 0)
        self.assertGreater(result["square_side_mm"], 0)
        self.assertIn(result["recommended_diameter_mm"], [100, 125, 150, 160, 200, 250, 315, 355, 400])
    
    def test_duct_size_high_velocity(self):
        """测试高风速管道"""
        result_low = calculate_fresh_air_duct_size(airflow=500, air_velocity=4)
        result_high = calculate_fresh_air_duct_size(airflow=500, air_velocity=6)
        
        # 高风速需要更小的管道
        self.assertLess(result_high["diameter_mm"], result_low["diameter_mm"])


class TestOccupancyEstimation(unittest.TestCase):
    """测试人数估算"""
    
    def test_estimate_occupancy(self):
        """测试人数估算"""
        room = RoomInfo(length=10, width=8, height=3)
        # 模拟已知稳态浓度反推人数
        occupancy = estimate_occupancy_from_co2(
            room=room,
            current_co2=1000,
            airflow=500
        )
        
        self.assertGreaterEqual(occupancy, 0)
        self.assertIsInstance(occupancy, int)
    
    def test_estimate_zero_airflow(self):
        """测试零通风量时的人数估算"""
        room = RoomInfo(length=10, width=8, height=3)
        occupancy = estimate_occupancy_from_co2(
            room=room,
            current_co2=1000,
            airflow=0
        )
        self.assertEqual(occupancy, 0)
    
    def test_estimate_outdoor_co2(self):
        """测试CO2接近室外浓度时"""
        room = RoomInfo(length=10, width=8, height=3)
        occupancy = estimate_occupancy_from_co2(
            room=room,
            current_co2=CO2_OUTDOOR + 10,
            airflow=500
        )
        # 接近室外浓度应该估算出很少人
        self.assertLess(occupancy, 5)


class TestHVACCalculations(unittest.TestCase):
    """测试HVAC计算"""
    
    def test_cooling_load(self):
        """测试制冷负荷"""
        room = RoomInfo(length=10, width=8, height=3)
        result = calculate_hvac_requirements(
            room=room,
            outdoor_temp=35,
            indoor_temp_target=24,
            ventilation_rate=2
        )
        
        self.assertEqual(result["mode"], "cooling")
        self.assertGreater(result["ventilation_heat_load_kw"], 0)
        self.assertGreater(result["btu_per_hour"], 0)
    
    def test_heating_load(self):
        """测试制热负荷"""
        room = RoomInfo(length=10, width=8, height=3)
        result = calculate_hvac_requirements(
            room=room,
            outdoor_temp=-5,
            indoor_temp_target=20,
            ventilation_rate=2
        )
        
        self.assertEqual(result["mode"], "heating")
        self.assertGreater(result["ventilation_heat_load_kw"], 0)


class TestQuickCheck(unittest.TestCase):
    """测试快速检查功能"""
    
    def test_quick_ventilation_check(self):
        """测试快速通风检查"""
        result = quick_ventilation_check(
            room_length=10,
            room_width=8,
            room_height=3,
            occupants=20,
            room_type="office"
        )
        
        self.assertIn("room_volume_m3", result)
        self.assertIn("floor_area_m2", result)
        self.assertIn("occupants", result)
        self.assertIn("required_ach", result)
        self.assertIn("required_airflow_m3h", result)
        self.assertIn("recommended_airflow_m3h", result)
        self.assertIn("co2_level_ppm", result)
        self.assertIn("air_quality", result)
        self.assertIn("ventilation_type", result)
        self.assertIn("notes", result)
        
        # 验证数值合理性
        self.assertEqual(result["room_volume_m3"], 240)
        self.assertEqual(result["floor_area_m2"], 80)
        self.assertEqual(result["occupants"], 20)
        self.assertGreater(result["required_ach"], 0)
        self.assertGreater(result["required_airflow_m3h"], 0)


class TestConstants(unittest.TestCase):
    """测试常量值"""
    
    def test_co2_constants(self):
        """测试CO2常量"""
        self.assertEqual(CO2_OUTDOOR, 420)
        self.assertEqual(CO2_EXCELLENT_LIMIT, 600)
        self.assertEqual(CO2_GOOD_LIMIT, 800)
        self.assertEqual(CO2_MODERATE_LIMIT, 1000)
        self.assertEqual(CO2_POOR_LIMIT, 1500)
    
    def test_standard_ach_values(self):
        """测试标准ACH值"""
        self.assertIn("bedroom", STANDARD_ACH)
        self.assertIn("office", STANDARD_ACH)
        self.assertIn("hospital", STANDARD_ACH)
        # 医院应该比卧室要求更高
        self.assertGreater(STANDARD_ACH["hospital"], STANDARD_ACH["bedroom"])
    
    def test_fresh_air_standards(self):
        """测试新风标准"""
        self.assertIn("minimal", FRESH_AIR_PER_PERSON)
        self.assertIn("premium", FRESH_AIR_PER_PERSON)
        # 高端标准应该高于最低标准
        self.assertGreater(FRESH_AIR_PER_PERSON["premium"], FRESH_AIR_PER_PERSON["minimal"])


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)