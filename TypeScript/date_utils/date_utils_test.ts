/**
 * Date Utilities Test Suite
 * 
 * Comprehensive tests for the date_utils module.
 * Run with: deno test date_utils_test.ts
 * Or: bun test date_utils_test.ts
 * Or: node --test date_utils_test.ts (Node 18+)
 */

import {
  formatDate,
  parseDate,
  toDate,
  addDays,
  addMonths,
  addYears,
  subtractDays,
  diff,
  diffDays,
  isBefore,
  isAfter,
  isBetween,
  isEqual,
  isSameDay,
  timeAgo,
  fromNow,
  startOfDay,
  startOfWeek,
  startOfMonth,
  startOfYear,
  endOfDay,
  endOfWeek,
  endOfMonth,
  endOfYear,
  isLeapYear,
  getDaysInMonth,
  getQuarter,
  getWeekNumber,
  getDayOfYear,
  isWeekend,
  isWeekday,
  nextDay,
  nextMonday,
  businessDaysBetween,
  addBusinessDays,
  isValid,
  DATE_FORMATS,
  DayOfWeek,
  Month,
} from './mod.ts';

// Test result tracking
let passed = 0;
let failed = 0;
const failures: string[] = [];

function assert(condition: boolean, message: string): void {
  if (condition) {
    passed++;
  } else {
    failed++;
    failures.push(message);
  }
}

function assertEquals(actual: unknown, expected: unknown, message: string): void {
  if (actual === expected) {
    passed++;
  } else {
    failed++;
    failures.push(`${message}: expected ${expected}, got ${actual}`);
  }
}

function assertClose(actual: number, expected: number, tolerance: number, message: string): void {
  if (Math.abs(actual - expected) <= tolerance) {
    passed++;
  } else {
    failed++;
    failures.push(`${message}: expected ${expected} (±${tolerance}), got ${actual}`);
  }
}

// ==================== Test Suites ====================

console.log('🧪 Running Date Utils Tests...\n');

// --- Formatting Tests ---
console.log('📝 Testing formatDate...');

{
  const date = new Date(2024, 0, 15, 14, 30, 45, 123);
  
  // ISO format
  const isoResult = formatDate(date, 'YYYY-MM-DD');
  assert(isoResult === '2024-01-15', `ISO date format: got ${isoResult}`);
  
  // US format
  const usResult = formatDate(date, 'MM/DD/YYYY');
  assert(usResult === '01/15/2024', `US format: got ${usResult}`);
  
  // Human readable
  const humanResult = formatDate(date, 'MMMM D, YYYY', 'en');
  assert(humanResult === 'January 15, 2024', `Human format: got ${humanResult}`);
  
  // Chinese format
  const cnResult = formatDate(date, 'YYYY 年 MM 月 DD 日', 'zh');
  assert(cnResult === '2024 年 01 月 15 日', `Chinese format: got ${cnResult}`);
  
  // Time format
  const timeResult = formatDate(date, 'HH:mm:ss');
  assert(timeResult === '14:30:45', `Time format: got ${timeResult}`);
  
  // 12-hour format
  const time12Result = formatDate(date, 'h:mm A');
  assert(time12Result === '2:30 PM', `12-hour format: got ${time12Result}`);
}

// --- Parsing Tests ---
console.log('📝 Testing parseDate...');

{
  // ISO format
  const isoDate = parseDate('2024-01-15');
  assert(isoDate !== null, 'Parse ISO date');
  assert(isoDate!.getFullYear() === 2024, 'ISO year');
  assert(isoDate!.getMonth() === 0, 'ISO month');
  assert(isoDate!.getDate() === 15, 'ISO day');
  
  // US format
  const usDate = parseDate('01/15/2024');
  assert(usDate !== null, 'Parse US date');
  assert(usDate!.getFullYear() === 2024, 'US year');
  
  // Chinese format
  const cnDate = parseDate('2024 年 01 月 15 日');
  assert(cnDate !== null, 'Parse Chinese date');
  assert(cnDate!.getFullYear() === 2024, 'Chinese year');
  
  // Invalid date
  const invalidDate = parseDate('not-a-date');
  assert(invalidDate === null, 'Invalid date returns null');
}

