# slice_utils

全面的 Go 切片操作工具库，零外部依赖，仅使用 Go 标准库。

## 功能特性

### 基础操作
- `Contains` - 检查切片是否包含元素
- `ContainsAll` - 检查是否包含所有指定元素
- `ContainsAny` - 检查是否包含任意指定元素
- `IndexOf` - 获取元素首次出现的索引
- `LastIndexOf` - 获取元素最后出现的索引
- `Count` - 统计元素出现次数
- `CountBy` - 按条件统计元素数量

### 转换操作
- `Map` - 转换每个元素
- `Filter` - 筛选符合条件的元素
- `Reject` - 筛选不符合条件的元素
- `Reduce` - 累积计算（从左到右）
- `ReduceRight` - 累积计算（从右到左）
- `ForEach` - 对每个元素执行操作
- `ForEachWithIndex` - 带索引遍历
- `FlatMap` - 映射并扁平化

### 切片操作
- `Chunk` - 分块
- `Flatten` - 扁平化二维切片
- `Reverse` - 原位反转
- `Reversed` - 返回反转后的新切片
- `Slice` - 安全切片
- `Take` - 取前 n 个元素
- `TakeWhile` - 取满足条件的元素直到不满足
- `TakeLast` - 取后 n 个元素
- `Drop` - 删除前 n 个元素
- `DropWhile` - 删除满足条件的元素直到不满足
- `DropLast` - 删除后 n 个元素

### 集合操作
- `Unique` - 去重（保持顺序）
- `UniqueBy` - 按键去重
- `Union` - 并集
- `Intersection` - 交集
- `Difference` - 差集
- `SymmetricDifference` - 对称差集
- `IsSubset` - 子集判断
- `IsSuperset` - 超集判断

### 排序与极值
- `SortBy` - 按键排序（原位）
- `SortByDesc` - 按键降序排序
- `SortedBy` - 返回排序后的新切片
- `Min` - 最小值
- `Max` - 最大值
- `MinBy` - 按键取最小
- `MaxBy` - 按键取最大

### 搜索操作
- `Find` - 查找第一个满足条件的元素
- `FindIndex` - 查找第一个满足条件的索引
- `FindLast` - 查找最后一个满足条件的元素
- `FindLastIndex` - 查找最后一个满足条件的索引
- `FindAll` - 查找所有满足条件的元素
- `Every` - 所有元素都满足条件
- `Some` - 存在元素满足条件
- `None` - 所有元素都不满足条件

### 分组与分区
- `Partition` - 按条件分区
- `GroupBy` - 按键分组
- `GroupByToMap` - 分组并转换值
- `CountByKeys` - 按键统计数量

### 增删改操作
- `Insert` - 在指定位置插入元素
- `InsertAll` - 在指定位置插入多个元素
- `Remove` - 删除指定位置的元素
- `RemoveFirst` - 删除首次出现的元素
- `RemoveAll` - 删除所有出现的元素
- `Replace` - 替换指定位置的元素
- `ReplaceAll` - 替换所有匹配的元素

### 随机与抽样
- `Shuffle` - 原位随机打乱
- `Shuffled` - 返回打乱后的新切片
- `Sample` - 随机抽取 n 个元素
- `RandomElement` - 随机取一个元素

### 实用工具
- `Clone` - 浅拷贝
- `Concat` - 合并多个切片
- `Repeat` - 创建重复元素的切片
- `Range` - 创建整数范围
- `RangeWithStep` - 带步长的整数范围
- `Fill` - 填充切片
- `IsEmpty` / `IsNotEmpty` - 空切片判断
- `Length` - 获取长度
- `First` / `Last` / `Second` / `Third` - 取特定位置元素
- `Nth` - 取第 n 个元素（支持负索引）
- `Head` / `Tail` / `Init` - 头尾操作
- `Equal` / `DeepEqual` - 切片比较

### 统计计算
- `Sum` - 求和
- `Product` - 求积
- `Average` - 平均值
- `Median` - 中位数
- `Mode` - 众数

### Zip/Unzip 操作
- `Zip` - 合并两个切片为 Pair 切片
- `Unzip` - 分离 Pair 切片为两个切片
- `ZipWith` - 合并两个切片并转换

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/slice_utils
```

## 快速开始

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/slice_utils"
)

func main() {
    numbers := []int{1, 2, 3, 4, 5}
    
    // 基础操作
    fmt.Println(slice_utils.Contains(numbers, 3))  // true
    fmt.Println(slice_utils.IndexOf(numbers, 3))   // 2
    
    // 转换
    doubled := slice_utils.Map(numbers, func(n int) int { return n * 2 })
    fmt.Println(doubled)  // [2, 4, 6, 8, 10]
    
    // 筛选
    evens := slice_utils.Filter(numbers, func(n int) bool { return n % 2 == 0 })
    fmt.Println(evens)  // [2, 4]
    
    // 累积
    sum := slice_utils.Reduce(numbers, 0, func(acc, n int) int { return acc + n })
    fmt.Println(sum)  // 15
    
    // 集合操作
    a := []int{1, 2, 3}
    b := []int{3, 4, 5}
    fmt.Println(slice_utils.Union(a, b))          // [1, 2, 3, 4, 5]
    fmt.Println(slice_utils.Intersection(a, b))   // [3]
    
    // 分块
    chunks, _ := slice_utils.Chunk(numbers, 2)
    fmt.Println(chunks)  // [[1, 2], [3, 4], [5]]
    
    // 分组
    groups := slice_utils.GroupBy(numbers, func(n int) int { return n % 2 })
    fmt.Println(groups[0])  // [2, 4] (偶数)
    fmt.Println(groups[1])  // [1, 3, 5] (奇数)
}
```

## 泛型支持

所有函数都支持 Go 1.18+ 的泛型，可用于任意类型：

```go
// 整数切片
ints := []int{1, 2, 3}
doubled := slice_utils.Map(ints, func(n int) int { return n * 2 })

// 字符串切片
strings := []string{"a", "b", "c"}
upper := slice_utils.Map(strings, func(s string) string { return strings.ToUpper(s) })

// 自定义类型
type Person struct {
    Name string
    Age  int
}
people := []Person{{"Alice", 30}, {"Bob", 25}}
adults := slice_utils.Filter(people, func(p Person) bool { return p.Age >= 18 })
```

## 测试

```bash
cd Go/slice_utils
go test -v
```

运行基准测试：

```bash
go test -bench=.
```

## 设计原则

1. **零外部依赖** - 仅使用 Go 标准库
2. **泛型支持** - 所有函数支持任意类型
3. **原位 vs 新切片** - 明确区分修改原切片和返回新切片的函数
4. **错误处理** - 边界错误返回 error，避免 panic
5. **性能优化** - 使用预分配减少内存分配

## License

MIT