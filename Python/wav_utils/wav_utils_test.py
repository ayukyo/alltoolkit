"""
WAV 工具集测试
==============

测试 wav_utils 模块的所有功能。
"""

import os
import sys
import tempfile
import unittest

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WavReader, WavWriter, WavProcessor,
    WavInfo, WavFormat,
    read_wav, write_wav, get_wav_info, create_sine_wav
)


class TestWavWriter(unittest.TestCase):
    """测试 WAV 写入器"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_sine_wave(self):
        """测试创建正弦波"""
        filepath = os.path.join(self.temp_dir, 'sine.wav')
        
        writer = WavWriter(filepath, sample_rate=44100, channels=1, bits_per_sample=16)
        writer.add_sine_wave(frequency=440, duration_ms=100, amplitude=0.5)
        info = writer.write()
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        
        # 验证文件大小合理
        file_size = os.path.getsize(filepath)
        self.assertGreater(file_size, 44)  # 至少包含头部
        
        # 验证信息正确
        self.assertEqual(info.sample_rate, 44100)
        self.assertEqual(info.channels, 1)
        self.assertEqual(info.bits_per_sample, 16)
        self.assertAlmostEqual(info.duration, 0.1, places=2)
    
    def test_create_stereo(self):
        """测试创建立体声文件"""
        filepath = os.path.join(self.temp_dir, 'stereo.wav')
        
        left_channel = [1000] * 1000
        right_channel = [-1000] * 1000
        
        writer = WavWriter(filepath, sample_rate=44100, channels=2, bits_per_sample=16)
        writer.add_samples([left_channel, right_channel])
        info = writer.write()
        
        self.assertEqual(info.channels, 2)
        self.assertAlmostEqual(info.duration, 1000 / 44100, places=4)
    
    def test_add_silence(self):
        """测试添加静音"""
        filepath = os.path.join(self.temp_dir, 'silence.wav')
        
        writer = WavWriter(filepath, sample_rate=44100, channels=1)
        writer.add_silence(500)  # 500ms
        info = writer.write()
        
        self.assertAlmostEqual(info.duration, 0.5, places=2)
    
    def test_different_bit_depths(self):
        """测试不同位深"""
        for bits in [8, 16, 24, 32]:
            filepath = os.path.join(self.temp_dir, f'test_{bits}bit.wav')
            
            writer = WavWriter(filepath, sample_rate=44100, bits_per_sample=bits)
            writer.add_sine_wave(440, 100, 0.5)
            info = writer.write()
            
            self.assertEqual(info.bits_per_sample, bits)


class TestWavReader(unittest.TestCase):
    """测试 WAV 读取器"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_read_info(self):
        """测试读取文件信息"""
        filepath = os.path.join(self.temp_dir, 'test.wav')
        create_sine_wav(filepath, frequency=440, duration_ms=500)
        
        info = get_wav_info(filepath)
        
        self.assertEqual(info.channels, 1)
        self.assertEqual(info.sample_rate, 44100)
        self.assertEqual(info.bits_per_sample, 16)
        self.assertEqual(info.format_tag, WavFormat.PCM.value)
    
    def test_read_samples(self):
        """测试读取样本数据"""
        filepath = os.path.join(self.temp_dir, 'test.wav')
        create_sine_wav(filepath, frequency=440, duration_ms=100)
        
        reader = WavReader(filepath)
        samples = reader.read_samples_mono()
        
        # 验证样本数量
        expected_samples = int(44100 * 0.1)  # 100ms
        self.assertEqual(len(samples), expected_samples)
        
        # 验证样本值范围
        for s in samples:
            self.assertGreaterEqual(s, -32768)
            self.assertLessEqual(s, 32767)
    
    def test_roundtrip(self):
        """测试读写往返一致性"""
        filepath = os.path.join(self.temp_dir, 'roundtrip.wav')
        
        # 创建原始数据
        original_samples = [1000, 2000, 3000, 4000, 5000]
        
        # 写入
        write_wav(filepath, original_samples, sample_rate=44100)
        
        # 读取
        info, read_samples = read_wav(filepath)
        
        # 验证
        self.assertEqual(len(read_samples), 1)
        self.assertEqual(read_samples[0], original_samples)


