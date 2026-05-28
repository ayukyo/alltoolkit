#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake Game Utils - 贪吃蛇游戏工具库
==========================================

一个完整的贪吃蛇游戏实现，支持终端界面和游戏逻辑分离。
纯 Python 实现，零外部依赖。

功能列表:
- 完整的贪吃蛇游戏逻辑
- 终端界面渲染
- 碰撞检测
- 分数和等级系统
- 游戏状态管理
- AI 自动游戏模式
- 录制和回放功能

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import random
import time
import sys
import tty
import termios
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy


class Direction(Enum):
    """方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def opposite(self) -> 'Direction':
        """获取相反方向"""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]


@dataclass
class Position:
    """位置坐标"""
    x: int
    y: int
    
    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    @classmethod
    def from_direction(cls, direction: Direction) -> 'Position':
        """从方向创建位移"""
        dx, dy = direction.value
        return cls(dx, dy)


@dataclass
class GameConfig:
    """游戏配置"""
    width: int = 20
    height: int = 15
    initial_length: int = 3
    initial_speed: int = 150  # 毫秒
    speed_increment: int = 10  # 每吃一个食物加速
    min_speed: int = 50  # 最快速度
    walls_kill: bool = True  # 撞墙是否死亡
    self_collision_kills: bool = True  # 自身碰撞是否死亡
    food_score: int = 10  # 每个食物得分
    level_up_score: int = 50  # 升级所需分数


@dataclass
class GameState:
    """游戏状态"""
    snake: List[Position] = field(default_factory=list)
    food: Optional[Position] = None
    direction: Direction = Direction.RIGHT
    score: int = 0
    level: int = 1
    is_game_over: bool = False
    is_paused: bool = False
    speed: int = 150
    foods_eaten: int = 0
    moves_made: int = 0
    high_score: int = 0


class SnakeGame:
    """贪吃蛇游戏核心逻辑"""
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        初始化游戏
        
        Args:
            config: 游戏配置
        """
        self.config = config or GameConfig()
        self.state = GameState()
        self._move_history: List[Tuple[Direction, int]] = []
        self._food_history: List[Tuple[Position, int]] = []
        self.reset()
    
    def reset(self) -> None:
        """重置游戏"""
        self.state = GameState(speed=self.config.initial_speed)
        
        # 初始化蛇的位置（中间位置，水平排列）
        start_x = self.config.width // 2
        start_y = self.config.height // 2
        
        self.state.snake = [
            Position(start_x - i, start_y)
            for i in range(self.config.initial_length)
        ]
        
        self.state.direction = Direction.RIGHT
        self._move_history = []
        self._food_history = []
        self._spawn_food()
    
    def _spawn_food(self) -> None:
        """生成食物"""
        if not self.state.snake:
            return
        
        snake_positions = set(self.state.snake)
        available_positions = []
        
        for x in range(self.config.width):
            for y in range(self.config.height):
                pos = Position(x, y)
                if pos not in snake_positions:
                    available_positions.append(pos)
        
        if available_positions:
            self.state.food = random.choice(available_positions)
            self._food_history.append((self.state.food, self.state.moves_made))
    
    def set_direction(self, direction: Direction) -> bool:
        """
        设置移动方向
        
        Args:
            direction: 新方向
            
        Returns:
            是否成功设置（不能直接反向）
        """
        if direction == self.state.direction.opposite():
            return False
        self.state.direction = direction
        return True
    
    def move(self) -> bool:
        """
        执行一次移动
        
        Returns:
            游戏是否继续
        """
        if self.state.is_game_over or self.state.is_paused:
            return False
        
        # 计算新头部位置
        head = self.state.snake[0]
        delta = Position.from_direction(self.state.direction)
        new_head = head + delta
        
        # 边界处理
        if self.config.walls_kill:
            if not (0 <= new_head.x < self.config.width and 
                    0 <= new_head.y < self.config.height):
                self.state.is_game_over = True
                return False
        else:
            # 穿墙模式
            new_head.x = new_head.x % self.config.width
            new_head.y = new_head.y % self.config.height
        
        # 自身碰撞检测
        if self.config.self_collision_kills:
            if new_head in self.state.snake:
                self.state.is_game_over = True
                return False
        
        # 移动蛇
        self.state.snake.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.state.food:
            self._eat_food()
        else:
            self.state.snake.pop()
        
        self.state.moves_made += 1
        self._move_history.append((self.state.direction, self.state.moves_made))
        
        return not self.state.is_game_over
    
    def _eat_food(self) -> None:
        """处理吃到食物"""
        self.state.score += self.config.food_score
        self.state.foods_eaten += 1
        
        # 升级检测
        new_level = (self.state.score // self.config.level_up_score) + 1
        if new_level > self.state.level:
            self.state.level = new_level
            # 加速
            self.state.speed = max(
                self.config.min_speed,
                self.state.speed - self.config.speed_increment
            )
        
        # 更新最高分
        if self.state.score > self.state.high_score:
            self.state.high_score = self.state.score
        
        self._spawn_food()
    
    def toggle_pause(self) -> None:
        """切换暂停状态"""
        self.state.is_paused = not self.state.is_paused
    
    def is_win(self) -> bool:
        """检查是否获胜（蛇填满整个屏幕）"""
        return len(self.state.snake) >= self.config.width * self.config.height
    
    def get_snake_head(self) -> Optional[Position]:
        """获取蛇头位置"""
        return self.state.snake[0] if self.state.snake else None
    
    def get_snake_tail(self) -> Optional[Position]:
        """获取蛇尾位置"""
        return self.state.snake[-1] if self.state.snake else None
    
    def get_game_area(self) -> int:
        """获取游戏区域大小"""
        return self.config.width * self.config.height
    
    def get_occupancy(self) -> float:
        """获取蛇占据的面积比例"""
        return len(self.state.snake) / self.get_game_area()


class SnakeRenderer:
    """贪吃蛇渲染器"""
    
    # 渲染字符
    WALL_H = '─'
    WALL_V = '│'
    WALL_TL = '┌'
    WALL_TR = '┐'
    WALL_BL = '└'
    WALL_BR = '┘'
    SNAKE_HEAD = '●'
    SNAKE_BODY = '○'
    FOOD = '★'
    EMPTY = ' '
    
    def __init__(self, game: SnakeGame):
        """
        初始化渲染器
        
        Args:
            game: 游戏实例
        """
        self.game = game
    
    def render(self) -> str:
        """
        渲染游戏画面
        
        Returns:
            渲染后的字符串
        """
        lines = []
        
        # 顶部边框
        top_border = (
            self.WALL_TL + 
            self.WALL_H * self.game.config.width + 
            self.WALL_TR
        )
        lines.append(top_border)
        
        # 游戏区域
        for y in range(self.game.config.height):
            row = [self.WALL_V]
            for x in range(self.game.config.width):
                pos = Position(x, y)
                char = self._get_char(pos)
                row.append(char)
            row.append(self.WALL_V)
            lines.append(''.join(row))
        
        # 底部边框
        bottom_border = (
            self.WALL_BL + 
            self.WALL_H * self.game.config.width + 
            self.WALL_BR
        )
        lines.append(bottom_border)
        
        # 状态信息
        state = self.game.state
        status = (
            f"分数: {state.score} | "
            f"等级: {state.level} | "
            f"长度: {len(state.snake)} | "
            f"速度: {state.speed}ms"
        )
        lines.append(status)
        
        if state.is_game_over:
            lines.append("游戏结束! 按 R 重新开始")
        elif state.is_paused:
            lines.append("游戏暂停! 按 P 继续")
        else:
            lines.append("方向键移动 | P 暂停 | Q 退出")
        
        return '\n'.join(lines)
    
    def _get_char(self, pos: Position) -> str:
        """获取指定位置的字符"""
        # 蛇头
        if self.game.state.snake and pos == self.game.state.snake[0]:
            return self.SNAKE_HEAD
        
        # 蛇身
        if pos in self.game.state.snake[1:]:
            return self.SNAKE_BODY
        
        # 食物
        if pos == self.game.state.food:
            return self.FOOD
        
        return self.EMPTY
    
    def render_minimal(self) -> str:
        """
        简洁渲染模式（无边框）
        
        Returns:
            渲染后的字符串
        """
        lines = []
        
        for y in range(self.game.config.height):
            row = []
            for x in range(self.game.config.width):
                pos = Position(x, y)
                row.append(self._get_char(pos))
            lines.append(''.join(row))
        
        return '\n'.join(lines)


class SnakeAI:
    """贪吃蛇 AI（简单策略）"""
    
    def __init__(self, game: SnakeGame):
        """
        初始化 AI
        
        Args:
            game: 游戏实例
        """
        self.game = game
    
    def get_next_direction(self) -> Direction:
        """
        计算下一步方向
        
        Returns:
            推荐的移动方向
        """
        if not self.game.state.food or not self.game.state.snake:
            return self.game.state.direction
        
        head = self.game.state.snake[0]
        food = self.game.state.food
        
        # 简单策略：优先向食物方向移动
        possible_moves = self._get_safe_moves()
        
        if not possible_moves:
            # 无安全移动，保持当前方向
            return self.game.state.direction
        
        # 选择最接近食物的方向
        best_move = min(
            possible_moves,
            key=lambda d: self._distance(head + Position.from_direction(d), food)
        )
        
        return best_move
    
    def _get_safe_moves(self) -> List[Direction]:
        """获取安全的移动方向"""
        safe = []
        
        for direction in Direction:
            if direction == self.game.state.direction.opposite():
                continue
            
            if self._is_safe_move(direction):
                safe.append(direction)
        
        return safe
    
    def _is_safe_move(self, direction: Direction) -> bool:
        """检查移动是否安全"""
        head = self.game.state.snake[0]
        delta = Position.from_direction(direction)
        new_head = head + delta
        
        # 边界检查
        if self.game.config.walls_kill:
            if not (0 <= new_head.x < self.game.config.width and
                    0 <= new_head.y < self.game.config.height):
                return False
        
        # 自身碰撞检查
        if new_head in self.game.state.snake[:-1]:  # 排除尾部（会移动）
            return False
        
        return True
    
    def _distance(self, p1: Position, p2: Position) -> int:
        """计算曼哈顿距离"""
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)


