/**
 * duration_utils - Parse and format human-readable duration strings
 * 
 * Features:
 * - Parse duration strings like "2h30m", "1d 4h 30m", "5 minutes", "2小时30分"
 * - Support multiple unit formats (short: h, m, s / long: hour, minute, second)
 * - Support Chinese units (天, 小时, 分钟, 秒)
 * - Format milliseconds to human-readable duration strings
 * - Zero external dependencies
 * 
 * @module duration_utils
 */

/** Duration units with their millisecond equivalents */
const UNIT_MS: Record<string, number> = {
  // Milliseconds
  'ms': 1,
  'millisecond': 1,
  'milliseconds': 1,
  '毫秒': 1,

  // Seconds
  's': 1000,
  'sec': 1000,
  'second': 1000,
  'seconds': 1000,
  '秒': 1000,

  // Minutes
  'm': 60 * 1000,
  'min': 60 * 1000,
  'minute': 60 * 1000,
  'minutes': 60 * 1000,
  '分钟': 60 * 1000,
  '分': 60 * 1000,

  // Hours
  'h': 60 * 60 * 1000,
  'hr': 60 * 60 * 1000,
  'hour': 60 * 60 * 1000,
  'hours': 60 * 60 * 1000,
  '小时': 60 * 60 * 1000,
  '时': 60 * 60 * 1000,

  // Days
  'd': 24 * 60 * 60 * 1000,
  'day': 24 * 60 * 60 * 1000,
  'days': 24 * 60 * 60 * 1000,
  '天': 24 * 60 * 60 * 1000,
  '日': 24 * 60 * 60 * 1000,

  // Weeks
  'w': 7 * 24 * 60 * 60 * 1000,
  'week': 7 * 24 * 60 * 60 * 1000,
  'weeks': 7 * 24 * 60 * 60 * 1000,
  '周': 7 * 24 * 60 * 60 * 1000,

  // Months (approximate, 30 days)
  'mo': 30 * 24 * 60 * 60 * 1000,
  'month': 30 * 24 * 60 * 60 * 1000,
  'months': 30 * 24 * 60 * 60 * 1000,
  '月': 30 * 24 * 60 * 60 * 1000,

  // Years (approximate, 365 days)
  'y': 365 * 24 * 60 * 60 * 1000,
  'year': 365 * 24 * 60 * 60 * 1000,
  'years': 365 * 24 * 60 * 60 * 1000,
  '年': 365 * 24 * 60 * 60 * 1000,
};

/** Unit order from largest to smallest for formatting */
const UNIT_ORDER: Array<[string, number, string]> = [
  ['y', 365 * 24 * 60 * 60 * 1000, '年'],
  ['mo', 30 * 24 * 60 * 60 * 1000, '月'],
  ['w', 7 * 24 * 60 * 60 * 1000, '周'],
  ['d', 24 * 60 * 60 * 1000, '天'],
  ['h', 60 * 60 * 1000, '小时'],
  ['m', 60 * 1000, '分钟'],
  ['s', 1000, '秒'],
  ['ms', 1, '毫秒'],
];

/** Parse options */
export interface ParseOptions {
  /** Default unit when number has no unit (default: 'ms') */
  defaultUnit?: string;
  /** Allow negative durations (default: true) */
  allowNegative?: boolean;
  /** Throw on invalid input (default: false, returns 0) */
  strict?: boolean;
}

/** Format options */
export interface FormatOptions {
  /** Maximum units to display (default: 3) */
  maxUnits?: number;
  /** Use short unit names (default: false) */
  short?: boolean;
  /** Use Chinese unit names (default: false) */
  chinese?: boolean;
  /** Show milliseconds (default: true if remainder < 1s) */
  showMs?: boolean;
  /** Separator between units (default: ' ') */
  separator?: string;
}

/**
 * Parse a duration string to milliseconds
 * 
 * @example
 * ```ts
 * parse('2h30m')        // 9000000 (2 hours 30 minutes)
 * parse('1d 4h 30m')    // 102600000 (1 day 4 hours 30 minutes)
 * parse('5 minutes')    // 300000
 * parse('2小时30分')    // 9000000
 * parse('1h 30m 45s')   // 5445000
 * parse(3600)           // 3600 (number treated as ms)
 * parse('100', { defaultUnit: 's' })  // 100000 (100 seconds)
 * ```
 */
