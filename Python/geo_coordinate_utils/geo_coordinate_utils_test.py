"""
地理坐标工具模块测试
"""

import math
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    is_valid_coordinate,
    normalize_longitude,
    midpoint,
    total_distance,
    find_nearest,
    coordinates_within_radius,
    format_coordinate,
    to_geojson,
    EARTH_RADIUS_KM,
)


def test_decimal_to_dms():
    """测试十进制转DMS"""
    print("=" * 50)
    print("测试: decimal_to_dms")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        (39.9084, True, "39°54'30.24\"N"),
        (116.3972, False, "116°23'49.92\"E"),
        (-33.8568, True, "33°51'24.48\"S"),
        (-151.2153, False, "151°12'55.08\"W"),
        (0, True, "0°0'0.00\"N"),
        (90, True, "90°0'0.00\"N"),
        (-90, True, "90°0'0.00\"S"),
    ]
    
    all_passed = True
    for decimal, is_lat, expected_pattern in test_cases:
        result = decimal_to_dms(decimal, is_lat)
        # 检查方向正确
        if decimal >= 0:
            direction = "N" if is_lat else "E"
        else:
            direction = "S" if is_lat else "W"
        
        passed = direction in result
        status = "✓" if passed else "✗"
        print(f"  {status} decimal_to_dms({decimal}, is_latitude={is_lat})")
        print(f"      结果: {result}")
        
        if not passed:
            all_passed = False
    
    print()
    return all_passed


def test_dms_to_decimal():
    """测试DMS转十进制"""
    print("=" * 50)
    print("测试: dms_to_decimal")
    print("=" * 50)
    
    test_cases = [
        ("39°54'30\"N", 39.9083333),
        ("116°23'50\"E", 116.3972222),
        ("33°51'24\"S", -33.8566667),
        ("151°12'55\"W", -151.2152778),
        ("N39°54'30\"", 39.9083333),
        ("E116°23'50\"", 116.3972222),
        ("39 54 30 N", 39.9083333),
    ]
    
    all_passed = True
    for dms, expected in test_cases:
        result = dms_to_decimal(dms)
        passed = abs(result - expected) < 0.0001
        status = "✓" if passed else "✗"
        print(f"  {status} dms_to_decimal('{dms}')")
        print(f"      期望: {expected:.6f}, 结果: {result:.6f}")
        
        if not passed:
            all_passed = False
    
    print()
    return all_passed


def test_coordinate():
    """测试Coordinate类"""
    print("=" * 50)
    print("测试: Coordinate")
    print("=" * 50)
    
    all_passed = True
    
    # 测试创建
    try:
        coord = Coordinate(39.9042, 116.4074)
        print(f"  ✓ 创建坐标: {coord}")
    except Exception as e:
        print(f"  ✗ 创建坐标失败: {e}")
        all_passed = False
    
    # 测试边界验证
    try:
        coord = Coordinate(91, 0)
        print(f"  ✗ 应该抛出异常但没有")
        all_passed = False
    except ValueError as e:
        print(f"  ✓ 纬度越界正确抛出异常")
    
    try:
        coord = Coordinate(0, 181)
        print(f"  ✗ 应该抛出异常但没有")
        all_passed = False
    except ValueError as e:
        print(f"  ✓ 经度越界正确抛出异常")
    
    # 测试有效性检查
    coord = Coordinate(39.9042, 116.4074)
    passed = coord.is_valid
    status = "✓" if passed else "✗"
    print(f"  {status} 坐标有效性检查: {passed}")
    
    # 测试to_dms
    coord = Coordinate(39.9084, 116.3972)
    lat_dms, lon_dms = coord.to_dms()
    print(f"  ✓ DMS转换: {lat_dms}, {lon_dms}")
    
    print()
    return all_passed


