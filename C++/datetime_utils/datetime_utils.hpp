/**
 * @file datetime_utils.hpp
 * @brief Comprehensive date and time utility library for C++
 * 
 * A lightweight, header-only datetime utility library with zero external dependencies.
 * Provides formatting, parsing, calculations, and timezone-aware operations.
 * 
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-13
 */

#ifndef DATETIME_UTILS_HPP
#define DATETIME_UTILS_HPP

#include <string>
#include <chrono>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <vector>
#include <stdexcept>
#include <cstdint>
#include <cmath>
#include <array>
#include <optional>
#include <thread>

namespace datetime_utils {

// ============================================================================
// Type Definitions
// ============================================================================

using TimePoint = std::chrono::system_clock::time_point;
using Days = std::chrono::duration<int, std::ratio<86400>>;
using Hours = std::chrono::hours;
using Minutes = std::chrono::minutes;
using Seconds = std::chrono::seconds;
using Milliseconds = std::chrono::milliseconds;
using Microseconds = std::chrono::microseconds;

/**
 * @brief Represents a date (year, month, day)
 */
struct Date {
    int year;
    int month;
    int day;
    
    Date(int y = 1970, int m = 1, int d = 1) : year(y), month(m), day(d) {}
    
    bool operator==(const Date& other) const {
        return year == other.year && month == other.month && day == other.day;
    }
    
    bool operator!=(const Date& other) const { return !(*this == other); }
    
    bool operator<(const Date& other) const {
        if (year != other.year) return year < other.year;
        if (month != other.month) return month < other.month;
        return day < other.day;
    }
    
    bool operator<=(const Date& other) const { return *this < other || *this == other; }
    bool operator>(const Date& other) const { return other < *this; }
    bool operator>=(const Date& other) const { return other <= *this; }
    
    std::string to_string() const {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(4) << year << "-"
            << std::setw(2) << month << "-"
            << std::setw(2) << day;
        return oss.str();
    }
};

/**
 * @brief Represents a time (hour, minute, second, microsecond)
 */
struct Time {
    int hour;
    int minute;
    int second;
    int microsecond;
    
    Time(int h = 0, int m = 0, int s = 0, int us = 0) 
        : hour(h), minute(m), second(s), microsecond(us) {}
    
    bool operator==(const Time& other) const {
        return hour == other.hour && minute == other.minute && 
               second == other.second && microsecond == other.microsecond;
    }
    
    bool operator!=(const Time& other) const { return !(*this == other); }
    
    bool operator<(const Time& other) const {
        if (hour != other.hour) return hour < other.hour;
        if (minute != other.minute) return minute < other.minute;
        if (second != other.second) return second < other.second;
        return microsecond < other.microsecond;
    }
    
    bool operator<=(const Time& other) const { return *this < other || *this == other; }
    bool operator>(const Time& other) const { return other < *this; }
    bool operator>=(const Time& other) const { return other <= *this; }
    
    std::string to_string() const {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << hour << ":"
            << std::setw(2) << minute << ":"
            << std::setw(2) << second;
        if (microsecond > 0) {
            oss << "." << std::setw(6) << microsecond;
        }
        return oss.str();
    }
};

/**
 * @brief Represents a full datetime with optional timezone offset
 */
struct DateTime {
    Date date;
    Time time;
    int tz_offset_minutes; // Timezone offset in minutes from UTC
    
    DateTime() : date(), time(), tz_offset_minutes(0) {}
    DateTime(const Date& d, const Time& t, int tz_offset = 0)
        : date(d), time(t), tz_offset_minutes(tz_offset) {}
    
    bool operator==(const DateTime& other) const {
        return date == other.date && time == other.time && 
               tz_offset_minutes == other.tz_offset_minutes;
    }
    
    bool operator!=(const DateTime& other) const { return !(*this == other); }
    
    bool operator<(const DateTime& other) const {
        // Compare in UTC
        auto a = to_utc_timestamp();
        auto b = other.to_utc_timestamp();
        return a < b;
    }
    
    bool operator<=(const DateTime& other) const { return *this < other || *this == other; }
    bool operator>(const DateTime& other) const { return other < *this; }
    bool operator>=(const DateTime& other) const { return other <= *this; }
    
