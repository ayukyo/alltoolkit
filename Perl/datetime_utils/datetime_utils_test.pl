#!/usr/bin/perl
# DateTimeUtils Test Suite
# Comprehensive tests for DateTimeUtils module

use strict;
use warnings;
use utf8;
use lib '.';
use DateTimeUtils;

my $TESTS_RUN = 0;
my $TESTS_PASSED = 0;
my $TESTS_FAILED = 0;

sub test {
    my ($name, $condition) = @_;
    $TESTS_RUN++;
    if ($condition) {
        $TESTS_PASSED++;
        print "  ✓ $name\n";
    } else {
        $TESTS_FAILED++;
        print "  ✗ $name\n";
    }
}

sub test_group {
    my ($name) = @_;
    print "\n$name\n";
}

print "DateTimeUtils Test Suite\n";
print "=" x 50 . "\n";

#==============================================================================
# Core Functions Tests
#==============================================================================
test_group("Core Functions");

test("now() returns current timestamp", now() > 0);
test("today() returns midnight timestamp", format_datetime(today(), '%H:%M:%S') eq '00:00:00');
test("timestamp() equals now()", timestamp() == now());

#==============================================================================
# Formatting Tests
#==============================================================================
test_group("Formatting Functions");

my $test_ts = timelocal(30, 15, 10, 15, 2, 2024);  # 2024-03-15 10:15:30
test("format_datetime with default format", format_datetime($test_ts) eq '2024-03-15 10:15:30');
test("format_datetime with custom format", format_datetime($test_ts, '%Y/%m/%d') eq '2024/03/15');
test("to_iso8601 format", to_iso8601($test_ts) eq '2024-03-15T10:15:30');

#==============================================================================
# Parsing Tests
#==============================================================================
test_group("Parsing Functions");

my $parsed = from_iso8601('2024-03-15T10:15:30');
test("from_iso8601 parses correctly", defined $parsed && format_datetime($parsed) eq '2024-03-15 10:15:30');

test("from_iso8601 handles date only", defined from_iso8601('2024-03-15'));
test("from_iso8601 returns undef for invalid", !defined from_iso8601('invalid'));

my $auto_parsed = parse_auto('2024-03-15');
test("parse_auto with ISO date", defined $auto_parsed);

my $auto_parsed2 = parse_auto('2024/03/15');
test("parse_auto with slash format", defined $auto_parsed2);

#==============================================================================
# Arithmetic Tests
#==============================================================================
test_group("Time Arithmetic");

my $base = timelocal(0, 0, 0, 15, 2, 2024);  # 2024-03-15
my $plus_5_days = add_days($base, 5);
test("add_days adds correctly", format_datetime($plus_5_days, '%Y-%m-%d') eq '2024-03-20');

my $minus_3_days = add_days($base, -3);
test("add_days subtracts correctly", format_datetime($minus_3_days, '%Y-%m-%d') eq '2024-03-12');

my $plus_2_hours = add_hours($base, 2);
test("add_hours adds correctly", format_datetime($plus_2_hours, '%H') eq '02');

my $plus_30_min = add_minutes($base, 30);
test("add_minutes adds correctly", format_datetime($plus_30_min, '%M') eq '30');

#==============================================================================
# Difference Tests
#==============================================================================
test_group("Time Differences");

my $start = timelocal(0, 0, 0, 10, 2, 2024);  # March 10
my $end = timelocal(0, 0, 0, 15, 2, 2024);    # March 15
test("days_between calculates correctly", days_between($start, $end) == 5);

my $hour_start = timelocal(0, 0, 10, 15, 2, 2024);  # 10:00
my $hour_end = timelocal(0, 0, 15, 15, 2, 2024);    # 15:00
test("hours_between calculates correctly", hours_between($hour_start, $hour_end) == 5);

#==============================================================================
# Date Checks Tests
#==============================================================================
test_group("Date Checks");

test("is_leap_year for leap year", is_leap_year(2024));
test("is_leap_year for non-leap year", !is_leap_year(2023));
test("is_leap_year for century non-leap", !is_leap_year(1900));
test("is_leap_year for century leap", is_leap_year(2000));

my $weekend_ts = timelocal(0, 0, 0, 16, 2, 2024);  # Saturday March 16, 2024
test("is_weekend detects weekend", is_weekend($weekend_ts));
test("is_weekday detects weekday", !is_weekday($weekend_ts));

my $weekday_ts = timelocal(0, 0, 0, 18, 2, 2024);  # Monday March 18, 2024
test("is_weekday detects weekday", is_weekday($weekday_ts));

#==============================================================================
# Period Boundaries Tests
#==============================================================================
test_group("Period Boundaries");

