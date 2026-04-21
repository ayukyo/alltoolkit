#!/usr/bin/env python3
"""
Zodiac Utils 使用示例

演示西方星座和中国生肖工具的各种用法。
"""

from datetime import datetime, date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ZodiacUtils, ChineseZodiacUtils, Zodiac, ChineseZodiac,
    Element, Quality,
    get_zodiac, get_zodiac_from_date,
    get_chinese_zodiac, get_chinese_zodiac_from_date,
    calculate_zodiac_compatibility, calculate_chinese_zodiac_compatibility
)


def print_separator(title: str = ""):
    """打印分隔线"""
    print("\n" + "=" * 50)
    if title:
        print(f"  {title}")
        print("=" * 50)


def example_basic_zodiac():
    """基本星座判断示例"""
    print_separator("基本星座判断")

    # 方式1：使用月份和日期
    zodiac1 = ZodiacUtils.get_zodiac(7, 15)
    print(f"7月15日: {zodiac1}")

    # 方式2：使用日期字符串
    zodiac2 = get_zodiac_from_date("1990-07-15")
    print(f"1990年7月15日: {zodiac2}")

    # 方式3：使用 datetime 对象
    birth_date = datetime(1985, 12, 25)
    zodiac3 = ZodiacUtils.get_zodiac_from_date(birth_date)
    print(f"1985年12月25日: {zodiac3}")

    # 方式4：使用时间戳
    timestamp = datetime(2000, 2, 29).timestamp()
    zodiac4 = ZodiacUtils.get_zodiac_from_date(timestamp)
    print(f"2000年2月29日（闰年）: {zodiac4}")


def example_zodiac_info():
    """星座详细信息示例"""
    print_separator("星座详细信息")

    # 获取狮子座详细信息
    info = ZodiacUtils.get_zodiac_info(Zodiac.LEO)
    print(f"\n♌ {info['name']} ({info['english_name']})")
    print(f"   日期范围: {info['date_range']}")
    print(f"   元素: {info['element']}")
    print(f"   属性: {info['quality']}")
    print(f"   守护星: {info['ruling_planet']}")
    print(f"   幸运数字: {', '.join(map(str, info['lucky_numbers']))}")
    print(f"   幸运颜色: {', '.join(info['lucky_colors'])}")
    print(f"   性格特点: {', '.join(info['personality_traits'])}")


def example_zodiac_by_element():
    """按元素筛选星座示例"""
    print_separator("按元素分类")

    elements = ["火象", "土象", "风象", "水象"]
    for element in elements:
        zodiacs = ZodiacUtils.get_zodiacs_by_element(element)
        print(f"\n{element}星座: {', '.join(zodiacs)}")


def example_zodiac_by_quality():
    """按属性筛选星座示例"""
    print_separator("按属性分类")

    qualities = ["基本宫", "固定宫", "变动宫"]
    for quality in qualities:
        zodiacs = ZodiacUtils.get_zodiacs_by_quality(quality)
        print(f"\n{quality}: {', '.join(zodiacs)}")


def example_zodiac_compatibility():
    """星座兼容性示例"""
    print_separator("星座兼容性分析")

    # 查看所有星座的最佳配对
    print("\n最佳配对 TOP 3:")
    for zodiac in ZodiacUtils.get_all_zodiacs()[:4]:  # 只显示前4个
        matches = ZodiacUtils.get_best_matches(zodiac, 3)
        match_str = ", ".join([f"{m['zodiac']}({m['score']}%)" for m in matches])
        print(f"  {zodiac}: {match_str}")

    # 详细兼容性分析
    print("\n详细兼容性分析:")
    pairs = [
        (Zodiac.ARIES, Zodiac.LEO),
        (Zodiac.TAURUS, Zodiac.SCORPIO),
        (Zodiac.GEMINI, Zodiac.SAGITTARIUS),
    ]
    for z1, z2 in pairs:
        result = ZodiacUtils.calculate_compatibility(z1, z2)
        print(f"\n  {z1} ♡ {z2}")
        print(f"    兼容度: {result['score']}%")
        print(f"    等级: {result['level']}")
        print(f"    描述: {result['description']}")


def example_basic_chinese_zodiac():
    """基本生肖判断示例"""
    print_separator("基本生肖判断")

    # 方式1：使用年份
    zodiac1 = ChineseZodiacUtils.get_zodiac(1990)
    print(f"1990年: {zodiac1}")

    # 方式2：使用日期字符串
    zodiac2 = get_chinese_zodiac_from_date("2000-06-15")
    print(f"2000年: {zodiac2}")

    # 方式3：使用 datetime 对象
    birth_date = datetime(1988, 8, 8)
    zodiac3 = ChineseZodiacUtils.get_zodiac_from_date(birth_date)
    print(f"1988年: {zodiac3}")


def example_chinese_zodiac_info():
    """生肖详细信息示例"""
    print_separator("生肖详细信息")

    # 获取龙年信息
    info = ChineseZodiacUtils.get_zodiac_info(ChineseZodiac.DRAGON)
    print(f"\n🐲 {info['name']}")
    print(f"   排序: 第{info['order']}位")
    print(f"   性格: {', '.join(info['personality'])}")
    print(f"   优点: {', '.join(info['strengths'])}")
    print(f"   缺点: {', '.join(info['weaknesses'])}")
    print(f"   最佳配对: {', '.join(info['best_matches'])}")
    print(f"   幸运数字: {', '.join(map(str, info['lucky_numbers']))}")
    print(f"   幸运颜色: {', '.join(info['lucky_colors'])}")