export function parse(input: string | number, options: ParseOptions = {}): number {
  const { defaultUnit = 'ms', allowNegative = true, strict = false } = options;

  // Handle number input
  if (typeof input === 'number') {
    if (!allowNegative && input < 0) {
      if (strict) throw new Error('Negative durations not allowed');
      return 0;
    }
    return input;
  }

  // Handle empty or invalid input
  if (!input || typeof input !== 'string') {
    if (strict) throw new Error('Invalid input: empty or non-string');
    return 0;
  }

  const trimmed = input.trim();
  if (!trimmed) {
    if (strict) throw new Error('Invalid input: empty string');
    return 0;
  }

  let totalMs = 0;
  let isNegative = false;
  let remaining = trimmed;

  // Check for negative
  if (remaining.startsWith('-')) {
    isNegative = true;
    remaining = remaining.slice(1).trim();
  }

  // Pattern to match number + optional unit
  const pattern = /(\d+(?:\.\d+)?)\s*([a-zA-Z\u4e00-\u9fff]+)?/g;
  let match;
  let hasMatch = false;

  while ((match = pattern.exec(remaining)) !== null) {
    const value = parseFloat(match[1]);
    const unit = (match[2] || defaultUnit).toLowerCase();

    if (isNaN(value)) continue;

    const multiplier = UNIT_MS[unit];
    if (multiplier === undefined) {
      if (strict) throw new Error(`Unknown unit: ${unit}`);
      continue;
    }

    totalMs += value * multiplier;
    hasMatch = true;
  }

  if (!hasMatch && strict) {
    throw new Error(`No valid duration found in: ${input}`);
  }

  if (!allowNegative && isNegative) {
    if (strict) throw new Error('Negative durations not allowed');
    return 0;
  }

  return isNegative ? -totalMs : totalMs;
}

/**
 * Format milliseconds to human-readable duration string
 * 
 * @example
 * ```ts
 * format(9000000)                    // '2h 30m'
 * format(9000000, { short: false })  // '2 hours 30 minutes'
 * format(9000000, { chinese: true }) // '2小时 30分钟'
 * format(5445000, { maxUnits: 2 })    // '1h 30m'
 * format(1000, { separator: ', ' })  // '1s'
 * ```
 */
export function format(ms: number, options: FormatOptions = {}): string {
  const {
    maxUnits = 3,
    short = true,
    chinese = false,
    showMs,
    separator = ' ',
  } = options;

  if (ms === 0) {
    if (chinese) return '0毫秒';
    return short ? '0ms' : '0 milliseconds';
  }

  const isNegative = ms < 0;
  const absMs = Math.abs(ms);
  const parts: string[] = [];

  let remaining = absMs;
  let unitCount = 0;

  for (const [shortUnit, unitMs, chineseUnit] of UNIT_ORDER) {
    if (unitCount >= maxUnits) break;

    // Skip ms unless explicitly requested or it's the only unit left
    if (shortUnit === 'ms') {
      const shouldShowMs = showMs === true || (showMs !== false && absMs < 1000 && parts.length === 0);
      if (!shouldShowMs) continue;
    }

    if (remaining >= unitMs || (parts.length === 0 && shortUnit === 'ms')) {
      const value = Math.floor(remaining / unitMs);
      remaining -= value * unitMs;

      if (value > 0 || (parts.length === 0 && remaining === 0)) {
        let unitName: string;
        if (chinese) {
          unitName = chineseUnit;
        } else if (short) {
          unitName = shortUnit;
        } else {
          // Long English unit names
          const longNames: Record<string, string> = {
            'y': value === 1 ? 'year' : 'years',
            'mo': value === 1 ? 'month' : 'months',
            'w': value === 1 ? 'week' : 'weeks',
            'd': value === 1 ? 'day' : 'days',
            'h': value === 1 ? 'hour' : 'hours',
            'm': value === 1 ? 'minute' : 'minutes',
            's': value === 1 ? 'second' : 'seconds',
            'ms': value === 1 ? 'millisecond' : 'milliseconds',
          };
          unitName = longNames[shortUnit] || shortUnit;
        }

        // Chinese: no space between number and unit, short English: no space
        const spaceBetween = chinese ? '' : (short ? '' : ' ');
        parts.push(`${value}${spaceBetween}${unitName}`);
        unitCount++;
      }
    }
  }

  const result = parts.join(separator) || (short ? '0ms' : '0 milliseconds');
  return isNegative ? `-${result}` : result;
}

