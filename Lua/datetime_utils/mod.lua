--[[
datetime_utils.lua - A comprehensive datetime utility library for Lua
Provides date/time parsing, formatting, manipulation, and calculations
Zero external dependencies - uses only Lua standard library
]]

local datetime_utils = {}

-- Constants
local DAYS_IN_WEEK = 7
local SECONDS_IN_MINUTE = 60
local SECONDS_IN_HOUR = 3600
local SECONDS_IN_DAY = 86400
local MONTHS_IN_YEAR = 12

local MONTH_NAMES = {
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
}

local MONTH_NAMES_SHORT = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
}

local DAY_NAMES = {
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
}

local DAY_NAMES_SHORT = {
    "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
}

-- Days in each month (non-leap year)
local DAYS_IN_MONTH = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}

--------------------------------------------------------------------------------
-- Helper Functions
--------------------------------------------------------------------------------

-- Check if a year is a leap year
local function is_leap_year(year)
    return (year % 4 == 0 and year % 100 ~= 0) or (year % 400 == 0)
end

-- Get days in a specific month
local function days_in_month(year, month)
    if month == 2 and is_leap_year(year) then
        return 29
    end
    return DAYS_IN_MONTH[month]
end

-- Validate date components
local function validate_date(year, month, day, hour, min, sec)
    if type(year) ~= "number" or type(month) ~= "number" or type(day) ~= "number" then
        return false, "year, month, and day must be numbers"
    end

    if month < 1 or month > 12 then
        return false, "month must be between 1 and 12"
    end

    if day < 1 or day > days_in_month(year, month) then
        return false, "invalid day for the given month/year"
    end

    if hour then
        if type(hour) ~= "number" or hour < 0 or hour >= 24 then
            return false, "hour must be between 0 and 23"
        end
    end

    if min then
        if type(min) ~= "number" or min < 0 or min >= 60 then
            return false, "minute must be between 0 and 59"
        end
    end

    if sec then
        if type(sec) ~= "number" or sec < 0 or sec >= 60 then
            return false, "second must be between 0 and 59"
        end
    end

    return true
end

--------------------------------------------------------------------------------
-- Core Functions
--------------------------------------------------------------------------------

-- Get current timestamp (seconds since Unix epoch)
function datetime_utils.now()
    return os.time()
end

-- Get current date as a table
function datetime_utils.today()
    return os.date("*t")
end

-- Create a datetime table from components
function datetime_utils.create(year, month, day, hour, min, sec)
    hour = hour or 0
    min = min or 0
    sec = sec or 0

    local valid, err = validate_date(year, month, day, hour, min, sec)
    if not valid then
        return nil, err
    end

    return {
        year = year,
        month = month,
        day = day,
        hour = hour,
        min = min,
        sec = sec,
        wday = tonumber(os.date("%w", os.time({
            year = year, month = month, day = day, hour = hour, min = min, sec = sec
        }))) + 1  -- Lua wday is 1-7 (Sunday = 1)
    }
end

-- Convert datetime table to timestamp
function datetime_utils.to_timestamp(dt)
    if type(dt) == "table" then
        return os.time(dt)
    end
    return dt
end

-- Convert timestamp to datetime table
function datetime_utils.from_timestamp(timestamp)
    if type(timestamp) ~= "number" then
        return nil, "timestamp must be a number"
    end
    return os.date("*t", timestamp)
end

--------------------------------------------------------------------------------
-- Parsing Functions
--------------------------------------------------------------------------------

