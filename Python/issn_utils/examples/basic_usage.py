#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISSN Utilities - 基础用法示例
展示ISSN验证、转换、格式化等基本功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    is_issn8, is_issn13, is_valid_issn,
    format_issn, clean_issn,
    issn8_to_issn13, issn13_to_issn8,
    parse_issn, get_issn_variants,
)


def main():
    print("=" * 60)
    print("ISSN Utilities - 基础用法示例")
    print("=" * 60)
    
    # 1. ISSN验证
    print("\n【1. ISSN验证】")
    test_issns = [
        "0028-0836",       # 有效 ISSN-8 (Nature)
        "9770028083002",   # 有效 ISSN-13 (Nature)
        "2434-561X",       # 有效 ISSN-8（X检验位）
        "invalid",         # 无效
        "0028-0837",       # 无效（错误检验位）
    ]
    
    for issn in test_issns:
        status = "✓ 有效" if is_valid_issn(issn) else "✗ 无效"
        type_info = ""
        if is_issn8(issn):
            type_info = "(ISSN-8)"
        elif is_issn13(issn):
            type_info = "(ISSN-13)"
        print(f"  {issn:15s} → {status} {type_info}")
    
    # 2. ISSN格式化
    print("\n【2. ISSN格式化】")
    print(f"  clean_issn('0028-0836')     → {clean_issn('0028-0836')}")
    print(f"  clean_issn('ISSN 0028-0836') → {clean_issn('ISSN 0028-0836')}")
    print(f"  format_issn('00280836')     → {format_issn('00280836')}")
    print(f"  format_issn('9770028083002') → {format_issn('9770028083002')}")
    
    # 3. ISSN转换
    print("\n【3. ISSN转换】")
    print(f"  ISSN-8 → ISSN-13:")
    print(f"    '0028-0836' → {issn8_to_issn13('0028-0836')}")
    print(f"    '2434-561X' → {issn8_to_issn13('2434-561X')}")
    
    print(f"  ISSN-13 → ISSN-8:")
    print(f"    '9770028083002' → {issn13_to_issn8('9770028083002')}")
    
    # 4. ISSN解析
    print("\n【4. ISSN详细解析】")
    issn = "0028-0836"
    info = parse_issn(issn)
    print(f"  ISSN: {issn}")
    print(f"    类型: {info['type']}")
    print(f"    紧凑: {info['clean']}")
    print(f"    格式化: {info['formatted']}")
    print(f"    检验位: {info['check_digit']}")
    print(f"    ISSN-8: {info['issn8']}")
    print(f"    ISSN-13: {info['issn13']}")
    print(f"    ISSN-L: {info['issn_l']}")
    
    # 5. ISSN变体
    print("\n【5. ISSN变体】")
    variants = get_issn_variants("0028-0836")
    print(f"  ISSN-8:   {variants['issn8']}")
    print(f"  格式化8:  {variants['formatted8']}")
    print(f"  ISSN-13:  {variants['issn13']}")
    print(f"  格式化13: {variants['formatted13']}")
    print(f"  ISSN-L:   {variants['issn_l']}")
    
    print("\n" + "=" * 60)
    print("完成！")


if __name__ == "__main__":
    main()