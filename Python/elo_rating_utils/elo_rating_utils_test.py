"""
Elo Rating Utils - 测试模块

测试 Elo 等级分系统的各项功能
"""

import unittest
import sys
sys.path.insert(0, '.')

from mod import (
    EloRating,
    Player,
    TeamElo,
    Matchmaking,
    RatingCalculator,
    Leaderboard,
    KFactorStrategy,
    elo_diff_to_probability,
    probability_to_elo_diff,
    rating_to_title
)


class TestPlayer(unittest.TestCase):
    """测试 Player 类"""
    
    def test_player_creation(self):
        """测试玩家创建"""
        player = Player("test", rating=1500)
        self.assertEqual(player.id, "test")
        self.assertEqual(player.rating, 1500)
        self.assertEqual(player.games_played, 0)
        self.assertEqual(player.wins, 0)
        self.assertEqual(player.losses, 0)
    
    def test_win_rate(self):
        """测试胜率计算"""
        player = Player("test")
        player.wins = 10
        player.losses = 5
        player.games_played = 15
        self.assertEqual(player.win_rate, 10/15)
        
        # 无比赛时胜率为 0
        empty_player = Player("empty")
        self.assertEqual(empty_player.win_rate, 0.0)
    
    def test_is_provisional(self):
        """测试新手判定"""
        new_player = Player("new", games_played=5)
        self.assertTrue(new_player.is_provisional)
        
        old_player = Player("old", games_played=30)
        self.assertFalse(old_player.is_provisional)
    
    def test_peak_rating_update(self):
        """测试历史最高分更新"""
        player = Player("test", rating=1500)
        self.assertEqual(player.peak_rating, 1500)  # 初始化时就是当前值
        
        player.rating = 1600
        player.update_peak()
        self.assertEqual(player.peak_rating, 1600)
        
        # 降分不更新
        player.rating = 1550
        player.update_peak()
        self.assertEqual(player.peak_rating, 1600)


class TestEloRating(unittest.TestCase):
    """测试 EloRating 类"""
    
    def setUp(self):
        self.elo = EloRating(k_factor=32)
    
    def test_expected_score_equal(self):
        """测试相同等级分的预期得分"""
        expected = self.elo.expected_score(1500, 1500)
        self.assertAlmostEqual(expected, 0.5, places=2)
    
    def test_expected_score_higher(self):
        """测试高分对低分的预期得分"""
        expected = self.elo.expected_score(1600, 1400)
        self.assertGreater(expected, 0.5)
        self.assertLess(expected, 1.0)
    
    def test_expected_score_lower(self):
        """测试低分对高分的预期得分"""
        expected = self.elo.expected_score(1400, 1600)
        self.assertLess(expected, 0.5)
        self.assertGreater(expected, 0.0)
    
    def test_rating_change_win(self):
        """测试获胜的等级分变化"""
        player = Player("p1", rating=1500, games_played=30)
        change = self.elo.rating_change(player, 1600, 1.0)
        self.assertGreater(change, 0)  # 胜利得分
    
    def test_rating_change_loss(self):
        """测试失败的等级分变化"""
        player = Player("p1", rating=1500, games_played=30)
        change = self.elo.rating_change(player, 1400, 0.0)
        self.assertLess(change, 0)  # 失败扣分
    
    def test_rating_change_draw(self):
        """测试平局的等级分变化"""
        player = Player("p1", rating=1500, games_played=30)
        change = self.elo.rating_change(player, 1500, 0.5)
        self.assertAlmostEqual(change, 0, places=2)
    
    def test_calculate_ratings(self):
        """测试等级分计算"""
        p1 = Player("p1", rating=1500, games_played=30)
        p2 = Player("p2", rating=1600, games_played=30)
        
        new_r1, new_r2 = self.elo.calculate_ratings(p1, p2, 1.0)
        
        # p1 胜利，得分增加
        self.assertGreater(new_r1, 1500)
        # p2 失败，得分减少
        self.assertLess(new_r2, 1600)
    
    def test_k_factor_strategies(self):
        """测试 K 因子策略"""
        # 固定策略
        elo_constant = EloRating(k_factor=32, k_strategy=KFactorStrategy.CONSTANT)
        player = Player("p", games_played=50)
        self.assertEqual(elo_constant.get_k_factor(player), 32)
        
        # 新手策略
        elo_provisional = EloRating(k_strategy=KFactorStrategy.PROVISIONAL)
        new_player = Player("new", games_played=5)
        self.assertEqual(elo_provisional.get_k_factor(new_player), 50)
        
        old_player = Player("old", games_played=30)
        self.assertEqual(elo_provisional.get_k_factor(old_player), 20)
    
    def test_rating_clamp(self):
        """测试等级分范围限制"""
        elo = EloRating(min_rating=100, max_rating=3000)
        p1 = Player("p1", rating=50, games_played=30)
        p2 = Player("p2", rating=1500, games_played=30)
        
        new_r1, _ = elo.calculate_ratings(p1, p2, 0.0)  # p1 失败
        self.assertGreaterEqual(new_r1, 100)
    
    def test_update_players(self):
        """测试玩家数据更新"""
        p1 = Player("p1", rating=1500)
        p2 = Player("p2", rating=1600)
        
        self.elo.update_players(p1, p2, 1.0)  # p1 胜
        
        self.assertEqual(p1.wins, 1)
        self.assertEqual(p2.losses, 1)
        self.assertEqual(p1.games_played, 1)
        self.assertEqual(p2.games_played, 1)


