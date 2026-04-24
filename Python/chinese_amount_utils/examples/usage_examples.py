"""
AllToolkit - Chinese Amount Utilities Examples

中文金额大写转换工具的使用示例。

Author: AllToolkit
License: MIT
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mod as ca


def basic_conversion():
    """基本转换示例"""
    print("=" * 60)
    print("基本转换示例")
    print("=" * 60)
    
    # 整数金额
    amounts = [1, 10, 100, 1000, 10000, 100000, 1000000, 100000000]
    for amt in amounts:
        print(f"{amt:>12,} → {ca.to_chinese_amount(amt)}")
    
    print()
    
    # 小数金额
    decimal_amounts = [0.01, 0.5, 1.5, 12.34, 123.45, 1234.56]
    for amt in decimal_amounts:
        print(f"{amt:>12} → {ca.to_chinese_amount(amt)}")


def negative_amounts():
    """负数金额示例"""
    print("=" * 60)
    print("负数金额示例")
    print("=" * 60)
    
    amounts = [-100, -1234.56, -10000]
    for amt in amounts:
        print(f"{amt:>12} → {ca.to_chinese_amount(amt)}")


def complex_amounts():
    """复杂金额示例"""
    print("=" * 60)
    print("复杂金额示例（含零的金额）")
    print("=" * 60)
    
    # 包含零的金额
    amounts = [
        101,       # 一百零一
        1001,      # 一千零一
        10001,     # 一万零一
        101010,    # 十万一千零十
        1010101,   # 一百零一万零一百零一
        100000001, # 一亿零一
    ]
    
    for amt in amounts:
        print(f"{amt:>12,} → {ca.to_chinese_amount(amt)}")


def simplified_format():
    """简化格式示例"""
    print("=" * 60)
    print("简化格式示例（不含货币单位）")
    print("=" * 60)
    
    amounts = [1234, 123456789, 100000000]
    for amt in amounts:
        print(f"{amt:>12,} → {ca.to_chinese_amount_simple(amt)}")


def chinese_number():
    """普通中文数字示例"""
    print("=" * 60)
    print("普通中文数字转换")
    print("=" * 60)
    
    numbers = [123, 1001, 12345, 100000000]
    for num in numbers:
        print(f"{num:>12,} → {ca.to_chinese_number(num)}")


def parse_example():
    """解析中文金额示例"""
    print("=" * 60)
    print("解析中文金额为数字")
    print("=" * 60)
    
    chinese_amounts = [
        '壹仟贰佰叁拾肆元伍角陆分',
        '壹佰元整',
        '拾元整',
        '壹万元整',
        '负壹佰元整',
    ]
    
    for cn in chinese_amounts:
        parsed = ca.parse_chinese_amount(cn)
        print(f"{cn:<30} → {parsed}")


def receipt_format():
    """收据格式示例"""
    print("=" * 60)
    print("收据/发票格式")
    print("=" * 60)
    
    amounts = [1234.56, 10000, 1000000]
    for amt in amounts:
        print(f"{amt:>12,} → {ca.format_amount_for_receipt(amt)}")
    
    print()
    
    # 不带"人民币"前缀
    for amt in amounts:
        print(f"{amt:>12,} → {ca.format_amount_for_receipt(amt, include_prefix=False)}")


def validation():
    """验证示例"""
    print("=" * 60)
    print("验证中文金额格式")
    print("=" * 60)
    
    test_strings = [
        '壹仟贰佰叁拾肆元伍角陆分',
        '壹佰元整',
        'abc',
        '123',
        '',
    ]
    
    for s in test_strings:
        valid = ca.validate_chinese_amount(s)
        status = "有效" if valid else "无效"
        print(f"'{s}' → {status}")


def different_styles():
    """不同风格示例"""
    print("=" * 60)
    print("不同输出风格")
    print("=" * 60)
    
    amount = 1234.56
    
    styles = ['standard', 'simple']
    for style in styles:
        result = ca.amount_in_words(amount, style=style)
        print(f"{style:10} → {result}")


def shortcut_functions():
    """快捷函数示例"""
    print("=" * 60)
    print("快捷函数（rmb / cny）")
    print("=" * 60)
    
    amounts = [1234.56, 10000, 5000000]
    for amt in amounts:
        print(f"{amt:>12,} → rmb: {ca.rmb(amt)}")
        print(f"{amt:>12,} → cny: {ca.cny(amt)}")


def real_world_examples():
    """实际场景示例"""
    print("=" * 60)
    print("实际应用场景")
    print("=" * 60)
    
    print("\n【发票金额】")
    invoice_amounts = [18.5, 99.99, 1280, 5678.90]
    for amt in invoice_amounts:
        print(f"发票金额 ¥{amt:>8} → {ca.to_chinese_amount(amt)}")
    
    print("\n【薪资金额】")
    salary_amounts = [8500, 12000, 25000, 50000]
    for amt in salary_amounts:
        print(f"月薪 ¥{amt:>8} → {ca.to_chinese_amount(amt)}")
    
    print("\n【银行转账】")
    transfer_amounts = [10000, 50000, 100000, 5000000]
    for amt in transfer_amounts:
        print(f"转账金额 ¥{amt:>8} → {ca.format_amount_for_receipt(amt)}")
    
    print("\n【合同金额】")
    contract_amounts = [1000000, 5000000, 10000000]
    for amt in contract_amounts:
        print(f"合同金额 ¥{amt:>12} → {ca.format_amount_for_receipt(amt)}")


def string_input():
    """字符串输入示例"""
    print("=" * 60)
    print("字符串输入（支持逗号分隔）")
    print("=" * 60)
    
    inputs = ['100', '1234.56', '1,000', '1,000,000']
    for s in inputs:
        print(f"'{s}' → {ca.to_chinese_amount(s)}")


def decimal_type():
    """Decimal 类型示例"""
    print("=" * 60)
    print("Decimal 类型（精确计算）")
    print("=" * 60)
    
    from decimal import Decimal
    
    amounts = [
        Decimal('100.50'),
        Decimal('1234.56'),
        Decimal('99999999.99'),
    ]
    
    for amt in amounts:
        print(f"{amt:>15} → {ca.to_chinese_amount(amt)}")


def custom_units():
    """自定义货币单位示例"""
    print("=" * 60)
    print("自定义货币单位")
    print("=" * 60)
    
    amount = 1234.56
    
    # 自定义单位
    result = ca.to_chinese_amount(
        amount,
        currency='圆',
        sub_currency_1='毛',
        sub_currency_2='分',
        suffix='正'
    )
    print(f"自定义单位: {result}")


def main():
    """运行所有示例"""
    basic_conversion()
    negative_amounts()
    complex_amounts()
    simplified_format()
    chinese_number()
    parse_example()
    receipt_format()
    validation()
    different_styles()
    shortcut_functions()
    real_world_examples()
    string_input()
    decimal_type()
    custom_units()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()