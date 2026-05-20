#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Ambient Noise Generator Utilities Tests
=====================================================

Comprehensive tests for the ambient noise generator module.

Run with: python -m pytest test_ambient_noise_utils.py -v
Or directly: python test_ambient_noise_utils.py
"""

import sys
import os
import tempfile
import math
import random

# Add module path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Noise generation
    generate_white_noise,
    generate_pink_noise,
    generate_brown_noise,
    generate_blue_noise,
    generate_violet_noise,
    generate_grey_noise,
    generate_noise,
    
    # Ambient sound generation
    generate_ambient_sound,
    generate_rain_sound,
    generate_ocean_sound,
    generate_wind_sound,
    generate_fire_sound,
    
    # Mixing functions
    mix_noises,
    layer_ambient_sounds,
    apply_fade,
    apply_volume,
    
    # WAV functions
    samples_to_wav_bytes,
    save_wav_file,
    load_wav_file,
    
    # Utility functions
    get_noise_info,
    get_ambient_info,
    list_noise_types,
    list_ambient_types,
    calculate_duration,
    calculate_num_samples,
    estimate_file_size,
    format_duration,
    format_file_size,
    
    # Constants
    DEFAULT_SAMPLE_RATE,
    DEFAULT_BITS_PER_SAMPLE,
    DEFAULT_NUM_CHANNELS,
    
    # Classes
    AmbientNoiseGenerator,
    AudioConfig,
    NoiseType,
    AmbientType,
    
    # Data
    NOISE_DESCRIPTIONS,
    AMBIENT_PRESETS,
)


class TestNoiseGeneration:
    """噪音生成测试"""
    
    def test_white_noise_generation(self):
        """测试白噪音生成"""
        samples = generate_white_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
        
        # 验证种子可重复性
        samples2 = generate_white_noise(1000, 0.5, seed=42)
        assert samples == samples2
    
    def test_pink_noise_generation(self):
        """测试粉噪音生成"""
        samples = generate_pink_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
    
    def test_brown_noise_generation(self):
        """测试棕色噪音生成"""
        samples = generate_brown_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
    
    def test_blue_noise_generation(self):
        """测试蓝噪音生成"""
        samples = generate_blue_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
    
    def test_violet_noise_generation(self):
        """测试紫噪音生成"""
        samples = generate_violet_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
    
    def test_grey_noise_generation(self):
        """测试灰噪音生成"""
        samples = generate_grey_noise(1000, 0.5, seed=42)
        
        assert len(samples) == 1000
        assert all(-0.5 <= s <= 0.5 for s in samples)
    
    def test_generate_noise_all_types(self):
        """测试通用噪音生成函数"""
        noise_types = ['white', 'pink', 'brown', 'blue', 'violet', 'grey']
        
        for noise_type in noise_types:
            samples = generate_noise(noise_type, 100, 0.3, seed=42)
            assert len(samples) == 100
    
    def test_generate_noise_invalid_type(self):
        """测试无效噪音类型"""
        try:
            generate_noise('invalid_type', 100)
            assert False, "应该抛出异常"
        except ValueError as e:
            assert '无效的噪音类型' in str(e)
    
    def test_noise_amplitude_bounds(self):
        """测试振幅边界"""
        # 振幅为 0
        samples = generate_white_noise(100, 0.0)
        assert all(s == 0 for s in samples)
        
        # 振幅为 1
        samples = generate_white_noise(100, 1.0)
        assert all(-1 <= s <= 1 for s in samples)
        
        # 超出范围自动校正
        samples = generate_white_noise(100, 2.0)
        assert all(-1 <= s <= 1 for s in samples)


class TestAmbientSoundGeneration:
    """环境音生成测试"""
    
    def test_ambient_sound_generation(self):
        """测试环境音生成"""
        for ambient_type in ['light_rain', 'heavy_rain', 'ocean_waves', 'wind']:
            samples = generate_ambient_sound(ambient_type, 1.0, seed=42)
            assert len(samples) == DEFAULT_SAMPLE_RATE
    
    def test_ambient_sound_invalid_type(self):
        """测试无效环境音类型"""
        try:
            generate_ambient_sound('invalid', 1.0)
            assert False, "应该抛出异常"
        except ValueError as e:
            assert '无效的环境音类型' in str(e)
    
    def test_rain_sound_generation(self):
        """测试雨声生成"""
        for intensity in ['light', 'medium', 'heavy']:
            samples = generate_rain_sound(2.0, intensity)
            assert len(samples) == 2 * DEFAULT_SAMPLE_RATE
    
    def test_ocean_sound_generation(self):
        """测试海浪声生成"""
        for intensity in ['calm', 'medium', 'rough']:
            samples = generate_ocean_sound(2.0, intensity)
            assert len(samples) == 2 * DEFAULT_SAMPLE_RATE
    
    def test_wind_sound_generation(self):
        """测试风声生成"""
        for strength in ['light', 'moderate', 'strong']:
            samples = generate_wind_sound(2.0, strength)
            assert len(samples) == 2 * DEFAULT_SAMPLE_RATE
    
    def test_fire_sound_generation(self):
        """测试火焰声生成"""
        samples_no_crackle = generate_fire_sound(2.0, crackling=False, seed=42)
        samples_with_crackle = generate_fire_sound(2.0, crackling=True, seed=42)
        
        assert len(samples_no_crackle) == 2 * DEFAULT_SAMPLE_RATE
        assert len(samples_with_crackle) == 2 * DEFAULT_SAMPLE_RATE
        
        # 带噼啪声应该有不同的样本
        assert samples_no_crackle != samples_with_crackle


class TestNoiseMixing:
    """噪音混合测试"""
    
    def test_mix_noises(self):
        """测试噪音混合"""
        mixed = mix_noises([('pink', 0.4), ('brown', 0.3)], 2.0, seed=42)
        
        assert len(mixed) == 2 * DEFAULT_SAMPLE_RATE
    
    def test_layer_ambient_sounds(self):
        """测试环境音叠加"""
        layered = layer_ambient_sounds([('light_rain', 0.5), ('fireplace', 0.3)], 2.0, seed=42)
        
        assert len(layered) == 2 * DEFAULT_SAMPLE_RATE
    
    def test_apply_fade(self):
        """测试淡入淡出"""
        samples = generate_pink_noise(1000, 0.5, seed=42)
        faded = apply_fade(samples, 0.01, 0.01, DEFAULT_SAMPLE_RATE)
        
        assert len(faded) == 1000
        
        # 淡入起始应该接近 0
        assert abs(faded[0]) < abs(samples[0])
        
        # 淡出结尾应该接近 0
        assert abs(faded[-1]) < abs(samples[-1])
    
    def test_apply_volume(self):
        """测试音量调整"""
        samples = generate_white_noise(100, 0.5, seed=42)
        
        # 减小音量
        quieter = apply_volume(samples, 0.5)
        assert all(abs(s) <= 0.25 for s in quieter)
        
        # 增大音量
        louder = apply_volume(samples, 1.5)
        assert all(abs(s) <= 0.75 for s in louder)


class TestWavFunctions:
    """WAV 文件测试"""
    
    def test_samples_to_wav_bytes(self):
        """测试 WAV 字节转换"""
        samples = generate_pink_noise(1000, 0.5, seed=42)
        wav_data = samples_to_wav_bytes(samples)
        
        # WAV 头部是 44 字节
        assert len(wav_data) == 44 + 1000 * 2  # 16-bit = 2 bytes per sample
        
        # 验证 WAV 标识
        assert wav_data[:4] == b'RIFF'
        assert wav_data[8:12] == b'WAVE'
        assert wav_data[12:16] == b'fmt '
        assert wav_data[36:40] == b'data'
    
    def test_wav_bits_per_sample(self):
        """测试不同位深度的 WAV"""
        samples = generate_white_noise(100, 0.5, seed=42)
        
        # 8-bit
        wav_8 = samples_to_wav_bytes(samples, bits_per_sample=8)
        assert wav_8[34:36] == struct_pack('<H', 8)
        
        # 16-bit
        wav_16 = samples_to_wav_bytes(samples, bits_per_sample=16)
        assert wav_16[34:36] == struct_pack('<H', 16)
    
    def test_save_and_load_wav(self):
        """测试 WAV 文件保存和加载"""
        original_samples = generate_pink_noise(44100, 0.5, seed=42)
        original_samples = apply_fade(original_samples, 0.5, 0.5)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            filepath = f.name
        
        try:
            # 保存
            save_wav_file(original_samples, filepath)
            
            # 加载
            loaded_samples, sr, bits, ch = load_wav_file(filepath)
            
            assert sr == DEFAULT_SAMPLE_RATE
            assert bits == DEFAULT_BITS_PER_SAMPLE
            assert ch == DEFAULT_NUM_CHANNELS
            assert len(loaded_samples) == len(original_samples)
            
            # 样本应该大致相同（允许轻微精度损失）
            for i in range(0, len(original_samples), 100):
                assert abs(original_samples[i] - loaded_samples[i]) < 0.01
        finally:
            os.unlink(filepath)
    
    def test_invalid_wav_file(self):
        """测试无效 WAV 文件"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(b'invalid data')
            filepath = f.name
        
        try:
            try:
                load_wav_file(filepath)
                assert False, "应该抛出异常"
            except ValueError as e:
                assert '无效' in str(e)
        finally:
            os.unlink(filepath)


