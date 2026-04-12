"""
AllToolkit - Python Cron Utilities Test Suite

Comprehensive test coverage for cron_utils module.
Run with: python cron_utils_test.py -v
"""

import unittest
from datetime import datetime, timedelta
from typing import List, Set
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CronParser, CronMatcher, CronScheduler, CronExpression,
    CronParseError, CronField, CronSchedule, ScheduledTask,
    parse, validate, matches, next_run, next_runs, create_scheduler
)


class TestCronParser(unittest.TestCase):
    """Test cron expression parsing."""
    
    def setUp(self):
        self.parser = CronParser()
    
    def tearDown(self):
        self.parser.clear_cache()
    
    # Basic parsing tests
    def test_parse_every_minute(self):
        """Test '* * * * *' - every minute."""
        expr = self.parser.parse("* * * * *")
        self.assertEqual(expr.minutes, set(range(0, 60)))
        self.assertEqual(expr.hours, set(range(0, 24)))
        self.assertEqual(expr.days_of_month, set(range(1, 32)))
        self.assertEqual(expr.months, set(range(1, 13)))
        self.assertEqual(expr.days_of_week, set(range(0, 7)))
    
    def test_parse_specific_time(self):
        """Test '30 14 * * *' - 14:30 every day."""
        expr = self.parser.parse("30 14 * * *")
        self.assertEqual(expr.minutes, {30})
        self.assertEqual(expr.hours, {14})
    
    def test_parse_list(self):
        """Test '0,15,30,45 * * * *' - every 15 minutes."""
        expr = self.parser.parse("0,15,30,45 * * * *")
        self.assertEqual(expr.minutes, {0, 15, 30, 45})
    
    def test_parse_range(self):
        """Test '0 9-17 * * *' - every hour from 9 to 17."""
        expr = self.parser.parse("0 9-17 * * *")
        self.assertEqual(expr.hours, set(range(9, 18)))
    
    def test_parse_step(self):
        """Test '*/10 * * * *' - every 10 minutes."""
        expr = self.parser.parse("*/10 * * * *")
        self.assertEqual(expr.minutes, {0, 10, 20, 30, 40, 50})
    
    def test_parse_range_with_step(self):
        """Test '0-30/5 * * * *' - every 5 minutes from 0 to 30."""
        expr = self.parser.parse("0-30/5 * * * *")
        self.assertEqual(expr.minutes, {0, 5, 10, 15, 20, 25, 30})
    
    def test_parse_month_names(self):
        """Test month name abbreviations."""
        expr = self.parser.parse("0 0 1 jan,mar,may,jul,sep,nov *")
        self.assertEqual(expr.months, {1, 3, 5, 7, 9, 11})
    
    def test_parse_day_names(self):
        """Test day-of-week name abbreviations."""
        expr = self.parser.parse("0 9 * * mon-fri")
        self.assertEqual(expr.days_of_week, {1, 2, 3, 4, 5})
    
    def test_parse_sunday(self):
        """Test Sunday as 0."""
        expr = self.parser.parse("0 0 * * 0")
        self.assertEqual(expr.days_of_week, {0})
    
    def test_parse_combined(self):
        """Test complex combined expression."""
        expr = self.parser.parse("0,30 8-18/2 1,15 * mon,wed,fri")
        self.assertEqual(expr.minutes, {0, 30})
        self.assertEqual(expr.hours, {8, 10, 12, 14, 16, 18})
        self.assertEqual(expr.days_of_month, {1, 15})
        self.assertEqual(expr.days_of_week, {1, 3, 5})
    
    # Validation tests
    def test_validate_valid(self):
        """Test validation of valid expressions."""
        self.assertTrue(self.parser.validate("* * * * *"))
        self.assertTrue(self.parser.validate("0 0 * * *"))
        self.assertTrue(self.parser.validate("*/5 * * * *"))
    
    def test_validate_invalid_field_count(self):
        """Test validation fails with wrong field count."""
        self.assertFalse(self.parser.validate("* * * *"))
        self.assertFalse(self.parser.validate("* * * * * *"))
    
    def test_validate_invalid_value(self):
        """Test validation fails with out-of-range values."""
        self.assertFalse(self.parser.validate("60 * * * *"))
        self.assertFalse(self.parser.validate("* 24 * * *"))
        self.assertFalse(self.parser.validate("* * 32 * *"))
        self.assertFalse(self.parser.validate("* * * 13 *"))
        self.assertFalse(self.parser.validate("* * * * 7"))
    
    def test_validate_invalid_syntax(self):
        """Test validation fails with invalid syntax."""
        self.assertFalse(self.parser.validate("abc * * * *"))
        self.assertFalse(self.parser.validate("* abc * * *"))
    
    # Error handling tests
    def test_parse_error_wrong_field_count(self):
        """Test CronParseError for wrong field count."""
        with self.assertRaises(CronParseError):
            self.parser.parse("* * * *")
    
    def test_parse_error_out_of_range(self):
        """Test CronParseError for out-of-range values."""
        with self.assertRaises(CronParseError):
            self.parser.parse("60 * * * *")
    
    def test_parse_error_invalid_step(self):
        """Test CronParseError for invalid step values."""
        with self.assertRaises(CronParseError):
            self.parser.parse("*/0 * * * *")
        with self.assertRaises(CronParseError):
            self.parser.parse("*/abc * * * *")
    
    def test_parse_error_invalid_range(self):
        """Test CronParseError for invalid ranges."""
        with self.assertRaises(CronParseError):
            self.parser.parse("30-10 * * * *")
    
    # Cache tests
    def test_cache_hit(self):
        """Test that parsing same expression twice uses cache."""
        expr1 = self.parser.parse("30 14 * * *")
        expr2 = self.parser.parse("30 14 * * *")
        self.assertIs(expr1, expr2)
    
    def test_clear_cache(self):
        """Test cache clearing."""
        self.parser.parse("30 14 * * *")
        self.parser.clear_cache()
        expr = self.parser.parse("30 14 * * *")
        self.assertIsNotNone(expr)


