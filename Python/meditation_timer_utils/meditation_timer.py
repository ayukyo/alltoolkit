"""
Meditation Timer Utils - 冥想计时器工具

功能：
1. 冥想计时器 - 支持开始、暂停、继续、停止
2. 呼吸模式指导 - 多种呼吸练习（4-7-8、箱式呼吸等）
3. 会话记录 - 记录冥想历史
4. 统计分析 - 总时长、连续天数、平均时长等

零外部依赖，纯 Python 标准库实现。
"""

import time
import threading
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Callable, Dict, Any
from enum import Enum
import math


class BreathingPattern(Enum):
    """呼吸模式枚举"""
    RELAXING_4_7_8 = "4-7-8 放松呼吸"  # 吸4秒-屏7秒-呼8秒
    BOX_BREATHING = "箱式呼吸"  # 吸4秒-屏4秒-呼4秒-屏4秒
    CALMING_4_6 = "镇静呼吸"  # 吸4秒-呼6秒
    ENERGIZING = "激发呼吸"  # 快速吸呼
    DEEP_RELAXATION = "深度放松"  # 吸6秒-屏2秒-呼7秒-屏2秒
    EQUAL_BREATHING = "平衡呼吸"  # 吸5秒-呼5秒
    CUSTOM = "自定义"


@dataclass
class BreathingPhase:
    """呼吸阶段"""
    name: str  # inhale, hold, exhale
    duration: float  # 秒
    instruction: str  # 指导语


@dataclass
class BreathingCycle:
    """呼吸循环定义"""
    pattern_name: str
    phases: List[BreathingPhase]
    cycles_per_minute: float = 4.0  # 每分钟循环次数

    def get_total_duration(self) -> float:
        """获取一个循环的总时长"""
        return sum(phase.duration for phase in self.phases)


@dataclass
class MeditationSession:
    """冥想会话记录"""
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: float = 0.0
    breathing_pattern: Optional[str] = None
    completed: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MeditationSession':
        return cls(**data)


@dataclass
class MeditationStats:
    """冥想统计"""
    total_sessions: int = 0
    total_minutes: float = 0.0
    completed_sessions: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    average_session_minutes: float = 0.0
    last_session_date: Optional[str] = None


