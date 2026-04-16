# Circuit Breaker Utils (Go)

断路器模式实现，用于分布式系统的容错保护。

## 功能特性

- **三态断路器**: Closed、Open、HalfOpen 状态自动切换
- **可配置阈值**: 自定义失败阈值和成功恢复阈值
- **超时控制**: Open 状态自动超时后尝试恢复
- **并发控制**: 支持最大并发调用限制
- **事件回调**: 状态变化和事件通知回调
- **统计信息**: 详细的调用统计和健康状态
- **零依赖**: 仅使用 Go 标准库
- **线程安全**: 使用 sync.RWMutex 保护共享状态

## 快速开始

### 基本使用

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    "github.com/ayukyo/alltoolkit/Go/circuit_breaker"
)

func main() {
    // 创建断路器
    cb := circuit_breaker.New(circuit_breaker.Config{
        FailureThreshold:   5,               // 连续5次失败后打开
        SuccessThreshold:   3,               // 连续3次成功后关闭
        Timeout:           30 * time.Second, // Open状态持续30秒
    })
    
    ctx := context.Background()
    
    // 执行受保护的函数
    result, err := cb.Execute(ctx, func() (interface{}, error) {
        // 调用外部服务
        return callExternalService()
    })
    
    if err == circuit_breaker.ErrCircuitOpen {
        fmt.Println("断路器已打开，服务不可用")
    } else if err != nil {
        fmt.Printf("调用失败: %v\n", err)
    } else {
        fmt.Printf("调用成功: %v\n", result)
    }
}
```

### 使用 Fallback 降级

```go
result, err := cb.ExecuteWithFallback(ctx,
    func() (interface{}, error) {
        // 主逻辑
        return callPrimaryService()
    },
    func(e error) (interface{}, error) {
        // 降级逻辑
        fmt.Printf("主服务不可用: %v, 使用降级服务\n", e)
        return callFallbackService()
    },
)
```

### 状态监控

```go
// 获取当前状态
state := cb.State()
fmt.Printf("当前状态: %s\n", state) // closed, open, half-open

// 获取统计信息
stats := cb.Stats()
fmt.Printf("总调用: %d\n", stats.TotalCalls)
fmt.Printf("成功: %d\n", stats.Successes)
fmt.Printf("失败: %d\n", stats.Failures)
fmt.Printf("拒绝: %d\n", stats.RejectedCalls)
fmt.Printf("失败率: %.2f%%\n", stats.FailureRate())

// 获取健康状态
health := cb.Health()
fmt.Printf("健康: %v\n", health.Healthy)
fmt.Printf("状态: %s\n", health.State)
```

### 事件回调

```go
cb := circuit_breaker.New(circuit_breaker.Config{
    FailureThreshold: 5,
    Timeout:         30 * time.Second,
    
    // 状态变化回调
    OnStateChange: func(oldState, newState circuit_breaker.State) {
        fmt.Printf("状态变化: %s -> %s\n", oldState, newState)
    },
    
    // 事件回调
    OnEvent: func(event circuit_breaker.Event, stats circuit_breaker.Stats) {
        fmt.Printf("事件: %s, 总调用: %d\n", event, stats.TotalCalls)
    },
})
```

### 自定义失败判断

```go
cb := circuit_breaker.New(circuit_breaker.Config{
    FailureThreshold: 5,
    
    // 只将特定错误计为失败
    IsFailure: func(err error) bool {
        // 忽略取消错误
        if errors.Is(err, context.Canceled) {
            return false
        }
        // 忽略 4xx 错误
        var httpErr HTTPError
        if errors.As(err, &httpErr) && httpErr.Code >= 400 && httpErr.Code < 500 {
            return false
        }
        return true
    },
})
```

### 并发控制

```go
cb := circuit_breaker.New(circuit_breaker.Config{
    FailureThreshold:   5,
    MaxConcurrentCalls: 100, // 最大100个并发调用
})
```

### 调用超时

```go
cb := circuit_breaker.New(circuit_breaker.Config{
    FailureThreshold:   5,
    TimeoutDuration:   5 * time.Second, // 单次调用超时
})
```

### 手动操作

```go
// 检查是否允许调用
if cb.Allow() {
    // 执行调用
    result, err := callService()
    
    // 手动记录结果
    if err != nil {
        cb.RecordFailure(err)
    } else {
        cb.RecordSuccess()
    }
}

