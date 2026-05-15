# Cron Expression Utilities

A comprehensive Python tool for parsing, validating, and computing cron expressions with zero external dependencies.

## Features

- ✅ Parse standard 5-field cron expressions
- ✅ Parse extended 6-field expressions (with seconds)
- ✅ Validate cron expressions with helpful error messages
- ✅ Calculate next execution times
- ✅ Get multiple future run times
- ✅ Convert to human-readable descriptions
- ✅ Support for special characters: `*`, `,`, `-`, `/`
- ✅ Support for month and day names (e.g., `jan`, `mon`)
- ✅ Built-in presets for common schedules
- ✅ Zero external dependencies

## Installation

No installation required! Simply copy the `mod.py` file to your project.

## Quick Start

```python
from mod import parse_cron, get_next_run, get_next_runs

# Parse a cron expression
cron = parse_cron('*/15 * * * *')  # Every 15 minutes

# Get the next run time
from datetime import datetime
next_run = get_next_run('*/15 * * * *', datetime.now())
print(f"Next run: {next_run}")

# Get the next 5 run times
runs = get_next_runs('0 */2 * * *', datetime.now(), 5)  # Every 2 hours
for i, run in enumerate(runs, 1):
    print(f"{i}. {run}")
```

## Cron Expression Format

### Standard 5-Field Format

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

### Extended 6-Field Format (with seconds)

```
┌───────────── second (0-59)
│ ┌───────────── minute (0-59)
│ │ ┌───────────── hour (0-23)
│ │ │ ┌───────────── day of month (1-31)
│ │ │ │ ┌───────────── month (1-12)
│ │ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
│ │ │ │ │ │
* * * * * *
```

### Special Characters

| Character | Description | Example |
|-----------|-------------|---------|
| `*` | Any value | `* * * * *` (every minute) |
| `,` | Value list separator | `0,15,30,45 * * * *` (every 15 mins) |
| `-` | Range | `0-30 * * * *` (minutes 0-30) |
| `/` | Step values | `*/15 * * * *` (every 15 mins) |

### Examples

| Expression | Description |
|------------|-------------|
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour |
| `*/15 * * * *` | Every 15 minutes |
| `0 */2 * * *` | Every 2 hours |
| `0 0 * * *` | Every day at midnight |
| `30 14 * * *` | Every day at 2:30 PM |
| `0 9-17 * * 1-5` | Every hour 9-5 on weekdays |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 0 1 * *` | First day of every month |
| `0 0 1 1 *` | Every January 1st |

## API Reference

### `parse_cron(expression) -> CronExpression`

Parse a cron expression string.

```python
cron = parse_cron('*/15 * * * *')
print(cron.fields['minute'])  # [0, 15, 30, 45]
```

### `validate_cron(expression) -> Tuple[bool, Optional[str]]`

Validate a cron expression.

```python
is_valid, error = validate_cron('* * * * *')
if is_valid:
    print("Valid!")
else:
    print(f"Invalid: {error}")
```

### `get_next_run(expression, from_time=None) -> datetime`

Get the next run time for a cron expression.

```python
next_run = get_next_run('*/15 * * * *')
print(f"Next run: {next_run}")
```

### `get_next_runs(expression, from_time=None, count=5) -> List[datetime]`

Get multiple future run times.

```python
runs = get_next_runs('0 */2 * * *', count=10)
for run in runs:
    print(run)
```

### `cron_to_human_readable(expression) -> str`

Convert a cron expression to a human-readable description.

```python
desc = cron_to_human_readable('*/15 9-17 * * 1-5')
print(desc)  # "at minutes 0, 15, 30, 45 of hours 9, 10, ..."
```

### `get_preset(preset_name) -> Optional[str]`

Get a cron expression by preset name.

```python
expr = get_preset('every_5_minutes')  # '*/5 * * * *'
```

### `list_presets() -> Dict[str, str]`

List all available presets.

```python
presets = list_presets()
for name, expr in presets.items():
    print(f"{name}: {expr}")
```

## Built-in Presets

| Preset | Expression | Description |
|--------|------------|-------------|
| `every_minute` | `* * * * *` | Every minute |
| `every_hour` | `0 * * * *` | Every hour |
| `every_day` | `0 0 * * *` | Every day at midnight |
| `every_week` | `0 0 * * 0` | Every Sunday at midnight |
| `every_month` | `0 0 1 * *` | First day of every month |
| `every_year` | `0 0 1 1 *` | Every January 1st |
| `every_5_minutes` | `*/5 * * * *` | Every 5 minutes |
| `every_15_minutes` | `*/15 * * * *` | Every 15 minutes |
| `every_30_minutes` | `*/30 * * * *` | Every 30 minutes |
| `every_6_hours` | `0 */6 * * *` | Every 6 hours |
| `every_12_hours` | `0 */12 * * *` | Every 12 hours |
| `every_weekday` | `0 0 * * 1-5` | Weekdays at midnight |
| `every_weekend` | `0 0 * * 0,6` | Weekends at midnight |

## Running Tests

```bash
python test.py
```

## Running Examples

```bash
python example.py
```

## License

MIT License - Part of the AllToolkit project.

## Author

AllToolkit - 2025-05-15