/**
 * @file datetime_utils_test.cpp
 * @brief Comprehensive tests for datetime_utils library
 * 
 * Tests cover all public functions with 100% code coverage.
 * Compile: g++ -std=c++17 -o datetime_utils_test datetime_utils_test.cpp
 * Run: ./datetime_utils_test
 * 
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-13
 */

#include "datetime_utils.hpp"
#include <iostream>
#include <cassert>
#include <cmath>
#include <thread>
#include <chrono>

using namespace datetime_utils;

// Test counters
int tests_passed = 0;
int tests_failed = 0;

// Helper macro for test assertions
#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    std::cout << "Running " << #name << "... "; \
    try { \
        test_##name(); \
        std::cout << "PASSED" << std::endl; \
        tests_passed++; \
    } catch (const std::exception& e) { \
        std::cout << "FAILED: " << e.what() << std::endl; \
        tests_failed++; \
    } \
} while(0)

#define ASSERT_TRUE(cond) if (!(cond)) throw std::runtime_error("Assertion failed: " #cond)
#define ASSERT_FALSE(cond) if (cond) throw std::runtime_error("Assertion failed: " #cond)
#define ASSERT_EQ(a, b) if ((a) != (b)) throw std::runtime_error("Assertion failed: " #a " != " #b)
#define ASSERT_NE(a, b) if ((a) == (b)) throw std::runtime_error("Assertion failed: " #a " == " #b)
#define ASSERT_THROW(expr, exc) do { bool caught = false; try { expr; } catch (const exc&) { caught = true; } if (!caught) throw std::runtime_error("Expected exception: " #exc); } while(0)
#define ASSERT_NO_THROW(expr) do { try { expr; } catch (...) { throw std::runtime_error("Unexpected exception"); } } while(0)

// ============================================================================
// Date Structure Tests
// ============================================================================

TEST(date_constructor) {
    Date d;
    ASSERT_EQ(d.year, 1970);
    ASSERT_EQ(d.month, 1);
    ASSERT_EQ(d.day, 1);
    
    Date d2(2026, 4, 13);
    ASSERT_EQ(d2.year, 2026);
    ASSERT_EQ(d2.month, 4);
    ASSERT_EQ(d2.day, 13);
}

TEST(date_comparison) {
    Date d1(2026, 4, 13);
    Date d2(2026, 4, 14);
    Date d3(2026, 4, 13);
    
    ASSERT_TRUE(d1 == d3);
    ASSERT_TRUE(d1 != d2);
    ASSERT_TRUE(d1 < d2);
    ASSERT_TRUE(d1 <= d2);
    ASSERT_TRUE(d1 <= d3);
    ASSERT_TRUE(d2 > d1);
    ASSERT_TRUE(d2 >= d1);
    ASSERT_TRUE(d1 >= d3);
}

TEST(date_to_string) {
    Date d(2026, 4, 13);
    ASSERT_EQ(d.to_string(), "2026-04-13");
    
    Date d2(2000, 1, 1);
    ASSERT_EQ(d2.to_string(), "2000-01-01");
    
    Date d3(1999, 12, 31);
    ASSERT_EQ(d3.to_string(), "1999-12-31");
}

// ============================================================================
// Time Structure Tests
// ============================================================================

TEST(time_constructor) {
    Time t;
    ASSERT_EQ(t.hour, 0);
    ASSERT_EQ(t.minute, 0);
    ASSERT_EQ(t.second, 0);
    ASSERT_EQ(t.microsecond, 0);
    
    Time t2(14, 30, 45, 123456);
    ASSERT_EQ(t2.hour, 14);
    ASSERT_EQ(t2.minute, 30);
    ASSERT_EQ(t2.second, 45);
    ASSERT_EQ(t2.microsecond, 123456);
}

TEST(time_comparison) {
    Time t1(12, 30, 45);
    Time t2(12, 30, 46);
    Time t3(12, 30, 45);
    
    ASSERT_TRUE(t1 == t3);
    ASSERT_TRUE(t1 != t2);
    ASSERT_TRUE(t1 < t2);
    ASSERT_TRUE(t1 <= t2);
    ASSERT_TRUE(t1 <= t3);
    ASSERT_TRUE(t2 > t1);
    ASSERT_TRUE(t2 >= t1);
    ASSERT_TRUE(t1 >= t3);
    
    // Test with microseconds
    Time t4(12, 30, 45, 100);
    Time t5(12, 30, 45, 200);
    ASSERT_TRUE(t4 < t5);
}

TEST(time_to_string) {
    Time t(14, 30, 45);
    ASSERT_EQ(t.to_string(), "14:30:45");
    
    Time t2(9, 5, 7);
    ASSERT_EQ(t2.to_string(), "09:05:07");
    
    Time t3(14, 30, 45, 123456);
    ASSERT_EQ(t3.to_string(), "14:30:45.123456");
}

