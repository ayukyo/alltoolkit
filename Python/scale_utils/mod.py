"""
Musical Scale Utilities - 音乐音阶工具库

提供音阶生成、识别、转换和分析功能的纯Python实现。
零外部依赖，支持多种音阶类型和音乐理论操作。

功能:
- 音符表示和转换 (C, C#, Db, etc.)
- 音阶生成 (大调、小调、五声、蓝调、调式等)
- 音阶识别 (根据音符集合识别可能的音阶)
- 转调和移调
- 音阶-和弦关系
- 五度圈工具
- 音程计算
"""

from typing import List, Tuple, Dict, Optional, Set, NamedTuple
from enum import Enum
import re


class Note(NamedTuple):
    """音符表示"""
    name: str      # C, D, E, F, G, A, B
    accidental: str  # '', '#', 'b'
    octave: int = 4  # 默认八度
    
    def __str__(self) -> str:
        return f"{self.name}{self.accidental}"
    
    def full_name(self) -> str:
        return f"{self.name}{self.accidental}{self.octave}"


class Interval(NamedTuple):
    """音程"""
    semitones: int
    name: str
    short_name: str
    abbreviation: str


# 音符常量
NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
ACCIDENTALS = {'': 0, '#': 1, 'b': -1, '##': 2, 'bb': -2}

# 音符名到半音的映射（自然音在C大调中的半音位置）
NOTE_NAME_TO_SEMITONE = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11,
}

# 半音到音符的映射 (使用标准命名)
SEMITONE_TO_NOTE = {
    0: ('C', ''),
    1: ('C', '#'),  # or Db
    2: ('D', ''),
    3: ('D', '#'),  # or Eb
    4: ('E', ''),
    5: ('F', ''),
    6: ('F', '#'),  # or Gb
    7: ('G', ''),
    8: ('G', '#'),  # or Ab
    9: ('A', ''),
    10: ('A', '#'),  # or Bb
    11: ('B', ''),
}

# 音程定义
INTERVALS = {
    0: Interval(0, "纯一度", "Unison", "P1"),
    1: Interval(1, "小二度", "Minor 2nd", "m2"),
    2: Interval(2, "大二度", "Major 2nd", "M2"),
    3: Interval(3, "小三度", "Minor 3rd", "m3"),
    4: Interval(4, "大三度", "Major 3rd", "M3"),
    5: Interval(5, "纯四度", "Perfect 4th", "P4"),
    6: Interval(6, "增四度/减五度", "Tritone", "A4/d5"),
    7: Interval(7, "纯五度", "Perfect 5th", "P5"),
    8: Interval(8, "小六度", "Minor 6th", "m6"),
    9: Interval(9, "大六度", "Major 6th", "M6"),
    10: Interval(10, "小七度", "Minor 7th", "m7"),
    11: Interval(11, "大七度", "Major 7th", "M7"),
    12: Interval(12, "纯八度", "Octave", "P8"),
}