def test_haversine_distance():
    """测试Haversine距离计算"""
    print("=" * 50)
    print("测试: haversine_distance")
    print("=" * 50)
    
    all_passed = True
    
    # 北京到上海
    beijing = Coordinate(39.9042, 116.4074)
    shanghai = Coordinate(31.2304, 121.4737)
    dist = haversine_distance(beijing, shanghai)
    expected = 1068  # 约1068公里
    passed = abs(dist - expected) < 10
    status = "✓" if passed else "✗"
    print(f"  {status} 北京到上海: {dist:.2f} km (期望约{expected} km)")
    if not passed:
        all_passed = False
    
    # 北京到纽约
    newyork = Coordinate(40.7128, -74.0060)
    dist = haversine_distance(beijing, newyork)
    expected = 10990  # 约10990公里
    passed = abs(dist - expected) < 100
    status = "✓" if passed else "✗"
    print(f"  {status} 北京到纽约: {dist:.2f} km (期望约{expected} km)")
    if not passed:
        all_passed = False
    
    # 同一点
    dist = haversine_distance(beijing, beijing)
    passed = dist < 0.001
    status = "✓" if passed else "✗"
    print(f"  {status} 同一点距离: {dist:.6f} km")
    if not passed:
        all_passed = False
    
    # 赤道一圈
    equator1 = Coordinate(0, 0)
    equator2 = Coordinate(0, 90)
    dist = haversine_distance(equator1, equator2)
    expected = EARTH_RADIUS_KM * math.pi / 2  # 四分之一圈
    passed = abs(dist - expected) < 10
    status = "✓" if passed else "✗"
    print(f"  {status} 赤道四分之一圈: {dist:.2f} km")
    if not passed:
        all_passed = False
    
    # 测试不同单位
    dist_km = haversine_distance(beijing, shanghai, "km")
    dist_m = haversine_distance(beijing, shanghai, "m")
    dist_mile = haversine_distance(beijing, shanghai, "mile")
    
    print(f"  ✓ 公里: {dist_km:.2f} km")
    print(f"  ✓ 米: {dist_m:.2f} m")
    print(f"  ✓ 英里: {dist_mile:.2f} miles")
    
    print()
    return all_passed


def test_bearing():
    """测试方位角计算"""
    print("=" * 50)
    print("测试: bearing")
    print("=" * 50)
    
    all_passed = True
    
    # 正北
    p1 = Coordinate(0, 0)
    p2 = Coordinate(1, 0)
    brng = bearing(p1, p2)
    passed = abs(brng - 0) < 1
    status = "✓" if passed else "✗"
    print(f"  {status} 正北方向: {brng:.2f}° (期望 0°)")
    if not passed:
        all_passed = False
    
    # 正东
    p1 = Coordinate(0, 0)
    p2 = Coordinate(0, 1)
    brng = bearing(p1, p2)
    passed = abs(brng - 90) < 1
    status = "✓" if passed else "✗"
    print(f"  {status} 正东方向: {brng:.2f}° (期望 90°)")
    if not passed:
        all_passed = False
    
    # 正南
    p1 = Coordinate(1, 0)
    p2 = Coordinate(0, 0)
    brng = bearing(p1, p2)
    passed = abs(brng - 180) < 1
    status = "✓" if passed else "✗"
    print(f"  {status} 正南方向: {brng:.2f}° (期望 180°)")
    if not passed:
        all_passed = False
    
    # 正西
    p1 = Coordinate(0, 1)
    p2 = Coordinate(0, 0)
    brng = bearing(p1, p2)
    passed = abs(brng - 270) < 1
    status = "✓" if passed else "✗"
    print(f"  {status} 正西方向: {brng:.2f}° (期望 270°)")
    if not passed:
        all_passed = False
    
    # 测试方向描述
    directions = [
        (0, "北"),
        (45, "东北"),
        (90, "东"),
        (135, "东南"),
        (180, "南"),
        (225, "西南"),
        (270, "西"),
        (315, "西北"),
    ]
    
    for deg, expected_dir in directions:
        result = bearing_to_direction(deg)
        passed = result == expected_dir
        status = "✓" if passed else "✗"
        print(f"  {status} bearing_to_direction({deg}°) = {result} (期望 {expected_dir})")
        if not passed:
            all_passed = False
    
    print()
    return all_passed


