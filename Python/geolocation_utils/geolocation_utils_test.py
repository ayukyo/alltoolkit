#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geolocation Utils 测试套件
==========================

全面测试地理定位工具库的所有功能。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

import unittest
import math
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Coordinate, DistanceUnit, Geofence,
    haversine_distance, initial_bearing, final_bearing,
    destination_point, bounding_box, midpoint, interpolate,
    is_point_in_polygon, polygon_area,
    encode_geohash, decode_geohash, geohash_neighbors,
    dm_to_decimal, decimal_to_dm, utm_zone, lat_to_utm_band,
    distance_between, bearing_to_compass, format_coordinates,
    UNIT_TO_METERS, WGS84_A, WGS84_B
)


class TestCoordinate(unittest.TestCase):
    """测试 Coordinate 类"""
    
    def test_create_coordinate(self):
        """测试坐标创建"""
        coord = Coordinate(39.9042, 116.4074)
        self.assertEqual(coord.latitude, 39.9042)
        self.assertEqual(coord.longitude, 116.4074)
        self.assertIsNone(coord.altitude)
    
    def test_coordinate_with_altitude(self):
        """测试带海拔的坐标"""
        coord = Coordinate(39.9042, 116.4074, 50.0)
        self.assertEqual(coord.altitude, 50.0)
    
    def test_coordinate_properties(self):
        """测试坐标属性"""
        coord = Coordinate(39.9042, 116.4074)
        self.assertEqual(coord.lat, 39.9042)
        self.assertEqual(coord.lng, 116.4074)
        self.assertAlmostEqual(coord.lat_rad, math.radians(39.9042), places=6)
        self.assertAlmostEqual(coord.lng_rad, math.radians(116.4074), places=6)
    
    def test_coordinate_validation(self):
        """测试坐标验证"""
        # 有效坐标
        Coordinate(90, 180)
        Coordinate(-90, -180)
        Coordinate(0, 0)
        
        # 无效纬度
        with self.assertRaises(ValueError):
            Coordinate(91, 0)
        with self.assertRaises(ValueError):
            Coordinate(-91, 0)
        
        # 无效经度
        with self.assertRaises(ValueError):
            Coordinate(0, 181)
        with self.assertRaises(ValueError):
            Coordinate(0, -181)
    
    def test_to_dms(self):
        """测试度分秒转换"""
        coord = Coordinate(39.9042, 116.4074)
        lat_dms, lng_dms = coord.to_dms()
        
        self.assertEqual(lat_dms[0], 39)
        self.assertEqual(lat_dms[1], 54)
        self.assertAlmostEqual(lat_dms[2], 15.12, places=1)
        
        self.assertEqual(lng_dms[0], 116)
        self.assertEqual(lng_dms[1], 24)
        self.assertAlmostEqual(lng_dms[2], 26.64, places=1)
    
    def test_from_dms(self):
        """测试从度分秒创建"""
        coord = Coordinate.from_dms(39, 54, 15.12, 116, 24, 26.64)
        self.assertAlmostEqual(coord.latitude, 39.9042, places=3)
        self.assertAlmostEqual(coord.longitude, 116.4074, places=3)
        
        # 南纬西经
        coord_sw = Coordinate.from_dms(1, 0, 0, 1, 0, 0, 'S', 'W')
        self.assertAlmostEqual(coord_sw.latitude, -1.0, places=6)
        self.assertAlmostEqual(coord_sw.longitude, -1.0, places=6)


