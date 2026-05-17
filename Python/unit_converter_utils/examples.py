#!/usr/bin/env python3
"""
Unit Converter 使用示例

展示各种单位转换的使用方法
"""

from converter import UnitConverter, convert, convert_length, convert_weight
from converter import convert_temperature, convert_volume, convert_area
from converter import convert_time, convert_speed, convert_data, convert_pressure, convert_angle


def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    converter = UnitConverter(precision=4)
    
    # ============ 长度转换示例 ============
    print_separator("长度转换示例")
    
    print("\n[基础用法]")
    print(f"1000 米 = {convert_length(1000, 'm', 'km')} 公里")
    print(f"1 英里 = {convert_length(1, 'mi', 'km')} 公里")
    print(f"1 海里 = {convert_length(1, 'nmi', 'km')} 公里")
    print(f"1 光年 = {convert_length(1, 'ly', 'km')} 公里")
    print(f"6 英尺 = {convert_length(6, 'ft', 'm')} 米")
    print(f"72 英寸 = {convert_length(72, 'in', 'cm')} 厘米")
    
    # ============ 重量转换示例 ============
    print_separator("重量转换示例")
    
    print("\n[国际单位]")
    print(f"1 千克 = {convert_weight(1, 'kg', 'g')} 克")
    print(f"1 吨 = {convert_weight(1, 't', 'kg')} 千克")
    
    print("\n[英制单位]")
    print(f"1 磅 = {convert_weight(1, 'lb', 'kg')} 千克")
    print(f"1 盎司 = {convert_weight(1, 'oz', 'g')} 克")
    print(f"1 英石 = {convert_weight(1, 'st', 'kg')} 千克")
    
    print("\n[中国传统单位]")
    print(f"1 市斤 = {convert_weight(1, 'jin', 'kg')} 千克")
    print(f"1 两 = {convert_weight(1, 'liang', 'g')} 克")
    print(f"1 克拉 = {convert_weight(1, 'ct', 'g')} 克")
    
    # ============ 温度转换示例 ============
    print_separator("温度转换示例")
    
    print("\n[常见温度点]")
    print(f"0°C = {convert_temperature(0, 'C', 'F')}°F")
    print(f"100°C = {convert_temperature(100, 'C', 'F')}°F")
    print(f"-40°C = {convert_temperature(-40, 'C', 'F')}°F (温度计校准点)")
    print(f"37°C = {convert_temperature(37, 'C', 'F')}°F (人体温度)")
    
    print("\n[绝对零度]")
    print(f"0 K = {convert_temperature(0, 'K', 'C')}°C")
    print(f"273.15 K = {convert_temperature(273.15, 'K', 'C')}°C")
    
    # ============ 体积转换示例 ============
    print_separator("体积转换示例")
    
    print("\n[日常单位]")
    print(f"1 升 = {convert_volume(1, 'L', 'mL')} 毫升")
    print(f"1 立方米 = {convert_volume(1, 'm3', 'L')} 升")
    
    print("\n[美制单位]")
    print(f"1 加仑 = {convert_volume(1, 'gal', 'L')} 升")
    print(f"1 夸脱 = {convert_volume(1, 'qt', 'mL')} 毫升")
    print(f"1 品脱 = {convert_volume(1, 'pt', 'mL')} 毫升")
    print(f"1 杯 = {convert_volume(1, 'cup', 'mL')} 毫升")
    print(f"1 液体盎司 = {convert_volume(1, 'fl_oz', 'mL')} 毫升")
    
    print("\n[厨具单位]")
    print(f"1 汤勺 = {convert_volume(1, 'tbsp', 'mL')} 毫升")
    print(f"1 茶勺 = {convert_volume(1, 'tsp', 'mL')} 毫升")
    
    # ============ 面积转换示例 ============
    print_separator("面积转换示例")
    
    print("\n[标准单位]")
    print(f"1 平方公里 = {convert_area(1, 'km2', 'm2')} 平方米")
    print(f"1 公顷 = {convert_area(1, 'ha', 'm2')} 平方米")
    
    print("\n[英制单位]")
    print(f"1 英亩 = {convert_area(1, 'acre', 'm2')} 平方米")
    print(f"1 平方英尺 = {convert_area(1, 'ft2', 'm2')} 平方米")
    
    print("\n[中国传统单位]")
    print(f"1 亩 = {convert_area(1, 'mu', 'm2')} 平方米")
    print(f"1 顷 = {convert_area(1, 'qing', 'm2')} 平方米")
    
    # ============ 时间转换示例 ============
    print_separator("时间转换示例")
    
    print("\n[日常单位]")
    print(f"1 小时 = {convert_time(1, 'h', 'min')} 分钟")
    print(f"1 天 = {convert_time(1, 'd', 'h')} 小时")
    print(f"1 周 = {convert_time(1, 'w', 'd')} 天")
    print(f"1 年 = {convert_time(1, 'y', 'd')} 天")
    
    print("\n[精确单位]")
    print(f"1 秒 = {convert_time(1, 's', 'ms')} 毫秒")
    print(f"1 毫秒 = {convert_time(1, 'ms', 'us')} 微秒")
    print(f"1 微秒 = {convert_time(1, 'us', 'ns')} 纳秒")
    
    # ============ 速度转换示例 ============
    print_separator("速度转换示例")
    
    print("\n[常见速度]")
    print(f"100 km/h = {convert_speed(100, 'km/h', 'm/s')} m/s")
    print(f"60 mph = {convert_speed(60, 'mph', 'km/h')} km/h")
    print(f"1 节 = {convert_speed(1, 'knot', 'km/h')} km/h")
    print(f"1 马赫 = {convert_speed(1, 'mach', 'm/s')} m/s")
    print(f"光速 = {convert_speed(1, 'c', 'm/s')} m/s")
    
    # ============ 数据转换示例 ============
    print_separator("数据转换示例")
    
    print("\n[十进制 (SI) 单位]")
    print(f"1 KB = {convert_data(1, 'KB', 'B')} 字节")
    print(f"1 MB = {convert_data(1, 'MB', 'KB')} KB")
    print(f"1 GB = {convert_data(1, 'GB', 'MB')} MB")
    print(f"1 TB = {convert_data(1, 'TB', 'GB')} GB")
    
    print("\n[二进制 (IEC) 单位]")
    print(f"1 KiB = {convert_data(1, 'KiB', 'B')} 字节")
    print(f"1 MiB = {convert_data(1, 'MiB', 'KiB')} KiB")
    print(f"1 GiB = {convert_data(1, 'GiB', 'MiB')} MiB")
    
    print("\n[网络速度]")
    print(f"8 bit = {convert_data(8, 'bit', 'B')} 字节")
    print(f"1 Mbit = {convert_data(1, 'Mbit', 'KB')} KB")
    
    # ============ 压力转换示例 ============
    print_separator("压力转换示例")
    
    print("\n[标准单位]")
    print(f"1 kPa = {convert_pressure(1, 'kPa', 'Pa')} Pa")
    print(f"1 MPa = {convert_pressure(1, 'MPa', 'kPa')} kPa")
    
    print("\n[常用单位]")
    print(f"1 bar = {convert_pressure(1, 'bar', 'Pa')} Pa")
    print(f"1 atm = {convert_pressure(1, 'atm', 'Pa')} Pa")
    print(f"1 psi = {convert_pressure(1, 'psi', 'kPa')} kPa")
    
    print("\n[医学单位]")
    print(f"1 mmHg = {convert_pressure(1, 'mmHg', 'Pa')} Pa")
    
    # ============ 角度转换示例 ============
    print_separator("角度转换示例")
    
    print("\n[基础单位]")
    print(f"180° = {convert_angle(180, 'deg', 'rad')} 弧度")
    print(f"π 弧度 = {convert_angle(3.14159265, 'rad', 'deg')} 度")
    print(f"90° = {convert_angle(90, 'deg', 'grad')} 百分度")
    
    print("\n[精密单位]")
    print(f"1° = {convert_angle(1, 'deg', 'arcmin')} 角分")
    print(f"1 角分 = {convert_angle(1, 'arcmin', 'arcsec')} 角秒")
    
    # ============ 高级用法示例 ============
    print_separator("高级用法示例")
    
    print("\n[自动类型检测]")
    print(f"convert(1, 'kg', 'lb') = {convert(1, 'kg', 'lb'):.4f} (自动识别为重量)")
    print(f"convert(1, 'km', 'mi') = {convert(1, 'km', 'mi'):.4f} (自动识别为长度)")
    print(f"convert(100, 'C', 'F') = {convert(100, 'C', 'F'):.4f} (自动识别为温度)")
    
    print("\n[批量转换]")
    conversions = [
        (100, 'km', 'mi'),
        (1, 'kg', 'lb'),
        (0, 'C', 'K'),
        (1, 'gal', 'L'),
    ]
    results = converter.batch_convert(conversions)
    for (val, from_u, to_u), res in zip(conversions, results):
        print(f"  {val} {from_u} = {res:.4f} {to_u}")
    
    print("\n[全量转换 - 将 100 km/h 转换为所有速度单位]")
    all_speeds = converter.convert_all(100, 'km/h', 'speed')
    for unit, value in sorted(all_speeds.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {value:.4f} {unit}")
    
    print("\n[支持的单位类型]")
    units = converter.get_supported_units()
    for category, unit_list in units.items():
        print(f"  {category}: {len(unit_list)} 种单位")
    
    # ============ 实用场景示例 ============
    print_separator("实用场景示例")
    
    print("\n[场景1: 国际旅行]")
    print(f"纽约到洛杉矶: 2800 英里 = {convert_length(2800, 'mi', 'km'):.2f} 公里")
    print(f"汽车油箱: 15 加仑 = {convert_volume(15, 'gal', 'L'):.2f} 升")
    
    print("\n[场景2: 烹饪食谱]")
    print(f"2 杯面粉: 2 cup = {convert_volume(2, 'cup', 'mL'):.0f} mL")
    print(f"350°F 烤箱温度 = {convert_temperature(350, 'F', 'C'):.0f}°C")
    print(f"1 磅牛排 = {convert_weight(1, 'lb', 'g'):.0f} 克")
    
    print("\n[场景3: 健康监测]")
    print(f"血压 120 mmHg = {convert_pressure(120, 'mmHg', 'kPa'):.2f} kPa")
    print(f"体重 150 磅 = {convert_weight(150, 'lb', 'kg'):.2f} kg")
    print(f"体温 98.6°F = {convert_temperature(98.6, 'F', 'C'):.1f}°C")
    
    print("\n[场景4: 科技计算]")
    print(f"网络下载: 100 Mbps = {convert_data(100, 'Mbit', 'MB'):.2f} MB/s (理论最大)")
    print(f"SSD 容量: 512 GB = {convert_data(512, 'GB', 'GiB'):.2f} GiB (实际)")
    print(f"处理器频率: 3.6 GHz = {convert_speed(3.6e9, 'm/s', 'km/h'):.2e} km/h (信号速度)")
    
    print("\n[场景5: 体育运动]")
    print(f"马拉松: 26.2 英里 = {convert_length(26.2, 'mi', 'km'):.2f} 公里")
    print(f"配速 5分钟/公里 = {convert_speed(1/5, 'km/h', 'm/s') * 3600 / 5:.2f} km/h")
    
    print("\n" + "="*60)
    print("  示例演示完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()