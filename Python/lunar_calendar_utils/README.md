# 农历日历工具模块 (Lunar Calendar Utils)

农历日历工具模块，提供农历与公历之间的转换，支持节气计算、传统节日查询、生肖干支计算等功能。

## 功能特性

### 核心转换
- **公历转农历**：将公历日期转换为农历日期
- **农历转公历**：将农历日期转换为公历日期
- **闰月支持**：正确处理闰月的转换

### 干支计算
- **年干支**：计算年份的天干地支
- **月干支**：计算月份的天干地支
- **日干支**：计算日期的天干地支
- **时辰干支**：计算时辰的天干地支

### 其他功能
- **生肖计算**：根据年份计算生肖
- **星座计算**：根据公历日期计算星座
- **节气查询**：查询24节气日期
- **节日查询**：查询传统节日和公历节日
- **农历格式化**：格式化农历日期为中文表示

## 支持范围

- **年份范围**：1900年 - 2100年
- **无外部依赖**：仅使用 Python 标准库

## 快速使用

### 公历转农历

```python
from lunar_calendar_utils.mod import solar_to_lunar, format_lunar_date

# 转换日期
lunar = solar_to_lunar(2024, 2, 10)
print(lunar)  # LunarDate(2024, 1, 1)

# 格式化输出
print(format_lunar_date(lunar))  # 甲辰年（龙年）正月初一
```

### 农历转公历

```python
from lunar_calendar_utils.mod import lunar_to_solar

# 正常月份
solar = lunar_to_solar(2024, 1, 1)
print(solar)  # 2024-02-10

# 闰月（2023年有闰二月）
solar = lunar_to_solar(2023, 2, 1, True)
print(solar)  # 2023-03-22
```

### 干支计算

```python
from lunar_calendar_utils.mod import get_year_ganzhi, get_zodiac

# 年干支
ganzhi = get_year_ganzhi(2024)
print(ganzhi)  # 甲辰

# 生肖
zodiac = get_zodiac(2024)
print(zodiac)  # 龙
```

### 节日查询

```python
from lunar_calendar_utils.mod import get_all_festivals

# 查询某日的所有节日
festivals = get_all_festivals(2024, 2, 10)
print(festivals)  # ['春节']
```

### 获取完整信息

```python
from lunar_calendar_utils.mod import get_lunar_info

# 获取完整农历信息
info = get_lunar_info(2024, 2, 10)
print(info)
# {
#   'solar_date': '2024-02-10',
#   'lunar_date': '农历正月初一',
#   'year_ganzhi': '甲辰',
#   'zodiac': '龙',
#   'constellation': '水瓶座',
#   'solar_term': '立春',
#   'festivals': ['春节'],
#   ...
# }
```

### LunarCalendar 类

```python
from lunar_calendar_utils.mod import LunarCalendar

# 创建年历
cal = LunarCalendar(2024)

# 获取年份信息
info = cal.get_year_info()
print(info['ganzhi'])  # 甲辰
print(info['zodiac'])  # 龙

# 获取节气
terms = cal.get_solar_terms()
for name, date in terms[:6]:
    print(f"{name}: {date}")
```

### 便捷函数

```python
from lunar_calendar_utils.mod import today_lunar, today_info, quick_convert
from datetime import date

# 今天农历
lunar = today_lunar()
print(lunar)

# 今天完整信息
info = today_info()

# 快速转换
result = quick_convert(date.today())
```

## API 参考

### LunarDate 类

| 属性/方法 | 说明 |
|-----------|------|
| `year` | 农历年份 |
| `month` | 农历月份 |
| `day` | 农历日 |
| `is_leap_month` | 是否是闰月 |
| `__str__()` | 中文表示 |
| `get_ganzhi_year()` | 年干支 |
| `get_zodiac()` | 生肖 |

### 转换函数

| 函数 | 说明 |
|------|------|
| `solar_to_lunar(year, month, day)` | 公历转农历 |
| `lunar_to_solar(year, month, day, is_leap)` | 农历转公历 |

### 干支函数

| 函数 | 说明 |
|------|------|
| `get_year_ganzhi(year)` | 年干支 |
| `get_month_ganzhi(year, month)` | 月干支 |
| `get_day_ganzhi(year, month, day)` | 日干支 |
| `get_hour_ganzhi(day_ganzhi, hour)` | 时辰干支 |

### 其他函数

| 函数 | 说明 |
|------|------|
| `get_zodiac(year)` | 生肖 |
| `get_constellation(month, day)` | 星座 |
| `get_solar_term_year(year)` | 一年节气 |
| `get_lunar_festival(year, month, day, is_leap)` | 农历节日 |
| `get_solar_festival(month, day)` | 公历节日 |
| `get_all_festivals(year, month, day)` | 所有节日 |

## 常量

| 常量 | 说明 |
|------|------|
| `TIAN_GAN` | 十天干 |
| `DI_ZHI` | 十二地支 |
| `ZODIAC` | 十二生肖 |
| `LUNAR_MONTH_NAMES` | 农历月份名称 |
| `LUNAR_DAY_NAMES` | 农历日期名称 |

## 测试

运行测试：

```bash
python lunar_calendar_utils_test.py
```

测试覆盖：
- 公历农历转换（正常、闰月、边界）
- 干支计算
- 生肖星座计算
- 节气节日查询
- 边界值和异常情况

## 文件结构

```
lunar_calendar_utils/
├── mod.py                 # 主模块
├── lunar_calendar_utils_test.py  # 测试文件
├── README.md              # 本文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 注意事项

1. 年份范围限制为 1900-2100 年
2. 闰月转换需要明确指定 `is_leap_month=True`
3. 节气日期为估算值，可能与实际天文日期有1-2天的偏差
4. 除夕日期根据农历腊月最后一天动态计算

## 更新日志

- 2026-04-23: 初始版本
  - 公历农历互转
  - 干支生肖星座计算
  - 节气节日查询
  - 完整测试覆盖（167 测试用例）

## 许可证

MIT License