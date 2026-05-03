"""
Geohash 工具模块使用示例

Author: AllToolkit
Date: 2026-05-03
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode, decode, get_neighbors, distance,
    get_precision_meters, get_bounding_box, get_geohashes_in_radius,
    is_valid, common_prefix, get_center, Geohash
)


def example_basic_encode_decode():
    """基础编码解码示例"""
    print("=" * 60)
    print("示例 1: 基础编码解码")
    print("=" * 60)
    
    # 编码坐标
    lat, lon = 39.9042, 116.4074  # 北京天安门
    precision = 6
    
    geohash = encode(lat, lon, precision)
    print(f"坐标 ({lat}, {lon}) 编码为: {geohash}")
    
    # 解码
    (decoded_lat, decoded_lon), bounds = decode(geohash)
    print(f"解码后坐标: ({decoded_lat:.6f}, {decoded_lon:.6f})")
    print(f"边界框: 纬度 [{bounds[0]:.6f}, {bounds[1]:.6f}], 经度 [{bounds[2]:.6f}, {bounds[3]:.6f}]")
    print()


def example_different_precisions():
    """不同精度示例"""
    print("=" * 60)
    print("示例 2: 不同精度")
    print("=" * 60)
    
    lat, lon = 39.9042, 116.4074
    
    for precision in range(1, 13):
        gh = encode(lat, lon, precision)
        error = get_precision_meters(precision)
        print(f"精度 {precision:2d}: {gh:12s} | 误差: ±{error:.1f}m")
    print()


def example_world_cities():
    """世界城市编码示例"""
    print("=" * 60)
    print("示例 3: 世界城市编码")
    print("=" * 60)
    
    cities = [
        ("北京", 39.9042, 116.4074),
        ("上海", 31.2304, 121.4737),
        ("东京", 35.6762, 139.6503),
        ("纽约", 40.7128, -74.0060),
        ("伦敦", 51.5074, -0.1278),
        ("巴黎", 48.8566, 2.3522),
        ("悉尼", -33.8688, 151.2093),
        ("开普敦", -33.9249, 18.4241),
        ("里约热内卢", -22.9068, -43.1729),
        ("莫斯科", 55.7558, 37.6173),
    ]
    
    for name, lat, lon in cities:
        gh = encode(lat, lon, 6)
        print(f"{name:12s}: ({lat:8.4f}, {lon:9.4f}) → {gh}")
    print()


def example_neighbors():
    """相邻区域示例"""
    print("=" * 60)
    print("示例 4: 相邻区域")
    print("=" * 60)
    
    geohash = "wx4g0b"  # 北京天安门
    print(f"Geohash: {geohash}")
    
    neighbors = get_neighbors(geohash)
    directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
    
    for direction, neighbor in zip(directions, neighbors):
        (lat, lon), _ = decode(neighbor)
        print(f"  {direction}: {neighbor} ({lat:.4f}, {lon:.4f})")
    print()


def example_distance():
    """距离计算示例"""
    print("=" * 60)
    print("示例 5: 距离计算")
    print("=" * 60)
    
    # 北京到上海的距离
    beijing = (39.9042, 116.4074)
    shanghai = (31.2304, 121.4737)
    d = distance(*beijing, *shanghai)
    print(f"北京 → 上海: {d:.2f} km")
    
    # 北京到纽约
    new_york = (40.7128, -74.0060)
    d = distance(*beijing, *new_york)
    print(f"北京 → 纽约: {d:.2f} km")
    
    # 北京到东京
    tokyo = (35.6762, 139.6503)
    d = distance(*beijing, *tokyo)
    print(f"北京 → 东京: {d:.2f} km")
    print()


def example_bounding_box():
    """边界框示例"""
    print("=" * 60)
    print("示例 6: 边界框计算")
    print("=" * 60)
    
    lat, lon = 39.9042, 116.4074
    radius_km = 10
    
    bbox = get_bounding_box(lat, lon, radius_km)
    print(f"中心点: ({lat}, {lon})")
    print(f"半径: {radius_km} km")
    print(f"边界框:")
    print(f"  纬度范围: [{bbox[0]:.6f}, {bbox[1]:.6f}]")
    print(f"  经度范围: [{bbox[2]:.6f}, {bbox[3]:.6f}]")
    print()


def example_geohashes_in_radius():
    """半径范围查询示例"""
    print("=" * 60)
    print("示例 7: 半径范围查询")
    print("=" * 60)
    
    lat, lon = 39.9042, 116.4074
    
    for radius in [1, 5, 10]:
        geohashes = get_geohashes_in_radius(lat, lon, radius, precision=6)
        print(f"半径 {radius:2d}km: {len(geohashes):3d} 个 geohash")
    print()


def example_common_prefix():
    """公共前缀示例"""
    print("=" * 60)
    print("示例 8: 公共前缀")
    print("=" * 60)
    
    # 同一区域的多个点
    geohashes = [
        encode(39.9042, 116.4074, 6),  # 北京天安门
        encode(39.9087, 116.3975, 6),  # 北京故宫
        encode(39.9163, 116.3908, 6),  # 北京景山公园
    ]
    
    print("Geohashes:")
    for gh in geohashes:
        (lat, lon), _ = decode(gh)
        print(f"  {gh} ({lat:.4f}, {lon:.4f})")
    
    prefix = common_prefix(geohashes)
    print(f"\n公共前缀: {prefix}")
    print(f"前缀长度: {len(prefix)} (误差约 {get_precision_meters(len(prefix)):.1f}m)")
    print()


def example_geohash_class():
    """Geohash 类示例"""
    print("=" * 60)
    print("示例 9: Geohash 类")
    print("=" * 60)
    
    # 创建 Geohash 对象
    gh = Geohash(39.9042, 116.4074, precision=6)
    
    print(f"Geohash: {gh}")
    print(f"坐标: ({gh.lat:.4f}, {gh.lon:.4f})")
    print(f"精度: {gh.precision}")
    print(f"边界框: {gh.bounds}")
    print(f"相邻区域: {gh.neighbors}")
    
    # 从 hash 创建
    gh2 = Geohash.from_hash('wtw3sj')  # 上海
    print(f"\n从 hash 创建: {gh2}")
    
    # 距离计算
    d = gh.distance_to(gh2)
    print(f"北京到上海距离: {d:.2f} km")
    
    # 包含检查
    print(f"\n北京 geohash 是否包含 (39.904, 116.407): {gh.contains(39.904, 116.407)}")
    print()


def example_validation():
    """有效性验证示例"""
    print("=" * 60)
    print("示例 10: 有效性验证")
    print("=" * 60)
    
    valid = "wx4g0b"
    invalid = "wx4g0i"  # 'i' 是无效字符
    
    print(f"'{valid}' 有效: {is_valid(valid)}")
    print(f"'{invalid}' 有效: {is_valid(invalid)}")
    print()


def example_practical_use():
    """实际应用示例"""
    print("=" * 60)
    print("示例 11: 实际应用 - 附近地点搜索")
    print("=" * 60)
    
    # 用户当前位置
    user_lat, user_lon = 39.9042, 116.4074
    user_gh = encode(user_lat, user_lon, 6)
    
    print(f"用户位置: ({user_lat}, {user_lon})")
    print(f"用户 geohash: {user_gh}")
    
    # 模拟一些地点
    places = [
        ("餐厅A", 39.9060, 116.4080),
        ("餐厅B", 39.9100, 116.4150),
        ("餐厅C", 39.9000, 116.4000),
        ("餐厅D", 39.9200, 116.4200),
    ]
    
    print("\n附近地点:")
    for name, lat, lon in places:
        gh = encode(lat, lon, 6)
        d = distance(user_lat, user_lon, lat, lon)
        print(f"  {name}: {gh} | 距离: {d:.2f} km")
    
    # 获取 5km 内的 geohash
    print("\n5km 范围内的 geohash 区域:")
    nearby_hashes = get_geohashes_in_radius(user_lat, user_lon, 5, precision=6)
    print(f"  共 {len(nearby_hashes)} 个区域: {nearby_hashes[:5]}...")
    print()


def example_geohash_prefix_search():
    """前缀搜索示例"""
    print("=" * 60)
    print("示例 12: 前缀搜索优化")
    print("=" * 60)
    
    # 在数据库查询中，可以使用 geohash 前缀进行范围查询
    # 例如查找附近 1km 内的点，可以使用精度为 5 的前缀
    
    points = [
        (39.9042, 116.4074),  # 北京天安门
        (39.9060, 116.4080),  # 附近
        (39.9100, 116.4150),  # 稍远
        (31.2304, 121.4737),  # 上海（很远）
    ]
    
    # 使用精度 5 的前缀
    target = encode(39.9042, 116.4074, 5)  # wx4g0
    print(f"目标区域前缀: {target}")
    
    print("\n点的分类:")
    for lat, lon in points:
        gh = encode(lat, lon, 5)
        is_nearby = gh == target
        status = "✓ 附近" if is_nearby else "✗ 远离"
        print(f"  ({lat:.4f}, {lon:.4f}) → {gh} {status}")
    print()


if __name__ == "__main__":
    example_basic_encode_decode()
    example_different_precisions()
    example_world_cities()
    example_neighbors()
    example_distance()
    example_bounding_box()
    example_geohashes_in_radius()
    example_common_prefix()
    example_geohash_class()
    example_validation()
    example_practical_use()
    example_geohash_prefix_search()
    
    print("=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)