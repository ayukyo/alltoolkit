--[[
basic_usage.lua - Basic usage examples for datetime_utils
]]

-- Load the module
local datetime_utils = dofile("../mod.lua")

print("========================================")
print("datetime_utils - Basic Usage Examples")
print("========================================")

--------------------------------------------------------------------------------
-- Current Date/Time
--------------------------------------------------------------------------------
print("\n--- Current Date/Time ---")

local now = datetime_utils.now()
print("Current timestamp: " .. now)

local today = datetime_utils.today()
print("Today's date: " .. today.year .. "-" .. today.month .. "-" .. today.day)
print("Current time: " .. today.hour .. ":" .. today.min .. ":" .. today.sec)

--------------------------------------------------------------------------------
-- Creating Dates
--------------------------------------------------------------------------------
print("\n--- Creating Dates ---")

-- Create a specific date
local dt = datetime_utils.create(2024, 3, 15, 14, 30, 45)
print("Created date: " .. dt.year .. "-" .. dt.month .. "-" .. dt.day)
print("Created time: " .. dt.hour .. ":" .. dt.min .. ":" .. dt.sec)

-- Create date only (time defaults to midnight)
local dt2 = datetime_utils.create(2024, 12, 25)
print("Christmas 2024: " .. dt2.year .. "-" .. dt2.month .. "-" .. dt2.day)

--------------------------------------------------------------------------------
-- Formatting Dates
--------------------------------------------------------------------------------
print("\n--- Formatting Dates ---")

-- ISO format
print("ISO format: " .. datetime_utils.format_iso(dt))

-- Date only
print("Date format: " .. datetime_utils.format_date(dt))

-- Time only
print("Time format: " .. datetime_utils.format_time(dt))

-- Custom formats
print("Custom (YYYY-MM-DD): " .. datetime_utils.format(dt, "YYYY-MM-DD"))
print("Custom (DD/MM/YYYY): " .. datetime_utils.format(dt, "DD/MM/YYYY"))
print("Custom (MMMM DD, YYYY): " .. datetime_utils.format(dt, "MMMM DD, YYYY"))
print("Custom (DDD, MMM D, YYYY): " .. datetime_utils.format(dt, "DDD, MMM D, YYYY"))

--------------------------------------------------------------------------------
-- Parsing Dates
--------------------------------------------------------------------------------
print("\n--- Parsing Dates ---")

-- Parse ISO 8601
local parsed1 = datetime_utils.parse_iso("2024-06-20")
print("Parsed ISO date: " .. parsed1.year .. "-" .. parsed1.month .. "-" .. parsed1.day)

-- Parse ISO datetime
local parsed2 = datetime_utils.parse_iso("2024-06-20T15:30:00")
print("Parsed ISO datetime: " .. parsed2.hour .. ":" .. parsed2.min .. ":" .. parsed2.sec)

-- Parse custom formats
local parsed3 = datetime_utils.parse("15/03/2024", "%d/%m/%Y")
print("Parsed DD/MM/YYYY: " .. parsed3.year .. "-" .. parsed3.month .. "-" .. parsed3.day)

local parsed4 = datetime_utils.parse("03/15/2024", "%m/%d/%Y")
print("Parsed MM/DD/YYYY: " .. parsed4.year .. "-" .. parsed4.month .. "-" .. parsed4.day)

--------------------------------------------------------------------------------
-- Date Arithmetic
--------------------------------------------------------------------------------
print("\n--- Date Arithmetic ---")

local base_date = datetime_utils.create(2024, 3, 15)
print("Base date: " .. datetime_utils.format_date(base_date))

-- Add days
local future_date = datetime_utils.add_days(base_date, 10)
print("After 10 days: " .. datetime_utils.format_date(future_date))

-- Add months
local next_month = datetime_utils.add_months(base_date, 2)
print("After 2 months: " .. datetime_utils.format_date(next_month))

-- Add years
local next_year = datetime_utils.add_years(base_date, 1)
print("After 1 year: " .. datetime_utils.format_date(next_year))

-- Subtract days
local past_date = datetime_utils.add_days(base_date, -5)
print("5 days before: " .. datetime_utils.format_date(past_date))

--------------------------------------------------------------------------------
-- Date Differences
--------------------------------------------------------------------------------
print("\n--- Date Differences ---")

local date1 = datetime_utils.create(2024, 3, 15)
local date2 = datetime_utils.create(2024, 3, 25)

print("Difference between Mar 15 and Mar 25:")
print("  Days: " .. datetime_utils.diff_days(date1, date2))

local time1 = datetime_utils.create(2024, 3, 15, 10, 0, 0)
local time2 = datetime_utils.create(2024, 3, 15, 14, 30, 0)

print("Difference between 10:00 and 14:30:")
print("  Hours: " .. datetime_utils.diff_hours(time1, time2))
print("  Minutes: " .. datetime_utils.diff_minutes(time1, time2))
print("  Seconds: " .. datetime_utils.diff_seconds(time1, time2))

--------------------------------------------------------------------------------
-- Date Comparisons
--------------------------------------------------------------------------------
print("\n--- Date Comparisons ---")

