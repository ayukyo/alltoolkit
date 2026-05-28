#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake Game Utils 使用示例
===========================

展示贪吃蛇游戏工具库的各种使用方法。

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snake_game_utils.mod import (
    SnakeGame,
    GameConfig,
    Direction,
    Position,
    SnakeRenderer,
    SnakeAI,
    SnakeRecorder,
    SnakeGameUtils,
    play_snake,
    create_snake_game,
    simulate_snake_game,
    run_snake_tournament,
)


def example_basic_game():
    """示例1: 基础游戏操作"""
    print("\n" + "=" * 60)
    print("示例1: 基础游戏操作")
    print("=" * 60)
    
    # 创建游戏
    game = create_snake_game(width=15, height=10)
    
    # 获取初始状态
    print(f"\n初始状态:")
    print(f"  蛇头位置: {game.get_snake_head()}")
    print(f"  蛇尾位置: {game.get_snake_tail()}")
    print(f"  蛇身长度: {len(game.state.snake)}")
    print(f"  食物位置: {game.state.food}")
    
    # 渲染初始状态
    renderer = SnakeRenderer(game)
    print(f"\n初始画面:")
    print(renderer.render())
    
    # 执行一些移动
    print(f"\n执行移动...")
    for i in range(5):
        game.move()
        print(f"  第{i+1}步: 蛇头在 {game.get_snake_head()}, 得分: {game.state.score}")
    
    # 改变方向
    print(f"\n改变方向向下...")
    game.set_direction(Direction.DOWN)
    for i in range(3):
        game.move()
        print(f"  第{i+1}步: 蛇头在 {game.get_snake_head()}, 得分: {game.state.score}")
    
    # 渲染最终状态
    print(f"\n当前画面:")
    print(renderer.render())


def example_custom_config():
    """示例2: 自定义配置"""
    print("\n" + "=" * 60)
    print("示例2: 自定义配置")
    print("=" * 60)
    
    # 创建自定义配置
    config = GameConfig(
        width=25,              # 更宽的游戏区域
        height=15,             # 更高的游戏区域
        initial_length=5,      # 初始蛇长度
        initial_speed=200,     # 初始速度 (毫秒)
        speed_increment=20,     # 每吃食物加速 20ms
        min_speed=80,          # 最快速度
        food_score=15,         # 每个食物得分
        level_up_score=100,    # 每100分升级
        walls_kill=False,      # 穿墙模式
    )
    
    game = SnakeGame(config)
    
    print(f"\n游戏配置:")
    print(f"  区域大小: {config.width} x {config.height}")
    print(f"  初始长度: {config.initial_length}")
    print(f"  初始速度: {config.initial_speed}ms")
    print(f"  食物得分: {config.food_score}")
    print(f"  穿墙模式: {'是' if not config.walls_kill else '否'}")
    
    # 使用 AI 自动玩一段时间
    ai = SnakeAI(game)
    moves = 0
    while not game.state.is_game_over and moves < 50:
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
        moves += 1
    
    print(f"\nAI 模拟 50 步后:")
    print(f"  得分: {game.state.score}")
    print(f"  长度: {len(game.state.snake)}")
    print(f"  等级: {game.state.level}")
    print(f"  速度: {game.state.speed}ms")


def example_ai_autoplay():
    """示例3: AI 自动游戏"""
    print("\n" + "=" * 60)
    print("示例3: AI 自动游戏")
    print("=" * 60)
    
    game = create_snake_game(width=20, height=12)
    ai = SnakeAI(game)
    renderer = SnakeRenderer(game)
    
    print(f"\nAI 自动游戏模拟...")
    
    # 记录游戏过程
    states = []
    max_moves = 100
    
    while not game.state.is_game_over and game.state.moves_made < max_moves:
        # 保存状态
        if game.state.moves_made % 20 == 0:
            states.append({
                'moves': game.state.moves_made,
                'score': game.state.score,
                'length': len(game.state.snake),
            })
        
        # AI 决策
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    # 最终状态
    print(f"\n游戏结束!")
    print(f"  总移动次数: {game.state.moves_made}")
    print(f"  最终得分: {game.state.score}")
    print(f"  最终长度: {len(game.state.snake)}")
    print(f"  吃食物数: {game.state.foods_eaten}")
    print(f"  占据率: {game.get_occupancy():.2%}")
    
    # 显示关键状态
    print(f"\n关键状态:")
    for state in states:
        print(f"  移动 {state['moves']}: 得分={state['score']}, 长度={state['length']}")