// ============================================================================
// DateTime Structure Tests
// ============================================================================

TEST(datetime_constructor) {
    DateTime dt;
    ASSERT_EQ(dt.date.year, 1970);
    ASSERT_EQ(dt.date.month, 1);
    ASSERT_EQ(dt.date.day, 1);
    ASSERT_EQ(dt.time.hour, 0);
    ASSERT_EQ(dt.tz_offset_minutes, 0);
    
    Date d(2026, 4, 13);
    Time t(14, 30, 45);
    DateTime dt2(d, t, 480); // UTC+8
    ASSERT_EQ(dt2.date.year, 2026);
    ASSERT_EQ(dt2.time.hour, 14);
    ASSERT_EQ(dt2.tz_offset_minutes, 480);
}

TEST(datetime_to_string) {
    DateTime dt(Date(2026, 4, 13), Time(14, 30, 45));
    ASSERT_EQ(dt.to_string(), "2026-04-13 14:30:45");
    
    DateTime dt2(Date(2026, 4, 13), Time(14, 30, 45), 480);
    ASSERT_EQ(dt2.to_string(), "2026-04-13 14:30:45+08:00");
    
    DateTime dt3(Date(2026, 4, 13), Time(14, 30, 45), -300);
    ASSERT_EQ(dt3.to_string(), "2026-04-13 14:30:45-05:00");
}

// ============================================================================
// Validation Tests
// ============================================================================

TEST(is_leap_year) {
    ASSERT_TRUE(is_leap_year(2000));  // Divisible by 400
    ASSERT_TRUE(is_leap_year(2024));  // Divisible by 4, not 100
    ASSERT_FALSE(is_leap_year(1900)); // Divisible by 100, not 400
    ASSERT_FALSE(is_leap_year(2023)); // Not divisible by 4
    ASSERT_TRUE(is_leap_year(2400));  // Divisible by 400
    ASSERT_FALSE(is_leap_year(2100)); // Divisible by 100, not 400
}

TEST(is_valid_year) {
    ASSERT_TRUE(is_valid_year(1000));
    ASSERT_TRUE(is_valid_year(2026));
    ASSERT_TRUE(is_valid_year(9999));
    ASSERT_FALSE(is_valid_year(999));
    ASSERT_FALSE(is_valid_year(10000));
}

TEST(is_valid_month) {
    for (int m = 1; m <= 12; ++m) {
        ASSERT_TRUE(is_valid_month(m));
    }
    ASSERT_FALSE(is_valid_month(0));
    ASSERT_FALSE(is_valid_month(13));
    ASSERT_FALSE(is_valid_month(-1));
}

TEST(days_in_month) {
    // Non-leap year
    ASSERT_EQ(days_in_month(2023, 1), 31);
    ASSERT_EQ(days_in_month(2023, 2), 28);
    ASSERT_EQ(days_in_month(2023, 4), 30);
    ASSERT_EQ(days_in_month(2023, 12), 31);
    
    // Leap year
    ASSERT_EQ(days_in_month(2024, 2), 29);
    ASSERT_EQ(days_in_month(2000, 2), 29);
    
    // Invalid month
    ASSERT_THROW(days_in_month(2023, 0), std::invalid_argument);
    ASSERT_THROW(days_in_month(2023, 13), std::invalid_argument);
}

TEST(is_valid_day) {
    ASSERT_TRUE(is_valid_day(2023, 1, 31));
    ASSERT_TRUE(is_valid_day(2023, 1, 1));
    ASSERT_FALSE(is_valid_day(2023, 1, 32));
    ASSERT_FALSE(is_valid_day(2023, 1, 0));
    
    ASSERT_TRUE(is_valid_day(2024, 2, 29));  // Leap year
    ASSERT_FALSE(is_valid_day(2023, 2, 29)); // Non-leap year
}

TEST(is_valid_date) {
    ASSERT_TRUE(is_valid_date(Date(2026, 4, 13)));
    ASSERT_TRUE(is_valid_date(Date(2000, 2, 29)));
    ASSERT_FALSE(is_valid_date(Date(2023, 2, 29)));
    ASSERT_FALSE(is_valid_date(Date(100, 1, 1)));
    ASSERT_FALSE(is_valid_date(Date(2023, 13, 1)));
}

TEST(is_valid_time) {
    ASSERT_TRUE(is_valid_time(Time(0, 0, 0)));
    ASSERT_TRUE(is_valid_time(Time(23, 59, 59, 999999)));
    ASSERT_FALSE(is_valid_time(Time(24, 0, 0)));
    ASSERT_FALSE(is_valid_time(Time(0, 60, 0)));
    ASSERT_FALSE(is_valid_time(Time(0, 0, 60)));
    ASSERT_FALSE(is_valid_time(Time(0, 0, 0, 1000000)));
}

