//! Date Utilities Module for Rust
//!
//! A zero-dependency date and time manipulation library.
//! Provides comprehensive date operations including parsing, formatting,
//! arithmetic, comparison, and range generation.
//!
//! # Features
//! - Zero dependencies, uses only Rust standard library
//! - Date parsing from multiple formats (YYYY-MM-DD, DD/MM/YYYY, etc.)
//! - Date formatting to various output formats
//! - Date arithmetic (add/subtract days, months, years)
//! - Date comparison (before, after, equal, between)
//! - Date information extraction (year, month, day, weekday, day of year)
//! - Timestamp conversion (Unix epoch seconds)
//! - Date range generation
//! - Leap year detection
//! - Days in month calculation
//! - UTC offset support
//!
//! # Example
//! ```rust
//! use date_utils::{Date, parse_date, format_date};
//!
//! // Parse a date
//! let date = parse_date("2024-03-15").unwrap();
//! println!("Year: {}, Month: {}, Day: {}", date.year(), date.month(), date.day());
//!
//! // Format a date
//! let formatted = format_date(&date, "YYYY-MM-DD");
//! println!("{}", formatted); // 2024-03-15
//!
//! // Date arithmetic
//! let future = date.add_days(30);
//! let past = date.subtract_months(1);
//!
//! // Compare dates
//! if date.is_before(&future) {
//!     println!("Today is before the future date");
//! }
//! ```

use std::fmt;
use std::ops::{Add, Sub};

/// Error type for date operations
#[derive(Debug, Clone, PartialEq)]
pub enum DateError {
    InvalidFormat { input: String, expected: String },
    InvalidDate { year: i32, month: u8, day: u8 },
    InvalidMonth { month: u8 },
    InvalidDay { year: i32, month: u8, day: u8 },
    ParseError { message: String },
    Custom(String),
}

impl fmt::Display for DateError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DateError::InvalidFormat { input, expected } => {
                write!(f, "Invalid date format: '{}' (expected: {})", input, expected)
            }
            DateError::InvalidDate { year, month, day } => {
                write!(f, "Invalid date: {}-{:02}-{:02}", year, month, day)
            }
            DateError::InvalidMonth { month } => {
                write!(f, "Invalid month: {} (must be 1-12)", month)
            }
            DateError::InvalidDay { year, month, day } => {
                write!(f, "Invalid day: {} for year {} month {}", day, year, month)
            }
            DateError::ParseError { message } => {
                write!(f, "Parse error: {}", message)
            }
            DateError::Custom(msg) => write!(f, "{}", msg),
        }
    }
}

impl std::error::Error for DateError {}

/// Result type for date operations
pub type DateResult<T> = Result<T, DateError>;

/// Day of week enumeration
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Weekday {
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday,
}

impl Weekday {
    /// Get the short name (Mon, Tue, etc.)
    pub fn short_name(&self) -> &'static str {
        match self {
            Weekday::Monday => "Mon",
            Weekday::Tuesday => "Tue",
            Weekday::Wednesday => "Wed",
            Weekday::Thursday => "Thu",
            Weekday::Friday => "Fri",
            Weekday::Saturday => "Sat",
            Weekday::Sunday => "Sun",
        }
    }

    /// Get the full name
    pub fn full_name(&self) -> &'static str {
        match self {
            Weekday::Monday => "Monday",
            Weekday::Tuesday => "Tuesday",
            Weekday::Wednesday => "Wednesday",
            Weekday::Thursday => "Thursday",
            Weekday::Friday => "Friday",
            Weekday::Saturday => "Saturday",
            Weekday::Sunday => "Sunday",
        }
    }

    /// Get the number (1-7, Monday=1)
    pub fn number(&self) -> u8 {
        match self {
            Weekday::Monday => 1,
            Weekday::Tuesday => 2,
            Weekday::Wednesday => 3,
            Weekday::Thursday => 4,
            Weekday::Friday => 5,
            Weekday::Saturday => 6,
            Weekday::Sunday => 7,
        }
    }
}

