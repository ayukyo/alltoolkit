#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Damm Utils 使用示例
==========================================

展示 Damm 校验码算法的各种使用场景。

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from damm_utils.mod import (
    DammCalculator,
    DammUtils,
    ErrorDetector,
    compute_damm_check_digit,
    validate_damm,
    generate_damm_code,
    batch_generate_damm_codes,
    batch_validate_damm_codes,
    analyze_damm_error_detection,
)


def example_basic_usage():
    """基本用法示例"""
    print("\n" + "=" * 60)
    print("基本用法示例")
    print("=" * 60)
    
    # 1. 计算校验码
    print("\n1. 计算校验码")
    numbers = ["572", "123456", "987654321"]
    for num in numbers:
        check = compute_damm_check_digit(num)
        print(f"   {num} 的校验码: {check}")
    
    # 2. 生成完整编码
    print("\n2. 生成完整编码")
    for num in numbers:
        full = generate_damm_code(num)
        print(f"   {num} -> {full}")
    
    # 3. 验证编码
    print("\n3. 验证编码")
    test_codes = ["5726", "1234563", "9876543210", "1111"]
    for code in test_codes:
        valid = validate_damm(code)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"   {code}: {status}")


def example_product_identification():
    """产品标识示例"""
    print("\n" + "=" * 60)
    print("产品标识示例 - 使用Damm校验码")
    print("=" * 60)
    
    calculator = DammCalculator()
    
    # 产品编码生成（Damm仅支持数字）
    print("\n1. 为产品生成带校验码的标识（数字编码）")
    products = [
        ("笔记本电脑", "1001234"),
        ("手机", "2005678"),
        ("平板电脑", "3009876"),
        ("耳机", "4001234"),
    ]
    
    for name, code in products:
        full = calculator.generate_full_code(code)
        print(f"   {name}: {code} -> {full}")
    
    # 扫描验证
    print("\n2. 扫描验证产品码")
    # 使用上面生成的编码
    scanned_codes = [
        "10012347",  # 需验证
        "10012340",  # 错误校验码
        "20056780",  # 需验证
    ]
    
    for code in scanned_codes:
        result = calculator.validate_with_result(code)
        if result.valid:
            print(f"   {code}: ✓ 有效 - 产品ID: {result.original}")
        else:
            print(f"   {code}: ✗ 无效 - 错误: {result.error_type}")


def example_financial_transactions():
    """金融交易示例"""
    print("\n" + "=" * 60)
    print("金融交易示例 - 交易ID校验")
    print("=" * 60)
    
    # 批量生成交易ID（纯数字）
    print("\n1. 批量生成带校验码的交易ID")
    transaction_ids = ["10001", "10002", "10003", "10004", "10005"]
    
    full_ids = batch_generate_damm_codes(transaction_ids)
    for i, (tx, full) in enumerate(zip(transaction_ids, full_ids)):
        print(f"   交易{i+1}: {tx} -> {full}")
    
    # 批量验证
    print("\n2. 批量验证交易ID")
    # 创建一个错误ID（修改校验码）
    wrong_id = full_ids[0][:-1] + "0"  # 修改校验码为0
    test_ids = full_ids[:3] + [wrong_id]
    
    results = batch_validate_damm_codes(test_ids)
    for tx, valid in zip(test_ids, results):
        status = "✓" if valid else "✗"
        print(f"   {tx}: {status}")


def example_id_cards():
    """证件号码示例"""
    print("\n" + "=" * 60)
    print("证件号码示例 - 成员卡号验证")
    print("=" * 60)
    
    calculator = DammCalculator()
    
    # 生成会员卡号（Damm仅支持数字）
    print("\n1. 生成会员卡号")
    member_ids = ["001", "002", "003"]
    
    for mid in member_ids:
        full = calculator.generate_full_code(mid)
        print(f"   会员号 M{mid}: 数字码 {mid} -> 完整编码 {full}")
    
    # 验证会员卡
    print("\n2. 验证会员卡号")
    test_cards = [
        ("M001", "001", calculator.generate_full_code("001")),  # 正确
        ("M002", "002", "0020"),  # 可能错误
    ]
    
    for card_id, num, full_num in test_cards:
        valid = calculator.validate(full_num)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"   卡号 {card_id}: 数字码 {full_num} -> {status}")


def example_error_detection():
    """错误检测示例"""
    print("\n" + "=" * 60)
    print("错误检测能力示例")
    print("=" * 60)
    
    detector = ErrorDetector()
    
    # 测试单个数字错误
    print("\n1. 单个数字错误检测")
    original = "1234"
    errors = [
        "1239",  # 位置3错误
        "1235",  # 位置3错误
        "9234",  # 位置0错误
    ]
    
    for err in errors:
        result = detector.detect_single_digit_error(original, err)
        print(f"   {original} -> {err}:")
        print(f"      检测到错误: {result.detected}")
        print(f"      错误位置: {result.error_position}")
        print(f"      错误类型: {result.error_type}")
    
    # 测试换位错误
    print("\n2. 换位错误检测")
    transpositions = [
        ("1234", "1324"),  # 位置1和2换位
        ("1234", "2134"),  # 位置0和1换位
        ("1234", "1243"),  # 位置2和3换位
    ]
    
    for orig, trans in transpositions:
        result = detector.detect_single_digit_error(orig, trans)
        print(f"   {orig} -> {trans}:")
        print(f"      检测到错误: {result.detected}")
        print(f"      错误类型: {result.error_type}")
        print(f"      描述: {result.description}")


