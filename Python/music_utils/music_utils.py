"""
Music Theory Utilities - 零外部依赖的乐理工具库

功能:
- 音符频率计算 (A4 = 440Hz 标准)
- 音阶生成 (大调、小调、调式、五声、布鲁斯)
- 和弦生成与识别
- MIDI 音符转换
- 音程计算
- 调号助手
- 五度圈与四度圈
- 节拍器计算
- 泛音列生成
- 纯律计算

作者: AllToolkit
日期: 2026-05-02
"""

import math
from enum import Enum, IntEnum
from typing import List, Tuple, Optional, Dict, Set


class NoteName(IntEnum):
    """音符名称枚举"""
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11


# 音符显示名称
_NOTE_NAMES_SHARP = {
    NoteName.C: "C",
    NoteName.C_SHARP: "C#",
    NoteName.D: "D",
    NoteName.D_SHARP: "D#",
    NoteName.E: "E",
    NoteName.F: "F",
    NoteName.F_SHARP: "F#",
    NoteName.G: "G",
    NoteName.G_SHARP: "G#",
    NoteName.A: "A",
    NoteName.A_SHARP: "A#",
    NoteName.B: "B",
}

_NOTE_NAMES_FLAT = {
    NoteName.C: "C",
    NoteName.C_SHARP: "Db",
    NoteName.D: "D",
    NoteName.D_SHARP: "Eb",
    NoteName.E: "E",
    NoteName.F: "F",
    NoteName.F_SHARP: "Gb",
    NoteName.G: "G",
    NoteName.G_SHARP: "Ab",
    NoteName.A: "A",
    NoteName.A_SHARP: "Bb",
    NoteName.B: "B",
}


class Note:
    """表示一个音符（包含音名和八度）"""
    
    def __init__(self, name: NoteName, octave: int = 4):
        """
        初始化音符
        
        Args:
            name: 音名 (NoteName 枚举)
            octave: 八度号 (默认为4)
        """
        self.name = name
        self.octave = octave
    
    def __repr__(self) -> str:
        return f"Note({self.name}, {self.octave})"
    
    def __str__(self) -> str:
        return f"{_NOTE_NAMES_SHARP[self.name]}{self.octave}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Note):
            return self.name == other.name and self.octave == other.octave
        return False
    
    def __hash__(self) -> int:
        return hash((self.name, self.octave))
    
    def __lt__(self, other) -> bool:
        return self.midi() < other.midi()
    
    def __le__(self, other) -> bool:
        return self.midi() <= other.midi()
    
    def __gt__(self, other) -> bool:
        return self.midi() > other.midi()
    
    def __ge__(self, other) -> bool:
        return self.midi() >= other.midi()
    
    @property
    def sharp_name(self) -> str:
        """返回升号表示的音名"""
        return _NOTE_NAMES_SHARP[self.name]
    
    @property
    def flat_name(self) -> str:
        """返回降号表示的音名"""
        return _NOTE_NAMES_FLAT[self.name]
    
    def frequency(self) -> float:
        """
        计算音符频率 (Hz)
        使用十二平均律: f = 440 * 2^((n-69)/12)
        其中 n 是 MIDI 音符号
        """
        midi = self.midi()
        return 440.0 * (2 ** ((midi - 69) / 12.0))
    
    def midi(self) -> int:
        """
        返回 MIDI 音符号
        C4 = 60, A4 = 69
        """
        return self.octave * 12 + int(self.name) + 12
    
    def semitones_from(self, other: 'Note') -> int:
        """计算与另一个音符的半音距离"""
        return self.midi() - other.midi()
    
    def transpose(self, semitones: int) -> 'Note':
        """移调（按半音数）"""
        new_midi = self.midi() + semitones
        return Note.midi_to_note(new_midi)
    
    def interval_to(self, other: 'Note') -> 'Interval':
        """获取到另一个音符的音程"""
        semitones = other.semitones_from(self)
        return Interval.from_semitones(abs(semitones))
    
    @classmethod
    def midi_to_note(cls, midi: int) -> 'Note':
        """将 MIDI 音符号转换为音符"""
        octave = (midi - 12) // 12
        name = NoteName((midi - 12) % 12)
        return cls(name, octave)
    
    @classmethod
    def from_frequency(cls, freq: float) -> 'Note':
        """从频率获取最近的音符"""
        if freq <= 0:
            return cls(NoteName.A, 4)
        # f = 440 * 2^((n-69)/12)
        # n = 69 + 12 * log2(f/440)
        midi = 69 + 12 * math.log2(freq / 440.0)
        return cls.midi_to_note(int(round(midi)))
    
    @classmethod
    def cents_deviation(cls, freq: float) -> int:
        """
        计算频率与最近音符的音分偏差
        1 音分 = 1/100 半音
        """
        if freq <= 0:
            return 0
        midi_exact = 69 + 12 * math.log2(freq / 440.0)
        midi_nearest = round(midi_exact)
        return int(round((midi_exact - midi_nearest) * 100))


