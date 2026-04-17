# cache_utils - 内存缓存工具模块

轻量级内存缓存实现，零外部依赖，支持 TTL 过期、LRU 淘汰策略、线程安全和缓存统计。

## 功能特性

- ✅ **TTL 过期** - 支持全局默认 TTL 和单键 TTL
- ✅ **LRU 淘汰** - Least Recently Used 淘汰策略
- ✅ **最大容量限制** - 防止内存无限增长
- ✅ **线程安全** - 可选的线程安全模式
- ✅ **缓存统计** - 命中率、未命中、淘汰计数
- ✅ **装饰器模式** - 简单易用的函数缓存装饰器
- ✅ **多级缓存** - 支持 L1/L2 分层架构
- ✅ **缓存管理器** - 管理多个命名缓存实例

## 快速开始

### 基本使用

```python
from mod import MemoryCache

# 创建缓存
cache = MemoryCache(max_size=1000, default_ttl=300)  # 最大1000条，默认5分钟过期

# 设置和获取
cache.set('user:1', {'name': 'Alice', 'age': 30})
user = cache.get('user:1')
print(user)  # {'name': 'Alice', 'age': 30}

# 不存在时返回默认值
value = cache.get('nonexistent', default='N/A')
print(value)  # N/A

# 检查存在
if 'user:1' in cache:
    print("用户已缓存")
```

### TTL 过期

```python
# 全局默认 TTL
cache = MemoryCache(default_ttl=60)  # 60秒后过期

# 单键 TTL
cache.set('temp_data', 'value', ttl=10)  # 10秒后过期
cache.set('permanent_data', 'value', ttl=None)  # 永不过期

# 清理过期条目
cleaned = cache.cleanup_expired()
print(f"清理了 {cleaned} 个过期条目")
```

### LRU 淘汰

```python
# 容量限制 + LRU 淘汰
cache = MemoryCache(max_size=3)

cache.set('a', 1)
cache.set('b', 2)
cache.set('c', 3)
# 缓存: a, b, c

cache.get('a')  # 访问 'a'，使其成为最近使用
cache.set('d', 4)  # 添加 'd'，淘汰最久未使用的 'b'
# 缓存: a, c, d
```

### 字典接口

```python
cache = MemoryCache()

# 像字典一样使用
cache['key'] = 'value'
print(cache['key'])
del cache['key']

print(len(cache))
print('key' in cache)
```

### 缓存统计

```python
cache = MemoryCache()

cache.set('key', 'value')
cache.get('key')      # 命中
cache.get('key')      # 命中
cache.get('missing')  # 未命中

stats = cache.get_stats()
print(f"命中率: {stats.hit_rate:.2%}")
print(f"总请求: {stats.total_requests}")
# 命中率: 66.67%
# 总请求: 3
```

## 高级用法

### get_or_set 模式

```python
cache = MemoryCache(ttl=300)

def fetch_user(user_id):
    # 模拟数据库查询
    return {'id': user_id, 'name': f'User{user_id}'}

# 自动获取或创建
user = cache.get_or_set('user:123', lambda: fetch_user(123))
```

### 函数结果缓存装饰器

```python
from mod import cached

@cached(ttl=60, max_size=100)
def expensive_computation(n):
    """耗时计算，结果缓存60秒"""
    print(f"计算中... {n}")
    return sum(i ** 2 for i in range(n))

# 第一次调用
result1 = expensive_computation(1000)  # 计算中... 1000

# 第二次调用（缓存命中）
result2 = expensive_computation(1000)  # 无输出，直接返回缓存

# 查看缓存统计
print(expensive_computation.cache_stats())

# 清除缓存
expensive_computation.cache_clear()
```

### 自定义缓存键

```python
@cached(ttl=60, key_prefix='user_')
def get_user(user_id, include_deleted=False):
    return {'id': user_id, 'name': 'User'}

# 或完全自定义键构建
def build_key(*args, **kwargs):
    return f"custom:{args[0]}:{kwargs.get('flag', 'default')}"

@cached(ttl=60, key_builder=build_key)
def custom_func(id, flag=None):
    return id
```

### 时间窗口缓存

```python
from mod import TimedCache

# 每60秒刷新一次
cache = TimedCache(window_seconds=60)

def fetch_latest_data():
    return "最新数据"

data = cache.get_or_refresh('data', fetch_latest_data)
```

### 多级缓存

```python
from mod import MultiLevelCache

# L1: 本地内存缓存
cache = MultiLevelCache(l1_size=1000, l1_ttl=60)

# 可选：配置 L2 远程缓存（如 Redis）
def redis_get(key):
    # 从 Redis 获取
    pass

def redis_set(key, value, ttl):
    # 写入 Redis
    pass

cache.set_l2_handlers(
    get_handler=redis_get,
    set_handler=redis_set
)

# 自动从 L2 回填 L1
value = cache.get('key')
```

### 缓存管理器

```python
from mod import CacheManager

# 单例管理器
manager = CacheManager()

# 创建命名缓存
user_cache = manager.get_cache('users', max_size=500, default_ttl=300)
product_cache = manager.get_cache('products', max_size=1000, default_ttl=600)

# 获取所有缓存统计
stats = manager.get_all_stats()
for name, stat in stats.items():
    print(f"{name}: 命中率 {stat['hit_rate']:.2%}")

# 清空所有缓存
manager.clear_all()
```

## API 参考

### MemoryCache

| 方法 | 说明 |
|------|------|
| `get(key, default=None)` | 获取缓存值 |
| `set(key, value, ttl=None)` | 设置缓存值 |
| `delete(key)` | 删除缓存条目 |
| `exists(key)` | 检查键是否存在且未过期 |
| `clear()` | 清空缓存 |
| `size()` | 返回当前缓存大小 |
| `cleanup_expired()` | 清理所有过期条目 |
| `get_or_set(key, factory, ttl=None)` | 获取或创建缓存值 |
| `get_stats()` | 获取统计信息 |
| `get_all_keys()` | 获取所有键 |
| `get_entries_info()` | 获取所有条目详情 |

### CacheStats

| 属性/方法 | 说明 |
|-----------|------|
| `hits` | 命中次数 |
| `misses` | 未命中次数 |
| `evictions` | 淘汰次数 |
| `expirations` | 过期次数 |
| `total_requests` | 总请求数 |
| `hit_rate` | 命中率 (0.0-1.0) |
| `reset()` | 重置统计 |
| `to_dict()` | 转换为字典 |

### 装饰器 @cached

```python
@cached(ttl=None, max_size=1000, key_prefix='', key_builder=None)
def func(*args, **kwargs):
    ...
```

| 参数 | 说明 |
|------|------|
| `ttl` | 缓存时间（秒） |
| `max_size` | 最大缓存条目数 |
| `key_prefix` | 缓存键前缀 |
| `key_builder` | 自定义键构建函数 |

## 使用场景

1. **API 响应缓存** - 缓存频繁请求的 API 响应
2. **数据库查询缓存** - 减少数据库查询压力
3. **计算结果缓存** - 缓存耗时计算的结果
4. **配置缓存** - 缓存应用配置信息
5. **会话数据** - 临时会话数据存储
6. **限流计数** - API 访问频率限制

## 性能建议

- 合理设置 `max_size` 防止内存溢出
- 根据数据新鲜度要求设置 TTL
- 高并发场景启用 `thread_safe=True`
- 定期调用 `cleanup_expired()` 清理过期数据
- 监控 `hit_rate` 优化缓存策略

## 测试

```bash
python -m pytest cache_utils_test.py -v
```

## 许可证

MIT License