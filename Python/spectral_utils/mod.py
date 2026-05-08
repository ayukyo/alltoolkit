"""
Spectral Utils - 频谱分析工具

零依赖的信号频谱分析库，支持：
- 快速傅里叶变换 (FFT)
- 功率谱密度计算
- 频谱分析
- 信号滤波
- 频率检测
- 时频分析

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math


class WindowFunction(Enum):
    """窗函数类型"""
    RECTANGULAR = "rectangular"  # 矩形窗
    HANN = "hann"                # 汉宁窗
    HAMMING = "hamming"          # 汉明窗
    BLACKMAN = "blackman"         # 布莱克曼窗
    BARTLETT = "bartlett"         # 巴特利特窗


class FilterType(Enum):
    """滤波器类型"""
    LOW_PASS = "low_pass"     # 低通滤波器
    HIGH_PASS = "high_pass"   # 高通滤波器
    BAND_PASS = "band_pass"   # 带通滤波器
    BAND_STOP = "band_stop"   # 带阻滤波器


@dataclass
class SpectrumResult:
    """频谱分析结果"""
    frequencies: List[float]      # 频率数组 (Hz)
    magnitudes: List[float]       # 幅值数组
    phases: List[float]           # 相位数组 (弧度)
    power_spectrum: List[float]    # 功率谱
    sample_rate: float             # 采样率 (Hz)


@dataclass
class PeakInfo:
    """峰值信息"""
    frequency: float     # 频率 (Hz)
    magnitude: float     # 幅值
    phase: float         # 相位 (弧度)
    index: int           # 在频谱中的索引


class SpectralError(Exception):
    """频谱分析相关错误的基类"""
    pass


class InvalidSignalError(SpectralError):
    """无效的信号数据"""
    pass


class InvalidParameterError(SpectralError):
    """无效的参数"""
    pass


# ============ 基础数学函数 ============

def _next_power_of_2(n: int) -> int:
    """计算大于等于 n 的最小 2 的幂"""
    if n <= 0:
        return 1
    power = 1
    while power < n:
        power *= 2
    return power


def _bit_reverse(n: int, bits: int) -> int:
    """位反转"""
    result = 0
    for i in range(bits):
        if n & (1 << i):
            result |= 1 << (bits - 1 - i)
    return result


def _complex_multiply(a_real: float, a_imag: float, 
                       b_real: float, b_imag: float) -> Tuple[float, float]:
    """复数乘法"""
    real = a_real * b_real - a_imag * b_imag
    imag = a_real * b_imag + a_imag * b_real
    return real, imag


def _complex_add(a_real: float, a_imag: float,
                 b_real: float, b_imag: float) -> Tuple[float, float]:
    """复数加法"""
    return a_real + b_real, a_imag + b_imag


def _complex_subtract(a_real: float, a_imag: float,
                      b_real: float, b_imag: float) -> Tuple[float, float]:
    """复数减法"""
    return a_real - b_real, a_imag - b_imag


# ============ 窗函数 ============

def rectangular_window(size: int) -> List[float]:
    """矩形窗"""
    return [1.0] * size


def hann_window(size: int) -> List[float]:
    """汉宁窗 (Hann Window)"""
    return [0.5 * (1 - math.cos(2 * math.pi * n / (size - 1))) 
            for n in range(size)] if size > 1 else [1.0]


def hamming_window(size: int) -> List[float]:
    """汉明窗 (Hamming Window)"""
    return [0.54 - 0.46 * math.cos(2 * math.pi * n / (size - 1))
            for n in range(size)] if size > 1 else [1.0]


def blackman_window(size: int) -> List[float]:
    """布莱克曼窗 (Blackman Window)"""
    return [0.42 - 0.5 * math.cos(2 * math.pi * n / (size - 1)) +
            0.08 * math.cos(4 * math.pi * n / (size - 1))
            for n in range(size)] if size > 1 else [1.0]


def bartlett_window(size: int) -> List[float]:
    """巴特利特窗 (Bartlett Window)"""
    if size <= 1:
        return [1.0]
    mid = (size - 1) / 2.0
    return [1 - abs(n - mid) / mid for n in range(size)]


def apply_window(signal: List[float], window_type: WindowFunction) -> List[float]:
    """
    对信号应用窗函数
    
    Args:
        signal: 输入信号
        window_type: 窗函数类型
        
    Returns:
        加窗后的信号
    """
    size = len(signal)
    
    window_funcs = {
        WindowFunction.RECTANGULAR: rectangular_window,
        WindowFunction.HANN: hann_window,
        WindowFunction.HAMMING: hamming_window,
        WindowFunction.BLACKMAN: blackman_window,
        WindowFunction.BARTLETT: bartlett_window,
    }
    
    window = window_funcs[window_type](size)
    return [signal[i] * window[i] for i in range(size)]


# ============ FFT ============

def fft(signal: List[float]) -> List[Tuple[float, float]]:
    """
    快速傅里叶变换 (Cooley-Tukey 算法)
    
    Args:
        signal: 输入信号（实数）
        
    Returns:
        复数列表 [(实部, 虚部), ...]
        
    Raises:
        InvalidSignalError: 信号长度为 0
    """
    n = len(signal)
    if n == 0:
        raise InvalidSignalError("信号长度不能为 0")
    
    # 补零到 2 的幂次
    n_fft = _next_power_of_2(n)
    padded_signal = signal + [0.0] * (n_fft - n)
    
    # 计算位数
    bits = int(math.log2(n_fft))
    
    # 位反转重排
    real = [0.0] * n_fft
    imag = [0.0] * n_fft
    for i in range(n_fft):
        j = _bit_reverse(i, bits)
        real[j] = padded_signal[i]
    
    # Cooley-Tukey 迭代 FFT
    for s in range(1, bits + 1):
        m = 2 ** s
        m2 = m // 2
        
        # 主根
        w_real = math.cos(2 * math.pi / m)
        w_imag = -math.sin(2 * math.pi / m)
        
        for k in range(0, n_fft, m):
            w_m_real = 1.0
            w_m_imag = 0.0
            
            for j in range(m2):
                t_real, t_imag = _complex_multiply(
                    w_m_real, w_m_imag,
                    real[k + j + m2], imag[k + j + m2]
                )
                u_real, u_imag = real[k + j], imag[k + j]
                
                real[k + j] = u_real + t_real
                imag[k + j] = u_imag + t_imag
                real[k + j + m2] = u_real - t_real
                imag[k + j + m2] = u_imag - t_imag
                
                # 更新旋转因子
                w_m_real, w_m_imag = _complex_multiply(
                    w_m_real, w_m_imag, w_real, w_imag
                )
    
    return list(zip(real, imag))


def ifft(spectrum: List[Tuple[float, float]]) -> List[float]:
    """
    快速傅里叶逆变换
    
    Args:
        spectrum: 频谱数据 [(实部, 虚部), ...]
        
    Returns:
        时域信号（实数）
    """
    n = len(spectrum)
    if n == 0:
        return []
    
    # 共轭
    conjugated = [(real, -imag) for real, imag in spectrum]
    
    # 正向 FFT
    result = fft_complex(conjugated)
    
    # 除以 N 并取实部
    return [real / n for real, imag in result]


def fft_complex(signal: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    复数 FFT
    
    Args:
        signal: 复数信号 [(实部, 虚部), ...]
        
    Returns:
        复数频谱 [(实部, 虚部), ...]
    """
    n = len(signal)
    if n == 0:
        return []
    
    # 补零
    n_fft = _next_power_of_2(n)
    padded = list(signal) + [(0.0, 0.0)] * (n_fft - n)
    
    # 分离实部和虚部
    real = [r for r, i in padded]
    imag = [i for r, i in padded]
    
    # 计算位数
    bits = int(math.log2(n_fft))
    
    # 位反转
    real_out = [0.0] * n_fft
    imag_out = [0.0] * n_fft
    for i in range(n_fft):
        j = _bit_reverse(i, bits)
        real_out[j] = real[i]
        imag_out[j] = imag[i]
    
    real, imag = real_out, imag_out
    
    # Cooley-Tukey 迭代
    for s in range(1, bits + 1):
        m = 2 ** s
        m2 = m // 2
        
        w_real = math.cos(2 * math.pi / m)
        w_imag = -math.sin(2 * math.pi / m)
        
        for k in range(0, n_fft, m):
            w_m_real = 1.0
            w_m_imag = 0.0
            
            for j in range(m2):
                t_real, t_imag = _complex_multiply(
                    w_m_real, w_m_imag,
                    real[k + j + m2], imag[k + j + m2]
                )
                u_real, u_imag = real[k + j], imag[k + j]
                
                real[k + j] = u_real + t_real
                imag[k + j] = u_imag + t_imag
                real[k + j + m2] = u_real - t_real
                imag[k + j + m2] = u_imag - t_imag
                
                w_m_real, w_m_imag = _complex_multiply(
                    w_m_real, w_m_imag, w_real, w_imag
                )
    
    return list(zip(real, imag))


