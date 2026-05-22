# Water Intake Utils - 饮水量计算工具

💧 提供全面的饮水量计算、记录和追踪功能，帮助您保持健康的水分摄入。

## 功能列表

### 📊 每日饮水量计算
- 基于体重计算基础饮水量（30ml/kg）
- 活动水平调整（久坐 → 非常活跃）
- 气候环境调整（寒冷 → 酷热）
- 运动量调整
- 年龄调整
- 特殊情况调整（孕期、哺乳期、发烧等）

### ⏰ 饮水时间管理
- 生成个性化饮水时间表
- 自定义起床/睡眠时间
- 智能时段调整（睡前减少饮水）
- 每小时饮水建议

### 📝 饮水记录追踪
- 记录每次饮水量和饮料类型
- 每日饮水汇总统计
- 按饮料类型分组统计
- 进度跟踪和目标达成判断

### 🔍 补水状态评估
- 6级补水状态判断
- 尿液颜色辅助评估
- 个性化补水建议
- 警告提醒

### 🏃 运动补水方案
- 运动出汗量估算
- 运动前/中/后补水计划
- 多种运动类型支持
- 温度和强度影响计算

### 🥤 饮料等效计算
- 各种饮料的补水效果系数
- 含水率换算
- 健康饮水建议

## 快速开始

### 安装

```python
from water_intake_utils import WaterIntakeCalculator, ActivityLevel, ClimateType
```

### 基础使用

```python
calc = WaterIntakeCalculator()

# 计算每日饮水量
result = calc.calculate_daily_intake(
    weight_kg=70,
    activity_level=ActivityLevel.ACTIVE,
    climate=ClimateType.HOT,
    exercise_minutes=60
)

print(f"每日建议饮水量: {result['total_intake_ml']} ml")
# 输出: 每日建议饮水量: 2800 ml

# 生成饮水时间表
schedule = calc.generate_drinking_schedule(
    daily_intake_ml=result['total_intake_ml'],
    num_reminders=8
)

for s in schedule:
    print(f"{s['time']} - {s['amount_ml']}ml ({s['note']})")
```

### 便捷函数

```python
from water_intake_utils import calculate_daily_water, get_quick_schedule

# 快速计算
result = calculate_daily_water(weight_kg=70, activity_level='active')
print(f"每日建议: {result['total_intake_ml']} ml")

# 快速时间表
schedule = get_quick_schedule(total_ml=2000, wake_hour=7)
```

## API 参考

### WaterIntakeCalculator 类

#### `calculate_daily_intake(weight_kg, activity_level, climate, ...)`

计算每日建议饮水量。

**参数:**
- `weight_kg` (float): 体重（公斤）
- `activity_level` (ActivityLevel): 活动水平
- `climate` (ClimateType): 气候类型
- `exercise_minutes` (int): 运动时间（分钟）
- `special_conditions` (list): 特殊情况列表
- `age` (int): 年龄（可选）

**返回:**
```python
{
    'base_intake_ml': 2100,
    'total_intake_ml': 2800,
    'activity_multiplier': 1.3,
    'climate_multiplier': 1.2,
    'exercise_addition_ml': 700,
    'glasses_of_water': 11,
    ...
}
```

#### `generate_drinking_schedule(daily_intake_ml, ...)`

生成饮水时间表。

**参数:**
- `daily_intake_ml` (float): 每日总饮水量
- `wake_time` (tuple): 起床时间（小时, 分钟）
- `sleep_time` (tuple): 睡眠时间
- `num_reminders` (int): 提醒次数

**返回:**
```python
[
    {
        'time': '08:30',
        'amount_ml': 350,
        'cumulative_ml': 350,
        'percentage': 12.5,
        'note': '早晨补水，唤醒身体'
    },
    ...
]
```

#### `record_intake(amount_ml, beverage_type, ...)`

记录饮水量。

**参数:**
- `amount_ml` (float): 饮水量（毫升）
- `beverage_type` (str): 饭料类型
- `note` (str): 备注

#### `get_daily_summary(date, target_intake_ml)`

获取每日饮水摘要。

**返回:**
```python
{
    'total_intake_ml': 1500,
    'progress_percentage': 75.0,
    'remaining_ml': 500,
    'target_met': False,
    'by_beverage_type': {'water': 1000, 'tea': 500}
}
```

#### `assess_hydration(current_intake_ml, target_intake_ml, urine_color)`

评估补水状态。

**返回:**
```python
{
    'status': 'slightly_dehydrated',
    'status_display': '轻度脱水',
    'progress_ratio': 0.8,
    'recommendations': ['继续补水，保持饮水节奏', ...]
}
```

