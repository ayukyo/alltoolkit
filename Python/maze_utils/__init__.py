"""
Maze Utilities - 迷宫生成与求解工具
=====================================

提供多种迷宫生成算法和求解算法，零外部依赖。

功能：
- 迷宫生成：DFS、Prim、Kruskal、递归分割等算法
- 迷宫求解：BFS、DFS、A*、墙跟随等算法
- 迷宫可视化：ASCII、Unicode、JSON格式
- 迷宫验证与操作

作者：AllToolkit 自动化生成
日期：2026-04-20
"""

from .maze import Maze, Cell, Direction
from .generator import (
    generate_dfs,
    generate_prim,
    generate_kruskal,
    generate_recursive_division,
    generate_ellers,
    generate_binary_tree,
)
from .solver import (
    solve_bfs,
    solve_dfs,
    solve_astar,
    solve_wall_follower,
    solve_dead_end_filling,
)
from .renderer import render_ascii, render_unicode, render_path
from .serializer import (
    to_json,
    from_json,
    to_dict,
    from_dict,
    to_binary,
    from_binary,
    to_csv,
    save_to_file,
    load_from_file,
)

__all__ = [
    # Core classes
    'Maze',
    'Cell',
    'Direction',
    # Generators
    'generate_dfs',
    'generate_prim',
    'generate_kruskal',
    'generate_recursive_division',
    'generate_ellers',
    'generate_binary_tree',
    # Solvers
    'solve_bfs',
    'solve_dfs',
    'solve_astar',
    'solve_wall_follower',
    'solve_dead_end_filling',
    # Renderers
    'render_ascii',
    'render_unicode',
    'render_path',
    # Serializers
    'to_json',
    'from_json',
    'to_dict',
    'from_dict',
    'to_binary',
    'from_binary',
    'to_csv',
    'save_to_file',
    'load_from_file',
]

__version__ = '1.0.0'