"""
Rolling Hash Utils - 滚动哈希工具模块

提供高效的滚动哈希实现，支持字符串匹配、重复检测、文件指纹等场景。
零外部依赖，纯 Python 标准库实现。

主要功能：
- RollingHash: 基础滚动哈希类
- RabinKarp: Rabin-Karp 字符串匹配算法
- MultiRollingHash: 多模式匹配
- 文件指纹比较
- 重复内容检测
"""

from typing import List, Tuple, Optional, Set, Dict, Any, Iterator
from collections import defaultdict
import hashlib


class RollingHash:
    """
    滚动哈希类 - 高效计算滑动窗口哈希值
    
    使用多项式滚动哈希：
    hash = (c0 * base^(k-1) + c1 * base^(k-2) + ... + c(k-1)) % mod
    
    特点：
    - O(1) 时间添加/移除字符
    - 支持任意窗口大小
    - 可配置基数和模数
    """
    
    # 常用的大质数模数
    DEFAULT_MOD = 2**61 - 1  # 梅森质数，减少溢出风险
    DEFAULT_BASE = 256  # 字节值范围
    
    def __init__(
        self,
        window_size: int,
        base: int = DEFAULT_BASE,
        mod: int = DEFAULT_MOD
    ):
        """
        初始化滚动哈希
        
        Args:
            window_size: 滑动窗口大小
            base: 哈希基数
            mod: 模数
        """
        if window_size <= 0:
            raise ValueError("窗口大小必须大于 0")
        
        self.window_size = window_size
        self.base = base
        self.mod = mod
        self.hash = 0
        self.window: List[int] = []
        # 预计算 base^(window_size-1) % mod
        self.base_pow = pow(base, window_size - 1, mod)
    
    def _char_value(self, char: str) -> int:
        """获取字符的数值"""
        return ord(char)
    
    def append(self, char: str) -> int:
        """
        添加字符到窗口，返回新的哈希值
        
        如果窗口已满，自动移除最旧的字符
        
        Args:
            char: 要添加的字符
            
        Returns:
            当前窗口的哈希值
        """
        value = self._char_value(char)
        
        if len(self.window) == self.window_size:
            # 移除最旧的字符
            old_value = self.window.pop(0)
            self.hash = (self.hash - old_value * self.base_pow) % self.mod
        
        self.window.append(value)
        self.hash = (self.hash * self.base + value) % self.mod
        
        return self.hash
    
    def extend(self, text: str) -> int:
        """
        扩展多个字符，返回最终哈希值
        
        Args:
            text: 要添加的文本
            
        Returns:
            当前窗口的哈希值
        """
        for char in text:
            self.append(char)
        return self.hash
    
    def reset(self) -> None:
        """重置哈希状态"""
        self.hash = 0
        self.window.clear()
    
    def get_hash(self) -> int:
        """获取当前哈希值"""
        return self.hash
    
    def is_full(self) -> bool:
        """检查窗口是否已满"""
        return len(self.window) == self.window_size
    
    def get_window(self) -> str:
        """获取当前窗口内容"""
        return ''.join(chr(v) for v in self.window)
    
    def __str__(self) -> str:
        return f"RollingHash(window_size={self.window_size}, hash={self.hash}, window='{self.get_window()}')"


class DoubleRollingHash:
    """
    双重滚动哈希 - 使用两个不同的哈希函数减少碰撞
    
    返回元组 (hash1, hash2)，碰撞概率极低
    """
    
    # 两套不同的参数
    PARAMS = [
        (256, 2**61 - 1),      # 梅森质数
        (257, 10**9 + 7),      # 常用大质数
    ]
    
    def __init__(self, window_size: int):
        """
        初始化双重滚动哈希
        
        Args:
            window_size: 滑动窗口大小
        """
        self.rh1 = RollingHash(window_size, *self.PARAMS[0])
        self.rh2 = RollingHash(window_size, *self.PARAMS[1])
    
    def append(self, char: str) -> Tuple[int, int]:
        """
        添加字符，返回双重哈希值元组
        
        Returns:
            (hash1, hash2) 元组
        """
        h1 = self.rh1.append(char)
        h2 = self.rh2.append(char)
        return (h1, h2)
    
    def extend(self, text: str) -> Tuple[int, int]:
        """扩展多个字符"""
        for char in text:
            self.append(char)
        return self.get_hash()
    
    def get_hash(self) -> Tuple[int, int]:
        """获取当前双重哈希值"""
        return (self.rh1.get_hash(), self.rh2.get_hash())
    
    def reset(self) -> None:
        """重置哈希状态"""
        self.rh1.reset()
        self.rh2.reset()
    
    def is_full(self) -> bool:
        """检查窗口是否已满"""
        return self.rh1.is_full()
    
    def get_window(self) -> str:
        """获取当前窗口内容"""
        return self.rh1.get_window()


