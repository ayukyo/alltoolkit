# Memoization Utils

一个功能完整的记忆化/缓存工具库，专为 Zig 设计。支持 TTL 过期、LRU 驱逐和统计信息。

## 功能特性

- **泛型缓存**: 支持任意键值类型
- **TTL 支持**: 可设置条目的生存时间
- **LRU 驱逐**: 当达到最大容量时自动驱逐最少使用的条目
- **统计信息**: 跟踪命中率、驱逐次数等
- **零外部依赖**: 纯 Zig 标准库实现
- **线程安全选项**: 可配置的并发控制

## 核心类型

### CacheEntry(V)

缓存条目，包含值和 TTL 元数据。

```zig
const entry = CacheEntry(i32).init(42, 60000); // 值: 42, TTL: 60秒
const is_expired = entry.isExpired();
const remaining = entry.remainingTtl();
```

### CacheStats

缓存统计信息。

```zig
var stats = CacheStats{};
stats.hits += 1;
const ratio = stats.hitRatio(); // 命中率
stats.reset(); // 重置统计
```

### CacheOptions

缓存配置选项。

```zig
const options = CacheOptions{
    .max_size = 1000,          // 最大条目数
    .default_ttl_ms = 60000,   // 默认 TTL (60秒)
    .enable_stats = true,      // 启用统计
};
```

### MemoCache(K, V)

主缓存类型，泛型实现。

```zig
var cache = MemoCache(i32, []const u8).init(allocator, .{});
defer cache.deinit();
```

## 使用方法

### 基本操作

```zig
const std = @import("std");
const memoization = @import("memoization");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // 创建缓存
    var cache = memoization.MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    // 设置值
    try cache.set(1, 100);
    try cache.set(2, 200);

    // 获取值
    if (cache.get(1)) |value| {
        std.debug.print("Value: {}\n", .{value});
    }

    // 检查存在
    if (cache.contains(2)) {
        std.debug.print("Key 2 exists\n", .{});
    }

    // 删除
    _ = cache.remove(1);

    // 清空
    cache.clear();
}
```

### TTL (生存时间)

```zig
// 设置带 TTL 的值 (毫秒)
try cache.setWithTtl(1, 100, 5000); // 5秒后过期

// 或使用默认 TTL
var cache = MemoCache(i32, i32).init(allocator, .{
    .default_ttl_ms = 60000, // 默认60秒
});

// 获取剩余 TTL
if (cache.getEntry(1)) |entry| {
    std.debug.print("Remaining: {}ms\n", .{entry.remainingTtl().?});
}
```

### LRU 驱逐

```zig
// 创建容量受限的缓存
var cache = MemoCache(i32, i32).init(allocator, .{
    .max_size = 100, // 最多100个条目
});
defer cache.deinit();

// 当超过容量时，自动驱逐最少使用的条目
for (0..200) |i| {
    try cache.set(@intCast(i), @intCast(i));
}

// 检查驱逐统计
std.debug.print("Evictions: {}\n", .{cache.getStats().evictions});
```

### 统计信息

```zig
var cache = MemoCache(i32, i32).init(allocator, .{
    .enable_stats = true,
});

// 执行操作...

const stats = cache.getStats();
std.debug.print("Hits: {}\n", .{stats.hits});
std.debug.print("Misses: {}\n", .{stats.misses});
std.debug.print("Sets: {}\n", .{stats.sets});
std.debug.print("Deletes: {}\n", .{stats.deletes});
std.debug.print("Evictions: {}\n", .{stats.evictions});
std.debug.print("Hit ratio: {d:.2}\n", .{stats.hitRatio()});

// 重置统计
cache.resetStats();
```

### 函数记忆化

```zig
var cache = MemoCache(i32, i64).init(allocator, .{});
defer cache.deinit();

// 记忆化函数调用
const result = try cache.memoizeError(key, struct {
    fn call() anyerror!i64 {
        return expensiveComputation();
    }
}.call);
```

### 简化辅助类型

```zig
// 使用 memoize 辅助类型
var memo = memoization.memoize(i32, i64).init(allocator);
defer memo.deinit();

const result = try memo.call(key, myFunc);
```

### 组合键

```zig
// 使用组合键进行复杂查找
const Key = struct {
    category: i32,
    id: i32,
};

var cache = MemoCache(Key, i64).init(allocator, .{});
defer cache.deinit();

try cache.set(.{ .category = 1, .id = 10 }, 55);

if (cache.get(.{ .category = 1, .id = 10 })) |value| {
    std.debug.print("Value: {}\n", .{value});
}
```

**注意**: Zig 的 `AutoHashMap` 要求键类型能自动哈希和比较。对于字符串键，请使用 Zig 内置的 `StringHashMap` 或提供自定义哈希上下文。

## API 参考

### MemoCache 方法

| 方法 | 描述 |
|------|------|
| `init(allocator, options)` | 创建新缓存 |
| `deinit()` | 释放资源 |
| `get(key)` | 获取值，不存在返回 null |
| `getEntry(key)` | 获取条目（含元数据） |
| `set(key, value)` | 设置值 |
| `setWithTtl(key, value, ttl_ms)` | 设置值（带 TTL） |
| `contains(key)` | 检查键是否存在 |
| `remove(key)` | 删除键，返回是否成功 |
| `clear()` | 清空所有条目 |
| `size()` | 返回当前条目数 |
| `getStats()` | 获取统计信息 |
| `resetStats()` | 重置统计信息 |
| `keys(allocator)` | 获取所有键 |
| `values(allocator)` | 获取所有值 |
| `memoize(key, func)` | 记忆化函数 |
| `memoizeError(key, func)` | 记忆化可能失败的函数 |

## 构建

```bash
# 运行测试
zig build test

# 运行示例
zig build example

# 运行基准测试
zig build benchmark
```

## 应用场景

- 缓存昂贵的计算结果
- API 响应缓存
- 数据库查询缓存
- 函数结果缓存
- HTTP 响应缓存
- 配置缓存
- 会话存储
- 频率限制器后端

## 性能特点

- O(1) 平均插入、查找、删除
- LRU 操作 O(1)
- 内存使用与条目数成正比
- TTL 检查在访问时惰性执行

## 许可证

MIT License