class BreathingGuide:
    """呼吸指导器"""
    
    # 预定义的呼吸模式
    PATTERNS: Dict[BreathingPattern, BreathingCycle] = {
        BreathingPattern.RELAXING_4_7_8: BreathingCycle(
            pattern_name="4-7-8 放松呼吸",
            phases=[
                BreathingPhase("inhale", 4.0, "吸气..."),
                BreathingPhase("hold", 7.0, "屏息..."),
                BreathingPhase("exhale", 8.0, "呼气..."),
            ]
        ),
        BreathingPattern.BOX_BREATHING: BreathingCycle(
            pattern_name="箱式呼吸",
            phases=[
                BreathingPhase("inhale", 4.0, "吸气..."),
                BreathingPhase("hold", 4.0, "屏息..."),
                BreathingPhase("exhale", 4.0, "呼气..."),
                BreathingPhase("hold", 4.0, "屏息..."),
            ]
        ),
        BreathingPattern.CALMING_4_6: BreathingCycle(
            pattern_name="镇静呼吸",
            phases=[
                BreathingPhase("inhale", 4.0, "吸气..."),
                BreathingPhase("exhale", 6.0, "呼气..."),
            ]
        ),
        BreathingPattern.ENERGIZING: BreathingCycle(
            pattern_name="激发呼吸",
            phases=[
                BreathingPhase("inhale", 1.5, "快速吸气..."),
                BreathingPhase("exhale", 1.5, "快速呼气..."),
            ]
        ),
        BreathingPattern.DEEP_RELAXATION: BreathingCycle(
            pattern_name="深度放松",
            phases=[
                BreathingPhase("inhale", 6.0, "深吸气..."),
                BreathingPhase("hold", 2.0, "屏息..."),
                BreathingPhase("exhale", 7.0, "缓慢呼气..."),
                BreathingPhase("hold", 2.0, "屏息..."),
            ]
        ),
        BreathingPattern.EQUAL_BREATHING: BreathingCycle(
            pattern_name="平衡呼吸",
            phases=[
                BreathingPhase("inhale", 5.0, "吸气..."),
                BreathingPhase("exhale", 5.0, "呼气..."),
            ]
        ),
    }
    
    def __init__(self, pattern: BreathingPattern = BreathingPattern.BOX_BREATHING):
        self.pattern = pattern
        self.cycle = self.PATTERNS.get(pattern)
        self._is_running = False
        self._callback: Optional[Callable[[str, float, str], None]] = None
        self._thread: Optional[threading.Thread] = None
    
    def set_pattern(self, pattern: BreathingPattern) -> None:
        """设置呼吸模式"""
        self.pattern = pattern
        self.cycle = self.PATTERNS.get(pattern)
    
    def get_available_patterns(self) -> List[Dict[str, Any]]:
        """获取所有可用的呼吸模式"""
        result = []
        for pattern_type, cycle in self.PATTERNS.items():
            result.append({
                "type": pattern_type.value,
                "total_duration": cycle.get_total_duration(),
                "phases": [{"name": p.name, "duration": p.duration} for p in cycle.phases]
            })
        return result
    
    def _run_cycle(self, duration: float, callback: Optional[Callable[[str, float, str], None]] = None) -> None:
        """运行呼吸循环"""
        if not self.cycle:
            return
        
        start_time = time.time()
        elapsed = 0.0
        
        while elapsed < duration and self._is_running:
            # 执行一个完整的呼吸循环
            for phase in self.cycle.phases:
                if not self._is_running:
                    break
                
                phase_start = time.time()
                phase_elapsed = 0.0
                
                if callback:
                    callback(phase.name, phase.duration, phase.instruction)
                
                # 等待当前阶段完成
                while phase_elapsed < phase.duration and self._is_running:
                    sleep_time = min(0.1, phase.duration - phase_elapsed)
                    time.sleep(sleep_time)
                    phase_elapsed = time.time() - phase_start
            
            elapsed = time.time() - start_time
    
    def start(self, duration_minutes: float, 
              callback: Optional[Callable[[str, float, str], None]] = None) -> None:
        """开始呼吸指导"""
        self._is_running = True
        self._callback = callback
        duration_seconds = duration_minutes * 60
        self._thread = threading.Thread(target=self._run_cycle, args=(duration_seconds, callback))
        self._thread.daemon = True
        self._thread.start()
    
    def stop(self) -> None:
        """停止呼吸指导"""
        self._is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def is_running(self) -> bool:
        """检查是否正在运行"""
        return self._is_running