class TestTeamElo(unittest.TestCase):
    """测试 TeamElo 类"""
    
    def setUp(self):
        self.team_elo = TeamElo(k_factor=32)
    
    def test_team_rating_average(self):
        """测试团队平均等级分"""
        team = [Player("a", 1500), Player("b", 1600)]
        rating = self.team_elo.team_rating(team, "average")
        self.assertEqual(rating, 1550)
    
    def test_team_rating_sum(self):
        """测试团队总等级分"""
        team = [Player("a", 1500), Player("b", 1600)]
        rating = self.team_elo.team_rating(team, "sum")
        self.assertEqual(rating, 3100)
    
    def test_team_rating_best(self):
        """测试团队最高等级分"""
        team = [Player("a", 1500), Player("b", 1600)]
        rating = self.team_elo.team_rating(team, "best")
        self.assertEqual(rating, 1600)
    
    def test_calculate_team_ratings(self):
        """测试团队比赛等级分计算"""
        team1 = [Player("a", 1500), Player("b", 1600)]
        team2 = [Player("c", 1400), Player("d", 1500)]
        
        new_r1, new_r2 = self.team_elo.calculate_team_ratings(
            team1, team2, 1.0, "average"
        )
        
        # team1 平均分更高且赢了，得分增加
        self.assertGreater(new_r1[0], 1500)
        self.assertGreater(new_r1[1], 1600)


