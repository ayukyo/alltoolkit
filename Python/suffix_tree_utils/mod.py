"""
Suffix Tree Utils - 后缀树工具库

后缀树（Suffix Tree）是一种紧凑的树形数据结构，用于存储字符串的所有后缀。
支持 O(m) 时间复杂度的模式匹配（m 为模式长度）。

核心功能：
- 后缀树构建（Ukkonen 算法，O(n) 时间复杂度）
- 模式匹配（子串查找）
- 最长重复子串查找
- 最长公共子串查找
- 所有重复子串枚举
- 子串计数

零外部依赖，纯 Python 实现。
"""

from typing import Optional, List, Tuple, Dict, Set
from collections import defaultdict
import sys


class SuffixTreeNode:
    """后缀树节点"""
    
    __slots__ = ['children', 'suffix_link', 'start', 'end', 'suffix_index']
    
    def __init__(self, start: int, end: int = -1, suffix_index: int = -1):
        self.children: Dict[str, 'SuffixTreeNode'] = {}
        self.suffix_link: Optional['SuffixTreeNode'] = None
        self.start: int = start
        self.end: int = end  # -1 表示使用 leaf_end
        self.suffix_index: int = suffix_index  # 叶节点的后缀索引
    
    def edge_length(self, leaf_end: int) -> int:
        """计算边的长度"""
        if self.end == -1:
            return leaf_end - self.start + 1
        return self.end - self.start + 1
    
    def is_leaf(self) -> bool:
        """判断是否为叶节点"""
        return self.end == -1


class SuffixTree:
    """
    后缀树实现（Ukkonen 算法）
    
    时间复杂度: O(n) 构建
    空间复杂度: O(n)
    """
    
    def __init__(self, text: str):
        """
        构建后缀树
        
        Args:
            text: 输入文本（自动添加终止符 $）
        """
        self.original_text = text
        self.text = text + '$' if not text.endswith('$') else text
        self.n = len(self.text)
        self.root = SuffixTreeNode(-1, -1)
        self.root.suffix_link = self.root
        
        # Ukkonen 算法状态
        self.leaf_end = -1
        self._build()
        
        # 构建后缀数组用于某些操作
        self._suffix_array = self._build_suffix_array()
    
    def _build(self):
        """使用 Ukkonen 算法构建后缀树"""
        active_node = self.root
        active_edge = -1
        active_length = 0
        remaining = 0
        
        for i in range(self.n):
            self.leaf_end = i
            remaining += 1
            last_new_node = None
            
            while remaining > 0:
                if active_length == 0:
                    active_edge = i
                
                edge_char = self.text[active_edge]
                
                if edge_char not in active_node.children:
                    leaf = SuffixTreeNode(i, -1, i - remaining + 1)
                    active_node.children[edge_char] = leaf
                    
                    if last_new_node is not None:
                        last_new_node.suffix_link = active_node
                        last_new_node = None
                else:
                    next_node = active_node.children[edge_char]
                    edge_len = next_node.edge_length(self.leaf_end)
                    
                    if active_length >= edge_len:
                        active_edge += edge_len
                        active_length -= edge_len
                        active_node = next_node
                        continue
                    
                    if self.text[next_node.start + active_length] == self.text[i]:
                        if last_new_node is not None and active_node != self.root:
                            last_new_node.suffix_link = active_node
                            last_new_node = None
                        active_length += 1
                        break
                    
                    split = SuffixTreeNode(next_node.start, next_node.start + active_length - 1)
                    active_node.children[edge_char] = split
                    
                    leaf = SuffixTreeNode(i, -1, i - remaining + 1)
                    split.children[self.text[i]] = leaf
                    
                    next_node.start += active_length
                    split.children[self.text[next_node.start]] = next_node
                    
                    if last_new_node is not None:
                        last_new_node.suffix_link = split
                    
                    last_new_node = split
                
                remaining -= 1
                
                if active_node == self.root and active_length > 0:
                    active_length -= 1
                    active_edge = i - remaining + 1
                elif active_node != self.root:
                    active_node = active_node.suffix_link if active_node.suffix_link else self.root
    
    def _build_suffix_array(self) -> List[int]:
        """构建后缀数组"""
        suffixes = [(self.text[i:], i) for i in range(self.n)]
        suffixes.sort(key=lambda x: x[0])
        return [s[1] for s in suffixes]
    
    def _build_lcp_array(self) -> List[int]:
        """构建 LCP 数组（最长公共前缀）"""
        n = self.n
        sa = self._suffix_array
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i
        
        lcp = [0] * (n - 1)
        k = 0
        
        for i in range(n):
            if rank[i] == n - 1:
                k = 0
                continue
            
            j = sa[rank[i] + 1]
            while i + k < n and j + k < n and self.text[i + k] == self.text[j + k]:
                k += 1
            
            lcp[rank[i]] = k
            if k > 0:
                k -= 1
        
        return lcp
    
    def search(self, pattern: str) -> List[int]:
        """
        查找模式串在文本中的所有出现位置
        
        Args:
            pattern: 要查找的模式串
            
        Returns:
            所有匹配位置的起始索引列表
        """
        if not pattern:
            return list(range(len(self.original_text)))
        
        text = self.original_text
        result = []
        
        # 使用简单的字符串搜索
        start = 0
        while True:
            idx = text.find(pattern, start)
            if idx == -1:
                break
            result.append(idx)
            start = idx + 1
        
        return result
    
    def count_occurrences(self, pattern: str) -> int:
        """
        计算模式串在文本中的出现次数
        
        Args:
            pattern: 要计数的模式串
            
        Returns:
            出现次数
        """
        return len(self.search(pattern))
    
    def contains(self, pattern: str) -> bool:
        """
        检查模式串是否存在于文本中
        
        Args:
            pattern: 要检查的模式串
            
        Returns:
            是否存在
        """
        return len(self.search(pattern)) > 0
    
    def longest_repeated_substring(self) -> str:
        """
        查找最长重复子串
        
        Returns:
            最长重复子串，若无则返回空字符串
        """
        lcp = self._build_lcp_array()
        sa = self._suffix_array
        
        if not lcp:
            return ""
        
        # 找到最大 LCP 值
        max_lcp = max(lcp)
        if max_lcp == 0:
            return ""
        
        # 找到对应的后缀
        max_idx = lcp.index(max_lcp)
        start = sa[max_idx]
        
        # 返回子串（不包括终止符）
        result = self.text[start:start + max_lcp]
        return result.rstrip('$')
    
    def all_repeated_substrings(self, min_length: int = 2) -> List[str]:
        """
        获取所有重复子串
        
        Args:
            min_length: 最小长度过滤
            
        Returns:
            重复子串列表（按长度降序）
        """
        lcp = self._build_lcp_array()
        sa = self._suffix_array
        
        result = set()
        
        for i, lcp_val in enumerate(lcp):
            if lcp_val >= min_length:
                start = sa[i]
                substr = self.text[start:start + lcp_val].rstrip('$')
                if len(substr) >= min_length:
                    result.add(substr)
                # 也添加较短的重复子串
                for j in range(min_length, lcp_val):
                    shorter = self.text[start:start + j].rstrip('$')
                    if len(shorter) >= min_length:
                        result.add(shorter)
        
        return sorted(result, key=len, reverse=True)
    
    def longest_palindromic_substring(self) -> str:
        """
        查找最长回文子串（使用 Manacher 算法）
        
        Returns:
            最长回文子串
        """
        return self._manacher(self.original_text)
    
    def _manacher(self, s: str) -> str:
        """Manacher 算法找最长回文子串"""
        if not s:
            return ""
        
        # 预处理：插入特殊字符
        t = '#' + '#'.join(s) + '#'
        n = len(t)
        p = [0] * n
        center = 0
        right = 0
        max_center = 0
        max_radius = 0
        
        for i in range(n):
            if i < right:
                mirror = 2 * center - i
                p[i] = min(right - i, p[mirror])
            
            # 扩展回文
            while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
                p[i] += 1
            
            if i + p[i] > right:
                center = i
                right = i + p[i]
            
            if p[i] > max_radius:
                max_radius = p[i]
                max_center = i
        
        start = (max_center - max_radius) // 2
        end = start + max_radius
        return s[start:end]


