#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hash Utils - Basic Usage Examples

演示 hash_utils 模块的基本用法。
"""

import sys
import os

# Add parent directory (hash_utils) to path for mod import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    md5, sha1, sha256, sha512, hash, hash_algorithms,
    hmac_hash, hmac_verify,
    hex_to_base64, base64_to_hex,
    IncrementalHasher,
    crc32, crc32_hex
)


def main():
    print("="*60)
    print("Hash Utils - Basic Usage Examples")
    print("="*60)
    print()
    
    # 1. 基本哈希
    print("1. 基本哈希函数")
    print("-"*60)
    data = "Hello, AllToolkit!"
    print(f"输入数据：{data}")
    print(f"  MD5:    {md5(data)}")
    print(f"  SHA1:   {sha1(data)}")
    print(f"  SHA256: {sha256(data)}")
    print(f"  SHA512: {sha512(data)[:64]}...")
    print()
    
    # 2. 使用通用 hash 函数
    print("2. 通用 hash 函数")
    print("-"*60)
    for algo in ['md5', 'sha1', 'sha256']:
        h = hash(data, algo)
        print(f"  {algo.upper()}: {h}")
    print()
    
    # 3. 支持的算法
    print("3. 支持的哈希算法")
    print("-"*60)
    print(f"  共 {len(hash_algorithms())} 种算法:")
    for algo in hash_algorithms():
        print(f"    - {algo}")
    print()
    
    # 4. HMAC
    print("4. HMAC 消息认证码")
    print("-"*60)
    secret_key = "my-secret-key-2024"
    message = "This is a secure message"
    
    mac = hmac_hash(message, secret_key)
    print(f"  密钥：{secret_key}")
    print(f"  消息：{message}")
    print(f"  HMAC-SHA256: {mac}")
    
    # 验证
    is_valid = hmac_verify(message, secret_key, mac)
    print(f"  验证结果：{'✓ 有效' if is_valid else '✗ 无效'}")
    
    # 验证篡改的消息
    is_tampered = hmac_verify("Tampered message", secret_key, mac)
    print(f"  篡改验证：{'✓ 检测到篡改' if not is_tampered else '✗ 未检测到'}")
    print()
    
    # 5. 编码转换
    print("5. 编码转换")
    print("-"*60)
    original = "Hello"
    hex_val = original.encode().hex()
    base64_val = hex_to_base64(hex_val)
    
    print(f"  原始文本：{original}")
    print(f"  十六进制：{hex_val}")
    print(f"  Base64:   {base64_val}")
    print(f"  还原验证：{base64_to_hex(base64_val) == hex_val}")
    print()
    
    # 6. 增量哈希
    print("6. 增量哈希（流式处理）")
    print("-"*60)
    hasher = IncrementalHasher('sha256')
    
    chunks = ["Hello, ", "world", "!"]
    for i, chunk in enumerate(chunks, 1):
        hasher.update(chunk)
        print(f"  第 {i} 块：'{chunk}'")
    
    print(f"  最终哈希：{hasher.hexdigest()}")
    
    # 验证与批量哈希一致
    bulk_hash = sha256("".join(chunks))
    print(f"  批量哈希：{bulk_hash}")
    print(f"  结果一致：{hasher.hexdigest() == bulk_hash}")
    print()
    
    # 7. CRC32 校验和
    print("7. CRC32 校验和")
    print("-"*60)
    test_data = "File content for checksum"
    print(f"  数据：{test_data}")
    print(f"  CRC32:     {crc32(test_data)}")
    print(f"  CRC32 Hex: {crc32_hex(test_data)}")
    print()
    
    # 8. Unicode 支持
    print("8. Unicode 支持")
    print("-"*60)
    unicode_tests = [
        "你好世界",           # 中文
        "こんにちは",         # 日文
        "Привет мир",        # 俄文
        "🌍🚀💻",             # Emoji
        "Mixed 混合 смешанны", # 混合
    ]
    
    for text in unicode_tests:
        h = sha256(text)
        print(f"  '{text}' -> {h[:32]}...")
    print()
    
    print("="*60)
    print("示例完成！")
    print("="*60)


if __name__ == "__main__":
    main()
