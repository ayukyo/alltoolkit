using System;
using System.Collections.Generic;

namespace CronParserUtils.Tests;

/// <summary>
/// Comprehensive tests for CronExpression parser.
/// Run with: dotnet test or via TestRunner.cs
/// </summary>
public static class CronExpressionTests
{
    private static int _passed = 0;
    private static int _failed = 0;
    private static readonly List<string> _errors = new();

    public static void RunAllTests()
    {
        Console.WriteLine("=== Cron Expression Parser Tests ===\n");

        TestBasicParsing();
        TestStepValues();
        TestRanges();
        TestLists();
        TestMonthNames();
        TestDayNames();
        TestComplexExpressions();
        TestNextExecution();
        TestNextExecutions();
        TestMatches();
        TestDescription();
        TestEdgeCases();
        TestErrorHandling();

        Console.WriteLine($"\n=== Test Results ===");
        Console.WriteLine($"Passed: {_passed}");
        Console.WriteLine($"Failed: {_failed}");
        
        if (_errors.Count > 0)
        {
            Console.WriteLine("\nErrors:");
            foreach (var error in _errors)
            {
                Console.WriteLine($"  - {error}");
            }
        }
    }

    private static void TestBasicParsing()
    {
        Console.WriteLine("\n--- Basic Parsing Tests ---");

        // Every minute
        Assert("Parse '* * * * *'", () =>
        {
            var cron = CronExpression.Parse("* * * * *");
            var (m, h, dom, mon, dow) = cron.GetFields();
            return m.Length == 60 && h.Length == 24 && dom.Length == 31 && 
                   mon.Length == 12 && dow.Length == 7;
        });

        // Specific time
        Assert("Parse '0 0 * * *'", () =>
        {
            var cron = CronExpression.Parse("0 0 * * *");
            var (m, h, _, _, _) = cron.GetFields();
            return m.Length == 1 && m[0] == 0 && h.Length == 1 && h[0] == 0;
        });

        // Specific values
        Assert("Parse '30 14 * * *'", () =>
        {
            var cron = CronExpression.Parse("30 14 * * *");
            var (m, h, _, _, _) = cron.GetFields();
            return m[0] == 30 && h[0] == 14;
        });
    }

    private static void TestStepValues()
    {
        Console.WriteLine("\n--- Step Values Tests ---");

        Assert("Parse '*/5 * * * *'", () =>
        {
            var cron = CronExpression.Parse("*/5 * * * *");
            var (m, _, _, _, _) = cron.GetFields();
            return m.SequenceEqual(new[] { 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 });
        });

        Assert("Parse '*/15 * * * *'", () =>
        {
            var cron = CronExpression.Parse("*/15 * * * *");
            var (m, _, _, _, _) = cron.GetFields();
            return m.SequenceEqual(new[] { 0, 15, 30, 45 });
        });

        Assert("Parse '0 */2 * * *'", () =>
        {
            var cron = CronExpression.Parse("0 */2 * * *");
            var (_, h, _, _, _) = cron.GetFields();
            return h.SequenceEqual(new[] { 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 });
        });
    }

    private static void TestRanges()
    {
        Console.WriteLine("\n--- Range Tests ---");

        Assert("Parse '0 9-17 * * *'", () =>
        {
            var cron = CronExpression.Parse("0 9-17 * * *");
            var (_, h, _, _, _) = cron.GetFields();
            return h.Length == 9 && h[0] == 9 && h[8] == 17;
        });

        Assert("Parse '0-5 * * * *'", () =>
        {
            var cron = CronExpression.Parse("0-5 * * * *");
            var (m, _, _, _, _) = cron.GetFields();
            return m.SequenceEqual(new[] { 0, 1, 2, 3, 4, 5 });
        });
    }

    private static void TestLists()
    {
        Console.WriteLine("\n--- List Tests ---");

        Assert("Parse '1,15,30 * * * *'", () =>
        {
            var cron = CronExpression.Parse("1,15,30 * * * *");
            var (m, _, _, _, _) = cron.GetFields();
            return m.SequenceEqual(new[] { 1, 15, 30 });
        });

        Assert("Parse '0 8,12,18 * * *'", () =>
        {
            var cron = CronExpression.Parse("0 8,12,18 * * *");
            var (_, h, _, _, _) = cron.GetFields();
            return h.SequenceEqual(new[] { 8, 12, 18 });
        });
    }

    private static void TestMonthNames()
    {
        Console.WriteLine("\n--- Month Names Tests ---");

        Assert("Parse '0 0 1 JAN *'", () =>
        {
            var cron = CronExpression.Parse("0 0 1 JAN *");
            var (_, _, _, mon, _) = cron.GetFields();
            return mon.SequenceEqual(new[] { 1 });
        });

        Assert("Parse '0 0 1 JAN-MAR *'", () =>
        {
            var cron = CronExpression.Parse("0 0 1 JAN-MAR *");
            var (_, _, _, mon, _) = cron.GetFields();
            return mon.SequenceEqual(new[] { 1, 2, 3 });
        });

        Assert("Parse '0 0 1 JAN,JUN,DEC *'", () =>
        {
            var cron = CronExpression.Parse("0 0 1 JAN,JUN,DEC *");
            var (_, _, _, mon, _) = cron.GetFields();
            return mon.SequenceEqual(new[] { 1, 6, 12 });
        });
    }

