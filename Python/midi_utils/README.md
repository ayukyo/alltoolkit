# MIDI Utilities 🎹

零依赖 MIDI 文件处理工具函数库

## 简介

`midi_utils` 提供完整的 MIDI 文件读取、解析、写入和生成功能，仅使用 Python 标准库，无需任何外部依赖。

### 核心功能

| 功能 | 说明 |
|------|------|
| 文件读写 | 读取和写入 MIDI 文件（格式 0 和 1） |
| 事件解析 | 解析所有 MIDI 事件类型（音符、控制变化、Meta 等） |
| 音符提取 | 从 MIDI 文件提取音符、时间、力度信息 |
| 旋律生成 | 快速创建旋律、音阶、和弦 |
| 移调处理 | 对音符进行升调或降调处理 |
| 时间转换 | tick、秒、BPM 之间的转换 |

---

## 快速开始

### 安装

无需安装！直接复制 `mod.py` 到项目即可使用。

```python
from midi_utils.mod import (
    read_midi, 
    write_midi,
    get_midi_info,
    extract_notes,
    create_simple_melody,
    create_scale,
    create_chord,
)
```

### 基础示例

```python
# 读取 MIDI 文件
midi = read_midi("song.mid")
print(f"轨道数: {len(midi.tracks)}")
print(f"BPM: {midi.bpm}")

# 提取音符
notes = extract_notes("song.mid")
for note in notes:
    print(f"{note.note_name} at {note.start_time}s, duration {note.duration}s")

# 创建简单旋律
melody = [
    ("C4", 1.0),  # 四分音符 C4
    ("D4", 1.0),  # 四分音符 D4
    ("E4", 1.0),  # 四分音符 E4
    ("G4", 2.0),  # 二分音符 G4
]
midi = create_simple_melody(melody, bpm=120)
write_midi(midi, "my_melody.mid")
```

---

## API 参考

### 文件操作

#### `read_midi(filepath)`

读取并解析 MIDI 文件。

```python
midi = read_midi("song.mid")
print(f"格式: {midi.format_type}")
print(f"轨道: {len(midi.tracks)}")
print(f"PPQN: {midi.ticks_per_beat}")
```

#### `write_midi(midi_file, filepath)`

写入 MIDI 文件。

```python
write_midi(midi, "output.mid")
```

#### `get_midi_info(filepath)`

获取 MIDI 文件信息摘要。

```python
info = get_midi_info("song.mid")
print(info)
# Output:
# MIDIInfo(
#   file='song.mid',
#   format=1,
#   tracks=4,
#   ppqn=480,
#   duration=120.50s,
#   bpm=120.0,
#   notes=256
# )
```

---

### 音符提取

#### `extract_notes(filepath)`

从 MIDI 文件提取所有音符事件。

```python
notes = extract_notes("song.mid")
for note in notes[:10]:
    print(f"{note.note_name} | {note.start_time:.3f}s | {note.duration:.3f}s | vel={note.velocity}")
```

---

### 旋律创建

#### `create_simple_melody(notes, bpm=120, velocity=100, channel=0, program=0)`

创建简单旋律 MIDI 文件。

```python
melody = [
    ("C4", 1.0),     # 四分音符
    ("D4", 1.0),     # 四分音符
    ("E4", 0.5),     # 八分音符
    ("F4", 0.5),     # 八分音符
    ("G4", 2.0),     # 二分音符
    ("R", 1.0),      # 四分休止符
]
midi = create_simple_melody(melody, bpm=120, program=0)  # 钢琴
write_midi(midi, "melody.mid")
```

**参数说明:**
- `notes`: 音符列表，格式为 `(音符名称, 时长)` 或 `(音符名称, 时长, 力度)`
- `bpm`: 速度 (BPM)
- `velocity`: 默认力度 (0-127)
- `channel`: MIDI 通道 (0-15)
- `program`: 音色编号 (0-127)

**时长单位:** 以四分音符为基准
- 1.0 = 四分音符
- 0.5 = 八分音符
- 0.25 = 十六分音符
- 2.0 = 二分音符
- 4.0 = 全音符

---

#### `create_scale(scale_type, root, bpm=120, velocity=80)`

创建音阶 MIDI 文件。

