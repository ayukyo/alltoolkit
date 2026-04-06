{*******************************************************************************
 * AllToolkit - Delphi DateTime Utilities Test Suite
 * Comprehensive test suite for DateTime utilities
 *******************************************************************************}

program datetime_utils_test;

{$APPTYPE CONSOLE}

uses
  SysUtils, DateUtils, mod;

var
  TestCount: Integer = 0;
  PassCount: Integer = 0;
  FailCount: Integer = 0;

procedure Test(const AName: string; const ACondition: Boolean);
begin
  Inc(TestCount);
  if ACondition then
  begin
    Inc(PassCount);
    WriteLn(Format('[PASS] %s', [AName]));
  end
  else
  begin
    Inc(FailCount);
    WriteLn(Format('[FAIL] %s', [AName]));
  end;
end;

procedure TestFormatting;
var
  Dt: TDateTime;
  S: string;
begin
  WriteLn('--- Testing Formatting ---');
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 45, 0);
  
  S := TDateTimeUtils.ToISO8601(Dt);
  Test('ToISO8601', S = '2024-03-15T10:30:45');
  
  S := TDateTimeUtils.ToRFC3339(Dt);
  Test('ToRFC3339 contains T', Pos('T', S) > 0);
  
  S := TDateTimeUtils.ToUSFormat(Dt);
  Test('ToUSFormat', Pos('03/15/2024', S) > 0);
  
  S := TDateTimeUtils.ToUKFormat(Dt);
  Test('ToUKFormat', Pos('15/03/2024', S) > 0);
  
  S := TDateTimeUtils.ToCompactFormat(Dt);
  Test('ToCompactFormat', S = '20240315103045');
  
  S := TDateTimeUtils.FormatDateTime(Dt, 'yyyy-mm-dd');
  Test('FormatDateTime', S = '2024-03-15');
end;

procedure TestParsing;
var
  Dt: TDateTime;
  Success: Boolean;
begin
  WriteLn('--- Testing Parsing ---');
  
  Dt := TDateTimeUtils.Parse('2024-03-15', 'yyyy-mm-dd');
  Test('Parse date', TDateTimeUtils.GetYear(Dt) = 2024);
  
  Success := TDateTimeUtils.TryParse('2024-03-15', 'yyyy-mm-dd', Dt);
  Test('TryParse success', Success);
  
  Success := TDateTimeUtils.TryParse('invalid', 'yyyy-mm-dd', Dt);
  Test('TryParse failure', not Success);
  
  Dt := TDateTimeUtils.ParseISO8601('2024-03-15T10:30:00');
  Test('ParseISO8601', TDateTimeUtils.GetYear(Dt) = 2024);
end;

procedure TestCurrentTime;
var
  Ts: Int64;
begin
  WriteLn('--- Testing Current Time ---');
  
  Ts := TDateTimeUtils.Timestamp;
  Test('Timestamp is positive', Ts > 0);
  
  Ts := TDateTimeUtils.TimestampMS;
  Test('TimestampMS is positive', Ts > 0);
  
  Test('TimestampMS > Timestamp', TDateTimeUtils.TimestampMS > TDateTimeUtils.Timestamp);
end;

procedure TestTimestampConversion;
var
  Dt, Dt2: TDateTime;
  Ts: Int64;
begin
  WriteLn('--- Testing Timestamp Conversion ---');
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 0, 0);
  Ts := TDateTimeUtils.ToTimestamp(Dt);
  Dt2 := TDateTimeUtils.FromTimestamp(Ts);
  Test('Timestamp round-trip', TDateTimeUtils.IsSameDay(Dt, Dt2));
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 0, 0);
  Ts := TDateTimeUtils.ToTimestampMS(Dt);
  Dt2 := TDateTimeUtils.FromTimestampMS(Ts);
  Test('TimestampMS round-trip', TDateTimeUtils.IsSameDay(Dt, Dt2));
end;

procedure TestDateArithmetic;
var
  Dt, Result: TDateTime;
begin
  WriteLn('--- Testing Date Arithmetic ---');
  
  Dt := EncodeDate(2024, 3, 15);
  Result := TDateTimeUtils.AddDays(Dt, 5);
  Test('AddDays', TDateTimeUtils.GetDay(Result) = 20);
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 0, 0, 0);
  Result := TDateTimeUtils.AddHours(Dt, 5);
  Test('AddHours', TDateTimeUtils.GetHour(Result) = 15);
  
  Dt := EncodeDate(2024, 3, 15);
  Result := TDateTimeUtils.AddMonths(Dt, 2);
  Test('AddMonths', TDateTimeUtils.GetMonth(Result) = 5);
  
  Dt := EncodeDate(2024, 3, 15);
  Result := TDateTimeUtils.AddYears(Dt, 1);
  Test('AddYears', TDateTimeUtils.GetYear(Result) = 2025);
