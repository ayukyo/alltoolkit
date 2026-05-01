"""
MIDI Utilities - 零依赖 MIDI 文件处理工具

提供 MIDI 文件的读取、解析、写入和生成功能。
仅使用 Python 标准库，无外部依赖。

功能：
- 读取和解析 MIDI 文件（格式 0 和 1）
- 提取音符、节拍、轨道信息
- 生成简单的 MIDI 文件
- MIDI 事件解析（音符开/关、控制变化、程序变化等）
- 时间格式转换（tick、PPQN、BPM）

作者: AllToolkit
版本: 1.0.0
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Dict, Optional, Tuple, BinaryIO, Union
import struct
from pathlib import Path


# ============================================================================
# 异常类
# ============================================================================

class MIDIUtilsError(Exception):
    """MIDI 工具基础异常"""
    pass


class InvalidMIDIFileError(MIDIUtilsError):
    """无效的 MIDI 文件"""
    pass


class UnsupportedMIDIFormatError(MIDIUtilsError):
    """不支持的 MIDI 格式"""
    pass


# ============================================================================
# 枚举和常量
# ============================================================================

class MIDIMessageType(IntEnum):
    """MIDI 消息类型"""
    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    POLY_KEY_PRESSURE = 0xA0
    CONTROL_CHANGE = 0xB0
    PROGRAM_CHANGE = 0xC0
    CHANNEL_PRESSURE = 0xD0
    PITCH_BEND = 0xE0
    SYSTEM_MESSAGE = 0xF0


class MetaEventType(IntEnum):
    """Meta 事件类型"""
    SEQUENCE_NUMBER = 0x00
    TEXT = 0x01
    COPYRIGHT = 0x02
    TRACK_NAME = 0x03
    INSTRUMENT_NAME = 0x04
    LYRIC = 0x05
    MARKER = 0x06
    CUE_POINT = 0x07
    CHANNEL_PREFIX = 0x20
    END_OF_TRACK = 0x2F
    TEMPO = 0x51
    SMPTE_OFFSET = 0x54
    TIME_SIGNATURE = 0x58
    KEY_SIGNATURE = 0x59
    SEQUENCER_SPECIFIC = 0x7F


class ControlChange(IntEnum):
    """常用控制变化"""
    BANK_SELECT = 0
    MODULATION = 1
    VOLUME = 7
    PAN = 10
    EXPRESSION = 11
    SUSTAIN_PEDAL = 64
    ALL_NOTES_OFF = 123


# 音符名称映射
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 通用 MIDI 乐器名称（部分）
GM_INSTRUMENTS = {
    0: "Acoustic Grand Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    3: "Honky-tonk Piano",
    4: "Electric Piano 1",
    5: "Electric Piano 2",
    6: "Harpsichord",
    7: "Clavi",
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)",
    28: "Electric Guitar (muted)",
    29: "Overdriven Guitar",
    30: "Distortion Guitar",
    31: "Guitar harmonics",
    # ... 更多乐器
    32: "Acoustic Bass",
    33: "Electric Bass (finger)",
    34: "Electric Bass (pick)",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "SynthStrings 1",
    51: "SynthStrings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "SynthBrass 1",
    63: "SynthBrass 2",
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
    80: "Lead 1 (square)",
    81: "Lead 2 (sawtooth)",
    82: "Lead 3 (calliope)",
    83: "Lead 4 (chiff)",
    84: "Lead 5 (charang)",
    85: "Lead 6 (voice)",
    86: "Lead 7 (fifths)",
    87: "Lead 8 (bass + lead)",
    88: "Pad 1 (new age)",
    89: "Pad 2 (warm)",
    90: "Pad 3 (polysynth)",
    91: "Pad 4 (choir)",
    92: "Pad 5 (bowed)",
    93: "Pad 6 (metallic)",
    94: "Pad 7 (halo)",
    95: "Pad 8 (sweep)",
    96: "FX 1 (rain)",
    97: "FX 2 (soundtrack)",
    98: "FX 3 (crystal)",
    99: "FX 4 (atmosphere)",
    100: "FX 5 (brightness)",
    101: "FX 6 (goblins)",
    102: "FX 7 (echoes)",
    103: "FX 8 (sci-fi)",
    104: "Sitar",
    105: "Banjo",
    106: "Shamisen",
    107: "Koto",
    108: "Kalimba",
    109: "Bag pipe",
    110: "Fiddle",
    111: "Shanai",
    112: "Tinkle Bell",
    113: "Agogo",
    114: "Steel Drums",
    115: "Woodblock",
    116: "Taiko Drum",
    117: "Melodic Tom",
    118: "Synth Drum",
    119: "Reverse Cymbal",
    120: "Guitar Fret Noise",
    121: "Breath Noise",
    122: "Seashore",
    123: "Bird Tweet",
    124: "Telephone Ring",
    125: "Helicopter",
    126: "Applause",
    127: "Gunshot",
}

# 打击乐器映射（Channel 10）
DRUM_NAMES = {
    35: "Acoustic Bass Drum",
    36: "Bass Drum 1",
    37: "Side Stick",
    38: "Acoustic Snare",
    39: "Hand Clap",
    40: "Electric Snare",
    41: "Low Floor Tom",
    42: "Closed Hi Hat",
    43: "High Floor Tom",
    44: "Pedal Hi-Hat",
    45: "Low Tom",
    46: "Open Hi-Hat",
    47: "Low-Mid Tom",
    48: "Hi-Mid Tom",
    49: "Crash Cymbal 1",
    50: "High Tom",
    51: "Ride Cymbal 1",
    52: "Chinese Cymbal",
    53: "Ride Bell",
    54: "Tambourine",
    55: "Splash Cymbal",
    56: "Cowbell",
    57: "Crash Cymbal 2",
    58: "Vibraslap",
    59: "Ride Cymbal 2",
    60: "Hi Bongo",
    61: "Low Bongo",
    62: "Mute Hi Conga",
    63: "Open Hi Conga",
    64: "Low Conga",
    65: "High Timbale",
    66: "Low Timbale",
    67: "High Agogo",
    68: "Low Agogo",
    69: "Cabasa",
    70: "Maracas",
    71: "Short Whistle",
    72: "Long Whistle",
    73: "Short Guiro",
    74: "Long Guiro",
    75: "Claves",
    76: "Hi Wood Block",
    77: "Low Wood Block",
    78: "Mute Cuica",
    79: "Open Cuica",
    80: "Mute Triangle",
    81: "Open Triangle",
}


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class MIDIEvent:
    """MIDI 事件"""
    delta_time: int  # tick 为单位的时间差
    event_type: int  # 事件类型
    channel: int = 0  # 通道 (0-15)
    data: bytes = b''  # 事件数据
    meta_type: int = 0  # Meta 事件类型（仅用于 Meta 事件）
    
    def __repr__(self):
        type_name = self.get_type_name()
        return f"MIDIEvent(delta={self.delta_time}, type={type_name}, ch={self.channel}, data={self.data.hex()})"
    
    def get_type_name(self) -> str:
        """获取事件类型名称"""
        if self.event_type == 0xFF:
            return f"Meta({self.meta_type:02X})"
        elif self.event_type == 0xF0 or self.event_type == 0xF7:
            return "SysEx"
        elif self.event_type & 0xF0 in (0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0):
            return MIDIMessageType(self.event_type & 0xF0).name
        return f"Unknown({self.event_type:02X})"


@dataclass
class NoteEvent:
    """音符事件（已解析）"""
    note: int  # 音符编号 (0-127)
    note_name: str  # 音符名称 (如 C4, D#5)
    start_time: float  # 开始时间（秒）
    duration: float  # 持续时间（秒）
    velocity: int  # 力度 (0-127)
    channel: int  # 通道 (0-15)
    instrument: str = ""  # 乐器名称
    track_name: str = ""  # 轨道名称


@dataclass
class MIDITrack:
    """MIDI 轨道"""
    events: List[MIDIEvent] = field(default_factory=list)
    name: str = ""
    instrument: str = ""
    
    def get_note_events(self, ticks_per_beat: int, bpm: float = 120.0) -> List[NoteEvent]:
        """提取轨道中的所有音符事件"""
        notes = []
        active_notes: Dict[int, Tuple[float, int, int]] = {}  # note -> (start_time, velocity, channel)
        
        seconds_per_tick = 60.0 / (bpm * ticks_per_beat)
        current_time = 0.0
        
        for event in self.events:
            current_time += event.delta_time * seconds_per_tick
            
            if event.event_type & 0xF0 == MIDIMessageType.NOTE_ON:
                note = event.data[0] if len(event.data) > 0 else 0
                velocity = event.data[1] if len(event.data) > 1 else 0
                channel = event.channel
                
                if velocity > 0:
                    active_notes[note] = (current_time, velocity, channel)
                elif note in active_notes:
                    # velocity = 0 等同于 NOTE_OFF
                    start_time, vel, ch = active_notes.pop(note)
                    duration = current_time - start_time
                    notes.append(NoteEvent(
                        note=note,
                        note_name=midi_note_to_name(note),
                        start_time=start_time,
                        duration=duration,
                        velocity=vel,
                        channel=ch,
                        instrument=self.instrument,
                        track_name=self.name
                    ))
            
            elif event.event_type & 0xF0 == MIDIMessageType.NOTE_OFF:
                note = event.data[0] if len(event.data) > 0 else 0
                if note in active_notes:
                    start_time, velocity, channel = active_notes.pop(note)
                    duration = current_time - start_time
                    notes.append(NoteEvent(
                        note=note,
                        note_name=midi_note_to_name(note),
                        start_time=start_time,
                        duration=duration,
                        velocity=velocity,
                        channel=channel,
                        instrument=self.instrument,
                        track_name=self.name
                    ))
        
        return notes


@dataclass
class MIDIInfo:
    """MIDI 文件信息"""
    filepath: str
    format_type: int  # 格式类型 (0, 1, 2)
    num_tracks: int  # 轨道数
    ticks_per_beat: int  # 每个 beat 的 tick 数 (PPQN)
    duration: float  # 总时长（秒）
    bpm: float  # 速度 (BPM)
    time_signature: Tuple[int, int, int, int]  # (分子, 分母, metronome, thirty-seconds)
    key_signature: Tuple[int, bool]  # (升降号数, 是否小调)
    track_names: List[str]  # 轨道名称列表
    num_notes: int  # 音符总数
    
    def __repr__(self):
        return (
            f"MIDIInfo(\n"
            f"  file='{self.filepath}',\n"
            f"  format={self.format_type},\n"
            f"  tracks={self.num_tracks},\n"
            f"  ppqn={self.ticks_per_beat},\n"
            f"  duration={self.duration:.2f}s,\n"
            f"  bpm={self.bpm:.1f},\n"
            f"  notes={self.num_notes}\n"
            f")"
        )


@dataclass
class MIDIFile:
    """MIDI 文件对象"""
    format_type: int = 1
    ticks_per_beat: int = 480  # 标准 PPQN
    tracks: List[MIDITrack] = field(default_factory=list)
    bpm: float = 120.0
    time_signature: Tuple[int, int, int, int] = (4, 4, 24, 8)
    key_signature: Tuple[int, bool] = (0, False)
    
    def get_all_notes(self) -> List[NoteEvent]:
        """获取所有轨道的音符事件"""
        all_notes = []
        for track in self.tracks:
            notes = track.get_note_events(self.ticks_per_beat, self.bpm)
            all_notes.extend(notes)
        return all_notes
    
    def get_duration(self) -> float:
        """获取总时长（秒）"""
        if not self.tracks:
            return 0.0
        
        max_time = 0.0
        seconds_per_tick = 60.0 / (self.bpm * self.ticks_per_beat)
        
        for track in self.tracks:
            time = 0
            for event in track.events:
                time += event.delta_time
            max_time = max(max_time, time * seconds_per_tick)
        
        return max_time


# ============================================================================
# 辅助函数
# ============================================================================

def midi_note_to_name(note: int) -> str:
    """将 MIDI 音符编号转换为名称（如 C4, D#5）"""
    if not 0 <= note <= 127:
        return f"INVALID({note})"
    
    octave = (note // 12) - 1
    note_name = NOTE_NAMES[note % 12]
    return f"{note_name}{octave}"


def name_to_midi_note(name: str) -> int:
    """将音符名称转换为 MIDI 音符编号（如 C4 -> 60）"""
    name = name.strip().upper()
    
    # 解析音符名称
    if name[0] not in 'ABCDEFG':
        raise ValueError(f"Invalid note name: {name}")
    
    note_char = name[0]
    rest = name[1:]
    
    # 检查是否有升降号
    sharp = False
    flat = False
    if rest.startswith('#'):
        sharp = True
        rest = rest[1:]
    elif rest.startswith('B') or rest.startswith('♭'):
        flat = True
        rest = rest[1:]
    
    # 解析八度
    try:
        octave = int(rest)
    except ValueError:
        raise ValueError(f"Invalid octave in note name: {name}")
    
    # 计算音符编号
    base_note = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}[note_char]
    
    if flat:
        base_note -= 1
    if sharp:
        base_note += 1
    
    return (octave + 1) * 12 + base_note


