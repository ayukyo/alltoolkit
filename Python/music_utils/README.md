# Music Utils - 乐理工具库

零外部依赖的 Python 乐理工具库，提供音符、音阶、和弦、频率计算等完整的乐理功能。

## 功能特性

### 🎵 音符系统
- 音名枚举（C, D, E, F, G, A, B 及升降号）
- 音符类（包含音名和八度）
- MIDI 音符号转换
- 频率计算（十二平均律）
- 移调功能
- 音分偏差计算

### 🎼 音阶系统
- 大调、小调（自然、和声、旋律）
- 七种教会调式（多利亚、弗里几亚、利底亚等）
- 五声音阶（大调、小调）
- 布鲁斯音阶
- 半音阶、全音阶
- 音阶级别计算
- 调内和弦生成

### 🎸 和弦系统
- 30+ 和弦类型
- 大三、小三、增三、减三和弦
- 各类七和弦、九和弦、十一和弦、十三和弦
- 挂留和弦、强力和弦
- 和弦转位
- 和弦识别

### 🎹 频率与音律
- 十二平均律频率计算
- 纯律频率计算
- 泛音列生成
- 音分偏差计算
- 拍频计算

### ⏱ 节拍器
- BPM 到时值转换
- 速度术语标记
- 音符时值计算（含附点）

### 🎸 乐器支持
- 吉他标准调弦
- 贝斯标准调弦
- 尤克里里标准调弦
- 钢琴键号转换
- 品格音符计算

## 安装

无需安装依赖，直接导入使用：

```python
from music_utils import Note, NoteName, Scale, Chord
```

## 使用示例

### 音符操作

```python
from music_utils import Note, NoteName, parse_note

# 创建音符
c4 = Note(NoteName.C, 4)
print(c4)  # "C4"

# 频率计算
a4 = Note(NoteName.A, 4)
print(f"{a4.frequency()} Hz")  # 440.0 Hz

# 移调
d4 = c4.transpose(2)  # 移高大二度

# 解析音符字符串
note = parse_note("A#5")
```

### 音阶操作

```python
from music_utils import Scale, ScaleType, NoteName

# 创建大调音阶
c_major = Scale(NoteName.C, ScaleType.MAJOR)
print(c_major.notes())  # [C, D, E, F, G, A, B]

# 创建布鲁斯音阶
a_blues = Scale(NoteName.A, ScaleType.BLUES)

# 获取音阶频率
freqs = c_major.frequencies(4, 1)  # C4 大调音阶频率

# 检查音符是否在音阶内
c_major.contains_note(NoteName.E)  # True
c_major.contains_note(NoteName.F_SHARP)  # False
```

### 和弦操作

```python
from music_utils import Chord, ChordType, parse_chord

# 创建和弦
c_major = Chord(NoteName.C, ChordType.MAJOR)
print(c_major.notes())  # [C, E, G]

# 七和弦
g7 = Chord(NoteName.G, ChordType.DOMINANT_7)
print(g7.notes())  # [G, B, D, F]

# 和弦转位
voicing = c_major.invert(1)  # 第一转位

# 解析和弦字符串
chord = parse_chord("Am7")
chord = parse_chord("Cmaj7")
```

### 五度圈

```python
from music_utils import circle_of_fifths, circle_of_fourths

# 五度圈
fifths = circle_of_fifths()  # [C, G, D, A, E, B, F#, C#, G#, D#, A#, F]

# 四度圈
fourths = circle_of_fourths()
```

### 关系调

```python
from music_utils import relative_minor, relative_major

# C 大调的关系小调是 A 小调
a_minor = relative_minor(NoteName.C)

# A 小调的关系大调是 C 大调
c_major = relative_major(NoteName.A)
```

### 节拍器

```python
from music_utils import bpm_to_milliseconds, get_tempo_marking, NoteValue

# BPM 转换
ms = bpm_to_milliseconds(120)  # 500 ms/拍

# 速度术语
print(get_tempo_marking(140))  # Allegro (快板)

# 音符时值
quarter = NoteValue.QUARTER.duration_beats()  # 1.0 拍
dotted = NoteValue.QUARTER.duration_with_dots(1)  # 1.5 拍（附点）
```

