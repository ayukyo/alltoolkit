"""
geo_utils 使用示例

演示地理坐标工具模块的各项功能
"""

import sys
sys.path.insert(0, '..')

from mod import (
    haversine_distance,
    calculate_bearing,
    bearing_to_compass,
    destination_point,
    get_bounding_box,
    is_point_in_bounding_box,
    midpoint,
    interpolate_points,
    dms_to_decimal,
    decimal_to_dms,
    format_coordinates,
    find_nearest_point,
    calculate_area,
    GeoPoint,
    get_city_coordinates,
    distance_between_cities,
    CITY_COORDINATES,
)


def example_basic_distance():
    """示例1: 基础距离计算"""
    print("=" * 60)
    print("示例1: 基础距离计算")
    print("=" * 60)
    
    # 北京坐标
    beijing_lat, beijing_lon = 39.9042, 116.4074
    # 上海坐标
    shanghai_lat, shanghai_lon = 31.2304, 121.4737
    
    # 计算距离（默认公里）
    distance_km = haversine_distance(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon)
    print(f"北京到上海的距离: {distance_km:.2f} 公里")
    
    # 计算距离（米）
    distance_m = haversine_distance(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon, "m")
    print(f"北京到上海的距离: {distance_m:.0f} 米")
    
    # 计算距离（英里）
    distance_mi = haversine_distance(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon, "mi")
    print(f"北京到上海的距离: {distance_mi:.2f} 英里")
    
    print()


def example_bearing():
    """示例2: 方位角计算"""
    print("=" * 60)
    print("示例2: 方位角计算")
    print("=" * 60)
    
    beijing_lat, beijing_lon = 39.9042, 116.4074
    shanghai_lat, shanghai_lon = 31.2304, 121.4737
    
    # 计算方位角
    bearing = calculate_bearing(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon)
    compass = bearing_to_compass(bearing)
    
    print(f"北京到上海的方位角: {bearing:.1f}° ({compass})")
    
    # 计算到广州的方位角
    guangzhou_lat, guangzhou_lon = 23.1291, 113.2644
    bearing_gz = calculate_bearing(beijing_lat, beijing_lon, guangzhou_lat, guangzhou_lon)
    compass_gz = bearing_to_compass(bearing_gz)
    
    print(f"北京到广州的方位角: {bearing_gz:.1f}° ({compass_gz})")
    print()


def example_destination():
    """示例3: 目标点计算"""
    print("=" * 60)
    print("示例3: 目标点计算")
    print("=" * 60)
    
    # 从北京出发
    beijing_lat, beijing_lon = 39.9042, 116.4074
    
    # 向正北方向移动100公里
    dest_north = destination_point(beijing_lat, beijing_lon, 0, 100, "km")
    print(f"从北京向北100公里到达: ({dest_north[0]:.4f}, {dest_north[1]:.4f})")
    
    # 向东南方向移动500公里
    dest_se = destination_point(beijing_lat, beijing_lon, 135, 500, "km")
    print(f"从北京向东南500公里到达: ({dest_se[0]:.4f}, {dest_se[1]:.4f})")
    
    # 格式化显示
    print(f"格式化坐标: {format_coordinates(dest_se[0], dest_se[1], 'dms')}")
    print()


def example_bounding_box():
    """示例4: 边界框计算"""
    print("=" * 60)
    print("示例4: 边界框计算")
    print("=" * 60)
    
    # 以天安门为中心，10公里为半径
    tiananmen_lat, tiananmen_lon = 39.9087, 116.3975
    
    bbox = get_bounding_box(tiananmen_lat, tiananmen_lon, 10, "km")
    print(f"天安门周围10公里边界框:")
    print(f"  最小纬度: {bbox['min_lat']:.4f}")
    print(f"  最大纬度: {bbox['max_lat']:.4f}")
    print(f"  最小经度: {bbox['min_lon']:.4f}")
    print(f"  最大经度: {bbox['max_lon']:.4f}")
    
    # 检查点是否在边界框内
    test_point = (39.91, 116.40)
    is_inside = is_point_in_bounding_box(test_point[0], test_point[1], bbox)
    print(f"\n点 {test_point} 是否在边界框内: {is_inside}")
    
    outside_point = (40.0, 116.40)
    is_outside = is_point_in_bounding_box(outside_point[0], outside_point[1], bbox)
    print(f"点 {outside_point} 是否在边界框内: {is_outside}")
    print()


