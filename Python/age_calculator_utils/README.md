# Age Calculator Utilities - 年龄计算工具模块

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

提供完整的年龄计算功能，零依赖，仅使用 Python 标准库。

## 功能特性

- ✅ **精确年龄计算** - 支持年、月、日精确计算
- ✅ **多单位年龄** - 支持天、周、月、小时等单位
- ✅ **生日倒计时** - 计算距离下一个生日的天数
- ✅ **代际分类** - 自动识别代际（婴儿潮、千禧一代、Z世代等）
- ✅ **年龄里程碑** - 特殊生日、天数里程碑计算
- ✅ **闰年生日** - 支持2月29日出生的特殊处理
- ✅ **中国生肖** - 基于年份的生肖计算
- ✅ **年龄格式化** - 多种格式输出
- ✅ **灵活日期输入** - 支持 date/datetime/str 多种格式

## 安装

无需安装，直接复制模块到项目中使用。

## 快速开始

### 基本用法

```python
from age_calculator_utils import calculate_age, format_age, days_until_birthday

# 计算年龄
age = calculate_age("1990-05-15")
print(f"年龄: {age}岁")  # 输出: 年龄: 34岁

# 格式化年龄
formatted = format_age("1990-05-15")
print(f"精确年龄: {formatted}")  # 输出: 34岁2个月5天

# 生日倒计时
days = days_until_birthday("1990-12-25")
print(f"距离生日还有 {days} 天")
```

### 精确年龄计算

```python
from age_calculator_utils import calculate_exact_age

years, months, days = calculate_exact_age("1990-03-15", "2024-05-20")
print(f"{years}岁{months}个月{days}天")  # 输出: 34岁2个月5天
```

### 代际分类

```python
from age_calculator_utils import get_generation, AgeCalculatorUtils

# 获取代际
generation = get_generation("1990-05-15")
print(f"代际: {generation.value}")  # 输出: 千禧一代

# 获取详细信息
info = AgeCalculatorUtils.get_generation_info("1990-05-15")
print(f"英文名: {info['english_name']}")  # 输出: Millennial (Gen Y)
print(f"年份范围: {info['year_range']}")  # 输出: (1981, 1996)
print(f"特征: {info['characteristics']}")  # 输出: ['精通科技', '重视工作生活平衡', ...]
```

### 年龄里程碑

```python
from age_calculator_utils import AgeCalculatorUtils

# 获取所有里程碑
milestones = AgeCalculatorUtils.get_age_milestones("1990-05-15")
for m in milestones[:5]:
    print(f"{m['description']} - {m['date']} - {m['status']}")

# 获取下一个里程碑
next_milestone = AgeCalculatorUtils.get_next_milestone("1990-05-15")
print(f"下一个里程碑: {next_milestone['description']}")
print(f"还有 {next_milestone['days_until']} 天")
```

### 生日信息

```python
from age_calculator_utils import AgeCalculatorUtils

info = AgeCalculatorUtils.get_birthday_info("1990-06-15")
print(f"当前年龄: {info['current_age']}岁")
print(f"精确年龄: {info['exact_age']}")
print(f"今天是生日: {info['is_birthday_today']}")
print(f"距离下次生日: {info['days_until_birthday']}天")
print(f"已生活总天数: {info['total_days_lived']}天")
```

### 不同单位计算

```python
from age_calculator_utils import AgeCalculatorUtils

birth = "1990-05-15"

# 天数
days = AgeCalculatorUtils.calculate_age_in_days(birth)
print(f"已生活 {days} 天")

# 周数
weeks, remainder = AgeCalculatorUtils.calculate_age_in_weeks(birth)
print(f"已生活 {weeks} 周 {remainder} 天")

# 月数
months = AgeCalculatorUtils.calculate_age_in_months(birth)
print(f"已生活 {months} 个月")

# 小时
hours = AgeCalculatorUtils.calculate_age_in_hours(birth)
print(f"已生活 {hours} 小时")
```

### 年龄差计算

```python
from age_calculator_utils import AgeCalculatorUtils

diff = AgeCalculatorUtils.calculate_age_difference("1990-05-15", "1985-05-15")
print(f"年龄差: {diff['difference_years']}年 {diff['difference_months']}个月")
print(f"相差天数: {diff['difference_days']}天")
```

