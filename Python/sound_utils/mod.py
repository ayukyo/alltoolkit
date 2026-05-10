"""
Sound Utilities - 声音与音频工具

A comprehensive toolkit for working with sound, music theory, and audio calculations.
Zero external dependencies - pure Python implementation.

Features:
- Frequency ↔ musical note conversion (with cents deviation)
- Wavelength and wave property calculations
- Decibel calculations (power, amplitude, SPL)
- BPM/tempo utilities for music production
- Audio sample and file size calculations
- Harmonic series generation
- Musical interval and chord frequency calculations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class NoteName(Enum):
    """音符名称枚举"""
    C = "C"
    C_SHARP = "C#"
    D = "D"
    D_SHARP = "D#"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G = "G"
    G_SHARP = "G#"
    A = "A"
    A_SHARP = "A#"
    B = "B"


# 标准音高定义
A4_FREQUENCY = 440.0  # A4 = 440 Hz (标准音高)

# 十二平均律半音频率比率
SEMITONE_RATIO = 2 ** (1 / 12)

# 音符名称列表（按半音顺序）
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 音符名称的替代写法映射
NOTE_ALIASES = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#',
    'C♯': 'C#', 'D♯': 'D#', 'F♯': 'F#', 'G♯': 'G#', 'A♯': 'A#',
    'D♭': 'C#', 'E♭': 'D#', 'G♭': 'F#', 'A♭': 'G#', 'B♭': 'A#',
}

# 声音在空气中的速度（20°C，海平面，约 343 m/s）
SPEED_OF_SOUND_AIR = 343.0

# 参考声压（0 dB SPL 的参考值）
REFERENCE_SOUND_PRESSURE = 20e-6  # 20 μPa（微帕）


@dataclass
class MusicalNote:
    """音符数据类"""
    name: str           # 音符名称 (C, C#, D, etc.)
    octave: int         # 八度 (0-8)
    frequency: float    # 频率 (Hz)
    midi_note: int      # MIDI 音符号 (0-127)
    wavelength: float   # 波长 (米)
    cents_deviation: float = 0.0  # 与精确频率的偏差（音分）


@dataclass
class AudioFileInfo:
    """音频文件信息"""
    sample_rate: int        # 采样率 (Hz)
    bit_depth: int          # 位深度 (bits)
    channels: int           # 声道数
    duration_seconds: float # 时长（秒）
    file_size_bytes: int    # 文件大小（字节）
    bit_rate: int           # 比特率 (bps)


# ==================== 频率与音符转换 ====================

def frequency_to_note(frequency: float, a4: float = A4_FREQUENCY) -> MusicalNote:
    """
    将频率转换为音符
    
    Args:
        frequency: 频率 (Hz)
        a4: A4 的参考频率 (默认 440 Hz)
    
    Returns:
        MusicalNote 对象
    
    Raises:
        ValueError: 如果频率无效
    
    Examples:
        >>> note = frequency_to_note(440.0)
        >>> note.name, note.octave
        ('A', 4)
        >>> note = frequency_to_note(261.63)  # Middle C
        >>> note.name, note.octave
        ('C', 4)
    """
    if frequency <= 0:
        raise ValueError("频率必须为正数")
    
    # 计算与 A4 的半音数
    semitones_from_a4 = 12 * math.log2(frequency / a4)
    
    # MIDI 音符号（A4 = 69）
    midi_note = round(69 + semitones_from_a4)
    
    # 限制 MIDI 范围
    midi_note = max(0, min(127, midi_note))
    
    # 计算精确频率的偏差（音分）
    exact_freq = midi_to_frequency(midi_note, a4)
    cents = 1200 * math.log2(frequency / exact_freq) if frequency > 0 else 0
    
    # 音符名称和八度
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    name = NOTE_NAMES[note_index]
    
    # 计算波长
    wavelength = speed_of_sound_to_wavelength(SPEED_OF_SOUND_AIR, frequency)
    
    return MusicalNote(
        name=name,
        octave=octave,
        frequency=exact_freq,
        midi_note=midi_note,
        wavelength=wavelength,
        cents_deviation=round(cents, 2)
    )


def note_to_frequency(note: str, octave: int = 4, a4: float = A4_FREQUENCY) -> float:
    """
    将音符转换为频率
    
    Args:
        note: 音符名称 (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
              也支持降号写法 (Db, Eb, Gb, Ab, Bb)
        octave: 八度 (默认 4)
        a4: A4 的参考频率 (默认 440 Hz)
    
    Returns:
        频率 (Hz)
    
    Raises:
        ValueError: 如果音符名称无效
    
    Examples:
        >>> note_to_frequency('A', 4)
        440.0
        >>> note_to_frequency('C', 4)  # Middle C
        261.6255653...
        >>> note_to_frequency('C#', 4)
        277.1826309...
    """
    # 处理降号别名
    note = NOTE_ALIASES.get(note, note)
    
    if note not in NOTE_NAMES:
        raise ValueError(f"无效的音符名称: {note}")
    
    note_index = NOTE_NAMES.index(note)
    
    # A4 = 69 (MIDI)
    # 公式: MIDI note = 12 * (octave + 1) + note_index
    # C4 = 60 (MIDI)
    midi_note = 12 * (octave + 1) + note_index
    
    # A4 的 MIDI 音符号 = 69
    # 半音数 = midi_note - 69
    semitones = midi_note - 69
    
    # 频率 = A4 * 2^(semitones/12)
    frequency = a4 * (2 ** (semitones / 12))
    
    return frequency


def midi_to_frequency(midi_note: int, a4: float = A4_FREQUENCY) -> float:
    """
    将 MIDI 音符号转换为频率
    
    Args:
        midi_note: MIDI 音符号 (0-127)
        a4: A4 的参考频率 (默认 440 Hz)
    
    Returns:
        频率 (Hz)
    
    Raises:
        ValueError: 如果 MIDI 音符号超出范围
    
    Examples:
        >>> midi_to_frequency(69)  # A4
        440.0
        >>> midi_to_frequency(60)  # C4 (Middle C)
        261.6255653...
    """
    if not 0 <= midi_note <= 127:
        raise ValueError("MIDI 音符号必须在 0-127 范围内")
    
    return a4 * (2 ** ((midi_note - 69) / 12))


def frequency_to_midi(frequency: float, a4: float = A4_FREQUENCY) -> int:
    """
    将频率转换为最近的 MIDI 音符号
    
    Args:
        frequency: 频率 (Hz)
        a4: A4 的参考频率 (默认 440 Hz)
    
    Returns:
        MIDI 音符号 (0-127)
    
    Raises:
        ValueError: 如果频率无效
    
    Examples:
        >>> frequency_to_midi(440.0)
        69
        >>> frequency_to_midi(261.63)
        60
    """
    if frequency <= 0:
        raise ValueError("频率必须为正数")
    
    midi_float = 69 + 12 * math.log2(frequency / a4)
    return max(0, min(127, round(midi_float)))


# ==================== 波长计算 ====================

def speed_of_sound_to_wavelength(speed: float, frequency: float) -> float:
    """
    根据声速和频率计算波长
    
    Args:
        speed: 声速 (m/s)
        frequency: 频率 (Hz)
    
    Returns:
        波长 (m)
    
    Examples:
        >>> speed_of_sound_to_wavelength(343, 440)
        0.7795454...
    """
    if frequency <= 0:
        raise ValueError("频率必须为正数")
    return speed / frequency


def wavelength_to_frequency(speed: float, wavelength: float) -> float:
    """
    根据声速和波长计算频率
    
    Args:
        speed: 声速 (m/s)
        wavelength: 波长 (m)
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> wavelength_to_frequency(343, 0.78)
        439.7435...
    """
    if wavelength <= 0:
        raise ValueError("波长必须为正数")
    return speed / wavelength


def speed_of_sound_temperature(temperature_celsius: float = 20.0) -> float:
    """
    根据温度计算空气中的声速
    
    Args:
        temperature_celsius: 温度（摄氏度）
    
    Returns:
        声速 (m/s)
    
    Examples:
        >>> speed_of_sound_temperature(20)
        343.2
        >>> speed_of_sound_temperature(0)
        331.3
    """
    # 公式: v = 331.3 + 0.606 * T
    return 331.3 + 0.606 * temperature_celsius


# ==================== 分贝计算 ====================

def power_ratio_to_decibels(power_ratio: float) -> float:
    """
    将功率比转换为分贝
    
    公式: dB = 10 * log10(P1/P0)
    
    Args:
        power_ratio: 功率比 (P1/P0)
    
    Returns:
        分贝值
    
    Examples:
        >>> power_ratio_to_decibels(10)
        10.0
        >>> power_ratio_to_decibels(2)
        3.0102...
    """
    if power_ratio <= 0:
        raise ValueError("功率比必须为正数")
    return 10 * math.log10(power_ratio)


def decibels_to_power_ratio(decibels: float) -> float:
    """
    将分贝转换为功率比
    
    公式: ratio = 10^(dB/10)
    
    Args:
        decibels: 分贝值
    
    Returns:
        功率比
    
    Examples:
        >>> decibels_to_power_ratio(10)
        10.0
        >>> decibels_to_power_ratio(3)
        1.9952...
    """
    return 10 ** (decibels / 10)


def amplitude_ratio_to_decibels(amplitude_ratio: float) -> float:
    """
    将振幅比转换为分贝
    
    公式: dB = 20 * log10(A1/A0)
    
    Args:
        amplitude_ratio: 振幅比 (A1/A0)
    
    Returns:
        分贝值
    
    Examples:
        >>> amplitude_ratio_to_decibels(10)
        20.0
        >>> amplitude_ratio_to_decibels(2)
        6.0205...
    """
    if amplitude_ratio <= 0:
        raise ValueError("振幅比必须为正数")
    return 20 * math.log10(amplitude_ratio)


def decibels_to_amplitude_ratio(decibels: float) -> float:
    """
    将分贝转换为振幅比
    
    公式: ratio = 10^(dB/20)
    
    Args:
        decibels: 分贝值
    
    Returns:
        振幅比
    
    Examples:
        >>> decibels_to_amplitude_ratio(20)
        10.0
        >>> decibels_to_amplitude_ratio(6)
        1.9952...
    """
    return 10 ** (decibels / 20)


def sound_pressure_to_spl(pressure: float, reference: float = REFERENCE_SOUND_PRESSURE) -> float:
    """
    将声压转换为声压级（SPL）
    
    公式: SPL = 20 * log10(P / P0)
    
    Args:
        pressure: 声压 (Pa)
        reference: 参考声压 (默认 20 μPa)
    
    Returns:
        声压级 (dB SPL)
    
    Examples:
        >>> sound_pressure_to_spl(20e-6)
        0.0
        >>> sound_pressure_to_spl(1)  # 1 Pascal
        93.9794...
    """
    if pressure <= 0:
        raise ValueError("声压必须为正数")
    return 20 * math.log10(pressure / reference)


def spl_to_sound_pressure(spl: float, reference: float = REFERENCE_SOUND_PRESSURE) -> float:
    """
    将声压级转换为声压
    
    公式: P = P0 * 10^(SPL/20)
    
    Args:
        spl: 声压级 (dB SPL)
        reference: 参考声压 (默认 20 μPa)
    
    Returns:
        声压 (Pa)
    
    Examples:
        >>> spl_to_sound_pressure(0)
        2e-05
        >>> spl_to_sound_pressure(94)  # ~1 Pascal
        1.000...
    """
    return reference * (10 ** (spl / 20))


def combine_decibels(decibels_list: List[float]) -> float:
    """
    合并多个分贝值（非相干声源）
    
    公式: 总dB = 10 * log10(sum(10^(dB/10)))
    
    Args:
        decibels_list: 分贝值列表
    
    Returns:
        合并后的分贝值
    
    Examples:
        >>> combine_decibels([60, 60])
        63.0102...
        >>> combine_decibels([60, 60, 60])
        64.7712...
    """
    if not decibels_list:
        return 0.0
    
    total_power = sum(10 ** (db / 10) for db in decibels_list)
    return 10 * math.log10(total_power)


# ==================== BPM 与时间计算 ====================

def bpm_to_beat_duration_ms(bpm: float) -> float:
    """
    将 BPM 转换为每拍时长（毫秒）
    
    Args:
        bpm: 每分钟节拍数
    
    Returns:
        每拍时长 (ms)
    
    Examples:
        >>> bpm_to_beat_duration_ms(120)
        500.0
        >>> bpm_to_beat_duration_ms(60)
        1000.0
    """
    if bpm <= 0:
        raise ValueError("BPM 必须为正数")
    return 60000.0 / bpm


def beat_duration_to_bpm(duration_ms: float) -> float:
    """
    将每拍时长转换为 BPM
    
    Args:
        duration_ms: 每拍时长 (ms)
    
    Returns:
        BPM
    
    Examples:
        >>> beat_duration_to_bpm(500)
        120.0
        >>> beat_duration_to_bpm(1000)
        60.0
    """
    if duration_ms <= 0:
        raise ValueError("时长必须为正数")
    return 60000.0 / duration_ms


def bpm_to_note_duration(bpm: float, note_type: str = "quarter") -> float:
    """
    将 BPM 转换为指定音符类型的时长（毫秒）
    
    Args:
        bpm: 每分钟节拍数（四分音符 BPM）
        note_type: 音符类型
    
    Returns:
        音符时长 (ms)
    
    Examples:
        >>> bpm_to_note_duration(120, "quarter")
        500.0
        >>> bpm_to_note_duration(120, "eighth")
        250.0
        >>> bpm_to_note_duration(120, "half")
        1000.0
    """
    quarter_note_ms = bpm_to_beat_duration_ms(bpm)
    
    note_ratios = {
        "whole": 4.0,
        "half": 2.0,
        "quarter": 1.0,
        "eighth": 0.5,
        "sixteenth": 0.25,
        "thirty_second": 0.125,
        "sixty_fourth": 0.0625,
        # 中文别名
        "全音符": 4.0,
        "二分": 2.0,
        "四分": 1.0,
        "八分": 0.5,
        "十六分": 0.25,
        "三十二分": 0.125,
        "六十四分": 0.0625,
    }
    
    if note_type.lower() not in {k.lower() for k in note_ratios}:
        raise ValueError(f"无效的音符类型: {note_type}")
    
    ratio = None
    for k, v in note_ratios.items():
        if k.lower() == note_type.lower():
            ratio = v
            break
    
    return quarter_note_ms * ratio


def bpm_to_measure_duration(bpm: float, time_signature: str = "4/4") -> float:
    """
    将 BPM 转换为小节时长（毫秒）
    
    Args:
        bpm: 每分钟节拍数
        time_signature: 拍号 (如 "4/4", "3/4", "6/8")
    
    Returns:
        小节时长 (ms)
    
    Examples:
        >>> bpm_to_measure_duration(120, "4/4")
        2000.0
        >>> bpm_to_measure_duration(120, "3/4")
        1500.0
    """
    quarter_note_ms = bpm_to_beat_duration_ms(bpm)
    
    try:
        beats_per_measure, beat_unit = time_signature.split("/")
        beats_per_measure = int(beats_per_measure)
        beat_unit = int(beat_unit)
    except ValueError:
        raise ValueError(f"无效的拍号格式: {time_signature}")
    
    # 计算一个拍子的长度相对于四分音符
    beat_ratio = 4 / beat_unit
    
    return quarter_note_ms * beat_ratio * beats_per_measure


def calculate_delay_time_ms(bpm: float, subdivision: str = "quarter") -> float:
    """
    计算延迟时间（毫秒）以同步 BPM
    
    Args:
        bpm: 每分钟节拍数
        subdivision: 节拍细分
    
    Returns:
        延迟时间 (ms)
    
    Examples:
        >>> calculate_delay_time_ms(120, "quarter")
        500.0
        >>> calculate_delay_time_ms(120, "eighth")
        250.0
        >>> calculate_delay_time_ms(120, "dotted_eighth")
        375.0
    """
    quarter_note_ms = bpm_to_beat_duration_ms(bpm)
    
    subdivisions = {
        "whole": 4.0,
        "half": 2.0,
        "quarter": 1.0,
        "eighth": 0.5,
        "sixteenth": 0.25,
        "thirty_second": 0.125,
        "dotted_half": 3.0,
        "dotted_quarter": 1.5,
        "dotted_eighth": 0.75,
        "dotted_sixteenth": 0.375,
        "triplet_half": 4.0 / 3.0,
        "triplet_quarter": 2.0 / 3.0,
        "triplet_eighth": 1.0 / 3.0,
    }
    
    if subdivision.lower() not in {k.lower() for k in subdivisions}:
        raise ValueError(f"无效的细分类型: {subdivision}")
    
    ratio = None
    for k, v in subdivisions.items():
        if k.lower() == subdivision.lower():
            ratio = v
            break
    
    return quarter_note_ms * ratio


# ==================== 音频采样计算 ====================

def calculate_audio_file_size(
    duration_seconds: float,
    sample_rate: int,
    bit_depth: int,
    channels: int = 1
) -> int:
    """
    计算未压缩音频文件大小
    
    Args:
        duration_seconds: 时长（秒）
        sample_rate: 采样率 (Hz)
        bit_depth: 位深度 (bits)
        channels: 声道数
    
    Returns:
        文件大小（字节）
    
    Examples:
        >>> calculate_audio_file_size(60, 44100, 16, 2)
        10584000
        >>> calculate_audio_file_size(180, 48000, 24, 2)  # 3分钟 48kHz 24bit 立体声
        51840000
    """
    return int(duration_seconds * sample_rate * (bit_depth / 8) * channels)


def calculate_audio_duration(
    file_size_bytes: int,
    sample_rate: int,
    bit_depth: int,
    channels: int = 1
) -> float:
    """
    根据文件大小计算音频时长
    
    Args:
        file_size_bytes: 文件大小（字节）
        sample_rate: 采样率 (Hz)
        bit_depth: 位深度 (bits)
        channels: 声道数
    
    Returns:
        时长（秒）
    
    Examples:
        >>> calculate_audio_duration(10584000, 44100, 16, 2)
        60.0
    """
    bytes_per_second = sample_rate * (bit_depth / 8) * channels
    if bytes_per_second == 0:
        raise ValueError("无效的音频参数")
    return file_size_bytes / bytes_per_second


def calculate_bit_rate(sample_rate: int, bit_depth: int, channels: int = 1) -> int:
    """
    计算音频比特率
    
    Args:
        sample_rate: 采样率 (Hz)
        bit_depth: 位深度 (bits)
        channels: 声道数
    
    Returns:
        比特率 (bps)
    
    Examples:
        >>> calculate_bit_rate(44100, 16, 2)
        1411200
        >>> calculate_bit_rate(48000, 24, 2)
        2304000
    """
    return sample_rate * bit_depth * channels


def get_audio_info(
    duration_seconds: float,
    sample_rate: int,
    bit_depth: int,
    channels: int = 1
) -> AudioFileInfo:
    """
    获取音频文件完整信息
    
    Args:
        duration_seconds: 时长（秒）
        sample_rate: 采样率 (Hz)
        bit_depth: 位深度 (bits)
        channels: 声道数
    
    Returns:
        AudioFileInfo 对象
    
    Examples:
        >>> info = get_audio_info(60, 44100, 16, 2)
        >>> info.bit_rate
        1411200
    """
    file_size = calculate_audio_file_size(duration_seconds, sample_rate, bit_depth, channels)
    bit_rate = calculate_bit_rate(sample_rate, bit_depth, channels)
    
    return AudioFileInfo(
        sample_rate=sample_rate,
        bit_depth=bit_depth,
        channels=channels,
        duration_seconds=duration_seconds,
        file_size_bytes=file_size,
        bit_rate=bit_rate
    )


def samples_to_milliseconds(samples: int, sample_rate: int) -> float:
    """
    将采样数转换为毫秒
    
    Args:
        samples: 采样数
        sample_rate: 采样率 (Hz)
    
    Returns:
        毫秒数
    
    Examples:
        >>> samples_to_milliseconds(44100, 44100)
        1000.0
        >>> samples_to_milliseconds(512, 44100)
        11.6099...
    """
    if sample_rate <= 0:
        raise ValueError("采样率必须为正数")
    return (samples / sample_rate) * 1000


def milliseconds_to_samples(ms: float, sample_rate: int) -> int:
    """
    将毫秒转换为采样数
    
    Args:
        ms: 毫秒数
        sample_rate: 采样率 (Hz)
    
    Returns:
        采样数
    
    Examples:
        >>> milliseconds_to_samples(1000, 44100)
        44100
        >>> milliseconds_to_samples(500, 48000)
        24000
    """
    if sample_rate <= 0:
        raise ValueError("采样率必须为正数")
    return int((ms / 1000) * sample_rate)


# ==================== 泛音系列 ====================

def generate_harmonics(fundamental: float, num_harmonics: int = 10) -> List[Tuple[int, float, str]]:
    """
    生成泛音系列
    
    Args:
        fundamental: 基频 (Hz)
        num_harmonics: 泛音数量
    
    Returns:
        列表，每项为 (泛音序号, 频率, 音符名称)
    
    Examples:
        >>> harmonics = generate_harmonics(440, 5)
        >>> harmonics[0]
        (1, 440.0, 'A4')
        >>> harmonics[1]
        (2, 880.0, 'A5')
    """
    if fundamental <= 0:
        raise ValueError("基频必须为正数")
    
    harmonics = []
    for n in range(1, num_harmonics + 1):
        freq = fundamental * n
        note = frequency_to_note(freq)
        note_name = f"{note.name}{note.octave}"
        harmonics.append((n, round(freq, 2), note_name))
    
    return harmonics


def generate_overtones_series(base_frequency: float, series_type: str = "harmonic") -> List[float]:
    """
    生成泛音系列
    
    Args:
        base_frequency: 基频 (Hz)
        series_type: 泛音系列类型
            - "harmonic": 谐波系列 (1f, 2f, 3f, ...)
            - "odd": 奇次谐波 (1f, 3f, 5f, ...)
            - "even": 偶次谐波 (2f, 4f, 6f, ...)
    
    Returns:
        频率列表
    
    Examples:
        >>> generate_overtones_series(100, "harmonic")[:5]
        [100.0, 200.0, 300.0, 400.0, 500.0]
        >>> generate_overtones_series(100, "odd")[:5]
        [100.0, 300.0, 500.0, 700.0, 900.0]
    """
    if base_frequency <= 0:
        raise ValueError("基频必须为正数")
    
    harmonics = []
    
    if series_type == "harmonic":
        for n in range(1, 11):
            harmonics.append(base_frequency * n)
    elif series_type == "odd":
        for n in range(1, 11):
            harmonics.append(base_frequency * (2 * n - 1))
    elif series_type == "even":
        for n in range(1, 11):
            harmonics.append(base_frequency * 2 * n)
    else:
        raise ValueError(f"无效的泛音系列类型: {series_type}")
    
    return harmonics


# ==================== 音程与和弦 ====================

# 音程名称映射（半音数 -> 音程名）
INTERVAL_NAMES = {
    0: "纯一度 (P1)",
    1: "小二度 (m2)",
    2: "大二度 (M2)",
    3: "小三度 (m3)",
    4: "大三度 (M3)",
    5: "纯四度 (P4)",
    6: "增四度/减五度 (A4/d5)",
    7: "纯五度 (P5)",
    8: "小六度 (m6)",
    9: "大六度 (M6)",
    10: "小七度 (m7)",
    11: "大七度 (M7)",
    12: "纯八度 (P8)",
}

# 和弦公式（相对于根音的半音数）
CHORD_FORMULAS = {
    "major": [0, 4, 7],               # 大三和弦
    "minor": [0, 3, 7],               # 小三和弦
    "diminished": [0, 3, 6],          # 减三和弦
    "augmented": [0, 4, 8],           # 增三和弦
    "sus2": [0, 2, 7],                # 挂二和弦
    "sus4": [0, 5, 7],                # 挂四和弦
    "major7": [0, 4, 7, 11],          # 大七和弦
    "minor7": [0, 3, 7, 10],          # 小七和弦
    "dominant7": [0, 4, 7, 10],       # 属七和弦
    "diminished7": [0, 3, 6, 9],      # 减七和弦
    "half_diminished7": [0, 3, 6, 10], # 半减七和弦
    "minor_major7": [0, 3, 7, 11],    # 小大七和弦
    "augmented7": [0, 4, 8, 10],      # 增七和弦
    "power": [0, 7],                  # 强力和弦 (5)
    "add9": [0, 4, 7, 14],            # add9
    "major9": [0, 4, 7, 11, 14],      # 大九和弦
    "minor9": [0, 3, 7, 10, 14],      # 小九和弦
}


def calculate_interval(frequency1: float, frequency2: float) -> Tuple[int, str, float]:
    """
    计算两个频率之间的音程
    
    Args:
        frequency1: 第一个频率 (Hz)
        frequency2: 第二个频率 (Hz)
    
    Returns:
        (半音数, 音程名称, 频率比)
    
    Examples:
        >>> calculate_interval(261.63, 329.63)  # C4 to E4
        (4, '大三度 (M3)', 1.2599...)
        >>> calculate_interval(261.63, 523.25)  # C4 to C5
        (12, '纯八度 (P8)', 2.0)
    """
    if frequency1 <= 0 or frequency2 <= 0:
        raise ValueError("频率必须为正数")
    
    # 计算半音数
    semitones = round(12 * math.log2(frequency2 / frequency1))
    semitones = semitones % 12  # 归一化到八度内
    
    # 获取音程名称
    interval_name = INTERVAL_NAMES.get(semitones, f"{semitones}半音")
    
    # 计算频率比
    ratio = frequency2 / frequency1
    
    return semitones, interval_name, round(ratio, 4)


def generate_chord_frequencies(
    root_note: str,
    octave: int = 4,
    chord_type: str = "major",
    a4: float = A4_FREQUENCY
) -> Dict[str, float]:
    """
    生成和弦中各音的频率
    
    Args:
        root_note: 根音名称
        octave: 根音八度
        chord_type: 和弦类型
        a4: A4 参考频率
    
    Returns:
        {音符名称: 频率} 字典
    
    Raises:
        ValueError: 如果和弦类型未知
    
    Examples:
        >>> chord = generate_chord_frequencies('C', 4, 'major')
        >>> list(chord.keys())
        ['C4', 'E4', 'G4']
        >>> chord = generate_chord_frequencies('A', 4, 'minor7')
        >>> list(chord.keys())
        ['A4', 'C5', 'E5', 'G5']
    """
    if chord_type not in CHORD_FORMULAS:
        raise ValueError(f"未知和弦类型: {chord_type}。可用: {list(CHORD_FORMULAS.keys())}")
    
    # 处理降号别名
    root_note = NOTE_ALIASES.get(root_note, root_note)
    
    if root_note not in NOTE_NAMES:
        raise ValueError(f"无效的音符名称: {root_note}")
    
    root_index = NOTE_NAMES.index(root_note)
    formula = CHORD_FORMULAS[chord_type]
    
    chord = {}
    for semitones in formula:
        # 计算音符索引和八度
        total_semitones = root_index + semitones
        note_index = total_semitones % 12
        note_octave = octave + total_semitones // 12
        
        note_name = NOTE_NAMES[note_index]
        frequency = note_to_frequency(note_name, note_octave, a4)
        
        chord[f"{note_name}{note_octave}"] = round(frequency, 2)
    
    return chord


def get_scale_notes(root_note: str, scale_type: str = "major") -> List[str]:
    """
    获取音阶中的音符
    
    Args:
        root_note: 根音
        scale_type: 音阶类型
    
    Returns:
        音符名称列表
    
    Examples:
        >>> get_scale_notes('C', 'major')
        ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        >>> get_scale_notes('A', 'minor')
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    """
    # 音阶公式（半音间隔）
    SCALE_FORMULAS = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "natural_minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
        "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10],
        # 中文名称
        "大调": [0, 2, 4, 5, 7, 9, 11],
        "小调": [0, 2, 3, 5, 7, 8, 10],
        "自然小调": [0, 2, 3, 5, 7, 8, 10],
        "和声小调": [0, 2, 3, 5, 7, 8, 11],
        "旋律小调": [0, 2, 3, 5, 7, 9, 11],
        "五声音阶": [0, 2, 4, 7, 9],
        "蓝调": [0, 3, 5, 6, 7, 10],
    }
    
    if scale_type not in SCALE_FORMULAS:
        raise ValueError(f"未知音阶类型: {scale_type}。可用: {list(SCALE_FORMULAS.keys())}")
    
    # 处理降号别名
    root_note = NOTE_ALIASES.get(root_note, root_note)
    
    if root_note not in NOTE_NAMES:
        raise ValueError(f"无效的音符名称: {root_note}")
    
    root_index = NOTE_NAMES.index(root_note)
    formula = SCALE_FORMULAS[scale_type]
    
    notes = []
    for semitones in formula:
        note_index = (root_index + semitones) % 12
        notes.append(NOTE_NAMES[note_index])
    
    return notes


def transpose_frequency(frequency: float, semitones: int) -> float:
    """
    移调（改变频率）
    
    Args:
        frequency: 原频率 (Hz)
        semitones: 移动的半音数（正数为升高，负数为降低）
    
    Returns:
        移调后的频率 (Hz)
    
    Examples:
        >>> transpose_frequency(440.0, 12)  # 升高一个八度
        880.0
        >>> transpose_frequency(440.0, -12)  # 降低一个八度
        220.0
        >>> transpose_frequency(440.0, 7)  # 升高纯五度
        659.255...
    """
    if frequency <= 0:
        raise ValueError("频率必须为正数")
    
    return frequency * (SEMITONE_RATIO ** semitones)


def cents_to_frequency_ratio(cents: float) -> float:
    """
    将音分转换为频率比
    
    Args:
        cents: 音分数
    
    Returns:
        频率比
    
    Examples:
        >>> cents_to_frequency_ratio(1200)  # 1200音分 = 一个八度
        2.0
        >>> cents_to_frequency_ratio(100)  # 100音分 = 一个半音
        1.0594...
    """
    return 2 ** (cents / 1200)


def frequency_ratio_to_cents(ratio: float) -> float:
    """
    将频率比转换为音分
    
    Args:
        ratio: 频率比
    
    Returns:
        音分数
    
    Examples:
        >>> frequency_ratio_to_cents(2.0)  # 一个八度
        1200.0
        >>> frequency_ratio_to_cents(1.5)  # 纯五度
        701.955...
    """
    if ratio <= 0:
        raise ValueError("频率比必须为正数")
    
    return 1200 * math.log2(ratio)


# ==================== 常用参考值 ====================

# 常见频率参考表
COMMON_FREQUENCIES: Dict[str, float] = {
    # 音符参考
    "C0": 16.35,
    "A4": 440.0,
    "C4": 261.63,  # 中央C
    "C5": 523.25,
    "C8": 4186.01,  # 钢琴最高音
    
    # 人声范围
    "bass_low": 82.41,     # 男低音最低 E2
    "bass_high": 349.23,   # 男低音最高 F4
    "tenor_low": 130.81,   # 男高音最低 C3
    "tenor_high": 493.88,  # 男高音最高 B4
    "alto_low": 174.61,    # 女中音最低 F3
    "alto_high": 659.26,   # 女中音最高 E5
    "soprano_low": 261.63, # 女高音最低 C4
    "soprano_high": 1046.5, # 女高音最高 C6
    
    # 乐器范围
    "piano_low": 27.5,      # 钢琴最低 A0
    "piano_high": 4186.01,  # 钢琴最高 C8
    "guitar_low": 82.41,    # 吉他最低 E2
    "guitar_high": 1318.51, # 吉他最高 E6
    "violin_low": 196.0,    # 小提琴最低 G3
    "violin_high": 3135.96, # 小提琴最高 G7
    
    # 工程参考
    "acoustic_guitar": 100.0,  # 木吉他共振峰
    "kick_drum": 60.0,         # 底鼓
    "snare_drum": 200.0,       # 军鼓
    "hi_hat": 8000.0,          # 踩镲
    "bass_guitar": 80.0,       # 贝斯
}

# 常见采样率
SAMPLE_RATES: Dict[str, int] = {
    "telephone": 8000,
    "voice_chat": 16000,
    "cd_quality": 44100,
    "dvd_quality": 48000,
    "studio_quality": 96000,
    "high_resolution": 192000,
    "professional": 384000,
}

# 常见比特率
BIT_DEPTHS: Dict[str, int] = {
    "8bit": 8,
    "16bit": 16,  # CD 标准
    "24bit": 24,  # 专业音频
    "32bit": 32,  # 高精度
    "32bit_float": 32,  # 浮点
}

# 常见声压级参考
SPL_REFERENCE: Dict[str, float] = {
    "threshold_of_hearing": 0.0,       # 听觉阈值
    "rustling_leaves": 10.0,          # 树叶沙沙声
    "whisper": 30.0,                  # 耳语
    "quiet_library": 40.0,            # 安静图书馆
    "normal_conversation": 60.0,      # 正常交谈
    "busy_street": 80.0,              # 繁忙街道
    "factory_noise": 90.0,            # 工厂噪音
    "motorcycle": 100.0,              # 摩托车
    "chainsaw": 110.0,                # 电锯
    "rock_concert": 120.0,            # 摇滚演唱会
    "jet_engine": 140.0,              # 喷气引擎
    "threshold_of_pain": 130.0,       # 疼痛阈值
    "gunshot": 160.0,                 # 枪声
}


if __name__ == "__main__":
    # 示例用法
    print("=" * 60)
    print("声音与音频工具 - 示例")
    print("=" * 60)
    
    # 1. 频率与音符转换
    print("\n1. 频率与音符转换:")
    note = frequency_to_note(440.0)
    print(f"  440 Hz -> {note.name}{note.octave} (MIDI: {note.midi_note})")
    
    freq = note_to_frequency("A", 4)
    print(f"  A4 -> {freq} Hz")
    
    # 2. 波长计算
    print("\n2. 波长计算:")
    wavelength = speed_of_sound_to_wavelength(343, 440)
    print(f"  440 Hz 在空气中的波长: {wavelength:.4f} 米")
    
    # 3. 分贝计算
    print("\n3. 分贝计算:")
    db = power_ratio_to_decibels(10)
    print(f"  功率比 10 -> {db} dB")
    
    combined = combine_decibels([60, 60, 60])
    print(f"  三个 60 dB 声源合并: {combined:.2f} dB")
    
    # 4. BPM 计算
    print("\n4. BPM 与时间计算:")
    beat_ms = bpm_to_beat_duration_ms(120)
    print(f"  120 BPM 每拍时长: {beat_ms} ms")
    
    eighth_ms = bpm_to_note_duration(120, "eighth")
    print(f"  120 BPM 八分音符时长: {eighth_ms} ms")
    
    # 5. 音频文件计算
    print("\n5. 音频文件计算:")
    file_size = calculate_audio_file_size(180, 44100, 16, 2)
    print(f"  3分钟 CD 质量 (44.1kHz, 16bit, 立体声): {file_size / 1024 / 1024:.2f} MB")
    
    # 6. 泛音系列
    print("\n6. A4 的前 10 个泛音:")
    harmonics = generate_harmonics(440, 10)
    for n, freq, note_name in harmonics:
        print(f"  {n}次泛音: {freq:.1f} Hz ({note_name})")
    
    # 7. 和弦频率
    print("\n7. C 大三和弦频率:")
    chord = generate_chord_frequencies("C", 4, "major")
    for note, freq in chord.items():
        print(f"  {note}: {freq} Hz")
    
    # 8. 音阶
    print("\n8. C 大调音阶:")
    scale = get_scale_notes("C", "major")
    print(f"  {' - '.join(scale)}")
    
    print("\n9. 音程计算:")
    semitones, name, ratio = calculate_interval(261.63, 329.63)
    print(f"  C4 到 E4: {semitones} 半音, {name}, 比值 {ratio}")