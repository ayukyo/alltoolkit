--[[
datetime_utils_test.lua - Comprehensive test suite for datetime_utils
100% coverage of all functions and edge cases
]]

-- Load the module
local datetime_utils = dofile("mod.lua")

-- Test helper
local tests_passed = 0
local tests_failed = 0
local function assert_equal(actual, expected, tolerance, message)
    -- Support optional tolerance parameter for floating-point comparisons
    if type(tolerance) == "number" then
        if math.abs(actual - expected) <= tolerance then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print("FAILED: " .. (message or "assertion failed"))
            print("  Expected: " .. tostring(expected) .. " (±" .. tolerance .. ")")
            print("  Actual: " .. tostring(actual))
        end
    elseif type(tolerance) == "string" then
        -- tolerance is actually the message
        if actual == expected then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print("FAILED: " .. tolerance)
            print("  Expected: " .. tostring(expected))
            print("  Actual: " .. tostring(actual))
        end
    else
        if actual == expected then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print("FAILED: " .. (message or "assertion failed"))
            print("  Expected: " .. tostring(expected))
            print("  Actual: " .. tostring(actual))
        end
    end
end

local function assert_not_nil(value, message)
    if value ~= nil then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        print("FAILED: " .. (message or "expected non-nil value"))
    end
end

local function assert_nil(value, message)
    if value == nil then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        print("FAILED: " .. (message or "expected nil value"))
        print("  Actual: " .. tostring(value))
    end
end

local function assert_true(value, message)
    if value == true then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        print("FAILED: " .. (message or "expected true"))
        print("  Actual: " .. tostring(value))
    end
end

local function assert_false(value, message)
    if value == false then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        print("FAILED: " .. (message or "expected false"))
        print("  Actual: " .. tostring(value))
    end
end

print("========================================")
print("datetime_utils Test Suite")
print("========================================")

--------------------------------------------------------------------------------
-- Constants Tests
--------------------------------------------------------------------------------
print("\n--- Constants Tests ---")

