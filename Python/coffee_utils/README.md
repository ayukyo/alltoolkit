# Coffee Utils - 咖啡冲泡工具库

一个功能完整的咖啡冲泡计算和分析工具库，零外部依赖。

## 功能特性

### 🔢 咖啡计算器
- **比例计算**: 咖啡粉与水的比例计算
- **萃取率计算**: 根据TDS计算萃取率
- **金杯标准检查**: 检验是否符合SCAA金杯标准
- **闷蒸参数**: 闷蒸水量和时间建议

### ☕ 冲泡推荐
支持12种冲泡方式的参数推荐：
- 滴滤 (Drip)
- 法压壶 (French Press)
- 意式浓缩 (Espresso)
- 手冲 (Pour Over)
- 冷萃 (Cold Brew)
- 爱乐压 (Aeropress)
- 摩卡壶 (Moka Pot)
- 虹吸壶 (Siphon)
- 土耳其咖啡 (Turkish)
- Chemex
- V60
- Kalita Wave

### 📊 研磨度指南
7种研磨粗细详细说明：
- 极细 (Extra Fine) - 土耳其咖啡
- 细 (Fine) - 浓缩咖啡
- 中细 (Medium Fine) - 手冲
- 中等 (Medium) - 滴滤
- 中粗 (Medium Coarse) - Chemex
- 粗 (Coarse) - 法压壶、冷萃
- 极粗 (Extra Coarse) - 特殊冲泡

### 🔥 烘焙程度分析
6种烘焙程度特性：
- 浅烘 (Light)
- 中浅烘 (Light Medium)
- 中烘 (Medium)
- 中深烘 (Medium Dark)
- 深烘 (Dark)
- 极深烘 (Very Dark)

### 🌍 产地信息
14个主要咖啡产地的详细信息：
- 埃塞俄比亚、肯尼亚、哥伦比亚、巴西
- 危地马拉、哥斯达黎加、苏门答腊、也门
- 牙买加(蓝山)、夏威夷(科纳)、巴拿马
- 印度尼西亚、越南、印度

### 💊 咖啡因计算
- 基于冲泡方式的咖啡因估算
- 每日摄入限制检查
- 咖啡因半衰期计算

### 💧 水质分析
- 水硬度评估
- pH值分析
- 镁含量影响评估

## 安装使用

```python
from coffee_utils.mod import (
    CoffeeCalculator, CaffeineCalculator, BrewRecommender,
    WaterQualityAnalyzer, RoastAnalyzer, OriginInfo,
    BrewMethod, GrindSize, RoastLevel, CoffeeOrigin,
)

# 或使用便捷函数
from coffee_utils.mod import (
    calculate_ratio, estimate_caffeine, get_brew_recipe,
    golden_cup_check, search_coffee_by_flavor,
)
```

## 使用示例

### 1. 计算咖啡比例

```python
from coffee_utils.mod import CoffeeCalculator

# 计算比例
ratio = CoffeeCalculator.calculate_ratio(15, 225)
print(ratio)  # "1:15.0"

# 根据水量计算所需咖啡粉
coffee_g = CoffeeCalculator.calculate_coffee_for_water(300, "1:15")
print(f"需要 {coffee_g}g 咖啡粉")  # 需要 20.0g 咖啡粉

# 根据咖啡量计算所需水量
water_ml = CoffeeCalculator.calculate_water_for_coffee(18, "1:2")
print(f"需要 {water_ml}ml 水")  # 需要 36.0ml 水
```

### 2. 金杯标准检查

```python
from coffee_utils.mod import CoffeeCalculator

# 计算萃取率
extraction = CoffeeCalculator.calculate_extraction_yield(
    coffee_g=15, 
    water_ml=225, 
    tds_percent=1.25
)
print(f"萃取率: {extraction}%")  # 萃取率: 18.75%

# 检查金杯标准
result = CoffeeCalculator.is_golden_cup(19.0, 1.25)
print(result["is_golden_cup"])  # True
print(result["suggestions"])     # ["完美！您的咖啡符合金杯标准"]
```

### 3. 获取冲泡参数

```python
from coffee_utils.mod import BrewRecommender, BrewMethod

# 获取V60冲泡参数
params = BrewRecommender.get_brew_parameters(BrewMethod.V60)
print(f"研磨度: {params.grind_size.value}")
print(f"比例: {params.ratio}")
print(f"温度: {params.temperature_c}°C")
print(f"时间: {params.brew_time_seconds}秒")

# 获取多杯配方
recipe = BrewRecommender.recommend_for_cups(BrewMethod.POUR_OVER, cups=2)
print(f"总咖啡粉: {recipe['total_coffee_g']}g")
print(f"总水量: {recipe['total_water_ml']}ml")

# 根据口味调整
stronger = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "stronger")
weaker = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "weaker")
```

### 4. 研磨度指南

