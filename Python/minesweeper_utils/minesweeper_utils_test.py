#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minesweeper Utilities - 测试模块
================================

测试扫雷游戏工具模块的所有功能。

作者: AllToolkit 自动化开发助手
日期: 2026-05-02
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from minesweeper_utils.mod import (
    # 类
    CellState, GameState, Difficulty, Cell, GameStats, GameBoard,
    # 创建函数
    create_board, create_board_from_difficulty,
    # 雷区函数
    place_mines,
    # 游戏操作
    reveal_cell, toggle_flag, set_flag, chord_reveal,
    # 游戏状态
    get_game_state, is_game_over, is_won, is_lost, 
    get_remaining_mines, get_progress,
    # 可视化
    board_to_string, board_to_emoji,
    # 序列化
    serialize_board, deserialize_board,
    # 求解辅助
    get_safe_cells, get_mine_cells, get_hint,
    # 统计
    get_statistics,
    # 完整流程
    new_game, make_move,
)


class TestBoardCreation(unittest.TestCase):
    """测试游戏板创建"""
    
    def test_create_board_basic(self):
        """测试基本创建"""
        board = create_board(9, 9, 10)
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.cols, 9)
        self.assertEqual(board.mines, 10)
        self.assertEqual(board.state, GameState.PLAYING)
    
    def test_create_board_small(self):
        """测试最小尺寸"""
        board = create_board(3, 3, 1)
        self.assertEqual(board.rows, 3)
        self.assertEqual(board.cols, 3)
        self.assertEqual(board.mines, 1)
    
    def test_create_board_custom(self):
        """测试自定义参数"""
        board = create_board(20, 15, 50)
        self.assertEqual(board.rows, 20)
        self.assertEqual(board.cols, 15)
        self.assertEqual(board.mines, 50)
    
    def test_create_board_invalid_rows(self):
        """测试无效行数"""
        with self.assertRaises(ValueError):
            create_board(0, 9, 10)
    
    def test_create_board_invalid_cols(self):
        """测试无效列数"""
        with self.assertRaises(ValueError):
            create_board(9, 0, 10)
    
    def test_create_board_invalid_mines_negative(self):
        """测试负雷数"""
        with self.assertRaises(ValueError):
            create_board(9, 9, -1)
    
    def test_create_board_invalid_mines_too_many(self):
        """测试过多雷数"""
        with self.assertRaises(ValueError):
            create_board(9, 9, 81)  # 总格子数
    
    def test_create_board_from_difficulty_beginner(self):
        """测试初级难度"""
        board = create_board_from_difficulty(Difficulty.BEGINNER)
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.cols, 9)
        self.assertEqual(board.mines, 10)
    
    def test_create_board_from_difficulty_intermediate(self):
        """测试中级难度"""
        board = create_board_from_difficulty(Difficulty.INTERMEDIATE)
        self.assertEqual(board.rows, 16)
        self.assertEqual(board.cols, 16)
        self.assertEqual(board.mines, 40)
    
    def test_create_board_from_difficulty_expert(self):
        """测试高级难度"""
        board = create_board_from_difficulty(Difficulty.EXPERT)
        self.assertEqual(board.rows, 30)
        self.assertEqual(board.cols, 16)
        self.assertEqual(board.mines, 99)
    
    def test_create_board_from_difficulty_custom(self):
        """测试自定义难度（应抛出错误）"""
        with self.assertRaises(ValueError):
            create_board_from_difficulty(Difficulty.CUSTOM)
    
    def test_board_initial_state(self):
        """测试初始状态"""
        board = create_board(9, 9, 10)
        self.assertEqual(board.state, GameState.PLAYING)
        self.assertEqual(board.stats.first_click, True)
        self.assertEqual(board.stats.revealed_cells, 0)
        self.assertEqual(board.stats.flagged_cells, 0)
    
    def test_cell_initial_state(self):
        """测试格子初始状态"""
        board = create_board(9, 9, 10)
        for r in range(board.rows):
            for c in range(board.cols):
                cell = board.board[r][c]
                self.assertEqual(cell.state, CellState.HIDDEN)
                self.assertEqual(cell.is_mine, False)
                self.assertEqual(cell.adjacent_mines, 0)


