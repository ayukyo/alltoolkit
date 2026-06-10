# Constellation Utils - 星座与生肖工具

星座查询和生肖计算工具，零依赖。

## 功能特性

- **星座查询**: 根据日期查询星座
- **生肖计算**: 根据年份计算生肖
- **日期范围**: 包含各星座精确日期边界
- **中英文支持**: 支持中英文星座名称

## 快速开始

```python
from constellation_utils.mod import get_zodiac, get_chinese_zodiac, Zodiac

# 根据日期获取星座
zodiac = get_zodiac(6, 15)  # 6月15日
print(zodiac)  # Zodiac.GEMINI

# 根据日期对象获取
from datetime import date
zodiac = get_zodiac_from_date(date(1990, 4, 15))
print(zodiac)  # Zodiac.ARIES

# 获取生肖
animal = get_chinese_zodiac(2024)
print(animal)  # "龙"
```

## API 参考

| 函数 | 说明 |
|------|------|
| `get_zodiac(month, day)` | 根据月日获取星座 |
| `get_zodiac_from_date(date_obj)` | 根据日期对象获取星座 |
| `get_chinese_zodiac(year)` | 根据年份获取生肖 |
| `get_zodiac_name(zodiac, lang)` | 获取星座名称 |

## 星座日期表

| 星座 | 日期范围 |
|------|----------|
| Aries (白羊座) | 3.21 - 4.19 |
| Taurus (金牛座) | 4.20 - 5.20 |
| Gemini (双子座) | 5.21 - 6.20 |
| Cancer (巨蟹座) | 6.21 - 7.22 |
| Leo (狮子座) | 7.23 - 8.22 |
| Virgo (处女座) | 8.23 - 9.22 |
| Libra (天秤座) | 9.23 - 10.22 |
| Scorpio (天蝎座) | 10.23 - 11.21 |
| Sagittarius (射手座) | 11.22 - 12.21 |
| Capricorn (摩羯座) | 12.22 - 1.19 |
| Aquarius (水瓶座) | 1.20 - 2.18 |
| Pisces (双鱼座) | 2.19 - 3.20 |

---

**测试覆盖**: 56 passed