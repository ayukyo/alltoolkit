# calorie_utils - 卡路里/热量计算工具 🍽️

完整的卡路里和热量管理工具，包含BMR计算、TDEE计算、食物热量数据库、运动消耗估算、体重目标计划和宏量营养素分配。

## ✨ 功能特性

- **BMR计算**：支持多种公式（Mifflin-St Jeor, Harris-Benedict, Katch-McArdle）
- **TDEE计算**：基于活动水平的每日总能量消耗
- **食物热量数据库**：100+常见食物，包含详细营养信息
- **运动消耗估算**：MET值方法，60+运动类型
- **体重目标计划**：减重/增重计划生成
- **宏量营养素分配**：基于目标的蛋白质/碳水/脂肪分配
- **BMI计算**：身体质量指数和分类
- **理想体重计算**：多种公式（Devine, Robinson, Miller, Hamwi）
- **饮水量建议**：基于体重和活动水平

**零依赖，仅使用Python标准库。**

## 🚀 快速开始

```python
from mod import (
    calculate_bmr_mifflin,
    calculate_tdee,
    calculate_tdee_full,
    Gender, ActivityLevel, Goal
)

# 计算BMR
bmr = calculate_bmr_mifflin(weight=70, height=175, age=30, gender=Gender.MALE)
print(f"BMR: {bmr:.1f} kcal/天")

# 计算TDEE
tdee = calculate_tdee(bmr, ActivityLevel.MODERATE)
print(f"TDEE: {tdee:.1f} kcal/天")

# 完整计算
result = calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE)
print(result)
# {'bmr': 1648.8, 'tdee': 2555.6, 'activity_multiplier': 1.55, ...}
```

## 📖 API 文档

### BMR计算

#### calculate_bmr_mifflin(weight, height, age, gender)
使用Mifflin-St Jeor公式计算BMR（最准确）

```python
bmr = calculate_bmr_mifflin(70, 175, 30, Gender.MALE)
# 男性: BMR = 10×体重 + 6.25×身高 - 5×年龄 + 5
# 女性: BMR = 10×体重 + 6.25×身高 - 5×年龄 - 161
```

#### calculate_bmr_harris_benedict(weight, height, age, gender)
使用Harris-Benedict公式计算BMR（历史公式）

```python
bmr = calculate_bmr_harris_benedict(70, 175, 30, Gender.MALE)
```

#### calculate_bmr_katch_mcardle(lean_body_mass)
使用Katch-McArdle公式（基于瘦体重）

```python
# 70kg体重，20%体脂，瘦体重=56kg
bmr = calculate_bmr_katch_mcardle(56)
# BMR = 370 + 21.6 × 瘦体重
```

#### calculate_bmr_from_body_fat(weight, body_fat_percent, gender)
从体脂率计算BMR

```python
bmr = calculate_bmr_from_body_fat(70, 20, Gender.MALE)
# 自动计算瘦体重并使用Katch-McArdle公式
```

### TDEE计算

#### calculate_tdee(bmr, activity_level)
计算每日总能量消耗

```python
tdee = calculate_tdee(1700, ActivityLevel.MODERATE)
# TDEE = BMR × 活动系数
```

**活动系数表**：
| 活动水平 | 系数 | 描述 |
|---------|-----|------|
| SEDENTARY | 1.2 | 久坐不动 |
| LIGHT | 1.375 | 每周1-3天运动 |
| MODERATE | 1.55 | 每周3-5天运动 |
| ACTIVE | 1.725 | 每周6-7天运动 |
| VERY_ACTIVE | 1.9 | 体力劳动/每天两次训练 |

#### calculate_tdee_full(weight, height, age, gender, activity_level, method)
完整TDEE计算，返回所有信息

```python
result = calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE)
# 返回: {'bmr': 1648.8, 'tdee': 2555.6, 'activity_multiplier': 1.55, 'method': 'mifflin'}
```

### 食物热量

#### get_food_info(food_key)
获取食物详细信息

```python
info = get_food_info("rice_white_cooked")
# {'name': '白米饭（熟）', 'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3}
```

