"""
Tests for Cron Expression Utilities

Comprehensive tests for cron expression parsing, validation, and calculation.
"""

import unittest
from datetime import datetime
from mod import (
    CronExpression,
    CronParseError,
    parse_cron,
    validate_cron,
    get_next_run,
    get_next_runs,
    cron_to_human_readable,
    get_preset,
    list_presets,
    CRON_PRESETS,
)


class TestCronExpressionParsing(unittest.TestCase):
    """Test cron expression parsing."""
    
    def test_parse_5_field_expression(self):
        """Test parsing standard 5-field expression."""
        cron = CronExpression('* * * * *')
        self.assertFalse(cron.has_seconds)
        self.assertEqual(cron.fields['minute'], list(range(60)))
        self.assertEqual(cron.fields['hour'], list(range(24)))
        self.assertEqual(cron.fields['day_of_month'], list(range(1, 32)))
        self.assertEqual(cron.fields['month'], list(range(1, 13)))
        self.assertEqual(cron.fields['day_of_week'], list(range(7)))
    
    def test_parse_6_field_expression(self):
        """Test parsing 6-field expression with seconds."""
        cron = CronExpression('0 * * * * *')
        self.assertTrue(cron.has_seconds)
        self.assertEqual(cron.fields['second'], [0])
    
    def test_parse_specific_values(self):
        """Test parsing specific values."""
        cron = CronExpression('30 14 15 6 1')
        self.assertEqual(cron.fields['minute'], [30])
        self.assertEqual(cron.fields['hour'], [14])
        self.assertEqual(cron.fields['day_of_month'], [15])
        self.assertEqual(cron.fields['month'], [6])
        self.assertEqual(cron.fields['day_of_week'], [1])
    
    def test_parse_comma_separated(self):
        """Test parsing comma-separated values."""
        cron = CronExpression('0,15,30,45 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 15, 30, 45])
    
    def test_parse_range(self):
        """Test parsing range values."""
        cron = CronExpression('0-30 * * * *')
        self.assertEqual(cron.fields['minute'], list(range(31)))
    
    def test_parse_step(self):
        """Test parsing step values."""
        cron = CronExpression('*/15 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 15, 30, 45])
    
    def test_parse_range_with_step(self):
        """Test parsing range with step."""
        cron = CronExpression('0-30/10 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 10, 20, 30])
    
    def test_parse_month_names(self):
        """Test parsing month names."""
        cron = CronExpression('* * * jan,feb,mar *')
        self.assertEqual(cron.fields['month'], [1, 2, 3])
    
    def test_parse_day_of_week_names(self):
        """Test parsing day of week names."""
        cron = CronExpression('* * * * mon,wed,fri')
        self.assertEqual(cron.fields['day_of_week'], [1, 3, 5])
    
    def test_parse_invalid_fields(self):
        """Test parsing invalid number of fields."""
        with self.assertRaises(CronParseError):
            CronExpression('* * * *')
        with self.assertRaises(CronParseError):
            CronExpression('* * * * * * *')
    
    def test_parse_invalid_value(self):
        """Test parsing invalid values."""
        with self.assertRaises(CronParseError):
            CronExpression('60 * * * *')  # minute > 59
        with self.assertRaises(CronParseError):
            CronExpression('* 24 * * *')  # hour > 23
        with self.assertRaises(CronParseError):
            CronExpression('* * 0 * *')  # day < 1


class TestCronValidation(unittest.TestCase):
    """Test cron expression validation."""
    
    def test_validate_valid_expressions(self):
        """Test validation of valid expressions."""
        valid_expressions = [
            '* * * * *',
            '0 * * * *',
            '*/5 * * * *',
            '0 0 * * *',
            '0 0 1 * *',
            '0 0 1 1 *',
            '0 0 * * 0',
            '30 14 15 6 1',
            '0,15,30,45 9-17 * * 1-5',
        ]
        for expr in valid_expressions:
            is_valid, error = validate_cron(expr)
            self.assertTrue(is_valid, f"Expected '{expr}' to be valid, got: {error}")
    
    def test_validate_invalid_expressions(self):
        """Test validation of invalid expressions."""
        invalid_cases = [
            ('* * * *', 'Expected 4 fields to fail'),
            ('* * * * * * *', 'Expected 7 fields to fail'),
            ('60 * * * *', 'Expected minute > 59 to fail'),
            ('* 24 * * *', 'Expected hour > 23 to fail'),
            ('* * 32 * *', 'Expected day > 31 to fail'),
            ('* * * 13 *', 'Expected month > 12 to fail'),
            ('* * * * 7', 'Expected dow > 6 to fail'),
        ]
        for expr, reason in invalid_cases:
            is_valid, error = validate_cron(expr)
            self.assertFalse(is_valid, f"Expected '{expr}' to fail: {reason}")


class TestNextRunCalculation(unittest.TestCase):
    """Test next run time calculation."""
    
    def test_every_minute(self):
        """Test next run for every minute."""
        cron = CronExpression('* * * * *')
        from_time = datetime(2025, 5, 15, 10, 30, 45)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run, datetime(2025, 5, 15, 10, 31, 0))
    
    def test_every_hour(self):
        """Test next run for every hour."""
        cron = CronExpression('0 * * * *')
        from_time = datetime(2025, 5, 15, 10, 30, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run, datetime(2025, 5, 15, 11, 0, 0))
    
    def test_specific_time(self):
        """Test next run for specific time."""
        cron = CronExpression('30 14 * * *')
        from_time = datetime(2025, 5, 15, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run, datetime(2025, 5, 15, 14, 30, 0))
    
    def test_specific_day_of_week(self):
        """Test next run for specific day of week."""
        cron = CronExpression('0 0 * * 1')  # Every Monday at midnight
        from_time = datetime(2025, 5, 15, 10, 0, 0)  # Thursday
        next_run = cron.get_next_run(from_time)
        # Should be next Monday (May 19)
        self.assertEqual(next_run.weekday(), 0)  # Monday
        self.assertEqual(next_run.day, 19)
    
    def test_specific_day_of_month(self):
        """Test next run for specific day of month."""
        cron = CronExpression('0 0 1 * *')  # Every 1st of month at midnight
        from_time = datetime(2025, 5, 15, 0, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.day, 1)
        self.assertEqual(next_run.month, 6)  # June 1st
    
    def test_specific_month(self):
        """Test next run for specific month."""
        cron = CronExpression('0 0 1 1 *')  # Every January 1st at midnight
        from_time = datetime(2025, 5, 15, 0, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.month, 1)
        self.assertEqual(next_run.day, 1)
        self.assertEqual(next_run.year, 2026)
    
    def test_with_seconds(self):
        """Test next run with 6-field expression."""
        cron = CronExpression('30 * * * * *')  # Every minute at 30 seconds
        from_time = datetime(2025, 5, 15, 10, 30, 15)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run, datetime(2025, 5, 15, 10, 30, 30))
    
    def test_get_next_runs_multiple(self):
        """Test getting multiple next runs."""
        cron = CronExpression('0 */2 * * *')  # Every 2 hours
        from_time = datetime(2025, 5, 15, 10, 0, 0)
        runs = cron.get_next_runs(from_time, 3)
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], datetime(2025, 5, 15, 12, 0, 0))
        self.assertEqual(runs[1], datetime(2025, 5, 15, 14, 0, 0))
        self.assertEqual(runs[2], datetime(2025, 5, 15, 16, 0, 0))


