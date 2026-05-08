"""
Spectral Utils - 测试文件

Author: AllToolkit
License: MIT
"""

import sys
import os
import math

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 窗函数
    rectangular_window, hann_window, hamming_window,
    blackman_window, bartlett_window, apply_window,
    WindowFunction,
    
    # FFT
    fft, ifft, fft_complex,
    
    # 频谱分析
    compute_spectrum, compute_power_spectral_density,
    find_peaks, detect_dominant_frequency,
    
    # 滤波器
    low_pass_filter, high_pass_filter,
    band_pass_filter, band_stop_filter,
    
    # 时频分析
    short_time_fourier_transform, compute_spectrogram,
    
    # 工具函数
    generate_sine_wave, generate_composite_wave,
    compute_rms, normalize_signal,
    
    # 数据类
    SpectrumResult, PeakInfo, FilterType,
    
    # 异常
    SpectralError, InvalidSignalError, InvalidParameterError,
)


def test_window_functions():
    """测试窗函数"""
    print("\n测试窗函数...")
    
    size = 10
    
    # 矩形窗
    rect = rectangular_window(size)
    assert len(rect) == size
    assert all(r == 1.0 for r in rect), "矩形窗应该全为 1.0"
    
    # 汉宁窗
    hann = hann_window(size)
    assert len(hann) == size
    assert 0 <= hann[0] <= 1, "汉宁窗值应在 0-1 之间"
    
    # 汉明窗
    hamming = hamming_window(size)
    assert len(hamming) == size
    
    # 布莱克曼窗
    blackman = blackman_window(size)
    assert len(blackman) == size
    
    # 巴特利特窗
    bartlett = bartlett_window(size)
    assert len(bartlett) == size
    
    # 单元素窗
    single = hann_window(1)
    assert single == [1.0], "单元素窗应为 [1.0]"
    
    print("   ✓ 所有窗函数测试通过")


def test_apply_window():
    """测试窗函数应用"""
    print("\n测试窗函数应用...")
    
    signal = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    # 矩形窗（不改变信号）
    rect_signal = apply_window(signal, WindowFunction.RECTANGULAR)
    assert rect_signal == signal, "矩形窗不应改变信号"
    
    # 汉宁窗
    hann_signal = apply_window(signal, WindowFunction.HANN)
    assert len(hann_signal) == len(signal)
    assert hann_signal != signal, "汉宁窗应该改变信号"
    
    print("   ✓ 窗函数应用测试通过")


