"""
Luhn算法工具使用示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from luhn_utils.mod import (
    validate,
    calculate_check_digit,
    generate_with_check_digit,
    format_card_number,
    mask_card_number,
    validate_card,
    generate_test_card,
    validate_imei,
    generate_imei,
    extract_luhn_info,
    identify_card_type,
)


def example_1_basic_validation():
    """示例1: 基础卡号验证"""
    print("\n=== 示例1: 基础卡号验证 ===")
    
    cards = [
        ("4532015112830366", "Visa卡"),
        ("5555555555554444", "MasterCard"),
        ("378282246310005", "American Express"),
        ("6011111111111117", "Discover"),
        ("1234567890123456", "无效卡号"),
    ]
    
    for number, description in cards:
        is_valid = validate(number)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {description}: {number} -> {status}")


def example_2_generate_check_digit():
    """示例2: 生成校验位"""
    print("\n=== 示例2: 生成校验位 ===")
    
    # 假设有一个不含校验位的卡号
    partial_number = "453201511283036"
    check_digit = calculate_check_digit(partial_number)
    full_number = generate_with_check_digit(partial_number)
    
    print(f"  部分号码: {partial_number}")
    print(f"  计算校验位: {check_digit}")
    print(f"  完整号码: {full_number}")
    print(f"  验证: {'有效' if validate(full_number) else '无效'}")


def example_3_formatting():
    """示例3: 格式化卡号"""
    print("\n=== 示例3: 格式化卡号 ===")
    
    number = "4532015112830366"
    
    print(f"  原始: {number}")
    print(f"  空格分隔: {format_card_number(number)}")
    print(f"  横线分隔: {format_card_number(number, '-')}")
    print(f"  遮蔽显示: {mask_card_number(number)}")
    print(f"  自定义遮蔽: {mask_card_number(number, show_first=6, show_last=2, mask_char='X')}")


def example_4_card_type():
    """示例4: 卡类型识别"""
    print("\n=== 示例4: 卡类型识别 ===")
    
    cards = [
        "4532015112830366",
        "5555555555554444",
        "378282246310005",
        "6011111111111117",
        "3530111333300000",
    ]
    
    for card in cards:
        is_valid, card_type, formatted = validate_card(card)
        if is_valid:
            print(f"  {formatted} -> {card_type}")
        else:
            print(f"  {card} -> 无效")


def example_5_test_cards():
    """示例5: 生成测试卡号"""
    print("\n=== 示例5: 生成测试卡号 ===")
    
    for card_type in ["Visa", "MasterCard", "American Express", "Discover"]:
        test_card = generate_test_card(card_type)
        is_valid = validate(test_card)
        print(f"  {card_type}: {test_card} ({'有效' if is_valid else '无效'})")


def example_6_imei():
    """示例6: IMEI号码验证"""
    print("\n=== 示例6: IMEI号码验证 ===")
    
    # 测试真实IMEI格式
    test_imeis = [
        "490154203237518",  # 有效
        "356938035643809",  # 有效
        "123456789012345",  # 无效
    ]
    
    for imei in test_imeis:
        is_valid = validate_imei(imei)
        print(f"  {imei}: {'有效' if is_valid else '无效'}")
    
    # 生成测试IMEI
    generated = generate_imei()
    print(f"  生成的IMEI: {generated} ({'有效' if validate_imei(generated) else '无效'})")


def example_7_detailed_info():
    """示例7: 提取详细信息"""
    print("\n=== 示例7: 提取详细信息 ===")
    
    card = "4532015112830366"
    info = extract_luhn_info(card)
    
    print(f"  卡号: {info['number']}")
    print(f"  长度: {info['length']}")
    print(f"  有效: {'是' if info['valid'] else '否'}")
    print(f"  校验位: {info['check_digit']}")
    print(f"  计算校验位: {info['calculated_check_digit']}")
    print(f"  校验位正确: {'是' if info['check_digit_correct'] else '否'}")
    print(f"  格式化: {info['formatted']}")
    print(f"  遮蔽: {info['masked']}")
    print(f"  卡类型: {info['card_type']}")


def example_8_user_input():
    """示例8: 用户输入验证"""
    print("\n=== 示例8: 用户输入验证 ===")
    
    # 模拟用户输入（可能包含格式化字符）
    user_inputs = [
        "4532-0151-1283-0366",
        "4532 0151 1283 0366",
        " 4532015112830366 ",
    ]
    
    for user_input in user_inputs:
        is_valid, card_type, formatted = validate_card(user_input)
        print(f"  输入: '{user_input.strip()}'")
        print(f"    -> 有效: {'是' if is_valid else '否'}, 类型: {card_type or '未知'}, 格式化: {formatted}")


if __name__ == "__main__":
    print("=" * 50)
    print("Luhn算法工具使用示例")
    print("=" * 50)
    
    example_1_basic_validation()
    example_2_generate_check_digit()
    example_3_formatting()
    example_4_card_type()
    example_5_test_cards()
    example_6_imei()
    example_7_detailed_info()
    example_8_user_input()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)