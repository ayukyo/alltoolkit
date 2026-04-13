# Go Time Utilities

全面的 Go 时间和日期处理工具库，零外部依赖，仅使用 Go 标准库。

## 功能特性

### 时间解析
- **自动格式检测** - 智能识别多种日期时间格式
- **Unix 时间戳解析** - 支持秒和毫秒时间戳
- **人类可读时长解析** - 支持 "1d2h30m" 格式

### 时间格式化
- 预定义常用格式常量 (ISO8601, RFC3339, 日期时间等)
- 人类可读时长格式化
- Unix 时间戳转换

### 时间计算
- 日期加减 (天/月/年)
- 时间边界 (日/周/月/年的开始和结束)
- 工作日计算

### 时间比较
- 前后比较
- 同日/同月/同年判断
- 今天/昨天/明天判断
- 周末/工作日判断
- 闰年判断
- 月天数计算

### 时间差计算
- 精确差异 (天/小时/分钟/秒)
- 人类可读差异
- 详细差异分解

### 时间范围
- 范围创建和验证
- 包含判断
- 重叠检测
- 区间分割

### 计时工具
- **Stopwatch** - 计时器 (支持开始/暂停/重置)
- **Countdown** - 倒计时器 (支持进度追踪)

### 周计算
- 下一/上一周几
- 第 N 个周几
- 月末周几

### 其他实用工具
- 年龄计算 (精确到年月日)
- 时区转换
- 时间排序
- Min/Max/Clamp

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/time_utils
```

## 快速开始

```go
package main

import (
    "fmt"
    "time"
    
    timeutils "github.com/ayukyo/alltoolkit/Go/time_utils"
)

func main() {
    // 解析时间
    t, _ := timeutils.Parse("2024-01-15 10:30:00")
    fmt.Println(t)
    
    // 格式化
    fmt.Println(timeutils.FormatDateTime(t))
    
    // 计算日期边界
    fmt.Println(timeutils.StartOfDay(t))
    fmt.Println(timeutils.EndOfMonth(t))
    
    // 时间差
    diff := timeutils.DiffDetailed(t, time.Now())
    fmt.Printf("%d 天, %d 小时, %d 分钟\n", 
        diff.Days, diff.Hours, diff.Minutes)
    
    // 计时器
    sw := timeutils.NewStopwatch()
    sw.Start()
    // ... 执行操作
    sw.Stop()
    fmt.Println(sw.ElapsedString())
}
```

## API 文档

### 解析函数

```go
// 自动检测格式解析
Parse(s string, opts ...ParseOptions) (time.Time, error)

// 解析 Unix 时间戳 (秒或毫秒)
ParseUnix(v interface{}) (time.Time, error)

// 解析人类可读时长 ("1d2h30m", "2h 45m 30s")
ParseDuration(s string) (time.Duration, error)
```

### 格式化函数

```go
Format(t time.Time, layout string) string
FormatISO8601(t time.Time) string
FormatDateTime(t time.Time) string
FormatDate(t time.Time) string
FormatTime(t time.Time) string
FormatHumanDuration(d time.Duration) string
```

### 时间计算函数

```go
AddDays(t time.Time, days int) time.Time
AddMonths(t time.Time, months int) time.Time
AddYears(t time.Time, years int) time.Time
StartOfDay(t time.Time) time.Time
EndOfDay(t time.Time) time.Time
StartOfWeek(t time.Time) time.Time
EndOfWeek(t time.Time) time.Time
StartOfMonth(t time.Time) time.Time
EndOfMonth(t time.Time) time.Time
StartOfYear(t time.Time) time.Time
EndOfYear(t time.Time) time.Time
```

### 比较函数

```go
IsBefore(t1, t2 time.Time) bool
IsAfter(t1, t2 time.Time) bool
IsSameDay(t1, t2 time.Time) bool
IsToday(t time.Time) bool
IsWeekend(t time.Time) bool
IsLeapYear(year int) bool
DaysInMonth(year int, month time.Month) int
```

### 时间差函数

```go
Diff(t1, t2 time.Time) time.Duration
DiffInDays(t1, t2 time.Time) int
DiffInHours(t1, t2 time.Time) float64
DiffHuman(t1, t2 time.Time) string
DiffDetailed(t1, t2 time.Time) Duration
```

### 时间范围

```go
tr, _ := NewTimeRange(start, end)
tr.Duration() time.Duration
tr.Contains(t time.Time) bool
tr.Overlaps(other TimeRange) bool
tr.Split(interval time.Duration) []time.Time
```

### 计时器

```go
// Stopwatch (计时器)
sw := NewStopwatch()
sw.Start()
sw.Stop()
sw.Reset()
elapsed := sw.Elapsed()
str := sw.ElapsedString()

// Countdown (倒计时)
cd := NewCountdown(2 * time.Hour)
remaining := cd.Remaining()
expired := cd.IsExpired()
progress := cd.Progress(totalDuration)
```

## 测试

```bash
go test ./...
go test -bench=. ./...
```

## 许可证

MIT License