def example_game_recording():
    """示例4: 游戏录制"""
    print("\n" + "=" * 60)
    print("示例4: 游戏录制")
    print("=" * 60)
    
    game = create_snake_game(width=12, height=8)
    ai = SnakeAI(game)
    recorder = SnakeRecorder(game)
    
    print(f"\n开始录制...")
    recorder.start_recording()
    
    # 玩一局游戏
    while not game.state.is_game_over and game.state.moves_made < 30:
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
        recorder.record_frame()
    
    recorder.stop_recording()
    
    print(f"录制完成!")
    print(f"  录制帧数: {len(recorder.recording)}")
    
    # 查看录制数据
    if recorder.recording:
        first_frame = recorder.recording[0]
        last_frame = recorder.recording[-1]
        
        print(f"\n第一帧:")
        print(f"  蛇长度: {len(first_frame['snake'])}")
        print(f"  方向: {first_frame['direction']}")
        
        print(f"\n最后一帧:")
        print(f"  蛇长度: {len(last_frame['snake'])}")
        print(f"  得分: {last_frame['score']}")
        print(f"  游戏结束: {last_frame['is_game_over']}")


def example_tournament():
    """示例5: 锦标赛模式"""
    print("\n" + "=" * 60)
    print("示例5: 锦标赛模式")
    print("=" * 60)
    
    print(f"\n运行 10 局 AI 锦标赛...")
    tournament = run_snake_tournament(games=10, width=15, height=10)
    
    print(f"\n锦标赛结果:")
    print(f"  总局数: {tournament['games']}")
    print(f"  平均得分: {tournament['average_score']:.1f}")
    print(f"  最高得分: {tournament['max_score']}")
    print(f"  最低得分: {tournament['min_score']}")
    print(f"  平均长度: {tournament['average_length']:.1f}")
    print(f"  平均移动: {tournament['average_moves']:.1f}")
    
    print(f"\n各局得分: {tournament['scores']}")


def example_different_sizes():
    """示例6: 不同尺寸的游戏区域"""
    print("\n" + "=" * 60)
    print("示例6: 不同尺寸的游戏区域")
    print("=" * 60)
    
    sizes = [(10, 10), (20, 15), (30, 20)]
    
    for width, height in sizes:
        result = simulate_snake_game(width=width, height=height, max_moves=50)
        area = width * height
        
        print(f"\n区域 {width}x{height} (面积 {area}):")
        print(f"  得分: {result['score']}")
        print(f"  长度: {result['length']}")
        print(f"  占据率: {result['occupancy']:.2%}")


def example_rendering_styles():
    """示例7: 不同渲染风格"""
    print("\n" + "=" * 60)
    print("示例7: 不同渲染风格")
    print("=" * 60)
    
    game = create_snake_game(width=12, height=6)
    renderer = SnakeRenderer(game)
    
    # 执行一些移动
    ai = SnakeAI(game)
    for _ in range(10):
        if game.state.is_game_over:
            break
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    print(f"\n完整渲染模式:")
    print(renderer.render())
    
    print(f"\n简洁渲染模式:")
    print(renderer.render_minimal())


