"""
FFT Utils - 快速傅里叶变换工具库

功能:
- FFT (快速傅里叶变换, Cooley-Tukey 算法)
- IFFT (逆快速傅里叶变换)
- DFT/IDFT (离散傅里叶变换, 用于验证和小数据集)
- 频谱分析: 幅度谱、相位谱、功率谱密度
- 窗函数: Hamming, Hanning, Blackman, Bartlett, Kaiser
- 实数 FFT (RFFT/IRFFT) 优化
- 频率 bin 计算
- 频谱峰值检测
- 卷积和相关性分析
- 零填充和插值

零外部依赖, 纯 Python 标准库实现

作者: AllToolkit 自动化生成
日期: 2026-05-29
"""

import math
from typing import List, Tuple, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum


class WindowType(Enum):
    """窗函数类型"""
    RECTANGULAR = "rectangular"
    HANNING = "hanning"
    HAMMING = "hamming"
    BLACKMAN = "blackman"
    BARTLETT = "bartlett"
    KAISER = "kaiser"


@dataclass
class SpectrumResult:
    """频谱分析结果"""
    frequencies: List[float]          # 频率 (Hz)
    magnitudes: List[float]            # 幅度谱
    phases: List[float]                # 相位谱 (弧度)
    power_spectrum: List[float]        # 功率谱
    power_density: List[float]         # 功率谱密度
    peak_frequency: Optional[float]    # 峰值频率
    peak_magnitude: Optional[float]     # 峰值幅度


# ============================================================
# 复数运算辅助函数
# ============================================================

def _complex_multiply(a: complex, b: complex) -> complex:
    """复数乘法"""
    return a * b


def _complex_exp(angle: float) -> complex:
    """欧拉公式: e^(i*angle) = cos(angle) + i*sin(angle)"""
    return complex(math.cos(angle), math.sin(angle))


def _next_power_of_two(n: int) -> int:
    """计算大于等于 n 的最小 2 的幂"""
    if n <= 0:
        return 1
    power = 1
    while power < n:
        power <<= 1
    return power


def _bit_reverse(n: int, bits: int) -> int:
    """位反转"""
    result = 0
    for _ in range(bits):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# ============================================================
# DFT - 离散傅里叶变换 (O(n^2), 用于验证和小数据集)
# ============================================================

def dft(signal: List[Union[float, complex]]) -> List[complex]:
    """
    离散傅里叶变换 (DFT)
    
    时间复杂度: O(n^2)
    空间复杂度: O(n)
    
    Args:
        signal: 输入信号序列
        
    Returns:
        频域复数序列
    """
    n = len(signal)
    if n == 0:
        return []
    
    result = []
    for k in range(n):
        total = complex(0, 0)
        for j in range(n):
            angle = -2 * math.pi * k * j / n
            total += signal[j] * _complex_exp(angle)
        result.append(total)
    
    return result


def idft(spectrum: List[complex]) -> List[complex]:
    """
    逆离散傅里叶变换 (IDFT)
    
    时间复杂度: O(n^2)
    空间复杂度: O(n)
    
    Args:
        spectrum: 频域复数序列
        
    Returns:
        时域复数序列
    """
    n = len(spectrum)
    if n == 0:
        return []
    
    result = []
    for j in range(n):
        total = complex(0, 0)
        for k in range(n):
            angle = 2 * math.pi * k * j / n
            total += spectrum[k] * _complex_exp(angle)
        result.append(total / n)
    
    return result


# ============================================================
# FFT - 快速傅里叶变换 (Cooley-Tukey 算法)
# ============================================================

