"""
Word Search Puzzle Generator and Solver
========================================

A comprehensive word search puzzle utility with zero external dependencies.
Generate, solve, and manipulate word search puzzles with customizable options.

Features:
- Generate puzzles from word lists
- Multiple placement strategies (random, optimal)
- Configurable directions (horizontal, vertical, diagonal, reverse)
- Difficulty levels (easy, medium, hard)
- Puzzle solving with word location finding
- Export to various formats (text, grid)
- Random fill characters or custom alphabet
- Seed-based reproducibility for testing

Author: AllToolkit
Date: 2026-05-11
"""

import random
import string
from typing import List, Tuple, Optional, Set, Dict, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from copy import deepcopy


class Direction(Enum):
    """Directions for word placement."""
    HORIZONTAL = auto()          # Left to right
    VERTICAL = auto()            # Top to bottom
    DIAGONAL_DOWN = auto()       # Top-left to bottom-right
    DIAGONAL_UP = auto()         # Bottom-left to top-right
    HORIZONTAL_REVERSE = auto()   # Right to left
    VERTICAL_REVERSE = auto()    # Bottom to top
    DIAGONAL_DOWN_REVERSE = auto()  # Bottom-right to top-left
    DIAGONAL_UP_REVERSE = auto()    # Top-right to bottom-left


