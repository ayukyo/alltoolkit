# BAC Utils (Blood Alcohol Content Calculator)

血液酒精含量计算器，基于 Widmark 公式，零外部依赖。

## 功能特性

- **BAC 计算**: Widmark 公式精确计算
- **时间估算**: 清醒时间、合法驾驶时间
- **损伤评估**: 7 级损伤程度评估
- **各国限值**: 25+ 国家法定驾驶限值
- **饮料追踪**: 支持带时间戳的饮料记录
- **代谢计算**: 个性化代谢率支持

## 快速开始

```python
from bac_utils.mod import calculate_bac, Gender, format_bac

# 计算啤酒后的 BAC
bac = calculate_bac(
    weight_kg=70,           # 体重 70kg
    gender=Gender.MALE,     # 男性
    alcohol_grams=40,       # 40g 酒精（约 3 瓶啤酒）
    hours_since_first_drink=2  # 2 小时后
)

print(f"BAC: {format_bac(bac)}")  # 0.042%
```

## 使用示例

### 基础计算

```python
from bac_utils.mod import calculate_bac, calculate_bac_result, Gender

# 计算 BAC
bac = calculate_bac(70, Gender.MALE, 40, 2)

# 获取完整结果
result = calculate_bac_result(70, Gender.MALE, 40, 2, country_code="CN")
print(f"BAC: {result.bac}%")
print(f"损伤程度: {result.impairment.value}")
print(f"清醒时间: {result.time_to_sober} 小时")
print(f"能否驾驶: {result.is_legal_to_drive}")
```

### 饮料对象

```python
from bac_utils.mod import Drink, calculate_bac_from_drinks, Gender
from datetime import datetime, timedelta

now = datetime.now()
drinks = [
    Drink.from_beer(500, 5.0, "大瓶啤酒", now - timedelta(hours=3)),
    Drink.from_wine(150, 12.0, "红酒", now - timedelta(hours=1.5)),
    Drink.from_spirit(45, 40.0, "威士忌", now - timedelta(minutes=30)),
]

bac = calculate_bac_from_drinks(80, Gender.MALE, drinks, now)
```

### 便捷函数

```python
# 啤酒 BAC 计算
bac = beer_bac(70, Gender.MALE, beer_count=3, hours=2)

# 红酒 BAC 计算
bac = wine_bac(60, Gender.FEMALE, glass_count=2, hours=1.5)

# 烈酒 BAC 计算
bac = spirit_bac(75, Gender.MALE, shot_count=4, hours=3)
```

### 损伤程度评估

```python
from bac_utils.mod import get_impairment_level, ImpairmentLevel

level, description = get_impairment_level(0.08)
print(f"程度: {level.value}")  # moderate
print(description)  # 详细描述
```

| BAC 范围 | 损伤程度 | 说明 |
|----------|----------|------|
| 0.00-0.02 | sober | 清醒状态 |
| 0.02-0.05 | mild | 轻度损伤 |
| 0.05-0.10 | moderate | 中度损伤 |
| 0.10-0.15 | significant | 显著损伤 |
| 0.15-0.20 | severe | 严重损伤 |
| 0.20-0.30 | dangerous | 危险水平 |
| 0.30+ | life_threatening | 危及生命 |

### 各国法定限值

```python
from bac_utils.mod import get_legal_limit, LEGAL_LIMITS, list_zero_tolerance_countries

# 获取中国法定限值
limit = get_legal_limit('CN')  # 0.02%

# 获取所有国家限值
print(LEGAL_LIMITS)  # {'CN': 0.02, 'US': 0.08, 'UK': 0.08, ...}

# 零容忍国家
print(list_zero_tolerance_countries())  # ['BR', 'CZ', 'HU']
```

| 国家 | 法定限值 | 说明 |
|------|----------|------|
| CN (中国) | 0.02% | 严格限制 |
| US (美国) | 0.08% | 大多数州 |
| UK (英国) | 0.08% | |
| DE (德国) | 0.05% | |
| JP (日本) | 0.03% | |
| BR (巴西) | 0.00% | 零容忍 |
| CZ (捷克) | 0.00% | 零容忍 |

### 时间估算

```python
from bac_utils.mod import time_to_sober, time_to_legal_limit, format_time_hours

# 清醒所需时间
hours = time_to_sober(0.08)
print(f"清醒时间: {format_time_hours(hours)}")  # 5 hours 20 min

# 达到法定驾驶限值时间
hours = time_to_legal_limit(0.10, country_code='CN')
print(f"可驾驶时间: {format_time_hours(hours)}")
```

### 警告信息

```python
from bac_utils.mod import get_bac_warning

warnings = get_bac_warning(0.15)
for w in warnings:
    print(w)
# ⚠️ ILLEGAL TO DRIVE: You are above the legal limit...
# ⚠️ HIGH IMPAIRMENT: Risk of blackout...
```

### 预估饮酒量

```python
from bac_utils.mod import calculate_drinks_by_bac

# 达到目标 BAC 需要多少标准饮料
drinks = calculate_drinks_by_bac(
    target_bac=0.05,
    weight_kg=70,
    gender=Gender.MALE,
    hours=2
)
print(f"需要约 {drinks:.1f} 标准饮料")
```

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `calculate_bac(weight, gender, alcohol, hours)` | 计算 BAC |
| `calculate_bac_result(...)` | 完整结果 |
| `calculate_bac_from_drinks(weight, gender, drinks)` | 从饮料列表计算 |
| `get_impairment_level(bac)` | 损伤程度评估 |
| `time_to_sober(bac)` | 清醒时间 |
| `time_to_legal_limit(bac, country)` | 合法驾驶时间 |

### Drink 类

```python
Drink.from_standard(name, units=1.0)      # 标准饮料（10g 酒精）
Drink.from_beer(volume_ml, abv=5.0)       # 啤酒
Drink.from_wine(volume_ml, abv=12.0)      # 红酒
Drink.from_spirit(volume_ml, abv=40.0)    # 烈酒
```

### BACResult 类

```python
@dataclass
class BACResult:
    bac: float               # BAC 百分比
    impairment: ImpairmentLevel
    description: str         # 损伤描述
    time_to_sober: float     # 清醒时间（小时）
    time_to_drive: float     # 合法驾驶时间（小时）
    is_legal_to_drive: bool
    confidence: str          # 估算置信度
```

### 便捷函数

| 函数 | 说明 |
|------|------|
| `beer_bac(weight, gender, count, hours)` | 啤酒 BAC |
| `wine_bac(weight, gender, count, hours)` | 红酒 BAC |
| `spirit_bac(weight, gender, count, hours)` | 烈酒 BAC |
| `estimate_alcohol_content(volume, abv)` | 酒精含量计算 |
| `format_bac(bac)` | 格式化 BAC |
| `format_time_hours(hours)` | 格式化时间 |

## Widmark 公式

```
BAC = (酒精克数 / (体重克数 × r)) × 100 - (代谢率 × 小时)

其中:
- r = 0.68 (男性) 或 0.55 (女性)
- 代谢率 ≈ 0.015% / 小时（平均值）
```

## 注意事项

⚠️ **重要提示**:
- BAC 计算为估算值，实际值受个体差异影响
- 代谢率因人而异（0.01-0.02%/小时）
- **切勿依赖此计算判断能否安全驾驶**
- 饮酒后请勿驾驶

---

**测试覆盖**: 完整测试套件，覆盖 Widmark 公式、饮料计算、损伤评估、各国限值等