def fft(signal: List[Union[float, complex]], zero_pad: bool = False) -> List[complex]:
    """
    快速傅里叶变换 (FFT) - Cooley-Tukey 迭代实现
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    
    要求输入长度为 2 的幂次方，否则自动零填充
    
    Args:
        signal: 输入信号序列
        zero_pad: 是否零填充到 2 的幂次方
        
    Returns:
        频域复数序列
    """
    n = len(signal)
    if n == 0:
        return []
    
    # 如果不是 2 的幂次方，零填充
    if n & (n - 1) != 0:
        if zero_pad:
            new_n = _next_power_of_two(n)
            signal = list(signal) + [complex(0, 0)] * (new_n - n)
            n = new_n
        else:
            # 对于非 2 的幂次方，使用 DFT
            return dft(signal)
    
    # 位反转排列
    bits = n.bit_length() - 1
    result = [complex(0, 0)] * n
    for i in range(n):
        result[_bit_reverse(i, bits)] = complex(signal[i]) if isinstance(signal[i], float) else signal[i]
    
    # Cooley-Tukey 迭代 FFT
    length = 2
    while length <= n:
        half_length = length // 2
        angle_step = -2 * math.pi / length
        
        for i in range(0, n, length):
            for j in range(half_length):
                twiddle = _complex_exp(angle_step * j)
                idx1 = i + j
                idx2 = i + j + half_length
                
                temp = result[idx2] * twiddle
                result[idx2] = result[idx1] - temp
                result[idx1] = result[idx1] + temp
        
        length <<= 1
    
    return result


def ifft(spectrum: List[complex]) -> List[complex]:
    """
    逆快速傅里叶变换 (IFFT)
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    
    Args:
        spectrum: 频域复数序列
        
    Returns:
        时域复数序列
    """
    n = len(spectrum)
    if n == 0:
        return []
    
    # 共轭 -> FFT -> 共轭 -> 归一化
    conjugated = [x.conjugate() for x in spectrum]
    result = fft(conjugated, zero_pad=True)
    return [x.conjugate() / n for x in result]


# ============================================================
# 实数 FFT 优化 (RFFT/IRFFT)
# ============================================================

def rfft(signal: List[float]) -> List[complex]:
    """
    实数快速傅里叶变换 (RFFT)
    
    利用在实数信号的对称性，只计算 n//2 + 1 个频点
    
    Args:
        signal: 实数信号序列
        
    Returns:
        频域复数序列 (长度为 n//2 + 1)
    """
    n = len(signal)
    if n == 0:
        return []
    
    # 对于实数信号，使用标准 FFT
    full_spectrum = fft(signal, zero_pad=True)
    
    # 实数信号的频谱是共轭对称的，只需返回前一半
    return full_spectrum[:n // 2 + 1]


def irfft(spectrum: List[complex], n: Optional[int] = None) -> List[float]:
    """
    逆实数快速傅里叶变换 (IRFFT)
    
    从半边频谱恢复实数信号
    
    Args:
        spectrum: 半边频域复数序列
        n: 输出信号长度
        
    Returns:
        时域实数序列
    """
    m = len(spectrum)
    if m == 0:
        return []
    
    if n is None:
        n = (m - 1) * 2
    
    # 重建完整频谱
    full_spectrum = list(spectrum)
    
    # 添加共轭对称部分
    if n % 2 == 0:
        # 偶数长度: DC 和 Nyquist 频点是实数
        for i in range(m - 2, 0, -1):
            full_spectrum.append(full_spectrum[i].conjugate())
    else:
        # 奇数长度: 只有 DC 频点是实数
        for i in range(m - 1, 0, -1):
            full_spectrum.append(full_spectrum[i].conjugate())
    
    # 执行 IFFT
    result = ifft(full_spectrum)
    return [x.real for x in result]


# ============================================================
# 窗函数
# ============================================================

def rectangular_window(n: int) -> List[float]:
    """矩形窗 (无窗)"""
    return [1.0] * n


def hanning_window(n: int) -> List[float]:
    """汉宁窗 (Hanning Window)"""
    return [0.5 * (1 - math.cos(2 * math.pi * i / (n - 1))) for i in range(n)]


def hamming_window(n: int) -> List[float]:
    """汉明窗 (Hamming Window)"""
    return [0.54 - 0.46 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]


def blackman_window(n: int) -> List[float]:
    """布莱克曼窗 (Blackman Window)"""
    return [0.42 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) + 
            0.08 * math.cos(4 * math.pi * i / (n - 1)) for i in range(n)]


def bartlett_window(n: int) -> List[float]:
    """巴特利特窗 (Bartlett/Triangular Window)"""
    half = (n - 1) / 2
    return [1 - abs(i - half) / half for i in range(n)]