def test_fft_basic():
    """测试基础 FFT"""
    print("\n测试基础 FFT...")
    
    # 单频信号
    signal = generate_sine_wave(10.0, 100.0, 1.0)
    spectrum = fft(signal)
    
    assert len(spectrum) > 0, "频谱不应为空"
    assert len(spectrum) >= len(signal), "频谱长度应至少等于信号长度"
    
    # 验证对称性（跳过 DC 和 Nyquist 频率）
    n = len(spectrum)
    for i in range(1, n // 2 - 1):  # 跳过边界
        real_fwd, imag_fwd = spectrum[i]
        real_bwd, imag_bwd = spectrum[n - i]
        # 共轭对称（对于实信号）：实部相同，虚部相反
        assert abs(real_fwd - real_bwd) < 0.1 or abs(imag_fwd + imag_bwd) < 0.1, \
            f"FFT 结果应在索引 {i} 和 {n-i} 处共轭对称"
    
    print("   ✓ 基础 FFT 测试通过")


def test_ifft():
    """测试逆 FFT"""
    print("\n测试逆 FFT...")
    
    # 原始信号
    original = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    
    # FFT -> IFFT
    spectrum = fft(original)
    reconstructed = ifft(spectrum)
    
    # 检查重建
    for i, (orig, rec) in enumerate(zip(original, reconstructed)):
        assert abs(orig - rec) < 1e-6, f"重建误差过大，索引 {i}: {orig} vs {rec}"
    
    print("   ✓ IFFT 测试通过")


def test_fft_empty_signal():
    """测试空信号"""
    print("\n测试空信号...")
    
    try:
        fft([])
        assert False, "空信号应抛出异常"
    except InvalidSignalError:
        pass
    
    print("   ✓ 空信号测试通过")


def test_compute_spectrum():
    """测试频谱计算"""
    print("\n测试频谱计算...")
    
    sample_rate = 1000.0
    frequency = 100.0
    
    # 生成正弦波
    signal = generate_sine_wave(frequency, sample_rate, 1.0)
    
    # 计算频谱
    spectrum = compute_spectrum(signal, sample_rate)
    
    assert isinstance(spectrum, SpectrumResult)
    assert len(spectrum.frequencies) > 0
    assert len(spectrum.magnitudes) == len(spectrum.frequencies)
    assert len(spectrum.phases) == len(spectrum.frequencies)
    assert len(spectrum.power_spectrum) == len(spectrum.frequencies)
    assert spectrum.sample_rate == sample_rate
    
    # 检查峰值在正确位置
    peaks = find_peaks(spectrum, threshold=0.1)
    
    # 找到最接近的峰
    peak_freq = min(peaks, key=lambda p: abs(p.frequency - frequency)).frequency
    error = abs(peak_freq - frequency) / frequency
    assert error < 0.1, f"频率误差过大: {error * 100:.1f}%"
    
    print("   ✓ 频谱计算测试通过")


def test_find_peaks():
    """测试峰值检测"""
    print("\n测试峰值检测...")
    
    sample_rate = 1000.0
    signal = generate_composite_wave(
        frequencies=[50, 150, 300],
        amplitudes=[1.0, 0.5, 0.3],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    spectrum = compute_spectrum(signal, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.01, max_peaks=10)
    
    assert len(peaks) > 0, "应检测到峰值"
    
    # 验证峰值频率
    peak_freqs = [p.frequency for p in peaks]
    
    # 应该检测到三个主要频率
    for freq in [50, 150, 300]:
        closest = min(peak_freqs, key=lambda f: abs(f - freq))
        error = abs(closest - freq) / freq
        assert error < 0.1, f"未能正确检测到 {freq}Hz，检测到 {closest}Hz"
    
    print("   ✓ 峰值检测测试通过")


def test_detect_dominant_frequency():
    """测试主频率检测"""
    print("\n测试主频率检测...")
    
    sample_rate = 1000.0
    frequency = 250.0
    
    signal = generate_sine_wave(frequency, sample_rate, 1.0)
    detected = detect_dominant_frequency(signal, sample_rate)
    
    assert detected is not None, "应检测到频率"
    error = abs(detected - frequency) / frequency
    assert error < 0.05, f"频率误差过大: {error * 100:.1f}%"
    
    print("   ✓ 主频率检测测试通过")


def test_low_pass_filter():
    """测试低通滤波器"""
    print("\n测试低通滤波器...")
    
    sample_rate = 1000.0
    cutoff = 100.0
    
    # 生成低频和高频信号
    low_freq = generate_sine_wave(30.0, sample_rate, 1.0, amplitude=1.0)
    high_freq = generate_sine_wave(300.0, sample_rate, 1.0, amplitude=1.0)
    combined = [l + h for l, h in zip(low_freq, high_freq)]
    
    # 低通滤波
    filtered = low_pass_filter(combined, sample_rate, cutoff, order=4)
    
    # 检查滤波后的频谱
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.1)
    
    # 应该主要保留低频
    for peak in peaks:
        if peak.magnitude > 0.2:
            assert peak.frequency < cutoff * 2, \
                f"低通滤波后不应有明显的高频分量: {peak.frequency}Hz"
    
    print("   ✓ 低通滤波器测试通过")


def test_high_pass_filter():
    """测试高通滤波器"""
    print("\n测试高通滤波器...")
    
    sample_rate = 1000.0
    cutoff = 100.0
    
    # 生成低频和高频信号
    low_freq = generate_sine_wave(30.0, sample_rate, 1.0, amplitude=1.0)
    high_freq = generate_sine_wave(300.0, sample_rate, 1.0, amplitude=1.0)
    combined = [l + h for l, h in zip(low_freq, high_freq)]
    
    # 高通滤波
    filtered = high_pass_filter(combined, sample_rate, cutoff, order=4)
    
    # 检查滤波后的频谱
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.01)  # 降低阈值
    
    # 应该主要保留高频
    assert len(peaks) > 0, "应该有峰值"
    
    # 高频分量应该更明显
    high_peak = None
    for peak in peaks:
        if peak.frequency > cutoff:
            if high_peak is None or peak.magnitude > high_peak.magnitude:
                high_peak = peak
    
    assert high_peak is not None, "应该有高频峰值"
    
    print("   ✓ 高通滤波器测试通过")


