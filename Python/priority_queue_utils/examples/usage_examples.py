"""
优先队列工具使用示例

演示 PriorityQueue 的各种使用场景：
1. 任务调度
2. 合并有序列表
3. Top-K 问题
4. Dijkstra 最短路径
5. 事件模拟
"""

import sys
import os

# 确保能导入 mod 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PriorityQueue,
    ThreadSafePriorityQueue,
    BoundedPriorityQueue,
    QueueMode,
    create_min_heap,
    create_max_heap,
    merge_queues,
    from_list,
    top_k,
)


def example_task_scheduler():
    """
    示例1: 任务调度系统
    
    按优先级执行任务，支持动态调整任务优先级
    """
    print("\n=== 任务调度系统示例 ===")
    
    # 创建任务队列（数字越小优先级越高）
    task_queue = create_min_heap()
    
    # 添加任务
    task_queue.extend([
        ("发送邮件", 3),
        ("数据备份", 5),
        ("紧急修复", 1),
        ("日志清理", 4),
        ("用户验证", 2),
    ])
    
    print(f"当前队列大小: {len(task_queue)}")
    
    # 查看最高优先级任务
    next_task = task_queue.peek()
    print(f"下一个要执行的任务: {next_task}")
    
    # 动态提升某个任务的优先级
    print("\n提升 '日志清理' 的优先级...")
    task_queue.update_priority_by_value("日志清理", 1)
    
    # 按优先级执行任务
    print("\n按优先级执行任务:")
    while task_queue:
        task, priority = task_queue.pop()
        print(f"  执行: {task} (优先级: {priority})")


def example_merge_sorted_lists():
    """
    示例2: 合并多个有序列表
    
    使用优先队列高效合并 K 个有序列表
    """
    print("\n=== 合并有序列表示例 ===")
    
    # 3 个已排序的列表
    list1 = [1, 4, 7, 10]
    list2 = [2, 3, 5, 8]
    list3 = [6, 9, 11, 12]
    
    # 使用优先队列合并
    pq = create_min_heap()
    
    # 记录每个列表的当前索引
    iterators = {
        0: iter(list1),
        1: iter(list2),
        2: iter(list3),
    }
    
    # 初始化：每个列表取第一个元素
    for list_id, it in iterators.items():
        try:
            value = next(it)
            pq.push((list_id, value), value)
        except StopIteration:
            pass
    
    # 合并
    merged = []
    while pq:
        (list_id, value), _ = pq.pop()
        merged.append(value)
        
        # 从同一个列表取下一个元素
        try:
            next_value = next(iterators[list_id])
            pq.push((list_id, next_value), next_value)
        except StopIteration:
            pass
    
    print(f"列表1: {list1}")
    print(f"列表2: {list2}")
    print(f"列表3: {list3}")
    print(f"合并结果: {merged}")


def example_top_k():
    """
    示例3: Top-K 问题
    
    找出数据流中最大/最小的 K 个元素
    """
    print("\n=== Top-K 问题示例 ===")
    
    # 模拟大量数据
    data = [(f"user_{i}", i * 10 + i % 7) for i in range(1000)]
    
    # 找出分数最高的 5 个用户
    top_5_scores = top_k(data, k=5, largest=True)
    print("分数最高的 5 个用户:")
    for user, score in top_5_scores:
        print(f"  {user}: {score}")
    
    # 找出分数最低的 5 个用户
    bottom_5_scores = top_k(data, k=5, largest=False)
    print("\n分数最低的 5 个用户:")
    for user, score in bottom_5_scores:
        print(f"  {user}: {score}")


def example_dijkstra():
    """
    示例4: Dijkstra 最短路径算法
    
    使用优先队列实现高效的最短路径搜索
    """
    print("\n=== Dijkstra 最短路径示例 ===")
    
    # 构建图（邻接表）
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)],
    }
    
    def dijkstra(graph, start):
        """Dijkstra 算法"""
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        
        pq = create_min_heap()
        pq.push(start, 0)
        
        while pq:
            current, dist = pq.pop()
            
            # 跳过已处理的节点
            if dist > distances[current]:
                continue
            
            for neighbor, weight in graph[current]:
                new_dist = distances[current] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    pq.push(neighbor, new_dist)
        
        return distances
    
    distances = dijkstra(graph, 'A')
    
    print("从节点 A 到各节点的最短距离:")
    for node in sorted(distances.keys()):
        print(f"  A -> {node}: {distances[node]}")