def example_ganzhi_wuxing():
    """干支纪年和五行示例"""
    print_separator("干支纪年与五行")

    # 干支纪年
    print("\n干支纪年:")
    for year in [1984, 2000, 2024, 2025, 2026]:
        ganzhi = ChineseZodiacUtils.get_ganzhi(year)
        zodiac = ChineseZodiacUtils.get_zodiac(year)
        print(f"  {year}年: {ganzhi}年 ({zodiac}年)")

    # 五行属性
    print("\n五行属性:")
    for year in range(2024, 2034):
        wuxing = ChineseZodiacUtils.get_wuxing(year)
        zodiac = ChineseZodiacUtils.get_zodiac(year)
        print(f"  {year}年 ({zodiac}年): {wuxing}")


def example_chinese_zodiac_compatibility():
    """生肖兼容性示例"""
    print_separator("生肖兼容性分析")

    # 测试各种配对
    pairs = [
        (ChineseZodiac.RAT, ChineseZodiac.DRAGON),    # 六合
        (ChineseZodiac.RAT, ChineseZodiac.HORSE),     # 相冲
        (ChineseZodiac.TIGER, ChineseZodiac.HORSE),   # 三合
        (ChineseZodiac.RABBIT, ChineseZodiac.GOAT),   # 三合
    ]

    for z1, z2 in pairs:
        result = ChineseZodiacUtils.calculate_compatibility(z1, z2)
        print(f"\n  {z1} ♡ {z2}")
        print(f"    兼容度: {result['score']}%")
        print(f"    等级: {result['level']}")
        print(f"    描述: {result['description']}")


def example_benming_nian():
    """本命年示例"""
    print_separator("本命年判断")

    current_year = datetime.now().year
    current_zodiac = ChineseZodiacUtils.get_zodiac(current_year)
    print(f"\n当前年份: {current_year}年 ({current_zodiac}年)")

    # 查找未来10年内的本命年
    print(f"\n未来10年本命年 ({current_zodiac}):")
    years = ChineseZodiacUtils.get_zodiac_year(current_zodiac)
    future_years = [y for y in years if y >= current_year][:3]
    for year in future_years:
        zodiac, is_benming = ChineseZodiacUtils.get_benming_nian(year)
        print(f"  {year}年: {zodiac}年 {'(本命年)' if is_benming else ''}")


def example_all_zodiacs():
    """所有星座/生肖列表"""
    print_separator("所有星座与生肖")

    # 西方星座
    print("\n西方星座:")
    zodiacs = ZodiacUtils.get_all_zodiacs()
    for i, zodiac in enumerate(zodiacs, 1):
        info = ZodiacUtils.get_zodiac_info(zodiac)
        print(f"  {i:2d}. {info['symbol']} {zodiac} ({info['english_name']})")

    # 中国生肖
    print("\n中国生肖:")
    chinese_zodiacs = ChineseZodiacUtils.get_all_zodiacs()
    for i, zodiac in enumerate(chinese_zodiacs, 1):
        print(f"  {i:2d}. {zodiac}")


def example_user_profile():
    """用户档案示例"""
    print_separator("根据出生日期生成档案")

    birth_date = "1990-07-15"

    # 西方星座
    zodiac = get_zodiac_from_date(birth_date)
    zodiac_info = ZodiacUtils.get_zodiac_info(zodiac)

    # 中国生肖
    chinese_zodiac = get_chinese_zodiac_from_date(birth_date)
    chinese_info = ChineseZodiacUtils.get_zodiac_info(chinese_zodiac)

    # 干支
    year = int(birth_date[:4])
    ganzhi = ChineseZodiacUtils.get_ganzhi(year)
    wuxing = ChineseZodiacUtils.get_wuxing(year)

    print(f"\n📅 出生日期: {birth_date}")
    print(f"\n⭐ 西方星座: {zodiac_info['symbol']} {zodiac}")
    print(f"   元素: {zodiac_info['element']}")
    print(f"   属性: {zodiac_info['quality']}")
    print(f"   守护星: {zodiac_info['ruling_planet']}")
    print(f"   性格: {', '.join(zodiac_info['personality_traits'])}")

    print(f"\n🐲 中国生肖: {chinese_zodiac}")
    print(f"   干支: {ganzhi}年")
    print(f"   五行: {wuxing}")
    print(f"   性格: {', '.join(chinese_info['personality'])}")

    # 最佳配对
    print(f"\n💕 最佳配对:")
    matches = ZodiacUtils.get_best_matches(zodiac, 2)
    print(f"   星座: {matches[0]['zodiac']}、{matches[1]['zodiac']}")
    print(f"   生肖: {', '.join(chinese_info['best_matches'][:2])}")


def main():
    """运行所有示例"""
    example_basic_zodiac()
    example_zodiac_info()
    example_zodiac_by_element()
    example_zodiac_by_quality()
    example_zodiac_compatibility()
    example_basic_chinese_zodiac()
    example_chinese_zodiac_info()
    example_ganzhi_wuxing()
    example_chinese_zodiac_compatibility()
    example_benming_nian()
    example_all_zodiacs()
    example_user_profile()

    print_separator()
    print("\n✨ 所有示例运行完成！\n")


if __name__ == "__main__":
    main()