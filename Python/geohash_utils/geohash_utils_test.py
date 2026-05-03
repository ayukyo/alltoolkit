"""
Geohash 工具模块测试

Author: AllToolkit
Date: 2026-05-03
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    encode, decode, get_neighbors, distance,
    get_precision_meters, get_bounding_box, get_geohashes_in_radius,
    is_valid, common_prefix, get_center, Geohash,
    BASE32_CHARS, BASE32_DECODE
)


class TestEncode(unittest.TestCase):
    """测试编码功能"""
    
    def test_beijing(self):
        """测试北京天安门编码"""
        result = encode(39.9042, 116.4074, 6)
        self.assertEqual(result, 'wx4g0b')
    
    def test_shanghai(self):
        """测试上海编码"""
        result = encode(31.2304, 121.4737, 6)
        self.assertEqual(result, 'wtw3sj')
    
    def test_new_york(self):
        """测试纽约编码"""
        result = encode(40.7128, -74.0060, 6)
        self.assertEqual(result, 'dr5reg')
    
    def test_london(self):
        """测试伦敦编码"""
        result = encode(51.5074, -0.1278, 6)
        self.assertEqual(result, 'gcpvj0')
    
    def test_precision_1(self):
        """测试精度 1"""
        result = encode(39.9042, 116.4074, 1)
        self.assertEqual(len(result), 1)
    
    def test_precision_12(self):
        """测试最高精度"""
        result = encode(39.9042, 116.4074, 12)
        self.assertEqual(len(result), 12)
    
    def test_invalid_latitude(self):
        """测试无效纬度"""
        with self.assertRaises(ValueError):
            encode(91, 0, 6)
        with self.assertRaises(ValueError):
            encode(-91, 0, 6)
    
    def test_invalid_longitude(self):
        """测试无效经度"""
        with self.assertRaises(ValueError):
            encode(0, 181, 6)
        with self.assertRaises(ValueError):
            encode(0, -181, 6)
    
    def test_invalid_precision(self):
        """测试无效精度"""
        with self.assertRaises(ValueError):
            encode(0, 0, 0)
        with self.assertRaises(ValueError):
            encode(0, 0, 13)
    
    def test_edge_case_lat_90(self):
        """测试纬度边界 90"""
        result = encode(90, 0, 6)
        self.assertTrue(is_valid(result))
    
    def test_edge_case_lon_180(self):
        """测试经度边界 180"""
        result = encode(0, 180, 6)
        self.assertTrue(is_valid(result))
    
    def test_equator(self):
        """测试赤道"""
        result = encode(0, 0, 6)
        self.assertEqual(result, 's00000')
    
    def test_south_pole(self):
        """测试南极"""
        result = encode(-90, 0, 6)
        self.assertTrue(is_valid(result))


class TestDecode(unittest.TestCase):
    """测试解码功能"""
    
    def test_decode_beijing(self):
        """测试解码北京"""
        (lat, lon), bounds = decode('wx4g0b')
        self.assertAlmostEqual(lat, 39.9042, delta=0.01)
        self.assertAlmostEqual(lon, 116.4074, delta=0.01)
    
    def test_decode_shanghai(self):
        """测试解码上海"""
        (lat, lon), bounds = decode('wtw3sj')
        self.assertAlmostEqual(lat, 31.2304, delta=0.01)
        self.assertAlmostEqual(lon, 121.4737, delta=0.01)
    
    def test_decode_encode_inverse(self):
        """测试编解码互逆性"""
        original_lat, original_lon = 39.9042, 116.4074
        gh = encode(original_lat, original_lon, 12)
        (lat, lon), _ = decode(gh)
        self.assertAlmostEqual(lat, original_lat, delta=0.000001)
        self.assertAlmostEqual(lon, original_lon, delta=0.000001)
    
    def test_bounds(self):
        """测试边界框"""
        _, bounds = decode('wx4g0b')
        lat_min, lat_max, lon_min, lon_max = bounds
        self.assertLess(lat_min, lat_max)
        self.assertLess(lon_min, lon_max)
        self.assertTrue(-90 <= lat_min <= 90)
        self.assertTrue(-90 <= lat_max <= 90)
        self.assertTrue(-180 <= lon_min <= 180)
        self.assertTrue(-180 <= lon_max <= 180)
    
    def test_invalid_geohash(self):
        """测试无效 geohash"""
        with self.assertRaises(ValueError):
            decode('')
        with self.assertRaises(ValueError):
            decode('wx4g0i')  # 'i' 是无效字符
    
    def test_decode_equator(self):
        """测试解码赤道"""
        (lat, lon), _ = decode('s00000')
        self.assertAlmostEqual(lat, 0, delta=0.1)
        self.assertAlmostEqual(lon, 0, delta=0.1)


class TestNeighbors(unittest.TestCase):
    """测试相邻区域计算"""
    
    def test_neighbors_count(self):
        """测试相邻区域数量"""
        neighbors = get_neighbors('wx4g0b')
        self.assertEqual(len(neighbors), 8)
    
    def test_neighbors_valid(self):
        """测试相邻区域都是有效的"""
        neighbors = get_neighbors('wx4g0b')
        for n in neighbors:
            self.assertTrue(is_valid(n))
    
    def test_neighbors_unique(self):
        """测试相邻区域都是唯一的"""
        neighbors = get_neighbors('wx4g0b')
        self.assertEqual(len(neighbors), len(set(neighbors)))
    
    def test_neighbors_precision(self):
        """测试相邻区域精度相同"""
        neighbors = get_neighbors('wx4g0b')
        for n in neighbors:
            self.assertEqual(len(n), 6)
    
    def test_neighbor_decode_valid(self):
        """测试相邻区域解码有效"""
        neighbors = get_neighbors('wx4g0b')
        center_lat, center_lon = decode('wx4g0b')[0]
        for n in neighbors:
            (lat, lon), _ = decode(n)
            # 相邻区域应该在中心区域附近
            self.assertTrue(distance(center_lat, center_lon, lat, lon) < 100)  # 小于100km


class TestDistance(unittest.TestCase):
    """测试距离计算"""
    
    def test_same_point(self):
        """测试相同点距离为 0"""
        d = distance(39.9042, 116.4074, 39.9042, 116.4074)
        self.assertAlmostEqual(d, 0, places=1)
    
    def test_beijing_shanghai(self):
        """测试北京上海距离"""
        d = distance(39.9042, 116.4074, 31.2304, 121.4737)
        self.assertAlmostEqual(d, 1068, delta=50)  # 约1068公里
    
    def test_beijing_new_york(self):
        """测试北京纽约距离"""
        d = distance(39.9042, 116.4074, 40.7128, -74.0060)
        self.assertAlmostEqual(d, 10980, delta=500)  # 约10980公里
    
    def test_equator_distance(self):
        """测试赤道距离"""
        d = distance(0, 0, 0, 1)
        self.assertAlmostEqual(d, 111.32, delta=1)  # 约111公里
    
    def test_pole_to_equator(self):
        """测试极地到赤道距离"""
        d = distance(90, 0, 0, 0)
        self.assertAlmostEqual(d, 10000, delta=100)  # 约10000公里


class TestPrecisionMeters(unittest.TestCase):
    """测试精度误差"""
    
    def test_precision_1(self):
        """测试精度 1 的误差"""
        meters = get_precision_meters(1)
        self.assertEqual(meters, 2500000)
    
    def test_precision_6(self):
        """测试精度 6 的误差"""
        meters = get_precision_meters(6)
        self.assertEqual(meters, 610)
    
    def test_precision_12(self):
        """测试精度 12 的误差"""
        meters = get_precision_meters(12)
        self.assertAlmostEqual(meters, 0.019, places=3)


class TestBoundingBox(unittest.TestCase):
    """测试边界框计算"""
    
    def test_bbox_beijing(self):
        """测试北京边界框"""
        lat_min, lat_max, lon_min, lon_max = get_bounding_box(39.9042, 116.4074, 10)
        self.assertAlmostEqual(lat_min, 39.8142, delta=0.1)
        self.assertAlmostEqual(lat_max, 39.9942, delta=0.1)
    
    def test_bbox_contains_center(self):
        """测试边界框包含中心点"""
        lat, lon = 39.9042, 116.4074
        lat_min, lat_max, lon_min, lon_max = get_bounding_box(lat, lon, 10)
        self.assertTrue(lat_min <= lat <= lat_max)
        self.assertTrue(lon_min <= lon <= lon_max)
    
    def test_bbox_near_pole(self):
        """测试近极地边界框"""
        lat_min, lat_max, lon_min, lon_max = get_bounding_box(85, 0, 100)
        self.assertLessEqual(lat_max, 90)


class TestGeohashesInRadius(unittest.TestCase):
    """测试半径范围内 geohash 查询"""
    
    def test_small_radius(self):
        """测试小半径"""
        geohashes = get_geohashes_in_radius(39.9042, 116.4074, 1, 6)
        self.assertGreater(len(geohashes), 0)
    
    def test_medium_radius(self):
        """测试中等半径"""
        geohashes = get_geohashes_in_radius(39.9042, 116.4074, 10, 5)
        self.assertGreater(len(geohashes), 1)
    
    def test_geohashes_valid(self):
        """测试返回的 geohash 都有效"""
        geohashes = get_geohashes_in_radius(39.9042, 116.4074, 5, 6)
        for gh in geohashes:
            self.assertTrue(is_valid(gh))


class TestIsValid(unittest.TestCase):
    """测试有效性检查"""
    
    def test_valid_geohash(self):
        """测试有效 geohash"""
        self.assertTrue(is_valid('wx4g0b'))
    
    def test_empty_geohash(self):
        """测试空 geohash"""
        self.assertFalse(is_valid(''))
    
    def test_invalid_char(self):
        """测试无效字符"""
        self.assertFalse(is_valid('wx4g0i'))  # 'i' 无效
        self.assertFalse(is_valid('wx4g0a'))  # 'a' 无效
        self.assertFalse(is_valid('wx4g0o'))  # 'o' 无效


class TestCommonPrefix(unittest.TestCase):
    """测试公共前缀"""
    
    def test_common_prefix(self):
        """测试公共前缀"""
        result = common_prefix(['wx4g0b', 'wx4g0c', 'wx4g0d'])
        self.assertEqual(result, 'wx4g0')
    
    def test_no_common_prefix(self):
        """测试无公共前缀"""
        result = common_prefix(['wx4g0b', 'dr5ru7'])
        self.assertEqual(result, '')
    
    def test_empty_list(self):
        """测试空列表"""
        result = common_prefix([])
        self.assertEqual(result, '')
    
    def test_single_item(self):
        """测试单个元素"""
        result = common_prefix(['wx4g0b'])
        self.assertEqual(result, 'wx4g0b')


class TestGetCenter(unittest.TestCase):
    """测试中心点计算"""
    
    def test_center_two_points(self):
        """测试两点中心"""
        lat, lon = get_center(['wx4g0b', 'wx4g0c'])
        self.assertAlmostEqual(lat, 39.904, delta=0.01)
    
    def test_center_invalid_empty(self):
        """测试空列表"""
        with self.assertRaises(ValueError):
            get_center([])


class TestGeohashClass(unittest.TestCase):
    """测试 Geohash 类"""
    
    def test_init(self):
        """测试初始化"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        self.assertEqual(gh.hash, 'wx4g0b')
    
    def test_properties(self):
        """测试属性"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        self.assertEqual(gh.precision, 6)
        self.assertAlmostEqual(gh.lat, 39.9042, delta=0.001)
        self.assertAlmostEqual(gh.lon, 116.4074, delta=0.001)
    
    def test_neighbors_property(self):
        """测试 neighbors 属性"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        self.assertEqual(len(gh.neighbors), 8)
    
    def test_bounds_property(self):
        """测试 bounds 属性"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        bounds = gh.bounds
        self.assertEqual(len(bounds), 4)
    
    def test_distance_to(self):
        """测试距离计算"""
        gh1 = Geohash(39.9042, 116.4074, precision=6)
        gh2 = Geohash(31.2304, 121.4737, precision=6)
        d = gh1.distance_to(gh2)
        self.assertAlmostEqual(d, 1068, delta=50)
    
    def test_contains(self):
        """测试包含检查"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        self.assertTrue(gh.contains(39.904, 116.407))
    
    def test_from_hash(self):
        """测试从 hash 创建"""
        gh = Geohash.from_hash('wx4g0b')
        self.assertEqual(gh.hash, 'wx4g0b')
        self.assertEqual(gh.precision, 6)
    
    def test_equality(self):
        """测试相等性"""
        gh1 = Geohash(39.9042, 116.4074, precision=6)
        gh2 = Geohash.from_hash('wx4g0b')
        self.assertEqual(gh1, gh2)
        self.assertEqual(gh1, 'wx4g0b')
    
    def test_str_repr(self):
        """测试字符串表示"""
        gh = Geohash(39.9042, 116.4074, precision=6)
        self.assertEqual(str(gh), 'wx4g0b')
        self.assertIn('wx4g0b', repr(gh))
    
    def test_hash(self):
        """测试哈希值"""
        gh1 = Geohash(39.9042, 116.4074, precision=6)
        gh2 = Geohash(39.9042, 116.4074, precision=6)
        self.assertEqual(hash(gh1), hash(gh2))


