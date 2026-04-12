# AllToolkit - Python Async Utils ⚡

**零依赖异步编程工具 - 生产就绪**

---

## 📖 概述

`async_utils` 提供完整的异步编程工具集，包括重试、超时、限流、并发控制、缓存等功能。完全使用 Python 标准库 `asyncio` 实现，无需任何外部依赖。

适用于需要高并发、容错、性能优化的异步应用场景。

---

## ✨ 特性

- **智能重试** - 指数退避 + 抖动，可配置重试策略
- **超时控制** - 协程级超时保护
- **并发限流** - 信号量控制并发数
- **增强收集** - 带详细结果的并发收集
- **异步锁** - 带超时和统计的锁
- **结果缓存** - 异步函数结果缓存
- **批量处理** - 分块批量处理工具
- **工具函数** - async_map, async_filter, run_concurrently

---

## 🚀 快速开始

### 基础重试

```python
from mod import retry, AsyncRetry, RetryConfig

# 使用装饰器
@retry(max_attempts=3, initial_delay=1.0)
async def fetch_data(url):
    # 可能失败的操作
    return data

# 使用类
async def run():
    retry_executor = AsyncRetry()
    result = await retry_executor.execute(fetch_data, "https://api.example.com")
```

### 超时控制

```python
from mod import with_timeout, timeout, TimeoutError

# 使用函数
async def run():
    try:
        result = await with_timeout(slow_operation(), timeout=5.0)
    except TimeoutError:
        print("操作超时")

# 使用装饰器
@timeout(timeout=10.0)
async def must_complete_quickly():
    ...
```

### 并发限流

```python
from mod import AsyncSemaphore, rate_limit

# 使用信号量
semaphore = AsyncSemaphore(limit=10)

async def limited_task():
    async with semaphore.limit_context():
        # 同时最多 10 个任务执行
        await do_work()

# 使用装饰器
@rate_limit(limit=5)
async def api_call():
    ...
```

### 异步缓存

```python
from mod import async_cached, AsyncCache

# 使用装饰器
@async_cached(ttl=300.0, max_size=100)
async def expensive_query(user_id):
    # 耗时操作，结果会被缓存
    return await db.query(user_id)

# 使用类
cache = AsyncCache(ttl=60.0)
await cache.set("key", "value")
value = await cache.get("key")
```

---

## 📚 API 参考

### 重试模块

| 类/函数 | 描述 |
|---------|------|
| `RetryConfig` | 重试配置数据类 |
| `AsyncRetry` | 重试执行器类 |
| `@retry` | 重试装饰器 |

#### RetryConfig 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `max_attempts` | int | 3 | 最大重试次数 |
| `initial_delay` | float | 1.0 | 初始延迟（秒） |
| `max_delay` | float | 60.0 | 最大延迟（秒） |
| `exponential_base` | float | 2.0 | 指数退避基数 |
| `jitter` | bool | True | 是否添加抖动 |
| `jitter_factor` | float | 0.1 | 抖动因子 |
| `retryable_exceptions` | tuple | (Exception,) | 可重试的异常类型 |

### 超时模块

| 函数/装饰器 | 描述 |
|-------------|------|
| `with_timeout(coro, timeout)` | 带超时的协程执行 |
| `@timeout(timeout)` | 超时装饰器 |

### 限流模块

| 类/装饰器 | 描述 |
|-----------|------|
| `AsyncSemaphore` | 异步信号量 |
| `@rate_limit(limit, timeout)` | 速率限制装饰器 |

#### AsyncSemaphore 方法

| 方法 | 描述 | 返回 |
|------|------|------|
| `acquire()` | 获取信号量 | `bool` |
| `release()` | 释放信号量 | `None` |
| `limit_context()` | 上下文管理器 | `AsyncContextManager` |

### 并发模块

| 函数 | 描述 | 返回 |
|------|------|------|
| `gather_with_results(*coros)` | 增强并发收集 | `GatherResult` |
| `gather_with_timeout(*coros, timeout)` | 带超时并发收集 | `GatherResult` |

#### GatherResult 属性

| 属性 | 描述 |
|------|------|
| `successful` | 成功结果列表 |
| `failed` | 失败列表 `(index, exception)` |
| `total` | 总任务数 |
| `success_rate` | 成功率 (0.0-1.0) |

### 锁模块

| 类 | 描述 |
|----|------|
| `AsyncLock` | 带超时和统计的异步锁 |

