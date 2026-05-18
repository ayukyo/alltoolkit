"""
燃油消耗计算工具使用示例
"""

import sys
sys.path.insert(0, '..')

from mod import (
    mpg_to_liters_per_100km,
    liters_per_100km_to_mpg,
    calculate_consumption,
    calculate_trip_fuel,
    calculate_carbon_emission,
    estimate_range,
    compare_vehicles,
    get_consumption_rating,
    quick_mpg_convert,
    format_consumption,
)


def example_basic_conversion():
    """示例1: 基本单位转换"""
    print("=" * 60)
    print("示例1: 基本单位转换")
    print("=" * 60)
    
    # MPG 转 L/100km
    mpg = 30
    l100km = mpg_to_liters_per_100km(mpg)
    print(f"✅ {mpg} MPG = {l100km} L/100km")
    
    # L/100km 转 MPG
    consumption = 8
    mpg_result = liters_per_100km_to_mpg(consumption)
    print(f"✅ {consumption} L/100km = {mpg_result} MPG")
    
    # 快速转换
    print(f"✅ 快速转换: 25 MPG = {quick_mpg_convert(25, 'mpg', 'l100km')} L/100km")
    print(f"✅ 快速转换: 6 L/100km = {quick_mpg_convert(6, 'l100km', 'kml')} km/L")
    print()


def example_trip_planning():
    """示例2: 行程规划"""
    print("=" * 60)
    print("示例2: 行程规划 - 北京到上海自驾")
    print("=" * 60)
    
    distance = 1200  # 北京到上海约1200公里
    consumption = 8  # 油耗 8L/100km
    price = 7.5  # 汽油价格 7.5元/升
    
    result = calculate_trip_fuel(distance, consumption, price)
    
    print(f"行程距离: {distance} 公里")
    print(f"车辆油耗: {consumption} L/100km")
    print(f"汽油价格: ¥{price}/升")
    print(f"预估燃油: {result.fuel_needed_liters} 升 ({result.fuel_needed_gallons} 加仑)")
    print(f"预估成本: ¥{result.estimated_cost_local}")
    print()


def example_carbon_footprint():
    """示例3: 碳足迹计算"""
    print("=" * 60)
    print("示例3: 碳足迹计算")
    print("=" * 60)
    
    # 年度燃油消耗
    annual_distance = 15000  # 年行驶15000公里
    consumption = 10  # 油耗10L/100km
    annual_fuel = annual_distance * consumption / 100
    
    # 计算碳排放
    emission = calculate_carbon_emission(annual_fuel, 'gasoline')
    
    print(f"年行驶里程: {annual_distance} 公里")
    print(f"车辆油耗: {consumption} L/100km")
    print(f"年燃油消耗: {annual_fuel} 升")
    print(f"CO₂排放量: {emission.co2_kg} kg ({emission.co2_tons} 吨)")
    print(f"抵消碳排放需种植: {emission.trees_needed} 棵树")
    print()
    
    # 不同燃料对比
    print("不同燃料类型碳排放对比 (100升):")
    for fuel_type in ['gasoline', 'diesel', 'ethanol_e85']:
        result = calculate_carbon_emission(100, fuel_type)
        print(f"  {fuel_type}: {result.co2_kg} kg CO₂")
    print()


def example_range_estimation():
    """示例4: 续航里程估算"""
    print("=" * 60)
    print("示例4: 续航里程估算")
    print("=" * 60)
    
    tank = 55  # 油箱55升
    consumption = 7  # 油耗7L/100km
    
    print(f"油箱容量: {tank} 升")
    print(f"车辆油耗: {consumption} L/100km")
    
    # 不同油量下的续航
    for percentage in [100, 75, 50, 25, 10]:
        km, miles = estimate_range(tank, consumption, percentage)
        print(f"  {percentage}% 油量 → 续航: {km} km ({miles} miles)")
    print()


def example_vehicle_comparison():
    """示例5: 车辆对比"""
    print("=" * 60)
    print("示例5: 车辆油耗对比")
    print("=" * 60)
    
    # 两辆车对比
    vehicle1 = 12  # SUV油耗12L/100km
    vehicle2 = 6   # 混动车油耗6L/100km
    annual_km = 20000
    price = 7.5
    
    result = compare_vehicles(vehicle1, vehicle2, annual_km, price)
    
    print(f"车辆1 (SUV): {vehicle1} L/100km ({result['vehicle1_mpg']} MPG)")
    print(f"  年度燃油: {result['vehicle1_fuel_liters']} 升")
    print(f"  年度成本: ¥{result['vehicle1_cost']}")
    
    print(f"车辆2 (混动): {vehicle2} L/100km ({result['vehicle2_mpg']} MPG)")
    print(f"  年度燃油: {result['vehicle2_fuel_liters']} 升")
    print(f"  年度成本: ¥{result['vehicle2_cost']}")
    
    print(f"年节省: ¥{result['annual_savings']}")
    print(f"推荐: 车辆{result['better_vehicle']}")
    print()


def example_consumption_rating():
    """示例6: 油耗评级"""
    print("=" * 60)
    print("示例6: 油耗评级系统")
    print("=" * 60)
    
    test_cases = [
        (5, 'car', '紧凑型轿车'),
        (8, 'car', '中型轿车'),
        (12, 'car', '大型轿车'),
        (8, 'suv', '紧凑型SUV'),
        (12, 'suv', '中型SUV'),
        (10, 'truck', '轻型卡车'),
        (15, 'truck', '重型卡车'),
    ]
    
    for consumption, vtype, desc in test_cases:
        rating = get_consumption_rating(consumption, vtype)
        print(f"{desc} ({consumption} L/100km): {rating}")
    print()


def example_real_trip():
    """示例7: 实际行程记录"""
    print("=" * 60)
    print("示例7: 实际行程油耗计算")
    print("=" * 60)
    
    # 从行程记录计算实际油耗
    print("行程记录:")
    print("  起点: 北京")
    print("  终点: 天津")
    print("  距离: 120公里")
    print("  燃油消耗: 9.6升")
    
    result = calculate_consumption(distance_km=120, fuel_liters=9.6)
    print(f"\n实际油耗指标:")
    print(f"  L/100km: {result.liters_per_100km}")
    print(f"  MPG: {result.mpg}")
    print(f"  km/L: {result.km_per_liter}")
    
    rating = get_consumption_rating(result.liters_per_100km, 'car')
    print(f"  油耗评级: {rating}")
    print()


def example_fuel_efficiency_table():
    """示例8: 油耗效率参考表"""
    print("=" * 60)
    print("示例8: 油耗效率参考表")
    print("=" * 60)
    
    print("\n不同油耗对应的指标:")
    print("-" * 40)
    print(f"{'L/100km':<12}{'MPG':<12}{'km/L':<12}{'评级':<20}")
    print("-" * 40)
    
    for l100km in [4, 5, 6, 7, 8, 9, 10, 12, 15]:
        mpg = liters_per_100km_to_mpg(l100km)
        kml = 100 / l100km
        rating = get_consumption_rating(l100km, 'car')
        print(f"{l100km:<12}{mpg:<12.2f}{kml:<12.2f}{rating:<20}")
    print()


def main():
    """运行所有示例"""
    example_basic_conversion()
    example_trip_planning()
    example_carbon_footprint()
    example_range_estimation()
    example_vehicle_comparison()
    example_consumption_rating()
    example_real_trip()
    example_fuel_efficiency_table()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()