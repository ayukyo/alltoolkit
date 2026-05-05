# clock_utils - 时钟与闹钟工具模块

提供时钟时间管理和闹钟调度功能。
零外部依赖，纯 Python 标准库实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| `Clock` | 虚拟时钟，可调整时间流速 |
| `Alarm` | 闹钟，支持一次性/周期性 |
| `AlarmManager` | 闹钟管理器，批量管理多个闹钟 |
| `Timer` | 定时器，倒计时功能 |

## 快速开始

### 虚拟时钟

```python
from clock_utils import Clock

# 创建时钟
clock = Clock()

# 获取当前时间
now = clock.now()

# 加速时间流逝（测试用）
clock.set_speed(10)  # 10倍速度
```

### 设置闹钟

```python
from clock_utils import Alarm, AlarmManager

# 创建闹钟
alarm = Alarm(time="08:00", message="起床")

# 闹钟管理器
manager = AlarmManager()
manager.add_alarm(alarm)

# 检查是否有闹钟触发
triggered = manager.check()
```

### 定时器

```python
from clock_utils import Timer

# 创建定时器
timer = Timer(duration_seconds=60)

# 开始计时
timer.start()

# 检查剩余时间
remaining = timer.remaining()

# 暂停/继续
timer.pause()
timer.resume()
```

## 测试覆盖

- **60 个单元测试，100% 通过率**
- 测试内容：
  - 时钟操作、时间流逝
  - 闹钟设置、触发检测
  - 定时器功能、暂停/继续

## 许可证

MIT License