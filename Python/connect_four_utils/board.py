"""
Connect Four game board implementation.
"""

from typing import List, Optional, Tuple
from copy import deepcopy
from .constants import ROWS, COLS, EMPTY, PLAYER_ONE, PLAYER_TWO, WINNING_LENGTH


class Board:
    """
    Connect Four game board.
    
    The board is represented as a 2D list where:
    - board[row][col] contains the cell value
    - Row 0 is the top, row ROWS-1 is the bottom
    - Column 0 is leftmost, column COLS-1 is rightmost
    """
    
    def __init__(self, grid: Optional[List[List[int]]] = None):
        """Initialize the board."""
        if grid is None:
            self._grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        else:
            self._grid = [row[:] for row in grid]
    
    @property
    def grid(self) -> List[List[int]]:
        """Return a copy of the grid."""
        return [row[:] for row in self._grid]
    
    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        return Board(self._grid)
    
    def get_cell(self, row: int, col: int) -> int:
        """Get the value at a specific cell."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._grid[row][col]
    
    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set the value at a specific cell."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        self._grid[row][col] = value
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within board bounds."""
        return 0 <= row < ROWS and 0 <= col < COLS
    
    def is_column_full(self, col: int) -> bool:
        """Check if a column is full."""
        if not 0 <= col < COLS:
            raise ValueError(f"Invalid column: {col}")
        return self._grid[0][col] != EMPTY
    
    def get_available_columns(self) -> List[int]:
        """Get list of columns that are not full."""
        return [col for col in range(COLS) if not self.is_column_full(col)]
    
    def get_drop_row(self, col: int) -> int:
        """
        Get the row where a piece would land in the given column.
        Returns -1 if column is full.
        """
        if not 0 <= col < COLS:
            return -1
        for row in range(ROWS - 1, -1, -1):
            if self._grid[row][col] == EMPTY:
                return row
        return -1
    
    def drop_piece(self, col: int, player: int) -> int:
        """
        Drop a piece in the specified column.
        Returns the row where the piece landed.
        Raises ValueError if column is full or invalid.
        """
        if not 0 <= col < COLS:
            raise ValueError(f"Invalid column: {col}")
        if self.is_column_full(col):
            raise ValueError(f"Column {col} is full")
        
        row = self.get_drop_row(col)
        self._grid[row][col] = player
        return row
    
    def remove_piece(self, row: int, col: int) -> None:
        """Remove a piece from the board (for AI undoing moves)."""
        if self.is_valid_position(row, col):
            self._grid[row][col] = EMPTY
    
    def check_win(self, player: int) -> bool:
        """Check if the specified player has won."""
        # Check all positions for a winning sequence
        for row in range(ROWS):
            for col in range(COLS):
                if self._grid[row][col] == player:
                    if self._check_win_from_position(row, col, player):
                        return True
        return False
    
    def _check_win_from_position(self, row: int, col: int, player: int) -> bool:
        """Check for a win starting from a specific position."""
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1),  # Diagonal down-left
        ]
        
        for dr, dc in directions:
            count = 1
            # Check in positive direction
            r, c = row + dr, col + dc
            while self.is_valid_position(r, c) and self._grid[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while self.is_valid_position(r, c) and self._grid[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= WINNING_LENGTH:
                return True
        
        return False
    
    def get_winning_positions(self, player: int) -> Optional[List[Tuple[int, int]]]:
        """
        Get the positions of winning pieces for a player.
        Returns None if no win, otherwise list of (row, col) tuples.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self._grid[row][col] == player:
                    positions = self._get_winning_positions_from(row, col, player)
                    if positions:
                        return positions
        return None
    
    def _get_winning_positions_from(self, row: int, col: int, player: int) -> Optional[List[Tuple[int, int]]]:
        """Get winning positions starting from a specific cell."""
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1),  # Diagonal down-left
        ]
        
        for dr, dc in directions:
            positions = [(row, col)]
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while self.is_valid_position(r, c) and self._grid[r][c] == player:
                positions.append((r, c))
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while self.is_valid_position(r, c) and self._grid[r][c] == player:
                positions.append((r, c))
                r -= dr
                c -= dc
            
            if len(positions) >= WINNING_LENGTH:
                return positions[:WINNING_LENGTH]
        
        return None
    
    def is_full(self) -> bool:
        """Check if the board is completely full (draw)."""
        return all(self._grid[0][col] != EMPTY for col in range(COLS))
    
    def is_empty(self) -> bool:
        """Check if the board is completely empty."""
        return all(self._grid[row][col] == EMPTY 
                   for row in range(ROWS) for col in range(COLS))
    
    def count_pieces(self, player: int) -> int:
        """Count the number of pieces for a player."""
        return sum(1 for row in range(ROWS) for col in range(COLS) 
                   if self._grid[row][col] == player)
    
    def get_column_height(self, col: int) -> int:
        """Get the number of pieces in a column."""
        return ROWS - self.get_drop_row(col) - 1 if not self.is_column_full(col) else ROWS
    
    def to_string(self, symbols: Optional[Tuple[str, str, str]] = None) -> str:
        """
        Convert board to string representation.
        
        Args:
            symbols: Tuple of (empty, player1, player2) symbols
                     Default: (' ', '●', '○')
        """
        if symbols is None:
            symbols = ('·', '●', '○')
        
        empty_sym, p1_sym, p2_sym = symbols
        
        lines = []
        for row in range(ROWS):
            line = '|'
            for col in range(COLS):
                cell = self._grid[row][col]
                if cell == EMPTY:
                    line += empty_sym
                elif cell == PLAYER_ONE:
                    line += p1_sym
                else:
                    line += p2_sym
                line += '|'
            lines.append(line)
        
        # Column numbers
        footer = ' ' + ' '.join(str(i) for i in range(COLS)) + ' '
        lines.append(footer)
        
        return '\n'.join(lines)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"Board({self._grid})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            return False
        return self._grid == other._grid
    
    def serialize(self) -> str:
        """Serialize the board state to a string."""
        return ''.join(str(self._grid[row][col]) 
                       for row in range(ROWS) for col in range(COLS))
    
    @classmethod
    def deserialize(cls, data: str) -> 'Board':
        """Deserialize a board state from a string."""
        if len(data) != ROWS * COLS:
            raise ValueError(f"Invalid board data length: {len(data)}")
        
        grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        idx = 0
        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col] = int(data[idx])
                idx += 1
        
        return cls(grid)
    
    def to_dict(self) -> dict:
        """Convert board to dictionary representation."""
        return {
            'rows': ROWS,
            'cols': COLS,
            'grid': self._grid,
            'serialized': self.serialize()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Board':
        """Create board from dictionary representation."""
        return cls(data['grid'])