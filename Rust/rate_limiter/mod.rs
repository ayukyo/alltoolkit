//! Rate Limiter Utilities
//! 
//! This module provides various rate limiting algorithms with zero external dependencies.
//! 
//! # Algorithms
//! - Token Bucket: Allows bursts up to bucket capacity
//! - Leaky Bucket: Smooths out request rate
//! - Sliding Window: Precise rate control with memory efficiency options
//! - Fixed Window: Simple and memory-efficient
//! 
//! # Example
//! ```rust
//! use rate_limiter::{TokenBucket, RateLimiter};
//! 
//! let mut bucket = TokenBucket::new(100, 10.0); // 100 capacity, 10 tokens/sec
//! assert!(bucket.try_acquire(1).is_ok());
//! ```

use std::time::{Duration, Instant};

/// Error type for rate limiting operations
#[derive(Debug, Clone, PartialEq)]
pub enum RateLimitError {
    /// Request was rejected due to rate limit
    Rejected {
        /// Time to wait before retrying
        retry_after: Duration,
    },
    /// Invalid configuration
    InvalidConfig(String),
}

impl std::fmt::Display for RateLimitError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RateLimitError::Rejected { retry_after } => {
                write!(f, "Rate limit exceeded. Retry after {:?}", retry_after)
            }
            RateLimitError::InvalidConfig(msg) => {
                write!(f, "Invalid configuration: {}", msg)
            }
        }
    }
}

impl std::error::Error for RateLimitError {}

/// Result type for rate limiting operations
pub type RateLimitResult<T> = Result<T, RateLimitError>;

/// Trait for rate limiters
pub trait RateLimiter {
    /// Try to acquire the specified number of permits
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()>;
    
    /// Get the time until the next permit is available
    fn time_until_available(&self) -> Duration;
    
    /// Get the current number of available permits
    fn available_permits(&self) -> f64;
    
    /// Reset the rate limiter to its initial state
    fn reset(&mut self);
}

/// Token Bucket Rate Limiter
/// 
/// Allows bursts up to the bucket capacity, with tokens refilling at a constant rate.
/// This is ideal for scenarios where you want to allow temporary bursts but maintain
/// an average rate limit.
/// 
/// # Example
/// ```rust
/// use rate_limiter::{TokenBucket, RateLimiter};
/// 
/// let mut bucket = TokenBucket::new(100, 10.0);
/// 
/// // Can burst up to 100 requests
/// assert!(bucket.try_acquire(100).is_ok());
/// 
/// // But will be rejected after that
/// assert!(bucket.try_acquire(1).is_err());
/// ```
#[derive(Debug, Clone)]
pub struct TokenBucket {
    /// Maximum capacity of the bucket
    capacity: f64,
    /// Current number of tokens
    tokens: f64,
    /// Tokens added per second
    refill_rate: f64,
    /// Last time tokens were updated
    last_update: Instant,
}

impl TokenBucket {
    /// Create a new token bucket
    /// 
    /// # Arguments
    /// * `capacity` - Maximum number of tokens the bucket can hold
    /// * `refill_rate` - Number of tokens added per second
    /// 
    /// # Example
    /// ```rust
    /// use rate_limiter::TokenBucket;
    /// 
    /// let bucket = TokenBucket::new(100, 10.0);
    /// ```
    pub fn new(capacity: u32, refill_rate: f64) -> Self {
        Self {
            capacity: capacity as f64,
            tokens: capacity as f64,
            refill_rate,
            last_update: Instant::now(),
        }
    }
    
    /// Create a token bucket that starts empty
    pub fn new_empty(capacity: u32, refill_rate: f64) -> Self {
        Self {
            capacity: capacity as f64,
            tokens: 0.0,
            refill_rate,
            last_update: Instant::now(),
        }
    }
    
    /// Update tokens based on elapsed time
    fn update_tokens(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_update).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.refill_rate).min(self.capacity);
        self.last_update = now;
    }
}

impl RateLimiter for TokenBucket {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        self.update_tokens();
        
