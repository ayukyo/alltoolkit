/**
 * Date Utilities for ArkTS
 * 
 * A comprehensive date/time manipulation utility module for ArkTS/HarmonyOS
 * providing common date operations with zero dependencies.
 * 
 * Features:
 * - Date creation and parsing
 * - Date formatting
 * - Date arithmetic (add/subtract days, months, years)
 * - Date comparison
 * - Date boundary operations (start/end of day, week, month, year)
 * - Date difference calculations
 * - Validation utilities
 * - Relative time formatting (e.g., "2 hours ago")
 * - Weekday and month names
 * 
 * @module date_utils
 * @version 1.0.0
 */

// ============================================
// Constants
// ============================================

export const MILLIS_PER_SECOND = 1000;
export const MILLIS_PER_MINUTE = 60000;
export const MILLIS_PER_HOUR = 3600000;
export const MILLIS_PER_DAY = 86400000;
export const MILLIS_PER_WEEK = 604800000;

export const MONTH_NAMES_EN = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

export const MONTH_NAMES_SHORT_EN = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

export const DAY_NAMES_EN = [
  'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
];

export const DAY_NAMES_SHORT_EN = [
  'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'
];

// Chinese month and day names
export const MONTH_NAMES_CN = [
  '一月', '二月', '三月', '四月', '五月', '六月',
  '七月', '八月', '九月', '十月', '十一月', '十二月'
];

export const DAY_NAMES_CN = [
  '周日', '周一', '周二', '周三', '周四', '周五', '周六'
];

// ============================================
// Date Creation
// ============================================

/**
 * Get current date
 */
export function now(): Date {
  return new Date();
}

/**
 * Get current timestamp in milliseconds
 */
export function timestamp(): number {
  return Date.now();
}

/**
 * Create date from components
 */
export function createDate(
  year: number,
  month: number,
  day: number,
  hour: number = 0,
  minute: number = 0,
  second: number = 0,
  millisecond: number = 0
): Date {
  return new Date(year, month - 1, day, hour, minute, second, millisecond);
}

/**
 * Create date from timestamp
 */
export function fromTimestamp(ms: number): Date {
  return new Date(ms);
}

/**
 * Clone a date
 */
export function clone(date: Date): Date {
  return new Date(date.getTime());
}

/**
 * Get today's date (at midnight)
 */
export function today(): Date {
  return startOfDay(new Date());
}

/**
 * Get tomorrow's date (at midnight)
 */
export function tomorrow(): Date {
  return addDays(startOfDay(new Date()), 1);
}

/**
 * Get yesterday's date (at midnight)
 */
export function yesterday(): Date {
  return addDays(startOfDay(new Date()), -1);
}

// ============================================
// Date Parsing
// ============================================

/**
 * Parse date string in various formats
 * Supported formats: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY
 */
export function parseDate(dateStr: string, format?: string): Date | null {
  if (!dateStr || dateStr.trim() === '') {
    return null;
  }

  // Try native parsing first
  const nativeParsed = new Date(dateStr);
  if (!isNaN(nativeParsed.getTime())) {
    return nativeParsed;
  }

  // Try specific formats
  const formats = format ? [format] : [
    'YYYY-MM-DD',
    'YYYY/MM/DD',
    'DD-MM-YYYY',
    'DD/MM/YYYY',
    'YYYY-MM-DD HH:mm:ss',
    'YYYY/MM/DD HH:mm:ss',
    'YYYY-MM-DDTHH:mm:ss',
    'YYYY-MM-DDTHH:mm:ss.SSSZ'
  ];

  for (const fmt of formats) {
    const result = parseWithFormat(dateStr, fmt);
    if (result) {
      return result;
    }
  }

  return null;
}

/**
 * Parse date string with specific format
 */
function parseWithFormat(dateStr: string, format: string): Date | null {
  const formatParts = format.split(/[-/ :T.Z]/);
  const dateParts = dateStr.split(/[-/ :T.Z]/);

  if (formatParts.length !== dateParts.length) {
    return null;
  }

  let year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0, ms = 0;

  for (let i = 0; i < formatParts.length; i++) {
    const part = formatParts[i];
    const value = parseInt(dateParts[i], 10);

    switch (part) {
      case 'YYYY':
        year = value;
        break;
      case 'YY':
        year = value < 50 ? 2000 + value : 1900 + value;
        break;
      case 'MM':
        month = value;
        break;
      case 'DD':
        day = value;
        break;
      case 'HH':
        hour = value;
        break;
      case 'mm':
        minute = value;
        break;
      case 'ss':
        second = value;
        break;
      case 'SSS':
        ms = value;
        break;
    }
  }

  if (year && month && day) {
    return new Date(year, month - 1, day, hour, minute, second, ms);
  }

  return null;
}

