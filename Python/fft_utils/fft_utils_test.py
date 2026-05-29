"""
FFT Utils 测试套件

测试:
- DFT/IDFT 基本功能
- FFT/IFFT 基本功能和正确性
- RFFT/IRFFT 实数优化
- 窗函数生成
- 频谱分析
- 峰值检测
- 卷积和相关性
- 信号生成
- 工具函数
"""

import pytest
import math
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # DFT
    dft, idft,
    # FFT
    fft, ifft,
    # RFFT
    rfft, irfft,
    # 窗函数
    WindowType,
    rectangular_window, hanning_window, hamming_window,
    blackman_window, bartlett_window, kaiser_window,
    get_window, apply_window,
    # 频谱分析
    compute_frequencies, compute_frequencies_rfft,
    magnitude_spectrum, phase_spectrum, power_spectrum,
    power_spectral_density, analyze_spectrum,
    # 峰值检测
    find_peaks, find_harmonics,
    # 卷积和相关性
    convolve, correlate, autocorrelate,
    # 信号生成
    generate_sine, generate_cosine, generate_chirp,
    # 工具函数
    zero_pad, pad_to_power_of_two, dc_offset, remove_dc,
    resample, normalize_signal,
    _next_power_of_two, _bit_reverse,
    SpectrumResult
)


class TestHelperFunctions:
    """辅助函数测试"""
    
    def test_next_power_of_two(self):
        """测试计算下一个 2 的幂"""
        assert _next_power_of_two(0) == 1
        assert _next_power_of_two(1) == 1
        assert _next_power_of_two(2) == 2
        assert _next_power_of_two(3) == 4
        assert _next_power_of_two(5) == 8
        assert _next_power_of_two(16) == 16
        assert _next_power_of_two(17) == 32
        assert _next_power_of_two(1024) == 1024
        assert _next_power_of_two(1025) == 2048
    
    def test_bit_reverse(self):
        """测试位反转"""
        # 3 位反转
        assert _bit_reverse(0, 3) == 0
        assert _bit_reverse(1, 3) == 4
        assert _bit_reverse(2, 3) == 2
        assert _bit_reverse(3, 3) == 6
        assert _bit_reverse(4, 3) == 1
        assert _bit_reverse(5, 3) == 5
        assert _bit_reverse(6, 3) == 3
        assert _bit_reverse(7, 3) == 7


class TestDFT:
    """DFT/IDFT 测试"""
    
    def test_dft_empty(self):
        """测试空信号 DFT"""
        assert dft([]) == []
    
    def test_idft_empty(self):
        """测试空频谱 IDFT"""
        assert idft([]) == []
    
    def test_dft_single(self):
        """测试单点 DFT"""
        signal = [5.0]
        result = dft(signal)
        assert len(result) == 1
        assert abs(result[0].real - 5.0) < 1e-10
        assert abs(result[0].imag) < 1e-10
    
    def test_dft_dc(self):
        """测试直流信号 DFT"""
        signal = [1.0, 1.0, 1.0, 1.0]
        result = dft(signal)
        # DC 分量应该在索引 0
        assert abs(result[0].real - 4.0) < 1e-10
        # 其他分量应该为 0
        for i in range(1, 4):
            assert abs(result[i]) < 1e-10
    
    def test_dft_sine(self):
        """测试正弦信号 DFT"""
        n = 8
        # 一个完整的正弦周期
        signal = [math.sin(2 * math.pi * i / n) for i in range(n)]
        result = dft(signal)
        
        # 正弦波应该在第 1 和第 7 个频率 bin
        assert abs(result[0]) < 1e-10  # DC 为 0
        assert abs(result[1]) > 1.0  # 基频分量
        for i in range(2, 6):
            assert abs(result[i]) < 1e-10  # 其他谐波为 0
    
    def test_idft_reconstruction(self):
        """测试 IDFT 重建"""
        signal = [1, 2, 3, 4, 5, 6, 7, 8]
        spectrum = dft(signal)
        reconstructed = idft(spectrum)
        
        assert len(reconstructed) == len(signal)
        for i in range(len(signal)):
            assert abs(reconstructed[i].real - signal[i]) < 1e-10
            assert abs(reconstructed[i].imag) < 1e-10
    
    def test_dft_linearity(self):
        """测试 DFT 线性性"""
        a = [1, 2, 3, 4]
        b = [5, 6, 7, 8]
        
        # DFT(a + b) = DFT(a) + DFT(b)
        dft_a = dft(a)
        dft_b = dft(b)
        dft_sum = dft([x + y for x, y in zip(a, b)])
        
        for i in range(len(a)):
            expected = dft_a[i] + dft_b[i]
            assert abs(dft_sum[i] - expected) < 1e-10


