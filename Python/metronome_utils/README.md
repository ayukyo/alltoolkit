# Metronome Utils - 节拍器工具模块

节拍器工具模块，提供 BPM 计算、节拍生成、速度标记转换、节奏模式等功能，帮助音乐家练习节奏。

## 功能特点

- **BPM 计算**: BPM 与毫秒/秒转换、时长计算
- **速度标记**: 意大利语速度标记对照（Largo, Allegro, Presto 等）
- **拍号处理**: 支持简单拍号和复合拍号（2/4, 3/4, 4/4, 6/8, 5/4, 7/8 等）
- **节拍细分**: 四分音符、八分音符、三连音、十六分音符等
- **节奏模式**: 生成各种节奏模式的时间点
- **练习计划**: 自动生成 BPM 递进练习序列
- **音乐风格**: 各音乐风格的推荐 BPM 范围
- **延迟计算**: 效果器延迟时间计算

## 安装

```bash
# 无需安装，直接导入使用
from metronome_utils.mod import Metronome, bpm_to_ms
```

## 快速开始

### BPM 转换

```python
from mod import bpm_to_ms, bpm_to_seconds, get_tempo_marking

# BPM 转毫秒/秒
ms = bpm_to_ms(120)      # 500.0 毫秒
sec = bpm_to_seconds(60) # 1.0 秒

# 获取速度标记
italian, chinese = get_tempo_marking(120)
print(f"{italian} ({chinese})")  # Allegro (快板)
```

### 节拍器类

```python
from mod import Metronome, TimeSignature, Subdivision

# 创建节拍器
metronome = Metronome(
    bpm=100,
    time_signature=TimeSignature.FOUR_FOUR,
    subdivision=Subdivision.EIGHTH
)

# 获取时间信息
beat_duration = metronome.get_beat_duration_ms()     # 600ms
measure_duration = metronome.get_measure_duration_ms() # 2400ms

# 获取强拍位置
downbeats = metronome.get_downbeats()  # [1, 3] for 4/4

# 生成节拍序列
beats = metronome.generate_beats(4)  # 4小节
```

### 拍号处理

```python
from mod import parse_time_signature, get_time_signature_info

# 解析拍号
beats, unit = parse_time_signature("6/8")

# 获取拍号信息
info = get_time_signature_info(6, 8)
print(f"名称: {info['name']}")           # 六八拍（复拍子）
print(f"类型: {info['type']}")           # 复合拍号
print(f"强拍: {info['downbeats']}")      # [1]
```

### 练习计划

```python
from mod import create_practice_routine, adjust_bpm_for_exercise

# 创建练习计划
routine = create_practice_routine(
    target_bpm=120,
    current_bpm=60,
    minutes_per_step=5,
    difficulty='medium'
)

for step in routine:
    print(f"步骤{step['step']}: {step['bpm']} BPM")
```

### 节奏模式

```python
from mod import generate_rhythm_pattern

# 创建切分节奏模式
pattern = [1, 0, 1, 0]  # 强 弱 休止 弱
result = generate_rhythm_pattern(120, pattern, 2)  # 2小节

for r in result:
    symbol = '●' if r['has_note'] else '○'
    print(f"{symbol} @ {r['time_ms']:.0f}ms")
```

### 音乐风格 BPM

```python
from mod import suggest_bpm_for_genre

# 获取摇滚乐 BPM 推荐
info = suggest_bpm_for_genre('rock')
print(f"BPM范围: {info['min_bpm']} - {info['max_bpm']}")
print(f"推荐: {info['suggested_bpm']} BPM")

# 其他风格
suggest_bpm_for_genre('jazz')    # 爵士: 100-150 BPM
suggest_bpm_for_genre('house')   # 浩室: 120-130 BPM
suggest_bpm_for_genre('waltz')   # 华尔兹: 84-120 BPM
```

### 延迟时间计算

```python
from mod import calculate_delay_time

# 计算效果器延迟时间
delay = calculate_delay_time(120, 'quarter')     # 500ms
delay = calculate_delay_time(120, 'eighth')      # 250ms
delay = calculate_delay_time(120, 'dotted_quarter')  # 750ms
```

## API 参考

### 工具函数