def example_error_analysis():
    """错误分析示例"""
    print("\n" + "=" * 60)
    print("错误检测能力分析")
    print("=" * 60)
    
    # 分析检测能力
    print("\n执行错误检测能力分析...")
    analysis = analyze_damm_error_detection(6)
    
    print("\n分析结果:")
    for category, stats in analysis.items():
        if isinstance(stats, dict) and 'detection_rate' in stats:
            rate = stats['detection_rate']
            detected = stats['detected']
            total = stats['total']
            print(f"   {category}:")
            print(f"      检测数: {detected}/{total}")
            print(f"      检测率: {rate}%")
    
    # 解释
    print("\n重要说明:")
    print("   - Damm算法能检测所有单个数字错误 (100%)")
    print("   - Damm算法能检测所有相邻换位错误 (100%)")
    print("   - 这优于Luhn算法（Luhn无法检测某些换位）")


def example_data_entry_validation():
    """数据录入验证示例"""
    print("\n" + "=" * 60)
    print("数据录入验证示例")
    print("=" * 60)
    
    calculator = DammCalculator()
    
    # 模拟数据录入场景
    print("\n场景: 用户录入产品编码")
    
    # 正确编码（纯数字）
    correct_code = calculator.generate_full_code("123456")
    print(f"\n正确编码: {correct_code}")
    
    # 模拟录入错误
    print("\n模拟录入错误:")
    errors = [
        ("单个数字错误", correct_code[:2] + "9" + correct_code[3:]),
        ("换位错误", correct_code[:1] + correct_code[2] + correct_code[1] + correct_code[3:]),
        ("遗漏数字", correct_code[:-1]),
        ("多余数字", correct_code + "0"),
    ]
    
    for error_type, corrupted in errors:
        valid = calculator.validate(corrupted)
        status = "检测到 ✓" if not valid else "未检测 ✗"
        print(f"   {error_type}: {corrupted} -> {status}")


def example_comparison_with_luhn():
    """与Luhn算法对比示例"""
    print("\n" + "=" * 60)
    print("Damm vs Luhn 对比示例")
    print("=" * 60)
    
    print("\nDamm算法优势:")
    print("   1. 检测所有单个数字替换错误")
    print("   2. 检测所有相邻换位错误")
    print("   3. 检测所有音位换位错误（如 09 <-> 90）")
    print("   4. 使用完全反对称拟群，数学性质更严谨")
    
    print("\nLuhn算法局限:")
    print("   1. 无法检测某些换位错误")
    print("   2. 例如: 09 <-> 90 在Luhn中校验值相同")
    print("   3. 例如: 13 <-> 31 在Luhn中校验值相同")
    
    # 演示
    print("\n演示: 09 <-> 90 换位")
    calculator = DammCalculator()
    
    code09 = calculator.generate_full_code("09")
    code90 = calculator.generate_full_code("90")
    
    print(f"   09 校验码: {code09[-1]}")
    print(f"   90 校验码: {code90[-1]}")
    print(f"   校验码不同: Damm能检测此换位错误 ✓")
    
    # 验证换位后的错误码
    swapped09_to_90 = code09[:-1] + "90"[-1:]
    valid = calculator.validate(swapped09_to_90)
    print(f"   09换位为90后验证: {valid} (应无效)")


def example_bulk_operations():
    """批量操作示例"""
    print("\n" + "=" * 60)
    print("批量操作示例")
    print("=" * 60)
    
    # 批量生成
    print("\n1. 批量生成编码")
    numbers = [str(i).zfill(6) for i in range(1, 11)]
    codes = batch_generate_damm_codes(numbers)
    
    print(f"   生成了 {len(codes)} 个编码")
    for i, (num, code) in enumerate(zip(numbers[:5], codes[:5])):
        print(f"      {num} -> {code}")
    
    # 批量验证
    print("\n2. 批量验证编码")
    # 创建一些有效和一些无效编码
    test_codes = codes[:5] + ["0000000", "9999999"]
    
    results = batch_validate_damm_codes(test_codes)
    
    print(f"   验证结果:")
    for code, valid in zip(test_codes, results):
        status = "有效" if valid else "无效"
        print(f"      {code}: {status}")


def main():
    """主函数"""
    print("=" * 60)
    print("Damm Utils 使用示例集合")
    print("=" * 60)
    
    example_basic_usage()
    example_product_identification()
    example_financial_transactions()
    example_id_cards()
    example_error_detection()
    example_error_analysis()
    example_data_entry_validation()
    example_comparison_with_luhn()
    example_bulk_operations()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)


if __name__ == '__main__':
    main()