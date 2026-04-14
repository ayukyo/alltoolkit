"""
高级优先队列功能示例

演示：
- UpdatablePriorityQueue 高效优先级更新
- BoundedPriorityQueue 有界队列
- 合并有序列表
- top_k 函数
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    UpdatablePriorityQueue,
    BoundedPriorityQueue,
    merge_sorted_lists,
    top_k,
)


def updatable_queue_demo():
    """可更新优先级队列演示"""
    print("=" * 50)
    print("UpdatablePriorityQueue - 高效优先级更新")
    print("=" * 50)
    
    pq = UpdatablePriorityQueue[str]()
    
    # 添加任务
    pq.push("任务A", 3)
    pq.push("任务B", 2)
    pq.push("任务C", 1)
    
    print("\n初始队列:")
    print(f"  下一个任务: {pq.peek()}")
    print(f"  '任务A' 的优先级: {pq.get_priority('任务A')}")
    
    # 更新优先级
    print("\n更新 '任务A' 的优先级为 0（最高）:")
    pq.update_priority("任务A", 0)
    print(f"  下一个任务: {pq.peek()}")
    print(f"  '任务A' 的优先级: {pq.get_priority('任务A')}")
    
    # 重复推入会更新优先级
    print("\n推入已存在的元素会更新优先级:")
    pq.push("任务B", 0)  # 更新为最高优先级
    print(f"  下一个任务: {pq.peek()}")
    
    print("\n按优先级执行:")
    while pq:
        print(f"  - {pq.pop()}")
    
    print()


def bounded_queue_demo():
    """有界优先队列演示"""
    print("=" * 50)
    print("BoundedPriorityQueue - 有界队列")
    print("=" * 50)
    
    pq = BoundedPriorityQueue[str](max_size=3)
    
    print(f"\n队列最大容量: {pq.max_size}")
    
    # 添加任务
    print("\n添加任务:")
    print(f"  添加 '低优先级' (优先级=5): {pq.push('低优先级', 5)}")
    print(f"  添加 '中优先级' (优先级=3): {pq.push('中优先级', 3)}")
    print(f"  添加 '高优先级' (优先级=1): {pq.push('高优先级', 1)}")
    
    print(f"\n队列已满: {pq.is_full()}")
    
    # 尝试添加更低优先级
    print("\n尝试添加更低优先级任务:")
    print(f"  添加 '超低优先级' (优先级=10): {pq.push('超低优先级', 10)}")
    
    # 添加更高优先级
    print("\n尝试添加更高优先级任务:")
    print(f"  添加 '紧急任务' (优先级=0): {pq.push('紧急任务', 0)}")
    
    print("\n队列内容:")
    while pq:
        print(f"  - {pq.pop()}")
    
    print()


def top_k_demo():
    """top_k 函数演示"""
    print("=" * 50)
    print("top_k - 获取前 K 个元素")
    print("=" * 50)
    
    # 学生成绩
    students = [
        ("Alice", 85),
        ("Bob", 92),
        ("Charlie", 78),
        ("David", 95),
        ("Eve", 88),
        ("Frank", 72),
        ("Grace", 91),
        ("Henry", 83),
    ]
    
    print("\n学生成绩:")
    for name, score in students:
        print(f"  {name}: {score}")
    
    # 前 3 名
    top3 = top_k(students, 3, largest=True)
    print("\n成绩前 3 名:")
    for name, score in top3:
        print(f"  {name}: {score}")
    
    # 后 3 名
    bottom3 = top_k(students, 3, largest=False)
    print("\n成绩后 3 名:")
    for name, score in bottom3:
        print(f"  {name}: {score}")
    
    print()


def merge_sorted_lists_demo():
    """合并有序列表演示"""
    print("=" * 50)
    print("merge_sorted_lists - 合并有序列表")
    print("=" * 50)
    
    # 多个有序列表
    list1 = [("Alice", 1), ("Charlie", 3), ("Eve", 5)]
    list2 = [("Bob", 2), ("David", 4), ("Frank", 6)]
    list3 = [("Grace", 0), ("Henry", 7)]
    
    print("\n列表 1（按优先级排序）:")
    for name, priority in list1:
        print(f"  {name}: {priority}")
    
    print("\n列表 2:")
    for name, priority in list2:
        print(f"  {name}: {priority}")
    
    print("\n列表 3:")
    for name, priority in list3:
        print(f"  {name}: {priority}")
    
    # 合并
    merged = merge_sorted_lists([list1, list2, list3])
    
    print("\n合并后的列表:")
    for name, priority in merged:
        print(f"  {name}: {priority}")
    
    print()


def use_case_task_priority():
    """实际用例：任务优先级调度"""
    print("=" * 50)
    print("实际用例：任务优先级调度")
    print("=" * 50)
    
    from datetime import datetime, timedelta
    
    # 使用可更新优先级队列
    pq = UpdatablePriorityQueue[dict]()
    
    # 添加任务
    tasks = [
        {"id": "TASK-001", "name": "修复 Bug", "priority": 1},
        {"id": "TASK-002", "name": "写文档", "priority": 5},
        {"id": "TASK-003", "name": "代码审查", "priority": 3},
        {"id": "TASK-004", "name": "回复邮件", "priority": 4},
    ]
    
    print("\n初始任务:")
    for task in tasks:
        pq.push(task, task["priority"])
        print(f"  [{task['id']}] {task['name']} (优先级: {task['priority']})")
    
    # 模拟优先级变化
    print("\n'写文档' 任务变得紧急，优先级提升为 1:")
    pq.update_priority(
        next(t for t in tasks if t["id"] == "TASK-002"),
        1
    )
    
    print("\n任务执行顺序:")
    while pq:
        task = pq.pop()
        print(f"  [{task['id']}] {task['name']}")
    
    print()


def use_case_top_k_products():
    """实际用例：热销商品 Top K"""
    print("=" * 50)
    print("实际用例：热销商品 Top K")
    print("=" * 50)
    
    # 商品销量数据
    products = [
        ("iPhone 15", 1250),
        ("Samsung S24", 980),
        ("MacBook Pro", 650),
        ("iPad Air", 890),
        ("AirPods Pro", 1420),
        ("Apple Watch", 780),
        ("Surface Pro", 450),
        ("Pixel 8", 520),
    ]
    
    print("\n商品销量:")
    for name, sales in products:
        print(f"  {name}: {sales} 件")
    
    # Top 5 热销商品
    top5 = top_k(products, 5, largest=True)
    
    print("\nTop 5 热销商品:")
    for i, (name, sales) in enumerate(top5, 1):
        print(f"  第 {i} 名: {name} ({sales} 件)")
    
    print()


if __name__ == "__main__":
    updatable_queue_demo()
    bounded_queue_demo()
    top_k_demo()
    merge_sorted_lists_demo()
    use_case_task_priority()
    use_case_top_k_products()