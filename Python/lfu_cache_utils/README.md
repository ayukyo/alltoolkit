# LFU Cache Utils 🚀

Least Frequently Used (LFU) 缓存实现，高性能内存缓存方案。

## 特性

- ✅ **LFU 算法** - 按访问频率淘汰
- ✅ **O(1) 复杂度** - 高效的 get/put 操作
- ✅ **装饰器支持** - `@lfu_cache_decorator`
- ✅ **构建器模式** - 灵活的缓存配置
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 基本使用

```python
from lfu_cache_utils import LFUCache

cache = LFUCache(capacity=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)

print(cache.get("a"))  # 1 (access count: 2)
print(cache.get("b"))  # 2 (access count: 2)

# 触发淘汰
cache.put("d", 4)  # 淘汰访问次数最少的
print(cache.get("c"))  # None (已淘汰)
```

### 装饰器

```python
from lfu_cache_utils import lfu_cache_decorator

@lfu_cache_decorator(capacity=128)
def expensive_computation(x):
    return x * x

result = expensive_computation(10)  # 计算
result = expensive_computation(10)  # 缓存命中
```

## API 参考

### 类

| 类 | 说明 |
|---|------|
| `LFUCache` | LFU 缓存实现 |
| `LFUCacheBuilder` | 缓存构建器 |

### 核心函数

| 函数 | 说明 |
|------|------|
| `cache.get(key)` | 获取缓存值 |
| `cache.put(key, value)` | 设置缓存 |
| `cache.size()` | 当前缓存大小 |
| `lfu_cache_decorator(capacity)` | 缓存装饰器 |
