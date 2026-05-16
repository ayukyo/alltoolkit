"""
节拍器工具模块 (Metronome Utils)

提供节拍器相关功能，包括 BPM 计算、节拍生成、时间计算、
速度标记转换、节奏模式等，帮助音乐家练习节奏。

零外部依赖，纯 Python 标准库实现。

作者: AllToolkit
日期: 2026-05-17
"""

import math
import time
import threading
from typing import Optional, Callable, List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class TimeSignature(Enum):
    """拍号枚举"""
    TWO_FOUR = (2, 4)      # 2/4 拍
    THREE_FOUR = (3, 4)    # 3/4 拍
    FOUR_FOUR = (4, 4)     # 4/4 拍
    SIX_EIGHT = (6, 8)     # 6/8 拍
    NINE_EIGHT = (9, 8)    # 9/8 拍
    TWELVE_EIGHT = (12, 8) # 12/8 拍
    FIVE_FOUR = (5, 4)     # 5/4 拍
    SEVEN_EIGHT = (7, 8)   # 7/8 拍
    THREE_EIGHT = (3, 8)   # 3/8 拍
    SIX_FOUR = (6, 4)      # 6/4 拍


class TempoMarking(Enum):
    """速度标记枚举（意大利语术语）"""
    LARGHISSIMO = ("Larghissimo", 20, 40)       # 极广板
    GRAVE = ("Grave", 25, 45)                   # 庄板
    LARGO = ("Largo", 40, 60)                   # 广板
    LENTO = ("Lento", 45, 60)                   # 慢板
    LARGHETTO = ("Larghetto", 60, 66)           # 甚广板
    ADAGIO = ("Adagio", 66, 76)                 # 柔板
    ADAGIETTO = ("Adagietto", 70, 80)           # 小柔板
    ANDANTE = ("Andante", 76, 108)              # 行板
    ANDANTINO = ("Andantino", 80, 108)          # 小行板
    MARCIA_MODERATO = ("Marcia Moderato", 83, 85)  # 中板进行曲
    MODERATO = ("Moderato", 108, 120)           # 中板
    ALLEGRETTO = ("Allegretto", 100, 128)      # 小快板
    ALLEGRO = ("Allegro", 120, 168)             # 快板
    VIVACE = ("Vivace", 168, 176)               # 活泼快板
    VIVACISSIMO = ("Vivacissimo", 172, 176)     # 极活泼快板
    ALLEGRERO = ("Allegrero", 174, 176)         # 极快板
    PRESTO = ("Presto", 168, 200)               # 急板
    PRESTISSIMO = ("Prestissimo", 200, 250)     # 极急板

    @property
    def italian(self) -> str:
        """获取意大利语名称"""
        return self.value[0]

    @property
    def min_bpm(self) -> int:
        """获取最小 BPM"""
        return self.value[1]

    @property
    def max_bpm(self) -> int:
        """获取最大 BPM"""
        return self.value[2]


class Subdivision(Enum):
    """节拍细分类型"""
    QUARTER = (1, "四分音符")           # 基本拍
    EIGHTH = (2, "八分音符")            # 每拍分2份
    TRIPLET = (3, "三连音")             # 每拍分3份
    SIXTEENTH = (4, "十六分音符")       # 每拍分4份
    QUINTUPLET = (5, "五连音")          # 每拍分5份
    SEXTUPLET = (6, "六连音")           # 每拍分6份
    SEPTUPLET = (7, "七连音")           # 每拍分7份
    THIRTY_SECOND = (8, "三十二分音符")  # 每拍分8份

    @property
    def divisions(self) -> int:
        """获取细分数量"""
        return self.value[0]

    @property
    def name(self) -> str:
        """获取中文名称"""
        return self.value[1]


@dataclass
class Beat:
    """节拍数据类"""
    position: int           # 在小节中的位置（从1开始）
    is_downbeat: bool       # 是否为强拍
    is_accent: bool         # 是否重音
    beat_type: str          # 拍类型：'downbeat', 'upbeat', 'offbeat'
    time_ms: float          # 距离小节开始的时间（毫秒）


