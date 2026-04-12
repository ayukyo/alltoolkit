//! Date Utilities Module - Unit Tests
//!
//! Comprehensive tests for all date_utils functionality.
//!
//! Run with: cargo test

use super::*;

// =============================================================================
// Test Helper Functions
// =============================================================================

fn create_date(year: i32, month: u8, day: u8) -> Date {
    Date::new(year, month, day).unwrap()
}

// =============================================================================
// Date Creation Tests
// =============================================================================

#[test]
fn test_date_new_valid() {
    let date = Date::new(2024, 3, 15).unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_date_new_invalid_month() {
    assert!(Date::new(2024, 0, 15).is_err());
    assert!(Date::new(2024, 13, 15).is_err());
}

#[test]
fn test_date_new_invalid_day() {
    assert!(Date::new(2024, 2, 30).is_err());
    assert!(Date::new(2024, 4, 31).is_err());
    assert!(Date::new(2024, 1, 0).is_err());
}

#[test]
fn test_date_new_leap_year_feb_29() {
    let date = Date::new(2024, 2, 29).unwrap();
    assert_eq!(date.day(), 29);
}

#[test]
fn test_date_new_non_leap_year_feb_29() {
    assert!(Date::new(2023, 2, 29).is_err());
}

#[test]
fn test_date_today() {
    let today = Date::today();
    assert!(today.year() >= 2024);
    assert!(today.month() >= 1 && today.month() <= 12);
    assert!(today.day() >= 1 && today.day() <= 31);
}

// =============================================================================
// Leap Year Tests
// =============================================================================

#[test]
fn test_is_leap_year_divisible_by_4() {
    assert!(Date::is_leap_year(2024));
    assert!(Date::is_leap_year(2028));
}

#[test]
fn test_is_leap_year_divisible_by_100() {
    assert!(!Date::is_leap_year(1900));
    assert!(!Date::is_leap_year(2100));
}

#[test]
fn test_is_leap_year_divisible_by_400() {
    assert!(Date::is_leap_year(2000));
    assert!(Date::is_leap_year(2400));
}

#[test]
fn test_is_leap_year_not_divisible_by_4() {
    assert!(!Date::is_leap_year(2023));
    assert!(!Date::is_leap_year(2019));
}

// =============================================================================
// Days in Month Tests
// =============================================================================

#[test]
fn test_days_in_month_31_days() {
    assert_eq!(Date::days_in_month(2024, 1), 31);
    assert_eq!(Date::days_in_month(2024, 3), 31);
    assert_eq!(Date::days_in_month(2024, 5), 31);
    assert_eq!(Date::days_in_month(2024, 7), 31);
    assert_eq!(Date::days_in_month(2024, 8), 31);
    assert_eq!(Date::days_in_month(2024, 10), 31);
    assert_eq!(Date::days_in_month(2024, 12), 31);
}

#[test]
fn test_days_in_month_30_days() {
    assert_eq!(Date::days_in_month(2024, 4), 30);
    assert_eq!(Date::days_in_month(2024, 6), 30);
    assert_eq!(Date::days_in_month(2024, 9), 30);
    assert_eq!(Date::days_in_month(2024, 11), 30);
}

#[test]
fn test_days_in_month_february_leap() {
    assert_eq!(Date::days_in_month(2024, 2), 29);
}

#[test]
fn test_days_in_month_february_non_leap() {
    assert_eq!(Date::days_in_month(2023, 2), 28);
}

// =============================================================================
// Weekday Tests
// =============================================================================

#[test]
fn test_weekday_known_dates() {
    // 2024-01-01 was a Monday
    let date = create_date(2024, 1, 1);
    assert_eq!(date.weekday(), Weekday::Monday);
    
    // 2024-03-15 was a Friday
    let date = create_date(2024, 3, 15);
    assert_eq!(date.weekday(), Weekday::Friday);
    
    // 2024-12-25 was a Wednesday
    let date = create_date(2024, 12, 25);
    assert_eq!(date.weekday(), Weekday::Wednesday);
}

#[test]
fn test_weekday_short_name() {
    assert_eq!(Weekday::Monday.short_name(), "Mon");
    assert_eq!(Weekday::Sunday.short_name(), "Sun");
}

#[test]
fn test_weekday_full_name() {
    assert_eq!(Weekday::Monday.full_name(), "Monday");
    assert_eq!(Weekday::Sunday.full_name(), "Sunday");
}

#[test]
fn test_weekday_number() {
    assert_eq!(Weekday::Monday.number(), 1);
    assert_eq!(Weekday::Sunday.number(), 7);
}

// =============================================================================
// Month Tests
// =============================================================================

#[test]
fn test_month_from_number() {
    assert_eq!(Month::from_number(1), Some(Month::January));
    assert_eq!(Month::from_number(12), Some(Month::December));
    assert_eq!(Month::from_number(0), None);
    assert_eq!(Month::from_number(13), None);
}

#[test]
fn test_month_short_name() {
    assert_eq!(Month::January.short_name(), "Jan");
    assert_eq!(Month::December.short_name(), "Dec");
}

#[test]
fn test_month_full_name() {
    assert_eq!(Month::January.full_name(), "January");
    assert_eq!(Month::December.full_name(), "December");
}

// =============================================================================
// Day of Year Tests
// =============================================================================

#[test]
fn test_day_of_year_jan_1() {
    let date = create_date(2024, 1, 1);
    assert_eq!(date.day_of_year(), 1);
}

#[test]
fn test_day_of_year_dec_31() {
    let date = create_date(2024, 12, 31);
    assert_eq!(date.day_of_year(), 366); // Leap year
    
    let date = create_date(2023, 12, 31);
    assert_eq!(date.day_of_year(), 365); // Non-leap year
}

#[test]
fn test_day_of_year_march_1() {
    let date = create_date(2024, 3, 1);
    assert_eq!(date.day_of_year(), 61); // 31 + 29 + 1
    
    let date = create_date(2023, 3, 1);
    assert_eq!(date.day_of_year(), 60); // 31 + 28 + 1
}

// =============================================================================
// Timestamp Tests
// =============================================================================

#[test]
fn test_timestamp_epoch() {
    let date = create_date(1970, 1, 1);
    assert_eq!(date.to_timestamp(), 0);
}

#[test]
fn test_timestamp_roundtrip() {
    let original = create_date(2024, 6, 15);
    let timestamp = original.to_timestamp();
    let restored = Date::from_timestamp(timestamp);
    assert_eq!(original, restored);
}

#[test]
fn test_from_timestamp_known_date() {
    // 2024-01-01
    let date = Date::from_timestamp(1704067200);
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 1);
    assert_eq!(date.day(), 1);
}

