"""
Frame Rate Utils - 帧率计算工具模块

提供帧率相关的各种计算功能，支持：
- 帧数与时间的相互转换
- 时间码格式处理（SMPTE 时间码）
- Drop-frame 和 Non-drop-frame 处理
- 帧率转换计算
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Union, Dict
from fractions import Fraction


# 常见帧率预设（帧/秒）
FRAME_RATE_PRESETS: Dict[str, Fraction] = {
    'film': Fraction(24, 1),           # 电影标准
    'pal': Fraction(25, 1),             # PAL 电视
    'ntsc': Fraction(30, 1),            # NTSC 整数帧率
    'ntsc_df': Fraction(30000, 1001),   # NTSC Drop-frame (29.97fps)
    'ntsc_ndf': Fraction(30000, 1001),  # NTSC Non-drop-frame
    'p25': Fraction(25, 1),             # 25fps
    'p30': Fraction(30, 1),             # 30fps
    'p50': Fraction(50, 1),             # 50fps
    'p60': Fraction(60, 1),             # 60fps
    'ntsc_60': Fraction(60000, 1001),   # 59.94fps
    'p24': Fraction(24, 1),             # 24fps
    'p48': Fraction(48, 1),             # 48fps (HFR)
    'p120': Fraction(120, 1),           # 120fps (HFR)
    'p240': Fraction(240, 1),           # 240fps (HFR)
}


@dataclass
class FrameRate:
    """
    帧率类，支持精确的分数表示
    
    Attributes:
        fps: 每秒帧数（分数形式）
        is_drop_frame: 是否为 drop-frame 格式（仅适用于 NTSC）
    """
    fps: Fraction
    is_drop_frame: bool = False
    
    def __init__(self, fps: Union[int, float, str, Fraction], is_drop_frame: bool = False):
        """
        初始化帧率
        
        Args:
            fps: 帧率值，可以是整数、浮点数、字符串或 Fraction
            is_drop_frame: 是否为 drop-frame 格式
        """
        if isinstance(fps, str):
            # 支持字符串形式，如 "30000/1001" 或 "29.97"
            if '/' in fps:
                self.fps = Fraction(fps)
            else:
                self.fps = Fraction(fps).limit_denominator(100000)
        elif isinstance(fps, (int, float)):
            self.fps = Fraction(fps).limit_denominator(100000)
        else:
            self.fps = fps
        self.is_drop_frame = is_drop_frame
    
    @property
    def float_value(self) -> float:
        """返回浮点数形式的帧率"""
        return float(self.fps)
    
    @property
    def numerator(self) -> int:
        """返回帧率分子"""
        return self.fps.numerator
    
    @property
    def denominator(self) -> int:
        """返回帧率分母"""
        return self.fps.denominator
    
    @property
    def frame_duration(self) -> Fraction:
        """返回每帧时长（秒）"""
        return Fraction(1, 1) / self.fps
    
    @property
    def frame_duration_ms(self) -> float:
        """返回每帧时长（毫秒）"""
        return float(self.frame_duration * 1000)
    
    def frames_to_seconds(self, frames: int) -> float:
        """
        将帧数转换为秒数
        
        Args:
            frames: 帧数
            
        Returns:
            秒数（浮点数）
        """
        return float(frames * self.frame_duration)
    
    def seconds_to_frames(self, seconds: float, rounding: str = 'round') -> int:
        """
        将秒数转换为帧数
        
        Args:
            seconds: 秒数
            rounding: 舍入方式 ('round', 'floor', 'ceil')
            
        Returns:
            帧数（整数）
        """
        raw_frames = seconds * float(self.fps)
        if rounding == 'floor':
            return int(raw_frames)
        elif rounding == 'ceil':
            return int(raw_frames + 0.999999)
        else:
            return int(round(raw_frames))
    
    def __str__(self) -> str:
        df_suffix = " (DF)" if self.is_drop_frame else ""
        return f"{self.float_value:.4g} fps{df_suffix}"
    
    def __repr__(self) -> str:
        return f"FrameRate({self.fps}, is_drop_frame={self.is_drop_frame})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, FrameRate):
            return self.fps == other.fps and self.is_drop_frame == other.is_drop_frame
        return False
    
    def __hash__(self) -> int:
        return hash((self.fps, self.is_drop_frame))


class DropFrameCalculator:
    """
    Drop-frame 计算器
    
    NTSC 视频的实际帧率是 29.97fps (30000/1001)，
    为了便于时间计算，使用 drop-frame 方式：
    每分钟丢弃前 2 帧（除了第 0, 10, 20, 30, 40, 50 分钟）
    这样 1 小时正好是 107892 帧，对应时间码显示 1:00:00:00
    """
    
    @staticmethod
    def is_drop_frame_rate(fps: Union[Fraction, FrameRate, int, float]) -> bool:
        """
        判断是否为 drop-frame 帧率
        
        Args:
            fps: 帧率
            
        Returns:
            是否为 drop-frame 帧率
        """
        if isinstance(fps, FrameRate):
            return fps.is_drop_frame
        if isinstance(fps, (int, float)):
            fps = Fraction(fps).limit_denominator(100000)
        # 标准的 drop-frame 帧率
        drop_frame_rates = [
            Fraction(30000, 1001),   # 29.97fps
            Fraction(60000, 1001),   # 59.94fps
            Fraction(24000, 1001),   # 23.976fps
        ]
        return fps in drop_frame_rates
    
    @staticmethod
    def calculate_drop_frame_count(frames: int, fps: Fraction = Fraction(30000, 1001)) -> int:
        """
        计算在 drop-frame 模式下需要丢弃的帧数
        
        Args:
            frames: 总帧数
            fps: 帧率（默认 29.97fps）
            
        Returns:
            需要丢弃的帧数
        """
        # 计算帧持续时间（毫秒）
        frame_duration_ms = 1000 * float(Fraction(1001, 30000)) if fps == Fraction(30000, 1001) else 1000 / float(fps)
        
        # 计算总时长（毫秒）
        total_ms = frames * frame_duration_ms
        
        # 计算完整分钟数
        total_minutes = int(total_ms / 60000)
        
        # 每 10 分钟一个周期，每分钟丢 2 帧（除了第 0 分钟）
        # 每 10 分钟丢 18 帧 (9 分钟 * 2)
        drop_frames = (total_minutes // 10) * 18 + (total_minutes % 10) * 2
        
        return drop_frames
    
    @staticmethod
    def frames_to_timecode_df(frames: int, fps: Fraction = Fraction(30000, 1001)) -> str:
        """
        将帧数转换为 drop-frame 时间码
        
        Args:
            frames: 帧数
            fps: 帧率
            
        Returns:
            时间码字符串 (HH:MM:SS;FF 格式，分号表示 drop-frame)
        """
        # 每秒帧数（整数）
        fps_int = int(round(float(fps)))  # 30
        
        # 每分钟丢弃的帧数
        drop_frames_per_minute = 2
        
        # 计算总分钟数（用于计算丢弃的帧）
        # 使用简化的公式
        frames_per_10_minutes = fps_int * 60 * 10 - 2 * 9  # 30*600 - 18 = 17982
        
        # 计算小时、分钟、秒、帧
        hours = frames // (frames_per_10_minutes * 6)
        remaining = frames % (frames_per_10_minutes * 6)
        
        ten_minute_blocks = remaining // frames_per_10_minutes
        remaining = remaining % frames_per_10_minutes
        
        # 计算分钟内的帧
        frames_per_minute_df = fps_int * 60 - 2  # 1798 for 30fps
        
        minutes_in_block = remaining // frames_per_minute_df
        frames_in_minute = remaining % frames_per_minute_df
        
        minutes = ten_minute_blocks * 10 + minutes_in_block
        seconds = frames_in_minute // fps_int
        frames_remaining = frames_in_minute % fps_int
        
        # 调整小时（因为上面的计算可能有偏差）
        if minutes >= 60:
            hours += minutes // 60
            minutes = minutes % 60
        
        # 格式化时间码（使用分号表示 drop-frame）
        return f"{hours:02d}:{minutes:02d}:{seconds:02d};{frames_remaining:02d}"
    
    @staticmethod
    def timecode_df_to_frames(timecode: str, fps: Fraction = Fraction(30000, 1001)) -> int:
        """
        将 drop-frame 时间码转换为帧数
        
        Args:
            timecode: 时间码字符串 (HH:MM:SS;FF 或 HH:MM:SS:FF)
            fps: 帧率
            
        Returns:
            帧数
        """
        # 支持分号或冒号分隔
        tc = timecode.replace(';', ':').replace('.', ':')
        parts = tc.split(':')
        
        if len(parts) != 4:
            raise ValueError(f"Invalid timecode format: {timecode}")
        
        hours, minutes, seconds, frames = map(int, parts)
        
        fps_int = int(round(float(fps)))  # 30
        drop_frames_per_minute = 2
        
        # 计算总分钟数
        total_minutes = hours * 60 + minutes
        
        # 计算需要丢弃的帧数
        # 每 10 分钟丢 18 帧
        drop_frames = (total_minutes // 10) * 18 + (total_minutes % 10) * 2
        
        # 计算总帧数
        total_frames = (hours * 3600 + minutes * 60 + seconds) * fps_int + frames - drop_frames
        
        return max(0, total_frames)


@dataclass
class Timecode:
    """
    时间码类，表示视频中的时间位置
    
    支持格式：
    - HH:MM:SS:FF (non-drop frame)
    - HH:MM:SS;FF (drop frame)
    - HH:MM:SS.mmm (毫秒)
    - 秒数（浮点数）
    - 帧数（整数）
    """
    hours: int
    minutes: int
    seconds: int
    frames: int
    fps: FrameRate
    is_drop_frame: bool = False
    
    @classmethod
    def from_frames(cls, frames: int, fps: Union[FrameRate, Fraction, int, float] = 30,
                   is_drop_frame: bool = False) -> 'Timecode':
        """
        从帧数创建时间码
        
        Args:
            frames: 帧数
            fps: 帧率
            is_drop_frame: 是否为 drop-frame
            
        Returns:
            Timecode 对象
        """
        if not isinstance(fps, FrameRate):
            fps = FrameRate(fps, is_drop_frame)
        
        fps_int = int(round(fps.float_value))
        
        if is_drop_frame and DropFrameCalculator.is_drop_frame_rate(fps):
            # Drop-frame 计算
            total_frames = frames
            
            frames_per_10_minutes = fps_int * 600 - 18
            frames_per_minute = fps_int * 60 - 2
            
            hours = total_frames // (frames_per_10_minutes * 6)
            total_frames %= (frames_per_10_minutes * 6)
            
            ten_min_blocks = total_frames // frames_per_10_minutes
            total_frames %= frames_per_10_minutes
            
            minutes = ten_min_blocks * 10
            if total_frames >= frames_per_minute:
                minutes += 1
                total_frames -= frames_per_minute
                if total_frames >= frames_per_minute:
                    minutes += 1
                    total_frames -= frames_per_minute
            
            # 调整
            while minutes >= 60:
                hours += 1
                minutes -= 60
            
            seconds = total_frames // fps_int
            remaining_frames = total_frames % fps_int
            
            return cls(hours, minutes, seconds, remaining_frames, fps, True)
        else:
            # Non-drop-frame 计算
            frames_per_hour = fps_int * 3600
            frames_per_minute = fps_int * 60
            frames_per_second = fps_int
            
            hours = frames // frames_per_hour
            remaining = frames % frames_per_hour
            
            minutes = remaining // frames_per_minute
            remaining = remaining % frames_per_minute
            
            seconds = remaining // fps_int
            remaining_frames = remaining % fps_int
            
            return cls(hours, minutes, seconds, remaining_frames, fps, is_drop_frame)
    
    @classmethod
    def from_seconds(cls, seconds: float, fps: Union[FrameRate, Fraction, int, float] = 30,
                    is_drop_frame: bool = False) -> 'Timecode':
        """
        从秒数创建时间码
        
        Args:
            seconds: 秒数
            fps: 帧率
            is_drop_frame: 是否为 drop-frame
            
        Returns:
            Timecode 对象
        """
        if not isinstance(fps, FrameRate):
            fps = FrameRate(fps, is_drop_frame)
        
        frames = fps.seconds_to_frames(seconds)
        return cls.from_frames(frames, fps, is_drop_frame)
    
    @classmethod
    def from_string(cls, timecode: str, fps: Union[FrameRate, Fraction, int, float] = 30) -> 'Timecode':
        """
        从字符串解析时间码
        
        Args:
            timecode: 时间码字符串
            fps: 帧率
            
        Returns:
            Timecode 对象
        """
        if not isinstance(fps, FrameRate):
            fps = FrameRate(fps)
        
        # 判断是否为 drop-frame（使用分号）
        is_drop_frame = ';' in timecode
        
        # 支持多种分隔符
        tc = timecode.replace(';', ':').replace('.', ':')
        parts = tc.split(':')
        
        if len(parts) == 4:
            hours, minutes, seconds, frames = map(int, parts)
        elif len(parts) == 3:
            hours = 0
            minutes, seconds, frames = map(int, parts)
        else:
            raise ValueError(f"Invalid timecode format: {timecode}")
        
        return cls(hours, minutes, seconds, frames, fps, is_drop_frame)
    
    @property
    def total_frames(self) -> int:
        """
        返回总帧数
        """
        fps_int = int(round(self.fps.float_value))
        
        if self.is_drop_frame:
            # Drop-frame 计算
            total_minutes = self.hours * 60 + self.minutes
            drop_frames = (total_minutes // 10) * 18 + (total_minutes % 10) * 2
            return (self.hours * 3600 + self.minutes * 60 + self.seconds) * fps_int + self.frames - drop_frames
        else:
            # Non-drop-frame 计算
            return (self.hours * 3600 + self.minutes * 60 + self.seconds) * fps_int + self.frames
    
    @property
    def total_seconds(self) -> float:
        """返回总秒数"""
        return self.fps.frames_to_seconds(self.total_frames)
    
    @property
    def total_milliseconds(self) -> int:
        """返回总毫秒数"""
        return int(self.total_seconds * 1000)
    
    def __str__(self) -> str:
        """返回时间码字符串"""
        separator = ';' if self.is_drop_frame else ':'
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}{separator}{self.frames:02d}"
    
    def __repr__(self) -> str:
        return f"Timecode({self}, fps={self.fps})"
    
    def __add__(self, other: Union['Timecode', int]) -> 'Timecode':
        """添加帧数或时间码"""
        if isinstance(other, Timecode):
            total = self.total_frames + other.total_frames
        else:
            total = self.total_frames + other
        return Timecode.from_frames(total, self.fps, self.is_drop_frame)
    
    def __sub__(self, other: Union['Timecode', int]) -> 'Timecode':
        """减去帧数或时间码"""
        if isinstance(other, Timecode):
            total = self.total_frames - other.total_frames
        else:
            total = self.total_frames - other
        return Timecode.from_frames(max(0, total), self.fps, self.is_drop_frame)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Timecode):
            return self.total_frames == other.total_frames and self.fps == other.fps
        return False
    
    def __lt__(self, other: 'Timecode') -> bool:
        return self.total_frames < other.total_frames
    
    def __le__(self, other: 'Timecode') -> bool:
        return self.total_frames <= other.total_frames
    
    def __gt__(self, other: 'Timecode') -> bool:
        return self.total_frames > other.total_frames
    
    def __ge__(self, other: 'Timecode') -> bool:
        return self.total_frames >= other.total_frames


class FrameConverter:
    """
    帧率转换器
    
    用于在不同帧率之间转换帧数
    """
    
    @staticmethod
    def convert_frames(frames: int, from_fps: Union[FrameRate, Fraction, int, float],
                      to_fps: Union[FrameRate, Fraction, int, float],
                      rounding: str = 'round') -> int:
        """
        将帧数从一个帧率转换为另一个帧率
        
        Args:
            frames: 源帧数
            from_fps: 源帧率
            to_fps: 目标帧率
            rounding: 舍入方式 ('round', 'floor', 'ceil')
            
        Returns:
            目标帧数
        """
        if not isinstance(from_fps, FrameRate):
            from_fps = FrameRate(from_fps)
        if not isinstance(to_fps, FrameRate):
            to_fps = FrameRate(to_fps)
        
        # 先转换为秒
        seconds = from_fps.frames_to_seconds(frames)
        
        # 再从秒转换为目标帧数
        return to_fps.seconds_to_frames(seconds, rounding)
    
    @staticmethod
    def calculate_pull_down(source_fps: Fraction = Fraction(24, 1),
                           target_fps: Fraction = Fraction(30000, 1001)) -> dict:
        """
        计算下拉（pulldown）参数
        
        用于将电影（24fps）转换为电视（29.97fps）
        
        Args:
            source_fps: 源帧率
            target_fps: 目标帧率
            
        Returns:
            包含下拉参数的字典
        """
        source_frame_duration = 1 / float(source_fps)
        target_frame_duration = 1 / float(target_fps)
        
        # 计算需要的重复帧比例
        ratio = float(target_fps) / float(source_fps)
        
        # 3:2 pulldown 常用于 24fps → 29.97fps
        is_32_pulldown = abs(ratio - 1.25) < 0.01  # 30/24 = 1.25
        
        return {
            'source_fps': float(source_fps),
            'target_fps': float(target_fps),
            'ratio': ratio,
            'is_32_pulldown': is_32_pulldown,
            'source_frame_duration_ms': source_frame_duration * 1000,
            'target_frame_duration_ms': target_frame_duration * 1000,
            'description': '3:2 pulldown' if is_32_pulldown else 'Frame rate conversion'
        }
    
    @staticmethod
    def calculate_speed_change(original_fps: Fraction, desired_duration: float) -> dict:
        """
        计算变速播放参数
        
        Args:
            original_fps: 原始帧率
            desired_duration: 期望时长（秒）
            
        Returns:
            包含变速参数的字典
        """
        return {
            'original_fps': float(original_fps),
            'speed_factor': 1.0,
            'new_duration': desired_duration
        }


# ============ 便捷函数 ============

def frames_to_seconds(frames: int, fps: Union[int, float, Fraction] = 30) -> float:
    """
    将帧数转换为秒数
    
    Args:
        frames: 帧数
        fps: 帧率（默认 30fps）
        
    Returns:
        秒数
    """
    frame_rate = FrameRate(fps)
    return frame_rate.frames_to_seconds(frames)


def seconds_to_frames(seconds: float, fps: Union[int, float, Fraction] = 30,
                     rounding: str = 'round') -> int:
    """
    将秒数转换为帧数
    
    Args:
        seconds: 秒数
        fps: 帧率（默认 30fps）
        rounding: 舍入方式
        
    Returns:
        帧数
    """
    frame_rate = FrameRate(fps)
    return frame_rate.seconds_to_frames(seconds, rounding)


def frames_to_timecode(frames: int, fps: Union[int, float, Fraction] = 30,
                       is_drop_frame: bool = False) -> str:
    """
    将帧数转换为时间码字符串
    
    Args:
        frames: 帧数
        fps: 帧率
        is_drop_frame: 是否为 drop-frame
        
    Returns:
        时间码字符串
    """
    tc = Timecode.from_frames(frames, fps, is_drop_frame)
    return str(tc)


def timecode_to_frames(timecode: str, fps: Union[int, float, Fraction] = 30) -> int:
    """
    将时间码字符串转换为帧数
    
    Args:
        timecode: 时间码字符串
        fps: 帧率
        
    Returns:
        帧数
    """
    tc = Timecode.from_string(timecode, fps)
    return tc.total_frames


def timecode_to_seconds(timecode: str, fps: Union[int, float, Fraction] = 30) -> float:
    """
    将时间码字符串转换为秒数
    
    Args:
        timecode: 时间码字符串
        fps: 帧率
        
    Returns:
        秒数
    """
    tc = Timecode.from_string(timecode, fps)
    return tc.total_seconds


def seconds_to_timecode(seconds: float, fps: Union[int, float, Fraction] = 30,
                        is_drop_frame: bool = False) -> str:
    """
    将秒数转换为时间码字符串
    
    Args:
        seconds: 秒数
        fps: 帧率
        is_drop_frame: 是否为 drop-frame
        
    Returns:
        时间码字符串
    """
    tc = Timecode.from_seconds(seconds, fps, is_drop_frame)
    return str(tc)


def convert_frame_rate(frames: int, from_fps: Union[int, float, Fraction],
                      to_fps: Union[int, float, Fraction], rounding: str = 'round') -> int:
    """
    帧率转换
    
    Args:
        frames: 源帧数
        from_fps: 源帧率
        to_fps: 目标帧率
        rounding: 舍入方式
        
    Returns:
        目标帧数
    """
    return FrameConverter.convert_frames(frames, from_fps, to_fps, rounding)


def calculate_drop_frame_count(frames: int, fps: Fraction = Fraction(30000, 1001)) -> int:
    """
    计算 drop-frame 模式下的丢帧数
    
    Args:
        frames: 帧数
        fps: 帧率
        
    Returns:
        丢帧数
    """
    return DropFrameCalculator.calculate_drop_frame_count(frames, fps)


def is_drop_frame_rate(fps: Union[Fraction, FrameRate, int, float]) -> bool:
    """
    判断是否为 drop-frame 帧率
    
    Args:
        fps: 帧率
        
    Returns:
        是否为 drop-frame 帧率
    """
    return DropFrameCalculator.is_drop_frame_rate(fps)