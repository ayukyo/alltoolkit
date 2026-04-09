/**
 * Date Utilities Module for TypeScript
 * 
 * A comprehensive date and time manipulation utility module with zero dependencies.
 * 
 * Features:
 * - Date formatting (custom patterns, ISO, locale)
 * - Date parsing (multiple formats, fuzzy parsing)
 * - Date arithmetic (add/subtract days, months, years)
 * - Date comparison (isBefore, isAfter, isBetween)
 * - Relative time (time ago, from now)
 * - Date validation
 * - Timezone utilities
 * - Business day calculations
 * - Quarter and week utilities
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module date_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Day of week enumeration (Sunday = 0)
 */
export enum DayOfWeek {
  Sunday = 0,
  Monday = 1,
  Tuesday = 2,
  Wednesday = 3,
  Thursday = 4,
  Friday = 5,
  Saturday = 6,
}

/**
 * Month enumeration (January = 1)
 */
export enum Month {
  January = 1,
  February = 2,
  March = 3,
  April = 4,
  May = 5,
  June = 6,
  July = 7,
  August = 8,
  September = 9,
  October = 10,
  November = 11,
  December = 12,
}

/**
 * Date format patterns
 */
export const DATE_FORMATS = {
  ISO: 'YYYY-MM-DDTHH:mm:ss.SSSZ',
  ISO_DATE: 'YYYY-MM-DD',
  ISO_TIME: 'HH:mm:ss.SSSZ',
  DATE_ONLY: 'YYYY-MM-DD',
  TIME_ONLY: 'HH:mm:ss',
  DATETIME: 'YYYY-MM-DD HH:mm:ss',
  US: 'MM/DD/YYYY',
  EU: 'DD/MM/YYYY',
  CN: 'YYYY 年 MM 月 DD 日',
  CN_DATETIME: 'YYYY 年 MM 月 DD 日 HH:mm:ss',
  RFC2822: 'ddd, DD MMM YYYY HH:mm:ss ZZ',
  RFC3339: 'YYYY-MM-DDTHH:mm:ssZ',
  HUMAN: 'MMMM D, YYYY',
  HUMAN_DATETIME: 'MMMM D, YYYY h:mm A',
  SHORT: 'M/D/YY',
  COMPACT: 'YYYYMMDD',
  TIMESTAMP: 'x',
} as const;

/**
 * Month names
 */
export const MONTH_NAMES = {
  en: {
    full: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    short: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  },
  zh: {
    full: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
    short: ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月'],
  },
} as const;

/**
 * Day names
 */
export const DAY_NAMES = {
  en: {
    full: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    short: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
  },
  zh: {
    full: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
    short: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
  },
} as const;

/**
 * Format a date using a pattern string
 * @param date - Date to format (Date object, timestamp, or string)
 * @param pattern - Format pattern (default: ISO format)
 * @param locale - Locale for names (default: 'en')
 * @returns Formatted date string
 * 
 * Pattern tokens:
 * - YYYY: 4-digit year
 * - YY: 2-digit year
 * - MM: 2-digit month (01-12)
 * - M: Month (1-12)
 * - MMMM: Full month name
 * - MMM: Short month name
 * - DD: 2-digit day (01-31)
 * - D: Day (1-31)
 * - dddd: Full day name
 * - ddd: Short day name
 * - HH: 2-digit hour (00-23)
 * - H: Hour (0-23)
 * - hh: 2-digit hour (01-12)
 * - h: Hour (1-12)
 * - mm: 2-digit minute (00-59)
 * - m: Minute (0-59)
 * - ss: 2-digit second (00-59)
 * - s: Second (0-59)
 * - SSS: Milliseconds
 * - A: AM/PM
 * - a: am/pm
 * - ZZ: Timezone offset (+0800)
 * - Z: Timezone offset (+08:00)
 * - x: Unix timestamp (ms)
 * 
 * @example
 * ```typescript
 * formatDate(new Date(), 'YYYY-MM-DD'); // "2024-01-15"
 * formatDate(new Date(), 'MMMM D, YYYY', 'en'); // "January 15, 2024"
 * formatDate(new Date(), 'YYYY 年 MM 月 DD 日', 'zh'); // "2024 年 01 月 15 日"
 * ```
 */