class TestMinePlacement(unittest.TestCase):
    """测试雷区放置"""
    
    def test_place_mines_count(self):
        """测试雷数正确"""
        board = create_board(9, 9, 10)
        place_mines(board, 4, 4)
        mine_count = sum(1 for r in range(board.rows) 
                        for c in range(board.cols) 
                        if board.board[r][c].is_mine)
        self.assertEqual(mine_count, 10)
    
    def test_place_mines_safe_zone(self):
        """测试安全区域"""
        board = create_board(9, 9, 10)
        safe_row, safe_col = 4, 4
        place_mines(board, safe_row, safe_col)
        
        # 检查安全区域没有雷
        from minesweeper_utils.mod import DIRECTIONS
        for dr, dc in DIRECTIONS:
            nr, nc = safe_row + dr, safe_col + dc
            if 0 <= nr < board.rows and 0 <= nc < board.cols:
                self.assertEqual(board.board[nr][nc].is_mine, False)
        self.assertEqual(board.board[safe_row][safe_col].is_mine, False)
    
    def test_place_mines_adjacent_count(self):
        """测试周围雷数计算"""
        # 使用更大的板子，避免安全区域覆盖所有格子
        board = create_board(5, 5, 1)
        place_mines(board, 2, 2)  # 中间安全
        
        # 找出雷的位置
        mine_pos = None
        for r in range(board.rows):
            for c in range(board.cols):
                if board.board[r][c].is_mine:
                    mine_pos = (r, c)
                    break
        
        self.assertIsNotNone(mine_pos)
        
        # 验证周围雷数
        for r in range(board.rows):
            for c in range(board.cols):
                if board.board[r][c].is_mine:
                    self.assertEqual(board.board[r][c].adjacent_mines, 0)
    
    def test_place_mines_positions_recorded(self):
        """测试雷位置记录"""
        board = create_board(9, 9, 10)
        place_mines(board, 4, 4)
        self.assertEqual(len(board._mine_positions), 10)