class TestFFT:
    """FFT/IFFT 测试"""
    
    def test_fft_empty(self):
        """测试空信号 FFT"""
        assert fft([]) == []
    
    def test_ifft_empty(self):
        """测试空频谱 IFFT"""
        assert ifft([]) == []
    
    def test_fft_single(self):
        """测试单点 FFT"""
        result = fft([5.0])
        assert len(result) == 1
        assert abs(result[0].real - 5.0) < 1e-10
    
    def test_fft_power_of_two(self):
        """测试 2 的幂次长度 FFT"""
        signal = [i for i in range(16)]
        result = fft(signal)
        assert len(result) == 16
    
    def test_fft_non_power_of_two(self):
        """测试非 2 的幂次长度 FFT (自动使用 DFT)"""
        signal = [i for i in range(10)]
        result = fft(signal, zero_pad=False)
        assert len(result) == 10
        
        # 验证与 DFT 结果一致
        dft_result = dft(signal)
        for i in range(10):
            assert abs(result[i] - dft_result[i]) < 1e-10
    
    def test_fft_zero_pad(self):
        """测试零填充 FFT"""
        signal = [1, 2, 3, 4, 5]  # 长度 5，填充到 8
        result = fft(signal, zero_pad=True)
        assert len(result) == 8
    
    def test_fft_dc(self):
        """测试直流信号 FFT"""
        signal = [1.0] * 8
        result = fft(signal)
        
        # DC 分量
        assert abs(result[0].real - 8.0) < 1e-10
        # 其他分量应该为 0
        for i in range(1, 8):
            assert abs(result[i]) < 1e-10
    
    def test_fft_sine(self):
        """测试正弦信号 FFT"""
        n = 64
        freq = 4  # 4 个完整周期
        signal = [math.sin(2 * math.pi * freq * i / n) for i in range(n)]
        result = fft(signal)
        
        # 应该在第 4 个频率 bin 有峰值
        mags = [abs(r) for r in result]
        peak_idx = mags.index(max(mags))
        assert peak_idx == freq or peak_idx == n - freq  # 对称性
    
    def test_ifft_reconstruction(self):
        """测试 IFFT 重建"""
        signal = [1, 2, 3, 4, 5, 6, 7, 8]
        spectrum = fft(signal)
        reconstructed = ifft(spectrum)
        
        assert len(reconstructed) == len(signal)
        for i in range(len(signal)):
            assert abs(reconstructed[i].real - signal[i]) < 1e-10
            assert abs(reconstructed[i].imag) < 1e-10
    
    def test_fft_vs_dft(self):
        """测试 FFT 与 DFT 结果一致性"""
        signal = [i * 0.1 for i in range(8)]
        fft_result = fft(signal)
        dft_result = dft(signal)
        
        for i in range(8):
            assert abs(fft_result[i] - dft_result[i]) < 1e-10
    
    def test_fft_complex_input(self):
        """测试复数输入"""
        signal = [complex(1, 1), complex(2, -1), complex(3, 2), complex(4, -2)]
        result = fft(signal)
        assert len(result) == 4
        
        # 验证可逆性
        reconstructed = ifft(result)
        for i in range(4):
            assert abs(reconstructed[i] - signal[i]) < 1e-10


