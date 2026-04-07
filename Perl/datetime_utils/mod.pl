#!/usr/bin/perl
# DateTimeUtils - Comprehensive Date and Time Utility Module for Perl
# Zero dependencies, uses only Perl standard library
#
# Provides formatting, parsing, arithmetic, and various date/time operations
#
# Author: AllToolkit
# License: MIT

package DateTimeUtils;

use strict;
use warnings;
use utf8;
use Time::Local;
use POSIX qw(strftime);

our $VERSION = '1.0.0';

# Export all public functions
use Exporter 'import';
our @EXPORT = qw(
    now now_utc today timestamp timestamp_ms
    format_datetime parse_datetime parse_auto
    to_iso8601 from_iso8601
    add_days add_hours add_minutes add_seconds add_months add_years
    days_between hours_between minutes_between seconds_between
    is_today is_yesterday is_tomorrow is_this_week is_this_month is_this_year
    is_weekend is_weekday is_leap_year
    start_of_day end_of_day start_of_week end_of_week
    start_of_month end_of_month start_of_year end_of_year
    get_age get_weekday_name get_month_name days_in_month
    relative_time format_duration countdown
    generate_date_range
);

our @EXPORT_OK = qw(
    validate_date get_timezone_offset
);

#==============================================================================
# Constants
#==============================================================================

use constant {
    SECONDS_PER_MINUTE => 60,
    SECONDS_PER_HOUR   => 3600,
    SECONDS_PER_DAY    => 86400,
    DAYS_PER_WEEK      => 7,
    MONTHS_PER_YEAR    => 12,
};

# Month names
our @MONTH_NAMES_EN = qw(
    January February March April May June
    July August September October November December
);

our @MONTH_NAMES_EN_SHORT = qw(
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
);

our @MONTH_NAMES_CN = qw(
    一月 二月 三月 四月 五月 六月
    七月 八月 九月 十月 十一月 十二月
);

our @WEEKDAY_NAMES_EN = qw(
    Sunday Monday Tuesday Wednesday Thursday Friday Saturday
);

our @WEEKDAY_NAMES_EN_SHORT = qw(
    Sun Mon Tue Wed Thu Fri Sat
);

our @WEEKDAY_NAMES_CN = qw(
    星期日 星期一 星期二 星期三 星期四 星期五 星期六
);

# Days in each month (non-leap year)
our @DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);

#==============================================================================
# Core Functions - Current Time
#==============================================================================

sub now {
    return time();
}

sub now_utc {
    return time();
}

sub today {
    my @lt = localtime(time());
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub timestamp {
    return time();
}

sub timestamp_ms {
    my ($seconds, $microseconds) = Time::HiRes::gettimeofday();
    return $seconds * 1000 + int($microseconds / 1000);
}

#==============================================================================
# Formatting Functions
#==============================================================================

sub format_datetime {
    my ($timestamp, $format) = @_;
    $timestamp = time() unless defined $timestamp;
    $format = '%Y-%m-%d %H:%M:%S' unless defined $format;
    return strftime($format, localtime($timestamp));
}

sub to_iso8601 {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    return strftime('%Y-%m-%dT%H:%M:%S', localtime($timestamp));
}

sub from_iso8601 {
    my ($iso_string) = @_;
    return undef unless defined $iso_string;
    
    if ($iso_string =~ /^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})/) {
        my ($year, $mon, $day, $hour, $min, $sec) = ($1, $2, $3, $4, $5, $6);
        return eval { timelocal($sec, $min, $hour, $day, $mon - 1, $year) };
    }
    elsif ($iso_string =~ /^(\d{4})-(\d{2})-(\d{2})$/) {
        my ($year, $mon, $day) = ($1, $2, $3);
        return eval { timelocal(0, 0, 0, $day, $mon - 1, $year) };
    }
    return undef;
}