def ticks_to_seconds(ticks: int, ticks_per_beat: int, bpm: float) -> float:
    """将 tick 转换为秒"""
    return (ticks / ticks_per_beat) * (60.0 / bpm)


def seconds_to_ticks(seconds: float, ticks_per_beat: int, bpm: float) -> int:
    """将秒转换为 tick"""
    return int(seconds * ticks_per_beat * bpm / 60.0)


def get_instrument_name(program: int, channel: int = 0) -> str:
    """获取乐器名称"""
    if channel == 9:  # 打击乐器轨道
        return DRUM_NAMES.get(program, f"Drum {program}")
    return GM_INSTRUMENTS.get(program, f"Instrument {program}")


# ============================================================================
# MIDI 文件读取
# ============================================================================

def read_variable_length(data: bytes, offset: int) -> Tuple[int, int]:
    """
    读取可变长度数值
    返回: (value, bytes_read)
    """
    value = 0
    bytes_read = 0
    
    while True:
        if offset + bytes_read >= len(data):
            raise InvalidMIDIFileError("Unexpected end of file while reading variable length")
        
        byte = data[offset + bytes_read]
        bytes_read += 1
        
        value = (value << 7) | (byte & 0x7F)
        
        if not (byte & 0x80):
            break
        
        if bytes_read > 4:
            raise InvalidMIDIFileError("Variable length value too long")
    
    return value, bytes_read


