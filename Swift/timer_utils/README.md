# Swift Timer Utilities

高性能计时器工具类，提供精确的时间测量、性能分析和倒计时功能。

## 功能特性

- **PrecisionTimer** - 纳秒级精确计时器，使用 `mach_absolute_time` 实现
- **BlockTimer** - 简单的代码块计时器，自动打印耗时
- **PerformanceProfiler** - 性能分析器，统计分析多次执行的耗时
- **CountdownTimer** - 倒计时器，支持暂停、恢复和回调
- **Stopwatch** - 秒表，支持圈数记录和统计分析
- **便捷函数** - `timeit()`, `delay()` 快速使用

## 安装

将 `mod.swift` 文件添加到您的 Swift 项目中即可。

### Swift Package Manager

```swift
dependencies: [
    .package(path: "path/to/timer_utils")
]
```

## 使用示例

### PrecisionTimer - 精确计时

```swift
import Foundation

let timer = PrecisionTimer()
timer.start()

// 执行一些工作
var sum = 0
for i in 0..<100000 {
    sum += i
}

timer.stop()

print("耗时: \(timer.formatted)")  // 如: "1.23ms"
print("纳秒: \(timer.elapsedNanoseconds)")
print("毫秒: \(timer.elapsedMilliseconds)")

// 或者使用 measure 方法
let (result, duration) = timer.measure {
    return complexCalculation()
}
```

### BlockTimer - 代码块计时

```swift
// 自动打印模式
let timer = BlockTimer("数据处理")
processData()
timer.stop()  // 打印: [数据处理] 耗时: 123.45ms

// 简洁写法
let _ = BlockTimer.measure("排序")
array.sort()
```

### PerformanceProfiler - 性能分析

```swift
let profiler = PerformanceProfiler()

// 测量多次操作
for _ in 0..<10 {
    profiler.measure("API请求") {
        fetchData()
    }
}

// 获取统计数据
if let stats = profiler.statistics(for: "API请求") {
    print(stats.formatted)
    // 输出:
    // [API请求] 性能统计 (共10次):
    //   总耗时: 1234.56ms
    //   平均: 123.46ms
    //   最小: 100.00ms
    //   最大: 150.00ms
    //   中位数: 120.00ms
    //   标准差: 15.00ms
    //   P95: 145.00ms
    //   P99: 148.00ms
}

// 导出 CSV
let csv = profiler.exportCSV()
```

### CountdownTimer - 倒计时

```swift
let timer = CountdownTimer()

timer.onTick = { remaining in
    print("剩余: \(remaining)秒")
}

timer.onFinished = {
    print("倒计时结束！")
}

timer.set(seconds: 60)  // 设置60秒
timer.start()           // 开始
timer.pause()           // 暂停
timer.start()           // 继续
timer.stop()            // 停止并重置

// 格式化显示
print(timer.formatted)  // "01:00.00"
```

### Stopwatch - 秒表

```swift
let stopwatch = Stopwatch()

stopwatch.start()

// 记录圈数
Thread.sleep(forTimeInterval: 1.0)
let lap1 = stopwatch.lap()
print("第1圈: \(lap1.lapTime)秒")

Thread.sleep(forTimeInterval: 0.5)
let lap2 = stopwatch.lap()
print("第2圈: \(lap2.lapTime)秒")

stopwatch.stop()

// 统计信息
print("总时间: \(stopwatch.formatted)")
print("最佳圈: \(stopwatch.bestLap?.lapTime ?? 0)秒")
print("最差圈: \(stopwatch.worstLap?.lapTime ?? 0)秒")
print("平均圈速: \(stopwatch.averageLapTime ?? 0)秒")
```

### 便捷函数

```swift
// 快速计时
let result = timeit("计算") {
    return (0..<10000).reduce(0, +)
}

// 带详细结果
let (sum, ms) = timeit("求和") {
    return (0..<1000000).reduce(0, +)
}
print("结果: \(sum), 耗时: \(ms)ms")

// 延迟执行
delay(2.0) {
    print("2秒后执行")
}
```

## API 参考

### PrecisionTimer

| 方法/属性 | 描述 |
|---------|------|
| `start()` | 开始计时 |
| `stop()` | 停止计时 |
| `reset()` | 重置计时器 |
| `measure(_:)` | 测量代码块执行时间 |
| `elapsedNanoseconds` | 纳秒数 |
| `elapsedMicroseconds` | 微秒数 |
| `elapsedMilliseconds` | 毫秒数 |
| `elapsedSeconds` | 秒数 |
| `formatted` | 格式化字符串 |

### PerformanceProfiler.Statistics

| 属性 | 描述 |
|------|------|
| `count` | 执行次数 |
| `totalMs` | 总耗时(毫秒) |
| `averageMs` | 平均耗时 |
| `minMs` | 最小耗时 |
| `maxMs` | 最大耗时 |
| `medianMs` | 中位数 |
| `standardDeviation` | 标准差 |
| `p95Ms` | P95 百分位 |
| `p99Ms` | P99 百分位 |

## 系统要求

- iOS 13.0+ / macOS 10.15+ / watchOS 6.0+ / tvOS 13.0+
- Swift 5.0+

## 许可证

MIT License