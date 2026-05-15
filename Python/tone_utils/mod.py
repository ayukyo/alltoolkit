"""
Tone Utilities - 音调/音符频率计算工具

提供音符与频率之间的转换、音阶生成、和弦识别等功能。
零外部依赖，纯 Python 实现。
"""

from typing import List, Tuple, Dict, Optional
import math

# 标准音高定义 (A4 = 440Hz)
STANDARD_PITCH = 440.0

# 西方音乐中的音符名称
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# 音阶模式 (半音间隔)
SCALE_PATTERNS = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
}

# 和弦模式 (相对于根音的半音)
CHORD_PATTERNS = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dom7': [0, 4, 7, 10],
    'dim7': [0, 3, 6, 9],
    'sus2': [0, 2, 7],
    'sus4': [0, 5, 7],
    'add9': [0, 4, 7, 14],
    'min9': [0, 3, 7, 10, 14],
    'maj9': [0, 4, 7, 11, 14],
}

# MIDI 音符编号范围
MIDI_MIN = 0
MIDI_MAX = 127


def note_to_frequency(note: str, octave: int = 4, a4_freq: float = STANDARD_PITCH) -> float:
    """
    将音符名称转换为频率。
    
    Args:
        note: 音符名称 (如 'C', 'C#', 'Db', 'A')
        octave: 八度编号 (默认 4)
        a4_freq: A4 的参考频率 (默认 440Hz)
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> note_to_frequency('A', 4)
        440.0
        >>> note_to_frequency('C', 4)
        261.625...
        >>> note_to_frequency('A#', 4)
        466.163...
    """
    # 标准化音符名称
    note = note.strip().capitalize()
    
    # 处理降号
    if 'b' in note.lower() and len(note) == 2:
        # 转换为升号表示
        note_index = NOTE_NAMES_FLAT.index(note)
        note_name = NOTE_NAMES[note_index]
    else:
        note_name = note.upper()
        if note_name not in NOTE_NAMES:
            raise ValueError(f"Invalid note name: {note}")
        note_index = NOTE_NAMES.index(note_name)
    
    # 计算与 A4 的半音距离
    # A4 是 MIDI 音符 69
    midi_note = (octave + 1) * 12 + note_index
    semitones_from_a4 = midi_note - 69
    
    # 使用公式: f = a4_freq * 2^(n/12)
    frequency = a4_freq * (2 ** (semitones_from_a4 / 12))
    
    return frequency


def frequency_to_note(frequency: float, a4_freq: float = STANDARD_PITCH, 
                       prefer_flat: bool = False) -> Tuple[str, int, int]:
    """
    将频率转换为最近的音符。
    
    Args:
        frequency: 频率 (Hz)
        a4_freq: A4 的参考频率 (默认 440Hz)
        prefer_flat: 是否优先使用降号表示
    
    Returns:
        (音符名称, 八度, MIDI音符号)
    
    Examples:
        >>> frequency_to_note(440)
        ('A', 4, 69)
        >>> frequency_to_note(261.63)
        ('C', 4, 60)
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    
    # 计算与 A4 的半音距离
    semitones_from_a4 = 12 * math.log2(frequency / a4_freq)
    
    # MIDI 音符号
    midi_note = round(69 + semitones_from_a4)
    midi_note = max(MIDI_MIN, min(MIDI_MAX, midi_note))
    
    # 计算音符和八度
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    
    note_name = NOTE_NAMES_FLAT[note_index] if prefer_flat else NOTE_NAMES[note_index]
    
    return (note_name, octave, midi_note)


def midi_to_frequency(midi_note: int, a4_freq: float = STANDARD_PITCH) -> float:
    """
    将 MIDI 音符号转换为频率。
    
    Args:
        midi_note: MIDI 音符号 (0-127)
        a4_freq: A4 的参考频率 (默认 440Hz)
    
    Returns:
        频率 (Hz)
    
    Examples:
        >>> midi_to_frequency(69)  # A4
        440.0
        >>> midi_to_frequency(60)  # C4
        261.625...
    """
    if not MIDI_MIN <= midi_note <= MIDI_MAX:
        raise ValueError(f"MIDI note must be between {MIDI_MIN} and {MIDI_MAX}")
    
    return a4_freq * (2 ** ((midi_note - 69) / 12))


def frequency_to_midi(frequency: float, a4_freq: float = STANDARD_PITCH) -> int:
    """
    将频率转换为最近的 MIDI 音符号。
    
    Args:
        frequency: 频率 (Hz)
        a4_freq: A4 的参考频率 (默认 440Hz)
    
    Returns:
        MIDI 音符号 (0-127)
    
    Examples:
        >>> frequency_to_midi(440)
        69
        >>> frequency_to_midi(261.63)
        60
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    
    midi_note = round(69 + 12 * math.log2(frequency / a4_freq))
    return max(MIDI_MIN, min(MIDI_MAX, midi_note))


