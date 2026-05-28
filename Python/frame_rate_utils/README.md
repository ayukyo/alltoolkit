# Frame Rate Utils - 帧率计算工具

视频编辑、动画和游戏开发中的帧率计算工具集。

## 功能特性

- ✅ 帧数与时间的相互转换
- ✅ 时间码生成和解析（SMPTE 时间码格式）
- ✅ Drop-frame 和 Non-drop-frame 支持
- ✅ 帧率转换计算
- ✅ 常见帧率预设（24fps, 25fps, 30fps, 29.97fps, 60fps 等）
- ✅ 高帧率支持（48fps, 120fps, 240fps）
- ✅ 3:2 Pulldown 计算
- ✅ 精确的分数表示（避免浮点误差）
- ✅ 零外部依赖，纯 Python 实现

## 安装

直接复制 `frame_rate_utils` 目录到项目中即可使用。

```python
from frame_rate_utils import (
    FrameRate,
    Timecode,
    FrameConverter,
    frames_to_seconds,
    seconds_to_frames,
    frames_to_timecode,
    timecode_to_frames,
)
```

## 快速开始

### 基本帧率操作

```python
from frame_rate_utils import FrameRate
from fractions import Fraction

# 创建帧率对象
fps_30 = FrameRate(30)
fps_24 = FrameRate(24)
fps_2997 = FrameRate(Fraction(30000, 1001))  # 29.97fps (NTSC)

print(fps_30)  # 30 fps
print(fps_2997)  # 29.97 fps

# 帧率属性
print(fps_30.float_value)      # 30.0
print(fps_30.frame_duration_ms) # 33.33... 每帧毫秒数
```

### 帧数与时间转换

```python
from frame_rate_utils import frames_to_seconds, seconds_to_frames

# 帧数转秒数
seconds = frames_to_seconds(90, 30)  # 3.0 秒

# 秒数转帧数
frames = seconds_to_frames(5.5, 30)   # 165 帧

# 不同舍入方式
frames_round = seconds_to_frames(1.7, 30, 'round')  # 51
frames_floor = seconds_to_frames(1.7, 30, 'floor')  # 50
frames_ceil = seconds_to_frames(1.7, 30, 'ceil')    # 51
```

### 时间码操作

```python
from frame_rate_utils import Timecode, frames_to_timecode, timecode_to_frames

# 从帧数创建时间码
tc = Timecode.from_frames(90, 30)
print(tc)  # 00:00:03:00

# 从秒数创建时间码
tc = Timecode.from_seconds(90.5, 30)
print(tc)  # 00:01:30:15

# 从字符串解析时间码
tc = Timecode.from_string("01:23:45:12", 30)
print(tc.hours, tc.minutes, tc.seconds, tc.frames)  # 1 23 45 12

# 时间码转帧数
frames = timecode_to_frames("00:01:30:00", 30)  # 2700

# 帧数转时间码
tc_str = frames_to_timecode(2700, 30)  # "00:01:30:00"

# 时间码运算
tc1 = Timecode.from_string("00:00:30:00", 30)
tc2 = Timecode.from_string("00:00:45:00", 30)
print(tc1 + tc2)  # 00:01:15:00
print(tc2 - tc1)  # 00:00:15:00

# 时间码比较
print(tc1 < tc2)   # True
print(tc1 == tc1)  # True
```

### Drop-Frame 时间码

```python
from frame_rate_utils import FrameRate, Timecode, is_drop_frame_rate
from fractions import Fraction

# 创建 drop-frame 帧率
fps_df = FrameRate(Fraction(30000, 1001), is_drop_frame=True)

# Drop-frame 时间码使用分号分隔
tc_df = Timecode.from_frames(107892, fps_df, is_drop_frame=True)
print(tc_df)  # 01:00:00;00 (使用分号表示 drop-frame)

# 判断是否为 drop-frame 帧率
print(is_drop_frame_rate(Fraction(30000, 1001)))  # True (29.97fps)
print(is_drop_frame_rate(30))                     # False
```

### 帧率转换

```python
from frame_rate_utils import convert_frame_rate, FrameConverter
from fractions import Fraction

# 24fps 转 30fps
frames_30 = convert_frame_rate(24, 24, 30)  # 30

# 23.976fps 转 29.97fps
frames_2997 = convert_frame_rate(
    24,
    Fraction(24000, 1001),  # 23.976fps
    Fraction(30000, 1001)   # 29.97fps
)

# 计算 3:2 Pulldown 参数
pulldown = FrameConverter.calculate_pull_down()
print(pulldown['is_32_pulldown'])  # True
```

