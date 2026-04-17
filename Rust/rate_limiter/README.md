# Rate Limiter Utilities

A comprehensive rate limiting library for Rust with zero external dependencies.

## Features

- **Token Bucket**: Allows bursts up to bucket capacity, with tokens refilling at a constant rate
- **Leaky Bucket**: Processes requests at a constant rate, smoothing out bursts
- **Fixed Window**: Simple and memory-efficient, divides time into fixed windows
- **Sliding Window**: Precise rate control without boundary issues
- **Sliding Log**: Exact tracking of request timestamps for precise rate limiting
- **Adaptive Limiter**: Automatically adjusts rate limit based on success/failure patterns
- **Concurrency Limiter**: Limits concurrent operations (not rate per second)

## Usage

Add to your `Cargo.toml`:

```toml
[dependencies]
rate_limiter = { path = "rate_limiter" }
```

### Token Bucket

```rust
use rate_limiter::{TokenBucket, RateLimiter};

let mut bucket = TokenBucket::new(100, 10.0); // 100 capacity, 10 tokens/sec

// Can burst up to 100 requests
assert!(bucket.try_acquire(100).is_ok());

// Will be rejected after capacity exhausted
assert!(bucket.try_acquire(1).is_err());

// Tokens refill over time
std::thread::sleep(std::time::Duration::from_secs(1));
assert!(bucket.try_acquire(10).is_ok()); // ~10 tokens refilled
```

### Leaky Bucket

```rust
use rate_limiter::{LeakyBucket, RateLimiter};

let mut bucket = LeakyBucket::new(100, 10.0); // 100 capacity, 10 req/sec

// Requests are processed at a steady rate
assert!(bucket.try_acquire(10).is_ok());
```

### Fixed Window

```rust
use rate_limiter::{FixedWindow, RateLimiter};
use std::time::Duration;

let mut limiter = FixedWindow::new(100, Duration::from_secs(60));

// Allow up to 100 requests per 60-second window
assert!(limiter.try_acquire(1).is_ok());
```

### Sliding Window

```rust
use rate_limiter::{SlidingWindow, RateLimiter};
use std::time::Duration;

let mut limiter = SlidingWindow::new(100, Duration::from_secs(60));

// Precise rate control without boundary issues
assert!(limiter.try_acquire(1).is_ok());
```

### Sliding Log (Exact)

```rust
use rate_limiter::{SlidingLog, RateLimiter};
use std::time::Duration;

let mut limiter = SlidingLog::new(100, Duration::from_secs(60));

// Exact tracking of request timestamps
assert!(limiter.try_acquire(1).is_ok());
```

### Adaptive Limiter

```rust
use rate_limiter::AdaptiveLimiter;

let mut limiter = AdaptiveLimiter::new(100, 0.5);

// On success, limit gradually increases
limiter.on_success();

// On failure, limit decreases
limiter.on_failure();

// Use with RateLimiter trait
assert!(limiter.try_acquire(50).is_ok());
```

### Concurrency Limiter

```rust
use rate_limiter::ConcurrencyLimiter;
use std::sync::Arc;
use std::thread;

let limiter = Arc::new(ConcurrencyLimiter::new(10));

let permit = limiter.try_acquire();
assert!(permit.is_ok());

// Permit is released when dropped
drop(permit);
```

## Algorithm Comparison

| Algorithm | Memory | Precision | Burst Support | Use Case |
|-----------|--------|-----------|---------------|----------|
| Token Bucket | O(1) | Medium | High | API rate limiting |
| Leaky Bucket | O(1) | Medium | Low | Traffic shaping |
| Fixed Window | O(1) | Low | Medium | Simple rate limits |
| Sliding Window | O(n) | High | Medium | Precise rate control |
| Sliding Log | O(n) | Highest | Low | Critical rate control |
| Adaptive | O(1) | Variable | Variable | Backpressure handling |
| Concurrency | O(1) | Exact | N/A | Resource limiting |

## Running Tests

```bash
cd rate_limiter
cargo test
```

## License

MIT License