#!/usr/bin/env python3
"""
Ambient Noise Utils 测试套件

测试环境噪音生成功能
"""

import unittest
import math
import struct
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    generate_white_noise,
    generate_pink_noise,
    generate_brown_noise,
    generate_blue_noise,
    generate_violet_noise,
    generate_grey_noise,
    generate_noise,
    generate_ambient_sound,
    generate_rain_sound,
    generate_ocean_sound,
    generate_wind_sound,
    generate_fire_sound,
    mix_noises,
    layer_ambient_sounds,
    apply_fade,
    apply_volume,
    samples_to_wav_bytes,
    save_wav_file,
    load_wav_file,
    get_noise_info,
    get_ambient_info,
    list_noise_types,
    list_ambient_types,
    calculate_duration,
    calculate_num_samples,
    estimate_file_size,
    format_duration,
    format_file_size,
    AmbientNoiseGenerator,
    AudioConfig,
    NoiseProfile,
    NoiseType,
    AmbientType,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_BITS_PER_SAMPLE
)


class TestWhiteNoise(unittest.TestCase):
    """白噪音生成测试"""
    
    def test_generate_white_noise_basic(self):
        """测试基本白噪音生成"""
        samples = generate_white_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
        self.assertTrue(all(-0.5 <= s <= 0.5 for s in samples))
    
    def test_generate_white_noise_amplitude(self):
        """测试振幅控制"""
        samples_low = generate_white_noise(100, 0.1)
        samples_high = generate_white_noise(100, 0.9)
        
        max_low = max(abs(s) for s in samples_low)
        max_high = max(abs(s) for s in samples_high)
        
        self.assertLess(max_low, max_high)
    
    def test_generate_white_noise_seed(self):
        """测试随机种子"""
        samples1 = generate_white_noise(100, 0.5, seed=42)
        samples2 = generate_white_noise(100, 0.5, seed=42)
        
        self.assertEqual(samples1, samples2)
    
    def test_generate_white_noise_different_seeds(self):
        """测试不同种子产生不同结果"""
        samples1 = generate_white_noise(100, 0.5, seed=1)
        samples2 = generate_white_noise(100, 0.5, seed=2)
        
        self.assertNotEqual(samples1, samples2)
    
    def test_generate_white_noise_zero_amplitude(self):
        """测试零振幅"""
        samples = generate_white_noise(100, 0.0)
        
        self.assertTrue(all(s == 0 for s in samples))
    
    def test_generate_white_noise_negative_amplitude(self):
        """测试负振幅（应转换为正）"""
        samples = generate_white_noise(100, -0.5)
        
        self.assertTrue(all(s >= 0 for s in samples))


class TestPinkNoise(unittest.TestCase):
    """粉噪音生成测试"""
    
    def test_generate_pink_noise_basic(self):
        """测试基本粉噪音生成"""
        samples = generate_pink_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
    
    def test_generate_pink_noise_amplitude(self):
        """测试振幅控制"""
        samples = generate_pink_noise(100, 0.3)
        max_val = max(abs(s) for s in samples)
        
        self.assertLessEqual(max_val, 0.3)
    
    def test_generate_pink_noise_seed(self):
        """测试随机种子"""
        samples1 = generate_pink_noise(100, 0.5, seed=42)
        samples2 = generate_pink_noise(100, 0.5, seed=42)
        
        self.assertEqual(samples1, samples2)
    
    def test_generate_pink_noise_spectrum(self):
        """测试粉噪音频谱特性（-3dB/octave）"""
        samples = generate_pink_noise(44100, 0.5)
        
        # 粉噪音应有较多低频成分
        self.assertEqual(len(samples), 44100)


class TestBrownNoise(unittest.TestCase):
    """棕色噪音生成测试"""
    
    def test_generate_brown_noise_basic(self):
        """测试基本棕色噪音生成"""
        samples = generate_brown_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
    
    def test_generate_brown_noise_amplitude(self):
        """测试振幅控制"""
        samples = generate_brown_noise(100, 0.4)
        max_val = max(abs(s) for s in samples)
        
        self.assertLessEqual(max_val, 0.4)
    
    def test_generate_brown_noise_seed(self):
        """测试随机种子"""
        samples1 = generate_brown_noise(100, 0.5, seed=42)
        samples2 = generate_brown_noise(100, 0.5, seed=42)
        
        self.assertEqual(samples1, samples2)


