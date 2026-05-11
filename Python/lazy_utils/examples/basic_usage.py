#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lazy Utils 使用示例
==================

展示各种惰性求值工具的使用方法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Lazy, lazy_property, lazy_class_property, LazySequence,
    Thunk, LazyDict, LazyList, Deferred, lazy, thunk,
    lazy_sequence, lazy_list
)


def example_lazy():
    """Lazy 基本示例"""
    print("\n" + "=" * 50)
    print("示例 1: Lazy 惰性值")
    print("=" * 50)
    
    # 创建一个惰性值
    expensive_config = Lazy(lambda: {
        "database_url": "localhost:5432",
        "api_key": "secret-key",
        "timeout": 30
    })
    
    print(f"创建后状态: {expensive_config}")
    print(f"是否已计算: {expensive_config.is_computed}")
    
    # 首次访问时计算
    config = expensive_config.value
    print(f"首次访问后: {expensive_config}")
    print(f"配置内容: {config}")
    
    # 使用 map 转换
    timeout_lazy = expensive_config.map(lambda c: c["timeout"])
    print(f"超时时间: {timeout_lazy.value}")
    
    # 重置并重新计算
    expensive_config.reset()
    print(f"重置后状态: {expensive_config}")
    print(f"再次访问: {expensive_config.value}")


def example_lazy_property():
    """lazy_property 示例"""
    print("\n" + "=" * 50)
    print("示例 2: lazy_property 惰性属性")
    print("=" * 50)
    
    class DatabaseConnection:
        """数据库连接类，使用惰性属性延迟初始化"""
        
        def __init__(self, host, port):
            self.host = host
            self.port = port
        
        @lazy_property
        def connection(self):
            """延迟创建连接"""
            print(f"正在连接 {self.host}:{self.port}...")
            # 模拟创建连接
            return {"status": "connected", "host": self.host, "port": self.port}
        
        @lazy_property
        def pool(self):
            """延迟创建连接池"""
            print("正在创建连接池...")
            return ["conn1", "conn2", "conn3"]
    
    db = DatabaseConnection("localhost", 5432)
    
    print("创建 DatabaseConnection 对象...")
    print("访问 connection 属性:")
    conn = db.connection  # 首次访问，会打印消息
    print(f"连接状态: {conn}")
    
    print("\n再次访问 connection 属性:")
    conn2 = db.connection  # 不再打印消息，返回缓存
    print(f"连接状态: {conn2}")
    
    print("\n访问 pool 属性:")
    pool = db.pool
    print(f"连接池: {pool}")


def example_lazy_sequence():
    """LazySequence 示例"""
    print("\n" + "=" * 50)
    print("示例 3: LazySequence 惰性序列")
    print("=" * 50)
    
    # 创建无限斐波那契序列
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    fibs = LazySequence(fibonacci)
    
    print("获取斐波那契数列前10项:")
    first_10 = fibs.take(10)
    print(f"前10项: {first_10}")
    
    print("\n获取第20项:")
    fib_20 = fibs[20]
    print(f"F(20) = {fib_20}")
    
    print("\n切片获取第5-10项:")
    slice_result = fibs[5:10]
    print(f"F(5)到F(9): {slice_result}")
    
    # 创建有限序列
    def range_gen(n):
        for i in range(n):
            yield i * 2
    
    doubled = LazySequence(lambda: range_gen(100), length=100)
    print("\n获取有限序列前5项:")
    print(f"{doubled.take(5)}")


def example_thunk():
    """Thunk 示例"""
    print("\n" + "=" * 50)
    print("示例 4: Thunk 延迟计算块")
    print("=" * 50)
    
    # 创建多个 Thunk 并组合
    x = thunk(lambda: 10)
    y = thunk(lambda: 20)
    
    # 组合计算
    sum_thunk = thunk(lambda: x.force() + y.force())
    product_thunk = thunk(lambda: x.value * y.value)
    
    print(f"x 未强制前: {x}")
    print(f"强制 x: {x.force()}")
    print(f"强制 sum: {sum_thunk.force()}")
    print(f"强制 product: {product_thunk.force()}")


def example_lazy_dict():
    """LazyDict 示例"""
    print("\n" + "=" * 50)
    print("示例 5: LazyDict 延迟字典")
    print("=" * 50)
    
    # 创建延迟字典，自动生成缺失键的值
    def default_factory(key):
        print(f"生成键 '{key}' 的默认值...")
        return f"auto-{key}"
    
    cache = LazyDict(default_factory)
    
    print("访问未设置的键:")
    val_a = cache['a']
    print(f"cache['a'] = {val_a}")
    
    print("\n再次访问已生成的键:")
    val_a2 = cache['a']
    print(f"cache['a'] = {val_a2} (不重新生成)")
    
    print("\n预取多个键:")
    cache.prefetch('x', 'y', 'z')
    print(f"预取后访问 'x': {cache['x']} (不重新生成)")
    
    print("\n手动设置值:")
    cache['manual'] = "manual-value"
    print(f"cache['manual'] = {cache['manual']}")