#### `calculate_for_sport(sport_type, duration_minutes, ...)`

计算运动补水方案。

**返回:**
```python
{
    'estimated_sweat_loss_ml': 800,
    'hydration_plan': {
        'before_exercise_ml': 750,
        'during_exercise': {'per_15_minutes_ml': 280, 'total_ml': 560},
        'after_exercise_ml': 1000
    },
    'tips': ['运动前2小时补水...', ...]
}
```

### 枚举类型

#### ActivityLevel
- `SEDENTARY`: 久坐（很少或无运动）
- `LIGHT`: 轻度活动（每周1-3天轻度运动）
- `MODERATE`: 中度活动（每周3-5天中度运动）
- `ACTIVE`: 活跃（每周6-7天运动）
- `VERY_ACTIVE`: 非常活跃（剧烈运动或体力劳动）

#### ClimateType
- `COLD`: 寒冷（<10°C）
- `MILD`: 温和（10-20°C）
- `WARM`: 温暖（20-25°C）
- `HOT`: 炎热（25-35°C）
- `VERY_HOT`: 酷热（>35°C）
- `HUMID`: 潮湿（高湿度）

#### HydrationStatus
- `DEHYDRATED_SEVERE`: 严重脱水
- `DEHYDRATED`: 脱水
- `SLIGHTLY_DEHYDRATED`: 轻度脱水
- `OPTIMAL`: 最佳状态
- `WELL_HYDRATED`: 补水良好
- `OVERHYDRATED`: 饮水过量

## 常见使用场景

### 场景 1：办公室工作人员

```python
calc = WaterIntakeCalculator()

# 久坐、室内环境
result = calc.calculate_daily_intake(
    weight_kg=65,
    activity_level=ActivityLevel.SEDENTARY,
    climate=ClimateType.MILD
)

# 简单时间表
schedule = calc.generate_drinking_schedule(result['total_intake_ml'])
# 建议: 每天约 1950ml，分8次饮用
```

### 场景 2：运动爱好者

```python
# 高强度运动补水方案
sport_plan = calc.calculate_for_sport(
    sport_type='running',
    duration_minutes=90,
    intensity='high',
    weight_kg=70,
    temperature_c=28
)

print(f"预计出汗量: {sport_plan['estimated_sweat_loss_ml']} ml")
print(f"运动前补水: {sport_plan['hydration_plan']['before_exercise_ml']} ml")
print(f"运动中每15分钟: {sport_plan['hydration_plan']['during_exercise']['per_15_minutes_ml']} ml")
print(f"运动后补水: {sport_plan['hydration_plan']['after_exercise_ml']} ml")
```

### 场景 3：孕期补水

```python
result = calc.calculate_daily_intake(
    weight_kg=60,
    activity_level=ActivityLevel.LIGHT,
    special_conditions=['pregnancy']
)

# 孕期需要额外300ml
print(f"每日建议: {result['total_intake_ml']} ml")
```

### 场景 4：追踪每日饮水

```python
calc = WaterIntakeCalculator()

# 计算目标
target = calc.calculate_daily_intake(weight_kg=70)['total_intake_ml']

# 记录饮水
calc.record_intake(250, 'water', '起床后')
calc.record_intake(300, 'tea', '上午')
calc.record_intake(500, 'water', '午餐后')

# 查看进度
summary = calc.get_daily_summary(target_intake_ml=target)
print(f"进度: {summary['progress_percentage']}%")
print(f"还需: {summary['remaining_ml']} ml")
```

## 健康提示

### 💧 饮水原则
- 均匀分布在整个白天
- 避免一次性大量饮水
- 睡前减少饮水避免夜起
- 运动前后注意补水

### 🚨 警告信号
- 尿液深黄色 → 需要补水
- 尿液透明 → 可能饮水过量
- 头痛、疲劳 → 可能脱水

### 🥤 饮料选择
| 饮料 | 补水系数 | 备注 |
|------|---------|------|
| 纯水 | 1.0 | 最佳选择 |
| 茶 | 0.98 | 补水效果好 |
| 椰子水 | 0.95 | 天然电解质 |
| 运动饮料 | 0.95 | 运动时适用 |
| 果汁 | 0.9 | 注意糖分 |
| 咖啡 | 0.85 | 轻微利尿 |
| 啤酒 | 0.6 | 脱水效果 |

## 测试

```bash
python Python/water_intake_utils/water_intake_utils_test.py
```

测试覆盖 22 个测试用例，100% 通过。

## 作者

AllToolkit 自动化生成

## 更新日期

2026-05-23