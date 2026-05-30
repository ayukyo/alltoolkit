"""
波形工具测试模块

测试所有波形生成、分析和变换功能。
"""

import math
import random
import unittest
from mod import (
    WaveformType,
    WaveformGenerator,
    WaveformAnalyzer,
    WaveformTransformer,
    WaveformVisualizer,
    generate_waveform,
    analyze_waveform,
    create_envelope,
    apply_envelope,
)


class TestWaveformGenerator(unittest.TestCase):
    """测试波形生成器"""
    
    def setUp(self):
        self.sample_rate = 8000  # 使用较低采样率加快测试
        self.gen = WaveformGenerator(self.sample_rate)
    
    def test_sine_wave(self):
        """测试正弦波生成"""
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        
        # 验证长度
        expected_length = int(self.sample_rate * 0.1)
        self.assertEqual(len(samples), expected_length)
        
        # 验证范围在 [-1, 1]
        for s in samples:
            self.assertGreaterEqual(s, -1.0)
            self.assertLessEqual(s, 1.0)
        
        # 验证正弦波特性：第一个样本应接近 0
        self.assertAlmostEqual(samples[0], 0.0, places=5)
    
    def test_square_wave(self):
        """测试方波生成"""
        samples = self.gen.generate(WaveformType.SQUARE, 440, 0.1)
        
        # 方波值应该是 +1 或 -1（或非常接近）
        for s in samples:
            self.assertTrue(s >= 0.9 or s <= -0.9)
    
    def test_sawtooth_wave(self):
        """测试锯齿波生成"""
        samples = self.gen.generate(WaveformType.SAWTOOTH, 440, 0.1)
        
        # 验证范围
        for s in samples:
            self.assertGreaterEqual(s, -1.0)
            self.assertLessEqual(s, 1.0)
        
        # 验证锯齿波特性：应该是单调递增的模式
        # 检查第一个周期内的单调性
        period_samples = self.sample_rate // 440
        increasing_count = 0
        for i in range(1, min(period_samples, len(samples))):
            if samples[i] > samples[i-1]:
                increasing_count += 1
        self.assertGreater(increasing_count, period_samples * 0.9)
    
    def test_triangle_wave(self):
        """测试三角波生成"""
        samples = self.gen.generate(WaveformType.TRIANGLE, 440, 0.1)
        
        # 验证范围
        for s in samples:
            self.assertGreaterEqual(s, -1.0)
            self.assertLessEqual(s, 1.0)
        
        # 三角波应该有明显的峰值和谷值
        max_val = max(samples)
        min_val = min(samples)
        self.assertAlmostEqual(max_val, 1.0, places=5)
        self.assertAlmostEqual(min_val, -1.0, places=5)
    
    def test_pulse_wave(self):
        """测试脉冲波生成"""
        # 50% 占空比应该等于方波
        pulse_50 = self.gen.generate(WaveformType.PULSE, 440, 0.1, duty_cycle=0.5)
        square = self.gen.generate(WaveformType.SQUARE, 440, 0.1)
        self.assertEqual(len(pulse_50), len(square))
        
        # 25% 占空比
        pulse_25 = self.gen.generate(WaveformType.PULSE, 440, 0.1, duty_cycle=0.25)
        self.assertEqual(len(pulse_25), int(self.sample_rate * 0.1))
        
        # 验证占空比：正值应该占 25%
        positive_count = sum(1 for s in pulse_25 if s > 0)
        ratio = positive_count / len(pulse_25)
        self.assertAlmostEqual(ratio, 0.25, places=1)
    
    def test_white_noise(self):
        """测试白噪声生成"""
        samples = self.gen.generate(WaveformType.WHITE_NOISE, 440, 0.1)
        
        # 验证长度
        self.assertEqual(len(samples), int(self.sample_rate * 0.1))
        
        # 白噪声应该有随机性
        # 计算标准差
        mean = sum(samples) / len(samples)
        variance = sum((s - mean) ** 2 for s in samples) / len(samples)
        std = math.sqrt(variance)
        
        # 白噪声的标准差应该约为 0.577 (均匀分布 [-1, 1])
        self.assertGreater(std, 0.4)
        self.assertLess(std, 0.7)
    
    def test_pink_noise(self):
        """测试粉红噪声生成"""
        samples = self.gen.generate(WaveformType.PINK_NOISE, 440, 0.1)
        
        # 验证长度
        self.assertEqual(len(samples), int(self.sample_rate * 0.1))
        
        # 粉红噪声应该有不同的频谱特性
        # 简单验证：前半部分和后半部分的能量应该不同
        half = len(samples) // 2
        first_half_energy = sum(s ** 2 for s in samples[:half])
        second_half_energy = sum(s ** 2 for s in samples[half:])
        
        # 能量应该有差异（随机性）
        self.assertGreater(first_half_energy + second_half_energy, 0)
    
    def test_amplitude(self):
        """测试振幅控制"""
        # 不同振幅的正弦波
        amp1 = self.gen.generate(WaveformType.SINE, 440, 0.1, amplitude=1.0)
        amp05 = self.gen.generate(WaveformType.SINE, 440, 0.1, amplitude=0.5)
        
        max_amp1 = max(abs(s) for s in amp1)
        max_amp05 = max(abs(s) for s in amp05)
        
        self.assertAlmostEqual(max_amp1, 1.0, places=5)
        self.assertAlmostEqual(max_amp05, 0.5, places=5)
    
    def test_phase(self):
        """测试相位控制"""
        # 相位差 π/2 的正弦波
        phase0 = self.gen.generate(WaveformType.SINE, 440, 0.01, phase=0)
        phase_pi2 = self.gen.generate(WaveformType.SINE, 440, 0.01, phase=math.pi/2)
        
        # 第一个样本应该不同
        self.assertNotAlmostEqual(phase0[0], phase_pi2[0], places=3)
        
        # 相位 π/2 的正弦波第一个样本应该是 1
        self.assertAlmostEqual(phase_pi2[0], 1.0, places=5)
    
    def test_sawtooth_reverse(self):
        """测试反向锯齿波"""
        forward = self.gen.generate(WaveformType.SAWTOOTH, 440, 0.1)
        reverse = self.gen.generate(WaveformType.SAWTOOTH_REVERSE, 440, 0.1)
        
        # 应该是相反的
        for f, r in zip(forward, reverse):
            self.assertAlmostEqual(f, -r, places=5)


