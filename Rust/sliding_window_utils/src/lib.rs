//! # Sliding Window Utils
//!
//! A comprehensive sliding window implementation for Rust.
//! 
//! Features:
//! - Time-based sliding window (for rate limiting, metrics)
//! - Count-based sliding window (fixed size, moving window)
//! - Weighted sliding window (for weighted moving averages)
//! - Zero external dependencies - pure Rust stdlib

use std::collections::VecDeque;
use std::time::{Duration, Instant};

/// A time-based sliding window for tracking events within a time period.
/// 
/// Useful for rate limiting, metrics collection, and time-series analysis.
/// 
/// # Example
/// 
/// ```
/// use sliding_window_utils::TimeWindow;
/// use std::time::Duration;
/// 
/// let mut window = TimeWindow::new(Duration::from_secs(60));
/// window.record(1);
/// window.record(2);
/// assert!(window.count() >= 2);
/// ```
#[derive(Debug)]
pub struct TimeWindow<T> {
    /// The duration of the window
    duration: Duration,
    /// Events stored with their timestamps
    events: VecDeque<(Instant, T)>,
    /// Maximum capacity (0 means unlimited)
    max_capacity: usize,
}

impl<T: Clone> TimeWindow<T> {
    /// Creates a new time-based sliding window with the given duration.
    /// 
    /// # Arguments
    /// 
    /// * `duration` - The time window duration
    /// 
    /// # Example
    /// 
    /// ```
    /// use sliding_window_utils::TimeWindow;
    /// use std::time::Duration;
    /// 
    /// let window: TimeWindow<i32> = TimeWindow::new(Duration::from_secs(60));
    /// ```
    pub fn new(duration: Duration) -> Self {
        Self {
            duration,
            events: VecDeque::new(),
            max_capacity: 0,
        }
    }

    /// Creates a new time-based sliding window with a maximum capacity.
    /// 
    /// # Arguments
    /// 
    /// * `duration` - The time window duration
    /// * `max_capacity` - Maximum number of events to store (0 = unlimited)
    pub fn with_capacity(duration: Duration, max_capacity: usize) -> Self {
        Self {
            duration,
            events: VecDeque::new(),
            max_capacity,
        }
    }

    /// Records an event in the window.
    /// 
    /// # Arguments
    /// 
    /// * `value` - The value to record
    /// 
    /// # Example
    /// 
    /// ```
    /// use sliding_window_utils::TimeWindow;
    /// use std::time::Duration;
    /// 
    /// let mut window = TimeWindow::new(Duration::from_secs(60));
    /// window.record(42);
    /// ```
    pub fn record(&mut self, value: T) {
        self.cleanup();
        if self.max_capacity > 0 && self.events.len() >= self.max_capacity {
            self.events.pop_front();
        }
        self.events.push_back((Instant::now(), value));
    }

    /// Removes expired events from the window.
    fn cleanup(&mut self) {
        let now = Instant::now();
        while let Some(front) = self.events.front() {
            if now.duration_since(front.0) > self.duration {
                self.events.pop_front();
            } else {
                break;
            }
        }
    }

    /// Returns the number of events in the current window.
    pub fn count(&mut self) -> usize {
        self.cleanup();
        self.events.len()
    }

    /// Returns true if the window is empty.
    pub fn is_empty(&mut self) -> bool {
        self.cleanup();
        self.events.is_empty()
    }

    /// Returns all values in the current window.
    pub fn values(&mut self) -> Vec<T> {
        self.cleanup();
        self.events.iter().map(|(_, v)| v.clone()).collect()
    }

    /// Returns all events with their timestamps in the current window.
    pub fn events(&mut self) -> Vec<(Instant, T)> {
        self.cleanup();
        self.events.iter().map(|(t, v)| (*t, v.clone())).collect()
    }

    /// Clears all events from the window.
    pub fn clear(&mut self) {
        self.events.clear();
    }

    /// Returns the duration of the window.
    pub fn duration(&self) -> Duration {
        self.duration
    }
}

