"""
Battery Utils 使用示例
==========================================

演示电池计算工具的各种用法。
"""

from mod import (
    BatteryCalculator,
    BatteryType,
    calculate_charge_time,
    estimate_runtime,
    calculate_battery_health
)


def example_charge_time():
    """充电时间计算示例"""
    print("\n" + "=" * 50)
    print("充电时间计算示例")
    print("=" * 50)
    
    # 基本充电时间
    print("\n【基本充电时间】")
    result = calculate_charge_time(3000, 1000)  # 3000mAh电池，1000mA充电
    print(f"电池容量: 3000mAh")
    print(f"充电电流: 1000mA")
    print(f"预计充电时间: {result['formatted']}")
    print(f"详细: {result['hours']}小时{result['minutes']}分钟{result['seconds']}秒")
    
    # 快速充电
    print("\n【快速充电】")
    fast = calculate_charge_time(3000, 2000)  # 2A快充
    print(f"充电电流: 2000mA (快充)")
    print(f"预计充电时间: {fast['formatted']}")
    
    # 从50%开始充电
    print("\n【部分充电】")
    partial = BatteryCalculator.calculate_charge_time(3000, 1000, 0.85, 50)
    print(f"当前电量: 50%")
    print(f"充电时间: {partial['formatted']}")
    
    # 比较不同充电效率
    print("\n【充电效率对比】")
    for efficiency in [0.70, 0.85, 0.95]:
        result = BatteryCalculator.calculate_charge_time(3000, 1000, efficiency)
        print(f"效率 {efficiency*100}%: {result['formatted']}")


def example_runtime():
    """续航估算示例"""
    print("\n" + "=" * 50)
    print("续航估算示例")
    print("=" * 50)
    
    # 手机续航估算
    print("\n【智能手机续航】")
    battery = 3000  # mAh
    voltage = 3.7   # V
    
    scenarios = {
        '待机': 0.5,      # W
        '日常使用': 2,     # W
        '视频播放': 3,     # W
        '游戏': 5         # W
    }
    
    for scenario, power in scenarios.items():
        runtime = estimate_runtime(battery, voltage, power)
        print(f"{scenario} ({power}W): {runtime:.1f}小时")
    
    # 笔记本电脑续航
    print("\n【笔记本电脑续航】")
    laptop_battery = 50000  # 50Wh约等于50000mAh@3.7V
    laptop_scenarios = {
        '文档办公': 20,
        '网页浏览': 30,
        '视频剪辑': 60,
        '游戏': 80
    }
    
    for scenario, power in laptop_scenarios.items():
        runtime = estimate_runtime(laptop_battery, 3.7, power)
        print(f"{scenario} ({power}W): {runtime:.1f}小时")


def example_battery_health():
    """电池健康度评估示例"""
    print("\n" + "=" * 50)
    print("电池健康度评估示例")
    print("=" * 50)
    
    # 新电池
    print("\n【新电池评估】")
    new_battery = BatteryCalculator.calculate_battery_health(3000, 3000, 0)
    print(f"原容量: 3000mAh")
    print(f"现容量: 3000mAh")
    print(f"循环次数: 0次")
    print(f"健康度: {new_battery['overall_health_percent']}%")
    print(f"等级: {new_battery['grade']} ({new_battery['status']})")
    print(f"建议: {new_battery['suggestion']}")
    
    # 使用一年的电池
    print("\n【使用一年的电池】")
    one_year = BatteryCalculator.calculate_battery_health(2700, 3000, 150)
    print(f"原容量: 3000mAh")
    print(f"现容量: 2700mAh")
    print(f"循环次数: 150次")
    print(f"健康度: {one_year['overall_health_percent']}%")
    print(f"等级: {one_year['grade']} ({one_year['status']})")
    print(f"剩余循环: {one_year['remaining_cycles']}次")
    
    # 需要更换的电池
    print("\n【老化电池】")
    old_battery = BatteryCalculator.calculate_battery_health(1800, 3000, 400)
    print(f"原容量: 3000mAh")
    print(f"现容量: 1800mAh")
    print(f"循环次数: 400次")
    print(f"健康度: {old_battery['overall_health_percent']}%")
    print(f"等级: {old_battery['grade']} ({old_battery['status']})")
    print(f"建议: {old_battery['suggestion']}")