### 缓存模块

| 类/装饰器 | 描述 |
|-----------|------|
| `AsyncCache` | 异步缓存类 |
| `@async_cached(ttl, max_size)` | 异步缓存装饰器 |

#### AsyncCache 方法

| 方法 | 描述 |
|------|------|
| `get(key)` | 获取缓存 |
| `set(key, value, ttl)` | 设置缓存 |
| `clear()` | 清空缓存 |
| `size` | 当前缓存大小 |
| `stats` | 统计信息 |
| `hit_rate` | 命中率 |

### 批量处理

| 函数 | 描述 |
|------|------|
| `batch_process(items, processor, batch_size, concurrency)` | 批量处理 |
| `chunked_gather(coros, chunk_size, delay)` | 分块并发 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `async_map(func, items, concurrency)` | 异步 map |
| `async_filter(predicate, items, concurrency)` | 异步 filter |
| `run_concurrently(*coros, limit)` | 限制并发执行 |

---

## 🎯 使用场景

### 1. API 调用重试

```python
from mod import retry
import aiohttp

@retry(
    max_attempts=5,
    initial_delay=0.5,
    max_delay=30.0,
    retryable_exceptions=(aiohttp.ClientError,)
)
async def fetch_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
```

### 2. 数据库连接池限流

```python
from mod import AsyncSemaphore

db_semaphore = AsyncSemaphore(limit=10)  # 最多 10 个并发连接

async def query_database(sql):
    async with db_semaphore.limit_context():
        async with get_db_connection() as conn:
            return await conn.execute(sql)
```

### 3. 爬虫速率限制

```python
from mod import rate_limit

@rate_limit(limit=5, timeout=60.0)  # 每秒最多 5 个请求
async def crawl_page(url):
    # 爬取逻辑
    pass

# 批量爬取
urls = [...]
await asyncio.gather(*[crawl_page(url) for url in urls])
```

### 4. 函数结果缓存

```python
from mod import async_cached

@async_cached(ttl=3600.0, max_size=1000)
async def get_user_profile(user_id):
    # 耗时数据库查询
    return await db.users.find_one({"_id": user_id})

# 第一次：执行查询
profile = await get_user_profile("123")

# 一小时内：直接返回缓存
profile = await get_user_profile("123")
```

### 5. 批量数据处理

```python
from mod import batch_process

async def process_item(item):
    # 处理单个项目
    return transform(item)

items = [...]  # 大量数据

# 每批 100 个，并发 20 个
results = await batch_process(
    items,
    process_item,
    batch_size=100,
    concurrency=20
)
```

### 6. 带详细结果的并发

```python
from mod import gather_with_results

async def fetch_user(user_id):
    # 可能失败
    return await api.get_user(user_id)

user_ids = [1, 2, 3, 4, 5]
coros = [fetch_user(uid) for uid in user_ids]

result = await gather_with_results(*coros)

print(f"成功：{len(result.successful)}")
print(f"失败：{len(result.failed)}")
print(f"成功率：{result.success_rate:.2%}")

for idx, exc in result.failed:
    print(f"用户 {user_ids[idx]} 失败：{exc}")
```

### 7. 多级缓存

```python
from mod import AsyncCache

# L1: 热数据缓存
l1_cache = AsyncCache(ttl=60.0, max_size=100)

# L2: 温数据缓存
l2_cache = AsyncCache(ttl=3600.0, max_size=1000)

async def get_multi_level(key):
    # 先查 L1
    value = await l1_cache.get(key)
    if value is not None:
        return value, "L1"
    
    # 再查 L2
    value = await l2_cache.get(key)
    if value is not None:
        await l1_cache.set(key, value)  # 提升到 L1
        return value, "L2"
    
    # 从数据源加载
    value = await load_from_source(key)
    await l2_cache.set(key, value)
    return value, "SOURCE"
```

### 8. 异步 Map/Filter

```python
from mod import async_map, async_filter

# 异步 map
async def fetch_price(product_id):
    return await api.get_price(product_id)

product_ids = [1, 2, 3, 4, 5]
prices = await async_map(fetch_price, product_ids, concurrency=3)

# 异步 filter
async def is_available(product_id):
    stock = await api.get_stock(product_id)
    return stock > 0

available_ids = await async_filter(is_available, product_ids)
```

---

## 🧪 运行测试

```bash
cd async_utils
python async_utils_test.py -v
```

### 测试覆盖

