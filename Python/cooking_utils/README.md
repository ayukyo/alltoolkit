# Cooking Utils

烹饪工具模块，提供烹饪相关的实用功能。

## 特性

- **温度转换** - 摄氏/华氏互转，常见烘焙温度参考
- **重量转换** - 克/盎司/磅/千克互转
- **容积转换** - 毫升/杯/茶匙/汤匙等互转
- **烘焙计算** - 时间估算、预热时间
- **食物保存** - 冷藏冷冻时间指南
- **食材替代** - 烘焙食材替代建议
- **烹饪术语** - 中文烹饪术语词典
- **火候控制** - 火候等级和菜肴推荐
- **食谱缩放** - 按人数调整用量
- **零外部依赖** - 纯 Python 标准库实现

## 快速开始

### 温度转换

```python
from cooking_utils import celsius_to_fahrenheit, fahrenheit_to_celsius

celsius_to_fahrenheit(180)  # 356°F
fahrenheit_to_celsius(350)  # 177°C

# 常见温度参考
get_common_temperatures()
# {"水沸腾": (100, 212), "中温烘烤": (175, 350), ...}
```

### 重量转换

```python
from cooking_utils import grams_to_ounces, pounds_to_grams

grams_to_ounces(500)  # 17.64盎司
pounds_to_grams(2)    # 907.2克

# 综合转换
convert_weight(1000, WeightUnit.GRAM, WeightUnit.POUND)  # 2.2磅
```

### 容积转换

```python
from cooking_utils import cups_to_milliliters, teaspoons_to_milliliters

cups_to_milliliters(1)       # 240毫升
teaspoons_to_milliliters(3)  # 15毫升（相当于1汤匙）
```

### 烘焙计算

```python
from cooking_utils import calculate_baking_time, get_oven_preheat_time

# 烘焙蛋糕
info = calculate_baking_time(180, TemperatureUnit.CELSIUS, "蛋糕")
# {"min_time_minutes": 25, "max_time_minutes": 35, ...}

# 预热时间
get_oven_preheat_time(180)  # 10分钟
```

### 食物保存指南

```python
from cooking_utils import get_food_storage_info

get_food_storage_info("鸡蛋")
# {"冷藏": "3-5周", "冷冻": "不推荐", "注意事项": "原包装保存，不要清洗"}
```

### 食材替代

```python
from cooking_utils import get_ingredient_substitutes

get_ingredient_substitutes("鸡蛋")
# [{"替代": "亚麻籽粉+水", "比例": "1大勺亚麻籽粉+3大勺水=1个鸡蛋", ...}]
```

### 烹饪术语

```python
from cooking_utils import get_cooking_term_definition

get_cooking_term_definition("焯水")
# {"术语": "焯水", "定义": "将食材放入沸水中短时间加热..."}
```

### 火候控制

```python
from cooking_utils import recommend_heat_level, get_heat_level_guide

recommend_heat_level("炒菜")
# {"火候": "大火或中火", "说明": "快速翻炒保持食材脆嫩"}

get_heat_level_guide()
# {"大火": {"温度": "200-300°C", "适用": "爆炒、煎炸"}, ...}
```

### 食谱缩放

```python
from cooking_utils import recipe_scale

# 2人份转4人份
recipe_scale(200, 2, 4)  # 400

# 4人份转2人份  
recipe_scale(200, 4, 2)  # 100
```

### 米水比例

```python
from cooking_utils import calculate_cooking_water_ratio

calculate_cooking_water_ratio("普通米")
# {"比例": 1.5, "说明": "水是米的1.5倍"}
```

### 快速转换

```python
from cooking_utils import quick_convert

quick_convert(180, "temperature", "celsius", "fahrenheit")  # 356
quick_convert(500, "weight", "gram", "ounce")  # 17.64
```

## API 参考

### 温度

| 函数 | 描述 |
|------|------|
| `celsius_to_fahrenheit(c)` | 摄氏转华氏 |
| `fahrenheit_to_celsius(f)` | 华氏转摄氏 |
| `get_common_temperatures()` | 常见烹饪温度 |

### 重量

| 函数 | 描述 |
|------|------|
| `grams_to_ounces(g)` | 克转盎司 |
| `ounces_to_grams(o)` | 盎司转克 |
| `grams_to_pounds(g)` | 克转磅 |
| `pounds_to_grams(p)` | 磅转克 |
| `convert_weight(value, from, to)` | 综合重量转换 |

### 容积

| 函数 | 描述 |
|------|------|
| `cups_to_milliliters(cups)` | 杯转毫升 |
| `milliliters_to_cups(ml)` | 毫升转杯 |
| `tablespoons_to_milliliters(tbsp)` | 汤匙转毫升 |
| `teaspoons_to_milliliters(tsp)` | 茶匙转毫升 |
| `convert_volume(value, from, to)` | 综合容积转换 |

### 烘焙

| 函数 | 描述 |
|------|------|
| `calculate_baking_time(temp, unit, food)` | 烘焙时间计算 |
| `get_oven_preheat_time(temp)` | 预热时间 |

### 其他

| 函数 | 描述 |
|------|------|
| `get_food_storage_info(food)` | 食物保存信息 |
| `get_ingredient_substitutes(ingredient)` | 食材替代建议 |
| `get_cooking_term_definition(term)` | 烹饪术语定义 |
| `recommend_heat_level(dish)` | 火候推荐 |
| `recipe_scale(amount, old_servings, new_servings)` | 食谱缩放 |
| `calculate_cooking_water_ratio(rice_type)` | 米水比例 |

## 使用场景

1. **烘焙食谱** - 温度转换、时间估算
2. **国际化烹饪** - 单位转换（中式/西式）
3. **食材替换** - 特殊饮食需求替代方案
4. **食物管理** - 保存时间参考
5. **烹饪学习** - 术语解释、火候指南

## 测试

```bash
python cooking_utils_test.py
```

## 许可证

MIT