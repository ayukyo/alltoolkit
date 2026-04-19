"""
滑动窗口统计工具使用示例

演示各种滑动窗口数据结构和统计计算的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import random
from mod import (
    SlidingWindowMax, SlidingWindowMin, SlidingWindowStats,
    SlidingWindowMedian, SlidingWindowPercentile, TimeWindowStats,
    SlidingWindowCounter,
    sliding_max, sliding_min, sliding_mean, sliding_sum, sliding_median
)


def example_sliding_max_min():
    """示例：滑动窗口最大值和最小值"""
    print("=" * 60)
    print("示例 1: 滑动窗口最大值和最小值")
    print("=" * 60)
    
    # 股票价格模拟
    stock_prices = [100, 105, 102, 108, 107, 103, 110, 115, 112, 118]
    window_size = 3
    
    print(f"\n股票价格: {stock_prices}")
    print(f"窗口大小: {window_size}")
    
    max_values = sliding_max(stock_prices, window_size)
    min_values = sliding_min(stock_prices, window_size)
    
    print("\n价格 | 窗口最大 | 窗口最小")
    print("-" * 35)
    for i, price in enumerate(stock_prices):
        print(f"{price:4} | {max_values[i]:8} | {min_values[i]:8}")
    
    print("\n应用场景：股票技术分析中的支撑位和压力位计算")


def example_sliding_stats():
    """示例：滑动窗口统计计算"""
    print("\n" + "=" * 60)
    print("示例 2: 滑动窗口统计计算")
    print("=" * 60)
    
    # 服务器响应时间模拟（毫秒）
    response_times = [50, 45, 60, 55, 70, 65, 80, 75, 90, 85, 100, 95]
    window_size = 5
    
    print(f"\n响应时间 (ms): {response_times}")
    print(f"窗口大小: {window_size}")
    
    stats = SlidingWindowStats(window_size)
    
    print("\n响应时间 | 平均值 | 最小值 | 最大值 | 标准差")
    print("-" * 55)
    
    for rt in response_times:
        stats.push(rt)
        mean = stats.mean()
        min_val = stats.min()
        max_val = stats.max()
        std = stats.std_dev()
        
        if mean is not None:
            print(f"{rt:8} | {mean:6.1f} | {min_val:6.1f} | {max_val:6.1f} | {std:6.1f}")
    
    print("\n应用场景：实时性能监控、异常检测（标准差超过阈值时报警）")


def example_sliding_median():
    """示例：滑动窗口中位数"""
    print("\n" + "=" * 60)
    print("示例 3: 滑动窗口中位数")
    print("=" * 60)
    
    # 网络延迟数据（毫秒）
    latencies = [20, 22, 25, 100, 23, 24, 21, 150, 22, 23]
    window_size = 5
    
    print(f"\n网络延迟 (ms): {latencies}")
    print(f"窗口大小: {window_size}")
    
    print("\n延迟 | 中位数 | 说明")
    print("-" * 50)
    
    swm = SlidingWindowMedian(window_size)
    for lat in latencies:
        swm.push(lat)
        median = swm.median()
        note = "异常高" if lat > 50 else "正常"
        print(f"{lat:4} | {median:6.1f} | {note}")
    
    print("\n应用场景：中位数比平均值更抗异常值，适合网络延迟监控")


def example_sliding_percentile():
    """示例：滑动窗口百分位数"""
    print("\n" + "=" * 60)
    print("示例 4: 滑动窗口百分位数")
    print("=" * 60)
    
    # API 响应时间
    response_times = list(range(10, 101, 10))  # 10, 20, 30, ..., 100
    window_size = 10
    
    print(f"\n响应时间 (ms): {response_times}")
    print(f"窗口大小: {window_size}")
    
    # 计算 P50, P90, P95, P99
    percentiles = [50, 90, 95, 99]
    swp = SlidingWindowPercentile(window_size)
    
    for rt in response_times:
        swp.push(rt)
    
    print("\n百分位数统计:")
    print("-" * 30)
    for p in percentiles:
        swp.set_percentile(p)
        print(f"P{p:2}: {swp.percentile_value():.1f} ms")
    
    print("\n应用场景：SLA 监控，如 '99% 的请求响应时间低于 100ms'")


def example_time_window():
    """示例：时间窗口统计"""
    print("\n" + "=" * 60)
    print("示例 5: 时间窗口统计（实时数据流）")
    print("=" * 60)
    
    # 模拟实时数据流
    tws = TimeWindowStats(window_seconds=5)
    
    print("\n模拟 10 秒的数据流，5 秒时间窗口")
    print("-" * 50)
    
    now = time.time()
    
    # 添加历史数据（将被清理）
    tws.push(now - 10, 100)
    print(f"[-10s] 添加 100 → 窗口计数: {tws.count()} (过期数据被清理)")
    
    # 添加有效数据
    for i in range(10):
        ts = now - (9 - i)
        value = random.randint(50, 150)
        tws.push(ts, value)
        tws.refresh(now)  # 刷新过期数据
        
        print(f"[{i-8}s] 添加 {value:3} → 计数: {tws.count()}, "
              f"平均: {tws.mean():.1f if tws.mean() else 'N/A'}, "
              f"速率: {tws.rate(now):.2f}/s" if tws.rate(now) else "")
    
    print("\n应用场景：实时监控、滑动窗口限流、实时统计")


def example_counter():
    """示例：滑动窗口计数器"""
    print("\n" + "=" * 60)
    print("示例 6: 滑动窗口计数器")
    print("=" * 60)
    
    # HTTP 状态码监控
    status_codes = [200, 200, 404, 200, 500, 200, 200, 404, 200, 500, 200, 200]
    window_size = 5
    
    counter = SlidingWindowCounter(window_size)
    
    print(f"\nHTTP 状态码: {status_codes}")
    print(f"窗口大小: {window_size}")
    
    print("\n状态码 | 窗口内 200 | 404 | 500 | 总数 | 唯一数")
    print("-" * 55)
    
    for code in status_codes:
        counter.push(code)
        print(f"{code:6} | {counter.count(200):10} | {counter.count(404):3} | "
              f"{counter.count(500):3} | {counter.total():4} | {counter.unique_count():6}")
    
    # 最常见状态码
    most_common = counter.most_common(3)
    print(f"\n最常见状态码: {most_common}")
    
    print("\n应用场景：错误率监控、限流、热点分析")


def example_performance_monitoring():
    """示例：综合性能监控"""
    print("\n" + "=" * 60)
    print("示例 7: 综合性能监控面板")
    print("=" * 60)
    
    # 模拟 30 秒的性能数据
    window_size = 10
    
    max_monitor = SlidingWindowMax(window_size)
    min_monitor = SlidingWindowMin(window_size)
    stats_monitor = SlidingWindowStats(window_size)
    median_monitor = SlidingWindowMedian(window_size)
    p95_monitor = SlidingWindowPercentile(window_size, percentile=95)
    
    print(f"\n模拟 30 个数据点的性能监控（窗口大小: {window_size}）")
    print("-" * 70)
    print("数据  | 最大 | 最小 | 平均 | 中位数 | P95  | 标准差 | 状态")
    print("-" * 70)
    
    random.seed(42)  # 固定随机种子以便复现
    
    for i in range(30):
        # 生成模拟数据，偶尔有峰值
        if random.random() < 0.1:
            value = random.randint(200, 300)  # 异常峰值
        else:
            value = random.randint(40, 80)  # 正常范围
        
        max_monitor.push(value)
        min_monitor.push(value)
        stats_monitor.push(value)
        median_monitor.push(value)
        p95_monitor.push(value)
        
        max_val = max_monitor.max()
        min_val = min_monitor.min()
        mean = stats_monitor.mean()
        median = median_monitor.median()
        p95 = p95_monitor.percentile_value()
        std = stats_monitor.std_dev()
        
        # 判断状态
        if mean and mean > 100:
            status = "⚠️ 警告"
        elif std and std > 50:
            status = "📊 波动大"
        else:
            status = "✅ 正常"
        
        print(f"{value:4}  | {max_val:4} | {min_val:4} | "
              f"{mean:5.1f} | {median:6.1f} | {p95:5.1f} | "
              f"{std:6.1f} | {status}")
    
    print("\n应用场景：APM 系统中的实时性能监控仪表板")


def example_rate_limiting():
    """示例：基于滑动窗口的限流"""
    print("\n" + "=" * 60)
    print("示例 8: API 限流检查器")
    print("=" * 60)
    
    class RateLimiter:
        """简单的滑动窗口限流器"""
        
        def __init__(self, max_requests: int, window_size: int):
            self.max_requests = max_requests
            self.window_size = window_size
            self.counter = SlidingWindowCounter(window_size)
        
        def check(self, user_id: str) -> tuple:
            """
            检查请求是否允许
            
            Returns:
                (allowed: bool, remaining: int, reset_in: int)
            """
            # 模拟：每次请求都传入 user_id 作为 key
            current_count = self.counter.count(user_id)
            
            if current_count >= self.max_requests:
                # 计算需要等待的位置
                return False, 0, self.window_size
            
            self.counter.push(user_id)
            remaining = self.max_requests - self.counter.count(user_id)
            
            return True, remaining, 0
    
    # 创建限流器：每分钟最多 5 次请求
    limiter = RateLimiter(max_requests=5, window_size=10)
    
    print("\n模拟用户请求（每分钟最多 5 次请求，窗口大小 10）")
    print("-" * 50)
    
    for i in range(12):
        allowed, remaining, reset_in = limiter.check("user_123")
        status = "✅ 通过" if allowed else "❌ 拒绝"
        print(f"请求 {i+1:2}: {status} | 剩余配额: {remaining}")
    
    print("\n应用场景：API 网关限流、防止 DDoS 攻击")


def example_stock_analysis():
    """示例：股票技术指标分析"""
    print("\n" + "=" * 60)
    print("示例 9: 股票技术指标计算")
    print("=" * 60)
    
    # 模拟股价数据
    prices = [
        100.0, 101.5, 102.3, 101.8, 103.2,  # 5 天
        104.1, 103.5, 105.2, 106.0, 105.5,  # 10 天
        107.3, 108.1, 107.8, 109.2, 110.5   # 15 天
    ]
    
    window_size = 5
    
    # MA5 (5 日移动平均线)
    ma5 = sliding_mean(prices, window_size)
    
    # 布林带（需要标准差）
    stats = SlidingWindowStats(window_size)
    upper_band = []
    lower_band = []
    
    for price in prices:
        stats.push(price)
        mean = stats.mean()
        std = stats.std_dev()
        if mean is not None and std is not None:
            upper_band.append(mean + 2 * std)
            lower_band.append(mean - 2 * std)
        else:
            upper_band.append(None)
            lower_band.append(None)
    
    print(f"\n股价数据: {prices}")
    print(f"窗口大小: {window_size}")
    print("\n天数 | 价格   | MA5    | 布林上轨 | 布林下轨")
    print("-" * 55)
    
    for i, price in enumerate(prices):
        ma = ma5[i]
        upper = upper_band[i]
        lower = lower_band[i]
        print(f"{i+1:3}  | {price:6.2f} | {ma:6.2f} | "
              f"{upper:8.2f} | {lower:8.2f}" if upper else
              f"{i+1:3}  | {price:6.2f} | {ma:6.2f} |    N/A   |    N/A")
    
    print("\n应用场景：量化交易、技术分析、算法交易")


def main():
    """运行所有示例"""
    example_sliding_max_min()
    example_sliding_stats()
    example_sliding_median()
    example_sliding_percentile()
    example_time_window()
    example_counter()
    example_performance_monitoring()
    example_rate_limiting()
    example_stock_analysis()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()