class TestRFFT:
    """RFFT/IRFFT 测试"""
    
    def test_rfft_empty(self):
        """测试空信号 RFFT"""
        assert rfft([]) == []
    
    def test_rfft_single(self):
        """测试单点 RFFT"""
        result = rfft([5.0])
        assert len(result) == 1  # n=1: 1 // 2 + 1 = 1
    
    def test_rfft_length(self):
        """测试 RFFT 输出长度"""
        signal = [1.0] * 8
        result = rfft(signal)
        assert len(result) == 5  # 8 // 2 + 1
    
    def test_rfft_dc(self):
        """测试直流信号 RFFT"""
        signal = [2.0] * 16
        result = rfft(signal)
        
        # DC 分量
        assert abs(result[0].real - 32.0) < 1e-10
        # 其他分量
        for i in range(1, len(result)):
            assert abs(result[i]) < 1e-10
    
    def test_rfft_symmetry(self):
        """测试 RFFT 频谱对称性"""
        signal = [math.sin(2 * math.pi * i / 16) for i in range(16)]
        full_fft = fft(signal, zero_pad=True)
        rfft_result = rfft(signal)
        
        # RFFT 结果应该等于 FFT 结果的前半部分
        for i in range(len(rfft_result)):
            diff = abs(rfft_result[i] - full_fft[i])
            assert diff < 1e-10
    
    def test_irfft_reconstruction(self):
        """测试 IRFFT 重建"""
        signal = [1, 2, 3, 4, 5, 6, 7, 8]  # 使用 2 的幂次长度更稳定
        spectrum = rfft(signal)
        reconstructed = irfft(spectrum, n=len(signal))
        
        assert len(reconstructed) == len(signal)
        for i in range(len(signal)):
            assert abs(reconstructed[i] - signal[i]) < 1e-10
    
    def test_irfft_with_n(self):
        """测试指定输出长度的 IRFFT"""
        signal = [1, 2, 3, 4, 5, 6, 7, 8]
        spectrum = rfft(signal)
        
        # 重建为原长度
        reconstructed = irfft(spectrum, n=8)
        assert len(reconstructed) == 8


class TestWindows:
    """窗函数测试"""
    
    def test_rectangular_window(self):
        """测试矩形窗"""
        w = rectangular_window(10)
        assert len(w) == 10
        assert all(x == 1.0 for x in w)
    
    def test_hanning_window(self):
        """测试汉宁窗"""
        w = hanning_window(10)
        assert len(w) == 10
        # 两端应该接近 0
        assert w[0] < 0.1
        assert w[-1] < 0.1
        # 中间应该最大
        assert w[4] > 0.8
    
    def test_hamming_window(self):
        """测试汉明窗"""
        w = hamming_window(10)
        assert len(w) == 10
        # 边缘值不应该为 0 (与 Hanning 不同)
        assert w[0] > 0.05
    
    def test_blackman_window(self):
        """测试布莱克曼窗"""
        w = blackman_window(10)
        assert len(w) == 10
        # 两端应该接近 0
        assert w[0] < 0.01
    
    def test_bartlett_window(self):
        """测试巴特利特窗"""
        w = bartlett_window(10)
        assert len(w) == 10
        # 两端应该接近 0
        assert w[0] < 0.1
        assert w[-1] < 0.1
        # 中间应该最大（三角形窗）
        mid = len(w) // 2
        assert w[mid] > 0.8  # 三角形窗中间值约 1.0
    
    def test_kaiser_window(self):
        """测试凯撒窗"""
        # beta=0 应该接近矩形窗
        w0 = kaiser_window(10, beta=0)
        for x in w0:
            assert abs(x - 1.0) < 0.01
        
        # 更大的 beta 应该有更低的边缘值
        w5 = kaiser_window(10, beta=5)
        w10 = kaiser_window(10, beta=10)
        assert w10[0] < w5[0]
    
    def test_get_window(self):
        """测试 get_window 函数"""
        for wt in [WindowType.RECTANGULAR, WindowType.HANNING, WindowType.HAMMING,
                   WindowType.BLACKMAN, WindowType.BARTLETT]:
            w = get_window(wt, 10)
            assert len(w) == 10
        
        # Kaiser 需要额外参数
        w = get_window(WindowType.KAISER, 10, beta=5.0)
        assert len(w) == 10
    
    def test_apply_window(self):
        """测试应用窗函数"""
        signal = [1.0] * 10
        windowed = apply_window(signal, WindowType.HANNING)
        
        assert len(windowed) == 10
        # 窗函数应该缩放信号
        assert windowed[0] < 0.1  # Hanning 边缘接近 0