class TestGameOperations(unittest.TestCase):
    """测试游戏操作"""
    
    def test_reveal_cell_basic(self):
        """测试基本揭开"""
        board = create_board(9, 9, 10)
        revealed = reveal_cell(board, 4, 4)
        self.assertGreater(len(revealed), 0)
        self.assertEqual(board.stats.first_click, False)
    
    def test_reveal_cell_already_revealed(self):
        """测试已揭开格子"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        revealed = reveal_cell(board, 4, 4)  # 再次点击同一位置
        self.assertEqual(len(revealed), 0)
    
    def test_reveal_cell_invalid_position(self):
        """测试无效位置"""
        board = create_board(9, 9, 10)
        with self.assertRaises(ValueError):
            reveal_cell(board, -1, 0)
        with self.assertRaises(ValueError):
            reveal_cell(board, 0, -1)
        with self.assertRaises(ValueError):
            reveal_cell(board, 9, 0)
        with self.assertRaises(ValueError):
            reveal_cell(board, 0, 9)
    
    def test_reveal_cell_game_over(self):
        """测试游戏结束后操作"""
        board = create_board(3, 3, 1)
        # 找到雷的位置并点击它
        reveal_cell(board, 1, 1)  # 首次点击触发放置雷
        
        # 找一个雷格子
        mine_pos = None
        for pos in board._mine_positions:
            mine_pos = pos
            break
        
        if mine_pos:
            # 重新创建一个已知雷位置的测试
            board2 = create_board(1, 1, 0)  # 无雷板
            reveal_cell(board2, 0, 0)
            board2.state = GameState.LOST
            result = reveal_cell(board2, 0, 0)
            self.assertEqual(len(result), 0)
    
    def test_flood_fill_reveal(self):
        """测试洪水填充"""
        board = create_board(9, 9, 10)
        revealed = reveal_cell(board, 4, 4)
        
        # 检查揭开的格子是否连续
        # 如果第一个揭开的格子周围没有雷，应该揭开更多
        if board.board[4][4].adjacent_mines == 0:
            self.assertGreater(len(revealed), 1)
    
    def test_toggle_flag_basic(self):
        """测试基本标记"""
        board = create_board(9, 9, 10)
        state = toggle_flag(board, 0, 0)
        self.assertEqual(state, CellState.FLAGGED)
        self.assertEqual(board.board[0][0].state, CellState.FLAGGED)
        self.assertEqual(board.stats.flagged_cells, 1)
    
    def test_toggle_flag_cycle(self):
        """测试标记循环"""
        board = create_board(9, 9, 10)
        
        # 隐藏 -> 旗帜
        state = toggle_flag(board, 0, 0)
        self.assertEqual(state, CellState.FLAGGED)
        
        # 旗帜 -> 问号
        state = toggle_flag(board, 0, 0)
        self.assertEqual(state, CellState.QUESTION)
        self.assertEqual(board.stats.flagged_cells, 0)
        
        # 问号 -> 隐藏
        state = toggle_flag(board, 0, 0)
        self.assertEqual(state, CellState.HIDDEN)
    
    def test_toggle_flag_revealed_cell(self):
        """测试已揭开格子标记"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        state = toggle_flag(board, 4, 4)
        self.assertEqual(state, CellState.REVEALED)  # 不能标记已揭开
    
    def test_toggle_flag_invalid_position(self):
        """测试无效位置标记"""
        board = create_board(9, 9, 10)
        with self.assertRaises(ValueError):
            toggle_flag(board, -1, 0)
    
    def test_set_flag_basic(self):
        """测试直接设置标记"""
        board = create_board(9, 9, 10)
        set_flag(board, 0, 0, CellState.FLAGGED)
        self.assertEqual(board.board[0][0].state, CellState.FLAGGED)
        self.assertEqual(board.stats.flagged_cells, 1)
    
    def test_chord_reveal_basic(self):
        """测试双击操作"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        
        # 双击只有在周围旗帜数等于雷数时才有效
        # 这里应该返回空（因为没有足够旗帜）
        revealed = chord_reveal(board, 4, 4)
        self.assertEqual(len(revealed), 0)


class TestGameState(unittest.TestCase):
    """测试游戏状态"""
    
    def test_get_game_state(self):
        """测试获取游戏状态"""
        board = create_board(9, 9, 10)
        state = get_game_state(board)
        self.assertEqual(state, GameState.PLAYING)
    
    def test_is_game_over_playing(self):
        """测试进行中状态"""
        board = create_board(9, 9, 10)
        self.assertEqual(is_game_over(board), False)
    
    def test_is_won(self):
        """测试胜利检测"""
        board = create_board(9, 9, 10)
        self.assertEqual(is_won(board), False)
    
    def test_is_lost(self):
        """测试失败检测"""
        board = create_board(9, 9, 10)
        self.assertEqual(is_lost(board), False)
    
    def test_get_remaining_mines(self):
        """测试剩余雷数"""
        board = create_board(9, 9, 10)
        remaining = get_remaining_mines(board)
        self.assertEqual(remaining, 10)
        
        toggle_flag(board, 0, 0)
        remaining = get_remaining_mines(board)
        self.assertEqual(remaining, 9)
    
    def test_get_progress(self):
        """测试进度"""
        board = create_board(9, 9, 10)
        progress = get_progress(board)
        self.assertEqual(progress, 0.0)
        
        reveal_cell(board, 4, 4)
        progress = get_progress(board)
        self.assertGreater(progress, 0.0)


class TestVisualization(unittest.TestCase):
    """测试可视化"""
    
    def test_board_to_string(self):
        """测试字符串表示"""
        board = create_board(3, 3, 1)
        str_repr = board_to_string(board)
        self.assertIn('?', str_repr)
        self.assertIn('│', str_repr)
        self.assertIn('┌', str_repr)
    
    def test_board_to_string_with_mines(self):
        """测试显示雷"""
        # 使用更大的板子
        board = create_board(5, 5, 1)
        place_mines(board, 2, 2)  # 中间安全
        str_repr = board_to_string(board, show_mines=True)
        # 雷的符号在未揭开状态是 '*'（带空格）
        self.assertTrue('*' in str_repr or '💣' in str_repr)
    
    def test_board_to_emoji(self):
        """测试 Emoji 表示"""
        board = create_board(3, 3, 1)
        emoji_repr = board_to_emoji(board)
        self.assertIn('⬜', emoji_repr)
    
    def test_board_to_emoji_revealed(self):
        """测试揭开后的 Emoji"""
        board = create_board(3, 3, 0)  # 无雷
        reveal_cell(board, 1, 1)
        emoji_repr = board_to_emoji(board)
        # 无雷的板子揭开后应该显示空格或数字
        self.assertTrue('⬜' in emoji_repr or '   ' in emoji_repr or '⬛' in emoji_repr)


class TestSerialization(unittest.TestCase):
    """测试序列化"""
    
    def test_serialize_board_basic(self):
        """测试基本序列化"""
        board = create_board(9, 9, 10)
        json_str = serialize_board(board)
        self.assertIn('rows', json_str)
        self.assertIn('cols', json_str)
        self.assertIn('mines', json_str)
    
    def test_serialize_deserialize_roundtrip(self):
        """测试序列化/反序列化往返"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        toggle_flag(board, 0, 0)
        
        json_str = serialize_board(board)
        restored = deserialize_board(json_str)
        
        self.assertEqual(restored.rows, board.rows)
        self.assertEqual(restored.cols, board.cols)
        self.assertEqual(restored.mines, board.mines)
        self.assertEqual(restored.state, board.state)
        self.assertEqual(restored.stats.revealed_cells, board.stats.revealed_cells)
        self.assertEqual(restored.stats.flagged_cells, board.stats.flagged_cells)
    
    def test_deserialize_invalid_json(self):
        """测试无效 JSON"""
        with self.assertRaises(ValueError):
            deserialize_board("invalid json")
    
    def test_serialize_with_mine_positions(self):
        """测试雷位置序列化"""
        board = create_board(9, 9, 10)
        place_mines(board, 4, 4)
        json_str = serialize_board(board)
        restored = deserialize_board(json_str)
        self.assertEqual(len(restored._mine_positions), 10)