#### calculate_food_calories(food_key, grams)
计算指定克数食物的热量

```python
result = calculate_food_calories("chicken_breast", 150)
print(f"热量: {result.calories} kcal")  # 247.5 kcal
print(f"蛋白质: {result.protein} g")     # 46.5 g
```

#### calculate_meal_calories(ingredients)
计算一餐总热量

```python
meal = calculate_meal_calories([
    ("rice_white_cooked", 200),   # 200g米饭
    ("chicken_breast", 150),      # 150g鸡胸肉
    ("broccoli", 100),            # 100g西兰花
])
print(f"总热量: {meal.calories} kcal")  # 541.5 kcal
```

#### search_food(keyword)
搜索食物

```python
results = search_food("chicken")
for food in results:
    print(f"{food['key']}: {food['name']}")
```

### 运动消耗

#### calculate_exercise_calories(exercise_key, weight, duration_minutes)
计算运动消耗热量

```python
# 70kg，跑步8km/h，30分钟
calories = calculate_exercise_calories("running_8kmh", 70, 30)
print(f"消耗: {calories} kcal")  # 280 kcal
# 公式: MET × 体重(kg) × 时长(小时)
```

#### calculate_custom_exercise_calories(met, weight, duration_minutes)
计算自定义MET运动

```python
# MET=10的运动，70kg，45分钟
calories = calculate_custom_exercise_calories(10, 70, 45)
# 525 kcal
```

#### search_exercise(keyword)
搜索运动

```python
results = search_exercise("running")
for exercise in results:
    print(f"{exercise['key']}: MET={exercise['met']}")
```

### 体重目标

#### calculate_weight_goal_plan(current_weight, target_weight, tdee, rate)
生成体重目标计划

```python
plan = calculate_weight_goal_plan(80, 75, 2500)
print(f"目标体重: {plan.target_weight} kg")
print(f"达成周数: {plan.weeks_to_achieve} 周")
print(f"每日热量目标: {plan.daily_calorie_target} kcal")
print(f"宏量营养素: {plan.macro_split}")
```

#### calculate_weight_loss_calories(tdee, loss_rate)
计算减重所需热量

```python
result = calculate_weight_loss_calories(2500, 0.5)  # 每周减0.5kg
print(f"每日目标: {result['daily_target']} kcal")  # 1950 kcal
print(f"每日缺口: {result['daily_deficit']} kcal")  # 550 kcal
```

#### calculate_weight_gain_calories(tdee, gain_rate)
计算增重所需热量

```python
result = calculate_weight_gain_calories(2500, 0.25)  # 每周增0.25kg
print(f"每日目标: {result['daily_target']} kcal")  # 2775 kcal
```

### 宏量营养素

#### calculate_macro_split(total_calories, goal)
计算宏量营养素分配

```python
macros = calculate_macro_split(2000, Goal.LOSE)
print(f"蛋白质: {macros['protein']} g")    # 150 g (30%)
print(f"碳水: {macros['carbs']} g")        # 200 g (40%)
print(f"脂肪: {macros['fat']} g")          # 67 g (30%)
```

**目标比例**：
| 目标 | 蛋白质 | 脂肪 | 碳水 |
|-----|-------|------|-----|
| LOSE | 30% | 30% | 40% |
| MAINTAIN | 25% | 30% | 45% |
| GAIN | 20% | 25% | 55% |

#### calculate_macro_calories(protein, carbs, fat, ...)
从宏量计算热量

```python
calories = calculate_macro_calories(100, 200, 50)
# 100×4 + 200×4 + 50×9 = 1650 kcal
```

#### calculate_macro_percentages(protein, carbs, fat)
计算宏量热量占比

```python
pct = calculate_macro_percentages(100, 200, 50)
print(f"蛋白质占比: {pct['protein_pct']}%")  # 24.2%
```

### 工具函数

#### bmi_calculate(weight, height)
计算BMI

```python
result = bmi_calculate(70, 175)
print(f"BMI: {result['bmi']}")            # 22.86
print(f"分类: {result['category_cn']}")   # 正常
print(f"健康体重范围: {result['healthy_weight_range']}")
```

