"""
优先队列基本使用示例

演示 PriorityQueue 的基本操作：
- 推入元素
- 弹出元素
- 最小堆/最大堆模式
- 查看堆顶元素
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import PriorityQueue, create_min_heap, create_max_heap


def basic_usage():
    """基本使用示例"""
    print("=" * 50)
    print("基本优先队列使用（最小堆）")
    print("=" * 50)
    
    pq = create_min_heap()
    
    # 推入任务，优先级值越小越优先
    pq.push("处理紧急 Bug", priority=1)
    pq.push("编写文档", priority=5)
    pq.push("代码审查", priority=3)
    pq.push("回复邮件", priority=4)
    pq.push("修复小问题", priority=2)
    
    print("\n任务队列内容:")
    print(f"  队列大小: {len(pq)}")
    print(f"  下一个任务: {pq.peek()}")
    
    print("\n按优先级执行任务:")
    while pq:
        task = pq.pop()
        print(f"  - {task}")
    
    print()


def max_heap_usage():
    """最大堆使用示例"""
    print("=" * 50)
    print("最大堆优先队列（优先级值越大越优先）")
    print("=" * 50)
    
    pq = create_max_heap()
    
    # 分数排名系统
    players = [
        ("Alice", 95),
        ("Bob", 78),
        ("Charlie", 92),
        ("David", 85),
        ("Eve", 88),
    ]
    
    print("\n玩家分数:")
    for name, score in players:
        pq.push(name, score)
        print(f"  {name}: {score} 分")
    
    print("\n排行榜（从高到低）:")
    rank = 1
    while pq:
        player = pq.pop()
        print(f"  第 {rank} 名: {player}")
        rank += 1
    
    print()


def peek_and_contains():
    """查看堆顶和包含检查示例"""
    print("=" * 50)
    print("查看堆顶和包含检查")
    print("=" * 50)
    
    pq = PriorityQueue[str]()
    pq.push("任务A", 2)
    pq.push("任务B", 1)
    pq.push("任务C", 3)
    
    print(f"\n当前队列大小: {len(pq)}")
    print(f"堆顶元素（不移除）: {pq.peek()}")
    print(f"堆顶优先级: {pq.peek_priority()}")
    
    print(f"\n包含 '任务A': {'任务A' in pq}")
    print(f"包含 '任务D': {'任务D' in pq}")
    
    print(f"\n弹出堆顶后队列大小: {len(pq)} (弹出了 '{pq.pop()}')")
    print()


def update_and_remove():
    """更新优先级和移除元素示例"""
    print("=" * 50)
    print("更新优先级和移除元素")
    print("=" * 50)
    
    pq = PriorityQueue[str]()
    pq.push("低优先级任务", priority=10)
    pq.push("中等优先级任务", priority=5)
    pq.push("高优先级任务", priority=1)
    
    print("\n初始队列:")
    while pq:
        print(f"  - {pq.pop()}")
    
    # 重新推入
    pq.push("低优先级任务", priority=10)
    pq.push("中等优先级任务", priority=5)
    pq.push("高优先级任务", priority=1)
    
    # 更新优先级
    print("\n更新 '低优先级任务' 的优先级为 0（最高）:")
    pq.update_priority("低优先级任务", 0)
    while pq:
        print(f"  - {pq.pop()}")
    
    # 演示移除
    pq.push("任务A", 1)
    pq.push("任务B", 2)
    pq.push("任务C", 3)
    
    print("\n移除 '任务B' 后:")
    pq.remove("任务B")
    while pq:
        print(f"  - {pq.pop()}")
    
    print()


def merge_queues():
    """合并队列示例"""
    print("=" * 50)
    print("合并两个优先队列")
    print("=" * 50)
    
    pq1 = PriorityQueue[int]()
    pq1.push(1, 1)
    pq1.push(3, 3)
    
    pq2 = PriorityQueue[int]()
    pq2.push(2, 2)
    pq2.push(4, 4)
    
    print("\n队列 1: [1(优先级1), 3(优先级3)]")
    print("队列 2: [2(优先级2), 4(优先级4)]")
    
    pq1.merge(pq2)
    
    print("\n合并后按优先级弹出:")
    while pq1:
        print(f"  - {pq1.pop()}")
    
    print()


if __name__ == "__main__":
    basic_usage()
    max_heap_usage()
    peek_and_contains()
    update_and_remove()
    merge_queues()