def note_to_midi(note: str, octave: int = 4) -> int:
    """
    将音符名称转换为 MIDI 音符号。
    
    Args:
        note: 音符名称
        octave: 八度编号
    
    Returns:
        MIDI 音符号
    
    Examples:
        >>> note_to_midi('A', 4)
        69
        >>> note_to_midi('C', 4)
        60
    """
    note = note.strip().capitalize()
    
    if 'b' in note.lower() and len(note) == 2:
        note_index = NOTE_NAMES_FLAT.index(note)
    else:
        note_name = note.upper()
        if note_name not in NOTE_NAMES:
            raise ValueError(f"Invalid note name: {note}")
        note_index = NOTE_NAMES.index(note_name)
    
    return (octave + 1) * 12 + note_index


def midi_to_note(midi_note: int, prefer_flat: bool = False) -> Tuple[str, int]:
    """
    将 MIDI 音符号转换为音符名称和八度。
    
    Args:
        midi_note: MIDI 音符号
        prefer_flat: 是否优先使用降号表示
    
    Returns:
        (音符名称, 八度)
    
    Examples:
        >>> midi_to_note(69)
        ('A', 4)
        >>> midi_to_note(60)
        ('C', 4)
    """
    if not MIDI_MIN <= midi_note <= MIDI_MAX:
        raise ValueError(f"MIDI note must be between {MIDI_MIN} and {MIDI_MAX}")
    
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    
    note_name = NOTE_NAMES_FLAT[note_index] if prefer_flat else NOTE_NAMES[note_index]
    
    return (note_name, octave)


def generate_scale(root: str, scale_type: str = 'major', octave: int = 4,
                   a4_freq: float = STANDARD_PITCH) -> List[Tuple[str, float]]:
    """
    生成指定音阶的所有音符及其频率。
    
    Args:
        root: 根音
        scale_type: 音阶类型 ('major', 'minor', 'pentatonic_major', etc.)
        octave: 八度编号
        a4_freq: A4 参考频率
    
    Returns:
        [(音符名称, 频率), ...]
    
    Examples:
        >>> scale = generate_scale('C', 'major', 4)
        >>> len(scale)
        7
        >>> scale[0][0]
        'C'
    """
    if scale_type not in SCALE_PATTERNS:
        raise ValueError(f"Unknown scale type: {scale_type}. "
                        f"Available: {list(SCALE_PATTERNS.keys())}")
    
    root_midi = note_to_midi(root, octave)
    pattern = SCALE_PATTERNS[scale_type]
    
    result = []
    for interval in pattern:
        midi_note = root_midi + interval
        if midi_note <= MIDI_MAX:
            note_name, note_octave = midi_to_note(midi_note)
            freq = midi_to_frequency(midi_note, a4_freq)
            result.append((f"{note_name}{note_octave}", freq))
    
    return result