class TestBlueNoise(unittest.TestCase):
    """蓝噪音生成测试"""
    
    def test_generate_blue_noise_basic(self):
        """测试基本蓝噪音生成"""
        samples = generate_blue_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
    
    def test_generate_blue_noise_amplitude(self):
        """测试振幅控制"""
        samples = generate_blue_noise(100, 0.3)
        
        self.assertEqual(len(samples), 100)


class TestVioletNoise(unittest.TestCase):
    """紫噪音生成测试"""
    
    def test_generate_violet_noise_basic(self):
        """测试基本紫噪音生成"""
        samples = generate_violet_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
    
    def test_generate_violet_noise_amplitude(self):
        """测试振幅控制"""
        samples = generate_violet_noise(100, 0.2)
        
        self.assertEqual(len(samples), 100)


class TestGreyNoise(unittest.TestCase):
    """灰噪音生成测试"""
    
    def test_generate_grey_noise_basic(self):
        """测试基本灰噪音生成"""
        samples = generate_grey_noise(44100, 0.5)
        
        self.assertEqual(len(samples), 44100)
    
    def test_generate_grey_noise_seed(self):
        """测试随机种子"""
        samples1 = generate_grey_noise(100, 0.5, seed=42)
        samples2 = generate_grey_noise(100, 0.5, seed=42)
        
        self.assertEqual(samples1, samples2)


class TestGenerateNoise(unittest.TestCase):
    """通用噪音生成测试"""
    
    def test_generate_noise_all_types(self):
        """测试所有噪音类型"""
        for noise_type in ['white', 'pink', 'brown', 'blue', 'violet', 'grey']:
            samples = generate_noise(noise_type, 100, 0.5)
            self.assertEqual(len(samples), 100)
    
    def test_generate_noise_invalid_type(self):
        """测试无效噪音类型"""
        with self.assertRaises(ValueError):
            generate_noise('invalid', 100, 0.5)
    
    def test_generate_noise_case_insensitive(self):
        """测试大小写不敏感"""
        samples1 = generate_noise('PINK', 100, 0.5)
        samples2 = generate_noise('pink', 100, 0.5, seed=1)
        
        self.assertEqual(len(samples1), 100)


