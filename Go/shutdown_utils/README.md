# shutdown_utils

优雅关闭工具包，用于 Go 应用程序的平滑关闭。处理 OS 信号、管理关闭钩子、确保资源清理。

## 功能特性

- 🔔 **信号监听** - 自动监听 SIGINT (Ctrl+C) 和 SIGTERM 信号
- 📋 **优先级钩子** - 按优先级顺序执行关闭钩子（数字越小越先执行）
- ⏱️ **超时控制** - 支持全局和单个钩子的超时设置
- 🔒 **线程安全** - 使用互斥锁保护并发访问
- 📝 **可自定义日志** - 支持自定义日志接口
- 🔄 **幂等关闭** - 多次调用 Shutdown() 只执行一次

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/shutdown_utils
```

## 快速开始

### 基本使用

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    "github.com/ayukyo/alltoolkit/Go/shutdown_utils"
)

func main() {
    // 创建关闭管理器
    mgr := shutdown.New(shutdown.WithTimeout(30*time.Second))
    
    // 注册关闭钩子
    mgr.RegisterFunc("close-db", func(ctx context.Context) error {
        fmt.Println("Closing database...")
        return nil
    }, shutdown.WithPriority(10))
    
    // 监听信号
    shutdownChan := mgr.Listen()
    
    // 等待关闭
    <-shutdownChan
    mgr.WaitForShutdown()
}
```

### 与 HTTP 服务器集成

```go
server := &http.Server{Addr: ":8080"}

mgr := shutdown.New()
mgr.RegisterFunc("http-shutdown", func(ctx context.Context) error {
    return server.Shutdown(ctx)
})

mgr.Listen()
server.ListenAndServe()
mgr.WaitForShutdown()
```

### 手动触发关闭

```go
mgr := shutdown.New()
mgr.RegisterFunc("cleanup", func(ctx context.Context) error {
    // 清理逻辑
    return nil
})

// 手动触发（非信号方式）
mgr.Shutdown()
```

## API 文档

### Manager

```go
// 创建管理器
mgr := shutdown.New(
    shutdown.WithTimeout(15*time.Second),  // 默认超时
    shutdown.WithLogger(customLogger),      // 自定义日志
)

// 注册钩子
err := mgr.Register(&shutdown.Hook{
    Name:     "my-hook",
    Priority: 100,  // 数字越小越先执行
    Func:     func(ctx context.Context) error { return nil },
    Timeout:  5*time.Second,
})

// 便捷注册
mgr.RegisterFunc("name", fn, 
    shutdown.WithPriority(10),
    shutdown.WithHookTimeout(2*time.Second),
)

// 监听信号
shutdownChan := mgr.Listen()

// 获取关闭上下文
ctx := mgr.ListenWithContext()

// 检查状态
isShuttingDown := mgr.IsShuttingDown()

// 手动关闭
mgr.Shutdown()

// 等待完成
mgr.WaitForShutdown()
```

### Hook 优先级

- 数字越小，优先级越高（越先执行）
- 推荐优先级：
  - 0-10: 紧急操作（停止接受新请求）
  - 10-30: 核心服务（数据库、缓存）
  - 30-50: 应用层（HTTP 服务器）
  - 50+: 清理操作（日志刷新、指标上报）

## 测试

```bash
cd Go/shutdown_utils
go test -v
```

## 示例

完整示例见 `example/main.go`，演示了：
- 多优先级钩子注册
- HTTP 服务器优雅关闭
- 数据库连接关闭
- 缓存刷新
- 超时处理

运行示例：

```bash
cd Go/shutdown_utils/example
go run main.go
```

## 许可证

MIT License