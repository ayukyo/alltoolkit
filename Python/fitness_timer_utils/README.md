# fitness_timer_utils -健身计时器工具模块

综合健身计时器模块，支持多种训练方式。零外部依赖，纯 Python 标准库实现。

## 支持的训练类型

| 类型 | 说明 | 典型参数 |
|------|------|----------|
| **HIIT** | 高强度间歇训练 | 可自定义工作和休息时间 |
| **Tabata** | 20秒工作 / 10秒休息 | 标准 8 轮 |
| **EMOM** | 每分钟执行 | 指定动作数量 |
| **AMRAP** | 尽可能多轮数 | 指定总时间 |
| **Circuit** | 循环训练 | 多个动作循环 |
| **Countdown** | 倒计时器 | 指定总时长 |
| **Stopwatch** | 秒表 | 计时功能 |

## 快速使用

```python
from fitness_timer_utils.mod import (
    HIITTimer,
    TabataTimer,
    EMOMTimer,
    AMRAPTimer,
    CircuitTimer,
    CountdownTimer,
    Stopwatch,
    format_time,
    parse_time,
    create_interval_timer
)

# HIIT 训练
hiit = HIITTimer(
    work_seconds=30,      # 工作30秒
    rest_seconds=10,      # 休息10秒
    rounds=8              # 8轮
)
result = hiit.run()
print(f"总时长: {format_time(result.total_duration_seconds)}")

# Tabata 训练（标准）
tabata = TabataTimer()
result = tabata.run()  # 20s 工作, 10s 休息, 8轮

# EMOM 训练
emom = EMOMTimer(
    duration_minutes=10,  # 10分钟
    reps_per_minute=5     # 每分钟5个动作
)

# AMRAP 训练
amrap = AMRAPTimer(
    duration_minutes=20   # 20分钟内尽可能多轮
)

# 循环训练
circuit = CircuitTimer(
    exercises=["俯卧撑", "深蹲", "平板支撑"],
    work_seconds=45,
    rest_seconds=15,
    rounds=3
)

# 倒计时
countdown = CountdownTimer(seconds=300)  # 5分钟

# 秒表
stopwatch = Stopwatch()
stopwatch.start()
# ... 执行动作 ...
stopwatch.stop()
print(f"用时: {stopwatch.elapsed_seconds}秒")
```

## 详细示例

### HIIT训练（带回调）

```python
from fitness_timer_utils.mod import HIITTimer, TimerEvent

def on_tick(event: TimerEvent):
    print(f"阶段: {event.phase_name}, 剩余: {event.remaining_seconds}s")

def on_phase_change(event: TimerEvent):
    print(f"切换到: {event.phase_name}")

hiit = HIITTimer(work_seconds=30, rest_seconds=10, rounds=8)
hiit.set_callbacks(on_tick=on_tick, on_phase_change=on_phase_change)
result = hiit.run()
```

### 自定义训练

```python
from fitness_timer_utils.mod import create_interval_timer

# 创建自定义间歇训练
timer = create_interval_timer(
    intervals=[
        (30, "高强度"),   # 30秒高强度
        (15, "休息"),     # 15秒休息
        (45, "中强度"),   # 45秒中强度
        (20, "休息"),     # 20秒休息
    ],
    rounds=4
)
result = timer.run()
```

### 卡路里计算

```python
from fitness_timer_utils.mod import calculate_calories_burned, get_met_value

# 获取运动 MET 值
met = get_met_value("running")  # 跑步 MET ≈ 7.0

# 计算消耗卡路里
calories = calculate_calories_burned(
    met_value=7.0,
    duration_minutes=30,
    weight_kg=70
)
print(f"消耗约{calories} 千卡")
```

## API 参考

### HIITTimer

| 参数 | 类型 | 说明 |
|------|------|------|
| `work_seconds` | int | 工作时长（秒） |
| `rest_seconds` | int | 休息时长（秒） |
| `rounds` | int | 轮数 |
| `prepare_seconds` | int | 准备时间（秒） |

### TabataTimer

标准 Tabata 参数：20s 工作 / 10s 休息 / 8 轮

### EMOMTimer

| 参数 | 类型 | 说明 |
|------|------|------|
| `duration_minutes` | int | 总时长（分钟） |
| `reps_per_minute` | int | 每分钟动作数 |

### AMRAPTimer

| 参数 | 类型 | 说明 |
|------|------|------|
| `duration_minutes` | int | 总时长（分钟） |

### CircuitTimer

| 参数 | 类型 | 说明 |
|------|------|------|
| `exercises` | List[str] | 动作列表 |
| `work_seconds` | int | 每个动作时长 |
| `rest_seconds` | int | 动作间休息时长 |
| `rounds` | int | 循环轮数 |

### 辅助函数

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `format_time(seconds)` | int | str | 格式化时间 (MM:SS) |
| `parse_time(time_str)` | str | int | 解析时间字符串 |
| `calculate_calories_burned(met, duration, weight)` | float, int, float | float | 计算消耗卡路里 |
| `get_met_value(activity)` | str | float | 获取活动 MET 值 |

## 测试

运行测试：

```bash
python fitness_timer_utils/fitness_timer_utils_test.py
```

---

**最后更新**: 2026-05-11