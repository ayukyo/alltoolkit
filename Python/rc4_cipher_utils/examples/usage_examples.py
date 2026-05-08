#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC4 Cipher Utils - 使用示例
============================

本示例展示 RC4 流加密工具的各种用法：
1. 基本加密解密
2. 字符串加密
3. 十六进制和 Base64 输出
4. RC4-drop 变体
5. 实际应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    RC4Cipher,
    RC4Drop,
    RC4Drop256,
    RC4Drop768,
    RC4Drop3072,
    rc4_encrypt,
    rc4_decrypt,
    rc4_encrypt_hex,
    rc4_decrypt_hex,
    rc4_encrypt_b64,
    rc4_decrypt_b64,
)


def example_basic_encrypt_decrypt():
    """基本加密解密示例"""
    print("=" * 60)
    print("1. 基本加密解密")
    print("=" * 60)
    
    # 使用字节密钥
    key = b'my_secret_key'
    plaintext = b'Hello, RC4 Cipher!'
    
    # 加密
    cipher = RC4Cipher(key)
    encrypted = cipher.encrypt(plaintext)
    
    # 解密（需要新实例）
    cipher2 = RC4Cipher(key)
    decrypted = cipher2.decrypt(encrypted)
    
    print(f"原始数据: {plaintext}")
    print(f"密钥: {key}")
    print(f"加密后 (hex): {encrypted.hex()}")
    print(f"解密后: {decrypted}")
    print(f"验证成功: {plaintext == decrypted}")
    print()


def example_string_encryption():
    """字符串加密示例"""
    print("=" * 60)
    print("2. 字符串加密")
    print("=" * 60)
    
    # 静态方法 - 最简单的用法
    message = "这是一条秘密消息！This is a secret message!"
    password = "mypassword123"
    
    # 加密字符串，返回 Base64
    encrypted = RC4Cipher.encrypt_string(message, password)
    print(f"原始消息: {message}")
    print(f"密码: {password}")
    print(f"加密后 (Base64): {encrypted}")
    
    # 解密
    decrypted = RC4Cipher.decrypt_string(encrypted, password)
    print(f"解密后: {decrypted}")
    print(f"验证成功: {message == decrypted}")
    print()


def example_output_formats():
    """不同输出格式示例"""
    print("=" * 60)
    print("3. 输出格式")
    print("=" * 60)
    
    key = b'encryption_key'
    data = 'Hello World'
    
    cipher = RC4Cipher(key)
    
    # 原始字节
    encrypted_bytes = cipher.encrypt(data)
    print(f"原始字节: {encrypted_bytes}")
    
    # 十六进制字符串
    cipher = RC4Cipher(key)
    encrypted_hex = cipher.encrypt_to_hex(data)
    print(f"十六进制: {encrypted_hex}")
    
    # Base64 字符串
    cipher = RC4Cipher(key)
    encrypted_b64 = cipher.encrypt_to_base64(data)
    print(f"Base64: {encrypted_b64}")
    
    # 便捷函数
    print(f"\n便捷函数:")
    print(f"hex: {rc4_encrypt_hex(data.encode(), key)}")
    print(f"b64: {rc4_encrypt_b64(data, key)}")
    print()