export function formatDate(
  date: Date | number | string,
  pattern: string = DATE_FORMATS.ISO,
  locale: 'en' | 'zh' = 'en'
): string {
  const d = toDate(date);
  
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const day = d.getDate();
  const hours = d.getHours();
  const minutes = d.getMinutes();
  const seconds = d.getSeconds();
  const milliseconds = d.getMilliseconds();
  const dayOfWeek = d.getDay();
  
  const timezoneOffset = -d.getTimezoneOffset();
  const tzSign = timezoneOffset >= 0 ? '+' : '-';
  const tzHours = Math.abs(Math.floor(timezoneOffset / 60));
  const tzMinutes = Math.abs(timezoneOffset % 60);
  const tzOffset = `${tzSign}${String(tzHours).padStart(2, '0')}:${String(tzMinutes).padStart(2, '0')}`;
  const tzOffsetCompact = `${tzSign}${String(tzHours).padStart(2, '0')}${String(tzMinutes).padStart(2, '0')}`;
  
  const names = locale === 'zh' ? { months: MONTH_NAMES.zh, days: DAY_NAMES.zh } : { months: MONTH_NAMES.en, days: DAY_NAMES.en };
  
  const replacements: Record<string, string> = {
    'YYYY': String(year),
    'YY': String(year).slice(-2),
    'MM': String(month).padStart(2, '0'),
    'M': String(month),
    'MMMM': names.months.full[month - 1],
    'MMM': names.months.short[month - 1],
    'DD': String(day).padStart(2, '0'),
    'D': String(day),
    'dddd': names.days.full[dayOfWeek],
    'ddd': names.days.short[dayOfWeek],
    'HH': String(hours).padStart(2, '0'),
    'H': String(hours),
    'hh': String(hours % 12 || 12).padStart(2, '0'),
    'h': String(hours % 12 || 12),
    'mm': String(minutes).padStart(2, '0'),
    'm': String(minutes),
    'ss': String(seconds).padStart(2, '0'),
    's': String(seconds),
    'SSS': String(milliseconds).padStart(3, '0'),
    'A': hours >= 12 ? 'PM' : 'AM',
    'a': hours >= 12 ? 'pm' : 'am',
    'ZZ': tzOffsetCompact,
    'Z': tzOffset,
    'x': String(d.getTime()),
  };
  
  // Sort by length (longest first) to avoid partial replacements
  const sortedPatterns = Object.keys(replacements).sort((a, b) => b.length - a.length);
  
  let result = pattern;
  for (const patternKey of sortedPatterns) {
    result = result.split(patternKey).join(replacements[patternKey]);
  }
  
  return result;
}

/**
 * Parse a date string into a Date object
 * @param dateString - Date string to parse
 * @param pattern - Expected format pattern (optional, auto-detect if not provided)
 * @returns Parsed Date object or null if invalid
 * 
 * @example
 * ```typescript
 * parseDate('2024-01-15'); // Date object
 * parseDate('01/15/2024', 'MM/DD/YYYY'); // Date object
 * parseDate('2024 年 01 月 15 日'); // Date object
 * ```
 */
export function parseDate(dateString: string, pattern?: string): Date | null {
  if (!dateString || typeof dateString !== 'string') {
    return null;
  }
  
  const trimmed = dateString.trim();
  
  // Try ISO format first
  const isoMatch = trimmed.match(/^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?(?:\.(\d{3}))?(?:Z|([+-])(\d{2}):?(\d{2}))?)?$/);
  if (isoMatch) {
    const [, year, month, day, hour = '0', minute = '0', second = '0', ms = '0'] = isoMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second), Number(ms));
    return isNaN(date.getTime()) ? null : date;
  }
  
  // Try US format MM/DD/YYYY
  const usMatch = trimmed.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{2})(?::(\d{2}))?)?$/);
  if (usMatch) {
    const [, month, day, year, hour = '0', minute = '0', second = '0'] = usMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
    return isNaN(date.getTime()) ? null : date;
  }
  
  // Try EU format DD/MM/YYYY
  const euMatch = trimmed.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})(?:\s+(\d{1,2}):(\d{2})(?::(\d{2}))?)?$/);
  if (euMatch) {
    const [, day, month, year, hour = '0', minute = '0', second = '0'] = euMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
    return isNaN(date.getTime()) ? null : date;
  }
  
  // Try Chinese format YYYY 年 MM 月 DD 日
  const cnMatch = trimmed.match(/^(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日 (?: (\d{1,2}):(\d{2})(?::(\d{2}))?)?$/);
  if (cnMatch) {
    const [, year, month, day, hour = '0', minute = '0', second = '0'] = cnMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
    return isNaN(date.getTime()) ? null : date;
  }
  
  // Try timestamp
  const timestamp = Number(trimmed);
  if (!isNaN(timestamp) && timestamp.toString().length >= 10) {
    const date = new Date(timestamp);
    return isNaN(date.getTime()) ? null : date;
  }
  
  // Fallback to native Date parsing
  const date = new Date(trimmed);
  return isNaN(date.getTime()) ? null : date;
}

