#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minesweeper Utilities - 扫雷游戏工具模块
==========================================

提供完整的扫雷游戏逻辑，包括游戏板生成、雷区计算、安全区域自动揭开、
游戏状态检测等功能。零外部依赖，仅使用 Python 标准库。

功能特性:
    - 多种难度预设（初级、中级、高级、自定义）
    - 随机雷区生成，确保首次点击安全
    - 自动计算周围雷数
    - 洪水填充算法揭开连续安全区域
    - 右键标记旗帜/问号
    - 游戏状态检测（胜利/失败/进行中）
    - 游戏板序列化与反序列化
    - 求解提示（安全格子推荐）
    - 完整的游戏统计

作者: AllToolkit 自动化开发助手
日期: 2026-05-02
版本: 1.0.0
"""

import random
import json
from typing import List, Tuple, Optional, Set, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from copy import deepcopy


# ============================================================================
# 常量定义
# ============================================================================

class CellState(Enum):
    """格子状态"""
    HIDDEN = 0      # 未揭开
    REVEALED = 1    # 已揭开
    FLAGGED = 2     # 已标记旗帜
    QUESTION = 3    # 已标记问号


class GameState(Enum):
    """游戏状态"""
    PLAYING = 0     # 进行中
    WON = 1         # 胜利
    LOST = 2        # 失败


class Difficulty(Enum):
    """难度预设"""
    BEGINNER = (9, 9, 10)       # 初级: 9x9, 10雷
    INTERMEDIATE = (16, 16, 40) # 中级: 16x16, 40雷
    EXPERT = (30, 16, 99)       # 高级: 30x16, 99雷
    CUSTOM = (0, 0, 0)          # 自定义


# 方向偏移量（8个相邻格子）
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class Cell:
    """单个格子"""
    is_mine: bool = False           # 是否是雷
    adjacent_mines: int = 0         # 周围雷数
    state: CellState = CellState.HIDDEN  # 当前状态


@dataclass
class GameStats:
    """游戏统计"""
    total_cells: int = 0            # 总格子数
    total_mines: int = 0            # 总雷数
    revealed_cells: int = 0         # 已揭开格子数
    flagged_cells: int = 0         # 已标记格子数
    start_time: float = 0.0         # 开始时间
    end_time: float = 0.0           # 结束时间
    clicks: int = 0                 # 点击次数
    first_click: bool = True        # 是否首次点击


@dataclass
class GameBoard:
    """游戏板"""
    rows: int                       # 行数
    cols: int                       # 列数
    mines: int                      # 雷数
    board: List[List[Cell]] = field(default_factory=list)  # 格子矩阵
    state: GameState = GameState.PLAYING  # 游戏状态
    stats: GameStats = field(default_factory=GameStats)    # 游戏统计
    _mine_positions: Set[Tuple[int, int]] = field(default_factory=set)  # 雷位置集合
    
    def __post_init__(self):
        """初始化游戏板"""
        if not self.board:
            self.board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
            self.stats.total_cells = self.rows * self.cols
            self.stats.total_mines = self.mines


# ============================================================================
# 游戏板创建
# ============================================================================

def create_board(rows: int, cols: int, mines: int) -> GameBoard:
    """
    创建新的游戏板。
    
    Args:
        rows: 行数
        cols: 列数
        mines: 雷数
    
    Returns:
        新的游戏板实例
    
    Raises:
        ValueError: 如果参数无效
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> board.rows
        9
        >>> board.mines
        10
    """
    # 参数验证
    if rows < 1 or cols < 1:
        raise ValueError("行数和列数必须大于0")
    if mines < 0:
        raise ValueError("雷数不能为负数")
    if mines >= rows * cols:
        raise ValueError("雷数必须小于总格子数")
    
    return GameBoard(rows=rows, cols=cols, mines=mines)


def create_board_from_difficulty(difficulty: Difficulty) -> GameBoard:
    """
    根据难度创建游戏板。
    
    Args:
        difficulty: 难度级别
    
    Returns:
        新的游戏板实例
    
    Examples:
        >>> board = create_board_from_difficulty(Difficulty.BEGINNER)
        >>> board.rows, board.cols, board.mines
        (9, 9, 10)
    """
    if difficulty == Difficulty.CUSTOM:
        raise ValueError("自定义难度需要使用 create_board() 函数")
    
    rows, cols, mines = difficulty.value
    return create_board(rows, cols, mines)


# ============================================================================
# 雷区生成
# ============================================================================

def place_mines(board: GameBoard, safe_row: int, safe_col: int) -> None:
    """
    放置雷区，确保首次点击位置安全。
    
    Args:
        board: 游戏板
        safe_row: 安全行（首次点击位置）
        safe_col: 安全列（首次点击位置）
    
    Note:
        此函数会修改游戏板状态。首次点击位置及其周围8格都不会有雷。
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> place_mines(board, 4, 4)
        >>> len(board._mine_positions)
        10
    """
    # 计算安全区域（首次点击位置及其周围）
    safe_positions: Set[Tuple[int, int]] = set()
    for dr, dc in DIRECTIONS:
        nr, nc = safe_row + dr, safe_col + dc
        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            safe_positions.add((nr, nc))
    safe_positions.add((safe_row, safe_col))
    
    # 计算可用位置
    available_positions = [
        (r, c) 
        for r in range(board.rows) 
        for c in range(board.cols)
        if (r, c) not in safe_positions
    ]
    
    # 如果可用位置不足，调整雷数
    actual_mines = min(board.mines, len(available_positions))
    
    # 随机选择雷位置
    mine_positions = random.sample(available_positions, actual_mines)
    board._mine_positions = set(mine_positions)
    
    # 放置雷
    for r, c in mine_positions:
        board.board[r][c].is_mine = True
    
    # 计算周围雷数
    _calculate_adjacent_mines(board)


def _calculate_adjacent_mines(board: GameBoard) -> None:
    """计算每个格子周围的雷数"""
    for r in range(board.rows):
        for c in range(board.cols):
            if board.board[r][c].is_mine:
                continue
            
            count = 0
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.rows and 0 <= nc < board.cols:
                    if board.board[nr][nc].is_mine:
                        count += 1
            
            board.board[r][c].adjacent_mines = count


# ============================================================================
# 游戏操作
# ============================================================================

def reveal_cell(board: GameBoard, row: int, col: int) -> List[Tuple[int, int]]:
    """
    揭开指定格子。
    
    Args:
        board: 游戏板
        row: 行索引
        col: 列索引
    
    Returns:
        被揭开的格子坐标列表
    
    Raises:
        ValueError: 如果坐标越界或格子已揭开/已标记
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> place_mines(board, 4, 4)
        >>> revealed = reveal_cell(board, 4, 4)
        >>> len(revealed) > 0
        True
    """
    # 边界检查
    if not (0 <= row < board.rows and 0 <= col < board.cols):
        raise ValueError(f"坐标越界: ({row}, {col})")
    
    # 游戏状态检查
    if board.state != GameState.PLAYING:
        return []
    
    cell = board.board[row][col]
    
    # 状态检查
    if cell.state == CellState.REVEALED:
        return []
    if cell.state == CellState.FLAGGED:
        return []
    
    revealed_cells: List[Tuple[int, int]] = []
    
    # 首次点击时放置雷
    if board.stats.first_click:
        board.stats.first_click = False
        place_mines(board, row, col)
    
    # 点击计数
    board.stats.clicks += 1
    
    # 如果踩雷
    if cell.is_mine:
        cell.state = CellState.REVEALED
        board.state = GameState.LOST
        revealed_cells.append((row, col))
        # 揭开所有雷
        for r, c in board._mine_positions:
            board.board[r][c].state = CellState.REVEALED
        return revealed_cells
    
    # 洪水填充揭开安全区域
    _flood_fill_reveal(board, row, col, revealed_cells)
    
    # 更新统计
    board.stats.revealed_cells = sum(
        1 for r in range(board.rows) 
        for c in range(board.cols) 
        if board.board[r][c].state == CellState.REVEALED
    )
    
    # 检查胜利
    _check_win(board)
    
    return revealed_cells


def _flood_fill_reveal(board: GameBoard, row: int, col: int, 
                       revealed: List[Tuple[int, int]]) -> None:
    """洪水填充算法揭开连续安全区域"""
    # 边界检查
    if not (0 <= row < board.rows and 0 <= col < board.cols):
        return
    
    cell = board.board[row][col]
    
    # 已揭开或已标记
    if cell.state != CellState.HIDDEN:
        return
    
    # 是雷
    if cell.is_mine:
        return
    
    # 揭开
    cell.state = CellState.REVEALED
    revealed.append((row, col))
    
    # 如果周围没有雷，继续揭开相邻格子
    if cell.adjacent_mines == 0:
        for dr, dc in DIRECTIONS:
            _flood_fill_reveal(board, row + dr, col + dc, revealed)


def toggle_flag(board: GameBoard, row: int, col: int) -> CellState:
    """
    切换标记状态（隐藏 -> 旗帜 -> 问号 -> 隐藏）。
    
    Args:
        board: 游戏板
        row: 行索引
        col: 列索引
    
    Returns:
        新的格子状态
    
    Raises:
        ValueError: 如果坐标越界
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> new_state = toggle_flag(board, 0, 0)
        >>> new_state == CellState.FLAGGED
        True
    """
    if not (0 <= row < board.rows and 0 <= col < board.cols):
        raise ValueError(f"坐标越界: ({row}, {col})")
    
    cell = board.board[row][col]
    
    if cell.state == CellState.REVEALED:
        return cell.state
    
    # 循环切换状态
    if cell.state == CellState.HIDDEN:
        cell.state = CellState.FLAGGED
        board.stats.flagged_cells += 1
    elif cell.state == CellState.FLAGGED:
        cell.state = CellState.QUESTION
        board.stats.flagged_cells -= 1
    else:  # QUESTION
        cell.state = CellState.HIDDEN
    
    return cell.state


def set_flag(board: GameBoard, row: int, col: int, state: CellState) -> None:
    """
    设置指定格子的标记状态。
    
    Args:
        board: 游戏板
        row: 行索引
        col: 列索引
        state: 目标状态
    
    Raises:
        ValueError: 如果坐标越界或状态无效
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> set_flag(board, 0, 0, CellState.FLAGGED)
        >>> board.board[0][0].state == CellState.FLAGGED
        True
    """
    if not (0 <= row < board.rows and 0 <= col < board.cols):
        raise ValueError(f"坐标越界: ({row}, {col})")
    
    cell = board.board[row][col]
    
    if cell.state == CellState.REVEALED:
        return
    
    # 更新旗帜计数
    if state == CellState.FLAGGED and cell.state != CellState.FLAGGED:
        board.stats.flagged_cells += 1
    elif state != CellState.FLAGGED and cell.state == CellState.FLAGGED:
        board.stats.flagged_cells -= 1
    
    cell.state = state


def _check_win(board: GameBoard) -> None:
    """检查是否胜利"""
    # 计算非雷格子数
    non_mine_cells = board.rows * board.cols - board.mines
    
    # 计算已揭开的非雷格子数
    revealed_non_mines = sum(
        1 for r in range(board.rows)
        for c in range(board.cols)
        if board.board[r][c].state == CellState.REVEALED 
        and not board.board[r][c].is_mine
    )
    
    if revealed_non_mines == non_mine_cells:
        board.state = GameState.WON


# ============================================================================
# 快捷操作
# ============================================================================

def chord_reveal(board: GameBoard, row: int, col: int) -> List[Tuple[int, int]]:
    """
    双击操作：如果周围旗帜数等于雷数，揭开周围未标记格子。
    
    Args:
        board: 游戏板
        row: 行索引
        col: 列索引
    
    Returns:
        被揭开的格子坐标列表
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> place_mines(board, 4, 4)
        >>> reveal_cell(board, 4, 4)
        []
        >>> chord_reveal(board, 4, 4)  # 尝试双击
        []
    """
    if not (0 <= row < board.rows and 0 <= col < board.cols):
        return []
    
    cell = board.board[row][col]
    
    # 只有已揭开的格子可以双击
    if cell.state != CellState.REVEALED:
        return []
    
    # 如果是雷或周围没有雷，不能双击
    if cell.is_mine or cell.adjacent_mines == 0:
        return []
    
    # 计算周围旗帜数
    flagged_count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            if board.board[nr][nc].state == CellState.FLAGGED:
                flagged_count += 1
    
    # 如果旗帜数不等于雷数，不能双击
    if flagged_count != cell.adjacent_mines:
        return []
    
    # 揭开周围未标记格子
    revealed: List[Tuple[int, int]] = []
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            neighbor = board.board[nr][nc]
            if neighbor.state == CellState.HIDDEN:
                # 揭开该格子
                if neighbor.is_mine:
                    # 踩雷，游戏结束
                    neighbor.state = CellState.REVEALED
                    board.state = GameState.LOST
                    revealed.append((nr, nc))
                    for r, c in board._mine_positions:
                        board.board[r][c].state = CellState.REVEALED
                    return revealed
                else:
                    _flood_fill_reveal(board, nr, nc, revealed)
    
    # 更新统计
    board.stats.revealed_cells = sum(
        1 for r in range(board.rows) 
        for c in range(board.cols) 
        if board.board[r][c].state == CellState.REVEALED
    )
    
    # 检查胜利
    _check_win(board)
    
    return revealed


# ============================================================================
# 游戏状态查询
# ============================================================================

def get_game_state(board: GameBoard) -> GameState:
    """
    获取当前游戏状态。
    
    Args:
        board: 游戏板
    
    Returns:
        游戏状态
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> get_game_state(board) == GameState.PLAYING
        True
    """
    return board.state


def is_game_over(board: GameBoard) -> bool:
    """
    检查游戏是否结束。
    
    Args:
        board: 游戏板
    
    Returns:
        是否结束
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> is_game_over(board)
        False
    """
    return board.state in (GameState.WON, GameState.LOST)


def is_won(board: GameBoard) -> bool:
    """
    检查是否胜利。
    
    Args:
        board: 游戏板
    
    Returns:
        是否胜利
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> is_won(board)
        False
    """
    return board.state == GameState.WON


def is_lost(board: GameBoard) -> bool:
    """
    检查是否失败。
    
    Args:
        board: 游戏板
    
    Returns:
        是否失败
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> is_lost(board)
        False
    """
    return board.state == GameState.LOST


def get_remaining_mines(board: GameBoard) -> int:
    """
    获取剩余雷数（总雷数 - 已标记旗帜数）。
    
    Args:
        board: 游戏板
    
    Returns:
        剩余雷数
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> get_remaining_mines(board)
        10
        >>> toggle_flag(board, 0, 0)
        <CellState.FLAGGED: 2>
        >>> get_remaining_mines(board)
        9
    """
    return board.mines - board.stats.flagged_cells


def get_progress(board: GameBoard) -> float:
    """
    获取游戏进度（0.0 - 1.0）。
    
    Args:
        board: 游戏板
    
    Returns:
        完成进度
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> get_progress(board)
        0.0
    """
    non_mine_cells = board.rows * board.cols - board.mines
    if non_mine_cells == 0:
        return 1.0
    return board.stats.revealed_cells / non_mine_cells


# ============================================================================
# 游戏板可视化
# ============================================================================

def board_to_string(board: GameBoard, show_mines: bool = False) -> str:
    """
    将游戏板转换为字符串表示。
    
    Args:
        board: 游戏板
        show_mines: 是否显示雷（调试模式）
    
    Returns:
        游戏板的字符串表示
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> print(board_to_string(board, show_mines=False))
        ┌───┬───┬───┐
        │ ? │ ? │ ? │
        ├───┼───┼───┤
        │ ? │ ? │ ? │
        ├───┼───┼───┤
        │ ? │ ? │ ? │
        └───┴───┴───┘
    """
    # 格子符号映射
    symbols = {
        CellState.HIDDEN: '?',
        CellState.REVEALED: '.',  # 会被实际数字替换
        CellState.FLAGGED: '⚑',
        CellState.QUESTION: '?',
    }
    
    # 构建字符串
    lines: List[str] = []
    
    # 顶边框
    top_border = '┌' + '┬'.join(['───'] * board.cols) + '┐'
    lines.append(top_border)
    
    for r in range(board.rows):
        row_parts = []
        for c in range(board.cols):
            cell = board.board[r][c]
            
            if cell.state == CellState.REVEALED:
                if cell.is_mine:
                    row_parts.append(' 💣' if show_mines else ' ? ')
                elif cell.adjacent_mines == 0:
                    row_parts.append('   ')
                else:
                    row_parts.append(f' {cell.adjacent_mines} ')
            elif cell.state == CellState.FLAGGED:
                row_parts.append(' ⚑ ')
            elif cell.state == CellState.QUESTION:
                row_parts.append(' ? ')
            else:
                if show_mines and cell.is_mine:
                    row_parts.append(' * ')
                else:
                    row_parts.append(' ? ')
        
        lines.append('│' + '│'.join(row_parts) + '│')
        
        # 中间边框或底边框
        if r < board.rows - 1:
            mid_border = '├' + '┼'.join(['───'] * board.cols) + '┤'
            lines.append(mid_border)
    
    # 底边框
    bottom_border = '└' + '┴'.join(['───'] * board.cols) + '┘'
    lines.append(bottom_border)
    
    return '\n'.join(lines)


def board_to_emoji(board: GameBoard, show_mines: bool = False) -> str:
    """
    将游戏板转换为 Emoji 表示。
    
    Args:
        board: 游戏板
        show_mines: 是否显示雷（调试模式）
    
    Returns:
        游戏板的 Emoji 表示
    
    Examples:
        >>> board = create_board(2, 2, 1)
        >>> result = board_to_emoji(board)
        >>> '⬜' in result
        True
    """
    emoji_map = {
        'hidden': '⬜',
        'mine': '💣',
        'flag': '🚩',
        'question': '❓',
        '0': '⬜',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
    }
    
    lines: List[str] = []
    
    for r in range(board.rows):
        row_str = ''
        for c in range(board.cols):
            cell = board.board[r][c]
            
            if cell.state == CellState.REVEALED:
                if cell.is_mine:
                    row_str += emoji_map['mine']
                else:
                    row_str += emoji_map.get(str(cell.adjacent_mines), emoji_map['0'])
            elif cell.state == CellState.FLAGGED:
                row_str += emoji_map['flag']
            elif cell.state == CellState.QUESTION:
                row_str += emoji_map['question']
            else:
                if show_mines and cell.is_mine:
                    row_str += emoji_map['mine']
                else:
                    row_str += emoji_map['hidden']
        
        lines.append(row_str)
    
    return '\n'.join(lines)


# ============================================================================
# 序列化与反序列化
# ============================================================================

def serialize_board(board: GameBoard) -> str:
    """
    将游戏板序列化为 JSON 字符串。
    
    Args:
        board: 游戏板
    
    Returns:
        JSON 字符串
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> json_str = serialize_board(board)
        >>> '"rows": 3' in json_str
        True
    """
    data = {
        'rows': board.rows,
        'cols': board.cols,
        'mines': board.mines,
        'state': board.state.value,
        'stats': {
            'total_cells': board.stats.total_cells,
            'total_mines': board.stats.total_mines,
            'revealed_cells': board.stats.revealed_cells,
            'flagged_cells': board.stats.flagged_cells,
            'clicks': board.stats.clicks,
            'first_click': board.stats.first_click,
        },
        'board': [
            [
                {
                    'is_mine': cell.is_mine,
                    'adjacent_mines': cell.adjacent_mines,
                    'state': cell.state.value,
                }
                for cell in row
            ]
            for row in board.board
        ],
        'mine_positions': list(board._mine_positions),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def deserialize_board(json_str: str) -> GameBoard:
    """
    从 JSON 字符串反序列化游戏板。
    
    Args:
        json_str: JSON 字符串
    
    Returns:
        游戏板实例
    
    Raises:
        ValueError: 如果 JSON 格式无效
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> json_str = serialize_board(board)
        >>> restored = deserialize_board(json_str)
        >>> restored.rows == board.rows
        True
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"无效的 JSON 格式: {e}")
    
    board = GameBoard(
        rows=data['rows'],
        cols=data['cols'],
        mines=data['mines'],
        state=GameState(data['state']),
        stats=GameStats(
            total_cells=data['stats']['total_cells'],
            total_mines=data['stats']['total_mines'],
            revealed_cells=data['stats']['revealed_cells'],
            flagged_cells=data['stats']['flagged_cells'],
            clicks=data['stats']['clicks'],
            first_click=data['stats']['first_click'],
        ),
    )
    
    # 恢复格子状态
    for r, row_data in enumerate(data['board']):
        for c, cell_data in enumerate(row_data):
            board.board[r][c] = Cell(
                is_mine=cell_data['is_mine'],
                adjacent_mines=cell_data['adjacent_mines'],
                state=CellState(cell_data['state']),
            )
    
    # 恢复雷位置
    board._mine_positions = set(tuple(pos) for pos in data['mine_positions'])
    
    return board