def kaiser_window(n: int, beta: float = 5.0) -> List[float]:
    """
    凯撒窗 (Kaiser Window)
    
    Args:
        n: 窗长度
        beta: 形状参数，控制旁瓣衰减
              beta=0: 矩形窗
              beta=5: 类似 Hamming
              beta=6: 类似 Hanning
              beta=8.6: 类似 Blackman
    """
    def bessel_i0(x: float) -> float:
        """零阶第一类修正贝塞尔函数"""
        result = 1.0
        term = 1.0
        for k in range(1, 50):
            term *= (x / (2 * k)) ** 2
            result += term
            if term < 1e-10:
                break
        return result
    
    denominator = bessel_i0(beta)
    half = (n - 1) / 2
    return [bessel_i0(beta * math.sqrt(1 - ((i - half) / half) ** 2)) / denominator 
            for i in range(n)]


def get_window(window_type: WindowType, n: int, **kwargs) -> List[float]:
    """
    获取指定类型的窗函数
    
    Args:
        window_type: 窗函数类型
        n: 窗长度
        **kwargs: 窗函数参数 (如 Kaiser 窗的 beta)
        
    Returns:
        窗函数系数列表
    """
    if window_type == WindowType.RECTANGULAR:
        return rectangular_window(n)
    elif window_type == WindowType.HANNING:
        return hanning_window(n)
    elif window_type == WindowType.HAMMING:
        return hamming_window(n)
    elif window_type == WindowType.BLACKMAN:
        return blackman_window(n)
    elif window_type == WindowType.BARTLETT:
        return bartlett_window(n)
    elif window_type == WindowType.KAISER:
        beta = kwargs.get('beta', 5.0)
        return kaiser_window(n, beta)
    else:
        raise ValueError(f"Unknown window type: {window_type}")


def apply_window(signal: List[float], window_type: WindowType, **kwargs) -> List[float]:
    """
    对信号应用窗函数
    
    Args:
        signal: 输入信号
        window_type: 窗函数类型
        **kwargs: 窗函数参数
        
    Returns:
        加窗后的信号
    """
    window = get_window(window_type, len(signal), **kwargs)
    return [s * w for s, w in zip(signal, window)]


# ============================================================
# 频谱分析
# ============================================================

def compute_frequencies(n: int, sample_rate: float) -> List[float]:
    """
    计算 FFT 频率 bin
    
    Args:
        n: FFT 长度
        sample_rate: 采样率 (Hz)
        
    Returns:
        频率列表 (Hz)
    """
    freq_resolution = sample_rate / n
    return [i * freq_resolution for i in range(n)]


