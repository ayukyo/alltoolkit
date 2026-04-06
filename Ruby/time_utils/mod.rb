#!/usr/bin/env ruby
# frozen_string_literal: true

module AllToolkit
  module TimeUtils
    FORMAT_ISO8601 = '%Y-%m-%dT%H:%M:%S%z'
    FORMAT_ISO8601_DATE = '%Y-%m-%d'
    FORMAT_RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
    FORMAT_SHORT_DATE = '%Y-%m-%d'
    FORMAT_SHORT_TIME = '%H:%M'
    FORMAT_LONG_DATE = '%B %d, %Y'
    FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'
    FORMAT_CHINESE = '%Y年%m月%d日 %H时%M分%S秒'
    FORMAT_CHINESE_DATE = '%Y年%m月%d日'
    FORMAT_US = '%m/%d/%Y %I:%M %p'
    FORMAT_EU = '%d/%m/%Y %H:%M:%S'
    FORMAT_COMPACT = '%Y%m%d%H%M%S'

    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800

    WEEKDAYS_EN = %w[Sunday Monday Tuesday Wednesday Thursday Friday Saturday]
    WEEKDAYS_EN_SHORT = %w[Sun Mon Tue Wed Thu Fri Sat]
    WEEKDAYS_CN = %w[星期日 星期一 星期二 星期三 星期四 星期五 星期六]
    WEEKDAYS_CN_SHORT = %w[周日 周一 周二 周三 周四 周五 周六]

    MONTHS_EN = %w[January February March April May June July August September October November December]
    MONTHS_EN_SHORT = %w[Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec]
    MONTHS_CN = %w[一月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月]

    def self.format(time, format = FORMAT_DATETIME)
      return nil if time.nil?
      time.strftime(format)
    end

    def self.to_iso8601(time)
      format(time, FORMAT_ISO8601)
    end

    def self.to_rfc2822(time)
      format(time, FORMAT_RFC2822)
    end

    def self.to_short_date(time)
      format(time, FORMAT_SHORT_DATE)
    end

    def self.to_short_time(time)
      format(time, FORMAT_SHORT_TIME)
    end

    def self.to_long_date(time, locale: :en)
      return nil if time.nil?
      locale == :cn ? format(time, FORMAT_CHINESE_DATE) : format(time, FORMAT_LONG_DATE)
    end

    def self.to_chinese(time)
      format(time, FORMAT_CHINESE)
    end

    def self.to_compact(time)
      format(time, FORMAT_COMPACT)
    end

    def self.parse(time_string, format = FORMAT_DATETIME, default: nil)
      return default if time_string.nil? || time_string.empty?
      Time.strptime(time_string, format)
    rescue ArgumentError
      default
    end

    def self.parse_auto(time_string, default: nil)
      return default if time_string.nil? || time_string.empty?
      formats = [
        FORMAT_ISO8601, FORMAT_DATETIME, FORMAT_SHORT_DATE, FORMAT_US, FORMAT_EU,
        '%Y/%m/%d %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S',
        '%Y%m%d%H%M%S', '%Y%m%d', FORMAT_RFC2822
      ]
      formats.each do |fmt|
        result = parse(time_string, fmt, default: nil)
        return result if result
      end
      default
    end

    def self.parse_iso8601(time_string, default: nil)
      parse(time_string, FORMAT_ISO8601, default: default)
    end

    def self.add_seconds(time, seconds)
      return nil if time.nil?
      time + seconds
    end

    def self.add_minutes(time, minutes)
      add_seconds(time, minutes * MINUTE)
    end

    def self.add_hours(time, hours)
      add_seconds(time, hours * HOUR)
    end

    def self.add_days(time, days)
      add_seconds(time, days * DAY)
    end

    def self.add_weeks(time, weeks)
      add_seconds(time, weeks * WEEK)
    end

    def self.add_months(time, months)
      return nil if time.nil?
      year = time.year + (time.month - 1 + months) / 12
      month = ((time.month - 1 + months) % 12) + 1
      day = [time.day, days_in_month(year, month)].min
      Time.local(year, month, day, time.hour, time.min, time.sec)
    end

    def self.add_years(time, years)
      return nil if time.nil?
      add_months(time, years * 12)
    end

    def self.difference_in_seconds(time1, time2)
      return nil if time1.nil? || time2.nil?
      (time1 - time2).abs
    end

    def self.difference_in_minutes(time1, time2)
      difference_in_seconds(time1, time2) / MINUTE
    end

    def self.difference_in_hours(time1, time2)
      difference_in_seconds(time1, time2) / HOUR
    end

    def self.difference_in_days(time1, time2)
      difference_in_seconds(time1, time2) / DAY
    end

    def self.difference_in_weeks(time1, time2)
      difference_in_seconds(time1, time2) / WEEK
    end

    def self.relative_time(time, from_time = Time.now, locale: :en)
      return nil if time.nil?
      diff = from_time - time
      is_future = diff < 0
      diff = diff.abs
      locale == :cn ? relative_time_cn(diff, is_future) : relative_time_en(diff, is_future)
    end

    def self.relative_time_en(diff, is_future)
      unit, value = case diff
                    when 0...10 then ['just now', 0]
                    when 10...60 then ['second', diff.round]
                    when 60...3600 then ['minute', (diff / 60).round]
                    when 3600...86400 then ['hour', (diff / 3600).round]
                    when 86400...604800 then ['day', (diff / 86400).round]
                    when 604800...2592000 then ['week', (diff / 604800).round]
                    when 2592000...31536000 then ['month', (diff / 2592000).round]
                    else ['year', (diff / 31536000).round]
                    end
      return unit if value == 0
      suffix = is_future ? 'from now' : 'ago'
      "#{value} #{unit}#{value == 1 ? '' : 's'} #{suffix}"
    end

    def self.relative_time_cn(diff, is_future)
      return '刚刚' if diff < 10
      value, unit = case diff
                    when 10...60 then [diff.round, '秒']
                    when 60...3600 then [(diff / 60).round, '分钟']
                    when 3600...86400 then [(diff / 3600).round, '小时']
                    when 86400...604800 then [(diff / 86400).round, '天']
                    when 604800...2592000 then [(diff / 604800).round, '周']
                    when 2592000...31536000 then [(diff / 2592000).round, '个月']
                    else [(diff / 31536000).round, '年']
                    end
      is_future ? "#{value}#{unit}后" : "#{value}#{unit}前"
    end

    def self.is_today?(time)
      return false if time.nil?
      time.to_date == Time.now.to_date
    end

    def self.is_yesterday?(time)
      return false if time.nil?
      time.to_date == (Time.now - DAY).to_date
    end

    def self.is_tomorrow?(time)
      return false if time.nil?
      time.to_date == (Time.now + DAY).to_date
    end

    def self.is_this_week?(time)
      return false if time.nil?
      now = Time.now
      time.to_date >= (now - now.wday * DAY).to_date && time.to_date <= (now + (6 - now.wday) * DAY).to_date
    end

    def self.is_this_month?(time)
      return false if time.nil?
      now = Time.now
      time.year == now.year && time.month == now.month
    end

    def self.is_this_year?(time)
      return false if time.nil?
      time.year == Time.now.year
    end

    def self.is_weekend?(time)
      return false if time.nil?
      time.wday == 0 || time.wday == 6
    end

    def self.is_weekday?(time)
      !is_weekend?(time)
    end

    def self.is_leap_year?(year)
      (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
    end

    def self.days_in_month(year, month)
      days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
      days[1] = 29 if is_leap_year?(year)
      days[month - 1]
    end

    def self.start_of_day(time)
      return nil if time.nil?
      Time.local(time.year, time.month, time.day, 0, 0, 0)
    end

    def self.end_of_day(time)
      return nil if time.nil?
      Time.local(time.year, time.month, time.day, 23, 59, 59)
    end

    def self.start_of_week(time)
      return nil if time.nil?
      start_of_day(time - time.wday * DAY)
    end

    def self.end_of_week(time)
      return nil if time.nil?
      end_of_day(time + (6 - time.wday) * DAY)
    end

    def self.start_of_month(time)
      return nil if time.nil?
      Time.local(time.year, time.month, 1, 0, 0, 0)
    end

    def self.end_of_month(time)
      return nil if time.nil?
      Time.local(time.year, time.month, days_in_month(time.year, time.month), 23, 59, 59)
    end

    def self.start_of_year(time)
      return nil if time.nil?
      Time.local(time.year, 1, 1, 0, 0, 0)
    end

    def self.end_of_year(time)
      return nil if time.nil?
      Time.local(time.year, 12, 31, 23, 59, 59)
    end

    def self.weekday_name(time, locale: :en, short: false)
      return nil if time.nil?
      if locale == :cn
        short ? WEEKDAYS_CN_SHORT[time.wday] : WEEKDAYS_CN[time.wday]
      else
        short ? WEEKDAYS_EN_SHORT[time.wday] : WEEKDAYS_EN[time.wday]
      end
    end

    def self.month_name(month, locale: :en, short: false)
      return nil if month.nil? || month < 1 || month > 12
      if locale == :cn
        MONTHS_CN[month - 1]
      else
        short ? MONTHS_EN_SHORT[month - 1] : MONTHS_EN[month - 1]
      end
    end

    def self.format_duration(seconds, short: false)
      return nil if seconds.nil?
      
      if short
        parts = []
        parts << "#{seconds / 3600}h" if seconds >= 3600
        parts << "#{(seconds % 3600) / 60}m" if seconds >= 60
        parts << "#{seconds % 60}s" if parts.empty? || seconds % 60 > 0
        parts.join(' ')
      else
        parts = []
        days = seconds / DAY
        hours = (seconds % DAY) / HOUR
        minutes = (seconds % HOUR) / MINUTE
        secs = seconds % MINUTE
        
        parts << "#{days} day#{days == 1 ? '' : 's'}" if days > 0
        parts << "#{hours} hour#{hours == 1 ? '' : 's'}" if hours > 0
        parts << "#{minutes} minute#{minutes == 1 ? '' : 's'}" if minutes > 0
        parts << "#{secs} second#{secs == 1 ? '' : 's'}" if secs > 0 || parts.empty?
        parts.join(', ')
      end
    end

    def self.countdown(target_time, from_time = Time.now)
      return nil if target_time.nil?
      diff = target_time - from_time
      is_future = diff > 0
      diff = diff.abs
      
      {
        days: (diff / DAY).to_i,
        hours: ((diff % DAY) / HOUR).to_i,
        minutes: ((diff % HOUR) / MINUTE).to_i,
        seconds: (diff % MINUTE).to_i,
        total_seconds: diff.to_i,
        is_future: is_future,
        formatted: format_duration(diff.to_i)
      }
    end

    def self.age(birth_time, now = Time.now)
      return nil if birth_time.nil?
      years = now.year - birth_time.year
      years -= 1 if now.month < birth_time.month || (now.month == birth_time.month && now.day < birth_time.day)
      years
    end

    def self.timestamp(time = Time.now)
      return nil if time.nil?
      time.to_i
    end

    def self.timestamp_ms(time = Time.now)
      return nil if time.nil?
      (time.to_f * 1000).to_i
    end

    def self.from_timestamp(timestamp)
      Time.at(timestamp)
    end

    def self.from_timestamp_ms(timestamp_ms)
      Time.at(timestamp_ms / 1000.0)
    end

    def self.now
      Time.now
    end

    def self.today
      Time.now
    end

    def self.utc_now
      Time.now.utc
    end

    def self.to_utc(time)
      return nil if time.nil?
      time.utc
    end

    def self.to_local(time)
      return nil if time.nil?
      time.localtime
    end

    def self.is_valid?(time_string, format = FORMAT_DATETIME)
      return false if time_string.nil? || time_string.empty?
      parse(time_string, format, default: nil) != nil
    end

    def self.clamp(time, min_time, max_time)
      return nil if time.nil?
      return min_time if min_time && time < min_time
      return max_time if max_time && time > max_time
      time
    end

    def self.min(*times)
      times.compact.min
    end

    def self.max(*times)
      times.compact.max
    end

    def self.between?(time, start_time, end_time)
      return false if time.nil? || start_time.nil? || end_time.nil?
      time >= start_time && time <= end_time
    end
  end
end

# Convenience method
module AllToolkit
  def self.time_utils
    TimeUtils
  end
end