# ============================================================================
# 求解辅助
# ============================================================================

def get_safe_cells(board: GameBoard) -> List[Tuple[int, int]]:
    """
    获取确定安全的格子列表。
    
    使用约束满足方法分析已揭开格子，找出确定安全的格子。
    
    Args:
        board: 游戏板
    
    Returns:
        安全格子坐标列表
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> place_mines(board, 1, 1)
        >>> reveal_cell(board, 0, 0)
        [(0, 0)]
        >>> safe = get_safe_cells(board)
        >>> isinstance(safe, list)
        True
    """
    safe_cells: List[Tuple[int, int]] = []
    
    # 如果还未放置雷，所有格子都是潜在安全的
    if board.stats.first_click:
        return [(r, c) for r in range(board.rows) for c in range(board.cols)]
    
    # 遍历所有已揭开的格子
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.board[r][c]
            
            if cell.state != CellState.REVEALED:
                continue
            
            if cell.is_mine or cell.adjacent_mines == 0:
                continue
            
            # 计算周围隐藏格子和旗帜数
            hidden_neighbors = []
            flagged_count = 0
            
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.rows and 0 <= nc < board.cols:
                    neighbor = board.board[nr][nc]
                    if neighbor.state == CellState.HIDDEN:
                        hidden_neighbors.append((nr, nc))
                    elif neighbor.state == CellState.FLAGGED:
                        flagged_count += 1
            
            # 如果旗帜数等于雷数，所有隐藏邻居都是安全的
            if flagged_count == cell.adjacent_mines:
                safe_cells.extend(hidden_neighbors)
    
    return list(set(safe_cells))


