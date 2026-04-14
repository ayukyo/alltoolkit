"""
Temperature Utils - 使用示例

演示温度转换工具的各种用法
"""

import sys
import os
# 添加 AllToolkit 目录到路径
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, base_dir)

from Python.temperature_utils.mod import (
    TemperatureUnit,
    ABSOLUTE_ZERO,
    REFERENCE_POINTS,
    TemperatureError,
    InvalidTemperatureError,
    InvalidUnitError,
    convert,
    convert_all,
    batch_convert,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    fahrenheit_to_celsius,
    kelvin_to_celsius,
    is_valid_temperature,
    is_above_freezing,
    is_below_freezing,
    is_fever,
    is_hypothermia,
    get_temperature_category,
    get_temperature_description,
    compare,
    add,
    subtract,
    difference,
    in_range,
    get_reference_point,
    list_reference_points,
    find_nearest_reference,
    format_temperature,
    parse_temperature,
)


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_basic_conversion():
    """基础转换示例"""
    print_section("1. 基础转换")
    
    # 基本单位转换
    print("摄氏度 → 华氏度:")
    temps = [0, 20, 37, 100, -40]
    for t in temps:
        print(f"  {t}°C → {celsius_to_fahrenheit(t)}°F")
    
    print("\n华氏度 → 摄氏度:")
    temps = [32, 68, 98.6, 212, -40]
    for t in temps:
        print(f"  {t}°F → {fahrenheit_to_celsius(t)}°C")
    
    print("\n摄氏度 → 开尔文:")
    temps = [0, 20, 100, -273.15]
    for t in temps:
        print(f"  {t}°C → {celsius_to_kelvin(t)}K")
    
    print("\n开尔文 → 摄氏度:")
    temps = [0, 273.15, 373.15]
    for t in temps:
        print(f"  {t}K → {kelvin_to_celsius(t)}°C")


def example_convert_function():
    """通用转换函数示例"""
    print_section("2. 通用转换函数 convert()")
    
    # 基本转换
    print("基本转换:")
    print(f"  convert(0, 'C', 'F') → {convert(0, 'C', 'F')}°F")
    print(f"  convert(100, 'C', 'K') → {convert(100, 'C', 'K')}K")
    print(f"  convert(32, 'F', 'C') → {convert(32, 'F', 'C')}°C")
    
    # 单位别名
    print("\n单位别名支持:")
    print(f"  convert(0, 'celsius', 'fahrenheit') → {convert(0, 'celsius', 'fahrenheit')}°F")
    print(f"  convert(0, '摄氏度', '华氏度') → {convert(0, '摄氏度', '华氏度')}°F")
    print(f"  convert(37, '人体温度', 'K') → 报错（无效别名）")
    
    # 精度控制
    print("\n精度控制:")
    print(f"  convert(36.555, 'C', 'F', precision=2) → {convert(36.555, 'C', 'F', precision=2)}°F")
    print(f"  convert(36.555, 'C', 'F', precision=0) → {convert(36.555, 'C', 'F', precision=0)}°F")


def example_convert_all():
    """转换到所有单位"""
    print_section("3. 转换到所有单位")
    
    temps = [0, 37, 100, -40]
    for t in temps:
        result = convert_all(t, 'C')
        print(f"{t}°C:")
        print(f"  摄氏度: {result['celsius']}°C")
        print(f"  华氏度: {result['fahrenheit']}°F")
        print(f"  开尔文: {result['kelvin']}K")
        print(f"  兰氏度: {result['rankine']}°R")
        print()


def example_batch_convert():
    """批量转换"""
    print_section("4. 批量转换")
    
    temperatures = [0, 20, 40, 60, 80, 100]
    
    print("批量转华氏度:")
    results = batch_convert(temperatures, 'C', 'F')
    for original, converted, error in results:
        print(f"  {original}°C → {converted}°F")
    
    print("\n批量转开尔文:")
    results = batch_convert(temperatures, 'C', 'K', precision=2)
    for original, converted, error in results:
        print(f"  {original}°C → {converted}K")


