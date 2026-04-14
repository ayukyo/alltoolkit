"""
StopWatch Utils 使用示例

演示秒表计时工具的各种用法。
"""

import time
import asyncio
from mod import (
    StopWatch,
    LapTimer,
    Timer,
    PerformanceTimer,
    StopwatchContext,
    timed,
    timed_async,
    measure_time,
    measure_time_async,
    countdown
)


def example_basic_stopwatch():
    """基本秒表用法示例"""
    print("\n" + "=" * 50)
    print("基本秒表示例")
    print("=" * 50)
    
    # 创建秒表并启动
    sw = StopWatch()
    print(f"初始状态: {sw}")
    
    # 启动计时
    sw.start()
    print("秒表已启动...")
    
    # 模拟一些工作
    time.sleep(0.5)
    print(f"0.5秒后: {sw.elapsed_str()}")
    
    # 暂停
    sw.pause()
    print(f"已暂停: {sw.elapsed_str()}")
    
    # 暂停期间时间不计入
    time.sleep(0.3)
    print(f"暂停0.3秒后仍然是: {sw.elapsed_str()}")
    
    # 恢复
    sw.resume()
    time.sleep(0.2)
    print(f"恢复并等待0.2秒后: {sw.elapsed_str()}")
    
    # 重置
    sw.reset()
    print(f"重置后: {sw}")


def example_context_manager():
    """上下文管理器用法示例"""
    print("\n" + "=" * 50)
    print("上下文管理器示例")
    print("=" * 50)
    
    # 使用 with 语句自动管理
    with StopWatch() as sw:
        print("自动启动计时...")
        time.sleep(0.3)
        print(f"执行中: {sw.elapsed_str()}")
    # 退出时自动暂停
    print(f"退出后: {sw.elapsed_str()}")


def example_lap_timer():
    """圈计时器示例"""
    print("\n" + "=" * 50)
    print("圈计时器示例（模拟跑步比赛）")
    print("=" * 50)
    
    timer = LapTimer(auto_start=True)
    
    # 模拟四圈跑步
    laps = [
        ("第一圈", 0.8),
        ("第二圈", 0.7),
        ("第三圈", 0.9),
        ("第四圈（冲刺）", 0.6)
    ]
    
    for label, duration in laps:
        time.sleep(duration)
        lap = timer.lap(label)
        print(f"  {lap.label}: {lap.lap_time:.2f}s (累计: {lap.total_time:.2f}s)")
    
    # 输出摘要
    print("\n" + timer.summary())


def example_timer_countdown():
    """倒计时器示例"""
    print("\n" + "=" * 50)
    print("倒计时器示例")
    print("=" * 50)
    
    result = []
    
    def on_timeout():
        result.append("时间到!")
        print("🔔 时间到!")
    
    timer = Timer(2.0, callback=on_timeout)
    print("开始2秒倒计时...")
    timer.start()
    
    # 等待完成
    time.sleep(2.5)
    print(f"结果: {result}")


def example_timer_cancel():
    """取消倒计时示例"""
    print("\n" + "=" * 50)
    print("取消倒计时示例")
    print("=" * 50)
    
    def on_timeout():
        print("这不应该打印")
    
    timer = Timer(5.0, callback=on_timeout, auto_start=True)
    print("开始5秒倒计时...")
    
    time.sleep(1)
    remaining = timer.remaining()
    print(f"1秒后剩余: {remaining:.1f}秒")
    
    timer.cancel()
    print("已取消倒计时")


