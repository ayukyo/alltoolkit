# Pomodoro Timer Utilities - 番茄钟工具库

🍅 **专业的番茄钟时间管理工具，零外部依赖**

---

## 📋 功能特性

- **完整番茄钟周期管理** - 工作、短休息、长休息自动切换
- **灵活配置** - 自定义工作时长、休息时长、长休息间隔
- **事件回调系统** - 支持自定义事件处理
- **详细统计追踪** - 完成数、中断数、工作时间、生产力评分
- **会话历史管理** - 记录每个番茄钟会话详情
- **暂停/恢复支持** - 随时暂停和恢复计时
- **JSON 序列化** - 支持数据持久化
- **时间估算** - 计算完成目标所需时间
- **零依赖** - 仅使用 Python 标准库

---

## 🚀 快速开始

### 基本使用

```python
from pomodoro_utils.mod import PomodoroTimer

# 创建番茄钟（默认配置：25分钟工作，5分钟短休息，15分钟长休息）
timer = PomodoroTimer()

# 开始工作
timer.start_work()
print(f"状态: {timer.get_status_text()}")  # "工作中 - 剩余 24:59"

# 完成番茄钟
timer.complete_session()
print(f"今日完成: {timer.get_today_completed_count()} 个")

# 开始休息
timer.start_break()
timer.complete_session()
```

### 自定义配置

```python
# 50分钟工作，10分钟短休息，30分钟长休息，每3个番茄后长休息
timer = PomodoroTimer(
    work_minutes=50,
    short_break_minutes=10,
    long_break_minutes=30,
    long_break_interval=3,
    auto_start_break=True  # 自动开始休息
)
```

---

## 📚 API 文档

### PomodoroTimer 类

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `work_minutes` | int | 25 | 工作时长（分钟） |
| `short_break_minutes` | int | 5 | 短休息时长（分钟） |
| `long_break_minutes` | int | 15 | 长休息时长（分钟） |
| `long_break_interval` | int | 4 | 长休息间隔（完成多少番茄后） |
| `auto_start_break` | bool | False | 是否自动开始休息 |

#### 主要方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `start_work(duration=None)` | bool | 开始工作，可自定义时长 |
| `start_break(is_long=False)` | bool | 开始休息 |
| `pause()` | bool | 暂停计时 |
| `resume()` | bool | 恢复计时 |
| `complete_session()` | bool | 完成当前会话 |
| `interrupt_session(reason)` | bool | 中断当前会话 |
| `reset()` | None | 重置当前计时 |
| `reset_all()` | None | 重置所有数据 |

#### 时间追踪方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `get_elapsed_seconds()` | int | 已过秒数 |
| `get_elapsed_minutes()` | int | 已过分钟数 |
| `get_remaining_seconds()` | int | 剩余秒数 |
| `get_remaining_minutes()` | int | 剩余分钟数 |
| `get_progress_percent()` | float | 进度百分比 (0-100) |
| `is_completed()` | bool | 是否完成 |
| `get_status_text()` | str | 状态描述文本 |

#### 统计方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `get_stats()` | PomodoroStats | 获取统计信息 |
| `get_sessions(limit=0)` | List | 获取会话历史 |
| `get_today_sessions()` | List | 获取今日会话 |
| `get_today_completed_count()` | int | 今日完成番茄数 |
| `get_productivity_score()` | float | 生产力评分 (0-100) |
| `should_take_long_break()` | bool | 是否应该长休息 |
| `estimate_completion_time(target)` | datetime | 估算完成目标时间 |

#### 序列化方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `to_json()` | str | 序列化为 JSON |
| `from_json(json_str)` | PomodoroTimer | 从 JSON 反序列化 |

### 事件回调

```python
timer = PomodoroTimer()

# 注册回调
timer.on("on_start", lambda s: print("开始工作!"))
timer.on("on_complete", lambda s: print("完成!"))
timer.on("on_interrupt", lambda s: print(f"中断: {s.notes}"))
timer.on("on_break_start", lambda s: print("开始休息"))
timer.on("on_break_end", lambda s: print("休息结束"))
```