def parse_midi_file(filepath: Union[str, Path]) -> MIDIFile:
    """
    解析 MIDI 文件
    
    参数:
        filepath: MIDI 文件路径
    
    返回:
        MIDIFile 对象
    
    异常:
        FileNotFoundError: 文件不存在
        InvalidMIDIFileError: 无效的 MIDI 文件
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"MIDI file not found: {filepath}")
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    if len(data) < 14:
        raise InvalidMIDIFileError("File too short to be a valid MIDI file")
    
    # 解析头部
    if data[0:4] != b'MThd':
        raise InvalidMIDIFileError("Invalid MIDI file: missing MThd header")
    
    header_length = struct.unpack('>I', data[4:8])[0]
    format_type = struct.unpack('>H', data[8:10])[0]
    num_tracks = struct.unpack('>H', data[10:12])[0]
    ticks_per_beat = struct.unpack('>H', data[12:14])[0]
    
    # 检查格式
    if format_type not in (0, 1, 2):
        raise UnsupportedMIDIFormatError(f"Unsupported MIDI format: {format_type}")
    
    midi_file = MIDIFile(
        format_type=format_type,
        ticks_per_beat=ticks_per_beat,
        tracks=[]
    )
    
    # 解析轨道
    offset = 8 + header_length
    
    for track_idx in range(num_tracks):
        if offset + 8 > len(data):
            raise InvalidMIDIFileError(f"Unexpected end of file at track {track_idx}")
        
        if data[offset:offset+4] != b'MTrk':
            raise InvalidMIDIFileError(f"Invalid track header at offset {offset}")
        
        track_length = struct.unpack('>I', data[offset+4:offset+8])[0]
        track_data = data[offset+8:offset+8+track_length]
        offset += 8 + track_length
        
        track = parse_track(track_data, midi_file)
        midi_file.tracks.append(track)
    
    return midi_file


def parse_track(data: bytes, midi_file: MIDIFile) -> MIDITrack:
    """解析 MIDI 轨道数据"""
    track = MIDITrack()
    offset = 0
    running_status = 0
    
    while offset < len(data):
        # 读取 delta time
        delta_time, bytes_read = read_variable_length(data, offset)
        offset += bytes_read
        
        # 读取事件类型
        if offset >= len(data):
            break
        
        event_type = data[offset]
        
        # 检查是否使用 running status
        if event_type < 0x80:
            event_type = running_status
        else:
            offset += 1
            running_status = event_type
        
        # 解析事件
        event, offset = parse_event(data, offset, event_type, delta_time)
        track.events.append(event)
        
        # 提取轨道名称和乐器
        if event.event_type == 0xFF:
            if event.meta_type == MetaEventType.TRACK_NAME:
                track.name = event.data.decode('utf-8', errors='replace')
            elif event.meta_type == MetaEventType.INSTRUMENT_NAME:
                track.instrument = event.data.decode('utf-8', errors='replace')
            elif event.meta_type == MetaEventType.TEMPO:
                microseconds_per_beat = struct.unpack('>I', b'\x00' + event.data)[0]
                midi_file.bpm = 60000000.0 / microseconds_per_beat
            elif event.meta_type == MetaEventType.TIME_SIGNATURE:
                if len(event.data) >= 4:
                    midi_file.time_signature = tuple(event.data)
            elif event.meta_type == MetaEventType.KEY_SIGNATURE:
                if len(event.data) >= 2:
                    midi_file.key_signature = (event.data[0], event.data[1] != 0)
    
    return track


def parse_event(data: bytes, offset: int, event_type: int, delta_time: int) -> Tuple[MIDIEvent, int]:
    """解析单个 MIDI 事件"""
    if event_type == 0xFF:
        # Meta 事件
        if offset >= len(data):
            raise InvalidMIDIFileError("Unexpected end of file in meta event")
        
        meta_type = data[offset]
        offset += 1
        
        length, bytes_read = read_variable_length(data, offset)
        offset += bytes_read
        
        meta_data = data[offset:offset+length]
        offset += length
        
        return MIDIEvent(
            delta_time=delta_time,
            event_type=0xFF,
            meta_type=meta_type,
            data=meta_data
        ), offset
    
    elif event_type == 0xF0 or event_type == 0xF7:
        # SysEx 事件
        length, bytes_read = read_variable_length(data, offset)
        offset += bytes_read
        
        sys_data = data[offset:offset+length]
        offset += length
        
        return MIDIEvent(
            delta_time=delta_time,
            event_type=event_type,
            data=sys_data
        ), offset
    
    else:
        # 通道消息
        channel = event_type & 0x0F
        msg_type = event_type & 0xF0
        
        # 确定数据长度
        if msg_type in (0xC0, 0xD0):  # Program Change, Channel Pressure
            data_length = 1
        else:
            data_length = 2
        
        if offset + data_length > len(data):
            raise InvalidMIDIFileError("Unexpected end of file in channel message")
        
        msg_data = data[offset:offset+data_length]
        offset += data_length
        
        return MIDIEvent(
            delta_time=delta_time,
            event_type=msg_type,
            channel=channel,
            data=msg_data
        ), offset


# ============================================================================
# MIDI 文件写入
# ============================================================================

def write_variable_length(value: int) -> bytes:
    """将整数编码为可变长度格式"""
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    if value == 0:
        return b'\x00'
    
    result = []
    result.append(value & 0x7F)
    value >>= 7
    
    while value:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    
    return bytes(reversed(result))


def create_midi_event(delta_time: int, event_type: int, channel: int = 0, 
                      data: bytes = b'', meta_type: int = 0) -> MIDIEvent:
    """创建 MIDI 事件"""
    return MIDIEvent(
        delta_time=delta_time,
        event_type=event_type,
        channel=channel,
        data=data,
        meta_type=meta_type
    )


def create_note_on_event(delta_time: int, note: int, velocity: int, channel: int = 0) -> MIDIEvent:
    """创建 NOTE_ON 事件"""
    return MIDIEvent(
        delta_time=delta_time,
        event_type=MIDIMessageType.NOTE_ON,
        channel=channel,
        data=bytes([note & 0x7F, velocity & 0x7F])
    )


def create_note_off_event(delta_time: int, note: int, velocity: int, channel: int = 0) -> MIDIEvent:
    """创建 NOTE_OFF 事件"""
    return MIDIEvent(
        delta_time=delta_time,
        event_type=MIDIMessageType.NOTE_OFF,
        channel=channel,
        data=bytes([note & 0x7F, velocity & 0x7F])
    )


def create_tempo_event(delta_time: int, bpm: float) -> MIDIEvent:
    """创建速度 Meta 事件"""
    microseconds = int(60000000.0 / bpm)
    return MIDIEvent(
        delta_time=delta_time,
        event_type=0xFF,
        meta_type=MetaEventType.TEMPO,
        data=struct.pack('>I', microseconds)[1:]  # 3 bytes
    )


def create_track_name_event(delta_time: int, name: str) -> MIDIEvent:
    """创建轨道名称 Meta 事件"""
    return MIDIEvent(
        delta_time=delta_time,
        event_type=0xFF,
        meta_type=MetaEventType.TRACK_NAME,
        data=name.encode('utf-8')
    )


def create_end_of_track_event(delta_time: int = 0) -> MIDIEvent:
    """创建轨道结束 Meta 事件"""
    return MIDIEvent(
        delta_time=delta_time,
        event_type=0xFF,
        meta_type=MetaEventType.END_OF_TRACK,
        data=b''
    )


def write_midi_file(midi_file: MIDIFile, filepath: Union[str, Path]) -> bool:
    """
    写入 MIDI 文件
    
    参数:
        midi_file: MIDIFile 对象
        filepath: 输出文件路径
    
    返回:
        bool: 成功返回 True
    
    异常:
        InvalidMIDIFileError: 无效的 MIDI 数据
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'wb') as f:
        # 写入头部
        f.write(b'MThd')
        f.write(struct.pack('>I', 6))  # 头部长度
        f.write(struct.pack('>H', midi_file.format_type))
        f.write(struct.pack('>H', len(midi_file.tracks)))
        f.write(struct.pack('>H', midi_file.ticks_per_beat))
        
        # 写入轨道
        for track in midi_file.tracks:
            track_data = write_track(track, midi_file.bpm)
            f.write(b'MTrk')
            f.write(struct.pack('>I', len(track_data)))
            f.write(track_data)
    
    return True


