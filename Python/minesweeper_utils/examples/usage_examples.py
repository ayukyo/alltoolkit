#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minesweeper Utilities - 使用示例
================================

展示扫雷游戏工具模块的各种使用场景。

作者: AllToolkit 自动化开发助手
日期: 2026-05-02
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from minesweeper_utils.mod import (
    # 类和枚举
    CellState, GameState, Difficulty,
    # 游戏创建
    create_board, create_board_from_difficulty, new_game,
    # 游戏操作
    reveal_cell, toggle_flag, set_flag, chord_reveal, make_move,
    # 雷区管理
    place_mines,
    # 状态查询
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
)


def example_1_basic_game():
    """
    示例 1: 基本游戏流程
    """
    print("=" * 60)
    print("示例 1: 基本游戏流程")
    print("=" * 60)
    
    # 创建初级难度游戏
    board = new_game(Difficulty.BEGINNER)
    print(f"创建游戏板: {board.rows}x{board.cols}, 雷数: {board.mines}")
    
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
    
    print()


def example_2_custom_board():
    """
    示例 2: 自定义游戏板
    """
    print("=" * 60)
    print("示例 2: 自定义游戏板")
    print("=" * 60)
    
    # 创建 20x20 的自定义游戏板，50 个雷
    board = create_board(20, 20, 50)
    print(f"自定义游戏板: {board.rows}x{board.cols}, 雷数: {board.mines}")
    
    # 中间位置点击
    reveal_cell(board, 10, 10)
    
    # 检查进度
    progress = get_progress(board)
    print(f"当前进度: {progress:.2%}")
    
    # 剩余雷数
    remaining = get_remaining_mines(board)
    print(f"剩余雷数: {remaining}")
    
    print()


def example_3_flagging():
    """
    示例 3: 标记操作
    """
    print("=" * 60)
    print("示例 3: 标记操作")
    print("=" * 60)
    
    board = new_game(Difficulty.BEGINNER)
    
    # 揭开一些格子
    reveal_cell(board, 4, 4)
    
    print("初始状态:")
    print(board_to_string(board))
    
    # 标记几个可疑格子
    positions_to_flag = [(0, 0), (0, 1), (1, 0)]
    for r, c in positions_to_flag:
        toggle_flag(board, r, c)
        print(f"\n标记 ({r}, {c})")
    
    print("\n标记后:")
    print(board_to_string(board))
    
    # 显示剩余雷数
    remaining = get_remaining_mines(board)
    print(f"\n剩余雷数: {remaining}")
    
    # 循环标记状态
    print("\n循环标记状态演示:")
    toggle_flag(board, 0, 0)  # FLAGGED -> QUESTION
    print(board_to_string(board))
    toggle_flag(board, 0, 0)  # QUESTION -> HIDDEN
    print(board_to_string(board))
    
    print()


def example_4_solver_hint():
    """
    示例 4: 求解辅助和提示
    """
    print("=" * 60)
    print("示例 4: 求解辅助和提示")
    print("=" * 60)
    
    board = new_game(Difficulty.BEGINNER)
    
    # 揭开中间
    reveal_cell(board, 4, 4)
    
    print("当前游戏状态:")
    print(board_to_emoji(board))
    
    # 获取安全格子
    safe_cells = get_safe_cells(board)
    print(f"\n确定安全的格子数: {len(safe_cells)}")
    if safe_cells:
        print(f"安全格子示例: {safe_cells[:5]}")
    
    # 获取确定的雷
    mine_cells = get_mine_cells(board)
    print(f"\n确定是雷的格子数: {len(mine_cells)}")
    if mine_cells:
        print(f"雷格子示例: {mine_cells[:5]}")
    
    # 获取提示
    hint = get_hint(board)
    if hint:
        print(f"\n系统提示: 位置 ({hint[0]}, {hint[1]}) - {hint[2]}")
    
    print()


def example_5_serialization():
    """
    示例 5: 序列化和保存游戏
    """
    print("=" * 60)
    print("示例 5: 序列化和保存游戏")
    print("=" * 60)
    
    board = new_game(Difficulty.INTERMEDIATE)
    
    # 进行一些操作
    reveal_cell(board, 8, 8)
    toggle_flag(board, 0, 0)
    
    print("当前游戏状态:")
    print(board_to_emoji(board))
    
    # 序列化为 JSON
    json_str = serialize_board(board)
    print(f"\n序列化 JSON (部分):")
    print(json_str[:200] + "...")
    
    # 反序列化
    restored = deserialize_board(json_str)
    print(f"\n反序列化成功!")
    print(f"  行数: {restored.rows}")
    print(f"  列数: {restored.cols}")
    print(f"  雷数: {restored.mines}")
    print(f"  已揭开: {restored.stats.revealed_cells}")
    print(f"  已标记: {restored.stats.flagged_cells}")
    
    # 保存到文件示例（不实际保存，仅展示用法）
    print("\n保存到文件的方法:")
    print("  with open('minesweeper_save.json', 'w') as f:")
    print("      f.write(serialize_board(board))")
    
    print()


