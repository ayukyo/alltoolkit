"""
Music Chord and Scale Utilities
音乐和弦与音阶工具

功能:
- 音符处理（音名、MIDI编号、频率转换）
- 和弦识别与生成（大三、小三、属七、大七等）
- 音阶生成（大调、小调、五声、蓝调等）
- 音程计算（半音数、音程名称）
- 和弦转位
- 调号识别
- 零依赖，纯 Python 标准库实现
"""

from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


class NoteName(Enum):
    """音符名称（使用升号表示）"""
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


# 音符名称映射
NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# 音符别名
NOTE_ALIASES = {
    'C#': 'C#', 'Db': 'C#',
    'D#': 'D#', 'Eb': 'D#',
    'F#': 'F#', 'Gb': 'F#',
    'G#': 'G#', 'Ab': 'G#',
    'A#': 'A#', 'Bb': 'A#',
}


@dataclass
class Chord:
    """和弦"""
    root: str  # 根音
    quality: str  # 和弦品质 (major, minor, dim, aug, 7, maj7, m7, etc.)
    notes: List[str]  # 和弦音
    symbol: str  # 和弦符号


@dataclass
class Interval:
    """音程"""
    semitones: int
    name: str
    short_name: str
    abbreviation: str


# 音程表（从根音开始的半音数）
INTERVALS = {
    0: Interval(0, "纯一度", "P1", "P1"),
    1: Interval(1, "小二度", "m2", "m2"),
    2: Interval(2, "大二度", "M2", "M2"),
    3: Interval(3, "小三度", "m3", "m3"),
    4: Interval(4, "大三度", "M3", "M3"),
    5: Interval(5, "纯四度", "P4", "P4"),
    6: Interval(6, "增四度/减五度", "A4/d5", "TT"),
    7: Interval(7, "纯五度", "P5", "P5"),
    8: Interval(8, "小六度", "m6", "m6"),
    9: Interval(9, "大六度", "M6", "M6"),
    10: Interval(10, "小七度", "m7", "m7"),
    11: Interval(11, "大七度", "M7", "M7"),
    12: Interval(12, "纯八度", "P8", "P8"),
    13: Interval(13, "小九度", "m9", "m9"),
    14: Interval(14, "大九度", "M9", "M9"),
}

# 和弦公式（相对于根音的半音数）
CHORD_FORMULAS = {
    'major': [0, 4, 7],           # 大三和弦
    'minor': [0, 3, 7],           # 小三和弦
    'dim': [0, 3, 6],             # 减三和弦
    'aug': [0, 4, 8],             # 增三和弦
    'sus2': [0, 2, 7],            # 挂二和弦
    'sus4': [0, 5, 7],            # 挂四和弦
    '7': [0, 4, 7, 10],           # 属七和弦
    'maj7': [0, 4, 7, 11],        # 大七和弦
    'm7': [0, 3, 7, 10],          # 小七和弦
    'm7b5': [0, 3, 6, 10],        # 半减七和弦
    'dim7': [0, 3, 6, 9],         # 减七和弦
    'add9': [0, 4, 7, 14],        # add9和弦
    '6': [0, 4, 7, 9],            # 大六和弦
    'm6': [0, 3, 7, 9],           # 小六和弦
    '9': [0, 4, 7, 10, 14],       # 属九和弦
    'maj9': [0, 4, 7, 11, 14],    # 大九和弦
    'm9': [0, 3, 7, 10, 14],      # 小九和弦
    '11': [0, 4, 7, 10, 14, 17], # 属十一和弦
    '13': [0, 4, 7, 10, 14, 17, 21], # 属十三和弦
    'power': [0, 7],              # 强力和弦（根音+五音）
}

# 和弦品质名称映射
CHORD_QUALITY_NAMES = {
    'major': '大三和弦',
    'minor': '小三和弦',
    'dim': '减三和弦',
    'aug': '增三和弦',
    'sus2': '挂二和弦',
    'sus4': '挂四和弦',
    '7': '属七和弦',
    'maj7': '大七和弦',
    'm7': '小七和弦',
    'm7b5': '半减七和弦',
    'dim7': '减七和弦',
    'add9': 'add9和弦',
    '6': '大六和弦',
    'm6': '小六和弦',
    '9': '属九和弦',
    'maj9': '大九和弦',
    'm9': '小九和弦',
    '11': '属十一和弦',
    '13': '属十三和弦',
    'power': '强力和弦',
}