def write_track(track: MIDITrack, bpm: float) -> bytes:
    """写入轨道数据"""
    data = bytearray()
    
    # 写入轨道名称（如果有）
    if track.name:
        data.extend(write_variable_length(0))  # delta time = 0
        data.append(0xFF)  # Meta event
        data.append(MetaEventType.TRACK_NAME)
        name_bytes = track.name.encode('utf-8')
        data.extend(write_variable_length(len(name_bytes)))
        data.extend(name_bytes)
    
    # 写入事件
    for event in track.events:
        data.extend(write_variable_length(event.delta_time))
        
        if event.event_type == 0xFF:
            # Meta 事件
            data.append(0xFF)
            data.append(event.meta_type)
            data.extend(write_variable_length(len(event.data)))
            data.extend(event.data)
        
        elif event.event_type == 0xF0 or event.event_type == 0xF7:
            # SysEx 事件
            data.append(event.event_type)
            data.extend(write_variable_length(len(event.data)))
            data.extend(event.data)
        
        else:
            # 通道消息
            data.append(event.event_type | event.channel)
            data.extend(event.data)
    
    # 写入轨道结束事件
    data.extend(write_variable_length(0))
    data.append(0xFF)
    data.append(MetaEventType.END_OF_TRACK)
    data.append(0)
    
    return bytes(data)


