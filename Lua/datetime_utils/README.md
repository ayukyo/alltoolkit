# datetime_utils

A comprehensive datetime utility library for Lua providing date/time parsing, formatting, manipulation, and calculations with **zero external dependencies**.

## Features

- **Parsing**: ISO 8601 and custom date format parsing
- **Formatting**: Flexible date/time formatting with custom patterns
- **Arithmetic**: Add/subtract days, months, years, hours, minutes, seconds
- **Differences**: Calculate differences between dates
- **Comparisons**: Compare dates (before, after, equal, between)
- **Utilities**: Leap year, day of week/year, weekend detection, and more
- **Zero Dependencies**: Uses only Lua standard library

## Installation

Simply copy `mod.lua` to your project and require it:

```lua
local datetime_utils = dofile("path/to/mod.lua")
```

Or with the standard module system:

```lua
package.path = package.path .. ";path/to/datetime_utils/?.lua"
local datetime_utils = require("datetime_utils.mod")
```

## Quick Start

```lua
local datetime = dofile("mod.lua")

-- Get current date and time
local now = datetime.now()
local today = datetime.today()

-- Create a date
local dt = datetime.create(2024, 3, 15, 14, 30, 0)

-- Format dates
print(datetime.format_iso(dt))      -- "2024-03-15T14:30:00"
print(datetime.format_date(dt))     -- "2024-03-15"
print(datetime.format_time(dt))     -- "14:30:00"
print(datetime.format(dt, "MMMM DD, YYYY"))  -- "March 15, 2024"

-- Parse dates
local parsed = datetime.parse_iso("2024-03-15T14:30:00")
local parsed2 = datetime.parse("15/03/2024", "%d/%m/%Y")

-- Date arithmetic
local tomorrow = datetime.add_days(dt, 1)
local next_month = datetime.add_months(dt, 1)
local next_year = datetime.add_years(dt, 1)

-- Date differences
local days = datetime.diff_days(dt1, dt2)
local hours = datetime.diff_hours(dt1, dt2)
local months = datetime.diff_months(dt1, dt2)

-- Comparisons
if datetime.is_before(dt1, dt2) then
    print("dt1 is before dt2")
end

-- Utilities
if datetime.leap_year(2024) then
    print("2024 is a leap year!")
end

-- Relative time
print(datetime.relative_time(past_date))  -- "2 hours ago"
print(datetime.relative_time(future_date))  -- "in 3 days"
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `now()` | Returns current Unix timestamp |
| `today()` | Returns current date as a table |
| `create(year, month, day, [hour], [min], [sec])` | Creates a datetime table |
| `to_timestamp(dt)` | Converts datetime table to Unix timestamp |
| `from_timestamp(timestamp)` | Converts Unix timestamp to datetime table |

### Parsing Functions

| Function | Description |
|----------|-------------|
| `parse_iso(str)` | Parses ISO 8601 date/datetime string |
| `parse(str, format)` | Parses date string with custom format |

**Supported formats for `parse()`:**
- `%Y-%m-%d` - "2024-03-15"
- `%Y/%m/%d` - "2024/03/15"
- `%d/%m/%Y` - "15/03/2024"
- `%m/%d/%Y` - "03/15/2024"
- `%Y%m%d` - "20240315"
- `%Y-%m-%d %H:%M:%S` - "2024-03-15 14:30:00"
- `%d %b %Y` - "15 Mar 2024"
- `%d %B %Y` - "15 March 2024"

### Formatting Functions

| Function | Description |
|----------|-------------|
| `format_iso(dt)` | Formats as ISO 8601 string |
| `format_date(dt)` | Formats as date string (YYYY-MM-DD) |
| `format_time(dt)` | Formats as time string (HH:MM:SS) |
| `format(dt, pattern)` | Custom format with placeholders |

**Placeholder patterns for `format()`:**
- `YYYY` - Full year (2024)
- `YY` - Short year (24)
- `MM` - Zero-padded month (03)
- `M` - Month (3)
- `DD` - Zero-padded day (15)
- `D` - Day (15)
- `HH` - Zero-padded hour (14)
- `H` - Hour (14)
- `mm` - Zero-padded minute (30)
- `m` - Minute (30)
- `SS` - Zero-padded second (45)
- `S` - Second (45)
- `MMMM` - Full month name (March)
- `MMM` - Short month name (Mar)
- `DDDD` - Full day name (Friday)
- `DDD` - Short day name (Fri)

### Arithmetic Functions

| Function | Description |
|----------|-------------|
| `add_days(dt, days)` | Adds days to date |
| `add_months(dt, months)` | Adds months to date |
| `add_years(dt, years)` | Adds years to date |
| `add_hours(dt, hours)` | Adds hours to datetime |
| `add_minutes(dt, minutes)` | Adds minutes to datetime |
| `add_seconds(dt, seconds)` | Adds seconds to datetime |

### Difference Functions

| Function | Description |
|----------|-------------|
| `diff_days(dt1, dt2)` | Difference in days |
| `diff_hours(dt1, dt2)` | Difference in hours |
| `diff_minutes(dt1, dt2)` | Difference in minutes |
| `diff_seconds(dt1, dt2)` | Difference in seconds |
| `diff_months(dt1, dt2)` | Difference in months |

### Comparison Functions

| Function | Description |
|----------|-------------|
| `is_before(dt1, dt2)` | Checks if dt1 is before dt2 |
| `is_after(dt1, dt2)` | Checks if dt1 is after dt2 |
| `is_equal(dt1, dt2)` | Checks if dt1 equals dt2 |
| `is_between(dt, start, end)` | Checks if dt is between start and end |

### Utility Functions

| Function | Description |
|----------|-------------|
| `leap_year(year)` | Checks if year is a leap year |
| `get_days_in_month(year, month)` | Gets days in a month |
| `day_of_week(dt)` | Gets day of week (1=Sunday, 7=Saturday) |
| `day_of_year(dt)` | Gets day of year (1-366) |
| `week_of_year(dt)` | Gets week of year |
| `is_weekend(dt)` | Checks if date is weekend |
| `is_weekday(dt)` | Checks if date is weekday |
| `quarter(dt)` | Gets quarter of year (1-4) |
| `clone(dt)` | Creates a copy of datetime table |
| `relative_time(dt, [from])` | Returns relative time string |

### Period Functions

| Function | Description |
|----------|-------------|
| `start_of_day(dt)` | Returns start of day (midnight) |
| `end_of_day(dt)` | Returns end of day (23:59:59) |
| `start_of_week(dt)` | Returns start of week (Sunday) |
| `end_of_week(dt)` | Returns end of week (Saturday) |
| `start_of_month(dt)` | Returns start of month |
| `end_of_month(dt)` | Returns end of month |
| `start_of_year(dt)` | Returns start of year |
| `end_of_year(dt)` | Returns end of year |

### Constants

| Constant | Description |
|----------|-------------|
| `MONTH_NAMES` | Array of full month names |
| `MONTH_NAMES_SHORT` | Array of short month names |
| `DAY_NAMES` | Array of full day names |
| `DAY_NAMES_SHORT` | Array of short day names |

## Running Tests

```bash
cd datetime_utils
lua datetime_utils_test.lua
```

## License

MIT License - Feel free to use in your projects.