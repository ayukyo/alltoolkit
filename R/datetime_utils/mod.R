# datetime_utils/mod.R
# A comprehensive date and time utility module for R with zero dependencies.
# Provides formatting, parsing, arithmetic, and various date/time operations.
#
# Features:
# - Zero dependencies, uses only R standard library
# - Multiple date/time formats (ISO 8601, Chinese, US, compact, etc.)
# - Automatic format detection for parsing
# - Complete time arithmetic (days, hours, minutes, seconds, months, years)
# - Relative time descriptions in Chinese
# - Period boundary calculations (day, week, month, year)
# - Age calculation with birthday handling
#
# Author: AllToolkit
# Version: 1.0.0

#' Get current local datetime
#' @return POSIXct object representing current time
dt_now <- function() {
  return(Sys.time())
}

#' Get current UTC datetime
#' @return POSIXct object representing current UTC time
dt_now_utc <- function() {
  return(as.POSIXct(format(Sys.time(), tz = "UTC"), tz = "UTC"))
}

#' Get today at 00:00:00
#' @return POSIXct object representing start of today
dt_today <- function() {
  return(as.POSIXct(format(Sys.time(), "%Y-%m-%d"), tz = ""))
}

#' Get current timestamp in seconds
#' @return Numeric timestamp (seconds since epoch)
dt_timestamp <- function() {
  return(as.numeric(Sys.time()))
}

#' Get current timestamp in milliseconds
#' @return Numeric timestamp (milliseconds since epoch)
dt_timestamp_ms <- function() {
  return(as.numeric(Sys.time()) * 1000)
}

#' Convert timestamp to datetime
#' @param ts Timestamp value
#' @param unit Unit of timestamp: "s" for seconds, "ms" for milliseconds
#' @param tz Timezone (default: system timezone)
#' @return POSIXct object
dt_timestamp_to_datetime <- function(ts, unit = "s", tz = "") {
  if (unit == "ms") {
    ts <- ts / 1000
  }
  return(as.POSIXct(ts, origin = "1970-01-01", tz = tz))
}

#' Convert datetime to timestamp
#' @param dt POSIXct datetime object
#' @param unit Unit of output: "s" for seconds, "ms" for milliseconds
#' @return Numeric timestamp
dt_datetime_to_timestamp <- function(dt, unit = "s") {
  ts <- as.numeric(dt)
  if (unit == "ms") {
    ts <- ts * 1000
  }
  return(ts)
}

#' Format datetime to string
#' @param dt POSIXct datetime object (default: current time)
#' @param fmt Format string (default: "%Y-%m-%d %H:%M:%S")
#' @return Formatted string
dt_format <- function(dt = NULL, fmt = "%Y-%m-%d %H:%M:%S") {
  if (is.null(dt)) {
    dt <- dt_now()
  }
  return(format(dt, format = fmt))
}

#' Parse string to datetime
#' @param date_string Date string to parse
#' @param fmt Format string
#' @param tz Timezone (default: system timezone)
#' @return POSIXct object or NULL if parsing fails
dt_parse <- function(date_string, fmt, tz = "") {
  tryCatch({
    return(as.POSIXct(date_string, format = fmt, tz = tz))
  }, error = function(e) {
    return(NULL)
  })
}

#' Auto-detect format and parse datetime
#' @param date_string Date string to parse
#' @param tz Timezone (default: system timezone)
#' @return POSIXct object or NULL if parsing fails
dt_parse_auto <- function(date_string, tz = "") {
  formats <- c(
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%OS",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d",
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y",
    "%m-%d-%Y %H:%M:%S",
    "%m-%d-%Y"
  )
  
  for (fmt in formats) {
    result <- dt_parse(date_string, fmt, tz)
    if (!is.null(result) && !is.na(result)) {
      return(result)
    }
  }
  return(NULL)
}

#' Convert to ISO 8601 format
#' @param dt POSIXct datetime object (default: current time)
#' @return ISO 8601 formatted string
dt_to_iso8601 <- function(dt = NULL) {
  if (is.null(dt)) {
    dt <- dt_now()
  }
  return(format(dt, format = "%Y-%m-%dT%H:%M:%S"))
}

