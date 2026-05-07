"""
Maidenhead Grid Locator Utils 使用示例

梅登黑德网格定位器（QTH Locator）是业余无线电常用的位置编码系统
"""

import sys
import os

# 添加模块目录到路径
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

# 直接从当前目录导入
import importlib.util
spec = importlib.util.spec_from_file_location("mod", os.path.join(module_dir, "mod.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

MaidenheadUtils = mod.MaidenheadUtils
maidenhead = mod.maidenhead
validate_locator = mod.validate_locator
latlon_to_locator = mod.latlon_to_locator
locator_to_latlon = mod.locator_to_latlon


def example_basic_conversion():
    """基本转换示例"""
    print("\n" + "="*60)
    print("基本转换示例")
    print("="*60)
    
    # 经纬度转定位器
    print("\n经纬度 → 定位器转换:")
    
    # 纽约市
    ny_lat, ny_lon = 40.7128, -74.0060
    ny_locator_4 = maidenhead.from_latlon(ny_lat, ny_lon, precision=4)
    ny_locator_6 = maidenhead.from_latlon(ny_lat, ny_lon, precision=6)
    ny_locator_8 = maidenhead.from_latlon(ny_lat, ny_lon, precision=8)
    print(f"  纽约市 ({ny_lat}, {ny_lon}):")
    print(f"    4字符: {ny_locator_4}")
    print(f"    6字符: {ny_locator_6}")
    print(f"    8字符: {ny_locator_8}")
    
    # 东京
    tk_lat, tk_lon = 35.6762, 139.6503
    tk_locator = maidenhead.from_latlon(tk_lat, tk_lon, precision=6)
    print(f"  东京 ({tk_lat}, {tk_lon}): {tk_locator}")
    
    # 伦敦
    ld_lat, ld_lon = 51.5074, -0.1278
    ld_locator = maidenhead.from_latlon(ld_lat, ld_lon, precision=6)
    print(f"  伦敦 ({ld_lat}, {ld_lon}): {ld_locator}")
    
    # 定位器转经纬度
    print("\n定位器 → 经纬度转换:")
    
    lat, lon = maidenhead.to_latlon('FN31pr')
    print(f"  FN31pr → ({lat:.6f}, {lon:.6f})")
    
    lat2, lon2 = maidenhead.to_latlon('QM68')
    print(f"  QM68 → ({lat2:.4f}, {lon2:.4f})")
    
    lat3, lon3 = maidenhead.to_latlon('IO91')
    print(f"  IO91 → ({lat3:.4f}, {lon3:.4f})")


def example_validation():
    """验证示例"""
    print("\n" + "="*60)
    print("验证示例")
    print("="*60)
    
    test_locators = ['FN', 'FN31', 'FN31pr', 'FN31praa', 
                     'invalid', 'FN3', 'SZ31', 'FN31yz']
    
    print("\n定位器验证:")
    for loc in test_locators:
        valid = maidenhead.validate(loc)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {loc:12} {status}")


def example_precision():
    """精度级别示例"""
    print("\n" + "="*60)
    print("精度级别示例")
    print("="*60)
    
    print("\n不同精度级别说明:")
    for precision in [2, 4, 6, 8, 10]:
        desc = maidenhead.precision_description(precision)
        print(f"  {precision}字符: {desc}")
    
    print("\n同一位置不同精度的定位器:")
    lat, lon = 40.5, -74.5
    
    for precision in [2, 4, 6, 8]:
        locator = maidenhead.from_latlon(lat, lon, precision)
        center = maidenhead.to_latlon(locator)
        bounds = maidenhead.get_bounds(locator)
        size = maidenhead.get_grid_size(locator)
        
        print(f"\n  精度 {precision}字符: {locator}")
        print(f"    中心点: ({center[0]:.6f}, {center[1]:.6f})")
        print(f"    边界: N={bounds['north']:.4f}, S={bounds['south']:.4f}")
        print(f"          E={bounds['east']:.4f}, W={bounds['west']:.4f}")
        print(f"    面积: {size['area_km2']:.4f} km²")


def example_distance():
    """距离计算示例"""
    print("\n" + "="*60)
    print("距离计算示例")
    print("="*60)
    
    # 计算不同城市之间的距离
    cities = {
        '纽约': 'FN31',
        '洛杉矶': 'DM',
        '伦敦': 'IO',
        '东京': 'QM',
        '悉尼': 'QF'
    }
    
    print("\n城市间距离 (公里):")
    
    pairs = [('纽约', '洛杉矶'), ('纽约', '伦敦'), ('伦敦', '东京'), 
             ('东京', '悉尼'), ('纽约', '悉尼')]
    
    for city1, city2 in pairs:
        loc1 = cities[city1]
        loc2 = cities[city2]
        dist = maidenhead.distance(loc1, loc2, 'km')
        bearing = maidenhead.bearing(loc1, loc2)
        print(f"  {city1} ({loc1}) → {city2} ({loc2}):")
        print(f"    距离: {dist:.2f} km ({dist/1.609:.2f} mi)")
        print(f"    方位角: {bearing:.2f}°")


def example_neighbors():
    """相邻网格示例"""
    print("\n" + "="*60)
    print("相邻网格示例")
    print("="*60)
    
    locator = 'FN31pr'
    
    print(f"\n{locator} 的相邻网格:")
    
    # 第一层邻域
    neighbors_l1 = maidenhead.neighbors(locator, level=1)
    print(f"  第一层邻域 ({len(neighbors_l1)}个):")
    print(f"    {', '.join(neighbors_l1[:8])}")
    
    # 第二层邻域
    neighbors_l2 = maidenhead.neighbors(locator, level=2)
    print(f"  第二层邻域 ({len(neighbors_l2)}个):")
    print(f"    {', '.join(neighbors_l2[:12])}...")


def example_path():
    """路径示例"""
    print("\n" + "="*60)
    print("路径示例")
    print("="*60)
    
    # 创建一条路径
    path = ['FN31', 'FN32', 'FN33', 'FN34', 'FN35']
    
    print("\n路径分析:")
    print(f"  路径: {path}")
    print(f"  长度: {maidenhead.path_length(path)} 点")
    print(f"  总距离: {maidenhead.path_distance(path):.2f} km")
    
    # 编码解码
    encoded = maidenhead.encode_path(path)
    decoded = maidenhead.decode_path(encoded)
    print(f"\n  编码: {encoded}")
    print(f"  解码: {decoded}")
    
    # 中间点
    print("\n路径中间点:")
    mid = maidenhead.intermediate_point('FN31', 'FN35', 0.5)
    print(f"  FN31 → FN35 的中点: {mid}")
    
    quarter = maidenhead.intermediate_point('FN31', 'FN35', 0.25)
    print(f"  FN31 → FN35 的1/4点: {quarter}")


def example_formatting():
    """格式化示例"""
    print("\n" + "="*60)
    print("格式化示例")
    print("="*60)
    
    locator = 'FN31pr'
    
    print(f"\n定位器 {locator} 的不同格式:")
    
    standard = maidenhead.format_location(locator, style='standard')
    print(f"  标准格式: {standard}")
    
    compact = maidenhead.format_location(locator, style='compact')
    print(f"  紧凑格式: {compact}")
    
    detailed = maidenhead.format_location(locator, style='detailed')
    print(f"  详细格式: {detailed}")


def example_ham_radio_use():
    """业余无线电应用示例"""
    print("\n" + "="*60)
    print("业余无线电应用示例")
    print("="*60)
    
    # 两个业余电台之间的距离
    station_a = 'FN31pr'  # 新泽西
    station_b = 'FN44'    # 新英格兰
    
    print("\n电台通信分析:")
    print(f"  电台A位置: {station_a}")
    print(f"  电台B位置: {station_b}")
    
    lat_a, lon_a = maidenhead.to_latlon(station_a)
    lat_b, lon_b = maidenhead.to_latlon(station_b)
    
    print(f"  电台A坐标: ({lat_a:.4f}, {lon_a:.4f})")
    print(f"  电台B坐标: ({lat_b:.4f}, {lon_b:.4f})")
    
    distance = maidenhead.distance(station_a, station_b)
    bearing = maidenhead.bearing(station_a, station_b)
    
    print(f"  通信距离: {distance:.2f} km")
    print(f"  通信方向: {bearing:.2f}°")
    
    # 方向描述
    directions = ['北', '东北', '东', '东南', '南', '西南', '西', '西北']
    dir_idx = int((bearing + 22.5) / 45) % 8
    print(f"  大致方向: {directions[dir_idx]}")


def example_grid_size_analysis():
    """网格大小分析示例"""
    print("\n" + "="*60)
    print("网格大小分析示例")
    print("="*60)
    
    print("\n各精度级别网格大小比较:")
    
    # 使用纽约附近的定位器
    locators = ['FN', 'FN31', 'FN31pr', 'FN31praa', 'FN31praaab']
    
    for loc in locators:
        if maidenhead.validate(loc):
            size = maidenhead.get_grid_size(loc)
            precision = maidenhead.precision_description(len(loc))
            print(f"\n  {loc} ({precision}):")
            print(f"    经度宽度: {size['lon_width_deg']:.8f}° = {size['lon_width_km']:.4f} km")
            print(f"    纬度高度: {size['lat_height_deg']:.8f}° = {size['lat_height_km']:.4f} km")
            print(f"    面积: {size['area_km2']:.6f} km² ({size['area_mi2']:.6f} mi²)")


def main():
    """运行所有示例"""
    print("="*60)
    print("Maidenhead Grid Locator Utils 使用示例")
    print("梅登黑德网格定位器（业余无线电QTH定位系统）")
    print("="*60)
    
    example_basic_conversion()
    example_validation()
    example_precision()
    example_distance()
    example_neighbors()
    example_path()
    example_formatting()
    example_ham_radio_use()
    example_grid_size_analysis()
    
    print("\n" + "="*60)
    print("示例完成！")
    print("="*60)


if __name__ == '__main__':
    main()