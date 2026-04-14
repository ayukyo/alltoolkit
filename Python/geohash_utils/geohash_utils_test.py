"""
Geohash Utilities 单元测试

测试覆盖：
1. 编码功能
2. 解码功能
3. 相邻Geohash计算
4. 距离计算
5. 精度信息
6. 边界框计算
7. 验证功能
8. 中点和目标点计算
9. 方位角计算
"""

import unittest
import math
from mod import (
    encode, decode, get_neighbors, distance, get_precision_info,
    get_common_precision, get_bounding_box, get_geohashes_in_bbox,
    is_valid, expand, midpoint, destination, bearing,
    GeoHashError, GEOHASH_PRECISION_SIZES
)


class TestEncode(unittest.TestCase):
    """测试Geohash编码功能"""
    
    def test_encode_beijing(self):
        """测试北京坐标编码"""
        geohash = encode(39.9042, 116.4074, 6)
        self.assertEqual(geohash, 'wx4g0b')
    
    def test_encode_shanghai(self):
        """测试上海坐标编码"""
        geohash = encode(31.2304, 121.4737, 6)
        # 上海的Geohash应该是 'wtmkq3' 或类似
        self.assertEqual(len(geohash), 6)
        # 验证往返一致性
        decoded = decode(geohash)
        self.assertAlmostEqual(decoded['lat'], 31.2304, delta=0.1)
    
    def test_encode_new_york(self):
        """测试纽约坐标编码"""
        geohash = encode(40.7580, -73.9855, 6)
        self.assertTrue(geohash.startswith('dr5r'))
    
    def test_encode_precision(self):
        """测试不同精度的编码"""
        lat, lng = 39.9042, 116.4074
        for precision in range(1, 13):
            geohash = encode(lat, lng, precision)
            self.assertEqual(len(geohash), precision)
    
    def test_encode_invalid_latitude(self):
        """测试无效纬度"""
        with self.assertRaises(GeoHashError):
            encode(91.0, 0.0, 6)
        with self.assertRaises(GeoHashError):
            encode(-91.0, 0.0, 6)
    
    def test_encode_invalid_longitude(self):
        """测试无效经度"""
        with self.assertRaises(GeoHashError):
            encode(0.0, 181.0, 6)
        with self.assertRaises(GeoHashError):
            encode(0.0, -181.0, 6)
    
    def test_encode_invalid_precision(self):
        """测试无效精度"""
        with self.assertRaises(GeoHashError):
            encode(0.0, 0.0, 0)
        with self.assertRaises(GeoHashError):
            encode(0.0, 0.0, 13)
    
    def test_encode_equator_prime_meridian(self):
        """测试赤道和本初子午线交叉点"""
        geohash = encode(0.0, 0.0, 6)
        self.assertEqual(geohash, 's00000')
    
    def test_encode_polar_regions(self):
        """测试极地区域"""
        # 北极附近
        geohash = encode(89.0, 0.0, 6)
        self.assertTrue(is_valid(geohash))
        
        # 南极附近
        geohash = encode(-89.0, 0.0, 6)
        self.assertTrue(is_valid(geohash))


class TestDecode(unittest.TestCase):
    """测试Geohash解码功能"""
    
    def test_decode_beijing(self):
        """测试北京Geohash解码"""
        decoded = decode('wx4g0b')
        self.assertAlmostEqual(decoded['lat'], 39.9042, delta=0.01)
        self.assertAlmostEqual(decoded['lng'], 116.4074, delta=0.01)
    
    def test_decode_shanghai(self):
        """测试上海Geohash解码"""
        # 先编码上海坐标，再解码验证往返一致性
        shanghai_gh = encode(31.2304, 121.4737, 6)
        decoded = decode(shanghai_gh)
        self.assertAlmostEqual(decoded['lat'], 31.2304, delta=0.1)
        self.assertAlmostEqual(decoded['lng'], 121.4737, delta=0.1)
    
    def test_decode_precision(self):
        """测试解码结果的精度字段"""
        decoded = decode('wx4g0b')
        self.assertEqual(decoded['precision'], 6)
        
        decoded = decode('wx4g0b2xyz')
        self.assertEqual(decoded['precision'], 10)
    
    def test_decode_bounding_box(self):
        """测试边界框计算"""
        decoded = decode('wx4g0b')
        self.assertIn('lat_min', decoded)
        self.assertIn('lat_max', decoded)
        self.assertIn('lng_min', decoded)
        self.assertIn('lng_max', decoded)
        self.assertTrue(decoded['lat_min'] < decoded['lat_max'])
        self.assertTrue(decoded['lng_min'] < decoded['lng_max'])
    
    def test_decode_size(self):
        """测试尺寸信息"""
        decoded = decode('wx4g0b')
        self.assertIn('width_km', decoded)
        self.assertIn('height_km', decoded)
        self.assertTrue(decoded['width_km'] > 0)
        self.assertTrue(decoded['height_km'] > 0)
    
    def test_decode_invalid_char(self):
        """测试无效字符"""
        with self.assertRaises(GeoHashError):
            decode('wx4g0o')  # 'o' 不是有效字符
    
    def test_decode_invalid_a(self):
        """测试无效字符 'a'"""
        with self.assertRaises(GeoHashError):
            decode('wx4g0a')  # 'a' 不是有效字符
    
    def test_decode_empty(self):
        """测试空字符串"""
        with self.assertRaises(GeoHashError):
            decode('')
    
    def test_decode_case_insensitive(self):
        """测试大小写不敏感"""
        decoded_lower = decode('wx4g0b')
        decoded_upper = decode('WX4G0B')
        self.assertEqual(decoded_lower['lat'], decoded_upper['lat'])
        self.assertEqual(decoded_lower['lng'], decoded_upper['lng'])


