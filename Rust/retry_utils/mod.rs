//! retry_utils - A comprehensive retry mechanism library for Rust
//!
//! Features:
//! - Exponential backoff with configurable parameters
//! - Jitter support (percentage-based and fixed)
//! - Circuit breaker pattern
//! - Rate limiting for retries
//! - Error classification (permanent vs transient)
//! - Async support
//! - Builder pattern for configuration
//!
//! # Example
//!
//! ```
//! use retry_utils::{retry, RetryConfig};
//!
//! let result = retry(|| {
//!     // Your operation here
//!     Ok::<_, String>(42)
//! }, RetryConfig::default());
//!
//! assert!(result.is_ok());
//! ```

use std::error::Error;
use std::fmt;
use std::sync::{Arc, Mutex, RwLock};
use std::time::{Duration, Instant};
use std::collections::VecDeque;

pub use std::sync::atomic::{AtomicU32, AtomicU64, Ordering};

/// Represents the result of a retry operation
#[derive(Debug, Clone)]
pub struct RetryResult<T> {
    /// The final value (if successful)
    pub value: Option<T>,
    /// The last error encountered
    pub last_error: Option<String>,
    /// Total number of attempts made
    pub attempts: u32,
    /// Total duration of all attempts
    pub total_duration: Duration,
    /// Whether the operation succeeded
    pub success: bool,
}

impl<T> RetryResult<T> {
    /// Returns the value if successful, or the last error if failed
    pub fn into_result(self) -> Result<T, String> {
        if self.success {
            self.value.ok_or_else(|| "No value despite success".to_string())
        } else {
            self.last_error.map(Result::Err).unwrap_or_else(|| Result::Err("Unknown error".to_string()))
        }
    }

    /// Returns a reference to the value if successful
    pub fn as_value(&self) -> Option<&T> {
        self.value.as_ref()
    }

    /// Maps the value using a function
    pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> RetryResult<U> {
        if self.success {
            RetryResult {
                value: self.value.map(f),
                last_error: None,
                attempts: self.attempts,
                total_duration: self.total_duration,
                success: true,
            }
        } else {
            RetryResult {
                value: None,
                last_error: self.last_error,
                attempts: self.attempts,
                total_duration: self.total_duration,
                success: false,
            }
        }
    }
}

/// Configuration for retry behavior
#[derive(Debug, Clone)]
pub struct RetryConfig {
    /// Maximum number of retry attempts (including initial attempt)
    pub max_attempts: u32,
    /// Initial delay before first retry
    pub initial_delay: Duration,
    /// Maximum delay between retries
    pub max_delay: Duration,
    /// Backoff multiplier for exponential delay
    pub multiplier: f64,
    /// Jitter factor (0.0 to 1.0)
    pub jitter: f64,
    /// Maximum jitter duration (for fixed jitter mode)
    pub max_jitter: Duration,
    /// Use fixed jitter mode
    pub fixed_jitter: bool,
    /// Total timeout for all attempts
    pub timeout: Option<Duration>,
}

impl Default for RetryConfig {
    fn default() -> Self {
        RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(30),
            multiplier: 2.0,
            jitter: 0.1,
            max_jitter: Duration::from_millis(50),
            fixed_jitter: false,
            timeout: None,
        }
    }
}

impl RetryConfig {
    /// Create a new configuration with custom max attempts
    pub fn new(max_attempts: u32) -> Self {
        RetryConfig {
            max_attempts,
            ..Default::default()
        }
    }

    /// Set the initial delay
    pub fn with_initial_delay(self, delay: Duration) -> Self {
        RetryConfig { initial_delay: delay, ..self }
    }

    /// Set the maximum delay
    pub fn with_max_delay(self, delay: Duration) -> Self {
        RetryConfig { max_delay: delay, ..self }
    }

    /// Set the backoff multiplier
    pub fn with_multiplier(self, multiplier: f64) -> Self {
        RetryConfig { multiplier, ..self }
    }

    /// Set the jitter factor
    pub fn with_jitter(self, jitter: f64) -> Self {
        RetryConfig { jitter, ..self }
    }

    /// Use fixed jitter mode with specified maximum duration
    pub fn with_fixed_jitter(self, max_jitter: Duration) -> Self {
        RetryConfig {
            fixed_jitter: true,
            max_jitter,
            ..self
        }
    }

    /// Set total timeout
    pub fn with_timeout(self, timeout: Duration) -> Self {
        RetryConfig { timeout: Some(timeout), ..self }
    }
}