class RabinKarp:
    """
    Rabin-Karp 字符串匹配算法
    
    使用滚动哈希进行高效模式匹配：
    - 平均时间复杂度: O(n + m)
    - 最坏时间复杂度: O(nm)（哈希碰撞时）
    """
    
    def __init__(self, pattern: str):
        """
        初始化 Rabin-Karp 匹配器
        
        Args:
            pattern: 要匹配的模式字符串
        """
        if not pattern:
            raise ValueError("模式字符串不能为空")
        
        self.pattern = pattern
        self.pattern_length = len(pattern)
        # 使用双重哈希减少碰撞
        self.rh = DoubleRollingHash(self.pattern_length)
        self.pattern_hash = self._compute_pattern_hash()
    
    def _compute_pattern_hash(self) -> Tuple[int, int]:
        """计算模式字符串的哈希值"""
        self.rh.reset()
        return self.rh.extend(self.pattern)
    
    def find_all(self, text: str) -> List[int]:
        """
        查找所有匹配位置
        
        Args:
            text: 要搜索的文本
            
        Returns:
            匹配起始位置列表
        """
        if len(text) < self.pattern_length:
            return []
        
        matches = []
        self.rh.reset()
        
        # 初始化窗口
        for i in range(self.pattern_length):
            self.rh.append(text[i])
        
        # 滑动窗口
        for i in range(len(text) - self.pattern_length + 1):
            if self.rh.get_hash() == self.pattern_hash:
                # 哈希匹配，验证实际内容
                if text[i:i + self.pattern_length] == self.pattern:
                    matches.append(i)
            
            # 滑动窗口
            if i + self.pattern_length < len(text):
                self.rh.append(text[i + self.pattern_length])
        
        return matches
    
    def find_first(self, text: str) -> Optional[int]:
        """
        查找第一个匹配位置
        
        Args:
            text: 要搜索的文本
            
        Returns:
            第一个匹配位置，未找到返回 None
        """
        matches = self.find_all(text)
        return matches[0] if matches else None
    
    def count(self, text: str) -> int:
        """
        统计匹配次数
        
        Args:
            text: 要搜索的文本
            
        Returns:
            匹配次数
        """
        return len(self.find_all(text))
    
    def contains(self, text: str) -> bool:
        """
        检查是否包含模式
        
        Args:
            text: 要搜索的文本
            
        Returns:
            是否包含
        """
        return self.find_first(text) is not None


class MultiPatternMatcher:
    """
    多模式匹配器 - 同时匹配多个模式
    
    使用多个独立的 Rabin-Karp 匹配器
    """
    
    def __init__(self, patterns: List[str]):
        """
        初始化多模式匹配器
        
        Args:
            patterns: 模式字符串列表
        """
        if not patterns:
            raise ValueError("模式列表不能为空")
        
        # 按长度分组
        self.patterns_by_length: Dict[int, Dict[str, Tuple[int, int]]] = defaultdict(dict)
        self.matchers_by_length: Dict[int, Dict[str, RabinKarp]] = defaultdict(dict)
        
        for pattern in patterns:
            if not pattern:
                raise ValueError("模式字符串不能为空")
            length = len(pattern)
            self.matchers_by_length[length][pattern] = RabinKarp(pattern)
    
    def find_all(self, text: str) -> Dict[str, List[int]]:
        """
        查找所有模式的所有匹配位置
        
        Args:
            text: 要搜索的文本
            
        Returns:
            {pattern: [positions]} 字典
        """
        results: Dict[str, List[int]] = {}
        
        for length, matchers in self.matchers_by_length.items():
            for pattern, matcher in matchers.items():
                positions = matcher.find_all(text)
                if positions:
                    results[pattern] = positions
        
        return results
    
    def find_any(self, text: str) -> Optional[Tuple[str, int]]:
        """
        查找任意一个匹配
        
        Args:
            text: 要搜索的文本
            
        Returns:
            (pattern, position) 或 None
        """
        for length, matchers in self.matchers_by_length.items():
            for pattern, matcher in matchers.items():
                pos = matcher.find_first(text)
                if pos is not None:
                    return (pattern, pos)
        return None
    
    def count_all(self, text: str) -> Dict[str, int]:
        """
        统计所有模式的匹配次数
        
        Args:
            text: 要搜索的文本
            
        Returns:
            {pattern: count} 字典
        """
        results = self.find_all(text)
        return {pattern: len(positions) for pattern, positions in results.items()}