TEST(is_valid_datetime) {
    ASSERT_TRUE(is_valid_datetime(DateTime(Date(2026, 4, 13), Time(14, 30, 45))));
    ASSERT_FALSE(is_valid_datetime(DateTime(Date(2023, 2, 29), Time(14, 30, 45))));
    ASSERT_FALSE(is_valid_datetime(DateTime(Date(2026, 4, 13), Time(25, 30, 45))));
}

// ============================================================================
// Current Time Tests
// ============================================================================

TEST(now_functions) {
    auto tp = now();
    ASSERT_TRUE(tp.time_since_epoch().count() > 0);
    
    Date d = today();
    ASSERT_TRUE(is_valid_date(d));
    ASSERT_TRUE(d.year >= 2026);
    
    DateTime dt = now_datetime();
    ASSERT_TRUE(is_valid_datetime(dt));
    
    DateTime utc = utcnow();
    ASSERT_TRUE(is_valid_datetime(utc));
    
    int64_t ts = timestamp();
    ASSERT_TRUE(ts > 0);
    
    int64_t ts_ms = timestamp_ms();
    ASSERT_TRUE(ts_ms > 0);
    ASSERT_EQ(ts_ms / 1000, ts);
    
    int64_t ts_us = timestamp_us();
    ASSERT_TRUE(ts_us > 0);
}

// ============================================================================
// Parsing Tests
// ============================================================================

TEST(parse_date) {
    Date d = parse_date("2026-04-13");
    ASSERT_EQ(d.year, 2026);
    ASSERT_EQ(d.month, 4);
    ASSERT_EQ(d.day, 13);
    
    Date d2 = parse_date("2000-01-01");
    ASSERT_EQ(d2.year, 2000);
    ASSERT_EQ(d2.month, 1);
    ASSERT_EQ(d2.day, 1);
    
    ASSERT_THROW(parse_date("invalid"), std::invalid_argument);
    ASSERT_THROW(parse_date("2023-13-01"), std::invalid_argument);
    ASSERT_THROW(parse_date("2023-02-30"), std::invalid_argument);
}

TEST(parse_time) {
    Time t = parse_time("14:30:45");
    ASSERT_EQ(t.hour, 14);
    ASSERT_EQ(t.minute, 30);
    ASSERT_EQ(t.second, 45);
    ASSERT_EQ(t.microsecond, 0);
    
    Time t2 = parse_time("09:05:07.123456");
    ASSERT_EQ(t2.hour, 9);
    ASSERT_EQ(t2.minute, 5);
    ASSERT_EQ(t2.second, 7);
    ASSERT_EQ(t2.microsecond, 123456);
    
    Time t3 = parse_time("00:00:00.1");
    ASSERT_EQ(t3.microsecond, 100000);
    
    ASSERT_THROW(parse_time("invalid"), std::invalid_argument);
    ASSERT_THROW(parse_time("25:00:00"), std::invalid_argument);
    ASSERT_THROW(parse_time("00:60:00"), std::invalid_argument);
}

TEST(parse_datetime) {
    DateTime dt = parse_datetime("2026-04-13 14:30:45");
    ASSERT_EQ(dt.date.year, 2026);
    ASSERT_EQ(dt.date.month, 4);
    ASSERT_EQ(dt.date.day, 13);
    ASSERT_EQ(dt.time.hour, 14);
    ASSERT_EQ(dt.time.minute, 30);
    ASSERT_EQ(dt.time.second, 45);
    ASSERT_EQ(dt.tz_offset_minutes, 0);
    
    // ISO format with T
    DateTime dt2 = parse_datetime("2026-04-13T14:30:45");
    ASSERT_EQ(dt2.date.year, 2026);
    
    // With timezone
    DateTime dt3 = parse_datetime("2026-04-13T14:30:45+08:00");
    ASSERT_EQ(dt3.tz_offset_minutes, 480);
    
    DateTime dt4 = parse_datetime("2026-04-13T14:30:45-05:00");
    ASSERT_EQ(dt4.tz_offset_minutes, -300);
    
    DateTime dt5 = parse_datetime("2026-04-13T14:30:45Z");
    ASSERT_EQ(dt5.tz_offset_minutes, 0);
    
    ASSERT_THROW(parse_datetime("invalid"), std::invalid_argument);
}

TEST(from_timestamp) {
    // Known timestamp: 2024-01-01 00:00:00 UTC = 1704067200
    DateTime dt = from_timestamp(1704067200);
    ASSERT_EQ(dt.date.year, 2024);
    ASSERT_EQ(dt.date.month, 1);
    ASSERT_EQ(dt.date.day, 1);
    ASSERT_EQ(dt.time.hour, 0);
    ASSERT_EQ(dt.time.minute, 0);
    ASSERT_EQ(dt.time.second, 0);
}

