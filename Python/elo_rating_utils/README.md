# Elo Rating Utils

Elo 等级分系统工具模块，用于竞技排名和匹配系统。

## 功能特点

- ✅ **经典 Elo 计算** - 标准 Elo 等级分算法
- ✅ **多策略 K 因子** - 固定/新手/等级分/时间策略
- ✅ **团队 Elo** - 团队比赛等级分计算
- ✅ **智能匹配** - 基于等级分的对手匹配
- ✅ **排行榜系统** - 玩家排名管理
- ✅ **等级分转换** - 不同系统间的等级分转换
- ✅ **零外部依赖** - 仅使用 Python 标准库

## 安装

```python
# 直接导入使用
from elo_rating_utils.mod import EloRating, Player, Matchmaking, Leaderboard
```

## 快速开始

### 1. 基本使用

```python
from mod import EloRating, Player

# 创建 Elo 计算器
elo = EloRating(k_factor=32)

# 创建玩家
alice = Player("alice", rating=1500)
bob = Player("bob", rating=1600)

# 计算预期得分
expected = elo.expected_score(alice.rating, bob.rating)
print(f"Alice 对 Bob 的预期得分: {expected:.2%}")

# 比赛结果：Alice 胜利
elo.update_players(alice, bob, score1=1.0)

print(f"Alice 新等级分: {alice.rating}")
print(f"Bob 新等级分: {bob.rating}")
```

### 2. 团队比赛

```python
from mod import TeamElo, Player

team_elo = TeamElo()

# 创建团队
team1 = [Player("a1", 1500), Player("a2", 1600)]
team2 = [Player("b1", 1400), Player("b2", 1500)]

# 计算
new_ratings1, new_ratings2 = team_elo.calculate_team_ratings(
    team1, team2, score1=1.0
)

print(f"Team1 新等级分: {new_ratings1}")
print(f"Team2 新等级分: {new_ratings2}")
```

### 3. 匹配系统

```python
from mod import Matchmaking, Player

mm = Matchmaking(max_rating_diff=200)

# 寻找对手
player = Player("target", 1600)
candidates = [
    Player("c1", 1550),
    Player("c2", 1590),
    Player("c3", 1650),
]

matches = mm.find_matches(player, candidates)
for opponent, quality in matches:
    print(f"对手: {opponent.id}, 匹配质量: {quality:.2f}")
```

### 4. 排行榜

```python
from mod import Leaderboard, Player

lb = Leaderboard("Chess")

# 添加玩家
lb.add_player(Player("alice", 1800))
lb.add_player(Player("bob", 1600))
lb.add_player(Player("charlie", 1700))

# 获取排名
print(f"Alice 排名: {lb.get_rank('alice')}")

# 获取前10名
top10 = lb.get_top_players(10)
for player in top10:
    print(f"{player.id}: {player.rating}")
```

## API 参考

### EloRating

主要等级分计算器。

| 方法 | 说明 |
|------|------|
| `expected_score(rating_a, rating_b)` | 计算预期得分 |
| `calculate_ratings(player1, player2, score1)` | 计算新等级分 |
| `update_players(player1, player2, score1)` | 更新玩家数据 |

### Player

玩家数据类。

| 属性 | 说明 |
|------|------|
| `id` | 玩家ID |
| `rating` | 当前等级分 |
| `games_played` | 总场次 |
| `wins/losses/draws` | 胜/负/平场次 |
| `win_rate` | 胜率 |
| `peak_rating` | 历史最高分 |

### Matchmaking

匹配系统。

| 方法 | 说明 |
|------|------|
| `find_matches(player, candidates)` | 搜索匹配对手 |
| `best_match(player, candidates)` | 最佳匹配 |
| `balanced_teams(players, team_size)` | 均衡分队 |

### Leaderboard

排行榜管理。

| 方法 | 说明 |
|------|------|
| `add_player(player)` | 添加玩家 |
| `get_rank(player_id)` | 获取排名 |
| `get_top_players(n)` | 获取前N名 |
| `get_statistics()` | 统计信息 |

## K 因子策略

| 策略 | 说明 |
|------|------|
| `CONSTANT` | 固定 K 值 |
| `PROVISIONAL` | 新手高 K，老手低 K |
| `RATING_BASED` | 高分段低 K |
| `TIME_BASED` | 基于活跃度 |

## 等级分转换

```python
from mod import RatingCalculator

# Elo 转 Chess.com
converted = RatingCalculator.convert_rating(1500, "elo", "chess_com")

# 获取百分位
percentile = RatingCalculator.percentile(1800, "elo")
```

## 运行测试

```bash
python elo_rating_utils_test.py
```

## 应用场景

- 🎮 在线游戏排名系统
- ♟️ 棋类比赛排名
- ⚽ 体育比赛排名
- 🏆 竞技匹配系统
- 📊 技能评估系统

---

**Author**: AllToolkit  
**Date**: 2026-05-03