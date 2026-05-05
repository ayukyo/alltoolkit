"""
护照工具使用示例
演示护照号码验证和MRZ解析的各种用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PassportUtils,
    PassportType,
    Country,
    validate_passport,
    parse_mrz,
    is_passport_expired,
    get_passport_formats,
    PassportValidationResult,
    MRZParseResult
)


def example_basic_validation():
    """示例1: 基础护照号码验证"""
    print("=" * 60)
    print("示例1: 基础护照号码验证")
    print("=" * 60)
    
    # 验证中国护照
    passports = [
        ("P1234567", Country.CHINA, "中国普通护照"),
        ("D1234567", Country.CHINA, "中国外交护照"),
        ("S1234567", Country.CHINA, "中国公务护照"),
        ("E12345678", Country.CHINA, "中国公务普通护照"),
        ("G12345678", Country.CHINA, "中国旧版普通护照"),
    ]
    
    for passport_num, country, desc in passports:
        result = validate_passport(passport_num, country)
        print(f"\n{desc} ({passport_num}):")
        print(f"  有效: {result.is_valid}")
        print(f"  类型: {result.passport_type.value}")
        print(f"  消息: {result.message}")


def example_country_specific_validation():
    """示例2: 指定国家验证"""
    print("\n" + "=" * 60)
    print("示例2: 指定国家验证护照号码")
    print("=" * 60)
    
    # 验证美国护照
    result = validate_passport("123456789", Country.USA)
    print(f"\n美国护照 (123456789):")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    print(f"  格式: {result.format_pattern}")
    
    # 验证日本护照
    result = validate_passport("AB1234567", Country.JAPAN)
    print(f"\n日本护照 (AB1234567):")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    
    # 验证德国护照
    result = validate_passport("C12345678", Country.GERMANY)
    print(f"\n德国护照 (C12345678):")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")


def example_auto_detection():
    """示例3: 自动检测护照国家"""
    print("\n" + "=" * 60)
    print("示例3: 自动检测护照国家")
    print("=" * 60)
    
    # 自动检测各种护照
    test_passports = [
        "P1234567",       # 中国
        "TA1234567",      # 日本
        "C12345678",      # 德国
        "12AB34567",      # 法国
        "AB12345678",     # 韩国
        "A1234567",       # 澳大利亚
        "E1234567A",      # 新加坡
        "UNKNOWN123",     # 未知
    ]
    
    for passport_num in test_passports:
        result = validate_passport(passport_num)
        print(f"\n护照号码: {passport_num}")
        print(f"  有效: {result.is_valid}")
        print(f"  国家: {result.country.value}")
        print(f"  类型: {result.passport_type.value}")
        print(f"  消息: {result.message}")


def example_mrz_parsing():
    """示例4: MRZ解析"""
    print("\n" + "=" * 60)
    print("示例4: MRZ(Machine Readable Zone)解析")
    print("=" * 60)
    
    # TD3格式MRZ示例 (护照)
    # 格式: P<国家代码<<姓<<名<<<<<<...
    # 第二行: 护照号+校验位+国籍+生日+校验位+性别+有效期+校验位...
    
    print("\n1. TD3格式护照MRZ解析:")
    mrz_example = """P<CHNZHANG<<SAN<<<<<<<<<<<<<<<<<<<<<<<
