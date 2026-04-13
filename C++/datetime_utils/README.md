# datetime_utils - C++ Date and Time Utility Library

A comprehensive, header-only date and time utility library for C++ with zero external dependencies.

## Features

- **Zero External Dependencies**: Single header file, pure C++17
- **Comprehensive Date Handling**: Date validation, formatting, parsing, arithmetic
- **Time Operations**: Time validation, parsing, formatting, addition/subtraction
- **DateTime Support**: Full datetime with timezone offset support
- **ISO 8601 Compliant**: Standard datetime format parsing and formatting
- **Leap Year Support**: Correct handling of leap years (including century rules)
- **Date Arithmetic**: Add/subtract days, months, years
- **Week Calculations**: Day of week, week of year, ISO week support
- **Duration Calculations**: Human-readable duration formatting
- **Timer Utility**: High-resolution timer for performance measurement
- **100% Test Coverage**: Comprehensive test suite included

## Installation

Simply include the header file in your project:

```cpp
#include "datetime_utils.hpp"
```

## Quick Start

### Current Time

```cpp
#include "datetime_utils.hpp"
using namespace datetime_utils;

// Get current date
Date today = today();
std::cout << "Today: " << today.to_string() << std::endl; // 2026-04-13

// Get current datetime
DateTime now = now_datetime();
std::cout << "Now: " << now.to_string() << std::endl; // 2026-04-13 14:30:45

// Get Unix timestamp
int64_t ts = timestamp();
int64_t ts_ms = timestamp_ms();
int64_t ts_us = timestamp_us();
```

### Parsing

```cpp
// Parse date
Date d = parse_date("2026-04-13");

// Parse time
Time t = parse_time("14:30:45.123456");

// Parse datetime
DateTime dt = parse_datetime("2026-04-13T14:30:45+08:00");

// Parse from timestamp
DateTime dt2 = from_timestamp(1704067200);
DateTime dt3 = from_timestamp_ms(1704067200123);
```

### Formatting

```cpp
Date d(2026, 4, 13);

// Standard format
format_date(d, "YYYY-MM-DD");  // 2026-04-13

// Custom formats
format_date(d, "MMMM DD, YYYY");    // April 13, 2026
format_date(d, "MMM DD, YY");       // Apr 13, 26
format_date(d, "DD/MM/YYYY");       // 13/04/2026

Time t(14, 30, 45, 123456);
format_time(t, "HH:mm:ss.SSSSSS");  // 14:30:45.123456
format_time(t, "HH:mm:ss");         // 14:30:45

DateTime dt(Date(2026, 4, 13), Time(14, 30, 45));
to_iso_string(dt);  // 2026-04-13 14:30:45
```

### Date Arithmetic

```cpp
Date d(2026, 4, 13);

// Add/subtract days
Date d1 = add_days(d, 1);    // 2026-04-14
Date d2 = add_days(d, -7);   // 2026-04-06

// Add/subtract months
Date d3 = add_months(d, 2);  // 2026-06-13
Date d4 = add_months(d, -1); // 2026-03-13

// Add/subtract years
Date d5 = add_years(d, 1);   // 2027-04-13

// Days between dates
int days = days_between(Date(2026, 1, 1), Date(2026, 12, 31)); // 364
```

### Week Calculations

```cpp
Date d(2026, 4, 13);

// Day of week (0=Sunday, 1=Monday, ..., 6=Saturday)
int dow = day_of_week(d);  // 1 (Monday)

// Day name
std::string name = day_of_week_name(d);      // "Monday"
std::string short_name = day_of_week_name(d, true); // "Mon"

// Week of year
int week = week_of_year(d);

// Check weekend
bool weekend = is_weekend(d);  // false
bool weekday = is_weekday(d);  // true
```

### Time Arithmetic

```cpp
Time t(14, 30, 45);

Time t1 = add_seconds(t, 30);   // 14:31:15
Time t2 = add_minutes(t, 90);   // 15:30:45
Time t3 = add_hours(t, 10);     // 00:30:45 (wraps around)

// Seconds between times
int secs = seconds_between(Time(12, 0, 0), Time(13, 0, 0)); // 3600
```

### Duration

