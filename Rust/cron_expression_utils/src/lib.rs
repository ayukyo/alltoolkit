//! Cron Expression Utilities
//!
//! A comprehensive tool for parsing, validating, and computing cron expressions.
//! Supports standard 5-field and 6-field (with seconds) cron formats.
//!
//! # Features
//!
//! - Parse cron expressions into structured format
//! - Validate cron expressions
//! - Calculate next execution times
//! - Support for special characters: `*`, `,`, `-`, `/`
//! - Zero external dependencies
//!
//! # Format
//!
//! ## 5-field format:
//! ```text
//! ┌───────────── minute (0-59)
//! │ ┌───────────── hour (0-23)
//! │ │ ┌───────────── day of month (1-31)
//! │ │ │ ┌───────────── month (1-12)
//! │ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
//! │ │ │ │ │
//! * * * * *
//! ```
//!
//! ## 6-field format (with seconds):
//! ```text
//! ┌───────────── second (0-59)
//! │ ┌───────────── minute (0-59)
//! │ │ ┌───────────── hour (0-23)
//! │ │ │ ┌───────────── day of month (1-31)
//! │ │ │ │ ┌───────────── month (1-12)
//! │ │ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
//! │ │ │ │ │ │
//! * * * * * *
//! ```

use std::collections::HashSet;
use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

/// Error type for cron expression parsing failures
#[derive(Debug, Clone, PartialEq)]
pub enum CronError {
    /// Invalid number of fields in expression
    InvalidFieldCount { expected: usize, got: usize },
    /// Invalid value in a field
    InvalidValue { field: String, value: String, reason: String },
    /// Invalid range specification
    InvalidRange { field: String, range: String },
    /// Invalid step value
    InvalidStep { field: String, step: String },
    /// No valid next run time found
    NoNextRunTime,
}

impl fmt::Display for CronError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CronError::InvalidFieldCount { expected, got } => {
                write!(f, "Invalid cron expression: expected {} fields, got {}", expected, got)
            }
            CronError::InvalidValue { field, value, reason } => {
                write!(f, "Invalid value '{}' for field {}: {}", value, field, reason)
            }
            CronError::InvalidRange { field, range } => {
                write!(f, "Invalid range '{}' for field {}", range, field)
            }
            CronError::InvalidStep { field, step } => {
                write!(f, "Invalid step '{}' for field {}", step, field)
            }
            CronError::NoNextRunTime => {
                write!(f, "Could not find next run time within 5 years")
            }
        }
    }
}

impl std::error::Error for CronError {}

