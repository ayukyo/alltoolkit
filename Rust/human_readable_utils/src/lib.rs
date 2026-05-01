//! Human Readable Formatting Utilities
//! ====================================
//!
//! A zero-dependency library for formatting values into human-readable strings.
//!
//! Features:
//! - Bytes formatting (1024 -> "1.00 KB")
//! - Duration formatting (3661 -> "1h 1m 1s")
//! - Number formatting with separators (1000000 -> "1,000,000")
//! - Ordinal numbers (1 -> "1st", 2 -> "2nd")
//! - Relative time ("3 hours ago", "in 2 days")
//!
//! Author: AllToolkit
//! Date: 2026-05-02

use std::time::{Duration, SystemTime, UNIX_EPOCH};

/// Byte size units
const BYTE_UNITS: [&str; 9] = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

/// Time units for duration formatting
const TIME_UNITS: [(&str, u64); 6] = [
    ("y", 365 * 24 * 60 * 60),
    ("d", 24 * 60 * 60),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1),
    ("ms", 0),
];

/// Formats bytes into a human-readable string.
///
/// # Arguments
/// * `bytes` - The number of bytes
///
/// # Returns
/// A human-readable string like "1.50 KB" or "2.00 GB"
///
/// # Examples
/// ```
/// use human_readable_utils::format_bytes;
///
/// assert_eq!(format_bytes(0), "0 B");
/// assert_eq!(format_bytes(1024), "1.00 KB");
/// assert_eq!(format_bytes(1536), "1.50 KB");
/// assert_eq!(format_bytes(1048576), "1.00 MB");
/// ```
pub fn format_bytes(bytes: u64) -> String {
    if bytes == 0 {
        return "0 B".to_string();
    }

    let mut size = bytes as f64;
    let mut unit_index = 0;

    while size >= 1024.0 && unit_index < BYTE_UNITS.len() - 1 {
        size /= 1024.0;
        unit_index += 1;
    }

    if unit_index == 0 {
        format!("{} {}", bytes, BYTE_UNITS[0])
    } else {
        format!("{:.2} {}", size, BYTE_UNITS[unit_index])
    }
}

/// Formats bytes with a specified precision.
///
/// # Arguments
/// * `bytes` - The number of bytes
/// * `precision` - Number of decimal places
///
/// # Examples
/// ```
/// use human_readable_utils::format_bytes_with_precision;
///
/// assert_eq!(format_bytes_with_precision(1536, 0), "2 KB");
/// assert_eq!(format_bytes_with_precision(1536, 1), "1.5 KB");
/// assert_eq!(format_bytes_with_precision(1536, 3), "1.500 KB");
/// ```
pub fn format_bytes_with_precision(bytes: u64, precision: usize) -> String {
    if bytes == 0 {
        return "0 B".to_string();
    }

    let mut size = bytes as f64;
    let mut unit_index = 0;

    while size >= 1024.0 && unit_index < BYTE_UNITS.len() - 1 {
        size /= 1024.0;
        unit_index += 1;
    }

    if unit_index == 0 {
        format!("{} {}", bytes, BYTE_UNITS[0])
    } else {
        format!("{:.*} {}", precision, size, BYTE_UNITS[unit_index])
    }
}

/// Formats a duration in seconds into a human-readable string.
///
/// # Arguments
/// * `seconds` - Duration in seconds
///
/// # Returns
/// A string like "1h 30m 45s" or "45s"
///
/// # Examples
/// ```
/// use human_readable_utils::format_duration;
///
/// assert_eq!(format_duration(0), "0s");
/// assert_eq!(format_duration(45), "45s");
/// assert_eq!(format_duration(90), "1m 30s");
/// assert_eq!(format_duration(3661), "1h 1m 1s");
/// assert_eq!(format_duration(86461), "1d 1m 1s");
/// ```
pub fn format_duration(seconds: u64) -> String {
    if seconds == 0 {
        return "0s".to_string();
    }

    let mut remaining = seconds;
    let mut parts = Vec::new();

    for (unit, value) in TIME_UNITS.iter().take(5) {
        if remaining >= *value {
            let count = remaining / value;
            parts.push(format!("{}{}", count, unit));
            remaining %= value;
        }
    }

    if parts.is_empty() {
        format!("{}ms", remaining)
    } else {
        parts.join(" ")
    }
}