# ============ 频谱分析 ============

def compute_spectrum(signal: List[float], 
                     sample_rate: float,
                     window: WindowFunction = WindowFunction.HANN) -> SpectrumResult:
    """
    计算信号的频谱
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        window: 窗函数类型
        
    Returns:
        SpectrumResult 对象
    """
    if len(signal) == 0:
        raise InvalidSignalError("信号长度不能为 0")
    if sample_rate <= 0:
        raise InvalidParameterError("采样率必须大于 0")
    
    n = len(signal)
    
    # 应用窗函数
    windowed_signal = apply_window(signal, window)
    
    # FFT
    spectrum = fft(windowed_signal)
    n_fft = len(spectrum)
    
    # 只取前一半（对称性）
    half = n_fft // 2 + 1
    
    # 计算频率
    frequencies = [i * sample_rate / n_fft for i in range(half)]
    
    # 计算幅值和相位
    magnitudes = []
    phases = []
    for real, imag in spectrum[:half]:
        magnitude = math.sqrt(real * real + imag * imag) / n
        phase = math.atan2(imag, real)
        magnitudes.append(magnitude)
        phases.append(phase)
    
    # 功率谱
    power_spectrum = [mag * mag for mag in magnitudes]
    
    return SpectrumResult(
        frequencies=frequencies,
        magnitudes=magnitudes,
        phases=phases,
        power_spectrum=power_spectrum,
        sample_rate=sample_rate
    )