/**
 * Parse ISO date string
 */
export function parseISO(isoString: string): Date | null {
  const date = new Date(isoString);
  return isNaN(date.getTime()) ? null : date;
}

// ============================================
// Date Formatting
// ============================================

/**
 * Format date using format string
 * Supported tokens:
 * YYYY - 4-digit year
 * YY - 2-digit year
 * MM - 2-digit month (01-12)
 * M - month (1-12)
 * DD - 2-digit day (01-31)
 * D - day (1-31)
 * HH - 2-digit hour (00-23)
 * H - hour (0-23)
 * hh - 2-digit hour (01-12)
 * h - hour (1-12)
 * mm - 2-digit minute (00-59)
 * m - minute (0-59)
 * ss - 2-digit second (00-59)
 * s - second (0-59)
 * SSS - milliseconds
 * A - AM/PM
 * a - am/pm
 * dddd - day name
 * ddd - short day name
 * MMMM - month name
 * MMM - short month name
 */
export function format(date: Date, formatStr: string): string {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = date.getMinutes();
  const second = date.getSeconds();
  const ms = date.getMilliseconds();
  const dayOfWeek = date.getDay();

  let result = formatStr;

  // Year
  result = result.replace(/YYYY/g, year.toString());
  result = result.replace(/YY/g, year.toString().slice(-2));

  // Month name
  result = result.replace(/MMMM/g, MONTH_NAMES_EN[month - 1]);
  result = result.replace(/MMM/g, MONTH_NAMES_SHORT_EN[month - 1]);

  // Month number
  result = result.replace(/MM/g, month.toString().padStart(2, '0'));
  result = result.replace(/M/g, month.toString());

  // Day name
  result = result.replace(/dddd/g, DAY_NAMES_EN[dayOfWeek]);
  result = result.replace(/ddd/g, DAY_NAMES_SHORT_EN[dayOfWeek]);

  // Day
  result = result.replace(/DD/g, day.toString().padStart(2, '0'));
  result = result.replace(/D/g, day.toString());

  // Hour 12-hour format
  const hour12 = hour % 12 || 12;
  result = result.replace(/hh/g, hour12.toString().padStart(2, '0'));
  result = result.replace(/h/g, hour12.toString());

  // Hour 24-hour format
  result = result.replace(/HH/g, hour.toString().padStart(2, '0'));
  result = result.replace(/H/g, hour.toString());

  // Minute
  result = result.replace(/mm/g, minute.toString().padStart(2, '0'));
  result = result.replace(/m/g, minute.toString());

  // Second
  result = result.replace(/ss/g, second.toString().padStart(2, '0'));
  result = result.replace(/s/g, second.toString());

  // Millisecond
  result = result.replace(/SSS/g, ms.toString().padStart(3, '0'));

  // AM/PM
  result = result.replace(/A/g, hour < 12 ? 'AM' : 'PM');
  result = result.replace(/a/g, hour < 12 ? 'am' : 'pm');

  return result;
}

/**
 * Format date to ISO string
 */
export function toISO(date: Date): string {
  return date.toISOString();
}

/**
 * Format date to ISO date (YYYY-MM-DD)
 */
export function toISODate(date: Date): string {
  return format(date, 'YYYY-MM-DD');
}

/**
 * Format date to ISO time (HH:mm:ss)
 */
export function toISOTime(date: Date): string {
  return format(date, 'HH:mm:ss');
}

/**
 * Format date to ISO datetime (YYYY-MM-DD HH:mm:ss)
 */
export function toISODatetime(date: Date): string {
  return format(date, 'YYYY-MM-DD HH:mm:ss');
}

// ============================================
// Date Component Getters
// ============================================

/**
 * Get year from date
 */
export function getYear(date: Date): number {
  return date.getFullYear();
}

/**
 * Get month from date (1-12)
 */
export function getMonth(date: Date): number {
  return date.getMonth() + 1;
}

/**
 * Get day of month from date (1-31)
 */
