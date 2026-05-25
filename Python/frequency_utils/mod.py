#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Frequency Utilities Module
========================================
A comprehensive frequency conversion and audio calculation utility module for Python
with zero external dependencies.

Features:
    - Frequency unit conversion (Hz, kHz, MHz, GHz, THz, rpm)
    - Frequency to period conversion
    - Frequency to wavelength conversion (with customizable wave speed)
    - Musical note frequency calculation (A4 = 440 Hz standard)
    - Octave calculation
    - Cent calculation (pitch difference)
    - Harmonic series generation
    - Frequency band classification (radio spectrum)

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-25
"""

from typing import Union, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import math


# ============================================================================
# Constants
# ============================================================================

# Speed of light in vacuum (m/s)
SPEED_OF_LIGHT = 299792458.0

# Speed of sound in air at 20°C (m/s)
SPEED_OF_SOUND_AIR_20C = 343.0

# Speed of sound in water at 20°C (m/s)
SPEED_OF_SOUND_WATER = 1481.0

# Standard A4 frequency (Hz)
STANDARD_A4 = 440.0

# Number of cents per octave
CENTS_PER_OCTAVE = 1200

# Number of semitones per octave
SEMITONES_PER_OCTAVE = 12

# Frequency unit conversion factors to Hz
FREQUENCY_UNITS = {
    'pHz': 1e-12,    # picohertz
    'nHz': 1e-9,     # nanohertz
    'μHz': 1e-6,     # microhertz
    'mHz': 1e-3,     # millihertz
    'Hz': 1.0,       # hertz
    'kHz': 1e3,      # kilohertz
    'MHz': 1e6,      # megahertz
    'GHz': 1e9,      # gigahertz
    'THz': 1e12,     # terahertz
    'PHz': 1e15,     # petahertz
    'rpm': 1.0 / 60.0,  # revolutions per minute
    'rps': 1.0,      # revolutions per second
}

# Musical note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Radio spectrum bands (frequency ranges in Hz)
RADIO_BANDS = {
    'ELF': (3, 30, 'Extremely Low Frequency'),
    'SLF': (30, 300, 'Super Low Frequency'),
    'ULF': (300, 3000, 'Ultra Low Frequency'),
    'VLF': (3e3, 30e3, 'Very Low Frequency'),
    'LF': (30e3, 300e3, 'Low Frequency'),
    'MF': (300e3, 3e6, 'Medium Frequency'),
    'HF': (3e6, 30e6, 'High Frequency'),
    'VHF': (30e6, 300e6, 'Very High Frequency'),
    'UHF': (300e6, 3e9, 'Ultra High Frequency'),
    'SHF': (3e9, 30e9, 'Super High Frequency'),
    'EHF': (30e9, 300e9, 'Extremely High Frequency'),
    'THF': (300e9, 3e12, 'Tremendously High Frequency'),
}


# ============================================================================
# Enums
# ============================================================================

class FrequencyUnit(Enum):
    """频率单位枚举"""
    PICOHZ = 'pHz'
    NANOHZ = 'nHz'
    MICROHZ = 'μHz'
    MILLIHZ = 'mHz'
    HZ = 'Hz'
    KILOHZ = 'kHz'
    MEGAHZ = 'MHz'
    GIGAHZ = 'GHz'
    TERAHZ = 'THz'
    PETAHZ = 'PHz'
    RPM = 'rpm'
    RPS = 'rps'


class WaveMedium(Enum):
    """波传播介质枚举"""
    VACUUM = 'vacuum'
    AIR = 'air'
    WATER = 'water'


class NoteNaming(Enum):
    """音符命名方式枚举"""
    SHARP = 'sharp'      # C#, D#, F#, G#, A#
    FLAT = 'flat'        # Db, Eb, Gb, Ab, Bb
    BOTH = 'both'        # 返回两种名称


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FrequencyResult:
    """频率转换结果"""
    hertz: float
    kilohertz: float
    megahertz: float
    gigahertz: float
    terahertz: float
    rpm: float
    period_seconds: float
    period_milliseconds: float
    period_microseconds: float


@dataclass
class WavelengthResult:
    """波长计算结果"""
    frequency_hz: float
    wavelength_m: float
    wavelength_cm: float
    wavelength_mm: float
    wavelength_um: float
    wavelength_nm: float
    wave_speed: float
    medium: str


@dataclass
class NoteResult:
    """音符计算结果"""
    note_name: str
    note_name_flat: str
    octave: int
    full_name: str
    frequency_hz: float
    midi_note: int
    semitones_from_a4: int


@dataclass
class CentResult:
    """音分计算结果"""
    frequency1_hz: float
    frequency2_hz: float
    cents: float
    semitones: float
    octaves: float
    ratio: float


@dataclass
class HarmonicResult:
    """谐波系列结果"""
    fundamental_hz: float
    harmonics: List[Tuple[int, float, str]]
    overtones: List[Tuple[int, float, str]]


# ============================================================================
# Frequency Conversion Functions
# ============================================================================

def convert_frequency(
    value: float,
    from_unit: Union[str, FrequencyUnit],
    to_unit: Union[str, FrequencyUnit]
) -> float:
    """
    频率单位转换.
    
    Args:
        value: 频率值
        from_unit: 原单位 (Hz, kHz, MHz, GHz, THz, rpm, rps 等)
        to_unit: 目标单位
    
    Returns:
        转换后的频率值
    
    Examples:
        >>> convert_frequency(1000, 'Hz', 'kHz')
        1.0
        >>> convert_frequency(60, 'rpm', 'Hz')
        1.0
        >>> convert_frequency(1, 'GHz', 'MHz')
        1000.0
    """
    # 转换为字符串
    from_str = from_unit.value if isinstance(from_unit, FrequencyUnit) else from_unit
    to_str = to_unit.value if isinstance(to_unit, FrequencyUnit) else to_unit
    
    if from_str not in FREQUENCY_UNITS:
        raise ValueError(f"未知的频率单位: {from_str}")
    if to_str not in FREQUENCY_UNITS:
        raise ValueError(f"未知的频率单位: {to_str}")
    
    # 先转换为 Hz
    hertz = value * FREQUENCY_UNITS[from_str]
    
    # 再从 Hz 转换为目标单位
    result = hertz / FREQUENCY_UNITS[to_str]
    
    return result


def frequency_to_all(value: float, unit: Union[str, FrequencyUnit] = 'Hz') -> FrequencyResult:
    """
    将频率转换为所有常用单位.
    
    Args:
        value: 频率值
        unit: 输入单位
    
    Returns:
        FrequencyResult 对象，包含所有单位的转换结果
    
    Examples:
        >>> result = frequency_to_all(1, 'MHz')
        >>> result.hertz
        1000000.0
        >>> result.kilohertz
        1000.0
    """
    hz = convert_frequency(value, unit, 'Hz')
    
    return FrequencyResult(
        hertz=hz,
        kilohertz=convert_frequency(hz, 'Hz', 'kHz'),
        megahertz=convert_frequency(hz, 'Hz', 'MHz'),
        gigahertz=convert_frequency(hz, 'Hz', 'GHz'),
        terahertz=convert_frequency(hz, 'Hz', 'THz'),
        rpm=convert_frequency(hz, 'Hz', 'rpm'),
        period_seconds=1.0 / hz if hz > 0 else float('inf'),
        period_milliseconds=1000.0 / hz if hz > 0 else float('inf'),
        period_microseconds=1000000.0 / hz if hz > 0 else float('inf')
    )


# ============================================================================
# Period Functions
# ============================================================================

def frequency_to_period(frequency_hz: float) -> float:
    """
    频率转周期.
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        周期 (秒)
    
    Examples:
        >>> frequency_to_period(50)
        0.02
        >>> frequency_to_period(1000)
        0.001
    """
    if frequency_hz <= 0:
        raise ValueError("频率必须为正数")
    return 1.0 / frequency_hz


def period_to_frequency(period_seconds: float) -> float:
    """
    周期转频率.
    
    Args:
        period_seconds: 周期 (秒)
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> period_to_frequency(0.02)
        50.0
        >>> period_to_frequency(0.001)
        1000.0
    """
    if period_seconds <= 0:
        raise ValueError("周期必须为正数")
    return 1.0 / period_seconds


def angular_frequency(frequency_hz: float) -> float:
    """
    计算角频率 (ω = 2πf).
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        角频率 (rad/s)
    
    Examples:
        >>> round(angular_frequency(1), 4)
        6.2832
    """
    return 2 * math.pi * frequency_hz


def angular_to_frequency(angular_freq: float) -> float:
    """
    角频率转普通频率.
    
    Args:
        angular_freq: 角频率 (rad/s)
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> round(angular_to_frequency(6.28318), 4)
        1.0
    """
    return angular_freq / (2 * math.pi)


# ============================================================================
# Wavelength Functions
# ============================================================================

def frequency_to_wavelength(
    frequency_hz: float,
    wave_speed: float = SPEED_OF_LIGHT,
    medium: WaveMedium = WaveMedium.VACUUM
) -> float:
    """
    频率转波长.
    
    公式: λ = v / f
    
    Args:
        frequency_hz: 频率 (Hz)
        wave_speed: 波速 (m/s)，默认为光速
        medium: 传播介质
    
    Returns:
        波长 (米)
    
    Examples:
        >>> round(frequency_to_wavelength(100e6), 2)  # 100 MHz radio wave
        3.0
        >>> round(frequency_to_wavelength(440, SPEED_OF_SOUND_AIR_20C), 3)  # A4 note
        0.78
    """
    if frequency_hz <= 0:
        raise ValueError("频率必须为正数")
    return wave_speed / frequency_hz


def wavelength_to_frequency(
    wavelength_m: float,
    wave_speed: float = SPEED_OF_LIGHT,
    medium: WaveMedium = WaveMedium.VACUUM
) -> float:
    """
    波长转频率.
    
    公式: f = v / λ
    
    Args:
        wavelength_m: 波长 (米)
        wave_speed: 波速 (m/s)，默认为光速
        medium: 传播介质
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> wavelength_to_frequency(3)  # 3 meter wavelength
        99930819.33...
    """
    if wavelength_m <= 0:
        raise ValueError("波长必须为正数")
    return wave_speed / wavelength_m


def get_wavelength_result(
    frequency_hz: float,
    medium: WaveMedium = WaveMedium.VACUUM
) -> WavelengthResult:
    """
    获取完整的波长计算结果.
    
    Args:
        frequency_hz: 频率 (Hz)
        medium: 传播介质
    
    Returns:
        WavelengthResult 对象
    
    Examples:
        >>> result = get_wavelength_result(440, WaveMedium.AIR)
        >>> result.wavelength_m  # A4 note in air
        0.78...
    """
    # 根据介质选择波速
    if medium == WaveMedium.VACUUM:
        wave_speed = SPEED_OF_LIGHT
        medium_name = '真空 (光速)'
    elif medium == WaveMedium.AIR:
        wave_speed = SPEED_OF_SOUND_AIR_20C
        medium_name = '空气 (20°C)'
    elif medium == WaveMedium.WATER:
        wave_speed = SPEED_OF_SOUND_WATER
        medium_name = '水 (20°C)'
    else:
        wave_speed = SPEED_OF_LIGHT
        medium_name = '未知'
    
    wavelength_m = frequency_to_wavelength(frequency_hz, wave_speed, medium)
    
    return WavelengthResult(
        frequency_hz=frequency_hz,
        wavelength_m=wavelength_m,
        wavelength_cm=wavelength_m * 100,
        wavelength_mm=wavelength_m * 1000,
        wavelength_um=wavelength_m * 1e6,
        wavelength_nm=wavelength_m * 1e9,
        wave_speed=wave_speed,
        medium=medium_name
    )


# ============================================================================
# Musical Note Functions
# ============================================================================

def note_to_frequency(
    note: str,
    octave: int,
    a4_hz: float = STANDARD_A4
) -> float:
    """
    音符名称转频率.
    
    Args:
        note: 音符名称 (C, C#, D, D#, E, F, F#, G, G#, A, A#, B 或 Db, Eb 等)
        octave: 八度 (0-9)
        a4_hz: A4 参考频率，默认 440 Hz
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> round(note_to_frequency('A', 4), 2)
        440.0
        >>> round(note_to_frequency('C', 4), 2)  # Middle C
        261.63
    """
    # 标准化音符名称
    note = note.strip().upper()
    
    # 处理降号
    flat_to_sharp = {
        'DB': 'C#', 'EB': 'D#', 'FB': 'E', 'GB': 'F#',
        'AB': 'G#', 'BB': 'A#', 'CB': 'B'
    }
    
    if note in flat_to_sharp:
        note = flat_to_sharp[note]
    
    # 获取音符的半音偏移
    if note not in NOTE_NAMES:
        raise ValueError(f"未知的音符: {note}")
    
    semitone_offset = NOTE_NAMES.index(note)
    
    # A4 的 MIDI 音符编号是 69
    # 计算 MIDI 音符编号
    midi_note = 12 + octave * 12 + semitone_offset
    
    # 计算与 A4 的半音差
    a4_midi = 69
    semitones_from_a4 = midi_note - a4_midi
    
    # 使用十二平均律计算频率
    frequency = a4_hz * (2 ** (semitones_from_a4 / 12.0))
    
    return frequency


def frequency_to_note(
    frequency_hz: float,
    a4_hz: float = STANDARD_A4,
    naming: NoteNaming = NoteNaming.SHARP
) -> NoteResult:
    """
    频率转音符.
    
    Args:
        frequency_hz: 频率 (Hz)
        a4_hz: A4 参考频率，默认 440 Hz
        naming: 音符命名方式
    
    Returns:
        NoteResult 对象
    
    Examples:
        >>> result = frequency_to_note(440)
        >>> result.note_name
        'A'
        >>> result.octave
        4
    """
    if frequency_hz <= 0:
        raise ValueError("频率必须为正数")
    
    # 计算与 A4 的半音差
    semitones_from_a4 = 12 * math.log2(frequency_hz / a4_hz)
    
    # 四舍五入到最近的半音
    rounded_semitones = round(semitones_from_a4)
    
    # A4 的 MIDI 音符编号是 69
    midi_note = 69 + rounded_semitones
    
    # 计算八度和音符
    octave = (midi_note // 12) - 1
    note_index = midi_note % 12
    
    note_name = NOTE_NAMES[note_index]
    
    # 生成降号名称
    sharp_to_flat = {
        'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb',
        'G#': 'Ab', 'A#': 'Bb'
    }
    note_name_flat = sharp_to_flat.get(note_name, note_name)
    
    # 计算精确频率
    exact_frequency = a4_hz * (2 ** (rounded_semitones / 12.0))
    
    return NoteResult(
        note_name=note_name,
        note_name_flat=note_name_flat,
        octave=octave,
        full_name=f"{note_name}{octave}",
        frequency_hz=round(exact_frequency, 2),
        midi_note=midi_note,
        semitones_from_a4=rounded_semitones
    )


def get_midi_frequency(midi_note: int, a4_hz: float = STANDARD_A4) -> float:
    """
    MIDI 音符编号转频率.
    
    Args:
        midi_note: MIDI 音符编号 (0-127)
        a4_hz: A4 参考频率
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> round(get_midi_frequency(69), 2)  # A4
        440.0
        >>> round(get_midi_frequency(60), 2)  # C4 (Middle C)
        261.63
    """
    if not 0 <= midi_note <= 127:
        raise ValueError("MIDI 音符编号必须在 0-127 之间")
    
    return a4_hz * (2 ** ((midi_note - 69) / 12.0))


def get_note_harmonics(
    fundamental_hz: float,
    num_harmonics: int = 10,
    include_fundamental: bool = True
) -> HarmonicResult:
    """
    生成谐波系列.
    
    Args:
        fundamental_hz: 基频 (Hz)
        num_harmonics: 谐波数量
        include_fundamental: 是否包含基频
    
    Returns:
        HarmonicResult 对象
    
    Examples:
        >>> result = get_note_harmonics(440, 5)
        >>> result.harmonics[0]  # 1st harmonic (fundamental)
        (1, 440.0, 'A4')
    """
    harmonics = []
    overtones = []
    
    start = 1 if include_fundamental else 2
    
    for n in range(start, num_harmonics + start):
        freq = fundamental_hz * n
        note_info = frequency_to_note(freq)
        harmonics.append((n, round(freq, 2), f"{note_info.note_name}{note_info.octave}"))
        
        if n > 1:
            overtones.append((n - 1, round(freq, 2), f"{note_info.note_name}{note_info.octave}"))
    
    return HarmonicResult(
        fundamental_hz=fundamental_hz,
        harmonics=harmonics,
        overtones=overtones
    )


# ============================================================================
# Cent and Interval Functions
# ============================================================================

def calculate_cents(
    frequency1_hz: float,
    frequency2_hz: float
) -> float:
    """
    计算两个频率之间的音分差.
    
    公式: cents = 1200 × log2(f2 / f1)
    
    Args:
        frequency1_hz: 第一个频率 (Hz)
        frequency2_hz: 第二个频率 (Hz)
    
    Returns:
        音分差 (正数表示 f2 更高)
    
    Examples:
        >>> calculate_cents(440, 880)  # One octave
        1200.0
        >>> calculate_cents(440, 466.16)  # One semitone
        100.0
    """
    if frequency1_hz <= 0 or frequency2_hz <= 0:
        raise ValueError("频率必须为正数")
    
    return CENTS_PER_OCTAVE * math.log2(frequency2_hz / frequency1_hz)


def cents_to_frequency(
    base_frequency_hz: float,
    cents: float
) -> float:
    """
    从基频和音分计算目标频率.
    
    公式: f2 = f1 × 2^(cents/1200)
    
    Args:
        base_frequency_hz: 基频 (Hz)
        cents: 音分差
    
    Returns:
        目标频率 (Hz)
    
    Examples:
        >>> round(cents_to_frequency(440, 1200), 2)  # One octave up
        880.0
        >>> round(cents_to_frequency(440, 100), 2)  # One semitone up
        466.16
    """
    if base_frequency_hz <= 0:
        raise ValueError("基频必须为正数")
    
    return base_frequency_hz * (2 ** (cents / CENTS_PER_OCTAVE))


def get_cent_result(
    frequency1_hz: float,
    frequency2_hz: float
) -> CentResult:
    """
    获取完整的音分计算结果.
    
    Args:
        frequency1_hz: 第一个频率 (Hz)
        frequency2_hz: 第二个频率 (Hz)
    
    Returns:
        CentResult 对象
    
    Examples:
        >>> result = get_cent_result(440, 880)
        >>> result.cents
        1200.0
        >>> result.octaves
        1.0
    """
    cents = calculate_cents(frequency1_hz, frequency2_hz)
    semitones = cents / 100.0
    octaves = cents / CENTS_PER_OCTAVE
    ratio = frequency2_hz / frequency1_hz
    
    return CentResult(
        frequency1_hz=frequency1_hz,
        frequency2_hz=frequency2_hz,
        cents=round(cents, 2),
        semitones=round(semitones, 2),
        octaves=round(octaves, 4),
        ratio=round(ratio, 4)
    )


def frequency_ratio_to_cents(ratio: float) -> float:
    """
    频率比转音分.
    
    Args:
        ratio: 频率比 (f2/f1)
    
    Returns:
        音分
    
    Examples:
        >>> frequency_ratio_to_cents(2)  # Octave
        1200.0
        >>> round(frequency_ratio_to_cents(1.5), 2)  # Perfect fifth
        701.95
    """
    if ratio <= 0:
        raise ValueError("频率比必须为正数")
    return CENTS_PER_OCTAVE * math.log2(ratio)


def cents_to_ratio(cents: float) -> float:
    """
    音分转频率比.
    
    Args:
        cents: 音分
    
    Returns:
        频率比
    
    Examples:
        >>> round(cents_to_ratio(1200), 4)
        2.0
        >>> round(cents_to_ratio(700), 4)  # Perfect fifth
        1.4983
    """
    return 2 ** (cents / CENTS_PER_OCTAVE)


# ============================================================================
# Radio Spectrum Functions
# ============================================================================

def get_radio_band(frequency_hz: float) -> Tuple[str, str]:
    """
    获取无线电频段信息.
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        (频段代码, 频段名称)
    
    Examples:
        >>> get_radio_band(100e6)  # 100 MHz
        ('VHF', 'Very High Frequency')
        >>> get_radio_band(2.4e9)  # 2.4 GHz
        ('UHF', 'Ultra High Frequency')
    """
    for band_code, (min_freq, max_freq, band_name) in RADIO_BANDS.items():
        if min_freq <= frequency_hz < max_freq:
            return band_code, band_name
    
    if frequency_hz >= 3e12:
        return 'IR', 'Infrared and above'
    else:
        return 'Unknown', 'Unknown frequency band'


def get_band_frequencies(band_code: str) -> Tuple[float, float, str]:
    """
    获取指定频段的频率范围.
    
    Args:
        band_code: 频段代码 (ELF, VLF, LF, MF, HF, VHF, UHF, SHF, EHF 等)
    
    Returns:
        (最小频率 Hz, 最大频率 Hz, 频段名称)
    
    Examples:
        >>> get_band_frequencies('FM')  # FM radio is in VHF
        >>> get_band_frequencies('VHF')
        (30000000.0, 300000000.0, 'Very High Frequency')
    """
    band_code = band_code.upper()
    if band_code in RADIO_BANDS:
        return RADIO_BANDS[band_code]
    raise ValueError(f"未知的频段代码: {band_code}")


def list_radio_bands() -> List[Tuple[str, float, float, str]]:
    """
    列出所有无线电频段.
    
    Returns:
        频段列表 [(代码, 最小频率, 最大频率, 名称), ...]
    
    Examples:
        >>> bands = list_radio_bands()
        >>> bands[0]
        ('ELF', 3, 30, 'Extremely Low Frequency')
    """
    return [
        (code, min_freq, max_freq, name)
        for code, (min_freq, max_freq, name) in RADIO_BANDS.items()
    ]


# ============================================================================
# Utility Functions
# ============================================================================

def is_audio_frequency(frequency_hz: float) -> bool:
    """
    检查是否为音频范围 (20 Hz - 20 kHz).
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        是否为音频
    
    Examples:
        >>> is_audio_frequency(440)
        True
        >>> is_audio_frequency(100000)
        False
    """
    return 20 <= frequency_hz <= 20000


def is_radio_frequency(frequency_hz: float) -> bool:
    """
    检查是否为无线电频率 (3 kHz - 300 GHz).
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        是否为无线电频率
    
    Examples:
        >>> is_radio_frequency(100e6)
        True
        >>> is_radio_frequency(440)
        False
    """
    return 3e3 <= frequency_hz <= 300e9


def is_visible_light(frequency_hz: float) -> bool:
    """
    检查是否为可见光频率 (约 400-800 THz).
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        是否为可见光
    
    Examples:
        >>> is_visible_light(500e12)  # 500 THz
        True
        >>> is_visible_light(100e12)
        False
    """
    return 400e12 <= frequency_hz <= 800e12


def get_frequency_description(frequency_hz: float) -> str:
    """
    获取频率的描述信息.
    
    Args:
        frequency_hz: 频率 (Hz)
    
    Returns:
        频率描述字符串
    
    Examples:
        >>> get_frequency_description(440)
        '音频范围 - A4 音符'
        >>> get_frequency_description(100e6)
        'VHF (Very High Frequency) - 甚高频'
    """
    if is_audio_frequency(frequency_hz):
        note = frequency_to_note(frequency_hz)
        return f"音频范围 - {note.full_name} 音符"
    elif is_visible_light(frequency_hz):
        wavelength_nm = SPEED_OF_LIGHT / frequency_hz * 1e9
        return f"可见光 - 波长约 {wavelength_nm:.0f} nm"
    elif is_radio_frequency(frequency_hz):
        band_code, band_name = get_radio_band(frequency_hz)
        return f"{band_code} ({band_name})"
    elif frequency_hz < 20:
        return "次声波范围"
    elif frequency_hz > 800e12:
        return "高频电磁波 (紫外/X射线/伽马射线等)"
    else:
        return "未知频率范围"


def format_frequency(frequency_hz: float, precision: int = 2) -> str:
    """
    格式化频率显示，自动选择合适的单位.
    
    Args:
        frequency_hz: 频率 (Hz)
        precision: 小数位数
    
    Returns:
        格式化的频率字符串
    
    Examples:
        >>> format_frequency(1000)
        '1.00 kHz'
        >>> format_frequency(1500000)
        '1.50 MHz'
    """
    if frequency_hz >= 1e12:
        return f"{frequency_hz / 1e12:.{precision}f} THz"
    elif frequency_hz >= 1e9:
        return f"{frequency_hz / 1e9:.{precision}f} GHz"
    elif frequency_hz >= 1e6:
        return f"{frequency_hz / 1e6:.{precision}f} MHz"
    elif frequency_hz >= 1e3:
        return f"{frequency_hz / 1e3:.{precision}f} kHz"
    elif frequency_hz >= 1:
        return f"{frequency_hz:.{precision}f} Hz"
    elif frequency_hz >= 1e-3:
        return f"{frequency_hz * 1e3:.{precision}f} mHz"
    elif frequency_hz >= 1e-6:
        return f"{frequency_hz * 1e6:.{precision}f} μHz"
    else:
        return f"{frequency_hz * 1e9:.{precision}f} nHz"


# ============================================================================
# Scale Generation Functions
# ============================================================================

def generate_chromatic_scale(
    start_note: str = 'C',
    start_octave: int = 4,
    num_notes: int = 12,
    a4_hz: float = STANDARD_A4
) -> List[Tuple[str, int, float]]:
    """
    生成半音阶.
    
    Args:
        start_note: 起始音符
        start_octave: 起始八度
        num_notes: 音符数量
        a4_hz: A4 参考频率
    
    Returns:
        [(音符名, 八度, 频率), ...]
    
    Examples:
        >>> scale = generate_chromatic_scale('C', 4, 3)
        >>> scale[0]
        ('C', 4, 261.63...)
    """
    # 获取起始 MIDI 音符
    start_midi = note_to_midi(start_note, start_octave)
    
    scale = []
    for i in range(num_notes):
        midi = start_midi + i
        freq = get_midi_frequency(midi, a4_hz)
        note_info = frequency_to_note(freq, a4_hz)
        scale.append((note_info.note_name, note_info.octave, round(freq, 2)))
    
    return scale


def note_to_midi(note: str, octave: int) -> int:
    """
    音符名称转 MIDI 编号.
    
    Args:
        note: 音符名称
        octave: 八度
    
    Returns:
        MIDI 音符编号
    
    Examples:
        >>> note_to_midi('A', 4)
        69
        >>> note_to_midi('C', 4)
        60
    """
    note = note.strip().upper()
    
    # 处理降号
    flat_to_sharp = {
        'DB': 'C#', 'EB': 'D#', 'FB': 'E', 'GB': 'F#',
        'AB': 'G#', 'BB': 'A#', 'CB': 'B'
    }
    
    if note in flat_to_sharp:
        note = flat_to_sharp[note]
    
    if note not in NOTE_NAMES:
        raise ValueError(f"未知的音符: {note}")
    
    semitone_offset = NOTE_NAMES.index(note)
    return 12 + octave * 12 + semitone_offset


def generate_major_scale(
    root_note: str,
    octave: int = 4,
    a4_hz: float = STANDARD_A4
) -> List[Tuple[str, int, float]]:
    """
    生成大调音阶.
    
    Args:
        root_note: 根音
        octave: 八度
        a4_hz: A4 参考频率
    
    Returns:
        [(音符名, 八度, 频率), ...]
    
    Examples:
        >>> scale = generate_major_scale('C', 4)
        >>> len(scale)
        8
    """
    # 大调音阶的半音间隔
    major_intervals = [0, 2, 4, 5, 7, 9, 11, 12]
    
    root_midi = note_to_midi(root_note, octave)
    
    scale = []
    for interval in major_intervals:
        midi = root_midi + interval
        freq = get_midi_frequency(midi, a4_hz)
        note_info = frequency_to_note(freq, a4_hz)
        scale.append((note_info.note_name, note_info.octave, round(freq, 2)))
    
    return scale


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Frequency Utilities Demo")
    print("=" * 60)
    
    # 频率单位转换
    print("\n--- 频率单位转换 ---")
    result = frequency_to_all(100, 'MHz')
    print(f"100 MHz = {result.hertz} Hz")
    print(f"         = {result.kilohertz} kHz")
    print(f"         = {result.gigahertz} GHz")
    print(f"周期: {result.period_seconds * 1e9:.2f} ns")
    
    # 频率与波长
    print("\n--- 频率与波长 ---")
    wl = get_wavelength_result(100e6)
    print(f"100 MHz 无线电波:")
    print(f"  波长: {wl.wavelength_m:.2f} m")
    print(f"  介质: {wl.medium}")
    
    wl_audio = get_wavelength_result(440, WaveMedium.AIR)
    print(f"\n440 Hz 声波 (A4):")
    print(f"  波长: {wl_audio.wavelength_m:.2f} m")
    print(f"  介质: {wl_audio.medium}")
    
    # 音符频率
    print("\n--- 音符频率 ---")
    print(f"A4 = {note_to_frequency('A', 4):.2f} Hz")
    print(f"C4 (中央C) = {note_to_frequency('C', 4):.2f} Hz")
    print(f"A#4 = {note_to_frequency('A#', 4):.2f} Hz")
    print(f"Db4 = {note_to_frequency('Db', 4):.2f} Hz")
    
    # 频率转音符
    print("\n--- 频率转音符 ---")
    note = frequency_to_note(466.16)
    print(f"466.16 Hz → {note.full_name} (MIDI: {note.midi_note})")
    
    note2 = frequency_to_note(261.63)
    print(f"261.63 Hz → {note2.full_name} (MIDI: {note2.midi_note})")
    
    # 音分计算
    print("\n--- 音分计算 ---")
    cents = get_cent_result(440, 880)
    print(f"440 Hz → 880 Hz: {cents.cents} 音分 = {cents.semitones} 半音 = {cents.octaves} 八度")
    
    cents2 = get_cent_result(440, 466.16)
    print(f"440 Hz → 466.16 Hz: {cents2.cents} 音分")
    
    # 谐波系列
    print("\n--- 谐波系列 (A4) ---")
    harmonics = get_note_harmonics(440, 8)
    print(f"基频: {harmonics.fundamental_hz} Hz")
    for n, freq, note_name in harmonics.harmonics:
        print(f"  {n}次谐波: {freq:.2f} Hz ({note_name})")
    
    # 无线电频段
    print("\n--- 无线电频段 ---")
    test_freqs = [100e3, 1e6, 100e6, 2.4e9, 5e9]
    for freq in test_freqs:
        band_code, band_name = get_radio_band(freq)
        print(f"{format_frequency(freq)}: {band_code} ({band_name})")
    
    # 大调音阶
    print("\n--- C 大调音阶 ---")
    scale = generate_major_scale('C', 4)
    for note_name, octave, freq in scale:
        print(f"  {note_name}{octave}: {freq:.2f} Hz")
    
    print("\n" + "=" * 60)