/**
 * Convert various inputs to a Date object
 * @param input - Date, timestamp, or date string
 * @returns Date object
 */
export function toDate(input: Date | number | string): Date {
  if (input instanceof Date) {
    return input;
  }
  if (typeof input === 'number') {
    return new Date(input);
  }
  const parsed = parseDate(input);
  return parsed || new Date();
}

/**
 * Add time to a date
 * @param date - Base date
 * @param amount - Amount to add
 * @param unit - Unit of time ('ms', 's', 'm', 'h', 'd', 'w', 'M', 'y')
 * @returns New Date with added time
 * 
 * @example
 * ```typescript
 * addDays(new Date(), 7); // 7 days from now
 * addMonths(new Date(), 1); // 1 month from now
 * ```
 */
export function addTime(
  date: Date | number | string,
  amount: number,
  unit: 'ms' | 's' | 'm' | 'h' | 'd' | 'w' | 'M' | 'y' = 'd'
): Date {
  const d = toDate(date);
  const result = new Date(d);
  
  switch (unit) {
    case 'ms':
      result.setMilliseconds(result.getMilliseconds() + amount);
      break;
    case 's':
      result.setSeconds(result.getSeconds() + amount);
      break;
    case 'm':
      result.setMinutes(result.getMinutes() + amount);
      break;
    case 'h':
      result.setHours(result.getHours() + amount);
      break;
    case 'd':
      result.setDate(result.getDate() + amount);
      break;
    case 'w':
      result.setDate(result.getDate() + amount * 7);
      break;
    case 'M':
      result.setMonth(result.getMonth() + amount);
      break;
    case 'y':
      result.setFullYear(result.getFullYear() + amount);
      break;
  }
  
  return result;
}

/**
 * Add days to a date
 * @param date - Base date
 * @param days - Number of days to add
 * @returns New Date with added days
 */
export function addDays(date: Date | number | string, days: number): Date {
  return addTime(date, days, 'd');
}

/**
 * Add months to a date
 * @param date - Base date
 * @param months - Number of months to add
 * @returns New Date with added months
 */
export function addMonths(date: Date | number | string, months: number): Date {
  return addTime(date, months, 'M');
}

/**
 * Add years to a date
 * @param date - Base date
 * @param years - Number of years to add
 * @returns New Date with added years
 */
export function addYears(date: Date | number | string, years: number): Date {
  return addTime(date, years, 'y');
}

/**
 * Subtract time from a date
 * @param date - Base date
 * @param amount - Amount to subtract
 * @param unit - Unit of time
 * @returns New Date with subtracted time
 */
export function subtractTime(
  date: Date | number | string,
  amount: number,
  unit: 'ms' | 's' | 'm' | 'h' | 'd' | 'w' | 'M' | 'y' = 'd'
): Date {
  return addTime(date, -amount, unit);
}

/**
 * Subtract days from a date
 * @param date - Base date
 * @param days - Number of days to subtract
 * @returns New Date with subtracted days
 */
export function subtractDays(date: Date | number | string, days: number): Date {
  return subtractTime(date, days, 'd');
}