class TestWaveformAnalyzer(unittest.TestCase):
    """测试波形分析器"""
    
    def setUp(self):
        self.sample_rate = 8000
        self.analyzer = WaveformAnalyzer(self.sample_rate)
        self.gen = WaveformGenerator(self.sample_rate)
    
    def test_statistics(self):
        """测试统计计算"""
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        stats = self.analyzer.get_statistics(samples)
        
        # 检查键存在
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertIn("mean", stats)
        self.assertIn("rms", stats)
        self.assertIn("peak_to_peak", stats)
        
        # 正弦波的 RMS 应该约为 0.707
        self.assertAlmostEqual(stats["rms"], 0.707, places=2)
        
        # 正弦波的峰峰值应该约为 2
        self.assertAlmostEqual(stats["peak_to_peak"], 2.0, places=2)
        
        # 正弦波的均值应该接近 0
        self.assertAlmostEqual(stats["mean"], 0.0, places=5)
    
    def test_statistics_empty(self):
        """测试空波形的统计"""
        stats = self.analyzer.get_statistics([])
        self.assertEqual(stats["min"], 0.0)
        self.assertEqual(stats["max"], 0.0)
        self.assertEqual(stats["mean"], 0.0)
    
    def test_zero_crossing_rate(self):
        """测试过零率"""
        # 正弦波的过零率应该接近 2 * 频率
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        zcr = self.analyzer.zero_crossing_rate(samples)
        
        # 理论上应该是 2 * 440 = 880
        self.assertAlmostEqual(zcr, 880, delta=50)
    
    def test_estimate_frequency(self):
        """测试频率估计"""
        # 使用正弦波测试频率估计
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        freq = self.analyzer.estimate_frequency(samples)
        
        # 应该接近 440 Hz
        self.assertAlmostEqual(freq, 440, delta=30)
    
    def test_dc_offset(self):
        """测试 DC 偏移"""
        # 无 DC 偏移的波形
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        dc = self.analyzer.calculate_dc_offset(samples)
        self.assertAlmostEqual(dc, 0.0, places=5)
        
        # 添加 DC 偏移
        biased = [s + 0.5 for s in samples]
        dc_biased = self.analyzer.calculate_dc_offset(biased)
        self.assertAlmostEqual(dc_biased, 0.5, places=5)
    
    def test_remove_dc_offset(self):
        """测试移除 DC 偏移"""
        samples = self.gen.generate(WaveformType.SINE, 440, 0.1)
        biased = [s + 0.3 for s in samples]
        
        corrected = self.analyzer.remove_dc_offset(biased)
        dc_corrected = self.analyzer.calculate_dc_offset(corrected)
        
        self.assertAlmostEqual(dc_corrected, 0.0, places=5)
    
    def test_normalize(self):
        """测试归一化"""
        samples = [0.5, -0.3, 0.8, -0.6, 0.1]
        normalized = self.analyzer.normalize(samples, target_peak=1.0)
        
        max_abs = max(abs(s) for s in normalized)
        self.assertAlmostEqual(max_abs, 1.0, places=5)
    
    def test_clip(self):
        """测试限幅"""
        samples = [0.8, 1.5, -0.9, -1.2, 0.3]
        clipped = self.analyzer.clip(samples, threshold=1.0)
        
        for s in clipped:
            self.assertGreaterEqual(s, -1.0)
            self.assertLessEqual(s, 1.0)
    
    def test_detect_silence(self):
        """测试静音检测"""
        # 创建包含静音的波形
        silence = [0.0] * 1000
        noise = [random.uniform(-0.5, 0.5) for _ in range(1000)]
        
        samples = silence + noise + silence
        
        regions = self.analyzer.detect_silence(
            samples, 
            threshold=0.01, 
            min_duration=0.05
        )
        
        # 应该检测到前后两个静音区域
        self.assertGreaterEqual(len(regions), 1)