TEST(from_timestamp_ms) {
    DateTime dt = from_timestamp_ms(1704067200123);
    ASSERT_EQ(dt.date.year, 2024);
    ASSERT_EQ(dt.date.month, 1);
    ASSERT_EQ(dt.date.day, 1);
    ASSERT_TRUE(dt.time.microsecond > 0);
}

// ============================================================================
// Formatting Tests
// ============================================================================

TEST(format_date) {
    Date d(2026, 4, 13);
    
    ASSERT_EQ(format_date(d, "YYYY-MM-DD"), "2026-04-13");
    ASSERT_EQ(format_date(d, "YY-M-D"), "26-4-13");
    ASSERT_EQ(format_date(d, "DD/MM/YYYY"), "13/04/2026");
    ASSERT_EQ(format_date(d, "MMMM DD, YYYY"), "April 13, 2026");
    ASSERT_EQ(format_date(d, "MMM DD, YYYY"), "Apr 13, 2026");
    
    Date d2(2026, 1, 5);
    ASSERT_EQ(format_date(d2, "YYYY-MM-DD"), "2026-01-05");
    ASSERT_EQ(format_date(d2, "YYYY-M-D"), "2026-1-5");
}

TEST(format_time) {
    Time t(14, 30, 45, 123456);
    
    ASSERT_EQ(format_time(t, "HH:mm:ss"), "14:30:45");
    ASSERT_EQ(format_time(t, "H:m:s"), "14:30:45");
    ASSERT_EQ(format_time(t, "HH:mm:ss.SSSSSS"), "14:30:45.123456");
    ASSERT_EQ(format_time(t, "HH:mm:ss.SSS"), "14:30:45.123");
    
    Time t2(9, 5, 7);
    ASSERT_EQ(format_time(t2, "HH:mm:ss"), "09:05:07");
    ASSERT_EQ(format_time(t2, "H:m:s"), "9:5:7");
}

TEST(format_datetime) {
    DateTime dt(Date(2026, 4, 13), Time(14, 30, 45, 123456));
    
    ASSERT_EQ(format_datetime(dt, "YYYY-MM-DD HH:mm:ss"), "2026-04-13 14:30:45");
    ASSERT_EQ(to_iso_string(dt), "2026-04-13 14:30:45.123456");
}

// ============================================================================
// Date Arithmetic Tests
// ============================================================================

TEST(add_days) {
    Date d(2026, 4, 13);
    
    Date d1 = add_days(d, 1);
    ASSERT_EQ(d1.day, 14);
    
    // 4月有30天，13 + 17 = 30，所以是4月30日
    Date d2 = add_days(d, 17);
    ASSERT_EQ(d2.month, 4);
    ASSERT_EQ(d2.day, 30);
    
    // 4月13日 + 18天 = 5月1日
    Date d2b = add_days(d, 18);
    ASSERT_EQ(d2b.month, 5);
    ASSERT_EQ(d2b.day, 1);
    
    Date d3 = add_days(d, -1);
    ASSERT_EQ(d3.day, 12);
    
    // Year boundary
    Date d4(2026, 1, 1);
    Date d5 = add_days(d4, -1);
    ASSERT_EQ(d5.year, 2025);
    ASSERT_EQ(d5.month, 12);
    ASSERT_EQ(d5.day, 31);
    
    // Leap year
    Date d6(2024, 2, 28);
    Date d7 = add_days(d6, 1);
    ASSERT_EQ(d7.month, 2);
    ASSERT_EQ(d7.day, 29);
}

TEST(add_months) {
    Date d(2026, 4, 13);
    
    Date d1 = add_months(d, 1);
    ASSERT_EQ(d1.month, 5);
    ASSERT_EQ(d1.day, 13);
    
    Date d2 = add_months(d, 12);
    ASSERT_EQ(d2.year, 2027);
    ASSERT_EQ(d2.month, 4);
    
    Date d3 = add_months(d, -4);
    ASSERT_EQ(d3.month, 12);
    ASSERT_EQ(d3.year, 2025);
    
    // Day adjustment for shorter months
    Date d4(2026, 1, 31);
    Date d5 = add_months(d4, 1);
    ASSERT_EQ(d5.month, 2);
    ASSERT_EQ(d5.day, 28); // Feb 2026 has 28 days
    
    // Leap year
    Date d6(2024, 1, 31);
    Date d7 = add_months(d6, 1);
    ASSERT_EQ(d7.month, 2);
    ASSERT_EQ(d7.day, 29); // Feb 2024 has 29 days
}

TEST(add_years) {
    Date d(2026, 4, 13);
    
    Date d1 = add_years(d, 1);
    ASSERT_EQ(d1.year, 2027);
    
    Date d2 = add_years(d, -1);
    ASSERT_EQ(d2.year, 2025);
    
    // Leap year adjustment
    Date d3(2024, 2, 29);
    Date d4 = add_years(d3, 1);
    ASSERT_EQ(d4.year, 2025);
    ASSERT_EQ(d4.month, 2);
    ASSERT_EQ(d4.day, 28);
}