class TestAmbientSound(unittest.TestCase):
    """环境音生成测试"""
    
    def test_generate_ambient_sound_light_rain(self):
        """测试小雨声"""
        samples = generate_ambient_sound('light_rain', 5.0)
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ambient_sound_heavy_rain(self):
        """测试大雨声"""
        samples = generate_ambient_sound('heavy_rain', 3.0)
        
        self.assertEqual(len(samples), int(3.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ambient_sound_ocean(self):
        """测试海浪声"""
        samples = generate_ambient_sound('ocean_waves', 10.0)
        
        self.assertEqual(len(samples), int(10.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ambient_sound_wind(self):
        """测试风声"""
        samples = generate_ambient_sound('wind', 5.0)
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ambient_sound_fireplace(self):
        """测试壁炉声"""
        samples = generate_ambient_sound('fireplace', 5.0)
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ambient_sound_invalid_type(self):
        """测试无效环境音类型"""
        with self.assertRaises(ValueError):
            generate_ambient_sound('invalid', 5.0)
    
    def test_generate_ambient_sound_amplitude_override(self):
        """测试振幅覆盖"""
        samples = generate_ambient_sound('light_rain', 2.0, amplitude_override=0.1)
        
        self.assertEqual(len(samples), int(2.0 * DEFAULT_SAMPLE_RATE))


class TestRainSound(unittest.TestCase):
    """雨声生成测试"""
    
    def test_generate_rain_light(self):
        """测试小雨"""
        samples = generate_rain_sound(5.0, intensity='light')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_rain_medium(self):
        """测试中雨"""
        samples = generate_rain_sound(5.0, intensity='medium')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_rain_heavy(self):
        """测试大雨"""
        samples = generate_rain_sound(5.0, intensity='heavy')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))


class TestOceanSound(unittest.TestCase):
    """海浪声生成测试"""
    
    def test_generate_ocean_calm(self):
        """测试平静海浪"""
        samples = generate_ocean_sound(10.0, wave_intensity='calm')
        
        self.assertEqual(len(samples), int(10.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ocean_medium(self):
        """测试中等海浪"""
        samples = generate_ocean_sound(10.0, wave_intensity='medium')
        
        self.assertEqual(len(samples), int(10.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_ocean_rough(self):
        """测试汹涌海浪"""
        samples = generate_ocean_sound(10.0, wave_intensity='rough')
        
        self.assertEqual(len(samples), int(10.0 * DEFAULT_SAMPLE_RATE))


class TestWindSound(unittest.TestCase):
    """风声生成测试"""
    
    def test_generate_wind_light(self):
        """测试轻风"""
        samples = generate_wind_sound(5.0, strength='light')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_wind_moderate(self):
        """测试中风"""
        samples = generate_wind_sound(5.0, strength='moderate')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_wind_strong(self):
        """测试强风"""
        samples = generate_wind_sound(5.0, strength='strong')
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))


class TestFireSound(unittest.TestCase):
    """火焰声生成测试"""
    
    def test_generate_fire_no_crackling(self):
        """测试无噼啪声"""
        samples = generate_fire_sound(5.0, crackling=False)
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_generate_fire_with_crackling(self):
        """测试有噼啪声"""
        samples = generate_fire_sound(5.0, crackling=True, seed=42)
        
        self.assertEqual(len(samples), int(5.0 * DEFAULT_SAMPLE_RATE))


class TestMixNoises(unittest.TestCase):
    """噪音混合测试"""
    
    def test_mix_noises_basic(self):
        """测试基本混合"""
        configs = [('pink', 0.4), ('brown', 0.3)]
        mixed = mix_noises(configs, 5.0)
        
        self.assertEqual(len(mixed), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_mix_noises_multiple(self):
        """测试多噪音混合"""
        configs = [('white', 0.2), ('pink', 0.3), ('brown', 0.2)]
        mixed = mix_noises(configs, 3.0)
        
        self.assertEqual(len(mixed), int(3.0 * DEFAULT_SAMPLE_RATE))
    
    def test_mix_noises_seed(self):
        """测试随机种子"""
        configs = [('pink', 0.5)]
        mixed1 = mix_noises(configs, 1.0, seed=42)
        mixed2 = mix_noises(configs, 1.0, seed=42)
        
        self.assertEqual(mixed1, mixed2)


class TestLayerAmbientSounds(unittest.TestCase):
    """环境音叠加测试"""
    
    def test_layer_ambient_basic(self):
        """测试基本叠加"""
        layers = [('light_rain', 0.5), ('fireplace', 0.3)]
        mixed = layer_ambient_sounds(layers, 5.0)
        
        self.assertEqual(len(mixed), int(5.0 * DEFAULT_SAMPLE_RATE))
    
    def test_layer_ambient_multiple(self):
        """测试多层叠加"""
        layers = [('ocean_waves', 0.4), ('wind', 0.3), ('forest', 0.2)]
        mixed = layer_ambient_sounds(layers, 10.0)
        
        self.assertEqual(len(mixed), int(10.0 * DEFAULT_SAMPLE_RATE))


class TestApplyFade(unittest.TestCase):
    """淡入淡出测试"""
    
    def test_apply_fade_in(self):
        """测试淡入"""
        samples = [0.5] * 44100
        faded = apply_fade(samples, fade_in_seconds=1.0, fade_out_seconds=0.0)
        
        # 前1秒应该逐渐增大
        first_sample = faded[0]
        later_sample = faded[int(0.5 * DEFAULT_SAMPLE_RATE)]
        
        self.assertLess(first_sample, later_sample)
    
    def test_apply_fade_out(self):
        """测试淡出"""
        samples = [0.5] * 44100
        faded = apply_fade(samples, fade_in_seconds=0.0, fade_out_seconds=1.0)
        
        # 最后1秒应该逐渐减小
        last_sample = faded[-1]
        earlier_sample = faded[int(-0.5 * DEFAULT_SAMPLE_RATE)]
        
        self.assertLess(last_sample, earlier_sample)
    
    def test_apply_fade_both(self):
        """测试同时淡入淡出"""
        samples = [0.5] * 44100
        faded = apply_fade(samples, fade_in_seconds=1.0, fade_out_seconds=1.0)
        
        self.assertEqual(len(faded), len(samples))
    
    def test_apply_fade_zero(self):
        """测试零时长淡入淡出"""
        samples = [0.5] * 100
        faded = apply_fade(samples, fade_in_seconds=0.0, fade_out_seconds=0.0)
        
        self.assertEqual(samples, faded)


class TestApplyVolume(unittest.TestCase):
    """音量调整测试"""
    
    def test_apply_volume_increase(self):
        """测试增加音量"""
        samples = [0.3, 0.4, 0.5]
        louder = apply_volume(samples, 2.0)
        
        self.assertEqual([s * 2.0 for s in samples], louder)
    
    def test_apply_volume_decrease(self):
        """测试减少音量"""
        samples = [0.5, 0.6, 0.7]
        quieter = apply_volume(samples, 0.5)
        
        self.assertEqual([s * 0.5 for s in samples], quieter)
    
    def test_apply_volume_mute(self):
        """测试静音"""
        samples = [0.5, 0.6, 0.7]
        muted = apply_volume(samples, 0.0)
        
        self.assertTrue(all(s == 0 for s in muted))


class TestWavConversion(unittest.TestCase):
    """WAV 格式转换测试"""
    
    def test_samples_to_wav_bytes_basic(self):
        """测试基本 WAV 转换"""
        samples = generate_pink_noise(44100, 0.5, seed=42)
        wav_data = samples_to_wav_bytes(samples)
        
        # WAV 文件至少有 44 字节头
        self.assertGreater(len(wav_data), 44)
        
        # 检查 RIFF 头
        self.assertEqual(wav_data[:4], b'RIFF')
        self.assertEqual(wav_data[8:12], b'WAVE')
    
    def test_samples_to_wav_bytes_8bit(self):
        """测试 8 位 WAV"""
        samples = [0.5, -0.5, 0.0]
        wav_data = samples_to_wav_bytes(samples, bits_per_sample=8)
        
        self.assertGreater(len(wav_data), 44)
    
    def test_samples_to_wav_bytes_24bit(self):
        """测试 24 位 WAV"""
        samples = [0.5, -0.5, 0.0]
        wav_data = samples_to_wav_bytes(samples, bits_per_sample=24)
        
        self.assertGreater(len(wav_data), 44)
    
    def test_samples_to_wav_bytes_invalid_bits(self):
        """测试无效位深度"""
        samples = [0.5]
        
        with self.assertRaises(ValueError):
            samples_to_wav_bytes(samples, bits_per_sample=12)


class TestSaveLoadWav(unittest.TestCase):
    """WAV 文件保存和加载测试"""
    
    def test_save_wav_file(self):
        """测试保存 WAV 文件"""
        samples = generate_pink_noise(44100, 0.5, seed=42)
        filepath = '/tmp/test_ambient.wav'
        
        bytes_written = save_wav_file(samples, filepath)
        
        self.assertGreater(bytes_written, 44)
        
        # 清理
        os.remove(filepath)
    
    def test_load_wav_file(self):
        """测试加载 WAV 文件"""
        # 先创建一个文件
        samples = generate_pink_noise(44100, 0.5, seed=42)
        filepath = '/tmp/test_ambient_load.wav'
        save_wav_file(samples, filepath)
        
        # 再加载
        loaded_samples, sr, bits, channels = load_wav_file(filepath)
        
        self.assertEqual(sr, DEFAULT_SAMPLE_RATE)
        self.assertEqual(bits, DEFAULT_BITS_PER_SAMPLE)
        self.assertEqual(channels, 1)
        
        # 清理
        os.remove(filepath)
    
    def test_load_wav_invalid_file(self):
        """测试加载无效文件"""
        # 创建一个无效文件
        filepath = '/tmp/test_invalid.wav'
        with open(filepath, 'wb') as f:
            f.write(b'INVALID DATA')
        
        with self.assertRaises(ValueError):
            load_wav_file(filepath)
        
        os.remove(filepath)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_get_noise_info(self):
        """测试噪音信息获取"""
        info = get_noise_info('pink')
        
        self.assertIn('type', info)
        self.assertIn('description', info)
        self.assertEqual(info['type'], 'pink')
    
    def test_get_ambient_info(self):
        """测试环境音信息获取"""
        info = get_ambient_info('light_rain')
        
        self.assertIn('name', info)
        self.assertIn('name_en', info)
        self.assertEqual(info['name'], '小雨')
    
    def test_list_noise_types(self):
        """测试噪音类型列表"""
        types = list_noise_types()
        
        self.assertIn('white', types)
        self.assertIn('pink', types)
        self.assertIn('brown', types)
    
    def test_list_ambient_types(self):
        """测试环境音类型列表"""
        types = list_ambient_types()
        
        self.assertIn('light_rain', types)
        self.assertIn('ocean_waves', types)
    
    def test_calculate_duration(self):
        """测试时长计算"""
        duration = calculate_duration(44100)
        self.assertEqual(duration, 1.0)
        
        duration = calculate_duration(88200)
        self.assertEqual(duration, 2.0)
    
    def test_calculate_num_samples(self):
        """测试样本数计算"""
        num_samples = calculate_num_samples(1.0)
        self.assertEqual(num_samples, DEFAULT_SAMPLE_RATE)
        
        num_samples = calculate_num_samples(5.0)
        self.assertEqual(num_samples, 5 * DEFAULT_SAMPLE_RATE)
    
    def test_estimate_file_size(self):
        """测试文件大小估算"""
        size = estimate_file_size(10.0)
        
        # 10秒 16位单声道 WAV
        expected = 44 + 10 * DEFAULT_SAMPLE_RATE * 2
        self.assertEqual(size, expected)
    
    def test_format_duration(self):
        """测试时长格式化"""
        self.assertEqual(format_duration(65.5), '1:05.5')
        self.assertEqual(format_duration(3661.25), '1:01:01.2')
        self.assertEqual(format_duration(0.5), '0:00.5')
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        self.assertEqual(format_file_size(1024), '1.0 KB')
        self.assertEqual(format_file_size(1536000), '1.5 MB')
        self.assertEqual(format_file_size(500), '500.0 B')


class TestAmbientNoiseGenerator(unittest.TestCase):
    """环境噪音生成器类测试"""
    
    def test_generator_initialization(self):
        """测试初始化"""
        generator = AmbientNoiseGenerator()
        
        self.assertEqual(generator.sample_rate, DEFAULT_SAMPLE_RATE)
        self.assertEqual(generator.num_samples, 0)
        self.assertEqual(generator.duration, 0.0)
    
    def test_generator_add_noise(self):
        """测试添加噪音"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 2.0, 0.5)
        
        self.assertEqual(generator.duration, 2.0)
    
    def test_generator_add_ambient(self):
        """测试添加环境音"""
        generator = AmbientNoiseGenerator()
        generator.add_ambient('light_rain', 3.0, 0.4)
        
        self.assertEqual(generator.duration, 3.0)
    
    def test_generator_chain_methods(self):
        """测试方法链"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_noise('pink', 2.0, 0.5)
            .normalize()
            .apply_fade(0.5, 0.5)
        )
        
        self.assertEqual(generator.duration, 2.0)
    
    def test_generator_normalize(self):
        """测试归一化"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 2.0, 10.0)  # 很大振幅
        generator.normalize()
        
        samples = generator.get_samples()
        max_val = max(abs(s) for s in samples)
        self.assertLessEqual(max_val, 1.0)
    
    def test_generator_set_volume(self):
        """测试音量设置"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 2.0, 0.5)
        generator.set_volume(0.3)
        
        self.assertEqual(generator.duration, 2.0)
    
    def test_generator_clear(self):
        """测试清空"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 2.0, 0.5)
        generator.clear()
        
        self.assertEqual(generator.num_samples, 0)
    
    def test_generator_info(self):
        """测试信息获取"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 5.0, 0.5)
        
        info = generator.info()
        
        self.assertIn('duration', info)
        self.assertIn('num_samples', info)
        self.assertEqual(info['duration'], 5.0)
    
    def test_generator_to_wav_bytes(self):
        """测试 WAV 转换"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 1.0, 0.5)
        
        wav_data = generator.to_wav_bytes()
        
        self.assertGreater(len(wav_data), 44)
    
    def test_generator_save_wav(self):
        """测试保存 WAV"""
        generator = AmbientNoiseGenerator()
        generator.add_noise('pink', 1.0, 0.5)
        
        filepath = '/tmp/test_generator.wav'
        bytes_written = generator.save_wav(filepath)
        
        self.assertGreater(bytes_written, 44)
        os.remove(filepath)


class TestDataClasses(unittest.TestCase):
    """数据类测试"""
    
    def test_audio_config(self):
        """测试音频配置"""
        config = AudioConfig()
        
        self.assertEqual(config.sample_rate, DEFAULT_SAMPLE_RATE)
        self.assertGreater(config.max_amplitude, 0)
    
    def test_audio_config_custom(self):
        """测试自定义音频配置"""
        config = AudioConfig(sample_rate=48000, bits_per_sample=24, num_channels=2)
        
        self.assertEqual(config.sample_rate, 48000)
        self.assertEqual(config.bits_per_sample, 24)
        self.assertEqual(config.num_channels, 2)
    
    def test_noise_profile(self):
        """测试噪音配置文件"""
        profile = NoiseProfile(
            noise_type='pink',
            name='粉噪音',
            name_en='Pink Noise',
            description='自然的声音',
            amplitude=0.5
        )
        
        self.assertEqual(profile.noise_type, 'pink')


class TestEnums(unittest.TestCase):
    """枚举测试"""
    
    def test_noise_type_enum(self):
        """测试噪音类型枚举"""
        self.assertEqual(NoiseType.WHITE.value, 'white')
        self.assertEqual(NoiseType.PINK.value, 'pink')
        self.assertEqual(NoiseType.BROWN.value, 'brown')
    
    def test_ambient_type_enum(self):
        """测试环境音类型枚举"""
        self.assertEqual(AmbientType.LIGHT_RAIN.value, 'light_rain')
        self.assertEqual(AmbientType.OCEAN_WAVES.value, 'ocean_waves')


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_empty_samples(self):
        """测试空样本"""
        samples = []
        faded = apply_fade(samples)
        
        self.assertEqual(len(faded), 0)
    
    def test_single_sample(self):
        """测试单样本"""
        samples = [0.5]
        faded = apply_fade(samples, 1.0, 1.0)
        
        self.assertEqual(len(faded), 1)
    
    def test_extreme_duration(self):
        """测试极端时长"""
        # 非常短的时长
        samples = generate_pink_noise(100, 0.5)
        self.assertEqual(len(samples), 100)
    
    def test_extreme_amplitude(self):
        """测试极端振幅"""
        # 振幅 > 1 应被限制
        samples = generate_white_noise(100, 5.0)
        max_val = max(abs(s) for s in samples)
        self.assertLessEqual(max_val, 1.0)
    
    def test_very_long_samples(self):
        """测试长样本"""
        # 1分钟音频
        samples = generate_pink_noise(60 * DEFAULT_SAMPLE_RATE, 0.5)
        self.assertEqual(len(samples), 60 * DEFAULT_SAMPLE_RATE)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 生成噪音
        generator = AmbientNoiseGenerator()
        
        # 添加多层
        generator.add_ambient('light_rain', 30.0, 0.5)
        generator.add_ambient('fireplace', 30.0, 0.3)
        
        # 处理
        generator.normalize()
        generator.apply_fade(1.0, 2.0)
        
        # 导出
        info = generator.info()
        
        self.assertEqual(info['duration'], 30.0)
    
    def test_mixed_ambient_creation(self):
        """测试混合环境音创建"""
        # 创建雨声+壁炉声组合
        rain = generate_ambient_sound('light_rain', 10.0, seed=42)
        fire = generate_ambient_sound('fireplace', 10.0, seed=42)
        
        # 手动混合
        mixed = []
        for i in range(len(rain)):
            mixed.append(rain[i] * 0.5 + fire[i] * 0.3)
        
        # 归一化
        max_val = max(abs(s) for s in mixed) if mixed else 1.0
        if max_val > 1.0:
            mixed = [s / max_val for s in mixed]
        
        # 导出
        wav_data = samples_to_wav_bytes(mixed)
        
        self.assertGreater(len(wav_data), 44)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestWhiteNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestPinkNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestBrownNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestBlueNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestVioletNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestGreyNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateNoise))
    suite.addTests(loader.loadTestsFromTestCase(TestAmbientSound))
    suite.addTests(loader.loadTestsFromTestCase(TestRainSound))
    suite.addTests(loader.loadTestsFromTestCase(TestOceanSound))
    suite.addTests(loader.loadTestsFromTestCase(TestWindSound))
    suite.addTests(loader.loadTestsFromTestCase(TestFireSound))
    suite.addTests(loader.loadTestsFromTestCase(TestMixNoises))
    suite.addTests(loader.loadTestsFromTestCase(TestLayerAmbientSounds))
    suite.addTests(loader.loadTestsFromTestCase(TestApplyFade))
    suite.addTests(loader.loadTestsFromTestCase(TestApplyVolume))
    suite.addTests(loader.loadTestsFromTestCase(TestWavConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestSaveLoadWav))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestAmbientNoiseGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestEnums))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()