export function getDay(date: Date): number {
  return date.getDate();
}

/**
 * Get day of week from date (0-6, Sunday = 0)
 */
export function getDayOfWeek(date: Date): number {
  return date.getDay();
}

/**
 * Get day of week as ISO (1-7, Monday = 1)
 */
export function getISODayOfWeek(date: Date): number {
  const day = date.getDay();
  return day === 0 ? 7 : day;
}

/**
 * Get hour from date (0-23)
 */
export function getHour(date: Date): number {
  return date.getHours();
}

/**
 * Get minute from date (0-59)
 */
export function getMinute(date: Date): number {
  return date.getMinutes();
}

/**
 * Get second from date (0-59)
 */
export function getSecond(date: Date): number {
  return date.getSeconds();
}

/**
 * Get millisecond from date (0-999)
 */
export function getMillisecond(date: Date): number {
  return date.getMilliseconds();
}

/**
 * Get day of year (1-366)
 */
export function getDayOfYear(date: Date): number {
  const start = new Date(date.getFullYear(), 0, 0);
  const diff = date.getTime() - start.getTime();
  return Math.floor(diff / MILLIS_PER_DAY);
}

/**
 * Get week of year
 */
export function getWeekOfYear(date: Date): number {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil(((d.getTime() - yearStart.getTime()) / MILLIS_PER_DAY + 1) / 7);
}

/**
 * Get quarter of year (1-4)
 */
export function getQuarter(date: Date): number {
  return Math.ceil((date.getMonth() + 1) / 3);
}

/**
 * Get days in month
 */
export function getDaysInMonth(date: Date): number {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
}

/**
 * Check if year is leap year
 */