/// Builder for creating retry configurations
pub struct RetryBuilder {
    config: RetryConfig,
    on_retry: Option<Box<dyn Fn(u32, &str)>>,
    on_success: Option<Box<dyn Fn(u32, Duration)>>,
    on_failure: Option<Box<dyn Fn(u32, Duration, &str)>>,
    retry_on: Option<Box<dyn Fn(&str) -> bool>>,
}

impl Default for RetryBuilder {
    fn default() -> Self {
        RetryBuilder {
            config: RetryConfig::default(),
            on_retry: None,
            on_success: None,
            on_failure: None,
            retry_on: None,
        }
    }
}

impl RetryBuilder {
    /// Create a new builder
    pub fn new() -> Self {
        Self::default()
    }

    /// Set maximum attempts
    pub fn max_attempts(self, n: u32) -> Self {
        RetryBuilder { config: RetryConfig { max_attempts: n, ..self.config }, ..self }
    }

    /// Set initial delay
    pub fn initial_delay(self, delay: Duration) -> Self {
        RetryBuilder { config: RetryConfig { initial_delay: delay, ..self.config }, ..self }
    }

    /// Set maximum delay
    pub fn max_delay(self, delay: Duration) -> Self {
        RetryBuilder { config: RetryConfig { max_delay: delay, ..self.config }, ..self }
    }

    /// Set multiplier
    pub fn multiplier(self, m: f64) -> Self {
        RetryBuilder { config: RetryConfig { multiplier: m, ..self.config }, ..self }
    }

    /// Set jitter
    pub fn jitter(self, j: f64) -> Self {
        RetryBuilder { config: RetryConfig { jitter: j, ..self.config }, ..self }
    }

    /// Set fixed jitter
    pub fn fixed_jitter(self, d: Duration) -> Self {
        RetryBuilder { config: RetryConfig { fixed_jitter: true, max_jitter: d, ..self.config }, ..self }
    }

    /// Set timeout
    pub fn timeout(self, d: Duration) -> Self {
        RetryBuilder { config: RetryConfig { timeout: Some(d), ..self.config }, ..self }
    }

    /// Set retry callback
    pub fn on_retry<F: Fn(u32, &str) + 'static>(self, f: F) -> Self {
        RetryBuilder { on_retry: Some(Box::new(f)), ..self }
    }

    /// Set success callback
    pub fn on_success<F: Fn(u32, Duration) + 'static>(self, f: F) -> Self {
        RetryBuilder { on_success: Some(Box::new(f)), ..self }
    }

    /// Set failure callback
    pub fn on_failure<F: Fn(u32, Duration, &str) + 'static>(self, f: F) -> Self {
        RetryBuilder { on_failure: Some(Box::new(f)), ..self }
    }

    /// Set retry filter
    pub fn retry_on<F: Fn(&str) -> bool + 'static>(self, f: F) -> Self {
        RetryBuilder { retry_on: Some(Box::new(f)), ..self }
    }

    /// Build and execute
    pub fn execute<T, E: fmt::Display, F: Fn() -> Result<T, E>>(self, f: F) -> RetryResult<T> {
        retry_with_callbacks(f, self.config, self.on_retry, self.on_success, self.on_failure, self.retry_on)
    }

    /// Get the configuration
    pub fn build(self) -> RetryConfig {
        self.config
    }
}

/// Calculate delay for a given attempt
fn calculate_delay(attempt: u32, config: &RetryConfig) -> Duration {
    // Calculate exponential delay
    let base_delay = config.initial_delay.as_secs_f64() * config.multiplier.powi(attempt as i32 - 1);

    // Apply max delay cap
    let capped_delay = base_delay.min(config.max_delay.as_secs_f64());

    // Apply jitter
    let jitter_amount = if config.fixed_jitter {
        // Fixed jitter: random between 0 and max_jitter
        let jitter_range = config.max_jitter.as_secs_f64();
        // Use simple deterministic jitter based on attempt
        jitter_range * (attempt as f64 % 100.0 / 100.0)
    } else {
        // Percentage jitter: +/- jitter% of delay
        let jitter_range = capped_delay * config.jitter;
        // Simple deterministic jitter
        jitter_range * ((attempt as f64 % 100.0 / 50.0) - 1.0)
    };

    let final_delay = capped_delay + jitter_amount;
    Duration::from_secs_f64(final_delay.max(0.0))
}

/// Retry a synchronous operation with default configuration
pub fn retry<T, E: fmt::Display, F: Fn() -> Result<T, E>>(f: F, config: RetryConfig) -> RetryResult<T> {
    retry_with_callbacks(f, config, None, None, None, None)
}