class SnakeRecorder:
    """游戏录制器"""
    
    def __init__(self, game: SnakeGame):
        """
        初始化录制器
        
        Args:
            game: 游戏实例
        """
        self.game = game
        self.recording: List[Dict[str, Any]] = []
        self._recording = False
        self._start_time = 0
    
    def start_recording(self) -> None:
        """开始录制"""
        self.recording = []
        self._recording = True
        self._start_time = time.time()
    
    def stop_recording(self) -> None:
        """停止录制"""
        self._recording = False
    
    def record_frame(self) -> None:
        """记录当前帧"""
        if not self._recording:
            return
        
        frame = {
            'time': time.time() - self._start_time,
            'snake': [pos.to_tuple() for pos in self.game.state.snake],
            'food': self.game.state.food.to_tuple() if self.game.state.food else None,
            'direction': self.game.state.direction.name,
            'score': self.game.state.score,
            'is_game_over': self.game.state.is_game_over,
        }
        self.recording.append(frame)
    
    def save_replay(self, filename: str) -> None:
        """
        保存录像
        
        Args:
            filename: 文件名
        """
        import json
        data = {
            'config': {
                'width': self.game.config.width,
                'height': self.game.config.height,
            },
            'frames': self.recording,
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load_replay(self, filename: str) -> Dict[str, Any]:
        """
        加载录像
        
        Args:
            filename: 文件名
            
        Returns:
            录像数据
        """
        import json
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def replay(self, data: Dict[str, Any], callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        回放录像
        
        Args:
            data: 录像数据
            callback: 每帧回调函数
        """
        for frame in data.get('frames', []):
            callback(frame)
            time.sleep(0.05)  # 回放速度


class SnakeGameCLI:
    """贪吃蛇命令行界面"""
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        初始化 CLI
        
        Args:
            config: 游戏配置
        """
        self.game = SnakeGame(config)
        self.renderer = SnakeRenderer(self.game)
        self.ai = SnakeAI(self.game)
        self.recorder = SnakeRecorder(self.game)
        self._use_ai = False
        self._old_settings = None
    
    def _setup_terminal(self) -> None:
        """设置终端"""
        # 隐藏光标
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
        
        # 设置非阻塞输入
        try:
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except:
            pass
    
    def _restore_terminal(self) -> None:
        """恢复终端设置"""
        # 显示光标
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
        
        # 恢复终端设置
        if self._old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
            except:
                pass
    
    def _clear_screen(self) -> None:
        """清屏"""
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
    
    def _get_key(self) -> Optional[str]:
        """获取按键"""
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
    
    def run(self, use_ai: bool = False) -> None:
        """
        运行游戏
        
        Args:
            use_ai: 是否使用 AI 自动游戏
        """
        self._use_ai = use_ai
        self._setup_terminal()
        self.recorder.start_recording()
        
        try:
            while True:
                self._clear_screen()
                print(self.renderer.render())
                
                # 处理输入
                if self._use_ai:
                    direction = self.ai.get_next_direction()
                    self.game.set_direction(direction)
                else:
                    key = self._get_key()
                    if key:
                        self._handle_key(key)
                
                # 移动
                if not self.game.state.is_paused and not self.game.state.is_game_over:
                    self.game.move()
                
                self.recorder.record_frame()
                
                # 检查游戏结束
                if self.game.state.is_game_over:
                    time.sleep(1)
                    # 等待重新开始或退出
                    while True:
                        key = self._get_key()
                        if key:
                            if key.lower() == 'r':
                                self.game.reset()
                                self.recorder.start_recording()
                                break
                            elif key.lower() == 'q':
                                return
                        time.sleep(0.05)
                
                time.sleep(self.game.state.speed / 1000.0)
                
        finally:
            self.recorder.stop_recording()
            self._restore_terminal()
    
    def _handle_key(self, key: str) -> None:
        """处理按键"""
        key_map = {
            'w': Direction.UP,
            'W': Direction.UP,
            's': Direction.DOWN,
            'S': Direction.DOWN,
            'a': Direction.LEFT,
            'A': Direction.LEFT,
            'd': Direction.RIGHT,
            'D': Direction.RIGHT,
        }
        
        # 方向键（ANSI 转义序列）
        if key == '\x1b':
            # 可能是方向键
            next_chars = []
            import select
            while select.select([sys.stdin], [], [], 0.01)[0]:
                next_chars.append(sys.stdin.read(1))
            
            seq = ''.join(next_chars)
            if seq == '[A':
                key = 'w'
            elif seq == '[B':
                key = 's'
            elif seq == '[C':
                key = 'd'
            elif seq == '[D':
                key = 'a'
        
        if key in key_map:
            self.game.set_direction(key_map[key])
        elif key.lower() == 'p':
            self.game.toggle_pause()
        elif key.lower() == 'r':
            self.game.reset()
        elif key.lower() == 'q':
            raise KeyboardInterrupt


class SnakeGameUtils:
    """贪吃蛇工具集（便捷接口）"""
    
    @staticmethod
    def create_game(
        width: int = 20,
        height: int = 15,
        speed: int = 150
    ) -> SnakeGame:
        """
        创建游戏实例
        
        Args:
            width: 宽度
            height: 高度
            speed: 初始速度（毫秒）
            
        Returns:
            游戏实例
        """
        config = GameConfig(width=width, height=height, initial_speed=speed)
        return SnakeGame(config)
    
    @staticmethod
    def play(
        width: int = 20,
        height: int = 15,
        use_ai: bool = False
    ) -> int:
        """
        开始游戏
        
        Args:
            width: 宽度
            height: 高度
            use_ai: 是否使用 AI
            
        Returns:
            最终得分
        """
        config = GameConfig(width=width, height=height)
        cli = SnakeGameCLI(config)
        try:
            cli.run(use_ai=use_ai)
        except KeyboardInterrupt:
            pass
        return cli.game.state.score
    
    @staticmethod
    def simulate_game(
        width: int = 20,
        height: int = 15,
        max_moves: int = 1000
    ) -> Dict[str, Any]:
        """
        模拟一局游戏
        
        Args:
            width: 宽度
            height: 高度
            max_moves: 最大移动次数
            
        Returns:
            游戏结果
        """
        game = SnakeGame(GameConfig(width=width, height=height))
        ai = SnakeAI(game)
        
        while not game.state.is_game_over and game.state.moves_made < max_moves:
            direction = ai.get_next_direction()
            game.set_direction(direction)
            game.move()
        
        return {
            'score': game.state.score,
            'length': len(game.state.snake),
            'moves': game.state.moves_made,
            'foods_eaten': game.state.foods_eaten,
            'level': game.state.level,
            'occupancy': game.get_occupancy(),
            'won': game.is_win(),
        }


# =============================================================================
# 便捷函数
# =============================================================================

def play_snake(width: int = 20, height: int = 15, use_ai: bool = False) -> int:
    """
    开始贪吃蛇游戏（便捷函数）
    
    Args:
        width: 游戏区域宽度
        height: 游戏区域高度
        use_ai: 是否使用 AI 自动游戏
        
    Returns:
        最终得分
    """
    return SnakeGameUtils.play(width=width, height=height, use_ai=use_ai)


def create_snake_game(width: int = 20, height: int = 15) -> SnakeGame:
    """
    创建贪吃蛇游戏实例（便捷函数）
    
    Args:
        width: 宽度
        height: 高度
        
    Returns:
        游戏实例
    """
    return SnakeGameUtils.create_game(width=width, height=height)


def simulate_snake_game(
    width: int = 20,
    height: int = 15,
    max_moves: int = 1000
) -> Dict[str, Any]:
    """
    模拟贪吃蛇游戏（便捷函数）
    
    Args:
        width: 宽度
        height: 高度
        max_moves: 最大移动次数
        
    Returns:
        模拟结果
    """
    return SnakeGameUtils.simulate_game(
        width=width, height=height, max_moves=max_moves
    )


def run_snake_tournament(
    games: int = 10,
    width: int = 20,
    height: int = 15
) -> Dict[str, Any]:
    """
    运行贪吃蛇锦标赛（便捷函数）
    
    Args:
        games: 游戏局数
        width: 宽度
        height: 高度
        
    Returns:
        锦标赛统计
    """
    results = []
    
    for _ in range(games):
        result = simulate_snake_game(width=width, height=height)
        results.append(result)
    
    scores = [r['score'] for r in results]
    lengths = [r['length'] for r in results]
    moves = [r['moves'] for r in results]
    
    return {
        'games': games,
        'scores': scores,
        'average_score': sum(scores) / len(scores),
        'max_score': max(scores),
        'min_score': min(scores),
        'average_length': sum(lengths) / len(lengths),
        'average_moves': sum(moves) / len(moves),
    }


# =============================================================================
# 主函数
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Snake Game Utils - 贪吃蛇游戏工具库")
    print("=" * 60)
    
    # 模拟游戏测试
    print("\n【模拟游戏测试】")
    result = simulate_snake_game(width=15, height=10)
    print(f"  得分: {result['score']}")
    print(f"  长度: {result['length']}")
    print(f"  移动次数: {result['moves']}")
    print(f"  吃食物数: {result['foods_eaten']}")
    print(f"  等级: {result['level']}")
    print(f"  占据率: {result['occupancy']:.2%}")
    
    # 渲染测试
    print("\n【渲染测试】")
    game = create_snake_game(width=15, height=8)
    renderer = SnakeRenderer(game)
    print(renderer.render())
    
    # 执行几步移动
    print("\n【执行移动】")
    game.move()  # 右
    game.move()  # 右
    game.set_direction(Direction.DOWN)
    game.move()  # 下
    print(renderer.render())
    
    # 锦标赛测试
    print("\n【AI 锦标赛 (5局)】")
    tournament = run_snake_tournament(games=5, width=15, height=10)
    print(f"  平均得分: {tournament['average_score']:.1f}")
    print(f"  最高得分: {tournament['max_score']}")
    print(f"  平均长度: {tournament['average_length']:.1f}")
    
    print("\n" + "=" * 60)
    print("提示: 运行 play_snake() 开始交互式游戏")
    print("=" * 60)