def example_validation():
    """温度验证"""
    print_section("5. 温度验证")
    
    # 绝对零度检查
    print("绝对零度检查:")
    test_cases = [-300, -273.15, 0, 100]
    for t in test_cases:
        valid = is_valid_temperature(t, 'C')
        status = "✓ 有效" if valid else "✗ 无效（低于绝对零度）"
        print(f"  {t}°C → {status}")
    
    # 冰点检查
    print("\n冰点检查:")
    test_cases = [-10, 0, 10, 25]
    for t in test_cases:
        above = is_above_freezing(t, 'C')
        below = is_below_freezing(t, 'C')
        status = "冰点以上" if above else ("冰点以下" if below else "在冰点")
        print(f"  {t}°C → {status}")


def example_body_temperature():
    """体温相关"""
    print_section("6. 体温检测")
    
    temperatures = [34, 35, 36, 37, 37.5, 38, 39, 40]
    
    print("体温状态检测:")
    for t in temperatures:
        status = []
        if is_hypothermia(t, 'C'):
            status.append("体温过低")
        if is_fever(t, 'C'):
            status.append("发烧")
        if not status:
            status.append("正常")
        
        print(f"  {t}°C → {', '.join(status)}")


def example_temperature_category():
    """温度类别"""
    print_section("7. 温度类别")
    
    temperatures = [-40, -20, -5, 5, 15, 25, 28, 33, 38, 45]
    
    print("温度类别分类:")
    for t in temperatures:
        category = get_temperature_category(t, 'C')
        print(f"  {t}°C → {category}")


def example_temperature_description():
    """温度完整描述"""
    print_section("8. 温度完整描述")
    
    temps = [-40, 0, 25, 37, 100]
    for t in temps:
        desc = get_temperature_description(t, 'C')
        print(f"  {desc}")


def example_compare():
    """温度比较"""
    print_section("9. 温度比较")
    
    # 不同单位的温度比较
    pairs = [
        (0, 'C', 32, 'F'),
        (100, 'C', 212, 'F'),
        (0, 'C', 0, 'F'),
        (37, 'C', 100, 'F'),
    ]
    
    print("温度比较:")
    for t1, u1, t2, u2 in pairs:
        result = compare(t1, u1, t2, u2)
        if result == 0:
            relation = "等于"
        elif result < 0:
            relation = "小于"
        else:
            relation = "大于"
        print(f"  {t1}°{u1} {relation} {t2}°{u2}")


def example_arithmetic():
    """温度运算"""
    print_section("10. 温度运算")
    
    # 加法
    print("温度加法（加温差）:")
    print(f"  0°C + 10°C温差 = {add(0, 'C', 10, 'C')}°C")
    print(f"  32°F + 10°C温差 = {add(32, 'F', 10, 'C')}°F")
    
    # 减法
    print("\n温度减法（减温差）:")
    print(f"  10°C - 5°C温差 = {subtract(10, 'C', 5, 'C')}°C")
    
    # 温差计算
    print("\n温差计算:")
    print(f"  100°C - 0°C = {difference(100, 'C', 0, 'C')}°C温差")
    print(f"  212°F - 32°F (以°C表示) = {difference(212, 'F', 32, 'F', 'C')}°C温差")


def example_range_check():
    """范围检查"""
    print_section("11. 范围检查")
    
    # 舒适室温范围 (20-26°C)
    temps = [15, 20, 22, 25, 26, 30]
    print("检查是否在舒适室温范围 (20-26°C):")
    for t in temps:
        in_comfort = in_range(t, 'C', 20, 26, 'C')
        status = "✓ 舒适" if in_comfort else "✗ 不舒适"
        print(f"  {t}°C → {status}")
    
    # 不同单位范围
    print("\n检查华氏度温度是否在摄氏度范围:")
    temps_f = [68, 77, 86, 95]
    for t in temps_f:
        in_comfort = in_range(t, 'F', 20, 26, 'C')
        celsius = convert(t, 'F', 'C')
        status = "✓ 在范围内" if in_comfort else "✗ 超出范围"
        print(f"  {t}°F ({celsius:.1f}°C) → {status}")