@dataclass
class PracticeSession:
    """练习会话数据类"""
    bpm: int                                    # 当前 BPM
    time_signature: TimeSignature               # 拍号
    duration_seconds: float                     # 总时长（秒）
    beats_played: int                           # 已演奏拍数
    measures_completed: int                     # 已完成小节数
    subdivision: Subdivision                    # 细分类型
    elapsed_seconds: float = 0.0                # 已用时间


class Metronome:
    """
    节拍器类
    
    提供完整的节拍器功能，包括节拍生成、
    练习模式、节奏模式等。
    """
    
    def __init__(
        self,
        bpm: int = 120,
        time_signature: TimeSignature = TimeSignature.FOUR_FOUR,
        subdivision: Subdivision = Subdivision.QUARTER
    ):
        """
        初始化节拍器
        
        Args:
            bpm: 每分钟拍数
            time_signature: 拍号
            subdivision: 节拍细分
        """
        self._bpm = max(20, min(250, bpm))  # 限制在20-250 BPM
        self._time_signature = time_signature
        self._subdivision = subdivision
        self._is_running = False
        self._current_beat = 0
        self._current_subdivision = 0
        self._beat_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._on_beat_callback: Optional[Callable[[int, int, bool], None]] = None
        self._practice_start_time: Optional[float] = None
        
    @property
    def bpm(self) -> int:
        """获取当前 BPM"""
        return self._bpm
    
    @bpm.setter
    def bpm(self, value: int):
        """设置 BPM"""
        self._bpm = max(20, min(250, value))
    
    @property
    def time_signature(self) -> TimeSignature:
        """获取拍号"""
        return self._time_signature
    
    @time_signature.setter
    def time_signature(self, value: TimeSignature):
        """设置拍号"""
        self._time_signature = value
    
    @property
    def subdivision(self) -> Subdivision:
        """获取细分类型"""
        return self._subdivision
    
    @subdivision.setter
    def subdivision(self, value: Subdivision):
        """设置细分类型"""
        self._subdivision = value
    
    @property
    def beats_per_measure(self) -> int:
        """获取每小节拍数"""
        return self._time_signature.value[0]
    
    @property
    def beat_unit(self) -> int:
        """获取拍单位（如 4 表示四分音符为一拍）"""
        return self._time_signature.value[1]
    
    @property
    def is_running(self) -> bool:
        """检查节拍器是否正在运行"""
        return self._is_running
    
    @property
    def current_beat(self) -> int:
        """获取当前拍位置（从1开始）"""
        return self._current_beat
    
    @property
    def current_measure(self) -> int:
        """获取当前小节数"""
        if self._current_beat == 0:
            return 0
        return (self._current_beat - 1) // self.beats_per_measure + 1
    
    def get_beat_duration_ms(self) -> float:
        """
        获取一拍的时长（毫秒）
        
        Returns:
            一拍的毫秒数
        """
        return 60000.0 / self._bpm
    
    def get_beat_duration_seconds(self) -> float:
        """
        获取一拍的时长（秒）
        
        Returns:
            一拍的秒数
        """
        return 60.0 / self._bpm
    
    def get_subdivision_duration_ms(self) -> float:
        """
        获取细分的时长（毫秒）
        
        Returns:
            细分的毫秒数
        """
        return self.get_beat_duration_ms() / self._subdivision.divisions
    
    def get_measure_duration_ms(self) -> float:
        """
        获取一小节的时长（毫秒）
        
        Returns:
            一小节的毫秒数
        """
        return self.get_beat_duration_ms() * self.beats_per_measure
    
    def get_measure_duration_seconds(self) -> float:
        """
        获取一小节的时长（秒）
        
        Returns:
            一小节的秒数
        """
        return self.get_beat_duration_seconds() * self.beats_per_measure
    
    def get_downbeats(self) -> List[int]:
        """
        获取小节中的强拍位置列表
        
        Returns:
            强拍位置列表（从1开始）
        """
        beats = self.beats_per_measure
        beat_unit = self.beat_unit
        
        # 根据拍号确定强拍位置
        if beat_unit == 4:
            # 简单拍号：每拍是四分音符
            if beats == 2:  # 2/4
                return [1]
            elif beats == 3:  # 3/4
                return [1]
            elif beats == 4:  # 4/4
                return [1, 3]
            elif beats == 5:  # 5/4
                return [1, 4]
            elif beats == 6:  # 6/4
                return [1, 4]
            else:
                return [1]
        elif beat_unit == 8:
            # 复合拍号：每拍是附点四分音符（三拍八分音符）
            if beats == 6:  # 6/8
                return [1]
            elif beats == 9:  # 9/8
                return [1, 4]
            elif beats == 12:  # 12/8
                return [1, 4, 7]
            elif beats == 7:  # 7/8
                return [1, 4]
            elif beats == 3:  # 3/8
                return [1]
            else:
                return [1]
        else:
            return [1]
    
    def is_downbeat(self, beat: int) -> bool:
        """
        判断指定拍是否为强拍
        
        Args:
            beat: 拍位置（从1开始）
            
        Returns:
            是否为强拍
        """
        downbeats = self.get_downbeats()
        return beat in downbeats
    
    def get_beat_type(self, beat: int) -> str:
        """
        获取拍的类型
        
        Args:
            beat: 拍位置（从1开始）
            
        Returns:
            拍类型：'downbeat', 'upbeat', 'offbeat'
        """
        downbeats = self.get_downbeats()
        if beat in downbeats:
            return 'downbeat'
        elif beat <= self.beats_per_measure:
            return 'upbeat'
        else:
            return 'offbeat'
    
    def generate_beats(self, num_measures: int = 1) -> List[Beat]:
        """
        生成指定小节数的节拍
        
        Args:
            num_measures: 小节数
            
        Returns:
            节拍列表
        """
        beats = []
        beat_duration_ms = self.get_beat_duration_ms()
        downbeats = self.get_downbeats()
        
        for measure in range(num_measures):
            measure_start_time = measure * self.get_measure_duration_ms()
            
            for beat_in_measure in range(1, self.beats_per_measure + 1):
                global_beat = measure * self.beats_per_measure + beat_in_measure
                is_downbeat = beat_in_measure in downbeats
                beat_type = self.get_beat_type(beat_in_measure)
                
                beat = Beat(
                    position=beat_in_measure,
                    is_downbeat=is_downbeat,
                    is_accent=is_downbeat,  # 默认强拍重音
                    beat_type=beat_type,
                    time_ms=measure_start_time + (beat_in_measure - 1) * beat_duration_ms
                )
                beats.append(beat)
        
        return beats
    
    def generate_subdivisions(self, num_beats: int = 1) -> List[Dict[str, Any]]:
        """
        生成指定拍数的细分
        
        Args:
            num_beats: 拍数
            
        Returns:
            细分列表，每个元素包含拍位置、细分位置、是否强拍等信息
        """
        subdivisions = []
        subdivision_duration_ms = self.get_subdivision_duration_ms()
        downbeats = self.get_downbeats()
        
        for beat_num in range(1, num_beats + 1):
            beat_in_measure = ((beat_num - 1) % self.beats_per_measure) + 1
            is_downbeat = beat_in_measure in downbeats
            
            for sub_num in range(self._subdivision.divisions):
                subdivisions.append({
                    'beat': beat_num,
                    'beat_in_measure': beat_in_measure,
                    'subdivision': sub_num + 1,
                    'is_first_subdivision': sub_num == 0,
                    'is_downbeat': is_downbeat and sub_num == 0,
                    'time_ms': ((beat_num - 1) * self.get_beat_duration_ms() + 
                               sub_num * subdivision_duration_ms)
                })
        
        return subdivisions
    
    def set_on_beat_callback(self, callback: Callable[[int, int, bool], None]):
        """
        设置节拍回调函数
        
        Args:
            callback: 回调函数，参数为 (拍位置, 小节数, 是否强拍)
        """
        self._on_beat_callback = callback
    
    def _beat_loop(self):
        """节拍循环"""
        beat_duration = self.get_beat_duration_seconds()
        
        while not self._stop_event.is_set():
            self._current_beat += 1
            beat_in_measure = ((self._current_beat - 1) % self.beats_per_measure) + 1
            is_downbeat = self.is_downbeat(beat_in_measure)
            
            if self._on_beat_callback:
                try:
                    self._on_beat_callback(beat_in_measure, self.current_measure, is_downbeat)
                except Exception:
                    pass
            
            # 等待一拍的时间
            self._stop_event.wait(beat_duration)
    
    def start(self):
        """启动节拍器"""
        if self._is_running:
            return
        
        self._is_running = True
        self._stop_event.clear()
        self._current_beat = 0
        self._practice_start_time = time.time()
        
        self._beat_thread = threading.Thread(target=self._beat_loop, daemon=True)
        self._beat_thread.start()
    
    def stop(self):
        """停止节拍器"""
        if not self._is_running:
            return
        
        self._is_running = False
        self._stop_event.set()
        
        if self._beat_thread:
            self._beat_thread.join(timeout=1.0)
            self._beat_thread = None
    
    def tap(self, times: int = 3) -> float:
        """
        Tap tempo 功能（需要手动调用）
        返回上次调用到现在的时间间隔，用于计算 BPM
        
        Args:
            times: 点击次数
            
        Returns:
            时间间隔（秒）
        """
        current_time = time.time()
        interval = current_time - getattr(self, '_last_tap_time', current_time)
        self._last_tap_time = current_time
        return interval
    
    def calculate_bpm_from_taps(self, intervals: List[float]) -> int:
        """
        从时间间隔列表计算 BPM
        
        Args:
            intervals: 时间间隔列表（秒）
            
        Returns:
            平均 BPM
        """
        if not intervals:
            return self._bpm
        
        avg_interval = sum(intervals) / len(intervals)
        if avg_interval == 0:
            return self._bpm
        
        bpm = 60.0 / avg_interval
        return int(max(20, min(250, round(bpm))))
    
    def get_practice_session(self) -> PracticeSession:
        """
        获取当前练习会话信息
        
        Returns:
            练习会话数据
        """
        elapsed = 0.0
        if self._practice_start_time:
            elapsed = time.time() - self._practice_start_time
        
        return PracticeSession(
            bpm=self._bpm,
            time_signature=self._time_signature,
            duration_seconds=elapsed,
            beats_played=self._current_beat,
            measures_completed=max(0, self.current_measure),
            subdivision=self._subdivision,
            elapsed_seconds=elapsed
        )