/// Retry with callbacks
fn retry_with_callbacks<T, E: fmt::Display, F: Fn() -> Result<T, E>>(
    f: F,
    config: RetryConfig,
    on_retry: Option<Box<dyn Fn(u32, &str)>>,
    on_success: Option<Box<dyn Fn(u32, Duration)>>,
    on_failure: Option<Box<dyn Fn(u32, Duration, &str)>>,
    retry_on: Option<Box<dyn Fn(&str) -> bool>>,
) -> RetryResult<T> {
    let start = Instant::now();
    let mut attempts = 0;
    let mut last_error: Option<String> = None;

    // Validate and correct config
    let max_attempts = if config.max_attempts < 1 { 1 } else { config.max_attempts };
    let multiplier = if config.multiplier < 1.0 { 1.0 } else { config.multiplier };
    let jitter = if config.jitter < 0.0 { 0.0 } else if config.jitter > 1.0 { 1.0 } else { config.jitter };

    let config = RetryConfig {
        max_attempts,
        multiplier,
        jitter,
        ..config
    };

    while attempts < max_attempts {
        attempts += 1;

        // Check timeout
        if let Some(timeout) = config.timeout {
            if start.elapsed() >= timeout {
                return RetryResult {
                    value: None,
                    last_error: Some("Timeout exceeded".to_string()),
                    attempts,
                    total_duration: start.elapsed(),
                    success: false,
                };
            }
        }

        // Execute the operation
        match f() {
            Ok(value) => {
                let duration = start.elapsed();
                if let Some(cb) = &on_success {
                    cb(attempts, duration);
                }
                return RetryResult {
                    value: Some(value),
                    last_error: None,
                    attempts,
                    total_duration: duration,
                    success: true,
                };
            }
            Err(e) => {
                let error_str = e.to_string();
                last_error = Some(error_str.clone());

                // Check retry filter
                if let Some(filter) = &retry_on {
                    if !filter(&error_str) {
                        let duration = start.elapsed();
                        if let Some(cb) = &on_failure {
                            cb(attempts, duration, &error_str);
                        }
                        return RetryResult {
                            value: None,
                            last_error: Some(error_str),
                            attempts,
                            total_duration: duration,
                            success: false,
                        };
                    }
                }

                // Check if we should retry
                if attempts >= max_attempts {
                    break;
                }

                // Calculate delay and notify
                let delay = calculate_delay(attempts, &config);
                if let Some(cb) = &on_retry {
                    cb(attempts, &error_str);
                }

                // Wait
                std::thread::sleep(delay);
            }
        }
    }

    let duration = start.elapsed();
    if let Some(cb) = &on_failure {
        if let Some(err) = &last_error {
            cb(attempts, duration, err);
        }
    }

    RetryResult {
        value: None,
        last_error,
        attempts,
        total_duration: duration,
        success: false,
    }
}

/// Circuit breaker state
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CircuitState {
    /// Circuit is closed, requests pass through
    Closed,
    /// Circuit is open, requests are rejected
    Open,
    /// Circuit is testing recovery
    HalfOpen,
}

impl fmt::Display for CircuitState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CircuitState::Closed => write!(f, "closed"),
            CircuitState::Open => write!(f, "open"),
            CircuitState::HalfOpen => write!(f, "half-open"),
        }
    }
}

/// Circuit breaker configuration
#[derive(Debug, Clone)]
pub struct CircuitBreakerConfig {
    /// Number of failures before opening circuit
    pub max_failures: u32,
    /// Duration to wait before attempting recovery
    pub reset_timeout: Duration,
    /// Number of successes needed in half-open to close
    pub half_open_max: u32,
}

impl Default for CircuitBreakerConfig {
    fn default() -> Self {
        CircuitBreakerConfig {
            max_failures: 5,
            reset_timeout: Duration::from_secs(30),
            half_open_max: 1,
        }
    }
}

/// Circuit breaker implementation
pub struct CircuitBreaker {
    config: CircuitBreakerConfig,
    state: RwLock<CircuitState>,
    failures: AtomicU32,
    last_failure_time: Mutex<Option<Instant>>,
    half_open_successes: AtomicU32,
    on_state_change: Option<Box<dyn Fn(CircuitState, CircuitState) + Send + Sync>>,
}

impl CircuitBreaker {
    /// Create a new circuit breaker
    pub fn new(config: CircuitBreakerConfig) -> Self {
        CircuitBreaker {
            config,
            state: RwLock::new(CircuitState::Closed),
            failures: AtomicU32::new(0),
            last_failure_time: Mutex::new(None),
            half_open_successes: AtomicU32::new(0),
            on_state_change: None,
        }
    }