// --- Arithmetic Tests ---
console.log('📝 Testing date arithmetic...');

{
  const baseDate = new Date(2024, 0, 15);
  
  // Add days
  const addedDays = addDays(baseDate, 7);
  assert(addedDays.getDate() === 22, `Add 7 days: got ${addedDays.getDate()}`);
  
  // Add months
  const addedMonths = addMonths(baseDate, 2);
  assert(addedMonths.getMonth() === 2, `Add 2 months: got month ${addedMonths.getMonth() + 1}`);
  
  // Add years
  const addedYears = addYears(baseDate, 1);
  assert(addedYears.getFullYear() === 2025, `Add 1 year: got ${addedYears.getFullYear()}`);
  
  // Subtract days
  const subtractedDays = subtractDays(baseDate, 5);
  assert(subtractedDays.getDate() === 10, `Subtract 5 days: got ${subtractedDays.getDate()}`);
  
  // Month overflow handling
  const jan31 = new Date(2024, 0, 31);
  const febResult = addMonths(jan31, 1);
  assert(febResult.getMonth() === 1, 'Month overflow handled');
}

// --- Difference Tests ---
console.log('📝 Testing date difference...');

{
  const date1 = new Date(2024, 0, 1);
  const date2 = new Date(2024, 0, 11);
  
  const daysDiff = diffDays(date2, date1);
  assertEquals(daysDiff, 10, 'Days difference');
  
  const msDiff = diff(date2, date1, 'ms');
  assertClose(msDiff, 10 * 24 * 60 * 60 * 1000, 1000, 'Milliseconds difference');
}

// --- Comparison Tests ---
console.log('📝 Testing date comparison...');

{
  const date1 = new Date(2024, 0, 1);
  const date2 = new Date(2024, 0, 15);
  const date3 = new Date(2024, 0, 1);
  
  assert(isBefore(date1, date2), 'isBefore');
  assert(isAfter(date2, date1), 'isAfter');
  assert(isBetween(date2, date1, new Date(2024, 1, 1)), 'isBetween');
  assert(isEqual(date1, date3), 'isEqual');
  assert(isSameDay(date1, date3), 'isSameDay');
  assert(!isSameDay(date1, date2), 'isSameDay different');
}

// --- Relative Time Tests ---
console.log('📝 Testing relative time...');

{
  const now = new Date();
  const oneMinuteAgo = new Date(now.getTime() - 60000);
  const oneHourAgo = new Date(now.getTime() - 3600000);
  const oneDayAgo = new Date(now.getTime() - 86400000);
  
  const minuteAgoStr = timeAgo(oneMinuteAgo, 'en');
  assert(minuteAgoStr.includes('minute'), `Time ago minute: ${minuteAgoStr}`);
  
  const hourAgoStr = timeAgo(oneHourAgo, 'en');
  assert(hourAgoStr.includes('hour'), `Time ago hour: ${hourAgoStr}`);
  
  const dayAgoStr = timeAgo(oneDayAgo, 'en');
  assert(dayAgoStr.includes('day'), `Time ago day: ${dayAgoStr}`);
  
  // Chinese locale
  const cnAgoStr = timeAgo(oneDayAgo, 'zh');
  assert(cnAgoStr.includes('天'), `Chinese time ago: ${cnAgoStr}`);
}

// --- Start/End Tests ---
console.log('📝 Testing startOf/endOf...');

{
  const date = new Date(2024, 5, 15, 14, 30, 45);
  
  // Start of day
  const sod = startOfDay(date);
  assert(sod.getHours() === 0 && sod.getMinutes() === 0 && sod.getSeconds() === 0, 'Start of day');
  
  // End of day
  const eod = endOfDay(date);
  assert(eod.getHours() === 23 && eod.getMinutes() === 59, 'End of day');
  
  // Start of month
  const som = startOfMonth(date);
  assert(som.getDate() === 1, 'Start of month');
  
  // End of month
  const eom = endOfMonth(date);
  assert(eom.getDate() === 30, 'End of month (June)');
  
  // Start of year
  const soy = startOfYear(date);
  assert(soy.getMonth() === 0 && soy.getDate() === 1, 'Start of year');
  
  // End of year
  const eoy = endOfYear(date);
  assert(eoy.getMonth() === 11 && eoy.getDate() === 31, 'End of year');
}

