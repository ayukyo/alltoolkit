# Nutrition Utils - 营养计算工具

一个全面的营养计算和分析工具模块，零外部依赖。

## 功能特点

- 🍎 **食物营养数据库** - 包含 70+ 种常见食物的营养数据
- 📊 **营养计算** - 热量、蛋白质、碳水化合物、脂肪、膳食纤维
- 🎯 **每日需求计算** - 基于 BMR/TDEE 的个性化营养需求
- 📈 **营养分析** - 摄入达标率、营养平衡评分
- 💡 **饮食建议** - 根据目标生成饮食建议
- 🏋️ **健身目标支持** - 减脂、维持、增肌三种目标

## 快速开始

### 基本使用

```python
from nutrition_utils.mod import *

# 搜索食物
results = search_foods('鸡')  # ['鸡胸肉', '鸡腿肉']

# 计算食物营养
item = calculate_food_nutrition('鸡胸肉', 150)
print(f"热量: {item.calories} kcal")
print(f"蛋白质: {item.protein}g")

# 计算餐饮营养
foods = [('米饭', 200), ('鸡胸肉', 150), ('西兰花', 100)]
summary = calculate_meal_nutrition(foods)
print(f"总热量: {summary.total_calories} kcal")
```

### 每日营养需求

```python
# 计算每日营养需求
needs = calculate_daily_needs(
    weight=70,      # kg
    height=175,     # cm
    age=30,
    gender=Gender.MALE,
    activity_level=ActivityLevel.MODERATE,
    goal=Goal.MAINTAIN  # 或 LOSE_WEIGHT, GAIN_MUSCLE
)

print(f"每日热量需求: {needs.calories} kcal")
print(f"蛋白质需求: {needs.protein}g")
```

### 营养分析

```python
# 分析一日饮食
daily_food = [
    ('米饭', 200), ('鸡胸肉', 150), ('西兰花', 100),
    ('三文鱼', 120), ('香蕉', 100)
]

analysis = analyze_nutrition(daily_food, needs)
print(f"热量达标率: {analysis.calories_percent}%")
print(f"营养平衡分数: {analysis.balance_score}/100")
print(f"建议: {analysis.recommendations[0]}")
```

## 主要功能

### 食物数据库

包含以下分类的常见食物：
- 主食类（米饭、面条、燕麦、红薯等）
- 肉类（鸡胸肉、牛肉、猪肉等）
- 海鲜（三文鱼、虾、鳕鱼等）
- 蛋奶类（鸡蛋、牛奶、酸奶等）
- 豆类（豆腐、豆浆、黄豆等）
- 蔬菜（西兰花、菠菜、番茄等）
- 水果（苹果、香蕉、橙子等）
- 坚果（杏仁、核桃、花生等）

### 营养计算

- 单个食物营养计算
- 多食物餐饮营养汇总
- 宏量营养素热量转换
- 营养比例分析

### 每日需求估算

基于 Mifflin-St Jeor 公式：
- 基础代谢率 (BMR) 计算
- 总每日能量消耗 (TDEE) 计算
- 根据活动水平调整
- 根据健身目标调整

### 活动水平

| 水平 | 说明 | 活动因子 |
|-----|------|---------|
| SEDENTARY | 久坐，几乎不运动 | 1.2 |
| LIGHT | 轻度活动，每周 1-3 天运动 | 1.375 |
| MODERATE | 中度活动，每周 3-5 天运动 | 1.55 |
| ACTIVE | 高度活动，每周 6-7 天运动 | 1.725 |
| VERY_ACTIVE | 非常活跃，体力劳动或每天两次训练 | 1.9 |

### 健身目标

| 目标 | 热量调整 | 宏量营养素比例 |
|-----|---------|--------------|
| LOSE_WEIGHT | -20% | 蛋白 35%, 碳水 35%, 脂肪 30% |
| MAINTAIN | 0% | 蛋白 25%, 碳水 50%, 脂肪 25% |
| GAIN_MUSCLE | +10% | 蛋白 30%, 碳水 45%, 脂肪 25% |

## API 参考

### 食物数据库函数

- `get_food_info(name)` - 获取食物营养信息
- `search_foods(keyword, limit)` - 搜索食物
- `get_foods_by_category(category)` - 按分类获取食物
- `get_all_foods()` - 获取所有食物列表
- `get_all_categories()` - 获取所有分类列表

### 营养计算函数

- `calculate_food_nutrition(name, amount)` - 计算食物营养
- `calculate_meal_nutrition(foods)` - 计算餐饮营养
- `calculate_calories_from_macros(p, c, f)` - 从宏量营养素计算热量
- `calculate_macros_from_calories(calories, ratios)` - 从热量计算宏量营养素

### 每日需求函数

- `calculate_bmr(weight, height, age, gender)` - 计算 BMR
- `calculate_tdee(bmr, activity_level)` - 计算 TDEE
- `calculate_daily_needs(...)` - 计算完整每日需求
- `calculate_protein_needs(weight, activity, goal)` - 计算蛋白质需求

### 分析函数

- `analyze_nutrition(foods, daily_needs)` - 营养分析
- `get_meal_suggestion(calories, protein)` - 生成饮食建议

### 格式化函数

- `format_nutrition_label(name, amount)` - 格式化营养标签
- `format_meal_summary(foods)` - 格式化餐饮摘要

## 数据类型

### FoodItem
```python
@dataclass
class FoodItem:
    name: str
    amount: float
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    category: str
```

### NutritionSummary
```python
@dataclass
class NutritionSummary:
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    protein_ratio: float
    carbs_ratio: float
    fat_ratio: float
    food_count: int
    food_items: List[FoodItem]
```

### DailyNeeds
```python
@dataclass
class DailyNeeds:
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    activity_level: str
    goal: str
```

## 测试

运行测试：
```bash
python nutrition_utils_test.py
```

## 示例

运行示例：
```bash
cd examples
python example_basic.py
```

## 作者

AllToolkit Contributors

## 许可证

MIT License

## 日期

2026-05-14