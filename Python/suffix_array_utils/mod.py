"""
Suffix Array Utils - 后缀数组工具模块

后缀数组是一种高效的字符串处理数据结构，用于解决多种字符串问题：
- 模式匹配（查找子串出现位置）
- 最长重复子串
- 最长公共子串
- 字符串排序和排名
- 统计不同子串数量

特点：
- 构建时间 O(n log n) 或 O(n log² n)
- 查询时间 O(m log n)，m为模式串长度
- 空间复杂度 O(n)

零外部依赖，纯Python实现。
"""

from typing import List, Tuple, Optional, Set


class SuffixArray:
    """
    后缀数组实现
    
    后缀数组是字符串所有后缀按字典序排序后的数组，
    每个元素表示对应后缀在原字符串中的起始位置。
    """
    
    def __init__(self, text: str):
        """
        初始化后缀数组
        
        Args:
            text: 输入字符串
        """
        self.text = text
        self.n = len(text)
        self.suffix_array: List[int] = []
        self.lcp_array: List[int] = []
        self.rank: List[int] = []
        
        if self.n > 0:
            self._build_suffix_array()
            self._build_lcp_array()
    
    def _build_suffix_array(self) -> None:
        """
        构建后缀数组 - 使用倍增算法
        时间复杂度: O(n log n)
        """
        n = self.n
        text = self.text
        
        # 初始化：按单个字符排序
        # k 表示当前比较的长度，从1开始倍增
        suffix = list(range(n))
        rank = [ord(c) for c in text]
        tmp = [0] * n
        
        k = 1
        while k < n:
            # 按二元组 (rank[i], rank[i+k]) 排序
            def sort_key(i: int) -> Tuple[int, int]:
                return (rank[i], rank[i + k] if i + k < n else -1)
            
            suffix.sort(key=sort_key)
            
            # 重新分配排名
            tmp[suffix[0]] = 0
            for i in range(1, n):
                prev_key = sort_key(suffix[i - 1])
                curr_key = sort_key(suffix[i])
                tmp[suffix[i]] = tmp[suffix[i - 1]] + (prev_key != curr_key)
            
            rank = tmp[:]
            
            # 如果所有排名都不同，排序完成
            if rank[suffix[n - 1]] == n - 1:
                break
            
            k *= 2
        
        self.suffix_array = suffix
        self.rank = rank
    
    def _build_lcp_array(self) -> None:
        """
        构建LCP数组 (最长公共前缀数组)
        LCP[i] 表示 SA[i] 和 SA[i-1] 对应后缀的最长公共前缀长度
        时间复杂度: O(n)
        """
        n = self.n
        sa = self.suffix_array
        rank = self.rank
        
        lcp = [0] * n
        
        # 单字符特殊处理
        if n == 1:
            self.lcp_array = lcp
            return
        
        k = 0
        for i in range(n):
            if rank[i] == 0:
                k = 0
                continue
            
            # SA中相邻后缀的前一个位置
            j = sa[rank[i] - 1]
            
            # 利用已计算的LCP值
            while i + k < n and j + k < n and self.text[i + k] == self.text[j + k]:
                k += 1
            
            lcp[rank[i]] = k
            
            if k > 0:
                k -= 1
        
        self.lcp_array = lcp
    
    def search(self, pattern: str) -> List[int]:
        """
        在文本中查找模式串的所有出现位置
        
        Args:
            pattern: 要查找的模式串
            
        Returns:
            所有匹配位置的列表（按字典序排列）
        """
        if not pattern or self.n == 0:
            return []
        
        m = len(pattern)
        sa = self.suffix_array
        n = self.n
        
        # 二分查找左边界
        def compare_pattern(idx: int) -> int:
            """比较模式串与后缀，返回 -1, 0, 1"""
            suffix_start = sa[idx]
            for i in range(m):
                if suffix_start + i >= n:
                    return 1  # 后缀较短，模式串更大
                if pattern[i] < self.text[suffix_start + i]:
                    return -1
                if pattern[i] > self.text[suffix_start + i]:
                    return 1
            return 0  # 完全匹配
        
        # 找左边界
        left, right = 0, n - 1
        while left < right:
            mid = (left + right) // 2
            if compare_pattern(mid) > 0:
                left = mid + 1
            else:
                right = mid
        
        start = left
        if compare_pattern(start) != 0:
            return []
        
        # 找右边界
        left, right = 0, n - 1
        while left < right:
            mid = (left + right + 1) // 2
            if compare_pattern(mid) < 0:
                right = mid - 1
            else:
                left = mid
        
        end = right
        
        # 返回所有匹配位置
        return [sa[i] for i in range(start, end + 1)]
    
    def contains(self, pattern: str) -> bool:
        """
        检查模式串是否存在于文本中
        
        Args:
            pattern: 要查找的模式串
            
        Returns:
            是否存在
        """
        return len(self.search(pattern)) > 0
    
    def count_occurrences(self, pattern: str) -> int:
        """
        统计模式串在文本中出现的次数
        
        Args:
            pattern: 要统计的模式串
            
        Returns:
            出现次数
        """
        return len(self.search(pattern))
    
    def longest_repeated_substring(self) -> Tuple[str, List[Tuple[int, int]]]:
        """
        找出文本中最长的重复子串
        
        Returns:
            (最长重复子串, [(起始位置1, 结束位置1), ...])
        """
        if self.n == 0:
            return ("", [])
        
        # 找LCP数组中的最大值（跳过第一个元素，因为LCP[0]=0）
        max_lcp = 0
        max_idx = -1
        for i in range(1, self.n):
            if self.lcp_array[i] > max_lcp:
                max_lcp = self.lcp_array[i]
                max_idx = i
        
        if max_lcp == 0:
            return ("", [])
        
        # 收集所有具有最大LCP的相邻对
        positions = []
        for i in range(1, self.n):
            if self.lcp_array[i] == max_lcp:
                # SA[i-1] 和 SA[i] 这两个后缀有最长公共前缀
                pos1 = self.suffix_array[i - 1]
                pos2 = self.suffix_array[i]
                positions.append((pos1, pos1 + max_lcp))
                positions.append((pos2, pos2 + max_lcp))
        
        # 去重并排序
        positions = list(set(positions))
        positions.sort()
        
        substring = self.text[positions[0][0]:positions[0][1]]
        return (substring, positions)
    
    def all_repeated_substrings(self, min_length: int = 2) -> List[Tuple[str, List[Tuple[int, int]]]]:
        """
        找出所有长度超过阈值的重复子串
        
        Args:
            min_length: 最小长度阈值
            
        Returns:
            列表，每项为 (子串, [位置列表])
        """
        if self.n == 0:
            return []
        
        result = []
        n = self.n
        sa = self.suffix_array
        lcp = self.lcp_array
        
        # 使用栈来追踪重复子串
        i = 1
        while i < n:
            if lcp[i] >= min_length:
                # 找到一组重复子串
                group_start = i
                current_lcp = lcp[i]
                
                # 扩展到所有相邻且LCP足够的后缀
                while i < n and lcp[i] >= min_length:
                    i += 1
                
                group_end = i
                
                # 提取公共子串
                substring = self.text[sa[group_start]:sa[group_start] + current_lcp]
                
                # 收集所有出现位置
                positions = []
                for j in range(group_start - 1, group_end):
                    start = sa[j]
                    end = start + current_lcp
                    positions.append((start, end))
                
                # 去重
                positions = list(set(positions))
                positions.sort()
                
                if len(positions) >= 2:
                    result.append((substring, positions))
            else:
                i += 1
        
        # 按长度降序排列
        result.sort(key=lambda x: len(x[0]), reverse=True)
        return result
    
    def longest_common_substring(self, other: str) -> Tuple[str, Tuple[int, int]]:
        """
        找出与另一个字符串的最长公共子串
        
        Args:
            other: 另一个字符串
            
        Returns:
            (公共子串, (在self中的位置, 在other中的位置))
        """
        if self.n == 0 or not other:
            return ("", (-1, -1))
        
        # 使用一个不在两个字符串中出现的分隔符
        separator = '#'
        while separator in self.text or separator in other:
            separator = chr(ord(separator) + 1)
            if ord(separator) > 127:
                separator = chr(1)
                break
        
        # 构建连接字符串
        combined = self.text + separator + other
        n1 = self.n
        n2 = len(other)
        total_len = len(combined)
        
        # 构建连接字符串的后缀数组
        combined_sa = SuffixArray(combined)
        
        # 在LCP数组中找最大值，且两个后缀分别来自两个字符串
        max_lcp = 0
        best_pos = (-1, -1)
        
        for i in range(1, total_len):
            pos1 = combined_sa.suffix_array[i - 1]
            pos2 = combined_sa.suffix_array[i]
            
            # 一个在第一个字符串，一个在第二个字符串
            in_first1 = pos1 < n1
            in_first2 = pos2 < n1
            
            if in_first1 != in_first2:  # 分别来自两个字符串
                lcp = combined_sa.lcp_array[i]
                
                # 关键修正：来自第一个字符串的后缀的有效长度不能超过分隔符
                # 即不能超过 n1 - pos（如果来自第一个字符串）
                if in_first1:
                    # pos1 来自第一个字符串，有效长度限制为 n1 - pos1
                    effective_lcp = min(lcp, n1 - pos1)
                else:
                    # pos2 来自第一个字符串，有效长度限制为 n1 - pos2
                    effective_lcp = min(lcp, n1 - pos2)
                
                if effective_lcp > max_lcp:
                    max_lcp = effective_lcp
                    if in_first1:
                        best_pos = (pos1, pos2 - n1 - 1)
                    else:
                        best_pos = (pos2, pos1 - n1 - 1)
        
        if max_lcp == 0:
            return ("", (-1, -1))
        
        substring = self.text[best_pos[0]:best_pos[0] + max_lcp]
        return (substring, best_pos)
    
    def distinct_substrings_count(self) -> int:
        """
        计算文本中不同子串的数量
        
        Returns:
            不同子串的数量
        """
        if self.n == 0:
            return 0
        
        # 总子串数 - 所有LCP值之和
        total = self.n * (self.n + 1) // 2
        lcp_sum = sum(self.lcp_array)
        
        return total - lcp_sum
    
    def kth_substring(self, k: int) -> str:
        """
        找出字典序第k小的子串（从1开始）
        
        Args:
            k: 子串的排名（从1开始）
            
        Returns:
            第k小的子串
        """
        if k < 1 or self.n == 0:
            return ""
        
        count = 0
        for i in range(self.n):
            sa_pos = self.suffix_array[i]
            # 这个后缀贡献的子串数量
            substr_count = self.n - sa_pos
            
            # 减去与前一个后缀重复的部分
            if i > 0:
                substr_count -= self.lcp_array[i]
            
            if count + substr_count >= k:
                # 第k小子串在这个后缀中
                start = sa_pos
                # 需要跳过的子串数
                skip = k - count - 1
                # 加上LCP部分
                if i > 0:
                    skip += self.lcp_array[i]
                end = sa_pos + skip + 1
                return self.text[start:end]
            
            count += substr_count
        
        return ""
    
    def get_suffix(self, rank: int) -> str:
        """
        获取指定排名的后缀
        
        Args:
            rank: 排名（从0开始）
            
        Returns:
            对应的后缀字符串
        """
        if rank < 0 or rank >= self.n:
            return ""
        return self.text[self.suffix_array[rank]:]
    
    def get_rank(self, position: int) -> int:
        """
        获取指定位置后缀的排名
        
        Args:
            position: 后缀起始位置
            
        Returns:
            排名（从0开始）
        """
        if position < 0 or position >= self.n:
            return -1
        return self.rank[position]
    
    def compare_substrings(self, start1: int, start2: int, length: int) -> int:
        """
        比较两个子串的字典序
        
        Args:
            start1: 第一个子串的起始位置
            start2: 第二个子串的起始位置
            length: 比较的长度
            
        Returns:
            -1: 子串1 < 子串2
            0: 子串1 == 子串2
            1: 子串1 > 子串2
        """
        for i in range(length):
            if start1 + i >= self.n and start2 + i >= self.n:
                return 0
            if start1 + i >= self.n:
                return -1
            if start2 + i >= self.n:
                return 1
            
            c1 = self.text[start1 + i]
            c2 = self.text[start2 + i]
            
            if c1 < c2:
                return -1
            if c1 > c2:
                return 1
        
        return 0


