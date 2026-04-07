//! Benchmark Utilities for Rust
//!
//! A comprehensive performance testing and benchmarking utility module for Rust
//! providing timing, throughput measurement, statistical analysis, and comparison tools.
//!
//! # Features
//! - Simple timing of code blocks
//! - Statistical analysis (mean, median, std dev, percentiles)
//! - Throughput measurement (ops/sec)
//! - Multiple iterations with warmup
//! - Comparison between multiple implementations
//!
//! # Example
//! ```rust
//! use benchmark_utils::Benchmark;
//!
//! let bench = Benchmark::new("sum").iterations(1000);
//! let result = bench.run(|| {
//!     let sum: u64 = (0..100).sum();
//!     sum
//! });
//!
//! println!("{}", result);
//! ```

use std::fmt;
use std::time::{Duration, Instant};

/// A benchmark configuration and runner
pub struct Benchmark {
    name: String,
    iterations: usize,
    warmup: usize,
}

/// Statistical results from a benchmark run
#[derive(Debug, Clone)]
pub struct BenchmarkResult {
    /// Name of the benchmark
    pub name: String,
    /// Number of iterations run
    pub iteration_count: usize,
    /// Total duration of all iterations
    pub total_duration: Duration,
    /// Individual timings (stored for percentile calculation)
    timings: Vec<Duration>,
}

/// Statistics calculated from benchmark results
#[derive(Debug, Clone, Copy)]
pub struct Statistics {
    /// Mean (average) duration
    pub mean: Duration,
    /// Median duration
    pub median: Duration,
    /// Minimum duration
    pub min: Duration,
    /// Maximum duration
    pub max: Duration,
    /// Standard deviation in nanoseconds
    pub std_dev_ns: f64,
    /// 95th percentile
    pub p95: Duration,
    /// 99th percentile
    pub p99: Duration,
    /// Operations per second
    pub ops_per_sec: f64,
    /// Average nanoseconds per operation
    pub ns_per_op: f64,
}

/// A comparison between two benchmark results
#[derive(Debug, Clone)]
pub struct Comparison {
    /// Name of the baseline benchmark
    pub baseline_name: String,
    /// Name of the candidate benchmark
    pub candidate_name: String,
    /// Speedup factor (baseline / candidate)
    pub speedup: f64,
    /// Percentage improvement
    pub improvement_pct: f64,
    /// Whether candidate is faster
    pub is_faster: bool,
}

/// Simple timer for measuring code execution time
pub struct Timer {
    start: Instant,
    laps: Vec<Duration>,
}

impl Benchmark {
    /// Create a new benchmark with the given name
    ///
    /// # Example
    /// ```
    /// use benchmark_utils::Benchmark;
    ///
    /// let bench = Benchmark::new("vector_push");
    /// ```
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            iterations: 100,
            warmup: 10,
        }
    }

    /// Set the number of iterations to run
    pub fn iterations(mut self, count: usize) -> Self {
        self.iterations = count;
        self
    }

    /// Set the number of warmup iterations
    pub fn warmup(mut self, count: usize) -> Self {
        self.warmup = count;
        self
    }

    /// Run the benchmark with the given function
    ///
    /// # Example
    /// ```
    /// use benchmark_utils::Benchmark;
    ///
    /// let bench = Benchmark::new("sum").iterations(1000);
    /// let result = bench.run(|| {
    ///     let sum: u64 = (0..100).sum();
    ///     sum
    /// });
    /// ```
    pub fn run<F, R>(self, mut f: F) -> BenchmarkResult
    where
        F: FnMut() -> R,
    {
        // Warmup phase
        for _ in 0..self.warmup {
            let _ = f();
        }

        let mut timings = Vec::with_capacity(self.iterations);
        let start = Instant::now();

        // Main benchmark loop
        for _ in 0..self.iterations {
            let iter_start = Instant::now();
            let _ = f();
            let duration = iter_start.elapsed();
            timings.push(duration);
        }

        BenchmarkResult {
            name: self.name,
            iteration_count: self.iterations,
            total_duration: start.elapsed(),
            timings,
        }
    }
}

