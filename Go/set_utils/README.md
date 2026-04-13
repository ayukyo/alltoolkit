# Go Set Utils - 泛型集合操作工具

零外部依赖的 Go 泛型集合工具库，提供高效的集合操作实现。

## 特性

- 🚀 **零依赖** - 仅使用 Go 标准库
- 🔧 **泛型支持** - Go 1.18+ 泛型，支持任意可比较类型
- ⚡ **高效实现** - 基于 map 的 O(1) 查找
- 📦 **完整功能** - 并集、交集、差集、对称差集等
- 🧪 **全面测试** - 100% 测试覆盖

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/set_utils
```

## 快速开始

### 创建集合

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/set_utils"
)

func main() {
    // 创建空集合
    s := set_utils.NewSet[int]()
    
    // 从切片创建（自动去重）
    s2 := set_utils.NewSetFromSlice([]int{1, 2, 2, 3, 3, 3})
    fmt.Println(s2.Size()) // 输出: 3
    
    // 添加元素
    s.Add(1)
    s.Add(2)
    s.Add(3)
    
    // 检查元素
    fmt.Println(s.Contains(2)) // 输出: true
    
    // 删除元素
    s.Remove(2)
}
```

### 集合操作

```go
s1 := set_utils.NewSetFromSlice([]int{1, 2, 3})
s2 := set_utils.NewSetFromSlice([]int{2, 3, 4})

// 并集: {1, 2, 3, 4}
union := set_utils.Union(s1, s2)

// 交集: {2, 3}
intersection := set_utils.Intersection(s1, s2)

// 差集 (s1 - s2): {1}
difference := set_utils.Difference(s1, s2)

// 对称差集: {1, 4}
symDiff := set_utils.SymmetricDifference(s1, s2)
```

### 子集判断

```go
s1 := set_utils.NewSetFromSlice([]int{1, 2})
s2 := set_utils.NewSetFromSlice([]int{1, 2, 3, 4})

set_utils.IsSubset(s1, s2)        // true: s1 是 s2 的子集
set_utils.IsSuperset(s2, s1)      // true: s2 是 s1 的超集
set_utils.IsProperSubset(s1, s2)  // true: s1 是 s2 的真子集
set_utils.AreDisjoint(s1, s2)     // false: s1 和 s2 有交集
set_utils.Equals(s1, s2)          // false: s1 不等于 s2
```

### 函数式操作

```go
s := set_utils.NewSetFromSlice([]int{1, 2, 3, 4, 5, 6})

// 过滤
evens := s.Filter(func(n int) bool {
    return n%2 == 0
})
// evens: {2, 4, 6}

// 映射
strings := set_utils.Map(s, func(n int) string {
    return fmt.Sprintf("num_%d", n)
})
// strings: {"num_1", "num_2", ...}

// 判断
allPositive := s.All(func(n int) bool { return n > 0 })  // true
hasEven := s.Any(func(n int) bool { return n%2 == 0 })   // true

// 遍历
s.Each(func(n int) {
    fmt.Println(n)
})
```

### 切片工具函数

```go
// 切片去重
unique := set_utils.UniqueSlice([]int{1, 2, 2, 3, 3, 3})
// unique: [1, 2, 3]

// 切片包含检查
hasValue := set_utils.SliceContains([]int{1, 2, 3}, 2)  // true

// 多切片并集
union := set_utils.SliceUnion([]int{1, 2}, []int{2, 3}, []int{3, 4})
// union: [1, 2, 3, 4]

// 多切片交集
intersection := set_utils.SliceIntersection([]int{1, 2, 3}, []int{2, 3, 4}, []int{2, 3, 5})
// intersection: [2, 3]

// 切片差集
diff := set_utils.SliceDifference([]int{1, 2, 3}, []int{2, 3, 4})
// diff: [1]
```

### 统计函数

```go
items := []string{"a", "b", "a", "c", "a", "b"}

// 计数
counts := set_utils.CountBy(items)
// counts: {"a": 3, "b": 2, "c": 1}

// 最频繁元素
mostFrequent := set_utils.MostFrequent(items)
// mostFrequent: ["a"]

// 最少出现元素
leastFrequent := set_utils.LeastFrequent(items)
// leastFrequent: ["c"]
```