def example_performance_timer():
    """性能计时器示例"""
    print("\n" + "=" * 50)
    print("性能计时器示例")
    print("=" * 50)
    
    # 单次测量
    print("单次测量:")
    with PerformanceTimer("数据库查询模拟"):
        time.sleep(0.1)  # 模拟数据库操作
    
    # 多次测量
    print("\n多次测量:")
    perf = PerformanceTimer("API调用")
    
    for i in range(5):
        with perf.measure():
            # 模拟API调用，每次时间略有不同
            time.sleep(0.05 + i * 0.01)
    
    print(perf.summary())
    
    # 获取统计数据
    stats = perf.statistics()
    print(f"\n统计数据:")
    print(f"  测量次数: {stats['count']}")
    print(f"  总时间: {stats['total']:.4f}s")
    print(f"  平均时间: {stats['average']:.4f}s")
    print(f"  最短时间: {stats['min']:.4f}s")
    print(f"  最长时间: {stats['max']:.4f}s")


def example_timed_decorator():
    """计时装饰器示例"""
    print("\n" + "=" * 50)
    print("计时装饰器示例")
    print("=" * 50)
    
    @timed("数据处理")
    def process_data(size: int) -> list:
        """模拟数据处理"""
        time.sleep(0.1)
        return list(range(size))
    
    @timed(print_result=False)  # 不自动打印
    def silent_operation():
        """静默操作"""
        time.sleep(0.05)
        return "done"
    
    result = process_data(100)
    print(f"返回结果长度: {len(result)}")
    
    result = silent_operation()
    print(f"静默操作结果: {result}")


def example_async_timer():
    """异步计时示例"""
    print("\n" + "=" * 50)
    print("异步计时示例")
    print("=" * 50)
    
    @timed_async("异步操作")
    async def async_operation():
        """异步操作"""
        await asyncio.sleep(0.1)
        return "异步完成"
    
    @timed_async(print_result=False)
    async def silent_async():
        """静默异步操作"""
        await asyncio.sleep(0.05)
        return "静默异步完成"
    
    async def run_async_examples():
        result1 = await async_operation()
        print(f"结果: {result1}")
        
        result2 = await silent_async()
        print(f"静默结果: {result2}")
    
    asyncio.run(run_async_examples())


def example_measure_time():
    """测量函数时间示例"""
    print("\n" + "=" * 50)
    print("测量函数时间示例")
    print("=" * 50)
    
    def complex_calculation(n: int) -> int:
        """复杂计算"""
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    result, elapsed = measure_time(complex_calculation, 10000)
    print(f"计算结果: {result}")
    print(f"耗时: {elapsed * 1000:.3f}ms")


def example_countdown():
    """倒计时函数示例"""
    print("\n" + "=" * 50)
    print("倒计时函数示例")
    print("=" * 50)
    
    print("5秒倒计时开始:")
    countdown(5, callback=lambda s: print(f"  ⏱️ 剩余 {s} 秒..."))
    print("🚀 发射!")


def example_elapsed_units():
    """不同时间单位示例"""
    print("\n" + "=" * 50)
    print("不同时间单位示例")
    print("=" * 50)
    
    sw = StopWatch(auto_start=True)
    time.sleep(0.123)
    
    print(f"秒: {sw.elapsed('seconds'):.6f}")
    print(f"毫秒: {sw.elapsed('milliseconds'):.3f}")
    print(f"微秒: {sw.elapsed('microseconds'):.0f}")
    print(f"分钟: {sw.elapsed('minutes'):.6f}")
    print(f"小时: {sw.elapsed('hours'):.8f}")


def example_simplified_context():
    """简化上下文计时器示例"""
    print("\n" + "=" * 50)
    print("简化上下文计时器示例")
    print("=" * 50)
    
    print("使用简化计时器:")
    with StopwatchContext("简单操作"):
        time.sleep(0.1)
    # 自动打印耗时
    
    print("\n静默模式:")
    with StopwatchContext("静默操作", print_result=False) as ctx:
        time.sleep(0.05)
    print("完成后可以继续其他操作")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("StopWatch Utils - 完整使用示例")
    print("=" * 60)
    
    example_basic_stopwatch()
    example_context_manager()
    example_lap_timer()
    example_timer_countdown()
    example_timer_cancel()
    example_performance_timer()
    example_timed_decorator()
    example_async_timer()
    example_measure_time()
    example_countdown()
    example_elapsed_units()
    example_simplified_context()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()