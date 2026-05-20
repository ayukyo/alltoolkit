"""
AI Player implementation using Minimax algorithm with Alpha-Beta pruning.
"""

from typing import Optional, Tuple
from .player import Player
from .board import Board
from .constants import (
    PLAYER_ONE, PLAYER_TWO, EMPTY, ROWS, COLS, WINNING_LENGTH,
    Difficulty, DIFFICULTY_DEPTHS
)


class AIPlayer(Player):
    """
    AI player using Minimax algorithm with Alpha-Beta pruning.
    
    Features:
    - Multiple difficulty levels
    - Position evaluation heuristics
    - Alpha-beta pruning for efficiency
    - Center column preference
    """
    
    def __init__(
        self,
        player_id: int,
        difficulty: Difficulty = Difficulty.MEDIUM,
        name: Optional[str] = None
    ):
        """
        Initialize AI player.
        
        Args:
            player_id: Either PLAYER_ONE (1) or PLAYER_TWO (2)
            difficulty: AI difficulty level
            name: Optional player name
        """
        super().__init__(player_id, name or f"AI ({difficulty.name})")
        self._difficulty = difficulty
        self._depth = DIFFICULTY_DEPTHS[difficulty]
    
    @property
    def difficulty(self) -> Difficulty:
        """Get the AI difficulty level."""
        return self._difficulty
    
    def set_difficulty(self, difficulty: Difficulty) -> None:
        """Set the AI difficulty level."""
        self._difficulty = difficulty
        self._depth = DIFFICULTY_DEPTHS[difficulty]
    
    def get_move(self, board: Board) -> int:
        """
        Get the best move for the current board state.
        
        Args:
            board: Current game board
            
        Returns:
            Best column index (0-6)
        """
        # Handle difficulty EASY separately (random)
        if self._difficulty == Difficulty.EASY:
            return self._get_random_move(board)
        
        # Use minimax for other difficulties
        best_col, _ = self._minimax(
            board, 
            self._depth, 
            float('-inf'), 
            float('inf'), 
            True
        )
        return best_col
    
    def _get_random_move(self, board: Board) -> int:
        """Get a random valid move (for EASY difficulty)."""
        import random
        columns = board.get_available_columns()
        return random.choice(columns)
    
    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool
    ) -> Tuple[int, float]:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current board state
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing player's turn
            
        Returns:
            Tuple of (best_column, score)
        """
        # Check for terminal states
        if board.check_win(self.player_id):
            return (0, 100000 + depth)  # Win bonus with depth preference
        if board.check_win(self.opponent_id):
            return (0, -100000 - depth)  # Loss penalty
        if board.is_full():
            return (0, 0)  # Draw
        
        if depth == 0:
            return (0, self._evaluate_board(board))
        
        available_cols = self._get_ordered_columns(board)
        
        if maximizing:
            max_eval = float('-inf')
            best_col = available_cols[0]
            
            for col in available_cols:
                # Make move
                row = board.drop_piece(col, self.player_id)
                
                # Recurse
                _, eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                
                # Undo move
                board.remove_piece(row, col)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return (best_col, max_eval)
        else:
            min_eval = float('inf')
            best_col = available_cols[0]
            
            for col in available_cols:
                # Make move
                row = board.drop_piece(col, self.opponent_id)
                
                # Recurse
                _, eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                
                # Undo move
                board.remove_piece(row, col)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return (best_col, min_eval)
    
    def _get_ordered_columns(self, board: Board) -> list:
        """
        Get available columns ordered by center preference.
        Center columns are checked first for better pruning.
        """
        available = board.get_available_columns()
        # Order by distance from center (center first)
        center = COLS // 2
        return sorted(available, key=lambda x: abs(x - center))
    
    def _evaluate_board(self, board: Board) -> float:
        """
        Evaluate the board position for this player.
        Higher scores favor this player.
        
        Evaluation considers:
        - Center control
        - Number of potential winning lines
        - Blocking opponent's winning lines
        - Piece patterns (2-in-row, 3-in-row, etc.)
        """
        score = 0.0
        
        # Center column preference
        center_col = COLS // 2
        center_count = sum(1 for row in range(ROWS) 
                          if board.get_cell(row, center_col) == self.player_id)
        score += center_count * 3
        
        # Evaluate all windows (potential winning positions)
        score += self._evaluate_horizontal(board)
        score += self._evaluate_vertical(board)
        score += self._evaluate_diagonals(board)
        
        return score
    
    def _evaluate_horizontal(self, board: Board) -> float:
        """Evaluate horizontal windows."""
        score = 0.0
        for row in range(ROWS):
            for col in range(COLS - 3):
                window = [board.get_cell(row, col + i) for i in range(4)]
                score += self._evaluate_window(window)
        return score
    
    def _evaluate_vertical(self, board: Board) -> float:
        """Evaluate vertical windows."""
        score = 0.0
        for col in range(COLS):
            for row in range(ROWS - 3):
                window = [board.get_cell(row + i, col) for i in range(4)]
                score += self._evaluate_window(window)
        return score
    
    def _evaluate_diagonals(self, board: Board) -> float:
        """Evaluate diagonal windows (both directions)."""
        score = 0.0
        
        # Positive slope diagonals
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board.get_cell(row + i, col + i) for i in range(4)]
                score += self._evaluate_window(window)
        
        # Negative slope diagonals
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                window = [board.get_cell(row - i, col + i) for i in range(4)]
                score += self._evaluate_window(window)
        
        return score
    
    def _evaluate_window(self, window: list) -> float:
        """
        Evaluate a window of 4 cells.
        
        Scoring:
        - 4 in a row: Huge score (should be caught earlier)
        - 3 in a row + 1 empty: Good score
        - 2 in a row + 2 empty: Small score
        - Opponent 3 in a row + 1 empty: Negative (block!)
        """
        my_pieces = window.count(self.player_id)
        opp_pieces = window.count(self.opponent_id)
        empty = window.count(EMPTY)
        
        # My pieces scoring
        if my_pieces == 4:
            return 100.0
        elif my_pieces == 3 and empty == 1:
            return 5.0
        elif my_pieces == 2 and empty == 2:
            return 2.0
        
        # Opponent pieces (blocking)
        if opp_pieces == 3 and empty == 1:
            return -4.0  # Must block!
        
        return 0.0
    
    def __repr__(self) -> str:
        return f"AIPlayer(id={self.player_id}, difficulty={self._difficulty.name})"


def create_ai_player(
    player_id: int,
    difficulty: str = "medium",
    name: Optional[str] = None
) -> AIPlayer:
    """
    Factory function to create AI player with difficulty string.
    
    Args:
        player_id: Player ID (1 or 2)
        difficulty: Difficulty level string (easy/medium/hard/expert)
        name: Optional player name
        
    Returns:
        AIPlayer instance
    """
    difficulty_map = {
        'easy': Difficulty.EASY,
        'medium': Difficulty.MEDIUM,
        'hard': Difficulty.HARD,
        'expert': Difficulty.EXPERT,
    }
    
    diff_key = difficulty.lower()
    if diff_key not in difficulty_map:
        raise ValueError(f"Invalid difficulty: {difficulty}. "
                        f"Valid options: {list(difficulty_map.keys())}")
    
    return AIPlayer(player_id, difficulty_map[diff_key], name)