impl fmt::Display for Weekday {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.short_name())
    }
}

/// Month enumeration
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Month {
    January,
    February,
    March,
    April,
    May,
    June,
    July,
    August,
    September,
    October,
    November,
    December,
}

impl Month {
    /// Get the short name (Jan, Feb, etc.)
    pub fn short_name(&self) -> &'static str {
        match self {
            Month::January => "Jan",
            Month::February => "Feb",
            Month::March => "Mar",
            Month::April => "Apr",
            Month::May => "May",
            Month::June => "Jun",
            Month::July => "Jul",
            Month::August => "Aug",
            Month::September => "Sep",
            Month::October => "Oct",
            Month::November => "Nov",
            Month::December => "Dec",
        }
    }

    /// Get the full name
    pub fn full_name(&self) -> &'static str {
        match self {
            Month::January => "January",
            Month::February => "February",
            Month::March => "March",
            Month::April => "April",
            Month::May => "May",
            Month::June => "June",
            Month::July => "July",
            Month::August => "August",
            Month::September => "September",
            Month::October => "October",
            Month::November => "November",
            Month::December => "December",
        }
    }

    /// Get the number (1-12)
    pub fn number(&self) -> u8 {
        match self {
            Month::January => 1,
            Month::February => 2,
            Month::March => 3,
            Month::April => 4,
            Month::May => 5,
            Month::June => 6,
            Month::July => 7,
            Month::August => 8,
            Month::September => 9,
            Month::October => 10,
            Month::November => 11,
            Month::December => 12,
        }
    }

    /// Create from number (1-12)
    pub fn from_number(n: u8) -> Option<Month> {
        match n {
            1 => Some(Month::January),
            2 => Some(Month::February),
            3 => Some(Month::March),
            4 => Some(Month::April),
            5 => Some(Month::May),
            6 => Some(Month::June),
            7 => Some(Month::July),
            8 => Some(Month::August),
            9 => Some(Month::September),
            10 => Some(Month::October),
            11 => Some(Month::November),
            12 => Some(Month::December),
            _ => None,
        }
    }
}

impl fmt::Display for Month {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.short_name())
    }
}

/// Represents a calendar date
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Date {
    year: i32,
    month: u8,
    day: u8,
}

impl Date {
    /// Create a new date with validation
    pub fn new(year: i32, month: u8, day: u8) -> DateResult<Self> {
        if month < 1 || month > 12 {
            return Err(DateError::InvalidMonth { month });
        }
        
        let max_day = Self::days_in_month(year, month);
        if day < 1 || day > max_day {
            return Err(DateError::InvalidDay { year, month, day });
        }
        
        Ok(Date { year, month, day })
    }

    /// Create a new date without validation (use with caution)
    pub fn new_unchecked(year: i32, month: u8, day: u8) -> Self {
        Date { year, month, day }
    }

    /// Get today's date (based on system time)
    pub fn today() -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap();
        
