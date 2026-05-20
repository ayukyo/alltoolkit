"""
AQI Utils 使用示例

展示空气质量指数计算工具的完整使用方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aqi_utils.mod import (
    AQILevel, PollutantType,
    calculate_aqi, calculate_comprehensive_aqi, aqi_to_concentration,
    get_health_recommendations, compare_standards, get_pollutant_info,
    calculate_aqi_range, estimate_pm25_from_visibility, get_aqi_summary,
    get_aqi_level, pm25_to_aqi, pm10_to_aqi, o3_to_aqi,
    co_to_aqi, so2_to_aqi, no2_to_aqi,
)


def example_basic_pm25():
    """基础PM2.5 AQI计算示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基础 PM2.5 AQI 计算")
    print("=" * 50)
    
    # 计算PM2.5的AQI
    concentrations = [10, 35, 75, 115, 150, 250, 400]
    
    print("\nPM2.5 浓度与AQI对照表 (中国标准):")
    print("-" * 45)
    print("浓度(μg/m³)  | AQI值 | 空气质量等级")
    print("-" * 45)
    
    for conc in concentrations:
        result = calculate_aqi(conc, PollutantType.PM25, "cn")
        print(f"{conc:12d} | {result.aqi:5d} | {result.level.value}")
    
    print("-" * 45)


def example_comprehensive_aqi():
    """综合AQI计算示例"""
    print("\n" + "=" * 50)
    print("示例 2: 综合 AQI 计算")
    print("=" * 50)
    
    # 模拟一个城市的空气质量数据
    city_data = {
        "pm25": 68,
        "pm10": 95,
        "o3": 120,
        "co": 1.2,
        "so2": 25,
        "no2": 45
    }
    
    print("\n城市空气质量数据:")
    for pollutant, conc in city_data.items():
        print(f"  {pollutant}: {conc}")
    
    result = calculate_comprehensive_aqi(city_data, "cn")
    
    print("\n综合AQI结果:")
    print(f"  AQI值: {result.aqi}")
    print(f"  空气质量等级: {result.level.value}")
    print(f"  首要污染物: {result.primary_pollutant.value}")
    print(f"  颜色代码: {result.color}")
    print(f"  健康建议: {result.health_advice}")
    
    print("\n各污染物单独AQI:")
    for name, aqi_result in result.all_results.items():
        print(f"  {name}: AQI {aqi_result.aqi} ({aqi_result.level.value})")


def example_health_recommendations():
    """健康建议示例"""
    print("\n" + "=" * 50)
    print("示例 3: 健康建议获取")
    print("=" * 50)
    
    aqi_values = [30, 100, 150, 200, 300]
    
    for aqi in aqi_values:
        recommendations = get_health_recommendations(aqi)
        level = get_aqi_level(aqi)
        
        print(f"\nAQI {aqi} ({level.value}):")
        print(f"  总体建议: {recommendations['general']}")
        print(f"  活动建议: {recommendations['activity']}")
        print(f"  敏感人群: {recommendations['sensitive_groups']}")
        print(f"  口罩建议: {recommendations['mask']}")
        print(f"  通风建议: {recommendations['ventilation']}")


def example_compare_standards():
    """中国/美国标准对比示例"""
    print("\n" + "=" * 50)
    print("示例 4: 中国与美国标准对比")
    print("=" * 50)
    
    concentrations = [10, 35, 50, 100, 150, 250]
    
    print("\nPM2.5 中国 vs 美国标准对比:")
    print("-" * 60)
    print("浓度(μg/m³) | 中国AQI | 中国等级 | 美国AQI | 美国等级")
    print("-" * 60)
    
    for conc in concentrations:
        results = compare_standards(conc, PollutantType.PM25)
        cn = results["cn"]
        us = results["us"]
        print(f"{conc:12d} | {cn.aqi:7d} | {cn.level.value:8s} | {us.aqi:7d} | {us.level.value}")
    
    print("-" * 60)


def example_pollutant_info():
    """污染物信息示例"""
    print("\n" + "=" * 50)
    print("示例 5: 污染物详细信息")
    print("=" * 50)
    
    pollutants = [PollutantType.PM25, PollutantType.O3_1H, PollutantType.CO]
    
    for pollutant in pollutants:
        info = get_pollutant_info(pollutant)
        print(f"\n{info['name']}:")
        print(f"  描述: {info['description']}")
        print(f"  来源: {info['source']}")
        print(f"  健康影响: {info['health_effect']}")