# 音阶模式定义 (半音间隔)
SCALE_PATTERNS = {
    # 基础音阶
    'major': [2, 2, 1, 2, 2, 2, 1],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
    'harmonic_minor': [2, 1, 2, 2, 1, 3, 1],
    'melodic_minor': [2, 1, 2, 2, 2, 2, 1],
    'melodic_minor_descending': [2, 1, 2, 2, 1, 2, 2],
    
    # 五声音阶
    'pentatonic_major': [2, 2, 3, 2, 3],
    'pentatonic_minor': [3, 2, 2, 3, 2],
    'pentatonic_blues': [3, 2, 1, 1, 3, 2],
    
    # 蓝调音阶
    'blues': [3, 2, 1, 1, 3, 2],
    'blues_hexatonic': [3, 2, 1, 1, 3, 2],
    
    # 教会调式
    'ionian': [2, 2, 1, 2, 2, 2, 1],      # 大调
    'dorian': [2, 1, 2, 2, 2, 1, 2],
    'phrygian': [1, 2, 2, 2, 1, 2, 2],
    'lydian': [2, 2, 2, 1, 2, 2, 1],
    'mixolydian': [2, 2, 1, 2, 2, 1, 2],
    'aeolian': [2, 1, 2, 2, 1, 2, 2],     # 自然小调
    'locrian': [1, 2, 2, 1, 2, 2, 2],
    
    # 其他调式
    'phrygian_dominant': [1, 3, 1, 2, 1, 2, 2],
    'lydian_dominant': [2, 2, 2, 2, 1, 2, 1],
    'super_locrian': [1, 2, 1, 2, 2, 2, 2],
    
    # 对称音阶
    'whole_tone': [2, 2, 2, 2, 2, 2],
    'chromatic': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'diminished_half': [2, 1, 2, 1, 2, 1, 2, 1],
    'diminished_whole': [1, 2, 1, 2, 1, 2, 1, 2],
    'augmented': [3, 1, 3, 1, 3, 1],
    
    # 世界音乐音阶
    'hungarian_minor': [2, 1, 3, 1, 1, 3, 1],
    'neapolitan_minor': [1, 2, 2, 2, 1, 3, 1],
    'neapolitan_major': [1, 2, 2, 2, 2, 2, 1],
    'enigmatic': [1, 3, 2, 2, 2, 1, 1],
    'spanish_gypsy': [1, 3, 1, 2, 1, 2, 2],
    'oriental': [1, 3, 1, 1, 3, 1, 2],
    'double_harmonic': [1, 3, 1, 2, 1, 3, 1],
    'byzantine': [1, 3, 1, 2, 1, 3, 1],
    
    # 日本音阶
    'japanese_in': [1, 4, 2, 1, 4],
    'japanese_yo': [2, 3, 2, 3, 2],
    'japanese_hirajoshi': [1, 4, 1, 4, 2],
    'japanese_kumoi': [2, 1, 4, 2, 3],
    
    # 印度音阶
    'raga_bhairav': [1, 3, 1, 2, 1, 3, 1],
    'raga_todi': [1, 2, 3, 1, 1, 3, 1],
    
    # 其他特色音阶
    'bebop_dorian': [2, 1, 2, 2, 2, 1, 2, 2],
    'bebop_major': [2, 2, 1, 2, 2, 1, 1, 1],
    'bebop_dominant': [2, 2, 1, 2, 2, 1, 2, 2],
    'bebop_melodic_minor': [2, 1, 2, 2, 2, 2, 1, 2],
}

# 音阶中文名称
SCALE_NAMES_CN = {
    'major': '大调',
    'natural_minor': '自然小调',
    'harmonic_minor': '和声小调',
    'melodic_minor': '旋律小调',
    'pentatonic_major': '大调五声',
    'pentatonic_minor': '小调五声',
    'pentatonic_blues': '蓝调五声',
    'blues': '蓝调',
    'ionian': '伊奥尼亚调式',
    'dorian': '多利亚调式',
    'phrygian': '弗里吉亚调式',
    'lydian': '利底亚调式',
    'mixolydian': '混合利底亚调式',
    'aeolian': '爱奥利亚调式',
    'locrian': '洛克里亚调式',
    'whole_tone': '全音音阶',
    'chromatic': '半音阶',
    'diminished_half': '减音阶(半全)',
    'diminished_whole': '减音阶(全半)',
    'augmented': '增音阶',
}

# 五度圈顺序
CIRCLE_OF_FIFTHS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
CIRCLE_OF_FOURTHS = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb', 'Bbb', 'Ebb', 'Abb']


def parse_note(note_str: str) -> Note:
    """
    解析音符字符串
    
    Args:
        note_str: 音符字符串，如 'C', 'C#', 'Db', 'C4', 'C#4'
    
    Returns:
        Note对象
    
    Examples:
        >>> parse_note('C')
        Note(name='C', accidental='', octave=4)
        >>> parse_note('C#')
        Note(name='C', accidental='#', octave=4)
        >>> parse_note('Db5')
        Note(name='D', accidental='b', octave=5)
    """
    note_str = note_str.strip()
    
    # 匹配音符、变音记号、八度
    match = re.match(r'^([A-Ga-g])([#b]*)(\d*)$', note_str)
    if not match:
        raise ValueError(f"Invalid note format: {note_str}")
    
    name = match.group(1).upper()
    accidental = match.group(2)
    octave = int(match.group(3)) if match.group(3) else 4
    
    return Note(name, accidental, octave)