def compute_frequencies_rfft(n: int, sample_rate: float) -> List[float]:
    """
    计算 RFFT 频率 bin (只返回正频率部分)
    
    Args:
        n: 原始信号长度
        sample_rate: 采样率 (Hz)
        
    Returns:
        频率列表 (Hz), 长度为 n//2 + 1
    """
    freq_resolution = sample_rate / n
    return [i * freq_resolution for i in range(n // 2 + 1)]


def magnitude_spectrum(spectrum: List[complex], normalize: bool = True) -> List[float]:
    """
    计算幅度谱
    
    Args:
        spectrum: FFT 结果
        normalize: 是否归一化 (除以长度)
        
    Returns:
        幅度谱
    """
    n = len(spectrum)
    factor = 2 / n if normalize else 1
    return [abs(x) * factor for x in spectrum]


def phase_spectrum(spectrum: List[complex]) -> List[float]:
    """
    计算相位谱 (弧度)
    
    Args:
        spectrum: FFT 结果
        
    Returns:
        相位谱 (弧度)
    """
    return [math.atan2(x.imag, x.real) for x in spectrum]


def power_spectrum(spectrum: List[complex], normalize: bool = True) -> List[float]:
    """
    计算功率谱
    
    Args:
        spectrum: FFT 结果
        normalize: 是否归一化
        
    Returns:
        功率谱
    """
    mags = magnitude_spectrum(spectrum, normalize=False)
    if normalize:
        n = len(spectrum)
        factor = 2 / n
        return [(m * factor) ** 2 for m in mags]
    return [m ** 2 for m in mags]


def power_spectral_density(spectrum: List[complex], sample_rate: float) -> List[float]:
    """
    计算功率谱密度 (PSD)
    
    Args:
        spectrum: FFT 结果
        sample_rate: 采样率 (Hz)
        
    Returns:
        功率谱密度 (单位: V^2/Hz)
    """
    n = len(spectrum)
    freq_resolution = sample_rate / n
    mags = magnitude_spectrum(spectrum, normalize=False)
    return [(m ** 2) / (n * freq_resolution) for m in mags]


def analyze_spectrum(signal: List[float], sample_rate: float, 
                    window_type: WindowType = WindowType.HANNING,
                    detect_peaks: bool = True,
                    peak_threshold_db: float = -40.0) -> SpectrumResult:
    """
    频谱分析
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        window_type: 窗函数类型
        detect_peaks: 是否检测峰值频率
        peak_threshold_db: 峰值检测阈值 (dB)
        
    Returns:
        SpectrumResult 包含完整的频谱分析结果
    """
    n = len(signal)
    
    # 应用窗函数
    windowed_signal = apply_window(signal, window_type)
    
    # 执行 RFFT
    spectrum = rfft(windowed_signal)
    
    # 计算频率
    frequencies = compute_frequencies_rfft(n, sample_rate)
    
    # 计算幅度谱、相位谱、功率谱
    mags = magnitude_spectrum(spectrum)
    phases = phase_spectrum(spectrum)
    power = power_spectrum(spectrum)
    psd = power_spectral_density(spectrum, sample_rate)
    
    # 检测峰值
    peak_freq = None
    peak_mag = None
    
    if detect_peaks and mags:
        # 转换为 dB
        mags_db = [20 * math.log10(m + 1e-10) for m in mags]
        
        # 找最大值
        max_idx = mags.index(max(mags))
        if mags_db[max_idx] > peak_threshold_db:
            peak_freq = frequencies[max_idx]
            peak_mag = mags[max_idx]
    
    return SpectrumResult(
        frequencies=frequencies,
        magnitudes=mags,
        phases=phases,
        power_spectrum=power,
        power_density=psd,
        peak_frequency=peak_freq,
        peak_magnitude=peak_mag
    )


# ============================================================
# 峰值检测
# ============================================================

def find_peaks(spectrum: List[float], frequencies: List[float],
               min_height: float = 0.0, min_distance: int = 1) -> List[Tuple[float, float]]:
    """
    在频谱中查找峰值
    
    Args:
        spectrum: 幅度谱或功率谱
        frequencies: 对应的频率列表
        min_height: 最小峰值高度
        min_distance: 峰值之间的最小距离 (bin 数)
        
    Returns:
        峰值列表 [(频率, 幅度), ...]
    """
    if len(spectrum) != len(frequencies):
        raise ValueError("Spectrum and frequencies must have the same length")
    
    n = len(spectrum)
    peaks = []
    
    # 找所有局部最大值
    for i in range(n):
        if spectrum[i] < min_height:
            continue
        
        is_peak = True
        # 检查邻域
        for j in range(max(0, i - min_distance), min(n, i + min_distance + 1)):
            if j != i and spectrum[j] >= spectrum[i]:
                is_peak = False
                break
        
        if is_peak:
            peaks.append((frequencies[i], spectrum[i]))
    
    return peaks


def find_harmonics(fundamental_freq: float, max_harmonic: int, 
                   frequencies: List[float], spectrum: List[float],
                   tolerance: float = 0.05) -> List[Tuple[int, float, float]]:
    """
    查找谐波成分
    
    Args:
        fundamental_freq: 基频
        max_harmonic: 最大谐波次数
        frequencies: 频率列表
        spectrum: 幅度谱
        tolerance: 频率容差 (相对值)
        
    Returns:
        谐波列表 [(谐波次数, 频率, 幅度), ...]
    """
    harmonics = []
    freq_resolution = frequencies[1] - frequencies[0] if len(frequencies) > 1 else 1
    
    for h in range(1, max_harmonic + 1):
        target_freq = fundamental_freq * h
        freq_tolerance = target_freq * tolerance
        
        # 在容差范围内搜索最大值
        candidates = []
        for i, f in enumerate(frequencies):
            if abs(f - target_freq) <= freq_tolerance:
                candidates.append((f, spectrum[i]))
        
        if candidates:
            best = max(candidates, key=lambda x: x[1])
            harmonics.append((h, best[0], best[1]))
    
    return harmonics


# ============================================================
# 卷积和相关性
# ============================================================

def convolve(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    使用 FFT 计算线性卷积
    
    Args:
        signal1: 信号 1
        signal2: 信号 2
        
    Returns:
        卷积结果
    """
    n1, n2 = len(signal1), len(signal2)
    n = n1 + n2 - 1
    
    # 零填充到合适长度
    n_fft = _next_power_of_two(n)
    
    # FFT
    fft1 = fft(list(signal1) + [0] * (n_fft - n1), zero_pad=False)
    fft2 = fft(list(signal2) + [0] * (n_fft - n2), zero_pad=False)
    
    # 频域相乘
    product = [a * b for a, b in zip(fft1, fft2)]
    
    # IFFT
    result = ifft(product)
    
    # 取前 n 个点
    return [x.real for x in result[:n]]


def correlate(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    使用 FFT 计算互相关
    
    Args:
        signal1: 信号 1
        signal2: 信号 2
        
    Returns:
        互相关结果
    """
    # 相关等价于 signal1 与反转的 signal2 卷积
    signal2_reversed = list(reversed(signal2))
    return convolve(signal1, signal2_reversed)


def autocorrelate(signal: List[float]) -> List[float]:
    """
    计算自相关
    
    Args:
        signal: 输入信号
        
    Returns:
        自相关结果
    """
    return correlate(signal, signal)


# ============================================================
# 信号生成
# ============================================================

def generate_sine(frequency: float, sample_rate: float, duration: float,
                  amplitude: float = 1.0, phase: float = 0.0) -> List[float]:
    """
    生成正弦波
    
    Args:
        frequency: 频率 (Hz)
        sample_rate: 采样率 (Hz)
        duration: 持续时间 (秒)
        amplitude: 振幅
        phase: 初始相位 (弧度)
        
    Returns:
        正弦波信号
    """
    n = int(sample_rate * duration)
    t = [i / sample_rate for i in range(n)]
    return [amplitude * math.sin(2 * math.pi * frequency * ti + phase) for ti in t]


def generate_cosine(frequency: float, sample_rate: float, duration: float,
                    amplitude: float = 1.0, phase: float = 0.0) -> List[float]:
    """
    生成余弦波
    
    Args:
        frequency: 频率 (Hz)
        sample_rate: 采样率 (Hz)
        duration: 持续时间 (秒)
        amplitude: 振幅
        phase: 初始相位 (弧度)
        
    Returns:
        余弦波信号
    """
    n = int(sample_rate * duration)
    t = [i / sample_rate for i in range(n)]
    return [amplitude * math.cos(2 * math.pi * frequency * ti + phase) for ti in t]


def generate_chirp(start_freq: float, end_freq: float, sample_rate: float,
                   duration: float, amplitude: float = 1.0) -> List[float]:
    """
    生成线性扫频信号 (Chirp)
    
    Args:
        start_freq: 起始频率 (Hz)
        end_freq: 结束频率 (Hz)
        sample_rate: 采样率 (Hz)
        duration: 持续时间 (秒)
        amplitude: 振幅
        
    Returns:
        扫频信号
    """
    n = int(sample_rate * duration)
    t = [i / sample_rate for i in range(n)]
    
    # 线性扫频: 瞬时频率线性变化
    k = (end_freq - start_freq) / duration
    return [amplitude * math.sin(2 * math.pi * (start_freq * ti + 0.5 * k * ti ** 2)) 
            for ti in t]


# ============================================================
# 工具函数
# ============================================================

def zero_pad(signal: List[float], target_length: int) -> List[float]:
    """
    零填充信号到指定长度
    
    Args:
        signal: 输入信号
        target_length: 目标长度
        
    Returns:
        零填充后的信号
    """
    if len(signal) >= target_length:
        return list(signal)
    return list(signal) + [0.0] * (target_length - len(signal))


def pad_to_power_of_two(signal: List[float]) -> List[float]:
    """
    零填充信号到最近的 2 的幂次方长度
    
    Args:
        signal: 输入信号
        
    Returns:
        零填充后的信号
    """
    return zero_pad(signal, _next_power_of_two(len(signal)))


def dc_offset(signal: List[float]) -> float:
    """
    计算 DC 偏移量 (直流分量)
    
    Args:
        signal: 输入信号
        
    Returns:
        DC 偏移量
    """
    return sum(signal) / len(signal) if signal else 0.0


def remove_dc(signal: List[float]) -> List[float]:
    """
    移除 DC 偏移
    
    Args:
        signal: 输入信号
        
    Returns:
        去除 DC 后的信号
    """
    offset = dc_offset(signal)
    return [s - offset for s in signal]


def resample(signal: List[float], original_rate: float, target_rate: float) -> List[float]:
    """
    重采样信号
    
    简单实现，使用线性插值
    
    Args:
        signal: 输入信号
        original_rate: 原始采样率
        target_rate: 目标采样率
        
    Returns:
        重采样后的信号
    """
    ratio = target_rate / original_rate
    n_original = len(signal)
    n_target = int(n_original * ratio)
    
    result = []
    for i in range(n_target):
        orig_idx = i / ratio
        idx_floor = int(orig_idx)
        idx_ceil = min(idx_floor + 1, n_original - 1)
        frac = orig_idx - idx_floor
        result.append(signal[idx_floor] * (1 - frac) + signal[idx_ceil] * frac)
    
    return result


def normalize_signal(signal: List[float], target_max: float = 1.0) -> List[float]:
    """
    归一化信号
    
    Args:
        signal: 输入信号
        target_max: 目标最大幅度
        
    Returns:
        归一化后的信号
    """
    max_val = max(abs(s) for s in signal) if signal else 1.0
    if max_val == 0:
        return list(signal)
    scale = target_max / max_val
    return [s * scale for s in signal]


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    print("FFT Utils 测试")
    print("=" * 50)
    
    # 生成测试信号: 两个正弦波叠加
    sample_rate = 1000.0
    duration = 1.0
    freq1, freq2 = 50.0, 120.0
    
    t = [i / sample_rate for i in range(int(sample_rate * duration))]
    signal = [math.sin(2 * math.pi * freq1 * ti) + 0.5 * math.sin(2 * math.pi * freq2 * ti) 
              for ti in t]
    
    print(f"\n测试信号: {freq1}Hz + {freq2}Hz 正弦波")
    print(f"采样率: {sample_rate}Hz")
    print(f"信号长度: {len(signal)}")
    
    # 测试 FFT
    spectrum = fft(signal, zero_pad=True)
    print(f"\nFFT 结果长度: {len(spectrum)}")
    
    # 频谱分析
    result = analyze_spectrum(signal, sample_rate, WindowType.HANNING)
    print(f"\n频谱分析结果:")
    print(f"峰值频率: {result.peak_frequency:.2f} Hz")
    print(f"峰值幅度: {result.peak_magnitude:.4f}")
    
    # 查找前 5 个峰值
    peaks = find_peaks(result.magnitudes, result.frequencies, min_height=0.1, min_distance=5)
    peaks.sort(key=lambda x: x[1], reverse=True)
    print(f"\n前 5 个峰值:")
    for freq, mag in peaks[:5]:
        print(f"  {freq:.2f} Hz: {mag:.4f}")
    
    # 测试 IFFT
    reconstructed = ifft(spectrum)
    error = sum(abs(r.real - s) for r, s in zip(reconstructed, signal))
    print(f"\nIFFT 重建误差: {error:.10f}")
    
    # 测试窗函数
    print("\n窗函数测试:")
    for wt in [WindowType.RECTANGULAR, WindowType.HANNING, WindowType.HAMMING, 
               WindowType.BLACKMAN, WindowType.BARTLETT]:
        window = get_window(wt, 10)
        print(f"  {wt.value}: {[f'{w:.3f}' for w in window[:5]]}...")
    
    # 测试卷积
    print("\n卷积测试:")
    a = [1, 2, 3, 4, 5]
    b = [1, 1, 1]
    conv = convolve(a, b)
    print(f"  {a} * {b} = {conv}")
    
    # 测试自相关
    print("\n自相关测试:")
    auto = autocorrelate(a)
    print(f"  自相关结果长度: {len(auto)}")
    
    print("\n所有测试完成!")