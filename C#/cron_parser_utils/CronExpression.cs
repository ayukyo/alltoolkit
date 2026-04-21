using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace CronParserUtils;

/// <summary>
/// Represents a parsed cron expression with methods for calculating next execution times.
/// Supports standard 5-field cron format: minute hour day-of-month month day-of-week
/// </summary>
public class CronExpression
{
    private readonly int[] _minutes;
    private readonly int[] _hours;
    private readonly int[] _daysOfMonth;
    private readonly int[] _months;
    private readonly int[] _daysOfWeek;

    private static readonly string[] MonthNames = 
    {
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
    };

    private static readonly string[] DayNames = 
    {
        "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"
    };

    public string OriginalExpression { get; }

    private CronExpression(string expression, int[] minutes, int[] hours, 
        int[] daysOfMonth, int[] months, int[] daysOfWeek)
    {
        OriginalExpression = expression;
        _minutes = minutes;
        _hours = hours;
        _daysOfMonth = daysOfMonth;
        _months = months;
        _daysOfWeek = daysOfWeek;
    }

    /// <summary>
    /// Parses a cron expression string.
    /// </summary>
    /// <param name="expression">Cron expression (5 fields: minute hour day month day-of-week)</param>
    /// <returns>Parsed CronExpression object</returns>
    /// <exception cref="ArgumentException">Thrown when expression is invalid</exception>
    public static CronExpression Parse(string expression)
    {
        if (string.IsNullOrWhiteSpace(expression))
            throw new ArgumentException("Cron expression cannot be empty", nameof(expression));

        var parts = expression.Trim().Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
        
        if (parts.Length != 5)
            throw new ArgumentException($"Expected 5 fields, got {parts.Length}", nameof(expression));

        try
        {
            var minutes = ParseField(parts[0], 0, 59, MonthNames, DayNames);
            var hours = ParseField(parts[1], 0, 23, MonthNames, DayNames);
            var daysOfMonth = ParseField(parts[2], 1, 31, MonthNames, DayNames);
            var months = ParseField(parts[3], 1, 12, MonthNames, DayNames);
            var daysOfWeek = ParseField(parts[4], 0, 6, MonthNames, DayNames);

            return new CronExpression(expression, minutes, hours, daysOfMonth, months, daysOfWeek);
        }
        catch (Exception ex) when (ex is not ArgumentException)
        {
            throw new ArgumentException($"Invalid cron expression: {ex.Message}", nameof(expression), ex);
        }
    }

    /// <summary>
    /// Tries to parse a cron expression string.
    /// </summary>
    /// <param name="expression">Cron expression</param>
    /// <param name="result">Parsed result if successful</param>
    /// <returns>True if parsing succeeded, false otherwise</returns>
    public static bool TryParse(string expression, out CronExpression? result)
    {
        try
        {
            result = Parse(expression);
            return true;
        }
        catch
        {
            result = null;
            return false;
        }
    }

    /// <summary>
    /// Gets the next execution time after the specified date.
    /// </summary>
    /// <param name="after">The starting point (defaults to now)</param>
    /// <returns>Next execution time</returns>
    public DateTime GetNextExecution(DateTime? after = null)
    {
        var start = after ?? DateTime.Now;
        start = start.AddSeconds(1).AddMilliseconds(-start.Millisecond);
        
        // Round to the next minute if we're at the start of a minute
        if (start.Second > 0)
            start = start.AddSeconds(60 - start.Second);

        return GetNextAfter(start);
    }

    /// <summary>
    /// Gets multiple next execution times.
    /// </summary>
    /// <param name="count">Number of future times to return</param>
    /// <param name="after">Starting point (defaults to now)</param>
    /// <returns>List of next execution times</returns>
    public List<DateTime> GetNextExecutions(int count, DateTime? after = null)
    {
        var result = new List<DateTime>();
        var next = after ?? DateTime.Now;

        for (int i = 0; i < count; i++)
        {
            next = GetNextExecution(next);
            result.Add(next);
        }

        return result;
    }

    /// <summary>
    /// Checks if the cron expression should fire at the specified time.
    /// </summary>
    /// <param name="time">Time to check</param>
    /// <returns>True if the expression matches the time</returns>
    public bool Matches(DateTime time)
    {
        return _minutes.Contains(time.Minute) &&
               _hours.Contains(time.Hour) &&
               _daysOfMonth.Contains(time.Day) &&
               _months.Contains(time.Month) &&
               _daysOfWeek.Contains((int)time.DayOfWeek);
    }

    /// <summary>
    /// Returns a human-readable description of the cron expression.
    /// </summary>
    public string GetDescription()
    {
        return CronDescriptor.Describe(this);
    }

