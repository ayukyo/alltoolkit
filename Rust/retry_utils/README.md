# retry_utils

A comprehensive Rust library for implementing retry mechanisms with exponential backoff, jitter, circuit breaker pattern, and rate limiting. Zero external dependencies.

## Features

- **Exponential Backoff**: Configurable multiplier-based backoff strategy
- **Jitter Support**: Percentage-based, fixed, and decorrelated jitter
- **Circuit Breaker**: Complete circuit breaker pattern implementation
- **Rate Limiting**: Token bucket and sliding window rate limiters
- **Error Classification**: Permanent, transient, and retriable error types
- **Builder Pattern**: Fluent configuration API
- **Callbacks**: Hooks for retry, success, and failure events
- **Thread Safe**: All components safe for concurrent use
- **Zero Dependencies**: Uses only `std`

## Usage

Add to your `Cargo.toml`:

```toml
[dependencies]
retry_utils = { path = "../retry_utils" }
```

Or copy the `mod.rs` file into your project.

## Quick Start

### Basic Retry

```rust
use retry_utils::{retry, RetryConfig};

let result = retry(|| {
    // Your operation here
    Ok::<_, String>(42)
}, RetryConfig::default());

if result.success {
    println!("Got value: {:?}", result.value);
} else {
    println!("Failed: {:?}", result.last_error);
}
```

### Exponential Backoff

```rust
use retry_utils::{retry, RetryConfig};
use std::time::Duration;

let result = retry(|| some_operation(),
    RetryConfig::new(5)
        .with_initial_delay(Duration::from_millis(100))
        .with_max_delay(Duration::from_secs(30))
        .with_multiplier(2.0)
        .with_jitter(0.1),
);
```

### Builder Pattern

```rust
use retry_utils::RetryBuilder;
use std::time::Duration;

let result = RetryBuilder::new()
    .max_attempts(5)
    .initial_delay(Duration::from_millis(100))
    .max_delay(Duration::from_secs(10))
    .multiplier(2.0)
    .jitter(0.1)
    .timeout(Duration::from_secs(30))
    .execute(|| some_operation());
```

### With Callbacks

```rust
let result = RetryBuilder::new()
    .max_attempts(5)
    .on_retry(|attempt, err| {
        println!("Retry {} failed: {}", attempt, err);
    })
    .on_success(|attempts, duration| {
        println!("Success after {} attempts in {:?}", attempts, duration);
    })
    .on_failure(|attempts, duration, err| {
        println!("Failed after {} attempts: {}", attempts, err);
    })
    .execute(|| some_operation());
```

## Error Handling

### Permanent vs Transient Errors

```rust
use retry_utils::{PermanentError, TransientError};

// Permanent errors are not retried
fn auth_operation() -> Result<Data, PermanentError<AuthError>> {
    Err(PermanentError::new(AuthError::InvalidCredentials))
}

// Transient errors can be retried
fn network_operation() -> Result<Data, TransientError<NetworkError>> {
    Err(TransientError::new(NetworkError::Timeout))
}
```

### Retry-After Support

```rust
use retry_utils::RetriableError;
use std::time::Duration;

fn api_call() -> Result<Data, RetriableError<ApiError>> {
    Err(RetriableError::new(ApiError::RateLimited, Duration::from_secs(5)))
}
```

### Custom Retry Filter

```rust
let result = RetryBuilder::new()
    .max_attempts(10)
    .retry_on(|err| {
        err.contains("timeout") || err.contains("connection refused")
    })
    .execute(|| some_operation());
```

## Circuit Breaker

```rust
use retry_utils::{CircuitBreaker, CircuitBreakerConfig, CircuitState};
use std::time::Duration;

let cb = CircuitBreaker::new(CircuitBreakerConfig {
    max_failures: 5,
    reset_timeout: Duration::from_secs(30),
    half_open_max: 3, // Require 3 successes to close
});

// Execute through circuit breaker
let result = cb.execute(|| {
    some_network_call()
});

match result {
    Ok(value) => println!("Success: {:?}", value),
    Err(e) => println!("Failed: {:?}", e),
}

// Check state
println!("Circuit state: {}", cb.state());

// Reset manually
cb.reset();
```