// =============================================================================
// Date Arithmetic Tests
// =============================================================================

#[test]
fn test_add_days() {
    let date = create_date(2024, 1, 1);
    let result = date.add_days(10);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 1);
    assert_eq!(result.day(), 11);
}

#[test]
fn test_add_days_cross_month() {
    let date = create_date(2024, 1, 25);
    let result = date.add_days(10);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 2);
    assert_eq!(result.day(), 4);
}

#[test]
fn test_add_days_cross_year() {
    let date = create_date(2023, 12, 25);
    let result = date.add_days(10);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 1);
    assert_eq!(result.day(), 4);
}

#[test]
fn test_subtract_days() {
    let date = create_date(2024, 1, 15);
    let result = date.subtract_days(10);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 1);
    assert_eq!(result.day(), 5);
}

#[test]
fn test_add_months() {
    let date = create_date(2024, 1, 15);
    let result = date.add_months(3);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 4);
    assert_eq!(result.day(), 15);
}

#[test]
fn test_add_months_cross_year() {
    let date = create_date(2024, 10, 15);
    let result = date.add_months(5);
    assert_eq!(result.year(), 2025);
    assert_eq!(result.month(), 3);
    assert_eq!(result.day(), 15);
}

#[test]
fn test_add_months_day_adjustment() {
    // Jan 31 + 1 month = Feb 29 (leap year)
    let date = create_date(2024, 1, 31);
    let result = date.add_months(1);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 2);
    assert_eq!(result.day(), 29);
}

#[test]
fn test_subtract_months() {
    let date = create_date(2024, 4, 15);
    let result = date.subtract_months(3);
    assert_eq!(result.year(), 2024);
    assert_eq!(result.month(), 1);
    assert_eq!(result.day(), 15);
}

#[test]
fn test_add_years() {
    let date = create_date(2024, 3, 15);
    let result = date.add_years(5);
    assert_eq!(result.year(), 2029);
    assert_eq!(result.month(), 3);
    assert_eq!(result.day(), 15);
}

#[test]
fn test_add_years_leap_day() {
    // Feb 29, 2024 + 1 year = Feb 28, 2025
    let date = create_date(2024, 2, 29);
    let result = date.add_years(1);
    assert_eq!(result.year(), 2025);
    assert_eq!(result.month(), 2);
    assert_eq!(result.day(), 28);
}

// =============================================================================
// Date Comparison Tests
// =============================================================================