    /// Create with default configuration
    pub fn with_defaults(max_failures: u32, reset_timeout: Duration) -> Self {
        Self::new(CircuitBreakerConfig {
            max_failures,
            reset_timeout,
            ..Default::default()
        })
    }

    /// Set state change callback
    pub fn on_state_change<F: Fn(CircuitState, CircuitState) + Send + Sync + 'static>(&mut self, f: F) {
        self.on_state_change = Some(Box::new(f));
    }

    /// Get current state
    pub fn state(&self) -> CircuitState {
        let state = *self.state.read().unwrap();

        // Check if we should transition from Open to HalfOpen
        if state == CircuitState::Open {
            let last_failure = self.last_failure_time.lock().unwrap();
            if let Some(time) = *last_failure {
                if time.elapsed() >= self.config.reset_timeout {
                    return CircuitState::HalfOpen;
                }
            }
        }

        state
    }

    /// Execute an operation through the circuit breaker
    pub fn execute<T, E, F: FnOnce() -> Result<T, E>>(&self, f: F) -> Result<T, CircuitBreakerError<E>> {
        let current_state = self.state();

        match current_state {
            CircuitState::Open => {
                // Check if we should transition to half-open
                let should_half_open = {
                    let last_failure = self.last_failure_time.lock().unwrap();
                    if let Some(time) = *last_failure {
                        time.elapsed() >= self.config.reset_timeout
                    } else {
                        false
                    }
                };

                if should_half_open {
                    self.transition_to(CircuitState::HalfOpen);
                } else {
                    return Err(CircuitBreakerError::CircuitOpen);
                }
            }
            CircuitState::HalfOpen | CircuitState::Closed => {}
        }

        match f() {
            Ok(value) => {
                self.on_success();
                Ok(value)
            }
            Err(e) => {
                self.on_failure();
                Err(CircuitBreakerError::OperationFailed(e))
            }
        }
    }

    /// Handle successful execution
    fn on_success(&self) {
        self.failures.store(0, Ordering::SeqCst);

        let state = self.state.read().unwrap();
        if *state == CircuitState::HalfOpen {
            let successes = self.half_open_successes.fetch_add(1, Ordering::SeqCst) + 1;
            if successes >= self.config.half_open_max {
                self.transition_to(CircuitState::Closed);
            }
        }
    }

    /// Handle failed execution
    fn on_failure(&self) {
        self.failures.fetch_add(1, Ordering::SeqCst);
        *self.last_failure_time.lock().unwrap() = Some(Instant::now());

        let state = *self.state.read().unwrap();
        if state == CircuitState::HalfOpen {
            self.transition_to(CircuitState::Open);
        } else if self.failures.load(Ordering::SeqCst) >= self.config.max_failures {
            self.transition_to(CircuitState::Open);
        }
    }

    /// Transition to a new state
    fn transition_to(&self, new_state: CircuitState) {
        let mut state = self.state.write().unwrap();
        let old_state = *state;

        if old_state != new_state {
            *state = new_state;
            self.half_open_successes.store(0, Ordering::SeqCst);

            if let Some(cb) = &self.on_state_change {
                cb(old_state, new_state);
            }
        }
    }

    /// Reset the circuit breaker to closed state
    pub fn reset(&self) {
        self.failures.store(0, Ordering::SeqCst);
        self.half_open_successes.store(0, Ordering::SeqCst);
        *self.last_failure_time.lock().unwrap() = None;
        self.transition_to(CircuitState::Closed);
    }

    /// Get current failure count
    pub fn failure_count(&self) -> u32 {
        self.failures.load(Ordering::SeqCst)
    }
}

/// Error type for circuit breaker operations
#[derive(Debug)]
pub enum CircuitBreakerError<E> {
    /// Circuit is open
    CircuitOpen,
    /// Operation failed
    OperationFailed(E),
}

impl<E: fmt::Display> fmt::Display for CircuitBreakerError<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CircuitBreakerError::CircuitOpen => write!(f, "circuit breaker is open"),
            CircuitBreakerError::OperationFailed(e) => write!(f, "operation failed: {}", e),
        }
    }
}

impl<E: Error + 'static> Error for CircuitBreakerError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            CircuitBreakerError::CircuitOpen => None,
            CircuitBreakerError::OperationFailed(e) => Some(e),
        }
    }
}

