# Habit Chain Utils - 习惯链追踪工具

一个用于追踪习惯链的Python工具库，帮助用户实现"不要断链"的习惯养成策略。

## 功能特点

- ✅ **多种习惯频率支持**: 每日、工作日、周末、自定义星期几
- ✅ **连续天数追踪**: 计算当前连续天数和历史最长连续天数
- ✅ **完成率统计**: 总完成率、最近30天完成率
- ✅ **周进度追踪**: 查看每周各习惯的完成情况
- ✅ **日历热力图**: 可视化习惯完成情况
- ✅ **健康分数**: 综合评估习惯执行情况
- ✅ **里程碑系统**: 达成连续7天、30天、100天等里程碑
- ✅ **激励消息**: 根据完成情况给出个性化激励
- ✅ **多习惯管理**: 同时管理多个不同类型的习惯
- ✅ **数据持久化**: JSON序列化，支持保存和加载

## 零依赖

纯Python实现，无需安装任何外部库。

## 安装

直接将模块复制到项目中使用。

```python
from habit_chain_utils import HabitChain, HabitChainManager
```

## 快速开始

### 创建单个习惯

```python
from datetime import date, timedelta
from habit_chain_utils import create_daily_habit

# 创建一个每日习惯
reading = create_daily_habit("每天阅读30分钟", "#4CAF50")

# 标记今天完成
reading.complete()

# 标记过去几天完成
today = date.today()
for i in range(7):
    reading.complete(today - timedelta(days=i))

# 获取统计信息
stats = reading.get_stats()
print(f"当前连续: {stats['current_streak']} 天")
print(f"最长连续: {stats['longest_streak']} 天")
print(f"完成率: {stats['completion_rate'] * 100:.1f}%")
```

### 创建不同类型的习惯

```python
from habit_chain_utils import (
    create_daily_habit,
    create_weekday_habit,
    create_weekend_habit,
    create_custom_habit
)

# 每日习惯
daily = create_daily_habit("阅读", "#4CAF50")

# 工作日习惯 (周一到周五)
weekday = create_weekday_habit("健身", "#2196F3")

# 周末习惯 (周六周日)
weekend = create_weekend_habit("整理房间", "#FF9800")

# 自定义习惯 (周一、周三、周五)
custom = create_custom_habit("跑步", {0, 2, 4}, "#9C27B0")
```

### 使用管理器管理多个习惯

```python
from habit_chain_utils import HabitChainManager

manager = HabitChainManager()

# 添加习惯
manager.add_chain(create_daily_habit("阅读", "#4CAF50"))
manager.add_chain(create_weekday_habit("健身", "#2196F3"))

# 标记完成
manager.complete("阅读")
manager.complete("健身")

# 获取今日概览
overview = manager.get_today_overview()
print(f"今日进度: {overview['completed_today']}/{overview['habits_to_track_today']}")

# 获取排行榜
leaderboard = manager.get_leaderboard(by="current_streak")

# 获取激励消息
message = manager.get_motivational_message()
print(message)
```

## API 参考

### HabitChain 类

习惯链类，管理单个习惯的追踪。

#### 构造函数

```python
HabitChain(
    name: str,                          # 习惯名称
    frequency: HabitFrequency,          # 频率类型
    custom_days: Optional[Set[int]],    # 自定义星期几 (0=周一, 6=周日)
    start_date: Optional[date],         # 开始日期
    color: str                          # 显示颜色
)
```

#### HabitFrequency 枚举

| 值 | 说明 |
|---|---|
| `DAILY` | 每日追踪 |
| `WEEKDAYS` | 工作日 (周一到周五) |
| `WEEKENDS` | 周末 (周六周日) |
| `WEEKLY` | 每周一次 |
| `CUSTOM` | 自定义星期几 |

#### 主要方法

| 方法 | 说明 |
|---|---|
| `complete(date)` | 标记某天完成 |
| `uncomplete(date)` | 取消完成标记 |
| `is_completed(date)` | 检查是否完成 |
| `get_current_streak()` | 获取当前连续天数 |
| `get_longest_streak()` | 获取最长连续天数 |
| `get_completion_rate(days)` | 获取最近N天完成率 |
| `get_stats()` | 获取完整统计信息 |
| `get_weekly_progress()` | 获取周进度 |
| `get_calendar_heatmap()` | 获取日历热力图 |

