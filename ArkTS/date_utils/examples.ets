/**
 * Date Utilities Examples for ArkTS
 */

import {
  now, today, createDate, parseDate, fromTimestamp,
  format, toISODate, toISODatetime,
  addDays, addMonths, addYears, subtractDays,
  startOfDay, endOfDay, startOfMonth, endOfMonth,
  isToday, isWeekend, isLeapYear,
  diff, diffInDays, fromNow,
  getAge, countBusinessDays, addBusinessDays,
  DateUtils
} from '../date_utils/mod';

// ============================================
// Example 1: Basic Date Operations
// ============================================

console.log('=== Basic Date Operations ===');

// Current date and time
const currentDate = now();
console.log(`Current date: ${format(currentDate, 'YYYY-MM-DD HH:mm:ss')}`);

// Today, tomorrow, yesterday
const todayDate = today();
console.log(`Today: ${toISODate(todayDate)}`);

// Create specific date
const birthday = createDate(1990, 6, 15);
console.log(`Birthday: ${format(birthday, 'MMMM DD, YYYY')}`);

// ============================================
// Example 2: Date Formatting
// ============================================

console.log('\n=== Date Formatting ===');

const date = createDate(2024, 3, 15, 14, 30, 45);

console.log(`ISO format: ${format(date, 'YYYY-MM-DDTHH:mm:ss')}`);
console.log(`Long format: ${format(date, 'MMMM DD, YYYY at HH:mm A')}`);
console.log(`Short format: ${format(date, 'MMM D, h:mm A')}`);
console.log(`Day name: ${format(date, 'dddd, MMMM DD')}`);
console.log(`Chinese style: ${format(date, 'YYYY年MM月DD日 HH:mm')}`);

// ============================================
// Example 3: Date Parsing
// ============================================

console.log('\n=== Date Parsing ===');

const parsed1 = parseDate('2024-03-15');
console.log(`Parsed YYYY-MM-DD: ${parsed1 ? toISODate(parsed1) : 'invalid'}`);

const parsed2 = parseDate('2024/12/25');
console.log(`Parsed YYYY/MM/DD: ${parsed2 ? toISODate(parsed2) : 'invalid'}`);

const parsed3 = parseDate('March 15, 2024');
console.log(`Parsed natural: ${parsed3 ? toISODate(parsed3) : 'invalid'}`);

// ============================================
// Example 4: Date Arithmetic
// ============================================

console.log('\n=== Date Arithmetic ===');

const baseDate = createDate(2024, 1, 1);
console.log(`Base date: ${toISODate(baseDate)}`);

console.log(`+7 days: ${toISODate(addDays(baseDate, 7))}`);
console.log(`+1 month: ${toISODate(addMonths(baseDate, 1))}`);
console.log(`+1 year: ${toISODate(addYears(baseDate, 1))}`);
console.log(`-10 days: ${toISODate(subtractDays(baseDate, 10))}`);

// ============================================
// Example 5: Date Boundaries
// ============================================

console.log('\n=== Date Boundaries ===');

const someDate = createDate(2024, 3, 15, 14, 30, 45);

console.log(`Start of day: ${toISODatetime(startOfDay(someDate))}`);
console.log(`End of day: ${toISODatetime(endOfDay(someDate))}`);
console.log(`Start of month: ${toISODate(startOfMonth(someDate))}`);
console.log(`End of month: ${toISODate(endOfMonth(someDate))}`);

// ============================================
// Example 6: Date Comparison
// ============================================

console.log('\n=== Date Comparison ===');

const date1 = createDate(2024, 3, 1);
const date2 = createDate(2024, 6, 15);

console.log(`Is today?: ${isToday(now())}`);
console.log(`Is weekend?: ${isWeekend(createDate(2024, 3, 16))}`); // Saturday
console.log(`Is 2024 leap year?: ${isLeapYear(createDate(2024, 1, 1))}`);

// ============================================
// Example 7: Date Difference
// ============================================

console.log('\n=== Date Difference ===');

const start = createDate(2024, 1, 1);
const end = createDate(2024, 12, 31);

const difference = diff(start, end);
console.log(`Days between: ${difference.days}`);
console.log(`Weeks between: ${difference.weeks}`);
console.log(`Months between: ${difference.months}`);
console.log(`Hours between: ${difference.hours}`);

// ============================================
// Example 8: Relative Time
// ============================================

console.log('\n=== Relative Time ===');

const past1 = subtractDays(now(), 1);
console.log(`1 day ago: ${fromNow(past1)}`);

const past2 = subtractDays(now(), 7);
console.log(`7 days ago: ${fromNow(past2)}`);

const past3 = subtractHours(now(), 3);
console.log(`3 hours ago: ${fromNow(past3)}`);

const future = addDays(now(), 2);
console.log(`2 days future: ${fromNow(future)}`);

// ============================================
// Example 9: Utility Functions
// ============================================

console.log('\n=== Utility Functions ===');

// Calculate age
const birthDate = createDate(1990, 6, 15);
const age = getAge(birthDate);
console.log(`Age: ${age} years`);

// Business days
const workStart = createDate(2024, 3, 18); // Monday
const workEnd = createDate(2024, 3, 22); // Friday
console.log(`Business days: ${countBusinessDays(workStart, workEnd)}`);

const friday = createDate(2024, 3, 22);
const nextWorkDay = addBusinessDays(friday, 1);
console.log(`Next business day after Friday: ${toISODate(nextWorkDay)} (Monday)`);

// ============================================
// Example 10: DateUtils Class (Chainable)
// ============================================

console.log('\n=== DateUtils Class ===');

// Create and manipulate dates fluently
const result = DateUtils.create(2024, 1, 1)
  .addDays(5)
  .addMonths(1)
  .startOfDay()
  .toDate();
console.log(`Chained result: ${toISODate(result)}`);

// Check properties
console.log(`Is past?: ${DateUtils.now().subtractDays(1).isPast()}`);
console.log(`Is future?: ${DateUtils.now().addDays(1).isFuture()}`);

// Format relative time
console.log(`2 hours ago: ${DateUtils.now().subtractHours(2).fromNow()}`);

// ============================================
// Summary
// ============================================

console.log('\n=== Summary ===');
console.log('Date utilities module provides comprehensive date/time operations.');
console.log('Supports parsing, formatting, arithmetic, comparison, and utilities.');
console.log('Zero external dependencies, works with ArkTS/HarmonyOS.');