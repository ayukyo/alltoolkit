"""
Leaderboard Utils 使用示例

展示排行榜工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from mod import (
    Leaderboard, RankingMethod, SortOrder, TieBreakRule,
    MultiLeaderboard, LeaderboardBuilder,
    create_leaderboard
)


def example_basic_leaderboard():
    """基本排行榜使用示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基本排行榜")
    print("=" * 50)
    
    # 创建排行榜
    lb = Leaderboard("游戏排行榜")
    
    # 添加玩家
    lb.add_entry("p001", "张三", 1500)
    lb.add_entry("p002", "李四", 2000)
    lb.add_entry("p003", "王五", 1800)
    lb.add_entry("p004", "赵六", 2000)  # 与李四同分
    
    # 获取前 3 名
    print("\n🏆 前三名:")
    for re in lb.get_top(3):
        tie_marker = " (并列)" if re.tied else ""
        print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分{tie_marker}")
    
    # 查询特定玩家排名
    rank = lb.get_rank("p001")
    print(f"\n张三的排名: 第{rank}名")


def example_ranking_methods():
    """不同排名方式示例"""
    print("\n" + "=" * 50)
    print("示例 2: 四种排名方式对比")
    print("=" * 50)
    
    scores = [100, 100, 90, 80, 80, 70]
    
    methods = [
        (RankingMethod.DENSE, "密集排名", "1, 1, 2, 3, 3, 4 - 无间隙"),
        (RankingMethod.COMPETITION, "竞争排名", "1, 1, 3, 4, 4, 6 - 有间隙"),
        (RankingMethod.ORDINAL, "顺序排名", "1, 2, 3, 4, 5, 6 - 无平局"),
        (RankingMethod.FRACTIONAL, "分数排名", "1.5, 1.5, 3, 4.5, 4.5, 6 - 平均"),
    ]
    
    for method, name, desc in methods:
        lb = Leaderboard(name, ranking_method=method)
        for i, score in enumerate(scores):
            lb.add_entry(f"p{i}", f"玩家{i}", score)
        
        print(f"\n{name} ({desc}):")
        for re in lb.get_top(6):
            rank_str = f"{re.rank}" if isinstance(re.rank, int) else f"{re.rank:.1f}"
            print(f"  {re.entry.name}: 分数={re.entry.score}, 排名={rank_str}")


def example_tie_breaking():
    """平局决胜示例"""
    print("\n" + "=" * 50)
    print("示例 3: 平局决胜规则")
    print("=" * 50)
    
    lb = Leaderboard(
        "段位赛排行榜",
        tie_break_rules=[
            TieBreakRule("level", SortOrder.DESC),  # 等级高者优先
            TieBreakRule("wins", SortOrder.DESC),   # 胜场多者优先
            TieBreakRule("join_time", SortOrder.ASC),  # 加入时间早者优先
        ]
    )
    
    # 添加同分玩家
    players = [
        ("p001", "玩家A", 2000, {"level": 50, "wins": 100, "join_time": 1000}),
        ("p002", "玩家B", 2000, {"level": 60, "wins": 80, "join_time": 2000}),   # 等级最高
        ("p003", "玩家C", 2000, {"level": 50, "wins": 120, "join_time": 1500}),  # 等级同A，胜场最高
        ("p004", "玩家D", 1800, {"level": 55, "wins": 90, "join_time": 500}),
    ]
    
    for pid, name, score, meta in players:
        lb.add_entry(pid, name, score, meta)
    
    print("\n平局决胜结果:")
    for re in lb.get_top(4):
        meta = re.entry.metadata
        print(f"  第{int(re.rank)}名: {re.entry.name}")
        print(f"    分数={re.entry.score}, 等级={meta['level']}, 胜场={meta['wins']}")


def example_pagination():
    """分页示例"""
    print("\n" + "=" * 50)
    print("示例 4: 分页查询")
    print("=" * 50)
    
    lb = Leaderboard("大型排行榜")
    
    # 添加 35 名玩家
    for i in range(35):
        score = 1000 - i * 10 + (i % 3) * 5  # 添加一些变化
        lb.add_entry(f"p{i:03d}", f"玩家{i}", score)
    
    # 分页显示
    page = 1
    per_page = 10
    
    print(f"\n共有 {lb.count()} 名玩家，每页 {per_page} 名")
    
    while True:
        entries, total_pages, total = lb.get_page(page, per_page)
        if not entries:
            break
        
        print(f"\n📖 第 {page}/{total_pages} 页:")
        for re in entries:
            change = ""
            if re.entry.rank_change:
                if re.entry.rank_change > 0:
                    change = f" ↑{re.entry.rank_change}"
                elif re.entry.rank_change < 0:
                    change = f" ↓{abs(re.entry.rank_change)}"
            print(f"  {int(re.rank):>3}. {re.entry.name}: {re.entry.score}分{change}")
        
        page += 1
        if page > total_pages:
            break