/// Field definition: name, min value, max value
type FieldDef = (&'static str, u32, u32);

const FIVE_FIELD_DEFS: [FieldDef; 5] = [
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day_of_month", 1, 31),
    ("month", 1, 12),
    ("day_of_week", 0, 6),
];

const SIX_FIELD_DEFS: [FieldDef; 6] = [
    ("second", 0, 59),
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day_of_month", 1, 31),
    ("month", 1, 12),
    ("day_of_week", 0, 6),
];

/// Month name mappings
const MONTH_NAMES: [(&str, u32); 12] = [
    ("jan", 1), ("feb", 2), ("mar", 3), ("apr", 4),
    ("may", 5), ("jun", 6), ("jul", 7), ("aug", 8),
    ("sep", 9), ("oct", 10), ("nov", 11), ("dec", 12),
];

/// Day of week name mappings
const DOW_NAMES: [(&str, u32); 7] = [
    ("sun", 0), ("mon", 1), ("tue", 2), ("wed", 3),
    ("thu", 4), ("fri", 5), ("sat", 6),
];

/// Represents a parsed cron expression
#[derive(Debug, Clone)]
pub struct CronExpression {
    /// Original expression string
    pub original: String,
    /// Whether this expression includes seconds field
    pub has_seconds: bool,
    /// Parsed field values
    fields: CronFields,
}

/// Container for all cron fields
#[derive(Debug, Clone, Default)]
struct CronFields {
    second: HashSet<u32>,
    minute: HashSet<u32>,
    hour: HashSet<u32>,
    day_of_month: HashSet<u32>,
    month: HashSet<u32>,
    day_of_week: HashSet<u32>,
}

impl CronExpression {
    /// Parse a cron expression string
    ///
    /// # Arguments
    ///
    /// * `expression` - Cron expression string (5 or 6 fields)
    ///
    /// # Returns
    ///
    /// A parsed `CronExpression` on success, or a `CronError` on failure
    ///
    /// # Examples
    ///
    /// ```
    /// use cron_expression_utils::CronExpression;
    ///
    /// let cron = CronExpression::parse("0 0 * * *").unwrap();
    /// assert!(!cron.has_seconds);
    ///
    /// let cron_with_seconds = CronExpression::parse("0 0 0 * * *").unwrap();
    /// assert!(cron_with_seconds.has_seconds);
    /// ```
    pub fn parse(expression: &str) -> Result<Self, CronError> {
        let original = expression.trim().to_string();
        let parts: Vec<&str> = original.split_whitespace().collect();

        let (field_defs, has_seconds) = match parts.len() {
            5 => (&FIVE_FIELD_DEFS[..], false),
            6 => (&SIX_FIELD_DEFS[..], true),
            n => return Err(CronError::InvalidFieldCount {
                expected: 5,
                got: n,
            }),
        };

        let mut fields = CronFields::default();

        for (i, (name, min_val, max_val)) in field_defs.iter().enumerate() {
            let parsed = Self::parse_field(parts[i], *min_val, *max_val, name)?;
            
            match *name {
                "second" => fields.second = parsed,
                "minute" => fields.minute = parsed,
                "hour" => fields.hour = parsed,
                "day_of_month" => fields.day_of_month = parsed,
                "month" => fields.month = parsed,
                "day_of_week" => fields.day_of_week = parsed,
                _ => {}
            }
        }

        Ok(CronExpression {
            original,
            has_seconds,
            fields,
        })
    }

    /// Parse a single cron field into a set of valid values
    fn parse_field(
        field: &str,
        min_val: u32,
        max_val: u32,
        name: &str,
    ) -> Result<HashSet<u32>, CronError> {
        let mut values = HashSet::new();
        
        // Handle special names for month and day of week
        let field_lower = field.to_lowercase();
        let mut field_resolved = field_lower.clone();
        
        if name == "month" {
            for (month_name, month_num) in MONTH_NAMES {
                field_resolved = field_resolved.replace(month_name, &month_num.to_string());
            }
        } else if name == "day_of_week" {
            for (dow_name, dow_num) in DOW_NAMES {
                field_resolved = field_resolved.replace(dow_name, &dow_num.to_string());
            }
        }

        // Split by comma for multiple parts
        for part in field_resolved.split(',') {
            let part = part.trim();
            if part.is_empty() {
                continue;
            }

            // Check for step notation
            let (range_part, step) = if part.contains('/') {
                let parts: Vec<&str> = part.split('/').collect();
                if parts.len() != 2 {
                    return Err(CronError::InvalidStep {
                        field: name.to_string(),
                        step: part.to_string(),
                    });
                }
                let step: u32 = parts[1].parse().map_err(|_| CronError::InvalidStep {
                    field: name.to_string(),
                    step: parts[1].to_string(),
                })?;
                if step == 0 {
                    return Err(CronError::InvalidStep {
                        field: name.to_string(),
                        step: "0".to_string(),
                    });
                }
                (parts[0], step)
            } else {
                (part, 1)
            };

            // Determine range
            let (start, end) = if range_part == "*" {
                (min_val, max_val)
            } else if range_part.contains('-') {
                let parts: Vec<&str> = range_part.split('-').collect();
                if parts.len() != 2 {
                    return Err(CronError::InvalidRange {
                        field: name.to_string(),
                        range: range_part.to_string(),
                    });
                }
                let start: u32 = parts[0].parse().map_err(|_| CronError::InvalidValue {
                    field: name.to_string(),
                    value: parts[0].to_string(),
                    reason: "not a valid number".to_string(),
                })?;
                let end: u32 = parts[1].parse().map_err(|_| CronError::InvalidValue {
                    field: name.to_string(),
                    value: parts[1].to_string(),
                    reason: "not a valid number".to_string(),
                })?;
                (start, end)
            } else {
                let val: u32 = range_part.parse().map_err(|_| CronError::InvalidValue {
                    field: name.to_string(),
                    value: range_part.to_string(),
                    reason: "not a valid number".to_string(),
                })?;
                (val, val)
            };

            // Validate range
            if start < min_val || start > max_val {
                return Err(CronError::InvalidValue {
                    field: name.to_string(),
                    value: start.to_string(),
                    reason: format!("out of range [{}, {}]", min_val, max_val),
                });
            }
            if end < min_val || end > max_val {
                return Err(CronError::InvalidValue {
                    field: name.to_string(),
                    value: end.to_string(),
                    reason: format!("out of range [{}, {}]", min_val, max_val),
                });
            }
            if end < start {
                return Err(CronError::InvalidRange {
                    field: name.to_string(),
                    range: format!("{}-{}", start, end),
                });
            }

            // Generate values with step
            for v in (start..=end).step_by(step as usize) {
                values.insert(v);
            }
        }

        Ok(values)
    }

    /// Check if a datetime matches the cron expression
    ///
    /// # Arguments
    ///
    /// * `second` - Second (0-59)
    /// * `minute` - Minute (0-59)
    /// * `hour` - Hour (0-23)
    /// * `day_of_month` - Day of month (1-31)
    /// * `month` - Month (1-12)
    /// * `day_of_week` - Day of week (0-6, 0=Sunday)
    ///
    /// # Returns
    ///
    /// `true` if the datetime matches, `false` otherwise
    pub fn matches(
        &self,
        second: u32,
        minute: u32,
        hour: u32,
        day_of_month: u32,
        month: u32,
        day_of_week: u32,
    ) -> bool {
        // Check seconds if 6-field format
        if self.has_seconds && !self.fields.second.contains(&second) {
            return false;
        }

        // Check other fields
        if !self.fields.minute.contains(&minute) {
            return false;
        }
        if !self.fields.hour.contains(&hour) {
            return false;
        }
        if !self.fields.month.contains(&month) {
            return false;
        }

        // Day matching is special - both day of month and day of week
        // if both are restricted (not *), OR logic applies
        let dom_all = self.fields.day_of_month.len() == 31;
        let dow_all = self.fields.day_of_week.len() == 7;

        let dom_matches = self.fields.day_of_month.contains(&day_of_month);
        let dow_matches = self.fields.day_of_week.contains(&day_of_week);

        if !dom_all && !dow_all {
            // Both restricted - OR logic
            if !dom_matches && !dow_matches {
                return false;
            }
        } else if !dom_all {
            if !dom_matches {
                return false;
            }
        } else if !dow_all {
            if !dow_matches {
                return false;
            }
        }

        true
    }

    /// Calculate the next execution time after a given timestamp
    ///
    /// # Arguments
    ///
    /// * `from_timestamp` - Unix timestamp to start from (0 for current time)
    ///
    /// # Returns
    ///
    /// Unix timestamp of the next execution time, or `CronError::NoNextRunTime`
    pub fn next_run(&self, from_timestamp: u64) -> Result<u64, CronError> {
        let from_ts = if from_timestamp == 0 {
            SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs()
        } else {
            from_timestamp
        };

        // Maximum search: 5 years (in seconds)
        let max_ts = from_ts + 5 * 365 * 24 * 60 * 60;

        // Start from next second/minute
        let mut current = if self.has_seconds {
            from_ts + 1
        } else {
            (from_ts / 60 + 1) * 60 // Round up to next minute
        };

        while current <= max_ts {
            if self.matches_timestamp(current) {
                return Ok(current);
            }
            current = if self.has_seconds {
                current + 1
            } else {
                current + 60
            };
        }

        Err(CronError::NoNextRunTime)
    }

    /// Calculate the next N execution times after a given timestamp
    ///
    /// # Arguments
    ///
    /// * `from_timestamp` - Unix timestamp to start from (0 for current time)
    /// * `count` - Number of future times to return
    ///
    /// # Returns
    ///
    /// Vector of Unix timestamps for next execution times
    pub fn next_runs(&self, from_timestamp: u64, count: usize) -> Result<Vec<u64>, CronError> {
        let mut runs = Vec::with_capacity(count);
        let mut current = from_timestamp;

        for _ in 0..count {
            let next = self.next_run(current)?;
            runs.push(next);
            current = next;
        }

        Ok(runs)
    }

    /// Check if a timestamp matches the cron expression
    fn matches_timestamp(&self, timestamp: u64) -> bool {
        let (second, minute, hour, day, month, day_of_week, _) = timestamp_to_components(timestamp);
        self.matches(second, minute, hour, day, month, day_of_week)
    }

    /// Get the field values as sorted vectors
    pub fn second_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.second.iter().copied().collect();
        v.sort();
        v
    }

    pub fn minute_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.minute.iter().copied().collect();
        v.sort();
        v
    }

    pub fn hour_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.hour.iter().copied().collect();
        v.sort();
        v
    }

    pub fn day_of_month_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.day_of_month.iter().copied().collect();
        v.sort();
        v
    }

    pub fn month_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.month.iter().copied().collect();
        v.sort();
        v
    }

    pub fn day_of_week_values(&self) -> Vec<u32> {
        let mut v: Vec<u32> = self.fields.day_of_week.iter().copied().collect();
        v.sort();
        v
    }

    /// Convert to a human-readable description
    pub fn to_human_readable(&self) -> String {
        let mut parts = Vec::new();

        // Seconds
        if self.has_seconds {
            let seconds = self.second_values();
            if seconds.len() == 60 {
                parts.push("every second".to_string());
            } else if seconds.len() == 1 {
                parts.push(format!("at second {}", seconds[0]));
            } else {
                parts.push(format!("at seconds {}", format_values(&seconds)));
            }
        }

        // Minutes
        let minutes = self.minute_values();
        if minutes.len() == 60 {
            if !self.has_seconds {
                parts.push("every minute".to_string());
            }
        } else if minutes.len() == 1 {
            parts.push(format!("at minute {}", minutes[0]));
        } else {
            parts.push(format!("at minutes {}", format_values(&minutes)));
        }

        // Hours
        let hours = self.hour_values();
        if hours.len() != 24 {
            if hours.len() == 1 {
                parts.push(format!("of hour {}", hours[0]));
            } else {
                parts.push(format!("of hours {}", format_values(&hours)));
            }
        }

        // Days of month
        let dom = self.day_of_month_values();
        let dom_restricted = dom.len() != 31;

        // Days of week
        let dow = self.day_of_week_values();
        let dow_restricted = dow.len() != 7;
        let dow_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

        if dom_restricted && dow_restricted {
            let dow_strs: Vec<String> = dow.iter().map(|&d| dow_names[d as usize].to_string()).collect();
            parts.push(format!("on day {} of month or on {}", format_values(&dom), dow_strs.join(", ")));
        } else if dom_restricted {
            if dom.len() == 1 {
                parts.push(format!("on day {} of month", dom[0]));
            } else {
                parts.push(format!("on days {} of month", format_values(&dom)));
            }
        } else if dow_restricted {
            let dow_strs: Vec<String> = dow.iter().map(|&d| dow_names[d as usize].to_string()).collect();
            parts.push(format!("on {}", dow_strs.join(", ")));
        }

        // Months
        let months = self.month_values();
        if months.len() != 12 {
            let month_names = ["January", "February", "March", "April", "May", "June",
                           "July", "August", "September", "October", "November", "December"];
            let month_strs: Vec<String> = months.iter().map(|&m| month_names[(m - 1) as usize].to_string()).collect();
            parts.push(format!("in {}", month_strs.join(", ")));
        }

        if parts.is_empty() {
            "every second".to_string()
        } else {
            parts.join(" ")
        }
    }
}

