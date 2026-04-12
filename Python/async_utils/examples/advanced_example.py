#!/usr/bin/env python3
"""
AllToolkit - Async Utils 高级使用示例

演示复杂场景下的 async_utils 应用。
"""

import asyncio
import time
import random
import sys
import os
from typing import List, Dict, Any
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    retry, AsyncRetry, RetryConfig,
    with_timeout, timeout,
    AsyncSemaphoreWithContext as AsyncSemaphore, rate_limit,
    gather_with_results, gather_with_timeout,
    AsyncLockWithContext as AsyncLock,
    AsyncCache, async_cached,
    batch_process, chunked_gather,
    async_map, async_filter, run_concurrently,
    TimeoutError, RetryExhaustedError,
)


# =============================================================================
# 场景 1: 高并发 API 爬虫
# =============================================================================

@dataclass
class CrawlResult:
    url: str
    status: str
    data: Any = None
    error: str = None


class WebCrawler:
    """高并发网页爬虫示例"""
    
    def __init__(self, max_concurrent: int = 10, max_retries: int = 3):
        self.semaphore = AsyncSemaphore(limit=max_concurrent)
        self.cache = AsyncCache(ttl=3600.0, max_size=1000)
        self.retry_config = RetryConfig(
            max_attempts=max_retries,
            initial_delay=0.5,
            max_delay=10.0,
        )
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'cached': 0,
        }
    
    async def fetch_page(self, url: str) -> Dict[str, Any]:
        """模拟网页抓取"""
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # 模拟随机失败
        if random.random() < 0.1:
            raise ConnectionError(f"连接失败：{url}")
        
        return {
            'url': url,
            'title': f"Page: {url}",
            'content': '...' * 100,
            'timestamp': time.time(),
        }
    
    async def crawl_url(self, url: str) -> CrawlResult:
        """爬取单个 URL"""
        self.stats['total'] += 1
        
        # 检查缓存
        cached = await self.cache.get(url)
        if cached:
            self.stats['cached'] += 1
            return CrawlResult(url=url, status='cached', data=cached)
        
        # 带限流和重试的抓取
        retry_executor = AsyncRetry(self.retry_config)
        
        async def fetch_with_retry():
            async with self.semaphore.limit_context():
                return await self.fetch_page(url)
        
        try:
            data = await retry_executor.execute(fetch_with_retry)
            await self.cache.set(url, data)
            self.stats['success'] += 1
            return CrawlResult(url=url, status='success', data=data)
        except Exception as e:
            self.stats['failed'] += 1
            return CrawlResult(url=url, status='failed', error=str(e))
    
    async def crawl_batch(self, urls: List[str]) -> List[CrawlResult]:
        """批量爬取"""
        coros = [self.crawl_url(url) for url in urls]
        
        # 分块处理，避免一次性太多
        return await chunked_gather(
            coros,
            chunk_size=20,
            delay_between_chunks=0.1
        )
    
    def print_stats(self):
        """打印统计"""
        print(f"\n爬取统计:")
        print(f"  总数：{self.stats['total']}")
        print(f"  成功：{self.stats['success']}")
        print(f"  失败：{self.stats['failed']}")
        print(f"  缓存：{self.stats['cached']}")
        if self.stats['total'] > 0:
            print(f"  成功率：{self.stats['success']/self.stats['total']:.2%}")


async def example_crawler():
    """爬虫示例"""
    print("\n=== 高并发爬虫示例 ===")
    
    crawler = WebCrawler(max_concurrent=5, max_retries=2)
    
    # 生成测试 URL
    urls = [f"https://example.com/page/{i}" for i in range(15)]
    
    print(f"开始爬取 {len(urls)} 个页面...")
    start = time.time()
    
    results = await crawler.crawl_batch(urls)
    
    elapsed = time.time() - start
    print(f"完成！耗时：{elapsed:.2f}秒")
    
    # 分析结果
    success = [r for r in results if r.status == 'success']
    cached = [r for r in results if r.status == 'cached']
    failed = [r for r in results if r.status == 'failed']
    
    print(f"  成功：{len(success)}")
    print(f"  缓存：{len(cached)}")
    print(f"  失败：{len(failed)}")
    
    crawler.print_stats()


