# Snake Game Utils 🐍

贪吃蛇游戏引擎与 AI 工具，提供完整的游戏逻辑、AI 算法和录制回放功能。

## 特性

- ✅ **游戏引擎** - 完整的贪吃蛇游戏逻辑
- ✅ **多种 AI** - 内置 AI 算法自动玩
- ✅ **录制回放** - 记录并回放游戏过程
- ✅ **CLI 界面** - 命令行玩贪吃蛇
- ✅ **统计分析** - 游戏数据统计

## 快速开始

### 基本游戏

```python
from snake_game_utils import SnakeGame, Direction, GameConfig

config = GameConfig(width=20, height=20)
game = SnakeGame(config)

# 设置方向
game.set_direction(Direction.RIGHT)

# 运行一步
game.update()

# 获取状态
state = game.get_state()
print(f"分数: {state.score}")
print(f"蛇长度: {len(state.snake)}")
```

### 使用 AI

```python
from snake_game_utils import SnakeAI, SnakeGame

game = SnakeGame()
ai = SnakeAI(game)

# AI 决策下一步
next_direction = ai.get_next_direction()
game.set_direction(next_direction)
```

## API 参考

### 类

| 类 | 说明 |
|---|------|
| `Direction` | 方向枚举 |
| `Position` | 位置坐标 |
| `GameConfig` | 游戏配置 |
| `GameState` | 游戏状态 |
| `SnakeGame` | 游戏引擎 |
| `SnakeAI` | AI 控制器 |
| `SnakeRecorder` | 录制器 |
| `SnakeGameCLI` | 命令行界面 |

### 核心函数

| 函数 | 说明 |
|------|------|
| `SnakeGame.update()` | 更新游戏状态 |
| `SnakeAI.get_next_direction()` | AI 决策 |
| `SnakeRecorder.record(state)` | 录制状态 |
| `SnakeRecorder.replay()` | 回放录制 |
