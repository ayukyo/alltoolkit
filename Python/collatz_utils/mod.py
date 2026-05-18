"""
考拉兹猜想工具模块 (Collatz Conjecture Utils)

考拉兹猜想（也称为3n+1猜想、冰雹猜想）是数学中最著名的未解问题之一。
对于任意正整数 n：
- 如果 n 是偶数，则 n = n / 2
- 如果 n 是奇数，则 n = 3 * n + 1
猜想认为，无论从哪个正整数开始，最终都会到达 1。

功能：
- 生成完整的考拉兹序列
- 计算到达1所需的步数
- 找出序列中的最大值
- 批量分析多个数字
- 找出指定范围内最长序列的起始数
- 验证考拉兹猜想（对指定范围内的数）
"""

from typing import List, Tuple, Dict, Optional
from functools import lru_cache


def collatz_step(n: int) -> int:
    """
    执行一步考拉兹变换
    
    Args:
        n: 正整数
        
    Returns:
        变换后的数值
        
    Raises:
        ValueError: 如果 n 不是正整数
        
    Examples:
        >>> collatz_step(6)
        3
        >>> collatz_step(7)
        22
        >>> collatz_step(1)
        4
    """
    if n < 1:
        raise ValueError("n 必须是正整数")
    
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def generate_sequence(n: int, max_steps: int = 10000, include_cycle: bool = False) -> List[int]:
    """
    生成从 n 开始的完整考拉兹序列
    
    Args:
        n: 起始正整数
        max_steps: 最大步数限制（防止无限循环）
        include_cycle: 是否包含 4-2-1 循环（当 n=1 时生成 [1,4,2,1]）
        
    Returns:
        考拉兹序列列表
        
    Raises:
        ValueError: 如果 n 不是正整数或超过最大步数
        
    Examples:
        >>> generate_sequence(6)
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> generate_sequence(7)
        [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        >>> generate_sequence(1, include_cycle=True)
        [1, 4, 2, 1]
        >>> generate_sequence(1)
        [1]
    """
    if n < 1:
        raise ValueError("n 必须是正整数")
    
    sequence = [n]
    current = n
    steps = 0
    
    # 对于 n=1 的特殊情况
    if n == 1 and include_cycle:
        sequence.extend([4, 2, 1])
        return sequence
    
    while current != 1 and steps < max_steps:
        current = collatz_step(current)
        sequence.append(current)
        steps += 1
    
    if current != 1:
        raise ValueError(f"在 {max_steps} 步内未收敛到 1，可能存在反例！")
    
    return sequence


@lru_cache(maxsize=10000)
def get_steps_to_one(n: int) -> int:
    """
    计算从 n 到达 1 所需的步数（使用缓存优化）
    
    步数定义为从 n 变换到 1 所需的操作次数（不包括起始值）
    例如：6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 需要 8 步
    
    Args:
        n: 赵始正整数
        
    Returns:
        到达 1 所需的步数
        
    Raises:
        ValueError: 如果 n 不是正整数
        
    Examples:
        >>> get_steps_to_one(6)
        8
        >>> get_steps_to_one(1)
        0
        >>> get_steps_to_one(27)
        111
    """
    if n < 1:
        raise ValueError("n 必须是正整数")
    
    if n == 1:
        return 0
    
    return 1 + get_steps_to_one(collatz_step(n))


def get_max_value(n: int) -> int:
    """
    获取从 n 开始的考拉兹序列中的最大值
    
    Args:
        n: 起始正整数
        
    Returns:
        序列中的最大值
        
    Examples:
        >>> get_max_value(6)
        16
        >>> get_max_value(27)
        9232
    """
    sequence = generate_sequence(n)
    return max(sequence)