def note_to_semitone(note: Note) -> int:
    """
    将音符转换为半音数 (相对于C0)
    
    Args:
        note: Note对象
    
    Returns:
        半音数
    
    Examples:
        >>> note_to_semitone(Note('C', '', 4))
        48
        >>> note_to_semitone(Note('A', '', 4))
        57
    """
    base = NOTE_NAME_TO_SEMITONE[note.name] + ACCIDENTALS.get(note.accidental, 0)
    return base + note.octave * 12


def semitone_to_note(semitone: int, prefer_flat: bool = False) -> Note:
    """
    将半音数转换为音符
    
    Args:
        semitone: 半音数
        prefer_flat: 是否偏好降号
    
    Returns:
        Note对象
    
    Examples:
        >>> semitone_to_note(48)
        Note(name='C', accidental='', octave=4)
        >>> semitone_to_note(49)
        Note(name='C', accidental='#', octave=4)
    """
    octave = semitone // 12
    note_num = semitone % 12
    
    # 处理升号和降号的等音
    flat_mapping = {
        1: ('D', 'b'),
        3: ('E', 'b'),
        6: ('G', 'b'),
        8: ('A', 'b'),
        10: ('B', 'b'),
    }
    
    if prefer_flat and note_num in flat_mapping:
        name, accidental = flat_mapping[note_num]
    else:
        name, accidental = SEMITONE_TO_NOTE[note_num]
    
    return Note(name, accidental, octave)


def transpose_note(note: Note, semitones: int) -> Note:
    """
    移调
    
    Args:
        note: 原始音符
        semitones: 移动的半音数
    
    Returns:
        移调后的音符
    
    Examples:
        >>> transpose_note(Note('C', '', 4), 2)
        Note(name='D', accidental='', octave=4)
        >>> transpose_note(Note('C', '', 4), -1)
        Note(name='B', accidental='', octave=3)
    """
    current = note_to_semitone(note)
    new_semitone = current + semitones
    return semitone_to_note(new_semitone)


def interval_between(note1: Note, note2: Note) -> Interval:
    """
    计算两个音符之间的音程
    
    Args:
        note1: 第一个音符
        note2: 第二个音符
    
    Returns:
        Interval对象
    
    Examples:
        >>> interval_between(Note('C', '', 4), Note('E', '', 4))
        Interval(semitones=4, name='大三度', short_name='Major 3rd', abbreviation='M3')
    """
    diff = note_to_semitone(note2) - note_to_semitone(note1)
    diff = diff % 12  # 简化为单八度
    
    return INTERVALS.get(diff, Interval(diff, f"{diff}半音", f"{diff} semitones", f"i{diff}"))


def generate_scale(root: str, scale_type: str = 'major', octaves: int = 1) -> List[str]:
    """
    生成音阶
    
    Args:
        root: 根音，如 'C', 'C#', 'Db'
        scale_type: 音阶类型
        octaves: 生成几个八度
    
    Returns:
        音阶音符列表
    
    Examples:
        >>> generate_scale('C', 'major')
        ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
        >>> generate_scale('A', 'natural_minor')
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']
    """
    if scale_type not in SCALE_PATTERNS:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    root_note = parse_note(root)
    current = note_to_semitone(root_note)
    pattern = SCALE_PATTERNS[scale_type]
    
    scale = [root]
    
    # 使用与根音一致的变音偏好
    prefer_flat = root_note.accidental == 'b'
    
    for octave_num in range(octaves):
        for interval in pattern:
            current += interval
            note = semitone_to_note(current, prefer_flat=prefer_flat)
            scale.append(str(note))
    
    return scale