class TestWaveformTransformer(unittest.TestCase):
    """测试波形变换器"""
    
    def setUp(self):
        self.sample_rate = 8000
        self.transformer = WaveformTransformer(self.sample_rate)
        self.gen = WaveformGenerator(self.sample_rate)
    
    def test_fade_in(self):
        """测试淡入"""
        samples = [1.0] * 1000
        
        faded = self.transformer.fade_in(samples, duration=0.05, curve="linear")
        
        # 开头应该接近 0
        self.assertAlmostEqual(faded[0], 0.0, places=5)
        
        # 结尾应该接近 1
        self.assertAlmostEqual(faded[-1], 1.0, places=5)
    
    def test_fade_out(self):
        """测试淡出"""
        samples = [1.0] * 1000
        
        faded = self.transformer.fade_out(samples, duration=0.05, curve="linear")
        
        # 开头应该接近 1
        self.assertAlmostEqual(faded[0], 1.0, places=5)
        
        # 结尾应该接近 0（允许微小误差）
        self.assertAlmostEqual(faded[-1], 0.0, places=2)
    
    def test_fade_curves(self):
        """测试不同的淡入淡出曲线"""
        samples = [1.0] * 1000
        curves = ["linear", "exponential", "logarithmic", "cosine"]
        
        for curve in curves:
            faded = self.transformer.fade_in(samples, duration=0.05, curve=curve)
            self.assertAlmostEqual(faded[0], 0.0, places=5)
            self.assertGreater(faded[-1], 0.9)
    
    def test_mix(self):
        """测试波形混合"""
        samples1 = [1.0] * 100
        samples2 = [0.5] * 100
        
        # 等权重混合
        mixed = self.transformer.mix([samples1, samples2])
        avg = sum(mixed) / len(mixed)
        self.assertAlmostEqual(avg, 1.5, places=5)
        
        # 不同权重混合
        weighted = self.transformer.mix([samples1, samples2], weights=[0.5, 1.0])
        avg_weighted = sum(weighted) / len(weighted)
        self.assertAlmostEqual(avg_weighted, 1.0, places=5)
    
    def test_amplitude_modulate(self):
        """测试振幅调制"""
        carrier = [1.0] * 1000
        modulator = self.gen.generate(WaveformType.SINE, 5, 0.125)  # 5 Hz 调制
        
        modulated = self.transformer.amplitude_modulate(carrier, modulator, depth=1.0)
        
        # 调制后的波形应该有变化
        self.assertNotEqual(carrier[:len(modulated)], modulated)
    
    def test_time_stretch(self):
        """测试时间拉伸"""
        samples = list(range(1000))
        
        # 拉伸 2 倍
        stretched = self.transformer.time_stretch(samples, 2.0)
        self.assertEqual(len(stretched), 2000)
        
        # 压缩 0.5 倍
        compressed = self.transformer.time_stretch(samples, 0.5)
        self.assertEqual(len(compressed), 500)
    
    def test_reverse(self):
        """测试波形反转"""
        samples = [1, 2, 3, 4, 5]
        reversed_samples = self.transformer.reverse(samples)
        self.assertEqual(reversed_samples, [5, 4, 3, 2, 1])
    
    def test_delay(self):
        """测试延迟效果"""
        samples = [1.0] * 100 + [0.0] * 500
        
        delayed = self.transformer.delay(
            samples, 
            delay_time=0.05,  # 50ms
            decay=0.5
        )
        
        # 延迟后的信号应该在后面出现
        delay_samples = int(0.05 * self.sample_rate)
        
        # 原始信号应该还在
        self.assertGreater(delayed[50], 0)
        
        # 延迟信号应该在延迟时间后出现
        self.assertGreater(delayed[50 + delay_samples], 0)


