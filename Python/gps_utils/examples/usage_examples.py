"""
GPS Utilities 使用示例

展示各种 GPS/地理位置处理功能的使用方法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Coordinate, BoundingBox,
    distance_between, bearing_to, midpoint_of, destination_from,
    create_bbox, dd_to_dms, dms_to_dd, format_gps,
    parse_gps, GPSParser, GPSValidator, GPSFormatter,
    total_track_distance, maps_url, get_region, is_in_region,
    create_coordinate, GPSConverter, GPSCalculator,
)


def example_distance_calculation():
    """示例：距离计算"""
    print("=== 距离计算示例 ===")
    
    # 定义城市坐标
    cities = {
        '北京': (39.9042, 116.4074),
        '上海': (31.2304, 121.4737),
        '广州': (23.1291, 113.2644),
        '成都': (30.5728, 104.0668),
        '纽约': (40.7128, -74.0060),
        '伦敦': (51.5074, -0.1278),
    }
    
    # 计算北京到其他城市的距离
    beijing = cities['北京']
    print(f"\n从北京出发的距离：")
    
    for name, coord in cities.items():
        if name == '北京':
            continue
        
        dist = distance_between(beijing[0], beijing[1], coord[0], coord[1])
        bearing = bearing_to(beijing[0], beijing[1], coord[0], coord[1])
        
        # 格式化距离
        if dist < 1000:
            dist_str = f"{dist:.1f} km"
        else:
            dist_str = f"{dist:.0f} km ({dist/1000:.2f}千公里)"
        
        print(f"  -> {name}: {dist_str}, 方位 {bearing:.1f}°")
    
    # 使用不同单位
    print(f"\n北京-上海距离（不同单位）：")
    dist_km = distance_between(beijing[0], beijing[1], 
                               cities['上海'][0], cities['上海'][1], 'km')
    dist_mi = distance_between(beijing[0], beijing[1],
                               cities['上海'][0], cities['上海'][1], 'mi')
    dist_nm = distance_between(beijing[0], beijing[1],
                               cities['上海'][0], cities['上海'][1], 'nm')
    
    print(f"  公里: {dist_km:.1f} km")
    print(f"  英里: {dist_mi:.1f} mi")
    print(f"  海里: {dist_nm:.1f} nm")


def example_coordinate_conversion():
    """示例：坐标格式转换"""
    print("\n=== 坐标格式转换示例 ===")
    
    lat = 39.9042  # 北京纬度
    lon = 116.4074  # 北京经度
    
    # 十进制度 (DD)
    print(f"\n十进制度 (DD):")
    print(f"  纬度: {lat}°")
    print(f"  经度: {lon}°")
    
    # 度分秒 (DMS)
    print(f"\n度分秒 (DMS):")
    lat_dms = dd_to_dms(lat, is_latitude=True)
    lon_dms = dd_to_dms(lon, is_latitude=False)
    
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'
    
    print(f"  纬度: {lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.2f}\"{lat_dir}")
    print(f"  经度: {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.2f}\"{lon_dir}")
    
    # 度分 (DDM)
    print(f"\n度分 (DDM):")
    lat_ddm = GPSConverter.dd_to_ddm(lat)
    lon_ddm = GPSConverter.dd_to_ddm(lon)
    
    print(f"  纬度: {lat_ddm[0]}°{lat_ddm[1]:.4f}'{lat_dir}")
    print(f"  经度: {lon_ddm[0]}°{lon_ddm[1]:.4f}'{lon_dir}")
    
    # NMEA 格式
    print(f"\nNMEA 格式:")
    nMEA = GPSFormatter.format_nMEA(lat, lon)
    print(f"  {nMEA}")
    
    # UTM 格式
    print(f"\nUTM 格式:")
    utm = GPSConverter.dd_to_utm(lat, lon)
    print(f"  Zone: {utm.zone}{utm.hemisphere}")
    print(f"  Easting: {utm.easting:.2f} m")
    print(f"  Northing: {utm.northing:.2f} m")
    
    # 使用便捷格式化函数
    print(f"\n一键格式化:")
    print(f"  DMS: {format_gps(lat, lon, 'dms')}")
    print(f"  DDM: {format_gps(lat, lon, 'ddm')}")
    print(f"  DD: {format_gps(lat, lon, 'dd', precision=6)}")


def example_coordinate_object():
    """示例：坐标对象"""
    print("\n=== 坐标对象示例 ===")
    
    # 创建坐标
    coord = create_coordinate(39.9042, 116.4074, altitude=50)
    
    print(f"\n基本信息:")
    print(f"  纬度: {coord.latitude}")
    print(f"  经度: {coord.longitude}")
    print(f"  高度: {coord.altitude} m")
    
    print(f"\n位置属性:")
    print(f"  北半球: {coord.is_north}")
    print(f"  东半球: {coord.is_east}")
    print(f"  半球: {coord.hemisphere}")
    
    print(f"\n转换方法:")
    print(f"  DMS: {coord.to_dms()}")
    print(f"  DDM: {coord.to_ddm()}")
    print(f"  Dict: {coord.to_dict()}")


def example_navigation():
    """示例：导航计算"""
    print("\n=== 导航计算示例 ===")
    
    # 起点：北京
    start = (39.9042, 116.4074)
    
    # 目标：向东飞行 500km
    bearing = 90  # 正东
    distance = 500  # km
    
    # 计算终点
    dest = destination_from(start[0], start[1], bearing, distance)
    
    print(f"\n导航计划:")
    print(f"  起点: {start[0]:.4f}°, {start[1]:.4f}°")
    print(f"  方位: {bearing}° (正东)")
    print(f"  距离: {distance} km")
    print(f"  终点: {dest[0]:.4f}°, {dest[1]:.4f}°")
    
    # 验证计算
    actual_dist = distance_between(start[0], start[1], dest[0], dest[1])
    actual_bearing = bearing_to(start[0], start[1], dest[0], dest[1])
    
    print(f"\n验证:")
    print(f"  实际距离: {actual_dist:.1f} km")
    print(f"  实际方位: {actual_bearing:.1f}°")
    
    # 计算中间点
    mid = midpoint_of(start[0], start[1], dest[0], dest[1])
    print(f"\n中间点: {mid[0]:.4f}°, {mid[1]:.4f}°")


def example_boundary_box():
    """示例：边界框"""
    print("\n=== 边界框示例 ===")
    
    # 以北京为中心，创建不同半径的边界框
    center = (39.9042, 116.4074)
    
    radii = [1, 5, 10, 50]
    
    print(f"\n中心点: {center[0]:.4f}°, {center[1]:.4f}°")
    print(f"\n边界框:")
    
    for radius in radii:
        bbox = create_bbox(center[0], center[1], radius)
        
        print(f"\n  {radius}km 边界框:")
        print(f"    纬度: {bbox.min_lat:.4f} - {bbox.max_lat:.4f}")
        print(f"    经度: {bbox.min_lon:.4f} - {bbox.max_lon:.4f}")
        print(f"    宽度: {bbox.width_km():.1f} km")
        print(f"    高度: {bbox.height_km():.1f} km")
    
    # 检查点是否在边界框内
    print(f"\n包含检测:")
    bbox_10 = create_bbox(center[0], center[1], 10)
    
    test_points = [
        ("北京中心", create_coordinate(39.9042, 116.4074)),
        ("近郊", create_coordinate(39.95, 116.45)),
        ("远处", create_coordinate(40.5, 117.5)),
    ]
    
    for name, point in test_points:
        inside = bbox_10.contains(point)
        print(f"  {name}: {'在范围内' if inside else '超出范围'}")


def example_coordinate_parsing():
    """示例：坐标解析"""
    print("\n=== 坐标解析示例 ===")
    
    # 多种格式测试
    test_strings = [
        "39°54'15\"N",        # 度分秒
        "N 39° 54' 15\"",     # 度分秒（前置方向）
        "39°54.25'N",         # 度分
        "39.9042°N",          # 十进制度
        "3954.2500,N",        # NMEA 格式
        "45.5",               # 纯数字
    ]
    
    print(f"\n解析各种格式:")
    
    for s in test_strings:
        try:
            value, direction = parse_gps(s)
            print(f"  '{s}' -> {value:.4f}° ({direction or '无方向'})")
        except ValueError as e:
            print(f"  '{s}' -> 解析失败: {e}")
    
    # 解析坐标对
    print(f"\n解析坐标对:")
    pairs = [
        "39.9042, 116.4074",
        "39.9042 116.4074",
    ]
    
    for p in pairs:
        coord = GPSParser.parse_coordinate_pair(p)
        print(f"  '{p}' -> ({coord.latitude:.4f}, {coord.longitude:.4f})")
    
    # 解析 GeoJSON
    print(f"\n解析 GeoJSON:")
    geojson_point = {
        'type': 'Point',
        'coordinates': [116.4074, 39.9042]
    }
    
    coords = GPSParser.parse_geojson(geojson_point)
    print(f"  Point: {coords[0].latitude:.4f}°, {coords[0].longitude:.4f}°")


def example_validation():
    """示例：坐标验证"""
    print("\n=== 坐标验证示例 ===")
    
    # 验证坐标范围
    test_coords = [
        ("正常", 39.9042, 116.4074),
        ("纬度超限", 100, 116.4074),
        ("经度超限", 39.9042, 200),
        ("极点附近", 85, 0),
        ("日期线附近", 0, 170),
    ]
    
    print(f"\n坐标验证:")
    
    for name, lat, lon in test_coords:
        valid, msg = GPSValidator.validate_coordinate(lat, lon)
        
        if valid:
            near_pole = GPSValidator.is_near_pole(lat)
            near_dateline = GPSValidator.is_near_dateline(lon)
            
            extras = []
            if near_pole:
                extras.append("靠近极点")
            if near_dateline:
                extras.append("靠近日期线")
            
            extra_str = f" ({', '.join(extras)})" if extras else ""
            print(f"  {name}: 有效{extra_str}")
        else:
            print(f"  {name}: 无效 - {msg}")
    
    # 区域检测
    print(f"\n区域检测:")
    
    test_locations = [
        ("北京", 39.9042, 116.4074),
        ("纽约", 40.7128, -74.0060),
        ("伦敦", 51.5074, -0.1278),
        ("悉尼", -33.8688, 151.2093),
        ("南极点", -90, 0),
    ]
    
    for name, lat, lon in test_locations:
        region = get_region(lat, lon)
        in_china = is_in_region(lat, lon, 'china')
        
        print(f"  {name}: 区域={region or '未知'}, 在中国={in_china}")


def example_track_processing():
    """示例：轨迹处理"""
    print("\n=== 轨迹处理示例 ===")
    
    # 北京 -> 济南 -> 上海 路线
    track = [
        (39.9042, 116.4074),  # 北京
        (36.6512, 117.1201),  # 济南
        (35.0, 117.0),        # 泰安附近
        (31.2304, 121.4737),  # 上海
    ]
    
    print(f"\n路线点:")
    for i, point in enumerate(track):
        print(f"  {i+1}. {point[0]:.4f}°, {point[1]:.4f}°")
    
    # 计算总距离
    total = total_track_distance(track)
    print(f"\n总距离: {total:.1f} km")
    
    # 计算各段距离
    print(f"\n各段距离:")
    segment_names = ["北京-济南", "济南-泰安", "泰安-上海"]
    
    for i, name in enumerate(segment_names):
        seg_dist = distance_between(track[i][0], track[i][1],
                                   track[i+1][0], track[i+1][1])
        bearing = bearing_to(track[i][0], track[i][1],
                            track[i+1][0], track[i+1][1])
        
        print(f"  {name}: {seg_dist:.1f} km, 方位 {bearing:.1f}°")


def example_map_urls():
    """示例：地图 URL"""
    print("\n=== 地图 URL 示例 ===")
    
    lat, lon = 39.9042, 116.4074
    
    # 各平台 URL
    print(f"\n坐标: {lat:.4f}°, {lon:.4f}°")
    
    print(f"\n地图链接:")
    print(f"  Google Maps: {maps_url(lat, lon, 'google')}")
    print(f"  OpenStreetMap: {maps_url(lat, lon, 'osm')}")
    print(f"  百度地图: {maps_url(lat, lon, 'baidu')}")
    
    # GeoJSON 输出
    print(f"\nGeoJSON 格式:")
    
    point = GPSFormatter.format_geojson_point(lat, lon)
    print(f"  Point: {point}")
    
    line_coords = [(39.9, 116.4), (31.2, 121.5)]
    line = GPSFormatter.format_geojson_line(line_coords)
    print(f"  LineString: {line}")


def example_advanced_calculations():
    """示例：高级计算"""
    print("\n=== 高级计算示例 ===")
    
    # 垂直距离计算
    print(f"\n垂直距离计算:")
    
    # 定义一条线段（北京 -> 上海）
    p1 = (39.9042, 116.4074)
    p2 = (31.2304, 121.4737)
    
    # 测试点（济南）
    p3 = (36.6512, 117.1201)
    
    cross_dist = GPSCalculator.cross_track_distance(
        p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
    )
    
    along_dist = GPSCalculator.along_track_distance(
        p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
    )
    
    print(f"  线段: 北京 -> 上海")
    print(f"  测试点: 济南")
    print(f"  垂直距离: {cross_dist:.1f} km")
    print(f"  沿线距离: {along_dist:.1f} km")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("GPS Utilities 使用示例")
    print("=" * 60)
    
    example_distance_calculation()
    example_coordinate_conversion()
    example_coordinate_object()
    example_navigation()
    example_boundary_box()
    example_coordinate_parsing()
    example_validation()
    example_track_processing()
    example_map_urls()
    example_advanced_calculations()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()