/**
 * Date Utils - Basic Usage Examples
 * 
 * 基础使用示例 - 展示 date_utils 模块的常用功能
 */

import { DateUtils, formatDate, addDays, timeAgo } from '../mod.ts';

console.log('📅 Date Utils - Basic Usage Examples\n');
console.log('='.repeat(50));

// ==================== 1. 日期格式化 ====================
console.log('\n1️⃣ 日期格式化 (Date Formatting)\n');

const now = new Date();

console.log('当前时间:', formatDate(now, 'YYYY-MM-DD HH:mm:ss'));
console.log('ISO 格式:', formatDate(now, 'YYYY-MM-DDTHH:mm:ss.SSSZ'));
console.log('美国格式:', formatDate(now, 'MM/DD/YYYY'));
console.log('欧洲格式:', formatDate(now, 'DD/MM/YYYY'));
console.log('中文格式:', formatDate(now, 'YYYY 年 MM 月 DD 日 HH:mm:ss', 'zh'));
console.log('人类可读:', formatDate(now, 'MMMM D, YYYY h:mm A', 'en'));
console.log('简短格式:', formatDate(now, 'M/D/YY'));
console.log('星期:', formatDate(now, 'dddd, MMMM D'));

// ==================== 2. 日期运算 ====================
console.log('\n2️⃣ 日期运算 (Date Arithmetic)\n');

const today = new Date();

console.log('今天:', formatDate(today, 'YYYY-MM-DD'));
console.log('7 天后:', formatDate(addDays(today, 7), 'YYYY-MM-DD'));
console.log('30 天后:', formatDate(addDays(today, 30), 'YYYY-MM-DD'));
console.log('1 个月后:', formatDate(DateUtils.addMonths(today, 1), 'YYYY-MM-DD'));
console.log('1 年后:', formatDate(DateUtils.addYears(today, 1), 'YYYY-MM-DD'));
console.log('3 天前:', formatDate(DateUtils.subtractDays(today, 3), 'YYYY-MM-DD'));

// ==================== 3. 日期比较 ====================
console.log('\n3️⃣ 日期比较 (Date Comparison)\n');

const date1 = new Date('2024-01-01');
const date2 = new Date('2024-06-15');
const date3 = new Date('2024-12-31');

console.log('日期 1:', formatDate(date1, 'YYYY-MM-DD'));
console.log('日期 2:', formatDate(date2, 'YYYY-MM-DD'));
console.log('日期 3:', formatDate(date3, 'YYYY-MM-DD'));
console.log('');
console.log('date1 在 date2 之前吗？', DateUtils.isBefore(date1, date2));
console.log('date3 在 date2 之后吗？', DateUtils.isAfter(date3, date2));
console.log('date2 在 date1 和 date3 之间吗？', DateUtils.isBetween(date2, date1, date3));

// ==================== 4. 相对时间 ====================
console.log('\n4️⃣ 相对时间 (Relative Time)\n');

const oneMinuteAgo = new Date(Date.now() - 60000);
const oneHourAgo = new Date(Date.now() - 3600000);
const oneDayAgo = new Date(Date.now() - 86400000);
const oneWeekAgo = new Date(Date.now() - 604800000);

console.log('1 分钟前:', timeAgo(oneMinuteAgo, 'zh'));
console.log('1 小时前:', timeAgo(oneHourAgo, 'zh'));
console.log('1 天前:', timeAgo(oneDayAgo, 'zh'));
console.log('1 周前:', timeAgo(oneWeekAgo, 'zh'));
console.log('');
console.log('1 minute ago:', timeAgo(oneMinuteAgo, 'en'));
console.log('1 hour ago:', timeAgo(oneHourAgo, 'en'));
console.log('1 day ago:', timeAgo(oneDayAgo, 'en'));
console.log('1 week ago:', timeAgo(oneWeekAgo, 'en'));

// ==================== 5. 周期边界 ====================
console.log('\n5️⃣ 周期边界 (Period Boundaries)\n');

const sampleDate = new Date('2024-06-15 14:30:45');

console.log('示例日期:', formatDate(sampleDate, 'YYYY-MM-DD HH:mm:ss'));
console.log('');
console.log('当天开始:', formatDate(DateUtils.startOfDay(sampleDate), 'YYYY-MM-DD HH:mm:ss'));
console.log('当天结束:', formatDate(DateUtils.endOfDay(sampleDate), 'YYYY-MM-DD HH:mm:ss'));
console.log('当周开始:', formatDate(DateUtils.startOfWeek(sampleDate), 'YYYY-MM-DD'));
console.log('当周结束:', formatDate(DateUtils.endOfWeek(sampleDate), 'YYYY-MM-DD'));
console.log('当月开始:', formatDate(DateUtils.startOfMonth(sampleDate), 'YYYY-MM-DD'));
console.log('当月结束:', formatDate(DateUtils.endOfMonth(sampleDate), 'YYYY-MM-DD'));
console.log('当年开始:', formatDate(DateUtils.startOfYear(sampleDate), 'YYYY-MM-DD'));
console.log('当年结束:', formatDate(DateUtils.endOfYear(sampleDate), 'YYYY-MM-DD'));

// ==================== 6. 实用工具 ====================
console.log('\n6️⃣ 实用工具 (Utilities)\n');

const testDate = new Date('2024-02-15');

console.log('测试日期:', formatDate(testDate, 'YYYY-MM-DD'));
console.log('');
console.log('2024 是闰年吗？', DateUtils.isLeapYear(2024));
console.log('2024 年 2 月有多少天？', DateUtils.getDaysInMonth(2024, 2));
console.log('当前季度:', DateUtils.getQuarter(new Date()));
console.log('今天是一年中的第几天？', DateUtils.getDayOfYear(new Date()));
console.log('今天是周数？', DateUtils.getWeekNumber(new Date()));
console.log('今天是周末吗？', DateUtils.isWeekend(new Date()));
console.log('今天是工作日吗？', DateUtils.isWeekday(new Date()));

// ==================== 7. 工作日计算 ====================
console.log('\n7️⃣ 工作日计算 (Business Days)\n');

const monday = new Date('2024-01-15'); // Monday
const friday = new Date('2024-01-19'); // Friday

console.log('周一:', formatDate(monday, 'YYYY-MM-DD dddd'));
console.log('周五:', formatDate(friday, 'YYYY-MM-DD dddd'));
console.log('');
console.log('周一到周五有多少个工作日？', DateUtils.businessDaysBetween(monday, friday));
console.log('周一 +5 个工作日:', formatDate(DateUtils.addBusinessDays(monday, 5), 'YYYY-MM-DD dddd'));

// ==================== 8. 下一个指定日期 ====================
console.log('\n8️⃣ 下一个指定日期 (Next Day)\n');

console.log('今天:', formatDate(new Date(), 'YYYY-MM-DD dddd'));
console.log('下一个周一:', formatDate(DateUtils.nextMonday(new Date()), 'YYYY-MM-DD'));
console.log('下一个周五:', formatDate(DateUtils.nextDay(new Date(), 5), 'YYYY-MM-DD'));

console.log('\n' + '='.repeat(50));
console.log('✅ 示例完成！\n');
