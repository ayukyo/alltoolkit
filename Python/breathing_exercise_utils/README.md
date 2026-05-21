# Breathing Exercise Utils

呼吸训练工具，提供多种呼吸模式的计时和指导。

## 功能特性

- **多种呼吸模式**: 4-7-8、Box、深呼吸等
- **可视化指导**: 步骤提示和计时
- **音频提示**: 可选的音频信号
- **统计数据**: 练习记录和统计
- **自定义模式**: 创建自定义呼吸模式

## 快速开始

```python
from breathing_exercise_utils.mod import BreathingExercise, BreathingPattern

# 4-7-8 放松呼吸法
pattern = BreathingPattern.FOUR_SEVEN_EIGHT
exercise = BreathingExercise(pattern)

# 开始练习
exercise.start()
# 输出: 吸气 4 秒... 屏息 7 秒... 呼气 8 秒...
```

## 使用示例

### 预定义模式

```python
from breathing_exercise_utils.mod import BreathingPattern

# 4-7-8 放松呼吸法（吸气4秒-屏息7秒-呼气8秒）
pattern_478 = BreathingPattern.FOUR_SEVEN_EIGHT

# Box 呼吸法（吸气4秒-屏息4秒-呼气4秒-屏息4秒）
pattern_box = BreathingPattern.BOX

# 深呼吸（吸气6秒-呼气6秒）
pattern_deep = BreathingPattern.DEEP_BREATHING

# 激活呼吸（快速吸气-短屏息-长呼气）
pattern_energizing = BreathingPattern.ENERGIZING

# 放松呼吸（短吸-长呼）
pattern_relaxing = BreathingPattern.RELAXING
```

### 练习指导

```python
from breathing_exercise_utils.mod import BreathingExercise

exercise = BreathingExercise(
    pattern=BreathingPattern.BOX,
    cycles=4,       # 4 个循环
    show_timer=True # 显示计时
)

# 开始练习
exercise.start()

# 获取步骤指导
steps = exercise.get_steps()
for step in steps:
    print(f"{step.phase}: {step.duration} 秒")
```

### 自定义模式

```python
from breathing_exercise_utils.mod import CustomBreathingPattern, BreathingPhase

# 创建自定义模式
custom = CustomBreathingPattern(
    phases=[
        BreathingPhase.INHALE,      # 吸气
        BreathingPhase.HOLD,        # 屏息
        BreathingPhase.EXHALE,      # 呼气
        BreathingPhase.HOLD_EMPTY,  # 空（呼气后屏息）
    ],
    durations=[4, 4, 4, 4],  # 各阶段时长
    name="自定义呼吸法"
)

exercise = BreathingExercise(custom)
```

### 练习统计

```python
from breathing_exercise_utils.mod import PracticeSession

session = PracticeSession()

# 记录练习
session.record_practice(
    pattern="4-7-8",
    cycles=4,
    duration_minutes=3
)

# 统计
stats = session.get_stats()
print(f"总练习次数: {stats['total_sessions']}")
print(f"总练习时间: {stats['total_minutes']} 分钟")
print(f"最常用模式: {stats['favorite_pattern']}")
```

### 可视化输出

```python
from breathing_exercise_utils.mod import BreathingVisualizer

visualizer = BreathingVisualizer()

# 运行并可视化
visualizer.run(
    pattern=BreathingPattern.BOX,
    cycles=4,
    style="text"  # 文本模式
)

# 其他可视化风格
# style="emoji" - emoji 模式
# style="simple" - 简洁模式
```

## 预定义模式

| 模式 | 吸气 | 屏息 | 呼气 | 空 | 说明 |
|------|------|------|------|-----|------|
| 4-7-8 | 4秒 | 7秒 | 8秒 | - | 放松/助眠 |
| Box | 4秒 | 4秒 | 4秒 | 4秒 | 平衡/冥想 |
| 深呼吸 | 6秒 | - | 6秒 | - | 基础放松 |
| Energizing | 2秒 | 1秒 | 6秒 | - | 提神/激活 |
| Relaxing | 4秒 | - | 8秒 | - | 深度放松 |
| Wim Hof | 1秒 | - | 1秒 | 15秒 | 激活/增强 |

## API 参考

### BreathingExercise

| 方法 | 说明 |
|------|------|
| `start()` | 开始练习 |
| `get_steps()` | 获取步骤列表 |
| `get_current_phase()` | 当前阶段 |
| `get_remaining_time()` | 剩余时间 |

### BreathingPattern

| 模式 | 说明 |
|------|------|
| FOUR_SEVEN_EIGHT | 4-7-8 放松法 |
| BOX | Box 呼吸法 |
| DEEP_BREATHING | 深呼吸 |
| ENERGIZING | 激活呼吸 |
| RELAXING | 放松呼吸 |
| WIM_HOF | Wim Hof 方法 |

### CustomBreathingPattern

```python
CustomBreathingPattern(
    phases=[...],      # 呼吸阶段列表
    durations=[...],   # 各阶段时长
    name="自定义"
)
```

### PracticeSession

| 方法 | 说明 |
|------|------|
| `record_practice(pattern, cycles, duration)` | 记录练习 |
| `get_stats()` | 获取统计 |
| `get_history()` | 获取历史 |

## 呼吸阶段

| 阶段 | 说明 |
|------|------|
| INHALE | 吸气 |
| HOLD | 屏息（吸气后） |
| EXHALE | 呼气 |
| HOLD_EMPTY | 空（呼气后屏息） |

---

**测试覆盖**: 完整测试套件，覆盖各呼吸模式、计时、统计等