# ==================== 工具函数 ====================

def bpm_to_ms(bpm: int) -> float:
    """
    将 BPM 转换为每拍的毫秒数
    
    Args:
        bpm: 每分钟拍数
        
    Returns:
        每拍的毫秒数
    """
    if bpm <= 0:
        raise ValueError("BPM must be positive")
    return 60000.0 / bpm


def bpm_to_seconds(bpm: int) -> float:
    """
    将 BPM 转换为每拍的秒数
    
    Args:
        bpm: 每分钟拍数
        
    Returns:
        每拍的秒数
    """
    if bpm <= 0:
        raise ValueError("BPM must be positive")
    return 60.0 / bpm


def ms_to_bpm(ms: float) -> int:
    """
    将毫秒转换为 BPM
    
    Args:
        ms: 每拍的毫秒数
        
    Returns:
        BPM 值
    """
    if ms <= 0:
        raise ValueError("Milliseconds must be positive")
    return int(round(60000.0 / ms))


def seconds_to_bpm(seconds: float) -> int:
    """
    将秒转换为 BPM
    
    Args:
        seconds: 每拍的秒数
        
    Returns:
        BPM 值
    """
    if seconds <= 0:
        raise ValueError("Seconds must be positive")
    return int(round(60.0 / seconds))


def get_tempo_marking(bpm: int) -> Tuple[str, str]:
    """
    根据 BPM 获取对应的意大利语速度标记
    
    Args:
        bpm: 每分钟拍数
        
    Returns:
        (意大利语名称, 中文描述)
    """
    for marking in TempoMarking:
        if marking.min_bpm <= bpm <= marking.max_bpm:
            return (marking.italian, marking.name)
    
    # 超出范围
    if bpm < TempoMarking.LARGHISSIMO.min_bpm:
        return (TempoMarking.LARGHISSIMO.italian, "极慢")
    else:
        return (TempoMarking.PRESTISSIMO.italian, "极快")