#[test]
fn test_is_before() {
    let date1 = create_date(2024, 1, 15);
    let date2 = create_date(2024, 1, 20);
    assert!(date1.is_before(&date2));
    assert!(!date2.is_before(&date1));
    assert!(!date1.is_before(&date1));
}

#[test]
fn test_is_after() {
    let date1 = create_date(2024, 1, 15);
    let date2 = create_date(2024, 1, 20);
    assert!(date2.is_after(&date1));
    assert!(!date1.is_after(&date2));
    assert!(!date1.is_after(&date1));
}

#[test]
fn test_is_equal() {
    let date1 = create_date(2024, 1, 15);
    let date2 = create_date(2024, 1, 15);
    let date3 = create_date(2024, 1, 16);
    assert!(date1.is_equal(&date2));
    assert!(!date1.is_equal(&date3));
}

#[test]
fn test_is_between() {
    let start = create_date(2024, 1, 1);
    let end = create_date(2024, 12, 31);
    let middle = create_date(2024, 6, 15);
    let before = create_date(2023, 12, 31);
    let after = create_date(2025, 1, 1);
    
    assert!(middle.is_between(&start, &end));
    assert!(start.is_between(&start, &end));
    assert!(end.is_between(&start, &end));
    assert!(!before.is_between(&start, &end));
    assert!(!after.is_between(&start, &end));
}

#[test]
fn test_days_difference() {
    let date1 = create_date(2024, 1, 1);
    let date2 = create_date(2024, 1, 11);
    assert_eq!(date1.days_difference(&date2), 10);
    assert_eq!(date2.days_difference(&date1), -10);
}

#[test]
fn test_sub_operator() {
    let date1 = create_date(2024, 1, 1);
    let date2 = create_date(2024, 1, 11);
    assert_eq!(date2 - date1, 10);
}

// =============================================================================
// First/Last Day Tests
// =============================================================================

#[test]
fn test_first_day_of_month() {
    let date = create_date(2024, 6, 15);
    let first = date.first_day_of_month();
    assert_eq!(first.year(), 2024);
    assert_eq!(first.month(), 6);
    assert_eq!(first.day(), 1);
}

#[test]
fn test_last_day_of_month() {
    let date = create_date(2024, 2, 15);
    let last = date.last_day_of_month();
    assert_eq!(last.year(), 2024);
    assert_eq!(last.month(), 2);
    assert_eq!(last.day(), 29);
}

#[test]
fn test_first_day_of_year() {
    let date = create_date(2024, 6, 15);
    let first = date.first_day_of_year();
    assert_eq!(first.year(), 2024);
    assert_eq!(first.month(), 1);
    assert_eq!(first.day(), 1);
}

#[test]
fn test_last_day_of_year() {
    let date = create_date(2024, 6, 15);
    let last = date.last_day_of_year();
    assert_eq!(last.year(), 2024);
    assert_eq!(last.month(), 12);
    assert_eq!(last.day(), 31);
}

// =============================================================================
// Parse Date Tests
// =============================================================================

#[test]
fn test_parse_date_iso_format() {
    let date = parse_date("2024-03-15").unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_parse_date_slash_format() {
    let date = parse_date("2024/03/15").unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_parse_date_european_format() {
    let date = parse_date("15-03-2024").unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_parse_date_us_format() {
    let date = parse_date("03-15-2024").unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_parse_date_compact_format() {
    let date = parse_date("20240315").unwrap();
    assert_eq!(date.year(), 2024);
    assert_eq!(date.month(), 3);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_parse_date_invalid() {
    assert!(parse_date("invalid").is_err());
    assert!(parse_date("2024-13-01").is_err());
    assert!(parse_date("2024-02-30").is_err());
}

// =============================================================================
// Format Date Tests
// =============================================================================

#[test]
fn test_format_date_iso() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "YYYY-MM-DD"), "2024-03-15");
}

#[test]
fn test_format_date_us() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "MM/DD/YYYY"), "03/15/2024");
}

#[test]
fn test_format_date_european() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "DD/MM/YYYY"), "15/03/2024");
}

#[test]
fn test_format_date_with_month_name() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "'Month:' MMMM"), "Month: March");
    assert_eq!(format_date(&date, "'Month:' MMM"), "Month: Mar");
}

#[test]
fn test_format_date_with_weekday() {
    let date = create_date(2024, 3, 15); // Friday
    assert_eq!(format_date(&date, "EEEE"), "Friday");
    assert_eq!(format_date(&date, "EEE"), "Fri");
}