/**
 * Get the difference between two dates
 * @param date1 - First date
 * @param date2 - Second date
 * @param unit - Unit for result ('ms', 's', 'm', 'h', 'd', 'w', 'M', 'y')
 * @returns Difference in specified unit (can be negative)
 * 
 * @example
 * ```typescript
 * diffDays(new Date(), addDays(new Date(), 7)); // -7
 * diffDays(addDays(new Date(), 7), new Date()); // 7
 * ```
 */
export function diff(
  date1: Date | number | string,
  date2: Date | number | string,
  unit: 'ms' | 's' | 'm' | 'h' | 'd' | 'w' | 'M' | 'y' = 'ms'
): number {
  const d1 = toDate(date1);
  const d2 = toDate(date2);
  const diffMs = d1.getTime() - d2.getTime();
  
  switch (unit) {
    case 'ms':
      return diffMs;
    case 's':
      return Math.floor(diffMs / 1000);
    case 'm':
      return Math.floor(diffMs / (1000 * 60));
    case 'h':
      return Math.floor(diffMs / (1000 * 60 * 60));
    case 'd':
      return Math.floor(diffMs / (1000 * 60 * 60 * 24));
    case 'w':
      return Math.floor(diffMs / (1000 * 60 * 60 * 24 * 7));
    case 'M':
      return (d1.getFullYear() - d2.getFullYear()) * 12 + (d1.getMonth() - d2.getMonth());
    case 'y':
      return d1.getFullYear() - d2.getFullYear();
    default:
      return diffMs;
  }
}

/**
 * Get the difference in days between two dates
 * @param date1 - First date
 * @param date2 - Second date
 * @returns Difference in days
 */
export function diffDays(date1: Date | number | string, date2: Date | number | string): number {
  return diff(date1, date2, 'd');
}

/**
 * Check if a date is before another date
 * @param date - Date to check
 * @param compareTo - Date to compare against
 * @returns True if date is before compareTo
 */
export function isBefore(date: Date | number | string, compareTo: Date | number | string): boolean {
  return toDate(date).getTime() < toDate(compareTo).getTime();
}

/**
 * Check if a date is after another date
 * @param date - Date to check
 * @param compareTo - Date to compare against
 * @returns True if date is after compareTo
 */
export function isAfter(date: Date | number | string, compareTo: Date | number | string): boolean {
  return toDate(date).getTime() > toDate(compareTo).getTime();
}

/**
 * Check if a date is between two dates
 * @param date - Date to check
 * @param start - Start date (inclusive)
 * @param end - End date (inclusive)
 * @returns True if date is between start and end
 */
export function isBetween(
  date: Date | number | string,
  start: Date | number | string,
  end: Date | number | string
): boolean {
  const d = toDate(date).getTime();
  return d >= toDate(start).getTime() && d <= toDate(end).getTime();
}

/**
 * Check if two dates are equal (same time)
 * @param date1 - First date
 * @param date2 - Second date
 * @returns True if dates are equal
 */
export function isEqual(date1: Date | number | string, date2: Date | number | string): boolean {
  return toDate(date1).getTime() === toDate(date2).getTime();
}

/**
 * Check if two dates are equal (same day, ignoring time)
 * @param date1 - First date
 * @param date2 - Second date
 * @returns True if dates are the same day
 */
export function isSameDay(date1: Date | number | string, date2: Date | number | string): boolean {
  const d1 = toDate(date1);
  const d2 = toDate(date2);
  return d1.getFullYear() === d2.getFullYear() &&
         d1.getMonth() === d2.getMonth() &&
         d1.getDate() === d2.getDate();
}

/**
 * Get relative time string (time ago)
 * @param date - Date to compare to now
 * @param locale - Locale for output
 * @returns Relative time string
 * 
 * @example
 * ```typescript
 * timeAgo(new Date(Date.now() - 60000)); // "1 minute ago"
 * timeAgo(new Date(Date.now() - 86400000)); // "1 day ago"
 * ```
 */