export function isLeapYear(date: Date): boolean {
  const year = date.getFullYear();
  return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

// ============================================
// Date Arithmetic
// ============================================

/**
 * Add milliseconds to date
 */
export function addMilliseconds(date: Date, amount: number): Date {
  const result = new Date(date.getTime());
  result.setTime(result.getTime() + amount);
  return result;
}

/**
 * Add seconds to date
 */
export function addSeconds(date: Date, amount: number): Date {
  return addMilliseconds(date, amount * MILLIS_PER_SECOND);
}

/**
 * Add minutes to date
 */
export function addMinutes(date: Date, amount: number): Date {
  return addMilliseconds(date, amount * MILLIS_PER_MINUTE);
}

/**
 * Add hours to date
 */
export function addHours(date: Date, amount: number): Date {
  return addMilliseconds(date, amount * MILLIS_PER_HOUR);
}

/**
 * Add days to date
 */
export function addDays(date: Date, amount: number): Date {
  const result = new Date(date.getTime());
  result.setDate(result.getDate() + amount);
  return result;
}

/**
 * Add weeks to date
 */
export function addWeeks(date: Date, amount: number): Date {
  return addDays(date, amount * 7);
}

/**
 * Add months to date
 */
export function addMonths(date: Date, amount: number): Date {
  const result = new Date(date.getTime());
  const expectedMonth = (date.getMonth() + amount) % 12;
  const expectedYear = date.getFullYear() + Math.floor((date.getMonth() + amount) / 12);
  
  result.setMonth(result.getMonth() + amount);
  
  // Handle overflow (e.g., Jan 31 + 1 month should not be Mar 3)
  if (result.getMonth() !== (expectedMonth + 12) % 12) {
    result.setDate(0); // Go to last day of previous month
  }
  
  return result;
}

/**
 * Add years to date
 */
export function addYears(date: Date, amount: number): Date {
  const result = new Date(date.getTime());
  result.setFullYear(result.getFullYear() + amount);
  
  // Handle Feb 29 on non-leap year
  if (date.getMonth() === 1 && date.getDate() === 29 && !isLeapYear(result)) {
    result.setDate(28);
  }
  
  return result;
}

/**
 * Subtract milliseconds from date
 */
export function subtractMilliseconds(date: Date, amount: number): Date {
  return addMilliseconds(date, -amount);
}

/**
 * Subtract seconds from date
 */
export function subtractSeconds(date: Date, amount: number): Date {
  return addSeconds(date, -amount);
}

/**
 * Subtract minutes from date
 */
export function subtractMinutes(date: Date, amount: number): Date {
  return addMinutes(date, -amount);
}

/**
 * Subtract hours from date
 */
export function subtractHours(date: Date, amount: number): Date {
  return addHours(date, -amount);
}

/**
 * Subtract days from date
 */
export function subtractDays(date: Date, amount: number): Date {
  return addDays(date, -amount);
}

/**
 * Subtract weeks from date
 */
export function subtractWeeks(date: Date, amount: number): Date {
  return addWeeks(date, -amount);
}

/**
 * Subtract months from date
 */
export function subtractMonths(date: Date, amount: number): Date {
  return addMonths(date, -amount);
}

/**
 * Subtract years from date
 */
export function subtractYears(date: Date, amount: number): Date {
  return addYears(date, -amount);
}

// ============================================
// Date Boundary Operations
// ============================================

/**
 * Get start of day (midnight)
 */
export function startOfDay(date: Date): Date {
  const result = new Date(date.getTime());
  result.setHours(0, 0, 0, 0);
  return result;
}

/**
 * Get end of day (23:59:59.999)
 */
export function endOfDay(date: Date): Date {
  const result = new Date(date.getTime());
  result.setHours(23, 59, 59, 999);
  return result;
}

/**
 * Get start of week (Monday)
 */
export function startOfWeek(date: Date, startOnSunday: boolean = false): Date {
  const result = new Date(date.getTime());
  const day = result.getDay();
  const diff = startOnSunday ? day : (day === 0 ? -6 : 1 - day);
  result.setDate(result.getDate() + diff);
  return startOfDay(result);
}

/**
 * Get end of week (Sunday)
 */
export function endOfWeek(date: Date, endOnSaturday: boolean = false): Date {
  const result = new Date(date.getTime());
  const day = result.getDay();
  const diff = endOnSaturday ? (6 - day) : (day === 0 ? 0 : 7 - day);
  result.setDate(result.getDate() + diff);
  return endOfDay(result);
}

/**
 * Get start of month
 */
export function startOfMonth(date: Date): Date {
  const result = new Date(date.getTime());
  result.setDate(1);
  return startOfDay(result);
}

/**
 * Get end of month
 */
export function endOfMonth(date: Date): Date {
  const result = new Date(date.getTime());
  result.setMonth(result.getMonth() + 1);
  result.setDate(0);
  return endOfDay(result);
}

/**
 * Get start of year
 */
export function startOfYear(date: Date): Date {
  const result = new Date(date.getTime());
  result.setMonth(0, 1);
  return startOfDay(result);
}

/**
 * Get end of year
 */
export function endOfYear(date: Date): Date {
  const result = new Date(date.getTime());
  result.setMonth(11, 31);
  return endOfDay(result);
}

/**
 * Get start of quarter
 */
export function startOfQuarter(date: Date): Date {
  const quarter = getQuarter(date);
  const month = (quarter - 1) * 3;
  const result = new Date(date.getFullYear(), month, 1);
  return startOfDay(result);
}

/**
 * Get end of quarter
 */
export function endOfQuarter(date: Date): Date {
  const quarter = getQuarter(date);
  const month = quarter * 3 - 1;
  const result = new Date(date.getFullYear(), month + 1, 0);
  return endOfDay(result);
}

/**
 * Get start of hour
 */
export function startOfHour(date: Date): Date {
  const result = new Date(date.getTime());
  result.setMinutes(0, 0, 0);
  return result;
}

/**
 * Get end of hour
 */
export function endOfHour(date: Date): Date {
  const result = new Date(date.getTime());
  result.setMinutes(59, 59, 999);
  return result;
}

/**
 * Get start of minute
 */
export function startOfMinute(date: Date): Date {
  const result = new Date(date.getTime());
  result.setSeconds(0, 0);
  return result;
}

/**
 * Get end of minute
 */
export function endOfMinute(date: Date): Date {
  const result = new Date(date.getTime());
  result.setSeconds(59, 999);
  return result;
}

// ============================================
// Date Comparison
// ============================================

/**
 * Check if date is before another date
 */
export function isBefore(date: Date, dateToCompare: Date): boolean {
  return date.getTime() < dateToCompare.getTime();
}

/**
 * Check if date is after another date
 */
export function isAfter(date: Date, dateToCompare: Date): boolean {
  return date.getTime() > dateToCompare.getTime();
}

/**
 * Check if date is same as another date
 */
export function isSame(date: Date, dateToCompare: Date): boolean {
  return date.getTime() === dateToCompare.getTime();
}

/**
 * Check if date is same day as another date
 */
export function isSameDay(date: Date, dateToCompare: Date): boolean {
  return toISODate(date) === toISODate(dateToCompare);
}

/**
 * Check if date is same month as another date
 */
export function isSameMonth(date: Date, dateToCompare: Date): boolean {
  return date.getFullYear() === dateToCompare.getFullYear() &&
         date.getMonth() === dateToCompare.getMonth();
}

/**
 * Check if date is same year as another date
 */
export function isSameYear(date: Date, dateToCompare: Date): boolean {
  return date.getFullYear() === dateToCompare.getFullYear();
}

/**
 * Check if date is between two dates
 */
export function isBetween(date: Date, startDate: Date, endDate: Date, inclusive: boolean = true): boolean {
  if (inclusive) {
    return date.getTime() >= startDate.getTime() && date.getTime() <= endDate.getTime();
  }
  return date.getTime() > startDate.getTime() && date.getTime() < endDate.getTime();
}

/**
 * Check if date is today
 */
export function isToday(date: Date): boolean {
  return isSameDay(date, new Date());
}

/**
 * Check if date is yesterday
 */
export function isYesterday(date: Date): boolean {
  return isSameDay(date, subtractDays(new Date(), 1));
}

/**
 * Check if date is tomorrow
 */
export function isTomorrow(date: Date): boolean {
  return isSameDay(date, addDays(new Date(), 1));
}

/**
 * Check if date is in the past
 */
export function isPast(date: Date): boolean {
  return date.getTime() < Date.now();
}

/**
 * Check if date is in the future
 */
export function isFuture(date: Date): boolean {
  return date.getTime() > Date.now();
}

/**
 * Check if date is weekend (Saturday or Sunday)
 */
export function isWeekend(date: Date): boolean {
  const day = date.getDay();
  return day === 0 || day === 6;
}

/**
 * Check if date is weekday (Monday-Friday)
 */
export function isWeekday(date: Date): boolean {
  return !isWeekend(date);
}

/**
 * Get the minimum of two dates
 */
export function min(date1: Date, date2: Date): Date {
  return date1.getTime() <= date2.getTime() ? new Date(date1.getTime()) : new Date(date2.getTime());
}

/**
 * Get the maximum of two dates
 */
export function max(date1: Date, date2: Date): Date {
  return date1.getTime() >= date2.getTime() ? new Date(date1.getTime()) : new Date(date2.getTime());
}

// ============================================
// Date Difference
// ============================================

export interface DateDiff {
  milliseconds: number;
  seconds: number;
  minutes: number;
  hours: number;
  days: number;
  weeks: number;
  months: number;
  years: number;
}

/**
 * Calculate difference between two dates
 */
export function diff(date1: Date, date2: Date): DateDiff {
  const diffMs = Math.abs(date2.getTime() - date1.getTime());
  
  const milliseconds = diffMs;
  const seconds = Math.floor(diffMs / MILLIS_PER_SECOND);
  const minutes = Math.floor(diffMs / MILLIS_PER_MINUTE);
  const hours = Math.floor(diffMs / MILLIS_PER_HOUR);
  const days = Math.floor(diffMs / MILLIS_PER_DAY);
  const weeks = Math.floor(diffMs / MILLIS_PER_WEEK);
  
  // Approximate months and years
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);
  
  return {
    milliseconds,
    seconds,
    minutes,
    hours,
    days,
    weeks,
    months,
    years
  };
}

