#!/usr/bin/env python3
"""
NATO Phonetic Alphabet Utils - 无线电通信示例

演示在无线电通信场景中使用北约音标字母

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode, decode, text_to_radio_speech, pronounce_callsign,
    pronounce_phone_number, verify_callsign, NATOConverter
)


def main():
    print("=" * 60)
    print("NATO Phonetic Alphabet Utils - 无线电通信示例")
    print("=" * 60)
    
    # 1. 航空通信
    print("\n1. 航空通信 - 呼号处理")
    print("-" * 40)
    
    callsigns = [
        'UAL123',    # 美联航 123
        'BAW456',    # 英航 456
        'DLH789',    # 汉莎 789
        'AFR001',    # 法航 001
    ]
    
    print("  航空呼号音标拼写:")
    for callsign in callsigns:
        phonetic = pronounce_callsign(callsign)
        print(f"    {callsign:8s} -> {phonetic}")
    
    # 2. 海事通信
    print("\n2. 海事通信 - 船舶呼号")
    print("-" * 40)
    
    ship_callsigns = [
        'WABC',      # 美国注册船舶
        'GBTT',      # 英国注册船舶
        'FNRT',      # 法国注册船舶
    ]
    
    print("  船舶呼号音标拼写:")
    for callsign in ship_callsigns:
        phonetic = pronounce_callsign(callsign)
        print(f"    {callsign:8s} -> {phonetic}")
    
    # 3. 业余无线电
    print("\n3. 业余无线电 - 业余电台呼号")
    print("-" * 40)
    
    ham_callsigns = [
        'W1AW',      # ARRL 总部电台
        'K1ABC',     # 美国业余电台
        'VK3XYZ',    # 澳大利亚业余电台
        'JA1ABC',    # 日本业余电台
    ]
    
    print("  业余电台呼号音标拼写:")
    for callsign in ham_callsigns:
        phonetic = pronounce_callsign(callsign)
        print(f"    {callsign:8s} -> {phonetic}")
    
    # 4. 紧急通信
    print("\n4. 紧急通信 - MAYDAY 和 PAN-PAN")
    print("-" * 40)
    
    print("  紧急呼叫格式:")
    print(f"    MAYDAY -> {encode('MAYDAY')}")
    print(f"    PAN-PAN -> {encode('PANPAN')}")
    print(f"    SOS -> {encode('SOS')}")
    
    # 5. 数字通信
    print("\n5. 数字通信 - 频率和高度")
    print("-" * 40)
    
    frequencies = ['121.5', '123.45', '118.1']
    print("  频率发音:")
    for freq in frequencies:
        phonetic = encode(freq)
        print(f"    {freq:8s} MHz -> {phonetic}")
    
    altitudes = ['35000', '10000', '5500']
    print("\n  高度发音:")
    for alt in altitudes:
        phonetic = encode(alt)
        print(f"    {alt:8s} ft -> {phonetic}")
    
    # 6. 飞机尾号
    print("\n6. 飞机尾号 - N号码")
    print("-" * 40)
    
    tail_numbers = [
        'N12345',    # 美国注册飞机
        'G-ABCD',    # 英国注册飞机
        'F-WXYZ',    # 法国注册飞机
    ]
    
    print("  飞机尾号音标拼写:")
    for tail in tail_numbers:
        phonetic = encode(tail)
        print(f"    {tail:8s} -> {phonetic}")
    
    # 7. 验证呼号
    print("\n7. 验证呼号 - 检查有效字符")
    print("-" * 40)
    
    test_callsigns = ['ABC123', 'KLM-456', 'TEST@01', 'N123AB']
    
    print("  呼号验证:")
    for callsign in test_callsigns:
        valid, spelling = verify_callsign(callsign)
        status = "✓ 有效" if valid else "✗ 包含无效字符"
        print(f"    {callsign:8s} {status}")
        if not valid:
            print(f"            问题位置: {spelling}")
    
    # 8. 电话号码
    print("\n8. 电话号码 - 无线电话音通信")
    print("-" * 40)
    
    phone_numbers = [
        '911',           # 紧急号码
        '1-800-FLOWERS',  # 免费号码
        '+1-555-123-4567', # 国际号码
    ]
    
    print("  电话号码发音:")
    for phone in phone_numbers:
        phonetic = pronounce_phone_number(phone)
        print(f"    {phone:20s} -> {phonetic}")
    
    # 9. 无线电通话示例
    print("\n9. 无线电通话示例")
    print("-" * 40)
    
    # 创建通话示例
    converter = NATOConverter()
    
    messages = [
        ('KLM123', 'Line up and wait, runway 27'),
        ('UAL456', 'Cleared to land, runway 27L'),
        ('BAW789', 'Contact Tower 118.1'),
    ]
    
    print("  模拟航空通话:")
    for callsign, message in messages:
        print(f"\n    [{callsign}] {message}")
        print(f"    呼号音标: {converter.encode(callsign)}")
        if 'runway' in message.lower():
            rw = ''.join(c for c in message if c.isdigit())
            if rw:
                print(f"    跑道音标: {converter.encode('RW' + rw)}")
    
    # 10. 解码接收信息
    print("\n10. 解码接收信息")
    print("-" * 40)
    
    received = [
        'Alpha Bravo Charlie',
        'Kilo Lima Mike One Two Three',
        'Victor Alpha November Romeo Alpha',
    ]
    
    print("  接收信息解码:")
    for msg in received:
        decoded = decode(msg)
        print(f"    {msg:40s} -> {decoded}")
    
    print("\n" + "=" * 60)
    print("无线电通信示例完成")
    print("=" * 60)
    print("\n提示: 在实际无线电通信中:")
    print("  - 使用标准 NATO 音标字母")
    print("  - 数字逐位发音")
    print("  - 小数点读作 'Decimal'")
    print("  - 保持清晰和稳定的语速")


if __name__ == '__main__':
    main()