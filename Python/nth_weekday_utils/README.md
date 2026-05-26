# Nth Weekday Utilities

零依赖的 Python 工具库，用于计算每月第 N 个星期几，支持节假日计算、日期查找等功能。

## 功能特性

- ✅ 查找每月第 N 个星期几（如"11月的第4个星期四"）
- ✅ 查找每月最后一个/第一个星期几
- ✅ 获取一个月内所有特定星期几的日期
- ✅ 计算指定星期几在月份中的出现次数
- ✅ 判断一个日期是第几个星期几
- ✅ 常见节假日计算（感恩节、劳动节、母亲节等）
- ✅ 日期范围内的星期几查找与计数
- ✅ 前后星期几查找
- ✅ 多语言星期/月份名称

## 安装

无需外部依赖，直接导入使用：

```python
from nth_weekday_utils.mod import NthWeekdayUtils, Weekday
```

## 快速示例

### 基本使用

```python
from nth_weekday_utils.mod import nth_weekday, Weekday

# 查找 2024 年 11 月的第 4 个星期四（感恩节）
thanksgiving = nth_weekday(2024, 11, 4, Weekday.THURSDAY)
print(thanksgiving)  # 2024-11-28

# 查找 2024 年 5 月的最后一个星期一（阵亡将士纪念日）
memorial_day = nth_weekday(2024, 5, -1, Weekday.MONDAY)
print(memorial_day)  # 2024-05-27

# 查找 2024 年 9 月的第 1 个星期一（劳动节）
labor_day = nth_weekday(2024, 9, 1, Weekday.MONDAY)
print(labor_day)  # 2024-09-02
```

### 节假日计算

```python
from nth_weekday_utils.mod import holiday, list_holidays

# 计算感恩节
thanksgiving = holiday('thanksgiving', 2024)
print(thanksgiving)  # 2024-11-28

# 列出美国 2024 年所有基于第 N 个星期几的节假日
holidays = list_holidays(2024, 'us')
for name, date in holidays:
    print(f"{name}: {date}")
```

### 月份内所有星期几

```python
from nth_weekday_utils.mod import all_weekdays_in_month, Weekday

# 获取 2024 年 11 月所有星期四
thursdays = all_weekdays_in_month(2024, 11, Weekday.THURSDAY)
print(thursdays)  # [2024-11-07, 2024-11-14, 2024-11-21, 2024-11-28]

# 计算出现次数
count = len(thursdays)  # 4
```

### 日期范围查询

```python
from nth_weekday_utils.mod import weekdays_between, Weekday

# 获取 2024 年 1 月所有星期五
fridays = weekdays_between('2024-01-01', '2024-01-31', Weekday.FRIDAY)
print(fridays)  # [2024-01-05, 2024-01-12, 2024-01-19, 2024-01-26]
```

## API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `nth_weekday(year, month, nth, weekday)` | 查找第 N 个星期几 |
| `last_weekday(year, month, weekday)` | 查找最后一个星期几 |
| `first_weekday(year, month, weekday)` | 查找第一个星期几 |
| `all_weekdays_in_month(year, month, weekday)` | 所有星期几列表 |
| `count_weekdays_in_month(year, month, weekday)` | 计数 |
| `which_nth_weekday(date)` | 判断是第几个 |

### 节假日函数

| 函数 | 说明 |
|------|------|
| `holiday(name, year)` | 计算指定节假日 |
| `list_holidays(year, country)` | 列出国家节假日 |

### 范围函数

| 函数 | 说明 |
|------|------|
| `weekdays_between(start, end, weekday)` | 日期范围内所有星期几 |
| `count_weekdays_between(start, end, weekday)` | 计数 |
| `next_weekday_after(date, weekday)` | 下一个星期几 |
| `previous_weekday_before(date, weekday)` | 上一个星期几 |

### 名称函数

| 函数 | 说明 |
|------|------|
| `weekday_name(weekday, lang)` | 星期名称（多语言） |
| `month_name(month, lang)` | 月份名称（多语言） |

## Weekday 枚举

```python
Weekday.MONDAY = 0
Weekday.TUESDAY = 1
Weekday.WEDNESDAY = 2
Weekday.THURSDAY = 3
Weekday.FRIDAY = 4
Weekday.SATURDAY = 5
Weekday.SUNDAY = 6
```

## 支持的节假日

### 美国
- `martin_luther_king_day` - 1 月第 3 个星期一
- `presidents_day` - 2 月第 3 个星期一
- `memorial_day` - 5 月最后一个星期一
- `labor_day` - 9 月第 1 个星期一
- `columbus_day` - 10 月第 2 个星期一
- `thanksgiving` - 11 月第 4 个星期四
- `mothers_day` - 5 月第 2 个星期日
- `fathers_day` - 6 月第 3 个星期日

### 英国
- `early_may_bank_holiday` - 5 月第 1 个星期一
- `spring_bank_holiday` - 5 月最后一个星期一
- `summer_bank_holiday` - 8 月最后一个星期一

### 加拿大
- `thanksgiving_canada` - 10 月第 2 个星期一
- `victoria_day` - 5 月第 3 个星期一

## 多语言支持

支持语言：`en`（英语）、`zh`（中文）、`es`（西班牙语）、`fr`（法语）、`de`（德语）、`ja`（日语）

```python
from nth_weekday_utils.mod import weekday_name, month_name, Weekday

print(weekday_name(Weekday.MONDAY, 'en'))  # Monday
print(weekday_name(Weekday.MONDAY, 'zh'))  # 星期一
print(weekday_name(Weekday.MONDAY, 'ja'))  # 月曜日

print(month_name(11, 'en'))  # November
print(month_name(11, 'zh'))  # 十一月
```

## 测试

```bash
python nth_weekday_utils_test.py
```

## License

MIT