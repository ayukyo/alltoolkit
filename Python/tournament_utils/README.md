# Tournament Utilities - 锦标赛赛程生成器

零外部依赖的锦标赛管理工具，支持多种赛制。

## 功能特性

- **单败淘汰赛** (Single Elimination) - 输一场即淘汰
- **双败淘汰赛** (Double Elimination) - 输两场才淘汰
- **循环赛** (Round Robin) - 每个人都与其他人对战
- **瑞士制** (Swiss System) - 固定轮次，按积分配对

### 核心功能

- ✅ 种子选手处理（高种子选手分开）
- ✅ 轮空自动处理（奇数参赛者）
- ✅ 比分记录与自动判定胜者
- ✅ 积分榜与排名
- ✅ 赛程可视化
- ✅ JSON 导出

## 快速开始

```python
from tournament_utils import (
    create_single_elimination,
    create_double_elimination,
    create_round_robin,
    create_swiss
)
```

### 单败淘汰赛

```python
# 创建8人淘汰赛，带种子排名
names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
seeds = [1, 8, 4, 5, 3, 6, 2, 7]  # 1号种子 vs 8号种子...
tournament = create_single_elimination(names, seeds)

# 可视化对阵表
print(tournament.visualize())

# 设置比赛结果
match = tournament.get_round_matches(1)[0]
tournament.set_winner(match.id, match.participant1.id)

# 或设置比分（自动判定胜者）
tournament.set_score(match.id, 3, 1)

# 检查是否完成
if tournament.is_completed():
    print(f"冠军: {tournament.get_winner().name}")

# 导出为字典
data = tournament.to_dict()
```

### 双败淘汰赛

```python
# 创建双败淘汰赛
tournament = create_double_elimination(["A", "B", "C", "D", "E", "F", "G", "H"])

# 设置胜者组比赛结果
for match in tournament.winners_bracket.values():
    if match.participant1 and match.participant2:
        tournament.set_winner_winner(match.id, match.participant1.id)
        # 败者会自动进入败者组

# 设置败者组比赛结果
for match in tournament.losers_bracket.values():
    if match.participant1 and match.participant2:
        tournament.set_loser_winner(match.id, match.participant1.id)

# 设置总决赛胜者
tournament.set_grand_final_winner(tournament.grand_final.participant1.id)

print(f"冠军: {tournament.get_winner().name}")
```

### 循环赛

```python
# 创建4人循环赛
tournament = create_round_robin(["张三", "李四", "王五", "赵六"])

# 设置比赛结果 (支持平局)
tournament.set_result(0, 3, 1)  # 张三 3-1 李四
tournament.set_result(1, 2, 2)  # 王五 2-2 赵六 (平局)

# 查看积分榜
standings = tournament.get_standings()
for rank, s in enumerate(standings, 1):
    print(f"{rank}. {s['participant'].name}: {s['points']}分")

# 可视化
print(tournament.visualize())
```

### 瑞士制比赛

```python
# 创建8人瑞士制，共3轮
tournament = create_swiss(["选手" + str(i) for i in range(1, 9)], num_rounds=3)

# 逐轮进行
for round_num in range(tournament.num_rounds):
    # 生成配对
    matches = tournament.generate_round_pairings()
    
    for match in matches:
        if match.status.name != "BYE":
            # 设置结果 (1=胜, 0=负, 0.5=平)
            tournament.set_result(match.id, 1, 0)

# 最终排名
standings = tournament.get_standings()
print(f"冠军: {standings[0]['participant'].name}")
```

## API 参考

### Participant

```python
Participant(id: int, name: str, seed: int = None, rating: int = None)
```

参赛者对象。

### Match

```python
Match(id, round_num, position, participant1, participant2, ...)
```

比赛对象。

### SingleElimination

| 方法 | 说明 |
|------|------|
| `__init__(participants)` | 创建淘汰赛 |
| `set_winner(match_id, winner_id)` | 设置胜者 |
| `set_score(match_id, score1, score2)` | 设置比分 |
| `get_round_matches(round_num)` | 获取某轮比赛 |
| `get_current_round()` | 获取当前轮次 |
| `is_completed()` | 是否完成 |
| `get_winner()` | 获取冠军 |
| `get_standings()` | 获取排名 |
| `visualize()` | 可视化输出 |
| `to_dict()` | 转换为字典 |

### DoubleElimination

| 方法 | 说明 |
|------|------|
| `set_winner_winner(match_id, winner_id)` | 设置胜者组结果 |
| `set_loser_winner(match_id, winner_id)` | 设置败者组结果 |
| `set_grand_final_winner(winner_id)` | 设置总决赛胜者 |
| `get_winner()` | 获取冠军 |

### RoundRobin

| 方法 | 说明 |
|------|------|
| `set_result(match_id, score1, score2, draw=False)` | 设置结果 |
| `get_standings()` | 获取积分榜 |

### SwissSystem

| 方法 | 说明 |
|------|------|
| `generate_round_pairings()` | 生成下一轮配对 |
| `set_result(match_id, score1, score2)` | 设置结果 |
| `get_standings()` | 获取积分榜 |
| `get_winners(top_n)` | 获取前N名 |

## 种子排名说明

在淘汰赛中，种子选手会被安排在对阵表的两端，确保：
- 1号种子和2号种子只在决赛相遇
- 高种子选手在早期轮次面对低种子选手

```
种子排序示例（8人）：
位置: 0  1  2  3  4  5  6  7
种子: 1  8  5  4  3  6  7  2

对阵：
1 vs 8
5 vs 4
3 vs 6
7 vs 2

这样确保：
- 1号和2号在决赛相遇
- 前四种子在半决赛之前不会相遇
```

## 示例输出

### 单败淘汰赛可视化

```
🏆 单败淘汰赛对阵表
==================================================

第一轮
------------------------------
  ⏳ [1] 张三 vs [8] 李四
  ⏳ [5] 钱七 vs [4] 赵六
  ⏳ [3] 王五 vs [6] 孙八
  ⏳ [7] 周九 vs [2] 吴十

⚔️ 半决赛
------------------------------
  ⏳ TBD vs TBD
  ⏳ TBD vs TBD

🏅 决赛
------------------------------
  ⏳ TBD vs TBD
```

### 循环赛积分榜

```
📊 积分榜
------------------------------
排名 选手            胜    负    平    积分
----------------------------------------
1    张三           3     0     0     9   
2    李四           2     1     0     6   
3    王五           1     1     1     4   
4    赵六           0     3     0     0   

🏆 冠军: 张三
```

### 瑞士制积分榜

```
📊 积分榜 (第3轮后)
--------------------------------------------------
排名 选手        胜    负    平    积分    BH    
--------------------------------------------------
1    选手1      3     0     0     3.0     6.0  
2    选手3      2     1     0     2.0     5.0  
3    选手2      2     1     0     2.0     4.0  
```

## 许可证

MIT License