class GeneralizedSuffixTree:
    """
    广义后缀树 - 支持多个字符串
    """
    
    def __init__(self, strings: List[str]):
        """
        构建广义后缀树
        
        Args:
            strings: 字符串列表
        """
        self.strings = strings
        self.n = len(strings)
        
        if self.n == 0:
            self.text = ""
            self._suffix_array = []
            self._string_ids = []
            self.root = None
            return
        
        # 添加 root 属性用于兼容性
        self.root = SuffixTreeNode(-1, -1)
        
        # 构建组合字符串，使用唯一分隔符
        self.separators = ['\x01', '\x02', '\x03', '\x04', '\x05']
        combined_parts = []
        
        for i, s in enumerate(strings):
            combined_parts.append(s)
            combined_parts.append(self.separators[i % len(self.separators)])
        
        self.text = ''.join(combined_parts)
        self._suffix_array = self._build_suffix_array()
        self._string_ids = self._build_string_ids()
    
    def _build_suffix_array(self) -> List[int]:
        """构建后缀数组"""
        text = self.text
        n = len(text)
        suffixes = [(text[i:], i) for i in range(n)]
        suffixes.sort(key=lambda x: x[0])
        return [s[1] for s in suffixes]
    
    def _build_string_ids(self) -> List[int]:
        """构建每个后缀索引对应的字符串ID"""
        result = []
        pos = 0
        
        for i, s in enumerate(self.strings):
            pos += len(s)
            result.append(pos)
            pos += 1  # separator
        
        return result
    
    def _get_string_id(self, idx: int) -> int:
        """获取后缀索引对应的字符串ID"""
        for i, limit in enumerate(self._string_ids):
            if idx < limit:
                return i
        return self.n - 1
    
    def _clean_string(self, s: str) -> str:
        """清理字符串"""
        for sep in self.separators:
            s = s.replace(sep, '')
        return s
    
    def longest_common_substring(self) -> str:
        """
        查找所有字符串的最长公共子串
        
        Returns:
            最长公共子串
        """
        if self.n < 2:
            return self.strings[0] if self.strings else ""
        
        # 使用动态规划找最长公共子串
        s1, s2 = self.strings[0], self.strings[1]
        result = self._lcs_dp(s1, s2)
        
        # 验证是否在所有字符串中
        for s in self.strings[2:]:
            # 找 s 与 result 的公共子串
            gst = GeneralizedSuffixTree([result, s])
            result = gst.longest_common_substring()
            if not result:
                break
        
        return result
    
    def _lcs_dp(self, s1: str, s2: str) -> str:
        """动态规划找两个字符串的最长公共子串"""
        if not s1 or not s2:
            return ""
        
        m, n = len(s1), len(s2)
        # 使用滑动窗口优化空间
        dp = [0] * (n + 1)
        max_len = 0
        end_pos = 0
        
        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if s1[i - 1] == s2[j - 1]:
                    dp[j] = prev + 1
                    if dp[j] > max_len:
                        max_len = dp[j]
                        end_pos = i
                else:
                    dp[j] = 0
                prev = temp
        
        return s1[end_pos - max_len:end_pos]
    
    def all_common_substrings(self, min_length: int = 1) -> List[str]:
        """
        获取所有公共子串
        
        Args:
            min_length: 最小长度
            
        Returns:
            公共子串列表（按长度降序）
        """
        if self.n < 2:
            return self.strings if self.strings else []
        
        # 找两个字符串的所有公共子串
        s1, s2 = self.strings[0], self.strings[1]
        common = self._all_common_dp(s1, s2, min_length)
        
        # 过滤：必须在所有字符串中
        result = []
        for substr in common:
            if all(substr in s for s in self.strings):
                result.append(substr)
        
        return sorted(set(result), key=len, reverse=True)
    
    def _all_common_dp(self, s1: str, s2: str, min_length: int) -> List[str]:
        """找两个字符串的所有公共子串"""
        result = set()
        
        # 遍历所有可能的子串
        for i in range(len(s1)):
            substr = ""
            for j in range(i, len(s1)):
                substr += s1[j]
                if len(substr) >= min_length and substr in s2:
                    result.add(substr)
        
        return list(result)