def generate_chord(root: str, chord_type: str = 'major', octave: int = 4,
                   a4_freq: float = STANDARD_PITCH) -> List[Tuple[str, float]]:
    """
    生成指定和弦的所有音符及其频率。
    
    Args:
        root: 根音
        chord_type: 和弦类型 ('major', 'minor', 'maj7', etc.)
        octave: 八度编号
        a4_freq: A4 参考频率
    
    Returns:
        [(音符名称, 频率), ...]
    
    Examples:
        >>> chord = generate_chord('C', 'major', 4)
        >>> len(chord)
        3
        >>> chord[0][0]
        'C4'
    """
    if chord_type not in CHORD_PATTERNS:
        raise ValueError(f"Unknown chord type: {chord_type}. "
                        f"Available: {list(CHORD_PATTERNS.keys())}")
    
    root_midi = note_to_midi(root, octave)
    pattern = CHORD_PATTERNS[chord_type]
    
    result = []
    for interval in pattern:
        midi_note = root_midi + interval
        if midi_note <= MIDI_MAX:
            note_name, note_octave = midi_to_note(midi_note)
            freq = midi_to_frequency(midi_note, a4_freq)
            result.append((f"{note_name}{note_octave}", freq))
    
    return result


def identify_chord(notes: List[str], octave: int = 4) -> List[Tuple[str, str]]:
    """
    根据音符列表识别可能的和弦。
    
    Args:
        notes: 音符名称列表 (如 ['C', 'E', 'G'])
        octave: 八度编号
    
    Returns:
        [(根音, 和弦类型), ...]
    
    Examples:
        >>> identify_chord(['C', 'E', 'G'])
        [('C', 'major')]
        >>> identify_chord(['A', 'C', 'E'])
        [('A', 'minor')]
    """
    if not notes:
        return []
    
    # 将音符转换为 MIDI 编号（相对值）
    note_midi_values = sorted(set(note_to_midi(n, octave) % 12 for n in notes))
    
    if len(note_midi_values) < 3:
        return []
    
    identified = []
    
    # 尝试每个音符作为根音
    for root_index in note_midi_values:
        # 计算相对于假设根音的间隔
        intervals = sorted([(n - root_index) % 12 for n in note_midi_values])
        
        # 检查每种和弦模式
        for chord_name, pattern in CHORD_PATTERNS.items():
            pattern_sorted = sorted(set(pattern))
            if intervals == pattern_sorted:
                root_note = NOTE_NAMES[root_index]
                identified.append((root_note, chord_name))
    
    return identified


def cents_difference(freq1: float, freq2: float) -> float:
    """
    计算两个频率之间的音分差。
    
    Args:
        freq1: 第一个频率
        freq2: 第二个频率
    
    Returns:
        音分差 (cents)
    
    Examples:
        >>> cents_difference(440, 880)  # 一个八度
        1200.0
        >>> cents_difference(440, 466.16)  # 约一个半音
        100.0...
    """
    if freq1 <= 0 or freq2 <= 0:
        raise ValueError("Frequencies must be positive")
    
    return 1200 * math.log2(freq2 / freq1)


def frequency_ratio_to_cents(ratio: float) -> float:
    """
    将频率比转换为音分。
    
    Args:
        ratio: 频率比
    
    Returns:
        音分
    
    Examples:
        >>> frequency_ratio_to_cents(2)  # 八度
        1200.0
        >>> frequency_ratio_to_cents(1.5)  # 纯五度
        701.955...
    """
    if ratio <= 0:
        raise ValueError("Ratio must be positive")
    
    return 1200 * math.log2(ratio)


def cents_to_frequency_ratio(cents: float) -> float:
    """
    将音分转换为频率比。
    
    Args:
        cents: 音分值
    
    Returns:
        频率比
    
    Examples:
        >>> cents_to_frequency_ratio(1200)  # 八度
        2.0
        >>> round(cents_to_frequency_ratio(700), 3)  # 约纯五度
        1.498
    """
    return 2 ** (cents / 1200)