```python
from coffee_utils.mod import BrewRecommender, GrindSize

# 获取研磨度详情
rec = BrewRecommender.get_grind_recommendation(GrindSize.MEDIUM_FINE)
print(f"描述: {rec.description}")        # 中细，砂糖状质地
print(f"粒径: {rec.particle_size_um}μm") # (300, 500)
print(f"目数: {rec.mesh_size}")           # (140, 200)
```

### 5. 咖啡因估算

```python
from coffee_utils.mod import CaffeineCalculator, BrewMethod, RoastLevel

# 估算咖啡因
info = CaffeineCalculator.estimate_caffeine(
    coffee_g=15,
    brew_method=BrewMethod.POUR_OVER,
    roast_level=RoastLevel.MEDIUM
)
print(f"每杯咖啡因: {info.mg_per_cup}mg")
print(f"敏感度等级: {info.sensitivity_level}")

# 每日限制检查
check = CaffeineCalculator.daily_limit_check(250, limit_mg=400)
print(f"剩余可摄入: {check['remaining_mg']}mg")
print(f"浓缩咖啡剩余杯数: {check['cups_remaining']['espresso']}")

# 半衰期计算
hours = CaffeineCalculator.half_life_hours(200, 50, 5.0)
print(f"从200mg降到50mg需要 {hours} 小时")
```

### 6. 烘焙程度分析

```python
from coffee_utils.mod import RoastAnalyzer, RoastLevel

# 获取烘焙特性
chars = RoastAnalyzer.get_roast_characteristics(RoastLevel.LIGHT)
print(f"颜色: {chars['color']}")
print(f"风味: {chars['flavor']}")
print(f"酸度: {chars['acidity']}")
print(f"醇厚度: {chars['body']}")

# 推荐冲泡温度
temp = RoastAnalyzer.recommend_brew_temp(RoastLevel.LIGHT)
print(f"推荐温度: {temp[0]}-{temp[1]}°C")

# 根据烘焙推荐产地
origins = RoastAnalyzer.suggest_origin_for_roast(RoastLevel.LIGHT)
for origin in origins:
    print(origin.value)
```

### 7. 产地信息查询

```python
from coffee_utils.mod import OriginInfo, CoffeeOrigin

# 获取产地信息
info = OriginInfo.get_origin_info(CoffeeOrigin.ETHIOPIA)
print(f"产地: {info.name}")
print(f"海拔: {info.altitude_range[0]}-{info.altitude_range[1]}m")
print(f"风味: {', '.join(info.flavor_notes)}")
print(f"酸度: {info.acidity}")
print(f"醇厚度: {info.body}")

# 按风味搜索
origins = OriginInfo.search_by_flavor("巧克力")
for origin in origins:
    print(CoffeeOrigin(origin).value)

# 按酸度搜索
high_acidity = OriginInfo.search_by_acidity("high")

# 按醇厚度搜索
full_body = OriginInfo.search_by_body("full")
```

### 8. 水质分析

```python
from coffee_utils.mod import WaterQualityAnalyzer

# 评估水质
result = WaterQualityAnalyzer.assess_water(
    hardness_ppm=100,
    ph=7.0,
    alkalinity_ppm=50
)
print(f"硬度状态: {result['hardness']['status']}")
print(f"pH状态: {result['ph']['status']}")
print(f"整体评估: {result['overall']}")

# 镁含量评估
mg_result = WaterQualityAnalyzer.magnesium_benefit(30)
print(f"镁含量: {mg_result['magnesium_level']}")
print(f"影响: {mg_result['effect']}")
```

### 9. 使用便捷函数

```python
from coffee_utils.mod import (
    calculate_ratio, estimate_caffeine, get_brew_recipe,
    golden_cup_check, search_coffee_by_flavor,
)

# 快速计算比例
ratio = calculate_ratio(15, 225)  # "1:15.0"

# 快速估算咖啡因
info = estimate_caffeine(15, "pour_over")

# 快速获取配方
recipe = get_brew_recipe("v60", cups=2)

# 快速金杯检查
result = golden_cup_check(15, 225, 1.25)

# 快速风味搜索
origins = search_coffee_by_flavor("花香")
```

## 支持的冲泡方式

| 方式 | 比例 | 研磨度 | 水温(°C) | 时间(秒) |
|------|------|--------|----------|----------|
| 浓缩 | 1:2 | 细 | 90-96 | 25-30 |
| V60 | 1:15 | 中细 | 91-96 | 150-210 |
| Chemex | 1:16 | 中粗 | 90-96 | 240-300 |
| 法压壶 | 1:15 | 粗 | 93-96 | 240-360 |
| 冷萃 | 1:8 | 粗 | 0-25 | 12-24h |
| 爱乐压 | 1:16 | 中细 | 80-90 | 60-180 |
| 摩卡壶 | 1:10 | 中细 | 95-100 | 300-420 |
| 滴滤 | 1:16 | 中 | 90-96 | 300-420 |

## 金杯标准

根据SCAA(美国精品咖啡协会)金杯标准：
- **萃取率**: 18-22%
- **TDS(溶解性总固体)**: 1.15-1.35%

## 许可证

MIT License