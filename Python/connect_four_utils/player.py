"""
Player classes for Connect Four.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .constants import PLAYER_ONE, PLAYER_TWO


class Player(ABC):
    """Abstract base class for players."""
    
    def __init__(self, player_id: int, name: Optional[str] = None):
        """
        Initialize a player.
        
        Args:
            player_id: Either PLAYER_ONE (1) or PLAYER_TWO (2)
            name: Optional player name
        """
        if player_id not in (PLAYER_ONE, PLAYER_TWO):
            raise ValueError(f"player_id must be {PLAYER_ONE} or {PLAYER_TWO}")
        
        self._player_id = player_id
        self._name = name or f"Player {player_id}"
    
    @property
    def player_id(self) -> int:
        """Get the player ID (1 or 2)."""
        return self._player_id
    
    @property
    def name(self) -> str:
        """Get the player name."""
        return self._name
    
    @property
    def symbol(self) -> str:
        """Get the player symbol for display."""
        return '●' if self._player_id == PLAYER_ONE else '○'
    
    @property
    def opponent_id(self) -> int:
        """Get the opponent's player ID."""
        return PLAYER_TWO if self._player_id == PLAYER_ONE else PLAYER_ONE
    
    @abstractmethod
    def get_move(self, board) -> int:
        """
        Get the column for the next move.
        
        Args:
            board: Current game board
            
        Returns:
            Column index (0-6)
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._player_id}, name='{self._name}')"


class HumanPlayer(Player):
    """Human player that takes input externally."""
    
    def __init__(self, player_id: int, name: Optional[str] = None):
        super().__init__(player_id, name)
        self._next_move: Optional[int] = None
    
    def set_move(self, column: int) -> None:
        """
        Set the next move (called externally).
        
        Args:
            column: Column index (0-6)
        """
        self._next_move = column
    
    def get_move(self, board) -> int:
        """
        Get the previously set move.
        
        Raises:
            ValueError if no move has been set
        """
        if self._next_move is None:
            raise ValueError("No move set. Call set_move() first.")
        
        move = self._next_move
        self._next_move = None  # Clear after use
        return move
    
    def is_ready(self) -> bool:
        """Check if a move has been set."""
        return self._next_move is not None


class RandomPlayer(Player):
    """Player that makes random valid moves."""
    
    def __init__(self, player_id: int, name: Optional[str] = None):
        super().__init__(player_id, name or "Random Bot")
    
    def get_move(self, board) -> int:
        """Get a random valid column."""
        import random
        columns = board.get_available_columns()
        if not columns:
            raise ValueError("No valid moves available")
        return random.choice(columns)