// --- Utility Tests ---
console.log('📝 Testing utilities...');

{
  // Leap year
  assert(isLeapYear(2024) === true, '2024 is leap year');
  assert(isLeapYear(2023) === false, '2023 is not leap year');
  assert(isLeapYear(2000) === true, '2000 is leap year');
  assert(isLeapYear(1900) === false, '1900 is not leap year');
  
  // Days in month
  assertEquals(getDaysInMonth(2024, 2), 29, 'Feb 2024 has 29 days');
  assertEquals(getDaysInMonth(2023, 2), 28, 'Feb 2023 has 28 days');
  assertEquals(getDaysInMonth(2024, 1), 31, 'Jan has 31 days');
  
  // Quarter
  assertEquals(getQuarter(new Date(2024, 0, 15)), 1, 'Q1');
  assertEquals(getQuarter(new Date(2024, 3, 15)), 2, 'Q2');
  assertEquals(getQuarter(new Date(2024, 6, 15)), 3, 'Q3');
  assertEquals(getQuarter(new Date(2024, 9, 15)), 4, 'Q4');
  
  // Weekend
  assert(isWeekend(new Date(2024, 0, 13)), 'Saturday is weekend'); // Jan 13, 2024 is Saturday
  assert(isWeekend(new Date(2024, 0, 14)), 'Sunday is weekend'); // Jan 14, 2024 is Sunday
  assert(!isWeekend(new Date(2024, 0, 15)), 'Monday is not weekend');
  
  // Weekday
  assert(isWeekday(new Date(2024, 0, 15)), 'Monday is weekday');
  assert(!isWeekday(new Date(2024, 0, 13)), 'Saturday is not weekday');
}

// --- Next Day Tests ---
console.log('📝 Testing nextDay...');

{
  // Jan 15, 2024 is Monday
  const monday = new Date(2024, 0, 15);
  
  const nextMon = nextMonday(monday);
  assertEquals(nextMon.getDate(), 22, 'Next Monday');
  
  const nextFri = nextDay(monday, DayOfWeek.Friday);
  assertEquals(nextFri.getDate(), 19, 'Next Friday');
}

// --- Business Days Tests ---
console.log('📝 Testing business days...');

{
  // Jan 15-19, 2024 (Mon-Fri) = 5 business days
  const start = new Date(2024, 0, 15);
  const end = new Date(2024, 0, 19);
  
  const bizDays = businessDaysBetween(start, end);
  assertEquals(bizDays, 5, 'Business days in a week');
  
  // Add business days
  const result = addBusinessDays(start, 5);
  assertEquals(result.getDate(), 22, 'Add 5 business days (lands on Monday)');
}

// --- Validation Tests ---
console.log('📝 Testing validation...');

{
  assert(isValid(new Date()), 'Valid Date object');
  assert(isValid(Date.now()), 'Valid timestamp');
  assert(isValid('2024-01-15'), 'Valid date string');
  assert(!isValid('not-a-date'), 'Invalid date string');
  assert(!isValid(NaN), 'NaN is invalid');
}

// --- Constants Tests ---
console.log('📝 Testing constants...');

{
  assert(DATE_FORMATS.ISO === 'YYYY-MM-DDTHH:mm:ss.SSSZ', 'ISO format constant');
  assert(DayOfWeek.Monday === 1, 'Monday enum');
  assert(Month.January === 1, 'January enum');
}

// ==================== Test Results ====================

console.log('\n' + '='.repeat(50));
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log('='.repeat(50));

if (failures.length > 0) {
  console.log('\n❌ Failures:');
  failures.forEach(f => console.log(`  - ${f}`));
  Deno.exit(1);
} else {
  console.log('\n🎉 All tests passed!');
  Deno.exit(0);
}