#[test]
fn test_format_date_day_of_year() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "'Day 'DDD' of year'"), "Day 75 of year");
}

#[test]
fn test_format_date_mixed() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format_date(&date, "EEEE, MMMM D, YYYY"), "Friday, March 15, 2024");
}

// =============================================================================
// Date Range Tests
// =============================================================================

#[test]
fn test_date_range_small() {
    let start = create_date(2024, 1, 1);
    let end = create_date(2024, 1, 5);
    let range = date_range(&start, &end);
    
    assert_eq!(range.len(), 5);
    assert_eq!(range[0].day(), 1);
    assert_eq!(range[4].day(), 5);
}

#[test]
fn test_date_range_step() {
    let start = create_date(2024, 1, 1);
    let end = create_date(2024, 1, 10);
    let range = date_range_step(&start, &end, 2);
    
    assert_eq!(range.len(), 5);
    assert_eq!(range[0].day(), 1);
    assert_eq!(range[1].day(), 3);
    assert_eq!(range[2].day(), 5);
    assert_eq!(range[3].day(), 7);
    assert_eq!(range[4].day(), 9);
}

#[test]
fn test_weekdays_in_range() {
    // Jan 1-7, 2024: Mon, Tue, Wed, Thu, Fri, Sat, Sun
    let start = create_date(2024, 1, 1);
    let end = create_date(2024, 1, 7);
    let weekdays = weekdays_in_range(&start, &end);
    
    assert_eq!(weekdays.len(), 5);
    for day in &weekdays {
        let wd = day.weekday();
        assert!(wd != Weekday::Saturday && wd != Weekday::Sunday);
    }
}

#[test]
fn test_weekends_in_range() {
    // Jan 1-7, 2024: Mon, Tue, Wed, Thu, Fri, Sat, Sun
    let start = create_date(2024, 1, 1);
    let end = create_date(2024, 1, 7);
    let weekends = weekends_in_range(&start, &end);
    
    assert_eq!(weekends.len(), 2);
    for day in &weekends {
        let wd = day.weekday();
        assert!(wd == Weekday::Saturday || wd == Weekday::Sunday);
    }
}

// =============================================================================
// Operator Tests
// =============================================================================

#[test]
fn test_add_operator() {
    let date = create_date(2024, 1, 1);
    let result = date + 10;
    assert_eq!(result.day(), 11);
}

#[test]
fn test_sub_days_operator() {
    let date = create_date(2024, 1, 15);
    let result = date - 10;
    assert_eq!(result.day(), 5);
}

// =============================================================================
// Display Tests
// =============================================================================

#[test]
fn test_date_display() {
    let date = create_date(2024, 3, 15);
    assert_eq!(format!("{}", date), "2024-03-15");
}

#[test]
fn test_weekday_display() {
    assert_eq!(format!("{}", Weekday::Monday), "Mon");
}

#[test]
fn test_month_display() {
    assert_eq!(format!("{}", Month::January), "Jan");
}

// =============================================================================
// Edge Cases
// =============================================================================

#[test]
fn test_negative_year() {
    let date = Date::new(-100, 6, 15).unwrap();
    assert_eq!(date.year(), -100);
    assert_eq!(date.month(), 6);
    assert_eq!(date.day(), 15);
}

#[test]
fn test_large_year() {
    let date = Date::new(9999, 12, 31).unwrap();
    assert_eq!(date.year(), 9999);
    assert_eq!(date.month(), 12);
    assert_eq!(date.day(), 31);
}

#[test]
fn test_days_difference_cross_year() {
    let date1 = create_date(2023, 12, 31);
    let date2 = create_date(2024, 1, 1);
    assert_eq!(date1.days_difference(&date2), 1);
}

#[test]
fn test_add_months_negative() {
    let date = create_date(2024, 3, 15);
    let result = date.add_months(-5);
    assert_eq!(result.year(), 2023);
    assert_eq!(result.month(), 10);
    assert_eq!(result.day(), 15);
}

#[test]
fn test_add_years_negative() {
    let date = create_date(2024, 3, 15);
    let result = date.add_years(-10);
    assert_eq!(result.year(), 2014);
    assert_eq!(result.month(), 3);
    assert_eq!(result.day(), 15);
}

// =============================================================================
// Convenience Functions Tests
// =============================================================================

#[test]
fn test_is_leap_year_function() {
    assert!(is_leap_year(2024));
    assert!(!is_leap_year(2023));
}

#[test]
fn test_days_in_month_function() {
    assert_eq!(days_in_month(2024, 2), 29);
    assert_eq!(days_in_month(2023, 2), 28);
}