def example_game_states():
    """示例8: 游戏状态管理"""
    print("\n" + "=" * 60)
    print("示例8: 游戏状态管理")
    print("=" * 60)
    
    game = create_snake_game(width=10, height=10)
    
    print(f"\n初始状态:")
    print(f"  游戏结束: {game.state.is_game_over}")
    print(f"  暂停状态: {game.state.is_paused}")
    
    # 测试暂停
    print(f"\n测试暂停功能...")
    game.toggle_pause()
    print(f"  暂停后: {game.state.is_paused}")
    
    # 尝试在暂停时移动
    initial_moves = game.state.moves_made
    game.move()
    print(f"  暂停时移动: {game.state.moves_made == initial_moves} (移动数不变)")
    
    # 继续
    game.toggle_pause()
    print(f"  继续后: {game.state.is_paused}")
    
    # 测试重置
    print(f"\n测试重置功能...")
    for _ in range(20):
        if game.state.is_game_over:
            break
        direction = SnakeAI(game).get_next_direction()
        game.set_direction(direction)
        game.move()
    
    print(f"  移动后得分: {game.state.score}")
    game.reset()
    print(f"  重置后得分: {game.state.score}")


def example_direction_control():
    """示例9: 方向控制"""
    print("\n" + "=" * 60)
    print("示例9: 方向控制")
    print("=" * 60)
    
    game = create_snake_game(width=10, height=10)
    
    print(f"\n初始方向: {game.state.direction.name}")
    
    # 测试方向设置
    directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
    
    for d in directions:
        game.state.direction = Direction.RIGHT  # 重置方向
        result = game.set_direction(d)
        print(f"  设置方向 {d.name}: {'成功' if result else '失败 (不能直接反向)'}")
    
    # 测试反向
    print(f"\n测试反向规则:")
    game.state.direction = Direction.RIGHT
    result = game.set_direction(Direction.LEFT)
    print(f"  当前向右，尝试向左: {'成功' if result else '失败'}")
    
    game.state.direction = Direction.UP
    result = game.set_direction(Direction.DOWN)
    print(f"  当前向上，尝试向下: {'成功' if result else '失败'}")


def example_statistics():
    """示例10: 游戏统计"""
    print("\n" + "=" * 60)
    print("示例10: 游戏统计")
    print("=" * 60)
    
    # 模拟多局游戏并收集统计
    results = []
    for _ in range(20):
        result = simulate_snake_game(width=15, height=10, max_moves=200)
        results.append(result)
    
    # 计算统计数据
    scores = [r['score'] for r in results]
    lengths = [r['length'] for r in results]
    moves = [r['moves'] for r in results]
    foods = [r['foods_eaten'] for r in results]
    
    print(f"\n20 局游戏统计:")
    print(f"  得分:")
    print(f"    平均: {sum(scores)/len(scores):.1f}")
    print(f"    最高: {max(scores)}")
    print(f"    最低: {min(scores)}")
    
    print(f"  蛇长度:")
    print(f"    平均: {sum(lengths)/len(lengths):.1f}")
    print(f"    最长: {max(lengths)}")
    print(f"    最短: {min(lengths)}")
    
    print(f"  移动次数:")
    print(f"    平均: {sum(moves)/len(moves):.1f}")
    print(f"    最多: {max(moves)}")
    print(f"    最少: {min(moves)}")
    
    print(f"  吃食物数:")
    print(f"    平均: {sum(foods)/len(foods):.1f}")
    print(f"    最多: {max(foods)}")
    print(f"    最少: {min(foods)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Snake Game Utils 使用示例集")
    print("=" * 60)
    
    examples = [
        ("基础游戏操作", example_basic_game),
        ("自定义配置", example_custom_config),
        ("AI 自动游戏", example_ai_autoplay),
        ("游戏录制", example_game_recording),
        ("锦标赛模式", example_tournament),
        ("不同尺寸", example_different_sizes),
        ("渲染风格", example_rendering_styles),
        ("状态管理", example_game_states),
        ("方向控制", example_direction_control),
        ("游戏统计", example_statistics),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n示例 '{name}' 出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
    print("\n提示: 运行 play_snake() 可以开始交互式游戏")


if __name__ == '__main__':
    main()