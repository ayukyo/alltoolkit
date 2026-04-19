#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Sudoku Utilities Module
====================================
A comprehensive Sudoku puzzle utility module with zero external dependencies.

Features:
    - Sudoku puzzle solving (optimized backtracking with constraint propagation)
    - Puzzle generation with configurable difficulty
    - Puzzle validation and checking
    - Difficulty estimation
    - Hint system for stuck players
    - Multiple output formats (grid, string, pretty print)
    - Puzzle import/export (various formats)
    - Solution uniqueness verification

Author: AllToolkit Contributors
License: MIT
Date: 2026-04-20
"""

import random
import copy
from typing import List, Optional, Tuple, Set, Generator
from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    """Sudoku difficulty levels."""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4
    EVIL = 5


@dataclass
class SudokuCell:
    """Represents a single cell in a Sudoku grid."""
    value: int  # 0 means empty
    candidates: Set[int]  # Possible values for this cell
    fixed: bool  # True if this is a given number (not player-filled)


class SudokuGrid:
    """
    Represents a 9x9 Sudoku grid with full state management.
    
    Supports:
        - Cell value access and modification
        - Candidate tracking
        - Row, column, and box operations
        - Validation and checking
    """
    
    def __init__(self, grid: Optional[List[List[int]]] = None):
        """
        Initialize a Sudoku grid.
        
        Args:
            grid: Optional 9x9 grid of integers (0 for empty cells)
        """
        self._grid: List[List[SudokuCell]] = []
        
        if grid is None:
            # Empty grid
            for i in range(9):
                row = []
                for j in range(9):
                    row.append(SudokuCell(
                        value=0,
                        candidates=set(range(1, 10)),
                        fixed=False
                    ))
                self._grid.append(row)
        else:
            self._load_grid(grid)
    
    def _load_grid(self, grid: List[List[int]]) -> None:
        """Load a grid from a 2D list."""
        if len(grid) != 9:
            raise ValueError("Grid must be 9x9")
        
        self._grid = []
        for i in range(9):
            if len(grid[i]) != 9:
                raise ValueError("Grid must be 9x9")
            row = []
            for j in range(9):
                val = grid[i][j]
                if val < 0 or val > 9:
                    raise ValueError(f"Invalid value at ({i}, {j}): {val}")
                
                cell = SudokuCell(
                    value=val,
                    candidates=set() if val != 0 else set(range(1, 10)),
                    fixed=(val != 0)
                )
                row.append(cell)
            self._grid.append(row)
        
        # Update candidates based on existing values
        self._update_all_candidates()
    
    def _update_all_candidates(self) -> None:
        """Update candidates for all empty cells."""
        for i in range(9):
            for j in range(9):
                if self._grid[i][j].value == 0:
                    self._grid[i][j].candidates = self._get_candidates(i, j)
    
    def _get_candidates(self, row: int, col: int) -> Set[int]:
        """Get possible values for a cell."""
        if self._grid[row][col].value != 0:
            return set()
        
        used = set()
        
        # Row
        for j in range(9):
            if self._grid[row][j].value != 0:
                used.add(self._grid[row][j].value)
        
        # Column
        for i in range(9):
            if self._grid[i][col].value != 0:
                used.add(self._grid[i][col].value)
        
        # 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self._grid[i][j].value != 0:
                    used.add(self._grid[i][j].value)
        
        return set(range(1, 10)) - used
    
    def get(self, row: int, col: int) -> int:
        """Get the value at a cell."""
        return self._grid[row][col].value
    
    def set(self, row: int, col: int, value: int) -> bool:
        """
        Set a value at a cell.
        
        Returns:
            True if the value was set successfully, False if invalid.
        """
        if self._grid[row][col].fixed:
            return False
        
        if value != 0 and value not in self._grid[row][col].candidates:
            return False
        
        self._grid[row][col].value = value
        if value != 0:
            self._grid[row][col].candidates = set()
        
        # Update candidates for affected cells
        self._update_all_candidates()
        return True
    
    def get_candidates(self, row: int, col: int) -> Set[int]:
        """Get candidates for a cell."""
        return self._grid[row][col].candidates.copy()
    
    def is_fixed(self, row: int, col: int) -> bool:
        """Check if a cell is a given (fixed) number."""
        return self._grid[row][col].fixed
    
    def get_row(self, row: int) -> List[int]:
        """Get a row as a list of values."""
        return [self._grid[row][j].value for j in range(9)]
    
    def get_col(self, col: int) -> List[int]:
        """Get a column as a list of values."""
        return [self._grid[i][col].value for i in range(9)]
    
    def get_box(self, box: int) -> List[int]:
        """
        Get a 3x3 box as a list of values.
        
        Args:
            box: Box number (0-8), left to right, top to bottom.
        """
        box_row, box_col = 3 * (box // 3), 3 * (box % 3)
        values = []
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                values.append(self._grid[i][j].value)
        return values
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get list of empty cell coordinates."""
        empty = []
        for i in range(9):
            for j in range(9):
                if self._grid[i][j].value == 0:
                    empty.append((i, j))
        return empty
    
    def to_list(self) -> List[List[int]]:
        """Convert to 2D list of integers."""
        return [[self._grid[i][j].value for j in range(9)] for i in range(9)]
    
    def copy(self) -> 'SudokuGrid':
        """Create a deep copy of the grid."""
        new_grid = SudokuGrid()
        for i in range(9):
            for j in range(9):
                new_grid._grid[i][j].value = self._grid[i][j].value
                new_grid._grid[i][j].candidates = self._grid[i][j].candidates.copy()
                new_grid._grid[i][j].fixed = self._grid[i][j].fixed
        return new_grid
    
    def __str__(self) -> str:
        """Pretty string representation."""
        lines = []
        for i in range(9):
            if i % 3 == 0 and i != 0:
                lines.append("-" * 21)
            row_str = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str.append("|")
                val = self._grid[i][j].value
                row_str.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row_str))
        return "\n".join(lines)