class MeditationTimer:
    """冥想计时器"""
    
    def __init__(self, duration_minutes: float = 10.0):
        self.duration_minutes = duration_minutes
        self.duration_seconds = duration_minutes * 60
        self._start_time: Optional[float] = None
        self._elapsed: float = 0.0
        self._is_running = False
        self._is_paused = False
        self._session: Optional[MeditationSession] = None
        self._on_tick: Optional[Callable[[float, float], None]] = None
        self._on_complete: Optional[Callable[[], None]] = None
        self._tick_thread: Optional[threading.Thread] = None
    
    def set_duration(self, minutes: float) -> None:
        """设置冥想时长（分钟）"""
        if self._is_running:
            raise RuntimeError("无法在运行时修改时长")
        self.duration_minutes = minutes
        self.duration_seconds = minutes * 60
    
    def set_callbacks(self, on_tick: Optional[Callable[[float, float], None]] = None,
                      on_complete: Optional[Callable[[], None]] = None) -> None:
        """设置回调函数"""
        self._on_tick = on_tick
        self._on_complete = on_complete
    
    def _tick_loop(self) -> None:
        """计时循环"""
        while self._is_running:
            if not self._is_paused:
                self._elapsed = time.time() - self._start_time
                
                if self._on_tick:
                    remaining = max(0, self.duration_seconds - self._elapsed)
                    self._on_tick(self._elapsed, remaining)
                
                if self._elapsed >= self.duration_seconds:
                    self._complete()
                    break
            
            time.sleep(0.1)
    
    def start(self, breathing_pattern: Optional[BreathingPattern] = None) -> MeditationSession:
        """开始冥想"""
        if self._is_running:
            raise RuntimeError("计时器已在运行")
        
        self._start_time = time.time()
        self._elapsed = 0.0
        self._is_running = True
        self._is_paused = False
        
        self._session = MeditationSession(
            start_time=datetime.now().isoformat(),
            breathing_pattern=breathing_pattern.value if breathing_pattern else None
        )
        
        # 启动计时线程
        self._tick_thread = threading.Thread(target=self._tick_loop)
        self._tick_thread.daemon = True
        self._tick_thread.start()
        
        return self._session
    
    def pause(self) -> None:
        """暂停冥想"""
        if not self._is_running:
            raise RuntimeError("计时器未在运行")
        self._is_paused = True
    
    def resume(self) -> None:
        """继续冥想"""
        if not self._is_running or not self._is_paused:
            raise RuntimeError("无法继续")
        self._is_paused = False
        # 调整开始时间以补偿暂停的时间
        self._start_time = time.time() - self._elapsed
    
    def stop(self, completed: bool = False, notes: str = "") -> MeditationSession:
        """停止冥想"""
        if not self._is_running:
            raise RuntimeError("计时器未在运行")
        
        self._is_running = False
        self._is_paused = False
        
        if self._tick_thread:
            self._tick_thread.join(timeout=1.0)
        
        if self._session:
            self._session.end_time = datetime.now().isoformat()
            self._session.duration_seconds = round(self._elapsed, 2)
            self._session.completed = completed
            self._session.notes = notes
        
        return self._session
    
    def _complete(self) -> None:
        """冥想完成"""
        self._is_running = False
        
        if self._session:
            self._session.end_time = datetime.now().isoformat()
            self._session.duration_seconds = round(self.duration_seconds, 2)
            self._session.completed = True
        
        if self._on_complete:
            self._on_complete()
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "is_running": self._is_running,
            "is_paused": self._is_paused,
            "elapsed_seconds": round(self._elapsed, 2) if self._is_running else 0,
            "remaining_seconds": round(max(0, self.duration_seconds - self._elapsed), 2) if self._is_running else self.duration_seconds,
            "progress_percent": round(min(100, (self._elapsed / self.duration_seconds) * 100), 2) if self._is_running else 0
        }
    
    def is_running(self) -> bool:
        """检查是否正在运行"""
        return self._is_running
    
    def is_paused(self) -> bool:
        """检查是否已暂停"""
        return self._is_paused