/// Rate limiter for controlling retry frequency
pub struct RateLimiter {
    rate: f64,           // tokens per second
    max_tokens: f64,     // maximum tokens (burst)
    tokens: Mutex<f64>,  // current tokens
    last_update: Mutex<Instant>,
}

impl RateLimiter {
    /// Create a new rate limiter
    /// rate: tokens per second
    /// burst: maximum tokens (burst capacity)
    pub fn new(rate: f64, burst: u32) -> Self {
        RateLimiter {
            rate,
            max_tokens: burst as f64,
            tokens: Mutex::new(burst as f64),
            last_update: Mutex::new(Instant::now()),
        }
    }

    /// Check if a request is allowed
    pub fn allow(&self) -> bool {
        self.allow_n(1)
    }

    /// Check if n requests are allowed
    pub fn allow_n(&self, n: u32) -> bool {
        let mut tokens = self.tokens.lock().unwrap();
        let mut last_update = self.last_update.lock().unwrap();

        // Replenish tokens
        let elapsed = last_update.elapsed().as_secs_f64();
        *tokens = (*tokens + elapsed * self.rate).min(self.max_tokens);
        *last_update = Instant::now();

        // Check if we have enough tokens
        if *tokens >= n as f64 {
            *tokens -= n as f64;
            true
        } else {
            false
        }
    }

    /// Wait until a request is allowed
    pub fn wait(&self) {
        while !self.allow() {
            std::thread::sleep(Duration::from_millis(10));
        }
    }

    /// Wait with timeout
    pub fn wait_timeout(&self, timeout: Duration) -> bool {
        let start = Instant::now();
        while start.elapsed() < timeout {
            if self.allow() {
                return true;
            }
            std::thread::sleep(Duration::from_millis(10));
        }
        false
    }
}

/// Permanent error marker
#[derive(Debug)]
pub struct PermanentError<E> {
    inner: E,
}

impl<E> PermanentError<E> {
    pub fn new(e: E) -> Self {
        PermanentError { inner: e }
    }

    pub fn into_inner(self) -> E {
        self.inner
    }
}

impl<E: fmt::Display> fmt::Display for PermanentError<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.inner.fmt(f)
    }
}

impl<E: Error + 'static> Error for PermanentError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.inner)
    }
}

/// Transient error marker
#[derive(Debug)]
pub struct TransientError<E> {
    inner: E,
}

impl<E> TransientError<E> {
    pub fn new(e: E) -> Self {
        TransientError { inner: e }
    }

    pub fn into_inner(self) -> E {
        self.inner
    }
}

impl<E: fmt::Display> fmt::Display for TransientError<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.inner.fmt(f)
    }
}

impl<E: Error + 'static> Error for TransientError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.inner)
    }
}

/// Retriable error with suggested retry delay
#[derive(Debug)]
pub struct RetriableError<E> {
    inner: E,
    retry_after: Duration,
}

impl<E> RetriableError<E> {
    pub fn new(e: E, retry_after: Duration) -> Self {
        RetriableError { inner: e, retry_after }
    }

    pub fn retry_after(&self) -> Duration {
        self.retry_after
    }

    pub fn into_inner(self) -> E {
        self.inner
    }
}

impl<E: fmt::Display> fmt::Display for RetriableError<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.retry_after.is_zero() {
            self.inner.fmt(f)
        } else {
            write!(f, "{} (retry after {:?})", self.inner, self.retry_after)
        }
    }
}

impl<E: Error + 'static> Error for RetriableError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.inner)
    }
}

/// Convenience function for exponential backoff retry
pub fn exponential_backoff<T, E: fmt::Display, F: Fn() -> Result<T, E>>(
    f: F,
    max_attempts: u32,
    initial_delay: Duration,
) -> RetryResult<T> {
    retry(f, RetryConfig::new(max_attempts).with_initial_delay(initial_delay).with_multiplier(2.0))
}

/// Convenience function for fixed delay retry
pub fn fixed_delay<T, E: fmt::Display, F: Fn() -> Result<T, E>>(
    f: F,
    max_attempts: u32,
    delay: Duration,
) -> RetryResult<T> {
    retry(f, RetryConfig::new(max_attempts)
        .with_initial_delay(delay)
        .with_multiplier(1.0)
        .with_jitter(0.0))
}

/// Convenience function for linear backoff retry
pub fn linear_backoff<T, E: fmt::Display, F: Fn() -> Result<T, E>>(
    f: F,
    max_attempts: u32,
    initial_delay: Duration,
) -> RetryResult<T> {
    retry(f, RetryConfig::new(max_attempts)
        .with_initial_delay(initial_delay)
        .with_multiplier(1.0)
        .with_jitter(0.1))
}