TEST(days_between) {
    Date d1(2026, 4, 13);
    Date d2(2026, 4, 14);
    ASSERT_EQ(days_between(d1, d2), 1);
    
    Date d3(2026, 4, 13);
    Date d4(2026, 4, 13);
    ASSERT_EQ(days_between(d3, d4), 0);
    
    Date d5(2026, 1, 1);
    Date d6(2026, 12, 31);
    ASSERT_EQ(days_between(d5, d6), 364);
    
    Date d7(2024, 1, 1);
    Date d8(2025, 1, 1);
    ASSERT_EQ(days_between(d7, d8), 366); // Leap year
    
    // Negative
    ASSERT_EQ(days_between(d2, d1), -1);
}

TEST(day_of_week) {
    // 2026-04-13 is a Monday
    Date d(2026, 4, 13);
    ASSERT_EQ(day_of_week(d), 1);
    
    // 2026-04-12 is a Sunday
    Date d2(2026, 4, 12);
    ASSERT_EQ(day_of_week(d2), 0);
    
    // 2026-04-18 is a Saturday
    Date d3(2026, 4, 18);
    ASSERT_EQ(day_of_week(d3), 6);
}

TEST(day_of_week_name) {
    Date d(2026, 4, 13);
    ASSERT_EQ(day_of_week_name(d), "Monday");
    ASSERT_EQ(day_of_week_name(d, true), "Mon");
    
    Date d2(2026, 4, 12);
    ASSERT_EQ(day_of_week_name(d2), "Sunday");
    ASSERT_EQ(day_of_week_name(d2, true), "Sun");
}

TEST(month_name) {
    ASSERT_EQ(month_name(1), "January");
    ASSERT_EQ(month_name(1, true), "Jan");
    ASSERT_EQ(month_name(12), "December");
    ASSERT_EQ(month_name(12, true), "Dec");
    
    ASSERT_THROW(month_name(0), std::invalid_argument);
    ASSERT_THROW(month_name(13), std::invalid_argument);
}

TEST(day_of_year) {
    Date d1(2026, 1, 1);
    ASSERT_EQ(day_of_year(d1), 1);
    
    Date d2(2026, 12, 31);
    ASSERT_EQ(day_of_year(d2), 365);
    
    Date d3(2024, 12, 31); // Leap year
    ASSERT_EQ(day_of_year(d3), 366);
    
    Date d4(2026, 2, 1);
    ASSERT_EQ(day_of_year(d4), 32);
}

TEST(week_of_year) {
    Date d1(2026, 1, 1);
    int w1 = week_of_year(d1);
    ASSERT_TRUE(w1 >= 1 && w1 <= 53);
    
    Date d2(2026, 12, 31);
    int w2 = week_of_year(d2);
    ASSERT_TRUE(w2 >= 1 && w2 <= 53);
}

TEST(is_weekend) {
    // 2026-04-13 is Monday
    Date d1(2026, 4, 13);
    ASSERT_FALSE(is_weekend(d1));
    ASSERT_TRUE(is_weekday(d1));
    
    // 2026-04-12 is Sunday
    Date d2(2026, 4, 12);
    ASSERT_TRUE(is_weekend(d2));
    ASSERT_FALSE(is_weekday(d2));
    
    // 2026-04-18 is Saturday
    Date d3(2026, 4, 18);
    ASSERT_TRUE(is_weekend(d3));
    ASSERT_FALSE(is_weekday(d3));
}

TEST(first_last_day_of_month) {
    Date first = first_day_of_month(2026, 4);
    ASSERT_EQ(first.day, 1);
    ASSERT_EQ(first.month, 4);
    
    Date last = last_day_of_month(2026, 4);
    ASSERT_EQ(last.day, 30);
    
    Date last_feb = last_day_of_month(2024, 2);
    ASSERT_EQ(last_feb.day, 29);
    
    Date last_feb2 = last_day_of_month(2025, 2);
    ASSERT_EQ(last_feb2.day, 28);
}

TEST(first_last_day_of_week) {
    // 2026-04-13 is Monday
    Date d(2026, 4, 13);
    Date first = first_day_of_week(d);
    ASSERT_EQ(first.day, 13); // Same day (Monday)
    
    Date last = last_day_of_week(d);
    ASSERT_EQ(last.day, 19); // Sunday
    
    // 2026-04-15 is Wednesday
    Date d2(2026, 4, 15);
    Date first2 = first_day_of_week(d2);
    ASSERT_EQ(first2.day, 13); // Monday
    
    Date last2 = last_day_of_week(d2);
    ASSERT_EQ(last2.day, 19); // Sunday
}