end;

procedure TestTimeDifference;
var
  Start, EndDate: TDateTime;
  Days: Integer;
  Hours: Int64;
begin
  WriteLn('--- Testing Time Difference ---');
  
  Start := EncodeDate(2024, 3, 15);
  EndDate := EncodeDate(2024, 3, 20);
  Days := TDateTimeUtils.DaysBetween(Start, EndDate);
  Test('DaysBetween', Days = 5);
  
  Start := EncodeDate(2024, 3, 15) + EncodeTime(10, 0, 0, 0);
  EndDate := EncodeDate(2024, 3, 15) + EncodeTime(15, 0, 0, 0);
  Hours := TDateTimeUtils.HoursBetween(Start, EndDate);
  Test('HoursBetween', Hours = 5);
end;

procedure TestDateChecks;
var
  Dt: TDateTime;
  Year, Month, Day: Word;
begin
  WriteLn('--- Testing Date Checks ---');
  
  Dt := SysUtils.Date;
  Test('IsToday', TDateTimeUtils.IsToday(Dt));
  
  Dt := DateUtils.IncDay(SysUtils.Date, -1);
  Test('IsYesterday', TDateTimeUtils.IsYesterday(Dt));
  
  Dt := DateUtils.IncDay(SysUtils.Date, 1);
  Test('IsTomorrow', TDateTimeUtils.IsTomorrow(Dt));
  
  Test('IsLeapYear 2024', TDateTimeUtils.IsLeapYear(2024));
  Test('IsLeapYear 2023', not TDateTimeUtils.IsLeapYear(2023));
  
  Dt := EncodeDate(2024, 3, 15);
  Test('IsWeekend Saturday', TDateTimeUtils.IsWeekend(EncodeDate(2024, 3, 16)));
  Test('IsWeekday Monday', TDateTimeUtils.IsWeekday(EncodeDate(2024, 3, 18)));
end;

procedure TestPeriodBoundaries;
var
  Dt, Start, EndDate: TDateTime;
begin
  WriteLn('--- Testing Period Boundaries ---');
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 0, 0);
  Start := TDateTimeUtils.StartOfDay(Dt);
  Test('StartOfDay', TDateTimeUtils.GetHour(Start) = 0);
  
  EndDate := TDateTimeUtils.EndOfDay(Dt);
  Test('EndOfDay hour', TDateTimeUtils.GetHour(EndDate) = 23);
  
  Dt := EncodeDate(2024, 3, 15);
  Start := TDateTimeUtils.StartOfMonth(Dt);
  Test('StartOfMonth', TDateTimeUtils.GetDay(Start) = 1);
  
  EndDate := TDateTimeUtils.EndOfMonth(Dt);
  Test('EndOfMonth', TDateTimeUtils.GetDay(EndDate) = 31);
end;

procedure TestComponentExtraction;
var
  Dt: TDateTime;
begin
  WriteLn('--- Testing Component Extraction ---');
  
  Dt := EncodeDate(2024, 3, 15) + EncodeTime(10, 30, 45, 500);
  
  Test('GetYear', TDateTimeUtils.GetYear(Dt) = 2024);
  Test('GetMonth', TDateTimeUtils.GetMonth(Dt) = 3);
  Test('GetDay', TDateTimeUtils.GetDay(Dt) = 15);
  Test('GetHour', TDateTimeUtils.GetHour(Dt) = 10);
  Test('GetMinute', TDateTimeUtils.GetMinute(Dt) = 30);
  Test('GetSecond', TDateTimeUtils.GetSecond(Dt) = 45);
  Test('GetMillisecond', TDateTimeUtils.GetMillisecond(Dt) = 500);
  Test('GetQuarter', TDateTimeUtils.GetQuarter(Dt) = 1);
  Test('DaysInMonth', TDateTimeUtils.DaysInMonth(2024, 3) = 31);
  Test('DaysInYear leap', TDateTimeUtils.DaysInYear(2024) = 366);
  Test('DaysInYear normal', TDateTimeUtils.DaysInYear(2023) = 365);