#' Parse ISO 8601 string
#' @param iso_string ISO 8601 formatted string
#' @param tz Timezone (default: system timezone)
#' @return POSIXct object or NULL if parsing fails
dt_from_iso8601 <- function(iso_string, tz = "") {
  return(dt_parse(iso_string, "%Y-%m-%dT%H:%M:%S", tz))
}

#' Add days to datetime
#' @param dt POSIXct datetime object
#' @param days Number of days to add (can be negative)
#' @return POSIXct object
dt_add_days <- function(dt, days) {
  return(dt + as.difftime(days, units = "days"))
}

#' Add hours to datetime
#' @param dt POSIXct datetime object
#' @param hours Number of hours to add (can be negative)
#' @return POSIXct object
dt_add_hours <- function(dt, hours) {
  return(dt + as.difftime(hours, units = "hours"))
}

#' Add minutes to datetime
#' @param dt POSIXct datetime object
#' @param minutes Number of minutes to add (can be negative)
#' @return POSIXct object
dt_add_minutes <- function(dt, minutes) {
  return(dt + as.difftime(minutes, units = "mins"))
}

#' Add seconds to datetime
#' @param dt POSIXct datetime object
#' @param seconds Number of seconds to add (can be negative)
#' @return POSIXct object
dt_add_seconds <- function(dt, seconds) {
  return(dt + as.difftime(seconds, units = "secs"))
}

#' Add months to datetime
#' @param dt POSIXct datetime object
#' @param months Number of months to add (can be negative)
#' @return POSIXct object
dt_add_months <- function(dt, months) {
  current_month <- as.numeric(format(dt, "%m"))
  current_year <- as.numeric(format(dt, "%Y"))
  current_day <- as.numeric(format(dt, "%d"))
  
  new_month <- current_month + months
  new_year <- current_year + floor((new_month - 1) / 12)
  new_month <- ((new_month - 1) %% 12) + 1
  
  # Handle day overflow (e.g., Jan 31 + 1 month = Feb 28/29)
  days_in_new_month <- dt_days_in_month(new_year, new_month)
  new_day <- min(current_day, days_in_new_month)
  
  new_date_str <- sprintf("%04d-%02d-%02d %s", 
                          new_year, new_month, new_day,
                          format(dt, "%H:%M:%S"))
  return(as.POSIXct(new_date_str, tz = attr(dt, "tzone")))
}

#' Add years to datetime
#' @param dt POSIXct datetime object
#' @param years Number of years to add (can be negative)
#' @return POSIXct object
dt_add_years <- function(dt, years) {
  current_year <- as.numeric(format(dt, "%Y"))
  current_month <- as.numeric(format(dt, "%m"))
  current_day <- as.numeric(format(dt, "%d"))
  
  new_year <- current_year + years
  
  # Handle Feb 29 in non-leap years
  if (current_month == 2 && current_day == 29) {
    if (!dt_is_leap_year(new_year)) {
      current_day <- 28
    }
  }
  
  new_date_str <- sprintf("%04d-%02d-%02d %s", 
                          new_year, current_month, current_day,
                          format(dt, "%H:%M:%S"))
  return(as.POSIXct(new_date_str, tz = attr(dt, "tzone")))
}

#' Calculate days between two datetimes
#' @param start Start datetime
#' @param end End datetime
#' @return Numeric days
dt_days_between <- function(start, end) {
  return(as.numeric(difftime(end, start, units = "days")))
}

#' Calculate hours between two datetimes
#' @param start Start datetime
#' @param end End datetime
#' @return Numeric hours
dt_hours_between <- function(start, end) {
  return(as.numeric(difftime(end, start, units = "hours")))
}

#' Calculate minutes between two datetimes
#' @param start Start datetime
#' @param end End datetime
#' @return Numeric minutes
dt_minutes_between <- function(start, end) {
  return(as.numeric(difftime(end, start, units = "mins")))
}

#' Calculate seconds between two datetimes
#' @param start Start datetime
#' @param end End datetime
#' @return Numeric seconds
dt_seconds_between <- function(start, end) {
  return(as.numeric(difftime(end, start, units = "secs")))
}

#' Check if datetime is today
#' @param dt POSIXct datetime object
#' @return TRUE if today, FALSE otherwise
dt_is_today <- function(dt) {
  return(format(dt, "%Y-%m-%d") == format(Sys.time(), "%Y-%m-%d"))
}

