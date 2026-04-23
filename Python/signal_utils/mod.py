"""
Signal Processing Utilities - 信号处理工具集

零外部依赖的信号处理工具，纯 Python 标准库实现。

功能模块：
1. 信号生成 - 生成各种波形（正弦、方波、三角波、噪声等）
2. 信号滤波 - 基础滤波器（移动平均、中值滤波、平滑滤波）
3. 信号变换 - FFT 离散傅里叶变换及其逆变换
4. 信号分析 - 频率检测、峰值检测、能量计算
5. 信号操作 - 卷积、相关性、插值、重采样

作者：AllToolkit 自动生成
日期：2026-04-23
"""

import math
import cmath
from typing import List, Tuple, Optional, Callable, Union
from collections import deque


# ============================================================================
# 信号生成模块
# ============================================================================

def generate_sine_wave(
    frequency: float,
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0,
    phase: float = 0.0
) -> List[float]:
    """
    生成正弦波信号
    
    Args:
        frequency: 频率 (Hz)
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅 (0-1)
        phase: 相位偏移 (弧度)
    
    Returns:
        正弦波采样值列表
    
    Example:
        >>> wave = generate_sine_wave(440, 1.0)  # 440Hz 正弦波，持续 1 秒
        >>> len(wave)  # 44100 个采样点
        44100
    """
    num_samples = int(duration * sample_rate)
    return [
        amplitude * math.sin(2 * math.pi * frequency * t / sample_rate + phase)
        for t in range(num_samples)
    ]