impl BenchmarkResult {
    /// Calculate statistics from the benchmark results
    pub fn statistics(&self) -> Statistics {
        if self.timings.is_empty() {
            return Statistics {
                mean: Duration::ZERO,
                median: Duration::ZERO,
                min: Duration::ZERO,
                max: Duration::ZERO,
                std_dev_ns: 0.0,
                p95: Duration::ZERO,
                p99: Duration::ZERO,
                ops_per_sec: 0.0,
                ns_per_op: 0.0,
            };
        }

        let mut sorted = self.timings.clone();
        sorted.sort();

        let len = sorted.len();
        let min = sorted[0];
        let max = sorted[len - 1];

        // Calculate mean
        let total_ns: u128 = sorted.iter().map(|d| d.as_nanos()).sum();
        let mean_ns = total_ns as f64 / len as f64;
        let mean = Duration::from_nanos(mean_ns as u64);

        // Calculate median
        let median = if len % 2 == 0 {
            let mid1 = sorted[len / 2 - 1].as_nanos();
            let mid2 = sorted[len / 2].as_nanos();
            Duration::from_nanos(((mid1 + mid2) / 2) as u64)
        } else {
            sorted[len / 2]
        };

        // Calculate standard deviation
        let variance: f64 = sorted
            .iter()
            .map(|d| {
                let diff = d.as_nanos() as f64 - mean_ns;
                diff * diff
            })
            .sum::<f64>() / len as f64;
        let std_dev_ns = variance.sqrt();

        // Calculate percentiles
        let p95_idx = ((len as f64) * 0.95) as usize;
        let p99_idx = ((len as f64) * 0.99) as usize;
        let p95 = sorted[p95_idx.min(len - 1)];
        let p99 = sorted[p99_idx.min(len - 1)];

        // Calculate ops/sec
        let ops_per_sec = if mean_ns > 0.0 {
            1_000_000_000.0 / mean_ns
        } else {
            0.0
        };

        Statistics {
            mean,
            median,
            min,
            max,
            std_dev_ns,
            p95,
            p99,
            ops_per_sec,
            ns_per_op: mean_ns,
        }
    }

    /// Compare this result with another benchmark result
    pub fn compare(&self, other: &BenchmarkResult) -> Comparison {
        let self_mean = self.statistics().mean.as_nanos() as f64;
        let other_mean = other.statistics().mean.as_nanos() as f64;

        let speedup = if other_mean > 0.0 {
            self_mean / other_mean
        } else {
            1.0
        };

        let improvement_pct = (speedup - 1.0) * 100.0;
        let is_faster = speedup > 1.0;

        Comparison {
            baseline_name: self.name.clone(),
            candidate_name: other.name.clone(),
            speedup,
            improvement_pct,
            is_faster,
        }
    }
}

impl fmt::Display for BenchmarkResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let stats = self.statistics();
        writeln!(f, "Benchmark: {}", self.name)?;
        writeln!(f, "  Iterations: {}", self.iteration_count)?;
        writeln!(f, "  Mean:   {:?}", stats.mean)?;
        writeln!(f, "  Median: {:?}", stats.median)?;
        writeln!(f, "  Min:    {:?}", stats.min)?;
        writeln!(f, "  Max:    {:?}", stats.max)?;
        writeln!(f, "  StdDev: {:.2} ns", stats.std_dev_ns)?;
        writeln!(f, "  P95:    {:?}", stats.p95)?;
        writeln!(f, "  P99:    {:?}", stats.p99)?;
        writeln!(f, "  Ops/s:  {:.2}", stats.ops_per_sec)?;
        writeln!(f, "  ns/op:  {:.2}", stats.ns_per_op)?;
        Ok(())
    }
}

impl fmt::Display for Comparison {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "Comparison: {} vs {}", self.baseline_name, self.candidate_name)?;
        writeln!(f, "  Speedup: {:.2}x", self.speedup)?;
        writeln!(f, "  Improvement: {:.1}%", self.improvement_pct)?;
        writeln!(f, "  Faster: {}", if self.is_faster { "YES" } else { "NO" })?;
        Ok(())
    }
}