TEST(nth_weekday_of_month) {
    // Second Monday of April 2026
    auto d1 = nth_weekday_of_month(2026, 4, 1, 2);
    ASSERT_TRUE(d1.has_value());
    ASSERT_EQ(d1->day, 13);
    
    // First Sunday of January 2026
    auto d2 = nth_weekday_of_month(2026, 1, 0, 1);
    ASSERT_TRUE(d2.has_value());
    ASSERT_EQ(d2->day, 4);
    
    // Fifth Monday of April 2026 (doesn't exist)
    auto d3 = nth_weekday_of_month(2026, 4, 1, 5);
    ASSERT_FALSE(d3.has_value());
    
    // Invalid input
    auto d4 = nth_weekday_of_month(2026, 13, 1, 1);
    ASSERT_FALSE(d4.has_value());
}

TEST(days_in_year) {
    ASSERT_EQ(days_in_year(2024), 366);
    ASSERT_EQ(days_in_year(2025), 365);
    ASSERT_EQ(days_in_year(2000), 366);
    ASSERT_EQ(days_in_year(1900), 365);
}

TEST(age_in_years) {
    Date birth(2000, 4, 13);
    Date today(2026, 4, 13);
    ASSERT_EQ(age_in_years(birth, today), 26);
    
    Date before_birthday(2026, 4, 12);
    ASSERT_EQ(age_in_years(birth, before_birthday), 25);
    
    Date after_birthday(2026, 4, 14);
    ASSERT_EQ(age_in_years(birth, after_birthday), 26);
}

// ============================================================================
// Time Arithmetic Tests
// ============================================================================

TEST(time_add_seconds) {
    Time t(12, 30, 45);
    
    Time t1 = add_seconds(t, 30);
    ASSERT_EQ(t1.second, 15);
    ASSERT_EQ(t1.minute, 31);
    
    Time t2 = add_seconds(t, -45);
    ASSERT_EQ(t2.second, 0);
    ASSERT_EQ(t2.minute, 30);
    
    // Wrap around midnight
    Time t3(23, 59, 59);
    Time t4 = add_seconds(t3, 1);
    ASSERT_EQ(t4.hour, 0);
    ASSERT_EQ(t4.minute, 0);
    ASSERT_EQ(t4.second, 0);
    
    Time t5(0, 0, 0);
    Time t6 = add_seconds(t5, -1);
    ASSERT_EQ(t6.hour, 23);
    ASSERT_EQ(t6.minute, 59);
    ASSERT_EQ(t6.second, 59);
}

TEST(time_add_minutes) {
    Time t(12, 30, 45);
    
    Time t1 = add_minutes(t, 30);
    ASSERT_EQ(t1.hour, 13);
    ASSERT_EQ(t1.minute, 0);
    
    Time t2 = add_minutes(t, -60);
    ASSERT_EQ(t2.hour, 11);
    ASSERT_EQ(t2.minute, 30);
}

TEST(time_add_hours) {
    Time t(12, 30, 45);
    
    Time t1 = add_hours(t, 2);
    ASSERT_EQ(t1.hour, 14);
    
    Time t2 = add_hours(t, -13);
    ASSERT_EQ(t2.hour, 23);
    ASSERT_EQ(t2.minute, 30);
    
    // Wrap around
    Time t3(23, 0, 0);
    Time t4 = add_hours(t3, 2);
    ASSERT_EQ(t4.hour, 1);
}

TEST(seconds_between_time) {
    Time t1(12, 0, 0);
    Time t2(13, 0, 0);
    ASSERT_EQ(seconds_between(t1, t2), 3600);
    
    Time t3(0, 0, 0);
    Time t4(0, 0, 30);
    ASSERT_EQ(seconds_between(t3, t4), 30);
    
    Time t5(12, 30, 0);
    Time t6(11, 30, 0);
    ASSERT_EQ(seconds_between(t5, t6), -3600);
}

// ============================================================================
// Duration Tests
// ============================================================================

TEST(duration_functions) {
    DateTime dt1(Date(2026, 4, 13), Time(0, 0, 0));
    DateTime dt2(Date(2026, 4, 13), Time(1, 30, 45));
    
    ASSERT_EQ(duration_seconds(dt1, dt2), 5445);
    ASSERT_EQ(duration_minutes(dt1, dt2), 90);
    ASSERT_EQ(duration_hours(dt1, dt2), 1);
    
    DateTime dt3(Date(2026, 4, 10), Time(0, 0, 0));
    DateTime dt4(Date(2026, 4, 13), Time(0, 0, 0));
    ASSERT_EQ(duration_days(dt3, dt4), 3);
}