def generate_square_wave(
    frequency: float,
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成方波信号
    
    Args:
        frequency: 频率 (Hz)
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅 (0-1)
    
    Returns:
        方波采样值列表
    """
    num_samples = int(duration * sample_rate)
    period = sample_rate / frequency
    return [
        amplitude if (t % period) < period / 2 else -amplitude
        for t in range(num_samples)
    ]


def generate_triangle_wave(
    frequency: float,
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成三角波信号
    
    Args:
        frequency: 频率 (Hz)
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅 (0-1)
    
    Returns:
        三角波采样值列表
    """
    num_samples = int(duration * sample_rate)
    period = sample_rate / frequency
    result = []
    for t in range(num_samples):
        phase = (t % period) / period
        # 三角波：从 -amplitude 到 amplitude 的线性变化
        if phase < 0.25:
            value = amplitude * (4 * phase)
        elif phase < 0.75:
            value = amplitude * (2 - 4 * phase)
        else:
            value = amplitude * (4 * phase - 4)
        result.append(value)
    return result


def generate_sawtooth_wave(
    frequency: float,
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成锯齿波信号
    
    Args:
        frequency: 频率 (Hz)
        duration: 挀续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅 (0-1)
    
    Returns:
        锯齿波采样值列表
    """
    num_samples = int(duration * sample_rate)
    period = sample_rate / frequency
    return [
        amplitude * (2 * ((t % period) / period) - 1)
        for t in range(num_samples)
    ]


def generate_white_noise(
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成白噪声信号（伪随机）
    
    Args:
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅 (0-1)
    
    Returns:
        白噪声采样值列表
    
    Note:
        使用简单的伪随机算法，零依赖
    """
    num_samples = int(duration * sample_rate)
    # 简单的线性同余随机数生成器
    seed = 12345
    a = 1103515245
    c = 12345
    m = 2 ** 31
    
    result = []
    for _ in range(num_samples):
        seed = (a * seed + c) % m
        # 映射到 [-amplitude, amplitude]
        value = amplitude * (2 * seed / m - 1)
        result.append(value)
    return result


def generate_pulse(
    duration: float,
    sample_rate: float = 44100,
    pulse_width: float = 0.1,
    amplitude: float = 1.0,
    position: float = 0.5
) -> List[float]:
    """
    生成脉冲信号
    
    Args:
        duration: 总持续时间 (秒)
        sample_rate: 采样率 (Hz)
        pulse_width: 脉冲宽度 (秒)
        amplitude: 脉冲振幅
        position: 脉冲位置 (0-1，相对于总时长)
    
    Returns:
        脉冲信号采样值列表
    """
    num_samples = int(duration * sample_rate)
    pulse_start = int(position * num_samples)
    pulse_end = int(pulse_start + pulse_width * sample_rate)
    
    result = [0.0] * num_samples
    for i in range(pulse_start, min(pulse_end, num_samples)):
        result[i] = amplitude
    return result


def generate_chirp(
    start_freq: float,
    end_freq: float,
    duration: float,
    sample_rate: float = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成线性扫频信号（Chirp）
    
    Args:
        start_freq: 起始频率 (Hz)
        end_freq: 结束频率 (Hz)
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitude: 振幅
    
    Returns:
        扫频信号采样值列表
    """
    num_samples = int(duration * sample_rate)
    # 线性频率变化
    freq_rate = (end_freq - start_freq) / duration
    
    result = []
    for t in range(num_samples):
        time = t / sample_rate
        # 线性扫频的瞬时频率
        instant_freq = start_freq + freq_rate * time
        # 相位积分
        phase = 2 * math.pi * (start_freq * time + 0.5 * freq_rate * time ** 2)
        result.append(amplitude * math.sin(phase))
    return result


def generate_custom_wave(
    duration: float,
    sample_rate: float = 44100,
    wave_func: Callable[[float], float] = None
) -> List[float]:
    """
    生成自定义波形信号
    
    Args:
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        wave_func: 波形函数，输入相位 (0-1)，输出振幅
    
    Returns:
        自定义波形采样值列表
    
    Example:
        >>> # 生成半正弦波
        >>> wave = generate_custom_wave(1.0, wave_func=lambda p: math.sin(p * math.pi) if p < 0.5 else 0)
    """
    if wave_func is None:
        wave_func = lambda p: math.sin(2 * math.pi * p)
    
    num_samples = int(duration * sample_rate)
    return [wave_func(t / num_samples) for t in range(num_samples)]


def generate_harmonic_series(
    base_freq: float,
    num_harmonics: int,
    duration: float,
    sample_rate: float = 44100,
    amplitudes: Optional[List[float]] = None
) -> List[float]:
    """
    生成谐波序列（多个正弦波的叠加）
    
    Args:
        base_freq: 基频 (Hz)
        num_harmonics: 谐波数量
        duration: 持续时间 (秒)
        sample_rate: 采样率 (Hz)
        amplitudes: 各谐波振幅列表（默认递减）
    
    Returns:
        谐波叠加信号
    
    Example:
        >>> # 生成 5 个谐波
        >>> wave = generate_harmonic_series(440, 5, 1.0)
    """
    if amplitudes is None:
        # 默认振幅递减：基频最大，高频递减
        amplitudes = [1.0 / (i + 1) for i in range(num_harmonics)]
    
    num_samples = int(duration * sample_rate)
    result = [0.0] * num_samples
    
    for harmonic in range(num_harmonics):
        freq = base_freq * (harmonic + 1)
        amp = amplitudes[harmonic] if harmonic < len(amplitudes) else 0.0
        for t in range(num_samples):
            result[t] += amp * math.sin(2 * math.pi * freq * t / sample_rate)
    
    return result


# ============================================================================
# 信号滤波模块
# ============================================================================

def moving_average_filter(
    signal: List[float],
    window_size: int
) -> List[float]:
    """
    移动平均滤波器
    
    Args:
        signal: 输入信号
        window_size: 窗口大小
    
    Returns:
        滤波后的信号
    
    Example:
        >>> filtered = moving_average_filter([1, 2, 3, 4, 5], 3)
        >>> # 结果：[1, 1.5, 2, 3, 4]
    """
    if window_size < 1:
        raise ValueError("窗口大小必须 >= 1")
    
    n = len(signal)
    result = []
    
    # 使用滑动窗口计算
    window = deque(signal[:window_size], maxlen=window_size)
    current_sum = sum(window)
    
    for i in range(n):
        if i < window_size - 1:
            # 前几个点，窗口不完整
            result.append(signal[i])
        elif i == window_size - 1:
            # 窗口刚填满
            result.append(current_sum / window_size)
        else:
            # 滑动窗口
            old_val = window[0] if len(window) == window_size else 0
            new_val = signal[i]
            window.append(new_val)
            current_sum = current_sum - old_val + new_val
            result.append(current_sum / window_size)
    
    return result


def median_filter(
    signal: List[float],
    window_size: int
) -> List[float]:
    """
    中值滤波器（有效去除脉冲噪声）
    
    Args:
        signal: 输入信号
        window_size: 窗口大小
    
    Returns:
        滤波后的信号
    """
    if window_size < 1:
        raise ValueError("窗口大小必须 >= 1")
    
    n = len(signal)
    result = []
    half_window = window_size // 2
    
    for i in range(n):
        # 确定窗口范围
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        window = signal[start:end]
        # 计算中值
        sorted_window = sorted(window)
        mid = len(sorted_window) // 2
        if len(sorted_window) % 2 == 0:
            median = (sorted_window[mid - 1] + sorted_window[mid]) / 2
        else:
            median = sorted_window[mid]
        result.append(median)
    
    return result


def exponential_smoothing(
    signal: List[float],
    alpha: float = 0.3
) -> List[float]:
    """
    指数平滑滤波器
    
    Args:
        signal: 输入信号
        alpha: 平滑系数 (0-1)，越大越接近原信号
    
    Returns:
        滤波后的信号
    
    Example:
        >>> filtered = exponential_smoothing([1, 2, 3, 4, 5], 0.5)
    """
    if not 0 <= alpha <= 1:
        raise ValueError("alpha 必须在 [0, 1] 范围内")
    
    if not signal:
        return []
    
    result = [signal[0]]
    for i in range(1, len(signal)):
        smoothed = alpha * signal[i] + (1 - alpha) * result[-1]
        result.append(smoothed)
    
    return result


def lowpass_filter_simple(
    signal: List[float],
    cutoff_ratio: float = 0.1
) -> List[float]:
    """
    简单低通滤波器（一阶 RC 滤波器模拟）
    
    Args:
        signal: 输入信号
        cutoff_ratio: 截断比率 (0-1)，越小滤波越强
    
    Returns:
        滤波后的信号
    """
    if not 0 < cutoff_ratio < 1:
        raise ValueError("cutoff_ratio 必须在 (0, 1) 范围内")
    
    # 一阶低通滤波器：y[n] = alpha * x[n] + (1-alpha) * y[n-1]
    # alpha = cutoff_ratio
    return exponential_smoothing(signal, cutoff_ratio)


def highpass_filter_simple(
    signal: List[float],
    cutoff_ratio: float = 0.1
) -> List[float]:
    """
    简单高通滤波器
    
    Args:
        signal: 输入信号
        cutoff_ratio: 截断比率 (0-1)
    
    Returns:
        滤波后的信号
    """
    if not 0 < cutoff_ratio < 1:
        raise ValueError("cutoff_ratio 必须在 (0, 1) 范围内")
    
    # 高通 = 原信号 - 低通
    lowpass = exponential_smoothing(signal, cutoff_ratio)
    return [signal[i] - lowpass[i] for i in range(len(signal))]


def bandpass_filter_simple(
    signal: List[float],
    low_cutoff: float = 0.1,
    high_cutoff: float = 0.3
) -> List[float]:
    """
    简单带通滤波器
    
    Args:
        signal: 输入信号
        low_cutoff: 低频截断比率
        high_cutoff: 高频截断比率
    
    Returns:
        滤波后的信号
    """
    # 带通 = 高通(低截断) 然后 低通(高截断)
    highpass = highpass_filter_simple(signal, low_cutoff)
    return exponential_smoothing(highpass, high_cutoff)


def savitzky_golay_filter(
    signal: List[float],
    window_size: int = 5,
    polynomial_order: int = 2
) -> List[float]:
    """
    Savitzky-Golay 滤波器（多项式平滑）
    
    Args:
        signal: 输入信号
        window_size: 窗口大小（奇数）
        polynomial_order: 多项式阶数
    
    Returns:
        滤波后的信号
    
    Note:
        简化实现，使用最小二乘多项式拟合
    """
    if window_size % 2 == 0:
        raise ValueError("窗口大小必须是奇数")
    if polynomial_order >= window_size:
        raise ValueError("多项式阶数必须小于窗口大小")
    
    n = len(signal)
    half_window = window_size // 2
    result = []
    
    for i in range(n):
        # 确定窗口范围
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        window = signal[start:end]
        
        # 简化的多项式拟合：使用中心点的线性拟合
        # 对于小窗口，直接用窗口平均值作为平滑值
        # 对于 order=2，使用二次多项式拟合
        
        if polynomial_order == 0:
            result.append(sum(window) / len(window))
        elif polynomial_order == 1:
            # 线性拟合
            m = len(window)
            x = list(range(m))
            y = window
            # 简化：取中心点拟合值
            x_mean = sum(x) / m
            y_mean = sum(y) / m
            if m > 1:
                slope = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y)) / \
                        sum((xi - x_mean) ** 2 for xi in x)
                center_x = i - start
                fitted = y_mean + slope * (center_x - x_mean)
                result.append(fitted)
            else:
                result.append(y[0])
        else:
            # 对于 order >= 2，使用二次多项式简化拟合
            # 使用最小二乘法（简化版）
            m = len(window)
            x = [j - (m - 1) / 2 for j in range(m)]  # 中心化的 x
            y = window
            
            # 计算二次多项式系数 a*x^2 + b*x + c
            # 简化：对于中心点 x=0，值为 c ≈ mean(y) - variance correction
            if m >= 3:
                x2_sum = sum(xi ** 2 for xi in x)
                x4_sum = sum(xi ** 4 for xi in x)
                y_sum = sum(y)
                x2y_sum = sum(xi ** 2 * yi for xi, yi in zip(x, y))
                
                # 解简化方程
                denom = m * x4_sum - x2_sum ** 2
                if denom != 0:
                    a = (m * x2y_sum - x2_sum * y_sum) / denom
                    c = (y_sum - a * x2_sum) / m
                    result.append(c)
                else:
                    result.append(y_sum / m)
            else:
                result.append(sum(window) / len(window))
    
    return result


def notch_filter(
    signal: List[float],
    notch_freq_ratio: float,
    bandwidth_ratio: float = 0.02
) -> List[float]:
    """
    简单陷波滤波器（去除特定频率）
    
    Args:
        signal: 输入信号
        notch_freq_ratio: 陷波频率比率 (0-0.5)
        bandwidth_ratio: 带宽比率
    
    Returns:
        滤波后的信号
    
    Note:
        使用 FFT 实现，在频域去除特定频率
    """
    n = len(signal)
    if n < 4:
        return signal.copy()
    
    # FFT 变换
    spectrum = fft(signal)
    
    # 计算陷波频率位置
    notch_bin = int(notch_freq_ratio * n)
    bandwidth_bins = int(bandwidth_ratio * n)
    
    # 频域陷波
    for i in range(max(1, notch_bin - bandwidth_bins), min(n // 2, notch_bin + bandwidth_bins + 1)):
        spectrum[i] = 0.0
        spectrum[n - i] = 0.0  # 对称位置
    
    # IFFT 恢复
    return ifft(spectrum)


# ============================================================================
# 信号变换模块 (FFT)
# ============================================================================

def fft(signal: List[float]) -> List[float]:
    """
    快速傅里叶变换 (FFT) - Cooley-Tukey 算法
    
    Args:
        signal: 输入信号（实数序列）
    
    Returns:
        FFT 结果（复数序列，实数表示的幅度谱）
    
    Note:
        - 纯 Python 实现，零依赖
        - 输入长度如果不是 2^n，会自动补零
        - 返回复数形式的频谱
    
    Example:
        >>> spectrum = fft([1, 2, 3, 4])
        >>> # 返回 4 个复数值
    """
    n = len(signal)
    
    # 补零到最近的 2^n
    next_power = 1
    while next_power < n:
        next_power *= 2
    
    padded = signal + [0.0] * (next_power - n)
    n = next_power
    
    # 转换为复数
    complex_signal = [complex(x, 0) for x in padded]
    
    # Cooley-Tukey FFT
    def cooley_tukey(x: List[complex]) -> List[complex]:
        n = len(x)
        if n <= 1:
            return x
        
        # 分离偶数和奇数索引
        even = cooley_tukey([x[i] for i in range(0, n, 2)])
        odd = cooley_tukey([x[i] for i in range(1, n, 2)])
        
        # 合并
        result = [complex(0, 0)] * n
        for k in range(n // 2):
            t = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
            result[k] = even[k] + t
            result[k + n // 2] = even[k] - t
        
        return result
    
    return cooley_tukey(complex_signal)


def ifft(spectrum: List[complex]) -> List[float]:
    """
    快速傅里叶逆变换 (IFFT)
    
    Args:
        spectrum: FFT 频谱（复数序列）
    
    Returns:
        逆变换后的实数信号
    
    Example:
        >>> signal = [1, 2, 3, 4]
        >>> spectrum = fft(signal)
        >>> recovered = ifft(spectrum)
        >>> # recovered ≈ signal
    """
    n = len(spectrum)
    
    # 取共轭
    conjugated = [x.conjugate() for x in spectrum]
    
    # FFT
    def cooley_tukey(x: List[complex]) -> List[complex]:
        n = len(x)
        if n <= 1:
            return x
        
        even = cooley_tukey([x[i] for i in range(0, n, 2)])
        odd = cooley_tukey([x[i] for i in range(1, n, 2)])
        
        result = [complex(0, 0)] * n
        for k in range(n // 2):
            t = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
            result[k] = even[k] + t
            result[k + n // 2] = even[k] - t
        
        return result
    
    # FFT 后再取共轮并归一化
    result = cooley_tukey(conjugated)
    result = [x.conjugate() / n for x in result]
    
    # 返回实部
    return [x.real for x in result]


def fft_magnitude(spectrum: List[complex]) -> List[float]:
    """
    计算 FFT 幅度谱
    
    Args:
        spectrum: FFT 频谱
    
    Returns:
        幅度谱（每个频率分量的幅度）
    """
    return [abs(x) for x in spectrum]


def fft_phase(spectrum: List[complex]) -> List[float]:
    """
    计算 FFT 相位谱
    
    Args:
        spectrum: FFT 频谱
    
    Returns:
        相位谱（每个频率分量的相位，弧度）
    """
    return [cmath.phase(x) for x in spectrum]


def power_spectrum(spectrum: List[complex]) -> List[float]:
    """
    计算功率谱（幅度平方）
    
    Args:
        spectrum: FFT 频谱
    
    Returns:
        功率谱
    """
    return [abs(x) ** 2 for x in spectrum]


def frequency_bins(
    n: int,
    sample_rate: float
) -> List[float]:
    """
    计算频率 bins（每个 FFT 点对应的频率）
    
    Args:
        n: FFT 长度
        sample_rate: 采样率
    
    Returns:
        频率列表 (Hz)
    """
    return [i * sample_rate / n for i in range(n)]


def dft(signal: List[float]) -> List[complex]:
    """
    离散傅里叶变换 (DFT) - 直接计算
    
    Args:
        signal: 输入信号
    
    Returns:
        DFT 频谱
    
    Note:
        O(n^2) 复杂度，用于教学或小信号
        大信号请使用 fft()
    """
    n = len(signal)
    result = []
    
    for k in range(n):
        sum_val = complex(0, 0)
        for t in range(n):
            angle = -2 * cmath.pi * k * t / n
            sum_val += signal[t] * cmath.exp(complex(0, angle))
        result.append(sum_val)
    
    return result


# ============================================================================
# 信号分析模块
# ============================================================================

def find_peaks(
    signal: List[float],
    min_height: Optional[float] = None,
    min_distance: int = 1,
    threshold: float = 0.0
) -> List[int]:
    """
    查找信号峰值位置
    
    Args:
        signal: 输入信号
        min_height: 最小峰值高度
        min_distance: 峰值之间的最小距离
        threshold: 峰值与相邻点的最小差值
    
    Returns:
        峰值索引列表
    
    Example:
        >>> peaks = find_peaks([1, 3, 2, 5, 3, 7, 2])
        >>> # 找到位置 1, 3, 5 的峰值
    """
    n = len(signal)
    if n < 3:
        return []
    
    # 确定最小高度
    if min_height is None:
        min_height = (max(signal) - min(signal)) * 0.1 + min(signal)
    
    # 找局部最大值
    candidates = []
    for i in range(1, n - 1):
        if signal[i] > signal[i - 1] and signal[i] > signal[i + 1]:
            if signal[i] >= min_height:
                if signal[i] - max(signal[i - 1], signal[i + 1]) >= threshold:
                    candidates.append((i, signal[i]))
    
    # 按高度排序
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    # 应用最小距离约束
    result = []
    for idx, height in candidates:
        # 检查与已选峰值的距离
        if all(abs(idx - p) >= min_distance for p in result):
            result.append(idx)
    
    return sorted(result)


def find_valleys(
    signal: List[float],
    min_depth: Optional[float] = None,
    min_distance: int = 1
) -> List[int]:
    """
    查找信号谷值位置
    
    Args:
        signal: 输入信号
        min_depth: 最小谷值深度（相对于最大值）
        min_distance: 谷值之间的最小距离
    
    Returns:
        谷值索引列表
    """
    n = len(signal)
    if n < 3:
        return []
    
    max_val = max(signal)
    if min_depth is None:
        min_depth = max_val - (max_val - min(signal)) * 0.1
    
    candidates = []
    for i in range(1, n - 1):
        if signal[i] < signal[i - 1] and signal[i] < signal[i + 1]:
            if signal[i] <= min_depth:
                candidates.append((i, signal[i]))
    
    # 按深度排序（越小越优先）
    candidates.sort(key=lambda x: x[1])
    
    result = []
    for idx, depth in candidates:
        if all(abs(idx - v) >= min_distance for v in result):
            result.append(idx)
    
    return sorted(result)


def detect_frequency(
    signal: List[float],
    sample_rate: float
) -> float:
    """
    检测信号的主频率
    
    Args:
        signal: 输入信号
        sample_rate: 采样率
    
    Returns:
        主频率 (Hz)
    
    Example:
        >>> wave = generate_sine_wave(440, 1.0)
        >>> freq = detect_frequency(wave, 44100)
        >>> # freq ≈ 440 Hz
    """
    n = len(signal)
    if n < 4:
        return 0.0
    
    # FFT
    spectrum = fft(signal)
    magnitude = fft_magnitude(spectrum)
    
    # 只看前半部分（正频率）
    half_n = n // 2
    
    # 找最大幅度对应的频率
    max_idx = 0
    max_mag = 0.0
    for i in range(1, half_n):  # 跳过 DC 分量 (i=0)
        if magnitude[i] > max_mag:
            max_mag = magnitude[i]
            max_idx = i
    
    # 计算频率
    return max_idx * sample_rate / n


def detect_multiple_frequencies(
    signal: List[float],
    sample_rate: float,
    num_freqs: int = 3,
    min_magnitude_ratio: float = 0.1
) -> List[Tuple[float, float]]:
    """
    检测信号的多个主要频率
    
    Args:
        signal: 输入信号
        sample_rate: 采样率
        num_freqs: 要检测的频率数量
        min_magnitude_ratio: 最小幅度比率（相对于最大幅度）
    
    Returns:
        (频率, 幅度) 列表
    """
    n = len(signal)
    if n < 4:
        return []
    
    spectrum = fft(signal)
    magnitude = fft_magnitude(spectrum)
    
    half_n = n // 2
    max_mag = max(magnitude[1:half_n])
    
    # 找所有显著的频率分量
    candidates = []
    for i in range(1, half_n):
        if magnitude[i] >= max_mag * min_magnitude_ratio:
            freq = i * sample_rate / n
            candidates.append((freq, magnitude[i]))
    
    # 按幅度排序，取前 num_freqs 个
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:num_freqs]


def calculate_energy(signal: List[float]) -> float:
    """
    计算信号能量
    
    Args:
        signal: 输入信号
    
    Returns:
        信号能量（平方和）
    """
    return sum(x ** 2 for x in signal)


def calculate_power(signal: List[float]) -> float:
    """
    计算信号平均功率
    
    Args:
        signal: 输入信号
    
    Returns:
        平均功率
    """
    if not signal:
        return 0.0
    return sum(x ** 2 for x in signal) / len(signal)


def calculate_rms(signal: List[float]) -> float:
    """
    计算信号 RMS（均方根）
    
    Args:
        signal: 输入信号
    
    Returns:
        RMS 值
    """
    if not signal:
        return 0.0
    return math.sqrt(sum(x ** 2 for x in signal) / len(signal))


def zero_crossing_rate(signal: List[float]) -> float:
    """
    计算零交叉率（信号穿越零点的频率）
    
    Args:
        signal: 输入信号
    
    Returns:
        零交叉率 (0-1)
    """
    if len(signal) < 2:
        return 0.0
    
    crossings = 0
    for i in range(1, len(signal)):
        if signal[i - 1] * signal[i] < 0:
            crossings += 1
        elif signal[i - 1] == 0 and signal[i] != 0:
            crossings += 1
    
    return crossings / (len(signal) - 1)


def signal_statistics(signal: List[float]) -> dict:
    """
    计算信号统计信息
    
    Args:
        signal: 输入信号
    
    Returns:
        包含均值、方差、标准差、最大值、最小值等的字典
    """
    if not signal:
        return {
            'mean': 0.0,
            'variance': 0.0,
            'std': 0.0,
            'max': 0.0,
            'min': 0.0,
            'range': 0.0,
            'rms': 0.0,
            'energy': 0.0,
            'power': 0.0
        }
    
    n = len(signal)
    mean = sum(signal) / n
    variance = sum((x - mean) ** 2 for x in signal) / n
    std = math.sqrt(variance)
    max_val = max(signal)
    min_val = min(signal)
    
    return {
        'mean': mean,
        'variance': variance,
        'std': std,
        'max': max_val,
        'min': min_val,
        'range': max_val - min_val,
        'rms': calculate_rms(signal),
        'energy': calculate_energy(signal),
        'power': calculate_power(signal)
    }


def autocorrelation(signal: List[float], max_lag: Optional[int] = None) -> List[float]:
    """
    计算信号自相关函数
    
    Args:
        signal: 输入信号
        max_lag: 最大滞后值
    
    Returns:
        自相关序列
    
    Example:
        >>> corr = autocorrelation([1, 2, 3, 4])
        >>> # corr[0] 最大（完全相关）
    """
    n = len(signal)
    if n < 2:
        return signal.copy() if signal else []
    
    if max_lag is None:
        max_lag = n - 1
    max_lag = min(max_lag, n - 1)
    
    mean = sum(signal) / n
    variance = sum((x - mean) ** 2 for x in signal)
    
    if variance == 0:
        return [1.0] * (max_lag + 1)
    
    result = []
    for lag in range(max_lag + 1):
        corr = sum((signal[i] - mean) * (signal[i + lag] - mean) for i in range(n - lag))
        result.append(corr / variance)
    
    return result


def cross_correlation(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    计算两个信号的互相关函数
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        互相关序列
    """
    n1, n2 = len(signal1), len(signal2)
    if n1 < 1 or n2 < 1:
        return []
    
    # 补零到相同长度
    max_len = max(n1, n2)
    s1 = signal1 + [0.0] * (max_len - n1)
    s2 = signal2 + [0.0] * (max_len - n2)
    
    mean1 = sum(s1) / max_len
    mean2 = sum(s2) / max_len
    std1 = math.sqrt(sum((x - mean1) ** 2 for x in s1))
    std2 = math.sqrt(sum((x - mean2) ** 2 for x in s2))
    
    if std1 == 0 or std2 == 0:
        return [0.0] * max_len
    
    result = []
    for lag in range(max_len):
        corr = 0.0
        for i in range(max_len):
            j = i + lag
            if j < max_len:
                corr += (s1[i] - mean1) * (s2[j] - mean2)
        result.append(corr / (std1 * std2 * max_len))
    
    return result


def spectral_centroid(
    spectrum: List[complex],
    sample_rate: float
) -> float:
    """
    计算频谱质心（"亮度"指标）
    
    Args:
        spectrum: FFT 频谱
        sample_rate: 采样率
    
    Returns:
        频谱质心 (Hz)
    """
    n = len(spectrum)
    magnitude = fft_magnitude(spectrum)
    
    total_mag = sum(magnitude[1:n // 2])  # 跳过 DC
    if total_mag == 0:
        return 0.0
    
    weighted_sum = 0.0
    for i in range(1, n // 2):
        freq = i * sample_rate / n
        weighted_sum += freq * magnitude[i]
    
    return weighted_sum / total_mag


def spectral_bandwidth(
    spectrum: List[complex],
    sample_rate: float,
    centroid: Optional[float] = None
) -> float:
    """
    计算频谱带宽
    
    Args:
        spectrum: FFT 频谱
        sample_rate: 采样率
        centroid: 频谱质心（可选，会自动计算）
    
    Returns:
        频谱带宽 (Hz)
    """
    if centroid is None:
        centroid = spectral_centroid(spectrum, sample_rate)
    
    n = len(spectrum)
    magnitude = fft_magnitude(spectrum)
    
    total_mag = sum(magnitude[1:n // 2])
    if total_mag == 0:
        return 0.0
    
    variance = 0.0
    for i in range(1, n // 2):
        freq = i * sample_rate / n
        variance += magnitude[i] * (freq - centroid) ** 2
    
    return math.sqrt(variance / total_mag)


# ============================================================================
# 信号操作模块
# ============================================================================

def convolve(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    信号卷积
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        卷积结果
    
    Example:
        >>> result = convolve([1, 2, 3], [0.5, 0.5])
        >>> # 结果：[0.5, 1.5, 2.5, 1.5]
    """
    n1, n2 = len(signal1), len(signal2)
    if n1 < 1 or n2 < 1:
        return []
    
    result_len = n1 + n2 - 1
    result = [0.0] * result_len
    
    for i in range(n1):
        for j in range(n2):
            result[i + j] += signal1[i] * signal2[j]
    
    return result


def convolve_fft(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    使用 FFT 计算卷积（更快）
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        卷积结果
    """
    n1, n2 = len(signal1), len(signal2)
    if n1 < 1 or n2 < 1:
        return []
    
    # 补零到卷积长度
    result_len = n1 + n2 - 1
    next_power = 1
    while next_power < result_len:
        next_power *= 2
    
    s1 = signal1 + [0.0] * (next_power - n1)
    s2 = signal2 + [0.0] * (next_power - n2)
    
    # FFT 卷积
    fft1 = fft(s1)
    fft2 = fft(s2)
    
    # 频域乘法
    product = [a * b for a, b in zip(fft1, fft2)]
    
    # IFFT
    result = ifft(product)
    
    return result[:result_len]


def normalize_signal(
    signal: List[float],
    target_max: float = 1.0
) -> List[float]:
    """
    归一化信号
    
    Args:
        signal: 输入信号
        target_max: 目标最大值
    
    Returns:
        归一化后的信号
    """
    if not signal:
        return []
    
    current_max = max(abs(x) for x in signal)
    if current_max == 0:
        return signal.copy()
    
    return [x * target_max / current_max for x in signal]


def normalize_to_range(
    signal: List[float],
    min_val: float = 0.0,
    max_val: float = 1.0
) -> List[float]:
    """
    归一化信号到指定范围
    
    Args:
        signal: 输入信号
        min_val: 目标最小值
        max_val: 目标最大值
    
    Returns:
        归一化后的信号
    """
    if not signal:
        return []
    
    signal_min = min(signal)
    signal_max = max(signal)
    
    if signal_max == signal_min:
        return [(min_val + max_val) / 2] * len(signal)
    
    return [
        min_val + (x - signal_min) * (max_val - min_val) / (signal_max - signal_min)
        for x in signal
    ]


def resample(
    signal: List[float],
    new_length: int
) -> List[float]:
    """
    重采样信号（线性插值）
    
    Args:
        signal: 输入信号
        new_length: 新的长度
    
    Returns:
        重采样后的信号
    """
    if new_length < 1:
        return []
    
    old_length = len(signal)
    if old_length < 2:
        return signal.copy() if signal else []
    
    if new_length == old_length:
        return signal.copy()
    
    result = []
    for i in range(new_length):
        # 计算在原信号中的位置
        pos = i * (old_length - 1) / (new_length - 1) if new_length > 1 else 0
        
        # 线性插值
        idx = int(pos)
        frac = pos - idx
        
        if idx >= old_length - 1:
            result.append(signal[-1])
        else:
            interpolated = signal[idx] * (1 - frac) + signal[idx + 1] * frac
            result.append(interpolated)
    
    return result


def interpolate_linear(
    signal: List[float],
    factor: int = 2
) -> List[float]:
    """
    线性插值（增加采样点）
    
    Args:
        signal: 输入信号
        factor: 插值因子
    
    Returns:
        插值后的信号
    """
    return resample(signal, len(signal) * factor)


def decimate(
    signal: List[float],
    factor: int = 2
) -> List[float]:
    """
    抽取（减少采样点）
    
    Args:
        signal: 输入信号
        factor: 抽取因子
    
    Returns:
        抽取后的信号
    """
    if factor < 1:
        raise ValueError("抽取因子必须 >= 1")
    
    return [signal[i] for i in range(0, len(signal), factor)]


def shift_signal(
    signal: List[float],
    shift: int,
    fill_value: float = 0.0
) -> List[float]:
    """
    时移信号
    
    Args:
        signal: 输入信号
        shift: 位移量（正数向前，负数向后）
        fill_value: 填充值
    
    Returns:
        时移后的信号
    """
    n = len(signal)
    if n == 0:
        return []
    
    result = [fill_value] * n
    
    if shift > 0:
        # 向前移
        for i in range(n - shift):
            result[i + shift] = signal[i]
    elif shift < 0:
        # 向后移
        for i in range(n + shift):
            result[i] = signal[i - shift]
    else:
        return signal.copy()
    
    return result


def reverse_signal(signal: List[float]) -> List[float]:
    """
    反转信号
    
    Args:
        signal: 输入信号
    
    Returns:
        反转后的信号
    """
    return signal[::-1]


def add_signals(signals: List[List[float]]) -> List[float]:
    """
    多信号叠加
    
    Args:
        signals: 信号列表
    
    Returns:
        叠加后的信号
    """
    if not signals:
        return []
    
    max_len = max(len(s) for s in signals)
    result = [0.0] * max_len
    
    for signal in signals:
        for i, val in enumerate(signal):
            result[i] += val
    
    return result


def multiply_signals(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    信号相乘
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        相乘后的信号
    """
    min_len = min(len(signal1), len(signal2))
    return [signal1[i] * signal2[i] for i in range(min_len)]


def scale_signal(signal: List[float], factor: float) -> List[float]:
    """
    缩放信号
    
    Args:
        signal: 输入信号
        factor: 缩放因子
    
    Returns:
        缩放后的信号
    """
    return [x * factor for x in signal]


def offset_signal(signal: List[float], offset: float) -> List[float]:
    """
    偏移信号（直流偏移）
    
    Args:
        signal: 输入信号
        offset: 偏移值
    
    Returns:
        偏移后的信号
    """
    return [x + offset for x in signal]


def envelope_detection(
    signal: List[float],
    method: str = 'absolute'
) -> List[float]:
    """
    包络检测
    
    Args:
        signal: 输入信号
        method: 检测方法 ('absolute', 'hilbert')
    
    Returns:
        包络信号
    
    Note:
        'hilbert' 方法使用简化实现
    """
    if method == 'absolute':
        # 取绝对值后平滑
        abs_signal = [abs(x) for x in signal]
        return exponential_smoothing(abs_signal, 0.3)
    elif method == 'hilbert':
        # 简化的 Hilbert 变换包络检测
        # 使用 FFT 方法
        spectrum = fft(signal)
        n = len(spectrum)
        
        # 创建 Hilbert 滤波器
        h = [complex(0, 0)] * n
        h[0] = 1.0
        for i in range(1, n // 2):
            h[i] = 2.0
        if n % 2 == 0:
            h[n // 2] = 1.0
        
        # 应用滤波器
        filtered = [s * h for s in spectrum]
        
        # IFFT
        analytic = ifft(filtered)
        
        # 包络 = sqrt(signal^2 + analytic^2)
        return [math.sqrt(s ** 2 + a ** 2) for s, a in zip(signal, analytic)]
    else:
        raise ValueError(f"未知方法: {method}")


def derivative(signal: List[float], order: int = 1) -> List[float]:
    """
    计算信号的导数
    
    Args:
        signal: 输入信号
        order: 导数阶数
    
    Returns:
        导数信号
    
    Example:
        >>> # 一阶导数（变化率）
        >>> deriv = derivative([1, 2, 4, 7, 11])
    """
    if order < 1:
        raise ValueError("阶数必须 >= 1")
    
    result = signal.copy()
    for _ in range(order):
        n = len(result)
        if n < 2:
            return []
        # 一阶导数：差分
        result = [result[i + 1] - result[i] for i in range(n - 1)]
    
    return result


def integral(signal: List[float], initial: float = 0.0) -> List[float]:
    """
    计算信号的积分
    
    Args:
        signal: 输入信号
        initial: 初始值
    
    Returns:
        积分信号
    """
    if not signal:
        return []
    
    result = [initial]
    cumsum = initial
    for x in signal:
        cumsum += x
        result.append(cumsum)
    
    return result


# ============================================================================
# 特殊信号处理
# ============================================================================

def window_function(
    n: int,
    window_type: str = 'hann'
) -> List[float]:
    """
    生成窗函数
    
    Args:
        n: 窗口长度
        window_type: 窗函数类型 ('rectangular', 'hann', 'hamming', 'blackman', 'gaussian')
    
    Returns:
        窗函数系数
    
    Example:
        >>> window = window_function(100, 'hann')
    """
    if window_type == 'rectangular':
        return [1.0] * n
    elif window_type == 'hann':
        return [0.5 * (1 - math.cos(2 * math.pi * i / (n - 1))) for i in range(n)]
    elif window_type == 'hamming':
        return [0.54 - 0.46 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]
    elif window_type == 'blackman':
        a0 = 0.42
        a1 = 0.5
        a2 = 0.08
        return [a0 - a1 * math.cos(2 * math.pi * i / (n - 1)) + a2 * math.cos(4 * math.pi * i / (n - 1)) 
                for i in range(n)]
    elif window_type == 'gaussian':
        sigma = n / 4
        center = (n - 1) / 2
        return [math.exp(-((i - center) ** 2) / (2 * sigma ** 2)) for i in range(n)]
    else:
        raise ValueError(f"未知窗函数: {window_type}")


def apply_window(signal: List[float], window_type: str = 'hann') -> List[float]:
    """
    对信号应用窗函数
    
    Args:
        signal: 输入信号
        window_type: 窗函数类型
    
    Returns:
        加窗后的信号
    """
    window = window_function(len(signal), window_type)
    return [s * w for s, w in zip(signal, window)]


def stft(
    signal: List[float],
    frame_size: int = 256,
    hop_size: int = 128,
    window_type: str = 'hann'
) -> List[List[complex]]:
    """
    短时傅里叶变换 (STFT)
    
    Args:
        signal: 输入信号
        frame_size: 帧大小
        hop_size: 步长
        window_type: 窗函数类型
    
    Returns:
        每帧的 FFT 结果列表
    
    Example:
        >>> frames = stft(audio_signal, 512, 256)
        >>> # 得到时间-频率表示
    """
    n = len(signal)
    if n < frame_size:
        return [fft(apply_window(signal, window_type))]
    
    num_frames = (n - frame_size) // hop_size + 1
    result = []
    
    for i in range(num_frames):
        start = i * hop_size
        frame = signal[start:start + frame_size]
        windowed = apply_window(frame, window_type)
        result.append(fft(windowed))
    
    return result


def istft(
    stft_frames: List[List[complex]],
    hop_size: int = 128,
    window_type: str = 'hann'
) -> List[float]:
    """
    短时傅里叶逆变换 (ISTFT)
    
    Args:
        stft_frames: STFT 帧
        hop_size: 步长
        window_type: 窗函数类型
    
    Returns:
        重构的信号
    """
    if not stft_frames:
        return []
    
    frame_size = len(stft_frames[0])
    num_frames = len(stft_frames)
    total_length = (num_frames - 1) * hop_size + frame_size
    
    result = [0.0] * total_length
    window_sum = [0.0] * total_length
    
    window = window_function(frame_size, window_type)
    
    for i, frame in enumerate(stft_frames):
        start = i * hop_size
        
        # IFFT
        time_frame = ifft(frame)
        
        # 加窗并叠加
        for j in range(frame_size):
            if start + j < total_length:
                result[start + j] += time_frame[j] * window[j]
                window_sum[start + j] += window[j] ** 2
    
    # 归一化（补偿窗函数重叠）
    for i in range(total_length):
        if window_sum[i] > 0:
            result[i] /= window_sum[i]
    
    return result


def spectrogram(
    signal: List[float],
    frame_size: int = 256,
    hop_size: int = 128,
    window_type: str = 'hann'
) -> List[List[float]]:
    """
    计算频谱图（时频分析）
    
    Args:
        signal: 输入信号
        frame_size: 帧大小
        hop_size: 步长
        window_type: 窗函数类型
    
    Returns:
        幅度频谱图（时间 x 频率）
    """
    stft_frames = stft(signal, frame_size, hop_size, window_type)
    return [fft_magnitude(frame) for frame in stft_frames]


# ============================================================================
# 实用工具
# ============================================================================

def silence_detection(
    signal: List[float],
    threshold: float = 0.01,
    min_duration: int = 10
) -> List[Tuple[int, int]]:
    """
    检测静音区间
    
    Args:
        signal: 输入信号
        threshold: 静音阈值
        min_duration: 最小静音长度
    
    Returns:
        (开始, 结束) 静音区间列表
    """
    n = len(signal)
    regions = []
    in_silence = False
    start = 0
    
    for i in range(n):
        if abs(signal[i]) < threshold:
            if not in_silence:
                in_silence = True
                start = i
        else:
            if in_silence:
                if i - start >= min_duration:
                    regions.append((start, i))
                in_silence = False
    
    # 处理结尾的静音
    if in_silence and n - start >= min_duration:
        regions.append((start, n))
    
    return regions


def signal_similarity(signal1: List[float], signal2: List[float]) -> float:
    """
    计算两个信号的相似度
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        相似度 (0-1)
    
    Note:
        使用归一化互相关
    """
    corr = cross_correlation(signal1, signal2)
    if not corr:
        return 0.0
    return max(corr)


def signal_difference(signal1: List[float], signal2: List[float]) -> List[float]:
    """
    计算两个信号的差异
    
    Args:
        signal1: 第一个信号
        signal2: 第二个信号
    
    Returns:
        差异信号
    """
    min_len = min(len(signal1), len(signal2))
    return [signal1[i] - signal2[i] for i in range(min_len)]


def threshold_signal(
    signal: List[float],
    threshold: float,
    mode: str = 'above'
) -> List[int]:
    """
    阈值化信号
    
    Args:
        signal: 输入信号
        threshold: 阈值
        mode: 模式 ('above', 'below', 'absolute')
    
    Returns:
        二值结果（0 或 1）
    """
    result = []
    for x in signal:
        if mode == 'above':
            result.append(1 if x > threshold else 0)
        elif mode == 'below':
            result.append(1 if x < threshold else 0)
        elif mode == 'absolute':
            result.append(1 if abs(x) > threshold else 0)
        else:
            raise ValueError(f"未知模式: {mode}")
    return result


def clip_signal(
    signal: List[float],
    min_val: float,
    max_val: float
) -> List[float]:
    """
    限制信号范围
    
    Args:
        signal: 输入信号
        min_val: 最小值
        max_val: 最大值
    
    Returns:
        裁剪后的信号
    """
    return [max(min_val, min(max_val, x)) for x in signal]


def fade_in(
    signal: List[float],
    fade_samples: int
) -> List[float]:
    """
    渐入效果
    
    Args:
        signal: 输入信号
        fade_samples: 渐入长度
    
    Returns:
        渐入后的信号
    """
    if fade_samples >= len(signal):
        fade_samples = len(signal)
    
    result = signal.copy()
    for i in range(fade_samples):
        factor = i / fade_samples
        result[i] *= factor
    
    return result


def fade_out(
    signal: List[float],
    fade_samples: int
) -> List[float]:
    """
    渐出效果
    
    Args:
        signal: 输入信号
        fade_samples: 渐出长度
    
    Returns:
        渐出后的信号
    """
    n = len(signal)
    if fade_samples >= n:
        fade_samples = n
    
    result = signal.copy()
    for i in range(fade_samples):
        factor = (fade_samples - i) / fade_samples
        result[n - fade_samples + i] *= factor
    
    return result


def fade_both(
    signal: List[float],
    fade_in_samples: int,
    fade_out_samples: int
) -> List[float]:
    """
    同时渐入渐出
    
    Args:
        signal: 输入信号
        fade_in_samples: 渐入长度
        fade_out_samples: 渐出长度
    
    Returns:
        处理后的信号
    """
    result = fade_in(signal, fade_in_samples)
    result = fade_out(result, fade_out_samples)
    return result


# 导出所有函数
__all__ = [
    # 信号生成
    'generate_sine_wave',
    'generate_square_wave',
    'generate_triangle_wave',
    'generate_sawtooth_wave',
    'generate_white_noise',
    'generate_pulse',
    'generate_chirp',
    'generate_custom_wave',
    'generate_harmonic_series',
    
    # 信号滤波
    'moving_average_filter',
    'median_filter',
    'exponential_smoothing',
    'lowpass_filter_simple',
    'highpass_filter_simple',
    'bandpass_filter_simple',
    'savitzky_golay_filter',
    'notch_filter',
    
    # 信号变换
    'fft',
    'ifft',
    'fft_magnitude',
    'fft_phase',
    'power_spectrum',
    'frequency_bins',
    'dft',
    
    # 信号分析
    'find_peaks',
    'find_valleys',
    'detect_frequency',
    'detect_multiple_frequencies',
    'calculate_energy',
    'calculate_power',
    'calculate_rms',
    'zero_crossing_rate',
    'signal_statistics',
    'autocorrelation',
    'cross_correlation',
    'spectral_centroid',
    'spectral_bandwidth',
    
    # 信号操作
    'convolve',
    'convolve_fft',
    'normalize_signal',
    'normalize_to_range',
    'resample',
    'interpolate_linear',
    'decimate',
    'shift_signal',
    'reverse_signal',
    'add_signals',
    'multiply_signals',
    'scale_signal',
    'offset_signal',
    'envelope_detection',
    'derivative',
    'integral',
    
    # 特殊处理
    'window_function',
    'apply_window',
    'stft',
    'istft',
    'spectrogram',
    
    # 实用工具
    'silence_detection',
    'signal_similarity',
    'signal_difference',
    'threshold_signal',
    'clip_signal',
    'fade_in',
    'fade_out',
    'fade_both',
]