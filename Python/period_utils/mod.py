#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Period Utilities
=============================
A comprehensive periodic pattern generation and calculation module with zero external dependencies.

Features:
    - Periodic sequence generation (sine, square, sawtooth, triangle waves)
    - BPM to milliseconds conversion and vice versa
    - Heartbeat pattern generation
    - Rhythm pattern analysis and generation
    - Frequency to period conversion
    - Musical timing calculations
    - Oscillator pattern generators
    - LFO (Low Frequency Oscillator) patterns
    - Custom waveform builders

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-29
"""

import math
from typing import List, Tuple, Optional, Callable, Dict, Union
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants
# ============================================================================

# Standard musical BPM ranges
BPM_MIN = 20
BPM_MAX = 300

# Standard sample rate for audio generation
DEFAULT_SAMPLE_RATE = 44100

# Musical note frequencies (A4 = 440Hz)
NOTE_FREQUENCIES = {
    'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.60,
    'F0': 21.83, 'F#0': 23.12, 'G0': 24.50, 'G#0': 25.96, 'A0': 27.50,
    'A#0': 29.14, 'B0': 30.87,
    'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20,
    'F1': 43.65, 'F#1': 46.25, 'G1': 49.00, 'G#1': 51.91, 'A1': 55.00,
    'A#1': 58.27, 'B1': 61.74,
    'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41,
    'F2': 87.31, 'F#2': 92.50, 'G2': 98.00, 'G#2': 103.83, 'A2': 110.00,
    'A#2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81,
    'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00,
    'A#3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,
    'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,
    'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25,
    'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00,
    'A#5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51,
    'F6': 1396.91, 'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.00,
    'A#6': 1864.66, 'B6': 1975.53,
    'C7': 2093.00, 'C#7': 2217.46, 'D7': 2349.32, 'D#7': 2489.02, 'E7': 2637.02,
    'F7': 2793.83, 'F#7': 2959.96, 'G7': 3135.96, 'G#7': 3322.44, 'A7': 3520.00,
    'A#7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01, 'C#8': 4434.92, 'D8': 4698.63, 'D#8': 4978.03, 'E8': 5274.04,
    'F8': 5587.65, 'F#8': 5919.91, 'G8': 6271.93, 'G#8': 6644.88, 'A8': 7040.00,
    'A#8': 7458.62, 'B8': 7902.13,
}

# Standard rhythm patterns (1 = note, 0 = rest, . = subdivision)
RHYTHM_PATTERNS = {
    'straight_4': [1, 0, 1, 0],
    'straight_8': [1, 0, 1, 0, 1, 0, 1, 0],
    'straight_16': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    'swing_8': [1, 0.5, 0, 0.5, 1, 0.5, 0, 0.5],
    'waltz': [1, 0, 0],
    'bossa_nova': [1, 0, 0, 1, 0, 0, 1, 0],
    'clave': [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    'syncopated': [0, 1, 0, 0, 1, 0, 0, 1],
    'heartbeat': [1, 0, 0.7, 0, 0, 0, 0, 0],
}


# ============================================================================
# Enums
# ============================================================================

class WaveType(Enum):
    """波形类型"""
    SINE = 'sine'
    SQUARE = 'square'
    SAWTOOTH = 'sawtooth'
    TRIANGLE = 'triangle'
    PULSE = 'pulse'


class TimeUnit(Enum):
    """时间单位"""
    SECONDS = 'seconds'
    MILLISECONDS = 'milliseconds'
    MICROSECONDS = 'microseconds'
    SAMPLES = 'samples'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class PeriodConfig:
    """周期配置"""
    frequency_hz: float
    amplitude: float = 1.0
    phase_offset: float = 0.0
    sample_rate: int = DEFAULT_SAMPLE_RATE
    
    @property
    def period_seconds(self) -> float:
        """周期（秒）"""
        return 1.0 / self.frequency_hz if self.frequency_hz > 0 else 0.0
    
    @property
    def period_samples(self) -> int:
        """周期（采样点数）"""
        return int(self.period_seconds * self.sample_rate)


@dataclass
class BPMConfig:
    """BPM配置"""
    bpm: float
    
    def __post_init__(self):
        if not BPM_MIN <= self.bpm <= BPM_MAX:
            raise ValueError(f"BPM must be between {BPM_MIN} and {BPM_MAX}")
    
    @property
    def beat_duration_ms(self) -> float:
        """单拍时长（毫秒）"""
        return 60000.0 / self.bpm
    
    @property
    def beat_duration_seconds(self) -> float:
        """单拍时长（秒）"""
        return 60.0 / self.bpm
    
    @property
    def quarter_note_ms(self) -> float:
        """四分音符时长（毫秒）"""
        return self.beat_duration_ms
    
    @property
    def eighth_note_ms(self) -> float:
        """八分音符时长（毫秒）"""
        return self.beat_duration_ms / 2
    
    @property
    def sixteenth_note_ms(self) -> float:
        """十六分音符时长（毫秒）"""
        return self.beat_duration_ms / 4
    
    @property
    def thirty_second_note_ms(self) -> float:
        """三十二分音符时长（毫秒）"""
        return self.beat_duration_ms / 8


# ============================================================================
# Core Conversion Functions
# ============================================================================

def bpm_to_ms(bpm: float) -> float:
    """
    将BPM转换为每拍毫秒数.
    
    Args:
        bpm: 每分钟拍数
    
    Returns:
        每拍毫秒数
    
    Examples:
        >>> bpm_to_ms(120)
        500.0
        >>> bpm_to_ms(60)
        1000.0
    """
    if bpm <= 0:
        raise ValueError("BPM must be positive")
    return 60000.0 / bpm


def ms_to_bpm(ms: float) -> float:
    """
    将每拍毫秒数转换为BPM.
    
    Args:
        ms: 每拍毫秒数
    
    Returns:
        每分钟拍数
    
    Examples:
        >>> ms_to_bpm(500)
        120.0
        >>> ms_to_bpm(1000)
        60.0
    """
    if ms <= 0:
        raise ValueError("Milliseconds must be positive")
    return 60000.0 / ms


def hz_to_period_ms(frequency_hz: float) -> float:
    """
    将频率（Hz）转换为周期（毫秒）.
    
    Args:
        frequency_hz: 频率（赫兹）
    
    Returns:
        周期（毫秒）
    
    Examples:
        >>> hz_to_period_ms(1)
        1000.0
        >>> hz_to_period_ms(2)
        500.0
    """
    if frequency_hz <= 0:
        raise ValueError("Frequency must be positive")
    return 1000.0 / frequency_hz


def period_ms_to_hz(period_ms: float) -> float:
    """
    将周期（毫秒）转换为频率（Hz）.
    
    Args:
        period_ms: 周期（毫秒）
    
    Returns:
        频率（赫兹）
    
    Examples:
        >>> period_ms_to_hz(1000)
        1.0
        >>> period_ms_to_hz(500)
        2.0
    """
    if period_ms <= 0:
        raise ValueError("Period must be positive")
    return 1000.0 / period_ms


def frequency_to_note_name(frequency_hz: float) -> str:
    """
    根据频率查找最接近的音符名称.
    
    Args:
        frequency_hz: 频率（赫兹）
    
    Returns:
        音符名称
    
    Examples:
        >>> frequency_to_note_name(440)
        'A4'
        >>> frequency_to_note_name(261.63)
        'C4'
    """
    closest_note = 'A4'
    closest_diff = float('inf')
    
    for note, freq in NOTE_FREQUENCIES.items():
        diff = abs(frequency_hz - freq)
        if diff < closest_diff:
            closest_diff = diff
            closest_note = note
    
    return closest_note


def note_name_to_frequency(note_name: str) -> float:
    """
    将音符名称转换为频率.
    
    Args:
        note_name: 音符名称（如 'A4', 'C#5'）
    
    Returns:
        频率（赫兹）
    
    Raises:
        ValueError: 无效的音符名称
    
    Examples:
        >>> note_name_to_frequency('A4')
        440.0
        >>> note_name_to_frequency('C4')
        261.63
    """
    note_upper = note_name.upper().replace('♯', '#')
    if note_upper not in NOTE_FREQUENCIES:
        raise ValueError(f"Invalid note name: {note_name}")
    return NOTE_FREQUENCIES[note_upper]


def samples_to_seconds(samples: int, sample_rate: int = DEFAULT_SAMPLE_RATE) -> float:
    """
    将采样点数转换为秒.
    
    Args:
        samples: 采样点数
        sample_rate: 采样率
    
    Returns:
        时长（秒）
    
    Examples:
        >>> samples_to_seconds(44100)
        1.0
        >>> samples_to_seconds(22050)
        0.5
    """
    return samples / sample_rate


def seconds_to_samples(seconds: float, sample_rate: int = DEFAULT_SAMPLE_RATE) -> int:
    """
    将秒转换为采样点数.
    
    Args:
        seconds: 时长（秒）
        sample_rate: 采样率
    
    Returns:
        采样点数
    
    Examples:
        >>> seconds_to_samples(1.0)
        44100
        >>> seconds_to_samples(0.5)
        22050
    """
    return int(seconds * sample_rate)


# ============================================================================
# Wave Generation Functions
# ============================================================================

def generate_sine_wave(
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成正弦波样本.
    
    Args:
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅 (0.0 - 1.0)
        phase_offset: 相位偏移（弧度）
        sample_rate: 采样率
    
    Returns:
        正弦波样本列表
    
    Examples:
        >>> wave = generate_sine_wave(44100, 440)
        >>> len(wave)
        44100
        >>> all(-1 <= s <= 1 for s in wave)
        True
    """
    amplitude = max(0.0, min(1.0, amplitude))
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency_hz * t + phase_offset)
        samples.append(value)
    
    return samples