    int64_t to_utc_timestamp() const {
        std::tm tm = {};
        tm.tm_year = date.year - 1900;
        tm.tm_mon = date.month - 1;
        tm.tm_mday = date.day;
        tm.tm_hour = time.hour;
        tm.tm_min = time.minute;
        tm.tm_sec = time.second;
        tm.tm_isdst = -1;
        
        auto timestamp = static_cast<int64_t>(std::mktime(&tm));
        // Adjust for local timezone to get UTC, then apply stored offset
        // Note: This is a simplification; proper timezone handling is complex
        return timestamp - tz_offset_minutes * 60;
    }
    
    std::string to_string() const {
        std::ostringstream oss;
        oss << date.to_string() << " " << time.to_string();
        if (tz_offset_minutes != 0) {
            int offset_hours = std::abs(tz_offset_minutes) / 60;
            int offset_mins = std::abs(tz_offset_minutes) % 60;
            oss << (tz_offset_minutes >= 0 ? "+" : "-")
                << std::setfill('0') << std::setw(2) << offset_hours
                << ":" << std::setw(2) << offset_mins;
        }
        return oss.str();
    }
};

// ============================================================================
// Constants
// ============================================================================

namespace constants {
    constexpr int SECONDS_PER_MINUTE = 60;
    constexpr int MINUTES_PER_HOUR = 60;
    constexpr int HOURS_PER_DAY = 24;
    constexpr int SECONDS_PER_HOUR = 3600;
    constexpr int SECONDS_PER_DAY = 86400;
    constexpr int DAYS_PER_WEEK = 7;
    constexpr int MONTHS_PER_YEAR = 12;
    
