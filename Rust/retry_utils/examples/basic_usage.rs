//! retry_utils Examples
//!
//! Demonstrates various retry patterns and components

use std::time::Duration;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;

// Note: In a real project, you would import from the module:
// use retry_utils::{retry, RetryConfig, RetryBuilder, CircuitBreaker, ...};

// For this example, we'll simulate the module inline
mod retry_utils {
    include!("../mod.rs");
}

use retry_utils::*;

fn main() {
    println!("=== retry_utils Examples ===\n");

    basic_retry_example();
    exponential_backoff_example();
    builder_pattern_example();
    error_classification_example();
    circuit_breaker_example();
    rate_limiter_example();
    sliding_window_example();
    convenience_functions_example();
    retry_filter_example();
    callback_example();
    decorrelated_jitter_example();
}

fn basic_retry_example() {
    println("--- Basic Retry ---");

    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    let result = retry(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        println!("  Attempt {}", count);
        if count < 3 {
            Err("temporary error")
        } else {
            Ok(42)
        }
    }, RetryConfig::default());

    println!("  Success: {}, Attempts: {}, Value: {:?}", 
        result.success, result.attempts, result.value);
    println!();
}

fn exponential_backoff_example() {
    println("--- Exponential Backoff ---");

    let start = std::time::Instant::now();
    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    let result = retry(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let elapsed = start.elapsed();
        println!("  Attempt {} at {:?}", count, elapsed);
        if count < 4 {
            Err("temporary error")
        } else {
            Ok("success")
        }
    }, RetryConfig::new(5)
        .with_initial_delay(Duration::from_millis(50))
        .with_max_delay(Duration::from_secs(1))
        .with_multiplier(2.0)
        .with_jitter(0.1));

    println!("  Total duration: {:?}", result.total_duration);
    println!();
}

fn builder_pattern_example() {
    println("--- Builder Pattern ---");

    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    let result = RetryBuilder::new()
        .max_attempts(3)
        .initial_delay(Duration::from_millis(50))
        .max_delay(Duration::from_millis(500))
        .multiplier(1.5)
        .jitter(0.2)
        .execute(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            println!("  Builder attempt {}", count);
            if count < 2 {
                Err("error")
            } else {
                Ok(100)
            }
        });

    println!("  Result: success={}, value={:?}", result.success, result.value);
    println!();
}

fn error_classification_example() {
    println("--- Error Classification ---");

    // Permanent error
    let perm_err = PermanentError::new("authentication failed");
    println!("  Permanent error: {}", perm_err);

    // Transient error
    let trans_err = TransientError::new("network timeout");
    println!("  Transient error: {}", trans_err);

    // Retriable error with delay suggestion
    let retry_err = RetriableError::new("rate limited", Duration::from_secs(5));
    println!("  Retriable error: {}", retry_err);
    println!("  Retry after: {:?}", retry_err.retry_after());
    println!();
}

fn circuit_breaker_example() {
    println!("--- Circuit Breaker ---");

    let cb = CircuitBreaker::new(CircuitBreakerConfig {
        max_failures: 3,
        reset_timeout: Duration::from_millis(200),
        half_open_max: 1,
    });

    println!("  Initial state: {}", cb.state());

    // Cause failures
    for i in 0..3 {
        let _: Result<i32, _> = cb.execute(|| {
            println!("  Failing request {}", i + 1);
            Err::<i32, &str>("service error")
        });
        println!("  State after failure {}: {}", i + 1, cb.state());
    }

    // Circuit should be open
    let result: Result<i32, CircuitBreakerError<&str>> = cb.execute(|| Ok(42));
    println!("  Request while open: {:?}", result);

    // Wait for half-open
    println!("  Waiting for half-open transition...");
    std::thread::sleep(Duration::from_millis(250));
    println!("  State after wait: {}", cb.state());

    // Successful request
    let result: Result<i32, _> = cb.execute(|| Ok(42));
    println!("  Success in half-open: {:?}", result);
    println!("  Final state: {}", cb.state());

    // Reset
    cb.reset();
    println!("  After reset: {}", cb.state());
    println!();
}