/**
 * Parse and format duration (convenience function)
 * 
 * @example
 * ```ts
 * parseFormat('2h30m', { chinese: true })  // '2小时 30分钟'
 * ```
 */
export function parseFormat(input: string | number, formatOptions?: FormatOptions): string {
  return format(parse(input), formatOptions);
}

/**
 * Add duration to a date
 * 
 * @example
 * ```ts
 * const future = addDuration(new Date(), '2h30m')
 * ```
 */
export function addDuration(date: Date, duration: string | number): Date {
  return new Date(date.getTime() + parse(duration));
}

/**
 * Subtract duration from a date
 * 
 * @example
 * ```ts
 * const past = subtractDuration(new Date(), '1d')
 * ```
 */
export function subtractDuration(date: Date, duration: string | number): Date {
  return new Date(date.getTime() - parse(duration));
}

/**
 * Get the difference between two dates as a duration string
 * 
 * @example
 * ```ts
 * const diff = diffDates(new Date(), new Date(Date.now() + 3600000))
 * // '1h'
 * ```
 */
export function diffDates(date1: Date, date2: Date, formatOptions?: FormatOptions): string {
  return format(Math.abs(date2.getTime() - date1.getTime()), formatOptions);
}

/**
 * Check if a string looks like a duration
 * 
 * @example
 * ```ts
 * isDuration('2h30m')   // true
 * isDuration('hello')   // false
 * ```
 */
export function isDuration(input: string): boolean {
  if (!input || typeof input !== 'string') return false;
  const pattern = /^-?\s*\d+(?:\.\d+)?\s*[a-zA-Z\u4e00-\u9fff]*\s*/;
  return pattern.test(input.trim());
}

/**
 * Normalize a duration string to a canonical form
 * 
 * @example
 * ```ts
 * normalize('2 hours 30 minutes')  // '2h 30m'
 * normalize('1天2小时', { chinese: true })  // '1天 2小时'
 * ```
 */
export function normalize(input: string | number, options?: FormatOptions): string {
  return format(parse(input), options);
}

/**
 * Convert duration to specific unit
 * 
 * @example
 * ```ts
 * toUnit('2h30m', 'minutes')  // 150
 * toUnit('1d', 'hours')       // 24
 * ```
 */
export function toUnit(input: string | number, unit: string): number {
  const ms = parse(input);
  const unitMs = UNIT_MS[unit.toLowerCase()];
  if (!unitMs) throw new Error(`Unknown unit: ${unit}`);
  return ms / unitMs;
}

/**
 * Duration class for fluent API
 * 
 * @example
 * ```ts
 * const d = Duration.from('2h30m')
 *   .add('30m')
 *   .subtract('15m')
 * d.toMilliseconds()  // 9900000
 * d.toString()        // '2h 45m'
 * ```
 */
export class Duration {
  private ms: number;

  constructor(ms: number = 0) {
    this.ms = ms;
  }

  static from(input: string | number): Duration {
    return new Duration(parse(input));
  }

  static between(date1: Date, date2: Date): Duration {
    return new Duration(Math.abs(date2.getTime() - date1.getTime()));
  }

  add(duration: string | number | Duration): Duration {
    if (duration instanceof Duration) {
      this.ms += duration.toMilliseconds();
    } else {
      this.ms += parse(duration);
    }
    return this;
  }

  subtract(duration: string | number | Duration): Duration {
    if (duration instanceof Duration) {
      this.ms -= duration.toMilliseconds();
    } else {
      this.ms -= parse(duration);
    }
    return this;
  }

  multiply(factor: number): Duration {
    this.ms *= factor;
    return this;
  }

  divide(factor: number): Duration {
    this.ms /= factor;
    return this;
  }

  toMilliseconds(): number {
    return this.ms;
  }

  toSeconds(): number {
    return this.ms / 1000;
  }

  toMinutes(): number {
    return this.ms / (60 * 1000);
  }

  toHours(): number {
    return this.ms / (60 * 60 * 1000);
  }

  toDays(): number {
    return this.ms / (24 * 60 * 60 * 1000);
  }

  format(options?: FormatOptions): string {
    return format(this.ms, options);
  }

  toString(): string {
    return this.format();
  }

  valueOf(): number {
    return this.ms;
  }
}

// Export all functions and class
export default {
  parse,
  format,
  parseFormat,
  addDuration,
  subtractDuration,
  diffDates,
  isDuration,
  normalize,
  toUnit,
  Duration,
};