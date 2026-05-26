"""
Meditation Timer Utils - 冥想计时器工具

提供冥想计时、呼吸指导和会话记录功能。
"""

from .meditation_timer import (
    # 枚举
    BreathingPattern,
    
    # 数据类
    BreathingPhase,
    BreathingCycle,
    MeditationSession,
    MeditationStats,
    
    # 核心类
    BreathingGuide,
    MeditationTimer,
    SessionRecorder,
    MeditationBell,
    MeditationAssistant,
    
    # 便捷函数
    format_duration,
    quick_meditation,
    guided_breathing,
)

__all__ = [
    "BreathingPattern",
    "BreathingPhase",
    "BreathingCycle",
    "MeditationSession",
    "MeditationStats",
    "BreathingGuide",
    "MeditationTimer",
    "SessionRecorder",
    "MeditationBell",
    "MeditationAssistant",
    "format_duration",
    "quick_meditation",
    "guided_breathing",
]

__version__ = "1.0.0"