```python
# 大调音阶
midi = create_scale("major", "C4")
write_midi(midi, "c_major_scale.mid")

# 小调音阶
midi = create_scale("minor", "A3")
write_midi(midi, "a_minor_scale.mid")

# 五声音阶
midi = create_scale("pentatonic", "G4")
write_midi(midi, "g_pentatonic.mid")
```

**支持的音阶类型:**
- `major` - 大调音阶 (8 音符)
- `minor` - 自然小调音阶 (8 音符)
- `pentatonic` - 五声音阶 (6 音符)
- `blues` - 布鲁斯音阶 (7 音符)
- `chromatic` - 半音阶 (13 音符)

---

#### `create_chord(chord_name, duration=1.0, bpm=120, velocity=80)`

创建和弦 MIDI 文件。

```python
# 大三和弦
midi = create_chord("C4:major")
write_midi(midi, "c_major.mid")

# 小三和弦
midi = create_chord("A4:minor")
write_midi(midi, "a_minor.mid")

# 大七和弦
midi = create_chord("F4:maj7")
write_midi(midi, "f_major7.mid")
```

**和弦格式:** `根音:和弦类型`

**支持的和弦类型:**
- `major` - 大三和弦 (C-E-G)
- `minor` - 小三和弦 (C-Eb-G)
- `dim` - 减三和弦 (C-Eb-Gb)
- `aug` - 增三和弦 (C-E-G#)
- `maj7` - 大七和弦 (C-E-G-B)
- `min7` - 小七和弦 (C-Eb-G-Bb)
- `dom7` - 属七和弦 (C-E-G-Bb)
- `dim7` - 减七和弦 (C-Eb-Gb-A)
- `sus4` - 挂四和弦 (C-F-G)
- `sus2` - 挂二和弦 (C-D-G)

---

### 音符处理

#### `transpose_notes(notes, semitones)`

对音符进行移调。

```python
notes = extract_notes("song.mid")

# 升高一个八度
high = transpose_notes(notes, 12)

# 降低 3 个半音
low = transpose_notes(notes, -3)
```

#### `notes_to_text(notes)`

将音符列表转换为可读文本表格。

```python
notes = extract_notes("song.mid")
print(notes_to_text(notes))
# Output:
# Note     Start      Duration    Velocity   Channel
# --------------------------------------------------
# C4          0.000s     0.500s        100        0
# E4          0.500s     0.500s        100        0
# G4          1.000s     1.000s        100        0
```

---

### 音符转换

#### `midi_note_to_name(note_number)`

将 MIDI 音符编号转换为名称。

```python
print(midi_note_to_name(60))  # "C4"
print(midi_note_to_name(69))  # "A4" (标准音)
print(midi_note_to_name(0))   # "C-1"
print(midi_note_to_name(127)) # "G9"
```

#### `name_to_midi_note(note_name)`

将音符名称转换为 MIDI 编号。

```python
print(name_to_midi_note("C4"))  # 60
print(name_to_midi_note("A4"))  # 69
print(name_to_midi_note("C#5")) # 73
print(name_to_midi_note("Db5")) # 73 (同 C#5)
```

---

### 时间转换

#### `ticks_to_seconds(ticks, ticks_per_beat, bpm)`

将 tick 数转换为秒。

```python
# 120 BPM, 480 PPQN
# 480 ticks = 1 beat = 0.5 秒
duration = ticks_to_seconds(480, 480, 120)  # 0.5 秒
```

#### `seconds_to_ticks(seconds, ticks_per_beat, bpm)`

将秒转换为 tick 数。

```python
ticks = seconds_to_ticks(1.0, 480, 120)  # 960 ticks (2 beats)
```

---

### 乐器名称

#### `get_instrument_name(program, channel=0)`

获取乐器名称。

```python
print(get_instrument_name(0))   # "Acoustic Grand Piano"
print(get_instrument_name(24))  # "Acoustic Guitar (nylon)"
print(get_instrument_name(40))  # "Violin"
```

---

## 实用示例

### 1. 分析 MIDI 文件

```python
from midi_utils.mod import get_midi_info, extract_notes

# 获取基本信息
info = get_midi_info("piano_piece.mid")
print(f"时长: {info.duration:.2f}s")
print(f"音符数: {info.num_notes}")
print(f"BPM: {info.bpm}")

# 获取音符分布
notes = extract_notes("piano_piece.mid")
pitch_range = (min(n.note for n in notes), max(n.note for n in notes))
print(f"音域: {midi_note_to_name(pitch_range[0]} - {midi_note_to_name(pitch_range[1])}")
```

### 2. 批量移调

```python
from midi_utils.mod import read_midi, extract_notes, transpose_notes, write_midi

# 读取文件
midi = read_midi("original.mid")

# 提取音符
notes = midi.get_all_notes()

# 升高 2 个半音
transposed = transpose_notes(notes, 2)

# 创建新文件（简化示例）
# 注意：完整实现需要重新构建轨道事件
```

### 3. 生成练习音阶

```python
from midi_utils.mod import create_scale, write_midi

# 生成所有大调音阶
roots = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
for root in roots:
    midi = create_scale("major", root)
    write_midi(midi, f"{root[0]}_major_scale.mid")
```

### 4. 创建和弦练习

```python
from midi_utils.mod import create_chord, write_midi

# C 大调常用和弦
chords = [
    ("C4:major", "I"),
    ("D4:minor", "ii"),
    ("E4:minor", "iii"),
    ("F4:major", "IV"),
    ("G4:major", "V"),
    ("A4:minor", "vi"),
]

for chord_name, roman in chords:
    midi = create_chord(chord_name, duration=2.0)
    write_midi(midi, f"chord_{roman}.mid")
```

### 5. 创建简单旋律

```python
from midi_utils.mod import create_simple_melody, write_midi

# 《小星星》旋律
twinkle_twinkle = [
    ("C4", 0.5), ("C4", 0.5),  # 一闪一闪
    ("G4", 0.5), ("G4", 0.5),  # 亮晶晶
    ("A4", 0.5), ("A4", 0.5),  # 漫天都是
    ("G4", 1.0),               # 小星星
    ("F4", 0.5), ("F4", 0.5),  # 挂在天上
    ("E4", 0.5), ("E4", 0.5),  # 放光明
    ("D4", 0.5), ("D4", 0.5),  # 好像许多
    ("C4", 1.0),               # 小眼睛
]

midi = create_simple_melody(twinkle_twinkle, bpm=120, program=0)
write_midi(midi, "twinkle_twinkle.mid")
```

---

## MIDI 基础知识

### MIDI 音符编号

| 音符 | 编号 | 说明 |
|------|------|------|
| C-1 | 0 | MIDI 最低音 |
| A0 | 21 | 钢琴最低音 |
| C4 | 60 | 中央 C |
| A4 | 69 | 标准音 (440Hz) |
| C8 | 108 | 钢琴最高音附近 |
| G9 | 127 | MIDI 最高音 |

### 常用音色 (GM)

| 编号 | 音色 |
|------|------|
| 0 | 钢琴 |
| 24 | 尼龙弦吉他 |
| 25 | 钢弦吉他 |
| 33 | 电贝司 |
| 40 | 小提琴 |
| 56 | 小号 |
| 64 | 萨克斯 |
| 73 | 长笛 |

### 时间单位

- **PPQN** (Pulses Per Quarter Note): 每四分音符的 tick 数
- **常用值**: 96, 120, 240, 480, 960
- **BPM** (Beats Per Minute): 每分钟节拍数

---

## 测试

运行测试套件：

```bash
cd AllToolkit/Python/midi_utils
python midi_utils_test.py
```

测试覆盖：
- ✓ 音符编号转换
- ✓ 时间转换
- ✓ 可变长度编码
- ✓ MIDI 事件创建
- ✓ 旋律生成
- ✓ 音阶生成
- ✓ 和弦生成
- ✓ 音符提取
- ✓ 移调处理
- ✓ 文件读写
- ✓ 错误处理

---

## 注意事项

### 格式支持

- 支持 MIDI 格式 0（单轨道）和格式 1（多轨道）
- 不支持格式 2（很少使用）

### 限制

- 不支持 SMF (Standard MIDI File) 的某些高级特性
- 不支持 MIDI 2.0 格式
- 不处理音频采样（MIDI 仅记录音符信息）

---

## 版本历史

- **1.0.0** (2026-05-01) - 初始版本
  - MIDI 文件读写（格式 0/1）
  - 音符提取和解析
  - 旋律、音阶、和弦生成
  - 移调和时间转换
  - 完整测试套件

---

## 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

---

**Author:** AllToolkit  
**Version:** 1.0.0  
**Last Updated:** 2026-05-01