"""
sudoku_utils - Sudoku puzzle utilities

Provides comprehensive sudoku puzzle operations including solving, generating,
validating, and analyzing difficulty. Pure Python implementation with zero
external dependencies.

Features:
- Solve sudoku puzzles (backtracking algorithm)
- Generate new puzzles with configurable difficulty
- Validate puzzle solutions
- Analyze puzzle difficulty
- Get hints for next move
- Pretty print and format utilities
"""

import random
import copy
from typing import List, Optional, Tuple, Set, Generator
from enum import Enum


class SudokuError(Exception):
    """Base exception for sudoku errors."""
    pass


class InvalidPuzzleError(SudokuError):
    """Raised when puzzle is invalid or unsolvable."""
    pass


class Difficulty(Enum):
    """Sudoku difficulty levels based on given cell count."""
    EASY = "easy"        # 36-45 given cells
    MEDIUM = "medium"    # 27-35 given cells
    HARD = "hard"        # 22-26 given cells
    EXPERT = "expert"    # 17-21 given cells
    EVIL = "evil"       # < 17 given cells (may have multiple solutions)


class SudokuGrid:
    """
    A 9x9 Sudoku grid representation.
    
    Supports:
    - Cell access via grid[row][col] or grid.get(row, col)
    - Row, column, and box iteration
    - Deep copying
    - String representation
    """
    
    def __init__(self, grid: Optional[List[List[int]]] = None):
        """
        Initialize sudoku grid.
        
        Args:
            grid: 9x9 grid (0 or empty for unfilled cells). If None, creates empty grid.
        """
        if grid is None:
            self._grid = [[0 for _ in range(9)] for _ in range(9)]
        else:
            if len(grid) != 9 or any(len(row) != 9 for row in grid):
                raise ValueError("Grid must be 9x9")
            self._grid = [row[:] for row in grid]  # Deep copy
    
    def __getitem__(self, row: int) -> List[int]:
        return self._grid[row]
    
    def __setitem__(self, row: int, value: List[int]):
        if len(value) != 9:
            raise ValueError("Row must have 9 elements")
        self._grid[row] = value[:]
    
    def get(self, row: int, col: int) -> int:
        """Get cell value (0 for empty)."""
        return self._grid[row][col]
    
    def set(self, row: int, col: int, value: int):
        """Set cell value (0 for empty, 1-9 for filled)."""
        if not 0 <= value <= 9:
            raise ValueError("Value must be 0-9")
        self._grid[row][col] = value
    
    def copy(self) -> 'SudokuGrid':
        """Create a deep copy of the grid."""
        return SudokuGrid(self._grid)
    
    def get_row(self, row: int) -> List[int]:
        """Get all values in a row."""
        return self._grid[row][:]
    
    def get_col(self, col: int) -> List[int]:
        """Get all values in a column."""
        return [self._grid[row][col] for row in range(9)]
    
    def get_box(self, row: int, col: int) -> List[int]:
        """Get all values in the 3x3 box containing (row, col)."""
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        return [
            self._grid[r][c]
            for r in range(box_row, box_row + 3)
            for c in range(box_col, box_col + 3)
        ]
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get list of empty cell positions (row, col)."""
        return [
            (r, c)
            for r in range(9)
            for c in range(9)
            if self._grid[r][c] == 0
        ]
    
    def count_given(self) -> int:
        """Count number of given (filled) cells."""
        return sum(1 for r in range(9) for c in range(9) if self._grid[r][c] != 0)
    
    def is_filled(self) -> bool:
        """Check if grid is completely filled."""
        return all(self._grid[r][c] != 0 for r in range(9) for c in range(9))
    
    def to_list(self) -> List[List[int]]:
        """Convert to nested list."""
        return [row[:] for row in self._grid]
    
    def to_flat(self) -> List[int]:
        """Convert to flat list (row-major order)."""
        return [self._grid[r][c] for r in range(9) for c in range(9)]
    
    @classmethod
    def from_flat(cls, flat: List[int]) -> 'SudokuGrid':
        """Create grid from flat list (row-major order)."""
        if len(flat) != 81:
            raise ValueError("Flat list must have 81 elements")
        grid = [[flat[r * 9 + c] for c in range(9)] for r in range(9)]
        return cls(grid)
    
    @classmethod
    def from_string(cls, s: str) -> 'SudokuGrid':
        """
        Parse grid from string.
        
        Supports formats:
        - Single line of 81 digits (0 or . for empty)
        - 9 lines of 9 digits
        - With or without separators (spaces, |, -, +)
        """
        # Remove all separators and whitespace except newlines
        cleaned = ''.join(c for c in s if c.isdigit() or c == '.')
        
        # Replace . with 0
        cleaned = cleaned.replace('.', '0')
        
        if len(cleaned) != 81:
            raise ValueError(f"Expected 81 digits, got {len(cleaned)}")
        
        flat = [int(c) for c in cleaned]
        return cls.from_flat(flat)
    
    def __str__(self) -> str:
        """Pretty string representation with box borders."""
        lines = []
        for r in range(9):
            if r > 0 and r % 3 == 0:
                lines.append("------+-------+------")
            row_str = ""
            for c in range(9):
                if c > 0 and c % 3 == 0:
                    row_str += "| "
                val = self._grid[r][c]
                row_str += f"{val if val != 0 else '.'} "
            lines.append(row_str.rstrip())
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"SudokuGrid({self._grid!r})"


class SudokuSolver:
    """
    Sudoku puzzle solver using backtracking algorithm.
    
    Features:
    - Solve any valid sudoku puzzle
    - Count solutions (to check uniqueness)
    - Find all solutions up to a limit
    - Get possible values for a cell
    """
    
    def __init__(self, grid: SudokuGrid):
        """Initialize solver with a grid."""
        self.grid = grid.copy()
        self._solutions: List[SudokuGrid] = []
    
    def is_valid_placement(self, row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in self.grid.get_row(row):
            return False
        
        # Check column
        if num in self.grid.get_col(col):
            return False
        
        # Check 3x3 box
        if num in self.grid.get_box(row, col):
            return False
        
        return True
    
    def get_possible_values(self, row: int, col: int) -> Set[int]:
        """Get all valid values for a cell."""
        if self.grid.get(row, col) != 0:
            return set()
        
        used = set(self.grid.get_row(row))
        used.update(self.grid.get_col(col))
        used.update(self.grid.get_box(row, col))
        
        return set(range(1, 10)) - used
    
    def _find_empty(self) -> Optional[Tuple[int, int]]:
        """Find next empty cell (with MRV heuristic)."""
        empty_cells = self.grid.get_empty_cells()
        if not empty_cells:
            return None
        
        # Minimum Remaining Values heuristic - choose cell with fewest possibilities
        min_options = 10
        best_cell = empty_cells[0]
        
        for r, c in empty_cells:
            options = len(self.get_possible_values(r, c))
            if options < min_options:
                min_options = options
                best_cell = (r, c)
                if options == 1:  # Can't do better than 1
                    break
        
        return best_cell
    
    def solve(self) -> bool:
        """
        Solve the puzzle in-place.
        
        Returns:
            True if solved, False if unsolvable
        """
        empty = self._find_empty()
        if empty is None:
            return True  # Solved!
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid_placement(row, col, num):
                self.grid.set(row, col, num)
                
                if self.solve():
                    return True
                
                self.grid.set(row, col, 0)  # Backtrack
        
        return False
    
    def count_solutions(self, max_count: int = 2) -> int:
        """
        Count number of solutions (up to max_count).
        
        Args:
            max_count: Stop counting after this many solutions found
        
        Returns:
            Number of solutions found (capped at max_count)
        """
        self._solutions = []
        self._count_solutions_recursive(max_count)
        return len(self._solutions)
    
    def _count_solutions_recursive(self, max_count: int) -> bool:
        """Recursive helper for counting solutions."""
        if len(self._solutions) >= max_count:
            return True
        
        empty = self._find_empty()
        if empty is None:
            self._solutions.append(self.grid.copy())
            return len(self._solutions) >= max_count
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid_placement(row, col, num):
                self.grid.set(row, col, num)
                
                if self._count_solutions_recursive(max_count):
                    return True
                
                self.grid.set(row, col, 0)
        
        return False
    
    def get_solution(self) -> Optional[SudokuGrid]:
        """Get the solution (or first solution if multiple exist)."""
        grid_copy = self.grid.copy()
        solver = SudokuSolver(grid_copy)
        if solver.solve():
            return solver.grid
        return None
    
    def has_unique_solution(self) -> bool:
        """Check if puzzle has exactly one solution."""
        return self.count_solutions(2) == 1


class SudokuGenerator:
    """
    Sudoku puzzle generator.
    
    Features:
    - Generate valid puzzles with specified difficulty
    - Generate full solved grids
    - Remove cells while maintaining unique solution
    """
    
    @staticmethod
    def _shuffle_range() -> List[int]:
        """Get shuffled list of 1-9."""
        nums = list(range(1, 10))
        random.shuffle(nums)
        return nums
    
    @staticmethod
    def _get_shuffled_positions() -> List[Tuple[int, int]]:
        """Get shuffled list of all grid positions."""
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        return positions
    
    @staticmethod
    def generate_solved() -> SudokuGrid:
        """
        Generate a fully solved valid sudoku grid.
        
        Uses randomized backtracking for variety.
        """
        grid = SudokuGrid()
        
        def fill(pos: int) -> bool:
            if pos == 81:
                return True
            
            row, col = pos // 9, pos % 9
            nums = SudokuGenerator._shuffle_range()
            
            for num in nums:
                solver = SudokuSolver(grid)
                if solver.is_valid_placement(row, col, num):
                    grid.set(row, col, num)
                    if fill(pos + 1):
                        return True
                    grid.set(row, col, 0)
            
            return False
        
        fill(0)
        return grid
    
    @staticmethod
    def generate(
        difficulty: Difficulty = Difficulty.MEDIUM,
        given_range: Optional[Tuple[int, int]] = None
    ) -> SudokuGrid:
        """
        Generate a new sudoku puzzle.
        
        Args:
            difficulty: Difficulty level (determines number of given cells)
            given_range: Optional override for number of given cells (min, max)
        
        Returns:
            Unsolved puzzle grid
        """
        # Determine target number of given cells
        if given_range:
            min_given, max_given = given_range
        else:
            ranges = {
                Difficulty.EASY: (36, 45),
                Difficulty.MEDIUM: (27, 35),
                Difficulty.HARD: (22, 26),
                Difficulty.EXPERT: (17, 21),
                Difficulty.EVIL: (10, 16),
            }
            min_given, max_given = ranges[difficulty]
        
        # Generate solved grid
        solved = SudokuGenerator.generate_solved()
        puzzle = solved.copy()
        
        # Determine number of cells to remove
        total_cells = 81
        target_given = random.randint(min_given, max_given)
        cells_to_remove = total_cells - target_given
        
        # Remove cells while maintaining unique solution
        positions = SudokuGenerator._get_shuffled_positions()
        removed = 0
        
        for row, col in positions:
            if removed >= cells_to_remove:
                break
            
            original = puzzle.get(row, col)
            puzzle.set(row, col, 0)
            
            # Check if still has unique solution
            solver = SudokuSolver(puzzle)
            if solver.count_solutions(2) == 1:
                removed += 1
            else:
                # Restore cell if removing it creates multiple solutions
                puzzle.set(row, col, original)
        
        return puzzle
    
    @staticmethod
    def generate_with_solution(
        difficulty: Difficulty = Difficulty.MEDIUM
    ) -> Tuple[SudokuGrid, SudokuGrid]:
        """
        Generate puzzle along with its solution.
        
        Returns:
            Tuple of (puzzle, solution)
        """
        solved = SudokuGenerator.generate_solved()
        puzzle = solved.copy()
        
        ranges = {
            Difficulty.EASY: (36, 45),
            Difficulty.MEDIUM: (27, 35),
            Difficulty.HARD: (22, 26),
            Difficulty.EXPERT: (17, 21),
            Difficulty.EVIL: (10, 16),
        }
        min_given, max_given = ranges[difficulty]
        target_given = random.randint(min_given, max_given)
        cells_to_remove = 81 - target_given
        
        positions = SudokuGenerator._get_shuffled_positions()
        removed = 0
        
        for row, col in positions:
            if removed >= cells_to_remove:
                break
            
            original = puzzle.get(row, col)
            puzzle.set(row, col, 0)
            
            solver = SudokuSolver(puzzle)
            if solver.count_solutions(2) == 1:
                removed += 1
            else:
                puzzle.set(row, col, original)
        
        return puzzle, solved


class SudokuValidator:
    """
    Sudoku puzzle and solution validator.
    
    Features:
    - Validate puzzle format
    - Validate solution correctness
    - Check for conflicts
    - Find duplicate entries
    """
    
    @staticmethod
    def is_valid_grid(grid: SudokuGrid) -> bool:
        """Check if grid has valid format (no conflicts in given cells)."""
        for r in range(9):
            for c in range(9):
                val = grid.get(r, c)
                if val == 0:
                    continue
                
                # Check for duplicates in row
                row = grid.get_row(r)
                if row.count(val) > 1:
                    return False
                
                # Check for duplicates in column
                col = grid.get_col(c)
                if col.count(val) > 1:
                    return False
                
                # Check for duplicates in box
                box = grid.get_box(r, c)
                if box.count(val) > 1:
                    return False
        
        return True
    
    @staticmethod
    def is_valid_solution(grid: SudokuGrid) -> bool:
        """Check if grid is a valid complete solution."""
        # Check if filled
        if not grid.is_filled():
            return False
        
        # Check all rows
        for r in range(9):
            if set(grid.get_row(r)) != set(range(1, 10)):
                return False
        
        # Check all columns
        for c in range(9):
            if set(grid.get_col(c)) != set(range(1, 10)):
                return False
        
        # Check all 3x3 boxes
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                box = grid.get_box(box_r, box_c)
                if set(box) != set(range(1, 10)):
                    return False
        
        return True
    
    @staticmethod
    def find_conflicts(grid: SudokuGrid) -> List[Tuple[int, int, int, str]]:
        """
        Find all conflicts in the grid.
        
        Returns:
            List of (row, col, value, conflict_type) tuples
        """
        conflicts = []
        seen_rows: dict = {}  # (row, num) -> col
        seen_cols: dict = {}  # (col, num) -> row
        seen_boxes: dict = {}  # (box, num) -> (row, col)
        
        for r in range(9):
            for c in range(9):
                val = grid.get(r, c)
                if val == 0:
                    continue
                
                # Check row conflict
                row_key = (r, val)
                if row_key in seen_rows:
                    conflicts.append((r, c, val, f"row duplicate with ({r}, {seen_rows[row_key]})"))
                else:
                    seen_rows[row_key] = c
                
                # Check column conflict
                col_key = (c, val)
                if col_key in seen_cols:
                    conflicts.append((r, c, val, f"col duplicate with ({seen_cols[col_key]}, {c})"))
                else:
                    seen_cols[col_key] = r
                
                # Check box conflict
                box_key = (r // 3, c // 3, val)
                if box_key in seen_boxes:
                    other_r, other_c = seen_boxes[box_key]
                    conflicts.append((r, c, val, f"box duplicate with ({other_r}, {other_c})"))
                else:
                    seen_boxes[box_key] = (r, c)
        
        return conflicts


class SudokuAnalyzer:
    """
    Sudoku puzzle analyzer.
    
    Features:
    - Estimate difficulty
    - Find hints
    - Get solving progress
    """
    
    @staticmethod
    def estimate_difficulty(grid: SudokuGrid) -> Difficulty:
        """
        Estimate puzzle difficulty based on given cells.
        
        Note: This is a heuristic. True difficulty depends on
        the techniques required to solve (naked singles, hidden pairs, etc.)
        """
        given = grid.count_given()
        
        if given >= 36:
            return Difficulty.EASY
        elif given >= 27:
            return Difficulty.MEDIUM
        elif given >= 22:
            return Difficulty.HARD
        elif given >= 17:
            return Difficulty.EXPERT
        else:
            return Difficulty.EVIL
    
    @staticmethod
    def get_progress(grid: SudokuGrid) -> Tuple[int, int, float]:
        """
        Get solving progress.
        
        Returns:
            Tuple of (filled_cells, total_cells, percentage)
        """
        filled = 81 - len(grid.get_empty_cells())
        percentage = (filled / 81) * 100
        return filled, 81, percentage
    
    @staticmethod
    def get_hint(grid: SudokuGrid) -> Optional[Tuple[int, int, int, str]]:
        """
        Get a hint for the next move.
        
        Returns:
            Tuple of (row, col, value, technique) or None if no hint available
        """
        solver = SudokuSolver(grid)
        
        # Find naked single (cell with only one possibility)
        for r, c in grid.get_empty_cells():
            possible = solver.get_possible_values(r, c)
            if len(possible) == 1:
                val = possible.pop()
                return (r, c, val, "naked single")
        
        # Find hidden single in row
        for r in range(9):
            for num in range(1, 10):
                positions = []
                for c in range(9):
                    if grid.get(r, c) == 0 and num in solver.get_possible_values(r, c):
                        positions.append(c)
                if len(positions) == 1:
                    return (r, positions[0], num, "hidden single in row")
        
        # Find hidden single in column
        for c in range(9):
            for num in range(1, 10):
                positions = []
                for r in range(9):
                    if grid.get(r, c) == 0 and num in solver.get_possible_values(r, c):
                        positions.append(r)
                if len(positions) == 1:
                    return (positions[0], c, num, "hidden single in column")
        
        # Find hidden single in box
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                for num in range(1, 10):
                    positions = []
                    for r in range(box_r, box_r + 3):
                        for c in range(box_c, box_c + 3):
                            if grid.get(r, c) == 0 and num in solver.get_possible_values(r, c):
                                positions.append((r, c))
                    if len(positions) == 1:
                        return (*positions[0], num, "hidden single in box")
        
        return None
    
    @staticmethod
    def get_all_hints(grid: SudokuGrid) -> List[Tuple[int, int, int, str]]:
        """Get all available hints using basic techniques."""
        hints = []
        grid_copy = grid.copy()
        
        while True:
            hint = SudokuAnalyzer.get_hint(grid_copy)
            if hint is None:
                break
            hints.append(hint)
            r, c, val, _ = hint
            grid_copy.set(r, c, val)
        
        return hints


# Convenience functions
def solve(grid: SudokuGrid) -> Optional[SudokuGrid]:
    """Solve a sudoku puzzle and return the solution."""
    solver = SudokuSolver(grid)
    return solver.get_solution()


def generate(difficulty: Difficulty = Difficulty.MEDIUM) -> SudokuGrid:
    """Generate a new sudoku puzzle."""
    return SudokuGenerator.generate(difficulty)


def validate(grid: SudokuGrid) -> bool:
    """Check if a grid is valid (no conflicts)."""
    return SudokuValidator.is_valid_grid(grid)


def is_solved(grid: SudokuGrid) -> bool:
    """Check if a grid is a valid complete solution."""
    return SudokuValidator.is_valid_solution(grid)


def analyze(grid: SudokuGrid) -> dict:
    """Analyze a sudoku puzzle and return statistics."""
    return {
        "given_cells": grid.count_given(),
        "empty_cells": len(grid.get_empty_cells()),
        "difficulty": SudokuAnalyzer.estimate_difficulty(grid).value,
        "is_valid": SudokuValidator.is_valid_grid(grid),
        "has_unique_solution": SudokuSolver(grid).has_unique_solution(),
    }