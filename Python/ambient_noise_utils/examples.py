#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Ambient Noise Generator Examples
==============================================

Practical examples demonstrating ambient noise generation capabilities.

Run with: python examples.py
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Basic noise generation
    generate_noise,
    generate_white_noise,
    generate_pink_noise,
    generate_brown_noise,
    
    # Ambient sounds
    generate_ambient_sound,
    generate_rain_sound,
    generate_ocean_sound,
    generate_wind_sound,
    generate_fire_sound,
    
    # Mixing and effects
    mix_noises,
    layer_ambient_sounds,
    apply_fade,
    apply_volume,
    
    # WAV file operations
    save_wav_file,
    estimate_file_size,
    format_file_size,
    format_duration,
    
    # Generator class
    AmbientNoiseGenerator,
    
    # Utilities
    list_noise_types,
    list_ambient_types,
    get_noise_info,
    get_ambient_info,
    DEFAULT_SAMPLE_RATE,
)


def example_1_basic_noise_types():
    """
    示例 1: 基础噪音类型
    
    演示各种噪音类型的生成和特性。
    """
    print("\n" + "=" * 60)
    print("示例 1: 基础噪音类型")
    print("=" * 60)
    
    noise_types = list_noise_types()
    print(f"\n可用的噪音类型: {noise_types}")
    
    duration = 5.0  # 5 秒
    
    for noise_type in ['white', 'pink', 'brown', 'blue']:
        info = get_noise_info(noise_type)
        print(f"\n{noise_type.upper()}:")
        print(f"  描述: {info['description']}")
        
        samples = generate_noise(noise_type, int(duration * DEFAULT_SAMPLE_RATE), 0.5, seed=42)
        print(f"  样本数: {len(samples)}")
        print(f"  时长: {format_duration(duration)}")
        print(f"  文件大小估算: {format_file_size(estimate_file_size(duration))}")


def example_2_ambient_sounds():
    """
    示例 2: 环境声音
    
    演示各种自然环境声音的生成。
    """
    print("\n" + "=" * 60)
    print("示例 2: 环境声音")
    print("=" * 60)
    
    ambient_types = list_ambient_types()
    print(f"\n可用的环境音类型: {ambient_types}")
    
    duration = 10.0
    
    for ambient_type in ['light_rain', 'ocean_waves', 'wind', 'fireplace', 'forest']:
        info = get_ambient_info(ambient_type)
        print(f"\n{info['name']} ({ambient_type}):")
        print(f"  描述: {info['description']}")
        print(f"  基础噪音: {info['base_noise']}")
        
        samples = generate_ambient_sound(ambient_type, duration, seed=42)
        print(f"  样本数: {len(samples)}")


def example_3_rain_intensity():
    """
    示例 3: 雨声强度调节
    
    演示如何生成不同强度的雨声。
    """
    print("\n" + "=" * 60)
    print("示例 3: 雨声强度调节")
    print("=" * 60)
    
    duration = 10.0
    
    intensities = ['light', 'medium', 'heavy']
    
    for intensity in intensities:
        print(f"\n生成 {intensity} 雨声...")
        samples = generate_rain_sound(duration, intensity)
        
        # 计算一些统计信息
        max_amp = max(abs(s) for s in samples)
        avg_amp = sum(abs(s) for s in samples) / len(samples)
        
        print(f"  最大振幅: {max_amp:.3f}")
        print(f"  平均振幅: {avg_amp:.3f}")
        print(f"  样本数: {len(samples)}")


def example_4_mixing_noises():
    """
    示例 4: 混合噪音
    
    演示如何混合多种噪音创建复合声音。
    """
    print("\n" + "=" * 60)
    print("示例 4: 混合噪音")
    print("=" * 60)
    
    duration = 30.0
    
    print("\n混合粉噪音和棕色噪音（自然声音混合）:")
    mixed = mix_noises([('pink', 0.4), ('brown', 0.3)], duration, seed=42)
    print(f"  结果样本数: {len(mixed)}")
    print(f"  时长: {format_duration(duration)}")
    
    print("\n添加蓝噪音增加高频:")
    mixed_high = mix_noises([('pink', 0.3), ('brown', 0.3), ('blue', 0.2)], duration, seed=42)
    print(f"  结果样本数: {len(mixed_high)}")