class TestSpectrumAnalysis:
    """频谱分析测试"""
    
    def test_compute_frequencies(self):
        """测试频率计算"""
        freqs = compute_frequencies(8, 1000.0)
        assert len(freqs) == 8
        assert freqs[0] == 0.0
        assert freqs[1] == 125.0  # 1000 / 8
        assert freqs[-1] == 875.0
    
    def test_compute_frequencies_rfft(self):
        """测试 RFFT 频率计算"""
        freqs = compute_frequencies_rfft(8, 1000.0)
        assert len(freqs) == 5  # 8 // 2 + 1
        assert freqs[0] == 0.0
        assert freqs[-1] == 500.0  # Nyquist
    
    def test_magnitude_spectrum(self):
        """测试幅度谱计算"""
        spectrum = [complex(3, 4), complex(0, 0), complex(1, 0), complex(0, 1)]
        mags = magnitude_spectrum(spectrum, normalize=True)
        
        assert abs(mags[0] - 2.5) < 1e-10  # 5 * 2/4
        assert abs(mags[1]) < 1e-10
    
    def test_phase_spectrum(self):
        """测试相位谱计算"""
        spectrum = [complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)]
        phases = phase_spectrum(spectrum)
        
        assert abs(phases[0]) < 1e-10  # 0 度
        assert abs(phases[1] - math.pi / 2) < 1e-10  # 90 度
        assert abs(phases[2] - math.pi) < 1e-10  # 180 度
        assert abs(phases[3] + math.pi / 2) < 1e-10  # -90 度
    
    def test_power_spectrum(self):
        """测试功率谱计算"""
        spectrum = [complex(3, 4), complex(0, 0), complex(1, 0)]
        power = power_spectrum(spectrum, normalize=True)
        
        # 功率 = 幅度^2
        expected_mag = 5.0 * 2 / 3
        assert abs(power[0] - expected_mag ** 2) < 1e-10
    
    def test_power_spectral_density(self):
        """测试功率谱密度计算"""
        spectrum = [complex(1, 0)] * 4
        sample_rate = 1000.0
        psd = power_spectral_density(spectrum, sample_rate)
        
        assert len(psd) == 4
        assert all(p > 0 for p in psd)
    
    def test_analyze_spectrum(self):
        """测试频谱分析"""
        sample_rate = 1000.0
        duration = 1.0
        freq = 50.0
        
        # 生成正弦波
        n = int(sample_rate * duration)
        signal = [math.sin(2 * math.pi * freq * i / sample_rate) for i in range(n)]
        
        result = analyze_spectrum(signal, sample_rate)
        
        assert isinstance(result, SpectrumResult)
        assert len(result.frequencies) > 0
        assert len(result.magnitudes) > 0
        assert result.peak_frequency is not None
        # 峰值频率应该接近 50 Hz
        assert abs(result.peak_frequency - freq) < 5.0


class TestPeakDetection:
    """峰值检测测试"""
    
    def test_find_peaks_single(self):
        """测试单峰检测"""
        spectrum = [0, 0, 0, 1, 0, 0, 0]
        frequencies = [i * 10 for i in range(7)]
        
        peaks = find_peaks(spectrum, frequencies, min_height=0.5)
        assert len(peaks) == 1
        assert peaks[0][0] == 30  # 频率
    
    def test_find_peaks_multiple(self):
        """测试多峰检测"""
        spectrum = [0, 1, 0, 0, 2, 0, 0, 1, 0]
        frequencies = [i * 10 for i in range(9)]
        
        peaks = find_peaks(spectrum, frequencies, min_height=0.5)
        assert len(peaks) == 3
        # 最高峰应该在 40 Hz
        peaks_sorted = sorted(peaks, key=lambda x: x[1], reverse=True)
        assert peaks_sorted[0][0] == 40
    
    def test_find_peaks_min_distance(self):
        """测试最小峰间距"""
        spectrum = [0, 1, 0.9, 1, 0, 0, 2, 0]
        frequencies = [i * 10 for i in range(8)]
        
        # 无间距限制
        peaks1 = find_peaks(spectrum, frequencies, min_height=0.5, min_distance=0)
        # 有间距限制
        peaks2 = find_peaks(spectrum, frequencies, min_height=0.5, min_distance=2)
        
        assert len(peaks1) >= len(peaks2)
    
    def test_find_harmonics(self):
        """测试谐波检测"""
        fundamental = 100.0
        frequencies = [i * 50 for i in range(20)]
        spectrum = [0] * 20
        # 设置基频和前 3 个谐波
        spectrum[2] = 1.0   # 100 Hz
        spectrum[4] = 0.5   # 200 Hz
        spectrum[6] = 0.3   # 300 Hz
        spectrum[8] = 0.2   # 400 Hz
        
        harmonics = find_harmonics(fundamental, 4, frequencies, spectrum)
        assert len(harmonics) == 4
        # 检查基频
        assert harmonics[0][0] == 1
        assert abs(harmonics[0][1] - fundamental) < 10