class TestWavProcessor(unittest.TestCase):
    """测试 WAV 处理器"""
    
    def test_normalize(self):
        """测试归一化"""
        samples = [1000, 2000, 3000, 4000, 5000]
        normalized = WavProcessor.normalize(samples, target_peak=0.8)
        
        # 验证最大值接近目标峰值
        max_val = max(abs(s) for s in normalized)
        expected_max = int(32767 * 0.8)
        self.assertLess(abs(max_val - expected_max), 10)
    
    def test_amplify(self):
        """测试增益"""
        samples = [1000, 2000, 3000]
        
        # +6dB ≈ 2x
        amplified = WavProcessor.amplify(samples, gain_db=6)
        
        self.assertAlmostEqual(amplified[0], 1995, delta=50)  # 约 2x
        
        # -6dB ≈ 0.5x
        attenuated = WavProcessor.amplify(samples, gain_db=-6)
        
        self.assertAlmostEqual(attenuated[0], 501, delta=50)  # 约 0.5x
    
    def test_find_silence(self):
        """测试静音检测"""
        # 创建包含静音的音频
        samples = [0, 0, 0, 0, 0, 1000, 2000, 3000, 0, 0, 0, 0, 0, 0]
        
        # 使用低采样率以使 min_samples 小于实际静音长度
        silence_regions = WavProcessor.find_silence(
            samples, threshold=100, min_duration_ms=10, sample_rate=100
        )
        
        # 应该检测到开头和结尾的静音
        self.assertGreater(len(silence_regions), 0)
    
    def test_trim_silence(self):
        """测试去除静音"""
        samples = [0, 0, 0, 1000, 2000, 3000, 0, 0, 0]
        
        trimmed = WavProcessor.trim_silence(samples, threshold=500)
        
        # 验证首尾的静音被去除
        self.assertEqual(trimmed[0], 1000)
        self.assertEqual(trimmed[-1], 3000)
    
    def test_mix(self):
        """测试混合"""
        source1 = [1000, 2000, 3000]
        source2 = [1000, 2000, 3000]
        
        mixed = WavProcessor.mix([source1, source2])
        
        # 等权重混合应该是平均值
        self.assertEqual(mixed[0], 1000)  # (1000 + 1000) / 2 * 2 = 1000
        self.assertEqual(mixed[1], 2000)
        self.assertEqual(mixed[2], 3000)
    
    def test_resample(self):
        """测试重采样"""
        samples = [0, 1000, 2000, 3000, 4000, 5000]
        
        # 下采样
        downsampled = WavProcessor.resample(samples, from_rate=44100, to_rate=22050)
        self.assertEqual(len(downsampled), 3)  # 长度减半
        
        # 上采样
        upsampled = WavProcessor.resample(samples, from_rate=44100, to_rate=88200)
        self.assertEqual(len(upsampled), 12)  # 长度翻倍
    
    def test_reverse(self):
        """测试反转"""
        samples = [1, 2, 3, 4, 5]
        reversed_samples = WavProcessor.reverse(samples)
        
        self.assertEqual(reversed_samples, [5, 4, 3, 2, 1])
    
    def test_fade_in(self):
        """测试淡入"""
        samples = [1000] * 100
        
        faded = WavProcessor.fade_in(samples, duration_ms=10, sample_rate=10000)
        
        # 开头的样本应该更小
        self.assertLess(abs(faded[0]), abs(faded[50]))
        
        # 结尾的样本应该接近原值
        self.assertAlmostEqual(faded[-1], samples[-1], delta=10)
    
    def test_fade_out(self):
        """测试淡出"""
        samples = [1000] * 100
        
        faded = WavProcessor.fade_out(samples, duration_ms=10, sample_rate=10000)
        
        # 开头的样本应该接近原值
        self.assertAlmostEqual(faded[0], samples[0], delta=10)
        
        # 结尾的样本应该更小
        self.assertLess(abs(faded[-1]), abs(faded[50]))


class TestWavInfo(unittest.TestCase):
    """测试 WAV 信息类"""
    
    def test_duration_calculation(self):
        """测试时长计算"""
        info = WavInfo(
            channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            format_tag=1,
            num_samples=44100,
            data_size=176400
        )
        
        self.assertEqual(info.duration, 1.0)  # 1 秒
    
    def test_byte_rate(self):
        """测试字节率计算"""
        info = WavInfo(
            channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            format_tag=1,
            num_samples=44100,
            data_size=176400
        )
        
        self.assertEqual(info.byte_rate, 176400)
    
    def test_block_align(self):
        """测试块对齐计算"""
        info = WavInfo(
            channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            format_tag=1,
            num_samples=44100,
            data_size=176400
        )
        
        self.assertEqual(info.block_align, 4)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_read_write_wav(self):
        """测试读写便捷函数"""
        filepath = os.path.join(self.temp_dir, 'convenience.wav')
        
        samples = [i * 100 for i in range(100)]
        
        # 写入
        info = write_wav(filepath, samples, sample_rate=44100)
        self.assertEqual(info.sample_rate, 44100)
        
        # 读取
        read_info, read_samples = read_wav(filepath)
        
        self.assertEqual(read_info.sample_rate, 44100)
        self.assertEqual(len(read_samples), 1)
        self.assertEqual(len(read_samples[0]), 100)
    
    def test_create_sine_wav(self):
        """测试创建正弦波便捷函数"""
        filepath = os.path.join(self.temp_dir, 'sine.wav')
        
        info = create_sine_wav(filepath, frequency=880, duration_ms=200, amplitude=0.7)
        
        self.assertEqual(info.sample_rate, 44100)
        self.assertAlmostEqual(info.duration, 0.2, places=2)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_empty_samples(self):
        """测试空样本"""
        filepath = os.path.join(self.temp_dir, 'empty.wav')
        
        writer = WavWriter(filepath)
        info = writer.write()
        
        self.assertEqual(info.num_samples, 0)
    
    def test_large_amplitude(self):
        """测试大振幅"""
        filepath = os.path.join(self.temp_dir, 'large_amp.wav')
        
        # 大振幅应该被裁剪
        writer = WavWriter(filepath)
        writer.add_sine_wave(440, 100, amplitude=2.0)  # 超过 1.0
        info = writer.write()
        
        self.assertTrue(os.path.exists(filepath))
    
    def test_high_frequency(self):
        """测试高频"""
        filepath = os.path.join(self.temp_dir, 'high_freq.wav')
        
        create_sine_wav(filepath, frequency=20000, duration_ms=100)
        info = get_wav_info(filepath)
        
        self.assertEqual(info.sample_rate, 44100)


if __name__ == '__main__':
    unittest.main(verbosity=2)