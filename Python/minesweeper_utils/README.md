# Minesweeper Utils 💣

扫雷游戏工具模块 - 提供完整的扫雷游戏逻辑实现。

## 功能特性

- **多难度预设** - 初级、中级、高级、自定义
- **随机雷区生成** - 首次点击安全保证
- **自动计算雷数** - 周围雷数自动计算
- **安全区域展开** - 洪水填充算法
- **标记支持** - 旗帜、问号标记
- **游戏状态检测** - 胜利/失败判断
- **序列化** - 游戏板导入导出
- **求解提示** - 安全格子推荐

## 快速开始

```python
from minesweeper_utils.mod import MinesweeperGame, Difficulty

# 创建游戏（初级难度）
game = MinesweeperGame(Difficulty.BEGINNER)

# 或自定义难度
game = MinesweeperGame(rows=10, cols=10, mines=15)

# 点击格子
game.click(row=0, col=0)

# 标记旗帜
game.flag(row=5, col=3)

# 检查游戏状态
if game.is_won():
    print("胜利！")
elif game.is_lost():
    print("踩雷了！")
```

## 核心类

### MinesweeperGame

```python
from minesweeper_utils.mod import MinesweeperGame, Difficulty

# 预设难度
game = MinesweeperGame(Difficulty.BEGINNER)   # 9×9, 10雷
game = MinesweeperGame(Difficulty.INTERMEDIATE) # 16×16, 40雷
game = MinesweeperGame(Difficulty.EXPERT)     # 30×16, 99雷

# 自定义
game = MinesweeperGame(rows=20, cols=20, mines=50)

# 游戏操作
game.click(3, 4)        # 点击
game.flag(5, 6)         # 标记旗帜
game.question(5, 6)     # 标记问号
game.unflag(5, 6)       # 取消标记
```

## 游戏信息

```python
# 获取游戏板状态
board = game.get_board()

# 获取统计信息
stats = game.get_stats()
# {
#     'total_cells': 81,
#     'revealed': 25,
#     'flagged': 5,
#     'mines': 10,
#     'time_elapsed': 45
# }

# 获取剩余雷数
remaining = game.get_remaining_mines()
```

## 难度设置

| 难度 | 尺寸 | 雷数 |
|------|------|------|
| 初级 | 9×9 | 10 |
| 中级 | 16×16 | 40 |
| 高级 | 30×16 | 99 |

## 序列化

```python
# 导出游戏状态
state = game.export_state()

# 导入游戏状态
game = MinesweeperGame()
game.import_state(state)

# JSON 格式
json_data = game.to_json()
game.from_json(json_data)
```

## 求解提示

```python
from minesweeper_utils.mod import get_safe_cells_hint

# 获取推荐的安全格子
safe_cells = get_safe_cells_hint(game)
for row, col in safe_cells:
    print(f"建议点击 ({row}, {col})")
```

## 游戏状态

```python
from minesweeper_utils.mod import GameState

state = game.get_state()

if state == GameState.PLAYING:
    print("游戏进行中")
elif state == GameState.WON:
    print("胜利！")
elif state == GameState.LOST:
    print("踩雷失败")
```

## 测试

```bash
python Python/minesweeper_utils/minesweeper_utils_test.py
```

## 许可证

MIT License