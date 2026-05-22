"""
Habit Chain Utils - 习惯链追踪工具

帮助用户追踪习惯形成的链条，支持"不要断链"概念。
"""

from mod import (
    # 核心类
    HabitChain,
    HabitChainManager,
    HabitFrequency,
    
    # 便捷函数
    create_daily_habit,
    create_weekday_habit,
    create_weekend_habit,
    create_custom_habit,
    
    # 工具函数
    calculate_streak_milestone,
    get_chain_health_score,
)

__all__ = [
    "HabitChain",
    "HabitChainManager",
    "HabitFrequency",
    "create_daily_habit",
    "create_weekday_habit",
    "create_weekend_habit",
    "create_custom_habit",
    "calculate_streak_milestone",
    "get_chain_health_score",
]

__version__ = "1.0.0"