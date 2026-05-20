"""
Constants for Connect Four game.
"""

from enum import Enum, auto


# Board dimensions
ROWS = 6
COLS = 7

# Cell values
EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

# Game settings
WINNING_LENGTH = 4  # Number of pieces in a row to win


class Difficulty(Enum):
    """AI difficulty levels."""
    EASY = auto()      # Random moves
    MEDIUM = auto()    # 3-ply minimax
    HARD = auto()      # 5-ply minimax
    EXPERT = auto()    # 7-ply minimax


DIFFICULTY_DEPTHS = {
    Difficulty.EASY: 1,
    Difficulty.MEDIUM: 3,
    Difficulty.HARD: 5,
    Difficulty.EXPERT: 7,
}