class SudokuSolver:
    """
    Advanced Sudoku solver using multiple techniques.
    
    Techniques used (in order):
        1. Naked singles
        2. Hidden singles
        3. Constraint propagation
        4. Backtracking (with MRV heuristic)
    """
    
    @staticmethod
    def solve(grid: SudokuGrid) -> bool:
        """
        Solve the Sudoku puzzle in place.
        
        Args:
            grid: SudokuGrid to solve
        
        Returns:
            True if solved successfully, False if unsolvable.
        """
        # Apply constraint propagation first
        if not SudokuSolver._propagate(grid):
            return False
        
        # Check if solved
        if not grid.get_empty_cells():
            return True
        
        # Use backtracking for remaining cells
        return SudokuSolver._backtrack(grid)
    
    @staticmethod
    def solve_copy(grid: SudokuGrid) -> Optional[SudokuGrid]:
        """
        Solve and return a copy of the solved grid.
        
        Returns:
            Solved grid copy, or None if unsolvable.
        """
        new_grid = grid.copy()
        if SudokuSolver.solve(new_grid):
            return new_grid
        return None
    
    @staticmethod
    def count_solutions(grid: SudokuGrid, max_count: int = 2) -> int:
        """
        Count the number of solutions (up to max_count).
        
        Args:
            grid: Grid to check
            max_count: Maximum solutions to count (for early termination)
        
        Returns:
            Number of solutions found (capped at max_count)
        """
        grid_copy = grid.copy()
        if not SudokuSolver._propagate(grid_copy):
            return 0
        
        return SudokuSolver._count_solutions_recursive(grid_copy, max_count, 0)
    
    @staticmethod
    def _count_solutions_recursive(grid: SudokuGrid, max_count: int, current: int) -> int:
        """Recursive solution counting."""
        if current >= max_count:
            return current
        
        empty = grid.get_empty_cells()
        if not empty:
            return current + 1
        
        # MRV: choose cell with minimum candidates
        min_cell = min(empty, key=lambda c: len(grid.get_candidates(c[0], c[1])))
        row, col = min_cell
        candidates = list(grid.get_candidates(row, col))
        
        count = current
        for val in candidates:
            grid_copy = grid.copy()
            grid_copy.set(row, col, val)
            SudokuSolver._propagate(grid_copy)
            count = SudokuSolver._count_solutions_recursive(grid_copy, max_count, count)
            if count >= max_count:
                return count
        
        return count
    
    @staticmethod
    def _propagate(grid: SudokuGrid) -> bool:
        """
        Apply constraint propagation techniques.
        
        Returns:
            False if a contradiction is found, True otherwise.
        """
        changed = True
        while changed:
            changed = False
            
            # Naked singles
            for row, col in grid.get_empty_cells():
                candidates = grid.get_candidates(row, col)
                if len(candidates) == 0:
                    return False  # Contradiction
                if len(candidates) == 1:
                    val = list(candidates)[0]
                    grid.set(row, col, val)
                    changed = True
            
            # Hidden singles in rows
            for row in range(9):
                changed |= SudokuSolver._find_hidden_singles_in_row(grid, row)
            
            # Hidden singles in columns
            for col in range(9):
                changed |= SudokuSolver._find_hidden_singles_in_col(grid, col)
            
            # Hidden singles in boxes
            for box in range(9):
                changed |= SudokuSolver._find_hidden_singles_in_box(grid, box)
        
        return True
    
    @staticmethod
    def _find_hidden_singles_in_row(grid: SudokuGrid, row: int) -> bool:
        """Find and fill hidden singles in a row."""
        changed = False
        for num in range(1, 10):
            positions = []
            for col in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(col)
            
            if len(positions) == 1:
                grid.set(row, positions[0], num)
                changed = True
            elif len(positions) == 0:
                # Check if number is already placed
                if num not in grid.get_row(row):
                    return False  # Contradiction
        return changed
    
    @staticmethod
    def _find_hidden_singles_in_col(grid: SudokuGrid, col: int) -> bool:
        """Find and fill hidden singles in a column."""
        changed = False
        for num in range(1, 10):
            positions = []
            for row in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(row)
            
            if len(positions) == 1:
                grid.set(positions[0], col, num)
                changed = True
            elif len(positions) == 0:
                if num not in grid.get_col(col):
                    return False
        return changed
    
    @staticmethod
    def _find_hidden_singles_in_box(grid: SudokuGrid, box: int) -> bool:
        """Find and fill hidden singles in a 3x3 box."""
        changed = False
        box_row, box_col = 3 * (box // 3), 3 * (box % 3)
        
        for num in range(1, 10):
            positions = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if grid.get(i, j) == 0 and num in grid.get_candidates(i, j):
                        positions.append((i, j))
            
            if len(positions) == 1:
                grid.set(positions[0][0], positions[0][1], num)
                changed = True
            elif len(positions) == 0:
                # Check if number is in box
                found = False
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if grid.get(i, j) == num:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
        return changed
    
    @staticmethod
    def _backtrack(grid: SudokuGrid) -> bool:
        """Backtracking with MRV (Minimum Remaining Values) heuristic."""
        empty = grid.get_empty_cells()
        if not empty:
            return True  # Solved
        
        # MRV: choose cell with minimum candidates
        row, col = min(empty, key=lambda c: len(grid.get_candidates(c[0], c[1])))
        candidates = list(grid.get_candidates(row, col))
        
        if not candidates:
            return False  # No valid moves
        
        random.shuffle(candidates)  # Randomize for variety
        
        for val in candidates:
            grid_copy = grid.copy()
            grid_copy.set(row, col, val)
            
            if SudokuSolver._propagate(grid_copy):
                if SudokuSolver._backtrack(grid_copy):
                    # Copy solution back
                    for i in range(9):
                        for j in range(9):
                            grid.set(i, j, grid_copy.get(i, j))
                    return True
        
        return False


class SudokuGenerator:
    """
    Sudoku puzzle generator with configurable difficulty.
    """
    
    # Difficulty settings: number of cells to remove
    DIFFICULTY_CELLS = {
        Difficulty.EASY: (35, 40),      # Remove 35-40 cells (41-46 given)
        Difficulty.MEDIUM: (40, 46),     # Remove 40-46 cells (35-41 given)
        Difficulty.HARD: (46, 52),       # Remove 46-52 cells (29-35 given)
        Difficulty.EXPERT: (52, 56),    # Remove 52-56 cells (25-29 given)
        Difficulty.EVIL: (56, 60),      # Remove 56-60 cells (21-25 given)
    }
    
    @staticmethod
    def generate(difficulty: Difficulty = Difficulty.MEDIUM) -> SudokuGrid:
        """
        Generate a new Sudoku puzzle.
        
        Args:
            difficulty: Desired difficulty level
        
        Returns:
            A new SudokuGrid with the puzzle (not solved)
        """
        # Generate a complete valid grid
        grid = SudokuGenerator._generate_complete_grid()
        
        # Determine how many cells to remove
        min_remove, max_remove = SudokuGenerator.DIFFICULTY_CELLS[difficulty]
        cells_to_remove = random.randint(min_remove, max_remove)
        
        # Remove cells while maintaining unique solution
        SudokuGenerator._remove_cells(grid, cells_to_remove)
        
        # Mark remaining numbers as fixed
        for i in range(9):
            for j in range(9):
                grid._grid[i][j].fixed = (grid.get(i, j) != 0)
        
        return grid
    
    @staticmethod
    def _generate_complete_grid() -> SudokuGrid:
        """Generate a complete valid Sudoku grid."""
        grid = SudokuGrid()
        
        # Fill diagonal boxes first (they're independent)
        for box in [0, 4, 8]:
            SudokuGenerator._fill_box(grid, box)
        
        # Solve the rest using backtracking
        SudokuSolver._backtrack(grid)
        
        return grid
    
    @staticmethod
    def _fill_box(grid: SudokuGrid, box: int) -> None:
        """Fill a 3x3 box with random valid numbers."""
        box_row, box_col = 3 * (box // 3), 3 * (box % 3)
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        idx = 0
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                grid._grid[i][j].value = numbers[idx]
                grid._grid[i][j].candidates = set()
                idx += 1
    
    @staticmethod
    def _remove_cells(grid: SudokuGrid, count: int) -> None:
        """Remove cells while ensuring unique solution."""
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= count:
                break
            
            if grid.get(row, col) == 0:
                continue
            
            # Save the value
            old_value = grid.get(row, col)
            
            # Try removing
            grid.set(row, col, 0)
            grid._grid[row][col].candidates = grid._get_candidates(row, col)
            
            # Check if still unique solution
            solution_count = SudokuSolver.count_solutions(grid, 2)
            
            if solution_count == 1:
                removed += 1
            else:
                # Restore the value
                grid.set(row, col, old_value)
        
        # Update candidates
        grid._update_all_candidates()
    
    @staticmethod
    def generate_with_solution(difficulty: Difficulty = Difficulty.MEDIUM) -> Tuple[SudokuGrid, SudokuGrid]:
        """
        Generate a puzzle and its solution.
        
        Returns:
            Tuple of (puzzle_grid, solution_grid)
        """
        puzzle = SudokuGenerator.generate(difficulty)
        solution = SudokuSolver.solve_copy(puzzle)
        return puzzle, solution


class SudokuValidator:
    """
    Sudoku puzzle validation utilities.
    """
    
    @staticmethod
    def is_valid_grid(grid: SudokuGrid) -> bool:
        """
        Check if the grid has no conflicts (ignoring empty cells).
        
        Returns:
            True if no conflicts exist.
        """
        # Check rows
        for row in range(9):
            if not SudokuValidator._is_valid_group(grid.get_row(row)):
                return False
        
        # Check columns
        for col in range(9):
            if not SudokuValidator._is_valid_group(grid.get_col(col)):
                return False
        
        # Check boxes
        for box in range(9):
            if not SudokuValidator._is_valid_group(grid.get_box(box)):
                return False
        
        return True
    
    @staticmethod
    def _is_valid_group(values: List[int]) -> bool:
        """Check if a group (row/col/box) has no duplicates (ignoring zeros)."""
        seen = set()
        for val in values:
            if val == 0:
                continue
            if val in seen:
                return False
            seen.add(val)
        return True
    
    @staticmethod
    def is_complete(grid: SudokuGrid) -> bool:
        """Check if the grid is completely filled."""
        for i in range(9):
            for j in range(9):
                if grid.get(i, j) == 0:
                    return False
        return True
    
    @staticmethod
    def is_solved(grid: SudokuGrid) -> bool:
        """Check if the grid is complete and valid (solved)."""
        return SudokuValidator.is_complete(grid) and SudokuValidator.is_valid_grid(grid)
    
    @staticmethod
    def has_unique_solution(grid: SudokuGrid) -> bool:
        """Check if the puzzle has exactly one solution."""
        return SudokuSolver.count_solutions(grid, 2) == 1
    
    @staticmethod
    def is_solvable(grid: SudokuGrid) -> bool:
        """Check if the puzzle has at least one solution."""
        return SudokuSolver.count_solutions(grid, 1) >= 1
    
    @staticmethod
    def get_conflicts(grid: SudokuGrid) -> List[Tuple[int, int, int, int]]:
        """
        Find all conflicting cells.
        
        Returns:
            List of (row1, col1, row2, col2) pairs of conflicting cells.
        """
        conflicts = []
        
        # Check rows
        for row in range(9):
            row_conflicts = SudokuValidator._find_conflicts_in_line(
                [(row, col, grid.get(row, col)) for col in range(9)]
            )
            conflicts.extend(row_conflicts)
        
        # Check columns
        for col in range(9):
            col_conflicts = SudokuValidator._find_conflicts_in_line(
                [(row, col, grid.get(row, col)) for row in range(9)]
            )
            conflicts.extend(col_conflicts)
        
        # Check boxes
        for box in range(9):
            box_row, box_col = 3 * (box // 3), 3 * (box % 3)
            box_cells = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    box_cells.append((i, j, grid.get(i, j)))
            box_conflicts = SudokuValidator._find_conflicts_in_line(box_cells)
            conflicts.extend(box_conflicts)
        
        return conflicts
    
    @staticmethod
    def _find_conflicts_in_line(cells: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """Find conflicts in a line of cells."""
        conflicts = []
        value_positions = {}  # value -> list of (row, col)
        
        for row, col, val in cells:
            if val == 0:
                continue
            if val not in value_positions:
                value_positions[val] = []
            value_positions[val].append((row, col))
        
        for val, positions in value_positions.items():
            if len(positions) > 1:
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        conflicts.append((*positions[i], *positions[j]))
        
        return conflicts


class SudokuHint:
    """
    Hint system for Sudoku puzzles.
    """
    
    @staticmethod
    def get_next_cell_hint(grid: SudokuGrid) -> Optional[Tuple[int, int, int]]:
        """
        Get the next cell to fill (easiest by candidates).
        
        Returns:
            Tuple of (row, col, value) or None if solved.
        """
        empty = grid.get_empty_cells()
        if not empty:
            return None
        
        # Find cell with minimum candidates
        best_cell = None
        min_candidates = 10
        
        for row, col in empty:
            candidates = grid.get_candidates(row, col)
            if len(candidates) < min_candidates:
                min_candidates = len(candidates)
                best_cell = (row, col, candidates)
        
        if best_cell:
            row, col, candidates = best_cell
            if candidates:
                return (row, col, list(candidates)[0])
        
        return None
    
    @staticmethod
    def get_hint(grid: SudokuGrid, solution: Optional[SudokuGrid] = None) -> Optional[Tuple[int, int, int, str]]:
        """
        Get a hint for the next move.
        
        Args:
            grid: Current puzzle state
            solution: Optional pre-computed solution
        
        Returns:
            Tuple of (row, col, value, technique) or None if solved.
            technique describes why this value works.
        """
        # Try naked single
        for row, col in grid.get_empty_cells():
            candidates = grid.get_candidates(row, col)
            if len(candidates) == 1:
                val = list(candidates)[0]
                return (row, col, val, f"Only candidate in cell ({row+1}, {col+1})")
        
        # Try hidden single in row
        for row in range(9):
            result = SudokuHint._find_hidden_single_row(grid, row)
            if result:
                col, val = result
                return (row, col, val, f"Only place for {val} in row {row+1}")
        
        # Try hidden single in column
        for col in range(9):
            result = SudokuHint._find_hidden_single_col(grid, col)
            if result:
                row, val = result
                return (row, col, val, f"Only place for {val} in column {col+1}")
        
        # Try hidden single in box
        for box in range(9):
            result = SudokuHint._find_hidden_single_box(grid, box)
            if result:
                row, col, val = result
                return (row, col, val, f"Only place for {val} in box {box+1}")
        
        # Fall back to solution-based hint
        if solution:
            for row in range(9):
                for col in range(9):
                    if grid.get(row, col) == 0:
                        return (row, col, solution.get(row, col), "From solution")
        
        return None
    
    @staticmethod
    def _find_hidden_single_row(grid: SudokuGrid, row: int) -> Optional[Tuple[int, int]]:
        """Find hidden single in row. Returns (col, value) or None."""
        for num in range(1, 10):
            positions = []
            for col in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(col)
            if len(positions) == 1:
                return (positions[0], num)
        return None
    
    @staticmethod
    def _find_hidden_single_col(grid: SudokuGrid, col: int) -> Optional[Tuple[int, int]]:
        """Find hidden single in column. Returns (row, value) or None."""
        for num in range(1, 10):
            positions = []
            for row in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(row)
            if len(positions) == 1:
                return (positions[0], num)
        return None
    
    @staticmethod
    def _find_hidden_single_box(grid: SudokuGrid, box: int) -> Optional[Tuple[int, int, int]]:
        """Find hidden single in box. Returns (row, col, value) or None."""
        box_row, box_col = 3 * (box // 3), 3 * (box % 3)
        
        for num in range(1, 10):
            positions = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if grid.get(i, j) == 0 and num in grid.get_candidates(i, j):
                        positions.append((i, j))
            if len(positions) == 1:
                return (*positions[0], num)
        return None


class SudokuDifficultyEstimator:
    """
    Estimate the difficulty of a Sudoku puzzle.
    
    Uses multiple metrics:
        - Number of given cells
        - Number of naked singles
        - Number of hidden singles
        - Techniques required to solve
    """
    
    @staticmethod
    def estimate(grid: SudokuGrid) -> Tuple[Difficulty, dict]:
        """
        Estimate puzzle difficulty.
        
        Returns:
            Tuple of (Difficulty, metrics_dict)
        """
        metrics = SudokuDifficultyEstimator._calculate_metrics(grid)
        
        # Score based on metrics
        score = 0
        
        # Number of givens (fewer = harder)
        givens = metrics['givens']
        if givens >= 45:
            score += 1
        elif givens >= 35:
            score += 2
        elif givens >= 28:
            score += 3
        elif givens >= 24:
            score += 4
        else:
            score += 5
        
        # Empty cells with few candidates (easier)
        min_candidates = metrics['min_candidates_in_empty']
        if min_candidates == 1:
            score += 0
        elif min_candidates == 2:
            score += 1
        else:
            score += 2
        
        # Average candidates per empty cell (higher = harder)
        avg_candidates = metrics['avg_candidates']
        if avg_candidates <= 2:
            score += 0
        elif avg_candidates <= 3:
            score += 1
        elif avg_candidates <= 4:
            score += 2
        else:
            score += 3
        
        # Hidden singles count (fewer = harder)
        hidden_singles = metrics['hidden_singles']
        if hidden_singles >= 20:
            score += 0
        elif hidden_singles >= 10:
            score += 1
        elif hidden_singles >= 5:
            score += 2
        else:
            score += 3
        
        # Determine difficulty
        if score <= 3:
            difficulty = Difficulty.EASY
        elif score <= 5:
            difficulty = Difficulty.MEDIUM
        elif score <= 7:
            difficulty = Difficulty.HARD
        elif score <= 9:
            difficulty = Difficulty.EXPERT
        else:
            difficulty = Difficulty.EVIL
        
        return difficulty, metrics
    
    @staticmethod
    def _calculate_metrics(grid: SudokuGrid) -> dict:
        """Calculate various metrics for the puzzle."""
        givens = 0
        empty_cells = 0
        total_candidates = 0
        min_candidates = 10
        naked_singles = 0
        hidden_singles = 0
        
        for i in range(9):
            for j in range(9):
                val = grid.get(i, j)
                if val != 0:
                    givens += 1
                else:
                    empty_cells += 1
                    candidates = grid.get_candidates(i, j)
                    total_candidates += len(candidates)
                    min_candidates = min(min_candidates, len(candidates))
                    if len(candidates) == 1:
                        naked_singles += 1
        
        # Count hidden singles in rows, cols, boxes
        for row in range(9):
            hidden_singles += SudokuDifficultyEstimator._count_hidden_singles_row(grid, row)
        for col in range(9):
            hidden_singles += SudokuDifficultyEstimator._count_hidden_singles_col(grid, col)
        for box in range(9):
            hidden_singles += SudokuDifficultyEstimator._count_hidden_singles_box(grid, box)
        
        return {
            'givens': givens,
            'empty_cells': empty_cells,
            'total_candidates': total_candidates,
            'avg_candidates': total_candidates / empty_cells if empty_cells > 0 else 0,
            'min_candidates_in_empty': min_candidates if empty_cells > 0 else 0,
            'naked_singles': naked_singles,
            'hidden_singles': hidden_singles,
        }
    
    @staticmethod
    def _count_hidden_singles_row(grid: SudokuGrid, row: int) -> int:
        """Count hidden singles in a row."""
        count = 0
        for num in range(1, 10):
            positions = []
            for col in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(col)
            if len(positions) == 1:
                count += 1
        return count
    
    @staticmethod
    def _count_hidden_singles_col(grid: SudokuGrid, col: int) -> int:
        """Count hidden singles in a column."""
        count = 0
        for num in range(1, 10):
            positions = []
            for row in range(9):
                if grid.get(row, col) == 0 and num in grid.get_candidates(row, col):
                    positions.append(row)
            if len(positions) == 1:
                count += 1
        return count
    
    @staticmethod
    def _count_hidden_singles_box(grid: SudokuGrid, box: int) -> int:
        """Count hidden singles in a box."""
        count = 0
        box_row, box_col = 3 * (box // 3), 3 * (box % 3)
        
        for num in range(1, 10):
            positions = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if grid.get(i, j) == 0 and num in grid.get_candidates(i, j):
                        positions.append((i, j))
            if len(positions) == 1:
                count += 1
        return count


class SudokuFormatter:
    """
    Format Sudoku puzzles for display and export.
    """
    
    @staticmethod
    def to_string(grid: SudokuGrid, empty: str = '.') -> str:
        """
        Convert grid to a single-line string.
        
        Args:
            grid: Sudoku grid
            empty: Character for empty cells
        
        Returns:
            81-character string
        """
        chars = []
        for i in range(9):
            for j in range(9):
                val = grid.get(i, j)
                chars.append(str(val) if val != 0 else empty)
        return ''.join(chars)
    
    @staticmethod
    def from_string(s: str) -> SudokuGrid:
        """
        Parse a string into a SudokuGrid.
        
        Args:
            s: 81-character string (digits 1-9 are filled, '0', '.' or any non-digit is empty)
        
        Returns:
            SudokuGrid
        """
        # Filter to valid Sudoku characters
        cells = []
        for c in s:
            if c in '123456789':
                cells.append(int(c))
            elif c in '0.':
                cells.append(0)
            elif c.isdigit():
                cells.append(int(c))  # Handle any digit
        
        # Also accept shorter strings with dots as placeholders
        if len(cells) != 81:
            # Try parsing as compact format (only digits and dots)
            filtered = []
            for c in s:
                if c.isdigit():
                    filtered.append(int(c))
                elif c == '.':
                    filtered.append(0)
            if len(filtered) == 81:
                cells = filtered
            else:
                raise ValueError(f"Expected 81 cells, got {len(cells)}")
        
        grid_data = [cells[i*9:(i+1)*9] for i in range(9)]
        return SudokuGrid(grid_data)
    
    @staticmethod
    def to_pretty_string(grid: SudokuGrid) -> str:
        """Format grid with borders and spacing."""
        return str(grid)
    
    @staticmethod
    def to_markdown(grid: SudokuGrid) -> str:
        """Format grid as Markdown table."""
        lines = ["|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"]
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        
        for i in range(9):
            row_vals = [str(i + 1)]
            for j in range(9):
                val = grid.get(i, j)
                row_vals.append(str(val) if val != 0 else ' ')
            lines.append("| " + " | ".join(row_vals) + " |")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_json(grid: SudokuGrid) -> str:
        """Format grid as JSON."""
        import json
        return json.dumps(grid.to_list())
    
    @staticmethod
    def from_json(json_str: str) -> SudokuGrid:
        """Parse JSON into SudokuGrid."""
        import json
        data = json.loads(json_str)
        return SudokuGrid(data)
    
    @staticmethod
    def to_2d_array(grid: SudokuGrid) -> List[List[int]]:
        """Convert to 2D array (alias for to_list)."""
        return grid.to_list()


# =============================================================================
# Convenience Functions
# =============================================================================

def create_puzzle(difficulty: Difficulty = Difficulty.MEDIUM) -> SudokuGrid:
    """Create a new Sudoku puzzle with specified difficulty."""
    return SudokuGenerator.generate(difficulty)


def solve_puzzle(grid: SudokuGrid) -> Optional[SudokuGrid]:
    """Solve a Sudoku puzzle and return the solution."""
    return SudokuSolver.solve_copy(grid)


def is_valid_puzzle(grid: SudokuGrid) -> bool:
    """Check if a puzzle is valid (no conflicts)."""
    return SudokuValidator.is_valid_grid(grid)


def is_solved_puzzle(grid: SudokuGrid) -> bool:
    """Check if a puzzle is completely solved."""
    return SudokuValidator.is_solved(grid)


def get_hint(grid: SudokuGrid, solution: Optional[SudokuGrid] = None) -> Optional[Tuple[int, int, int, str]]:
    """Get a hint for the next move."""
    return SudokuHint.get_hint(grid, solution)


def estimate_difficulty(grid: SudokuGrid) -> Tuple[Difficulty, dict]:
    """Estimate the difficulty of a puzzle."""
    return SudokuDifficultyEstimator.estimate(grid)


def parse_puzzle(s: str) -> SudokuGrid:
    """Parse a string into a Sudoku puzzle."""
    return SudokuFormatter.from_string(s)


def format_puzzle(grid: SudokuGrid, format: str = 'pretty') -> str:
    """
    Format a puzzle for display.
    
    Args:
        grid: Sudoku grid
        format: 'pretty', 'string', 'markdown', or 'json'
    """
    if format == 'pretty':
        return SudokuFormatter.to_pretty_string(grid)
    elif format == 'string':
        return SudokuFormatter.to_string(grid)
    elif format == 'markdown':
        return SudokuFormatter.to_markdown(grid)
    elif format == 'json':
        return SudokuFormatter.to_json(grid)
    else:
        raise ValueError(f"Unknown format: {format}")


# =============================================================================
# Main Demo
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Sudoku Utilities Demo")
    print("=" * 50)
    
    # Generate a puzzle
    print("\n1. Generating a Medium difficulty puzzle...")
    puzzle = create_puzzle(Difficulty.MEDIUM)
    print(puzzle)
    
    # Estimate difficulty
    print("\n2. Estimating difficulty...")
    difficulty, metrics = estimate_difficulty(puzzle)
    print(f"   Difficulty: {difficulty.name}")
    print(f"   Metrics: {metrics}")
    
    # Solve the puzzle
    print("\n3. Solving the puzzle...")
    solution = solve_puzzle(puzzle)
    if solution:
        print(solution)
    else:
        print("   Could not solve!")
    
    # Get a hint
    print("\n4. Getting a hint (for original puzzle)...")
    hint = get_hint(puzzle, solution)
    if hint:
        row, col, val, technique = hint
        print(f"   Hint: Place {val} at row {row+1}, col {col+1}")
        print(f"   Technique: {technique}")
    
    # Validate
    print("\n5. Validating...")
    print(f"   Puzzle valid: {is_valid_puzzle(puzzle)}")
    print(f"   Puzzle solved: {is_solved_puzzle(puzzle)}")
    print(f"   Solution valid: {is_valid_puzzle(solution) if solution else 'N/A'}")
    print(f"   Solution solved: {is_solved_puzzle(solution) if solution else 'N/A'}")
    
    # Format
    print("\n6. Different formats...")
    print(f"   String: {format_puzzle(puzzle, 'string')[:40]}...")
    print(f"   JSON: {format_puzzle(puzzle, 'json')[:40]}...")
    
    print("\n" + "=" * 50)
    print("Demo complete!")