        let days_since_epoch = (now.as_secs() / 86400) as i64;
        Self::from_days_since_epoch(days_since_epoch)
    }

    /// Get the year
    pub fn year(&self) -> i32 {
        self.year
    }

    /// Get the month (1-12)
    pub fn month(&self) -> u8 {
        self.month
    }

    /// Get the day (1-31)
    pub fn day(&self) -> u8 {
        self.day
    }

    /// Get the month as enum
    pub fn month_enum(&self) -> Month {
        Month::from_number(self.month).unwrap()
    }

    /// Get the day of week
    pub fn weekday(&self) -> Weekday {
        // Zeller's congruence for Gregorian calendar
        let q = self.day as i32;
        let mut m = self.month as i32;
        let mut y = self.year;
        
        if m < 3 {
            m += 12;
            y -= 1;
        }
        
        let k = y % 100;
        let j = y / 100;
        
        let h = (q + (13 * (m + 1)) / 5 + k + k / 4 + j / 4 - 2 * j) % 7;
        let h = ((h % 7) + 7) % 7; // Ensure positive
        
        // Convert Zeller result (0=Saturday) to Weekday (Monday=0)
        match h {
            0 => Weekday::Saturday,
            1 => Weekday::Sunday,
            2 => Weekday::Monday,
            3 => Weekday::Tuesday,
            4 => Weekday::Wednesday,
            5 => Weekday::Thursday,
            6 => Weekday::Friday,
            _ => unreachable!(),
        }
    }

    /// Get the day of year (1-366)
    pub fn day_of_year(&self) -> u16 {
        let days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        let mut day_of_year = self.day as u16;
        
        for i in 1..self.month as usize {
            day_of_year += days_in_months[i] as u16;
            if i == 2 && Self::is_leap_year(self.year) {
                day_of_year += 1;
            }
        }
        
        day_of_year
    }

    /// Check if the year is a leap year
    pub fn is_leap_year(year: i32) -> bool {
        (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
    }

    /// Check if this date's year is a leap year
    pub fn is_current_year_leap(&self) -> bool {
        Self::is_leap_year(self.year)
    }

    /// Get the number of days in a month
    pub fn days_in_month(year: i32, month: u8) -> u8 {
        match month {
            1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
            4 | 6 | 9 | 11 => 30,
            2 => {
                if Self::is_leap_year(year) {
                    29
                } else {
                    28
                }
            }
            _ => 28, // Default for invalid months
        }
    }

    /// Get the number of days in this date's month
    pub fn days_in_current_month(&self) -> u8 {
        Self::days_in_month(self.year, self.month)
    }

    /// Get the number of days in a year
    pub fn days_in_year(year: i32) -> u16 {
        if Self::is_leap_year(year) {
            366
        } else {
            365
        }
    }

    /// Convert to days since Unix epoch (1970-01-01)
    pub fn to_days_since_epoch(&self) -> i64 {
        let mut days = 0i64;
        
        // Days from years
        for y in 1970..self.year {
            days += Self::days_in_year(y) as i64;
        }
        for y in self.year..1970 {
            days -= Self::days_in_year(y) as i64;
        }
        
        // Days from months
        let days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        for m in 1..self.month {
            days += days_in_months[m as usize] as i64;
            if m == 2 && Self::is_leap_year(self.year) {
                days += 1;
            }
        }
        
        // Days from day of month
        days += (self.day - 1) as i64;
        
        days
    }

    /// Create from days since Unix epoch
    pub fn from_days_since_epoch(days: i64) -> Self {
        let mut remaining_days = days;
        let mut year = 1970;
        
        if remaining_days >= 0 {
            while remaining_days >= Self::days_in_year(year) as i64 {
                remaining_days -= Self::days_in_year(year) as i64;
                year += 1;
            }
        } else {
            while remaining_days < 0 {
                year -= 1;
                remaining_days += Self::days_in_year(year) as i64;
            }
        }
        
        let mut month = 1u8;
        let days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        
        while month < 12 {
            let days_in_current = days_in_months[month as usize] as i64
                + if month == 2 && Self::is_leap_year(year) { 1 } else { 0 };
            
            if remaining_days < days_in_current {
                break;
            }
            remaining_days -= days_in_current;
            month += 1;
        }
        
        let day = (remaining_days + 1) as u8;
        
        Date::new_unchecked(year, month, day)
    }

    /// Convert to Unix timestamp (seconds since epoch)
    pub fn to_timestamp(&self) -> i64 {
        self.to_days_since_epoch() * 86400
    }

    /// Create from Unix timestamp
    pub fn from_timestamp(timestamp: i64) -> Self {
        let days = timestamp / 86400;
        Self::from_days_since_epoch(days)
    }

    /// Add days to this date
    pub fn add_days(&self, days: i64) -> Self {
        let new_days = self.to_days_since_epoch() + days;
        Self::from_days_since_epoch(new_days)
    }

    /// Subtract days from this date
    pub fn subtract_days(&self, days: i64) -> Self {
        self.add_days(-days)
    }

    /// Add months to this date
    pub fn add_months(&self, months: i64) -> Self {
        let mut new_year = self.year;
        let mut new_month = self.month as i64 + months;
        
        while new_month > 12 {
            new_month -= 12;
            new_year += 1;
        }
        while new_month < 1 {
            new_month += 12;
            new_year -= 1;
        }
        
        let new_month = new_month as u8;
        let max_day = Self::days_in_month(new_year, new_month);
        let new_day = self.day.min(max_day);
        
        Date::new_unchecked(new_year, new_month, new_day)
    }

    /// Subtract months from this date
    pub fn subtract_months(&self, months: i64) -> Self {
        self.add_months(-months)
    }

    /// Add years to this date
    pub fn add_years(&self, years: i64) -> Self {
        let new_year = self.year + years as i32;
        let max_day = Self::days_in_month(new_year, self.month);
        let new_day = self.day.min(max_day);
        
        Date::new_unchecked(new_year, self.month, new_day)
    }

    /// Subtract years from this date
    pub fn subtract_years(&self, years: i64) -> Self {
        self.add_years(-years)
    }

    /// Check if this date is before another date
    pub fn is_before(&self, other: &Date) -> bool {
        self.to_days_since_epoch() < other.to_days_since_epoch()
    }

    /// Check if this date is after another date
    pub fn is_after(&self, other: &Date) -> bool {
        self.to_days_since_epoch() > other.to_days_since_epoch()
    }

    /// Check if this date is equal to another date
    pub fn is_equal(&self, other: &Date) -> bool {
        self.to_days_since_epoch() == other.to_days_since_epoch()
    }

    /// Check if this date is between two dates (inclusive)
    pub fn is_between(&self, start: &Date, end: &Date) -> bool {
        !self.is_before(start) && !self.is_after(end)
    }

    /// Get the first day of the month
    pub fn first_day_of_month(&self) -> Self {
        Date::new_unchecked(self.year, self.month, 1)
    }

    /// Get the last day of the month
    pub fn last_day_of_month(&self) -> Self {
        let last_day = Self::days_in_month(self.year, self.month);
        Date::new_unchecked(self.year, self.month, last_day)
    }

    /// Get the first day of the year
    pub fn first_day_of_year(&self) -> Self {
        Date::new_unchecked(self.year, 1, 1)
    }

    /// Get the last day of the year
    pub fn last_day_of_year(&self) -> Self {
        Date::new_unchecked(self.year, 12, 31)
    }

    /// Calculate the difference in days between two dates
    pub fn days_difference(&self, other: &Date) -> i64 {
        other.to_days_since_epoch() - self.to_days_since_epoch()
    }
}