```cpp
// Calculate duration between datetimes
DateTime dt1(Date(2026, 4, 10), Time(0, 0, 0));
DateTime dt2(Date(2026, 4, 13), Time(12, 0, 0));

int64_t secs = duration_seconds(dt1, dt2);
int64_t mins = duration_minutes(dt1, dt2);
int64_t hrs = duration_hours(dt1, dt2);
int64_t days = duration_days(dt1, dt2);

// Human-readable duration
std::string human = humanize_duration(90061); // "1 day, 1 hour, 1 minute and 1 second"
```

### Utility Functions

```cpp
// Validation
bool valid_date = is_valid_date(Date(2026, 4, 13));
bool valid_time = is_valid_time(Time(14, 30, 45));
bool leap = is_leap_year(2024);  // true

// Leap year rules
is_leap_year(2000);  // true (divisible by 400)
is_leap_year(1900);  // false (divisible by 100, not 400)
is_leap_year(2024);  // true (divisible by 4)

// Days in month
int days = days_in_month(2024, 2);  // 29 (leap year)
int days2 = days_in_month(2023, 2); // 28

// Month/Year boundaries
Date first = first_day_of_month(2026, 4);  // 2026-04-01
Date last = last_day_of_month(2026, 4);    // 2026-04-30
Date first_week = first_day_of_week(d);    // Monday of that week
Date last_week = last_day_of_week(d);      // Sunday of that week

// Age calculation
Date birth(2000, 4, 13);
int age = age_in_years(birth);  // Current age

// Nth weekday of month
auto second_monday = nth_weekday_of_month(2026, 4, 1, 2); // 2026-04-13
```

### Timer Utility

```cpp
// Measure execution time
int64_t ms = measure_ms([]() {
    // Your code here
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
});

// Timer class
Timer timer;
// ... do work ...
std::cout << "Elapsed: " << timer.elapsed_ms() << " ms" << std::endl;
timer.reset(); // Reset timer
```

### Timezone Support

```cpp
// Parse timezone offset
int offset = parse_timezone_offset("+08:00");  // 480 minutes
int offset2 = parse_timezone_offset("-05:00"); // -300 minutes

// Format timezone offset
std::string tz1 = format_timezone_offset(480);   // "+08:00"
std::string tz2 = format_timezone_offset(0);     // "Z"

// Create datetime with timezone
DateTime dt(Date(2026, 4, 13), Time(14, 30, 45), 480);
```

## API Reference

### Types

| Type | Description |
|------|-------------|
| `Date` | Year, month, day structure |
| `Time` | Hour, minute, second, microsecond structure |
| `DateTime` | Full datetime with timezone offset |
| `TimePoint` | `std::chrono::system_clock::time_point` |
| `Timer` | High-resolution timer class |

### Current Time Functions

| Function | Returns |
|----------|---------|
| `now()` | Current `TimePoint` |
| `today()` | Current `Date` |
| `now_datetime()` | Current `DateTime` (local) |
| `utcnow()` | Current `DateTime` (UTC) |
| `timestamp()` | Unix timestamp (seconds) |
| `timestamp_ms()` | Unix timestamp (milliseconds) |
| `timestamp_us()` | Unix timestamp (microseconds) |

### Parsing Functions

| Function | Input | Output |
|----------|-------|--------|
| `parse_date(str)` | `"YYYY-MM-DD"` | `Date` |
| `parse_time(str)` | `"HH:MM:SS"` | `Time` |
| `parse_datetime(str)` | ISO 8601 | `DateTime` |
| `from_timestamp(ts)` | Unix seconds | `DateTime` |
| `from_timestamp_ms(ts)` | Unix ms | `DateTime` |

### Formatting Functions

| Function | Format Specifiers | Example |
|----------|-------------------|---------|
| `format_date(date, format)` | YYYY, YY, MM, M, DD, D, MMM, MMMM | `"April 13, 2026"` |
| `format_time(time, format)` | HH, H, mm, m, ss, s, SSS, SSSSSS | `"14:30:45.123"` |
| `format_datetime(dt, format)` | Combined | `"2026-04-13 14:30"` |
| `to_iso_string(dt)` | ISO 8601 | `"2026-04-13T14:30:45Z"` |

### Validation Functions