/**
 * Get difference in milliseconds
 */
export function diffInMilliseconds(date1: Date, date2: Date): number {
  return date2.getTime() - date1.getTime();
}

/**
 * Get difference in seconds
 */
export function diffInSeconds(date1: Date, date2: Date): number {
  return Math.floor(diffInMilliseconds(date1, date2) / MILLIS_PER_SECOND);
}

/**
 * Get difference in minutes
 */
export function diffInMinutes(date1: Date, date2: Date): number {
  return Math.floor(diffInMilliseconds(date1, date2) / MILLIS_PER_MINUTE);
}

/**
 * Get difference in hours
 */
export function diffInHours(date1: Date, date2: Date): number {
  return Math.floor(diffInMilliseconds(date1, date2) / MILLIS_PER_HOUR);
}

/**
 * Get difference in days
 */
export function diffInDays(date1: Date, date2: Date): number {
  return Math.floor(diffInMilliseconds(date1, date2) / MILLIS_PER_DAY);
}

/**
 * Get difference in weeks
 */
export function diffInWeeks(date1: Date, date2: Date): number {
  return Math.floor(diffInMilliseconds(date1, date2) / MILLIS_PER_WEEK);
}

/**
 * Get difference in months (approximate)
 */
export function diffInMonths(date1: Date, date2: Date): number {
  let months = (date2.getFullYear() - date1.getFullYear()) * 12;
  months -= date1.getMonth();
  months += date2.getMonth();
  return months;
}