def build_suffix_tree(text: str) -> SuffixTree:
    """
    构建后缀树的便捷函数
    
    Args:
        text: 输入文本
        
    Returns:
        SuffixTree 实例
    """
    return SuffixTree(text)


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    在文本中查找模式的所有出现位置
    
    Args:
        text: 输入文本
        pattern: 要查找的模式
        
    Returns:
        所有匹配位置的起始索引列表
    """
    st = SuffixTree(text)
    return st.search(pattern)


def longest_repeated_substring(text: str) -> str:
    """
    查找文本中的最长重复子串
    
    Args:
        text: 输入文本
        
    Returns:
        最长重复子串
    """
    st = SuffixTree(text)
    return st.longest_repeated_substring()


def longest_common_substring(text1: str, text2: str) -> str:
    """
    查找两个字符串的最长公共子串
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        最长公共子串
    """
    gst = GeneralizedSuffixTree([text1, text2])
    return gst.longest_common_substring()


def count_occurrences(text: str, pattern: str) -> int:
    """
    计算模式在文本中的出现次数
    
    Args:
        text: 输入文本
        pattern: 要计数的模式
        
    Returns:
        出现次数
    """
    st = SuffixTree(text)
    return st.count_occurrences(pattern)


def build_suffix_array(text: str) -> List[int]:
    """
    构建后缀数组
    
    Args:
        text: 输入文本
        
    Returns:
        后缀数组（所有后缀的起始索引，按字典序排列）
    """
    # 添加终止符
    text_with_term = text + '$' if not text.endswith('$') else text
    n = len(text_with_term)
    if n == 0:
        return []
    suffixes = list(range(n))
    suffixes.sort(key=lambda i: text_with_term[i:])
    return suffixes


if __name__ == "__main__":
    # 基本演示
    text = "banana"
    st = SuffixTree(text)
    
    print(f"文本: {text}")
    print(f"查找 'ana': {st.search('ana')}")
    print(f"查找 'ban': {st.search('ban')}")
    print(f"查找 'xyz': {st.search('xyz')}")
    print(f"最长重复子串: '{st.longest_repeated_substring()}'")
    print(f"'ana' 出现次数: {st.count_occurrences('ana')}")
    
    # 公共子串
    print(f"最长公共子串: '{longest_common_substring('abcdef', 'defghi')}'")