# ============================================================================
# 高级 API
# ============================================================================

def get_midi_info(filepath: Union[str, Path]) -> MIDIInfo:
    """
    获取 MIDI 文件信息
    
    参数:
        filepath: MIDI 文件路径
    
    返回:
        MIDIInfo 对象
    """
    midi_file = parse_midi_file(filepath)
    notes = midi_file.get_all_notes()
    
    return MIDIInfo(
        filepath=str(filepath),
        format_type=midi_file.format_type,
        num_tracks=len(midi_file.tracks),
        ticks_per_beat=midi_file.ticks_per_beat,
        duration=midi_file.get_duration(),
        bpm=midi_file.bpm,
        time_signature=midi_file.time_signature,
        key_signature=midi_file.key_signature,
        track_names=[t.name for t in midi_file.tracks],
        num_notes=len(notes)
    )


def extract_notes(filepath: Union[str, Path]) -> List[NoteEvent]:
    """
    从 MIDI 文件提取所有音符事件
    
    参数:
        filepath: MIDI 文件路径
    
    返回:
        NoteEvent 列表
    """
    midi_file = parse_midi_file(filepath)
    return midi_file.get_all_notes()


def create_simple_melody(
    notes: List[Union[Tuple[str, float], Tuple[str, float, int]]],
    bpm: float = 120.0,
    ticks_per_beat: int = 480,
    velocity: int = 100,
    channel: int = 0,
    program: int = 0
) -> MIDIFile:
    """
    创建简单旋律 MIDI 文件
    
    参数:
        notes: 音符列表，每个元素为 (音符名称, 时长) 或 (音符名称, 时长, 力度)
               音符名称如 "C4", "D#5", "R"（休止符）
               时长以四分音符为单位（1.0 = 四分音符, 0.5 = 八分音符）
        bpm: 速度 (BPM)
        ticks_per_beat: 每 beat 的 tick 数
        velocity: 默认力度
        channel: MIDI 通道
        program: 音色编号 (0-127)
    
    返回:
        MIDIFile 对象
    
    示例:
        # 创建一个简单旋律
        melody = [
            ("C4", 1.0),    # 四分音符 C4
            ("D4", 1.0),    # 四分音符 D4
            ("E4", 1.0),    # 四分音符 E4
            ("F4", 1.0),    # 四分音符 F4
            ("G4", 2.0),    # 二分音符 G4
            ("R", 1.0),     # 四分休止符
        ]
        midi = create_simple_melody(melody, bpm=120)
        write_midi_file(midi, "melody.mid")
    """
    midi_file = MIDIFile(
        format_type=0,
        ticks_per_beat=ticks_per_beat,
        bpm=bpm
    )
    
    track = MIDITrack(name="Melody")
    events = []
    
    # 添加音色变化
    events.append(MIDIEvent(
        delta_time=0,
        event_type=MIDIMessageType.PROGRAM_CHANGE,
        channel=channel,
        data=bytes([program])
    ))
    
    # 添加速度
    events.append(create_tempo_event(0, bpm))
    
    current_time = 0
    
    for note_spec in notes:
        if len(note_spec) == 2:
            note_name, duration = note_spec
            note_velocity = velocity
        else:
            note_name, duration, note_velocity = note_spec
        
        duration_ticks = int(duration * ticks_per_beat)
        
        if note_name.upper() == 'R':
            # 休止符
            current_time += duration_ticks
            continue
        
        # 转换音符名称
        midi_note = name_to_midi_note(note_name)
        
        # 添加 NOTE_ON
        events.append(MIDIEvent(
            delta_time=current_time,
            event_type=MIDIMessageType.NOTE_ON,
            channel=channel,
            data=bytes([midi_note, note_velocity])
        ))
        
        # 添加 NOTE_OFF
        events.append(MIDIEvent(
            delta_time=current_time + duration_ticks,
            event_type=MIDIMessageType.NOTE_OFF,
            channel=channel,
            data=bytes([midi_note, 0])
        ))
        
        current_time += duration_ticks
    
    # 按时间排序并计算 delta time
    events.sort(key=lambda e: e.delta_time)
    
    prev_time = 0
    for event in events:
        delta = event.delta_time - prev_time
        event.delta_time = delta
        prev_time += delta
    
    # 添加轨道结束事件
    events.append(create_end_of_track_event())
    
    track.events = events
    midi_file.tracks.append(track)
    
    return midi_file


