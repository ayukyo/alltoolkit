# Date Utils - 模块信息

## 快速参考

### 导入
```rust
use date_utils::{Date, parse_date, format_date};
use date_utils::{date_range, weekdays_in_range, weekends_in_range};
```

### 创建日期
```rust
let date = Date::new(2024, 3, 15)?;
let today = Date::today();
let from_ts = Date::from_timestamp(1704067200);
```

### 解析日期
```rust
parse_date("2024-03-15")?;     // ISO
parse_date("15/03/2024")?;     // 欧洲
parse_date("03/15/2024")?;     // 美国
parse_date("20240315")?;       // 紧凑
```

### 格式化
```rust
format_date(&date, "YYYY-MM-DD");           // 2024-03-15
format_date(&date, "MM/DD/YYYY");           // 03/15/2024
format_date(&date, "EEEE, MMMM D, YYYY");   // Friday, March 15, 2024
format_date(&date, "'Day ' DDD ' of year'"); // Day 75 of year
```

### 计算
```rust
date.add_days(30);
date.subtract_days(30);
date.add_months(1);
date.subtract_months(1);
date.add_years(1);
date.subtract_years(1);

// 运算符
let future = date + 30;
let past = date - 30;
let diff = date2 - date1;  // 天数差
```

### 比较
```rust
date1.is_before(&date2);
date1.is_after(&date2);
date1.is_equal(&date2);
date1.is_between(&start, &end);
date1.days_difference(&date2);
```

### 信息
```rust
date.year();              // 2024
date.month();             // 3
date.day();               // 15
date.weekday();           // Weekday::Friday
date.day_of_year();       // 75
Date::is_leap_year(2024); // true
Date::days_in_month(2024, 2); // 29
```

### 范围
```rust
let range = date_range(&start, &end);
let step_range = date_range_step(&start, &end, 7);
let workdays = weekdays_in_range(&start, &end);
let weekends = weekends_in_range(&start, &end);
```

### 边界
```rust
date.first_day_of_month();
date.last_day_of_month();
date.first_day_of_year();
date.last_day_of_year();
```

## 格式符

| 格式 | 说明 | 示例 |
|------|------|------|
| YYYY | 4 位年份 | 2024 |
| YY | 2 位年份 | 24 |
| MM | 2 位月份 | 03 |
| M | 1 位月份 | 3 |
| MMMM | 完整月份名 | March |
| MMM | 缩写月份名 | Mar |
| DD | 2 位日期 | 15 |
| D | 1 位日期 | 15 |
| DDD | 一年中的第几天 | 75 |
| EEEE | 完整星期名 | Friday |
| EEE | 缩写星期名 | Fri |
| W | 星期几 (1-7) | 5 |

**转义**: 使用单引号包裹普通文本 `'text'`

## 错误类型

```rust
pub enum DateError {
    InvalidFormat { input, expected },
    InvalidDate { year, month, day },
    InvalidMonth { month },
    InvalidDay { year, month, day },
    ParseError { message },
    Custom(String),
}
```

## 版本

- **当前版本**: 1.0.0
- **Rust Edition**: 2021
- **依赖**: 无
