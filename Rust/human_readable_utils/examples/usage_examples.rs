//! Human Readable Utils - Usage Examples
//!
//! Run with: cargo run --example usage_examples

use human_readable_utils::*;

fn main() {
    println!("=== Human Readable Utils Examples ===\n");

    // Bytes formatting
    println!("--- Bytes Formatting ---");
    println!("format_bytes(0)       = {}", format_bytes(0));
    println!("format_bytes(500)     = {}", format_bytes(500));
    println!("format_bytes(1024)    = {}", format_bytes(1024));
    println!("format_bytes(1536)    = {}", format_bytes(1536));
    println!("format_bytes(1048576) = {}", format_bytes(1048576));
    println!("format_bytes(1_073_741_824) = {}", format_bytes(1_073_741_824));
    println!("format_bytes_with_precision(1536, 0) = {}", format_bytes_with_precision(1536, 0));
    println!("format_bytes_with_precision(1536, 1) = {}", format_bytes_with_precision(1536, 1));
    println!();

    // Duration formatting
    println!("--- Duration Formatting ---");
    println!("format_duration(0)     = {}", format_duration(0));
    println!("format_duration(45)    = {}", format_duration(45));
    println!("format_duration(90)    = {}", format_duration(90));
    println!("format_duration(3661)  = {}", format_duration(3661));
    println!("format_duration(86400) = {}", format_duration(86400));
    println!("format_duration(90061) = {}", format_duration(90061));
    println!("format_duration_long(90)    = {}", format_duration_long(90));
    println!("format_duration_long(3661)  = {}", format_duration_long(3661));
    println!();

    // Number formatting
    println!("--- Number Formatting ---");
    println!("format_number(1000, ',')      = {}", format_number(1000, ','));
    println!("format_number(10000, ',')     = {}", format_number(10000, ','));
    println!("format_number(100000, ',')    = {}", format_number(100000, ','));
    println!("format_number(1000000, ',')   = {}", format_number(1000000, ','));
    println!("format_number(1234567, '_')   = {}", format_number(1234567, '_'));
    println!("format_number(-1000, ',')     = {}", format_number(-1000, ','));
    println!("format_float(1234567.89, 2, ',') = {}", format_float(1234567.89, 2, ','));
    println!();

    // Ordinal formatting
    println!("--- Ordinal Formatting ---");
    for n in [1, 2, 3, 4, 10, 11, 12, 13, 21, 22, 23, 100, 101, 111] {
        println!("format_ordinal({}) = {}", n, format_ordinal(n));
    }
    println!();

    // Relative time
    println!("--- Relative Time ---");
    println!("format_relative_past(30)    = {}", format_relative_past(30));
    println!("format_relative_past(60)    = {}", format_relative_past(60));
    println!("format_relative_past(3600)  = {}", format_relative_past(3600));
    println!("format_relative_past(86400) = {}", format_relative_past(86400));
    println!("format_relative_future(30)    = {}", format_relative_future(30));
    println!("format_relative_future(60)    = {}", format_relative_future(60));
    println!("format_relative_future(3600)  = {}", format_relative_future(3600));
    println!();

    // Parse bytes
    println!("--- Parse Bytes ---");
    println!("parse_bytes(\"1024\")    = {:?}", parse_bytes("1024"));
    println!("parse_bytes(\"1KB\")     = {:?}", parse_bytes("1KB"));
    println!("parse_bytes(\"1.5 MB\")  = {:?}", parse_bytes("1.5 MB"));
    println!("parse_bytes(\"2GB\")     = {:?}", parse_bytes("2GB"));
    println!();

    // Frequency formatting
    println!("--- Frequency Formatting ---");
    println!("format_frequency(100)      = {}", format_frequency(100));
    println!("format_frequency(1000)     = {}", format_frequency(1000));
    println!("format_frequency(1500)     = {}", format_frequency(1500));
    println!("format_frequency(1000000)  = {}", format_frequency(1000000));
    println!("format_frequency(2_500_000) = {}", format_frequency(2_500_000));
    println!();

    // Percentage formatting
    println!("--- Percentage Formatting ---");
    println!("format_percentage(0.5, 0)     = {}", format_percentage(0.5, 0));
    println!("format_percentage(0.123, 1)   = {}", format_percentage(0.123, 1));
    println!("format_percentage(0.12345, 2) = {}", format_percentage(0.12345, 2));
    println!();

    // Ratio formatting
    println!("--- Ratio Formatting ---");
    println!("format_ratio(0.5, 100)   = {}", format_ratio(0.5, 100));
    println!("format_ratio(0.25, 100)  = {}", format_ratio(0.25, 100));
    println!("format_ratio(0.75, 100)  = {}", format_ratio(0.75, 100));
    println!("format_ratio(0.333, 100) = {}", format_ratio(0.333, 100));
    println!();

    // Plural formatting
    println!("--- Plural Formatting ---");
    println!("format_plural(1, \"item\", None)       = {}", format_plural(1, "item", None));
    println!("format_plural(5, \"item\", None)       = {}", format_plural(5, "item", None));
    println!("format_plural(1, \"child\", Some(\"children\")) = {}", format_plural(1, "child", Some("children")));
    println!("format_plural(5, \"child\", Some(\"children\")) = {}", format_plural(5, "child", Some("children")));
    println!();

    // Scientific notation
    println!("--- Scientific Notation ---");
    println!("format_scientific(1234567.0, 2) = {}", format_scientific(1234567.0, 2));
    println!("format_scientific(0.000123, 2)  = {}", format_scientific(0.000123, 2));
    println!();

    println!("=== All examples completed successfully! ===");
}