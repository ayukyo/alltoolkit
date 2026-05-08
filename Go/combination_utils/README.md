# Combination Utils

组合数学工具库，提供组合和排列的生成与计算功能。零外部依赖，纯 Go 标准库实现。

## 功能特性

- **组合生成**: 生成 n 个元素中选 k 个的所有组合
- **排列生成**: 生成所有全排列
- **k-排列**: 生成 k 个元素的有序排列
- **重复组合**: 允许元素重复选择的组合
- **幂集**: 生成所有子集
- **笛卡尔积**: 多个集合的笛卡尔积
- **多重集排列**: 处理重复元素的唯一排列
- **计数函数**: 计算组合数、排列数等数学函数
- **通道生成器**: 内存友好的生成器模式

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/combination_utils
```

## 快速开始

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/combination_utils"
)

func main() {
    // 生成组合
    nums := []int{1, 2, 3, 4}
    combos := combination_utils.Combinations(nums, 2)
    fmt.Println("C(4,2) =", combos)
    // 输出: [[1 2] [1 3] [1 4] [2 3] [2 4] [3 4]]

    // 生成排列
    perms := combination_utils.Permutations([]int{1, 2, 3})
    fmt.Println("P(3) =", perms)
    // 输出: [[1 2 3] [1 3 2] [2 1 3] [2 3 1] [3 1 2] [3 2 1]]

    // 计算组合数
    n, _ := combination_utils.BinomialCoefficient(10, 3)
    fmt.Println("C(10,3) =", n)
    // 输出: 120
}
```

## API 文档

### 组合相关

#### Combinations[T any](slice []T, k int) [][]T
生成从 n 个元素中选择 k 个的所有组合（无序，不重复）。

```go
result := combination_utils.Combinations([]string{"a", "b", "c"}, 2)
// 输出: [[a b] [a c] [b c]]
```

#### CombinationsChan[T any](slice []T, k int) <-chan []T
通过通道生成组合，适用于大数据集。

```go
for combo := range combination_utils.CombinationsChan(nums, 3) {
    process(combo)
}
```

#### CombinationsWithRepetition[T any](slice []T, k int) [][]T
生成允许重复的组合。

```go
result := combination_utils.CombinationsWithRepetition([]int{1, 2}, 3)
// 输出: [[1 1 1] [1 1 2] [1 2 2] [2 2 2]]
```

### 排列相关

#### Permutations[T any](slice []T) [][]T
生成所有全排列。

```go
result := combination_utils.Permutations([]int{1, 2, 3})
// 输出: 6 种排列
```

#### PermutationsChan[T any](slice []T) <-chan []T
通过通道生成排列。

#### PermutationsK[T any](slice []T, k int) [][]T
生成 k-排列（从 n 个元素中选 k 个的有序排列）。

```go
result := combination_utils.PermutationsK([]int{1, 2, 3, 4}, 2)
// 输出: [[1 2] [1 3] [1 4] [2 1] [2 3] [2 4] [3 1] [3 2] [3 4] [4 1] [4 2] [4 3]]
```

### 幂集

#### PowerSet[T any](slice []T) [][]T
生成所有子集（2^n 个）。

```go
result := combination_utils.PowerSet([]int{1, 2})
// 输出: [[] [1] [2] [1 2]]
```

#### PowerSetChan[T any](slice []T) <-chan []T
通过通道生成幂集。

### 笛卡尔积

#### CartesianProduct[T any](slices ...[]T) [][]T
计算多个集合的笛卡尔积。

```go
result := combination_utils.CartesianProduct(
    []string{"a", "b"},
    []string{"x", "y"},
)
// 输出: [[a x] [a y] [b x] [b y]]
```

### 多重集排列

#### MultiSetPermutation[T comparable](elements []T) [][]T
生成有重复元素时的唯一排列。

```go
result := combination_utils.MultiSetPermutation([]int{1, 1, 2})
// 输出: [[1 1 2] [1 2 1] [2 1 1]]
```

### 计数函数

#### BinomialCoefficient(n, k int) (int, error)
计算二项式系数 C(n, k)。

```go
n, _ := combination_utils.BinomialCoefficient(5, 2)
// 输出: 10
```

#### Factorial(n int) (int, error)
计算阶乘 n!。

```go
n, _ := combination_utils.Factorial(5)
// 输出: 120
```

#### CountPermutations(n, k int) (int, error)
计算 k-排列数 P(n, k)。

```go
n, _ := combination_utils.CountPermutations(5, 3)
// 输出: 60
```

#### CountPowerSet(n int) int
计算幂集大小（2^n）。

#### CombinationsWithRepetitionCount(n, k int) (int, error)
计算允许重复的组合数 C(n+k-1, k)。

#### CartesianProductCount(lengths ...int) (int, error)
计算笛卡尔积大小。

#### MultiSetPermutationCount(total int, counts ...int) (int, error)
计算多重集排列数。

## 性能说明

- **组合算法**: 使用字典序生成，时间复杂度 O(C(n,k) × k)
- **排列算法**: 使用 Heap 算法，时间复杂度 O(n!)
- **幂集**: 位运算实现，时间复杂度 O(2^n)
- **通道生成器**: 内存友好，适用于大数据集

## 测试

```bash
go test -v ./...
```

基准测试：

```bash
go test -bench=. -benchmem
```

## 使用示例

见 [examples/main.go](examples/main.go)

## 许可证

MIT License