def test_destination_point():
    """测试终点计算"""
    print("=" * 50)
    print("测试: destination_point")
    print("=" * 50)
    
    all_passed = True
    
    # 从赤道向正北走100公里
    start = Coordinate(0, 0)
    dest = destination_point(start, 100, 0)
    # 纬度应该增加约0.9度
    expected_lat = 100 / 111.32  # 每度约111.32公里
    passed = abs(dest.latitude - expected_lat) < 0.1
    status = "✓" if passed else "✗"
    print(f"  {status} 正北100km: {dest}")
    print(f"      期望纬度约 {expected_lat:.2f}°")
    if not passed:
        all_passed = False
    
    # 向正东走100公里
    start = Coordinate(0, 0)
    dest = destination_point(start, 100, 90)
    passed = abs(dest.latitude) < 0.01 and dest.longitude > 0
    status = "✓" if passed else "✗"
    print(f"  {status} 正东100km: {dest}")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_bounding_box():
    """测试边界框计算"""
    print("=" * 50)
    print("测试: bounding_box")
    print("=" * 50)
    
    all_passed = True
    
    center = Coordinate(39.9042, 116.4074)  # 北京
    bbox = bounding_box(center, 10)  # 10公里范围
    
    print(f"  中心: {center}")
    print(f"  半径: 10 km")
    print(f"  边界框: {bbox}")
    
    # 检查边界框合理性
    lat_range = bbox.max_lat - bbox.min_lat
    lon_range = bbox.max_lon - bbox.min_lon
    
    passed = lat_range > 0 and lon_range > 0
    status = "✓" if passed else "✗"
    print(f"  {status} 纬度范围: {lat_range:.4f}°")
    print(f"  {status} 经度范围: {lon_range:.4f}°")
    
    # 测试contains
    inside = Coordinate(39.91, 116.41)
    outside = Coordinate(40.0, 116.5)
    
    passed = bbox.contains(center) and bbox.contains(inside) and not bbox.contains(outside)
    status = "✓" if passed else "✗"
    print(f"  {status} contains测试: 中心点在内部={bbox.contains(center)}")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_midpoint():
    """测试中点计算"""
    print("=" * 50)
    print("测试: midpoint")
    print("=" * 50)
    
    all_passed = True
    
    # 对角线中点
    p1 = Coordinate(0, 0)
    p2 = Coordinate(10, 20)
    mid = midpoint(p1, p2)
    
    print(f"  起点: {p1}")
    print(f"  终点: {p2}")
    print(f"  中点: {mid}")
    
    # 中点到两端距离应该相等
    dist1 = haversine_distance(p1, mid)
    dist2 = haversine_distance(p2, mid)
    
    passed = abs(dist1 - dist2) < 1  # 差距小于1公里
    status = "✓" if passed else "✗"
    print(f"  {status} 到起点距离: {dist1:.2f} km")
    print(f"  {status} 到终点距离: {dist2:.2f} km")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_total_distance():
    """测试路径总距离"""
    print("=" * 50)
    print("测试: total_distance")
    print("=" * 50)
    
    all_passed = True
    
    coords = [
        Coordinate(39.9042, 116.4074),  # 北京
        Coordinate(34.3416, 108.9398),  # 西安
        Coordinate(31.2304, 121.4737),  # 上海
    ]
    
    total = total_distance(coords)
    print(f"  路径: 北京 → 西安 → 上海")
    print(f"  总距离: {total:.2f} km")
    
    # 验证分段距离
    dist1 = haversine_distance(coords[0], coords[1])
    dist2 = haversine_distance(coords[1], coords[2])
    expected = dist1 + dist2
    
    passed = abs(total - expected) < 0.1
    status = "✓" if passed else "✗"
    print(f"  {status} 分段之和: {dist1:.2f} + {dist2:.2f} = {expected:.2f} km")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_find_nearest():
    """测试查找最近点"""
    print("=" * 50)
    print("测试: find_nearest")
    print("=" * 50)
    
    all_passed = True
    
    target = Coordinate(39.9, 116.4)  # 接近北京
    candidates = [
        Coordinate(31.2, 121.5),   # 上海
        Coordinate(34.3, 108.9),   # 西安
        Coordinate(40.0, 116.5),   # 北京附近
        Coordinate(22.5, 114.0),   # 香港
    ]
    
    nearest, dist, idx = find_nearest(target, candidates)
    
    print(f"  目标: {target}")
    print(f"  候选点:")
    for i, c in enumerate(candidates):
        marker = " ← 最近" if i == idx else ""
        print(f"    {i}: {c}{marker}")
    
    print(f"  最近点: {nearest}")
    print(f"  距离: {dist:.2f} km")
    print(f"  索引: {idx}")
    
    passed = idx == 2  # 北京附近应该是最近的
    status = "✓" if passed else "✗"
    print(f"  {status} 正确识别最近点")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_coordinates_within_radius():
    """测试半径内坐标查找"""
    print("=" * 50)
    print("测试: coordinates_within_radius")
    print("=" * 50)
    
    all_passed = True
    
    center = Coordinate(39.9, 116.4)
    coords = [
        Coordinate(39.91, 116.41),  # 约1.5公里
        Coordinate(39.95, 116.45),  # 约7公里
        Coordinate(35.0, 120.0),    # 很远
        Coordinate(40.0, 116.5),    # 约15公里
    ]
    
    results = coordinates_within_radius(center, coords, 10)
    
    print(f"  中心: {center}")
    print(f"  半径: 10 km")
    print(f"  范围内的点 ({len(results)}个):")
    for coord, dist in results:
        print(f"    {coord} - {dist:.2f} km")
    
    passed = len(results) == 2  # 应该只有2个点在10公里内
    status = "✓" if passed else "✗"
    print(f"  {status} 正确识别范围内的点 (期望2个)")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_format_coordinate():
    """测试坐标格式化"""
    print("=" * 50)
    print("测试: format_coordinate")
    print("=" * 50)
    
    all_passed = True
    
    coord = Coordinate(39.9042, 116.4074)
    
    # 十进制格式
    result = format_coordinate(coord, "decimal")
    print(f"  decimal: {result}")
    
    # DMS格式
    result = format_coordinate(coord, "dms")
    print(f"  dms: {result}")
    
    # GeoJSON格式
    result = format_coordinate(coord, "geojson")
    print(f"  geojson: {result}")
    passed = "[116.407400, 39.904200]" == result
    status = "✓" if passed else "✗"
    print(f"  {status} GeoJSON格式正确")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_to_geojson():
    """测试GeoJSON转换"""
    print("=" * 50)
    print("测试: to_geojson")
    print("=" * 50)
    
    all_passed = True
    
    coords = [
        Coordinate(39.9, 116.4),
        Coordinate(31.2, 121.5),
    ]
    
    geojson = to_geojson(coords)
    
    print(f"  输入: {len(coords)} 个坐标")
    print(f"  输出类型: {geojson['type']}")
    print(f"  特征数量: {len(geojson['features'])}")
    
    passed = geojson["type"] == "FeatureCollection" and len(geojson["features"]) == 2
    status = "✓" if passed else "✗"
    print(f"  {status} GeoJSON结构正确")
    if not passed:
        all_passed = False
    
    # 检查坐标顺序（GeoJSON是lon, lat）
    first_coords = geojson["features"][0]["geometry"]["coordinates"]
    passed = first_coords[0] == 116.4 and first_coords[1] == 39.9
    status = "✓" if passed else "✗"
    print(f"  {status} 坐标顺序正确 [lon, lat] = {first_coords}")
    if not passed:
        all_passed = False
    
    print()
    return all_passed


