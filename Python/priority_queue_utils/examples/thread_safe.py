"""
线程安全优先队列示例

演示 ThreadSafePriorityQueue 的使用：
- 多线程生产者-消费者模式
- 阻塞等待
- 并发安全操作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import ThreadSafePriorityQueue
import threading
import time
import random


def producer_consumer_demo():
    """生产者-消费者模式演示"""
    print("=" * 50)
    print("多线程生产者-消费者模式")
    print("=" * 50)
    
    queue = ThreadSafePriorityQueue[str]()
    produced_count = 0
    consumed_count = 0
    lock = threading.Lock()
    
    def producer(name: str, count: int):
        nonlocal produced_count
        for i in range(count):
            priority = random.randint(1, 10)
            item = f"{name}-任务{i+1}"
            queue.push(item, priority)
            with lock:
                produced_count += 1
            time.sleep(random.uniform(0.01, 0.05))
    
    def consumer(name: str, count: int):
        nonlocal consumed_count
        for _ in range(count):
            item = queue.pop(timeout=1.0)
            if item is not None:
                with lock:
                    consumed_count += 1
                time.sleep(random.uniform(0.01, 0.03))
    
    # 创建生产者和消费者线程
    producers = [
        threading.Thread(target=producer, args=("P1", 10)),
        threading.Thread(target=producer, args=("P2", 10)),
        threading.Thread(target=producer, args=("P3", 10)),
    ]
    
    consumers = [
        threading.Thread(target=consumer, args=("C1", 15)),
        threading.Thread(target=consumer, args=("C2", 15)),
    ]
    
    # 启动所有线程
    start_time = time.time()
    
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    
    # 等待所有线程完成
    for p in producers:
        p.join()
    for c in consumers:
        c.join()
    
    elapsed = time.time() - start_time
    
    print(f"\n生产者线程数: {len(producers)}")
    print(f"消费者线程数: {len(consumers)}")
    print(f"生产任务数: {produced_count}")
    print(f"消费任务数: {consumed_count}")
    print(f"耗时: {elapsed:.2f} 秒")
    print(f"队列剩余: {len(queue)}")
    
    # 清空剩余任务
    queue.clear()
    print()


def blocking_wait_demo():
    """阻塞等待演示"""
    print("=" * 50)
    print("阻塞等待演示")
    print("=" * 50)
    
    queue = ThreadSafePriorityQueue[int]()
    result = []
    
    def delayed_producer():
        time.sleep(0.5)
        queue.push(42, 1)
        print("  [生产者] 已推入任务")
    
    def waiting_consumer():
        print("  [消费者] 等待任务...")
        item = queue.pop(timeout=2.0)
        if item is not None:
            result.append(item)
            print(f"  [消费者] 收到任务: {item}")
        else:
            print("  [消费者] 超时，未收到任务")
    
    # 启动消费者和生产者
    consumer_thread = threading.Thread(target=waiting_consumer)
    producer_thread = threading.Thread(target=delayed_producer)
    
    start_time = time.time()
    
    consumer_thread.start()
    producer_thread.start()
    
    consumer_thread.join()
    producer_thread.join()
    
    elapsed = time.time() - start_time
    print(f"\n等待时间: {elapsed:.2f} 秒")
    print(f"收到结果: {result}")
    print()


def try_pop_demo():
    """非阻塞弹出演示"""
    print("=" * 50)
    print("非阻塞弹出演示")
    print("=" * 50)
    
    queue = ThreadSafePriorityQueue[str]()
    
    # 空队列尝试弹出
    print("\n空队列尝试弹出:")
    item = queue.try_pop()
    print(f"  结果: {item}")
    
    # 添加一些任务
    queue.push("高优先级", 1)
    queue.push("低优先级", 5)
    
    print("\n队列非空时弹出:")
    while queue:
        item = queue.try_pop()
        print(f"  弹出: {item}")
    
    print()


def concurrent_peek():
    """并发查看堆顶演示"""
    print("=" * 50)
    print("并发查看堆顶")
    print("=" * 50)
    
    queue = ThreadSafePriorityQueue[int]()
    
    # 添加任务
    for i in range(5):
        queue.push(i + 1, i + 1)
    
    print(f"\n队列大小: {len(queue)}")
    
    # 多个线程同时查看堆顶
    results = []
    lock = threading.Lock()
    
    def peek_task():
        item = queue.peek()
        with lock:
            results.append(item)
    
    threads = [threading.Thread(target=peek_task) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"多个线程查看堆顶: {results}")
    print(f"堆顶元素未被移除，队列大小仍为: {len(queue)}")
    
    queue.clear()
    print()


if __name__ == "__main__":
    producer_consumer_demo()
    blocking_wait_demo()
    try_pop_demo()
    concurrent_peek()