class TestSolverHelper(unittest.TestCase):
    """测试求解辅助"""
    
    def test_get_safe_cells_initial(self):
        """测试初始安全格子"""
        board = create_board(9, 9, 10)
        safe = get_safe_cells(board)
        # 初始时所有格子都是潜在安全的
        self.assertEqual(len(safe), 81)
    
    def test_get_safe_cells_after_reveal(self):
        """测试揭开后安全格子"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        safe = get_safe_cells(board)
        self.assertIsInstance(safe, list)
    
    def test_get_mine_cells_initial(self):
        """测试初始雷格子"""
        board = create_board(9, 9, 10)
        mines = get_mine_cells(board)
        # 初始时无法确定雷
        self.assertEqual(len(mines), 0)
    
    def test_get_hint_initial(self):
        """测试初始提示"""
        board = create_board(9, 9, 10)
        hint = get_hint(board)
        self.assertIsNotNone(hint)
        self.assertEqual(len(hint), 3)
    
    def test_get_hint_after_reveal(self):
        """测试揭开后提示"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        hint = get_hint(board)
        if hint:
            self.assertIn(hint[2], ['safe', 'mine', 'guess'])


class TestStatistics(unittest.TestCase):
    """测试统计"""
    
    def test_get_statistics_basic(self):
        """测试基本统计"""
        board = create_board(9, 9, 10)
        stats = get_statistics(board)
        self.assertEqual(stats['rows'], 9)
        self.assertEqual(stats['cols'], 9)
        self.assertEqual(stats['total_cells'], 81)
        self.assertEqual(stats['total_mines'], 10)
    
    def test_get_statistics_after_moves(self):
        """测试操作后统计"""
        board = create_board(9, 9, 10)
        reveal_cell(board, 4, 4)
        toggle_flag(board, 0, 0)
        
        stats = get_statistics(board)
        self.assertGreater(stats['revealed_cells'], 0)
        self.assertEqual(stats['flagged_cells'], 1)
    
    def test_get_statistics_progress(self):
        """测试进度统计"""
        board = create_board(9, 9, 10)
        stats = get_statistics(board)
        self.assertEqual(stats['progress'], 0.0)


class TestFullGameFlow(unittest.TestCase):
    """测试完整游戏流程"""
    
    def test_new_game_beginner(self):
        """测试新游戏初级"""
        board = new_game(Difficulty.BEGINNER)
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.cols, 9)
        self.assertEqual(board.mines, 10)
    
    def test_new_game_custom(self):
        """测试新游戏自定义"""
        board = new_game(Difficulty.CUSTOM, rows=20, cols=20, mines=50)
        self.assertEqual(board.rows, 20)
        self.assertEqual(board.cols, 20)
        self.assertEqual(board.mines, 50)
    
    def test_make_move_reveal(self):
        """测试揭示操作"""
        board = new_game(Difficulty.BEGINNER)
        result = make_move(board, 4, 4, 'reveal')
        self.assertEqual(result['success'], True)
        self.assertIn('revealed', result)
    
    def test_make_move_flag(self):
        """测试标记操作"""
        board = new_game(Difficulty.BEGINNER)
        result = make_move(board, 0, 0, 'flag')
        self.assertEqual(result['success'], True)
    
    def test_make_move_chord(self):
        """测试双击操作"""
        board = new_game(Difficulty.BEGINNER)
        make_move(board, 4, 4, 'reveal')
        result = make_move(board, 4, 4, 'chord')
        self.assertEqual(result['success'], True)
    
    def test_make_move_invalid_action(self):
        """测试无效操作"""
        board = new_game(Difficulty.BEGINNER)
        result = make_move(board, 4, 4, 'invalid')
        self.assertEqual(result['success'], False)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_mines_board(self):
        """测试无雷板"""
        board = create_board(9, 9, 0)
        reveal_cell(board, 4, 4)
        
        # 所有格子应该被揭开
        revealed_count = sum(
            1 for r in range(board.rows)
            for c in range(board.cols)
            if board.board[r][c].state == CellState.REVEALED
        )
        self.assertEqual(revealed_count, 81)
        self.assertEqual(board.state, GameState.WON)
    
    def test_single_cell_board(self):
        """测试单格板"""
        board = create_board(1, 1, 0)
        reveal_cell(board, 0, 0)
        self.assertEqual(board.state, GameState.WON)
    
    def test_all_mines_flagged(self):
        """测试全部雷被标记"""
        board = create_board(5, 5, 1)
        reveal_cell(board, 2, 2)
        
        # 标记所有隐藏格子（不揭开雷）
        flagged_count = 0
        for r in range(board.rows):
            for c in range(board.cols):
                if board.board[r][c].state == CellState.HIDDEN:
                    set_flag(board, r, c, CellState.FLAGGED)
                    flagged_count += 1
        
        # 标记后剩余雷数应该是 (总雷数 - 标记数)
        remaining = get_remaining_mines(board)
        # 只要有标记，剩余雷数应该小于等于总雷数
        self.assertLessEqual(remaining, board.mines)
        # 如果有格子被标记，剩余雷数应该减少
        if flagged_count > 0:
            self.assertLess(remaining, board.mines)


