{*******************************************************************************
 * AllToolkit - Delphi DateTime Utilities
 * A comprehensive date and time manipulation utility module
 * Zero dependencies, uses only Delphi standard library
 *******************************************************************************}

unit mod;

interface

uses
  SysUtils, DateUtils;

type
  { DateTime utility record }
  TDateTimeUtils = record
    { Formatting }
    class function FormatDateTime(const ADateTime: TDateTime; const AFormat: string): string; static;
    class function ToISO8601(const ADateTime: TDateTime): string; static;
    class function ToRFC3339(const ADateTime: TDateTime): string; static;
    class function ToChineseFormat(const ADateTime: TDateTime): string; static;
    class function ToUSFormat(const ADateTime: TDateTime): string; static;
    class function ToUKFormat(const ADateTime: TDateTime): string; static;
    class function ToCompactFormat(const ADateTime: TDateTime): string; static;
    
    { Parsing }
    class function Parse(const ADateString: string; const AFormat: string): TDateTime; static;
    class function ParseISO8601(const ADateString: string): TDateTime; static;
    class function TryParse(const ADateString: string; const AFormat: string; out ADateTime: TDateTime): Boolean; static;
    class function TryParseISO8601(const ADateString: string; out ADateTime: TDateTime): Boolean; static;
    
    { Current Time }
    class function Now: TDateTime; static;
    class function NowUTC: TDateTime; static;
    class function Today: TDateTime; static;
    class function Timestamp: Int64; static;
    class function TimestampMS: Int64; static;
    
    { Timestamp Conversion }
    class function FromTimestamp(const ATimestamp: Int64): TDateTime; static;
    class function FromTimestampMS(const ATimestampMS: Int64): TDateTime; static;
    class function ToTimestamp(const ADateTime: TDateTime): Int64; static;
    class function ToTimestampMS(const ADateTime: TDateTime): Int64; static;
    
    { Date Arithmetic }
    class function AddDays(const ADateTime: TDateTime; const ADays: Integer): TDateTime; static;
    class function AddHours(const ADateTime: TDateTime; const AHours: Integer): TDateTime; static;
    class function AddMinutes(const ADateTime: TDateTime; const AMinutes: Integer): TDateTime; static;
    class function AddSeconds(const ADateTime: TDateTime; const ASeconds: Integer): TDateTime; static;
    class function AddMonths(const ADateTime: TDateTime; const AMonths: Integer): TDateTime; static;
    class function AddYears(const ADateTime: TDateTime; const AYears: Integer): TDateTime; static;
    class function AddWeeks(const ADateTime: TDateTime; const AWeeks: Integer): TDateTime; static;
    
    { Time Difference }
    class function DaysBetween(const AStart, AEnd: TDateTime): Integer; static;
    class function HoursBetween(const AStart, AEnd: TDateTime): Int64; static;
    class function MinutesBetween(const AStart, AEnd: TDateTime): Int64; static;
    class function SecondsBetween(const AStart, AEnd: TDateTime): Int64; static;
    class function MilliSecondsBetween(const AStart, AEnd: TDateTime): Int64; static;
    class function WeeksBetween(const AStart, AEnd: TDateTime): Integer; static;
    class function MonthsBetween(const AStart, AEnd: TDateTime): Integer; static;
    class function YearsBetween(const AStart, AEnd: TDateTime): Integer; static;
    
    { Date Checks }
    class function IsToday(const ADateTime: TDateTime): Boolean; static;
    class function IsYesterday(const ADateTime: TDateTime): Boolean; static;
    class function IsTomorrow(const ADateTime: TDateTime): Boolean; static;
    class function IsThisWeek(const ADateTime: TDateTime): Boolean; static;
    class function IsThisMonth(const ADateTime: TDateTime): Boolean; static;
    class function IsThisYear(const ADateTime: TDateTime): Boolean; static;
    class function IsWeekend(const ADateTime: TDateTime): Boolean; static;
    class function IsWeekday(const ADateTime: TDateTime): Boolean; static;
    class function IsLeapYear(const AYear: Integer): Boolean; static;
    class function IsSameDay(const ADate1, ADate2: TDateTime): Boolean; static;
    class function IsAM(const ADateTime: TDateTime): Boolean; static;
    class function IsPM(const ADateTime: TDateTime): Boolean; static;
    
    { Period Boundaries }
    class function StartOfDay(const ADateTime: TDateTime): TDateTime; static;
    class function EndOfDay(const ADateTime: TDateTime): TDateTime; static;
    class function StartOfWeek(const ADateTime: TDateTime): TDateTime; static;
    class function EndOfWeek(const ADateTime: TDateTime): TDateTime; static;
    class function StartOfMonth(const ADateTime: TDateTime): TDateTime; static;
    class function EndOfMonth(const ADateTime: TDateTime): TDateTime; static;
    class function StartOfYear(const ADateTime: TDateTime): TDateTime; static;
    class function EndOfYear(const ADateTime: TDateTime): TDateTime; static;
    class function StartOfQuarter(const ADateTime: TDateTime): TDateTime; static;
    class function EndOfQuarter(const ADateTime: TDateTime): TDateTime; static;
    
    { Component Extraction }
    class function GetYear(const ADateTime: TDateTime): Integer; static;
    class function GetMonth(const ADateTime: TDateTime): Integer; static;
    class function GetDay(const ADateTime: TDateTime): Integer; static;
    class function GetHour(const ADateTime: TDateTime): Integer; static;
    class function GetMinute(const ADateTime: TDateTime): Integer; static;
    class function GetSecond(const ADateTime: TDateTime): Integer; static;
    class function GetMillisecond(const ADateTime: TDateTime): Integer; static;
    class function GetDayOfWeek(const ADateTime: TDateTime): Integer; static;
    class function GetDayOfYear(const ADateTime: TDateTime): Integer; static;
    class function GetWeekOfYear(const ADateTime: TDateTime): Integer; static;
    class function GetQuarter(const ADateTime: TDateTime): Integer; static;
    class function DaysInMonth(const AYear, AMonth: Integer): Integer; static;
    class function DaysInYear(const AYear: Integer): Integer; static;
    
    { Component Modification }
    class function SetYear(const ADateTime: TDateTime; const AYear: Integer): TDateTime; static;
    class function SetMonth(const ADateTime: TDateTime; const AMonth: Integer): TDateTime; static;
    class function SetDay(const ADateTime: TDateTime; const ADay: Integer): TDateTime; static;
    class function SetHour(const ADateTime: TDateTime; const AHour: Integer): TDateTime; static;
    class function SetMinute(const ADateTime: TDateTime; const AMinute: Integer): TDateTime; static;
    class function SetSecond(const ADateTime: TDateTime; const ASecond: Integer): TDateTime; static;
    
    { Age Calculation }
    class function CalculateAge(const ABirthDate: TDateTime; const AReferenceDate: TDateTime): Integer; static;
    class function CalculateAgeToday(const ABirthDate: TDateTime): Integer; static;
    
    { Relative Time }
    class function RelativeTime(const ADateTime: TDateTime; const AReferenceDate: TDateTime = 0): string; static;
    class function TimeAgo(const ADateTime: TDateTime): string; static;
    
    { Duration Formatting }
    class function FormatDuration(const ASeconds: Int64): string; static;
    class function FormatDurationShort(const ASeconds: Int64): string; static;
    class function FormatDurationMS(const AMilliseconds: Int64): string; static;
    
    { Time Zone }
    class function LocalToUTC(const ADateTime: TDateTime): TDateTime; static;
    class function UTCToLocal(const ADateTime: TDateTime): TDateTime; static;
    class function GetTimeZoneOffset: Integer; static;
    
    { Validation }
    class function IsValidDate(const AYear, AMonth, ADay: Integer): Boolean; static;
    class function IsValidTime(const AHour, AMinute, ASecond, AMillisecond: Integer): Boolean; static;
    
    { Utility }
    class function Min(const ADateTime1, ADateTime2: TDateTime): TDateTime; static;
    class function Max(const ADateTime1, ADateTime2: TDateTime): TDateTime; static;
    class function Clamp(const ADateTime, AMin, AMax: TDateTime): TDateTime; static;
    class function GetDayName(const ADateTime: TDateTime): string; static;
    class function GetMonthName(const ADateTime: TDateTime): string; static;
    class function GetShortDayName(const ADateTime: TDateTime): string; static;
    class function GetShortMonthName(const ADateTime: TDateTime): string; static;
  end;