# =============================================================================
# 场景 2: 数据库连接池管理
# =============================================================================

class DatabasePool:
    """模拟数据库连接池"""
    
    def __init__(self, pool_size: int = 5):
        self.semaphore = AsyncSemaphore(limit=pool_size)
        self.cache = AsyncCache(ttl=60.0)
        self.lock = AsyncLock()
        self.query_count = [0]
    
    async def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """执行查询"""
        cache_key = f"query:{query}:{params}"
        
        # 检查缓存
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        async with self.semaphore.limit_context():
            # 模拟数据库操作
            await asyncio.sleep(0.05)
            self.query_count[0] += 1
            
            # 模拟结果
            result = [
                {'id': i, 'value': f'data_{i}'}
                for i in range(3)
            ]
            
            await self.cache.set(cache_key, result)
            return result
    
    async def transaction(self, operations: List[callable]) -> bool:
        """执行事务（简化版）"""
        async with self.lock.lock_context():
            try:
                for op in operations:
                    await op()
                return True
            except Exception as e:
                print(f"  事务失败：{e}")
                return False
    
    def get_stats(self):
        return {
            'queries': self.query_count[0],
            'cache_size': self.cache.size,
            'cache_hits': self.cache.stats.get('hits', 0),
            'cache_misses': self.cache.stats.get('misses', 0),
        }