### 乐器调弦

```python
from music_utils import (
    guitar_standard_tuning,
    bass_standard_tuning,
    ukulele_standard_tuning,
    fret_positions
)

# 吉他标准调弦 (EADGBE)
guitar = guitar_standard_tuning()

# 品格音符
e_string = guitar[0]  # 6弦 E2
frets = fret_positions(e_string, 12)  # 12品格音符
```

### 频率计算

```python
from music_utils import (
    equal_temperament_frequency,
    harmonic_series,
    just_intonation_frequency
)

# 十二平均律
freq = equal_temperament_frequency(0)  # 440 Hz (A4)

# 泛音列
harmonics = harmonic_series(440.0, 8)

# 纯律
freq = just_intonation_frequency(440.0, (3, 2))  # E5 纯律
```

## API 参考

### 音符

| 方法 | 说明 |
|------|------|
| `Note(name, octave)` | 创建音符 |
| `note.frequency()` | 返回频率 (Hz) |
| `note.midi()` | 返回 MIDI 音符号 |
| `note.transpose(semitones)` | 移调 |
| `Note.midi_to_note(midi)` | MIDI 转音符 |
| `Note.from_frequency(freq)` | 从频率获取音符 |
| `parse_note(str)` | 解析音符字符串 |

### 音阶

| 方法 | 说明 |
|------|------|
| `Scale(root, type)` | 创建音阶 |
| `scale.notes()` | 返回音阶音符 |
| `scale.frequencies(oct, octaves)` | 返回频率列表 |
| `scale.contains_note(note)` | 检查音符是否在音阶内 |
| `scale.degree(num)` | 返回音阶级别音名 |
| `scale.triad(num)` | 返回调内三和弦 |

### 和弦

| 方法 | 说明 |
|------|------|
| `Chord(root, type)` | 创建和弦 |
| `chord.notes()` | 返回和弦内音 |
| `chord.invert(num)` | 和弦转位 |
| `Chord.identify(notes)` | 从音名识别和弦 |
| `parse_chord(str)` | 解析和弦字符串 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `circle_of_fifths()` | 五度圈 |
| `circle_of_fourths()` | 四度圈 |
| `relative_minor(major)` | 关系小调 |
| `relative_major(minor)` | 关系大调 |
| `key_signature(key)` | 调号升降号 |
| `bpm_to_milliseconds(bpm)` | BPM 转毫秒 |
| `harmonic_series(freq, n)` | 泛音列 |

## 测试

运行测试：

```bash
python music_utils_test.py
```

## 支持的音阶类型

- MAJOR - 大调
- MINOR - 自然小调
- HARMONIC_MINOR - 和声小调
- MELODIC_MINOR - 旋律小调
- DORIAN - 多利亚调式
- PHRYGIAN - 弗里几亚调式
- LYDIAN - 利底亚调式
- MIXOLYDIAN - 混合利底亚调式
- LOCRIAN - 洛克利亚调式
- PENTATONIC_MAJOR - 大调五声
- PENTATONIC_MINOR - 小调五声
- BLUES - 布鲁斯
- CHROMATIC - 半音阶
- WHOLE_TONE - 全音阶

## 支持的和弦类型

- MAJOR - 大三和弦
- MINOR - 小三和弦
- DIMINISHED - 减三和弦
- AUGMENTED - 增三和弦
- MAJOR_7 - 大七和弦
- MINOR_7 - 小七和弦
- DOMINANT_7 - 属七和弦
- DIMINISHED_7 - 减七和弦
- HALF_DIMINISHED - 半减七和弦
- SUS_2, SUS_4 - 挂留和弦
- POWER - 强力和弦
- 以及九和弦、十一和弦、十三和弦等

## 作者

AllToolkit - 2026-05-02

## 许可

MIT License