# Zodiac Utils - 星座计算工具

提供西方星座和中国生肖的完整计算功能，包括星座判断、特性分析、兼容性计算等。

## 功能特性

### 西方星座
- 根据日期判断星座
- 获取星座详细信息（元素、属性、守护星、幸运数字/颜色）
- 星座兼容性分析
- 按元素/属性筛选星座
- 获取最佳配对

### 中国生肖
- 根据年份判断生肖
- 干支纪年计算
- 五行属性计算
- 生肖兼容性分析
- 本命年判断
- 获取生肖详细信息

## 安装

```python
# 直接导入使用，零依赖
from zodiac_utils.mod import ZodiacUtils, ChineseZodiacUtils
```

## 快速开始

### 西方星座

```python
from zodiac_utils.mod import ZodiacUtils, Zodiac

# 根据日期获取星座
zodiac = ZodiacUtils.get_zodiac(7, 15)  # 巨蟹座
print(zodiac)  # 巨蟹座

# 从完整日期获取星座
from datetime import datetime
birth_date = datetime(1990, 7, 15)
zodiac = ZodiacUtils.get_zodiac_from_date(birth_date)
print(zodiac)  # 巨蟹座

# 获取星座详细信息
info = ZodiacUtils.get_zodiac_info(Zodiac.LEO)
print(info)
# {
#     'name': '狮子座',
#     'date_range': '7月23日 - 8月22日',
#     'element': '火象',
#     'quality': '固定宫',
#     'ruling_planet': '太阳',
#     'lucky_numbers': [1, 5],
#     'lucky_colors': ['金色', '橙色'],
#     'personality_traits': ['自信', '慷慨', '领导力', '自负'],
#     'english_name': 'Leo',
#     'symbol': '♌'
# }

# 计算星座兼容性
compat = ZodiacUtils.calculate_compatibility(Zodiac.ARIES, Zodiac.LEO)
print(f"白羊座和狮子座兼容度: {compat['score']}分 - {compat['level']}")
# 白羊座和狮子座兼容度: 95分 - 非常契合

# 获取最佳配对
matches = ZodiacUtils.get_best_matches(Zodiac.ARIES)
print(matches)  # [{'zodiac': '狮子座', 'score': 95}, ...]

# 按元素获取星座
fire_signs = ZodiacUtils.get_zodiacs_by_element("火象")
print(fire_signs)  # ['白羊座', '狮子座', '射手座']
```

### 中国生肖

```python
from zodiac_utils.mod import ChineseZodiacUtils, ChineseZodiac

# 根据年份获取生肖
zodiac = ChineseZodiacUtils.get_zodiac(1990)
print(zodiac)  # 马

# 从日期获取生肖
from datetime import datetime
birth_date = datetime(1990, 6, 15)
zodiac = ChineseZodiacUtils.get_zodiac_from_date(birth_date)
print(zodiac)  # 马

# 获取干支纪年
ganzhi = ChineseZodiacUtils.get_ganzhi(2024)
print(ganzhi)  # 甲辰

# 获取五行
wuxing = ChineseZodiacUtils.get_wuxing(2024)
print(wuxing)  # 木

# 判断本命年
zodiac, is_benming = ChineseZodiacUtils.get_benming_nian(1990)
print(f"{zodiac}, 本命年: {is_benming}")

# 获取生肖详细信息
info = ChineseZodiacUtils.get_zodiac_info(ChineseZodiac.DRAGON)
print(info)
# {
#     'name': '龙',
#     'order': 5,
#     'personality': ['自信', '勇敢', '有魅力', '理想主义'],
#     'strengths': ['有抱负', '精力充沛', '慷慨'],
#     'weaknesses': ['急躁', '傲慢'],
#     'best_matches': ['鼠', '猴', '鸡'],
#     'lucky_numbers': [1, 6, 7],
#     'lucky_colors': ['金色', '银色', '灰色']
# }

# 计算生肖兼容性
compat = ChineseZodiacUtils.calculate_compatibility(ChineseZodiac.RAT, ChineseZodiac.DRAGON)
print(f"鼠和龙兼容度: {compat['score']}分 - {compat['level']}")
# 鼠和龙兼容度: 95分 - 天作之合

# 获取生肖对应年份
years = ChineseZodiacUtils.get_zodiac_year(ChineseZodiac.DRAGON)
print(years)  # [..., 2000, 2012, 2024, 2036, ...]
```