class TestEncodeDecodeRoundtrip(unittest.TestCase):
    """测试编码解码往返一致性"""
    
    def test_roundtrip_major_cities(self):
        """测试主要城市的往返一致性"""
        cities = [
            ('Beijing', 39.9042, 116.4074),
            ('Shanghai', 31.2304, 121.4737),
            ('New York', 40.7128, -74.0060),
            ('London', 51.5074, -0.1278),
            ('Tokyo', 35.6762, 139.6503),
            ('Sydney', -33.8688, 151.2093),
            ('Paris', 48.8566, 2.3522),
            ('Moscow', 55.7558, 37.6173),
        ]
        
        for name, lat, lng in cities:
            for precision in [4, 6, 8, 10]:
                geohash = encode(lat, lng, precision)
                decoded = decode(geohash)
                
                # 解码的中心点应该在原始坐标附近
                error_km = distance(lat, lng, decoded['lat'], decoded['lng'])
                max_error = GEOHASH_PRECISION_SIZES[precision][0] * 2
                
                self.assertLess(error_km, max_error,
                    f"{name}往返误差过大: {error_km}km > {max_error}km (precision={precision})")


class TestNeighbors(unittest.TestCase):
    """测试相邻Geohash计算"""
    
    def test_neighbors_count(self):
        """测试邻居数量"""
        neighbors = get_neighbors('wx4g0b')
        self.assertEqual(len(neighbors), 8)
        self.assertIn('n', neighbors)
        self.assertIn('s', neighbors)
        self.assertIn('e', neighbors)
        self.assertIn('w', neighbors)
        self.assertIn('ne', neighbors)
        self.assertIn('nw', neighbors)
        self.assertIn('se', neighbors)
        self.assertIn('sw', neighbors)
    
    def test_neighbors_valid(self):
        """测试邻居都是有效的Geohash"""
        neighbors = get_neighbors('wx4g0b')
        for direction, neighbor in neighbors.items():
            self.assertTrue(is_valid(neighbor), f"{direction}方向邻居无效: {neighbor}")
    
    def test_neighbors_different(self):
        """测试邻居与中心不同"""
        neighbors = get_neighbors('wx4g0b')
        # 北邻居纬度应该更高
        center = decode('wx4g0b')
        n_decoded = decode(neighbors['n'])
        self.assertGreater(n_decoded['lat'], center['lat'])
        
        # 南邻居纬度应该更低
        s_decoded = decode(neighbors['s'])
        self.assertLess(s_decoded['lat'], center['lat'])
    
    def test_neighbors_empty(self):
        """测试空字符串"""
        with self.assertRaises(GeoHashError):
            get_neighbors('')


