//! Usage Examples for Cron Expression Utilities
//!
//! This example demonstrates various ways to use the cron expression utilities.

use cron_expression_utils::{CronExpression, validate, next_run, next_runs, get_preset, list_presets};

fn main() {
    println!("=== Cron Expression Utilities Examples ===\n");

    // Basic parsing
    println!("1. Basic Parsing:");
    let cron = CronExpression::parse("* * * * *").unwrap();
    println!("   Parsed: {}", cron);
    println!("   Has seconds: {}", cron.has_seconds);
    println!();

    // Specific time expressions
    println!("2. Specific Time Expressions:");
    let cron = CronExpression::parse("30 14 * * *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Minutes: {:?}", cron.minute_values());
    println!("   Hours: {:?}", cron.hour_values());
    println!();

    // Range expressions
    println!("3. Range Expressions:");
    let cron = CronExpression::parse("0 9-17 * * *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Hours (9am-5pm): {:?}", cron.hour_values());
    println!();

    // Step expressions
    println!("4. Step Expressions:");
    let cron = CronExpression::parse("*/15 * * * *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Minutes (every 15): {:?}", cron.minute_values());
    println!();

    // Weekday expressions
    println!("5. Weekday Expressions:");
    let cron = CronExpression::parse("0 9 * * mon-fri").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Days of week: {:?}", cron.day_of_week_values());
    println!();

    // Month expressions
    println!("6. Month Expressions:");
    let cron = CronExpression::parse("0 0 1 jan,jul *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Months: {:?}", cron.month_values());
    println!();

    // 6-field expressions (with seconds)
    println!("7. Six-Field Expressions (with seconds):");
    let cron = CronExpression::parse("30 0 12 * * *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Has seconds: {}", cron.has_seconds);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Seconds: {:?}", cron.second_values());
    println!();

    // Validation
    println!("8. Validation:");
    let expressions = [
        "* * * * *",
        "*/5 * * * *",
        "0 12 * * *",
        "0 0 1 * *",
        "invalid",
        "60 * * * *",
    ];
    for expr in expressions {
        let result = validate(expr);
        println!("   '{}' -> {}", expr, if result.is_ok() { "valid" } else { "invalid" });
    }
    println!();

    // Next run times
    println!("9. Next Run Times:");
    let cron = CronExpression::parse("0 12 * * *").unwrap();
    println!("   Expression: {}", cron.original);
    
    // Use a fixed timestamp for demonstration
    let timestamp = 1700000000u64; // 2023-11-14 22:13:20 UTC
    let next = cron.next_run(timestamp).unwrap();
    println!("   Current timestamp: {}", timestamp);
    println!("   Next run timestamp: {}", next);
    println!();

    // Multiple next runs
    println!("10. Multiple Next Runs:");
    let runs = cron.next_runs(timestamp, 5).unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Next 5 runs:");
    for (i, run) in runs.iter().enumerate() {
        println!("     Run {}: {}", i + 1, run);
    }
    println!();

    // Convenience functions
    println!("11. Convenience Functions:");
    let next = next_run("*/15 * * * *", timestamp).unwrap();
    println!("   next_run('*/15 * * * *', {}) = {}", timestamp, next);
    
    let runs = next_runs("0 * * * *", timestamp, 3).unwrap();
    println!("   next_runs('0 * * * *', {}, 3) = {:?}", timestamp, runs);
    println!();

    // Presets
    println!("12. Cron Presets:");
    let presets = list_presets();
    println!("   Available presets:");
    for (name, expr) in presets {
        println!("     {} = '{}'", name, expr);
    }
    println!();

    // Get specific preset
    println!("13. Get Preset by Name:");
    let preset = get_preset("every_hour");
    println!("   get_preset('every_hour') = {:?}", preset);
    let preset = get_preset("every_weekday");
    println!("   get_preset('every_weekday') = {:?}", preset);
    println!();

    // Complex expressions
    println!("14. Complex Expressions:");
    let cron = CronExpression::parse("*/10 9-17 * * 1-5").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   Human readable: {}", cron.to_human_readable());
    println!("   Every 10 minutes during business hours on weekdays");
    println!("   Minutes: {:?}", cron.minute_values());
    println!("   Hours: {:?}", cron.hour_values());
    println!("   Days: {:?}", cron.day_of_week_values());
    println!();

    // Matching specific times
    println!("15. Matching Specific Times:");
    let cron = CronExpression::parse("30 14 * * *").unwrap();
    println!("   Expression: {}", cron.original);
    println!("   matches(0, 30, 14, ...) = {}", cron.matches(0, 30, 14, 15, 5, 3)); // 14:30
    println!("   matches(0, 31, 14, ...) = {}", cron.matches(0, 31, 14, 15, 5, 3)); // 14:31
    println!("   matches(0, 30, 15, ...) = {}", cron.matches(0, 30, 15, 15, 5, 3)); // 15:30
    println!();

    println!("=== Examples Complete ===");
}