# Semaphore Utils

信号量工具模块 - 提供线程安全的并发控制功能。

## 概述

信号量是一种同步原语，用于限制并发操作的数量。本模块提供了增强版的信号量实现，包括：

- **基本信号量** - 固定容量的计数信号量
- **加权信号量** - 可变资源分配
- **信号量池** - 多资源管理
- **异步信号量** - asyncio 支持
- **有界信号量** - 防止过度释放
- **优先级信号量** - 按优先级服务
- **速率限制器** - 基于 token bucket 算法
- **并发限制器** - 组合信号量和速率限制

## 特性

- ✅ 零外部依赖 (仅使用 Python 标准库)
- ✅ 线程安全实现
- ✅ 超时支持
- ✅ 非阻塞 try_acquire
- ✅ 上下文管理器协议
- ✅ asyncio 异步支持
- ✅ 优先级队列
- ✅ 速率限制
- ✅ 多资源原子获取

## 安装

无需安装，直接导入使用：

```python
from semaphore_utils.semaphore_utils import Semaphore, WeightedSemaphore
```

## 快速示例

### 基本信号量

```python
from semaphore_utils.semaphore_utils import Semaphore

# 创建允许3个并发操作的信号量
sem = Semaphore(3)

# 使用上下文管理器
with sem:
    # 执行受保护的操作
    process_data()

# 手动获取和释放
sem.acquire()
try:
    do_work()
finally:
    sem.release()

# 非阻塞尝试
if sem.try_acquire():
    do_quick_work()
    sem.release()
else:
    print("Semaphore is busy")
```

### 加权信号量

```python
from semaphore_utils.semaphore_utils import WeightedSemaphore

# 创建总容量100单位的加权信号量
sem = WeightedSemaphore(100)

# 获取30单位资源
sem.acquire(30)
# ... 执行需要30单位资源的操作
sem.release(30)

# 使用上下文管理器
with sem.acquire_context(50):
    process_large_data()
```

### 速率限制器

```python
from semaphore_utils.semaphore_utils import RateLimiter

# 每秒最多5次操作
limiter = RateLimiter(5, 1.0)

for i in range(10):
    limiter.acquire()  # 可能等待
    call_api()
```

### 异步信号量

```python
from semaphore_utils.semaphore_utils import AsyncSemaphore

sem = AsyncSemaphore(5)

async def worker():
    async with sem:
        await async_operation()
```

### 信号量池

```python
from semaphore_utils.semaphore_utils import SemaphorePool

pool = SemaphorePool(5)

# 获取不同资源的信号量
db_sem = pool.get('database', capacity=10)
api_sem = pool.get('api')

with db_sem:
    query_database()
```

## API 文档

### Semaphore

| 方法 | 说明 |
|------|------|
| `acquire(timeout)` | 获取许可，可设置超时 |
| `try_acquire()` | 非阻塞尝试获取 |
| `release()` | 释放许可 |
| `available()` | 返回可用许可数 |
| `in_use()` | 返回已使用许可数 |
| `capacity` | 总容量属性 |

### WeightedSemaphore

| 方法 | 说明 |
|------|------|
| `acquire(weight, timeout)` | 获取指定权重单位 |
| `try_acquire(weight)` | 非阻塞尝试获取 |
| `release(weight)` | 释放指定权重单位 |
| `acquire_context(weight)` | 上下文管理器 |

### RateLimiter

| 方法 | 说明 |
|------|------|
| `acquire(timeout)` | 等待许可 |
| `try_acquire()` | 非阻塞尝试 |
| `available()` | 返回可用 token 数 |

### PrioritySemaphore

| 方法 | 说明 |
|------|------|
| `acquire(priority)` | 按优先级获取 (数字越小优先级越高) |

## 辅助函数

```python
# 原子获取多个信号量
acquire_all(sem1, sem2, sem3)

# 在信号量保护下运行函数
result = run_with_semaphore(sem, my_function, arg1, arg2)
```

## 使用场景

1. **API 限流** - 控制并发 API 调用
2. **数据库连接池** - 限制连接数
3. **资源分配** - 按权重分配内存/CPU
4. **优先级调度** - 关键任务优先执行
5. **速率控制** - 防止请求过载
6. **线程安全计数** - 保护共享变量

## 测试

运行测试：

```bash
python semaphore_utils_test.py
```

## 示例

运行示例：

```bash
python examples.py
```

## 作者

AllToolkit

## 版本

1.0.0

## 许可证

MIT