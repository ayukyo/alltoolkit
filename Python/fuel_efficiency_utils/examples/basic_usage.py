"""
Fuel Efficiency Utils - 使用示例
=================================

展示燃油效率计算工具的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    FuelEfficiencyCalculator, FuelType,
    mpg_to_lp100k, lp100k_to_mpg,
    calculate_fuel_cost, calculate_co2
)


def example_unit_conversion():
    """单位转换示例"""
    print("\n" + "=" * 60)
    print("【示例 1: 单位转换】")
    print("=" * 60)
    
    # MPG 转 L/100km
    mpg_values = [25, 30, 35, 40, 50]
    print("\nMPG → L/100km 转换:")
    for mpg in mpg_values:
        lp100k = mpg_to_lp100k(mpg)
        mpg_back = lp100k_to_mpg(lp100k)
        print(f"  {mpg} MPG = {lp100k:.2f} L/100km (往返验证: {mpg_back:.1f} MPG)")
    
    # km/L 转 L/100km
    print("\nkm/L ↔ L/100km 转换:")
    kmpl_values = [10, 12, 14, 16, 20]
    for kmpl in kmpl_values:
        lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(kmpl)
        print(f"  {kmpl} km/L = {lp100k:.2f} L/100km")


def example_fuel_cost():
    """燃油成本计算示例"""
    print("\n" + "=" * 60)
    print("【示例 2: 燃油成本计算】")
    print("=" * 60)
    
    # 基本成本计算
    print("\n行驶500公里，油耗8L/100km，油价8.5元/升:")
    cost = calculate_fuel_cost(500, 8, 8.5)
    print(f"  总成本: ¥{cost}")
    
    # 不同油耗对比
    print("\n不同油耗的成本对比 (500公里，油价8.5元/升):")
    efficiencies = [6, 7, 8, 9, 10, 12]
    for eff in efficiencies:
        cost = calculate_fuel_cost(500, eff, 8.5)
        print(f"  {eff} L/100km: ¥{cost}")
    
    # MPG 单位计算
    print("\n美国单位计算 (300英里，30 MPG，油价$3.5/加仑):")
    cost = FuelEfficiencyCalculator.calculate_fuel_cost(
        300, 30, 3.5, 'mpg', 'mile'
    )
    print(f"  总成本: ${cost}")


def example_range_calculation():
    """续航里程计算示例"""
    print("\n" + "=" * 60)
    print("【示例 3: 续航里程计算】")
    print("=" * 60)
    
    # 不同油箱容量和油耗
    print("\n不同油箱容量的续航里程:")
    tank_sizes = [40, 50, 60, 70]
    efficiency = 8
    
    for tank in tank_sizes:
        range_km = FuelEfficiencyCalculator.calculate_range(tank, efficiency)
        print(f"  {tank}升油箱，{efficiency}L/100km: {range_km}公里")
    
    # 不同油耗的续航 (50升油箱)
    print("\n50升油箱，不同油耗的续航:")
    efficiencies = [5, 6, 8, 10, 12]
    for eff in efficiencies:
        range_km = FuelEfficiencyCalculator.calculate_range(50, eff)
        print(f"  {eff} L/100km: {range_km}公里")


def example_co2_emissions():
    """碳排放计算示例"""
    print("\n" + "=" * 60)
    print("【示例 4: 碳排放计算】")
    print("=" * 60)
    
    # 汽油车排放
    print("\n汽油车碳排放 (100公里):")
    efficiencies = [6, 8, 10, 12]
    for eff in efficiencies:
        co2 = FuelEfficiencyCalculator.calculate_co2_emissions(
            100, eff, FuelType.GASOLINE
        )
        print(f"  {eff} L/100km: {co2:.2f} kg CO2")
    
    # 柴油车排放对比
    print("\n柴油车碳排放 (100公里，6L/100km):")
    co2_diesel = FuelEfficiencyCalculator.calculate_co2_emissions(
        100, 6, FuelType.DIESEL
    )
    print(f"  6 L/100km: {co2_diesel:.2f} kg CO2")
    
    # 电动车间接排放
    print("\n电动车间接排放 (100公里，不同电网):")
    energy_eff = 15  # kWh/100km
    regions = ['china', 'us', 'eu', 'clean', 'dirty']
    for region in regions:
        co2 = FuelEfficiencyCalculator.calculate_electric_emissions(
            100, energy_eff, region
        )
        print(f"  {region}: {co2:.2f} kg CO2")


def example_annual_cost():
    """年度成本计算示例"""
    print("\n" + "=" * 60)
    print("【示例 5: 年度燃油成本】")
    print("=" * 60)
    
    annual_distance = 15000
    fuel_price = 8.5
    
    print(f"\n年行驶{annual_distance}公里，油价{fuel_price}元/升:")
    efficiencies = [5, 6, 7, 8, 10, 12]
    
    for eff in efficiencies:
        result = FuelEfficiencyCalculator.calculate_annual_fuel_cost(
            annual_distance, eff, fuel_price
        )
        print(f"\n  {eff} L/100km:")
        print(f"    年成本: ¥{result['annual_cost']}")
        print(f"    月成本: ¥{result['monthly_cost']}")
        print(f"    年耗油: {result['fuel_consumed_liters']}升")


def example_vehicle_comparison():
    """车辆对比示例"""
    print("\n" + "=" * 60)
    print("【示例 6: 车辆对比】")
    print("=" * 60)
    
    # 紧凑型车 vs SUV
    print("\n紧凑型车 (6L/100km) vs SUV (10L/100km):")
    print("  年行驶15000公里，油价8.5元/升")
    
    result = FuelEfficiencyCalculator.compare_vehicles(
        15000, 10, 6, 8.5
    )
    
    print(f"  SUV成本: ¥{result['vehicle1_cost']}")
    print(f"  紧凑型车成本: ¥{result['vehicle2_cost']}")
    print(f"  年节省: ¥{result['savings']}")
    print(f"  效率提升: {result['percentage_improvement']}%")


def example_break_even():
    """回本分析示例"""
    print("\n" + "=" * 60)
    print("【示例 7: 回本分析】")
    print("=" * 60)
    
    # 购买省油车的回本分析
    print("\n购买省油车的回本分析:")
    print("  省油车: 25万元，5L/100km")
    print("  普通车: 18万元，8L/100km")
    print("  油价: 8.5元/升")
    
    result = FuelEfficiencyCalculator.calculate_break_even(
        250000, 5, 180000, 8, 8.5
    )
    
    print(f"  车价差: ¥{result['price_difference']}")
    print(f"  每公里节省: ¥{result['savings_per_km']}")
    print(f"  回本里程: {result['break_even_km']:,}公里")
    print(f"  回本时间: {result['break_even_years']}年")
    print(f"  {result['message']}")


def example_efficiency_rating():
    """效率评级示例"""
    print("\n" + "=" * 60)
    print("【示例 8: 效率评级】")
    print("=" * 60)
    
    print("\n轿车效率评级:")
    efficiencies = [4, 5, 6, 7, 8, 9, 10, 12, 15]
    for eff in efficiencies:
        rating = FuelEfficiencyCalculator.efficiency_rating(eff, 'car')
        print(f"  {eff} L/100km: {rating[0]} - {rating[1]} ({rating[2]})")
    
    print("\nSUV效率评级:")
    efficiencies = [6, 8, 10, 12, 14, 16, 18]
    for eff in efficiencies:
        rating = FuelEfficiencyCalculator.efficiency_rating(eff, 'suv')
        print(f"  {eff} L/100km: {rating[0]} - {rating[1]}")


def example_trip_calculation():
    """旅行计算示例"""
    print("\n" + "=" * 60)
    print("【示例 9: 旅行成本计算】")
    print("=" * 60)
    
    # 北京到上海
    print("\n北京到上海旅行 (约1200公里):")
    print("  油耗: 8L/100km，油价: 8.5元/升，乘客: 4人")
    
    result = FuelEfficiencyCalculator.calculate_trip_fuel(
        1200, 8, 8.5, 4
    )
    
    print(f"  行程距离: {result['distance_km']}公里 ({result['distance_miles']:.1f}英里)")
    print(f"  需燃油: {result['fuel_needed_liters']}升 ({result['fuel_needed_gallons']:.2f}加仑)")
    print(f"  总成本: ¥{result['total_cost']}")
    print(f"  每公里成本: ¥{result['cost_per_km']}")
    print(f"  人均成本: ¥{result['cost_per_passenger']}")


def example_full_report():
    """完整报告示例"""
    print("\n" + "=" * 60)
    print("【示例 10: 完整效率报告】")
    print("=" * 60)
    
    # 汽油车报告
    print("\n汽油车完整效率报告:")
    print("  油耗: 8L/100km，年行驶: 15000公里，油价: 8.5元/升")
    
    report = FuelEfficiencyCalculator.full_efficiency_report(
        8, 15000, 8.5, FuelType.GASOLINE, 'car'
    )
    
    print(f"\n效率转换:")
    print(f"  L/100km: {report['efficiency']['lp100k']}")
    print(f"  MPG (美制): {report['efficiency']['mpg_us']:.1f}")
    print(f"  MPG (英制): {report['efficiency']['mpg_uk']:.1f}")
    print(f"  km/L: {report['efficiency']['km_per_liter']:.2f}")
    
    print(f"\n年度成本:")
    print(f"  年成本: ¥{report['annual_costs']['annual_cost']}")
    print(f"  月成本: ¥{report['annual_costs']['monthly_cost']}")
    print(f"  日成本: ¥{report['annual_costs']['daily_cost']}")
    print(f"  年耗油: {report['annual_costs']['fuel_consumed_liters']}升")
    
    print(f"\n碳排放:")
    print(f"  年排放: {report['co2_emissions_kg']} kg CO2")
    
    print(f"\n效率评级:")
    print(f"  等级: {report['efficiency_rating']['grade']} - {report['efficiency_rating']['description']}")
    print(f"  建议: {report['efficiency_rating']['suggestion']}")
    
    print(f"\n燃油信息:")
    print(f"  类型: {report['fuel_info']['name_cn']} ({report['fuel_info']['name_en']})")
    print(f"  CO2因子: {report['fuel_info']['co2_per_liter']} kg/L")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Fuel Efficiency Utils - 使用示例演示")
    print("=" * 60)
    
    example_unit_conversion()
    example_fuel_cost()
    example_range_calculation()
    example_co2_emissions()
    example_annual_cost()
    example_vehicle_comparison()
    example_break_even()
    example_efficiency_rating()
    example_trip_calculation()
    example_full_report()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()