def compute_power_spectral_density(signal: List[float],
                                   sample_rate: float,
                                   window: WindowFunction = WindowFunction.HANN) -> Tuple[List[float], List[float]]:
    """
    计算功率谱密度 (PSD)
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        window: 窗函数类型
        
    Returns:
        (频率数组, 功率谱密度数组)
    """
    spectrum = compute_spectrum(signal, sample_rate, window)
    
    # 功率谱密度 = 功率谱 / 频率分辨率
    n = len(signal)
    df = sample_rate / (2 * _next_power_of_2(n))
    
    psd = [p / df for p in spectrum.power_spectrum]
    
    return spectrum.frequencies, psd


def find_peaks(spectrum: SpectrumResult,
               threshold: float = 0.0,
               min_distance: int = 1,
               max_peaks: int = 10) -> List[PeakInfo]:
    """
    找出频谱中的峰值
    
    Args:
        spectrum: 频谱分析结果
        threshold: 幅值阈值
        min_distance: 峰值之间的最小距离（索引）
        max_peaks: 最大峰值数量
        
    Returns:
        峰值信息列表
    """
    magnitudes = spectrum.magnitudes
    n = len(magnitudes)
    
    peaks = []
    for i in range(1, n - 1):
        # 检查是否为局部最大值
        if magnitudes[i] > magnitudes[i-1] and magnitudes[i] > magnitudes[i+1]:
            if magnitudes[i] >= threshold:
                peaks.append((i, magnitudes[i]))
    
    # 按幅值排序
    peaks.sort(key=lambda x: x[1], reverse=True)
    
    # 过滤距离太近的峰
    filtered = []
    for idx, mag in peaks:
        if len(filtered) == 0:
            filtered.append((idx, mag))
        else:
            if all(abs(idx - f[0]) >= min_distance for f in filtered):
                filtered.append((idx, mag))
    
    # 限制数量
    filtered = filtered[:max_peaks]
    
    return [
        PeakInfo(
            frequency=spectrum.frequencies[idx],
            magnitude=mag,
            phase=spectrum.phases[idx],
            index=idx
        )
        for idx, mag in filtered
    ]


