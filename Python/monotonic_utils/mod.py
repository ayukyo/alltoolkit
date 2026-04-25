"""
单调栈和单调队列工具模块

单调栈：栈内元素保持单调递增或单调递减，用于求解下一个更大/更小元素等问题
单调队列：队列内元素保持单调性，用于滑动窗口最大/最小值等问题

零外部依赖，纯 Python 实现
"""

from typing import List, Optional, Tuple, Callable, TypeVar, Generic
from collections import deque
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class MonotonicStackResult:
    """单调栈操作结果"""
    next_greater: List[int]  # 下一个更大元素的索引，-1表示不存在
    next_smaller: List[int]  # 下一个更小元素的索引，-1表示不存在
    prev_greater: List[int]  # 上一个更大元素的索引，-1表示不存在
    prev_smaller: List[int]  # 上一个更小元素的索引，-1表示不存在


class MonotonicStack(Generic[T]):
    """
    单调栈实现
    
    支持：
    - 单调递增栈（栈底到栈顶递增）
    - 单调递减栈（栈底到栈顶递减）
    - 查找下一个更大/更小元素
    - 查找上一个更大/更小元素
    """
    
    def __init__(self, increasing: bool = True):
        """
        初始化单调栈
        
        Args:
            increasing: True 表示单调递增栈，False 表示单调递减栈
        """
        self.increasing = increasing
        self._stack: List[T] = []
        self._indices: List[int] = []  # 存储元素原始索引
    
    @property
    def is_empty(self) -> bool:
        """栈是否为空"""
        return len(self._stack) == 0
    
    @property
    def size(self) -> int:
        """栈大小"""
        return len(self._stack)
    
    @property
    def top(self) -> Optional[T]:
        """获取栈顶元素"""
        return self._stack[-1] if self._stack else None
    
    @property
    def top_index(self) -> Optional[int]:
        """获取栈顶元素的原始索引"""
        return self._indices[-1] if self._indices else None
    
    def push(self, value: T, index: int = -1) -> List[Tuple[T, int]]:
        """
        入栈，返回被弹出的元素列表（元组：值，索引）
        
        Args:
            value: 要入栈的值
            index: 元素的原始索引（可选）
        
        Returns:
            被弹出的元素列表 [(value, index), ...]
        """
        popped = []
        
        while self._stack:
            top_value = self._stack[-1]
            # 单调递增栈：弹出所有 >= value 的元素
            # 单调递减栈：弹出所有 <= value 的元素
            should_pop = (top_value >= value) if self.increasing else (top_value <= value)
            
            if should_pop:
                popped.append((self._stack.pop(), self._indices.pop()))
            else:
                break
        
        self._stack.append(value)
        self._indices.append(index)
        return popped
    
    def pop(self) -> Optional[Tuple[T, int]]:
        """出栈，返回 (value, index)"""
        if not self._stack:
            return None
        return (self._stack.pop(), self._indices.pop())
    
    def clear(self) -> None:
        """清空栈"""
        self._stack.clear()
        self._indices.clear()
    
    def to_list(self) -> List[T]:
        """转换为列表"""
        return self._stack.copy()
    
    def __len__(self) -> int:
        return len(self._stack)
    
    def __repr__(self) -> str:
        direction = "递增" if self.increasing else "递减"
        return f"MonotonicStack({direction}, {self._stack})"