/**
 * Get difference in years
 */
export function diffInYears(date1: Date, date2: Date): number {
  return date2.getFullYear() - date1.getFullYear();
}

// ============================================
// Relative Time
// ============================================

/**
 * Format relative time from now (e.g., "2 hours ago", "in 3 days")
 */
export function fromNow(date: Date, locale: string = 'en'): string {
  return formatDistanceToNow(date, locale);
}

/**
 * Format distance to now
 */
export function formatDistanceToNow(date: Date, locale: string = 'en'): string {
  const now = new Date();
  const diffMs = date.getTime() - now.getTime();
  const isPast = diffMs < 0;
  const absDiffMs = Math.abs(diffMs);
  
  const seconds = Math.floor(absDiffMs / MILLIS_PER_SECOND);
  const minutes = Math.floor(absDiffMs / MILLIS_PER_MINUTE);
  const hours = Math.floor(absDiffMs / MILLIS_PER_HOUR);
  const days = Math.floor(absDiffMs / MILLIS_PER_DAY);
  const weeks = Math.floor(absDiffMs / MILLIS_PER_WEEK);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);
  
  const suffix = locale === 'cn' 
    ? (isPast ? '前' : '后')
    : (isPast ? ' ago' : ' in ');
  
  let value = '';
  
  if (locale === 'cn') {
    if (seconds < 60) {
      value = `${seconds}秒`;
    } else if (minutes < 60) {
      value = `${minutes}分钟`;
    } else if (hours < 24) {
      value = `${hours}小时`;
    } else if (days < 7) {
      value = `${days}天`;
    } else if (weeks < 4) {
      value = `${weeks}周`;
    } else if (months < 12) {
      value = `${months}个月`;
    } else {
      value = `${years}年`;
    }
    return value + suffix;
  } else {
    if (seconds < 60) {
      value = `${seconds} second${seconds !== 1 ? 's' : ''}`;
    } else if (minutes < 60) {
      value = `${minutes} minute${minutes !== 1 ? 's' : ''}`;
    } else if (hours < 24) {
      value = `${hours} hour${hours !== 1 ? 's' : ''}`;
    } else if (days < 7) {
      value = `${days} day${days !== 1 ? 's' : ''}`;
    } else if (weeks < 4) {
      value = `${weeks} week${weeks !== 1 ? 's' : ''}`;
    } else if (months < 12) {
      value = `${months} month${months !== 1 ? 's' : ''}`;
    } else {
      value = `${years} year${years !== 1 ? 's' : ''}`;
    }
    return isPast ? `${value} ago` : `in ${value}`;
  }
}

// ============================================
// Validation
// ============================================

/**
 * Check if value is a valid Date
 */
export function isValid(date: Date | null | undefined): boolean {
  if (!date) return false;
  return !isNaN(date.getTime());
}

/**
 * Check if string is a valid date
 */
export function isValidDateString(dateStr: string): boolean {
  const date = new Date(dateStr);
  return !isNaN(date.getTime());
}

/**
 * Check if year is a leap year
 */
export function isLeapYearNum(year: number): boolean {
  return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

/**
 * Get days in month for year/month
 */
export function getDaysInMonthNum(year: number, month: number): number {
  return new Date(year, month, 0).getDate();
}

/**
 * Check if date components are valid
 */
export function isValidDate(year: number, month: number, day: number): boolean {
  if (month < 1 || month > 12) return false;
  if (day < 1 || day > getDaysInMonthNum(year, month)) return false;
  return true;
}

// ============================================
// Utility Functions
// ============================================

/**
 * Get age from birthdate
 */
export function getAge(birthDate: Date, referenceDate: Date = new Date()): number {
  let age = referenceDate.getFullYear() - birthDate.getFullYear();
  const monthDiff = referenceDate.getMonth() - birthDate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && referenceDate.getDate() < birthDate.getDate())) {
    age--;
  }
  
  return age;
}