    private DateTime GetNextAfter(DateTime start)
    {
        var next = new DateTime(start.Year, start.Month, start.Day, 
            start.Hour, start.Minute, 0);

        // Search up to 5 years in the future
        var maxDate = start.AddYears(5);

        while (next < maxDate)
        {
            // Check month
            if (!_months.Contains(next.Month))
            {
                next = next.AddMonths(1);
                next = new DateTime(next.Year, next.Month, 1, 0, 0, 0);
                continue;
            }

            // Check day
            if (!IsValidDay(next))
            {
                next = next.AddDays(1);
                next = new DateTime(next.Year, next.Month, next.Day, 0, 0, 0);
                continue;
            }

            // Check hour
            if (!_hours.Contains(next.Hour))
            {
                next = next.AddHours(1);
                next = new DateTime(next.Year, next.Month, next.Day, next.Hour, 0, 0);
                continue;
            }

            // Check minute
            if (!_minutes.Contains(next.Minute))
            {
                next = next.AddMinutes(1);
                continue;
            }

            return next;
        }

        throw new InvalidOperationException("Could not find a valid execution time within 5 years");
    }

    private bool IsValidDay(DateTime date)
    {
        // Check day of month
        var dayOfMonthValid = _daysOfMonth.Contains(date.Day);
        
        // Handle days that don't exist in the month
        if (date.Day > DateTime.DaysInMonth(date.Year, date.Month))
            return false;

        // Check day of week
        var dayOfWeekValid = _daysOfWeek.Contains((int)date.DayOfWeek);

        // Special handling for '*' in either field
        // If both are '*', day matches
        // If one is specific, that one controls
        if (_daysOfMonth.Length == 31 && _daysOfWeek.Length == 7)
        {
            return true; // Both are '*', every day
        }
        
        if (_daysOfMonth.Length == 31) // day-of-month is '*'
        {
            return dayOfWeekValid;
        }
        
        if (_daysOfWeek.Length == 7) // day-of-week is '*'
        {
            return dayOfMonthValid;
        }

        // Both have specific values, either can match
        return dayOfMonthValid || dayOfWeekValid;
    }

    private static int[] ParseField(string field, int min, int max, 
        string[] monthNames, string[] dayNames)
    {
        var result = new HashSet<int>();

        // Handle step values (e.g., */5, 1-10/2)
        var stepMatch = Regex.Match(field, @"^(.+?)/(\d+)$");
        int step = 1;
        if (stepMatch.Success)
        {
            field = stepMatch.Groups[1].Value;
            step = int.Parse(stepMatch.Groups[2].Value);
            if (step <= 0)
                throw new ArgumentException("Step value must be positive");
        }

        // Handle wildcards
        if (field == "*")
        {
            for (int i = min; i <= max; i += step)
                result.Add(i);
            return result.ToArray();
        }

        // Handle multiple values (comma-separated)
        var parts = field.Split(',');
        foreach (var part in parts)
        {
            var trimmed = part.Trim();
            
            // Handle ranges (e.g., 1-5, MON-FRI)
            var rangeMatch = Regex.Match(trimmed, @"^(\w+)-(\w+)$");
            if (rangeMatch.Success)
            {
                int start = ParseValue(rangeMatch.Groups[1].Value, min, max, monthNames, dayNames);
                int end = ParseValue(rangeMatch.Groups[2].Value, min, max, monthNames, dayNames);
                
                for (int i = start; i <= end; i += step)
                    result.Add(i);
            }
            else
            {
                int value = ParseValue(trimmed, min, max, monthNames, dayNames);
                result.Add(value);
            }
        }

        // Apply step to collected values
        if (step > 1)
        {
            var sorted = result.OrderBy(x => x).ToList();
            result.Clear();
            for (int i = 0; i < sorted.Count; i += step)
                result.Add(sorted[i]);
        }

        // Validate values
        foreach (var val in result)
        {
            if (val < min || val > max)
                throw new ArgumentException($"Value {val} out of range [{min}, {max}]");
        }

        return result.OrderBy(x => x).ToArray();
    }

    private static int ParseValue(string value, int min, int max, 
        string[] monthNames, string[] dayNames)
    {
        // Try parsing as number
        if (int.TryParse(value, out int num))
            return num;

        // Try month names
        var monthIndex = Array.FindIndex(monthNames, 
            m => m.Equals(value, StringComparison.OrdinalIgnoreCase));
        if (monthIndex >= 0)
        {
            if (min == 1 && max == 12) // Month field
                return monthIndex + 1;
            throw new ArgumentException($"Month name '{value}' not valid for this field");
        }

        // Try day names
        var dayIndex = Array.FindIndex(dayNames, 
            d => d.Equals(value, StringComparison.OrdinalIgnoreCase));
        if (dayIndex >= 0)
        {
            if (min == 0 && max == 6) // Day of week field
                return dayIndex;
            throw new ArgumentException($"Day name '{value}' not valid for this field");
        }

        throw new ArgumentException($"Invalid value: {value}");
    }

    /// <summary>
    /// Gets the allowed values for each field.
    /// </summary>
    public (int[] Minutes, int[] Hours, int[] DaysOfMonth, int[] Months, int[] DaysOfWeek) GetFields()
    {
        return (_minutes, _hours, _daysOfMonth, _months, _daysOfWeek);
    }

    public override string ToString() => OriginalExpression;
}