fn rate_limiter_example() {
    println!("--- Rate Limiter (Token Bucket) ---");

    // 10 requests per second, burst of 3
    let rl = RateLimiter::new(10.0, 3);

    println!("  Testing burst capacity:");
    for i in 0..5 {
        let allowed = rl.allow();
        println!("  Request {}: allowed={}", i + 1, allowed);
    }

    println!("\n  Waiting for token replenish...");
    std::thread::sleep(Duration::from_millis(200));

    println!("  After wait:");
    for i in 0..2 {
        let allowed = rl.allow();
        println!("  Request {}: allowed={}", i + 1, allowed);
    }
    println!();
}

fn sliding_window_example() {
    println!("--- Sliding Window Counter ---");

    // Max 3 requests per second
    let counter = SlidingWindowCounter::new(Duration::from_millis(500), 3);

    println!("  Testing window limit (max 3 per 500ms):");
    for i in 0..5 {
        let allowed = counter.allow();
        println!("  Request {}: allowed={}, count={}", 
            i + 1, allowed, counter.count());
    }

    println!("\n  Waiting for window to expire...");
    std::thread::sleep(Duration::from_millis(600));

    println!("  After window expires:");
    for i in 0..2 {
        let allowed = counter.allow();
        println!("  Request {}: allowed={}", i + 1, allowed);
    }
    println!();
}

fn convenience_functions_example() {
    println!("--- Convenience Functions ---");

    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    // Exponential backoff
    let result = exponential_backoff(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count < 3 {
            Err("error")
        } else {
            Ok("exp-backoff success")
        }
    }, 5, Duration::from_millis(20));
    println!("  exponential_backoff: attempts={}, success={}", 
        result.attempts, result.success);

    // Fixed delay
    counter.store(0, Ordering::SeqCst);
    let result = fixed_delay(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count < 2 {
            Err("error")
        } else {
            Ok("fixed-delay success")
        }
    }, 3, Duration::from_millis(20));
    println!("  fixed_delay: attempts={}, success={}", 
        result.attempts, result.success);

    // Linear backoff
    counter.store(0, Ordering::SeqCst);
    let result = linear_backoff(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count < 2 {
            Err("error")
        } else {
            Ok("linear-backoff success")
        }
    }, 3, Duration::from_millis(20));
    println!("  linear_backoff: attempts={}, success={}", 
        result.attempts, result.success);

    // Until success
    counter.store(0, Ordering::SeqCst);
    let result = until_success(|| {
        let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count < 5 {
            Err("error")
        } else {
            Ok("until-success complete")
        }
    }, Duration::from_millis(10), Duration::from_secs(5));
    println!("  until_success: attempts={}, success={}", 
        result.attempts, result.success);
    println!();
}

fn retry_filter_example() {
    println!("--- Retry Filter ---");

    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    let result = RetryBuilder::new()
        .max_attempts(5)
        .retry_on(|err| err.contains("retryable"))
        .execute(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            match count {
                1 => Err("retryable timeout"),
                _ => Err("permanent auth error"),
            }
        });

    println!("  With filter: attempts={}, success={}", 
        result.attempts, result.success);
    println!("  Stopped because 'auth error' doesn't match filter");
    println!();
}

fn callback_example() {
    println!("--- Callbacks ---");

    let counter = Arc::new(AtomicU32::new(0));
    let counter_clone = counter.clone();

    let result = RetryBuilder::new()
        .max_attempts(5)
        .initial_delay(Duration::from_millis(20))
        .on_retry(|attempt, err| {
            println!("  [Retry {}] Error: {}", attempt, err);
        })
        .on_success(|attempts, duration| {
            println!("  [Success] {} attempts in {:?}", attempts, duration);
        })
        .on_failure(|attempts, duration, err| {
            println!("  [Failure] {} attempts in {:?}: {}", attempts, duration, err);
        })
        .execute(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            if count < 3 {
                Err("temporary error")
            } else {
                Ok(42)
            }
        });

    println!("  Final: success={}", result.success);
    println!();
}

fn decorrelated_jitter_example() {
    println!("--- Decorrelated Jitter ---");

    let base = Duration::from_millis(100);
    let cap = Duration::from_secs(1);

    println!("  Delay progression:");
    for attempt in 1..6 {
        let delay = decorrelated_jitter(base, cap, attempt);
        println!("    Attempt {}: {:?}", attempt, delay);
    }
    println!();
}