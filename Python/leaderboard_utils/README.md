# Leaderboard Utils - 排行榜工具模块

功能完整的排行榜管理系统，支持多种排名方式、平局处理、分页查询、统计分析等功能。

## 特性

- ✅ **零外部依赖** - 纯 Python 标准库实现
- ✅ **四种排名方式** - 密集排名、竞争排名、顺序排名、分数排名
- ✅ **平局决胜** - 支持多级决胜规则
- ✅ **分页查询** - 支持分页和周围排名查询
- ✅ **排名变化追踪** - 自动追踪排名变化
- ✅ **统计分析** - 平均分、中位数、标准差、分数分布
- ✅ **搜索功能** - 按名称或元数据搜索
- ✅ **多排行榜管理** - 支持多个命名排行榜
- ✅ **数据导出导入** - JSON 序列化支持
- ✅ **构建器模式** - 流式 API 构建排行榜

## 安装

将 `leaderboard_utils` 目录复制到你的项目中。

## 快速开始

```python
from leaderboard_utils.mod import Leaderboard, create_leaderboard

# 快速创建排行榜
lb = create_leaderboard("游戏排行榜")

# 添加玩家
lb.add_entry("p001", "张三", 1500)
lb.add_entry("p002", "李四", 2000)
lb.add_entry("p003", "王五", 1800)

# 获取前 10 名
for re in lb.get_top(10):
    print(f"第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分")

# 查询特定玩家排名
rank = lb.get_rank("p001")
print(f"张三排名: 第{rank}名")
```

## 排名方式

### 密集排名 (Dense) - 默认
平局时使用相同排名，后续排名无间隙：
```
分数: 100, 100, 90, 80, 80, 70
排名: 1,   1,   2,  3,  3,  4
```

### 竞争排名 (Competition)
平局时使用相同排名，后续排名有间隙：
```
分数: 100, 100, 90, 80, 80, 70
排名: 1,   1,   3,  4,  4,  6
```

### 顺序排名 (Ordinal)
无平局，按顺序排名：
```
分数: 100, 100, 90, 80, 80, 70
排名: 1,   2,   3,  4,  5,  6
```

### 分数排名 (Fractional)
平局时使用平均排名：
```
分数: 100, 100, 90, 80, 80, 70
排名: 1.5, 1.5, 3,  4.5, 4.5, 6
```

```python
from leaderboard_utils.mod import Leaderboard, RankingMethod

lb = Leaderboard(
    "排行榜",
    ranking_method=RankingMethod.COMPETITION
)
```

## 平局决胜

当多个条目分数相同时，可以设置决胜规则：

```python
from leaderboard_utils.mod import Leaderboard, TieBreakRule, SortOrder

lb = Leaderboard(
    "段位赛",
    tie_break_rules=[
        TieBreakRule("level", SortOrder.DESC),     # 等级高者优先
        TieBreakRule("wins", SortOrder.DESC),      # 胜场多者优先
        TieBreakRule("join_time", SortOrder.ASC),  # 加入早者优先
    ]
)

lb.add_entry("p1", "玩家A", 2000, {"level": 50, "wins": 100, "join_time": 1000})
lb.add_entry("p2", "玩家B", 2000, {"level": 60, "wins": 80, "join_time": 2000})
# 玩家B 排前面（等级更高）
```

## 分页查询

```python
# 获取第一页，每页 10 条
page, total_pages, total = lb.get_page(1, per_page=10)
for re in page:
    print(f"第{int(re.rank)}名: {re.entry.name}")

# 获取某玩家周围的排名（前后各 5 名）
around = lb.get_around("p001", radius=5)
```

## 排名变化追踪

```python
# 添加初始数据
lb.add_entry("p1", "玩家1", 100)
lb.add_entry("p2", "玩家2", 200)

# 获取排名（此时 previous_rank 为 None）
top = lb.get_top(2)

# 更新分数
lb.update_score("p1", 300)

# 再次获取排名（此时可看到排名变化）
top = lb.get_top(2)
for re in top:
    if re.entry.rank_change:
        change = f"变化: {'↑' if re.entry.rank_change > 0 else '↓'}{abs(re.entry.rank_change)}"
        print(f"{re.entry.name}: {change}")
```

## 统计分析

```python
stats = lb.get_stats()
print(f"总条目: {stats.total_entries}")
print(f"平均分: {stats.average_score}")
print(f"最高分: {stats.max_score}")
print(f"最低分: {stats.min_score}")
print(f"中位数: {stats.median_score}")
print(f"标准差: {stats.std_dev}")
print(f"分数分布: {stats.score_distribution}")
```

## 搜索功能

```python
# 按名称搜索
results = lb.search("张三")

# 按元数据搜索
results = lb.search("龙之谷", field="guild")
```

## 多排行榜管理

```python
from leaderboard_utils.mod import MultiLeaderboard

mlb = MultiLeaderboard()

# 创建多个排行榜
daily = mlb.create("daily", "每日排行榜")
weekly = mlb.create("weekly", "每周排行榜")

# 添加条目
mlb.add_entry("daily", "p001", "张三", 100)
mlb.add_entry("weekly", "p001", "张三", 500)

# 获取跨排行榜前 N 名
top_across = mlb.get_top_across(10)
```

## 构建器模式

```python
from leaderboard_utils.mod import LeaderboardBuilder, RankingMethod, SortOrder

lb = (LeaderboardBuilder("竞技场排行榜")
      .with_ranking_method(RankingMethod.COMPETITION)
      .with_sort_order(SortOrder.DESC)
      .add_tie_breaker("rating", SortOrder.DESC)
      .add_tie_breaker("win_rate", SortOrder.DESC)
      .with_max_entries(1000)
      .with_history(True)
      .build())
```

## 数据导出导入

```python
# 导出为字典
data = lb.to_dict()

# 从字典导入
lb2 = Leaderboard.from_dict(data)
```

## API 参考

### Leaderboard 类

| 方法 | 说明 |
|------|------|
| `add_entry(id, name, score, metadata)` | 添加或更新条目 |
| `update_score(id, score)` | 更新分数 |
| `increment_score(id, delta)` | 增量更新分数 |
| `remove_entry(id)` | 移除条目 |
| `get_entry(id)` | 获取条目 |
| `get_rank(id)` | 获取排名 |
| `get_ranked_entry(id)` | 获取带排名信息的条目 |
| `get_top(n)` | 获取前 N 名 |
| `get_bottom(n)` | 获取后 N 名 |
| `get_page(page, per_page)` | 分页获取 |
| `get_around(id, radius)` | 获取周围排名 |
| `get_stats()` | 获取统计信息 |
| `search(query, field, limit)` | 搜索条目 |
| `count()` | 条目总数 |
| `clear()` | 清空排行榜 |
| `to_dict()` | 导出为字典 |
| `from_dict(data)` | 从字典创建 |

### RankedEntry 类

| 属性 | 说明 |
|------|------|
| `entry` | 排行榜条目 |
| `rank` | 排名 |
| `tied` | 是否平局 |
| `tied_count` | 平局数量 |

### LeaderboardEntry 类

| 属性 | 说明 |
|------|------|
| `id` | 唯一标识 |
| `name` | 显示名称 |
| `score` | 分数 |
| `metadata` | 额外元数据 |
| `timestamp` | 更新时间 |
| `previous_rank` | 上次排名 |
| `rank_change` | 排名变化 |
| `score_history` | 分数历史 |

## 测试

```bash
python leaderboard_utils_test.py
```

## 示例

```bash
python examples/usage_examples.py
```

## 许可证

MIT License