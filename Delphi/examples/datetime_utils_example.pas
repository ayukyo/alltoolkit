{*******************************************************************************
 * AllToolkit - Delphi DateTime Utilities Example
 * Practical usage examples for DateTime utilities
 *******************************************************************************}

program datetime_utils_example;

{$APPTYPE CONSOLE}

uses
  SysUtils, DateUtils, mod;

procedure ExampleFormatting;
begin
  WriteLn('=== Formatting Examples ===');
  
  var Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 45, 0);
  
  WriteLn('DateTime: ', TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('ISO8601: ', TDateTimeUtils.ToISO8601(Dt));
  WriteLn('RFC3339: ', TDateTimeUtils.ToRFC3339(Dt));
  WriteLn('US Format: ', TDateTimeUtils.ToUSFormat(Dt));
  WriteLn('UK Format: ', TDateTimeUtils.ToUKFormat(Dt));
  WriteLn('Chinese Format: ', TDateTimeUtils.ToChineseFormat(Dt));
  WriteLn('Compact: ', TDateTimeUtils.ToCompactFormat(Dt));
  WriteLn('');
end;

procedure ExampleParsing;
begin
  WriteLn('=== Parsing Examples ===');
  
  var Dt := TDateTimeUtils.Parse('2024-03-15', 'yyyy-mm-dd');
  WriteLn('Parsed date: ', TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd'));
  
  var Dt2 := TDateTimeUtils.ParseISO8601('2024-03-15T10:30:00');
  WriteLn('Parsed ISO8601: ', TDateTimeUtils.ToISO8601(Dt2));
  
  var Parsed: TDateTime;
  if TDateTimeUtils.TryParse('2024-03-15', 'yyyy-mm-dd', Parsed) then
    WriteLn('TryParse succeeded');
  
  if not TDateTimeUtils.TryParse('invalid', 'yyyy-mm-dd', Parsed) then
    WriteLn('TryParse failed as expected');
  WriteLn('');
end;

procedure ExampleCurrentTime;
begin
  WriteLn('=== Current Time Examples ===');
  
  WriteLn('Now: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.Now, 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('Today: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.Today, 'yyyy-mm-dd'));
  WriteLn('Timestamp: ', TDateTimeUtils.Timestamp);
  WriteLn('Timestamp (ms): ', TDateTimeUtils.TimestampMS);
  WriteLn('');
end;

procedure ExampleDateArithmetic;
begin
  WriteLn('=== Date Arithmetic Examples ===');
  
  var Dt := EncodeDate(2024, 3, 15);
  
  WriteLn('Original: ', TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd'));
  WriteLn('Add 5 days: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.AddDays(Dt, 5), 'yyyy-mm-dd'));
  WriteLn('Add 2 months: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.AddMonths(Dt, 2), 'yyyy-mm-dd'));
  WriteLn('Add 1 year: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.AddYears(Dt, 1), 'yyyy-mm-dd'));
  WriteLn('');
end;

procedure ExampleTimeDifference;
begin
  WriteLn('=== Time Difference Examples ===');
  
  var Start := EncodeDate(2024, 3, 15);
  var EndDate := EncodeDate(2024, 3, 20);
  
  WriteLn('Start: ', TDateTimeUtils.FormatDateTime(Start, 'yyyy-mm-dd'));
  WriteLn('End: ', TDateTimeUtils.FormatDateTime(EndDate, 'yyyy-mm-dd'));
  WriteLn('Days between: ', TDateTimeUtils.DaysBetween(Start, EndDate));
  WriteLn('Weeks between: ', TDateTimeUtils.WeeksBetween(Start, EndDate));
  WriteLn('Months between: ', TDateTimeUtils.MonthsBetween(Start, EndDate));
  WriteLn('');
end;

procedure ExampleDateChecks;
begin
  WriteLn('=== Date Check Examples ===');
  
  var Today := TDateTimeUtils.Today;
  WriteLn('Is today: ', TDateTimeUtils.IsToday(Today));
  
  var Yesterday := TDateTimeUtils.AddDays(Today, -1);
  WriteLn('Is yesterday: ', TDateTimeUtils.IsYesterday(Yesterday));
  
  var Tomorrow := TDateTimeUtils.AddDays(Today, 1);
  WriteLn('Is tomorrow: ', TDateTimeUtils.IsTomorrow(Tomorrow));
  
  WriteLn('Is leap year 2024: ', TDateTimeUtils.IsLeapYear(2024));
  WriteLn('Is leap year 2023: ', TDateTimeUtils.IsLeapYear(2023));
  
  var Saturday := EncodeDate(2024, 3, 16);
  WriteLn('Is weekend (Saturday): ', TDateTimeUtils.IsWeekend(Saturday));
  
  var Monday := EncodeDate(2024, 3, 18);
  WriteLn('Is weekday (Monday): ', TDateTimeUtils.IsWeekday(Monday));
  WriteLn('');
end;

procedure ExamplePeriodBoundaries;
begin
  WriteLn('=== Period Boundary Examples ===');
  
  var Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 0, 0);
  
  WriteLn('Original: ', TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('Start of day: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.StartOfDay(Dt), 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('End of day: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.EndOfDay(Dt), 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('Start of month: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.StartOfMonth(Dt), 'yyyy-mm-dd'));
  WriteLn('End of month: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.EndOfMonth(Dt), 'yyyy-mm-dd'));
  WriteLn('Start of year: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.StartOfYear(Dt), 'yyyy-mm-dd'));
  WriteLn('End of year: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.EndOfYear(Dt), 'yyyy-mm-dd'));
  WriteLn('');
end;

procedure ExampleComponentExtraction;
begin
  WriteLn('=== Component Extraction Examples ===');
  
  var Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 45, 500);
  
  WriteLn('DateTime: ', TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd hh:nn:ss'));
  WriteLn('Year: ', TDateTimeUtils.GetYear(Dt));
  WriteLn('Month: ', TDateTimeUtils.GetMonth(Dt));
  WriteLn('Day: ', TDateTimeUtils.GetDay(Dt));
  WriteLn('Hour: ', TDateTimeUtils.GetHour(Dt));
  WriteLn('Minute: ', TDateTimeUtils.GetMinute(Dt));
  WriteLn('Second: ', TDateTimeUtils.GetSecond(Dt));
  WriteLn('Millisecond: ', TDateTimeUtils.GetMillisecond(Dt));
  WriteLn('Day of week: ', TDateTimeUtils.GetDayOfWeek(Dt));
  WriteLn('Day of year: ', TDateTimeUtils.GetDayOfYear(Dt));
  WriteLn('Week of year: ', TDateTimeUtils.GetWeekOfYear(Dt));
  WriteLn('Quarter: ', TDateTimeUtils.GetQuarter(Dt));
  WriteLn('Days in month: ', TDateTimeUtils.DaysInMonth(2024, 3));
  WriteLn('');
end;

procedure ExampleAgeCalculation;
begin
  WriteLn('=== Age Calculation Examples ===');
  
  var BirthDate := EncodeDate(1990, 6, 15);
  var ReferenceDate := EncodeDate(2024, 6, 15);
  
  WriteLn('Birth date: ', TDateTimeUtils.FormatDateTime(BirthDate, 'yyyy-mm-dd'));
  WriteLn('Reference date: ', TDateTimeUtils.FormatDateTime(ReferenceDate, 'yyyy-mm-dd'));
  WriteLn('Age: ', TDateTimeUtils.CalculateAge(BirthDate, ReferenceDate), ' years');
  WriteLn('Age today: ', TDateTimeUtils.CalculateAgeToday(BirthDate), ' years');
  WriteLn('');
end;

procedure ExampleRelativeTime;
begin
  WriteLn('=== Relative Time Examples ===');
  
  var Now := TDateTimeUtils.Now;
  var FiveMinutesAgo := TDateTimeUtils.AddMinutes(Now, -5);
  var OneHourAgo := TDateTimeUtils.AddHours(Now, -1);
  var Yesterday := TDateTimeUtils.AddDays(Now, -1);
  
  WriteLn('Now: ', TDateTimeUtils.RelativeTime(Now, Now));
  WriteLn('5 minutes ago: ', TDateTimeUtils.RelativeTime(FiveMinutesAgo, Now));
  WriteLn('1 hour ago: ', TDateTimeUtils.RelativeTime(OneHourAgo, Now));
  WriteLn('Yesterday: ', TDateTimeUtils.RelativeTime(Yesterday, Now));
  WriteLn('');
end;

procedure ExampleDurationFormatting;
begin
  WriteLn('=== Duration Formatting Examples ===');
  
  WriteLn('0 seconds: ', TDateTimeUtils.FormatDuration(0));
  WriteLn('45 seconds: ', TDateTimeUtils.FormatDuration(45));
  WriteLn('90 seconds: ', TDateTimeUtils.FormatDuration(90));
  WriteLn('3661 seconds (1h 1m 1s): ', TDateTimeUtils.FormatDuration(3661));
  WriteLn('90061 seconds (1d 1h 1m 1s): ', TDateTimeUtils.FormatDuration(90061));
  WriteLn('');
  
  WriteLn('Short format 3661: ', TDateTimeUtils.FormatDurationShort(3661));
  WriteLn('Short format 90061: ', TDateTimeUtils.FormatDurationShort(90061));
  WriteLn('');
end;

procedure ExampleUtility;
begin
  WriteLn('=== Utility Examples ===');
  
  var Dt1 := EncodeDate(2024, 3, 15);
  var Dt2 := EncodeDate(2024, 3, 20);
  
  WriteLn('Min of two dates: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.Min(Dt1, Dt2), 'yyyy-mm-dd'));
  WriteLn('Max of two dates: ', TDateTimeUtils.FormatDateTime(TDateTimeUtils.Max(Dt1, Dt2), 'yyyy-mm-dd'));
  
  var Dt := EncodeDate(2024, 3, 15);
  WriteLn('Day name: ', TDateTimeUtils.GetDayName(Dt));
  WriteLn('Month name: ', TDateTimeUtils.GetMonthName(Dt));
  WriteLn('Short day name: ', TDateTimeUtils.GetShortDayName(Dt));
  WriteLn('Short month name: ', TDateTimeUtils.GetShortMonthName(Dt));
  WriteLn('');
end;

procedure ExampleValidation;
begin
  WriteLn('=== Validation Examples ===');
  
  WriteLn('Is valid date (2024, 3, 15): ', TDateTimeUtils.IsValidDate(2024, 3, 15));
  WriteLn('Is valid date (2024, 2, 29): ', TDateTimeUtils.IsValidDate(2024, 2, 29));
  WriteLn('Is valid date (2023, 2, 29): ', TDateTimeUtils.IsValidDate(2023, 2, 29));
  WriteLn('Is valid date (2024, 3, 32): ', TDateTimeUtils.IsValidDate(2024, 3, 32));
  WriteLn('Is valid time (10, 30, 45, 500): ', TDateTimeUtils.IsValidTime(10, 30, 45, 500));
  WriteLn('Is valid time (25, 0, 0, 0): ', TDateTimeUtils.IsValidTime(25, 0, 0, 0));
  WriteLn('');
end;

begin
  WriteLn('Delphi DateTime Utilities Examples');
  WriteLn('==================================');
  WriteLn('');
  
  try
    ExampleFormatting;
    ExampleParsing;
    ExampleCurrentTime;
    ExampleDateArithmetic;
    ExampleTimeDifference;
    ExampleDateChecks;
    ExamplePeriodBoundaries;
    ExampleComponentExtraction;
    ExampleAgeCalculation;
    ExampleRelativeTime;
    ExampleDurationFormatting;
    ExampleUtility;
    ExampleValidation;
    
    WriteLn('All examples completed!');
  except
    on E: Exception do
    begin
      WriteLn(Format('Error: %s', [E.Message]));
      Halt(1);
    end;
  end;
end.