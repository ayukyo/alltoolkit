#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for elo_rating_utils"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Player, EloRating, TeamElo, Matchmaking, RatingCalculator, Leaderboard,
    KFactorStrategy,
    elo_diff_to_probability, probability_to_elo_diff, rating_to_title
)

import unittest


class TestPlayer(unittest.TestCase):
    def test_creation(self):
        player = Player("p1", rating=1500, games_played=10)
        self.assertEqual(player.id, "p1")
        self.assertEqual(player.rating, 1500)
        self.assertEqual(player.games_played, 10)

    def test_win_rate(self):
        player = Player("p1", wins=5, losses=3, games_played=10)
        self.assertAlmostEqual(player.win_rate, 0.5, places=3)

    def test_is_provisional(self):
        player_new = Player("p1", games_played=5)
        player_old = Player("p2", games_played=30)
        self.assertTrue(player_new.is_provisional)
        self.assertFalse(player_old.is_provisional)

    def test_update_peak(self):
        player = Player("p1", rating=1500)
        player.rating = 1600
        player.update_peak()
        self.assertEqual(player.peak_rating, 1600)


class TestEloRating(unittest.TestCase):
    def test_expected_score_equal(self):
        elo = EloRating()
        expected = elo.expected_score(1500, 1500)
        self.assertAlmostEqual(expected, 0.5, places=3)

    def test_expected_score_higher(self):
        elo = EloRating()
        expected = elo.expected_score(1600, 1400)
        self.assertGreater(expected, 0.5)

    def test_expected_score_lower(self):
        elo = EloRating()
        expected = elo.expected_score(1400, 1600)
        self.assertLess(expected, 0.5)

    def test_rating_change_win(self):
        elo = EloRating()
        player = Player("p1", rating=1500, games_played=30)
        change = elo.rating_change(player, 1500, 1.0)
        self.assertGreater(change, 0)

    def test_rating_change_loss(self):
        elo = EloRating()
        player = Player("p1", rating=1500, games_played=30)
        change = elo.rating_change(player, 1500, 0.0)
        self.assertLess(change, 0)

    def test_calculate_ratings_win(self):
        elo = EloRating()
        p1 = Player("p1", rating=1500)
        p2 = Player("p2", rating=1500)
        new_p1, new_p2 = elo.calculate_ratings(p1, p2, 1.0)
        self.assertGreater(new_p1, 1500)
        self.assertLess(new_p2, 1500)

    def test_calculate_ratings_draw(self):
        elo = EloRating()
        p1 = Player("p1", rating=1500)
        p2 = Player("p2", rating=1500)
        new_p1, new_p2 = elo.calculate_ratings(p1, p2, 0.5)
        self.assertEqual(new_p1, new_p2)

    def test_update_players(self):
        elo = EloRating()
        p1 = Player("p1", rating=1500)
        p2 = Player("p2", rating=1500)
        elo.update_players(p1, p2, 1.0)
        self.assertEqual(p1.games_played, 1)
        self.assertEqual(p1.wins, 1)
        self.assertEqual(p2.games_played, 1)
        self.assertEqual(p2.losses, 1)

    def test_k_factor_constant(self):
        elo = EloRating(k_strategy=KFactorStrategy.CONSTANT)
        player = Player("p1", rating=1500)
        self.assertEqual(elo.get_k_factor(player), 32.0)

    def test_k_factor_provisional_low_games(self):
        elo = EloRating(k_strategy=KFactorStrategy.PROVISIONAL)
        player = Player("p1", games_played=5)
        self.assertEqual(elo.get_k_factor(player), 50.0)

    def test_expected_score_range(self):
        elo = EloRating()
        result = elo.expected_score_range(1500)
        self.assertIn("vs_lower", result)
        self.assertIn("vs_equal", result)
        self.assertIn("vs_higher", result)


class TestTeamElo(unittest.TestCase):
    def test_team_rating_average(self):
        team = [Player("p1", rating=1400), Player("p2", rating=1600)]
        team_elo = TeamElo()
        avg = team_elo.team_rating(team, method="average")
        self.assertEqual(avg, 1500)

    def test_team_rating_best(self):
        team = [Player("p1", rating=1400), Player("p2", rating=1600)]
        team_elo = TeamElo()
        best = team_elo.team_rating(team, method="best")
        self.assertEqual(best, 1600)

    def test_calculate_team_ratings(self):
        team1 = [Player("p1", rating=1500), Player("p2", rating=1500)]
        team2 = [Player("p3", rating=1500), Player("p4", rating=1500)]
        team_elo = TeamElo()
        new_ratings1, new_ratings2 = team_elo.calculate_team_ratings(team1, team2, 1.0)
        self.assertEqual(len(new_ratings1), 2)
        self.assertEqual(len(new_ratings2), 2)


