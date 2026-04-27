"""
单调栈和单调队列工具模块测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    MonotonicStack,
    MonotonicQueue,
    MonotonicStackResult,
    next_greater_element,
    next_greater_element_index,
    next_smaller_element,
    prev_greater_element,
    prev_smaller_element,
    compute_all_monotonic_relations,
    largest_rectangle_in_histogram,
    maximal_rectangle,
    sliding_window_max,
    sliding_window_min,
    sliding_window_max_min,
    trap_rain_water,
    sum_subarray_mins,
    sum_subarray_maxs,
    remove_k_digits,
    daily_temperatures,
    find_unsorted_subarray,
    validate_parentheses_with_star,
)


def test_monotonic_stack_basic():
    """测试单调栈基本操作"""
    print("测试单调栈基本操作...")
    
    # 测试单调递增栈（栈底到栈顶递增，即弹出 >= 当前值的元素）
    stack = MonotonicStack(increasing=True)
    assert stack.is_empty == True
    assert stack.size == 0
    
    stack.push(3)  # 栈: [3]
    stack.push(1)  # 弹出 3 (>=1)，栈: [1]
    stack.push(4)  # 栈: [1, 4]
    stack.push(2)  # 弹出 4 (>=2)，栈: [1, 2]
    
    assert stack.size == 2
    assert stack.to_list() == [1, 2]
    
    # 测试单调递减栈（栈底到栈顶递减，即弹出 <= 当前值的元素）
    stack2 = MonotonicStack(increasing=False)
    popped = stack2.push(5)
    assert len(popped) == 0
    
    popped = stack2.push(3)
    assert len(popped) == 0  # 3 < 5，不弹出 (<= 检查)
    
    popped = stack2.push(7)
    assert len(popped) == 2  # 弹出 5 和 3 (都 <= 7)
    assert stack2.size == 1
    
    print("  ✓ 单调栈基本操作测试通过")


def test_monotonic_stack_operations():
    """测试单调栈高级操作"""
    print("测试单调栈高级操作...")
    
    stack = MonotonicStack(increasing=True)
    
    # 测试带索引的入栈
    popped = stack.push(5, 0)
    assert popped == []  # 空栈，无弹出
    
    popped = stack.push(3, 1)
    # 单调递增栈：5 >= 3，弹出 5
    assert len(popped) == 1
    assert popped[0] == (5, 0)
    
    popped = stack.push(4, 2)
    # 栈: [3]，push(4)：3 < 4，不弹出
    assert len(popped) == 0
    
    popped = stack.push(2, 3)
    # 栈: [3, 4]，push(2)：4 >= 2 弹出，3 >= 2 弹出
    assert len(popped) == 2
    assert popped == [(4, 2), (3, 1)]
    
    # 测试出栈
    result = stack.pop()
    assert result == (2, 3)
    
    # 测试清空
    stack.clear()
    assert stack.is_empty == True
    
    print("  ✓ 单调栈高级操作测试通过")


def test_next_greater_element():
    """测试下一个更大元素"""
    print("测试下一个更大元素...")
    
    # 测试基本功能
    result = next_greater_element([2, 1, 2, 4, 3])
    assert result == [4, 2, 4, -1, -1], f"期望 [4, 2, 4, -1, -1]，得到 {result}"
    
    # 测试空数组
    assert next_greater_element([]) == []
    
    # 测试单元素
    assert next_greater_element([5]) == [-1]
    
    # 测试递减数组
    assert next_greater_element([5, 4, 3, 2, 1]) == [-1, -1, -1, -1, -1]
    
    # 测试递增数组
    assert next_greater_element([1, 2, 3, 4, 5]) == [2, 3, 4, 5, -1]
    
    # 测试索引版本
    result_idx = next_greater_element_index([2, 1, 2, 4, 3])
    assert result_idx == [3, 2, 3, -1, -1], f"期望 [3, 2, 3, -1, -1]，得到 {result_idx}"
    
    print("  ✓ 下一个更大元素测试通过")


def test_next_smaller_element():
    """测试下一个更小元素"""
    print("测试下一个更小元素...")
    
    result = next_smaller_element([2, 1, 2, 4, 3])
    # 分析: nums[0]=2 -> 1, nums[1]=1 -> 无, nums[2]=2 -> 无(右边3>2), nums[3]=4 -> 3, nums[4]=3 -> 无
    assert result == [1, -1, -1, 3, -1], f"期望 [1, -1, -1, 3, -1]，得到 {result}"
    
    # 测试空数组
    assert next_smaller_element([]) == []
    
    # 测试单元素
    assert next_smaller_element([5]) == [-1]
    
    # 测试递增数组（没有更小元素）
    assert next_smaller_element([1, 2, 3, 4, 5]) == [-1, -1, -1, -1, -1]
    
    # 测试递减数组（有更小元素）
    assert next_smaller_element([5, 4, 3, 2, 1]) == [4, 3, 2, 1, -1]
    
    print("  ✓ 下一个更小元素测试通过")


def test_prev_greater_element():
    """测试上一个更大元素"""
    print("测试上一个更大元素...")
    
    result = prev_greater_element([2, 1, 2, 4, 3])
    assert result == [-1, 2, -1, -1, 4], f"期望 [-1, 2, -1, -1, 4]，得到 {result}"
    
    # 测试空数组
    assert prev_greater_element([]) == []
    
    print("  ✓ 上一个更大元素测试通过")


def test_prev_smaller_element():
    """测试上一个更小元素"""
    print("测试上一个更小元素...")
    
    result = prev_smaller_element([2, 1, 2, 4, 3])
    assert result == [-1, -1, 1, 2, 2], f"期望 [-1, -1, 1, 2, 2]，得到 {result}"
    
    print("  ✓ 上一个更小元素测试通过")


def test_compute_all_monotonic_relations():
    """测试计算所有单调关系"""
    print("测试计算所有单调关系...")
    
    result = compute_all_monotonic_relations([3, 1, 4, 2])
    
    assert result.next_greater == [2, 2, -1, -1], f"next_greater 错误: {result.next_greater}"
    assert result.next_smaller == [1, -1, 3, -1], f"next_smaller 错误: {result.next_smaller}"
    assert result.prev_greater == [-1, 0, -1, 2], f"prev_greater 错误: {result.prev_greater}"
    assert result.prev_smaller == [-1, -1, 1, 1], f"prev_smaller 错误: {result.prev_smaller}"
    
    print("  ✓ 计算所有单调关系测试通过")


def test_largest_rectangle_in_histogram():
    """测试柱状图最大矩形"""
    print("测试柱状图最大矩形...")
    
    # 测试基本功能
    area = largest_rectangle_in_histogram([2, 1, 5, 6, 2, 3])
    assert area == 10, f"期望 10，得到 {area}"
    
    # 测试空数组
    assert largest_rectangle_in_histogram([]) == 0
    
    # 测试单柱
    assert largest_rectangle_in_histogram([5]) == 5
    
    # 测试递增
    assert largest_rectangle_in_histogram([1, 2, 3, 4, 5]) == 9
    
    # 测试递减
    assert largest_rectangle_in_histogram([5, 4, 3, 2, 1]) == 9
    
    # 测试相同高度
    assert largest_rectangle_in_histogram([2, 2, 2, 2]) == 8
    
    print("  ✓ 柱状图最大矩形测试通过")


def test_maximal_rectangle():
    """测试最大矩形"""
    print("测试最大矩形...")
    
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"]
    ]
    area = maximal_rectangle(matrix)
    assert area == 6, f"期望 6，得到 {area}"
    
    # 测试空矩阵
    assert maximal_rectangle([]) == 0
    assert maximal_rectangle([[]]) == 0
    
    # 测试全 0 矩阵
    assert maximal_rectangle([["0", "0"], ["0", "0"]]) == 0
    
    # 测试全 1 矩阵
    assert maximal_rectangle([["1", "1"], ["1", "1"]]) == 4
    
    print("  ✓ 最大矩形测试通过")


def test_monotonic_queue_basic():
    """测试单调队列基本操作"""
    print("测试单调队列基本操作...")
    
    # 测试单调递增队列
    mq = MonotonicQueue(increasing=True)
    assert mq.is_empty == True
    
    mq.push(5)
    mq.push(3)
    mq.push(7)
    
    assert mq.front == 3  # 最小值在前
    assert mq.back == 7
    
    # 测试单调递减队列
    mq2 = MonotonicQueue(increasing=False)
    mq2.push(5)
    mq2.push(3)
    mq2.push(7)
    
    assert mq2.front == 7  # 最大值在前
    
    print("  ✓ 单调队列基本操作测试通过")


def test_monotonic_queue_sliding_window():
    """测试单调队列滑动窗口功能"""
    print("测试单调队列滑动窗口功能...")
    
    mq = MonotonicQueue(increasing=False)  # 递减队列，用于求最大值
    
    # 模拟滑动窗口
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    
    for i, num in enumerate(nums):
        mq.push(num, i)
        mq.pop_expired(i - k + 1)
        
        if i >= k - 1:
            # 验证窗口最大值
            expected_max = max(nums[i - k + 1:i + 1])
            assert mq.front == expected_max, f"窗口 [{i-k+1}, {i}] 最大值错误: 期望 {expected_max}，得到 {mq.front}"
    
    print("  ✓ 单调队列滑动窗口功能测试通过")


def test_sliding_window_max():
    """测试滑动窗口最大值"""
    print("测试滑动窗口最大值...")
    
    result = sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    assert result == [3, 3, 5, 5, 6, 7], f"期望 [3, 3, 5, 5, 6, 7]，得到 {result}"
    
    # 测试 k = 1
    assert sliding_window_max([1, 2, 3], 1) == [1, 2, 3]
    
    # 测试 k > len(nums)
    assert sliding_window_max([1, 2, 3], 5) == [3]
    
    # 测试空数组
    assert sliding_window_max([], 3) == []
    
    print("  ✓ 滑动窗口最大值测试通过")


def test_sliding_window_min():
    """测试滑动窗口最小值"""
    print("测试滑动窗口最小值...")
    
    result = sliding_window_min([1, 3, -1, -3, 5, 3, 6, 7], 3)
    assert result == [-1, -3, -3, -3, 3, 3], f"期望 [-1, -3, -3, -3, 3, 3]，得到 {result}"
    
    print("  ✓ 滑动窗口最小值测试通过")


def test_sliding_window_max_min():
    """测试滑动窗口最大最小值"""
    print("测试滑动窗口最大最小值...")
    
    result = sliding_window_max_min([1, 3, -1, -3, 5, 3, 6, 7], 3)
    expected = [(3, -1), (3, -3), (5, -3), (5, -3), (6, 3), (7, 3)]
    assert result == expected, f"期望 {expected}，得到 {result}"
    
    print("  ✓ 滑动窗口最大最小值测试通过")


def test_trap_rain_water():
    """测试接雨水问题"""
    print("测试接雨水问题...")
    
    water = trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    assert water == 6, f"期望 6，得到 {water}"
    
    # 测试无接水情况
    assert trap_rain_water([1, 2, 3, 4, 5]) == 0
    
    # 测试空数组
    assert trap_rain_water([]) == 0
    
    # 测试单柱
    assert trap_rain_water([5]) == 0
    
    print("  ✓ 接雨水问题测试通过")


def test_sum_subarray_mins():
    """测试子数组最小值之和"""
    print("测试子数组最小值之和...")
    
    result = sum_subarray_mins([3, 1, 2, 4])
    # 子数组: [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]
    # 最小值:  3,   1,   2,   4,    1,     1,     2,      1,       1,        1
    # 总和 = 3+1+2+4+1+1+2+1+1+1 = 17
    assert result == 17, f"期望 17，得到 {result}"
    
    # 测试单元素
    assert sum_subarray_mins([5]) == 5
    
    print("  ✓ 子数组最小值之和测试通过")


def test_sum_subarray_maxs():
    """测试子数组最大值之和"""
    print("测试子数组最大值之和...")
    
    result = sum_subarray_maxs([3, 1, 2, 4])
    # 子数组: [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]
    # 最大值:  3,   1,   2,   4,    3,     2,     4,      3,       4,        4
    # 总和 = 3+1+2+4+3+2+4+3+4+4 = 30
    assert result == 30, f"期望 30，得到 {result}"
    
    print("  ✓ 子数组最大值之和测试通过")


def test_remove_k_digits():
    """测试删除 k 个数字"""
    print("测试删除 k 个数字...")
    
    result = remove_k_digits("1432219", 3)
    assert result == "1219", f"期望 '1219'，得到 '{result}'"
    
    # 测试删除所有数字
    assert remove_k_digits("12345", 5) == "0"
    
    # 测试前导零
    result = remove_k_digits("10200", 1)
    assert result == "200", f"期望 '200'，得到 '{result}'"
    
    # 测试删除末尾数字
    result = remove_k_digits("10", 2)
    assert result == "0", f"期望 '0'，得到 '{result}'"
    
    print("  ✓ 删除 k 个数字测试通过")


def test_daily_temperatures():
    """测试每日温度"""
    print("测试每日温度...")
    
    result = daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
    expected = [1, 1, 4, 2, 1, 1, 0, 0]
    assert result == expected, f"期望 {expected}，得到 {result}"
    
    # 测试递减温度
    assert daily_temperatures([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]
    
    # 测试递增温度
    assert daily_temperatures([1, 2, 3, 4, 5]) == [1, 1, 1, 1, 0]
    
    print("  ✓ 每日温度测试通过")


def test_find_unsorted_subarray():
    """测试找出需要排序的子数组"""
    print("测试找出需要排序的子数组...")
    
    result = find_unsorted_subarray([2, 6, 4, 8, 10, 9, 15])
    assert result == (1, 5), f"期望 (1, 5)，得到 {result}"
    
    # 测试已排序数组
    assert find_unsorted_subarray([1, 2, 3, 4, 5]) == (0, 0)
    
    # 测试单元素
    assert find_unsorted_subarray([1]) == (0, 0)
    
    # 测试空数组
    assert find_unsorted_subarray([]) == (0, 0)
    
    print("  ✓ 找出需要排序的子数组测试通过")


def test_validate_parentheses_with_star():
    """测试验证带有通配符的括号字符串"""
    print("测试验证带有通配符的括号字符串...")
    
    assert validate_parentheses_with_star("()") == True
    assert validate_parentheses_with_star("(*)") == True
    assert validate_parentheses_with_star("(*))") == True
    assert validate_parentheses_with_star(")(") == False
    assert validate_parentheses_with_star("(*(") == False
    assert validate_parentheses_with_star("") == True
    assert validate_parentheses_with_star("*") == True
    assert validate_parentheses_with_star("**") == True
    assert validate_parentheses_with_star("(*") == True
    
    print("  ✓ 验证带有通配符的括号字符串测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空数组测试
    assert next_greater_element([]) == []
    assert next_smaller_element([]) == []
    assert sliding_window_max([], 1) == []
    assert trap_rain_water([]) == 0
    assert largest_rectangle_in_histogram([]) == 0
    
    # 单元素测试
    assert next_greater_element([1]) == [-1]
    assert next_smaller_element([1]) == [-1]
    assert sliding_window_max([1], 1) == [1]
    assert trap_rain_water([1]) == 0
    
    # 负数测试
    assert next_greater_element([-1, -2, -3]) == [-1, -1, -1]
    assert sliding_window_max([-1, -2, -3], 2) == [-1, -2]
    
    print("  ✓ 边界情况测试通过")


def test_performance():
    """测试性能（大数据量）"""
    print("测试性能...")
    import time
    
    # 大数组测试
    n = 10000
    large_arr = list(range(n, 0, -1))  # 递减数组
    
    start = time.time()
    result = next_greater_element(large_arr)
    elapsed = time.time() - start
    assert len(result) == n
    assert all(x == -1 for x in result)  # 递减数组没有更大的元素
    print(f"  next_greater_element({n} 元素): {elapsed:.3f}s")
    
    # 滑动窗口性能
    start = time.time()
    result = sliding_window_max(large_arr, 100)
    elapsed = time.time() - start
    assert len(result) == n - 100 + 1
    print(f"  sliding_window_max({n} 元素, k=100): {elapsed:.3f}s")
    
    # 柱状图最大矩形性能 - 使用全相等高度数组便于验证
    equal_heights = [5] * n
    start = time.time()
    area = largest_rectangle_in_histogram(equal_heights)
    elapsed = time.time() - start
    expected_area = 5 * n  # 全相等高度，最大矩形是整个数组
    assert area == expected_area
    print(f"  largest_rectangle_in_histogram({n} 元素, 全相等高度): {elapsed:.3f}s")
    
    # 接雨水性能测试
    rain_heights = [i % 100 + 1 for i in range(n)]
    start = time.time()
    water = trap_rain_water(rain_heights)
    elapsed = time.time() - start
    assert water >= 0
    print(f"  trap_rain_water({n} 元素): {elapsed:.3f}s")
    
    print("  ✓ 性能测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("单调栈和单调队列工具模块测试")
    print("=" * 60)
    
    test_monotonic_stack_basic()
    test_monotonic_stack_operations()
    test_next_greater_element()
    test_next_smaller_element()
    test_prev_greater_element()
    test_prev_smaller_element()
    test_compute_all_monotonic_relations()
    test_largest_rectangle_in_histogram()
    test_maximal_rectangle()
    test_monotonic_queue_basic()
    test_monotonic_queue_sliding_window()
    test_sliding_window_max()
    test_sliding_window_min()
    test_sliding_window_max_min()
    test_trap_rain_water()
    test_sum_subarray_mins()
    test_sum_subarray_maxs()
    test_remove_k_digits()
    test_daily_temperatures()
    test_find_unsorted_subarray()
    test_validate_parentheses_with_star()
    test_edge_cases()
    test_performance()
    
    print("=" * 60)
    print("所有测试通过！✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()