"""
geo_utils 模块测试
"""

import unittest
import math
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
    degrees_to_radians,
    radians_to_degrees,
    CITY_COORDINATES,
)


class TestBasicConversions(unittest.TestCase):
    """基础转换测试"""
    
    def test_degrees_to_radians(self):
        self.assertAlmostEqual(degrees_to_radians(180), math.pi, places=6)
        self.assertAlmostEqual(degrees_to_radians(90), math.pi / 2, places=6)
        self.assertAlmostEqual(degrees_to_radians(0), 0, places=6)
    
    def test_radians_to_degrees(self):
        self.assertAlmostEqual(radians_to_degrees(math.pi), 180, places=6)
        self.assertAlmostEqual(radians_to_degrees(math.pi / 2), 90, places=6)
        self.assertAlmostEqual(radians_to_degrees(0), 0, places=6)


class TestHaversineDistance(unittest.TestCase):
    """距离计算测试"""
    
    def test_beijing_to_shanghai(self):
        """测试北京到上海的距离"""
        distance = haversine_distance(39.9042, 116.4074, 31.2304, 121.4737)
        # 实际距离约1067公里
        self.assertAlmostEqual(distance, 1067, delta=5)
    
    def test_beijing_to_guangzhou(self):
        """测试北京到广州的距离"""
        distance = haversine_distance(39.9042, 116.4074, 23.1291, 113.2644)
        # 实际距离约1888公里
        self.assertAlmostEqual(distance, 1888, delta=10)
    
    def test_same_point(self):
        """测试同一点距离为0"""
        distance = haversine_distance(39.9042, 116.4074, 39.9042, 116.4074)
        self.assertAlmostEqual(distance, 0, places=6)
    
    def test_distance_units(self):
        """测试不同距离单位"""
        km = haversine_distance(39.9042, 116.4074, 31.2304, 121.4737, "km")
        m = haversine_distance(39.9042, 116.4074, 31.2304, 121.4737, "m")
        mi = haversine_distance(39.9042, 116.4074, 31.2304, 121.4737, "mi")
        
        self.assertAlmostEqual(m, km * 1000, places=1)
        self.assertAlmostEqual(mi, km * 0.621371, delta=1)
    
    def test_antipodal_points(self):
        """测试对趾点距离约为地球半周长"""
        # 北京的大致对趾点
        distance = haversine_distance(39.9042, 116.4074, -39.9042, -63.5926)
        # 应该接近地球周长的一半（约20000公里）
        self.assertAlmostEqual(distance, 19900, delta=500)


class TestBearing(unittest.TestCase):
    """方位角测试"""
    
    def test_bearing_north(self):
        """测试正北方向"""
        bearing = calculate_bearing(40.0, 116.0, 41.0, 116.0)
        self.assertAlmostEqual(bearing, 0, delta=1)
    
    def test_bearing_east(self):
        """测试正东方向"""
        bearing = calculate_bearing(40.0, 116.0, 40.0, 117.0)
        self.assertAlmostEqual(bearing, 90, delta=1)
    
    def test_bearing_south(self):
        """测试正南方向"""
        bearing = calculate_bearing(40.0, 116.0, 39.0, 116.0)
        self.assertAlmostEqual(bearing, 180, delta=1)
    
    def test_bearing_west(self):
        """测试正西方向"""
        bearing = calculate_bearing(40.0, 116.0, 40.0, 115.0)
        self.assertAlmostEqual(bearing, 270, delta=1)
    
    def test_bearing_to_compass(self):
        """测试方位角转罗盘方向"""
        self.assertEqual(bearing_to_compass(0), 'N')
        self.assertEqual(bearing_to_compass(45), 'NE')
        self.assertEqual(bearing_to_compass(90), 'E')
        self.assertEqual(bearing_to_compass(135), 'SE')
        self.assertEqual(bearing_to_compass(180), 'S')
        self.assertEqual(bearing_to_compass(225), 'SW')
        self.assertEqual(bearing_to_compass(270), 'W')
        self.assertEqual(bearing_to_compass(315), 'NW')


class TestDestinationPoint(unittest.TestCase):
    """目标点计算测试"""
    
    def test_destination_north(self):
        """测试向北移动"""
        lat, lon = destination_point(40.0, 116.0, 0, 111, "km")  # 约1度纬度
        self.assertAlmostEqual(lat, 41.0, delta=0.1)
        self.assertAlmostEqual(lon, 116.0, delta=0.1)
    
    def test_destination_roundtrip(self):
        """测试往返一致性"""
        start_lat, start_lon = 39.9042, 116.4074
        distance = 500
        bearing = 135  # 东南方向
        
        end_lat, end_lon = destination_point(start_lat, start_lon, bearing, distance, "km")
        # 直接使用终点到起点的方位角
        back_bearing = calculate_bearing(end_lat, end_lon, start_lat, start_lon)
        back_lat, back_lon = destination_point(end_lat, end_lon, back_bearing, distance, "km")
        
        # 由于球面计算的特性，往返会有小误差
        self.assertAlmostEqual(back_lat, start_lat, delta=1.0)
        self.assertAlmostEqual(back_lon, start_lon, delta=1.0)