def test_normalize_longitude():
    """测试经度标准化"""
    print("=" * 50)
    print("测试: normalize_longitude")
    print("=" * 50)
    
    all_passed = True
    
    test_cases = [
        (190, -170),
        (-190, 170),
        (360, 0),
        (0, 0),
        (180, 180),
        (-180, -180),
    ]
    
    for lon, expected in test_cases:
        result = normalize_longitude(lon)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} normalize_longitude({lon}) = {result} (期望 {expected})")
        if not passed:
            all_passed = False
    
    print()
    return all_passed


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print(" 地理坐标工具模块 - 完整测试")
    print("=" * 60 + "\n")
    
    tests = [
        ("十进制转DMS", test_decimal_to_dms),
        ("DMS转十进制", test_dms_to_decimal),
        ("Coordinate类", test_coordinate),
        ("Haversine距离", test_haversine_distance),
        ("方位角", test_bearing),
        ("终点计算", test_destination_point),
        ("边界框", test_bounding_box),
        ("中点计算", test_midpoint),
        ("路径总距离", test_total_distance),
        ("查找最近点", test_find_nearest),
        ("半径内坐标", test_coordinates_within_radius),
        ("坐标格式化", test_format_coordinate),
        ("GeoJSON转换", test_to_geojson),
        ("经度标准化", test_normalize_longitude),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except Exception as e:
            results.append((name, False, str(e)))
    
    # 汇总
    print("=" * 60)
    print(" 测试结果汇总")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for _, p, _ in results if p)
    failed = total - passed
    
    for name, p, err in results:
        status = "✓ PASS" if p else "✗ FAIL"
        print(f"  {status} - {name}")
        if err:
            print(f"         错误: {err}")
    
    print()
    print(f"  总计: {total} 个测试")
    print(f"  通过: {passed} 个")
    print(f"  失败: {failed} 个")
    print(f"  通过率: {passed/total*100:.1f}%")
    print()
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)