def transpose_note(note: str, octave: int, semitones: int) -> Tuple[str, int]:
    """
    移调一个音符。
    
    Args:
        note: 音符名称
        octave: 当前八度
        semitones: 移调的半音数 (正数升高，负数降低)
    
    Returns:
        (新音符名称, 新八度)
    
    Examples:
        >>> transpose_note('C', 4, 2)
        ('D', 4)
        >>> transpose_note('A', 4, 3)
        ('C', 5)
    """
    midi_note = note_to_midi(note, octave) + semitones
    midi_note = max(MIDI_MIN, min(MIDI_MAX, midi_note))
    return midi_to_note(midi_note)


def get_interval(note1: str, octave1: int, note2: str, octave2: int) -> Tuple[int, str]:
    """
    计算两个音符之间的音程。
    
    Args:
        note1: 第一个音符
        octave1: 第一个音符的八度
        note2: 第二个音符
        octave2: 第二个音符的八度
    
    Returns:
        (半音数, 音程名称)
    
    Examples:
        >>> get_interval('C', 4, 'G', 4)
        (7, 'perfect_fifth')
        >>> get_interval('C', 4, 'E', 4)
        (4, 'major_third')
    """
    midi1 = note_to_midi(note1, octave1)
    midi2 = note_to_midi(note2, octave2)
    
    semitones = abs(midi2 - midi1)
    
    # 音程名称映射
    interval_names = {
        0: 'unison',
        1: 'minor_second',
        2: 'major_second',
        3: 'minor_third',
        4: 'major_third',
        5: 'perfect_fourth',
        6: 'tritone',
        7: 'perfect_fifth',
        8: 'minor_sixth',
        9: 'major_sixth',
        10: 'minor_seventh',
        11: 'major_seventh',
        12: 'octave'
    }
    
    # 如果正好是 12 半音（一个八度），直接返回 octave
    if semitones == 12:
        return (semitones, 'octave')
    
    # 简化到单八度
    simplified = semitones % 12
    interval_name = interval_names.get(simplified, 'unknown')
    
    if semitones > 12:
        # 添加八度信息
        octaves = semitones // 12
        interval_name = f"{interval_name}+{octaves}_octaves"
    
    return (semitones, interval_name)


def get_harmonics(fundamental: float, num_harmonics: int = 8) -> List[Tuple[int, float, str]]:
    """
    生成泛音系列。
    
    Args:
        fundamental: 基频 (Hz)
        num_harmonics: 泛音数量
    
    Returns:
        [(泛音序号, 频率, 最接近的音符名称), ...]
    
    Examples:
        >>> harmonics = get_harmonics(440, 5)
        >>> len(harmonics)
        5
        >>> harmonics[0][1]
        440.0
    """
    if fundamental <= 0:
        raise ValueError("Fundamental frequency must be positive")
    
    result = []
    for n in range(1, num_harmonics + 1):
        freq = fundamental * n
        note_name, octave, _ = frequency_to_note(freq)
        result.append((n, freq, f"{note_name}{octave}"))
    
    return result


def get_enharmonic_equivalents(note: str) -> List[str]:
    """
    获取等音（同音异名）。
    
    Args:
        note: 音符名称
    
    Returns:
        等音列表
    
    Examples:
        >>> get_enharmonic_equivalents('C#')
        ['C#', 'Db']
        >>> get_enharmonic_equivalents('D')
        ['D']
    """
    note = note.strip().capitalize()
    
    # 获取 MIDI 编号
    if 'b' in note.lower():
        note_index = NOTE_NAMES_FLAT.index(note)
    else:
        note_name = note.upper()
        if note_name not in NOTE_NAMES:
            raise ValueError(f"Invalid note name: {note}")
        note_index = NOTE_NAMES.index(note_name)
    
    # 返回升号和降号表示
    return [NOTE_NAMES[note_index], NOTE_NAMES_FLAT[note_index]]


def is_consonant_interval(semitones: int) -> bool:
    """
    判断音程是否协和。
    
    Args:
        semitones: 半音数
    
    Returns:
        是否为协和音程
    
    Examples:
        >>> is_consonant_interval(7)  # 纯五度
        True
        >>> is_consonant_interval(6)  # 三全音
        False
    """
    # 完全协和: 纯一度、纯八度、纯五度、纯四度
    # 不完全协和: 大三度、小六度、小三度、大六度
    # 不协和: 大二度、小七度、小二度、大七度、三全音
    
    simplified = semitones % 12
    
    # 完全协和
    if simplified in [0, 7, 12]:
        return True
    # 纯四度在某些情况下协和
    if simplified == 5:
        return True
    # 不完全协和
    if simplified in [3, 4, 8, 9]:
        return True
    
    return False


