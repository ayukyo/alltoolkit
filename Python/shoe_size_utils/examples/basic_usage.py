#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shoe Size Utilities Basic Usage Examples
=======================================================
Simple examples demonstrating how to use the shoe_size_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shoe_size_utils.mod import (
    convert_size,
    get_all_conversions,
    recommend_size,
    generate_size_chart,
    validate_size,
    format_size_string,
    SizeSystem,
    Gender,
    AgeGroup,
)


def example_basic_conversion():
    """基本尺码转换示例"""
    print("=" * 60)
    print("基本尺码转换示例")
    print("=" * 60)
    
    # EU 转 US 男码
    eu_size = 42
    us_men = convert_size(eu_size, SizeSystem.EU, SizeSystem.US, Gender.MALE)
    print(f"EU {eu_size} → US {us_men} (Men)")
    
    # EU 转 US 女码
    us_women = convert_size(eu_size, SizeSystem.EU, SizeSystem.US, Gender.FEMALE)
    print(f"EU {eu_size} → US {us_women} (Women)")
    
    # US 转 EU
    us_size = 8.5
    eu = convert_size(us_size, SizeSystem.US, SizeSystem.EU, Gender.MALE)
    print(f"US {us_size} (Men) → EU {eu}")
    
    # EU 转 CN (厘米)
    cn = convert_size(eu_size, SizeSystem.EU, SizeSystem.CN)
    print(f"EU {eu_size} → CN {cn}cm")
    
    # EU 转 UK
    uk = convert_size(eu_size, SizeSystem.EU, SizeSystem.UK)
    print(f"EU {eu_size} → UK {uk}")
    
    # EU 转 KR (毫米)
    kr = convert_size(eu_size, SizeSystem.EU, SizeSystem.KR)
    print(f"EU {eu_size} → KR {kr}mm")


def example_full_conversion():
    """完整转换示例"""
    print("\n" + "=" * 60)
    print("完整转换示例 - 获取所有尺码")
    print("=" * 60)
    
    # 成人男性 EU 42
    result = get_all_conversions(42, SizeSystem.EU, Gender.MALE)
    
    print(f"\n原始尺码: EU {result.original_size} ({result.original_gender})")
    print(f"脚长: {result.foot_length_cm}cm ({result.foot_length_inch}in)")
    print(f"分类: {result.size_category_cn} ({result.size_category_en})")
    print(f"\n转换结果:")
    print(f"  CN: {result.conversions['CN']}cm")
    print(f"  EU: {result.conversions['EU']}")
    print(f"  US Men: {result.conversions['US_men']}")
    print(f"  US Women: {result.conversions['US_women']}")
    print(f"  UK: {result.conversions['UK']}")
    print(f"  AU: {result.conversions['AU']}")
    print(f"  JP: {result.conversions['JP']}cm")
    print(f"  KR: {result.conversions['KR']}mm")
    print(f"  BR: {result.conversions['BR']}")
    print(f"  MX: {result.conversions['MX']}")
    print(f"  TW: {result.conversions['TW']}")
    
    print(f"\n推荐:")
    for rec in result.recommendations:
        print(f"  - {rec}")


def example_women_sizes():
    """女性尺码示例"""
    print("\n" + "=" * 60)
    print("女性尺码示例")
    print("=" * 60)
    
    # 成人女性 EU 38
    result = get_all_conversions(38, SizeSystem.EU, Gender.FEMALE)
    
    print(f"\nEU {result.original_size} (女性成人):")
    print(f"  US Women: {result.conversions['US_women']}")
    print(f"  US Men: {result.conversions['US_men']} (对比)")
    print(f"  UK: {result.conversions['UK']}")
    print(f"  CN: {result.conversions['CN']}cm")
    
    # 女性尺码差异说明
    print(f"\n注意: US 女码比男码大约 1.5")


def example_child_sizes():
    """儿童尺码示例"""
    print("\n" + "=" * 60)
    print("儿童尺码示例")
    print("=" * 60)
    
    # 儿童 EU 28
    result = get_all_conversions(28, SizeSystem.EU, Gender.MALE, AgeGroup.CHILD)
    
    print(f"\nEU {result.original_size} (儿童):")
    print(f"  US Children: {result.conversions['US']}")
    print(f"  UK Children: {result.conversions['UK']}")
    print(f"  CN: {result.conversions['CN']}cm")
    print(f"  JP: {result.conversions['JP']}cm")
    
    print(f"\n推荐:")
    for rec in result.recommendations:
        print(f"  - {rec}")


