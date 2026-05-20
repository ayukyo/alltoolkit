#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Ambient Noise Generator Utilities
===============================================
A comprehensive ambient noise generation module with zero external dependencies.

Features:
    - White noise generation (equal energy across frequencies)
    - Pink noise generation (-3dB per octave, 1/f noise)
    - Brown/Brownian noise generation (-6dB per octave, 1/f² noise)
    - Blue noise generation (+3dB per octave)
    - Violet noise generation (+6dB per octave)
    - Natural ambient sounds simulation (rain, wind, ocean, forest, fire)
    - Noise mixing and layering
    - WAV file export capability
    - Real-time noise generation

All generated audio is in standard WAV format (16-bit PCM, 44100Hz by default).

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-20
"""

import struct
import math
import random
from typing import List, Tuple, Optional, Callable, BinaryIO
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


# ============================================================================
# Constants
# ============================================================================

# Default audio parameters
DEFAULT_SAMPLE_RATE = 44100  # Hz
DEFAULT_BITS_PER_SAMPLE = 16
DEFAULT_NUM_CHANNELS = 1

# Noise type frequency characteristics
NOISE_DESCRIPTIONS = {
    'white': '白噪音 - 所有频率能量相等，类似静电声',
    'pink': '粉噪音 - 每倍频程能量减半，类似雨声',
    'brown': '棕色噪音 - 每倍频程能量减少6dB，类似瀑布声',
    'blue': '蓝噪音 - 每倍频程能量增加3dB，声音更尖锐',
    'violet': '紫噪音 - 每倍频程能量增加6dB，声音非常尖锐',
    'grey': '灰噪音 - 心理声学补偿，听起来更均匀',
}

# Natural ambient sound presets
AMBIENT_PRESETS = {
    'light_rain': {
        'name': '小雨',
        'name_en': 'Light Rain',
        'description': '轻柔的雨滴声，适合专注和放松',
        'base_noise': 'pink',
        'amplitude': 0.4,
        'modulation': 0.1,
        'modulation_freq': 0.3,
    },
    'heavy_rain': {
        'name': '大雨',
        'name_en': 'Heavy Rain',
        'description': '密集的雨声，适合掩蔽背景噪音',
        'base_noise': 'brown',
        'amplitude': 0.6,
        'modulation': 0.15,
        'modulation_freq': 0.5,
    },
    'thunderstorm': {
        'name': '雷雨',
        'name_en': 'Thunderstorm',
        'description': '带有雷声的暴风雨',
        'base_noise': 'pink',
        'amplitude': 0.5,
        'modulation': 0.3,
        'modulation_freq': 0.2,
    },
    'ocean_waves': {
        'name': '海浪',
        'name_en': 'Ocean Waves',
        'description': '轻柔的海浪拍岸声',
        'base_noise': 'brown',
        'amplitude': 0.45,
        'modulation': 0.25,
        'modulation_freq': 0.08,
    },
    'forest': {
        'name': '森林',
        'name_en': 'Forest',
        'description': '森林环境音，鸟鸣和风吹树叶',
        'base_noise': 'pink',
        'amplitude': 0.35,
        'modulation': 0.2,
        'modulation_freq': 0.15,
    },
    'wind': {
        'name': '风声',
        'name_en': 'Wind',
        'description': '风吹过树叶的声音',
        'base_noise': 'brown',
        'amplitude': 0.4,
        'modulation': 0.3,
        'modulation_freq': 0.1,
    },
    'fireplace': {
        'name': '壁炉',
        'name_en': 'Fireplace',
        'description': '柴火噼啪燃烧声',
        'base_noise': 'brown',
        'amplitude': 0.35,
        'modulation': 0.15,
        'modulation_freq': 0.4,
    },
    'waterfall': {
        'name': '瀑布',
        'name_en': 'Waterfall',
        'description': '持续的水流声',
        'base_noise': 'brown',
        'amplitude': 0.55,
        'modulation': 0.1,
        'modulation_freq': 0.05,
    },
    'stream': {
        'name': '溪流',
        'name_en': 'Stream',
        'description': '轻缓的溪水流动声',
        'base_noise': 'pink',
        'amplitude': 0.35,
        'modulation': 0.12,
        'modulation_freq': 0.2,
    },
    'night_ambience': {
        'name': '夜晚',
        'name_en': 'Night Ambience',
        'description': '宁静的夜晚环境音',
        'base_noise': 'brown',
        'amplitude': 0.25,
        'modulation': 0.08,
        'modulation_freq': 0.05,
    },
    'cafe': {
        'name': '咖啡馆',
        'name_en': 'Cafe',
        'description': '咖啡馆环境嗡嗡声',
        'base_noise': 'pink',
        'amplitude': 0.3,
        'modulation': 0.2,
        'modulation_freq': 0.3,
    },
    'airplane': {
        'name': '飞机客舱',
        'name_en': 'Airplane Cabin',
        'description': '飞机飞行时的低频嗡嗡声',
        'base_noise': 'brown',
        'amplitude': 0.4,
        'modulation': 0.05,
        'modulation_freq': 0.02,
    },
}


# ============================================================================
# Enums
# ============================================================================

class NoiseType(Enum):
    """噪音类型枚举"""
    WHITE = 'white'
    PINK = 'pink'
    BROWN = 'brown'
    BLUE = 'blue'
    VIOLET = 'violet'
    GREY = 'grey'


class AmbientType(Enum):
    """环境音类型枚举"""
    LIGHT_RAIN = 'light_rain'
    HEAVY_RAIN = 'heavy_rain'
    THUNDERSTORM = 'thunderstorm'
    OCEAN_WAVES = 'ocean_waves'
    FOREST = 'forest'
    WIND = 'wind'
    FIREPLACE = 'fireplace'
    WATERFALL = 'waterfall'
    STREAM = 'stream'
    NIGHT_AMBIENCE = 'night_ambience'
    CAFE = 'cafe'
    AIRPLANE = 'airplane'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class AudioConfig:
    """音频配置"""
    sample_rate: int = DEFAULT_SAMPLE_RATE
    bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE
    num_channels: int = DEFAULT_NUM_CHANNELS
    
    @property
    def max_amplitude(self) -> int:
        """获取最大振幅值"""
        return (2 ** (self.bits_per_sample - 1)) - 1
    
    @property
    def byte_rate(self) -> int:
        """字节率"""
        return self.sample_rate * self.num_channels * (self.bits_per_sample // 8)
    
    @property
    def block_align(self) -> int:
        """块对齐"""
        return self.num_channels * (self.bits_per_sample // 8)


@dataclass
class NoiseProfile:
    """噪音配置文件"""
    noise_type: str
    name: str
    name_en: str
    description: str
    amplitude: float  # 0.0 - 1.0
    sample_rate: int = DEFAULT_SAMPLE_RATE
    duration_seconds: float = 10.0


@dataclass
class MixedNoiseConfig:
    """混合噪音配置"""
    layers: List[Tuple[str, float]]  # [(noise_type, amplitude), ...]
    crossfade_seconds: float = 0.5
    sample_rate: int = DEFAULT_SAMPLE_RATE


# ============================================================================
# Core Noise Generation Functions
# ============================================================================

def generate_white_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成白噪音样本.
    
    白噪音在所有频率上具有相等的能量密度，听起来像静电声。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子（用于可重复生成）
    
    Returns:
        白噪音样本列表 (-1.0 到 1.0)
    
    Examples:
        >>> samples = generate_white_noise(44100, 0.5)
        >>> len(samples)
        44100
        >>> all(-0.5 <= s <= 0.5 for s in samples)
        True
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # 白噪音：均匀分布的随机值
    samples = [random.uniform(-1, 1) * amplitude for _ in range(num_samples)]
    
    return samples


def generate_pink_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成粉噪音样本.
    
    粉噪音每倍频程能量减半（-3dB/octave），听起来更自然，
    类似雨声或树叶沙沙声。
    
    使用 Paul Kellet 的算法实现。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        粉噪音样本列表
    
    Examples:
        >>> samples = generate_pink_noise(44100, 0.5)
        >>> len(samples)
        44100
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # Paul Kellet 的粉噪音算法
    b0 = b1 = b2 = b3 = b4 = b5 = b6 = 0.0
    samples = []
    
    for _ in range(num_samples):
        white = random.uniform(-1, 1)
        
        b0 = 0.99886 * b0 + white * 0.0555179
        b1 = 0.99332 * b1 + white * 0.0750759
        b2 = 0.96900 * b2 + white * 0.1538520
        b3 = 0.86650 * b3 + white * 0.3104856
        b4 = 0.55000 * b4 + white * 0.5329522
        b5 = -0.7616 * b5 - white * 0.0168980
        
        pink = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11
        b6 = white * 0.115926
        
        samples.append(pink * amplitude)
    
    # 归一化以防止削波
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0:
        samples = [s / max_val * amplitude for s in samples]
    
    return samples


def generate_brown_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成棕色噪音样本（布朗噪音/红噪音）.
    
    棕色噪音每倍频程能量减少6dB（-6dB/octave），
    听起来低沉，类似瀑布或远处的雷声。
    
    通过积分白噪音生成。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        棕色噪音样本列表
    
    Examples:
        >>> samples = generate_brown_noise(44100, 0.5)
        >>> len(samples)
        44100
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # 棕色噪音：白噪音的积分
    samples = []
    last = 0.0
    
    for _ in range(num_samples):
        white = random.uniform(-1, 1)
        # 积分白噪音，但添加衰减防止发散
        brown = (last + white * 0.02) * 0.999
        last = brown
        samples.append(brown)
    
    # 归一化
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0:
        samples = [s / max_val * amplitude for s in samples]
    
    return samples


def generate_blue_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成蓝噪音样本.
    
    蓝噪音每倍频程能量增加3dB（+3dB/octave），
    听起来比白噪音更尖锐，能量集中在高频。
    
    通过微分白噪音生成。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        蓝噪音样本列表
    
    Examples:
        >>> samples = generate_blue_noise(44100, 0.5)
        >>> len(samples)
        44100
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # 蓝噪音：白噪音的微分
    samples = []
    last = 0.0
    
    for _ in range(num_samples):
        white = random.uniform(-1, 1)
        blue = white - last  # 微分
        last = white
        samples.append(blue)
    
    # 归一化
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0:
        samples = [s / max_val * amplitude for s in samples]
    
    return samples


def generate_violet_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成紫噪音样本.
    
    紫噪音每倍频程能量增加6dB（+6dB/octave），
    能量高度集中在高频，声音非常尖锐。
    
    通过双重微分白噪音生成。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        紫噪音样本列表
    
    Examples:
        >>> samples = generate_violet_noise(44100, 0.5)
        >>> len(samples)
        44100
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # 紫噪音：白噪音的双重微分
    samples = []
    last1 = 0.0
    last2 = 0.0
    
    for _ in range(num_samples):
        white = random.uniform(-1, 1)
        blue = white - last1
        violet = blue - last2  # 第二次微分
        last2 = blue
        last1 = white
        samples.append(violet)
    
    # 归一化
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0:
        samples = [s / max_val * amplitude for s in samples]
    
    return samples


def generate_grey_noise(
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成灰噪音样本.
    
    灰噪音经过心理声学补偿，使人耳感觉所有频率响度相等。
    实际上是经过 A-weighting 滤波的粉噪音。
    
    Args:
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        灰噪音样本列表
    
    Examples:
        >>> samples = generate_grey_noise(44100, 0.5)
        >>> len(samples)
        44100
    """
    if seed is not None:
        random.seed(seed)
    
    amplitude = max(0.0, min(1.0, amplitude))
    
    # 灰噪音：粉噪音 + 高频提升（简化版 A-weighting 补偿）
    pink = generate_pink_noise(num_samples, 1.0, seed)
    
    # 简化的高频提升
    samples = []
    prev = 0.0
    
    for i, p in enumerate(pink):
        # 添加轻微的高频成分
        high = p - prev
        prev = p
        # 混合粉噪音和高频成分
        grey = p * 0.7 + high * 0.3
        samples.append(grey)
    
    # 归一化
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0:
        samples = [s / max_val * amplitude for s in samples]
    
    return samples