def get_mine_cells(board: GameBoard) -> List[Tuple[int, int]]:
    """
    获取确定是雷的格子列表。
    
    使用约束满足方法分析已揭开格子，找出确定是雷的格子。
    
    Args:
        board: 游戏板
    
    Returns:
        雷格子坐标列表
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> place_mines(board, 1, 1)
        >>> mines = get_mine_cells(board)
        >>> isinstance(mines, list)
        True
    """
    mine_cells: List[Tuple[int, int]] = []
    
    # 如果还未放置雷，无法确定
    if board.stats.first_click:
        return []
    
    # 遍历所有已揭开的格子
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.board[r][c]
            
            if cell.state != CellState.REVEALED:
                continue
            
            if cell.is_mine or cell.adjacent_mines == 0:
                continue
            
            # 计算周围隐藏格子数和旗帜数
            hidden_neighbors = []
            flagged_count = 0
            
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.rows and 0 <= nc < board.cols:
                    neighbor = board.board[nr][nc]
                    if neighbor.state == CellState.HIDDEN:
                        hidden_neighbors.append((nr, nc))
                    elif neighbor.state == CellState.FLAGGED:
                        flagged_count += 1
            
            # 如果隐藏格子数 + 旗帜数 == 雷数，所有隐藏邻居都是雷
            remaining_mines = cell.adjacent_mines - flagged_count
            if len(hidden_neighbors) == remaining_mines and remaining_mines > 0:
                mine_cells.extend(hidden_neighbors)
    
    return list(set(mine_cells))