@dataclass
class WordPlacement:
    """Represents a placed word in the puzzle."""
    word: str
    start_row: int
    start_col: int
    direction: Direction
    positions: List[Tuple[int, int]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.positions:
            self.positions = self._calculate_positions()
    
    def _calculate_positions(self) -> List[Tuple[int, int]]:
        """Calculate all positions occupied by this word."""
        positions = []
        row, col = self.start_row, self.start_col
        dr, dc = self._get_direction_delta()
        
        for _ in range(len(self.word)):
            positions.append((row, col))
            row += dr
            col += dc
        
        return positions
    
    def _get_direction_delta(self) -> Tuple[int, int]:
        """Get row and column deltas for the direction."""
        deltas = {
            Direction.HORIZONTAL: (0, 1),
            Direction.VERTICAL: (1, 0),
            Direction.DIAGONAL_DOWN: (1, 1),
            Direction.DIAGONAL_UP: (-1, 1),
            Direction.HORIZONTAL_REVERSE: (0, -1),
            Direction.VERTICAL_REVERSE: (-1, 0),
            Direction.DIAGONAL_DOWN_REVERSE: (-1, -1),
            Direction.DIAGONAL_UP_REVERSE: (1, -1),
        }
        return deltas[self.direction]


@dataclass
class PuzzleResult:
    """Result of puzzle generation."""
    grid: List[List[str]]
    words_placed: List[WordPlacement]
    words_not_placed: List[str]
    size: Tuple[int, int]
    
    def get_grid_string(self) -> str:
        """Get the puzzle as a formatted string."""
        lines = []
        for row in self.grid:
            lines.append(' '.join(row))
        return '\n'.join(lines)
    
    def get_solution_string(self) -> str:
        """Get the solution grid with words highlighted."""
        solution = [row[:] for row in self.grid]
        highlight_positions = set()
        
        for placement in self.words_placed:
            for pos in placement.positions:
                highlight_positions.add(pos)
        
        lines = []
        for i, row in enumerate(solution):
            line = []
            for j, char in enumerate(row):
                if (i, j) in highlight_positions:
                    line.append(f'[{char}]')
                else:
                    line.append(f' {char} ')
            lines.append(''.join(line))
        return '\n'.join(lines)


class Difficulty(Enum):
    """Puzzle difficulty levels."""
    EASY = auto()      # Only horizontal and vertical
    MEDIUM = auto()    # Add diagonal directions
    HARD = auto()      # All directions including reverse


class WordSearchGenerator:
    """Generate word search puzzles from word lists."""
    
    # Default directions for each difficulty
    DIFFICULTY_DIRECTIONS = {
        Difficulty.EASY: [
            Direction.HORIZONTAL,
            Direction.VERTICAL,
        ],
        Difficulty.MEDIUM: [
            Direction.HORIZONTAL,
            Direction.VERTICAL,
            Direction.DIAGONAL_DOWN,
            Direction.DIAGONAL_UP,
        ],
        Difficulty.HARD: list(Direction),  # All directions
    }
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.rng = random.Random(seed)
    
    def generate(
        self,
        words: List[str],
        size: Optional[Tuple[int, int]] = None,
        difficulty: Difficulty = Difficulty.MEDIUM,
        directions: Optional[List[Direction]] = None,
        fill_char: str = '',
        alphabet: str = string.ascii_uppercase,
        max_attempts: int = 1000,
        auto_size: bool = True,
        min_size: int = 10,
        max_size: int = 25,
    ) -> PuzzleResult:
        """
        Generate a word search puzzle.
        
        Args:
            words: List of words to place in the puzzle
            size: Grid size as (rows, cols). If None, auto-calculated
            difficulty: Puzzle difficulty level
            directions: Custom list of directions (overrides difficulty)
            fill_char: Character for empty cells (empty string = random fill)
            alphabet: Characters to use for random fill
            max_attempts: Maximum attempts to place each word
            auto_size: Automatically calculate grid size based on words
            min_size: Minimum grid dimension when auto-sizing
            max_size: Maximum grid dimension when auto-sizing
            
        Returns:
            PuzzleResult containing the generated puzzle
        """
        # Normalize words
        words = [self._normalize_word(w) for w in words]
        words = [w for w in words if w]  # Remove empty strings
        
        if not words:
            raise ValueError("No valid words to place")
        
        # Determine directions
        if directions is None:
            directions = self.DIFFICULTY_DIRECTIONS[difficulty]
        
        # Calculate grid size
        if size is None:
            if auto_size:
                size = self._calculate_size(words, min_size, max_size)
            else:
                max_word_len = max(len(w) for w in words)
                size = (max_word_len + 2, max_word_len + 2)
        
        rows, cols = size
        
        # Initialize grid
        grid = [['' for _ in range(cols)] for _ in range(rows)]
        placements: List[WordPlacement] = []
        words_not_placed: List[str] = []
        
        # Sort words by length (longer first for better placement)
        sorted_words = sorted(words, key=len, reverse=True)
        
        for word in sorted_words:
            placed = False
            
            for _ in range(max_attempts):
                direction = self.rng.choice(directions)
                position = self._find_position(grid, word, direction)
                
                if position:
                    row, col = position
                    placement = WordPlacement(word, row, col, direction)
                    
                    if self._can_place(grid, placement):
                        self._place_word(grid, placement)
                        placements.append(placement)
                        placed = True
                        break
            
            if not placed:
                words_not_placed.append(word)
        
        # Fill empty cells
        self._fill_grid(grid, fill_char, alphabet)
        
        return PuzzleResult(
            grid=grid,
            words_placed=placements,
            words_not_placed=words_not_placed,
            size=(rows, cols),
        )
    
    def _normalize_word(self, word: str) -> str:
        """Normalize a word for the puzzle."""
        # Convert to uppercase, remove non-alphabetic characters
        return ''.join(c.upper() for c in word if c.isalpha())
    
    def _calculate_size(
        self, words: List[str], min_size: int, max_size: int
    ) -> Tuple[int, int]:
        """Calculate appropriate grid size for the given words."""
        if not words:
            return (min_size, min_size)
        
        total_chars = sum(len(w) for w in words)
        max_word_len = max(len(w) for w in words)
        word_count = len(words)
        
        # Estimate grid size: total chars should fit with some overlap
        # Aim for about 30-40% fill ratio
        estimated_area = int(total_chars / 0.35)
        side = int(estimated_area ** 0.5)
        side = max(side, max_word_len + 2, min_size)
        side = min(side, max_size)
        
        return (side, side)
    
    def _find_position(
        self, grid: List[List[str]], word: str, direction: Direction
    ) -> Optional[Tuple[int, int]]:
        """Find a valid starting position for a word."""
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        if rows == 0 or cols == 0:
            return None
        
        # Calculate valid starting range
        dr, dc = WordPlacement(word, 0, 0, direction)._get_direction_delta()
        
        # Determine valid start positions based on direction
        if dr > 0:
            min_row, max_row = 0, rows - len(word)
        elif dr < 0:
            min_row, max_row = len(word) - 1, rows - 1
        else:
            min_row, max_row = 0, rows - 1
        
        if dc > 0:
            min_col, max_col = 0, cols - len(word)
        elif dc < 0:
            min_col, max_col = len(word) - 1, cols - 1
        else:
            min_col, max_col = 0, cols - 1
        
        if min_row > max_row or min_col > max_col:
            return None
        
        # Try random positions
        positions = [
            (r, c)
            for r in range(min_row, max_row + 1)
            for c in range(min_col, max_col + 1)
        ]
        self.rng.shuffle(positions)
        
        return positions[0] if positions else None
    
    def _can_place(self, grid: List[List[str]], placement: WordPlacement) -> bool:
        """Check if a word can be placed at its position."""
        rows = len(grid)
        cols = len(grid[0])
        
        for i, (r, c) in enumerate(placement.positions):
            if not (0 <= r < rows and 0 <= c < cols):
                return False
            if grid[r][c] and grid[r][c] != placement.word[i]:
                return False
        
        return True
    
    def _place_word(self, grid: List[List[str]], placement: WordPlacement) -> None:
        """Place a word on the grid."""
        for i, (r, c) in enumerate(placement.positions):
            grid[r][c] = placement.word[i]
    
    def _fill_grid(
        self, grid: List[List[str]], fill_char: str, alphabet: str
    ) -> None:
        """Fill empty cells in the grid."""
        for row in grid:
            for j in range(len(row)):
                if not row[j]:
                    if fill_char:
                        row[j] = fill_char
                    else:
                        row[j] = self.rng.choice(alphabet)


class WordSearchSolver:
    """Solve word search puzzles by finding word locations."""
    
    @staticmethod
    def solve(
        grid: List[List[str]],
        words: List[str],
        directions: Optional[List[Direction]] = None,
    ) -> Tuple[List[WordPlacement], List[str]]:
        """
        Find all words in a puzzle grid.
        
        Args:
            grid: The puzzle grid
            words: Words to find
            directions: Directions to search (default: all)
            
        Returns:
            Tuple of (found placements, not found words)
        """
        if directions is None:
            directions = list(Direction)
        
        found: List[WordPlacement] = []
        not_found: List[str] = []
        
        for word in words:
            word = ''.join(c.upper() for c in word if c.isalpha())
            if not word:
                continue
            
            placement = WordSearchSolver._find_word(grid, word, directions)
            if placement:
                found.append(placement)
            else:
                not_found.append(word)
        
        return found, not_found
    
    @staticmethod
    def _find_word(
        grid: List[List[str]], word: str, directions: List[Direction]
    ) -> Optional[WordPlacement]:
        """Find a specific word in the grid."""
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        if rows == 0 or cols == 0:
            return None
        
        first_char = word[0]
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c].upper() != first_char:
                    continue
                
                for direction in directions:
                    placement = WordPlacement(word, r, c, direction)
                    if WordSearchSolver._check_word(grid, placement):
                        return placement
        
        return None
    
    @staticmethod
    def _check_word(grid: List[List[str]], placement: WordPlacement) -> bool:
        """Check if a word exists at the placement position."""
        rows = len(grid)
        cols = len(grid[0])
        
        for i, (r, c) in enumerate(placement.positions):
            if not (0 <= r < rows and 0 <= c < cols):
                return False
            if grid[r][c].upper() != placement.word[i]:
                return False
        
        return True