impl fmt::Display for CronExpression {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "CronExpression('{}')", self.original)
    }
}

/// Format a vector of values for display
fn format_values(values: &[u32]) -> String {
    values.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(", ")
}

/// Convert a Unix timestamp to time components
/// Returns (second, minute, hour, day, month, day_of_week, year)
fn timestamp_to_components(timestamp: u64) -> (u32, u32, u32, u32, u32, u32, u32) {
    // Simple implementation without external dependencies
    // Days since Unix epoch
    let total_days = timestamp / 86400;
    let remaining = timestamp % 86400;
    
    let hour = (remaining / 3600) as u32;
    let minute = ((remaining % 3600) / 60) as u32;
    let second = (remaining % 60) as u32;
    
    // Calculate date (simplified, works for years 1970-2099)
    let mut year = 1970u32;
    let mut days_remaining = total_days;
    
    loop {
        let days_in_year = if is_leap_year(year) { 366 } else { 365 };
        if days_remaining < days_in_year as u64 {
            break;
        }
        days_remaining -= days_in_year as u64;
        year += 1;
    }
    
    let (month, day) = days_to_month_day(days_remaining as u32, is_leap_year(year));
    
    // Calculate day of week (0 = Sunday)
    // Unix epoch (1970-01-01) was a Thursday (4)
    let day_of_week = ((total_days + 4) % 7) as u32;
    
    (second, minute, hour, day, month, day_of_week, year)
}