impl TimeWindow<i64> {
    /// Returns the sum of all values in the window.
    pub fn sum(&mut self) -> i64 {
        self.cleanup();
        self.events.iter().map(|(_, v)| v).sum()
    }

    /// Returns the average of all values in the window.
    /// Returns None if the window is empty.
    pub fn average(&mut self) -> Option<f64> {
        self.cleanup();
        if self.events.is_empty() {
            return None;
        }
        let sum: i64 = self.events.iter().map(|(_, v)| v).sum();
        Some(sum as f64 / self.events.len() as f64)
    }
}

impl TimeWindow<f64> {
    /// Returns the sum of all values in the window.
    pub fn sum(&mut self) -> f64 {
        self.cleanup();
        self.events.iter().map(|(_, v)| v).sum()
    }

    /// Returns the average of all values in the window.
    /// Returns None if the window is empty.
    pub fn average(&mut self) -> Option<f64> {
        self.cleanup();
        if self.events.is_empty() {
            return None;
        }
        let sum: f64 = self.events.iter().map(|(_, v)| v).sum();
        Some(sum / self.events.len() as f64)
    }
}

/// A count-based sliding window with fixed size.
/// 
/// Useful for moving averages, data stream processing, and fixed-size buffers.
/// 
/// # Example
/// 
/// ```
/// use sliding_window_utils::CountWindow;
/// 
/// let mut window = CountWindow::new(5);
/// for i in 1..=10 {
///     window.push(i);
/// }
/// assert_eq!(window.values(), vec![6, 7, 8, 9, 10]);
/// ```
#[derive(Debug, Clone)]
pub struct CountWindow<T> {
    /// The fixed size of the window
    size: usize,
    /// Events in the window
    events: VecDeque<T>,
}

impl<T: Clone> CountWindow<T> {
    /// Creates a new count-based sliding window with the given size.
    /// 
    /// # Arguments
    /// 
    /// * `size` - The maximum number of elements in the window
    /// 
    /// # Panics
    /// 
    /// Panics if size is 0.
    /// 
    /// # Example
    /// 
    /// ```
    /// use sliding_window_utils::CountWindow;
    /// 
    /// let window: CountWindow<i32> = CountWindow::new(10);
    /// ```
    pub fn new(size: usize) -> Self {
        assert!(size > 0, "Window size must be greater than 0");
        Self {
            size,
            events: VecDeque::with_capacity(size),
        }
    }

    /// Pushes a new value into the window.
    /// If the window is full, the oldest value is removed.
    /// 
    /// # Returns
    /// 
    /// The evicted value, if any.
    /// 
    /// # Example
    /// 
    /// ```
    /// use sliding_window_utils::CountWindow;
    /// 
    /// let mut window = CountWindow::new(2);
    /// assert_eq!(window.push(1), None);
    /// assert_eq!(window.push(2), None);
    /// assert_eq!(window.push(3), Some(1));
    /// ```
    pub fn push(&mut self, value: T) -> Option<T> {
        let evicted = if self.events.len() >= self.size {
            self.events.pop_front()
        } else {
            None
        };
        self.events.push_back(value);
        evicted
    }

    /// Returns the number of elements in the window.
    pub fn len(&self) -> usize {
        self.events.len()
    }

    /// Returns true if the window is empty.
    pub fn is_empty(&self) -> bool {
        self.events.is_empty()
    }

    /// Returns true if the window is full.
    pub fn is_full(&self) -> bool {
        self.events.len() == self.size
    }

    /// Returns the size of the window.
    pub fn size(&self) -> usize {
        self.size
    }

    /// Returns all values in the window.
    pub fn values(&self) -> Vec<T> {
        self.events.iter().cloned().collect()
    }

    /// Clears all values from the window.
    pub fn clear(&mut self) {
        self.events.clear();
    }

    /// Returns the oldest value in the window.
    pub fn oldest(&self) -> Option<&T> {
        self.events.front()
    }

    /// Returns the newest value in the window.
    pub fn newest(&self) -> Option<&T> {
        self.events.back()
    }