TEST(humanize_duration) {
    ASSERT_EQ(humanize_duration(0), "0 seconds");
    ASSERT_EQ(humanize_duration(1), "1 second");
    ASSERT_EQ(humanize_duration(30), "30 seconds");
    ASSERT_EQ(humanize_duration(60), "1 minute");
    ASSERT_EQ(humanize_duration(90), "1 minute and 30 seconds");
    ASSERT_EQ(humanize_duration(3600), "1 hour");
    ASSERT_EQ(humanize_duration(3661), "1 hour, 1 minute and 1 second");
    ASSERT_EQ(humanize_duration(86400), "1 day");
    ASSERT_EQ(humanize_duration(90061), "1 day, 1 hour, 1 minute and 1 second");
    ASSERT_EQ(humanize_duration(172800), "2 days");
}

// ============================================================================
// Utility Tests
// ============================================================================

TEST(sleep_functions) {
    auto start = std::chrono::high_resolution_clock::now();
    sleep_ms(10);
    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    ASSERT_TRUE(elapsed >= 10);
    
    start = std::chrono::high_resolution_clock::now();
    sleep(0.01);
    end = std::chrono::high_resolution_clock::now();
    elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    ASSERT_TRUE(elapsed >= 10);
}

TEST(measure_functions) {
    int64_t ms = measure_ms([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    });
    ASSERT_TRUE(ms >= 10);
    
    int64_t us = measure_us([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    });
    ASSERT_TRUE(us >= 1000);
}

TEST(timer_class) {
    Timer timer;
    
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    
    int64_t ms = timer.elapsed_ms();
    ASSERT_TRUE(ms >= 10);
    
    int64_t us = timer.elapsed_us();
    ASSERT_TRUE(us >= 10000);
    
    double sec = timer.elapsed_seconds();
    ASSERT_TRUE(sec >= 0.01);
    
    timer.reset();
    int64_t ms2 = timer.elapsed_ms();
    ASSERT_TRUE(ms2 < ms);
}

// ============================================================================
// Timezone Tests
// ============================================================================

TEST(parse_timezone_offset) {
    ASSERT_EQ(parse_timezone_offset("Z"), 0);
    ASSERT_EQ(parse_timezone_offset("+00:00"), 0);
    ASSERT_EQ(parse_timezone_offset("+08:00"), 480);
    ASSERT_EQ(parse_timezone_offset("-05:00"), -300);
    ASSERT_EQ(parse_timezone_offset("+12:00"), 720);
    ASSERT_EQ(parse_timezone_offset("-12:00"), -720);
    ASSERT_EQ(parse_timezone_offset("+0530"), 330); // Without colon
    
    ASSERT_THROW(parse_timezone_offset("invalid"), std::invalid_argument);
}

TEST(format_timezone_offset) {
    ASSERT_EQ(format_timezone_offset(0), "Z");
    ASSERT_EQ(format_timezone_offset(480), "+08:00");
    ASSERT_EQ(format_timezone_offset(-300), "-05:00");
    ASSERT_EQ(format_timezone_offset(720), "+12:00");
    ASSERT_EQ(format_timezone_offset(-720), "-12:00");
    ASSERT_EQ(format_timezone_offset(330), "+05:30");
}

// ============================================================================
// Constants Tests
// ============================================================================

TEST(constants) {
    ASSERT_EQ(constants::SECONDS_PER_MINUTE, 60);
    ASSERT_EQ(constants::MINUTES_PER_HOUR, 60);
    ASSERT_EQ(constants::HOURS_PER_DAY, 24);
    ASSERT_EQ(constants::SECONDS_PER_HOUR, 3600);
    ASSERT_EQ(constants::SECONDS_PER_DAY, 86400);
    ASSERT_EQ(constants::DAYS_PER_WEEK, 7);
    ASSERT_EQ(constants::MONTHS_PER_YEAR, 12);
    
    ASSERT_EQ(constants::DAYS_IN_MONTH[0], 31); // January
    ASSERT_EQ(constants::DAYS_IN_MONTH[1], 28); // February (non-leap)
    ASSERT_EQ(constants::DAYS_IN_MONTH[11], 31); // December
    
    ASSERT_EQ(constants::WEEKDAY_NAMES[0], "Sunday");
    ASSERT_EQ(constants::WEEKDAY_NAMES[1], "Monday");
    ASSERT_EQ(constants::WEEKDAY_NAMES_SHORT[0], "Sun");
    
    ASSERT_EQ(constants::MONTH_NAMES[0], "January");
    ASSERT_EQ(constants::MONTH_NAMES[11], "December");
    ASSERT_EQ(constants::MONTH_NAMES_SHORT[0], "Jan");
}

// ============================================================================
// Edge Cases and Stress Tests
// ============================================================================