sub parse_datetime {
    my ($date_string, $format) = @_;
    return undef unless defined $date_string && defined $format;
    return from_iso8601($date_string) if $format eq '%Y-%m-%d' || $format eq '%Y-%m-%d %H:%M:%S';
    
    my $regex = $format;
    $regex =~ s/%Y/(\\d{4})/g;
    $regex =~ s/%m/(\\d{2})/g;
    $regex =~ s/%d/(\\d{2})/g;
    $regex =~ s/%H/(\\d{2})/g;
    $regex =~ s/%M/(\\d{2})/g;
    $regex =~ s/%S/(\\d{2})/g;
    
    my @parts = ($format =~ /%([YmdHMS])/g);
    
    if ($date_string =~ /^$regex$/) {
        my %values;
        my $i = 1;
        foreach my $part (@parts) {
            $values{$part} = ${$i++};
        }
        
        my $year = $values{'Y'} || 1970;
        my $mon  = $values{'m'} || 1;
        my $day  = $values{'d'} || 1;
        my $hour = $values{'H'} || 0;
        my $min  = $values{'M'} || 0;
        my $sec  = $values{'S'} || 0;
        
        return eval { timelocal($sec, $min, $hour, $day, $mon - 1, $year) };
    }
    return undef;
}

sub parse_auto {
    my ($date_string) = @_;
    return undef unless defined $date_string;
    
    my $result = from_iso8601($date_string);
    return $result if defined $result;
    
    # YYYY/MM/DD
    if ($date_string =~ /^(\d{4})\/(\d{2})\/(\d{2})$/) {
        return eval { timelocal(0, 0, 0, $3, $2 - 1, $1) };
    }
    # DD/MM/YYYY
    if ($date_string =~ /^(\d{2})\/(\d{2})\/(\d{4})$/) {
        return eval { timelocal(0, 0, 0, $1, $2 - 1, $3) };
    }
    # YYYY-MM-DD HH:MM:SS
    if ($date_string =~ /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/) {
        return eval { timelocal($6, $5, $4, $3, $2 - 1, $1) };
    }
    return undef;
}

#==============================================================================
# Time Arithmetic
#==============================================================================

sub add_days {
    my ($timestamp, $days) = @_;
    return $timestamp + ($days * SECONDS_PER_DAY);
}

sub add_hours {
    my ($timestamp, $hours) = @_;
    return $timestamp + ($hours * SECONDS_PER_HOUR);
}

sub add_minutes {
    my ($timestamp, $minutes) = @_;
    return $timestamp + ($minutes * SECONDS_PER_MINUTE);
}

sub add_seconds {
    my ($timestamp, $seconds) = @_;
    return $timestamp + $seconds;
}

sub add_months {
    my ($timestamp, $months) = @_;
    my @lt = localtime($timestamp);
    my $year = $lt[5] + 1900;
    my $mon = $lt[4];
    my $day = $lt[3];
    my $hour = $lt[2];
    my $min = $lt[1];
    my $sec = $lt[0];
    
    $mon += $months;
    $year += int($mon / 12);
    $mon = $mon % 12;
    
    my $days_in_month = days_in_month($year, $mon + 1);
    $day = $days_in_month if $day > $days_in_month;
    
    return eval { timelocal($sec, $min, $hour, $day, $mon, $year) } || $timestamp;
}

sub add_years {
    my ($timestamp, $years) = @_;
    return add_months($timestamp, $years * 12);
}

#==============================================================================
# Time Difference
#==============================================================================

sub days_between {
    my ($start, $end) = @_;
    return int(($end - $start) / SECONDS_PER_DAY);
}

sub hours_between {
    my ($start, $end) = @_;
    return int(($end - $start) / SECONDS_PER_HOUR);
}

sub minutes_between {
    my ($start, $end) = @_;
    return int(($end - $start) / SECONDS_PER_MINUTE);
}

sub seconds_between {
    my ($start, $end) = @_;
    return $end - $start;
}

#==============================================================================
# Date Checks
#==============================================================================

sub is_today {
    my ($timestamp) = @_;
    return format_datetime($timestamp, '%Y%m%d') eq format_datetime(today(), '%Y%m%d');
}

sub is_yesterday {
    my ($timestamp) = @_;
    return format_datetime($timestamp, '%Y%m%d') eq format_datetime(add_days(today(), -1), '%Y%m%d');
}

sub is_tomorrow {
    my ($timestamp) = @_;
    return format_datetime($timestamp, '%Y%m%d') eq format_datetime(add_days(today(), 1), '%Y%m%d');
}

sub is_this_week {
    my ($timestamp) = @_;
    my $now = time();
    my $start = start_of_week($now);
    my $end = end_of_week($now);
    return $timestamp >= $start && $timestamp <= $end;
}

sub is_this_month {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    my @now = localtime(time());
    return ($lt[5] == $now[5]) && ($lt[4] == $now[4]);
}

sub is_this_year {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    my @now = localtime(time());
    return $lt[5] == $now[5];
}