def example_event_simulation():
    """
    示例5: 离散事件模拟
    
    使用优先队列按时间顺序处理事件
    """
    print("\n=== 离散事件模拟示例 ===")
    
    from dataclasses import dataclass
    
    @dataclass(frozen=True)  # 使用 frozen=True 使 dataclass 可哈希
    class Event:
        """事件"""
        name: str
        time: float
        action: str
    
    # 创建事件队列
    event_queue = create_min_heap()
    
    # 添加事件（按时间优先）
    events = [
        Event("客户到达", 0.0, "开始服务"),
        Event("服务完成", 5.0, "客户离开"),
        Event("客户到达", 2.0, "加入等待队列"),
        Event("客户到达", 4.0, "加入等待队列"),
        Event("服务完成", 10.0, "客户离开"),
        Event("店铺关门", 15.0, "停止服务"),
    ]
    
    for event in events:
        event_queue.push(event, event.time)
    
    print("事件模拟时间线:")
    current_time = 0.0
    
    while event_queue:
        event, time = event_queue.pop()
        current_time = time
        
        print(f"  时间 {time:.1f}: {event.name} -> {event.action}")


def example_thread_safe_queue():
    """
    示例6: 多线程任务处理
    
    使用线程安全优先队列实现生产者-消费者模式
    """
    print("\n=== 多线程任务处理示例 ===")
    
    import threading
    import time
    import random
    
    task_queue = ThreadSafePriorityQueue[str, int]()
    results = []
    results_lock = threading.Lock()
    
    def producer(name: str, count: int):
        """生产者：添加任务"""
        for i in range(count):
            priority = random.randint(1, 10)
            task = f"{name}-task-{i}"
            task_queue.push(task, priority)
            time.sleep(0.01)  # 模拟生产延迟
    
    def consumer(name: str, count: int):
        """消费者：处理任务"""
        for _ in range(count):
            result = task_queue.pop()
            if result:
                task, priority = result
                with results_lock:
                    results.append((name, task, priority))
            time.sleep(0.02)  # 模拟处理延迟
    
    # 创建生产者和消费者线程
    producers = [
        threading.Thread(target=producer, args=(f"P{i}", 5))
        for i in range(2)
    ]
    consumers = [
        threading.Thread(target=consumer, args=(f"C{i}", 5))
        for i in range(2)
    ]
    
    # 启动所有线程
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    
    # 等待完成
    for p in producers:
        p.join()
    for c in consumers:
        c.join()
    
    print(f"生产者: 2 个，每个生产 5 个任务")
    print(f"消费者: 2 个，每个消费 5 个任务")
    print(f"处理结果数量: {len(results)}")
    print("前 5 个处理结果:")
    for consumer_name, task, priority in sorted(results, key=lambda x: x[2])[:5]:
        print(f"  消费者 {consumer_name}: {task} (优先级: {priority})")


def example_bounded_queue():
    """
    示例7: 有界队列 - 保持 Top-N 记录
    
    使用有界优先队列保持最近的最高分记录
    """
    print("\n=== 有界队列示例：排行榜 ===")
    
    # 创建容量为 5 的排行榜（保留最高分）
    leaderboard = BoundedPriorityQueue[str, int](max_size=5, mode=QueueMode.MIN_HEAP)
    
    # 添加玩家分数
    scores = [
        ("Alice", 85),
        ("Bob", 92),
        ("Charlie", 78),
        ("David", 95),
        ("Eve", 88),
        ("Frank", 91),  # 会挤掉最低分
        ("Grace", 99),  # 会挤掉下一个最低分
    ]
    
    print("添加分数:")
    for player, score in scores:
        success, evicted = leaderboard.push(player, score)
        if evicted:
            print(f"  {player}: {score} -> 挤掉 {evicted[0]}: {evicted[1]}")
        else:
            print(f"  {player}: {score}")
    
    print("\n当前排行榜 Top 5:")
    for player, score in sorted(leaderboard.to_list(), key=lambda x: -x[1]):
        print(f"  {player}: {score}")
    
    print("\n被挤掉的玩家:")
    for player, score in leaderboard.get_evicted():
        print(f"  {player}: {score}")


def example_priority_update():
    """
    示例8: 动态优先级更新
    
    演示如何在运行时调整任务优先级
    """
    print("\n=== 动态优先级更新示例 ===")
    
    pq = create_min_heap()
    
    # 添加任务并记录序列号
    tasks = {
        "任务A": pq.push("任务A", 3),
        "任务B": pq.push("任务B", 1),
        "任务C": pq.push("任务C", 2),
    }
    
    print("初始队列:")
    for task, priority in pq:
        print(f"  {task}: {priority}")
    
    # 将任务A的优先级提升到最高
    print("\n提升任务A的优先级到 0...")
    pq.update_priority(tasks["任务A"], 0)
    
    print("更新后队列:")
    for task, priority in pq:
        print(f"  {task}: {priority}")
    
    # 按新优先级执行
    print("\n执行顺序:")
    while pq:
        task, priority = pq.pop()
        print(f"  执行: {task} (优先级: {priority})")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("优先队列工具使用示例")
    print("=" * 60)
    
    example_task_scheduler()
    example_merge_sorted_lists()
    example_top_k()
    example_dijkstra()
    example_event_simulation()
    example_thread_safe_queue()
    example_bounded_queue()
    example_priority_update()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()