impl fmt::Display for Date {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:04}-{:02}-{:02}", self.year, self.month, self.day)
    }
}

impl Add<i64> for Date {
    type Output = Self;

    fn add(self, days: i64) -> Self::Output {
        self.add_days(days)
    }
}

impl Sub<i64> for Date {
    type Output = Self;

    fn sub(self, days: i64) -> Self::Output {
        self.subtract_days(days)
    }
}

impl Sub for Date {
    type Output = i64;

    fn sub(self, other: Self) -> Self::Output {
        self.to_days_since_epoch() - other.to_days_since_epoch()
    }
}

/// Parse a date string in various formats
pub fn parse_date(input: &str) -> DateResult<Date> {
    let input = input.trim();
    
    // Try YYYY-MM-DD
    if let Ok(date) = parse_date_format(input, "%Y-%m-%d") {
        return Ok(date);
    }
    
    // Try YYYY/MM/DD
    if let Ok(date) = parse_date_format(input, "%Y/%m/%d") {
        return Ok(date);
    }
    
    // Try DD-MM-YYYY
    if let Ok(date) = parse_date_format(input, "%d-%m-%Y") {
        return Ok(date);
    }
    
    // Try DD/MM/YYYY
    if let Ok(date) = parse_date_format(input, "%d/%m/%Y") {
        return Ok(date);
    }
    
    // Try MM-DD-YYYY
    if let Ok(date) = parse_date_format(input, "%m-%d-%Y") {
        return Ok(date);
    }
    
    // Try MM/DD/YYYY
    if let Ok(date) = parse_date_format(input, "%m/%d/%Y") {
        return Ok(date);
    }
    
    // Try YYYYMMDD
    if input.len() == 8 && input.chars().all(|c| c.is_ascii_digit()) {
        let year: i32 = input[0..4].parse().map_err(|_| DateError::ParseError {
            message: format!("Invalid year in '{}'", input),
        })?;
        let month: u8 = input[4..6].parse().map_err(|_| DateError::ParseError {
            message: format!("Invalid month in '{}'", input),
        })?;
        let day: u8 = input[6..8].parse().map_err(|_| DateError::ParseError {
            message: format!("Invalid day in '{}'", input),
        })?;
        return Date::new(year, month, day);
    }
    
    Err(DateError::InvalidFormat {
        input: input.to_string(),
        expected: "YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY, MM-DD-YYYY, MM/DD/YYYY, or YYYYMMDD".to_string(),
    })
}