        let requested = permits as f64;
        if self.tokens >= requested {
            self.tokens -= requested;
            Ok(())
        } else {
            let deficit = requested - self.tokens;
            let retry_after = Duration::from_secs_f64(deficit / self.refill_rate);
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        if self.tokens >= 1.0 {
            Duration::ZERO
        } else {
            let deficit = 1.0 - self.tokens;
            Duration::from_secs_f64(deficit / self.refill_rate)
        }
    }
    
    fn available_permits(&self) -> f64 {
        self.tokens
    }
    
    fn reset(&mut self) {
        self.tokens = self.capacity;
        self.last_update = Instant::now();
    }
}

/// Leaky Bucket Rate Limiter
/// 
/// Processes requests at a constant rate, smoothing out any bursts.
/// This is ideal for scenarios where you need to maintain a steady flow of requests.
/// 
/// # Example
/// ```rust
/// use rate_limiter::{LeakyBucket, RateLimiter};
/// 
/// let mut bucket = LeakyBucket::new(100, 10.0);
/// 
/// // Requests are processed at a steady rate of 10/sec
/// assert!(bucket.try_acquire(1).is_ok());
/// ```
#[derive(Debug, Clone)]
pub struct LeakyBucket {
    /// Maximum capacity of the bucket
    capacity: f64,
    /// Current water level
    water: f64,
    /// Water drained per second
    drain_rate: f64,
    /// Last time water was drained
    last_drain: Instant,
}

impl LeakyBucket {
    /// Create a new leaky bucket
    /// 
    /// # Arguments
    /// * `capacity` - Maximum number of requests that can be queued
    /// * `drain_rate` - Number of requests processed per second
    pub fn new(capacity: u32, drain_rate: f64) -> Self {
        Self {
            capacity: capacity as f64,
            water: 0.0,
            drain_rate,
            last_drain: Instant::now(),
        }
    }
    
    /// Drain water based on elapsed time
    fn drain(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_drain).as_secs_f64();
        self.water = (self.water - elapsed * self.drain_rate).max(0.0);
        self.last_drain = now;
    }
}

impl RateLimiter for LeakyBucket {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        self.drain();
        
        let requested = permits as f64;
        if self.water + requested <= self.capacity {
            self.water += requested;
            Ok(())
        } else {
            let overflow = self.water + requested - self.capacity;
            let retry_after = Duration::from_secs_f64(overflow / self.drain_rate);
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        if self.water < self.capacity {
            Duration::ZERO
        } else {
            Duration::from_secs_f64(1.0 / self.drain_rate)
        }
    }
    
    fn available_permits(&self) -> f64 {
        (self.capacity - self.water).max(0.0)
    }
    
    fn reset(&mut self) {
        self.water = 0.0;
        self.last_drain = Instant::now();
    }
}

/// Fixed Window Rate Limiter
/// 
/// Divides time into fixed windows and limits requests per window.
/// Simple and memory-efficient, but can allow bursts at window boundaries.
/// 
/// # Example
/// ```rust
/// use rate_limiter::{FixedWindow, RateLimiter};
/// use std::time::Duration;
/// 
/// let mut limiter = FixedWindow::new(100, Duration::from_secs(60));
/// 
/// // Allow up to 100 requests per 60-second window
/// assert!(limiter.try_acquire(1).is_ok());
/// ```
#[derive(Debug, Clone)]
pub struct FixedWindow {
    /// Maximum requests per window
    limit: u32,
    /// Window duration
    window_size: Duration,
    /// Current window start time
    window_start: Instant,
    /// Request count in current window
    count: u32,
}

impl FixedWindow {
    /// Create a new fixed window rate limiter
    /// 
    /// # Arguments
    /// * `limit` - Maximum requests allowed per window
    /// * `window_size` - Duration of each window
    pub fn new(limit: u32, window_size: Duration) -> Self {
        Self {
            limit,
            window_size,
            window_start: Instant::now(),
            count: 0,
        }
    }
    
    /// Check if we need to advance to a new window
    fn advance_window(&mut self) {
        let now = Instant::now();
        if now.duration_since(self.window_start) >= self.window_size {
            self.window_start = now;
            self.count = 0;
        }
    }
}