class TestMatchmaking(unittest.TestCase):
    def test_find_matches(self):
        mm = Matchmaking(max_rating_diff=200)
        player = Player("p1", rating=1500)
        candidates = [Player("p2", rating=1400), Player("p3", rating=1600)]
        matches = mm.find_matches(player, candidates)
        self.assertEqual(len(matches), 2)

    def test_find_matches_no_candidates(self):
        mm = Matchmaking()
        player = Player("p1", rating=1500)
        matches = mm.find_matches(player, [])
        self.assertEqual(len(matches), 0)

    def test_best_match(self):
        mm = Matchmaking()
        player = Player("p1", rating=1500)
        candidates = [Player("p2", rating=1400), Player("p3", rating=1490)]
        best = mm.best_match(player, candidates)
        self.assertIsNotNone(best)

    def test_balanced_teams(self):
        players = [
            Player("p1", rating=1600),
            Player("p2", rating=1500),
            Player("p3", rating=1400),
            Player("p4", rating=1300)
        ]
        mm = Matchmaking()
        team1, team2, score = mm.balanced_teams(players, team_size=2)
        self.assertEqual(len(team1), 2)
        self.assertEqual(len(team2), 2)


class TestRatingCalculator(unittest.TestCase):
    def test_convert_rating(self):
        result = RatingCalculator.convert_rating(1500, "elo", "glicko")
        self.assertIsInstance(result, float)

    def test_percentile(self):
        result = RatingCalculator.percentile(1200, "elo")
        self.assertAlmostEqual(result, 50.0, places=1)

    def test_rating_for_percentile(self):
        result = RatingCalculator.rating_for_percentile(50, "elo")
        self.assertAlmostEqual(result, 1200, places=1)

    def test_classify_rating(self):
        self.assertIn("大师", RatingCalculator.classify_rating(2700, "elo"))
        # 1500 falls in 1200+200 to 1200+400 range = "熟练"
        self.assertIn("熟练", RatingCalculator.classify_rating(1500, "elo"))


class TestLeaderboard(unittest.TestCase):
    def test_add_player(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1500))
        self.assertIsNotNone(lb.get_player("p1"))

    def test_remove_player(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1500))
        removed = lb.remove_player("p1")
        self.assertIsNotNone(removed)
        self.assertIsNone(lb.get_player("p1"))

    def test_get_rank(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1600))
        lb.add_player(Player("p2", rating=1500))
        lb.add_player(Player("p3", rating=1400))
        rank = lb.get_rank("p1")
        self.assertEqual(rank, 1)

    def test_get_top_players(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1400))
        lb.add_player(Player("p2", rating=1600))
        lb.add_player(Player("p3", rating=1500))
        top = lb.get_top_players(2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].rating, 1600)

    def test_get_nearby_players(self):
        lb = Leaderboard()
        for i in range(5):
            lb.add_player(Player("p{}".format(i), rating=1500 + i * 100))
        nearby = lb.get_nearby_players("p2")
        self.assertGreater(len(nearby), 0)

    def test_get_statistics(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1500))
        lb.add_player(Player("p2", rating=1600))
        stats = lb.get_statistics()
        self.assertEqual(stats["player_count"], 2)
        self.assertEqual(stats["average_rating"], 1550)

    def test_export_rankings(self):
        lb = Leaderboard()
        lb.add_player(Player("p1", rating=1600))
        lb.add_player(Player("p2", rating=1500))
        rankings = lb.export_rankings()
        self.assertEqual(len(rankings), 2)
        self.assertEqual(rankings[0]["rank"], 1)


class TestHelperFunctions(unittest.TestCase):
    def test_elo_diff_to_probability(self):
        prob = elo_diff_to_probability(0)
        self.assertEqual(prob, 0.5)

    def test_elo_diff_positive(self):
        prob = elo_diff_to_probability(400)
        self.assertGreater(prob, 0.5)

    def test_probability_to_elo_diff(self):
        diff = probability_to_elo_diff(0.5)
        self.assertLess(abs(diff), 1)

    def test_rating_to_title(self):
        title = rating_to_title(2700, "chess")
        self.assertTrue("GM" in title or "大师" in title)


if __name__ == "__main__":
    unittest.main()