fn parse_date_format(input: &str, format: &str) -> DateResult<Date> {
    let parts: Vec<&str> = match format {
        "%Y-%m-%d" | "%d-%m-%Y" | "%m-%d-%Y" => input.split('-').collect(),
        "%Y/%m/%d" | "%d/%m/%Y" | "%m/%d/%Y" => input.split('/').collect(),
        _ => return Err(DateError::ParseError { message: "Unsupported format".to_string() }),
    };
    
    if parts.len() != 3 {
        return Err(DateError::ParseError {
            message: format!("Expected 3 parts, got {}", parts.len()),
        });
    }
    
    let (year_str, month_str, day_str) = match format {
        "%Y-%m-%d" | "%Y/%m/%d" => (parts[0], parts[1], parts[2]),
        "%d-%m-%Y" | "%d/%m/%Y" => (parts[2], parts[1], parts[0]),
        "%m-%d-%Y" | "%m/%d/%Y" => (parts[2], parts[0], parts[1]),
        _ => return Err(DateError::ParseError { message: "Unsupported format".to_string() }),
    };
    
    let year: i32 = year_str.parse().map_err(|_| DateError::ParseError {
        message: format!("Invalid year: '{}'", year_str),
    })?;
    
    let month: u8 = month_str.parse().map_err(|_| DateError::ParseError {
        message: format!("Invalid month: '{}'", month_str),
    })?;
    
    let day: u8 = day_str.parse().map_err(|_| DateError::ParseError {
        message: format!("Invalid day: '{}'", day_str),
    })?;
    
    Date::new(year, month, day)
}