def example_aqi_to_concentration():
    """AQI转浓度示例"""
    print("\n" + "=" * 50)
    print("示例 6: AQI 转浓度")
    print("=" * 50)
    
    aqi_values = [50, 100, 150, 200, 300]
    
    print("\nAQI转PM2.5浓度:")
    print("-" * 40)
    print("AQI值 | PM2.5浓度(μg/m³)")
    print("-" * 40)
    
    for aqi in aqi_values:
        concentration = aqi_to_concentration(aqi, PollutantType.PM25, "cn")
        print(f"{aqi:5d} | {concentration:.1f}")
    
    print("-" * 40)


def example_aqi_range():
    """AQI范围计算示例"""
    print("\n" + "=" * 50)
    print("示例 7: AQI 范围计算")
    print("=" * 50)
    
    print("\nPM2.5 浓度 0-150 μg/m³ 的AQI变化:")
    results = calculate_aqi_range(0, 150, PollutantType.PM25, steps=6, standard="cn")
    
    for r in results:
        print(f"  浓度 {r['concentration']:6.1f} μg/m³ -> AQI {r['aqi']:3d} ({r['level']})")


def example_visibility_estimation():
    """能见度估算示例"""
    print("\n" + "=" * 50)
    print("示例 8: 能见度估算 PM2.5")
    print("=" * 50)
    
    visibility_km = [30, 20, 10, 5, 2, 1]
    
    print("\n能见度与PM2.5估算:")
    print("-" * 45)
    print("能见度(km) | 估算PM2.5(μg/m³) | AQI估算")
    print("-" * 45)
    
    for vis in visibility_km:
        pm25 = estimate_pm25_from_visibility(vis)
        aqi = pm25_to_aqi(pm25)
        level = get_aqi_level(aqi)
        print(f"{vis:10d} | {pm25:15.1f} | {aqi:3d} ({level.value})")
    
    print("-" * 45)
    print("注: 此为粗略估算，高湿度条件下不准确")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("示例 9: 便捷函数")
    print("=" * 50)
    
    print("\n快速AQI计算:")
    
    # PM2.5
    print(f"  PM2.5 浓度 50 μg/m³ -> AQI {pm25_to_aqi(50)}")
    
    # PM10
    print(f"  PM10 浓度 100 μg/m³ -> AQI {pm10_to_aqi(100)}")
    
    # 臭氧
    print(f"  O3 浓度 150 μg/m³ -> AQI {o3_to_aqi(150)}")
    
    # CO
    print(f"  CO 浓度 2.5 mg/m³ -> AQI {co_to_aqi(2.5)}")
    
    # SO2
    print(f"  SO2 浓度 80 μg/m³ -> AQI {so2_to_aqi(80)}")
    
    # NO2
    print(f"  NO2 浓度 60 μg/m³ -> AQI {no2_to_aqi(60)}")


def example_real_world_scenario():
    """真实场景示例"""
    print("\n" + "=" * 50)
    print("示例 10: 真实场景 - 查看今日空气质量")
    print("=" * 50)
    
    # 模拟今日空气质量数据
    today_data = {
        "pm25": 45,
        "pm10": 80,
        "o3": 95,
        "co": 0.8,
        "so2": 15,
        "no2": 35
    }
    
    print("\n今日空气质量数据:")
    print("-" * 30)
    for pollutant, conc in today_data.items():
        unit = "μg/m³" if pollutant != "co" else "mg/m³"
        print(f"  {pollutant.upper()}: {conc} {unit}")
    
    result = calculate_comprehensive_aqi(today_data, "cn")
    
    print("\n今日空气质量报告:")
    print("=" * 40)
    print(f"  AQI指数: {result.aqi}")
    print(f"  空气质量: {result.level.value}")
    print(f"  首要污染物: {result.primary_pollutant.value}")
    print(f"  等级颜色: {result.color}")
    print("\n健康建议:")
    print(f"  {result.health_advice}")
    print("\n活动建议:")
    print(f"  {get_health_recommendations(result.aqi)['activity']}")
    print("\n口罩建议:")
    print(f"  {get_health_recommendations(result.aqi)['mask']}")
    
    print("=" * 40)


def run_all_examples():
    """运行所有示例"""
    example_basic_pm25()
    example_comprehensive_aqi()
    example_health_recommendations()
    example_compare_standards()
    example_pollutant_info()
    example_aqi_to_concentration()
    example_aqi_range()
    example_visibility_estimation()
    example_convenience_functions()
    example_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()