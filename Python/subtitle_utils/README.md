# Subtitle Utils 📝

字幕文件处理工具，支持 SRT、VTT 等格式的解析、编辑、合并。

## 特性

- ✅ **格式解析** - SRT、VTT 字幕解析
- ✅ **时间轴调整** - 延迟/提前字幕时间
- ✅ **字幕合并** - 合并多个字幕文件
- ✅ **字幕分割** - 按时间或行数分割
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from subtitle_utils import Subtitle, SubtitleFile

# 解析 SRT
sub = SubtitleFile.from_srt("movie.srt")
for cue in sub.cues:
    print(f"{cue.start} --> {cue.end}")
    print(cue.text)

# 时间轴调整
sub.shift_time(seconds=5)  # 延迟 5 秒

# 保存
sub.to_srt("movie_shifted.srt")
```