def get_bpm_range_for_tempo(tempo_name: str) -> Tuple[int, int]:
    """
    根据速度标记名称获取 BPM 范围
    
    Args:
        tempo_name: 速度标记名称（意大利语或中文）
        
    Returns:
        (最小 BPM, 最大 BPM)
    """
    tempo_name_lower = tempo_name.lower()
    
    # 中文名称映射到枚举成员
    chinese_to_marking = {
        '极广板': TempoMarking.LARGHISSIMO,
        '庄板': TempoMarking.GRAVE,
        '广板': TempoMarking.LARGO,
        '慢板': TempoMarking.LENTO,
        '甚广板': TempoMarking.LARGHETTO,
        '柔板': TempoMarking.ADAGIO,
        '小柔板': TempoMarking.ADAGIETTO,
        '行板': TempoMarking.ANDANTE,
        '小行板': TempoMarking.ANDANTINO,
        '中板进行曲': TempoMarking.MARCIA_MODERATO,
        '中板': TempoMarking.MODERATO,
        '小快板': TempoMarking.ALLEGRETTO,
        '快板': TempoMarking.ALLEGRO,
        '活泼快板': TempoMarking.VIVACE,
        '极活泼快板': TempoMarking.VIVACISSIMO,
        '极快板': TempoMarking.ALLEGRERO,
        '急板': TempoMarking.PRESTO,
        '极急板': TempoMarking.PRESTISSIMO,
    }
    
    # 检查中文映射
    if tempo_name in chinese_to_marking:
        marking = chinese_to_marking[tempo_name]
        return (marking.min_bpm, marking.max_bpm)
    
    for marking in TempoMarking:
        if (tempo_name_lower == marking.italian.lower() or 
            tempo_name_lower == marking.name.lower() or
            tempo_name_lower == marking.name):
            return (marking.min_bpm, marking.max_bpm)
    
    # 默认返回中速范围
    return (108, 120)


