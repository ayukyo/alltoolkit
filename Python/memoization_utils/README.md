# Memoization Utils

零依赖的 Python 函数结果缓存工具库，用于优化函数性能。

## 特性

- **多种缓存策略**：LRU 淘汰、TTL 过期
- **线程安全**：支持并发访问
- **灵活配置**：自定义缓存大小、过期时间、键生成函数
- **零依赖**：纯 Python 标准库实现
- **完整统计**：命中率、缓存大小等统计信息

## 快速开始

### 基本用法

```python
from mod import memoize

@memoize(max_size=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 第一次调用会计算
print(fibonacci(30))  # 832040

# 第二次调用使用缓存
print(fibonacci(30))  # 瞬间返回

# 查看缓存统计
print(fibonacci.cache_stats())
```

### TTL 缓存

```python
from mod import ttl_cache

@ttl_cache(ttl=60)  # 60秒过期
def fetch_api_data(url):
    return requests.get(url).json()

# 60秒内重复调用使用缓存
data = fetch_api_data("https://api.example.com/data")
```

### 方法记忆化

```python
from mod import memoize_method

class DataProcessor:
    @memoize_method(max_size=100)
    def process(self, data_id):
        # 复杂处理逻辑
        return expensive_operation(data_id)

# 每个实例独立缓存
processor = DataProcessor()
result = processor.process("data_1")
```

### 缓存属性

```python
from mod import cached_property

class Config:
    def __init__(self, data):
        self.data = data
    
    @cached_property
    def processed_data(self):
        # 延迟计算，只执行一次
        return expensive_processing(self.data)
```

### 手动缓存控制

```python
from mod import MemoCache

cache = MemoCache(max_size=100, ttl=60)

# 设置缓存
cache.set(("user", 1), {}, {"name": "Alice"})

# 获取缓存
found, value = cache.get(("user", 1), {})
if found:
    print(value)

# 查看统计
print(cache.stats())

# 清空缓存
cache.clear()
```

## API 参考

### `memoize(max_size=128, ttl=None, thread_safe=True, key_func=None)`

装饰器，缓存函数结果。

**参数：**
- `max_size`: 最大缓存条目数
- `ttl`: 生存时间（秒），None 表示永不过期
- `thread_safe`: 是否线程安全
- `key_func`: 自定义键生成函数

### `MemoCache`

缓存类，提供手动控制。

**方法：**
- `get(args, kwargs)`: 获取缓存值
- `set(args, kwargs, value, ttl=None)`: 设置缓存值
- `clear()`: 清空缓存
- `cleanup()`: 清理过期条目
- `stats()`: 获取统计信息

### 其他装饰器

- `lru_cache(max_size)`: 简化的 LRU 缓存
- `ttl_cache(ttl, max_size)`: TTL 缓存
- `cached_property`: 缓存属性
- `memoize_method()`: 方法记忆化
- `expire_after(seconds)`: 定时过期

## 性能

在递归斐波那契计算测试中，缓存版本比无缓存版本快 **4000+ 倍**：

```
fibonacci(35):
  有缓存版本: 0.0006s
  无缓存版本: 2.63s
  加速比: 4330x
```

## 许可证

MIT License