"""
Voting Utilities - 多种投票算法实现

包含以下投票方法：
1. Plurality Voting (简单多数/领先者获胜)
2. Ranked Choice Voting (排序选择投票/即时决选)
3. Borda Count (波达计数法)
4. Condorcet Method (孔多塞法 - Schulze算法)
5. Approval Voting (批准投票)
6. Single Transferable Vote (单记可转移投票 STV)
7. Score Voting (评分投票)

所有算法零外部依赖，纯Python实现。
"""

from typing import List, Dict, Tuple, Optional, Set, Any
from collections import defaultdict
import random
import copy


class PluralityVoting:
    """
    简单多数投票（领先者获胜）
    每个选民投一票，得票最多者获胜
    """
    
    @staticmethod
    def vote(ballots: List[str]) -> Tuple[str, Dict[str, int]]:
        """
        计算简单多数投票结果
        
        Args:
            ballots: 选票列表，每张选票是一个候选人名称
            
        Returns:
            (获胜者, 各候选人得票数)
        """
        counts = defaultdict(int)
        for ballot in ballots:
            if ballot:  # 忽略空票
                counts[ballot] += 1
        
        if not counts:
            return None, {}
        
        winner = max(counts.keys(), key=lambda x: counts[x])
        return winner, dict(counts)
    
    @staticmethod
    def vote_with_tiebreaker(ballots: List[str], 
                             tiebreaker: str = 'random',
                             seed: Optional[int] = None) -> Tuple[str, Dict[str, int], List[str]]:
        """
        带平局处理的多数投票
        
        Args:
            ballots: 选票列表
            tiebreaker: 平局处理方式 ('random' 随机, 'alphabetical' 字母顺序)
            seed: 随机种子
            
        Returns:
            (获胜者, 各候选人得票数, 平局候选人列表)
        """
        counts = defaultdict(int)
        for ballot in ballots:
            if ballot:
                counts[ballot] += 1
        
        if not counts:
            return None, {}, []
        
        max_votes = max(counts.values())
        winners = [c for c, v in counts.items() if v == max_votes]
        
        if len(winners) == 1:
            return winners[0], dict(counts), []
        
        # 处理平局
        if tiebreaker == 'alphabetical':
            winner = sorted(winners)[0]
        else:
            if seed is not None:
                random.seed(seed)
            winner = random.choice(winners)
        
        return winner, dict(counts), winners


class RankedChoiceVoting:
    """
    排序选择投票（即时决选投票 - IRV）
    选民按偏好排序候选人，依次淘汰得票最少的候选人
    """
    
    @staticmethod
    def vote(ballots: List[List[str]], 
             candidates: Optional[List[str]] = None) -> Tuple[str, List[Dict]]:
        """
        执行排序选择投票
        
        Args:
            ballots: 选票列表，每张选票是候选人的排序列表（最偏好在前）
            candidates: 所有候选人列表（可选，从选票推断）
            
        Returns:
            (获胜者, 各轮投票详情列表)
        """
        if not ballots:
            return None, []
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return None, []
        
        candidates = set(candidates)
        eliminated = set()
        rounds = []
        
        while True:
            # 统计当前首选票
            counts = defaultdict(int)
            for ballot in ballots:
                for choice in ballot:
                    if choice and choice in candidates and choice not in eliminated:
                        counts[choice] += 1
                        break
            
            total = sum(counts.values())
            if total == 0:
                return None, rounds
            
            # 记录本轮结果
            round_result = {
                'counts': dict(counts),
                'total': total,
                'eliminated': list(eliminated)
            }
            rounds.append(round_result)
            
            # 检查是否有人过半
            for candidate, votes in counts.items():
                if votes > total / 2:
                    return candidate, rounds
            
            # 淘汰得票最少的候选人
            min_votes = min(counts.values())
            to_eliminate = [c for c, v in counts.items() if v == min_votes]
            
            # 如果所有人票数相同，随机淘汰一个
            if len(to_eliminate) == len(counts):
                to_eliminate = [random.choice(to_eliminate)]
            
            for c in to_eliminate:
                eliminated.add(c)
            
            # 检查是否只剩一人
            remaining = candidates - eliminated
            if len(remaining) == 1:
                return list(remaining)[0], rounds
            elif len(remaining) == 0:
                return None, rounds