def detect_dominant_frequency(signal: List[float],
                               sample_rate: float) -> Optional[float]:
    """
    检测信号的主频率
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        
    Returns:
        主频率 (Hz)，如果信号太弱返回 None
    """
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.01, max_peaks=1)
    
    if peaks:
        return peaks[0].frequency
    return None


# ============ 滤波器 ============

def low_pass_filter(signal: List[float],
                    sample_rate: float,
                    cutoff_frequency: float,
                    order: int = 4) -> List[float]:
    """
    低通滤波器 (简单 RC 滤波器实现)
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        cutoff_frequency: 截止频率 (Hz)
        order: 滤波器阶数
        
    Returns:
        滤波后的信号
    """
    if cutoff_frequency <= 0 or cutoff_frequency >= sample_rate / 2:
        raise InvalidParameterError("截止频率必须在 0 和奈奎斯特频率之间")
    
    # RC 时间常数
    rc = 1.0 / (2 * math.pi * cutoff_frequency)
    dt = 1.0 / sample_rate
    alpha = dt / (rc + dt)
    
    # 多级滤波
    result = list(signal)
    for _ in range(order):
        filtered = [result[0]]
        for i in range(1, len(result)):
            filtered.append(filtered[-1] + alpha * (result[i] - filtered[-1]))
        result = filtered
    
    return result


def high_pass_filter(signal: List[float],
                     sample_rate: float,
                     cutoff_frequency: float,
                     order: int = 4) -> List[float]:
    """
    高通滤波器
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        cutoff_frequency: 截止频率 (Hz)
        order: 滤波器阶数
        
    Returns:
        滤波后的信号
    """
    if cutoff_frequency <= 0 or cutoff_frequency >= sample_rate / 2:
        raise InvalidParameterError("截止频率必须在 0 和奈奎斯特频率之间")
    
    # RC 时间常数
    rc = 1.0 / (2 * math.pi * cutoff_frequency)
    dt = 1.0 / sample_rate
    alpha = rc / (rc + dt)
    
    # 多级滤波
    result = list(signal)
    for _ in range(order):
        filtered = [result[0]]
        for i in range(1, len(result)):
            filtered.append(alpha * (filtered[-1] + result[i] - result[i-1]))
        result = filtered
    
    return result


def band_pass_filter(signal: List[float],
                     sample_rate: float,
                     low_cutoff: float,
                     high_cutoff: float,
                     order: int = 4) -> List[float]:
    """
    带通滤波器
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        low_cutoff: 低截止频率 (Hz)
        high_cutoff: 高截止频率 (Hz)
        order: 滤波器阶数
        
    Returns:
        滤波后的信号
    """
    # 先高通，再低通
    high_passed = high_pass_filter(signal, sample_rate, low_cutoff, order)
    return low_pass_filter(high_passed, sample_rate, high_cutoff, order)


