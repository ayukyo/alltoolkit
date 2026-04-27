//! # Histogram Utilities Examples
//!
//! Demonstrates usage of the histogram utilities for Rust.

use histogram_utils::{Histogram, BinningStrategy, describe, histogram, histogram_with_bins};

fn main() {
    println!("=== Histogram Utilities Examples ===\n");

    // Example 1: Basic histogram creation
    basic_histogram();
    
    // Example 2: Different binning strategies
    binning_strategies();
    
    // Example 3: Statistical analysis
    statistical_analysis();
    
    // Example 4: Custom bin edges
    custom_edges();
    
    // Example 5: Descriptive statistics
    descriptive_stats();
    
    // Example 6: ASCII visualization
    ascii_visualization();
    
    // Example 7: Percentile calculation
    percentile_example();
    
    // Example 8: Working with real-world data
    real_world_example();
}

fn basic_histogram() {
    println!("--- Example 1: Basic Histogram ---");
    
    let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
    let hist = histogram(&data).unwrap();
    
    println!("Data: {:?}", data);
    println!("Bin count: {}", hist.bin_count());
    println!("Bin width: {}", hist.bin_width());
    println!("Counts: {:?}", hist.counts());
    println!("Edges: {:?}", hist.edges());
    println!("Total: {}", hist.total());
    println!();
}

fn binning_strategies() {
    println!("--- Example 2: Binning Strategies ---");
    
    let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
    
    let strategies = [
        ("Sturges", BinningStrategy::Sturges),
        ("Square Root", BinningStrategy::SquareRoot),
        ("Rice", BinningStrategy::Rice),
        ("Freedman-Diaconis", BinningStrategy::FreedmanDiaconis),
        ("Fixed (10)", BinningStrategy::Fixed(10)),
    ];
    
    for (name, strategy) in strategies {
        let hist = Histogram::new(&data, strategy).unwrap();
        println!("{}: {} bins", name, hist.bin_count());
    }
    println!();
}

fn statistical_analysis() {
    println!("--- Example 3: Statistical Analysis ---");
    
    let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
    let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
    
    println!("Mean: {:?}", hist.mean());
    println!("Median: {:?}", hist.median());
    println!("Mode: {:?}", hist.mode());
    println!("Variance: {:?}", hist.variance());
    println!("Std Dev: {:?}", hist.std_dev());
    println!("Min: {}", hist.min());
    println!("Max: {}", hist.max());
    println!();
}

fn custom_edges() {
    println!("--- Example 4: Custom Bin Edges ---");
    
    let data = vec![
        15.0, 22.0, 31.0, 45.0, 52.0, 61.0, 72.0, 85.0, 91.0, 98.0,
        105.0, 112.0, 125.0, 138.0, 152.0
    ];
    
    // Custom edges for age groups
    let edges = vec![0.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0];
    let hist = Histogram::with_edges(&data, &edges).unwrap();
    
    println!("Custom bin edges (age groups):");
    for i in 0..hist.bin_count() {
        let range = hist.bin_range(i).unwrap();
        let count = hist.count_for_bin(i).unwrap();
        println!("  Age {:.0}-{:.0}: {} people", range.0, range.1, count);
    }
    println!();
}

fn descriptive_stats() {
    println!("--- Example 5: Descriptive Statistics ---");
    
    let data = vec![12.5, 15.3, 18.7, 22.1, 25.8, 29.3, 33.5, 37.2, 41.8, 48.5];
    let stats = describe(&data).unwrap();
    
    println!("Data: {:?}", data);
    println!("Count: {}", stats.count);
    println!("Sum: {:.2}", stats.sum);
    println!("Mean: {:.2}", stats.mean);
    println!("Variance: {:.2}", stats.variance);
    println!("Std Dev: {:.2}", stats.std_dev);
    println!("Min: {:.2}", stats.min);
    println!("Max: {:.2}", stats.max);
    println!("Range: {:.2}", stats.range);
    println!("Median: {:.2}", stats.median);
    println!("Q1: {:.2}", stats.q1);
    println!("Q3: {:.2}", stats.q3);
    println!("IQR: {:.2}", stats.iqr);
    println!();
}

fn ascii_visualization() {
    println!("--- Example 6: ASCII Visualization ---");
    
    // Create data with some variation
    let data = vec![
        5.0, 5.0, 5.0, 5.0, // 4 counts in first bin
        10.0, 10.0, 10.0, 10.0, 10.0, // 5 counts
        15.0, 15.0, 15.0, 15.0, 15.0, 15.0, // 6 counts (peak)
        20.0, 20.0, 20.0, 20.0, 20.0, // 5 counts
        25.0, 25.0, 25.0, // 3 counts
    ];
    
    let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
    println!("Histogram (ASCII art):");
    println!("{}", hist.to_ascii(20));
}

fn percentile_example() {
    println!("--- Example 7: Percentile Calculation ---");
    
    let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
    let hist = Histogram::new(&data, BinningStrategy::Fixed(20)).unwrap();
    
    println!("Percentiles from histogram:");
    for p in [10.0, 25.0, 50.0, 75.0, 90.0] {
        let value = hist.percentile(p).unwrap();
        println!("  {}th percentile: {:.2}", p, value);
    }
    println!();
}

fn real_world_example() {
    println!("--- Example 8: Real-World Example (Test Scores) ---");
    
    // Simulate test scores (0-100)
    let scores = vec![
        45.0, 52.0, 58.0, 61.0, 63.0, 65.0, 67.0, 68.0, 70.0, 72.0,
        74.0, 75.0, 76.0, 78.0, 79.0, 80.0, 82.0, 83.0, 85.0, 87.0,
        88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 98.0,
    ];
    
    // Create histogram with 5 bins (grade ranges)
    let grade_edges = vec![0.0, 60.0, 70.0, 80.0, 90.0, 100.0];
    let hist = Histogram::with_edges(&scores, &grade_edges).unwrap();
    
    println!("Test Score Distribution:");
    let grade_labels = ["F", "D", "C", "B", "A"];
    for i in 0..hist.bin_count() {
        let range = hist.bin_range(i).unwrap();
        let count = hist.count_for_bin(i).unwrap();
        let freq = hist.frequencies()[i] * 100.0;
        println!("  {} ({:.0}-{:.0}): {} students ({:.1}%)", 
            grade_labels[i], range.0, range.1, count, freq);
    }
    
    println!("\nStatistics:");
    println!("  Mean score: {:.1}", hist.mean().unwrap_or(0.0));
    println!("  Median score: {:.1}", hist.median().unwrap_or(0.0));
    println!("  Class average: {:.1}", describe(&scores).unwrap().mean);
    
    println!("\nPercentile analysis:");
    println!("  25th percentile: {:.1} (bottom quarter)", hist.percentile(25.0).unwrap_or(0.0));
    println!("  75th percentile: {:.1} (top quarter)", hist.percentile(75.0).unwrap_or(0.0));
    println!();
}