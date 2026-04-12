#!/usr/bin/env python3
"""
AllToolkit - Async Utils 基础使用示例

演示 async_utils 模块的核心功能。
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    retry, AsyncRetry, RetryConfig,
    with_timeout, timeout,
    AsyncSemaphoreWithContext as AsyncSemaphore, rate_limit,
    gather_with_results, gather_with_timeout,
    AsyncLockWithContext as AsyncLock,
    AsyncCache, async_cached,
    batch_process, chunked_gather,
    async_map, async_filter,
    TimeoutError, RetryExhaustedError,
)


# =============================================================================
# 1. 重试示例
# =============================================================================

async def example_retry():
    """重试功能示例"""
    print("\n=== 重试示例 ===")
    
    attempt_count = [0]
    
    @retry(
        max_attempts=3,
        initial_delay=0.5,
        jitter=True
    )
    async def flaky_operation():
        attempt_count[0] += 1
        print(f"  尝试 {attempt_count[0]}...")
        if attempt_count[0] < 3:
            raise ConnectionError("网络不稳定")
        return "成功！"
    
    try:
        result = await flaky_operation()
        print(f"  结果：{result}")
    except RetryExhaustedError as e:
        print(f"  重试耗尽：{e}")


# =============================================================================
# 2. 超时示例
# =============================================================================

async def example_timeout():
    """超时功能示例"""
    print("\n=== 超时示例 ===")
    
    async def slow_operation():
        await asyncio.sleep(2)
        return "完成"
    
    try:
        # 设置 0.5 秒超时
        result = await with_timeout(slow_operation(), timeout=0.5)
        print(f"  结果：{result}")
    except TimeoutError as e:
        print(f"  超时：{e}")
    
    # 快速操作不会超时
    async def fast_operation():
        await asyncio.sleep(0.1)
        return "快速完成"
    
    result = await with_timeout(fast_operation(), timeout=1.0)
    print(f"  快速操作：{result}")


# =============================================================================
# 3. 限流示例
# =============================================================================

async def example_rate_limit():
    """限流功能示例"""
    print("\n=== 限流示例 ===")
    
    semaphore = AsyncSemaphore(limit=3)
    
    async def task(id):
        async with semaphore.limit_context():
            print(f"  任务 {id} 开始")
            await asyncio.sleep(0.5)
            print(f"  任务 {id} 完成")
            return id
    
    # 同时启动 5 个任务，但最多 3 个并发
    await asyncio.gather(*[task(i) for i in range(5)])


# =============================================================================
# 4. 并发收集示例
# =============================================================================

async def example_gather():
    """并发收集示例"""
    print("\n=== 并发收集示例 ===")
    
    async def success_task(n):
        await asyncio.sleep(0.1)
        return n * 2
    
    async def fail_task():
        await asyncio.sleep(0.1)
        raise ValueError("失败了")
    
    result = await gather_with_results(
        success_task(1),
        fail_task(),
        success_task(3),
        success_task(4),
    )
    
    print(f"  总数：{result.total}")
    print(f"  成功：{len(result.successful)} -> {result.successful}")
    print(f"  失败：{len(result.failed)}")
    print(f"  成功率：{result.success_rate:.2%}")
    
    for idx, exc in result.failed:
        print(f"    任务 {idx} 失败：{exc}")


# =============================================================================
# 5. 异步锁示例
# =============================================================================

async def example_lock():
    """异步锁示例"""
    print("\n=== 异步锁示例 ===")
    
    lock = AsyncLock()
    counter = [0]
    
    async def increment():
        async with lock.lock_context():
            current = counter[0]
            await asyncio.sleep(0.01)  # 模拟操作
            counter[0] = current + 1
            print(f"  计数器：{counter[0]}")
    
    # 并发增加，但锁保证原子性
    await asyncio.gather(*[increment() for _ in range(5)])
    print(f"  最终值：{counter[0]}")


# =============================================================================
# 6. 异步缓存示例
# =============================================================================

async def example_cache():
    """异步缓存示例"""
    print("\n=== 异步缓存示例 ===")
    
    call_count = [0]
    
    @async_cached(ttl=10.0, max_size=100)
    async def expensive_query(user_id):
        call_count[0] += 1
        await asyncio.sleep(0.1)  # 模拟耗时
        return {"id": user_id, "name": f"User_{user_id}"}
    
    # 第一次：实际查询
    user1 = await expensive_query(1)
    print(f"  第一次查询用户 1: {user1}")
    
    # 第二次：缓存命中
    user1_cached = await expensive_query(1)
    print(f"  第二次查询用户 1（缓存）: {user1_cached}")
    
    # 不同参数：新查询
    user2 = await expensive_query(2)
    print(f"  查询用户 2: {user2}")
    
    print(f"  实际调用次数：{call_count[0]}")


# =============================================================================
# 7. 批量处理示例
# =============================================================================

async def example_batch():
    """批量处理示例"""
    print("\n=== 批量处理示例 ===")
    
    async def process_item(item):
        await asyncio.sleep(0.05)
        return item * 2
    
    items = list(range(10))
    
    # 每批 3 个，并发 2 个
    results = await batch_process(
        items,
        process_item,
        batch_size=3,
        concurrency=2
    )
    
    print(f"  输入：{items}")
    print(f"  输出：{results}")


# =============================================================================
# 8. Async Map/Filter 示例
# =============================================================================

async def example_map_filter():
    """异步 Map/Filter 示例"""
    print("\n=== Map/Filter 示例 ===")
    
    async def square(x):
        await asyncio.sleep(0.01)
        return x ** 2
    
    async def is_even(x):
        await asyncio.sleep(0.01)
        return x % 2 == 0
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Map
    squares = await async_map(square, numbers, concurrency=5)
    print(f"  平方：{squares}")
    
    # Filter
    evens = await async_filter(is_even, numbers, concurrency=5)
    print(f"  偶数：{evens}")


# =============================================================================
# 主函数
# =============================================================================

async def main():
    """运行所有示例"""
    print("=" * 50)
    print("AllToolkit - Async Utils 基础示例")
    print("=" * 50)
    
    await example_retry()
    await example_timeout()
    await example_rate_limit()
    await example_gather()
    await example_lock()
    await example_cache()
    await example_batch()
    await example_map_filter()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    # Python 3.6 兼容
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
