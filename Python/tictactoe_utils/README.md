# Tic-Tac-Toe Utils (井字棋工具)

一个功能完整的井字棋游戏工具模块，支持 AI 对弈、游戏管理、胜负判断等功能。

## 功能特性

- 🎮 **完整游戏状态管理**：棋盘操作、走法验证、撤销功能
- 🤖 **智能 AI 对手**：Minimax 算法实现，支持三种难度
- 🏆 **胜负判断**：实时检测获胜和平局
- 💾 **序列化支持**：支持 JSON 和字符串格式存储/恢复
- 📊 **位置评估**：评估棋盘局势优劣
- ⚡ **零外部依赖**：纯 Python 标准库实现

## 快速开始

### 基本用法

```python
from tictactoe_utils import TicTacToeBoard, TicTacToeAI, find_best_move

# 创建棋盘
board = TicTacToeBoard()

# 走棋
board.make_move(1, 1)  # X 占中心
board.make_move(0, 0)  # O 占左上角

# 显示棋盘
print(board)
# 输出:
#  O |   |  
# ---+---+---
#    | X |  
# ---+---+---
#    |   |  

# 检查当前玩家
print(board.current_player)  # Player.X

# 获取最佳走法建议
best = find_best_move(board)
print(f"建议走法: {best}")
```

### AI 对弈

```python
from tictactoe_utils import TicTacToeAI, TicTacToeBoard

# 创建困难模式 AI
ai = TicTacToeAI(difficulty='hard')

board = TicTacToeBoard()
board.make_move(0, 0)  # X 先手
board.make_move(1, 1)  # O 占中心

# 让 AI 选择最佳走法
move = ai.get_move(board)
print(f"AI 建议走: {move}")
```

### 完整游戏管理

```python
from tictactoe_utils import TicTacToeGame, GameResult

# 创建游戏：人类(X) vs AI(O)
game = TicTacToeGame(x_player='human', o_player='ai_hard')

# 人类走棋
game.make_move(1, 1)

# AI 走棋
game.ai_move()

# 查看状态
print(game)

# 游戏结束后查看结果
if game.is_game_over:
    print(f"结果: {game.result}")
```

### AI 自动对弈

```python
from tictactoe_utils import TicTacToeGame

# 困难 AI vs 困难 AI
game = TicTacToeGame(x_player='ai_hard', o_player='ai_hard')
result = game.auto_play()

print(game.board)
print(f"结果: {result.value}")
```

## API 文档

### TicTacToeBoard

棋盘类，管理游戏状态。

#### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `board` | List[List[Player]] | 棋盘状态副本 |
| `current_player` | Player | 当前应走棋的玩家 |
| `move_count` | int | 已走步数 |

#### 方法

| 方法 | 描述 |
|------|------|
| `make_move(row, col, player=None)` | 在指定位置落子 |
| `undo_move()` | 撤销上一步 |
| `get_available_moves()` | 获取所有可用走法 |
| `is_valid_move(row, col)` | 检查走法是否有效 |
| `get_winner()` | 获取获胜者 |
| `get_winning_line()` | 获取获胜线坐标 |
| `check_result()` | 检查游戏结果 |
| `is_game_over()` | 检查游戏是否结束 |
| `to_string()` | 序列化为字符串 |
| `to_json()` | 序列化为 JSON |
| `from_string(s)` | 从字符串恢复 |
| `from_json(s)` | 从 JSON 恢复 |
| `copy()` | 深拷贝棋盘 |

### TicTacToeAI

AI 玩家类，使用 Minimax 算法。

#### 构造函数

```python
ai = TicTacToeAI(difficulty='hard')
```

**难度选项：**
- `'easy'`：随机走法
- `'medium'`：50% 概率使用最优走法
- `'hard'`：始终使用最优走法（Minimax + Alpha-Beta 剪枝）

#### 方法

| 方法 | 描述 |
|------|------|
| `get_move(board)` | 返回 AI 选择的走法 (row, col) |

### TicTacToeGame

游戏管理类，支持人机对战和 AI 对战。

#### 构造函数

```python
game = TicTacToeGame(x_player='human', o_player='ai_medium')
```

**玩家类型：**
- `'human'`：人类玩家
- `'random'`：随机走法
- `'ai_easy'`：简单 AI
- `'ai_medium'`：中等 AI
- `'ai_hard'`：困难 AI

#### 方法

| 方法 | 描述 |
|------|------|
| `make_move(row, col)` | 人类玩家走棋 |
| `ai_move()` | AI 玩家走棋 |
| `auto_play()` | 自动完成游戏 |
| `reset()` | 重置游戏 |
| `get_move_suggestion()` | 获取走法建议 |

### 便捷函数

```python
# 创建对象
board = create_board()
ai = create_ai(difficulty='hard')
game = create_game(x_player='human', o_player='ai_hard')

# 获取最佳走法
best_move = find_best_move(board)

# 评估局势
score = evaluate_position(board, Player.X)

# 快速进行一局 AI 对战
result = play_game(x_strategy='ai_hard', o_strategy='ai_medium')
```

## 测试

运行测试：

```bash
cd tictactoe_utils
python tictactoe_utils_test.py
```

测试覆盖（34 个测试用例，100% 通过）：
- ✅ 棋盘基本操作（创建、走棋、撤销）
- ✅ 胜负判断（横、竖、斜、平局）
- ✅ AI 决策（获胜走法、阻止对手、抢占中心）
- ✅ 游戏管理（人类走棋、AI 走棋、自动对弈）
- ✅ 序列化/反序列化（字符串、JSON）
- ✅ 边缘情况（满盘无胜者、无效输入、连续撤销）
- ✅ 性能测试（AI 响应时间 < 500ms）

## 示例输出

```
=== 井字棋工具示例 ===

示例 1：基本操作
 O |   | X
---+---+---
 X | X |  
---+---+---
   |   | O
当前玩家: X

示例 2：AI vs AI (困难模式)
 X | O | X
---+---+---
 X | O | X
---+---+---
 O | X | O
结果: DRAW

示例 3：获取走法建议
 X |   |  
---+---+---
   | O |  
---+---+---
    |   |  
建议走法: (0, 2)
```

## 算法说明

### Minimax 算法

困难模式使用 Minimax 算法进行决策，配合 Alpha-Beta 剪枝优化：

1. **最大化玩家**：AI 轮次，选择分数最大的走法
2. **最小化玩家**：对手轮次，选择分数最小的走法
3. **终止条件**：游戏结束（胜/负/平）或达到深度限制

### 评分规则

| 结果 | AI 玩家分数 | 对手分数 |
|------|-------------|----------|
| AI 获胜 | +10 - depth | -10 + depth |
| 对手获胜 | -10 + depth | +10 - depth |
| 平局 | 0 | 0 |

- `depth` 表示搜索深度，鼓励快速获胜

### 位置权重

作为平局决胜，使用位置权重：

```
[3, 2, 3]
[2, 4, 2]
[3, 2, 3]
```

中心（4）最重要，角（3）次之，边（2）最低。

## 文件结构

```
tictactoe_utils/
├── mod.py                 # 主模块
├── tictactoe_utils_test.py # 测试文件（34 测试）
└── README.md              # 本文档
```

## 许可证

MIT License