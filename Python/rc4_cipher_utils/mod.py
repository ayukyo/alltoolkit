#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - RC4 Cipher Utilities
RC4 流加密工具模块 - 零依赖实现经典的 RC4 流加密算法

@module: rc4_cipher_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- RC4 加密/解密
- RC4 密钥调度算法 (KSA)
- 伪随机生成算法 (PRGA)
- 变体 RC4-drop 支持
- 十六进制/Base64 输出格式

使用示例:
    from rc4_cipher_utils.mod import RC4Cipher
    
    # 加密
    cipher = RC4Cipher(b'my_secret_key')
    encrypted = cipher.encrypt(b'Hello World')
    
    # 解密
    cipher = RC4Cipher(b'my_secret_key')
    decrypted = cipher.decrypt(encrypted)
    
    # 字符串加密
    encrypted = RC4Cipher.encrypt_string('Hello', 'password')
    decrypted = RC4Cipher.decrypt_string(encrypted, 'password')

安全警告:
    RC4 是一个古老的加密算法，存在已知的安全漏洞。
    不推荐用于新的安全敏感应用。
    仅用于教学目的、遗留系统兼容或非安全关键场景。
    对于新的应用，请使用 AES-GCM 或 ChaCha20-Poly1305。
"""

from typing import Union, Optional
import base64


class RC4Error(Exception):
    """RC4 相关错误"""
    pass


class RC4Cipher:
    """
    RC4 流加密器
    
    RC4 (Rivest Cipher 4) 是一种流加密算法，使用可变长度密钥。
    本实现为纯 Python，零外部依赖。
    
    Attributes:
        key: 加密密钥
        drop_bytes: 初始丢弃的字节数（增强安全性）
    
    Example:
        >>> cipher = RC4Cipher(b'secret_key')
        >>> encrypted = cipher.encrypt(b'data')
        >>> decrypted = cipher.decrypt(encrypted)
        >>> assert decrypted == b'data'
    """
    
    def __init__(self, key: Union[bytes, str], drop_bytes: int = 0):
        """
        初始化 RC4 加密器
        
        Args:
            key: 加密密钥（字节或字符串，字符串将使用 UTF-8 编码）
            drop_bytes: 初始丢弃的字节数（RC4-drop 变体，默认 0）
                       推荐值: 256, 768, 3072 用于增强安全性
        
        Raises:
            RC4Error: 密钥无效时
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        if not key or len(key) < 1:
            raise RC4Error("Key cannot be empty")
        
        if len(key) > 256:
            # RC4 密钥最长 256 字节，但通常会截断或使用哈希
            # 这里我们允许但会自动截断
            key = key[:256]
        
        self.key = key
        self.drop_bytes = drop_bytes
        self._S = None  # S-box
        self._i = 0
        self._j = 0
    
    def _ksa(self) -> list:
        """
        Key Scheduling Algorithm (KSA)
        密钥调度算法 - 使用密钥初始化 S-box
        
        Returns:
            初始化后的 S-box
        """
        S = list(range(256))
        j = 0
        key_length = len(self.key)
        
        for i in range(256):
            j = (j + S[i] + self.key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        
        return S
    
    def _prga(self, data: bytes) -> bytes:
        """
        Pseudo-Random Generation Algorithm (PRGA)
        伪随机生成算法 - 生成密钥流并加密/解密数据
        
        Args:
            data: 要处理的数据
        
        Returns:
            加密/解密后的数据
        """
        result = bytearray()
        
        for byte in data:
            self._i = (self._i + 1) % 256
            self._j = (self._j + self._S[self._i]) % 256
            
            # 交换
            self._S[self._i], self._S[self._j] = self._S[self._j], self._S[self._i]
            
            # 生成密钥流字节
            K = self._S[(self._S[self._i] + self._S[self._j]) % 256]
            
            # XOR 操作
            result.append(byte ^ K)
        
        return bytes(result)
    
    def _drop(self, n: int) -> None:
        """
        丢弃初始的 n 个字节（增强安全性）
        
        Args:
            n: 要丢弃的字节数
        """
        dummy = bytes(n)
        self._prga(dummy)
    
    def encrypt(self, plaintext: Union[bytes, str]) -> bytes:
        """
        加密数据
        
        Args:
            plaintext: 明文数据（字节或字符串）
        
        Returns:
            密文字节
        
        Raises:
            RC4Error: 数据无效时
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> encrypted = cipher.encrypt(b'Hello')
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        if plaintext is None:
            raise RC4Error("Plaintext cannot be None")
        
        # 重置状态
        self._S = self._ksa()
        self._i = 0
        self._j = 0
        
        # 如果设置了 drop_bytes，丢弃初始字节
        if self.drop_bytes > 0:
            self._drop(self.drop_bytes)
        
        return self._prga(plaintext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        解密数据
        
        注意: RC4 是对称加密，解密与加密使用相同操作
        
        Args:
            ciphertext: 密文数据
        
        Returns:
            明文字节
        
        Raises:
            RC4Error: 数据无效时
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> encrypted = cipher.encrypt(b'Hello')
            >>> cipher2 = RC4Cipher(b'key')
            >>> decrypted = cipher2.decrypt(encrypted)
            >>> assert decrypted == b'Hello'
        """
        if ciphertext is None:
            raise RC4Error("Ciphertext cannot be None")
        
        if not isinstance(ciphertext, bytes):
            raise RC4Error("Ciphertext must be bytes")
        
        # RC4 是对称的，解密与加密相同
        return self.encrypt(ciphertext)
    
    def encrypt_to_hex(self, plaintext: Union[bytes, str]) -> str:
        """
        加密并返回十六进制字符串
        
        Args:
            plaintext: 明文数据
        
        Returns:
            十六进制密文字符串
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> hex_encrypted = cipher.encrypt_to_hex('Hello')
        """
        encrypted = self.encrypt(plaintext)
        return encrypted.hex()
    
    def decrypt_from_hex(self, hex_ciphertext: str) -> bytes:
        """
        从十六进制字符串解密
        
        Args:
            hex_ciphertext: 十六进制密文字符串
        
        Returns:
            明文字节
        
        Raises:
            RC4Error: 十六进制格式无效时
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> encrypted = cipher.encrypt_to_hex('Hello')
            >>> cipher2 = RC4Cipher(b'key')
            >>> decrypted = cipher2.decrypt_from_hex(encrypted)
        """
        try:
            ciphertext = bytes.fromhex(hex_ciphertext)
        except ValueError as e:
            raise RC4Error(f"Invalid hex string: {e}")
        
        return self.decrypt(ciphertext)
    
    def encrypt_to_base64(self, plaintext: Union[bytes, str]) -> str:
        """
        加密并返回 Base64 字符串
        
        Args:
            plaintext: 明文数据
        
        Returns:
            Base64 编码的密文字符串
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> b64_encrypted = cipher.encrypt_to_base64('Hello')
        """
        encrypted = self.encrypt(plaintext)
        return base64.b64encode(encrypted).decode('ascii')
    
    def decrypt_from_base64(self, b64_ciphertext: str) -> bytes:
        """
        从 Base64 字符串解密
        
        Args:
            b64_ciphertext: Base64 编码的密文字符串
        
        Returns:
            明文字节
        
        Raises:
            RC4Error: Base64 格式无效时
        
        Example:
            >>> cipher = RC4Cipher(b'key')
            >>> encrypted = cipher.encrypt_to_base64('Hello')
            >>> cipher2 = RC4Cipher(b'key')
            >>> decrypted = cipher2.decrypt_from_base64(encrypted)
        """
        try:
            ciphertext = base64.b64decode(b64_ciphertext)
        except Exception as e:
            raise RC4Error(f"Invalid base64 string: {e}")
        
        return self.decrypt(ciphertext)
    
    # ==================== 静态方法 ====================
    
    @staticmethod
    def encrypt_string(plaintext: str, key: Union[bytes, str], 
                       drop_bytes: int = 0, encoding: str = 'utf-8') -> str:
        """
        加密字符串并返回 Base64 密文（静态方法）
        
        Args:
            plaintext: 明文字符串
            key: 密钥
            drop_bytes: 初始丢弃字节数
            encoding: 明文编码方式
        
        Returns:
            Base64 编码的密文字符串
        
        Example:
            >>> encrypted = RC4Cipher.encrypt_string('Hello', 'password')
            >>> decrypted = RC4Cipher.decrypt_string(encrypted, 'password')
        """
        cipher = RC4Cipher(key, drop_bytes)
        return cipher.encrypt_to_base64(plaintext)
    
    @staticmethod
    def decrypt_string(b64_ciphertext: str, key: Union[bytes, str],
                       drop_bytes: int = 0, encoding: str = 'utf-8') -> str:
        """
        从 Base64 密文解密为字符串（静态方法）
        
        Args:
            b64_ciphertext: Base64 编码的密文字符串
            key: 密钥
            drop_bytes: 初始丢弃字节数
            encoding: 输出字符串编码方式
        
        Returns:
            解密后的明文字符串
        
        Raises:
            RC4Error: 解密失败时
        
        Example:
            >>> encrypted = RC4Cipher.encrypt_string('Hello', 'password')
            >>> decrypted = RC4Cipher.decrypt_string(encrypted, 'password')
            >>> assert decrypted == 'Hello'
        """
        cipher = RC4Cipher(key, drop_bytes)
        return cipher.decrypt_from_base64(b64_ciphertext).decode(encoding)
    
    @staticmethod
    def encrypt_bytes(data: bytes, key: Union[bytes, str], 
                      drop_bytes: int = 0) -> bytes:
        """
        加密字节数据（静态方法）
        
        Args:
            data: 明文字节
            key: 密钥
            drop_bytes: 初始丢弃字节数
        
        Returns:
            密文字节
        
        Example:
            >>> encrypted = RC4Cipher.encrypt_bytes(b'data', b'key')
            >>> decrypted = RC4Cipher.decrypt_bytes(encrypted, b'key')
        """
        cipher = RC4Cipher(key, drop_bytes)
        return cipher.encrypt(data)
    
    @staticmethod
    def decrypt_bytes(data: bytes, key: Union[bytes, str],
                      drop_bytes: int = 0) -> bytes:
        """
        解密字节数据（静态方法）
        
        Args:
            data: 密文字节
            key: 密钥
            drop_bytes: 初始丢弃字节数
        
        Returns:
            明文字节
        
        Example:
            >>> encrypted = RC4Cipher.encrypt_bytes(b'data', b'key')
            >>> decrypted = RC4Cipher.decrypt_bytes(encrypted, b'key')
        """
        cipher = RC4Cipher(key, drop_bytes)
        return cipher.decrypt(data)


class RC4Drop(RC4Cipher):
    """
    RC4-drop 变体
    
    预先丢弃初始的一些密钥流字节以增强安全性。
    常见的丢弃值:
    - RC4-drop256: 丢弃 256 字节
    - RC4-drop768: 丢弃 768 字节
    - RC4-drop3072: 丢弃 3072 字节
    
    Example:
        >>> # RC4-drop256
        >>> cipher = RC4Drop256(b'key')
        >>> encrypted = cipher.encrypt(b'data')
    """
    
    def __init__(self, key: Union[bytes, str], drop_bytes: int = 256):
        """
        初始化 RC4-drop 变体
        
        Args:
            key: 加密密钥
            drop_bytes: 要丢弃的字节数（默认 256）
        """
        super().__init__(key, drop_bytes)


class RC4Drop256(RC4Drop):
    """RC4-drop256: 丢弃前 256 字节"""
    
    def __init__(self, key: Union[bytes, str]):
        super().__init__(key, 256)


class RC4Drop768(RC4Drop):
    """RC4-drop768: 丢弃前 768 字节"""
    
    def __init__(self, key: Union[bytes, str]):
        super().__init__(key, 768)


class RC4Drop3072(RC4Drop):
    """RC4-drop3072: 丢弃前 3072 字节"""
    
    def __init__(self, key: Union[bytes, str]):
        super().__init__(key, 3072)


# ==================== 便捷函数 ====================

def rc4_encrypt(plaintext: Union[bytes, str], key: Union[bytes, str]) -> bytes:
    """
    RC4 加密便捷函数
    
    Args:
        plaintext: 明文
        key: 密钥
    
    Returns:
        密文字节
    
    Example:
        >>> encrypted = rc4_encrypt('Hello', 'secret')
    """
    return RC4Cipher.encrypt_bytes(
        plaintext.encode('utf-8') if isinstance(plaintext, str) else plaintext,
        key
    )


def rc4_decrypt(ciphertext: bytes, key: Union[bytes, str]) -> bytes:
    """
    RC4 解密便捷函数
    
    Args:
        ciphertext: 密文
        key: 密钥
    
    Returns:
        明文字节
    
    Example:
        >>> encrypted = rc4_encrypt('Hello', 'secret')
        >>> decrypted = rc4_decrypt(encrypted, 'secret')
    """
    return RC4Cipher.decrypt_bytes(ciphertext, key)


def rc4_encrypt_hex(plaintext: Union[bytes, str], key: Union[bytes, str]) -> str:
    """
    RC4 加密并返回十六进制字符串
    
    Args:
        plaintext: 明文
        key: 密钥
    
    Returns:
        十六进制密文字符串
    
    Example:
        >>> encrypted = rc4_encrypt_hex('Hello', 'secret')
    """
    cipher = RC4Cipher(key)
    return cipher.encrypt_to_hex(plaintext)


def rc4_decrypt_hex(hex_ciphertext: str, key: Union[bytes, str]) -> bytes:
    """
    从十六进制字符串解密
    
    Args:
        hex_ciphertext: 十六进制密文
        key: 密钥
    
    Returns:
        明文字节
    
    Example:
        >>> encrypted = rc4_encrypt_hex('Hello', 'secret')
        >>> decrypted = rc4_decrypt_hex(encrypted, 'secret')
    """
    cipher = RC4Cipher(key)
    return cipher.decrypt_from_hex(hex_ciphertext)


def rc4_encrypt_b64(plaintext: Union[bytes, str], key: Union[bytes, str]) -> str:
    """
    RC4 加密并返回 Base64 字符串
    
    Args:
        plaintext: 明文
        key: 密钥
    
    Returns:
        Base64 密文字符串
    
    Example:
        >>> encrypted = rc4_encrypt_b64('Hello', 'secret')
    """
    cipher = RC4Cipher(key)
    return cipher.encrypt_to_base64(plaintext)


def rc4_decrypt_b64(b64_ciphertext: str, key: Union[bytes, str]) -> bytes:
    """
    从 Base64 字符串解密
    
    Args:
        b64_ciphertext: Base64 密文
        key: 密钥
    
    Returns:
        明文字节
    
    Example:
        >>> encrypted = rc4_encrypt_b64('Hello', 'secret')
        >>> decrypted = rc4_decrypt_b64(encrypted, 'secret')
    """
    cipher = RC4Cipher(key)
    return cipher.decrypt_from_base64(b64_ciphertext)


# 模块级别导出
__all__ = [
    'RC4Cipher',
    'RC4Drop',
    'RC4Drop256',
    'RC4Drop768',
    'RC4Drop3072',
    'RC4Error',
    'rc4_encrypt',
    'rc4_decrypt',
    'rc4_encrypt_hex',
    'rc4_decrypt_hex',
    'rc4_encrypt_b64',
    'rc4_decrypt_b64',
]


if __name__ == '__main__':
    # 简单测试
    print("RC4 Cipher Utils - Simple Test")
    print("=" * 50)
    
    # 基本加密解密
    key = b'my_secret_key'
    plaintext = b'Hello, RC4 Cipher!'
    
    cipher = RC4Cipher(key)
    encrypted = cipher.encrypt(plaintext)
    
    cipher2 = RC4Cipher(key)
    decrypted = cipher2.decrypt(encrypted)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted (hex): {encrypted.hex()}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")
    print()
    
    # 字符串加密
    enc_str = RC4Cipher.encrypt_string('Hello World', 'password')
    dec_str = RC4Cipher.decrypt_string(enc_str, 'password')
    print(f"String encrypted (base64): {enc_str}")
    print(f"String decrypted: {dec_str}")
    print()
    
    # RC4-drop 变体
    drop_cipher = RC4Drop256('another_key')
    enc_drop = drop_cipher.encrypt_to_hex('Sensitive data')
    print(f"RC4-drop256 encrypted: {enc_drop}")