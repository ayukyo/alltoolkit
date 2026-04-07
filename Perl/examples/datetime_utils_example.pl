#!/usr/bin/perl
# DateTimeUtils Example
# Demonstrates usage of DateTimeUtils module

use strict;
use warnings;
use utf8;
use lib '../datetime_utils';
use DateTimeUtils;

print "DateTimeUtils Example\n";
print "=" x 50 . "\n\n";

#==============================================================================
# Example 1: Current Time
#==============================================================================
print "1. Current Time\n";
print "-" x 30 . "\n";
print "Current timestamp: " . now() . "\n";
print "Today at midnight: " . format_datetime(today()) . "\n";
print "Current time (ISO): " . to_iso8601() . "\n\n";

#==============================================================================
# Example 2: Formatting
#==============================================================================
print "2. Formatting Dates\n";
print "-" x 30 . "\n";
my $ts = timelocal(30, 15, 10, 15, 2, 2024);  # 2024-03-15 10:15:30
print "Timestamp: $ts\n";
print "Default format: " . format_datetime($ts) . "\n";
print "Date only: " . format_datetime($ts, '%Y-%m-%d') . "\n";
print "Time only: " . format_datetime($ts, '%H:%M:%S') . "\n";
print "Chinese format: " . format_datetime($ts, '%Y年%m月%d日') . "\n";
print "ISO 8601: " . to_iso8601($ts) . "\n\n";

#==============================================================================
# Example 3: Parsing
#==============================================================================
print "3. Parsing Dates\n";
print "-" x 30 . "\n";
my $parsed1 = parse_auto('2024-03-15');
print "Parsed '2024-03-15': " . format_datetime($parsed1) . "\n";

my $parsed2 = from_iso8601('2024-03-15T10:30:00');
print "Parsed ISO '2024-03-15T10:30:00': " . format_datetime($parsed2) . "\n";

my $parsed3 = parse_auto('2024/03/15');
print "Parsed '2024/03/15': " . format_datetime($parsed3) . "\n";
print "\n";

#==============================================================================
# Example 4: Date Arithmetic
#==============================================================================
print "4. Date Arithmetic\n";
print "-" x 30 . "\n";
my $base = timelocal(0, 0, 0, 15, 2, 2024);  # March 15, 2024
print "Base date: " . format_datetime($base, '%Y-%m-%d') . "\n";
print "Add 5 days: " . format_datetime(add_days($base, 5), '%Y-%m-%d') . "\n";
print "Add 2 months: " . format_datetime(add_months($base, 2), '%Y-%m-%d') . "\n";
print "Add 1 year: " . format_datetime(add_years($base, 1), '%Y-%m-%d') . "\n";
print "Subtract 3 days: " . format_datetime(add_days($base, -3), '%Y-%m-%d') . "\n\n";

#==============================================================================
# Example 5: Time Differences
#==============================================================================
print "5. Time Differences\n";
print "-" x 30 . "\n";
my $start = timelocal(0, 0, 0, 10, 2, 2024);  # March 10
my $end = timelocal(0, 0, 0, 15, 2, 2024);    # March 15
print "Start: " . format_datetime($start, '%Y-%m-%d') . "\n";
print "End: " . format_datetime($end, '%Y-%m-%d') . "\n";
print "Days between: " . days_between($start, $end) . "\n";
print "Hours between: " . hours_between($start, $end) . "\n";
print "Minutes between: " . minutes_between($start, $end) . "\n\n";

#==============================================================================
# Example 6: Date Checks
#==============================================================================
print "6. Date Checks\n";
print "-" x 30 . "\n";
print "Is 2024 a leap year? " . (is_leap_year(2024) ? 'Yes' : 'No') . "\n";
print "Is 2023 a leap year? " . (is_leap_year(2023) ? 'Yes' : 'No') . "\n";

my $weekend = timelocal(0, 0, 0, 16, 2, 2024);  # Saturday
my $weekday = timelocal(0, 0, 0, 18, 2, 2024);  # Monday
print "Is Saturday a weekend? " . (is_weekend($weekend) ? 'Yes' : 'No') . "\n";
print "Is Monday a weekday? " . (is_weekday($weekday) ? 'Yes' : 'No') . "\n\n";

#==============================================================================
# Example 7: Period Boundaries
#==============================================================================
print "7. Period Boundaries\n";
print "-" x 30 . "\n";
my $mid_month = timelocal(30, 15, 14, 15, 2, 2024);  # March 15, 14:15:30
print "Date: " . format_datetime($mid_month) . "\n";
print "Start of day: " . format_datetime(start_of_day($mid_month)) . "\n";
print "End of day: " . format_datetime(end_of_day($mid_month)) . "\n";
print "Start of month: " . format_datetime(start_of_month($mid_month), '%Y-%m-%d') . "\n";
print "End of month: " . format_datetime(end_of_month($mid_month), '%Y-%m-%d') . "\n";
print "Start of year: " . format_datetime(start_of_year($mid_month), '%Y-%m-%d') . "\n";
print "End of year: " . format_datetime(end_of_year($mid_month), '%Y-%m-%d') . "\n\n";