def example_degradation():
    """电池衰减预测示例"""
    print("\n" + "=" * 50)
    print("电池衰减预测示例")
    print("=" * 50)
    
    # 不同使用年限的衰减
    print("\n【锂离子电池衰减曲线】")
    for years in [1, 2, 3, 5]:
        result = BatteryCalculator.model_degradation(years)
        print(f"{years}年后: 剩余容量 {result['remaining_capacity_percent']}%")
    
    # 温度影响
    print("\n【温度对衰减的影响】")
    temperatures = [15, 25, 35, 45]
    for temp in temperatures:
        result = BatteryCalculator.model_degradation(2, BatteryType.LI_ION, 365, temp)
        print(f"{temp}°C工作环境: 剩余容量 {result['remaining_capacity_percent']}%")
    
    # 不同电池类型对比
    print("\n【不同电池类型衰减对比】(使用5年)")
    battery_types = [
        BatteryType.LI_ION,
        BatteryType.LI_PO,
        BatteryType.LI_FEPO4,
        BatteryType.NIMH
    ]
    
    for bt in battery_types:
        result = BatteryCalculator.model_degradation(5, bt)
        name = BatteryCalculator.BATTERY_PROPERTIES[bt]['name_cn']
        print(f"{name}: {result['remaining_capacity_percent']}%")


def example_power_analysis():
    """功耗分析示例"""
    print("\n" + "=" * 50)
    print("功耗分析示例")
    print("=" * 50)
    
    # 手机日常使用分析
    print("\n【手机日常使用分析】")
    usage_pattern = {
        'active': 4,    # 活跃使用4小时
        'idle': 20      # 待机20小时
    }
    
    analysis = BatteryCalculator.analyze_power_consumption(3000, 3.7, usage_pattern)
    print(f"电池容量: 3000mAh")
    print(f"使用模式: 活跃4小时，待机20小时")
    print(f"日功耗: {analysis['total_daily_consumption_wh']}Wh")
    print(f"续航: {analysis['runtime_days']}天")
    
    # 不同使用模式对比
    print("\n【使用模式对比】")
    patterns = {
        '轻度使用': {'idle': 22, 'active': 2},
        '中度使用': {'idle': 16, 'active': 8},
        '重度使用': {'active': 12, 'idle': 12}
    }
    
    for pattern_name, pattern in patterns.items():
        analysis = BatteryCalculator.analyze_power_consumption(3000, 3.7, pattern)
        print(f"{pattern_name}: 续航 {analysis['runtime_hours']}小时")


def example_charger_recommend():
    """充电器推荐示例"""
    print("\n" + "=" * 50)
    print("充电器推荐示例")
    print("=" * 50)
    
    # 不同容量电池的充电器推荐
    print("\n【充电器推荐】")
    capacities = [2000, 3000, 4000, 5000]
    
    for cap in capacities:
        standard = BatteryCalculator.recommend_charger(cap, BatteryType.LI_ION, False)
        fast = BatteryCalculator.recommend_charger(cap, BatteryType.LI_ION, True)
        
        print(f"\n{cap}mAh电池:")
        print(f"  标准充电: {int(standard['recommended_current_ma'])}mA, "
              f"时间 {standard['estimated_charge_time']}")
        print(f"  快速充电: {int(fast['recommended_current_ma'])}mA, "
              f"时间 {fast['estimated_charge_time']}")


def example_battery_config():
    """电池配置示例"""
    print("\n" + "=" * 50)
    print("电池配置示例")
    print("=" * 50)
    
    # 并联增加容量
    print("\n【并联配置】(增加容量)")
    parallel = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'parallel')
    print(f"2节3000mAh电池并联")
    print(f"总容量: {parallel['total_capacity_mah']}mAh")
    print(f"总电压: {parallel['total_voltage']}V")
    print(f"总能量: {parallel['total_energy_wh']}Wh")
    
    # 串联增加电压
    print("\n【串联配置】(增加电压)")
    series = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'series')
    print(f"2节3000mAh电池串联")
    print(f"总容量: {series['total_capacity_mah']}mAh")
    print(f"总电压: {series['total_voltage']}V")
    print(f"总能量: {series['total_energy_wh']}Wh")
    
    # 电动车电池组示例
    print("\n【电动车电池组】")
    # 96节电池，3串32并
    ev_config = BatteryCalculator.calculate_parallel_series(96, 3000, 3.7, 'both')
    print(f"96节电池混联")
    print(f"总容量: {ev_config['total_capacity_mah']}mAh")
    print(f"总电压: {ev_config['total_voltage']}V")


