# Water Intake Utils - 饮水量追踪工具 🚰

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

智能饮水追踪工具，根据体重、活动水平、气候等条件计算每日建议饮水量，支持饮水记录管理、时间表生成、习惯分析等功能。

## ✨ 特性

- 🧮 **智能计算** - 根据体重、活动水平、气候、年龄、孕期/哺乳状态计算每日建议饮水量
- 📊 **追踪管理** - 记录饮水历史，支持多种饮品类型
- ⏰ **时间表生成** - 自动生成每日饮水时间表
- 📈 **统计分析** - 每日/周汇总、完成率统计、目标达成率
- 🔔 **智能提醒** - 基于时间和目标的饮水提醒
- 💾 **数据持久化** - JSON 序列化支持
- 🌡️ **气候适应** - 支持 5 种气候类型的调整系数
- 🏃 **活动适配** - 支持 5 种活动水平的调整系数
- 🤰 **特殊状态** - 支持怀孕和哺乳期的额外需求
- 🍵 **多种饮品** - 支持 8 种饮品类型，自动计算有效水量
- 🚫 **零依赖** - 仅使用 Python 标准库

## 📦 安装

```python
from water_intake_utils.mod import (
    WaterIntakeCalculator,
    WaterTracker,
    DrinkReminder,
    ActivityLevel,
    Climate,
    DrinkType,
)
```

## 🚀 快速开始

### 1. 计算每日建议饮水量

```python
from water_intake_utils.mod import WaterIntakeCalculator, ActivityLevel, Climate

# 创建计算器
calculator = WaterIntakeCalculator(
    weight_kg=70,
    activity_level=ActivityLevel.MODERATE,
    climate=Climate.MILD,
)

# 获取每日建议饮水量
target = calculator.calculate_daily_target()
print(f"每日建议饮水量: {target}ml")  # 输出: 2500ml

# 获取饮水建议
recommendations = calculator.get_recommendations()
for rec in recommendations:
    print(f"- {rec}")
```

### 2. 追踪饮水量

```python
from water_intake_utils.mod import WaterTracker, DrinkType

# 创建追踪器
tracker = WaterTracker(calculator)

# 添加饮水记录
tracker.add_drink(250, DrinkType.WATER, note="起床第一杯")
tracker.add_drink(200, DrinkType.COFFEE)  # 咖啡因有轻微利尿作用
tracker.add_drink(300, DrinkType.TEA)
tracker.add_drink(500, DrinkType.WATER)

# 获取今日状态
status = tracker.get_hydration_status()
print(f"今日饮水: {status.current_ml}ml / {status.target_ml}ml")
print(f"完成率: {status.completion_rate * 100:.1f}%")
print(f"状态: {status.status_text}")
```

### 3. 生成饮水时间表

```python
from datetime import time

# 获取饮水时间表
schedule = calculator.get_drink_schedule(
    start_time=time(8, 0),
    end_time=time(22, 0),
    interval_minutes=120,
    drink_size_ml=250,
)

for drink_time, amount in schedule:
    print(f"{drink_time.strftime('%H:%M')} - 饮水 {amount}ml")
```

### 4. 统计分析

```python
# 获取每日汇总
summary = tracker.get_daily_summary()
print(f"日期: {summary.date}")
print(f"总饮水量: {summary.total_ml}ml")
print(f"有效水量: {summary.effective_ml}ml")
print(f"完成率: {summary.completion_rate * 100:.1f}%")
print(f"是否达标: {'是' if summary.is_goal_met else '否'}")

# 获取周汇总
weekly = tracker.get_weekly_summary()
for day in weekly:
    print(f"{day.date}: {day.effective_ml}ml ({day.completion_rate * 100:.0f}%)")

# 获取统计数据
stats = tracker.get_statistics(days=7)
print(f"平均饮水量: {stats['average_ml']:.0f}ml")
print(f"平均完成率: {stats['average_completion_rate'] * 100:.1f}%")
print(f"目标达成天数: {stats['days_goal_met']}/{stats['days_tracked']}")
```

### 5. 饮水提醒

```python
from water_intake_utils.mod import DrinkReminder
from datetime import time

# 创建提醒器
reminder = DrinkReminder(
    tracker=tracker,
    interval_minutes=60,
    start_time=time(7, 0),
    end_time=time(22, 0),
)

# 检查是否需要提醒
message = reminder.check_reminder()
if message:
    print(message)  # 例如: "💧 该喝水啦！今日还差 1200ml 达标"

# 获取下次提醒时间
next_time = reminder.get_next_reminder_time()
print(f"下次提醒: {next_time}")

# 获取今日剩余提醒次数
remaining = reminder.get_remaining_reminders_today()
print(f"今日还需提醒 {remaining} 次")
```

### 6. 数据持久化

```python
# 导出为 JSON
json_data = tracker.to_json()

# 从 JSON 导入
restored = WaterTracker.from_json(json_data)
```

## 📚 API 文档

### WaterIntakeCalculator

饮水量计算器，根据个人情况计算每日建议饮水量。

#### 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `weight_kg` | float | - | 体重（公斤） |
| `activity_level` | ActivityLevel | MODERATE | 活动水平 |
| `climate` | Climate | MILD | 气候类型 |
| `age` | int, optional | None | 年龄 |
| `is_pregnant` | bool | False | 是否怀孕 |
| `is_breastfeeding` | bool | False | 是否哺乳 |