class WordSearchUtils:
    """Utility class for word search operations."""
    
    @staticmethod
    def create_empty_grid(rows: int, cols: int, fill: str = ' ') -> List[List[str]]:
        """Create an empty puzzle grid."""
        return [[fill for _ in range(cols)] for _ in range(rows)]
    
    @staticmethod
    def copy_grid(grid: List[List[str]]) -> List[List[str]]:
        """Create a deep copy of a grid."""
        return [row[:] for row in grid]
    
    @staticmethod
    def grid_to_string(grid: List[List[str]], spacing: str = ' ') -> str:
        """Convert grid to string representation."""
        return '\n'.join(spacing.join(row) for row in grid)
    
    @staticmethod
    def string_to_grid(s: str) -> List[List[str]]:
        """Parse a string into a grid."""
        lines = s.strip().split('\n')
        return [[c for c in line.replace(' ', '')] for line in lines if line.strip()]
    
    @staticmethod
    def highlight_words(
        grid: List[List[str]],
        placements: List[WordPlacement],
        highlight_char: str = '*',
    ) -> List[List[str]]:
        """Create a grid with highlighted word positions."""
        result = WordSearchUtils.copy_grid(grid)
        positions = set()
        
        for placement in placements:
            positions.update(placement.positions)
        
        for r, c in positions:
            if 0 <= r < len(result) and 0 <= c < len(result[0]):
                result[r][c] = highlight_char + result[r][c] + highlight_char
        
        return result
    
    @staticmethod
    def get_word_list_from_placement(
        placements: List[WordPlacement],
    ) -> Dict[str, Tuple[int, int, str]]:
        """Get word locations as a dictionary."""
        result = {}
        for p in placements:
            direction_name = p.direction.name
            result[p.word] = (p.start_row, p.start_col, direction_name)
        return result
    
    @staticmethod
    def calculate_fill_ratio(
        grid: List[List[str]], placements: List[WordPlacement]
    ) -> float:
        """Calculate what percentage of grid is covered by words."""
        if not grid:
            return 0.0
        
        total_cells = len(grid) * len(grid[0])
        word_cells = set()
        
        for placement in placements:
            word_cells.update(placement.positions)
        
        return len(word_cells) / total_cells if total_cells > 0 else 0.0
    
    @staticmethod
    def generate_word_hints(
        placements: List[WordPlacement],
        show_direction: bool = True,
        show_position: bool = False,
    ) -> List[str]:
        """Generate hints for finding words."""
        hints = []
        
        for p in placements:
            hint = p.word
            
            if show_direction:
                dir_names = {
                    Direction.HORIZONTAL: "→",
                    Direction.VERTICAL: "↓",
                    Direction.DIAGONAL_DOWN: "↘",
                    Direction.DIAGONAL_UP: "↗",
                    Direction.HORIZONTAL_REVERSE: "←",
                    Direction.VERTICAL_REVERSE: "↑",
                    Direction.DIAGONAL_DOWN_REVERSE: "↖",
                    Direction.DIAGONAL_UP_REVERSE: "↙",
                }
                hint += f" ({dir_names.get(p.direction, '?')})"
            
            if show_position:
                hint += f" [{p.start_row},{p.start_col}]"
            
            hints.append(hint)
        
        return hints