- ✅ RetryConfig 配置
- ✅ AsyncRetry 执行器
- ✅ @retry 装饰器
- ✅ with_timeout 超时
- ✅ @timeout 装饰器
- ✅ AsyncSemaphore 信号量
- ✅ @rate_limit 限流
- ✅ gather_with_results 并发收集
- ✅ gather_with_timeout 超时收集
- ✅ AsyncLock 异步锁
- ✅ AsyncCache 缓存
- ✅ @async_cached 装饰器
- ✅ batch_process 批量处理
- ✅ chunked_gather 分块收集
- ✅ async_map/async_filter 工具
- ✅ 集成测试
- ✅ 边界情况
- ✅ 性能测试

---

## 📊 统计监控

### 重试统计

```python
retry_executor = AsyncRetry()
await retry_executor.execute(some_func)

stats = retry_executor.stats
print(f"总尝试：{stats['total_attempts']}")
print(f"成功：{stats['successful']}")
print(f"失败：{stats['failed']}")
print(f"重试：{stats['retries']}")
```

### 信号量统计

```python
semaphore = AsyncSemaphore(limit=10)

# 使用后...
stats = semaphore.stats
print(f"获取：{stats['total_acquires']}")
print(f"释放：{stats['total_releases']}")
print(f"超时：{stats['timeouts']}")
print(f"当前持有：{stats['current_held']}")
print(f"可用：{semaphore.available}")
```

### 缓存统计

```python
cache = AsyncCache()

# 使用后...
stats = cache.stats
print(f"命中：{stats['hits']}")
print(f"未命中：{stats['misses']}")
print(f"命中率：{cache.hit_rate:.2%}")
print(f"设置：{stats['sets']}")
print(f"淘汰：{stats['evictions']}")
```

---

## ⚠️ 注意事项

1. **异常处理**: 重试会捕获指定异常，确保正确设置 `retryable_exceptions`
2. **超时精度**: 基于 asyncio.wait_for，精度约毫秒级
3. **缓存 None**: 缓存 None 值会被视为未命中（设计选择）
4. **内存限制**: 缓存存储在内存中，注意 max_size 设置
5. **线程安全**: asyncio 是单线程的，但要注意跨协程共享状态
6. **资源清理**: 使用上下文管理器确保资源正确释放

---

## 🔧 配置示例

### 激进重试（快速失败场景）

```python
@retry(
    max_attempts=3,
    initial_delay=0.1,
    max_delay=1.0,
    jitter=True
)
async def quick_retry_api():
    ...
```

### 保守重试（重要操作）

```python
@retry(
    max_attempts=10,
    initial_delay=2.0,
    max_delay=120.0,
    exponential_base=1.5,
    retryable_exceptions=(ConnectionError, TimeoutError)
)
async def critical_operation():
    ...
```

### 严格限流（API 配额）

```python
@rate_limit(limit=2, timeout=30.0)  # 严格限制
async def quota_limited_api():
    ...
```

### 宽松缓存（读多写少）

```python
@async_cached(ttl=86400.0, max_size=10000)  # 24 小时缓存
async def rarely_changes_data():
    ...
```

---

## 📁 文件结构

```
async_utils/
├── mod.py                      # 主要实现
├── async_utils_test.py         # 测试套件 (80+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 💡 最佳实践

### 1. 组合使用工具

```python
@async_cached(ttl=300.0)
@retry(max_attempts=3)
@rate_limit(limit=10)
async def optimized_api_call(param):
    return await api.call(param)
```

### 2. 监控重试率

```python
if retry_executor.stats['retries'] > retry_executor.stats['successful']:
    logger.warning("重试率过高，可能需要检查服务健康")
```

### 3. 合理设置缓存 TTL

```python
# 频繁变化：短 TTL
@async_cached(ttl=60.0)
async def get_stock_price(): ...

# 稳定数据：长 TTL
@async_cached(ttl=86400.0)
async def get_product_info(): ...
```

### 4. 批量处理优化

```python
# 根据下游承受能力调整
results = await batch_process(
    items,
    processor,
    batch_size=50,      # 每批 50 个
    concurrency=10      # 同时 10 个
)
```

### 5. 优雅降级

```python
from mod import gather_with_results

result = await gather_with_results(*coros)

# 即使部分失败，也处理成功的
for item in result.successful:
    process(item)

# 记录失败的
for idx, exc in result.failed:
    logger.error(f"Task {idx} failed: {exc}")
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
