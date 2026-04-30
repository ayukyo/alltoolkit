# Cache Utilities - JavaScript 缓存工具模块

提供多种缓存实现，零依赖，仅使用 JavaScript 标准库。

## 功能特性

### 缓存类型

1. **LRU Cache** - 最近最少使用缓存
   - 当缓存满时，淘汰最久未使用的条目
   - 适合：数据缓存、图片缓存、配置缓存

2. **LFU Cache** - 最不经常使用缓存
   - 当缓存满时，淘汰访问频率最低的条目
   - 适合：热门内容缓存、排行榜缓存

3. **TTL Cache** - 带过期时间的缓存
   - 条目在指定时间后自动过期
   - 支持自动清理和手动清理
   - 适合：API 响应缓存、临时数据、会话缓存

4. **Memory Cache** - 简单内存缓存
   - 提供基本缓存功能
   - 支持过期时间和最大容量
   - 适合：通用缓存场景

5. **Two-Level Cache** - 两级缓存
   - L1 快速小容量缓存 + L2 大容量缓存
   - 自动回填机制
   - 适合：高性能缓存场景

### 装饰器函数

- **memoize** - 同步函数缓存装饰器
- **memoizeAsync** - 异步函数缓存装饰器（防止重复请求）

### 工具函数

- **createCacheKey** - 创建缓存键
- **multiGet** - 批量获取缓存值
- **multiSet** - 批量设置缓存值

## 使用方法

### LRU Cache

```javascript
const { LRUCache } = require('./mod.js');

const cache = new LRUCache(100); // 最大容量 100

// 设置值
cache.set('key1', 'value1');
cache.set('key2', 'value2');

// 获取值
const value = cache.get('key1'); // 'value1'

// 检查存在
cache.has('key1'); // true

// 删除
cache.delete('key1');

// 清空
cache.clear();

// 统计信息
cache.getStats(); // { size, capacity, hits, misses, hitRate }
```

### LFU Cache

```javascript
const { LFUCache } = require('./mod.js');

const cache = new LFUCache(50);

// 使用方法与 LRU Cache 类似
// 区别：淘汰策略基于访问频率
```

### TTL Cache

```javascript
const { TTLCache } = require('./mod.js');

const cache = new TTLCache({
  defaultTTL: 60000, // 默认 60 秒过期
  maxSize: 200, // 最大容量
  cleanupInterval: 10000 // 每 10 秒自动清理
});

// 使用自定义 TTL
cache.set('key', 'value', 30000); // 30 秒过期

// 获取剩余时间
cache.getRemainingTTL('key'); // 剩余毫秒数

// 刷新过期时间
cache.refresh('key', 60000);

// 手动清理过期条目
cache.cleanup();

// 停止自动清理
cache.stopCleanup();
```

### Memory Cache

```javascript
const { MemoryCache } = require('./mod.js');

const cache = new MemoryCache({
  maxSize: 500,
  defaultTTL: 60000
});

// 基本操作
cache.set('key', 'value');
cache.get('key', 'default'); // 第二参数为默认值

// 条件设置（不存在时才设置）
cache.setNX('key', 'value'); // true/false

// 获取并删除
cache.take('key');

// 遍历
cache.forEach((value, key) => {
  console.log(key, value);
});
```

### Two-Level Cache

```javascript
const { TwoLevelCache } = require('./mod.js');

const cache = new TwoLevelCache({
  l1Capacity: 50, // L1 快速缓存容量
  l2Capacity: 500, // L2 大容量缓存容量
  l2TTL: 300000 // L2 过期时间
});

// L2 命中会自动回填到 L1
cache.get('key'); // 先查 L1，再查 L2
```

### Memoize

```javascript
const { memoize } = require('./mod.js');

// 缓存函数结果
function expensiveCalculation(n) {
  // 复杂计算...
  return result;
}

const cachedCalculation = memoize(expensiveCalculation, {
  ttl: 60000, // 缓存 60 秒
  maxSize: 100,
  keyFn: (n) => `calc:${n}` // 自定义键生成
});

cachedCalculation(100); // 计算
cachedCalculation(100); // 使用缓存

cachedCalculation.clear(); // 清空缓存
cachedCalculation.getStats(); // 统计信息
```

### Memoize Async

```javascript
const { memoizeAsync } = require('./mod.js');

// 缓存异步函数结果
async function fetchData(id) {
  const response = await fetch(`/api/data/${id}`);
  return response.json();
}

const cachedFetch = memoizeAsync(fetchData, {
  ttl: 10000, // 10 秒缓存
  maxSize: 50
});

// 防止重复请求 - 同时发起多个相同请求只会执行一次
await cachedFetch(1); // 发起请求
await cachedFetch(1); // 使用缓存（或等待进行中的请求）
```

### 工具函数

```javascript
const { createCacheKey, multiGet, multiSet } = require('./mod.js');

// 创建缓存键
const key = createCacheKey('user', 123, 'profile');
// 'user:123:profile'

// 批量操作
const cache = new LRUCache(10);
multiSet(cache, { a: 1, b: 2, c: 3 });
multiGet(cache, ['a', 'b', 'c']); // { a: 1, b: 2, c: 3 }
```

## 测试

运行测试：

```bash
node cache_utils_test.js
```

## 运行示例

```bash
node examples.js
```

## API 参考

### LRUCache

| 方法 | 说明 |
|------|------|
| `get(key)` | 获取值 |
| `set(key, value)` | 设置值 |
| `has(key)` | 检查存在 |
| `delete(key)` | 删除条目 |
| `clear()` | 清空缓存 |
| `keys()` | 获取所有键 |
| `values()` | 获取所有值 |
| `getStats()` | 获取统计信息 |
| `getHitRate()` | 获取命中率 |

### LFUCache

与 LRUCache API 相同。

### TTLCache

| 方法 | 说明 |
|------|------|
| `get(key)` | 获取值（检查过期） |
| `set(key, value, ttl)` | 设置值（可选 TTL） |
| `has(key)` | 检查存在（检查过期） |
| `delete(key)` | 删除条目 |
| `clear()` | 清空缓存 |
| `cleanup()` | 手动清理过期条目 |
| `getRemainingTTL(key)` | 获取剩余时间 |
| `refresh(key, ttl)` | 刷新过期时间 |
| `stopCleanup()` | 停止自动清理 |
| `getStats()` | 获取统计信息 |

### MemoryCache

| 方法 | 说明 |
|------|------|
| `get(key, defaultValue)` | 获取值（可带默认值） |
| `set(key, value, ttl)` | 设置值 |
| `setNX(key, value, ttl)` | 不存在时才设置 |
| `take(key)` | 获取并删除 |
| `has(key)` | 检查存在 |
| `delete(key)` | 删除条目 |
| `clear()` | 清空缓存 |
| `forEach(callback)` | 遍历缓存 |
| `getStats()` | 获取统计信息 |

## 性能特点

- **零外部依赖**：仅使用 JavaScript 标准库
- **O(1) 时间复杂度**：所有主要操作都是常数时间
- **内存高效**：自动淘汰机制防止内存溢出
- **统计完整**：提供命中率、访问次数等统计信息

## 适用场景

- Web 应用数据缓存
- API 响应缓存
- 图片/资源缓存
- 计算结果缓存
- 配置缓存
- 会话管理
- 热门内容缓存