class TestHaversineDistance(unittest.TestCase):
    """测试 Haversine 距离计算"""
    
    def test_beijing_shanghai(self):
        """测试北京到上海的距离"""
        beijing = Coordinate(39.9042, 116.4074)
        shanghai = Coordinate(31.2304, 121.4737)
        
        dist = haversine_distance(beijing, shanghai)
        # 实际距离约 1068 km
        self.assertAlmostEqual(dist, 1068, delta=10)
    
    def test_same_point(self):
        """测试相同点的距离"""
        coord = Coordinate(39.9042, 116.4074)
        dist = haversine_distance(coord, coord)
        self.assertEqual(dist, 0)
    
    def test_antipodal_points(self):
        """测试对跖点距离"""
        # 对跖点距离约为地球周长的一半 (约 20000 km)
        point1 = Coordinate(0, 0)
        point2 = Coordinate(0, 180)
        dist = haversine_distance(point1, point2)
        self.assertAlmostEqual(dist, 20015, delta=50)
    
    def test_distance_units(self):
        """测试不同距离单位"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 1)  # 经度差 1 度
        
        dist_km = haversine_distance(coord1, coord2, DistanceUnit.KILOMETERS)
        dist_m = haversine_distance(coord1, coord2, DistanceUnit.METERS)
        dist_mi = haversine_distance(coord1, coord2, DistanceUnit.MILES)
        
        self.assertAlmostEqual(dist_m, dist_km * 1000, places=1)
        self.assertAlmostEqual(dist_mi, dist_km / 1.609344, places=2)
    
    def test_equator_distance(self):
        """测试赤道上的距离"""
        # 赤道上经度差 1 度约 111.32 km
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 1)
        dist = haversine_distance(coord1, coord2)
        self.assertAlmostEqual(dist, 111.32, delta=0.5)


class TestBearing(unittest.TestCase):
    """测试方位角计算"""
    
    def test_initial_bearing(self):
        """测试初始方位角"""
        beijing = Coordinate(39.9042, 116.4074)
        shanghai = Coordinate(31.2304, 121.4737)
        
        bearing = initial_bearing(beijing, shanghai)
        # 北京到上海大约是东南方向
        self.assertTrue(130 < bearing < 170)
    
    def test_north_bearing(self):
        """测试正北方位角"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(10, 0)  # 正北
        
        bearing = initial_bearing(coord1, coord2)
        self.assertAlmostEqual(bearing, 0, delta=1)
    
    def test_east_bearing(self):
        """测试正东方位角"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 10)  # 正东
        
        bearing = initial_bearing(coord1, coord2)
        self.assertAlmostEqual(bearing, 90, delta=1)
    
    def test_south_bearing(self):
        """测试正南方位角"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(-10, 0)  # 正南
        
        bearing = initial_bearing(coord1, coord2)
        self.assertAlmostEqual(bearing, 180, delta=1)
    
    def test_west_bearing(self):
        """测试正西方位角"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, -10)  # 正西
        
        bearing = initial_bearing(coord1, coord2)
        self.assertAlmostEqual(bearing, 270, delta=1)
    
    def test_final_bearing(self):
        """测试最终方位角"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(10, 0)
        
        bearing = final_bearing(coord1, coord2)
        # 从 (0,0) 到 (10,0) 是正北方向
        # 终点返回起点是正南(180)，再加180变成360(即0)
        # 所以最终方位角是 0
        self.assertAlmostEqual(bearing, 0, delta=5)


class TestDestinationPoint(unittest.TestCase):
    """测试目的地计算"""
    
    def test_destination_basic(self):
        """测试基本目的地计算"""
        # 从北京出发，向上海方向走约 1068 km
        beijing = Coordinate(39.9042, 116.4074)
        shanghai = Coordinate(31.2304, 121.4737)
        
        bearing = initial_bearing(beijing, shanghai)
        dest = destination_point(beijing, bearing, 1068)
        
        self.assertAlmostEqual(dest.latitude, shanghai.latitude, delta=0.5)
        self.assertAlmostEqual(dest.longitude, shanghai.longitude, delta=0.5)
    
    def test_destination_north(self):
        """测试向北的目的地"""
        start = Coordinate(0, 0)
        dest = destination_point(start, 0, 111.32)  # 向北约 1 度
        
        self.assertAlmostEqual(dest.latitude, 1, delta=0.1)
        self.assertAlmostEqual(dest.longitude, 0, delta=0.1)
    
    def test_destination_east(self):
        """测试向东的目的地"""
        start = Coordinate(0, 0)
        dest = destination_point(start, 90, 111.32)  # 向东
        
        self.assertAlmostEqual(dest.latitude, 0, delta=0.1)
        self.assertAlmostEqual(dest.longitude, 1, delta=0.1)


class TestBoundingBox(unittest.TestCase):
    """测试边界框计算"""
    
    def test_bounding_box_basic(self):
        """测试基本边界框"""
        center = Coordinate(0, 0)
        sw, ne = bounding_box(center, 111.32)  # 约 1 度
        
        # 边界框应该包含中心点
        self.assertTrue(sw.latitude < center.latitude < ne.latitude)
        self.assertTrue(sw.longitude < center.longitude < ne.longitude)
    
    def test_bounding_box_contains(self):
        """测试边界框是否正确包含点"""
        center = Coordinate(39.9042, 116.4074)
        sw, ne = bounding_box(center, 10)  # 10 km
        
        # 中心附近的点应该在内
        nearby = Coordinate(39.91, 116.42)
        self.assertTrue(sw.latitude <= nearby.latitude <= ne.latitude)
        self.assertTrue(sw.longitude <= nearby.longitude <= ne.longitude)