class TestDistance(unittest.TestCase):
    """测试距离计算"""
    
    def test_distance_beijing_shanghai(self):
        """测试北京到上海的距离"""
        dist = distance(39.9042, 116.4074, 31.2304, 121.4737)
        self.assertAlmostEqual(dist, 1067, delta=20)
    
    def test_distance_beijing_new_york(self):
        """测试北京到纽约的距离"""
        dist = distance(39.9042, 116.4074, 40.7128, -74.0060)
        self.assertAlmostEqual(dist, 10990, delta=100)
    
    def test_distance_zero(self):
        """测试相同点距离为零"""
        dist = distance(39.9042, 116.4074, 39.9042, 116.4074)
        self.assertAlmostEqual(dist, 0, delta=0.001)
    
    def test_distance_units(self):
        """测试不同单位"""
        lat1, lng1 = 39.9042, 116.4074
        lat2, lng2 = 31.2304, 121.4737
        
        dist_km = distance(lat1, lng1, lat2, lng2, 'km')
        dist_m = distance(lat1, lng1, lat2, lng2, 'm')
        dist_mile = distance(lat1, lng1, lat2, lng2, 'mile')
        
        self.assertAlmostEqual(dist_km * 1000, dist_m, delta=1)
        self.assertAlmostEqual(dist_km * 0.621371, dist_mile, delta=1)
    
    def test_distance_invalid_unit(self):
        """测试无效单位"""
        with self.assertRaises(GeoHashError):
            distance(0, 0, 1, 1, 'invalid')
    
    def test_distance_antipodal(self):
        """测试对拓点距离（地球半周长）"""
        dist = distance(0, 0, 0, 180)
        self.assertAlmostEqual(dist, 20015, delta=100)


class TestPrecisionInfo(unittest.TestCase):
    """测试精度信息功能"""
    
    def test_precision_info_keys(self):
        """测试返回的键"""
        info = get_precision_info(6)
        expected_keys = ['precision', 'width_km', 'height_km', 'area_km2',
                        'width_m', 'height_m', 'description']
        for key in expected_keys:
            self.assertIn(key, info)
    
    def test_precision_info_values(self):
        """测试精度值"""
        info = get_precision_info(6)
        self.assertEqual(info['precision'], 6)
        self.assertTrue(info['width_km'] > 0)
        self.assertTrue(info['height_km'] > 0)
        self.assertTrue(info['area_km2'] > 0)
    
    def test_precision_info_description(self):
        """测试精度描述"""
        info = get_precision_info(1)
        self.assertIn('全球', info['description'])
        
        info = get_precision_info(12)
        self.assertIn('精细', info['description'])
    
    def test_precision_info_invalid(self):
        """测试无效精度"""
        with self.assertRaises(GeoHashError):
            get_precision_info(0)
        with self.assertRaises(GeoHashError):
            get_precision_info(13)


class TestCommonPrecision(unittest.TestCase):
    """测试推荐精度计算"""
    
    def test_common_precision_medium(self):
        """测试中等范围"""
        precision = get_common_precision(10)
        self.assertGreater(precision, 3)
        self.assertLess(precision, 7)
    
    def test_common_precision_large(self):
        """测试大范围"""
        precision = get_common_precision(1000)
        self.assertLess(precision, 4)
    
    def test_common_precision_very_large(self):
        """测试超大范围"""
        precision = get_common_precision(10000)
        self.assertEqual(precision, 1)


class TestBoundingBox(unittest.TestCase):
    """测试边界框计算"""
    
    def test_bounding_box_keys(self):
        """测试返回的键"""
        bbox = get_bounding_box(39.9042, 116.4074, 10)
        expected_keys = ['lat_min', 'lat_max', 'lng_min', 'lng_max']
        for key in expected_keys:
            self.assertIn(key, bbox)
    
    def test_bounding_box_order(self):
        """测试边界顺序"""
        bbox = get_bounding_box(39.9042, 116.4074, 10)
        self.assertLess(bbox['lat_min'], bbox['lat_max'])
        self.assertLess(bbox['lng_min'], bbox['lng_max'])
    
    def test_bounding_box_center(self):
        """测试中心点"""
        lat, lng, radius = 39.9042, 116.4074, 10
        bbox = get_bounding_box(lat, lng, radius)
        
        center_lat = (bbox['lat_min'] + bbox['lat_max']) / 2
        center_lng = (bbox['lng_min'] + bbox['lng_max']) / 2
        
        self.assertAlmostEqual(center_lat, lat, delta=0.001)
        self.assertAlmostEqual(center_lng, lng, delta=0.001)
    
    def test_bounding_box_size(self):
        """测试边界框大小"""
        bbox = get_bounding_box(0, 0, 100)
        lat_span = bbox['lat_max'] - bbox['lat_min']
        
        # 100公里半径应该产生约200公里的纬度跨度（每度约111公里）
        self.assertAlmostEqual(lat_span * 111, 200, delta=20)