class SessionRecorder:
    """冥想会话记录器"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "meditation_sessions.json"
        )
        self._sessions: List[MeditationSession] = []
        self._load_sessions()
    
    def _load_sessions(self) -> None:
        """从文件加载会话记录"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._sessions = [MeditationSession.from_dict(s) for s in data]
            except (json.JSONDecodeError, KeyError):
                self._sessions = []
    
    def _save_sessions(self) -> None:
        """保存会话记录到文件"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self._sessions], f, ensure_ascii=False, indent=2)
    
    def record_session(self, session: MeditationSession) -> None:
        """记录一次冥想会话"""
        self._sessions.append(session)
        self._save_sessions()
    
    def get_sessions(self, limit: Optional[int] = None) -> List[MeditationSession]:
        """获取会话记录"""
        sessions = sorted(self._sessions, key=lambda s: s.start_time, reverse=True)
        return sessions[:limit] if limit else sessions
    
    def get_stats(self) -> MeditationStats:
        """获取冥想统计"""
        if not self._sessions:
            return MeditationStats()
        
        total_sessions = len(self._sessions)
        completed_sessions = sum(1 for s in self._sessions if s.completed)
        total_minutes = sum(s.duration_seconds for s in self._sessions) / 60
        avg_minutes = total_minutes / total_sessions if total_sessions > 0 else 0
        
        # 计算连续天数
        dates = sorted(set(s.start_time[:10] for s in self._sessions), reverse=True)
        current_streak = 0
        longest_streak = 0
        today = datetime.now().date()
        
        if dates:
            # 计算最长连续天数
            temp_streak = 1
            for i in range(1, len(dates)):
                prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
                curr_date = datetime.strptime(dates[i], "%Y-%m-%d").date()
                if (prev_date - curr_date).days == 1:
                    temp_streak += 1
                else:
                    temp_streak = 1
                longest_streak = max(longest_streak, temp_streak)
            longest_streak = max(longest_streak, temp_streak)
            
            # 计算当前连续天数
            for i, date_str in enumerate(dates):
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if i == 0:
                    days_diff = (today - date).days
                    if days_diff <= 1:  # 今天或昨天
                        current_streak = 1
                    else:
                        break
                else:
                    prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
                    if (prev_date - date).days == 1:
                        current_streak += 1
                    else:
                        break
        
        return MeditationStats(
            total_sessions=total_sessions,
            total_minutes=round(total_minutes, 2),
            completed_sessions=completed_sessions,
            current_streak=current_streak,
            longest_streak=longest_streak,
            average_session_minutes=round(avg_minutes, 2),
            last_session_date=dates[0] if dates else None
        )
    
    def clear_sessions(self) -> None:
        """清空所有会话记录"""
        self._sessions = []
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)


class MeditationBell:
    """冥想铃声生成器"""
    
    @staticmethod
    def generate_bell_sound(frequency: float = 432.0, duration: float = 2.0, 
                           sample_rate: int = 44100) -> List[int]:
        """
        生成冥想铃声的音频样本
        
        参数:
            frequency: 基频（Hz），默认432Hz（被认为有治愈效果）
            duration: 持续时间（秒）
            sample_rate: 采样率
        
        返回:
            16位有符号整数音频样本列表
        """
        samples = []
        total_samples = int(duration * sample_rate)
        
        for i in range(total_samples):
            t = i / sample_rate
            
            # 组合多个谐波，创建铃声效果
            # 主频率
            sample = math.sin(2 * math.pi * frequency * t)
            # 二次谐波
            sample += 0.5 * math.sin(2 * math.pi * frequency * 2 * t)
            # 三次谐波
            sample += 0.25 * math.sin(2 * math.pi * frequency * 3 * t)
            
            # 指数衰减
            decay = math.exp(-t * 1.5)
            sample *= decay
            
            # 归一化到16位范围 - 确保不超过最大值
            # 总振幅为 1 + 0.5 + 0.25 = 1.75，所以归一化系数为 1/1.75 * 0.8 = 0.457
            max_amplitude = 1.75  # 主频 + 二次谐波 + 三次谐波的最大叠加
            normalization = 0.8 / max_amplitude  # 确保不会溢出
            sample = int(sample * 32767 * normalization)
            # 确保在范围内
            sample = max(-32767, min(32767, sample))
            samples.append(sample)
        
        return samples
    
    @staticmethod
    def to_wav_bytes(samples: List[int], sample_rate: int = 44100) -> bytes:
        """
        将音频样本转换为WAV格式字节
        
        参数:
            samples: 16位有符号整数音频样本
            sample_rate: 采样率
        
        返回:
            WAV格式的字节串
        """
        import struct
        
        # WAV头部
        num_samples = len(samples)
        num_channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        data_size = num_samples * block_align
        
        # 构建WAV文件
        wav = bytearray()
        
        # RIFF头
        wav.extend(b'RIFF')
        wav.extend(struct.pack('<I', 36 + data_size))  # 文件大小 - 8
        wav.extend(b'WAVE')
        
        # fmt子块
        wav.extend(b'fmt ')
        wav.extend(struct.pack('<I', 16))  # fmt块大小
        wav.extend(struct.pack('<H', 1))   # 音频格式 (1 = PCM)
        wav.extend(struct.pack('<H', num_channels))
        wav.extend(struct.pack('<I', sample_rate))
        wav.extend(struct.pack('<I', byte_rate))
        wav.extend(struct.pack('<H', block_align))
        wav.extend(struct.pack('<H', bits_per_sample))
        
        # data子块
        wav.extend(b'data')
        wav.extend(struct.pack('<I', data_size))
        
        # 音频数据
        for sample in samples:
            wav.extend(struct.pack('<h', sample))
        
        return bytes(wav)


class MeditationAssistant:
    """冥想助手 - 主入口类"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.timer = MeditationTimer()
        self.breathing_guide = BreathingGuide()
        self.recorder = SessionRecorder(storage_path)
        self._bell_enabled = True
    
    def set_timer_duration(self, minutes: float) -> None:
        """设置冥想时长"""
        self.timer.set_duration(minutes)
    
    def start_meditation(self, duration_minutes: Optional[float] = None,
                         breathing_pattern: Optional[BreathingPattern] = None) -> MeditationSession:
        """
        开始冥想会话
        
        参数:
            duration_minutes: 冥想时长（分钟），None则使用已设置的时长
            breathing_pattern: 呼吸模式，None则无呼吸指导
        
        返回:
            MeditationSession 对象
        """
        if duration_minutes:
            self.timer.set_duration(duration_minutes)
        
        return self.timer.start(breathing_pattern)
    
    def pause_meditation(self) -> None:
        """暂停冥想"""
        self.timer.pause()
    
    def resume_meditation(self) -> None:
        """继续冥想"""
        self.timer.resume()
    
    def end_meditation(self, completed: bool = False, notes: str = "") -> MeditationSession:
        """
        结束冥想会话
        
        参数:
            completed: 是否完成
            notes: 备注
        
        返回:
            MeditationSession 对象
        """
        session = self.timer.stop(completed, notes)
        self.recorder.record_session(session)
        return session
    
    def start_breathing_guide(self, pattern: BreathingPattern, 
                               duration_minutes: float,
                               callback: Optional[Callable[[str, float, str], None]] = None) -> None:
        """
        开始呼吸指导
        
        参数:
            pattern: 呼吸模式
            duration_minutes: 持续时间（分钟）
            callback: 回调函数，参数为(阶段名, 阶段时长, 指导语)
        """
        self.breathing_guide.set_pattern(pattern)
        self.breathing_guide.start(duration_minutes, callback)
    
    def stop_breathing_guide(self) -> None:
        """停止呼吸指导"""
        self.breathing_guide.stop()
    
    def get_breathing_patterns(self) -> List[Dict[str, Any]]:
        """获取所有可用的呼吸模式"""
        return self.breathing_guide.get_available_patterns()
    
    def get_stats(self) -> MeditationStats:
        """获取冥想统计"""
        return self.recorder.get_stats()
    
    def get_session_history(self, limit: int = 10) -> List[MeditationSession]:
        """获取冥想历史记录"""
        return self.recorder.get_sessions(limit)
    
    def get_current_status(self) -> Dict[str, Any]:
        """获取当前冥想状态"""
        return self.timer.get_status()
    
    @staticmethod
    def generate_bell_wav(frequency: float = 432.0, duration: float = 2.0) -> bytes:
        """
        生成冥想铃声WAV文件
        
        参数:
            frequency: 基频（Hz）
            duration: 持续时间（秒）
        
        返回:
            WAV格式的字节串
        """
        samples = MeditationBell.generate_bell_sound(frequency, duration)
        return MeditationBell.to_wav_bytes(samples)