/// Check if a year is a leap year
fn is_leap_year(year: u32) -> bool {
    (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
}

/// Convert days since start of year to (month, day)
fn days_to_month_day(days: u32, leap: bool) -> (u32, u32) {
    let days_in_month = if leap {
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    } else {
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    };
    
    let mut remaining = days;
    for (i, &days) in days_in_month.iter().enumerate() {
        if remaining < days {
            return ((i + 1) as u32, remaining + 1);
        }
        remaining -= days;
    }
    
    (12, 31)
}

/// Validate a cron expression
///
/// # Arguments
///
/// * `expression` - Cron expression string
///
/// # Returns
///
/// `Ok(())` if valid, `Err(CronError)` if invalid
pub fn validate(expression: &str) -> Result<(), CronError> {
    CronExpression::parse(expression)?;
    Ok(())
}

/// Get the next run time for a cron expression
///
/// # Arguments
///
/// * `expression` - Cron expression string
/// * `from_timestamp` - Unix timestamp to start from (0 for current time)
///
/// # Returns
///
/// Unix timestamp of the next execution time
pub fn next_run(expression: &str, from_timestamp: u64) -> Result<u64, CronError> {
    let cron = CronExpression::parse(expression)?;
    cron.next_run(from_timestamp)
}

/// Get the next N run times for a cron expression
///
/// # Arguments
///
/// * `expression` - Cron expression string
/// * `from_timestamp` - Unix timestamp to start from (0 for current time)
/// * `count` - Number of future times to return
///
/// # Returns
///
/// Vector of Unix timestamps
pub fn next_runs(expression: &str, from_timestamp: u64, count: usize) -> Result<Vec<u64>, CronError> {
    let cron = CronExpression::parse(expression)?;
    cron.next_runs(from_timestamp, count)
}

/// Common cron presets
pub const PRESETS: &[(&str, &str)] = &[
    ("every_minute", "* * * * *"),
    ("every_hour", "0 * * * *"),
    ("every_day", "0 0 * * *"),
    ("every_week", "0 0 * * 0"),
    ("every_month", "0 0 1 * *"),
    ("every_year", "0 0 1 1 *"),
    ("every_5_minutes", "*/5 * * * *"),
    ("every_15_minutes", "*/15 * * * *"),
    ("every_30_minutes", "*/30 * * * *"),
    ("every_6_hours", "0 */6 * * *"),
    ("every_12_hours", "0 */12 * * *"),
    ("every_weekday", "0 0 * * 1-5"),
    ("every_weekend", "0 0 * * 0,6"),
];

/// Get a cron expression by preset name
///
/// # Arguments
///
/// * `preset_name` - Name of the preset (e.g., "every_hour")
///
/// # Returns
///
/// The cron expression string if found, or None
pub fn get_preset(preset_name: &str) -> Option<&'static str> {
    PRESETS.iter()
        .find(|(name, _)| name.eq_ignore_ascii_case(preset_name))
        .map(|(_, expr)| *expr)
}

