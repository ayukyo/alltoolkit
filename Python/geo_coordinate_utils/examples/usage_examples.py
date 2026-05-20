"""
地理坐标工具模块 - 使用示例

本示例演示如何使用 geo_coordinate_utils 模块进行：
1. 坐标格式转换
2. 距离和方位计算
3. 边界框计算
4. 坐标查找和筛选
5. GeoJSON输出
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Coordinate,
    BoundingBox,
    decimal_to_dms,
    dms_to_decimal,
    parse_coordinate,
    haversine_distance,
    bearing,
    bearing_to_direction,
    destination_point,
    bounding_box,
    midpoint,
    total_distance,
    find_nearest,
    coordinates_within_radius,
    format_coordinate,
    to_geojson,
)


def example_1_format_conversion():
    """示例1: 坐标格式转换"""
    print("\n" + "=" * 60)
    print("示例1: 坐标格式转换")
    print("=" * 60)
    
    # 十进制转DMS
    print("\n--- 十进制转DMS ---")
    coords = [
        (39.9042, "北京天安门"),
        (31.2304, "上海外滩"),
        (48.8566, "巴黎埃菲尔铁塔"),
        (-33.8568, "悉尼歌剧院"),
    ]
    
    for lat, name in coords:
        dms = decimal_to_dms(lat, is_latitude=True)
        print(f"  {name}: {lat}° → {dms}")
    
    # DMS转十进制
    print("\n--- DMS转十进制 ---")
    dms_list = [
        ("39°54'15\"N", "北京天安门"),
        ("31°13'49\"N", "上海外滩"),
        ("48°51'24\"N", "巴黎埃菲尔铁塔"),
        ("33°51'24\"S", "悉尼歌剧院"),
    ]
    
    for dms, name in dms_list:
        decimal = dms_to_decimal(dms)
        print(f"  {name}: {dms} → {decimal:.6f}°")
    
    # 使用Coordinate类
    print("\n--- Coordinate类 ---")
    coord = Coordinate(39.9042, 116.4074)
    print(f"  创建坐标: {coord}")
    lat_dms, lon_dms = coord.to_dms()
    print(f"  DMS格式: {lat_dms}, {lon_dms}")
    print(f"  是否有效: {coord.is_valid}")
    
    # 解析多种格式
    print("\n--- 解析多种格式 ---")
    examples = [
        ("39.9042", "116.4074"),
        ("39°54'15\"N", "116°24'26\"E"),
        ("N39.9042", "E116.4074"),
    ]
    
    for lat_str, lon_str in examples:
        coord = parse_coordinate(lat_str, lon_str)
        print(f"  '{lat_str}', '{lon_str}' → {coord}")


def example_2_distance_calculation():
    """示例2: 距离计算"""
    print("\n" + "=" * 60)
    print("示例2: 距离计算")
    print("=" * 60)
    
    # 定义城市坐标
    cities = {
        "北京": Coordinate(39.9042, 116.4074),
        "上海": Coordinate(31.2304, 121.4737),
        "广州": Coordinate(23.1291, 113.2644),
        "深圳": Coordinate(22.5431, 114.0579),
        "成都": Coordinate(30.5728, 104.0668),
        "西安": Coordinate(34.3416, 108.9398),
        "纽约": Coordinate(40.7128, -74.0060),
        "伦敦": Coordinate(51.5074, -0.1278),
        "东京": Coordinate(35.6762, 139.6503),
    }
    
    print("\n--- 城市间距离 ---")
    distances = [
        ("北京", "上海"),
        ("北京", "广州"),
        ("上海", "深圳"),
        ("北京", "纽约"),
        ("伦敦", "东京"),
    ]
    
    for city1, city2 in distances:
        coord1 = cities[city1]
        coord2 = cities[city2]
        dist = haversine_distance(coord1, coord2)
        dist_mile = haversine_distance(coord1, coord2, "mile")
        print(f"  {city1} → {city2}: {dist:.2f} km ({dist_mile:.2f} miles)")
    
    # 路径总距离
    print("\n--- 旅行路径总距离 ---")
    route = [cities["北京"], cities["西安"], cities["成都"], cities["广州"]]
    total = total_distance(route)
    print(f"  北京 → 西安 → 成都 → 广州")
    print(f"  总距离: {total:.2f} km")


def example_3_bearing_calculation():
    """示例3: 方位角计算"""
    print("\n" + "=" * 60)
    print("示例3: 方位角计算")
    print("=" * 60)
    
    # 北京到各城市的方位
    beijing = Coordinate(39.9042, 116.4074)
    targets = {
        "上海": Coordinate(31.2304, 121.4737),
        "广州": Coordinate(23.1291, 113.2644),
        "成都": Coordinate(30.5728, 104.0668),
        "西安": Coordinate(34.3416, 108.9398),
        "哈尔滨": Coordinate(45.8038, 126.5350),
        "乌鲁木齐": Coordinate(43.8256, 87.6168),
    }
    
    print("\n从北京出发到各城市的方位:")
    for name, coord in targets.items():
        brng = bearing(beijing, coord)
        direction = bearing_to_direction(brng)
        dist = haversine_distance(beijing, coord)
        print(f"  {name}: {brng:.1f}° ({direction}) - 距离 {dist:.0f} km")
    
    # 根据方位和距离计算终点
    print("\n--- 根据方位计算终点 ---")
    print(f"  起点: 北京 {beijing}")
    
    directions = [
        (100, 0, "正北100km"),
        (100, 90, "正东100km"),
        (100, 180, "正南100km"),
        (100, 270, "正西100km"),
        (500, 45, "东北500km"),
    ]
    
    for dist, brng, desc in directions:
        dest = destination_point(beijing, dist, brng)
        print(f"  {desc}: {dest}")


def example_4_bounding_box():
    """示例4: 边界框计算"""
    print("\n" + "=" * 60)
    print("示例4: 边界框计算")
    print("=" * 60)
    
    # 计算北京周边10公里的边界框
    beijing = Coordinate(39.9042, 116.4074)
    bbox = bounding_box(beijing, 10)
    
    print(f"\n北京市中心: {beijing}")
    print(f"半径10公里边界框:")
    print(f"  纬度范围: {bbox.min_lat:.6f}° ~ {bbox.max_lat:.6f}°")
    print(f"  经度范围: {bbox.min_lon:.6f}° ~ {bbox.max_lon:.6f}°")
    
    # 测试点是否在范围内
    print("\n点是否在范围内:")
    test_points = [
        Coordinate(39.91, 116.41),   # 约2km内
        Coordinate(39.95, 116.45),   # 约7km内
        Coordinate(40.0, 116.5),     # 约15km外
    ]
    
    for point in test_points:
        inside = bbox.contains(point)
        status = "✓ 在范围内" if inside else "✗ 在范围外"
        print(f"  {point}: {status}")


def example_5_find_nearest():
    """示例5: 查找最近点"""
    print("\n" + "=" * 60)
    print("示例5: 查找最近点")
    print("=" * 60)
    
    # 用户当前位置
    user_location = Coordinate(39.9, 116.4)
    
    # 周边城市
    nearby_cities = [
        Coordinate(40.0, 116.5),    # 最近
        Coordinate(39.8, 116.3),    # 第二近
        Coordinate(40.2, 117.0),    # 较远
        Coordinate(39.5, 115.8),    # 更远
    ]
    
    nearest, dist, idx = find_nearest(user_location, nearby_cities)
    
    print(f"用户位置: {user_location}")
    print(f"最近的城市距离: {dist:.2f} km")
    print(f"最近城市坐标: {nearest} (索引 {idx})")
    
    # 查找半径内的所有点
    print("\n--- 半径20公里内的城市 ---")
    within = coordinates_within_radius(user_location, nearby_cities, 20)
    
    for coord, dist in within:
        print(f"  {coord} - {dist:.2f} km")


def example_6_geojson_output():
    """示例6: GeoJSON输出"""
    print("\n" + "=" * 60)
    print("示例6: GeoJSON输出")
    print("=" * 60)
    
    # 创建一组城市坐标
    cities = [
        Coordinate(39.9042, 116.4074),  # 北京
        Coordinate(31.2304, 121.4737),  # 上海
        Coordinate(23.1291, 113.2644),  # 广州
    ]
    
    # 转换为GeoJSON
    geojson = to_geojson(cities)
    
    print("\nGeoJSON FeatureCollection:")
    import json
    print(json.dumps(geojson, indent=2, ensure_ascii=False))
    
    # 格式化输出示例
    print("\n--- 坐标格式化输出 ---")
    for i, coord in enumerate(cities):
        print(f"\n城市 {i+1}:")
        print(f"  十进制: {format_coordinate(coord, 'decimal')}")
        print(f"  DMS: {format_coordinate(coord, 'dms')}")
        print(f"  GeoJSON: {format_coordinate(coord, 'geojson')}")


def example_7_practical_scenario():
    """示例7: 实际应用场景"""
    print("\n" + "=" * 60)
    print("示例7: 实际应用场景 - 附近门店搜索")
    print("=" * 60)
    
    # 用户位置
    user = Coordinate(39.9042, 116.4074)
    print(f"用户位置: {user}")
    
    # 门店列表（名称和坐标）
    stores = [
        ("朝阳店", Coordinate(39.92, 116.46)),
        ("海淀店", Coordinate(39.98, 116.30)),
        ("东城店", Coordinate(39.93, 116.42)),
        ("西城店", Coordinate(39.91, 116.36)),
        ("通州店", Coordinate(39.88, 116.66)),
    ]
    
    # 搜索半径
    radius = 15  # 15公里
    
    print(f"\n搜索半径: {radius} km")
    
    # 计算每个门店的距离和方位
    print("\n所有门店信息:")
    for name, coord in stores:
        dist = haversine_distance(user, coord)
        brng = bearing(user, coord)
        direction = bearing_to_direction(brng)
        print(f"  {name}: {dist:.1f} km, 方位 {brng:.0f}° ({direction})")
    
    # 筛选范围内的门店
    coords = [c for _, c in stores]
    within = coordinates_within_radius(user, coords, radius)
    
    print(f"\n{radius}公里范围内的门店:")
    for coord, dist in within:
        # 找到对应的门店名
        for name, c in stores:
            if c.latitude == coord.latitude and c.longitude == coord.longitude:
                brng = bearing(user, coord)
                direction = bearing_to_direction(brng)
                print(f"  {name}: {dist:.1f} km, 在 {direction} 方向")
                break
    
    # 计算配送边界框
    bbox = bounding_box(user, radius)
    print(f"\n配送区域边界框:")
    print(f"  西南角: ({bbox.min_lat:.4f}, {bbox.min_lon:.4f})")
    print(f"  东北角: ({bbox.max_lat:.4f}, {bbox.max_lon:.4f})")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print(" 地理坐标工具模块 - 完整使用示例")
    print("=" * 60)
    
    example_1_format_conversion()
    example_2_distance_calculation()
    example_3_bearing_calculation()
    example_4_bounding_box()
    example_5_find_nearest()
    example_6_geojson_output()
    example_7_practical_scenario()
    
    print("\n" + "=" * 60)
    print(" 示例运行完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()