end;

procedure TestAgeCalculation;
var
  BirthDate: TDateTime;
  Age: Integer;
begin
  WriteLn('--- Testing Age Calculation ---');
  
  BirthDate := EncodeDate(2000, 1, 1);
  Age := TDateTimeUtils.CalculateAgeToday(BirthDate);
  Test('CalculateAgeToday', Age >= 24);
  
  BirthDate := EncodeDate(1990, 6, 15);
  Age := TDateTimeUtils.CalculateAge(BirthDate, EncodeDate(2024, 6, 15));
  Test('CalculateAge exact', Age = 34);
end;

procedure TestRelativeTime;
var
  Dt: TDateTime;
  S: string;
begin
  WriteLn('--- Testing Relative Time ---');
  
  Dt := SysUtils.Now;
  S := TDateTimeUtils.RelativeTime(Dt, SysUtils.Now);
  Test('RelativeTime now', S = 'just now');
  
  Dt := DateUtils.IncMinute(SysUtils.Now, -5);
  S := TDateTimeUtils.RelativeTime(Dt, SysUtils.Now);
  Test('RelativeTime 5 min ago', Pos('5 minutes ago', S) > 0);
end;

procedure TestDurationFormatting;
var
  S: string;
begin
  WriteLn('--- Testing Duration Formatting ---');
  
  S := TDateTimeUtils.FormatDuration(0);
  Test('FormatDuration 0', S = '0 seconds');
  
  S := TDateTimeUtils.FormatDuration(3661);
  Test('FormatDuration 3661', Pos('1 hour', S) > 0);
  
  S := TDateTimeUtils.FormatDurationShort(3661);
  Test('FormatDurationShort', Pos('h', S) > 0);
end;

procedure TestValidation;
begin
  WriteLn('--- Testing Validation ---');
  
  Test('IsValidDate valid', TDateTimeUtils.IsValidDate(2024, 3, 15));
  Test('IsValidDate invalid day', not TDateTimeUtils.IsValidDate(2024, 3, 32));
  Test('IsValidDate invalid month', not TDateTimeUtils.IsValidDate(2024, 13, 15));
  Test('IsValidTime valid', TDateTimeUtils.IsValidTime(10, 30, 45, 500));
  Test('IsValidTime invalid hour', not TDateTimeUtils.IsValidTime(25, 0, 0, 0));
end;

procedure TestUtility;
var
  Dt1, Dt2, Result: TDateTime;
  S: string;
begin
  WriteLn('--- Testing Utility Functions ---');
  
  Dt1 := EncodeDate(2024, 3, 15);
  Dt2 := EncodeDate(2024, 3, 20);
  Result := TDateTimeUtils.Min(Dt1, Dt2);
  Test('Min', Result = Dt1);
  
  Result := TDateTimeUtils.Max(Dt1, Dt2);
  Test('Max', Result = Dt2);
  
  Dt1 := EncodeDate(2024, 3, 15);
  S := TDateTimeUtils.GetDayName(Dt1);
  Test('GetDayName not empty', Length(S) > 0);
  
  S := TDateTimeUtils.GetMonthName(Dt1);
  Test('GetMonthName not empty', Length(S) > 0);
end;

procedure PrintSummary;
begin
  WriteLn('');
  WriteLn('========================================');
  WriteLn(Format('Total Tests: %d', [TestCount]));
  WriteLn(Format('Passed: %d', [PassCount]));
  WriteLn(Format('Failed: %d', [FailCount]));
  WriteLn('========================================');
  
  if FailCount = 0 then
    WriteLn('All tests passed!')
  else
    WriteLn(Format('%d test(s) failed.', [FailCount]));
end;

begin
  WriteLn('Delphi DateTime Utilities Test Suite');
  WriteLn('====================================');
  WriteLn('');
  
  try
    TestFormatting;
    TestParsing;
    TestCurrentTime;
    TestTimestampConversion;
    TestDateArithmetic;
    TestTimeDifference;
    TestDateChecks;
    TestPeriodBoundaries;
    TestComponentExtraction;
    TestAgeCalculation;
    TestRelativeTime;
    TestDurationFormatting;
    TestValidation;
    TestUtility;
    
    PrintSummary;
  except
    on E: Exception do
    begin
      WriteLn(Format('Test suite error: %s', [E.Message]));
      Halt(1);
    end;
  end;
  
  if FailCount > 0 then
    Halt(1)
  else
    Halt(0);
end.