const
  { Format constants }
  FORMAT_ISO8601 = 'yyyy-mm-dd"T"hh:nn:ss';
  FORMAT_ISO8601_MS = 'yyyy-mm-dd"T"hh:nn:ss.zzz';
  FORMAT_RFC3339 = 'yyyy-mm-dd"T"hh:nn:ss.zzz"Z"';
  FORMAT_CHINESE = 'yyyy"年"mm"月"dd"日" hh"时"nn"分"ss"秒"';
  FORMAT_US = 'mm/dd/yyyy hh:nn:ss';
  FORMAT_UK = 'dd/mm/yyyy hh:nn:ss';
  FORMAT_COMPACT = 'yyyymmddhhnnss';
  FORMAT_DATE_ONLY = 'yyyy-mm-dd';
  FORMAT_TIME_ONLY = 'hh:nn:ss';

implementation

{*******************************************************************************
 * Formatting Functions
 *******************************************************************************}

class function TDateTimeUtils.FormatDateTime(const ADateTime: TDateTime; const AFormat: string): string;
begin
  Result := SysUtils.FormatDateTime(AFormat, ADateTime);
end;

class function TDateTimeUtils.ToISO8601(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_ISO8601, ADateTime);
end;

class function TDateTimeUtils.ToRFC3339(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_ISO8601_MS, ADateTime) + 'Z';
end;

