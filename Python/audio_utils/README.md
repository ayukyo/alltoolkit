# Audio Utilities 🎵

音频处理工具函数库 - 零依赖，生产就绪

## 📖 简介

`audio_utils` 提供常用的音频文件处理功能，仅使用 Python 标准库（`wave`, `aifc`, `sunau`, `audioop`），无需任何外部依赖。

### 支持格式

- **WAV** (.wav) - 完全支持读写
- **AIFF** (.aif, .aiff) - 完全支持读写
- **AU/SND** (.au, .snd) - 完全支持读写

### 核心功能

| 功能 | 说明 |
|------|------|
| 文件读写 | 安全读取/写入音频文件，自动创建目录 |
| 信息提取 | 获取格式、采样率、声道数、时长等元数据 |
| 音量调整 | 按比例放大或衰减音量 |
| 淡入淡出 | 添加线性淡入/淡出效果 |
| 音频拼接 | 将多个音频文件按顺序拼接 |
| 片段提取 | 提取指定时间段的音频片段 |
| 声道转换 | 立体声转单声道，分离左右声道 |
| 音频反转 | 倒放效果 |
| 波形生成 | 生成正弦波、音调 |
| 静音检测 | 检测音频中的静音片段 |
| 标准化 | 将音量标准化到指定峰值 |

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 导入
cp AllToolkit/Python/audio_utils/mod.py your_project/audio_utils.py
```

### 基础示例

```python
from audio_utils import (
    get_audio_info,
    read_audio,
    write_audio,
    adjust_volume,
    create_tone,
)

# 获取音频信息
info = get_audio_info('sample.wav')
print(f"格式：{info.format}")
print(f"时长：{info.duration:.2f}秒")
print(f"采样率：{info.framerate}Hz")
print(f"声道数：{info.channels}")

# 创建音调文件
create_tone('beep.wav', frequency=1000.0, duration=0.5)

# 调整音量
adjust_volume('quiet.wav', 'loud.wav', factor=2.0)
```

---

## 📚 API 参考

### 数据类

#### AudioInfo

音频文件信息数据类。

```python
@dataclass
class AudioInfo:
    filepath: str           # 文件路径
    format: str             # 格式：'WAV', 'AIFF', 'AU'
    channels: int           # 声道数
    sample_width: int       # 每采样字节数
    framerate: int          # 采样率 (Hz)
    frames: int             # 总帧数
    duration: float         # 时长 (秒)
    compression_type: str   # 压缩类型（可选）
    compression_name: str   # 压缩名称（可选）
```

### 异常类

```python
class AudioUtilsError(Exception)         # 基类
class UnsupportedFormatError(AudioUtilsError)  # 不支持的格式
class InvalidAudioError(AudioUtilsError)       # 无效的音频文件
```

### 核心函数

#### get_audio_info(filepath)

获取音频文件信息。

```python
info = get_audio_info('sample.wav')
print(f"Duration: {info.duration:.2f}s, Sample Rate: {info.framerate}Hz")
```

**参数:**
- `filepath`: 音频文件路径（支持 WAV/AIFF/AU）

**返回:** `AudioInfo` 数据类

**异常:**
- `FileNotFoundError`: 文件不存在
- `UnsupportedFormatError`: 不支持的格式
- `InvalidAudioError`: 无效的音频文件

---

#### read_audio(filepath)

读取音频文件原始数据。

```python
data, channels, sample_width, framerate = read_audio('sample.wav')
print(f"Read {len(data)} bytes of audio data")
```

**参数:**
- `filepath`: 音频文件路径

**返回:** `tuple` - (raw_data, channels, sample_width, framerate)

---

#### write_audio(filepath, data, channels, sample_width, framerate)

写入 WAV 音频文件。

```python
# 生成 1 秒 440Hz 正弦波
import math
data = b''.join(
    int(32767 * math.sin(2 * math.pi * 440 * i / 44100))
    .to_bytes(2, 'little', signed=True)
    for i in range(44100)
)
write_audio('tone.wav', data, channels=1, sample_width=2, framerate=44100)
```

**参数:**
- `filepath`: 输出文件路径
- `data`: 原始 PCM 数据 (bytes)
- `channels`: 声道数 (1=单声道，2=立体声)
- `sample_width`: 每采样字节数 (1=8-bit, 2=16-bit, 4=32-bit)
- `framerate`: 采样率 (Hz)

**返回:** `bool` - 成功返回 True

---

#### adjust_volume(filepath, output_path, factor)

调整音频音量。

```python
# 放大 2 倍
adjust_volume('quiet.wav', 'loud.wav', factor=2.0)

