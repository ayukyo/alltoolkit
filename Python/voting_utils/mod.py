"""
投票选举工具模块 (Voting and Election Utilities)

提供多种投票算法实现，支持各种选举和决策场景。

支持的投票方法:
1. 多数制 (Plurality/First-Past-The-Post)
2. 两轮决选制 (Two-Round System/Runoff)
3. 排名选择投票 (Ranked Choice Voting / Instant Runoff)
4. 波达计数法 (Borda Count)
5. 孔多塞方法 (Condorcet Method)
6. 单一可转移投票 (Single Transferable Vote - STV)
7. 比例代表制 (Proportional Representation - D'Hondt Method)
8. 赞成投票 (Approval Voting)
9. 范围投票 (Range Voting / Score Voting)
10. 库姆斯规则 (Coombs' Method)

零外部依赖，纯Python实现。
"""

from typing import List, Dict, Tuple, Optional, Set, Any
from collections import defaultdict, Counter
from dataclasses import dataclass
import random
import math


@dataclass
class Candidate:
    """候选人类"""
    name: str
    id: Optional[str] = None
    
    def __hash__(self):
        return hash(self.id or self.name)
    
    def __eq__(self, other):
        if isinstance(other, Candidate):
            return (self.id or self.name) == (other.id or other.name)
        return False
    
    def __repr__(self):
        return self.name


@dataclass
class Ballot:
    """选票类"""
    rankings: List[str]  # 按偏好排序的候选人名称列表
    weights: Optional[Dict[str, float]] = None  # 用于范围投票的分数
    approvals: Optional[Set[str]] = None  # 用于赞成投票
    
    def __post_init__(self):
        if self.approvals is None:
            self.approvals = set()


@dataclass
class ElectionResult:
    """选举结果类"""
    winner: Optional[str]
    rankings: List[Tuple[str, int]]  # 候选人及其得票/得分
    rounds: Optional[List[Dict[str, int]]] = None  # 多轮投票的各轮结果
    method: str = ""
    details: Optional[Dict[str, Any]] = None
    
    def __repr__(self):
        if self.winner:
            return f"ElectionResult(winner='{self.winner}', method='{self.method}')"
        return f"ElectionResult(winner=None, method='{self.method}')"


class PluralityVoting:
    """多数制投票 (First-Past-The-Post)"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算多数制投票结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        votes = Counter()
        for ballot in ballots:
            if ballot.rankings:
                first_choice = ballot.rankings[0]
                if first_choice in candidates:
                    votes[first_choice] += 1
        
        sorted_results = votes.most_common()
        winner = sorted_results[0][0] if sorted_results else None
        
        return ElectionResult(
            winner=winner,
            rankings=sorted_results,
            method="Plurality (First-Past-The-Post)",
            details={"total_votes": len(ballots), "valid_votes": sum(votes.values())}
        )


class RunoffVoting:
    """两轮决选制"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str], threshold: float = 0.5) -> ElectionResult:
        """
        计算两轮决选结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            threshold: 获胜阈值（默认50%）
            
        Returns:
            ElectionResult: 选举结果
        """
        # 第一轮
        first_round = Counter()
        for ballot in ballots:
            if ballot.rankings:
                first_choice = ballot.rankings[0]
                if first_choice in candidates:
                    first_round[first_choice] += 1
        
        total_votes = sum(first_round.values())
        rounds = [dict(first_round)]
        
        # 检查是否有人达到阈值
        for candidate, votes in first_round.items():
            if votes / total_votes > threshold:
                return ElectionResult(
                    winner=candidate,
                    rankings=first_round.most_common(),
                    rounds=rounds,
                    method="Two-Round Runoff",
                    details={"won_in_round": 1, "threshold": threshold}
                )
        
        # 第二轮：取前两名
        top_two = [c for c, _ in first_round.most_common(2)]
        second_round = Counter()
        
        for ballot in ballots:
            for choice in ballot.rankings:
                if choice in top_two:
                    second_round[choice] += 1
                    break
        
        rounds.append(dict(second_round))
        sorted_results = second_round.most_common()
        winner = sorted_results[0][0] if sorted_results else None
        
        return ElectionResult(
            winner=winner,
            rankings=sorted_results,
            rounds=rounds,
            method="Two-Round Runoff",
            details={"threshold": threshold, "finalists": top_two}
        )