    /// Returns an iterator over the values in the window.
    pub fn iter(&self) -> impl Iterator<Item = &T> {
        self.events.iter()
    }
}

impl<T: Clone + Default> CountWindow<T> {
    /// Creates a new window pre-filled with default values.
    pub fn filled(size: usize) -> Self {
        let mut events = VecDeque::with_capacity(size);
        for _ in 0..size {
            events.push_back(T::default());
        }
        Self { size, events }
    }
}

impl CountWindow<i64> {
    /// Returns the sum of all values in the window.
    pub fn sum(&self) -> i64 {
        self.events.iter().sum()
    }

    /// Returns the average of all values in the window.
    /// Returns 0.0 if the window is empty.
    pub fn average(&self) -> f64 {
        if self.events.is_empty() {
            return 0.0;
        }
        self.sum() as f64 / self.events.len() as f64
    }

    /// Returns the minimum value in the window.
    /// Returns None if the window is empty.
    pub fn min(&self) -> Option<i64> {
        self.events.iter().copied().min()
    }

    /// Returns the maximum value in the window.
    /// Returns None if the window is empty.
    pub fn max(&self) -> Option<i64> {
        self.events.iter().copied().max()
    }
}

impl CountWindow<f64> {
    /// Returns the sum of all values in the window.
    pub fn sum(&self) -> f64 {
        self.events.iter().sum()
    }

    /// Returns the average of all values in the window.
    /// Returns 0.0 if the window is empty.
    pub fn average(&self) -> f64 {
        if self.events.is_empty() {
            return 0.0;
        }
        self.sum() / self.events.len() as f64
    }

    /// Returns the minimum value in the window.
    /// Returns None if the window is empty.
    pub fn min(&self) -> Option<f64> {
        self.events.iter().copied().fold(None, |acc, x| {
            Some(acc.map_or(x, |a: f64| a.min(x)))
        })
    }

    /// Returns the maximum value in the window.
    /// Returns None if the window is empty.
    pub fn max(&self) -> Option<f64> {
        self.events.iter().copied().fold(None, |acc, x| {
            Some(acc.map_or(x, |a: f64| a.max(x)))
        })
    }

    /// Returns the standard deviation of values in the window.
    /// Returns None if the window has fewer than 2 elements.
    pub fn std_dev(&self) -> Option<f64> {
        if self.events.len() < 2 {
            return None;
        }
        let mean = self.average();
        let variance: f64 = self.events.iter()
            .map(|x| (x - mean).powi(2))
            .sum::<f64>() / self.events.len() as f64;
        Some(variance.sqrt())
    }
}

/// A weighted sliding window for calculating weighted moving averages.
/// 
/// More recent values have higher weights, useful for trend analysis.
/// 
/// # Example
/// 
/// ```
/// use sliding_window_utils::WeightedWindow;
/// 
/// let mut window = WeightedWindow::new(3);
/// window.push(10.0);
/// window.push(20.0);
/// window.push(30.0);
/// // Weighted average: (10*1 + 20*2 + 30*3) / (1+2+3) = 23.33
/// let avg = window.weighted_average();
/// assert!(avg > 23.0 && avg < 24.0);
/// ```
#[derive(Debug, Clone)]
pub struct WeightedWindow {
    /// The fixed size of the window
    size: usize,
    /// Values in the window
    values: VecDeque<f64>,
    /// Weight function: weight = f(position, size)
    /// Position is 0-based, where 0 is the oldest
    weight_fn: fn(usize, usize) -> f64,
}

impl WeightedWindow {
    /// Creates a new weighted window with linear weights (1, 2, 3, ..., n).
    /// 
    /// # Panics
    /// 
    /// Panics if size is 0.
    pub fn new(size: usize) -> Self {
        assert!(size > 0, "Window size must be greater than 0");
        Self {
            size,
            values: VecDeque::with_capacity(size),
            weight_fn: linear_weight,
        }
    }

    /// Creates a weighted window with exponential weights.
    /// Each weight is double the previous (1, 2, 4, 8, ...).
    pub fn exponential(size: usize) -> Self {
        assert!(size > 0, "Window size must be greater than 0");
        Self {
            size,
            values: VecDeque::with_capacity(size),
            weight_fn: exponential_weight,
        }
    }