def calculate_measures(
    bpm: int,
    duration_seconds: float,
    beats_per_measure: int = 4
) -> float:
    """
    计算在指定时间内的小节数
    
    Args:
        bpm: 每分钟拍数
        duration_seconds: 时长（秒）
        beats_per_measure: 每小节拍数
        
    Returns:
        小节数（可能为小数）
    """
    if bpm <= 0 or duration_seconds < 0:
        return 0.0
    
    beats = bpm * (duration_seconds / 60.0)
    return beats / beats_per_measure


def calculate_duration(
    bpm: int,
    measures: int,
    beats_per_measure: int = 4
) -> float:
    """
    计算指定小节数的时长
    
    Args:
        bpm: 每分钟拍数
        measures: 小节数
        beats_per_measure: 每小节拍数
        
    Returns:
        时长（秒）
    """
    if bpm <= 0 or measures < 0:
        return 0.0
    
    beats = measures * beats_per_measure
    return (beats / bpm) * 60.0


def adjust_bpm_for_exercise(
    current_bpm: int,
    target_bpm: int,
    difficulty: str = 'medium'
) -> List[int]:
    """
    生成练习 BPM 递进序列
    
    Args:
        current_bpm: 当前 BPM
        target_bpm: 目标 BPM
        difficulty: 难度级别 ('easy', 'medium', 'hard')
        
    Returns:
        BPM 递进列表
    """
    steps = {
        'easy': 5,      # 每次增加5 BPM
        'medium': 10,   # 每次增加10 BPM
        'hard': 15      # 每次增加15 BPM
    }
    
    step = steps.get(difficulty, 10)
    bpm_list = []
    
    if current_bpm < target_bpm:
        current = current_bpm
        while current < target_bpm:
            bpm_list.append(current)
            current += step
        bpm_list.append(target_bpm)
    elif current_bpm > target_bpm:
        current = current_bpm
        while current > target_bpm:
            bpm_list.append(current)
            current -= step
        bpm_list.append(target_bpm)
    else:
        bpm_list.append(current_bpm)
    
    return bpm_list


def get_subdivision_name(divisions: int) -> str:
    """
    根据细分数获取细分名称
    
    Args:
        divisions: 细分数
        
    Returns:
        细分名称
    """
    subdivision_names = {
        1: "四分音符",
        2: "八分音符",
        3: "三连音",
        4: "十六分音符",
        5: "五连音",
        6: "六连音",
        7: "七连音",
        8: "三十二分音符",
        9: "九连音",
        12: "十二连音",
        16: "六十四分音符"
    }
    return subdivision_names.get(divisions, f"{divisions}连音")