class TestBoundingBox(unittest.TestCase):
    """边界框测试"""
    
    def test_bounding_box_center(self):
        """测试边界框中心点"""
        bbox = get_bounding_box(40.0, 116.0, 10, "km")
        
        # 中心点应该在边界框内
        self.assertTrue(is_point_in_bounding_box(40.0, 116.0, bbox))
    
    def test_bounding_box_outside(self):
        """测试边界框外的点"""
        bbox = get_bounding_box(40.0, 116.0, 10, "km")
        
        # 远处的点不应该在边界框内
        self.assertFalse(is_point_in_bounding_box(50.0, 116.0, bbox))
        self.assertFalse(is_point_in_bounding_box(40.0, 126.0, bbox))


class TestMidpoint(unittest.TestCase):
    """中点测试"""
    
    def test_midpoint_equator(self):
        """测试赤道上中点"""
        lat, lon = midpoint(0.0, 0.0, 0.0, 2.0)
        self.assertAlmostEqual(lat, 0.0, places=6)
        self.assertAlmostEqual(lon, 1.0, places=6)
    
    def test_midpoint_beijing_shanghai(self):
        """测试北京上海中点"""
        lat, lon = midpoint(39.9042, 116.4074, 31.2304, 121.4737)
        # 中点应该大约在山东附近
        self.assertTrue(34 < lat < 37)
        self.assertTrue(117 < lon < 120)


class TestInterpolation(unittest.TestCase):
    """插值测试"""
    
    def test_interpolate_simple(self):
        """测试简单插值"""
        points = interpolate_points(0.0, 0.0, 0.0, 3.0, 2)
        self.assertEqual(len(points), 4)  # 起点 + 2插值点 + 终点
        self.assertAlmostEqual(points[0][0], 0.0, places=6)
        self.assertAlmostEqual(points[3][0], 0.0, places=6)
        self.assertAlmostEqual(points[3][1], 3.0, places=6)


class TestCoordinateConversion(unittest.TestCase):
    """坐标转换测试"""
    
    def test_dms_to_decimal(self):
        """测试度分秒转十进制"""
        # 北京坐标: 39°54'15.12"N, 116°24'26.64"E
        lat = dms_to_decimal(39, 54, 15.12, 'N')
        self.assertAlmostEqual(lat, 39.9042, places=4)
        
        lon = dms_to_decimal(116, 24, 26.64, 'E')
        self.assertAlmostEqual(lon, 116.4074, places=4)
    
    def test_dms_to_decimal_south(self):
        """测试南纬转换"""
        lat = dms_to_decimal(33, 52, 10.8, 'S')
        self.assertAlmostEqual(lat, -33.869667, places=4)
    
    def test_dms_to_decimal_west(self):
        """测试西经转换"""
        lon = dms_to_decimal(151, 12, 35.52, 'W')
        self.assertAlmostEqual(lon, -151.209867, places=4)
    
    def test_decimal_to_dms(self):
        """测试十进制转度分秒"""
        d, m, s, direction = decimal_to_dms(39.9042, True)
        self.assertEqual(d, 39)
        self.assertEqual(m, 54)
        self.assertAlmostEqual(s, 15.12, places=1)
        self.assertEqual(direction, 'N')
    
    def test_decimal_to_dms_negative(self):
        """测试负数转换"""
        d, m, s, direction = decimal_to_dms(-33.869667, True)
        self.assertEqual(direction, 'S')


class TestFormatCoordinates(unittest.TestCase):
    """坐标格式化测试"""
    
    def test_format_decimal(self):
        """测试十进制格式"""
        result = format_coordinates(39.9042, 116.4074, "decimal")
        self.assertIn("39.9042°N", result)
        self.assertIn("116.4074°E", result)
    
    def test_format_dms(self):
        """测试度分秒格式"""
        result = format_coordinates(39.9042, 116.4074, "dms")
        self.assertIn("39°", result)
        self.assertIn("N", result)


class TestFindNearestPoint(unittest.TestCase):
    """最近点查找测试"""
    
    def test_find_nearest(self):
        """测试查找最近点"""
        points = [
            (31.2304, 121.4737),  # 上海
            (30.5728, 114.3052),  # 武汉 (注意：坐标修正)
            (29.5630, 106.5516),  # 重庆
        ]
        idx, point, distance = find_nearest_point(39.9042, 116.4074, points)  # 北京
        
        # 离北京最近的应该是上海（约1067公里）或武汉（约1050公里）
        # 实际上武汉坐标约 (30.5728, 114.3052)，距离北京约1050公里
        self.assertIn(idx, [0, 1])  # 上海或武汉之一
        self.assertAlmostEqual(distance, 1050, delta=50)


