"""
约束满足问题工具模块 (Constraint Satisfaction Utilities)

一个零外部依赖的约束满足问题（CSP）求解器。
"""

from .mod import (
    CSP, CSPSolver, Constraint,
    UnaryConstraint, BinaryConstraint,
    AllDifferentConstraint, AllEqualConstraint,
    SumConstraint, MaxValueConstraint,
    create_n_queens_csp, create_sudoku_csp,
    create_graph_coloring_csp, create_scheduling_csp,
    solve_n_queens, solve_sudoku, solve_graph_coloring,
    count_n_queens_solutions,
    print_n_queens_solution, print_sudoku_solution
)

__all__ = [
    'CSP', 'CSPSolver', 'Constraint',
    'UnaryConstraint', 'BinaryConstraint',
    'AllDifferentConstraint', 'AllEqualConstraint',
    'SumConstraint', 'MaxValueConstraint',
    'create_n_queens_csp', 'create_sudoku_csp',
    'create_graph_coloring_csp', 'create_scheduling_csp',
    'solve_n_queens', 'solve_sudoku', 'solve_graph_coloring',
    'count_n_queens_solutions',
    'print_n_queens_solution', 'print_sudoku_solution'
]