#### 活动水平 (ActivityLevel)

| 值 | 描述 | 调整系数 |
|----|------|----------|
| SEDENTARY | 久坐不动 | 1.0 |
| LIGHT | 轻度活动 | 1.1 |
| MODERATE | 中度活动 | 1.2 |
| ACTIVE | 活跃 | 1.3 |
| VERY_ACTIVE | 非常活跃 | 1.4 |

#### 气候类型 (Climate)

| 值 | 描述 | 调整系数 |
|----|------|----------|
| COLD | 寒冷 (< 10°C) | 0.9 |
| MILD | 温和 (10-20°C) | 1.0 |
| WARM | 温暖 (20-25°C) | 1.1 |
| HOT | 炎热 (25-30°C) | 1.2 |
| VERY_HOT | 酷热 (> 30°C) | 1.3 |

#### 方法

- `calculate_daily_target()` - 计算每日建议饮水量（毫升）
- `get_drink_schedule(start_time, end_time, interval_minutes, drink_size_ml)` - 生成饮水时间表
- `get_recommendations()` - 获取饮水建议

### WaterTracker

饮水追踪器，管理饮水记录和统计。

#### 方法

- `add_drink(amount_ml, drink_type, timestamp, note)` - 添加饮水记录
- `get_today_records()` - 获取今日记录
- `get_records_by_date(date)` - 获取指定日期记录
- `get_total_today()` - 获取今日有效饮水量
- `get_hydration_status()` - 获取当前水分状态
- `get_daily_summary(date)` - 获取每日汇总
- `get_weekly_summary()` - 获取本周汇总
- `get_statistics(days)` - 获取统计数据
- `clear_today()` - 清空今日记录
- `to_json()` - 导出为 JSON
- `from_json(json_str)` - 从 JSON 导入

### DrinkType

饮品类型枚举。

| 值 | 描述 | 有效水量系数 |
|----|------|--------------|
| WATER | 纯净水 | 1.0 |
| SPARKLING_WATER | 气泡水 | 1.0 |
| TEA | 茶 | 0.95 |
| COFFEE | 咖啡 | 0.85 |
| JUICE | 果汁 | 0.9 |
| SPORTS_DRINK | 运动饮料 | 1.0 |
| MILK | 牛奶 | 0.9 |
| SOUP | 汤 | 0.85 |

### DrinkReminder

饮水提醒器。

#### 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `tracker` | WaterTracker | - | 饮水追踪器 |
| `interval_minutes` | int | 60 | 提醒间隔（分钟） |
| `start_time` | time | 07:00 | 开始时间 |
| `end_time` | time | 22:00 | 结束时间 |

#### 方法

- `check_reminder()` - 检查是否需要提醒
- `get_next_reminder_time()` - 获取下次提醒时间
- `get_remaining_reminders_today()` - 获取今日剩余提醒次数

### 便捷函数

```python
# 快速计算每日建议饮水量
from water_intake_utils.mod import calculate_water_needs

target = calculate_water_needs(
    weight_kg=70,
    activity_level="moderate",
    climate="hot",
    age=30,
)
```

```python
# 格式化水量显示
from water_intake_utils.mod import format_water_amount

print(format_water_amount(1500))  # "1.5L"
print(format_water_amount(250))   # "250ml"
```

```python
# 获取饮水进度条
from water_intake_utils.mod import get_water_percentage

print(get_water_percentage(1500, 2000))
# "[💧💧💧💧💧💧💧💧⬜⬜⬜⬜] 75%"
```

## 📊 计算公式

### 基础公式

```
每日建议饮水量 = 体重(kg) × 30ml × 活动系数 × 气候系数 + 特殊状态调整
```

### 特殊状态调整

- 老年人（>65岁）：总水量 × 0.9
- 青少年（<18岁）：总水量 × 0.85
- 怀孕：+300ml
- 哺乳：+700ml

### 有效水量

不同饮品的补水效果不同，咖啡和茶有轻微利尿作用：

```
有效水量 = 实际饮用量 × 饮品系数
```

## 🧪 测试

```bash
python water_intake_utils_test.py
```

## 📝 示例场景

### 场景 1: 办公室工作者

```python
calculator = WaterIntakeCalculator(
    weight_kg=65,
    activity_level=ActivityLevel.SEDENTARY,
    climate=Climate.MILD,  # 空调环境
)
# 建议饮水量: 1950ml
```

### 场景 2: 户外运动爱好者

```python
calculator = WaterIntakeCalculator(
    weight_kg=75,
    activity_level=ActivityLevel.VERY_ACTIVE,
    climate=Climate.HOT,  # 夏季户外
)
# 建议饮水量: 3780ml
```

### 场景 3: 哺乳期妈妈

```python
calculator = WaterIntakeCalculator(
    weight_kg=58,
    activity_level=ActivityLevel.LIGHT,
    climate=Climate.MILD,
    is_breastfeeding=True,
)
# 建议饮水量: 2620ml
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 本工具提供的饮水量建议仅供参考，实际饮水需求因人而异，如有健康问题请咨询医生。