# 音阶公式（相对于根音的半音数）
SCALE_FORMULAS = {
    'major': [0, 2, 4, 5, 7, 9, 11],              # 自然大调
    'natural_minor': [0, 2, 3, 5, 7, 8, 10],      # 自然小调
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],     # 和声小调
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],      # 旋律小调（上行）
    'pentatonic_major': [0, 2, 4, 7, 9],          # 大调五声
    'pentatonic_minor': [0, 3, 5, 7, 10],         # 小调五声
    'blues': [0, 3, 5, 6, 7, 10],                 # 蓝调音阶
    'dorian': [0, 2, 3, 5, 7, 9, 10],             # 多利亚调式
    'phrygian': [0, 1, 3, 5, 7, 8, 10],           # 弗里吉亚调式
    'lydian': [0, 2, 4, 6, 7, 9, 11],            # 利底亚调式
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],        # 混合利底亚调式
    'locrian': [0, 1, 3, 5, 6, 8, 10],           # 洛克里亚调式
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # 半音阶
    'whole_tone': [0, 2, 4, 6, 8, 10],            # 全音阶
    'diminished': [0, 2, 3, 5, 6, 8, 9, 11],     # 减音阶
}

# 音阶名称映射
SCALE_NAMES = {
    'major': '自然大调',
    'natural_minor': '自然小调',
    'harmonic_minor': '和声小调',
    'melodic_minor': '旋律小调',
    'pentatonic_major': '大调五声',
    'pentatonic_minor': '小调五声',
    'blues': '蓝调音阶',
    'dorian': '多利亚调式',
    'phrygian': '弗里吉亚调式',
    'lydian': '利底亚调式',
    'mixolydian': '混合利底亚调式',
    'locrian': '洛克里亚调式',
    'chromatic': '半音阶',
    'whole_tone': '全音阶',
    'diminished': '减音阶',
}

# 调号（升号调/降号调）
KEY_SIGNATURES_SHARP = ['G', 'D', 'A', 'E', 'B', 'F#', 'C#']
KEY_SIGNATURES_FLAT = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']


def normalize_note(note: str) -> str:
    """
    标准化音符名称为升号表示
    
    Args:
        note: 音符名称 (C, C#, Db, D, etc.)
    
    Returns:
        标准化后的音符名称 (使用升号)
    
    Examples:
        >>> normalize_note('Db')
        'C#'
        >>> normalize_note('C')
        'C'
    """
    note = note.strip().capitalize()
    if note in NOTE_ALIASES:
        return NOTE_ALIASES[note]
    if note in NOTE_NAMES_SHARP:
        return note
    raise ValueError(f"Invalid note: {note}")


def note_to_semitone(note: str) -> int:
    """
    将音符名称转换为半音编号 (C=0, C#=1, ..., B=11)
    
    Args:
        note: 音符名称
    
    Returns:
        半音编号 (0-11)
    
    Examples:
        >>> note_to_semitone('C')
        0
        >>> note_to_semitone('A')
        9
    """
    note = normalize_note(note)
    return NOTE_NAMES_SHARP.index(note)


def semitone_to_note(semitone: int, use_flat: bool = False) -> str:
    """
    将半音编号转换为音符名称
    
    Args:
        semitone: 半音编号 (0-11)
        use_flat: 是否使用降号表示
    
    Returns:
        音符名称
    
    Examples:
        >>> semitone_to_note(0)
        'C'
        >>> semitone_to_note(1, use_flat=True)
        'Db'
    """
    semitone = semitone % 12
    return NOTE_NAMES_FLAT[semitone] if use_flat else NOTE_NAMES_SHARP[semitone]