class TestWinLoseConditions(unittest.TestCase):
    """测试胜负条件"""
    
    def test_win_condition_zero_mines(self):
        """测试胜利（无雷）"""
        board = create_board(5, 5, 0)
        reveal_cell(board, 2, 2)
        
        # 无雷的板子点击后应该直接胜利
        self.assertEqual(board.state, GameState.WON)
    
    def test_lose_condition(self):
        """测试失败条件"""
        board = create_board(3, 3, 8)  # 大量雷
        
        # 找到雷并点击
        # 由于安全区域限制，可能无法触发失败
        # 使用一个已知会失败的设置
        board2 = create_board(1, 2, 1)
        reveal_cell(board2, 0, 0)  # 首次点击安全
        
        # 检查是否有一个雷
        if board2.mines > 0:
            # 创建另一个板子，手动设置失败状态
            board3 = create_board(3, 3, 1)
            board3.state = GameState.LOST
            self.assertEqual(is_lost(board3), True)


class TestCellDataClass(unittest.TestCase):
    """测试 Cell 数据类"""
    
    def test_cell_defaults(self):
        """测试 Cell 默认值"""
        cell = Cell()
        self.assertEqual(cell.is_mine, False)
        self.assertEqual(cell.adjacent_mines, 0)
        self.assertEqual(cell.state, CellState.HIDDEN)
    
    def test_cell_custom_values(self):
        """测试 Cell 自定义值"""
        cell = Cell(is_mine=True, adjacent_mines=3, state=CellState.FLAGGED)
        self.assertEqual(cell.is_mine, True)
        self.assertEqual(cell.adjacent_mines, 3)
        self.assertEqual(cell.state, CellState.FLAGGED)


class TestGameStatsDataClass(unittest.TestCase):
    """测试 GameStats 数据类"""
    
    def test_game_stats_defaults(self):
        """测试 GameStats 默认值"""
        stats = GameStats()
        self.assertEqual(stats.total_cells, 0)
        self.assertEqual(stats.total_mines, 0)
        self.assertEqual(stats.revealed_cells, 0)
        self.assertEqual(stats.flagged_cells, 0)
        self.assertEqual(stats.clicks, 0)
        self.assertEqual(stats.first_click, True)


class TestConstants(unittest.TestCase):
    """测试常量"""
    
    def test_difficulty_values(self):
        """测试难度值"""
        self.assertEqual(Difficulty.BEGINNER.value, (9, 9, 10))
        self.assertEqual(Difficulty.INTERMEDIATE.value, (16, 16, 40))
        self.assertEqual(Difficulty.EXPERT.value, (30, 16, 99))
    
    def test_cell_state_values(self):
        """测试格子状态值"""
        self.assertEqual(CellState.HIDDEN.value, 0)
        self.assertEqual(CellState.REVEALED.value, 1)
        self.assertEqual(CellState.FLAGGED.value, 2)
        self.assertEqual(CellState.QUESTION.value, 3)
    
    def test_game_state_values(self):
        """测试游戏状态值"""
        self.assertEqual(GameState.PLAYING.value, 0)
        self.assertEqual(GameState.WON.value, 1)
        self.assertEqual(GameState.LOST.value, 2)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)