class BordaCount:
    """
    波达计数法
    选民对候选人排序，根据排名赋分，总分最高者获胜
    """
    
    @staticmethod
    def vote(ballots: List[List[str]], 
             candidates: Optional[List[str]] = None,
             scoring: str = 'standard') -> Tuple[str, Dict[str, int], List[Dict]]:
        """
        执行波达计数投票
        
        Args:
            ballots: 选票列表，每张选票是候选人的排序列表
            candidates: 所有候选人列表
            scoring: 计分方式 
                - 'standard': n-1, n-2, ..., 0 (标准)
                - 'dowdall': 1, 1/2, 1/3, ... (道达尔制)
                - 'custom': 自定义分数列表
                
        Returns:
            (获胜者, 各候选人总分, 各选票得分详情)
        """
        if not ballots:
            return None, {}, []
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return None, {}, []
        
        n = len(candidates)
        scores = defaultdict(int)
        details = []
        
        for ballot in ballots:
            ballot_scores = {}
            for rank, candidate in enumerate(ballot):
                if candidate and candidate in candidates:
                    if scoring == 'standard':
                        score = max(0, n - rank - 1)
                    elif scoring == 'dowdall':
                        score = 1 / (rank + 1) if rank < n else 0
                    else:
                        score = max(0, n - rank - 1)
                    
                    scores[candidate] += score
                    ballot_scores[candidate] = score
            
            details.append({
                'ballot': ballot,
                'scores': ballot_scores
            })
        
        if not scores:
            return None, {}, details
        
        winner = max(scores.keys(), key=lambda x: scores[x])
        return winner, dict(scores), details


class ApprovalVoting:
    """
    批准投票
    选民可以批准多个候选人，获得最多批准的候选人获胜
    """
    
    @staticmethod
    def vote(ballots: List[List[str]], 
             candidates: Optional[List[str]] = None) -> Tuple[str, Dict[str, int]]:
        """
        执行批准投票
        
        Args:
            ballots: 选票列表，每张选票是被批准的候选人列表
            candidates: 所有候选人列表
            
        Returns:
            (获胜者, 各候选人批准数)
        """
        if not ballots:
            return None, {}
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return None, {}
        
        approvals = defaultdict(int)
        for ballot in ballots:
            for candidate in ballot:
                if candidate and candidate in candidates:
                    approvals[candidate] += 1
        
        if not approvals:
            return None, {}
        
        winner = max(approvals.keys(), key=lambda x: approvals[x])
        return winner, dict(approvals)
    
    @staticmethod
    def vote_with_threshold(ballots: List[List[str]], 
                           threshold: int,
                           candidates: Optional[List[str]] = None) -> Tuple[List[str], Dict[str, int]]:
        """
        带阈值的批准投票（选出所有达到阈值的候选人）
        
        Args:
            ballots: 选票列表
            threshold: 批准数阈值
            candidates: 所有候选人列表
            
        Returns:
            (获胜者列表, 各候选人批准数)
        """
        winner, approvals = ApprovalVoting.vote(ballots, candidates)
        if not approvals:
            return [], {}
        
        winners = [c for c, v in approvals.items() if v >= threshold]
        return winners, approvals


