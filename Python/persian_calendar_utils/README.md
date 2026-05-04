# Persian Calendar Utilities (波斯历工具包)

波斯历( Jalali Calendar )与公历( Gregorian Calendar )之间的转换工具，纯 Python 实现，零外部依赖。

## 功能特性

- 🔄 **日期转换**: 波斯历 <-> 公历双向转换
- 📅 **儒略日转换**: 支持通过儒略日进行精确转换
- ✅ **闰年判断**: 33年周期规则的波斯历闰年算法
- 📝 **日期格式化**: 波斯语/英语双语格式化
- 🗓️ **月份名称**: 波斯历12个月双语名称
- 📊 **日期计算**: 加减天数、天数差、年日/周数计算
- 🐍 **Python兼容**: 与 datetime.date/datetime 无缝集成

## 安装

无需安装，直接导入使用：

```python
from persian_calendar_utils import (
    persian_to_gregorian,
    gregorian_to_persian,
    now_persian,
)
```

## 快速使用

### 日期转换

```python
# 波斯历转公历
gregorian_to_persian(1403, 1, 1)  # 波斯历新年 -> (2024, 3, 20)

# 公历转波斯历
persian_to_gregorian(2024, 3, 20)  # -> (1403, 1, 1)
```

### 当前日期

```python
# 获取当前波斯历日期
now_persian()  # -> (1403, 1, 15)
```

### 闰年判断

```python
is_leap_year_persian(1403)  # True (闰年)
is_leap_year_persian(1402)  # False (平年)
```

### 格式化

```python
format_persian_date(1403, 1, 1)  # '1403/01/01'
format_persian_date(1403, 1, 1, 'long', 'en')  # '1403 Farvardin 1'
```

## API 参考

### 核心转换函数

| 函数 | 说明 |
|------|------|
| `persian_to_gregorian(year, month, day)` | 波斯历转公历 |
| `gregorian_to_persian(year, month, day)` | 公历转波斯历 |
| `persian_from_date(date)` | Python date 转波斯历 |
| `persian_to_date(year, month, day)` | 波斯历转 Python date |

### 日期验证与计算

| 函数 | 说明 |
|------|------|
| `is_leap_year_persian(year)` | 判断闰年 |
| `days_in_persian_month(year, month)` | 获取月份天数 |
| `validate_persian_date(year, month, day)` | 验证日期有效性 |
| `persian_add_days(year, month, day, days)` | 日期加减 |
| `persian_diff_days(date1, date2)` | 计算天数差 |

### 格式化与名称

| 函数 | 说明 |
|------|------|
| `format_persian_date(year, month, day, format, lang)` | 格式化日期 |
| `get_persian_month_name(month, lang)` | 获取月份名称 |
| `get_persian_weekday_name(weekday, lang)` | 获取星期名称 |

### 常量

| 常量 | 说明 |
|------|------|
| `PERSIAN_MONTH_NAMES` | 波斯语月份名称列表 |
| `PERSIAN_MONTH_NAMES_EN` | 英语月份名称列表 |
| `PERSIAN_WEEKDAY_NAMES` | 波斯语星期名称列表 |
| `PERSIAN_WEEKDAY_NAMES_EN` | 英语星期名称列表 |

## 波斯历简介

波斯历( Jalali Calendar )是伊朗和阿富汗使用的官方太阳历：

- 🌸 **新年**: 春分(约3月20-21日)开始
- 📅 **月份**: 前6月31天，后5月30天，末月29/30天
- 🔄 **闰年**: 33年周期，8个闰年(周期位置: 1, 5, 9, 13, 17, 22, 26, 30)

月份名称：
| # | 波斯语 | 英语 |
|---|--------|------|
| 1 | فروردین | Farvardin |
| 2 | اردیبهشت | Ordibehesht |
| 3 | خرداد | Khordad |
| 4 | تیر | Tir |
| 5 | مرداد | Mordad |
| 6 | شهریور | Shahrivar |
| 7 | مهر | Mehr |
| 8 | آبان | Aban |
| 9 | آذر | Azar |
| 10 | دی | Dey |
| 11 | بهمن | Bahman |
| 12 | اسفند | Esfand |

## 运行测试

```bash
cd Python/persian_calendar_utils
python persian_calendar_utils_test.py
```

## 运行示例

```bash
cd Python/persian_calendar_utils/examples
python usage_examples.py
```

## 许可证

MIT License