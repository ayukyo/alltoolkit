/**
 * Date Utilities Test Suite (Node.js version)
 * 
 * Run with: node --test date_utils_test.node.ts
 */

import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';
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

describe('Date Utils', () => {
  describe('formatDate', () => {
    it('should format ISO date correctly', () => {
      const date = new Date(2024, 0, 15, 14, 30, 45, 123);
      const result = formatDate(date, 'YYYY-MM-DD');
      assert.strictEqual(result, '2024-01-15');
    });

    it('should format US date correctly', () => {
      const date = new Date(2024, 0, 15);
      const result = formatDate(date, 'MM/DD/YYYY');
      assert.strictEqual(result, '01/15/2024');
    });

    it('should format human readable date in English', () => {
      const date = new Date(2024, 0, 15);
      const result = formatDate(date, 'MMMM D, YYYY', 'en');
      assert.strictEqual(result, 'January 15, 2024');
    });

    it('should format date in Chinese', () => {
      const date = new Date(2024, 0, 15);
      const result = formatDate(date, 'YYYY 年 MM 月 DD 日', 'zh');
      assert.strictEqual(result, '2024 年 01 月 15 日');
    });

    it('should format time correctly', () => {
      const date = new Date(2024, 0, 15, 14, 30, 45);
      const result = formatDate(date, 'HH:mm:ss');
      assert.strictEqual(result, '14:30:45');
    });

    it('should format 12-hour time correctly', () => {
      const date = new Date(2024, 0, 15, 14, 30);
      const result = formatDate(date, 'h:mm A');
      assert.strictEqual(result, '2:30 PM');
    });
  });

  describe('parseDate', () => {
    it('should parse ISO format', () => {
      const result = parseDate('2024-01-15');
      assert.ok(result);
      assert.strictEqual(result!.getFullYear(), 2024);
      assert.strictEqual(result!.getMonth(), 0);
      assert.strictEqual(result!.getDate(), 15);
    });

    it('should parse US format', () => {
      const result = parseDate('01/15/2024');
      assert.ok(result);
      assert.strictEqual(result!.getFullYear(), 2024);
    });

    it('should parse Chinese format', () => {
      const result = parseDate('2024 年 01 月 15 日');
      assert.ok(result);
      assert.strictEqual(result!.getFullYear(), 2024);
    });

    it('should return null for invalid date', () => {
      const result = parseDate('not-a-date');
      assert.strictEqual(result, null);
    });
  });

  describe('date arithmetic', () => {
    it('should add days correctly', () => {
      const baseDate = new Date(2024, 0, 15);
      const result = addDays(baseDate, 7);
      assert.strictEqual(result.getDate(), 22);
    });

    it('should add months correctly', () => {
      const baseDate = new Date(2024, 0, 15);
      const result = addMonths(baseDate, 2);
      assert.strictEqual(result.getMonth(), 2);
    });

    it('should add years correctly', () => {
      const baseDate = new Date(2024, 0, 15);
      const result = addYears(baseDate, 1);
      assert.strictEqual(result.getFullYear(), 2025);
    });

    it('should subtract days correctly', () => {
      const baseDate = new Date(2024, 0, 15);
      const result = subtractDays(baseDate, 5);
      assert.strictEqual(result.getDate(), 10);
    });

    it('should handle month overflow', () => {
      const jan31 = new Date(2024, 0, 31);
      const result = addMonths(jan31, 1);
      assert.strictEqual(result.getMonth(), 1);
    });
  });

  describe('date difference', () => {
    it('should calculate days difference correctly', () => {
      const date1 = new Date(2024, 0, 1);
      const date2 = new Date(2024, 0, 11);
      const result = diffDays(date2, date1);
      assert.strictEqual(result, 10);
    });
  });

  describe('date comparison', () => {
    const date1 = new Date(2024, 0, 1);
    const date2 = new Date(2024, 0, 15);
    const date3 = new Date(2024, 0, 1);

    it('should check isBefore correctly', () => {
      assert.ok(isBefore(date1, date2));
    });

    it('should check isAfter correctly', () => {
      assert.ok(isAfter(date2, date1));
    });

    it('should check isBetween correctly', () => {
      assert.ok(isBetween(date2, date1, new Date(2024, 1, 1)));
    });

    it('should check isEqual correctly', () => {
      assert.ok(isEqual(date1, date3));
    });

    it('should check isSameDay correctly', () => {
      assert.ok(isSameDay(date1, date3));
      assert.ok(!isSameDay(date1, date2));
    });
  });

  describe('relative time', () => {
    it('should show time ago in English', () => {
      const now = new Date();
      const oneMinuteAgo = new Date(now.getTime() - 60000);
      const result = timeAgo(oneMinuteAgo, 'en');
      assert.ok(result.includes('minute'));
    });

    it('should show time ago in Chinese', () => {
      const now = new Date();
      const oneDayAgo = new Date(now.getTime() - 86400000);
      const result = timeAgo(oneDayAgo, 'zh');
      assert.ok(result.includes('天'));
    });
  });

  describe('startOf/endOf', () => {
    it('should get start of day', () => {
      const date = new Date(2024, 5, 15, 14, 30, 45);
      const result = startOfDay(date);
      assert.strictEqual(result.getHours(), 0);
      assert.strictEqual(result.getMinutes(), 0);
      assert.strictEqual(result.getSeconds(), 0);
    });

    it('should get end of day', () => {
      const date = new Date(2024, 5, 15, 14, 30, 45);
      const result = endOfDay(date);
      assert.strictEqual(result.getHours(), 23);
      assert.strictEqual(result.getMinutes(), 59);
    });

    it('should get start of month', () => {
      const date = new Date(2024, 5, 15);
      const result = startOfMonth(date);
      assert.strictEqual(result.getDate(), 1);
    });

    it('should get end of month', () => {
      const date = new Date(2024, 5, 15); // June
      const result = endOfMonth(date);
      assert.strictEqual(result.getDate(), 30);
    });

    it('should get start of year', () => {
      const date = new Date(2024, 5, 15);
      const result = startOfYear(date);
      assert.strictEqual(result.getMonth(), 0);
      assert.strictEqual(result.getDate(), 1);
    });

    it('should get end of year', () => {
      const date = new Date(2024, 5, 15);
      const result = endOfYear(date);
      assert.strictEqual(result.getMonth(), 11);
      assert.strictEqual(result.getDate(), 31);
    });
  });

  describe('utilities', () => {
    it('should check leap year correctly', () => {
      assert.ok(isLeapYear(2024));
      assert.ok(!isLeapYear(2023));
      assert.ok(isLeapYear(2000));
      assert.ok(!isLeapYear(1900));
    });

    it('should get days in month correctly', () => {
      assert.strictEqual(getDaysInMonth(2024, 2), 29);
      assert.strictEqual(getDaysInMonth(2023, 2), 28);
      assert.strictEqual(getDaysInMonth(2024, 1), 31);
    });

    it('should get quarter correctly', () => {
      assert.strictEqual(getQuarter(new Date(2024, 0, 15)), 1);
      assert.strictEqual(getQuarter(new Date(2024, 3, 15)), 2);
      assert.strictEqual(getQuarter(new Date(2024, 6, 15)), 3);
      assert.strictEqual(getQuarter(new Date(2024, 9, 15)), 4);
    });

    it('should check weekend correctly', () => {
      assert.ok(isWeekend(new Date(2024, 0, 13))); // Saturday
      assert.ok(isWeekend(new Date(2024, 0, 14))); // Sunday
      assert.ok(!isWeekend(new Date(2024, 0, 15))); // Monday
    });

    it('should check weekday correctly', () => {
      assert.ok(isWeekday(new Date(2024, 0, 15)));
      assert.ok(!isWeekday(new Date(2024, 0, 13)));
    });
  });

  describe('nextDay', () => {
    it('should get next Monday', () => {
      const monday = new Date(2024, 0, 15); // Monday
      const result = nextMonday(monday);
      assert.strictEqual(result.getDate(), 22);
    });

    it('should get next Friday', () => {
      const monday = new Date(2024, 0, 15);
      const result = nextDay(monday, DayOfWeek.Friday);
      assert.strictEqual(result.getDate(), 19);
    });
  });

  describe('business days', () => {
    it('should count business days correctly', () => {
      const start = new Date(2024, 0, 15); // Monday
      const end = new Date(2024, 0, 19); // Friday
      const result = businessDaysBetween(start, end);
      assert.strictEqual(result, 5);
    });

    it('should add business days correctly', () => {
      const start = new Date(2024, 0, 15); // Monday
      const result = addBusinessDays(start, 5);
      assert.strictEqual(result.getDate(), 22); // Next Monday
    });
  });

  describe('validation', () => {
    it('should validate date correctly', () => {
      assert.ok(isValid(new Date()));
      assert.ok(isValid(Date.now()));
      assert.ok(isValid('2024-01-15'));
      assert.ok(!isValid('not-a-date'));
      assert.ok(!isValid(NaN));
    });
  });

  describe('constants', () => {
    it('should have correct format constants', () => {
      assert.strictEqual(DATE_FORMATS.ISO, 'YYYY-MM-DDTHH:mm:ss.SSSZ');
    });

    it('should have correct enum values', () => {
      assert.strictEqual(DayOfWeek.Monday, 1);
      assert.strictEqual(Month.January, 1);
    });
  });
});
