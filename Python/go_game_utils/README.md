# go_game_utils - 围棋工具模块

围棋游戏完整实现，零外部依赖。

## 功能

- **棋盘管理**: 9x9, 13x13, 19x19 标准棋盘
- **落子规则**: 禁入点、自杀检测、打劫规则
- **提子规则**: 气的计算、连通组识别、自动提子
- **死活判断**: 眼的识别、活棋/死棋判定
- **领地计算**: 中国规则、日本规则
- **SGF 格式**: 导出、解析 Smart Game Format
- **计分系统**: 中国规则、日本规则计分
- **棋形识别**: 打吃检测、劫材分析
- **让子设置**: 标准 2-9 子让子布局

## 使用示例

### 创建棋盘

```python
from mod import GoBoard, Stone

# 19路标准棋盘
board = GoBoard(19)

# 9路小棋盘
board9 = GoBoard(9)

# 13路中棋盘
board13 = GoBoard(13)
```

### 落子

```python
# 黑方先行
board.play(3, 3)  # 黑方左上星位
board.play(15, 15)  # 白方右下星位
board.play(3, 15)  # 黑方右上星位

# 检查落子合法性
legal, reason = board.is_legal_move(4, 4)
print(f"合法: {legal}, 原因: {reason}")
```

### 提子

```python
# 气的计算
board.play(4, 4)
liberties = board.count_liberties(4, 4)  # 4气

# 连通组
board.play(4, 3)
group = board.get_group(4, 4)  # {(4,4), (4,3)}
liberties = board.count_liberties(4, 4)  # 6气（连接后）
```

### 打劫规则

```python
# 打劫检测
if board.is_ko(row, col):
    print("打劫点，不能立即落子")

# 打劫点会在提子后自动设置
# 下一步必须先在其他位置落子
```

### 领地计算

```python
from mod import Territory

territory = Territory.calculate(board)
print(f"黑方领地: {territory[Stone.BLACK]}")
print(f"白方领地: {territory[Stone.WHITE]}")
```

### 计分

```python
from mod import ScoreCalculator

# 中国规则（子数+领地）
score = ScoreCalculator.calculate_chinese_score(board, komi=7.5)
print(f"黑方: {score['black']['total']} 目")
print(f"白方: {score['white']['total']} 目")

# 日本规则（领地+提子）
score = ScoreCalculator.calculate_japanese_score(board, komi=6.5)
```

### SGF 格式

```python
from mod import SGF

# 导出
sgf = SGF.export(board, black_name="黑方", white_name="白方")

# 解析
parsed_board = SGF.parse("(;SZ[9];B[dd];W[cd])")
```

### 死活分析

```python
from mod import LifeDeath

# 分析棋子组
analysis = LifeDeath.analyze_group(board, 4, 4)
print(f"大小: {analysis['size']}")
print(f"气数: {analysis['liberties']}")
print(f"状态: {analysis['status']}")

# 找眼
eyes = LifeDeath.get_eyes(board, Stone.BLACK)
```

### 棋形识别

```python
from mod import Pattern

# 打吃检测
is_atari = Pattern.is_atari(board, row, col)

# 找打吃组
atari_groups = Pattern.find_atari_groups(board, Stone.BLACK)

# 劫材
threats = Pattern.find_ko_threats(board)
```

### 让子设置

```python
from mod import Handicap

board = GoBoard(19)
Handicap.setup_handicap(board, 3)  # 3子让子

# 让子后白方先行
print(f"当前玩家: {board.current_player}")
```

### 坐标转换

```python
from mod import coord_to_sgf, sgf_to_coord, coord_to_label, label_to_coord

# SGF 格式
sgf = coord_to_sgf(4, 4)  # "dd"
coord = sgf_to_coord("dd")  # (4, 4)

# 棋盘标记（跳过 I）
label = coord_to_label(8, 8)  # "J9"
coord = label_to_coord("J9")  # (8, 8)
```

## API 参考

### GoBoard 类

| 方法 | 说明 |
|------|------|
| `play(row, col)` | 落子 |
| `is_legal_move(row, col)` | 检查合法性 |
| `get(row, col)` | 获取棋子 |
| `set(row, col, stone)` | 设置棋子 |
| `get_group(row, col)` | 获取连通组 |
| `count_liberties(row, col)` | 计算气数 |
| `is_ko(row, col)` | 检查打劫点 |
| `pass_turn()` | 虚手 |
| `is_game_over()` | 检查游戏结束 |
| `reset()` | 重置棋盘 |
| `copy()` | 创建副本 |

### Territory 类

| 方法 | 说明 |
|------|------|
| `calculate(board)` | 计算领地 |
| `get_territory_map(board)` | 获取领地归属图 |

### ScoreCalculator 类

| 方法 | 说明 |
|------|------|
| `calculate_chinese_score(board, komi)` | 中国规则计分 |
| `calculate_japanese_score(board, komi)` | 日本规则计分 |

### SGF 类

| 方法 | 说明 |
|------|------|
| `export(board, ...)` | 导出 SGF |
| `parse(sgf_content)` | 解析 SGF |

## 测试

```bash
python go_game_utils_test.py
```

## 许可证

MIT License