class RollingHashIterator:
    """
    滚动哈希迭代器 - 生成所有窗口的哈希值
    
    适用于需要遍历所有子串哈希的场景
    """
    
    def __init__(self, text: str, window_size: int, double_hash: bool = True):
        """
        初始化迭代器
        
        Args:
            text: 要处理的文本
            window_size: 窗口大小
            double_hash: 是否使用双重哈希
        """
        self.text = text
        self.window_size = window_size
        self.double_hash = double_hash
        
        if double_hash:
            self.rh = DoubleRollingHash(window_size)
        else:
            self.rh = RollingHash(window_size)
        
        self.index = 0
    
    def __iter__(self) -> Iterator[Tuple[int, Any, str]]:
        """
        迭代所有窗口
        
        Yields:
            (index, hash, window) 元组
        """
        if len(self.text) < self.window_size:
            return
        
        self.rh.reset()
        
        # 初始化窗口
        for i in range(self.window_size):
            self.rh.append(self.text[i])
        
        # 迭代
        for i in range(len(self.text) - self.window_size + 1):
            window = self.text[i:i + self.window_size]
            yield (i, self.rh.get_hash(), window)
            
            # 滑动
            if i + self.window_size < len(self.text):
                self.rh.append(self.text[i + self.window_size])


class DuplicateDetector:
    """
    重复内容检测器
    
    使用滚动哈希高效检测重复内容
    """
    
    def __init__(
        self,
        min_length: int = 10,
        double_hash: bool = True
    ):
        """
        初始化检测器
        
        Args:
            min_length: 最小重复长度
            double_hash: 是否使用双重哈希
        """
        if min_length <= 0:
            raise ValueError("最小重复长度必须大于 0")
        
        self.min_length = min_length
        self.double_hash = double_hash
    
    def find_duplicates(self, text: str) -> Dict[str, List[int]]:
        """
        查找所有重复内容
        
        Args:
            text: 要检测的文本
            
        Returns:
            {content: [positions]} 字典
        """
        if len(text) < self.min_length:
            return {}
        
        hash_map: Dict[Any, List[Tuple[int, str]]] = defaultdict(list)
        
        # 收集所有窗口哈希
        iterator = RollingHashIterator(text, self.min_length, self.double_hash)
        for idx, hash_val, window in iterator:
            hash_map[hash_val].append((idx, window))
        
        # 找出重复项（验证碰撞）
        duplicates: Dict[str, List[int]] = {}
        
        for hash_val, positions in hash_map.items():
            if len(positions) > 1:
                # 验证内容相同
                first_content = positions[0][1]
                same_content = [positions[0][0]]
                
                for pos, content in positions[1:]:
                    if content == first_content:
                        same_content.append(pos)
                
                if len(same_content) > 1:
                    duplicates[first_content] = sorted(same_content)
        
        return duplicates
    
    def has_duplicates(self, text: str) -> bool:
        """
        检查是否有重复内容
        
        Args:
            text: 要检测的文本
            
        Returns:
            是否有重复
        """
        duplicates = self.find_duplicates(text)
        return len(duplicates) > 0
    
    def count_unique_substrings(self, text: str) -> int:
        """
        统计不同子串数量
        
        Args:
            text: 要分析的文本
            
        Returns:
            不同子串数量
        """
        if len(text) < self.min_length:
            return 0
        
        seen: Set[Any] = set()
        iterator = RollingHashIterator(text, self.min_length, self.double_hash)
        
        for _, hash_val, _ in iterator:
            seen.add(hash_val)
        
        return len(seen)


