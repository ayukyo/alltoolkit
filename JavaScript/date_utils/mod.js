/**
 * Date Utilities - JavaScript 日期时间工具模块
 * 
 * 提供常用的日期时间操作函数，包括格式化、解析、计算、比较等
 * 零依赖，仅使用 JavaScript 标准库
 * 
 * @module date_utils
 * @version 1.0.0
 */

const DateUtils = {
  // ==================== 常量定义 ====================
  
  /**
   * 时间单位常量（毫秒）
   */
  MS: {
    SECOND: 1000,
    MINUTE: 60 * 1000,
    HOUR: 60 * 60 * 1000,
    DAY: 24 * 60 * 60 * 1000,
    WEEK: 7 * 24 * 60 * 60 * 1000,
    YEAR: 365 * 24 * 60 * 60 * 1000,
  },

  /**
   * 星期名称（中文）
   */
  WEEKDAYS_CN: ['日', '一', '二', '三', '四', '五', '六'],

  /**
   * 星期名称（英文）
   */
  WEEKDAYS_EN: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

  /**
   * 星期名称（英文简写）
   */
  WEEKDAYS_SHORT: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],

  /**
   * 月份名称（中文）
   */
  MONTHS_CN: ['一月', '二月', '三月', '四月', '五月', '六月', 
             '七月', '八月', '九月', '十月', '十一月', '十二月'],

  /**
   * 月份名称（英文）
   */
  MONTHS_EN: ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December'],

  /**
   * 月份名称（英文简写）
   */
  MONTHS_SHORT: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],

  // ==================== 创建日期 ====================

  /**
   * 获取当前时间
   * @returns {Date} 当前时间
   */
  now() {
    return new Date();
  },

  /**
   * 获取当前时间戳（毫秒）
   * @returns {number} 时间戳
   */
  timestamp() {
    return Date.now();
  },

  /**
   * 获取当前时间戳（秒）
   * @returns {number} 时间戳（秒）
   */
  unix() {
    return Math.floor(Date.now() / 1000);
  },

  /**
   * 从时间戳创建日期
   * @param {number} ts - 时间戳（毫秒或秒）
   * @returns {Date} 日期对象
   */
  fromTimestamp(ts) {
    // 自动判断是秒还是毫秒
    if (ts < 1e12) {
      return new Date(ts * 1000);
    }
    return new Date(ts);
  },

  /**
   * 创建日期（支持多种输入格式）
   * @param {Date|string|number} input - 日期输入
   * @returns {Date|null} 日期对象或 null
   */
  create(input) {
    if (!input) return null;
    if (input instanceof Date) return new Date(input);
    if (typeof input === 'number') return this.fromTimestamp(input);
    if (typeof input === 'string') {
      const date = new Date(input);
      return isNaN(date.getTime()) ? null : date;
    }
    return null;
  },

  /**
   * 创建指定日期
   * @param {number} year - 年
   * @param {number} month - 月（1-12）
   * @param {number} [day=1] - 日
   * @param {number} [hour=0] - 时
   * @param {number} [minute=0] - 分
   * @param {number} [second=0] - 秒
   * @param {number} [ms=0] - 毫秒
   * @returns {Date} 日期对象
   */
  createFrom(year, month, day = 1, hour = 0, minute = 0, second = 0, ms = 0) {
    return new Date(year, month - 1, day, hour, minute, second, ms);
  },

  // ==================== 获取日期组件 ====================

  /**
   * 获取年份
   * @param {Date} date - 日期
   * @returns {number} 年份
   */
  getYear(date) {
    return date.getFullYear();
  },

  /**
   * 获取月份（1-12）
   * @param {Date} date - 日期
   * @returns {number} 月份
   */
  getMonth(date) {
    return date.getMonth() + 1;
  },

  /**
   * 获取日期（1-31）
   * @param {Date} date - 日期
   * @returns {number} 日
   */
  getDay(date) {
    return date.getDate();
  },

  /**
   * 获取星期（0-6，0为周日）
   * @param {Date} date - 日期
   * @returns {number} 星期
   */
  getWeekday(date) {
    return date.getDay();
  },

  /**
   * 获取小时（0-23）
   * @param {Date} date - 日期
   * @returns {number} 小时
   */
  getHour(date) {
    return date.getHours();
  },

  /**
   * 获取分钟（0-59）
   * @param {Date} date - 日期
   * @returns {number} 分钟
   */
  getMinute(date) {
    return date.getMinutes();
  },

  /**
   * 获取秒（0-59）
   * @param {Date} date - 日期
   * @returns {number} 秒
   */
  getSecond(date) {
    return date.getSeconds();
  },

  /**
   * 获取毫秒（0-999）
   * @param {Date} date - 日期
   * @returns {number} 毫秒
   */
  getMillisecond(date) {
    return date.getMilliseconds();
  },

  /**
   * 获取一年中的第几天（1-366）
   * @param {Date} date - 日期
   * @returns {number} 第几天
   */
  getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    return Math.floor(diff / this.MS.DAY);
  },

  /**
   * 获取一年中的第几周（ISO周）
   * @param {Date} date - 日期
   * @returns {number} 第几周
   */
  getWeekOfYear(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / this.MS.DAY) + 1) / 7);
  },

  /**
   * 获取季度（1-4）
   * @param {Date} date - 日期
   * @returns {number} 季度
   */
  getQuarter(date) {
    return Math.floor(date.getMonth() / 3) + 1;
  },

  /**
   * 获取月份天数
   * @param {Date} date - 日期
   * @returns {number} 天数
   */
  getDaysInMonth(date) {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  },

  // ==================== 日期计算 ====================

  /**
   * 添加年
   * @param {Date} date - 日期
   * @param {number} years - 年数
   * @returns {Date} 新日期
   */
  addYears(date, years) {
    const result = new Date(date);
    const originalMonth = result.getMonth();
    const originalDay = result.getDate();
    const newYear = result.getFullYear() + years;
    
    // 设置新年份，保留原月和日
    result.setFullYear(newYear, originalMonth, originalDay);
    
    // 处理闰年问题：如 2月29日 + 1年 → 2月28日（而不是 3月1日）
    if (result.getMonth() !== originalMonth) {
      // 月份变了，说明目标年份没有这一天
      // 设置为该月的最后一天
      result.setFullYear(newYear, originalMonth + 1, 0); // 下个月的第0天 = 本月最后一天
    }
    return result;
  },

  /**
   * 添加月
   * @param {Date} date - 日期
   * @param {number} months - 月数
   * @returns {Date} 新日期
   */
  addMonths(date, months) {
    const result = new Date(date);
    const expectedMonth = (result.getMonth() + months) % 12;
    result.setMonth(result.getMonth() + months);
    // 处理月份溢出（如 1月31日 + 1月 = 2月28/29日，但 JS 会变成 3月3日）
    if (result.getMonth() !== (expectedMonth + 12) % 12) {
      result.setDate(0); // 设置为上月最后一天
    }
    return result;
  },

  /**
   * 添加天
   * @param {Date} date - 日期
   * @param {number} days - 天数
   * @returns {Date} 新日期
   */
  addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  },

  /**
   * 添加小时
   * @param {Date} date - 日期
   * @param {number} hours - 小时数
   * @returns {Date} 新日期
   */
  addHours(date, hours) {
    return new Date(date.getTime() + hours * this.MS.HOUR);
  },

  /**
   * 添加分钟
   * @param {Date} date - 日期
   * @param {number} minutes - 分钟数
   * @returns {Date} 新日期
   */
  addMinutes(date, minutes) {
    return new Date(date.getTime() + minutes * this.MS.MINUTE);
  },

  /**
   * 添加秒
   * @param {Date} date - 日期
   * @param {number} seconds - 秒数
   * @returns {Date} 新日期
   */
  addSeconds(date, seconds) {
    return new Date(date.getTime() + seconds * this.MS.SECOND);
  },

  /**
   * 添加毫秒
   * @param {Date} date - 日期
   * @param {number} ms - 毫秒数
   * @returns {Date} 新日期
   */
  addMilliseconds(date, ms) {
    return new Date(date.getTime() + ms);
  },

  /**
   * 计算两个日期之间的天数差
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} 天数差（date2 - date1）
   */
  diffDays(date1, date2) {
    const d1 = this.startOfDay(date1);
    const d2 = this.startOfDay(date2);
    return Math.round((d2 - d1) / this.MS.DAY);
  },

  /**
   * 计算两个日期之间的小时差
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} 小时差
   */
  diffHours(date1, date2) {
    return (date2 - date1) / this.MS.HOUR;
  },

  /**
   * 计算两个日期之间的分钟差
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} 分钟差
   */
  diffMinutes(date1, date2) {
    return (date2 - date1) / this.MS.MINUTE;
  },

  /**
   * 计算两个日期之间的秒差
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} 秒差
   */
  diffSeconds(date1, date2) {
    return (date2 - date1) / this.MS.SECOND;
  },

  /**
   * 计算两个日期之间的毫秒差
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} 毫秒差
   */
  diffMilliseconds(date1, date2) {
    return date2 - date1;
  },

  // ==================== 日期比较 ====================

  /**
   * 判断是否为同一日
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {boolean} 是否同一天
   */
  isSameDay(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getDate() === date2.getDate();
  },

  /**
   * 判断是否为同一周（ISO周）
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {boolean} 是否同一周
   */
  isSameWeek(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
           this.getWeekOfYear(date1) === this.getWeekOfYear(date2);
  },

  /**
   * 判断是否为同一月
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {boolean} 是否同一月
   */
  isSameMonth(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
           date1.getMonth() === date2.getMonth();
  },

  /**
   * 判断是否为同一年
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {boolean} 是否同一年
   */
  isSameYear(date1, date2) {
    return date1.getFullYear() === date2.getFullYear();
  },

  /**
   * 判断是否在今天之前
   * @param {Date} date - 日期
   * @returns {boolean} 是否在今天之前
   */
  isBefore(date) {
    return date < this.startOfDay(new Date());
  },

  /**
   * 判断是否在今天之后
   * @param {Date} date - 日期
   * @returns {boolean} 是否在今天之后
   */
  isAfter(date) {
    return date > this.endOfDay(new Date());
  },

  /**
   * 判断是否为今天
   * @param {Date} date - 日期
   * @returns {boolean} 是否为今天
   */
  isToday(date) {
    return this.isSameDay(date, new Date());
  },

  /**
   * 判断是否为昨天
   * @param {Date} date - 日期
   * @returns {boolean} 是否为昨天
   */
  isYesterday(date) {
    return this.isSameDay(date, this.addDays(new Date(), -1));
  },

  /**
   * 判断是否为明天
   * @param {Date} date - 日期
   * @returns {boolean} 是否为明天
   */
  isTomorrow(date) {
    return this.isSameDay(date, this.addDays(new Date(), 1));
  },

  /**
   * 判断是否为工作日（周一到周五）
   * @param {Date} date - 日期
   * @returns {boolean} 是否为工作日
   */
  isWeekday(date) {
    const day = date.getDay();
    return day > 0 && day < 6;
  },

  /**
   * 判断是否为周末
   * @param {Date} date - 日期
   * @returns {boolean} 是否为周末
   */
  isWeekend(date) {
    const day = date.getDay();
    return day === 0 || day === 6;
  },

  /**
   * 判断是否为闰年
   * @param {Date|number} input - 日期或年份
   * @returns {boolean} 是否为闰年
   */
  isLeapYear(input) {
    const year = input instanceof Date ? input.getFullYear() : input;
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
  },

  /**
   * 判断日期是否在范围内
   * @param {Date} date - 日期
   * @param {Date} start - 开始日期
   * @param {Date} end - 结束日期
   * @returns {boolean} 是否在范围内
   */
  isBetween(date, start, end) {
    return date >= start && date <= end;
  },

  // ==================== 日期边界 ====================

  /**
   * 获取一天的开始时间（00:00:00）
   * @param {Date} date - 日期
   * @returns {Date} 一天的开始
   */
  startOfDay(date) {
    const result = new Date(date);
    result.setHours(0, 0, 0, 0);
    return result;
  },

  /**
   * 获取一天的结束时间（23:59:59.999）
   * @param {Date} date - 日期
   * @returns {Date} 一天的结束
   */
  endOfDay(date) {
    const result = new Date(date);
    result.setHours(23, 59, 59, 999);
    return result;
  },

  /**
   * 获取一周的开始（周一）
   * @param {Date} date - 日期
   * @returns {Date} 一周的开始
   */
  startOfWeek(date) {
    const result = new Date(date);
    const day = result.getDay();
    const diff = result.getDate() - day + (day === 0 ? -6 : 1);
    result.setDate(diff);
    return this.startOfDay(result);
  },

  /**
   * 获取一周的结束（周日）
   * @param {Date} date - 日期
   * @returns {Date} 一周的结束
   */
  endOfWeek(date) {
    const start = this.startOfWeek(date);
    return this.endOfDay(this.addDays(start, 6));
  },

  /**
   * 获取一月的开始
   * @param {Date} date - 日期
   * @returns {Date} 一月的开始
   */
  startOfMonth(date) {
    const result = new Date(date.getFullYear(), date.getMonth(), 1);
    return this.startOfDay(result);
  },

  /**
   * 获取一月的结束
   * @param {Date} date - 日期
   * @returns {Date} 一月的结束
   */
  endOfMonth(date) {
    const result = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    return this.endOfDay(result);
  },

  /**
   * 获取一年的开始
   * @param {Date} date - 日期
   * @returns {Date} 一年的开始
   */
  startOfYear(date) {
    const result = new Date(date.getFullYear(), 0, 1);
    return this.startOfDay(result);
  },

  /**
   * 获取一年的结束
   * @param {Date} date - 日期
   * @returns {Date} 一年的结束
   */
  endOfYear(date) {
    const result = new Date(date.getFullYear(), 11, 31);
    return this.endOfDay(result);
  },

  /**
   * 获取季度的开始
   * @param {Date} date - 日期
   * @returns {Date} 季度的开始
   */
  startOfQuarter(date) {
    const quarter = this.getQuarter(date);
    const month = (quarter - 1) * 3;
    return this.startOfDay(new Date(date.getFullYear(), month, 1));
  },

  /**
   * 获取季度的结束
   * @param {Date} date - 日期
   * @returns {Date} 季度的结束
   */
  endOfQuarter(date) {
    const quarter = this.getQuarter(date);
    const month = quarter * 3;
    return this.endOfDay(new Date(date.getFullYear(), month, 0));
  },

  // ==================== 格式化 ====================

  /**
   * 格式化日期
   * @param {Date} date - 日期
   * @param {string} format - 格式字符串
   *   YYYY: 4位年, YY: 2位年
   *   MM: 2位月, M: 月
   *   DD: 2位日, D: 日
   *   HH: 2位小时(24), H: 小时(24)
   *   hh: 2位小时(12), h: 小时(12)
   *   mm: 2位分钟, m: 分钟
   *   ss: 2位秒, s: 秒
   *   SSS: 毫秒
   *   A: AM/PM, a: am/pm
   *   dddd: 星期中文, ddd: 星期英文, dd: 星期简写, d: 星期数字
   * @returns {string} 格式化后的字符串
   */
  format(date, format = 'YYYY-MM-DD HH:mm:ss') {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const hour12 = hour % 12 || 12;
    const minute = date.getMinutes();
    const second = date.getSeconds();
    const ms = date.getMilliseconds();
    const weekday = date.getDay();

    const pad = (n, len = 2) => String(n).padStart(len, '0');

    // 构建替换映射（按长度降序排列）
    const replacements = [
      ['dddd', this.WEEKDAYS_CN[weekday]],
      ['ddd', this.WEEKDAYS_EN[weekday]],
      ['dd', this.WEEKDAYS_SHORT[weekday]],
      ['YYYY', year],
      ['YY', String(year).slice(-2)],
      ['MM', pad(month)],
      ['DD', pad(day)],
      ['HH', pad(hour)],
      ['hh', pad(hour12)],
      ['mm', pad(minute)],
      ['ss', pad(second)],
      ['SSS', pad(ms, 3)],
      // 单字符替换（需要特殊处理，避免误替换）
      ['M', String(month)],
      ['D', String(day)],
      ['H', String(hour)],
      ['h', String(hour12)],
      ['m', String(minute)],
      ['s', String(second)],
      ['d', String(weekday)],
      ['A', hour < 12 ? 'AM' : 'PM'],
      ['a', hour < 12 ? 'am' : 'pm'],
    ];

    let result = format;
    
    // 先替换长模式
    for (const [pattern, value] of replacements) {
      if (pattern.length > 1) {
        result = result.split(pattern).join(value);
      }
    }
    
    // 再替换单字符（需要避免替换已经被替换过的部分）
    // 使用占位符技巧
    for (const [pattern, value] of replacements) {
      if (pattern.length === 1) {
        // 只替换未被其他模式包含的单字符
        // 用特殊标记避免重复替换
        result = result.replace(new RegExp(`(?<![A-Za-z])${pattern}(?![A-Za-z])`, 'g'), value);
      }
    }

    return result;
  },

  /**
   * 格式化为 ISO 8601 字符串
   * @param {Date} date - 日期
   * @returns {string} ISO 字符串
   */
  toISO(date) {
    return date.toISOString();
  },

  /**
   * 格式化为本地日期字符串
   * @param {Date} date - 日期
   * @returns {string} 本地日期字符串
   */
  toLocalDate(date) {
    return this.format(date, 'YYYY-MM-DD');
  },

  /**
   * 格式化为本地时间字符串
   * @param {Date} date - 日期
   * @returns {string} 本地时间字符串
   */
  toLocalTime(date) {
    return this.format(date, 'HH:mm:ss');
  },

  /**
   * 格式化为本地日期时间字符串
   * @param {Date} date - 日期
   * @returns {string} 本地日期时间字符串
   */
  toLocalDateTime(date) {
    return this.format(date, 'YYYY-MM-DD HH:mm:ss');
  },

  /**
   * 格式化为中文日期
   * @param {Date} date - 日期
   * @returns {string} 中文日期字符串
   */
  toChineseDate(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekday = this.WEEKDAYS_CN[date.getDay()];
    return `${year}年${month}月${day}日 星期${weekday}`;
  },

  /**
   * 相对时间描述（如：刚刚、5分钟前、昨天）
   * @param {Date} date - 日期
   * @param {Date} [now=new Date()] - 当前时间
   * @returns {string} 相对时间描述
   */
  toRelative(date, now = new Date()) {
    const diffMs = now - date;
    const diffSeconds = Math.floor(diffMs / this.MS.SECOND);
    const diffMinutes = Math.floor(diffMs / this.MS.MINUTE);
    const diffHours = Math.floor(diffMs / this.MS.HOUR);
    const diffDays = Math.floor(diffMs / this.MS.DAY);

    if (diffSeconds < 0) {
      // 未来时间
      const absDiffSeconds = Math.abs(diffSeconds);
      const absDiffMinutes = Math.abs(diffMinutes);
      const absDiffHours = Math.abs(diffHours);
      const absDiffDays = Math.abs(diffDays);

      if (absDiffSeconds < 60) return `${absDiffSeconds}秒后`;
      if (absDiffMinutes < 60) return `${absDiffMinutes}分钟后`;
      if (absDiffHours < 24) return `${absDiffHours}小时后`;
      if (absDiffDays < 7) return `${absDiffDays}天后`;
      return this.format(date, 'YYYY-MM-DD');
    }

    // 过去时间
    if (diffSeconds < 60) return '刚刚';
    if (diffMinutes < 60) return `${diffMinutes}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (this.isYesterday(date)) return '昨天';
    if (diffDays < 7) return `${diffDays}天前`;
    return this.format(date, 'YYYY-MM-DD');
  },

  // ==================== 解析 ====================

  /**
   * 解析日期字符串
   * @param {string} str - 日期字符串
   * @param {string} format - 格式字符串
   * @returns {Date|null} 日期对象或 null
   */
  parse(str, format = 'YYYY-MM-DD') {
    if (!str) return null;

    // 格式映射（只使用双字符模式，避免单字符模式的歧义）
    const patterns = {
      'YYYY': '(\\d{4})',
      'YY': '(\\d{2})',
      'MM': '(\\d{2})',
      'DD': '(\\d{2})',
      'HH': '(\\d{2})',
      'hh': '(\\d{2})',
      'mm': '(\\d{2})',
      'ss': '(\\d{2})',
      'SSS': '(\\d{3})',
      // 单字符模式（只在需要时使用）
      'M': '(\\d{1,2})',
      'D': '(\\d{1,2})',
      'H': '(\\d{1,2})',
      'h': '(\\d{1,2})',
      'm': '(\\d{1,2})',
      's': '(\\d{1,2})',
    };

    // 找出格式中实际使用的模式（避免重叠）
    let regexStr = format;
    const usedPatterns = [];
    
    // 按长度降序检查
    const sortedKeys = Object.keys(patterns).sort((a, b) => b.length - a.length);
    
    for (const key of sortedKeys) {
      // 检查是否在原格式中出现，且没有被更长的模式覆盖
      if (format.includes(key)) {
        // 检查是否是子串（如 YY 是 YYYY 的子串）
        const pos = format.indexOf(key);
        // 对于子串情况，只使用更长的模式
        const isSubstring = sortedKeys.some(k => k.length > key.length && k.includes(key) && format.includes(k));
        if (!isSubstring) {
          usedPatterns.push({ key, pos });
        }
      }
    }
    
    // 按位置排序
    usedPatterns.sort((a, b) => a.pos - b.pos);
    const keys = usedPatterns.map(p => p.key);
    
    // 构建正则表达式
    for (const key of sortedKeys) {
      if (keys.includes(key)) {
        regexStr = regexStr.replace(key, patterns[key]);
      }
    }

    // 转义分隔符
    regexStr = regexStr.replace(/[-.\/]/g, '\\$&');

    const regex = new RegExp(`^${regexStr}$`);
    const match = str.match(regex);

    if (!match) return null;

    // 提取值
    const values = {};
    keys.forEach((key, index) => {
      const value = parseInt(match[index + 1], 10);
      switch (key) {
        case 'YY':
          values.YYYY = value < 70 ? 2000 + value : 1900 + value;
          break;
        case 'YYYY':
          values.YYYY = value;
          break;
        case 'MM':
        case 'M':
          values.M = value;
          break;
        case 'DD':
        case 'D':
          values.D = value;
          break;
        case 'HH':
        case 'H':
          values.H = value;
          break;
        case 'hh':
        case 'h':
          values.H = value;
          break;
        case 'mm':
        case 'm':
          values.m = value;
          break;
        case 'ss':
        case 's':
          values.s = value;
          break;
        case 'SSS':
          values.S = value;
          break;
      }
    });

    const year = values.YYYY || new Date().getFullYear();
    const month = values.M || 1;
    const day = values.D || 1;
    const hour = values.H || 0;
    const minute = values.m || 0;
    const second = values.s || 0;
    const ms = values.S || 0;

    return new Date(year, month - 1, day, hour, minute, second, ms);
  },

  /**
   * 尝试自动解析日期字符串
   * @param {string} str - 日期字符串
   * @returns {Date|null} 日期对象或 null
   */
  parseAuto(str) {
    if (!str) return null;

    // 尝试 ISO 格式
    const isoDate = new Date(str);
    if (!isNaN(isoDate.getTime())) {
      return isoDate;
    }

    // 常见格式
    const formats = [
      'YYYY-MM-DD HH:mm:ss',
      'YYYY-MM-DD HH:mm',
      'YYYY-MM-DD',
      'YYYY/MM/DD HH:mm:ss',
      'YYYY/MM/DD HH:mm',
      'YYYY/MM/DD',
      'YYYY年MM月DD日',
      'MM/DD/YYYY',
      'DD/MM/YYYY',
      'MM-DD-YYYY',
      'DD-MM-YYYY',
    ];

    for (const format of formats) {
      const result = this.parse(str, format);
      if (result && !isNaN(result.getTime())) {
        return result;
      }
    }

    return null;
  },

  // ==================== 验证 ====================

  /**
   * 判断是否为有效日期
   * @param {Date} date - 日期
   * @returns {boolean} 是否有效
   */
  isValid(date) {
    return date instanceof Date && !isNaN(date.getTime());
  },

  /**
   * 验证日期组件
   * @param {number} year - 年
   * @param {number} month - 月（1-12）
   * @param {number} day - 日
   * @returns {boolean} 是否有效
   */
  isValidDate(year, month, day) {
    if (year < 1 || year > 9999) return false;
    if (month < 1 || month > 12) return false;
    if (day < 1) return false;
    
    const maxDay = new Date(year, month, 0).getDate();
    return day <= maxDay;
  },

  /**
   * 验证时间组件
   * @param {number} hour - 小时（0-23）
   * @param {number} minute - 分钟（0-59）
   * @param {number} second - 秒（0-59）
   * @returns {boolean} 是否有效
   */
  isValidTime(hour, minute, second) {
    return hour >= 0 && hour < 24 &&
           minute >= 0 && minute < 60 &&
           second >= 0 && second < 60;
  },

  // ==================== 工具方法 ====================

  /**
   * 获取两个日期之间的所有日期
   * @param {Date} start - 开始日期
   * @param {Date} end - 结束日期
   * @returns {Date[]} 日期数组
   */
  getDatesBetween(start, end) {
    const dates = [];
    const current = this.startOfDay(start);
    const endDate = this.startOfDay(end);

    while (current <= endDate) {
      dates.push(new Date(current));
      current.setDate(current.getDate() + 1);
    }

    return dates;
  },

  /**
   * 获取指定月份的所有日期
   * @param {Date} date - 日期
   * @returns {Date[]} 日期数组
   */
  getDatesInMonth(date) {
    const start = this.startOfMonth(date);
    const end = this.endOfMonth(date);
    return this.getDatesBetween(start, end);
  },

  /**
   * 获取指定周的所有日期（周一到周日）
   * @param {Date} date - 日期
   * @returns {Date[]} 日期数组
   */
  getDatesInWeek(date) {
    const start = this.startOfWeek(date);
    const dates = [];
    for (let i = 0; i < 7; i++) {
      dates.push(this.addDays(start, i));
    }
    return dates;
  },

  /**
   * 获取下一个指定星期几
   * @param {Date} date - 起始日期
   * @param {number} weekday - 星期几（0-6，0为周日）
   * @returns {Date} 下一个指定星期几的日期
   */
  getNextWeekday(date, weekday) {
    const result = new Date(date);
    const currentDay = result.getDay();
    let daysUntil = weekday - currentDay;
    if (daysUntil <= 0) {
      daysUntil += 7;
    }
    return this.addDays(result, daysUntil);
  },

  /**
   * 获取上一个指定星期几
   * @param {Date} date - 起始日期
   * @param {number} weekday - 星期几（0-6，0为周日）
   * @returns {Date} 上一个指定星期几的日期
   */
  getPrevWeekday(date, weekday) {
    const result = new Date(date);
    const currentDay = result.getDay();
    let daysSince = currentDay - weekday;
    if (daysSince < 0) {
      daysSince += 7;
    }
    return this.addDays(result, -daysSince);
  },

  /**
   * 获取某个月的第 n 个星期几
   * @param {number} year - 年
   * @param {number} month - 月（1-12）
   * @param {number} n - 第几个（1-5）
   * @param {number} weekday - 星期几（0-6）
   * @returns {Date|null} 日期或 null
   */
  getNthWeekdayOfMonth(year, month, n, weekday) {
    const firstDay = new Date(year, month - 1, 1);
    let count = 0;
    let current = firstDay;

    while (current.getMonth() === month - 1) {
      if (current.getDay() === weekday) {
        count++;
        if (count === n) {
          return current;
        }
      }
      current = this.addDays(current, 1);
    }

    return null; // 该月没有第 n 个这样的星期几
  },

  /**
   * 复制日期（仅日期部分，时间为 00:00:00）
   * @param {Date} date - 日期
   * @returns {Date} 新日期
   */
  cloneDate(date) {
    return this.startOfDay(new Date(date));
  },

  /**
   * 复制时间（仅时间部分）
   * @param {Date} time - 时间源
   * @returns {Object} 时间对象 { hour, minute, second, ms }
   */
  cloneTime(time) {
    return {
      hour: time.getHours(),
      minute: time.getMinutes(),
      second: time.getSeconds(),
      ms: time.getMilliseconds()
    };
  },

  /**
   * 设置时间部分
   * @param {Date} date - 日期
   * @param {Object} time - 时间对象 { hour, minute, second, ms }
   * @returns {Date} 新日期
   */
  setTime(date, time) {
    const result = new Date(date);
    if (time.hour !== undefined) result.setHours(time.hour);
    if (time.minute !== undefined) result.setMinutes(time.minute);
    if (time.second !== undefined) result.setSeconds(time.second);
    if (time.ms !== undefined) result.setMilliseconds(time.ms);
    return result;
  },

  /**
   * 比较两个日期（返回 -1, 0, 1）
   * @param {Date} date1 - 日期1
   * @param {Date} date2 - 日期2
   * @returns {number} -1 表示 date1 < date2, 0 表示相等, 1 表示 date1 > date2
   */
  compare(date1, date2) {
    const diff = date1.getTime() - date2.getTime();
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
  },

  /**
   * 获取年龄（根据生日）
   * @param {Date} birthday - 生日
   * @param {Date} [now=new Date()] - 当前日期
   * @returns {number} 年龄
   */
  getAge(birthday, now = new Date()) {
    let age = now.getFullYear() - birthday.getFullYear();
    const monthDiff = now.getMonth() - birthday.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birthday.getDate())) {
      age--;
    }
    return age;
  },
};

// CommonJS 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DateUtils;
}

// ES Module 导出
if (typeof exports !== 'undefined') {
  exports.default = DateUtils;
}