/// List all available cron presets
pub fn list_presets() -> Vec<(&'static str, &'static str)> {
    PRESETS.to_vec()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_basic() {
        let cron = CronExpression::parse("* * * * *").unwrap();
        assert!(!cron.has_seconds);
        assert_eq!(cron.original, "* * * * *");
    }

    #[test]
    fn test_parse_with_seconds() {
        let cron = CronExpression::parse("0 0 0 * * *").unwrap();
        assert!(cron.has_seconds);
    }

    #[test]
    fn test_parse_invalid_field_count() {
        let result = CronExpression::parse("* * *");
        assert!(matches!(result, Err(CronError::InvalidFieldCount { .. })));
    }

    #[test]
    fn test_parse_asterisk() {
        let cron = CronExpression::parse("* * * * *").unwrap();
        assert_eq!(cron.minute_values().len(), 60);
        assert_eq!(cron.hour_values().len(), 24);
        assert_eq!(cron.day_of_month_values().len(), 31);
        assert_eq!(cron.month_values().len(), 12);
        assert_eq!(cron.day_of_week_values().len(), 7);
    }

    #[test]
    fn test_parse_specific_values() {
        let cron = CronExpression::parse("30 14 * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![30]);
        assert_eq!(cron.hour_values(), vec![14]);
    }

    #[test]
    fn test_parse_range() {
        let cron = CronExpression::parse("0 9-17 * * *").unwrap();
        assert_eq!(cron.hour_values(), vec![9, 10, 11, 12, 13, 14, 15, 16, 17]);
    }

    #[test]
    fn test_parse_list() {
        let cron = CronExpression::parse("0,15,30,45 * * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![0, 15, 30, 45]);
    }

    #[test]
    fn test_parse_step() {
        let cron = CronExpression::parse("*/10 * * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![0, 10, 20, 30, 40, 50]);
    }

    #[test]
    fn test_parse_range_with_step() {
        let cron = CronExpression::parse("0-30/10 * * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![0, 10, 20, 30]);
    }

    #[test]
    fn test_parse_month_names() {
        let cron = CronExpression::parse("* * * jan-jun *").unwrap();
        assert_eq!(cron.month_values(), vec![1, 2, 3, 4, 5, 6]);
    }

    #[test]
    fn test_parse_day_names() {
        let cron = CronExpression::parse("* * * * mon-fri").unwrap();
        assert_eq!(cron.day_of_week_values(), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_invalid_value() {
        let result = CronExpression::parse("60 * * * *");
        assert!(matches!(result, Err(CronError::InvalidValue { .. })));
    }

    #[test]
    fn test_invalid_range() {
        let result = CronExpression::parse("10-5 * * * *");
        assert!(matches!(result, Err(CronError::InvalidRange { .. })));
    }

    #[test]
    fn test_invalid_step() {
        let result = CronExpression::parse("*/0 * * * *");
        assert!(matches!(result, Err(CronError::InvalidStep { .. })));
    }

    #[test]
    fn test_matches_basic() {
        let cron = CronExpression::parse("30 14 * * *").unwrap();
        // 14:30 on any day
        assert!(cron.matches(0, 30, 14, 15, 5, 3)); // May 15, Thursday
        assert!(!cron.matches(0, 31, 14, 15, 5, 3)); // Wrong minute
        assert!(!cron.matches(0, 30, 15, 15, 5, 3)); // Wrong hour
    }

    #[test]
    fn test_matches_every_minute() {
        let cron = CronExpression::parse("* * * * *").unwrap();
        // Should match any time
        assert!(cron.matches(30, 15, 10, 1, 6, 2));
        assert!(cron.matches(0, 0, 0, 1, 1, 0));
    }

    #[test]
    fn test_matches_day_of_week() {
        let cron = CronExpression::parse("* * * * 1-5").unwrap();
        // Weekdays only
        assert!(cron.matches(0, 0, 0, 1, 1, 1)); // Monday
        assert!(cron.matches(0, 0, 0, 1, 1, 5)); // Friday
        assert!(!cron.matches(0, 0, 0, 1, 1, 0)); // Sunday
        assert!(!cron.matches(0, 0, 0, 1, 1, 6)); // Saturday
    }

    #[test]
    fn test_matches_both_day_restricted() {
        // Both day of month and day of week restricted - OR logic
        let cron = CronExpression::parse("* * 1 * 1").unwrap();
        // Should match on 1st of month OR on Monday
        assert!(cron.matches(0, 0, 0, 1, 1, 1)); // 1st (Wednesday in 1970)
        assert!(cron.matches(0, 0, 0, 5, 1, 1)); // Monday Jan 5
        assert!(!cron.matches(0, 0, 0, 3, 1, 3)); // Not 1st, not Monday
    }

    #[test]
    fn test_next_run_every_minute() {
        let cron = CronExpression::parse("* * * * *").unwrap();
        // Use a fixed timestamp
        let ts: u64 = 1700000000; // 2023-11-14 22:13:20 UTC
        let next = cron.next_run(ts).unwrap();
        // Should be the next minute
        assert!(next > ts);
        assert!((next - ts) <= 60);
    }

    #[test]
    fn test_next_run_specific_time() {
        let cron = CronExpression::parse("0 12 * * *").unwrap();
        // Should find next noon
        let ts: u64 = 1700000000; // 2023-11-14 22:13:20 UTC
        let next = cron.next_run(ts).unwrap();
        
        // Verify it's at minute 0, hour 12
        let (sec, min, hour, _, _, _, _) = timestamp_to_components(next);
        assert_eq!(sec, 0);
        assert_eq!(min, 0);
        assert_eq!(hour, 12);
    }

    #[test]
    fn test_next_runs() {
        let cron = CronExpression::parse("0 * * * *").unwrap();
        let ts: u64 = 1700000000;
        let runs = cron.next_runs(ts, 3).unwrap();
        
        assert_eq!(runs.len(), 3);
        // Each run should be 1 hour apart
        assert!(runs[1] > runs[0]);
        assert!(runs[2] > runs[1]);
    }

    #[test]
    fn test_human_readable() {
        let cron = CronExpression::parse("0 12 * * *").unwrap();
        let desc = cron.to_human_readable();
        assert!(desc.contains("minute 0"));
        assert!(desc.contains("hour 12"));
    }

    #[test]
    fn test_human_readable_weekday() {
        let cron = CronExpression::parse("0 0 * * 1-5").unwrap();
        let desc = cron.to_human_readable();
        assert!(desc.contains("Monday") || desc.contains("Friday"));
    }

    #[test]
    fn test_validate() {
        assert!(validate("* * * * *").is_ok());
        assert!(validate("0 0 0 * * *").is_ok());
        assert!(validate("invalid").is_err());
    }

    #[test]
    fn test_get_preset() {
        assert_eq!(get_preset("every_hour"), Some("0 * * * *"));
        assert_eq!(get_preset("EVERY_HOUR"), Some("0 * * * *"));
        assert_eq!(get_preset("nonexistent"), None);
    }

    #[test]
    fn test_list_presets() {
        let presets = list_presets();
        assert!(!presets.is_empty());
        assert!(presets.iter().any(|(name, _)| *name == "every_minute"));
    }

    #[test]
    fn test_function_next_run() {
        let ts: u64 = 1700000000;
        let next = next_run("* * * * *", ts).unwrap();
        assert!(next > ts);
    }

    #[test]
    fn test_function_next_runs() {
        let ts: u64 = 1700000000;
        let runs = next_runs("0 * * * *", ts, 5).unwrap();
        assert_eq!(runs.len(), 5);
    }

    #[test]
    fn test_timestamp_to_components() {
        // 1970-01-01 00:00:00 UTC
        let (sec, min, hour, day, month, dow, year) = timestamp_to_components(0);
        assert_eq!(sec, 0);
        assert_eq!(min, 0);
        assert_eq!(hour, 0);
        assert_eq!(day, 1);
        assert_eq!(month, 1);
        assert_eq!(dow, 4); // Thursday
        assert_eq!(year, 1970);

        // 1970-01-02 00:00:00 UTC (86400 seconds)
        let (_, _, _, day2, month2, dow2, year2) = timestamp_to_components(86400);
        assert_eq!(day2, 2);
        assert_eq!(month2, 1);
        assert_eq!(dow2, 5); // Friday
        assert_eq!(year2, 1970);
    }

    #[test]
    fn test_complex_expressions() {
        // Every 5 minutes on weekdays
        let cron = CronExpression::parse("*/5 * * * 1-5").unwrap();
        assert_eq!(cron.minute_values(), vec![0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]);
        assert_eq!(cron.day_of_week_values(), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_every_15_minutes() {
        let cron = CronExpression::parse("*/15 * * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![0, 15, 30, 45]);
    }

    #[test]
    fn test_midnight_daily() {
        let cron = CronExpression::parse("0 0 * * *").unwrap();
        assert_eq!(cron.minute_values(), vec![0]);
        assert_eq!(cron.hour_values(), vec![0]);
    }

    #[test]
    fn test_first_of_month() {
        let cron = CronExpression::parse("0 0 1 * *").unwrap();
        assert_eq!(cron.day_of_month_values(), vec![1]);
    }

    #[test]
    fn test_six_field_expression() {
        let cron = CronExpression::parse("30 0 12 * * *").unwrap();
        assert!(cron.has_seconds);
        assert_eq!(cron.second_values(), vec![30]);
        assert_eq!(cron.minute_values(), vec![0]);
        assert_eq!(cron.hour_values(), vec![12]);
    }

    #[test]
    fn test_display() {
        let cron = CronExpression::parse("* * * * *").unwrap();
        assert_eq!(format!("{}", cron), "CronExpression('* * * * *')");
    }

    #[test]
    fn test_is_leap_year() {
        assert!(is_leap_year(2000));
        assert!(is_leap_year(2024));
        assert!(!is_leap_year(1900));
        assert!(!is_leap_year(2023));
    }

    #[test]
    fn test_days_to_month_day() {
        assert_eq!(days_to_month_day(0, false), (1, 1)); // Jan 1
        assert_eq!(days_to_month_day(31, false), (2, 1)); // Feb 1 (non-leap)
        assert_eq!(days_to_month_day(31, true), (2, 1)); // Feb 1 (leap)
        assert_eq!(days_to_month_day(58, false), (2, 28)); // Feb 28 (non-leap)
        assert_eq!(days_to_month_day(59, false), (3, 1)); // Mar 1 (non-leap: Jan 31 + Feb 28 = 59)
        assert_eq!(days_to_month_day(59, true), (2, 29)); // Feb 29 (leap)
        assert_eq!(days_to_month_day(60, true), (3, 1)); // Mar 1 (leap: Jan 31 + Feb 29 = 60)
    }
}