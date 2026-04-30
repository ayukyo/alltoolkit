//! # Sliding Window Utils - Usage Examples
//! 
//! This example demonstrates various use cases for sliding windows:
//! - Rate limiting
//! - Moving averages
//! - Metrics collection
//! - Trend analysis

use sliding_window_utils::{CountWindow, RateLimiter, TimeWindow, WeightedWindow};
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Sliding Window Utils Examples ===\n");

    // Example 1: Rate Limiting
    rate_limiting_example();
    
    // Example 2: Moving Average
    moving_average_example();
    
    // Example 3: Weighted Moving Average
    weighted_average_example();
    
    // Example 4: Time-based Metrics
    time_window_example();
    
    // Example 5: Stock Price Analysis
    stock_price_example();
    
    // Example 6: Network Traffic Monitoring
    network_monitor_example();
}

/// Example 1: Rate Limiting
/// Use case: API rate limiting
fn rate_limiting_example() {
    println!("--- Example 1: Rate Limiting ---");
    
    // Allow maximum 5 requests per minute
    let mut limiter = RateLimiter::new(5, Duration::from_secs(60));
    
    println!("API Rate Limiter (5 requests/minute)");
    
    // Simulate 7 requests
    for i in 1..=7 {
        let allowed = limiter.allow();
        let remaining = limiter.remaining();
        println!(
            "  Request {}: {} (remaining: {})",
            i,
            if allowed { "ALLOWED" } else { "DENIED" },
            remaining
        );
    }
    
    println!("  Current count: {}", limiter.current_count());
    println!();
}

/// Example 2: Simple Moving Average
/// Use case: Sensor data smoothing
fn moving_average_example() {
    println!("--- Example 2: Simple Moving Average ---");
    
    let mut window = CountWindow::<f64>::new(5);
    let temperatures = [22.5, 23.1, 22.8, 24.0, 23.5, 22.9, 23.8, 24.5, 23.7, 22.8];
    
    println!("Temperature readings (5-period moving average):");
    
    for temp in temperatures {
        window.push(temp);
        let avg = window.average();
        let min = window.min().unwrap_or(0.0);
        let max = window.max().unwrap_or(0.0);
        println!(
            "  Temp: {:.1}°C | Avg: {:.2}°C | Range: [{:.1}, {:.1}]",
            temp, avg, min, max
        );
    }
    println!();
}

/// Example 3: Weighted Moving Average
/// Use case: Recent data is more important
fn weighted_average_example() {
    println!("--- Example 3: Weighted Moving Average ---");
    
    let mut linear_window = WeightedWindow::new(4);
    let mut exp_window = WeightedWindow::exponential(4);
    
    let prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0];
    
    println!("Price trend analysis:");
    println!("  Linear weights give equal importance growth");
    println!("  Exponential weights heavily favor recent data\n");
    
    println!("{:>8} | {:>12} | {:>12}", "Price", "Linear WMA", "Exp WMA");
    println!("{:-<8}-+-{:-<12}-+-{:-<12}", "", "", "");
    
    for price in prices {
        linear_window.push(price);
        exp_window.push(price);
        
        let linear_avg = linear_window.weighted_average();
        let exp_avg = exp_window.weighted_average();
        
        println!(
            "  ${:>6.2} | ${:>11.2} | ${:>11.2}",
            price, linear_avg, exp_avg
        );
    }
    println!();
}

/// Example 4: Time-based Window
/// Use case: Event tracking within time period
fn time_window_example() {
    println!("--- Example 4: Time-based Window ---");
    
    let mut window = TimeWindow::new(Duration::from_secs(2));
    
    println!("Tracking events in a 2-second window:\n");
    
    window.record("event_1");
    window.record("event_2");
    window.record("event_3");
    
    println!("  Recorded 3 events");
    println!("  Current count: {}", window.count());
    println!("  Events: {:?}", window.values());
    
    println!("\n  Waiting 2.5 seconds...");
    thread::sleep(Duration::from_millis(2500));
    
    println!("  After 2.5 seconds:");
    println!("  Current count: {} (events expired)", window.count());
    
    window.record("event_4");
    println!("  After new event: count = {}", window.count());
    println!();
}

/// Example 5: Stock Price Analysis
/// Use case: Technical indicators
fn stock_price_example() {
    println!("--- Example 5: Stock Price Analysis ---");
    
    let mut prices = CountWindow::<f64>::new(10);
    let mut volume = CountWindow::<i64>::new(10);
    
    // Simulated stock data
    let data = [
        (150.25, 1000000),
        (151.10, 1200000),
        (150.80, 900000),
        (152.00, 1500000),
        (153.25, 1800000),
        (152.50, 1300000),
        (153.80, 1600000),
        (154.10, 1700000),
        (153.90, 1400000),
        (154.50, 1900000),
    ];
    
    println!("Analyzing stock price movements:\n");
    println!("{:>8} | {:>10} | {:>10} | {:>10}", 
             "Price", "Vol Avg", "Price Avg", "Vol(M)");
    println!("{:-<8}-+-{:-<10}-+-{:-<10}-+-{:-<10}", "", "", "", "");
    
    for (price, vol) in data {
        prices.push(price);
        volume.push(vol);
        
        let price_avg = prices.average();
        let vol_avg = volume.average();
        let vol_sum = volume.sum() as f64 / 1_000_000.0;
        
        println!(
            "  ${:>6.2} | {:>10.0} | ${:>9.2} | {:>9.2}M",
            price, vol_avg, price_avg, vol_sum
        );
    }
    
    // Calculate price statistics
    println!("\n  Price Statistics:");
    println!("    Min: ${:.2}", prices.min().unwrap_or(0.0));
    println!("    Max: ${:.2}", prices.max().unwrap_or(0.0));
    println!("    Avg: ${:.2}", prices.average());
    println!();
}

/// Example 6: Network Traffic Monitoring
/// Use case: Bandwidth monitoring
fn network_monitor_example() {
    println!("--- Example 6: Network Traffic Monitoring ---");
    
    let mut bandwidth = CountWindow::<f64>::new(6); // 6 samples
    
    // Simulated bandwidth samples in Mbps
    let samples = [45.2, 52.1, 78.5, 95.3, 82.7, 65.4, 48.9, 55.2, 71.8, 89.1];
    
    println!("Monitoring network bandwidth (6-sample window):\n");
    println!("{:>8} | {:>8} | {:>8} | {:>12}", 
             "Sample", "Current", "Avg", "Status");
    println!("{:-<8}-+-{:-<8}-+-{:-<8}-+-{:-<12}", "", "", "", "");
    
    for sample in samples {
        bandwidth.push(sample);
        
        let avg = bandwidth.average();
        let _min = bandwidth.min().unwrap_or(0.0);
        let _max = bandwidth.max().unwrap_or(0.0);
        
        let status = if sample > avg * 1.2 {
            "HIGH SPIKE"
        } else if sample < avg * 0.8 {
            "LOW"
        } else {
            "NORMAL"
        };
        
        println!(
            "  {:>6.1} Mbps | {:>6.1} Mbps | {:>6.1} Mbps | {:>12}",
            sample, avg, sample, status
        );
        
        // Alert on high bandwidth usage
        if sample > 80.0 {
            println!("    ⚠️  High bandwidth alert!");
        }
    }
    
    println!("\n  Summary:");
    println!("    Peak: {:.1} Mbps", bandwidth.max().unwrap_or(0.0));
    println!("    Low:  {:.1} Mbps", bandwidth.min().unwrap_or(0.0));
    println!();
}