def format_duration(seconds: float) -> str:
    """
    格式化时长为人类可读格式
    
    参数:
        seconds: 秒数
    
    返回:
        格式化的时长字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}分{secs}秒" if secs > 0 else f"{minutes}分钟"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}小时{minutes}分钟" if minutes > 0 else f"{hours}小时"


def print_breathing_guide(phase: str, duration: float, instruction: str) -> None:
    """打印呼吸指导信息（用于命令行演示）"""
    bar_length = 30
    filled = int(bar_length * (duration / 8))  # 归一化显示
    
    phase_emoji = {
        "inhale": "🌬️ 吸气",
        "hold": "⏸️ 屏息",
        "exhale": "💨 呼气"
    }
    
    print(f"\r{phase_emoji.get(phase, phase)} {instruction} [{duration:.1f}s] {'█' * filled}{'░' * (bar_length - filled)}", end="", flush=True)


# 便捷函数
def quick_meditation(minutes: float = 5) -> Dict[str, Any]:
    """
    快速冥想（阻塞式）
    
    参数:
        minutes: 冥想时长（分钟）
    
    返回:
        冥想结果字典
    """
    assistant = MeditationAssistant()
    assistant.start_meditation(duration_minutes=minutes)
    
    print(f"🧘 开始 {minutes} 分钟冥想...")
    
    try:
        while assistant.timer.is_running():
            status = assistant.get_current_status()
            elapsed = status["elapsed_seconds"]
            remaining = status["remaining_seconds"]
            progress = status["progress_percent"]
            
            bar_length = 30
            filled = int(bar_length * progress / 100)
            print(f"\r⏱️ [{elapsed:.0f}s] {'█' * filled}{'░' * (bar_length - filled)} {progress:.1f}%", end="", flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n⏹️ 冥想已中断")
        session = assistant.end_meditation(completed=False, notes="用户中断")
        return {"status": "interrupted", "session": session.to_dict()}
    
    print("\n\n✨ 冥想完成！")
    session = assistant.end_meditation(completed=True)
    return {"status": "completed", "session": session.to_dict()}


def guided_breathing(pattern: BreathingPattern = BreathingPattern.BOX_BREATHING,
                    cycles: int = 5) -> Dict[str, Any]:
    """
    引导式呼吸练习（阻塞式）
    
    参数:
        pattern: 呼吸模式
        cycles: 呼吸循环次数
    
    返回:
        练习结果字典
    """
    assistant = MeditationAssistant()
    guide = BreathingGuide(pattern)
    cycle_duration = guide.cycle.get_total_duration() if guide.cycle else 10
    total_duration = (cycle_duration * cycles) / 60  # 转换为分钟
    
    print(f"🌬️ 开始 {pattern.value} 练习...")
    print(f"   共 {cycles} 个循环，预计 {format_duration(cycle_duration * cycles)}\n")
    
    completed_cycles = [0]  # 使用列表以便在回调中修改
    
    def on_phase(phase: str, duration: float, instruction: str):
        if phase == "inhale" and completed_cycles[0] > 0:
            print()  # 新循环换行
        print_breathing_guide(phase, duration, instruction)
        if phase == guide.cycle.phases[-1].name if guide.cycle else None:
            completed_cycles[0] += 1
    
    guide.start(total_duration, on_phase)
    
    try:
        while guide.is_running():
            time.sleep(0.1)
    except KeyboardInterrupt:
        guide.stop()
        print("\n\n⏹️ 练习已中断")
        return {"status": "interrupted", "cycles_completed": completed_cycles[0]}
    
    print(f"\n\n✨ 练习完成！共完成 {completed_cycles[0]} 个循环")
    return {"status": "completed", "cycles_completed": completed_cycles[0]}


if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("🧘 冥想计时器工具演示")
    print("=" * 60)
    
    # 1. 显示可用呼吸模式
    print("\n📋 可用呼吸模式:")
    assistant = MeditationAssistant()
    for pattern in assistant.get_breathing_patterns():
        print(f"   • {pattern['type']}: {pattern['total_duration']:.1f}秒/循环")
    
    # 2. 引导式呼吸练习
    print("\n" + "=" * 60)
    print("🌬️ 引导式呼吸练习演示 (箱式呼吸)")
    print("=" * 60)
    
    result = guided_breathing(BreathingPattern.BOX_BREATHING, cycles=2)
    print(f"\n练习结果: {result}")
    
    # 3. 显示统计
    print("\n" + "=" * 60)
    print("📊 冥想统计")
    print("=" * 60)
    
    stats = assistant.get_stats()
    print(f"   总会话数: {stats.total_sessions}")
    print(f"   总时长: {format_duration(stats.total_minutes * 60)}")
    print(f"   完成会话: {stats.completed_sessions}")
    print(f"   当前连续: {stats.current_streak} 天")
    print(f"   最长连续: {stats.longest_streak} 天")
    
    # 4. 生成铃声
    print("\n" + "=" * 60)
    print("🔔 生成冥想铃声")
    print("=" * 60)
    
    wav_data = MeditationAssistant.generate_bell_wav(frequency=432.0, duration=2.0)
    print(f"   已生成铃声: {len(wav_data)} 字节 (432Hz, 2秒)")
    
    print("\n✨ 演示完成！")