local dt_a = datetime_utils.create(2024, 3, 15)
local dt_b = datetime_utils.create(2024, 3, 20)
local dt_c = datetime_utils.create(2024, 3, 15)

print("Comparing Mar 15 and Mar 20:")
print("  Is Mar 15 before Mar 20? " .. tostring(datetime_utils.is_before(dt_a, dt_b)))
print("  Is Mar 15 after Mar 20? " .. tostring(datetime_utils.is_after(dt_a, dt_b)))
print("  Is Mar 15 equal to Mar 20? " .. tostring(datetime_utils.is_equal(dt_a, dt_b)))
print("  Is Mar 15 equal to Mar 15? " .. tostring(datetime_utils.is_equal(dt_a, dt_c)))

--------------------------------------------------------------------------------
-- Leap Year and Days in Month
--------------------------------------------------------------------------------
print("\n--- Leap Year and Days in Month ---")

print("Is 2024 a leap year? " .. tostring(datetime_utils.leap_year(2024)))
print("Is 2023 a leap year? " .. tostring(datetime_utils.leap_year(2023)))
print("Is 2000 a leap year? " .. tostring(datetime_utils.leap_year(2000)))
print("Is 1900 a leap year? " .. tostring(datetime_utils.leap_year(1900)))

print("\nDays in each month (2024):")
for month = 1, 12 do
    print("  " .. datetime_utils.MONTH_NAMES[month] .. ": " .. 
          datetime_utils.get_days_in_month(2024, month) .. " days")
end

--------------------------------------------------------------------------------
-- Day of Week and Year
--------------------------------------------------------------------------------
print("\n--- Day of Week and Year ---")

local dt_test = datetime_utils.create(2024, 3, 15)
print("Date: " .. datetime_utils.format_date(dt_test))
print("  Day of week: " .. datetime_utils.DAY_NAMES[datetime_utils.day_of_week(dt_test)])
print("  Day of year: " .. datetime_utils.day_of_year(dt_test))
print("  Week of year: " .. datetime_utils.week_of_year(dt_test))
print("  Quarter: Q" .. datetime_utils.quarter(dt_test))
print("  Is weekend? " .. tostring(datetime_utils.is_weekend(dt_test)))

--------------------------------------------------------------------------------
-- Start/End of Periods
--------------------------------------------------------------------------------
print("\n--- Start/End of Periods ---")

local dt_period = datetime_utils.create(2024, 3, 15, 14, 30, 45)

print("For " .. datetime_utils.format_iso(dt_period) .. ":")
print("  Start of day: " .. datetime_utils.format_iso(datetime_utils.start_of_day(dt_period)))
print("  End of day: " .. datetime_utils.format_iso(datetime_utils.end_of_day(dt_period)))
print("  Start of month: " .. datetime_utils.format_date(datetime_utils.start_of_month(dt_period)))
print("  End of month: " .. datetime_utils.format_date(datetime_utils.end_of_month(dt_period)))
print("  Start of year: " .. datetime_utils.format_date(datetime_utils.start_of_year(dt_period)))
print("  End of year: " .. datetime_utils.format_date(datetime_utils.end_of_year(dt_period)))

--------------------------------------------------------------------------------
-- Relative Time
--------------------------------------------------------------------------------
print("\n--- Relative Time ---")

local current = datetime_utils.now()

-- Various time offsets
print("From now:")
print("  -30 seconds: " .. datetime_utils.relative_time(datetime_utils.add_seconds(current, -30), current))
print("  -5 minutes: " .. datetime_utils.relative_time(datetime_utils.add_minutes(current, -5), current))
print("  -2 hours: " .. datetime_utils.relative_time(datetime_utils.add_hours(current, -2), current))
print("  -3 days: " .. datetime_utils.relative_time(datetime_utils.add_days(current, -3), current))
print("  +1 hour: " .. datetime_utils.relative_time(datetime_utils.add_hours(current, 1), current))
print("  +7 days: " .. datetime_utils.relative_time(datetime_utils.add_days(current, 7), current))

--------------------------------------------------------------------------------
-- Chinese Date Format
--------------------------------------------------------------------------------
print("\n--- Chinese Date Format ---")

local chinese_date = datetime_utils.create(2024, 3, 15)
print("Chinese format: " .. datetime_utils.format(chinese_date, "YYYY年MM月DD日"))

--------------------------------------------------------------------------------
-- Practical Example: Age Calculation
--------------------------------------------------------------------------------
print("\n--- Practical Example: Age Calculation ---")

function calculate_age(birth_year, birth_month, birth_day)
    local birth_date = datetime_utils.create(birth_year, birth_month, birth_day)
    local today = datetime_utils.today()
    local age = datetime_utils.diff_years(birth_date, today)
    
    -- diff_years not available, use diff_days approximation
    local days = datetime_utils.diff_days(birth_date, today)
    return math.floor(days / 365.25)
end

-- Example birthday
local birth = datetime_utils.create(1990, 6, 15)
local today = datetime_utils.today()
local days_alive = datetime_utils.diff_days(birth, today)
local years = math.floor(days_alive / 365.25)

print("Born: " .. datetime_utils.format_date(birth))
print("Days alive: " .. days_alive)
print("Approximate age: " .. years .. " years")

print("\n========================================")
print("Examples completed!")
print("========================================")