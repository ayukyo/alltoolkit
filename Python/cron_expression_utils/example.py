"""
Cron Expression Utilities - Examples

Demonstrates various use cases for the cron expression utilities.
"""

from datetime import datetime
from mod import (
    CronExpression,
    parse_cron,
    validate_cron,
    get_next_run,
    get_next_runs,
    cron_to_human_readable,
    get_preset,
    list_presets,
)


def print_separator(title: str):
    """Print a section separator."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def main():
    """Run all examples."""
    
    # Example 1: Basic Parsing
    print_separator("Example 1: Basic Cron Expression Parsing")
    
    expressions = [
        '* * * * *',           # Every minute
        '0 * * * *',           # Every hour
        '*/15 * * * *',        # Every 15 minutes
        '0 0 * * *',           # Every day at midnight
        '30 14 * * *',         # Every day at 2:30 PM
        '0 9-17 * * 1-5',      # Every hour 9-5 on weekdays
    ]
    
    for expr in expressions:
        cron = parse_cron(expr)
        print(f"\nExpression: {expr}")
        print(f"  Minutes: {cron.fields['minute'][:10]}...")
        print(f"  Hours: {cron.fields['hour']}")
        print(f"  Days of Month: {cron.fields['day_of_month']}")
        print(f"  Months: {cron.fields['month']}")
        print(f"  Days of Week: {cron.fields['day_of_week']}")
    
    # Example 2: Validation
    print_separator("Example 2: Validating Cron Expressions")
    
    test_cases = [
        '* * * * *',
        '0 0 1 1 *',
        'invalid',
        '* * * *',  # Missing field
        '60 * * * *',  # Invalid minute
    ]
    
    for expr in test_cases:
        is_valid, error = validate_cron(expr)
        status = "✓ Valid" if is_valid else f"✗ Invalid: {error}"
        print(f"  '{expr}' -> {status}")
    
    # Example 3: Next Run Times
    print_separator("Example 3: Calculating Next Run Times")
    
    current_time = datetime(2025, 5, 15, 10, 30, 0)
    print(f"Current time: {current_time}")
    print()
    
    for expr in ['*/5 * * * *', '0 */2 * * *', '0 0 * * *', '0 0 1 * *']:
        next_run = get_next_run(expr, current_time)
        print(f"  '{expr}' -> Next run: {next_run}")
    
    # Example 4: Multiple Next Runs
    print_separator("Example 4: Getting Multiple Future Run Times")
    
    expr = '*/10 * * * *'  # Every 10 minutes
    runs = get_next_runs(expr, current_time, 5)
    print(f"Expression: {expr}")
    print(f"From: {current_time}")
    print("Next 5 runs:")
    for i, run in enumerate(runs, 1):
        print(f"  {i}. {run}")
    
    # Example 5: 6-Field Expressions (with seconds)
    print_separator("Example 5: 6-Field Expressions (with seconds)")
    
    expr_6field = '30 * * * * *'  # Every minute at 30 seconds
    cron_6 = parse_cron(expr_6field)
    print(f"Expression: {expr_6field}")
    print(f"Has seconds: {cron_6.has_seconds}")
    print(f"Seconds: {cron_6.fields['second']}")
    
    next_run = cron_6.get_next_run(current_time)
    print(f"Next run: {next_run}")
    
    # Example 6: Using Presets
    print_separator("Example 6: Using Presets")
    
    print("Available presets:")
    for name, expr in list_presets().items():
        print(f"  {name}: {expr}")
    
    print("\nUsing presets:")
    preset_names = ['every_minute', 'every_hour', 'every_weekday', 'every_5_minutes']
    for name in preset_names:
        expr = get_preset(name)
        if expr:
            print(f"  {name} -> {expr}")
    
    # Example 7: Human-Readable Descriptions
    print_separator("Example 7: Human-Readable Descriptions")
    
    for expr in [
        '* * * * *',
        '*/15 * * * *',
        '0 */6 * * *',
        '30 14 * * 1-5',
        '0 0 1 1 *',
    ]:
        desc = cron_to_human_readable(expr)
        print(f"  {expr}")
        print(f"    -> {desc}")
    
    # Example 8: Complex Expressions
    print_separator("Example 8: Complex Expressions")
    
    complex_cases = [
        '0,15,30,45 9-17 * * 1-5',  # Every 15 mins during business hours on weekdays
        '0 0 * * 0',               # Every Sunday at midnight
        '0 0 29 2 *',              # Every Feb 29 (leap years)
        '*/5 */2 * * *',           # Every 5 minutes every 2 hours
    ]
    
    for expr in complex_cases:
        cron = parse_cron(expr)
        print(f"\nExpression: {expr}")
        print(f"  Minutes: {cron.fields['minute']}")
        print(f"  Hours: {cron.fields['hour']}")
        print(f"  Days of Month: {cron.fields['day_of_month'][:10]}...")
        print(f"  Months: {cron.fields['month']}")
        print(f"  Days of Week: {cron.fields['day_of_week']}")
        print(f"  Next run: {cron.get_next_run(current_time)}")
    
    # Example 9: Working with CronExpression Objects
    print_separator("Example 9: Working with CronExpression Objects")
    
    cron = CronExpression('30 14 * * 1-5')
    print(f"Original: {cron.original}")
    print(f"Has seconds: {cron.has_seconds}")
    print(f"Dict representation: {cron.to_dict()}")
    print(f"String representation: {cron}")
    
    # Example 10: Month and Day Names
    print_separator("Example 10: Month and Day Names")
    
    named_expressions = [
        '* * * jan *',           # Every day in January
        '* * * jan,feb,mar *',   # Every day in Q1
        '* * * * mon,fri',       # Every Monday and Friday
        '* * * * mon-wed',       # Monday through Wednesday
    ]
    
    for expr in named_expressions:
        cron = parse_cron(expr)
        print(f"\nExpression: {expr}")
        if 'month' in str(cron.fields):
            print(f"  Months: {cron.fields['month']}")
        if 'day_of_week' in str(cron.fields):
            print(f"  Days of Week: {cron.fields['day_of_week']}")


if __name__ == '__main__':
    main()