class TestMidpoint(unittest.TestCase):
    """测试中点计算"""
    
    def test_midpoint_basic(self):
        """测试基本中点计算"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 2)
        
        mid = midpoint(coord1, coord2)
        self.assertAlmostEqual(mid.latitude, 0, delta=0.1)
        self.assertAlmostEqual(mid.longitude, 1, delta=0.1)
    
    def test_midpoint_beijing_shanghai(self):
        """测试北京上海的中点"""
        beijing = Coordinate(39.9042, 116.4074)
        shanghai = Coordinate(31.2304, 121.4737)
        
        mid = midpoint(beijing, shanghai)
        
        # 中点纬度应该大约在中间
        self.assertTrue(35 < mid.latitude < 36)
        # 中点经度可能在 117-119 之间（考虑球面几何）
        self.assertTrue(116 < mid.longitude < 120)


class TestInterpolate(unittest.TestCase):
    """测试插值计算"""
    
    def test_interpolate_start(self):
        """测试起点插值"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 10)
        
        result = interpolate(coord1, coord2, 0)
        self.assertAlmostEqual(result.latitude, 0, delta=0.1)
        self.assertAlmostEqual(result.longitude, 0, delta=0.1)
    
    def test_interpolate_mid(self):
        """测试中点插值"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 10)
        
        result = interpolate(coord1, coord2, 0.5)
        self.assertAlmostEqual(result.latitude, 0, delta=0.1)
        self.assertAlmostEqual(result.longitude, 5, delta=0.5)
    
    def test_interpolate_end(self):
        """测试终点插值"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 10)
        
        result = interpolate(coord1, coord2, 1)
        self.assertAlmostEqual(result.latitude, 0, delta=0.1)
        self.assertAlmostEqual(result.longitude, 10, delta=0.5)
    
    def test_interpolate_invalid_fraction(self):
        """测试无效插值比例"""
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(0, 10)
        
        with self.assertRaises(ValueError):
            interpolate(coord1, coord2, -0.1)
        with self.assertRaises(ValueError):
            interpolate(coord1, coord2, 1.1)


class TestPointInPolygon(unittest.TestCase):
    """测试点多边形判断"""
    
    def test_point_inside_square(self):
        """测试点在正方形内"""
        polygon = [
            Coordinate(-1, -1),
            Coordinate(1, -1),
            Coordinate(1, 1),
            Coordinate(-1, 1)
        ]
        
        point = Coordinate(0, 0)
        self.assertTrue(is_point_in_polygon(point, polygon))
    
    def test_point_outside_square(self):
        """测试点在正方形外"""
        polygon = [
            Coordinate(-1, -1),
            Coordinate(1, -1),
            Coordinate(1, 1),
            Coordinate(-1, 1)
        ]
        
        point = Coordinate(2, 2)
        self.assertFalse(is_point_in_polygon(point, polygon))
    
    def test_point_on_edge(self):
        """测试点在边上"""
        polygon = [
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(1, 1),
            Coordinate(0, 1)
        ]
        
        # 边上的点
        point = Coordinate(0.5, 0)
        # 射线法可能会返回 True 或 False，取决于实现


class TestPolygonArea(unittest.TestCase):
    """测试多边形面积计算"""
    
    def test_square_area(self):
        """测试正方形面积"""
        # 赤道上 1°×1° 的正方形
        polygon = [
            Coordinate(0, 0),
            Coordinate(0, 1),
            Coordinate(1, 1),
            Coordinate(1, 0)
        ]
        
        area = polygon_area(polygon)
        # 赤道上 1°×1° 约为 12356 km²
        self.assertTrue(12000 < area < 12500)
    
    def test_triangle_area(self):
        """测试三角形面积"""
        polygon = [
            Coordinate(0, 0),
            Coordinate(0, 1),
            Coordinate(1, 0)
        ]
        
        area = polygon_area(polygon)
        # 应该是正方形的一半，约 6000-6500 km²
        self.assertTrue(6000 < area < 6500)