def build_suffix_array(text: str) -> List[int]:
    """
    快速构建后缀数组
    
    Args:
        text: 输入字符串
        
    Returns:
        后缀数组
    """
    sa = SuffixArray(text)
    return sa.suffix_array


def build_lcp_array(text: str) -> List[int]:
    """
    快速构建LCP数组
    
    Args:
        text: 输入字符串
        
    Returns:
        LCP数组
    """
    sa = SuffixArray(text)
    return sa.lcp_array


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    在文本中查找模式串的所有出现位置
    
    Args:
        text: 输入文本
        pattern: 要查找的模式串
        
    Returns:
        所有匹配位置的列表
    """
    sa = SuffixArray(text)
    return sa.search(pattern)


def longest_repeated_substring(text: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    找出文本中最长的重复子串
    
    Args:
        text: 输入文本
        
    Returns:
        (最长重复子串, [位置列表])
    """
    sa = SuffixArray(text)
    return sa.longest_repeated_substring()


def longest_common_substring(text1: str, text2: str) -> Tuple[str, Tuple[int, int]]:
    """
    找出两个字符串的最长公共子串
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        (公共子串, (在text1中的位置, 在text2中的位置))
    """
    sa = SuffixArray(text1)
    return sa.longest_common_substring(text2)


def count_distinct_substrings(text: str) -> int:
    """
    计算字符串中不同子串的数量
    
    Args:
        text: 输入字符串
        
    Returns:
        不同子串的数量
    """
    sa = SuffixArray(text)
    return sa.distinct_substrings_count()


