# ring_buffer_utils

Go 循环缓冲区（环形缓冲区）工具库 - 零依赖，生产就绪。

## 功能特性

- ✅ **零外部依赖** - 仅使用 Go 标准库
- ✅ **泛型支持** - Go 1.18+ 泛型实现
- ✅ **线程安全** - 可选的并发安全模式
- ✅ **完整统计** - NumericRingBuffer 提供均值、方差、标准差等
- ✅ **实用工具** - 滑动窗口、批量处理等辅助函数

## 安装

```go
import rb "github.com/ayukyo/alltoolkit/Go/ring_buffer_utils"
```

## 快速开始

### 基础 Ring Buffer

```go
// 创建容量为 5 的缓冲区
buffer := rb.NewRingBuffer[int](5)

// 添加元素
buffer.Push(1)
buffer.Push(2)
buffer.Push(3)

// 获取内容
fmt.Println(buffer.ToSlice())  // [1, 2, 3]

// 缓冲区满时自动覆盖最旧元素
buffer.Extend([]int{4, 5, 6})
fmt.Println(buffer.ToSlice())  // [2, 3, 4, 5, 6]
```

### 线程安全版本

```go
// 创建线程安全缓冲区
buffer := rb.NewThreadSafeRingBuffer[int](100)

// 可安全在多个 goroutine 中使用
go func() { buffer.Push(1) }()
go func() { buffer.Pop() }()
go func() { buffer.Len() }()
```

### 队列操作

```go
buffer := rb.NewRingBuffer[string](10)
buffer.Extend([]string{"a", "b", "c"})

// 查看最新元素（不删除）
newest, _ := buffer.Peek()
fmt.Println(newest)  // "c"

// 查看最旧元素（不删除）
oldest, _ := buffer.PeekLeft()
fmt.Println(oldest)  // "a"

// 弹出最旧元素
front, _ := buffer.PopLeft()
fmt.Println(front)  // "a"

// 弹出最新元素
back, _ := buffer.Pop()
fmt.Println(back)  // "c"
```

## NumericRingBuffer 统计功能

数值型缓冲区提供丰富的统计功能：

```go
nrb := rb.NewNumericRingBuffer(100)

// 添加数据
nrb.Extend([]float64{23.5, 24.1, 23.8, 24.5, 25.0})

// 统计计算
mean, _ := nrb.Mean()         // 均值
stdDev, _ := nrb.StdDev()     // 标准差
min, _ := nrb.Min()           // 最小值
max, _ := nrb.Max()           // 最大值
median, _ := nrb.Median()     // 中位数
p75, _ := nrb.Percentile(75)  // 百分位数

// 移动平均
ma5, _ := nrb.MovingAverage(5)
```

## 实用工具函数

### 滑动窗口

```go
data := []int{1, 2, 3, 4, 5}
windows := rb.SlidingWindow(data, 3)
// [[1,2,3], [2,3,4], [3,4,5]]
```

### 批量处理

```go
data := []int{1, 2, 3, 4, 5, 6, 7}
sums := rb.Batch(data, 3, func(batch []int) int {
    sum := 0
    for _, v := range batch {
        sum += v
    }
    return sum
})
// [6, 15, 7] -> (1+2+3), (4+5+6), (7)
```

## API 参考

### RingBuffer[T]

| 方法 | 描述 |
|------|------|
| `NewRingBuffer[T](capacity)` | 创建新缓冲区 |
| `NewThreadSafeRingBuffer[T](capacity)` | 创建线程安全缓冲区 |
| `Push(item)` | 添加元素，返回被覆盖的元素 |
| `Pop()` | 弹出最新元素 |
| `PopLeft()` | 弹出最旧元素 |
| `Peek()` | 查看最新元素 |
| `PeekLeft()` | 查看最旧元素 |
| `Get(index)` | 获取指定索引元素 |
| `Set(index, item)` | 设置指定索引元素 |
| `Len()` | 当前元素数量 |
| `Cap()` | 缓冲区容量 |
| `IsFull()` | 是否已满 |
| `IsEmpty()` | 是否为空 |
| `Clear()` | 清空缓冲区 |
| `ToSlice()` | 转换为切片 |
| `Extend(items)` | 批量添加 |
| `ForEach(fn)` | 迭代元素 |
| `Contains(item, equal)` | 检查元素是否存在 |
| `Reverse()` | 反序返回 |
| `Copy()` | 创建副本 |

### NumericRingBuffer

| 方法 | 描述 |
|------|------|
| `NewNumericRingBuffer(capacity)` | 创建数值缓冲区 |
| `NewThreadSafeNumericRingBuffer(capacity)` | 创建线程安全数值缓冲区 |
| `Mean()` | 均值 |
| `Sum()` | 总和 |
| `Variance()` | 样本方差 |
| `StdDev()` | 标准差 |
| `Min()` | 最小值 |
| `Max()` | 最大值 |
| `Range()` | 最大值-最小值 |
| `Median()` | 中位数 |
| `Percentile(p)` | 百分位数 (0-100) |
| `MovingAverage(window)` | 移动平均 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `SlidingWindow[T](data, size)` | 滑动窗口迭代 |
| `Batch[T, R](data, size, processor)` | 批量处理 |

## 应用场景

- **滚动窗口统计** - 实时计算均值、标准差
- **事件日志缓冲** - 保留最近 N 条日志
- **数据流处理** - 处理连续数据流
- **股票监控** - 移动平均计算
- **系统监控** - CPU/内存使用率追踪
- **传感器数据** - 实时统计计算

## 性能

- `Push`: O(1)
- `Pop/PopLeft`: O(1)
- `Peek/PeekLeft`: O(1)
- `Get/Set`: O(1)
- `ToSlice`: O(n)
- `Mean/Sum`: O(1) (实时更新)
- `MovingAverage`: O(n)
- `Median/Percentile`: O(n log n)

## 测试

```bash
cd Go/ring_buffer_utils
go test -v
go test -bench=.
go test -race  # 竞态检测
```

## 许可证

MIT License