def get_max_value_position(n: int) -> Tuple[int, int]:
    """
    获取从 n 开始的考拉兹序列中最大值及其位置
    
    Args:
        n: 起始正整数
        
    Returns:
        (最大值, 位置索引) 元组
        
    Examples:
        >>> get_max_value_position(6)
        (16, 4)
        >>> get_max_value_position(27)
        (9232, 71)
    """
    sequence = generate_sequence(n)
    max_val = max(sequence)
    position = sequence.index(max_val)
    return (max_val, position)


def analyze(n: int) -> Dict:
    """
    全面分析从 n 开始的考拉兹序列
    
    Args:
        n: 起始正整数
        
    Returns:
        包含以下键的字典：
        - start_value: 起始值
        - steps: 到达1的步数
        - max_value: 序列中的最大值
        - max_value_step: 最大值出现的步数
        - sequence_length: 序列总长度（含起始和结尾的1）
        - odd_count: 奇数出现次数
        - even_count: 偶数出现次数
        - sequence: 完整序列（可选）
        
    Examples:
        >>> result = analyze(6)
        >>> result['steps']
        7
        >>> result['max_value']
        16
    """
    sequence = generate_sequence(n)
    
    odd_count = sum(1 for x in sequence if x % 2 == 1)
    even_count = len(sequence) - odd_count
    max_val = max(sequence)
    max_val_step = sequence.index(max_val)
    
    return {
        'start_value': n,
        'steps': get_steps_to_one(n),
        'max_value': max_val,
        'max_value_step': max_val_step,
        'sequence_length': len(sequence),
        'odd_count': odd_count,
        'even_count': even_count,
        'sequence': sequence
    }


def find_longest_sequence(limit: int) -> Tuple[int, int]:
    """
    在 1 到 limit 范围内找出到达1需要最多步数的起始数
    
    Args:
        limit: 搜索上限
        
    Returns:
        (起始数, 步数) 元组
        
    Examples:
        >>> find_longest_sequence(10)
        (9, 19)
        >>> find_longest_sequence(100)
        (97, 118)
    """
    max_steps = 0
    max_n = 1
    
    for n in range(1, limit + 1):
        steps = get_steps_to_one(n)
        if steps > max_steps:
            max_steps = steps
            max_n = n
    
    return (max_n, max_steps)


def find_highest_value(limit: int) -> Tuple[int, int]:
    """
    在 1 到 limit 范围内找出产生最高中间值的起始数
    
    Args:
        limit: 搜索上限
        
    Returns:
        (起始数, 最大值) 元组
        
    Examples:
        >>> find_highest_value(10)
        (9, 52)
    """
    max_val = 1
    max_n = 1
    
    for n in range(1, limit + 1):
        val = get_max_value(n)
        if val > max_val:
            max_val = val
            max_n = n
    
    return (max_n, max_val)


def verify_conjecture(limit: int) -> Tuple[bool, int]:
    """
    验证考拉兹猜想对 1 到 limit 范围内的所有整数成立
    
    Args:
        limit: 验证上限
        
    Returns:
        (是否全部通过验证, 验证数量) 元组
        
    Examples:
        >>> verify_conjecture(100)
        (True, 100)
        >>> verify_conjecture(1000)[0]
        True
    """
    count = 0
    for n in range(1, limit + 1):
        try:
            get_steps_to_one(n)
            count += 1
        except ValueError:
            return (False, count)
    
    return (True, count)


def batch_analyze(numbers: List[int]) -> List[Dict]:
    """
    批量分析多个数字的考拉兹序列
    
    Args:
        numbers: 起始数字列表
        
    Returns:
        分析结果列表
        
    Examples:
        >>> results = batch_analyze([1, 2, 3, 4, 5])
        >>> len(results)
        5
    """
    return [analyze(n) for n in numbers]


def get_odd_even_ratio(n: int) -> float:
    """
    计算考拉兹序列中奇数与偶数的比例
    
    Args:
        n: 起始正整数
        
    Returns:
        奇数/偶数 比例
        
    Examples:
        >>> get_odd_even_ratio(6)
        0.5
    """
    result = analyze(n)
    if result['even_count'] == 0:
        return float('inf')
    return result['odd_count'] / result['even_count']


