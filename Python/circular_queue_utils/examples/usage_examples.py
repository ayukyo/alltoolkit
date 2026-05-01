"""
Circular Queue Utils 使用示例

本文件展示循环队列模块的各种使用场景。
"""

import time
import threading
from typing import List

# 添加父目录到路径
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circular_queue_utils.mod import (
    CircularQueue,
    create_queue,
    sliding_window,
    recent_buffer
)


def example_basic_operations():
    """基本操作示例"""
    print("\n" + "=" * 50)
    print("基本操作示例")
    print("=" * 50)
    
    # 创建队列
    queue = CircularQueue[int](capacity=5)
    print(f"创建容量为 5 的队列: {queue}")
    
    # 入队
    queue.enqueue(1, 2, 3)
    print(f"入队 1, 2, 3: {queue}")
    
    # 查看队首和队尾
    print(f"队首元素: {queue.peek()}")
    print(f"队尾元素: {queue.peek_last()}")
    
    # 出队
    item = queue.dequeue()
    print(f"出队: {item}")
    print(f"当前队列: {queue}")
    
    # 查看队列状态
    print(f"队列大小: {len(queue)}")
    print(f"是否为空: {queue.is_empty}")
    print(f"是否已满: {queue.is_full}")


def example_overwrite_mode():
    """自动覆盖模式示例"""
    print("\n" + "=" * 50)
    print("自动覆盖模式示例")
    print("=" * 50)
    
    # 创建自动覆盖队列（用于保存最近的 N 个元素）
    recent_items = CircularQueue[str](capacity=3, overwrite=True)
    
    print("容量为 3，启用自动覆盖:")
    recent_items.enqueue("消息1", "消息2", "消息3")
    print(f"初始: {recent_items.to_list()}")
    
    recent_items.enqueue("消息4", "消息5")
    print(f"添加消息4、消息5后: {recent_items.to_list()}")
    
    recent_items.enqueue("消息6")
    print(f"添加消息6后: {recent_items.to_list()}")
    
    print(f"\n统计信息: {recent_items.stats}")


def example_sliding_window():
    """滑动窗口示例"""
    print("\n" + "=" * 50)
    print("滑动窗口示例")
    print("=" * 50)
    
    # 计算移动平均
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    window_size = 3
    
    print(f"数据: {data}")
    print(f"窗口大小: {window_size}")
    print(f"\n滑动窗口:")
    
    for i, window in enumerate(sliding_window(data, window_size)):
        avg = sum(window) / len(window)
        print(f"  窗口 {i + 1}: {window} -> 平均值: {avg:.1f}")


def example_moving_average():
    """移动平均计算器示例"""
    print("\n" + "=" * 50)
    print("移动平均计算器")
    print("=" * 50)
    
    def moving_average(data: List[float], window: int) -> List[float]:
        """计算移动平均"""
        result = []
        queue = CircularQueue[float](capacity=window, overwrite=True)
        
        for value in data:
            queue.enqueue(value)
            if len(queue) == window:
                avg = sum(queue) / window
                result.append(avg)
        
        return result
    
    # 股票价格示例
    prices = [100.0, 102.5, 101.8, 105.2, 103.7, 107.1, 108.3, 106.9, 109.5, 112.0]
    ma5 = moving_average(prices, 5)
    
    print(f"股票价格: {prices}")
    print(f"5日移动平均: {ma5}")


def example_rate_limiter():
    """速率限制器示例"""
    print("\n" + "=" * 50)
    print("速率限制器示例")
    print("=" * 50)
    
    class RateLimiter:
        """简单的滑动窗口速率限制器"""
        
        def __init__(self, max_requests: int, window_seconds: float):
            self.queue = CircularQueue[float](capacity=max_requests, overwrite=True)
            self.window = window_seconds
        
        def allow(self) -> bool:
            """检查是否允许请求"""
            now = time.time()
            
            # 移除过期的请求记录
            while self.queue and now - self.queue.peek() > self.window:
                self.queue.dequeue()
            
            # 检查是否超过限制
            if self.queue.is_full:
                return False
            
            self.queue.enqueue(now)
            return True
        
        @property
        def remaining(self) -> int:
            """剩余请求数"""
            now = time.time()
            count = 0
            for timestamp in self.queue:
                if now - timestamp <= self.window:
                    count += 1
            return self.queue.capacity - count
    
    # 创建速率限制器：每秒最多 5 个请求
    limiter = RateLimiter(max_requests=5, window_seconds=1.0)
    
    print("速率限制器: 每秒最多 5 个请求")
    for i in range(8):
        allowed = limiter.allow()
        print(f"  请求 {i + 1}: {'✓ 允许' if allowed else '✗ 拒绝'}")


