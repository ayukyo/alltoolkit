#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Crypto Utilities
加密工具模块 - 提供哈希、编码、加密等常用功能

@module: crypto_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- 哈希算法: MD5, SHA1, SHA256, SHA512, SHA3_256, SHA3_512, BLAKE2b
- HMAC: HMAC-SHA256, HMAC-SHA512
- 编码: Base64, Base32, Base16, URL-safe Base64
- 加密: XOR 对称加密
- 随机数: 安全随机字符串、密码、UUID
- 验证: 哈希格式验证、Base64验证

使用示例:
    from crypto_utils.mod import CryptoUtils
    
    # 计算哈希
    hash_value = CryptoUtils.sha256_hash("hello world")
    
    # Base64 编解码
    encoded = CryptoUtils.base64_encode("你好世界")
    decoded = CryptoUtils.base64_decode(encoded)
    
    # 生成随机密码
    password = CryptoUtils.random_password(16)
"""

import hashlib
import hmac
import base64
import secrets
import string
import uuid
import re
from typing import Optional, Union


class CryptoUtils:
    """加密工具类 - 提供静态方法进行哈希、编码和加密操作"""
    
    # 字符集常量
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    ALPHANUMERIC = LOWERCASE + UPPERCASE + DIGITS
    ALL_CHARS = ALPHANUMERIC + SPECIAL_CHARS
    
    # ==================== 哈希函数 ====================
    
    @staticmethod
    def md5_hash(data: Union[str, bytes]) -> str:
        """
        计算 MD5 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            32位小写十六进制哈希字符串
            
        Example:
            >>> CryptoUtils.md5_hash("hello")
            '5d41402abc4b2a76b9719d911017c592'
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def sha1_hash(data: Union[str, bytes]) -> str:
        """
        计算 SHA1 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            40位小写十六进制哈希字符串
            
        Example:
            >>> CryptoUtils.sha1_hash("hello")
            'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha1(data).hexdigest()
    
    @staticmethod
    def sha256_hash(data: Union[str, bytes]) -> str:
        """
        计算 SHA256 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            64位小写十六进制哈希字符串
            
        Example:
            >>> CryptoUtils.sha256_hash("hello")
            '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def sha512_hash(data: Union[str, bytes]) -> str:
        """
        计算 SHA512 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            128位小写十六进制哈希字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha512(data).hexdigest()
    
    @staticmethod
    def sha3_256_hash(data: Union[str, bytes]) -> str:
        """
        计算 SHA3-256 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            64位小写十六进制哈希字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha3_256(data).hexdigest()
    
    @staticmethod
    def sha3_512_hash(data: Union[str, bytes]) -> str:
        """
        计算 SHA3-512 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            128位小写十六进制哈希字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha3_512(data).hexdigest()
    
    @staticmethod
    def blake2b_hash(data: Union[str, bytes], digest_size: int = 32) -> str:
        """
        计算 BLAKE2b 哈希值
        
        Args:
            data: 输入数据，字符串或字节
            digest_size: 输出长度（字节），默认32（64位十六进制）
            
        Returns:
            十六进制哈希字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.blake2b(data, digest_size=digest_size).hexdigest()
    
    # ==================== HMAC 函数 ====================
    
    @staticmethod
    def hmac_sha256(key: Union[str, bytes], message: Union[str, bytes]) -> str:
        """
        计算 HMAC-SHA256
        
        Args:
            key: 密钥，字符串或字节
            message: 消息，字符串或字节
            
        Returns:
            64位小写十六进制 HMAC 字符串
            
        Example:
            >>> CryptoUtils.hmac_sha256("secret_key", "hello world")
            '...'
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha256).hexdigest()
    
    @staticmethod
    def hmac_sha512(key: Union[str, bytes], message: Union[str, bytes]) -> str:
        """
        计算 HMAC-SHA512
        
        Args:
            key: 密钥，字符串或字节
            message: 消息，字符串或字节
            
        Returns:
            128位小写十六进制 HMAC 字符串
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha512).hexdigest()
    
    # ==================== Base64 编码 ====================
    
    @staticmethod
    def base64_encode(data: Union[str, bytes]) -> str:
        """
        Base64 编码
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            Base64 编码字符串
            
        Example:
            >>> CryptoUtils.base64_encode("hello")
            'aGVsbG8='
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def base64_decode(data: str) -> bytes:
        """
        Base64 解码
        
        Args:
            data: Base64 编码字符串
            
        Returns:
            解码后的字节数据
            
        Raises:
            ValueError: 如果输入不是有效的 Base64
        """
        return base64.b64decode(data)
    
    @staticmethod
    def base64_decode_string(data: str) -> str:
        """
        Base64 解码并返回字符串
        
        Args:
            data: Base64 编码字符串
            
        Returns:
            解码后的 UTF-8 字符串
        """
        return base64.b64decode(data).decode('utf-8')
    
    @staticmethod
    def base64_url_encode(data: Union[str, bytes]) -> str:
        """
        URL 安全的 Base64 编码（RFC 4648）
        
        将 + 替换为 -，/ 替换为 _，并移除填充 =
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            URL 安全的 Base64 字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')
    
    @staticmethod
    def base64_url_decode(data: str) -> bytes:
        """
        URL 安全的 Base64 解码
        
        Args:
            data: URL 安全的 Base64 字符串
            
        Returns:
            解码后的字节数据
        """
        # 添加填充
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        return base64.urlsafe_b64decode(data)
    
    @staticmethod
    def base32_encode(data: Union[str, bytes]) -> str:
        """
        Base32 编码
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            Base32 编码字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b32encode(data).decode('utf-8')
    
    @staticmethod
    def base32_decode(data: str) -> bytes:
        """
        Base32 解码
        
        Args:
            data: Base32 编码字符串
            
        Returns:
            解码后的字节数据
        """
        return base64.b32decode(data)
    
    @staticmethod
    def base16_encode(data: Union[str, bytes]) -> str:
        """
        Base16 (Hex) 编码
        
        Args:
            data: 输入数据，字符串或字节
            
        Returns:
            十六进制编码字符串
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b16encode(data).decode('utf-8')
    
    @staticmethod
    def base16_decode(data: str) -> bytes:
        """
        Base16 (Hex) 解码
        
        Args:
            data: 十六进制编码字符串
            
        Returns:
            解码后的字节数据
        """
        return base64.b16decode(data.upper())
    
    # ==================== XOR 加密 ====================
    
    @staticmethod
    def xor_encrypt(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """
        XOR 对称加密
        
        使用密钥对数据进行异或加密，返回 Base64 编码结果
        
        Args:
            data: 要加密的数据，字符串或字节
            key: 加密密钥，字符串或字节
            
        Returns:
            Base64 编码的加密结果
            
        Example:
            >>> encrypted = CryptoUtils.xor_encrypt("hello", "key")
            >>> decrypted = CryptoUtils.xor_decrypt(encrypted, "key")
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        # XOR 加密
        encrypted = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        return base64.b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def xor_decrypt(encrypted_data: str, key: Union[str, bytes]) -> str:
        """
        XOR 对称解密
        
        使用密钥解密 XOR 加密的数据
        
        Args:
            encrypted_data: Base64 编码的加密数据
            key: 解密密钥，字符串或字节
            
        Returns:
            解密后的字符串
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        encrypted = base64.b64decode(encrypted_data)
        decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
        return decrypted.decode('utf-8')
    
    # ==================== 随机数生成 ====================
    
    @staticmethod
    def random_string(length: int = 16, chars: Optional[str] = None) -> str:
        """
        生成安全随机字符串
        
        使用 secrets 模块生成加密安全的随机字符串
        
        Args:
            length: 字符串长度，默认16
            chars: 使用的字符集，默认使用字母数字
            
        Returns:
            随机字符串
            
        Example:
            >>> CryptoUtils.random_string(8)
            'a3K9mP2n'
        """
        if chars is None:
            chars = CryptoUtils.ALPHANUMERIC
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_password(length: int = 16) -> str:
        """
        生成安全随机密码
        
        密码包含大小写字母、数字和特殊字符
        
        Args:
            length: 密码长度，默认16
            
        Returns:
            随机密码字符串
            
        Example:
            >>> CryptoUtils.random_password(12)
            'aB3$kL9@mP2#'
        """
        if length < 4:
            length = 4
        
        # 确保每种类型的字符至少有一个
        password = [
            secrets.choice(CryptoUtils.LOWERCASE),
            secrets.choice(CryptoUtils.UPPERCASE),
            secrets.choice(CryptoUtils.DIGITS),
            secrets.choice(CryptoUtils.SPECIAL_CHARS)
        ]
        
        # 填充剩余长度
        password.extend(secrets.choice(CryptoUtils.ALL_CHARS) for _ in range(length - 4))
        
        # 打乱顺序
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def random_hex(length: int = 32) -> str:
        """
        生成随机十六进制字符串
        
        Args:
            length: 十六进制字符数，默认32（16字节）
            
        Returns:
            随机十六进制字符串
        """
        return secrets.token_hex(length // 2)
    
    @staticmethod
    def random_bytes(length: int = 32) -> bytes:
        """
        生成随机字节
        
        Args:
            length: 字节数，默认32
            
        Returns:
            随机字节数据
        """
        return secrets.token_bytes(length)
    
    @staticmethod
    def random_urlsafe(length: int = 32) -> str:
        """
        生成 URL 安全的随机字符串
        
        Args:
            length: 字符串长度，默认32
            
        Returns:
            URL 安全的随机字符串
        """
        return secrets.token_urlsafe(length)
    
    # ==================== UUID 生成 ====================
    
    @staticmethod
    def uuid_v4() -> str:
        """
        生成 UUID v4（随机 UUID）
        
        Returns:
            标准格式的 UUID 字符串，如 '550e8400-e29b-41d4-a716-446655440000'
        """
        return str(uuid.uuid4())
    
    @staticmethod
    def uuid_v4_compact() -> str:
        """
        生成紧凑格式的 UUID v4（无连字符）
        
        Returns:
            32位 UUID 字符串，如 '550e8400e29b41d4a716446655440000'
        """
        return uuid.uuid4().hex
    
    @staticmethod
    def uuid_v1() -> str:
        """
        生成 UUID v1（基于时间和 MAC 地址）
        
        Returns:
            标准格式的 UUID 字符串
        """
        return str(uuid.uuid1())
    
    # ==================== 验证函数 ====================
    
    @staticmethod
    def is_valid_md5(hash_str: str) -> bool:
        """
        验证字符串是否为有效的 MD5 格式
        
        Args:
            hash_str: 要验证的字符串
            
        Returns:
            是否为有效的 MD5 格式
        """
        return bool(re.match(r'^[a-fA-F0-9]{32}$', hash_str))
    
    @staticmethod
    def is_valid_sha1(hash_str: str) -> bool:
        """
        验证字符串是否为有效的 SHA1 格式
        
        Args:
            hash_str: 要验证的字符串
            
        Returns:
            是否为有效的 SHA1 格式
        """
        return bool(re.match(r'^[a-fA-F0-9]{40}$', hash_str))
    
    @staticmethod
    def is_valid_sha256(hash_str: str) -> bool:
        """
        验证字符串是否为有效的 SHA256 格式
        
        Args:
            hash_str: 要验证的字符串
            
        Returns:
            是否为有效的 SHA256 格式
        """
        return bool(re.match(r'^[a-fA-F0-9]{64}$', hash_str))
    
    @staticmethod
    def is_valid_sha512(hash_str: str) -> bool:
        """
        验证字符串是否为有效的 SHA512 格式
        
        Args:
            hash_str: 要验证的字符串
            
        Returns:
            是否为有效的 SHA512 格式
        """
        return bool(re.match(r'^[a-fA-F0-9]{128}$', hash_str))
    
    @staticmethod
    def is_valid_base64(data: str) -> bool:
        """
        验证字符串是否为有效的 Base64
        
        Args:
            data: 要验证的字符串
            
        Returns:
            是否为有效的 Base64
        """
        pattern = r'^[A-Za-z0-9+/]*={0,2}$'
        if not re.match(pattern, data):
            return False
        try:
            base64.b64decode(data)
            return True
        except Exception:
            return False
    
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """
        验证字符串是否为有效的 UUID
        
        Args:
            uuid_str: 要验证的字符串
            
        Returns:
            是否为有效的 UUID
        """
        pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return bool(re.match(pattern, uuid_str))
    
    @staticmethod
    def is_valid_uuid_compact(uuid_str: str) -> bool:
        """
        验证字符串是否为有效的紧凑格式 UUID
        
        Args:
            uuid_str: 要验证的字符串
            
        Returns:
            是否为有效的紧凑格式 UUID
        """
        return bool(re.match(r'^[0-9a-fA-F]{32}$', uuid_str))


# 便捷函数（模块级别直接调用）
def md5_hash(data: Union[str, bytes]) -> str:
    """计算 MD5 哈希值"""
    return CryptoUtils.md5_hash(data)

def sha256_hash(data: Union[str, bytes]) -> str:
    """计算 SHA256 哈希值"""
    return CryptoUtils.sha256_hash(data)

def sha512_hash(data: Union[str, bytes]) -> str:
    """计算 SHA512 哈希值"""
    return CryptoUtils.sha512_hash(data)

def base64_encode(data: Union[str, bytes]) -> str:
    """Base64 编码"""
    return CryptoUtils.base64_encode(data)

def base64_decode(data: str) -> bytes:
    """Base64 解码"""
    return CryptoUtils.base64_decode(data)

def random_string(length: int = 16, chars: Optional[str] = None) -> str:
    """生成安全随机字符串"""
    return CryptoUtils.random_string(length, chars)

def random_password(length: int = 16) -> str:
    """生成安全随机密码"""
    return CryptoUtils.random_password(length)

def uuid_v4() -> str:
    """生成 UUID v4"""
    return CryptoUtils.uuid_v4()


if __name__ == "__main__":
    # 简单测试
    print("=== AllToolkit Python Crypto Utils ===")
    print(f"MD5: {CryptoUtils.md5_hash('hello')}")
    print(f"SHA256: {CryptoUtils.sha256_hash('hello')}")
    print(f"Base64: {CryptoUtils.base64_encode('hello')}")
    print(f"Random: {CryptoUtils.random_string(8)}")
    print(f"Password: {CryptoUtils.random_password(12)}")
    print(f"UUID: {CryptoUtils.uuid_v4()}")
