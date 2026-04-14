# LRU Cache Utils

**LRU（最近最少使用）缓存工具模块**

零依赖的 LRU 缓存实现，支持 TTL、线程安全、统计信息等功能。

---

## 特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **线程安全** - 支持并发读写操作
- ✅ **TTL 支持** - 可设置条目过期时间
- ✅ **自动清理** - 定期清理过期条目
- ✅ **统计信息** - 命中率、淘汰数等统计
- ✅ **批量操作** - 批量获取、设置、删除
- ✅ **装饰器模式** - 函数结果缓存
- ✅ **多种变体** - TTLCache、BoundedLRUCache、WeightedLRUCache 等

---

## 快速开始

### 基本使用

```python
from mod import LRUCache

# 创建缓存
cache = LRUCache(max_size=100)

# 设置值
cache.set('key', 'value')

# 获取值
value = cache.get('key')  # 'value'
missing = cache.get('missing', 'default')  # 'default'

# 字典接口
cache['name'] = 'Alice'
value = cache['name']  # 'Alice'

# 存在性检查
if 'key' in cache:
    print("存在")
```

### TTL 过期

```python
# 默认 TTL
cache = LRUCache(max_size=100, default_ttl=300)  # 5 分钟

# 单条 TTL
cache.set('session', data, ttl=60)  # 1 分钟

# 查询剩余 TTL
ttl = cache.ttl('session')  # 剩余秒数
```

### 装饰器缓存

```python
from mod import lru_cache

@lru_cache(max_size=100, ttl=60)
def expensive_function(n):
    return n * 2

result = expensive_function(5)  # 计算并缓存
result = expensive_function(5)  # 使用缓存
```

---

## API 参考

### LRUCache

#### 构造参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `max_size` | int | 最大缓存条目数 |
| `default_ttl` | float | 默认 TTL（秒），None 表示永不过期 |
| `auto_cleanup` | bool | 是否自动清理过期条目 |
| `cleanup_interval` | int | 清理间隔（操作次数） |

#### 方法

| 方法 | 说明 |
|------|------|
| `get(key, default)` | 获取值，不存在返回 default |
| `set(key, value, ttl)` | 设置值，可选 TTL |
| `delete(key)` | 删除条目 |
| `exists(key)` | 检查是否存在且未过期 |
| `clear()` | 清空缓存 |
| `size()` | 当前大小 |
| `keys()` | 所有键 |
| `values()` | 所有值 |
| `items()` | 所有键值对 |
| `get_many(keys)` | 批量获取 |
| `set_many(items, ttl)` | 批量设置 |
| `delete_many(keys)` | 批量删除 |
| `get_or_set(key, factory, ttl)` | 获取或创建 |
| `touch(key, ttl)` | 更新访问时间和 TTL |
| `ttl(key)` | 查询剩余 TTL |
| `peek(key)` | 查看但不更新访问信息 |
| `cleanup()` | 手动清理过期条目 |
| `stats()` | 统计信息 |
| `reset_stats()` | 重置统计 |

#### 统计信息

```python
stats = cache.stats()
# {
#     'size': 50,
#     'max_size': 100,
#     'hits': 120,
#     'misses': 30,
#     'hit_rate': 0.8,
#     'evictions': 5,
#     'expirations': 10,
#     'total_requests': 150
# }
```

---

## 变体类型

### TTLCache

强制 TTL 的缓存，所有条目必须有过期时间。

```python
from mod import TTLCache

cache = TTLCache(max_size=100, default_ttl=300)

cache.set('key', 'value')  # 自动设置 300 秒 TTL
cache.refresh_ttl('key')   # 刷新单个 TTL
cache.refresh_all()        # 刷新所有 TTL
```

### BoundedLRUCache

设置最小保留数量的缓存。

```python
from mod import BoundedLRUCache

cache = BoundedLRUCache(max_size=100, min_size=20)
# 即使压力很大，也至少保留 20 个条目
```

### WeightedLRUCache

按权重控制容量的缓存。

```python
from mod import WeightedLRUCache

cache = WeightedLRUCache(max_weight=1000)

cache.set('small', data, weight=10)   # 小权重
cache.set('large', data, weight=500)  # 大权重

cache.current_weight()    # 当前总权重
cache.available_weight()  # 可用权重
```

### ExpiringPriorityCache

淘汰时优先淘汰即将过期的条目。

```python
from mod import ExpiringPriorityCache

cache = ExpiringPriorityCache(max_size=100)
cache.set('long', value, ttl=3600)  # 长过期
cache.set('short', value, ttl=10)   # 短过期
# 淘汰时优先淘汰 short
```

---

## 使用场景

### 会话管理

```python
session_cache = TTLCache(max_size=1000, default_ttl=1800)  # 30 分钟

session_cache.set(session_id, {'user': user, 'data': data})
session = session_cache.get(session_id)
session_cache.refresh_ttl(session_id)  # 延长会话
```

### API 结果缓存

```python
@lru_cache(max_size=1000, ttl=60)
def get_weather(city):
    # 调用天气 API
    return fetch_weather(city)
```

### 计算缓存

```python
calc_cache = LRUCache(max_size=100)

def calculate(x, y):
    key = (x, y)
    return calc_cache.get_or_set(
        key,
        lambda: expensive_calculation(x, y)
    )
```

### 图片缓存（加权）

```python
image_cache = WeightedLRUCache(max_weight=50_000_000)  # 50MB

# 小图
image_cache.set('thumbnail', thumb, weight=len(thumb))

# 大图
image_cache.set('full', image, weight=len(image))
```

---

## 线程安全

所有缓存类型都是线程安全的，支持并发读写：

```python
import threading

cache = LRUCache(max_size=1000)

def worker():
    for i in range(100):
        cache.set(f'key_{i}', i)
        cache.get(f'key_{i}')

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
```

---

## 测试

```bash
python Python/lru_cache_utils/lru_cache_utils_test.py
```

---

## 许可证

MIT License