class TestCronMatcher(unittest.TestCase):
    """Test cron datetime matching."""
    
    def setUp(self):
        self.matcher = CronMatcher()
    
    # Matching tests
    def test_matches_every_minute(self):
        """Test matching against '* * * * *'."""
        dt = datetime(2024, 6, 15, 14, 30, 0)
        self.assertTrue(self.matcher.matches("* * * * *", dt))
    
    def test_matches_specific_time(self):
        """Test matching against specific time."""
        dt = datetime(2024, 6, 15, 14, 30, 0)
        self.assertTrue(self.matcher.matches("30 14 * * *", dt))
        self.assertFalse(self.matcher.matches("30 15 * * *", dt))
        self.assertFalse(self.matcher.matches("31 14 * * *", dt))
    
    def test_matches_day_of_week(self):
        """Test matching day of week."""
        # June 17, 2024 is a Monday
        dt = datetime(2024, 6, 17, 12, 0, 0)
        self.assertTrue(self.matcher.matches("0 12 * * mon", dt))
        self.assertFalse(self.matcher.matches("0 12 * * tue", dt))
    
    def test_matches_month(self):
        """Test matching month."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        self.assertTrue(self.matcher.matches("0 12 15 6 *", dt))
        self.assertFalse(self.matcher.matches("0 12 15 7 *", dt))
    
    def test_matches_day_of_month(self):
        """Test matching day of month."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        self.assertTrue(self.matcher.matches("0 12 15 * *", dt))
        self.assertFalse(self.matcher.matches("0 12 16 * *", dt))
    
    # Next run calculation tests
    def test_next_run_basic(self):
        """Test basic next run calculation."""
        # Every minute
        now = datetime(2024, 6, 15, 14, 30, 45)
        next_dt = self.matcher.next_run("* * * * *", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 15, 14, 31, 0))
    
    def test_next_run_specific_time(self):
        """Test next run for specific time."""
        now = datetime(2024, 6, 15, 14, 30, 0)
        next_dt = self.matcher.next_run("30 15 * * *", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 15, 15, 30, 0))
    
    def test_next_run_next_day(self):
        """Test next run on next day."""
        now = datetime(2024, 6, 15, 23, 30, 0)
        next_dt = self.matcher.next_run("0 9 * * *", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 16, 9, 0, 0))
    
    def test_next_run_next_week(self):
        """Test next run on next week."""
        # June 17, 2024 is Monday
        now = datetime(2024, 6, 17, 10, 0, 0)
        # Next Monday at 10am
        next_dt = self.matcher.next_run("0 10 * * mon", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 24, 10, 0, 0))
    
    def test_next_runs_multiple(self):
        """Test getting multiple next runs."""
        now = datetime(2024, 6, 15, 14, 30, 0)
        runs = self.matcher.next_runs("0 * * * *", count=3, after=now)
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], datetime(2024, 6, 15, 15, 0, 0))
        self.assertEqual(runs[1], datetime(2024, 6, 15, 16, 0, 0))
        self.assertEqual(runs[2], datetime(2024, 6, 15, 17, 0, 0))
    
    def test_next_run_with_step(self):
        """Test next run with step values."""
        now = datetime(2024, 6, 15, 14, 32, 0)
        next_dt = self.matcher.next_run("*/10 * * * *", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 15, 14, 40, 0))


