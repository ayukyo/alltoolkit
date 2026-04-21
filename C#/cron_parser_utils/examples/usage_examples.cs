using System;
using CronParserUtils;

namespace CronParserUtils.Examples;

/// <summary>
/// Usage examples for the Cron Expression Parser.
/// </summary>
public static class UsageExamples
{
    public static void Main()
    {
        Console.WriteLine("=== Cron Expression Parser - Usage Examples ===\n");

        BasicParsing();
        StepValuesAndRanges();
        NextExecutionTimes();
        MultipleExecutions();
        MonthAndDayNames();
        HumanReadableDescriptions();
        Validation();
        CommonPatterns();
    }

    private static void BasicParsing()
    {
        Console.WriteLine("--- Basic Parsing ---\n");

        // Parse a simple cron expression
        var cron = CronExpression.Parse("0 * * * *");
        Console.WriteLine($"Expression: {cron.OriginalExpression}");
        Console.WriteLine($"Description: {cron.GetDescription()}");
        Console.WriteLine();

        // Parse specific time
        var daily = CronExpression.Parse("30 14 * * *");
        Console.WriteLine($"Expression: {daily.OriginalExpression}");
        Console.WriteLine($"Description: {daily.GetDescription()}");
        Console.WriteLine();

        // Every minute
        var everyMinute = CronExpression.Parse("* * * * *");
        Console.WriteLine($"Expression: {everyMinute.OriginalExpression}");
        Console.WriteLine($"Description: {everyMinute.GetDescription()}");
        Console.WriteLine();
    }

    private static void StepValuesAndRanges()
    {
        Console.WriteLine("--- Step Values and Ranges ---\n");

        // Every 5 minutes
        var every5 = CronExpression.Parse("*/5 * * * *");
        Console.WriteLine($"Every 5 minutes: {every5.OriginalExpression}");
        Console.WriteLine($"Description: {every5.GetDescription()}");
        Console.WriteLine();

        // Every 15 minutes during business hours
        var business = CronExpression.Parse("*/15 9-17 * * *");
        Console.WriteLine($"Every 15 min during 9-17: {business.OriginalExpression}");
        Console.WriteLine($"Description: {business.GetDescription()}");
        Console.WriteLine();

        // Hourly on weekdays
        var weekdays = CronExpression.Parse("0 9-17 * * 1-5");
        Console.WriteLine($"Hourly on weekdays: {weekdays.OriginalExpression}");
        Console.WriteLine($"Description: {weekdays.GetDescription()}");
        Console.WriteLine();
    }

    private static void NextExecutionTimes()
    {
        Console.WriteLine("--- Next Execution Times ---\n");

        var cron = CronExpression.Parse("30 14 * * *"); // Daily at 2:30 PM

        // Get next execution from now
        var next = cron.GetNextExecution();
        Console.WriteLine($"Next execution: {next:yyyy-MM-dd HH:mm:ss dddd}");

        // Get next execution from a specific time
        var after = new DateTime(2024, 1, 15, 10, 0, 0);
        var nextFrom = cron.GetNextExecution(after);
        Console.WriteLine($"Next after {after:yyyy-MM-dd HH:mm}: {nextFrom:yyyy-MM-dd HH:mm:ss}");
        Console.WriteLine();
    }

    private static void MultipleExecutions()
    {
        Console.WriteLine("--- Multiple Future Executions ---\n");

        var cron = CronExpression.Parse("0 */6 * * *"); // Every 6 hours

        var executions = cron.GetNextExecutions(5);
        Console.WriteLine("Next 5 executions:");
        foreach (var exec in executions)
        {
            Console.WriteLine($"  - {exec:yyyy-MM-dd HH:mm:ss dddd}");
        }
        Console.WriteLine();
    }