def get_hint(board: GameBoard) -> Optional[Tuple[int, int, str]]:
    """
    获取游戏提示。
    
    分析当前游戏状态，返回一个安全格子或需要标记的雷。
    
    Args:
        board: 游戏板
    
    Returns:
        (行, 列, 提示类型) 或 None（如果无提示）
        提示类型: 'safe' 表示安全格子, 'mine' 表示雷
    
    Examples:
        >>> board = create_board(3, 3, 1)
        >>> hint = get_hint(board)
        >>> hint is not None
        True
    """
    # 优先返回安全格子
    safe = get_safe_cells(board)
    if safe:
        return safe[0][0], safe[0][1], 'safe'
    
    # 然后返回确定的雷
    mines = get_mine_cells(board)
    if mines:
        return mines[0][0], mines[0][1], 'mine'
    
    # 如果没有确定的结果，随机选择一个隐藏格子
    for r in range(board.rows):
        for c in range(board.cols):
            if board.board[r][c].state == CellState.HIDDEN:
                return r, c, 'guess'
    
    return None


# ============================================================================
# 统计分析
# ============================================================================

def get_statistics(board: GameBoard) -> Dict[str, Any]:
    """
    获取游戏统计信息。
    
    Args:
        board: 游戏板
    
    Returns:
        统计信息字典
    
    Examples:
        >>> board = create_board(9, 9, 10)
        >>> stats = get_statistics(board)
        >>> stats['total_cells']
        81
    """
    hidden_count = sum(
        1 for r in range(board.rows)
        for c in range(board.cols)
        if board.board[r][c].state == CellState.HIDDEN
    )
    
    flagged_count = sum(
        1 for r in range(board.rows)
        for c in range(board.cols)
        if board.board[r][c].state == CellState.FLAGGED
    )
    
    question_count = sum(
        1 for r in range(board.rows)
        for c in range(board.cols)
        if board.board[r][c].state == CellState.QUESTION
    )
    
    revealed_count = sum(
        1 for r in range(board.rows)
        for c in range(board.cols)
        if board.board[r][c].state == CellState.REVEALED
    )
    
    return {
        'rows': board.rows,
        'cols': board.cols,
        'total_cells': board.stats.total_cells,
        'total_mines': board.stats.total_mines,
        'hidden_cells': hidden_count,
        'revealed_cells': revealed_count,
        'flagged_cells': flagged_count,
        'question_cells': question_count,
        'remaining_mines': get_remaining_mines(board),
        'progress': get_progress(board),
        'clicks': board.stats.clicks,
        'game_state': board.state.name,
        'first_click': board.stats.first_click,
    }


