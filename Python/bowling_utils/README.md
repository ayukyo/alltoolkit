# Bowling Utils

保龄球计分工具，零依赖，支持完整保龄球规则。

## 功能特性

- **多种输入格式**: 字符串、列表、元组
- **完整计分**: Strike/Spare 奖分计算
- **逐局分解**: 每局得分详情
- **验证输入**: 详细错误提示
- **统计信息**: Strike、Spare、平均得分
- **完美局/零分局**: 检测
- **最大可能得分**: 从当前状态推算

## 快速开始

```python
from bowling_utils.mod import calculate_score, parse_game

# 从字符串计算得分
score = calculate_score("X X X X X X X X X XXX")
print(score)  # 300（完美局）

# 从列表计算
score = calculate_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
```

## 使用示例

### 基础计分

```python
from bowling_utils.mod import calculate_score

# 字符串格式
# X = Strike, / = Spare, - = Gutter（零分）, 数字 = 具体得分
score = calculate_score("X 7/ 9- X X 8/ 9/ 7- X X X9")  # 168

# 列表格式
score = calculate_score([10, 7, 3, 9, 0, 10, 10, 8, 2, 9, 1, 7, 0, 10, 10, 10, 9])

# 元组格式
score = calculate_score((10, 7, 3, 9, 0, 10, 10, 8, 2, 9, 1, 7, 0, 10, 10, 10, 9))
```

### 详细结果

```python
from bowling_utils.mod import analyze_game

game = analyze_game("X X X X X X X X X XXX")

print(f"总分: {game.total_score}")
print(f"Strike 数: {game.strikes}")
print(f"Spare 数: {game.spares}")
print(f"是否完美局: {game.is_perfect}")

# 查看每局详情
for frame in game.frames:
    print(f"第{frame.frame_number}局: {frame.roll_symbols} = {frame.frame_score}")
```

### 逐局分解

```python
from bowling_utils.mod import get_frame_breakdown

breakdown = get_frame_breakdown("7/ 9- X X 8/ 9/ 7- X X X9")

for frame_info in breakdown:
    print(f"局 {frame_info['frame']}: {frame_info['rolls']} -> {frame_info['score']}")
```

### 输入解析

```python
from bowling_utils.mod import parse_game, parse_roll_symbol

# 解析单次投球符号
pins = parse_roll_symbol('X')  # 10 (Strike)
pins = parse_roll_symbol('/')  # 补球数（需要上下文）
pins = parse_roll_symbol('7')  # 7
pins = parse_roll_symbol('-')  # 0 (Gutter)

# 解析整局游戏
rolls = parse_game("X 7/ 9- X")
```

### 验证输入

```python
from bowling_utils.mod import validate_game

# 验证游戏输入
is_valid, errors = validate_game("X X X X X X X X X XX")
if not is_valid:
    for error in errors:
        print(error)
```

### 最大可能得分

```python
from bowling_utils.mod import get_max_possible_score

# 从当前状态推算最大可能得分
# 假设打了前 5 局
max_score = get_max_possible_score([10, 10, 10, 10, 10])
print(f"剩余全 Strike 可达最高分: {max_score}")  # 300
```

### 统计信息

```python
from bowling_utils.mod import BowlingGame

game = BowlingGame.from_string("X 7/ 9- X X 8/")

print(f"Strike 数: {game.strikes}")
print(f"Spare 数: {game.spares}")
print(f"零分投球数: {game.gutter_rolls}")
print(f"平均每局得分: {game.average_pins_per_frame}")
```

## 保龄球计分规则

### Strike（全中）

- 第 10 局前：得分 = 10 + 后两次投球得分
- 第 10 局：两次额外投球

### Spare（补中）

- 第 10 局前：得分 = 10 + 后一次投球得分
- 第 10 局：一次额外投球

### Open Frame（未补中）

- 得分 = 两次投球实际得分

### 第 10 局特殊规则

- Strike: 两次额外投球
- Spare: 一次额外投球
- Open: 无额外投球

## 输入符号

| 符号 | 说明 | 得分 |
|------|------|------|
| X | Strike（全中） | 10 |
| / | Spare（补中） | 10 - 第一投 |
| - | Gutter（零分） | 0 |
| 1-9 | 具体得分 | 对应数字 |

## API 参考

| 函数 | 说明 |
|------|------|
| `calculate_score(input)` | 计算总分 |
| `analyze_game(input)` | 详细分析 |
| `parse_game(string)` | 解析字符串 |
| `parse_roll_symbol(symbol)` | 解析单次投球 |
| `validate_game(input)` | 验证输入 |
| `get_frame_breakdown(input)` | 逐局分解 |
| `get_max_possible_score(rolls)` | 最大可能得分 |

### BowlingGame 类

| 属性 | 说明 |
|------|------|
| `total_score` | 总分 |
| `frames` | 每局详情列表 |
| `strikes` | Strike 数 |
| `spares` | Spare 数 |
| `is_perfect` | 是否完美局（300） |
| `is_gutter_game` | 是否零分局 |
| `is_complete` | 是否完整 |

### FrameScore 类

| 属性 | 说明 |
|------|------|
| `frame_number` | 局号（1-10） |
| `rolls` | 投球得分列表 |
| `roll_symbols` | 显示符号 |
| `frame_score` | 累计得分 |
| `is_strike` | 是否 Strike |
| `is_spare` | 是否 Spare |
| `is_open` | 是否 Open |

## 示例得分

| 输入 | 得分 | 说明 |
|------|------|------|
| X X X X X X X X X XXX | 300 | 完美局 |
| - - - - - - - - - - | 0 | 零分局 |
| X 7/ 9- X X 8/ 9/ 7- X X X9 | 168 | 典型局 |

---

**测试覆盖**: 完整测试套件，覆盖计分规则、输入解析、边界情况等