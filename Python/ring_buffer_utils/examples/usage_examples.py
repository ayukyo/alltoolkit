"""
Ring Buffer Utils 使用示例

演示循环缓冲区的各种应用场景。
"""

import sys
sys.path.insert(0, '..')

from ring_buffer_utils.mod import (
    RingBuffer, NumericRingBuffer, EventBuffer,
    create_ring_buffer, create_numeric_buffer,
    sliding_window, batch_process
)
import time


def basic_usage():
    """基础用法示例"""
    print("=" * 50)
    print("基础用法示例")
    print("=" * 50)
    
    # 创建容量为 5 的循环缓冲区
    rb = RingBuffer[int](5)
    
    # 添加元素
    for i in range(1, 8):
        rb.append(i)
        print(f"添加 {i}，缓冲区: {list(rb)}")
    
    # 访问元素
    print(f"\n第一个元素: {rb[0]}")
    print(f"最后一个元素: {rb[-1]}")
    
    # 弹出元素
    print(f"\n弹出最新: {rb.pop()}")
    print(f"弹出最旧: {rb.popleft()}")
    print(f"剩余: {list(rb)}")
    
    # 清空
    rb.clear()
    print(f"\n清空后: {list(rb)}")


def numeric_buffer_example():
    """数值缓冲区示例"""
    print("\n" + "=" * 50)
    print("数值缓冲区示例 - 实时统计")
    print("=" * 50)
    
    # 创建数值缓冲区，用于实时统计
    stats = NumericRingBuffer(10)
    
    # 模拟温度传感器数据
    temperatures = [22.5, 23.1, 22.8, 23.5, 24.0, 23.8, 24.2, 24.5, 24.1, 23.9]
    
    for temp in temperatures:
        stats.append(temp)
        print(f"温度: {temp:.1f}°C | 均值: {stats.mean:.2f}°C | "
              f"范围: {stats.min_value:.1f}~{stats.max_value:.1f}°C | "
              f"标准差: {stats.std_dev:.3f}")
    
    # 移动平均
    print(f"\n3点移动平均: {[f'{v:.2f}' for v in stats.moving_average(3)]}")


def event_buffer_example():
    """事件缓冲区示例"""
    print("\n" + "=" * 50)
    print("事件缓冲区示例 - 日志系统")
    print("=" * 50)
    
    # 创建事件缓冲区
    log_buffer = EventBuffer[dict](100, ttl_seconds=60)
    
    # 添加日志事件
    base_time = time.time()
    
    log_buffer.add({"level": "INFO", "message": "系统启动"}, base_time)
    log_buffer.add({"level": "DEBUG", "message": "加载配置"}, base_time + 1)
    log_buffer.add({"level": "INFO", "message": "连接数据库"}, base_time + 2)
    log_buffer.add({"level": "WARN", "message": "连接超时，重试中"}, base_time + 3)
    log_buffer.add({"level": "INFO", "message": "数据库连接成功"}, base_time + 5)
    
    # 查询事件
    print("所有事件:")
    for ts, event in log_buffer:
        print(f"  [{event['level']:5}] {event['message']}")
    
    # 时间范围查询
    start = base_time + 2
    end = base_time + 5
    print(f"\n时间范围 [{start} - {end}] 的事件:")
    for ts, event in log_buffer.get_events(since=start, until=end):
        print(f"  [{event['level']:5}] {event['message']}")


def sliding_window_example():
    """滑动窗口示例"""
    print("\n" + "=" * 50)
    print("滑动窗口示例 - 数据流处理")
    print("=" * 50)
    
    # 模拟数据流
    data_stream = [10, 12, 11, 15, 14, 13, 16, 18, 17, 20]
    
    print("原始数据:", data_stream)
    print("\n窗口大小=3 的滑动平均:")
    
    for window in sliding_window(data_stream, 3):
        avg = sum(window) / len(window)
        print(f"  窗口 {window} -> 均值 {avg:.2f}")


def batch_processing_example():
    """批量处理示例"""
    print("\n" + "=" * 50)
    print("批量处理示例 - 数据分批")
    print("=" * 50)
    
    # 模拟大量数据
    large_data = list(range(1, 101))  # 1-100
    
    # 批量求和
    batch_sums = batch_process(large_data, 10, sum)
    print(f"批量求和结果 (每批10个): {batch_sums}")
    
    # 批量统计
    def batch_stats(batch):
        return {
            "count": len(batch),
            "sum": sum(batch),
            "avg": sum(batch) / len(batch)
        }
    
    results = batch_process(large_data[:25], 5, batch_stats)
    print("\n批量统计结果:")
    for i, result in enumerate(results):
        print(f"  批次 {i+1}: {result}")


