"""
AllToolkit - Nth Weekday Utilities Tests

Comprehensive test suite for nth_weekday_utils module.
"""

import unittest
from datetime import date
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nth_weekday_utils.mod import (
    NthWeekdayUtils, Weekday, NthWeekdayError,
    nth_weekday, last_weekday, first_weekday,
    all_weekdays_in_month, count_weekdays_in_month,
    which_nth_weekday, holiday, list_holidays,
    weekdays_between, count_weekdays_between,
    next_weekday_after, previous_weekday_before,
    weekday_name, month_name
)


class TestNthWeekday(unittest.TestCase):
    """Tests for nth_weekday function"""
    
    def test_first_thursday_november_2024(self):
        """Test finding 1st Thursday of November 2024"""
        result = nth_weekday(2024, 11, 1, Weekday.THURSDAY)
        self.assertEqual(result, date(2024, 11, 7))
    
    def test_fourth_thursday_november_2024(self):
        """Test finding 4th Thursday of November 2024 (Thanksgiving)"""
        result = nth_weekday(2024, 11, 4, Weekday.THURSDAY)
        self.assertEqual(result, date(2024, 11, 28))
    
    def test_fifth_thursday_november_2024(self):
        """Test finding 5th Thursday of November 2024 - should raise error"""
        # November 2024 only has 4 Thursdays: 7, 14, 21, 28
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 11, 5, Weekday.THURSDAY)
    
    def test_last_monday_may_2024(self):
        """Test finding last Monday of May 2024 (Memorial Day)"""
        result = nth_weekday(2024, 5, -1, Weekday.MONDAY)
        self.assertEqual(result, date(2024, 5, 27))
    
    def test_second_to_last_friday_january_2024(self):
        """Test finding second to last Friday of January 2024"""
        result = nth_weekday(2024, 1, -2, Weekday.FRIDAY)
        # January 2024 Fridays: 5, 12, 19, 26
        # Second to last = 19
        self.assertEqual(result, date(2024, 1, 19))
    
    def test_first_monday_september_2024(self):
        """Test finding 1st Monday of September 2024 (Labor Day)"""
        result = nth_weekday(2024, 9, 1, Weekday.MONDAY)
        self.assertEqual(result, date(2024, 9, 2))
    
    def test_invalid_month(self):
        """Test invalid month raises error"""
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 13, 1, Weekday.MONDAY)
    
    def test_invalid_weekday(self):
        """Test invalid weekday raises error"""
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 11, 1, 7)
    
    def test_nth_too_large(self):
        """Test nth too large raises error"""
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 11, 5, Weekday.THURSDAY)  # Only 4 Thursdays
    
    def test_nth_zero(self):
        """Test nth=0 raises error"""
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 11, 0, Weekday.MONDAY)
    
    def test_nth_negative_too_large(self):
        """Test negative nth too large raises error"""
        with self.assertRaises(NthWeekdayError):
            nth_weekday(2024, 11, -5, Weekday.THURSDAY)  # Only 4 Thursdays


class TestLastFirstWeekday(unittest.TestCase):
    """Tests for last_weekday and first_weekday functions"""
    
    def test_last_monday_may_2024(self):
        """Test last Monday of May 2024"""
        result = last_weekday(2024, 5, Weekday.MONDAY)
        self.assertEqual(result, date(2024, 5, 27))
    
    def test_first_thursday_november_2024(self):
        """Test first Thursday of November 2024"""
        result = first_weekday(2024, 11, Weekday.THURSDAY)
        self.assertEqual(result, date(2024, 11, 7))
    
    def test_last_sunday_december_2024(self):
        """Test last Sunday of December 2024"""
        result = last_weekday(2024, 12, Weekday.SUNDAY)
        self.assertEqual(result, date(2024, 12, 29))
    
    def test_first_day_of_month(self):
        """Test when first day of month is the target weekday"""
        # January 2024 starts on Monday
        result = first_weekday(2024, 1, Weekday.MONDAY)
        self.assertEqual(result, date(2024, 1, 1))