class function TDateTimeUtils.ToChineseFormat(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_CHINESE, ADateTime);
end;

class function TDateTimeUtils.ToUSFormat(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_US, ADateTime);
end;

class function TDateTimeUtils.ToUKFormat(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_UK, ADateTime);
end;

class function TDateTimeUtils.ToCompactFormat(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime(FORMAT_COMPACT, ADateTime);
end;

{*******************************************************************************
 * Parsing Functions
 *******************************************************************************}

class function TDateTimeUtils.Parse(const ADateString: string; const AFormat: string): TDateTime;
begin
  Result := StrToDateTimeDef(ADateString, 0, AFormat);
  if Result = 0 then
    raise EConvertError.CreateFmt('Cannot parse date: %s with format: %s', [ADateString, AFormat]);
end;

class function TDateTimeUtils.ParseISO8601(const ADateString: string): TDateTime;
begin
  Result := Parse(ADateString, FORMAT_ISO8601);
end;

class function TDateTimeUtils.TryParse(const ADateString: string; const AFormat: string; out ADateTime: TDateTime): Boolean;
begin
  try
    ADateTime := StrToDateTimeDef(ADateString, 0, AFormat);
    Result := ADateTime <> 0;
  except
    ADateTime := 0;
    Result := False;
  end;
end;

class function TDateTimeUtils.TryParseISO8601(const ADateString: string; out ADateTime: TDateTime): Boolean;
begin
  Result := TryParse(ADateString, FORMAT_ISO8601, ADateTime);
end;

{*******************************************************************************
 * Current Time Functions
 *******************************************************************************}

class function TDateTimeUtils.Now: TDateTime;
begin
  Result := SysUtils.Now;
end;

class function TDateTimeUtils.NowUTC: TDateTime;
begin
  Result := DateUtils.TTimeZone.Local.ToUniversalTime(SysUtils.Now);
end;

class function TDateTimeUtils.Today: TDateTime;
begin
  Result := SysUtils.Date;
end;

class function TDateTimeUtils.Timestamp: Int64;
begin
  Result := Trunc(DateTimeToUnix(SysUtils.Now));
end;

class function TDateTimeUtils.TimestampMS: Int64;
begin
  Result := Trunc(DateTimeToUnix(SysUtils.Now) * 1000);
end;

{*******************************************************************************
 * Timestamp Conversion Functions
 *******************************************************************************}

class function TDateTimeUtils.FromTimestamp(const ATimestamp: Int64): TDateTime;
begin
  Result := UnixToDateTime(ATimestamp);
end;

class function TDateTimeUtils.FromTimestampMS(const ATimestampMS: Int64): TDateTime;
begin
  Result := UnixToDateTime(ATimestampMS div 1000);
end;

class function TDateTimeUtils.ToTimestamp(const ADateTime: TDateTime): Int64;
begin
  Result := Trunc(DateTimeToUnix(ADateTime));
end;

class function TDateTimeUtils.ToTimestampMS(const ADateTime: TDateTime): Int64;
begin
  Result := Trunc(DateTimeToUnix(ADateTime) * 1000);
end;

{*******************************************************************************
 * Date Arithmetic Functions
 *******************************************************************************}

class function TDateTimeUtils.AddDays(const ADateTime: TDateTime; const ADays: Integer): TDateTime;
begin
  Result := DateUtils.IncDay(ADateTime, ADays);
end;

class function TDateTimeUtils.AddHours(const ADateTime: TDateTime; const AHours: Integer): TDateTime;
begin
  Result := DateUtils.IncHour(ADateTime, AHours);
end;

class function TDateTimeUtils.AddMinutes(const ADateTime: TDateTime; const AMinutes: Integer): TDateTime;
begin
  Result := DateUtils.IncMinute(ADateTime, AMinutes);
end;

class function TDateTimeUtils.AddSeconds(const ADateTime: TDateTime; const ASeconds: Integer): TDateTime;
begin
  Result := DateUtils.IncSecond(ADateTime, ASeconds);
end;

class function TDateTimeUtils.AddMonths(const ADateTime: TDateTime; const AMonths: Integer): TDateTime;
begin
  Result := DateUtils.IncMonth(ADateTime, AMonths);
end;

class function TDateTimeUtils.AddYears(const ADateTime: TDateTime; const AYears: Integer): TDateTime;
begin
  Result := DateUtils.IncYear(ADateTime, AYears);
end;

class function TDateTimeUtils.AddWeeks(const ADateTime: TDateTime; const AWeeks: Integer): TDateTime;
begin
  Result := DateUtils.IncWeek(ADateTime, AWeeks);
end;

{*******************************************************************************
 * Time Difference Functions
 *******************************************************************************}

class function TDateTimeUtils.DaysBetween(const AStart, AEnd: TDateTime): Integer;
begin
  Result := DateUtils.DaysBetween(AStart, AEnd);
end;

class function TDateTimeUtils.HoursBetween(const AStart, AEnd: TDateTime): Int64;
begin
  Result := DateUtils.HoursBetween(AStart, AEnd);
end;

class function TDateTimeUtils.MinutesBetween(const AStart, AEnd: TDateTime): Int64;
begin
  Result := DateUtils.MinutesBetween(AStart, AEnd);
end;

class function TDateTimeUtils.SecondsBetween(const AStart, AEnd: TDateTime): Int64;
begin
  Result := DateUtils.SecondsBetween(AStart, AEnd);
end;

class function TDateTimeUtils.MilliSecondsBetween(const AStart, AEnd: TDateTime): Int64;
begin
  Result := DateUtils.MilliSecondsBetween(AStart, AEnd);
end;

class function TDateTimeUtils.WeeksBetween(const AStart, AEnd: TDateTime): Integer;
begin
  Result := DateUtils.WeeksBetween(AStart, AEnd);
end;

class function TDateTimeUtils.MonthsBetween(const AStart, AEnd: TDateTime): Integer;
begin
  Result := DateUtils.MonthsBetween(AStart, AEnd);
end;

class function TDateTimeUtils.YearsBetween(const AStart, AEnd: TDateTime): Integer;
begin
  Result := DateUtils.YearsBetween(AStart, AEnd);
end;

{*******************************************************************************
 * Date Checks Functions
 *******************************************************************************}

class function TDateTimeUtils.IsToday(const ADateTime: TDateTime): Boolean;
begin
  Result := IsSameDay(ADateTime, SysUtils.Date);
end;

class function TDateTimeUtils.IsYesterday(const ADateTime: TDateTime): Boolean;
begin
  Result := IsSameDay(ADateTime, DateUtils.IncDay(SysUtils.Date, -1));
end;

class function TDateTimeUtils.IsTomorrow(const ADateTime: TDateTime): Boolean;
begin
  Result := IsSameDay(ADateTime, DateUtils.IncDay(SysUtils.Date, 1));
end;

class function TDateTimeUtils.IsThisWeek(const ADateTime: TDateTime): Boolean;
var
  StartOfWeek, EndOfWeek: TDateTime;
begin
  StartOfWeek := DateUtils.StartOfTheWeek(SysUtils.Date);
  EndOfWeek := DateUtils.EndOfTheWeek(SysUtils.Date);
  Result := (ADateTime >= StartOfWeek) and (ADateTime <= EndOfWeek);
end;

class function TDateTimeUtils.IsThisMonth(const ADateTime: TDateTime): Boolean;
var
  StartOfMonth, EndOfMonth: TDateTime;
begin
  StartOfMonth := DateUtils.StartOfTheMonth(SysUtils.Date);
  EndOfMonth := DateUtils.EndOfTheMonth(SysUtils.Date);
  Result := (ADateTime >= StartOfMonth) and (ADateTime <= EndOfMonth);
end;

class function TDateTimeUtils.IsThisYear(const ADateTime: TDateTime): Boolean;
begin
  Result := GetYear(ADateTime) = GetYear(SysUtils.Date);
end;

class function TDateTimeUtils.IsWeekend(const ADateTime: TDateTime): Boolean;
var
  DayOfWeek: Integer;
begin
  DayOfWeek := GetDayOfWeek(ADateTime);
  Result := (DayOfWeek = DaySaturday) or (DayOfWeek = DaySunday);
end;

class function TDateTimeUtils.IsWeekday(const ADateTime: TDateTime): Boolean;
begin
  Result := not IsWeekend(ADateTime);
end;

class function TDateTimeUtils.IsLeapYear(const AYear: Integer): Boolean;
begin
  Result := DateUtils.IsLeapYear(AYear);
end;

class function TDateTimeUtils.IsSameDay(const ADate1, ADate2: TDateTime): Boolean;
begin
  Result := DateUtils.IsSameDay(ADate1, ADate2);
end;

class function TDateTimeUtils.IsAM(const ADateTime: TDateTime): Boolean;
begin
  Result := GetHour(ADateTime) < 12;
end;

class function TDateTimeUtils.IsPM(const ADateTime: TDateTime): Boolean;
begin
  Result := GetHour(ADateTime) >= 12;
end;

{*******************************************************************************
 * Period Boundaries Functions
 *******************************************************************************}

class function TDateTimeUtils.StartOfDay(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.StartOfTheDay(ADateTime);
end;

class function TDateTimeUtils.EndOfDay(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.EndOfTheDay(ADateTime);
end;

class function TDateTimeUtils.StartOfWeek(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.StartOfTheWeek(ADateTime);
end;

class function TDateTimeUtils.EndOfWeek(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.EndOfTheWeek(ADateTime);
end;

class function TDateTimeUtils.StartOfMonth(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.StartOfTheMonth(ADateTime);
end;

class function TDateTimeUtils.EndOfMonth(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.EndOfTheMonth(ADateTime);
end;

class function TDateTimeUtils.StartOfYear(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.StartOfTheYear(ADateTime);
end;

class function TDateTimeUtils.EndOfYear(const ADateTime: TDateTime): TDateTime;
begin
  Result := DateUtils.EndOfTheYear(ADateTime);
end;

class function TDateTimeUtils.StartOfQuarter(const ADateTime: TDateTime): TDateTime;
var
  Year, Month, Day: Word;
  QuarterStartMonth: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  QuarterStartMonth := ((Month - 1) div 3) * 3 + 1;
  Result := EncodeDate(Year, QuarterStartMonth, 1);
end;

class function TDateTimeUtils.EndOfQuarter(const ADateTime: TDateTime): TDateTime;
var
  Year, Month, Day: Word;
  QuarterEndMonth: Integer;
  DaysInEndMonth: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  QuarterEndMonth := ((Month - 1) div 3) * 3 + 3;
  DaysInEndMonth := DaysInMonth(Year, QuarterEndMonth);
  Result := EncodeDate(Year, QuarterEndMonth, DaysInEndMonth);
end;

{*******************************************************************************
 * Component Extraction Functions
 *******************************************************************************}

class function TDateTimeUtils.GetYear(const ADateTime: TDateTime): Integer;
var
  Year, Month, Day: Word;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  Result := Year;
end;

class function TDateTimeUtils.GetMonth(const ADateTime: TDateTime): Integer;
var
  Year, Month, Day: Word;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  Result := Month;
end;

class function TDateTimeUtils.GetDay(const ADateTime: TDateTime): Integer;
var
  Year, Month, Day: Word;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  Result := Day;
end;

class function TDateTimeUtils.GetHour(const ADateTime: TDateTime): Integer;
var
  Hour, Min, Sec, MSec: Word;
begin
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  Result := Hour;
end;

class function TDateTimeUtils.GetMinute(const ADateTime: TDateTime): Integer;
var
  Hour, Min, Sec, MSec: Word;
begin
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  Result := Min;
end;

class function TDateTimeUtils.GetSecond(const ADateTime: TDateTime): Integer;
var
  Hour, Min, Sec, MSec: Word;
begin
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  Result := Sec;
end;

class function TDateTimeUtils.GetMillisecond(const ADateTime: TDateTime): Integer;
var
  Hour, Min, Sec, MSec: Word;
begin
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  Result := MSec;
end;

class function TDateTimeUtils.GetDayOfWeek(const ADateTime: TDateTime): Integer;
begin
  Result := DayOfWeek(ADateTime);
end;

class function TDateTimeUtils.GetDayOfYear(const ADateTime: TDateTime): Integer;
begin
  Result := DateUtils.DayOfTheYear(ADateTime);
end;

class function TDateTimeUtils.GetWeekOfYear(const ADateTime: TDateTime): Integer;
begin
  Result := DateUtils.WeekOfTheYear(ADateTime);
end;

class function TDateTimeUtils.GetQuarter(const ADateTime: TDateTime): Integer;
var
  Month: Integer;
begin
  Month := GetMonth(ADateTime);
  Result := (Month - 1) div 3 + 1;
end;

class function TDateTimeUtils.DaysInMonth(const AYear, AMonth: Integer): Integer;
begin
  Result := DateUtils.DaysInAMonth(AYear, AMonth);
end;

class function TDateTimeUtils.DaysInYear(const AYear: Integer): Integer;
begin
  if IsLeapYear(AYear) then
    Result := 366
  else
    Result := 365;
end;

{*******************************************************************************
 * Component Modification Functions
 *******************************************************************************}

class function TDateTimeUtils.SetYear(const ADateTime: TDateTime; const AYear: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  Result := EncodeDate(AYear, Month, Day) + EncodeTime(Hour, Min, Sec, MSec);
end;

class function TDateTimeUtils.SetMonth(const ADateTime: TDateTime; const AMonth: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
  NewMonth: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  NewMonth := AMonth;
  if NewMonth < 1 then NewMonth := 1;
  if NewMonth > 12 then NewMonth := 12;
  Result := EncodeDate(Year, NewMonth, Day) + EncodeTime(Hour, Min, Sec, MSec);
end;

class function TDateTimeUtils.SetDay(const ADateTime: TDateTime; const ADay: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
  MaxDay: Integer;
  NewDay: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  MaxDay := DaysInMonth(Year, Month);
  NewDay := ADay;
  if NewDay < 1 then NewDay := 1;
  if NewDay > MaxDay then NewDay := MaxDay;
  Result := EncodeDate(Year, Month, NewDay) + EncodeTime(Hour, Min, Sec, MSec);
end;

class function TDateTimeUtils.SetHour(const ADateTime: TDateTime; const AHour: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
  NewHour: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  NewHour := AHour;
  if NewHour < 0 then NewHour := 0;
  if NewHour > 23 then NewHour := 23;
  Result := EncodeDate(Year, Month, Day) + EncodeTime(NewHour, Min, Sec, MSec);
end;

class function TDateTimeUtils.SetMinute(const ADateTime: TDateTime; const AMinute: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
  NewMinute: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  NewMinute := AMinute;
  if NewMinute < 0 then NewMinute := 0;
  if NewMinute > 59 then NewMinute := 59;
  Result := EncodeDate(Year, Month, Day) + EncodeTime(Hour, NewMinute, Sec, MSec);
end;

class function TDateTimeUtils.SetSecond(const ADateTime: TDateTime; const ASecond: Integer): TDateTime;
var
  Year, Month, Day: Word;
  Hour, Min, Sec, MSec: Word;
  NewSecond: Integer;
begin
  DecodeDate(ADateTime, Year, Month, Day);
  DecodeTime(ADateTime, Hour, Min, Sec, MSec);
  NewSecond := ASecond;
  if NewSecond < 0 then NewSecond := 0;
  if NewSecond > 59 then NewSecond := 59;
  Result := EncodeDate(Year, Month, Day) + EncodeTime(Hour, Min, NewSecond, MSec);
end;

{*******************************************************************************
 * Age Calculation Functions
 *******************************************************************************}

class function TDateTimeUtils.CalculateAge(const ABirthDate: TDateTime; const AReferenceDate: TDateTime): Integer;
var
  BirthYear, BirthMonth, BirthDay: Word;
  RefYear, RefMonth, RefDay: Word;
  Age: Integer;
begin
  DecodeDate(ABirthDate, BirthYear, BirthMonth, BirthDay);
  DecodeDate(AReferenceDate, RefYear, RefMonth, RefDay);
  
  Age := RefYear - BirthYear;
  
  if (RefMonth < BirthMonth) or
     ((RefMonth = BirthMonth) and (RefDay < BirthDay)) then
    Dec(Age);
    
  Result := Age;
end;

class function TDateTimeUtils.CalculateAgeToday(const ABirthDate: TDateTime): Integer;
begin
  Result := CalculateAge(ABirthDate, SysUtils.Date);
end;

{*******************************************************************************
 * Relative Time Functions
 *******************************************************************************}

class function TDateTimeUtils.RelativeTime(const ADateTime: TDateTime; const AReferenceDate: TDateTime = 0): string;
var
  RefDate: TDateTime;
  DiffSeconds: Int64;
  DiffMinutes: Int64;
  DiffHours: Int64;
  DiffDays: Int64;
  DiffMonths: Int64;
  DiffYears: Int64;
begin
  if AReferenceDate = 0 then
    RefDate := SysUtils.Now
  else
    RefDate := AReferenceDate;
    
  DiffSeconds := SecondsBetween(ADateTime, RefDate);
  DiffMinutes := DiffSeconds div 60;
  DiffHours := DiffMinutes div 60;
  DiffDays := DaysBetween(ADateTime, RefDate);
  DiffMonths := MonthsBetween(ADateTime, RefDate);
  DiffYears := YearsBetween(ADateTime, RefDate);
  
  if ADateTime > RefDate then
  begin
    { Future }
    if DiffSeconds < 60 then
      Result := 'in a few seconds'
    else if DiffMinutes < 60 then
      Result := Format('in %d minutes', [DiffMinutes])
    else if DiffHours < 24 then
      Result := Format('in %d hours', [DiffHours])
    else if DiffDays < 30 then
      Result := Format('in %d days', [DiffDays])
    else if DiffMonths < 12 then
      Result := Format('in %d months', [DiffMonths])
    else
      Result := Format('in %d years', [DiffYears]);
  end
  else
  begin
    { Past }
    if DiffSeconds < 60 then
      Result := 'just now'
    else if DiffMinutes < 60 then
      Result := Format('%d minutes ago', [DiffMinutes])
    else if DiffHours < 24 then
      Result := Format('%d hours ago', [DiffHours])
    else if DiffDays = 1 then
      Result := 'yesterday'
    else if DiffDays < 7 then
      Result := Format('%d days ago', [DiffDays])
    else if DiffDays < 30 then
      Result := Format('%d weeks ago', [DiffDays div 7])
    else if DiffMonths < 12 then
      Result := Format('%d months ago', [DiffMonths])
    else
      Result := Format('%d years ago', [DiffYears]);
  end;
end;

class function TDateTimeUtils.TimeAgo(const ADateTime: TDateTime): string;
begin
  Result := RelativeTime(ADateTime, SysUtils.Now);
end;

{*******************************************************************************
 * Duration Formatting Functions
 *******************************************************************************}

class function TDateTimeUtils.FormatDuration(const ASeconds: Int64): string;
var
  Days, Hours, Minutes, Seconds: Int64;
  Parts: array of string;
  I: Integer;
begin
  if ASeconds = 0 then
  begin
    Result := '0 seconds';
    Exit;
  end;
  
  Days := ASeconds div 86400;
  Hours := (ASeconds mod 86400) div 3600;
  Minutes := (ASeconds mod 3600) div 60;
  Seconds := ASeconds mod 60;
  
  SetLength(Parts, 0);
  
  if Days > 0 then
  begin
    if Days = 1 then
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := '1 day';
    else
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := Format('%d days', [Days]);
  end;
  
  if Hours > 0 then
  begin
    if Hours = 1 then
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := '1 hour';
    else
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := Format('%d hours', [Hours]);
  end;
  
  if Minutes > 0 then
  begin
    if Minutes = 1 then
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := '1 minute';
    else
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := Format('%d minutes', [Minutes]);
  end;
  
  if Seconds > 0 then
  begin
    if Seconds = 1 then
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := '1 second';
    else
      SetLength(Parts, Length(Parts) + 1);
      Parts[High(Parts)] := Format('%d seconds', [Seconds]);
  end;
  
  Result := '';
  for I := 0 to High(Parts) do
  begin
    if I > 0 then
    begin
      if I = High(Parts) then
        Result := Result + ' and '
      else
        Result := Result + ', ';
    end;
    Result := Result + Parts[I];
  end;
end;

class function TDateTimeUtils.FormatDurationShort(const ASeconds: Int64): string;
var
  Days, Hours, Minutes, Seconds: Int64;
  Parts: array of string;
  I: Integer;
begin
  if ASeconds = 0 then
  begin
    Result := '0s';
    Exit;
  end;
  
  Days := ASeconds div 86400;
  Hours := (ASeconds mod 86400) div 3600;
  Minutes := (ASeconds mod 3600) div 60;
  Seconds := ASeconds mod 60;
  
  SetLength(Parts, 0);
  
  if Days > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dd', [Days]);
  end;
  
  if Hours > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dh', [Hours]);
  end;
  
  if Minutes > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dm', [Minutes]);
  end;
  
  if Seconds > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%ds', [Seconds]);
  end;
  
  Result := '';
  for I := 0 to High(Parts) do
  begin
    if I > 0 then
      Result := Result + ' ';
    Result := Result + Parts[I];
  end;
end;

class function TDateTimeUtils.FormatDurationMS(const AMilliseconds: Int64): string;
var
  Days, Hours, Minutes, Seconds, Millis: Int64;
  Parts: array of string;
  I: Integer;
begin
  if AMilliseconds = 0 then
  begin
    Result := '0ms';
    Exit;
  end;
  
  Days := AMilliseconds div 86400000;
  Hours := (AMilliseconds mod 86400000) div 3600000;
  Minutes := (AMilliseconds mod 3600000) div 60000;
  Seconds := (AMilliseconds mod 60000) div 1000;
  Millis := AMilliseconds mod 1000;
  
  SetLength(Parts, 0);
  
  if Days > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dd', [Days]);
  end;
  
  if Hours > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dh', [Hours]);
  end;
  
  if Minutes > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dm', [Minutes]);
  end;
  
  if Seconds > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%ds', [Seconds]);
  end;
  
  if Millis > 0 then
  begin
    SetLength(Parts, Length(Parts) + 1);
    Parts[High(Parts)] := Format('%dms', [Millis]);
  end;
  
  Result := '';
  for I := 0 to High(Parts) do
  begin
    if I > 0 then
      Result := Result + ' ';
    Result := Result + Parts[I];
  end;
end;

{*******************************************************************************
 * Time Zone Functions
 *******************************************************************************}

class function TDateTimeUtils.LocalToUTC(const ADateTime: TDateTime): TDateTime;
begin
  Result := TTimeZone.Local.ToUniversalTime(ADateTime);
end;

class function TDateTimeUtils.UTCToLocal(const ADateTime: TDateTime): TDateTime;
begin
  Result := TTimeZone.Local.ToLocalTime(ADateTime);
end;

class function TDateTimeUtils.GetTimeZoneOffset: Integer;
begin
  Result := TTimeZone.Local.GetUtcOffset(SysUtils.Now).Hours;
end;

{*******************************************************************************
 * Validation Functions
 *******************************************************************************}

class function TDateTimeUtils.IsValidDate(const AYear, AMonth, ADay: Integer): Boolean;
begin
  Result := (AYear > 0) and (AMonth >= 1) and (AMonth <= 12) and
            (ADay >= 1) and (ADay <= DaysInMonth(AYear, AMonth));
end;

class function TDateTimeUtils.IsValidTime(const AHour, AMinute, ASecond, AMillisecond: Integer): Boolean;
begin
  Result := (AHour >= 0) and (AHour <= 23) and
            (AMinute >= 0) and (AMinute <= 59) and
            (ASecond >= 0) and (ASecond <= 59) and
            (AMillisecond >= 0) and (AMillisecond <= 999);
end;

{*******************************************************************************
 * Utility Functions
 *******************************************************************************}

class function TDateTimeUtils.Min(const ADateTime1, ADateTime2: TDateTime): TDateTime;
begin
  if ADateTime1 < ADateTime2 then
    Result := ADateTime1
  else
    Result := ADateTime2;
end;

class function TDateTimeUtils.Max(const ADateTime1, ADateTime2: TDateTime): TDateTime;
begin
  if ADateTime1 > ADateTime2 then
    Result := ADateTime1
  else
    Result := ADateTime2;
end;

class function TDateTimeUtils.Clamp(const ADateTime, AMin, AMax: TDateTime): TDateTime;
begin
  if ADateTime < AMin then
    Result := AMin
  else if ADateTime > AMax then
    Result := AMax
  else
    Result := ADateTime;
end;

class function TDateTimeUtils.GetDayName(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime('dddd', ADateTime);
end;

class function TDateTimeUtils.GetMonthName(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime('mmmm', ADateTime);
end;

class function TDateTimeUtils.GetShortDayName(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime('ddd', ADateTime);
end;

class function TDateTimeUtils.GetShortMonthName(const ADateTime: TDateTime): string;
begin
  Result := FormatDateTime('mmm', ADateTime);
end;

end.