def generate_scale_notes(root: str, scale_type: str = 'major', octaves: int = 1) -> List[Note]:
    """
    生成音阶（返回Note对象）
    
    Args:
        root: 根音
        scale_type: 音阶类型
        octaves: 生成几个八度
    
    Returns:
        Note对象列表
    """
    if scale_type not in SCALE_PATTERNS:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    root_note = parse_note(root)
    current = note_to_semitone(root_note)
    pattern = SCALE_PATTERNS[scale_type]
    
    scale = [root_note]
    
    for octave in range(octaves):
        for interval in pattern:
            current += interval
            note = semitone_to_note(current, prefer_flat=(root_note.accidental == 'b'))
            scale.append(note)
    
    return scale


def scale_degrees(scale_type: str = 'major') -> List[str]:
    """
    获取音阶的度数名称
    
    Args:
        scale_type: 音阶类型
    
    Returns:
        度数名称列表
    
    Examples:
        >>> scale_degrees('major')
        ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'I']
    """
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    pattern = SCALE_PATTERNS.get(scale_type, SCALE_PATTERNS['major'])
    return roman_numerals[:len(pattern) + 1]


def identify_scale(notes: List[str]) -> List[Tuple[str, str, str]]:
    """
    根据音符集合识别可能的音阶
    
    Args:
        notes: 音符列表
    
    Returns:
        可能的音阶列表 (根音, 音阶类型, 音阶名)
    
    Examples:
        >>> identify_scale(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        [('C', 'major', '大调'), ('A', 'natural_minor', '自然小调'), ...]
    """
    # 标准化音符为半音集合
    note_set = set()
    for note in notes:
        try:
            n = parse_note(note)
            note_set.add(note_to_semitone(n) % 12)
        except ValueError:
            continue
    
    results = []
    
    # 存储每个结果的scale_semitones用于排序
    result_details = []
    
    for root_semitone in range(12):
        root_note = semitone_to_note(root_semitone)
        root_str = str(root_note)
        
        for scale_type, pattern in SCALE_PATTERNS.items():
            # 生成音阶的半音集合
            scale_semitones = set()
            current = root_semitone
            scale_semitones.add(current)
            
            for interval in pattern:
                current = (current + interval) % 12
                scale_semitones.add(current)
            
            # 检查输入音符是否是音阶的子集
            if note_set.issubset(scale_semitones):
                scale_name = SCALE_NAMES_CN.get(scale_type, scale_type)
                is_exact = note_set == scale_semitones
                results.append((root_str, scale_type, scale_name))
                result_details.append((is_exact, len(scale_semitones), root_str, scale_type))
    
    # 按匹配程度排序：完全匹配优先，然后按scale大小排序
    combined = list(zip(results, result_details))
    combined.sort(key=lambda x: (not x[1][0], x[1][1], x[1][2], x[1][3]))
    results = [r[0] for r in combined]
    
    return results[:10]  # 返回前10个结果


def get_relative_minor(major_key: str) -> str:
    """
    获取关系小调
    
    Args:
        major_key: 大调主音
    
    Returns:
        关系小调主音
    
    Examples:
        >>> get_relative_minor('C')
        'A'
        >>> get_relative_minor('G')
        'E'
    """
    major_note = parse_note(major_key)
    # 大调的关系小调是大调的vi级，即下方小三度
    relative_minor = transpose_note(major_note, -3)
    return str(relative_minor)


def get_relative_major(minor_key: str) -> str:
    """
    获取关系大调
    
    Args:
        minor_key: 小调主音
    
    Returns:
        关系大调主音
    
    Examples:
        >>> get_relative_major('A')
        'C'
        >>> get_relative_major('E')
        'G'
    """
    minor_note = parse_note(minor_key)
    # 小调的关系大调是小调的iii级，即上方小三度
    relative_major = transpose_note(minor_note, 3)
    return str(relative_major)


