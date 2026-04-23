# Signal Processing Utilities - 信号处理工具集

零外部依赖的信号处理工具，纯 Python 标准库实现。

## 功能模块

### 1. 信号生成 🎵
生成各种波形信号：

| 函数 | 功能 | 示例 |
|------|------|------|
| `generate_sine_wave` | 正弦波 | 生成 440Hz 音频信号 |
| `generate_square_wave` | 方波 | 数字信号合成 |
| `generate_triangle_wave` | 三角波 | 音效合成 |
| `generate_sawtooth_wave` | 锯齿波 | 合成器音源 |
| `generate_white_noise` | 白噪声 | 噪声测试 |
| `generate_pulse` | 脉冲信号 | 脉冲响应测试 |
| `generate_chirp` | 扫频信号 | 频率响应测试 |
| `generate_custom_wave` | 自定义波形 | 特殊波形生成 |
| `generate_harmonic_series` | 谐波序列 | 音乐合成 |

### 2. 信号滤波 🔧
基础滤波器：

| 函数 | 功能 | 特点 |
|------|------|------|
| `moving_average_filter` | 移动平均 | 简单有效平滑 |
| `median_filter` | 中值滤波 | 去除脉冲噪声 |
| `exponential_smoothing` | 指数平滑 | 快速响应 |
| `lowpass_filter_simple` | 低通滤波 | 去除高频噪声 |
| `highpass_filter_simple` | 高通滤波 | 去除直流成分 |
| `bandpass_filter_simple` | 带通滤波 | 频率选择 |
| `savitzky_golay_filter` | S-G 滤波 | 保持形状平滑 |
| `notch_filter` | 陷波滤波 | 去除特定频率 |

### 3. 信号变换 🔄
FFT 离散傅里叶变换：

| 函数 | 功能 | 应用 |
|------|------|------|
| `fft` | 快速傅里叶变换 | 频域分析 |
| `ifft` | 傅里叶逆变换 | 信号重构 |
| `fft_magnitude` | 幅度谱 | 频率分量强度 |
| `fft_phase` | 相位谱 | 相位分析 |
| `power_spectrum` | 功率谱 | 能量分布 |
| `frequency_bins` | 频率 bins | 频率映射 |
| `dft` | 离散傅里叶变换 | 教学演示 |

### 4. 信号分析 📊
频率、峰值、能量分析：

| 函数 | 功能 | 输出 |
|------|------|------|
| `find_peaks` | 峰值检测 | 峰值位置列表 |
| `find_valleys` | 谷值检测 | 谷值位置列表 |
| `detect_frequency` | 主频率检测 | 主频率 Hz |
| `detect_multiple_frequencies` | 多频率检测 | (频率,幅度)列表 |
| `calculate_energy` | 能量计算 | 总能量 |
| `calculate_power` | 功率计算 | 平均功率 |
| `calculate_rms` | RMS 计算 | 均方根值 |
| `zero_crossing_rate` | 零交叉率 | 0-1 |
| `signal_statistics` | 统计信息 | 均值、方差等 |
| `autocorrelation` | 自相关 | 相关序列 |
| `cross_correlation` | 互相关 | 相关序列 |
| `spectral_centroid` | 频谱质心 | "亮度"指标 |
| `spectral_bandwidth` | 频谱带宽 | 频谱宽度 |

### 5. 信号操作 ⚙️
卷积、归一化、重采样：

| 函数 | 功能 | 应用 |
|------|------|------|
| `convolve` | 信号卷积 | 滤波、特征提取 |
| `convolve_fft` | FFT 卷积 | 快速卷积 |
| `normalize_signal` | 归一化 | 幅度调整 |
| `normalize_to_range` | 范围归一化 | 值域调整 |
| `resample` | 重采样 | 改变采样率 |
| `interpolate_linear` | 线性插值 | 增加采样点 |
| `decimate` | 抽取 | 减少采样点 |
| `shift_signal` | 时移 | 时间调整 |
| `reverse_signal` | 反转 | 信号反转 |
| `add_signals` | 信号叠加 | 多信号合成 |
| `multiply_signals` | 信号相乘 | 幅度调制 |
| `scale_signal` | 缩放 | 幅度调整 |
| `offset_signal` | 偏移 | 直流偏移 |
| `envelope_detection` | 包络检测 | 振幅包络 |
| `derivative` | 导数 | 变化率 |
| `integral` | 积分 | 累积量 |