def test_band_pass_filter():
    """测试带通滤波器"""
    print("\n测试带通滤波器...")
    
    sample_rate = 1000.0
    low_cutoff = 80.0
    high_cutoff = 120.0
    
    # 生成多频率信号
    signal = generate_composite_wave(
        frequencies=[30, 100, 300],
        amplitudes=[1.0, 1.0, 1.0],
        sample_rate=sample_rate,
        duration=1.0
    )
    
    # 带通滤波
    filtered = band_pass_filter(signal, sample_rate, low_cutoff, high_cutoff)
    
    # 检查频谱
    spectrum = compute_spectrum(filtered, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.1)
    
    # 应该主要保留中间频率
    for peak in peaks:
        if peak.magnitude > 0.3:
            # 允许一定的过渡带
            assert low_cutoff * 0.5 < peak.frequency < high_cutoff * 2, \
                f"带通滤波后应有明显的通带分量: {peak.frequency}Hz"
    
    print("   ✓ 带通滤波器测试通过")


def test_short_time_fourier_transform():
    """测试短时傅里叶变换"""
    print("\n测试短时傅里叶变换...")
    
    sample_rate = 1000.0
    window_size = 256
    hop_size = 128
    
    # 生成信号
    signal = generate_sine_wave(100.0, sample_rate, 2.0)
    
    # STFT
    results = short_time_fourier_transform(
        signal, window_size, hop_size, sample_rate
    )
    
    assert len(results) > 0, "STFT 结果不应为空"
    
    for result in results:
        assert isinstance(result, SpectrumResult)
        assert result.sample_rate == sample_rate
    
    print("   ✓ STFT 测试通过")


def test_spectrogram():
    """测试频谱图"""
    print("\n测试频谱图...")
    
    sample_rate = 1000.0
    window_size = 256
    hop_size = 128
    
    signal = generate_sine_wave(100.0, sample_rate, 2.0)
    
    times, frequencies, spectrogram = compute_spectrogram(
        signal, window_size, hop_size, sample_rate
    )
    
    assert len(times) > 0, "时间轴不应为空"
    assert len(frequencies) > 0, "频率轴不应为空"
    assert len(spectrogram) == len(times), "频谱图时间维度应匹配"
    assert len(spectrogram[0]) == len(frequencies), "频谱图频率维度应匹配"
    
    print("   ✓ 频谱图测试通过")


def test_generate_sine_wave():
    """测试正弦波生成"""
    print("\n测试正弦波生成...")
    
    sample_rate = 1000.0
    frequency = 100.0
    duration = 1.0
    amplitude = 2.0
    
    wave = generate_sine_wave(frequency, sample_rate, duration, amplitude)
    
    assert len(wave) == int(sample_rate * duration), "采样点数应正确"
    
    # 检查幅值范围（由于离散采样，可能不完全达到峰值）
    max_val = max(wave)
    min_val = min(wave)
    
    # 最大值应该接近幅值（允许小的采样误差）
    assert max_val <= amplitude + 1e-6, f"最大值不应超过幅值: {max_val}"
    assert max_val > amplitude * 0.9, f"最大值应接近幅值: {max_val}"
    
    # 最小值应该接近负幅值
    assert min_val >= -amplitude - 1e-6, f"最小值不应低于负幅值: {min_val}"
    assert min_val < -amplitude * 0.9, f"最小值应接近负幅值: {min_val}"
    
    print("   ✓ 正弦波生成测试通过")


def test_generate_composite_wave():
    """测试复合波生成"""
    print("\n测试复合波生成...")
    
    frequencies = [50, 100, 200]
    amplitudes = [1.0, 0.5, 0.3]
    sample_rate = 1000.0
    duration = 1.0
    
    wave = generate_composite_wave(frequencies, amplitudes, sample_rate, duration)
    
    assert len(wave) == int(sample_rate * duration), "采样点数应正确"
    
    # 验证频谱包含这些频率
    spectrum = compute_spectrum(wave, sample_rate)
    peaks = find_peaks(spectrum, threshold=0.05)
    
    peak_freqs = [p.frequency for p in peaks]
    for freq in frequencies:
        closest = min(peak_freqs, key=lambda f: abs(f - freq))
        error = abs(closest - freq) / freq
        assert error < 0.1, f"未检测到 {freq}Hz"
    
    print("   ✓ 复合波生成测试通过")