def transpose_notes(notes: List[NoteEvent], semitones: int) -> List[NoteEvent]:
    """
    移调音符
    
    参数:
        notes: 音符事件列表
        semitones: 半音数（正数升高，负数降低）
    
    返回:
        移调后的音符事件列表
    """
    transposed = []
    for note in notes:
        new_note_value = note.note + semitones
        if 0 <= new_note_value <= 127:
            transposed.append(NoteEvent(
                note=new_note_value,
                note_name=midi_note_to_name(new_note_value),
                start_time=note.start_time,
                duration=note.duration,
                velocity=note.velocity,
                channel=note.channel,
                instrument=note.instrument,
                track_name=note.track_name
            ))
    return transposed


def notes_to_text(notes: List[NoteEvent]) -> str:
    """
    将音符列表转换为可读文本
    
    参数:
        notes: 音符事件列表
    
    返回:
        格式化的文本
    """
    lines = []
    lines.append(f"{'Note':<6} {'Start':>10} {'Duration':>10} {'Velocity':>10} {'Channel':>8}")
    lines.append("-" * 50)
    
    for note in sorted(notes, key=lambda n: n.start_time):
        lines.append(
            f"{note.note_name:<6} "
            f"{note.start_time:>10.3f}s "
            f"{note.duration:>10.3f}s "
            f"{note.velocity:>10} "
            f"{note.channel:>8}"
        )
    
    return "\n".join(lines)