# Helper for struct.pack compatibility
def struct_pack(fmt, val):
    import struct
    return struct.pack(fmt, val)


class TestUtilityFunctions:
    """工具函数测试"""
    
    def test_get_noise_info(self):
        """测试噪音信息获取"""
        info = get_noise_info('pink')
        
        assert info['type'] == 'pink'
        assert '粉噪音' in info['description']
    
    def test_get_ambient_info(self):
        """测试环境音信息获取"""
        info = get_ambient_info('light_rain')
        
        assert info['type'] == 'light_rain'
        assert info['name'] == '小雨'
        assert info['name_en'] == 'Light Rain'
    
    def test_list_noise_types(self):
        """测试噪音类型列表"""
        types = list_noise_types()
        
        assert 'white' in types
        assert 'pink' in types
        assert 'brown' in types
        assert len(types) >= 6
    
    def test_list_ambient_types(self):
        """测试环境音类型列表"""
        types = list_ambient_types()
        
        assert 'light_rain' in types
        assert 'ocean_waves' in types
        assert len(types) >= 10
    
    def test_calculate_duration(self):
        """测试时长计算"""
        duration = calculate_duration(44100)
        assert duration == 1.0
        
        duration = calculate_duration(88200)
        assert duration == 2.0
    
    def test_calculate_num_samples(self):
        """测试样本数计算"""
        samples = calculate_num_samples(1.0)
        assert samples == DEFAULT_SAMPLE_RATE
        
        samples = calculate_num_samples(2.5)
        assert samples == int(2.5 * DEFAULT_SAMPLE_RATE)
    
    def test_estimate_file_size(self):
        """测试文件大小估算"""
        size = estimate_file_size(1.0)
        
        # WAV 头部 44 字节 + 数据
        expected = 44 + DEFAULT_SAMPLE_RATE * 2  # 16-bit mono
        assert size == expected
    
    def test_format_duration(self):
        """测试时长格式化"""
        assert format_duration(65.5) == '1:05.5'
        assert format_duration(3661.25) == '1:01:01.2'
        assert format_duration(30.0) == '0:30.0'
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        assert format_file_size(1024) == '1.0 KB'
        assert format_file_size(1536000) == '1.5 MB'
        assert format_file_size(512) == '512.0 B'