/// Format a date to a string
/// 
/// Format specifiers:
/// - YYYY: 4-digit year, YY: 2-digit year
/// - MM: 2-digit month, M: 1-digit month
/// - MMMM: full month name, MMM: short month name
/// - DD: 2-digit day, D: 1-digit day
/// - DDD: day of year
/// - EEEE: full weekday name, EEE: short weekday name
/// - W: weekday number (1-7)
/// 
/// Use single quotes to escape literal text: 'Day' D 'of year'
pub fn format_date(date: &Date, format: &str) -> String {
    let mut result = String::new();
    let mut chars = format.chars().peekable();
    
    while let Some(c) = chars.next() {
        // Handle escaped text (single quotes)
        if c == '\'' {
            while let Some(&next) = chars.peek() {
                chars.next();
                if next == '\'' {
                    // Check for escaped quote ('')
                    if chars.peek() == Some(&'\'') {
                        result.push('\'');
                        chars.next();
                    } else {
                        break; // End of escaped text
                    }
                } else {
                    result.push(next);
                }
            }
            continue;
        }
        
        match c {
            'Y' => {
                let mut count = 1;
                while chars.peek() == Some(&'Y') {
                    count += 1;
                    chars.next();
                }
                if count >= 4 {
                    result.push_str(&format!("{:04}", date.year()));
                } else {
                    result.push_str(&format!("{:02}", date.year() % 100));
                }
            }
            'M' => {
                let mut count = 1;
                while chars.peek() == Some(&'M') {
                    count += 1;
                    chars.next();
                }
                if count >= 4 {
                    // MMMM = full month name
                    let month = date.month_enum();
                    result.push_str(month.full_name());
                } else if count >= 3 {
                    // MMM = short month name
                    let month = date.month_enum();
                    result.push_str(month.short_name());
                } else if count >= 2 {
                    // MM = two-digit month number
                    result.push_str(&format!("{:02}", date.month()));
                } else {
                    // M = one-digit month number
                    result.push_str(&format!("{}", date.month()));
                }
            }
            'd' => {
                let mut count = 1;
                while chars.peek() == Some(&'d') {
                    count += 1;
                    chars.next();
                }
                if count >= 2 {
                    result.push_str(&format!("{:02}", date.day()));
                } else {
                    result.push_str(&format!("{}", date.day()));
                }
            }
            'E' => {
                let mut count = 1;
                while chars.peek() == Some(&'E') {
                    count += 1;
                    chars.next();
                }
                let weekday = date.weekday();
                if count >= 4 {
                    result.push_str(weekday.full_name());
                } else {
                    result.push_str(weekday.short_name());
                }
            }
            'D' => {
                let mut count = 1;
                while chars.peek() == Some(&'D') {
                    count += 1;
                    chars.next();
                }
                if count >= 3 {
                    // DDD = day of year
                    result.push_str(&format!("{}", date.day_of_year()));
                } else {
                    // D or DD = day of month
                    if count >= 2 {
                        result.push_str(&format!("{:02}", date.day()));
                    } else {
                        result.push_str(&format!("{}", date.day()));
                    }
                }
            }
            'W' => {
                result.push_str(&format!("{}", date.weekday().number()));
            }
            c => result.push(c),
        }
    }
    
    result
}

/// Generate a range of dates
pub fn date_range(start: &Date, end: &Date) -> Vec<Date> {
    let mut dates = Vec::new();
    let mut current = *start;
    
    while !current.is_after(end) {
        dates.push(current);
        current = current.add_days(1);
    }
    
    dates
}

/// Generate a range of dates with a step
pub fn date_range_step(start: &Date, end: &Date, step_days: i64) -> Vec<Date> {
    let mut dates = Vec::new();
    let mut current = *start;
    
    while !current.is_after(end) {
        dates.push(current);
        current = current.add_days(step_days);
    }
    
    dates
}

/// Get all weekdays (Mon-Fri) in a date range
pub fn weekdays_in_range(start: &Date, end: &Date) -> Vec<Date> {
    date_range(start, end)
        .into_iter()
        .filter(|d| {
            let wd = d.weekday();
            wd != Weekday::Saturday && wd != Weekday::Sunday
        })
        .collect()
}

/// Get all weekends in a date range
pub fn weekends_in_range(start: &Date, end: &Date) -> Vec<Date> {
    date_range(start, end)
        .into_iter()
        .filter(|d| {
            let wd = d.weekday();
            wd == Weekday::Saturday || wd == Weekday::Sunday
        })
        .collect()
}

/// Get the module version
pub fn get_version() -> &'static str {
    env!("CARGO_PKG_VERSION", "1.0.0")
}

/// Check if a year is a leap year (convenience function)
pub fn is_leap_year(year: i32) -> bool {
    Date::is_leap_year(year)
}

/// Get days in a month (convenience function)
pub fn days_in_month(year: i32, month: u8) -> u8 {
    Date::days_in_month(year, month)
}

#[cfg(test)]
mod tests;