def pattern_exists(text: str, pattern: str) -> bool:
    """
    检查模式串是否存在于文本中
    
    Args:
        text: 输入文本
        pattern: 模式串
        
    Returns:
        是否存在
    """
    sa = SuffixArray(text)
    return sa.contains(pattern)


# 高级功能
class SuffixArrayAdvanced(SuffixArray):
    """
    后缀数组高级功能扩展
    """
    
    def __init__(self, text: str):
        super().__init__(text)
        self._rmq_cache: Optional[List[List[int]]] = None
    
    def _build_rmq(self) -> None:
        """构建RMQ（区间最小值查询）表，用于快速LCP查询"""
        n = self.n
        if n == 0:
            return
        
        log = [0] * (n + 1)
        for i in range(2, n + 1):
            log[i] = log[i // 2] + 1
        
        k = log[n] + 1
        self._rmq_cache = [[0] * k for _ in range(n)]
        
        for i in range(n):
            self._rmq_cache[i][0] = self.lcp_array[i]
        
        for j in range(1, k):
            for i in range(n - (1 << j) + 1):
                self._rmq_cache[i][j] = min(
                    self._rmq_cache[i][j - 1],
                    self._rmq_cache[i + (1 << (j - 1))][j - 1]
                )
    
    def lcp_between_suffixes(self, i: int, j: int) -> int:
        """
        计算两个后缀的最长公共前缀
        
        Args:
            i: 第一个后缀的起始位置
            j: 第二个后缀的起始位置
            
        Returns:
            LCP长度
        """
        if i == j:
            return self.n - i
        
        rank_i = self.rank[i]
        rank_j = self.rank[j]
        
        if rank_i > rank_j:
            rank_i, rank_j = rank_j, rank_i
        
        # LCP(rank_i, rank_j) = min(LCP[rank_i+1...rank_j])
        return self._range_lcp(rank_i + 1, rank_j)
    
    def _range_lcp(self, left: int, right: int) -> int:
        """使用RMQ计算区间最小LCP"""
        if left > right:
            return 0
        
        if self._rmq_cache is None:
            self._build_rmq()
        
        if self._rmq_cache is None or self.n == 0:
            return 0
        
        import math
        length = right - left + 1
        k = int(math.log2(length))
        
        return min(
            self._rmq_cache[left][k],
            self._rmq_cache[right - (1 << k) + 1][k]
        )
    
    def count_substring_occurrences(self, substring: str) -> int:
        """
        统计子串在文本中出现的次数（考虑重叠）
        
        Args:
            substring: 子串
            
        Returns:
            出现次数
        """
        return self.count_occurrences(substring)
    
    def find_maximal_palindromes(self) -> List[Tuple[int, int]]:
        """
        找出所有极大回文子串的位置
        
        Returns:
            列表，每项为 (中心位置, 半径)
        """
        # 构建反转字符串的后缀数组
        reversed_text = self.text[::-1]
        reversed_sa = SuffixArray(reversed_text)
        
        palindromes = []
        n = self.n
        
        for center in range(n):
            # 奇数长度回文
            radius = 0
            while center - radius >= 0 and center + radius < n:
                if self.text[center - radius] == self.text[center + radius]:
                    radius += 1
                else:
                    break
            
            if radius > 0:
                palindromes.append((center, radius - 1, 'odd'))
            
            # 偶数长度回文
            radius = 0
            left_center = center
            right_center = center + 1
            while left_center - radius >= 0 and right_center + radius < n:
                if self.text[left_center - radius] == self.text[right_center + radius]:
                    radius += 1
                else:
                    break
            
            if radius > 0:
                palindromes.append((center, radius, 'even'))
        
        # 过滤出极大回文
        maximal = []
        for i, (center, radius, ptype) in enumerate(palindromes):
            is_maximal = True
            for j, (c, r, t) in enumerate(palindromes):
                if i != j and c == center:
                    if (ptype == 'odd' and t == 'odd' and r > radius):
                        is_maximal = False
                        break
                    if (ptype == 'even' and t == 'even' and r > radius):
                        is_maximal = False
                        break
            
            if is_maximal and ((ptype == 'odd' and radius > 0) or 
                              (ptype == 'even' and radius > 0)):
                maximal.append((center, radius, ptype))
        
        return maximal


if __name__ == "__main__":
    # 简单演示
    text = "banana"
    sa = SuffixArray(text)
    
    print(f"文本: {text}")
    print(f"后缀数组: {sa.suffix_array}")
    print(f"LCP数组: {sa.lcp_array}")
    print(f"排序后的后缀:")
    for i, pos in enumerate(sa.suffix_array):
        print(f"  {i}: {text[pos:]}")
    
    print(f"\n查找 'ana': {sa.search('ana')}")
    print(f"最长重复子串: {sa.longest_repeated_substring()}")
    print(f"不同子串数量: {sa.distinct_substrings_count()}")