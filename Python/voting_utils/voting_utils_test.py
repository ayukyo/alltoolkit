"""
投票工具测试套件
测试所有投票算法的正确性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voting_utils.mod import (
    PluralityVoting, RankedChoiceVoting, BordaCount,
    ApprovalVoting, CondorcetVoting, SingleTransferableVote,
    ScoreVoting, VotingSimulator,
    plurality, ranked_choice, borda, approval, condorcet, stv, score
)


def test_plurality_voting():
    """测试简单多数投票"""
    print("测试简单多数投票...")
    
    # 基本测试
    ballots = ['Alice', 'Bob', 'Alice', 'Charlie', 'Alice', 'Bob']
    winner, counts = PluralityVoting.vote(ballots)
    assert winner == 'Alice', f"期望 Alice 获胜，实际 {winner}"
    assert counts == {'Alice': 3, 'Bob': 2, 'Charlie': 1}
    
    # 平局测试
    ballots = ['Alice', 'Bob', 'Alice', 'Bob']
    winner, counts, ties = PluralityVoting.vote_with_tiebreaker(ballots, 'alphabetical')
    assert winner == 'Alice'  # 字母顺序
    assert len(ties) == 2
    
    # 空选票测试
    winner, counts = PluralityVoting.vote([])
    assert winner is None
    
    # 包含空票的测试
    ballots = ['Alice', '', 'Bob', None, 'Alice']
    winner, counts = PluralityVoting.vote([b for b in ballots if b])
    assert winner == 'Alice'
    
    print("  ✓ 简单多数投票测试通过")


def test_ranked_choice_voting():
    """测试排序选择投票"""
    print("测试排序选择投票...")
    
    # 简单测试 - Alice 应该在第一轮就过半
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Charlie', 'Bob'],
        ['Bob', 'Alice', 'Charlie'],
        ['Charlie', 'Bob', 'Alice'],
        ['Alice', 'Bob', 'Charlie'],
    ]
    winner, rounds = RankedChoiceVoting.vote(ballots)
    assert winner == 'Alice', f"期望 Alice 获胜，实际 {winner}"
    assert len(rounds) == 1  # 第一轮就决出
    
    # 需要多轮的测试
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Alice', 'Charlie'],
        ['Charlie', 'Alice', 'Bob'],
        ['Charlie', 'Bob', 'Alice'],
        ['Alice', 'Charlie', 'Bob'],
    ]
    winner, rounds = RankedChoiceVoting.vote(ballots)
    # Alice: 2, Bob: 1, Charlie: 2 -> Bob 被淘汰 -> Bob 的票转给 Alice
    assert winner == 'Alice'
    assert len(rounds) >= 2
    
    # 空选票测试
    winner, rounds = RankedChoiceVoting.vote([])
    assert winner is None
    
    print("  ✓ 排序选择投票测试通过")


def test_borda_count():
    """测试波达计数"""
    print("测试波达计数...")
    
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Alice', 'Charlie'],
        ['Charlie', 'Alice', 'Bob'],
    ]
    candidates = ['Alice', 'Bob', 'Charlie']
    
    # 标准计分: Alice: 2+1+1=4, Bob: 1+2+0=3, Charlie: 0+0+2=2
    winner, scores, details = BordaCount.vote(ballots, candidates)
    assert winner == 'Alice', f"期望 Alice 获胜，实际 {winner}"
    assert scores['Alice'] == 4
    assert scores['Bob'] == 3
    assert scores['Charlie'] == 2
    
    # Dowdall 计分
    winner, scores, details = BordaCount.vote(ballots, candidates, scoring='dowdall')
    # Alice: 1 + 0.5 + 0.5 = 2
    # Bob: 0.5 + 1 + 0 = 1.5
    # Charlie: 0 + 0 + 1 = 1
    assert winner == 'Alice'
    
    print("  ✓ 波达计数测试通过")


def test_approval_voting():
    """测试批准投票"""
    print("测试批准投票...")
    
    ballots = [
        ['Alice', 'Bob'],
        ['Bob', 'Charlie'],
        ['Alice', 'Charlie'],
        ['Bob', 'Alice'],
    ]
    candidates = ['Alice', 'Bob', 'Charlie', 'David']
    
    # Alice: 3, Bob: 3, Charlie: 2, David: 0
    winner, approvals = ApprovalVoting.vote(ballots, candidates)
    assert winner in ['Alice', 'Bob']  # Alice 和 Bob 都是 3 票
    
    # 带阈值的批准投票
    winners, approvals = ApprovalVoting.vote_with_threshold(ballots, 2, candidates)
    assert 'Alice' in winners
    assert 'Bob' in winners
    assert 'Charlie' in winners
    assert 'David' not in winners
    
    print("  ✓ 批准投票测试通过")


def test_condorcet_voting():
    """测试孔多塞投票"""
    print("测试孔多塞投票...")
    
    # 创建一个明确的孔多塞赢家场景
    # Alice 在所有一对一对决中都获胜
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Charlie', 'Bob'],
        ['Bob', 'Alice', 'Charlie'],
        ['Charlie', 'Alice', 'Bob'],
    ]
    
    # 孔多塞赢家检查
    condorcet_winner = CondorcetVoting.find_condorcet_winner(ballots)
    assert condorcet_winner == 'Alice', f"期望 Alice 是孔多塞赢家，实际 {condorcet_winner}"
    
    # Schulze 方法
    winner, prefs, ranking = CondorcetVoting.vote(ballots)
    assert winner == 'Alice'
    assert ranking[0] == 'Alice'
    
    # 循环偏好场景（无孔多塞赢家）
    # A > B > C > A
    ballots_cycle = [
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Charlie', 'Alice'],
        ['Charlie', 'Alice', 'Bob'],
    ]
    
    condorcet_winner = CondorcetVoting.find_condorcet_winner(ballots_cycle)
    assert condorcet_winner is None  # 应该没有孔多塞赢家
    
    # 但 Schulze 方法仍然能给出排名
    winner, prefs, ranking = CondorcetVoting.vote(ballots_cycle)
    assert len(ranking) == 3  # 应该能给出完整排名
    
    print("  ✓ 孔多塞投票测试通过")


def test_single_transferable_vote():
    """测试STV"""
    print("测试STV...")
    
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Charlie', 'Bob'],
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Alice', 'Charlie'],
        ['Bob', 'Charlie', 'Alice'],
        ['Charlie', 'Alice', 'Bob'],
        ['Charlie', 'Bob', 'Alice'],
        ['Charlie', 'Alice', 'Bob'],
    ]
    
    winners, stats = SingleTransferableVote.vote(ballots, seats=2)
    # Alice 有 3 票，Charlie 有 3 票，Bob 有 2 票
    # 配额 = (8 / 3) + 1 = 3（向下取整后加1）
    assert 'Alice' in winners
    
    print("  ✓ STV测试通过")


def test_score_voting():
    """测试评分投票"""
    print("测试评分投票...")
    
    ballots = [
        {'Alice': 10, 'Bob': 8, 'Charlie': 5},
        {'Alice': 9, 'Bob': 9, 'Charlie': 6},
        {'Alice': 7, 'Bob': 10, 'Charlie': 8},
    ]
    
    # 总分: Alice: 26, Bob: 27, Charlie: 19
    winner, totals, avg = ScoreVoting.vote(ballots)
    assert winner == 'Bob', f"期望 Bob 获胜，实际 {winner}"
    assert totals['Alice'] == 26
    assert totals['Bob'] == 27
    assert totals['Charlie'] == 19
    
    # 平均分: Alice: 8.67, Bob: 9.0, Charlie: 6.33
    winner_by_avg, avg = ScoreVoting.vote_by_average(ballots)
    assert winner_by_avg == 'Bob'
    
    print("  ✓ 评分投票测试通过")


def test_voting_simulator():
    """测试投票模拟器"""
    print("测试投票模拟器...")
    
    candidates = ['Alice', 'Bob', 'Charlie', 'David']
    
    # 生成简单多数选票
    ballots = VotingSimulator.generate_ballots_plurality(100, candidates, 'uniform', seed=42)
    assert len(ballots) == 100
    assert all(b in candidates for b in ballots)
    
    # 正态分布
    ballots = VotingSimulator.generate_ballots_plurality(100, candidates, 'normal', seed=42)
    assert len(ballots) == 100
    
    # 生成排序选票
    ballots = VotingSimulator.generate_ballots_ranked(50, candidates, 'uniform', seed=42)
    assert len(ballots) == 50
    for ballot in ballots:
        assert len(ballot) == 4
        assert set(ballot) == set(candidates)
    
    # 生成评分选票
    ballots = VotingSimulator.generate_ballots_score(50, candidates, 10, 'uniform', seed=42)
    assert len(ballots) == 50
    for ballot in ballots:
        assert all(0 <= ballot[c] <= 10 for c in candidates)
    
    print("  ✓ 投票模拟器测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # plurality
    winner = plurality(['Alice', 'Bob', 'Alice', 'Bob', 'Alice'])
    assert winner == 'Alice'
    
    # ranked_choice
    winner = ranked_choice([
        ['Alice', 'Bob'],
        ['Alice', 'Bob'],
        ['Bob', 'Alice'],
    ])
    assert winner == 'Alice'
    
    # borda
    winner = borda([
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Alice', 'Charlie'],
    ], ['Alice', 'Bob', 'Charlie'])
    assert winner in ['Alice', 'Bob']
    
    # approval
    winner = approval([
        ['Alice', 'Bob'],
        ['Bob', 'Charlie'],
        ['Alice'],
    ], ['Alice', 'Bob', 'Charlie'])
    assert winner in ['Alice', 'Bob']
    
    # score
    winner = score([
        {'Alice': 10, 'Bob': 5},
        {'Alice': 8, 'Bob': 9},
    ])
    assert winner == 'Alice'  # Alice: 18, Bob: 14
    
    print("  ✓ 便捷函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 单候选人
    ballots = [['Alice'], ['Alice'], ['Alice']]
    winner, rounds = RankedChoiceVoting.vote(ballots, ['Alice'])
    assert winner == 'Alice'
    
    # 所有选票相同
    ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Bob', 'Charlie'],
    ]
    winner, rounds = RankedChoiceVoting.vote(ballots)
    assert winner == 'Alice'
    
    # 波达计数 - 单个候选人
    winner, scores, _ = BordaCount.vote([['Alice']], ['Alice'])
    assert winner == 'Alice'
    assert scores['Alice'] == 0  # n-1 = 0
    
    # STV - 席位数等于候选人数
    ballots = [['Alice', 'Bob'], ['Bob', 'Alice']]
    winners, _ = SingleTransferableVote.vote(ballots, seats=2)
    assert len(winners) == 2
    
    print("  ✓ 边界情况测试通过")


def test_real_world_scenario():
    """测试真实场景"""
    print("测试真实选举场景...")
    
    # 模拟真实选举：3位候选人，100位选民
    candidates = ['张三', '李四', '王五']
    
    # 生成选民偏好
    # 40% 偏好 张三 > 李四 > 王五
    # 35% 偏好 李四 > 王五 > 张三
    # 25% 偏好 王五 > 李四 > 张三
    
    ballots_ranked = (
        [['张三', '李四', '王五']] * 40 +
        [['李四', '王五', '张三']] * 35 +
        [['王五', '李四', '张三']] * 25
    )
    
    ballots_plurality = ['张三'] * 40 + ['李四'] * 35 + ['王五'] * 25
    
    # 简单多数
    winner_p, counts = PluralityVoting.vote(ballots_plurality)
    assert winner_p == '张三'
    print(f"  简单多数: {winner_p} 获胜，票数 {counts}")
    
    # 排序选择
    winner_rc, rounds = RankedChoiceVoting.vote(ballots_ranked)
    # 第一轮：张三 40，李四 35，王五 25
    # 王五被淘汰，票转给李四
    # 第二轮：张三 40，李四 60
    assert winner_rc == '李四'
    print(f"  排序选择: {winner_rc} 获胜，经过 {len(rounds)} 轮")
    
    # 波达计数 (n=3)
    # 张三: 2*40 + 0*35 + 0*25 = 80
    # 李四: 1*40 + 2*35 + 1*25 = 140
    # 王五: 0*40 + 1*35 + 2*25 = 85
    winner_b, scores, _ = BordaCount.vote(ballots_ranked)
    assert winner_b == '李四'
    print(f"  波达计数: {winner_b} 获胜，分数 {scores}")
    
    # 孔多塞
    winner_c, _, ranking = CondorcetVoting.vote(ballots_ranked)
    print(f"  孔多塞: {winner_c} 获胜，排名 {ranking}")
    
    print("  ✓ 真实选举场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("投票工具测试套件")
    print("=" * 50)
    print()
    
    test_plurality_voting()
    test_ranked_choice_voting()
    test_borda_count()
    test_approval_voting()
    test_condorcet_voting()
    test_single_transferable_vote()
    test_score_voting()
    test_voting_simulator()
    test_convenience_functions()
    test_edge_cases()
    test_real_world_scenario()
    
    print()
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()