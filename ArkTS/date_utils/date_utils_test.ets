/**
 * Date Utilities Test Suite for ArkTS
 * 
 * Comprehensive tests for the date_utils module with high coverage.
 */

import {
  // Constants
  MILLIS_PER_SECOND, MILLIS_PER_MINUTE, MILLIS_PER_HOUR, MILLIS_PER_DAY, MILLIS_PER_WEEK,
  MONTH_NAMES_EN, MONTH_NAMES_SHORT_EN, DAY_NAMES_EN, DAY_NAMES_SHORT_EN,
  MONTH_NAMES_CN, DAY_NAMES_CN,
  
  // Date Creation
  now, timestamp, createDate, fromTimestamp, clone, today, tomorrow, yesterday,
  
  // Date Parsing
  parseDate, parseISO,
  
  // Date Formatting
  format, toISO, toISODate, toISOTime, toISODatetime,
  
  // Date Component Getters
  getYear, getMonth, getDay, getDayOfWeek, getISODayOfWeek,
  getHour, getMinute, getSecond, getMillisecond,
  getDayOfYear, getWeekOfYear, getQuarter, getDaysInMonth, isLeapYear,
  
  // Date Arithmetic
  addMilliseconds, addSeconds, addMinutes, addHours, addDays, addWeeks, addMonths, addYears,
  subtractMilliseconds, subtractSeconds, subtractMinutes, subtractHours,
  subtractDays, subtractWeeks, subtractMonths, subtractYears,
  
  // Date Boundary Operations
  startOfDay, endOfDay, startOfWeek, endOfWeek,
  startOfMonth, endOfMonth, startOfYear, endOfYear,
  startOfQuarter, endOfQuarter, startOfHour, endOfHour, startOfMinute, endOfMinute,
  
  // Date Comparison
  isBefore, isAfter, isSame, isSameDay, isSameMonth, isSameYear,
  isBetween, isToday, isYesterday, isTomorrow, isPast, isFuture,
  isWeekend, isWeekday, min, max,
  
  // Date Difference
  diff, diffInMilliseconds, diffInSeconds, diffInMinutes, diffInHours,
  diffInDays, diffInWeeks, diffInMonths, diffInYears,
  
  // Relative Time
  fromNow, formatDistanceToNow,
  
  // Validation
  isValid, isValidDateString, isLeapYearNum, getDaysInMonthNum, isValidDate,
  
  // Utility Functions
  getAge, getNextDayOfWeek, getPreviousDayOfWeek, getNthDayOfMonth,
  getDatesInRange, countBusinessDays, addBusinessDays,
  
  // Class
  DateUtils
} from './mod';