def generate_noise(
    noise_type: str,
    num_samples: int,
    amplitude: float = 1.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    根据类型生成噪音样本.
    
    Args:
        noise_type: 噪音类型 ('white', 'pink', 'brown', 'blue', 'violet', 'grey')
        num_samples: 样本数量
        amplitude: 振幅 (0.0 - 1.0)
        seed: 随机种子
    
    Returns:
        噪音样本列表
    
    Raises:
        ValueError: 无效的噪音类型
    
    Examples:
        >>> samples = generate_noise('pink', 44100, 0.5)
        >>> len(samples)
        44100
    """
    generators = {
        'white': generate_white_noise,
        'pink': generate_pink_noise,
        'brown': generate_brown_noise,
        'blue': generate_blue_noise,
        'violet': generate_violet_noise,
        'grey': generate_grey_noise,
    }
    
    noise_type_lower = noise_type.lower()
    if noise_type_lower not in generators:
        raise ValueError(
            f"无效的噪音类型: {noise_type}. "
            f"有效类型: {', '.join(generators.keys())}"
        )
    
    return generators[noise_type_lower](num_samples, amplitude, seed)


# ============================================================================
# Ambient Sound Generation Functions
# ============================================================================

def generate_ambient_sound(
    ambient_type: str,
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    amplitude_override: Optional[float] = None,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成环境声音.
    
    Args:
        ambient_type: 环境音类型（见 AMBIENT_PRESETS）
        duration_seconds: 时长（秒）
        sample_rate: 采样率
        amplitude_override: 覆盖预设振幅
        seed: 随机种子
    
    Returns:
        环境音样本列表
    
    Raises:
        ValueError: 无效的环境音类型
    
    Examples:
        >>> samples = generate_ambient_sound('light_rain', 5.0)
        >>> len(samples)
        220500  # 5 * 44100
    """
    ambient_type_lower = ambient_type.lower()
    if ambient_type_lower not in AMBIENT_PRESETS:
        raise ValueError(
            f"无效的环境音类型: {ambient_type}. "
            f"有效类型: {', '.join(AMBIENT_PRESETS.keys())}"
        )
    
    preset = AMBIENT_PRESETS[ambient_type_lower]
    num_samples = int(duration_seconds * sample_rate)
    
    amplitude = amplitude_override if amplitude_override is not None else preset['amplitude']
    
    # 生成基础噪音
    base_noise = generate_noise(
        preset['base_noise'],
        num_samples,
        amplitude,
        seed
    )
    
    # 添加调制（模拟自然变化）
    modulation = preset['modulation']
    mod_freq = preset['modulation_freq']
    
    if modulation > 0 and mod_freq > 0:
        samples = []
        for i, sample in enumerate(base_noise):
            # 低频正弦调制
            t = i / sample_rate
            mod_factor = 1.0 + modulation * math.sin(2 * math.pi * mod_freq * t)
            samples.append(sample * mod_factor)
        base_noise = samples
    
    # 最终归一化
    max_val = max(abs(s) for s in base_noise) if base_noise else 1.0
    if max_val > 0:
        base_noise = [s / max_val * amplitude for s in base_noise]
    
    return base_noise


def generate_rain_sound(
    duration_seconds: float,
    intensity: str = 'medium',
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成雨声.
    
    Args:
        duration_seconds: 时长（秒）
        intensity: 强度 ('light', 'medium', 'heavy')
        sample_rate: 采样率
        seed: 随机种子
    
    Returns:
        雨声样本列表
    
    Examples:
        >>> samples = generate_rain_sound(10.0, 'heavy')
        >>> len(samples)
        441000
    """
    intensity_map = {
        'light': ('light_rain', None),
        'medium': ('heavy_rain', 0.5),
        'heavy': ('heavy_rain', None),
    }
    
    preset_name, amp_override = intensity_map.get(intensity, ('heavy_rain', None))
    return generate_ambient_sound(preset_name, duration_seconds, sample_rate, amp_override, seed)


def generate_ocean_sound(
    duration_seconds: float,
    wave_intensity: str = 'medium',
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成海浪声.
    
    Args:
        duration_seconds: 时长（秒）
        wave_intensity: 浪强度 ('calm', 'medium', 'rough')
        sample_rate: 采样率
        seed: 随机种子
    
    Returns:
        海浪声样本列表
    
    Examples:
        >>> samples = generate_ocean_sound(30.0, 'calm')
        >>> len(samples)
        1323000
    """
    intensity_map = {
        'calm': 0.3,
        'medium': 0.45,
        'rough': 0.6,
    }
    
    amplitude = intensity_map.get(wave_intensity, 0.45)
    return generate_ambient_sound('ocean_waves', duration_seconds, sample_rate, amplitude, seed)


def generate_wind_sound(
    duration_seconds: float,
    strength: str = 'moderate',
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成风声.
    
    Args:
        duration_seconds: 时长（秒）
        strength: 风强度 ('light', 'moderate', 'strong')
        sample_rate: 采样率
        seed: 随机种子
    
    Returns:
        风声样本列表
    
    Examples:
        >>> samples = generate_wind_sound(15.0, 'light')
        >>> len(samples)
        661500
    """
    intensity_map = {
        'light': 0.25,
        'moderate': 0.4,
        'strong': 0.55,
    }
    
    amplitude = intensity_map.get(strength, 0.4)
    return generate_ambient_sound('wind', duration_seconds, sample_rate, amplitude, seed)


def generate_fire_sound(
    duration_seconds: float,
    crackling: bool = True,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: Optional[int] = None
) -> List[float]:
    """
    生成火焰声.
    
    Args:
        duration_seconds: 时长（秒）
        crackling: 是否添加噼啪声
        sample_rate: 采样率
        seed: 随机种子
    
    Returns:
        火焰声样本列表
    
    Examples:
        >>> samples = generate_fire_sound(20.0, crackling=True)
        >>> len(samples)
        882000
    """
    if seed is not None:
        random.seed(seed)
    
    base = generate_ambient_sound('fireplace', duration_seconds, sample_rate)
    
    if crackling:
        # 添加随机噼啪声
        num_samples = len(base)
        num_crackles = int(duration_seconds * 3)  # 每秒约3个噼啪声
        
        for _ in range(num_crackles):
            pos = random.randint(0, num_samples - 1)
            crackle_len = random.randint(100, 500)
            crackle_amp = random.uniform(0.1, 0.3)
            
            for i in range(min(crackle_len, num_samples - pos)):
                decay = math.exp(-i / 100)
                base[pos + i] += crackle_amp * decay * random.uniform(-1, 1)
    
    # 归一化
    max_val = max(abs(s) for s in base) if base else 1.0
    if max_val > 0:
        base = [s / max_val * 0.35 for s in base]
    
    return base


# ============================================================================
# Noise Mixing Functions
# ============================================================================

def mix_noises(
    noise_configs: List[Tuple[str, float]],
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    crossfade_seconds: float = 0.0,
    seed: Optional[int] = None
) -> List[float]:
    """
    混合多种噪音.
    
    Args:
        noise_configs: 噪音配置列表 [(噪音类型, 振幅), ...]
        duration_seconds: 时长（秒）
        sample_rate: 采样率
        crossfade_seconds: 交叉淡化时长（秒）
        seed: 随机种子
    
    Returns:
        混合后的样本列表
    
    Examples:
        >>> samples = mix_noises([('pink', 0.5), ('brown', 0.3)], 10.0)
        >>> len(samples)
        441000
    """
    num_samples = int(duration_seconds * sample_rate)
    mixed = [0.0] * num_samples
    
    for i, (noise_type, amplitude) in enumerate(noise_configs):
        # 使用不同的种子生成每种噪音
        noise_seed = seed + i if seed is not None else None
        noise = generate_noise(noise_type, num_samples, amplitude, noise_seed)
        
        # 叠加噪音
        for j in range(num_samples):
            mixed[j] += noise[j]
    
    # 归一化防止削波
    max_val = max(abs(s) for s in mixed) if mixed else 1.0
    if max_val > 1.0:
        mixed = [s / max_val for s in mixed]
    
    return mixed


def layer_ambient_sounds(
    layers: List[Tuple[str, float]],
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: Optional[int] = None
) -> List[float]:
    """
    叠加多层环境音.
    
    Args:
        layers: 环境音层配置 [(环境音类型, 振幅), ...]
        duration_seconds: 时长（秒）
        sample_rate: 采样率
        seed: 随机种子
    
    Returns:
        混合后的样本列表
    
    Examples:
        >>> samples = layer_ambient_sounds([('rain', 0.5), ('fire', 0.3)], 30.0)
        >>> len(samples)
        1323000
    """
    num_samples = int(duration_seconds * sample_rate)
    mixed = [0.0] * num_samples
    
    for i, (ambient_type, amplitude) in enumerate(layers):
        ambient_seed = seed + i if seed is not None else None
        ambient = generate_ambient_sound(ambient_type, duration_seconds, sample_rate, amplitude, ambient_seed)
        
        for j in range(num_samples):
            mixed[j] += ambient[j]
    
    # 归一化
    max_val = max(abs(s) for s in mixed) if mixed else 1.0
    if max_val > 1.0:
        mixed = [s / max_val for s in mixed]
    
    return mixed


def apply_fade(
    samples: List[float],
    fade_in_seconds: float = 0.0,
    fade_out_seconds: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    应用淡入淡出效果.
    
    Args:
        samples: 音频样本
        fade_in_seconds: 淡入时长（秒）
        fade_out_seconds: 淡出时长（秒）
        sample_rate: 采样率
    
    Returns:
        应用淡入淡出后的样本
    
    Examples:
        >>> samples = generate_white_noise(44100)
        >>> faded = apply_fade(samples, 1.0, 2.0)
    """
    samples = samples.copy()
    num_samples = len(samples)
    
    fade_in_samples = int(fade_in_seconds * sample_rate)
    fade_out_samples = int(fade_out_seconds * sample_rate)
    
    # 淡入
    if fade_in_samples > 0:
        for i in range(min(fade_in_samples, num_samples)):
            fade_factor = i / fade_in_samples
            # 使用余弦曲线更平滑
            fade_factor = (1 - math.cos(fade_factor * math.pi)) / 2
            samples[i] *= fade_factor
    
    # 淡出
    if fade_out_samples > 0:
        start = max(0, num_samples - fade_out_samples)
        for i in range(start, num_samples):
            fade_factor = (num_samples - i) / fade_out_samples
            # 使用余弦曲线
            fade_factor = (1 - math.cos(fade_factor * math.pi)) / 2
            samples[i] *= fade_factor
    
    return samples


def apply_volume(
    samples: List[float],
    volume: float
) -> List[float]:
    """
    调整音量.
    
    Args:
        samples: 音频样本
        volume: 音量倍数 (1.0 = 100%, 0.5 = 50%, 2.0 = 200%)
    
    Returns:
        调整音量后的样本
    
    Examples:
        >>> samples = generate_pink_noise(44100)
        >>> quieter = apply_volume(samples, 0.5)
    """
    return [s * volume for s in samples]


# ============================================================================
# WAV File Functions
# ============================================================================

def samples_to_wav_bytes(
    samples: List[float],
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE,
    num_channels: int = DEFAULT_NUM_CHANNELS
) -> bytes:
    """
    将音频样本转换为 WAV 格式字节.
    
    Args:
        samples: 音频样本列表 (-1.0 到 1.0)
        sample_rate: 采样率
        bits_per_sample: 位深度 (8, 16, 24, 32)
        num_channels: 声道数
    
    Returns:
        WAV 格式的字节数据
    
    Examples:
        >>> samples = generate_pink_noise(44100)
        >>> wav_data = samples_to_wav_bytes(samples)
        >>> len(wav_data) > 44  # WAV header is 44 bytes
        True
    """
    # 确定格式
    if bits_per_sample == 8:
        fmt_code = 1  # PCM
        max_val = 127
    elif bits_per_sample == 16:
        fmt_code = 1
        max_val = 32767
    elif bits_per_sample == 24:
        fmt_code = 1
        max_val = 8388607
    elif bits_per_sample == 32:
        fmt_code = 1
        max_val = 2147483647
    else:
        raise ValueError(f"不支持的位深度: {bits_per_sample}")
    
    # 字节率
    byte_rate = sample_rate * num_channels * (bits_per_sample // 8)
    block_align = num_channels * (bits_per_sample // 8)
    
    # 转换样本
    sample_data = bytearray()
    for sample in samples:
        # 归一化并转换
        val = int(max(-1.0, min(1.0, sample)) * max_val)
        
        if bits_per_sample == 8:
            sample_data.append((val + 128) & 0xFF)
        elif bits_per_sample == 16:
            sample_data.extend(struct.pack('<h', val))
        elif bits_per_sample == 24:
            # 24-bit little-endian
            sample_data.append(val & 0xFF)
            sample_data.append((val >> 8) & 0xFF)
            sample_data.append((val >> 16) & 0xFF)
        elif bits_per_sample == 32:
            sample_data.extend(struct.pack('<i', val))
    
    # 如果是多声道，复制数据
    if num_channels > 1:
        mono_data = bytes(sample_data)
        sample_data = bytearray()
        bytes_per_sample = bits_per_sample // 8
        for i in range(0, len(mono_data), bytes_per_sample):
            sample_bytes = mono_data[i:i+bytes_per_sample]
            for _ in range(num_channels):
                sample_data.extend(sample_bytes)
    
    data_size = len(sample_data)
    
    # 构建 WAV 文件头
    header = bytearray()
    
    # RIFF header
    header.extend(b'RIFF')
    header.extend(struct.pack('<I', 36 + data_size))  # File size - 8
    header.extend(b'WAVE')
    
    # fmt chunk
    header.extend(b'fmt ')
    header.extend(struct.pack('<I', 16))  # Chunk size
    header.extend(struct.pack('<H', fmt_code))  # Audio format (1 = PCM)
    header.extend(struct.pack('<H', num_channels))
    header.extend(struct.pack('<I', sample_rate))
    header.extend(struct.pack('<I', byte_rate))
    header.extend(struct.pack('<H', block_align))
    header.extend(struct.pack('<H', bits_per_sample))
    
    # data chunk
    header.extend(b'data')
    header.extend(struct.pack('<I', data_size))
    
    return bytes(header) + bytes(sample_data)


def save_wav_file(
    samples: List[float],
    filepath: str,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE,
    num_channels: int = DEFAULT_NUM_CHANNELS
) -> int:
    """
    保存音频样本为 WAV 文件.
    
    Args:
        samples: 音频样本列表
        filepath: 文件路径
        sample_rate: 采样率
        bits_per_sample: 位深度
        num_channels: 声道数
    
    Returns:
        写入的字节数
    
    Examples:
        >>> samples = generate_pink_noise(44100)
        >>> save_wav_file(samples, 'noise.wav')
        88244
    """
    wav_data = samples_to_wav_bytes(samples, sample_rate, bits_per_sample, num_channels)
    
    with open(filepath, 'wb') as f:
        f.write(wav_data)
    
    return len(wav_data)


def load_wav_file(filepath: str) -> Tuple[List[float], int, int, int]:
    """
    从 WAV 文件加载音频样本.
    
    Args:
        filepath: 文件路径
    
    Returns:
        (样本列表, 采样率, 位深度, 声道数)
    
    Raises:
        ValueError: 文件格式无效
    
    Examples:
        >>> samples, sr, bits, ch = load_wav_file('noise.wav')
        >>> sr
        44100
    """
    with open(filepath, 'rb') as f:
        # 读取 RIFF header
        riff = f.read(4)
        if riff != b'RIFF':
            raise ValueError("无效的 WAV 文件：缺少 RIFF 标识")
        
        file_size = struct.unpack('<I', f.read(4))[0]
        wave = f.read(4)
        if wave != b'WAVE':
            raise ValueError("无效的 WAV 文件：缺少 WAVE 标识")
        
        # 读取 fmt chunk
        sample_rate = 0
        bits_per_sample = 0
        num_channels = 0
        
        while True:
            chunk_id = f.read(4)
            if len(chunk_id) < 4:
                break
            
            chunk_size = struct.unpack('<I', f.read(4))[0]
            
            if chunk_id == b'fmt ':
                fmt_code = struct.unpack('<H', f.read(2))[0]
                num_channels = struct.unpack('<H', f.read(2))[0]
                sample_rate = struct.unpack('<I', f.read(4))[0]
                byte_rate = struct.unpack('<I', f.read(4))[0]
                block_align = struct.unpack('<H', f.read(2))[0]
                bits_per_sample = struct.unpack('<H', f.read(2))[0]
                
                # 跳过剩余的 fmt 数据
                if chunk_size > 16:
                    f.read(chunk_size - 16)
            
            elif chunk_id == b'data':
                # 读取音频数据
                data = f.read(chunk_size)
                
                # 转换为样本
                samples = []
                bytes_per_sample = bits_per_sample // 8
                
                if bits_per_sample == 8:
                    max_val = 127
                    for byte in data:
                        samples.append((byte - 128) / max_val)
                
                elif bits_per_sample == 16:
                    max_val = 32767
                    for i in range(0, len(data), 2):
                        if i + 2 <= len(data):
                            val = struct.unpack('<h', data[i:i+2])[0]
                            samples.append(val / max_val)
                
                elif bits_per_sample == 24:
                    max_val = 8388607
                    for i in range(0, len(data), 3):
                        if i + 3 <= len(data):
                            val = data[i] | (data[i+1] << 8) | (data[i+2] << 16)
                            if val >= 0x800000:
                                val -= 0x1000000
                            samples.append(val / max_val)
                
                elif bits_per_sample == 32:
                    max_val = 2147483647
                    for i in range(0, len(data), 4):
                        if i + 4 <= len(data):
                            val = struct.unpack('<i', data[i:i+4])[0]
                            samples.append(val / max_val)
                
                # 如果是多声道，取第一个声道
                if num_channels > 1:
                    samples = samples[::num_channels]
                
                return samples, sample_rate, bits_per_sample, num_channels
            
            else:
                # 跳过其他 chunk
                f.read(chunk_size)
    
    raise ValueError("无效的 WAV 文件：缺少 data chunk")


# ============================================================================
# Utility Functions
# ============================================================================

def get_noise_info(noise_type: str) -> dict:
    """
    获取噪音类型信息.
    
    Args:
        noise_type: 噪音类型
    
    Returns:
        噪音信息字典
    
    Examples:
        >>> info = get_noise_info('pink')
        >>> info['description']
        '粉噪音 - 每倍频程能量减半，类似雨声'
    """
    noise_type_lower = noise_type.lower()
    return {
        'type': noise_type_lower,
        'description': NOISE_DESCRIPTIONS.get(noise_type_lower, '未知类型'),
    }


def get_ambient_info(ambient_type: str) -> dict:
    """
    获取环境音类型信息.
    
    Args:
        ambient_type: 环境音类型
    
    Returns:
        环境音信息字典
    
    Examples:
        >>> info = get_ambient_info('light_rain')
        >>> info['name']
        '小雨'
    """
    ambient_type_lower = ambient_type.lower()
    preset = AMBIENT_PRESETS.get(ambient_type_lower, {})
    return {
        'type': ambient_type_lower,
        'name': preset.get('name', '未知'),
        'name_en': preset.get('name_en', 'Unknown'),
        'description': preset.get('description', ''),
        'base_noise': preset.get('base_noise', ''),
        'amplitude': preset.get('amplitude', 0.5),
    }


def list_noise_types() -> List[str]:
    """
    列出所有噪音类型.
    
    Returns:
        噪音类型列表
    
    Examples:
        >>> types = list_noise_types()
        >>> 'pink' in types
        True
    """
    return list(NOISE_DESCRIPTIONS.keys())


def list_ambient_types() -> List[str]:
    """
    列出所有环境音类型.
    
    Returns:
        环境音类型列表
    
    Examples:
        >>> types = list_ambient_types()
        >>> 'light_rain' in types
        True
    """
    return list(AMBIENT_PRESETS.keys())


def calculate_duration(
    num_samples: int,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> float:
    """
    根据样本数计算时长.
    
    Args:
        num_samples: 样本数量
        sample_rate: 采样率
    
    Returns:
        时长（秒）
    
    Examples:
        >>> calculate_duration(44100)
        1.0
        >>> calculate_duration(88200, 44100)
        2.0
    """
    return num_samples / sample_rate


def calculate_num_samples(
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> int:
    """
    根据时长计算样本数.
    
    Args:
        duration_seconds: 时长（秒）
        sample_rate: 采样率
    
    Returns:
        样本数量
    
    Examples:
        >>> calculate_num_samples(1.0)
        44100
        >>> calculate_num_samples(2.5, 44100)
        110250
    """
    return int(duration_seconds * sample_rate)


def estimate_file_size(
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE,
    num_channels: int = DEFAULT_NUM_CHANNELS
) -> int:
    """
    估算 WAV 文件大小.
    
    Args:
        duration_seconds: 时长（秒）
        sample_rate: 采样率
        bits_per_sample: 位深度
        num_channels: 声道数
    
    Returns:
        文件大小（字节）
    
    Examples:
        >>> estimate_file_size(10.0)
        882044  # ~861 KB
    """
    num_samples = int(duration_seconds * sample_rate)
    data_size = num_samples * num_channels * (bits_per_sample // 8)
    return 44 + data_size  # 44 bytes header + data


def format_duration(seconds: float) -> str:
    """
    格式化时长显示.
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化的时长字符串
    
    Examples:
        >>> format_duration(65.5)
        '1:05.5'
        >>> format_duration(3661.25)
        '1:01:01.2'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:04.1f}"
    else:
        return f"{minutes}:{secs:04.1f}"


def format_file_size(bytes_size: int) -> str:
    """
    格式化文件大小显示.
    
    Args:
        bytes_size: 字节数
    
    Returns:
        格式化的文件大小字符串
    
    Examples:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1536000)
        '1.5 MB'
    """
    units = ['B', 'KB', 'MB', 'GB']
    size = float(bytes_size)
    
    for unit in units[:-1]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    
    return f"{size:.1f} {units[-1]}"


# ============================================================================
# High-Level Generator Class
# ============================================================================

class AmbientNoiseGenerator:
    """环境噪音生成器类"""
    
    def __init__(
        self,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE,
        num_channels: int = DEFAULT_NUM_CHANNELS
    ):
        """
        初始化噪音生成器.
        
        Args:
            sample_rate: 采样率
            bits_per_sample: 位深度
            num_channels: 声道数
        """
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        self.num_channels = num_channels
        self._samples: List[float] = []
        self._seed: Optional[int] = None
    
    @property
    def duration(self) -> float:
        """当前时长（秒）"""
        return len(self._samples) / self.sample_rate
    
    @property
    def num_samples(self) -> int:
        """当前样本数"""
        return len(self._samples)
    
    def set_seed(self, seed: int) -> 'AmbientNoiseGenerator':
        """设置随机种子"""
        self._seed = seed
        return self
    
    def add_noise(
        self,
        noise_type: str,
        duration_seconds: float,
        amplitude: float = 1.0
    ) -> 'AmbientNoiseGenerator':
        """添加噪音层"""
        num_samples = int(duration_seconds * self.sample_rate)
        noise = generate_noise(noise_type, num_samples, amplitude, self._seed)
        
        # 如果已有样本，叠加；否则直接赋值
        if self._samples:
            for i in range(min(len(self._samples), len(noise))):
                self._samples[i] += noise[i]
            # 如果新噪音更长，追加
            if len(noise) > len(self._samples):
                self._samples.extend(noise[len(self._samples):])
        else:
            self._samples = noise
        
        return self
    
    def add_ambient(
        self,
        ambient_type: str,
        duration_seconds: float,
        amplitude: Optional[float] = None
    ) -> 'AmbientNoiseGenerator':
        """添加环境音层"""
        num_samples = int(duration_seconds * self.sample_rate)
        ambient = generate_ambient_sound(
            ambient_type, duration_seconds, self.sample_rate, amplitude, self._seed
        )
        
        if self._samples:
            for i in range(min(len(self._samples), len(ambient))):
                self._samples[i] += ambient[i]
            if len(ambient) > len(self._samples):
                self._samples.extend(ambient[len(self._samples):])
        else:
            self._samples = ambient
        
        return self
    
    def apply_fade(
        self,
        fade_in_seconds: float = 1.0,
        fade_out_seconds: float = 1.0
    ) -> 'AmbientNoiseGenerator':
        """应用淡入淡出"""
        self._samples = apply_fade(
            self._samples, fade_in_seconds, fade_out_seconds, self.sample_rate
        )
        return self
    
    def normalize(self) -> 'AmbientNoiseGenerator':
        """归一化音量"""
        max_val = max(abs(s) for s in self._samples) if self._samples else 1.0
        if max_val > 0:
            self._samples = [s / max_val for s in self._samples]
        return self
    
    def set_volume(self, volume: float) -> 'AmbientNoiseGenerator':
        """设置音量"""
        self._samples = apply_volume(self._samples, volume)
        return self
    
    def get_samples(self) -> List[float]:
        """获取样本"""
        return self._samples.copy()
    
    def to_wav_bytes(self) -> bytes:
        """转换为 WAV 字节数据"""
        return samples_to_wav_bytes(
            self._samples, self.sample_rate, self.bits_per_sample, self.num_channels
        )
    
    def save_wav(self, filepath: str) -> int:
        """保存为 WAV 文件"""
        return save_wav_file(
            self._samples, filepath, self.sample_rate, self.bits_per_sample, self.num_channels
        )
    
    def clear(self) -> 'AmbientNoiseGenerator':
        """清空当前样本"""
        self._samples = []
        return self
    
    def info(self) -> dict:
        """获取生成器信息"""
        return {
            'sample_rate': self.sample_rate,
            'bits_per_sample': self.bits_per_sample,
            'num_channels': self.num_channels,
            'duration': round(self.duration, 2),
            'num_samples': self.num_samples,
            'file_size': estimate_file_size(
                self.duration, self.sample_rate, self.bits_per_sample, self.num_channels
            ),
        }


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Ambient Noise Generator Demo")
    print("=" * 60)
    
    # 生成各种噪音示例
    print("\n--- 噪音类型演示 ---")
    duration = 3.0
    
    for noise_type in ['white', 'pink', 'brown', 'blue']:
        info = get_noise_info(noise_type)
        print(f"\n{noise_type.upper()}: {info['description']}")
        samples = generate_noise(noise_type, int(duration * DEFAULT_SAMPLE_RATE), 0.5, seed=42)
        print(f"  生成 {duration} 秒样本，共 {len(samples)} 个采样点")
    
    # 环境音演示
    print("\n--- 环境音演示 ---")
    for ambient_type in ['light_rain', 'ocean_waves', 'wind']:
        info = get_ambient_info(ambient_type)
        print(f"\n{info['name']} ({info['name_en']}): {info['description']}")
        samples = generate_ambient_sound(ambient_type, duration, seed=42)
        print(f"  生成 {duration} 秒样本")
    
    # 混合噪音演示
    print("\n--- 混合噪音演示 ---")
    print("混合粉噪音和棕色噪音...")
    mixed = mix_noises([('pink', 0.4), ('brown', 0.3)], duration, seed=42)
    print(f"  混合后样本数: {len(mixed)}")
    
    # 使用生成器类
    print("\n--- 使用生成器类 ---")
    generator = (
        AmbientNoiseGenerator()
        .set_seed(42)
        .add_ambient('light_rain', 5.0, 0.5)
        .add_ambient('fireplace', 5.0, 0.3)
        .normalize()
        .apply_fade(0.5, 1.0)
    )
    
    print(f"生成器信息: {generator.info()}")
    
    # 文件大小估算
    print("\n--- 文件大小估算 ---")
    for dur in [10, 30, 60, 300]:
        size = estimate_file_size(dur)
        print(f"  {dur} 秒音频 ≈ {format_file_size(size)}")
    
    # 导出文件
    print("\n--- 导出示例 ---")
    sample_noise = generate_pink_noise(int(5 * DEFAULT_SAMPLE_RATE), 0.5, seed=42)
    sample_noise = apply_fade(sample_noise, 1.0, 1.0)
    print(f"示例: 5秒粉噪音，带1秒淡入淡出")
    print(f"  预计文件大小: {format_file_size(estimate_file_size(5.0))}")
    
    print("\n" + "=" * 60)