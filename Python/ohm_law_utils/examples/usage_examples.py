"""
Ohm's Law Utilities 使用示例

本示例展示如何使用欧姆定律计算工具进行各种电子计算。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    OhmLawCalculator, OhmLawResult, ResistorCalculator,
    VoltageDivider, CurrentDivider, PowerCalculator,
    ResistorColorCode, calculate, series_resistance, parallel_resistance
)


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_basic_ohm_law():
    """基础欧姆定律计算"""
    print_section("基础欧姆定律计算")
    
    # 方法1：使用便捷函数 calculate()
    print("\n【方法1：便捷函数】")
    result = calculate(voltage=12, resistance=4)
    print(f"已知: 电压=12V, 电阻=4Ω")
    print(f"结果:\n{result}")
    
    # 方法2：使用计算器类
    print("\n【方法2：计算器类】")
    result2 = OhmLawCalculator.from_current_resistance(current=2, resistance=5)
    print(f"已知: 电流=2A, 电阻=5Ω")
    print(f"电压: {result2.voltage}V")
    print(f"功率: {result2.power}W")
    
    # 方法3：已知电压和电流
    print("\n【方法3：从电压和功率计算】")
    result3 = OhmLawCalculator.from_voltage_power(voltage=9, power=4.5)
    print(f"已知: 电压=9V, 功率=4.5W")
    print(f"电流: {result3.current}A")
    print(f"电阻: {result3.resistance}Ω")


def example_resistor_combinations():
    """电阻组合计算"""
    print_section("电阻组合计算")
    
    # 串联电阻
    print("\n【串联电阻】")
    resistors = [100, 220, 330, 470]
    total = series_resistance(*resistors)
    print(f"串联电阻: {' + '.join(map(str, resistors))} = {total}Ω")
    
    # 并联电阻
    print("\n【并联电阻】")
    resistors = [100, 100, 100]
    total = parallel_resistance(*resistors)
    print(f"三个100Ω电阻并联 = {total:.2f}Ω")
    
    resistors = [1000, 2200]
    total = parallel_resistance(*resistors)
    print(f"1kΩ || 2.2kΩ = {total:.2f}Ω")
    
    # 混合连接
    print("\n【混合连接】")
    # 10kΩ 串联 (20kΩ || 30kΩ) 串联 40kΩ
    config = [10000, [20000, 30000], 40000]
    total = ResistorCalculator.mixed(config)
    print(f"10kΩ + (20kΩ||30kΩ) + 40kΩ = {total/1000:.2f}kΩ")
    
    # 查找最佳组合
    print("\n【查找最佳电阻组合】")
    available = [10, 22, 47, 100, 220, 470, 1000, 2200, 4700]
    target = 500
    combos = ResistorCalculator.find_combination(target, available, max_count=2)
    print(f"目标: {target}Ω，使用标准值: {available}")
    print("最佳串联组合:")
    for combo, actual in combos[:3]:
        print(f"  {' + '.join(map(str, combo))} = {actual}Ω")


def example_voltage_divider():
    """分压器计算"""
    print_section("分压器计算")
    
    # 基本分压计算
    print("\n【基本分压计算】")
    vin = 12
    r1, r2 = 10000, 2000
    vout = VoltageDivider.calculate(vin, r1, r2)
    print(f"输入: {vin}V")
    print(f"电阻: R1={r1/1000}kΩ, R2={r2/1000}kΩ")
    print(f"输出: {vout:.2f}V")
    
    # 设计分压器
    print("\n【设计分压器】")
    vin = 5
    vout_target = 3.3
    available = [1000, 2200, 3300, 4700, 10000, 22000]
    print(f"目标: 从{vin}V分压到{vout_target}V")
    print("可用电阻:", ', '.join(f"{r}" for r in available))
    
    combos = VoltageDivider.find_resistors(vin, vout_target, available)
    print("\n最佳组合:")
    for r1, r2, actual in combos[:3]:
        print(f"  R1={r1}Ω, R2={r2}Ω → Vout={actual:.3f}V")


def example_current_divider():
    """分流器计算"""
    print_section("分流器计算")
    
    print("\n【基本分流计算】")
    itotal = 1.0  # 总电流1A
    r1, r2 = 100, 200
    i1, i2 = CurrentDivider.calculate(itotal, r1, r2)
    print(f"总电流: {itotal}A")
    print(f"电阻: R1={r1}Ω, R2={r2}Ω")
    print(f"分流结果: I1={i1:.3f}A, I2={i2:.3f}A")
    print(f"验证: I1+I2={i1+i2:.3f}A (应等于总电流)")
    
    # 相等电阻分流
    print("\n【相等电阻分流】")
    i1, i2 = CurrentDivider.calculate(2.0, 100, 100)
    print(f"两个100Ω电阻并联，总电流2A")
    print(f"每个支路电流: {i1}A")


def example_power_calculations():
    """功率计算"""
    print_section("功率计算")
    
    # 直流功率
    print("\n【直流功率】")
    result = calculate(voltage=12, current=2)
    print(f"电压=12V, 电流=2A")
    print(f"功率: {result.power}W")
    print(f"电阻: {result.resistance}Ω")
    
    # 交流功率
    print("\n【交流功率】")
    ac = PowerCalculator.ac_power(voltage=220, current=10, power_factor=0.8)
    print(f"电压=220V, 电流=10A, 功率因数=0.8")
    print(f"视在功率: {ac['apparent_power']}VA")
    print(f"有功功率: {ac['real_power']}W")
    print(f"无功功率: {ac['reactive_power']:.2f}VAR")
    
    # 电费计算
    print("\n【电费计算】")
    appliance_power = 1500  # 1500W电器
    hours = 30 * 2  # 每天2小时，30天
    rate = 0.6  # 0.6元/kWh
    energy = PowerCalculator.energy_cost(appliance_power, hours, rate)
    print(f"电器功率: {appliance_power}W")
    print(f"使用时间: {hours}小时 (每天2小时，30天)")
    print(f"电价: {rate}元/kWh")
    print(f"消耗电能: {energy['energy_kwh']}kWh")
    print(f"电费: {energy['cost']:.2f}元")
    
    # 电池续航
    print("\n【电池续航估算】")
    capacity = 5000  # 5000mAh
    current = 500    # 500mA
    battery = PowerCalculator.battery_life(capacity, current, 0.85)
    print(f"电池容量: {capacity}mAh")
    print(f"工作电流: {current}mA")
    print(f"效率: 85%")
    print(f"续航时间: {battery['hours']:.1f}小时 ({battery['minutes']:.0f}分钟)")


def example_resistor_color_code():
    """电阻色环解码"""
    print_section("电阻色环解码")
    
    # 4色环解码
    print("\n【4色环解码】")
    colors_4 = [
        ('brown', 'black', 'red', 'gold'),
        ('red', 'red', 'orange', 'gold'),
        ('yellow', 'violet', 'yellow', 'gold'),
    ]
    
    color_names = {
        'brown': '棕', 'black': '黑', 'red': '红', 'orange': '橙',
        'yellow': '黄', 'green': '绿', 'blue': '蓝', 'violet': '紫',
        'gray': '灰', 'white': '白', 'gold': '金', 'silver': '银'
    }
    
    for band1, band2, band3, band4 in colors_4:
        result = ResistorColorCode.decode_4band(band1, band2, band3, band4)
        print(f"{color_names[band1]}-{color_names[band2]}-{color_names[band3]}-{color_names[band4]}")
        print(f"  → {OhmLawResult.format_value(result['resistance'], 'Ω')} ±{result['tolerance']}%")
        print(f"  范围: {OhmLawResult.format_value(result['range'][0], 'Ω')} ~ {OhmLawResult.format_value(result['range'][1], 'Ω')}")
    
    # 5色环解码
    print("\n【5色环解码】")
    colors_5 = ('red', 'red', 'black', 'red', 'brown')
    result = ResistorColorCode.decode_5band(*colors_5)
    print(f"红-红-黑-红-棕")
    print(f"  → {OhmLawResult.format_value(result['resistance'], 'Ω')} ±{result['tolerance']}%")
    
    # 色环编码
    print("\n【色环编码】")
    values = [100, 470, 1000, 10000, 47000]
    for value in values:
        colors = ResistorColorCode.encode(value, 5)
        color_cn = '-'.join(color_names.get(c, c) for c in colors)
        print(f"{value}Ω → {color_cn}")


def example_practical_applications():
    """实际应用示例"""
    print_section("实际应用示例")
    
    # LED限流电阻计算
    print("\n【LED限流电阻计算】")
    supply = 5      # 供电电压5V
    led_vf = 2.1    # LED正向压降2.1V
    led_current = 0.020  # 期望电流20mA
    
    resistor_voltage = supply - led_vf
    resistor_value = resistor_voltage / led_current
    power = resistor_voltage * led_current
    
    print(f"供电电压: {supply}V")
    print(f"LED压降: {led_vf}V")
    print(f"期望电流: {led_current * 1000}mA")
    print(f"需要电阻: {resistor_value:.1f}Ω")
    print(f"电阻功率: {power * 1000:.1f}mW")
    print(f"建议使用: 150Ω, 1/4W电阻")
    
    # USB充电器功率计算
    print("\n【USB充电器计算】")
    usb_voltage = 5.0
    fast_charge_current = 2.0
    result = calculate(voltage=usb_voltage, current=fast_charge_current)
    print(f"USB电压: {usb_voltage}V")
    print(f"快充电流: {fast_charge_current}A")
    print(f"输出功率: {result.power}W")
    print(f"等效电阻: {result.resistance}Ω")
    
    # 家用电器耗电分析
    print("\n【家用电器耗电分析】")
    appliances = [
        ("空调", 1500, 8),
        ("冰箱", 150, 24),
        ("电视", 100, 4),
        ("洗衣机", 500, 1),
        ("电脑", 200, 6),
    ]
    rate = 0.6
    total_cost = 0
    
    print(f"{'电器':<10} {'功率(W)':<10} {'时间(h)':<10} {'耗电(kWh)':<12} {'费用(元)':<10}")
    print("-" * 52)
    
    for name, power, hours in appliances:
        energy = PowerCalculator.energy_cost(power, hours, rate)
        total_cost += energy['cost']
        print(f"{name:<10} {power:<10} {hours:<10} {energy['energy_kwh']:<12.2f} {energy['cost']:<10.2f}")
    
    print("-" * 52)
    print(f"{'合计':<32} {power*hours/1000*30:.2f}kWh/月  {total_cost*30:.2f}元/月")


def example_formatted_output():
    """格式化输出示例"""
    print_section("格式化输出示例")
    
    # OhmLawResult 自动格式化
    print("\n【自动单位前缀】")
    results = [
        calculate(voltage=12000000, resistance=1000),  # 12MV
        calculate(voltage=0.001, resistance=1000),     # 1mV
        calculate(voltage=12, current=0.000001),       # 1μA
        calculate(voltage=12, current=5),              # 60W
    ]
    
    for r in results:
        print(r)
        print()


if __name__ == "__main__":
    example_basic_ohm_law()
    example_resistor_combinations()
    example_voltage_divider()
    example_current_divider()
    example_power_calculations()
    example_resistor_color_code()
    example_practical_applications()
    example_formatted_output()
    
    print_section("示例演示完成")