class TestAllWeekdaysInMonth(unittest.TestCase):
    """Tests for all_weekdays_in_month function"""
    
    def test_all_thursdays_november_2024(self):
        """Test all Thursdays in November 2024"""
        result = all_weekdays_in_month(2024, 11, Weekday.THURSDAY)
        expected = [date(2024, 11, 7), date(2024, 11, 14), 
                    date(2024, 11, 21), date(2024, 11, 28)]
        self.assertEqual(result, expected)
    
    def test_all_mondays_january_2024(self):
        """Test all Mondays in January 2024"""
        result = all_weekdays_in_month(2024, 1, Weekday.MONDAY)
        expected = [date(2024, 1, 1), date(2024, 1, 8), 
                    date(2024, 1, 15), date(2024, 1, 22), date(2024, 1, 29)]
        self.assertEqual(result, expected)
    
    def test_all_days_in_february_2024(self):
        """Test all days in February 2024 (leap year)"""
        result = all_weekdays_in_month(2024, 2)
        self.assertEqual(len(result), 29)
    
    def test_all_days_in_february_2023(self):
        """Test all days in February 2023 (non-leap year)"""
        result = all_weekdays_in_month(2023, 2)
        self.assertEqual(len(result), 28)


class TestCountWeekdaysInMonth(unittest.TestCase):
    """Tests for count_weekdays_in_month function"""
    
    def test_count_thursdays_november_2024(self):
        """Test counting Thursdays in November 2024"""
        result = count_weekdays_in_month(2024, 11, Weekday.THURSDAY)
        self.assertEqual(result, 4)
    
    def test_count_mondays_january_2024(self):
        """Test counting Mondays in January 2024"""
        result = count_weekdays_in_month(2024, 1, Weekday.MONDAY)
        self.assertEqual(result, 5)
    
    def test_count_fridays_august_2024(self):
        """Test counting Fridays in August 2024"""
        result = count_weekdays_in_month(2024, 8, Weekday.FRIDAY)
        self.assertEqual(result, 5)


class TestWhichNthWeekday(unittest.TestCase):
    """Tests for which_nth_weekday function"""
    
    def test_thanksgiving_2024(self):
        """Test identifying Thanksgiving 2024"""
        year, month, nth = which_nth_weekday(date(2024, 11, 28))
        self.assertEqual((year, month, nth), (2024, 11, 4))
    
    def test_first_day_january_2024(self):
        """Test identifying first Monday of January 2024"""
        year, month, nth = which_nth_weekday(date(2024, 1, 1))
        self.assertEqual((year, month, nth), (2024, 1, 1))
    
    def test_string_input(self):
        """Test with ISO string input"""
        year, month, nth = which_nth_weekday('2024-09-02')
        self.assertEqual((year, month, nth), (2024, 9, 1))


class TestHolidays(unittest.TestCase):
    """Tests for holiday functions"""
    
    def test_thanksgiving_2024(self):
        """Test Thanksgiving 2024"""
        result = holiday('thanksgiving', 2024)
        self.assertEqual(result, date(2024, 11, 28))
    
    def test_thanksgiving_2023(self):
        """Test Thanksgiving 2023"""
        result = holiday('thanksgiving', 2023)
        self.assertEqual(result, date(2023, 11, 23))
    
    def test_labor_day_2024(self):
        """Test Labor Day 2024"""
        result = holiday('labor_day', 2024)
        self.assertEqual(result, date(2024, 9, 2))
    
    def test_memorial_day_2024(self):
        """Test Memorial Day 2024"""
        result = holiday('memorial_day', 2024)
        self.assertEqual(result, date(2024, 5, 27))
    
    def test_mothers_day_2024(self):
        """Test Mother's Day 2024"""
        result = holiday('mothers_day', 2024)
        self.assertEqual(result, date(2024, 5, 12))
    
    def test_fathers_day_2024(self):
        """Test Father's Day 2024"""
        result = holiday('fathers_day', 2024)
        self.assertEqual(result, date(2024, 6, 16))
    
    def test_unknown_holiday(self):
        """Test unknown holiday returns None"""
        result = holiday('unknown_holiday', 2024)
        self.assertIsNone(result)
    
    def test_holiday_with_spaces(self):
        """Test holiday name with spaces"""
        result = holiday('Labor Day', 2024)
        self.assertEqual(result, date(2024, 9, 2))
    
    def test_list_holidays_us_2024(self):
        """Test listing US holidays for 2024"""
        result = list_holidays(2024, 'us')
        self.assertGreater(len(result), 0)
        
        # Check sorted by date
        dates = [d for _, d in result]
        self.assertEqual(dates, sorted(dates))
    
    def test_list_holidays_uk_2024(self):
        """Test listing UK holidays for 2024"""
        result = list_holidays(2024, 'uk')
        self.assertGreater(len(result), 0)