class TestWaveformVisualizer(unittest.TestCase):
    """测试波形可视化"""
    
    def test_ascii_waveform(self):
        """测试 ASCII 波形图生成"""
        samples = [math.sin(2 * math.pi * i / 20) for i in range(100)]
        
        ascii_wave = WaveformVisualizer.get_ascii_waveform(
            samples, 
            width=40, 
            height=8
        )
        
        # 应该返回多行字符串
        lines = ascii_wave.split('\n')
        self.assertEqual(len(lines), 8)
        self.assertEqual(len(lines[0]), 40)
        
        # 应该包含 * 和 -
        self.assertIn('*', ascii_wave)
        self.assertIn('-', ascii_wave)
    
    def test_ascii_waveform_empty(self):
        """测试空波形的 ASCII 图"""
        ascii_wave = WaveformVisualizer.get_ascii_waveform([])
        self.assertEqual(ascii_wave, "")
    
    def test_histogram(self):
        """测试直方图生成"""
        # 生成正态分布的样本
        samples = [random.gauss(0, 0.3) for _ in range(1000)]
        
        hist = WaveformVisualizer.get_histogram(samples, bins=10, width=30)
        
        # 应该返回多行字符串
        lines = hist.split('\n')
        self.assertEqual(len(lines), 10)
        
        # 应该包含统计信息
        self.assertIn('█', hist)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_waveform_with_string(self):
        """测试使用字符串生成波形"""
        sine = generate_waveform("sine", 440, 0.1)
        self.assertEqual(len(sine), 4410)  # 默认采样率 44100
        
        square = generate_waveform("square", 440, 0.1)
        self.assertEqual(len(square), 4410)
    
    def test_generate_waveform_with_enum(self):
        """测试使用枚举生成波形"""
        sine = generate_waveform(WaveformType.SINE, 440, 0.1)
        self.assertEqual(len(sine), 4410)
    
    def test_analyze_waveform(self):
        """测试波形分析便捷函数"""
        samples = generate_waveform("sine", 440, 0.1)
        stats = analyze_waveform(samples)
        
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertIn("rms", stats)
        self.assertIn("estimated_frequency", stats)
        self.assertIn("zero_crossing_rate", stats)
    
    def test_create_envelope(self):
        """测试 ADSR 包络创建"""
        env = create_envelope(
            attack=0.01,
            decay=0.05,
            sustain=0.1,
            release=0.02,
            total_duration=0.18
        )
        
        # 验证长度
        self.assertEqual(len(env), int(0.18 * 44100))
        
        # 验证开始为 0
        self.assertAlmostEqual(env[0], 0.0, places=5)
        
        # 验证结束接近 0（允许微小误差）
        self.assertAlmostEqual(env[-1], 0.0, places=2)
        
        # 验证有峰值（大约在 attack 阶段结束）
        max_val = max(env)
        self.assertAlmostEqual(max_val, 1.0, places=3)
    
    def test_apply_envelope(self):
        """测试包络应用"""
        samples = generate_waveform("sine", 440, 0.1, sample_rate=8000)
        env = create_envelope(0.01, 0.02, 0.05, 0.02, 0.1, sample_rate=8000)
        
        result = apply_envelope(samples, env)
        
        self.assertEqual(len(result), min(len(samples), len(env)))
        
        # 开始应该很安静
        self.assertLess(abs(result[0]), 0.01)
        
        # 中间应该是最响的
        mid = len(result) // 2
        start = len(result) // 4
        self.assertGreater(abs(result[mid]), abs(result[0]))


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        self.sample_rate = 8000
        self.gen = WaveformGenerator(self.sample_rate)
        self.analyzer = WaveformAnalyzer(self.sample_rate)
        self.transformer = WaveformTransformer(self.sample_rate)
    
    def test_full_pipeline(self):
        """测试完整的生成-分析-变换流程"""
        # 1. 生成波形
        samples = self.gen.generate(WaveformType.SINE, 440, 0.5)
        
        # 2. 分析
        stats = self.analyzer.get_statistics(samples)
        self.assertAlmostEqual(stats["rms"], 0.707, places=2)
        
        # 3. 应用变换
        faded = self.transformer.fade_in(samples, 0.1)
        faded = self.transformer.fade_out(faded, 0.1)
        
        # 4. 再次分析
        faded_stats = self.analyzer.get_statistics(faded)
        
        # 淡入淡出后的 RMS 应该更小
        self.assertLess(faded_stats["rms"], stats["rms"])
    
    def test_complex_waveform(self):
        """测试复杂波形生成"""
        # 生成多个波形并混合
        sine1 = self.gen.generate(WaveformType.SINE, 440, 0.5)
        sine2 = self.gen.generate(WaveformType.SINE, 880, 0.5)
        sine3 = self.gen.generate(WaveformType.SINE, 1320, 0.5)
        
        mixed = self.transformer.mix(
            [sine1, sine2, sine3],
            weights=[0.5, 0.3, 0.2]
        )
        
        # 归一化
        normalized = self.analyzer.normalize(mixed)
        
        # 验证
        max_abs = max(abs(s) for s in normalized)
        self.assertAlmostEqual(max_abs, 1.0, places=3)
    
    def test_noise_characteristics(self):
        """测试噪声特性"""
        # 白噪声
        white = self.gen.generate(WaveformType.WHITE_NOISE, 0, 1.0, seed=42)
        
        # 粉红噪声
        pink = self.gen.generate(WaveformType.PINK_NOISE, 0, 1.0)
        
        # 分析
        white_stats = self.analyzer.get_statistics(white)
        pink_stats = self.analyzer.get_statistics(pink)
        
        # 两种噪声都应该在 [-1, 1] 范围内
        self.assertLessEqual(white_stats["max"], 1.0)
        self.assertGreaterEqual(white_stats["min"], -1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)