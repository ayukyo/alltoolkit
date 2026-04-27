# Pulse Utils - 脉冲/心跳工具模块

提供脉冲信号生成、处理、检测和分析功能。零外部依赖，仅使用 Python 标准库。

## 功能概览

| 功能模块 | 描述 |
|---------|------|
| 波形生成 | 方波、正弦波、三角波、锯齿波、脉冲序列 |
| BPM 工具 | BPM 与频率/间隔转换 |
| 节拍器 | 音乐节拍器信号生成 |
| 占空比 | 占空比计算与分析 |
| 脉冲检测 | 信号中的脉冲识别与计数 |
| 心跳模拟 | 生物心跳信号模拟与分析 |
| 音符转换 | 音符名称与频率互转 |
| 信号处理 | 混合、归一化、放大、限幅 |

## 安装使用

```python
from pulse_utils import (
    generate_square_wave,
    generate_sine_wave,
    bpm_to_frequency,
    generate_metronome,
    simulate_heartbeat,
    note_to_frequency
)

# 生成方波
samples = generate_square_wave(440, 1.0)  # 440Hz, 1秒

# BPM 转换
bpm = 120
freq = bpm_to_frequency(bpm)  # 2 Hz
interval = bpm_to_interval_ms(bpm)  # 500 ms

# 音符转换
freq = note_to_frequency('A4')  # 440 Hz
```

## 详细功能

### 波形生成

#### 方波 (Square Wave)

```python
samples = generate_square_wave(
    frequency=440,      # 频率 (Hz)
    duration=1.0,       # 持续时间 (秒)
    sample_rate=44100,  # 采样率
    duty_cycle=0.5,     # 占空比 (0-1)
    amplitude=1.0       # 振幅 (0-1)
)
```

#### 正弦波 (Sine Wave)

```python
samples = generate_sine_wave(
    frequency=440,
    duration=1.0,
    amplitude=1.0,
    phase=0.0           # 初始相位 (弧度)
)
```

#### 三角波 (Triangle Wave)

```python
samples = generate_triangle_wave(
    frequency=220,
    duration=1.0,
    amplitude=1.0
)
```

#### 锯齿波 (Sawtooth Wave)

```python
samples = generate_sawtooth_wave(
    frequency=330,
    duration=1.0,
    amplitude=1.0,
    rising=True         # True=上升, False=下降
)
```

#### 脉冲序列 (Pulse Train)

```python
samples = generate_pulse_train(
    frequency=10,       # 重复频率
    duration=1.0,
    pulse_width=0.01,   # 单个脉冲宽度
    amplitude=1.0
)
```

### BPM 工具

```python
# BPM ↔ 频率
freq = bpm_to_frequency(120)        # 2 Hz
bpm = frequency_to_bpm(2.0)         # 120

# BPM ↔ 间隔 (毫秒)
interval = bpm_to_interval_ms(120)  # 500 ms
bpm = interval_ms_to_bpm(500)       # 120
```

### 节拍器

```python
# 基本节拍器
samples = generate_metronome(
    bpm=120,
    duration=10.0
)

# 带重音模式 (4/4拍)
samples = generate_metronome(
    bpm=120,
    duration=10.0,
    accent_pattern=[1, 0, 0, 0]  # 第一拍重音
)
```

### 占空比计算

```python
# 计算占空比
duty = calculate_duty_cycle(0.5, 1.0)  # 高电平0.5秒，周期1秒 → 50%

# 计算高电平时间
high_time = calculate_high_time(0.25, 2.0)  # 25%占空比，周期2秒 → 0.5秒
```

### 脉冲检测

```python
# 检测脉冲
pulses = detect_pulses(
    samples,           # 样本列表
    sample_rate=44100,
    threshold=0.5,     # 检测阈值
    min_pulse_width=0.001
)

for pulse in pulses:
    print(f"时间: {pulse.timestamp}s")
    print(f"值: {pulse.value}")
    print(f"持续时间: {pulse.duration}s")

# 快速计数
count = count_pulses(samples, threshold=0.5)
```

### 脉冲分析

```python
result = analyze_pulse_signal(samples, 44100)
print(f"脉冲数: {result['pulse_count']}")
print(f"平均占空比: {result['avg_duty_cycle']}")
print(f"估计频率: {result['frequency']} Hz")
```

### 心跳模拟

```python
from pulse_utils import HeartbeatPattern, simulate_heartbeat, analyze_heartbeat

# 自定义心跳模式
pattern = HeartbeatPattern(
    base_bpm=72,          # 基础心率
    variability=5,        # 心率变异
    double_beat=True      # 双跳模式 (lub-dub)
)

# 生成心跳信号
heartbeat = simulate_heartbeat(10.0, pattern)

# 分析心跳
analysis = analyze_heartbeat(heartbeat)
print(f"估计心率: {analysis['estimated_bpm']} BPM")
print(f"规律性: {analysis['regularity']}")
```

### 音符频率转换

```python
# 音符 → 频率
freq = note_to_frequency('A4')   # 440 Hz
freq = note_to_frequency('C4')   # ~261.63 Hz
freq = note_to_frequency('C#4')  # ~277.18 Hz (升号支持)

# 频率 → 音符
note = frequency_to_note(440)    # 'A4'

# 获取谐波
harmonics = get_harmonics(440, 8)  # [440, 880, 1320, 1760, ...]
```

### 信号处理

```python
# 混合信号
mixed = mix_signals(signal1, signal2)
mixed = mix_signals(signal1, signal2, weights=[0.7, 0.3])

# 归一化到 [-1, 1]
normalized = normalize_signal(samples)

# 放大
amplified = amplify_signal(samples, gain=2.0)

# 限幅
clipped = clip_signal(samples, limit=1.0)
```

## 数据类

### Pulse

```python
pulse = Pulse(
    timestamp=1.5,   # 时间戳 (秒)
    value=0.8,       # 脉冲值
    duration=0.1     # 持续时间 (秒)
)
```

### PulseSequence

```python
seq = PulseSequence(
    pulses=[...],
    total_duration=10.0,
    frequency=2.0,
    duty_cycle=0.2
)

len(seq)              # 脉冲数量
seq[0]                # 第一个脉冲
seq.get_values()      # 所有值列表
seq.get_timestamps()  # 所有时间戳列表
```

## 测试

```bash
python pulse_utils_test.py
```

测试覆盖:
- 波形生成 (方波/正弦/三角/锯齿/脉冲序列)
- BPM 转换
- 节拍器生成
- 占空比计算
- 脉冲检测与分析
- 心跳模拟与分析
- 音符频率转换
- 谐波生成
- 信号处理工具
- 边界值处理

## 应用场景

- 音频合成与处理
- 嵌入式系统脉冲控制
- 音乐节拍器应用
- 生物信号模拟
- 定时任务触发
- 信号分析教学
- 游戏开发音效

## 许可证

MIT License - 详见项目 LICENSE 文件

---

**作者**: AllToolkit  
**日期**: 2026-04-27