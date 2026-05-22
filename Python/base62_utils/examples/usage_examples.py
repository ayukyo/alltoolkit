"""
Base62 Utilities 使用示例

展示 Base62 编码工具的各种使用场景。
"""

import sys
import os

# 修正路径：从 examples 目录向上两级找到 Python 目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base62_utils.mod import (
    Base62Encoder,
    encode, decode,
    encode_bytes, decode_bytes,
    encode_uuid, decode_uuid,
    encode_snowflake, decode_snowflake,
    generate_short_id,
    generate_time_based_id,
    is_valid,
    URL_FRIENDLY_CHARSET,
)


def example_basic_encoding():
    """基础整数编解码示例"""
    print("\n=== 基础整数编解码 ===")
    
    # 使用便捷函数
    num = 123456789
    encoded = encode(num)
    decoded = decode(encoded)
    
    print(f"整数 {num} 编码为: {encoded}")
    print(f"解码回整数: {decoded}")
    
    # 使用编码器类
    encoder = Base62Encoder()
    
    # 编码一系列数字
    numbers = [0, 61, 62, 3844, 238327]
    for n in numbers:
        e = encoder.encode_int(n)
        print(f"  {n} → {e}")


def example_bytes_encoding():
    """字节流编解码示例"""
    print("\n=== 字节流编解码 ===")
    
    # 编码字符串
    text = "Hello, Base62!"
    encoded = encode_bytes(text.encode('utf-8'))
    decoded = decode_bytes(encoded).decode('utf-8')
    
    print(f"文本 '{text}' 编码为: {encoded}")
    print(f"解码回文本: '{decoded}'")
    
    # 编码二进制数据
    binary_data = bytes([0, 127, 255, 128, 64])
    encoded = encode_bytes(binary_data)
    decoded = decode_bytes(encoded, len(binary_data))
    
    print(f"二进制数据 {list(binary_data)} 编码为: {encoded}")
    print(f"解码回: {list(decoded)}")


def example_uuid_encoding():
    """UUID 编码示例"""
    print("\n=== UUID 编码 ===")
    
    # 标准 UUID 转 Base62 (用于 URL 短链接)
    uuid = "550e8400-e29b-41d4-a716-446655440000"
    encoded = encode_uuid(uuid)
    
    print(f"UUID: {uuid} (36字符)")
    print(f"Base62: {encoded} ({len(encoded)}字符)")
    print(f"缩短比例: {36 / len(encoded):.1f}x")
    
    # 解码回 UUID
    decoded = decode_uuid(encoded)
    print(f"解码回: {decoded}")
    
    # 应用场景：API 资源标识符
    print("\n应用场景：")
    print(f"  原始 URL: /api/users/550e8400-e29b-41d4-a716-446655440000")
    print(f"  短 URL: /api/users/{encoded}")


def example_snowflake_encoding():
    """雪花 ID 编码示例"""
    print("\n=== 雪花 ID 编码 ===")
    
    # 模拟雪花 ID (通常是分布式系统生成的唯一 ID)
    snowflake_id = 1234567890123456789
    
    encoded = encode_snowflake(snowflake_id)
    decoded = decode_snowflake(encoded)
    
    print(f"雪花 ID: {snowflake_id}")
    print(f"Base62 编码: {encoded} ({len(encoded)}字符)")
    print(f"解码验证: {decoded}")
    
    # 与原始 ID 长度对比
    print(f"\n对比:")
    print(f"  原始数字长度: {len(str(snowflake_id))} 字符")
    print(f"  Base62 长度: {len(encoded)} 字符")
    print(f"  缩短比例: {len(str(snowflake_id)) / len(encoded):.1f}x")


def example_short_id_generation():
    """短 ID 生成示例"""
    print("\n=== 短 ID 生成 ===")
    
    # 生成随机短 ID (适用于订单号、邀请码等)
    print("随机短 ID:")
    for i in range(5):
        id8 = generate_short_id(8)
        id12 = generate_short_id(12)
        print(f"  8字符: {id8}  12字符: {id12}")
    
    # 生成基于时间的 ID (有序且唯一)
    print("\n基于时间的 ID (有序):")
    for i in range(5):
        id1 = generate_time_based_id(12)
        id2 = generate_time_based_id(12)
        print(f"  {id1}  {id2}")
    
    # 应用场景
    print("\n应用场景:")
    print("  - 订单号: ORD_" + generate_short_id(10))
    print("  - 邀请码: INV_" + generate_short_id(8))
    print("  - 短链接: https://s.example.com/" + generate_short_id(6))