def create_scale(scale_type: str = "major", root: str = "C4", 
                 bpm: float = 120.0, velocity: int = 80) -> MIDIFile:
    """
    创建音阶 MIDI 文件
    
    参数:
        scale_type: 音阶类型 ("major", "minor", "pentatonic", "blues", "chromatic")
        root: 根音 (如 "C4", "D#4")
        bpm: 速度
        velocity: 力度
    
    返回:
        MIDIFile 对象
    """
    # 音阶间隔模式（半音）
    SCALE_PATTERNS = {
        "major": [0, 2, 4, 5, 7, 9, 11, 12],
        "minor": [0, 2, 3, 5, 7, 8, 10, 12],
        "pentatonic": [0, 2, 4, 7, 9, 12],
        "blues": [0, 3, 5, 6, 7, 10, 12],
        "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    }
    
    if scale_type not in SCALE_PATTERNS:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    root_note = name_to_midi_note(root)
    pattern = SCALE_PATTERNS[scale_type]
    
    notes = []
    for interval in pattern:
        note_value = root_note + interval
        if 0 <= note_value <= 127:
            notes.append((midi_note_to_name(note_value), 0.5))
    
    return create_simple_melody(notes, bpm=bpm, velocity=velocity)


def create_chord(chord_name: str, duration: float = 1.0, 
                 bpm: float = 120.0, velocity: int = 80) -> MIDIFile:
    """
    创建和弦 MIDI 文件
    
    参数:
        chord_name: 和弦名称 (如 "C4:major", "G4:minor", "F#4:dim7")
        duration: 持续时间（四分音符为单位）
        bpm: 速度
        velocity: 力度
    
    返回:
        MIDIFile 对象
    """
    # 和弦模式（半音间隔）
    CHORD_PATTERNS = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
        "dim7": [0, 3, 6, 9],
        "sus4": [0, 5, 7],
        "sus2": [0, 2, 7],
    }
    
    # 解析和弦名称
    if ':' in chord_name:
        root, chord_type = chord_name.split(':')
    else:
        root = chord_name
        chord_type = "major"
    
    if chord_type not in CHORD_PATTERNS:
        raise ValueError(f"Unknown chord type: {chord_type}")
    
    root_note = name_to_midi_note(root)
    pattern = CHORD_PATTERNS[chord_type]
    
    midi_file = MIDIFile(format_type=0, bpm=bpm)
    track = MIDITrack(name="Chord")
    
    events = []
    events.append(create_tempo_event(0, bpm))
    
    # 添加和弦音符
    for interval in pattern:
        note_value = root_note + interval
        if 0 <= note_value <= 127:
            # NOTE_ON (同时发音)
            events.append(MIDIEvent(
                delta_time=0,
                event_type=MIDIMessageType.NOTE_ON,
                channel=0,
                data=bytes([note_value, velocity])
            ))
    
    duration_ticks = int(duration * midi_file.ticks_per_beat)
    
    # 添加 NOTE_OFF
    for interval in pattern:
        note_value = root_note + interval
        if 0 <= note_value <= 127:
            events.append(MIDIEvent(
                delta_time=duration_ticks,
                event_type=MIDIMessageType.NOTE_OFF,
                channel=0,
                data=bytes([note_value, 0])
            ))
    
    # 重新计算 delta time
    events.sort(key=lambda e: e.delta_time)
    prev_time = 0
    for event in events:
        delta = event.delta_time - prev_time
        event.delta_time = delta
        prev_time += delta
    
    events.append(create_end_of_track_event())
    track.events = events
    midi_file.tracks.append(track)
    
    return midi_file


