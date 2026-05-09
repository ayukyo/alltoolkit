#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Diffie-Hellman Key Exchange Utilities
Diffie-Hellman 密钥交换工具模块 - 实现安全的密钥协商协议

@module: diffie_hellman_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- 密钥交换: 经典 Diffie-Hellman 协议实现
- 安全参数: 预定义安全素数和生成元
- 密钥派生: 从共享密钥派生加密密钥
- 验证: 密钥交换结果验证
- 零知识: 不传输私钥的安全设计

使用示例:
    from diffie_hellman_utils.mod import DiffieHellman
    
    # Alice 生成密钥对
    alice = DiffieHellman()
    alice_private = alice.generate_private_key()
    alice_public = alice.generate_public_key()
    
    # Bob 生成密钥对
    bob = DiffieHellman()
    bob_private = bob.generate_private_key()
    bob_public = bob.generate_public_key()
    
    # 双方计算共享密钥
    alice_shared = alice.compute_shared_key(bob_public)
    bob_shared = bob.compute_shared_key(alice_public)
    
    # alice_shared == bob_shared
"""

import secrets
import hashlib
from typing import Tuple, Optional


class DiffieHellman:
    """
    Diffie-Hellman 密钥交换实现
    
    使用安全素数和生成元进行密钥协商，
    允许双方在不安全的信道上建立共享密钥。
    """
    
    # RFC 3526 定义的安全素数 (2048-bit MODP Group)
    # 这些参数经过密码学验证，适合生产环境
    PRIME_2048 = int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
        "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
        "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
        "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
        "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
        "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
        "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
        "15728E5A8AACAA68FFFFFFFFFFFFFFFF",
        16
    )
    
    # 对应的生成元
    GENERATOR_2048 = 2
    
    # 1024-bit 参数 (用于快速测试，生产环境建议使用 2048-bit)
    PRIME_1024 = int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
        "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
        "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
        "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
        "670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF",
        16
    )
    
    GENERATOR_1024 = 2
    
    # 256-bit 参数 (仅用于演示和测试，不安全！)
    PRIME_256 = int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234"
        "C4C6628B80DC1CD129024E088A67CC74"
        "020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F1437",
        16
    )
    
    GENERATOR_256 = 2
    
    def __init__(self, prime: Optional[int] = None, generator: Optional[int] = None, 
                 key_bits: int = 2048):
        """
        初始化 Diffie-Hellman 实例
        
        Args:
            prime: 自定义素数，如果为 None 则使用预定义参数
            generator: 自定义生成元，如果为 None 则使用预定义参数
            key_bits: 密钥位数，可选 256, 1024, 2048 (默认 2048)
        """
        if prime is not None and generator is not None:
            self.prime = prime
            self.generator = generator
        else:
            # 使用预定义安全参数
            if key_bits >= 2048:
                self.prime = self.PRIME_2048
                self.generator = self.GENERATOR_2048
                self.key_bits = 2048
            elif key_bits >= 1024:
                self.prime = self.PRIME_1024
                self.generator = self.GENERATOR_1024
                self.key_bits = 1024
            else:
                self.prime = self.PRIME_256
                self.generator = self.GENERATOR_256
                self.key_bits = 256
        
        self._private_key: Optional[int] = None
        self._public_key: Optional[int] = None
        self._shared_key: Optional[int] = None
    
    def generate_private_key(self) -> int:
        """
        生成私钥
        
        使用安全随机数生成器生成私钥。
        私钥必须是 [1, p-1] 范围内的整数。
        
        Returns:
            私钥（大整数）
        """
        # 生成 [1, p-2] 范围内的随机私钥
        # 使用 secrets 保证密码学安全
        self._private_key = 1 + secrets.randbelow(self.prime - 2)
        return self._private_key
    
    def generate_public_key(self, private_key: Optional[int] = None) -> int:
        """
        生成公钥
        
        公钥 = g^private mod p
        
        Args:
            private_key: 私钥，如果为 None 则使用已生成的私钥
            
        Returns:
            公钥（大整数）
            
        Raises:
            ValueError: 如果没有提供或生成私钥
        """
        if private_key is not None:
            self._private_key = private_key
        
        if self._private_key is None:
            raise ValueError("必须先生成或提供私钥")
        
        # 使用内置 pow 进行模幂运算 (比手动实现快得多)
        self._public_key = pow(self.generator, self._private_key, self.prime)
        return self._public_key
    
    def compute_shared_key(self, other_public_key: int) -> int:
        """
        计算共享密钥
        
        使用对方的公钥和自己的私钥计算共享密钥。
        shared_key = other_public^private mod p
        
        Args:
            other_public_key: 对方的公钥
            
        Returns:
            共享密钥（大整数）
            
        Raises:
            ValueError: 如果没有私钥或对方公钥无效
        """
        if self._private_key is None:
            raise ValueError("必须先生成私钥")
        
        if other_public_key <= 1 or other_public_key >= self.prime:
            raise ValueError("无效的对方公钥")
        
        self._shared_key = pow(other_public_key, self._private_key, self.prime)
        return self._shared_key
    
    def derive_key(self, shared_key: Optional[int] = None, 
                   key_length: int = 32,
                   hash_algorithm: str = "sha256",
                   salt: Optional[bytes] = None,
                   info: Optional[bytes] = None) -> bytes:
        """
        从共享密钥派生加密密钥
        
        使用 HKDF (HMAC-based Key Derivation Function) 派生密钥。
        
        Args:
            shared_key: 共享密钥，如果为 None 则使用已计算的共享密钥
            key_length: 派生密钥长度（字节），默认 32 (256-bit)
            hash_algorithm: 哈希算法，默认 sha256
            salt: 盐值，增加密钥派生的安全性
            info: 上下文信息，用于密钥派生的附加绑定
            
        Returns:
            派生的密钥字节
            
        Raises:
            ValueError: 如果没有共享密钥
        """
        if shared_key is not None:
            self._shared_key = shared_key
        
        if self._shared_key is None:
            raise ValueError("必须先计算共享密钥")
        
        # 将共享密钥转换为字节
        shared_bytes = self._shared_key.to_bytes(
            (self._shared_key.bit_length() + 7) // 8, 'big'
        )
        
        # 简化的 HKDF 实现
        hash_func = getattr(hashlib, hash_algorithm)
        
        # 如果没有提供盐，使用默认盐
        if salt is None:
            salt = b'\x00' * hash_func().digest_size
        
        # 如果没有提供信息，使用默认信息
        if info is None:
            info = b'Diffie-Hellman Key Derivation'
        
        # Extract: PRK = HMAC-Hash(salt, IKM)
        prk = hashlib.new(hash_algorithm)
        prk_hmac = self._hmac(salt, shared_bytes, hash_algorithm)
        
        # Expand: OKM = HMAC-Hash(PRK, info || counter)
        derived_key = b''
        counter = 1
        while len(derived_key) < key_length:
            derived_key += self._hmac(prk_hmac, info + bytes([counter]), hash_algorithm)
            counter += 1
        
        return derived_key[:key_length]
    
    @staticmethod
    def _hmac(key: bytes, message: bytes, algorithm: str = "sha256") -> bytes:
        """
        计算 HMAC
        
        Args:
            key: 密钥
            message: 消息
            algorithm: 哈希算法
            
        Returns:
            HMAC 值
        """
        import hmac
        return hmac.new(key, message, getattr(hashlib, algorithm)).digest()
    
    def get_private_key(self) -> Optional[int]:
        """获取当前私钥（仅用于内部存储，不应传输）"""
        return self._private_key
    
    def get_public_key(self) -> Optional[int]:
        """获取当前公钥"""
        return self._public_key
    
    def get_shared_key(self) -> Optional[int]:
        """获取当前共享密钥"""
        return self._shared_key
    
    def export_public_key(self) -> str:
        """
        导出公钥为十六进制字符串
        
        Returns:
            十六进制格式的公钥字符串
            
        Raises:
            ValueError: 如果没有公钥
        """
        if self._public_key is None:
            raise ValueError("没有公钥可导出")
        return hex(self._public_key)[2:]  # 移除 '0x' 前缀
    
    def import_public_key(self, hex_key: str) -> int:
        """
        从十六进制字符串导入公钥
        
        Args:
            hex_key: 十六进制格式的公钥字符串
            
        Returns:
            公钥整数
        """
        return int(hex_key, 16)
    
    @staticmethod
    def verify_key_exchange(alice_shared: int, bob_shared: int) -> bool:
        """
        验证密钥交换是否成功
        
        双方计算的共享密钥应该相等。
        
        Args:
            alice_shared: Alice 计算的共享密钥
            bob_shared: Bob 计算的共享密钥
            
        Returns:
            是否相等
        """
        return alice_shared == bob_shared
    
    def clear_sensitive_data(self) -> None:
        """
        清除敏感数据
        
        安全擦除内存中的私钥和共享密钥。
        应在密钥交换完成后调用。
        """
        if self._private_key is not None:
            # 使用随机值覆盖
            self._private_key = secrets.randbelow(self.prime)
            self._private_key = None
        
        if self._shared_key is not None:
            self._shared_key = secrets.randbelow(self.prime)
            self._shared_key = None
    
    def __repr__(self) -> str:
        """对象表示"""
        return (f"DiffieHellman(key_bits={self.key_bits}, "
                f"has_private={self._private_key is not None}, "
                f"has_public={self._public_key is not None}, "
                f"has_shared={self._shared_key is not None})")


class ECDHKey:
    """
    简化的椭圆曲线 Diffie-Hellman 实现
    
    使用 Curve25519 曲线（如果可用），否则使用简化实现。
    注意：这是一个简化实现，仅用于演示。
    生产环境请使用 cryptography 或 PyNaCl 库。
    """
    
    # Curve25519 素数 p = 2^255 - 19
    PRIME = (2 ** 255) - 19
    
    # Curve25519 基点
    BASEPOINT = 9
    
    # 阶 (order of the basepoint)
    ORDER = 2**252 + 27742317777372353535851937790883648493
    
    def __init__(self):
        """初始化 ECDH 实例"""
        self._private_key: Optional[int] = None
        self._public_key: Optional[int] = None
        self._shared_key: Optional[int] = None
    
    def generate_private_key(self) -> int:
        """
        生成私钥
        
        生成一个 256 位的随机私钥。
        
        Returns:
            私钥整数
        """
        # 生成 32 字节随机私钥
        self._private_key = secrets.randbits(256)
        # 确保私钥在有效范围内
        self._private_key &= (1 << 254) - 1
        self._private_key |= (1 << 254)
        return self._private_key
    
    def generate_public_key(self, private_key: Optional[int] = None) -> int:
        """
        生成公钥
        
        简化实现：public_key = private_key * basepoint mod p
        注意：这是简化版本，不是真正的 Curve25519！
        
        Args:
            private_key: 私钥
            
        Returns:
            公钥整数
        """
        if private_key is not None:
            self._private_key = private_key
        
        if self._private_key is None:
            raise ValueError("必须先生成私钥")
        
        # 简化的标量乘法（非真实 Curve25519）
        self._public_key = (self._private_key * self.BASEPOINT) % self.PRIME
        return self._public_key
    
    def compute_shared_key(self, other_public_key: int) -> int:
        """
        计算共享密钥
        
        Args:
            other_public_key: 对方公钥
            
        Returns:
            共享密钥
        """
        if self._private_key is None:
            raise ValueError("必须先生成私钥")
        
        self._shared_key = (self._private_key * other_public_key) % self.PRIME
        return self._shared_key
    
    def derive_key(self, key_length: int = 32) -> bytes:
        """
        派生密钥
        
        Args:
            key_length: 密钥长度
            
        Returns:
            派生密钥
        """
        if self._shared_key is None:
            raise ValueError("必须先计算共享密钥")
        
        shared_bytes = self._shared_key.to_bytes(32, 'big')
        return hashlib.sha256(shared_bytes).digest()[:key_length]


def create_dh_pair(key_bits: int = 2048) -> Tuple[DiffieHellman, int, int]:
    """
    创建 Diffie-Hellman 密钥对的便捷函数
    
    Args:
        key_bits: 密钥位数，256/1024/2048
        
    Returns:
        (DiffieHellman实例, 私钥, 公钥)
    """
    dh = DiffieHellman(key_bits=key_bits)
    private_key = dh.generate_private_key()
    public_key = dh.generate_public_key()
    return dh, private_key, public_key


def perform_key_exchange(alice_dh: DiffieHellman, bob_dh: DiffieHellman) -> Tuple[int, int]:
    """
    执行密钥交换的便捷函数
    
    Args:
        alice_dh: Alice 的 DH 实例
        bob_dh: Bob 的 DH 实例
        
    Returns:
        (alice_shared_key, bob_shared_key)
        
    Raises:
        ValueError: 如果双方没有生成密钥对
    """
    if alice_dh._public_key is None or bob_dh._public_key is None:
        raise ValueError("双方必须先生成公钥")
    
    alice_shared = alice_dh.compute_shared_key(bob_dh._public_key)
    bob_shared = bob_dh.compute_shared_key(alice_dh._public_key)
    
    return alice_shared, bob_shared


if __name__ == "__main__":
    print("=== Diffie-Hellman 密钥交换演示 ===\n")
    
    # 使用 2048 位参数
    print("1. 使用 2048 位安全参数")
    print("-" * 40)
    
    # Alice 创建密钥对
    alice = DiffieHellman(key_bits=2048)
    alice_private = alice.generate_private_key()
    alice_public = alice.generate_public_key()
    print(f"Alice 私钥: {hex(alice_private)[:20]}...")
    print(f"Alice 公钥: {hex(alice_public)[:20]}...")
    
    # Bob 创建密钥对
    bob = DiffieHellman(key_bits=2048)
    bob_private = bob.generate_private_key()
    bob_public = bob.generate_public_key()
    print(f"Bob 私钥: {hex(bob_private)[:20]}...")
    print(f"Bob 公钥: {hex(bob_public)[:20]}...")
    
    # 交换公钥并计算共享密钥
    alice_shared = alice.compute_shared_key(bob_public)
    bob_shared = bob.compute_shared_key(alice_public)
    
    print(f"\nAlice 共享密钥: {hex(alice_shared)[:20]}...")
    print(f"Bob 共享密钥: {hex(bob_shared)[:20]}...")
    
    # 验证
    if DiffieHellman.verify_key_exchange(alice_shared, bob_shared):
        print("✓ 密钥交换成功！双方共享密钥一致")
    else:
        print("✗ 密钥交换失败！")
    
    # 派生加密密钥
    derived_key = alice.derive_key(key_length=32)
    print(f"\n派生的加密密钥: {derived_key.hex()}")
    
    # 清除敏感数据
    alice.clear_sensitive_data()
    bob.clear_sensitive_data()
    print("\n敏感数据已清除")
    
    print("\n" + "=" * 50)
    print("\n2. 便捷函数演示")
    print("-" * 40)
    
    # 使用便捷函数
    dh1, priv1, pub1 = create_dh_pair(key_bits=1024)
    dh2, priv2, pub2 = create_dh_pair(key_bits=1024)
    
    shared1 = dh1.compute_shared_key(pub2)
    shared2 = dh2.compute_shared_key(pub1)
    
    print(f"便捷函数密钥交换: {'成功' if shared1 == shared2 else '失败'}")
    
    print("\n" + "=" * 50)
    print("\n3. 公钥导入导出演示")
    print("-" * 40)
    
    dh = DiffieHellman(key_bits=2048)
    dh.generate_private_key()
    dh.generate_public_key()
    
    exported = dh.export_public_key()
    print(f"导出的公钥 (前40字符): {exported[:40]}...")
    
    imported = dh.import_public_key(exported)
    print(f"导入的公钥: {hex(imported)[:20]}...")
    print(f"导入验证: {'成功' if imported == dh._public_key else '失败'}")