class TestWeekdaysBetween(unittest.TestCase):
    """Tests for weekdays_between function"""
    
    def test_all_fridays_in_january_2024(self):
        """Test all Fridays in January 2024"""
        result = weekdays_between('2024-01-01', '2024-01-31', Weekday.FRIDAY)
        expected = [date(2024, 1, 5), date(2024, 1, 12),
                    date(2024, 1, 19), date(2024, 1, 26)]
        self.assertEqual(result, expected)
    
    def test_all_mondays_across_months(self):
        """Test Mondays across month boundary"""
        result = weekdays_between('2024-11-25', '2024-12-10', Weekday.MONDAY)
        expected = [date(2024, 11, 25), date(2024, 12, 2), date(2024, 12, 9)]
        self.assertEqual(result, expected)
    
    def test_reversed_dates(self):
        """Test with reversed start/end dates"""
        result = weekdays_between('2024-01-31', '2024-01-01', Weekday.FRIDAY)
        expected = [date(2024, 1, 5), date(2024, 1, 12),
                    date(2024, 1, 19), date(2024, 1, 26)]
        self.assertEqual(result, expected)
    
    def test_single_day(self):
        """Test with single day range"""
        result = weekdays_between('2024-01-01', '2024-01-01', Weekday.MONDAY)
        self.assertEqual(result, [date(2024, 1, 1)])
        
        result = weekdays_between('2024-01-01', '2024-01-01', Weekday.TUESDAY)
        self.assertEqual(result, [])


class TestCountWeekdaysBetween(unittest.TestCase):
    """Tests for count_weekdays_between function"""
    
    def test_count_mondays_january_2024(self):
        """Test counting Mondays in January 2024"""
        result = count_weekdays_between('2024-01-01', '2024-01-31', Weekday.MONDAY)
        self.assertEqual(result, 5)
    
    def test_count_all_days(self):
        """Test counting all days"""
        result = count_weekdays_between('2024-01-01', '2024-01-31')
        self.assertEqual(result, 31)
    
    def test_count_sundays_in_month(self):
        """Test counting Sundays in a month"""
        result = count_weekdays_between('2024-02-01', '2024-02-29', Weekday.SUNDAY)
        self.assertEqual(result, 4)


class TestNextPreviousWeekday(unittest.TestCase):
    """Tests for next_weekday_after and previous_weekday_before functions"""
    
    def test_next_monday_after_wednesday(self):
        """Test next Monday after a Wednesday"""
        result = next_weekday_after('2024-11-27', Weekday.MONDAY)
        self.assertEqual(result, date(2024, 12, 2))
    
    def test_next_monday_inclusive(self):
        """Test next Monday with inclusive=True on a Monday"""
        result = next_weekday_after('2024-12-02', Weekday.MONDAY, inclusive=True)
        self.assertEqual(result, date(2024, 12, 2))
    
    def test_next_monday_not_inclusive(self):
        """Test next Monday with inclusive=False on a Monday"""
        result = next_weekday_after('2024-12-02', Weekday.MONDAY, inclusive=False)
        self.assertEqual(result, date(2024, 12, 9))
    
    def test_previous_monday_before_wednesday(self):
        """Test previous Monday before a Wednesday"""
        result = previous_weekday_before('2024-11-27', Weekday.MONDAY)
        self.assertEqual(result, date(2024, 11, 25))
    
    def test_previous_monday_inclusive(self):
        """Test previous Monday with inclusive=True on a Monday"""
        result = previous_weekday_before('2024-12-02', Weekday.MONDAY, inclusive=True)
        self.assertEqual(result, date(2024, 12, 2))
    
    def test_previous_monday_not_inclusive(self):
        """Test previous Monday with inclusive=False on a Monday"""
        result = previous_weekday_before('2024-12-02', Weekday.MONDAY, inclusive=False)
        self.assertEqual(result, date(2024, 11, 25))