class Interval(IntEnum):
    """音程枚举"""
    UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    PERFECT_FOURTH = 5
    AUGMENTED_FOURTH = 6  # 减五度
    PERFECT_FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    OCTAVE = 12
    MINOR_NINTH = 13
    MAJOR_NINTH = 14
    MINOR_TENTH = 15
    MAJOR_TENTH = 16
    PERFECT_ELEVENTH = 17
    AUGMENTED_ELEVENTH = 18
    PERFECT_TWELFTH = 19
    MINOR_THIRTEENTH = 20
    MAJOR_THIRTEENTH = 21
    
    @classmethod
    def from_semitones(cls, semitones: int) -> 'Interval':
        """从半音数获取音程"""
        if semitones > 24:
            semitones = semitones % 12 + 12
        
        mapping = {
            0: cls.UNISON,
            1: cls.MINOR_SECOND,
            2: cls.MAJOR_SECOND,
            3: cls.MINOR_THIRD,
            4: cls.MAJOR_THIRD,
            5: cls.PERFECT_FOURTH,
            6: cls.AUGMENTED_FOURTH,
            7: cls.PERFECT_FIFTH,
            8: cls.MINOR_SIXTH,
            9: cls.MAJOR_SIXTH,
            10: cls.MINOR_SEVENTH,
            11: cls.MAJOR_SEVENTH,
            12: cls.OCTAVE,
            13: cls.MINOR_NINTH,
            14: cls.MAJOR_NINTH,
            15: cls.MINOR_TENTH,
            16: cls.MAJOR_TENTH,
            17: cls.PERFECT_ELEVENTH,
            18: cls.AUGMENTED_ELEVENTH,
            19: cls.PERFECT_TWELFTH,
            20: cls.MINOR_THIRTEENTH,
            21: cls.MAJOR_THIRTEENTH,
        }
        return mapping.get(semitones, cls.UNISON)
    
    def name_zh(self) -> str:
        """返回中文音程名称"""
        names = {
            Interval.UNISON: "纯一度",
            Interval.MINOR_SECOND: "小二度",
            Interval.MAJOR_SECOND: "大二度",
            Interval.MINOR_THIRD: "小三度",
            Interval.MAJOR_THIRD: "大三度",
            Interval.PERFECT_FOURTH: "纯四度",
            Interval.AUGMENTED_FOURTH: "增四度/减五度",
            Interval.PERFECT_FIFTH: "纯五度",
            Interval.MINOR_SIXTH: "小六度",
            Interval.MAJOR_SIXTH: "大六度",
            Interval.MINOR_SEVENTH: "小七度",
            Interval.MAJOR_SEVENTH: "大七度",
            Interval.OCTAVE: "纯八度",
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
        return names.get(self, "未知音程")
    
    def __str__(self) -> str:
        return self.name_zh()


class ScaleType(Enum):
    """音阶类型"""
    MAJOR = "major"
    MINOR = "minor"
    HARMONIC_MINOR = "harmonic_minor"
    MELODIC_MINOR = "melodic_minor"
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    LOCRIAN = "locrian"
    PENTATONIC_MAJOR = "pentatonic_major"
    PENTATONIC_MINOR = "pentatonic_minor"
    BLUES = "blues"
    CHROMATIC = "chromatic"
    WHOLE_TONE = "whole_tone"


# 音阶模式（从根音开始的半音数）
_SCALE_PATTERNS = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.MINOR: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11],
    ScaleType.MELODIC_MINOR: [0, 2, 3, 5, 7, 9, 11],
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
    ScaleType.LYDIAN: [0, 2, 4, 6, 7, 9, 11],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    ScaleType.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],
    ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],
    ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],
    ScaleType.BLUES: [0, 3, 5, 6, 7, 10],
    ScaleType.CHROMATIC: list(range(12)),
    ScaleType.WHOLE_TONE: [0, 2, 4, 6, 8, 10],
}

# 音阶名称
_SCALE_NAMES = {
    ScaleType.MAJOR: ("大调", "Major"),
    ScaleType.MINOR: ("自然小调", "Natural Minor"),
    ScaleType.HARMONIC_MINOR: ("和声小调", "Harmonic Minor"),
    ScaleType.MELODIC_MINOR: ("旋律小调", "Melodic Minor"),
    ScaleType.DORIAN: ("多利亚", "Dorian"),
    ScaleType.PHRYGIAN: ("弗里几亚", "Phrygian"),
    ScaleType.LYDIAN: ("利底亚", "Lydian"),
    ScaleType.MIXOLYDIAN: ("混合利底亚", "Mixolydian"),
    ScaleType.LOCRIAN: ("洛克利亚", "Locrian"),
    ScaleType.PENTATONIC_MAJOR: ("大调五声", "Major Pentatonic"),
    ScaleType.PENTATONIC_MINOR: ("小调五声", "Minor Pentatonic"),
    ScaleType.BLUES: ("布鲁斯", "Blues"),
    ScaleType.CHROMATIC: ("半音阶", "Chromatic"),
    ScaleType.WHOLE_TONE: ("全音阶", "Whole Tone"),
}