class TestHumanReadable(unittest.TestCase):
    """Test human-readable descriptions."""
    
    def test_every_minute(self):
        """Test description for every minute."""
        desc = cron_to_human_readable('* * * * *')
        self.assertIn('every minute', desc.lower())
    
    def test_every_hour(self):
        """Test description for every hour."""
        desc = cron_to_human_readable('0 * * * *')
        self.assertIn('minute 0', desc.lower())
    
    def test_specific_time(self):
        """Test description for specific time."""
        desc = cron_to_human_readable('30 14 * * *')
        self.assertIn('minute 30', desc.lower())
        self.assertIn('hour 14', desc.lower())
    
    def test_every_weekday(self):
        """Test description for weekdays."""
        desc = cron_to_human_readable('0 0 * * 1-5')
        self.assertIn('monday', desc.lower())


class TestPresets(unittest.TestCase):
    """Test cron presets."""
    
    def test_get_preset(self):
        """Test getting preset by name."""
        self.assertEqual(get_preset('every_minute'), '* * * * *')
        self.assertEqual(get_preset('every_hour'), '0 * * * *')
        self.assertEqual(get_preset('every_day'), '0 0 * * *')
    
    def test_get_preset_case_insensitive(self):
        """Test preset names are case insensitive."""
        self.assertEqual(get_preset('EVERY_MINUTE'), '* * * * *')
        self.assertEqual(get_preset('Every_Hour'), '0 * * * *')
    
    def test_get_invalid_preset(self):
        """Test getting invalid preset."""
        self.assertIsNone(get_preset('invalid_preset'))
    
    def test_list_presets(self):
        """Test listing all presets."""
        presets = list_presets()
        self.assertIn('every_minute', presets)
        self.assertIn('every_hour', presets)
        self.assertIn('every_day', presets)
        self.assertIn('every_week', presets)
        self.assertIn('every_month', presets)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_leap_year(self):
        """Test handling leap year."""
        cron = CronExpression('0 0 29 2 *')  # Feb 29
        from_time = datetime(2025, 5, 15, 0, 0, 0)
        next_run = cron.get_next_run(from_time)
        # Next leap year is 2028
        self.assertEqual(next_run.year, 2028)
        self.assertEqual(next_run.month, 2)
        self.assertEqual(next_run.day, 29)
    
    def test_month_end(self):
        """Test handling month end."""
        cron = CronExpression('0 0 31 * *')  # Every 31st
        from_time = datetime(2025, 2, 15, 0, 0, 0)
        next_run = cron.get_next_run(from_time)
        # Next month with 31 days after Feb is March
        self.assertEqual(next_run.month, 3)
        self.assertEqual(next_run.day, 31)
    
    def test_year_boundary(self):
        """Test handling year boundary."""
        cron = CronExpression('0 0 1 1 *')  # Jan 1
        from_time = datetime(2025, 12, 31, 23, 59, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.year, 2026)
        self.assertEqual(next_run.month, 1)
        self.assertEqual(next_run.day, 1)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_parse_cron_function(self):
        """Test parse_cron convenience function."""
        cron = parse_cron('* * * * *')
        self.assertIsInstance(cron, CronExpression)
    
    def test_get_next_run_function(self):
        """Test get_next_run convenience function."""
        from_time = datetime(2025, 5, 15, 10, 30, 45)
        next_run = get_next_run('* * * * *', from_time)
        self.assertEqual(next_run, datetime(2025, 5, 15, 10, 31, 0))
    
    def test_get_next_runs_function(self):
        """Test get_next_runs convenience function."""
        from_time = datetime(2025, 5, 15, 10, 0, 0)
        runs = get_next_runs('0 * * * *', from_time, 3)
        self.assertEqual(len(runs), 3)


if __name__ == '__main__':
    unittest.main()