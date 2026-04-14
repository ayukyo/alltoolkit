"""
Geohash Utilities 使用示例

演示所有主要功能的使用方法。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode, decode, get_neighbors, distance, get_precision_info,
    get_common_precision, get_bounding_box, get_geohashes_in_bbox,
    is_valid, expand, midpoint, destination, bearing
)


def example_encode():
    """编码示例"""
    print("=" * 60)
    print("Geohash 编码示例")
    print("=" * 60)
    
    cities = [
        ("北京天安门", 39.9042, 116.4074),
        ("上海外滩", 31.2304, 121.4737),
        ("纽约时代广场", 40.7580, -73.9855),
        ("伦敦大本钟", 51.5007, -0.1246),
        ("东京塔", 35.6586, 139.7454),
        ("悉尼歌剧院", -33.8568, 151.2153),
    ]
    
    for name, lat, lng in cities:
        for precision in [4, 6, 8]:
            geohash = encode(lat, lng, precision)
            print(f"{name} (精度{precision}): {geohash}")
        print()


def example_decode():
    """解码示例"""
    print("=" * 60)
    print("Geohash 解码示例")
    print("=" * 60)
    
    geohashes = ['wx4g', 'wx4g0b', 'wx4g0b2x']
    
    for gh in geohashes:
        decoded = decode(gh)
        print(f"\nGeohash: {gh}")
        print(f"  中心点: ({decoded['lat']:.6f}, {decoded['lng']:.6f})")
        print(f"  边界框: [{decoded['lat_min']:.6f}, {decoded['lat_max']:.6f}] × [{decoded['lng_min']:.6f}, {decoded['lng_max']:.6f}]")
        print(f"  尺寸: {decoded['width_km']:.2f}km × {decoded['height_km']:.2f}km")


def example_neighbors():
    """相邻Geohash示例"""
    print("=" * 60)
    print("相邻 Geohash 示例")
    print("=" * 60)
    
    geohash = 'wx4g0b'
    neighbors = get_neighbors(geohash)
    
    print(f"\n中心: {geohash}")
    print(f"\n相邻Geohash:")
    print(f"    {neighbors['nw']}    {neighbors['n']}    {neighbors['ne']}")
    print(f"    {neighbors['w']}    {geohash}    {neighbors['e']}")
    print(f"    {neighbors['sw']}    {neighbors['s']}    {neighbors['se']}")


def example_distance():
    """距离计算示例"""
    print("=" * 60)
    print("距离计算示例")
    print("=" * 60)
    
    routes = [
        ("北京 → 上海", 39.9042, 116.4074, 31.2304, 121.4737),
        ("北京 → 纽约", 39.9042, 116.4074, 40.7128, -74.0060),
        ("北京 → 东京", 39.9042, 116.4074, 35.6762, 139.6503),
        ("伦敦 → 巴黎", 51.5074, -0.1278, 48.8566, 2.3522),
    ]
    
    for name, lat1, lng1, lat2, lng2 in routes:
        dist_km = distance(lat1, lng1, lat2, lng2, 'km')
        dist_mile = distance(lat1, lng1, lat2, lng2, 'mile')
        dist_nmi = distance(lat1, lng1, lat2, lng2, 'nmi')
        
        print(f"\n{name}:")
        print(f"  {dist_km:.1f} 公里")
        print(f"  {dist_mile:.1f} 英里")
        print(f"  {dist_nmi:.1f} 海里")


def example_precision():
    """精度信息示例"""
    print("=" * 60)
    print("精度信息示例")
    print("=" * 60)
    
    for precision in range(1, 13):
        info = get_precision_info(precision)
        print(f"精度{precision:2d}: {info['width_km']:8.3f}km × {info['height_km']:8.3f}km  |  {info['description']}")
    
    print("\n根据距离推荐精度:")
    for dist_km in [0.001, 0.01, 0.1, 1, 5, 10, 50, 100, 500, 1000]:
        precision = get_common_precision(dist_km)
        info = get_precision_info(precision)
        print(f"  {dist_km:6.1f}km 范围 → 精度{precision} ({info['width_km']:.2f}km)")


def example_bounding_box():
    """边界框示例"""
    print("=" * 60)
    print("边界框示例")
    print("=" * 60)
    
    # 以北京天安门为中心，10公里半径
    lat, lng = 39.9042, 116.4074
    radius_km = 10
    
    bbox = get_bounding_box(lat, lng, radius_km)
    
    print(f"\n中心点: ({lat}, {lng})")
    print(f"半径: {radius_km}公里")
    print(f"\n边界框:")
    print(f"  纬度范围: [{bbox['lat_min']:.6f}, {bbox['lat_max']:.6f}]")
    print(f"  经度范围: [{bbox['lng_min']:.6f}, {bbox['lng_max']:.6f}]")
    
    # 获取边界框内的Geohash
    print("\n边界框内的Geohash (精度5):")
    geohashes = get_geohashes_in_bbox(
        bbox['lat_min'], bbox['lat_max'],
        bbox['lng_min'], bbox['lng_max'],
        precision=5
    )
    print(f"  数量: {len(geohashes)}")
    print(f"  示例: {geohashes[:10]}...")


def example_expand():
    """扩展Geohash示例"""
    print("=" * 60)
    print("扩展 Geohash 示例")
    print("=" * 60)
    
    center = 'wx4g0b'  # 北京天安门附近
    
    for radius_km in [1, 5, 10]:
        expanded = expand(center, radius_km)
        print(f"\n中心: {center}, 半径: {radius_km}公里")
        print(f"  扩展后Geohash数量: {len(expanded)}")
        print(f"  Geohash列表: {expanded[:10]}{'...' if len(expanded) > 10 else ''}")


def example_validation():
    """验证示例"""
    print("=" * 60)
    print("Geohash 验证示例")
    print("=" * 60)
    
    test_cases = [
        ('wx4g0b', True),
        ('WX4G0B', True),
        ('s00000', True),
        ('b', True),
        ('', False),
        ('wx4g0o', False),  # 'o' 无效
        ('wx4g0a', False),  # 'a' 无效
        ('wx4g0i', False),  # 'i' 无效
        ('wx4g0l', False),  # 'l' 无效
    ]
    
    for geohash, expected in test_cases:
        result = is_valid(geohash)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{geohash}': {result} (期望: {expected})")


def example_midpoint_destination():
    """中点和目标点示例"""
    print("=" * 60)
    print("中点和目标点示例")
    print("=" * 60)
    
    # 北京和上海的中点
    beijing = (39.9042, 116.4074)
    shanghai = (31.2304, 121.4737)
    
    mid = midpoint(beijing[0], beijing[1], shanghai[0], shanghai[1])
    print(f"\n北京和上海的中点: ({mid[0]:.4f}, {mid[1]:.4f})")
    
    dist_to_beijing = distance(mid[0], mid[1], beijing[0], beijing[1])
    dist_to_shanghai = distance(mid[0], mid[1], shanghai[0], shanghai[1])
    print(f"  到北京的距离: {dist_to_beijing:.1f}km")
    print(f"  到上海的距离: {dist_to_shanghai:.1f}km")
    
    # 从北京向东北方向移动100公里
    print("\n从北京向东北方向移动100公里:")
    dest = destination(beijing[0], beijing[1], 45, 100)
    print(f"  目标点: ({dest[0]:.4f}, {dest[1]:.4f})")
    
    # 计算北京到上海的方位角
    brg = bearing(beijing[0], beijing[1], shanghai[0], shanghai[1])
    print(f"\n北京到上海的方位角: {brg:.1f}° (东南方向)")


def example_practical_use():
    """实际应用示例"""
    print("=" * 60)
    print("实际应用示例：附近地点搜索")
    print("=" * 60)
    
    # 模拟一个附近地点搜索场景
    user_location = (39.9042, 116.4074)  # 用户位置（北京天安门）
    search_radius = 5  # 搜索半径5公里
    
    print(f"\n用户位置: ({user_location[0]}, {user_location[1]})")
    print(f"搜索半径: {search_radius}公里")
    
    # 获取用户位置的Geohash
    user_geohash = encode(user_location[0], user_location[1], precision=6)
    print(f"用户Geohash: {user_geohash}")
    
    # 扩展Geohash覆盖搜索范围
    expanded = expand(user_geohash, search_radius)
    print(f"搜索范围Geohash数量: {len(expanded)}")
    
    # 模拟数据库查询（这里用示例数据）
    mock_places = [
        ("故宫", 39.9163, 116.3972),
        ("天坛", 39.8822, 116.4066),
        ("颐和园", 39.9999, 116.2755),  # 较远
        ("北海公园", 39.9249, 116.3840),
    ]
    
    print("\n附近地点:")
    for name, lat, lng in mock_places:
        dist = distance(user_location[0], user_location[1], lat, lng)
        if dist <= search_radius:
            brg = bearing(user_location[0], user_location[1], lat, lng)
            direction = "北" if brg < 45 or brg >= 315 else "东" if brg < 135 else "南" if brg < 225 else "西"
            print(f"  {name}: {dist:.2f}公里 ({direction}方向, 方位角{brg:.0f}°)")


def main():
    """运行所有示例"""
    example_encode()
    example_decode()
    example_neighbors()
    example_distance()
    example_precision()
    example_bounding_box()
    example_expand()
    example_validation()
    example_midpoint_destination()
    example_practical_use()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()