export function timeAgo(date: Date | number | string, locale: 'en' | 'zh' = 'en'): string {
  const d = toDate(date);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  
  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);
  
  if (locale === 'zh') {
    if (years > 0) return `${years}年前`;
    if (months > 0) return `${months}个月前`;
    if (days > 0) return `${days}天前`;
    if (hours > 0) return `${hours}小时前`;
    if (minutes > 0) return `${minutes}分钟前`;
    if (seconds > 0) return `${seconds}秒前`;
    return '刚刚';
  } else {
    if (years > 0) return `${years} year${years > 1 ? 's' : ''} ago`;
    if (months > 0) return `${months} month${months > 1 ? 's' : ''} ago`;
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    if (seconds > 0) return `${seconds} second${seconds > 1 ? 's' : ''} ago`;
    return 'just now';
  }
}

/**
 * Get relative time string (from now)
 * @param date - Future date
 * @param locale - Locale for output
 * @returns Relative time string
 * 
 * @example
 * ```typescript
 * fromNow(addDays(new Date(), 7)); // "in 7 days"
 * ```
 */
export function fromNow(date: Date | number | string, locale: 'en' | 'zh' = 'en'): string {
  const d = toDate(date);
  const now = new Date();
  const diffMs = d.getTime() - now.getTime();
  
  if (diffMs < 0) {
    return timeAgo(date, locale);
  }
  
  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);
  
  if (locale === 'zh') {
    if (years > 0) return `${years}年后`;
    if (months > 0) return `${months}个月后`;
    if (days > 0) return `${days}天后`;
    if (hours > 0) return `${hours}小时后`;
    if (minutes > 0) return `${minutes}分钟后`;
    if (seconds > 0) return `${seconds}秒后`;
    return '即将';
  } else {
    if (years > 0) return `in ${years} year${years > 1 ? 's' : ''}`;
    if (months > 0) return `in ${months} month${months > 1 ? 's' : ''}`;
    if (days > 0) return `in ${days} day${days > 1 ? 's' : ''}`;
    if (hours > 0) return `in ${hours} hour${hours > 1 ? 's' : ''}`;
    if (minutes > 0) return `in ${minutes} minute${minutes > 1 ? 's' : ''}`;
    if (seconds > 0) return `in ${seconds} second${seconds > 1 ? 's' : ''}`;
    return 'in a moment';
  }
}

/**
 * Get the start of a time unit
 * @param date - Base date
 * @param unit - Unit ('d', 'w', 'M', 'y')
 * @returns Date at start of unit
 * 
 * @example
 * ```typescript
 * startOfDay(new Date()); // Today at 00:00:00
 * startOfMonth(new Date()); // First day of current month
 * ```
 */
export function startOf(date: Date | number | string, unit: 'd' | 'w' | 'M' | 'y' = 'd'): Date {
  const d = toDate(date);
  const result = new Date(d);
  
  switch (unit) {
    case 'd':
      result.setHours(0, 0, 0, 0);
      break;
    case 'w':
      result.setDate(result.getDate() - result.getDay());
      result.setHours(0, 0, 0, 0);
      break;
    case 'M':
      result.setDate(1);
      result.setHours(0, 0, 0, 0);
      break;
    case 'y':
      result.setMonth(0, 1);
      result.setHours(0, 0, 0, 0);
      break;
  }
  
  return result;
}

/**
 * Get the start of the day
 * @param date - Base date
 * @returns Date at start of day (00:00:00)
 */
export function startOfDay(date: Date | number | string): Date {
  return startOf(date, 'd');
}

/**
 * Get the start of the week (Sunday)
 * @param date - Base date
 * @returns Date at start of week
 */
export function startOfWeek(date: Date | number | string): Date {
  return startOf(date, 'w');
}

/**
 * Get the start of the month
 * @param date - Base date
 * @returns Date at start of month
 */
export function startOfMonth(date: Date | number | string): Date {
  return startOf(date, 'M');
}

/**
 * Get the start of the year
 * @param date - Base date
 * @returns Date at start of year (Jan 1)
 */
export function startOfYear(date: Date | number | string): Date {
  return startOf(date, 'y');
}

/**
 * Get the end of a time unit
 * @param date - Base date
 * @param unit - Unit ('d', 'w', 'M', 'y')
 * @returns Date at end of unit
 * 
 * @example
 * ```typescript
 * endOfDay(new Date()); // Today at 23:59:59.999
 * endOfMonth(new Date()); // Last day of current month
 * ```
 */
