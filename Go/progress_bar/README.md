# progress_bar

Go 终端进度条工具库 - 零外部依赖，功能完整，并发安全。

## 特性

- **多种进度条样式** - 8种内置样式（Default、Classic、Arrow、Blocks、Dots、Pipe、Minimal、Circle）
- **ANSI 颜色支持** - 完成部分和未完成部分可独立设置颜色
- **实时信息显示** - 百分比、计数、ETA、速度、已用时间
- **并发安全** - 所有操作都使用互斥锁保护
- **动态更新** - 支持运行时更新描述和配置
- **Spinner 动画** - 内置旋转动画支持
- **多进度条** - 同时管理多个进度条
- **静态进度条** - 无动画模式，适合日志输出
- **迭代器支持** - 泛型迭代器，自动显示进度
- **工具函数** - 字节格式化、数字格式化、时间估算等

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/progress_bar
```

## 快速开始

### 基本使用

```go
package main

import (
    "time"
    progress "github.com/ayukyo/alltoolkit/Go/progress_bar"
)

func main() {
    // 创建进度条
    pb := progress.New(100)
    
    for i := 0; i < 100; i++ {
        pb.Increment()
        time.Sleep(20 * time.Millisecond)
    }
    
    pb.Finish()
}
```

### 自定义配置

```go
pb := progress.NewWithConfig(progress.Config{
    Total:           1000,
    Width:           50,
    Style:           progress.StyleArrow,
    Description:     "Downloading",
    ShowPercentage:  true,
    ShowCount:       true,
    ShowETA:         true,
    ShowSpeed:       true,
    ShowElapsedTime: false,
    ColorComplete:   progress.ColorGreen,
    ColorIncomplete: progress.ColorWhite,
})

for i := 0; i < 1000; i++ {
    pb.Increment()
    time.Sleep(2 * time.Millisecond)
}
pb.Finish()
```

## 进度条样式

```go
// 可用样式
progress.StyleDefault  // ████░░░░ |█    |
progress.StyleClassic  // ====  [======   ]
progress.StyleArrow    // ====> [=====>   ]
progress.StyleBlocks   // ▓▓▓▓░░░░
progress.StyleDots     // ●●●●○○○○
progress.StylePipe      // ├████░░░░┤
progress.StyleMinimal   // ####----
progress.StyleCircle    // ◉◉◉◉◎◎◎◎
```

## API

### ProgressBar

```go
// 创建
pb := progress.New(total int64) *ProgressBar
pb := progress.NewWithConfig(config Config) *ProgressBar

// 更新进度
pb.Add(n int64)           // 增加进度
pb.Set(current int64)     // 设置当前进度
pb.Increment()            // 增加 1

// 获取信息
pb.Current() int64        // 获取当前进度
pb.Percentage() float64   // 获取百分比 (0-100)
pb.ETA() time.Duration    // 获取预计剩余时间
pb.Elapsed() time.Duration // 获取已用时间
pb.Speed() float64        // 获取速度 (items/s)

// 控制
pb.Finish()               // 完成进度条
pb.Reset()                // 重置进度条
pb.Clear()                // 清除进度条行
pb.Describe(desc string)  // 更新描述
pb.UpdateConfig(config Config) // 更新配置
```

### 静态进度条

```go
// 无动画，适合日志输出
bar := progress.Static(current, total int64, width int, style Style) string
bar := progress.StaticPercentage(current, total int64, width int, style Style) string
bar := progress.StaticFull(current, total int64, width int, style Style, desc string) string
```

### Spinner

```go
// 旋转动画
spinner := progress.NewSpinner("Loading").
    SetSuffix("Processing...").
    SetInterval(80 * time.Millisecond)

spinner.Start()
time.Sleep(2 * time.Second)
spinner.Stop()

// 自定义帧
spinner.SetFrames([]string{"|", "/", "-", "\\"})
```

### 多进度条

```go
mb := progress.NewMultiBar()
bar1 := mb.AddBar(100, "Task 1:")
bar2 := mb.AddBar(200, "Task 2:")
bar3 := mb.AddBar(50, "Task 3:")

for i := 0; i < 200; i++ {
    bar1.Increment()
    bar2.Increment()
    bar3.Increment()
    mb.Render()
    time.Sleep(20 * time.Millisecond)
}
```

### 迭代器

```go
// 自动显示进度的迭代
items := []string{"a", "b", "c", "d", "e"}
err := progress.Iterate(items, "Processing", func(i int, item string) error {
    // 处理 item
    return nil
})

// 带配置的迭代
err := progress.IterateWithConfig(items, config, func(i int, item string) error {
    return nil
})
```

### 工具函数

```go
// 字节格式化
progress.FormatBytes(1024)      // "1.00 KB"
progress.FormatBytes(1048576)   // "1.00 MB"
progress.FormatBytes(1073741824) // "1.00 GB"

// 数字格式化
progress.FormatNumber(1000)      // "1,000"
progress.FormatNumber(1000000)   // "1,000,000"

// 进度计算
progress.CalculateProgress(50, 100) // 50.0

// 时间估算
progress.EstimateTime(elapsed, current, total)
```

### 颜色

```go
// ANSI 颜色常量
progress.ColorReset   // \033[0m
progress.ColorRed     // \033[31m
progress.ColorGreen   // \033[32m
progress.ColorYellow  // \033[33m
progress.ColorBlue    // \033[34m
progress.ColorPurple  // \033[35m
progress.ColorCyan    // \033[36m
progress.ColorWhite   // \033[37m
progress.ColorBold    // \033[1m
```

## 配置选项

| 字段 | 类型 | 说明 |
|------|------|------|
| Total | int64 | 总任务数 |
| Width | int | 进度条宽度（字符数） |
| Style | Style | 进度条样式 |
| Description | string | 描述文本 |
| ShowPercentage | bool | 显示百分比 |
| ShowCount | bool | 显示计数 (当前/总数) |
| ShowETA | bool | 显示预计剩余时间 |
| ShowSpeed | bool | 显示速度 (items/s) |
| ShowElapsedTime | bool | 显示已用时间 |
| ShowSpinner | bool | 显示旋转动画 |
| ColorComplete | Color | 完成部分颜色 |
| ColorIncomplete | Color | 未完成部分颜色 |
| Writer | io.Writer | 输出目标（默认 os.Stderr） |

## 并发安全

所有进度条操作都是并发安全的，可以在多个 goroutine 中安全使用：

```go
pb := progress.New(10000)

var wg sync.WaitGroup
for i := 0; i < 100; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        for j := 0; j < 100; j++ {
            pb.Increment()
            time.Sleep(time.Millisecond)
        }
    }()
}
wg.Wait()
pb.Finish()
```

## 示例输出

```
Processing: [==================>                         ] 45.00% 450/1000 [1000/s] ETA: 00:01
Downloading: ███████████████████░░░░░░░░░░░░░░░░░░░  50% 50/100 [200/s] ETA: 00:00
⠋ Compiling: 75% (75/100)
```

## 许可证

MIT License