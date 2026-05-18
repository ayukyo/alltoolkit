"""
province_utils 使用示例

展示各种用法：
- 省份查询
- 相邻省份
- 路径查找
- 统计信息
- 导出数据
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from province_utils.mod import (
    get_all_provinces,
    get_province_by_short,
    get_province_by_name,
    get_province_by_code,
    get_province_by_capital,
    get_province_by_area_code,
    get_neighbors,
    search_province,
    get_municipalities,
    get_autonomous_regions,
    get_special_administrative_regions,
    get_province_cities,
    get_province_statistics,
    calculate_distance,
    find_route,
    get_province_name_variants,
    get_national_statistics,
    list_province_short_names,
    export_to_dict,
)


def example_basic_query():
    """基本查询示例"""
    print("\n" + "=" * 50)
    print("基本查询示例")
    print("=" * 50)
    
    # 通过简称查询
    beijing = get_province_by_short("京")
    print(f"简称'京' -> {beijing.name}, 省会: {beijing.capital}")
    
    # 通过全称查询
    guangdong = get_province_by_name("广东省")
    print(f"全称'广东省' -> 简称: {guangdong.short_name}, 省会: {guangdong.capital}")
    
    # 通过行政代码查询
    shanghai = get_province_by_code("310000")
    print(f"代码'310000' -> {shanghai.name}")
    
    # 通过省会查询
    sichuan = get_province_by_capital("成都市")
    print(f"省会'成都市' -> {sichuan.name}")
    
    # 通过区号查询
    province = get_province_by_area_code("020")
    print(f"区号'020' -> {province.name} ({province.capital})")


def example_search():
    """搜索示例"""
    print("\n" + "=" * 50)
    print("搜索示例")
    print("=" * 50)
    
    # 搜索包含"州"的省份
    results = search_province("州")
    print(f"搜索'州'找到 {len(results)} 个省份:")
    for p in results[:5]:
        print(f"  - {p.name}")
    
    # 搜索省会
    results = search_province("成都")
    print(f"搜索'成都': {results[0].name}")


def example_neighbors():
    """相邻省份示例"""
    print("\n" + "=" * 50)
    print("相邻省份示例")
    print("=" * 50)
    
    # 北京相邻省份
    neighbors = get_neighbors("京")
    print(f"北京相邻省份: {[n.name for n in neighbors]}")
    
    # 四川相邻省份（内陆多相邻）
    neighbors = get_neighbors("川")
    print(f"四川相邻省份 ({len(neighbors)} 个): {[n.name for n in neighbors]}")
    
    # 海南无相邻
    neighbors = get_neighbors("琼")
    print(f"海南相邻省份: {neighbors} (岛屿省份)")


def example_administrative_types():
    """行政区划类型示例"""
    print("\n" + "=" * 50)
    print("行政区划类型示例")
    print("=" * 50)
    
    # 直辖市
    mun = get_municipalities()
    print(f"直辖市: {[m.name for m in mun]}")
    
    # 自治区
    auto = get_autonomous_regions()
    print(f"自治区: {[a.name for a in auto]}")
    
    # 特别行政区
    sars = get_special_administrative_regions()
    print(f"特别行政区: {[s.name for s in sars]}")


def example_cities():
    """城市列表示例"""
    print("\n" + "=" * 50)
    print("城市列表示例")
    print("=" * 50)
    
    # 广东城市
    cities = get_province_cities("粤")
    print(f"广东省下辖 {len(cities)} 个市:")
    print(f"  {cities[:5]}...")
    
    # 北京区
    cities = get_province_cities("京")
    print(f"北京市下辖 {len(cities)} 个区:")
    print(f"  {cities[:5]}...")


def example_statistics():
    """统计信息示例"""
    print("\n" + "=" * 50)
    print("统计信息示例")
    print("=" * 50)
    
    # 广东省统计
    stats = get_province_statistics("粤")
    print(f"广东省统计:")
    print(f"  面积: {stats['area_km2']} km²")
    print(f"  人口: {stats['population_万']} 万")
    print(f"  市数量: {stats['city_count']}")
    print(f"  相邻省: {stats['neighbor_count']}")
    
    # 全国统计
    national = get_national_statistics()
    print(f"\n全国统计:")
    print(f"  省级行政区总数: {national['total_count']}")
    print(f"  省份: {national['province_count']}")
    print(f"  直辖市: {national['municipality_count']}")
    print(f"  自治区: {national['autonomous_region_count']}")
    print(f"  特别行政区: {national['sar_count']}")
    print(f"  总面积: {national['total_area_km2']} km²")
    print(f"  总人口: {national['total_population_万']} 万")


def example_route():
    """路径查找示例"""
    print("\n" + "=" * 50)
    print("路径查找示例")
    print("=" * 50)
    
    # 北京到天津（相邻）
    route = find_route("京", "津")
    print(f"北京 -> 天津: {[get_province_by_short(s).name for s in route]}")
    
    # 北京到广东（跨省）
    route = find_route("京", "粤")
    print(f"北京 -> 广东 ({len(route)}步): {[get_province_by_short(s).name for s in route]}")
    
    # 计算距离
    dist = calculate_distance("京", "沪")
    print(f"北京到上海距离: {dist} 步")
    
    dist = calculate_distance("川", "粤")
    print(f"四川到广东距离: {dist} 步")


def example_name_variants():
    """名称变体示例"""
    print("\n" + "=" * 50)
    print("名称变体示例")
    print("=" * 50)
    
    # 北京
    variants = get_province_name_variants("京")
    print(f"北京名称变体:")
    for key, value in variants.items():
        print(f"  {key}: {value}")
    
    # 香港（有ISO代码）
    variants = get_province_name_variants("港")
    print(f"\n香港名称变体:")
    for key, value in variants.items():
        print(f"  {key}: {value}")


def example_export():
    """数据导出示例"""
    print("\n" + "=" * 50)
    print("数据导出示例")
    print("=" * 50)
    
    # 导出为字典
    data = export_to_dict()
    print(f"导出 {len(data)} 个省份数据")
    
    # 查看北京数据
    print(f"北京数据:")
    beijing_data = data["京"]
    print(f"  名称: {beijing_data['name']}")
    print(f"  类型: {beijing_data['region_type']}")
    print(f"  面积: {beijing_data['area_km2']} km²")
    print(f"  区号: {beijing_data['area_codes']}")


def example_list_names():
    """列出所有名称示例"""
    print("\n" + "=" * 50)
    print("列出所有名称示例")
    print("=" * 50)
    
    # 所有简称
    shorts = list_province_short_names()
    print(f"所有简称 ({len(shorts)} 个): {shorts}")
    
    # 所有全称
    names = list_province_names()
    print(f"\n所有全称 ({len(names)} 个):")
    print(f"  {names}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("province_utils 使用示例")
    print("=" * 60)
    
    example_basic_query()
    example_search()
    example_neighbors()
    example_administrative_types()
    example_cities()
    example_statistics()
    example_route()
    example_name_variants()
    example_export()
    example_list_names()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()