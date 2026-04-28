# Counter Utils

线程安全的计数器工具模块，支持原子操作、命名计数器管理、快照、统计信息和速率计算。

## 功能特性

- **Counter**: 单计数器，支持原子递增/递减/获取/设置/重置
- **CounterManager**: 命名计数器管理器，支持多计数器管理
- **Snapshot**: 计数器快照，捕获某一时刻所有计数器的值
- **StatsCollector**: 统计收集器，记录最小值/最大值/平均值
- **RateCounter**: 速率计数器，测量事件在时间窗口内的速率
- **BucketCounter**: 桶计数器，按时间窗口分桶统计

## 使用示例

### 基础计数器

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    // 创建计数器
    counter := counter_utils.NewCounter()
    
    // 递增
    counter.Increment()
    counter.IncrementBy(10)
    
    // 获取值
    fmt.Printf("值: %d\n", counter.Get()) // 输出: 值: 11
    
    // 递减
    counter.Decrement()
    counter.DecrementBy(5)
    
    fmt.Printf("值: %d\n", counter.Get()) // 输出: 值: 5
    
    // 重置
    prev := counter.Reset()
    fmt.Printf("重置前的值: %d\n", prev) // 输出: 重置前的值: 5
}
```

### 命名计数器管理器

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    cm := counter_utils.NewCounterManager()
    
    // 自动创建并递增命名计数器
    cm.Increment("requests")
    cm.Increment("requests")
    cm.IncrementBy("requests", 10)
    
    cm.Increment("errors")
    cm.Increment("errors")
    
    // 获取所有计数器值
    all := cm.GetAll()
    for name, value := range all {
        fmt.Printf("%s: %d\n", name, value)
    }
    // 输出:
    // requests: 12
    // errors: 2
    
    // 获取单个计数器值
    fmt.Printf("请求总数: %d\n", cm.GetValue("requests"))
    
    // 重置单个计数器
    cm.Reset("errors")
    
    // 重置所有计数器
    cm.ResetAll()
}
```

### 快照功能

```go
package main

import (
    "fmt"
    "time"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    cm := counter_utils.NewCounterManager()
    
    // 记录一些数据
    cm.IncrementBy("requests", 100)
    cm.IncrementBy("errors", 5)
    
    // 拍摄快照
    snapshot := cm.TakeSnapshot()
    fmt.Printf("快照时间: %s\n", snapshot.Timestamp.Format(time.RFC3339))
    fmt.Printf("请求数: %d\n", snapshot.Values["requests"])
    
    // 继续记录
    cm.Increment("requests")
    
    // 快照值不变
    fmt.Printf("快照中的请求数: %d\n", snapshot.Values["requests"]) // 还是 100
    fmt.Printf("当前请求数: %d\n", cm.GetValue("requests"))       // 101
    
    // 查看历史快照
    history := cm.GetHistory()
    fmt.Printf("历史快照数: %d\n", len(history))
}
```

### 统计收集器

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    sc := counter_utils.NewStatsCollector()
    
    // 记录温度读数
    readings := []int64{20, 22, 25, 23, 18, 21, 24, 26, 22, 20}
    for _, temp := range readings {
        sc.Record("temperature", temp)
    }
    
    // 获取统计信息
    stats := sc.GetStats("temperature")
    fmt.Printf("当前值: %d\n", stats.Value)
    fmt.Printf("最小值: %d\n", stats.Min)
    fmt.Printf("最大值: %d\n", stats.Max)
    fmt.Printf("平均值: %.2f\n", stats.Avg)
    fmt.Printf("记录次数: %d\n", stats.Count)
}
```

### 速率计数器

```go
package main

import (
    "fmt"
    "time"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    // 创建一个 1 分钟窗口的速率计数器
    rc := counter_utils.NewRateCounter(time.Minute)
    
    // 模拟事件
    for i := 0; i < 100; i++ {
        rc.Record()
        time.Sleep(10 * time.Millisecond)
    }
    
    fmt.Printf("窗口内事件数: %d\n", rc.Count())
    fmt.Printf("每秒速率: %.2f\n", rc.Rate())
    
    // 重置
    rc.Reset()
    fmt.Printf("重置后事件数: %d\n", rc.Count())
}
```

### 桶计数器

```go
package main

import (
    "fmt"
    "time"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    // 创建一个 10 个桶、每桶 1 秒的计数器
    bc := counter_utils.NewBucketCounter(time.Second, 10)
    
    // 记录事件
    for i := 0; i < 50; i++ {
        bc.Increment()
        time.Sleep(100 * time.Millisecond)
    }
    
    // 获取总数
    fmt.Printf("总事件数: %d\n", bc.Total())
    
    // 获取所有桶的值
    buckets := bc.GetAllBuckets()
    for i, v := range buckets {
        fmt.Printf("桶 %d: %d\n", i, v)
    }
}
```

### 并发安全

所有组件都是线程安全的，可以在多个 goroutine 中安全使用：

```go
package main