def example_midpoint():
    """示例5: 中点计算"""
    print("=" * 60)
    print("示例5: 中点计算")
    print("=" * 60)
    
    beijing_lat, beijing_lon = 39.9042, 116.4074
    shanghai_lat, shanghai_lon = 31.2304, 121.4737
    
    # 计算北京和上海的中点
    mid_lat, mid_lon = midpoint(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon)
    print(f"北京到上海的中点坐标: ({mid_lat:.4f}, {mid_lon:.4f})")
    print(f"格式化显示: {format_coordinates(mid_lat, mid_lon, 'dms')}")
    
    # 验证中点距离
    dist_to_beijing = haversine_distance(mid_lat, mid_lon, beijing_lat, beijing_lon)
    dist_to_shanghai = haversine_distance(mid_lat, mid_lon, shanghai_lat, shanghai_lon)
    print(f"中点到北京的距离: {dist_to_beijing:.2f} 公里")
    print(f"中点到上海的距离: {dist_to_shanghai:.2f} 公里")
    print()


def example_interpolation():
    """示例6: 路径插值"""
    print("=" * 60)
    print("示例6: 路径插值")
    print("=" * 60)
    
    beijing_lat, beijing_lon = 39.9042, 116.4074
    shanghai_lat, shanghai_lon = 31.2304, 121.4737
    
    # 在北京和上海之间插值生成5个点
    points = interpolate_points(beijing_lat, beijing_lon, shanghai_lat, shanghai_lon, 5)
    
    print("从北京到上海的路径插值点:")
    for i, (lat, lon) in enumerate(points):
        print(f"  点{i+1}: ({lat:.4f}, {lon:.4f})")
    print()


def example_coordinate_conversion():
    """示例7: 坐标格式转换"""
    print("=" * 60)
    print("示例7: 坐标格式转换")
    print("=" * 60)
    
    # 十进制转度分秒
    lat, lon = 39.9042, 116.4074
    lat_dms = decimal_to_dms(lat, True)
    lon_dms = decimal_to_dms(lon, False)
    
    print(f"十进制坐标: ({lat}, {lon})")
    print(f"度分秒格式: {lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.2f}\"{lat_dms[3]}, {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.2f}\"{lon_dms[3]}")
    
    # 度分秒转十进制
    decimal_lat = dms_to_decimal(39, 54, 15.12, 'N')
    decimal_lon = dms_to_decimal(116, 24, 26.64, 'E')
    
    print(f"\n度分秒: 39°54'15.12\"N, 116°24'26.64\"E")
    print(f"十进制: ({decimal_lat:.4f}, {decimal_lon:.4f})")
    
    # 格式化显示
    print(f"\n格式化显示（十进制）: {format_coordinates(lat, lon, 'decimal')}")
    print(f"格式化显示（度分秒）: {format_coordinates(lat, lon, 'dms')}")
    print()


def example_find_nearest():
    """示例8: 最近点查找"""
    print("=" * 60)
    print("示例8: 最近点查找")
    print("=" * 60)
    
    # 北京坐标
    beijing_lat, beijing_lon = 39.9042, 116.4074
    
    # 中国主要城市
    cities = [
        (31.2304, 121.4737),  # 上海
        (23.1291, 113.2644),   # 广州
        (22.5431, 114.0579),   # 深圳
        (30.2741, 120.1551),   # 杭州
        (30.5728, 104.0668),   # 成都
        (30.5928, 114.3052),   # 武汉
    ]
    city_names = ["上海", "广州", "深圳", "杭州", "成都", "武汉"]
    
    idx, nearest_point, distance = find_nearest_point(beijing_lat, beijing_lon, cities)
    
    print(f"从北京出发，最近的城市是: {city_names[idx]}")
    print(f"坐标: ({nearest_point[0]:.4f}, {nearest_point[1]:.4f})")
    print(f"距离: {distance:.2f} 公里")
    
    # 按距离排序所有城市
    print("\n各城市到北京的距离:")
    distances = []
    for i, (city, name) in enumerate(zip(cities, city_names)):
        dist = haversine_distance(beijing_lat, beijing_lon, city[0], city[1])
        distances.append((name, dist))
    
    distances.sort(key=lambda x: x[1])
    for name, dist in distances:
        print(f"  {name}: {dist:.2f} 公里")
    print()