class TestMatchmaking(unittest.TestCase):
    """测试 Matchmaking 类"""
    
    def setUp(self):
        self.mm = Matchmaking(max_rating_diff=200)
    
    def test_find_matches(self):
        """测试匹配搜索"""
        player = Player("target", 1600)
        candidates = [
            Player("c1", 1550),
            Player("c2", 1850),  # 超出范围 (差250)
            Player("c3", 1590),
            Player("c4", 1610),
        ]
        
        matches = self.mm.find_matches(player, candidates)
        
        # 应找到3个匹配（1850超出范围）
        self.assertEqual(len(matches), 3)
        
        # 最佳匹配应该最接近（c3和c4都是差10分）
        best = matches[0][0]
        self.assertIn(best.id, ["c3", "c4"])
        self.assertEqual(abs(best.rating - player.rating), 10)
    
    def test_find_matches_with_limit(self):
        """测试匹配数量限制"""
        player = Player("target", 1600)
        candidates = [Player(str(i), 1600) for i in range(20)]
        
        matches = self.mm.find_matches(player, candidates, limit=5)
        self.assertEqual(len(matches), 5)
    
    def test_best_match(self):
        """测试最佳匹配"""
        player = Player("target", 1600)
        candidates = [
            Player("c1", 1400),
            Player("c2", 1590),
            Player("c3", 1700),
        ]
        
        best = self.mm.best_match(player, candidates)
        self.assertIsNotNone(best)
        self.assertEqual(best.rating, 1590)
    
    def test_balanced_teams(self):
        """测试均衡分队"""
        players = [
            Player("a", 1800),
            Player("b", 1600),
            Player("c", 1400),
            Player("d", 1200),
        ]
        
        team1, team2, balance = self.mm.balanced_teams(players, team_size=2)
        
        # 分队后实力应接近
        avg1 = sum(p.rating for p in team1) / 2
        avg2 = sum(p.rating for p in team2) / 2
        
        self.assertGreater(balance, 0.8)
    
    def test_balanced_teams_error(self):
        """测试分队人数不足"""
        players = [Player("a", 1500)]
        
        with self.assertRaises(ValueError):
            self.mm.balanced_teams(players, team_size=2)


class TestRatingCalculator(unittest.TestCase):
    """测试 RatingCalculator 类"""
    
    def test_convert_rating(self):
        """测试等级分转换"""
        # Elo 1500 -> Chess.com
        converted = RatingCalculator.convert_rating(1500, "elo", "chess_com")
        self.assertGreater(converted, 1500)
        
        # 反向转换
        back = RatingCalculator.convert_rating(converted, "chess_com", "elo")
        self.assertAlmostEqual(back, 1500, places=1)
    
    def test_percentile(self):
        """测试百分位计算"""
        p50 = RatingCalculator.percentile(1200, "elo")
        self.assertAlmostEqual(p50, 50, places=1)
        
        p_higher = RatingCalculator.percentile(1600, "elo")
        self.assertGreater(p_higher, 50)
    
    def test_rating_for_percentile(self):
        """测试百分位反算"""
        rating = RatingCalculator.rating_for_percentile(50, "elo")
        self.assertAlmostEqual(rating, 1200, places=1)
        
        rating_95 = RatingCalculator.rating_for_percentile(95, "elo")
        self.assertGreater(rating_95, 1800)
    
    def test_classify_rating(self):
        """测试等级分分类"""
        # elo 系统均值是 1200
        self.assertEqual(RatingCalculator.classify_rating(700, "elo"), "初学者")   # < 800
        self.assertEqual(RatingCalculator.classify_rating(900, "elo"), "新手")     # 800-1000
        self.assertEqual(RatingCalculator.classify_rating(1100, "elo"), "普通")    # 1000-1400
        self.assertEqual(RatingCalculator.classify_rating(1500, "elo"), "熟练")    # 1400-1600
        self.assertEqual(RatingCalculator.classify_rating(1700, "elo"), "高手")    # 1600-1800
        self.assertEqual(RatingCalculator.classify_rating(1900, "elo"), "专家")    # 1800-2000
        self.assertEqual(RatingCalculator.classify_rating(2100, "elo"), "大师")    # >= 2000


