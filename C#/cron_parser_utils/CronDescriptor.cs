using System;
using System.Linq;
using System.Text;

namespace CronParserUtils;

/// <summary>
/// Generates human-readable descriptions for cron expressions.
/// </summary>
internal static class CronDescriptor
{
    public static string Describe(CronExpression cron)
    {
        var (minutes, hours, daysOfMonth, months, daysOfWeek) = cron.GetFields();
        
        var sb = new StringBuilder();
        
        // Determine the type of expression
        var isEveryMinute = minutes.Length == 60;
        var isEveryHour = hours.Length == 24;
        var isEveryDayOfMonth = daysOfMonth.Length == 31;
        var isEveryMonth = months.Length == 12;
        var isEveryDayOfWeek = daysOfWeek.Length == 7;

        // Handle common patterns
        if (isEveryMinute && isEveryHour && isEveryDayOfMonth && isEveryMonth && isEveryDayOfWeek)
        {
            return "Every minute";
        }

        // Minute patterns
        if (minutes.Length == 1)
        {
            if (isEveryHour && isEveryDayOfMonth && isEveryMonth && isEveryDayOfWeek)
            {
                return $"At minute {minutes[0]} of every hour";
            }
            
            if (hours.Length == 1 && isEveryDayOfMonth && isEveryMonth && isEveryDayOfWeek)
            {
                return $"Every day at {hours[0]:00}:{minutes[0]:00}";
            }

            if (hours.Length == 1 && isEveryMonth)
            {
                var dayDesc = DescribeDays(daysOfMonth, daysOfWeek, isEveryDayOfMonth, isEveryDayOfWeek);
                var monthDesc = isEveryMonth ? "" : $" in {DescribeMonths(months)}";
                return $"{dayDesc} at {hours[0]:00}:{minutes[0]:00}{monthDesc}";
            }
        }

        // Hour patterns
        if (isEveryMinute && hours.Length == 1)
        {
            return $"Every minute during hour {hours[0]}";
        }

        // Build general description
        var timeDesc = DescribeTime(minutes, hours, isEveryMinute, isEveryHour);
        var dayDesc2 = DescribeDays(daysOfMonth, daysOfWeek, isEveryDayOfMonth, isEveryDayOfWeek);
        var monthDesc2 = isEveryMonth ? "" : $" in {DescribeMonths(months)}";

        sb.Append(timeDesc);
        if (!string.IsNullOrEmpty(dayDesc2))
        {
            sb.Append(" on ");
            sb.Append(dayDesc2);
        }
        sb.Append(monthDesc2);

        return sb.ToString();
    }

    private static string DescribeTime(int[] minutes, int[] hours, bool everyMinute, bool everyHour)
    {
        if (everyMinute && everyHour)
            return "Every minute";

        if (everyMinute)
            return $"Every minute during hour{(hours.Length > 1 ? "s" : "")} {DescribeValues(hours)}";

        if (everyHour)
            return $"At minute{(minutes.Length > 1 ? "s" : "")} {DescribeValues(minutes)} of every hour";

        if (minutes.Length == 1 && hours.Length == 1)
            return $"At {hours[0]:00}:{minutes[0]:00}";

        return $"At minute{(minutes.Length > 1 ? "s" : "")} {DescribeValues(minutes)} of hour{(hours.Length > 1 ? "s" : "")} {DescribeValues(hours)}";
    }

    private static string DescribeDays(int[] daysOfMonth, int[] daysOfWeek, bool everyDayOfMonth, bool everyDayOfWeek)
    {
        if (everyDayOfMonth && everyDayOfWeek)
            return "every day";

        if (everyDayOfMonth)
            return DescribeDaysOfWeek(daysOfWeek);

        if (everyDayOfWeek)
            return $"day{(daysOfMonth.Length > 1 ? "s" : "")} {DescribeValues(daysOfMonth)} of the month";

        return $"{DescribeDaysOfWeek(daysOfWeek)} and day{(daysOfMonth.Length > 1 ? "s" : "")} {DescribeValues(daysOfMonth)} of the month";
    }

    private static string DescribeDaysOfWeek(int[] days)
    {
        if (days.Length == 7)
            return "every day";

        if (days.Length == 5 && !days.Contains(0) && !days.Contains(6))
            return "weekdays";

        if (days.Length == 2 && days.Contains(0) && days.Contains(6))
            return "weekends";

        var names = days.Select(d => GetDayName(d)).ToArray();
        return string.Join(", ", names);
    }

    private static string DescribeMonths(int[] months)
    {
        if (months.Length == 12)
            return "every month";

        var names = months.Select(m => GetMonthName(m)).ToArray();
        return string.Join(", ", names);
    }

    private static string DescribeValues(int[] values)
    {
        if (values.Length == 1)
            return values[0].ToString();

        // Check for ranges
        var ranges = new System.Collections.Generic.List<string>();
        int rangeStart = values[0];
        int rangeEnd = values[0];

        for (int i = 1; i < values.Length; i++)
        {
            if (values[i] == rangeEnd + 1)
            {
                rangeEnd = values[i];
            }
            else
            {
                ranges.Add(rangeStart == rangeEnd 
                    ? rangeStart.ToString() 
                    : $"{rangeStart}-{rangeEnd}");
                rangeStart = rangeEnd = values[i];
            }
        }
        ranges.Add(rangeStart == rangeEnd 
            ? rangeStart.ToString() 
            : $"{rangeStart}-{rangeEnd}");

        return string.Join(", ", ranges);
    }

    private static string GetDayName(int dayOfWeek)
    {
        return dayOfWeek switch
        {
            0 => "Sunday",
            1 => "Monday",
            2 => "Tuesday",
            3 => "Wednesday",
            4 => "Thursday",
            5 => "Friday",
            6 => "Saturday",
            _ => throw new ArgumentException($"Invalid day of week: {dayOfWeek}")
        };
    }

    private static string GetMonthName(int month)
    {
        return month switch
        {
            1 => "January",
            2 => "February",
            3 => "March",
            4 => "April",
            5 => "May",
            6 => "June",
            7 => "July",
            8 => "August",
            9 => "September",
            10 => "October",
            11 => "November",
            12 => "December",
            _ => throw new ArgumentException($"Invalid month: {month}")
        };
    }
}