def example_5_layering_ambient():
    """
    示例 5: 环境音叠加
    
    演示如何叠加多层环境音创建复杂场景。
    """
    print("\n" + "=" * 60)
    print("示例 5: 环境音叠加")
    print("=" * 60)
    
    duration = 60.0
    
    print("\n创建「雨夜壁炉」场景:")
    scene = layer_ambient_sounds([
        ('heavy_rain', 0.5),      # 大雨
        ('fireplace', 0.35),      # 壁炉
        ('night_ambience', 0.2),  # 夜晚背景
    ], duration, seed=42)
    
    print(f"  场景时长: {format_duration(duration)}")
    print(f"  预计文件大小: {format_file_size(estimate_file_size(duration))}")
    
    print("\n创建「海滩森林」场景:")
    scene2 = layer_ambient_sounds([
        ('ocean_waves', 0.4),     # 海浪
        ('forest', 0.3),          # 森林
        ('wind', 0.2),            # 微风
    ], duration, seed=42)
    
    print(f"  场景时长: {format_duration(duration)}")


def example_6_apply_effects():
    """
    示例 6: 应用效果
    
    演示淡入淡出和音量调整效果。
    """
    print("\n" + "=" * 60)
    print("示例 6: 应用效果")
    print("=" * 60)
    
    duration = 30.0
    
    print("\n生成基础粉噪音...")
    samples = generate_pink_noise(int(duration * DEFAULT_SAMPLE_RATE), 0.5, seed=42)
    
    print("\n应用淡入淡出效果:")
    faded = apply_fade(samples, fade_in_seconds=2.0, fade_out_seconds=3.0)
    
    # 检查起始和结尾
    print(f"  原始起始振幅: {abs(samples[0]):.3f}")
    print(f"  淡入后起始振幅: {abs(faded[0]):.3f}")
    print(f"  原始结尾振幅: {abs(samples[-1]):.3f}")
    print(f"  淡出后结尾振幅: {abs(faded[-1]):.3f}")
    
    print("\n调整音量:")
    quiet = apply_volume(samples, 0.3)
    loud = apply_volume(samples, 0.8)
    
    print(f"  30% 音量平均振幅: {sum(abs(s) for s in quiet[:1000])/1000:.3f}")
    print(f"  80% 音量平均振幅: {sum(abs(s) for s in loud[:1000])/1000:.3f}")


def example_7_generator_class():
    """
    示例 7: 使用生成器类
    
    演示 AmbientNoiseGenerator 类的链式操作。
    """
    print("\n" + "=" * 60)
    print("示例 7: 使用生成器类")
    print("=" * 60)
    
    print("\n使用生成器创建「专注工作」音景:")
    generator = (
        AmbientNoiseGenerator()
        .set_seed(42)
        .add_ambient('cafe', 60.0, 0.4)         # 咖啡馆背景
        .add_ambient('light_rain', 60.0, 0.25)  # 轻雨
        .normalize()                            # 归一化
        .apply_fade(1.0, 2.0)                   # 淡入淡出
        .set_volume(0.6)                        # 最终音量
    )
    
    info = generator.info()
    print(f"\n生成器信息:")
    print(f"  采样率: {info['sample_rate']}")
    print(f"  位深度: {info['bits_per_sample']}")
    print(f"  时长: {format_duration(info['duration'])}")
    print(f"  样本数: {info['num_samples']}")
    print(f"  文件大小: {format_file_size(info['file_size'])}")
    
    print("\n创建「深度睡眠」音景:")
    sleep_generator = (
        AmbientNoiseGenerator()
        .set_seed(123)
        .add_ambient('heavy_rain', 120.0, 0.35)     # 大雨
        .add_ambient('night_ambience', 120.0, 0.15) # 夜晚背景
        .normalize()
        .apply_fade(3.0, 5.0)
        .set_volume(0.4)
    )
    
    sleep_info = sleep_generator.info()
    print(f"  时长: {format_duration(sleep_info['duration'])}")
    print(f"  文件大小: {format_file_size(sleep_info['file_size'])}")


