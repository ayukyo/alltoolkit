# FFT Utils - 快速傅里叶变换工具库

零外部依赖的 Python FFT 工具库，提供完整的频域分析功能。

## 功能特性

### 核心 FFT 算法
- **FFT (快速傅里叶变换)** - Cooley-Tukey 迭代算法，O(n log n) 时间复杂度
- **IFFT (逆快速傅里叶变换)** - 快速重建原始信号
- **DFT/IDFT (离散傅里叶变换)** - O(n²) 算法，用于验证和小数据集
- **RFFT/IRFFT (实数 FFT)** - 针对实数信号优化，只计算正频率部分

### 窗函数
- 矩形窗 (Rectangular)
- 汉宁窗 (Hanning)
- 汉明窗 (Hamming)
- 布莱克曼窗 (Blackman)
- 巴特利特窗 (Bartlett/Triangular)
- 凯撒窗 (Kaiser) - 可调参数 β

### 频谱分析
- 幅度谱计算
- 相位谱计算
- 功率谱计算
- 功率谱密度 (PSD) 计算
- 频率 bin 计算
- 完整频谱分析 (`analyze_spectrum`)

### 峰值检测
- 频谱峰值检测
- 谐波检测
- 支持最小高度和最小间距参数

### 信号处理
- 卷积计算 (FFT 方法)
- 互相关计算
- 自相关计算

### 信号生成
- 正弦波生成
- 余弦波生成
- 线性扫频信号 (Chirp)

### 工具函数
- 零填充
- DC 偏移计算与移除
- 信号重采样
- 信号归一化

## 安装使用

无需安装，直接导入模块：

```python
from mod import fft, ifft, rfft, irfft
from mod import analyze_spectrum, WindowType
from mod import generate_sine, convolve, find_peaks
```

## 快速开始

### 基本 FFT 使用

```python
from mod import fft, ifft, magnitude_spectrum

# 生成信号
import math
sample_rate = 1000
signal = [math.sin(2 * math.pi * 50 * i / sample_rate) for i in range(256)]

# 执行 FFT
spectrum = fft(signal, zero_pad=True)

# 计算幅度谱
mags = magnitude_spectrum(spectrum)

# 找峰值频率
peak_idx = mags.index(max(mags))
peak_freq = peak_idx * sample_rate / len(signal)
print(f"峰值频率: {peak_freq} Hz")

# IFFT 重建
reconstructed = ifft(spectrum)
```

### 频谱分析

```python
from mod import analyze_spectrum, WindowType

# 分析信号
result = analyze_spectrum(
    signal,
    sample_rate=1000,
    window_type=WindowType.HANNING,
    detect_peaks=True
)

print(f"峰值频率: {result.peak_frequency} Hz")
print(f"峰值幅度: {result.peak_magnitude}")

# 查看频率和幅度
for freq, mag in zip(result.frequencies[:10], result.magnitudes[:10]):
    print(f"{freq:.1f} Hz: {mag:.4f}")
```

### 窗函数

```python
from mod import get_window, apply_window, WindowType

# 获取窗函数
window = get_window(WindowType.HAMMING, 256)

# 对信号应用窗函数
windowed_signal = apply_window(signal, WindowType.BLACKMAN)

# 凯撒窗 (可调参数)
kaiser_window = get_window(WindowType.KAISER, 256, beta=8.6)
```

### 峰值检测

```python
from mod import find_peaks, find_harmonics

# 在频谱中找峰值
peaks = find_peaks(
    spectrum=result.magnitudes,
    frequencies=result.frequencies,
    min_height=0.1,
    min_distance=5
)

for freq, mag in sorted(peaks, key=lambda x: x[1], reverse=True)[:5]:
    print(f"峰值: {freq:.1f} Hz, 幅度: {mag:.4f}")

# 检测谐波
harmonics = find_harmonics(
    fundamental_freq=50.0,
    max_harmonic=5,
    frequencies=result.frequencies,
    spectrum=result.magnitudes
)

for n, freq, mag in harmonics:
    print(f"第 {n} 次谐波: {freq:.1f} Hz")
```

### 卷积与相关性

```python
from mod import convolve, correlate, autocorrelate

# 线性卷积
result = convolve(signal1, signal2)

# 互相关
result = correlate(signal1, signal2)

# 自相关
result = autocorrelate(signal)
```

### 信号生成

```python
from mod import generate_sine, generate_cosine, generate_chirp

# 正弦波
sine = generate_sine(frequency=440, sample_rate=44100, duration=1.0, amplitude=0.5)

# 余弦波
cosine = generate_cosine(frequency=440, sample_rate=44100, duration=1.0)

# 扫频信号
chirp = generate_chirp(start_freq=20, end_freq=2000, sample_rate=44100, duration=2.0)
```

### 实数信号优化

```python
from mod import rfft, irfft, compute_frequencies_rfft

# 对于实数信号，使用 RFFT 更高效
spectrum = rfft(real_signal)  # 只返回正频率部分

# 获取频率轴
frequencies = compute_frequencies_rfft(len(real_signal), sample_rate=1000)

# 重建信号
reconstructed = irfft(spectrum)
```

## 算法说明

### FFT 实现
采用经典的 Cooley-Tukey 迭代算法：
1. 位反转排列输入
2. 蝶形运算迭代合并
3. 时间复杂度 O(n log n)

### 窗函数选择

| 窗函数 | 主瓣宽度 | 旁瓣衰减 | 适用场景 |
|--------|----------|----------|----------|
| Rectangular | 最窄 | -13 dB | 瞬态信号 |
| Hanning | 中等 | -31 dB | 通用频谱分析 |
| Hamming | 中等 | -42 dB | 语音处理 |
| Blackman | 较宽 | -58 dB | 高精度分析 |
| Bartlett | 中等 | -26 dB | 图像处理 |
| Kaiser | 可调 | 可调 | 需要权衡的场景 |

## 测试

运行测试：

```bash
python -m pytest fft_utils_test.py -v
```

或直接运行模块：

```bash
python mod.py
```

## 应用场景

- 音频信号处理
- 振动分析
- 通信系统
- 图像处理
- 控制系统
- 医学信号处理 (ECG, EEG)
- 地震数据分析
- 语音识别
- 音乐信息检索
- 雷达信号处理

## 依赖

纯 Python 标准库实现，无外部依赖。

## 版本历史

- v1.0.0 (2026-05-29): 初始版本
  - FFT/IFFT/DFT/IDFT 核心算法
  - RFFT/IRFFT 实数优化
  - 6 种窗函数
  - 完整频谱分析功能
  - 峰值和谐波检测
  - 卷积和相关性计算
  - 信号生成和工具函数
  - 100+ 单元测试

## 许可证

MIT License