do
    assert_not_nil(datetime_utils.MONTH_NAMES, "MONTH_NAMES should exist")
    assert_equal(#datetime_utils.MONTH_NAMES, 12, "MONTH_NAMES should have 12 entries")
    assert_equal(datetime_utils.MONTH_NAMES[1], "January", "First month should be January")
    
    assert_not_nil(datetime_utils.MONTH_NAMES_SHORT, "MONTH_NAMES_SHORT should exist")
    assert_equal(#datetime_utils.MONTH_NAMES_SHORT, 12, "MONTH_NAMES_SHORT should have 12 entries")
    assert_equal(datetime_utils.MONTH_NAMES_SHORT[1], "Jan", "First short month should be Jan")
    
    assert_not_nil(datetime_utils.DAY_NAMES, "DAY_NAMES should exist")
    assert_equal(#datetime_utils.DAY_NAMES, 7, "DAY_NAMES should have 7 entries")
    assert_equal(datetime_utils.DAY_NAMES[1], "Sunday", "First day should be Sunday")
    
    assert_not_nil(datetime_utils.DAY_NAMES_SHORT, "DAY_NAMES_SHORT should exist")
    assert_equal(#datetime_utils.DAY_NAMES_SHORT, 7, "DAY_NAMES_SHORT should have 7 entries")
    assert_equal(datetime_utils.DAY_NAMES_SHORT[1], "Sun", "First short day should be Sun")
end

--------------------------------------------------------------------------------
-- Leap Year Tests
--------------------------------------------------------------------------------
print("\n--- Leap Year Tests ---")

do
    -- Test leap years
    assert_true(datetime_utils.leap_year(2024), "2024 is a leap year")
    assert_true(datetime_utils.leap_year(2000), "2000 is a leap year (century divisible by 400)")
    assert_true(datetime_utils.leap_year(2400), "2400 is a leap year")
    assert_true(datetime_utils.leap_year(1996), "1996 is a leap year")
    
    -- Test non-leap years
    assert_false(datetime_utils.leap_year(2023), "2023 is not a leap year")
    assert_false(datetime_utils.leap_year(1900), "1900 is not a leap year (century not divisible by 400)")
    assert_false(datetime_utils.leap_year(2100), "2100 is not a leap year")
    assert_false(datetime_utils.leap_year(2001), "2001 is not a leap year")
end

--------------------------------------------------------------------------------
-- Days in Month Tests
--------------------------------------------------------------------------------
print("\n--- Days in Month Tests ---")

do
    assert_equal(datetime_utils.get_days_in_month(2024, 1), 31, "January has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 2), 29, "February 2024 has 29 days (leap year)")
    assert_equal(datetime_utils.get_days_in_month(2023, 2), 28, "February 2023 has 28 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 3), 31, "March has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 4), 30, "April has 30 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 5), 31, "May has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 6), 30, "June has 30 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 7), 31, "July has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 8), 31, "August has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 9), 30, "September has 30 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 10), 31, "October has 31 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 11), 30, "November has 30 days")
    assert_equal(datetime_utils.get_days_in_month(2024, 12), 31, "December has 31 days")
end

--------------------------------------------------------------------------------
-- Create Tests
--------------------------------------------------------------------------------
print("\n--- Create Tests ---")

do
    -- Test valid date creation
    local dt = datetime_utils.create(2024, 3, 15)
    assert_not_nil(dt, "Should create valid date")
    assert_equal(dt.year, 2024, "Year should be 2024")
    assert_equal(dt.month, 3, "Month should be 3")
    assert_equal(dt.day, 15, "Day should be 15")
    assert_equal(dt.hour, 0, "Hour should default to 0")
    assert_equal(dt.min, 0, "Minute should default to 0")
    assert_equal(dt.sec, 0, "Second should default to 0")
    
    -- Test with time
    local dt2 = datetime_utils.create(2024, 6, 20, 14, 30, 45)
    assert_equal(dt2.hour, 14, "Hour should be 14")
    assert_equal(dt2.min, 30, "Minute should be 30")
    assert_equal(dt2.sec, 45, "Second should be 45")
    
    -- Test invalid dates
    local invalid, err = datetime_utils.create(2024, 13, 1)
    assert_nil(invalid, "Invalid month should return nil")
    assert_not_nil(err, "Should return error message for invalid month")
    
    invalid, err = datetime_utils.create(2024, 0, 1)
    assert_nil(invalid, "Month 0 should return nil")
    
    invalid, err = datetime_utils.create(2024, 2, 30)
    assert_nil(invalid, "Feb 30 should return nil")
    
    invalid, err = datetime_utils.create(2023, 2, 29)
    assert_nil(invalid, "Feb 29 in non-leap year should return nil")
    
    -- Valid Feb 29 in leap year
    local dt3 = datetime_utils.create(2024, 2, 29)
    assert_not_nil(dt3, "Feb 29 in leap year should be valid")
    
    -- Test invalid hour/minute/second
    invalid, err = datetime_utils.create(2024, 1, 1, 24, 0, 0)
    assert_nil(invalid, "Hour 24 should return nil")
    
    invalid, err = datetime_utils.create(2024, 1, 1, 0, 60, 0)
    assert_nil(invalid, "Minute 60 should return nil")
    
    invalid, err = datetime_utils.create(2024, 1, 1, 0, 0, 60)
    assert_nil(invalid, "Second 60 should return nil")
end

--------------------------------------------------------------------------------
-- Now and Today Tests
--------------------------------------------------------------------------------
print("\n--- Now and Today Tests ---")

do
    local now = datetime_utils.now()
    assert_not_nil(now, "now() should return a value")
    assert_equal(type(now), "number", "now() should return a number")
    
    local today = datetime_utils.today()
    assert_not_nil(today, "today() should return a value")
    assert_equal(type(today), "table", "today() should return a table")
    assert_not_nil(today.year, "today should have year")
    assert_not_nil(today.month, "today should have month")
    assert_not_nil(today.day, "today should have day")
end

--------------------------------------------------------------------------------
-- Timestamp Conversion Tests
--------------------------------------------------------------------------------
print("\n--- Timestamp Conversion Tests ---")

do
    -- Test timestamp to table
    local timestamp = 1704067200  -- 2024-01-01 00:00:00 UTC
    local dt = datetime_utils.from_timestamp(timestamp)
    assert_not_nil(dt, "from_timestamp should return a table")
    assert_equal(dt.year, 2024, "Year should be 2024")
    
    -- Test invalid timestamp
    local invalid = datetime_utils.from_timestamp("not a number")
    assert_nil(invalid, "from_timestamp should return nil for non-number")
    
    -- Test table to timestamp
    local dt2 = datetime_utils.create(2024, 1, 1, 0, 0, 0)
    local ts = datetime_utils.to_timestamp(dt2)
    assert_not_nil(ts, "to_timestamp should return a number")
    assert_equal(type(ts), "number", "to_timestamp should return a number")
    
    -- Test timestamp passed to to_timestamp (identity)
    local identity = datetime_utils.to_timestamp(12345)
    assert_equal(identity, 12345, "to_timestamp should pass through numbers")
end

--------------------------------------------------------------------------------
-- Parse ISO Tests
--------------------------------------------------------------------------------
print("\n--- Parse ISO Tests ---")

do
    -- Test valid ISO date format
    local dt, err = datetime_utils.parse_iso("2024-03-15")
    assert_not_nil(dt, "Should parse ISO date")
    assert_equal(dt.year, 2024, "Year should be 2024")
    assert_equal(dt.month, 3, "Month should be 3")
    assert_equal(dt.day, 15, "Day should be 15")
    
    -- Test ISO datetime format with T
    local dt2 = datetime_utils.parse_iso("2024-06-20T14:30:45")
    assert_not_nil(dt2, "Should parse ISO datetime with T")
    assert_equal(dt2.year, 2024, "Year should be 2024")
    assert_equal(dt2.month, 6, "Month should be 6")
    assert_equal(dt2.day, 20, "Day should be 20")
    assert_equal(dt2.hour, 14, "Hour should be 14")
    assert_equal(dt2.min, 30, "Minute should be 30")
    assert_equal(dt2.sec, 45, "Second should be 45")
    
    -- Test ISO datetime format with space
    local dt3 = datetime_utils.parse_iso("2024-12-25 23:59:59")
    assert_not_nil(dt3, "Should parse ISO datetime with space")
    assert_equal(dt3.hour, 23, "Hour should be 23")
    assert_equal(dt3.min, 59, "Minute should be 59")
    assert_equal(dt3.sec, 59, "Second should be 59")
    
    -- Test invalid formats
    local invalid = datetime_utils.parse_iso("not a date")
    assert_nil(invalid, "Should return nil for invalid format")
    
    invalid = datetime_utils.parse_iso(12345)
    assert_nil(invalid, "Should return nil for non-string")
    
    invalid = datetime_utils.parse_iso("2024/03/15")  -- Wrong separator
    assert_nil(invalid, "Should return nil for wrong separator")
end

--------------------------------------------------------------------------------
-- Parse Custom Format Tests
--------------------------------------------------------------------------------
print("\n--- Parse Custom Format Tests ---")

do
    -- Test various formats
    local dt1 = datetime_utils.parse("2024-03-15", "%Y-%m-%d")
    assert_not_nil(dt1, "Should parse %Y-%m-%d")
    assert_equal(dt1.year, 2024, "Year should be 2024")
    
    local dt2 = datetime_utils.parse("2024/03/15", "%Y/%m/%d")
    assert_not_nil(dt2, "Should parse %Y/%m/%d")
    
    local dt3 = datetime_utils.parse("15/03/2024", "%d/%m/%Y")
    assert_not_nil(dt3, "Should parse %d/%m/%Y")
    assert_equal(dt3.day, 15, "Day should be 15")
    assert_equal(dt3.month, 3, "Month should be 3")
    assert_equal(dt3.year, 2024, "Year should be 2024")
    
    local dt4 = datetime_utils.parse("03/15/2024", "%m/%d/%Y")
    assert_not_nil(dt4, "Should parse %m/%d/%Y")
    assert_equal(dt4.month, 3, "Month should be 3")
    assert_equal(dt4.day, 15, "Day should be 15")
    
    local dt5 = datetime_utils.parse("20240315", "%Y%m%d")
    assert_not_nil(dt5, "Should parse %Y%m%d")
    
    local dt6 = datetime_utils.parse("2024-03-15 14:30:45", "%Y-%m-%d %H:%M:%S")
    assert_not_nil(dt6, "Should parse %Y-%m-%d %H:%M:%S")
    assert_equal(dt6.hour, 14, "Hour should be 14")
    assert_equal(dt6.min, 30, "Minute should be 30")
    assert_equal(dt6.sec, 45, "Second should be 45")
    
    -- Test month name formats
    local dt7 = datetime_utils.parse("15 Mar 2024", "%d %b %Y")
    assert_not_nil(dt7, "Should parse %d %b %Y")
    assert_equal(dt7.month, 3, "Month should be 3 for Mar")
    
    local dt8 = datetime_utils.parse("15 March 2024", "%d %B %Y")
    assert_not_nil(dt8, "Should parse %d %B %Y")
    assert_equal(dt8.month, 3, "Month should be 3 for March")
    
    -- Test invalid input
    local invalid = datetime_utils.parse(12345)
    assert_nil(invalid, "Should return nil for non-string")
    
    invalid = datetime_utils.parse("invalid date", "%Y-%m-%d")
    assert_nil(invalid, "Should return nil for unparsable string")
end

--------------------------------------------------------------------------------
-- Format ISO Tests
--------------------------------------------------------------------------------
print("\n--- Format ISO Tests ---")

do
    -- Test ISO format
    local dt = datetime_utils.create(2024, 3, 15, 14, 30, 45)
    local iso = datetime_utils.format_iso(dt)
    assert_equal(iso, "2024-03-15T14:30:45", "Should format to ISO string")
    
    -- Test with timestamp
    local iso2 = datetime_utils.format_iso(1704067200)
    assert_not_nil(iso2, "Should format timestamp")
    
    -- Test with invalid input
    local invalid = datetime_utils.format_iso("not a date")
    assert_nil(invalid, "Should return nil for invalid input")
    
    -- Test date only format
    local date_str = datetime_utils.format_date(dt)
    assert_equal(date_str, "2024-03-15", "Should format date only")
    
    -- Test time only format
    local time_str = datetime_utils.format_time(dt)
    assert_equal(time_str, "14:30:45", "Should format time only")
end

--------------------------------------------------------------------------------
-- Custom Format Tests
--------------------------------------------------------------------------------
print("\n--- Custom Format Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15, 14, 30, 45)
    
    -- Test various format patterns
    local str1 = datetime_utils.format(dt, "YYYY-MM-DD")
    assert_equal(str1, "2024-03-15", "Should format YYYY-MM-DD")
    
    local str2 = datetime_utils.format(dt, "DD/MM/YYYY")
    assert_equal(str2, "15/03/2024", "Should format DD/MM/YYYY")
    
    local str3 = datetime_utils.format(dt, "HH:mm:SS")
    assert_equal(str3, "14:30:45", "Should format HH:mm:SS")
    
    local str4 = datetime_utils.format(dt, "YYYY年MM月DD日")
    assert_equal(str4, "2024年03月15日", "Should format with Chinese characters")
    
    -- Test month names
    local str5 = datetime_utils.format(dt, "MMMM DD, YYYY")
    assert_equal(str5, "March 15, 2024", "Should format with full month name")
    
    local str6 = datetime_utils.format(dt, "MMM DD, YYYY")
    assert_equal(str6, "Mar 15, 2024", "Should format with short month name")
    
    -- Test short year
    local str7 = datetime_utils.format(dt, "YY-MM-DD")
    assert_equal(str7, "24-03-15", "Should format with short year")
    
    -- Test single digit formats
    local dt2 = datetime_utils.create(2024, 1, 5, 9, 5, 3)
    local str8 = datetime_utils.format(dt2, "YYYY-M-D H:m:S")
    assert_equal(str8, "2024-1-5 9:5:3", "Should format with single digits")
    
    -- Test with timestamp
    local str9 = datetime_utils.format(1704067200, "YYYY-MM-DD")
    assert_not_nil(str9, "Should format timestamp")
    
    -- Test with invalid input
    local invalid = datetime_utils.format("not a date", "YYYY")
    assert_nil(invalid, "Should return nil for invalid input")
end

--------------------------------------------------------------------------------
-- Add Days Tests
--------------------------------------------------------------------------------
print("\n--- Add Days Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15, 12, 0, 0)
    
    -- Test adding days
    local dt2 = datetime_utils.add_days(dt, 5)
    assert_equal(dt2.day, 20, "Should add 5 days")
    assert_equal(dt2.month, 3, "Month should remain 3")
    
    -- Test subtracting days
    local dt3 = datetime_utils.add_days(dt, -5)
    assert_equal(dt3.day, 10, "Should subtract 5 days")
    
    -- Test month rollover
    local dt4 = datetime_utils.add_days(dt, 20)
    assert_equal(dt4.month, 4, "Should roll over to April")
    assert_equal(dt4.day, 4, "Day should be 4")
    
    -- Test year rollover
    local dt5 = datetime_utils.create(2024, 12, 30)
    local dt6 = datetime_utils.add_days(dt5, 5)
    assert_equal(dt6.year, 2025, "Should roll over to 2025")
    assert_equal(dt6.month, 1, "Should be January")
    assert_equal(dt6.day, 4, "Day should be 4")
    
    -- Test with timestamp
    local ts = datetime_utils.to_timestamp(dt)
    local ts2 = datetime_utils.add_days(ts, 1)
    assert_equal(type(ts2), "number", "Should return timestamp for timestamp input")
end

--------------------------------------------------------------------------------
-- Add Months Tests
--------------------------------------------------------------------------------
print("\n--- Add Months Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15)
    
    -- Test adding months
    local dt2 = datetime_utils.add_months(dt, 2)
    assert_equal(dt2.month, 5, "Should add 2 months")
    
    -- Test year rollover
    local dt3 = datetime_utils.add_months(dt, 10)
    assert_equal(dt3.year, 2025, "Should roll over year")
    assert_equal(dt3.month, 1, "Should be January")
    
    -- Test day adjustment for shorter month
    local dt4 = datetime_utils.create(2024, 1, 31)
    local dt5 = datetime_utils.add_months(dt4, 1)
    assert_equal(dt5.month, 2, "Should be February")
    assert_equal(dt5.day, 29, "Feb 31 should become Feb 29 (leap year)")
    
    -- Test non-leap year
    local dt6 = datetime_utils.create(2023, 1, 31)
    local dt7 = datetime_utils.add_months(dt6, 1)
    assert_equal(dt7.day, 28, "Feb 31 should become Feb 28 (non-leap year)")
    
    -- Test with timestamp
    local ts = datetime_utils.to_timestamp(dt)
    local dt8 = datetime_utils.add_months(ts, 1)
    assert_not_nil(dt8, "Should work with timestamp")
end

--------------------------------------------------------------------------------
-- Add Years Tests
--------------------------------------------------------------------------------
print("\n--- Add Years Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15)
    
    -- Test adding years
    local dt2 = datetime_utils.add_years(dt, 5)
    assert_equal(dt2.year, 2029, "Should add 5 years")
    
    -- Test subtracting years
    local dt3 = datetime_utils.add_years(dt, -4)
    assert_equal(dt3.year, 2020, "Should subtract 4 years")
    
    -- Test leap year adjustment
    local dt4 = datetime_utils.create(2024, 2, 29)
    local dt5 = datetime_utils.add_years(dt4, 1)
    assert_equal(dt5.year, 2025, "Should be 2025")
    assert_equal(dt5.day, 28, "Feb 29 should become Feb 28 in non-leap year")
    
    -- Test leap year to leap year
    local dt6 = datetime_utils.add_years(dt4, 4)
    assert_equal(dt6.year, 2028, "Should be 2028")
    assert_equal(dt6.day, 29, "Should still be Feb 29 in leap year")
end

--------------------------------------------------------------------------------
-- Add Hours/Minutes/Seconds Tests
--------------------------------------------------------------------------------
print("\n--- Add Hours/Minutes/Seconds Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15, 12, 30, 45)
    
    -- Test add hours
    local dt2 = datetime_utils.add_hours(dt, 5)
    assert_equal(dt2.hour, 17, "Should add 5 hours")
    
    -- Test add hours rollover
    local dt3 = datetime_utils.add_hours(dt, 12)
    assert_equal(dt3.hour, 0, "Should roll over to midnight")
    assert_equal(dt3.day, 16, "Should be next day")
    
    -- Test add minutes
    local dt4 = datetime_utils.add_minutes(dt, 45)
    assert_equal(dt4.min, 15, "Should add 45 minutes")
    
    -- Test add seconds
    local dt5 = datetime_utils.add_seconds(dt, 30)
    assert_equal(dt5.sec, 15, "Should add 30 seconds")
    
    -- Test with timestamps
    local ts = datetime_utils.to_timestamp(dt)
    local ts2 = datetime_utils.add_hours(ts, 1)
    assert_equal(type(ts2), "number", "Should return timestamp")
end

--------------------------------------------------------------------------------
-- Difference Tests
--------------------------------------------------------------------------------
print("\n--- Difference Tests ---")

do
    local dt1 = datetime_utils.create(2024, 3, 15, 12, 0, 0)
    local dt2 = datetime_utils.create(2024, 3, 20, 12, 0, 0)
    
    -- Test diff_days
    local days = datetime_utils.diff_days(dt1, dt2)
    assert_equal(days, 5, "Should be 5 days difference")
    
    -- Test negative diff
    local days2 = datetime_utils.diff_days(dt2, dt1)
    assert_equal(days2, -5, "Should be -5 days difference")
    
    -- Test diff_seconds
    local dt3 = datetime_utils.create(2024, 3, 15, 12, 0, 0)
    local dt4 = datetime_utils.create(2024, 3, 15, 14, 30, 30)
    local seconds = datetime_utils.diff_seconds(dt3, dt4)
    assert_equal(seconds, 9030, "Should be 9030 seconds difference")
    
    -- Test diff_hours
    local hours = datetime_utils.diff_hours(dt3, dt4)
    assert_equal(hours, 2.5083333333333, 0.0001, "Should be ~2.5 hours difference")
    
    -- Test diff_minutes
    local minutes = datetime_utils.diff_minutes(dt3, dt4)
    assert_equal(minutes, 150.5, 0.01, "Should be 150.5 minutes difference")
    
    -- Test diff_months
    local dt5 = datetime_utils.create(2024, 3, 15)
    local dt6 = datetime_utils.create(2024, 6, 20)
    local months = datetime_utils.diff_months(dt5, dt6)
    assert_equal(months, 3, "Should be 3 months difference")
    
    -- Test diff_months with year change
    local dt7 = datetime_utils.create(2024, 11, 15)
    local dt8 = datetime_utils.create(2025, 2, 20)
    local months2 = datetime_utils.diff_months(dt7, dt8)
    assert_equal(months2, 3, "Should be 3 months difference across year")
    
    -- Test with timestamps
    local ts1 = datetime_utils.to_timestamp(dt1)
    local ts2 = datetime_utils.to_timestamp(dt2)
    local days3 = datetime_utils.diff_days(ts1, ts2)
    assert_equal(days3, 5, "Should work with timestamps")
end

--------------------------------------------------------------------------------
-- Comparison Tests
--------------------------------------------------------------------------------
print("\n--- Comparison Tests ---")

do
    local dt1 = datetime_utils.create(2024, 3, 15, 12, 0, 0)
    local dt2 = datetime_utils.create(2024, 3, 16, 12, 0, 0)
    local dt3 = datetime_utils.create(2024, 3, 15, 12, 0, 0)
    
    -- Test is_before
    assert_true(datetime_utils.is_before(dt1, dt2), "dt1 should be before dt2")
    assert_false(datetime_utils.is_before(dt2, dt1), "dt2 should not be before dt1")
    assert_false(datetime_utils.is_before(dt1, dt3), "Equal dates should not be before")
    
    -- Test is_after
    assert_true(datetime_utils.is_after(dt2, dt1), "dt2 should be after dt1")
    assert_false(datetime_utils.is_after(dt1, dt2), "dt1 should not be after dt2")
    assert_false(datetime_utils.is_after(dt1, dt3), "Equal dates should not be after")
    
    -- Test is_equal
    assert_true(datetime_utils.is_equal(dt1, dt3), "dt1 should equal dt3")
    assert_false(datetime_utils.is_equal(dt1, dt2), "dt1 should not equal dt2")
    
    -- Test is_between
    local dt4 = datetime_utils.create(2024, 3, 15, 18, 0, 0)
    assert_true(datetime_utils.is_between(dt4, dt1, dt2), "dt4 should be between dt1 and dt2")
    assert_false(datetime_utils.is_between(dt1, dt4, dt2), "dt1 should not be between dt4 and dt2")
    
    -- Test with timestamps
    local ts1 = datetime_utils.to_timestamp(dt1)
    local ts2 = datetime_utils.to_timestamp(dt2)
    assert_true(datetime_utils.is_before(ts1, ts2), "Should work with timestamps")
end

--------------------------------------------------------------------------------
-- Day of Week/Year Tests
--------------------------------------------------------------------------------
print("\n--- Day of Week/Year Tests ---")

do
    -- 2024-03-15 is a Friday (wday = 6 in Lua, where Sunday = 1)
    local dt = datetime_utils.create(2024, 3, 15)
    
    -- Test day_of_week
    local wday = datetime_utils.day_of_week(dt)
    assert_equal(wday, 6, "2024-03-15 should be Friday (wday = 6)")
    
    -- Test with timestamp
    local ts = datetime_utils.to_timestamp(dt)
    local wday2 = datetime_utils.day_of_week(ts)
    assert_equal(wday2, 6, "Should work with timestamp")
    
    -- Test day_of_year
    local doy = datetime_utils.day_of_year(dt)
    assert_equal(doy, 75, "March 15 should be day 75 (31+29+15) in leap year")
    
    -- Test day_of_year for Jan 1
    local dt2 = datetime_utils.create(2024, 1, 1)
    assert_equal(datetime_utils.day_of_year(dt2), 1, "Jan 1 should be day 1")
    
    -- Test day_of_year for Dec 31
    local dt3 = datetime_utils.create(2024, 12, 31)
    assert_equal(datetime_utils.day_of_year(dt3), 366, "Dec 31 should be day 366 in leap year")
    
    -- Test day_of_year for Dec 31 non-leap year
    local dt4 = datetime_utils.create(2023, 12, 31)
    assert_equal(datetime_utils.day_of_year(dt4), 365, "Dec 31 should be day 365 in non-leap year")
    
    -- Test week_of_year
    local week = datetime_utils.week_of_year(dt)
    assert_not_nil(week, "week_of_year should return a value")
end

--------------------------------------------------------------------------------
-- Weekend/Weekday Tests
--------------------------------------------------------------------------------
print("\n--- Weekend/Weekday Tests ---")

do
    -- Saturday (2024-03-16)
    local saturday = datetime_utils.create(2024, 3, 16)
    assert_true(datetime_utils.is_weekend(saturday), "Saturday should be weekend")
    assert_false(datetime_utils.is_weekday(saturday), "Saturday should not be weekday")
    
    -- Sunday (2024-03-17)
    local sunday = datetime_utils.create(2024, 3, 17)
    assert_true(datetime_utils.is_weekend(sunday), "Sunday should be weekend")
    assert_false(datetime_utils.is_weekday(sunday), "Sunday should not be weekday")
    
    -- Monday (2024-03-18)
    local monday = datetime_utils.create(2024, 3, 18)
    assert_false(datetime_utils.is_weekend(monday), "Monday should not be weekend")
    assert_true(datetime_utils.is_weekday(monday), "Monday should be weekday")
end

--------------------------------------------------------------------------------
-- Start/End of Period Tests
--------------------------------------------------------------------------------
print("\n--- Start/End of Period Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15, 14, 30, 45)
    
    -- Test start_of_day
    local sod = datetime_utils.start_of_day(dt)
    assert_equal(sod.hour, 0, "Start of day hour should be 0")
    assert_equal(sod.min, 0, "Start of day min should be 0")
    assert_equal(sod.sec, 0, "Start of day sec should be 0")
    
    -- Test end_of_day
    local eod = datetime_utils.end_of_day(dt)
    assert_equal(eod.hour, 23, "End of day hour should be 23")
    assert_equal(eod.min, 59, "End of day min should be 59")
    assert_equal(eod.sec, 59, "End of day sec should be 59")
    
    -- Test start_of_week (should be Sunday)
    local sow = datetime_utils.start_of_week(dt)
    assert_equal(sow.wday, 1, "Start of week should be Sunday")
    
    -- Test end_of_week (should be Saturday)
    local eow = datetime_utils.end_of_week(dt)
    assert_equal(eow.wday, 7, "End of week should be Saturday")
    
    -- Test start_of_month
    local som = datetime_utils.start_of_month(dt)
    assert_equal(som.month, 3, "Start of month should still be March")
    assert_equal(som.day, 1, "Start of month day should be 1")
    assert_equal(som.hour, 0, "Start of month hour should be 0")
    
    -- Test end_of_month
    local eom = datetime_utils.end_of_month(dt)
    assert_equal(eom.month, 3, "End of month should still be March")
    assert_equal(eom.day, 31, "End of month day should be 31")
    assert_equal(eom.hour, 23, "End of month hour should be 23")
    
    -- Test end_of_month for February
    local feb = datetime_utils.create(2024, 2, 15)
    local eom_feb = datetime_utils.end_of_month(feb)
    assert_equal(eom_feb.day, 29, "End of February 2024 should be 29")
    
    -- Test start_of_year
    local soy = datetime_utils.start_of_year(dt)
    assert_equal(soy.year, 2024, "Start of year should be 2024")
    assert_equal(soy.month, 1, "Start of year month should be 1")
    assert_equal(soy.day, 1, "Start of year day should be 1")
    
    -- Test end_of_year
    local eoy = datetime_utils.end_of_year(dt)
    assert_equal(eoy.year, 2024, "End of year should be 2024")
    assert_equal(eoy.month, 12, "End of year month should be 12")
    assert_equal(eoy.day, 31, "End of year day should be 31")
end

--------------------------------------------------------------------------------
-- Relative Time Tests
--------------------------------------------------------------------------------
print("\n--- Relative Time Tests ---")

do
    local now = datetime_utils.now()
    
    -- Test seconds ago
    local dt1 = datetime_utils.add_seconds(now, -30)
    local rel1 = datetime_utils.relative_time(dt1, now)
    assert_not_nil(rel1, "Should return relative time string")
    assert_true(rel1:find("second") ~= nil, "Should mention seconds")
    
    -- Test minutes ago
    local dt2 = datetime_utils.add_minutes(now, -5)
    local rel2 = datetime_utils.relative_time(dt2, now)
    assert_true(rel2:find("minute") ~= nil, "Should mention minutes")
    
    -- Test hours ago
    local dt3 = datetime_utils.add_hours(now, -3)
    local rel3 = datetime_utils.relative_time(dt3, now)
    assert_true(rel3:find("hour") ~= nil, "Should mention hours")
    
    -- Test days ago
    local dt4 = datetime_utils.add_days(now, -7)
    local rel4 = datetime_utils.relative_time(dt4, now)
    assert_true(rel4:find("day") ~= nil, "Should mention days")
    
    -- Test future time
    local dt5 = datetime_utils.add_hours(now, 2)
    local rel5 = datetime_utils.relative_time(dt5, now)
    assert_true(rel5:find("in") ~= nil, "Should indicate future")
    
    -- Test just now
    local dt6 = datetime_utils.add_seconds(now, -0.5)
    local rel6 = datetime_utils.relative_time(dt6, now)
    assert_equal(rel6, "just now", "Should be just now")
end

--------------------------------------------------------------------------------
-- Clone Tests
--------------------------------------------------------------------------------
print("\n--- Clone Tests ---")

do
    local dt = datetime_utils.create(2024, 3, 15, 14, 30, 45)
    local clone = datetime_utils.clone(dt)
    
    assert_equal(clone.year, dt.year, "Clone should have same year")
    assert_equal(clone.month, dt.month, "Clone should have same month")
    assert_equal(clone.day, dt.day, "Clone should have same day")
    assert_equal(clone.hour, dt.hour, "Clone should have same hour")
    assert_equal(clone.min, dt.min, "Clone should have same min")
    assert_equal(clone.sec, dt.sec, "Clone should have same sec")
    
    -- Test that modifying clone doesn't affect original
    clone.day = 20
    assert_equal(dt.day, 15, "Original should not be affected")
    
    -- Test clone with timestamp
    local ts = datetime_utils.to_timestamp(dt)
    local clone2 = datetime_utils.clone(ts)
    assert_equal(clone2.year, dt.year, "Should clone from timestamp")
end

--------------------------------------------------------------------------------
-- Quarter Tests
--------------------------------------------------------------------------------
print("\n--- Quarter Tests ---")

do
    local q1 = datetime_utils.create(2024, 1, 15)
    assert_equal(datetime_utils.quarter(q1), 1, "January should be Q1")
    
    local q2 = datetime_utils.create(2024, 4, 15)
    assert_equal(datetime_utils.quarter(q2), 2, "April should be Q2")
    
    local q3 = datetime_utils.create(2024, 7, 15)
    assert_equal(datetime_utils.quarter(q3), 3, "July should be Q3")
    
    local q4 = datetime_utils.create(2024, 10, 15)
    assert_equal(datetime_utils.quarter(q4), 4, "October should be Q4")
    
    -- Test edge cases
    assert_equal(datetime_utils.quarter(datetime_utils.create(2024, 3, 31)), 1, "March should be Q1")
    assert_equal(datetime_utils.quarter(datetime_utils.create(2024, 6, 30)), 2, "June should be Q2")
    assert_equal(datetime_utils.quarter(datetime_utils.create(2024, 9, 30)), 3, "September should be Q3")
    assert_equal(datetime_utils.quarter(datetime_utils.create(2024, 12, 31)), 4, "December should be Q4")
end

--------------------------------------------------------------------------------
-- Summary
--------------------------------------------------------------------------------
print("\n========================================")
print(string.format("Tests completed: %d passed, %d failed", tests_passed, tests_failed))
print("========================================")

if tests_failed > 0 then
    os.exit(1)
else
    os.exit(0)
end