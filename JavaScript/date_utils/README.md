# Date Utilities - JavaScript 日期时间工具模块

> 零依赖、全功能的日期时间处理工具库

## 功能特性

- ✅ **日期创建** - 支持多种输入格式创建日期
- ✅ **日期获取** - 获取年/月/日/时/分/秒等组件
- ✅ **日期计算** - 加减年/月/日/时/分/秒，计算差值
- ✅ **日期比较** - 判断同天/同周/同月/同年，前后关系
- ✅ **日期边界** - 获取日/周/月/季/年的开始和结束
- ✅ **格式化** - 支持自定义格式，包含12小时制、星期、中文
- ✅ **相对时间** - "刚刚"、"5分钟前"、"昨天"等友好描述
- ✅ **解析** - 支持格式解析和自动解析
- ✅ **验证** - 验证日期和时间有效性
- ✅ **工具方法** - 获取日期范围、星期计算、年龄计算等

## 安装使用

```javascript
// CommonJS
const DateUtils = require('./mod.js');

// ES Module
import DateUtils from './mod.js';
```

## API 文档

### 常量

```javascript
// 时间单位（毫秒）
DateUtils.MS.SECOND   // 1000
DateUtils.MS.MINUTE   // 60000
DateUtils.MS.HOUR     // 3600000
DateUtils.MS.DAY      // 86400000
DateUtils.MS.WEEK     // 604800000

// 星期名称
DateUtils.WEEKDAYS_CN     // ['日', '一', '二', '三', '四', '五', '六']
DateUtils.WEEKDAYS_EN     // ['Sunday', 'Monday', ...]
DateUtils.WEEKDAYS_SHORT  // ['Sun', 'Mon', ...]

// 月份名称
DateUtils.MONTHS_CN       // ['一月', '二月', ...]
DateUtils.MONTHS_EN       // ['January', 'February', ...]
DateUtils.MONTHS_SHORT    // ['Jan', 'Feb', ...]
```

### 创建日期

```javascript
// 当前时间
DateUtils.now()           // Date 对象
DateUtils.timestamp()     // 毫秒时间戳
DateUtils.unix()          // 秒时间戳

// 从时间戳创建（自动判断秒/毫秒）
DateUtils.fromTimestamp(1609459200)    // 秒
DateUtils.fromTimestamp(1609459200000) // 毫秒

// 多格式创建
DateUtils.create('2024-03-15')
DateUtils.create(1609459200000)
DateUtils.create(new Date())

// 指定组件创建
DateUtils.createFrom(2024, 3, 15, 14, 30, 45, 123)
```

### 获取组件

```javascript
const date = new Date(2024, 2, 15, 14, 30, 45, 123)

DateUtils.getYear(date)          // 2024
DateUtils.getMonth(date)         // 3 (1-12)
DateUtils.getDay(date)           // 15
DateUtils.getWeekday(date)       // 5 (0-6, 0=周日)
DateUtils.getHour(date)          // 14
DateUtils.getMinute(date)        // 30
DateUtils.getSecond(date)        // 45
DateUtils.getMillisecond(date)   // 123
DateUtils.getDayOfYear(date)     // 75 (一年第几天)
DateUtils.getWeekOfYear(date)    // 11 (ISO周)
DateUtils.getQuarter(date)       // 1 (季度1-4)
DateUtils.getDaysInMonth(date)   // 31 (当月天数)
```

### 日期计算

```javascript
const date = new Date(2024, 2, 15)

// 加法
DateUtils.addYears(date, 1)      // 2025-03-15
DateUtils.addMonths(date, 2)     // 2024-05-15
DateUtils.addDays(date, 10)      // 2024-03-25
DateUtils.addHours(date, 5)      // +5小时
DateUtils.addMinutes(date, 30)   // +30分钟
DateUtils.addSeconds(date, 60)   // +60秒

// 差值计算
DateUtils.diffDays(date1, date2)     // 天数差
DateUtils.diffHours(date1, date2)    // 小时差
DateUtils.diffMinutes(date1, date2)  // 分钟差
DateUtils.diffSeconds(date1, date2)  // 秒差
```

### 日期比较

```javascript
DateUtils.isSameDay(date1, date2)    // 是否同一天
DateUtils.isSameWeek(date1, date2)   // 是否同一周
DateUtils.isSameMonth(date1, date2)  // 是否同一月
DateUtils.isSameYear(date1, date2)   // 是否同一年

DateUtils.isToday(date)      // 是否今天
DateUtils.isYesterday(date)  // 是否昨天
DateUtils.isTomorrow(date)   // 是否明天

DateUtils.isWeekday(date)    // 是否工作日
DateUtils.isWeekend(date)    // 是否周末

DateUtils.isLeapYear(2024)   // 是否闰年
DateUtils.isBetween(date, start, end)  // 是否在范围内
```

### 日期边界