/// Formats a duration with full unit names.
///
/// # Examples
/// ```
/// use human_readable_utils::format_duration_long;
///
/// assert_eq!(format_duration_long(90), "1 minute 30 seconds");
/// assert_eq!(format_duration_long(3661), "1 hour 1 minute 1 second");
/// ```
pub fn format_duration_long(seconds: u64) -> String {
    if seconds == 0 {
        return "0 seconds".to_string();
    }

    let mut remaining = seconds;
    let mut parts = Vec::new();

    let units: [(&str, &str, u64); 5] = [
        ("year", "years", 365 * 24 * 60 * 60),
        ("day", "days", 24 * 60 * 60),
        ("hour", "hours", 60 * 60),
        ("minute", "minutes", 60),
        ("second", "seconds", 1),
    ];

    for (singular, plural, value) in units.iter() {
        if remaining >= *value {
            let count = remaining / value;
            let unit = if count == 1 { *singular } else { *plural };
            parts.push(format!("{} {}", count, unit));
            remaining %= value;
        }
    }

    parts.join(" ")
}

/// Formats a duration from a `std::time::Duration`.
///
/// # Examples
/// ```
/// use std::time::Duration;
/// use human_readable_utils::format_duration_from;
///
/// let d = Duration::from_secs(90);
/// assert_eq!(format_duration_from(d), "1m 30s");
/// ```
pub fn format_duration_from(duration: Duration) -> String {
    format_duration(duration.as_secs())
}

/// Formats a number with thousands separators.
///
/// # Arguments
/// * `number` - The number to format
/// * `separator` - The separator character (usually ',' or '_')
///
/// # Examples
/// ```
/// use human_readable_utils::format_number;
///
/// assert_eq!(format_number(1000, ','), "1,000");
/// assert_eq!(format_number(1000000, ','), "1,000,000");
/// assert_eq!(format_number(1234567, '_'), "1_234_567");
/// ```
pub fn format_number(number: i64, separator: char) -> String {
    let num_str = number.abs().to_string();
    let mut result = String::new();
    let chars: Vec<char> = num_str.chars().collect();

    for (i, c) in chars.iter().enumerate() {
        if i > 0 && (chars.len() - i) % 3 == 0 {
            result.push(separator);
        }
        result.push(*c);
    }

    if number < 0 {
        format!("-{}", result)
    } else {
        result
    }
}

/// Formats a number with default comma separator.
///
/// # Examples
/// ```
/// use human_readable_utils::format_number_comma;
///
/// assert_eq!(format_number_comma(1000000), "1,000,000");
/// ```
pub fn format_number_comma(number: i64) -> String {
    format_number(number, ',')
}

/// Formats a floating point number with thousands separators.
///
/// # Examples
/// ```
/// use human_readable_utils::format_float;
///
/// assert_eq!(format_float(1234567.89, 2, ','), "1,234,567.89");
/// ```
pub fn format_float(number: f64, decimals: usize, separator: char) -> String {
    let abs_num = number.abs();
    let int_part = abs_num.trunc() as i64;
    let dec_part = abs_num.fract();

    let mut formatted_int = format_number(int_part, separator);
    
    if decimals > 0 {
        let dec_str = format!("{:.*}", decimals, dec_part);
        let dec_digits: String = dec_str.chars().skip(2).collect(); // Skip "0."
        formatted_int.push('.');
        formatted_int.push_str(&dec_digits);
    }

    if number < 0.0 {
        format!("-{}", formatted_int)
    } else {
        formatted_int
    }
}