def example_area_calculation():
    """示例9: 面积计算"""
    print("=" * 60)
    print("示例9: 面积计算")
    print("=" * 60)
    
    # 北京市中心大致区域（简化的矩形）
    polygon = [
        (39.95, 116.35),  # 西北
        (39.95, 116.45),  # 东北
        (39.85, 116.45),  # 东南
        (39.85, 116.35),  # 西南
    ]
    
    area_km2 = calculate_area(polygon, "km2")
    area_m2 = calculate_area(polygon, "m2")
    
    print(f"北京市中心区域面积约: {area_km2:.2f} 平方公里")
    print(f"北京市中心区域面积约: {area_m2:.0f} 平方米")
    print()


def example_geo_point_class():
    """示例10: GeoPoint 类使用"""
    print("=" * 60)
    print("示例10: GeoPoint 类使用")
    print("=" * 60)
    
    # 创建地理点
    beijing = GeoPoint(39.9042, 116.4074, "北京")
    shanghai = GeoPoint(31.2304, 121.4737, "上海")
    
    print(f"创建点: {beijing}")
    print(f"创建点: {shanghai}")
    
    # 计算距离
    distance = beijing.distance_to(shanghai)
    print(f"\n{beijing.name} 到 {shanghai.name} 的距离: {distance:.2f} 公里")
    
    # 计算方位角
    bearing = beijing.bearing_to(shanghai)
    compass = bearing_to_compass(bearing)
    print(f"{beijing.name} 到 {shanghai.name} 的方位角: {bearing:.1f}° ({compass})")
    
    # 计算中点
    mid = beijing.midpoint_to(shanghai)
    print(f"\n中点坐标: ({mid.lat:.4f}, {mid.lon:.4f})")
    
    # 计算目标点
    destination = beijing.destination(180, 500, "km")  # 向南500公里
    print(f"\n从{beijing.name}向南500公里到达: ({destination.lat:.4f}, {destination.lon:.4f})")
    
    # 度分秒格式
    lat_dms, lon_dms = beijing.to_dms()
    print(f"\n{beijing.name}的度分秒坐标: {lat_dms}, {lon_dms}")
    print()


def example_city_coordinates():
    """示例11: 城市坐标库"""
    print("=" * 60)
    print("示例11: 城市坐标库")
    print("=" * 60)
    
    # 获取城市坐标
    print("内置城市坐标:")
    for city in ["北京", "上海", "东京", "纽约", "伦敦", "巴黎"]:
        coords = get_city_coordinates(city)
        if coords:
            print(f"  {city}: ({coords[0]:.4f}, {coords[1]:.4f})")
    
    # 计算城市间距离
    print("\n城市间距离:")
    routes = [
        ("北京", "上海"),
        ("北京", "东京"),
        ("伦敦", "巴黎"),
        ("纽约", "洛杉矶"),
    ]
    
    for city1, city2 in routes:
        distance = distance_between_cities(city1, city2)
        if distance:
            print(f"  {city1} 到 {city2}: {distance:.2f} 公里")
    
    print(f"\n内置城市总数: {len(CITY_COORDINATES)} 个")
    print()


def example_travel_route():
    """示例12: 旅行路线规划"""
    print("=" * 60)
    print("示例12: 旅行路线规划")
    print("=" * 60)
    
    # 计划一条中国城市旅行路线
    cities = ["北京", "西安", "成都", "重庆", "武汉", "南京", "上海"]
    
    total_distance = 0
    print("旅行路线:")
    for i in range(len(cities) - 1):
        city1 = cities[i]
        city2 = cities[i + 1]
        distance = distance_between_cities(city1, city2)
        if distance:
            bearing = calculate_bearing(*get_city_coordinates(city1), *get_city_coordinates(city2))
            compass = bearing_to_compass(bearing)
            total_distance += distance
            print(f"  {city1} → {city2}: {distance:.0f}公里 ({compass}方向)")
    
    print(f"\n总路程: {total_distance:.0f} 公里")
    print()


if __name__ == "__main__":
    example_basic_distance()
    example_bearing()
    example_destination()
    example_bounding_box()
    example_midpoint()
    example_interpolation()
    example_coordinate_conversion()
    example_find_nearest()
    example_area_calculation()
    example_geo_point_class()
    example_city_coordinates()
    example_travel_route()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)