/**
 * Get next occurrence of a day of week
 */
export function getNextDayOfWeek(date: Date, dayOfWeek: number): Date {
  const result = new Date(date.getTime());
  const currentDay = result.getDay();
  const diff = (dayOfWeek - currentDay + 7) % 7;
  result.setDate(result.getDate() + (diff === 0 ? 7 : diff));
  return result;
}

/**
 * Get previous occurrence of a day of week
 */
export function getPreviousDayOfWeek(date: Date, dayOfWeek: number): Date {
  const result = new Date(date.getTime());
  const currentDay = result.getDay();
  const diff = (currentDay - dayOfWeek + 7) % 7;
  result.setDate(result.getDate() - (diff === 0 ? 7 : diff));
  return result;
}

/**
 * Get the Nth occurrence of a day of week in a month
 * (e.g., 2nd Monday of March)
 */
export function getNthDayOfMonth(year: number, month: number, dayOfWeek: number, n: number): Date | null {
  if (n < 1 || n > 5) return null;
  
  const firstDay = new Date(year, month - 1, 1);
  const firstDayOfWeek = firstDay.getDay();
  
  let day = 1 + (dayOfWeek - firstDayOfWeek + 7) % 7;
  day += (n - 1) * 7;
  
  const result = new Date(year, month - 1, day);
  
  // Check if it's still in the same month
  if (result.getMonth() !== month - 1) {
    return null;
  }
  
  return result;
}

/**
 * Get all dates in a range
 */
export function getDatesInRange(startDate: Date, endDate: Date): Date[] {
  const dates: Date[] = [];
  const current = startOfDay(startDate);
  const end = startOfDay(endDate);
  
  while (current.getTime() <= end.getTime()) {
    dates.push(new Date(current.getTime()));
    current.setDate(current.getDate() + 1);
  }
  
  return dates;
}

/**
 * Count business days between two dates
 */
export function countBusinessDays(startDate: Date, endDate: Date): number {
  let count = 0;
  const current = startOfDay(startDate);
  const end = startOfDay(endDate);
  
  while (current.getTime() <= end.getTime()) {
    if (isWeekday(current)) {
      count++;
    }
    current.setDate(current.getDate() + 1);
  }
  
  return count;
}

/**
 * Add business days to a date
 */
export function addBusinessDays(date: Date, amount: number): Date {
  const result = new Date(date.getTime());
  let remaining = Math.abs(amount);
  const sign = amount > 0 ? 1 : -1;
  
  while (remaining > 0) {
    result.setDate(result.getDate() + sign);
    if (isWeekday(result)) {
      remaining--;
    }
  }
  
  return result;
}

// ============================================
// Class-based API
// ============================================

/**
 * DateUtils class for chainable date operations
 */
export class DateUtils {
  private date: Date;

  constructor(date: Date = new Date()) {
    this.date = new Date(date.getTime());
  }

  static now(): DateUtils {
    return new DateUtils(new Date());
  }

  static from(timestamp: number): DateUtils {
    return new DateUtils(new Date(timestamp));
  }

  static parse(dateStr: string, format?: string): DateUtils | null {
    const date = parseDate(dateStr, format);
    return date ? new DateUtils(date) : null;
  }

  static create(year: number, month: number, day: number, hour?: number, minute?: number, second?: number): DateUtils {
    return new DateUtils(createDate(year, month, day, hour, minute, second));
  }

  clone(): DateUtils {
    return new DateUtils(this.date);
  }

  toDate(): Date {
    return new Date(this.date.getTime());
  }

  toNumber(): number {
    return this.date.getTime();
  }

  format(formatStr: string): string {
    return format(this.date, formatStr);
  }

  toISO(): string {
    return toISO(this.date);
  }

  // Getters
  getYear(): number { return getYear(this.date); }
  getMonth(): number { return getMonth(this.date); }
  getDay(): number { return getDay(this.date); }
  getHour(): number { return getHour(this.date); }
  getMinute(): number { return getMinute(this.date); }
  getSecond(): number { return getSecond(this.date); }
  getMillisecond(): number { return getMillisecond(this.date); }
  getDayOfWeek(): number { return getDayOfWeek(this.date); }
  getDayOfYear(): number { return getDayOfYear(this.date); }
  getWeekOfYear(): number { return getWeekOfYear(this.date); }
  getQuarter(): number { return getQuarter(this.date); }