def example_statistics():
    """统计分析示例"""
    print("\n" + "=" * 50)
    print("示例 5: 排行榜统计")
    print("=" * 50)
    
    lb = Leaderboard("赛季排行榜")
    
    # 模拟玩家数据
    import random
    random.seed(42)
    
    for i in range(100):
        score = random.randint(800, 2500)
        lb.add_entry(f"p{i:03d}", f"玩家{i}", score, {
            "level": random.randint(1, 100),
            "games": random.randint(10, 500),
            "wins": random.randint(5, 250),
        })
    
    stats = lb.get_stats()
    
    print(f"\n📊 排行榜统计:")
    print(f"  总玩家数: {stats.total_entries}")
    print(f"  平均分: {stats.average_score:.1f}")
    print(f"  最高分: {stats.max_score}")
    print(f"  最低分: {stats.min_score}")
    print(f"  中位数: {stats.median_score:.1f}")
    print(f"  标准差: {stats.std_dev:.1f}")
    
    print(f"\n📈 分数分布:")
    for range_label, count in sorted(stats.score_distribution.items()):
        bar = "█" * (count // 2)
        print(f"  {range_label}: {bar} ({count})")


def example_rank_tracking():
    """排名变化追踪示例"""
    print("\n" + "=" * 50)
    print("示例 6: 排名变化追踪")
    print("=" * 50)
    
    lb = Leaderboard("动态排行榜")
    
    # 初始排名
    lb.add_entry("p001", "张三", 1000)
    lb.add_entry("p002", "李四", 1500)
    lb.add_entry("p003", "王五", 1200)
    
    print("初始排名:")
    for re in lb.get_top(3):
        print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分")
    
    # 更新分数
    print("\n张三获得了 800 分！")
    lb.update_score("p001", 1800)
    
    print("\n更新后排名:")
    for re in lb.get_top(3):
        change = ""
        if re.entry.rank_change:
            if re.entry.rank_change > 0:
                change = f" (↑{re.entry.rank_change})"
            elif re.entry.rank_change < 0:
                change = f" (↓{abs(re.entry.rank_change)})"
        print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分{change}")


def example_multi_leaderboard():
    """多排行榜管理示例"""
    print("\n" + "=" * 50)
    print("示例 7: 多排行榜管理")
    print("=" * 50)
    
    mlb = MultiLeaderboard()
    
    # 创建不同时间范围的排行榜
    daily = mlb.create("daily", "每日排行榜")
    weekly = mlb.create("weekly", "每周排行榜")
    monthly = mlb.create("monthly", "每月排行榜")
    
    # 模拟数据
    players = [
        ("p001", "张三", 100, 500, 2000),
        ("p002", "李四", 80, 400, 1500),
        ("p003", "王五", 120, 600, 3000),
    ]
    
    for pid, name, daily_score, weekly_score, monthly_score in players:
        mlb.add_entry("daily", pid, name, daily_score)
        mlb.add_entry("weekly", pid, name, weekly_score)
        mlb.add_entry("monthly", pid, name, monthly_score)
    
    # 显示各排行榜
    for key in mlb.list():
        lb = mlb.get(key)
        print(f"\n{l(lb.name)}:")
        for re in lb.get_top(3):
            print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分")
    
    # 跨排行榜总排名
    print("\n🌟 所有排行榜综合前 5:")
    for lb_key, re in mlb.get_top_across(5):
        print(f"  [{lb_key}] 第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分")


def example_builder_pattern():
    """构建器模式示例"""
    print("\n" + "=" * 50)
    print("示例 8: 构建器模式")
    print("=" * 50)
    
    lb = (LeaderboardBuilder("竞技场排行榜")
          .with_ranking_method(RankingMethod.COMPETITION)
          .with_sort_order(SortOrder.DESC)
          .add_tie_breaker("rating", SortOrder.DESC)
          .add_tie_breaker("win_rate", SortOrder.DESC)
          .with_max_entries(1000)
          .with_history(True)
          .build())
    
    # 添加测试数据
    lb.add_entry("p001", "高手A", 2500, {"rating": 2800, "win_rate": 0.85})
    lb.add_entry("p002", "高手B", 2500, {"rating": 2750, "win_rate": 0.90})  # 胜率高
    lb.add_entry("p003", "高手C", 2400, {"rating": 2900, "win_rate": 0.75})
    
    print(f"排行榜名称: {lb.name}")
    print(f"排名方式: {lb.ranking_method.value}")
    print(f"排序顺序: {lb.sort_order.value}")
    print(f"决胜规则数: {len(lb.tie_break_rules)}")
    
    print("\n排名结果:")
    for re in lb.get_top(3):
        meta = re.entry.metadata
        print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分 (rating={meta['rating']}, win_rate={meta['win_rate']})")


def example_search():
    """搜索功能示例"""
    print("\n" + "=" * 50)
    print("示例 9: 搜索功能")
    print("=" * 50)
    
    lb = Leaderboard("公会排行榜")
    
    # 添加公会成员
    members = [
        ("m001", "龙骑士·张三", 2000, {"guild": "龙之谷", "class": "战士"}),
        ("m002", "凤舞·李四", 1800, {"guild": "凤之翼", "class": "法师"}),
        ("m003", "龙骑士·王五", 1900, {"guild": "龙之谷", "class": "牧师"}),
        ("m004", "暗影·赵六", 2100, {"guild": "暗影堂", "class": "刺客"}),
        ("m005", "龙骑士·钱七", 1700, {"guild": "龙之谷", "class": "猎人"}),
    ]
    
    for mid, name, score, meta in members:
        lb.add_entry(mid, name, score, meta)
    
    # 按名称搜索
    print("\n搜索名称包含 '龙骑士' 的成员:")
    for re in lb.search("龙骑士"):
        print(f"  {re.entry.name} - {re.entry.score}分")
    
    # 按公会搜索
    print("\n搜索 '龙之谷' 公会成员:")
    for re in lb.search("龙之谷", field="guild"):
        print(f"  {re.entry.name} ({re.entry.metadata['class']}) - {re.entry.score}分")


def example_around_rank():
    """周围排名查询示例"""
    print("\n" + "=" * 50)
    print("示例 10: 周围排名查询")
    print("=" * 50)
    
    lb = Leaderboard("天梯排行榜")
    
    # 添加 20 名玩家
    for i in range(20):
        lb.add_entry(f"p{i:03d}", f"玩家{i}", 1000 - i * 20)
    
    # 查询某个玩家周围的排名
    target = "p010"
    print(f"\n玩家10周围的排名 (前后各 3 名):")
    
    for re in lb.get_around(target, radius=3):
        marker = " 👈" if re.entry.id == target else ""
        print(f"  第{int(re.rank):>2}名: {re.entry.name} - {re.entry.score}分{marker}")


def example_export_import():
    """导出导入示例"""
    print("\n" + "=" * 50)
    print("示例 11: 数据导出导入")
    print("=" * 50)
    
    # 创建并填充排行榜
    lb1 = Leaderboard("原始排行榜")
    for i in range(5):
        lb1.add_entry(f"p{i:03d}", f"玩家{i}", 1000 - i * 50)
    
    # 导出为字典
    data = lb1.to_dict()
    print("导出数据:")
    print(f"  名称: {data['name']}")
    print(f"  条目数: {len(data['entries'])}")
    print(f"  统计: {data['stats']['average_score']:.1f} 平均分")
    
    # 导入到新排行榜
    lb2 = Leaderboard.from_dict(data)
    print(f"\n导入成功: {lb2.name}, 共 {lb2.count()} 条记录")
    
    # 验证数据
    for re in lb2.get_top(5):
        print(f"  第{int(re.rank)}名: {re.entry.name} - {re.entry.score}分")


def example_real_world():
    """真实场景示例"""
    print("\n" + "=" * 50)
    print("示例 12: 真实场景 - 游戏排位赛")
    print("=" * 50)
    
    # 创建排位赛排行榜
    lb = Leaderboard(
        "S1 排位赛",
        ranking_method=RankingMethod.COMPETITION,  # 使用竞争排名
        tie_break_rules=[
            TieBreakRule("wins", SortOrder.DESC),      # 胜场多者优先
            TieBreakRule("win_rate", SortOrder.DESC),  # 胜率高者优先
        ]
    )
    
    # 模拟玩家数据
    players = [
        ("玩家A", 2800, 150, 120, 0.80),
        ("玩家B", 2800, 180, 150, 0.83),  # 同分但胜场多
        ("玩家C", 2750, 200, 160, 0.80),
        ("玩家D", 2800, 180, 150, 0.83),  # 完全相同
        ("玩家E", 2700, 100, 70, 0.70),
    ]
    
    for i, (name, score, games, wins, win_rate) in enumerate(players):
        lb.add_entry(f"p{i}", name, score, {
            "games": games,
            "wins": wins,
            "win_rate": win_rate
        })
    
    print("\n🏆 S1 排位赛排行榜:")
    print("-" * 50)
    for re in lb.get_top(5):
        meta = re.entry.metadata
        tie = " [并列]" if re.tied else ""
        print(f"第{int(re.rank)}名{tie}: {re.entry.name}")
        print(f"  分数: {re.entry.score} | 胜场: {meta['wins']}/{meta['games']} | 胜率: {meta['win_rate']:.0%}")
    
    # 统计信息
    stats = lb.get_stats()
    print(f"\n📊 排位赛统计:")
    print(f"  参赛人数: {stats.total_entries}")
    print(f"  平均分数: {stats.average_score:.0f}")
    print(f"  最高分数: {stats.max_score}")
    print(f"  最低分数: {stats.min_score}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Leaderboard Utils 使用示例")
    print("=" * 60)
    
    examples = [
        example_basic_leaderboard,
        example_ranking_methods,
        example_tie_breaking,
        example_pagination,
        example_statistics,
        example_rank_tracking,
        example_multi_leaderboard,
        example_builder_pattern,
        example_search,
        example_around_rank,
        example_export_import,
        example_real_world,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ {example.__name__} 执行失败: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()