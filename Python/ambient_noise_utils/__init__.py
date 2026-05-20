#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Ambient Noise Generator Utilities

环境噪音生成器模块，支持各种噪音类型和环境声音生成。

Usage:
    from ambient_noise_utils import generate_pink_noise, save_wav_file
    
    samples = generate_pink_noise(44100, 0.5)  # 1秒粉噪音
    save_wav_file(samples, 'noise.wav')
"""

from .mod import (
    # Noise generation functions
    generate_white_noise,
    generate_pink_noise,
    generate_brown_noise,
    generate_blue_noise,
    generate_violet_noise,
    generate_grey_noise,
    generate_noise,
    
    # Ambient sound generation functions
    generate_ambient_sound,
    generate_rain_sound,
    generate_ocean_sound,
    generate_wind_sound,
    generate_fire_sound,
    
    # Mixing and effect functions
    mix_noises,
    layer_ambient_sounds,
    apply_fade,
    apply_volume,
    
    # WAV file functions
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
    
    # Classes
    AmbientNoiseGenerator,
    AudioConfig,
    NoiseType,
    AmbientType,
    NoiseProfile,
    MixedNoiseConfig,
    
    # Constants
    DEFAULT_SAMPLE_RATE,
    DEFAULT_BITS_PER_SAMPLE,
    DEFAULT_NUM_CHANNELS,
    NOISE_DESCRIPTIONS,
    AMBIENT_PRESETS,
)

__all__ = [
    # Noise generation
    'generate_white_noise',
    'generate_pink_noise',
    'generate_brown_noise',
    'generate_blue_noise',
    'generate_violet_noise',
    'generate_grey_noise',
    'generate_noise',
    
    # Ambient sounds
    'generate_ambient_sound',
    'generate_rain_sound',
    'generate_ocean_sound',
    'generate_wind_sound',
    'generate_fire_sound',
    
    # Mixing and effects
    'mix_noises',
    'layer_ambient_sounds',
    'apply_fade',
    'apply_volume',
    
    # WAV file operations
    'samples_to_wav_bytes',
    'save_wav_file',
    'load_wav_file',
    
    # Utilities
    'get_noise_info',
    'get_ambient_info',
    'list_noise_types',
    'list_ambient_types',
    'calculate_duration',
    'calculate_num_samples',
    'estimate_file_size',
    'format_duration',
    'format_file_size',
    
    # Classes
    'AmbientNoiseGenerator',
    'AudioConfig',
    'NoiseType',
    'AmbientType',
    'NoiseProfile',
    'MixedNoiseConfig',
    
    # Constants
    'DEFAULT_SAMPLE_RATE',
    'DEFAULT_BITS_PER_SAMPLE',
    'DEFAULT_NUM_CHANNELS',
    'NOISE_DESCRIPTIONS',
    'AMBIENT_PRESETS',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit Contributors'
__license__ = 'MIT'