# ============================================================================
# 完整游戏流程
# ============================================================================

def new_game(difficulty: Difficulty = Difficulty.BEGINNER, 
             rows: int = 0, cols: int = 0, mines: int = 0) -> GameBoard:
    """
    开始新游戏。
    
    Args:
        difficulty: 难度级别
        rows: 自定义行数（仅当 difficulty 为 CUSTOM 时使用）
        cols: 自定义列数（仅当 difficulty 为 CUSTOM 时使用）
        mines: 自定义雷数（仅当 difficulty 为 CUSTOM 时使用）
    
    Returns:
        新的游戏板
    
    Examples:
        >>> board = new_game(Difficulty.BEGINNER)
        >>> board.rows
        9
        >>> board = new_game(Difficulty.CUSTOM, rows=20, cols=20, mines=50)
        >>> board.rows
        20
    """
    if difficulty == Difficulty.CUSTOM:
        return create_board(rows, cols, mines)
    return create_board_from_difficulty(difficulty)


def make_move(board: GameBoard, row: int, col: int, 
              action: str = 'reveal') -> Dict[str, Any]:
    """
    执行游戏操作。
    
    Args:
        board: 游戏板
        row: 行索引
        col: 列索引
        action: 操作类型 ('reveal', 'flag', 'chord')
    
    Returns:
        操作结果字典
    
    Examples:
        >>> board = new_game(Difficulty.BEGINNER)
        >>> result = make_move(board, 4, 4, 'reveal')
        >>> 'revealed' in result
        True
    """
    result = {
        'action': action,
        'row': row,
        'col': col,
        'success': False,
        'revealed': [],
        'game_state': board.state.name,
        'message': '',
    }
    
    try:
        if action == 'reveal':
            revealed = reveal_cell(board, row, col)
            result['revealed'] = revealed
            result['success'] = True
            result['message'] = f'揭开了 {len(revealed)} 个格子'
        
        elif action == 'flag':
            new_state = toggle_flag(board, row, col)
            result['success'] = True
            result['message'] = f'标记状态: {new_state.name}'
        
        elif action == 'chord':
            revealed = chord_reveal(board, row, col)
            result['revealed'] = revealed
            result['success'] = True
            result['message'] = f'双击揭开了 {len(revealed)} 个格子'
        
        else:
            result['message'] = f'未知操作: {action}'
        
    except ValueError as e:
        result['message'] = str(e)
    
    result['game_state'] = board.state.name
    result['statistics'] = get_statistics(board)
    
    return result


# ============================================================================
# 主函数
# ============================================================================

if __name__ == '__main__':
    # 演示代码
    print("=" * 50)
    print("扫雷游戏工具模块 - 演示")
    print("=" * 50)
    
    # 创建初级难度游戏
    board = new_game(Difficulty.BEGINNER)
    print(f"\n游戏板大小: {board.rows}x{board.cols}, 雷数: {board.mines}")
    
    # 显示初始状态
    print("\n初始游戏板:")
    print(board_to_string(board))
    
    # 第一次点击（中间位置）
    print("\n点击 (4, 4)...")
    result = make_move(board, 4, 4, 'reveal')
    print(f"揭开格子数: {len(result['revealed'])}")
    
    # 显示点击后状态
    print("\n点击后游戏板:")
    print(board_to_emoji(board))
    
    # 显示统计
    print("\n游戏统计:")
    stats = get_statistics(board)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 获取提示
    hint = get_hint(board)
    if hint:
        print(f"\n提示: 位置 ({hint[0]}, {hint[1]}) - {hint[2]}")
    
    # 序列化测试
    print("\n序列化测试:")
    json_str = serialize_board(board)
    restored = deserialize_board(json_str)
    print(f"序列化/反序列化成功: {restored.rows == board.rows}")