export function endOf(date: Date | number | string, unit: 'd' | 'w' | 'M' | 'y' = 'd'): Date {
  const d = toDate(date);
  const result = new Date(d);
  
  switch (unit) {
    case 'd':
      result.setHours(23, 59, 59, 999);
      break;
    case 'w':
      result.setDate(result.getDate() + (6 - result.getDay()));
      result.setHours(23, 59, 59, 999);
      break;
    case 'M':
      result.setMonth(result.getMonth() + 1, 0);
      result.setHours(23, 59, 59, 999);
      break;
    case 'y':
      result.setMonth(11, 31);
      result.setHours(23, 59, 59, 999);
      break;
  }
  
  return result;
}

/**
 * Get the end of the day
 * @param date - Base date
 * @returns Date at end of day (23:59:59.999)
 */
export function endOfDay(date: Date | number | string): Date {
  return endOf(date, 'd');
}

/**
 * Get the end of the week (Saturday)
 * @param date - Base date
 * @returns Date at end of week
 */
export function endOfWeek(date: Date | number | string): Date {
  return endOf(date, 'w');
}

/**
 * Get the end of the month
 * @param date - Base date
 * @returns Date at end of month
 */
export function endOfMonth(date: Date | number | string): Date {
  return endOf(date, 'M');
}

/**
 * Get the end of the year
 * @param date - Base date
 * @returns Date at end of year (Dec 31)
 */
export function endOfYear(date: Date | number | string): Date {
  return endOf(date, 'y');
}

/**
 * Check if a year is a leap year
 * @param year - Year to check (or date to extract year from)
 * @returns True if leap year
 */
export function isLeapYear(year: number | Date | string): boolean {
  const y = typeof year === 'number' ? year : toDate(year).getFullYear();
  return (y % 4 === 0 && y % 100 !== 0) || (y % 400 === 0);
}

/**
 * Get the number of days in a month
 * @param year - Year
 * @param month - Month (1-12)
 * @returns Number of days in the month
 */
export function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month, 0).getDate();
}

/**
 * Get the quarter of a date
 * @param date - Date to check
 * @returns Quarter number (1-4)
 */
export function getQuarter(date: Date | number | string): number {
  const d = toDate(date);
  return Math.floor(d.getMonth() / 3) + 1;
}

/**
 * Get the week number of a date
 * @param date - Date to check
 * @returns Week number (1-53)
 */
export function getWeekNumber(date: Date | number | string): number {
  const d = toDate(date);
  const target = new Date(d.valueOf());
  const dayNr = (d.getDay() + 6) % 7;
  target.setDate(target.getDate() - dayNr + 3);
  const firstThursday = target.valueOf();
  target.setMonth(0, 1);
  if (target.getDay() !== 4) {
    target.setMonth(0, 1 + ((4 - target.getDay() + 7) % 7));
  }
  return 1 + Math.ceil((firstThursday - target.valueOf()) / 604800000);
}

/**
 * Get the day of year (1-366)
 * @param date - Date to check
 * @returns Day of year
 */
export function getDayOfYear(date: Date | number | string): number {
  const d = toDate(date);
  const start = new Date(d.getFullYear(), 0, 0);
  const diff = d.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diff / oneDay);
}

/**
 * Check if a date is a weekend
 * @param date - Date to check
 * @returns True if Saturday or Sunday
 */
export function isWeekend(date: Date | number | string): boolean {
  const d = toDate(date);
  const day = d.getDay();
  return day === DayOfWeek.Saturday || day === DayOfWeek.Sunday;
}

/**
 * Check if a date is a weekday
 * @param date - Date to check
 * @returns True if Monday-Friday
 */
export function isWeekday(date: Date | number | string): boolean {
  return !isWeekend(date);
}

/**
 * Get the next occurrence of a specific day of week
 * @param date - Base date
 * @param dayOfWeek - Target day of week (0-6, Sunday = 0)
 * @returns Date of next occurrence
 * 
 * @example
 * ```typescript
 * nextDay(new Date(), DayOfWeek.Monday); // Next Monday
 * ```
 */
