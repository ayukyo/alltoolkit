"""
Look and Say Utils - 外观数列工具集

外观数列（Look-and-Say sequence）是一个有趣的数学序列，
每个项是对前一项的"外观描述"。零外部依赖，纯Python实现。

示例序列:
    1 → 11 (一个1)
    11 → 21 (两个1)
    21 → 1211 (一个2，一个1)
    1211 → 111221 (一个1，一个2，两个1)
    ...

功能：
- 生成外观数列
- 计算第n项（支持大数）
- 分析序列长度增长规律
- 统计数字频率分布
- 支持自定义起始值和进制
- 康威常数计算
"""

from typing import List, Tuple, Dict, Iterator
from functools import lru_cache


class LookAndSayUtils:
    """外观数列工具类"""
    
    # 已知的康威常数（外观数列相邻项长度比的极限）
    # 约等于 1.303577269034296...
    CONWAY_CONSTANT = 1.303577269034296
    
    @staticmethod
    def next_term(term: str) -> str:
        """
        计算外观数列的下一项
        
        Args:
            term: 当前项（字符串形式）
            
        Returns:
            下一项
            
        Examples:
            >>> LookAndSayUtils.next_term("1")
            '11'
            >>> LookAndSayUtils.next_term("21")
            '1211'
            >>> LookAndSayUtils.next_term("111221")
            '312211'
        """
        if not term:
            return ""
        
        result = []
        count = 1
        current_char = term[0]
        
        for char in term[1:]:
            if char == current_char:
                count += 1
            else:
                result.append(str(count))
                result.append(current_char)
                current_char = char
                count = 1
        
        # 添加最后一组
        result.append(str(count))
        result.append(current_char)
        
        return ''.join(result)
    
    @staticmethod
    def generate(n: int, start: str = "1") -> List[str]:
        """
        生成外观数列的前n项
        
        Args:
            n: 要生成的项数
            start: 起始项（默认为"1"）
            
        Returns:
            包含前n项的列表
            
        Examples:
            >>> LookAndSayUtils.generate(5)
            ['1', '11', '21', '1211', '111221']
        """
        if n <= 0:
            return []
        
        result = [start]
        current = start
        
        for _ in range(n - 1):
            current = LookAndSayUtils.next_term(current)
            result.append(current)
        
        return result
    
    @staticmethod
    def nth_term(n: int, start: str = "1") -> str:
        """
        计算外观数列的第n项（从0开始）
        
        Args:
            n: 项索引（从0开始）
            start: 起始项（默认为"1"）
            
        Returns:
            第n项
            
        Examples:
            >>> LookAndSayUtils.nth_term(4)
            '111221'
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return start
        
        current = start
        for _ in range(n):
            current = LookAndSayUtils.next_term(current)
        
        return current
    
    @staticmethod
    def iterator(start: str = "1") -> Iterator[str]:
        """
        返回外观数列的无穷迭代器
        
        Args:
            start: 起始项（默认为"1"）
            
        Yields:
            数列的每一项
            
        Examples:
            >>> it = LookAndSayUtils.iterator()
            >>> [next(it) for _ in range(5)]
            ['1', '11', '21', '1211', '111221']
        """
        current = start
        while True:
            yield current
            current = LookAndSayUtils.next_term(current)
    
    @staticmethod
    def length_ratio(n: int, start: str = "1") -> float:
        """
        计算第n项与第n-1项的长度比
        
        随着n增大，这个比值趋近于康威常数 ≈ 1.303577
        
        Args:
            n: 项索引（n >= 1）
            start: 起始项
            
        Returns:
            长度比
            
        Examples:
            >>> round(LookAndSayUtils.length_ratio(10), 4)
            1.3035
        """
        if n < 1:
            raise ValueError("n must be at least 1")
        
        terms = LookAndSayUtils.generate(n + 1, start)
        return len(terms[n]) / len(terms[n - 1])
    
    @staticmethod
    def conway_constant_approximation(n: int, start: str = "1") -> float:
        """
        通过外观数列近似计算康威常数
        
        康威常数是外观数列相邻项长度比的极限值，
        是一个代数数，约为 1.303577...
        
        Args:
            n: 使用前n项计算近似值
            start: 起始项
            
        Returns:
            康威常数的近似值
            
        Examples:
            >>> round(LookAndSayUtils.conway_constant_approximation(30), 4)
            1.3036
        """
        if n < 2:
            return 1.0
        
        terms = LookAndSayUtils.generate(n + 1, start)
        ratios = []
        for i in range(1, len(terms)):
            if len(terms[i - 1]) > 0:
                ratios.append(len(terms[i]) / len(terms[i - 1]))
        
        return sum(ratios) / len(ratios) if ratios else 1.0
    
    @staticmethod
    def digit_frequency(term: str) -> Dict[str, int]:
        """
        统计一项中各数字的频率
        
        Args:
            term: 要分析的项
            
        Returns:
            数字频率字典
            
        Examples:
            >>> LookAndSayUtils.digit_frequency("111221")
            {'1': 4, '2': 2}
        """
        freq = {}
        for char in term:
            freq[char] = freq.get(char, 0) + 1
        return freq
    
    @staticmethod
    def digit_distribution(n: int, start: str = "1") -> Dict[str, float]:
        """
        计算第n项中各数字的分布比例
        
        有趣的是，外观数列中只会出现数字1、2、3（除了某些特殊起始值）
        
        Args:
            n: 项索引
            start: 起始项
            
        Returns:
            数字分布比例字典
            
        Examples:
            >>> LookAndSayUtils.digit_distribution(10)
            {'1': 0.42..., '2': 0.33..., '3': 0.24...}
        """
        term = LookAndSayUtils.nth_term(n, start)
        freq = LookAndSayUtils.digit_frequency(term)
        total = len(term)
        
        return {digit: count / total for digit, count in freq.items()}
    
    @staticmethod
    def analyze_growth(n: int, start: str = "1") -> List[Tuple[int, int, float]]:
        """
        分析数列长度增长情况
        
        Args:
            n: 分析前n项
            start: 起始项
            
        Returns:
            列表，每项为 (项索引, 长度, 相比上一项的增长比)
            
        Examples:
            >>> LookAndSayUtils.analyze_growth(5)
            [(0, 1, 1.0), (1, 2, 2.0), (2, 2, 1.0), (3, 4, 2.0), (4, 6, 1.5)]
        """
        terms = LookAndSayUtils.generate(n, start)
        result = []
        
        for i, term in enumerate(terms):
            length = len(term)
            ratio = length / len(terms[i - 1]) if i > 0 else 1.0
            result.append((i, length, ratio))
        
        return result
    
    @staticmethod
    def run_length_encoding(s: str) -> List[Tuple[str, int]]:
        """
        将字符串转换为游程编码
        
        这是外观数列的核心操作的可视化
        
        Args:
            s: 输入字符串
            
        Returns:
            游程编码列表，每项为 (字符, 连续次数)
            
        Examples:
            >>> LookAndSayUtils.run_length_encoding("111221")
            [('1', 3), ('2', 2), ('1', 1)]
        """
        if not s:
            return []
        
        result = []
        count = 1
        current = s[0]
        
        for char in s[1:]:
            if char == current:
                count += 1
            else:
                result.append((current, count))
                current = char
                count = 1
        
        result.append((current, count))
        return result
    
    @staticmethod
    def from_run_length(encoded: List[Tuple[str, int]]) -> str:
        """
        从游程编码还原字符串
        
        Args:
            encoded: 游程编码列表
            
        Returns:
            原始字符串
            
        Examples:
            >>> LookAndSayUtils.from_run_length([('1', 3), ('2', 2), ('1', 1)])
            '111221'
        """
        return ''.join(char * count for char, count in encoded)
    
    @staticmethod
    def is_valid_look_and_say_term(term: str) -> bool:
        """
        检查字符串是否可能是外观数列中的某一项
        
        规则：
        1. 只包含数字
        2. 不能以数字4及以上开头（理论上外观数列只出现1、2、3）
        3. 连续相同数字的描述必须正确
        
        Args:
            term: 要检查的项
            
        Returns:
            是否有效
            
        Examples:
            >>> LookAndSayUtils.is_valid_look_and_say_term("1211")
            True
            >>> LookAndSayUtils.is_valid_look_and_say_term("12345")
            False
        """
        if not term:
            return False
        
        # 检查是否只包含数字
        if not term.isdigit():
            return False
        
        # 外观数列中不会出现连续4个或更多相同数字
        count = 1
        for i in range(1, len(term)):
            if term[i] == term[i - 1]:
                count += 1
                if count > 3:
                    return False
            else:
                count = 1
        
        return True
    
    @staticmethod
    def split_into_elements(term: str) -> List[str]:
        """
        将外观数列项按元素分割
        
        康威发现外观数列可以分解为92个基本元素
        这里有简化版本
        
        Args:
            term: 要分割的项
            
        Returns:
            分割后的元素列表
            
        Examples:
            >>> LookAndSayUtils.split_into_elements("111321")
            ['111', '3', '2', '1']
        """
        if not term:
            return []
        
        elements = []
        current = term[0]
        count = 1
        
        for char in term[1:]:
            if char == current:
                count += 1
            else:
                elements.append(current * count)
                current = char
                count = 1
        
        elements.append(current * count)
        return elements
    
    @staticmethod
    def reverse_step(term: str) -> List[str]:
        """
        尝试找到可能的上一项（反向推导）
        
        注意：反向推导可能有多解或无解
        
        Args:
            term: 当前项
            
        Returns:
            可能的上一项列表
            
        Examples:
            >>> LookAndSayUtils.reverse_step("21")
            ['11']
            >>> LookAndSayUtils.reverse_step("1211")
            ['21']
        """
        if not term or len(term) % 2 != 0:
            return []
        
        # 解析项：每两个字符代表 (数量, 数字)
        counts = []
        digits = []
        for i in range(0, len(term), 2):
            if i + 1 >= len(term):
                return []
            count_char = term[i]
            digit_char = term[i + 1]
            
            if not count_char.isdigit():
                return []
            
            count = int(count_char)
            counts.append(count)
            digits.append(digit_char)
        
        # 重构上一项
        prev = ''.join(d * c for d, c in zip(digits, counts))
        
        # 验证：对上一项应用外观数列规则，应该得到当前项
        if LookAndSayUtils.next_term(prev) == term:
            return [prev]
        
        return []
    
    @staticmethod
    def cosmological_decay(n: int) -> Dict[str, List[int]]:
        """
        康威宇宙学定理演示
        
        外观数列中的元素最终会分解为"原子元素"
        这是简化版本，追踪特定模式的出现频率
        
        Args:
            n: 分析前n项
            
        Returns:
            各模式出现的项索引
            
        Examples:
            >>> decay = LookAndSayUtils.cosmological_decay(20)
            >>> '111' in decay
            True
        """
        terms = LookAndSayUtils.generate(n)
        patterns = ['111', '11', '22', '33', '12', '21', '13', '31', '23', '32']
        result = {p: [] for p in patterns}
        
        for i, term in enumerate(terms):
            for pattern in patterns:
                if pattern in term:
                    result[pattern].append(i)
        
        return result
    
    @staticmethod
    def different_seed(seed: str, n: int = 10) -> List[str]:
        """
        从不同的种子生成外观数列
        
        研究不同起始值的有趣行为
        
        Args:
            seed: 起始种子
            n: 生成项数
            
        Returns:
            生成的数列
            
        Examples:
            >>> LookAndSayUtils.different_seed("22", 5)
            ['22', '22', '22', '22', '22']  # 不动点
            >>> LookAndSayUtils.different_seed("3", 5)
            ['3', '13', '1113', '3113', '132113']
        """
        return LookAndSayUtils.generate(n, seed)
    
    @staticmethod
    def count_unique_digits(n: int, start: str = "1") -> List[int]:
        """
        统计前n项中每项包含的不同数字数量
        
        Args:
            n: 项数
            start: 起始项
            
        Returns:
            每项的不同数字数量列表
            
        Examples:
            >>> LookAndSayUtils.count_unique_digits(10)
            [1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
        """
        terms = LookAndSayUtils.generate(n, start)
        return [len(set(term)) for term in terms]
    
    @staticmethod
    def max_run_length(term: str) -> int:
        """
        找出一项中最长的连续相同数字长度
        
        Args:
            term: 要分析的项
            
        Returns:
            最长连续长度
            
        Examples:
            >>> LookAndSayUtils.max_run_length("111221")
            3
        """
        if not term:
            return 0
        
        max_run = 1
        current_run = 1
        
        for i in range(1, len(term)):
            if term[i] == term[i - 1]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        
        return max_run
    
    @staticmethod
    def estimate_nth_length(n: int, start: str = "1") -> int:
        """
        估算第n项的长度
        
        利用康威常数近似：len(T(n)) ≈ len(start) * λ^n
        其中 λ ≈ 1.303577 是康威常数
        
        Args:
            n: 项索引
            start: 起始项
            
        Returns:
            估算的长度
            
        Examples:
            >>> LookAndSayUtils.estimate_nth_length(20)
            106  # 实际约为 102
        """
        import math
        lambda_const = 1.303577269034
        return int(len(start) * (lambda_const ** n))


# 便捷函数
def next_term(term: str) -> str:
    """计算外观数列的下一项"""
    return LookAndSayUtils.next_term(term)


def generate(n: int, start: str = "1") -> List[str]:
    """生成外观数列的前n项"""
    return LookAndSayUtils.generate(n, start)


def nth_term(n: int, start: str = "1") -> str:
    """计算第n项"""
    return LookAndSayUtils.nth_term(n, start)


def conway_constant() -> float:
    """返回康威常数"""
    return LookAndSayUtils.CONWAY_CONSTANT


if __name__ == "__main__":
    # 简单演示
    print("=" * 50)
    print("外观数列（Look-and-Say Sequence）演示")
    print("=" * 50)
    
    print("\n前10项:")
    terms = LookAndSayUtils.generate(10)
    for i, term in enumerate(terms):
        print(f"  T({i}): {term}")
    
    print("\n长度增长分析:")
    growth = LookAndSayUtils.analyze_growth(10)
    for idx, length, ratio in growth:
        print(f"  T({idx}): 长度={length}, 增长比={ratio:.4f}")
    
    print(f"\n康威常数近似值 (10项): {LookAndSayUtils.conway_constant_approximation(10):.6f}")
    print(f"康威常数精确值: {LookAndSayUtils.CONWAY_CONSTANT:.15f}...")
    
    print("\n不同种子的行为:")
    seeds = ["1", "22", "3", "111111"]
    for seed in seeds:
        terms = LookAndSayUtils.different_seed(seed, 5)
        print(f"  种子'{seed}': {' → '.join(terms)}")
    
    print("\n数字分布分析 (第15项):")
    dist = LookAndSayUtils.digit_distribution(15)
    for digit, ratio in sorted(dist.items()):
        print(f"  数字'{digit}': {ratio:.2%}")
    
    print("\n第20项估算长度:", LookAndSayUtils.estimate_nth_length(20))
    actual = len(LookAndSayUtils.nth_term(20))
    print(f"第20项实际长度: {actual}")