### 帧率预设

```python
from frame_rate_utils import FrameRate, FRAME_RATE_PRESETS

# 可用预设
print(FRAME_RATE_PRESETS.keys())
# dict_keys(['film', 'pal', 'ntsc', 'ntsc_df', 'ntsc_ndf', 'p25', 'p30', ...])

# 使用预设创建帧率
film_fps = FrameRate(FRAME_RATE_PRESETS['film'])      # 24fps
pal_fps = FrameRate(FRAME_RATE_PRESETS['pal'])        # 25fps
ntsc_df = FrameRate(FRAME_RATE_PRESETS['ntsc_df'], is_drop_frame=True)  # 29.97fps
```

## API 参考

### FrameRate 类

| 方法/属性 | 描述 |
|----------|------|
| `FrameRate(fps, is_drop_frame=False)` | 创建帧率对象 |
| `.float_value` | 浮点数形式的帧率 |
| `.numerator` | 帧率分子 |
| `.denominator` | 帧率分母 |
| `.frame_duration` | 每帧时长（秒） |
| `.frame_duration_ms` | 每帧时长（毫秒） |
| `.frames_to_seconds(frames)` | 帧数转秒数 |
| `.seconds_to_frames(seconds, rounding)` | 秒数转帧数 |

### Timecode 类

| 方法/属性 | 描述 |
|----------|------|
| `Timecode.from_frames(frames, fps, is_drop_frame)` | 从帧数创建 |
| `Timecode.from_seconds(seconds, fps, is_drop_frame)` | 从秒数创建 |
| `Timecode.from_string(timecode, fps)` | 从字符串解析 |
| `.total_frames` | 总帧数 |
| `.total_seconds` | 总秒数 |
| `.total_milliseconds` | 总毫秒数 |
| `+`, `-` | 时间码加减运算 |
| `<`, `<=`, `>`, `>=`, `==` | 时间码比较 |

### 便捷函数

| 函数 | 描述 |
|------|------|
| `frames_to_seconds(frames, fps)` | 帧数转秒数 |
| `seconds_to_frames(seconds, fps, rounding)` | 秒数转帧数 |
| `frames_to_timecode(frames, fps, is_drop_frame)` | 帧数转时间码字符串 |
| `timecode_to_frames(timecode, fps)` | 时间码字符串转帧数 |
| `timecode_to_seconds(timecode, fps)` | 时间码字符串转秒数 |
| `seconds_to_timecode(seconds, fps, is_drop_frame)` | 秒数转时间码字符串 |
| `convert_frame_rate(frames, from_fps, to_fps, rounding)` | 帧率转换 |
| `is_drop_frame_rate(fps)` | 判断是否为 drop-frame 帧率 |
| `calculate_drop_frame_count(frames, fps)` | 计算 drop-frame 丢帧数 |

## 支持的帧率

| 名称 | 帧率 | 用途 |
|------|------|------|
| film | 24 fps | 电影标准 |
| pal | 25 fps | PAL 电视 |
| ntsc | 30 fps | NTSC 整数帧率 |
| ntsc_df | 29.97 fps | NTSC Drop-frame |
| p48 | 48 fps | 高帧率电影 |
| p50 | 50 fps | PAL 高帧率 |
| p60 | 60 fps | 高帧率视频 |
| ntsc_60 | 59.94 fps | NTSC 高帧率 |
| p120 | 120 fps | 高帧率游戏 |
| p240 | 240 fps | 高帧率内容 |

## 常见用途

### 视频编辑
- 计算视频片段的帧数和时间码
- 处理不同帧率素材的转换
- NTSC Drop-frame 时间码计算

### 动画制作
- 精确计算帧时长
- 不同帧率间的动画转换
- 帧数和时间的双向转换

### 游戏开发
- 计算固定时间步长
- 高帧率时间计算
- 帧数预算规划

### 后期制作
- 时间码计算和验证
- 帧率转换和校准
- Pulldown 参数计算

## 测试

```bash
python -m pytest frame_rate_utils_test.py -v
```

## 许可证

MIT License