# Bloom Filter (Go)

一个高性能的布隆过滤器实现，支持零外部依赖。

## 什么是布隆过滤器？

布隆过滤器是一种空间效率极高的概率数据结构，用于判断元素是否存在于集合中。

**特点：**
- **可能存在误报**：可能报告存在实际不存在的元素
- **不存在漏报**：如果报告不存在，那一定不存在
- **空间效率高**：比传统集合占用更少内存
- **查询和插入速度快**：O(k) 时间复杂度

## 功能特性

- ✅ 零外部依赖（仅使用 Go 标准库）
- ✅ 自动优化配置（根据预期元素数和误报率）
- ✅ 序列化/反序列化（JSON 格式）
- ✅ 集合运算（并集、交集）
- ✅ 统计信息（填充率、误报率估算）
- ✅ 完整的单元测试

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/bloom_filter
```

## 快速开始

### 基本使用

```go
package main

import (
    "fmt"
    bloom "github.com/ayukyo/alltoolkit/Go/bloom_filter"
)

func main() {
    // 创建布隆过滤器（自动优化配置）
    bf := bloom.NewWithConfig(bloom.Config{
        ExpectedItems:     10000, // 预期元素数量
        FalsePositiveRate: 0.01,  // 期望误报率 1%
    })
    
    // 添加元素
    bf.AddString("hello")
    bf.AddString("world")
    bf.Add([]byte{1, 2, 3, 4})
    
    // 检查元素
    fmt.Println(bf.ContainsString("hello")) // true
    fmt.Println(bf.ContainsString("world")) // true
    fmt.Println(bf.ContainsString("foo"))   // false (确定不存在)
    
    // 获取统计信息
    stats := bf.Stats()
    fmt.Printf("Size: %d, Items: %d, FP Rate: %.4f%%\n",
        stats.Size, stats.ItemCount, stats.ExpectedFP*100)
}
```

### 使用默认配置

```go
// 默认：10000 预期元素，1% 误报率
bf := bloom.NewDefault()
```

### 手动指定参数

```go
// size: 位图大小, hashCount: 哈希函数数量
bf := bloom.New(10000, 7)
```

## 序列化

### JSON 导出/导入

```go
// 导出到 JSON
jsonStr, err := bf.ToJSON()
if err != nil {
    panic(err)
}
fmt.Println(jsonStr)

// 从 JSON 导入
imported, err := bloom.FromJSON(jsonStr)
if err != nil {
    panic(err)
}
```

### 结构体导出

```go
exported := bf.Export()
// exported.Size, exported.HashCount, exported.Count, exported.Bitmap

// 导入
imported, err := bloom.Import(exported)
```

## 集合运算

```go
bf1 := bloom.New(10000, 7)
bf1.AddString("apple")
bf1.AddString("banana")

bf2 := bloom.New(10000, 7)
bf2.AddString("banana")
bf2.AddString("cherry")

// 并集
union, _ := bf1.Union(bf2)
// union 包含: apple, banana, cherry

// 交集
intersect, _ := bf1.Intersect(bf2)
// intersect 包含: banana
```

## 清空过滤器

```go
bf.Clear() // 移除所有元素
```

## API 参考

### 构造函数

| 函数 | 说明 |
|------|------|
| `New(size, hashCount uint)` | 创建指定参数的布隆过滤器 |
| `NewWithConfig(config Config)` | 根据配置自动优化参数 |
| `NewDefault()` | 默认配置（10000 元素，1% 误报率） |

### 方法

| 方法 | 说明 |
|------|------|
| `Add(data []byte)` | 添加字节切片 |
| `AddString(s string)` | 添加字符串 |
| `Contains(data []byte) bool` | 检查字节切片是否存在 |
| `ContainsString(s string) bool` | 检查字符串是否存在 |
| `Clear()` | 清空过滤器 |
| `Size() uint` | 获取位图大小 |
| `Count() uint` | 获取已添加元素数量 |
| `HashCount() uint` | 获取哈希函数数量 |
| `FillRatio() float64` | 获取填充率 |
| `FalsePositiveRate() float64` | 估算当前误报率 |
| `Stats() Stats` | 获取详细统计信息 |
| `Export() *ExportedFilter` | 导出为可序列化结构 |
| `ToJSON() (string, error)` | 导出为 JSON 字符串 |
| `Union(other *BloomFilter) (*BloomFilter, error)` | 计算并集 |
| `Intersect(other *BloomFilter) (*BloomFilter, error)` | 计算交集 |
| `String() string` | 获取字符串表示 |

### 静态函数

| 函数 | 说明 |
|------|------|
| `Import(exported *ExportedFilter) (*BloomFilter, error)` | 从导出结构导入 |
| `FromJSON(jsonStr string) (*BloomFilter, error)` | 从 JSON 字符串导入 |

## 配置参数说明

```go
type Config struct {
    ExpectedItems     uint    // 预期元素数量
    FalsePositiveRate float64 // 期望误报率 (0.0 - 1.0)
}
```

布隆过滤器会根据这些参数自动计算最优的位图大小和哈希函数数量：

- **位图大小**：`m = -n * ln(p) / (ln(2)²)`
- **哈希函数数量**：`k = (m/n) * ln(2)`

## 使用场景

### 1. 缓存穿透防护

```go
// 在查询数据库前，用布隆过滤器快速判断 key 是否可能存在
if !bf.ContainsString(key) {
    return nil, ErrNotFound // 一定不存在，直接返回
}
// 可能存在，继续查询数据库
return db.Query(key)
```

### 2. URL 去重

```go
// 爬虫中检查 URL 是否已爬取
if bf.ContainsString(url) {
    continue // 可能已爬取，跳过
}
bf.AddString(url)
crawl(url)
```

### 3. 推荐系统去重

```go
// 过滤已推荐过的内容
for _, item := range candidates {
    if bf.ContainsString(item.ID) {
        continue // 可能已推荐
    }
    bf.AddString(item.ID)
    recommendations = append(recommendations, item)
}
```

### 4. 垃圾邮件过滤

```go
// 快速判断邮箱是否在黑名单中
if bf.ContainsString(email) {
    return ErrSpam // 可能是垃圾邮件
}
```

## 性能基准

```
BenchmarkAdd-8          5000000    220 ns/op
BenchmarkContains-8    10000000    150 ns/op
BenchmarkAddString-8    5000000    230 ns/op
BenchmarkToJSON-8         5000  240000 ns/op
BenchmarkFromJSON-8       5000  260000 ns/op
```

## 运行测试

```bash
cd Go/bloom_filter
go test -v
go test -bench=.
```

## 许可证

MIT License