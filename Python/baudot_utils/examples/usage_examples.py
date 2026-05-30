"""
baudot_utils 使用示例

演示baudot_utils 模块的各种用法。

Author: AllToolkit
Date: 2026-05-31
"""

from baudot_utils.mod import (
    encode, decode, encode_char,
    encode_to_bits, decode_from_bits,
    encode_to_hex, decode_from_hex,
    bits_to_bauds,
    get_letters_table, get_figures_table, lookup_code,
    bauds_to_text, text_to_bauds,
    encode_text_to_bits, decode_bits_to_text,
)


def example_basic():
    """基础用法：文本与博多码互转"""
    print("=== 基础用法 ===")
    
    text = "HELLO"
    codes = encode(text)
    print(f"文本: {text!r}")
    print(f"博多码值: {codes}")
    
    decoded = decode(codes)
    print(f"解码结果: {decoded!r}")
    print()


def example_text_to_bits():
    """文本 → 二进制字符串"""
    print("=== 文本转二进制 ===")
    
    bits = encode_text_to_bits("HI")
    print(f"HELLO 的二进制表示: {bits}")
    
    # 还原
    text = decode_bits_to_text("01000 00110")
    print(f"解码: {text!r}")
    print()


def example_hex_encoding():
    """博多码与十六进制字符串互转"""
    print("=== 十六进制编码 ===")
    
    text = "TEST"
    codes = encode(text)
    hex_str = encode_to_hex(codes)
    print(f"文本: {text!r}")
    print(f"十六进制: {hex_str}")
    
    # 还原
    recovered_codes = decode_from_hex(hex_str)
    print(f"还原的码值: {recovered_codes}")
    print(f"还原的文本: {decode(recovered_codes)!r}")
    print()


def example_bitstream():
    """比特流解析"""
    print("=== 比特流解析 ===")
    
    bitstream = "0100000110001111100101"
    codes = bits_to_bauds(bitstream)
    print(f"比特流: {bitstream}")
    print(f"解析为码值: {codes}")
    print()


def example_tables():
    """码表查询"""
    print("=== 码表查询 ===")
    
    # 打印完整的 LTRS 表
    print("LTRS 码表 (字母模式):")
    ltrs = get_letters_table()
    for code, char in ltrs.items():
        if char:
            print(f"  0x{code:02X} ({code:2d}): {char!r}")
    
    print()
    print("FIGS 码表 (数字/符号模式):")
    figs = get_figures_table()
    for code, char in figs.items():
        if char:
            print(f"  0x{code:02X} ({code:2d}): {char!r}")
    print()


def example_encode_char():
    """单字符编码"""
    print("=== 单字符编码 ===")
    
    for char in ["A", "Z", "5", "1", " "]:
        code = encode_char(char, fig_mode=False)
        fig_code = encode_char(char, fig_mode=True) if char not in (" ", "\n") else None
        print(f"  '{char}': LTRS=0x{code:02X},FIGS={f'0x{fig_code:02X}' if fig_code else 'N/A'}")
    print()


def example_longer_message():
    """较长消息的完整流程"""
    print("=== 完整流程示例 ===")
    
    text = "HELLO WORLD"
    print(f"原文: {text!r}")
    
    # 编码
    codes = encode(text)
    print(f"码值序列 ({len(codes)} 个): {[hex(c) for c in codes]}")
    
    # 转二进制
    bits = encode_to_bits(codes)
    print(f"二进制: {bits}")
    
    # 转十六进制存储
    hex_str = encode_to_hex(codes)
    print(f"十六进制: {hex_str}")
    
    # 解码还原
    decoded = decode(codes)
    print(f"解码: {decoded!r}")
    print()


def example_roudtrip():
    """验证往返编码"""
    print("=== 往返验证 ===")
    
    test_texts = [
        "HELLO",
        "TEST 123",
        "BAUDOT",
        "HELLO\nWORLD",
        "A",
    ]
    
    for text in test_texts:
        codes = encode(text)
        recovered = decode(codes)
        ok = recovered.strip("\x00") is not None
        print(f"  {text!r:20s} → {len(codes):2d} codes → {recovered!r:20s} [{('OK' if ok else 'FAIL')}]")
    print()


if __name__ == "__main__":
    example_basic()
    example_text_to_bits()
    example_hex_encoding()
    example_bitstream()
    example_encode_char()
    example_tables()
    example_longer_message()
    example_roudtrip()
