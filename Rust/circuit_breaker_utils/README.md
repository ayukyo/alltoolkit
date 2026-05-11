# Circuit Breaker Utils (熔断器工具库)

[English](#english) | [中文](#中文)

---

## 中文

一个纯 Rust 实现的熔断器（Circuit Breaker）工具库，用于防止级联故障、实现快速失败和自动恢复。零外部依赖。

### 特性

- ✅ **完整熔断器模式实现**: Closed → Open → HalfOpen 状态转换
- ✅ **可配置参数**: 失败阈值、成功阈值、超时时间等
- ✅ **自动恢复**: 半开状态探测机制
- ✅ **手动控制**: 支持手动打开/关闭熔断器
- ✅ **统计监控**: 完整的请求统计和状态跟踪
- ✅ **线程安全**: 使用 Arc<Mutex> 保证并发安全
- ✅ **构建器模式**: 流畅的配置 API
- ✅ **零外部依赖**: 仅使用 Rust 标准库

### 熔断器状态

```
┌─────────┐  连续失败达到阈值  ┌─────────┐
│ Closed  │ ──────────────────> │  Open   │
│ (关闭)  │                     │ (打开)  │
└─────────┘                     └─────────┘
     ▲                                │
     │                                │ 超时后
     │ 连续成功达到阈值                │
     │                                ▼
     │                          ┌──────────┐
     └──────────────────────────│ HalfOpen │
               成功恢复         │ (半开)   │
                                └──────────┘
                                      │
                                      │ 失败
                                      ▼
                                ┌─────────┐
                                │  Open   │
                                │ (打开)  │
                                └─────────┘
```

- **Closed（关闭）**: 正常状态，请求正常执行
- **Open（打开）**: 熔断状态，请求直接失败，不执行实际操作
- **HalfOpen（半开）**: 恢复探测状态，允许部分请求通过以测试服务是否恢复

### 快速开始

```rust
use circuit_breaker_utils::{CircuitBreaker, CircuitState};

// 创建熔断器：连续5次失败触发熔断，连续3次成功恢复，熔断持续30秒
let breaker = CircuitBreaker::new(5, 3, 30);

// 执行受保护的函数
match breaker.call(|| {
    // 模拟可能失败的操作
    Ok::<_, String>("success")
}) {
    Ok(result) => println!("成功: {}", result),
    Err(e) => println!("失败: {}", e),
}
```

### 使用构建器配置

```rust
use circuit_breaker_utils::{CircuitBreakerBuilder, CircuitBreaker};

let breaker = CircuitBreakerBuilder::new()
    .failure_threshold(10)        // 连续10次失败触发熔断
    .success_threshold(5)         // 连续5次成功关闭熔断
    .timeout_secs(60)            // 熔断持续60秒
    .half_open_max_calls(3)      // 半开状态允许3个探测请求
    .fail_fast_on_half_open(true) // 半开状态失败立即重新打开
    .build();
```

### API 参考

#### `CircuitBreaker::new(failure_threshold, success_threshold, timeout_secs)`

创建新的熔断器。

- `failure_threshold`: 连续失败多少次后触发熔断
- `success_threshold`: 半开状态下连续成功多少次后关闭熔断器
- `timeout_secs`: 熔断持续时间（秒）

#### `call(f) -> Result<T, CircuitError<E>>`

执行受保护的函数。

- 成功时返回 `Ok(T)`
- 熔断器打开时返回 `Err(CircuitError::CircuitOpen)`
- 操作失败时返回 `Err(CircuitError::OperationError(E))`

#### `try_call(f) -> Option<Result<T, E>>`

尝试执行，如果熔断器打开则返回 `None`。

#### `state() -> CircuitState`

获取当前状态（Closed/Open/HalfOpen）。

#### `is_call_allowed() -> bool`

检查是否允许请求。

#### `trip()` / `reset()`

手动打开/关闭熔断器。

#### `stats() -> CircuitStats`

获取统计信息，包括：
- 总请求数
- 成功/失败请求数
- 连续失败/成功数
- 状态转换次数

#### `failure_rate() / success_rate() -> f64`

获取失败率/成功率（百分比）。

### 实际应用场景

#### 1. API 调用保护

```rust
let api_breaker = CircuitBreaker::new(3, 2, 30);

match api_breaker.call(|| {
    // 调用外部 API
    fetch_from_external_api()
}) {
    Ok(data) => process_data(data),
    Err(CircuitError::CircuitOpen) => {
        // 使用缓存或默认值
        get_cached_data()
    }
    Err(CircuitError::OperationError(e)) => {
        log_error(e);
        fallback_response()
    }
}
```

#### 2. 数据库连接保护

```rust
let db_breaker = CircuitBreakerBuilder::new()
    .failure_threshold(5)
    .success_threshold(3)
    .timeout_secs(20)
    .build();

fn query_user(id: u64) -> Option<User> {
    db_breaker.call(|| {
        database.query("SELECT * FROM users WHERE id = ?", &[id])
    }).ok()
}
```

#### 3. 微服务熔断

```rust
// 为不同服务创建独立熔断器
let payment_service = CircuitBreaker::new(3, 2, 15);
let inventory_service = CircuitBreaker::new(5, 3, 30);
let notification_service = CircuitBreaker::new(10, 5, 60);

async fn process_order(order: Order) -> Result<(), Error> {
    // 支付服务熔断保护
    payment_service.call(|| payment_service.charge(&order))?;
    
    // 库存服务熔断保护
    inventory_service.call(|| inventory.check_stock(&order.items))?;
    
    // 通知服务熔断保护（失败不影响主流程）
    let _ = notification_service.call(|| notification.send(&order));
    
    Ok(())
}
```

### 文件结构

```
circuit_breaker_utils/
├── mod.rs                      # 主模块实现
├── circuit_breaker_utils_test.rs # 测试文件
├── README.md                   # 本文档
└── examples/
    └── usage_examples.rs       # 使用示例
```

### 测试

```bash
# 运行测试
cargo test --package circuit_breaker_utils

# 运行示例
cargo run --example usage_examples
```

---

## English

A pure Rust implementation of the Circuit Breaker pattern for preventing cascading failures, enabling fast failure, and automatic recovery. Zero external dependencies.

### Features

- ✅ **Complete Circuit Breaker Pattern**: Closed → Open → HalfOpen state transitions
- ✅ **Configurable Parameters**: Failure threshold, success threshold, timeout, etc.
- ✅ **Automatic Recovery**: Half-open state probing mechanism
- ✅ **Manual Control**: Support for manual trip/reset
- ✅ **Statistics & Monitoring**: Complete request statistics and state tracking
- ✅ **Thread-Safe**: Uses Arc<Mutex> for concurrent safety
- ✅ **Builder Pattern**: Fluent configuration API
- ✅ **Zero External Dependencies**: Only uses Rust standard library

### Circuit Breaker States

```
┌─────────┐  Failures reach threshold  ┌─────────┐
│ Closed  │ ─────────────────────────────> │  Open   │
│         │                                │         │
└─────────┘                                └─────────┘
     ▲                                          │
     │                                          │ After timeout
     │ Successes reach threshold                │
     │                                          ▼
     │                                   ┌──────────┐
     └───────────────────────────────────│ HalfOpen │
                                         │          │
                                         └──────────┘
                                               │
                                               │ Failure
                                               ▼
                                         ┌─────────┐
                                         │  Open   │
                                         │         │
                                         └─────────┘
```

- **Closed**: Normal state, requests execute normally
- **Open**: Circuit broken, requests fail immediately without executing
- **HalfOpen**: Recovery probing state, allows limited requests to test if service recovered

### Quick Start

```rust
use circuit_breaker_utils::{CircuitBreaker, CircuitState};

// Create: 5 consecutive failures trigger, 3 consecutive successes recover, 30s timeout
let breaker = CircuitBreaker::new(5, 3, 30);

// Execute protected function
match breaker.call(|| {
    // Simulated operation that may fail
    Ok::<_, String>("success")
}) {
    Ok(result) => println!("Success: {}", result),
    Err(e) => println!("Failed: {}", e),
}
```

### Using Builder Pattern

```rust
use circuit_breaker_utils::{CircuitBreakerBuilder, CircuitBreaker};

let breaker = CircuitBreakerBuilder::new()
    .failure_threshold(10)        // Trip after 10 consecutive failures
    .success_threshold(5)         // Close after 5 consecutive successes
    .timeout_secs(60)             // Stay open for 60 seconds
    .half_open_max_calls(3)       // Allow 3 probe calls in half-open
    .fail_fast_on_half_open(true) // Reopen immediately on half-open failure
    .build();
```

### API Reference

#### `CircuitBreaker::new(failure_threshold, success_threshold, timeout_secs)`

Create a new circuit breaker.

#### `call(f) -> Result<T, CircuitError<E>>`

Execute a protected function.

- `Ok(T)` on success
- `Err(CircuitError::CircuitOpen)` when circuit is open
- `Err(CircuitError::OperationError(E))` when operation fails

#### `try_call(f) -> Option<Result<T, E>>`

Try to execute, returns `None` if circuit is open.

#### `state() -> CircuitState`

Get current state (Closed/Open/HalfOpen).

#### `is_call_allowed() -> bool`

Check if requests are allowed.

#### `trip()` / `reset()`

Manually open/close the circuit breaker.

#### `stats() -> CircuitStats`

Get statistics including total/successful/failed requests, consecutive counts, state transitions.

#### `failure_rate() / success_rate() -> f64`

Get failure/success rate as percentage.

### Real-World Use Cases

#### 1. API Call Protection

```rust
let api_breaker = CircuitBreaker::new(3, 2, 30);

match api_breaker.call(|| fetch_from_external_api()) {
    Ok(data) => process_data(data),
    Err(CircuitError::CircuitOpen) => get_cached_data(),
    Err(CircuitError::OperationError(e)) => fallback_response(),
}
```

#### 2. Database Connection Protection

```rust
let db_breaker = CircuitBreakerBuilder::new()
    .failure_threshold(5)
    .success_threshold(3)
    .timeout_secs(20)
    .build();

fn query_user(id: u64) -> Option<User> {
    db_breaker.call(|| database.query("SELECT * FROM users WHERE id = ?", &[id])).ok()
}
```

#### 3. Microservice Circuit Breaking

```rust
let payment_service = CircuitBreaker::new(3, 2, 15);
let inventory_service = CircuitBreaker::new(5, 3, 30);
let notification_service = CircuitBreaker::new(10, 5, 60);

async fn process_order(order: Order) -> Result<(), Error> {
    payment_service.call(|| payment_service.charge(&order))?;
    inventory_service.call(|| inventory.check_stock(&order.items))?;
    let _ = notification_service.call(|| notification.send(&order));
    Ok(())
}
```

### File Structure

```
circuit_breaker_utils/
├── mod.rs                      # Main module implementation
├── circuit_breaker_utils_test.rs # Test file
├── README.md                   # This document
└── examples/
    └── usage_examples.rs       # Usage examples
```

### Testing

```bash
# Run tests
cargo test --package circuit_breaker_utils

# Run examples
cargo run --example usage_examples
```

## License

MIT License - Free to use, modify, and distribute.

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.