def midi_to_note(midi_number: int, use_flat: bool = False) -> str:
    """
    将 MIDI 编号转换为音符名称（含八度）
    
    Args:
        midi_number: MIDI 编号 (0-127)
        use_flat: 是否使用降号表示
    
    Returns:
        音符名称（如 C4, A#3）
    
    Examples:
        >>> midi_to_note(60)
        'C4'
        >>> midi_to_note(61)
        'C#4'
    """
    if not 0 <= midi_number <= 127:
        raise ValueError(f"MIDI number must be 0-127, got {midi_number}")
    
    octave = (midi_number // 12) - 1
    semitone = midi_number % 12
    note = NOTE_NAMES_FLAT[semitone] if use_flat else NOTE_NAMES_SHARP[semitone]
    return f"{note}{octave}"


def note_to_midi(note: str) -> int:
    """
    将音符名称（含八度）转换为 MIDI 编号
    
    Args:
        note: 音符名称（如 C4, A#3）
    
    Returns:
        MIDI 编号 (0-127)
    
    Examples:
        >>> note_to_midi('C4')
        60
        >>> note_to_midi('A4')
        69
    """
    note = note.strip()
    
    # 分离音符和八度
    if len(note) < 2:
        raise ValueError(f"Invalid note format: {note}")
    
    # 处理如 C#4, Bb3 等情况
    if note[1] in '#b':
        note_name = note[:2]
        octave = int(note[2:])
    else:
        note_name = note[0]
        octave = int(note[1:])
    
    semitone = note_to_semitone(note_name)
    midi = (octave + 1) * 12 + semitone
    
    if not 0 <= midi <= 127:
        raise ValueError(f"Resulting MIDI number out of range: {midi}")
    
    return midi


def note_to_frequency(note: str, a4_freq: float = 440.0) -> float:
    """
    将音符名称转换为频率（Hz）
    
    Args:
        note: 音符名称（如 A4, C#5）
        a4_freq: A4 的频率（默认 440 Hz）
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> round(note_to_frequency('A4'), 2)
        440.0
        >>> round(note_to_frequency('A5'), 2)
        880.0
    """
    midi = note_to_midi(note)
    return midi_to_frequency(midi, a4_freq)


def midi_to_frequency(midi_number: int, a4_freq: float = 440.0) -> float:
    """
    将 MIDI 编号转换为频率（Hz）
    
    Args:
        midi_number: MIDI 编号 (0-127)
        a4_freq: A4 的频率（默认 440 Hz）
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> round(midi_to_frequency(69), 2)
        440.0
    """
    return a4_freq * (2 ** ((midi_number - 69) / 12))


def frequency_to_midi(frequency: float, a4_freq: float = 440.0) -> int:
    """
    将频率（Hz）转换为最近的 MIDI 编号
    
    Args:
        frequency: 频率 (Hz)
        a4_freq: A4 的频率（默认 440 Hz）
    
    Returns:
        MIDI 编号
    
    Examples:
        >>> frequency_to_midi(440)
        69
        >>> frequency_to_midi(880)
        81
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    
    import math
    midi = 69 + 12 * math.log2(frequency / a4_freq)
    return round(midi)


def get_interval(semitones: int) -> Interval:
    """
    获取音程信息
    
    Args:
        semitones: 半音数（可以是0-12或更多）
    
    Returns:
        音程对象
    
    Examples:
        >>> get_interval(7).name
        '纯五度'
        >>> get_interval(12).name
        '纯八度'
    """
    # 先检查完全匹配（如12 = 纯八度）
    if semitones in INTERVALS:
        return INTERVALS[semitones]
    
    # 对于超出范围的值，取模后查找
    semitones_in_octave = semitones % 12
    
    if semitones_in_octave not in INTERVALS:
        raise ValueError(f"No interval for {semitones} semitones")
    
    return INTERVALS[semitones_in_octave]


def calculate_interval(note1: str, note2: str) -> Interval:
    """
    计算两个音符之间的音程
    
    Args:
        note1: 第一个音符（不含八度）
        note2: 第二个音符（不含八度）
    
    Returns:
        音程对象
    
    Examples:
        >>> calculate_interval('C', 'G').name
        '纯五度'
        >>> calculate_interval('C', 'E').name
        '大三度'
    """
    s1 = note_to_semitone(note1)
    s2 = note_to_semitone(note2)
    diff = (s2 - s1) % 12
    return get_interval(diff)


def build_chord(root: str, quality: str = 'major') -> Chord:
    """
    构建和弦
    
    Args:
        root: 根音
        quality: 和弦品质 (major, minor, 7, maj7, etc.)
    
    Returns:
        和弦对象
    
    Examples:
        >>> build_chord('C', 'major').notes
        ['C', 'E', 'G']
        >>> build_chord('A', 'm7').notes
        ['A', 'C', 'E', 'G']
    """
    root = normalize_note(root)
    
    # 处理质量名称（支持 m 代替 minor 等）
    quality_map = {
        'm': 'minor',
        'min': 'minor',
        'M': 'major',
        'maj': 'major',
        '': 'major',
    }
    quality = quality_map.get(quality, quality)
    
    if quality not in CHORD_FORMULAS:
        raise ValueError(f"Unknown chord quality: {quality}")
    
    formula = CHORD_FORMULAS[quality]
    root_semitone = note_to_semitone(root)
    
    notes = []
    for interval in formula:
        note_semitone = (root_semitone + interval) % 12
        notes.append(semitone_to_note(note_semitone))
    
    # 生成和弦符号
    symbol = root
    if quality == 'major':
        symbol = root  # 大三和弦通常不写后缀
    elif quality == 'minor':
        symbol = f"{root}m"
    else:
        symbol = f"{root}{quality}"
    
    return Chord(
        root=root,
        quality=quality,
        notes=notes,
        symbol=symbol
    )


def identify_chord(notes: List[str]) -> Optional[Tuple[str, str]]:
    """
    识别和弦类型
    
    Args:
        notes: 音符列表（至少2个音）
    
    Returns:
        (根音, 和弦品质) 或 None（如果无法识别）
    
    注意：假设第一个音符为根音进行识别
    
    Examples:
        >>> identify_chord(['C', 'E', 'G'])
        ('C', 'major')
        >>> identify_chord(['A', 'C', 'E', 'G'])
        ('A', 'm7')
    """
    if len(notes) < 2:
        return None
    
    # 标准化音符
    notes = [normalize_note(n) for n in notes]
    
    # 转换为半音编号并去重
    semitones = list(set(note_to_semitone(n) for n in notes))
    
    # 首先尝试第一个音符作为根音
    first_note = notes[0]
    root_semitone = note_to_semitone(first_note)
    
    intervals = [(s - root_semitone) % 12 for s in semitones]
    intervals_sorted = sorted(set(intervals))
    
    # 匹配和弦公式
    for quality, formula in CHORD_FORMULAS.items():
        formula_mod = sorted(set(f % 12 for f in formula))
        
        if formula_mod == intervals_sorted:
            return (first_note, quality)
    
    # 如果第一个音符不匹配，尝试其他音作为根音
    for root in semitones:
        if root == root_semitone:
            continue  # 已经尝试过
        
        intervals = [(s - root) % 12 for s in semitones]
        intervals_sorted = sorted(set(intervals))
        
        for quality, formula in CHORD_FORMULAS.items():
            formula_mod = sorted(set(f % 12 for f in formula))
            
            if formula_mod == intervals_sorted:
                root_note = semitone_to_note(root)
                return (root_note, quality)
    
    return None


def invert_chord(notes: List[str], inversion: int) -> List[str]:
    """
    和弦转位
    
    Args:
        notes: 和弦音列表（按根音、三音、五音...顺序）
        inversion: 转位次数 (0=原位, 1=第一转位, 2=第二转位...)
    
    Returns:
        转位后的和弦音列表
    
    Examples:
        >>> invert_chord(['C', 'E', 'G'], 1)
        ['E', 'G', 'C']
        >>> invert_chord(['C', 'E', 'G'], 2)
        ['G', 'C', 'E']
    """
    if not notes:
        return notes
    
    notes = [normalize_note(n) for n in notes]
    inversion = inversion % len(notes)
    
    return notes[inversion:] + notes[:inversion]


def get_chord_inversions(root: str, quality: str = 'major') -> List[List[str]]:
    """
    获取和弦的所有转位
    
    Args:
        root: 根音
        quality: 和弦品质
    
    Returns:
        所有转位的列表
    
    Examples:
        >>> get_chord_inversions('C', 'major')
        [['C', 'E', 'G'], ['E', 'G', 'C'], ['G', 'C', 'E']]
    """
    chord = build_chord(root, quality)
    return [invert_chord(chord.notes, i) for i in range(len(chord.notes))]


def build_scale(root: str, scale_type: str = 'major') -> List[str]:
    """
    构建音阶
    
    Args:
        root: 根音
        scale_type: 音阶类型 (major, minor, pentatonic_major, etc.)
    Returns:
        音阶音符列表
    
    Examples:
        >>> build_scale('C', 'major')
        ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        >>> build_scale('A', 'natural_minor')
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    """
    root = normalize_note(root)
    
    # 处理音阶类型别名
    scale_map = {
        'minor': 'natural_minor',
        'nat_minor': 'natural_minor',
        'pentatonic': 'pentatonic_major',
        'min_pentatonic': 'pentatonic_minor',
    }
    scale_type = scale_map.get(scale_type, scale_type)
    
    if scale_type not in SCALE_FORMULAS:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    formula = SCALE_FORMULAS[scale_type]
    root_semitone = note_to_semitone(root)
    
    notes = []
    for interval in formula:
        note_semitone = (root_semitone + interval) % 12
        notes.append(semitone_to_note(note_semitone))
    
    return notes


def get_scale_degrees(scale_type: str = 'major') -> List[str]:
    """
    获取音阶的度数名称
    
    Args:
        scale_type: 音阶类型
    
    Returns:
        度数名称列表
    
    Examples:
        >>> get_scale_degrees('major')
        ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    """
    if scale_type not in SCALE_FORMULAS:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    degree_names = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    return degree_names[:len(SCALE_FORMULAS[scale_type])]


def get_diatonic_chords(root: str, scale_type: str = 'major') -> List[Chord]:
    """
    获取调内顺阶和弦
    
    Args:
        root: 根音
        scale_type: 音阶类型
    
    Returns:
        顺阶和弦列表
    
    Examples:
        >>> len(get_diatonic_chords('C', 'major'))
        7
    """
    scale = build_scale(root, scale_type)
    
    # 大调顺阶和弦类型
    major_chord_qualities = ['major', 'minor', 'minor', 'major', 'major', 'minor', 'dim']
    minor_chord_qualities = ['minor', 'dim', 'major', 'minor', 'minor', 'major', 'major']
    
    if scale_type == 'major':
        qualities = major_chord_qualities
    elif scale_type in ['natural_minor', 'minor']:
        qualities = minor_chord_qualities
    else:
        # 默认使用大调顺阶和弦
        qualities = major_chord_qualities
    
    chords = []
    for i, note in enumerate(scale):
        if i < len(qualities):
            chord = build_chord(note, qualities[i])
            chords.append(chord)
    
    return chords


def get_key_signature(root: str, scale_type: str = 'major') -> Tuple[List[str], bool]:
    """
    获取调号
    
    Args:
        root: 根音
        scale_type: 音阶类型
    
    Returns:
        (变化音列表, 是否升号调)
    
    Examples:
        >>> get_key_signature('G', 'major')
        (['F#'], True)
        >>> get_key_signature('F', 'major')
        (['Bb'], False)
    """
    root = normalize_note(root)
    
    # 升号调顺序：F# C# G# D# A# E# B#
    sharp_order = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#']
    # 降号调顺序：Bb Eb Ab Db Gb Cb Fb
    flat_order = ['Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb']
    
    # 升号调根音列表
    sharp_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    # 降号调根音列表
    flat_keys = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    
    if root in sharp_keys:
        # 升号调
        index = sharp_keys.index(root)
        accidentals = sharp_order[:index]
        return (accidentals, True)
    elif root in flat_keys:
        # 降号调
        index = flat_keys.index(root)
        accidentals = flat_order[:index]
        return (accidentals, False)
    else:
        # 其他情况，使用音阶计算
        scale = build_scale(root, scale_type)
        accidentals = [note for note in scale if '#' in note or 'b' in note]
        has_sharps = any('#' in note for note in accidentals)
        return (accidentals, has_sharps)


def transpose_note(note: str, semitones: int) -> str:
    """
    移调
    
    Args:
        note: 音符名称
        semitones: 移动的半音数（正数升高，负数降低）
    
    Returns:
        移调后的音符
    
    Examples:
        >>> transpose_note('C', 2)
        'D'
        >>> transpose_note('E', -1)
        'D#'
    """
    note = normalize_note(note)
    semitone = note_to_semitone(note)
    new_semitone = (semitone + semitones) % 12
    return semitone_to_note(new_semitone)


def transpose_chord(chord_symbol: str, semitones: int) -> str:
    """
    移调和弦符号
    
    Args:
        chord_symbol: 和弦符号（如 Cm7, G, Dmaj7）
        semitones: 移动的半音数
    
    Returns:
        移调后的和弦符号
    
    Examples:
        >>> transpose_chord('C', 2)
        'D'
        >>> transpose_chord('Am7', 3)
        'Cm7'
    """
    chord_symbol = chord_symbol.strip()
    
    # 提取根音和后缀
    if len(chord_symbol) >= 2 and chord_symbol[1] in '#b':
        root = chord_symbol[:2]
        suffix = chord_symbol[2:]
    else:
        root = chord_symbol[0]
        suffix = chord_symbol[1:]
    
    new_root = transpose_note(root, semitones)
    return f"{new_root}{suffix}"


def get_relative_key(root: str, scale_type: str = 'major') -> Tuple[str, str]:
    """
    获取关系调
    
    Args:
        root: 根音
        scale_type: 音阶类型
    
    Returns:
        (关系调根音, 关系调类型)
    
    Examples:
        >>> get_relative_key('C', 'major')
        ('A', 'natural_minor')
        >>> get_relative_key('A', 'minor')
        ('C', 'major')
    """
    root = normalize_note(root)
    scale_type = scale_type.replace('natural_', '').replace('_', '')
    
    if scale_type == 'major':
        # 大调的关系小调：下移小三度
        relative_root = transpose_note(root, -3)
        return (relative_root, 'natural_minor')
    elif scale_type == 'minor':
        # 小调的关系大调：上移小三度
        relative_root = transpose_note(root, 3)
        return (relative_root, 'major')
    else:
        raise ValueError(f"No relative key for scale type: {scale_type}")


def get_enharmonic(note: str) -> str:
    """
    获取等音（如 C# 和 Db）
    
    Args:
        note: 音符名称
    
    Returns:
        等音名称（升号音符返回降号表示，降号音符返回升号表示）
    
    Examples:
        >>> get_enharmonic('C#')
        'Db'
        >>> get_enharmonic('Db')
        'C#'
        >>> get_enharmonic('F#')
        'Gb'
    """
    # 保留原始输入的升降号信息
    original_note = note.strip().capitalize()
    
    # 获取半音编号
    semitone = note_to_semitone(note)
    
    # 获取升号和降号表示
    sharp_note = NOTE_NAMES_SHARP[semitone]
    flat_note = NOTE_NAMES_FLAT[semitone]
    
    # 如果这两个相同，说明是自然音，没有等音变化
    if sharp_note == flat_note:
        return original_note  # 自然音没有等音变化
    
    # 检查原始输入是升号还是降号
    if '#' in original_note:
        return flat_note  # 升号 -> 返回降号
    elif 'b' in original_note.lower():
        return sharp_note  # 降号 -> 返回升号
    else:
        # 自然音作为输入（经过normalize后变成升号表示）
        return flat_note  # 默认返回降号等音（如果是变化音）


def is_diatonic(note: str, root: str, scale_type: str = 'major') -> bool:
    """
    判断音符是否属于某调的调内音
    
    Args:
        note: 音符名称
        root: 调的根音
        scale_type: 音阶类型
    
    Returns:
        是否为调内音
    
    Examples:
        >>> is_diatonic('E', 'C', 'major')
        True
        >>> is_diatonic('F#', 'C', 'major')
        False
    """
    note = normalize_note(note)
    scale = build_scale(root, scale_type)
    return note in scale


def get_note_name_variants(note: str) -> Set[str]:
    """
    获取音符的所有可能表示方式
    
    Args:
        note: 音符名称
    
    Returns:
        所有可能的音符名称
    
    Examples:
        >>> get_note_name_variants('C#')
        {'C#', 'Db'}
    """
    note = normalize_note(note)
    semitone = note_to_semitone(note)
    
    variants = set()
    variants.add(NOTE_NAMES_SHARP[semitone])
    variants.add(NOTE_NAMES_FLAT[semitone])
    
    return variants


def parse_chord_symbol(symbol: str) -> Tuple[str, str]:
    """
    解析和弦符号
    
    Args:
        symbol: 和弦符号（如 Cm7, Gmaj7, D7）
    
    Returns:
        (根音, 和弦品质)
    
    Examples:
        >>> parse_chord_symbol('Cm7')
        ('C', 'm7')
        >>> parse_chord_symbol('G')
        ('G', 'major')
    """
    symbol = symbol.strip()
    
    if not symbol:
        raise ValueError("Empty chord symbol")
    
    # 提取根音
    if len(symbol) >= 2 and symbol[1] in '#b':
        root = symbol[:2]
        remainder = symbol[2:]
    else:
        root = symbol[0]
        remainder = symbol[1:]
    
    # 解析后缀
    if not remainder:
        quality = 'major'
    elif remainder == 'm' or remainder == 'min':
        quality = 'minor'
    elif remainder == 'dim':
        quality = 'dim'
    elif remainder == 'aug' or remainder == '+':
        quality = 'aug'
    elif remainder == '7':
        quality = '7'
    elif remainder in ['maj7', 'M7']:
        quality = 'maj7'
    elif remainder in ['m7', 'min7']:
        quality = 'm7'
    elif remainder == 'm7b5':
        quality = 'm7b5'
    elif remainder == 'dim7':
        quality = 'dim7'
    elif remainder == 'sus2':
        quality = 'sus2'
    elif remainder == 'sus4':
        quality = 'sus4'
    elif remainder == 'add9':
        quality = 'add9'
    elif remainder == '6':
        quality = '6'
    elif remainder in ['m6', 'min6']:
        quality = 'm6'
    elif remainder == '5' or remainder == 'power':
        quality = 'power'
    elif remainder == '9':
        quality = '9'
    elif remainder == 'maj9':
        quality = 'maj9'
    elif remainder in ['m9', 'min9']:
        quality = 'm9'
    elif remainder == '11':
        quality = '11'
    elif remainder == '13':
        quality = '13'
    else:
        # 尝试直接使用
        quality = remainder
    
    return (normalize_note(root), quality)


# 便捷函数
def c_major_scale() -> List[str]:
    """C大调音阶"""
    return build_scale('C', 'major')


def a_minor_scale() -> List[str]:
    """A小调音阶"""
    return build_scale('A', 'natural_minor')


def circle_of_fifths() -> List[str]:
    """五度圈"""
    notes = ['C']
    current = 'C'
    for _ in range(11):
        current = transpose_note(current, 7)
        notes.append(current)
    return notes


def circle_of_fourths() -> List[str]:
    """四度圈"""
    notes = ['C']
    current = 'C'
    for _ in range(11):
        current = transpose_note(current, 5)
        notes.append(current)
    return notes


if __name__ == "__main__":
    # 简单演示
    print("=== 音乐和弦与音阶工具 ===\n")
    
    # 音阶
    print("C大调音阶:", build_scale('C', 'major'))
    print("A小调音阶:", build_scale('A', 'natural_minor'))
    print("C蓝调音阶:", build_scale('C', 'blues'))
    print()
    
    # 和弦
    print("C大三和弦:", build_chord('C', 'major'))
    print("A小七和弦:", build_chord('A', 'm7'))
    print("G属七和弦:", build_chord('G', '7'))
    print()
    
    # 和弦识别
    print("识别和弦 ['C', 'E', 'G']:", identify_chord(['C', 'E', 'G']))
    print("识别和弦 ['A', 'C', 'E', 'G']:", identify_chord(['A', 'C', 'E', 'G']))
    print()
    
    # 五度圈
    print("五度圈:", circle_of_fifths())