### 中国生肖

```python
from age_calculator_utils import AgeCalculatorUtils

zodiac = AgeCalculatorUtils.get_chinese_zodiac("2000-01-01")
print(f"生肖: {zodiac}")  # 输出: 龙
```

### 闰年生日宝宝

```python
from age_calculator_utils import AgeCalculatorUtils

birth = "2000-02-29"

# 判断是否是闰年宝宝
is_leap_baby = AgeCalculatorUtils.is_leap_year_baby(birth)
print(f"是闰年宝宝: {is_leap_baby}")  # 输出: True

# 获取闰年宝宝特殊信息
info = AgeCalculatorUtils.get_leap_year_birthday_info(birth)
print(f"真实生日次数: {info['real_birthday_count']}")
print(f"下一个真实生日: {info['next_real_birthday']}")
```

### 年龄格式化

```python
from age_calculator_utils import format_age

birth = "1990-03-15"

print(format_age(birth, format_type="full"))   # 输出: 34岁2个月5天
print(format_age(birth, format_type="simple")) # 输出: 34岁
print(format_age(birth, format_type="days"))   # 输出: 12506天
print(format_age(birth, format_type="weeks"))  # 输出: 1786周4天
```

## API 参考

### 便捷函数

| 函数 | 说明 | 返回类型 |
|------|------|----------|
| `calculate_age(birth_date, reference_date=None)` | 计算年龄（周岁） | `int` |
| `calculate_exact_age(birth_date, reference_date=None)` | 计算精确年龄 | `Tuple[int, int, int]` |
| `days_until_birthday(birth_date, reference_date=None)` | 距离生日天数 | `int` |
| `get_generation(birth_date)` | 获取代际分类 | `Generation` |
| `format_age(birth_date, reference_date=None, format_type="full")` | 格式化年龄 | `str` |

### AgeCalculatorUtils 类方法

| 方法 | 说明 |
|------|------|
| `calculate_age()` | 计算年龄（周岁） |
| `calculate_exact_age()` | 计算精确年龄（年月日） |
| `calculate_age_in_days()` | 计算年龄（天数） |
| `calculate_age_in_weeks()` | 计算年龄（周数+天数） |
| `calculate_age_in_months()` | 计算年龄（月数） |
| `calculate_age_in_hours()` | 计算年龄（小时数） |
| `days_until_birthday()` | 距离生日天数 |
| `next_birthday_date()` | 下一个生日日期 |
| `get_birthday_info()` | 获取完整生日信息 |
| `get_generation()` | 获取代际分类 |
| `get_generation_info()` | 获取代际详细信息 |
| `calculate_age_difference()` | 计算两日期年龄差 |
| `get_age_milestones()` | 获取年龄里程碑列表 |
| `get_next_milestone()` | 获取下一个里程碑 |
| `get_chinese_zodiac()` | 获取中国生肖 |
| `is_leap_year_baby()` | 判断是否闰年宝宝 |
| `get_leap_year_birthday_info()` | 闰年宝宝信息 |
| `format_age()` | 格式化年龄显示 |

### Generation 枚举

| 值 | 中文名 | 年份范围 |
|----|--------|----------|
| `GREATEST` | 最伟大一代 | 1901-1927 |
| `SILENT` | 沉默的一代 | 1928-1945 |
| `BABY_BOOMER` | 婴儿潮一代 | 1946-1964 |
| `GENERATION_X` | X世代 | 1965-1980 |
| `MILLENNIAL` | 千禧一代 | 1981-1996 |
| `GENERATION_Z` | Z世代 | 1997-2012 |
| `GENERATION_ALPHA` | 阿尔法世代 | 2013-2025 |

## 支持的日期格式

- `date` 对象
- `datetime` 对象
- 字符串格式（默认 `"%Y-%m-%d"`）：
  - `"1990-05-15"` (默认)
  - `"1990/05/15"` (自动识别)
  - `"15-05-1990"` (自动识别)
  - `"19900515"` (自动识别)

## 测试

```bash
python -m pytest age_calculator_utils_test.py -v
```

或直接运行：

```bash
python age_calculator_utils_test.py
```

## 许可证

MIT License

## 作者

AllToolkit