def example_6_visualization():
    """
    示例 6: 游戏板可视化
    """
    print("=" * 60)
    print("示例 6: 游戏板可视化")
    print("=" * 60)
    
    # 创建一个小型测试板
    board = create_board(5, 5, 3)
    
    # 未揭开状态
    print("\n未揭开状态 (默认):")
    print(board_to_string(board))
    
    # 放置雷并显示（调试模式）
    place_mines(board, 2, 2)
    print("\n显示雷位置 (调试模式):")
    print(board_to_string(board, show_mines=True))
    
    # 揭开后
    reveal_cell(board, 2, 2)
    print("\n揭开后状态:")
    print(board_to_string(board))
    
    # Emoji 版本
    print("\nEmoji 表示:")
    print(board_to_emoji(board))
    
    # 显示雷的 Emoji 版本
    print("\nEmoji 版本 (显示雷):")
    print(board_to_emoji(board, show_mines=True))
    
    print()


def example_7_difficulty_levels():
    """
    示例 7: 不同难度级别
    """
    print("=" * 60)
    print("示例 7: 不同难度级别")
    print("=" * 60)
    
    difficulties = [
        ('初级', Difficulty.BEGINNER),
        ('中级', Difficulty.INTERMEDIATE),
        ('高级', Difficulty.EXPERT),
    ]
    
    for name, diff in difficulties:
        board = new_game(diff)
        print(f"\n{name}:")
        print(f"  尺寸: {board.rows}x{board.cols}")
        print(f"  总格子数: {board.rows * board.cols}")
        print(f"  雷数: {board.mines}")
        print(f"  雷密度: {board.mines / (board.rows * board.cols):.2%}")
    
    print()


def example_8_statistics():
    """
    示例 8: 游戏统计
    """
    print("=" * 60)
    print("示例 8: 游戏统计")
    print("=" * 60)
    
    board = new_game(Difficulty.INTERMEDIATE)
    
    # 初始统计
    print("初始统计:")
    stats = get_statistics(board)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 进行一些操作
    print("\n进行操作...")
    reveal_cell(board, 8, 8)
    toggle_flag(board, 0, 0)
    toggle_flag(board, 0, 1)
    toggle_flag(board, 1, 0)
    
    # 操作后统计
    print("\n操作后统计:")
    stats = get_statistics(board)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 进度
    progress = get_progress(board)
    print(f"\n完成进度: {progress:.2%}")
    
    print()


def example_9_game_loop_simulation():
    """
    示例 9: 简单游戏循环模拟
    """
    print("=" * 60)
    print("示例 9: 简单游戏循环模拟")
    print("=" * 60)
    
    board = new_game(Difficulty.BEGINNER)
    
    print("开始游戏循环（自动播放演示）")
    print(f"初始状态: {get_game_state(board).name}")
    
    move_count = 0
    max_moves = 20  # 限制演示步数
    
    while not is_game_over(board) and move_count < max_moves:
        # 获取提示
        hint = get_hint(board)
        
        if hint is None:
            print("无可用提示，游戏结束")
            break
        
        row, col, hint_type = hint
        move_count += 1
        
        if hint_type == 'safe':
            # 安全格子，揭开
            result = make_move(board, row, col, 'reveal')
            print(f"步 {move_count}: 揭开 ({row}, {col}) - 揭开了 {len(result['revealed'])} 格")
        
        elif hint_type == 'mine':
            # 确定是雷，标记
            make_move(board, row, col, 'flag')
            print(f"步 {move_count}: 标记 ({row}, {col}) 为雷")
        
        else:  # guess
            # 不确定，也揭开（演示用）
            result = make_move(board, row, col, 'reveal')
            print(f"步 {move_count}: 猜测揭开 ({row}, {col}) - 揭开了 {len(result['revealed'])} 格")
        
        # 检查是否踩雷
        if is_lost(board):
            print("\n踩雷了！游戏结束")
            break
    
    # 最终状态
    print(f"\n最终游戏状态: {get_game_state(board).name}")
    print(f"完成步数: {move_count}")
    print(f"完成进度: {get_progress(board):.2%}")
    
    # 显示最终游戏板
    print("\n最终游戏板:")
    print(board_to_emoji(board))
    
    print()


def example_10_zero_mine_board():
    """
    示例 10: 无雷游戏板（特殊情况）
    """
    print("=" * 60)
    print("示例 10: 无雷游戏板")
    print("=" * 60)
    
    # 创建无雷板
    board = create_board(5, 5, 0)
    print(f"创建 5x5 无雷游戏板")
    
    # 显示初始
    print("\n初始状态:")
    print(board_to_string(board))
    
    # 点击中间
    reveal_cell(board, 2, 2)
    
    # 无雷的板子一次点击应该全部揭开
    print("\n点击后:")
    print(board_to_emoji(board))
    
    # 检查状态
    print(f"\n游戏状态: {get_game_state(board).name}")
    print(f"是否胜利: {is_won(board)}")
    
    stats = get_statistics(board)
    print(f"揭开格子数: {stats['revealed_cells']}")
    print(f"进度: {stats['progress']:.2%}")
    
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n")
    print("=" * 60)
    print(" 扫雷游戏工具模块 - 使用示例集合")
    print("=" * 60)
    print("\n")
    
    example_1_basic_game()
    example_2_custom_board()
    example_3_flagging()
    example_4_solver_hint()
    example_5_serialization()
    example_6_visualization()
    example_7_difficulty_levels()
    example_8_statistics()
    example_9_game_loop_simulation()
    example_10_zero_mine_board()
    
    print("=" * 60)
    print(" 所有示例完成")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()