class TestCronScheduler(unittest.TestCase):
    """Test cron scheduler functionality."""
    
    def setUp(self):
        self.scheduler = create_scheduler()
        self.executed_tasks: List[str] = []
    
    def tearDown(self):
        self.scheduler.stop()
    
    def callback_factory(self, task_id: str):
        """Create a callback that records execution."""
        def callback():
            self.executed_tasks.append(task_id)
        return callback
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.scheduler.add_task(
            "task1", "Test Task", "* * * * *",
            self.callback_factory("task1")
        )
        self.assertEqual(task.id, "task1")
        self.assertEqual(task.name, "Test Task")
        self.assertTrue(task.is_active)
        self.assertIsNotNone(task.schedule.next_execution)
    
    def test_add_task_duplicate(self):
        """Test adding duplicate task raises error."""
        self.scheduler.add_task("task1", "Test Task", "* * * * *",
                                self.callback_factory("task1"))
        with self.assertRaises(ValueError):
            self.scheduler.add_task("task1", "Duplicate", "* * * * *",
                                    self.callback_factory("task1"))
    
    def test_remove_task(self):
        """Test removing a task."""
        self.scheduler.add_task("task1", "Test Task", "* * * * *",
                                self.callback_factory("task1"))
        self.assertTrue(self.scheduler.remove_task("task1"))
        self.assertFalse(self.scheduler.remove_task("task1"))
        self.assertIsNone(self.scheduler.get_task("task1"))
    
    def test_get_task(self):
        """Test getting a task."""
        self.scheduler.add_task("task1", "Test Task", "* * * * *",
                                self.callback_factory("task1"))
        task = self.scheduler.get_task("task1")
        self.assertIsNotNone(task)
        self.assertEqual(task.name, "Test Task")
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        self.scheduler.add_task("task1", "Task 1", "* * * * *",
                                self.callback_factory("task1"))
        self.scheduler.add_task("task2", "Task 2", "*/5 * * * *",
                                self.callback_factory("task2"))
        tasks = self.scheduler.list_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_enable_disable_task(self):
        """Test enabling and disabling tasks."""
        self.scheduler.add_task("task1", "Test Task", "* * * * *",
                                self.callback_factory("task1"))
        
        self.assertTrue(self.scheduler.disable_task("task1"))
        task = self.scheduler.get_task("task1")
        self.assertFalse(task.is_active)
        
        self.assertTrue(self.scheduler.enable_task("task1"))
        task = self.scheduler.get_task("task1")
        self.assertTrue(task.is_active)
    
    def test_run_due_tasks(self):
        """Test running due tasks manually."""
        # Add a task that should have run in the past
        past_time = datetime.now() - timedelta(minutes=5)
        task = self.scheduler.add_task("task1", "Test Task", "* * * * *",
                                       self.callback_factory("task1"))
        task.schedule.next_execution = past_time
        
        run_ids = self.scheduler.run_due_tasks()
        self.assertIn("task1", run_ids)
        self.assertEqual(len(self.executed_tasks), 1)
        self.assertEqual(task.run_count, 1)
        self.assertIsNotNone(task.schedule.next_execution)
        self.assertGreater(task.schedule.next_execution, past_time)
    
    def test_task_error_handling(self):
        """Test that task errors are captured."""
        def failing_callback():
            raise RuntimeError("Task failed!")
        
        task = self.scheduler.add_task("task1", "Failing Task", "* * * * *",
                                       failing_callback)
        past_time = datetime.now() - timedelta(minutes=5)
        task.schedule.next_execution = past_time
        
        self.scheduler.run_due_tasks()
        self.assertEqual(task.run_count, 1)
        self.assertIn("Task failed!", task.last_error)
    
    def test_scheduler_start_stop(self):
        """Test scheduler start and stop."""
        self.assertFalse(self.scheduler.is_running())
        self.scheduler.start(check_interval=1.0)
        self.assertTrue(self.scheduler.is_running())
        self.scheduler.stop()
        self.assertFalse(self.scheduler.is_running())