### 6. 特殊处理 🎯
窗函数、STFT、频谱图：

| 函数 | 功能 | 应用 |
|------|------|------|
| `window_function` | 窗函数生成 | Hann/Hamming 等 |
| `apply_window` | 应用窗函数 | FFT 预处理 |
| `stft` | 短时傅里叶变换 | 时频分析 |
| `istft` | STFT 逆变换 | 信号重构 |
| `spectrogram` | 频谱图 | 时频可视化 |

### 7. 实用工具 🔨
静音检测、渐变效果：

| 函数 | 功能 | 应用 |
|------|------|------|
| `silence_detection` | 静音检测 | 语音处理 |
| `signal_similarity` | 相似度计算 | 信号比对 |
| `signal_difference` | 差异计算 | 信号对比 |
| `threshold_signal` | 阈值化 | 信号分类 |
| `clip_signal` | 信号裁剪 | 幅度限制 |
| `fade_in` | 渐入效果 | 音频处理 |
| `fade_out` | 渐出效果 | 音频处理 |
| `fade_both` | 渐入渐出 | 音频平滑 |

## 使用示例

### 生成正弦波
```python
from mod import generate_sine_wave, detect_frequency

# 生成 440Hz 正弦波（A4音符）
wave = generate_sine_wave(
    frequency=440,
    duration=1.0,      # 1 秒
    sample_rate=44100, # 标准采样率
    amplitude=0.8,     # 振幅
    phase=0            # 相位
)

print(f"采样点数: {len(wave)}")  # 44100

# 检测主频率
freq = detect_frequency(wave, 44100)
print(f"检测频率: {freq:.1f} Hz")  # ~440 Hz
```

### 信号滤波
```python
from mod import generate_white_noise, moving_average_filter, median_filter

# 生成带噪声的信号
noise = generate_white_noise(0.1, 1000)

# 移动平均滤波（平滑）
smoothed = moving_average_filter(noise, window_size=5)

# 中值滤波（去除脉冲噪声）
filtered = median_filter(noise, window_size=3)

print(f"原始噪声方差: {sum((x-0)**2 for x in noise)/len(noise):.3f}")
print(f"平滑后方差: {sum((x-sum(smoothed)/len(smoothed))**2 for x in smoothed)/len(smoothed):.3f}")
```

### FFT 频域分析
```python
from mod import generate_sine_wave, fft, fft_magnitude, frequency_bins

# 生成复合信号（两个频率）
wave1 = generate_sine_wave(100, 1.0, 1000, amplitude=1.0)
wave2 = generate_sine_wave(250, 1.0, 1000, amplitude=0.5)
combined = [w1 + w2 for w1, w2 in zip(wave1, wave2)]

# FFT 分析
spectrum = fft(combined)
magnitude = fft_magnitude(spectrum)
freq_bins = frequency_bins(len(spectrum), 1000)

# 找最大幅度对应的频率
max_idx = max(range(len(magnitude)//2), key=lambda i: magnitude[i])
print(f"主频率: {freq_bins[max_idx]:.1f} Hz")
print(f"幅度: {magnitude[max_idx]:.2f}")
```

### 峰值检测
```python
from mod import find_peaks

# 信号示例
signal = [1, 3, 2, 5, 3, 7, 4, 2, 6, 3]

# 查找峰值
peaks = find_peaks(signal, min_height=3, min_distance=2)
print(f"峰值位置: {peaks}")
print(f"峰值值: {[signal[p] for p in peaks]}")
```

### 信号卷积
```python
from mod import convolve, convolve_fft

# 两个信号
signal1 = [1, 2, 3, 4, 5]
signal2 = [0.5, 0.5]  # 简单滤波器

# 直接卷积
result = convolve(signal1, signal2)
print(f"卷积结果: {result}")

# FFT 卷积（更快）
result_fft = convolve_fft(signal1, signal2)
print(f"FFT卷积: {result_fft}")
```

### 窗函数应用
```python
from mod import window_function, apply_window, fft

# 生成信号
signal = [1, 2, 3, 4, 5, 6, 7, 8]

# Hann 窗函数
hann_window = window_function(8, 'hann')
print(f"Hann窗: {[f'{x:.3f}' for x in hann_window]}")

# 应用窗函数
windowed = apply_window(signal, 'hann')

# 加窗后 FFT
spectrum = fft(windowed)
```

