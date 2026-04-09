# AllToolkit - Python Cache Utils 🧠

**零依赖内存缓存工具 - 生产就绪**

---

## 📖 概述

`cache_utils` 提供功能完整的内存缓存解决方案，支持 TTL 过期、LRU 淘汰、大小限制和线程安全操作。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **TTL 过期** - 支持按条目设置生存时间
- **LRU 淘汰** - 自动淘汰最少使用条目
- **大小限制** - 可配置最大缓存容量
- **线程安全** - 支持并发访问
- **统计追踪** - 命中率、驱逐数等指标
- **批量操作** - get_many/set_many/delete_many
- **原子计数** - increment/decrement 操作
- **懒加载** - get_or_set 模式
- **缓存装饰器** - @cached 一键缓存函数结果
- **缓存预热** - warm 方法批量填充

---

## 🚀 快速开始

### 基础使用

```python
from mod import Cache

# 创建缓存
cache = Cache(max_size=100, default_ttl=300.0)

# 设置值
cache.set("key", "value")
cache.set("key_with_ttl", "expires in 60s", ttl=60.0)

# 获取值
value = cache.get("key")
value_with_default = cache.get("missing", "default")

# 检查存在
if "key" in cache:
    print("Key exists!")

# 删除
cache.delete("key")

# 清空
cache.clear()
```

### 字典式访问

```python
cache["key"] = "value"
print(cache["key"])
del cache["key"]
print(len(cache))
```

---

## 📚 API 参考

### Cache 类

| 方法 | 描述 | 返回 |
|------|------|------|
| `get(key, default)` | 获取值 | `T` 或 `default` |
| `set(key, value, ttl)` | 设置值 | `None` |
| `delete(key)` | 删除键 | `bool` |
| `clear()` | 清空缓存 | `None` |
| `contains(key)` | 检查存在 | `bool` |
| `ttl(key)` | 获取剩余 TTL | `float` 或 `None` |
| `touch(key, ttl)` | 重置 TTL | `bool` |
| `increment(key, amount, default)` | 原子增加 | `int` |
| `decrement(key, amount, default)` | 原子减少 | `int` |
| `get_or_set(key, factory, ttl)` | 获取或计算 | `T` |
| `get_many(keys)` | 批量获取 | `Dict[str, T]` |
| `set_many(items, ttl)` | 批量设置 | `None` |
| `delete_many(keys)` | 批量删除 | `int` |
| `expire()` | 移除过期条目 | `int` |
| `warm(items, ttl)` | 预热缓存 | `int` |
| `keys()` | 获取所有键 | `List[str]` |
| `values()` | 获取所有值 | `List[T]` |
| `items()` | 获取所有键值对 | `List[Tuple]` |
| `to_dict()` | 导出为字典 | `Dict` |

### 属性

| 属性 | 描述 |
|------|------|
| `size` | 当前条目数 |
| `max_size` | 最大容量 |
| `stats` | 统计信息 |

### CacheStats 类

| 属性 | 描述 |
|------|------|
| `hits` | 命中次数 |
| `misses` | 未命中次数 |
| `evictions` | 驱逐次数 |
| `expirations` | 过期次数 |
| `sets` | 设置次数 |
| `deletes` | 删除次数 |
| `hit_rate` | 命中率 (0.0-1.0) |

---

## 🎯 使用场景

### 1. 函数结果缓存（Memoization）

```python
from mod import cached

@cached(ttl=60.0)
def expensive_computation(x, y):
    time.sleep(1)  # 模拟耗时操作
    return x + y

# 第一次调用：实际计算
result1 = expensive_computation(1, 2)

# 第二次调用：直接返回缓存
result2 = expensive_computation(1, 2)
```

### 2. 会话管理

```python
from mod import Cache
import secrets

session_cache = Cache(max_size=1000, default_ttl=1800.0)  # 30 分钟

def create_session(user_id):
    session_id = secrets.token_hex(16)
    session_cache.set(f"session:{session_id}", {"user_id": user_id})
    return session_id

def get_session(session_id):
    return session_cache.get(f"session:{session_id}")

def invalidate_session(session_id):
    return session_cache.delete(f"session:{session_id}")
```

### 3. 速率限制

```python
from mod import Cache

rate_cache = Cache(default_ttl=60.0)  # 1 分钟窗口
MAX_REQUESTS = 5

def check_rate_limit(user_id):
    key = f"rate:{user_id}"
    count = rate_cache.get(key, 0)
    
    if count >= MAX_REQUESTS:
        return False
    
    rate_cache.set(key, count + 1)
    return True
```