impl RateLimiter for FixedWindow {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        self.advance_window();
        
        if self.count + permits <= self.limit {
            self.count += permits;
            Ok(())
        } else {
            let elapsed = Instant::now().duration_since(self.window_start);
            let retry_after = self.window_size - elapsed;
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        if self.count < self.limit {
            Duration::ZERO
        } else {
            let elapsed = Instant::now().duration_since(self.window_start);
            self.window_size.saturating_sub(elapsed)
        }
    }
    
    fn available_permits(&self) -> f64 {
        (self.limit - self.count) as f64
    }
    
    fn reset(&mut self) {
        self.window_start = Instant::now();
        self.count = 0;
    }
}

/// Sliding Window Rate Limiter (with logarithmic approximation)
/// 
/// Provides precise rate limiting by tracking recent requests, but uses
/// a memory-efficient approximation by tracking counts in sub-windows.
/// 
/// # Example
/// ```rust
/// use rate_limiter::{SlidingWindow, RateLimiter};
/// use std::time::Duration;
/// 
/// let mut limiter = SlidingWindow::new(100, Duration::from_secs(60));
/// 
/// // Precise rate control without boundary issues
/// assert!(limiter.try_acquire(1).is_ok());
/// ```
#[derive(Debug, Clone)]
pub struct SlidingWindow {
    /// Maximum requests per window
    limit: u32,
    /// Window duration
    window_size: Duration,
    /// Number of sub-windows for tracking
    subdivisions: u32,
    /// Duration of each sub-window
    sub_window_size: Duration,
    /// Request counts per sub-window
    sub_windows: Vec<(Instant, u32)>,
}

impl SlidingWindow {
    /// Create a new sliding window rate limiter
    /// 
    /// # Arguments
    /// * `limit` - Maximum requests allowed per window
    /// * `window_size` - Duration of the sliding window
    pub fn new(limit: u32, window_size: Duration) -> Self {
        Self::with_subdivisions(limit, window_size, 10)
    }
    
    /// Create with custom number of subdivisions
    /// 
    /// More subdivisions = more precise but more memory usage
    pub fn with_subdivisions(limit: u32, window_size: Duration, subdivisions: u32) -> Self {
        let sub_window_size = window_size / subdivisions;
        Self {
            limit,
            window_size,
            subdivisions,
            sub_window_size,
            sub_windows: vec![(Instant::now(), 0); subdivisions as usize],
        }
    }
    
    /// Get current sub-window index
    fn current_sub_window(&self) -> usize {
        let now = Instant::now();
        let elapsed = now.duration_since(self.sub_windows[0].0);
        (elapsed.as_millis() / self.sub_window_size.as_millis()) as usize % self.subdivisions as usize
    }
    
    /// Clean up old sub-windows and get total count
    fn get_total_count(&mut self) -> u32 {
        let now = Instant::now();
        let cutoff = now - self.window_size;
        
        let mut total = 0;
        for (time, count) in &mut self.sub_windows {
            if *time < cutoff {
                *time = now;
                *count = 0;
            }
            total += *count;
        }
        total
    }
}

impl RateLimiter for SlidingWindow {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        let total = self.get_total_count();
        
        if total + permits <= self.limit {
            let idx = self.current_sub_window();
            self.sub_windows[idx].1 += permits;
            Ok(())
        } else {
            // Estimate retry time based on oldest requests
            let retry_after = self.sub_window_size;
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        let total: u32 = self.sub_windows.iter().map(|(_, c)| *c).sum();
        if total < self.limit {
            Duration::ZERO
        } else {
            self.sub_window_size
        }
    }
    
    fn available_permits(&self) -> f64 {
        let total: u32 = self.sub_windows.iter().map(|(_, c)| *c).sum();
        (self.limit - total) as f64
    }
    
    fn reset(&mut self) {
        let now = Instant::now();
        for entry in &mut self.sub_windows {
            *entry = (now, 0);
        }
    }
}