def rate_limiter_example():
    """限流器示例"""
    print("\n" + "=" * 50)
    print("实际应用 - 简单限流器")
    print("=" * 50)
    
    class RateLimiter:
        """滑动窗口限流器"""
        
        def __init__(self, max_requests: int, window_seconds: float):
            self.buffer = NumericRingBuffer(max_requests)
            self.window = window_seconds
        
        def allow(self) -> bool:
            """检查是否允许请求"""
            now = time.time()
            cutoff = now - self.window
            
            # 检查是否在限制内
            # 这里简化处理，实际需要时间戳
            return len(self.buffer) < self.buffer.capacity
        
        def record(self):
            """记录请求"""
            self.buffer.append(time.time())
    
    limiter = RateLimiter(max_requests=5, window_seconds=1.0)
    
    print("限流器测试 (最大 5 请求/秒):")
    for i in range(8):
        if limiter.allow():
            limiter.record()
            print(f"  请求 {i+1}: ✓ 允许")
        else:
            print(f"  请求 {i+1}: ✗ 拒绝")


def thread_safe_example():
    """线程安全示例"""
    print("\n" + "=" * 50)
    print("线程安全示例 - 多生产者")
    print("=" * 50)
    
    import threading
    
    # 创建线程安全缓冲区
    buffer = RingBuffer[int](100, thread_safe=True)
    
    def producer(start: int, count: int):
        for i in range(count):
            buffer.append(start + i)
    
    # 多线程添加
    threads = [
        threading.Thread(target=producer, args=(i * 100, 50))
        for i in range(3)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"添加完成，缓冲区大小: {len(buffer)}")
    print(f"前 10 个元素: {buffer.to_list()[:10]}")


def message_queue_example():
    """消息队列示例"""
    print("\n" + "=" * 50)
    print("实际应用 - 消息队列")
    print("=" * 50)
    
    # 使用循环缓冲区实现简单消息队列
    class MessageQueue:
        def __init__(self, max_size: int):
            self.buffer = RingBuffer[dict](max_size)
        
        def send(self, topic: str, message: str):
            """发送消息"""
            self.buffer.append({"topic": topic, "message": message, "time": time.time()})
            print(f"  [发送] {topic}: {message}")
        
        def receive(self, count: int = 1):
            """接收消息"""
            messages = []
            for _ in range(min(count, len(self.buffer))):
                messages.append(self.buffer.popleft())
            return messages
        
        def peek(self):
            """查看最新消息"""
            if self.buffer:
                return self.buffer.peek()
            return None
    
    queue = MessageQueue(10)
    
    # 发送消息
    queue.send("system", "启动完成")
    queue.send("user", "用户登录")
    queue.send("order", "新订单 #12345")
    
    # 查看消息
    print(f"\n最新消息: {queue.peek()}")
    
    # 接收消息
    print("\n接收消息:")
    for msg in queue.receive(2):
        print(f"  [接收] {msg['topic']}: {msg['message']}")


def rolling_stats_example():
    """滚动统计示例"""
    print("\n" + "=" * 50)
    print("实际应用 - 滚动统计")
    print("=" * 50)
    
    # 模拟实时数据流
    import random
    random.seed(42)
    
    window = NumericRingBuffer(10)
    
    print("实时数据流 (窗口大小=10):")
    print("-" * 60)
    
    for i in range(20):
        value = random.gauss(50, 10)  # 均值50，标准差10
        window.append(value)
        
        if len(window) >= 5:  # 至少 5 个数据才开始统计
            print(f"值: {value:6.2f} | "
                  f"均值: {window.mean:6.2f} | "
                  f"标准差: {window.std_dev:5.2f} | "
                  f"范围: [{window.min_value:.1f}, {window.max_value:.1f}]")
        else:
            print(f"值: {value:6.2f} | 数据不足...")


if __name__ == "__main__":
    basic_usage()
    numeric_buffer_example()
    event_buffer_example()
    sliding_window_example()
    batch_processing_example()
    rate_limiter_example()
    thread_safe_example()
    message_queue_example()
    rolling_stats_example()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)