"""
Encoding Utilities 使用示例

展示编码处理工具的各种用法。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    # Base64
    base64_encode, base64_decode, base64_encode_json, base64_decode_json,
    
    # Base32
    base32_encode, base32_decode,
    
    # Base58
    base58_encode, base58_decode,
    
    # Base85
    base85_encode, base85_decode,
    
    # URL
    url_encode, url_decode, url_encode_query, url_decode_query, url_encode_all,
    
    # Hex
    hex_encode, hex_decode, hex_encode_with_prefix, hex_decode_with_prefix,
    
    # Quoted-printable
    quoted_printable_encode, quoted_printable_decode,
    
    # Unicode
    unicode_normalize_nfc, unicode_normalize_nfd, unicode_normalize_nfkc,
    unicode_normalize_nfkd, unicode_remove_accents, unicode_is_normalized,
    
    # 检测
    detect_encoding, auto_decode,
    
    # 信息
    get_encoding_info, count_bytes, get_unicode_name, get_unicode_category,
    
    # 批量操作
    batch_encode, batch_decode,
    
    # 转换
    convert_encoding,
)


def print_section(title):
    """打印章节标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    print_section("Base64 编码示例")
    
    # 基础编码
    print("\n  基础编码:")
    text = "Hello World!"
    encoded = base64_encode(text)
    print(f"    原文: {text}")
    print(f"    Base64: {encoded}")
    
    decoded = base64_decode(encoded).decode()
    print(f"    解码: {decoded}")
    
    # URL-safe 编码
    print("\n  URL-safe 编码:")
    binary_data = bytes(range(256))
    encoded = base64_encode(binary_data, url_safe=True)
    print(f"    长度: {len(encoded)}")
    print(f"    包含 +: {'+' in encoded}")
    print(f"    包含 /: {'/' in encoded}")
    
    # JSON 编码
    print("\n  JSON 编码:")
    obj = {"name": "张三", "age": 25, "city": "北京"}
    encoded = base64_encode_json(obj)
    print(f"    JSON: {obj}")
    print(f"    Base64: {encoded}")
    
    decoded = base64_decode_json(encoded)
    print(f"    解码: {decoded}")
    
    print_section("Base32 编码示例")
    
    # 基础编码
    text = "Hello"
    encoded = base32_encode(text)
    print(f"\n  原文: {text}")
    print(f"  Base32: {encoded}")
    
    decoded = base32_decode(encoded).decode()
    print(f"  解码: {decoded}")
    
    # Base32Hex
    print("\n  Base32Hex 变体:")
    encoded_hex = base32_encode(text, hex_variant=True)
    print(f"    Base32Hex: {encoded_hex}")
    
    decoded = base32_decode(encoded_hex, hex_variant=True).decode()
    print(f"    解码: {decoded}")
    
    print_section("Base58 编码示例")
    
    # 基础编码
    text = "Hello World"
    encoded = base58_encode(text)
    print(f"\n  原文: {text}")
    print(f"  Base58: {encoded}")
    
    decoded = base58_decode(encoded).decode()
    print(f"  解码: {decoded}")
    
    # Bitcoin 地址示例
    print("\n  Bitcoin 应用:")
    # 假设的地址数据
    addr_data = bytes.fromhex("00" + "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"[:40])
    encoded_addr = base58_encode(addr_data)
    print(f"    地址数据编码: {encoded_addr[:20]}...")
    
    print_section("Base85 编码示例")
    
    # Ascii85
    text = "Hello World"
    encoded = base85_encode(text)
    print(f"\n  Ascii85 编码:")
    print(f"    原文: {text}")
    print(f"    编码: {encoded}")
    
    decoded = base85_decode(encoded).decode()
    print(f"    解码: {decoded}")
    
    # Z85
    print("\n  Z85 变体:")
    encoded_z85 = base85_encode(text, variant='z85')
    print(f"    Z85: {encoded_z85}")
    
    decoded = base85_decode(encoded_z85, variant='z85').decode()
    print(f"    解码: {decoded}")
    
    print_section("URL 编码示例")
    
    # 基础编码
    text = "Hello World! 你好"
    encoded = url_encode(text)
    print(f"\n  原文: {text}")
    print(f"  URL 编码: {encoded}")
    
    decoded = url_decode(encoded)
    print(f"  解码: {decoded}")
    
    # 查询参数
    print("\n  查询参数:")
    params = {"name": "张三", "age": 25, "search": "你好 world"}
    encoded = url_encode_query(params)
    print(f"    参数: {params}")
    print(f"    编码: {encoded}")
    
    decoded = url_decode_query(encoded)
    print(f"    解码: {decoded}")
    
    # 全编码
    print("\n  全字符编码:")
    text = "Hello"
    encoded = url_encode_all(text)
    print(f"    原文: {text}")
    print(f"    全编码: {encoded}")
    
    print_section("Hex 编码示例")
    
    # 基础编码
    text = "Hello"
    encoded = hex_encode(text)
    print(f"\n  原文: {text}")
    print(f"  Hex: {encoded}")
    
    decoded = hex_decode(encoded).decode()
    print(f"  解码: {decoded}")
    
    # 带前缀
    print("\n  带 0x 前缀:")
    encoded = hex_encode_with_prefix(text)
    print(f"    编码: {encoded}")
    
    decoded = hex_decode_with_prefix(encoded).decode()
    print(f"    解码: {decoded}")
    
    print_section("Quoted-printable 编码示例")
    
    # ASCII 文本
    text = "Hello World"
    encoded = quoted_printable_encode(text)
    print(f"\n  ASCII 文本:")
    print(f"    原文: {text}")
    print(f"    编码: {encoded}")
    
    # Unicode 文本
    text = "你好世界 Hello World"
    encoded = quoted_printable_encode(text)
    print(f"\n  Unicode 文本:")
    print(f"    原文: {text}")
    print(f"    编码: {encoded[:50]}...")
    
    decoded = quoted_printable_decode(encoded).decode()
    print(f"    解码: {decoded}")
    
    print_section("Unicode 规范化示例")
    
    # NFC 规范化
    print("\n  NFC 规范化（预组合）:")
    text = "café"  # 可能是组合或预组合
    normalized = unicode_normalize_nfc(text)
    print(f"    输入: {text}")
    print(f"    NFC: {normalized}")
    print(f"    长度: {len(normalized)}")
    
    # NFD 规范化
    print("\n  NFD 规范化（分解）:")
    normalized = unicode_normalize_nfd(text)
    print(f"    输入: {text}")
    print(f"    NFD: {normalized}")
    print(f"    长度: {len(normalized)}")
    
    # NFKC 规范化
    print("\n  NFKC 规范化（兼容性）:")
    text = "Ａ１２３"  # 全角字符
    normalized = unicode_normalize_nfkc(text)
    print(f"    输入: {text}")
    print(f"    NFKC: {normalized}")
    
    # 移除重音
    print("\n  移除重音符号:")
    words = ["café", "über", "naïve", "résumé"]
    for word in words:
        clean = unicode_remove_accents(word)
        print(f"    {word} → {clean}")
    
    print_section("编码检测示例")
    
    # 自动检测
    samples = [
        "SGVsbG8gV29ybGQh",
        "48656c6c6f20776f726c64",
        "Hello%20World",
        "=E4=BD=A0=E5=A5=BD",
        "普通文本",
    ]
    
    print("\n  自动检测编码类型:")
    for sample in samples:
        encoding = detect_encoding(sample)
        print(f"    '{sample[:30]}...' → {encoding}")
    
    # 自动解码
    print("\n  自动解码:")
    samples = [
        "SGVsbG8gV29ybGQh",  # Base64
        "48656c6c6f",        # Hex
        "Hello%20World",     # URL
    ]
    for sample in samples:
        decoded, encoding = auto_decode(sample)
        print(f"    '{sample}' → '{decoded}' (encoding: {encoding})")
    
    print_section("编码信息示例")
    
    text = "Hello 你好 世界 🌍"
    info = get_encoding_info(text)
    
    print(f"\n  文本: {text}")
    print(f"  字符数: {info['length']}")
    print(f"  字节数: {info['byte_length']}")
    print(f"  含 Unicode: {info['has_unicode']}")
    print(f"  Unicode 字符: {info['unicode_chars']}")
    print(f"  含重音: {info['has_accents']}")
    print(f"  规范化状态: {info['is_normalized']}")
    
    # Unicode 名称和分类
    print("\n  Unicode 名称和分类:")
    chars = ['A', '中', '🎉', ' ']
    for char in chars:
        name = get_unicode_name(char)
        category = get_unicode_category(char)
        print(f"    '{char}' → 名称: {name}, 分类: {category}")
    
    print_section("批量操作示例")
    
    # 批量编码
    items = ["Hello", "World", "你好", "世界"]
    
    print("\n  批量 Base64 编码:")
    encoded = batch_encode(items, 'base64')
    for i, e in enumerate(encoded):
        print(f"    {items[i]} → {e}")
    
    print("\n  批量 Hex 编码:")
    encoded = batch_encode(items, 'hex')
    for i, e in enumerate(encoded):
        print(f"    {items[i]} → {e}")
    
    print("\n  批量 URL 编码:")
    encoded = batch_encode(items, 'url')
    for i, e in enumerate(encoded):
        print(f"    {items[i]} → {e}")
    
    # 批量解码
    print("\n  批量 Base64 解码:")
    encoded_items = ["SGVsbG8", "World", "5L2g5aW9", "5LiW55WM"]
    decoded = batch_decode(encoded_items, 'base64')
    for i, d in enumerate(decoded):
        print(f"    {encoded_items[i]} → {d}")
    
    print_section("编码转换示例")
    
    # Base64 → Hex
    print("\n  Base64 → Hex:")
    base64_str = "SGVsbG8="
    hex_str = convert_encoding(base64_str, 'base64', 'hex')
    print(f"    {base64_str} → {hex_str}")
    
    # Hex → Base64
    print("\n  Hex → Base64:")
    hex_str = "48656c6c6f"
    base64_str = convert_encoding(hex_str, 'hex', 'base64')
    print(f"    {hex_str} → {base64_str}")
    
    # URL → Hex
    print("\n  URL → Hex:")
    url_str = "Hello%20World"
    hex_str = convert_encoding(url_str, 'url', 'hex')
    print(f"    {url_str} → {hex_str}")
    
    print_section("字节计数示例")
    
    texts = [
        "Hello",
        "你好",
        "Hello 你好",
        "🎉🌍💻",
    ]
    
    encodings = ['utf-8', 'gbk', 'utf-16']
    
    print("\n  不同编码的字节数:")
    for text in texts:
        print(f"\n  文本: '{text}'")
        for encoding in encodings:
            try:
                bytes_count = count_bytes(text, encoding)
                print(f"    {encoding}: {bytes_count} 字节")
            except:
                print(f"    {encoding}: 无法编码")
    
    print_section("完整总结")
    
    print("""
  Encoding Utilities 提供的功能总结:
  
  ✓ Base64 - 标准和 URL-safe 编码，JSON 编解码
  ✓ Base32 - 标准和 Hex 变体
  ✓ Base58 - Bitcoin 和 Flickr 字母表
  ✓ Base85 - Ascii85 和 Z85 变体
  ✓ URL - 编解码、查询参数、全编码
  ✓ Hex - 十六进制编解码，支持 0x 前缀
  ✓ Quoted-printable - 邮件编码格式
  ✓ Unicode - NFC/NFD/NFKC/NFKD 规范化，移除重音
  ✓ 检测 - 自动检测编码类型并解码
  ✓ 信息 - 编码信息、字节计数、Unicode 名称
  ✓ 批量 - 批量编解码
  ✓ 转换 - 编码格式互转
  
  零外部依赖，纯 Python 实现！
    """)


if __name__ == "__main__":
    main()