# Blood Alcohol Utils 🍺

血液酒精浓度（BAC）计算工具模块，提供专业的酒精代谢计算和法律驾驶限制检查。

## 特性

- ✅ **Widmark 公式** - 经典 BAC 计算方法
- ✅ **Watson 公式** - 更精确的计算（考虑体液量）
- ✅ **酒精代谢时间** - 醒酒时间估算
- ✅ **各国法律限制** - 20+ 国家酒驾限制查询
- ✅ **标准饮品计算** - 多国标准饮品定义
- ✅ **饮品预设** - 啤酒、葡萄酒、烈酒等常用饮品
- ✅ **完整报告** - 饮酒会话综合分析

## 快速开始

### 创建饮品

```python
from blood_alcohol_utils import create_drink, create_drink_from_preset

# 手动创建饮品
beer = create_drink("啤酒", 355, 0.05)  # 355ml, 5% ABV
print(f"酒精含量: {beer.alcohol_grams}g")

# 使用预设
beer = create_drink_from_preset("beer_regular")
wine = create_drink_from_preset("wine_red")
cocktail = create_drink_from_preset("cocktail_margarita")
```

### Widmark 公式计算 BAC

```python
from blood_alcohol_utils import calculate_bac_widmark

# 计算 BAC
# 70kg 男性，喝了 28g 酒精，已过 1.5 小时
bac = calculate_bac_widmark(70, "male", 28, 1.5)
print(f"BAC: {bac:.3f}%")  # 约 0.029%
```

### Watson 公式计算 BAC（更精确）

```python
from blood_alcohol_utils import calculate_bac_watson

# 需要身高和年龄
bac = calculate_bac_watson(
    weight_kg=70,
    height_cm=175,
    gender="male",
    age=30,
    total_alcohol_grams=28,
    hours_elapsed=1.5
)
```

### 完整 BAC 计算

```python
from blood_alcohol_utils import calculate_bac, create_drink_from_preset

# 喝了 2 杯啤酒
drinks = [create_drink_from_preset("beer_regular") for _ in range(2)]

result = calculate_bac(
    weight_kg=70,
    gender="male",
    drinks=drinks,
    hours_elapsed=1,
    country="china"  # 使用中国法律限制
)

print(f"BAC: {result.bac:.3f}%")
print(f"是否合法驾驶: {result.is_legal}")
print(f"醒酒时间: {result.time_to_sober:.1f}小时")
print(f"等级: {result.category}")
print(f"影响程度: {result.impairment_level}")
```

### 快速 BAC 计算

```python
from blood_alcohol_utils import quick_bac

# 70kg 男性，喝了 2 杯啤酒，已过 1 小时
bac = quick_bac(70, "male", 2, "beer_regular", 1)
print(f"BAC: {bac:.3f}%")
```

### 醒酒时间估算

```python
from blood_alcohol_utils import time_to_sober, time_to_legal, suggest_waiting_time

# 完全醒酒时间
hours = time_to_sober(0.08)  # 约 5.3 小时

# 达到法定限制的时间
hours_legal = time_to_legal(0.08, 0.05)  # 约 2 小时

# 详细建议
suggestion = suggest_waiting_time(0.08)
print(f"需等待: {suggestion['human']}")
print(f"醒酒时间: {suggestion['sober_at']}")
```

### 各国法律限制

```python
from blood_alcohol_utils import get_legal_limit, LEGAL_LIMITS

# 获取各国限制
china_limit = get_legal_limit("china")   # 0.02%
us_limit = get_legal_limit("us")         # 0.08%
japan_limit = get_legal_limit("japan")   # 0.03%

# 查看所有国家
print(LEGAL_LIMITS)
```

### 计算可喝多少杯

```python
from blood_alcohol_utils import calculate_drinks_to_limit

# 70kg 男性，2小时内，保持低于 0.05%
max_drinks = calculate_drinks_to_limit(70, "male", 0.05, 2, "beer_regular")
print(f"最多可喝 {max_drinks} 杯啤酒")
```