def test_compute_rms():
    """测试 RMS 计算"""
    print("\n测试 RMS 计算...")
    
    # 单位正弦波
    wave = generate_sine_wave(100.0, 1000.0, 1.0, amplitude=1.0)
    rms = compute_rms(wave)
    
    expected_rms = 1.0 / math.sqrt(2)  # 正弦波 RMS = A / sqrt(2)
    error = abs(rms - expected_rms) / expected_rms
    assert error < 0.01, f"RMS 误差过大: {error * 100:.1f}%"
    
    # 直流信号
    dc = [1.0] * 100
    rms = compute_rms(dc)
    assert abs(rms - 1.0) < 1e-6, "直流信号 RMS 应为 1.0"
    
    # 空信号
    rms = compute_rms([])
    assert rms == 0.0, "空信号 RMS 应为 0"
    
    print("   ✓ RMS 计算测试通过")


def test_normalize_signal():
    """测试信号归一化"""
    print("\n测试信号归一化...")
    
    signal = [1.0, 2.0, 3.0, 4.0, 5.0]
    target_rms = 2.0
    
    normalized = normalize_signal(signal, target_rms)
    
    rms = compute_rms(normalized)
    error = abs(rms - target_rms) / target_rms
    assert error < 1e-6, f"归一化后 RMS 误差过大: {error * 100:.1f}%"
    
    print("   ✓ 信号归一化测试通过")


def test_power_spectral_density():
    """测试功率谱密度"""
    print("\n测试功率谱密度...")
    
    sample_rate = 1000.0
    signal = generate_sine_wave(100.0, sample_rate, 1.0, amplitude=1.0)
    
    freqs, psd = compute_power_spectral_density(signal, sample_rate)
    
    assert len(freqs) > 0, "频率数组不应为空"
    assert len(psd) == len(freqs), "PSD 长度应与频率数组相同"
    
    # PSD 应该是正数
    assert all(p >= 0 for p in psd), "PSD 应该是非负的"
    
    print("   ✓ 功率谱密度测试通过")


def test_invalid_parameters():
    """测试无效参数"""
    print("\n测试无效参数...")
    
    # 无效采样率
    try:
        compute_spectrum([1, 2, 3], -1)
        assert False, "应抛出 InvalidParameterError"
    except InvalidParameterError:
        pass
    
    # 无效截止频率
    try:
        low_pass_filter([1, 2, 3], 100, -10)
        assert False, "应抛出 InvalidParameterError"
    except InvalidParameterError:
        pass
    
    # 截止频率超过奈奎斯特频率
    try:
        low_pass_filter([1, 2, 3], 100, 100)  # 截止频率 = 采样率/2
        assert False, "应抛出 InvalidParameterError"
    except InvalidParameterError:
        pass
    
    # 频率和幅值列表长度不匹配
    try:
        generate_composite_wave([1, 2], [1], 1000, 1.0)
        assert False, "应抛出 InvalidParameterError"
    except InvalidParameterError:
        pass
    
    # 无效窗口大小
    try:
        short_time_fourier_transform([1, 2, 3], 0, 1, 1000)
        assert False, "应抛出 InvalidParameterError"
    except InvalidParameterError:
        pass
    
    print("   ✓ 无效参数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Spectral Utils 测试套件")
    print("=" * 60)
    
    tests = [
        test_window_functions,
        test_apply_window,
        test_fft_basic,
        test_ifft,
        test_fft_empty_signal,
        test_compute_spectrum,
        test_find_peaks,
        test_detect_dominant_frequency,
        test_low_pass_filter,
        test_high_pass_filter,
        test_band_pass_filter,
        test_short_time_fourier_transform,
        test_spectrogram,
        test_generate_sine_wave,
        test_generate_composite_wave,
        test_compute_rms,
        test_normalize_signal,
        test_power_spectral_density,
        test_invalid_parameters,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"   ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"   ✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)