/// Converts a number to its ordinal form.
///
/// # Examples
/// ```
/// use human_readable_utils::format_ordinal;
///
/// assert_eq!(format_ordinal(1), "1st");
/// assert_eq!(format_ordinal(2), "2nd");
/// assert_eq!(format_ordinal(3), "3rd");
/// assert_eq!(format_ordinal(4), "4th");
/// assert_eq!(format_ordinal(11), "11th");
/// assert_eq!(format_ordinal(21), "21st");
/// assert_eq!(format_ordinal(22), "22nd");
/// assert_eq!(format_ordinal(23), "23rd");
/// assert_eq!(format_ordinal(111), "111th");
/// ```
pub fn format_ordinal(number: i64) -> String {
    if number <= 0 {
        return number.to_string();
    }

    let suffix = match number % 100 {
        11..=13 => "th",
        _ => match number % 10 {
            1 => "st",
            2 => "nd",
            3 => "rd",
            _ => "th",
        },
    };

    format!("{}{}", number, suffix)
}

/// Returns the ordinal suffix for a number.
///
/// # Examples
/// ```
/// use human_readable_utils::ordinal_suffix;
///
/// assert_eq!(ordinal_suffix(1), "st");
/// assert_eq!(ordinal_suffix(2), "nd");
/// assert_eq!(ordinal_suffix(3), "rd");
/// assert_eq!(ordinal_suffix(4), "th");
/// ```
pub fn ordinal_suffix(number: i64) -> &'static str {
    match number % 100 {
        11..=13 => "th",
        _ => match number % 10 {
            1 => "st",
            2 => "nd",
            3 => "rd",
            _ => "th",
        },
    }
}

/// Formats a relative time from a timestamp.
///
/// # Arguments
/// * `timestamp` - Unix timestamp in seconds
///
/// # Returns
/// A string like "3 hours ago" or "in 2 days"
///
/// # Examples
/// ```
/// use human_readable_utils::format_relative_time;
///
/// let now = std::time::SystemTime::now()
///     .duration_since(std::time::UNIX_EPOCH)
///     .unwrap()
///     .as_secs();
///
/// // Past time
/// assert!(format_relative_time(now - 3600).contains("ago"));
///
/// // Future time
/// assert!(format_relative_time(now + 7200).starts_with("in"));
/// ```
pub fn format_relative_time(timestamp: u64) -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);

    if timestamp > now {
        let diff = timestamp - now;
        format_relative_future(diff)
    } else {
        let diff = now - timestamp;
        format_relative_past(diff)
    }
}

/// Formats a duration as a future time string.
///
/// # Examples
/// ```
/// use human_readable_utils::format_relative_future;
///
/// assert_eq!(format_relative_future(30), "in 30 seconds");
/// assert_eq!(format_relative_future(60), "in 1 minute");
/// assert_eq!(format_relative_future(3600), "in 1 hour");
/// ```
pub fn format_relative_future(seconds: u64) -> String {
    let (value, unit) = get_relative_unit(seconds);
    format!("in {} {}", value, unit)
}

/// Formats a duration as a past time string.
///
/// # Examples
/// ```
/// use human_readable_utils::format_relative_past;
///
/// assert_eq!(format_relative_past(30), "30 seconds ago");
/// assert_eq!(format_relative_past(60), "1 minute ago");
/// assert_eq!(format_relative_past(3600), "1 hour ago");
/// ```
pub fn format_relative_past(seconds: u64) -> String {
    let (value, unit) = get_relative_unit(seconds);
    format!("{} {} ago", value, unit)
}

/// Gets the appropriate unit and value for a relative time.
fn get_relative_unit(seconds: u64) -> (u64, &'static str) {
    let units: [(u64, &str, &str); 6] = [
        (365 * 24 * 60 * 60, "year", "years"),
        (30 * 24 * 60 * 60, "month", "months"),
        (24 * 60 * 60, "day", "days"),
        (60 * 60, "hour", "hours"),
        (60, "minute", "minutes"),
        (1, "second", "seconds"),
    ];

    for (divisor, singular, plural) in units.iter() {
        if seconds >= *divisor {
            let value = seconds / divisor;
            let unit = if value == 1 { *singular } else { *plural };
            return (value, unit);
        }
    }

    (seconds, "seconds")
}