def circle_of_fifths(start: str = 'C', steps: int = 12, direction: str = 'fifths') -> List[str]:
    """
    生成五度圈或四度圈
    
    Args:
        start: 起始音符
        steps: 步数
        direction: 'fifths' 或 'fourths'
    
    Returns:
        音符列表
    
    Examples:
        >>> circle_of_fifths('C', 7)
        ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    """
    start_note = parse_note(start)
    current = note_to_semitone(start_note)
    result = [str(start_note)]
    
    interval = 7 if direction == 'fifths' else 5
    
    for _ in range(steps - 1):
        current = (current + interval) % 12
        note = semitone_to_note(current)
        result.append(str(note))
    
    return result


def key_signature(key: str) -> Tuple[List[str], List[str]]:
    """
    获取调号的升号和降号
    
    Args:
        key: 调名
    
    Returns:
        (升号列表, 降号列表)
    
    Examples:
        >>> key_signature('G')
        (['F#'], [])
        >>> key_signature('F')
        ([], ['Bb'])
        >>> key_signature('D')
        (['F#', 'C#'], [])
    """
    key_note = parse_note(key)
    key_str = str(key_note)
    
    # 大调升号顺序: F#, C#, G#, D#, A#, E#, B#
    sharps_order = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#']
    # 大调降号顺序: Bb, Eb, Ab, Db, Gb, Cb, Fb
    flats_order = ['Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb']
    
    # 升号调及其升号数量
    sharp_keys = {
        'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 
        'F#': 6, 'C#': 7, 'G#': 8, 'D#': 9, 'A#': 10
    }
    
    # 降号调及其降号数量
    flat_keys = {
        'F': 1, 'Bb': 2, 'Eb': 3, 'Ab': 4, 'Db': 5, 
        'Gb': 6, 'Cb': 7, 'Fb': 8, 'Bbb': 9
    }
    
    # C大调没有升降号
    if key_str == 'C':
        return ([], [])
    
    # A小调（C大调的关系小调）也没有升降号
    if key_str == 'A':
        return ([], [])
    
    # 检查是否是升号调
    if key_str in sharp_keys:
        num = sharp_keys[key_str]
        return (sharps_order[:min(num, 7)], [])
    
    # 检查是否是降号调
    if key_str in flat_keys:
        num = flat_keys[key_str]
        return ([], flats_order[:min(num, 7)])
    
    # 检查等音情况
    # G# = Ab (等音，但G#是升号调，Ab是降号调)
    # F# 和 Gb 是等音，但我们假设用户输入的是他们想要的
    
    # 如果键名带有升号
    if '#' in key_str:
        # 简化处理：根据半音位置判断
        root_semitone = note_to_semitone(key_note) % 12
        
        # 从C开始计算有多少升号
        c_semitone = 0
        fifths_up = (root_semitone - c_semitone) % 12
        # 五度圈上的位置对应升号数量
        num_sharps_map = {0: 0, 7: 1, 2: 2, 9: 3, 4: 4, 11: 5, 6: 6, 1: 7}
        num_sharps = num_sharps_map.get(root_semitone, 0)
        return (sharps_order[:min(num_sharps, 7)], [])
    
    # 如果键名带有降号
    if 'b' in key_str:
        root_semitone = note_to_semitone(key_note) % 12
        
        # 从C开始计算有多少降号
        num_flats_map = {0: 0, 5: 1, 10: 2, 3: 3, 8: 4, 1: 5, 6: 6, 11: 7}
        num_flats = num_flats_map.get(root_semitone, 0)
        return ([], flats_order[:min(num_flats, 7)])
    
    # 默认返回空
    return ([], [])