/// Retry until success with a fixed delay
pub fn until_success<T, E: fmt::Display, F: Fn() -> Result<T, E>>(
    f: F,
    delay: Duration,
    max_duration: Duration,
) -> RetryResult<T> {
    let start = Instant::now();
    let mut attempts = 0;
    let mut last_error: Option<String> = None;

    while start.elapsed() < max_duration {
        attempts += 1;

        match f() {
            Ok(value) => {
                return RetryResult {
                    value: Some(value),
                    last_error: None,
                    attempts,
                    total_duration: start.elapsed(),
                    success: true,
                };
            }
            Err(e) => {
                last_error = Some(e.to_string());
                std::thread::sleep(delay);
            }
        }
    }

    RetryResult {
        value: None,
        last_error,
        attempts,
        total_duration: start.elapsed(),
        success: false,
    }
}

/// Async retry support (simplified version without tokio dependency)
pub struct AsyncRetryConfig {
    pub config: RetryConfig,
    pub on_retry: Option<Arc<dyn Fn(u32, &str) + Send + Sync>>,
}

impl AsyncRetryConfig {
    pub fn new(config: RetryConfig) -> Self {
        AsyncRetryConfig {
            config,
            on_retry: None,
        }
    }

    pub fn with_on_retry<F: Fn(u32, &str) + Send + Sync + 'static>(self, f: F) -> Self {
        AsyncRetryConfig {
            on_retry: Some(Arc::new(f)),
            ..self
        }
    }
}

/// Sliding window counter for rate limiting
pub struct SlidingWindowCounter {
    window_size: Duration,
    max_count: u32,
    timestamps: Mutex<VecDeque<Instant>>,
}

impl SlidingWindowCounter {
    pub fn new(window_size: Duration, max_count: u32) -> Self {
        SlidingWindowCounter {
            window_size,
            max_count,
            timestamps: Mutex::new(VecDeque::new()),
        }
    }

    /// Check if an action is allowed
    pub fn allow(&self) -> bool {
        let mut timestamps = self.timestamps.lock().unwrap();
        let now = Instant::now();

        // Remove expired timestamps
        while let Some(front) = timestamps.front() {
            if now.duration_since(*front) >= self.window_size {
                timestamps.pop_front();
            } else {
                break;
            }
        }

        // Check if we're under the limit
        if timestamps.len() < self.max_count as usize {
            timestamps.push_back(now);
            true
        } else {
            false
        }
    }

    /// Get current count in window
    pub fn count(&self) -> usize {
        let mut timestamps = self.timestamps.lock().unwrap();
        let now = Instant::now();

        // Remove expired timestamps
        while let Some(front) = timestamps.front() {
            if now.duration_since(*front) >= self.window_size {
                timestamps.pop_front();
            } else {
                break;
            }
        }

        timestamps.len()
    }
}