def example_event_buffer():
    """事件缓冲区示例"""
    print("\n" + "=" * 50)
    print("事件缓冲区示例")
    print("=" * 50)
    
    class EventBuffer:
        """事件缓冲区，保存最近的事件"""
        
        def __init__(self, capacity: int):
            self.buffer = recent_buffer(capacity)
        
        def log(self, event: str):
            """记录事件"""
            timestamp = time.strftime("%H:%M:%S")
            self.buffer.enqueue(f"[{timestamp}] {event}")
        
        def get_recent(self, count: int = None) -> List[str]:
            """获取最近的事件"""
            events = self.buffer.to_list()
            if count:
                return events[-count:]
            return events
        
        def search(self, keyword: str) -> List[str]:
            """搜索包含关键词的事件"""
            return self.buffer.find_all(lambda e: keyword in e)
    
    # 使用示例
    logger = EventBuffer(capacity=5)
    
    logger.log("用户登录")
    logger.log("查看商品列表")
    logger.log("添加商品到购物车")
    logger.log("用户登出")
    logger.log("用户登录")
    logger.log("查看订单")  # 会覆盖最旧的 "用户登录"
    
    print("最近的事件:")
    for event in logger.get_recent():
        print(f"  {event}")
    
    print(f"\n搜索 '登录': {logger.search('登录')}")


def example_thread_safe_queue():
    """线程安全队列示例"""
    print("\n" + "=" * 50)
    print("线程安全队列示例（生产者-消费者）")
    print("=" * 50)
    
    queue = CircularQueue[int](capacity=10, thread_safe=True)
    produced = []
    consumed = []
    
    def producer(items: List[int]):
        for item in items:
            queue.enqueue(item)
            produced.append(item)
            time.sleep(0.01)
    
    def consumer(count: int):
        for _ in range(count):
            item = queue.blocking_dequeue(timeout=1.0)
            if item is not None:
                consumed.append(item)
    
    # 启动生产者
    producer_thread = threading.Thread(target=producer, args=(list(range(1, 6)),))
    producer_thread.start()
    
    # 启动消费者
    consumer_thread = threading.Thread(target=consumer, args=(5,))
    consumer_thread.start()
    
    # 等待完成
    producer_thread.join()
    consumer_thread.join()
    
    print(f"生产: {produced}")
    print(f"消费: {consumed}")
    print(f"顺序一致: {produced == consumed}")


def example_task_queue():
    """任务队列示例"""
    print("\n" + "=" * 50)
    print("任务队列示例")
    print("=" * 50)
    
    class TaskQueue:
        """简单任务队列"""
        
        def __init__(self, capacity: int):
            self.queue = CircularQueue(capacity=capacity, thread_safe=True)
        
        def submit(self, task_name: str, priority: int = 0):
            """提交任务"""
            self.queue.enqueue({"name": task_name, "priority": priority})
        
        def process(self) -> int:
            """处理所有任务"""
            count = 0
            while self.queue:
                task = self.queue.dequeue()
                print(f"  处理任务: {task['name']} (优先级: {task['priority']})")
                count += 1
            return count
    
    task_queue = TaskQueue(capacity=10)
    
    task_queue.submit("初始化系统", priority=10)
    task_queue.submit("加载数据", priority=5)
    task_queue.submit("处理请求", priority=3)
    task_queue.submit("生成报告", priority=1)
    
    print("处理任务:")
    processed = task_queue.process()
    print(f"共处理 {processed} 个任务")


