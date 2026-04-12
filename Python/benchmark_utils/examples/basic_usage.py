"""
AllToolkit - Benchmark Utils 基础使用示例

演示 benchmark_utils 模块的基本用法。
"""

import sys
import os

# Add parent directory (benchmark_utils) to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from mod import (
    Timer,
    BenchmarkRunner,
    benchmark,
    measure_time,
    time_func,
)


def example_timer():
    """示例 1: 使用 Timer 计时器"""
    print("=" * 60)
    print("示例 1: Timer 计时器")
    print("=" * 60)
    
    # 手动计时
    timer = Timer()
    timer.start()
    
    # 模拟一些工作
    total = sum(range(1000000))
    
    timer.stop()
    print(f"手动计时：{timer.elapsed_ms:.3f}ms, 结果：{total}")
    
    # 使用上下文管理器
    with Timer() as timer:
        total = sum(range(1000000))
    print(f"上下文管理器：{timer.elapsed_ms:.3f}ms, 结果：{total}")
    print()


def example_basic_benchmark():
    """示例 2: 基础基准测试"""
    print("=" * 60)
    print("示例 2: 基础基准测试")
    print("=" * 60)
    
    runner = BenchmarkRunner(warmup_iterations=3, verbose=True)
    
    def simple_sum():
        return sum(range(1000))
    
    def list_comprehension():
        return [i for i in range(1000)]
    
    # 运行基准测试
    result1 = runner.run("simple_sum", simple_sum, iterations=10000)
    result2 = runner.run("list_comp", list_comprehension, iterations=10000)
    
    # 查看详细统计
    print(f"\n详细统计:")
    print(f"  simple_sum - 平均：{result1.avg_time*1000:.4f}ms, "
          f"标准差：{result1.std_dev*1000:.4f}ms")
    print(f"  list_comp  - 平均：{result2.avg_time*1000:.4f}ms, "
          f"标准差：{result2.std_dev*1000:.4f}ms")
    print()


def example_decorator():
    """示例 3: 使用装饰器"""
    print("=" * 60)
    print("示例 3: @benchmark 装饰器")
    print("=" * 60)
    
    @benchmark(name="decorated_function", iterations=5000, warmup=2)
    def my_function():
        """被装饰的函数"""
        return sum(i * i for i in range(100))
    
    # 调用函数（自动运行基准测试）
    result = my_function()
    print(f"函数结果：{result}")
    
    # 查看基准结果
    bench_result = my_function.benchmark_result()
    print(f"基准结果：{bench_result}")
    print()


def example_measure_time():
    """示例 4: 使用 measure_time 上下文管理器"""
    print("=" * 60)
    print("示例 4: measure_time 上下文管理器")
    print("=" * 60)
    
    # 带输出的计时
    with measure_time("数据库查询模拟"):
        # 模拟数据库查询
        total = 0
        for i in range(100000):
            total += i
    
    # 静默计时
    from mod import measure_time_silent
    
    with measure_time_silent() as timer:
        # 模拟耗时操作
        data = list(range(1000000))
        data.sort(reverse=True)
    
    if timer.elapsed > 0.05:  # 超过 50ms
        print(f"⚠️ 警告：操作耗时较长 {timer.elapsed_ms:.1f}ms")
    else:
        print(f"✓ 操作完成 {timer.elapsed_ms:.1f}ms")
    print()


def example_time_func():
    """示例 5: 使用 time_func 快速计时"""
    print("=" * 60)
    print("示例 5: time_func 快速计时")
    print("=" * 60)
    
    def fibonacci(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    # 单次调用
    result, elapsed = time_func(lambda: fibonacci(100), print_result=True)
    print(f"结果：{result}")
    
    # 多次迭代
    _, elapsed = time_func(lambda: fibonacci(50), iterations=1000, print_result=True)
    print(f"1000 次迭代总耗时：{elapsed*1000:.2f}ms")
    print()


def example_with_arguments():
    """示例 6: 带参数的基准测试"""
    print("=" * 60)
    print("示例 6: 带参数的基准测试")
    print("=" * 60)
    
    runner = BenchmarkRunner(warmup_iterations=2, verbose=True)
    
    def multiply(a, b, c=1):
        return a * b * c
    
    # 使用位置参数
    runner.run(
        "multiply_args",
        multiply,
        iterations=10000,
        args=(10, 20),
    )
    
    # 使用关键字参数
    runner.run(
        "multiply_kwargs",
        multiply,
        iterations=10000,
        args=(10, 20),
        kwargs={'c': 2},
    )
    print()


def main():
    """运行所有示例"""
    print("\n" + "🔧 AllToolkit Benchmark Utils 使用示例\n")
    
    example_timer()
    example_basic_benchmark()
    example_decorator()
    example_measure_time()
    example_time_func()
    example_with_arguments()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