E1234567<CHN9001011M2512310<<<<<<<<<<<<<<00"""
    
    result = parse_mrz(mrz_example)
    print(f"  有效: {result.is_valid}")
    print(f"  文件类型: {result.document_type}")
    print(f"  国家代码: {result.country_code}")
    print(f"  护照号码: {result.document_number}")
    print(f"  姓名: {result.full_name}")
    print(f"    姓: {result.surname}")
    print(f"    名: {result.given_names}")
    print(f"  生日: {result.birth_date}")
    print(f"  性别: {result.sex}")
    print(f"  有效期: {result.expiry_date}")
    print(f"  国籍: {result.nationality}")
    print(f"  校验位验证:")
    print(f"    护照号: {result.check_digit_doc_valid}")
    print(f"    生日: {result.check_digit_birth_valid}")
    print(f"    有效期: {result.check_digit_expiry_valid}")
    print(f"  消息: {result.message}")
    
    # TD1格式示例
    print("\n2. TD1格式MRZ解析 (30字符):")
    mrz_td1 = "IDCHN123456789012345678901234"
    result = parse_mrz(mrz_td1)
    print(f"  有效: {result.is_valid}")
    print(f"  文件类型: {result.document_type}")
    print(f"  国家代码: {result.country_code}")
    print(f"  文件号码: {result.document_number}")
    
    # TD1格式44字符
    print("\n3. TD1格式MRZ解析 (44字符):")
    mrz_td1_44 = "IDCHN12345678901234567890010119001011M2512310"
    result = parse_mrz(mrz_td1_44)
    print(f"  有效: {result.is_valid}")
    print(f"  性别: {result.sex}")
    print(f"  生日: {result.birth_date}")
    print(f"  有效期: {result.expiry_date}")


def example_mrz_check_digit():
    """示例5: MRZ校验位计算和验证"""
    print("\n" + "=" * 60)
    print("示例5: MRZ校验位计算")
    print("=" * 60)
    
    # 计算校验位示例
    test_data = [
        "E12345678",   # 护照号
        "900101",      # 生日 YYMMDD
        "251231",      # 有效期 YYMMDD
    ]
    
    print("\n校验位计算示例:")
    for data in test_data:
        check = PassportUtils._calculate_check_digit(data)
        print(f"  数据 '{data}' -> 校验位 '{check}'")
    
    # 验证校验位
    print("\n校验位验证示例:")
    data = "12345678"
    correct_check = PassportUtils._calculate_check_digit(data)
    print(f"  数据 '{data}'")
    print(f"  正确校验位 '{correct_check}': {PassportUtils._verify_check_digit(data, correct_check)}")
    print(f"  错误校验位 'X': {PassportUtils._verify_check_digit(data, 'X')}")


def example_expiry_check():
    """示例6: 护照过期检查"""
    print("\n" + "=" * 60)
    print("示例6: 护照过期检查")
    print("=" * 60)
    
    # 检查各种有效期的护照
    expiry_dates = [
        ("2020-01-01", "已过期"),
        ("2025-12-31", "未过期"),
        ("200101", "已过期(YYMMDD格式)"),
        ("301231", "未过期(YYMMDD格式)"),
        ("invalid", "无效日期"),
    ]
    
    print("\n护照过期状态:")
    for expiry_date, desc in expiry_dates:
        expired = is_passport_expired(expiry_date)
        days = PassportUtils.days_until_expiry(expiry_date)
        print(f"\n{desc} ({expiry_date}):")
        print(f"  已过期: {expired}")
        if days is not None:
            print(f"  距离过期: {days} 天")
        else:
            print(f"  距离过期: 无法计算")


def example_country_code_lookup():
    """示例7: 国家代码查询"""
    print("\n" + "=" * 60)
    print("示例7: 国家代码查询")
    print("=" * 60)
    
    # 根据ISO 3166-1 alpha-3代码查询国家
    country_codes = [
        "CHN",  # 中国
        "USA",  # 美国
        "GBR",  # 英国
        "DEU",  # 德国
        "FRA",  # 法国
        "JPN",  # 日本
        "KOR",  # 韩国
        "XXX",  # 未知
    ]
    
    print("\n国家代码查询:")
    for code in country_codes:
        country = PassportUtils.get_country_by_code(code)
        print(f"  {code} -> {country.value}")


def example_passport_format_list():
    """示例8: 列出护照格式"""
    print("\n" + "=" * 60)
    print("示例8: 列出护照格式")
    print("=" * 60)
    
    # 列出所有护照格式
    print("\n所有支持的护照格式 (总数):")
    all_formats = get_passport_formats()
    print(f"  总数: {len(all_formats)}")
    
    # 列出中国护照格式
    print("\n中国护照格式:")
    china_formats = get_passport_formats(Country.CHINA)
    for fmt in china_formats:
        print(f"  - {fmt['description']}")
        print(f"    模式: {fmt['pattern']}")
        print(f"    校验位: {'有' if fmt['has_check_digit'] else '无'}")
    
    # 列出美国护照格式
    print("\n美国护照格式:")
    usa_formats = get_passport_formats(Country.USA)
    for fmt in usa_formats:
        print(f"  - {fmt['description']}")
    
    # 列出日本护照格式
    print("\n日本护照格式:")
    japan_formats = get_passport_formats(Country.JAPAN)
    for fmt in japan_formats:
        print(f"  - {fmt['description']}")


def example_passport_cleaning():
    """示例9: 护照号码清理"""
    print("\n" + "=" * 60)
    print("示例9: 护照号码清理和标准化")
    print("=" * 60)
    
    # 各种格式的护照号码
    dirty_passports = [
        ("P 1234567", "带空格"),
        ("P-1234567", "带连字符"),
        ("p1234567", "小写"),
        ("P<1234567", "带尖括号"),
        ("  P1234567  ", "前后空格"),
        ("P 12 34 56 7", "多个空格"),
    ]
    
    print("\n护照号码清理:")
    for passport, desc in dirty_passports:
        result = validate_passport(passport, Country.CHINA)
        print(f"\n{desc} ('{passport}'):")
        print(f"  标准化后: '{result.normalized}'")
        print(f"  有效: {result.is_valid}")


def example_passport_statistics():
    """示例10: 护照统计信息"""
    print("\n" + "=" * 60)
    print("示例10: 护照支持统计")
    print("=" * 60)
    
    # 统计支持的国家数量
    formats = get_passport_formats()
    countries = set(f["country"] for f in formats)
    print(f"\n支持的国家数量: {len(countries)}")
    
    # 统计各国的护照格式数量
    print("\n各国家护照格式数量:")
    country_counts = {}
    for fmt in formats:
        country = fmt["country"]
        country_counts[country] = country_counts.get(country, 0) + 1
    
    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {country}: {count} 种格式")
    
    # 统计有校验位的护照
    has_check_digit = sum(1 for f in formats if f["has_check_digit"])
    print(f"\n带校验位的护照格式: {has_check_digit}")
    print(f"不带校验位的护照格式: {len(formats) - has_check_digit}")


def example_batch_validation():
    """示例11: 批量验证护照"""
    print("\n" + "=" * 60)
    print("示例11: 批量验证护照号码")
    print("=" * 60)
    
    # 模拟批量验证护照号码
    passport_list = [
        "P1234567",
        "E12345678",
        "D1234567",
        "123456789",  # 美国
        "TA1234567",  # 日本
        "C12345678",  # 德国
        "INVALID",    # 无效
        "",           # 空
    ]
    
    print("\n批量验证结果:")
    valid_count = 0
    for passport_num in passport_list:
        result = validate_passport(passport_num)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {passport_num}: {result.country.value} - {result.message}")
        if result.is_valid:
            valid_count += 1
    
    print(f"\n统计:")
    print(f"  总数: {len(passport_list)}")
    print(f"  有效: {valid_count}")
    print(f"  无效: {len(passport_list) - valid_count}")


def main():
    """运行所有示例"""
    example_basic_validation()
    example_country_specific_validation()
    example_auto_detection()
    example_mrz_parsing()
    example_mrz_check_digit()
    example_expiry_check()
    example_country_code_lookup()
    example_passport_format_list()
    example_passport_cleaning()
    example_passport_statistics()
    example_batch_validation()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()