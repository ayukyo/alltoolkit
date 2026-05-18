"""
province_utils 测试文件

测试覆盖:
- 省份查询（按简称、全称、代码、省会）
- 区号查询
- 相邻省份
- 行政区划类型筛选
- 统计信息
- 路径计算
- 边界值测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from province_utils.mod import (
    PROVINCES,
    RegionType,
    Province,
    get_all_provinces,
    get_province_by_short,
    get_province_by_name,
    get_province_by_code,
    get_province_by_capital,
    get_province_by_area_code,
    get_neighbors,
    search_province,
    get_provinces_by_type,
    get_municipalities,
    get_autonomous_regions,
    get_special_administrative_regions,
    get_province_cities,
    get_province_statistics,
    calculate_distance,
    find_route,
    validate_province_name,
    get_province_name_variants,
    get_national_statistics,
    list_province_short_names,
    list_province_names,
    export_to_dict,
)


class TestResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"期望 {expected}, 实际 {actual} - {msg}")
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"条件应为 True - {msg}")
    
    def assert_false(self, condition, msg=""):
        if not condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"条件应为 False - {msg}")
    
    def assert_none(self, value, msg=""):
        if value is None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"值应为 None, 实际为 {value} - {msg}")
    
    def assert_not_none(self, value, msg=""):
        if value is not None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"值不应为 None - {msg}")
    
    def assert_in(self, item, container, msg=""):
        if item in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"{item} 应在 {container} 中 - {msg}")
    
    def assert_length(self, obj, length, msg=""):
        if len(obj) == length:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"长度应为 {length}, 实际为 {len(obj)} - {msg}")
    
    def assert_greater(self, actual, threshold, msg=""):
        if actual > threshold:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"{actual} 应大于 {threshold} - {msg}")
    
    def assert_type(self, obj, expected_type, msg=""):
        if isinstance(obj, expected_type):
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"类型应为 {expected_type}, 实际为 {type(obj)} - {msg}")
    
    def report(self):
        total = self.passed + self.failed
        print(f"\n测试结果: {self.passed}/{total} 通过")
        if self.errors:
            print(f"\n失败详情:")
            for error in self.errors:
                print(f"  - {error}")
        return self.failed == 0


def test_province_data_structure():
    """测试省份数据结构"""
    r = TestResultCollector()
    
    # 测试省份数量
    r.assert_length(PROVINCES, 34, "应有 34 个省级行政区")
    
    # 测试数据结构完整性
    for short, prov in PROVINCES.items():
        r.assert_type(prov, Province, f"{short} 应为 Province 类型")
        r.assert_not_none(prov.name, f"{short} 名称不应为空")
        r.assert_not_none(prov.short_name, f"{short} 简称不应为空")
        r.assert_not_none(prov.code, f"{short} 代码不应为空")
        r.assert_not_none(prov.capital, f"{short} 省会不应为空")
        r.assert_type(prov.region_type, RegionType, f"{short} 类型应为 RegionType")
        r.assert_greater(prov.area_km2, 0, f"{short} 面积应大于 0")
        r.assert_not_none(prov.cities, f"{short} 城市列表不应为空")
    
    return r.report()


def test_get_all_provinces():
    """测试获取所有省份"""
    r = TestResultCollector()
    
    provinces = get_all_provinces()
    r.assert_length(provinces, 34, "应返回 34 个省份")
    r.assert_type(provinces, list, "应返回列表")
    
    # 检查每个元素都是 Province 类型
    for prov in provinces:
        r.assert_type(prov, Province, "元素应为 Province 类型")
    
    return r.report()


def test_get_province_by_short():
    """测试通过简称获取省份"""
    r = TestResultCollector()
    
    # 测试有效简称
    beijing = get_province_by_short("京")
    r.assert_not_none(beijing, "京应返回北京")
    r.assert_equal(beijing.name, "北京市", "名称应为北京市")
    r.assert_equal(beijing.capital, "北京", "省会应为北京")
    
    shanghai = get_province_by_short("沪")
    r.assert_not_none(shanghai, "沪应返回上海")
    r.assert_equal(shanghai.name, "上海市", "名称应为上海市")
    
    guangdong = get_province_by_short("粤")
    r.assert_not_none(guangdong, "粤应返回广东")
    r.assert_equal(guangdong.capital, "广州市", "省会应为广州市")
    
    # 测试无效简称
    invalid = get_province_by_short("无效")
    r.assert_none(invalid, "无效简称应返回 None")
    
    # 测试空字符串
    empty = get_province_by_short("")
    r.assert_none(empty, "空字符串应返回 None")
    
    return r.report()


def test_get_province_by_name():
    """测试通过全称获取省份"""
    r = TestResultCollector()
    
    # 测试有效全称
    beijing = get_province_by_name("北京市")
    r.assert_not_none(beijing, "北京市应返回北京")
    r.assert_equal(beijing.short_name, "京", "简称应为京")
    
    guangdong = get_province_by_name("广东省")
    r.assert_not_none(guangdong, "广东省应返回广东")
    r.assert_equal(guangdong.short_name, "粤", "简称应为粤")
    
    xizang = get_province_by_name("西藏自治区")
    r.assert_not_none(xizang, "西藏自治区应返回西藏")
    r.assert_equal(xizang.short_name, "藏", "简称应为藏")
    
    # 测试无效全称
    invalid = get_province_by_name("无效省")
    r.assert_none(invalid, "无效全称应返回 None")
    
    return r.report()


def test_get_province_by_code():
    """测试通过行政代码获取省份"""
    r = TestResultCollector()
    
    # 测试有效代码
    beijing = get_province_by_code("110000")
    r.assert_not_none(beijing, "110000应返回北京")
    r.assert_equal(beijing.short_name, "京", "简称应为京")
    
    guangdong = get_province_by_code("440000")
    r.assert_not_none(guangdong, "440000应返回广东")
    r.assert_equal(guangdong.short_name, "粤", "简称应为粤")
    
    xizang = get_province_by_code("540000")
    r.assert_not_none(xizang, "540000应返回西藏")
    r.assert_equal(xizang.short_name, "藏", "简称应为藏")
    
    # 测试无效代码
    invalid = get_province_by_code("999999")
    r.assert_none(invalid, "无效代码应返回 None")
    
    return r.report()


def test_get_province_by_capital():
    """测试通过省会获取省份"""
    r = TestResultCollector()
    
    # 测试有效省会
    beijing = get_province_by_capital("北京")
    r.assert_not_none(beijing, "北京应返回北京市")
    r.assert_equal(beijing.short_name, "京", "简称应为京")
    
    guangzhou = get_province_by_capital("广州市")
    r.assert_not_none(guangzhou, "广州市应返回广东省")
    r.assert_equal(guangzhou.short_name, "粤", "简称应为粤")
    
    chengdu = get_province_by_capital("成都市")
    r.assert_not_none(chengdu, "成都市应返回四川省")
    r.assert_equal(chengdu.short_name, "川", "简称应为川")
    
    # 测试无效省会
    invalid = get_province_by_capital("无效市")
    r.assert_none(invalid, "无效省会应返回 None")
    
    return r.report()


def test_get_province_by_area_code():
    """测试通过电话区号获取省份"""
    r = TestResultCollector()
    
    # 测试有效区号
    beijing = get_province_by_area_code("010")
    r.assert_not_none(beijing, "010应返回北京")
    r.assert_equal(beijing.short_name, "京", "简称应为京")
    
    shanghai = get_province_by_area_code("021")
    r.assert_not_none(shanghai, "021应返回上海")
    r.assert_equal(shanghai.short_name, "沪", "简称应为沪")
    
    guangzhou = get_province_by_area_code("020")
    r.assert_not_none(guangzhou, "020应返回广东")
    r.assert_equal(guangzhou.short_name, "粤", "简称应为粤")
    
    # 测试无前缀0的区号
    beijing2 = get_province_by_area_code("10")
    r.assert_not_none(beijing2, "10应返回北京")
    r.assert_equal(beijing2.short_name, "京", "简称应为京")
    
    # 测试无效区号
    invalid = get_province_by_area_code("000")
    r.assert_none(invalid, "无效区号应返回 None")
    
    return r.report()


def test_get_neighbors():
    """测试获取相邻省份"""
    r = TestResultCollector()
    
    # 测试北京相邻省份
    beijing_neighbors = get_neighbors("京")
    r.assert_length(beijing_neighbors, 2, "北京应有2个相邻省份")
    neighbor_shorts = [p.short_name for p in beijing_neighbors]
    r.assert_in("津", neighbor_shorts, "北京相邻天津")
    r.assert_in("冀", neighbor_shorts, "北京相邻河北")
    
    # 测试四川相邻省份（内陆省份，多个相邻）
    sichuan_neighbors = get_neighbors("川")
    r.assert_length(sichuan_neighbors, 7, "四川应有7个相邻省份")
    neighbor_shorts = [p.short_name for p in sichuan_neighbors]
    r.assert_in("青", neighbor_shorts, "四川相邻青海")
    r.assert_in("滇", neighbor_shorts, "四川相邻云南")
    r.assert_in("渝", neighbor_shorts, "四川相邻重庆")
    
    # 测试海南（无相邻）
    hainan_neighbors = get_neighbors("琼")
    r.assert_length(hainan_neighbors, 0, "海南无相邻省份")
    
    # 测试台湾（与福建相邻）
    taiwan_neighbors = get_neighbors("台")
    r.assert_length(taiwan_neighbors, 1, "台湾应有1个相邻省份")
    r.assert_equal(taiwan_neighbors[0].short_name, "闽", "台湾相邻福建")
    
    # 测试无效省份
    invalid_neighbors = get_neighbors("无效")
    r.assert_length(invalid_neighbors, 0, "无效省份应返回空列表")
    
    return r.report()


def test_search_province():
    """测试搜索省份"""
    r = TestResultCollector()
    
    # 搜索"北"
    results = search_province("北")
    r.assert_greater(len(results), 0, "搜索'北'应有结果")
    
    # 搜索"州"
    results = search_province("州")
    r.assert_greater(len(results), 0, "搜索'州'应有结果")
    
    # 搜索完整名称
    results = search_province("广东省")
    r.assert_length(results, 1, "搜索'广东省'应返回1个结果")
    r.assert_equal(results[0].short_name, "粤", "结果应为广东")
    
    # 搜索省会
    results = search_province("广州")
    r.assert_greater(len(results), 0, "搜索'广州'应有结果")
    
    # 搜索简称
    results = search_province("京")
    r.assert_greater(len(results), 0, "搜索'京'应有结果")
    
    # 搜索无匹配关键词
    results = search_province("无匹配关键词xyz")
    r.assert_length(results, 0, "无匹配应返回空列表")
    
    return r.report()


def test_get_provinces_by_type():
    """测试按行政区划类型获取省份"""
    r = TestResultCollector()
    
    # 测试直辖市
    municipalities = get_municipalities()
    r.assert_length(municipalities, 4, "应有4个直辖市")
    mun_names = [p.name for p in municipalities]
    r.assert_in("北京市", mun_names, "直辖市包含北京")
    r.assert_in("上海市", mun_names, "直辖市包含上海")
    r.assert_in("天津市", mun_names, "直辖市包含天津")
    r.assert_in("重庆市", mun_names, "直辖市包含重庆")
    
    # 测试自治区
    autonomous = get_autonomous_regions()
    r.assert_length(autonomous, 5, "应有5个自治区")
    auto_names = [p.name for p in autonomous]
    r.assert_in("内蒙古自治区", auto_names, "自治区包含内蒙古")
    r.assert_in("西藏自治区", auto_names, "自治区包含西藏")
    r.assert_in("新疆维吾尔自治区", auto_names, "自治区包含新疆")
    
    # 测试特别行政区
    sars = get_special_administrative_regions()
    r.assert_length(sars, 2, "应有2个特别行政区")
    sar_names = [p.name for p in sars]
    r.assert_in("香港特别行政区", sar_names, "特别行政区包含香港")
    r.assert_in("澳门特别行政区", sar_names, "特别行政区包含澳门")
    
    # 测试普通省份
    provinces = get_provinces_by_type(RegionType.PROVINCE)
    r.assert_length(provinces, 23, "应有23个省")
    
    return r.report()


def test_get_province_cities():
    """测试获取省份下辖城市"""
    r = TestResultCollector()
    
    # 测试北京城市（直辖市是区）
    beijing_cities = get_province_cities("京")
    r.assert_greater(len(beijing_cities), 0, "北京应有下辖区域")
    r.assert_in("海淀区", beijing_cities, "北京包含海淀区")
    
    # 测试广东城市
    guangdong_cities = get_province_cities("粤")
    r.assert_length(guangdong_cities, 21, "广东应有21个市")
    r.assert_in("广州市", guangdong_cities, "广东包含广州")
    r.assert_in("深圳市", guangdong_cities, "广东包含深圳")
    
    # 测试无效省份
    invalid_cities = get_province_cities("无效")
    r.assert_length(invalid_cities, 0, "无效省份应返回空列表")
    
    return r.report()


def test_get_province_statistics():
    """测试获取省份统计信息"""
    r = TestResultCollector()
    
    # 测试北京统计
    stats = get_province_statistics("京")
    r.assert_not_none(stats, "应返回统计信息")
    r.assert_equal(stats["name"], "北京市", "名称应为北京市")
    r.assert_equal(stats["area_km2"], 16410, "面积应为16410")
    r.assert_greater(stats["city_count"], 0, "城市数量应大于0")
    
    # 测试广东统计
    stats = get_province_statistics("粤")
    r.assert_equal(stats["name"], "广东省", "名称应为广东省")
    r.assert_equal(stats["city_count"], 21, "广东应有21个城市")
    
    # 测试无效省份
    stats = get_province_statistics("无效")
    r.assert_length(stats, 0, "无效省份应返回空字典")
    
    return r.report()


def test_calculate_distance():
    """测试计算邻接距离"""
    r = TestResultCollector()
    
    # 测试相邻省份
    dist = calculate_distance("京", "津")
    r.assert_equal(dist, 1, "北京到天津距离为1")
    
    # 测试不相邻省份
    dist = calculate_distance("京", "粤")
    r.assert_greater(dist, 1, "北京到广东距离应大于1")
    
    # 测试同一省份
    dist = calculate_distance("京", "京")
    r.assert_equal(dist, 0, "同一省份距离为0")
    
    # 测试无法到达（海南）
    dist = calculate_distance("京", "琼")
    r.assert_none(dist, "北京无法到达海南")
    
    # 测试台湾
    dist = calculate_distance("闽", "台")
    r.assert_equal(dist, 1, "福建到台湾距离为1")
    
    # 测试无效省份
    dist = calculate_distance("无效", "京")
    r.assert_none(dist, "无效省份应返回None")
    
    return r.report()


def test_find_route():
    """测试查找路径"""
    r = TestResultCollector()
    
    # 测试相邻路径
    route = find_route("京", "津")
    r.assert_length(route, 2, "北京到天津路径长度为2")
    r.assert_equal(route[0], "京", "起点应为京")
    r.assert_equal(route[1], "津", "终点应为津")
    
    # 测试跨省份路径
    route = find_route("京", "粤")
    r.assert_greater(len(route), 2, "北京到广东路径长度应大于2")
    r.assert_equal(route[0], "京", "起点应为京")
    r.assert_equal(route[-1], "粤", "终点应为粤")
    
    # 测试同一省份
    route = find_route("京", "京")
    r.assert_length(route, 1, "同一省份路径长度为1")
    r.assert_equal(route[0], "京", "应为京")
    
    # 测试无法到达
    route = find_route("京", "琼")
    r.assert_length(route, 0, "无法到达海南")
    
    # 测试无效省份
    route = find_route("无效", "京")
    r.assert_length(route, 0, "无效省份应返回空列表")
    
    return r.report()


def test_validate_province_name():
    """测试验证省份名称"""
    r = TestResultCollector()
    
    # 测试有效简称
    r.assert_true(validate_province_name("京"), "京应有效")
    r.assert_true(validate_province_name("沪"), "沪应有效")
    
    # 测试有效全称
    r.assert_true(validate_province_name("北京市"), "北京市应有效")
    r.assert_true(validate_province_name("广东省"), "广东省应有效")
    
    # 测试无效名称
    r.assert_false(validate_province_name("无效"), "无效应无效")
    r.assert_false(validate_province_name("xyz"), "xyz应无效")
    
    return r.report()


def test_get_province_name_variants():
    """测试获取名称变体"""
    r = TestResultCollector()
    
    # 测试北京
    variants = get_province_name_variants("京")
    r.assert_equal(variants["short_name"], "京", "简称应为京")
    r.assert_equal(variants["full_name"], "北京市", "全称应为北京市")
    r.assert_equal(variants["capital"], "北京", "省会应为北京")
    r.assert_equal(variants["code"], "110000", "代码应为110000")
    
    # 测试香港（有ISO代码）
    variants = get_province_name_variants("港")
    r.assert_equal(variants["iso_code"], "HK", "香港ISO代码应为HK")
    
    # 测试台湾（有ISO代码）
    variants = get_province_name_variants("台")
    r.assert_equal(variants["iso_code"], "TW", "台湾ISO代码应为TW")
    
    # 测试无效省份
    variants = get_province_name_variants("无效")
    r.assert_length(variants, 0, "无效省份应返回空字典")
    
    return r.report()


def test_get_national_statistics():
    """测试获取全国统计"""
    r = TestResultCollector()
    
    stats = get_national_statistics()
    r.assert_equal(stats["total_count"], 34, "总共34个省级行政区")
    r.assert_equal(stats["province_count"], 23, "23个省")
    r.assert_equal(stats["municipality_count"], 4, "4个直辖市")
    r.assert_equal(stats["autonomous_region_count"], 5, "5个自治区")
    r.assert_equal(stats["sar_count"], 2, "2个特别行政区")
    r.assert_greater(stats["total_area_km2"], 0, "总面积应大于0")
    r.assert_greater(stats["total_population_万"], 0, "总人口应大于0")
    
    return r.report()


def test_list_province_short_names():
    """测试获取所有简称"""
    r = TestResultCollector()
    
    shorts = list_province_short_names()
    r.assert_length(shorts, 34, "应有34个简称")
    r.assert_in("京", shorts, "应包含京")
    r.assert_in("沪", shorts, "应包含沪")
    r.assert_in("粤", shorts, "应包含粤")
    
    return r.report()


def test_list_province_names():
    """测试获取所有全称"""
    r = TestResultCollector()
    
    names = list_province_names()
    r.assert_length(names, 34, "应有34个全称")
    r.assert_in("北京市", names, "应包含北京市")
    r.assert_in("广东省", names, "应包含广东省")
    
    return r.report()


def test_export_to_dict():
    """测试导出字典"""
    r = TestResultCollector()
    
    data = export_to_dict()
    r.assert_length(data, 34, "应导出34个省份数据")
    
    # 检查数据结构
    r.assert_not_none(data["京"], "应包含北京数据")
    r.assert_equal(data["京"]["name"], "北京市", "名称应为北京市")
    r.assert_equal(data["京"]["region_type"], "municipality", "类型应为直辖市")
    
    r.assert_not_none(data["粤"], "应包含广东数据")
    r.assert_equal(data["粤"]["region_type"], "province", "类型应为省")
    
    return r.report()


def test_boundary_cases():
    """边界值测试"""
    r = TestResultCollector()
    
    # 空字符串测试
    r.assert_none(get_province_by_short(""), "空简称应返回None")
    r.assert_none(get_province_by_name(""), "空全称应返回None")
    r.assert_none(get_province_by_code(""), "空代码应返回None")
    r.assert_none(get_province_by_capital(""), "空省会应返回None")
    r.assert_none(get_province_by_area_code(""), "空区号应返回None")
    
    # 空关键词搜索
    results = search_province("")
    r.assert_length(results, 34, "空关键词应返回所有省份")
    
    # 单字符搜索
    results = search_province("x")
    r.assert_length(results, 0, "不存在的单字符应返回空")
    
    # 超长字符串
    long_str = "a" * 1000
    r.assert_none(get_province_by_short(long_str), "超长简称应返回None")
    
    # 特殊字符
    special_chars = ["京@", "粤#", "沪!", "川$"]
    for char in special_chars:
        r.assert_none(get_province_by_short(char), f"特殊字符{char}应返回None")
    
    # Unicode测试
    results = search_province("广")
    r.assert_greater(len(results), 0, "Unicode搜索应有结果")
    
    return r.report()


def test_region_type_enum():
    """测试行政区划类型枚举"""
    r = TestResultCollector()
    
    r.assert_equal(RegionType.PROVINCE.value, "province", "省类型值")
    r.assert_equal(RegionType.MUNICIPALITY.value, "municipality", "直辖市类型值")
    r.assert_equal(RegionType.AUTONOMOUS_REGION.value, "autonomous_region", "自治区类型值")
    r.assert_equal(RegionType.SPECIAL_ADMINISTRATIVE_REGION.value, "sar", "特别行政区类型值")
    
    return r.report()


def test_province_area_codes():
    """测试省份区号"""
    r = TestResultCollector()
    
    # 北京区号
    beijing = get_province_by_short("京")
    r.assert_in("010", beijing.area_codes, "北京区号应为010")
    
    # 上海区号
    shanghai = get_province_by_short("沪")
    r.assert_in("021", shanghai.area_codes, "上海区号应为021")
    
    # 广东多个区号
    guangdong = get_province_by_short("粤")
    r.assert_greater(len(guangdong.area_codes), 1, "广东应有多个区号")
    r.assert_in("020", guangdong.area_codes, "广东包含广州区号020")
    r.assert_in("0755", guangdong.area_codes, "广东包含深圳区号0755")
    
    return r.report()


def test_province_population():
    """测试省份人口数据"""
    r = TestResultCollector()
    
    # 大省份人口
    guangdong = get_province_by_short("粤")
    r.assert_greater(guangdong.population, 10000, "广东人口应超过1亿")
    
    # 小省份人口
    macau = get_province_by_short("澳")
    r.assert_greater(macau.population, 0, "澳门人口应大于0")
    r.assert_true(macau.population < 100, "澳门人口应小于100万")
    
    # 验证人口排序
    provinces = get_all_provinces()
    population_sorted = sorted(
        [p for p in provinces if p.population],
        key=lambda p: p.population,
        reverse=True
    )
    r.assert_equal(population_sorted[0].short_name, "粤", "广东人口最多")
    
    return r.report()


def test_province_area():
    """测试省份面积数据"""
    r = TestResultCollector()
    
    # 最大省份
    xinjiang = get_province_by_short("新")
    r.assert_greater(xinjiang.area_km2, 1600000, "新疆面积应超过160万平方公里")
    
    # 最小省份（港澳）
    macau = get_province_by_short("澳")
    r.assert_true(macau.area_km2 < 100, "澳门面积应小于100平方公里")
    
    # 验证面积排序
    provinces = get_all_provinces()
    area_sorted = sorted(provinces, key=lambda p: p.area_km2, reverse=True)
    r.assert_equal(area_sorted[0].short_name, "新", "新疆面积最大")
    
    return r.report()


def run_all_tests():
    """运行所有测试"""
    tests = [
        test_province_data_structure,
        test_get_all_provinces,
        test_get_province_by_short,
        test_get_province_by_name,
        test_get_province_by_code,
        test_get_province_by_capital,
        test_get_province_by_area_code,
        test_get_neighbors,
        test_search_province,
        test_get_provinces_by_type,
        test_get_province_cities,
        test_get_province_statistics,
        test_calculate_distance,
        test_find_route,
        test_validate_province_name,
        test_get_province_name_variants,
        test_get_national_statistics,
        test_list_province_short_names,
        test_list_province_names,
        test_export_to_dict,
        test_boundary_cases,
        test_region_type_enum,
        test_province_area_codes,
        test_province_population,
        test_province_area,
    ]
    
    print("=" * 60)
    print("province_utils 测试")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    for test in tests:
        print(f"\n运行: {test.__name__}")
        try:
            if test():
                total_passed += 1
            else:
                total_failed += 1
        except Exception as e:
            print(f"  异常: {e}")
            total_failed += 1
    
    print("\n" + "=" * 60)
    print(f"总计: {len(tests)} 个测试函数")
    print(f"通过: {total_passed}")
    print(f"失败: {total_failed}")
    print("=" * 60)
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)