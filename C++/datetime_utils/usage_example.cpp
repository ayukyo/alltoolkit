/**
 * @file usage_example.cpp
 * @brief Usage examples for datetime_utils library
 * 
 * Demonstrates all major features of the library.
 * 
 * Compile: g++ -std=c++17 -o usage_example usage_example.cpp datetime_utils.hpp
 * Run: ./usage_example
 * 
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-13
 */

#include "datetime_utils.hpp"
#include <iostream>
#include <iomanip>

using namespace datetime_utils;

void print_section(const std::string& title) {
    std::cout << "\n=== " << title << " ===\n" << std::endl;
}

int main() {
    std::cout << "datetime_utils - C++ Date and Time Utility Library\n";
    std::cout << "==================================================\n";
    
    // =====================
    // Current Time
    // =====================
    print_section("Current Time");
    
    std::cout << "Today: " << today().to_string() << std::endl;
    std::cout << "Now: " << now_datetime().to_string() << std::endl;
    std::cout << "UTC Now: " << utcnow().to_string() << std::endl;
    std::cout << "Timestamp (s): " << timestamp() << std::endl;
    std::cout << "Timestamp (ms): " << timestamp_ms() << std::endl;
    std::cout << "Timestamp (μs): " << timestamp_us() << std::endl;
    
    // =====================
    // Parsing Examples
    // =====================
    print_section("Parsing");
    
    Date d = parse_date("2026-04-13");
    std::cout << "Parsed date: " << d.to_string() << std::endl;
    
    Time t = parse_time("14:30:45.123456");
    std::cout << "Parsed time: " << t.to_string() << std::endl;
    
    DateTime dt = parse_datetime("2026-04-13T14:30:45+08:00");
    std::cout << "Parsed datetime: " << dt.to_string() << std::endl;
    
    DateTime dt_ts = from_timestamp(1704067200);
    std::cout << "From timestamp 1704067200: " << dt_ts.to_string() << std::endl;
    
    // =====================
    // Formatting Examples
    // =====================
    print_section("Formatting");
    
    Date date(2026, 4, 13);
    std::cout << "YYYY-MM-DD: " << format_date(date, "YYYY-MM-DD") << std::endl;
    std::cout << "MMMM DD, YYYY: " << format_date(date, "MMMM DD, YYYY") << std::endl;
    std::cout << "MMM DD, YY: " << format_date(date, "MMM DD, YY") << std::endl;
    std::cout << "DD/MM/YYYY: " << format_date(date, "DD/MM/YYYY") << std::endl;
    std::cout << "YYYY-M-D: " << format_date(date, "YYYY-M-D") << std::endl;
    
    Time time(14, 30, 45, 123456);
    std::cout << "\nHH:mm:ss: " << format_time(time, "HH:mm:ss") << std::endl;
    std::cout << "HH:mm:ss.SSSSSS: " << format_time(time, "HH:mm:ss.SSSSSS") << std::endl;
    std::cout << "HH:mm:ss.SSS: " << format_time(time, "HH:mm:ss.SSS") << std::endl;
    std::cout << "H:m:s: " << format_time(time, "H:m:s") << std::endl;
    
    DateTime datetime(Date(2026, 4, 13), Time(14, 30, 45));
    std::cout << "\nFull datetime: " << format_datetime(datetime, "YYYY-MM-DD HH:mm:ss") << std::endl;
    std::cout << "ISO 8601: " << to_iso_string(datetime) << std::endl;
    
    // =====================
    // Validation Examples
    // =====================
    print_section("Validation");
    
    std::cout << "Is 2024 leap year? " << (is_leap_year(2024) ? "Yes" : "No") << std::endl;
    std::cout << "Is 2000 leap year? " << (is_leap_year(2000) ? "Yes" : "No") << std::endl;
    std::cout << "Is 1900 leap year? " << (is_leap_year(1900) ? "Yes" : "No") << std::endl;
    std::cout << "Is 2023 leap year? " << (is_leap_year(2023) ? "Yes" : "No") << std::endl;
    
    std::cout << "\nDays in Feb 2024: " << days_in_month(2024, 2) << std::endl;
    std::cout << "Days in Feb 2023: " << days_in_month(2023, 2) << std::endl;
    std::cout << "Days in Apr 2026: " << days_in_month(2026, 4) << std::endl;
    
    std::cout << "\nValid date 2026-04-13? " << (is_valid_date(Date(2026, 4, 13)) ? "Yes" : "No") << std::endl;
    std::cout << "Valid date 2023-02-29? " << (is_valid_date(Date(2023, 2, 29)) ? "Yes" : "No") << std::endl;
    std::cout << "Valid date 2024-02-29? " << (is_valid_date(Date(2024, 2, 29)) ? "Yes" : "No") << std::endl;
    
    std::cout << "\nValid time 14:30:45? " << (is_valid_time(Time(14, 30, 45)) ? "Yes" : "No") << std::endl;
    std::cout << "Valid time 25:00:00? " << (is_valid_time(Time(25, 0, 0)) ? "Yes" : "No") << std::endl;
    
    // =====================
    // Date Arithmetic
    // =====================
    print_section("Date Arithmetic");
    
    Date start(2026, 4, 13);
    std::cout << "Start date: " << start.to_string() << std::endl;
    
    std::cout << "\n+1 day: " << add_days(start, 1).to_string() << std::endl;
    std::cout << "+7 days: " << add_days(start, 7).to_string() << std::endl;
    std::cout << "+30 days: " << add_days(start, 30).to_string() << std::endl;
    std::cout << "-1 day: " << add_days(start, -1).to_string() << std::endl;
    
    std::cout << "\n+1 month: " << add_months(start, 1).to_string() << std::endl;
    std::cout << "+12 months: " << add_months(start, 12).to_string() << std::endl;
    std::cout << "-4 months: " << add_months(start, -4).to_string() << std::endl;
    
    // Day adjustment example
    Date jan31(2026, 1, 31);
    std::cout << "\nJan 31 +1 month: " << add_months(jan31, 1).to_string() << " (Feb has only 28 days in 2026)" << std::endl;
    
    Date jan31_leap(2024, 1, 31);
    std::cout << "Jan 31 (leap year) +1 month: " << add_months(jan31_leap, 1).to_string() << " (Feb has 29 days in 2024)" << std::endl;
    
    std::cout << "\n+1 year: " << add_years(start, 1).to_string() << std::endl;
    std::cout << "+10 years: " << add_years(start, 10).to_string() << std::endl;
    
    // Leap year adjustment
    Date feb29(2024, 2, 29);
    std::cout << "\nFeb 29 2024 +1 year: " << add_years(feb29, 1).to_string() << " (2025 is not leap year)" << std::endl;
    
    // Days between
    Date d1(2026, 1, 1);
    Date d2(2026, 12, 31);
    std::cout << "\nDays between Jan 1 and Dec 31 2026: " << days_between(d1, d2) << std::endl;
    
    Date d3(2024, 1, 1);
    Date d4(2025, 1, 1);
    std::cout << "Days between Jan 1 2024 and Jan 1 2025: " << days_between(d3, d4) << " (leap year)" << std::endl;
    
    // =====================
    // Week Calculations
    // =====================
    print_section("Week Calculations");
    
    Date wd(2026, 4, 13);
    std::cout << "Date: " << wd.to_string() << std::endl;
    std::cout << "Day of week (0-6): " << day_of_week(wd) << " (0=Sunday, 1=Monday, ...)" << std::endl;
    std::cout << "Day name: " << day_of_week_name(wd) << std::endl;
    std::cout << "Day name (short): " << day_of_week_name(wd, true) << std::endl;
    std::cout << "Day of year: " << day_of_year(wd) << std::endl;
    std::cout << "Week of year: " << week_of_year(wd) << std::endl;
    std::cout << "Is weekend? " << (is_weekend(wd) ? "Yes" : "No") << std::endl;
    std::cout << "Is weekday? " << (is_weekday(wd) ? "Yes" : "No") << std::endl;
    
    std::cout << "\nFirst day of week: " << first_day_of_week(wd).to_string() << std::endl;
    std::cout << "Last day of week: " << last_day_of_week(wd).to_string() << std::endl;
    
    // Nth weekday
    auto second_monday = nth_weekday_of_month(2026, 4, 1, 2);
    if (second_monday) {
        std::cout << "\n2nd Monday of April 2026: " << second_monday->to_string() << std::endl;
    }
    
    auto third_friday = nth_weekday_of_month(2026, 4, 5, 3);
    if (third_friday) {
        std::cout << "3rd Friday of April 2026: " << third_friday->to_string() << std::endl;
    }
    
    auto fifth_monday = nth_weekday_of_month(2026, 4, 1, 5);
    std::cout << "5th Monday of April 2026: " << (fifth_monday ? fifth_monday->to_string() : "doesn't exist") << std::endl;
    
    // =====================
    // Month Operations
    // =====================
    print_section("Month Operations");
    
    std::cout << "Month 1 name: " << month_name(1) << std::endl;
    std::cout << "Month 12 name: " << month_name(12) << std::endl;
    std::cout << "Month 4 (short): " << month_name(4, true) << std::endl;
    
    std::cout << "\nFirst day of Apr 2026: " << first_day_of_month(2026, 4).to_string() << std::endl;
    std::cout << "Last day of Apr 2026: " << last_day_of_month(2026, 4).to_string() << std::endl;
    std::cout << "Last day of Feb 2024: " << last_day_of_month(2024, 2).to_string() << " (leap year)" << std::endl;
    std::cout << "Last day of Feb 2023: " << last_day_of_month(2023, 2).to_string() << std::endl;
    
    // =====================
    // Time Arithmetic
    // =====================
    print_section("Time Arithmetic");
    
    Time base_time(14, 30, 45);
    std::cout << "Base time: " << base_time.to_string() << std::endl;
    
    std::cout << "\n+30 seconds: " << add_seconds(base_time, 30).to_string() << std::endl;
    std::cout << "+90 minutes: " << add_minutes(base_time, 90).to_string() << std::endl;
    std::cout << "+10 hours: " << add_hours(base_time, 10).to_string() << " (wraps around midnight)" << std::endl;
    
    std::cout << "\n-45 seconds: " << add_seconds(base_time, -45).to_string() << std::endl;
    std::cout << "-60 minutes: " << add_minutes(base_time, -60).to_string() << std::endl;
    
    // Midnight wrap
    Time midnight(23, 59, 59);
    std::cout << "\n23:59:59 +1 sec: " << add_seconds(midnight, 1).to_string() << " (wraps to 00:00:00)" << std::endl;
    
    Time early(0, 0, 1);
    std::cout << "00:00:01 -1 sec: " << add_seconds(early, -1).to_string() << " (wraps to 23:59:59)" << std::endl;
    
    // Time difference
    Time t1(12, 0, 0);
    Time t2(14, 30, 0);
    std::cout << "\nSeconds between 12:00 and 14:30: " << seconds_between(t1, t2) << std::endl;
    
    // =====================
    // Duration Examples
    // =====================
    print_section("Duration");
    
    DateTime dt1(Date(2026, 4, 10), Time(0, 0, 0));
    DateTime dt2(Date(2026, 4, 13), Time(12, 30, 45));
    
    std::cout << "Between " << dt1.to_string() << " and " << dt2.to_string() << std::endl;
    std::cout << "Seconds: " << duration_seconds(dt1, dt2) << std::endl;
    std::cout << "Minutes: " << duration_minutes(dt1, dt2) << std::endl;
    std::cout << "Hours: " << duration_hours(dt1, dt2) << std::endl;
    std::cout << "Days: " << duration_days(dt1, dt2) << std::endl;
    
    // Human-readable
    std::cout << "\nHuman-readable durations:" << std::endl;
    std::cout << "0 seconds: " << humanize_duration(0) << std::endl;
    std::cout << "1 second: " << humanize_duration(1) << std::endl;
    std::cout << "90 seconds: " << humanize_duration(90) << std::endl;
    std::cout << "3600 seconds: " << humanize_duration(3600) << std::endl;
    std::cout << "86400 seconds: " << humanize_duration(86400) << std::endl;
    std::cout << "90061 seconds: " << humanize_duration(90061) << std::endl;
    std::cout << "172800 seconds: " << humanize_duration(172800) << std::endl;
    
    // =====================
    // Age Calculation
    // =====================
    print_section("Age Calculation");
    
    Date birth(2000, 4, 13);
    Date reference(2026, 4, 13);
    std::cout << "Birth: " << birth.to_string() << std::endl;
    std::cout << "Reference: " << reference.to_string() << std::endl;
    std::cout << "Age: " << age_in_years(birth, reference) << " years" << std::endl;
    
    Date before_birthday(2026, 4, 12);
    std::cout << "\nReference (before birthday): " << before_birthday.to_string() << std::endl;
    std::cout << "Age: " << age_in_years(birth, before_birthday) << " years" << std::endl;
    
    // =====================
    // Timezone
    // =====================
    print_section("Timezone");
    
    std::cout << "Parse +08:00: " << parse_timezone_offset("+08:00") << " minutes" << std::endl;
    std::cout << "Parse -05:00: " << parse_timezone_offset("-05:00") << " minutes" << std::endl;
    std::cout << "Parse Z: " << parse_timezone_offset("Z") << " minutes" << std::endl;
    
    std::cout << "\nFormat 480 minutes: " << format_timezone_offset(480) << std::endl;
    std::cout << "Format -300 minutes: " << format_timezone_offset(-300) << std::endl;
    std::cout << "Format 0 minutes: " << format_timezone_offset(0) << std::endl;
    
    // DateTime with timezone
    DateTime dt_tz(Date(2026, 4, 13), Time(14, 30, 45), 480);
    std::cout << "\nDateTime with +08:00: " << dt_tz.to_string() << std::endl;
    
    // =====================
    // Timer Utility
    // =====================
    print_section("Timer Utility");
    
    std::cout << "Measuring 100ms sleep..." << std::endl;
    int64_t ms = measure_ms([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    });
    std::cout << "Elapsed: " << ms << " ms" << std::endl;
    
    Timer timer;
    std::cout << "\nTimer started..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::cout << "Elapsed: " << timer.elapsed_ms() << " ms" << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::cout << "Elapsed: " << timer.elapsed_ms() << " ms" << std::endl;
    timer.reset();
    std::cout << "Timer reset. Elapsed: " << timer.elapsed_ms() << " ms" << std::endl;
    
    // =====================
    // Constants
    // =====================
    print_section("Constants");
    
    std::cout << "Seconds per minute: " << constants::SECONDS_PER_MINUTE << std::endl;
    std::cout << "Minutes per hour: " << constants::MINUTES_PER_HOUR << std::endl;
    std::cout << "Hours per day: " << constants::HOURS_PER_DAY << std::endl;
    std::cout << "Seconds per day: " << constants::SECONDS_PER_DAY << std::endl;
    std::cout << "Days per week: " << constants::DAYS_PER_WEEK << std::endl;
    
    std::cout << "\nWeekday names: ";
    for (const auto& name : constants::WEEKDAY_NAMES) {
        std::cout << name << " ";
    }
    std::cout << std::endl;
    
    std::cout << "Month names: ";
    for (const auto& name : constants::MONTH_NAMES) {
        std::cout << name << " ";
    }
    std::cout << std::endl;
    
    std::cout << "\n=== Examples Complete ===" << std::endl;
    
    return 0;
}