def generate_square_wave(
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    duty_cycle: float = 0.5,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成方波样本.
    
    Args:
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅 (0.0 - 1.0)
        duty_cycle: 占空比 (0.0 - 1.0)
        phase_offset: 相位偏移（弧度）
        sample_rate: 采样率
    
    Returns:
        方波样本列表
    
    Examples:
        >>> wave = generate_square_wave(44100, 440)
        >>> len(wave)
        44100
    """
    amplitude = max(0.0, min(1.0, amplitude))
    duty_cycle = max(0.0, min(1.0, duty_cycle))
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        phase = (frequency_hz * t + phase_offset / (2 * math.pi)) % 1.0
        value = amplitude if phase < duty_cycle else -amplitude
        samples.append(value)
    
    return samples


def generate_sawtooth_wave(
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    ascending: bool = True
) -> List[float]:
    """
    生成锯齿波样本.
    
    Args:
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅 (0.0 - 1.0)
        phase_offset: 相位偏移（弧度）
        sample_rate: 采样率
        ascending: True为上升锯齿，False为下降锯齿
    
    Returns:
        锯齿波样本列表
    
    Examples:
        >>> wave = generate_sawtooth_wave(44100, 440)
        >>> len(wave)
        44100
    """
    amplitude = max(0.0, min(1.0, amplitude))
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        phase = (frequency_hz * t + phase_offset / (2 * math.pi)) % 1.0
        if ascending:
            value = amplitude * (2 * phase - 1)
        else:
            value = amplitude * (1 - 2 * phase)
        samples.append(value)
    
    return samples


def generate_triangle_wave(
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成三角波样本.
    
    Args:
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅 (0.0 - 1.0)
        phase_offset: 相位偏移（弧度）
        sample_rate: 采样率
    
    Returns:
        三角波样本列表
    
    Examples:
        >>> wave = generate_triangle_wave(44100, 440)
        >>> len(wave)
        44100
    """
    amplitude = max(0.0, min(1.0, amplitude))
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        phase = (frequency_hz * t + phase_offset / (2 * math.pi)) % 1.0
        # 三角波公式
        value = amplitude * (4 * abs(phase - 0.5) - 1)
        samples.append(value)
    
    return samples


def generate_pulse_wave(
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    pulse_width: float = 0.1,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成脉冲波样本.
    
    Args:
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅 (0.0 - 1.0)
        pulse_width: 脉冲宽度（占周期的比例）
        phase_offset: 相位偏移（弧度）
        sample_rate: 采样率
    
    Returns:
        脉冲波样本列表
    
    Examples:
        >>> wave = generate_pulse_wave(44100, 440)
        >>> len(wave)
        44100
    """
    return generate_square_wave(
        num_samples, frequency_hz, amplitude, pulse_width, phase_offset, sample_rate
    )


def generate_wave(
    wave_type: Union[str, WaveType],
    num_samples: int,
    frequency_hz: float,
    amplitude: float = 1.0,
    phase_offset: float = 0.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    **kwargs
) -> List[float]:
    """
    根据波形类型生成波形样本.
    
    Args:
        wave_type: 波形类型 ('sine', 'square', 'sawtooth', 'triangle', 'pulse')
        num_samples: 采样点数
        frequency_hz: 频率（赫兹）
        amplitude: 振幅
        phase_offset: 相位偏移
        sample_rate: 采样率
        **kwargs: 额外参数（如 duty_cycle, pulse_width）
    
    Returns:
        波形样本列表
    
    Raises:
        ValueError: 无效的波形类型
    
    Examples:
        >>> wave = generate_wave('sine', 44100, 440)
        >>> len(wave)
        44100
    """
    wave_type_str = wave_type.value if isinstance(wave_type, WaveType) else wave_type.lower()
    
    generators = {
        'sine': generate_sine_wave,
        'square': lambda n, f, a, p, sr: generate_square_wave(
            n, f, a, kwargs.get('duty_cycle', 0.5), p, sr
        ),
        'sawtooth': generate_sawtooth_wave,
        'triangle': generate_triangle_wave,
        'pulse': lambda n, f, a, p, sr: generate_pulse_wave(
            n, f, a, kwargs.get('pulse_width', 0.1), p, sr
        ),
    }
    
    if wave_type_str not in generators:
        raise ValueError(f"Invalid wave type: {wave_type}")
    
    return generators[wave_type_str](num_samples, frequency_hz, amplitude, phase_offset, sample_rate)


# ============================================================================
# Periodic Pattern Functions
# ============================================================================

def generate_periodic_sequence(
    pattern: List[float],
    num_repeats: int,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成周期性重复序列.
    
    Args:
        pattern: 基础模式
        num_repeats: 重复次数
        amplitude: 振幅系数
    
    Returns:
        重复的序列
    
    Examples:
        >>> seq = generate_periodic_sequence([1, 0, 0.5, 0], 3)
        >>> seq
        [1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.5, 0.0]
    """
    sequence = []
    for _ in range(num_repeats):
        for value in pattern:
            sequence.append(value * amplitude)
    return sequence


def generate_heartbeat_pattern(
    bpm: float,
    duration_seconds: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    strength_ratio: float = 0.7
) -> List[float]:
    """
    生成心跳模式样本.
    
    模拟人类心跳的"lub-dub"模式.
    
    Args:
        bpm: 每分钟心跳次数
        duration_seconds: 时长（秒）
        sample_rate: 采样率
        strength_ratio: 第二拍与第一拍的强度比 (0.0 - 1.0)
    
    Returns:
        心跳模式样本
    
    Examples:
        >>> pattern = generate_heartbeat_pattern(72, 10.0)
        >>> len(pattern)
        441000
    """
    num_samples = int(duration_seconds * sample_rate)
    samples = [0.0] * num_samples
    
    beat_interval = int(sample_rate * 60.0 / bpm)
    first_beat_width = int(sample_rate * 0.08)  # 80ms
    second_beat_width = int(sample_rate * 0.05)  # 50ms
    gap = int(sample_rate * 0.15)  # 150ms between beats
    
    pos = 0
    while pos < num_samples:
        # First beat (lub)
        for i in range(min(first_beat_width, num_samples - pos)):
            t = i / first_beat_width
            decay = math.exp(-3 * t)
            samples[pos + i] = decay
        
        pos += first_beat_width + gap
        
        if pos >= num_samples:
            break
        
        # Second beat (dub)
        for i in range(min(second_beat_width, num_samples - pos)):
            t = i / second_beat_width
            decay = math.exp(-3 * t)
            samples[pos + i] = decay * strength_ratio
        
        pos += second_beat_width + (beat_interval - first_beat_width - gap - second_beat_width)
    
    return samples


def generate_metronome_pattern(
    bpm: float,
    duration_seconds: float,
    beats_per_measure: int = 4,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    accent_strength: float = 1.0,
    normal_strength: float = 0.7
) -> List[float]:
    """
    生成节拍器模式.
    
    Args:
        bpm: 每分钟拍数
        duration_seconds: 时长（秒）
        beats_per_measure: 每小节拍数
        sample_rate: 采样率
        accent_strength: 重音拍强度
        normal_strength: 普通拍强度
    
    Returns:
        节拍器模式样本
    
    Examples:
        >>> pattern = generate_metronome_pattern(120, 5.0, beats_per_measure=4)
        >>> len(pattern)
        220500
    """
    num_samples = int(duration_seconds * sample_rate)
    samples = [0.0] * num_samples
    
    beat_interval = int(sample_rate * 60.0 / bpm)
    click_width = int(sample_rate * 0.01)  # 10ms click
    
    beat = 0
    pos = 0
    while pos < num_samples:
        # Determine beat strength
        is_downbeat = (beat % beats_per_measure) == 0
        strength = accent_strength if is_downbeat else normal_strength
        
        # Generate click
        for i in range(min(click_width, num_samples - pos)):
            t = i / click_width
            # Fast attack, quick decay
            value = strength * math.sin(2 * math.pi * 1000 * t) * math.exp(-10 * t)
            samples[pos + i] = value
        
        beat += 1
        pos += beat_interval
    
    return samples


def generate_lfo_pattern(
    num_samples: int,
    rate_hz: float,
    depth: float = 1.0,
    wave_type: Union[str, WaveType] = 'sine',
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成低频振荡器（LFO）模式.
    
    LFO通常用于调制效果，如颤音、相位等.
    
    Args:
        num_samples: 采样点数
        rate_hz: LFO速率（赫兹）
        depth: 深度 (0.0 - 1.0)
        wave_type: 波形类型
        sample_rate: 采样率
    
    Returns:
        LFO样本列表
    
    Examples:
        >>> lfo = generate_lfo_pattern(44100, 5.0)
        >>> len(lfo)
        44100
    """
    # Generate wave in range 0 to 1 for LFO
    wave = generate_wave(wave_type, num_samples, rate_hz, 0.5, 0, sample_rate)
    
    # Normalize to 0-1 range and apply depth
    lfo = [(w + 1) / 2 * depth for w in wave]
    
    return lfo


def generate_tremolo_pattern(
    num_samples: int,
    rate_hz: float,
    depth: float = 0.5,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成颤音模式.
    
    颤音是音量的周期性变化.
    
    Args:
        num_samples: 采样点数
        rate_hz: 颤音速率（赫兹）
        depth: 颤音深度 (0.0 - 1.0)
        sample_rate: 采样率
    
    Returns:
        颤音调制样本列表
    
    Examples:
        >>> tremolo = generate_tremolo_pattern(44100, 5.0, 0.3)
        >>> len(tremolo)
        44100
    """
    depth = max(0.0, min(1.0, depth))
    
    lfo = generate_sine_wave(num_samples, rate_hz, 1.0, 0.0, sample_rate)
    
    # Tremolo: volume modulates between (1-depth) and 1
    tremolo = [(1 - depth) + depth * (w + 1) / 2 for w in lfo]
    
    return tremolo


def generate_vibrato_pattern(
    num_samples: int,
    rate_hz: float,
    semitones: float = 1.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> List[float]:
    """
    生成颤音（音高）模式.
    
    颤音是音高的周期性变化.
    
    Args:
        num_samples: 采样点数
        rate_hz: 颤音速率（赫兹）
        semitones: 音高变化范围（半音）
        sample_rate: 采样率
    
    Returns:
        音高偏移样本列表（以半音为单位）
    
    Examples:
        >>> vibrato = generate_vibrato_pattern(44100, 6.0, 0.5)
        >>> len(vibrato)
        44100
    """
    lfo = generate_sine_wave(num_samples, rate_hz, 1.0, 0.0, sample_rate)
    
    # Vibrato: pitch offset in semitones
    vibrato = [semitones * w for w in lfo]
    
    return vibrato


# ============================================================================
# Rhythm Functions
# ============================================================================

def generate_rhythm_pattern(
    pattern_name: str,
    bpm: float,
    subdivision: str = 'sixteenth'
) -> List[Tuple[float, float]]:
    """
    生成节奏模式的时序信息.
    
    Args:
        pattern_name: 节奏模式名称
        bpm: 每分钟拍数
        subdivision: 细分类型 ('quarter', 'eighth', 'sixteenth', 'thirty_second')
    
    Returns:
        [(时间点毫秒, 强度), ...] 列表
    
    Raises:
        ValueError: 无效的模式名称
    
    Examples:
        >>> pattern = generate_rhythm_pattern('straight_4', 120)
        >>> len(pattern)
        4
    """
    if pattern_name not in RHYTHM_PATTERNS:
        raise ValueError(f"Unknown pattern: {pattern_name}. Available: {list(RHYTHM_PATTERNS.keys())}")
    
    pattern = RHYTHM_PATTERNS[pattern_name]
    beat_ms = bpm_to_ms(bpm)
    
    # Subdivision multipliers
    subdivision_multipliers = {
        'quarter': 1,
        'eighth': 0.5,
        'sixteenth': 0.25,
        'thirty_second': 0.125,
    }
    
    sub_mult = subdivision_multipliers.get(subdivision, 0.25)
    sub_ms = beat_ms * sub_mult
    
    result = []
    for i, strength in enumerate(pattern):
        if strength > 0:
            result.append((i * sub_ms, float(strength)))
    
    return result


def analyze_rhythm_pattern(pattern: List[Union[int, float]]) -> Dict:
    """
    分析节奏模式.
    
    Args:
        pattern: 节奏模式（1=拍，0=休止，小数为强度）
    
    Returns:
        分析结果字典
    
    Examples:
        >>> analysis = analyze_rhythm_pattern([1, 0, 0.5, 0])
        >>> analysis['beat_count']
        2
    """
    total_steps = len(pattern)
    beats = [p for p in pattern if p > 0]
    beat_count = len(beats)
    average_intensity = sum(beats) / beat_count if beat_count > 0 else 0
    
    # Calculate syncopation (how many beats are off the downbeat)
    syncopation_count = sum(1 for i, p in enumerate(pattern) if p > 0 and i % 2 != 0)
    
    # Find longest rest
    max_rest = 0
    current_rest = 0
    for p in pattern:
        if p == 0:
            current_rest += 1
            max_rest = max(max_rest, current_rest)
        else:
            current_rest = 0
    
    return {
        'total_steps': total_steps,
        'beat_count': beat_count,
        'rest_count': total_steps - beat_count,
        'density': beat_count / total_steps if total_steps > 0 else 0,
        'average_intensity': round(average_intensity, 3),
        'syncopation_count': syncopation_count,
        'max_consecutive_rests': max_rest,
        'is_regular': syncopation_count == 0 and all(p in [0, 1] for p in pattern),
    }


def create_custom_pattern(
    beat_positions: List[int],
    total_steps: int,
    strengths: Optional[List[float]] = None
) -> List[float]:
    """
    创建自定义节奏模式.
    
    Args:
        beat_positions: 拍位列表（从0开始）
        total_steps: 总步数
        strengths: 每拍的强度列表（可选）
    
    Returns:
        节奏模式列表
    
    Examples:
        >>> create_custom_pattern([0, 2, 4, 6], 8)
        [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    """
    pattern = [0.0] * total_steps
    
    if strengths is None:
        strengths = [1.0] * len(beat_positions)
    
    for i, pos in enumerate(beat_positions):
        if 0 <= pos < total_steps:
            pattern[pos] = strengths[i] if i < len(strengths) else 1.0
    
    return pattern


# ============================================================================
# Utility Functions
# ============================================================================

def calculate_harmonics(fundamental_hz: float, num_harmonics: int = 8) -> List[float]:
    """
    计算谐波频率.
    
    Args:
        fundamental_hz: 基频（赫兹）
        num_harmonics: 谐波数量
    
    Returns:
        谐波频率列表 [基频, 2次谐波, 3次谐波, ...]
    
    Examples:
        >>> harmonics = calculate_harmonics(440, 4)
        >>> harmonics
        [440.0, 880.0, 1320.0, 1760.0]
    """
    return [fundamental_hz * (n + 1) for n in range(num_harmonics)]


def calculate_octave_equivalent(frequency_hz: float, target_octave: int = 4) -> float:
    """
    计算等八度等效频率.
    
    将任意频率转换到目标八度.
    
    Args:
        frequency_hz: 原始频率（赫兹）
        target_octave: 目标八度
    
    Returns:
        目标八度的等效频率
    
    Examples:
        >>> calculate_octave_equivalent(880, 4)  # A5 to A4
        440.0
        >>> calculate_octave_equivalent(220, 4)  # A3 to A4
        440.0
    """
    a4 = 440.0
    octaves_from_a4 = math.log2(frequency_hz / a4)
    current_octave = 4 + octaves_from_a4
    octave_diff = current_octave - target_octave
    
    return frequency_hz / (2 ** octave_diff)


def quantize_to_grid(
    time_ms: float,
    grid_ms: float,
    rounding: str = 'nearest'
) -> float:
    """
    将时间量化到网格.
    
    Args:
        time_ms: 原始时间（毫秒）
        grid_ms: 网格大小（毫秒）
        rounding: 舍入方式 ('nearest', 'up', 'down')
    
    Returns:
        量化后的时间（毫秒）
    
    Examples:
        >>> quantize_to_grid(523, 100)
        500
        >>> quantize_to_grid(523, 100, 'up')
        600
    """
    if grid_ms <= 0:
        return time_ms
    
    if rounding == 'up':
        return math.ceil(time_ms / grid_ms) * grid_ms
    elif rounding == 'down':
        return math.floor(time_ms / grid_ms) * grid_ms
    else:
        return round(time_ms / grid_ms) * grid_ms


def calculate_swing_offset(
    position: int,
    swing_amount: float = 0.5,
    subdivision: int = 8
) -> float:
    """
    计算摇摆节奏的时间偏移.
    
    Args:
        position: 在细分中的位置
        swing_amount: 摇摆量 (0.0 - 1.0, 0.5 = 无摇摆)
        subdivision: 细分（通常为8或16）
    
    Returns:
        时间偏移比例
    
    Examples:
        >>> calculate_swing_offset(0, 0.6)  # First eighth, no offset
        0.0
        >>> calculate_swing_offset(1, 0.6)  # Second eighth, delayed
        0.1
    """
    # Swing only affects off-beats (odd positions in eighth notes)
    if subdivision == 8:
        if position % 2 == 1:
            return swing_amount - 0.5
    elif subdivision == 16:
        if position % 4 == 2:
            return (swing_amount - 0.5) * 0.5
    
    return 0.0


def format_time_ms(ms: float) -> str:
    """
    格式化毫秒时间显示.
    
    Args:
        ms: 毫秒数
    
    Returns:
        格式化的时间字符串
    
    Examples:
        >>> format_time_ms(1234.5)
        '1.235s'
        >>> format_time_ms(500)
        '500ms'
    """
    if ms >= 1000:
        return f"{ms / 1000:.3f}s"
    else:
        return f"{ms:.1f}ms"


def format_bpm(bpm: float) -> str:
    """
    格式化BPM显示.
    
    Args:
        bpm: 每分钟拍数
    
    Returns:
        格式化的BPM字符串
    
    Examples:
        >>> format_bpm(120)
        '120 BPM'
        >>> format_bpm(128.5)
        '128.5 BPM'
    """
    if bpm == int(bpm):
        return f"{int(bpm)} BPM"
    return f"{bpm:.1f} BPM"


def format_frequency(hz: float) -> str:
    """
    格式化频率显示.
    
    Args:
        hz: 频率（赫兹）
    
    Returns:
        格式化的频率字符串
    
    Examples:
        >>> format_frequency(440)
        '440 Hz'
        >>> format_frequency(1500)
        '1.50 kHz'
    """
    if hz >= 1000:
        return f"{hz / 1000:.2f} kHz"
    return f"{hz:.1f} Hz"


# ============================================================================
# High-Level Period Generator Class
# ============================================================================

class PeriodGenerator:
    """周期模式生成器类"""
    
    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        """
        初始化周期生成器.
        
        Args:
            sample_rate: 采样率
        """
        self.sample_rate = sample_rate
        self._samples: List[float] = []
        self._current_time: float = 0.0
    
    @property
    def duration_seconds(self) -> float:
        """当前时长（秒）"""
        return len(self._samples) / self.sample_rate
    
    @property
    def num_samples(self) -> int:
        """当前采样点数"""
        return len(self._samples)
    
    def add_wave(
        self,
        wave_type: Union[str, WaveType],
        frequency_hz: float,
        duration_seconds: float,
        amplitude: float = 1.0,
        phase_offset: float = 0.0,
        **kwargs
    ) -> 'PeriodGenerator':
        """添加波形"""
        num_samples = int(duration_seconds * self.sample_rate)
        wave = generate_wave(
            wave_type, num_samples, frequency_hz, amplitude, phase_offset, self.sample_rate, **kwargs
        )
        
        if self._samples:
            for i in range(min(len(self._samples), len(wave))):
                self._samples[i] += wave[i]
            if len(wave) > len(self._samples):
                self._samples.extend(wave[len(self._samples):])
        else:
            self._samples = wave
        
        return self
    
    def add_pattern(
        self,
        pattern: List[float],
        num_repeats: int,
        beat_duration_ms: float,
        amplitude: float = 1.0
    ) -> 'PeriodGenerator':
        """添加节奏模式"""
        beat_samples = int(beat_duration_ms * self.sample_rate / 1000)
        
        for _ in range(num_repeats):
            for strength in pattern:
                if strength > 0:
                    click = generate_wave('sine', 100, beat_samples // 4, strength * amplitude * 0.5)
                    start = len(self._samples)
                    self._samples.extend([0.0] * (beat_samples - len(click)))
                    for i, c in enumerate(click):
                        if start + i < len(self._samples):
                            self._samples[start + i] += c
                else:
                    self._samples.extend([0.0] * beat_samples)
        
        return self
    
    def add_heartbeat(
        self,
        bpm: float,
        duration_seconds: float,
        strength_ratio: float = 0.7
    ) -> 'PeriodGenerator':
        """添加心跳模式"""
        heartbeat = generate_heartbeat_pattern(bpm, duration_seconds, self.sample_rate, strength_ratio)
        
        if self._samples:
            for i in range(min(len(self._samples), len(heartbeat))):
                self._samples[i] += heartbeat[i]
            if len(heartbeat) > len(self._samples):
                self._samples.extend(heartbeat[len(self._samples):])
        else:
            self._samples = heartbeat
        
        return self
    
    def apply_envelope(
        self,
        attack_ms: float = 10.0,
        release_ms: float = 10.0
    ) -> 'PeriodGenerator':
        """应用包络"""
        attack_samples = int(attack_ms * self.sample_rate / 1000)
        release_samples = int(release_ms * self.sample_rate / 1000)
        
        # Apply attack
        for i in range(min(attack_samples, len(self._samples))):
            self._samples[i] *= i / attack_samples
        
        # Apply release
        for i in range(min(release_samples, len(self._samples))):
            self._samples[-(i + 1)] *= i / release_samples
        
        return self
    
    def normalize(self) -> 'PeriodGenerator':
        """归一化"""
        max_val = max(abs(s) for s in self._samples) if self._samples else 1.0
        if max_val > 0:
            self._samples = [s / max_val for s in self._samples]
        return self
    
    def get_samples(self) -> List[float]:
        """获取样本"""
        return self._samples.copy()
    
    def clear(self) -> 'PeriodGenerator':
        """清空"""
        self._samples = []
        return self
    
    def info(self) -> Dict:
        """获取信息"""
        return {
            'sample_rate': self.sample_rate,
            'duration_seconds': round(self.duration_seconds, 3),
            'num_samples': self.num_samples,
        }


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Period Utilities Demo")
    print("=" * 60)
    
    # BPM conversions
    print("\n--- BPM 转换 ---")
    for bpm in [60, 90, 120, 140, 160, 180]:
        ms = bpm_to_ms(bpm)
        print(f"{bpm} BPM = {ms:.1f}ms per beat")
    
    # Frequency conversions
    print("\n--- 频率转换 ---")
    for hz in [1, 2, 4, 10, 440]:
        period = hz_to_period_ms(hz)
        print(f"{hz} Hz = {period:.1f}ms period")
    
    # Note frequencies
    print("\n--- 音符频率 ---")
    for note in ['C4', 'A4', 'E4', 'G4', 'C5']:
        freq = note_name_to_frequency(note)
        print(f"{note} = {freq:.2f} Hz")
    
    # Wave generation
    print("\n--- 波形生成 ---")
    for wave_type in ['sine', 'square', 'triangle', 'sawtooth']:
        wave = generate_wave(wave_type, 44100, 440)
        print(f"{wave_type}: {len(wave)} samples, range [{min(wave):.3f}, {max(wave):.3f}]")
    
    # Heartbeat pattern
    print("\n--- 心跳模式 ---")
    heartbeat = generate_heartbeat_pattern(72, 5.0)
    print(f"72 BPM, 5秒心跳: {len(heartbeat)} samples")
    
    # Rhythm patterns
    print("\n--- 节奏模式 ---")
    for name in ['straight_4', 'waltz', 'heartbeat']:
        pattern = RHYTHM_PATTERNS[name]
        analysis = analyze_rhythm_pattern(pattern)
        print(f"{name}: {pattern} -> 密度 {analysis['density']:.2f}")
    
    # Harmonics
    print("\n--- 谐波 ---")
    harmonics = calculate_harmonics(440, 5)
    print(f"A4 (440 Hz) 的前5个谐波: {[f'{h:.0f}Hz' for h in harmonics]}")
    
    print("\n" + "=" * 60)