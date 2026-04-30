#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fibonacci Heap 基本使用示例

演示斐波那契堆的基本功能和使用方法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    FibonacciHeap, MaxFibonacciHeap,
    FibonacciHeapUtils,
    create_min_heap, create_max_heap,
    heap_sort, top_k
)


def example_basic_operations():
    """基本操作示例"""
    print("=" * 60)
    print("基本操作示例")
    print("=" * 60)
    
    # 创建最小堆
    heap = FibonacciHeap[str]()
    
    # 插入元素
    print("\n插入元素:")
    heap.insert(5, "task_low")
    heap.insert(1, "task_high")
    heap.insert(3, "task_medium")
    heap.insert(2, "task_medium_low")
    heap.insert(10, "task_very_low")
    
    print(f"  堆大小: {len(heap)}")
    print(f"  最小值: {heap.peek()} (key: {heap.peek_key()})")
    
    # 按优先级提取
    print("\n按优先级提取任务:")
    while not heap.is_empty():
        key, task = heap.extract_min_with_key()
        print(f"  优先级 {key}: {task}")


def example_max_heap():
    """最大堆示例"""
    print("\n" + "=" * 60)
    print("最大堆示例")
    print("=" * 60)
    
    heap = MaxFibonacciHeap[str]()
    
    # 按成绩排序
    heap.insert(85, "学生A")
    heap.insert(92, "学生B")
    heap.insert(78, "学生C")
    heap.insert(95, "学生D")
    heap.insert(88, "学生E")
    
    print("\n成绩排名（从高到低）:")
    while not heap.is_empty():
        score, student = heap.extract_max_with_key()
        print(f"  {student}: {score}分")


def example_decrease_key():
    """decrease_key 示例"""
    print("\n" + "=" * 60)
    print("decrease_key 示例 - 任务优先级调整")
    print("=" * 60)
    
    heap = FibonacciHeap[str]()
    
    # 创建任务
    task1 = heap.insert(10, "任务1-低优先级")
    task2 = heap.insert(5, "任务2-中优先级")
    task3 = heap.insert(3, "任务3-高优先级")
    
    print("\n初始状态:")
    print(f"  最高优先级任务: {heap.peek()}")
    
    # 将任务1的优先级提高（键值减小）
    print("\n提高任务1的优先级 (10 -> 1):")
    heap.decrease_key(task1, 1)
    print(f"  最高优先级任务: {heap.peek()}")
    
    # 提取所有任务
    print("\n最终执行顺序:")
    while not heap.is_empty():
        key, task = heap.extract_min_with_key()
        print(f"  优先级 {key}: {task}")


def example_merge_heaps():
    """合并堆示例"""
    print("\n" + "=" * 60)
    print("合并堆示例")
    print("=" * 60)
    
    # 两个不同的任务队列
    queue1 = FibonacciHeap[str]()
    queue1.insert(5, "队列1-任务A")
    queue1.insert(3, "队列1-任务B")
    
    queue2 = FibonacciHeap[str]()
    queue2.insert(4, "队列2-任务C")
    queue2.insert(1, "队列2-任务D")
    queue2.insert(2, "队列2-任务E")
    
    print("\n队列1大小:", len(queue1))
    print("队列2大小:", len(queue2))
    
    # 合并队列
    queue1.merge(queue2)
    
    print("\n合并后:")
    print(f"  队列1大小: {len(queue1)}")
    print(f"  队列2大小: {len(queue2)} (已清空)")
    
    print("\n合并后按优先级执行:")
    while not queue1.is_empty():
        key, task = queue1.extract_min_with_key()
        print(f"  优先级 {key}: {task}")


def example_heap_sort():
    """堆排序示例"""
    print("\n" + "=" * 60)
    print("堆排序示例")
    print("=" * 60)
    
    numbers = [64, 34, 25, 12, 22, 11, 90, 45, 33, 21]
    
    print(f"\n原始数组: {numbers}")
    
    ascending = heap_sort(numbers)
    print(f"升序排序: {ascending}")
    
    descending = heap_sort(numbers, reverse=True)
    print(f"降序排序: {descending}")