**BMI分类**：
| BMI | 分类 |
|-----|------|
| <18.5 | 偏瘦 |
| 18.5-24.9 | 正常 |
| 25-29.9 | 超重 |
| 30-34.9 | 肥胖I级 |
| 35-39.9 | 肥胖II级 |
| ≥40 | 肥胖III级 |

#### ideal_body_weight(height, gender, formula)
计算理想体重

```python
result = ideal_body_weight(175, Gender.MALE)
print(f"Devine公式: {result['devine']} kg")    # 71.4 kg
print(f"平均值: {result['average']} kg")
```

#### lean_body_mass_calculate(weight, body_fat_percent)
计算瘦体重

```python
result = lean_body_mass_calculate(70, 20)
print(f"瘦体重: {result['lean_body_mass']} kg")  # 56 kg
print(f"脂肪量: {result['fat_mass']} kg")        # 14 kg
```

#### calorie_deficit_timeline(current, target, deficit)
计算减重时间线

```python
timeline = calorie_deficit_timeline(80, 75, 500)
print(f"总天数: {timeline['total_days']}")      # 77天
print(f"里程碑: {timeline['milestones']}")
```

#### daily_water_intake(weight, activity_level)
计算每日建议饮水量

```python
result = daily_water_intake(70, ActivityLevel.MODERATE)
print(f"建议饮水: {result['liters']} L")        # 2.8 L
print(f"{result['glasses_250ml']}杯 (250ml)")
```

## 📊 数据库

### 食物数据库（部分）

| 食物 | 热量(kcal/100g) | 蛋白质 | 碳水 | 脂肪 |
|-----|----------------|-------|-----|-----|
| 白米饭 | 130 | 2.7 | 28 | 0.3 |
| 鸡胸肉 | 165 | 31 | 0 | 3.6 |
| 三文鱼 | 208 | 20 | 0 | 13 |
| 西兰花 | 34 | 2.8 | 7 | 0.4 |
| 苹果 | 52 | 0.3 | 14 | 0.2 |

### MET数据库（部分）

| 运动 | MET值 | 说明 |
|-----|------|-----|
| 睡眠 | 0.9 | 最低MET |
| 慢走 | 2.0 | 散步 |
| 快走 | 4.0 | 健步走 |
| 跑步(8km/h) | 8.0 | 中速跑 |
| 跑步(10km/h) | 10.0 | 较快跑 |
| 冲刺跑 | 16.0 | 最高MET |
| 自由泳 | 10.0 | 剧烈游泳 |
| HIIT | 8.0 | 高强度间歇 |
| 力量训练 | 5.0 | 中等强度 |

## 🧪 测试

```bash
python calorie_utils_test.py
```

测试覆盖：
- BMR计算（4种公式）
- TDEE计算（5种活动水平）
- 食物热量（查询、计算、搜索）
- 运动消耗（查询、计算）
- 体重目标（减重、增重）
- 宏量营养素（分配、计算）
- BMI计算（各分类）
- 理想体重（4种公式）
- 边界值测试（极端参数）

**总计：88+ 测试用例**

## ⚠️ 注意事项

1. **BMR公式选择**：
   - Mifflin-St Jeor：最准确，适合大多数人
   - Harris-Benedict：略微高估，适合老年人
   - Katch-McArdle：适合体脂率已知、运动员

2. **减重速度**：
   - 推荐：0.5-1kg/周
   - 过快减重可能导致肌肉流失
   - 每日热量不低于1200（女性）/1500（男性）

3. **MET值使用**：
   - MET值为平均值，实际消耗因人而异
   - 运动强度和个人体能会影响实际消耗

## 📝 更新日志

### v1.0.0 (2026-05-23)
- 初始版本
- 支持BMR计算（3种公式）
- 支持TDEE计算
- 100+食物数据库
- 60+运动MET数据库
- 体重目标计划
- 宏量营养素分配
- BMI和理想体重计算
- 88+测试用例

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-23