| Function | Description |
|----------|-------------|
| `is_leap_year(year)` | Check if year is leap year |
| `is_valid_year(year)` | Check year (1000-9999) |
| `is_valid_month(month)` | Check month (1-12) |
| `is_valid_day(year, month, day)` | Check day valid |
| `is_valid_date(date)` | Validate date |
| `is_valid_time(time)` | Validate time |
| `is_valid_datetime(dt)` | Validate datetime |
| `days_in_month(year, month)` | Get days in month |
| `days_in_year(year)` | Get days in year (365/366) |

### Date Arithmetic Functions

| Function | Description |
|----------|-------------|
| `add_days(date, days)` | Add/subtract days |
| `add_months(date, months)` | Add/subtract months |
| `add_years(date, years)` | Add/subtract years |
| `days_between(date1, date2)` | Days difference |

### Week Functions

| Function | Description |
|----------|-------------|
| `day_of_week(date)` | Day of week (0-6, 0=Sunday) |
| `day_of_week_name(date, short)` | Day name ("Monday"/"Mon") |
| `day_of_year(date)` | Day of year (1-366) |
| `week_of_year(date)` | ISO week of year (1-53) |
| `is_weekend(date)` | Check if weekend |
| `is_weekday(date)` | Check if weekday |
| `first_day_of_week(date)` | Monday of week |
| `last_day_of_week(date)` | Sunday of week |
| `nth_weekday_of_month(y, m, dow, n)` | Nth weekday occurrence |

### Month Functions

| Function | Description |
|----------|-------------|
| `month_name(month, short)` | Month name |
| `first_day_of_month(year, month)` | First day |
| `last_day_of_month(year, month)` | Last day |

### Time Arithmetic Functions

| Function | Description |
|----------|-------------|
| `add_seconds(time, secs)` | Add/subtract seconds |
| `add_minutes(time, mins)` | Add/subtract minutes |
| `add_hours(time, hours)` | Add/subtract hours |
| `seconds_between(time1, time2)` | Seconds difference |

### Duration Functions

| Function | Description |
|----------|-------------|
| `duration_seconds(dt1, dt2)` | Duration in seconds |
| `duration_minutes(dt1, dt2)` | Duration in minutes |
| `duration_hours(dt1, dt2)` | Duration in hours |
| `duration_days(dt1, dt2)` | Duration in days |
| `humanize_duration(seconds)` | Human-readable string |

### Utility Functions

| Function | Description |
|----------|-------------|
| `sleep_ms(ms)` | Sleep milliseconds |
| `sleep(seconds)` | Sleep seconds |
| `measure_ms(func)` | Measure execution time (ms) |
| `measure_us(func)` | Measure execution time (μs) |
| `age_in_years(birth, ref)` | Calculate age |
| `parse_timezone_offset(str)` | Parse TZ offset |
| `format_timezone_offset(mins)` | Format TZ offset |

## Format Specifiers

### Date Format

| Specifier | Description | Example |
|-----------|-------------|---------|
| `YYYY` | 4-digit year | `2026` |
| `YY` | 2-digit year | `26` |
| `MMMM` | Full month name | `April` |
| `MMM` | Short month name | `Apr` |
| `MM` | 2-digit month | `04` |
| `M` | Month (no padding) | `4` |
| `DD` | 2-digit day | `13` |
| `D` | Day (no padding) | `13` |

### Time Format

| Specifier | Description | Example |
|-----------|-------------|---------|
| `HH` | 2-digit hour (24h) | `14` |
| `H` | Hour (no padding) | `14` |
| `mm` | 2-digit minute | `30` |
| `m` | Minute (no padding) | `30` |
| `ss` | 2-digit second | `45` |
| `s` | Second (no padding) | `45` |
| `SSSSSS` | Microseconds (6 digits) | `123456` |
| `SSS` | Milliseconds (3 digits) | `123` |

## Compilation

### Requirements

- C++17 or later
- Standard library only

### Compile Tests

```bash
g++ -std=c++17 -o datetime_utils_test datetime_utils_test.cpp
./datetime_utils_test
```

### Usage in Your Project

```cpp
// Include the header
#include "datetime_utils.hpp"

// Use the namespace (optional)
using namespace datetime_utils;
```

## License

MIT License - Feel free to use in any project.

## Version History

- **1.0.0** (2026-04-13) - Initial release
  - Complete datetime handling
  - ISO 8601 parsing/formating
  - Leap year support
  - Timer utility
  - 100% test coverage