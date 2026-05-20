"""
AQI Utils 测试文件

测试空气质量指数计算工具的完整功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aqi_utils.mod import (
    AQILevel, PollutantType, AQIResult, ComprehensiveAQI,
    calculate_aqi, calculate_comprehensive_aqi, aqi_to_concentration,
    get_health_recommendations, compare_standards, get_pollutant_info,
    calculate_aqi_range, estimate_pm25_from_visibility, get_aqi_summary,
    get_aqi_level, pm25_to_aqi, pm10_to_aqi, o3_to_aqi,
    co_to_aqi, so2_to_aqi, no2_to_aqi,
    AQI_BREAKPOINTS_CN, AQI_BREAKPOINTS_US, AQI_COLORS
)


def test_pm25_aqi_calculation_cn():
    """测试PM2.5 AQI计算 (中国标准)"""
    print("测试 PM2.5 AQI 计算 (中国标准)...")
    
    # 优 (0-50)
    result = calculate_aqi(10, PollutantType.PM25, "cn")
    assert result.aqi >= 0 and result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    assert result.unit == "μg/m³"
    print(f"  浓度 10 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 良 (51-100)
    result = calculate_aqi(50, PollutantType.PM25, "cn")
    assert result.aqi >= 51 and result.aqi <= 100
    assert result.level == AQILevel.GOOD
    print(f"  浓度 50 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 轻度污染 (101-150)
    result = calculate_aqi(100, PollutantType.PM25, "cn")
    assert result.aqi >= 101 and result.aqi <= 150
    assert result.level == AQILevel.LIGHT_POLLUTION
    print(f"  浓度 100 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 中度污染 (151-200)
    result = calculate_aqi(130, PollutantType.PM25, "cn")
    assert result.aqi >= 151 and result.aqi <= 200
    assert result.level == AQILevel.MODERATE_POLLUTION
    print(f"  浓度 130 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 重度污染 (201-300)
    result = calculate_aqi(200, PollutantType.PM25, "cn")
    assert result.aqi >= 201 and result.aqi <= 300
    assert result.level == AQILevel.HEAVY_POLLUTION
    print(f"  浓度 200 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 严重污染 (>300)
    result = calculate_aqi(400, PollutantType.PM25, "cn")
    assert result.aqi > 300
    assert result.level == AQILevel.SEVERE_POLLUTION
    print(f"  浓度 400 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("PM2.5 AQI 计算测试通过 ✓\n")


def test_pm25_aqi_calculation_us():
    """测试PM2.5 AQI计算 (美国标准)"""
    print("测试 PM2.5 AQI 计算 (美国标准)...")
    
    # 美国 EPA 标准断点
    result = calculate_aqi(5.0, PollutantType.PM25, "us")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  浓度 5.0 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(20.0, PollutantType.PM25, "us")
    assert result.aqi >= 51 and result.aqi <= 100
    assert result.level == AQILevel.GOOD
    print(f"  浓度 20.0 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(45.0, PollutantType.PM25, "us")
    assert result.aqi >= 101 and result.aqi <= 150
    assert result.level == AQILevel.LIGHT_POLLUTION
    print(f"  浓度 45.0 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("PM2.5 AQI 计算测试 (美国标准) 通过 ✓\n")


def test_pm10_aqi_calculation():
    """测试PM10 AQI计算"""
    print("测试 PM10 AQI 计算...")
    
    result = calculate_aqi(30, PollutantType.PM10, "cn")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  浓度 30 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(100, PollutantType.PM10, "cn")
    assert result.level == AQILevel.GOOD
    print(f"  浓度 100 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(300, PollutantType.PM10, "cn")
    assert result.level == AQILevel.MODERATE_POLLUTION
    print(f"  浓度 300 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("PM10 AQI 计算测试通过 ✓\n")


def test_o3_aqi_calculation():
    """测试臭氧 AQI计算"""
    print("测试臭氧 AQI 计算...")
    
    # 1小时平均
    result = calculate_aqi(80, PollutantType.O3_1H, "cn")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  O3(1h) 浓度 80 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(250, PollutantType.O3_1H, "cn")
    assert result.level == AQILevel.LIGHT_POLLUTION
    print(f"  O3(1h) 浓度 250 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    # 8小时平均
    result = calculate_aqi(80, PollutantType.O3_8H, "cn")
    assert result.aqi <= 50
    print(f"  O3(8h) 浓度 80 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(180, PollutantType.O3_8H, "cn")
    assert result.level == AQILevel.LIGHT_POLLUTION
    print(f"  O3(8h) 浓度 180 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("臭氧 AQI 计算测试通过 ✓\n")


def test_co_aqi_calculation():
    """测试CO AQI计算"""
    print("测试 CO AQI 计算...")
    
    result = calculate_aqi(1.0, PollutantType.CO, "cn")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  浓度 1.0 mg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(3.0, PollutantType.CO, "cn")
    assert result.level == AQILevel.GOOD
    print(f"  浓度 3.0 mg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(10.0, PollutantType.CO, "cn")
    assert result.level == AQILevel.LIGHT_POLLUTION
    print(f"  浓度 10.0 mg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("CO AQI 计算测试通过 ✓\n")


def test_so2_aqi_calculation():
    """测试SO2 AQI计算"""
    print("测试 SO2 AQI 计算...")
    
    result = calculate_aqi(25, PollutantType.SO2, "cn")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  浓度 25 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(100, PollutantType.SO2, "cn")
    assert result.level == AQILevel.GOOD
    print(f"  浓度 100 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(500, PollutantType.SO2, "cn")
    assert result.level == AQILevel.MODERATE_POLLUTION
    print(f"  浓度 500 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("SO2 AQI 计算测试通过 ✓\n")


def test_no2_aqi_calculation():
    """测试NO2 AQI计算"""
    print("测试 NO2 AQI 计算...")
    
    result = calculate_aqi(20, PollutantType.NO2, "cn")
    assert result.aqi <= 50
    assert result.level == AQILevel.EXCELLENT
    print(f"  浓度 20 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(60, PollutantType.NO2, "cn")
    assert result.level == AQILevel.GOOD
    print(f"  浓度 60 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    result = calculate_aqi(200, PollutantType.NO2, "cn")
    assert result.level == AQILevel.MODERATE_POLLUTION
    print(f"  浓度 200 μg/m³ -> AQI {result.aqi} ({result.level.value}) ✓")
    
    print("NO2 AQI 计算测试通过 ✓\n")


def test_comprehensive_aqi():
    """测试综合AQI计算"""
    print("测试综合 AQI 计算...")
    
    # 正常情况
    concentrations = {
        "pm25": 75,
        "pm10": 120,
        "o3": 100,
        "co": 1.5,
        "so2": 30,
        "no2": 50
    }
    
    result = calculate_comprehensive_aqi(concentrations, "cn")
    assert result.aqi > 0
    assert result.primary_pollutant is not None
    assert len(result.all_results) == 6
    assert result.health_advice is not None
    print(f"  综合AQI: {result.aqi}, 首要污染物: {result.primary_pollutant.value} ✓")
    
    # 部分污染物
    concentrations = {
        "pm25": 200,
        "o3": 150
    }
    
    result = calculate_comprehensive_aqi(concentrations, "cn")
    assert result.aqi > 100
    assert result.level in [AQILevel.LIGHT_POLLUTION, AQILevel.MODERATE_POLLUTION, AQILevel.HEAVY_POLLUTION]
    print(f"  部分污染物综合AQI: {result.aqi}, 等级: {result.level.value} ✓")
    
    # PM2.5 应该是首要污染物
    assert result.primary_pollutant == PollutantType.PM25
    
    print("综合 AQI 计算测试通过 ✓\n")


def test_aqi_to_concentration():
    """测试AQI转浓度"""
    print("测试 AQI 转浓度...")
    
    # PM2.5
    concentration = aqi_to_concentration(50, PollutantType.PM25, "cn")
    assert 0 <= concentration <= 35  # AQI 50 对应浓度 0-35 μg/m³
    print(f"  AQI 50 -> PM2.5 浓度 {concentration:.1f} μg/m³ ✓")
    
    concentration = aqi_to_concentration(100, PollutantType.PM25, "cn")
    assert 35 <= concentration <= 75  # AQI 100 对应浓度 35-75 μg/m³
    print(f"  AQI 100 -> PM2.5 浓度 {concentration:.1f} μg/m³ ✓")
    
    concentration = aqi_to_concentration(200, PollutantType.PM25, "cn")
    assert 115 <= concentration <= 150  # AQI 200 对应浓度 115-150 μg/m³
    print(f"  AQI 200 -> PM2.5 浓度 {concentration:.1f} μg/m³ ✓")
    
    # 边界值
    concentration = aqi_to_concentration(0, PollutantType.PM25, "cn")
    assert concentration == 0
    print(f"  AQI 0 -> PM2.5 浓度 {concentration:.1f} μg/m³ ✓")
    
    concentration = aqi_to_concentration(500, PollutantType.PM25, "cn")
    assert concentration > 0
    print(f"  AQI 500 -> PM2.5 浓度 {concentration:.1f} μg/m³ ✓")
    
    print("AQI 转浓度测试通过 ✓\n")


def test_health_recommendations():
    """测试健康建议"""
    print("测试健康建议...")
    
    # 各等级建议
    for aqi in [25, 75, 125, 175, 250, 400]:
        recommendations = get_health_recommendations(aqi)
        assert "general" in recommendations
        assert "activity" in recommendations
        assert "sensitive_groups" in recommendations
        assert "outdoor" in recommendations
        assert "mask" in recommendations
        assert "ventilation" in recommendations
        
        level = get_aqi_level(aqi)
        print(f"  AQI {aqi} ({level.value}): ✓")
        print(f"    - 总体建议: {recommendations['general'][:30]}...")
        print(f"    - 口罩建议: {recommendations['mask']}")
    
    print("健康建议测试通过 ✓\n")


def test_compare_standards():
    """测试标准比较"""
    print("测试中国/美国标准比较...")
    
    # PM2.5 浓度 35 μg/m³
    results = compare_standards(35, PollutantType.PM25)
    assert "cn" in results
    assert "us" in results
    
    cn_aqi = results["cn"].aqi
    us_aqi = results["us"].aqi
    print(f"  PM2.5 浓度 35 μg/m³:")
    print(f"    - 中国标准: AQI {cn_aqi}")
    print(f"    - 美国标准: AQI {us_aqi}")
    
    # 美国标准通常更严格
    assert cn_aqi > 0
    assert us_aqi > 0
    
    print("标准比较测试通过 ✓\n")


def test_pollutant_info():
    """测试污染物信息"""
    print("测试污染物信息...")
    
    pollutants = [
        PollutantType.PM25,
        PollutantType.PM10,
        PollutantType.O3_1H,
        PollutantType.O3_8H,
        PollutantType.CO,
        PollutantType.SO2,
        PollutantType.NO2
    ]
    
    for pollutant in pollutants:
        info = get_pollutant_info(pollutant)
        assert "name" in info
        assert "description" in info
        assert "source" in info
        assert "health_effect" in info
        print(f"  {pollutant.value}: {info['name']} ✓")
    
    print("污染物信息测试通过 ✓\n")


def test_aqi_range():
    """测试AQI范围计算"""
    print("测试 AQI 范围计算...")
    
    results = calculate_aqi_range(0, 200, PollutantType.PM25, steps=5, standard="cn")
    assert len(results) == 5
    
    for i, r in enumerate(results):
        print(f"  浓度 {r['concentration']:.1f} -> AQI {r['aqi']} ({r['level']})")
    
    # 验证单调递增
    for i in range(1, len(results)):
        assert results[i]["aqi"] >= results[i-1]["aqi"]
    
    print("AQI 范围计算测试通过 ✓\n")


def test_estimate_pm25_from_visibility():
    """测试能见度估算PM2.5"""
    print("测试能见度估算 PM2.5...")
    
    # 好能见度 -> 低PM2.5
    pm25 = estimate_pm25_from_visibility(30)  # 30公里能见度
    print(f"  能见度 30km -> 估算 PM2.5: {pm25:.1f} μg/m³")
    assert pm25 >= 0
    
    # 差能见度 -> 高PM2.5
    pm25 = estimate_pm25_from_visibility(5)  # 5公里能见度
    print(f"  能见度 5km -> 估算 PM2.5: {pm25:.1f} μg/m³")
    assert pm25 > 0
    
    # 极差能见度
    pm25 = estimate_pm25_from_visibility(1)  # 1公里能见度
    print(f"  能见度 1km -> 估算 PM2.5: {pm25:.1f} μg/m³")
    assert pm25 > 50
    
    print("能见度估算 PM2.5 测试通过 ✓\n")


def test_aqi_summary():
    """测试AQI摘要"""
    print("测试 AQI 摘要...")
    
    for aqi in [30, 80, 120, 180, 250, 400]:
        summary = get_aqi_summary(aqi)
        level = get_aqi_level(aqi)
        print(f"  {summary}")
        assert str(aqi) in summary
        assert level.value in summary
    
    print("AQI 摘要测试通过 ✓\n")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # PM2.5
    aqi = pm25_to_aqi(50)
    assert aqi > 0
    print(f"  pm25_to_aqi(50) = {aqi} ✓")
    
    # PM10
    aqi = pm10_to_aqi(100)
    assert aqi > 0
    print(f"  pm10_to_aqi(100) = {aqi} ✓")
    
    # O3
    aqi = o3_to_aqi(150)
    assert aqi > 0
    print(f"  o3_to_aqi(150) = {aqi} ✓")
    
    # CO
    aqi = co_to_aqi(2.5)
    assert aqi > 0
    print(f"  co_to_aqi(2.5) = {aqi} ✓")
    
    # SO2
    aqi = so2_to_aqi(80)
    assert aqi > 0
    print(f"  so2_to_aqi(80) = {aqi} ✓")
    
    # NO2
    aqi = no2_to_aqi(50)
    assert aqi > 0
    print(f"  no2_to_aqi(50) = {aqi} ✓")
    
    print("便捷函数测试通过 ✓\n")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 零浓度
    result = calculate_aqi(0, PollutantType.PM25, "cn")
    assert result.aqi == 0
    print(f"  零浓度 -> AQI {result.aqi} ✓")
    
    # 极低浓度
    result = calculate_aqi(0.1, PollutantType.PM25, "cn")
    assert result.aqi >= 0
    print(f"  极低浓度 0.1 -> AQI {result.aqi} ✓")
    
    # 极高浓度 (超过500)
    result = calculate_aqi(600, PollutantType.PM25, "cn")
    assert result.aqi <= 500  # 应被限制在500
    assert result.level == AQILevel.SEVERE_POLLUTION
    print(f"  极高浓度 600 -> AQI {result.aqi} (限制在500内) ✓")
    
    # 负浓度处理
    try:
        result = calculate_aqi(-10, PollutantType.PM25, "cn")
        # 如果没有抛出异常，检查结果是否合理
        assert result.aqi >= 0
        print(f"  负浓度 -> AQI {result.aqi} ✓")
    except:
        print("  负浓度抛出异常 ✓")
    
    print("边界情况测试通过 ✓\n")


def test_aqi_levels():
    """测试AQI等级"""
    print("测试 AQI 等级分类...")
    
    test_cases = [
        (0, AQILevel.EXCELLENT),
        (25, AQILevel.EXCELLENT),
        (50, AQILevel.EXCELLENT),
        (51, AQILevel.GOOD),
        (100, AQILevel.GOOD),
        (101, AQILevel.LIGHT_POLLUTION),
        (150, AQILevel.LIGHT_POLLUTION),
        (151, AQILevel.MODERATE_POLLUTION),
        (200, AQILevel.MODERATE_POLLUTION),
        (201, AQILevel.HEAVY_POLLUTION),
        (300, AQILevel.HEAVY_POLLUTION),
        (301, AQILevel.SEVERE_POLLUTION),
        (500, AQILevel.SEVERE_POLLUTION),
    ]
    
    for aqi, expected_level in test_cases:
        level = get_aqi_level(aqi)
        assert level == expected_level, f"AQI {aqi}: 期望 {expected_level}, 实际 {level}"
        print(f"  AQI {aqi:3d} -> {level.value} ✓")
    
    print("AQI 等级分类测试通过 ✓\n")


def test_aqi_colors():
    """测试AQI颜色"""
    print("测试 AQI 颜色...")
    
    for level in AQILevel:
        color = AQI_COLORS[level]
        assert color.startswith("#")
        assert len(color) == 7  # #RRGGBB
        print(f"  {level.value}: {color} ✓")
    
    print("AQI 颜色测试通过 ✓\n")


def test_result_attributes():
    """测试结果对象属性"""
    print("测试结果对象属性...")
    
    result = calculate_aqi(75, PollutantType.PM25, "cn")
    
    # AQIResult 属性
    assert hasattr(result, 'aqi')
    assert hasattr(result, 'level')
    assert hasattr(result, 'pollutant')
    assert hasattr(result, 'concentration')
    assert hasattr(result, 'unit')
    assert hasattr(result, 'color')
    assert hasattr(result, 'health_advice')
    assert hasattr(result, 'activity_suggestion')
    
    print(f"  AQIResult 属性完整 ✓")
    print(f"    - aqi: {result.aqi}")
    print(f"    - level: {result.level.value}")
    print(f"    - pollutant: {result.pollutant.value}")
    print(f"    - concentration: {result.concentration} {result.unit}")
    print(f"    - color: {result.color}")
    
    # ComprehensiveAQI 属性
    comp_result = calculate_comprehensive_aqi({"pm25": 75}, "cn")
    assert hasattr(comp_result, 'aqi')
    assert hasattr(comp_result, 'level')
    assert hasattr(comp_result, 'primary_pollutant')
    assert hasattr(comp_result, 'all_results')
    assert hasattr(comp_result, 'color')
    assert hasattr(comp_result, 'health_advice')
    
    print(f"  ComprehensiveAQI 属性完整 ✓")
    
    print("结果对象属性测试通过 ✓\n")


def test_all_pollutants_cn():
    """测试所有污染物 (中国标准)"""
    print("测试所有污染物 (中国标准)...")
    
    test_data = [
        (PollutantType.PM25, 50),
        (PollutantType.PM10, 100),
        (PollutantType.O3_1H, 150),
        (PollutantType.O3_8H, 100),
        (PollutantType.CO, 2.0),
        (PollutantType.SO2, 80),
        (PollutantType.NO2, 60),
    ]
    
    for pollutant, concentration in test_data:
        result = calculate_aqi(concentration, pollutant, "cn")
        print(f"  {pollutant.value:8s} 浓度 {concentration:6.1f} -> AQI {result.aqi:3d} ({result.level.value}) ✓")
        assert result.aqi > 0
    
    print("所有污染物测试通过 ✓\n")


def test_all_pollutants_us():
    """测试所有污染物 (美国标准)"""
    print("测试所有污染物 (美国标准)...")
    
    test_data = [
        (PollutantType.PM25, 15.0),
        (PollutantType.PM10, 80),
        (PollutantType.O3_1H, 80),
        (PollutantType.O3_8H, 60),
        (PollutantType.CO, 5.0),
        (PollutantType.SO2, 50),
        (PollutantType.NO2, 60),
    ]
    
    for pollutant, concentration in test_data:
        result = calculate_aqi(concentration, pollutant, "us")
        print(f"  {pollutant.value:8s} 浓度 {concentration:6.1f} -> AQI {result.aqi:3d} ({result.level.value}) ✓")
        assert result.aqi > 0
    
    print("所有污染物 (美国标准) 测试通过 ✓\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("AQI Utils 测试套件")
    print("=" * 60)
    print()
    
    test_aqi_levels()
    test_aqi_colors()
    test_pm25_aqi_calculation_cn()
    test_pm25_aqi_calculation_us()
    test_pm10_aqi_calculation()
    test_o3_aqi_calculation()
    test_co_aqi_calculation()
    test_so2_aqi_calculation()
    test_no2_aqi_calculation()
    test_comprehensive_aqi()
    test_aqi_to_concentration()
    test_health_recommendations()
    test_compare_standards()
    test_pollutant_info()
    test_aqi_range()
    test_estimate_pm25_from_visibility()
    test_aqi_summary()
    test_convenience_functions()
    test_edge_cases()
    test_result_attributes()
    test_all_pollutants_cn()
    test_all_pollutants_us()
    
    print("=" * 60)
    print("所有测试通过! ✅")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()