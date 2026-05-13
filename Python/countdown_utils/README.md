# Countdown Utils - 倒计时工具模块

精确的倒计时计算工具，支持多种时间单位和格式化输出。零外部依赖，仅使用 Python 标准库。

## 功能特性

- ✅ 精确倒计时计算
- ✅ 多种时间格式支持
- ✅ 丰富的格式化输出风格
- ✅ 进度条显示
- ✅ 批量倒计时管理
- ✅ 正向计时器功能
- ✅ 零外部依赖

## 快速开始

```python
from countdown_utils import Countdown, create_countdown, countdown_from_delta

# 方式1: 使用字符串日期
cd = Countdown("2026-12-31 23:59:59", name="新年倒计时")
print(cd.format())  # 输出: X天 X小时 X分钟 X秒

# 方式2: 使用 datetime 对象
from datetime import datetime, timedelta
target = datetime.now() + timedelta(days=7)
cd = create_countdown(target, name="活动开始")

# 方式3: 使用时间差
cd = countdown_from_delta(timedelta(hours=2), name="限时优惠")
```

## API 文档

### Countdown 类

主要的倒计时类。

#### 初始化

```python
Countdown(target, start=None, name=None)
```

- `target`: 目标时间（字符串或datetime对象）
- `start`: 开始时间（可选，默认当前时间）
- `name`: 倒计时名称（可选）

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `target` | datetime | 目标时间 |
| `start` | datetime | 开始时间 |
| `name` | str | 倒计时名称 |
| `remaining` | timedelta | 剩余时间 |
| `total_seconds` | float | 总剩余秒数 |
| `is_expired` | bool | 是否已过期 |
| `progress` | float | 进度（0.0-1.0） |

#### 方法

```python
# 获取时间组件
days, hours, minutes, seconds = cd.get_components()

# 格式化输出
cd.format(style="default")  # 默认: X天 X小时 X分钟 X秒
cd.format(style="compact")  # 紧凑: Xd Xh Xm Xs
cd.format(style="chinese")  # 中文: X天X小时X分钟X秒
cd.format(style="digital")  # 数字: DD:HH:MM:SS
cd.format(style="words")    # 文字: X天X小时X分钟X秒

# 进度条
cd.progress_bar(width=20, filled_char="█", empty_char="░")

# 转换为字典
data = cd.to_dict()
```

### 便捷函数

```python
from countdown_utils import (
    create_countdown,
    countdown_from_delta,
    multi_countdown,
    format_duration,
    countdown_to_next,
    days_until,
    hours_until,
    minutes_until
)

# 创建倒计时
cd = create_countdown("2026-12-31")

# 从时间差创建
cd = countdown_from_delta(timedelta(hours=2))
cd = countdown_from_delta(3600)  # 秒数

# 批量倒计时
targets = [
    ("任务A", "2026-06-01"),
    ("任务B", "2026-07-01"),
]
results = multi_countdown(targets)

# 格式化持续时间
format_duration(3661)  # "1小时 1分钟 1秒"
format_duration(3661, style="compact")  # "1h 1m 1s"

# 到下一个指定时间
cd = countdown_to_next("18:00", name="下班")

# 便捷计算
days = days_until("2026-12-31")
hours = hours_until("2026-12-31 23:59:59")
minutes = minutes_until("2026-12-31 23:59:59")
```

### CountdownTimer 类

正向计时器。

```python
from countdown_utils import CountdownTimer

timer = CountdownTimer()

# 做一些事情...
import time
time.sleep(1)

# 获取已用时间
print(timer.elapsed())           # timedelta 对象
print(timer.elapsed_seconds())  # 秒数
print(timer.elapsed_formatted())  # 格式化字符串

# 暂停/恢复
timer.pause()
timer.resume()

# 重置
timer.reset()

# 计圈
lap_time = timer.lap()
```

## 支持的日期格式

```python
"%Y-%m-%d %H:%M:%S"  # 2026-12-31 23:59:59
"%Y-%m-%d %H:%M"     # 2026-12-31 23:59
"%Y-%m-%d"           # 2026-12-31
"%Y/%m/%d %H:%M:%S"  # 2026/12/31 23:59:59
"%Y/%m/%d %H:%M"     # 2026/12/31 23:59
"%Y/%m/%d"           # 2026/12/31
"%Y年%m月%d日"        # 2026年12月31日
```

## 示例

### 项目截止日期

```python
from countdown_utils import Countdown
from datetime import datetime

deadline = datetime(2026, 6, 30, 18, 0, 0)
cd = Countdown(deadline, name="项目截止")

print(f"{cd.format(include_name=True)}")
print(f"进度: {cd.progress_bar()}")
```

### 批量事件管理

```python
from countdown_utils import multi_countdown

events = [
    ("周末", "2026-05-16"),
    ("月末", "2026-05-31 23:59:59"),
    ("新年", "2027-01-01 00:00:00"),
]

for event in multi_countdown(events):
    print(f"{event['name']}: {event['formatted']}")
```

### 下班倒计时

```python
from countdown_utils import countdown_to_next

cd = countdown_to_next("18:00", name="下班")
print(cd.format(include_name=True, style="compact"))
```

## 运行测试

```bash
python test_mod.py
```

## 运行示例

```bash
python example.py
```

## 许可证

MIT License