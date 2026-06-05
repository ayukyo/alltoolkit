# Datetime Utils - 日期时间工具

功能丰富的日期时间处理工具库，支持解析、转换、计算和格式化。

## 功能特性

- ✅ 日期时间解析（ISO、标准格式、自然语言）
- ✅ 时区转换
- ✅ 工作日计算
- ✅ 年龄计算
- ✅ 人性化时间差格式化
- ✅ 日期范围工具
- ✅ 中文支持
- ✅ 零外部依赖

## 安装

无需安装，直接复制 `datetime_utils.py` 到项目即可使用。

```bash
pip install python-dateutil  # 可选，用于增强解析能力
```

## 快速开始

```python
from datetime_utils import format_datetime, parse_datetime, now_in_timezone

# 格式化当前时间
formatted = format_datetime("%Y年%m月%d日 %H:%M:%S")
print(formatted)  # 输出：2026年06月06日 00:00:00

# 解析日期字符串
dt = parse_datetime("2026-06-06 12:00:00")
print(dt)  # 输出：2026-06-06 12:00:00

# 获取指定时区的当前时间
tokyo_time = now_in_timezone("Asia/Tokyo")
print(tokyo_time)
```

## API 参考

### 解析函数

#### `parse_datetime(date_str: str, fmt: str = None) -> Optional[datetime]`
解析日期时间字符串。

```python
dt = parse_datetime("2026-06-06")  # 自动检测格式
dt = parse_datetime("2026/06/06 12:30", "%Y/%m/%d %H:%M")  # 指定格式
```

#### `parse_natural_time(text: str, base: datetime = None) -> Optional[datetime]`
解析自然语言时间描述。

```python
dt = parse_natural_time("明天上午9点")
dt = parse_natural_time("下周五", datetime.now())
dt = parse_natural_time("3天后")
```

#### `parse_weekday_cn(char: str) -> int`
解析中文星期字符。

```python
parse_weekday_cn("一")  # 返回 0（周一）
parse_weekday_cn("末")  # 返回 6（周日）
```

### 转换函数

#### `format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str`
格式化日期时间。

```python
formatted = format_datetime(dt, "%Y年%m月%d日")
```

#### `convert_timezone(dt: datetime, tz_name: str) -> datetime`
转换时区。

```python
from datetime import datetime
utc_time = datetime(2026, 6, 6, 12, 0, 0)
tokyo = convert_timezone(utc_time, "Asia/Tokyo")
```

#### `now_in_timezone(tz_name: str) -> datetime`
获取指定时区的当前时间。

```python
ny_time = now_in_timezone("America/New_York")
```

#### `timestamp_to_datetime(ts: Union[int, float], ms: bool = False) -> datetime`
时间戳转日期时间。

```python
dt = timestamp_to_datetime(1717660800)
dt_ms = timestamp_to_datetime(1717660800000, ms=True)
```

#### `datetime_to_timestamp(dt: datetime = None, ms: bool = False) -> Union[int, float]`
日期时间转时间戳。

```python
ts = datetime_to_timestamp()  # 当前时间戳
ts_ms = datetime_to_timestamp(ms=True)  # 毫秒时间戳
```

### 计算函数

#### `add_months(dt: datetime, months: int) -> datetime`
日期加减月。

```python
dt = add_months(datetime(2026, 1, 15), 2)  # 2026-03-15
dt = add_months(datetime(2026, 1, 31), 1)  # 2026-02-28（自动调整）
```

#### `add_years(dt: datetime, years: int) -> datetime`
日期加减年。

```python
dt = add_years(datetime(2026, 2, 29), 1)  # 2027-02-28（闰年处理）
```

#### `date_diff(start, end, unit: str = 'day') -> Union[int, float]`
计算日期间差。

```python
days = date_diff("2026-01-01", "2026-06-06")
weeks = date_diff("2026-01-01", "2026-06-06", unit='week')
hours = date_diff("2026-01-01", "2026-06-06", unit='hour')
```

#### `age(birthday: Union[date, datetime, str], reference: date = None) -> int`
计算年龄。

```python
age("1990-06-15")  # 以今天为基准计算年龄
age("1990-06-15", date(2026, 1, 1))  # 指定参考日期
```