/// Sliding Log Rate Limiter (exact, but higher memory usage)
/// 
/// Tracks exact timestamps of requests for precise rate limiting.
/// Best for scenarios where accuracy is critical and request volume is moderate.
/// 
/// # Example
/// ```rust
/// use rate_limiter::{SlidingLog, RateLimiter};
/// use std::time::Duration;
/// 
/// let mut limiter = SlidingLog::new(100, Duration::from_secs(60));
/// 
/// // Exact tracking of request timestamps
/// assert!(limiter.try_acquire(1).is_ok());
/// ```
#[derive(Debug, Clone)]
pub struct SlidingLog {
    /// Maximum requests per window
    limit: u32,
    /// Window duration
    window_size: Duration,
    /// Timestamps of requests in the current window
    timestamps: Vec<Instant>,
}

impl SlidingLog {
    /// Create a new sliding log rate limiter
    pub fn new(limit: u32, window_size: Duration) -> Self {
        Self {
            limit,
            window_size,
            timestamps: Vec::with_capacity(limit as usize),
        }
    }
    
    /// Clean up old timestamps and return current count
    fn cleanup(&mut self) -> usize {
        let cutoff = Instant::now() - self.window_size;
        self.timestamps.retain(|&ts| ts > cutoff);
        self.timestamps.len()
    }
}

impl RateLimiter for SlidingLog {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        let current_count = self.cleanup();
        
        if current_count + permits as usize <= self.limit as usize {
            let now = Instant::now();
            for _ in 0..permits {
                self.timestamps.push(now);
            }
            Ok(())
        } else {
            // Find the oldest timestamp that would allow this request
            let retry_after = if self.timestamps.is_empty() {
                self.window_size
            } else {
                let now = Instant::now();
                let cutoff = now - self.window_size;
                let oldest_in_window = self.timestamps.iter()
                    .filter(|&&ts| ts > cutoff)
                    .min()
                    .unwrap_or(&now);
                
                oldest_in_window.duration_since(now - self.window_size)
            };
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        let cutoff = Instant::now() - self.window_size;
        let count = self.timestamps.iter().filter(|&&ts| ts > cutoff).count();
        
        if count < self.limit as usize {
            Duration::ZERO
        } else {
            // Find the oldest timestamp in window
            let now = Instant::now();
            self.timestamps.iter()
                .filter(|&&ts| ts > now - self.window_size)
                .min()
                .map(|&ts| ts.duration_since(now - self.window_size))
                .unwrap_or(Duration::ZERO)
        }
    }
    
    fn available_permits(&self) -> f64 {
        let cutoff = Instant::now() - self.window_size;
        let count = self.timestamps.iter().filter(|&&ts| ts > cutoff).count();
        (self.limit as usize - count) as f64
    }
    
    fn reset(&mut self) {
        self.timestamps.clear();
    }
}

/// Adaptive Rate Limiter
/// 
/// Automatically adjusts rate limit based on success/failure patterns.
/// Useful for distributed systems where backpressure is needed.
/// 
/// # Example
/// ```rust
/// use rate_limiter::AdaptiveLimiter;
/// 
/// let mut limiter = AdaptiveLimiter::new(100, 0.5);
/// 
/// limiter.on_success();  // Gradually increases limit
/// limiter.on_failure();  // Decreases limit
/// ```
#[derive(Debug, Clone)]
pub struct AdaptiveLimiter {
    /// Current rate limit
    current_limit: f64,
    /// Minimum rate limit
    min_limit: f64,
    /// Maximum rate limit
    max_limit: f64,
    /// Factor to increase limit on success
    increase_factor: f64,
    /// Factor to decrease limit on failure
    decrease_factor: f64,
    /// Current request count in window
    count: u32,
    /// Window start time
    window_start: Instant,
    /// Window duration
    window_size: Duration,
}

impl AdaptiveLimiter {
    /// Create a new adaptive rate limiter
    /// 
    /// # Arguments
    /// * `initial_limit` - Starting rate limit
    /// * `adjustment_factor` - How much to adjust (0.0-1.0), higher = more aggressive
    pub fn new(initial_limit: u32, adjustment_factor: f64) -> Self {
        let limit = initial_limit as f64;
        Self {
            current_limit: limit,
            min_limit: limit * 0.1,
            max_limit: limit * 10.0,
            increase_factor: 1.0 + adjustment_factor,
            decrease_factor: 1.0 - adjustment_factor,
            count: 0,
            window_start: Instant::now(),
            window_size: Duration::from_secs(1),
        }
    }
    