def get_convergence_tree(n: int, max_depth: int = 10) -> Dict:
    """
    获取收敛到 n 的"反向考拉兹树"
    
    对于数字 n，找出可能收敛到它的前驱节点：
    - 如果 n 是偶数，前驱可以是 2n
    - 如果 (n-1) 能被 3 整除且结果为奇数，前驱可以是 (n-1)/3
    
    Args:
        n: 目标数字
        max_depth: 最大搜索深度
        
    Returns:
        表示收敛树的字典
        
    Examples:
        >>> tree = get_convergence_tree(1, 3)
        >>> 2 in tree['children']
        True
    """
    def build_tree(num: int, depth: int, visited: set) -> Dict:
        if depth > max_depth or num in visited:
            return {'value': num, 'children': [], 'truncated': depth > max_depth}
        
        visited = visited | {num}
        children = []
        
        # 前驱 1: 2n 总是收敛到 n
        pred1 = 2 * num
        if pred1 not in visited:
            children.append(build_tree(pred1, depth + 1, visited))
        
        # 前驱 2: 如果 (n-1) 能被 3 整除且结果为奇数大于1
        if (num - 1) % 3 == 0:
            pred2 = (num - 1) // 3
            if pred2 > 1 and pred2 % 2 == 1 and pred2 not in visited:
                children.append(build_tree(pred2, depth + 1, visited))
        
        return {'value': num, 'children': children, 'truncated': False}
    
    return build_tree(n, 0, set())


def get_stopping_time(n: int) -> int:
    """
    获取停止时间（首次降到起始值以下所需的步数）
    
    这是考拉兹猜想研究中的一个重要概念
    
    Args:
        n: 起始正整数
        
    Returns:
        停止时间，如果始终不降到起始值以下则返回 -1
        
    Examples:
        >>> get_stopping_time(6)
        1
        >>> get_stopping_time(7)
        7
    """
    if n < 1:
        raise ValueError("n 必须是正整数")
    
    if n == 1:
        return 0
    
    current = n
    steps = 0
    
    while steps < 10000:
        current = collatz_step(current)
        steps += 1
        if current < n:
            return steps
        if current == 1:
            return -1  # 直接到达1，没有降到起始值以下
    
    return -1


def is_in_4_2_1_cycle(n: int) -> bool:
    """
    检查数字是否在 4-2-1 循环中
    
    Args:
        n: 要检查的数字
        
    Returns:
        是否在 4-2-1 循环中
        
    Examples:
        >>> is_in_4_2_1_cycle(1)
        True
        >>> is_in_4_2_1_cycle(4)
        True
        >>> is_in_4_2_1_cycle(3)
        False
    """
    return n in (1, 2, 4)


def get_total_stopping_time(n: int) -> int:
    """
    获取总停止时间（到达1所需的步数）
    
    这是 get_steps_to_one 的别名，提供更专业的术语
    
    Args:
        n: 起始正整数
        
    Returns:
        总停止时间
        
    Examples:
        >>> get_total_stopping_time(27)
        111
    """
    return get_steps_to_one(n)


def get_eta(n: int) -> int:
    """
    获取扩充时间 (Eta) - 序列达到最大值所需的步数
    
    Args:
        n: 赵始正整数
        
    Returns:
        达到最大值的步数
        
    Examples:
        >>> get_eta(27)
        71
    """
    _, position = get_max_value_position(n)
    return position


def format_sequence(n: int, separator: str = " → ") -> str:
    """
    将考拉兹序列格式化为字符串
    
    Args:
        n: 起始正整数
        separator: 分隔符
        
    Returns:
        格式化的序列字符串
        
    Examples:
        >>> format_sequence(6)
        '6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1'
    """
    sequence = generate_sequence(n)
    return separator.join(str(x) for x in sequence)