class Scale:
    """音阶类"""
    
    def __init__(self, root: NoteName, scale_type: ScaleType):
        """
        初始化音阶
        
        Args:
            root: 根音
            scale_type: 音阶类型
        """
        self.root = root
        self.scale_type = scale_type
    
    def __repr__(self) -> str:
        zh_name, en_name = _SCALE_NAMES[self.scale_type]
        return f"Scale({_NOTE_NAMES_SHARP[self.root]} {en_name})"
    
    def __str__(self) -> str:
        zh_name, en_name = _SCALE_NAMES[self.scale_type]
        return f"{_NOTE_NAMES_SHARP[self.root]} {zh_name}"
    
    @property
    def name(self) -> str:
        """返回音阶名称"""
        return str(self)
    
    @property
    def pattern(self) -> List[int]:
        """返回音阶模式（半音数）"""
        return _SCALE_PATTERNS[self.scale_type]
    
    def notes(self) -> List[NoteName]:
        """返回音阶内的音名（一个八度）"""
        pattern = self.pattern
        return [NoteName((int(self.root) + s) % 12) for s in pattern]
    
    def notes_with_octave(self, start_octave: int = 4, octaves: int = 1) -> List[Note]:
        """
        返回音阶内的音符（指定八度范围）
        
        Args:
            start_octave: 起始八度
            octaves: 八度数量
        
        Returns:
            音符列表
        """
        pattern = self.pattern
        notes = []
        for oct_num in range(octaves):
            for semitone in pattern:
                total_semitones = int(self.root) + semitone
                note_name = NoteName(total_semitones % 12)
                note_octave = start_octave + oct_num + (total_semitones // 12)
                notes.append(Note(note_name, note_octave))
        return notes
    
    def frequencies(self, start_octave: int = 4, octaves: int = 1) -> List[float]:
        """返回音阶内所有音符的频率"""
        return [n.frequency() for n in self.notes_with_octave(start_octave, octaves)]
    
    def contains_note(self, note: NoteName) -> bool:
        """检查音名是否在音阶内"""
        return note in self.notes()
    
    def contains_midi(self, midi: int) -> bool:
        """检查 MIDI 音符号是否在音阶内"""
        note = Note.midi_to_note(midi)
        return self.contains_note(note.name)
    
    def degree(self, degree_num: int) -> NoteName:
        """
        返回指定音阶级别的音名
        
        Args:
            degree_num: 音阶级别 (1-7，超出则循环)
        """
        notes = self.notes()
        degree_index = (degree_num - 1) % len(notes)
        return notes[degree_index]
    
    def triad(self, degree_num: int) -> 'Chord':
        """
        返回指定音阶级别上的三和弦
        
        Args:
            degree_num: 音阶级别 (1-7)
        """
        scale_notes = self.notes()
        root = scale_notes[(degree_num - 1) % len(scale_notes)]
        third = scale_notes[(degree_num - 1 + 2) % len(scale_notes)]
        fifth = scale_notes[(degree_num - 1 + 4) % len(scale_notes)]
        
        # 确定和弦类型
        third_semitones = (int(third) - int(root)) % 12
        fifth_semitones = (int(fifth) - int(root)) % 12
        
        if third_semitones == 4 and fifth_semitones == 7:
            chord_type = ChordType.MAJOR
        elif third_semitones == 3 and fifth_semitones == 7:
            chord_type = ChordType.MINOR
        elif third_semitones == 3 and fifth_semitones == 6:
            chord_type = ChordType.DIMINISHED
        elif third_semitones == 4 and fifth_semitones == 8:
            chord_type = ChordType.AUGMENTED
        else:
            chord_type = ChordType.MAJOR  # 默认
        
        return Chord(root, chord_type)
    
    @classmethod
    def major(cls, root: NoteName) -> 'Scale':
        """创建大调音阶"""
        return cls(root, ScaleType.MAJOR)
    
    @classmethod
    def minor(cls, root: NoteName) -> 'Scale':
        """创建自然小调音阶"""
        return cls(root, ScaleType.MINOR)
    
    @classmethod
    def blues(cls, root: NoteName) -> 'Scale':
        """创建布鲁斯音阶"""
        return cls(root, ScaleType.BLUES)
    
    @classmethod
    def pentatonic_major(cls, root: NoteName) -> 'Scale':
        """创建大调五声音阶"""
        return cls(root, ScaleType.PENTATONIC_MAJOR)
    
    @classmethod
    def pentatonic_minor(cls, root: NoteName) -> 'Scale':
        """创建小调五声音阶"""
        return cls(root, ScaleType.PENTATONIC_MINOR)


class ChordType(Enum):
    """和弦类型"""
    MAJOR = "major"
    MINOR = "minor"
    DIMINISHED = "dim"
    AUGMENTED = "aug"
    MAJOR_7 = "maj7"
    MINOR_7 = "m7"
    DOMINANT_7 = "7"
    DIMINISHED_7 = "dim7"
    HALF_DIMINISHED = "m7b5"
    SUS_2 = "sus2"
    SUS_4 = "sus4"
    MAJOR_6 = "6"
    MINOR_6 = "m6"
    MINOR_MAJOR_7 = "mmaj7"
    AUG_MAJOR_7 = "augmaj7"
    AUG_7 = "aug7"
    NINTH = "9"
    MINOR_9 = "m9"
    MAJOR_9 = "maj9"
    ELEVENTH = "11"
    MINOR_11 = "m11"
    MAJOR_11 = "maj11"
    THIRTEENTH = "13"
    MINOR_13 = "m13"
    MAJOR_13 = "maj13"
    ADD_9 = "add9"
    MINOR_ADD_9 = "madd9"
    POWER = "5"


# 和弦模式（从根音开始的半音数）
_CHORD_PATTERNS = {
    ChordType.MAJOR: [0, 4, 7],
    ChordType.MINOR: [0, 3, 7],
    ChordType.DIMINISHED: [0, 3, 6],
    ChordType.AUGMENTED: [0, 4, 8],
    ChordType.MAJOR_7: [0, 4, 7, 11],
    ChordType.MINOR_7: [0, 3, 7, 10],
    ChordType.DOMINANT_7: [0, 4, 7, 10],
    ChordType.DIMINISHED_7: [0, 3, 6, 9],
    ChordType.HALF_DIMINISHED: [0, 3, 6, 10],
    ChordType.SUS_2: [0, 2, 7],
    ChordType.SUS_4: [0, 5, 7],
    ChordType.MAJOR_6: [0, 4, 7, 9],
    ChordType.MINOR_6: [0, 3, 7, 9],
    ChordType.MINOR_MAJOR_7: [0, 3, 7, 11],
    ChordType.AUG_MAJOR_7: [0, 4, 8, 11],
    ChordType.AUG_7: [0, 4, 8, 10],
    ChordType.NINTH: [0, 4, 7, 10, 14],
    ChordType.MINOR_9: [0, 3, 7, 10, 14],
    ChordType.MAJOR_9: [0, 4, 7, 11, 14],
    ChordType.ELEVENTH: [0, 4, 7, 10, 14, 17],
    ChordType.MINOR_11: [0, 3, 7, 10, 14, 17],
    ChordType.MAJOR_11: [0, 4, 7, 11, 14, 17],
    ChordType.THIRTEENTH: [0, 4, 7, 10, 14, 17, 21],
    ChordType.MINOR_13: [0, 3, 7, 10, 14, 17, 21],
    ChordType.MAJOR_13: [0, 4, 7, 11, 14, 17, 21],
    ChordType.ADD_9: [0, 4, 7, 14],
    ChordType.MINOR_ADD_9: [0, 3, 7, 14],
    ChordType.POWER: [0, 7],
}

# 和弦名称
_CHORD_NAMES = {
    ChordType.MAJOR: ("大三和弦", "Major"),
    ChordType.MINOR: ("小三和弦", "Minor"),
    ChordType.DIMINISHED: ("减三和弦", "Diminished"),
    ChordType.AUGMENTED: ("增三和弦", "Augmented"),
    ChordType.MAJOR_7: ("大七和弦", "Major 7th"),
    ChordType.MINOR_7: ("小七和弦", "Minor 7th"),
    ChordType.DOMINANT_7: ("属七和弦", "Dominant 7th"),
    ChordType.DIMINISHED_7: ("减七和弦", "Diminished 7th"),
    ChordType.HALF_DIMINISHED: ("半减七和弦", "Half Diminished"),
    ChordType.SUS_2: ("挂二和弦", "Suspended 2nd"),
    ChordType.SUS_4: ("挂四和弦", "Suspended 4th"),
    ChordType.MAJOR_6: ("大六和弦", "Major 6th"),
    ChordType.MINOR_6: ("小六和弦", "Minor 6th"),
    ChordType.MINOR_MAJOR_7: ("小大七和弦", "Minor-Major 7th"),
    ChordType.AUG_MAJOR_7: ("增大七和弦", "Augmented Major 7th"),
    ChordType.AUG_7: ("增七和弦", "Augmented 7th"),
    ChordType.NINTH: ("九和弦", "9th"),
    ChordType.MINOR_9: ("小九和弦", "Minor 9th"),
    ChordType.MAJOR_9: ("大九和弦", "Major 9th"),
    ChordType.ELEVENTH: ("十一和弦", "11th"),
    ChordType.MINOR_11: ("小十一和弦", "Minor 11th"),
    ChordType.MAJOR_11: ("大十一和弦", "Major 11th"),
    ChordType.THIRTEENTH: ("十三和弦", "13th"),
    ChordType.MINOR_13: ("小十三和弦", "Minor 13th"),
    ChordType.MAJOR_13: ("大十三和弦", "Major 13th"),
    ChordType.ADD_9: ("加九和弦", "Add 9"),
    ChordType.MINOR_ADD_9: ("小加九和弦", "Minor Add 9"),
    ChordType.POWER: ("强力和弦", "Power"),
}

# 和弦符号
_CHORD_SYMBOLS = {
    ChordType.MAJOR: "",
    ChordType.MINOR: "m",
    ChordType.DIMINISHED: "dim",
    ChordType.AUGMENTED: "aug",
    ChordType.MAJOR_7: "maj7",
    ChordType.MINOR_7: "m7",
    ChordType.DOMINANT_7: "7",
    ChordType.DIMINISHED_7: "dim7",
    ChordType.HALF_DIMINISHED: "m7b5",
    ChordType.SUS_2: "sus2",
    ChordType.SUS_4: "sus4",
    ChordType.MAJOR_6: "6",
    ChordType.MINOR_6: "m6",
    ChordType.MINOR_MAJOR_7: "mmaj7",
    ChordType.AUG_MAJOR_7: "augmaj7",
    ChordType.AUG_7: "aug7",
    ChordType.NINTH: "9",
    ChordType.MINOR_9: "m9",
    ChordType.MAJOR_9: "maj9",
    ChordType.ELEVENTH: "11",
    ChordType.MINOR_11: "m11",
    ChordType.MAJOR_11: "maj11",
    ChordType.THIRTEENTH: "13",
    ChordType.MINOR_13: "m13",
    ChordType.MAJOR_13: "maj13",
    ChordType.ADD_9: "add9",
    ChordType.MINOR_ADD_9: "madd9",
    ChordType.POWER: "5",
}


class Chord:
    """和弦类"""
    
    def __init__(self, root: NoteName, chord_type: ChordType):
        """
        初始化和弦
        
        Args:
            root: 根音
            chord_type: 和弦类型
        """
        self.root = root
        self.chord_type = chord_type
    
    def __repr__(self) -> str:
        return f"Chord({self.root}, {self.chord_type})"
    
    def __str__(self) -> str:
        return f"{_NOTE_NAMES_SHARP[self.root]}{_CHORD_SYMBOLS[self.chord_type]}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Chord):
            return self.root == other.root and self.chord_type == other.chord_type
        return False
    
    def __hash__(self) -> int:
        return hash((self.root, self.chord_type))
    
    @property
    def name(self) -> str:
        """返回和弦名称"""
        return str(self)
    
    @property
    def full_name(self) -> str:
        """返回和弦完整名称"""
        zh_name, _ = _CHORD_NAMES[self.chord_type]
        return f"{_NOTE_NAMES_SHARP[self.root]}{zh_name}"
    
    @property
    def symbol(self) -> str:
        """返回和弦符号"""
        return _CHORD_SYMBOLS[self.chord_type]
    
    def notes(self) -> List[NoteName]:
        """返回和弦内音名"""
        pattern = _CHORD_PATTERNS[self.chord_type]
        return [NoteName((int(self.root) + s) % 12) for s in pattern]
    
    def notes_with_octave(self, octave: int = 4) -> List[Note]:
        """返回和弦内音符（包含八度）"""
        pattern = _CHORD_PATTERNS[self.chord_type]
        notes = []
        for semitone in pattern:
            total_semitones = int(self.root) + semitone
            note_name = NoteName(total_semitones % 12)
            note_octave = octave + (total_semitones // 12)
            notes.append(Note(note_name, note_octave))
        return notes
    
    def frequencies(self, octave: int = 4) -> List[float]:
        """返回和弦内音符的频率"""
        return [n.frequency() for n in self.notes_with_octave(octave)]
    
    def invert(self, inversion: int) -> 'ChordVoicing':
        """
        返回转位和弦
        
        Args:
            inversion: 转位次数 (0=原位, 1=第一转位, 2=第二转位...)
        """
        return ChordVoicing(self, inversion=inversion)
    
    @classmethod
    def identify(cls, notes: List[NoteName]) -> Optional['Chord']:
        """
        从音名列表识别和弦
        
        Args:
            notes: 音名列表
        
        Returns:
            识别出的和弦，如果无法识别则返回 None
        """
        if len(notes) < 2:
            return None
        
        # 去重并排序
        unique_notes = list(set(notes))
        sorted_notes = sorted(unique_notes, key=lambda n: int(n))
        
        # 尝试每个音作为根音
        for i, root in enumerate(sorted_notes):
            # 计算从根音到其他音的半音数
            intervals = []
            for note in sorted_notes:
                interval = (int(note) - int(root)) % 12
                if interval not in intervals:
                    intervals.append(interval)
            intervals.sort()
            
            # 与和弦模式匹配
            for chord_type, pattern in _CHORD_PATTERNS.items():
                normalized_pattern = sorted([s % 12 for s in pattern])
                if intervals == normalized_pattern:
                    return cls(root, chord_type)
        
        return None
    
    @classmethod
    def major(cls, root: NoteName) -> 'Chord':
        """创建大三和弦"""
        return cls(root, ChordType.MAJOR)
    
    @classmethod
    def minor(cls, root: NoteName) -> 'Chord':
        """创建小三和弦"""
        return cls(root, ChordType.MINOR)
    
    @classmethod
    def power(cls, root: NoteName) -> 'Chord':
        """创建强力和弦"""
        return cls(root, ChordType.POWER)
    
    @classmethod
    def dominant_7(cls, root: NoteName) -> 'Chord':
        """创建属七和弦"""
        return cls(root, ChordType.DOMINANT_7)


class ChordVoicing:
    """和弦排列/转位"""
    
    def __init__(self, chord: Chord, inversion: int = 0, octave: int = 4):
        """
        初始化和弦排列
        
        Args:
            chord: 和弦
            inversion: 转位 (0=原位, 1=第一转位, 2=第二转位...)
            octave: 基础八度
        """
        self.chord = chord
        self.inversion = inversion
        self.octave = octave
    
    def notes(self) -> List[Note]:
        """返回排列后的音符"""
        base_notes = self.chord.notes_with_octave(self.octave)
        if not base_notes:
            return []
        
        # 处理转位
        inversion = self.inversion % len(base_notes)
        for _ in range(inversion):
            # 将最低音移高一个八度
            lowest = base_notes.pop(0)
            base_notes.append(Note(lowest.name, lowest.octave + 1))
        
        return base_notes
    
    def frequencies(self) -> List[float]:
        """返回排列后的频率"""
        return [n.frequency() for n in self.notes()]


def circle_of_fifths() -> List[NoteName]:
    """
    返回五度圈
    C -> G -> D -> A -> E -> B -> F# -> C# -> G# -> D# -> A# -> F
    """
    return [
        NoteName.C, NoteName.G, NoteName.D, NoteName.A,
        NoteName.E, NoteName.B, NoteName.F_SHARP, NoteName.C_SHARP,
        NoteName.G_SHARP, NoteName.D_SHARP, NoteName.A_SHARP, NoteName.F
    ]


def circle_of_fourths() -> List[NoteName]:
    """
    返回四度圈
    C -> F -> Bb -> Eb -> Ab -> Db -> Gb -> B -> E -> A -> D -> G
    """
    return [
        NoteName.C, NoteName.F, NoteName.A_SHARP, NoteName.D_SHARP,
        NoteName.G_SHARP, NoteName.C_SHARP, NoteName.F_SHARP, NoteName.B,
        NoteName.E, NoteName.A, NoteName.D, NoteName.G
    ]


def relative_minor(major_key: NoteName) -> NoteName:
    """返回大调的关系小调"""
    return NoteName((int(major_key) + 9) % 12)


def relative_major(minor_key: NoteName) -> NoteName:
    """返回小调的关系大调"""
    return NoteName((int(minor_key) + 3) % 12)


def key_signature(key: NoteName, is_major: bool = True) -> List[NoteName]:
    """
    返回调号中的升降号
    
    Args:
        key: 调式主音
        is_major: 是否为大调
    
    Returns:
        升号或降号音名列表
    """
    # 升号顺序: F#, C#, G#, D#, A#, E#, B#
    sharps_order = [NoteName.F_SHARP, NoteName.C_SHARP, NoteName.G_SHARP,
                    NoteName.D_SHARP, NoteName.A_SHARP, NoteName.F, NoteName.C]
    # 降号顺序: Bb, Eb, Ab, Db, Gb, Cb, Fb
    flats_order = [NoteName.A_SHARP, NoteName.D_SHARP, NoteName.G_SHARP,
                   NoteName.C_SHARP, NoteName.F_SHARP, NoteName.B, NoteName.E]
    
    # 大调升号调: G, D, A, E, B, F#, C#
    sharp_keys = [NoteName.G, NoteName.D, NoteName.A, NoteName.E,
                  NoteName.B, NoteName.F_SHARP, NoteName.C_SHARP]
    # 大调降号调: F, Bb, Eb, Ab, Db, Gb, Cb
    flat_keys = [NoteName.F, NoteName.A_SHARP, NoteName.D_SHARP,
                 NoteName.G_SHARP, NoteName.C_SHARP, NoteName.F_SHARP, NoteName.B]
    
    if is_major:
        for i, k in enumerate(sharp_keys):
            if k == key:
                return sharps_order[:i + 1]
        for i, k in enumerate(flat_keys):
            if k == key:
                return flats_order[:i + 1]
    else:
        # 小调：找关系大调的调号
        rel_major = relative_major(key)
        return key_signature(rel_major, True)
    
    return []  # C 大调无升降号


# 节拍器相关常量
TEMPO_MARKINGS = {
    "larghissimo": (1, 24, "极广板"),
    "grave": (25, 45, "庄板"),
    "largo": (46, 60, "广板"),
    "lento": (61, 66, "慢板"),
    "adagio": (67, 76, "柔板"),
    "andante": (77, 108, "行板"),
    "moderato": (109, 120, "中板"),
    "allegretto": (121, 132, "小快板"),
    "allegro": (133, 168, "快板"),
    "vivace": (169, 192, "活泼的快板"),
    "presto": (193, 208, "急板"),
    "prestissimo": (209, 240, "最急板"),
}


def bpm_to_milliseconds(bpm: int) -> float:
    """
    将 BPM 转换为毫秒/拍
    
    Args:
        bpm: 每分钟拍数
    
    Returns:
        每拍的毫秒数
    """
    if bpm <= 0:
        return 0
    return 60000.0 / bpm


def bpm_to_seconds(bpm: int) -> float:
    """
    将 BPM 转换为秒/拍
    
    Args:
        bpm: 每分钟拍数
    
    Returns:
        每拍的秒数
    """
    if bpm <= 0:
        return 0
    return 60.0 / bpm


def milliseconds_to_bpm(ms: float) -> int:
    """将毫秒/拍转换为 BPM"""
    if ms <= 0:
        return 0
    return int(round(60000.0 / ms))


def seconds_to_bpm(seconds: float) -> int:
    """将秒/拍转换为 BPM"""
    if seconds <= 0:
        return 0
    return int(round(60.0 / seconds))


def get_tempo_marking(bpm: int) -> str:
    """
    根据 BPM 返回速度术语
    
    Args:
        bpm: 每分钟拍数
    
    Returns:
        速度术语
    """
    for name, (low, high, zh_name) in TEMPO_MARKINGS.items():
        if low <= bpm <= high:
            return f"{name.capitalize()} ({zh_name})"
    return "Unknown"


class NoteValue(Enum):
    """音符时值"""
    DOUBLE_WHOLE = 0.5  # 倍全音符
    WHOLE = 1.0  # 全音符
    HALF = 2.0  # 二分音符
    QUARTER = 4.0  # 四分音符
    EIGHTH = 8.0  # 八分音符
    SIXTEENTH = 16.0  # 十六分音符
    THIRTY_SECOND = 32.0  # 三十二分音符
    SIXTY_FOURTH = 64.0  # 六十四分音符
    
    def duration_beats(self) -> float:
        """返回以四分音符为单位的时值"""
        return 4.0 / self.value
    
    def duration_ms(self, bpm: int) -> float:
        """返回以毫秒为单位的时值"""
        quarter_ms = bpm_to_milliseconds(bpm)
        return quarter_ms * self.duration_beats()
    
    def duration_with_dots(self, dots: int) -> float:
        """
        返回带附点的时值
        
        Args:
            dots: 附点数量
        
        Returns:
            时值（以四分音符为单位）
        """
        base = self.duration_beats()
        result = base
        for i in range(dots):
            result += base / (2 ** (i + 1))
        return result


def harmonic_series(fundamental: float, harmonics: int = 16) -> List[float]:
    """
    生成泛音列
    
    Args:
        fundamental: 基频 (Hz)
        harmonics: 泛音数量
    
    Returns:
        泛音频率列表
    """
    return [fundamental * (n + 1) for n in range(harmonics)]


def equal_temperament_frequency(semitones_from_a4: int) -> float:
    """
    计算十二平均律频率
    
    Args:
        semitones_from_a4: 与 A4 (440Hz) 的半音距离
    
    Returns:
        频率 (Hz)
    """
    return 440.0 * (2 ** (semitones_from_a4 / 12.0))


def just_intonation_frequency(fundamental: float, ratio: Tuple[int, int]) -> float:
    """
    计算纯律频率
    
    Args:
        fundamental: 基频 (Hz)
        ratio: 频率比 (分子, 分母)
    
    Returns:
        纯律频率 (Hz)
    """
    return fundamental * ratio[0] / ratio[1]


# 常用纯律音程
JUST_INTERVALS = {
    "unison": (1, 1, "纯一度"),
    "minor_second": (16, 15, "小二度"),
    "major_second": (9, 8, "大二度"),
    "minor_third": (6, 5, "小三度"),
    "major_third": (5, 4, "大三度"),
    "perfect_fourth": (4, 3, "纯四度"),
    "tritone": (7, 5, "三全音"),
    "perfect_fifth": (3, 2, "纯五度"),
    "minor_sixth": (8, 5, "小六度"),
    "major_sixth": (5, 3, "大六度"),
    "minor_seventh": (7, 4, "小七度"),
    "major_seventh": (15, 8, "大七度"),
    "octave": (2, 1, "纯八度"),
}


def cents_deviation(equal_freq: float, just_freq: float) -> float:
    """
    计算两个频率之间的音分偏差
    
    Args:
        equal_freq: 平均律频率
        just_freq: 纯律频率
    
    Returns:
        音分偏差
    """
    if equal_freq <= 0 or just_freq <= 0:
        return 0
    return 1200 * math.log2(just_freq / equal_freq)


def beat_frequency(freq1: float, freq2: float) -> float:
    """
    计算两个频率的拍频
    
    Args:
        freq1: 第一个频率
        freq2: 第二个频率
    
    Returns:
        拍频 (Hz)
    """
    return abs(freq1 - freq2)


def semitones_to_ratio(semitones: int) -> float:
    """将半音数转换为频率比"""
    return 2 ** (semitones / 12.0)


def ratio_to_semitones(ratio: float) -> int:
    """将频率比转换为半音数"""
    return int(round(12 * math.log2(ratio)))


def parse_note(note_str: str) -> Note:
    """
    解析音符字符串
    
    Args:
        note_str: 音符字符串 (如 "C4", "A#5", "Db3", "C")
    
    Returns:
        Note 对象
    
    Raises:
        ValueError: 无效的音符格式
    """
    note_str = note_str.strip()
    if len(note_str) < 1:
        raise ValueError(f"Invalid note format: {note_str}")
    
    # 解析音名
    name_map = {
        'C': NoteName.C, 'C#': NoteName.C_SHARP, 'Db': NoteName.C_SHARP,
        'D': NoteName.D, 'D#': NoteName.D_SHARP, 'Eb': NoteName.D_SHARP,
        'E': NoteName.E,
        'F': NoteName.F, 'F#': NoteName.F_SHARP, 'Gb': NoteName.F_SHARP,
        'G': NoteName.G, 'G#': NoteName.G_SHARP, 'Ab': NoteName.G_SHARP,
        'A': NoteName.A, 'A#': NoteName.A_SHARP, 'Bb': NoteName.A_SHARP,
        'B': NoteName.B,
    }
    
    # 尝试匹配两个字符的音名（带升降号）
    note_part = None
    octave_part = None
    
    if len(note_str) >= 2 and note_str[:2] in name_map:
        note_part = note_str[:2]
        octave_part = note_str[2:]
    elif note_str[0] in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        note_part = note_str[0]
        octave_part = note_str[1:]
    else:
        raise ValueError(f"Invalid note name: {note_str}")
    
    name = name_map.get(note_part)
    if name is None:
        raise ValueError(f"Invalid note name: {note_part}")
    
    # 解析八度（默认为4）
    if not octave_part:
        octave = 4
    else:
        try:
            octave = int(octave_part)
        except ValueError:
            raise ValueError(f"Invalid octave: {octave_part}")
    
    return Note(name, octave)


def parse_chord(chord_str: str) -> Chord:
    """
    解析和弦字符串
    
    Args:
        chord_str: 和弦字符串 (如 "C", "Am", "G7", "Dm7", "F#m7b5")
    
    Returns:
        Chord 对象
    
    Raises:
        ValueError: 无效的和弦格式
    """
    chord_str = chord_str.strip()
    if not chord_str:
        raise ValueError("Empty chord string")
    
    # 解析根音
    root = None
    remaining = ""
    
    if len(chord_str) >= 2 and chord_str[:2] in ['C#', 'Db', 'D#', 'Eb', 
                                                   'F#', 'Gb', 'G#', 'Ab', 
                                                   'A#', 'Bb']:
        root_map = {
            'C#': NoteName.C_SHARP, 'Db': NoteName.C_SHARP,
            'D#': NoteName.D_SHARP, 'Eb': NoteName.D_SHARP,
            'F#': NoteName.F_SHARP, 'Gb': NoteName.F_SHARP,
            'G#': NoteName.G_SHARP, 'Ab': NoteName.G_SHARP,
            'A#': NoteName.A_SHARP, 'Bb': NoteName.A_SHARP,
        }
        root = root_map[chord_str[:2]]
        remaining = chord_str[2:]
    elif chord_str[0] in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        root_map = {
            'C': NoteName.C, 'D': NoteName.D, 'E': NoteName.E,
            'F': NoteName.F, 'G': NoteName.G,
            'A': NoteName.A, 'B': NoteName.B,
        }
        root = root_map[chord_str[0]]
        remaining = chord_str[1:]
    else:
        raise ValueError(f"Invalid root note: {chord_str}")
    
    # 默认大三和弦
    if not remaining:
        return Chord(root, ChordType.MAJOR)
    
    # 解析和弦类型
    chord_type_map = {
        'm': ChordType.MINOR,
        'min': ChordType.MINOR,
        '-': ChordType.MINOR,
        'dim': ChordType.DIMINISHED,
        '°': ChordType.DIMINISHED,
        'aug': ChordType.AUGMENTED,
        '+': ChordType.AUGMENTED,
        'maj7': ChordType.MAJOR_7,
        'M7': ChordType.MAJOR_7,
        'Δ7': ChordType.MAJOR_7,
        'm7': ChordType.MINOR_7,
        'min7': ChordType.MINOR_7,
        '-7': ChordType.MINOR_7,
        '7': ChordType.DOMINANT_7,
        'dom7': ChordType.DOMINANT_7,
        'dim7': ChordType.DIMINISHED_7,
        '°7': ChordType.DIMINISHED_7,
        'm7b5': ChordType.HALF_DIMINISHED,
        'ø7': ChordType.HALF_DIMINISHED,
        'sus2': ChordType.SUS_2,
        'sus4': ChordType.SUS_4,
        'sus': ChordType.SUS_4,
        '6': ChordType.MAJOR_6,
        'm6': ChordType.MINOR_6,
        '-6': ChordType.MINOR_6,
        'mmaj7': ChordType.MINOR_MAJOR_7,
        '-maj7': ChordType.MINOR_MAJOR_7,
        '5': ChordType.POWER,
        'add9': ChordType.ADD_9,
        'madd9': ChordType.MINOR_ADD_9,
        '9': ChordType.NINTH,
        'm9': ChordType.MINOR_9,
        'maj9': ChordType.MAJOR_9,
        '11': ChordType.ELEVENTH,
        'm11': ChordType.MINOR_11,
        'maj11': ChordType.MAJOR_11,
        '13': ChordType.THIRTEENTH,
        'm13': ChordType.MINOR_13,
        'maj13': ChordType.MAJOR_13,
    }
    
    # 尝试匹配（按长度降序）
    for suffix in sorted(chord_type_map.keys(), key=len, reverse=True):
        if remaining == suffix or remaining.startswith(suffix):
            return Chord(root, chord_type_map[suffix])
    
    raise ValueError(f"Unknown chord type: {remaining}")


def fret_positions(string_note: Note, frets: int = 24) -> List[Note]:
    """
    计算弦乐器品格上的音符
    
    Args:
        string_note: 弦的空弦音
        frets: 品格数
    
    Returns:
        音符列表
    """
    return [string_note.transpose(f) for f in range(frets + 1)]


def guitar_standard_tuning() -> List[Note]:
    """返回吉他标准调弦的音符 (EADGBE)"""
    return [
        Note(NoteName.E, 2),  # 6弦
        Note(NoteName.A, 2),  # 5弦
        Note(NoteName.D, 3),  # 4弦
        Note(NoteName.G, 3),  # 3弦
        Note(NoteName.B, 3),  # 2弦
        Note(NoteName.E, 4),  # 1弦
    ]


def bass_standard_tuning() -> List[Note]:
    """返回贝斯标准调弦的音符 (EADG)"""
    return [
        Note(NoteName.E, 1),
        Note(NoteName.A, 1),
        Note(NoteName.D, 2),
        Note(NoteName.G, 2),
    ]


def ukulele_standard_tuning() -> List[Note]:
    """返回尤克里里标准调弦的音符 (GCEA)"""
    return [
        Note(NoteName.G, 4),
        Note(NoteName.C, 4),
        Note(NoteName.E, 4),
        Note(NoteName.A, 4),
    ]


def piano_key_to_note(key_number: int) -> Note:
    """
    将钢琴键号转换为音符
    
    Args:
        key_number: 钢琴键号 (1-88, 1=A0, 88=C8)
    
    Returns:
        Note 对象
    """
    # A0 = MIDI 21, 钢琴键号 1
    midi = key_number + 20
    return Note.midi_to_note(midi)


def note_to_piano_key(note: Note) -> int:
    """
    将音符转换为钢琴键号
    
    Args:
        note: Note 对象
    
    Returns:
        钢琴键号 (1-88)
    """
    return note.midi() - 20


# 钢琴所有键的频率 (A0 = 27.5 Hz)
def piano_frequencies() -> List[float]:
    """返回钢琴 88 键的频率列表"""
    return [Note.midi_to_note(21 + i).frequency() for i in range(88)]


# 导出主要类和函数
__all__ = [
    # 枚举
    'NoteName', 'Interval', 'ScaleType', 'ChordType', 'NoteValue',
    # 类
    'Note', 'Scale', 'Chord', 'ChordVoicing',
    # 音符函数
    'parse_note', 'parse_chord',
    # 音阶函数
    'circle_of_fifths', 'circle_of_fourths',
    'relative_minor', 'relative_major', 'key_signature',
    # 频率函数
    'equal_temperament_frequency', 'just_intonation_frequency',
    'harmonic_series', 'cents_deviation', 'beat_frequency',
    'semitones_to_ratio', 'ratio_to_semitones',
    # 节拍器函数
    'bpm_to_milliseconds', 'bpm_to_seconds',
    'milliseconds_to_bpm', 'seconds_to_bpm',
    'get_tempo_marking',
    # 乐器函数
    'fret_positions', 'guitar_standard_tuning',
    'bass_standard_tuning', 'ukulele_standard_tuning',
    'piano_key_to_note', 'note_to_piano_key', 'piano_frequencies',
    # 常量
    'JUST_INTERVALS', 'TEMPO_MARKINGS',
]