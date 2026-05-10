"""
MurmurHash 工具模块

MurmurHash 是一种非加密型哈希函数，具有高性能和良好的分布特性。
由 Austin Appleby 创建，广泛用于哈希表、布隆过滤器、一致性哈希等场景。

特点：
- 计算速度快，适合大规模数据处理
- 分布均匀，碰撞率低
- 平台无关的一致性输出（x86 和 x64 版本）
- 支持 32 位和 128 位输出

本模块实现：
- MurmurHash3_x86_32: 32位哈希值
- MurmurHash3_x86_128: 128位哈希值
- MurmurHash3_x64_128: 128位哈希值（64位优化版）

注意：MurmurHash 不是加密哈希函数，不适用于安全敏感场景。
"""

from typing import Union, Tuple
import struct


class MurmurHash3:
    """
    MurmurHash3 哈希算法实现
    
    提供多种变体：
    - x86_32: 32位哈希，适用于 32 位系统或小数据集
    - x86_128: 128位哈希，x86 优化版本
    - x64_128: 128位哈希，x64 优化版本，性能最佳
    """
    
    # 常量定义
    C1_32 = 0xcc9e2d51
    C2_32 = 0x1b873593
    
    C1_128_X86 = 0x239b961b
    C2_128_X86 = 0xab0e9789
    C3_128_X86 = 0x38b4ae56
    C4_128_X86 = 0xa1e38b93
    C5_128_X86 = 0x38b4ae56
    
    C1_128_X64 = 0x87c37b91114253d5
    C2_128_X64 = 0x4cf5ad432745937f
    
    @staticmethod
    def _rotl32(x: int, r: int) -> int:
        """32位循环左移"""
        return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF
    
    @staticmethod
    def _rotl64(x: int, r: int) -> int:
        """64位循环左移"""
        return ((x << r) | (x >> (64 - r))) & 0xFFFFFFFFFFFFFFFF
    
    @staticmethod
    def _fmix32(h: int) -> int:
        """32位最终混合函数"""
        h ^= h >> 16
        h = (h * 0x85ebca6b) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0xc2b2ae35) & 0xFFFFFFFF
        h ^= h >> 16
        return h
    
    @staticmethod
    def _fmix64(k: int) -> int:
        """64位最终混合函数"""
        k ^= k >> 33
        k = (k * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
        k ^= k >> 33
        k = (k * 0xc4ceb9fe1a85ec53) & 0xFFFFFFFFFFFFFFFF
        k ^= k >> 33
        return k
    
    @staticmethod
    def _getblock32(data: bytes, i: int) -> int:
        """从字节数据中获取32位块"""
        return struct.unpack('<I', data[i*4:(i+1)*4])[0]
    
    @staticmethod
    def _getblock64(data: bytes, i: int) -> int:
        """从字节数据中获取64位块"""
        return struct.unpack('<Q', data[i*8:(i+1)*8])[0]
    
    @classmethod
    def hash_x86_32(cls, data: Union[str, bytes], seed: int = 0) -> int:
        """
        MurmurHash3 x86 32位版本
        
        适用于：
        - 小数据集快速哈希
        - 32位系统
        - 哈希表索引计算
        
        Args:
            data: 要哈希的数据（字符串或字节）
            seed: 种子值，用于创建不同的哈希函数
            
        Returns:
            32位无符号整数哈希值
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        length = len(data)
        nblocks = length // 4
        
        h1 = seed & 0xFFFFFFFF
        
        # 处理4字节块
        for i in range(nblocks):
            k1 = cls._getblock32(data, i)
            
            k1 = (k1 * cls.C1_32) & 0xFFFFFFFF
            k1 = cls._rotl32(k1, 15)
            k1 = (k1 * cls.C2_32) & 0xFFFFFFFF
            
            h1 ^= k1
            h1 = cls._rotl32(h1, 13)
            h1 = ((h1 * 5) + 0xe6546b64) & 0xFFFFFFFF
        
        # 处理尾部字节
        tail = data[nblocks * 4:]
        k1 = 0
        
        if len(tail) >= 3:
            k1 ^= tail[2] << 16
        if len(tail) >= 2:
            k1 ^= tail[1] << 8
        if len(tail) >= 1:
            k1 ^= tail[0]
            k1 = (k1 * cls.C1_32) & 0xFFFFFFFF
            k1 = cls._rotl32(k1, 15)
            k1 = (k1 * cls.C2_32) & 0xFFFFFFFF
            h1 ^= k1
        
        # 最终处理
        h1 ^= length
        h1 = cls._fmix32(h1)
        
        return h1
    
    @classmethod
    def hash_x86_128(cls, data: Union[str, bytes], seed: int = 0) -> Tuple[int, int, int, int]:
        """
        MurmurHash3 x86 128位版本
        
        返回4个32位无符号整数组成的元组，适合需要更大哈希空间的场景。
        
        Args:
            data: 要哈希的数据（字符串或字节）
            seed: 种子值
            
        Returns:
            4个32位无符号整数的元组 (h1, h2, h3, h4)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        length = len(data)
        nblocks = length // 16
        
        h1 = seed & 0xFFFFFFFF
        h2 = seed & 0xFFFFFFFF
        h3 = seed & 0xFFFFFFFF
        h4 = seed & 0xFFFFFFFF
        
        # 处理16字节块
        for i in range(nblocks):
            k1 = cls._getblock32(data, i*4)
            k2 = cls._getblock32(data, i*4 + 1)
            k3 = cls._getblock32(data, i*4 + 2)
            k4 = cls._getblock32(data, i*4 + 3)
            
            k1 = (k1 * cls.C1_128_X86) & 0xFFFFFFFF
            k1 = cls._rotl32(k1, 15)
            k1 = (k1 * cls.C2_128_X86) & 0xFFFFFFFF
            h1 ^= k1
            
            h1 = cls._rotl32(h1, 19)
            h1 = ((h1 + h2) & 0xFFFFFFFF)
            h1 = ((h1 * 5) + 0x561ccd1b) & 0xFFFFFFFF
            
            k2 = (k2 * cls.C2_128_X86) & 0xFFFFFFFF
            k2 = cls._rotl32(k2, 16)
            k2 = (k2 * cls.C3_128_X86) & 0xFFFFFFFF
            h2 ^= k2
            
            h2 = cls._rotl32(h2, 17)
            h2 = ((h2 + h3) & 0xFFFFFFFF)
            h2 = ((h2 * 5) + 0x0bcaa747) & 0xFFFFFFFF
            
            k3 = (k3 * cls.C3_128_X86) & 0xFFFFFFFF
            k3 = cls._rotl32(k3, 17)
            k3 = (k3 * cls.C4_128_X86) & 0xFFFFFFFF
            h3 ^= k3
            
            h3 = cls._rotl32(h3, 15)
            h3 = ((h3 + h4) & 0xFFFFFFFF)
            h3 = ((h3 * 5) + 0x96cd1c35) & 0xFFFFFFFF
            
            k4 = (k4 * cls.C4_128_X86) & 0xFFFFFFFF
            k4 = cls._rotl32(k4, 18)
            k4 = (k4 * cls.C1_128_X86) & 0xFFFFFFFF
            h4 ^= k4
            
            h4 = cls._rotl32(h4, 13)
            h4 = ((h4 + h1) & 0xFFFFFFFF)
            h4 = ((h4 * 5) + 0x32ac3b17) & 0xFFFFFFFF
        
        # 处理尾部
        tail = data[nblocks * 16:]
        k1 = 0
        k2 = 0
        k3 = 0
        k4 = 0
        
        tail_len = len(tail)
        
        if tail_len >= 15:
            k4 ^= tail[14] << 16
        if tail_len >= 14:
            k4 ^= tail[13] << 8
        if tail_len >= 13:
            k4 ^= tail[12]
            k4 = (k4 * cls.C4_128_X86) & 0xFFFFFFFF
            k4 = cls._rotl32(k4, 18)
            k4 = (k4 * cls.C1_128_X86) & 0xFFFFFFFF
            h4 ^= k4
        
        if tail_len >= 12:
            k3 ^= tail[11] << 16
        if tail_len >= 11:
            k3 ^= tail[10] << 8
        if tail_len >= 10:
            k3 ^= tail[9]
            k3 = (k3 * cls.C3_128_X86) & 0xFFFFFFFF
            k3 = cls._rotl32(k3, 17)
            k3 = (k3 * cls.C4_128_X86) & 0xFFFFFFFF
            h3 ^= k3
        
        if tail_len >= 9:
            k2 ^= tail[8] << 16
        if tail_len >= 8:
            k2 ^= tail[7] << 8
        if tail_len >= 7:
            k2 ^= tail[6]
            k2 = (k2 * cls.C2_128_X86) & 0xFFFFFFFF
            k2 = cls._rotl32(k2, 16)
            k2 = (k2 * cls.C3_128_X86) & 0xFFFFFFFF
            h2 ^= k2
        
        if tail_len >= 6:
            k1 ^= tail[5] << 16
        if tail_len >= 5:
            k1 ^= tail[4] << 8
        if tail_len >= 4:
            k1 ^= tail[3]
            k1 = (k1 * cls.C1_128_X86) & 0xFFFFFFFF
            k1 = cls._rotl32(k1, 15)
            k1 = (k1 * cls.C2_128_X86) & 0xFFFFFFFF
            h1 ^= k1
        
        if tail_len >= 3:
            k1 ^= tail[2] << 16
        if tail_len >= 2:
            k1 ^= tail[1] << 8
        if tail_len >= 1:
            k1 ^= tail[0]
            k1 = (k1 * cls.C1_128_X86) & 0xFFFFFFFF
            k1 = cls._rotl32(k1, 15)
            k1 = (k1 * cls.C2_128_X86) & 0xFFFFFFFF
            h1 ^= k1
        
        # 最终处理
        h1 ^= length
        h2 ^= length
        h3 ^= length
        h4 ^= length
        
        h1 = (h1 + h2 + h3 + h4) & 0xFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFF
        h3 = (h3 + h1) & 0xFFFFFFFF
        h4 = (h4 + h1) & 0xFFFFFFFF
        
        h1 = cls._fmix32(h1)
        h2 = cls._fmix32(h2)
        h3 = cls._fmix32(h3)
        h4 = cls._fmix32(h4)
        
        h1 = (h1 + h2 + h3 + h4) & 0xFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFF
        h3 = (h3 + h1) & 0xFFFFFFFF
        h4 = (h4 + h1) & 0xFFFFFFFF
        
        return (h1, h2, h3, h4)
    
    @classmethod
    def hash_x64_128(cls, data: Union[str, bytes], seed: int = 0) -> Tuple[int, int]:
        """
        MurmurHash3 x64 128位版本（推荐使用）
        
        这是性能最佳的版本，返回2个64位无符号整数。
        适用于：
        - 大规模数据哈希
        - 一致性哈希
        - 布隆过滤器
        - 分布式系统
        
        Args:
            data: 要哈希的数据（字符串或字节）
            seed: 种子值
            
        Returns:
            2个64位无符号整数的元组 (h1, h2)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        length = len(data)
        nblocks = length // 16
        
        h1 = seed & 0xFFFFFFFFFFFFFFFF
        h2 = seed & 0xFFFFFFFFFFFFFFFF
        
        # 处理16字节块
        for i in range(nblocks):
            k1 = cls._getblock64(data, i*2)
            k2 = cls._getblock64(data, i*2 + 1)
            
            k1 = (k1 * cls.C1_128_X64) & 0xFFFFFFFFFFFFFFFF
            k1 = cls._rotl64(k1, 31)
            k1 = (k1 * cls.C2_128_X64) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1
            
            h1 = ((h1 + h2) & 0xFFFFFFFFFFFFFFFF)
            h1 = (h1 * 5 + 0x52dce729) & 0xFFFFFFFFFFFFFFFF
            h1 = cls._rotl64(h1, 27)
            h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
            h1 = (h1 * 5 + 0x38495ab5) & 0xFFFFFFFFFFFFFFFF
            
            k2 = (k2 * cls.C2_128_X64) & 0xFFFFFFFFFFFFFFFF
            k2 = cls._rotl64(k2, 33)
            k2 = (k2 * cls.C1_128_X64) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2
            
            h2 = ((h2 + h1) & 0xFFFFFFFFFFFFFFFF)
            h2 = (h2 * 5 + 0x38495ab5) & 0xFFFFFFFFFFFFFFFF
            h2 = cls._rotl64(h2, 31)
            h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
            h2 = (h2 * 5 + 0x52dce729) & 0xFFFFFFFFFFFFFFFF
        
        # 处理尾部
        tail = data[nblocks * 16:]
        k1 = 0
        k2 = 0
        
        tail_len = len(tail)
        
        if tail_len >= 15:
            k2 ^= tail[14] << 48
        if tail_len >= 14:
            k2 ^= tail[13] << 40
        if tail_len >= 13:
            k2 ^= tail[12] << 32
        if tail_len >= 12:
            k2 ^= tail[11] << 24
        if tail_len >= 11:
            k2 ^= tail[10] << 16
        if tail_len >= 10:
            k2 ^= tail[9] << 8
        if tail_len >= 9:
            k2 ^= tail[8]
            k2 = (k2 * cls.C2_128_X64) & 0xFFFFFFFFFFFFFFFF
            k2 = cls._rotl64(k2, 33)
            k2 = (k2 * cls.C1_128_X64) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2
        
        if tail_len >= 8:
            k1 ^= tail[7] << 56
        if tail_len >= 7:
            k1 ^= tail[6] << 48
        if tail_len >= 6:
            k1 ^= tail[5] << 40
        if tail_len >= 5:
            k1 ^= tail[4] << 32
        if tail_len >= 4:
            k1 ^= tail[3] << 24
        if tail_len >= 3:
            k1 ^= tail[2] << 16
        if tail_len >= 2:
            k1 ^= tail[1] << 8
        if tail_len >= 1:
            k1 ^= tail[0]
            k1 = (k1 * cls.C1_128_X64) & 0xFFFFFFFFFFFFFFFF
            k1 = cls._rotl64(k1, 31)
            k1 = (k1 * cls.C2_128_X64) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1
        
        # 最终处理
        h1 ^= length
        h2 ^= length
        
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
        
        h1 = cls._fmix64(h1)
        h2 = cls._fmix64(h2)
        
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
        
        return (h1, h2)


# 便捷函数
def murmurhash3_x86_32(data: Union[str, bytes], seed: int = 0) -> int:
    """
    MurmurHash3 x86 32位哈希函数
    
    Args:
        data: 要哈希的数据
        seed: 种子值
        
    Returns:
        32位无符号整数哈希值
    """
    return MurmurHash3.hash_x86_32(data, seed)


def murmurhash3_x86_128(data: Union[str, bytes], seed: int = 0) -> Tuple[int, int, int, int]:
    """
    MurmurHash3 x86 128位哈希函数
    
    Args:
        data: 要哈希的数据
        seed: 种子值
        
    Returns:
        4个32位无符号整数的元组
    """
    return MurmurHash3.hash_x86_128(data, seed)


def murmurhash3_x64_128(data: Union[str, bytes], seed: int = 0) -> Tuple[int, int]:
    """
    MurmurHash3 x64 128位哈希函数（推荐）
    
    Args:
        data: 要哈希的数据
        seed: 种子值
        
    Returns:
        2个64位无符号整数的元组
    """
    return MurmurHash3.hash_x64_128(data, seed)


def murmurhash3_hex(data: Union[str, bytes], seed: int = 0, variant: str = 'x64_128') -> str:
    """
    返回十六进制字符串形式的哈希值
    
    Args:
        data: 要哈希的数据
        seed: 种子值
        variant: 变体 ('x86_32', 'x86_128', 'x64_128')
        
    Returns:
        十六进制字符串
    """
    if variant == 'x86_32':
        h = murmurhash3_x86_32(data, seed)
        return f'{h:08x}'
    elif variant == 'x86_128':
        h1, h2, h3, h4 = murmurhash3_x86_128(data, seed)
        return f'{h1:08x}{h2:08x}{h3:08x}{h4:08x}'
    else:  # x64_128
        h1, h2 = murmurhash3_x64_128(data, seed)
        return f'{h1:016x}{h2:016x}'


class ConsistentHash:
    """
    基于 MurmurHash 的一致性哈希实现
    
    适用于分布式系统中的负载均衡和数据分片。
    使用虚拟节点提高分布均匀性。
    """
    
    def __init__(self, nodes: list = None, virtual_nodes: int = 150):
        """
        初始化一致性哈希环
        
        Args:
            nodes: 初始节点列表
            virtual_nodes: 每个物理节点的虚拟节点数量
        """
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # hash -> node
        self.sorted_keys = []  # 排序后的哈希值列表
        self.nodes = set()
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def add_node(self, node: str) -> None:
        """添加节点"""
        if node in self.nodes:
            return
        
        self.nodes.add(node)
        
        for i in range(self.virtual_nodes):
            virtual_key = f'{node}#{i}'
            hash_value = murmurhash3_x86_32(virtual_key)
            self.ring[hash_value] = node
            self.sorted_keys.append(hash_value)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node: str) -> None:
        """移除节点"""
        if node not in self.nodes:
            return
        
        self.nodes.remove(node)
        
        for i in range(self.virtual_nodes):
            virtual_key = f'{node}#{i}'
            hash_value = murmurhash3_x86_32(virtual_key)
            if hash_value in self.ring:
                del self.ring[hash_value]
                self.sorted_keys.remove(hash_value)
    
    def get_node(self, key: str) -> str:
        """
        获取键对应的节点
        
        Args:
            key: 数据键
            
        Returns:
            负责该键的节点
        """
        if not self.ring:
            raise ValueError("哈希环为空")
        
        hash_value = murmurhash3_x86_32(key)
        
        # 二分查找第一个大于等于 hash_value 的位置
        left, right = 0, len(self.sorted_keys)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_keys[mid] < hash_value:
                left = mid + 1
            else:
                right = mid
        
        # 如果超出范围，返回第一个节点（环形）
        if left >= len(self.sorted_keys):
            left = 0
        
        return self.ring[self.sorted_keys[left]]
    
    def get_nodes(self, key: str, count: int = 3) -> list:
        """
        获取键对应的多个节点（用于复制）
        
        Args:
            key: 数据键
            count: 需要的节点数量
            
        Returns:
            节点列表
        """
        if not self.ring:
            raise ValueError("哈希环为空")
        
        if count > len(self.nodes):
            count = len(self.nodes)
        
        hash_value = murmurhash3_x86_32(key)
        
        # 二分查找
        left, right = 0, len(self.sorted_keys)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_keys[mid] < hash_value:
                left = mid + 1
            else:
                right = mid
        
        result = []
        seen = set()
        idx = left
        
        while len(result) < count:
            if idx >= len(self.sorted_keys):
                idx = 0
            
            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                result.append(node)
                seen.add(node)
            
            idx += 1
            
            # 防止无限循环
            if idx == left and len(result) == 0:
                break
        
        return result


class HashBloomFilter:
    """
    基于 MurmurHash 的布隆过滤器
    
    使用 MurmurHash 的多个种子值生成多个哈希函数。
    """
    
    def __init__(self, expected_items: int = 10000, false_positive_rate: float = 0.01):
        """
        初始化布隆过滤器
        
        Args:
            expected_items: 预期元素数量
            false_positive_rate: 假阳性率
        """
        import math
        
        self.size = int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
        self.hash_count = int(self.size / expected_items * math.log(2) + 0.5)
        self.hash_count = max(1, self.hash_count)
        
        self.bit_array = [False] * self.size
        self.item_count = 0
    
    def add(self, item: Union[str, bytes]) -> None:
        """添加元素"""
        if isinstance(item, str):
            item = item.encode('utf-8')
        
        for i in range(self.hash_count):
            hash_value = murmurhash3_x86_32(item, i)
            self.bit_array[hash_value % self.size] = True
        
        self.item_count += 1
    
    def might_contain(self, item: Union[str, bytes]) -> bool:
        """检查元素是否可能存在"""
        if isinstance(item, str):
            item = item.encode('utf-8')
        
        for i in range(self.hash_count):
            hash_value = murmurhash3_x86_32(item, i)
            if not self.bit_array[hash_value % self.size]:
                return False
        
        return True
    
    def __contains__(self, item: Union[str, bytes]) -> bool:
        return self.might_contain(item)
    
    def __len__(self) -> int:
        return self.item_count
    
    def false_positive_probability(self) -> float:
        """估算当前假阳性率"""
        import math
        ratio = sum(self.bit_array) / self.size
        return ratio ** self.hash_count


# 使用示例
if __name__ == '__main__':
    # 基本哈希测试
    print("=== MurmurHash3 基本测试 ===")
    
    test_data = ["hello", "world", "MurmurHash", "一致性哈希", "12345", ""]
    
    for data in test_data:
        h32 = murmurhash3_x86_32(data)
        h128_x86 = murmurhash3_x86_128(data)
        h128_x64 = murmurhash3_x64_128(data)
        hex_str = murmurhash3_hex(data)
        
        print(f"'{data}':")
        print(f"  x86_32:  {h32:010u} (0x{h32:08x})")
        print(f"  x64_128: {hex_str}")
    
    print("\n=== 一致性哈希测试 ===")
    ch = ConsistentHash(['node1', 'node2', 'node3'])
    
    for key in ['user:1001', 'user:1002', 'user:1003', 'data:abc', 'data:xyz']:
        node = ch.get_node(key)
        print(f"'{key}' -> {node}")
    
    print("\n=== 布隆过滤器测试 ===")
    bf = HashBloomFilter(1000, 0.01)
    
    # 添加元素
    for i in range(500):
        bf.add(f'item_{i}')
    
    print(f"添加了 {len(bf)} 个元素")
    print(f"'item_100' 存在: {bf.might_contain('item_100')}")
    print(f"'item_999' 存在: {bf.might_contain('item_999')}")
    print(f"估计假阳性率: {bf.false_positive_probability():.4%}")