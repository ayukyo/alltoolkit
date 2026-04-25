"""
单调栈和单调队列工具模块使用示例

本示例展示如何使用 monotonic_utils 模块解决实际问题
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monotonic_utils.mod import (
    MonotonicStack,
    MonotonicQueue,
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


def example_next_greater_element():
    """示例：下一个更大元素"""
    print("=" * 50)
    print("示例 1: 下一个更大元素")
    print("=" * 50)
    
    nums = [4, 5, 2, 10, 8]
    print(f"输入数组: {nums}")
    
    result = next_greater_element(nums)
    print(f"每个元素右边第一个更大的元素: {result}")
    # 解释: 4->5, 5->10, 2->10, 8->无
    
    indices = next_greater_element_index(nums)
    print(f"对应索引: {indices}")
    print()


def example_daily_temperatures():
    """示例：每日温度"""
    print("=" * 50)
    print("示例 2: 每日温度 - 需要等几天才能等到更热的天")
    print("=" * 50)
    
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"每日温度: {temperatures}")
    
    days = daily_temperatures(temperatures)
    print(f"等待天数: {days}")
    # 解释: 73度等1天到74度，74度等1天到75度，75度等4天到76度...
    print()


def example_sliding_window():
    """示例：滑动窗口最大/最小值"""
    print("=" * 50)
    print("示例 3: 滑动窗口最大值/最小值")
    print("=" * 50)
    
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"输入数组: {nums}")
    print(f"窗口大小: {k}")
    
    max_values = sliding_window_max(nums, k)
    print(f"每个窗口的最大值: {max_values}")
    
    min_values = sliding_window_min(nums, k)
    print(f"每个窗口的最小值: {min_values}")
    
    both = sliding_window_max_min(nums, k)
    print(f"最大值和最小值: {both}")
    print()


def example_largest_rectangle():
    """示例：柱状图最大矩形"""
    print("=" * 50)
    print("示例 4: 柱状图中最大矩形面积")
    print("=" * 50)
    
    heights = [2, 1, 5, 6, 2, 3]
    print(f"柱子高度: {heights}")
    print("柱状图:")
    for i, h in enumerate(heights):
        print(f"  柱{i}: {'█' * h} ({h})")
    
    area = largest_rectangle_in_histogram(heights)
    print(f"\n最大矩形面积: {area}")
    # 解释: 以高度5计算，宽度2（柱2和柱3），面积=5*2=10
    print()


def example_maximal_rectangle():
    """示例：最大矩形"""
    print("=" * 50)
    print("示例 5: 0-1 矩阵中的最大矩形")
    print("=" * 50)
    
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"]
    ]
    
    print("矩阵:")
    for row in matrix:
        print(f"  {' '.join(row)}")
    
    area = maximal_rectangle(matrix)
    print(f"\n最大矩形面积: {area}")
    # 解释: 第2-3行的第2-4列构成3*2=6的矩形
    print()


def example_trap_rain_water():
    """示例：接雨水"""
    print("=" * 50)
    print("示例 6: 接雨水问题")
    print("=" * 50)
    
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"高度数组: {height}")
    print("示意图:")
    max_h = max(height)
    for h in range(max_h, 0, -1):
        line = ""
        for x in height:
            if x >= h:
                line += "█ "
            else:
                line += "  "
        print(f"  {h}: {line}")
    
    water = trap_rain_water(height)
    print(f"\n能接的雨水总量: {water}")
    print()


def example_remove_k_digits():
    """示例：删除 k 个数字使结果最小"""
    print("=" * 50)
    print("示例 7: 删除 K 个数字使结果最小")
    print("=" * 50)
    
    test_cases = [
        ("1432219", 3),
        ("10200", 1),
        ("10", 2),
        ("123456789", 3),
    ]
    
    for num, k in test_cases:
        result = remove_k_digits(num, k)
        print(f"  {num} 删除 {k} 个数字 -> {result}")
    print()


def example_monotonic_stack():
    """示例：单调栈类使用"""
    print("=" * 50)
    print("示例 8: 单调栈类操作")
    print("=" * 50)
    
    # 创建单调递增栈
    stack = MonotonicStack(increasing=True)
    print("创建单调递增栈（从小到大）")
    
    elements = [5, 3, 7, 2, 8]
    print(f"依次入栈: {elements}")
    
    for elem in elements:
        popped = stack.push(elem)
        if popped:
            print(f"  入栈 {elem}，弹出 {[p[0] for p in popped]}")
        else:
            print(f"  入栈 {elem}，无弹出")
        print(f"    当前栈: {stack.to_list()}")
    
    print(f"\n栈大小: {stack.size}")
    print(f"栈顶元素: {stack.top}")
    print()


def example_monotonic_queue():
    """示例：单调队列类使用"""
    print("=" * 50)
    print("示例 9: 单调队列类操作")
    print("=" * 50)
    
    # 创建单调递减队列（用于求最大值）
    mq = MonotonicQueue(increasing=False)
    print("创建单调递减队列（用于滑动窗口最大值）")
    
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"输入数组: {nums}")
    print(f"窗口大小: {k}\n")
    
    max_values = []
    for i, num in enumerate(nums):
        mq.push(num, i)
        # 移除过期的元素（超出窗口）
        mq.pop_expired(i - k + 1)
        
        if i >= k - 1:
            max_values.append(mq.front)
            print(f"窗口 [{i-k+1}, {i}]: {nums[i-k+1:i+1]}, 最大值: {mq.front}")
    
    print(f"\n滑动窗口最大值: {max_values}")
    print()


def example_all_relations():
    """示例：计算所有单调关系"""
    print("=" * 50)
    print("示例 10: 计算所有单调关系")
    print("=" * 50)
    
    nums = [3, 1, 4, 2]
    print(f"输入数组: {nums}")
    
    result = compute_all_monotonic_relations(nums)
    
    print("\n下一个更大元素的索引:")
    for i, idx in enumerate(result.next_greater):
        if idx != -1:
            print(f"  nums[{i}]={nums[i]} -> nums[{idx}]={nums[idx]}")
        else:
            print(f"  nums[{i}]={nums[i]} -> 无")
    
    print("\n下一个更小元素的索引:")
    for i, idx in enumerate(result.next_smaller):
        if idx != -1:
            print(f"  nums[{i}]={nums[i]} -> nums[{idx}]={nums[idx]}")
        else:
            print(f"  nums[{i}]={nums[i]} -> 无")
    
    print()


def example_stock_price():
    """示例：股票价格分析"""
    print("=" * 50)
    print("示例 11: 股票价格分析")
    print("=" * 50)
    
    prices = [100, 80, 60, 70, 60, 75, 85]
    print(f"股票价格: {prices}")
    
    # 找下一个更高的价格
    next_higher = next_greater_element(prices)
    print(f"\n下一个更高的价格:")
    for i, price in enumerate(prices):
        if next_higher[i] != -1:
            print(f"  第{i}天价格{price} -> 后续最高{next_higher[i]}")
        else:
            print(f"  第{i}天价格{price} -> 后续无更高价格")
    
    # 找上一个更高的价格
    prev_higher = prev_greater_element(prices)
    print(f"\n上一个更高的价格:")
    for i, price in enumerate(prices):
        if prev_higher[i] != -1:
            print(f"  第{i}天价格{price} -> 前一日最高{prev_higher[i]}")
        else:
            print(f"  第{i}天价格{price} -> 前面无更高价格")
    print()


def example_validate_parentheses():
    """示例：验证带通配符的括号"""
    print("=" * 50)
    print("示例 12: 验证带通配符的括号字符串")
    print("=" * 50)
    
    test_cases = [
        ("()", "标准括号"),
        ("(*)", "通配符作为空字符串"),
        ("(*))", "通配符作为左括号"),
        ("(", "不匹配"),
        ("(*(", "无法匹配"),
        ("(**)", "多个通配符"),
    ]
    
    for s, desc in test_cases:
        result = validate_parentheses_with_star(s)
        status = "✓ 有效" if result else "✗ 无效"
        print(f"  '{s}' ({desc}): {status}")
    print()


def example_sum_subarray():
    """示例：子数组最值之和"""
    print("=" * 50)
    print("示例 13: 子数组最小值/最大值之和")
    print("=" * 50)
    
    arr = [3, 1, 2, 4]
    print(f"数组: {arr}")
    
    # 列出所有子数组
    print("\n所有子数组:")
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            subarr = arr[i:j+1]
            print(f"  {subarr}: min={min(subarr)}, max={max(subarr)}")
    
    min_sum = sum_subarray_mins(arr)
    max_sum = sum_subarray_maxs(arr)
    
    print(f"\n所有子数组最小值之和: {min_sum}")
    print(f"所有子数组最大值之和: {max_sum}")
    print()


def example_unsorted_subarray():
    """示例：找出需要排序的子数组"""
    print("=" * 50)
    print("示例 14: 找出需要排序的最短子数组")
    print("=" * 50)
    
    nums = [2, 6, 4, 8, 10, 9, 15]
    print(f"数组: {nums}")
    
    left, right = find_unsorted_subarray(nums)
    
    if left == right == 0:
        print("数组已经有序")
    else:
        print(f"需要排序的子数组: 索引 [{left}, {right}]")
        print(f"子数组内容: {nums[left:right+1]}")
        print(f"排序后: {sorted(nums[left:right+1])}")
        print(f"完整排序后: {sorted(nums)}")
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  单调栈和单调队列工具模块 - 使用示例".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    example_next_greater_element()
    example_daily_temperatures()
    example_sliding_window()
    example_largest_rectangle()
    example_maximal_rectangle()
    example_trap_rain_water()
    example_remove_k_digits()
    example_monotonic_stack()
    example_monotonic_queue()
    example_all_relations()
    example_stock_price()
    example_validate_parentheses()
    example_sum_subarray()
    example_unsorted_subarray()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()