-- Parse ISO 8601 date string (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
function datetime_utils.parse_iso(str)
    if type(str) ~= "string" then
        return nil, "input must be a string"
    end

    local year, month, day, hour, min, sec

    -- Try parsing full datetime format
    year, month, day, hour, min, sec = str:match("(%d%d%d%d)%-(%d%d)%-(%d%d)[T ](%d%d):(%d%d):(%d%d)")

    if year then
        return datetime_utils.create(
            tonumber(year), tonumber(month), tonumber(day),
            tonumber(hour), tonumber(min), tonumber(sec)
        )
    end

    -- Try parsing date-only format
    year, month, day = str:match("(%d%d%d%d)%-(%d%d)%-(%d%d)")

    if year then
        return datetime_utils.create(tonumber(year), tonumber(month), tonumber(day))
    end

    return nil, "invalid ISO 8601 format"
end

-- Parse common date formats
function datetime_utils.parse(str, format)
    if type(str) ~= "string" then
        return nil, "input must be a string"
    end

    format = format or "%Y-%m-%d"

    -- Built-in format patterns with capture order info
    -- Each entry has: pattern, order (which capture is year/month/day/hour/min/sec)
    local formats = {
        ["%Y-%m-%d"] = { pattern = "(%d%d%d%d)%-(%d%d)%-(%d%d)", order = {1, 2, 3} },  -- Y M D
        ["%Y/%m/%d"] = { pattern = "(%d%d%d%d)/(%d%d)/(%d%d)", order = {1, 2, 3} },    -- Y M D
        ["%d/%m/%Y"] = { pattern = "(%d%d)/(%d%d)/(%d%d%d%d)", order = {3, 2, 1} },    -- D M Y -> Y M D
        ["%m/%d/%Y"] = { pattern = "(%d%d)/(%d%d)/(%d%d%d%d)", order = {3, 1, 2} },    -- M D Y -> Y M D
        ["%d-%m-%Y"] = { pattern = "(%d%d)%-(%d%d)%-(%d%d%d%d)", order = {3, 2, 1} },  -- D M Y -> Y M D
        ["%Y%m%d"] = { pattern = "(%d%d%d%d)(%d%d)(%d%d)", order = {1, 2, 3} },        -- Y M D
        ["%Y-%m-%d %H:%M:%S"] = { pattern = "(%d%d%d%d)%-(%d%d)%-(%d%d) (%d%d):(%d%d):(%d%d)", order = {1, 2, 3, 4, 5, 6} },
        ["%d %b %Y"] = { pattern = "(%d%d)%s+(%a%a%a)%s+(%d%d%d%d)", order = {3, 2, 1}, month_name = true },
        ["%d %B %Y"] = { pattern = "(%d%d)%s+(%a+)%s+(%d%d%d%d)", order = {3, 2, 1}, month_name = true },
    }

    local fmt = formats[format]
    if not fmt then
        return nil, "unsupported format: " .. format
    end

    local captures = {str:match(fmt.pattern)}

    if #captures == 0 or not captures[1] then
        return nil, "unable to parse date string"
    end

    local order = fmt.order
    local year = tonumber(captures[order[1]])
    local month, day, hour, min, sec

    -- Handle month names
    if fmt.month_name then
        local month_map = {
            ["Jan"] = 1, ["Feb"] = 2, ["Mar"] = 3, ["Apr"] = 4,
            ["May"] = 5, ["Jun"] = 6, ["Jul"] = 7, ["Aug"] = 8,
            ["Sep"] = 9, ["Oct"] = 10, ["Nov"] = 11, ["Dec"] = 12,
            ["January"] = 1, ["February"] = 2, ["March"] = 3, ["April"] = 4,
            ["May"] = 5, ["June"] = 6, ["July"] = 7, ["August"] = 8,
            ["September"] = 9, ["October"] = 10, ["November"] = 11, ["December"] = 12
        }
        month = month_map[captures[order[2]]]
        if not month then
            return nil, "invalid month name"
        end
    else
        month = tonumber(captures[order[2]])
    end

    day = tonumber(captures[order[3]])

    if order[4] then hour = tonumber(captures[order[4]]) else hour = 0 end
    if order[5] then min = tonumber(captures[order[5]]) else min = 0 end
    if order[6] then sec = tonumber(captures[order[6]]) else sec = 0 end

    return datetime_utils.create(year, month, day, hour, min, sec)
end

--------------------------------------------------------------------------------
-- Formatting Functions
--------------------------------------------------------------------------------

-- Format datetime as ISO 8601 string
function datetime_utils.format_iso(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return string.format("%04d-%02d-%02dT%02d:%02d:%02d",
        dt.year, dt.month, dt.day, dt.hour or 0, dt.min or 0, dt.sec or 0)
end

-- Format datetime as ISO date (YYYY-MM-DD)
function datetime_utils.format_date(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return string.format("%04d-%02d-%02d", dt.year, dt.month, dt.day)
end

-- Format datetime as time (HH:MM:SS)
function datetime_utils.format_time(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return string.format("%02d:%02d:%02d", dt.hour or 0, dt.min or 0, dt.sec or 0)
end

-- Custom format with placeholders
function datetime_utils.format(dt, pattern)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local result = pattern
    local wday = dt.wday or (tonumber(os.date("%w", os.time(dt))) + 1)

    -- Replace placeholders (order matters - use unique non-alphabetic tokens!)
    -- Step 1: Replace text placeholders with unique control-character tokens
    result = result:gsub("MMMM", "\x02")  -- Full month name
    result = result:gsub("MMM", "\x03")   -- Short month name
    result = result:gsub("DDDD", "\x04")  -- Full day name
    result = result:gsub("DDD", "\x05")   -- Short day name
    
    -- Step 2: Replace numeric placeholders
    result = result:gsub("YYYY", string.format("%04d", dt.year))
    result = result:gsub("YY", string.format("%02d", dt.year % 100))
    result = result:gsub("MM", string.format("%02d", dt.month))
    result = result:gsub("M", tostring(dt.month))
    result = result:gsub("DD", string.format("%02d", dt.day))
    result = result:gsub("D", tostring(dt.day))
    result = result:gsub("HH", string.format("%02d", dt.hour or 0))
    result = result:gsub("H", tostring(dt.hour or 0))
    result = result:gsub("mm", string.format("%02d", dt.min or 0))
    result = result:gsub("m", tostring(dt.min or 0))
    result = result:gsub("SS", string.format("%02d", dt.sec or 0))
    result = result:gsub("S", tostring(dt.sec or 0))
    
    -- Step 3: Replace unique tokens back with actual values
    result = result:gsub("\x02", MONTH_NAMES[dt.month] or "")
    result = result:gsub("\x03", MONTH_NAMES_SHORT[dt.month] or "")
    result = result:gsub("\x04", DAY_NAMES[wday] or "")
    result = result:gsub("\x05", DAY_NAMES_SHORT[wday] or "")

    return result
end

--------------------------------------------------------------------------------
-- Date Arithmetic Functions
--------------------------------------------------------------------------------

-- Add days to a date
function datetime_utils.add_days(dt, days)
    if type(dt) == "number" then
        return dt + (days * SECONDS_IN_DAY)
    end

    local timestamp = datetime_utils.to_timestamp(dt)
    if not timestamp then
        return nil, "invalid datetime"
    end

    return datetime_utils.from_timestamp(timestamp + (days * SECONDS_IN_DAY))
end

-- Add months to a date
function datetime_utils.add_months(dt, months)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local new_month = dt.month + months
    local new_year = dt.year + math.floor((new_month - 1) / 12)
    new_month = ((new_month - 1) % 12) + 1

    -- Adjust day if necessary (e.g., Jan 31 + 1 month = Feb 28/29)
    local new_day = math.min(dt.day, days_in_month(new_year, new_month))

    return datetime_utils.create(new_year, new_month, new_day, dt.hour, dt.min, dt.sec)
end

-- Add years to a date
function datetime_utils.add_years(dt, years)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local new_year = dt.year + years

    -- Adjust day for leap year (Feb 29 -> Feb 28)
    local new_day = dt.day
    if dt.month == 2 and dt.day == 29 and not is_leap_year(new_year) then
        new_day = 28
    end

    return datetime_utils.create(new_year, dt.month, new_day, dt.hour, dt.min, dt.sec)
end

-- Add hours to a datetime
function datetime_utils.add_hours(dt, hours)
    if type(dt) == "number" then
        return dt + (hours * SECONDS_IN_HOUR)
    end

    local timestamp = datetime_utils.to_timestamp(dt)
    if not timestamp then
        return nil, "invalid datetime"
    end

    return datetime_utils.from_timestamp(timestamp + (hours * SECONDS_IN_HOUR))
end

-- Add minutes to a datetime
function datetime_utils.add_minutes(dt, minutes)
    if type(dt) == "number" then
        return dt + (minutes * SECONDS_IN_MINUTE)
    end

    local timestamp = datetime_utils.to_timestamp(dt)
    if not timestamp then
        return nil, "invalid datetime"
    end

    return datetime_utils.from_timestamp(timestamp + (minutes * SECONDS_IN_MINUTE))
end

-- Add seconds to a datetime
function datetime_utils.add_seconds(dt, seconds)
    if type(dt) == "number" then
        return dt + seconds
    end

    local timestamp = datetime_utils.to_timestamp(dt)
    if not timestamp then
        return nil, "invalid datetime"
    end

    return datetime_utils.from_timestamp(timestamp + seconds)
end

--------------------------------------------------------------------------------
-- Difference Functions
--------------------------------------------------------------------------------

-- Calculate difference in days between two dates
function datetime_utils.diff_days(dt1, dt2)
    local t1 = type(dt1) == "number" and dt1 or datetime_utils.to_timestamp(dt1)
    local t2 = type(dt2) == "number" and dt2 or datetime_utils.to_timestamp(dt2)

    if not t1 or not t2 then
        return nil, "invalid datetime"
    end

    return math.floor((t2 - t1) / SECONDS_IN_DAY)
end

-- Calculate difference in seconds between two datetimes
function datetime_utils.diff_seconds(dt1, dt2)
    local t1 = type(dt1) == "number" and dt1 or datetime_utils.to_timestamp(dt1)
    local t2 = type(dt2) == "number" and dt2 or datetime_utils.to_timestamp(dt2)

    if not t1 or not t2 then
        return nil, "invalid datetime"
    end

    return t2 - t1
end

-- Calculate difference in hours between two datetimes
function datetime_utils.diff_hours(dt1, dt2)
    local seconds = datetime_utils.diff_seconds(dt1, dt2)
    if not seconds then
        return nil, "invalid datetime"
    end
    return seconds / SECONDS_IN_HOUR
end

-- Calculate difference in minutes between two datetimes
function datetime_utils.diff_minutes(dt1, dt2)
    local seconds = datetime_utils.diff_seconds(dt1, dt2)
    if not seconds then
        return nil, "invalid datetime"
    end
    return seconds / SECONDS_IN_MINUTE
end

-- Calculate the number of months between two dates
function datetime_utils.diff_months(dt1, dt2)
    if type(dt1) == "number" then
        dt1 = datetime_utils.from_timestamp(dt1)
    end
    if type(dt2) == "number" then
        dt2 = datetime_utils.from_timestamp(dt2)
    end

    if type(dt1) ~= "table" or type(dt2) ~= "table" then
        return nil, "invalid datetime"
    end

    local months = (dt2.year - dt1.year) * 12 + (dt2.month - dt1.month)

    -- Adjust for day of month
    if dt2.day < dt1.day then
        months = months - 1
    end

    return months
end

--------------------------------------------------------------------------------
-- Comparison Functions
--------------------------------------------------------------------------------

-- Check if date1 is before date2
function datetime_utils.is_before(dt1, dt2)
    local t1 = type(dt1) == "number" and dt1 or datetime_utils.to_timestamp(dt1)
    local t2 = type(dt2) == "number" and dt2 or datetime_utils.to_timestamp(dt2)

    if not t1 or not t2 then
        return nil, "invalid datetime"
    end

    return t1 < t2
end

-- Check if date1 is after date2
function datetime_utils.is_after(dt1, dt2)
    local t1 = type(dt1) == "number" and dt1 or datetime_utils.to_timestamp(dt1)
    local t2 = type(dt2) == "number" and dt2 or datetime_utils.to_timestamp(dt2)

    if not t1 or not t2 then
        return nil, "invalid datetime"
    end

    return t1 > t2
end

-- Check if date1 equals date2
function datetime_utils.is_equal(dt1, dt2)
    local t1 = type(dt1) == "number" and dt1 or datetime_utils.to_timestamp(dt1)
    local t2 = type(dt2) == "number" and dt2 or datetime_utils.to_timestamp(dt2)

    if not t1 or not t2 then
        return nil, "invalid datetime"
    end

    return t1 == t2
end

-- Check if date is between two dates
function datetime_utils.is_between(dt, start_dt, end_dt)
    return datetime_utils.is_after(dt, start_dt) and datetime_utils.is_before(dt, end_dt)
end

--------------------------------------------------------------------------------
-- Utility Functions
--------------------------------------------------------------------------------

-- Check if a year is a leap year
function datetime_utils.leap_year(year)
    return is_leap_year(year)
end

-- Get the number of days in a month
function datetime_utils.get_days_in_month(year, month)
    return days_in_month(year, month)
end

-- Get the day of the week (1-7, Sunday = 1)
function datetime_utils.day_of_week(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local timestamp = os.time(dt)
    return tonumber(os.date("%w", timestamp)) + 1
end

-- Get the day of the year (1-366)
function datetime_utils.day_of_year(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local day_count = 0
    for m = 1, dt.month - 1 do
        day_count = day_count + days_in_month(dt.year, m)
    end
    day_count = day_count + dt.day

    return day_count
end

-- Get the week of the year
function datetime_utils.week_of_year(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local doy = datetime_utils.day_of_year(dt)
    local first_day = datetime_utils.create(dt.year, 1, 1)
    local first_wday = datetime_utils.day_of_week(first_day)

    return math.floor((doy + first_wday - 2) / 7) + 1
end

-- Check if a date is a weekend (Saturday or Sunday)
function datetime_utils.is_weekend(dt)
    local wday = datetime_utils.day_of_week(dt)
    return wday == 1 or wday == 7
end

-- Check if a date is a weekday (Monday-Friday)
function datetime_utils.is_weekday(dt)
    return not datetime_utils.is_weekend(dt)
end

-- Get the start of a day (midnight)
function datetime_utils.start_of_day(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, dt.month, dt.day, 0, 0, 0)
end

-- Get the end of a day (23:59:59)
function datetime_utils.end_of_day(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, dt.month, dt.day, 23, 59, 59)
end

-- Get the start of a week (Sunday)
function datetime_utils.start_of_week(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local wday = datetime_utils.day_of_week(dt)
    return datetime_utils.add_days(dt, -(wday - 1))
end

-- Get the end of a week (Saturday)
function datetime_utils.end_of_week(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    local wday = datetime_utils.day_of_week(dt)
    return datetime_utils.add_days(dt, (7 - wday))
end

-- Get the start of a month
function datetime_utils.start_of_month(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, dt.month, 1, 0, 0, 0)
end

-- Get the end of a month
function datetime_utils.end_of_month(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, dt.month, days_in_month(dt.year, dt.month), 23, 59, 59)
end

-- Get the start of a year
function datetime_utils.start_of_year(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, 1, 1, 0, 0, 0)
end

-- Get the end of a year
function datetime_utils.end_of_year(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return datetime_utils.create(dt.year, 12, 31, 23, 59, 59)
end

-- Get relative time string (e.g., "2 hours ago", "in 3 days")
function datetime_utils.relative_time(dt, from)
    from = from or datetime_utils.now()

    local t = type(dt) == "number" and dt or datetime_utils.to_timestamp(dt)
    local f = type(from) == "number" and from or datetime_utils.to_timestamp(from)

    if not t or not f then
        return nil, "invalid datetime"
    end

    local diff = t - f
    local abs_diff = math.abs(diff)
    local future = diff > 0

    local function format_result(value, unit)
        local suffix = future and "in " or " ago"
        local prefix = future and "in " or ""
        local str = value .. " " .. unit
        if value ~= 1 then
            str = str .. "s"
        end
        return prefix .. str .. (not future and " ago" or "")
    end

    if abs_diff < 60 then
        if abs_diff < 1 then
            return "just now"
        end
        local result = abs_diff .. " second"
        if abs_diff ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    elseif abs_diff < 3600 then
        local minutes = math.floor(abs_diff / 60)
        local result = minutes .. " minute"
        if minutes ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    elseif abs_diff < 86400 then
        local hours = math.floor(abs_diff / 3600)
        local result = hours .. " hour"
        if hours ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    elseif abs_diff < 2592000 then  -- ~30 days
        local days = math.floor(abs_diff / 86400)
        local result = days .. " day"
        if days ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    elseif abs_diff < 31536000 then  -- ~1 year
        local months = math.floor(abs_diff / 2592000)
        local result = months .. " month"
        if months ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    else
        local years = math.floor(abs_diff / 31536000)
        local result = years .. " year"
        if years ~= 1 then
            result = result .. "s"
        end
        return future and "in " .. result or result .. " ago"
    end
end

-- Clone a datetime table
function datetime_utils.clone(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return {
        year = dt.year,
        month = dt.month,
        day = dt.day,
        hour = dt.hour,
        min = dt.min,
        sec = dt.sec,
        wday = dt.wday
    }
end

-- Get quarter of year (1-4)
function datetime_utils.quarter(dt)
    if type(dt) == "number" then
        dt = datetime_utils.from_timestamp(dt)
    end

    if type(dt) ~= "table" then
        return nil, "invalid datetime"
    end

    return math.floor((dt.month - 1) / 3) + 1
end

-- Export constants
datetime_utils.MONTH_NAMES = MONTH_NAMES
datetime_utils.MONTH_NAMES_SHORT = MONTH_NAMES_SHORT
datetime_utils.DAY_NAMES = DAY_NAMES
datetime_utils.DAY_NAMES_SHORT = DAY_NAMES_SHORT

return datetime_utils