"""
Pomodoro Timer Utilities - 番茄钟工具库

功能:
- Pomodoro 计时器管理（工作/短休息/长休息周期）
- 可配置的工作时长、休息时长、长休息间隔
- 会话追踪和统计
- 时间估算
- JSON 序列化/反序列化
- 零外部依赖
"""

import time
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
from dataclasses import dataclass, field


def _parse_iso_datetime(iso_str: str) -> datetime:
    """
    解析 ISO 格式的日期时间字符串（兼容 Python 3.6+）
    
    Args:
        iso_str: ISO 格式字符串 (YYYY-MM-DDTHH:MM:SS 或 YYYY-MM-DDTHH:MM:SS.ffffff)
        
    Returns:
        datetime 对象
    """
    # 处理带微秒的格式
    if '.' in iso_str:
        # 移除可能的时区信息（简化处理）
        iso_str = re.sub(r'[+-]\d{2}:\d{2}$', '', iso_str)
        iso_str = re.sub(r'Z$', '', iso_str)
        main_part, micro_part = iso_str.split('.')
        # 只保留6位微秒
        micro_part = micro_part[:6]
        dt = datetime.strptime(f"{main_part}.{micro_part}", "%Y-%m-%dT%H:%M:%S.%f")
    else:
        # 移除可能的时区信息
        iso_str = re.sub(r'[+-]\d{2}:\d{2}$', '', iso_str)
        iso_str = re.sub(r'Z$', '', iso_str)
        dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S")
    return dt


class TimerState(Enum):
    """计时器状态"""
    IDLE = "idle"           # 空闲
    WORKING = "working"     # 工作中
    SHORT_BREAK = "short_break"   # 短休息
    LONG_BREAK = "long_break"     # 长休息
    PAUSED = "paused"       # 暂停


@dataclass
class PomodoroSession:
    """单个番茄钟会话"""
    start_time: datetime
    end_time: Optional[datetime] = None
    state: TimerState = TimerState.WORKING
    duration_minutes: int = 25
    completed: bool = False
    interrupted: bool = False
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "state": self.state.value,
            "duration_minutes": self.duration_minutes,
            "completed": self.completed,
            "interrupted": self.interrupted,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PomodoroSession":
        """从字典创建"""
        return cls(
            start_time=_parse_iso_datetime(data["start_time"]),
            end_time=_parse_iso_datetime(data["end_time"]) if data.get("end_time") else None,
            state=TimerState(data["state"]),
            duration_minutes=data["duration_minutes"],
            completed=data["completed"],
            interrupted=data["interrupted"],
            notes=data.get("notes", "")
        )


@dataclass
class PomodoroStats:
    """番茄钟统计"""
    total_sessions: int = 0
    completed_sessions: int = 0
    interrupted_sessions: int = 0
    total_work_minutes: int = 0
    total_break_minutes: int = 0
    daily_sessions: Dict[str, int] = field(default_factory=dict)  # 日期 -> 完成数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_sessions": self.total_sessions,
            "completed_sessions": self.completed_sessions,
            "interrupted_sessions": self.interrupted_sessions,
            "total_work_minutes": self.total_work_minutes,
            "total_break_minutes": self.total_break_minutes,
            "daily_sessions": self.daily_sessions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PomodoroStats":
        """从字典创建"""
        return cls(
            total_sessions=data["total_sessions"],
            completed_sessions=data["completed_sessions"],
            interrupted_sessions=data["interrupted_sessions"],
            total_work_minutes=data["total_work_minutes"],
            total_break_minutes=data["total_break_minutes"],
            daily_sessions=data["daily_sessions"]
        )