def example_lazy_list():
    """LazyList 示例"""
    print("\n" + "=" * 50)
    print("示例 6: LazyList 惰性列表")
    print("=" * 50)
    
    # 创建惰性列表，每个元素是索引的平方
    squares = LazyList(lambda i: i * i)
    
    print("获取前10个平方数:")
    first_10 = squares[:10]
    print(f"squares[:10] = {first_10}")
    
    print("\n获取第20个元素:")
    square_20 = squares[20]
    print(f"squares[20] = {square_20}")
    
    print("\n追加元素:")
    squares.append(1000)
    print(f"追加后: {squares}")
    
    print("\n转换为普通列表:")
    regular_list = squares.to_list()
    print(f"普通列表前10项: {regular_list[:10]}")


def example_deferred():
    """Deferred 示例"""
    print("\n" + "=" * 50)
    print("示例 7: Deferred 延迟值（带状态）")
    print("=" * 50)
    
    # 模拟耗时操作
    def slow_operation():
        print("执行耗时操作...")
        import time
        time.sleep(1)
        return "操作完成"
    
    d = Deferred(slow_operation)
    
    print(f"初始状态: pending={d.is_pending}")
    
    # 添加回调
    d.on_complete(lambda v: print(f"完成回调: {v}"))
    d.on_error(lambda e: print(f"错误回调: {e}"))
    
    print("获取值:")
    result = d.get()
    print(f"结果: {result}")
    print(f"完成状态: completed={d.is_completed}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("示例 8: 便捷函数")
    print("=" * 50)
    
    # lazy() - 快速创建惰性值
    config = lazy(lambda: {"version": "1.0"})
    print(f"lazy() 创建: {config.value}")
    
    # thunk() - 快速创建 Thunk
    computation = thunk(lambda: 42 * 2)
    print(f"thunk() 创建: {computation.force()}")
    
    # lazy_sequence() - 快速创建惰性序列
    naturals = lazy_sequence(lambda: (i for i in range(10)))
    print(f"lazy_sequence() 前5项: {naturals.take(5)}")
    
    # lazy_list() - 快速创建惰性列表
    cubes = lazy_list(lambda i: i ** 3)
    print(f"lazy_list() 前5项: {cubes[:5]}")


def example_performance():
    """性能优化示例"""
    print("\n" + "=" * 50)
    print("示例 9: 性能优化场景")
    print("=" * 50)
    
    import time
    
    # 场景1：避免初始化时的昂贵计算
    class HeavyService:
        @lazy_property
        def database(self):
            print("初始化数据库连接...")
            time.sleep(0.5)
            return "DB Connection"
        
        @lazy_property  
        def cache(self):
            print("初始化缓存...")
            time.sleep(0.5)
            return "Cache Connection"
        
        @lazy_property
        def logger(self):
            print("初始化日志...")
            time.sleep(0.5)
            return "Logger Connection"
    
    print("创建 HeavyService...")
    start = time.time()
    service = HeavyService()
    init_time = time.time() - start
    print(f"创建耗时: {init_time:.3f}s (延迟初始化，无等待)")
    
    print("\n首次使用数据库:")
    start = time.time()
    db = service.database
    use_time = time.time() - start
    print(f"首次访问耗时: {use_time:.3f}s")
    
    print("\n后续使用:")
    start = time.time()
    db2 = service.database
    print(f"后续访问耗时: {time.time() - start:.3f}s (无延迟)")
    
    # 场景2：大型数据按需加载
    print("\n按需加载大数据:")
    
    def large_data_generator():
        """模拟生成大量数据"""
        for i in range(1000000):
            yield {"id": i, "data": f"item-{i}"}
    
    data_stream = LazySequence(large_data_generator, cache=False)
    
    print("只取前10条数据，避免加载全部:")
    first_10 = data_stream.take(10)
    print(f"前10条: {first_10[:3]}... (共{len(first_10)}条)")


def example_infinite_sequence():
    """无限序列示例"""
    print("\n" + "=" * 50)
    print("示例 10: 无限数据结构")
    print("=" * 50)
    
    # 无限自然数序列
    def naturals():
        n = 0
        while True:
            yield n
            n += 1
    
    natural_seq = LazySequence(naturals)
    
    print("无限自然数序列:")
    print(f"前10个自然数: {natural_seq.take(10)}")
    print(f"第100个自然数: {natural_seq[100]}")
    
    # 无限素数序列
    def primes():
        """素数生成器"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        n = 2
        while True:
            if is_prime(n):
                yield n
            n += 1
    
    prime_seq = LazySequence(primes)
    
    print("\n无限素数序列:")
    print(f"前10个素数: {prime_seq.take(10)}")
    print(f"第50个素数: {prime_seq[50]}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Lazy Utils - 使用示例")
    print("=" * 60)
    
    example_lazy()
    example_lazy_property()
    example_lazy_sequence()
    example_thunk()
    example_lazy_dict()
    example_lazy_list()
    example_deferred()
    example_convenience_functions()
    example_performance()
    example_infinite_sequence()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()