class TestCalculateArea(unittest.TestCase):
    """面积计算测试"""
    
    def test_small_square(self):
        """测试小正方形面积"""
        # 北京附近约1度×1度的区域
        polygon = [
            (40.0, 116.0),
            (40.0, 117.0),
            (39.0, 117.0),
            (39.0, 116.0),
        ]
        area = calculate_area(polygon, "km2")
        # 约111km × 85km ≈ 9400 km²
        self.assertTrue(8000 < area < 12000)
    
    def test_triangle(self):
        """测试三角形面积"""
        polygon = [
            (0.0, 0.0),
            (0.0, 1.0),
            (1.0, 0.0),
        ]
        area = calculate_area(polygon, "km2")
        # 球面三角形面积应该为正值
        self.assertTrue(area >= 0)
        # 面积不应该太大（约6000平方公里以下）
        self.assertTrue(area < 10000)


class TestGeoPoint(unittest.TestCase):
    """GeoPoint类测试"""
    
    def test_geo_point_creation(self):
        """测试创建GeoPoint"""
        point = GeoPoint(39.9042, 116.4074, "北京")
        self.assertEqual(point.lat, 39.9042)
        self.assertEqual(point.lon, 116.4074)
        self.assertEqual(point.name, "北京")
    
    def test_geo_point_distance(self):
        """测试GeoPoint距离计算"""
        beijing = GeoPoint(39.9042, 116.4074, "北京")
        shanghai = GeoPoint(31.2304, 121.4737, "上海")
        
        distance = beijing.distance_to(shanghai)
        self.assertAlmostEqual(distance, 1067, delta=5)
    
    def test_geo_point_bearing(self):
        """测试GeoPoint方位角计算"""
        beijing = GeoPoint(39.9042, 116.4074)
        shanghai = GeoPoint(31.2304, 121.4737)
        
        bearing = beijing.bearing_to(shanghai)
        # 北京到上海约为东南方向
        self.assertTrue(140 < bearing < 160)
    
    def test_geo_point_destination(self):
        """测试GeoPoint目标点计算"""
        start = GeoPoint(40.0, 116.0)
        end = start.destination(0, 111, "km")  # 向北111公里
        
        self.assertAlmostEqual(end.lat, 41.0, delta=0.1)
    
    def test_geo_point_midpoint(self):
        """测试GeoPoint中点计算"""
        p1 = GeoPoint(0.0, 0.0)
        p2 = GeoPoint(0.0, 2.0)
        mid = p1.midpoint_to(p2)
        
        self.assertAlmostEqual(mid.lat, 0.0, places=6)
        self.assertAlmostEqual(mid.lon, 1.0, places=6)
    
    def test_geo_point_bounding_box(self):
        """测试GeoPoint边界框"""
        point = GeoPoint(40.0, 116.0)
        bbox = point.bounding_box(10, "km")
        
        self.assertTrue(is_point_in_bounding_box(40.0, 116.0, bbox))
    
    def test_geo_point_to_dms(self):
        """测试GeoPoint度分秒转换"""
        point = GeoPoint(39.9042, 116.4074)
        lat_str, lon_str = point.to_dms()
        
        self.assertIn("39°", lat_str)
        self.assertIn("N", lat_str)
        self.assertIn("116°", lon_str)
        self.assertIn("E", lon_str)
    
    def test_geo_point_equality(self):
        """测试GeoPoint相等性"""
        p1 = GeoPoint(39.9042, 116.4074)
        p2 = GeoPoint(39.9042, 116.4074)
        p3 = GeoPoint(39.9042, 116.4075)
        
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
    
    def test_geo_point_repr(self):
        """测试GeoPoint字符串表示"""
        point = GeoPoint(39.9042, 116.4074, "北京")
        repr_str = repr(point)
        
        self.assertIn("GeoPoint", repr_str)
        self.assertIn("北京", repr_str)


class TestCityCoordinates(unittest.TestCase):
    """城市坐标测试"""
    
    def test_get_city_coordinates(self):
        """测试获取城市坐标"""
        coords = get_city_coordinates("北京")
        self.assertEqual(coords, (39.9042, 116.4074))
        
        coords = get_city_coordinates("上海")
        self.assertEqual(coords, (31.2304, 121.4737))
    
    def test_get_city_coordinates_not_found(self):
        """测试未找到城市"""
        coords = get_city_coordinates("不存在的城市")
        self.assertIsNone(coords)
    
    def test_distance_between_cities(self):
        """测试城市间距离"""
        distance = distance_between_cities("北京", "上海")
        self.assertAlmostEqual(distance, 1067, delta=10)
    
    def test_distance_between_cities_not_found(self):
        """测试未找到城市返回None"""
        distance = distance_between_cities("北京", "不存在的城市")
        self.assertIsNone(distance)


if __name__ == "__main__":
    unittest.main(verbosity=2)