class CondorcetVoting:
    """
    孔多塞投票法
    使用Schulze方法计算获胜者
    """
    
    @staticmethod
    def _build_preference_matrix(ballots: List[List[str]], 
                                  candidates: List[str]) -> Dict[Tuple[str, str], int]:
        """构建候选人对决偏好矩阵"""
        preferences = defaultdict(int)
        
        for ballot in ballots:
            for i, c1 in enumerate(ballot):
                if c1 not in candidates:
                    continue
                for j, c2 in enumerate(ballot):
                    if i >= j or c2 not in candidates:
                        continue
                    # c1 排在 c2 前面
                    preferences[(c1, c2)] += 1
        
        return dict(preferences)
    
    @staticmethod
    def _schulze_method(candidates: List[str], 
                        preferences: Dict[Tuple[str, str], int]) -> List[str]:
        """
        Schulze方法计算排名
        
        返回按排名排序的候选人列表
        """
        n = len(candidates)
        if n == 0:
            return []
        if n == 1:
            return candidates
        
        # 构建强度矩阵
        strength = {}
        for c1 in candidates:
            for c2 in candidates:
                if c1 != c2:
                    pref = preferences.get((c1, c2), 0)
                    pref_rev = preferences.get((c2, c1), 0)
                    strength[(c1, c2)] = pref if pref > pref_rev else 0
        
        # Floyd-Warshall 变体
        for ci in candidates:
            for c1 in candidates:
                if ci == c1:
                    continue
                for c2 in candidates:
                    if ci == c2 or c1 == c2:
                        continue
                    s1 = strength.get((c1, ci), 0)
                    s2 = strength.get((ci, c2), 0)
                    current = strength.get((c1, c2), 0)
                    strength[(c1, c2)] = max(current, min(s1, s2))
        
        # 计算每个候选人的胜利数
        wins = {c: 0 for c in candidates}
        for c1 in candidates:
            for c2 in candidates:
                if c1 != c2:
                    s1 = strength.get((c1, c2), 0)
                    s2 = strength.get((c2, c1), 0)
                    if s1 > s2:
                        wins[c1] += 1
        
        # 按胜利数排序
        sorted_candidates = sorted(candidates, key=lambda x: wins[x], reverse=True)
        return sorted_candidates
    
    @staticmethod
    def vote(ballots: List[List[str]], 
             candidates: Optional[List[str]] = None) -> Tuple[Optional[str], Dict, List[str]]:
        """
        执行孔多塞投票（Schulze方法）
        
        Args:
            ballots: 选票列表，每张选票是候选人的排序列表
            candidates: 所有候选人列表
            
        Returns:
            (获胜者, 对决矩阵, 完整排名)
        """
        if not ballots:
            return None, {}, []
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return None, {}, []
        
        candidates = list(candidates)
        preferences = CondorcetVoting._build_preference_matrix(ballots, candidates)
        ranking = CondorcetVoting._schulze_method(candidates, preferences)
        
        winner = ranking[0] if ranking else None
        return winner, preferences, ranking
    
    @staticmethod
    def find_condorcet_winner(ballots: List[List[str]], 
                              candidates: Optional[List[str]] = None) -> Optional[str]:
        """
        查找孔多塞赢家（在所有一对一对决中都获胜的候选人）
        可能不存在
        
        Args:
            ballots: 选票列表
            candidates: 所有候选人列表
            
        Returns:
            孔多塞赢家（如果存在），否则返回None
        """
        if not ballots:
            return None
        
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return None
        
        preferences = CondorcetVoting._build_preference_matrix(ballots, candidates)
        
        for c1 in candidates:
            is_winner = True
            for c2 in candidates:
                if c1 == c2:
                    continue
                pref = preferences.get((c1, c2), 0)
                pref_rev = preferences.get((c2, c1), 0)
                if pref <= pref_rev:
                    is_winner = False
                    break
            if is_winner:
                return c1
        
        return None