/// Formats a number in scientific notation.
///
/// # Examples
/// ```
/// use human_readable_utils::format_scientific;
///
/// assert_eq!(format_scientific(1234567.0, 2), "1.23e6");
/// assert_eq!(format_scientific(0.000123, 2), "1.23e-4");
/// ```
pub fn format_scientific(number: f64, precision: usize) -> String {
    format!("{:.*e}", precision, number)
}

/// Parses a human-readable byte string back to bytes.
///
/// # Examples
/// ```
/// use human_readable_utils::parse_bytes;
///
/// assert_eq!(parse_bytes("1KB"), Some(1024));
/// assert_eq!(parse_bytes("1.5 MB"), Some(1572864));
/// assert_eq!(parse_bytes("2 GB"), Some(2147483648));
/// ```
pub fn parse_bytes(s: &str) -> Option<u64> {
    let s_trimmed = s.trim();
    let s_upper = s_trimmed.to_uppercase();
    
    // First, check for unit suffixes
    for (i, unit) in BYTE_UNITS.iter().enumerate() {
        // Skip "B" unit - we'll handle plain numbers separately
        if i == 0 {
            continue;
        }
        
        let unit_upper = unit.to_uppercase();
        if s_upper.ends_with(&unit_upper) || s_upper.ends_with(&format!(" {}", unit_upper)) {
            // Find the position where the unit starts and extract the number part
            let suffix_pos = s_upper.rfind(&unit_upper).unwrap();
            let num_str = s_trimmed[..suffix_pos].trim_end_matches(' ').trim();
            let num: f64 = num_str.parse().ok()?;
            let multiplier = 1024_u64.pow(i as u32);
            return Some((num * multiplier as f64) as u64);
        }
    }
    
    // Check for explicit "B" suffix (like "500B")
    if s_upper.ends_with(" B") {
        let num_str = s_trimmed[..s_trimmed.len()-2].trim();
        return num_str.parse().ok();
    }
    if s_upper.ends_with("B") && s_upper.len() > 1 && !s_upper.ends_with("KB") 
        && !s_upper.ends_with("MB") && !s_upper.ends_with("GB") 
        && !s_upper.ends_with("TB") && !s_upper.ends_with("PB")
        && !s_upper.ends_with("EB") && !s_upper.ends_with("ZB")
        && !s_upper.ends_with("YB") {
        let num_str = s_trimmed[..s_trimmed.len()-1].trim();
        return num_str.parse().ok();
    }
    
    // Try parsing as plain number (bytes)
    s_trimmed.parse().ok()
}

/// Formats a frequency in Hz to human-readable form.
///
/// # Examples
/// ```
/// use human_readable_utils::format_frequency;
///
/// assert_eq!(format_frequency(1000), "1.00 kHz");
/// assert_eq!(format_frequency(1000000), "1.00 MHz");
/// assert_eq!(format_frequency(2500000), "2.50 MHz");
/// ```
pub fn format_frequency(hz: u64) -> String {
    const UNITS: [&str; 7] = ["Hz", "kHz", "MHz", "GHz", "THz", "PHz", "EHz"];
    
    if hz == 0 {
        return "0 Hz".to_string();
    }

    let mut size = hz as f64;
    let mut unit_index = 0;

    while size >= 1000.0 && unit_index < UNITS.len() - 1 {
        size /= 1000.0;
        unit_index += 1;
    }

    if unit_index == 0 {
        format!("{} {}", hz, UNITS[0])
    } else {
        format!("{:.2} {}", size, UNITS[unit_index])
    }
}

/// Formats a number as a percentage.
///
/// # Examples
/// ```
/// use human_readable_utils::format_percentage;
///
/// assert_eq!(format_percentage(0.123, 1), "12.3%");
/// assert_eq!(format_percentage(0.5, 0), "50%");
/// assert_eq!(format_percentage(1.0, 2), "100.00%");
/// ```
pub fn format_percentage(value: f64, precision: usize) -> String {
    format!("{:.*}%", precision, value * 100.0)
}