    /// Set min/max bounds
    pub fn with_bounds(mut self, min: u32, max: u32) -> Self {
        self.min_limit = min as f64;
        self.max_limit = max as f64;
        self
    }
    
    /// Record a successful request
    pub fn on_success(&mut self) {
        self.current_limit = (self.current_limit * self.increase_factor).min(self.max_limit);
    }
    
    /// Record a failed request (rate limited or error)
    pub fn on_failure(&mut self) {
        self.current_limit = (self.current_limit * self.decrease_factor).max(self.min_limit);
    }
    
    /// Get current rate limit
    pub fn current_limit(&self) -> u32 {
        self.current_limit as u32
    }
    
    /// Reset to initial state
    pub fn reset_limit(&mut self) {
        self.current_limit = self.max_limit / 10.0;
    }
}

impl RateLimiter for AdaptiveLimiter {
    fn try_acquire(&mut self, permits: u32) -> RateLimitResult<()> {
        let now = Instant::now();
        if now.duration_since(self.window_start) >= self.window_size {
            self.window_start = now;
            self.count = 0;
        }
        
        let limit = self.current_limit as u32;
        if self.count + permits <= limit {
            self.count += permits;
            Ok(())
        } else {
            let retry_after = self.window_size - now.duration_since(self.window_start);
            Err(RateLimitError::Rejected { retry_after })
        }
    }
    
    fn time_until_available(&self) -> Duration {
        if self.count < self.current_limit as u32 {
            Duration::ZERO
        } else {
            let elapsed = Instant::now().duration_since(self.window_start);
            self.window_size.saturating_sub(elapsed)
        }
    }
    
    fn available_permits(&self) -> f64 {
        let limit = self.current_limit as u32;
        (limit - self.count) as f64
    }
    
    fn reset(&mut self) {
        self.count = 0;
        self.window_start = Instant::now();
        self.reset_limit();
    }
}

/// Concurrency Limiter
/// 
/// Limits the number of concurrent operations (not rate per second).
/// Use this to control resource usage, not request rate.
/// 
/// # Example
/// ```rust
/// use rate_limiter::ConcurrencyLimiter;
/// 
/// let limiter = ConcurrencyLimiter::new(10);
/// 
/// let permit = limiter.try_acquire();
/// assert!(permit.is_ok());
/// 
/// // Drop the permit to release
/// drop(permit);
/// ```
#[derive(Debug)]
pub struct ConcurrencyLimiter {
    /// Maximum concurrent operations
    max_concurrent: u32,
    /// Current count
    current: std::sync::atomic::AtomicU32,
}

impl ConcurrencyLimiter {
    /// Create a new concurrency limiter
    pub fn new(max_concurrent: u32) -> Self {
        Self {
            max_concurrent,
            current: std::sync::atomic::AtomicU32::new(0),
        }
    }
    
    /// Try to acquire a concurrency permit
    pub fn try_acquire(&self) -> RateLimitResult<ConcurrencyPermit<'_>> {
        use std::sync::atomic::Ordering;
        
        let current = self.current.fetch_add(1, Ordering::Relaxed);
        if current < self.max_concurrent {
            Ok(ConcurrencyPermit {
                counter: &self.current,
            })
        } else {
            self.current.fetch_sub(1, Ordering::Relaxed);
            Err(RateLimitError::Rejected {
                retry_after: Duration::from_millis(100),
            })
        }
    }
    
    /// Get current concurrent count
    pub fn current(&self) -> u32 {
        use std::sync::atomic::Ordering;
        self.current.load(Ordering::Relaxed)
    }
    
    /// Get max concurrent
    pub fn max(&self) -> u32 {
        self.max_concurrent
    }
}

/// A permit for concurrent operation
#[derive(Debug)]
pub struct ConcurrencyPermit<'a> {
    counter: &'a std::sync::atomic::AtomicU32,
}