  // Arithmetic
  addMilliseconds(amount: number): DateUtils {
    this.date = addMilliseconds(this.date, amount);
    return this;
  }

  addSeconds(amount: number): DateUtils {
    this.date = addSeconds(this.date, amount);
    return this;
  }

  addMinutes(amount: number): DateUtils {
    this.date = addMinutes(this.date, amount);
    return this;
  }

  addHours(amount: number): DateUtils {
    this.date = addHours(this.date, amount);
    return this;
  }

  addDays(amount: number): DateUtils {
    this.date = addDays(this.date, amount);
    return this;
  }

  addWeeks(amount: number): DateUtils {
    this.date = addWeeks(this.date, amount);
    return this;
  }

  addMonths(amount: number): DateUtils {
    this.date = addMonths(this.date, amount);
    return this;
  }

  addYears(amount: number): DateUtils {
    this.date = addYears(this.date, amount);
    return this;
  }

  subtractMilliseconds(amount: number): DateUtils { return this.addMilliseconds(-amount); }
  subtractSeconds(amount: number): DateUtils { return this.addSeconds(-amount); }
  subtractMinutes(amount: number): DateUtils { return this.addMinutes(-amount); }
  subtractHours(amount: number): DateUtils { return this.addHours(-amount); }
  subtractDays(amount: number): DateUtils { return this.addDays(-amount); }
  subtractWeeks(amount: number): DateUtils { return this.addWeeks(-amount); }
  subtractMonths(amount: number): DateUtils { return this.addMonths(-amount); }
  subtractYears(amount: number): DateUtils { return this.addYears(-amount); }

  // Boundary operations
  startOfDay(): DateUtils {
    this.date = startOfDay(this.date);
    return this;
  }

  endOfDay(): DateUtils {
    this.date = endOfDay(this.date);
    return this;
  }

  startOfWeek(startOnSunday?: boolean): DateUtils {
    this.date = startOfWeek(this.date, startOnSunday);
    return this;
  }

  endOfWeek(endOnSaturday?: boolean): DateUtils {
    this.date = endOfWeek(this.date, endOnSaturday);
    return this;
  }

  startOfMonth(): DateUtils {
    this.date = startOfMonth(this.date);
    return this;
  }

  endOfMonth(): DateUtils {
    this.date = endOfMonth(this.date);
    return this;
  }

  startOfYear(): DateUtils {
    this.date = startOfYear(this.date);
    return this;
  }

  endOfYear(): DateUtils {
    this.date = endOfYear(this.date);
    return this;
  }

  // Comparison
  isBefore(date: Date): boolean { return isBefore(this.date, date); }
  isAfter(date: Date): boolean { return isAfter(this.date, date); }
  isSame(date: Date): boolean { return isSame(this.date, date); }
  isSameDay(date: Date): boolean { return isSameDay(this.date, date); }
  isSameMonth(date: Date): boolean { return isSameMonth(this.date, date); }
  isSameYear(date: Date): boolean { return isSameYear(this.date, date); }
  isToday(): boolean { return isToday(this.date); }
  isYesterday(): boolean { return isYesterday(this.date); }
  isTomorrow(): boolean { return isTomorrow(this.date); }
  isPast(): boolean { return isPast(this.date); }
  isFuture(): boolean { return isFuture(this.date); }
  isWeekend(): boolean { return isWeekend(this.date); }
  isWeekday(): boolean { return isWeekday(this.date); }
  isLeapYear(): boolean { return isLeapYear(this.date); }

  // Diff
  diff(date: Date): DateDiff { return diff(this.date, date); }
  diffInMilliseconds(date: Date): number { return diffInMilliseconds(this.date, date); }
  diffInSeconds(date: Date): number { return diffInSeconds(this.date, date); }
  diffInMinutes(date: Date): number { return diffInMinutes(this.date, date); }
  diffInHours(date: Date): number { return diffInHours(this.date, date); }
  diffInDays(date: Date): number { return diffInDays(this.date, date); }
  diffInWeeks(date: Date): number { return diffInWeeks(this.date, date); }
  diffInMonths(date: Date): number { return diffInMonths(this.date, date); }
  diffInYears(date: Date): number { return diffInYears(this.date, date); }

  // Relative time
  fromNow(locale?: string): string { return fromNow(this.date, locale); }
}