    const std::array<int, 12> DAYS_IN_MONTH = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    const std::array<std::string, 7> WEEKDAY_NAMES = {
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    };
    const std::array<std::string, 7> WEEKDAY_NAMES_SHORT = {
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    };
    const std::array<std::string, 12> MONTH_NAMES = {
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    };
    const std::array<std::string, 12> MONTH_NAMES_SHORT = {
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    };
}

// ============================================================================
// Validation Functions
// ============================================================================

/**
 * @brief Check if a year is a leap year
 * @param year The year to check
 * @return true if leap year, false otherwise
 */
inline bool is_leap_year(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

/**
 * @brief Check if a year is valid (1000-9999)
 * @param year The year to validate
 * @return true if valid
 */
inline bool is_valid_year(int year) {
    return year >= 1000 && year <= 9999;
}

/**
 * @brief Check if a month is valid (1-12)
 * @param month The month to validate
 * @return true if valid
 */
inline bool is_valid_month(int month) {
    return month >= 1 && month <= 12;
}

/**
 * @brief Get the number of days in a specific month
 * @param year The year
 * @param month The month (1-12)
 * @return Number of days in the month
 * @throws std::invalid_argument if month is invalid
 */
inline int days_in_month(int year, int month) {
    if (!is_valid_month(month)) {
        throw std::invalid_argument("Invalid month: " + std::to_string(month));
    }
    if (month == 2 && is_leap_year(year)) {
        return 29;
    }
    return constants::DAYS_IN_MONTH[month - 1];
}

/**
 * @brief Check if a day is valid for the given year and month
 * @param year The year
 * @param month The month
 * @param day The day to validate
 * @return true if valid
 */
inline bool is_valid_day(int year, int month, int day) {
    if (!is_valid_month(month)) return false;
    return day >= 1 && day <= days_in_month(year, month);
}

/**
 * @brief Validate a date
 * @param date The date to validate
 * @return true if the date is valid
 */
inline bool is_valid_date(const Date& date) {
    return is_valid_year(date.year) && 
           is_valid_month(date.month) && 
           is_valid_day(date.year, date.month, date.day);
}

/**
 * @brief Validate a time
 * @param time The time to validate
 * @return true if the time is valid
 */
inline bool is_valid_time(const Time& time) {
    return time.hour >= 0 && time.hour < 24 &&
           time.minute >= 0 && time.minute < 60 &&
           time.second >= 0 && time.second < 60 &&
           time.microsecond >= 0 && time.microsecond < 1000000;
}

/**
 * @brief Validate a datetime
 * @param dt The datetime to validate
 * @return true if the datetime is valid
 */
inline bool is_valid_datetime(const DateTime& dt) {
    return is_valid_date(dt.date) && is_valid_time(dt.time);
}

// ============================================================================
// Current Time Functions
// ============================================================================

/**
 * @brief Get the current time point
 * @return Current system time point
 */
inline TimePoint now() {
    return std::chrono::system_clock::now();
}

/**
 * @brief Get current date
 * @return Current date
 */
inline Date today() {
    auto now_time = now();
    std::time_t tt = std::chrono::system_clock::to_time_t(now_time);
    std::tm* tm = std::localtime(&tt);
    return Date(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday);
}

/**
 * @brief Get current datetime
 * @return Current datetime
 */
inline DateTime now_datetime() {
    auto now_time = now();
    std::time_t tt = std::chrono::system_clock::to_time_t(now_time);
    auto us = std::chrono::duration_cast<Microseconds>(
        now_time.time_since_epoch() % Seconds(1)
    );
    
    std::tm* tm = std::localtime(&tt);
    DateTime dt;
    dt.date = Date(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday);
    dt.time = Time(tm->tm_hour, tm->tm_min, tm->tm_sec, static_cast<int>(us.count()));
    dt.tz_offset_minutes = 0; // localtime already adjusted
    
    return dt;
}

/**
 * @brief Get current UTC datetime
 * @return Current UTC datetime
 */
inline DateTime utcnow() {
    auto now_time = now();
    std::time_t tt = std::chrono::system_clock::to_time_t(now_time);
    auto us = std::chrono::duration_cast<Microseconds>(
        now_time.time_since_epoch() % Seconds(1)
    );
    
    std::tm* tm = std::gmtime(&tt);
    DateTime dt;
    dt.date = Date(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday);
    dt.time = Time(tm->tm_hour, tm->tm_min, tm->tm_sec, static_cast<int>(us.count()));
    dt.tz_offset_minutes = 0;
    
    return dt;
}

/**
 * @brief Get Unix timestamp (seconds since epoch)
 * @return Unix timestamp
 */
inline int64_t timestamp() {
    return std::chrono::duration_cast<Seconds>(
        now().time_since_epoch()
    ).count();
}

/**
 * @brief Get Unix timestamp in milliseconds
 * @return Unix timestamp in milliseconds
 */
inline int64_t timestamp_ms() {
    return std::chrono::duration_cast<Milliseconds>(
        now().time_since_epoch()
    ).count();
}

/**
 * @brief Get Unix timestamp in microseconds
 * @return Unix timestamp in microseconds
 */
inline int64_t timestamp_us() {
    return std::chrono::duration_cast<Microseconds>(
        now().time_since_epoch()
    ).count();
}

// ============================================================================
// Parsing Functions
// ============================================================================

/**
 * @brief Parse a date string in ISO format (YYYY-MM-DD)
 * @param date_str The date string
 * @return Parsed date
 * @throws std::invalid_argument if parsing fails
 */
inline Date parse_date(const std::string& date_str) {
    if (date_str.length() < 10) {
        throw std::invalid_argument("Invalid date format: " + date_str);
    }
    
    try {
        int year = std::stoi(date_str.substr(0, 4));
        int month = std::stoi(date_str.substr(5, 2));
        int day = std::stoi(date_str.substr(8, 2));
        
        Date date(year, month, day);
        if (!is_valid_date(date)) {
            throw std::invalid_argument("Invalid date: " + date_str);
        }
        return date;
    } catch (const std::exception& e) {
        throw std::invalid_argument("Failed to parse date: " + date_str);
    }
}

/**
 * @brief Parse a time string (HH:MM:SS or HH:MM:SS.microseconds)
 * @param time_str The time string
 * @return Parsed time
 * @throws std::invalid_argument if parsing fails
 */
inline Time parse_time(const std::string& time_str) {
    if (time_str.length() < 8) {
        throw std::invalid_argument("Invalid time format: " + time_str);
    }
    
    try {
        int hour = std::stoi(time_str.substr(0, 2));
        int minute = std::stoi(time_str.substr(3, 2));
        int second = std::stoi(time_str.substr(6, 2));
        int microsecond = 0;
        
        if (time_str.length() > 8 && time_str[8] == '.') {
            // Parse microseconds
            size_t us_start = 9;
            size_t us_end = time_str.find_first_not_of("0123456789", us_start);
            if (us_end == std::string::npos) us_end = time_str.length();
            std::string us_str = time_str.substr(us_start, us_end - us_start);
            // Pad or truncate to 6 digits
            while (us_str.length() < 6) us_str += "0";
            if (us_str.length() > 6) us_str = us_str.substr(0, 6);
            microsecond = std::stoi(us_str);
        }
        
        Time time(hour, minute, second, microsecond);
        if (!is_valid_time(time)) {
            throw std::invalid_argument("Invalid time: " + time_str);
        }
        return time;
    } catch (const std::exception& e) {
        throw std::invalid_argument("Failed to parse time: " + time_str);
    }
}

/**
 * @brief Parse a datetime string in ISO format
 * @param datetime_str The datetime string (YYYY-MM-DD HH:MM:SS or with timezone)
 * @return Parsed datetime
 * @throws std::invalid_argument if parsing fails
 */
inline DateTime parse_datetime(const std::string& datetime_str) {
    if (datetime_str.length() < 19) {
        throw std::invalid_argument("Invalid datetime format: " + datetime_str);
    }
    
    try {
        Date date = parse_date(datetime_str.substr(0, 10));
        
        // Skip the separator (space or 'T')
        size_t time_start = 10;
        if (datetime_str[time_start] == ' ' || datetime_str[time_start] == 'T') {
            time_start++;
        }
        
        // Find end of time part
        size_t time_end = datetime_str.find_first_of("+-Z", time_start);
        if (time_end == std::string::npos) time_end = datetime_str.length();
        
        Time time = parse_time(datetime_str.substr(time_start, time_end - time_start));
        
        // Parse timezone offset if present
        int tz_offset = 0;
        if (time_end < datetime_str.length()) {
            char tz_sign = datetime_str[time_end];
            if (tz_sign == 'Z') {
                tz_offset = 0;
            } else {
                int tz_hour = std::stoi(datetime_str.substr(time_end + 1, 2));
                int tz_min = 0;
                if (datetime_str.length() > time_end + 4 && datetime_str[time_end + 3] == ':') {
                    tz_min = std::stoi(datetime_str.substr(time_end + 4, 2));
                }
                tz_offset = tz_hour * 60 + tz_min;
                if (tz_sign == '-') tz_offset = -tz_offset;
            }
        }
        
        return DateTime(date, time, tz_offset);
    } catch (const std::exception& e) {
        throw std::invalid_argument("Failed to parse datetime: " + datetime_str);
    }
}

/**
 * @brief Parse Unix timestamp to DateTime
 * @param ts Unix timestamp in seconds
 * @return DateTime
 */
inline DateTime from_timestamp(int64_t ts) {
    std::time_t tt = static_cast<std::time_t>(ts);
    std::tm* tm = std::gmtime(&tt);
    return DateTime(
        Date(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday),
        Time(tm->tm_hour, tm->tm_min, tm->tm_sec),
        0
    );
}

/**
 * @brief Parse Unix timestamp in milliseconds to DateTime
 * @param ts_ms Unix timestamp in milliseconds
 * @return DateTime
 */
inline DateTime from_timestamp_ms(int64_t ts_ms) {
    int64_t ts = ts_ms / 1000;
    int us = (ts_ms % 1000) * 1000;
    std::time_t tt = static_cast<std::time_t>(ts);
    std::tm* tm = std::gmtime(&tt);
    return DateTime(
        Date(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday),
        Time(tm->tm_hour, tm->tm_min, tm->tm_sec, us),
        0
    );
}

// ============================================================================
// Formatting Functions
// ============================================================================

/**
 * @brief Format date in custom format
 * @param date The date
 * @param format Format string (supports: YYYY, YY, MM, M, DD, D, MMM, MMMM)
 * @return Formatted string
 */
inline std::string format_date(const Date& date, const std::string& format = "YYYY-MM-DD") {
    std::string result = format;
    
    // Replace in order of length (longest first)
    size_t pos;
    
    // YYYY
    while ((pos = result.find("YYYY")) != std::string::npos) {
        result.replace(pos, 4, std::to_string(date.year));
    }
    
    // MMMM
    while ((pos = result.find("MMMM")) != std::string::npos) {
        result.replace(pos, 4, constants::MONTH_NAMES[date.month - 1]);
    }
    
    // MMM
    while ((pos = result.find("MMM")) != std::string::npos) {
        result.replace(pos, 3, constants::MONTH_NAMES_SHORT[date.month - 1]);
    }
    
    // DD
    while ((pos = result.find("DD")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << date.day;
        result.replace(pos, 2, oss.str());
    }
    
    // MM
    while ((pos = result.find("MM")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << date.month;
        result.replace(pos, 2, oss.str());
    }
    
    // YY
    while ((pos = result.find("YY")) != std::string::npos) {
        result.replace(pos, 2, std::to_string(date.year % 100));
    }
    
    // D
    while ((pos = result.find("D")) != std::string::npos) {
        result.replace(pos, 1, std::to_string(date.day));
    }
    
    // M
    while ((pos = result.find("M")) != std::string::npos) {
        result.replace(pos, 1, std::to_string(date.month));
    }
    
    return result;
}

/**
 * @brief Format time in custom format
 * @param time The time
 * @param format Format string (supports: HH, H, mm, m, ss, s, SSSSSS)
 * @return Formatted string
 */
inline std::string format_time(const Time& time, const std::string& format = "HH:mm:ss") {
    std::string result = format;
    
    size_t pos;
    
    // SSSSSS (microseconds, 6 digits)
    while ((pos = result.find("SSSSSS")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(6) << time.microsecond;
        result.replace(pos, 6, oss.str());
    }
    
    // SSS (milliseconds, 3 digits)
    while ((pos = result.find("SSS")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(3) << (time.microsecond / 1000);
        result.replace(pos, 3, oss.str());
    }
    
    // HH
    while ((pos = result.find("HH")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << time.hour;
        result.replace(pos, 2, oss.str());
    }
    
    // mm
    while ((pos = result.find("mm")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << time.minute;
        result.replace(pos, 2, oss.str());
    }
    
    // ss
    while ((pos = result.find("ss")) != std::string::npos) {
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << time.second;
        result.replace(pos, 2, oss.str());
    }
    
    // H
    while ((pos = result.find("H")) != std::string::npos) {
        result.replace(pos, 1, std::to_string(time.hour));
    }
    
    // m
    while ((pos = result.find("m")) != std::string::npos) {
        result.replace(pos, 1, std::to_string(time.minute));
    }
    
    // s
    while ((pos = result.find("s")) != std::string::npos) {
        result.replace(pos, 1, std::to_string(time.second));
    }
    
    return result;
}

/**
 * @brief Format datetime in ISO 8601 format
 * @param dt The datetime
 * @return ISO 8601 formatted string
 */
inline std::string to_iso_string(const DateTime& dt) {
    return dt.to_string();
}

/**
 * @brief Format datetime with custom format
 * @param dt The datetime
 * @param format Format string
 * @return Formatted string
 */
inline std::string format_datetime(const DateTime& dt, const std::string& format = "YYYY-MM-DD HH:mm:ss") {
    std::string result = format;
    
    // First handle date and time parts
    result = format_date(dt.date, result);
    result = format_time(dt.time, result);
    
    return result;
}

// ============================================================================
// Date Arithmetic Functions
// ============================================================================

/**
 * @brief Add days to a date
 * @param date The date
 * @param days Number of days to add (can be negative)
 * @return New date
 */
inline Date add_days(const Date& date, int days) {
    std::tm tm = {};
    tm.tm_year = date.year - 1900;
    tm.tm_mon = date.month - 1;
    tm.tm_mday = date.day;
    tm.tm_hour = 12; // Noon to avoid DST issues
    tm.tm_isdst = -1;
    
    tm.tm_mday += days;
    std::mktime(&tm); // Normalize
    
    return Date(tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday);
}

/**
 * @brief Add months to a date
 * @param date The date
 * @param months Number of months to add (can be negative)
 * @return New date
 */
inline Date add_months(const Date& date, int months) {
    int total_months = date.year * 12 + date.month - 1 + months;
    int new_year = total_months / 12;
    int new_month = (total_months % 12) + 1;
    
    // Adjust day if necessary
    int max_day = days_in_month(new_year, new_month);
    int new_day = std::min(date.day, max_day);
    
    return Date(new_year, new_month, new_day);
}

/**
 * @brief Add years to a date
 * @param date The date
 * @param years Number of years to add (can be negative)
 * @return New date
 */
inline Date add_years(const Date& date, int years) {
    int new_year = date.year + years;
    int new_day = date.day;
    
    // Handle Feb 29 in leap years
    if (date.month == 2 && date.day == 29 && !is_leap_year(new_year)) {
        new_day = 28;
    }
    
    return Date(new_year, date.month, new_day);
}

/**
 * @brief Calculate difference in days between two dates
 * @param date1 First date
 * @param date2 Second date
 * @return Number of days (positive if date2 > date1)
 */
inline int days_between(const Date& date1, const Date& date2) {
    auto to_days = [](const Date& d) -> int {
        int y = d.year;
        int m = d.month;
        int day = d.day;
        
        // Algorithm to convert date to day number
        if (m <= 2) {
            y--;
            m += 12;
        }
        
        int era = (y >= 0 ? y : y - 399) / 400;
        int yoe = y - era * 400;
        int doy = (153 * (m - 3) + 2) / 5 + day - 1;
        int doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return era * 146097 + doe - 719468;
    };
    
    return to_days(date2) - to_days(date1);
}

/**
 * @brief Get the day of the week (0=Sunday, 1=Monday, ..., 6=Saturday)
 * @param date The date
 * @return Day of week (0-6)
 */
inline int day_of_week(const Date& date) {
    std::tm tm = {};
    tm.tm_year = date.year - 1900;
    tm.tm_mon = date.month - 1;
    tm.tm_mday = date.day;
    tm.tm_hour = 12;
    tm.tm_isdst = -1;
    std::mktime(&tm);
    return tm.tm_wday;
}

/**
 * @brief Get the name of the day of the week
 * @param date The date
 * @param short_name If true, return short name (e.g., "Mon")
 * @return Day name
 */
inline std::string day_of_week_name(const Date& date, bool short_name = false) {
    int dow = day_of_week(date);
    return short_name ? constants::WEEKDAY_NAMES_SHORT[dow] : constants::WEEKDAY_NAMES[dow];
}

/**
 * @brief Get the month name
 * @param month Month number (1-12)
 * @param short_name If true, return short name (e.g., "Jan")
 * @return Month name
 */
inline std::string month_name(int month, bool short_name = false) {
    if (!is_valid_month(month)) {
        throw std::invalid_argument("Invalid month: " + std::to_string(month));
    }
    return short_name ? constants::MONTH_NAMES_SHORT[month - 1] : constants::MONTH_NAMES[month - 1];
}

/**
 * @brief Get the day of year (1-366)
 * @param date The date
 * @return Day of year
 */
inline int day_of_year(const Date& date) {
    int doy = date.day;
    for (int m = 1; m < date.month; ++m) {
        doy += days_in_month(date.year, m);
    }
    return doy;
}

/**
 * @brief Get the week of year
 * @param date The date
 * @return Week of year (1-53)
 */
inline int week_of_year(const Date& date) {
    std::tm tm = {};
    tm.tm_year = date.year - 1900;
    tm.tm_mon = date.month - 1;
    tm.tm_mday = date.day;
    tm.tm_hour = 12;
    tm.tm_isdst = -1;
    std::mktime(&tm);
    
    char week_str[3];
    std::strftime(week_str, sizeof(week_str), "%V", &tm);
    return std::stoi(week_str);
}

/**
 * @brief Check if a date is a weekend (Saturday or Sunday)
 * @param date The date
 * @return true if weekend
 */
inline bool is_weekend(const Date& date) {
    int dow = day_of_week(date);
    return dow == 0 || dow == 6; // Sunday or Saturday
}

/**
 * @brief Check if a date is a weekday (Monday-Friday)
 * @param date The date
 * @return true if weekday
 */
inline bool is_weekday(const Date& date) {
    return !is_weekend(date);
}

/**
 * @brief Get the first day of a month
 * @param year Year
 * @param month Month
 * @return First day of month
 */
inline Date first_day_of_month(int year, int month) {
    return Date(year, month, 1);
}

/**
 * @brief Get the last day of a month
 * @param year Year
 * @param month Month
 * @return Last day of month
 */
inline Date last_day_of_month(int year, int month) {
    return Date(year, month, days_in_month(year, month));
}

/**
 * @brief Get the first day of a week (Monday)
 * @param date The date
 * @return First day of the week (Monday)
 */
inline Date first_day_of_week(const Date& date) {
    int dow = day_of_week(date);
    int days_to_monday = (dow == 0) ? -6 : (1 - dow);
    return add_days(date, days_to_monday);
}

/**
 * @brief Get the last day of a week (Sunday)
 * @param date The date
 * @return Last day of the week (Sunday)
 */
inline Date last_day_of_week(const Date& date) {
    int dow = day_of_week(date);
    int days_to_sunday = (dow == 0) ? 0 : (7 - dow);
    return add_days(date, days_to_sunday);
}

/**
 * @brief Get the date of the nth occurrence of a weekday in a month
 * @param year Year
 * @param month Month
 * @param weekday Weekday (0=Sunday, 1=Monday, ..., 6=Saturday)
 * @param n Nth occurrence (1-5, negative for from end)
 * @return The date, or empty if not found
 */
inline std::optional<Date> nth_weekday_of_month(int year, int month, int weekday, int n) {
    if (!is_valid_month(month) || weekday < 0 || weekday > 6) {
        return std::nullopt;
    }
    
    if (n > 0) {
        // Find nth occurrence from start
        Date d = first_day_of_month(year, month);
        int first_dow = day_of_week(d);
        int days_until = (weekday - first_dow + 7) % 7;
        d = add_days(d, days_until);
        d = add_days(d, (n - 1) * 7);
        
        if (d.month == month) {
            return d;
        }
        return std::nullopt;
    } else {
        // Find nth occurrence from end
        Date d = last_day_of_month(year, month);
        int last_dow = day_of_week(d);
        int days_since = (last_dow - weekday + 7) % 7;
        d = add_days(d, -days_since);
        d = add_days(d, (n + 1) * 7);
        
        if (d.month == month) {
            return d;
        }
        return std::nullopt;
    }
}

/**
 * @brief Get the number of days in a year
 * @param year The year
 * @return 365 or 366
 */
inline int days_in_year(int year) {
    return is_leap_year(year) ? 366 : 365;
}

/**
 * @brief Get age in years
 * @param birth_date Birth date
 * @param reference_date Reference date (default: today)
 * @return Age in years
 */
inline int age_in_years(const Date& birth_date, const Date& reference_date = today()) {
    int age = reference_date.year - birth_date.year;
    if (reference_date.month < birth_date.month ||
        (reference_date.month == birth_date.month && reference_date.day < birth_date.day)) {
        age--;
    }
    return age;
}

// ============================================================================
// Time Arithmetic Functions
// ============================================================================

/**
 * @brief Add seconds to a time
 * @param time The time
 * @param seconds Seconds to add (can be negative)
 * @return New time (wraps around at midnight)
 */
inline Time add_seconds(const Time& time, int seconds) {
    int total_seconds = time.hour * 3600 + time.minute * 60 + time.second + seconds;
    
    // Handle wrap-around
    while (total_seconds < 0) total_seconds += constants::SECONDS_PER_DAY;
    total_seconds %= constants::SECONDS_PER_DAY;
    
    return Time(
        total_seconds / 3600,
        (total_seconds % 3600) / 60,
        total_seconds % 60,
        time.microsecond
    );
}

/**
 * @brief Add minutes to a time
 * @param time The time
 * @param minutes Minutes to add (can be negative)
 * @return New time (wraps around at midnight)
 */
inline Time add_minutes(const Time& time, int minutes) {
    return add_seconds(time, minutes * 60);
}

/**
 * @brief Add hours to a time
 * @param time The time
 * @param hours Hours to add (can be negative)
 * @return New time (wraps around at midnight)
 */
inline Time add_hours(const Time& time, int hours) {
    return add_seconds(time, hours * 3600);
}

/**
 * @brief Calculate difference in seconds between two times
 * @param time1 First time
 * @param time2 Second time
 * @return Seconds difference
 */
inline int seconds_between(const Time& time1, const Time& time2) {
    int s1 = time1.hour * 3600 + time1.minute * 60 + time1.second;
    int s2 = time2.hour * 3600 + time2.minute * 60 + time2.second;
    return s2 - s1;
}

// ============================================================================
// Duration Functions
// ============================================================================

/**
 * @brief Calculate duration between two datetimes in seconds
 * @param dt1 First datetime
 * @param dt2 Second datetime
 * @return Duration in seconds
 */
inline int64_t duration_seconds(const DateTime& dt1, const DateTime& dt2) {
    return dt2.to_utc_timestamp() - dt1.to_utc_timestamp();
}

/**
 * @brief Calculate duration between two datetimes in minutes
 * @param dt1 First datetime
 * @param dt2 Second datetime
 * @return Duration in minutes
 */
inline int64_t duration_minutes(const DateTime& dt1, const DateTime& dt2) {
    return duration_seconds(dt1, dt2) / 60;
}

/**
 * @brief Calculate duration between two datetimes in hours
 * @param dt1 First datetime
 * @param dt2 Second datetime
 * @return Duration in hours
 */
inline int64_t duration_hours(const DateTime& dt1, const DateTime& dt2) {
    return duration_seconds(dt1, dt2) / 3600;
}

/**
 * @brief Calculate duration between two datetimes in days
 * @param dt1 First datetime
 * @param dt2 Second datetime
 * @return Duration in days
 */
inline int64_t duration_days(const DateTime& dt1, const DateTime& dt2) {
    return duration_seconds(dt1, dt2) / 86400;
}

/**
 * @brief Human-readable duration
 * @param seconds Duration in seconds
 * @return Human-readable string (e.g., "2 hours 30 minutes")
 */
inline std::string humanize_duration(int64_t seconds) {
    std::vector<std::string> parts;
    
    int64_t days = seconds / 86400;
    seconds %= 86400;
    int64_t hours = seconds / 3600;
    seconds %= 3600;
    int64_t minutes = seconds / 60;
    seconds %= 60;
    
    if (days > 0) {
        parts.push_back(std::to_string(days) + (days == 1 ? " day" : " days"));
    }
    if (hours > 0) {
        parts.push_back(std::to_string(hours) + (hours == 1 ? " hour" : " hours"));
    }
    if (minutes > 0) {
        parts.push_back(std::to_string(minutes) + (minutes == 1 ? " minute" : " minutes"));
    }
    if (seconds > 0 || parts.empty()) {
        parts.push_back(std::to_string(seconds) + (seconds == 1 ? " second" : " seconds"));
    }
    
    std::ostringstream oss;
    for (size_t i = 0; i < parts.size(); ++i) {
        if (i > 0) {
            oss << (i == parts.size() - 1 ? " and " : ", ");
        }
        oss << parts[i];
    }
    return oss.str();
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * @brief Sleep for a specified duration
 * @param milliseconds Duration in milliseconds
 */
inline void sleep_ms(int64_t milliseconds) {
    std::this_thread::sleep_for(std::chrono::milliseconds(milliseconds));
}

/**
 * @brief Sleep for a specified duration
 * @param seconds Duration in seconds
 */
inline void sleep(double seconds) {
    std::this_thread::sleep_for(std::chrono::duration<double>(seconds));
}

/**
 * @brief Measure execution time of a function
 * @tparam Func Function type
 * @param func Function to measure
 * @return Execution time in milliseconds
 */
template<typename Func>
inline int64_t measure_ms(Func&& func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
}

/**
 * @brief Measure execution time of a function in microseconds
 * @tparam Func Function type
 * @param func Function to measure
 * @return Execution time in microseconds
 */
template<typename Func>
inline int64_t measure_us(Func&& func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
}

/**
 * @brief Create a timer object for measuring elapsed time
 */
class Timer {
public:
    Timer() : start_(std::chrono::high_resolution_clock::now()) {}
    
    void reset() {
        start_ = std::chrono::high_resolution_clock::now();
    }
    
    int64_t elapsed_ms() const {
        auto now = std::chrono::high_resolution_clock::now();
        return std::chrono::duration_cast<std::chrono::milliseconds>(now - start_).count();
    }
    
    int64_t elapsed_us() const {
        auto now = std::chrono::high_resolution_clock::now();
        return std::chrono::duration_cast<std::chrono::microseconds>(now - start_).count();
    }
    
    double elapsed_seconds() const {
        auto now = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<double>(now - start_).count();
    }
    
private:
    std::chrono::high_resolution_clock::time_point start_;
};

/**
 * @brief Parse timezone offset string (e.g., "+08:00", "-05:00")
 * @param tz_str Timezone offset string
 * @return Offset in minutes
 * @throws std::invalid_argument if parsing fails
 */
inline int parse_timezone_offset(const std::string& tz_str) {
    if (tz_str.empty() || tz_str == "Z") {
        return 0;
    }
    
    if (tz_str.length() < 3) {
        throw std::invalid_argument("Invalid timezone offset: " + tz_str);
    }
    
    char sign = tz_str[0];
    if (sign != '+' && sign != '-') {
        throw std::invalid_argument("Invalid timezone offset: " + tz_str);
    }
    
    try {
        int hours = std::stoi(tz_str.substr(1, 2));
        int minutes = 0;
        
        if (tz_str.length() >= 5 && tz_str[3] == ':') {
            minutes = std::stoi(tz_str.substr(4, 2));
        } else if (tz_str.length() >= 5) {
            minutes = std::stoi(tz_str.substr(3, 2));
        }
        
        int offset = hours * 60 + minutes;
        return (sign == '-') ? -offset : offset;
    } catch (const std::exception&) {
        throw std::invalid_argument("Invalid timezone offset: " + tz_str);
    }
}

/**
 * @brief Format timezone offset as string
 * @param offset_minutes Offset in minutes
 * @return Timezone offset string (e.g., "+08:00")
 */
inline std::string format_timezone_offset(int offset_minutes) {
    if (offset_minutes == 0) {
        return "Z";
    }
    
    std::ostringstream oss;
    oss << (offset_minutes >= 0 ? "+" : "-");
    int hours = std::abs(offset_minutes) / 60;
    int minutes = std::abs(offset_minutes) % 60;
    oss << std::setfill('0') << std::setw(2) << hours << ":"
        << std::setw(2) << minutes;
    return oss.str();
}

} // namespace datetime_utils

#endif // DATETIME_UTILS_HPP