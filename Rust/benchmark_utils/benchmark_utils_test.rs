//! Benchmark Utilities Test Suite
//!
//! Comprehensive tests for the benchmark_utils module

use std::thread;
use std::time::Duration;

// Import the module
#[path = "mod.rs"]
mod benchmark_utils;

use benchmark_utils::*;

fn main() {
    println!("Running Benchmark Utils Tests...\n");

    test_benchmark_creation();
    test_benchmark_run();
    test_benchmark_with_iterations();
    test_statistics();
    test_comparison();
    test_timer();
    test_time_once();
    test_display();
    test_multiple_benchmarks();
    test_edge_cases();

    println!("\nAll tests passed!");
}

fn test_benchmark_creation() {
    println!("Test: benchmark_creation");
    let bench = Benchmark::new("test").iterations(10).warmup(2);
    assert_eq!(bench.iterations, 10);
    assert_eq!(bench.warmup, 2);
    println!("  PASSED\n");
}

fn test_benchmark_run() {
    println!("Test: benchmark_run");
    let bench = Benchmark::new("sum").iterations(100).warmup(10);
    let result = bench.run(|| {
        let _sum: u64 = (0..100).sum();
    });

    assert_eq!(result.iteration_count, 100);
    assert!(!result.timings.is_empty());
    assert_eq!(result.name, "sum");
    println!("  PASSED\n");
}

fn test_benchmark_with_iterations() {
    println!("Test: benchmark_with_iterations");
    let bench = Benchmark::new("process_items").iterations(50).warmup(5);
    let result = bench.run(|| {
        // Simulate processing 100 items
        let mut sum = 0u64;
        for i in 0..100 {
            sum += i;
        }
        (sum, 100)
    });

    assert_eq!(result.iteration_count, 50);
    assert!(!result.timings.is_empty());
    println!("  PASSED\n");
}

fn test_statistics() {
    println!("Test: statistics");
    let bench = Benchmark::new("stats_test").iterations(100).warmup(10);
    let result = bench.run(|| {
        // Small predictable work
        let _ = thread::sleep(Duration::from_micros(10));
    });

    let stats = result.statistics();
    assert!(stats.mean.as_nanos() > 0);
    assert!(stats.min <= stats.max);
    assert!(stats.median >= stats.min && stats.median <= stats.max);
    assert!(stats.p95 >= stats.median);
    assert!(stats.p99 >= stats.p95);
    assert!(stats.ops_per_sec > 0.0);
    assert!(stats.ns_per_op > 0.0);
    assert!(stats.std_dev_ns >= 0.0);
    println!("  PASSED\n");
}

fn test_comparison() {
    println!("Test: comparison");
    let bench1 = Benchmark::new("fast").iterations(10).warmup(2);
    let result1 = bench1.run(|| {
        let _sum: u64 = (0..10).sum();
    });

    let bench2 = Benchmark::new("slow").iterations(10).warmup(2);
    let result2 = bench2.run(|| {
        let _sum: u64 = (0..10000).sum();
    });

    let comparison = result1.compare(&result2);
    assert!(comparison.speedup > 0.0);
    assert!(!comparison.baseline_name.is_empty());
    assert!(!comparison.candidate_name.is_empty());
    assert!(comparison.is_faster); // fast should be faster than slow
    println!("  PASSED\n");
}

fn test_timer() {
    println!("Test: timer");
    let mut timer = Timer::new();
    thread::sleep(Duration::from_micros(100));
    let lap = timer.lap();
    assert!(lap.as_nanos() > 0);

    let elapsed = timer.elapsed();
    assert!(elapsed.as_nanos() >= 0);

    assert_eq!(timer.laps().len(), 1);
    assert_eq!(timer.laps()[0], lap);

    timer.reset();
    assert!(timer.laps().is_empty());
    println!("  PASSED\n");
}

fn test_time_once() {
    println!("Test: time_once");
    let (result, duration) = time_once(|| {
        thread::sleep(Duration::from_micros(100));
        42
    });
    assert_eq!(result, 42);
    assert!(duration.as_nanos() > 0);
    println!("  PASSED\n");
}

fn test_display() {
    println!("Test: display");
    let bench = Benchmark::new("display_test").iterations(10).warmup(2);
    let result = bench.run(|| {
        let _sum: u64 = (0..10).sum();
    });

    let output = format!("{}", result);
    assert!(output.contains("Benchmark:"));
    assert!(output.contains("display_test"));
    assert!(output.contains("Iterations:"));
    assert!(output.contains("Mean:"));
    assert!(output.contains("Median:"));
    assert!(output.contains("Ops/s:"));
    println!("  PASSED\n");
}

fn test_multiple_benchmarks() {
    println!("Test: multiple_benchmarks");

    // Compare different implementations
    let bench1 = Benchmark::new("vec_push").iterations(1000).warmup(100);
    let result1 = bench1.run(|| {
        let mut v = Vec::new();
        for i in 0..100 {
            v.push(i);
        }
        v
    });

    let bench2 = Benchmark::new("vec_with_capacity").iterations(1000).warmup(100);
    let result2 = bench2.run(|| {
        let mut v = Vec::with_capacity(100);
        for i in 0..100 {
            v.push(i);
        }
        v
    });

    let comparison = result1.compare(&result2);
    println!("  Vec with capacity is {:.2}x faster", comparison.speedup);
    println!("  PASSED\n");
}

fn test_edge_cases() {
    println!("Test: edge_cases");

    // Empty benchmark
    let bench = Benchmark::new("empty").iterations(0).warmup(0);
    let result = bench.run(|| {});
    assert!(result.timings.is_empty());
    let stats = result.statistics();
    assert_eq!(stats.mean, Duration::ZERO);

    // Single iteration
    let bench = Benchmark::new("single").iterations(1).warmup(0);
    let result = bench.run(|| { 42 });
    assert_eq!(result.timings.len(), 1);

    // Very fast operation
    let bench = Benchmark::new("fast").iterations(10000).warmup(100);
    let result = bench.run(|| {
        let _ = 1 + 1;
    });
    assert_eq!(result.timings.len(), 10000);
    let stats = result.statistics();
    assert!(stats.ops_per_sec > 0.0);

    println!("  PASSED\n");
}
