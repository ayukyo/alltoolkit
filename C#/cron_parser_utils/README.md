# Cron Expression Parser - C#

A lightweight, zero-dependency cron expression parser for .NET/C#. Parses standard 5-field cron expressions, calculates next execution times, and generates human-readable descriptions.

## Features

- ✅ Parse standard 5-field cron expressions (minute, hour, day, month, day-of-week)
- ✅ Calculate next execution time(s)
- ✅ Generate human-readable descriptions
- ✅ Support for step values (`*/5`, `1-10/2`)
- ✅ Support for ranges (`1-5`, `MON-FRI`)
- ✅ Support for lists (`1,15,30`)
- ✅ Support for month/day names (`JAN`, `FEB`, `MON`, `TUE`)
- ✅ Check if a specific time matches the expression
- ✅ Zero external dependencies (pure C#)
- ✅ Comprehensive test coverage

## Installation

Copy the `CronExpression.cs` and `CronDescriptor.cs` files to your project.

## Quick Start

```csharp
using CronParserUtils;

// Parse a cron expression
var cron = CronExpression.Parse("0 9 * * 1-5"); // 9 AM on weekdays

// Get next execution time
DateTime nextRun = cron.GetNextExecution();
Console.WriteLine($"Next run: {nextRun}");

// Get multiple future executions
var upcoming = cron.GetNextExecutions(5);
foreach (var time in upcoming)
    Console.WriteLine(time);

// Get human-readable description
string desc = cron.GetDescription();
Console.WriteLine(desc); // "Every Monday, Tuesday, Wednesday, Thursday, Friday at 09:00"

// Check if a time matches
bool matches = cron.Matches(new DateTime(2024, 1, 15, 9, 0, 0)); // Monday 9 AM
```

## Cron Expression Format

Standard 5-field format:
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of week (0 - 6 or SUN-SAT)
│ │ │ │ │
* * * * *
```

### Supported Syntax

| Syntax | Example | Description |
|--------|---------|-------------|
| `*` | `* * * * *` | Any value (every minute/hour/etc) |
| Specific value | `30 14 * * *` | At minute 30, hour 14 |
| Range | `0 9-17 * * *` | Hours 9 through 17 |
| List | `1,15,30 * * * *` | Minutes 1, 15, and 30 |
| Step | `*/5 * * * *` | Every 5 minutes |
| Range with step | `1-30/5 * * * *` | Every 5 minutes from 1-30 |
| Month names | `0 0 1 JAN *` | January 1st |
| Day names | `0 0 * * MON-FRI` | Monday through Friday |

## Common Patterns

| Expression | Description |
|------------|-------------|
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour |
| `0 0 * * *` | Daily at midnight |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 0 * * 1-5` | Every weekday at midnight |
| `0 9 * * 1-5` | Weekdays at 9 AM |
| `0 0 1 * *` | First day of every month |
| `*/5 * * * *` | Every 5 minutes |
| `0 */2 * * *` | Every 2 hours |

## API Reference

### `CronExpression.Parse(string expression)`
Parse a cron expression string. Throws `ArgumentException` if invalid.

### `CronExpression.TryParse(string expression, out CronExpression? result)`
Attempt to parse. Returns `true` if successful.

### `GetNextExecution(DateTime? after = null)`
Get the next execution time after the specified datetime (defaults to now).

### `GetNextExecutions(int count, DateTime? after = null)`
Get multiple future execution times.

### `Matches(DateTime time)`
Check if the given time matches the cron expression.

### `GetDescription()`
Get a human-readable description of the schedule.

## Running Tests

```bash
# Using dotnet
dotnet run --project tests

# Or compile and run directly
csc CronExpression.cs CronDescriptor.cs CronExpressionTests.cs -out:Tests.exe
Tests.exe
```

## Files

- `CronExpression.cs` - Main parser implementation
- `CronDescriptor.cs` - Human-readable description generator
- `CronExpressionTests.cs` - Comprehensive test suite
- `examples/usage_examples.cs` - Usage examples

## License

MIT License - Free for personal and commercial use.