def calculate_delay_time(
    bpm: int,
    note_value: str = 'quarter'
) -> float:
    """
    计算延迟效果器的延迟时间
    
    Args:
        bpm: 每分钟拍数
        note_value: 音符时值 ('whole', 'half', 'quarter', 'eighth', 'sixteenth', 'dotted_half', 'dotted_quarter', 'dotted_eighth')
        
    Returns:
        延迟时间（毫秒）
    """
    quarter_ms = bpm_to_ms(bpm)
    
    note_multipliers = {
        'whole': 4.0,
        'half': 2.0,
        'quarter': 1.0,
        'eighth': 0.5,
        'sixteenth': 0.25,
        'thirty_second': 0.125,
        'dotted_half': 3.0,
        'dotted_quarter': 1.5,
        'dotted_eighth': 0.75,
        'dotted_sixteenth': 0.375,
        'triplet_half': 4.0 / 3.0,
        'triplet_quarter': 2.0 / 3.0,
        'triplet_eighth': 1.0 / 3.0
    }
    
    multiplier = note_multipliers.get(note_value, 1.0)
    return quarter_ms * multiplier


def calculate_reverb_pre_delay(bpm: int, note_value: str = 'eighth') -> float:
    """
    计算混响预延迟时间
    
    Args:
        bpm: 每分钟拍数
        note_value: 音符时值
        
    Returns:
        预延迟时间（毫秒）
    """
    return calculate_delay_time(bpm, note_value)


def time_signature_to_string(
    beats: int,
    beat_unit: int
) -> str:
    """
    将拍号转换为字符串表示
    
    Args:
        beats: 每小节拍数
        beat_unit: 拍单位
        
    Returns:
        拍号字符串（如 "4/4"）
    """
    return f"{beats}/{beat_unit}"


def parse_time_signature(ts_string: str) -> Tuple[int, int]:
    """
    解析拍号字符串
    
    Args:
        ts_string: 拍号字符串（如 "4/4", "6/8"）
        
    Returns:
        (每小节拍数, 拍单位)
    """
    try:
        parts = ts_string.replace(' ', '').split('/')
        if len(parts) == 2:
            beats = int(parts[0])
            beat_unit = int(parts[1])
            return (beats, beat_unit)
    except (ValueError, AttributeError):
        pass
    
    return (4, 4)  # 默认 4/4 拍


def get_time_signature_info(beats: int, beat_unit: int) -> Dict[str, Any]:
    """
    获取拍号的详细信息
    
    Args:
        beats: 每小节拍数
        beat_unit: 拍单位
        
    Returns:
        拍号信息字典
    """
    # 判断是简单拍号还是复合拍号
    is_compound = beat_unit == 8 and beats % 3 == 0
    
    # 确定强拍位置
    if is_compound:
        groups = beats // 3
        downbeats = [1] + [i * 3 + 1 for i in range(1, groups)]
    else:
        if beats == 2:
            downbeats = [1]
        elif beats == 3:
            downbeats = [1]
        elif beats == 4:
            downbeats = [1, 3]
        elif beats == 5:
            downbeats = [1, 4]  # 通常 2+3 或 3+2
        elif beats == 6:
            downbeats = [1, 4]
        elif beats == 7:
            downbeats = [1, 4]  # 通常 3+4 或 4+3
        else:
            downbeats = [1]
    
    # 拍号类型描述
    type_desc = "复合拍号" if is_compound else "简单拍号"
    
    # 常见拍号名称
    names = {
        (2, 4): "二四拍",
        (3, 4): "三四拍（华尔兹）",
        (4, 4): "四四拍（常用拍号）",
        (6, 8): "六八拍（复拍子）",
        (9, 8): "九八拍",
        (12, 8): "十二八拍",
        (5, 4): "五四拍（不对称拍号）",
        (7, 8): "七八拍（不对称拍号）",
        (3, 8): "三八拍",
        (6, 4): "六四拍"
    }
    
    return {
        'beats': beats,
        'beat_unit': beat_unit,
        'string': f"{beats}/{beat_unit}",
        'name': names.get((beats, beat_unit), f"{beats}/{beat_unit}拍"),
        'type': type_desc,
        'is_compound': is_compound,
        'downbeats': downbeats,
        'beat_divisions': 3 if is_compound else 1  # 复合拍每拍分3份
    }


