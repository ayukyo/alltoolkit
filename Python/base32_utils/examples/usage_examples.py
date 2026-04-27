"""
Base32 工具模块使用示例

演示三种 Base32 编码方案的使用方法
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base32_utils.mod import (
    Base32Encoder,
    Base32HexEncoder,
    CrockfordBase32Encoder,
    Base32Utils,
    encode, decode, encode_string, decode_string, generate_id
)


def example_standard_base32():
    """标准 Base32 编码示例"""
    print("=" * 60)
    print("标准 Base32 (RFC 4648) 示例")
    print("=" * 60)
    
    encoder = Base32Encoder()
    
    # 示例 1: 基本字符串编码
    print("\n1. 基本字符串编码")
    text = "Hello, Base32!"
    data = text.encode('utf-8')
    encoded = encoder.encode(data)
    decoded = encoder.decode(encoded)
    
    print(f"   原始文本: {text}")
    print(f"   编码结果: {encoded}")
    print(f"   解码结果: {decoded.decode('utf-8')}")
    print(f"   验证成功: {data == decoded}")
    
    # 示例 2: 二进制数据编码
    print("\n2. 二进制数据编码")
    binary_data = bytes([0x00, 0x01, 0x02, 0xFF, 0xFE, 0xFD])
    encoded = encoder.encode(binary_data)
    decoded = encoder.decode(encoded)
    
    print(f"   原始数据: {binary_data.hex()}")
    print(f"   编码结果: {encoded}")
    print(f"   验证成功: {binary_data == decoded}")
    
    # 示例 3: 文件内容模拟
    print("\n3. 模拟文件内容编码")
    file_content = b"""#!/usr/bin/env python3
print("Hello, World!")
"""
    encoded = encoder.encode(file_content)
    decoded = encoder.decode(encoded)
    
    print(f"   文件大小: {len(file_content)} 字节")
    print(f"   编码长度: {len(encoded)} 字符")
    print(f"   验证成功: {file_content == decoded}")
    
    print()


def example_base32hex():
    """Base32Hex 编码示例"""
    print("=" * 60)
    print("Base32Hex (十六进制风格) 示例")
    print("=" * 60)
    
    encoder = Base32HexEncoder()
    
    # 示例 1: 与标准 Base32 对比
    print("\n1. 与标准 Base32 对比")
    standard_encoder = Base32Encoder()
    data = b"test data"
    
    standard_encoded = standard_encoder.encode(data)
    hex_encoded = encoder.encode(data)
    
    print(f"   原始数据: {data}")
    print(f"   标准 Base32: {standard_encoded}")
    print(f"   Base32Hex:   {hex_encoded}")
    print(f"   使用字符集: 0-9, A-V (而非 A-Z, 2-7)")
    
    # 示例 2: 适合数字处理的场景
    print("\n2. UUID 风格数据编码")
    uuid_like = bytes([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0,
                      0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
    encoded = encoder.encode(uuid_like)
    decoded = encoder.decode(encoded)
    
    print(f"   UUID 数据: {uuid_like.hex()}")
    print(f"   Base32Hex: {encoded.rstrip('=')}")
    print(f"   验证成功: {uuid_like == decoded}")
    
    print()


def example_crockford_base32():
    """Crockford's Base32 编码示例"""
    print("=" * 60)
    print("Crockford's Base32 示例")
    print("=" * 60)
    
    encoder = CrockfordBase32Encoder()
    
    # 示例 1: URL 友好的 ID
    print("\n1. 生成 URL 友好的 ID")
    import secrets
    random_bytes = secrets.token_bytes(8)
    encoded = encoder.encode(random_bytes)
    
    print(f"   随机字节: {random_bytes.hex()}")
    print(f"   编码 ID: {encoded}")
    print(f"   字符集: 0-9, A-H, J-K, M-N, P-T, V-Z (排除 I,L,O,U)")
    
    # 示例 2: 带校验位
    print("\n2. 带校验位的编码")
    product_key = b"PROD12345"
    encoded_no_checksum = encoder.encode(product_key)
    encoded_with_checksum = encoder.encode(product_key, checksum=True)
    
    print(f"   产品数据: {product_key}")
    print(f"   无校验位: {encoded_no_checksum}")
    print(f"   有校验位: {encoded_with_checksum}")
    
    # 验证校验位
    try:
        decoded = encoder.decode(encoded_with_checksum, verify_checksum=True)
        print(f"   校验验证: 通过 ✓")
    except ValueError as e:
        print(f"   校验验证: 失败 - {e}")
    
    # 示例 3: 用户友好的序列号
    print("\n3. 用户友好的序列号")
    serial_data = secrets.token_bytes(10)
    serial = encoder.encode(serial_data)
    formatted = "-".join([serial[i:i+4] for i in range(0, len(serial), 4)])
    
    print(f"   原始数据: {serial_data.hex()}")
    print(f"   序列号:   {formatted}")
    print(f"   长度:     {len(serial)} 字符")
    
    # 示例 4: 处理用户输入（自动处理混淆字符）
    print("\n4. 处理用户输入（混淆字符自动映射）")
    data = b"test"
    encoded = encoder.encode(data)
    
    # 用户可能输入 'O' 代替 '0', 'I' 或 'L' 代替 '1'
    user_inputs = [
        encoded,
        encoded.replace('0', 'O'),  # O -> 0
        encoded.replace('1', 'I'),   # I -> 1
        encoded.replace('1', 'L'),   # L -> 1
    ]
    
    print(f"   正确编码: {encoded}")
    for i, user_input in enumerate(user_inputs):
        decoded = encoder.decode(user_input)
        print(f"   用户输入 {i+1}: {user_input} -> 解码成功 ✓")
    
    print()