class RankedChoiceVoting:
    """排名选择投票 (Instant Runoff Voting)"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算即时决选投票结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        active_candidates = set(candidates)
        rounds = []
        
        while len(active_candidates) > 1:
            # 统计当前轮的第一选择票
            current_round = Counter()
            for ballot in ballots:
                for choice in ballot.rankings:
                    if choice in active_candidates:
                        current_round[choice] += 1
                        break
            
            if not current_round:
                break
            
            rounds.append(dict(current_round))
            total_votes = sum(current_round.values())
            
            # 检查是否有人超过50%
            for candidate, votes in current_round.items():
                if votes > total_votes / 2:
                    return ElectionResult(
                        winner=candidate,
                        rankings=current_round.most_common(),
                        rounds=rounds,
                        method="Ranked Choice Voting (IRV)",
                        details={"rounds_held": len(rounds)}
                    )
            
            # 淘汰得票最少的候选人
            min_votes = min(current_round.values())
            to_eliminate = [c for c, v in current_round.items() if v == min_votes]
            
            # 如果所有剩余候选人票数相同，随机选择淘汰
            if len(to_eliminate) == len(active_candidates):
                to_eliminate = [random.choice(to_eliminate)]
            
            for c in to_eliminate:
                active_candidates.discard(c)
        
        winner = list(active_candidates)[0] if active_candidates else None
        
        return ElectionResult(
            winner=winner,
            rankings=current_round.most_common() if 'current_round' in dir() else [],
            rounds=rounds,
            method="Ranked Choice Voting (IRV)",
            details={"rounds_held": len(rounds)}
        )


class BordaCount:
    """波达计数法"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算波达计数结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        scores = defaultdict(int)
        n = len(candidates)
        
        for ballot in ballots:
            for rank, candidate in enumerate(ballot.rankings):
                if candidate in candidates:
                    # 波达分数：n-1-rank（第一名得n-1分，最后一名得0分）
                    borda_score = n - 1 - rank
                    scores[candidate] += borda_score
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        winner = sorted_results[0][0] if sorted_results else None
        
        return ElectionResult(
            winner=winner,
            rankings=sorted_results,
            method="Borda Count",
            details={"max_possible_score": len(ballots) * (n - 1)}
        )


class CondorcetMethod:
    """孔多塞方法"""
    
    @staticmethod
    def build_pairwise_matrix(ballots: List[Ballot], candidates: List[str]) -> Dict[str, Dict[str, int]]:
        """构建两两比较矩阵"""
        pairwise = {c1: {c2: 0 for c2 in candidates} for c1 in candidates}
        
        for ballot in ballots:
            rankings = ballot.rankings
            for i, c1 in enumerate(rankings):
                if c1 not in candidates:
                    continue
                for j in range(i + 1, len(rankings)):
                    c2 = rankings[j]
                    if c2 in candidates:
                        pairwise[c1][c2] += 1
        
        return pairwise
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算孔多塞结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        pairwise = CondorcetMethod.build_pairwise_matrix(ballots, candidates)
        
        # 找出孔多塞赢家（在所有两两对决中获胜的候选人）
        condorcet_winner = None
        for c1 in candidates:
            wins_all = True
            for c2 in candidates:
                if c1 != c2:
                    if pairwise[c1][c2] <= pairwise[c2][c1]:
                        wins_all = False
                        break
            if wins_all:
                condorcet_winner = c1
                break
        
        # 计算胜场数用于排名
        wins_count = {}
        for c1 in candidates:
            wins = 0
            for c2 in candidates:
                if c1 != c2 and pairwise[c1][c2] > pairwise[c2][c1]:
                    wins += 1
            wins_count[c1] = wins
        
        sorted_results = sorted(wins_count.items(), key=lambda x: x[1], reverse=True)
        
        return ElectionResult(
            winner=condorcet_winner,
            rankings=sorted_results,
            method="Condorcet Method",
            details={"pairwise_matrix": pairwise, "condorcet_exists": condorcet_winner is not None}
        )