# 衰减到 50%
adjust_volume('loud.wav', 'quiet.wav', factor=0.5)
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径
- `factor`: 音量因子 (0.0=静音，1.0=不变，>1.0=放大)

**返回:** `bool` - 成功返回 True

---

#### fade_in(filepath, output_path, duration)

添加淡入效果。

```python
fade_in('music.wav', 'music_fadein.wav', duration=2.0)
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径
- `duration`: 淡入时长（秒）

**返回:** `bool` - 成功返回 True

---

#### fade_out(filepath, output_path, duration)

添加淡出效果。

```python
fade_out('music.wav', 'music_fadeout.wav', duration=2.0)
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径
- `duration`: 淡出时长（秒）

**返回:** `bool` - 成功返回 True

---

#### concatenate_audio(filepaths, output_path)

拼接多个音频文件。

```python
concatenate_audio(
    ['intro.wav', 'main.wav', 'outro.wav'], 
    'full.wav'
)
```

**参数:**
- `filepaths`: 输入音频文件路径列表
- `output_path`: 输出音频文件路径

**返回:** `bool` - 成功返回 True

**注意:** 所有输入文件必须具有相同的采样率、声道数和采样宽度。

---

#### extract_segment(filepath, output_path, start_time, end_time)

提取音频片段。

```python
# 提取 60-90 秒的片段
extract_segment('song.wav', 'chorus.wav', start_time=60.0, end_time=90.0)
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径
- `start_time`: 起始时间（秒）
- `end_time`: 结束时间（秒）

**返回:** `bool` - 成功返回 True

---

#### convert_to_mono(filepath, output_path)

转换为单声道。

```python
convert_to_mono('stereo.wav', 'mono.wav')
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径

**返回:** `bool` - 成功返回 True

---

#### reverse_audio(filepath, output_path)

反转音频（倒放效果）。

```python
reverse_audio('normal.wav', 'reversed.wav')
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径

**返回:** `bool` - 成功返回 True

---

#### generate_sine_wave(frequency, duration, ...)

生成正弦波音频。

```python
# 生成 440Hz A 音，1 秒时长
data = generate_sine_wave(440.0, 1.0, framerate=44100, amplitude=0.5)
write_audio('a4.wav', data, channels=1, sample_width=2, framerate=44100)
```

**参数:**
- `frequency`: 频率 (Hz)
- `duration`: 时长（秒）
- `framerate`: 采样率 (Hz)，默认 44100
- `amplitude`: 振幅 (0.0-1.0)，默认 0.5
- `channels`: 声道数，默认 1
- `sample_width`: 每采样字节数，默认 2

**返回:** `bytes` - 原始 PCM 数据

---

#### detect_silence(filepath, threshold)

检测静音片段。

```python
silences = detect_silence('speech.wav', threshold=200)
for start, end in silences:
    print(f"Silence from {start:.2f}s to {end:.2f}s")
```

**参数:**
- `filepath`: 输入音频文件路径
- `threshold`: 静音阈值（0-65535），默认 100

**返回:** `list` - [(start_time, end_time), ...]

---

#### get_peak_amplitude(filepath)

获取峰值振幅。

```python
peak = get_peak_amplitude('audio.wav')
print(f"Peak amplitude: {peak:.2%}")
```

**参数:**
- `filepath`: 输入音频文件路径

**返回:** `float` - 峰值振幅 (0.0-1.0)

---

#### normalize_audio(filepath, output_path, target_peak)

音频标准化。

```python
normalize_audio('quiet.wav', 'normalized.wav', target_peak=0.95)
```

**参数:**
- `filepath`: 输入音频文件路径
- `output_path`: 输出音频文件路径
- `target_peak`: 目标峰值 (0.0-1.0)，默认 0.95

**返回:** `bool` - 成功返回 True

---

### 便捷函数

#### create_tone(filepath, frequency, duration, framerate)

快速创建音调文件。

```python
create_tone('beep.wav', frequency=1000.0, duration=0.5)
```

**参数:**
- `filepath`: 输出文件路径
- `frequency`: 频率 (Hz)
- `duration`: 时长（秒）
- `framerate`: 采样率 (Hz)

**返回:** `bool` - 成功返回 True

---

#### split_stereo(filepath, output_left, output_right)

分离立体声声道。

```python
split_stereo('stereo.wav', 'left.wav', 'right.wav')
```

**参数:**
- `filepath`: 输入立体声音频文件路径
- `output_left`: 左声道输出路径
- `output_right`: 右声道输出路径

**返回:** `bool` - 成功返回 True

---

## 💡 实用示例

### 1. 批量转换音频为单声道

```python
from audio_utils import convert_to_mono, get_audio_info
from pathlib import Path