def example_data_stream_buffer():
    """数据流缓冲区示例"""
    print("\n" + "=" * 50)
    print("数据流缓冲区示例")
    print("=" * 50)
    
    class StreamBuffer:
        """数据流缓冲区，用于数据处理流水线"""
        
        def __init__(self, capacity: int):
            self.buffer = CircularQueue(capacity=capacity, overwrite=False)
            self.dropped = 0
        
        def write(self, data: List[int]) -> int:
            """写入数据，返回成功写入的数量"""
            written = 0
            for item in data:
                try:
                    self.buffer.enqueue(item)
                    written += 1
                except OverflowError:
                    self.dropped += 1
            return written
        
        def read(self, count: int = None) -> List[int]:
            """读取数据"""
            if count is None:
                count = len(self.buffer)
            
            result = []
            for _ in range(min(count, len(self.buffer))):
                result.append(self.buffer.dequeue())
            return result
        
        @property
        def stats(self) -> dict:
            return {
                "buffered": len(self.buffer),
                "capacity": self.buffer.capacity,
                "dropped": self.dropped
            }
    
    # 使用示例
    stream = StreamBuffer(capacity=5)
    
    print("写入数据流:")
    data1 = [1, 2, 3, 4, 5]
    written1 = stream.write(data1)
    print(f"  写入 {data1}: 成功 {written1} 个")
    
    data2 = [6, 7, 8]
    written2 = stream.write(data2)
    print(f"  写入 {data2}: 成功 {written2} 个 (丢弃 {len(data2) - written2} 个)")
    
    print(f"\n缓冲区状态: {stream.stats}")
    
    print("\n读取数据:")
    data = stream.read(3)
    print(f"  读取 3 个: {data}")
    
    data = stream.read()
    print(f"  读取剩余: {data}")


def example_history_tracker():
    """历史记录跟踪器示例"""
    print("\n" + "=" * 50)
    print("历史记录跟踪器示例")
    print("=" * 50)
    
    class HistoryTracker:
        """命令历史跟踪器"""
        
        def __init__(self, max_size: int = 100):
            self.history = recent_buffer(max_size)
        
        def add(self, command: str):
            """添加命令"""
            self.history.enqueue(command)
        
        def get_last(self, count: int = 10) -> List[str]:
            """获取最近的命令"""
            all_history = self.history.to_list()
            return all_history[-count:]
        
        def search(self, keyword: str) -> List[str]:
            """搜索历史"""
            return self.history.find_all(lambda cmd: keyword in cmd)
        
        def clear(self):
            """清空历史"""
            self.history.clear()
    
    # 使用示例
    history = HistoryTracker(max_size=5)
    
    history.add("ls -la")
    history.add("cd /home")
    history.add("cat file.txt")
    history.add("grep 'error' log.txt")
    history.add("python script.py")
    history.add("git status")  # 会覆盖 "ls -la"
    
    print("最近 5 条命令:")
    for i, cmd in enumerate(history.get_last(5), 1):
        print(f"  {i}. {cmd}")
    
    print(f"\n搜索 'git': {history.search('git')}")


def example_matrix_style():
    """矩阵风格输出示例"""
    print("\n" + "=" * 50)
    print("循环缓冲区 - Matrix 风格")
    print("=" * 50)
    
    # 创建一个固定宽度的显示缓冲区
    width = 20
    display = CircularQueue[str](capacity=width, overwrite=True)
    
    # 初始化
    for _ in range(width):
        display.enqueue(" ")
    
    # 模拟滚动文字
    message = "Hello, Circular Queue! "
    for char in message:
        display.enqueue(char)
        print("\r" + "".join(display), end="", flush=True)
        time.sleep(0.05)
    
    print()  # 换行


if __name__ == "__main__":
    print("=" * 50)
    print("Circular Queue Utils 使用示例")
    print("=" * 50)
    
    example_basic_operations()
    example_overwrite_mode()
    example_sliding_window()
    example_moving_average()
    example_rate_limiter()
    example_event_buffer()
    example_task_queue()
    example_data_stream_buffer()
    example_history_tracker()
    
    # 线程安全示例（可能会增加运行时间）
    try:
        example_thread_safe_queue()
    except Exception as e:
        print(f"线程安全示例跳过: {e}")
    
    # Matrix 风格输出
    example_matrix_style()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)