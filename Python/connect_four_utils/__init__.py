"""
Connect Four Game Utilities
A complete Connect Four implementation with AI opponent using minimax algorithm.

Features:
- Game board management (7 columns x 6 rows)
- Move validation and drop mechanics
- Win detection (horizontal, vertical, diagonal)
- AI opponent with minimax and alpha-beta pruning
- Difficulty levels
- Game state serialization
- Score tracking
"""

from .game import ConnectFourGame, create_game, GameStatus
from .board import Board
from .player import Player, HumanPlayer, RandomPlayer
from .ai import AIPlayer, create_ai_player
from .constants import (
    ROWS, COLS, EMPTY, PLAYER_ONE, PLAYER_TWO,
    WINNING_LENGTH, Difficulty
)

__all__ = [
    'ConnectFourGame',
    'create_game',
    'GameStatus',
    'Board',
    'Player',
    'HumanPlayer',
    'RandomPlayer',
    'AIPlayer',
    'create_ai_player',
    'ROWS',
    'COLS',
    'EMPTY',
    'PLAYER_ONE',
    'PLAYER_TWO',
    'WINNING_LENGTH',
    'Difficulty'
]

__version__ = '1.0.0'