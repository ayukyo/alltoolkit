# LRU Cache Utils

一个零外部依赖的 LRU (Least Recently Used) 缓存实现，提供高效的 O(1) 操作。

## 功能特性

- **O(1) 时间复杂度** - 使用双向链表 + 哈希表实现
- **可配置容量** - 支持动态调整缓存大小
- **TTL 支持** - 可选的自动过期时间
- **线程安全** - 可选的线程安全模式
- **统计信息** - 命中率、淘汰次数等统计数据
- **批量操作** - 支持批量存取
- **装饰器** - 便捷的函数结果缓存
- **回调支持** - 淘汰时的自定义回调

## 快速开始

```python
from lru_cache_utils.mod import LRUCache

# 创建容量为 3 的缓存
cache = LRUCache[str, int](capacity=3)

# 添加项目
cache.put('a', 1)
cache.put('b', 2)
cache.put('c', 3)

# 访问项目（更新 LRU 顺序）
cache.get('a')

# 添加新项目，'b' 将被淘汰
cache.put('d', 4)

# 检查项目
print(cache.get('a'))  # 1
print(cache.get('b'))  # None (已淘汰)
```

## TTL 过期

```python
from lru_cache_utils.mod import LRUCache
import time

# 创建带 TTL 的缓存
cache = LRUCache[str, str](capacity=100, ttl=2.0)  # 2秒过期

cache.put('session', 'user123')
print(cache.get('session'))  # 'user123'

time.sleep(2.5)
print(cache.get('session'))  # None (已过期)
```

## 函数装饰器

```python
from lru_cache_utils.mod import lru_cache

@lru_cache(capacity=100)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))  # 快速计算

# 查看缓存统计
print(fibonacci.cache_stats())
```

## 线程安全

```python
from lru_cache_utils.mod import LRUCache

# 创建线程安全缓存
cache = LRUCache[str, int](capacity=100, thread_safe=True)

# 多线程安全访问
# ...
```

## 淘汰回调

```python
from lru_cache_utils.mod import LRUCache

def on_evict(key, value):
    print(f"淘汰: {key} = {value}")

cache = LRUCache[str, int](capacity=3, on_evict=on_evict)
```

## API 参考

### LRUCache

| 方法 | 描述 |
|------|------|
| `put(key, value, ttl=None)` | 存入键值对 |
| `get(key, default=None)` | 获取值 |
| `delete(key)` | 删除键 |
| `contains(key)` | 检查键是否存在 |
| `clear()` | 清空缓存 |
| `size()` | 当前大小 |
| `keys()` | 所有键（LRU 顺序） |
| `values()` | 所有值（LRU 顺序） |
| `items()` | 所有键值对 |
| `stats()` | 统计信息 |
| `get_or_set(key, factory)` | 获取或计算 |
| `peek(key)` | 查看不更新顺序 |
| `touch(key)` | 更新到最近使用 |
| `put_all(items)` | 批量存入 |
| `get_all(keys)` | 批量获取 |

### 装饰器

- `@lru_cache(capacity, ttl=None)` - LRU 缓存装饰器
- `@memoize` - 简单记忆化装饰器

### TTLCache

仅 TTL 过期缓存（无 LRU 淘汰）：

```python
from lru_cache_utils.mod import TTLCache

cache = TTLCache[str, str](ttl=60.0)  # 60秒过期
```

## 运行测试

```bash
python lru_cache_utils_test.py
```

## 运行示例

```bash
python examples/usage_examples.py
```