def generate_rhythm_pattern(
    bpm: int,
    pattern: List[int],
    measures: int = 1
) -> List[Dict[str, Any]]:
    """
    生成节奏模式的时间点
    
    Args:
        bpm: 每分钟拍数
        pattern: 节奏模式列表，1表示有音，0表示休止符
                 例如 [1, 1, 0, 1] 表示 "强 弱 休止 弱"
        measures: 小节数
        
    Returns:
        时间点列表，每个元素包含时间和是否发声
    """
    if not pattern:
        return []
    
    beat_ms = bpm_to_ms(bpm)
    subdivision_ms = beat_ms / len(pattern)
    
    result = []
    for measure in range(measures):
        measure_start = measure * beat_ms
        for i, has_note in enumerate(pattern):
            result.append({
                'measure': measure + 1,
                'position': i + 1,
                'time_ms': measure_start + i * subdivision_ms,
                'has_note': bool(has_note),
                'is_accent': i == 0 and has_note == 1  # 第一个位置为重音
            })
    
    return result


def suggest_bpm_for_genre(genre: str) -> Dict[str, Any]:
    """
    根据音乐风格推荐 BPM 范围
    
    Args:
        genre: 音乐风格名称
        
    Returns:
        推荐信息字典
    """
    genre_bpm = {
        'ballad': (60, 80, "抒情慢歌"),
        'blues': (60, 90, "蓝调"),
        'rock': (110, 140, "摇滚"),
        'pop': (100, 130, "流行"),
        'hip_hop': (80, 115, "嘻哈"),
        'rap': (80, 120, "说唱"),
        'r&b': (70, 110, "节奏布鲁斯"),
        'jazz': (100, 150, "爵士"),
        'swing': (120, 150, "摇摆"),
        'funk': (110, 130, "放克"),
        'disco': (110, 140, "迪斯科"),
        'house': (120, 130, "浩室"),
        'techno': (120, 150, "科技舞曲"),
        'trance': (125, 150, "恍惚舞曲"),
        'dubstep': (140, 150, "回响贝斯"),
        'drum_and_bass': (160, 180, "鼓打贝斯"),
        'metal': (100, 160, "金属"),
        'punk': (150, 200, "朋克"),
        'country': (100, 140, "乡村"),
        'folk': (90, 120, "民谣"),
        'classical': (60, 120, "古典"),
        'electronic': (120, 150, "电子"),
        'edm': (128, 150, "电子舞曲"),
        'reggae': (60, 90, "雷鬼"),
        'salsa': (150, 220, "萨尔萨"),
        'tango': (110, 130, "探戈"),
        'waltz': (84, 120, "华尔兹"),
        'march': (100, 130, "进行曲"),
        'soul': (80, 110, "灵魂乐"),
        'gospel': (70, 100, "福音音乐")
    }
    
    genre_lower = genre.lower().replace('-', '_').replace(' ', '_')
    genre_lower = genre_lower.replace('&', 'n')
    
    if genre_lower in genre_bpm:
        min_bpm, max_bpm, name = genre_bpm[genre_lower]
        return {
            'genre': name,
            'min_bpm': min_bpm,
            'max_bpm': max_bpm,
            'suggested_bpm': (min_bpm + max_bpm) // 2,
            'tempo_marking': get_tempo_marking((min_bpm + max_bpm) // 2)[0]
        }
    
    # 未找到则返回默认
    return {
        'genre': genre,
        'min_bpm': 60,
        'max_bpm': 200,
        'suggested_bpm': 120,
        'tempo_marking': 'Moderato'
    }


def create_practice_routine(
    target_bpm: int,
    current_bpm: int,
    minutes_per_step: int = 5,
    difficulty: str = 'medium'
) -> List[Dict[str, Any]]:
    """
    创建练习计划
    
    Args:
        target_bpm: 目标 BPM
        current_bpm: 当前 BPM
        minutes_per_step: 每步练习时间（分钟）
        difficulty: 难度级别
        
    Returns:
        练习步骤列表
    """
    bpm_sequence = adjust_bpm_for_exercise(current_bpm, target_bpm, difficulty)
    
    routine = []
    for i, bpm in enumerate(bpm_sequence):
        step = {
            'step': i + 1,
            'bpm': bpm,
            'duration_minutes': minutes_per_step,
            'duration_beats': bpm * minutes_per_step,
            'tempo_marking': get_tempo_marking(bpm)[0],
            'is_target': bpm == target_bpm,
            'is_start': bpm == current_bpm
        }
        routine.append(step)
    
    return routine


def calculate_polymetric_bpm(
    bpm1: int,
    bpm2: int
) -> Dict[str, Any]:
    """
    计算多节奏的同步点
    
    Args:
        bpm1: 第一个节奏的 BPM
        bpm2: 第二个节奏的 BPM
        
    Returns:
        同步信息
    """
    from math import gcd
    
    # 计算最小公倍数
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    # 找到两个节奏的共同周期
    common_multiple = lcm(bpm1, bpm2)
    
    # 计算同步点（秒）
    sync_interval = 60.0 * common_multiple / (bpm1 * bpm2)
    
    # 每个节奏在同步点前的拍数
    beats1 = common_multiple // bpm2
    beats2 = common_multiple // bpm1
    
    return {
        'bpm1': bpm1,
        'bpm2': bpm2,
        'sync_interval_seconds': sync_interval,
        'sync_interval_beats': (beats1, beats2),
        'least_common_multiple': common_multiple
    }


def get_metronome_exercise(type: str) -> Dict[str, Any]:
    """
    获取节拍器练习类型
    
    Args:
        type: 练习类型 ('basic', 'subdivision', 'accent', 'polyrhythm', 'mixed')
        
    Returns:
        练习信息
    """
    exercises = {
        'basic': {
            'name': '基础节拍练习',
            'description': '跟随节拍器，每拍敲击一次',
            'difficulty': '初级',
            'recommended_bpm_range': (60, 100),
            'subdivision': Subdivision.QUARTER,
            'instructions': [
                '从较慢的BPM开始（60-70）',
                '确保每个音符都与节拍器精确对齐',
                '逐渐提高速度，每次增加5-10 BPM',
                '保持稳定的节奏感'
            ]
        },
        'subdivision': {
            'name': '细分练习',
            'description': '练习八分音符、三连音、十六分音符等细分',
            'difficulty': '中级',
            'recommended_bpm_range': (50, 80),
            'subdivision': Subdivision.SIXTEENTH,
            'instructions': [
                '先掌握八分音符细分',
                '然后练习三连音',
                '最后尝试十六分音符',
                '每个细分类型都从慢速开始'
            ]
        },
        'accent': {
            'name': '重音练习',
            'description': '在不同位置添加重音',
            'difficulty': '中级',
            'recommended_bpm_range': (60, 100),
            'subdivision': Subdivision.QUARTER,
            'instructions': [
                '在每拍的第一拍加重音',
                '尝试在弱拍加重音',
                '练习切分节奏',
                '使用节拍器的重音功能辅助'
            ]
        },
        'polyrhythm': {
            'name': '多节奏练习',
            'description': '练习2对3、3对4等多节奏',
            'difficulty': '高级',
            'recommended_bpm_range': (40, 70),
            'subdivision': Subdivision.SEXTUPLET,
            'instructions': [
                '从2对3开始练习',
                '口中念"二对三"的节奏',
                '双手分别演奏不同节奏',
                '慢慢提高速度'
            ]
        },
        'mixed': {
            'name': '混合练习',
            'description': '结合多种技巧的综合练习',
            'difficulty': '高级',
            'recommended_bpm_range': (50, 90),
            'subdivision': Subdivision.EIGHTH,
            'instructions': [
                '将细分和重音结合',
                '尝试改变拍号',
                '练习速度渐变',
                '加入动态变化'
            ]
        }
    }
    
    return exercises.get(type, exercises['basic'])


# 版本信息
__version__ = '1.0.0'
__author__ = 'AllToolkit'