class SingleTransferableVote:
    """单一可转移投票 (STV)"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str], seats: int = 1, 
              quota_method: str = "droop") -> ElectionResult:
        """
        计算STV结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            seats: 需要选出的席位数
            quota_method: 配额计算方法 ("droop" 或 "hare")
            
        Returns:
            ElectionResult: 选举结果
        """
        total_votes = len(ballots)
        
        # 计算配额
        if quota_method == "droop":
            quota = math.floor(total_votes / (seats + 1)) + 1
        else:  # hare
            quota = math.floor(total_votes / seats)
        
        active_candidates = set(candidates)
        elected = []
        eliminated = []
        rounds = []
        vote_values = defaultdict(float)  # 每张选票的当前价值
        
        # 初始化选票价值
        for i, ballot in enumerate(ballots):
            vote_values[i] = 1.0
        
        while len(elected) < seats and len(active_candidates) > seats - len(elected):
            # 统计当前轮选票
            current_round = defaultdict(float)
            
            for i, ballot in enumerate(ballots):
                for choice in ballot.rankings:
                    if choice in active_candidates:
                        current_round[choice] += vote_values[i]
                        break
            
            rounds.append(dict(current_round))
            
            if not current_round:
                break
            
            # 检查是否有人达到配额
            someone_elected = False
            for candidate, votes in list(current_round.items()):
                if votes >= quota:
                    elected.append(candidate)
                    active_candidates.discard(candidate)
                    someone_elected = True
                    
                    # 重新分配剩余票值
                    surplus = votes - quota
                    if surplus > 0:
                        transfer_value = surplus / votes
                        for i, ballot in enumerate(ballots):
                            if ballot.rankings and ballot.rankings[0] == candidate:
                                vote_values[i] *= transfer_value
                    break
            
            if someone_elected:
                continue
            
            # 淘汰得票最少的候选人
            min_votes = min(current_round.values())
            to_eliminate = [c for c, v in current_round.items() if v == min_votes]
            
            if len(to_eliminate) == len(active_candidates):
                break
            
            for c in to_eliminate:
                active_candidates.discard(c)
                eliminated.append(c)
        
        # 如果还没选够，从剩余候选人中选择得票最高的
        while len(elected) < seats and active_candidates:
            current_round = defaultdict(float)
            for i, ballot in enumerate(ballots):
                for choice in ballot.rankings:
                    if choice in active_candidates:
                        current_round[choice] += vote_values[i]
                        break
            
            if current_round:
                winner = max(current_round.items(), key=lambda x: x[1])[0]
                elected.append(winner)
                active_candidates.discard(winner)
            else:
                break
        
        return ElectionResult(
            winner=elected[0] if elected else None,
            rankings=[(c, 0) for c in elected],  # STV的排名不太适用
            rounds=rounds,
            method="Single Transferable Vote (STV)",
            details={"seats": seats, "quota": quota, "elected": elected}
        )


class DHondtMethod:
    """洪德法（比例代表制）"""
    
    @staticmethod
    def count(party_votes: Dict[str, int], seats: int) -> ElectionResult:
        """
        使用洪德法分配席位
        
        Args:
            party_votes: 各政党得票数字典
            seats: 需要分配的席位总数
            
        Returns:
            ElectionResult: 选举结果
        """
        quotients = {party: votes for party, votes in party_votes.items()}
        seat_allocation = {party: 0 for party in party_votes}
        rounds = []
        
        for _ in range(seats):
            round_scores = {party: party_votes[party] / (seat_allocation[party] + 1) 
                          for party in party_votes}
            rounds.append(round_scores.copy())
            
            winner = max(round_scores.items(), key=lambda x: x[1])[0]
            seat_allocation[winner] += 1
        
        sorted_results = sorted(seat_allocation.items(), key=lambda x: x[1], reverse=True)
        
        return ElectionResult(
            winner=sorted_results[0][0] if sorted_results else None,
            rankings=sorted_results,
            rounds=rounds,
            method="D'Hondt Method (Proportional Representation)",
            details={"total_seats": seats, "party_votes": party_votes}
        )


class ApprovalVoting:
    """赞成投票"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算赞成投票结果
        
        Args:
            ballots: 选票列表（每张选票可赞成多个候选人）
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        approvals = Counter()
        
        for ballot in ballots:
            if ballot.approvals:
                for candidate in ballot.approvals:
                    if candidate in candidates:
                        approvals[candidate] += 1
            # 如果没有明确设置approvals，默认选择排名前半的候选人
            elif ballot.rankings:
                approve_count = max(1, len(ballot.rankings) // 2)
                for candidate in ballot.rankings[:approve_count]:
                    if candidate in candidates:
                        approvals[candidate] += 1
        
        sorted_results = approvals.most_common()
        winner = sorted_results[0][0] if sorted_results else None
        
        return ElectionResult(
            winner=winner,
            rankings=sorted_results,
            method="Approval Voting",
            details={"total_approvals": sum(approvals.values())}
        )


class RangeVoting:
    """范围投票 / 评分投票"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str], 
              min_score: int = 0, max_score: int = 10) -> ElectionResult:
        """
        计算范围投票结果
        
        Args:
            ballots: 选票列表（每张选票包含对每个候选人的评分）
            candidates: 候选人列表
            min_score: 最低分
            max_score: 最高分
            
        Returns:
            ElectionResult: 选举结果
        """
        total_scores = defaultdict(float)
        vote_counts = defaultdict(int)
        
        for ballot in ballots:
            if ballot.weights:
                for candidate, score in ballot.weights.items():
                    if candidate in candidates:
                        clamped_score = max(min_score, min(max_score, score))
                        total_scores[candidate] += clamped_score
                        vote_counts[candidate] += 1
        
        # 计算平均分
        average_scores = {}
        for candidate in candidates:
            if vote_counts[candidate] > 0:
                average_scores[candidate] = total_scores[candidate] / vote_counts[candidate]
            else:
                average_scores[candidate] = 0
        
        sorted_results = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)
        winner = sorted_results[0][0] if sorted_results else None
        
        return ElectionResult(
            winner=winner,
            rankings=sorted_results,
            method="Range Voting (Score Voting)",
            details={
                "score_range": (min_score, max_score),
                "total_scores": dict(total_scores),
                "vote_counts": dict(vote_counts)
            }
        )


class CoombsMethod:
    """库姆斯规则"""
    
    @staticmethod
    def count(ballots: List[Ballot], candidates: List[str]) -> ElectionResult:
        """
        计算库姆斯规则结果
        
        与IRV类似，但淘汰的是被最多人排在最后的候选人
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            
        Returns:
            ElectionResult: 选举结果
        """
        active_candidates = set(candidates)
        rounds = []
        
        while len(active_candidates) > 1:
            # 统计当前轮的第一选择票
            first_choices = Counter()
            last_choices = Counter()
            
            for ballot in ballots:
                valid_choices = [c for c in ballot.rankings if c in active_candidates]
                
                if valid_choices:
                    first_choices[valid_choices[0]] += 1
                    last_choices[valid_choices[-1]] += 1
            
            if not first_choices:
                break
            
            rounds.append({
                "first_choices": dict(first_choices),
                "last_choices": dict(last_choices)
            })
            
            total_votes = sum(first_choices.values())
            
            # 检查是否有人超过50%
            for candidate, votes in first_choices.items():
                if votes > total_votes / 2:
                    return ElectionResult(
                        winner=candidate,
                        rankings=first_choices.most_common(),
                        rounds=rounds,
                        method="Coombs' Method",
                        details={"rounds_held": len(rounds)}
                    )
            
            # 淘汰被最多人排在最后的候选人
            max_last = max(last_choices.values())
            to_eliminate = [c for c, v in last_choices.items() if v == max_last]
            
            if len(to_eliminate) == len(active_candidates):
                break
            
            for c in to_eliminate:
                active_candidates.discard(c)
        
        winner = list(active_candidates)[0] if active_candidates else None
        
        return ElectionResult(
            winner=winner,
            rankings=first_choices.most_common() if 'first_choices' in dir() else [],
            rounds=rounds,
            method="Coombs' Method",
            details={"rounds_held": len(rounds)}
        )


class VotingSystem:
    """投票系统综合类"""
    
    METHODS = {
        "plurality": PluralityVoting,
        "runoff": RunoffVoting,
        "rcv": RankedChoiceVoting,
        "borda": BordaCount,
        "condorcet": CondorcetMethod,
        "stv": SingleTransferableVote,
        "dhondt": DHondtMethod,
        "approval": ApprovalVoting,
        "range": RangeVoting,
        "coombs": CoombsMethod,
    }
    
    @staticmethod
    def run_election(method: str, ballots: List[Ballot], candidates: List[str], 
                    **kwargs) -> ElectionResult:
        """
        运行选举
        
        Args:
            method: 投票方法名称
            ballots: 选票列表
            candidates: 候选人列表
            **kwargs: 额外参数（如STV的seats参数）
            
        Returns:
            ElectionResult: 选举结果
        """
        method = method.lower()
        
        if method not in VotingSystem.METHODS:
            raise ValueError(f"未知的投票方法: {method}. 可用方法: {list(VotingSystem.METHODS.keys())}")
        
        voting_class = VotingSystem.METHODS[method]
        
        if method == "dhondt":
            # 洪德法需要政党得票数
            return voting_class.count(ballots, kwargs.get("seats", 1))
        elif method == "stv":
            return voting_class.count(ballots, candidates, 
                                     seats=kwargs.get("seats", 1),
                                     quota_method=kwargs.get("quota_method", "droop"))
        elif method == "range":
            return voting_class.count(ballots, candidates,
                                     min_score=kwargs.get("min_score", 0),
                                     max_score=kwargs.get("max_score", 10))
        elif method == "runoff":
            return voting_class.count(ballots, candidates,
                                     threshold=kwargs.get("threshold", 0.5))
        else:
            return voting_class.count(ballots, candidates)
    
    @staticmethod
    def compare_methods(ballots: List[Ballot], candidates: List[str], 
                       methods: Optional[List[str]] = None) -> Dict[str, ElectionResult]:
        """
        比较不同投票方法的结果
        
        Args:
            ballots: 选票列表
            candidates: 候选人列表
            methods: 要比较的方法列表，默认比较所有方法
            
        Returns:
            Dict[str, ElectionResult]: 各方法的选举结果
        """
        if methods is None:
            methods = [m for m in VotingSystem.METHODS.keys() if m != "dhondt"]
        
        results = {}
        for method in methods:
            try:
                results[method] = VotingSystem.run_election(method, ballots, candidates)
            except Exception as e:
                results[method] = ElectionResult(
                    winner=None,
                    rankings=[],
                    method=method,
                    details={"error": str(e)}
                )
        
        return results


def create_ballot(rankings: List[str], weights: Optional[Dict[str, float]] = None,
                 approvals: Optional[Set[str]] = None) -> Ballot:
    """创建选票的便捷函数"""
    return Ballot(rankings=rankings, weights=weights, approvals=approvals)


def generate_random_ballot(candidates: List[str], approve_count: Optional[int] = None,
                          score_range: Tuple[int, int] = (0, 10)) -> Ballot:
    """生成随机选票（用于模拟和测试）"""
    shuffled = candidates.copy()
    random.shuffle(shuffled)
    
    weights = {c: random.randint(score_range[0], score_range[1]) for c in candidates}
    
    if approve_count is None:
        approve_count = random.randint(1, len(candidates))
    approvals = set(random.sample(candidates, min(approve_count, len(candidates))))
    
    return Ballot(rankings=shuffled, weights=weights, approvals=approvals)


if __name__ == "__main__":
    # 简单演示
    candidates = ["Alice", "Bob", "Charlie", "David"]
    
    # 生成随机选票
    ballots = [generate_random_ballot(candidates) for _ in range(100)]
    
    # 比较不同投票方法
    results = VotingSystem.compare_methods(ballots, candidates)
    
    print("=" * 60)
    print("投票方法比较结果")
    print("=" * 60)
    
    for method, result in results.items():
        print(f"\n{result.method}:")
        print(f"  获胜者: {result.winner}")
        if result.rankings:
            print(f"  排名: {result.rankings[:3]}...")