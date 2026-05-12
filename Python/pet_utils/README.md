# Pet Utils 🐕🐈

**宠物工具库 - 宠物年龄转换、体重评估、喂食建议、疫苗计划等**

零依赖，生产就绪，支持多种宠物类型。

---

## ✨ 功能特性

- **年龄转换** - 狗/猫/兔子等宠物年龄转换为人类等效年龄
- **体重评估** - 根据品种评估宠物体重状态，给出 BCS 评分
- **喂食建议** - 计算每日热量需求、食物量、喂食时间表
- **疫苗计划** - 自动生成疫苗接种时间表
- **运动需求** - 根据体型、年龄、活动水平计算运动需求
- **寿命预测** - 基于多种因素预测宠物预期寿命
- **健康检查** - 根据生命阶段提供健康检查建议

---

## 🚀 快速开始

### 基础用法

```python
from pet_utils import dog_age_to_human, cat_age_to_human, evaluate_pet_weight

# 狗年龄转换
human_age = dog_age_to_human(5, 'medium')  # 42岁人类
human_age = dog_age_to_human(5, 'toy')     # 36岁人类
human_age = dog_age_to_human(5, 'large')   # 45岁人类

# 猫年龄转换
human_age = cat_age_to_human(1)   # 15岁
human_age = cat_age_to_human(2)   # 24岁
human_age = cat_age_to_human(10)  # 56岁

# 体重评估
result = evaluate_pet_weight(8.0, 'dog', 'beagle')
print(result['status_cn'])  # 理想体重
print(result['bcs'])        # 5 (体况评分)
```

### 喂食建议

```python
from pet_utils import get_feeding_plan

# 获取喂食计划
plan = get_feeding_plan('dog', 15.0, age_years=3, 
                        is_neutered=False, activity='moderate',
                        food_type='dry_food')

print(f"每日热量: {plan['daily_calories']} kcal")
print(f"每日食物量: {plan['daily_amount_grams']} g")
print(f"喂食次数: {plan['meals_per_day']} 次/天")
print(f"喂食时间: {plan['feeding_times']}")
```

### 疫苗计划

```python
from pet_utils import get_vaccine_schedule

# 获取疫苗时间表
schedule = get_vaccine_schedule('dog', '2026-01-01')

for item in schedule:
    print(f"日期: {item['due_date']}")
    for vaccine in item['vaccines']:
        print(f"  - {vaccine['name_cn']}: {vaccine['code']}")
```

### 运动需求

```python
from pet_utils import get_exercise_needs

# 获取运动建议
needs = get_exercise_needs('dog', size='medium', 
                           activity='high', age_years=3)

print(f"运动时间: {needs['min_minutes']}-{needs['max_minutes']} 分钟/天")
print(f"运动类型: {needs['exercise_type']}")
print(f"建议: {needs['suggestions']}")
```

### 寿命预测

```python
from pet_utils import predict_pet_lifespan

# 预测寿命
lifespan = predict_pet_lifespan('dog', size='medium',
                                is_neutered=True, is_obese=False,
                                has_regular_exercise=True, quality_diet=True)

print(f"预期寿命: {lifespan['min_years']}-{lifespan['max_years']} 年")
print(f"影响因素: {lifespan['adjustments']}")
```

---

## 📚 API 参考

### 年龄转换

#### `dog_age_to_human(dog_years, size)`
将狗的年龄转换为人类等效年龄。

**参数:**
- `dog_years` (float): 狗的年龄（年）
- `size` (str): 狗的体型 - `'toy'`, `'small'`, `'medium'`, `'large'`, `'giant'`

**返回:** `float` - 人类等效年龄

**示例:**
```python
>>> dog_age_to_human(5, 'medium')
42.0
```

#### `cat_age_to_human(cat_years)`
将猫的年龄转换为人类等效年龄。

**参数:**
- `cat_years` (float): 猫的年龄（年）

**返回:** `float` - 人类等效年龄

**示例:**
```python
>>> cat_age_to_human(2)
24.0
```

#### `pet_age_to_human(pet_years, pet_type, size)`
通用宠物年龄转换函数。