def example_top_k():
    """Top K 示例"""
    print("\n" + "=" * 60)
    print("Top K 示例")
    print("=" * 60)
    
    scores = [78, 92, 85, 95, 88, 76, 90, 82, 91, 87]
    
    print(f"\n学生成绩: {scores}")
    
    top_3 = top_k(scores, k=3, largest=True)
    print(f"成绩最高的3名学生: {top_3}")
    
    bottom_3 = top_k(scores, k=3, largest=False)
    print(f"成绩最低的3名学生: {bottom_3}")
    
    # 使用自定义键函数
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    print(f"\n单词列表: {words}")
    
    longest_2 = top_k(words, k=2, key_func=len, largest=True)
    print(f"最长的2个单词: {longest_2}")
    
    shortest_2 = top_k(words, k=2, key_func=len, largest=False)
    print(f"最短的2个单词: {shortest_2}")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 60)
    print("序列化示例")
    print("=" * 60)
    
    heap = FibonacciHeap[str]()
    heap.insert(1, "重要")
    heap.insert(5, "普通")
    heap.insert(3, "次要")
    
    # 转为字典
    data = heap.to_dict()
    print(f"\n字典表示: {data}")
    
    # 转为JSON
    json_str = heap.to_json()
    print(f"\nJSON表示: {json_str}")
    
    # 从JSON恢复
    restored = FibonacciHeap.from_json(json_str)
    print(f"\n恢复后的堆: {restored}")
    print(f"恢复后的元素: {restored.to_list()}")


def example_dijkstra_simulation():
    """模拟Dijkstra算法的使用"""
    print("\n" + "=" * 60)
    print("Dijkstra算法模拟")
    print("=" * 60)
    
    # 简化的图结构
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8},
        'D': {'B': 5, 'C': 8}
    }
    
    source = 'A'
    
    # 初始化距离
    dist = {v: float('inf') for v in graph}
    dist[source] = 0
    
    # 创建斐波那契堆
    heap = FibonacciHeap[float]()
    nodes = {}
    
    for v in graph:
        nodes[v] = heap.insert(dist[v], v)
    
    print(f"\n从节点 {source} 开始寻找最短路径:")
    
    while not heap.is_empty():
        d, u = heap.extract_min_with_key()
        
        print(f"\n处理节点 {u} (距离: {d})")
        
        for v, weight in graph[u].items():
            new_dist = d + weight
            if new_dist < dist[v]:
                print(f"  发现更短路径到 {v}: {dist[v]} -> {new_dist}")
                dist[v] = new_dist
                heap.decrease_key(nodes[v], new_dist)
    
    print(f"\n最终距离:")
    for v, d in sorted(dist.items()):
        print(f"  {source} -> {v}: {d}")


def example_task_scheduler():
    """任务调度器示例"""
    print("\n" + "=" * 60)
    print("任务调度器示例")
    print("=" * 60)
    
    class TaskScheduler:
        def __init__(self):
            self.heap = FibonacciHeap[str]()
            self.tasks = {}
        
        def add_task(self, priority, task_id):
            node = self.heap.insert(priority, task_id)
            self.tasks[task_id] = node
            print(f"  添加任务: {task_id} (优先级: {priority})")
        
        def get_next_task(self):
            if self.heap.is_empty():
                return None
            key, task = self.heap.extract_min_with_key()
            del self.tasks[task]
            return task, key
        
        def update_priority(self, task_id, new_priority):
            if task_id in self.tasks:
                old_key = self.tasks[task_id].key
                self.heap.decrease_key(self.tasks[task_id], new_priority)
                print(f"  更新优先级: {task_id} ({old_key} -> {new_priority})")
        
        def cancel_task(self, task_id):
            if task_id in self.tasks:
                self.heap.delete(self.tasks[task_id])
                del self.tasks[task_id]
                print(f"  取消任务: {task_id}")
        
        def show_status(self):
            print(f"  当前任务数: {len(self.heap)}")
            if not self.heap.is_empty():
                print(f"  最高优先级任务: {self.heap.peek()}")
    
    scheduler = TaskScheduler()
    
    print("\n添加任务:")
    scheduler.add_task(5, "写文档")
    scheduler.add_task(3, "修复bug")
    scheduler.add_task(8, "开会")
    scheduler.add_task(1, "紧急修复")
    
    print("\n当前状态:")
    scheduler.show_status()
    
    print("\n更新优先级:")
    scheduler.update_priority("开会", 2)  # 会议变得更重要
    
    print("\n取消任务:")
    scheduler.cancel_task("写文档")
    
    print("\n执行任务（按优先级）:")
    while True:
        result = scheduler.get_next_task()
        if result is None:
            break
        task, priority = result
        print(f"  执行: {task} (优先级: {priority})")


def main():
    """运行所有示例"""
    example_basic_operations()
    example_max_heap()
    example_decrease_key()
    example_merge_heaps()
    example_heap_sort()
    example_top_k()
    example_serialization()
    example_dijkstra_simulation()
    example_task_scheduler()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()