impl Timer {
    /// Create a new timer and start it immediately
    pub fn new() -> Self {
        Self {
            start: Instant::now(),
            laps: Vec::new(),
        }
    }

    /// Start the timer (or restart if already started)
    pub fn start(&mut self) {
        self.start = Instant::now();
    }

    /// Record a lap time and return the duration since last lap (or start)
    pub fn lap(&mut self) -> Duration {
        let elapsed = self.start.elapsed();
        self.laps.push(elapsed);
        self.start = Instant::now();
        elapsed
    }

    /// Get the elapsed time without recording a lap
    pub fn elapsed(&self) -> Duration {
        self.start.elapsed()
    }

    /// Get all recorded lap times
    pub fn laps(&self) -> &[Duration] {
        &self.laps
    }

    /// Reset the timer and clear all laps
    pub fn reset(&mut self) {
        self.start = Instant::now();
        self.laps.clear();
    }
}

impl Default for Timer {
    fn default() -> Self {
        Self::new()
    }
}

/// Time a single execution of a function
///
/// # Example
/// ```
/// use benchmark_utils::time_once;
///
/// let duration = time_once(|| {
///     let sum: u64 = (0..1000).sum();
///     sum
/// });
/// ```
pub fn time_once<F, R>(f: F) -> (R, Duration)
where
    F: FnOnce() -> R,
{
    let start = Instant::now();
    let result = f();
    let duration = start.elapsed();
    (result, duration)
}

/// Create a simple timer for quick measurements
///
/// # Example
/// ```
/// use benchmark_utils::timer;
///
/// let mut t = timer();
/// // ... some work ...
/// let elapsed = t.elapsed();
/// ```
pub fn timer() -> Timer {
    Timer::new()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_benchmark_creation() {
        let bench = Benchmark::new("test").iterations(10).warmup(2);
        assert_eq!(bench.iterations, 10);
        assert_eq!(bench.warmup, 2);
    }

    #[test]
    fn test_benchmark_run() {
        let bench = Benchmark::new("sum").iterations(100).warmup(10);
        let result = bench.run(|| {
            let _sum: u64 = (0..100).sum();
        });

        assert_eq!(result.iteration_count, 100);
        assert!(!result.timings.is_empty());
    }

    #[test]
    fn test_statistics() {
        let bench = Benchmark::new("test").iterations(50).warmup(5);
        let result = bench.run(|| {
            let _ = std::thread::sleep(std::time::Duration::from_micros(10));
        });

        let stats = result.statistics();
        assert!(stats.mean.as_nanos() > 0);
        assert!(stats.min <= stats.max);
        assert!(stats.ops_per_sec > 0.0);
    }

    #[test]
    fn test_comparison() {
        let bench1 = Benchmark::new("fast").iterations(10).warmup(2);
        let result1 = bench1.run(|| {
            let _sum: u64 = (0..10).sum();
        });

        let bench2 = Benchmark::new("slow").iterations(10).warmup(2);
        let result2 = bench2.run(|| {
            let _sum: u64 = (0..1000).sum();
        });

        let comparison = result1.compare(&result2);
        assert!(comparison.speedup > 0.0);
        assert!(!comparison.baseline_name.is_empty());
        assert!(!comparison.candidate_name.is_empty());
    }

    #[test]
    fn test_timer() {
        let mut timer = Timer::new();
        std::thread::sleep(std::time::Duration::from_micros(100));
        let lap = timer.lap();
        assert!(lap.as_nanos() > 0);

        let elapsed = timer.elapsed();
        assert!(elapsed.as_nanos() >= 0);
    }

    #[test]
    fn test_time_once() {
        let (result, duration) = time_once(|| {
            std::thread::sleep(std::time::Duration::from_micros(100));
            42
        });
        assert_eq!(result, 42);
        assert!(duration.as_nanos() > 0);
    }

    #[test]
    fn test_display() {
        let bench = Benchmark::new("display_test").iterations(10).warmup(2);
        let result = bench.run(|| {
            let _sum: u64 = (0..10).sum();
        });

        let output = format!("{}", result);
        assert!(output.contains("Benchmark:"));
        assert!(output.contains("display_test"));
        assert!(output.contains("Iterations:"));
    }
}
