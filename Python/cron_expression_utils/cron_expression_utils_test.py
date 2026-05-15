#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Cron Expression Utilities Test Suite
==================================================
Comprehensive tests for cron_expression_utils module.

Run with: python -m pytest cron_expression_utils_test.py -v
Or directly: python cron_expression_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

from datetime import datetime, timedelta
import unittest


class TestCronExpressionParsing(unittest.TestCase):
    """Test cron expression parsing."""
    
    def test_valid_5_field_expression(self):
        """Test valid 5-field cron expressions."""
        valid_expressions = [
            '* * * * *',
            '0 * * * *',
            '0 0 * * *',
            '0 0 1 * *',
            '0 0 1 1 *',
            '*/5 * * * *',
            '0 0 * * 0',
            '0 0 * * 1-5',
            '0 0,12 * * *',
            '0 0 1,15 * *',
        ]
        for expr in valid_expressions:
            with self.subTest(expr=expr):
                cron = CronExpression(expr)
                self.assertEqual(cron.original, expr)
                self.assertFalse(cron.has_seconds)
    
    def test_valid_6_field_expression(self):
        """Test valid 6-field cron expressions (with seconds)."""
        valid_expressions = [
            '0 * * * * *',
            '30 0 * * * *',
            '0 0 0 * * *',
            '*/10 * * * * *',
        ]
        for expr in valid_expressions:
            with self.subTest(expr=expr):
                cron = CronExpression(expr)
                self.assertEqual(cron.original, expr)
                self.assertTrue(cron.has_seconds)
    
    def test_invalid_field_count(self):
        """Test expressions with wrong number of fields."""
        invalid_expressions = [
            '* * * *',          # 4 fields
            '* * * * * * *',    # 7 fields
            '* *',              # 2 fields
            '*',                # 1 field
        ]
        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(CronParseError):
                    CronExpression(expr)
    
    def test_invalid_values(self):
        """Test expressions with invalid values."""
        # These are actual invalid values in their respective field positions
        # Format: minute hour day_of_month month day_of_week
        invalid_expressions = [
            '60 * * * *',       # Minute > 59 (field position 0)
            '* 24 * * *',       # Hour > 23 (field position 1)
            '* * 32 * *',       # Day of month > 31 (field position 2)
            '* * * 13 *',       # Month > 12 (field position 3)
            '* * * * 8',        # Day of week > 6 (field position 4)
        ]
        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(CronParseError):
                    CronExpression(expr)
    
    def test_step_values(self):
        """Test step notation parsing."""
        cron = CronExpression('*/5 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        
        cron = CronExpression('*/10 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 10, 20, 30, 40, 50])
        
        cron = CronExpression('0-30/5 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 5, 10, 15, 20, 25, 30])
    
    def test_range_values(self):
        """Test range notation parsing."""
        cron = CronExpression('1-5 * * * *')
        self.assertEqual(cron.fields['minute'], [1, 2, 3, 4, 5])
        
        cron = CronExpression('0-0 * * * *')
        self.assertEqual(cron.fields['minute'], [0])
    
    def test_list_values(self):
        """Test comma-separated list parsing."""
        cron = CronExpression('1,3,5,7 * * * *')
        self.assertEqual(cron.fields['minute'], [1, 3, 5, 7])
        
        cron = CronExpression('0,30 * * * *')
        self.assertEqual(cron.fields['minute'], [0, 30])
    
    def test_month_names(self):
        """Test month name parsing."""
        cron = CronExpression('0 0 1 jan *')
        self.assertEqual(cron.fields['month'], [1])
        
        cron = CronExpression('0 0 1 jan-mar *')
        self.assertEqual(cron.fields['month'], [1, 2, 3])
        
        cron = CronExpression('0 0 1 jan,apr,jul *')
        self.assertEqual(cron.fields['month'], [1, 4, 7])
    
    def test_day_names(self):
        """Test day of week name parsing."""
        cron = CronExpression('0 0 * * mon')
        self.assertEqual(cron.fields['day_of_week'], [1])
        
        cron = CronExpression('0 0 * * mon-fri')
        self.assertEqual(cron.fields['day_of_week'], [1, 2, 3, 4, 5])
        
        cron = CronExpression('0 0 * * sun,sat')
        self.assertEqual(cron.fields['day_of_week'], [0, 6])
    
    def test_wildcard_values(self):
        """Test wildcard (*) parsing."""
        cron = CronExpression('* * * * *')
        self.assertEqual(cron.fields['minute'], list(range(60)))
        self.assertEqual(cron.fields['hour'], list(range(24)))
        self.assertEqual(cron.fields['day_of_month'], list(range(1, 32)))
        self.assertEqual(cron.fields['month'], list(range(1, 13)))
        self.assertEqual(cron.fields['day_of_week'], list(range(7)))


class TestCronExpressionMethods(unittest.TestCase):
    """Test CronExpression methods."""
    
    def test_get_next_run(self):
        """Test next run calculation."""
        cron = CronExpression('0 * * * *')  # Every hour
        
        # From a specific time
        from_time = datetime(2024, 1, 1, 10, 30, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.hour, 11)
        self.assertEqual(next_run.minute, 0)
        
        # From another time
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.hour, 11)
    
    def test_get_next_run_specific_minute(self):
        """Test next run for specific minute."""
        cron = CronExpression('30 * * * *')  # Every hour at 30
        
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.minute, 30)
        
        from_time = datetime(2024, 1, 1, 10, 30, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.hour, 11)
        self.assertEqual(next_run.minute, 30)
    
    def test_get_next_runs(self):
        """Test getting multiple next runs."""
        cron = CronExpression('0 * * * *')
        
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        runs = cron.get_next_runs(from_time, 5)
        
        self.assertEqual(len(runs), 5)
        self.assertEqual(runs[0].hour, 11)
        self.assertEqual(runs[1].hour, 12)
        self.assertEqual(runs[2].hour, 13)
        self.assertEqual(runs[3].hour, 14)
        self.assertEqual(runs[4].hour, 15)
    
    def test_get_next_run_every_minute(self):
        """Test next run for every minute."""
        cron = CronExpression('* * * * *')
        
        from_time = datetime(2024, 1, 1, 10, 30, 45)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.minute, 31)
    
    def test_get_next_run_daily(self):
        """Test next run for daily schedule."""
        cron = CronExpression('0 8 * * *')  # Daily at 8:00
        
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.day, 2)
        self.assertEqual(next_run.hour, 8)
        
        from_time = datetime(2024, 1, 1, 6, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.day, 1)
        self.assertEqual(next_run.hour, 8)
    
    def test_get_next_run_weekly(self):
        """Test next run for weekly schedule."""
        cron = CronExpression('0 0 * * 0')  # Every Sunday
        
        # Wednesday, Jan 3, 2024
        from_time = datetime(2024, 1, 3, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        # Next Sunday should be Jan 7
        self.assertEqual(next_run.day, 7)
    
    def test_to_dict(self):
        """Test to_dict method."""
        cron = CronExpression('*/5 * * * *')
        result = cron.to_dict()
        
        self.assertEqual(result['original'], '*/5 * * * *')
        self.assertFalse(result['has_seconds'])
        self.assertIn('minute', result['fields'])
    
    def test_str_representation(self):
        """Test string representation."""
        cron = CronExpression('* * * * *')
        self.assertEqual(str(cron), "CronExpression('* * * * *')")


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_parse_cron(self):
        """Test parse_cron function."""
        cron = parse_cron('* * * * *')
        self.assertIsInstance(cron, CronExpression)
        self.assertEqual(cron.original, '* * * * *')
    
    def test_validate_cron(self):
        """Test validate_cron function."""
        is_valid, error = validate_cron('* * * * *')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        is_valid, error = validate_cron('* * * * * * *')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_get_next_run_function(self):
        """Test get_next_run function."""
        from_time = datetime(2024, 1, 1, 10, 30, 0)
        next_run = get_next_run('0 * * * *', from_time)
        self.assertEqual(next_run.hour, 11)
    
    def test_get_next_runs_function(self):
        """Test get_next_runs function."""
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        runs = get_next_runs('0 * * * *', from_time, 3)
        self.assertEqual(len(runs), 3)
    
    def test_cron_to_human_readable(self):
        """Test human-readable conversion."""
        tests = [
            ('* * * * *', 'every minute'),
            ('0 * * * *', 'at minute 0'),
            ('0 0 * * *', 'at minute 0 of hour 0'),
            ('0 0 * * 0', 'on Sunday'),
            ('0 0 * * 1-5', 'on Monday, Tuesday, Wednesday, Thursday, Friday'),
        ]
        
        for expr, expected_phrase in tests:
            with self.subTest(expr=expr):
                result = cron_to_human_readable(expr)
                # Check that key phrase is in result
                self.assertIn(expected_phrase.lower(), result.lower())


class TestPresets(unittest.TestCase):
    """Test cron presets."""
    
    def test_get_preset(self):
        """Test get_preset function."""
        self.assertEqual(get_preset('every_minute'), '* * * * *')
        self.assertEqual(get_preset('every_hour'), '0 * * * *')
        self.assertEqual(get_preset('every_day'), '0 0 * * *')
        self.assertEqual(get_preset('every_week'), '0 0 * * 0')
        self.assertEqual(get_preset('invalid_preset'), None)
    
    def test_list_presets(self):
        """Test list_presets function."""
        presets = list_presets()
        self.assertIsInstance(presets, dict)
        self.assertIn('every_minute', presets)
        self.assertIn('every_hour', presets)
        self.assertIn('every_day', presets)
    
    def test_cron_presets_constant(self):
        """Test CRON_PRESETS constant."""
        self.assertEqual(CRON_PRESETS['every_minute'], '* * * * *')
        self.assertEqual(CRON_PRESETS['every_5_minutes'], '*/5 * * * *')
        self.assertEqual(CRON_PRESETS['every_weekday'], '0 0 * * 1-5')
    
    def test_all_presets_valid(self):
        """Test that all presets are valid cron expressions."""
        for name, expr in CRON_PRESETS.items():
            with self.subTest(name=name):
                is_valid, error = validate_cron(expr)
                self.assertTrue(is_valid, f"Preset '{name}' has invalid expression: {error}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_zero_rate(self):
        """Test zero interest rate scenario."""
        cron = CronExpression('0 0 1 1 *')  # Yearly
        
        from_time = datetime(2024, 6, 15, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        # Should be Jan 1, 2025
        self.assertEqual(next_run.year, 2025)
        self.assertEqual(next_run.month, 1)
        self.assertEqual(next_run.day, 1)
    
    def complex_day_matching(self):
        """Test complex day matching with both DOM and DOW."""
        # Both day of month and day of week specified
        cron = CronExpression('0 0 1 * 0')  # Day 1 or Sunday
        
        # If day 1 is not Sunday, should run on day 1
        # If day 1 is Sunday, should run on day 1
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        # Should be either day 1 of next month or next Sunday
    
    def test_last_day_of_month(self):
        """Test behavior near month boundaries."""
        cron = CronExpression('0 0 31 * *')
        
        from_time = datetime(2024, 2, 15, 10, 0, 0)  # February doesn't have 31 days
        next_run = cron.get_next_run(from_time)
        # Should skip to a month that has 31 days
        self.assertIn(next_run.month, [1, 3, 5, 7, 8, 10, 12])
    
    def test_new_year_boundary(self):
        """Test behavior at year boundaries."""
        cron = CronExpression('0 0 1 1 *')  # Yearly
        
        from_time = datetime(2023, 12, 31, 23, 59, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.year, 2024)
        self.assertEqual(next_run.month, 1)
        self.assertEqual(next_run.day, 1)
    
    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        cron = CronExpression('  *   *   *   *   *  ')
        self.assertEqual(cron.fields['minute'], list(range(60)))


class TestSixFieldFormat(unittest.TestCase):
    """Test 6-field format (with seconds)."""
    
    def test_seconds_field(self):
        """Test seconds field parsing."""
        cron = CronExpression('0 * * * * *')
        self.assertTrue(cron.has_seconds)
        self.assertEqual(cron.fields['second'], [0])
        
        cron = CronExpression('*/10 * * * * *')
        self.assertEqual(cron.fields['second'], [0, 10, 20, 30, 40, 50])
    
    def test_get_next_run_with_seconds(self):
        """Test next run calculation with seconds."""
        cron = CronExpression('30 0 * * * *')  # Every minute at second 30
        
        from_time = datetime(2024, 1, 1, 10, 0, 0)
        next_run = cron.get_next_run(from_time)
        self.assertEqual(next_run.second, 30)


if __name__ == '__main__':
    unittest.main(verbosity=2)