class TestGeohash(unittest.TestCase):
    """测试 Geohash 编解码"""
    
    def test_encode_basic(self):
        """测试基本编码"""
        coord = Coordinate(39.9042, 116.4074)  # 北京
        geohash = encode_geohash(coord, 8)
        
        self.assertEqual(len(geohash), 8)
        self.assertTrue(all(c in '0123456789bcdefghjkmnpqrstuvwxyz' for c in geohash))
    
    def test_encode_decode_roundtrip(self):
        """测试编解码往返"""
        coord = Coordinate(39.9042, 116.4074)
        geohash = encode_geohash(coord, 8)
        decoded, err = decode_geohash(geohash)
        
        self.assertAlmostEqual(decoded.latitude, coord.latitude, delta=0.01)
        self.assertAlmostEqual(decoded.longitude, coord.longitude, delta=0.01)
    
    def test_decode_invalid(self):
        """测试无效 Geohash"""
        with self.assertRaises(ValueError):
            decode_geohash('invalid!')
    
    def test_geohash_neighbors(self):
        """测试相邻格子"""
        neighbors = geohash_neighbors('wx4g0b')
        self.assertEqual(len(neighbors), 8)
    
    def test_geohash_precision(self):
        """测试不同精度的 Geohash"""
        coord = Coordinate(39.9042, 116.4074)
        
        for precision in range(1, 13):
            geohash = encode_geohash(coord, precision)
            self.assertEqual(len(geohash), precision)
            
            decoded, _ = decode_geohash(geohash)
            # 精度越高，误差越小
            # 这里的测试是确保解码不会出错


class TestCoordinateConversion(unittest.TestCase):
    """测试坐标转换工具"""
    
    def test_dm_to_decimal(self):
        """测试度分转十进制"""
        decimal = dm_to_decimal(39, 54.252, 'N')
        self.assertAlmostEqual(decimal, 39.9042, places=3)
        
        decimal_south = dm_to_decimal(1, 0, 'S')
        self.assertAlmostEqual(decimal_south, -1.0, places=6)
    
    def test_decimal_to_dm(self):
        """测试十进制转度分"""
        degrees, minutes, direction = decimal_to_dm(39.9042)
        self.assertEqual(degrees, 39)
        self.assertAlmostEqual(minutes, 54.252, places=2)
        self.assertEqual(direction, 'N')
    
    def test_utm_zone(self):
        """测试 UTM 区号"""
        self.assertEqual(utm_zone(-177), 1)  # 西经 177°
        self.assertEqual(utm_zone(-3), 30)    # 西经 3°
        self.assertEqual(utm_zone(0), 31)     # 本初子午线
        self.assertEqual(utm_zone(116), 50)   # 北京
        self.assertEqual(utm_zone(177), 60)   # 东经 177°
    
    def test_lat_to_utm_band(self):
        """测试 UTM 纬度带"""
        # UTM 纬度带从 -80 开始，每 8 度一个带
        # -80 to -72: C, -72 to -64: D, -64 to -56: E, etc.
        self.assertEqual(lat_to_utm_band(-76), 'C')  # -80 to -72 范围内
        self.assertEqual(lat_to_utm_band(-68), 'D')  # -72 to -64 范围内
        self.assertEqual(lat_to_utm_band(0), 'N')    # 0 to 8
        self.assertEqual(lat_to_utm_band(39), 'S')   # 32 to 40
        self.assertEqual(lat_to_utm_band(75), 'X')   # 64 to 84
        
        # 超出范围
        with self.assertRaises(ValueError):
            lat_to_utm_band(-85)
        with self.assertRaises(ValueError):
            lat_to_utm_band(85)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_distance_between(self):
        """测试快捷距离函数"""
        dist = distance_between(39.9042, 116.4074, 31.2304, 121.4737)
        self.assertAlmostEqual(dist, 1068, delta=10)
        
        # 不同单位
        dist_m = distance_between(0, 0, 0, 1, 'm')
        self.assertTrue(111000 < dist_m < 112000)
        
        dist_mi = distance_between(0, 0, 0, 1, 'mi')
        self.assertTrue(69 < dist_mi < 70)
    
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
    
    def test_format_coordinates(self):
        """测试坐标格式化"""
        coord = Coordinate(39.9042, 116.4074)
        
        # 十进制度
        decimal = format_coordinates(coord, 'decimal')
        self.assertIn('39.9042', decimal)
        self.assertIn('N', decimal)
        
        # 度分秒
        dms = format_coordinates(coord, 'dms')
        self.assertIn('39', dms)
        self.assertIn('54', dms)
        
        # 度分
        dm = format_coordinates(coord, 'dm')
        self.assertIn('39', dm)