TEST(edge_cases) {
    // Year 2000 leap year
    ASSERT_TRUE(is_leap_year(2000));
    Date y2k(2000, 2, 29);
    ASSERT_TRUE(is_valid_date(y2k));
    
    // Century boundary
    Date d1(1999, 12, 31);
    Date d2 = add_days(d1, 1);
    ASSERT_EQ(d2.year, 2000);
    ASSERT_EQ(d2.month, 1);
    ASSERT_EQ(d2.day, 1);
    
    // Millennium boundary
    Date d3(9999, 12, 31);
    ASSERT_TRUE(is_valid_date(d3));
    
    // Max time
    Time t(23, 59, 59, 999999);
    ASSERT_TRUE(is_valid_time(t));
    
    // Min time
    Time t2(0, 0, 0, 0);
    ASSERT_TRUE(is_valid_time(t2));
    
    // Date order edge cases
    Date early(2000, 1, 1);
    Date late(2000, 12, 31);
    ASSERT_TRUE(early < late);
    ASSERT_TRUE(late > early);
}

// ============================================================================
// Main
// ============================================================================

int main() {
    std::cout << "=== datetime_utils Test Suite ===" << std::endl;
    std::cout << std::endl;
    
    // Date Structure Tests
    std::cout << "--- Date Structure Tests ---" << std::endl;
    RUN_TEST(date_constructor);
    RUN_TEST(date_comparison);
    RUN_TEST(date_to_string);
    
    // Time Structure Tests
    std::cout << std::endl << "--- Time Structure Tests ---" << std::endl;
    RUN_TEST(time_constructor);
    RUN_TEST(time_comparison);
    RUN_TEST(time_to_string);
    
    // DateTime Structure Tests
    std::cout << std::endl << "--- DateTime Structure Tests ---" << std::endl;
    RUN_TEST(datetime_constructor);
    RUN_TEST(datetime_to_string);
    
    // Validation Tests
    std::cout << std::endl << "--- Validation Tests ---" << std::endl;
    RUN_TEST(is_leap_year);
    RUN_TEST(is_valid_year);
    RUN_TEST(is_valid_month);
    RUN_TEST(days_in_month);
    RUN_TEST(is_valid_day);
    RUN_TEST(is_valid_date);
    RUN_TEST(is_valid_time);
    RUN_TEST(is_valid_datetime);
    
    // Current Time Tests
    std::cout << std::endl << "--- Current Time Tests ---" << std::endl;
    RUN_TEST(now_functions);
    
    // Parsing Tests
    std::cout << std::endl << "--- Parsing Tests ---" << std::endl;
    RUN_TEST(parse_date);
    RUN_TEST(parse_time);
    RUN_TEST(parse_datetime);
    RUN_TEST(from_timestamp);
    RUN_TEST(from_timestamp_ms);
    
    // Formatting Tests
    std::cout << std::endl << "--- Formatting Tests ---" << std::endl;
    RUN_TEST(format_date);
    RUN_TEST(format_time);
    RUN_TEST(format_datetime);
    
    // Date Arithmetic Tests
    std::cout << std::endl << "--- Date Arithmetic Tests ---" << std::endl;
    RUN_TEST(add_days);
    RUN_TEST(add_months);
    RUN_TEST(add_years);
    RUN_TEST(days_between);
    RUN_TEST(day_of_week);
    RUN_TEST(day_of_week_name);
    RUN_TEST(month_name);
    RUN_TEST(day_of_year);
    RUN_TEST(week_of_year);
    RUN_TEST(is_weekend);
    RUN_TEST(first_last_day_of_month);
    RUN_TEST(first_last_day_of_week);
    RUN_TEST(nth_weekday_of_month);
    RUN_TEST(days_in_year);
    RUN_TEST(age_in_years);
    
    // Time Arithmetic Tests
    std::cout << std::endl << "--- Time Arithmetic Tests ---" << std::endl;
    RUN_TEST(time_add_seconds);
    RUN_TEST(time_add_minutes);
    RUN_TEST(time_add_hours);
    RUN_TEST(seconds_between_time);
    
    // Duration Tests
    std::cout << std::endl << "--- Duration Tests ---" << std::endl;
    RUN_TEST(duration_functions);
    RUN_TEST(humanize_duration);
    
    // Utility Tests
    std::cout << std::endl << "--- Utility Tests ---" << std::endl;
    RUN_TEST(sleep_functions);
    RUN_TEST(measure_functions);
    RUN_TEST(timer_class);
    
    // Timezone Tests
    std::cout << std::endl << "--- Timezone Tests ---" << std::endl;
    RUN_TEST(parse_timezone_offset);
    RUN_TEST(format_timezone_offset);
    
    // Constants Tests
    std::cout << std::endl << "--- Constants Tests ---" << std::endl;
    RUN_TEST(constants);
    
    // Edge Cases Tests
    std::cout << std::endl << "--- Edge Cases Tests ---" << std::endl;
    RUN_TEST(edge_cases);
    
    // Summary
    std::cout << std::endl;
    std::cout << "=== Test Summary ===" << std::endl;
    std::cout << "Passed: " << tests_passed << std::endl;
    std::cout << "Failed: " << tests_failed << std::endl;
    
    return tests_failed > 0 ? 1 : 0;
}