sub is_weekend {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    return $lt[6] == 0 || $lt[6] == 6;
}

sub is_weekday {
    my ($timestamp) = @_;
    return !is_weekend($timestamp);
}

sub is_leap_year {
    my ($year) = @_;
    return 0 unless defined $year;
    return ($year % 4 == 0 && $year % 100 != 0) || ($year % 400 == 0);
}

#==============================================================================
# Period Boundaries
#==============================================================================

sub start_of_day {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_day {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

sub start_of_week {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $days_back = $lt[6];
    $days_back = 6 if $days_back == 0;
    $days_back--;
    return add_days(start_of_day($timestamp), -$days_back);
}

sub end_of_week {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $days_forward = 6 - $lt[6];
    $days_forward = 0 if $lt[6] == 0;
    return add_days(end_of_day($timestamp), $days_forward);
}

sub start_of_month {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 1;
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_month {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $year = $lt[5] + 1900;
    my $mon = $lt[4] + 1;
    $lt[3] = days_in_month($year, $mon);
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

sub start_of_year {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 1;
    $lt[4] = 0;
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_year {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 31;
    $lt[4] = 11;
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

#==============================================================================
# Utility Functions
#==============================================================================

sub days_in_month {
    my ($year, $month) = @_;
    return 0 unless defined $year && defined $month;
    return 29 if $month == 2 && is_leap_year($year);
    return $DAYS_IN_MONTH[$month - 1];
}

sub get_weekday_name {
    my ($timestamp, $locale) = @_;
    $timestamp = time() unless defined $timestamp;
    $locale = 'en' unless defined $locale;
    my @lt = localtime($timestamp);
    my $wday = $lt[6];
    
    if ($locale eq 'cn') {
        return $WEEKDAY_NAMES_CN[$wday];
    } elsif ($locale eq 'short') {
        return $WEEKDAY_NAMES_EN_SHORT[$wday];
    }
    return $WEEKDAY_NAMES_EN[$wday];
}

sub get_month_name {
    my ($month, $locale) = @_;
    return '' unless defined $month && $month >= 1 && $month <= 12;
    $locale = 'en' unless defined $locale;
    
    if ($locale eq 'cn') {
        return $MONTH_NAMES_CN[$month - 1];
    } elsif ($locale eq 'short') {
        return $MONTH_NAMES_EN_SHORT[$month - 1];
    }
    return $MONTH_NAMES_EN[$month - 1];
}

sub get_age {
    my ($birth_timestamp, $current_timestamp) = @_;
    $current_timestamp = time() unless defined $current_timestamp;
    
    my @birth = localtime($birth_timestamp);
    my @current = localtime($current_timestamp);
    
    my $age = ($current[5] + 1900) - ($birth[5] + 1900);
    $age-- if ($current[4] < $birth[4]) || 
              ($current[4] == $birth[4] && $current[3] < $birth[3]);
    
    return $age;
}

sub relative_time {
    my ($timestamp, $now) = @_;
    $now = time() unless defined $now;
    my $diff = $now - $timestamp;
    
    return '刚刚' if $diff < 60;
    return int($diff / 60) . '分钟前' if $diff < 3600;
    return int($diff / 3600) . '小时前' if $diff < 86400;
    return '昨天' if $diff < 172800;
    return int($diff / 86400) . '天前' if $diff < 604800;
    return format_datetime($timestamp, '%Y-%m-%d');
}

sub format_duration {
    my ($seconds) = @_;
    return '0秒' unless defined $seconds && $seconds > 0;
    
    my $days = int($seconds / SECONDS_PER_DAY);
    $seconds %= SECONDS_PER_DAY;
    my $hours = int($seconds / SECONDS_PER_HOUR);
    $seconds %= SECONDS_PER_HOUR;
    my $minutes = int($seconds / SECONDS_PER_MINUTE);
    $seconds %= SECONDS_PER_MINUTE;
    
    my @parts;
    push @parts, $days . '天' if $days > 0;
    push @parts, $hours . '小时' if $hours > 0;
    push @parts, $minutes . '分钟' if $minutes > 0;
    push @parts, $seconds . '秒' if $seconds > 0 || scalar(@parts) == 0;
    
    return join('', @parts);
}

sub countdown {
    my ($target, $now) = @_;
    $now = time() unless defined $now;
    my $diff = $target - $now;
    
    return { days => 0, hours => 0, minutes => 0, seconds => 0, total_seconds => 0 } if $diff <= 0;
    
    my $days = int($diff / SECONDS_PER_DAY);
    $diff %= SECONDS_PER_DAY;
    my $hours = int($diff / SECONDS_PER_HOUR);
    $diff %= SECONDS_PER_HOUR;
    my $minutes = int($diff / SECONDS_PER_MINUTE);
    my $seconds = $diff % SECONDS_PER_MINUTE;
    
    return {
        days => $days,
        hours => $hours,
        minutes => $minutes,
        seconds => $seconds,
        total_seconds => $target - $now
    };
}

sub generate_date_range {
    my ($start, $end, $step_days) = @_;
    $step_days = 1 unless defined $step_days && $step_days > 0;
    
    my @dates;
    my $current = $start;
    while ($current <= $end) {
        push @dates, $current;
        $current = add_days($current, $step_days);
    }
    return @dates;
}

#==============================================================================
# Validation Functions (Export OK)
#==============================================================================

sub validate_date {
    my ($year, $month, $day) = @_;
    return 0 unless defined $year && defined $month && defined $day;
    return 0 if $month < 1 || $month > 12;
    return 0 if $day < 1;
    my $max_days = days_in_month($year, $month);
    return 0 if $day > $max_days;
    return 1;
}

sub get_timezone_offset {
    my @t = localtime(time());
    my @g = gmtime(time());
    my $offset = ($t[2] - $g[2]) * 3600 + ($t[1] - $g[1]) * 60;
    $offset += 86400 if $t[3] != $g[3] && $t[3] - $g[3] != 1;
    $offset -= 86400 if $t[3] != $g[3] && $g[3] - $t[3] != 1;
    return $offset;
}

1;

__END__

=head1 NAME

DateTimeUtils - Comprehensive Date and Time Utility Module for Perl

=head1 SYNOPSIS

    use DateTimeUtils;
    
    # Get current time
    my $now = now();
    my $today = today();
    
    # Formatting
    my $formatted = format_datetime
    return format_datetime($timestamp, '%Y%m%d') eq format_datetime(add_days(today(), 1), '%Y%m%d');
}

sub is_this_week {
    my ($timestamp) = @_;
    my $now = time();
    my $start = start_of_week($now);
    my $end = end_of_week($now);
    return $timestamp >= $start && $timestamp <= $end;
}

sub is_this_month {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    my @now = localtime(time());
    return ($lt[5] == $now[5]) && ($lt[4] == $now[4]);
}

sub is_this_year {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    my @now = localtime(time());
    return $lt[5] == $now[5];
}

sub is_weekend {
    my ($timestamp) = @_;
    my @lt = localtime($timestamp);
    return $lt[6] == 0 || $lt[6] == 6;
}

sub is_weekday {
    my ($timestamp) = @_;
    return !is_weekend($timestamp);
}

sub is_leap_year {
    my ($year) = @_;
    return 0 unless defined $year;
    return ($year % 4 == 0 && $year % 100 != 0) || ($year % 400 == 0);
}

sub start_of_day {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_day {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

sub start_of_week {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $days_back = $lt[6];
    $days_back = 6 if $days_back == 0;
    $days_back--;
    return add_days(start_of_day($timestamp), -$days_back);
}

sub end_of_week {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $days_forward = 6 - $lt[6];
    $days_forward = 0 if $lt[6] == 0;
    return add_days(end_of_day($timestamp), $days_forward);
}

sub start_of_month {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 1;
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_month {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    my $year = $lt[5] + 1900;
    my $mon = $lt[4] + 1;
    $lt[3] = days_in_month($year, $mon);
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

sub start_of_year {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 1;
    $lt[4] = 0;
    $lt[0] = $lt[1] = $lt[2] = 0;
    return timelocal(@lt);
}

sub end_of_year {
    my ($timestamp) = @_;
    $timestamp = time() unless defined $timestamp;
    my @lt = localtime($timestamp);
    $lt[3] = 31;
    $lt[4] = 11;
    $lt[0] = 59; $lt[1] = 59; $lt[2] = 23;
    return timelocal(@lt);
}

sub days_in_month {
    my ($year, $month) = @_;
    return 0 unless defined $year && defined $month;
    return 29 if $month == 2 && is_leap_year($year);
    return $DAYS_IN_MONTH[$month - 1];
}

sub get_weekday_name {
    my ($timestamp, $locale) = @_;
    $timestamp = time() unless defined $timestamp;
    $locale = 'en' unless defined $locale;
    my @lt = localtime($timestamp);
    my $wday = $lt[6];
    
    if ($locale eq 'cn') {
        return $WEEKDAY_NAMES_CN[$wday];
    } elsif ($locale eq 'short') {
        return $WEEKDAY_NAMES_EN_SHORT[$wday];
    }
    return $WEEKDAY_NAMES_EN[$wday];
}

sub get_month_name {
    my ($month, $locale) = @_;
    return '' unless defined $month && $month >= 1 && $month <= 12;
    $locale = 'en' unless defined $locale;
    
    if ($locale eq 'cn') {
        return $MONTH_NAMES_CN[$month - 1];
    } elsif ($locale eq 'short') {
        return $MONTH_NAMES_EN_SHORT[$month - 1];
    }
    return $MONTH_NAMES_EN[$month - 1];
}

sub get_age {
    my ($birth_timestamp, $current_timestamp) = @_;
    $current_timestamp = time() unless defined $current_timestamp;
    
    my @birth = localtime($birth_timestamp);
    my @current = localtime($current_timestamp);
    
    my $age = ($current[5] + 1900) - ($birth[5] + 1900);
    $age-- if ($current[4] < $birth[4]) || 
              ($current[4] == $birth[4] && $current[3] < $birth[3]);
    
    return $age;
}

sub relative_time {
    my ($timestamp, $now) = @_;
    $now = time() unless defined $now;
    my $diff = $now - $timestamp;
    
    return '刚刚' if $diff < 60;
    return int($diff / 60) . '分钟前' if $diff < 3600;
    return int($diff / 3600) . '小时前' if $diff < 86400;
    return '昨天' if $diff < 172800;
    return int($diff / 86400) . '天前' if $diff < 604800;
    return format_datetime($timestamp, '%Y-%m-%d');
}

sub format_duration {
    my ($seconds) = @_;
    return '0秒' unless defined $seconds && $seconds > 0;
    
    my $days = int($seconds / SECONDS_PER_DAY);
    $seconds %= SECONDS_PER_DAY;
    my $hours = int($seconds / SECONDS_PER_HOUR);
    $seconds %= SECONDS_PER_HOUR;
    my $minutes = int($seconds / SECONDS_PER_MINUTE);
    $seconds %= SECONDS_PER_MINUTE;
    
    my @parts;
    push @parts, $days . '天' if $days > 0;
    push @parts, $hours . '小时' if $hours > 0;
    push @parts, $minutes . '分钟' if $minutes > 0;
    push @parts, $seconds . '秒' if $seconds > 0 || scalar(@parts) == 0;
    
    return join('', @parts);
}

sub countdown {
    my ($target, $now) = @_;
    $now = time() unless defined $now;
    my $diff = $target - $now;
    
    return { days => 0, hours => 0, minutes => 0, seconds => 0, total_seconds => 0 } if $diff <= 0;
    
    my $days = int($diff / SECONDS_PER_DAY);
    $diff %= SECONDS_PER_DAY;
    my $hours = int($diff / SECONDS_PER_HOUR);
    $diff %= SECONDS_PER_HOUR;
    my $minutes = int($diff / SECONDS_PER_MINUTE);
    my $seconds = $diff % SECONDS_PER_MINUTE;
    
    return {
        days => $days,
        hours => $hours,
        minutes => $minutes,
        seconds => $seconds,
        total_seconds => $target - $now
    };
}

sub generate_date_range {
    my ($start, $end, $step_days) = @_;
    $step_days = 1 unless defined $step_days && $step_days > 0;
    
    my @dates;
    my $current = $start;
    while ($current <= $end) {
        push @dates, $current;
        $current = add_days($current, $step_days);
    }
    return @dates;
}

sub validate_date {
    my ($year, $month, $day) = @_;
    return 0 unless defined $year && defined $month && defined $day;
    return 0 if $month < 1 || $month > 12;
    return 0 if $day < 1;
    my $max_days = days_in_month($year, $month);
    return 0 if $day > $max_days;
    return 1;
}

sub get_timezone_offset {
    my @t = localtime(time());
    my @g = gmtime(time());
    my $offset = ($t[2] - $g[2]) * 3600 + ($t[1] - $g[1]) * 60;
    $offset += 86400 if $t[3] != $g[3] && $t[3] - $g[3] != 1;
    $offset -= 86400 if $t[3] != $g[3] && $g[3] - $t[3] != 1;
    return $offset;
}

1;