    private static void TestDayNames()
    {
        Console.WriteLine("\n--- Day Names Tests ---");

        Assert("Parse '0 0 * * MON'", () =>
        {
            var cron = CronExpression.Parse("0 0 * * MON");
            var (_, _, _, _, dow) = cron.GetFields();
            return dow.SequenceEqual(new[] { 1 });
        });

        Assert("Parse '0 0 * * MON-FRI'", () =>
        {
            var cron = CronExpression.Parse("0 0 * * MON-FRI");
            var (_, _, _, _, dow) = cron.GetFields();
            return dow.SequenceEqual(new[] { 1, 2, 3, 4, 5 });
        });

        Assert("Parse '0 0 * * SUN,SAT'", () =>
        {
            var cron = CronExpression.Parse("0 0 * * SUN,SAT");
            var (_, _, _, _, dow) = cron.GetFields();
            return dow.SequenceEqual(new[] { 0, 6 });
        });
    }

    private static void TestComplexExpressions()
    {
        Console.WriteLine("\n--- Complex Expression Tests ---");

        Assert("Parse '*/5 9-17 * * 1-5'", () =>
        {
            var cron = CronExpression.Parse("*/5 9-17 * * 1-5");
            var (m, h, _, _, dow) = cron.GetFields();
            return m.Length == 12 && h.Length == 9 && dow.SequenceEqual(new[] { 1, 2, 3, 4, 5 });
        });

        Assert("Parse '0 0,12 1 1 *'", () =>
        {
            var cron = CronExpression.Parse("0 0,12 1 1 *");
            var (m, h, dom, mon, _) = cron.GetFields();
            return m[0] == 0 && h.SequenceEqual(new[] { 0, 12 }) && 
                   dom[0] == 1 && mon[0] == 1;
        });

        Assert("Parse '30 4 1,15 * *'", () =>
        {
            var cron = CronExpression.Parse("30 4 1,15 * *");
            var (m, h, dom, _, _) = cron.GetFields();
            return m[0] == 30 && h[0] == 4 && dom.SequenceEqual(new[] { 1, 15 });
        });
    }

    private static void TestNextExecution()
    {
        Console.WriteLine("\n--- Next Execution Tests ---");

        Assert("GetNextExecution returns valid date", () =>
        {
            var cron = CronExpression.Parse("0 * * * *");
            var next = cron.GetNextExecution();
            return next.Minute == 0;
        });

        Assert("GetNextExecution from specific time", () =>
        {
            var cron = CronExpression.Parse("30 * * * *");
            var after = new DateTime(2024, 1, 15, 10, 0, 0);
            var next = cron.GetNextExecution(after);
            return next.Minute == 30 && next.Hour == 10;
        });

        Assert("GetNextExecution with hour constraint", () =>
        {
            var cron = CronExpression.Parse("0 14 * * *");
            var after = new DateTime(2024, 1, 15, 10, 0, 0);
            var next = cron.GetNextExecution(after);
            return next.Hour == 14 && next.Minute == 0;
        });

        Assert("GetNextExecution with day constraint", () =>
        {
            var cron = CronExpression.Parse("0 0 15 * *");
            var after = new DateTime(2024, 1, 10, 0, 0, 0);
            var next = cron.GetNextExecution(after);
            return next.Day == 15 && next.Hour == 0 && next.Minute == 0;
        });

        Assert("GetNextExecution with weekday constraint", () =>
        {
            var cron = CronExpression.Parse("0 9 * * 1-5"); // 9 AM on weekdays
            var after = new DateTime(2024, 1, 15, 0, 0, 0); // Monday
            var next = cron.GetNextExecution(after);
            return next.Hour == 9 && (int)next.DayOfWeek >= 1 && (int)next.DayOfWeek <= 5;
        });
    }

    private static void TestNextExecutions()
    {
        Console.WriteLine("\n--- Multiple Executions Tests ---");

        Assert("GetNextExecutions returns correct count", () =>
        {
            var cron = CronExpression.Parse("0 * * * *");
            var executions = cron.GetNextExecutions(5);
            return executions.Count == 5;
        });

        Assert("GetNextExecutions returns sequential times", () =>
        {
            var cron = CronExpression.Parse("*/10 * * * *");
            var executions = cron.GetNextExecutions(5);
            for (int i = 1; i < executions.Count; i++)
            {
                var diff = executions[i] - executions[i - 1];
                if (diff.TotalMinutes < 10 || diff.TotalMinutes > 60)
                    return false;
            }
            return true;
        });
    }