def example_8_save_wav_file():
    """
    示例 8: 保存 WAV 文件
    
    演示如何将生成的噪音保存为 WAV 文件。
    """
    print("\n" + "=" * 60)
    print("示例 8: 保存 WAV 文件")
    print("=" * 60)
    
    duration = 10.0
    
    print("\n生成粉噪音并保存...")
    samples = generate_pink_noise(int(duration * DEFAULT_SAMPLE_RATE), 0.5, seed=42)
    samples = apply_fade(samples, 1.0, 1.0)
    
    # 使用临时目录
    output_dir = tempfile.gettempdir()
    filepath = os.path.join(output_dir, 'pink_noise_sample.wav')
    
    print(f"  保存路径: {filepath}")
    size = save_wav_file(samples, filepath)
    print(f"  文件大小: {format_file_size(size)}")
    
    print("\n使用生成器保存复杂音景...")
    generator = (
        AmbientNoiseGenerator()
        .set_seed(42)
        .add_ambient('ocean_waves', 30.0, 0.4)
        .add_ambient('wind', 30.0, 0.2)
        .normalize()
        .apply_fade(2.0, 3.0)
    )
    
    filepath2 = os.path.join(output_dir, 'ocean_wind_ambient.wav')
    size2 = generator.save_wav(filepath2)
    print(f"  保存路径: {filepath2}")
    print(f"  文件大小: {format_file_size(size2)}")
    
    print("\n提示: 实际使用时请将文件保存到需要的目录")


def example_9_file_size_estimation():
    """
    示例 9: 文件大小估算
    
    演示如何估算不同时长和配置的文件大小。
    """
    print("\n" + "=" * 60)
    print("示例 9: 文件大小估算")
    print("=" * 60)
    
    print("\n不同时长（16-bit 单声道，44100Hz）:")
    durations = [10, 30, 60, 120, 300, 600]
    
    for dur in durations:
        size = estimate_file_size(dur)
        print(f"  {format_duration(dur)} ≈ {format_file_size(size)}")
    
    print("\n不同位深度（30秒）:")
    for bits in [8, 16, 24, 32]:
        size = estimate_file_size(30, bits_per_sample=bits)
        print(f"  {bits}-bit: {format_file_size(size)}")


def example_10_quick_presets():
    """
    示例 10: 快速预设生成
    
    演示如何快速生成常见用途的噪音。
    """
    print("\n" + "=" * 60)
    print("示例 10: 快速预设生成")
    print("=" * 60)
    
    print("\n专注/学习 - 50分钟粉噪音:")
    focus_samples = generate_pink_noise(int(50 * 60 * DEFAULT_SAMPLE_RATE), 0.35, seed=42)
    focus_samples = apply_fade(focus_samples, 3.0, 5.0)
    print(f"  时长: {format_duration(50 * 60)}")
    print(f"  文件大小: {format_file_size(estimate_file_size(50 * 60))}")
    
    print("\n睡眠 - 2小时棕色噪音:")
    sleep_samples = generate_brown_noise(int(2 * 60 * 60 * DEFAULT_SAMPLE_RATE), 0.3, seed=42)
    sleep_samples = apply_fade(sleep_samples, 5.0, 10.0)
    print(f"  时长: {format_duration(2 * 60 * 60)}")
    print(f"  文件大小: {format_file_size(estimate_file_size(2 * 60 * 60))}")
    
    print("\n放松 - 30分钟海浪声:")
    relax_samples = generate_ambient_sound('ocean_waves', 30 * 60, amplitude_override=0.3, seed=42)
    relax_samples = apply_fade(relax_samples, 2.0, 3.0)
    print(f"  时长: {format_duration(30 * 60)}")
    print(f"  文件大小: {format_file_size(estimate_file_size(30 * 60))}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("AllToolkit - Ambient Noise Generator Examples")
    print("=" * 60)
    
    examples = [
        example_1_basic_noise_types,
        example_2_ambient_sounds,
        example_3_rain_intensity,
        example_4_mixing_noises,
        example_5_layering_ambient,
        example_6_apply_effects,
        example_7_generator_class,
        example_8_save_wav_file,
        example_9_file_size_estimation,
        example_10_quick_presets,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n示例执行失败: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()