class PomodoroTimer:
    """
    番茄钟计时器
    
    示例:
        >>> timer = PomodoroTimer()
        >>> timer.start_work()
        >>> # ... 25分钟后
        >>> timer.complete_session()
        >>> stats = timer.get_stats()
    """
    
    # 默认配置
    DEFAULT_WORK_MINUTES = 25
    DEFAULT_SHORT_BREAK_MINUTES = 5
    DEFAULT_LONG_BREAK_MINUTES = 15
    DEFAULT_LONG_BREAK_INTERVAL = 4
    
    def __init__(
        self,
        work_minutes: int = DEFAULT_WORK_MINUTES,
        short_break_minutes: int = DEFAULT_SHORT_BREAK_MINUTES,
        long_break_minutes: int = DEFAULT_LONG_BREAK_MINUTES,
        long_break_interval: int = DEFAULT_LONG_BREAK_INTERVAL,
        auto_start_break: bool = False
    ):
        """
        初始化番茄钟计时器
        
        Args:
            work_minutes: 工作时长（分钟）
            short_break_minutes: 短休息时长（分钟）
            long_break_minutes: 长休息时长（分钟）
            long_break_interval: 长休息间隔（多少个工作周期后）
            auto_start_break: 是否自动开始休息
        """
        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.long_break_interval = long_break_interval
        self.auto_start_break = auto_start_break
        
        self._state = TimerState.IDLE
        self._current_session: Optional[PomodoroSession] = None
        self._completed_work_count = 0
        self._sessions: List[PomodoroSession] = []
        self._stats = PomodoroStats()
        self._start_timestamp: Optional[float] = None
        self._paused_at: Optional[float] = None
        self._total_paused_seconds = 0.0
        self._callbacks: Dict[str, List[Callable]] = {
            "on_start": [],
            "on_complete": [],
            "on_interrupt": [],
            "on_tick": [],
            "on_break_start": [],
            "on_break_end": []
        }
    
    @property
    def state(self) -> TimerState:
        """当前状态"""
        return self._state
    
    @property
    def current_session(self) -> Optional[PomodoroSession]:
        """当前会话"""
        return self._current_session
    
    @property
    def stats(self) -> PomodoroStats:
        """统计信息"""
        return self._stats
    
    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件回调
        
        Args:
            event: 事件名称 (on_start, on_complete, on_interrupt, on_tick, on_break_start, on_break_end)
            callback: 回调函数
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _emit(self, event: str, *args, **kwargs) -> None:
        """触发事件"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception:
                pass
    
    def start_work(self, duration_minutes: Optional[int] = None) -> bool:
        """
        开始工作
        
        Args:
            duration_minutes: 自定义时长（分钟），None 使用默认值
            
        Returns:
            是否成功启动
        """
        if self._state not in (TimerState.IDLE, TimerState.PAUSED):
            return False
        
        duration = duration_minutes or self.work_minutes
        self._current_session = PomodoroSession(
            start_time=datetime.now(),
            state=TimerState.WORKING,
            duration_minutes=duration
        )
        self._state = TimerState.WORKING
        self._start_timestamp = time.time()
        self._total_paused_seconds = 0.0
        
        self._stats.total_sessions += 1
        self._emit("on_start", self._current_session)
        
        return True
    
    def start_break(self, is_long: bool = False) -> bool:
        """
        开始休息
        
        Args:
            is_long: 是否是长休息
            
        Returns:
            是否成功启动
        """
        if self._state not in (TimerState.IDLE, TimerState.PAUSED):
            return False
        
        duration = self.long_break_minutes if is_long else self.short_break_minutes
        state = TimerState.LONG_BREAK if is_long else TimerState.SHORT_BREAK
        
        self._current_session = PomodoroSession(
            start_time=datetime.now(),
            state=state,
            duration_minutes=duration
        )
        self._state = state
        self._start_timestamp = time.time()
        self._total_paused_seconds = 0.0
        
        self._emit("on_break_start", self._current_session)
        
        return True
    
    def pause(self) -> bool:
        """
        暂停计时
        
        Returns:
            是否成功暂停
        """
        if self._state in (TimerState.IDLE, TimerState.PAUSED):
            return False
        
        self._paused_at = time.time()
        self._state = TimerState.PAUSED
        
        return True
    
    def resume(self) -> bool:
        """
        恢复计时
        
        Returns:
            是否成功恢复
        """
        if self._state != TimerState.PAUSED or self._paused_at is None:
            return False
        
        # 累计暂停时间
        self._total_paused_seconds += time.time() - self._paused_at
        self._paused_at = None
        
        # 恢复之前的状态
        if self._current_session:
            self._state = self._current_session.state
        
        return True
    
    def complete_session(self) -> bool:
        """
        完成当前会话
        
        Returns:
            是否成功完成
        """
        if self._state == TimerState.IDLE or self._current_session is None:
            return False
        
        self._current_session.end_time = datetime.now()
        self._current_session.completed = True
        
        # 更新统计
        if self._current_session.state == TimerState.WORKING:
            self._stats.completed_sessions += 1
            self._stats.total_work_minutes += self._current_session.duration_minutes
            self._completed_work_count += 1
            
            # 更新每日统计
            date_key = self._current_session.start_time.strftime("%Y-%m-%d")
            self._stats.daily_sessions[date_key] = self._stats.daily_sessions.get(date_key, 0) + 1
        else:
            self._stats.total_break_minutes += self._current_session.duration_minutes
            self._emit("on_break_end", self._current_session)
        
        self._sessions.append(self._current_session)
        self._emit("on_complete", self._current_session)
        
        # 重置状态
        self._state = TimerState.IDLE
        self._current_session = None
        self._start_timestamp = None
        
        # 自动开始休息
        if self.auto_start_break:
            is_long = self._completed_work_count > 0 and self._completed_work_count % self.long_break_interval == 0
            self.start_break(is_long)
        
        return True
    
    def interrupt_session(self, reason: str = "") -> bool:
        """
        中断当前会话
        
        Args:
            reason: 中断原因
            
        Returns:
            是否成功中断
        """
        if self._state == TimerState.IDLE or self._current_session is None:
            return False
        
        self._current_session.end_time = datetime.now()
        self._current_session.interrupted = True
        self._current_session.notes = reason
        
        # 更新统计
        self._stats.interrupted_sessions += 1
        
        if self._current_session.state == TimerState.WORKING:
            self._stats.total_work_minutes += self.get_elapsed_minutes()
        
        self._sessions.append(self._current_session)
        self._emit("on_interrupt", self._current_session)
        
        # 重置状态
        self._state = TimerState.IDLE
        self._current_session = None
        self._start_timestamp = None
        
        return True
    
    def get_elapsed_seconds(self) -> int:
        """
        获取已过秒数
        
        Returns:
            已过秒数
        """
        if self._start_timestamp is None:
            return 0
        
        elapsed = time.time() - self._start_timestamp - self._total_paused_seconds
        return max(0, int(elapsed))
    
    def get_elapsed_minutes(self) -> int:
        """
        获取已过分钟数
        
        Returns:
            已过分钟数
        """
        return self.get_elapsed_seconds() // 60
    
    def get_remaining_seconds(self) -> int:
        """
        获取剩余秒数
        
        Returns:
            剩余秒数（如果已完成返回0）
        """
        if self._current_session is None:
            return 0
        
        total_seconds = self._current_session.duration_minutes * 60
        elapsed = self.get_elapsed_seconds()
        return max(0, total_seconds - elapsed)
    
    def get_remaining_minutes(self) -> int:
        """
        获取剩余分钟数
        
        Returns:
            剩余分钟数
        """
        return self.get_remaining_seconds() // 60
    
    def get_progress_percent(self) -> float:
        """
        获取进度百分比
        
        Returns:
            进度百分比 (0-100)
        """
        if self._current_session is None:
            return 0.0
        
        total_seconds = self._current_session.duration_minutes * 60
        if total_seconds == 0:
            return 100.0
        
        elapsed = self.get_elapsed_seconds()
        return min(100.0, (elapsed / total_seconds) * 100)
    
    def is_completed(self) -> bool:
        """
        检查当前会话是否完成
        
        Returns:
            是否完成
        """
        if self._current_session is None:
            return False
        
        return self.get_remaining_seconds() == 0
    
    def should_take_long_break(self) -> bool:
        """
        是否应该长休息
        
        Returns:
            是否应该长休息
        """
        return self._completed_work_count > 0 and self._completed_work_count % self.long_break_interval == 0
    
    def reset(self) -> None:
        """重置计时器"""
        self._state = TimerState.IDLE
        self._current_session = None
        self._start_timestamp = None
        self._paused_at = None
        self._total_paused_seconds = 0.0
    
    def reset_all(self) -> None:
        """重置所有数据（包括统计）"""
        self.reset()
        self._completed_work_count = 0
        self._sessions = []
        self._stats = PomodoroStats()
    
    def get_sessions(self, limit: int = 0) -> List[PomodoroSession]:
        """
        获取会话历史
        
        Args:
            limit: 限制数量，0 表示全部
            
        Returns:
            会话列表
        """
        if limit > 0:
            return self._sessions[-limit:]
        return self._sessions.copy()
    
    def get_today_sessions(self) -> List[PomodoroSession]:
        """
        获取今日会话
        
        Returns:
            今日会话列表
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [s for s in self._sessions if s.start_time.strftime("%Y-%m-%d") == today]
    
    def get_today_completed_count(self) -> int:
        """
        获取今日完成的番茄数
        
        Returns:
            今日完成的番茄数
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return self._stats.daily_sessions.get(today, 0)
    
    def estimate_completion_time(self, target_sessions: int) -> datetime:
        """
        估算完成目标时间
        
        Args:
            target_sessions: 目标番茄数
            
        Returns:
            预计完成时间
        """
        remaining = max(0, target_sessions - self._completed_work_count)
        
        # 计算需要的总时间
        total_minutes = remaining * self.work_minutes
        
        # 添加休息时间
        breaks_needed = remaining
        long_breaks = breaks_needed // self.long_break_interval
        short_breaks = breaks_needed - long_breaks
        
        total_minutes += long_breaks * self.long_break_minutes
        total_minutes += short_breaks * self.short_break_minutes
        
        return datetime.now() + timedelta(minutes=total_minutes)
    
    def get_productivity_score(self) -> float:
        """
        获取生产力评分（0-100）
        
        基于完成率、中断率等因素
        
        Returns:
            生产力评分
        """
        if self._stats.total_sessions == 0:
            return 0.0
        
        completion_rate = self._stats.completed_sessions / self._stats.total_sessions
        
        # 中断惩罚
        interruption_penalty = self._stats.interrupted_sessions / self._stats.total_sessions * 0.5
        
        score = completion_rate * 100 * (1 - interruption_penalty)
        return max(0.0, min(100.0, score))
    
    def get_status_text(self) -> str:
        """
        获取状态文本
        
        Returns:
            状态描述文本
        """
        state_texts = {
            TimerState.IDLE: "空闲",
            TimerState.WORKING: "工作中",
            TimerState.SHORT_BREAK: "短休息中",
            TimerState.LONG_BREAK: "长休息中",
            TimerState.PAUSED: "已暂停"
        }
        
        base = state_texts.get(self._state, "未知")
        
        if self._state in (TimerState.WORKING, TimerState.SHORT_BREAK, TimerState.LONG_BREAK, TimerState.PAUSED):
            remaining = self.get_remaining_seconds()
            minutes, seconds = divmod(remaining, 60)
            return f"{base} - 剩余 {minutes:02d}:{seconds:02d}"
        
        return base
    
    def to_json(self) -> str:
        """
        序列化为 JSON
        
        Returns:
            JSON 字符串
        """
        data = {
            "config": {
                "work_minutes": self.work_minutes,
                "short_break_minutes": self.short_break_minutes,
                "long_break_minutes": self.long_break_minutes,
                "long_break_interval": self.long_break_interval,
                "auto_start_break": self.auto_start_break
            },
            "state": self._state.value,
            "completed_work_count": self._completed_work_count,
            "stats": self._stats.to_dict(),
            "sessions": [s.to_dict() for s in self._sessions]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "PomodoroTimer":
        """
        从 JSON 反序列化
        
        Args:
            json_str: JSON 字符串
            
        Returns:
            PomodoroTimer 实例
        """
        data = json.loads(json_str)
        
        timer = cls(
            work_minutes=data["config"]["work_minutes"],
            short_break_minutes=data["config"]["short_break_minutes"],
            long_break_minutes=data["config"]["long_break_minutes"],
            long_break_interval=data["config"]["long_break_interval"],
            auto_start_break=data["config"]["auto_start_break"]
        )
        
        timer._state = TimerState(data["state"])
        timer._completed_work_count = data["completed_work_count"]
        timer._stats = PomodoroStats.from_dict(data["stats"])
        timer._sessions = [PomodoroSession.from_dict(s) for s in data["sessions"]]
        
        return timer


# 便捷函数

def create_timer(
    work_minutes: int = 25,
    short_break: int = 5,
    long_break: int = 15,
    long_break_interval: int = 4
) -> PomodoroTimer:
    """
    创建番茄钟计时器
    
    Args:
        work_minutes: 工作时长
        short_break: 短休息时长
        long_break: 长休息时长
        long_break_interval: 长休息间隔
        
    Returns:
        PomodoroTimer 实例
    """
    return PomodoroTimer(
        work_minutes=work_minutes,
        short_break_minutes=short_break,
        long_break_minutes=long_break,
        long_break_interval=long_break_interval
    )


def format_time(seconds: int) -> str:
    """
    格式化时间
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化字符串 (MM:SS)
    """
    minutes, secs = divmod(max(0, seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def calculate_total_time(
    sessions: int,
    work_minutes: int = 25,
    short_break: int = 5,
    long_break: int = 15,
    long_break_interval: int = 4
) -> int:
    """
    计算完成指定番茄数所需的总时间（分钟）
    
    Args:
        sessions: 番茄数
        work_minutes: 工作时长
        short_break: 短休息时长
        long_break: 长休息时长
        long_break_interval: 长休息间隔
        
    Returns:
        总时间（分钟）
    """
    total = sessions * work_minutes
    
    breaks = sessions
    long_breaks = breaks // long_break_interval
    short_breaks = breaks - long_breaks
    
    total += long_breaks * long_break
    total += short_breaks * short_break
    
    return total


def get_recommended_break(work_count: int, long_break_interval: int = 4) -> str:
    """
    获取推荐的休息类型
    
    Args:
        work_count: 已完成工作数
        long_break_interval: 长休息间隔
        
    Returns:
        推荐的休息类型
    """
    if work_count > 0 and work_count % long_break_interval == 0:
        return "long"
    return "short"


def estimate_daily_goal(
    target_hours: float,
    work_minutes: int = 25
) -> int:
    """
    根据目标工作时间估算每日番茄数
    
    Args:
        target_hours: 目标工作时间（小时）
        work_minutes: 每个番茄的工作时长
        
    Returns:
        推荐的番茄数
    """
    total_minutes = target_hours * 60
    return int(total_minutes / work_minutes)