    private static void TestMatches()
    {
        Console.WriteLine("\n--- Matches Tests ---");

        Assert("Matches returns true for matching time", () =>
        {
            var cron = CronExpression.Parse("30 14 * * *");
            var time = new DateTime(2024, 1, 15, 14, 30, 0);
            return cron.Matches(time);
        });

        Assert("Matches returns false for non-matching time", () =>
        {
            var cron = CronExpression.Parse("30 14 * * *");
            var time = new DateTime(2024, 1, 15, 14, 31, 0);
            return !cron.Matches(time);
        });

        Assert("Matches with day of week", () =>
        {
            var cron = CronExpression.Parse("0 0 * * 1"); // Monday at midnight
            var monday = new DateTime(2024, 1, 15, 0, 0, 0); // Monday
            var tuesday = new DateTime(2024, 1, 16, 0, 0, 0); // Tuesday
            return cron.Matches(monday) && !cron.Matches(tuesday);
        });
    }

    private static void TestDescription()
    {
        Console.WriteLine("\n--- Description Tests ---");

        Assert("Describe every minute", () =>
        {
            var cron = CronExpression.Parse("* * * * *");
            return cron.GetDescription() == "Every minute";
        });

        Assert("Describe specific time", () =>
        {
            var cron = CronExpression.Parse("30 14 * * *");
            var desc = cron.GetDescription();
            return desc.Contains("14") && desc.Contains("30");
        });

        Assert("Describe weekdays", () =>
        {
            var cron = CronExpression.Parse("0 9 * * 1-5");
            var desc = cron.GetDescription();
            return desc.Contains("weekday") || desc.Contains("Monday");
        });

        Assert("Describe every hour at minute 0", () =>
        {
            var cron = CronExpression.Parse("0 * * * *");
            var desc = cron.GetDescription();
            return desc.Contains("hour");
        });
    }

    private static void TestEdgeCases()
    {
        Console.WriteLine("\n--- Edge Cases Tests ---");

        Assert("Handle midnight (0 hour)", () =>
        {
            var cron = CronExpression.Parse("0 0 * * *");
            var (_, h, _, _, _) = cron.GetFields();
            return h.Contains(0);
        });

        Assert("Handle end of day (23 hour)", () =>
        {
            var cron = CronExpression.Parse("59 23 * * *");
            var (m, h, _, _, _) = cron.GetFields();
            return m.Contains(59) && h.Contains(23);
        });

        Assert("Handle December (month 12)", () =>
        {
            var cron = CronExpression.Parse("0 0 1 12 *");
            var (_, _, _, mon, _) = cron.GetFields();
            return mon.Contains(12);
        });

        Assert("Handle Saturday (day 6)", () =>
        {
            var cron = CronExpression.Parse("0 0 * * 6");
            var (_, _, _, _, dow) = cron.GetFields();
            return dow.Contains(6);
        });

        Assert("Handle February 29th", () =>
        {
            var cron = CronExpression.Parse("0 0 29 2 *");
            var (_, _, dom, mon, _) = cron.GetFields();
            return dom.Contains(29) && mon.Contains(2);
        });

        Assert("Handle leap year next execution", () =>
        {
            var cron = CronExpression.Parse("0 0 29 2 *");
            var after = new DateTime(2024, 1, 1, 0, 0, 0);
            var next = cron.GetNextExecution(after);
            return next.Month == 2 && next.Day == 29;
        });
    }

    private static void TestErrorHandling()
    {
        Console.WriteLine("\n--- Error Handling Tests ---");

        Assert("Empty expression throws", () =>
        {
            try
            {
                CronExpression.Parse("");
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("Null expression throws", () =>
        {
            try
            {
                CronExpression.Parse(null!);
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("Too few fields throws", () =>
        {
            try
            {
                CronExpression.Parse("* * * *");
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("Too many fields throws", () =>
        {
            try
            {
                CronExpression.Parse("* * * * * *");
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("Invalid minute throws", () =>
        {
            try
            {
                CronExpression.Parse("60 * * * *");
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("Invalid hour throws", () =>
        {
            try
            {
                CronExpression.Parse("* 24 * * *");
                return false;
            }
            catch (ArgumentException)
            {
                return true;
            }
        });

        Assert("TryParse returns false for invalid", () =>
        {
            return !CronExpression.TryParse("invalid", out _);
        });

        Assert("TryParse returns true for valid", () =>
        {
            return CronExpression.TryParse("0 0 * * *", out _);
        });
    }

    private static void Assert(string name, Func<bool> test)
    {
        try
        {
            if (test())
            {
                Console.WriteLine($"  ✓ {name}");
                _passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ {name} (assertion failed)");
                _failed++;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"  ✗ {name} (exception: {ex.Message})");
            _errors.Add($"{name}: {ex.Message}");
            _failed++;
        }
    }

    private static bool SequenceEqual<T>(this T[] arr, T[] other)
    {
        if (arr.Length != other.Length) return false;
        for (int i = 0; i < arr.Length; i++)
        {
            if (!arr[i]!.Equals(other[i])) return false;
        }
        return true;
    }
}