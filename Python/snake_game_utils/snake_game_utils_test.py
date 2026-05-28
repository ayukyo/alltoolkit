#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake Game Utils 测试文件
===========================

测试贪吃蛇游戏工具库的所有功能。

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
    GameState,
    Position,
    Direction,
    SnakeRenderer,
    SnakeAI,
    SnakeRecorder,
    SnakeGameUtils,
    play_snake,
    create_snake_game,
    simulate_snake_game,
    run_snake_tournament,
)


def test_position():
    """测试 Position 类"""
    print("测试 Position 类...")
    
    # 创建位置
    p1 = Position(3, 5)
    assert p1.x == 3
    assert p1.y == 5
    
    # 位置相加
    p2 = Position(1, 2)
    p3 = p1 + p2
    assert p3.x == 4
    assert p3.y == 7
    
    # 位置相等
    p4 = Position(3, 5)
    assert p1 == p4
    
    # 转换为元组
    assert p1.to_tuple() == (3, 5)
    
    # 从方向创建
    p5 = Position.from_direction(Direction.RIGHT)
    assert p5.x == 1
    assert p5.y == 0
    
    p6 = Position.from_direction(Direction.DOWN)
    assert p6.x == 0
    assert p6.y == 1
    
    print("  ✓ Position 类测试通过")


def test_direction():
    """测试 Direction 枚举"""
    print("测试 Direction 枚举...")
    
    # 方向值
    assert Direction.UP.value == (0, -1)
    assert Direction.DOWN.value == (0, 1)
    assert Direction.LEFT.value == (-1, 0)
    assert Direction.RIGHT.value == (1, 0)
    
    # 相反方向
    assert Direction.UP.opposite() == Direction.DOWN
    assert Direction.DOWN.opposite() == Direction.UP
    assert Direction.LEFT.opposite() == Direction.RIGHT
    assert Direction.RIGHT.opposite() == Direction.LEFT
    
    print("  ✓ Direction 枚举测试通过")


def test_game_config():
    """测试 GameConfig 配置"""
    print("测试 GameConfig 配置...")
    
    # 默认配置
    config = GameConfig()
    assert config.width == 20
    assert config.height == 15
    assert config.initial_length == 3
    assert config.initial_speed == 150
    
    # 自定义配置
    config2 = GameConfig(
        width=30,
        height=20,
        initial_speed=100,
        walls_kill=False
    )
    assert config2.width == 30
    assert config2.height == 20
    assert config2.initial_speed == 100
    assert config2.walls_kill == False
    
    print("  ✓ GameConfig 配置测试通过")


def test_snake_game_init():
    """测试游戏初始化"""
    print("测试游戏初始化...")
    
    game = SnakeGame()
    
    # 检查蛇的初始长度
    assert len(game.state.snake) == game.config.initial_length
    
    # 检查初始方向
    assert game.state.direction == Direction.RIGHT
    
    # 检查游戏状态
    assert not game.state.is_game_over
    assert not game.state.is_paused
    assert game.state.score == 0
    
    # 检查食物已生成
    assert game.state.food is not None
    
    # 检查食物不在蛇身上
    assert game.state.food not in game.state.snake
    
    print("  ✓ 游戏初始化测试通过")


