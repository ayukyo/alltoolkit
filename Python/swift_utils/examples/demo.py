#!/usr/bin/env python3
"""
Swift Utils 使用示例

演示SWIFT/BIC银行代码验证工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SwiftUtils, BicUtils, SwiftCodeType, SwiftNetworkStatus,
    validate_swift, validate_bic, parse_swift, parse_bic,
    get_swift_bank_code, get_swift_country, is_swift_primary, format_swift
)


def print_separator(title: str = ""):
    """打印分隔线"""
    print("\n" + "=" * 50)
    if title:
        print(f"  {title}")
        print("=" * 50)


def example_basic_validation():
    """基本验证示例"""
    print_separator("基本验证")

    # 有效的SWIFT代码
    swifts = [
        "BKCHCNBJ",      # 中国银行（8位）
        "BKCHCNBJXXX",   # 中国银行（11位，主要办公机构）
        "HSBCGB2L",      # 汇丰银行
        "DEUTDEFF",      # 德意志银行
        "CITIUS33",      # 花旗银行
    ]

    for swift in swifts:
        valid = SwiftUtils.validate(swift)
        print(f"  {swift}: {'✓ 有效' if valid else '✗ 无效'}")

    # 无效的SWIFT代码
    print("\n无效代码示例:")
    invalid = ["INVALID", "BKCHXXBJ", "1234CNBJ", "BKCH"]
    for swift in invalid:
        valid = SwiftUtils.validate(swift)
        print(f"  {swift}: {'✓ 有效' if valid else '✗ 无效'}")


def example_strict_validation():
    """严格验证示例"""
    print_separator("严格验证（详细错误信息）")

    # 有效代码
    valid, errors = SwiftUtils.validate_strict("BKCHCNBJ")
    print(f"  BKCHCNBJ: {valid}")
    if errors:
        for err in errors:
            print(f"    - {err}")

    # 无效代码
    invalid_codes = [
        "BKCH",           # 长度不足
        "1234CNBJ",       # 银行代码含数字
        "BKCHXXBJ",       # 无效国家代码
    ]

    for swift in invalid_codes:
        valid, errors = SwiftUtils.validate_strict(swift)
        print(f"\n  {swift}: {valid}")
        for err in errors:
            print(f"    ❌ {err}")


def example_parsing():
    """解析示例"""
    print_separator("SWIFT代码解析")

    swifts = ["BKCHCNBJ", "BKCHCNBJXXX", "HSBCGB2L", "DEUTDEFF500"]

    for swift in swifts:
        info = SwiftUtils.parse(swift)
        print(f"\n  🏦 {swift}")
        print(f"     银行: {info['bank_name']} ({info['bank_name_en']})")
        print(f"     国家: {info['country_name']} ({info['country_name_en']})")
        print(f"     地区: {info['location_code']}")
        print(f"     分行: {info['branch_code'] or '主要办公机构'}")
        print(f"     类型: {info['code_type']}")
        print(f"     货币: {info['country_currency']}")


def example_extraction():
    """提取功能示例"""
    print_separator("代码部分提取")

    swift = "BKCHCNBJA01"
    print(f"\n  原始代码: {swift}")
    print(f"     银行代码: {SwiftUtils.get_bank_code(swift)}")
    print(f"     国家代码: {SwiftUtils.get_country_code(swift)}")
    print(f"     地区代码: {SwiftUtils.get_location_code(swift)}")
    print(f"     分行代码: {SwiftUtils.get_branch_code(swift)}")


def example_generation():
    """生成功能示例"""
    print_separator("SWIFT代码生成")

    # 生成8位主要办公机构代码
    swift1 = SwiftUtils.generate_primary("BKCH", "CN", "BJ")
    print(f"\n  生成主要办公机构代码:")
    print(f"     银行: BKCH, 国家: CN, 地区: BJ")
    print(f"     结果: {swift1}")

    # 生成11位分行代码
    swift2 = SwiftUtils.generate_branch("BKCH", "CN", "BJ", "XXX")
    print(f"\n  生成分行代码:")
    print(f"     银行: BKCH, 国家: CN, 地区: BJ, 分行: XXX")
    print(f"     结果: {swift2}")

    swift3 = SwiftUtils.generate_branch("DEUT", "DE", "FF", "500")
    print(f"\n  生成德意志银行分行:")
    print(f"     银行: DEUT, 国家: DE, 地区: FF, 分行: 500")
    print(f"     结果: {swift3}")


def example_primary_office():
    """主要办公机构判断示例"""
    print_separator("主要办公机构判断")

    swifts = [
        "BKCHCNBJ",       # 8位代码
        "BKCHCNBJXXX",    # 11位，XXX分行
        "BKCHCNBJA01",    # 11位，特定分行
        "DEUTDEFF500",    # 11位，特定分行
    ]

    for swift in swifts:
        is_primary = SwiftUtils.is_primary_office(swift)
        primary_code = SwiftUtils.get_primary_code(swift)
        print(f"  {swift}: {'主要办公机构' if is_primary else '特定分行'}")
        print(f"     主要办公机构代码: {primary_code}")


def example_comparison():
    """比较功能示例"""
    print_separator("SWIFT代码比较")

    pairs = [
        ("BKCHCNBJ", "BKCHCNBJXXX"),     # 同银行同地区
        ("BKCHCNBJ", "BKCHSHA1"),        # 同银行不同地区
        ("BKCHCNBJ", "ICBKCNBJ"),        # 不同银行同国家
        ("BKCHCNBJ", "HSBCGB2L"),        # 不同银行不同国家
    ]

    for swift1, swift2 in pairs:
        result = SwiftUtils.compare(swift1, swift2)
        print(f"\n  {swift1} vs {swift2}")
        print(f"     同银行: {'✓' if result['same_bank'] else '✗'}")
        print(f"     同国家: {'✓' if result['same_country'] else '✗'}")
        print(f"     同地区: {'✓' if result['same_location'] else '✗'}")
        print(f"     相关: {'✓' if result['is_related'] else '✗'}")


def example_country_info():
    """国家信息示例"""
    print_separator("国家信息查询")

    countries = ["CN", "US", "GB", "DE", "JP", "FR", "CH", "HK"]

    for code in countries:
        info = SwiftUtils.get_country_info(code)
        print(f"  {code}: {info['name']} ({info['name_en']}) - 货币: {info['currency']}")

    # 统计
    all_countries = SwiftUtils.get_all_countries()
    print(f"\n  共支持 {len(all_countries)} 个国家和地区")


def example_bank_examples():
    """银行示例示例"""
    print_separator("银行示例数据")

    banks = SwiftUtils.get_all_bank_examples()
    print(f"\n  已知银行示例 ({len(banks)} 个):")

    for bank_code, info in list(banks.items())[:8]:
        print(f"     {bank_code}: {info['name']} ({info['country']})")

    # 搜索特定国家的银行
    print("\n  中国银行:")
    cn_banks = SwiftUtils.search_by_country("CN")
    for bank in cn_banks:
        print(f"     {bank['bank_code']}: {bank['bank_name']}")

    print("\n  美国银行:")
    us_banks = SwiftUtils.search_by_country("US")
    for bank in us_banks[:4]:
        print(f"     {bank['bank_code']}: {bank['bank_name_en']}")


def example_format():
    """格式化示例"""
    print_separator("代码格式化")

    inputs = [
        "bkchcnbj",           # 小写
        "BKCH CNBJ",          # 带空格
        "BKCH-CNBJ-XXX",      # 带连字符
        "  bkch cnbj  ",      # 带空格和小写
    ]

    for input_code in inputs:
        formatted = SwiftUtils.format(input_code)
        print(f"  '{input_code}' → '{formatted}'")


def example_bic_alias():
    """BIC别名示例"""
    print_separator("BIC别名功能")

    swift = "BKCHCNBJ"
    print(f"\n  使用BicUtils（SWIFT别名）:")
    print(f"     验证: {BicUtils.validate(swift)}")
    print(f"     解析: {BicUtils.parse(swift)['bank_name']}")
    print(f"     银行代码: {BicUtils.get_bank_code(swift)}")
    print(f"     国家代码: {BicUtils.get_country_code(swift)}")


def example_convenience_functions():
    """便捷函数示例"""
    print_separator("便捷函数")

    swift = "BKCHCNBJXXX"
    print(f"\n  SWIFT代码: {swift}")
    print(f"     验证: {validate_swift(swift)}")
    print(f"     解析: {parse_swift(swift)['bank_name']}")
    print(f"     银行代码: {get_swift_bank_code(swift)}")
    print(f"     国家: {get_swift_country(swift)}")
    print(f"     主要办公机构: {is_swift_primary(swift)}")
    print(f"     格式化: {format_swift('bkch cnbj')}")


def example_real_world_scenario():
    """实际应用场景示例"""
    print_separator("实际应用场景")

    # 场景1：验证用户输入的SWIFT代码
    print("\n  📝 场景1: 验证用户输入")
    user_input = "bkch-cnbj-xxx"
    formatted = SwiftUtils.format(user_input)
    valid = SwiftUtils.validate(formatted)
    print(f"     用户输入: '{user_input}'")
    print(f"     格式化后: '{formatted}'")
    print(f"     验证结果: {'✓ 有效' if valid else '✗ 无效'}")

    if valid:
        info = SwiftUtils.parse(formatted)
        print(f"     银行: {info['bank_name']}")
        print(f"     国家: {info['country_name']}")

    # 场景2：检查收款银行是否与汇款银行相同国家
    print("\n  💸 场景2: 国际汇款验证")
    sender_bank = "BKCHCNBJ"
    receiver_bank = "HSBCGB2L"
    result = SwiftUtils.compare(sender_bank, receiver_bank)
    print(f"     汇款银行: {sender_bank} ({SwiftUtils.parse(sender_bank)['country_name']})")
    print(f"     收款银行: {receiver_bank} ({SwiftUtils.parse(receiver_bank)['country_name']})")
    print(f"     同国家: {'是' if result['same_country'] else '否（国际汇款）'}")

    # 场景3：获取银行主要办公机构SWIFT代码
    print("\n  🏢 场景3: 获取主要办公机构代码")
    branch_code = "BKCHCNBJA01"
    primary = SwiftUtils.get_primary_code(branch_code)
    print(f"     分行代码: {branch_code}")
    print(f"     主要办公机构代码: {primary}")

    # 场景4：生成银行SWIFT代码
    print("\n  🔧 场景4: 生成测试SWIFT代码")
    test_swift = SwiftUtils.generate_primary("TEST", "US", "00")
    print(f"     生成的测试代码: {test_swift}")
    print(f"     验证: {SwiftUtils.validate(test_swift)}")


def main():
    """运行所有示例"""
    example_basic_validation()
    example_strict_validation()
    example_parsing()
    example_extraction()
    example_generation()
    example_primary_office()
    example_comparison()
    example_country_info()
    example_bank_examples()
    example_format()
    example_bic_alias()
    example_convenience_functions()
    example_real_world_scenario()

    print_separator()
    print("\n✅ 所有示例运行完成！\n")


if __name__ == "__main__":
    main()