# ============================================================================
# 便捷函数
# ============================================================================

def read_midi(filepath: Union[str, Path]) -> MIDIFile:
    """读取 MIDI 文件（parse_midi_file 的别名）"""
    return parse_midi_file(filepath)


def write_midi(midi_file: MIDIFile, filepath: Union[str, Path]) -> bool:
    """写入 MIDI 文件（write_midi_file 的别名）"""
    return write_midi_file(midi_file, filepath)


def midi_info(filepath: Union[str, Path]) -> str:
    """获取 MIDI 文件信息的可读字符串"""
    info = get_midi_info(filepath)
    return str(info)


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("MIDI Utilities - Zero-dependency MIDI file processing")
        print("\nUsage:")
        print("  python mod.py info <file.mid>      - Show MIDI file info")
        print("  python mod.py notes <file.mid>     - Extract and show notes")
        print("  python mod.py scale <type> <root>  - Create scale")
        print("  python mod.py demo                 - Create demo MIDI file")
        print("\nExample:")
        print("  python mod.py info song.mid")
        print("  python mod.py notes song.mid")
        print("  python mod.py scale major C4")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "info" and len(sys.argv) > 2:
        info = get_midi_info(sys.argv[2])
        print(info)
    
    elif command == "notes" and len(sys.argv) > 2:
        notes = extract_notes(sys.argv[2])
        print(notes_to_text(notes))
        print(f"\nTotal notes: {len(notes)}")
    
    elif command == "scale" and len(sys.argv) > 4:
        scale_type = sys.argv[2]
        root = sys.argv[3]
        output = sys.argv[4]
        
        midi = create_scale(scale_type, root)
        write_midi_file(midi, output)
        print(f"Created {scale_type} scale starting at {root}")
        print(f"Output: {output}")
    
    elif command == "demo":
        # 创建演示文件
        demo_melody = [
            ("C4", 1.0), ("D4", 1.0), ("E4", 1.0), ("F4", 1.0),
            ("G4", 2.0), ("R", 0.5),
            ("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 1.0),
            ("E4", 1.0), ("D4", 1.0), ("C4", 2.0),
        ]
        
        midi = create_simple_melody(demo_melody, bpm=120, program=0)
        write_midi_file(midi, "demo_melody.mid")
        print("Created demo_melody.mid")
        
        # 创建音阶
        scale = create_scale("major", "C4")
        write_midi_file(scale, "demo_scale.mid")
        print("Created demo_scale.mid")
        
        # 创建和弦
        chord = create_chord("C4:maj7")
        write_midi_file(chord, "demo_chord.mid")
        print("Created demo_chord.mid")
    
    else:
        print("Unknown command or missing arguments")
        print("Run 'python mod.py' for usage information")