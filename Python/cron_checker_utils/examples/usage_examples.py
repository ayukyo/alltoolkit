"""
Usage examples for cron_checker_utils
"""

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


def example_basic():
    """Basic usage examples."""
    print("=== Basic Usage ===")
    
    # Create a checker for a daily at noon cron
    checker = CronChecker('0 12 * * *')
    
    now = datetime.now()
    print(f"Current time: {now}")
    
    # Check if it matches now
    print(f"Matches now: {checker.matches(now)}")
    
    # Get next run
    next_run = checker.get_next_run()
    print(f"Next run: {next_run}")
    
    # Get human-readable description
    print(f"Description: {checker.describe()}")


def example_special_expressions():
    """Using special cron expressions."""
    print("\n=== Special Expressions ===")
    
    specials = ['@yearly', '@monthly', '@weekly', '@daily', '@hourly', '@noon']
    
    for expr in specials:
        checker = CronChecker(expr)
        print(f"{expr} -> {checker.expression} -> {checker.describe()}")


def example_validation():
    """Validating cron expressions."""
    print("\n=== Validation ===")
    
    expressions = [
        '0 0 * * *',
        '*/15 * * * *',
        '0 9-17 * * 1-5',
        'invalid',
        '0 0 * * * *',
    ]
    
    for expr in expressions:
        is_valid, error = validate(expr)
        if is_valid:
            print(f"✓ '{expr}' is valid")
        else:
            print(f"✗ '{expr}' is invalid: {error}")


def example_next_run():
    """Getting next run times."""
    print("\n=== Next Run Times ===")
    
    expressions = [
        '0 12 * * *',      # Daily at noon
        '*/30 * * * *',    # Every 30 minutes
        '0 9,17 * * *',    # At 9am and 5pm daily
    ]
    
    after = datetime(2026, 5, 30, 10, 0)
    print(f"After: {after}")
    
    for expr in expressions:
        checker = CronChecker(expr)
        next_run = checker.get_next_run(after)
        print(f"{expr}: next run = {next_run}")


def example_last_run():
    """Getting last run times."""
    print("\n=== Last Run Times ===")
    
    expressions = ['0 12 * * *', '0 9 * * *']
    
    before = datetime(2026, 5, 30, 14, 0)
    print(f"Before: {before}")
    
    for expr in expressions:
        checker = CronChecker(expr)
        last_run = checker.get_last_run(before)
        print(f"{expr}: last run = {last_run}")


def example_run_times():
    """Getting run times within a range."""
    print("\n=== Run Times in Range ===")
    
    checker = CronChecker('0 12 * * *')
    start = datetime(2026, 5, 30, 0, 0)
    end = datetime(2026, 6, 2, 23, 59)
    
    print(f"Expression: {checker.expression}")
    print(f"Range: {start.date()} to {end.date()}")
    print("Run times:")
    
    for run_time in checker.get_run_times(start, end):
        print(f"  - {run_time}")


def example_matches():
    """Checking if cron matches specific time."""
    print("\n=== Matches ===")
    
    expressions = [
        '0 12 * * *',      # Daily at noon
        '*/5 * * * *',     # Every 5 minutes
        '0 0 * * 0',       # Every Sunday at midnight
    ]
    
    test_times = [
        datetime(2026, 5, 30, 12, 0),   # Saturday noon
        datetime(2026, 5, 30, 12, 5),   # Saturday 12:05
        datetime(2026, 6, 1, 0, 0),     # Monday midnight
    ]
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        for dt in test_times:
            result = matches(expr, dt)
            symbol = "✓" if result else "✗"
            print(f"  {symbol} {dt.strftime('%Y-%m-%d %H:%M')}")


def example_to_dict():
    """Converting to dictionary."""
    print("\n=== To Dictionary ===")
    
    checker = CronChecker('0 12 * * *')
    d = checker.to_dict()
    
    print("CronChecker as dictionary:")
    for key, value in d.items():
        print(f"  {key}: {value}")


def example_weekday_schedule():
    """Schedule for weekdays only."""
    print("\n=== Weekday Schedule ===")
    
    # 9am to 5pm on weekdays
    expr = '0 9-17 * * 1-5'
    checker = CronChecker(expr)
    
    print(f"Expression: {expr}")
    print(f"Description: {checker.describe()}")
    
    # Check specific times
    times = [
        datetime(2026, 6, 1, 9, 0),   # Monday 9am
        datetime(2026, 6, 1, 17, 0),  # Monday 5pm
        datetime(2026, 6, 1, 18, 0),  # Monday 6pm
        datetime(2026, 6, 6, 9, 0),   # Saturday 9am
    ]
    
    for dt in times:
        result = checker.matches(dt)
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {dt.strftime('%A %Y-%m-%d %H:%M')}")


def example_workflow():
    """Full workflow example."""
    print("\n=== Full Workflow Example ===")
    
    # User wants a reminder at 9am every weekday
    expr = '0 9 * * 1-5'
    checker = CronChecker(expr)
    
    print("Creating a weekday morning reminder schedule...")
    print(f"Cron: {expr}")
    print(f"Description: {checker.describe()}")
    
    # Validate
    is_valid, error = validate(expr)
    if not is_valid:
        print(f"Error: {error}")
        return
    
    # Find next run
    now = datetime.now()
    next_reminder = checker.get_next_run(now)
    print(f"\nCurrent time: {now}")
    print(f"Next reminder: {next_reminder}")
    print(f"Time until next reminder: {next_reminder - now}")
    
    # Find next 5 runs
    print("\nNext 5 reminders:")
    current = next_reminder
    for i in range(5):
        print(f"  {i+1}. {current.strftime('%Y-%m-%d %H:%M (%A)')}")
        current = checker.get_next_run(current + timedelta(minutes=1))


if __name__ == '__main__':
    example_basic()
    example_special_expressions()
    example_validation()
    example_next_run()
    example_last_run()
    example_run_times()
    example_matches()
    example_to_dict()
    example_weekday_schedule()
    example_workflow()