def get_statistics(limit: int) -> Dict:
    """
    获取 1 到 limit 范围内的考拉兹序列统计信息
    
    Args:
        limit: 统计上限
        
    Returns:
        包含统计信息的字典
        
    Examples:
        >>> stats = get_statistics(10)
        >>> stats['total_numbers']
        10
    """
    total_steps = 0
    max_steps = 0
    max_steps_n = 1
    max_value = 1
    max_value_n = 1
    total_odd = 0
    total_even = 0
    
    for n in range(1, limit + 1):
        result = analyze(n)
        total_steps += result['steps']
        total_odd += result['odd_count']
        total_even += result['even_count']
        
        if result['steps'] > max_steps:
            max_steps = result['steps']
            max_steps_n = n
        
        if result['max_value'] > max_value:
            max_value = result['max_value']
            max_value_n = n
    
    return {
        'total_numbers': limit,
        'average_steps': total_steps / limit if limit > 0 else 0,
        'max_steps': max_steps,
        'max_steps_number': max_steps_n,
        'max_value': max_value,
        'max_value_number': max_value_n,
        'total_odd_operations': total_odd,
        'total_even_operations': total_even,
        'odd_even_ratio': total_odd / total_even if total_even > 0 else 0
    }


class CollatzSequence:
    """
    考拉兹序列类，提供迭代器和属性访问
    
    Examples:
        >>> seq = CollatzSequence(6)
        >>> list(seq)
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> seq.steps
        7
    """
    
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n 必须是正整数")
        self._start = n
        self._sequence = None
        self._analysis = None
    
    def _ensure_sequence(self):
        if self._sequence is None:
            self._sequence = generate_sequence(self._start)
        return self._sequence
    
    def _ensure_analysis(self):
        if self._analysis is None:
            self._analysis = analyze(self._start)
        return self._analysis
    
    def __iter__(self):
        return iter(self._ensure_sequence())
    
    def __len__(self):
        return len(self._ensure_sequence())
    
    def __getitem__(self, index):
        return self._ensure_sequence()[index]
    
    @property
    def start(self) -> int:
        """起始值"""
        return self._start
    
    @property
    def steps(self) -> int:
        """到达1的步数"""
        return self._ensure_analysis()['steps']
    
    @property
    def max_value(self) -> int:
        """序列中的最大值"""
        return self._ensure_analysis()['max_value']
    
    @property
    def odd_count(self) -> int:
        """奇数操作次数"""
        return self._ensure_analysis()['odd_count']
    
    @property
    def even_count(self) -> int:
        """偶数操作次数"""
        return self._ensure_analysis()['even_count']
    
    @property
    def sequence(self) -> List[int]:
        """完整序列"""
        return self._ensure_sequence()
    
    def __repr__(self):
        return f"CollatzSequence({self._start})"
    
    def __str__(self):
        return format_sequence(self._start)


if __name__ == "__main__":
    # 简单演示
    print("考拉兹猜想工具演示")
    print("=" * 50)
    
    # 演示单个数字分析
    n = 27
    print(f"\n分析数字 {n}:")
    result = analyze(n)
    print(f"  步数: {result['steps']}")
    print(f"  最大值: {result['max_value']}")
    print(f"  序列长度: {result['sequence_length']}")
    print(f"  序列: {format_sequence(n)}")
    
    # 演示找最长序列
    limit = 100
    print(f"\n在 1-{limit} 范围内:")
    longest_n, longest_steps = find_longest_sequence(limit)
    print(f"  最长序列起始数: {longest_n}")
    print(f"  步数: {longest_steps}")
    
    # 验证猜想
    verified, count = verify_conjecture(1000)
    print(f"\n验证 1-1000 范围: {'通过' if verified else '失败'} ({count} 个数)")
    
    # 使用类接口
    print(f"\n使用 CollatzSequence 类:")
    seq = CollatzSequence(6)
    print(f"  序列: {list(seq)}")
    print(f"  步数: {seq.steps}")
    print(f"  最大值: {seq.max_value}")