my $mid_day = timelocal(30, 15, 14, 15, 2, 2024);  # 14:15:30
my $start_day = start_of_day($mid_day);
test("start_of_day returns midnight", format_datetime($start_day, '%H:%M:%S') eq '00:00:00');

my $end_day = end_of_day($mid_day);
test("end_of_day returns 23:59:59", format_datetime($end_day, '%H:%M:%S') eq '23:59:59');

my $start_month = start_of_month($mid_day);
test("start_of_month returns 1st", format_datetime($start_month, '%d') eq '01');

my $end_month = end_of_month($mid_day);
test("end_of_month returns last day", format_datetime($end_month, '%d') eq '31');

# February leap year
my $feb_date = timelocal(0, 0, 0, 15, 1, 2024);  # Feb 15, 2024
my $end_feb = end_of_month($feb_date);
test("end_of_month for Feb leap year", format_datetime($end_feb, '%d') eq '29');

my $start_year = start_of_year($mid_day);
test("start_of_year returns Jan 1", format_datetime($start_year, '%m-%d') eq '01-01');

#==============================================================================
# Utility Functions Tests
#==============================================================================
test_group("Utility Functions");

test("days_in_month for January", days_in_month(2024, 1) == 31);
test("days_in_month for February leap", days_in_month(2024, 2) == 29);
test("days_in_month for February non-leap", days_in_month(2023, 2) == 28);
test("days_in_month for April", days_in_month(2024, 4) == 30);

test("get_weekday_name English", get_weekday_name($weekend_ts, 'en') eq 'Saturday');
test("get_weekday_name Chinese", get_weekday_name($weekend_ts, 'cn') eq '星期六');
test("get_weekday_name short", get_weekday_name($weekend_ts, 'short') eq 'Sat');

test("get_month_name English", get_month_name(3, 'en') eq 'March');
test("get_month_name Chinese", get_month_name(3, 'cn') eq '三月');
test("get_month_name short", get_month_name(3, 'short') eq 'Mar');

# Age calculation
my $birth = timelocal(0, 0, 0, 15, 2, 2000);  # Born March 15, 2000
my $now = timelocal(0, 0, 0, 15, 2, 2024);    # Now March 15, 2024
test("get_age calculates correctly", get_age($birth, $now) == 24);

# Relative time
my $just_now = time() - 30;
test("relative_time for just now", relative_time($just_now) eq '刚刚');

my $five_mins_ago = time() - 300;
test("relative_time for 5 minutes ago", relative_time($five_mins_ago) eq '5分钟前');

# Duration formatting
test("format_duration for seconds", format_duration(45) eq '45秒');
test("format_duration for minutes", format_duration(125) eq '2分钟5秒');
test("format_duration for hours", format_duration(3665) eq '1小时1分钟5秒');
test("format_duration for days", format_duration(90061) eq '1天1小时1分钟1秒');

# Countdown
my $future = time() + 90061;  # ~1 day, 1 hour, 1 minute, 1 second
my $countdown = countdown($future);
test("countdown returns hash", ref($countdown) eq 'HASH');
test("countdown days", $countdown->{days} == 1);
test("countdown hours", $countdown->{hours} == 1);

#==============================================================================
# Validation Tests
##==============================================================================
# Validation Tests
#==============================================================================
test_group("Validation Functions");

test("validate_date for valid date", validate_date(2024, 3, 15));
test("validate_date for invalid month", !validate_date(2024, 13, 15));
test("validate_date for invalid day", !validate_date(2024, 2, 30));
test("validate_date for Feb 29 leap", validate_date(2024, 2, 29));
test("validate_date for Feb 29 non-leap", !validate_date(2023, 2, 29));

#==============================================================================
# Date Range Tests
#==============================================================================
test_group("Date Range");

my $range_start = timelocal(0, 0, 0, 1, 2, 2024);   # March 1
my $range_end = timelocal(0, 0, 0, 5, 2, 2024);     # March 5
my @dates = generate_date_range($range_start, $range_end);
test("generate_date_range returns correct count", scalar(@dates) == 5);
test("generate_date_range first date", format_datetime($dates[0], '%d') eq '01');
test("generate_date_range last date", format_datetime($dates[-1], '%d') eq '05');

#==============================================================================
# Summary
#==============================================================================
print "\n" . "=" x 50 . "\n";
print "Test Summary\n";
print "  Total:  $TESTS_RUN\n";
print "  Passed: $TESTS_PASSED\n";
print "  Failed: $TESTS_FAILED\n";

if ($TESTS_FAILED == 0) {
    print "\nAll tests passed! ✓\n";
    exit 0;
} else {
    print "\nSome tests failed! ✗\n";
    exit 1;
}