| 函数 | 说明 |
|------|------|
| `bpm_to_ms(bpm)` | BPM 转毫秒 |
| `bpm_to_seconds(bpm)` | BPM 转秒 |
| `ms_to_bpm(ms)` | 毫秒转 BPM |
| `seconds_to_bpm(seconds)` | 秒转 BPM |
| `get_tempo_marking(bpm)` | 获取速度标记 |
| `get_bpm_range_for_tempo(name)` | 从标记获取 BPM 范围 |
| `calculate_measures(bpm, duration)` | 计算小节数 |
| `calculate_duration(bpm, measures)` | 计算时长 |
| `adjust_bpm_for_exercise(...)` | 生成 BPM 递进序列 |
| `get_subdivision_name(divisions)` | 获取细分名称 |
| `calculate_delay_time(bpm, note_value)` | 计算延迟时间 |
| `parse_time_signature(string)` | 解析拍号字符串 |
| `get_time_signature_info(beats, unit)` | 获取拍号信息 |
| `generate_rhythm_pattern(bpm, pattern)` | 生成节奏时间点 |
| `suggest_bpm_for_genre(genre)` | 风格 BPM 推荐 |
| `create_practice_routine(...)` | 创建练习计划 |
| `calculate_polymetric_bpm(bpm1, bpm2)` | 多节奏同步计算 |
| `get_metronome_exercise(type)` | 获取练习类型信息 |

### Metronome 类

```python
class Metronome:
    bpm: int                   # 当前 BPM
    time_signature: TimeSignature  # 拍号
    subdivision: Subdivision   # 细分类型
    
    # 方法
    get_beat_duration_ms()      # 每拍毫秒
    get_beat_duration_seconds() # 每拍秒数
    get_measure_duration_ms()   # 每小节毫秒
    get_subdivision_duration_ms()  # 细分毫秒
    get_downbeats()             # 强拍位置列表
    is_downbeat(beat)           # 是否强拍
    generate_beats(num_measures)  # 生成节拍序列
    generate_subdivisions(num_beats)  # 生成细分序列
    start()                     # 启动节拍器
    stop()                      # 停止节拍器
    get_practice_session()      # 获取练习会话信息
```

### 枚举类型

#### TimeSignature（拍号）

- `TWO_FOUR` - 2/4 拍
- `THREE_FOUR` - 3/4 拍（华尔兹）
- `FOUR_FOUR` - 4/4 拍
- `SIX_EIGHT` - 6/8 拍（复拍子）
- `NINE_EIGHT` - 9/8 拍
- `TWELVE_EIGHT` - 12/8 拍
- `FIVE_FOUR` - 5/4 拍（不对称）
- `SEVEN_EIGHT` - 7/8 拍（不对称）

#### TempoMarking（速度标记）

| 标记 | BPM 范围 |
|------|---------|
| Larghissimo | 20-40 |
| Grave | 25-45 |
| Largo | 40-60 |
| Lento | 45-60 |
| Adagio | 66-76 |
| Andante | 76-108 |
| Moderato | 108-120 |
| Allegro | 120-168 |
| Vivace | 168-176 |
| Presto | 168-200 |
| Prestissimo | 200-250 |

#### Subdivision（细分）

- `QUARTER` - 四分音符（基本拍）
- `EIGHTH` - 八分音符（2份）
- `TRIPLET` - 三连音（3份）
- `SIXTEENTH` - 十六分音符（4份）
- `QUINTUPLET` - 五连音（5份）
- `SEXTUPLET` - 六连音（6份）
- `SEPTUPLET` - 七连音（7份）
- `THIRTY_SECOND` - 三十二分音符（8份）

## 支持的音乐风格

| 风格 | BPM 范围 | 中文名 |
|------|---------|-------|
| ballad | 60-80 | 抒情慢歌 |
| rock | 110-140 | 摇滚 |
| pop | 100-130 | 流行 |
| hip_hop | 80-115 | 嘻哈 |
| jazz | 100-150 | 爵士 |
| house | 120-130 | 浩室 |
| techno | 120-150 | 科技舞曲 |
| dubstep | 140-150 | 回响贝斯 |
| drum_and_bass | 160-180 | 鼓打贝斯 |
| metal | 100-160 | 金属 |
| punk | 150-200 | 朋克 |
| waltz | 84-120 | 华尔兹 |
| tango | 110-130 | 探戈 |
| salsa | 150-220 | 萨尔萨 |

## 练习类型

| 类型 | 难度 | 说明 |
|------|------|------|
| basic | 初级 | 基础节拍练习 |
| subdivision | 中级 | 细分练习（八分音符、三连音等）|
| accent | 中级 | 重音练习 |
| polyrhythm | 高级 | 多节奏练习（2对3、3对4）|
| mixed | 高级 | 混合技巧综合练习 |

## 版本

- **版本**: 1.0.0
- **作者**: AllToolkit
- **日期**: 2026-05-17

## 许可证

MIT License