    private static void MonthAndDayNames()
    {
        Console.WriteLine("--- Month and Day Names ---\n");

        // Using month names
        var quarterly = CronExpression.Parse("0 0 1 JAN,APR,JUL,OCT *");
        Console.WriteLine($"Quarterly: {quarterly.OriginalExpression}");
        Console.WriteLine($"Description: {quarterly.GetDescription()}");
        Console.WriteLine();

        // Using day names
        var weekend = CronExpression.Parse("0 10 * * SAT,SUN");
        Console.WriteLine($"Weekend mornings: {weekend.OriginalExpression}");
        Console.WriteLine($"Description: {weekend.GetDescription()}");
        Console.WriteLine();

        // Mixed
        var mixed = CronExpression.Parse("0 9 1-7 * SUN");
        Console.WriteLine($"First Sunday of month: {mixed.OriginalExpression}");
        Console.WriteLine($"Description: {mixed.GetDescription()}");
        Console.WriteLine();
    }

    private static void HumanReadableDescriptions()
    {
        Console.WriteLine("--- Human-Readable Descriptions ---\n");

        var expressions = new[]
        {
            "* * * * *",
            "0 * * * *",
            "0 0 * * *",
            "0 0 * * 0",
            "0 0 * * 1-5",
            "0 0 1 * *",
            "0 0 1 1 *",
            "*/5 * * * *",
            "0 9-17 * * 1-5",
            "30 14 15 * *",
        };

        foreach (var expr in expressions)
        {
            var cron = CronExpression.Parse(expr);
            Console.WriteLine($"{expr,-15} → {cron.GetDescription()}");
        }
        Console.WriteLine();
    }

    private static void Validation()
    {
        Console.WriteLine("--- Validation ---\n");

        // Using TryParse for validation
        var expressions = new[] { "* * * * *", "invalid", "0 0 * * *", "60 * * * *" };

        foreach (var expr in expressions)
        {
            if (CronExpression.TryParse(expr, out var cron))
            {
                Console.WriteLine($"Valid: {expr} → {cron!.GetDescription()}");
            }
            else
            {
                Console.WriteLine($"Invalid: {expr}");
            }
        }
        Console.WriteLine();
    }

    private static void CommonPatterns()
    {
        Console.WriteLine("--- Common Cron Patterns ---\n");

        var patterns = new (string Expression, string Name)[]
        {
            ("* * * * *", "Every minute"),
            ("0 * * * *", "Every hour"),
            ("0 0 * * *", "Every day at midnight"),
            ("0 0 * * 0", "Every Sunday at midnight"),
            ("0 0 * * 1-5", "Every weekday at midnight"),
            ("0 9 * * 1-5", "Weekdays at 9 AM"),
            ("0 0 1 * *", "First day of month at midnight"),
            ("0 0 1 1 *", "January 1st at midnight (yearly)"),
            ("*/5 * * * *", "Every 5 minutes"),
            ("*/15 * * * *", "Every 15 minutes"),
            ("0 */2 * * *", "Every 2 hours"),
            ("0 8-17 * * *", "Every hour between 8 AM and 5 PM"),
            ("0 9 * * 1", "Every Monday at 9 AM"),
            ("0 0 1 JAN,JUL *", "First day of January and July"),
        };

        Console.WriteLine("Pattern                      | Description");
        Console.WriteLine("-----------------------------|------------------------------------------");
        
        foreach (var (expr, name) in patterns)
        {
            var cron = CronExpression.Parse(expr);
            Console.WriteLine($"{name,-28} | {expr,-14} → {cron.GetDescription()}");
        }
        Console.WriteLine();

        // Demonstrate checking if a time matches
        Console.WriteLine("--- Time Matching ---\n");
        
        var schedule = CronExpression.Parse("0 9 * * 1-5"); // 9 AM on weekdays
        
        var times = new[]
        {
            new DateTime(2024, 1, 15, 9, 0, 0),  // Monday 9 AM
            new DateTime(2024, 1, 15, 10, 0, 0), // Monday 10 AM
            new DateTime(2024, 1, 20, 9, 0, 0),  // Saturday 9 AM
            new DateTime(2024, 1, 17, 9, 0, 0),  // Wednesday 9 AM
        };

        Console.WriteLine($"Schedule: {schedule.OriginalExpression} ({schedule.GetDescription()})");
        foreach (var time in times)
        {
            var matches = schedule.Matches(time);
            Console.WriteLine($"  {time:yyyy-MM-dd HH:mm dddd} → {(matches ? "✓ Matches" : "✗ No match")}");
        }
    }
}