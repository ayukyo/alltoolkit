"""
堆工具集示例代码
================

展示 MinHeap、MaxHeap、PriorityQueue 等的使用方法。

运行方式：
    cd Python/heap_utils
    python examples/basic_usage.py
"""

import os
import sys

# 添加父目录到路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# 直接导入 mod 模块
import mod
MinHeap = mod.MinHeap
MaxHeap = mod.MaxHeap
MinMaxHeap = mod.MinMaxHeap
PriorityQueue = mod.PriorityQueue
heap_sort = mod.heap_sort
nth_smallest = mod.nth_smallest
nth_largest = mod.nth_largest
k_smallest = mod.k_smallest
k_largest = mod.k_largest
merge_sorted_lists = mod.merge_sorted_lists
median_of_data = mod.median_of_data


def demo_min_heap():
    """最小堆演示"""
    print("=" * 50)
    print("最小堆演示 (MinHeap)")
    print("=" * 50)
    
    heap = MinHeap[int]()
    
    # 入队
    for num in [3, 1, 4, 1, 5, 9, 2, 6]:
        heap.push(num)
        print(f"  入队 {num}，堆顶: {heap.peek()}")
    
    print(f"\n  当前堆大小: {len(heap)}")
    
    # 出队
    print("\n  出队顺序:")
    while heap:
        print(f"    {heap.pop()}")


def demo_max_heap():
    """最大堆演示"""
    print("\n" + "=" * 50)
    print("最大堆演示 (MaxHeap)")
    print("=" * 50)
    
    heap = MaxHeap[str]()
    
    # 入队
    words = ["cherry", "apple", "banana", "date", "elderberry"]
    for word in words:
        heap.push(word)
    
    print(f"  入队: {words}")
    print(f"  堆顶（最大）: {heap.peek()}")
    
    # 出队
    print("\n  出队顺序（字典序降序）:")
    while heap:
        print(f"    {heap.pop()}")


def demo_priority_queue():
    """优先队列演示"""
    print("\n" + "=" * 50)
    print("优先队列演示 (PriorityQueue)")
    print("=" * 50)
    
    pq = PriorityQueue[str]()
    
    tasks = [
        ("写代码", 3),
        ("修复Bug", 1),
        ("写文档", 2),
        ("紧急修复", 0),
        ("代码审查", 4),
    ]
    
    print("  入队任务（优先级越低越优先）:")
    for task, priority in tasks:
        pq.push(task, priority=priority)
        print(f"    优先级 {priority}: {task}")
    
    print("\n  出队顺序:")
    while pq:
        task = pq.pop()
        print(f"    {task}")


def demo_min_max_heap():
    """双端堆演示"""
    print("\n" + "=" * 50)
    print("双端堆演示 (MinMaxHeap)")
    print("=" * 50)
    
    heap = MinMaxHeap[int]()
    
    for num in [3, 1, 4, 1, 5, 9, 2, 6]:
        heap.push(num)
    
    print(f"  当前最小值: {heap.get_min()}")
    print(f"  当前最大值: {heap.get_max()}")
    
    print("\n  弹出最小元素:")
    for _ in range(3):
        print(f"    {heap.pop_min()}")
    
    print(f"\n  剩余最小值: {heap.get_min()}")
    print(f"  剩余最大值: {heap.get_max()}")


def demo_heap_sort():
    """堆排序演示"""
    print("\n" + "=" * 50)
    print("堆排序演示 (heap_sort)")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    
    print(f"  原始数据: {data}")
    print(f"  升序排序: {heap_sort(data)}")
    print(f"  降序排序: {heap_sort(data, reverse=True)}")
    
    # 带键函数排序
    words = ["apple", "pie", "a", "longword", "hi"]
    print(f"\n  按长度排序: {heap_sort(words, key=len)}")


def demo_k_selection():
    """第k大/小元素演示"""
    print("\n" + "=" * 50)
    print("第K大/小元素演示")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"  数据: {data}")
    
    print(f"\n  第1小: {nth_smallest(data, 1)}")
    print(f"  第3小: {nth_smallest(data, 3)}")
    print(f"  第5小: {nth_smallest(data, 5)}")
    
    print(f"\n  第1大: {nth_largest(data, 1)}")
    print(f"  第3大: {nth_largest(data, 3)}")
    print(f"  第5大: {nth_largest(data, 5)}")
    
    print(f"\n  最小3个: {k_smallest(data, 3)}")
    print(f"  最大3个: {k_largest(data, 3)}")


def demo_merge_lists():
    """合并有序列表演示"""
    print("\n" + "=" * 50)
    print("合并有序列表演示 (merge_sorted_lists)")
    print("=" * 50)
    
    list1 = [1, 3, 5, 7]
    list2 = [2, 4, 6, 8]
    list3 = [0, 9, 10]
    
    print(f"  列表1: {list1}")
    print(f"  列表2: {list2}")
    print(f"  列表3: {list3}")
    print(f"\n  合并结果: {merge_sorted_lists(list1, list2, list3)}")


def demo_median():
    """中位数演示"""
    print("\n" + "=" * 50)
    print("中位数计算演示 (median_of_data)")
    print("=" * 50)
    
    data1 = [1, 2, 3, 4, 5]
    data2 = [1, 2, 3, 4, 5, 6]
    
    print(f"  数据: {data1}")
    print(f"  中位数: {median_of_data(data1)}")
    
    print(f"\n  数据: {data2}")
    print(f"  中位数: {median_of_data(data2)}")


def demo_custom_objects():
    """自定义对象演示"""
    print("\n" + "=" * 50)
    print("自定义对象演示")
    print("=" * 50)
    
    # 定义任务类
    class Task:
        def __init__(self, name: str, priority: int):
            self.name = name
            self.priority = priority
        
        def __repr__(self):
            return f"Task({self.name}, p={self.priority})"
    
    tasks = [
        Task("写代码", 3),
        Task("修复Bug", 1),
        Task("写文档", 2),
        Task("开会", 5),
    ]
    
    # 使用键函数排序
    heap = MinHeap(tasks, key=lambda t: t.priority)
    
    print("  任务执行顺序（优先级升序）:")
    while heap:
        task = heap.pop()
        print(f"    {task.name} (优先级: {task.priority})")


def main():
    """运行所有演示"""
    print("\n堆工具集示例演示\n")
    
    demo_min_heap()
    demo_max_heap()
    demo_priority_queue()
    demo_min_max_heap()
    demo_heap_sort()
    demo_k_selection()
    demo_merge_lists()
    demo_median()
    demo_custom_objects()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()