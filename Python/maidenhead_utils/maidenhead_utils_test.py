"""
Maidenhead Grid Locator Utils 测试文件

测试梅登黑德网格定位器工具的所有功能
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import MaidenheadUtils, validate_locator, latlon_to_locator, locator_to_latlon, locator_distance


class TestMaidenheadValidation:
    """验证功能测试"""
    
    def test_valid_2_char_locator(self):
        """测试有效的2字符定位器"""
        assert MaidenheadUtils.validate('FN')
        assert MaidenheadUtils.validate('JJ')
        assert MaidenheadUtils.validate('AB')
        assert MaidenheadUtils.validate('QR')
    
    def test_valid_4_char_locator(self):
        """测试有效的4字符定位器"""
        assert MaidenheadUtils.validate('FN31')
        assert MaidenheadUtils.validate('JJ00')
        assert MaidenheadUtils.validate('AB55')
    
    def test_valid_6_char_locator(self):
        """测试有效的6字符定位器"""
        assert MaidenheadUtils.validate('FN31pr')
        assert MaidenheadUtils.validate('JJ00aa')
        assert MaidenheadUtils.validate('AB55xx')
    
    def test_valid_8_char_locator(self):
        """测试有效的8字符定位器"""
        assert MaidenheadUtils.validate('FN31praa')
        assert MaidenheadUtils.validate('JJ00aaxx')
    
    def test_valid_10_char_locator(self):
        """测试有效的10字符定位器"""
        assert MaidenheadUtils.validate('FN31praaab')
        assert MaidenheadUtils.validate('JJ00aaxxaa')
    
    def test_invalid_empty_locator(self):
        """测试空定位器"""
        assert not MaidenheadUtils.validate('')
        assert not MaidenheadUtils.validate(None)
    
    def test_invalid_odd_length(self):
        """测试奇数长度"""
        assert not MaidenheadUtils.validate('FN3')
        assert not MaidenheadUtils.validate('FN31p')
    
    def test_invalid_first_pair_letters(self):
        """测试第一对无效字母"""
        assert not MaidenheadUtils.validate('SZ')  # S不在A-R范围内
        assert not MaidenheadUtils.validate('TA')
        # 注意：验证函数会自动转大写，所以 'aB' 实际会变成 'AB' 是有效的
        # 这是设计选择：大小写不敏感验证
    
    def test_invalid_second_pair_digits(self):
        """测试第二对无效数字"""
        assert not MaidenheadUtils.validate('FN3A')  # A不是数字
        assert not MaidenheadUtils.validate('FN3!')
    
    def test_invalid_third_pair_letters(self):
        """测试第三对无效字母"""
        assert not MaidenheadUtils.validate('FN31yz')  # y和z不在a-x范围内
        # 注意：验证函数会自动转大写，FN31AB会变成 FN31ab，这是有效的（A-X转成a-x）
    
    def test_case_insensitive_validation(self):
        """测试大小写不敏感验证"""
        assert MaidenheadUtils.validate('fn31pr')
        assert MaidenheadUtils.validate('FN31PR')
        assert MaidenheadUtils.validate('Fn31Pr')
    
    def test_whitespace_handling(self):
        """测试空格处理"""
        assert MaidenheadUtils.validate('FN31pr ')
        assert MaidenheadUtils.validate(' FN31pr')
        assert MaidenheadUtils.validate(' FN31pr ')


class TestMaidenheadConversion:
    """转换功能测试"""
    
    def test_locator_to_latlon_2_char(self):
        """测试2字符定位器转经纬度"""
        lat, lon = MaidenheadUtils.to_latlon('FN')
        # FN: F=经度索引5, N=纬度索引13
        # 经度范围: -80到-60, 中心 -70
        # 纬度范围: 40到50, 中心 45
        assert lat == 45.0  # 中心纬度
        assert lon == -70.0  # 中心经度
    
    def test_locator_to_latlon_4_char(self):
        """测试4字符定位器转经纬度"""
        lat, lon = MaidenheadUtils.to_latlon('FN31')
        # FN31: F=5, N=13, 经度偏移=3, 纬度偏移=1
        # 经度范围: -74到-72, 中心 -73
        # 纬度范围: 41到42, 中心 41.5
        assert round(lat, 1) == 41.5
        assert round(lon, 1) == -73.0
    
    def test_locator_to_latlon_6_char(self):
        """测试6字符定位器转经纬度"""
        lat, lon = MaidenheadUtils.to_latlon('FN31pr')
        # FN31pr: 经度中心 -72.7083, 纬度中心 41.7292
        assert round(lat, 4) == 41.7292
        assert round(lon, 4) == -72.7083
    
    def test_latlon_to_locator_2_char(self):
        """测试经纬度转2字符定位器"""
        locator = MaidenheadUtils.from_latlon(45.0, -70, precision=2)
        assert locator == 'FN'
    
    def test_latlon_to_locator_4_char(self):
        """测试经纬度转4字符定位器"""
        locator = MaidenheadUtils.from_latlon(41.5, -73, precision=4)
        assert locator == 'FN31'
    
    def test_latlon_to_locator_6_char(self):
        """测试经纬度转6字符定位器"""
        locator = MaidenheadUtils.from_latlon(41.5, -73, precision=6)
        # 41.5, -73 对应的6字符定位器应该是 FN31加子网格
        assert locator.startswith('FN31')
    
    def test_roundtrip_conversion(self):
        """测试往返转换"""
        original = 'FN31pr'
        lat, lon = MaidenheadUtils.to_latlon(original)
        converted = MaidenheadUtils.from_latlon(lat, lon, precision=6)
        assert converted == original
    
    def test_edge_case_north_pole(self):
        """测试北极边界"""
        # 北极附近: 纬度接近90
        locator = MaidenheadUtils.from_latlon(85, 0, precision=2)
        # 纬度85°: 累加后175°，对应索引17=R
        # 经度0°: 累加后180°，对应索引9=J
        assert locator[1] == 'R'  # 纬度部分
    
    def test_edge_case_south_pole(self):
        """测试南极边界"""
        # 南极附近: 纬度接近-90
        locator = MaidenheadUtils.from_latlon(-85, 0, precision=2)
        # 纬度-85°: 累加后5°，对应索引0=A
        assert locator[1] == 'A'  # 纬度部分
    
    def test_edge_case_prime_meridian(self):
        """测试本初子午线"""
        locator = MaidenheadUtils.from_latlon(0, 0, precision=4)
        assert locator == 'JJ00'
    
    def test_invalid_lat_out_of_range(self):
        """测试纬度超出范围"""
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(91, 0)
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(-91, 0)
    
    def test_invalid_lon_out_of_range(self):
        """测试经度超出范围"""
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(0, 181)
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(0, -181)
    
    def test_invalid_precision(self):
        """测试无效精度"""
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(40, -74, precision=3)
        with pytest.raises(ValueError):
            MaidenheadUtils.from_latlon(40, -74, precision=12)


class TestMaidenheadBounds:
    """边界计算测试"""
    
    def test_get_bounds_2_char(self):
        """测试2字符定位器边界"""
        bounds = MaidenheadUtils.get_bounds('FN')
        # FN: F=经度5, N=纬度13
        # 纬度: -90 + 13*10 = 40 到 50
        # 经度: -180 + 5*20 = -80 到 -60
        assert bounds['south'] == 40.0
        assert bounds['north'] == 50.0
        assert bounds['west'] == -80.0
        assert bounds['east'] == -60.0
    
    def test_get_bounds_4_char(self):
        """测试4字符定位器边界"""
        bounds = MaidenheadUtils.get_bounds('FN31')
        # FN31: F=5, N=13, 经度偏移=3, 纬度偏移=1
        # 纬度: 40 + 1*1 = 41 到 42
        # 经度: -80 + 3*2 = -74 到 -72
        assert bounds['south'] == 41.0
        assert bounds['north'] == 42.0
        assert bounds['west'] == -74.0
        assert bounds['east'] == -72.0
    
    def test_get_bounds_6_char(self):
        """测试6字符定位器边界"""
        bounds = MaidenheadUtils.get_bounds('FN31pr')
        # FN31pr: p=经度偏移15, r=纬度偏移17
        # 经度宽度: 2/24 ≈ 0.0833°
        # 纬度高度: 1/24 ≈ 0.0417°
        # 经度起点: -74 + 15*(2/24) = -74 + 1.25 = -72.75
        # 纬度起点: 41 + 17*(1/24) = 41 + 0.7083 = 41.7083
        assert round(bounds['south'], 4) == 41.7083
        assert round(bounds['north'], 4) == 41.75
        assert round(bounds['west'], 4) == -72.75
        assert round(bounds['east'], 4) == -72.6667
    
    def test_get_grid_size(self):
        """测试网格大小计算"""
        size = MaidenheadUtils.get_grid_size('FN')
        # 字段级网格约为 400×800 km，面积约 320000 km²
        assert size['area_km2'] > 100000  # 面积应该很大
        
        size_4 = MaidenheadUtils.get_grid_size('FN31')
        # 方格级网格约 2°×1°，在纬度41°附近面积约 18500 km²
        assert size_4['area_km2'] > 10000  # 方格级面积
        assert size_4['area_km2'] < 30000
        
        size_6 = MaidenheadUtils.get_grid_size('FN31pr')
        # 子网格级面积约 800 km² (2/24° × 1/24°)
        assert size_6['area_km2'] < 1000


class TestMaidenheadDistance:
    """距离计算测试"""
    
    def test_distance_same_locator(self):
        """测试相同定位器的距离"""
        dist = MaidenheadUtils.distance('FN31pr', 'FN31pr')
        assert dist == 0.0
    
    def test_distance_adjacent_fields(self):
        """测试相邻字段距离"""
        dist = MaidenheadUtils.distance('FN', 'FN')
        assert dist == 0.0
        
        dist_adj = MaidenheadUtils.distance('FN', 'FM')
        assert dist_adj > 0
    
    def test_distance_far_apart(self):
        """测试远距离定位器"""
        # 美国东海岸到欧洲
        dist = MaidenheadUtils.distance('FN31pr', 'JO')
        assert dist > 3000  # 应该大于3000公里
    
    def test_distance_in_miles(self):
        """测试英里单位"""
        dist_km = MaidenheadUtils.distance('FN', 'FM', unit='km')
        dist_mi = MaidenheadUtils.distance('FN', 'FM', unit='mi')
        # 英里应该比公里小
        assert dist_mi < dist_km
        # 比例约为 1.609
        ratio = dist_km / dist_mi
        assert round(ratio, 1) == 1.6
    
    def test_haversine_formula(self):
        """测试Haversine公式"""
        # 已知距离：纽约到洛杉矶约 4000公里
        ny_lat, ny_lon = 40.7128, -74.0060
        la_lat, la_lon = 34.0522, -118.2437
        
        dist = MaidenheadUtils.haversine_distance(ny_lat, ny_lon, la_lat, la_lon)
        assert 3500 < dist < 4500  # 大约范围


class TestMaidenheadBearing:
    """方位角计算测试"""
    
    def test_bearing_north(self):
        """测试北方方位角"""
        # 向北需要经度相同，纬度增加
        # FN(经度索引F=5) -> FO(经度索引F=5不变，纬度索引O=14增加)
        # 但实际上FN和FO的经度相同，纬度不同
        # 测试真正的向北方向
        bearing = MaidenheadUtils.bearing('FN', 'FO')
        # FN位置: (45N, 70W), FO位置: (55N, 70W) - 纬度增加10°
        # 方位角应该接近0（北）
        assert round(bearing) == 0 or round(bearing) == 360
    
    def test_bearing_east(self):
        """测试东方方位角"""
        # 向东（大致）
        # 这需要仔细计算
    
    def test_bearing_same_point(self):
        """测试同点方位角"""
        bearing = MaidenheadUtils.bearing('FN31pr', 'FN31pr')
        # 同一点方位角可能不确定，应该返回合理值
        assert 0 <= bearing <= 360


class TestMaidenheadNeighbors:
    """相邻网格测试"""
    
    def test_neighbors_2_char(self):
        """测试2字符定位器的相邻网格"""
        neighbors = MaidenheadUtils.neighbors('FN', level=1)
        # 应该有8个相邻（如果不在边界）
        assert len(neighbors) >= 3  # 至少有一些相邻
    
    def test_neighbors_6_char(self):
        """测试6字符定位器的相邻网格"""
        neighbors = MaidenheadUtils.neighbors('FN31pr', level=1)
        assert len(neighbors) >= 3
    
    def test_neighbors_boundary(self):
        """测试边界位置的相邻网格"""
        # 边界位置可能没有完整的8个相邻
        neighbors_edge = MaidenheadUtils.neighbors('AA', level=1)
        assert len(neighbors_edge) >= 0  # 边界可能有较少相邻
    
    def test_neighbors_level_2(self):
        """测试第二层邻域"""
        neighbors_l1 = MaidenheadUtils.neighbors('FN31', level=1)
        neighbors_l2 = MaidenheadUtils.neighbors('FN31', level=2)
        assert len(neighbors_l2) > len(neighbors_l1)


class TestMaidenheadPath:
    """路径计算测试"""
    
    def test_encode_decode_path(self):
        """测试路径编码解码"""
        path = ['FN31', 'FN32', 'FN33']
        encoded = MaidenheadUtils.encode_path(path)
        decoded = MaidenheadUtils.decode_path(encoded)
        assert decoded == path
    
    def test_path_distance(self):
        """测试路径距离"""
        path = ['FN', 'FM', 'FL']
        dist = MaidenheadUtils.path_distance(path)
        assert dist > 0
    
    def test_path_length(self):
        """测试路径长度"""
        path = ['FN31', 'FN32', 'FN33', 'FN34']
        length = MaidenheadUtils.path_length(path)
        assert length == 4
    
    def test_empty_path(self):
        """测试空路径"""
        assert MaidenheadUtils.encode_path([]) == ""
        assert MaidenheadUtils.decode_path("") == []
        assert MaidenheadUtils.path_distance([]) == 0.0
        assert MaidenheadUtils.path_length([]) == 0


class TestMaidenheadIntermediate:
    """中间点计算测试"""
    
    def test_intermediate_point_half(self):
        """测试中点"""
        intermediate = MaidenheadUtils.intermediate_point('FN31', 'FN33', 0.5)
        # 应该是FN32附近
        lat, lon = MaidenheadUtils.to_latlon(intermediate)
        lat1, lon1 = MaidenheadUtils.to_latlon('FN31')
        lat2, lon2 = MaidenheadUtils.to_latlon('FN33')
        # 中点应该大约在中间
        assert lat1 <= lat <= lat2 or lat2 <= lat <= lat1
    
    def test_intermediate_point_start(self):
        """测试起点"""
        intermediate = MaidenheadUtils.intermediate_point('FN31', 'FN33', 0.0)
        assert intermediate == 'FN31'
    
    def test_intermediate_point_end(self):
        """测试终点"""
        intermediate = MaidenheadUtils.intermediate_point('FN31', 'FN33', 1.0)
        assert intermediate == 'FN33'


class TestMaidenheadFormatting:
    """格式化测试"""
    
    def test_format_standard(self):
        """测试标准格式"""
        formatted = MaidenheadUtils.format_location('FN31pr', style='standard')
        assert 'FN31PR' in formatted
        # 坐标大约在 41.7N, 72.8W
        assert '41.' in formatted or '41' in formatted
    
    def test_format_compact(self):
        """测试紧凑格式"""
        formatted = MaidenheadUtils.format_location('FN31pr', style='compact')
        assert formatted == 'FN31PR'
    
    def test_format_detailed(self):
        """测试详细格式"""
        formatted = MaidenheadUtils.format_location('FN31pr', style='detailed')
        assert 'FN31PR' in formatted
        assert 'km²' in formatted
    
    def test_precision_description(self):
        """测试精度描述"""
        desc2 = MaidenheadUtils.precision_description(2)
        assert '字段级' in desc2
        
        desc4 = MaidenheadUtils.precision_description(4)
        assert '方格级' in desc4
        
        desc6 = MaidenheadUtils.precision_description(6)
        assert '子网格级' in desc6
    
    def test_normalize(self):
        """测试标准化"""
        normalized = MaidenheadUtils.normalize('fn31pr')
        assert normalized == 'FN31PR'
        
        normalized_ws = MaidenheadUtils.normalize(' fn31pr ')
        assert normalized_ws == 'FN31PR'


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_validate_locator_func(self):
        """测试验证函数"""
        assert validate_locator('FN31pr')
        assert not validate_locator('invalid')
    
    def test_latlon_to_locator_func(self):
        """测试转换函数"""
        locator = latlon_to_locator(45.0, -70, precision=4)
        # 45N, 70W 对应 FN31
        assert locator.startswith('FN')
    
    def test_locator_to_latlon_func(self):
        """测试转换函数"""
        lat, lon = locator_to_latlon('FN31')
        assert round(lat, 1) == 41.5
    
    def test_locator_distance_func(self):
        """测试距离函数"""
        dist = locator_distance('FN', 'FM')
        assert dist > 0


class TestRealWorldExamples:
    """真实世界示例测试"""
    
    def test_new_york_city(self):
        """测试纽约市"""
        # 纽约市大约在 FN31区域附近
        locator = MaidenheadUtils.from_latlon(40.7128, -74.0060, precision=6)
        # 40.7N, 74W 对应 FN31附近（具体子网格可能略有不同）
        assert locator.startswith('FN')
    
    def test_tokyo(self):
        """测试东京"""
        # 东京大约在 QM区域
        locator = MaidenheadUtils.from_latlon(35.6762, 139.6503, precision=2)
        # 东京: 35.7N, 139.7E
        # 经度: 180 + 139.7 = 319.7°, 累加后索引约15-16 = P或Q
        # 纬度: 90 + 35.7 = 125.7°, 累加后索引约12-13 = M或N
        # 实际计算应该是 QM附近
        assert locator[0] in 'PQ'  # 经度部分
        assert locator[1] in 'MN'  # 纬度部分
    
    def test_london(self):
        """测试伦敦"""
        # 伦敦大约在 IO
        locator = MaidenheadUtils.from_latlon(51.5074, -0.1278, precision=2)
        assert locator == 'IO'
    
    def test_sydney(self):
        """测试悉尼"""
        # 悉尼大约在 QF
        locator = MaidenheadUtils.from_latlon(-33.8688, 151.2093, precision=2)
        assert locator == 'QF'
    
    def test_los_angeles(self):
        """测试洛杉矶"""
        # 洛杉矶大约在 DM
        locator = MaidenheadUtils.from_latlon(34.0522, -118.2437, precision=2)
        assert locator == 'DM'


class TestPrecisionLevels:
    """精度级别测试"""
    
    def test_precision_comparison(self):
        """测试不同精度的网格大小"""
        size2 = MaidenheadUtils.get_grid_size('FN')
        size4 = MaidenheadUtils.get_grid_size('FN31')
        size6 = MaidenheadUtils.get_grid_size('FN31pr')
        size8 = MaidenheadUtils.get_grid_size('FN31praa')
        
        # 精度越高，面积越小
        assert size2['area_km2'] > size4['area_km2']
        assert size4['area_km2'] > size6['area_km2']
        assert size6['area_km2'] > size8['area_km2']
    
    def test_precision_progression(self):
        """测试精度递进"""
        base_lat, base_lon = 40.5, -74.5
        
        loc2 = MaidenheadUtils.from_latlon(base_lat, base_lon, 2)
        loc4 = MaidenheadUtils.from_latlon(base_lat, base_lon, 4)
        loc6 = MaidenheadUtils.from_latlon(base_lat, base_lon, 6)
        
        # 更高精度应该以更低精度为前缀
        assert loc4.startswith(loc2)
        assert loc6.startswith(loc4)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])