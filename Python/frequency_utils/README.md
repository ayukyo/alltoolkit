# Frequency Utilities Module

频率单位转换与音频计算工具模块，零外部依赖，纯 Python 实现。

## 功能特性

### 频率单位转换
- 支持多种频率单位：Hz, kHz, MHz, GHz, THz, pHz, nHz, μHz, mHz
- 支持 RPM（转/分钟）和 RPS（转/秒）
- 自动选择最佳单位显示

### 周期与频率转换
- 频率转周期（秒、毫秒、微秒）
- 周期转频率
- 角频率计算（ω = 2πf）

### 波长计算
- 频率与波长转换
- 支持多种介质：真空（光速）、空气（声速）、水（声速）
- 返回多单位波长结果

### 音乐音符计算
- 音符名称转频率（A4 = 440 Hz 标准）
- 频率转音符（返回音符名、八度、MIDI编号）
- 支持升号（#）和降号（b）命名
- 可自定义 A4 参考频率
- 谐波系列生成
- 半音阶和大调音阶生成

### 音分计算
- 两频率间的音分差计算
- 音分转频率
- 频率比转音分
- 音分转频率比

### 无线电频谱
- 频段分类（ELF, VLF, LF, MF, HF, VHF, UHF, SHF, EHF 等）
- 频段频率范围查询
- 频段列表

### 实用工具
- 检测音频范围（20 Hz - 20 kHz）
- 检测无线电频率范围
- 检测可见光频率范围
- 频率描述生成
- 频率格式化显示

## 使用示例

```python
from mod import (
    convert_frequency,
    frequency_to_all,
    note_to_frequency,
    frequency_to_note,
    calculate_cents,
    get_radio_band,
    format_frequency,
)

# 频率单位转换
print(convert_frequency(1000, 'Hz', 'kHz'))  # 1.0
print(convert_frequency(60, 'rpm', 'Hz'))    # 1.0

# 获取所有单位转换结果
result = frequency_to_all(100, 'MHz')
print(result.hertz)        # 100000000.0
print(result.kilohertz)    # 100000.0
print(result.period_seconds)  # 1e-8

# 音符频率计算
print(note_to_frequency('A', 4))    # 440.0 Hz
print(note_to_frequency('C', 4))    # 261.63 Hz (中央C)

# 频率转音符
note = frequency_to_note(466.16)
print(note.full_name)  # A#4
print(note.midi_note)  # 70

# 音分计算
cents = calculate_cents(440, 880)  # 一个八度
print(cents)  # 1200.0

# 无线电频段
band = get_radio_band(2.4e9)  # WiFi频率
print(band)  # ('UHF', 'Ultra High Frequency')

# 格式化频率显示
print(format_frequency(1500000))  # 1.50 MHz
```

## 运行测试

```bash
cd Python/frequency_utils
python -m pytest frequency_utils_test.py -v
```

## API 参考

### 频率转换

| 函数 | 说明 |
|------|------|
| `convert_frequency(value, from_unit, to_unit)` | 频率单位转换 |
| `frequency_to_all(value, unit)` | 转换为所有常用单位 |

### 周期函数

| 函数 | 说明 |
|------|------|
| `frequency_to_period(frequency_hz)` | 频率转周期 |
| `period_to_frequency(period_seconds)` | 周期转频率 |
| `angular_frequency(frequency_hz)` | 计算角频率 |

### 波长函数

| 函数 | 说明 |
|------|------|
| `frequency_to_wavelength(frequency_hz, wave_speed)` | 频率转波长 |
| `wavelength_to_frequency(wavelength_m, wave_speed)` | 波长转频率 |
| `get_wavelength_result(frequency_hz, medium)` | 获取完整波长结果 |

### 音乐音符

| 函数 | 说明 |
|------|------|
| `note_to_frequency(note, octave, a4_hz)` | 音符转频率 |
| `frequency_to_note(frequency_hz, a4_hz, naming)` | 频率转音符 |
| `get_midi_frequency(midi_note, a4_hz)` | MIDI编号转频率 |
| `get_note_harmonics(fundamental_hz, num_harmonics)` | 获取谐波系列 |
| `generate_chromatic_scale(start_note, start_octave, num_notes)` | 生成半音阶 |
| `generate_major_scale(root_note, octave)` | 生成大调音阶 |

### 音分计算

| 函数 | 说明 |
|------|------|
| `calculate_cents(frequency1, frequency2)` | 计算音分差 |
| `cents_to_frequency(base_frequency, cents)` | 音分转频率 |
| `get_cent_result(frequency1, frequency2)` | 获取完整音分结果 |
| `frequency_ratio_to_cents(ratio)` | 频率比转音分 |
| `cents_to_ratio(cents)` | 音分转频率比 |

### 无线电频谱

| 函数 | 说明 |
|------|------|
| `get_radio_band(frequency_hz)` | 获取频段信息 |
| `get_band_frequencies(band_code)` | 获取频段频率范围 |
| `list_radio_bands()` | 列出所有频段 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `is_audio_frequency(frequency_hz)` | 检测音频范围 |
| `is_radio_frequency(frequency_hz)` | 检测无线电频率 |
| `is_visible_light(frequency_hz)` | 检测可见光 |
| `get_frequency_description(frequency_hz)` | 获取频率描述 |
| `format_frequency(frequency_hz, precision)` | 格式化频率显示 |

## 常量

```python
SPEED_OF_LIGHT = 299792458.0      # 光速 (m/s)
SPEED_OF_SOUND_AIR_20C = 343.0    # 空气中声速 (20°C)
SPEED_OF_SOUND_WATER = 1481.0    # 水中声速 (20°C)
STANDARD_A4 = 440.0               # A4 标准频率 (Hz)
CENTS_PER_OCTAVE = 1200           # 每八度的音分
SEMITONES_PER_OCTAVE = 12         # 每八度的半音
```

## 枚举类型

```python
FrequencyUnit    # 频率单位 (HZ, KILOHZ, MEGAHZ, GIGAHZ, TERAHZ, RPM, RPS 等)
WaveMedium       # 波介质 (VACUUM, AIR, WATER)
NoteNaming       # 音符命名 (SHARP, FLAT, BOTH)
```

## 数据类

```python
FrequencyResult      # 频率转换结果
WavelengthResult     # 波长计算结果
NoteResult           # 音符计算结果
CentResult           # 音分计算结果
HarmonicResult       # 谐波系列结果
```

## 无线电频段参考

| 频段 | 频率范围 | 名称 |
|------|----------|------|
| ELF | 3-30 Hz | 极低频 |
| SLF | 30-300 Hz | 超低频 |
| ULF | 300-3000 Hz | 特低频 |
| VLF | 3-30 kHz | 甚低频 |
| LF | 30-300 kHz | 低频 |
| MF | 300-3000 kHz | 中频 |
| HF | 3-30 MHz | 高频 |
| VHF | 30-300 MHz | 甚高频 |
| UHF | 300-3000 MHz | 特高频 |
| SHF | 3-30 GHz | 超高频 |
| EHF | 30-300 GHz | 极高频 |

## 作者

AllToolkit Contributors

## 许可证

MIT License