import (
    "sync"
    "github.com/ayukyo/alltoolkit/Go/counter_utils"
)

func main() {
    counter := counter_utils.NewCounter()
    var wg sync.WaitGroup
    
    // 100 个 goroutine，每个递增 1000 次
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := 0; j < 1000; j++ {
                counter.Increment()
            }
        }()
    }
    
    wg.Wait()
    
    // 结果应该是 100000
    println(counter.Get()) // 输出: 100000
}
```

## API 参考

### Counter

| 方法 | 说明 |
|------|------|
| `NewCounter() *Counter` | 创建值为 0 的计数器 |
| `NewCounterWithValue(v int64) *Counter` | 创建指定值的计数器 |
| `Increment() int64` | 递增 1，返回新值 |
| `IncrementBy(d int64) int64` | 递增 delta，返回新值 |
| `Decrement() int64` | 递减 1，返回新值 |
| `DecrementBy(d int64) int64` | 递减 delta，返回新值 |
| `Get() int64` | 获取当前值 |
| `Set(v int64)` | 设置值 |
| `Reset() int64` | 重置为 0，返回旧值 |
| `CompareAndSwap(old, new int64) bool` | 原子比较交换 |

### CounterManager

| 方法 | 说明 |
|------|------|
| `NewCounterManager() *CounterManager` | 创建计数器管理器 |
| `GetOrCreate(name string) *Counter` | 获取或创建计数器 |
| `Get(name string) *Counter` | 获取计数器（不存在返回 nil） |
| `Increment(name string) int64` | 递增命名计数器 |
| `IncrementBy(name string, d int64) int64` | 递增命名计数器指定值 |
| `Decrement(name string) int64` | 递减命名计数器 |
| `DecrementBy(name string, d int64) int64` | 递减命名计数器指定值 |
| `GetValue(name string) int64` | 获取命名计数器值 |
| `SetValue(name string, v int64)` | 设置命名计数器值 |
| `Delete(name string) bool` | 删除计数器 |
| `Reset(name string) int64` | 重置命名计数器 |
| `ResetAll()` | 重置所有计数器 |
| `Names() []string` | 获取所有计数器名称 |
| `Count() int` | 获取计数器数量 |
| `GetAll() map[string]int64` | 获取所有计数器值 |
| `TakeSnapshot() Snapshot` | 拍摄快照 |
| `GetHistory() []Snapshot` | 获取历史快照 |
| `ClearHistory()` | 清空历史快照 |

### StatsCollector

| 方法 | 说明 |
|------|------|
| `NewStatsCollector() *StatsCollector` | 创建统计收集器 |
| `Record(name string, value int64)` | 记录值 |
| `GetStats(name string) *Stats` | 获取统计信息 |
| `GetAllStats() map[string]*Stats` | 获取所有统计信息 |
| `ResetStats(name string)` | 重置指定统计 |
| `ResetAllStats()` | 重置所有统计 |

### RateCounter

| 方法 | 说明 |
|------|------|
| `NewRateCounter(window time.Duration) *RateCounter` | 创建速率计数器 |
| `Record()` | 记录一个事件 |
| `RecordAt(t time.Time)` | 在指定时间记录事件 |
| `Count() int` | 获取窗口内事件数 |
| `Rate() float64` | 获取每秒事件速率 |
| `Reset()` | 重置计数器 |

### BucketCounter

| 方法 | 说明 |
|------|------|
| `NewBucketCounter(bucketSize time.Duration, numBuckets int) *BucketCounter` | 创建桶计数器 |
| `Increment()` | 递增当前桶 |
| `IncrementBy(d int64)` | 递增当前桶指定值 |
| `GetBucket(idx int) int64` | 获取指定桶的值 |
| `GetAllBuckets() []int64` | 获取所有桶的值 |
| `Total() int64` | 获取所有桶的总和 |
| `Reset()` | 重置所有桶 |

## 测试

运行测试：

```bash
go test -v
```

运行基准测试：

```bash
go test -bench=.
```

## 性能特性

- 所有操作都是 O(1) 时间复杂度
- 使用 `sync/atomic` 实现无锁计数器
- 读操作使用读锁，允许并发读取
- 写操作使用写锁，保证数据一致性
- 适用于高并发场景

## 许可证

MIT License