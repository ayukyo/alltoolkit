"""
投票选举工具测试模块
测试所有投票算法的正确性
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Ballot, Candidate, ElectionResult,
    PluralityVoting, RunoffVoting, RankedChoiceVoting,
    BordaCount, CondorcetMethod, SingleTransferableVote,
    DHondtMethod, ApprovalVoting, RangeVoting, CoombsMethod,
    VotingSystem, create_ballot, generate_random_ballot
)


class TestBallotAndCandidate(unittest.TestCase):
    """测试选票和候选人类"""
    
    def test_candidate_creation(self):
        """测试候选人创建"""
        c1 = Candidate(name="Alice", id="a1")
        c2 = Candidate(name="Alice", id="a1")
        c3 = Candidate(name="Alice", id="a2")
        
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertEqual(repr(c1), "Alice")
    
    def test_candidate_hash(self):
        """测试候选人可哈希"""
        c = Candidate(name="Bob")
        candidates_set = {c}
        self.assertIn(c, candidates_set)
    
    def test_ballot_creation(self):
        """测试选票创建"""
        ballot = Ballot(
            rankings=["Alice", "Bob", "Charlie"],
            weights={"Alice": 9, "Bob": 8, "Charlie": 7},
            approvals={"Alice", "Bob"}
        )
        
        self.assertEqual(ballot.rankings, ["Alice", "Bob", "Charlie"])
        self.assertEqual(ballot.weights["Alice"], 9)
        self.assertIn("Alice", ballot.approvals)
    
    def test_create_ballot_helper(self):
        """测试创建选票辅助函数"""
        ballot = create_ballot(
            rankings=["A", "B", "C"],
            approvals={"A", "B"}
        )
        self.assertEqual(ballot.rankings, ["A", "B", "C"])
        self.assertEqual(ballot.approvals, {"A", "B"})


class TestPluralityVoting(unittest.TestCase):
    """测试多数制投票"""
    
    def test_simple_majority(self):
        """测试简单多数"""
        ballots = [
            Ballot(rankings=["Alice"]),
            Ballot(rankings=["Alice"]),
            Ballot(rankings=["Bob"]),
        ]
        result = PluralityVoting.count(ballots, ["Alice", "Bob"])
        
        self.assertEqual(result.winner, "Alice")
        self.assertEqual(result.rankings, [("Alice", 2), ("Bob", 1)])
    
    def test_tie_breaking(self):
        """测试平局情况"""
        ballots = [
            Ballot(rankings=["Alice"]),
            Ballot(rankings=["Bob"]),
        ]
        result = PluralityVoting.count(ballots, ["Alice", "Bob"])
        
        # 平局时返回得票最多的第一个（按字母或出现顺序）
        self.assertIsNotNone(result.winner)
        self.assertEqual(len(result.rankings), 2)
    
    def test_empty_ballots(self):
        """测试空选票"""
        ballots = []
        result = PluralityVoting.count(ballots, ["Alice", "Bob"])
        
        self.assertIsNone(result.winner)
        self.assertEqual(result.rankings, [])


class TestRunoffVoting(unittest.TestCase):
    """测试两轮决选制"""
    
    def test_winner_in_first_round(self):
        """测试第一轮获胜"""
        # Alice获得超过50%的选票
        ballots = [Ballot(rankings=["Alice"])] * 6 + [Ballot(rankings=["Bob"])] * 4
        result = RunoffVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        self.assertEqual(result.winner, "Alice")
        self.assertEqual(len(result.rounds), 1)  # 只需一轮
    
    def test_second_round_needed(self):
        """测试需要第二轮"""
        # 没有人超过50%，需要决选
        ballots = [
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Alice", "Charlie", "Bob"]),
            Ballot(rankings=["Bob", "Alice", "Charlie"]),
            Ballot(rankings=["Charlie", "Bob", "Alice"]),
        ]
        result = RunoffVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        self.assertEqual(len(result.rounds), 2)
        self.assertIn(result.winner, ["Alice", "Bob", "Charlie"])


class TestRankedChoiceVoting(unittest.TestCase):
    """测试排名选择投票"""
    
    def test_instant_runoff(self):
        """测试即时决选"""
        # Alice和Bob平分选票，Charlie被淘汰后
        # Charlie的支持者转投Alice
        ballots = [
            Ballot(rankings=["Alice", "Charlie", "Bob"]),
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Bob", "Charlie", "Alice"]),
            Ballot(rankings=["Charlie", "Alice", "Bob"]),
        ]
        result = RankedChoiceVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        self.assertEqual(result.winner, "Alice")
        self.assertTrue(len(result.rounds) >= 1)
    
    def test_condorcet_scenario(self):
        """测试孔多塞场景"""
        ballots = [
            Ballot(rankings=["A", "B", "C"]),
            Ballot(rankings=["A", "B", "C"]),
            Ballot(rankings=["B", "C", "A"]),
            Ballot(rankings=["B", "C", "A"]),
            Ballot(rankings=["C", "A", "B"]),
            Ballot(rankings=["C", "A", "B"]),
        ]
        result = RankedChoiceVoting.count(ballots, ["A", "B", "C"])
        
        self.assertIsNotNone(result.winner)


class TestBordaCount(unittest.TestCase):
    """测试波达计数法"""
    
    def test_borda_scoring(self):
        """测试波达计分"""
        ballots = [
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Bob", "Alice", "Charlie"]),
        ]
        result = BordaCount.count(ballots, ["Alice", "Bob", "Charlie"])
        
        # Alice: 2*2 + 1 = 5
        # Bob: 2*1 + 2 = 4
        # Charlie: 0
        self.assertEqual(result.winner, "Alice")
        self.assertEqual(result.rankings, [("Alice", 5), ("Bob", 4), ("Charlie", 0)])
    
    def test_unanimous_ranking(self):
        """测试一致排名"""
        ballots = [
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["A", "B", "C", "D"]),
        ]
        result = BordaCount.count(ballots, ["A", "B", "C", "D"])
        
        self.assertEqual(result.winner, "A")
        # A: 3*3=9, B: 3*2=6, C: 3*1=3, D: 0
        self.assertEqual(result.rankings, [("A", 9), ("B", 6), ("C", 3), ("D", 0)])


class TestCondorcetMethod(unittest.TestCase):
    """测试孔多塞方法"""
    
    def test_condorcet_winner(self):
        """测试孔多塞赢家"""
        # A在所有两两对决中获胜
        ballots = [
            Ballot(rankings=["A", "B", "C"]),
            Ballot(rankings=["A", "C", "B"]),
            Ballot(rankings=["B", "A", "C"]),
        ]
        result = CondorcetMethod.count(ballots, ["A", "B", "C"])
        
        self.assertEqual(result.winner, "A")
        self.assertTrue(result.details["condorcet_exists"])
    
    def test_condorcet_cycle(self):
        """测试孔多塞循环（无赢家）"""
        # 经典的孔多塞悖论：A>B, B>C, C>A
        ballots = [
            Ballot(rankings=["A", "B", "C"]),
            Ballot(rankings=["B", "C", "A"]),
            Ballot(rankings=["C", "A", "B"]),
        ]
        result = CondorcetMethod.count(ballots, ["A", "B", "C"])
        
        # 孔多塞循环，没有明显的赢家
        self.assertFalse(result.details["condorcet_exists"])


class TestSingleTransferableVote(unittest.TestCase):
    """测试单一可转移投票"""
    
    def test_single_winner(self):
        """测试单一席位（等同于IRV）"""
        ballots = [
            Ballot(rankings=["Alice", "Bob"]),
            Ballot(rankings=["Alice", "Bob"]),
            Ballot(rankings=["Bob", "Alice"]),
        ]
        result = SingleTransferableVote.count(ballots, ["Alice", "Bob"], seats=1)
        
        self.assertEqual(result.winner, "Alice")
    
    def test_multiple_seats(self):
        """测试多席位"""
        ballots = [
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["C", "D", "A", "B"]),
            Ballot(rankings=["C", "D", "A", "B"]),
            Ballot(rankings=["C", "D", "A", "B"]),
            Ballot(rankings=["C", "D", "A", "B"]),
        ]
        result = SingleTransferableVote.count(ballots, ["A", "B", "C", "D"], seats=2)
        
        # A和C应该获得席位
        self.assertEqual(len(result.details["elected"]), 2)


class TestDHondtMethod(unittest.TestCase):
    """测试洪德法"""
    
    def test_proportional_allocation(self):
        """测试比例分配"""
        party_votes = {"PartyA": 100, "PartyB": 60, "PartyC": 40}
        result = DHondtMethod.count(party_votes, seats=5)
        
        # 5个席位，PartyA应该获得更多席位
        total_seats = sum(v for _, v in result.rankings)
        self.assertEqual(total_seats, 5)
        
        # PartyA应该获得最多席位
        party_a_seats = dict(result.rankings).get("PartyA", 0)
        party_b_seats = dict(result.rankings).get("PartyB", 0)
        party_c_seats = dict(result.rankings).get("PartyC", 0)
        
        self.assertGreater(party_a_seats, party_b_seats)
        # PartyB和PartyC可能获得相同席位（取决于精确比例）
        self.assertGreaterEqual(party_b_seats, party_c_seats)
    
    def test_exact_proportionality(self):
        """测试精确比例"""
        party_votes = {"A": 500, "B": 300, "C": 200}
        result = DHondtMethod.count(party_votes, seats=10)
        
        # 大约: A=5, B=3, C=2
        allocation = dict(result.rankings)
        self.assertEqual(allocation["A"], 5)
        self.assertEqual(allocation["B"], 3)
        self.assertEqual(allocation["C"], 2)


class TestApprovalVoting(unittest.TestCase):
    """测试赞成投票"""
    
    def test_basic_approval(self):
        """测试基本赞成投票"""
        ballots = [
            Ballot(rankings=[], approvals={"Alice", "Bob"}),
            Ballot(rankings=[], approvals={"Alice", "Bob"}),
            Ballot(rankings=[], approvals={"Bob", "Charlie"}),
            Ballot(rankings=[], approvals={"Bob"}),
        ]
        result = ApprovalVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        # Bob: 4, Alice: 2, Charlie: 1
        self.assertEqual(result.winner, "Bob")
        self.assertEqual(result.rankings, [("Bob", 4), ("Alice", 2), ("Charlie", 1)])
    
    def test_approval_from_rankings(self):
        """测试从排名推断赞成票"""
        ballots = [
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Bob", "Alice", "Charlie"]),
        ]
        result = ApprovalVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        # 默认赞成前一半候选人
        self.assertIsNotNone(result.winner)


class TestRangeVoting(unittest.TestCase):
    """测试范围投票"""
    
    def test_range_scoring(self):
        """测试范围计分"""
        ballots = [
            Ballot(rankings=[], weights={"Alice": 10, "Bob": 8, "Charlie": 5}),
            Ballot(rankings=[], weights={"Alice": 9, "Bob": 9, "Charlie": 7}),
            Ballot(rankings=[], weights={"Alice": 8, "Bob": 10, "Charlie": 6}),
        ]
        result = RangeVoting.count(ballots, ["Alice", "Bob", "Charlie"])
        
        # Alice平均: (10+9+8)/3 = 9
        # Bob平均: (8+9+10)/3 = 9
        # Charlie平均: (5+7+6)/3 = 6
        self.assertIn(result.winner, ["Alice", "Bob"])
        
        # 检查平均分
        rankings_dict = dict(result.rankings)
        self.assertAlmostEqual(rankings_dict["Alice"], 9.0, places=2)
        self.assertAlmostEqual(rankings_dict["Bob"], 9.0, places=2)
        self.assertAlmostEqual(rankings_dict["Charlie"], 6.0, places=2)
    
    def test_custom_score_range(self):
        """测试自定义分数范围"""
        ballots = [
            Ballot(rankings=[], weights={"A": 100, "B": 50}),
            Ballot(rankings=[], weights={"A": 0, "B": 100}),
        ]
        result = RangeVoting.count(ballots, ["A", "B"], min_score=0, max_score=100)
        
        # A平均: 50, B平均: 75
        self.assertEqual(result.winner, "B")


class TestCoombsMethod(unittest.TestCase):
    """测试库姆斯规则"""
    
    def test_coombs_elimination(self):
        """测试库姆斯淘汰"""
        ballots = [
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Bob", "Alice", "Charlie"]),
            Ballot(rankings=["Charlie", "Alice", "Bob"]),
        ]
        result = CoombsMethod.count(ballots, ["Alice", "Bob", "Charlie"])
        
        # Charlie被最多人排在最后，会被淘汰
        self.assertEqual(result.winner, "Alice")
    
    def test_coombs_vs_irv(self):
        """测试库姆斯与IRV的区别"""
        # 在某些情况下，库姆斯会产生不同的结果
        ballots = [
            Ballot(rankings=["A", "B", "C", "D"]),
            Ballot(rankings=["B", "A", "C", "D"]),
            Ballot(rankings=["C", "B", "A", "D"]),
            Ballot(rankings=["D", "C", "B", "A"]),
        ]
        coombs_result = CoombsMethod.count(ballots, ["A", "B", "C", "D"])
        irv_result = RankedChoiceVoting.count(ballots, ["A", "B", "C", "D"])
        
        # 结果可能不同，这展示了不同方法的特性
        self.assertIsNotNone(coombs_result.winner)
        self.assertIsNotNone(irv_result.winner)


class TestVotingSystem(unittest.TestCase):
    """测试投票系统综合类"""
    
    def test_run_election(self):
        """测试运行选举"""
        ballots = [
            Ballot(rankings=["Alice", "Bob", "Charlie"]),
            Ballot(rankings=["Bob", "Alice", "Charlie"]),
            Ballot(rankings=["Charlie", "Alice", "Bob"]),
        ]
        
        methods = ["plurality", "rcv", "borda", "condorcet", "approval"]
        method_aliases = {
            "plurality": ["plurality"],
            "rcv": ["rcv", "ranked choice", "irv"],
            "borda": ["borda"],
            "condorcet": ["condorcet"],
            "approval": ["approval"],
        }
        
        for method in methods:
            result = VotingSystem.run_election(method, ballots, ["Alice", "Bob", "Charlie"])
            # 检查方法别名是否在结果名称中
            method_lower = result.method.lower()
            found = any(alias in method_lower for alias in method_aliases.get(method, [method]))
            self.assertTrue(found, f"Method '{method}' not found in '{result.method}'")
            self.assertIsNotNone(result.method)
    
    def test_invalid_method(self):
        """测试无效方法"""
        ballots = [Ballot(rankings=["A"])]
        
        with self.assertRaises(ValueError):
            VotingSystem.run_election("invalid_method", ballots, ["A", "B"])
    
    def test_compare_methods(self):
        """测试比较不同方法"""
        ballots = [
            Ballot(rankings=["A", "B", "C"]),
            Ballot(rankings=["A", "C", "B"]),
            Ballot(rankings=["B", "C", "A"]),
            Ballot(rankings=["C", "B", "A"]),
        ]
        
        results = VotingSystem.compare_methods(ballots, ["A", "B", "C"])
        
        self.assertIn("plurality", results)
        self.assertIn("borda", results)
        self.assertIn("condorcet", results)
        
        # 检查各方法都返回了结果
        for method, result in results.items():
            self.assertIsInstance(result, ElectionResult)


class TestRandomBallotGeneration(unittest.TestCase):
    """测试随机选票生成"""
    
    def test_random_ballot_structure(self):
        """测试随机选票结构"""
        candidates = ["A", "B", "C", "D"]
        ballot = generate_random_ballot(candidates)
        
        self.assertEqual(len(ballot.rankings), 4)
        self.assertEqual(set(ballot.rankings), set(candidates))
        self.assertEqual(len(ballot.weights), 4)
        self.assertTrue(len(ballot.approvals) >= 1)
    
    def test_random_ballot_uniqueness(self):
        """测试随机选票的随机性"""
        candidates = ["A", "B", "C"]
        ballots = [generate_random_ballot(candidates) for _ in range(10)]
        
        # 至少有些选票应该不同
        rankings_sets = [tuple(b.rankings) for b in ballots]
        unique_rankings = set(rankings_sets)
        
        # 由于随机性，应该有多种不同的排名
        self.assertGreater(len(unique_rankings), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)