### HabitChainManager 类

管理多个习惯链。

#### 主要方法

| 方法 | 说明 |
|---|---|
| `add_chain(chain)` | 添加习惯链 |
| `remove_chain(name)` | 移除习惯链 |
| `get_chain(name)` | 获取习惯链 |
| `complete(name, date)` | 标记某习惯完成 |
| `get_all_stats()` | 获取所有习惯统计 |
| `get_today_overview()` | 获取今日概览 |
| `get_weekly_overview()` | 获取周概览 |
| `get_leaderboard(by)` | 获取排行榜 |
| `get_motivational_message()` | 获取激励消息 |
| `find_best_chain_day()` | 找最佳补链日 |
| `to_json()` | 导出为JSON |
| `save_to_file(path)` | 保存到文件 |
| `load_from_file(path)` | 从文件加载 |

### 工具函数

```python
# 创建习惯
create_daily_habit(name, color)
create_weekday_habit(name, color)
create_weekend_habit(name, color)
create_custom_habit(name, days, color)

# 里程碑计算
calculate_streak_milestone(streak) -> Dict

# 健康分数
get_chain_health_score(chain) -> float
```

## 使用示例

### 查看习惯健康分数

```python
from habit_chain_utils import create_daily_habit, get_chain_health_score

habit = create_daily_habit("阅读")
for i in range(30):
    habit.complete(date.today() - timedelta(days=i))

score = get_chain_health_score(habit)
print(f"健康分数: {score}/100")

# 评分因素:
# - 当前连续天数 (40%)
# - 最近30天完成率 (30%)
# - 总完成率 (20%)
# - 今日是否完成 (10%)
```

### 计算里程碑

```python
from habit_chain_utils import calculate_streak_milestone

milestone = calculate_streak_milestone(25)
# 里程碑: 7天(一周)、14天(两周)、21天(三周)、30天(一个月)...
# 60天(两个月)、90天(三个月)、100天(100天)、365天(一年)...

print(f"已达成: {milestone['current_milestone']['name']}")
print(f"下一目标: {milestone['next_milestone']['name']}")
print(f"进度: {milestone['progress_to_next'] * 100:.1f}%")
```

### 生成日历热力图

```python
habit = create_daily_habit("阅读")
# ... 完成一些天

heatmap = habit.get_calendar_heatmap(year=2024, month=5)

for week in heatmap:
    for day in week:
        if day['in_month'] and day['completed']:
            print("██", end=" ")
        else:
            print("░░", end=" ")
    print()
```

### 持久化数据

```python
manager = HabitChainManager()
# ... 添加习惯

# 保存
manager.save_to_file("habits.json")

# 加载
manager = HabitChainManager.load_from_file("habits.json")
```

## 设计理念

### "不要断链"概念

本工具基于 Jerry Seinfeld 提出的习惯养成方法：每次完成习惯后，在日历上划掉那一天。目标是保持链条不断，看着连续的红叉会激励你继续下去。

### 健康分数体系

分数综合考虑多个因素：

| 因素 | 权重 | 说明 |
|---|---|---|
| 当前连续天数 | 40% | 最核心指标，每天2分，最多40分 |
| 最近30天完成率 | 30% | 短期执行情况 |
| 总完成率 | 20% | 长期坚持情况 |
| 今日是否完成 | 10% | 及时完成奖励 |

### 里程碑系统

| 连续天数 | 里程碑名称 | 符号 |
|---|---|---|
| 7 | 一周 | 🎯 |
| 14 | 两周 | 🔥 |
| 21 | 三周 | 💪 |
| 30 | 一个月 | 🏆 |
| 60 | 两个月 | ⭐ |
| 90 | 三个月 | 🌟 |
| 100 | 100天 | 💎 |
| 180 | 半年 | 👑 |
| 365 | 一年 | 🏅 |
| 500 | 500天 | 🚀 |
| 1000 | 1000天 | 🌈 |

## 测试

运行测试：

```bash
python -m pytest habit_chain_utils_test.py
```

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-05-23)

- 首次发布
- 支持多种习惯频率
- 完整的统计功能
- 周进度和日历热力图
- 健康分数和里程碑系统
- 数据持久化功能