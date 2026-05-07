# Reversi Utils

黑白棋（Reversi/Othello）游戏工具库 - 零依赖，生产就绪

## 简介

黑白棋是一种经典的双人策略棋盘游戏。本模块提供完整的黑白棋实现，包括：

- 游戏棋盘管理
- 落子验证和执行
- 棋子翻转逻辑
- 游戏结束判定
- AI 对手（Minimax 算法）
- 游戏序列化/反序列化

## 核心功能

### 棋盘管理

```python
from reversi_utils.mod import ReversiBoard, BLACK, WHITE

# 创建标准 8x8 棋盘
board = ReversiBoard()

# 查看棋盘
print(board)

# 获取棋子数量
black, white, empty = board.count_pieces()
```

### 落子操作

```python
# 获取当前玩家的有效落子位置
valid_moves = board.get_valid_moves()

# 检查某个位置是否有效
is_valid = board.is_valid_move(2, 3)

# 落子并翻转对方棋子
board.make_move(2, 3)

# 检查游戏是否结束
is_over = board.is_game_over()
```

### AI 对手

```python
from reversi_utils.mod import get_best_move, get_greedy_move

# 使用 Minimax 算法（深度可调）
best_move = get_best_move(board, BLACK, depth=4)
board.make_move(best_move[0], best_move[1])

# 使用贪心策略（快速）
greedy_move = get_greedy_move(board, WHITE)
```

### 游戏分析

```python
from reversi_utils.mod import analyze_game, evaluate_position

# 分析当前局面
analysis = analyze_game(board)
print(analysis['black_pieces'])
print(analysis['white_pieces'])
print(analysis['position_score'])

# 评估位置得分（针对某个玩家）
score = evaluate_position(board, BLACK)
```

### 序列化

```python
# 保存游戏状态
data = board.serialize()

# 加载游戏状态
loaded_board = ReversiBoard.deserialize(data)

# FEN 格式（类似国际象棋）
fen = board.to_fen()
restored = ReversiBoard.from_fen(fen)
```

## API 参考

### ReversiBoard 类

| 方法 | 描述 |
|------|------|
| `ReversiBoard(size=8)` | 创建棋盘（默认 8x8） |
| `get(row, col)` | 获取指定位置的棋子 |
| `is_valid_move(row, col)` | 检查落子是否有效 |
| `get_valid_moves()` | 获取所有有效落子位置 |
| `make_move(row, col)` | 落子并翻转 |
| `count_pieces()` | 统计棋子数量 |
| `get_score()` | 获取当前分数 |
| `is_game_over()` | 检查游戏是否结束 |
| `get_winner()` | 获取获胜者（BLACK/WHITE/None） |
| `copy()` | 复制棋盘 |
| `serialize()` | 序列化游戏状态 |
| `to_fen()` | 导出为 FEN 格式 |

### AI 函数

| 函数 | 描述 |
|------|------|
| `get_best_move(board, player, depth=4)` | Minimax AI（较慢但更强） |
| `get_greedy_move(board, player)` | 贪心 AI（快速） |
| `evaluate_position(board, player)` | 评估位置得分 |

### 常量

| 常量 | 值 | 描述 |
|------|-----|------|
| `EMPTY` | 0 | 空格 |
| `BLACK` | 1 | 黑棋（先行） |
| `WHITE` | 2 | 白棋 |

## 游戏规则

1. 标准 8x8 棋盘
2. 黑棋先行
3. 初始状态：中央 4 个棋子交叉放置
4. 落子必须"夹住"对方至少一个棋子
5. 被夹住的棋子全部翻转
6. 无法落子时跳过回合
7. 双方都无法落子时游戏结束
8. 棋子多的一方获胜

## 测试

```bash
python Python/reversi_utils/reversi_utils_test.py
```

## 示例

```bash
python Python/reversi_utils/examples/usage_examples.py
```

## 依赖

无外部依赖，仅使用 Python 标准库。

## 许可证

MIT License