def example_rc4_drop_variants():
    """RC4-drop 变体示例"""
    print("=" * 60)
    print("4. RC4-drop 变体")
    print("=" * 60)
    
    key = b'secret_key'
    plaintext = b'Sensitive data that needs protection'
    
    # 标准 RC4
    standard = RC4Cipher(key)
    enc_standard = standard.encrypt(plaintext)
    
    # RC4-drop256 - 丢弃前 256 字节密钥流
    drop256 = RC4Drop256(key)
    enc_drop256 = drop256.encrypt(plaintext)
    
    # RC4-drop768 - 丢弃前 768 字节密钥流
    drop768 = RC4Drop768(key)
    enc_drop768 = drop768.encrypt(plaintext)
    
    # RC4-drop3072 - 丢弃前 3072 字节密钥流
    drop3072 = RC4Drop3072(key)
    enc_drop3072 = drop3072.encrypt(plaintext)
    
    print(f"原始数据: {plaintext}")
    print(f"标准 RC4: {enc_standard.hex()[:32]}...")
    print(f"RC4-drop256: {enc_drop256.hex()[:32]}...")
    print(f"RC4-drop768: {enc_drop768.hex()[:32]}...")
    print(f"RC4-drop3072: {enc_drop3072.hex()[:32]}...")
    
    print("\n安全提示:")
    print("- RC4 存在已知的安全漏洞")
    print("- RC4-drop 通过丢弃初始字节增强安全性")
    print("- 不推荐用于新的安全敏感应用")
    print("- 对于新应用，请使用 AES-GCM 或 ChaCha20-Poly1305")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 60)
    print("5. 便捷函数")
    print("=" * 60)
    
    key = b'my_key'
    data = b'Quick encryption'
    
    # 使用便捷函数进行快速加密
    encrypted = rc4_encrypt(data, key)
    decrypted = rc4_decrypt(encrypted, key)
    print(f"rc4_encrypt/rc4_decrypt:")
    print(f"  原始: {data}")
    print(f"  加密: {encrypted.hex()}")
    print(f"  解密: {decrypted}")
    print()
    
    # 十六进制格式
    hex_enc = rc4_encrypt_hex(data, key)
    hex_dec = rc4_decrypt_hex(hex_enc, key)
    print(f"rc4_encrypt_hex/rc4_decrypt_hex:")
    print(f"  原始: {data}")
    print(f"  加密: {hex_enc}")
    print(f"  解密: {hex_dec}")
    print()
    
    # Base64 格式
    b64_enc = rc4_encrypt_b64(data, key)
    b64_dec = rc4_decrypt_b64(b64_enc, key)
    print(f"rc4_encrypt_b64/rc4_decrypt_b64:")
    print(f"  原始: {data}")
    print(f"  加密: {b64_enc}")
    print(f"  解密: {b64_dec}")
    print()


def example_message_encryption():
    """消息加密示例"""
    print("=" * 60)
    print("6. 消息加密示例")
    print("=" * 60)
    
    # 模拟安全消息传递场景
    alice_key = "shared_secret_key"
    bob_key = "shared_secret_key"  # 相同密钥
    
    messages = [
        "Hello Bob!",
        "This is Alice",
        "Let's meet at 5pm",
        "Secret location: Cafe Downtown",
    ]
    
    print("Alice 发送加密消息:")
    for msg in messages:
        encrypted = RC4Cipher.encrypt_string(msg, alice_key)
        print(f"  '{msg}' -> {encrypted[:30]}...")
    
    print("\nBob 接收并解密:")
    for msg in messages:
        encrypted = RC4Cipher.encrypt_string(msg, alice_key)
        decrypted = RC4Cipher.decrypt_string(encrypted, bob_key)
        print(f"  {encrypted[:30]}... -> '{decrypted}'")
    print()


def example_file_encryption_simulation():
    """文件加密模拟示例"""
    print("=" * 60)
    print("7. 文件加密模拟")
    print("=" * 60)
    
    # 模拟文件内容
    file_content = """这是一个模拟的文件内容。
包含多行文本。
可以加密任意二进制数据。

The quick brown fox jumps over the lazy dog.
1234567890
!@#$%^&*()
""".encode('utf-8')
    
    key = b'file_encryption_key'
    
    # 加密
    cipher = RC4Cipher(key)
    encrypted_file = cipher.encrypt(file_content)
    
    # 模拟存储/传输
    print(f"原始文件大小: {len(file_content)} 字节")
    print(f"加密后大小: {len(encrypted_file)} 字节 (相同，因为是流加密)")
    
    # 解密
    cipher2 = RC4Cipher(key)
    decrypted_file = cipher2.decrypt(encrypted_file)
    
    print(f"解密成功: {file_content == decrypted_file}")
    print(f"解密后内容预览:\n{decrypted_file[:100].decode('utf-8')}...")
    print()


def example_known_vector_verification():
    """已知向量验证示例"""
    print("=" * 60)
    print("8. 已知向量验证")
    print("=" * 60)
    
    # Wikipedia 测试向量
    # Key: "Key", Plaintext: "Plaintext"
    # Expected: BBF316E8D940AF0AD3
    key = b'Key'
    plaintext = b'Plaintext'
    
    cipher = RC4Cipher(key)
    encrypted = cipher.encrypt(plaintext)
    
    print("Wikipedia 测试向量:")
    print(f"  密钥: {key.decode()}")
    print(f"  明文: {plaintext.decode()}")
    print(f"  预期密文 (hex): bbf316e8d940af0ad3")
    print(f"  实际密文 (hex): {encrypted.hex()}")
    print(f"  验证: {'✓ 通过' if encrypted.hex() == 'bbf316e8d940af0ad3' else '✗ 失败'}")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("RC4 Cipher Utils - 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_encrypt_decrypt()
    example_string_encryption()
    example_output_formats()
    example_rc4_drop_variants()
    example_convenience_functions()
    example_message_encryption()
    example_file_encryption_simulation()
    example_known_vector_verification()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()