// ============================================
// Test Framework
// ============================================

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}: ${e}`);
    failed++;
  }
}

function assertEqual<T>(actual: T, expected: T, msg?: string): void {
  if (actual !== expected) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertApproxEqual(actual: number, expected: number, tolerance: number, msg?: string): void {
  if (Math.abs(actual - expected) > tolerance) {
    throw new Error(`${msg || 'Assertion failed'}: expected ~${expected}, got ${actual}`);
  }
}

function assertTrue(value: boolean, msg?: string): void {
  if (!value) {
    throw new Error(`${msg || 'Assertion failed'}: expected true, got false`);
  }
}

function assertFalse(value: boolean, msg?: string): void {
  if (value) {
    throw new Error(`${msg || 'Assertion failed'}: expected false, got true`);
  }
}

function assertNotNull<T>(value: T | null, msg?: string): void {
  if (value === null) {
    throw new Error(`${msg || 'Assertion failed'}: expected non-null, got null`);
  }
}

function assertNull<T>(value: T | null, msg?: string): void {
  if (value !== null) {
    throw new Error(`${msg || 'Assertion failed'}: expected null, got ${JSON.stringify(value)}`);
  }
}

function assertArrayEqual<T>(actual: T[], expected: T[], msg?: string): void {
  if (actual.length !== expected.length) {
    throw new Error(`${msg || 'Assertion failed'}: array lengths differ`);
  }
  for (let i = 0; i < actual.length; i++) {
    if (actual[i] !== expected[i]) {
      throw new Error(`${msg || 'Assertion failed'}: arrays differ at index ${i}`);
    }
  }
}

// ============================================
// Constants Tests
// ============================================

test('MILLIS_PER_SECOND should be 1000', () => {
  assertEqual(MILLIS_PER_SECOND, 1000);
});

test('MILLIS_PER_MINUTE should be 60000', () => {
  assertEqual(MILLIS_PER_MINUTE, 60000);
});

test('MILLIS_PER_HOUR should be 3600000', () => {
  assertEqual(MILLIS_PER_HOUR, 3600000);
});

test('MILLIS_PER_DAY should be 86400000', () => {
  assertEqual(MILLIS_PER_DAY, 86400000);
});

test('MILLIS_PER_WEEK should be 604800000', () => {
  assertEqual(MILLIS_PER_WEEK, 604800000);
});

test('MONTH_NAMES_EN should have 12 months', () => {
  assertEqual(MONTH_NAMES_EN.length, 12);
  assertEqual(MONTH_NAMES_EN[0], 'January');
  assertEqual(MONTH_NAMES_EN[11], 'December');
});

test('DAY_NAMES_EN should have 7 days', () => {
  assertEqual(DAY_NAMES_EN.length, 7);
  assertEqual(DAY_NAMES_EN[0], 'Sunday');
  assertEqual(DAY_NAMES_EN[6], 'Saturday');
});

// ============================================
// Date Creation Tests
// ============================================

test('now() should return current date', () => {
  const date = now();
  assertTrue(isValid(date));
  assertTrue(isValidDateString(date.toISOString()));
});

test('timestamp() should return current milliseconds', () => {
  const ts = timestamp();
  assertTrue(ts > 0);
  assertApproxEqual(ts, Date.now(), 1000);
});

test('createDate() should create date from components', () => {
  const date = createDate(2024, 3, 15, 10, 30, 45, 500);
  assertEqual(getYear(date), 2024);
  assertEqual(getMonth(date), 3);
  assertEqual(getDay(date), 15);
  assertEqual(getHour(date), 10);
  assertEqual(getMinute(date), 30);
  assertEqual(getSecond(date), 45);
  assertEqual(getMillisecond(date), 500);
});

test('createDate() with defaults should use 0 for time', () => {
  const date = createDate(2024, 6, 1);
  assertEqual(getHour(date), 0);
  assertEqual(getMinute(date), 0);
  assertEqual(getSecond(date), 0);
});

test('fromTimestamp() should create date from ms', () => {
  const ts = 1709424000000; // March 3, 2024
  const date = fromTimestamp(ts);
  assertEqual(date.getTime(), ts);
});

test('clone() should create independent copy', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = clone(date1);
  assertEqual(date1.getTime(), date2.getTime());
  date2.setFullYear(2025);
  assertEqual(getYear(date1), 2024);
  assertEqual(getYear(date2), 2025);
});

test('today() should return midnight of today', () => {
  const todayDate = today();
  assertTrue(isToday(todayDate));
  assertEqual(getHour(todayDate), 0);
  assertEqual(getMinute(todayDate), 0);
  assertEqual(getSecond(todayDate), 0);
});

test('tomorrow() should return midnight of tomorrow', () => {
  const tomorrowDate = tomorrow();
  assertTrue(isTomorrow(tomorrowDate));
  assertEqual(getHour(tomorrowDate), 0);
});

test('yesterday() should return midnight of yesterday', () => {
  const yesterdayDate = yesterday();
  assertTrue(isYesterday(yesterdayDate));
  assertEqual(getHour(yesterdayDate), 0);
});

// ============================================
// Date Parsing Tests
// ============================================

test('parseDate() should parse YYYY-MM-DD', () => {
  const date = parseDate('2024-03-15');
  assertNotNull(date);
  assertEqual(getYear(date!), 2024);
  assertEqual(getMonth(date!), 3);
  assertEqual(getDay(date!), 15);
});

test('parseDate() should parse YYYY/MM/DD', () => {
  const date = parseDate('2024/03/15');
  assertNotNull(date);
  assertEqual(getMonth(date!), 3);
});

test('parseDate() should return null for empty string', () => {
  assertNull(parseDate(''));
  assertNull(parseDate('   '));
});

test('parseISO() should parse ISO string', () => {
  const date = parseISO('2024-03-15T10:30:00Z');
  assertNotNull(date);
  assertEqual(getYear(date!), 2024);
});

test('parseISO() should return null for invalid', () => {
  assertNull(parseISO('invalid'));
});

// ============================================
// Date Formatting Tests
// ============================================

test('format() should format YYYY-MM-DD', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(format(date, 'YYYY-MM-DD'), '2024-03-15');
});

test('format() should format with month name', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(format(date, 'MMMM DD, YYYY'), 'March 15, 2024');
});

test('format() should format with short month name', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(format(date, 'MMM DD'), 'Mar 15');
});

test('format() should format with day name', () => {
  const date = createDate(2024, 3, 15); // Friday
  assertEqual(format(date, 'dddd'), 'Friday');
});

test('format() should format time correctly', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45);
  assertEqual(format(date, 'HH:mm:ss'), '14:30:45');
});

test('format() should format 12-hour time with AM/PM', () => {
  const date1 = createDate(2024, 3, 15, 10, 30, 0);
  assertEqual(format(date1, 'hh:mm A'), '10:30 AM');
  
  const date2 = createDate(2024, 3, 15, 14, 30, 0);
  assertEqual(format(date2, 'hh:mm A'), '02:30 PM');
});

test('format() should handle midnight correctly', () => {
  const date = createDate(2024, 3, 15, 0, 0, 0);
  assertEqual(format(date, 'hh:mm A'), '12:00 AM');
});

test('format() should handle noon correctly', () => {
  const date = createDate(2024, 3, 15, 12, 0, 0);
  assertEqual(format(date, 'hh:mm A'), '12:00 PM');
});

test('toISO() should return ISO string', () => {
  const date = createDate(2024, 3, 15);
  assertTrue(toISO(date).startsWith('2024-03-15'));
});

test('toISODate() should return YYYY-MM-DD', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(toISODate(date), '2024-03-15');
});

test('toISOTime() should return HH:mm:ss', () => {
  const date = createDate(2024, 3, 15, 10, 30, 45);
  assertEqual(toISOTime(date), '10:30:45');
});

test('toISODatetime() should return YYYY-MM-DD HH:mm:ss', () => {
  const date = createDate(2024, 3, 15, 10, 30, 45);
  assertEqual(toISODatetime(date), '2024-03-15 10:30:45');
});

// ============================================
// Date Component Getters Tests
// ============================================

test('getYear() should return year', () => {
  const date = createDate(2024, 1, 1);
  assertEqual(getYear(date), 2024);
});

test('getMonth() should return month (1-12)', () => {
  const date = createDate(2024, 6, 1);
  assertEqual(getMonth(date), 6);
});

test('getDay() should return day (1-31)', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(getDay(date), 15);
});

test('getDayOfWeek() should return 0-6 (Sunday=0)', () => {
  const sunday = createDate(2024, 3, 17); // March 17, 2024 is Sunday
  assertEqual(getDayOfWeek(sunday), 0);
  
  const monday = createDate(2024, 3, 18);
  assertEqual(getDayOfWeek(monday), 1);
});

test('getISODayOfWeek() should return 1-7 (Monday=1)', () => {
  const sunday = createDate(2024, 3, 17);
  assertEqual(getISODayOfWeek(sunday), 7);
  
  const monday = createDate(2024, 3, 18);
  assertEqual(getISODayOfWeek(monday), 1);
});

test('getHour() should return 0-23', () => {
  const date = createDate(2024, 1, 1, 15);
  assertEqual(getHour(date), 15);
});

test('getMinute() should return 0-59', () => {
  const date = createDate(2024, 1, 1, 0, 45);
  assertEqual(getMinute(date), 45);
});

test('getSecond() should return 0-59', () => {
  const date = createDate(2024, 1, 1, 0, 0, 30);
  assertEqual(getSecond(date), 30);
});

test('getMillisecond() should return 0-999', () => {
  const date = createDate(2024, 1, 1, 0, 0, 0, 500);
  assertEqual(getMillisecond(date), 500);
});

test('getDayOfYear() should return correct day number', () => {
  const jan1 = createDate(2024, 1, 1);
  assertEqual(getDayOfYear(jan1), 1);
  
  const feb1 = createDate(2024, 2, 1);
  assertEqual(getDayOfYear(feb1), 32);
  
  const dec31 = createDate(2024, 12, 31);
  assertEqual(getDayOfYear(dec31), 366); // 2024 is leap year
});

test('getQuarter() should return correct quarter', () => {
  assertEqual(getQuarter(createDate(2024, 1, 1)), 1);
  assertEqual(getQuarter(createDate(2024, 3, 1)), 1);
  assertEqual(getQuarter(createDate(2024, 4, 1)), 2);
  assertEqual(getQuarter(createDate(2024, 6, 1)), 2);
  assertEqual(getQuarter(createDate(2024, 7, 1)), 3);
  assertEqual(getQuarter(createDate(2024, 9, 1)), 3);
  assertEqual(getQuarter(createDate(2024, 10, 1)), 4);
  assertEqual(getQuarter(createDate(2024, 12, 1)), 4);
});

test('getDaysInMonth() should return correct days', () => {
  assertEqual(getDaysInMonth(createDate(2024, 1, 1)), 31);
  assertEqual(getDaysInMonth(createDate(2024, 2, 1)), 29); // leap year
  assertEqual(getDaysInMonth(createDate(2024, 4, 1)), 30);
  assertEqual(getDaysInMonth(createDate(2023, 2, 1)), 28); // non-leap year
});

test('isLeapYear() should detect leap year', () => {
  assertTrue(isLeapYear(createDate(2024, 1, 1)));
  assertTrue(isLeapYear(createDate(2000, 1, 1)));
  assertFalse(isLeapYear(createDate(2023, 1, 1)));
  assertFalse(isLeapYear(createDate(1900, 1, 1)));
});

// ============================================
// Date Arithmetic Tests
// ============================================

test('addMilliseconds() should add ms', () => {
  const date = createDate(2024, 1, 1, 0, 0, 0, 0);
  const result = addMilliseconds(date, 1000);
  assertEqual(getMillisecond(result), 1000);
});

test('addSeconds() should add seconds', () => {
  const date = createDate(2024, 1, 1, 0, 0, 0);
  const result = addSeconds(date, 30);
  assertEqual(getSecond(result), 30);
});

test('addSeconds() should overflow to minutes', () => {
  const date = createDate(2024, 1, 1, 0, 0, 30);
  const result = addSeconds(date, 30);
  assertEqual(getMinute(result), 1);
  assertEqual(getSecond(result), 0);
});

test('addMinutes() should add minutes', () => {
  const date = createDate(2024, 1, 1, 10, 0);
  const result = addMinutes(date, 30);
  assertEqual(getMinute(result), 30);
});

test('addHours() should add hours', () => {
  const date = createDate(2024, 1, 1, 10);
  const result = addHours(date, 5);
  assertEqual(getHour(result), 15);
});

test('addDays() should add days', () => {
  const date = createDate(2024, 1, 15);
  const result = addDays(date, 5);
  assertEqual(getDay(result), 20);
});

test('addDays() should overflow to next month', () => {
  const date = createDate(2024, 1, 31);
  const result = addDays(date, 1);
  assertEqual(getMonth(result), 2);
  assertEqual(getDay(result), 1);
});

test('addWeeks() should add weeks', () => {
  const date = createDate(2024, 1, 1);
  const result = addWeeks(date, 2);
  assertEqual(getDay(result), 15);
});

test('addMonths() should add months', () => {
  const date = createDate(2024, 1, 15);
  const result = addMonths(date, 2);
  assertEqual(getMonth(result), 3);
  assertEqual(getDay(result), 15);
});

test('addMonths() should handle month overflow', () => {
  const date = createDate(2024, 11, 15);
  const result = addMonths(date, 2);
  assertEqual(getYear(result), 2025);
  assertEqual(getMonth(result), 1);
});

test('addMonths() should handle Jan 31 -> Feb', () => {
  const date = createDate(2024, 1, 31);
  const result = addMonths(date, 1);
  assertEqual(getMonth(result), 2);
  assertEqual(getDay(result), 29); // Feb 29 in leap year 2024
});

test('addYears() should add years', () => {
  const date = createDate(2024, 1, 1);
  const result = addYears(date, 1);
  assertEqual(getYear(result), 2025);
});

test('addYears() should handle Feb 29 in non-leap year', () => {
  const date = createDate(2024, 2, 29);
  const result = addYears(date, 1);
  assertEqual(getYear(result), 2025);
  assertEqual(getMonth(result), 2);
  assertEqual(getDay(result), 28); // 2025 is not leap year
});

test('subtractDays() should subtract days', () => {
  const date = createDate(2024, 1, 10);
  const result = subtractDays(date, 5);
  assertEqual(getDay(result), 5);
});

test('subtractMonths() should subtract months', () => {
  const date = createDate(2024, 3, 15);
  const result = subtractMonths(date, 2);
  assertEqual(getMonth(result), 1);
});

// ============================================
// Date Boundary Operations Tests
// ============================================

test('startOfDay() should return midnight', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 500);
  const result = startOfDay(date);
  assertEqual(getHour(result), 0);
  assertEqual(getMinute(result), 0);
  assertEqual(getSecond(result), 0);
  assertEqual(getMillisecond(result), 0);
});

test('endOfDay() should return 23:59:59.999', () => {
  const date = createDate(2024, 3, 15, 10);
  const result = endOfDay(date);
  assertEqual(getHour(result), 23);
  assertEqual(getMinute(result), 59);
  assertEqual(getSecond(result), 59);
  assertEqual(getMillisecond(result), 999);
});

test('startOfWeek() should return Monday by default', () => {
  const wednesday = createDate(2024, 3, 20); // Wednesday
  const result = startOfWeek(wednesday);
  assertEqual(getDayOfWeek(result), 1); // Monday
  assertEqual(getDay(result), 18);
});

test('startOfWeek() with startOnSunday should return Sunday', () => {
  const wednesday = createDate(2024, 3, 20);
  const result = startOfWeek(wednesday, true);
  assertEqual(getDayOfWeek(result), 0); // Sunday
  assertEqual(getDay(result), 17);
});

test('endOfWeek() should return Sunday by default', () => {
  const wednesday = createDate(2024, 3, 20);
  const result = endOfWeek(wednesday);
  assertEqual(getDayOfWeek(result), 0); // Sunday
  assertEqual(getDay(result), 24);
});

test('startOfMonth() should return first day', () => {
  const date = createDate(2024, 3, 15);
  const result = startOfMonth(date);
  assertEqual(getDay(result), 1);
  assertEqual(getHour(result), 0);
});

test('endOfMonth() should return last day', () => {
  const date = createDate(2024, 3, 15);
  const result = endOfMonth(date);
  assertEqual(getDay(result), 31);
  assertEqual(getHour(result), 23);
});

test('endOfMonth() should handle February in leap year', () => {
  const date = createDate(2024, 2, 15);
  const result = endOfMonth(date);
  assertEqual(getDay(result), 29);
});

test('startOfYear() should return Jan 1', () => {
  const date = createDate(2024, 6, 15);
  const result = startOfYear(date);
  assertEqual(getMonth(result), 1);
  assertEqual(getDay(result), 1);
});

test('endOfYear() should return Dec 31', () => {
  const date = createDate(2024, 6, 15);
  const result = endOfYear(date);
  assertEqual(getMonth(result), 12);
  assertEqual(getDay(result), 31);
});

test('startOfQuarter() should return first day of quarter', () => {
  const q2Date = createDate(2024, 5, 15);
  const result = startOfQuarter(q2Date);
  assertEqual(getMonth(result), 4);
  assertEqual(getDay(result), 1);
});

test('endOfQuarter() should return last day of quarter', () => {
  const q2Date = createDate(2024, 5, 15);
  const result = endOfQuarter(q2Date);
  assertEqual(getMonth(result), 6);
  assertEqual(getDay(result), 30);
});

test('startOfHour() should return 0 minutes and seconds', () => {
  const date = createDate(2024, 3, 15, 10, 30, 45);
  const result = startOfHour(date);
  assertEqual(getMinute(result), 0);
  assertEqual(getSecond(result), 0);
});

test('endOfHour() should return 59:59.999', () => {
  const date = createDate(2024, 3, 15, 10, 30);
  const result = endOfHour(date);
  assertEqual(getMinute(result), 59);
  assertEqual(getSecond(result), 59);
});

// ============================================
// Date Comparison Tests
// ============================================

test('isBefore() should compare dates', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 2, 1);
  assertTrue(isBefore(date1, date2));
  assertFalse(isBefore(date2, date1));
});

test('isAfter() should compare dates', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 2, 1);
  assertTrue(isAfter(date2, date1));
  assertFalse(isAfter(date1, date2));
});

test('isSame() should compare exact dates', () => {
  const date1 = createDate(2024, 1, 1, 10, 30);
  const date2 = createDate(2024, 1, 1, 10, 30);
  assertTrue(isSame(date1, date2));
});

test('isSameDay() should compare days', () => {
  const date1 = createDate(2024, 1, 1, 10);
  const date2 = createDate(2024, 1, 1, 20);
  assertTrue(isSameDay(date1, date2));
});

test('isSameMonth() should compare months', () => {
  const date1 = createDate(2024, 3, 1);
  const date2 = createDate(2024, 3, 31);
  assertTrue(isSameMonth(date1, date2));
});

test('isSameYear() should compare years', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 12, 31);
  assertTrue(isSameYear(date1, date2));
});

test('isBetween() inclusive should include boundaries', () => {
  const start = createDate(2024, 1, 1);
  const end = createDate(2024, 12, 31);
  const middle = createDate(2024, 6, 15);
  
  assertTrue(isBetween(start, start, end));
  assertTrue(isBetween(end, start, end));
  assertTrue(isBetween(middle, start, end));
});

test('isBetween() exclusive should exclude boundaries', () => {
  const start = createDate(2024, 1, 1);
  const end = createDate(2024, 12, 31);
  
  assertFalse(isBetween(start, start, end, false));
  assertFalse(isBetween(end, start, end, false));
});

test('isToday() should detect today', () => {
  assertTrue(isToday(new Date()));
  assertFalse(isToday(createDate(2020, 1, 1)));
});

test('isYesterday() should detect yesterday', () => {
  assertTrue(isYesterday(subtractDays(new Date(), 1)));
});

test('isTomorrow() should detect tomorrow', () => {
  assertTrue(isTomorrow(addDays(new Date(), 1)));
});

test('isPast() should detect past dates', () => {
  assertTrue(isPast(createDate(2020, 1, 1)));
  assertFalse(isPast(createDate(2030, 1, 1)));
});

test('isFuture() should detect future dates', () => {
  assertTrue(isFuture(createDate(2030, 1, 1)));
  assertFalse(isFuture(createDate(2020, 1, 1)));
});

test('isWeekend() should detect Saturday and Sunday', () => {
  const saturday = createDate(2024, 3, 16); // Saturday
  const sunday = createDate(2024, 3, 17); // Sunday
  const monday = createDate(2024, 3, 18);
  
  assertTrue(isWeekend(saturday));
  assertTrue(isWeekend(sunday));
  assertFalse(isWeekend(monday));
});

test('isWeekday() should detect weekdays', () => {
  const monday = createDate(2024, 3, 18);
  const saturday = createDate(2024, 3, 16);
  
  assertTrue(isWeekday(monday));
  assertFalse(isWeekday(saturday));
});

test('min() should return earliest date', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 6, 1);
  const result = min(date1, date2);
  assertEqual(getMonth(result), 1);
});

test('max() should return latest date', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 6, 1);
  const result = max(date1, date2);
  assertEqual(getMonth(result), 6);
});

// ============================================
// Date Difference Tests
// ============================================

test('diff() should return all diff components', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 3, 12);
  const d = diff(date1, date2);
  
  assertApproxEqual(d.days, 2.5, 0.5);
  assertTrue(d.hours > 0);
  assertTrue(d.minutes > 0);
});

test('diffInMilliseconds() should return ms diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 1, 0, 0, 1); // +1 second
  assertEqual(diffInMilliseconds(date1, date2), 1000);
});

test('diffInSeconds() should return seconds diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 1, 0, 0, 30);
  assertEqual(diffInSeconds(date1, date2), 30);
});

test('diffInMinutes() should return minutes diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 1, 0, 15);
  assertEqual(diffInMinutes(date1, date2), 15);
});

test('diffInHours() should return hours diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 1, 5);
  assertEqual(diffInHours(date1, date2), 5);
});

test('diffInDays() should return days diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 5);
  assertEqual(diffInDays(date1, date2), 4);
});

test('diffInWeeks() should return weeks diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 15);
  assertEqual(diffInWeeks(date1, date2), 2);
});

test('diffInMonths() should return months diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 6, 1);
  assertEqual(diffInMonths(date1, date2), 5);
});

test('diffInYears() should return years diff', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2026, 1, 1);
  assertEqual(diffInYears(date1, date2), 2);
});

// ============================================
// Relative Time Tests
// ============================================

test('fromNow() should format past time in English', () => {
  const pastDate = subtractSeconds(new Date(), 30);
  assertTrue(fromNow(pastDate).includes('30 seconds ago'));
});

test('fromNow() should format future time in English', () => {
  const futureDate = addMinutes(new Date(), 5);
  assertTrue(fromNow(futureDate).includes('in 5 minutes'));
});

test('formatDistanceToNow() should format in Chinese', () => {
  const pastDate = subtractMinutes(new Date(), 10);
  const result = formatDistanceToNow(pastDate, 'cn');
  assertTrue(result.includes('10分钟'));
  assertTrue(result.includes('前'));
});

test('formatDistanceToNow() should handle days', () => {
  const pastDate = subtractDays(new Date(), 3);
  assertTrue(formatDistanceToNow(pastDate).includes('3 days ago'));
});

// ============================================
// Validation Tests
// ============================================

test('isValid() should return true for valid date', () => {
  assertTrue(isValid(new Date()));
  assertTrue(isValid(createDate(2024, 1, 1)));
});

test('isValid() should return false for invalid date', () => {
  const invalidDate = new Date('invalid');
  assertFalse(isValid(invalidDate));
  assertFalse(isValid(null));
  assertFalse(isValid(undefined));
});

test('isValidDateString() should validate date strings', () => {
  assertTrue(isValidDateString('2024-03-15'));
  assertTrue(isValidDateString('2024-03-15T10:30:00Z'));
  assertFalse(isValidDateString('invalid'));
});

test('isLeapYearNum() should detect leap year', () => {
  assertTrue(isLeapYearNum(2024));
  assertTrue(isLeapYearNum(2000));
  assertFalse(isLeapYearNum(2023));
  assertFalse(isLeapYearNum(1900));
});

test('getDaysInMonthNum() should return correct days', () => {
  assertEqual(getDaysInMonthNum(2024, 1), 31);
  assertEqual(getDaysInMonthNum(2024, 2), 29);
  assertEqual(getDaysInMonthNum(2023, 2), 28);
});

test('isValidDate() should validate components', () => {
  assertTrue(isValidDate(2024, 1, 15));
  assertTrue(isValidDate(2024, 2, 29)); // Leap year
  assertFalse(isValidDate(2023, 2, 29)); // Non-leap year
  assertFalse(isValidDate(2024, 13, 1)); // Invalid month
  assertFalse(isValidDate(2024, 1, 32)); // Invalid day
});

// ============================================
// Utility Functions Tests
// ============================================

test('getAge() should calculate age correctly', () => {
  const birthDate = createDate(1990, 6, 15);
  const referenceDate = createDate(2024, 6, 15);
  assertEqual(getAge(birthDate, referenceDate), 34);
});

test('getAge() should handle birthday not yet occurred', () => {
  const birthDate = createDate(1990, 6, 15);
  const referenceDate = createDate(2024, 5, 15);
  assertEqual(getAge(birthDate, referenceDate), 33);
});

test('getNextDayOfWeek() should get next occurrence', () => {
  const wednesday = createDate(2024, 3, 20);
  const nextMonday = getNextDayOfWeek(wednesday, 1);
  assertEqual(getDayOfWeek(nextMonday), 1);
  assertEqual(getDay(nextMonday), 25);
});

test('getPreviousDayOfWeek() should get previous occurrence', () => {
  const wednesday = createDate(2024, 3, 20);
  const prevMonday = getPreviousDayOfWeek(wednesday, 1);
  assertEqual(getDayOfWeek(prevMonday), 1);
  assertEqual(getDay(prevMonday), 18);
});

test('getNthDayOfMonth() should find nth weekday', () => {
  // 2nd Monday of March 2024
  const result = getNthDayOfMonth(2024, 3, 1, 2);
  assertNotNull(result);
  assertEqual(getDayOfWeek(result!), 1);
  assertEqual(getDay(result!), 11);
});

test('getNthDayOfMonth() should return null for invalid n', () => {
  assertNull(getNthDayOfMonth(2024, 3, 1, 6));
});

test('getDatesInRange() should return all dates', () => {
  const start = createDate(2024, 1, 1);
  const end = createDate(2024, 1, 5);
  const dates = getDatesInRange(start, end);
  assertEqual(dates.length, 5);
  assertEqual(getDay(dates[0]), 1);
  assertEqual(getDay(dates[4]), 5);
});

test('countBusinessDays() should count weekdays', () => {
  const start = createDate(2024, 3, 18); // Monday
  const end = createDate(2024, 3, 22); // Friday
  assertEqual(countBusinessDays(start, end), 5);
});

test('countBusinessDays() should exclude weekends', () => {
  const start = createDate(2024, 3, 18); // Monday
  const end = createDate(2024, 3, 24); // Sunday
  assertEqual(countBusinessDays(start, end), 5); // Mon-Fri only
});

test('addBusinessDays() should skip weekends', () => {
  const friday = createDate(2024, 3, 22);
  const result = addBusinessDays(friday, 1);
  assertEqual(getDayOfWeek(result), 1); // Monday
  assertEqual(getDay(result), 25);
});

// ============================================
// DateUtils Class Tests
// ============================================

test('DateUtils.now() should create instance', () => {
  const du = DateUtils.now();
  assertTrue(du instanceof DateUtils);
  assertTrue(isValid(du.toDate()));
});

test('DateUtils.from() should create from timestamp', () => {
  const ts = 1709424000000;
  const du = DateUtils.from(ts);
  assertEqual(du.toNumber(), ts);
});

test('DateUtils.parse() should parse string', () => {
  const du = DateUtils.parse('2024-03-15');
  assertNotNull(du);
  assertEqual(du!.getYear(), 2024);
});

test('DateUtils.create() should create from components', () => {
  const du = DateUtils.create(2024, 3, 15, 10, 30);
  assertEqual(du.getYear(), 2024);
  assertEqual(du.getMonth(), 3);
});

test('DateUtils.clone() should create independent copy', () => {
  const du1 = DateUtils.create(2024, 1, 1);
  const du2 = du1.clone();
  du2.addYears(1);
  assertEqual(du1.getYear(), 2024);
  assertEqual(du2.getYear(), 2025);
});

test('DateUtils.format() should format date', () => {
  const du = DateUtils.create(2024, 3, 15);
  assertEqual(du.format('YYYY-MM-DD'), '2024-03-15');
});

test('DateUtils chainable operations', () => {
  const result = DateUtils.create(2024, 1, 15)
    .addDays(5)
    .startOfDay();
  
  assertEqual(result.getMonth(), 1);
  assertEqual(result.getDay(), 20);
  assertEqual(result.getHour(), 0);
});

test('DateUtils boundary operations', () => {
  const du = DateUtils.create(2024, 3, 15, 14, 30);
  du.startOfDay();
  assertEqual(du.getHour(), 0);
});

test('DateUtils comparison methods', () => {
  const du = DateUtils.create(2024, 1, 1);
  const otherDate = createDate(2024, 6, 1);
  
  assertTrue(du.isBefore(otherDate));
  assertFalse(du.isAfter(otherDate));
  assertTrue(du.isPast());
});

test('DateUtils diff methods', () => {
  const du1 = DateUtils.create(2024, 1, 1);
  const du2 = DateUtils.create(2024, 6, 1);
  
  assertEqual(du1.diffInMonths(du2.toDate()), 5);
});

// ============================================
// Run Tests
// ============================================

console.log('\n========================================');
console.log('Date Utilities Test Results');
console.log('========================================');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);
console.log('========================================\n');

if (failed > 0) {
  console.log('Some tests failed!');
} else {
  console.log('All tests passed!');
}