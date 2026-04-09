# Date Utils - TypeScript 日期时间工具模块 📅

**零依赖的 TypeScript 日期时间处理工具 - 功能全面，生产就绪**

---

## 📦 功能特性

- ✅ **日期格式化** - 自定义格式、ISO、本地化格式
- ✅ **日期解析** - 多种格式自动识别、模糊解析
- ✅ **日期运算** - 加减天数、月份、年份
- ✅ **日期比较** - 前后判断、区间判断、相等判断
- ✅ **相对时间** - "X 分钟前"、"X days ago"
- ✅ **日期验证** - 有效性检查、闰年判断
- ✅ **周期计算** - 季度、周数、一年中的第几天
- ✅ **工作日计算** - 排除周末的业务日计算
- ✅ **零依赖** - 仅使用 TypeScript/JavaScript 标准库

---

## 🚀 快速开始

### 安装

无需安装！直接复制模块到你的项目：

```bash
# 复制整个模块
cp -r AllToolkit/TypeScript/date_utils your_project/

# 或克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

### 使用示例

```typescript
import { DateUtils } from './date_utils/mod.ts';
// 或单独导入
import { formatDate, addDays, isWeekend } from './date_utils/mod.ts';

// 格式化日期
const formatted = DateUtils.formatDate(new Date(), 'YYYY-MM-DD');
// "2024-01-15"

const human = DateUtils.formatDate(new Date(), 'MMMM D, YYYY', 'en');
// "January 15, 2024"

const chinese = DateUtils.formatDate(new Date(), 'YYYY 年 MM 月 DD 日', 'zh');
// "2024 年 01 月 15 日"

// 日期运算
const nextWeek = DateUtils.addDays(new Date(), 7);
const nextMonth = DateUtils.addMonths(new Date(), 1);
const nextYear = DateUtils.addYears(new Date(), 1);

// 日期比较
DateUtils.isBefore(new Date(), DateUtils.addDays(new Date(), 1)); // true
DateUtils.isAfter(new Date(), DateUtils.subtractDays(new Date(), 1)); // true

// 相对时间
DateUtils.timeAgo(new Date(Date.now() - 60000), 'zh'); // "1 分钟前"
DateUtils.timeAgo(new Date(Date.now() - 3600000), 'en'); // "1 hour ago"

// 周期计算
DateUtils.startOfDay(new Date()); // 今天 00:00:00
DateUtils.endOfMonth(new Date()); // 本月最后一天 23:59:59
DateUtils.getQuarter(new Date()); // 当前季度 (1-4)