### Circuit Breaker States

| State | Behavior |
|-------|----------|
| `Closed` | Normal operation, requests pass through |
| `Open` | Circuit is open, all requests fail immediately |
| `HalfOpen` | Testing recovery, limited requests allowed |

## Rate Limiting

### Token Bucket

```rust
use retry_utils::RateLimiter;

// 10 retries per second, burst of 5
let rl = RateLimiter::new(10.0, 5);

if rl.allow() {
    // Perform retry
} else {
    rl.wait(); // Block until allowed
}
```

### Sliding Window

```rust
use retry_utils::SlidingWindowCounter;
use std::time::Duration;

// Max 10 requests per minute
let counter = SlidingWindowCounter::new(Duration::from_secs(60), 10);

if counter.allow() {
    // Perform action
}
```

## Convenience Functions

### Exponential Backoff

```rust
use retry_utils::exponential_backoff;
use std::time::Duration;

let result = exponential_backoff(|| some_operation(), 5, Duration::from_millis(100));
```

### Fixed Delay

```rust
use retry_utils::fixed_delay;
use std::time::Duration;

let result = fixed_delay(|| some_operation(), 5, Duration::from_millis(500));
```

### Linear Backoff

```rust
use retry_utils::linear_backoff;
use std::time::Duration;

let result = linear_backoff(|| some_operation(), 5, Duration::from_millis(100));
```

### Until Success

```rust
use retry_utils::until_success;
use std::time::Duration;

// Retry until success or timeout
let result = until_success(|| some_operation(), 
    Duration::from_millis(100), // delay
    Duration::from_secs(5),     // max duration
);
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `max_attempts` | Maximum retry attempts | 3 |
| `initial_delay` | Initial delay between retries | 100ms |
| `max_delay` | Maximum delay cap | 30s |
| `multiplier` | Backoff multiplier | 2.0 |
| `jitter` | Jitter percentage (0-1) | 0.1 |
| `fixed_jitter` | Use fixed jitter mode | false |
| `timeout` | Total operation timeout | None |

## Result Structure

```rust
pub struct RetryResult<T> {
    pub value: Option<T>,        // Final value if successful
    pub last_error: Option<String>, // Last error encountered
    pub attempts: u32,           // Total attempts made
    pub total_duration: Duration, // Total time spent
    pub success: bool,           // Whether operation succeeded
}
```

## Decorrelated Jitter

Alternative jitter strategy that prevents synchronized retries:

```rust
use retry_utils::decorrelated_jitter;
use std::time::Duration;

let delay = decorrelated_jitter(
    Duration::from_millis(100), // base
    Duration::from_secs(1),     // cap
    3,                          // attempt number
);
```

## Examples

### HTTP Client with Retry

```rust
fn fetch_with_retry(url: &str) -> Option<String> {
    retry(|| {
        // Simulate HTTP request
        if url.contains("error") {
            Err(format!("Failed to fetch {}", url))
        } else {
            Ok(format!("Response from {}", url))
        }
    }, RetryConfig::new(3)
        .with_initial_delay(Duration::from_millis(500))
        .with_retry_on(|err| !err.contains("404")),
    )
    .into_result()
    .ok()
}
```

### Database with Circuit Breaker

```rust
lazy_static! {
    static ref DB_CIRCUIT: CircuitBreaker = CircuitBreaker::with_defaults(5, Duration::from_secs(30));
}

fn query_with_protection(sql: &str) -> Result<Rows, String> {
    DB_CIRCUIT.execute(|| {
        // Database query
        database_query(sql)
    })
    .map_err(|e| e.to_string())
}
```

## Testing

```bash
# Run tests
cargo test

# Run with output
cargo test -- --nocapture
```

## License

MIT License