class TestBase32Constants(unittest.TestCase):
    """测试 Base32 常量"""
    
    def test_base32_chars_length(self):
        """测试 Base32 字符数量"""
        self.assertEqual(len(BASE32_CHARS), 32)
    
    def test_base32_decode_keys(self):
        """测试 Base32 解码键"""
        self.assertEqual(len(BASE32_DECODE), 32)
    
    def test_no_invalid_chars(self):
        """测试不包含无效字符"""
        invalid_chars = set('ailo')
        for char in BASE32_CHARS:
            self.assertNotIn(char, invalid_chars)


class TestRoundTrip(unittest.TestCase):
    """测试往返编解码"""
    
    def test_roundtrip_various_coords(self):
        """测试多种坐标的往返"""
        test_coords = [
            (0, 0),
            (45, 90),
            (-45, -90),
            (89.9, 179.9),
            (-89.9, -179.9),
            (23.5, 67.8),
        ]
        
        for lat, lon in test_coords:
            with self.subTest(lat=lat, lon=lon):
                gh = encode(lat, lon, 12)
                (decoded_lat, decoded_lon), _ = decode(gh)
                self.assertAlmostEqual(decoded_lat, lat, delta=0.000001)
                self.assertAlmostEqual(decoded_lon, lon, delta=0.000001)


if __name__ == '__main__':
    unittest.main()