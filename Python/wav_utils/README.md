# Wav Utils


WAV 音频文件工具集
==================

无依赖的 WAV 音频文件读写和处理工具。

功能：
- WAV 文件读取和解析
- WAV 文件生成和写入
- 音频格式转换
- 音频数据处理（静音检测、归一化、混音等）
- 零外部依赖，仅使用 Python 标准库

作者: AllToolkit 自动生成
日期: 2026-04-22


## 功能

### 类

- **WavFormat**: WAV 音频格式枚举
- **WavInfo**: WAV 文件元信息
  方法: duration, byte_rate, block_align
- **WavReader**: WAV 文件读取器
  方法: read_info, read_samples, read_samples_mono
- **WavWriter**: WAV 文件写入器
  方法: add_samples, add_silence, add_sine_wave, write
- **WavProcessor**: WAV 音频处理器
  方法: normalize, amplify, find_silence, trim_silence, mix ... (9 个方法)

### 函数

- **read_wav(filepath**) - 读取 WAV 文件
- **write_wav(filepath, samples, sample_rate**, ...) - 写入 WAV 文件
- **get_wav_info(filepath**) - 获取 WAV 文件信息
- **create_sine_wav(filepath, frequency, duration_ms**, ...) - 创建正弦波 WAV 文件
- **duration(self**) - 音频时长（秒）
- **byte_rate(self**) - 字节率
- **block_align(self**) - 块对齐
- **read_info(self**) - 读取 WAV 文件信息
- **read_samples(self**) - 读取所有音频样本
- **read_samples_mono(self**) - 读取单声道样本（多声道自动混合）

... 共 23 个函数

## 使用示例

```python
from mod import read_wav

# 使用 read_wav
result = read_wav()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