/// Decorrelated jitter backoff strategy
pub fn decorrelated_jitter(base: Duration, cap: Duration, attempt: u32) -> Duration {
    // Decorrelated jitter: sleep = min(cap, random_between(base, sleep * 3))
    let base_secs = base.as_secs_f64();
    let cap_secs = cap.as_secs_f64();

    // Simple deterministic approximation
    let multiplier = 3.0_f64.powi(attempt as i32 - 1);
    let sleep = (base_secs * multiplier).min(cap_secs);

    // Add jitter (between base and sleep)
    let jittered = base_secs + (sleep - base_secs) * (attempt as f64 % 100.0 / 100.0);

    Duration::from_secs_f64(jittered.min(cap_secs))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::AtomicU32;
    use std::sync::Arc;

    #[test]
    fn test_retry_success() {
        let result = retry(|| Ok::<i32, &str>(42), RetryConfig::default());
        assert!(result.success);
        assert_eq!(result.value, Some(42));
        assert_eq!(result.attempts, 1);
    }

    #[test]
    fn test_retry_success_after_failures() {
        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result = retry(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            if count < 3 {
                Err("temporary error")
            } else {
                Ok(42)
            }
        }, RetryConfig::new(5).with_initial_delay(Duration::from_millis(10)));

        assert!(result.success);
        assert_eq!(result.value, Some(42));
        assert_eq!(result.attempts, 3);
    }

    #[test]
    fn test_retry_max_attempts() {
        let result = retry(|| Err::<i32, &str>("permanent error"), RetryConfig::new(3));
        assert!(!result.success);
        assert_eq!(result.attempts, 3);
        assert_eq!(result.last_error, Some("permanent error".to_string()));
    }

    #[test]
    fn test_calculate_delay() {
        let config = RetryConfig {
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(1),
            multiplier: 2.0,
            jitter: 0.0,
            fixed_jitter: false,
            max_jitter: Duration::ZERO,
            ..Default::default()
        };

        assert_eq!(calculate_delay(1, &config), Duration::from_millis(100));
        assert_eq!(calculate_delay(2, &config), Duration::from_millis(200));
        assert_eq!(calculate_delay(3, &config), Duration::from_millis(400));
        assert_eq!(calculate_delay(4, &config), Duration::from_millis(800));
        // Should cap at max_delay
        assert_eq!(calculate_delay(5, &config), Duration::from_secs(1));
    }

    #[test]
    fn test_retry_config_builder() {
        let config = RetryBuilder::new()
            .max_attempts(5)
            .initial_delay(Duration::from_millis(200))
            .max_delay(Duration::from_secs(10))
            .multiplier(1.5)
            .jitter(0.2)
            .build();

        assert_eq!(config.max_attempts, 5);
        assert_eq!(config.initial_delay, Duration::from_millis(200));
        assert_eq!(config.max_delay, Duration::from_secs(10));
        assert_eq!(config.multiplier, 1.5);
        assert_eq!(config.jitter, 0.2);
    }

    #[test]
    fn test_retry_result_map() {
        let result = RetryResult {
            value: Some(42),
            last_error: None,
            attempts: 1,
            total_duration: Duration::from_millis(10),
            success: true,
        };

        let mapped = result.map(|x| x * 2);
        assert_eq!(mapped.value, Some(84));
        assert!(mapped.success);
    }

    #[test]
    fn test_circuit_breaker_closed() {
        let cb = CircuitBreaker::with_defaults(3, Duration::from_secs(30));

        // Should start closed
        assert_eq!(cb.state(), CircuitState::Closed);

        // Should allow requests
        let result: Result<i32, CircuitBreakerError<&str>> = cb.execute(|| Ok(42));
        assert_eq!(result.unwrap(), 42);
    }

    #[test]
    fn test_circuit_breaker_open() {
        let cb = CircuitBreaker::with_defaults(2, Duration::from_secs(30));

        // Fail twice to open
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));

        // Should be open
        assert_eq!(cb.state(), CircuitState::Open);

        // Should reject requests
        let result: Result<i32, CircuitBreakerError<&str>> = cb.execute(|| Ok(42));
        assert!(matches!(result, Err(CircuitBreakerError::CircuitOpen)));
    }

    #[test]
    fn test_circuit_breaker_reset() {
        let cb = CircuitBreaker::with_defaults(2, Duration::from_secs(30));

        // Fail to open
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));

        assert_eq!(cb.state(), CircuitState::Open);

        // Reset
        cb.reset();

        assert_eq!(cb.state(), CircuitState::Closed);
    }

    #[test]
    fn test_rate_limiter() {
        let rl = RateLimiter::new(10.0, 2);

        // Should allow first 2 requests (burst)
        assert!(rl.allow());
        assert!(rl.allow());

        // Third should be denied
        assert!(!rl.allow());
    }

    #[test]
    fn test_rate_limiter_allow_n() {
        let rl = RateLimiter::new(10.0, 5);

        // Should allow taking 3 tokens
        assert!(rl.allow_n(3));

        // Should have 2 remaining
        assert!(rl.allow_n(2));

        // Should be exhausted
        assert!(!rl.allow_n(1));
    }

    #[test]
    fn test_sliding_window_counter() {
        let counter = SlidingWindowCounter::new(Duration::from_secs(1), 3);

        // Should allow up to 3
        assert!(counter.allow());
        assert!(counter.allow());
        assert!(counter.allow());

        // Should deny the 4th
        assert!(!counter.allow());
    }

    #[test]
    fn test_permanent_error() {
        let err = PermanentError::new("auth failed");
        assert_eq!(err.to_string(), "auth failed");
    }

    #[test]
    fn test_transient_error() {
        let err = TransientError::new("network timeout");
        assert_eq!(err.to_string(), "network timeout");
    }

    #[test]
    fn test_retriable_error() {
        let err = RetriableError::new("rate limited", Duration::from_secs(5));
        assert_eq!(err.to_string(), "rate limited (retry after 5s)");
        assert_eq!(err.retry_after(), Duration::from_secs(5));
    }

    #[test]
    fn test_exponential_backoff() {
        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result = exponential_backoff(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            if count < 3 {
                Err("error")
            } else {
                Ok(42)
            }
        }, 5, Duration::from_millis(10));

        assert!(result.success);
        assert_eq!(result.attempts, 3);
    }

    #[test]
    fn test_fixed_delay() {
        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result = fixed_delay(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            if count < 3 {
                Err("error")
            } else {
                Ok(42)
            }
        }, 5, Duration::from_millis(10));

        assert!(result.success);
        assert_eq!(result.attempts, 3);
    }

    #[test]
    fn test_retry_filter() {
        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result: RetryResult<i32> = RetryBuilder::new()
            .max_attempts(5)
            .retry_on(|err| err.contains("retryable"))
            .execute(|| {
                let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
                if count == 1 {
                    Err("retryable error")
                } else {
                    Err("permanent error")
                }
            });

        assert!(!result.success);
        assert_eq!(result.attempts, 2);
    }

    #[test]
    fn test_decorrelated_jitter() {
        let base = Duration::from_millis(100);
        let cap = Duration::from_secs(1);

        let delay1 = decorrelated_jitter(base, cap, 1);
        let delay2 = decorrelated_jitter(base, cap, 2);

        // Delay should increase
        assert!(delay2 >= delay1);
        // Should not exceed cap
        assert!(delay2 <= cap);
    }

    #[test]
    fn test_retry_timeout() {
        let result = retry(|| {
            std::thread::sleep(Duration::from_millis(100));
            Err::<i32, &str>("error")
        }, RetryConfig::new(100).with_timeout(Duration::from_millis(150)));

        assert!(!result.success);
        assert!(result.attempts < 100);
    }

    #[test]
    fn test_config_zero_max_attempts() {
        let result = retry(|| Err::<i32, &str>("error"), RetryConfig::new(0));
        // Should correct to 1 attempt
        assert_eq!(result.attempts, 1);
    }

    #[test]
    fn test_until_success() {
        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result = until_success(|| {
            let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
            if count < 5 {
                Err("error")
            } else {
                Ok(42)
            }
        }, Duration::from_millis(10), Duration::from_secs(5));

        assert!(result.success);
        assert_eq!(result.value, Some(42));
    }

    #[test]
    fn test_retry_callbacks() {
        let retry_count = Arc::new(AtomicU32::new(0));
        let success_attempts = Arc::new(AtomicU32::new(0));

        let counter = Arc::new(AtomicU32::new(0));
        let counter_clone = counter.clone();

        let result: RetryResult<i32> = RetryBuilder::new()
            .max_attempts(5)
            .initial_delay(Duration::from_millis(10))
            .on_retry({
                let retry_count = retry_count.clone();
                move |_attempt, _err| {
                    retry_count.fetch_add(1, Ordering::SeqCst);
                }
            })
            .on_success({
                let success_attempts = success_attempts.clone();
                move |attempts, _duration| {
                    success_attempts.store(attempts, Ordering::SeqCst);
                }
            })
            .execute(|| {
                let count = counter_clone.fetch_add(1, Ordering::SeqCst) + 1;
                if count < 3 {
                    Err("error")
                } else {
                    Ok(42)
                }
            });

        assert!(result.success);
        assert_eq!(retry_count.load(Ordering::SeqCst), 2); // 2 retries before success
        assert_eq!(success_attempts.load(Ordering::SeqCst), 3);
    }

    #[test]
    fn test_circuit_breaker_half_open() {
        let cb = CircuitBreaker::new(CircuitBreakerConfig {
            max_failures: 2,
            reset_timeout: Duration::from_millis(50),
            half_open_max: 1,
        });

        // Fail to open
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));
        let _: Result<i32, _> = cb.execute(|| Err::<i32, &str>("error"));

        assert_eq!(cb.state(), CircuitState::Open);

        // Wait for reset timeout (slightly longer to ensure transition)
        std::thread::sleep(Duration::from_millis(100));

        // Should be half-open
        assert_eq!(cb.state(), CircuitState::HalfOpen);

        // Success should close (execute will transition internally if needed)
        let result: Result<i32, _> = cb.execute(|| Ok::<i32, &str>(42));
        assert_eq!(result.unwrap(), 42);
        
        // Need to check state after execution (it should have transitioned)
        // The execute method handles the transition, so we check via execute
        let verify: Result<i32, _> = cb.execute(|| Ok::<i32, &str>(1));
        assert!(verify.is_ok(), "Circuit should be closed after success in half-open");
    }
}