    /// Creates a weighted window with custom weight function.
    pub fn with_weight_fn(size: usize, weight_fn: fn(usize, usize) -> f64) -> Self {
        assert!(size > 0, "Window size must be greater than 0");
        Self {
            size,
            values: VecDeque::with_capacity(size),
            weight_fn,
        }
    }

    /// Pushes a new value into the window.
    /// Returns the evicted value, if any.
    pub fn push(&mut self, value: f64) -> Option<f64> {
        let evicted = if self.values.len() >= self.size {
            self.values.pop_front()
        } else {
            None
        };
        self.values.push_back(value);
        evicted
    }

    /// Returns the weighted average of all values.
    /// Returns 0.0 if the window is empty.
    pub fn weighted_average(&self) -> f64 {
        if self.values.is_empty() {
            return 0.0;
        }

        let current_size = self.values.len();
        let mut weighted_sum = 0.0;
        let mut total_weight = 0.0;

        for (i, &value) in self.values.iter().enumerate() {
            let weight = (self.weight_fn)(i, current_size);
            weighted_sum += value * weight;
            total_weight += weight;
        }

        if total_weight == 0.0 {
            0.0
        } else {
            weighted_sum / total_weight
        }
    }

    /// Returns the number of elements in the window.
    pub fn len(&self) -> usize {
        self.values.len()
    }

    /// Returns true if the window is empty.
    pub fn is_empty(&self) -> bool {
        self.values.is_empty()
    }

    /// Returns true if the window is full.
    pub fn is_full(&self) -> bool {
        self.values.len() == self.size
    }

    /// Returns all values in the window.
    pub fn values(&self) -> Vec<f64> {
        self.values.iter().copied().collect()
    }

    /// Clears all values from the window.
    pub fn clear(&mut self) {
        self.values.clear();
    }
}

/// Linear weight function: weight = position + 1
fn linear_weight(position: usize, _size: usize) -> f64 {
    (position + 1) as f64
}

/// Exponential weight function: weight = 2^position
fn exponential_weight(position: usize, _size: usize) -> f64 {
    2_f64.powi(position as i32)
}

/// A rate limiter using sliding window algorithm.
/// 
/// Allows a maximum number of requests within a time window.
/// 
/// # Example
/// 
/// ```
/// use sliding_window_utils::RateLimiter;
/// use std::time::Duration;
/// 
/// let mut limiter = RateLimiter::new(5, Duration::from_secs(60));
/// 
/// // Allow 5 requests
/// for _ in 0..5 {
///     assert!(limiter.allow());
/// }
/// // 6th request is denied (within the same second)
/// assert!(!limiter.allow());
/// ```
#[derive(Debug)]
pub struct RateLimiter {
    max_requests: usize,
    window: TimeWindow<()>,
}

impl RateLimiter {
    /// Creates a new rate limiter.
    /// 
    /// # Arguments
    /// 
    /// * `max_requests` - Maximum requests allowed in the window
    /// * `duration` - The time window duration
    pub fn new(max_requests: usize, duration: Duration) -> Self {
        Self {
            max_requests,
            window: TimeWindow::new(duration),
        }
    }

    /// Attempts to make a request.
    /// 
    /// # Returns
    /// 
    /// `true` if the request is allowed, `false` if rate limit is exceeded.
    pub fn allow(&mut self) -> bool {
        self.window.count() < self.max_requests && {
            self.window.record(());
            true
        }
    }

    /// Checks if a request would be allowed without recording it.
    pub fn check(&mut self) -> bool {
        self.window.count() < self.max_requests
    }

    /// Returns the current count of requests in the window.
    pub fn current_count(&mut self) -> usize {
        self.window.count()
    }

    /// Returns the number of remaining requests allowed.
    pub fn remaining(&mut self) -> usize {
        self.max_requests.saturating_sub(self.window.count())
    }