class FileFingerprint:
    """
    文件指纹生成器
    
    使用滚动哈希生成文件指纹，用于快速比较文件相似性
    """
    
    def __init__(self, chunk_size: int = 4096):
        """
        初始化指纹生成器
        
        Args:
            chunk_size: 分块大小（字节）
        """
        self.chunk_size = chunk_size
    
    def fingerprint_bytes(self, data: bytes) -> List[int]:
        """
        计算字节数据的指纹
        
        Args:
            data: 字节数据
            
        Returns:
            指纹列表
        """
        if len(data) < self.chunk_size:
            return [hash(data)]
        
        fingerprints = []
        rh = RollingHash(self.chunk_size)
        
        # 计算每个窗口的哈希
        for i in range(len(data)):
            rh.append(chr(data[i]))
            if rh.is_full():
                fingerprints.append(rh.get_hash())
        
        return fingerprints
    
    def fingerprint_string(self, text: str) -> List[int]:
        """
        计算字符串的指纹
        
        Args:
            text: 文本字符串
            
        Returns:
            指纹列表
        """
        if len(text) < self.chunk_size:
            return [hash(text)]
        
        fingerprints = []
        rh = RollingHash(self.chunk_size)
        
        for char in text:
            rh.append(char)
            if rh.is_full():
                fingerprints.append(rh.get_hash())
        
        return fingerprints
    
    def similarity(self, fp1: List[int], fp2: List[int]) -> float:
        """
        计算两个指纹的相似度
        
        Args:
            fp1: 第一个指纹
            fp2: 第二个指纹
            
        Returns:
            相似度 (0-1)
        """
        if not fp1 or not fp2:
            return 0.0
        
        set1 = set(fp1)
        set2 = set(fp2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def jaccard_distance(self, fp1: List[int], fp2: List[int]) -> float:
        """
        计算 Jaccard 距离
        
        Args:
            fp1: 第一个指纹
            fp2: 第二个指纹
            
        Returns:
            Jaccard 距离 (0-1)
        """
        return 1.0 - self.similarity(fp1, fp2)


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    快速查找所有出现位置（便捷函数）
    
    Args:
        text: 要搜索的文本
        pattern: 模式字符串
        
    Returns:
        所有匹配位置列表
    """
    return RabinKarp(pattern).find_all(text)


def find_first_occurrence(text: str, pattern: str) -> Optional[int]:
    """
    快速查找第一个出现位置（便捷函数）
    
    Args:
        text: 要搜索的文本
        pattern: 模式字符串
        
    Returns:
        第一个匹配位置，未找到返回 None
    """
    return RabinKarp(pattern).find_first(text)


def compute_rolling_hash(text: str, window_size: int) -> List[Tuple[int, str]]:
    """
    计算所有窗口的滚动哈希（便捷函数）
    
    Args:
        text: 文本
        window_size: 窗口大小
        
    Returns:
        [(position, window)] 列表
    """
    results = []
    iterator = RollingHashIterator(text, window_size, double_hash=False)
    
    for pos, hash_val, window in iterator:
        results.append((hash_val, window))
    
    return results


def longest_repeated_substring(text: str, min_length: int = 2) -> Optional[str]:
    """
    查找最长重复子串
    
    Args:
        text: 文本
        min_length: 最小长度
        
    Returns:
        最长重复子串，不存在返回 None
    """
    if len(text) < min_length * 2:
        return None
    
    longest = None
    
    # 从长到短搜索
    for length in range(len(text) // 2, min_length - 1, -1):
        seen: Dict[Any, Tuple[int, str]] = {}
        iterator = RollingHashIterator(text, length)
        
        for pos, hash_val, window in iterator:
            if hash_val in seen:
                old_pos, old_window = seen[hash_val]
                if old_window == window:  # 验证碰撞
                    return window
            else:
                seen[hash_val] = (pos, window)
    
    return longest


# 导出公共接口
__all__ = [
    'RollingHash',
    'DoubleRollingHash',
    'RabinKarp',
    'MultiPatternMatcher',
    'RollingHashIterator',
    'DuplicateDetector',
    'FileFingerprint',
    'find_all_occurrences',
    'find_first_occurrence',
    'compute_rolling_hash',
    'longest_repeated_substring',
]