/// Formats a ratio as a simplified fraction.
///
/// # Examples
/// ```
/// use human_readable_utils::format_ratio;
///
/// assert_eq!(format_ratio(0.5, 100), "1/2");
/// assert_eq!(format_ratio(0.25, 100), "1/4");
/// assert_eq!(format_ratio(0.75, 100), "3/4");
/// assert_eq!(format_ratio(0.333, 100), "1/3");
/// ```
pub fn format_ratio(value: f64, max_denominator: u64) -> String {
    if value == 0.0 {
        return "0".to_string();
    }
    if value == 1.0 {
        return "1".to_string();
    }

    // Find the best fraction using Farey sequence approach
    let mut best_num = 1;
    let mut best_den = 1;
    let mut best_error = (value - 1.0).abs();

    for den in 2..=max_denominator {
        let num = (value * den as f64).round() as u64;
        if num == 0 || num > den {
            continue;
        }
        let error = (value - num as f64 / den as f64).abs();
        if error < best_error {
            best_error = error;
            best_num = num;
            best_den = den;
        }
    }

    // Simplify the fraction
    let gcd = gcd(best_num, best_den);
    let num = best_num / gcd;
    let den = best_den / gcd;

    if den == 1 {
        num.to_string()
    } else {
        format!("{}/{}", num, den)
    }
}

/// Calculates the greatest common divisor.
fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

