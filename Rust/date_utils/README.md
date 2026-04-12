# Date Utilities - AllToolkit

**功能完整的 Rust 日期时间工具 - 零依赖**

---

## 📦 功能特性

- ✅ **零依赖** - 仅使用 Rust 标准库
- ✅ **日期解析** - 支持多种格式 (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY 等)
- ✅ **日期格式化** - 自定义输出格式 (YYYY-MM-DD, EEEE MMMM D, YYYY 等)
- ✅ **日期计算** - 加减天数、月数、年数
- ✅ **日期比较** - before, after, equal, between
- ✅ **日期信息** - 年、月、日、星期、一年中的第几天
- ✅ **时间戳转换** - Unix 时间戳 (秒) 互相转换
- ✅ **日期范围** - 生成日期范围、工作日、周末
- ✅ **闰年检测** - 准确判断闰年
- ✅ **月份天数** - 计算每月天数
- ✅ **边界日期** - 月初、月末、年初、年末

---

## 🚀 快速开始

### 添加依赖

```toml
# Cargo.toml
[dependencies]
# 无需外部依赖！
```

### 基本使用

```rust
use date_utils::{Date, parse_date, format_date};

// 创建日期
let date = Date::new(2024, 3, 15).unwrap();
println!("{}", date); // 2024-03-15

// 获取今天
let today = Date::today();

// 解析日期
let date = parse_date("2024-03-15").unwrap();
let date = parse_date("15/03/2024").unwrap();
let date = parse_date("20240315").unwrap();

// 格式化日期
let formatted = format_date(&date, "YYYY-MM-DD");
let formatted = format_date(&date, "EEEE, MMMM D, YYYY"); // Friday, March 15, 2024

// 日期计算
let future = date.add_days(30);
let past = date.subtract_months(1);
let next_year = date.add_years(1);

// 日期比较
if date.is_before(&future) {
    println!("Today is before the future date");
}

// 获取信息
println!("Year: {}", date.year());
println!("Month: {}", date.month());
println!("Weekday: {}", date.weekday()); // Fri
println!("Day of year: {}", date.day_of_year()); // 75

// 时间戳
let timestamp = date.to_timestamp();
let date = Date::from_timestamp(1704067200);

// 日期范围
let start = parse_date("2024-01-01").unwrap();
let end = parse_date("2024-01-07").unwrap();
let range = date_utils::date_range(&start, &end);
let weekdays = date_utils::weekdays_in_range(&start, &end);
```

---

## 📖 API 参考

### 日期创建

#### `Date::new(year, month, day)` → `DateResult<Date>`

创建新日期，带验证。

```rust
let date = Date::new(2024, 3, 15).unwrap();
let invalid = Date::new(2024, 2, 30); // Err - 2 月没有 30 日
```

#### `Date::today()` → `Date`

获取当前日期。

```rust
let today = Date::today();
println!("Today is {}", today);
```

#### `Date::from_timestamp(ts)` → `Date`

从 Unix 时间戳创建日期。

```rust
let date = Date::from_timestamp(1704067200); // 2024-01-01
```

### 日期解析

#### `parse_date(input)` → `DateResult<Date>`

解析日期字符串，支持多种格式。

```rust
parse_date("2024-03-15").unwrap();   // ISO 格式
parse_date("2024/03/15").unwrap();   // 斜杠分隔
parse_date("15-03-2024").unwrap();   // 欧洲格式
parse_date("15/03/2024").unwrap();   // 欧洲格式
parse_date("03-15-2024").unwrap();   // 美国格式
parse_date("03/15/2024").unwrap();   // 美国格式
parse_date("20240315").unwrap();     // 紧凑格式
```

### 日期格式化

#### `format_date(date, format)` → `String`

格式化日期为字符串。

| 格式符 | 描述 | 示例 |
|--------|------|------|
| `YYYY` | 四位数年份 | 2024 |
| `YY` | 两位数年份 | 24 |
| `MM` | 两位数月份 | 03 |
| `M` | 一位数月份 | 3 |
| `DD` | 两位数日期 | 15 |
| `D` | 一位数日期 | 15 |
| `MMMM` | 完整月份名 | March |
| `MMM` | 缩写月份名 | Mar |
| `MMMM` | 完整月份名 | March |
| `EEEE` | 完整星期名 | Friday |
| `EEE` | 缩写星期名 | Fri |
| `D` | 一年中的第几天 | 75 |
| `W` | 星期几 (1-7) | 5 |