// 手动打开断路器
cb.Trip()

// 重置断路器
cb.Reset()

// 检查状态
if cb.IsOpen() {
    fmt.Println("断路器已打开")
}

// 获取重试等待时间
retryAfter := cb.TimeUntilRetry()
```

## 状态流转图

```
           失败达到阈值
    ┌──────────────────────┐
    │                      │
    ▼                      │
┌────────┐            ┌────────┐
│ Closed │            │  Open  │
└────────┘            └────────┘
    │                      │
    │                      │ 超时后
    │                      ▼
    │                 ┌─────────┐
    │ 成功恢复        │HalfOpen │
    │                 └─────────┘
    │                      │
    │         ┌────────────┼────────────┐
    │         │ 成功       │            │ 失败
    │         │ 达到阈值    │            │
    │         ▼            │            ▼
    │    ┌────────┐       │       ┌────────┐
    └───▶│ Closed │       │       │  Open  │
         └────────┘       │       └────────┘
                          │
```

## 配置说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FailureThreshold` | int | 5 | 连续失败多少次后打开断路器 |
| `SuccessThreshold` | int | 3 | HalfOpen状态下连续成功多少次后关闭断路器 |
| `Timeout` | time.Duration | 30s | Open状态持续时间后尝试恢复 |
| `MaxConcurrentCalls` | int | 0 | 最大并发调用数，0表示不限制 |
| `TimeoutDuration` | time.Duration | 0 | 单次调用超时时间，0表示不限制 |
| `OnStateChange` | func | nil | 状态变化回调函数 |
| `OnEvent` | func | nil | 事件回调函数 |
| `IsFailure` | func | nil | 自定义失败判断函数 |

## API 参考

### 主要方法

```go
// 执行受保护的函数
Execute(ctx context.Context, fn func() (interface{}, error)) (interface{}, error)

// 执行带降级的函数
ExecuteWithFallback(ctx context.Context, fn func() (interface{}, error), fallback func(error) (interface{}, error)) (interface{}, error)

// 批量执行
ExecuteBatch(ctx context.Context, fns []func() (interface{}, error)) BatchResult

// 运行无返回值函数
Run(ctx context.Context, r Runnable) error

// 调用有返回值函数
Call(ctx context.Context, c Callable) (interface{}, error)
```

### 状态检查

```go
State() State           // 获取当前状态
Stats() Stats           // 获取统计信息
Health() HealthStatus   // 获取健康状态
IsOpen() bool           // 是否打开
IsClosed() bool         // 是否关闭
IsHalfOpen() bool       // 是否半开
Allow() bool            // 是否允许调用
Ready() bool            // 是否就绪
TimeUntilRetry() time.Duration  // 重试等待时间
```

### 手动操作

```go
Trip()                  // 手动打开断路器
Reset()                 // 重置断路器
RecordSuccess()         // 记录成功
RecordFailure(err)      // 记录失败
```

## 使用场景

1. **微服务调用**: 保护对外部服务的调用，防止级联故障
2. **数据库访问**: 保护数据库连接，防止连接池耗尽
3. **API 网关**: 对下游服务进行熔断保护
4. **第三方集成**: 保护对不可靠第三方服务的调用
5. **资源保护**: 防止资源过载

## 测试

```bash
cd Go/circuit_breaker
go test -v
```

## 基准测试

```bash
go test -bench=. -benchmem
```

## 许可证

MIT License