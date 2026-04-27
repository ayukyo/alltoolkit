# Sudoku Utils


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


## 功能

### 类

- **Difficulty**: Sudoku difficulty levels
- **SudokuCell**: Represents a single cell in a Sudoku grid
- **SudokuGrid**: Represents a 9x9 Sudoku grid with full state management
  方法: get, set, get_candidates, is_fixed, get_row ... (10 个方法)
- **SudokuSolver**: Advanced Sudoku solver using multiple techniques
  方法: solve, solve_copy, count_solutions
- **SudokuGenerator**: Sudoku puzzle generator with configurable difficulty
  方法: generate, generate_with_solution
- **SudokuValidator**: Sudoku puzzle validation utilities
  方法: is_valid_grid, is_complete, is_solved, has_unique_solution, is_solvable ... (6 个方法)
- **SudokuHint**: Hint system for Sudoku puzzles
  方法: get_next_cell_hint, get_hint
- **SudokuDifficultyEstimator**: Estimate the difficulty of a Sudoku puzzle
  方法: estimate
- **SudokuFormatter**: Format Sudoku puzzles for display and export
  方法: to_string, from_string, to_pretty_string, to_markdown, to_json ... (7 个方法)

### 函数

- **create_puzzle(difficulty**) - Create a new Sudoku puzzle with specified difficulty.
- **solve_puzzle(grid**) - Solve a Sudoku puzzle and return the solution.
- **is_valid_puzzle(grid**) - Check if a puzzle is valid (no conflicts).
- **is_solved_puzzle(grid**) - Check if a puzzle is completely solved.
- **get_hint(grid, solution**) - Get a hint for the next move.
- **estimate_difficulty(grid**) - Estimate the difficulty of a puzzle.
- **parse_puzzle(s**) - Parse a string into a Sudoku puzzle.
- **format_puzzle(grid, format**) - Format a puzzle for display.
- **get(self, row, col**) - Get the value at a cell.
- **set(self, row, col**, ...) - Set a value at a cell.

... 共 39 个函数

## 使用示例

```python
from mod import create_puzzle

# 使用 create_puzzle
result = create_puzzle()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
