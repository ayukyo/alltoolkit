"""Tests for cron_checker_utils"""

import pytest
from datetime import datetime, timedelta
from cron_checker_utils import (
    CronChecker,
    validate,
    get_next_run,
    get_last_run,
    get_run_times,
    matches,
    describe
)
import pytest


class TestCronCheckerValidation:
    """Test cron expression validation."""
    
    def test_valid_standard_cron(self):
        """Test valid standard 5-field cron expressions."""
        assert CronChecker('0 0 * * *')
        assert CronChecker('*/5 * * * *')
        assert CronChecker('0 12 * * *')
        assert CronChecker('30 23 1 1 *')
    
    def test_valid_special_expressions(self):
        """Test valid special cron expressions."""
        assert CronChecker('@yearly').expression == '0 0 1 1 *'
        assert CronChecker('@monthly').expression == '0 0 1 * *'
        assert CronChecker('@weekly').expression == '0 0 * * 0'
        assert CronChecker('@daily').expression == '0 0 * * *'
        assert CronChecker('@hourly').expression == '0 * * * *'
        assert CronChecker('@noon').expression == '0 12 * * *'
    
    def test_valid_ranges(self):
        """Test valid range expressions."""
        assert CronChecker('0 9-17 * * *')  # 9am to 5pm
        assert CronChecker('0 0 1-15 * *')   # 1st to 15th of month
    
    def test_valid_steps(self):
        """Test valid step expressions."""
        assert CronChecker('*/15 * * * *')  # every 15 minutes
        assert CronChecker('0 */2 * * *')    # every 2 hours
        assert CronChecker('0 0 */3 * *')   # every 3 days
    
    def test_invalid_field_count(self):
        """Test invalid field count raises error."""
        with pytest.raises(ValueError, match="must have 5 fields"):
            CronChecker('0 0 * *')
        with pytest.raises(ValueError, match="must have 5 fields"):
            CronChecker('0 0 * * * *')
    
    def test_invalid_minute(self):
        """Test invalid minute field raises error."""
        with pytest.raises(ValueError, match="minute"):
            CronChecker('60 0 * * *')
    
    def test_invalid_hour(self):
        """Test invalid hour field raises error."""
        with pytest.raises(ValueError, match="hour"):
            CronChecker('0 24 * * *')
    
    def test_invalid_day(self):
        """Test invalid day of month raises error."""
        with pytest.raises(ValueError, match="day of month"):
            CronChecker('0 0 32 * *')
    
    def test_invalid_range(self):
        """Test invalid range raises error."""
        with pytest.raises(ValueError, match="Invalid range.*start.*end"):
            CronChecker('0 17-9 * * *')


class TestCronCheckerMatches:
    """Test cron expression matching."""
    
    def test_match_daily_noon(self):
        """Test matching daily at noon."""
        checker = CronChecker('0 12 * * *')
        assert checker.matches(datetime(2026, 5, 30, 12, 0))
        assert not checker.matches(datetime(2026, 5, 30, 12, 1))
        assert not checker.matches(datetime(2026, 5, 30, 11, 59))
    
    def test_match_hourly(self):
        """Test matching hourly at minute 0."""
        checker = CronChecker('0 * * * *')
        assert checker.matches(datetime(2026, 5, 30, 12, 0))
        assert checker.matches(datetime(2026, 5, 30, 13, 0))
        assert not checker.matches(datetime(2026, 5, 30, 12, 30))
    
    def test_match_every_5_minutes(self):
        """Test matching every 5 minutes."""
        checker = CronChecker('*/5 * * * *')
        assert checker.matches(datetime(2026, 5, 30, 12, 0))
        assert checker.matches(datetime(2026, 5, 30, 12, 5))
        assert checker.matches(datetime(2026, 5, 30, 12, 10))
        assert not checker.matches(datetime(2026, 5, 30, 12, 3))
    
    def test_match_specific_day(self):
        """Test matching specific day of month."""
        checker = CronChecker('0 0 15 * *')
        assert checker.matches(datetime(2026, 5, 15, 0, 0))
        assert not checker.matches(datetime(2026, 5, 16, 0, 0))
    
    def test_match_weekday(self):
        """Test matching specific day of week."""
        checker = CronChecker('0 0 * * 1')  # Monday
        assert checker.matches(datetime(2026, 6, 1, 0, 0))  # Monday
        assert not checker.matches(datetime(2026, 5, 30, 0, 0))  # Saturday


class TestCronCheckerNextRun:
    """Test getting next run times."""
    
    def test_next_daily_noon(self):
        """Test next run for daily at noon."""
        checker = CronChecker('0 12 * * *')
        after = datetime(2026, 5, 30, 10, 0)
        next_run = checker.get_next_run(after)
        assert next_run == datetime(2026, 5, 30, 12, 0)
    
    def test_next_daily_passed(self):
        """Test next run when daily time has passed."""
        checker = CronChecker('0 12 * * *')
        after = datetime(2026, 5, 30, 14, 0)
        next_run = checker.get_next_run(after)
        assert next_run == datetime(2026, 5, 31, 12, 0)
    
    def test_next_hourly(self):
        """Test next run for hourly schedule."""
        checker = CronChecker('0 * * * *')
        after = datetime(2026, 5, 30, 12, 30)
        next_run = checker.get_next_run(after)
        assert next_run == datetime(2026, 5, 30, 13, 0)
    
    def test_next_every_5_minutes(self):
        """Test next run for every 5 minutes."""
        checker = CronChecker('*/5 * * * *')
        after = datetime(2026, 5, 30, 12, 3)
        next_run = checker.get_next_run(after)
        assert next_run == datetime(2026, 5, 30, 12, 5)
    
    def test_next_special_yearly(self):
        """Test next run for @yearly."""
        checker = CronChecker('@yearly')
        after = datetime(2026, 7, 1)
        next_run = checker.get_next_run(after)
        assert next_run == datetime(2027, 1, 1, 0, 0)