impl Drop for ConcurrencyPermit<'_> {
    fn drop(&mut self) {
        use std::sync::atomic::Ordering;
        self.counter.fetch_sub(1, Ordering::Relaxed);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    use std::sync::Arc;
    use std::sync::atomic::{AtomicU32, Ordering};

    #[test]
    fn test_token_bucket_basic() {
        let mut bucket = TokenBucket::new(10, 1.0);
        
        // Should be able to acquire up to capacity
        assert!(bucket.try_acquire(10).is_ok());
        
        // Should fail after capacity exhausted
        assert!(bucket.try_acquire(1).is_err());
    }

    #[test]
    fn test_token_bucket_refill() {
        let mut bucket = TokenBucket::new(10, 10.0); // 10 tokens/sec
        
        // Use 5 tokens
        assert!(bucket.try_acquire(5).is_ok());
        
        // Wait 0.5 seconds (should refill 5 tokens)
        thread::sleep(Duration::from_millis(550));
        
        // Should have 5 + 5 = 10 tokens available
        assert!(bucket.try_acquire(5).is_ok());
    }

    #[test]
    fn test_leaky_bucket_basic() {
        let mut bucket = LeakyBucket::new(10, 1.0);
        
        // Should be able to add up to capacity
        assert!(bucket.try_acquire(10).is_ok());
        
        // Should fail when full
        assert!(bucket.try_acquire(1).is_err());
    }

    #[test]
    fn test_fixed_window_basic() {
        let mut window = FixedWindow::new(10, Duration::from_secs(60));
        
        // Should allow up to limit
        assert!(window.try_acquire(10).is_ok());
        
        // Should fail after limit
        assert!(window.try_acquire(1).is_err());
    }

    #[test]
    fn test_sliding_window_basic() {
        let mut window = SlidingWindow::new(10, Duration::from_secs(60));
        
        // Should allow up to limit
        assert!(window.try_acquire(10).is_ok());
        
        // Should fail after limit
        assert!(window.try_acquire(1).is_err());
    }

    #[test]
    fn test_sliding_log_basic() {
        let mut log = SlidingLog::new(10, Duration::from_secs(60));
        
        // Should allow up to limit
        assert!(log.try_acquire(10).is_ok());
        
        // Should fail after limit
        assert!(log.try_acquire(1).is_err());
    }

    #[test]
    fn test_adaptive_limiter() {
        let mut limiter = AdaptiveLimiter::new(100, 0.5);
        
        assert_eq!(limiter.current_limit(), 100);
        
        // Success should increase limit
        limiter.on_success();
        assert!(limiter.current_limit() > 100);
        
        // Failure should decrease limit
        limiter.on_failure();
        limiter.on_failure();
        limiter.on_failure();
        assert!(limiter.current_limit() < 200);
    }

    #[test]
    fn test_concurrency_limiter() {
        let limiter = Arc::new(ConcurrencyLimiter::new(3));
        let success_count = Arc::new(AtomicU32::new(0));
        
        let handles: Vec<_> = (0..5)
            .map(|_| {
                let limiter = Arc::clone(&limiter);
                let success_count = Arc::clone(&success_count);
                thread::spawn(move || {
                    if let Ok(_permit) = limiter.try_acquire() {
                        success_count.fetch_add(1, Ordering::Relaxed);
                        thread::sleep(Duration::from_millis(50));
                    }
                })
            })
            .collect();
        
        for handle in handles {
            handle.join().unwrap();
        }
        
        // Only 3 should have succeeded
        assert_eq!(success_count.load(Ordering::Relaxed), 3);
    }

    #[test]
    fn test_rate_limiter_reset() {
        let mut bucket = TokenBucket::new(10, 1.0);
        assert!(bucket.try_acquire(10).is_ok());
        bucket.reset();
        assert!(bucket.try_acquire(10).is_ok());
    }

    #[test]
    fn test_available_permits() {
        let mut bucket = TokenBucket::new(100, 1.0);
        assert_eq!(bucket.available_permits(), 100.0);
        
        assert!(bucket.try_acquire(30).is_ok());
        assert_eq!(bucket.available_permits(), 70.0);
    }
}