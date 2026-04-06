#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative 'mod'

class TimeUtilsTest
  def self.run
    puts "Running TimeUtils tests..."
    puts "=" * 50
    passed = 0
    failed = 0
    
    tests = [
      :test_formatting, :test_parsing, :test_arithmetic, :test_differences,
      :test_relative_time, :test_time_checks, :test_period_boundaries,
      :test_duration, :test_countdown, :test_age, :test_timestamp,
      :test_validation, :test_clamp
    ]
    
    tests.each do |test|
      begin
        send(test)
        passed += 1
      rescue => e
        puts "\n  ERROR in #{test}: #{e.message}"
        failed += 1
      end
    end
    
    puts "=" * 50
    puts "Tests: #{passed} passed, #{failed} failed"
    exit(failed > 0 ? 1 : 0)
  end

  def self.assert_equal(expected, actual, message)
    if expected != actual
      raise "Expected: #{expected.inspect}, Got: #{actual.inspect}"
    end
    puts "  PASS: #{message}"
  end

  def self.test_formatting
    puts "\n[Formatting Tests]"
    time = Time.local(2024, 3, 15, 10, 30, 45)
    
    assert_equal "2024-03-15 10:30:45", AllToolkit::TimeUtils.format(time), "format with default"
    assert_equal "2024-03-15", AllToolkit::TimeUtils.to_short_date(time), "to_short_date"
    assert_equal "10:30", AllToolkit::TimeUtils.to_short_time(time), "to_short_time"
    assert_equal "2024年03月15日", AllToolkit::TimeUtils.to_long_date(time, locale: :cn), "to_long_date cn"
    assert_equal "2024年03月15日 10时30分45秒", AllToolkit::TimeUtils.to_chinese(time), "to_chinese"
    assert_equal "20240315103045", AllToolkit::TimeUtils.to_compact(time), "to_compact"
    assert_equal nil, AllToolkit::TimeUtils.format(nil), "format nil returns nil"
  end

  def self.test_parsing
    puts "\n[Parsing Tests]"
    
    parsed = AllToolkit::TimeUtils.parse("2024-03-15 10:30:00", "%Y-%m-%d %H:%M:%S")
    assert_equal 2024, parsed.year, "parse year"
    assert_equal 3, parsed.month, "parse month"
    assert_equal 15, parsed.day, "parse day"
    
    auto = AllToolkit::TimeUtils.parse_auto("2024-03-15")
    assert_equal 2024, auto.year, "parse_auto date"
    
    assert_equal nil, AllToolkit::TimeUtils.parse("invalid", "%Y-%m-%d", default: nil), "parse invalid returns default"
  end

  def self.test_arithmetic
    puts "\n[Arithmetic Tests]"
    time = Time.local(2024, 3, 15, 10, 0, 0)
    
    result = AllToolkit::TimeUtils.add_seconds(time, 30)
    assert_equal 30, result.sec, "add_seconds"
    
    result = AllToolkit::TimeUtils.add_minutes(time, 5)
    assert_equal 10, result.min, "add_minutes"
    
    result = AllToolkit::TimeUtils.add_hours(time, 3)
    assert_equal 13, result.hour, "add_hours"
    
    result = AllToolkit::TimeUtils.add_days(time, 5)
    assert_equal 20, result.day, "add_days"
    
    result = AllToolkit::TimeUtils.add_months(time, 2)
    assert_equal 5, result.month, "add_months"
    
    result = AllToolkit::TimeUtils.add_years(time, 1)
    assert_equal 2025, result.year, "add_years"
  end

  def self.test_differences
    puts "\n[Difference Tests]"
    time1 = Time.local(2024, 3, 15, 10, 0, 0)
    time2 = Time.local(2024, 3, 15, 8, 0, 0)
    
    assert_equal 7200, AllToolkit::TimeUtils.difference_in_seconds(time1, time2), "difference_in_seconds"
    assert_equal 120, AllToolkit::TimeUtils.difference_in_minutes(time1, time2), "difference_in_minutes"
    assert_equal 2, AllToolkit::TimeUtils.difference_in_hours(time1, time2), "difference_in_hours"
  end

  def self.test_relative_time
    puts "\n[Relative Time Tests]"
    now = Time.now
    
    result = AllToolkit::TimeUtils.relative_time(now - 5, now, locale: :en)
    assert_equal "just now", result, "relative_time just now"
    
    result = AllToolkit::TimeUtils.relative_time(now - 300, now, locale: :en)
    raise "Expected 5 minutes ago, got #{result}" unless result.include?("5 minutes ago")
    puts "  PASS: relative_time 5 minutes ago"
    
    result = AllToolkit::TimeUtils.relative_time(now - 60, now, locale: :cn)
    assert_equal "1分钟前", result, "relative_time cn"
    
    result = AllToolkit::TimeUtils.relative_time(now - 5, now, locale: :cn)
    assert_equal "刚刚", result, "relative_time cn just now"
  end

  def self.test_time_checks
    puts "\n[Time Check Tests]"
    
    raise "is_leap_year? 2024 failed" unless AllToolkit::TimeUtils.is_leap_year?(2024)
    puts "  PASS: is_leap_year? 2024"
    raise "is_leap_year? 2023 should be false" if AllToolkit::TimeUtils.is_leap_year?(2023)
    puts "  PASS: is_leap_year? 2023"
    
    assert_equal 29, AllToolkit::TimeUtils.days_in_month(2024, 2), "days_in_month Feb 2024"
    assert_equal 28, AllToolkit::TimeUtils.days_in_month(2023, 2), "days_in_month Feb 2023"
    assert_equal 31, AllToolkit::TimeUtils.days_in_month(2024, 3), "days_in_month Mar"
    
    weekend = Time.local(2024, 3, 16)
    weekday = Time.local(2024, 3, 15)
    raise "is_weekend? failed" unless AllToolkit::TimeUtils.is_weekend?(weekend)
    puts "  PASS: is_weekend?"
    raise "is_weekday? failed" unless AllToolkit::TimeUtils.is_weekday?(weekday)
    puts "  PASS: is_weekday?"
  end

  def self.test_period_boundaries
    puts "\n[Period Boundary Tests]"
    time = Time.local(2024, 3, 15, 10, 30, 45)
    
    start_of_day = AllToolkit::TimeUtils.start_of_day(time)
    assert_equal 0, start_of_day.hour, "start_of_day hour"
    
    end_of_day = AllToolkit::TimeUtils.end_of_day(time)
    assert_equal 23, end_of_day.hour, "end_of_day hour"
    
    start_of_month = AllToolkit::TimeUtils.start_of_month(time)
    assert_equal 1, start_of_month.day, "start_of_month"
    
    end_of_month = AllToolkit::TimeUtils.end_of_month(time)
    assert_equal 31, end_of_month.day, "end_of_month"
    
    start_of_year = AllToolkit::TimeUtils.start_of_year(time)
    assert_equal 1, start_of_year.month, "start_of_year month"
    
    end_of_year = AllToolkit::TimeUtils.end_of_year(time)
    assert_equal 12, end_of_year.month, "end_of_year month"
  end

  def self.test_duration
    puts "\n[Duration Tests]"
    
    result = AllToolkit::TimeUtils.format_duration(3661)
    raise "format_duration missing hour/minute" unless result.include?("hour") && result.include?("minute")
    puts "  PASS: format_duration"
    
    result = AllToolkit::TimeUtils.format_duration(3661, short: true)
    assert_equal "1h 1m 1s", result, "format_duration short"
  end

  def self.test_countdown
    puts "\n[Countdown Tests]"
    now = Time.now
    future = now + 86400 + 3600 + 60 + 5
    
    countdown = AllToolkit::TimeUtils.countdown(future, now)
    assert_equal 1, countdown[:days], "countdown days"
    assert_equal 1, countdown[:hours], "countdown hours"
    assert_equal 1, countdown[:minutes], "countdown minutes"
    assert_equal 5, countdown[:seconds], "countdown seconds"
    raise "countdown is_future failed" unless countdown[:is_future]
    puts "  PASS: countdown is_future"
  end

  def self.test_age
    puts "\n[Age Tests]"
    birth = Time.local(2000, 1, 1)
    now = Time.local(2024, 6, 15)
    
    age = AllToolkit::TimeUtils.age(birth, now)
    assert_equal 24, age, "age calculation"
  end

  def self.test_timestamp
    puts "\n[Timestamp Tests]"
    time = Time.local(2024, 1, 1, 0, 0, 0)
    
    ts = AllToolkit::TimeUtils.timestamp(time)
    assert_equal time.to_i, ts, "timestamp"
    
    from_ts = AllToolkit::TimeUtils.from_timestamp(ts)
    assert_equal time.to_i, from_ts.to_i, "from_timestamp"
  end

  def self.test_validation
    puts "\n[Validation Tests]"
    
    raise "is_valid? valid failed" unless AllToolkit::TimeUtils.is_valid?("2024-03-15 10:30:00