```javascript
DateUtils.startOfDay(date)      // 00:00:00.000
DateUtils.endOfDay(date)        // 23:59:59.999
DateUtils.startOfWeek(date)     // 周一 00:00:00
DateUtils.endOfWeek(date)       // 周日 23:59:59
DateUtils.startOfMonth(date)    // 月初 1日
DateUtils.endOfMonth(date)      // 月末最后一天
DateUtils.startOfYear(date)     // 年初 1月1日
DateUtils.endOfYear(date)       // 年末 12月31日
DateUtils.startOfQuarter(date)  // 季初
DateUtils.endOfQuarter(date)    // 季末
```

### 格式化

```javascript
const date = new Date(2024, 2, 15, 14, 30, 45, 123)

// 自定义格式
DateUtils.format(date, 'YYYY-MM-DD')          // '2024-03-15'
DateUtils.format(date, 'YYYY-MM-DD HH:mm:ss') // '2024-03-15 14:30:45'
DateUtils.format(date, 'hh:mm A')             // '02:30 PM'
DateUtils.format(date, 'dddd')                // '五' (星期中文)

// 格式占位符：
// YYYY - 4位年, YY - 2位年
// MM - 2位月, M - 月
// DD - 2位日, D - 日
// HH - 24小时制, H - 小时
// hh - 12小时制, h - 小时(12)
// mm - 分钟, m - 分钟
// ss - 秒, s - 秒
// SSS - 毫秒
// A/a - AM/PM/am/pm
// d - 星期数字, dd - 简写, ddd - 全称, dddd - 中文

// 快捷方法
DateUtils.toISO(date)           // ISO 8601 字符串
DateUtils.toLocalDate(date)     // '2024-03-15'
DateUtils.toLocalTime(date)     // '14:30:45'
DateUtils.toLocalDateTime(date) // '2024-03-15 14:30:45'
DateUtils.toChineseDate(date)   // '2024年3月15日 星期五'

// 相对时间
DateUtils.toRelative(date)      // '刚刚' / '5分钟前' / '昨天'
```

### 解析

```javascript
// 格式解析
DateUtils.parse('2024-03-15', 'YYYY-MM-DD')
DateUtils.parse('2024-03-15 14:30:00', 'YYYY-MM-DD HH:mm:ss')

// 自动解析（尝试多种常见格式）
DateUtils.parseAuto('2024/03/15')
DateUtils.parseAuto('15-03-2024')
```

### 验证

```javascript
DateUtils.isValid(date)                     // 是否有效日期
DateUtils.isValidDate(2024, 3, 15)          // 是否有效日期组件
DateUtils.isValidTime(14, 30, 45)           // 是否有效时间组件
```

### 工具方法

```javascript
// 获取日期范围内的所有日期
DateUtils.getDatesBetween(start, end)

// 获取月份内所有日期
DateUtils.getDatesInMonth(date)

// 获取周内所有日期
DateUtils.getDatesInWeek(date)

// 获取下一个/上一个指定星期几
DateUtils.getNextWeekday(date, 1)   // 下一个周一
DateUtils.getPrevWeekday(date, 1)   // 上一个周一

// 获取某月第n个星期几
DateUtils.getNthWeekdayOfMonth(2024, 3, 2, 2)  // 3月第2个周二

// 复制日期/时间
DateUtils.cloneDate(date)
DateUtils.cloneTime(date)

// 设置时间
DateUtils.setTime(date, { hour: 14, minute: 30 })

// 比较
DateUtils.compare(date1, date2)  // -1, 0, 1

// 计算年龄
DateUtils.getAge(birthday)
```

## 使用示例

```javascript
const DateUtils = require('./mod.js');

// 创建日期
const date = DateUtils.createFrom(2024, 3, 15, 14, 30);

// 格式化
console.log(DateUtils.format(date, 'YYYY-MM-DD HH:mm:ss'));
// 输出: 2024-03-15 14:30:00

// 相对时间
console.log(DateUtils.toRelative(new Date(Date.now() - 5 * 60 * 1000)));
// 输出: 5分钟前

// 判断
console.log(DateUtils.isWeekday(date));  // true
console.log(DateUtils.isLeapYear(2024)); // true

// 计算差值
const later = DateUtils.addDays(date, 10);
console.log(DateUtils.diffDays(date, later));  // 10

// 获取季度
console.log(DateUtils.getQuarter(date));  // 1

// 中文日期
console.log(DateUtils.toChineseDate(date));
// 输出: 2024年3月15日 星期五
```

## 测试

```bash
node date_utils_test.js
```

## 特性

- **零依赖** - 仅使用 JavaScript 标准库
- **全功能** - 涵盖日常开发所有日期时间需求
- **类型安全** - 所有参数有默认值和边界检查
- **国际化** - 支持中英文星期和月份名称
- **灵活格式** - 支持自定义格式化占位符

## 版本

- v1.0.0 - 初始版本