def get_circle_of_fifths() -> List[Tuple[str, str, List[str]]]:
    """
    生成五度圈。
    
    Returns:
        [(调号, 关系小调, 调内音符), ...]
    
    Examples:
        >>> circle = get_circle_of_fifths()
        >>> len(circle)
        12
        >>> circle[0][0]
        'C'
    """
    circle = []
    current_note_index = 0  # 从 C 开始
    
    for i in range(12):
        major_key = NOTE_NAMES[current_note_index]
        
        # 关系小调在下方小三度
        minor_key = NOTE_NAMES[(current_note_index + 9) % 12]
        
        # 获取调内音符
        scale = generate_scale(major_key, 'major', 4)
        scale_notes = [note.replace('4', '') for note, _ in scale]
        
        circle.append((major_key, minor_key, scale_notes))
        
        # 向上五度移动
        current_note_index = (current_note_index + 7) % 12
    
    return circle


class Tone:
    """
    音符类，支持音符操作和转换。
    """
    
    def __init__(self, note: str, octave: int = 4, a4_freq: float = STANDARD_PITCH):
        """
        初始化音符。
        
        Args:
            note: 音符名称
            octave: 八度
            a4_freq: A4 参考频率
        """
        self.note = note.strip().capitalize()
        self.octave = octave
        self.a4_freq = a4_freq
        
        # 验证音符
        if 'b' in self.note.lower():
            if self.note not in NOTE_NAMES_FLAT:
                raise ValueError(f"Invalid note: {note}")
            self._note_index = NOTE_NAMES_FLAT.index(self.note)
        else:
            if self.note.upper() not in NOTE_NAMES:
                raise ValueError(f"Invalid note: {note}")
            self._note_index = NOTE_NAMES.index(self.note.upper())
    
    @property
    def frequency(self) -> float:
        """音符频率。"""
        return note_to_frequency(self.note, self.octave, self.a4_freq)
    
    @property
    def midi_note(self) -> int:
        """MIDI 音符号。"""
        return note_to_midi(self.note, self.octave)
    
    def transpose(self, semitones: int) -> 'Tone':
        """移调。"""
        new_note, new_octave = transpose_note(self.note, self.octave, semitones)
        return Tone(new_note, new_octave, self.a4_freq)
    
    def interval_to(self, other: 'Tone') -> Tuple[int, str]:
        """计算到另一个音符的音程。"""
        return get_interval(self.note, self.octave, other.note, other.octave)
    
    def harmonics(self, num: int = 8) -> List[Tuple[int, float, str]]:
        """获取泛音系列。"""
        return get_harmonics(self.frequency, num)
    
    def __repr__(self) -> str:
        return f"Tone({self.note}{self.octave}, {self.frequency:.2f}Hz)"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Tone):
            return self.midi_note == other.midi_note
        return False
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Tone):
            return self.midi_note < other.midi_note
        return NotImplemented
    
    def __le__(self, other) -> bool:
        if isinstance(other, Tone):
            return self.midi_note <= other.midi_note
        return NotImplemented
    
    def __gt__(self, other) -> bool:
        if isinstance(other, Tone):
            return self.midi_note > other.midi_note
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        if isinstance(other, Tone):
            return self.midi_note >= other.midi_note
        return NotImplemented
    
    def __sub__(self, other) -> int:
        """返回半音差。"""
        if isinstance(other, Tone):
            return self.midi_note - other.midi_note
        return NotImplemented
    
    def __add__(self, semitones: int) -> 'Tone':
        """升高指定半音数。"""
        return self.transpose(semitones)
    
    def __isub__(self, other) -> bool:
        return self.__le__(other)