    /// Resets the rate limiter.
    pub fn reset(&mut self) {
        self.window.clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_window_basic() {
        let mut window = CountWindow::new(3);
        
        window.push(1);
        window.push(2);
        window.push(3);
        
        assert_eq!(window.values(), vec![1, 2, 3]);
        assert!(window.is_full());
        
        window.push(4);
        assert_eq!(window.values(), vec![2, 3, 4]);
    }

    #[test]
    fn test_count_window_sum_average() {
        let mut window = CountWindow::<i64>::new(5);
        
        for i in 1..=5 {
            window.push(i);
        }
        
        assert_eq!(window.sum(), 15);
        assert_eq!(window.average(), 3.0);
        assert_eq!(window.min(), Some(1));
        assert_eq!(window.max(), Some(5));
    }

    #[test]
    fn test_count_window_f64() {
        let mut window = CountWindow::<f64>::new(3);
        
        window.push(1.5);
        window.push(2.5);
        window.push(3.5);
        
        assert!((window.sum() - 7.5).abs() < 0.001);
        assert!((window.average() - 2.5).abs() < 0.001);
        assert!((window.min().unwrap() - 1.5).abs() < 0.001);
        assert!((window.max().unwrap() - 3.5).abs() < 0.001);
    }

    #[test]
    fn test_weighted_window_linear() {
        let mut window = WeightedWindow::new(3);
        
        window.push(10.0);
        window.push(20.0);
        window.push(30.0);
        
        // Linear weights: 1, 2, 3
        // Weighted avg: (10*1 + 20*2 + 30*3) / 6 = 140/6 ≈ 23.33
        let avg = window.weighted_average();
        assert!(avg > 23.0 && avg < 24.0);
    }

    #[test]
    fn test_weighted_window_exponential() {
        let mut window = WeightedWindow::exponential(3);
        
        window.push(10.0);
        window.push(20.0);
        window.push(30.0);
        
        // Exponential weights: 1, 2, 4
        // Weighted avg: (10*1 + 20*2 + 30*4) / 7 = 170/7 ≈ 24.29
        let avg = window.weighted_average();
        assert!(avg > 24.0 && avg < 25.0);
    }

    #[test]
    fn test_rate_limiter() {
        let mut limiter = RateLimiter::new(3, Duration::from_secs(60));
        
        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(!limiter.allow()); // Exceeded
        
        assert_eq!(limiter.remaining(), 0);
    }

    #[test]
    fn test_rate_limiter_check() {
        let mut limiter = RateLimiter::new(2, Duration::from_secs(60));
        
        assert!(limiter.check());
        assert!(limiter.allow());
        assert!(limiter.check());
        assert!(limiter.allow());
        assert!(!limiter.check());
        assert!(!limiter.allow());
    }

    #[test]
    fn test_count_window_evict() {
        let mut window = CountWindow::new(2);
        
        assert_eq!(window.push(1), None);
        assert_eq!(window.push(2), None);
        assert_eq!(window.push(3), Some(1));
        assert_eq!(window.values(), vec![2, 3]);
    }

    #[test]
    fn test_empty_window() {
        let window: CountWindow<i64> = CountWindow::new(5);
        
        assert!(window.is_empty());
        assert!(!window.is_full());
        assert_eq!(window.sum(), 0);
        assert_eq!(window.average(), 0.0);
        assert_eq!(window.min(), None);
        assert_eq!(window.max(), None);
    }

    #[test]
    fn test_std_dev() {
        let mut window = CountWindow::<f64>::new(3);
        
        window.push(2.0);
        window.push(4.0);
        window.push(4.0);
        window.push(4.0);
        window.push(5.0);
        window.push(5.0);
        window.push(7.0);
        window.push(9.0);
        
        // Values: [5, 7, 9]
        // Mean: 7
        // Std dev: sqrt(((5-7)^2 + (7-7)^2 + (9-7)^2) / 3) = sqrt(8/3) ≈ 1.633
        let std_dev = window.std_dev().unwrap();
        assert!(std_dev > 1.6 && std_dev < 1.7);
    }
}