def chord_scale_relationship(scale_type: str = 'major') -> Dict[int, Tuple[str, str]]:
    """
    获取音阶的和弦关系
    
    Args:
        scale_type: 音阶类型
    
    Returns:
        度数到(和弦类型, 和弦符号)的映射
    
    Examples:
        >>> chord_scale_relationship('major')
        {1: ('major', 'I'), 2: ('minor', 'ii'), 3: ('minor', 'iii'), ...}
    """
    relationships = {
        'major': {
            1: ('major', 'I'),
            2: ('minor', 'ii'),
            3: ('minor', 'iii'),
            4: ('major', 'IV'),
            5: ('major', 'V'),
            6: ('minor', 'vi'),
            7: ('diminished', 'vii°'),
        },
        'natural_minor': {
            1: ('minor', 'i'),
            2: ('diminished', 'ii°'),
            3: ('major', 'III'),
            4: ('minor', 'iv'),
            5: ('minor', 'v'),
            6: ('major', 'VI'),
            7: ('major', 'VII'),
        },
        'harmonic_minor': {
            1: ('minor', 'i'),
            2: ('diminished', 'ii°'),
            3: ('augmented', 'III+'),
            4: ('minor', 'iv'),
            5: ('major', 'V'),
            6: ('major', 'VI'),
            7: ('diminished', 'vii°7'),
        },
        'melodic_minor': {
            1: ('minor', 'i'),
            2: ('minor', 'ii'),
            3: ('augmented', 'III+'),
            4: ('major', 'IV'),
            5: ('major', 'V'),
            6: ('diminished', 'vi°'),
            7: ('diminished', 'vii°'),
        },
        'dorian': {
            1: ('minor', 'i'),
            2: ('minor', 'ii'),
            3: ('major', 'III'),
            4: ('major', 'IV'),
            5: ('minor', 'v'),
            6: ('diminished', 'vi°'),
            7: ('minor', 'vii'),
        },
        'phrygian': {
            1: ('minor', 'i'),
            2: ('major', 'II'),
            3: ('major', 'III'),
            4: ('minor', 'iv'),
            5: ('diminished', 'v°'),
            6: ('minor', 'vi'),
            7: ('minor', 'vii'),
        },
        'lydian': {
            1: ('major', 'I'),
            2: ('major', 'II'),
            3: ('minor', 'iii'),
            4: ('augmented', 'IV+'),
            5: ('major', 'V'),
            6: ('minor', 'vi'),
            7: ('minor', 'vii'),
        },
        'mixolydian': {
            1: ('major', 'I'),
            2: ('minor', 'ii'),
            3: ('diminished', 'iii°'),
            4: ('major', 'IV'),
            5: ('minor', 'v'),
            6: ('minor', 'vi'),
            7: ('major', 'VII'),
        },
        'locrian': {
            1: ('diminished', 'i°'),
            2: ('minor', 'ii'),
            3: ('major', 'III'),
            4: ('minor', 'iv'),
            5: ('minor', 'v'),
            6: ('major', 'VI'),
            7: ('major', 'VII'),
        },
    }
    
    return relationships.get(scale_type, relationships['major'])


def get_scale_chords(root: str, scale_type: str = 'major') -> List[Tuple[str, str, str]]:
    """
    获取音阶上的和弦
    
    Args:
        root: 根音
        scale_type: 音阶类型
    
    Returns:
        (根音, 和弦类型, 和弦符号) 列表
    
    Examples:
        >>> get_scale_chords('C', 'major')
        [('C', 'major', 'I'), ('D', 'minor', 'ii'), ...]
    """
    scale = generate_scale(root, scale_type)
    relationships = chord_scale_relationship(scale_type)
    
    chords = []
    for i, degree in relationships.items():
        if i - 1 < len(scale):
            note = scale[i - 1]
            chord_type, symbol = degree
            chords.append((note, chord_type, symbol))
    
    return chords


def is_diatonic(note: str, key: str, scale_type: str = 'major') -> bool:
    """
    判断音符是否属于某调的自然音
    
    Args:
        note: 音符
        key: 调
        scale_type: 音阶类型
    
    Returns:
        是否为自然音
    
    Examples:
        >>> is_diatonic('C', 'C', 'major')
        True
        >>> is_diatonic('C#', 'C', 'major')
        False
    """
    scale = generate_scale(key, scale_type)
    note_str = str(parse_note(note))
    return note_str in scale