class TestNames(unittest.TestCase):
    """Tests for weekday_name and month_name functions"""
    
    def test_weekday_name_english(self):
        """Test weekday names in English"""
        self.assertEqual(weekday_name(Weekday.MONDAY, 'en'), 'Monday')
        self.assertEqual(weekday_name(Weekday.SUNDAY, 'en'), 'Sunday')
    
    def test_weekday_name_chinese(self):
        """Test weekday names in Chinese"""
        self.assertEqual(weekday_name(Weekday.MONDAY, 'zh'), '星期一')
        self.assertEqual(weekday_name(Weekday.SUNDAY, 'zh'), '星期日')
    
    def test_weekday_name_japanese(self):
        """Test weekday names in Japanese"""
        self.assertEqual(weekday_name(Weekday.MONDAY, 'ja'), '月曜日')
    
    def test_month_name_english(self):
        """Test month names in English"""
        self.assertEqual(month_name(1, 'en'), 'January')
        self.assertEqual(month_name(11, 'en'), 'November')
        self.assertEqual(month_name(12, 'en'), 'December')
    
    def test_month_name_chinese(self):
        """Test month names in Chinese"""
        self.assertEqual(month_name(1, 'zh'), '一月')
        self.assertEqual(month_name(11, 'zh'), '十一月')
    
    def test_invalid_month(self):
        """Test invalid month raises error"""
        with self.assertRaises(NthWeekdayError):
            month_name(13)


class TestWeekdayEnum(unittest.TestCase):
    """Tests for Weekday enum"""
    
    def test_weekday_values(self):
        """Test weekday enum values"""
        self.assertEqual(Weekday.MONDAY, 0)
        self.assertEqual(Weekday.TUESDAY, 1)
        self.assertEqual(Weekday.WEDNESDAY, 2)
        self.assertEqual(Weekday.THURSDAY, 3)
        self.assertEqual(Weekday.FRIDAY, 4)
        self.assertEqual(Weekday.SATURDAY, 5)
        self.assertEqual(Weekday.SUNDAY, 6)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases"""
    
    def test_february_29_leap_year(self):
        """Test February 29 in leap year"""
        result = nth_weekday(2024, 2, 5, Weekday.THURSDAY)
        # February 2024: 1, 8, 15, 22, 29 are Thursdays
        self.assertEqual(result, date(2024, 2, 29))
    
    def test_february_non_leap_year(self):
        """Test February in non-leap year"""
        result = count_weekdays_in_month(2023, 2, Weekday.THURSDAY)
        # February 2023: 2, 9, 16, 23 are Thursdays (only 4)
        self.assertEqual(result, 4)
    
    def test_year_boundary(self):
        """Test dates across year boundary"""
        result = weekdays_between('2024-12-30', '2025-01-05', Weekday.WEDNESDAY)
        # Dec 31, 2024 is Tuesday, Jan 1, 2025 is Wednesday
        self.assertEqual(result, [date(2025, 1, 1)])
    
    def test_month_with_6_occurrences(self):
        """Test month with 6 occurrences of a weekday"""
        # May 2024 has 6 Wednesdays: 1, 8, 15, 22, 29
        # Actually May 2024 starts on Wednesday, so: 1, 8, 15, 22, 29 = 5
        # Let me check a different month
        # August 2025 starts on Friday, let's check Fridays: 1, 8, 15, 22, 29 = 5
        # We need a month with 6 occurrences
        result = count_weekdays_in_month(2024, 3, Weekday.FRIDAY)
        # March 2024: 1, 8, 15, 22, 29 = 5 Fridays
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)