class TestConvolution:
    """卷积和相关性测试"""
    
    def test_convolve_basic(self):
        """测试基本卷积"""
        a = [1, 2, 3]
        b = [1, 1]
        result = convolve(a, b)
        
        assert len(result) == 4  # 3 + 2 - 1
        # [1, 2, 3] * [1, 1] = [1, 3, 5, 3]
        assert abs(result[0] - 1) < 1e-10
        assert abs(result[1] - 3) < 1e-10
        assert abs(result[2] - 5) < 1e-10
        assert abs(result[3] - 3) < 1e-10
    
    def test_convolve_delta(self):
        """测试与 delta 函数卷积"""
        signal = [1, 2, 3, 4, 5]
        delta = [1]
        result = convolve(signal, delta)
        
        assert len(result) == 5
        for i in range(5):
            assert abs(result[i] - signal[i]) < 1e-10
    
    def test_convolve_long(self):
        """测试较长信号卷积"""
        import random
        random.seed(42)
        a = [random.random() for _ in range(100)]
        b = [random.random() for _ in range(50)]
        
        result = convolve(a, b)
        assert len(result) == 149  # 100 + 50 - 1
    
    def test_correlate(self):
        """测试互相关"""
        a = [1, 2, 3, 4]
        b = [1, 2]
        result = correlate(a, b)
        
        assert len(result) == 5  # 4 + 2 - 1
    
    def test_autocorrelate(self):
        """测试自相关"""
        signal = [1, 2, 3, 2, 1]
        result = autocorrelate(signal)
        
        assert len(result) == 9  # 5 + 5 - 1
        # 自相关峰值应该在中心
        mid = len(result) // 2
        assert result[mid] == max(result)


class TestSignalGeneration:
    """信号生成测试"""
    
    def test_generate_sine(self):
        """测试正弦波生成"""
        freq = 10
        sample_rate = 100
        duration = 1.0
        
        signal = generate_sine(freq, sample_rate, duration)
        
        assert len(signal) == 100
        # 检查周期
        # 10 Hz 应该有 10 个完整周期
        peaks = 0
        for i in range(1, len(signal) - 1):
            if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
                peaks += 1
        assert peaks == 10
    
    def test_generate_cosine(self):
        """测试余弦波生成"""
        freq = 5
        sample_rate = 100
        duration = 1.0
        
        signal = generate_cosine(freq, sample_rate, duration)
        
        assert len(signal) == 100
        # 余弦波在 t=0 时应该为 1
        assert abs(signal[0] - 1.0) < 1e-10
    
    def test_generate_chirp(self):
        """测试扫频信号生成"""
        start_freq = 10
        end_freq = 100
        sample_rate = 1000
        duration = 1.0
        
        signal = generate_chirp(start_freq, end_freq, sample_rate, duration)
        
        assert len(signal) == 1000
        # 信号应该在有效范围内
        assert all(abs(s) <= 1.0 for s in signal)
    
    def test_sine_amplitude(self):
        """测试正弦波振幅"""
        amp = 2.5
        # 使用足够多的采样点确保能捕捉峰值
        signal = generate_sine(10, 1000, 1.0, amplitude=amp)
        
        # 正弦波的峰值应该接近振幅
        max_val = max(signal)
        min_val = min(signal)
        assert max_val <= amp + 0.01  # 允许小误差
        assert max_val >= amp - 0.01  # 峰值应该接近振幅
        assert min_val <= -amp + 0.01
        assert min_val >= -amp - 0.01
    
    def test_sine_phase(self):
        """测试正弦波相位"""
        # 0 相位正弦
        s1 = generate_sine(1, 100, 1.0, phase=0)
        # 90 度相位 = 余弦
        s2 = generate_sine(1, 100, 1.0, phase=math.pi/2)
        # 180 度相位 = 反相
        s3 = generate_sine(1, 100, 1.0, phase=math.pi)
        
        assert s1[0] == pytest.approx(0, abs=1e-10)
        assert s2[0] == pytest.approx(1, abs=1e-10)
        assert s3[0] == pytest.approx(0, abs=1e-10)