## API 参考

### Set 类型

| 方法 | 描述 |
|------|------|
| `NewSet[T]() *Set[T]` | 创建空集合 |
| `NewSetFromSlice[T]([]T) *Set[T]` | 从切片创建集合 |
| `Add(item T) bool` | 添加元素，返回是否新增 |
| `Remove(item T) bool` | 删除元素，返回是否删除 |
| `Contains(item T) bool` | 检查元素是否存在 |
| `Size() int` | 返回元素数量 |
| `IsEmpty() bool` | 检查是否为空 |
| `Clear()` | 清空集合 |
| `ToSlice() []T` | 转换为切片 |
| `Clone() *Set[T]` | 克隆集合 |
| `Filter(func(T) bool) *Set[T]` | 过滤元素 |
| `Each(func(T))` | 遍历元素 |
| `Any(func(T) bool) bool` | 是否存在满足条件的元素 |
| `All(func(T) bool) bool` | 是否所有元素都满足条件 |

### 集合操作函数

| 函数 | 描述 |
|------|------|
| `Union(s1, s2) *Set[T]` | 并集 |
| `Intersection(s1, s2) *Set[T]` | 交集 |
| `Difference(s1, s2) *Set[T]` | 差集 (s1 - s2) |
| `SymmetricDifference(s1, s2) *Set[T]` | 对称差集 |
| `IsSubset(s1, s2) bool` | s1 是否为 s2 的子集 |
| `IsSuperset(s1, s2) bool` | s1 是否为 s2 的超集 |
| `IsProperSubset(s1, s2) bool` | s1 是否为 s2 的真子集 |
| `IsProperSuperset(s1, s2) bool` | s1 是否为 s2 的真超集 |
| `Equals(s1, s2) bool` | 两集合是否相等 |
| `AreDisjoint(s1, s2) bool` | 两集合是否无交集 |
| `Map(s, func(T) U) *Set[U]` | 映射转换 |
| `ToSortedSlice[T](s) []T` | 返回排序后的切片 |

### 切片工具函数

| 函数 | 描述 |
|------|------|
| `UniqueSlice[T]([]T) []T` | 切片去重 |
| `UniqueSliceInPlace[T](*[]T)` | 原地去重 |
| `SliceContains[T]([]T, T) bool` | 切片包含检查 |
| `SliceUnion[T](...[]T) []T` | 多切片并集 |
| `SliceIntersection[T](...[]T) []T` | 多切片交集 |
| `SliceDifference[T](s1, s2 []T) []T` | 切片差集 |
| `SliceSymmetricDifference[T](s1, s2 []T) []T` | 切片对称差集 |
| `CountBy[T]([]T) map[T]int` | 元素计数 |
| `MostFrequent[T]([]T) []T` | 最频繁元素 |
| `LeastFrequent[T]([]T) []T` | 最少出现元素 |

## 时间复杂度

| 操作 | 复杂度 |
|------|--------|
| Add | O(1) |
| Remove | O(1) |
| Contains | O(1) |
| Size | O(1) |
| Union | O(n + m) |
| Intersection | O(min(n, m)) |
| Difference | O(n) |

## 示例：使用场景

### 用户权限检查

```go
requiredPerms := set_utils.NewSetFromSlice([]string{"read", "write"})
userPerms := set_utils.NewSetFromSlice([]string{"read", "write", "delete"})

if set_utils.IsSuperset(userPerms, requiredPerms) {
    fmt.Println("用户拥有所有必需权限")
}
```

### 找出两个列表的差异

```go
oldUsers := []string{"alice", "bob", "charlie"}
newUsers := []string{"alice", "bob", "david"}

added := set_utils.SliceDifference(newUsers, oldUsers)    // ["david"]
removed := set_utils.SliceDifference(oldUsers, newUsers)  // ["charlie"]
```

### 数据分析

```go
tags := []string{"go", "rust", "go", "python", "rust", "go"}
popularTags := set_utils.MostFrequent(tags)
fmt.Println("最受欢迎的标签:", popularTags) // ["go"]
```

## 运行测试

```bash
cd Go/set_utils
go test -v
```

## 基准测试

```bash
go test -bench=.
```

## 许可证

MIT License