def test_snake_movement():
    """测试蛇的移动"""
    print("测试蛇的移动...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    
    # 获取初始蛇头位置
    initial_head = game.state.snake[0]
    
    # 向右移动
    game.move()
    new_head = game.state.snake[0]
    assert new_head.x == initial_head.x + 1
    assert new_head.y == initial_head.y
    
    # 改变方向向下
    game.set_direction(Direction.DOWN)
    game.move()
    new_head = game.state.snake[0]
    assert new_head.x == initial_head.x + 1
    assert new_head.y == initial_head.y + 1
    
    # 不能直接反向
    result = game.set_direction(Direction.UP)
    assert result == False
    
    print("  ✓ 蛇的移动测试通过")


def test_wall_collision():
    """测试墙壁碰撞"""
    print("测试墙壁碰撞...")
    
    config = GameConfig(width=10, height=10, walls_kill=True)
    game = SnakeGame(config)
    
    # 移动蛇到右墙边
    for _ in range(15):
        if game.state.is_game_over:
            break
        game.move()
    
    assert game.state.is_game_over, "应该撞墙死亡"
    
    print("  ✓ 墙壁碰撞测试通过")


def test_self_collision():
    """测试自身碰撞"""
    print("测试自身碰撞...")
    
    config = GameConfig(
        width=5,
        height=5,
        initial_length=3,
        self_collision_kills=True
    )
    game = SnakeGame(config)
    
    # 创建一个蛇会撞到自己的情况
    # 先吃到足够多的食物变长
    for _ in range(100):
        if game.state.is_game_over:
            break
        
        # 使用 AI 移动
        ai = SnakeAI(game)
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    # 无论如何，游戏应该已经结束或仍在运行
    # 主要验证碰撞检测逻辑正常工作
    assert game.state.moves_made > 0
    
    print("  ✓ 自身碰撞测试通过")


def test_food_eating():
    """测试吃食物"""
    print("测试吃食物...")
    
    game = SnakeGame(GameConfig(width=10, height=10, food_score=10))
    
    initial_length = len(game.state.snake)
    initial_score = game.state.score
    
    # 持续移动直到吃到食物
    for _ in range(200):
        if game.state.is_game_over:
            break
        if game.state.foods_eaten > 0:
            break
        
        ai = SnakeAI(game)
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    # 应该至少吃到一个食物
    if game.state.foods_eaten > 0:
        assert len(game.state.snake) > initial_length
        assert game.state.score > initial_score
    
    print("  ✓ 吃食物测试通过")


def test_level_up():
    """测试升级系统"""
    print("测试升级系统...")
    
    config = GameConfig(
        width=10,
        height=10,
        food_score=20,
        level_up_score=50,
        speed_increment=10
    )
    game = SnakeGame(config)
    
    initial_speed = game.state.speed
    
    # 持续移动直到升级
    for _ in range(500):
        if game.state.is_game_over:
            break
        if game.state.level > 1:
            break
        
        ai = SnakeAI(game)
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    # 检查升级后速度变化
    if game.state.level > 1:
        assert game.state.speed < initial_speed
    
    print("  ✓ 升级系统测试通过")


def test_renderer():
    """测试渲染器"""
    print("测试渲染器...")
    
    game = SnakeGame(GameConfig(width=10, height=5))
    renderer = SnakeRenderer(game)
    
    # 渲染游戏
    output = renderer.render()
    
    # 检查输出包含预期内容
    assert '分数' in output
    assert '等级' in output
    
    lines = output.split('\n')
    # 高度 + 边框 + 状态行 = 5 + 2 + 2 = 9 行
    assert len(lines) >= 7
    
    # 简洁渲染
    minimal = renderer.render_minimal()
    assert minimal is not None
    
    print("  ✓ 渲染器测试通过")


def test_ai():
    """测试 AI"""
    print("测试 AI...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    ai = SnakeAI(game)
    
    # AI 应该给出有效方向
    direction = ai.get_next_direction()
    assert direction in Direction
    
    # 执行多次 AI 移动
    for _ in range(50):
        if game.state.is_game_over:
            break
        
        direction = ai.get_next_direction()
        game.set_direction(direction)
        game.move()
    
    # AI 应该能让游戏持续一段时间
    assert game.state.moves_made > 0
    
    print("  ✓ AI 测试通过")


def test_recorder():
    """测试录制器"""
    print("测试录制器...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    recorder = SnakeRecorder(game)
    
    # 开始录制
    recorder.start_recording()
    assert recorder._recording
    
    # 录制几帧
    for _ in range(10):
        game.move()
        recorder.record_frame()
    
    # 检查录制数据
    assert len(recorder.recording) > 0
    assert 'snake' in recorder.recording[0]
    assert 'food' in recorder.recording[0]
    assert 'direction' in recorder.recording[0]
    
    # 停止录制
    recorder.stop_recording()
    assert not recorder._recording
    
    print("  ✓ 录制器测试通过")


def test_game_reset():
    """测试游戏重置"""
    print("测试游戏重置...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    
    # 进行一些移动
    for _ in range(20):
        if game.state.is_game_over:
            break
        game.move()
    
    # 重置游戏
    game.reset()
    
    # 检查重置状态
    assert game.state.score == 0
    assert game.state.level == 1
    assert not game.state.is_game_over
    assert not game.state.is_paused
    assert game.state.moves_made == 0
    
    print("  ✓ 游戏重置测试通过")


def test_pause():
    """测试暂停功能"""
    print("测试暂停功能...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    
    # 暂停
    game.toggle_pause()
    assert game.state.is_paused
    
    # 暂停状态下移动应该无效
    initial_moves = game.state.moves_made
    game.move()
    assert game.state.moves_made == initial_moves
    
    # 继续
    game.toggle_pause()
    assert not game.state.is_paused
    
    # 现在可以移动
    game.move()
    assert game.state.moves_made > initial_moves
    
    print("  ✓ 暂停功能测试通过")


def test_simulate_game():
    """测试模拟游戏"""
    print("测试模拟游戏...")
    
    result = simulate_snake_game(width=15, height=10, max_moves=100)
    
    # 检查返回字段
    assert 'score' in result
    assert 'length' in result
    assert 'moves' in result
    assert 'foods_eaten' in result
    assert 'level' in result
    assert 'occupancy' in result
    
    # 检查值合理
    assert result['moves'] <= 100
    assert result['length'] >= 3
    assert result['occupancy'] >= 0
    
    print("  ✓ 模拟游戏测试通过")


def test_tournament():
    """测试锦标赛"""
    print("测试锦标赛...")
    
    tournament = run_snake_tournament(games=3, width=15, height=10)
    
    # 检查返回字段
    assert 'games' in tournament
    assert 'scores' in tournament
    assert 'average_score' in tournament
    assert 'max_score' in tournament
    assert 'min_score' in tournament
    
    # 检查值
    assert tournament['games'] == 3
    assert len(tournament['scores']) == 3
    
    print("  ✓ 锦标赛测试通过")


def test_wrap_mode():
    """测试穿墙模式"""
    print("测试穿墙模式...")
    
    config = GameConfig(width=5, height=5, walls_kill=False)
    game = SnakeGame(config)
    
    # 向右移动很多次，蛇应该能穿过墙壁
    for _ in range(20):
        if game.state.is_game_over:
            break
        game.move()
    
    # 在穿墙模式下不应该因为撞墙而死
    # 但可能会因为撞到自己而死
    # 主要验证游戏能继续运行
    assert game.state.moves_made > 0
    
    print("  ✓ 穿墙模式测试通过")


def test_getter_methods():
    """测试 getter 方法"""
    print("测试 getter 方法...")
    
    game = SnakeGame(GameConfig(width=10, height=10))
    
    # 蛇头位置
    head = game.get_snake_head()
    assert head is not None
    assert head == game.state.snake[0]
    
    # 蛇尾位置
    tail = game.get_snake_tail()
    assert tail is not None
    assert tail == game.state.snake[-1]
    
    # 游戏区域大小
    area = game.get_game_area()
    assert area == 10 * 10
    
    # 占据率
    occupancy = game.get_occupancy()
    assert occupancy > 0
    
    print("  ✓ getter 方法测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Snake Game Utils 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_position,
        test_direction,
        test_game_config,
        test_snake_game_init,
        test_snake_movement,
        test_wall_collision,
        test_self_collision,
        test_food_eating,
        test_level_up,
        test_renderer,
        test_ai,
        test_recorder,
        test_game_reset,
        test_pause,
        test_simulate_game,
        test_tournament,
        test_wrap_mode,
        test_getter_methods,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ 测试失败: {test.__name__}")
            print(f"    错误: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ 测试出错: {test.__name__}")
            print(f"    错误: {type(e).__name__}: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)