def next_greater_element(nums: List[int]) -> List[int]:
    """
    找出每个元素右边第一个更大的元素
    
    Args:
        nums: 输入数组
    
    Returns:
        结果数组，result[i] 表示 nums[i] 右边第一个更大元素的值，
        如果不存在则为 -1
    
    Example:
        >>> next_greater_element([2, 1, 2, 4, 3])
        [4, 2, 4, -1, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result


def next_greater_element_index(nums: List[int]) -> List[int]:
    """
    找出每个元素右边第一个更大元素的索引
    
    Args:
        nums: 输入数组
    
    Returns:
        结果数组，result[i] 表示 nums[i] 右边第一个更大元素的索引，
        如果不存在则为 -1
    
    Example:
        >>> next_greater_element_index([2, 1, 2, 4, 3])
        [3, 2, 3, -1, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = i
        stack.append(i)
    
    return result


def next_smaller_element(nums: List[int]) -> List[int]:
    """
    找出每个元素右边第一个更小的元素
    
    Args:
        nums: 输入数组
    
    Returns:
        结果数组，result[i] 表示 nums[i] 右边第一个更小元素的值，
        如果不存在则为 -1
    
    Example:
        >>> next_smaller_element([2, 1, 2, 4, 3])
        [1, -1, 1, 3, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result


def prev_greater_element(nums: List[int]) -> List[int]:
    """
    找出每个元素左边第一个更大的元素
    
    Args:
        nums: 输入数组
    
    Returns:
        结果数组，result[i] 表示 nums[i] 左边第一个更大元素的值，
        如果不存在则为 -1
    
    Example:
        >>> prev_greater_element([2, 1, 2, 4, 3])
        [-1, 2, -1, -1, 4]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result


def prev_smaller_element(nums: List[int]) -> List[int]:
    """
    找出每个元素左边第一个更小的元素
    
    Args:
        nums: 输入数组
    
    Returns:
        结果数组，result[i] 表示 nums[i] 左边第一个更小元素的值，
        如果不存在则为 -1
    
    Example:
        >>> prev_smaller_element([2, 1, 2, 4, 3])
        [-1, -1, 1, 2, 2]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] > nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result


def compute_all_monotonic_relations(nums: List[int]) -> MonotonicStackResult:
    """
    一次性计算所有单调栈关系
    
    Args:
        nums: 输入数组
    
    Returns:
        MonotonicStackResult 包含所有关系
    
    Example:
        >>> result = compute_all_monotonic_relations([3, 1, 4, 2])
        >>> result.next_greater
        [4, 4, -1, -1]
    """
    n = len(nums)
    next_greater = [-1] * n
    next_smaller = [-1] * n
    prev_greater = [-1] * n
    prev_smaller = [-1] * n
    
    # 计算 next_greater 和 next_smaller
    stack_inc = []  # 单调递增栈（找更小）
    stack_dec = []  # 单调递减栈（找更大）
    
    for i in range(n):
        # 处理 next_greater
        while stack_dec and nums[stack_dec[-1]] < nums[i]:
            idx = stack_dec.pop()
            next_greater[idx] = i
        
        # 处理 next_smaller
        while stack_inc and nums[stack_inc[-1]] > nums[i]:
            idx = stack_inc.pop()
            next_smaller[idx] = i
        
        stack_dec.append(i)
        stack_inc.append(i)
    
    # 计算 prev_greater 和 prev_smaller
    stack_inc.clear()
    stack_dec.clear()
    
    for i in range(n - 1, -1, -1):
        # 处理 prev_greater
        while stack_dec and nums[stack_dec[-1]] < nums[i]:
            idx = stack_dec.pop()
            prev_greater[idx] = i
        
        # 处理 prev_smaller
        while stack_inc and nums[stack_inc[-1]] > nums[i]:
            idx = stack_inc.pop()
            prev_smaller[idx] = i
        
        stack_dec.append(i)
        stack_inc.append(i)
    
    return MonotonicStackResult(
        next_greater=next_greater,
        next_smaller=next_smaller,
        prev_greater=prev_greater,
        prev_smaller=prev_smaller
    )


def largest_rectangle_in_histogram(heights: List[int]) -> int:
    """
    柱状图中最大的矩形面积
    
    使用单调栈计算每个柱子能扩展的最大宽度
    
    Args:
        heights: 柱子高度数组
    
    Returns:
        最大矩形面积
    
    Example:
        >>> largest_rectangle_in_histogram([2, 1, 5, 6, 2, 3])
        10
    """
    n = len(heights)
    if n == 0:
        return 0
    
    # 计算每个位置左边第一个更小的位置
    left = [-1] * n
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    # 计算每个位置右边第一个更小的位置
    right = [n] * n
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # 计算最大面积
    max_area = 0
    for i in range(n):
        width = right[i] - left[i] - 1
        area = heights[i] * width
        max_area = max(max_area, area)
    
    return max_area


def maximal_rectangle(matrix: List[List[str]]) -> int:
    """
    最大矩形
    
    在 0-1 矩阵中找到只包含 1 的最大矩形面积
    
    Args:
        matrix: 0-1 矩阵，元素为 '0' 或 '1'
    
    Returns:
        最大矩形面积
    
    Example:
        >>> maximal_rectangle([
        ...     ["1","0","1","0","0"],
        ...     ["1","0","1","1","1"],
        ...     ["1","1","1","1","1"],
        ...     ["1","0","0","1","0"]
        ... ])
        6
    """
    if not matrix or not matrix[0]:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0
    
    for row in matrix:
        # 更新高度数组
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        
        # 计算当前行的最大矩形
        max_area = max(max_area, largest_rectangle_in_histogram(heights))
    
    return max_area


class MonotonicQueue(Generic[T]):
    """
    单调队列实现
    
    支持：
    - 单调递增队列（队首到队尾递增）
    - 单调递减队列（队首到队尾递减）
    - 滑动窗口最大/最小值查询
    """
    
    def __init__(self, increasing: bool = True):
        """
        初始化单调队列
        
        Args:
            increasing: True 表示单调递增队列，False 表示单调递减队列
        """
        self.increasing = increasing
        self._deque: deque = deque()  # 存储 (value, index)
        self._index = 0
    
    @property
    def is_empty(self) -> bool:
        """队列是否为空"""
        return len(self._deque) == 0
    
    @property
    def size(self) -> int:
        """队列大小"""
        return len(self._deque)
    
    @property
    def front(self) -> Optional[T]:
        """获取队首元素的值"""
        return self._deque[0][0] if self._deque else None
    
    @property
    def back(self) -> Optional[T]:
        """获取队尾元素的值"""
        return self._deque[-1][0] if self._deque else None
    
    def push(self, value: T, index: Optional[int] = None) -> None:
        """
        入队
        
        Args:
            value: 要入队的值
            index: 元素的索引（可选，用于滑动窗口）
        """
        if index is None:
            index = self._index
            self._index += 1
        
        # 单调递增队列：弹出所有 >= value 的元素
        # 单调递减队列：弹出所有 <= value 的元素
        while self._deque:
            back_value = self._deque[-1][0]
            should_pop = (back_value >= value) if self.increasing else (back_value <= value)
            if should_pop:
                self._deque.pop()
            else:
                break
        
        self._deque.append((value, index))
    
    def pop_front(self) -> Optional[Tuple[T, int]]:
        """队首出队，返回 (value, index)"""
        if not self._deque:
            return None
        return self._deque.popleft()
    
    def pop_expired(self, max_index: int) -> None:
        """
        弹出过期的元素（索引 < max_index）
        
        用于滑动窗口场景
        
        Args:
            max_index: 有效元素的最小索引
        """
        while self._deque and self._deque[0][1] < max_index:
            self._deque.popleft()
    
    def clear(self) -> None:
        """清空队列"""
        self._deque.clear()
        self._index = 0
    
    def to_list(self) -> List[T]:
        """转换为列表（只含值）"""
        return [item[0] for item in self._deque]
    
    def __len__(self) -> int:
        return len(self._deque)
    
    def __repr__(self) -> str:
        direction = "递增" if self.increasing else "递减"
        values = [item[0] for item in self._deque]
        return f"MonotonicQueue({direction}, {values})"


def sliding_window_max(nums: List[int], k: int) -> List[int]:
    """
    滑动窗口最大值
    
    使用单调队列，时间复杂度 O(n)
    
    Args:
        nums: 输入数组
        k: 窗口大小
    
    Returns:
        每个窗口的最大值
    
    Example:
        >>> sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [3, 3, 5, 5, 6, 7]
    """
    if not nums or k <= 0:
        return []
    
    if k == 1:
        return nums.copy()
    
    n = len(nums)
    if k > n:
        return [max(nums)]
    
    result = []
    dq = deque()  # 存储 (值, 索引)
    
    for i, num in enumerate(nums):
        # 移除窗口外的元素
        while dq and dq[0][1] <= i - k:
            dq.popleft()
        
        # 维护单调递减队列
        while dq and dq[-1][0] < num:
            dq.pop()
        
        dq.append((num, i))
        
        # 当窗口形成后，记录最大值
        if i >= k - 1:
            result.append(dq[0][0])
    
    return result


def sliding_window_min(nums: List[int], k: int) -> List[int]:
    """
    滑动窗口最小值
    
    使用单调队列，时间复杂度 O(n)
    
    Args:
        nums: 输入数组
        k: 窗口大小
    
    Returns:
        每个窗口的最小值
    
    Example:
        >>> sliding_window_min([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [-1, -3, -3, -3, 3, 3]
    """
    if not nums or k <= 0:
        return []
    
    if k == 1:
        return nums.copy()
    
    n = len(nums)
    if k > n:
        return [min(nums)]
    
    result = []
    dq = deque()  # 存储 (值, 索引)
    
    for i, num in enumerate(nums):
        # 移除窗口外的元素
        while dq and dq[0][1] <= i - k:
            dq.popleft()
        
        # 维护单调递增队列
        while dq and dq[-1][0] > num:
            dq.pop()
        
        dq.append((num, i))
        
        # 当窗口形成后，记录最小值
        if i >= k - 1:
            result.append(dq[0][0])
    
    return result


def sliding_window_max_min(nums: List[int], k: int) -> List[Tuple[int, int]]:
    """
    滑动窗口的最大值和最小值
    
    Args:
        nums: 输入数组
        k: 窗口大小
    
    Returns:
        每个窗口的 (最大值, 最小值)
    
    Example:
        >>> sliding_window_max_min([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [(3, -1), (3, -3), (5, -3), (5, -3), (6, 3), (7, 3)]
    """
    maxs = sliding_window_max(nums, k)
    mins = sliding_window_min(nums, k)
    return list(zip(maxs, mins))


def trap_rain_water(height: List[int]) -> int:
    """
    接雨水问题
    
    使用单调栈计算能接多少雨水
    
    Args:
        height: 高度数组
    
    Returns:
        能接的雨水总量
    
    Example:
        >>> trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
        6
    """
    if not height:
        return 0
    
    n = len(height)
    water = 0
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and height[stack[-1]] < height[i]:
            bottom_idx = stack.pop()
            if not stack:
                break
            
            # 计算能接水的宽度
            left_idx = stack[-1]
            width = i - left_idx - 1
            
            # 计算能接水的高度
            min_height = min(height[left_idx], height[i]) - height[bottom_idx]
            
            water += width * min_height
        
        stack.append(i)
    
    return water


def sum_subarray_mins(arr: List[int]) -> int:
    """
    子数组最小值之和
    
    找出所有子数组的最小值之和
    
    Args:
        arr: 输入数组
    
    Returns:
        所有子数组最小值之和（对 10^9 + 7 取模）
    
    Example:
        >>> sum_subarray_mins([3, 1, 2, 4])
        17
    """
    MOD = 10**9 + 7
    n = len(arr)
    
    # 找每个元素左边第一个更小的位置
    left = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    # 找每个元素右边第一个更小的位置
    right = [n] * n
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # 计算贡献
    total = 0
    for i in range(n):
        # arr[i] 作为最小值的子数组数量
        count = (i - left[i]) * (right[i] - i)
        total = (total + arr[i] * count) % MOD
    
    return total


def sum_subarray_maxs(arr: List[int]) -> int:
    """
    子数组最大值之和
    
    找出所有子数组的最大值之和
    
    Args:
        arr: 输入数组
    
    Returns:
        所有子数组最大值之和（对 10^9 + 7 取模）
    
    Example:
        >>> sum_subarray_maxs([3, 1, 2, 4])
        30
    """
    MOD = 10**9 + 7
    n = len(arr)
    
    # 找每个元素左边第一个更大的位置
    left = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    # 找每个元素右边第一次更大的位置
    right = [n] * n
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # 计算贡献
    total = 0
    for i in range(n):
        # arr[i] 作为最大值的子数组数量
        count = (i - left[i]) * (right[i] - i)
        total = (total + arr[i] * count) % MOD
    
    return total


def remove_k_digits(num: str, k: int) -> str:
    """
    删除 k 个数字使结果最小
    
    使用单调栈贪心删除
    
    Args:
        num: 数字字符串
        k: 要删除的数字个数
    
    Returns:
        删除后的最小数字字符串（去除前导零）
    
    Example:
        >>> remove_k_digits("1432219", 3)
        '1219'
        >>> remove_k_digits("10200", 1)
        '200'
    """
    if k >= len(num):
        return "0"
    
    stack = []
    
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    
    # 如果还有剩余的 k，从末尾删除
    while k > 0:
        stack.pop()
        k -= 1
    
    # 构建结果并去除前导零
    result = ''.join(stack).lstrip('0')
    return result if result else "0"


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    每日温度
    
    找出每天需要等多少天才能有更高的温度
    
    Args:
        temperatures: 每日温度列表
    
    Returns:
        等待天数列表，如果不存在更热的天则为 0
    
    Example:
        >>> daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
        [1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    
    return result


def find_unsorted_subarray(nums: List[int]) -> Tuple[int, int]:
    """
    找出需要排序的最短子数组
    
    找出一个最短的连续子数组，如果将这个子数组排序，整个数组就会变得有序
    
    Args:
        nums: 输入数组
    
    Returns:
        (左边界, 右边界)，如果数组已排序则返回 (0, 0)
    
    Example:
        >>> find_unsorted_subarray([2, 6, 4, 8, 10, 9, 15])
        (1, 5)
    """
    n = len(nums)
    if n <= 1:
        return (0, 0)
    
    # 找左边界：从左到右找最后一个不满足单调递增的位置
    max_seen = float('-inf')
    right = 0
    for i in range(n):
        max_seen = max(max_seen, nums[i])
        if nums[i] < max_seen:
            right = i
    
    # 找右边界：从右到左找最后一个不满足单调递减的位置
    min_seen = float('inf')
    left = n - 1
    for i in range(n - 1, -1, -1):
        min_seen = min(min_seen, nums[i])
        if nums[i] > min_seen:
            left = i
    
    if left >= right:
        return (0, 0)
    
    return (left, right)


def validate_parentheses_with_star(s: str) -> bool:
    """
    验证带有通配符的括号字符串
    
    '*' 可以当作 '(' 或 ')' 或空字符串
    
    Args:
        s: 包含 '(', ')', '*' 的字符串
    
    Returns:
        是否可以构成有效的括号字符串
    
    Example:
        >>> validate_parentheses_with_star("()")
        True
        >>> validate_parentheses_with_star("(*)")
        True
        >>> validate_parentheses_with_star("(*))")
        True
    """
    # 使用两个单调栈记录 '(' 和 '*' 的位置
    open_stack = []
    star_stack = []
    
    for i, ch in enumerate(s):
        if ch == '(':
            open_stack.append(i)
        elif ch == '*':
            star_stack.append(i)
        else:  # ')'
            if open_stack:
                open_stack.pop()
            elif star_stack:
                star_stack.pop()
            else:
                return False
    
    # 处理剩余的 '('
    while open_stack:
        if not star_stack:
            return False
        # '*' 必须在 '(' 之后才能匹配
        if open_stack[-1] > star_stack[-1]:
            return False
        open_stack.pop()
        star_stack.pop()
    
    return True


# 导出所有公共 API
__all__ = [
    # 类
    'MonotonicStack',
    'MonotonicQueue',
    'MonotonicStackResult',
    # 单调栈函数
    'next_greater_element',
    'next_greater_element_index',
    'next_smaller_element',
    'prev_greater_element',
    'prev_smaller_element',
    'compute_all_monotonic_relations',
    # 经典应用
    'largest_rectangle_in_histogram',
    'maximal_rectangle',
    'sliding_window_max',
    'sliding_window_min',
    'sliding_window_max_min',
    'trap_rain_water',
    'sum_subarray_mins',
    'sum_subarray_maxs',
    'remove_k_digits',
    'daily_temperatures',
    'find_unsorted_subarray',
    'validate_parentheses_with_star',
]