### 便捷函数

```python
from pomodoro_utils.mod import (
    create_timer, format_time, calculate_total_time,
    get_recommended_break, estimate_daily_goal
)

# 创建计时器
timer = create_timer(30, 10, 20, 3)

# 格式化时间
print(format_time(1500))  # "25:00"

# 计算总时间
total = calculate_total_time(8)  # 完成8个番茄需要的总分钟数
print(f"需要 {total} 分钟")

# 推荐休息类型
break_type = get_recommended_break(4)  # "long" 或 "short"

# 估算每日目标
goal = estimate_daily_goal(3.0)  # 3小时需要的番茄数
```

---

## 📊 统计数据结构

### PomodoroStats

```python
stats = timer.stats

# 属性
stats.total_sessions          # 总会话数
stats.completed_sessions     # 完成会话数
stats.interrupted_sessions   # 中断会话数
stats.total_work_minutes     # 总工作分钟数
stats.total_break_minutes    # 总休息分钟数
stats.daily_sessions         # 每日完成数 {日期: 数量}
```

### PomodoroSession

```python
session = timer.current_session

# 属性
session.start_time           # 开始时间
session.end_time             # 结束时间
session.state                # 状态 (TimerState)
session.duration_minutes     # 时长
session.completed            # 是否完成
session.interrupted          # 是否中断
session.notes                # 备注
```

---

## 🔄 计时器状态

| 状态 | 值 | 说明 |
|------|------|------|
| IDLE | "idle" | 空闲 |
| WORKING | "working" | 工作中 |
| SHORT_BREAK | "short_break" | 短休息 |
| LONG_BREAK | "long_break" | 长休息 |
| PAUSED | "paused" | 已暂停 |

---

## 🎯 使用场景

### 日常时间管理

```python
timer = PomodoroTimer()

# 工作循环
for session_num in range(8):
    timer.start_work()
    # 等待完成或手动完成
    timer.complete_session()
    
    if timer.should_take_long_break():
        timer.start_break(is_long=True)
    else:
        timer.start_break()
    timer.complete_session()
```

### 自定义工作时长

```python
# 深度工作模式（90分钟）
timer = PomodoroTimer(work_minutes=90, short_break_minutes=20)

# 短专注模式（15分钟）
timer = PomodoroTimer(work_minutes=15, short_break_minutes=3)
```

### 数据持久化

```python
import json

# 保存到文件
timer = PomodoroTimer()
# ... 完成一些番茄钟 ...

with open("pomodoro_data.json", "w") as f:
    f.write(timer.to_json())

# 从文件恢复
with open("pomodoro_data.json", "r") as f:
    timer = PomodoroTimer.from_json(f.read())
```

### 生产力追踪

```python
timer = PomodoroTimer()

# 一天结束后检查
print(f"今日完成: {timer.get_today_completed_count()} 个番茄")
print(f"工作时间: {timer.stats.total_work_minutes} 分钟")
print(f"生产力评分: {timer.get_productivity_score():.1f}/100")
```

---

## 📦 模块结构

```
pomodoro_utils/
├── mod.py              # 主模块
├── pomodoro_utils_test.py  # 测试文件
├── README.md           # 本文档
└── examples/
    └── usage_examples.py  # 使用示例
```

---

## 🧪 测试

```bash
python pomodoro_utils/pomodoro_utils_test.py
```

测试覆盖：
- 计时器初始化和配置
- 工作/休息会话管理
- 暂停/恢复功能
- 完成和中断处理
- 时间追踪准确性
- 统计功能
- JSON 序列化
- 事件回调
- 边界值处理

---

## 📝 示例运行

```bash
python pomodoro_utils/examples/usage_examples.py
```

---

## 🔗 相关模块

- `timer_utils` - 通用计时器
- `stopwatch_utils` - 秒表
- `clock_utils` - 时钟/闹钟
- `time_zone_utils` - 时区处理

---

## 📄 许可证

MIT License - 零依赖，自由使用

---

**最后更新**: 2026-05-12