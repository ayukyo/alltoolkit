# Music Chord Utils 🎵

音乐和弦工具，提供和弦转位、调号识别、音程计算等功能。

## 特性

- ✅ **和弦转位** - 三和弦、七和弦转位
- ✅ **调号识别** - 大小调识别
- ✅ **音程计算** - 音程距离计算
- ✅ **和弦命名** - 自动识别和弦类型
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from music_chord_utils import Chord, get_chord_type, transpose_chord

# 创建和弦
chord = Chord("C", "major")
print(chord.notes)  # ['C', 'E', 'G']

# 转位
first_inv = chord.first_inversion()
print(first_inv.notes)  # ['E', 'G', 'C']

# 转调
transposed = transpose_chord("Am", 2)  # 向上大二度过
print(transposed)  # 'Bm'
```

## API 参考

| 类/函数 | 说明 |
|---------|------|
| `Chord` | 和弦类 |
| `get_chord_type(notes)` | 获取和弦类型 |
| `transpose_chord(chord, semitones)` | 和弦转调 |
| `get_scale(key)` | 获取音阶 |
| `get_key_signature(key)` | 获取调号 |
