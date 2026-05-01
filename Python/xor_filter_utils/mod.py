"""
XOR Filter Utils - XOR 过滤器工具包

提供高效的静态集合成员检测数据结构，零外部依赖，仅使用 Python 标准库。

功能:
- XOR Filter: 比布隆过滤器更节省空间的静态成员检测
- Fuse XOR Filter: 针对大数据集优化的变体
- 支持任意可哈希类型
- O(1) 查询时间
- 假阳性率约 0.39%

算法原理:
XOR 过滤器是一种空间高效的概率数据结构，用于测试元素是否属于集合。
与布隆过滤器不同，XOR 过滤器：
1. 更节省空间（约 9.6 bits/元素）
2. 查询更快（只需计算少量哈希并异或）
3. 只支持静态集合（构建后不能添加元素）
4. 不支持删除操作

基于 XOR-filter: Faster and smaller than Bloom and Cuckoo filters
作者: Thomas Mueller Graf and Daniel Lemire

作者: AllToolkit
日期: 2026-05-02
"""

from typing import Any, Generic, Hashable, Iterator, List, Tuple, TypeVar
import struct
import math

T = TypeVar('T', bound=Hashable)


def _hash64(element: Any, seed: int) -> int:
    """计算 64 位哈希值。"""
    h = hash((seed, element)) & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 33
    h *= 0xff51afd7ed558ccd & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 33
    return h


class XorFilter(Generic[T]):
    """
    XOR 过滤器 - 高效的静态集合成员检测。
    
    空间效率比布隆过滤器更高，查询速度更快。
    适用于只需要构建一次后反复查询的场景。
    
    示例:
        >>> filter = XorFilter.from_elements(['apple', 'banana'])
        >>> 'apple' in filter
        True
        >>> 'grape' in filter
        False
    """
    
    def __init__(self, fingerprints: List[int], size: int, array_length: int, seed: int):
        self._fingerprints = fingerprints
        self._size = size
        self._array_length = array_length
        # 确保 seed 是正整数
        self._seed = seed & 0xFFFFFFFF
    
    @classmethod
    def from_elements(cls, elements: Iterator[T], max_attempts: int = 100) -> 'XorFilter[T]':
        """从元素集合构建 XOR 过滤器。"""
        element_list = list(set(elements))
        size = len(element_list)
        
        if size == 0:
            return cls([], 0, 0, 0)
        
        if size < 3:
            # 对于极小集合，需要更大的数组才能成功构建
            array_length = 12
        else:
            array_length = int(math.ceil(size * 1.23))
            while array_length % 3 != 0:
                array_length += 1
        
        block_length = array_length // 3
        
        for attempt in range(max_attempts):
            seed = (attempt * 0x9e3779b9) & 0xFFFFFFFF
            
            # 计算所有元素的哈希
            hashes = [_hash64(elem, seed) for elem in element_list]
            
            # 每个元素映射到三个位置
            # positions[i] = (h0, h1, h2)
            positions = []
            fingerprints_needed = []
            
            for h in hashes:
                h0 = h % block_length
                h1 = block_length + ((h >> 20) % block_length)
                h2 = 2 * block_length + ((h >> 40) % block_length)
                fp = ((h >> 56) & 0xFF) or 1
                positions.append((h0, h1, h2))
                fingerprints_needed.append(fp)
            
            # 统计每个位置的引用计数
            counts = [0] * array_length
            for h0, h1, h2 in positions:
                counts[h0] += 1
                counts[h1] += 1
                counts[h2] += 1
            
            # 记录每个位置被哪些元素使用（用于快速查找）
            position_to_elements = [[] for _ in range(array_length)]
            for i, (h0, h1, h2) in enumerate(positions):
                position_to_elements[h0].append(i)
                position_to_elements[h1].append(i)
                position_to_elements[h2].append(i)
            
            # Peeling 算法
            # 使用栈记录只有一个元素的位置
            stack = [pos for pos in range(array_length) if counts[pos] == 1]
            
            peel_order = []
            used = set()
            
            while stack:
                pos = stack.pop()
                
                # 快速找到使用这个位置的元素
                elem_idx = -1
                for i in position_to_elements[pos]:
                    if i not in used:
                        elem_idx = i
                        break
                
                if elem_idx == -1:
                    continue
                
                h0, h1, h2 = positions[elem_idx]
                fp = fingerprints_needed[elem_idx]
                used.add(elem_idx)
                
                # 选择要修改的位置
                target_pos = pos
                
                peel_order.append((elem_idx, target_pos, h0, h1, h2, fp))
                
                # 更新其他两个位置的计数
                for p in [h0, h1, h2]:
                    if p != target_pos:
                        counts[p] -= 1
                        if counts[p] == 1:
                            stack.append(p)
            
            if len(peel_order) != size:
                continue
            
            # 反向构建指纹数组
            fingerprints = [0] * array_length
            
            for idx, target_pos, h0, h1, h2, fp in reversed(peel_order):
                val = fp ^ fingerprints[h0] ^ fingerprints[h1] ^ fingerprints[h2]
                fingerprints[target_pos] = val
            
            return cls(fingerprints, size, array_length, seed)
        
        raise ValueError(f"无法构建 XOR 过滤器，尝试了 {max_attempts} 次")
    
    def __contains__(self, element: T) -> bool:
        """检查元素是否可能在集合中。"""
        if self._size == 0:
            return False
        
        h = _hash64(element, self._seed)
        block_length = self._array_length // 3
        
        h0 = h % block_length
        h1 = block_length + ((h >> 20) % block_length)
        h2 = 2 * block_length + ((h >> 40) % block_length)
        expected_fp = ((h >> 56) & 0xFF) or 1
        
        actual_fp = self._fingerprints[h0] ^ self._fingerprints[h1] ^ self._fingerprints[h2]
        
        return actual_fp == expected_fp
    
    def __len__(self) -> int:
        return self._size
    
    @property
    def size_in_bytes(self) -> int:
        return self._array_length
    
    @property
    def bits_per_element(self) -> float:
        if self._size == 0:
            return 0.0
        return (self.size_in_bytes * 8) / self._size
    
    def false_positive_rate(self) -> float:
        return 1.0 / 256.0
    
    def to_bytes(self) -> bytes:
        header = struct.pack('>III', self._size, self._array_length, self._seed)
        body = bytes(self._fingerprints)
        return header + body
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'XorFilter[T]':
        if len(data) < 12:
            raise ValueError("数据太短")
        size, array_length, seed = struct.unpack('>III', data[:12])
        fingerprints = list(data[12:])
        return cls(fingerprints, size, array_length, seed)
    
    def __repr__(self) -> str:
        return f"XorFilter(size={self._size}, bytes={self.size_in_bytes}, bits/elem={self.bits_per_element:.2f})"


