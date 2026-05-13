# Countdown Utils - 倒计时工具 ⏱️

提供精确的倒计时计算功能，支持多种时间单位和格式化输出。零外部依赖，仅使用 Python 标准库。

## 功能特性

- ✅ 精确倒计时 - 计算到目标时间的精确剩余时间
- ✅ 多种时间单位 - 天、时、分、秒
- ✅ 多种格式输出 - 默认、紧凑、中文、数字、词语格式
- ✅ 进度计算 - 计算从开始到目标的进度百分比
- ✅ 进度条显示 - 可自定义字符和宽度
- ✅ 多种日期格式 - 支持多种日期字符串解析
- ✅ 批量倒计时 - 同时管理多个倒计时
- ✅ 计时器功能 - 正向计时，支持暂停、恢复、圈数
- ✅ 便捷函数 - 天数、小时、分钟快速计算

## 快速开始

### 基本用法

```python
from countdown_utils import Countdown
from datetime import datetime, timedelta

# 创建倒计时
target = datetime.now() + timedelta(days=7)
cd = Countdown(target, name="活动开始")

# 格式化输出
print(cd.format())  # "7天 XX小时 XX分钟 XX秒"

# 检查状态
if cd.is_expired:
    print("已结束")

# 获取剩余秒数
seconds = cd.total_seconds

# 获取时间组件
days, hours, minutes, seconds = cd.get_components()
```

### 多种格式

```python
cd = Countdown(target, name="倒计时")

# 默认格式: "XX天 XX小时 XX分钟 XX秒"
print(cd.format())

# 紧凑格式: "7d 3h 30m 45s"
print(cd.format(style="compact"))

# 中文格式: "7天3小时30分钟45秒"
print(cd.format(style="chinese"))

# 数字格式: "07:03:30:45"
print(cd.format(style="digital"))

# 词语格式: "7天3小时30分钟"
print(cd.format(style="words"))

# 包含名称
print(cd.format(include_name=True))  # "倒计时: 7天..."
```

### 进度条

```python
# 创建50%进度的倒计时
start = datetime.now() - timedelta(hours=1)
target = datetime.now() + timedelta(hours=1)
cd = Countdown(target, start=start)

# 默认进度条
print(cd.progress_bar())  # "[████████░░] 50.0%"

# 自定义字符
print(cd.progress_bar(filled_char="#", empty_char="-"))

# 自定义宽度
print(cd.progress_bar(width=30))

# 不显示百分比
print(cd.progress_bar(show_percent=False))
```

### 从时间差创建

```python
from countdown_utils import countdown_from_delta, timedelta

# 使用 timedelta
cd = countdown_from_delta(timedelta(days=3), name="3天后")

# 使用秒数
cd = countdown_from_delta(3600, name="1小时后")
```

### 批量倒计时

```python
from countdown_utils import multi_countdown

targets = [
    "2027-12-31",                    # 纯时间字符串
    ("春节", "2027-01-29"),          # 带名称
    ("考试", "2026-06-15 09:00:00"), # 带时间
]

results = multi_countdown(targets)
for item in results:
    print(f"{item['name']}: {item['formatted']}")
```

### 计时器（正向计时）

```python
from countdown_utils import CountdownTimer
import time

timer = CountdownTimer()

# 做一些事情
time.sleep(2)

# 查看耗时
print(timer.elapsed())           # timedelta对象
print(timer.elapsed_seconds())   # 秒数
print(timer.elapsed_formatted()) # "2秒"

# 暂停和恢复
timer.pause()
time.sleep(1)
timer.resume()

# 重置
timer.reset()

# 记录圈数
lap_time = timer.lap()
```

## 便捷函数

### 快速计算

```python
from countdown_utils import days_until, hours_until, minutes_until

# 计算天数
days = days_until("2026-12-31")

# 计算小时数
hours = hours_until(target)

# 计算分钟数
minutes = minutes_until(target)
```

### 下一次出现

```python
from countdown_utils import next_occurrence, countdown_to_next

# 获取下一个09:00的时间点
next_time = next_occurrence("09:00")

# 创建到下一个17:00的倒计时
cd = countdown_to_next("17:00", name="下班")
print(cd.format())
```

### 格式化持续时间

```python
from countdown_utils import format_duration

# 默认格式
print(format_duration(3661))  # "1小时 1分钟 1秒"

# 紧凑格式
print(format_duration(3661, style="compact"))  # "1h 1m 1s"

# 数字格式
print(format_duration(3661, style="digital"))  # "00:01:01:01"
```

## 支持的日期格式

```python
# 支持多种日期格式
formats = [
    "2026-12-31 23:59:59",
    "2026-12-31",
    "2026/12/31 23:59",
    "2026/12/31",
    "2026年12月31日",
    "12-31-2026",
    "12/31/2026",
]

for fmt in formats:
    future = fmt.replace("2026", "2027")  # 使用未来日期
    cd = Countdown(future)
    print(cd.format())
```

## API 参考

### Countdown 类

| 方法/属性 | 说明 |
|-----------|------|
| `remaining` | 剩余时间（timedelta） |
| `total_seconds` | 总剩余秒数 |
| `is_expired` | 是否已过期 |
| `progress` | 进度（0.0-1.0） |
| `get_components()` | 获取时间组件（天、时、分、秒） |
| `format(style)` | 格式化输出 |
| `progress_bar(width)` | 进度条 |
| `to_dict()` | 转字典 |

### CountdownTimer 类

| 方法 | 说明 |
|------|------|
| `elapsed()` | 已流逝时间 |
| `elapsed_seconds()` | 已流逝秒数 |
| `elapsed_formatted()` | 格式化已流逝时间 |
| `pause()` | 暂停 |
| `resume()` | 恢复 |
| `reset()` | 重置 |
| `lap()` | 记录圈数 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `create_countdown(target, name)` | 创建倒计时 |
| `countdown_from_delta(delta, name)` | 从时间差创建 |
| `multi_countdown(targets)` | 批量倒计时 |
| `format_duration(seconds, style)` | 格式化持续时间 |
| `time_until(target)` | 计算剩余时间 |
| `next_occurrence(time_str)` | 下一次时间出现 |
| `countdown_to_next(time_str, name)` | 到下一次时间的倒计时 |
| `days_until(target)` | 剩余天数 |
| `hours_until(target)` | 剩余小时数 |
| `minutes_until(target)` | 剩余分钟数 |

## 测试

```bash
python Python/countdown_utils/countdown_utils_test.py
```

**测试覆盖**: 23+ 测试用例，100% 通过率 ✅

---

**最后更新**: 2026-05-14