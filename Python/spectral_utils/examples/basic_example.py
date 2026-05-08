"""
Spectral Utils - 基础示例

演示频谱分析的基本用法
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate_sine_wave,
    generate_composite_wave,
    compute_spectrum,
    find_peaks,
    detect_dominant_frequency,
    compute_rms,
)


def example_single_frequency():
    """单频率信号分析示例"""
    print("\n" + "=" * 50)
    print("示例 1: 单频率正弦波分析")
    print("=" * 50)
    
    # 参数设置
    frequency = 100.0        # 100 Hz
    sample_rate = 1000.0     # 1 kHz 采样率
    duration = 1.0           # 1 秒
    
    print(f"\n生成信号:")
    print(f"  频率: {frequency} Hz")
    print(f"  采样率: {sample_rate} Hz")
    print(f"  持续时间: {duration} 秒")
    
    # 生成正弦波
    signal = generate_sine_wave(frequency, sample_rate, duration)
    print(f"  信号长度: {len(signal)} 个采样点")
    
    # 频谱分析
    spectrum = compute_spectrum(signal, sample_rate)
    
    # 检测峰值
    peaks = find_peaks(spectrum, threshold=0.1)
    
    print("\n检测结果:")
    for peak in peaks:
        print(f"  频率: {peak.frequency:.2f} Hz")
        print(f"  幅值: {peak.magnitude:.4f}")
        print(f"  相位: {peak.phase:.2f} rad")
    
    # 主频率检测
    dominant = detect_dominant_frequency(signal, sample_rate)
    print(f"\n主频率: {dominant:.2f} Hz")
    print(f"误差: {abs(dominant - frequency):.2f} Hz")


def example_composite_signal():
    """多频率复合信号分析示例"""
    print("\n" + "=" * 50)
    print("示例 2: 多频率复合信号分析")
    print("=" * 50)
    
    # 参数设置
    frequencies = [50.0, 150.0, 300.0]   # 三个频率分量
    amplitudes = [1.0, 0.7, 0.3]         # 不同幅值
    sample_rate = 1000.0
    
    print(f"\n生成复合信号:")
    print(f"  频率分量: {frequencies} Hz")
    print(f"  幅值: {amplitudes}")
    
    # 生成复合波
    signal = generate_composite_wave(frequencies, amplitudes, sample_rate, 1.0)
    print(f"  信号长度: {len(signal)} 个采样点")
    
    # 频谱分析
    spectrum = compute_spectrum(signal, sample_rate)
    
    # 检测峰值
    peaks = find_peaks(spectrum, threshold=0.05)
    
    print("\n检测到的峰值:")
    for peak in peaks:
        # 找到最接近的预设频率
        closest_freq = min(frequencies, key=lambda f: abs(f - peak.frequency))
        print(f"  检测: {peak.frequency:.2f} Hz (预设: {closest_freq:.0f} Hz, "
              f"幅值: {peak.magnitude:.4f})")


def example_rms_analysis():
    """RMS 分析示例"""
    print("\n" + "=" * 50)
    print("示例 3: RMS 分析")
    print("=" * 50)
    
    sample_rate = 1000.0
    
    # 单位正弦波
    signal = generate_sine_wave(100.0, sample_rate, 1.0, amplitude=1.0)
    rms = compute_rms(signal)
    
    import math
    expected = 1.0 / math.sqrt(2)
    
    print(f"\n单位正弦波 RMS:")
    print(f"  计算值: {rms:.6f}")
    print(f"  理论值: {expected:.6f}")
    print(f"  误差: {abs(rms - expected):.6f}")
    
    # 不同幅值
    for amp in [0.5, 1.0, 2.0, 5.0]:
        signal = generate_sine_wave(100.0, sample_rate, 1.0, amplitude=amp)
        rms = compute_rms(signal)
        print(f"\n幅值 {amp} 的正弦波 RMS: {rms:.6f} (理论: {amp/math.sqrt(2):.6f})")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("Spectral Utils - 基础示例")
    print("=" * 50)
    
    example_single_frequency()
    example_composite_signal()
    example_rms_analysis()
    
    print("\n" + "=" * 50)
    print("示例完成")
    print("=" * 50)


if __name__ == "__main__":
    main()