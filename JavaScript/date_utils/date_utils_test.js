/**
 * Date Utilities Test Suite
 * JavaScript 日期时间工具模块测试
 */

const DateUtils = require('./mod.js');

// 测试工具函数
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}\nExpected: ${expected}\nActual: ${actual}`);
  }
}

function assertDeepEqual(actual, expected, message) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message}\nExpected: ${JSON.stringify(expected)}\nActual: ${JSON.stringify(actual)}`);
  }
}

function assertDateEqual(actual, expected, message) {
  if (actual.getTime() !== expected.getTime()) {
    throw new Error(`${message}\nExpected: ${expected.toISOString()}\nActual: ${actual.toISOString()}`);
  }
}

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}`);
    console.error(`  ${e.message}`);
    failed++;
  }
}

// 辅助函数：创建固定日期
function createDate(year, month, day, hour = 0, minute = 0, second = 0, ms = 0) {
  return new Date(year, month - 1, day, hour, minute, second, ms);
}

console.log('Running DateUtils tests...\n');

// ==================== 常量测试 ====================
test('MS 常量 - 毫秒值正确', () => {
  assertEqual(DateUtils.MS.SECOND, 1000, '1秒应为1000毫秒');
  assertEqual(DateUtils.MS.MINUTE, 60000, '1分钟应为60000毫秒');
  assertEqual(DateUtils.MS.HOUR, 3600000, '1小时应为3600000毫秒');
  assertEqual(DateUtils.MS.DAY, 86400000, '1天应为86400000毫秒');
  assertEqual(DateUtils.MS.WEEK, 604800000, '1周应为604800000毫秒');
});

test('WEEKDAYS_CN - 星期名称正确', () => {
  assertEqual(DateUtils.WEEKDAYS_CN.length, 7, '应有7个星期名称');
  assertEqual(DateUtils.WEEKDAYS_CN[0], '日', '周日应为"日"');
  assertEqual(DateUtils.WEEKDAYS_CN[6], '六', '周六应为"六"');
});

test('MONTHS_CN - 月份名称正确', () => {
  assertEqual(DateUtils.MONTHS_CN.length, 12, '应有12个月份名称');
  assertEqual(DateUtils.MONTHS_CN[0], '一月', '第一个月应为"一月"');
  assertEqual(DateUtils.MONTHS_CN[11], '十二月', '最后一个月应为"十二月"');
});

// ==================== 创建日期测试 ====================
test('now - 返回当前时间', () => {
  const now = DateUtils.now();
  assert(now instanceof Date, '应返回Date对象');
  assert(Math.abs(now.getTime() - Date.now()) < 100, '应接近当前时间');
});

test('timestamp - 返回毫秒时间戳', () => {
  const ts = DateUtils.timestamp();
  assertEqual(typeof ts, 'number', '应返回数字');
  assert(Math.abs(ts - Date.now()) < 100, '应接近当前时间');
});

test('unix - 返回秒时间戳', () => {
  const unix = DateUtils.unix();
  assertEqual(typeof unix, 'number', '应返回数字');
  assert(Math.abs(unix - Math.floor(Date.now() / 1000)) < 1, '应接近当前时间（秒）');
});

test('fromTimestamp - 从时间戳创建日期', () => {
  const ts = 1609459200000; // 2021-01-01 00:00:00 UTC
  const date = DateUtils.fromTimestamp(ts);
  assert(date instanceof Date, '应返回Date对象');
  
  // 测试秒级时间戳
  const unixTs = 1609459200;
  const dateFromUnix = DateUtils.fromTimestamp(unixTs);
  assertEqual(dateFromUnix.getTime(), ts, '秒级时间戳应正确转换');
});

test('create - 支持多种输入格式', () => {
  const date = new Date(2024, 0, 1);
  
  // Date 对象
  const fromObj = DateUtils.create(date);
  assert(fromObj instanceof Date, 'Date对象应返回Date');
  
  // 数字
  const fromNum = DateUtils.create(1609459200000);
  assert(fromNum instanceof Date, '数字应返回Date');
  
  // 字符串
  const fromStr = DateUtils.create('2024-01-01');
  assert(fromStr instanceof Date, 'ISO字符串应返回Date');
  
  // 无效输入
  const invalid = DateUtils.create('invalid');
  assertEqual(invalid, null, '无效字符串应返回null');
  
  const empty = DateUtils.create(null);
  assertEqual(empty, null, 'null应返回null');
});

test('createFrom - 创建指定日期', () => {
  const date = DateUtils.createFrom(2024, 6, 15, 10, 30, 45, 500);
  assertEqual(date.getFullYear(), 2024, '年份应为2024');
  assertEqual(date.getMonth(), 5, '月份应为5（6月是索引5）');
  assertEqual(date.getDate(), 15, '日期应为15');
  assertEqual(date.getHours(), 10, '小时应为10');
  assertEqual(date.getMinutes(), 30, '分钟应为30');
  assertEqual(date.getSeconds(), 45, '秒应为45');
  assertEqual(date.getMilliseconds(), 500, '毫秒应为500');
});

// ==================== 获取日期组件测试 ====================
test('getYear - 获取年份', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.getYear(date), 2024, '年份应为2024');
});

test('getMonth - 获取月份（1-12）', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.getMonth(date), 3, '月份应为3');
});

test('getDay - 获取日期', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.getDay(date), 15, '日期应为15');
});

test('getWeekday - 获取星期', () => {
  // 2024-03-15 是周五
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.getWeekday(date), 5, '2024-03-15应为周五（5）');
  
  // 2024-03-17 是周日
  const sunday = createDate(2024, 3, 17);
  assertEqual(DateUtils.getWeekday(sunday), 0, '周日应为0');
});

test('getHour - 获取小时', () => {
  const date = createDate(2024, 3, 15, 14, 30);
  assertEqual(DateUtils.getHour(date), 14, '小时应为14');
});

test('getMinute - 获取分钟', () => {
  const date = createDate(2024, 3, 15, 14, 30);
  assertEqual(DateUtils.getMinute(date), 30, '分钟应为30');
});

test('getSecond - 获取秒', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45);
  assertEqual(DateUtils.getSecond(date), 45, '秒应为45');
});

test('getMillisecond - 获取毫秒', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  assertEqual(DateUtils.getMillisecond(date), 123, '毫秒应为123');
});

test('getDayOfYear - 获取一年中的第几天', () => {
  // 2024-01-01 是第1天
  const jan1 = createDate(2024, 1, 1);
  assertEqual(DateUtils.getDayOfYear(jan1), 1, '1月1日应是第1天');
  
  // 2024-02-01 是第32天（闰年）
  const feb1 = createDate(2024, 2, 1);
  assertEqual(DateUtils.getDayOfYear(feb1), 32, '2月1日应是第32天');
  
  // 2024-12-31 是第366天（闰年）
  const dec31 = createDate(2024, 12, 31);
  assertEqual(DateUtils.getDayOfYear(dec31), 366, '闰年12月31日应是第366天');
  
  // 2023-12-31 是第365天（平年）
  const dec31_2023 = createDate(2023, 12, 31);
  assertEqual(DateUtils.getDayOfYear(dec31_2023), 365, '平年12月31日应是第365天');
});

test('getWeekOfYear - 获取一年中的第几周', () => {
  // 2024-01-01 是周一，ISO周的第1周
  const jan1 = createDate(2024, 1, 1);
  assertEqual(DateUtils.getWeekOfYear(jan1), 1, '1月1日应在第1周');
  
  // 2024-12-31 是周二
  const dec31 = createDate(2024, 12, 31);
  assert(DateUtils.getWeekOfYear(dec31) >= 1 && DateUtils.getWeekOfYear(dec31) <= 53, '周数应在1-53之间');
});

test('getQuarter - 获取季度', () => {
  assertEqual(DateUtils.getQuarter(createDate(2024, 1, 1)), 1, '1月应为Q1');
  assertEqual(DateUtils.getQuarter(createDate(2024, 3, 31)), 1, '3月应为Q1');
  assertEqual(DateUtils.getQuarter(createDate(2024, 4, 1)), 2, '4月应为Q2');
  assertEqual(DateUtils.getQuarter(createDate(2024, 6, 30)), 2, '6月应为Q2');
  assertEqual(DateUtils.getQuarter(createDate(2024, 7, 1)), 3, '7月应为Q3');
  assertEqual(DateUtils.getQuarter(createDate(2024, 9, 30)), 3, '9月应为Q3');
  assertEqual(DateUtils.getQuarter(createDate(2024, 10, 1)), 4, '10月应为Q4');
  assertEqual(DateUtils.getQuarter(createDate(2024, 12, 31)), 4, '12月应为Q4');
});

test('getDaysInMonth - 获取月份天数', () => {
  assertEqual(DateUtils.getDaysInMonth(createDate(2024, 1, 1)), 31, '1月应有31天');
  assertEqual(DateUtils.getDaysInMonth(createDate(2024, 2, 1)), 29, '2024年2月应有29天（闰年）');
  assertEqual(DateUtils.getDaysInMonth(createDate(2023, 2, 1)), 28, '2023年2月应有28天（平年）');
  assertEqual(DateUtils.getDaysInMonth(createDate(2024, 4, 1)), 30, '4月应有30天');
  assertEqual(DateUtils.getDaysInMonth(createDate(2024, 12, 1)), 31, '12月应有31天');
});

// ==================== 日期计算测试 ====================
test('addYears - 添加年', () => {
  const date = createDate(2024, 2, 29); // 闰年2月29日
  const result = DateUtils.addYears(date, 1);
  assertEqual(result.getFullYear(), 2025, '年份应为2025');
  assertEqual(result.getMonth(), 1, '月份应为1（2月）');
  assertEqual(result.getDate(), 28, '平年2月29日应变为28日');
  
  const result4 = DateUtils.addYears(date, 4);
  assertEqual(result4.getDate(), 29, '4年后闰年应保持29日');
});

test('addMonths - 添加月', () => {
  const date = createDate(2024, 1, 31);
  
  // 1月31日 + 1月 = 2月29日（闰年）
  const result1 = DateUtils.addMonths(date, 1);
  assertEqual(result1.getMonth(), 1, '月份应为1（2月）');
  assertEqual(result1.getDate(), 29, '日期应为29');
  
  // 1月31日 + 2月 = 3月31日
  const result2 = DateUtils.addMonths(date, 2);
  assertEqual(result2.getMonth(), 2, '月份应为2（3月）');
  assertEqual(result2.getDate(), 31, '日期应为31');
});

test('addDays - 添加天', () => {
  const date = createDate(2024, 1, 1);
  
  const result = DateUtils.addDays(date, 30);
  assertEqual(result.getMonth(), 0, '应仍在1月');
  assertEqual(result.getDate(), 31, '应为31日');
  
  const result2 = DateUtils.addDays(date, 31);
  assertEqual(result2.getMonth(), 1, '应在2月');
  assertEqual(result2.getDate(), 1, '应为1日');
  
  // 负数
  const result3 = DateUtils.addDays(date, -1);
  assertEqual(result3.getMonth(), 11, '应在12月');
  assertEqual(result3.getDate(), 31, '应为31日');
});

test('addHours - 添加小时', () => {
  const date = createDate(2024, 1, 1, 10, 0, 0);
  
  const result = DateUtils.addHours(date, 5);
  assertEqual(result.getHours(), 15, '小时应为15');
  
  // 跨天
  const result2 = DateUtils.addHours(date, 20);
  assertEqual(result2.getDate(), 2, '应为2日');
  assertEqual(result2.getHours(), 6, '小时应为6');
});

test('addMinutes - 添加分钟', () => {
  const date = createDate(2024, 1, 1, 10, 30, 0);
  
  const result = DateUtils.addMinutes(date, 45);
  assertEqual(result.getHours(), 11, '小时应为11');
  assertEqual(result.getMinutes(), 15, '分钟应为15');
});

test('addSeconds - 添加秒', () => {
  const date = createDate(2024, 1, 1, 10, 0, 30);
  
  const result = DateUtils.addSeconds(date, 45);
  assertEqual(result.getMinutes(), 1, '分钟应为1');
  assertEqual(result.getSeconds(), 15, '秒应为15');
});

test('addMilliseconds - 添加毫秒', () => {
  const date = createDate(2024, 1, 1, 10, 0, 0, 500);
  
  const result = DateUtils.addMilliseconds(date, 600);
  assertEqual(result.getSeconds(), 1, '秒应为1');
  assertEqual(result.getMilliseconds(), 100, '毫秒应为100');
});

test('diffDays - 计算天数差', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 1, 10);
  
  assertEqual(DateUtils.diffDays(date1, date2), 9, '应相差9天');
  assertEqual(DateUtils.diffDays(date2, date1), -9, '反向应相差-9天');
});

test('diffHours - 计算小时差', () => {
  const date1 = createDate(2024, 1, 1, 0, 0, 0);
  const date2 = createDate(2024, 1, 1, 12, 0, 0);
  
  assertEqual(DateUtils.diffHours(date1, date2), 12, '应相差12小时');
});

test('diffMinutes - 计算分钟差', () => {
  const date1 = createDate(2024, 1, 1, 10, 0, 0);
  const date2 = createDate(2024, 1, 1, 10, 30, 0);
  
  assertEqual(DateUtils.diffMinutes(date1, date2), 30, '应相差30分钟');
});

test('diffSeconds - 计算秒差', () => {
  const date1 = createDate(2024, 1, 1, 10, 0, 0);
  const date2 = createDate(2024, 1, 1, 10, 0, 45);
  
  assertEqual(DateUtils.diffSeconds(date1, date2), 45, '应相差45秒');
});

// ==================== 日期比较测试 ====================
test('isSameDay - 判断是否同一天', () => {
  const date1 = createDate(2024, 3, 15, 10, 30);
  const date2 = createDate(2024, 3, 15, 20, 45);
  const date3 = createDate(2024, 3, 16, 10, 30);
  
  assert(DateUtils.isSameDay(date1, date2), '同一天不同时间应为true');
  assert(!DateUtils.isSameDay(date1, date3), '不同天应为false');
});

test('isSameWeek - 判断是否同一周', () => {
  // 2024-03-11 是周一，2024-03-17 是周日
  const mon = createDate(2024, 3, 11);
  const sun = createDate(2024, 3, 17);
  const nextMon = createDate(2024, 3, 18);
  
  assert(DateUtils.isSameWeek(mon, sun), '同一周应为true');
  assert(!DateUtils.isSameWeek(mon, nextMon), '不同周应为false');
});

test('isSameMonth - 判断是否同一月', () => {
  const date1 = createDate(2024, 3, 1);
  const date2 = createDate(2024, 3, 31);
  const date3 = createDate(2024, 4, 1);
  
  assert(DateUtils.isSameMonth(date1, date2), '同一月应为true');
  assert(!DateUtils.isSameMonth(date1, date3), '不同月应为false');
});

test('isSameYear - 判断是否同一年', () => {
  const date1 = createDate(2024, 1, 1);
  const date2 = createDate(2024, 12, 31);
  const date3 = createDate(2025, 1, 1);
  
  assert(DateUtils.isSameYear(date1, date2), '同一年应为true');
  assert(!DateUtils.isSameYear(date1, date3), '不同年应为false');
});

test('isToday/isYesterday/isTomorrow - 判断日期关系', () => {
  const today = new Date();
  today.setHours(12, 0, 0, 0);
  
  const yesterday = DateUtils.addDays(today, -1);
  const tomorrow = DateUtils.addDays(today, 1);
  
  assert(DateUtils.isToday(today), '今天应为true');
  assert(!DateUtils.isToday(yesterday), '昨天不是今天');
  assert(DateUtils.isYesterday(yesterday), '昨天应为true');
  assert(DateUtils.isTomorrow(tomorrow), '明天应为true');
});

test('isWeekday/isWeekend - 判断工作日/周末', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  assert(DateUtils.isWeekday(friday), '周五应为工作日');
  assert(!DateUtils.isWeekend(friday), '周五不是周末');
  
  // 2024-03-16 是周六
  const saturday = createDate(2024, 3, 16);
  assert(!DateUtils.isWeekday(saturday), '周六不是工作日');
  assert(DateUtils.isWeekend(saturday), '周六应为周末');
  
  // 2024-03-17 是周日
  const sunday = createDate(2024, 3, 17);
  assert(DateUtils.isWeekend(sunday), '周日应为周末');
});

test('isLeapYear - 判断闰年', () => {
  assert(DateUtils.isLeapYear(2024), '2024是闰年');
  assert(!DateUtils.isLeapYear(2023), '2023不是闰年');
  assert(DateUtils.isLeapYear(2000), '2000是闰年（能被400整除）');
  assert(!DateUtils.isLeapYear(1900), '1900不是闰年（能被100整除但不能被400整除）');
  
  // 使用日期
  assert(DateUtils.isLeapYear(createDate(2024, 1, 1)), '使用日期判断闰年');
});

test('isBetween - 判断日期是否在范围内', () => {
  const start = createDate(2024, 3, 10);
  const end = createDate(2024, 3, 20);
  const middle = createDate(2024, 3, 15);
  const before = createDate(2024, 3, 5);
  const after = createDate(2024, 3, 25);
  
  assert(DateUtils.isBetween(middle, start, end), '中间日期应在范围内');
  assert(DateUtils.isBetween(start, start, end), '开始日期应在范围内');
  assert(DateUtils.isBetween(end, start, end), '结束日期应在范围内');
  assert(!DateUtils.isBetween(before, start, end), '之前的日期不在范围内');
  assert(!DateUtils.isBetween(after, start, end), '之后的日期不在范围内');
});

// ==================== 日期边界测试 ====================
test('startOfDay - 获取一天的开始', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 500);
  const start = DateUtils.startOfDay(date);
  
  assertEqual(start.getHours(), 0, '小时应为0');
  assertEqual(start.getMinutes(), 0, '分钟应为0');
  assertEqual(start.getSeconds(), 0, '秒应为0');
  assertEqual(start.getMilliseconds(), 0, '毫秒应为0');
});

test('endOfDay - 获取一天的结束', () => {
  const date = createDate(2024, 3, 15, 10, 0, 0, 0);
  const end = DateUtils.endOfDay(date);
  
  assertEqual(end.getHours(), 23, '小时应为23');
  assertEqual(end.getMinutes(), 59, '分钟应为59');
  assertEqual(end.getSeconds(), 59, '秒应为59');
  assertEqual(end.getMilliseconds(), 999, '毫秒应为999');
});

test('startOfWeek - 获取一周的开始（周一）', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  const start = DateUtils.startOfWeek(friday);
  
  assertEqual(start.getDay(), 1, '应为周一');
  assertEqual(start.getDate(), 11, '应为11日');
});

test('endOfWeek - 获取一周的结束（周日）', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  const end = DateUtils.endOfWeek(friday);
  
  assertEqual(end.getDay(), 0, '应为周日');
  assertEqual(end.getDate(), 17, '应为17日');
});

test('startOfMonth - 获取一月的开始', () => {
  const date = createDate(2024, 3, 15);
  const start = DateUtils.startOfMonth(date);
  
  assertEqual(start.getMonth(), 2, '月份应为2（3月）');
  assertEqual(start.getDate(), 1, '日期应为1');
  assertEqual(start.getHours(), 0, '小时应为0');
});

test('endOfMonth - 获取一月的结束', () => {
  const date = createDate(2024, 3, 15); // 3月
  const end = DateUtils.endOfMonth(date);
  
  assertEqual(end.getMonth(), 2, '月份应为2（3月）');
  assertEqual(end.getDate(), 31, '日期应为31');
  
  // 测试2月
  const feb = createDate(2024, 2, 10);
  const febEnd = DateUtils.endOfMonth(feb);
  assertEqual(febEnd.getDate(), 29, '2024年2月应有29天');
});

test('startOfYear - 获取一年的开始', () => {
  const date = createDate(2024, 6, 15);
  const start = DateUtils.startOfYear(date);
  
  assertEqual(start.getMonth(), 0, '月份应为0（1月）');
  assertEqual(start.getDate(), 1, '日期应为1');
});

test('endOfYear - 获取一年的结束', () => {
  const date = createDate(2024, 6, 15);
  const end = DateUtils.endOfYear(date);
  
  assertEqual(end.getMonth(), 11, '月份应为11（12月）');
  assertEqual(end.getDate(), 31, '日期应为31');
});

test('startOfQuarter/endOfQuarter - 获取季度边界', () => {
  // Q1
  const q1 = createDate(2024, 2, 15);
  assertEqual(DateUtils.startOfQuarter(q1).getMonth(), 0, 'Q1开始应为1月');
  assertEqual(DateUtils.endOfQuarter(q1).getMonth(), 2, 'Q1结束应为3月');
  
  // Q2
  const q2 = createDate(2024, 5, 15);
  assertEqual(DateUtils.startOfQuarter(q2).getMonth(), 3, 'Q2开始应为4月');
  assertEqual(DateUtils.endOfQuarter(q2).getMonth(), 5, 'Q2结束应为6月');
  
  // Q3
  const q3 = createDate(2024, 8, 15);
  assertEqual(DateUtils.startOfQuarter(q3).getMonth(), 6, 'Q3开始应为7月');
  assertEqual(DateUtils.endOfQuarter(q3).getMonth(), 8, 'Q3结束应为9月');
  
  // Q4
  const q4 = createDate(2024, 11, 15);
  assertEqual(DateUtils.startOfQuarter(q4).getMonth(), 9, 'Q4开始应为10月');
  assertEqual(DateUtils.endOfQuarter(q4).getMonth(), 11, 'Q4结束应为12月');
});

// ==================== 格式化测试 ====================
test('format - 基本格式化', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  
  assertEqual(DateUtils.format(date, 'YYYY-MM-DD'), '2024-03-15', '日期格式化');
  assertEqual(DateUtils.format(date, 'HH:mm:ss'), '14:30:45', '时间格式化');
  assertEqual(DateUtils.format(date, 'YYYY-MM-DD HH:mm:ss'), '2024-03-15 14:30:45', '日期时间格式化');
});

test('format - 12小时制', () => {
  const am = createDate(2024, 3, 15, 9, 30, 0);
  const pm = createDate(2024, 3, 15, 14, 30, 0);
  
  assertEqual(DateUtils.format(am, 'hh:mm A'), '09:30 AM', '上午格式化');
  assertEqual(DateUtils.format(pm, 'hh:mm A'), '02:30 PM', '下午格式化');
  assertEqual(DateUtils.format(am, 'h:mm a'), '9:30 am', '上午小写');
  assertEqual(DateUtils.format(pm, 'h:mm a'), '2:30 pm', '下午小写');
});

test('format - 星期', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  
  assertEqual(DateUtils.format(friday, 'd'), '5', '星期数字');
  assertEqual(DateUtils.format(friday, 'dd'), 'Fri', '星期简写');
  assertEqual(DateUtils.format(friday, 'ddd'), 'Friday', '星期全称');
  assertEqual(DateUtils.format(friday, 'dddd'), '五', '星期中文');
});

test('format - 毫秒', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  assertEqual(DateUtils.format(date, 'SSS'), '123', '毫秒格式化');
});

test('toISO - ISO格式', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  const iso = DateUtils.toISO(date);
  assert(iso.includes('2024'), 'ISO格式应包含年份');
  assert(iso.includes('T'), 'ISO格式应包含T');
});

test('toLocalDate - 本地日期字符串', () => {
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.toLocalDate(date), '2024-03-15', '本地日期');
});

test('toLocalTime - 本地时间字符串', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45);
  assertEqual(DateUtils.toLocalTime(date), '14:30:45', '本地时间');
});

test('toLocalDateTime - 本地日期时间字符串', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45);
  assertEqual(DateUtils.toLocalDateTime(date), '2024-03-15 14:30:45', '本地日期时间');
});

test('toChineseDate - 中文日期', () => {
  // 2024-03-15 是周五
  const date = createDate(2024, 3, 15);
  assertEqual(DateUtils.toChineseDate(date), '2024年3月15日 星期五', '中文日期');
});

test('toRelative - 相对时间', () => {
  const now = new Date();
  
  // 刚刚
  const justNow = new Date(now.getTime() - 30 * 1000);
  assertEqual(DateUtils.toRelative(justNow, now), '刚刚', '30秒前应为刚刚');
  
  // 分钟前
  const minsAgo = new Date(now.getTime() - 5 * 60 * 1000);
  assertEqual(DateUtils.toRelative(minsAgo, now), '5分钟前', '应为5分钟前');
  
  // 小时前
  const hoursAgo = new Date(now.getTime() - 3 * 60 * 60 * 1000);
  assertEqual(DateUtils.toRelative(hoursAgo, now), '3小时前', '应为3小时前');
  
  // 昨天
  const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  assertEqual(DateUtils.toRelative(yesterday, now), '昨天', '应为昨天');
  
  // 未来
  const in5Mins = new Date(now.getTime() + 5 * 60 * 1000);
  assertEqual(DateUtils.toRelative(in5Mins, now), '5分钟后', '应为5分钟后');
});

// ==================== 解析测试 ====================
test('parse - 解析日期字符串', () => {
  const result1 = DateUtils.parse('2024-03-15', 'YYYY-MM-DD');
  assertEqual(result1.getFullYear(), 2024, '年份应为2024');
  assertEqual(result1.getMonth(), 2, '月份应为2（3月）');
  assertEqual(result1.getDate(), 15, '日期应为15');
  
  const result2 = DateUtils.parse('2024-03-15 14:30:45', 'YYYY-MM-DD HH:mm:ss');
  assertEqual(result2.getHours(), 14, '小时应为14');
  assertEqual(result2.getMinutes(), 30, '分钟应为30');
  assertEqual(result2.getSeconds(), 45, '秒应为45');
});

test('parse - 解析不同格式', () => {
  const result1 = DateUtils.parse('2024/03/15', 'YYYY/MM/DD');
  assertEqual(result1.getDate(), 15, '斜杠分隔格式');
  
  const result2 = DateUtils.parse('15-03-2024', 'DD-MM-YYYY');
  assertEqual(result2.getMonth(), 2, '日月年格式');
  
  const result3 = DateUtils.parse('03/15/2024', 'MM/DD/YYYY');
  assertEqual(result3.getMonth(), 2, '月日年格式');
});

test('parseAuto - 自动解析', () => {
  const result1 = DateUtils.parseAuto('2024-03-15');
  assert(result1 !== null, 'ISO格式应解析成功');
  
  const result2 = DateUtils.parseAuto('2024/03/15 14:30:00');
  assert(result2 !== null, '斜杠格式应解析成功');
  
  const result3 = DateUtils.parseAuto('invalid');
  assertEqual(result3, null, '无效字符串应返回null');
});

// ==================== 验证测试 ====================
test('isValid - 判断有效日期', () => {
  const validDate = new Date(2024, 0, 1);
  assert(DateUtils.isValid(validDate), '有效日期应为true');
  
  const invalidDate = new Date('invalid');
  assert(!DateUtils.isValid(invalidDate), '无效日期应为false');
  
  assert(!DateUtils.isValid('string'), '字符串应为false');
  assert(!DateUtils.isValid(123), '数字应为false');
});

test('isValidDate - 验证日期组件', () => {
  assert(DateUtils.isValidDate(2024, 3, 15), '有效日期');
  assert(DateUtils.isValidDate(2024, 2, 29), '闰年2月29日有效');
  assert(!DateUtils.isValidDate(2024, 2, 30), '2月30日无效');
  assert(!DateUtils.isValidDate(2024, 13, 1), '13月无效');
  assert(!DateUtils.isValidDate(2024, 0, 1), '0月无效');
});

test('isValidTime - 验证时间组件', () => {
  assert(DateUtils.isValidTime(14, 30, 45), '有效时间');
  assert(DateUtils.isValidTime(0, 0, 0), '午夜有效');
  assert(DateUtils.isValidTime(23, 59, 59), '最大时间有效');
  assert(!DateUtils.isValidTime(24, 0, 0), '24小时无效');
  assert(!DateUtils.isValidTime(0, 60, 0), '60分钟无效');
  assert(!DateUtils.isValidTime(0, 0, 60), '60秒无效');
});

// ==================== 工具方法测试 ====================
test('getDatesBetween - 获取日期范围内的所有日期', () => {
  const start = createDate(2024, 3, 10);
  const end = createDate(2024, 3, 12);
  
  const dates = DateUtils.getDatesBetween(start, end);
  assertEqual(dates.length, 3, '应有3个日期');
  assertEqual(dates[0].getDate(), 10, '第一个日期应为10日');
  assertEqual(dates[2].getDate(), 12, '最后一个日期应为12日');
});

test('getDatesInMonth - 获取月份内所有日期', () => {
  const date = createDate(2024, 3, 15);
  const dates = DateUtils.getDatesInMonth(date);
  assertEqual(dates.length, 31, '3月应有31天');
  
  const feb = createDate(2024, 2, 1);
  const febDates = DateUtils.getDatesInMonth(feb);
  assertEqual(febDates.length, 29, '2024年2月应有29天');
});

test('getDatesInWeek - 获取周内所有日期', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  const dates = DateUtils.getDatesInWeek(friday);
  
  assertEqual(dates.length, 7, '应有7天');
  assertEqual(dates[0].getDay(), 1, '第一天应为周一');
  assertEqual(dates[6].getDay(), 0, '最后一天应为周日');
});

test('getNextWeekday - 获取下一个指定星期几', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  
  // 下一个周一
  const nextMon = DateUtils.getNextWeekday(friday, 1);
  assertEqual(nextMon.getDate(), 18, '下一个周一应为18日');
  
  // 下一个周六（明天）
  const nextSat = DateUtils.getNextWeekday(friday, 6);
  assertEqual(nextSat.getDate(), 16, '下一个周六应为16日');
});

test('getPrevWeekday - 获取上一个指定星期几', () => {
  // 2024-03-15 是周五
  const friday = createDate(2024, 3, 15);
  
  // 上一个周一
  const prevMon = DateUtils.getPrevWeekday(friday, 1);
  assertEqual(prevMon.getDate(), 11, '上一个周一应为11日');
  
  // 上一个周四（昨天）
  const prevThu = DateUtils.getPrevWeekday(friday, 4);
  assertEqual(prevThu.getDate(), 14, '上一个周四应为14日');
});

test('getNthWeekdayOfMonth - 获取某月第n个星期几', () => {
  // 2024年3月第2个周二
  const result = DateUtils.getNthWeekdayOfMonth(2024, 3, 2, 2);
  assertEqual(result.getDate(), 12, '2024年3月第2个周二应为12日');
  
  // 2024年3月第1个周一
  const firstMon = DateUtils.getNthWeekdayOfMonth(2024, 3, 1, 1);
  assertEqual(firstMon.getDate(), 4, '2024年3月第1个周一应为4日');
  
  // 不存在的第5个周三
  const invalid = DateUtils.getNthWeekdayOfMonth(2024, 3, 5, 3);
  assertEqual(invalid, null, '不存在的第5个周三应返回null');
});

test('cloneDate - 复制日期', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  const cloned = DateUtils.cloneDate(date);
  
  assertEqual(cloned.getFullYear(), 2024, '年份应相同');
  assertEqual(cloned.getMonth(), 2, '月份应相同');
  assertEqual(cloned.getDate(), 15, '日期应相同');
  assertEqual(cloned.getHours(), 0, '时间应为00:00:00');
});

test('cloneTime - 复制时间', () => {
  const date = createDate(2024, 3, 15, 14, 30, 45, 123);
  const time = DateUtils.cloneTime(date);
  
  assertEqual(time.hour, 14, '小时应为14');
  assertEqual(time.minute, 30, '分钟应为30');
  assertEqual(time.second, 45, '秒应为45');
  assertEqual(time.ms, 123, '毫秒应为123');
});

test('setTime - 设置时间', () => {
  const date = createDate(2024, 3, 15, 10, 0, 0, 0);
  const result = DateUtils.setTime(date, { hour: 14, minute: 30, second: 45, ms: 123 });
  
  assertEqual(result.getHours(), 14, '小时应为14');
  assertEqual(result.getMinutes(), 30, '分钟应为30');
  assertEqual(result.getSeconds(), 45, '秒应为45');
  assertEqual(result.getMilliseconds(), 123, '毫秒应为123');
});

test('compare - 比较日期', () => {
  const date1 = createDate(2024, 3, 15);
  const date2 = createDate(2024, 3, 16);
  const date3 = createDate(2024, 3, 15);
  
  assertEqual(DateUtils.compare(date1, date2), -1, 'date1 < date2');
  assertEqual(DateUtils.compare(date2, date1), 1, 'date2 > date1');
  assertEqual(DateUtils.compare(date1, date3), 0, 'date1 == date3');
});

test('getAge - 计算年龄', () => {
  const birthday = createDate(1990, 6, 15);
  const now = createDate(2024, 6, 15);
  
  assertEqual(DateUtils.getAge(birthday, now), 34, '生日当天应为34岁');
  
  const beforeBirthday = createDate(2024, 6, 14);
  assertEqual(DateUtils.getAge(birthday, beforeBirthday), 33, '生日前一天应为33岁');
});

// ==================== 输出测试结果 ====================
console.log('\n' + '='.repeat(50));
console.log(`Tests completed: ${passed} passed, ${failed} failed`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}