def example_reference_points():
    """温度参考点"""
    print_section("12. 温度参考点")
    
    # 列出所有参考点
    print("常见温度参考点:")
    points = list_reference_points()
    for name, desc, celsius in points:
        print(f"  {name}: {celsius}°C ({desc})")
    
    # 获取特定参考点
    print("\n水沸点详细信息:")
    boiling = get_reference_point('water_boiling')
    print(f"  摄氏度: {boiling['celsius']}°C")
    print(f"  华氏度: {boiling['fahrenheit']}°F")
    print(f"  开尔文: {boiling['kelvin']}K")
    print(f"  兰氏度: {boiling['rankine']}°R")
    print(f"  描述: {boiling['description']}")
    
    # 找最近参考点
    print("\n找最近的参考点:")
    temps = [37, 99, -78, 5500]
    for t in temps:
        name, desc, diff = find_nearest_reference(t, 'C')
        print(f"  {t}°C → 最接近 {name} ({desc}), 差 {diff}°C")


def example_format_parse():
    """格式化与解析"""
    print_section("13. 格式化与解析")
    
    # 格式化
    print("温度格式化:")
    temps = [36.5, 100.0, -40.5]
    for t in temps:
        print(f"  默认: {format_temperature(t, 'C')}")
        print(f"  整数: {format_temperature(t, 'C', precision=0)}")
        print(f"  无单位: {format_temperature(t, 'C', include_unit=False)}")
    
    # 解析
    print("\n温度字符串解析:")
    strings = ['36.5°C', '100 F', '273.15K', '-40.5°R']
    for s in strings:
        value, unit = parse_temperature(s)
        print(f"  '{s}' → {value} {unit.name}")


def example_absolute_zero():
    """绝对零度"""
    print_section("14. 绝对零度")
    
    print("绝对零度（物理最低温度）:")
    for unit, value in ABSOLUTE_ZERO.items():
        print(f"  {unit.name}: {value}")
    
    print("\n绝对零度转换验证:")
    print(f"  0K = {convert(0, 'K', 'C')}°C")
    print(f"  -273.15°C = {convert(-273.15, 'C', 'K')}K")
    print(f"  -459.67°F = {convert(-459.67, 'F', 'K')}K")


def example_practical():
    """实际应用"""
    print_section("15. 实际应用")
    
    # 天气温度
    print("天气温度转换:")
    weather = {
        '北京': 15,
        '上海': 22,
        '广州': 28,
        '哈尔滨': -5,
    }
    for city, temp in weather.items():
        f = convert(temp, 'C', 'F')
        print(f"  {city}: {temp}°C / {f}°F - {get_temperature_category(temp, 'C')}")
    
    # 烹饪温度
    print("\n烹饪温度参考:")
    cooking_temps = {
        '低温慢煮': 55,
        '中温烤制': 165,
        '高温快烤': 220,
    }
    for name, temp in cooking_temps.items():
        f = convert(temp, 'C', 'F')
        print(f"  {name}: {temp}°C ({f}°F)")
    
    # 科学计算
    print("\n科学研究温度:")
    science_temps = {
        '液氮温度': -195.8,
        '室温': 20,
        '人体温度': 37,
        '水沸点': 100,
    }
    for name, temp in science_temps.items():
        kelvin = convert(temp, 'C', 'K', precision=2)
        print(f"  {name}: {temp}°C = {kelvin}K")


def main():
    """运行所有示例"""
    print("="*60)
    print("  Temperature Utils - 使用示例")
    print("="*60)
    
    example_basic_conversion()
    example_convert_function()
    example_convert_all()
    example_batch_convert()
    example_validation()
    example_body_temperature()
    example_temperature_category()
    example_temperature_description()
    example_compare()
    example_arithmetic()
    example_range_check()
    example_reference_points()
    example_format_parse()
    example_absolute_zero()
    example_practical()
    
    print_section("完成!")
    print("所有示例已运行完成。")
    print(f"\n支持单位: C(摄氏度), F(华氏度), K(开尔文), R(兰氏度)")
    print(f"绝对零度: {ABSOLUTE_ZERO[TemperatureUnit.CELSIUS]}°C")


if __name__ == '__main__':
    main()