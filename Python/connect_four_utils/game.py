"""
Connect Four game management.
"""

from typing import Optional, Tuple, List
from enum import Enum, auto
from dataclasses import dataclass
from .board import Board
from .player import Player, HumanPlayer, RandomPlayer
from .ai import AIPlayer
from .constants import PLAYER_ONE, PLAYER_TWO, Difficulty


class GameStatus(Enum):
    """Game status enumeration."""
    IN_PROGRESS = auto()
    PLAYER_ONE_WINS = auto()
    PLAYER_TWO_WINS = auto()
    DRAW = auto()


@dataclass
class MoveRecord:
    """Record of a single move."""
    player_id: int
    column: int
    row: int
    
    def to_dict(self) -> dict:
        return {
            'player_id': self.player_id,
            'column': self.column,
            'row': self.row
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MoveRecord':
        return cls(data['player_id'], data['column'], data['row'])


class ConnectFourGame:
    """
    Connect Four game manager.
    
    Features:
    - Turn-based gameplay
    - Win/draw detection
    - Move history with undo
    - Game serialization
    - Support for human, random, and AI players
    """
    
    def __init__(
        self,
        player1: Optional[Player] = None,
        player2: Optional[Player] = None
    ):
        """
        Initialize a new game.
        
        Args:
            player1: Player 1 (default: HumanPlayer)
            player2: Player 2 (default: AIPlayer with medium difficulty)
        """
        self._board = Board()
        self._player1 = player1 or HumanPlayer(PLAYER_ONE, "Player 1")
        self._player2 = player2 or AIPlayer(PLAYER_TWO, Difficulty.MEDIUM, "AI")
        self._current_player_id = PLAYER_ONE
        self._move_history: List[MoveRecord] = []
        self._status = GameStatus.IN_PROGRESS
        self._winner: Optional[int] = None
        self._winning_positions: Optional[List[Tuple[int, int]]] = None
    
    @property
    def board(self) -> Board:
        """Get the current board."""
        return self._board
    
    @property
    def current_player_id(self) -> int:
        """Get the current player's ID."""
        return self._current_player_id
    
    @property
    def current_player(self) -> Player:
        """Get the current player object."""
        return self._player1 if self._current_player_id == PLAYER_ONE else self._player2
    
    @property
    def player1(self) -> Player:
        """Get player 1."""
        return self._player1
    
    @property
    def player2(self) -> Player:
        """Get player 2."""
        return self._player2
    
    @property
    def status(self) -> GameStatus:
        """Get the current game status."""
        return self._status
    
    @property
    def winner(self) -> Optional[int]:
        """Get the winner's player ID (None if no winner)."""
        return self._winner
    
    @property
    def winning_positions(self) -> Optional[List[Tuple[int, int]]]:
        """Get the positions of winning pieces."""
        return self._winning_positions
    
    @property
    def move_history(self) -> List[MoveRecord]:
        """Get the move history."""
        return self._move_history.copy()
    
    @property
    def move_count(self) -> int:
        """Get the total number of moves."""
        return len(self._move_history)
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._status != GameStatus.IN_PROGRESS
    
    def get_available_columns(self) -> List[int]:
        """Get columns where a piece can be dropped."""
        return self._board.get_available_columns()
    
    def make_move(self, column: int) -> Tuple[bool, str]:
        """
        Make a move in the specified column.
        
        Args:
            column: Column index (0-6)
            
        Returns:
            Tuple of (success, message)
        """
        if self.is_game_over():
            return False, "Game is already over"
        
        if column not in self._board.get_available_columns():
            return False, f"Invalid move: column {column} is not available"
        
        # Make the move
        row = self._board.drop_piece(column, self._current_player_id)
        
        # Record the move
        self._move_history.append(MoveRecord(self._current_player_id, column, row))
        
        # Check for win
        if self._board.check_win(self._current_player_id):
            self._status = (GameStatus.PLAYER_ONE_WINS 
                          if self._current_player_id == PLAYER_ONE 
                          else GameStatus.PLAYER_TWO_WINS)
            self._winner = self._current_player_id
            self._winning_positions = self._board.get_winning_positions(self._current_player_id)
            return True, f"{self.current_player.name} wins!"
        
        # Check for draw
        if self._board.is_full():
            self._status = GameStatus.DRAW
            return True, "Game is a draw!"
        
        # Switch players
        self._current_player_id = PLAYER_TWO if self._current_player_id == PLAYER_ONE else PLAYER_ONE
        return True, "Move successful"
    
    def get_ai_move(self) -> int:
        """
        Get the AI's move for the current player.
        Only works if current player is an AI player.
        
        Returns:
            Column index for the AI's move
            
        Raises:
            ValueError if current player is not an AI
        """
        if not isinstance(self.current_player, (AIPlayer, RandomPlayer)):
            raise ValueError("Current player is not an AI")
        
        return self.current_player.get_move(self._board)
    
    def play_turn(self, column: Optional[int] = None) -> Tuple[bool, str]:
        """
        Play one turn of the game.
        
        For human players, you must provide a column.
        For AI players, the AI will choose.
        
        Args:
            column: Column index (required for human players)
            
        Returns:
            Tuple of (success, message)
        """
        current = self.current_player
        
        if isinstance(current, (AIPlayer, RandomPlayer)):
            column = current.get_move(self._board)
        
        if column is None:
            return False, "Column is required for human players"
        
        return self.make_move(column)
    
    def undo_last_move(self) -> bool:
        """
        Undo the last move.
        
        Returns:
            True if a move was undone, False if no moves to undo
        """
        if not self._move_history:
            return False
        
        last_move = self._move_history.pop()
        self._board.remove_piece(last_move.row, last_move.column)
        
        # Reset game state
        self._current_player_id = last_move.player_id
        self._status = GameStatus.IN_PROGRESS
        self._winner = None
        self._winning_positions = None
        
        return True
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        self._board = Board()
        self._current_player_id = PLAYER_ONE
        self._move_history = []
        self._status = GameStatus.IN_PROGRESS
        self._winner = None
        self._winning_positions = None
    
    def display(self) -> str:
        """Get a string representation of the current game state."""
        lines = [str(self._board)]
        
        if self.is_game_over():
            if self._status == GameStatus.DRAW:
                lines.append("\nGame Over: Draw!")
            else:
                winner_name = (self._player1.name if self._winner == PLAYER_ONE 
                              else self._player2.name)
                lines.append(f"\nGame Over: {winner_name} wins!")
        else:
            lines.append(f"\n{self.current_player.name}'s turn ({self.current_player.symbol})")
        
        return '\n'.join(lines)
    
    def __str__(self) -> str:
        return self.display()
    
    def serialize(self) -> dict:
        """Serialize the game state to a dictionary."""
        return {
            'board': self._board.serialize(),
            'current_player_id': self._current_player_id,
            'move_history': [m.to_dict() for m in self._move_history],
            'status': self._status.name,
            'winner': self._winner,
            'winning_positions': self._winning_positions
        }
    
    @classmethod
    def deserialize(cls, data: dict) -> 'ConnectFourGame':
        """Deserialize a game state from a dictionary."""
        game = cls()
        game._board = Board.deserialize(data['board'])
        game._current_player_id = data['current_player_id']
        game._move_history = [MoveRecord.from_dict(m) for m in data['move_history']]
        game._status = GameStatus[data['status']]
        game._winner = data.get('winner')
        game._winning_positions = data.get('winning_positions')
        
        # Convert winning positions back to tuples if present
        if game._winning_positions:
            game._winning_positions = [tuple(p) for p in game._winning_positions]
        
        return game
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        import json
        return json.dumps(self.serialize())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ConnectFourGame':
        """Deserialize from JSON string."""
        import json
        return cls.deserialize(json.loads(json_str))


def create_game(
    mode: str = "human_vs_ai",
    difficulty: str = "medium",
    player1_name: Optional[str] = None,
    player2_name: Optional[str] = None
) -> ConnectFourGame:
    """
    Factory function to create a game with specified mode.
    
    Args:
        mode: Game mode - one of:
            - "human_vs_ai": Human player vs AI
            - "human_vs_human": Two human players
            - "ai_vs_ai": Two AI players
            - "ai_vs_random": AI vs random bot
        difficulty: AI difficulty (for AI players)
        player1_name: Optional name for player 1
        player2_name: Optional name for player 2
        
    Returns:
        ConnectFourGame instance
    """
    from .ai import create_ai_player
    
    mode = mode.lower()
    
    if mode == "human_vs_ai":
        p1 = HumanPlayer(PLAYER_ONE, player1_name or "Player 1")
        p2 = create_ai_player(PLAYER_TWO, difficulty, player2_name or "AI")
    elif mode == "human_vs_human":
        p1 = HumanPlayer(PLAYER_ONE, player1_name or "Player 1")
        p2 = HumanPlayer(PLAYER_TWO, player2_name or "Player 2")
    elif mode == "ai_vs_ai":
        p1 = create_ai_player(PLAYER_ONE, difficulty, player1_name or "AI 1")
        p2 = create_ai_player(PLAYER_TWO, difficulty, player2_name or "AI 2")
    elif mode == "ai_vs_random":
        p1 = create_ai_player(PLAYER_ONE, difficulty, player1_name or "AI")
        p2 = RandomPlayer(PLAYER_TWO, player2_name or "Random Bot")
    else:
        raise ValueError(f"Unknown mode: {mode}. "
                        f"Valid modes: human_vs_ai, human_vs_human, ai_vs_ai, ai_vs_random")
    
    return ConnectFourGame(p1, p2)


def quick_game(difficulty: str = "medium", verbose: bool = True) -> int:
    """
    Play a quick game against the AI.
    
    Args:
        difficulty: AI difficulty level
        verbose: Whether to print game progress
        
    Returns:
        Winner: 1 for player 1, 2 for player 2, 0 for draw
    """
    game = create_game("human_vs_ai", difficulty)
    
    if verbose:
        print("Connect Four - Quick Game")
        print("=" * 40)
        print(game.display())
        print()
    
    while not game.is_game_over():
        if isinstance(game.current_player, HumanPlayer):
            # Human player - needs input from external source
            raise RuntimeError("Human player requires external input. "
                             "Use play_turn() with a column number.")
        else:
            # AI player
            column = game.get_ai_move()
            success, msg = game.make_move(column)
            
            if verbose:
                print(f"{game.current_player.name} plays column {column}")
                print(game.display())
                print()
    
    return game.winner or 0