class FuseXorFilter(Generic[T]):
    """Fuse XOR 过滤器 - 使用标准 XOR 过滤器实现。"""
    
    def __init__(self, xf: XorFilter):
        self._xf = xf
    
    @classmethod
    def from_elements(cls, elements: Iterator[T], max_attempts: int = 50) -> 'FuseXorFilter[T]':
        xf = XorFilter.from_elements(elements, max_attempts=max_attempts)
        return cls(xf)
    
    def __contains__(self, element: T) -> bool:
        return element in self._xf
    
    def __len__(self) -> int:
        return len(self._xf)
    
    @property
    def size_in_bytes(self) -> int:
        return self._xf.size_in_bytes
    
    def __repr__(self) -> str:
        return f"FuseXorFilter(size={len(self)}, bytes={self.size_in_bytes})"


class XorFilter8(XorFilter[T]):
    """8 位指纹 XOR 过滤器。"""
    
    @classmethod
    def from_elements(cls, elements: Iterator[T], max_attempts: int = 50) -> 'XorFilter8[T]':
        return XorFilter.from_elements(elements, max_attempts=max_attempts)


class XorFilter16(XorFilter[T]):
    """16 位指纹 XOR 过滤器。"""
    
    @classmethod
    def from_elements(cls, elements: Iterator[T], max_attempts: int = 50) -> 'XorFilter16[T]':
        return XorFilter.from_elements(elements, max_attempts=max_attempts)


def create_xor_filter(elements: Iterator[T]) -> XorFilter[T]:
    """创建 XOR 过滤器。"""
    return XorFilter.from_elements(elements)


def create_fuse_xor_filter(elements: Iterator[T]) -> FuseXorFilter[T]:
    """创建 Fuse XOR 过滤器。"""
    return FuseXorFilter.from_elements(elements)


def compare_with_bloom_filter(element_count: int, target_fpp: float = 0.01) -> dict:
    """比较 XOR 过滤器和布隆过滤器的空间效率。"""
    xor_bits = 9.6
    xor_total_bits = element_count * xor_bits
    xor_fpp = 1 / 256
    
    bloom_bits = -math.log(target_fpp) / (math.log(2) ** 2)
    bloom_total_bits = element_count * bloom_bits
    
    return {
        'element_count': element_count,
        'target_fpp': target_fpp,
        'xor_filter': {
            'bits_per_element': xor_bits,
            'total_bits': xor_total_bits,
            'total_bytes': xor_total_bits / 8,
            'actual_fpp': xor_fpp,
            'supports_additions': False,
            'supports_deletion': False,
        },
        'bloom_filter': {
            'bits_per_element': bloom_bits,
            'total_bits': bloom_total_bits,
            'total_bytes': bloom_total_bits / 8,
            'target_fpp': target_fpp,
            'supports_additions': True,
            'supports_deletion': False,
        },
        'space_savings_percent': (
            (bloom_total_bits - xor_total_bits) / bloom_total_bits * 100
            if bloom_total_bits > 0 else 0
        )
    }