class TestCronCheckerLastRun:
    """Test getting last run times."""
    
    def test_last_daily_noon(self):
        """Test last run for daily at noon."""
        checker = CronChecker('0 12 * * *')
        before = datetime(2026, 5, 30, 14, 0)
        last_run = checker.get_last_run(before)
        assert last_run == datetime(2026, 5, 30, 12, 0)
    
    def test_last_daily_not_yet(self):
        """Test last run when daily time hasn't arrived."""
        checker = CronChecker('0 12 * * *')
        before = datetime(2026, 5, 30, 10, 0)
        last_run = checker.get_last_run(before)
        assert last_run == datetime(2026, 5, 29, 12, 0)


class TestCronCheckerRunTimes:
    """Test getting run times within a range."""
    
    def test_run_times_same_day(self):
        """Test run times on same day."""
        checker = CronChecker('0 12 * * *')
        start = datetime(2026, 5, 30, 10, 0)
        end = datetime(2026, 5, 30, 14, 0)
        times = checker.get_run_times(start, end)
        assert len(times) == 1
        assert times[0] == datetime(2026, 5, 30, 12, 0)
    
    def test_run_times_multiple_days(self):
        """Test run times across multiple days."""
        checker = CronChecker('0 12 * * *')
        start = datetime(2026, 5, 30, 10, 0)
        end = datetime(2026, 6, 1, 14, 0)
        times = checker.get_run_times(start, end)
        assert len(times) == 3
        assert times[0] == datetime(2026, 5, 30, 12, 0)
        assert times[1] == datetime(2026, 5, 31, 12, 0)
        assert times[2] == datetime(2026, 6, 1, 12, 0)


class TestCronCheckerDescribe:
    """Test human-readable descriptions."""
    
    def test_describe_daily_noon(self):
        """Test description for daily at noon."""
        checker = CronChecker('0 12 * * *')
        desc = checker.describe()
        assert '12:00' in desc
        assert 'every day' in desc.lower() or 'day' in desc.lower()
    
    def test_describe_hourly(self):
        """Test description for hourly schedule."""
        checker = CronChecker('0 * * * *')
        desc = checker.describe()
        assert 'hour' in desc.lower()
    
    def test_describe_yearly(self):
        """Test description for @yearly."""
        checker = CronChecker('@yearly')
        desc = checker.describe()
        assert 'January' in desc or '1st' in desc


class TestCronCheckerToDict:
    """Test dictionary conversion."""
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        checker = CronChecker('0 12 * * *')
        d = checker.to_dict()
        assert d['minute'] == '0'
        assert d['hour'] == '12'
        assert d['day'] == '*'
        assert d['month'] == '*'
        assert d['dow'] == '*'
        assert 'description' in d


class TestModuleFunctions:
    """Test module-level convenience functions."""
    
    def test_validate_valid(self):
        """Test validating valid expressions."""
        is_valid, error = validate('0 0 * * *')
        assert is_valid
        assert error is None
    
    def test_validate_invalid(self):
        """Test validating invalid expressions."""
        is_valid, error = validate('0 0 * * * *')
        assert not is_valid
        assert error is not None
    
    def test_get_next_run_function(self):
        """Test get_next_run convenience function."""
        after = datetime(2026, 5, 30, 10, 0)
        result = get_next_run('0 12 * * *', after)
        assert result == datetime(2026, 5, 30, 12, 0)
    
    def test_matches_function(self):
        """Test matches convenience function."""
        dt = datetime(2026, 5, 30, 12, 0)
        assert matches('0 12 * * *', dt)
        assert not matches('0 13 * * *', dt)
    
    def test_describe_function(self):
        """Test describe convenience function."""
        desc = describe('0 12 * * *')
        assert len(desc) > 0


class TestEdgeCases:
    """Test edge cases."""
    
    def test_month_names(self):
        """Test month name parsing."""
        checker = CronChecker('0 0 1 jan *')
        assert checker.matches(datetime(2026, 1, 1, 0, 0))
        assert not checker.matches(datetime(2026, 2, 1, 0, 0))
    
    def test_day_of_week_names(self):
        """Test day of week name parsing."""
        checker = CronChecker('0 0 * * mon')
        assert checker.matches(datetime(2026, 6, 1, 0, 0))  # Monday
    
    def test_complex_expression(self):
        """Test complex cron expression."""
        checker = CronChecker('0 9-17 * * 1-5')  # 9am-5pm weekdays
        assert checker.matches(datetime(2026, 6, 1, 9, 0))  # Monday 9am
        assert checker.matches(datetime(2026, 6, 1, 17, 0))  # Monday 5pm
        assert not checker.matches(datetime(2026, 6, 1, 18, 0))  # Monday 6pm
        assert not checker.matches(datetime(2026, 6, 6, 9, 0))  # Saturday 9am


if __name__ == '__main__':
    pytest.main([__file__, '-v'])