async def example_database():
    """数据库示例"""
    print("\n=== 数据库连接池示例 ===")
    
    db = DatabasePool(pool_size=3)
    
    # 并发查询
    async def query_user(user_id):
        return await db.execute_query(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
    
    # 执行多个查询
    coros = [query_user(i) for i in range(10)]
    results = await asyncio.gather(*coros)
    
    print(f"执行了 {len(results)} 个查询")
    
    stats = db.get_stats()
    print(f"  实际查询次数：{stats['queries']}")
    print(f"  缓存命中：{stats['cache_hits']}")
    print(f"  缓存未命中：{stats['cache_misses']}")
    print(f"  缓存大小：{stats['cache_size']}")


# =============================================================================
# 场景 3: 实时数据聚合器
# =============================================================================

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float


class MetricsAggregator:
    """指标聚合器"""
    
    def __init__(self):
        self.cache = AsyncCache(ttl=30.0, max_size=100)
        self.lock = AsyncLock()
        self.aggregated = {}
    
    async def fetch_metric(self, source: str, metric_name: str) -> Metric:
        """从数据源获取指标"""
        cache_key = f"metric:{source}:{metric_name}"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # 模拟获取
        await asyncio.sleep(0.02)
        value = random.uniform(0, 100)
        
        metric = Metric(
            name=metric_name,
            value=value,
            timestamp=time.time()
        )
        
        await self.cache.set(cache_key, metric)
        return metric
    
    async def aggregate(
        self,
        sources: List[str],
        metric_names: List[str]
    ) -> Dict[str, float]:
        """聚合多个源的指标"""
        # 收集所有指标
        coros = []
        for source in sources:
            for name in metric_names:
                coros.append(self.fetch_metric(source, name))
        
        result = await gather_with_results(*coros)
        
        # 按指标名聚合
        aggregated = {}
        for metric in result.successful:
            if metric.name not in aggregated:
                aggregated[metric.name] = []
            aggregated[metric.name].append(metric.value)
        
        # 计算平均值
        return {
            name: sum(values) / len(values)
            for name, values in aggregated.items()
        }
    
    async def update_aggregated(self, averages: Dict[str, float]):
        """更新聚合结果（线程安全）"""
        async with self.lock.lock_context():
            self.aggregated.update(averages)


async def example_aggregator():
    """聚合器示例"""
    print("\n=== 实时数据聚合示例 ===")
    
    aggregator = MetricsAggregator()
    
    sources = ['server1', 'server2', 'server3']
    metrics = ['cpu', 'memory', 'disk']
    
    averages = await aggregator.aggregate(sources, metrics)
    await aggregator.update_aggregated(averages)
    
    print("聚合结果:")
    for name, value in averages.items():
        print(f"  {name}: {value:.2f}")


# =============================================================================
# 场景 4: 任务队列处理器
# =============================================================================

class TaskQueue:
    """任务队列处理器"""
    
    def __init__(self, workers: int = 5):
        self.semaphore = AsyncSemaphore(limit=workers)
        self.queue = asyncio.Queue()
        self.results = {}
        self.lock = AsyncLock()
        self.processed = 0
    
    async def add_task(self, task_id: str, task_data: Any):
        """添加任务"""
        await self.queue.put((task_id, task_data))
    
    async def process_task(self, task_id: str, task_data: Any) -> Any:
        """处理单个任务"""
        # 模拟处理
        await asyncio.sleep(random.uniform(0.05, 0.15))
        return f"result_{task_id}"
    
    async def worker(self, worker_id: int):
        """工作协程"""
        while True:
            try:
                task_id, task_data = await asyncio.wait_for(
                    self.queue.get(),
                    timeout=1.0
                )
            except asyncio.TimeoutError:
                break
            
            async with self.semaphore.limit_context():
                try:
                    result = await self.process_task(task_id, task_data)
                    
                    async with self.lock.lock_context():
                        self.results[task_id] = result
                        self.processed += 1
                    
                    print(f"  Worker {worker_id}: 完成 {task_id}")
                except Exception as e:
                    print(f"  Worker {worker_id}: {task_id} 失败 - {e}")
                
                self.queue.task_done()
    
    async def run(self, tasks: List[tuple]):
        """运行任务队列"""
        # 添加任务
        for task_id, task_data in tasks:
            await self.add_task(task_id, task_data)
        
        # 启动 workers (Python 3.6 兼容)
        workers = [
            asyncio.ensure_future(self.worker(i))
            for i in range(5)
        ]
        
        # 等待队列处理完成
        await self.queue.join()
        
        # 取消 workers
        for w in workers:
            w.cancel()
        
        return self.results


async def example_task_queue():
    """任务队列示例"""
    print("\n=== 任务队列示例 ===")
    
    queue = TaskQueue(workers=5)
    
    # 添加任务
    tasks = [(f"task_{i}", f"data_{i}") for i in range(20)]
    
    start = time.time()
    results = await queue.run(tasks)
    elapsed = time.time() - start
    
    print(f"处理完成！")
    print(f"  总任务：{len(tasks)}")
    print(f"  已处理：{queue.processed}")
    print(f"  耗时：{elapsed:.2f}秒")


# =============================================================================
# 场景 5: 组合装饰器
# =============================================================================

def robust_api_call(
    max_retries: int = 3,
    timeout_sec: float = 10.0,
    rate_limit_n: int = 5,
    cache_ttl: float = 300.0
):
    """组合装饰器：重试 + 超时 + 限流 + 缓存"""
    
    def decorator(func):
        @async_cached(ttl=cache_ttl)
        @rate_limit(limit=rate_limit_n)
        @timeout(timeout=timeout_sec)
        @retry(max_attempts=max_retries)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    
    return decorator


async def example_composed_decorators():
    """组合装饰器示例"""
    print("\n=== 组合装饰器示例 ===")
    
    call_count = [0]
    
    @robust_api_call(
        max_retries=3,
        timeout_sec=5.0,
        rate_limit_n=3,
        cache_ttl=60.0
    )
    async def api_endpoint(endpoint: str):
        call_count[0] += 1
        await asyncio.sleep(0.05)
        
        # 模拟偶尔失败
        if random.random() < 0.2:
            raise ConnectionError("API 不稳定")
        
        return {"endpoint": endpoint, "data": "ok"}
    
    # 多次调用
    results = await asyncio.gather(
        *[api_endpoint(f"/api/{i}") for i in range(5)],
        return_exceptions=True
    )
    
    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    
    print(f"  成功：{len(successes)}")
    print(f"  失败：{len(failures)}")
    print(f"  实际调用：{call_count[0]}")


# =============================================================================
# 主函数
# =============================================================================

async def main():
    """运行所有高级示例"""
    print("=" * 50)
    print("AllToolkit - Async Utils 高级示例")
    print("=" * 50)
    
    await example_crawler()
    await example_database()
    await example_aggregator()
    await example_task_queue()
    await example_composed_decorators()
    
    print("\n" + "=" * 50)
    print("所有高级示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    # Python 3.6 兼容
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