def band_stop_filter(signal: List[float],
                     sample_rate: float,
                     low_cutoff: float,
                     high_cutoff: float,
                     order: int = 4) -> List[float]:
    """
    带阻滤波器 (陷波滤波器)
    
    Args:
        signal: 输入信号
        sample_rate: 采样率 (Hz)
        low_cutoff: 低截止频率 (Hz)
        high_cutoff: 高截止频率 (Hz)
        order: 滤波器阶数
        
    Returns:
        滤波后的信号
    """
    # 低通 + 高通，然后相加
    low_passed = low_pass_filter(signal, sample_rate, low_cutoff, order)
    high_passed = high_pass_filter(signal, sample_rate, high_cutoff, order)
    
    # 简单叠加（假设滤波器特性良好）
    return [(l + h) / 2 for l, h in zip(low_passed, high_passed)]


# ============ 时频分析 ============

def short_time_fourier_transform(signal: List[float],
                                  window_size: int,
                                  hop_size: int,
                                  sample_rate: float,
                                  window: WindowFunction = WindowFunction.HANN) -> List[SpectrumResult]:
    """
    短时傅里叶变换 (STFT)
    
    Args:
        signal: 输入信号
        window_size: 窗口大小
        hop_size: 跳跃大小
        sample_rate: 采样率 (Hz)
        window: 窗函数类型
        
    Returns:
        各时间窗的频谱分析结果列表
    """
    if window_size <= 0 or hop_size <= 0:
        raise InvalidParameterError("窗口大小和跳跃大小必须大于 0")
    if window_size > len(signal):
        raise InvalidParameterError("窗口大小不能大于信号长度")
    
    results = []
    start = 0
    
    while start + window_size <= len(signal):
        segment = signal[start:start + window_size]
        spectrum = compute_spectrum(segment, sample_rate, window)
        results.append(spectrum)
        start += hop_size
    
    return results


def compute_spectrogram(signal: List[float],
                        window_size: int,
                        hop_size: int,
                        sample_rate: float,
                        window: WindowFunction = WindowFunction.HANN) -> Tuple[List[float], List[float], List[List[float]]]:
    """
    计算频谱图
    
    Args:
        signal: 输入信号
        window_size: 窗口大小
        hop_size: 跳跃大小
        sample_rate: 采样率 (Hz)
        window: 窗函数类型
        
    Returns:
        (时间数组, 频率数组, 功率谱矩阵)
    """
    stft_results = short_time_fourier_transform(
        signal, window_size, hop_size, sample_rate, window
    )
    
    if not stft_results:
        return [], [], []
    
    # 时间轴
    times = [i * hop_size / sample_rate for i in range(len(stft_results))]
    
    # 频率轴（取第一个结果的频率）
    frequencies = stft_results[0].frequencies
    
    # 功率谱矩阵
    spectrogram = [result.power_spectrum for result in stft_results]
    
    return times, frequencies, spectrogram


# ============ 工具函数 ============

def generate_sine_wave(frequency: float,
                       sample_rate: float,
                       duration: float,
                       amplitude: float = 1.0,
                       phase: float = 0.0) -> List[float]:
    """
    生成正弦波
    
    Args:
        frequency: 频率 (Hz)
        sample_rate: 采样率 (Hz)
        duration: 时长 (秒)
        amplitude: 幅值
        phase: 初始相位 (弧度)
        
    Returns:
        正弦波信号
    """
    n_samples = int(sample_rate * duration)
    return [
        amplitude * math.sin(2 * math.pi * frequency * i / sample_rate + phase)
        for i in range(n_samples)
    ]


def generate_composite_wave(frequencies: List[float],
                            amplitudes: List[float],
                            sample_rate: float,
                            duration: float,
                            phases: Optional[List[float]] = None) -> List[float]:
    """
    生成复合波
    
    Args:
        frequencies: 频率列表 (Hz)
        amplitudes: 幅值列表
        sample_rate: 采样率 (Hz)
        duration: 时长 (秒)
        phases: 相位列表 (弧度)，默认为 0
        
    Returns:
        复合波信号
    """
    if len(frequencies) != len(amplitudes):
        raise InvalidParameterError("频率和幅值列表长度必须相同")
    
    if phases is None:
        phases = [0.0] * len(frequencies)
    elif len(phases) != len(frequencies):
        raise InvalidParameterError("相位列表长度必须与频率列表相同")
    
    n_samples = int(sample_rate * duration)
    signal = [0.0] * n_samples
    
    for freq, amp, phase in zip(frequencies, amplitudes, phases):
        for i in range(n_samples):
            signal[i] += amp * math.sin(2 * math.pi * freq * i / sample_rate + phase)
    
    return signal