**参数:**
- `pet_years` (float): 宠物年龄
- `pet_type` (str): 宠物类型 - `'dog'`, `'cat'`, `'rabbit'`, `'hamster'`, `'guinea_pig'`, `'bird'`, `'fish'`, `'turtle'`, `'ferret'`, `'chinchilla'`
- `size` (str): 体型（仅狗需要）

**返回:** `float` - 人类等效年龄

---

### 体重评估

#### `evaluate_pet_weight(weight, pet_type, breed)`
评估宠物体重状态。

**参数:**
- `weight` (float): 体重（kg）
- `pet_type` (str): 宠物类型 - `'dog'` 或 `'cat'`
- `breed` (str): 品种名称（可选）

**返回:** `dict` - 包含以下字段:
- `weight`: 当前体重
- `ideal_min`: 理想体重最小值
- `ideal_max`: 理想体重最大值
- `status`: 状态 - `'underweight'`, `'ideal'`, `'overweight'`, `'obese'`
- `status_cn`: 状态中文描述
- `bcs`: 体况评分 (1-9)
- `recommendations`: 建议

**示例:**
```python
>>> evaluate_pet_weight(8.0, 'dog', 'beagle')
{
    'weight': 8.0,
    'ideal_min': 9.1,
    'ideal_max': 11.3,
    'status': 'underweight',
    'status_cn': '体重过轻',
    'bcs': 4,
    'recommendations': ['增加喂食频率...', '...']
}
```

---

### 喂食建议

#### `get_feeding_plan(pet_type, weight, age_years, is_neutered, activity, food_type)`
获取喂食计划。

**参数:**
- `pet_type` (str): 宠物类型
- `weight` (float): 体重（kg）
- `age_years` (float): 年龄
- `is_neutered` (bool): 是否绝育
- `activity` (str): 活动水平 - `'low'`, `'moderate'`, `'high'`, `'very_high'`
- `food_type` (str): 食物类型 - `'dry_food'`, `'wet_food'`, `'semi_moist'`, `'raw_food'`

**返回:** `dict` - 包含热量、食物量、喂食时间等

---

### 疫苗计划

#### `get_vaccine_schedule(pet_type, birth_date_str)`
获取疫苗时间表。

**参数:**
- `pet_type` (str): 宠物类型 - `'dog'` 或 `'cat'`
- `birth_date_str` (str): 出生日期 (YYYY-MM-DD)

**返回:** `list` - 疫苗接种计划列表

---

### 运动需求

#### `get_exercise_needs(pet_type, size, activity, age_years)`
获取运动需求建议。

**参数:**
- `pet_type` (str): 宠物类型
- `size` (str): 体型（仅狗需要）
- `activity` (str): 活动水平
- `age_years` (float): 年龄

**返回:** `dict` - 运动时间、类型、建议

---

### 寿命预测

#### `predict_pet_lifespan(pet_type, size, is_neutered, is_obese, has_regular_exercise, quality_diet)`
预测宠物预期寿命。

**参数:**
- `pet_type` (str): 宠物类型
- `size` (str): 体型
- `is_neutered` (bool): 是否绝育
- `is_obese` (bool): 是否肥胖
- `has_regular_exercise` (bool): 是否规律运动
- `quality_diet` (bool): 是否优质饮食

**返回:** `dict` - 包含预期寿命范围和影响因素

---

## 🐕 狗年龄转换规则

| 体型 | 第一年 | 第二年 | 后续每年 |
|------|--------|--------|----------|
| 玩具型 | 15岁 | 9岁 | 4岁 |
| 小型 | 15岁 | 9岁 | 5岁 |
| 中型 | 15岁 | 9岁 | 6岁 |
| 大型 | 15岁 | 9岁 | 7岁 |
| 巨型 | 12岁 | 10岁 | 8岁 |

**示例计算:**
- 5岁玩具型狗: 15 + 9 + (3 × 4) = 36岁人类
- 5岁中型狗: 15 + 9 + (3 × 6) = 42岁人类
- 5岁巨型狗: 12 + 10 + (3 × 8) = 46岁人类