class TestAmbientNoiseGenerator:
    """噪音生成器类测试"""
    
    def test_generator_basic(self):
        """测试生成器基本功能"""
        generator = AmbientNoiseGenerator()
        
        assert generator.duration == 0.0
        assert generator.num_samples == 0
    
    def test_generator_add_noise(self):
        """测试生成器添加噪音"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_noise('pink', 2.0, 0.5)
        )
        
        assert generator.duration == 2.0
        assert generator.num_samples == 2 * DEFAULT_SAMPLE_RATE
    
    def test_generator_add_ambient(self):
        """测试生成器添加环境音"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_ambient('light_rain', 3.0, 0.4)
        )
        
        assert generator.duration == 3.0
    
    def test_generator_chain_operations(self):
        """测试生成器链式操作"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_ambient('light_rain', 5.0, 0.5)
            .add_ambient('fireplace', 5.0, 0.3)
            .normalize()
            .apply_fade(0.5, 1.0)
        )
        
        samples = generator.get_samples()
        assert len(samples) == 5 * DEFAULT_SAMPLE_RATE
        
        # 淡入淡出应该生效
        assert abs(samples[0]) < 0.1
        assert abs(samples[-1]) < 0.1
    
    def test_generator_wav_output(self):
        """测试生成器 WAV 输出"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_noise('pink', 1.0, 0.5)
        )
        
        wav_bytes = generator.to_wav_bytes()
        assert wav_bytes[:4] == b'RIFF'
        
        info = generator.info()
        assert info['sample_rate'] == DEFAULT_SAMPLE_RATE
        assert info['duration'] == 1.0
    
    def test_generator_save_wav(self):
        """测试生成器保存文件"""
        generator = (
            AmbientNoiseGenerator()
            .set_seed(42)
            .add_noise('pink', 2.0, 0.5)
        )
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            filepath = f.name
        
        try:
            size = generator.save_wav(filepath)
            assert size > 0
            
            # 验证文件可加载
            samples, sr, bits, ch = load_wav_file(filepath)
            assert len(samples) == 2 * DEFAULT_SAMPLE_RATE
        finally:
            os.unlink(filepath)
    
    def test_generator_clear(self):
        """测试生成器清空"""
        generator = (
            AmbientNoiseGenerator()
            .add_noise('pink', 1.0)
            .clear()
        )
        
        assert generator.num_samples == 0