### STFT 时频分析
```python
from mod import generate_sine_wave, stft, spectrogram

# 生成信号
wave = generate_sine_wave(100, 1.0, 1000)

# STFT 分析
frames = stft(wave, frame_size=256, hop_size=128)
print(f"帧数: {len(frames)}")
print(f"每帧长度: {len(frames[0])}")

# 频谱图
spec = spectrogram(wave, frame_size=256, hop_size=128)
print(f"频谱图维度: {len(spec)} x {len(spec[0])}")
```

### 信号统计
```python
from mod import generate_sine_wave, signal_statistics

wave = generate_sine_wave(440, 1.0, 44100)
stats = signal_statistics(wave)

print(f"均值: {stats['mean']:.4f}")
print(f"方差: {stats['variance']:.4f}")
print(f"标准差: {stats['std']:.4f}")
print(f"RMS: {stats['rms']:.4f}")
print(f"能量: {stats['energy']:.2f}")
print(f"功率: {stats['power']:.4f}")
```

### 渐变效果
```python
from mod import generate_sine_wave, fade_both

# 生成信号
wave = generate_sine_wave(440, 0.5, 44100)

# 应用渐入渐出（100ms）
faded = fade_both(wave, 
                  fade_in_samples=4410,   # 100ms
                  fade_out_samples=4410)

# 验证渐入
print(f"开始值: {faded[0]:.4f} (应接近 0)")
print(f"结束值: {faded[-1]:.4f} (应接近 0)")
```

## 技术特点

### ✅ 零外部依赖
- 纯 Python 标准库实现
- 只使用 `math`, `cmath`, `typing`, `collections`
- 无需安装 numpy, scipy 等重型库

### ✅ 完整 FFT 实现
- Cooley-Tukey 快速傅里叶变换算法
- 支持任意长度信号（自动补零）
- IFFT 逆变换信号重构

### ✅ 多种滤波器
- 时域滤波：移动平均、中值、指数平滑
- S-G 滤波：保持形状的平滑
- 频域滤波：陷波滤波

### ✅ 时频分析
- STFT 短时傅里叶变换
- 频谱图生成
- 多种窗函数支持

## 测试

```bash
cd Python/signal_utils
python signal_utils_test.py
```

测试覆盖：
- ✅ 信号生成（9 个测试）
- ✅ 信号滤波（7 个测试）
- ✅ FFT 变换（7 个测试）
- ✅ 信号分析（12 个测试）
- ✅ 信号操作（16 个测试）
- ✅ 窗函数（2 个测试）
- ✅ STFT（2 个测试）
- ✅ 实用工具（8 个测试）

**总计：63+ 个测试**

## API 设计原则

1. **一致性**：函数命名遵循 `动词_名词` 模式
2. **直观性**：参数名称清晰表达含义
3. **安全性**：边界条件检查，错误提示
4. **灵活性**：可选参数提供默认值

## 应用场景

- 🎵 **音频处理**：信号生成、滤波、分析
- 📊 **数据平滑**：噪声去除、趋势提取
- 🔬 **科学计算**：频域分析、时频分析
- 🤖 **机器学习**：特征提取、预处理
- 📡 **通信系统**：信号调制解调
- ⚡ **电力分析**：谐波分析、功率计算

## 性能说明

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| FFT | O(n log n) | Cooley-Tukey 算法 |
| DFT | O(n²) | 教学用途，小信号 |
| 卷积 | O(n m) | 直接计算 |
| FFT卷积 | O(n log n) | 大信号更快 |
| 移动平均 | O(n) | 滑动窗口 |
| 中值滤波 | O(n k log k) | 每窗口排序 |

## 版本历史

- **v1.0.0 (2026-04-23)**：初始版本
  - 信号生成（9 种波形）
  - 信号滤波（8 种滤波器）
  - FFT 变换（Cooley-Tukey）
  - 信号分析（13 种分析）
  - 信号操作（16 种操作）
  - 窗函数（5 种窗函数）
  - STFT/频谱图
  - 实用工具（8 种工具）

---

**作者**：AllToolkit 自动生成  
**日期**：2026-04-23  
**许可**：MIT License