def generate_puzzle(
    words: List[str],
    size: Optional[Tuple[int, int]] = None,
    difficulty: str = "medium",
    seed: Optional[int] = None,
) -> PuzzleResult:
    """
    Convenience function to generate a word search puzzle.
    
    Args:
        words: List of words to include
        size: Grid size as (rows, cols)
        difficulty: "easy", "medium", or "hard"
        seed: Random seed for reproducibility
        
    Returns:
        PuzzleResult with generated puzzle
    """
    difficulty_map = {
        "easy": Difficulty.EASY,
        "medium": Difficulty.MEDIUM,
        "hard": Difficulty.HARD,
    }
    
    diff = difficulty_map.get(difficulty.lower(), Difficulty.MEDIUM)
    generator = WordSearchGenerator(seed=seed)
    
    return generator.generate(words, size=size, difficulty=diff)


def solve_puzzle(
    grid: List[List[str]],
    words: List[str],
) -> Tuple[List[WordPlacement], List[str]]:
    """
    Convenience function to solve a word search puzzle.
    
    Args:
        grid: The puzzle grid
        words: Words to find
        
    Returns:
        Tuple of (found placements, not found words)
    """
    return WordSearchSolver.solve(grid, words)


# Export main classes and functions
__all__ = [
    'Direction',
    'Difficulty',
    'WordPlacement',
    'PuzzleResult',
    'WordSearchGenerator',
    'WordSearchSolver',
    'WordSearchUtils',
    'generate_puzzle',
    'solve_puzzle',
]