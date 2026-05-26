"""
Riddle Utilities - 谜语工具库

提供谜语的存储、获取、提示和答案验证功能。
零外部依赖，纯 Python 标准库实现。
"""

from .mod import (
    RiddleManager,
    Riddle,
    Hint,
    RiddleCategory,
    RiddleDifficulty,
    RiddleLanguage,
    RiddleSession,
    RiddleGenerator,
    RiddleQuiz,
    get_random_riddle,
    get_daily_riddle,
    check_riddle_answer,
)

__all__ = [
    "RiddleManager",
    "Riddle",
    "Hint",
    "RiddleCategory",
    "RiddleDifficulty",
    "RiddleLanguage",
    "RiddleSession",
    "RiddleGenerator",
    "RiddleQuiz",
    "get_random_riddle",
    "get_daily_riddle",
    "check_riddle_answer",
]

__version__ = "1.0.0"
__author__ = "AllToolkit"