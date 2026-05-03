"""
Elo Rating Utils - 基础使用示例

演示 Elo 等级分系统的基本功能
"""

import sys
sys.path.insert(0, '..')

from mod import EloRating, Player, Matchmaking, Leaderboard, KFactorStrategy


def example_basic_game():
    """基本比赛示例"""
    print("=== 基本比赛示例 ===\n")
    
    # 创建 Elo 计算器
    elo = EloRating(k_factor=32, k_strategy=KFactorStrategy.PROVISIONAL)
    
    # 创建两个玩家
    alice = Player("Alice", rating=1500)
    bob = Player("Bob", rating=1600)
    
    print(f"初始状态:")
    print(f"  Alice: {alice.rating} 分")
    print(f"  Bob: {bob.rating} 分")
    
    # 计算预期得分
    expected_alice = elo.expected_score(alice.rating, bob.rating)
    print(f"\n预期得分:")
    print(f"  Alice 胜率: {expected_alice:.1%}")
    print(f"  Bob 胜率: {1 - expected_alice:.1%}")
    
    # Alice 胜利
    print(f"\n比赛结果: Alice 胜利!")
    elo.update_players(alice, bob, score1=1.0)
    
    print(f"\n赛后状态:")
    print(f"  Alice: {alice.rating:.1f} 分 (+{alice.rating - 1500:.1f})")
    print(f"  Bob: {bob.rating:.1f} 分 ({bob.rating - 1600:.1f})")
    
    print(f"\n统计数据:")
    print(f"  Alice: {alice.wins}胜 {alice.losses}负")
    print(f"  Bob: {bob.wins}胜 {bob.losses}负")


def example_matchmaking():
    """匹配系统示例"""
    print("\n=== 匹配系统示例 ===\n")
    
    mm = Matchmaking(max_rating_diff=150)
    
    # 创建目标玩家
    target = Player("You", rating=1650)
    
    # 创建候选玩家池
    candidates = [
        Player("Player1", rating=1600),
        Player("Player2", rating=1655),
        Player("Player3", rating=1700),  # 超出范围
        Player("Player4", rating=1550),
        Player("Player5", rating=1640),
    ]
    
    print(f"你的等级分: {target.rating}")
    print(f"\n候选玩家:")
    for p in candidates:
        print(f"  {p.id}: {p.rating}")
    
    # 寻找匹配
    matches = mm.find_matches(target, candidates, limit=3)
    
    print(f"\n匹配结果 (最大等级分差: {mm.max_rating_diff}):")
    for opponent, quality in matches:
        diff = abs(opponent.rating - target.rating)
        print(f"  {opponent.id}: {opponent.rating} (差距: {diff}, 质量: {quality:.2f})")


def example_leaderboard():
    """排行榜示例"""
    print("\n=== 排行榜示例 ===\n")
    
    lb = Leaderboard("Chess Championship")
    
    # 添加玩家
    players_data = [
        ("Magnus", 2850),
        ("Hikaru", 2800),
        ("Fabiano", 2750),
        ("Ding", 2700),
        ("Ian", 2650),
        ("Maxime", 2600),
        ("Anish", 2550),
        ("Wesley", 2500),
    ]
    
    for name, rating in players_data:
        lb.add_player(Player(name, rating))
    
    # 显示排行榜
    print(f"排行榜: {lb.name}")
    print(f"玩家数: {len(lb.players)}")
    
    print(f"\n前5名:")
    top5 = lb.get_top_players(5)
    for i, p in enumerate(top5, 1):
        print(f"  #{i} {p.id}: {p.rating}")
    
    # 获取统计信息
    stats = lb.get_statistics()
    print(f"\n统计:")
    print(f"  平均等级分: {stats['average_rating']:.1f}")
    print(f"  最高: {stats['highest_rating']}")
    print(f"  最低: {stats['lowest_rating']}")


def example_rating_analysis():
    """等级分分析示例"""
    print("\n=== 等级分分析示例 ===\n")
    
    from mod import RatingCalculator, elo_diff_to_probability, rating_to_title
    
    # 不同等级分差下的获胜概率
    print("等级分差与获胜概率:")
    for diff in [0, 100, 200, 400, 600]:
        prob = elo_diff_to_probability(diff)
        print(f"  +{diff} 分差: {prob:.1%} 获胜概率")
    
    # 等级分分类
    print("\n等级分分类:")
    for rating in [800, 1200, 1500, 1800, 2200, 2500, 2800]:
        title = rating_to_title(rating)
        percentile = RatingCalculator.percentile(rating, "elo")
        print(f"  {rating} 分: {title} (第 {percentile:.1f} 百分位)")


def example_tournament():
    """锦标赛模拟示例"""
    print("\n=== 锦标赛模拟示例 ===\n")
    
    elo = EloRating(k_strategy=KFactorStrategy.PROVISIONAL)
    lb = Leaderboard("Local Tournament")
    
    # 创建8名选手
    players = []
    for i in range(8):
        p = Player(f"Player{i+1}", rating=1500)
        players.append(p)
        lb.add_player(p)
    
    print("初始等级分: 全员 1500")
    
    # 模拟比赛 (简化版)
    matches = [
        (0, 1, 1.0),  # Player1 胜 Player2
        (2, 3, 1.0),  # Player3 胜 Player4
        (4, 5, 0.5),  # 平局
        (6, 7, 1.0),  # Player7 胜 Player8
        (0, 2, 1.0),  # Player1 胜 Player3
        (6, 4, 1.0),  # Player7 胜 Player5
        (0, 6, 1.0),  # Player1 胜 Player7 - 冠军
    ]
    
    print("\n比赛进行中...")
    for i, (p1_idx, p2_idx, score1) in enumerate(matches):
        p1 = players[p1_idx]
        p2 = players[p2_idx]
        elo.update_players(p1, p2, score1)
        result = "胜" if score1 > 0.5 else "平局" if score1 == 0.5 else "负"
        print(f"  第{i+1}场: {p1.id} vs {p2.id} - {p1.id} {result}")
    
    # 显示最终排名
    print("\n最终排名:")
    rankings = lb.export_rankings()
    for r in rankings[:5]:
        print(f"  #{r['rank']} {r['id']}: {r['rating']:.1f} ({r['wins']}胜/{r['losses']}负)")


if __name__ == "__main__":
    example_basic_game()
    example_matchmaking()
    example_leaderboard()
    example_rating_analysis()
    example_tournament()
    
    print("\n=== 示例完成 ===")