"""
Spectral Utils - 滤波示例

演示信号滤波的基本用法
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate_composite_wave,
    compute_spectrum,
    find_peaks,
    low_pass_filter,
    high_pass_filter,
    band_pass_filter,
    compute_rms,
)


def example_low_pass_filter():
    """低通滤波示例"""
    print("\n" + "=" * 50)
    print("示例 1: 低通滤波")
    print("=" * 50)
    
    sample_rate = 1000.0
    cutoff = 100.0
    
    # 生成包含低频和高频的信号
    signal = generate_composite_wave(
        frequencies=[30.0, 300.0],
        amplitudes=[1.0, 1.0],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    print(f"\n原始信号:")
    print(f"  包含频率: 30 Hz (低频), 300 Hz (高频)")
    
    # 分析原始信号
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.2)
    
    print(f"  原始信号峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")
    
    # 低通滤波
    print(f"\n低通滤波:")
    print(f"  截止频率: {cutoff} Hz")
    
    filtered = low_pass_filter(signal, sample_rate, cutoff, order=4)
    
    # 分析滤波后信号
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.1)
    
    print(f"  滤波后峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")
    
    # RMS 比较
    print(f"\nRMS 比较:")
    print(f"  原始信号 RMS: {compute_rms(signal):.4f}")
    print(f"  滤波信号 RMS: {compute_rms(filtered):.4f}")


def example_high_pass_filter():
    """高通滤波示例"""
    print("\n" + "=" * 50)
    print("示例 2: 高通滤波")
    print("=" * 50)
    
    sample_rate = 1000.0
    cutoff = 100.0
    
    # 生成包含低频和高频的信号
    signal = generate_composite_wave(
        frequencies=[30.0, 300.0],
        amplitudes=[1.0, 1.0],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    print(f"\n原始信号:")
    print(f"  包含频率: 30 Hz (低频), 300 Hz (高频)")
    
    # 分析原始信号
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.2)
    
    print(f"  原始信号峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")
    
    # 高通滤波
    print(f"\n高通滤波:")
    print(f"  截止频率: {cutoff} Hz")
    
    filtered = high_pass_filter(signal, sample_rate, cutoff, order=4)
    
    # 分析滤波后信号
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.1)
    
    print(f"  滤波后峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")


def example_band_pass_filter():
    """带通滤波示例"""
    print("\n" + "=" * 50)
    print("示例 3: 带通滤波")
    print("=" * 50)
    
    sample_rate = 1000.0
    low_cutoff = 80.0
    high_cutoff = 150.0
    
    # 生成包含三个频率的信号
    signal = generate_composite_wave(
        frequencies=[30.0, 100.0, 300.0],
        amplitudes=[1.0, 1.0, 1.0],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    print(f"\n原始信号:")
    print(f"  包含频率: 30 Hz, 100 Hz, 300 Hz")
    
    # 分析原始信号
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.2)
    
    print(f"  原始信号峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")
    
    # 带通滤波
    print(f"\n带通滤波:")
    print(f"  通带范围: {low_cutoff} Hz - {high_cutoff} Hz")
    
    filtered = band_pass_filter(
        signal, sample_rate, low_cutoff, high_cutoff, order=4
    )
    
    # 分析滤波后信号
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.1)
    
    print(f"  滤波后峰值:")
    for peak in peaks:
        print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")


def example_filter_order():
    """滤波器阶数影响示例"""
    print("\n" + "=" * 50)
    print("示例 4: 滤波器阶数的影响")
    print("=" * 50)
    
    sample_rate = 1000.0
    cutoff = 100.0
    
    # 生成信号
    signal = generate_composite_wave(
        frequencies=[50.0, 200.0],
        amplitudes=[1.0, 0.5],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    print(f"\n测试不同阶数的低通滤波:")
    print(f"  截止频率: {cutoff} Hz")
    
    for order in [1, 2, 4, 6]:
        filtered = low_pass_filter(signal, sample_rate, cutoff, order=order)
        
        spectrum = compute_spectrum(filtered, sample_rate)
        peaks = find_peaks(spectrum, threshold=0.1)
        
        print(f"\n  阶数 {order}:")
        for peak in peaks:
            print(f"    {peak.frequency:.2f} Hz, 幅值: {peak.magnitude:.4f}")
        
        rms = compute_rms(filtered)
        print(f"    RMS: {rms:.4f}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("Spectral Utils - 滤波示例")
    print("=" * 50)
    
    example_low_pass_filter()
    example_high_pass_filter()
    example_band_pass_filter()
    example_filter_order()
    
    print("\n" + "=" * 50)
    print("示例完成")
    print("=" * 50)


if __name__ == "__main__":
    main()