export function nextDay(date: Date | number | string, dayOfWeek: number): Date {
  const d = toDate(date);
  const result = new Date(d);
  const currentDay = d.getDay();
  const daysUntil = (dayOfWeek - currentDay + 7) % 7 || 7;
  result.setDate(d.getDate() + daysUntil);
  return result;
}

/**
 * Get the next Monday
 * @param date - Base date
 * @returns Next Monday
 */
export function nextMonday(date: Date | number | string): Date {
  return nextDay(date, DayOfWeek.Monday);
}

/**
 * Get business days between two dates (excluding weekends)
 * @param start - Start date
 * @param end - End date
 * @returns Number of business days
 */
export function businessDaysBetween(start: Date | number | string, end: Date | number | string): number {
  const s = toDate(start);
  const e = toDate(end);
  
  if (s > e) {
    return businessDaysBetween(e, s);
  }
  
  let count = 0;
  const current = new Date(s);
  
  while (current <= e) {
    if (!isWeekend(current)) {
      count++;
    }
    current.setDate(current.getDate() + 1);
  }
  
  return count;
}

/**
 * Add business days to a date (skipping weekends)
 * @param date - Base date
 * @param days - Number of business days to add
 * @returns Date after adding business days
 */
export function addBusinessDays(date: Date | number | string, days: number): Date {
  const d = toDate(date);
  const result = new Date(d);
  const sign = days >= 0 ? 1 : -1;
  const absDays = Math.abs(days);
  
  let added = 0;
  while (added < absDays) {
    result.setDate(result.getDate() + sign);
    if (!isWeekend(result)) {
      added++;
    }
  }
  
  return result;
}

/**
 * Validate if a date is valid
 * @param date - Date to validate
 * @returns True if valid date
 */
export function isValid(date: unknown): boolean {
  if (date instanceof Date) {
    return !isNaN(date.getTime());
  }
  if (typeof date === 'number') {
    return !isNaN(new Date(date).getTime());
  }
  if (typeof date === 'string') {
    return parseDate(date) !== null;
  }
  return false;
}

/**
 * Get the current timestamp in milliseconds
 * @returns Current timestamp
 */
export function now(): number {
  return Date.now();
}

/**
 * Get the current timestamp in seconds
 * @returns Current timestamp in seconds
 */
export function nowInSeconds(): number {
  return Math.floor(Date.now() / 1000);
}

/**
 * Sleep for a specified duration
 * @param ms - Duration in milliseconds
 * @returns Promise that resolves after the duration
 * 
 * @example
 * ```typescript
 * await sleep(1000); // Wait 1 second
 * ```
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Debounce a function
 * @param func - Function to debounce
 * @param wait - Wait time in milliseconds
 * @returns Debounced function
 */
export function debounce<T extends (...args: unknown[]) => unknown>(func: T, wait: number): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  
  return function (this: unknown, ...args: Parameters<T>) {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

/**
 * Throttle a function
 * @param func - Function to throttle
 * @param limit - Time limit in milliseconds
 * @returns Throttled function
 */
export function throttle<T extends (...args: unknown[]) => unknown>(func: T, limit: number): (...args: Parameters<T>) => void {
  let inThrottle = false;
  
  return function (this: unknown, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// ==================== Default Export ====================

/**
 * Date Utilities namespace
 */
export const DateUtils = {
  // Formatting & Parsing
  formatDate,
  parseDate,
  toDate,
  
  // Arithmetic
  addTime,
  addDays,
  addMonths,
  addYears,
  subtractTime,
  subtractDays,
  
  // Difference
  diff,
  diffDays,
  
  // Comparison
  isBefore,
  isAfter,
  isBetween,
  isEqual,
  isSameDay,
  
  // Relative Time
  timeAgo,
  fromNow,
  
  // Start/End of Period
  startOf,
  startOfDay,
  startOfWeek,
  startOfMonth,
  startOfYear,
  endOf,
  endOfDay,
  endOfWeek,
  endOfMonth,
  endOfYear,
  
  // Utilities
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
  
  // Current Time
  now,
  nowInSeconds,
  
  // Helpers
  sleep,
  debounce,
  throttle,
  
  // Constants
  DATE_FORMATS,
  MONTH_NAMES,
  DAY_NAMES,
  DayOfWeek,
  Month,
};

export default DateUtils;