for wav_file in Path('audio_folder').glob('*.wav'):
    info = get_audio_info(wav_file)
    if info.channels == 2:
        output = wav_file.with_stem(wav_file.stem + '_mono')
        convert_to_mono(wav_file, output)
        print(f"Converted: {wav_file.name}")
```

### 2. 制作铃声（提取 + 淡入淡出）

```python
from audio_utils import extract_segment, fade_in, fade_out

# 提取副歌部分（60-90 秒）
extract_segment('song.wav', 'chorus.wav', 60.0, 90.0)

# 添加淡入淡出
fade_in('chorus.wav', 'chorus_fadein.wav', duration=2.0)
fade_out('chorus_fadein.wav', 'ringtone.wav', duration=2.0)
```

### 3. 拼接多段录音

```python
from audio_utils import concatenate_audio

recordings = [
    'recording_001.wav',
    'recording_002.wav',
    'recording_003.wav',
]

concatenate_audio(recordings, 'combined_recording.wav')
```

### 4. 生成测试音序列

```python
from audio_utils import create_tone, concatenate_audio
from pathlib import Path

# 生成 C 大调音阶
frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
note_files = []

for i, freq in enumerate(frequencies):
    note_file = Path(f'note_{i}.wav')
    create_tone(note_file, frequency=freq, duration=0.5)
    note_files.append(note_file)

# 拼接成音阶
concatenate_audio(note_files, 'scale.wav')
```

### 5. 检测并移除静音

```python
from audio_utils import detect_silence, extract_segment

silences = detect_silence('speech.wav', threshold=200)

# 提取非静音部分
for i, (start, end) in enumerate(silences):
    if i > 0:
        prev_end = silences[i-1][1]
        if start - prev_end > 0.5:  # 只提取超过 0.5 秒的片段
            extract_segment('speech.wav', f'segment_{i}.wav', 
                           prev_end, start)
```

### 6. 音频标准化批处理

```python
from audio_utils import normalize_audio, get_peak_amplitude
from pathlib import Path

for wav_file in Path('podcast_episodes').glob('*.wav'):
    peak = get_peak_amplitude(wav_file)
    if peak < 0.8:  # 如果峰值低于 80%，进行标准化
        output = wav_file.with_stem(wav_file.stem + '_normalized')
        normalize_audio(wav_file, output, target_peak=0.95)
        print(f"Normalized: {wav_file.name} ({peak:.1%} → 95%)")
```

---

## 🧪 测试

运行测试套件：

```bash
cd AllToolkit/Python/audio_utils
python audio_utils_test.py
```

测试覆盖：
- ✓ WAV/AIFF/AU 文件读写
- ✓ 音频信息提取
- ✓ 音量调整（放大/衰减）
- ✓ 淡入淡出效果
- ✓ 音频拼接
- ✓ 片段提取
- ✓ 声道转换
- ✓ 音频反转
- ✓ 正弦波生成
- ✓ 静音检测
- ✓ 峰值振幅计算
- ✓ 音频标准化
- ✓ 音调创建
- ✓ 立体声分离

---

## ⚠️ 注意事项

### 格式限制

- 本模块仅支持无损格式（WAV/AIFF/AU）
- 不支持 MP3、AAC、OGG 等压缩格式（需要额外依赖如 pydub、ffmpeg）

### 性能考虑

- 大文件处理时，`read_audio` 会将整个文件加载到内存
- 对于超长音频（>10 分钟），建议先分割再处理

### 音频质量

- 音量放大超过 1.0 可能导致削波失真
- 标准化时建议使用 0.9-0.95 的目标峰值，留出余量

### 采样率匹配

- 拼接音频时，所有文件必须具有相同的采样率、声道数和采样宽度
- 如需转换采样率，请使用专业工具（如 ffmpeg）

---

## 📝 版本历史

- **1.0.0** (2026-04-10) - 初始版本
  - 支持 WAV/AIFF/AU 格式读写
  - 14 个核心函数
  - 完整测试套件
  - 详细文档和示例

---

## 📄 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 请求新功能
- 改进文档
- 添加新工具函数

---

**Author:** AllToolkit  
**Version:** 1.0.0  
**Last Updated:** 2026-04-10