### 4. 多级缓存

```python
from mod import Cache

# L1: 快速小缓存（热数据）
l1 = Cache(max_size=10, default_ttl=60.0)

# L2: 大缓存（温数据）
l2 = Cache(max_size=100, default_ttl=300.0)

def get_multi_level(key):
    # 先查 L1
    value = l1.get(key)
    if value is not None:
        return value, "L1"
    
    # 再查 L2
    value = l2.get(key)
    if value is not None:
        l1.set(key, value)  # 提升到 L1
        return value, "L2"
    
    return None, "MISS"
```

### 5. 懒加载

```python
from mod import Cache

cache = Cache()

def get_user_profile(user_id):
    def load_from_db():
        # 模拟数据库查询
        return {"id": user_id, "name": f"User_{user_id}"}
    
    return cache.get_or_set(
        f"user:{user_id}",
        load_from_db,
        ttl=3600.0
    )
```

### 6. 原子计数器

```python
from mod import Cache

counter = Cache()
counter.set("page:views", 0)

# 线程安全的增加
counter.increment("page:views", 1)
counter.increment("page:views", 5)

# 减少
counter.decrement("page:views", 2)

print(counter.get("page:views"))  # 4
```

---

## 🧪 运行测试

```bash
cd cache_utils
python cache_utils_test.py -v
```

### 测试覆盖

- ✅ CacheEntry 数据类
- ✅ CacheStats 统计
- ✅ 基础 get/set/delete
- ✅ TTL 过期
- ✅ LRU 淘汰
- ✅ 大小限制
- ✅ 线程安全
- ✅ 批量操作
- ✅ 原子计数
- ✅ get_or_set 懒加载
- ✅ @cached 装饰器
- ✅ 边界情况处理
- ✅ 集成测试

---

## 📊 统计监控

```python
cache = Cache(enable_stats=True)

# 使用缓存...
cache.set("key", "value")
cache.get("key")
cache.get("missing")

# 查看统计
stats = cache.stats
print(f"命中率：{stats.hit_rate:.2%}")
print(f"命中：{stats.hits}, 未命中：{stats.misses}")
print(f"驱逐：{stats.evictions}, 过期：{stats.expirations}")

# 导出完整状态
export = cache.to_dict()
print(export['stats'])
```

---

## ⚠️ 注意事项

1. **内存限制**: 缓存存储在内存中，注意 max_size 设置
2. **进程隔离**: 每个进程有独立缓存，不支持跨进程共享
3. **None 值**: 缓存 None 是合法的，get 返回 None 不一定表示未命中
4. **TTL 精度**: TTL 基于 time.time()，精度约毫秒级
5. **线程安全**: 所有操作都是线程安全的，使用 RLock 保护

---

## 🔧 配置选项

```python
cache = Cache(
    max_size=1000,        # 最大条目数（默认 1000）
    default_ttl=300.0,    # 默认 TTL 秒（默认 None=永不过期）
    enable_stats=True,    # 启用统计（默认 True）
)
```

---

## 📁 文件结构

```
cache_utils/
├── mod.py                      # 主要实现
├── cache_utils_test.py         # 测试套件 (70+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 💡 最佳实践

### 1. 选择合适的 max_size

```python
# 小型热点缓存
hot_cache = Cache(max_size=100, default_ttl=60.0)

# 大型通用缓存
main_cache = Cache(max_size=10000, default_ttl=3600.0)
```

### 2. 合理设置 TTL

```python
# 频繁变化数据：短 TTL
cache.set("stock_price:AAPL", price, ttl=30.0)

# 稳定数据：长 TTL
cache.set("config:version", version, ttl=86400.0)

# 永不过期
cache.set("constant:pi", 3.14159)
```

### 3. 监控命中率

```python
def monitor_cache(cache):
    stats = cache.stats
    if stats.hit_rate < 0.5:
        print("警告：命中率低于 50%")
    if stats.evictions > stats.sets * 0.5:
        print("警告：驱逐率过高，考虑增加 max_size")
```

### 4. 批量操作更高效

```python
# 推荐：批量操作
cache.set_many({"a": 1, "b": 2, "c": 3})
result = cache.get_many(["a", "b", "c"])

# 不推荐：多次单独操作
for key, value in items.items():
    cache.set(key, value)
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