#### `workdays_between(start, end, holidays: list = None) -> int`
计算工作日数量。

```python
workdays = workdays_between("2026-06-01", "2026-06-10")
```

#### `add_workdays(start, workdays: int, holidays: list = None)`
在起始日期后添加指定工作日数。

```python
next_working_day = add_workdays("2026-06-07", 3)  # 3个工作日后
```

#### `is_workday(dt: date, holidays: list = None) -> bool`
判断是否为工作日。

```python
is_workday(date(2026, 6, 6))  # 周五 -> True
is_workday(date(2026, 6, 7))  # 周六 -> False
```

### 星期计算函数

#### `next_weekday(base: datetime, weekday: int) -> datetime`
获取下一个指定星期几的日期。

```python
next_monday = next_weekday(datetime(2026, 6, 4), 0)  # 下一个周一
```

#### `this_weekday(base: datetime, weekday: int) -> datetime`
获取本周指定星期几的日期（如果已过则返回下周）。

```python
this_friday = this_weekday(datetime(2026, 6, 4), 4)  # 本周五
```

#### `last_weekday(base: datetime, weekday: int) -> datetime`
获取上周指定星期几的日期。

```python
last_monday = last_weekday(datetime(2026, 6, 4), 0)  # 上周一
```

### 范围函数

#### `date_range(start, end, step: int = 1) -> List[date]`
生成日期范围列表。

```python
dates = date_range("2026-06-01", "2026-06-05")
# [2026-06-01, 2026-06-02, 2026-06-03, 2026-06-04, 2026-06-05]
```

#### `get_month_range(year: int, month: int) -> Tuple[date, date]`
获取月份的开始和结束日期。

```python
start, end = get_month_range(2026, 6)
# (2026-06-01, 2026-06-30)
```

#### `get_week_range(dt: datetime = None) -> Tuple[date, date]`
获取本周的开始和结束日期。

```python
start, end = get_week_range()
# 默认以周一为开始，周日为结束
```

### 工具函数

#### `humanize_delta(seconds: Union[int, float]) -> str`
人性化时间差描述。

```python
humanize_delta(3661)   # "1小时1分1秒"
humanize_delta(90061)  # "1天1小时1分1秒"
```

#### `format_duration(seconds: Union[int, float]) -> str`
格式化时长。

```python
format_duration(3600)   # "1:00:00"
format_duration(90)    # "0:01:30"
```

#### `quarter(dt: datetime = None) -> int`
获取日期所在季度。

```python
quarter(date(2026, 4, 15))  # 2
```

#### `week_of_year(dt: datetime = None) -> Tuple[int, int]`
获取日期所在年份和周数。

```python
week_num, year = week_of_year(date(2026, 6, 6))
# (23, 2026) - 2026年第23周
```

#### `is_leap_year(year: int) -> bool`
判断是否为闰年。

```python
is_leap_year(2024)  # True
is_leap_year(2025)  # False
```

#### `days_in_month(year: int, month: int) -> int`
获取月份天数。

```python
days_in_month(2026, 2)  # 28
days_in_month(2024, 2)  # 29
```

#### `now(fmt: str = 'iso_datetime', tz: str = None) -> str`
获取当前时间（格式化字符串）。

```python
now()                          # ISO 格式
now("%Y年%m月%d日")            # 自定义格式
now(tz="Asia/Tokyo")           # 东京时间
```

#### `today(fmt: str = 'iso') -> str`
获取今天的日期字符串。

```python
today()                # "2026-06-06"
today("%Y/%m/%d")      # "2026/06/06"
```

## 运行测试

```bash
cd Python
python datetime_utils_test.py
```

## 注意事项

1. **时区名称**：使用标准 IANA 时区名称（如 "Asia/Shanghai"）
2. **日期解析**：优先尝试 ISO 格式，然后是常见格式
3. **闰年处理**：所有日期计算自动处理闰年
4. **工作日**：默认周一到周五为工作日，周六周日为休息日

## 许可证

MIT License - AllToolkit

## 版本

- Version: 1.0.0
- Author: AllToolkit
- Python: 3.6+