def example_size_recommendation():
    """尺码推荐示例"""
    print("\n" + "=" * 60)
    print("尺码推荐示例 - 根据脚长推荐")
    print("=" * 60)
    
    # 脚长 26cm，推荐 US 尺码
    rec = recommend_size(26.0, SizeSystem.US, Gender.MALE)
    print(f"\n脚长 26cm:")
    print(f"  推荐 US 尺码: {rec.recommended_size}")
    print(f"  尺码范围: {rec.size_range[0]}-{rec.size_range[1]}")
    print(f"  舒适余量: {rec.comfort_margin_cm}cm")
    
    # 带品牌调整
    print(f"\n考虑品牌调整:")
    rec_nike = recommend_size(26.0, SizeSystem.US, Gender.MALE, brand='Nike')
    print(f"  Nike 推荐: {rec_nike.recommended_size}")
    for note in rec_nike.notes:
        print(f"    - {note}")
    
    rec_converse = recommend_size(26.0, SizeSystem.US, Gender.MALE, brand='Converse')
    print(f"  Converse 推荐: {rec_converse.recommended_size}")
    
    rec_hoka = recommend_size(26.0, SizeSystem.US, Gender.MALE, brand='Hoka')
    print(f"  Hoka 推荐: {rec_hoka.recommended_size}")


def example_size_chart():
    """尺码对照表示例"""
    print("\n" + "=" * 60)
    print("尺码对照表示例")
    print("=" * 60)
    
    # 生成部分尺码表
    chart = generate_size_chart(start_cm=24.0, end_cm=27.0, step_cm=0.5)
    
    print("\n成人男性尺码对照表 (24-27cm):")
    print("-" * 70)
    print("脚长(cm) | CN | EU | US(Men) | US(Women) | UK | JP | KR(mm)")
    print("-" * 70)
    for row in chart:
        print(f"{row['foot_length_cm']} | {row['CN']} | {int(row['EU'])} | {row['US_men']} | {row['US_women']} | {row['UK']} | {row['JP']} | {row['KR']}")


def example_validation():
    """尺码验证示例"""
    print("\n" + "=" * 60)
    print("尺码验证示例")
    print("=" * 60)
    
    # 有效尺码
    valid, reason = validate_size(42, SizeSystem.EU)
    print(f"\nEU 42: {reason}")
    
    # 过大尺码
    valid, reason = validate_size(60, SizeSystem.EU)
    print(f"EU 60: {reason}")
    
    # 过小尺码
    valid, reason = validate_size(25, SizeSystem.EU)
    print(f"EU 25: {reason}")
    
    # US 尺码验证
    valid, reason = validate_size(8, SizeSystem.US, Gender.MALE)
    print(f"US 8 (Men): {reason}")
    
    valid, reason = validate_size(20, SizeSystem.US, Gender.MALE)
    print(f"US 20 (Men): {reason}")


def example_formatting():
    """尺码格式化示例"""
    print("\n" + "=" * 60)
    print("尺码格式化示例")
    print("=" * 60)
    
    print(f"\n格式化输出:")
    print(f"  {format_size_string(8.5, SizeSystem.US, Gender.MALE)}")
    print(f"  {format_size_string(7.5, SizeSystem.US, Gender.FEMALE)}")
    print(f"  {format_size_string(42, SizeSystem.EU)}")
    print(f"  {format_size_string(7.5, SizeSystem.UK)}")
    print(f"  {format_size_string(245, SizeSystem.KR)}")
    print(f"  {format_size_string(24.5, SizeSystem.CN)}")
    print(f"  {format_size_string(24.5, SizeSystem.JP)}")


def example_different_systems():
    """不同鞋码系统示例"""
    print("\n" + "=" * 60)
    print("不同鞋码系统示例")
    print("=" * 60)
    
    # 同一脚长在不同系统的表示
    foot_length = 25.5
    
    print(f"\n脚长 {foot_length}cm 在不同系统的表示:")
    
    cn = convert_size(foot_length, SizeSystem.CN, SizeSystem.CN)
    print(f"  CN: {cn}cm (直接使用脚长)")
    
    eu = convert_size(foot_length, SizeSystem.CN, SizeSystem.EU)
    print(f"  EU: {eu} (Paris point 系统)")
    
    us_men = convert_size(foot_length, SizeSystem.CN, SizeSystem.US, Gender.MALE)
    print(f"  US Men: {us_men} (Barleycorn 系统)")
    
    us_women = convert_size(foot_length, SizeSystem.CN, SizeSystem.US, Gender.FEMALE)
    print(f"  US Women: {us_women}")
    
    uk = convert_size(foot_length, SizeSystem.CN, SizeSystem.UK)
    print(f"  UK: {uk}")
    
    jp = convert_size(foot_length, SizeSystem.CN, SizeSystem.JP)
    print(f"  JP: {jp}cm (与 CN 相同)")
    
    kr = convert_size(foot_length, SizeSystem.CN, SizeSystem.KR)
    print(f"  KR: {kr}mm (毫米单位)")
    
    br = convert_size(foot_length, SizeSystem.CN, SizeSystem.BR)
    print(f"  BR: {br}")
    
    mx = convert_size(foot_length, SizeSystem.CN, SizeSystem.MX)
    print(f"  MX: {mx}")
    
    tw = convert_size(foot_length, SizeSystem.CN, SizeSystem.TW)
    print(f"  TW: {tw}")


def main():
    """运行所有示例"""
    example_basic_conversion()
    example_full_conversion()
    example_women_sizes()
    example_child_sizes()
    example_size_recommendation()
    example_size_chart()
    example_validation()
    example_formatting()
    example_different_systems()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()