def example_battery_comparison():
    """电池比较示例"""
    print("\n" + "=" * 50)
    print("电池比较示例")
    print("=" * 50)
    
    # 比较不同品牌电池
    print("\n【电池容量对比】")
    batteries = [
        {'name': '品牌A', 'capacity_mah': 2800, 'voltage': 3.7},
        {'name': '品牌B', 'capacity_mah': 3200, 'voltage': 3.7},
        {'name': '品牌C', 'capacity_mah': 3500, 'voltage': 3.7},
        {'name': '品牌D', 'capacity_mah': 5000, 'voltage': 3.85}
    ]
    
    comparison = BatteryCalculator.battery_comparison(batteries)
    
    print("\n排名:")
    for i, bat in enumerate(comparison['rankings'], 1):
        print(f"{i}. {bat['name']}: {bat['capacity_mah']}mAh, "
              f"{bat['voltage']}V, {bat['energy_wh']}Wh "
              f"(相对容量: {bat['relative_capacity_percent']}%)")
    
    print(f"\n最佳选择: {comparison['best']['name']}")
    print(f"总能量: {comparison['total_energy_wh']}Wh")


def example_full_report():
    """完整报告示例"""
    print("\n" + "=" * 50)
    print("完整电池报告示例")
    print("=" * 50)
    
    report = BatteryCalculator.full_battery_report(
        capacity_mah=3000,
        voltage=3.7,
        battery_type=BatteryType.LI_ION,
        cycle_count=150,
        current_capacity_mah=2700,
        average_power_w=2.0
    )
    
    print("\n【电池规格】")
    print(f"容量: {report['specs']['capacity_mah']}mAh")
    print(f"电压: {report['specs']['voltage']}V")
    print(f"能量: {report['specs']['energy_wh']}Wh")
    print(f"类型: {report['specs']['battery_name_cn']}")
    print(f"预期循环寿命: {report['specs']['expected_cycle_life']}次")
    
    print("\n【充电建议】")
    print(f"标准充电电流: {int(report['charging']['standard']['recommended_current_ma'])}mA")
    print(f"标准充电时间: {report['charging']['standard']['estimated_time']}")
    print(f"快充电流: {int(report['charging']['fast_charge']['recommended_current_ma'])}mA")
    print(f"快充时间: {report['charging']['fast_charge']['estimated_time']}")
    
    print("\n【续航估算】")
    print(f"功耗2W时续航: {report['runtime']['total_hours']}小时")
    
    print("\n【健康状态】")
    if report['health']:
        print(f"健康度: {report['health']['overall_health_percent']}%")
        print(f"等级: {report['health']['grade']} ({report['health']['status']})")
        print(f"建议: {report['health']['suggestion']}")
    
    print("\n【衰减预测】")
    print(f"1年后剩余容量: {report['degradation_forecast']['1_year']['remaining_capacity_percent']}%")
    print(f"3年后剩余容量: {report['degradation_forecast']['3_years']['remaining_capacity_percent']}%")
    
    print("\n【使用建议】")
    for tip in report['tips']:
        print(f"• {tip}")


def example_ev_battery():
    """电动车电池计算示例"""
    print("\n" + "=" * 50)
    print("电动车电池计算示例")
    print("=" * 50)
    
    # 假设电动车电池 60kWh
    capacity_kwh = 60
    capacity_wh = capacity_kwh * 1000
    
    # 不同能耗下的续航
    print("\n【续航估算】")
    efficiencies = [120, 150, 180]  # Wh/km
    
    for eff in efficiencies:
        range_km = capacity_wh / eff
        print(f"能耗 {eff} Wh/km: 续航 {range_km:.0f} km")
    
    # 充电时间
    print("\n【充电时间估算】")
    charger_powers = [7, 22, 50, 120]  # kW
    
    for power in charger_powers:
        hours = capacity_kwh / power * 1.15  # 考虑15%损耗
        print(f"{power}kW充电桩: {hours:.1f}小时充满")
    
    # 磷酸铁锂电池衰减
    print("\n【磷酸铁锂电池衰减】")
    for years in [1, 3, 5, 10]:
        degradation = BatteryCalculator.model_degradation(
            years, BatteryType.LI_FEPO4, 365, 25
        )
        print(f"{years}年后: {degradation['remaining_capacity_percent']}%容量")


def main():
    """运行所有示例"""
    example_charge_time()
    example_runtime()
    example_battery_health()
    example_degradation()
    example_power_analysis()
    example_charger_recommend()
    example_battery_config()
    example_battery_comparison()
    example_full_report()
    example_ev_battery()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()