def compute_rms(signal: List[float]) -> float:
    """
    计算信号的均方根值
    
    Args:
        signal: 输入信号
        
    Returns:
        RMS 值
    """
    if len(signal) == 0:
        return 0.0
    return math.sqrt(sum(x * x for x in signal) / len(signal))


def normalize_signal(signal: List[float],
                     target_rms: float = 1.0) -> List[float]:
    """
    归一化信号
    
    Args:
        signal: 输入信号
        target_rms: 目标 RMS 值
        
    Returns:
        归一化后的信号
    """
    current_rms = compute_rms(signal)
    if current_rms == 0:
        return signal
    
    scale = target_rms / current_rms
    return [x * scale for x in signal]


def compute_frequency_response(filter_func,
                               sample_rate: float,
                               n_points: int = 512) -> Tuple[List[float], List[float]]:
    """
    计算滤波器的频率响应
    
    Args:
        filter_func: 滤波函数，接受信号和采样率，返回滤波后的信号
        sample_rate: 采样率 (Hz)
        n_points: 频率点数
        
    Returns:
        (频率数组, 幅值响应数组)
    """
    # 生成冲击响应
    impulse = [1.0] + [0.0] * (n_points - 1)
    
    # 通过滤波器
    response = filter_func(impulse, sample_rate)
    
    # 计算频谱
    spectrum = compute_spectrum(response, sample_rate)
    
    return spectrum.frequencies, spectrum.magnitudes


# ============ 示例使用 ============

if __name__ == "__main__":
    print("=" * 60)
    print("Spectral Utils - 频谱分析工具演示")
    print("=" * 60)
    
    # 生成测试信号：复合波
    sample_rate = 1000.0  # 1 kHz
    duration = 1.0        # 1 秒
    
    print("\n1. 生成测试信号")
    signal = generate_composite_wave(
        frequencies=[50, 120, 300],   # 三个频率分量
        amplitudes=[1.0, 0.7, 0.3],     # 不同幅值
        sample_rate=sample_rate,
        duration=duration
    )
    print(f"   信号长度: {len(signal)} 个采样点")
    print(f"   包含频率: 50Hz, 120Hz, 300Hz")
    
    # 频谱分析
    print("\n2. 频谱分析")
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.01, max_peaks=5)
    
    print("   检测到的峰值频率:")
    for peak in peaks:
        print(f"   - {peak.frequency:.2f} Hz (幅值: {peak.magnitude:.4f})")
    
    # 主频率检测
    print("\n3. 主频率检测")
    dominant = detect_dominant_frequency(signal, sample_rate)
    print(f"   主频率: {dominant:.2f} Hz")
    
    # 滤波测试
    print("\n4. 低通滤波器测试 (截止频率: 100Hz)")
    filtered = low_pass_filter(signal, sample_rate, 100, order=4)
    filtered_spectrum = compute_spectrum(filtered, sample_rate)
    filtered_peaks = find_peaks(filtered_spectrum, threshold=0.01, max_peaks=5)
    
    print("   滤波后的峰值频率:")
    for peak in filtered_peaks:
        print(f"   - {peak.frequency:.2f} Hz (幅值: {peak.magnitude:.4f})")
    
    # RMS 计算
    print("\n5. 信号统计")
    print(f"   原始信号 RMS: {compute_rms(signal):.4f}")
    print(f"   滤波信号 RMS: {compute_rms(filtered):.4f}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)