### 便捷函数

```python
from zodiac_utils.mod import (
    get_zodiac,
    get_zodiac_from_date,
    get_chinese_zodiac,
    get_chinese_zodiac_from_date,
    calculate_zodiac_compatibility,
    calculate_chinese_zodiac_compatibility
)

# 快速获取星座
print(get_zodiac(7, 15))  # 巨蟹座
print(get_zodiac_from_date("1990-07-15"))  # 巨蟹座

# 快速获取生肖
print(get_chinese_zodiac(1990))  # 马

# 快速计算兼容性
print(calculate_zodiac_compatibility("白羊座", "狮子座"))
print(calculate_chinese_zodiac_compatibility("鼠", "龙"))
```

## API 参考

### ZodiacUtils 类

| 方法 | 描述 |
|------|------|
| `get_zodiac(month, day)` | 根据月份和日期判断星座 |
| `get_zodiac_from_date(date)` | 根据日期对象判断星座 |
| `get_zodiac_info(zodiac)` | 获取星座详细信息 |
| `get_element(zodiac)` | 获取星座元素 |
| `get_quality(zodiac)` | 获取星座属性 |
| `get_ruling_planet(zodiac)` | 获取星座守护星 |
| `get_lucky_numbers(zodiac)` | 获取幸运数字 |
| `get_lucky_colors(zodiac)` | 获取幸运颜色 |
| `get_personality_traits(zodiac)` | 获取性格特点 |
| `calculate_compatibility(z1, z2)` | 计算星座兼容性 |
| `get_all_zodiacs()` | 获取所有星座列表 |
| `get_zodiacs_by_element(element)` | 按元素获取星座 |
| `get_zodiacs_by_quality(quality)` | 按属性获取星座 |
| `get_best_matches(zodiac)` | 获取最佳配对 |

### ChineseZodiacUtils 类

| 方法 | 描述 |
|------|------|
| `get_zodiac(year)` | 根据年份判断生肖 |
| `get_zodiac_from_date(date)` | 根据日期判断生肖 |
| `get_zodiac_year(zodiac)` | 获取生肖对应年份列表 |
| `get_wuxing(year)` | 获取年份五行属性 |
| `get_benming_nian(year)` | 判断是否本命年 |
| `get_zodiac_info(zodiac)` | 获取生肖详细信息 |
| `get_all_zodiacs()` | 获取所有生肖列表 |
| `calculate_compatibility(z1, z2)` | 计算生肖兼容性 |
| `get_ganzhi(year)` | 获取干支纪年 |

### 枚举类

```python
# 星座
class Zodiac:
    ARIES = "白羊座"
    TAURUS = "金牛座"
    GEMINI = "双子座"
    CANCER = "巨蟹座"
    LEO = "狮子座"
    VIRGO = "处女座"
    LIBRA = "天秤座"
    SCORPIO = "天蝎座"
    SAGITTARIUS = "射手座"
    CAPRICORN = "摩羯座"
    AQUARIUS = "水瓶座"
    PISCES = "双鱼座"

# 生肖
class ChineseZodiac:
    RAT = "鼠"
    OX = "牛"
    TIGER = "虎"
    RABBIT = "兔"
    DRAGON = "龙"
    SNAKE = "蛇"
    HORSE = "马"
    GOAT = "羊"
    MONKEY = "猴"
    ROOSTER = "鸡"
    DOG = "狗"
    PIG = "猪"

# 元素
class Element:
    FIRE = "火象"
    EARTH = "土象"
    AIR = "风象"
    WATER = "水象"

# 属性
class Quality:
    CARDINAL = "基本宫"
    FIXED = "固定宫"
    MUTABLE = "变动宫"
```

## 测试

```bash
# 运行测试
python -m pytest zodiac_utils_test.py -v

# 或直接运行
python zodiac_utils_test.py
```

## 依赖

无外部依赖，仅使用 Python 标准库。

## 作者

AllToolkit

## 版本

1.0.0