```rust
let date = Date::new(2024, 3, 15).unwrap();

format_date(&date, "YYYY-MM-DD");        // "2024-03-15"
format_date(&date, "MM/DD/YYYY");        // "03/15/2024"
format_date(&date, "DD/MM/YYYY");        // "15/03/2024"
format_date(&date, "MMMM D, YYYY");      // "March 15, 2024"
format_date(&date, "EEEE, MMMM D, YYYY"); // "Friday, March 15, 2024"
format_date(&date, "Day D of year D");   // "Day 15 of year 75"
```

### 日期计算

#### `date.add_days(days)` → `Date`

添加天数。

```rust
let date = Date::new(2024, 1, 1).unwrap();
let future = date.add_days(30); // 2024-01-31
```

#### `date.subtract_days(days)` → `Date`

减去天数。

```rust
let date = Date::new(2024, 1, 31).unwrap();
let past = date.subtract_days(30); // 2024-01-01
```

#### `date.add_months(months)` → `Date`

添加月份。自动调整月末日期。

```rust
let date = Date::new(2024, 1, 31).unwrap();
let next = date.add_months(1); // 2024-02-29 (闰年)
```

#### `date.add_years(years)` → `Date`

添加年份。闰年 2 月 29 日会自动调整。

```rust
let date = Date::new(2024, 2, 29).unwrap();
let next = date.add_years(1); // 2025-02-28
```

#### 运算符重载

```rust
let date = Date::new(2024, 1, 1).unwrap();
let future = date + 30;  // 加 30 天
let past = date - 30;    // 减 30 天
let diff = date2 - date1; // 日期差 (天数)
```

### 日期比较

```rust
let date1 = Date::new(2024, 1, 15).unwrap();
let date2 = Date::new(2024, 1, 20).unwrap();

date1.is_before(&date2);  // true
date1.is_after(&date2);   // false
date1.is_equal(&date2);   // false

let start = Date::new(2024, 1, 1).unwrap();
let end = Date::new(2024, 12, 31).unwrap();
date1.is_between(&start, &end); // true
```

### 日期信息

```rust
let date = Date::new(2024, 3, 15).unwrap();

date.year();           // 2024
date.month();          // 3
date.day();            // 15
date.month_enum();     // Month::March
date.weekday();        // Weekday::Friday
date.day_of_year();    // 75
date.is_leap_year();   // true
date.days_in_current_month(); // 31
```

### 时间戳

```rust
let date = Date::new(2024, 1, 1).unwrap();
let ts = date.to_timestamp();      // 1704067200
let date = Date::from_timestamp(ts); // 2024-01-01
```

### 日期范围

```rust
let start = Date::new(2024, 1, 1).unwrap();
let end = Date::new(2024, 1, 7).unwrap();

// 所有日期
let range = date_utils::date_range(&start, &end);
// [Jan 1, Jan 2, ..., Jan 7]

// 带步长
let range = date_utils::date_range_step(&start, &end, 2);
// [Jan 1, Jan 3, Jan 5, Jan 7]

// 仅工作日
let weekdays = date_utils::weekdays_in_range(&start, &end);
// [Jan 1 (Mon), Jan 2 (Tue), ..., Jan 5 (Fri)]

// 仅周末
let weekends = date_utils::weekends_in_range(&start, &end);
// [Jan 6 (Sat), Jan 7 (Sun)]
```

### 边界日期

```rust
let date = Date::new(2024, 3, 15).unwrap();

date.first_day_of_month();   // 2024-03-01
date.last_day_of_month();    // 2024-03-31
date.first_day_of_year();    // 2024-01-01
date.last_day_of_year();     // 2024-12-31
```

### 工具函数

```rust
// 闰年检测
date_utils::is_leap_year(2024); // true
date_utils::is_leap_year(2023); // false

// 月份天数
date_utils::days_in_month(2024, 2); // 29
date_utils::days_in_month(2024, 4); // 30
```

---

## 🧪 运行测试

```bash
cd Rust/date_utils
cargo test
```

---

## 📝 示例

查看 `examples/` 目录获取完整示例代码：

- `basic_usage.rs` - 基本用法
- `date_arithmetic.rs` - 日期计算
- `date_range.rs` - 日期范围
- `formatting.rs` - 日期格式化

---

## ⚡ 性能特点

- **零依赖** - 无外部 crate，编译快速，二进制小
- **零成本抽象** - 所有操作都是内联优化
- **无堆分配** - `Date` 是 Copy 类型，栈上分配
- **常量友好** - 大部分函数可在 const 上下文使用

---

## 📄 许可证

MIT License - 详见 AllToolkit 主仓库 LICENSE 文件。
