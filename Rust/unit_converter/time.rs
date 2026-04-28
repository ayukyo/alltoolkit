//! Time unit conversions
//!
//! Provides conversions between various time units.

use crate::round_to;

/// Represents a time duration value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Time {
    /// The time in seconds (base unit)
    seconds: f64,
}

impl Time {
    // Constructors from various units
    
    /// Creates a Time from seconds
    pub fn from_seconds(s: f64) -> Self {
        Self { seconds: s }
    }
    
    /// Creates a Time from milliseconds
    pub fn from_milliseconds(ms: f64) -> Self {
        Self { seconds: ms / 1000.0 }
    }
    
    /// Creates a Time from microseconds
    pub fn from_microseconds(us: f64) -> Self {
        Self { seconds: us / 1_000_000.0 }
    }
    
    /// Creates a Time from nanoseconds
    pub fn from_nanoseconds(ns: f64) -> Self {
        Self { seconds: ns / 1_000_000_000.0 }
    }
    
    /// Creates a Time from minutes
    pub fn from_minutes(min: f64) -> Self {
        Self { seconds: min * 60.0 }
    }
    
    /// Creates a Time from hours
    pub fn from_hours(h: f64) -> Self {
        Self { seconds: h * 3600.0 }
    }
    
    /// Creates a Time from days
    pub fn from_days(d: f64) -> Self {
        Self { seconds: d * 86400.0 }
    }
    
    /// Creates a Time from weeks
    pub fn from_weeks(w: f64) -> Self {
        Self { seconds: w * 604800.0 }
    }
    
    /// Creates a Time from months (approximate, 30.44 days)
    pub fn from_months(m: f64) -> Self {
        Self { seconds: m * 2_629_746.0 }
    }
    
    /// Creates a Time from years (approximate, 365.25 days)
    pub fn from_years(y: f64) -> Self {
        Self { seconds: y * 31_557_600.0 }
    }
    
    /// Creates a Time from decades
    pub fn from_decades(d: f64) -> Self {
        Self { seconds: d * 315_576_000.0 }
    }
    
    /// Creates a Time from centuries
    pub fn from_centuries(c: f64) -> Self {
        Self { seconds: c * 3_155_760_000.0 }
    }
    
    /// Creates a Time from milliseconds (alias)
    pub fn from_ms(ms: f64) -> Self {
        Self::from_milliseconds(ms)
    }
    
    /// Creates a Time from microseconds (alias)
    pub fn from_us(us: f64) -> Self {
        Self::from_microseconds(us)
    }
    
    /// Creates a Time from nanoseconds (alias)
    pub fn from_ns(ns: f64) -> Self {
        Self::from_nanoseconds(ns)
    }
    
    // Conversion methods to various units
    
    /// Converts to seconds
    pub fn to_seconds(&self) -> f64 {
        self.seconds
    }
    
    /// Converts to milliseconds
    pub fn to_milliseconds(&self) -> f64 {
        self.seconds * 1000.0
    }
    
    /// Converts to microseconds
    pub fn to_microseconds(&self) -> f64 {
        self.seconds * 1_000_000.0
    }
    
    /// Converts to nanoseconds
    pub fn to_nanoseconds(&self) -> f64 {
        self.seconds * 1_000_000_000.0
    }
    
    /// Converts to minutes
    pub fn to_minutes(&self) -> f64 {
        self.seconds / 60.0
    }
    
    /// Converts to hours
    pub fn to_hours(&self) -> f64 {
        self.seconds / 3600.0
    }
    
    /// Converts to days
    pub fn to_days(&self) -> f64 {
        self.seconds / 86400.0
    }
    
    /// Converts to weeks
    pub fn to_weeks(&self) -> f64 {
        self.seconds / 604800.0
    }
    
    /// Converts to months (approximate)
    pub fn to_months(&self) -> f64 {
        self.seconds / 2_629_746.0
    }
    
    /// Converts to years (approximate)
    pub fn to_years(&self) -> f64 {
        self.seconds / 31_557_600.0
    }
    
    /// Converts to decades
    pub fn to_decades(&self) -> f64 {
        self.seconds / 315_576_000.0
    }
    
    /// Converts to centuries
    pub fn to_centuries(&self) -> f64 {
        self.seconds / 3_155_760_000.0
    }
    
    /// Converts to milliseconds (alias)
    pub fn to_ms(&self) -> f64 {
        self.to_milliseconds()
    }
    
    /// Converts to microseconds (alias)
    pub fn to_us(&self) -> f64 {
        self.to_microseconds()
    }
    
    /// Converts to nanoseconds (alias)
    pub fn to_ns(&self) -> f64 {
        self.to_nanoseconds()
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            seconds: round_to(self.seconds, decimals),
        }
    }
    
    /// Formats the time as a human-readable string
    pub fn format_human(&self) -> String {
        let total_seconds = self.seconds;
        
        if total_seconds < 0.001 {
            format!("{:.2} µs", self.to_microseconds())
        } else if total_seconds < 1.0 {
            format!("{:.2} ms", self.to_milliseconds())
        } else if total_seconds < 60.0 {
            format!("{:.2} s", self.seconds)
        } else if total_seconds < 3600.0 {
            let minutes = (total_seconds / 60.0).floor() as i32;
            let seconds = (total_seconds % 60.0) as i32;
            format!("{}m {}s", minutes, seconds)
        } else if total_seconds < 86400.0 {
            let hours = (total_seconds / 3600.0).floor() as i32;
            let minutes = ((total_seconds % 3600.0) / 60.0).floor() as i32;
            format!("{}h {}m", hours, minutes)
        } else if total_seconds < 604800.0 {
            let days = (total_seconds / 86400.0).floor() as i32;
            let hours = ((total_seconds % 86400.0) / 3600.0).floor() as i32;
            format!("{}d {}h", days, hours)
        } else {
            let weeks = (total_seconds / 604800.0).floor() as i32;
            let days = ((total_seconds % 604800.0) / 86400.0).floor() as i32;
            format!("{}w {}d", weeks, days)
        }
    }
}

impl Default for Time {
    fn default() -> Self {
        Self { seconds: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_seconds_to_milliseconds() {
        let time = Time::from_seconds(1.0);
        assert!((time.to_milliseconds() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_minutes_to_seconds() {
        let time = Time::from_minutes(1.0);
        assert!((time.to_seconds() - 60.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_hours_to_minutes() {
        let time = Time::from_hours(1.0);
        assert!((time.to_minutes() - 60.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_days_to_hours() {
        let time = Time::from_days(1.0);
        assert!((time.to_hours() - 24.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_weeks_to_days() {
        let time = Time::from_weeks(1.0);
        assert!((time.to_days() - 7.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_years_to_days() {
        let time = Time::from_years(1.0);
        assert!((time.to_days() - 365.25).abs() < 0.01);
    }
    
    #[test]
    fn test_nanoseconds_to_seconds() {
        let time = Time::from_nanoseconds(1_000_000_000.0);
        assert!((time.to_seconds() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 123.456;
        let time = Time::from_hours(original);
        assert!((time.to_hours() - original).abs() < 0.0001);
    }
    
    #[test]
    fn test_format_human() {
        assert_eq!(Time::from_microseconds(500.0).format_human(), "500.00 µs");
        assert_eq!(Time::from_milliseconds(500.0).format_human(), "500.00 ms");
        assert_eq!(Time::from_seconds(30.0).format_human(), "30.00 s");
        assert_eq!(Time::from_minutes(5.0).format_human(), "5m 0s");
        assert_eq!(Time::from_hours(2.5).format_human(), "2h 30m");
    }
}