#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Country Utilities Examples

Demonstrates various use cases of country_utils module.

Author: AllToolkit
License: MIT
"""

import sys
import os
# Add parent directory and workspace to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.dirname(parent_dir))

from country_utils.mod import (
    get_country,
    get_by_alpha2,
    get_by_alpha3,
    get_by_numeric,
    get_by_name,
    search_countries,
    get_all_countries,
    get_countries_by_continent,
    get_countries_by_region,
    validate_alpha2,
    validate_alpha3,
    validate_numeric,
    alpha2_to_alpha3,
    alpha3_to_alpha2,
    alpha2_to_numeric,
    numeric_to_alpha2,
    get_flag_emoji,
    get_calling_code,
    get_currency,
    get_continents,
    get_regions,
)


def example_basic_lookup():
    """基本查询示例"""
    print("=" * 60)
    print("基本查询示例")
    print("=" * 60)
    
    # 通过不同代码格式查询
    print("\n通过 alpha-2 查询:")
    us = get_by_alpha2("US")
    print(f"  US → {us.name_en} ({us.name_zh}) {us.flag_emoji}")
    print(f"      Alpha-3: {us.alpha3}, Numeric: {us.numeric}")
    print(f"      电话: {us.calling_code}, 货币: {us.currency}")
    
    print("\n通过 alpha-3 查询:")
    chn = get_by_alpha3("CHN")
    print(f"  CHN → {chn.name_en} ({chn.name_zh}) {chn.flag_emoji}")
    
    print("\n通过 numeric 查询:")
    jpn = get_by_numeric("392")
    print(f"  392 → {jpn.name_en} ({jpn.name_zh}) {jpn.flag_emoji}")
    
    print("\n通过名称查询:")
    germany = get_by_name("德国")
    print(f"  德国 → {germany.alpha2} {germany.name_en} {germany.flag_emoji}")
    
    france = get_by_name("France")
    print(f"  France → {france.alpha2} {france.name_zh} {france.flag_emoji}")


def example_search():
    """搜索示例"""
    print("\n" + "=" * 60)
    print("搜索示例")
    print("=" * 60)
    
    print("\n搜索包含 'United' 的国家:")
    results = search_countries("United", limit=10)
    for c in results:
        print(f"  {c.flag_emoji} {c.name_en} ({c.name_zh})")
    
    print("\n搜索中文 '韩':")
    results = search_countries("韩")
    for c in results:
        print(f"  {c.flag_emoji} {c.name_en} ({c.name_zh})")
    
    print("\n搜索 'land':")
    results = search_countries("land", limit=8)
    for c in results:
        print(f"  {c.flag_emoji} {c.name_en}")


def example_continent_region():
    """大陆和区域示例"""
    print("\n" + "=" * 60)
    print("大陆和区域示例")
    print("=" * 60)
    
    print("\n亚洲国家 (部分):")
    asia = get_countries_by_continent("Asia")
    for c in asia[:10]:
        print(f"  {c.flag_emoji} {c.name_zh} ({c.alpha2})")
    print(f"  ... 共 {len(asia)} 个国家")
    
    print("\n东亚国家:")
    east_asia = get_countries_by_region("East Asia")
    for c in east_asia:
        print(f"  {c.flag_emoji} {c.name_zh} ({c.alpha2}) - 电话: {c.calling_code}")
    
    print("\n东南亚国家:")
    southeast_asia = get_countries_by_region("Southeast Asia")
    for c in southeast_asia[:5]:
        print(f"  {c.flag_emoji} {c.name_zh} ({c.alpha2}) - 货币: {c.currency}")
    print(f"  ... 共 {len(southeast_asia)} 个国家")


def example_validation():
    """验证示例"""
    print("\n" + "=" * 60)
    print("验证示例")
    print("=" * 60)
    
    codes = ["US", "XX", "USA", "XXX", "840", "000"]
    
    print("\n验证 alpha-2 代码:")
    for code in codes[:2]:
        result = validate_alpha2(code)
        print(f"  validate_alpha2('{code}'): {result}")
    
    print("\n验证 alpha-3 代码:")
    for code in codes[2:4]:
        result = validate_alpha3(code)
        print(f"  validate_alpha3('{code}'): {result}")
    
    print("\n验证 numeric 代码:")
    for code in codes[4:]:
        result = validate_numeric(code)
        print(f"  validate_numeric('{code}'): {result}")


def example_conversion():
    """代码转换示例"""
    print("\n" + "=" * 60)
    print("代码转换示例")
    print("=" * 60)
    
    codes = ["US", "CN", "JP", "GB", "DE"]
    
    print("\nAlpha-2 → Alpha-3 → Numeric:")
    for code in codes:
        alpha3 = alpha2_to_alpha3(code)
        numeric = alpha2_to_numeric(code)
        print(f"  {code} → {alpha3} → {numeric}")
    
    print("\n反向转换:")
    numeric_codes = ["840", "156", "392"]
    for code in numeric_codes:
        alpha2 = numeric_to_alpha2(code)
        alpha3 = alpha2_to_alpha3(alpha2)
        country = get_by_alpha2(alpha2)
        print(f"  {code} → {alpha2} → {alpha3} ({country.name_zh})")


def example_flag_emoji():
    """国旗表情示例"""
    print("\n" + "=" * 60)
    print("国旗表情示例")
    print("=" * 60)
    
    # G8 国家国旗
    g8 = ["US", "JP", "DE", "FR", "GB", "IT", "CA", "RU"]
    print("\nG8 国家国旗:")
    flags = " ".join([get_flag_emoji(c) for c in g8])
    print(f"  {flags}")
    
    # 东亚国旗
    east_asia = ["CN", "JP", "KR", "TW", "HK", "MO"]
    print("\n东亚国旗:")
    flags = " ".join([get_flag_emoji(c) for c in east_asia])
    print(f"  {flags}")
    
    # 欧盟主要国家
    eu = ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "PT", "GR"]
    print("\n欧盟主要国家:")
    flags = " ".join([get_flag_emoji(c) for c in eu])
    print(f"  {flags}")


def example_phone_currency():
    """电话和货币示例"""
    print("\n" + "=" * 60)
    print("电话和货币示例")
    print("=" * 60)
    
    countries = ["US", "CN", "JP", "KR", "GB", "DE", "FR", "AU"]
    
    print("\n电话区号和货币:")
    for code in countries:
        country = get_by_alpha2(code)
        print(f"  {country.flag_emoji} {country.name_zh}: 电话 {country.calling_code}, 货币 {country.currency}")


def example_statistics():
    """统计示例"""
    print("\n" + "=" * 60)
    print("统计示例")
    print("=" * 60)
    
    all_countries = get_all_countries()
    print(f"\n国家总数: {len(all_countries)}")
    
    print("\n各大洲国家数:")
    for continent in sorted(get_continents()):
        count = len(get_countries_by_continent(continent))
        print(f"  {continent}: {count} 个国家")
    
    print("\n各区域国家数:")
    regions = sorted(get_regions())
    for region in regions[:8]:
        count = len(get_countries_by_region(region))
        print(f"  {region}: {count} 个国家")


def example_data_export():
    """数据导出示例"""
    print("\n" + "=" * 60)
    print("数据导出示例")
    print("=" * 60)
    
    print("\n导出东亚国家数据 (JSON 格式):")
    east_asia = get_countries_by_region("East Asia")
    
    import json
    data = [c.to_dict() for c in east_asia[:3]]
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """运行所有示例"""
    example_basic_lookup()
    example_search()
    example_continent_region()
    example_validation()
    example_conversion()
    example_flag_emoji()
    example_phone_currency()
    example_statistics()
    example_data_export()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()