class TestUtilityFunctions:
    """工具函数测试"""
    
    def test_zero_pad_extend(self):
        """测试零填充扩展"""
        signal = [1, 2, 3]
        result = zero_pad(signal, 6)
        
        assert len(result) == 6
        assert result[:3] == [1, 2, 3]
        assert result[3:] == [0, 0, 0]
    
    def test_zero_pad_no_change(self):
        """测试零填充不改变已够长的信号"""
        signal = [1, 2, 3, 4, 5]
        result = zero_pad(signal, 3)
        
        assert result == signal
    
    def test_pad_to_power_of_two(self):
        """测试填充到 2 的幂"""
        result = pad_to_power_of_two([1, 2, 3])
        assert len(result) == 4
        assert result[:3] == [1, 2, 3]
        
        result = pad_to_power_of_two([1, 2, 3, 4, 5])
        assert len(result) == 8
    
    def test_dc_offset(self):
        """测试 DC 偏移计算"""
        signal = [1, 2, 3, 4, 5]
        offset = dc_offset(signal)
        
        assert offset == pytest.approx(3.0, rel=1e-10)
        
        # DC 偏移信号
        signal2 = [5, 5, 5, 5, 5]
        assert dc_offset(signal2) == pytest.approx(5.0, rel=1e-10)
    
    def test_remove_dc(self):
        """测试移除 DC"""
        signal = [5, 6, 7, 6, 5]
        result = remove_dc(signal)
        
        avg = sum(result) / len(result)
        assert abs(avg) < 1e-10
    
    def test_resample(self):
        """测试重采样"""
        signal = [0, 1, 0, -1, 0]  # 一个正弦周期
        # 上采样 2x
        result = resample(signal, 100, 200)
        
        assert len(result) == 10
    
    def test_resample_downsample(self):
        """测试下采样"""
        signal = list(range(100))
        result = resample(signal, 100, 50)
        
        assert len(result) == 50
    
    def test_normalize_signal(self):
        """测试归一化"""
        signal = [1, 2, 3, -2, -1]
        result = normalize_signal(signal)
        
        max_val = max(abs(s) for s in result)
        assert abs(max_val - 1.0) < 1e-10
    
    def test_normalize_custom_max(self):
        """测试自定义最大值归一化"""
        signal = [1, 2, 3, -2, -1]
        result = normalize_signal(signal, target_max=2.0)
        
        max_val = max(abs(s) for s in result)
        assert abs(max_val - 2.0) < 1e-10


class TestIntegration:
    """集成测试"""
    
    def test_fft_roundtrip(self):
        """测试 FFT -> IFFT 往返"""
        import random
        random.seed(123)
        
        signal = [random.random() for _ in range(64)]
        spectrum = fft(signal)
        reconstructed = ifft(spectrum)
        
        for i in range(64):
            assert abs(reconstructed[i].real - signal[i]) < 1e-10
    
    def test_window_fft(self):
        """测试加窗 FFT"""
        sample_rate = 1000
        freq = 50
        
        signal = [math.sin(2 * math.pi * freq * i / sample_rate) for i in range(256)]
        
        # 加窗
        windowed = apply_window(signal, WindowType.HANNING)
        
        # FFT
        spectrum = rfft(windowed)
        mags = magnitude_spectrum(spectrum)
        
        # 找峰值
        peak_idx = mags.index(max(mags))
        peak_freq = peak_idx * sample_rate / len(signal)
        
        # 峰值频率应该接近 50 Hz
        assert abs(peak_freq - freq) < 10
    
    def test_convolution_theorem(self):
        """测试卷积定理 (FFT 方法与传统方法)"""
        a = [1, 2, 3, 4, 5]
        b = [1, 1, 1]
        
        # FFT 卷积
        result_fft = convolve(a, b)
        
        # 直接卷积
        result_direct = []
        n, m = len(a), len(b)
        for k in range(n + m - 1):
            total = 0
            for i in range(n):
                j = k - i
                if 0 <= j < m:
                    total += a[i] * b[j]
            result_direct.append(total)
        
        for i in range(len(result_fft)):
            assert abs(result_fft[i] - result_direct[i]) < 1e-10
    
    def test_multitone_analysis(self):
        """测试多音信号分析"""
        sample_rate = 1000
        duration = 1.0
        n = int(sample_rate * duration)
        
        # 三个频率
        freqs = [50, 120, 250]
        
        # 合成信号
        signal = []
        for i in range(n):
            val = sum(math.sin(2 * math.pi * f * i / sample_rate) for f in freqs)
            signal.append(val)
        
        # 分析
        result = analyze_spectrum(signal, sample_rate)
        peaks = find_peaks(result.magnitudes, result.frequencies, min_height=0.2, min_distance=5)
        
        # 检测到的峰值应该包含三个频率
        detected_freqs = sorted([p[0] for p in peaks])
        
        # 允许一定误差
        for f in freqs:
            found = any(abs(df - f) < 10 for df in detected_freqs)
            assert found, f"频率 {f} 未检测到"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])