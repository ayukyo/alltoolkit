//! Progress Bar Example
//! 
//! Demonstrates all features of the progress_bar module.
//! Run with: rustc example.rs --edition 2021 && ./example

mod mod_rs;

use mod_rs::{ProgressBar, Style, Config, run_examples};
use std::time::Duration;
use std::thread;

fn main() {
    println!("╔════════════════════════════════════════════╗");
    println!("║    Rust Progress Bar - Usage Examples      ║");
    println!("╚════════════════════════════════════════════╝");
    println!();

    // Example 1: Basic usage
    println!("Example 1: Basic Progress Bar");
    println!("-" ^ 40);
    {
        let mut pb = ProgressBar::new(30);
        pb.set_message("Processing");
        
        for i in 0..30 {
            thread::sleep(Duration::from_millis(50));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Done!");
    }
    println!();

    // Example 2: Different styles
    println!("Example 2: Progress Bar Styles");
    println!("-" ^ 40);
    
    let styles = [
        (Style::Classic, "Classic"),
        (Style::Modern, "Modern"),
        (Style::Dots, "Dots"),
        (Style::Arrows, "Arrows"),
        (Style::Minimal, "Minimal"),
    ];

    for (style, name) in styles.iter() {
        println!("  {} style:", name);
        let mut pb = ProgressBar::new(20);
        pb.set_style(*style);
        
        for _ in 0..20 {
            thread::sleep(Duration::from_millis(30));
            pb.inc(1);
            pb.print();
        }
        pb.finish();
        thread::sleep(Duration::from_millis(100));
    }
    println!();

    // Example 3: Custom configuration
    println!("Example 3: Custom Configuration");
    println!("-" ^ 40);
    {
        let config = Config {
            width: 25,
            show_percent: true,
            show_count: true,
            show_eta: true,
            show_elapsed: true,
            show_rate: true,
        };

        let mut pb = ProgressBar::new(50);
        pb.set_style(Style::Modern);
        pb.set_config(config);
        pb.set_message("🚀 Uploading");

        for _ in 0..50 {
            thread::sleep(Duration::from_millis(40));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Upload complete");
    }
    println!();

    // Example 4: Indeterminate progress
    println!("Example 4: Indeterminate Progress (Spinner)");
    println!("-" ^ 40);
    {
        let mut pb = ProgressBar::indeterminate();
        pb.set_message("⏳ Loading data");

        for _ in 0..25 {
            thread::sleep(Duration::from_millis(80));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Data loaded");
    }
    println!();

    // Example 5: Increment by different amounts
    println!("Example 5: Variable Increments");
    println!("-" ^ 40);
    {
        let mut pb = ProgressBar::new(100);
        pb.set_style(Style::Dots);
        pb.set_message("📊 Analytics");

        // Simulate batch processing with varying sizes
        let batches = [15, 25, 10, 30, 20];
        for batch in batches.iter() {
            thread::sleep(Duration::from_millis(100));
            pb.inc(*batch);
            pb.print();
        }
        pb.finish_with_message("Analysis complete");
    }
    println!();

    // Example 6: Reusable progress bar
    println!("Example 6: Reset and Reuse");
    println!("-" ^ 40);
    {
        let mut pb = ProgressBar::new(20);
        pb.set_style(Style::Arrows);

        // First task
        pb.set_message("Task 1");
        for _ in 0..20 {
            thread::sleep(Duration::from_millis(25));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Task 1 done");

        // Reset for second task
        pb.reset();
        pb.set_total(15);
        pb.set_message("Task 2");

        for _ in 0..15 {
            thread::sleep(Duration::from_millis(30));
            pb.inc(1);
            pb.print();
        }
        pb.finish_with_message("Task 2 done");
    }
    println!();

    println!("╔════════════════════════════════════════════╗");
    println!("║          All Examples Completed!           ║");
    println!("╚════════════════════════════════════════════╝");
}