#==============================================================================
# Example 8: Weekday and Month Names
#==============================================================================
print "8. Weekday and Month Names\n";
print "-" x 30 . "\n";
my $sample = timelocal(0, 0, 0, 15, 2, 2024);  # Friday, March 15
print "Weekday (English): " . get_weekday_name($sample, 'en') . "\n";
print "Weekday (Chinese): " . get_weekday_name($sample, 'cn') . "\n";
print "Weekday (Short): " . get_weekday_name($sample, 'short') . "\n";
print "Month (English): " . get_month_name(3, 'en') . "\n";
print "Month (Chinese): " . get_month_name(3, 'cn') . "\n";
print "Month (Short): " . get_month_name(3, 'short') . "\n\n";

#==============================================================================
# Example 9: Age Calculation
#==============================================================================
print "9. Age Calculation\n";
print "-" x 30 . "\n";
my $birth = timelocal(0, 0, 0, 15, 2, 2000);  # Born March 15, 2000
my $current = timelocal(0, 0, 0, 15, 2, 2024);  # March 15, 2024
print "Birth date: " . format_datetime($birth, '%Y-%m-%d') . "\n";
print "Current date: " . format_datetime($current, '%Y-%m-%d') . "\n";
print "Age: " . get_age($birth, $current) . " years\n\n";

#==============================================================================
# Example 10: Relative Time
#==============================================================================
print "10. Relative Time\n";
print "-" x 30 . "\n";
my $now = time();
print "Just now (30 seconds ago): " . relative_time($now - 30) . "\n";
print "5 minutes ago: " . relative_time($now - 300) . "\n";
print "2 hours ago: " . relative_time($now - 7200) . "\n";
print "Yesterday: " . relative_time($now - 90000) . "\n";
print "5 days ago: " . relative_time($now - 432000) . "\n\n";

#==============================================================================
# Example 11: Duration Formatting
#==============================================================================
print "11. Duration Formatting\n";
print "-" x 30 . "\n";
print "45 seconds: " . format_duration(45) . "\n";
print "125 seconds (2m 5s): " . format_duration(125) . "\n";
print "1 hour: " . format_duration(3600) . "\n";
print "1 day, 1 hour, 1 min, 1 sec: " . format_duration(90061) . "\n\n";

#==============================================================================
# Example 12: Countdown
#==============================================================================
print "12. Countdown\n";
print "-" x 30 . "\n";
my $target = time() + 90061;  # ~1 day, 1 hour, 1 minute, 1 second from now
my $cd = countdown($target);
print "Countdown to target:\n";
print "  Days: $cd->{days}\n";
print "  Hours: $cd->{hours}\n";
print "  Minutes: $cd->{minutes}\n";
print "  Seconds: $cd->{seconds}\n";
print "  Total: $cd->{total_seconds} seconds\n\n";

#==============================================================================
# Example 13: Date Range Generation
#==============================================================================
print "13. Date Range Generation\n";
print "-" x 30 . "\n";
my $range_start = timelocal(0, 0, 0, 1, 2, 2024);   # March 1
my $range_end = timelocal(0, 0, 0, 7, 2, 2024);     # March 7
print "Date range from " . format_datetime($range_start, '%Y-%m-%d') . 
      " to " . format_datetime($range_end, '%Y-%m-%d') . ":\n";
my @dates = generate_date_range($range_start, $range_end);
foreach my $date (@dates) {
    print "  " . format_datetime($date, '%Y-%m-%d (%a)') . "\n";
}
print "\n";

#==============================================================================
# Example 14: Validation
#==============================================================================
print "14. Date Validation\n";
print "-" x 30 . "\n";
print "2024-03-15 is valid: " . (validate_date(2024, 3, 15) ? 'Yes' : 'No') . "\n";
print "2024-02-29 is valid (leap year): " . (validate_date(2024, 2, 29) ? 'Yes' : 'No') . "\n";
print "2023-02-29 is valid (not leap year): " . (validate_date(2023, 2, 29) ? 'Yes' : 'No') . "\n";
print "2024-13-01 is valid: " . (validate_date(2024, 13, 1) ? 'Yes' : 'No') . "\n";
print "2024-04-31 is valid: " . (validate_date(2024, 4, 31) ? 'Yes' : 'No') . "\n\n";

print "Examples completed!\n";