def example_utility_functions():
    """便捷工具函数示例"""
    print("=" * 60)
    print("便捷工具函数示例")
    print("=" * 60)
    
    # 示例 1: 快速编解码
    print("\n1. 快速编解码")
    data = b"Quick encode test"
    encoded = encode(data)
    decoded = decode(encoded)
    print(f"   原始数据: {data}")
    print(f"   编码结果: {encoded}")
    print(f"   解码结果: {decoded}")
    
    # 示例 2: 字符串直接处理
    print("\n2. 字符串直接处理")
    text = "你好，世界！"
    encoded = encode_string(text)
    decoded = decode_string(encoded)
    print(f"   原始文本: {text}")
    print(f"   编码结果: {encoded}")
    print(f"   解码结果: {decoded}")
    
    # 示例 3: 随机 ID 生成
    print("\n3. 随机 ID 生成")
    print("   生成 5 个 12 位随机 ID:")
    for i in range(5):
        random_id = generate_id(12)
        print(f"     ID {i+1}: {random_id}")
    
    # 示例 4: 不同变体切换
    print("\n4. 不同变体切换")
    data = b"variant test"
    
    standard = Base32Utils.encode(data, "standard")
    hex_variant = Base32Utils.encode(data, "hex")
    crockford = Base32Utils.encode(data, "crockford")
    
    print(f"   原始数据: {data}")
    print(f"   标准:     {standard}")
    print(f"   Hex:      {hex_variant}")
    print(f"   Crockford: {crockford}")
    
    print()


def example_real_world_scenarios():
    """实际应用场景示例"""
    print("=" * 60)
    print("实际应用场景示例")
    print("=" * 60)
    
    # 场景 1: 短链接生成
    print("\n1. 短链接生成")
    import hashlib
    
    # 模拟长 URL
    long_url = "https://example.com/products/category/item/12345/details?ref=homepage&utm_source=newsletter"
    url_hash = hashlib.sha256(long_url.encode()).digest()[:8]  # 取前 8 字节
    short_code = Base32Utils.encode(url_hash, "crockford")
    
    print(f"   长链接: {long_url[:50]}...")
    print(f"   哈希:   {url_hash.hex()}")
    print(f"   短码:   {short_code}")
    print(f"   短链接: https://s.example/{short_code}")
    
    # 场景 2: 邀请码生成
    print("\n2. 邀请码生成")
    import secrets
    
    # 生成带校验位的邀请码
    invite_bytes = secrets.token_bytes(6)
    invite_code = Base32Utils.crockford_encode_with_checksum(invite_bytes)
    formatted = Base32Utils.format_with_separator(invite_code, 4, "-")
    
    print(f"   原始数据: {invite_bytes.hex()}")
    print(f"   邀请码:   {formatted}")
    
    # 验证邀请码
    try:
        cleaned = Base32Utils.strip_separator(formatted, "-")
        Base32Utils.crockford_decode_with_verify(cleaned)
        print(f"   验证:     有效 ✓")
    except ValueError:
        print(f"   验证:     无效 ✗")
    
    # 场景 3: 二进制数据传输
    print("\n3. 二进制数据传输（如配置文件）")
    config = {
        "host": "example.com",
        "port": 8080,
        "secure": True,
        "api_key": "abc123"
    }
    import json
    config_json = json.dumps(config)
    encoded_config = Base32Utils.encode_string(config_json)
    
    print(f"   配置: {config}")
    print(f"   JSON: {config_json}")
    print(f"   Base32: {encoded_config[:50]}...")
    
    # 解码
    decoded_config = Base32Utils.decode_string(encoded_config)
    restored = json.loads(decoded_config)
    print(f"   解码验证: {restored == config} ✓")
    
    # 场景 4: 数据库主键友好的 ID
    print("\n4. 数据库主键友好的 ID")
    for i in range(3):
        # 模拟数据库自增 ID
        db_id = i + 1000
        id_bytes = db_id.to_bytes(4, 'big')
        public_id = Base32Utils.encode(id_bytes, "crockford")
        print(f"   数据库 ID: {db_id:5d} -> 公开 ID: {public_id}")
    
    print()


def example_comparison():
    """编码方案对比"""
    print("=" * 60)
    print("三种编码方案对比")
    print("=" * 60)
    
    test_data = [
        b"a",
        b"ab",
        b"abc",
        b"hello",
        b"Hello, World!",
        bytes(range(10)),
    ]
    
    print(f"\n{'数据':<20} {'标准':<20} {'Hex':<20} {'Crockford':<20}")
    print("-" * 80)
    
    for data in test_data:
        standard = Base32Utils.encode(data, "standard").rstrip("=")
        hex_enc = Base32Utils.encode(data, "hex").rstrip("=")
        crockford = Base32Utils.encode(data, "crockford")
        
        if len(data) <= 10:
            display = str(data)
        else:
            display = f"{data[:5]}...{data[-3:]}"
        
        print(f"{display:<20} {standard:<20} {hex_enc:<20} {crockford:<20}")
    
    print("\n特点对比:")
    print("- 标准 Base32: RFC 4648 标准，广泛支持")
    print("- Base32Hex: 十六进制风格，适合与数字系统集成")
    print("- Crockford: 用户友好，排除混淆字符，支持校验位")
    print()


def main():
    """运行所有示例"""
    example_standard_base32()
    example_base32hex()
    example_crockford_base32()
    example_utility_functions()
    example_real_world_scenarios()
    example_comparison()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()