### 饮酒会话综合报告

```python
from blood_alcohol_utils import drinking_session_summary, create_drink_from_preset

drinks = [
    create_drink_from_preset("beer_regular"),
    create_drink_from_preset("wine_red"),
]

summary = drinking_session_summary(70, "male", drinks, "china")
print(summary)
# {
#   'bac_percent': 0.029,
#   'is_legal': True,
#   'time_to_sober_hours': 1.9,
#   'recommendation': 'Legal to drive (but consider waiting)'
# }
```

### BAC 等级分类

```python
from blood_alcohol_utils import categorize_bac

category, impairment = categorize_bac(0.03)
print(f"等级: {category}")      # Slight
print(f"影响: {impairment}")    # Mild relaxation, slight impairment
```

## BAC 等级对照表

| BAC (%) | 等级 | 影响 |
|---------|------|------|
| 0.00 | Sober | 无影响 |
| 0.01-0.02 | Trace | 极轻微影响 |
| 0.02-0.05 | Slight | 轻度放松，轻微影响 |
| 0.05-0.08 | Moderate | 协调能力下降，判断力受损 |
| 0.08-0.10 | High | 显著影响，法定醉酒 |
| 0.10-0.15 | Very High | 严重影响，危险驾驶 |
| 0.15-0.20 | Severe | 严重运动障碍，困惑 |
| 0.20-0.30 | Dangerous | 严重困惑，可能昏迷 |
| >0.30 | Life-threatening | 昏迷或死亡风险 |

## 各国法律限制

| 国家 | 限制 (%) |
|------|----------|
| 中国 | 0.02 |
| 日本 | 0.03 |
| 德国 | 0.05 |
| 法国 | 0.05 |
| 英国 | 0.08 |
| 美国 | 0.08 |
| 澳大利亚 | 0.05 |
| 加拿大 | 0.08 |
| 瑞典 | 0.02 |
| 挪威 | 0.02 |

## 饮品预设

| 预设名称 | 容量 (ml) | 酒精度 (%) |
|----------|-----------|------------|
| beer_regular | 355 | 5.0 |
| beer_light | 355 | 4.2 |
| beer_craft | 355 | 7.0 |
| wine_red | 150 | 13.0 |
| wine_white | 150 | 12.0 |
| spirits_vodka | 44 | 40.0 |
| spirits_whiskey | 44 | 43.0 |
| cocktail_margarita | 150 | 13.0 |
| cocktail_martini | 100 | 30.0 |
| sake | 180 | 15.0 |
| soju | 50 | 20.0 |

## 标准饮品定义

| 国家 | 标准饮品 (g) |
|------|-------------|
| 美国 | 14.0 |
| 英国 | 8.0 |
| 澳大利亚 | 10.0 |
| 加拿大 | 13.6 |
| 日本 | 19.75 |
| WHO | 10.0 |

## BACResult 数据类

```python
class BACResult:
    bac: float              # 血液酒精浓度 (%)
    bac_permille: float     # 千分比 (‰)
    is_legal: bool          # 是否合法驾驶
    legal_limit: float      # 使用的法律限制
    time_to_sober: float    # 完全醒酒时间 (小时)
    time_to_legal: float    # 达到合法限制时间 (小时)
    metabolism_rate: float  # 代谢率
    category: str           # BAC 等级分类
    impairment_level: str   # 影响程度描述
```

## 测试

```bash
python Python/blood_alcohol_utils/blood_alcohol_utils_test.py
```

## 许可证

MIT License

## ⚠️ 重要提示

本模块仅供参考和教育目的。实际酒精代谢因人而异，受多种因素影响：
- 个人代谢率差异
- 饮食情况
- 药物影响
- 体质差异

**请勿依赖本工具判断是否可以驾驶。如有疑问，请选择不驾驶。**