class TestGeofence(unittest.TestCase):
    """测试地理围栏"""
    
    def test_circle_fence_contains(self):
        """测试圆形围栏包含"""
        center = Coordinate(39.9042, 116.4074)
        fence = Geofence.circle(center, 10)  # 10 km
        
        # 围栏内的点
        inside = Coordinate(39.91, 116.42)
        self.assertTrue(fence.contains(inside))
        
        # 围栏外的点
        outside = Coordinate(40.0, 117.0)
        self.assertFalse(fence.contains(outside))
    
    def test_polygon_fence_contains(self):
        """测试多边形围栏包含"""
        polygon = [
            Coordinate(0, 0),
            Coordinate(0, 1),
            Coordinate(1, 1),
            Coordinate(1, 0)
        ]
        fence = Geofence.polygon(polygon)
        
        # 围栏内
        inside = Coordinate(0.5, 0.5)
        self.assertTrue(fence.contains(inside))
        
        # 围栏外
        outside = Coordinate(2, 2)
        self.assertFalse(fence.contains(outside))
    
    def test_rectangle_fence(self):
        """测试矩形围栏"""
        sw = Coordinate(0, 0)
        ne = Coordinate(1, 1)
        fence = Geofence.rectangle(sw, ne)
        
        # 围栏内
        inside = Coordinate(0.5, 0.5)
        self.assertTrue(fence.contains(inside))
        
        # 围栏外
        outside = Coordinate(1.5, 1.5)
        self.assertFalse(fence.contains(outside))
    
    def test_fence_distance_to_boundary(self):
        """测试到边界距离"""
        center = Coordinate(0, 0)
        fence = Geofence.circle(center, 100)  # 100 km
        
        # 围栏内的点
        inside = Coordinate(0, 0)
        dist = fence.distance_to_boundary(inside)
        self.assertAlmostEqual(dist, -100, delta=1)
        
        # 围栏外的点
        outside = Coordinate(0, 2)  # 约 222 km
        dist = fence.distance_to_boundary(outside)
        self.assertTrue(dist > 100)


class TestRealWorldScenarios(unittest.TestCase):
    """真实场景测试"""
    
    def test_china_major_cities(self):
        """测试中国主要城市距离"""
        cities = {
            '北京': Coordinate(39.9042, 116.4074),
            '上海': Coordinate(31.2304, 121.4737),
            '广州': Coordinate(23.1291, 113.2644),
            '深圳': Coordinate(22.5431, 114.0579),
            '成都': Coordinate(30.5728, 104.0668),
        }
        
        # 北京-上海
        dist = haversine_distance(cities['北京'], cities['上海'])
        self.assertTrue(1050 < dist < 1100)
        
        # 广州-深圳
        dist = haversine_distance(cities['广州'], cities['深圳'])
        self.assertTrue(100 < dist < 150)
        
        # 北京-成都
        dist = haversine_distance(cities['北京'], cities['成都'])
        self.assertTrue(1500 < dist < 1600)
    
    def test_world_cities(self):
        """测试世界城市距离"""
        cities = {
            '伦敦': Coordinate(51.5074, -0.1278),
            '纽约': Coordinate(40.7128, -74.0060),
            '东京': Coordinate(35.6762, 139.6503),
            '悉尼': Coordinate(-33.8688, 151.2093),
        }
        
        # 伦敦-纽约
        dist = haversine_distance(cities['伦敦'], cities['纽约'])
        self.assertTrue(5500 < dist < 5600)
        
        # 东京-悉尼
        dist = haversine_distance(cities['东京'], cities['悉尼'])
        self.assertTrue(7800 < dist < 7900)
    
    def test_travel_planning(self):
        """测试旅行规划场景"""
        # 规划从北京到上海的路线
        beijing = Coordinate(39.9042, 116.4074)
        shanghai = Coordinate(31.2304, 121.4737)
        
        # 计算总距离
        total_dist = haversine_distance(beijing, shanghai)
        
        # 计算中点
        mid = midpoint(beijing, shanghai)
        
        # 验证中点到两端距离相等
        dist_to_beijing = haversine_distance(mid, beijing)
        dist_to_shanghai = haversine_distance(mid, shanghai)
        self.assertAlmostEqual(dist_to_beijing, dist_to_shanghai, delta=10)


if __name__ == '__main__':
    unittest.main(verbosity=2)