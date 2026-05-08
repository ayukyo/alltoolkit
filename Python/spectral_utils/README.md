# Spectral Utils - 频谱分析工具

零依赖的信号频谱分析库，支持 FFT、功率谱计算、信号滤波等功能。

## 功能特性

- **快速傅里叶变换 (FFT)** - Cooley-Tukey 算法实现
- **频谱分析** - 幅值、相位、功率谱计算
- **峰值检测** - 自动检测频谱中的主要频率分量
- **信号滤波** - 低通、高通、带通、带阻滤波器
- **时频分析** - 短时傅里叶变换 (STFT)、频谱图
- **窗函数** - 支持多种窗函数减少频谱泄漏

## 快速开始

### 基础频谱分析

```python
from spectral_utils.mod import (
    generate_sine_wave,
    compute_spectrum,
    find_peaks
)

# 生成测试信号 (100Hz 正弦波)
signal = generate_sine_wave(100.0, sample_rate=1000.0, duration=1.0)

# 计算频谱
spectrum = compute_spectrum(signal, sample_rate=1000.0)

# 检测峰值频率
peaks = find_peaks(spectrum, threshold=0.1)
for peak in peaks:
    print(f"频率: {peak.frequency}Hz, 幅值: {peak.magnitude}")
```

### 主频率检测

```python
from spectral_utils.mod import detect_dominant_frequency

# 复合信号：包含多个频率分量
signal = generate_composite_wave(
    frequencies=[50, 120, 300],
    amplitudes=[1.0, 0.7, 0.3],
    sample_rate=1000.0,
    duration=1.0
)

# 自动检测主频率
dominant = detect_dominant_frequency(signal, sample_rate=1000.0)
print(f"主频率: {dominant}Hz")  # 输出: 50.0Hz
```

### 信号滤波

```python
from spectral_utils.mod import (
    low_pass_filter,
    high_pass_filter,
    band_pass_filter
)

# 低通滤波 (截止频率 100Hz)
filtered = low_pass_filter(signal, sample_rate=1000.0, cutoff_frequency=100.0)

# 高通滤波
filtered = high_pass_filter(signal, sample_rate=1000.0, cutoff_frequency=100.0)

# 带通滤波 (保留 80-120Hz)
filtered = band_pass_filter(
    signal,
    sample_rate=1000.0,
    low_cutoff=80.0,
    high_cutoff=120.0
)
```

### 时频分析

```python
from spectral_utils.mod import compute_spectrogram

# 计算频谱图
times, frequencies, spectrogram = compute_spectrogram(
    signal,
    window_size=256,
    hop_size=128,
    sample_rate=1000.0
)

# spectrogram 是一个二维矩阵，可用于可视化
```

## API 参考

### FFT 相关

#### `fft(signal) -> List[Tuple[float, float]]`
快速傅里叶变换，返回复数频谱。

#### `ifft(spectrum) -> List[float]`
逆傅里叶变换，重建时域信号。

### 频谱分析

#### `compute_spectrum(signal, sample_rate, window) -> SpectrumResult`
计算完整频谱，包含：
- `frequencies` - 频率数组
- `magnitudes` - 幅值数组
- `phases` - 相位数组
- `power_spectrum` - 功率谱

#### `find_peaks(spectrum, threshold, min_distance, max_peaks) -> List[PeakInfo]`
检测频谱峰值，返回峰值频率、幅值、相位等信息。

#### `detect_dominant_frequency(signal, sample_rate) -> Optional[float]`
自动检测信号的主频率。

### 滤波器

#### `low_pass_filter(signal, sample_rate, cutoff_frequency, order) -> List[float]`
低通滤波器。

#### `high_pass_filter(signal, sample_rate, cutoff_frequency, order) -> List[float]`
高通滤波器。

#### `band_pass_filter(signal, sample_rate, low_cutoff, high_cutoff, order) -> List[float]`
带通滤波器。

#### `band_stop_filter(signal, sample_rate, low_cutoff, high_cutoff, order) -> List[float]`
带阻滤波器（陷波滤波器）。

### 窗函数

#### `apply_window(signal, window_type) -> List[float]`
对信号应用窗函数。支持的窗函数类型：
- `RECTANGULAR` - 矩形窗
- `HANN` - 汉宁窗（推荐）
- `HAMMING` - 汉明窗
- `BLACKMAN` - 布莱克曼窗
- `BARTLETT` - 巴特利特窗

### 信号生成

#### `generate_sine_wave(frequency, sample_rate, duration, amplitude, phase) -> List[float]`
生成正弦波。

#### `generate_composite_wave(frequencies, amplitudes, sample_rate, duration, phases) -> List[float]`
生成多频率复合波。

### 工具函数

#### `compute_rms(signal) -> float`
计算信号的均方根值。

#### `normalize_signal(signal, target_rms) -> List[float]`
归一化信号到指定 RMS。

## 算法说明

### FFT 实现
采用 Cooley-Tukey 算法，时间复杂度 O(N log N)。信号自动补零到 2 的幂次长度以提高效率。

### 滤波器
采用简单 RC 滤波器设计，支持多级串联提高滤波效果。适合教学和简单应用，不依赖外部库。

### 窗函数
窗函数用于减少 FFT 的频谱泄漏。汉宁窗是通用场景的推荐选择。

## 应用场景

- 音频信号分析
- 振动信号处理
- 通信信号分析
- 生物医学信号处理（EEG、ECG）
- 机械故障诊断
- 科学计算和教学

## 注意事项

1. **采样定理**：采样率应至少为信号最高频率的 2 倍（奈奎斯特频率）
2. **频率分辨率**：频率分辨率 = 采样率 / FFT 长度
3. **窗函数选择**：不同窗函数有不同的频率分辨率和幅值精度平衡
4. **滤波器延迟**：RC 滤波器会引入相位延迟

## 测试

运行测试套件：

```bash
python spectral_utils_test.py
```

## 许可证

MIT License

## 作者

AllToolkit