class TestLeaderboard(unittest.TestCase):
    """测试 Leaderboard 类"""
    
    def setUp(self):
        self.lb = Leaderboard("Test")
    
    def test_add_remove_player(self):
        """测试添加/移除玩家"""
        player = Player("p1", 1500)
        self.lb.add_player(player)
        self.assertEqual(len(self.lb.players), 1)
        
        removed = self.lb.remove_player("p1")
        self.assertEqual(removed, player)
        self.assertEqual(len(self.lb.players), 0)
    
    def test_get_rank(self):
        """测试排名获取"""
        self.lb.add_player(Player("p1", 1800))
        self.lb.add_player(Player("p2", 1600))
        self.lb.add_player(Player("p3", 1400))
        
        self.assertEqual(self.lb.get_rank("p1"), 1)
        self.assertEqual(self.lb.get_rank("p2"), 2)
        self.assertEqual(self.lb.get_rank("p3"), 3)
    
    def test_get_top_players(self):
        """测试获取前N名"""
        self.lb.add_player(Player("p1", 1800))
        self.lb.add_player(Player("p2", 1700))
        self.lb.add_player(Player("p3", 1600))
        
        top = self.lb.get_top_players(2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].rating, 1800)
        self.assertEqual(top[1].rating, 1700)
    
    def test_get_nearby_players(self):
        """测试获取附近排名"""
        for i in range(10):
            self.lb.add_player(Player(str(i), 1500 + i * 10))
        
        nearby = self.lb.get_nearby_players("5", range_size=2)
        self.assertEqual(len(nearby), 5)
    
    def test_statistics(self):
        """测试统计信息"""
        self.lb.add_player(Player("p1", 1500))
        self.lb.add_player(Player("p2", 1700))
        
        stats = self.lb.get_statistics()
        self.assertEqual(stats["player_count"], 2)
        self.assertEqual(stats["average_rating"], 1600)
    
    def test_export_rankings(self):
        """测试导出排名"""
        self.lb.add_player(Player("p1", 1800, wins=10, losses=5))
        self.lb.add_player(Player("p2", 1600, wins=5, losses=10))
        
        rankings = self.lb.export_rankings()
        self.assertEqual(len(rankings), 2)
        self.assertEqual(rankings[0]["rank"], 1)
        self.assertEqual(rankings[0]["id"], "p1")


class TestHelperFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_elo_diff_to_probability(self):
        """测试等级分差转概率"""
        self.assertAlmostEqual(elo_diff_to_probability(0), 0.5, places=2)
        self.assertAlmostEqual(elo_diff_to_probability(400), 0.91, places=1)
        self.assertAlmostEqual(elo_diff_to_probability(-400), 0.09, places=1)
    
    def test_probability_to_elo_diff(self):
        """测试概率转等级分差"""
        self.assertAlmostEqual(probability_to_elo_diff(0.5), 0, places=1)
        self.assertGreater(probability_to_elo_diff(0.9), 300)
    
    def test_rating_to_title(self):
        """测试等级分转头衔"""
        self.assertEqual(rating_to_title(2800), "特级大师 (GM)")
        self.assertEqual(rating_to_title(1500), "新手")  # chess 系统阈值
        self.assertEqual(rating_to_title(900), "初学者")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_game_scenario(self):
        """测试完整比赛场景"""
        elo = EloRating(k_strategy=KFactorStrategy.PROVISIONAL)
        lb = Leaderboard("Chess")
        
        # 创建玩家
        players = [
            Player("alice", 1500),
            Player("bob", 1500),
            Player("charlie", 1600),
        ]
        
        for p in players:
            lb.add_player(p)
        
        # 进行比赛
        alice = lb.get_player("alice")
        bob = lb.get_player("bob")
        elo.update_players(alice, bob, 1.0)  # alice 胜
        
        # 检查结果
        self.assertGreater(alice.rating, 1500)
        self.assertLess(bob.rating, 1500)
        self.assertEqual(alice.wins, 1)
        self.assertEqual(bob.losses, 1)
        
        # 检查排名 - alice 应该超过 bob
        self.assertLess(lb.get_rank("alice"), lb.get_rank("bob"))
    
    def test_matchmaking_scenario(self):
        """测试匹配场景"""
        mm = Matchmaking(max_rating_diff=100)
        lb = Leaderboard()
        
        # 添加100个玩家
        for i in range(100):
            lb.add_player(Player(str(i), 1400 + i * 5))
        
        # 为玩家50找匹配
        player = lb.get_player("50")
        matches = mm.find_matches(player, list(lb.players.values()))
        
        self.assertGreater(len(matches), 0)
        
        # 最佳匹配应接近
        best_match = matches[0][0]
        self.assertLess(abs(best_match.rating - player.rating), 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)