// 工作日计算
DateUtils.isWeekend(new Date()); // 是否周末
DateUtils.addBusinessDays(new Date(), 5); // 5 个工作日后
```

---

## 📖 API 文档

### 格式化与解析

#### `formatDate(date, pattern?, locale?)`
格式化日期为字符串。

```typescript
formatDate(new Date(), 'YYYY-MM-DD'); // "2024-01-15"
formatDate(new Date(), 'MM/DD/YYYY'); // "01/15/2024"
formatDate(new Date(), 'YYYY 年 MM 月 DD 日', 'zh'); // "2024 年 01 月 15 日"
formatDate(new Date(), 'h:mm A'); // "2:30 PM"
```

**格式标记：**
| 标记 | 描述 | 示例 |
|------|------|------|
| `YYYY` | 4 位年份 | 2024 |
| `YY` | 2 位年份 | 24 |
| `MM` | 2 位月份 | 01-12 |
| `M` | 月份 | 1-12 |
| `MMMM` | 完整月份名 | January |
| `MMM` | 简短月份名 | Jan |
| `DD` | 2 位日期 | 01-31 |
| `D` | 日期 | 1-31 |
| `dddd` | 完整星期名 | Monday |
| `ddd` | 简短星期名 | Mon |
| `HH` | 24 小时制小时 | 00-23 |
| `H` | 小时 | 0-23 |
| `hh` | 12 小时制小时 | 01-12 |
| `h` | 小时 | 1-12 |
| `mm` | 分钟 | 00-59 |
| `ss` | 秒 | 00-59 |
| `SSS` | 毫秒 | 000-999 |
| `A` | AM/PM | AM/PM |
| `Z` | 时区偏移 | +08:00 |

#### `parseDate(dateString, pattern?)`
解析日期字符串为 Date 对象。

```typescript
parseDate('2024-01-15'); // Date 对象
parseDate('01/15/2024', 'MM/DD/YYYY'); // Date 对象
parseDate('2024 年 01 月 15 日'); // Date 对象
parseDate('invalid'); // null
```

#### `toDate(input)`
将各种输入转换为 Date 对象。

```typescript
toDate(new Date()); // Date
toDate(1705312800000); // Date
toDate('2024-01-15'); // Date
```

---

### 日期运算

#### `addDays(date, days)`
添加天数。

```typescript
addDays(new Date(), 7); // 7 天后
```

#### `addMonths(date, months)`
添加月份。

```typescript
addMonths(new Date(), 1); // 1 个月后
```

#### `addYears(date, years)`
添加年份。

```typescript
addYears(new Date(), 1); // 1 年后
```

#### `subtractDays(date, days)`
减去天数。

```typescript
subtractDays(new Date(), 5); // 5 天前
```

#### `diff(date1, date2, unit?)`
计算两个日期的差值。

```typescript
diff(new Date(), addDays(new Date(), 7), 'd'); // -7
diffDays(new Date(), addDays(new Date(), 7)); // -7
```

---

### 日期比较

#### `isBefore(date, compareTo)`
判断日期是否在之前。

```typescript
isBefore(new Date('2024-01-01'), new Date('2024-01-15')); // true
```

#### `isAfter(date, compareTo)`
判断日期是否在之后。

```typescript
isAfter(new Date('2024-01-15'), new Date('2024-01-01')); // true
```

#### `isBetween(date, start, end)`
判断日期是否在区间内。

```typescript
isBetween(new Date('2024-01-10'), new Date('2024-01-01'), new Date('2024-01-15')); // true
```

#### `isEqual(date1, date2)`
判断两个日期是否相等（精确到毫秒）。

```typescript
isEqual(new Date('2024-01-15'), new Date('2024-01-15')); // true
```

#### `isSameDay(date1, date2)`
判断两个日期是否是同一天（忽略时间）。

```typescript
isSameDay(new Date('2024-01-15 10:00'), new Date('2024-01-15 20:00')); // true
```

---

### 相对时间

#### `timeAgo(date, locale?)`
获取相对时间字符串（过去）。

```typescript
timeAgo(new Date(Date.now() - 60000), 'en'); // "1 minute ago"
timeAgo(new Date(Date.now() - 3600000), 'zh'); // "1 小时前"
timeAgo(new Date(Date.now() - 86400000), 'en'); // "1 day ago"
```

#### `fromNow(date, locale?)`
获取相对时间字符串（未来）。

```typescript
fromNow(addDays(new Date(), 7), 'en'); // "in 7 days"
fromNow(addDays(new Date(), 7), 'zh'); // "7 天后"
```

---

### 周期边界

#### `startOfDay(date)`
获取当天的开始（00:00:00）。

```typescript
startOfDay(new Date('2024-01-15 14:30')); // 2024-01-15 00:00:00
```

#### `endOfDay(date)`
获取当天的结束（23:59:59.999）。

```typescript
endOfDay(new Date('2024-01-15 14:30')); // 2024-01-15 23:59:59.999
```

#### `startOfWeek(date)`
获取当周的开始（周日）。

#### `endOfWeek(date)`
获取当周的结束（周六）。

#### `startOfMonth(date)`
获取当月的开始。

```typescript
startOfMonth(new Date('2024-01-15')); // 2024-01-01 00:00:00
```

#### `endOfMonth(date)`
获取当月的结束。

```typescript
endOfMonth(new Date('2024-01-15')); // 2024-01-31 23:59:59.999
```

#### `startOfYear(date)`
获取当年的开始。

#### `endOfYear(date)`
获取当年的结束。

---

### 工具函数

#### `isLeapYear(year)`
判断是否为闰年。

```typescript
isLeapYear(2024); // true
isLeapYear(2023); // false
```

#### `getDaysInMonth(year, month)`
获取月份的天数。

```typescript
getDaysInMonth(2024, 2); // 29 (闰年)
getDaysInMonth(2023, 2); // 28
```

#### `getQuarter(date)`
获取季度（1-4）。

```typescript
getQuarter(new Date('2024-01-15')); // 1
getQuarter(new Date('2024-06-15')); // 2
```

#### `getWeekNumber(date)`
获取周数（1-53）。

#### `getDayOfYear(date)`
获取一年中的第几天（1-366）。

#### `isWeekend(date)`
判断是否为周末。

```typescript
isWeekend(new Date('2024-01-13')); // true (Saturday)
```

#### `isWeekday(date)`
判断是否为工作日。

#### `nextDay(date, dayOfWeek)`
获取下一个指定星期几。

```typescript
nextDay(new Date(), DayOfWeek.Monday); // 下周一
```

#### `nextMonday(date)`
获取下一个周一。

#### `businessDaysBetween(start, end)`
计算两个日期之间的工作日天数。

```typescript
businessDaysBetween(new Date('2024-01-15'), new Date('2024-01-19')); // 5 (Mon-Fri)
```

#### `addBusinessDays(date, days)`
添加工作日（跳过周末）。

```typescript
addBusinessDays(new Date('2024-01-12'), 1); // 下周一（跳过周末）
```

#### `isValid(date)`
验证日期是否有效。

```typescript
isValid(new Date()); // true
isValid('2024-01-15'); // true
isValid('invalid'); // false
```

---

## 🧪 运行测试

```bash
# 使用 Deno
deno test date_utils_test.ts

# 使用 Bun
bun test date_utils_test.ts

# 使用 Node 18+
node --test date_utils_test.ts
```

---

## 📊 测试覆盖

- ✅ 日期格式化（多种格式、多语言）
- ✅ 日期解析（ISO、US、EU、中文格式）
- ✅ 日期运算（加减天数、月份、年份）
- ✅ 日期比较（前后、区间、相等）
- ✅ 相对时间（timeAgo、fromNow）
- ✅ 周期边界（startOf、endOf）
- ✅ 闰年判断
- ✅ 工作日计算
- ✅ 边界情况处理

---

## 🌍 多语言支持

支持英语和中文：

```typescript
// 英语
formatDate(new Date(), 'MMMM D, YYYY', 'en'); // "January 15, 2024"
timeAgo(new Date(Date.now() - 60000), 'en'); // "1 minute ago"

// 中文
formatDate(new Date(), 'YYYY 年 MM 月 DD 日', 'zh'); // "2024 年 01 月 15 日"
timeAgo(new Date(Date.now() - 60000), 'zh'); // "1 分钟前"
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