#' Check if datetime is yesterday
#' @param dt POSIXct datetime object
#' @return TRUE if yesterday, FALSE otherwise
dt_is_yesterday <- function(dt) {
  yesterday <- dt_add_days(dt_today(), -1)
  return(format(dt, "%Y-%m-%d") == format(yesterday, "%Y-%m-%d"))
}

#' Check if datetime is tomorrow
#' @param dt POSIXct datetime object
#' @return TRUE if tomorrow, FALSE otherwise
dt_is_tomorrow <- function(dt) {
  tomorrow <- dt_add_days(dt_today(), 1)
  return(format(dt, "%Y-%m-%d") == format(tomorrow, "%Y-%m-%d"))
}

#' Check if datetime is this week
#' @param dt POSIXct datetime object
#' @return TRUE if this week, FALSE otherwise
dt_is_this_week <- function(dt) {
  today <- dt_today()
  start_of_week <- dt_start_of_week(today)
  end_of_week <- dt_end_of_week(today)
  return(dt >= start_of_week && dt <= end_of_week)
}

#' Check if datetime is this month
#' @param dt POSIXct datetime object
#' @return TRUE if this month, FALSE otherwise
dt_is_this_month <- function(dt) {
  today <- dt_today()
  return(format(dt, "%Y-%m") == format(today, "%Y-%m"))
}

#' Check if datetime is this year
#' @param dt POSIXct datetime object
#' @return TRUE if this year, FALSE otherwise
dt_is_this_year <- function(dt) {
  return(format(dt, "%Y") == format(Sys.time(), "%Y"))
}

#' Check if datetime is weekend
#' @param dt POSIXct datetime object
#' @return TRUE if weekend, FALSE otherwise
dt_is_weekend <- function(dt) {
  weekday <- as.numeric(format(dt, "%w"))
  return(weekday == 0 || weekday == 6)
}

#' Check if datetime is weekday
#' @param dt POSIXct datetime object
#' @return TRUE if weekday, FALSE otherwise
dt_is_weekday <- function(dt) {
  return(!dt_is_weekend(dt))
}

#' Check if year is leap year
#' @param year Numeric year
#' @return TRUE if leap year, FALSE otherwise
dt_is_leap_year <- function(year) {
  return((year %% 4 == 0 && year %% 100 != 0) || (year %% 400 == 0))
}

#' Get days in month
#' @param year Numeric year
#' @param month Numeric month (1-12)
#' @return Number of days in month
dt_days_in_month <- function(year, month) {
  if (month == 2) {
    if (dt_is_leap_year(year)) {
      return(29)
    } else {
      return(28)
    }
  } else if (month %in% c(4, 6, 9, 11)) {
    return(30)
  } else {
    return(31)
  }
}

#' Get start of day
#' @param dt POSIXct datetime object
#' @return POSIXct object at 00:00:00
dt_start_of_day <- function(dt) {
  return(as.POSIXct(format(dt, "%Y-%m-%d"), tz = attr(dt, "tzone")))
}

#' Get end of day
#' @param dt POSIXct datetime object
#' @return POSIXct object at 23:59:59
dt_end_of_day <- function(dt) {
  return(dt_start_of_day(dt) + as.difftime(86399, units = "secs"))
}

#' Get start of week (Monday)
#' @param dt POSIXct datetime object
#' @return POSIXct object at start of week
dt_start_of_week <- function(dt) {
  weekday <- as.numeric(format(dt, "%w"))
  if (weekday == 0) weekday <- 7
  days_to_subtract <- weekday - 1
  return(dt_add_days(dt_start_of_day(dt), -days_to_subtract))
}

#' Get end of week (Sunday)
#' @param dt POSIXct datetime object
#' @return POSIXct object at end of week
dt_end_of_week <- function(dt) {
  weekday <- as.numeric(format(dt, "%w"))
  if (weekday == 0) weekday <- 7
  days_to_add <- 7 - weekday
  return(dt_add_days(dt_end_of_day(dt), days_to_add))
}

#' Get start of month
#' @param dt POSIXct datetime object
#' @return POSIXct object at start of month
dt_start_of_month <- function(dt) {
  year <- format(dt, "%Y")
  month <- format(dt, "%m")
  return(as.POSIXct(paste0(year, "-", month, "-01"), tz = attr(dt, "tzone")))
}

