"""
Sliding Window Utilities 使用示例

展示滑动窗口工具的各种使用场景：
1. 移动平均计算（股票/数据分析）
2. 限流器使用（API 保护）
3. 时间窗口统计（日志分析）
4. 窗口最值查询（数据监控）
5. 滑动窗口计数（事件追踪）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SlidingWindow,
    NumericSlidingWindow,
    MovingAverage,
    TimeSlidingWindow,
    RateLimiter,
    MinMaxSlidingWindow,
    SlidingWindowCounter,
    moving_average,
    sliding_window_stats,
    sliding_window_min_max,
)
import time


def example_moving_average():
    """
    示例 1: 移动平均计算
    
    应用场景：
    - 股票技术分析
    - 数据平滑处理
    - 传感器数据滤波
    """
    print("=" * 60)
    print("示例 1: 移动平均计算")
    print("=" * 60)
    
    # 模拟股票价格数据
    prices = [100, 102, 98, 105, 110, 108, 115, 120, 118, 125]
    
    print(f"\n股票价格数据: {prices}")
    
    # 计算不同类型的移动平均
    sma_5 = moving_average(prices, window=5, ma_type='sma')
    wma_5 = moving_average(prices, window=5, ma_type='wma')
    ema_5 = moving_average(prices, window=5, ma_type='ema')
    
    print("\n--- 5 日移动平均 ---")
    print(f"SMA (简单): {[round(x, 2) for x in sma_5]}")
    print(f"WMA (加权): {[round(x, 2) for x in wma_5]}")
    print(f"EMA (指数): {[round(x, 2) for x in ema_5]}")
    
    # 实时更新场景
    print("\n--- 实时价格追踪 ---")
    ma = MovingAverage(window_size=3, ma_type='sma')
    
    for price in [100, 102, 98, 105]:
        avg = ma.update(price)
        print(f"新价格: {price}, 3日SMA: {avg:.2f}")
    
    print()


def example_rate_limiter():
    """
    示例 2: API 限流
    
    应用场景：
    - API 请求保护
    - 防止滥用
    - 流量控制
    """
    print("=" * 60)
    print("示例 2: API 限流")
    print("=" * 60)
    
    # 创建不同类型的限流器
    print("\n--- 滑动窗口限流器 ---")
    limiter = RateLimiter(max_requests=5, window_seconds=10, algorithm='sliding')
    
    # 模拟请求
    print("\n模拟 10 次请求，限制 5 次/10秒:")
    for i in range(10):
        if limiter.allow():
            print(f"请求 {i+1}: ✓ 允许")
        else:
            print(f"请求 {i+1}: ✗ 被限流")
    
    # 查看状态
    print(f"\n当前状态: {limiter.get_state()}")
    
    # 令牌桶限流器
    print("\n--- 令牌桶限流器 ---")
    token_limiter = RateLimiter(max_requests=10, window_seconds=1.0, algorithm='token')
    
    print("\n令牌桶限流器特点：允许突发流量")
    for i in range(15):
        allowed = token_limiter.allow()
        status = "✓" if allowed else "✗"
        print(f"请求 {i+1}: {status}")
        if i == 9:
            print("   (初始令牌耗尽，等待补充...)")
    
    print()


def example_numeric_window():
    """
    示例 3: 数值窗口统计
    
    应用场景：
    - 实时数据监控
    - 传感器数据分析
    - 性能指标追踪
    """
    print("=" * 60)
    print("示例 3: 数值窗口统计")
    print("=" * 60)
    
    # 模拟温度传感器数据
    temperatures = [22.5, 23.1, 22.8, 24.0, 23.5, 22.9, 23.8, 24.2]
    
    print(f"\n温度数据: {temperatures}")
    
    # 使用数值滑动窗口
    window = NumericSlidingWindow(size=5)
    
    print("\n--- 5 分钟窗口统计（实时更新）---")
    print("时间 | 温度 | 窗口均值 | 最小 | 最大 | 标准差")
    print("-" * 50)
    
    for i, temp in enumerate(temperatures):
        window.add(temp)
        stats = window.get_stats()
        print(f"{i+1:4} | {temp:4.1f} | {stats.mean:7.2f} | {stats.min:4.1f} | {stats.max:4.1f} | {stats.std_dev:6.2f}")
    
    print()


def example_time_window():
    """
    示例 4: 时间窗口事件追踪
    
    应用场景：
    - 日志分析
    - 用户行为追踪
    - 实时监控告警
    """
    print("=" * 60)
    print("示例 4: 时间窗口事件追踪")
    print("=" * 60)
    
    # 创建 30 秒时间窗口
    window = TimeSlidingWindow(window_seconds=30)
    
    print("\n--- 模拟事件流 ---")
    
    # 添加事件（使用相对时间）
    events = [
        (0, "用户登录"),
        (5, "页面访问"),
        (10, "API调用"),
        (15, "文件下载"),
        (20, "用户操作"),
    ]
    
    for t, event in events:
        window.add(event, timestamp=t)
        print(f"时间 {t}s: {event}")
    
    # 模拟时间流逝，查看窗口内容
    print("\n--- 窗口内容（当前时间 25s）---")
    current_events = window.get_window()
    print(f"最近 30 秒内事件: {current_events}")
    print(f"事件数量: {len(current_events)}")
    
    print("\n--- 窗口内容（当前时间 35s）---")
    # 添加新事件
    window.add("新登录", timestamp=35)
    # 添加会触发清理的事件
    window.add("触发清理", timestamp=35)
    
    # 手动检查（使用 cleanup=False 防止自动清理）
    events_now = window.get_window()
    print(f"最近 30 秒内事件: {events_now}")
    
    print()


def example_min_max_window():
    """
    示例 5: 窗口最值查询
    
    应用场景：
    - 价格监控（最高/最低价）
    - 性能监控（峰值检测）
    - 异常检测
    """
    print("=" * 60)
    print("示例 5: 窗口最值查询（O(1) 复杂度）")
    print("=" * 60)
    
    # 模拟 CPU 使用率数据
    cpu_usage = [45, 50, 62, 55, 80, 75, 60, 85, 70, 65]
    
    print(f"\nCPU 使用率数据: {cpu_usage}")
    
    # 使用最小最大值窗口
    window = MinMaxSlidingWindow(size=5)
    
    print("\n--- 5 分钟窗口最值追踪 ---")
    print("时间 | CPU | 窗口最小 | 窗口最大")
    print("-" * 40)
    
    for i, usage in enumerate(cpu_usage):
        window.add(usage)
        min_val = window.get_min()
        max_val = window.get_max()
        print(f"{i+1:4} | {usage:3}% | {min_val:6.0f}% | {max_val:6.0f}%")
    
    # 使用便捷函数
    print("\n--- 便捷函数批量计算 ---")
    mins, maxs = sliding_window_min_max(cpu_usage, window=5)
    
    print(f"窗口最小值: {mins}")
    print(f"窗口最大值: {maxs}")
    
    print()


def example_counter():
    """
    示例 6: 滑动窗口计数器
    
    应用场景：
    - 请求计数
    - 错误率监控
    - 活跃用户统计
    """
    print("=" * 60)
    print("示例 6: 滑动窗口计数器")
    print("=" * 60)
    
    # 创建 1 分钟窗口计数器
    counter = SlidingWindowCounter(window_seconds=60, precision=10)
    
    print("\n--- 模拟请求计数 ---")
    
    # 模拟请求
    requests = [1, 1, 2, 1, 3, 1, 2, 1]  # 每次请求的数量
    
    for i, count in enumerate(requests):
        counter.increment(count)
        print(f"时间 {i}s: 增加 {count} 个请求, 当前计数: {counter.get_count()}")
    
    # 查看最终状态
    print(f"\n一分钟内总请求: {counter.get_count()}")
    
    print()


def example_combined_use():
    """
    示例 7: 综合应用 - API 监控系统
    
    应用场景：
    - API 性能监控
    - 异常检测
    - 自动告警
    """
    print("=" * 60)
    print("示例 7: 综合应用 - API 监控系统")
    print("=" * 60)
    
    # 创建监控组件
    response_time_window = NumericSlidingWindow(size=10)  # 10 次请求的响应时间
    error_counter = SlidingWindowCounter(window_seconds=60)  # 1 分钟错误计数
    rate_limiter = RateLimiter(max_requests=100, window_seconds=60)  # 限流器
    min_max_window = MinMaxSlidingWindow(size=10)  # 响应时间最值
    
    print("\n--- 模拟 API 请求 ---")
    
    # 模拟请求（响应时间和是否错误）
    requests = [
        (50, False),
        (45, False),
        (120, False),  # 较慢
        (30, False),
        (200, True),   # 很慢且错误
        (55, False),
        (40, False),
        (500, True),   # 超时错误
        (60, False),
        (35, False),
    ]
    
    print("\n请求 | 响应时间 | 状态 | 窗口均值 | 最小 | 最大 | 错误计数")
    print("-" * 70)
    
    for i, (response_time, is_error) in enumerate(requests):
        # 记录响应时间
        response_time_window.add(response_time)
        min_max_window.add(response_time)
        
        # 记录错误
        if is_error:
            error_counter.increment()
        
        # 获取统计
        stats = response_time_window.get_stats()
        min_rt = min_max_window.get_min()
        max_rt = min_max_window.get_max()
        error_count = error_counter.get_count()
        
        status = "✗ 错误" if is_error else "✓ 正常"
        print(f"{i+1:4} | {response_time:6}ms | {status:8} | {stats.mean:6.1f}ms | {min_rt:5}ms | {max_rt:5}ms | {error_count}")
        
        # 告警检查
        if stats.mean > 100:
            print(f"     ⚠️  告警: 平均响应时间超过 100ms")
        if error_count >= 3:
            print(f"     ⚠️  告警: 1 分钟内错误数达到 {error_count}")
        if max_rt > 300:
            print(f"     ⚠️  告警: 检测到峰值响应时间 {max_rt}ms")
    
    print()


def run_all_examples():
    """运行所有示例"""
    example_moving_average()
    example_rate_limiter()
    example_numeric_window()
    example_time_window()
    example_min_max_window()
    example_counter()
    example_combined_use()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()