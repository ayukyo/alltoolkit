# Bloom Filter Utils - Kotlin 布隆过滤器工具

高效的概率数据结构实现，用于快速判断元素是否在集合中。

## 特性

- **零外部依赖** - 纯Kotlin标准库实现
- **三种过滤器类型**：
  - `BloomFilter` - 标准布隆过滤器
  - `ScalableBloomFilter` - 可扩展布隆过滤器
  - `CountingBloomFilter` - 计数布隆过滤器（支持删除）
- **序列化支持** - 可序列化为字节数组，便于持久化
- **内存高效** - 相比HashSet可节省90%以上内存

## 文件结构

```
bloom_filter_utils/
├── BloomFilter.kt         # 核心实现
├── BloomFilterTest.kt     # 测试套件
├── BloomFilterExample.kt  # 使用示例
└── README.md              # 本文档
```

## 快速开始

### 基础用法

```kotlin
import bloom_filter_utils.BloomFilter

// 创建布隆过滤器
val filter = BloomFilter<String>(expectedInsertions = 10000, fpp = 0.01)

// 添加元素
filter.add("hello")
filter.addAll(listOf("world", "kotlin"))

// 检查元素
filter.mightContain("hello")        // true - 可能存在
filter.definitelyNotContains("xyz") // true - 一定不存在

// 获取统计信息
println(filter) // BloomFilter(inserted=3, bitSize=95850, hashCount=6, estimatedFpp=0.000000)
```

### 可扩展布隆过滤器

```kotlin
import bloom_filter_utils.ScalableBloomFilter

// 当元素超过预期时自动扩展
val filter = ScalableBloomFilter<String>(initialCapacity = 100)

for (i in 1..10000) {
    filter.add("item_$i")
}

println(filter.filterCount()) // 过滤器数量
println(filter.memoryUsage()) // 内存使用
```

### 计数布隆过滤器

```kotlin
import bloom_filter_utils.CountingBloomFilter

// 支持删除操作
val filter = CountingBloomFilter<String>(expectedInsertions = 1000)

filter.add("hello")
filter.mightContain("hello") // true
filter.remove("hello")
filter.mightContain("hello") // false
```

### 序列化

```kotlin
// 序列化
val bytes = filter.toByteArray()

// 反序列化
val restored = BloomFilter.fromByteArray<String>(bytes)
```

## 应用场景

1. **URL去重** - 爬虫中快速判断URL是否已爬取
2. **缓存穿透防护** - 防止恶意请求穿透缓存直达数据库
3. **垃圾邮件过滤** - 快速识别垃圾邮件URL
4. **UV统计** - 网站独立访客计数
5. **拼写检查** - 快速判断单词是否在词典中
6. **黑名单检测** - 快速检查是否在黑名单

## 性能特点

- **时间复杂度**: O(k)，其中k是哈希函数数量
- **空间复杂度**: O(m)，其中m是位数组大小
- **假阳性**: 可能存在，概率可配置
- **假阴性**: 不存在

## API参考

### BloomFilter

| 方法 | 说明 |
|------|------|
| `add(element)` | 添加元素 |
| `addAll(elements)` | 批量添加 |
| `mightContain(element)` | 检查是否可能存在 |
| `definitelyNotContains(element)` | 检查是否一定不存在 |
| `size()` | 获取已插入数量 |
| `clear()` | 清空过滤器 |
| `isEmpty()` | 是否为空 |
| `estimateFpp()` | 估计当前假阳性概率 |
| `memoryUsage()` | 内存使用量（字节） |
| `toByteArray()` | 序列化为字节数组 |

### ScalableBloomFilter

| 方法 | 说明 |
|------|------|
| `add(element)` | 添加元素（自动扩展） |
| `mightContain(element)` | 检查是否可能存在 |
| `filterCount()` | 获取内部过滤器数量 |
| `clear()` | 清空所有过滤器 |

### CountingBloomFilter

| 方法 | 说明 |
|------|------|
| `add(element)` | 添加元素 |
| `remove(element)` | 删除元素 |
| `mightContain(element)` | 检查是否可能存在 |

## 参数选择指南

```kotlin
// 高精度场景（假阳性率 < 0.1%）
BloomFilter<String>(100000, 0.001)

// 平衡场景（假阳性率 ≈ 1%）
BloomFilter<String>(100000, 0.01)

// 内存优先场景（假阳性率 ≈ 3%）
BloomFilter<String>(100000, 0.03)
```

## 作者

AllToolkit Auto-Generator

## 日期

2026-04-13