def get_enharmonic(note: str) -> List[str]:
    """
    获取等音
    
    Args:
        note: 音符
    
    Returns:
        等音列表
    
    Examples:
        >>> get_enharmonic('C#')
        ['C#', 'Db']
        >>> get_enharmonic('F#')
        ['F#', 'Gb']
    """
    note_obj = parse_note(note)
    semitone = note_to_semitone(note_obj) % 12
    
    enharmonics = [str(note_obj)]
    
    # 检查其他表示
    for s in range(12):
        if s == semitone:
            continue
        # 检查是否等音
    
    # 手动映射等音
    enharmonic_map = {
        1: ['C#', 'Db'],
        3: ['D#', 'Eb'],
        6: ['F#', 'Gb'],
        8: ['G#', 'Ab'],
        10: ['A#', 'Bb'],
    }
    
    if semitone in enharmonic_map:
        return enharmonic_map[semitone]
    
    return enharmonics


def list_scales() -> List[Tuple[str, str, int]]:
    """
    列出所有支持的音阶
    
    Returns:
        (音阶类型, 中文名称, 音符数量) 列表
    """
    result = []
    for scale_type, pattern in SCALE_PATTERNS.items():
        cn_name = SCALE_NAMES_CN.get(scale_type, scale_type)
        note_count = len(pattern) + 1
        result.append((scale_type, cn_name, note_count))
    
    return sorted(result, key=lambda x: (x[2], x[0]))


# 便捷函数
def major_scale(root: str) -> List[str]:
    """生成大调音阶"""
    return generate_scale(root, 'major')


def minor_scale(root: str, scale_type: str = 'natural') -> List[str]:
    """
    生成小调音阶
    
    Args:
        root: 根音
        scale_type: 'natural', 'harmonic', 或 'melodic'
    """
    scale_map = {
        'natural': 'natural_minor',
        'harmonic': 'harmonic_minor',
        'melodic': 'melodic_minor',
    }
    return generate_scale(root, scale_map.get(scale_type, 'natural_minor'))


def pentatonic(root: str, mode: str = 'major') -> List[str]:
    """
    生成五声音阶
    
    Args:
        root: 根音
        mode: 'major' 或 'minor'
    """
    if mode == 'major':
        return generate_scale(root, 'pentatonic_major')
    else:
        return generate_scale(root, 'pentatonic_minor')


def blues_scale(root: str) -> List[str]:
    """生成蓝调音阶"""
    return generate_scale(root, 'blues')


def mode(root: str, mode_name: str) -> List[str]:
    """
    生成调式音阶
    
    Args:
        root: 根音
        mode_name: 调式名称 (ionian, dorian, phrygian, lydian, mixolydian, aeolian, locrian)
    """
    return generate_scale(root, mode_name)


if __name__ == "__main__":
    # 演示
    print("=== 大调音阶 ===")
    print(f"C大调: {' '.join(major_scale('C'))}")
    print(f"G大调: {' '.join(major_scale('G'))}")
    
    print("\n=== 小调音阶 ===")
    print(f"A自然小调: {' '.join(minor_scale('A', 'natural'))}")
    print(f"A和声小调: {' '.join(minor_scale('A', 'harmonic'))}")
    print(f"A旋律小调: {' '.join(minor_scale('A', 'melodic'))}")
    
    print("\n=== 五声音阶 ===")
    print(f"C大调五声: {' '.join(pentatonic('C', 'major'))}")
    print(f"A小调五声: {' '.join(pentatonic('A', 'minor'))}")
    
    print("\n=== 蓝调音阶 ===")
    print(f"A蓝调: {' '.join(blues_scale('A'))}")
    
    print("\n=== 教会调式 ===")
    for m in ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']:
        print(f"{m}: {' '.join(mode('C', m))}")
    
    print("\n=== 五度圈 ===")
    print(f"五度圈: {' -> '.join(circle_of_fifths('C', 12))}")
    
    print("\n=== 音阶识别 ===")
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    print(f"音符 {notes} 可能是:")
    for root, stype, name in identify_scale(notes)[:5]:
        print(f"  {root} {name}")
    
    print("\n=== 和弦音阶关系 ===")
    for note, chord_type, symbol in get_scale_chords('C', 'major'):
        print(f"  {symbol}: {note} {chord_type}")