class TestIsValid(unittest.TestCase):
    """测试Geohash验证"""
    
    def test_valid_geohashes(self):
        """测试有效的Geohash"""
        valid_cases = ['wx4g0b', 'WX4G0B', 's00000', 'b', '0123456789bc']
        for geohash in valid_cases:
            self.assertTrue(is_valid(geohash), f"'{geohash}' 应该有效")
    
    def test_invalid_geohashes(self):
        """测试无效的Geohash"""
        invalid_cases = ['', 'wx4g0o', 'wx4g0a', 'wx4g0i', 'wx4g0l', 'wx4g0$']
        for geohash in invalid_cases:
            self.assertFalse(is_valid(geohash), f"'{geohash}' 应该无效")
    
    def test_is_valid_vs_decode(self):
        """测试验证与解码一致性"""
        self.assertTrue(is_valid('wx4g0b'))
        decode('wx4g0b')  # 不应抛出异常
        
        self.assertFalse(is_valid('wx4g0o'))
        with self.assertRaises(GeoHashError):
            decode('wx4g0o')


class TestExpand(unittest.TestCase):
    """测试Geohash扩展"""
    
    def test_expand_count(self):
        """测试扩展数量"""
        expanded = expand('wx4g0b', 5)
        self.assertGreater(len(expanded), 1)
    
    def test_expand_contains_center(self):
        """测试扩展包含附近区域"""
        center = decode('wx4g0b')
        expanded = expand('wx4g0b', 5)
        # 扩展结果应该包含中心附近的区域
        self.assertGreater(len(expanded), 0)
        # 检查扩展的点确实在中心附近
        for gh in expanded[:5]:
            decoded = decode(gh)
            dist = distance(center['lat'], center['lng'], decoded['lat'], decoded['lng'])
            self.assertLess(dist, 10)
    
    def test_expand_radius(self):
        """测试扩展半径"""
        center = decode('wx4g0b')
        expanded = expand('wx4g0b', 10)
        
        for gh in expanded:
            decoded = decode(gh)
            dist = distance(center['lat'], center['lng'], decoded['lat'], decoded['lng'])
            self.assertLess(dist, 50, f"扩展点 {gh} 距离中心过远: {dist}km")


class TestMidpoint(unittest.TestCase):
    """测试中点计算"""
    
    def test_midpoint_same_point(self):
        """测试相同点的中点"""
        lat, lng = 39.9042, 116.4074
        mid = midpoint(lat, lng, lat, lng)
        self.assertAlmostEqual(mid[0], lat, delta=0.001)
        self.assertAlmostEqual(mid[1], lng, delta=0.001)
    
    def test_midpoint_symmetry(self):
        """测试中点对称性"""
        lat1, lng1 = 39.9042, 116.4074
        lat2, lng2 = 31.2304, 121.4737
        
        mid1 = midpoint(lat1, lng1, lat2, lng2)
        mid2 = midpoint(lat2, lng2, lat1, lng1)
        
        self.assertAlmostEqual(mid1[0], mid2[0], delta=0.001)
        self.assertAlmostEqual(mid1[1], mid2[1], delta=0.001)
    
    def test_midpoint_distance(self):
        """测试中点到两端距离相等"""
        lat1, lng1 = 39.9042, 116.4074
        lat2, lng2 = 31.2304, 121.4737
        
        mid = midpoint(lat1, lng1, lat2, lng2)
        
        dist1 = distance(lat1, lng1, mid[0], mid[1])
        dist2 = distance(lat2, lng2, mid[0], mid[1])
        
        self.assertAlmostEqual(dist1, dist2, delta=10)


class TestDestination(unittest.TestCase):
    """测试目标点计算"""
    
    def test_destination_north(self):
        """测试向北移动"""
        lat, lng = 40.0, 0.0
        dest = destination(lat, lng, 0, 100)
        self.assertGreater(dest[0], lat)
        self.assertAlmostEqual(dest[1], lng, delta=1)
    
    def test_destination_south(self):
        """测试向南移动"""
        lat, lng = 40.0, 0.0
        dest = destination(lat, lng, 180, 100)
        self.assertLess(dest[0], lat)
        self.assertAlmostEqual(dest[1], lng, delta=1)
    
    def test_destination_east(self):
        """测试向东移动"""
        lat, lng = 0.0, 0.0
        dest = destination(lat, lng, 90, 100)
        self.assertGreater(dest[1], lng)
        self.assertAlmostEqual(dest[0], lat, delta=1)
    
    def test_destination_west(self):
        """测试向西移动"""
        lat, lng = 0.0, 0.0
        dest = destination(lat, lng, 270, 100)
        self.assertLess(dest[1], lng)
        self.assertAlmostEqual(dest[0], lat, delta=1)
    
    def test_destination_roundtrip(self):
        """测试往返"""
        lat, lng = 39.9042, 116.4074
        dest = destination(lat, lng, 45, 100)
        back = destination(dest[0], dest[1], 225, 100)
        
        self.assertAlmostEqual(back[0], lat, delta=0.1)
        self.assertAlmostEqual(back[1], lng, delta=0.1)