class TestConvenienceFunctions(unittest.TestCase):
    """Test module-level convenience functions."""
    
    def test_parse_function(self):
        """Test parse() convenience function."""
        expr = parse("30 14 * * *")
        self.assertEqual(expr.minutes, {30})
        self.assertEqual(expr.hours, {14})
    
    def test_validate_function(self):
        """Test validate() convenience function."""
        self.assertTrue(validate("* * * * *"))
        self.assertFalse(validate("60 * * * *"))
    
    def test_matches_function(self):
        """Test matches() convenience function."""
        dt = datetime(2024, 6, 15, 14, 30, 0)
        self.assertTrue(matches("30 14 * * *", dt))
        self.assertFalse(matches("30 15 * * *", dt))
    
    def test_next_run_function(self):
        """Test next_run() convenience function."""
        now = datetime(2024, 6, 15, 14, 30, 0)
        next_dt = next_run("30 15 * * *", after=now)
        self.assertEqual(next_dt, datetime(2024, 6, 15, 15, 30, 0))
    
    def test_next_runs_function(self):
        """Test next_runs() convenience function."""
        now = datetime(2024, 6, 15, 14, 30, 0)
        runs = next_runs("0 * * * *", count=3, after=now)
        self.assertEqual(len(runs), 3)
    
    def test_create_scheduler_function(self):
        """Test create_scheduler() convenience function."""
        scheduler = create_scheduler()
        self.assertIsInstance(scheduler, CronScheduler)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        self.parser = CronParser()
        self.matcher = CronMatcher()
    
    def test_midnight(self):
        """Test midnight (00:00)."""
        expr = self.parser.parse("0 0 * * *")
        self.assertEqual(expr.hours, {0})
        self.assertEqual(expr.minutes, {0})
    
    def test_sunday_as_0_and_7(self):
        """Test that Sunday is 0 (not 7)."""
        # Sunday should be 0
        expr = self.parser.parse("0 0 * * 0")
        self.assertEqual(expr.days_of_week, {0})
    
    def test_last_minute_of_hour(self):
        """Test last minute of hour (59)."""
        expr = self.parser.parse("59 * * * *")
        self.assertEqual(expr.minutes, {59})
    
    def test_last_hour_of_day(self):
        """Test last hour of day (23)."""
        expr = self.parser.parse("* 23 * * *")
        self.assertEqual(expr.hours, {23})
    
    def test_last_day_of_month(self):
        """Test last day of month (31)."""
        expr = self.parser.parse("* * 31 * *")
        self.assertEqual(expr.days_of_month, {31})
    
    def test_december(self):
        """Test December (month 12)."""
        expr = self.parser.parse("* * * 12 *")
        self.assertEqual(expr.months, {12})
    
    def test_saturday(self):
        """Test Saturday (day 6)."""
        expr = self.parser.parse("* * * * 6")
        self.assertEqual(expr.days_of_week, {6})
    
    def test_full_range_with_step(self):
        """Test full range with step."""
        expr = self.parser.parse("0-59/15 * * * *")
        self.assertEqual(expr.minutes, {0, 15, 30, 45})
    
    def test_single_value_with_step(self):
        """Test single value with step (step is ignored)."""
        expr = self.parser.parse("30/5 * * * *")
        self.assertEqual(expr.minutes, {30})
    
    def test_case_insensitive_names(self):
        """Test that month/day names are case-insensitive."""
        expr1 = self.parser.parse("* * * jan *")
        expr2 = self.parser.parse("* * * JAN *")
        expr3 = self.parser.parse("* * * Jan *")
        self.assertEqual(expr1.months, expr2.months)
        self.assertEqual(expr2.months, expr3.months)
    
    def test_whitespace_normalization(self):
        """Test that extra whitespace is normalized."""
        expr1 = self.parser.parse("* * * * *")
        expr2 = self.parser.parse("  *   *  *   * *  ")
        self.assertEqual(expr1.minutes, expr2.minutes)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_daily_backup_schedule(self):
        """Test a daily backup schedule."""
        # Daily backup at 2 AM
        expr = "0 2 * * *"
        self.assertTrue(validate(expr))
        
        matcher = CronMatcher()
        now = datetime(2024, 6, 15, 14, 30, 0)
        next_dt = matcher.next_run(expr, after=now)
        
        self.assertEqual(next_dt.hour, 2)
        self.assertEqual(next_dt.minute, 0)
        self.assertEqual(next_dt.day, 16)  # Next day
    
    def test_weekday_morning_schedule(self):
        """Test weekday morning schedule."""
        # Every weekday at 9 AM
        expr = "0 9 * * mon-fri"
        self.assertTrue(validate(expr))
        
        matcher = CronMatcher()
        # June 15, 2024 is a Saturday
        now = datetime(2024, 6, 15, 10, 0, 0)
        next_dt = matcher.next_run(expr, after=now)
        
        # Should be next Monday
        self.assertEqual(next_dt.weekday(), 0)  # Monday
        self.assertEqual(next_dt.hour, 9)
        self.assertEqual(next_dt.day, 17)
    
    def test_monthly_report_schedule(self):
        """Test monthly report schedule."""
        # First day of every month at 8 AM
        expr = "0 8 1 * *"
        self.assertTrue(validate(expr))
        
        matcher = CronMatcher()
        now = datetime(2024, 6, 15, 10, 0, 0)
        runs = matcher.next_runs(expr, count=3, after=now)
        
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0].day, 1)
        self.assertEqual(runs[0].month, 7)
        self.assertEqual(runs[1].day, 1)
        self.assertEqual(runs[1].month, 8)
        self.assertEqual(runs[2].day, 1)
        self.assertEqual(runs[2].month, 9)
    
    def test_scheduler_with_multiple_tasks(self):
        """Test scheduler managing multiple tasks."""
        scheduler = create_scheduler()
        results = {"task1": 0, "task2": 0, "task3": 0}
        
        def make_callback(name):
            def callback():
                results[name] += 1
            return callback
        
        # Task 1: Every minute
        scheduler.add_task("task1", "Every Minute", "* * * * *",
                          make_callback("task1"))
        
        # Task 2: Every 5 minutes
        scheduler.add_task("task2", "Every 5 Minutes", "*/5 * * * *",
                          make_callback("task2"))
        
        # Task 3: Every hour
        scheduler.add_task("task3", "Every Hour", "0 * * * *",
                          make_callback("task3"))
        
        # Set all tasks to be due
        past_time = datetime.now() - timedelta(minutes=10)
        for task in scheduler.list_tasks():
            task.schedule.next_execution = past_time
        
        # Run all due tasks
        scheduler.run_due_tasks()
        
        self.assertEqual(results["task1"], 1)
        self.assertEqual(results["task2"], 1)
        self.assertEqual(results["task3"], 1)
        
        scheduler.stop()


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
