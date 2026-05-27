# LRU Cache (Swift)

一个高效、线程安全的 LRU（最近最少使用）缓存实现，支持泛型键值类型。

## 功能特性

- ✅ **泛型支持**: 适用于任意 `Hashable` 键类型和任意值类型
- ✅ **O(1) 操作**: get/set 平均时间复杂度为常数
- ✅ **线程安全**: 使用 `NSLock` 实现线程安全
- ✅ **自动淘汰**: 容量满时自动淘汰最久未使用的条目
- ✅ **TTL 支持**: 支持条目过期时间设置
- ✅ **Codable 支持**: 当 Key 和 Value 遵循 Codable 时，可序列化/反序列化
- ✅ **丰富的 API**: 包含 `get`、`set`、`peek`、`contains`、`remove`、`clear` 等方法

## 快速开始

### 基本使用

```swift
// 创建容量为 3 的缓存
let cache = LRUCache<String, Int>(capacity: 3)

// 添加条目
cache.set("a", value: 1)
cache.set("b", value: 2)
cache.set("c", value: 3)

// 获取值（会更新为最近使用）
cache.get("a")  // 返回 1

// 添加第 4 个条目会淘汰最久未使用的 "b"
cache.set("d", value: 4)

cache.get("b")  // 返回 nil（已被淘汰）
```

### 下标语法

```swift
cache["key"] = 42     // 设置值
let value = cache["key"]  // 获取值
cache["key"] = nil     // 删除值
```

### TTL 过期设置

```swift
// 默认 TTL 60 秒
let cache = LRUCache<String, Data>(capacity: 100, defaultTTL: 60)

// 单独设置某个条目的 TTL
cache.set("key", value: data, ttl: 300)  // 5 分钟

// 手动清理过期条目
let removed = cache.removeExpired()
```

### 查看但不更新 LRU 顺序

```swift
// peek 不会改变条目的使用顺序
let value = cache.peek("key")
```

## API 参考

### 初始化

```swift
// 指定容量
init(capacity: Int, defaultTTL: TimeInterval? = nil)

// 默认容量 100
convenience init()
```

### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `count` | `Int` | 当前条目数量 |
| `isEmpty` | `Bool` | 是否为空 |
| `keys` | `[Key]` | 所有键 |
| `values` | `[Value]` | 所有值（MRU 到 LRU 顺序） |

### 方法

| 方法 | 描述 |
|------|------|
| `get(_ key:)` | 获取值，更新为最近使用 |
| `set(_ key:, value:, ttl:)` | 设置值，可指定 TTL |
| `peek(_ key:)` | 获取值，不更新 LRU 顺序 |
| `contains(_ key:)` | 检查键是否存在（不更新顺序） |
| `remove(_ key:)` | 删除指定键 |
| `clear()` | 清空缓存 |
| `removeExpired()` | 删除所有过期条目 |
| `getLRUKey()` | 获取最久未使用的键 |
| `getMRUKey()` | 获取最近使用的键 |

## 时间复杂度

| 操作 | 平均 | 最坏 |
|------|------|------|
| get | O(1) | O(n) |
| set | O(1) | O(n) |
| contains | O(1) | O(n) |
| remove | O(1) | O(n) |

## 使用场景

### 图片缓存

```swift
let imageCache = LRUCache<String, UIImage>(capacity: 50)

func loadImage(_ url: String) -> UIImage {
    if let cached = imageCache.get(url) {
        return cached
    }
    let image = downloadImage(from: url)
    imageCache.set(url, value: image)
    return image
}
```

### API 响应缓存

```swift
let responseCache = LRUCache<String, APIResponse>(capacity: 100, defaultTTL: 300)

func fetchAPI(_ endpoint: String) -> APIResponse {
    if let cached = responseCache.get(endpoint) {
        return cached
    }
    let response = callAPI(endpoint)
    responseCache.set(endpoint, value: response)
    return response
}
```

### 会话管理

```swift
let sessionCache = LRUCache<String, UserSession>(capacity: 1000, defaultTTL: 3600)

func getSession(_ token: String) -> UserSession? {
    return sessionCache.get(token)
}
```

## 文件说明

| 文件 | 描述 |
|------|------|
| `LRUCache.swift` | 主要实现 |
| `LRUCacheTests.swift` | 单元测试 |
| `main.swift` | 使用示例 |
| `README.md` | 本文档 |

## 运行测试

```bash
swift test
```

## 运行示例

```bash
swift run
```

## 许可证

MIT License