#' Get end of month
#' @param dt POSIXct datetime object
#' @return POSIXct object at end of month
dt_end_of_month <- function(dt) {
  year <- as.numeric(format(dt, "%Y"))
  month <- as.numeric(format(dt, "%m"))
  days <- dt_days_in_month(year, month)
  start <- dt_start_of_month(dt)
  return(start + as.difftime(days * 86400 - 1, units = "secs"))
}

#' Get start of year
#' @param dt POSIXct datetime object
#' @return POSIXct object at start of year
dt_start_of_year <- function(dt) {
  year <- format(dt, "%Y")
  return(as.POSIXct(paste0(year, "-01-01"), tz = attr(dt, "tzone")))
}

#' Get end of year
#' @param dt POSIXct datetime object
#' @return POSIXct object at end of year
dt_end_of_year <- function(dt) {
  year <- format(dt, "%Y")
  return(as.POSIXct(paste0(year, "-12-31 23:59:59"), tz = attr(dt, "tzone")))
}

#' Calculate age from birth date
#' @param birth_date POSIXct datetime object
#' @param today Reference date (default: current date)
#' @return Numeric age in years
dt_get_age <- function(birth_date, today = NULL) {
  if (is.null(today)) {
    today <- dt_today()
  }
  
  birth_year <- as.numeric(format(birth_date, "%Y"))
  birth_month <- as.numeric(format(birth_date, "%m"))
  birth_day <- as.numeric(format(birth_date, "%d"))
  
  today_year <- as.numeric(format(today, "%Y"))
  today_month <- as.numeric(format(today, "%m"))
  today_day <- as.numeric(format(today, "%d"))
  
  age <- today_year - birth_year
  
  # Adjust if birthday hasn't occurred this year
  if (today_month < birth_month || 
      (today_month == birth_month && today_day < birth_day)) {
    age <- age - 1
  }
  
  return(age)
}

#' Get relative time description in Chinese
#' @param dt POSIXct datetime object
#' @param now Reference time (default: current time)
#' @return Character string describing relative time
dt_relative_time <- function(dt, now = NULL) {
  if (is.null(now)) {
    now <- dt_now()
  }
  
  diff_secs <- as.numeric(difftime(now, dt, units = "secs"))
  
  if (diff_secs < 0) {
    # Future
    diff_secs <- abs(diff_secs)
    if (diff_secs < 60) {
      return("即将")
    } else if (diff_secs < 3600) {
      mins <- floor(diff_secs / 60)
      return(paste0(mins, "分钟后"))
    } else if (diff_secs < 86400) {
      hours <- floor(diff_secs / 3600)
      return(paste0(hours, "小时后"))
    } else {
      days <- floor(diff_secs / 86400)
      return(paste0(days, "天后"))
    }
  } else {
    # Past
    if (diff_secs < 60) {
      return("刚刚")
    } else if (diff_secs < 3600) {
      mins <- floor(diff_secs / 60)
      return(paste0(mins, "分钟前"))
    } else if (diff_secs < 7200) {
      return("1小时前")
    } else if (diff_secs < 86400) {
      hours <- floor(diff_secs / 3600)
      return(paste0(hours, "小时前"))
    } else if (diff_secs < 172800) {
      return("昨天")
    } else if (diff_secs < 604800) {
      days <- floor(diff_secs / 86400)
      return(paste0(days, "天前"))
    } else if (diff_secs < 2592000) {
      weeks <- floor(diff_secs / 604800)
      return(paste0(weeks, "周前"))
    } else if (diff_secs < 31536000) {
      months <- floor(diff_secs / 2592000)
      return(paste0(months, "个月前"))
    } else {
      years <- floor(diff_secs / 31536000)
      return(paste0(years, "年前"))
    }
  }
}

#' Format duration to readable string
#' @param seconds Duration in seconds
#' @return Character string describing duration
dt_format_duration <- function(seconds) {
  if (seconds < 60) {
    return(paste0(seconds, "秒"))
  } else if (seconds < 3600) {
    mins <- floor(seconds / 60)
    secs <- seconds %% 60
    if (secs == 0) {
      return(paste0(mins, "分钟"))
    } else {
      return(paste0(mins, "分", secs, "秒"))
    }
  } else if (seconds < 86400) {
    hours <- floor(seconds / 3600)
    mins <- floor((seconds %% 3600) / 60)
    if (mins == 0) {