---

## 🐈 猫年龄转换规则

| 猫年龄 | 人类年龄 |
|--------|----------|
| 0-1岁 | 0-15岁 (按比例) |
| 1-2岁 | 15-24岁 |
| 2岁以上 | 24 + 4 × (猫年龄-2) |

**示例:**
- 1岁猫 = 15岁人类
- 2岁猫 = 24岁人类
- 5岁猫 = 24 + 12 = 36岁人类
- 10岁猫 = 24 + 32 = 56岁人类

---

## 📊 体重状态分类

| 状态 | BCS评分 | 相对于理想体重 |
|------|---------|----------------|
| 过轻 | 1-4 | < 85% |
| 理想 | 5 | 85%-105% |
| 超重 | 6 | 105%-115% |
| 肥胖 | 7-9 | > 115% |

---

## 📋 疫苗计划

### 狗疫苗

| 年龄 | 疫苗 |
|------|------|
| 6周龄 | DHPPi + Corona |
| 9周龄 | DHPPi + Corona |
| 12周龄 | DHPPi + Rabies |
| 16周龄 | DHPPi |
| 12月龄 | DHPPi + Rabies (加强) |
| 15月龄 | Kennel Cough |

### 猫疫苗

| 年龄 | 疫苗 |
|------|------|
| 6周龄 | FVRCP |
| 9周龄 | FVRCP |
| 12周龄 | FVRCP + Rabies |
| 16周龄 | FVRCP |
| 12月龄 | FVRCP + Rabies (加强) |

---

## 🏃 运动需求参考

### 狗运动需求

| 体型 | 最少 | 最多 | 运动类型 |
|------|------|------|----------|
| 玩具型 | 20分钟 | 30分钟 | 轻度散步和室内游戏 |
| 小型 | 30分钟 | 45分钟 | 敛步和轻度游戏 |
| 中型 | 45分钟 | 60分钟 | 敛步、跑步和互动游戏 |
| 大型 | 60分钟 | 90分钟 | 长距离散步和跑步 |
| 巨型 | 45分钟 | 60分钟 | 适度运动，避免关节负担 |

### 特殊情况调整

- **幼犬**: 运动时间减少50%，避免剧烈运动
- **老年犬**: 运动时间减少30%，避免跳跃
- **高活动水平**: 增加30%运动时间
- **低活动水平**: 减少30%运动时间

---

## 📈 寿命预测参考

### 基础寿命范围

| 宠物类型 | 体型 | 寿命范围 |
|----------|------|----------|
| 狗 | 玩具型 | 12-16年 |
| 狗 | 小型 | 10-15年 |
| 狗 | 中型 | 10-14年 |
| 狗 | 大型 | 8-12年 |
| 狗 | 巨型 | 6-10年 |
| 猫 | 室内 | 14-20年 |
| 猫 | 室外 | 8-14年 |
| 兔子 | - | 8-12年 |
| 仓鼠 | - | 2-3年 |
| 乌龟 | - | 20-40年 |

### 影响因素

- **绝育**: 延长寿命1.5-2年
- **肥胖**: 缩短寿命2年
- **规律运动**: 延长寿命1年
- **优质饮食**: 延长寿命1年

---

## 🧪 测试

```bash
python pet_utils_test.py
```

**测试覆盖:**
- 年龄转换 (10+ 测试)
- 体重评估 (15+ 测试)
- 喂食计算 (15+ 测试)
- 疫苗计划 (15+ 测试)
- 运动需求 (15+ 测试)
- 寿命预测 (15+ 测试)
- 健康检查 (15+ 测试)
- 边界情况 (10+ 测试)

---

## 📝 版本历史

### v1.0.0 (2026-05-12)
- 初始版本
- 支持10种宠物类型
- 狗按5种体型分类
- 完整的年龄转换、体重评估、喂食建议功能
- 疫苗计划、运动需求、寿命预测
- 健康检查建议

---

## 📄 许可证

MIT License

---

## 👤 作者

AllToolkit 自动化生成

---

**让宠物健康管理更简单！** 🐾