class TestBearing(unittest.TestCase):
    """测试方位角计算"""
    
    def test_bearing_north(self):
        """测试向北的方位角"""
        brg = bearing(0, 0, 10, 0)
        self.assertAlmostEqual(brg, 0, delta=1)
    
    def test_bearing_south(self):
        """测试向南的方位角"""
        brg = bearing(10, 0, 0, 0)
        self.assertAlmostEqual(brg, 180, delta=1)
    
    def test_bearing_east(self):
        """测试向东的方位角"""
        brg = bearing(0, 0, 0, 10)
        self.assertAlmostEqual(brg, 90, delta=1)
    
    def test_bearing_west(self):
        """测试向西的方位角"""
        brg = bearing(0, 10, 0, 0)
        self.assertAlmostEqual(brg, 270, delta=1)
    
    def test_bearing_opposite(self):
        """测试反向方位角"""
        lat1, lng1 = 39.9042, 116.4074
        lat2, lng2 = 31.2304, 121.4737
        
        brg_forward = bearing(lat1, lng1, lat2, lng2)
        brg_backward = bearing(lat2, lng2, lat1, lng1)
        
        diff = abs(brg_forward - brg_backward)
        self.assertAlmostEqual(diff, 180, delta=5)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_pole_coordinates(self):
        """测试极地坐标"""
        geohash = encode(89.9, 0, 6)
        self.assertTrue(is_valid(geohash))
        
        geohash = encode(-89.9, 0, 6)
        self.assertTrue(is_valid(geohash))
    
    def test_date_line(self):
        """测试国际日期变更线"""
        geohash1 = encode(0, 179.9, 6)
        self.assertTrue(is_valid(geohash1))
        
        geohash2 = encode(0, -179.9, 6)
        self.assertTrue(is_valid(geohash2))
    
    def test_high_precision(self):
        """测试高精度"""
        geohash = encode(39.9042, 116.4074, 12)
        self.assertEqual(len(geohash), 12)
        
        decoded = decode(geohash)
        self.assertAlmostEqual(decoded['lat'], 39.9042, delta=0.000001)
        self.assertAlmostEqual(decoded['lng'], 116.4074, delta=0.000001)
    
    def test_special_characters(self):
        """测试特殊字符"""
        invalid_chars = ['a', 'i', 'l', 'o', 'A', 'I', 'L', 'O']
        for char in invalid_chars:
            geohash = 'wx4g0' + char
            self.assertFalse(is_valid(geohash))


class TestGeohashesInBbox(unittest.TestCase):
    """测试边界框内Geohash计算"""
    
    def test_bbox_count(self):
        """测试边界框Geohash数量"""
        geohashes = get_geohashes_in_bbox(39.9, 39.92, 116.3, 116.5, 5)
        self.assertGreater(len(geohashes), 0)
    
    def test_bbox_coverage(self):
        """测试边界框覆盖"""
        lat_min, lat_max = 39.9, 39.92
        lng_min, lng_max = 116.3, 116.32
        precision = 5
        
        geohashes = get_geohashes_in_bbox(lat_min, lat_max, lng_min, lng_max, precision)
        
        for gh in geohashes:
            decoded = decode(gh)
            self.assertGreaterEqual(decoded['lat'], lat_min - 0.01)
            self.assertLessEqual(decoded['lat'], lat_max + 0.01)
    
    def test_bbox_invalid_precision(self):
        """测试无效精度"""
        with self.assertRaises(GeoHashError):
            get_geohashes_in_bbox(0, 1, 0, 1, 0)


class TestUtilityFunctions(unittest.TestCase):
    """测试辅助功能"""
    
    def test_format_geohash(self):
        """测试格式化"""
        from mod import format_geohash
        result = format_geohash('wx4g0b')
        self.assertEqual(result, 'W X 4 G 0 B')
    
    def test_geohash_to_color(self):
        """测试颜色生成"""
        from mod import geohash_to_color
        color = geohash_to_color('wx4g0b')
        self.assertTrue(color.startswith('#'))
        self.assertEqual(len(color), 7)


if __name__ == '__main__':
    unittest.main(verbosity=2)