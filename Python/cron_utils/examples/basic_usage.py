"""
AllToolkit - Cron Utils Basic Usage Examples

This file demonstrates basic usage of the cron_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    parse, validate, matches, next_run, next_runs,
    CronParser, CronMatcher, create_scheduler
)
from datetime import datetime


def example_1_basic_parsing():
    """Example 1: Basic cron expression parsing."""
    print("=" * 60)
    print("Example 1: Basic Cron Expression Parsing")
    print("=" * 60)
    
    # Parse a simple expression
    expr = parse("30 14 * * *")
    print(f"Expression: {expr.original}")
    print(f"Minutes: {sorted(expr.minutes)}")
    print(f"Hours: {sorted(expr.hours)}")
    print(f"Days of month: {sorted(expr.days_of_month)}")
    print(f"Months: {sorted(expr.months)}")
    print(f"Days of week: {sorted(expr.days_of_week)}")
    print()


def example_2_validation():
    """Example 2: Validating cron expressions."""
    print("=" * 60)
    print("Example 2: Validating Cron Expressions")
    print("=" * 60)
    
    test_expressions = [
        ("* * * * *", True),           # Every minute
        ("0 0 * * *", True),           # Daily at midnight
        ("*/15 * * * *", True),        # Every 15 minutes
        ("0 9 * * mon-fri", True),     # Weekdays at 9 AM
        ("0 0 1 * *", True),           # First of every month
        ("60 * * * *", False),         # Invalid: minute out of range
        ("* 24 * * *", False),         # Invalid: hour out of range
        ("* * * *", False),            # Invalid: wrong field count
    ]
    
    for expr, expected in test_expressions:
        result = validate(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{expr}' -> {'Valid' if result else 'Invalid'}")
    print()


def example_3_datetime_matching():
    """Example 3: Matching datetime against cron expressions."""
    print("=" * 60)
    print("Example 3: Datetime Matching")
    print("=" * 60)
    
    # Test datetime: June 17, 2024 at 14:30 (Monday)
    test_dt = datetime(2024, 6, 17, 14, 30, 0)
    print(f"Test datetime: {test_dt} (Monday)")
    print()
    
    test_expressions = [
        "* * * * *",           # Every minute - should match
        "30 14 * * *",        # 14:30 daily - should match
        "0 14 * * *",         # 14:00 daily - should NOT match
        "30 14 * * mon",      # 14:30 Monday - should match
        "30 14 * * tue",      # 14:30 Tuesday - should NOT match
        "30 14 17 6 *",       # 14:30 on June 17 - should match
    ]
    
    for expr in test_expressions:
        result = matches(expr, test_dt)
        status = "✓" if result else "✗"
        print(f"{status} '{expr}' -> {'Matches' if result else 'No match'}")
    print()


def example_4_next_execution():
    """Example 4: Calculating next execution times."""
    print("=" * 60)
    print("Example 4: Next Execution Times")
    print("=" * 60)
    
    now = datetime(2024, 6, 15, 14, 30, 0)  # Saturday
    print(f"Current time: {now}")
    print()
    
    # Calculate next run for various expressions
    expressions = [
        ("* * * * *", "Every minute"),
        ("0 * * * *", "Every hour"),
        ("0 9 * * *", "Daily at 9 AM"),
        ("0 9 * * mon-fri", "Weekdays at 9 AM"),
        ("0 0 1 * *", "First of month at midnight"),
        ("0 12 * * sun", "Sunday noon"),
    ]
    
    for expr, description in expressions:
        next_dt = next_run(expr, after=now)
        print(f"{description}:")
        print(f"  Expression: {expr}")
        print(f"  Next run: {next_dt}")
        print()


def example_5_multiple_next_runs():
    """Example 5: Getting multiple upcoming execution times."""
    print("=" * 60)
    print("Example 5: Multiple Upcoming Execution Times")
    print("=" * 60)
    
    now = datetime(2024, 6, 15, 14, 30, 0)
    print(f"Current time: {now}")
    print()
    
    # Get next 5 runs for "every 6 hours"
    expr = "0 */6 * * *"
    print(f"Expression: {expr} (Every 6 hours)")
    runs = next_runs(expr, count=5, after=now)
    
    for i, run in enumerate(runs, 1):
        print(f"  Run {i}: {run}")
    print()


def example_6_custom_parser():
    """Example 6: Using a custom parser instance."""
    print("=" * 60)
    print("Example 6: Custom Parser Instance")
    print("=" * 60)
    
    parser = CronParser()
    
    # Parse with custom parser
    expr = parser.parse("0 9-17 * * mon-fri")
    print(f"Business hours expression: {expr.original}")
    print(f"Hours: {sorted(expr.hours)} (9 AM to 5 PM)")
    print(f"Days: {sorted(expr.days_of_week)} (Monday to Friday)")
    print()
    
    # Validate without raising exceptions
    test_exprs = ["0 9 * * *", "invalid", "* * * *"]
    for test_expr in test_exprs:
        is_valid = parser.validate(test_expr)
        print(f"'{test_expr}' is {'valid' if is_valid else 'invalid'}")
    print()
    
    # Clear cache if needed
    parser.clear_cache()
    print("Cache cleared")
    print()


def example_7_scheduler_basic():
    """Example 7: Basic scheduler usage."""
    print("=" * 60)
    print("Example 7: Basic Scheduler Usage")
    print("=" * 60)
    
    scheduler = create_scheduler()
    
    # Track executions
    executions = []
    
    def my_task():
        executions.append(datetime.now())
        print(f"  Task executed at {executions[-1]}")
    
    # Add a task
    task = scheduler.add_task(
        "my_task",
        "My Scheduled Task",
        "* * * * *",  # Every minute
        my_task
    )
    
    print(f"Task added: {task.name}")
    print(f"  ID: {task.id}")
    print(f"  Expression: {task.cron_expr}")
    print(f"  Next execution: {task.schedule.next_execution}")
    print(f"  Active: {task.is_active}")
    print()
    
    # List all tasks
    print("All tasks:")
    for t in scheduler.list_tasks():
        print(f"  - {t.name} ({t.cron_expr})")
    print()
    
    # Manually run due tasks (for demonstration)
    from datetime import timedelta
    past = datetime.now() - timedelta(minutes=5)
    task.schedule.next_execution = past
    
    print("Running due tasks...")
    run_ids = scheduler.run_due_tasks()
    print(f"Executed tasks: {run_ids}")
    print(f"Task run count: {task.run_count}")
    print()
    
    # Clean up
    scheduler.remove_task("my_task")
    print("Task removed")
    print()


def example_8_scheduler_multiple_tasks():
    """Example 8: Scheduler with multiple tasks."""
    print("=" * 60)
    print("Example 8: Multiple Scheduled Tasks")
    print("=" * 60)
    
    scheduler = create_scheduler()
    
    def make_callback(name):
        def callback():
            print(f"  [{name}] Executed!")
        return callback
    
    # Add multiple tasks
    tasks = [
        ("hourly_backup", "Hourly Backup", "0 * * * *"),
        ("daily_report", "Daily Report", "0 8 * * *"),
        ("weekly_cleanup", "Weekly Cleanup", "0 2 * * sun"),
        ("monthly_audit", "Monthly Audit", "0 3 1 * *"),
    ]
    
    for task_id, name, expr in tasks:
        scheduler.add_task(task_id, name, expr, make_callback(name))
        print(f"Added: {name} ({expr})")
    
    print()
    print(f"Total tasks: {len(scheduler.list_tasks())}")
    print()
    
    # Show next execution times
    print("Next execution times:")
    for task in scheduler.list_tasks():
        print(f"  {task.name}: {task.schedule.next_execution}")
    print()
    
    # Enable/disable tasks
    scheduler.disable_task("weekly_cleanup")
    print("Disabled: Weekly Cleanup")
    
    task = scheduler.get_task("weekly_cleanup")
    print(f"  Is active: {task.is_active}")
    print()
    
    scheduler.stop()


def example_9_common_patterns():
    """Example 9: Common cron expression patterns."""
    print("=" * 60)
    print("Example 9: Common Cron Expression Patterns")
    print("=" * 60)
    
    patterns = {
        "Every minute": "* * * * *",
        "Every 5 minutes": "*/5 * * * *",
        "Every hour": "0 * * * *",
        "Every day at midnight": "0 0 * * *",
        "Every day at 9 AM": "0 9 * * *",
        "Every weekday at 9 AM": "0 9 * * mon-fri",
        "Every weekend at 10 AM": "0 10 * * sat,sun",
        "First of month at noon": "0 12 1 * *",
        "Every Monday at 8 AM": "0 8 * * mon",
        "Every 15 minutes, 9 AM - 5 PM": "*/15 9-17 * * *",
        "Every hour, 8 AM - 8 PM": "0 8-20 * * *",
        "Quarterly (Jan, Apr, Jul, Oct)": "0 0 1 jan,apr,jul,oct *",
    }
    
    for description, expr in patterns.items():
        is_valid = validate(expr)
        next_dt = next_run(expr) if is_valid else None
        print(f"{description}:")
        print(f"  Expression: {expr}")
        print(f"  Valid: {is_valid}")
        if next_dt:
            print(f"  Next run: {next_dt}")
        print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("AllToolkit - Cron Utils Examples")
    print("=" * 60 + "\n")
    
    example_1_basic_parsing()
    example_2_validation()
    example_3_datetime_matching()
    example_4_next_execution()
    example_5_multiple_next_runs()
    example_6_custom_parser()
    example_7_scheduler_basic()
    example_8_scheduler_multiple_tasks()
    example_9_common_patterns()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
