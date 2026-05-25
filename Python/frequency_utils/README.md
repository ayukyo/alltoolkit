# frequency_utils - 频率转换计算工具

频率单位转换和音频计算工具，零外部依赖。

## 功能特性

- **频率单位转换** - Hz/kHz/MHz/GHz/THz/rpm 等单位转换
- **周期计算** - 频率与周期转换
- **波长计算** - 频率与波长转换（电磁波、声波）
- **音符频率计算** - 音乐音符与频率转换
- **音分计算** - 音分（cent）计算
- **谐波生成** - 生成谐波序列
- **无线电频谱分类** - 识别无线电频段

## 主要类

### FrequencyUnit
频率单位枚举：`HZ`, `KILOHZ`, `MEGAHZ`, `GIGAHZ`, `TERAHZ`

### WaveMedium
波传播介质枚举：`VACUUM`, `AIR`, `WATER`

### FrequencyResult
频率转换结果类。

### WavelengthResult
波长计算结果类。

### NoteResult
音符计算结果类。

### CentResult
音分计算结果类。

### HarmonicResult
谐波结果类。

## 主要函数

### convert_frequency(value, from_unit, to_unit)
频率单位转换。

```python
convert_frequency(1000, 'kHz', 'Hz')  # 1000000.0
convert_frequency(2.4, 'GHz', 'MHz')  # 2400.0
```

### frequency_to_period(frequency_hz)
频率转换为周期（秒）。

```python
frequency_to_period(50)  # 0.02 (50Hz -> 20ms)
```

### frequency_to_wavelength(frequency_hz, medium)
频率转换为波长。

```python
frequency_to_wavelength(1000, WaveMedium.VACUUM)  # ~300 km (电磁波)
frequency_to_wavelength(440, WaveMedium.AIR)      # ~0.78 m (声波)
```

### note_to_frequency(note, octave, a4_hz)
音符转换为频率。

```python
note_to_frequency('A', 4)  # 440.0 Hz (标准A4)
note_to_frequency('C', 4)  # 261.63 Hz
```

### frequency_to_note(frequency_hz)
频率转换为音符。

```python
frequency_to_note(440)  # ('A', 4)
```

### calculate_cents(freq1, freq2)
计算两个频率之间的音分差。

```python
calculate_cents(440, 441)  # ~3.9 cents
```

### get_radio_band(frequency_hz)
获取无线电频段名称。

```python
get_radio_band(2.4e9)  # ('UHF', 'Ultra High Frequency')
```

### is_audio_frequency(frequency_hz)
判断是否为音频频率（20Hz - 20kHz）。

### is_radio_frequency(frequency_hz)
判断是否为无线电频率。

## 使用示例

```python
from frequency_utils import convert_frequency, note_to_frequency, get_radio_band

# 单位转换
print(convert_frequency(2.4, 'GHz', 'MHz'))  # 2400 MHz

# 音符频率
print(note_to_frequency('C', 4))  # 261.63 Hz (C4)

# 无线电频段
print(get_radio_band(98.7e6))  # ('FM', 'Frequency Modulation')

# 检查音频范围
print(is_audio_frequency(1000))  # True (在20Hz-20kHz范围内)
```

## 测试

运行测试：
```bash
python frequency_utils/frequency_utils_test.py
```

测试覆盖率：80 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*