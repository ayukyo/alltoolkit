"""
Musical Scale Utils - 音乐音阶与和弦理论工具库

零依赖的音乐理论库，支持：
- 音阶生成（大调、小调、五声音阶、蓝调音阶、日本音阶等 20+ 种音阶）
- 和弦构建（三和弦、七和弦、九和弦、十一和弦、十三和弦）
- 音程计算与识别
- 调性关系分析（近关系调、远关系调）
- 调号计算
- MIDI 音符编号转换
- 频率计算（A4=440Hz 标准）
- 节拍与节奏分析

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math


class NoteName(Enum):
    """音符名称"""
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


class ScaleType(Enum):
    """音阶类型"""
    # 常用音阶
    MAJOR = "major"                      # 自然大调
    MINOR_NATURAL = "natural_minor"      # 自然小调
    MINOR_HARMONIC = "harmonic_minor"    # 和声小调
    MINOR_MELODIC = "melodic_minor"      # 旋律小调（上行）
    
    # 五声音阶
    PENTATONIC_MAJOR = "pentatonic_major"      # 大调五声
    PENTATONIC_MINOR = "pentatonic_minor"      # 小调五声
    PENTATONIC_BLUES = "blues"                  # 蓝调音阶
    
    # 调式音阶（教会调式）
    DORIAN = "dorian"          # 多利亚调式
    PHRYGIAN = "phrygian"      # 弗里吉亚调式
    LYDIAN = "lydian"          # 利底亚调式
    MIXOLYDIAN = "mixolydian"  # 混合利底亚调式
    LOCRIAN = "locrian"        # 洛克里亚调式
    
    # 其他音阶
    CHROMATIC = "chromatic"    # 半音阶
    WHOLE_TONE = "whole_tone"  # 全音阶
    
    # 日本音阶
    JAPANESE_YO = "yo_scale"         # 阳音阶
    JAPANESE_IN = "in_scale"         # 阴音阶
    JAPANESE_HIRAJOSHI = "hirajoshi" # 平调子音阶
    
    # 特殊音阶
    DIMINISHED = "diminished"        # 减音阶
    AUGMENTED = "augmented"          # 增音阶
    BEBOP_MAJOR = "bebop_major"      # 贝波大调
    GYPSY_MINOR = "gypsy_minor"      # 吉普赛小调
    NEAPOLITAN_MINOR = "neapolitan_minor"  # 那不勒斯小调


class ChordType(Enum):
    """和弦类型"""
    # 三和弦
    MAJOR_TRIAD = "major"
    MINOR_TRIAD = "minor"
    AUGMENTED_TRIAD = "augmented"
    DIMINISHED_TRIAD = "diminished"
    
    # 七和弦
    MAJOR_7 = "maj7"
    MINOR_7 = "min7"
    DOMINANT_7 = "7"
    DIMINISHED_7 = "dim7"
    HALF_DIMINISHED_7 = "m7b5"
    AUGMENTED_7 = "aug7"
    MINOR_MAJOR_7 = "mMaj7"
    
    # 扩展和弦
    MAJOR_9 = "maj9"
    MINOR_9 = "min9"
    DOMINANT_9 = "9"
    MAJOR_11 = "maj11"
    MINOR_11 = "min11"
    DOMINANT_11 = "11"
    MAJOR_13 = "maj13"
    MINOR_13 = "min13"
    DOMINANT_13 = "13"
    
    # 挂留和弦
    SUS_2 = "sus2"
    SUS_4 = "sus4"
    SUS_2_7 = "sus2_7"
    SUS_4_7 = "sus4_7"
    
    # 加音和弦
    ADD_9 = "add9"
    ADD_11 = "add11"
    ADD_2 = "add2"


class Interval(Enum):
    """音程"""
    UNISON = "P1"              # 纯一度 (0 半音)
    MINOR_SECOND = "m2"        # 小二度 (1 半音)
    MAJOR_SECOND = "M2"        # 大二度 (2 半音)
    MINOR_THIRD = "m3"         # 小三度 (3 半音)
    MAJOR_THIRD = "M3"         # 大三度 (4 半音)
    PERFECT_FOURTH = "P4"      # 纯四度 (5 半音)
    AUGMENTED_FOURTH = "A4"    # 增四度 (6 半音)
    DIMINISHED_FIFTH = "d5"    # 减五度 (6 半音)
    PERFECT_FIFTH = "P5"       # 纯五度 (7 半音)
    AUGMENTED_FIFTH = "A5"     # 增五度 (8 半音)
    MINOR_SIXTH = "m6"         # 小六度 (8 半音)
    MAJOR_SIXTH = "M6"         # 大六度 (9 半音)
    DIMINISHED_SEVENTH = "d7"  # 减七度 (9 半音)
    MINOR_SEVENTH = "m7"       # 小七度 (10 半音)
    MAJOR_SEVENTH = "M7"       # 大七度 (11 半音)
    PERFECT_OCTAVE = "P8"      # 纯八度 (12 半音)
    MINOR_NINTH = "m9"         # 小九度 (13 半音)
    MAJOR_NINTH = "M9"         # 大九度 (14 半音)
    MINOR_TENTH = "m10"        # 小十度 (15 半音)
    MAJOR_TENTH = "M10"        # 大十度 (16 半音)
    PERFECT_ELEVENTH = "P11"   # 纯十一度 (17 半音)
    AUGMENTED_ELEVENTH = "A11" # 增十一度 (18 半音)
    PERFECT_TWELFTH = "P12"    # 纯十二度 (19 半音)
    MINOR_THIRTEENTH = "m13"   # 小十三度 (20 半音)
    MAJOR_THIRTEENTH = "M13"   # 大十三度 (21 半音)


# 音程半音数映射
INTERVAL_SEMITONES = {
    Interval.UNISON: 0,
    Interval.MINOR_SECOND: 1,
    Interval.MAJOR_SECOND: 2,
    Interval.MINOR_THIRD: 3,
    Interval.MAJOR_THIRD: 4,
    Interval.PERFECT_FOURTH: 5,
    Interval.AUGMENTED_FOURTH: 6,
    Interval.DIMINISHED_FIFTH: 6,
    Interval.PERFECT_FIFTH: 7,
    Interval.AUGMENTED_FIFTH: 8,
    Interval.MINOR_SIXTH: 8,
    Interval.MAJOR_SIXTH: 9,
    Interval.DIMINISHED_SEVENTH: 9,
    Interval.MINOR_SEVENTH: 10,
    Interval.MAJOR_SEVENTH: 11,
    Interval.PERFECT_OCTAVE: 12,
    Interval.MINOR_NINTH: 13,
    Interval.MAJOR_NINTH: 14,
    Interval.MINOR_TENTH: 15,
    Interval.MAJOR_TENTH: 16,
    Interval.PERFECT_ELEVENTH: 17,
    Interval.AUGMENTED_ELEVENTH: 18,
    Interval.PERFECT_TWELFTH: 19,
    Interval.MINOR_THIRTEENTH: 20,
    Interval.MAJOR_THIRTEENTH: 21,
}

# 音程名称映射（中文）
INTERVAL_NAMES_CN = {
    Interval.UNISON: "纯一度",
    Interval.MINOR_SECOND: "小二度",
    Interval.MAJOR_SECOND: "大二度",
    Interval.MINOR_THIRD: "小三度",
    Interval.MAJOR_THIRD: "大三度",
    Interval.PERFECT_FOURTH: "纯四度",
    Interval.AUGMENTED_FOURTH: "增四度",
    Interval.DIMINISHED_FIFTH: "减五度",
    Interval.PERFECT_FIFTH: "纯五度",
    Interval.AUGMENTED_FIFTH: "增五度",
    Interval.MINOR_SIXTH: "小六度",
    Interval.MAJOR_SIXTH: "大六度",
    Interval.DIMINISHED_SEVENTH: "减七度",
    Interval.MINOR_SEVENTH: "小七度",
    Interval.MAJOR_SEVENTH: "大七度",
    Interval.PERFECT_OCTAVE: "纯八度",
    Interval.MINOR_NINTH: "小九度",
    Interval.MAJOR_NINTH: "大九度",
    Interval.MINOR_TENTH: "小十度",
    Interval.MAJOR_TENTH: "大十度",
    Interval.PERFECT_ELEVENTH: "纯十一度",
    Interval.AUGMENTED_ELEVENTH: "增十一度",
    Interval.PERFECT_TWELFTH: "纯十二度",
    Interval.MINOR_THIRTEENTH: "小十三度",
    Interval.MAJOR_THIRTEENTH: "大十三度",
}

# 音程协和性
INTERVAL_CONSONANCE = {
    Interval.UNISON: "完全协和",
    Interval.MINOR_SECOND: "极不协和",
    Interval.MAJOR_SECOND: "不协和",
    Interval.MINOR_THIRD: "不完全协和",
    Interval.MAJOR_THIRD: "不完全协和",
    Interval.PERFECT_FOURTH: "完全协和",
    Interval.AUGMENTED_FOURTH: "极不协和",
    Interval.DIMINISHED_FIFTH: "极不协和",
    Interval.PERFECT_FIFTH: "完全协和",
    Interval.AUGMENTED_FIFTH: "不协和",
    Interval.MINOR_SIXTH: "不完全协和",
    Interval.MAJOR_SIXTH: "不完全协和",
    Interval.DIMINISHED_SEVENTH: "不协和",
    Interval.MINOR_SEVENTH: "不协和",
    Interval.MAJOR_SEVENTH: "不协和",
    Interval.PERFECT_OCTAVE: "完全协和",
}

# 音阶半音模式
SCALE_INTERVALS = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.MINOR_NATURAL: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.MINOR_HARMONIC: [0, 2, 3, 5, 7, 8, 11],
    ScaleType.MINOR_MELODIC: [0, 2, 3, 5, 7, 9, 11],  # 上行
    
    ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],
    ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],
    ScaleType.PENTATONIC_BLUES: [0, 3, 5, 6, 7, 10],
    
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
    ScaleType.LYDIAN: [0, 2, 4, 6, 7, 9, 11],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    ScaleType.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],
    
    ScaleType.CHROMATIC: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ScaleType.WHOLE_TONE: [0, 2, 4, 6, 8, 10],
    
    ScaleType.JAPANESE_YO: [0, 2, 5, 7, 10],
    ScaleType.JAPANESE_IN: [0, 1, 5, 7, 8],
    ScaleType.JAPANESE_HIRAJOSHI: [0, 2, 3, 7, 8],
    
    ScaleType.DIMINISHED: [0, 2, 3, 5, 6, 8, 9, 11],
    ScaleType.AUGMENTED: [0, 3, 4, 7, 8, 11],
    ScaleType.BEBOP_MAJOR: [0, 2, 4, 5, 7, 8, 9, 11],
    ScaleType.GYPSY_MINOR: [0, 2, 3, 6, 7, 8, 11],
    ScaleType.NEAPOLITAN_MINOR: [0, 1, 3, 5, 7, 8, 11],
}

# 和弦半音结构
CHORD_INTERVALS = {
    ChordType.MAJOR_TRIAD: [0, 4, 7],
    ChordType.MINOR_TRIAD: [0, 3, 7],
    ChordType.AUGMENTED_TRIAD: [0, 4, 8],
    ChordType.DIMINISHED_TRIAD: [0, 3, 6],
    
    ChordType.MAJOR_7: [0, 4, 7, 11],
    ChordType.MINOR_7: [0, 3, 7, 10],
    ChordType.DOMINANT_7: [0, 4, 7, 10],
    ChordType.DIMINISHED_7: [0, 3, 6, 9],
    ChordType.HALF_DIMINISHED_7: [0, 3, 6, 10],
    ChordType.AUGMENTED_7: [0, 4, 8, 10],
    ChordType.MINOR_MAJOR_7: [0, 3, 7, 11],
    
    ChordType.MAJOR_9: [0, 4, 7, 11, 14],
    ChordType.MINOR_9: [0, 3, 7, 10, 14],
    ChordType.DOMINANT_9: [0, 4, 7, 10, 14],
    ChordType.MAJOR_11: [0, 4, 7, 11, 14, 17],
    ChordType.MINOR_11: [0, 3, 7, 10, 14, 17],
    ChordType.DOMINANT_11: [0, 4, 7, 10, 14, 17],
    ChordType.MAJOR_13: [0, 4, 7, 11, 14, 17, 21],
    ChordType.MINOR_13: [0, 3, 7, 10, 14, 17, 21],
    ChordType.DOMINANT_13: [0, 4, 7, 10, 14, 17, 21],
    
    ChordType.SUS_2: [0, 2, 7],
    ChordType.SUS_4: [0, 5, 7],
    ChordType.SUS_2_7: [0, 2, 7, 10],
    ChordType.SUS_4_7: [0, 5, 7, 10],
    
    ChordType.ADD_9: [0, 4, 7, 14],
    ChordType.ADD_11: [0, 4, 7, 17],
    ChordType.ADD_2: [0, 2, 4, 7],
}

# 和弦名称映射（中文）
CHORD_NAMES_CN = {
    ChordType.MAJOR_TRIAD: "大三和弦",
    ChordType.MINOR_TRIAD: "小三和弦",
    ChordType.AUGMENTED_TRIAD: "增三和弦",
    ChordType.DIMINISHED_TRIAD: "减三和弦",
    ChordType.MAJOR_7: "大七和弦",
    ChordType.MINOR_7: "小七和弦",
    ChordType.DOMINANT_7: "属七和弦",
    ChordType.DIMINISHED_7: "减七和弦",
    ChordType.HALF_DIMINISHED_7: "半减七和弦",
    ChordType.AUGMENTED_7: "增七和弦",
    ChordType.MINOR_MAJOR_7: "小大七和弦",
    ChordType.SUS_2: "挂二和弦",
    ChordType.SUS_4: "挂四和弦",
    ChordType.ADD_9: "加九和弦",
    ChordType.ADD_2: "加二和弦",
}

# 调号升降记号
KEY_SIGNATURES = {
    'C major': 0, 'A minor': 0,
    'G major': 1, 'E minor': 1,      # 1 个升号 (F#)
    'D major': 2, 'B minor': 2,      # 2 个升号 (F#, C#)
    'A major': 3, 'F# minor': 3,     # 3 个升号 (F#, C#, G#)
    'E major': 4, 'C# minor': 4,     # 4 个升号 (F#, C#, G#, D#)
    'B major': 5, 'G# minor': 5,     # 5 个升号 (F#, C#, G#, D#, A#)
    'F# major': 6, 'D# minor': 6,    # 6 个升号
    'C# major': 7, 'A# minor': 7,    # 7 个升号
    
    'F major': -1, 'D minor': -1,    # 1 个降号 (Bb)
    'Bb major': -2, 'G minor': -2,   # 2 个降号 (Bb, Eb)
    'Eb major': -3, 'C minor': -3,   # 3 个降号 (Bb, Eb, Ab)
    'Ab major': -4, 'F minor': -4,   # 4 个降号 (Bb, Eb, Ab, Db)
    'Db major': -5, 'Bb minor': -5,  # 5 个降号
    'Gb major': -6, 'Eb minor': -6,  # 6 个降号
    'Cb major': -7, 'Ab minor': -7,  # 7 个降号
}

# 升号顺序
SHARP_ORDER = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
# 降号顺序
FLAT_ORDER = ['B', 'E', 'A', 'D', 'G', 'C', 'F']

# 音符半音数（从 C 开始）
NOTE_SEMITONES = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}


@dataclass
class Note:
    """音符"""
    name: str          # 音名（C, D, E, F, G, A, B）
    octave: int        # 八度（0-9）
    accidental: str    # 变音记号（'', '#', 'b'）
    
    def __post_init__(self):
        self.name = self.name.upper()
        if self.octave < 0:
            self.octave = 0
        if self.octave > 9:
            self.octave = 9
    
    def get_full_name(self) -> str:
        """获取完整音符名称"""
        return f"{self.name}{self.accidental}"
    
    def get_midi_number(self) -> int:
        """获取 MIDI 音符编号"""
        base_note = f"{self.name}{self.accidental}"
        semitones = NOTE_SEMITONES.get(base_note, 0)
        return 12 + (self.octave * 12) + semitones
    
    def get_frequency(self, a4_freq: float = 440.0) -> float:
        """
        计算音符频率
        
        Args:
            a4_freq: A4 的参考频率（默认 440Hz）
        
        Returns:
            频率（Hz）
        """
        midi = self.get_midi_number()
        # A4 的 MIDI 编号是 69
        return a4_freq * (2 ** ((midi - 69) / 12))
    
    def __repr__(self) -> str:
        return f"{self.name}{self.accidental}{self.octave}"


@dataclass
class Scale:
    """音阶"""
    root: str           # 根音
    scale_type: ScaleType  # 音阶类型
    notes: List[Note]   # 音阶音符列表
    
    def __repr__(self) -> str:
        return f"{self.root} {self.scale_type.value}"


@dataclass
class Chord:
    """和弦"""
    root: str           # 根音
    chord_type: ChordType  # 和弦类型
    notes: List[Note]   # 和弦音符列表
    
    def get_symbol(self) -> str:
        """获取和弦符号"""
        chord_symbols = {
            ChordType.MAJOR_TRIAD: '',
            ChordType.MINOR_TRIAD: 'm',
            ChordType.AUGMENTED_TRIAD: 'aug',
            ChordType.DIMINISHED_TRIAD: 'dim',
            ChordType.MAJOR_7: 'maj7',
            ChordType.MINOR_7: 'm7',
            ChordType.DOMINANT_7: '7',
            ChordType.DIMINISHED_7: 'dim7',
            ChordType.HALF_DIMINISHED_7: 'm7b5',
            ChordType.AUGMENTED_7: 'aug7',
            ChordType.MINOR_MAJOR_7: 'mMaj7',
            ChordType.MAJOR_9: 'maj9',
            ChordType.MINOR_9: 'm9',
            ChordType.DOMINANT_9: '9',
            ChordType.SUS_2: 'sus2',
            ChordType.SUS_4: 'sus4',
            ChordType.ADD_9: 'add9',
            ChordType.ADD_2: 'add2',
        }
        symbol = chord_symbols.get(self.chord_type, self.chord_type.value)
        return f"{self.root}{symbol}"
    
    def __repr__(self) -> str:
        return self.get_symbol()


def midi_to_note(midi_number: int) -> Note:
    """
    将 MIDI 音符编号转换为音符对象
    
    Args:
        midi_number: MIDI 音符编号（0-127）
    
    Returns:
        Note 对象
    """
    midi_number = max(0, min(127, midi_number))
    
    octave = (midi_number - 12) // 12
    semitone = (midi_number - 12) % 12
    
    # 半音到音符映射（优先使用升号表示）
    semitone_to_note = {
        0: ('C', ''),
        1: ('C', '#'),
        2: ('D', ''),
        3: ('D', '#'),
        4: ('E', ''),
        5: ('F', ''),
        6: ('F', '#'),
        7: ('G', ''),
        8: ('G', '#'),
        9: ('A', ''),
        10: ('A', '#'),
        11: ('B', ''),
    }
    
    name, accidental = semitone_to_note[semitone]
    return Note(name=name, octave=octave, accidental=accidental)


def midi_to_frequency(midi_number: int, a4_freq: float = 440.0) -> float:
    """
    将 MIDI 音符编号转换为频率
    
    Args:
        midi_number: MIDI 音符编号
        a4_freq: A4 的参考频率
    
    Returns:
        频率（Hz）
    """
    return a4_freq * (2 ** ((midi_number - 69) / 12))


def frequency_to_midi(frequency: float, a4_freq: float = 440.0) -> int:
    """
    将频率转换为最接近的 MIDI 音符编号
    
    Args:
        frequency: 频率（Hz）
        a4_freq: A4 的参考频率
    
    Returns:
        MIDI 音符编号
    """
    if frequency <= 0:
        return 0
    
    midi = 69 + 12 * math.log2(frequency / a4_freq)
    return round(midi)


def generate_scale(root: str, scale_type: ScaleType, octave: int = 4) -> Scale:
    """
    生成音阶
    
    Args:
        root: 根音（如 'C', 'D', 'E#' 等）
        scale_type: 音阶类型
        octave: 八度
    
    Returns:
        Scale 对象
    
    Example:
        >>> scale = generate_scale('C', ScaleType.MAJOR)
        >>> [n.get_full_name() for n in scale.notes]
        ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    """
    root = root.upper()
    
    # 解析根音（检查长度以避免 'B' 被误判为降号）
    if len(root) > 1:
        if root[1] == '#':
            root_note = root[0]
            accidental = '#'
        elif root[1] == 'B':  # 大写后 'b' 变成 'B'
            root_note = root[0]
            accidental = 'b'
        else:
            root_note = root
            accidental = ''
    else:
        root_note = root
        accidental = ''
    
    # 获取根音的半音数
    root_semitone = NOTE_SEMITONES.get(f"{root_note}{accidental}", 0)
    
    # 获取音阶模式
    intervals = SCALE_INTERVALS.get(scale_type, SCALE_INTERVALS[ScaleType.MAJOR])
    
    # 生成音符
    notes = []
    for interval in intervals:
        semitone = root_semitone + interval
        octave_offset = semitone // 12
        semitone_in_octave = semitone % 12
        
        # 半音到音符映射（升号优先）
        sharp_map = {
            0: ('C', ''),
            1: ('C', '#'),
            2: ('D', ''),
            3: ('D', '#'),
            4: ('E', ''),
            5: ('F', ''),
            6: ('F', '#'),
            7: ('G', ''),
            8: ('G', '#'),
            9: ('A', ''),
            10: ('A', '#'),
            11: ('B', ''),
        }
        
        # 半音到音符映射（降号优先）
        flat_map = {
            0: ('C', ''),
            1: ('Db', 'b'),
            2: ('D', ''),
            3: ('Eb', 'b'),
            4: ('E', ''),
            5: ('F', ''),
            6: ('Gb', 'b'),
            7: ('G', ''),
            8: ('Ab', 'b'),
            9: ('A', ''),
            10: ('Bb', 'b'),
            11: ('B', ''),
        }
        
        # 根据根音的升降记号选择映射
        if accidental == 'b':
            name, acc = flat_map[semitone_in_octave]
        else:
            name, acc = sharp_map[semitone_in_octave]
        
        # 处理名称中的升降记号（只检查是否为双字符）
        if len(name) == 2 and (name[1] == '#' or name[1] == 'b'):
            actual_name = name[0]
            actual_acc = name[1]
        else:
            actual_name = name
            actual_acc = acc
        
        note = Note(name=actual_name, octave=octave + octave_offset, accidental=actual_acc)
        notes.append(note)
    
    return Scale(root=root, scale_type=scale_type, notes=notes)


def generate_chord(root: str, chord_type: ChordType, octave: int = 4) -> Chord:
    """
    生成和弦
    
    Args:
        root: 根音
        chord_type: 和弦类型
        octave: 八度
    
    Returns:
        Chord 对象
    
    Example:
        >>> chord = generate_chord('C', ChordType.MAJOR_7)
        >>> [n.get_full_name() for n in chord.notes]
        ['C', 'E', 'G', 'B']
    """
    root = root.upper()
    
    # 解析根音（检查长度以避免 'B' 被误判为降号）
    if len(root) > 1:
        if root[1] == '#':
            root_note = root[0]
            accidental = '#'
        elif root[1] == 'B':  # 大写后 'b' 变成 'B'
            root_note = root[0]
            accidental = 'b'
        else:
            root_note = root
            accidental = ''
    else:
        root_note = root
        accidental = ''
    
    # 获取根音的半音数
    root_semitone = NOTE_SEMITONES.get(f"{root_note}{accidental}", 0)
    
    # 获取和弦模式
    intervals = CHORD_INTERVALS.get(chord_type, CHORD_INTERVALS[ChordType.MAJOR_TRIAD])
    
    # 半音到音符映射（升号优先）
    semitone_to_note_sharp = {
        0: ('C', ''),
        1: ('C', '#'),
        2: ('D', ''),
        3: ('D', '#'),
        4: ('E', ''),
        5: ('F', ''),
        6: ('F', '#'),
        7: ('G', ''),
        8: ('G', '#'),
        9: ('A', ''),
        10: ('A', '#'),
        11: ('B', ''),
    }
    
    # 半音到音符映射（降号优先）
    semitone_to_note_flat = {
        0: ('C', ''),
        1: ('Db', 'b'),
        2: ('D', ''),
        3: ('Eb', 'b'),
        4: ('E', ''),
        5: ('F', ''),
        6: ('Gb', 'b'),
        7: ('G', ''),
        8: ('Ab', 'b'),
        9: ('A', ''),
        10: ('Bb', 'b'),
        11: ('B', ''),
    }
    
    # 生成音符
    notes = []
    for interval in intervals:
        semitone = root_semitone + interval
        octave_offset = semitone // 12
        semitone_in_octave = semitone % 12
        
        # 根据根音的升降记号选择映射
        if accidental == 'b':
            name, acc = semitone_to_note_flat[semitone_in_octave]
        else:
            name, acc = semitone_to_note_sharp[semitone_in_octave]
        
        # 处理名称中的升降记号（只检查是否为双字符）
        if len(name) == 2 and (name[1] == '#' or name[1] == 'b'):
            actual_name = name[0]
            actual_acc = name[1]
        else:
            actual_name = name
            actual_acc = acc
        
        note = Note(name=actual_name, octave=octave + octave_offset, accidental=actual_acc)
        notes.append(note)
    
    return Chord(root=root, chord_type=chord_type, notes=notes)


def get_interval(note1: Note, note2: Note) -> Interval:
    """
    计算两个音符之间的音程
    
    Args:
        note1: 第一个音符
        note2: 第二个音符
    
    Returns:
        Interval 对象
    
    Example:
        >>> get_interval(Note('C', 4, ''), Note('E', 4, ''))
        Interval.MAJOR_THIRD
    """
    semitones = note2.get_midi_number() - note1.get_midi_number()
    semitones = semitones % 12  # 只考虑单八度内的音程
    
    # 半音数到音程映射
    semitone_to_interval = {
        0: Interval.UNISON,
        1: Interval.MINOR_SECOND,
        2: Interval.MAJOR_SECOND,
        3: Interval.MINOR_THIRD,
        4: Interval.MAJOR_THIRD,
        5: Interval.PERFECT_FOURTH,
        6: Interval.AUGMENTED_FOURTH,  # 或 DIMINISHED_FIFTH
        7: Interval.PERFECT_FIFTH,
        8: Interval.MINOR_SIXTH,  # 或 AUGMENTED_FIFTH
        9: Interval.MAJOR_SIXTH,
        10: Interval.MINOR_SEVENTH,
        11: Interval.MAJOR_SEVENTH,
    }
    
    return semitone_to_interval.get(semitones, Interval.UNISON)


def get_interval_name(interval: Interval, language: str = 'cn') -> str:
    """
    获取音程名称
    
    Args:
        interval: 音程对象
        language: 语言（'cn' 中文，'en' 英文）
    
    Returns:
        音程名称
    """
    if language == 'cn':
        return INTERVAL_NAMES_CN.get(interval, interval.value)
    return interval.value


def get_interval_consonance(interval: Interval) -> str:
    """
    获取音程协和性
    
    Args:
        interval: 音程
    
    Returns:
        协和性描述
    """
    return INTERVAL_CONSONANCE.get(interval, "未知")


def transpose_note(note: Note, semitones: int) -> Note:
    """
    移调音符
    
    Args:
        note: 原音符
        semitones: 移调半音数（正数升高，负数降低）
    
    Returns:
        移调后的音符
    """
    new_midi = note.get_midi_number() + semitones
    return midi_to_note(new_midi)


def get_chord_tones(chord: Chord) -> Dict[str, str]:
    """
    获取和弦中各音的功能
    
    Args:
        chord: 和弦对象
    
    Returns:
        音符功能字典
    """
    if len(chord.notes) < 3:
        return {}
    
    roles = {
        'root': chord.notes[0].get_full_name(),
        'third': chord.notes[1].get_full_name() if len(chord.notes) > 1 else None,
        'fifth': chord.notes[2].get_full_name() if len(chord.notes) > 2 else None,
    }
    
    if len(chord.notes) > 3:
        roles['seventh'] = chord.notes[3].get_full_name()
    
    if len(chord.notes) > 4:
        roles['extensions'] = [n.get_full_name() for n in chord.notes[4:]]
    
    return roles


def analyze_chord_quality(chord: Chord) -> Dict[str, any]:
    """
    分析和弦性质
    
    Args:
        chord: 和弦
    
    Returns:
        和弦性质信息
    """
    notes = chord.notes
    
    result = {
        'symbol': chord.get_symbol(),
        'type': chord.chord_type.value,
        'type_cn': CHORD_NAMES_CN.get(chord.chord_type, chord.chord_type.value),
        'notes': [n.get_full_name() for n in notes],
        'midi_notes': [n.get_midi_number() for n in notes],
        'frequencies': [round(n.get_frequency(), 2) for n in notes],
        'intervals_from_root': [],
    }
    
    # 计算各音与根音的音程
    for note in notes:
        interval = get_interval(notes[0], note)
        result['intervals_from_root'].append({
            'note': note.get_full_name(),
            'interval': interval.value,
            'interval_cn': get_interval_name(interval),
            'semitones': INTERVAL_SEMITONES[interval],
        })
    
    return result


def get_relative_keys(key: str) -> Dict[str, List[str]]:
    """
    获取近关系调
    
    Args:
        key: 调名（如 'C major', 'A minor'）
    
    Returns:
        近关系调列表
    """
    # 解析调性
    if 'minor' in key.lower():
        is_minor = True
        tonic = key.split()[0].upper()
    else:
        is_minor = False
        tonic = key.split()[0].upper()
    
    tonic_semitone = NOTE_SEMITONES.get(tonic, 0)
    
    relatives = {
        'parallel': [],        # 同主音调
        'relative': [],        # 关系调
        'dominant': [],        # 属调
        'subdominant': [],     # 下属调
        'mediant': [],         # 中音调
    }
    
    if is_minor:
        # 小调的关系大调（上方小三度）
        major_tonic_semitone = (tonic_semitone + 3) % 12
        relatives['relative'] = [f"{midi_to_note(12 + major_tonic_semitone).get_full_name()} major"]
        
        # 同主音大调
        relatives['parallel'] = [f"{tonic} major"]
        
        # 属调（小调属调是小调）
        dominant_semitone = (tonic_semitone + 7) % 12
        relatives['dominant'] = [f"{midi_to_note(12 + dominant_semitone).get_full_name()} minor"]
        
        # 下属调
        subdominant_semitone = (tonic_semitone - 5) % 12
        relatives['subdominant'] = [f"{midi_to_note(12 + subdominant_semitone).get_full_name()} minor"]
    else:
        # 大调的关系小调（下方小三度）
        minor_tonic_semitone = (tonic_semitone - 3) % 12
        relatives['relative'] = [f"{midi_to_note(12 + minor_tonic_semitone).get_full_name()} minor"]
        
        # 同主音小调
        relatives['parallel'] = [f"{tonic} minor"]
        
        # 属调（大调属调是大调）
        dominant_semitone = (tonic_semitone + 7) % 12
        relatives['dominant'] = [f"{midi_to_note(12 + dominant_semitone).get_full_name()} major"]
        
        # 下属调
        subdominant_semitone = (tonic_semitone - 7) % 12
        relatives['subdominant'] = [f"{midi_to_note(12 + subdominant_semitone).get_full_name()} major"]
    
    return relatives


def get_key_signature(key: str) -> Dict[str, any]:
    """
    获取调号信息
    
    Args:
        key: 谓名（如 'C major', 'G major', 'A minor'）
    
    Returns:
        调号信息
    """
    # 标准化调名
    key_lower = key.lower()
    
    # 直接查找
    if key in KEY_SIGNATURES:
        accidentals = KEY_SIGNATURES[key]
    else:
        # 尝试解析
        parts = key.split()
        tonic = parts[0].upper()
        quality = 'major' if 'major' in key_lower else 'minor'
        standard_key = f"{tonic} {quality}"
        accidentals = KEY_SIGNATURES.get(standard_key, 0)
    
    result = {
        'key': key,
        'accidentals': accidentals,
        'accidental_type': 'sharps' if accidentals > 0 else 'flats' if accidentals < 0 else 'none',
        'accidental_notes': [],
    }
    
    # 列出具体的升降记号音符
    if accidentals > 0:
        result['accidental_notes'] = [f"{n}#" for n in SHARP_ORDER[:accidentals]]
    elif accidentals < 0:
        result['accidental_notes'] = [f"{n}b" for n in FLAT_ORDER[:abs(accidentals)]]
    
    return result


def get_scale_degrees(scale: Scale) -> List[Dict[str, any]]:
    """
    获取音阶各音的级数信息
    
    Args:
        scale: 音阶
    
    Returns:
        各音级信息
    """
    degree_names = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    degree_names_cn = ['主音', '上主音', '中音', '下属音', '属音', '下中音', '导音', '八度音']
    
    degrees = []
    for i, note in enumerate(scale.notes):
        if i >= len(degree_names):
            break
        
        degree_info = {
            'degree': degree_names[i],
            'degree_cn': degree_names_cn[i],
            'note': note.get_full_name(),
            'midi': note.get_midi_number(),
            'frequency': round(note.get_frequency(), 2),
        }
        
        # 如果有根音，计算音程
        if i > 0:
            interval = get_interval(scale.notes[0], note)
            degree_info['interval_from_root'] = interval.value
            degree_info['interval_cn'] = get_interval_name(interval)
        
        degrees.append(degree_info)
    
    return degrees


def get_chord_progression_degrees(scale: Scale) -> List[Dict[str, any]]:
    """
    获取调内和弦（基于音阶的自然和弦）
    
    Args:
        scale: 音阶
    
    Returns:
        调内和弦列表
    """
    # 大调调内和弦类型
    major_chord_types = [
        ChordType.MAJOR_TRIAD,     # I
        ChordType.MINOR_TRIAD,     # II
        ChordType.MINOR_TRIAD,     # III
        ChordType.MAJOR_TRIAD,     # IV
        ChordType.MAJOR_TRIAD,     # V
        ChordType.MINOR_TRIAD,     # VI
        ChordType.DIMINISHED_TRIAD, # VII
    ]
    
    # 小调调内和弦类型
    minor_chord_types = [
        ChordType.MINOR_TRIAD,     # I
        ChordType.DIMINISHED_TRIAD, # II
        ChordType.MAJOR_TRIAD,     # III
        ChordType.MINOR_TRIAD,     # IV
        ChordType.MINOR_TRIAD,     # V (自然小调) 或 MAJOR_TRIAD (和声小调)
        ChordType.MAJOR_TRIAD,     # VI
        ChordType.MAJOR_TRIAD,     # VII (自然小调) 或 DIMINISHED_TRIAD (和声小调)
    ]
    
    degree_names = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    
    is_major = scale.scale_type in [ScaleType.MAJOR, ScaleType.LYDIAN, ScaleType.MIXOLYDIAN]
    chord_types = major_chord_types if is_major else minor_chord_types
    
    progression = []
    for i, note in enumerate(scale.notes[:7]):
        if i >= len(degree_names):
            break
        
        chord_type = chord_types[i]
        chord = generate_chord(note.get_full_name(), chord_type, note.octave)
        
        progression.append({
            'degree': degree_names[i],
            'chord': chord.get_symbol(),
            'chord_type': chord_type.value,
            'function': 'T' if i in [0, 3, 5] else 'S' if i in [1, 3] else 'D' if i in [4, 6] else '?',
            'notes': [n.get_full_name() for n in chord.notes],
        })
    
    return progression


def calculate_tempo(duration_seconds: float, beats: int) -> float:
    """
    计算速度（BPM）
    
    Args:
        duration_seconds: 时长（秒）
        beats: 拍数
    
    Returns:
        BPM（每分钟拍数）
    """
    if duration_seconds <= 0 or beats <= 0:
        return 0
    
    return (beats / duration_seconds) * 60


def calculate_duration(bpm: float, beats: int) -> float:
    """
    计算时长
    
    Args:
        bpm: 速度（BPM）
        beats: 拍数
    
    Returns:
        时长（秒）
    """
    if bpm <= 0:
        return 0
    
    return (beats / bpm) * 60


def get_beat_durations(bpm: float) -> Dict[str, float]:
    """
    获取各种节拍的时长
    
    Args:
        bpm: 速度（BPM）
    
    Returns:
        各种节拍时长（秒）
    """
    quarter_duration = 60 / bpm
    
    return {
        'whole_note': quarter_duration * 4,        # 全音符
        'half_note': quarter_duration * 2,         # 二分音符
        'quarter_note': quarter_duration,          # 四分音符
        'eighth_note': quarter_duration / 2,       # 八分音符
        'sixteenth_note': quarter_duration / 4,    # 十六分音符
        'thirty_second_note': quarter_duration / 8, # 三十二分音符
        'dotted_half': quarter_duration * 3,       # 附点二分
        'dotted_quarter': quarter_duration * 1.5,  # 附点四分
        'dotted_eighth': quarter_duration * 0.75,  # 附点八分
    }


def analyze_rhythm_pattern(pattern: List[int], bpm: float) -> Dict[str, any]:
    """
    分析节奏模式
    
    Args:
        pattern: 节奏模式（每个值表示一个音符的 subdivision）
                 例如 [4, 4, 4, 4] 表示四个四分音符
                 [8, 8, 4, 8, 8, 4] 表示两个八分、一个四分、两个八分、一个四分
        bpm: 速度
    
    Returns:
        节奏分析结果
    """
    beat_durations = get_beat_durations(bpm)
    
    subdivision_to_name = {
        1: 'whole_note',
        2: 'half_note',
        4: 'quarter_note',
        8: 'eighth_note',
        16: 'sixteenth_note',
        32: 'thirty_second_note',
    }
    
    total_duration = 0
    note_info = []
    
    for subdivision in pattern:
        name = subdivision_to_name.get(subdivision, 'quarter_note')
        duration = beat_durations[name]
        total_duration += duration
        
        note_info.append({
            'subdivision': subdivision,
            'name': name,
            'duration': round(duration, 4),
        })
    
    return {
        'pattern': pattern,
        'bpm': bpm,
        'total_beats': sum(4 / s for s in pattern),  # 以四分音符为基准
        'total_duration_seconds': round(total_duration, 4),
        'notes': note_info,
    }


def suggest_harmony_for_melody(melody_notes: List[str], key: str) -> List[Dict[str, any]]:
    """
    为旋律建议和弦
    
    Args:
        melody_notes: 旋律音符列表
        key: 调性
    
    Returns:
        和弦建议
    """
    # 解析调性
    if 'minor' in key.lower():
        scale_type = ScaleType.MINOR_NATURAL
    else:
        scale_type = ScaleType.MAJOR
    
    tonic = key.split()[0].upper()
    scale = generate_scale(tonic, scale_type)
    
    # 获取调内和弦
    progression = get_chord_progression_degrees(scale)
    
    suggestions = []
    for melody_note in melody_notes:
        melody_note = melody_note.upper()
        
        # 找到包含该音符的和弦
        matching_chords = []
        for chord_info in progression:
            if melody_note.rstrip('#').rstrip('b') in chord_info['notes']:
                matching_chords.append(chord_info)
        
        suggestions.append({
            'melody_note': melody_note,
            'suggested_chords': matching_chords,
            'primary_suggestion': matching_chords[0] if matching_chords else None,
        })
    
    return suggestions


def compare_scales(scale1: Scale, scale2: Scale) -> Dict[str, any]:
    """
    比较两个音阶
    
    Args:
        scale1: 第一个音阶
        scale2: 第二个音阶
    
    Returns:
        比较结果
    """
    notes1 = set(n.get_full_name().rstrip('4').rstrip('3').rstrip('5') for n in scale1.notes)
    notes2 = set(n.get_full_name().rstrip('4').rstrip('3').rstrip('5') for n in scale2.notes)
    
    common = notes1 & notes2
    unique1 = notes1 - notes2
    unique2 = notes2 - notes1
    
    return {
        'scale1': f"{scale1.root} {scale1.scale_type.value}",
        'scale2': f"{scale2.root} {scale2.scale_type.value}",
        'common_notes': list(common),
        'unique_to_scale1': list(unique1),
        'unique_to_scale2': list(unique2),
        'similarity': round(len(common) / max(len(notes1), len(notes2)), 2),
    }


def get_all_modes_of_scale(root: str) -> Dict[str, Scale]:
    """
    获取一个音阶的所有调式
    
    Args:
        root: 根音
    
    Returns:
        所有调式音阶
    """
    modes = {
        'Ionian (Major)': generate_scale(root, ScaleType.MAJOR),
        'Dorian': generate_scale(root, ScaleType.DORIAN),
        'Phrygian': generate_scale(root, ScaleType.PHRYGIAN),
        'Lydian': generate_scale(root, ScaleType.LYDIAN),
        'Mixolydian': generate_scale(root, ScaleType.MIXOLYDIAN),
        'Aeolian (Natural Minor)': generate_scale(root, ScaleType.MINOR_NATURAL),
        'Locrian': generate_scale(root, ScaleType.LOCRIAN),
    }
    
    return modes


def invert_chord(chord: Chord, inversion: int) -> Chord:
    """
    和弦转位
    
    Args:
        chord: 原和弦
        inversion: 转位次数（1 = 第一转位，2 = 第二转位，3 = 第三转位）
    
    Returns:
        转位后的和弦
    """
    if inversion < 0 or inversion >= len(chord.notes):
        return chord
    
    # 将底部音符移到顶部
    notes = chord.notes.copy()
    for _ in range(inversion):
        bottom_note = notes[0]
        # 将底部音符升高一个八度
        notes = notes[1:] + [Note(
            name=bottom_note.name,
            octave=bottom_note.octave + 1,
            accidental=bottom_note.accidental
        )]
    
    return Chord(root=chord.root, chord_type=chord.chord_type, notes=notes)


def get_chord_inversion_name(chord_type: ChordType, inversion: int) -> str:
    """
    获取和弦转位名称
    
    Args:
        chord_type: 和弦类型
        inversion: 转位次数
    
    Returns:
        转位名称
    """
    if inversion == 0:
        return "原位"
    
    is_triad = chord_type in [
        ChordType.MAJOR_TRIAD, ChordType.MINOR_TRIAD,
        ChordType.AUGMENTED_TRIAD, ChordType.DIMINISHED_TRIAD,
        ChordType.SUS_2, ChordType.SUS_4
    ]
    
    if is_triad:
        inversion_names = {
            1: "第一转位（六和弦）",
            2: "第二转位（四六和弦）",
        }
    else:
        inversion_names = {
            1: "第一转位（五六和弦）",
            2: "第二转位（三四和弦）",
            3: "第三转位（二和弦）",
        }
    
    return inversion_names.get(inversion, f"{inversion}转位")


# ============ 高级功能 ============

def analyze_key_from_notes(notes: List[str]) -> Dict[str, any]:
    """
    根据音符分析可能的调性
    
    Args:
        notes: 音符列表
    
    Returns:
        可能的调性
    """
    # 收集所有音符（标准化）
    note_set = set(n.upper() for n in notes)
    
    # 检查各个大调和小调
    possible_keys = []
    
    for tonic in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        # 大调
        major_scale = generate_scale(tonic, ScaleType.MAJOR)
        major_notes = set(n.get_full_name() for n in major_scale.notes)
        
        matches = len(note_set & major_notes)
        if matches > 0:
            possible_keys.append({
                'key': f"{tonic} major",
                'matching_notes': matches,
                'total_notes': len(major_notes),
                'confidence': round(matches / len(note_set), 2),
            })
        
        # 小调
        minor_scale = generate_scale(tonic, ScaleType.MINOR_NATURAL)
        minor_notes = set(n.get_full_name() for n in minor_scale.notes)
        
        matches = len(note_set & minor_notes)
        if matches > 0:
            possible_keys.append({
                'key': f"{tonic} minor",
                'matching_notes': matches,
                'total_notes': len(minor_notes),
                'confidence': round(matches / len(note_set), 2),
            })
    
    # 按匹配度排序
    possible_keys.sort(key=lambda x: x['confidence'], reverse=True)
    
    return {
        'input_notes': list(note_set),
        'possible_keys': possible_keys[:5],  # 返回前5个最可能的调
        'best_match': possible_keys[0] if possible_keys else None,
    }


def generate_arpeggio(chord: Chord, pattern: str = 'up', octaves: int = 1) -> List[Note]:
    """
    生成琶音
    
    Args:
        chord: 和弦
        pattern: 琶音模式（'up', 'down', 'up_down'）
        octaves: 八度数
    
    Returns:
        琶音音符列表
    """
    base_notes = chord.notes
    
    arpeggio = []
    
    for octave_offset in range(octaves):
        octave_notes = [
            Note(n.name, n.octave + octave_offset, n.accidental)
            for n in base_notes
        ]
        
        if pattern == 'up' or pattern == 'up_down':
            arpeggio.extend(octave_notes)
        elif pattern == 'down':
            arpeggio.extend(reversed(octave_notes))
    
    if pattern == 'up_down':
        # 添加下行部分（去掉已添加的最高音）
        arpeggio.extend(reversed(arpeggio[:-1]))
    
    return arpeggio


def get_interval_matrix(root: str, octave: int = 4) -> Dict[str, Dict[str, any]]:
    """
    生成音程矩阵（根音与其他各音的音程关系）
    
    Args:
        root: 根音
        octave: 八度
    
    Returns:
        音程矩阵
    """
    root_note = Note(root[0].upper(), octave, root[1:] if len(root) > 1 else '')
    
    matrix = {}
    chromatic_scale = generate_scale(root, ScaleType.CHROMATIC)
    
    for note in chromatic_scale.notes[:12]:
        interval = get_interval(root_note, note)
        matrix[note.get_full_name()] = {
            'interval': interval.value,
            'interval_cn': get_interval_name(interval),
            'semitones': INTERVAL_SEMITONES[interval],
            'consonance': get_interval_consonance(interval),
        }
    
    return matrix


def create_chord_from_intervals(root: str, intervals: List[Interval], octave: int = 4) -> Chord:
    """
    根据音程列表创建和弦
    
    Args:
        root: 根音
        intervals: 音程列表
        octave: 八度
    
    Returns:
        Chord 对象
    """
    root_note = Note(root[0].upper(), octave, root[1:] if len(root) > 1 else '')
    
    notes = [root_note]
    
    for interval in intervals:
        semitones = INTERVAL_SEMITONES[interval]
        new_note = transpose_note(root_note, semitones)
        notes.append(new_note)
    
    # 尝试识别和弦类型
    chord_semitones = [INTERVAL_SEMITONES[get_interval(root_note, n)] for n in notes]
    
    # 匹配和弦类型
    chord_type = ChordType.MAJOR_TRIAD  # 默认
    for ct, intervals_list in CHORD_INTERVALS.items():
        if chord_semitones == intervals_list:
            chord_type = ct
            break
    
    return Chord(root=root, chord_type=chord_type, notes=notes)


def get_note_enharmonic(note: str) -> Dict[str, str]:
    """
    获取等音
    
    Args:
        note: 音符
    
    Returns:
        等音映射
    """
    note = note.upper()
    # 统一格式：降号用小写 'b'，升号用 '#'
    if len(note) > 1 and note[1] == 'B':
        note = note[0] + 'b'
    
    # 等音映射（双向）
    enharmonics = {
        'C#': 'Db',
        'DB': 'C#',
        'D#': 'Eb',
        'EB': 'D#',
        'F#': 'Gb',
        'GB': 'F#',
        'G#': 'Ab',
        'AB': 'G#',
        'A#': 'Bb',
        'BB': 'A#',
        # 小写 b 形式
        'Db': 'C#',
        'Eb': 'D#',
        'Gb': 'F#',
        'Ab': 'G#',
        'Bb': 'A#',
    }
    
    return {
        'note': note,
        'enharmonic': enharmonics.get(note, 'N/A'),
        'is_enharmonic': note in enharmonics,
    }


def get_all_scale_types_info() -> List[Dict[str, any]]:
    """
    获取所有音阶类型信息
    
    Returns:
        音阶类型列表
    """
    scale_info = []
    
    for scale_type, intervals in SCALE_INTERVALS.items():
        # 计算音阶特征
        semitone_pattern = intervals
        
        # 判断是否为七声音阶、五声音阶等
        if len(semitone_pattern) == 7:
            category = "七声音阶"
        elif len(semitone_pattern) == 5:
            category = "五声音阶"
        elif len(semitone_pattern) == 6:
            category = "六声音阶"
        elif len(semitone_pattern) == 12:
            category = "半音阶"
        else:
            category = "特殊音阶"
        
        scale_info.append({
            'name': scale_type.value,
            'category': category,
            'notes_count': len(semitone_pattern),
            'interval_pattern': semitone_pattern,
        })
    
    return scale_info


def get_all_chord_types_info() -> List[Dict[str, any]]:
    """
    获取所有和弦类型信息
    
    Returns:
        和弦类型列表
    """
    chord_info = []
    
    for chord_type, intervals in CHORD_INTERVALS.items():
        # 分类
        if len(intervals) == 3:
            category = "三和弦"
        elif len(intervals) == 4:
            category = "七和弦"
        elif len(intervals) <= 6:
            category = "扩展和弦"
        else:
            category = "特殊和弦"
        
        chord_info.append({
            'name': chord_type.value,
            'symbol': chord_type.value,
            'category': category,
            'notes_count': len(intervals),
            'interval_semitones': intervals,
            'name_cn': CHORD_NAMES_CN.get(chord_type, chord_type.value),
        })
    
    return chord_info


def generate_circle_of_fifths() -> List[Dict[str, any]]:
    """
    生成五度圈
    
    Returns:
        五度圈信息
    """
    # 大调五度圈
    major_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    
    circle = []
    
    for i, key in enumerate(major_keys):
        # 计算升降记号数
        if i <= 7:
            accidentals = i
            accidental_type = 'sharps'
        else:
            accidentals = 14 - i
            accidental_type = 'flats'
        
        # 关系小调
        tonic_semitone = NOTE_SEMITONES.get(key, 0)
        relative_minor_semitone = (tonic_semitone - 3) % 12
        
        # 找到关系小调的音符名
        for note_name, semitone in NOTE_SEMITONES.items():
            if semitone == relative_minor_semitone and 'b' not in note_name:
                relative_minor = note_name
                break
        
        circle.append({
            'position': i,
            'major_key': key,
            'relative_minor': relative_minor,
            'accidentals': accidentals,
            'accidental_type': accidental_type,
        })
    
    return circle