/// Formats a count with its plural form.
///
/// # Examples
/// ```
/// use human_readable_utils::format_plural;
///
/// assert_eq!(format_plural(1, "item", None), "1 item");
/// assert_eq!(format_plural(2, "item", None), "2 items");
/// assert_eq!(format_plural(5, "child", Some("children")), "5 children");
/// ```
pub fn format_plural(count: u64, singular: &str, plural: Option<&str>) -> String {
    if count == 1 {
        format!("1 {}", singular)
    } else {
        let default_plural = format!("{}s", singular);
        let plural_form = plural.unwrap_or(&default_plural);
        format!("{} {}", count, plural_form)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(0), "0 B");
        assert_eq!(format_bytes(500), "500 B");
        assert_eq!(format_bytes(1024), "1.00 KB");
        assert_eq!(format_bytes(1536), "1.50 KB");
        assert_eq!(format_bytes(1048576), "1.00 MB");
        assert_eq!(format_bytes(1073741824), "1.00 GB");
    }

    #[test]
    fn test_format_bytes_with_precision() {
        assert_eq!(format_bytes_with_precision(1536, 0), "2 KB");
        assert_eq!(format_bytes_with_precision(1536, 1), "1.5 KB");
        assert_eq!(format_bytes_with_precision(1536, 3), "1.500 KB");
    }

    #[test]
    fn test_format_duration() {
        assert_eq!(format_duration(0), "0s");
        assert_eq!(format_duration(1), "1s");
        assert_eq!(format_duration(59), "59s");
        assert_eq!(format_duration(60), "1m");
        assert_eq!(format_duration(61), "1m 1s");
        assert_eq!(format_duration(3600), "1h");
        assert_eq!(format_duration(3661), "1h 1m 1s");
        assert_eq!(format_duration(86400), "1d");
        assert_eq!(format_duration(90061), "1d 1h 1m 1s");
        assert_eq!(format_duration(31536000), "1y");
    }

    #[test]
    fn test_format_duration_long() {
        assert_eq!(format_duration_long(0), "0 seconds");
        assert_eq!(format_duration_long(1), "1 second");
        assert_eq!(format_duration_long(2), "2 seconds");
        assert_eq!(format_duration_long(60), "1 minute");
        assert_eq!(format_duration_long(61), "1 minute 1 second");
        assert_eq!(format_duration_long(3661), "1 hour 1 minute 1 second");
    }

    #[test]
    fn test_format_number() {
        assert_eq!(format_number(0, ','), "0");
        assert_eq!(format_number(100, ','), "100");
        assert_eq!(format_number(1000, ','), "1,000");
        assert_eq!(format_number(10000, ','), "10,000");
        assert_eq!(format_number(100000, ','), "100,000");
        assert_eq!(format_number(1000000, ','), "1,000,000");
        assert_eq!(format_number(-1000, ','), "-1,000");
        assert_eq!(format_number(1234567, '_'), "1_234_567");
    }

    #[test]
    fn test_format_ordinal() {
        assert_eq!(format_ordinal(1), "1st");
        assert_eq!(format_ordinal(2), "2nd");
        assert_eq!(format_ordinal(3), "3rd");
        assert_eq!(format_ordinal(4), "4th");
        assert_eq!(format_ordinal(10), "10th");
        assert_eq!(format_ordinal(11), "11th");
        assert_eq!(format_ordinal(12), "12th");
        assert_eq!(format_ordinal(13), "13th");
        assert_eq!(format_ordinal(14), "14th");
        assert_eq!(format_ordinal(21), "21st");
        assert_eq!(format_ordinal(22), "22nd");
        assert_eq!(format_ordinal(23), "23rd");
        assert_eq!(format_ordinal(24), "24th");
        assert_eq!(format_ordinal(101), "101st");
        assert_eq!(format_ordinal(111), "111th");
        assert_eq!(format_ordinal(121), "121st");
    }

    #[test]
    fn test_format_relative_past() {
        assert_eq!(format_relative_past(1), "1 second ago");
        assert_eq!(format_relative_past(30), "30 seconds ago");
        assert_eq!(format_relative_past(60), "1 minute ago");
        assert_eq!(format_relative_past(3600), "1 hour ago");
        assert_eq!(format_relative_past(86400), "1 day ago");
    }

    #[test]
    fn test_format_relative_future() {
        assert_eq!(format_relative_future(1), "in 1 second");
        assert_eq!(format_relative_future(30), "in 30 seconds");
        assert_eq!(format_relative_future(60), "in 1 minute");
        assert_eq!(format_relative_future(3600), "in 1 hour");
        assert_eq!(format_relative_future(86400), "in 1 day");
    }

    #[test]
    fn test_parse_bytes() {
        assert_eq!(parse_bytes("1024"), Some(1024));
        assert_eq!(parse_bytes("1KB"), Some(1024));
        assert_eq!(parse_bytes("1 KB"), Some(1024));
        assert_eq!(parse_bytes("1.5 KB"), Some(1536));
        assert_eq!(parse_bytes("2MB"), Some(2097152));
        assert_eq!(parse_bytes("1GB"), Some(1073741824));
    }

    #[test]
    fn test_format_frequency() {
        assert_eq!(format_frequency(100), "100 Hz");
        assert_eq!(format_frequency(1000), "1.00 kHz");
        assert_eq!(format_frequency(1500), "1.50 kHz");
        assert_eq!(format_frequency(1000000), "1.00 MHz");
    }

    #[test]
    fn test_format_percentage() {
        assert_eq!(format_percentage(0.5, 0), "50%");
        assert_eq!(format_percentage(0.123, 1), "12.3%");
        assert_eq!(format_percentage(0.12345, 2), "12.35%");
    }

    #[test]
    fn test_format_ratio() {
        assert_eq!(format_ratio(0.5, 100), "1/2");
        assert_eq!(format_ratio(0.25, 100), "1/4");
        assert_eq!(format_ratio(0.75, 100), "3/4");
        assert_eq!(format_ratio(0.333, 100), "1/3");
    }

    #[test]
    fn test_format_plural() {
        assert_eq!(format_plural(1, "item", None), "1 item");
        assert_eq!(format_plural(2, "item", None), "2 items");
        assert_eq!(format_plural(5, "child", Some("children")), "5 children");
    }

    #[test]
    fn test_format_scientific() {
        assert_eq!(format_scientific(1234567.0, 2), "1.23e6");
        assert_eq!(format_scientific(0.000123, 2), "1.23e-4");
    }

    #[test]
    fn test_format_float() {
        assert_eq!(format_float(1234567.89, 2, ','), "1,234,567.89");
        assert_eq!(format_float(1234.5, 1, ','), "1,234.5");
        assert_eq!(format_float(-1234.5, 1, ','), "-1,234.5");
    }
}