class TestAudioConfig:
    """音频配置测试"""
    
    def test_audio_config_defaults(self):
        """测试默认配置"""
        config = AudioConfig()
        
        assert config.sample_rate == DEFAULT_SAMPLE_RATE
        assert config.bits_per_sample == DEFAULT_BITS_PER_SAMPLE
        assert config.num_channels == DEFAULT_NUM_CHANNELS
    
    def test_audio_config_properties(self):
        """测试配置属性"""
        config = AudioConfig(bits_per_sample=16)
        
        assert config.max_amplitude == 32767
        assert config.byte_rate == DEFAULT_SAMPLE_RATE * 2
        assert config.block_align == 2


class TestEnums:
    """枚举测试"""
    
    def test_noise_type_enum(self):
        """测试噪音类型枚举"""
        assert NoiseType.WHITE.value == 'white'
        assert NoiseType.PINK.value == 'pink'
        assert NoiseType.BROWN.value == 'brown'
    
    def test_ambient_type_enum(self):
        """测试环境音类型枚举"""
        assert AmbientType.LIGHT_RAIN.value == 'light_rain'
        assert AmbientType.OCEAN_WAVES.value == 'ocean_waves'


class TestConstants:
    """常量测试"""
    
    def test_noise_descriptions(self):
        """测试噪音描述"""
        assert 'white' in NOISE_DESCRIPTIONS
        assert 'pink' in NOISE_DESCRIPTIONS
        assert '白噪音' in NOISE_DESCRIPTIONS['white']
    
    def test_ambient_presets(self):
        """测试环境音预设"""
        assert 'light_rain' in AMBIENT_PRESETS
        assert 'ocean_waves' in AMBIENT_PRESETS
        
        preset = AMBIENT_PRESETS['light_rain']
        assert preset['name'] == '小雨'
        assert preset['base_noise'] == 'pink'


def run_all_tests():
    """运行所有测试"""
    print("Running Ambient Noise Generator Tests...")
    print("=" * 50)
    
    test_classes = [
        TestNoiseGeneration,
        TestAmbientSoundGeneration,
        TestNoiseMixing,
        TestWavFunctions,
        TestUtilityFunctions,
        TestAmbientNoiseGenerator,
        TestAudioConfig,
        TestEnums,
        TestConstants,
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                except Exception as e:
                    print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Tests: {total_tests} total, {passed_tests} passed, {total_tests - passed_tests} failed")
    
    return passed_tests == total_tests


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)