def example_prefix_encoding():
    """带前缀编码示例"""
    print("\n=== 带前缀编码 ===")
    
    encoder = Base62Encoder()
    
    # 生成带类型前缀的 ID
    user_id = encoder.encode_with_prefix(1001, "user_")
    order_id = encoder.encode_with_prefix(5000, "order_")
    product_id = encoder.encode_with_prefix(300, "prod_")
    
    print(f"用户 ID: {user_id}")
    print(f"订单 ID: {order_id}")
    print(f"产品 ID: {product_id}")
    
    # 解码带前缀的 ID
    prefix, num = encoder.decode_with_prefix(user_id)
    print(f"\n解码 '{user_id}': 前缀={prefix}, ID={num}")


def example_url_friendly_encoding():
    """URL 友好编码示例"""
    print("\n=== URL 友好编码 ===")
    
    # 使用小写字母优先的字符集 (更易读)
    url_encoder = Base62Encoder(URL_FRIENDLY_CHARSET)
    
    # 编码对比
    num = 123456789
    default_encoded = encode(num)  # 默认字符集
    url_encoded = url_encoder.encode_int(num)  # URL 友好字符集
    
    print(f"数字: {num}")
    print(f"默认编码: {default_encoded}")
    print(f"URL友好: {url_encoded}")
    
    # URL 应用
    print("\nURL 应用:")
    print(f"  https://example.com/share/{url_encoder.generate_short_id(6)}")
    print(f"  https://example.com/file/{url_encoder.encode_int(12345)}")


def example_validation():
    """有效性验证示例"""
    print("\n=== 有效性验证 ===")
    
    test_strings = [
        "abc123",
        "ABCXYZ",
        "aB3xY9zQ",
        "hello!",  # 包含非法字符
        "test-123",  # 包含非法字符
        "",
    ]
    
    for s in test_strings:
        valid = is_valid(s)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  '{s}' → {status}")


def example_custom_charset():
    """自定义字符集示例"""
    print("\n=== 自定义字符集 ===")
    
    # 自定义字符集（避免易混淆字符）
    # 移除: 0 (与 O 混淆), 1 (与 I/l 混淆), l (与 1/I 混淆), O (与 0 混淆)
    custom_charset = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    try:
        encoder = Base62Encoder(custom_charset)
        
        num = 123456789
        encoded = encoder.encode_int(num)
        decoded = encoder.decode_int(encoded)
        
        print(f"自定义字符集 (移除易混淆字符):")
        print(f"  数字 {num} → {encoded}")
        print(f"  解码: {decoded}")
        
        # 应用场景：用户可输入的 ID (减少输入错误)
        print("\n应用场景 (减少用户输入错误):")
        print(f"  邀请码: {encoder.generate_short_id(8)}")
        print(f"  订单号: {encoder.generate_short_id(10)}")
        
    except ValueError as e:
        # 检查字符集长度
        print(f"自定义字符集需要62个字符，当前 {len(custom_charset)} 个")


def example_real_world_use_cases():
    """真实应用场景示例"""
    print("\n=== 真实应用场景 ===")
    
    encoder = Base62Encoder()
    
    # 1. URL 短链接服务
    print("1. URL 短链接服务:")
    original_url = "https://example.com/products/12345/details?category=electronics"
    short_code = encoder.generate_short_id(6)
    print(f"  原始: {original_url}")
    print(f"  短链接: https://s.link/{short_code}")
    
    # 2. 分布式 ID 显示
    print("\n2. 分布式 ID 显示:")
    snowflake_id = 1704067200000 << 22 | 1 << 12 | 1  # 模拟雪花 ID
    encoded_id = encoder.encode_snowflake(snowflake_id)
    print(f"  内部 ID: {snowflake_id}")
    print(f"  对外显示: {encoded_id}")
    
    # 3. 资源标识符
    print("\n3. API 资源标识符:")
    resource_uuid = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    encoded_uuid = encoder.encode_uuid(resource_uuid)
    print(f"  原始: /api/v1/resources/{resource_uuid}")
    print(f"  优化: /api/v1/resources/{encoded_uuid}")
    
    # 4. 订单号/交易号
    print("\n4. 订单号/交易号:")
    order_num = encoder.generate_time_based_id(12)
    print(f"  订单号: {order_num}")
    
    # 5. 验证码/邀请码
    print("\n5. 验证码/邀请码:")
    invite_code = encoder.generate_short_id(6)
    print(f"  邀请码: {invite_code}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Base62 Utilities 使用示例")
    print("=" * 60)
    
    example_basic_encoding()
    example_bytes_encoding()
    example_uuid_encoding()
    example_snowflake_encoding()
    example_short_id_generation()
    example_prefix_encoding()
    example_url_friendly_encoding()
    example_validation()
    example_custom_charset()
    example_real_world_use_cases()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()