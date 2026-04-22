#!/usr/bin/env python3
"""
NATO Phonetic Alphabet Utils - 基本用法示例

演示如何使用北约音标字母工具进行编码和解码

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode, decode, spell, get_nato_word, get_char_from_nato,
    is_nato_word, NATOConverter
)


def main():
    print("=" * 60)
    print("NATO Phonetic Alphabet Utils - 基本用法示例")
    print("=" * 60)
    
    # 1. 基本编码
    print("\n1. 基本编码")
    print("-" * 40)
    
    words = ['SOS', 'ABC', 'HELLO', 'WORLD']
    for word in words:
        encoded = encode(word)
        print(f"  {word:10s} -> {encoded}")
    
    # 2. 自定义分隔符
    print("\n2. 自定义分隔符")
    print("-" * 40)
    
    text = 'ABC'
    print(f"  空格分隔: {encode(text, separator=' ')}")
    print(f"  短横分隔: {encode(text, separator='-')}")
    print(f"  斜杠分隔: {encode(text, separator='/')}")
    print(f"  竖线分隔: {encode(text, separator=' | ')}")
    
    # 3. 包含原始字符
    print("\n3. 包含原始字符")
    print("-" * 40)
    
    print(f"  普通编码: {encode('ABC')}")
    print(f"  包含原字: {encode('ABC', include_original=True)}")
    
    # 4. 数字处理
    print("\n4. 数字处理")
    print("-" * 40)
    
    print(f"  123 -> {encode('123')}")
    print(f"  911 -> {encode('911')}")
    print(f"  A1B2 -> {encode('A1B2')}")
    
    # 5. 特殊字符
    print("\n5. 特殊字符")
    print("-" * 40)
    
    print(f"  A.B -> {encode('A.B')}")
    print(f"  A-B -> {encode('A-B')}")
    print(f"  A/B -> {encode('A/B')}")
    print(f"  +1 -> {encode('+1')}")
    
    # 6. 解码
    print("\n6. 解码")
    print("-" * 40)
    
    encoded_texts = [
        'Alpha Bravo Charlie',
        'One Two Three',
        'Sierra Oscar Sierra'
    ]
    
    for encoded in encoded_texts:
        decoded = decode(encoded)
        print(f"  {encoded:30s} -> {decoded}")
    
    # 7. 不同格式拼写
    print("\n7. 不同格式拼写")
    print("-" * 40)
    
    text = 'ABC'
    print(f"  默认格式:\n    {spell(text, 'default')}")
    print(f"\n  编号格式:\n    {spell(text, 'numbered').replace(chr(10), chr(10) + '    ')}")
    print(f"\n  表格格式:\n    {spell(text, 'table').replace(chr(10), chr(10) + '    ')}")
    print(f"\n  音标格式:\n    {spell(text, 'phonetic').replace(chr(10), chr(10) + '    ')}")
    
    # 8. 单字符操作
    print("\n8. 单字符操作")
    print("-" * 40)
    
    chars = ['A', 'Z', '5', '.']
    for char in chars:
        word = get_nato_word(char)
        back = get_char_from_nato(word)
        print(f"  {char} -> {word} -> {back}")
    
    # 9. 验证音标词
    print("\n9. 验证音标词")
    print("-" * 40)
    
    words_to_check = ['Alpha', 'Bravo', 'Hello', 'World']
    for word in words_to_check:
        valid = is_nato_word(word)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {word:10s} {status}")
    
    # 10. 使用 NATOConverter 类
    print("\n10. 使用 NATOConverter 类")
    print("-" * 40)
    
    converter = NATOConverter(separator=' ')
    print(f"  创建转换器: {converter}")
    
    text = 'HELLO'
    encoded = converter.encode(text)
    decoded = converter.decode(encoded)
    
    print(f"  编码 '{text}': {encoded}")
    print(f"  解码结果: {decoded}")
    
    # 11. 实用示例：电话号码
    print("\n11. 实用示例：电话号码")
    print("-" * 40)
    
    from mod import pronounce_phone_number
    
    phone = '1-800-CALL'
    phonetic = pronounce_phone_number(phone)
    print(f"  电话号码: {phone}")
    print(f"  音标发音: {phonetic}")
    
    # 12. 实用示例：呼号
    print("\n12. 实用示例：呼号")
    print("-" * 40)
    
    from mod import pronounce_callsign, verify_callsign
    
    callsigns = ['KLM123', 'ABC-XYZ', 'TEST@01']
    
    for callsign in callsigns:
        valid, spelling = verify_callsign(callsign)
        status = "✓ 有效" if valid else "✗ 包含无效字符"
        print(f"  {callsign:10s} {status}")
        print(f"            拼写: {' '.join(spelling)}")
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == '__main__':
    main()