class SingleTransferableVote:
    """
    单记可转移投票（STV）
    用于多席位选举，实现比例代表
    """
    
    @staticmethod
    def vote(ballots: List[List[str]], 
             seats: int,
             candidates: Optional[List[str]] = None) -> Tuple[List[str], Dict]:
        """
        执行STV投票
        
        Args:
            ballots: 选票列表
            seats: 席位数
            candidates: 所有候选人列表
            
        Returns:
            (当选者列表, 详细统计信息)
        """
        if not ballots or seats <= 0:
            return [], {}
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot if c))
        
        if not candidates:
            return [], {}
        
        total_votes = len(ballots)
        quota = (total_votes // (seats + 1)) + 1  # Droop 配额
        
        elected = []
        eliminated = set()
        vote_counts = {c: 0 for c in candidates}
        stats = {
            'quota': quota,
            'rounds': [],
            'total_votes': total_votes
        }
        
        # 初始化：统计第一选择票
        current_ballots = [list(b) for b in ballots]  # 复制选票
        
        while len(elected) < seats and len(eliminated) < len(candidates):
            # 重置计数
            vote_counts = {c: 0 for c in candidates if c not in eliminated and c not in elected}
            
            # 统计当前首选
            transfer_values = defaultdict(float)
            for ballot in current_ballots:
                for choice in ballot:
                    if choice in vote_counts:
                        transfer_values[choice] += 1
                        break
            
            # 应用之前的转移
            for c, v in transfer_values.items():
                vote_counts[c] = v
            
            # 记录本轮
            round_info = {
                'counts': dict(vote_counts),
                'elected': list(elected),
                'eliminated': list(eliminated)
            }
            stats['rounds'].append(round_info)
            
            if not vote_counts:
                break
            
            # 检查是否有人达到配额
            any_elected = False
            for candidate, votes in list(vote_counts.items()):
                if votes >= quota and candidate not in elected:
                    elected.append(candidate)
                    any_elected = True
                    
                    # 转移多余选票（简化版：不实际转移）
                    # 实际STV会更复杂地处理转移
                    break
            
            if any_elected:
                continue
            
            # 淘汰得票最少的候选人
            min_votes = min(vote_counts.values())
            to_eliminate = [c for c, v in vote_counts.items() if v == min_votes]
            
            if len(to_eliminate) == len(vote_counts):
                # 所有人票数相同，随机选择淘汰
                to_eliminate = [random.choice(to_eliminate)]
            
            for c in to_eliminate:
                eliminated.add(c)
        
        stats['final_counts'] = vote_counts
        return elected, stats


class ScoreVoting:
    """
    评分投票（范围投票）
    选民对每个候选人打分，总分最高者获胜
    """
    
    @staticmethod
    def vote(ballots: List[Dict[str, int]], 
             max_score: int = 10,
             candidates: Optional[List[str]] = None) -> Tuple[str, Dict[str, int], Dict[str, float]]:
        """
        执行评分投票
        
        Args:
            ballots: 选票列表，每张选票是 {候选人: 分数} 的字典
            max_score: 最高分
            candidates: 所有候选人列表
            
        Returns:
            (获胜者, 各候选人总分, 各候选人平均分)
        """
        if not ballots:
            return None, {}, {}
        
        # 确定候选人
        if candidates is None:
            candidates = list(set(c for ballot in ballots for c in ballot.keys() if c))
        
        if not candidates:
            return None, {}, {}
        
        total_scores = defaultdict(int)
        score_counts = defaultdict(int)
        
        for ballot in ballots:
            for candidate, score in ballot.items():
                if candidate in candidates and 0 <= score <= max_score:
                    total_scores[candidate] += score
                    score_counts[candidate] += 1
        
        if not total_scores:
            return None, {}, {}
        
        # 计算平均分
        avg_scores = {}
        for c in total_scores:
            if score_counts[c] > 0:
                avg_scores[c] = total_scores[c] / score_counts[c]
            else:
                avg_scores[c] = 0.0
        
        winner = max(total_scores.keys(), key=lambda x: total_scores[x])
        return winner, dict(total_scores), avg_scores
    
    @staticmethod
    def vote_by_average(ballots: List[Dict[str, int]], 
                       max_score: int = 10,
                       candidates: Optional[List[str]] = None) -> Tuple[str, Dict[str, float]]:
        """
        按平均分决定获胜者
        
        Returns:
            (获胜者, 各候选人平均分)
        """
        winner, total, avg = ScoreVoting.vote(ballots, max_score, candidates)
        if not avg:
            return None, {}
        
        winner_by_avg = max(avg.keys(), key=lambda x: avg[x])
        return winner_by_avg, avg


class VotingSimulator:
    """
    投票模拟器
    生成模拟选票并比较不同投票方法的结果
    """
    
    @staticmethod
    def generate_ballots_plurality(n_voters: int, 
                                    candidates: List[str],
                                    distribution: str = 'uniform',
                                    seed: Optional[int] = None) -> List[str]:
        """
        生成简单多数投票的模拟选票
        
        Args:
            n_voters: 选民数量
            candidates: 候选人列表
            distribution: 分布类型 ('uniform', 'normal', 'polarized')
            seed: 随机种子
            
        Returns:
            选票列表
        """
        if seed is not None:
            random.seed(seed)
        
        if distribution == 'uniform':
            return [random.choice(candidates) for _ in range(n_voters)]
        
        elif distribution == 'normal':
            # 中心候选人得票更多
            weights = [1.0] * len(candidates)
            mid = len(candidates) // 2
            for i in range(len(candidates)):
                weights[i] = 1.0 / (abs(i - mid) + 1)
            total = sum(weights)
            weights = [w / total for w in weights]
            return [random.choices(candidates, weights=weights)[0] for _ in range(n_voters)]
        
        elif distribution == 'polarized':
            # 两极化分布
            n = len(candidates)
            if n < 2:
                return [random.choice(candidates) for _ in range(n_voters)]
            
            weights = [0.0] * n
            weights[0] = 0.45
            weights[-1] = 0.45
            for i in range(1, n - 1):
                weights[i] = 0.1 / (n - 2)
            
            return [random.choices(candidates, weights=weights)[0] for _ in range(n_voters)]
        
        return [random.choice(candidates) for _ in range(n_voters)]
    
    @staticmethod
    def generate_ballots_ranked(n_voters: int, 
                                  candidates: List[str],
                                  distribution: str = 'uniform',
                                  seed: Optional[int] = None) -> List[List[str]]:
        """
        生成排序投票的模拟选票
        
        Args:
            n_voters: 选民数量
            candidates: 候选人列表
            distribution: 分布类型
            seed: 随机种子
            
        Returns:
            选票列表（每张选票是排序后的候选人列表）
        """
        if seed is not None:
            random.seed(seed)
        
        ballots = []
        n = len(candidates)
        
        for _ in range(n_voters):
            if distribution == 'uniform':
                ballot = candidates.copy()
                random.shuffle(ballot)
            
            elif distribution == 'normal':
                # 中心候选人倾向于排在前面
                weights = [1.0] * n
                mid = n // 2
                for i in range(n):
                    weights[i] = 1.0 / (abs(i - mid) + 0.5)
                total = sum(weights)
                weights = [w / total for w in weights]
                
                ballot = []
                remaining = candidates.copy()
                remaining_weights = weights.copy()
                
                while remaining:
                    chosen = random.choices(remaining, weights=remaining_weights)[0]
                    ballot.append(chosen)
                    idx = remaining.index(chosen)
                    remaining.pop(idx)
                    remaining_weights.pop(idx)
            
            elif distribution == 'polarized':
                # 两极化：前半部分选民偏好第一候选人，后半部分偏好最后候选人
                ballot = candidates.copy()
                if random.random() < 0.5:
                    ballot.sort()  # 按名称排序，使第一个靠前
                else:
                    ballot.sort(reverse=True)
            
            else:
                ballot = candidates.copy()
                random.shuffle(ballot)
            
            ballots.append(ballot)
        
        return ballots
    
    @staticmethod
    def generate_ballots_score(n_voters: int, 
                                 candidates: List[str],
                                 max_score: int = 10,
                                 distribution: str = 'uniform',
                                 seed: Optional[int] = None) -> List[Dict[str, int]]:
        """
        生成评分投票的模拟选票
        
        Args:
            n_voters: 选民数量
            candidates: 候选人列表
            max_score: 最高分
            distribution: 分布类型
            seed: 随机种子
            
        Returns:
            选票列表（每张选票是 {候选人: 分数} 的字典）
        """
        if seed is not None:
            random.seed(seed)
        
        ballots = []
        
        for _ in range(n_voters):
            ballot = {}
            for c in candidates:
                if distribution == 'uniform':
                    ballot[c] = random.randint(0, max_score)
                elif distribution == 'normal':
                    # 中间分数更常见
                    score = int(random.gauss(max_score / 2, max_score / 4))
                    ballot[c] = max(0, min(max_score, score))
                elif distribution == 'polarized':
                    # 倾向于给极端分数
                    if random.random() < 0.5:
                        ballot[c] = random.randint(0, max_score // 3)
                    else:
                        ballot[c] = random.randint(2 * max_score // 3, max_score)
                else:
                    ballot[c] = random.randint(0, max_score)
            
            ballots.append(ballot)
        
        return ballots
    
    @staticmethod
    def compare_methods(ballots_plurality: List[str],
                        ballots_ranked: List[List[str]],
                        ballots_approval: List[List[str]],
                        ballots_score: List[Dict[str, int]],
                        candidates: List[str]) -> Dict[str, str]:
        """
        比较不同投票方法的结果
        
        Returns:
            各方法获胜者的字典
        """
        results = {}
        
        # 简单多数
        winner, counts = PluralityVoting.vote(ballots_plurality)
        results['plurality'] = winner
        
        # 排序选择
        winner, rounds = RankedChoiceVoting.vote(ballots_ranked, candidates)
        results['ranked_choice'] = winner
        
        # 波达计数
        winner, scores, _ = BordaCount.vote(ballots_ranked, candidates)
        results['borda'] = winner
        
        # 批准投票
        winner, approvals = ApprovalVoting.vote(ballots_approval, candidates)
        results['approval'] = winner
        
        # 孔多塞
        winner, prefs, ranking = CondorcetVoting.vote(ballots_ranked, candidates)
        results['condorcet'] = winner
        
        # 评分投票
        winner, totals, avg = ScoreVoting.vote(ballots_score, 10, candidates)
        results['score'] = winner
        
        return results


# 便捷函数
def plurality(ballots: List[str]) -> str:
    """简单多数投票"""
    winner, _ = PluralityVoting.vote(ballots)
    return winner


def ranked_choice(ballots: List[List[str]], candidates: Optional[List[str]] = None) -> str:
    """排序选择投票"""
    winner, _ = RankedChoiceVoting.vote(ballots, candidates)
    return winner


def borda(ballots: List[List[str]], candidates: Optional[List[str]] = None) -> str:
    """波达计数"""
    winner, _, _ = BordaCount.vote(ballots, candidates)
    return winner


def approval(ballots: List[List[str]], candidates: Optional[List[str]] = None) -> str:
    """批准投票"""
    winner, _ = ApprovalVoting.vote(ballots, candidates)
    return winner


def condorcet(ballots: List[List[str]], candidates: Optional[List[str]] = None) -> str:
    """孔多塞投票"""
    winner, _, _ = CondorcetVoting.vote(ballots, candidates)
    return winner


def stv(ballots: List[List[str]], seats: int, candidates: Optional[List[str]] = None) -> List[str]:
    """单记可转移投票"""
    winners, _ = SingleTransferableVote.vote(ballots, seats, candidates)
    return winners


def score(ballots: List[Dict[str, int]], candidates: Optional[List[str]] = None) -> str:
    """评分投票"""
    winner, _, _ = ScoreVoting.vote(ballots, 10, candidates)
    return winner


if __name__ == '__main__':
    # 简单演示
    print("=== 投票工具演示 ===\n")
    
    candidates = ['Alice', 'Bob', 'Charlie', 'David']
    
    # 简单多数
    print("简单多数投票:")
    plurality_ballots = ['Alice', 'Bob', 'Alice', 'Charlie', 'Alice', 'Bob', 'David']
    winner, counts = PluralityVoting.vote(plurality_ballots)
    print(f"  选票: {plurality_ballots}")
    print(f"  结果: {winner} 获胜，得票: {counts}")
    
    print("\n排序选择投票:")
    ranked_ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Bob', 'Charlie', 'Alice'],
        ['Charlie', 'Alice', 'Bob'],
        ['Alice', 'Charlie', 'Bob'],
        ['Bob', 'Alice', 'Charlie'],
    ]
    winner, rounds = RankedChoiceVoting.vote(ranked_ballots)
    print(f"  获胜者: {winner}")
    print(f"  轮次: {len(rounds)}")
    
    print("\n波达计数:")
    winner, scores, _ = BordaCount.vote(ranked_ballots, candidates)
    print(f"  获胜者: {winner}")
    print(f"  得分: {scores}")
    
    print("\n批准投票:")
    approval_ballots = [
        ['Alice', 'Bob'],
        ['Bob', 'Charlie'],
        ['Alice', 'Charlie', 'David'],
        ['Bob', 'Alice'],
    ]
    winner, approvals = ApprovalVoting.vote(approval_ballots, candidates)
    print(f"  获胜者: {winner}")
    print(f"  批准数: {approvals}")
    
    print("\n孔多塞投票:")
    winner, prefs, ranking = CondorcetVoting.vote(ranked_ballots, candidates)
    print(f"  获胜者: {winner}")
    print(f"  排名: {ranking}")
    
    print("\n评分投票:")
    score_ballots = [
        {'Alice': 9, 'Bob': 7, 'Charlie': 5},
        {'Alice': 8, 'Bob': 8, 'Charlie': 6},
        {'Alice': 6, 'Bob': 9, 'Charlie': 7},
    ]
    winner, totals, avg = ScoreVoting.vote(score_ballots)
    print(f"  获胜者: {winner}")
    print(f"  总分: {totals}")
    print(f"  平均分: {avg}")
    
    print("\nSTV多席位:")
    stv_ballots = [
        ['Alice', 'Bob', 'Charlie'],
        ['Alice', 'Charlie', 'Bob'],
        ['Bob', 'Alice', 'Charlie'],
        ['Bob', 'Charlie', 'Alice'],
        ['Charlie', 'Alice', 'Bob'],
        ['Charlie', 'Bob', 'Alice'],
        ['David', 'Alice', 'Bob'],
    ]
    winners, stats = SingleTransferableVote.vote(stv_ballots, seats=2)
    print(f"  当选者: {winners}")
    print(f"  配额: {stats['quota']}")