"""
Tournament Utilities - 锦标赛赛程生成器

功能:
- 单败淘汰赛 (Single Elimination)
- 双败淘汰赛 (Double Elimination)
- 循环赛 (Round Robin)
- 瑞士制 (Swiss System)
- 种子选手处理
- 轮空处理
- 赛程可视化

零外部依赖，纯 Python 实现。
"""

import math
import random
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy


class MatchStatus(Enum):
    """比赛状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BYE = "bye"  # 轮空


@dataclass
class Participant:
    """参赛者"""
    id: int
    name: str
    seed: Optional[int] = None  # 种子排名
    rating: Optional[int] = None  # 评级/分数

    def __repr__(self):
        if self.seed:
            return f"[{self.seed}] {self.name}"
        return self.name


@dataclass
class Match:
    """比赛"""
    id: int
    round_num: int
    position: int  # 在该轮中的位置
    participant1: Optional[Participant] = None
    participant2: Optional[Participant] = None
    winner: Optional[Participant] = None
    loser: Optional[Participant] = None
    score1: Optional[int] = None
    score2: Optional[int] = None
    status: MatchStatus = MatchStatus.PENDING
    next_match_id: Optional[int] = None  # 胜者进入的下一场比赛
    next_match_slot: Optional[int] = None  # 进入下一场比赛的位置 (1 or 2)
    prev_match1_id: Optional[int] = None  # 前一场比赛1
    prev_match2_id: Optional[int] = None  # 前一场比赛2

    def __repr__(self):
        p1 = self.participant1.name if self.participant1 else "TBD"
        p2 = self.participant2.name if self.participant2 else "TBD"
        if self.status == MatchStatus.BYE:
            return f"轮空: {p1}"
        if self.status == MatchStatus.COMPLETED:
            return f"{p1} vs {p2} -> Winner: {self.winner.name if self.winner else 'N/A'}"
        return f"{p1} vs {p2}"


def _next_power_of_two(n: int) -> int:
    """计算大于等于n的最小2的幂"""
    if n <= 1:
        return 1
    return 2 ** math.ceil(math.log2(n))


def _get_seed_positions(bracket_size: int) -> List[int]:
    """获取种子位置序列，确保高种子选手分开"""
    if bracket_size == 1:
        return [0]
    if bracket_size == 2:
        return [0, 1]

    def generate(n):
        if n == 1:
            return [0]
        half = generate(n // 2)
        return half + [h + n // 2 for h in half]

    return generate(bracket_size)


class SingleElimination:
    """单败淘汰赛"""

    def __init__(self, participants: List[Participant]):
        self.participants = participants
        self.matches: Dict[int, Match] = {}
        self.num_rounds = 0
        self.generate_bracket()

    def generate_bracket(self):
        """生成淘汰赛对阵表"""
        n = len(self.participants)
        if n < 2:
            raise ValueError("至少需要2名参赛者")

        # 按 seed 排序参赛者
        sorted_p = sorted(self.participants, key=lambda p: (p.seed is None, p.seed or 0))

        # 计算 bracket 大小
        bracket_size = _next_power_of_two(n)
        self.num_rounds = math.ceil(math.log2(bracket_size))

        match_id = 0

        # 生成所有轮次的比赛
        round_matches = []

        # 第一轮
        first_round_matches = []
        num_first_round_matches = bracket_size // 2

        for i in range(num_first_round_matches):
            match = Match(
                id=match_id,
                round_num=1,
                position=i
            )
            first_round_matches.append(match)
            match_id += 1

        round_matches.append(first_round_matches)

        # 后续轮次
        for r in range(2, self.num_rounds + 1):
            matches_in_round = []
            num_matches = bracket_size // (2 ** r)
            for i in range(num_matches):
                match = Match(
                    id=match_id,
                    round_num=r,
                    position=i
                )
                matches_in_round.append(match)
                match_id += 1
            round_matches.append(matches_in_round)

        # 连接比赛关系
        for r, matches in enumerate(round_matches):
            if r == 0:  # 第一轮
                continue
            for i, match in enumerate(matches):
                prev1 = round_matches[r - 1][i * 2]
                prev2 = round_matches[r - 1][i * 2 + 1]
                match.prev_match1_id = prev1.id
                match.prev_match2_id = prev2.id
                prev1.next_match_id = match.id
                prev1.next_match_slot = 1
                prev2.next_match_id = match.id
                prev2.next_match_slot = 2

        # 使用标准种子分配算法
        seed_order = _get_seed_positions(bracket_size)

        # 将参赛者按种子顺序分配到 bracket 位置
        bracket_positions = [None] * bracket_size
        for i, p in enumerate(sorted_p):
            pos = seed_order[i]
            bracket_positions[pos] = p

        # 分配参赛者到第一轮比赛
        for i, match in enumerate(first_round_matches):
            pos1 = i * 2
            pos2 = i * 2 + 1

            match.participant1 = bracket_positions[pos1]
            match.participant2 = bracket_positions[pos2]

            # 处理轮空
            if match.participant1 and not match.participant2:
                match.status = MatchStatus.BYE
                match.winner = match.participant1
                if match.next_match_id is not None:
                    self._advance_winner(match)
            elif not match.participant1 and match.participant2:
                match.status = MatchStatus.BYE
                match.winner = match.participant2
                if match.next_match_id is not None:
                    next_match = self.matches.get(match.next_match_id)
                    if next_match:
                        if match.next_match_slot == 1:
                            next_match.participant1 = match.winner
                        else:
                            next_match.participant2 = match.winner
            elif not match.participant1 and not match.participant2:
                match.status = MatchStatus.BYE

        # 保存所有比赛
        for matches in round_matches:
            for m in matches:
                self.matches[m.id] = m

    def _advance_winner(self, match: Match):
        """晋级胜者到下一轮"""
        if match.next_match_id is None or match.winner is None:
            return

        next_match = self.matches.get(match.next_match_id)
        if next_match:
            if match.next_match_slot == 1:
                next_match.participant1 = match.winner
            else:
                next_match.participant2 = match.winner

    def set_winner(self, match_id: int, winner_id: int) -> Optional[Match]:
        """设置比赛胜者"""
        match = self.matches.get(match_id)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        if match.status == MatchStatus.BYE:
            raise ValueError("轮空比赛不能设置胜者")

        winner = None
        if match.participant1 and match.participant1.id == winner_id:
            winner = match.participant1
        elif match.participant2 and match.participant2.id == winner_id:
            winner = match.participant2
        else:
            raise ValueError(f"参赛者ID {winner_id} 不在此比赛中")

        match.winner = winner
        match.loser = match.participant2 if winner == match.participant1 else match.participant1
        match.status = MatchStatus.COMPLETED

        self._advance_winner(match)

        return self.matches.get(match.next_match_id) if match.next_match_id else None

    def set_score(self, match_id: int, score1: int, score2: int):
        """设置比赛比分"""
        match = self.matches.get(match_id)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        match.score1 = score1
        match.score2 = score2

        if score1 > score2:
            self.set_winner(match_id, match.participant1.id)
        elif score2 > score1:
            self.set_winner(match_id, match.participant2.id)

    def get_round_matches(self, round_num: int) -> List[Match]:
        """获取某一轮的所有比赛"""
        return [m for m in self.matches.values() if m.round_num == round_num]

    def get_current_round(self) -> int:
        """获取当前进行中的轮次"""
        for r in range(1, self.num_rounds + 1):
            matches = self.get_round_matches(r)
            pending = [m for m in matches if m.status in (MatchStatus.PENDING, MatchStatus.IN_PROGRESS)]
            if pending:
                return r
        return self.num_rounds

    def is_completed(self) -> bool:
        """锦标赛是否完成"""
        final_match = self.get_round_matches(self.num_rounds)
        return final_match and final_match[0].status == MatchStatus.COMPLETED

    def get_winner(self) -> Optional[Participant]:
        """获取锦标赛冠军"""
        if not self.is_completed():
            return None
        final_match = self.get_round_matches(self.num_rounds)[0]
        return final_match.winner

    def get_standings(self) -> List[Participant]:
        """获取最终排名（简化版）"""
        if not self.is_completed():
            return []

        standings = []
        winner = self.get_winner()
        if winner:
            standings.append(winner)

        final_match = self.get_round_matches(self.num_rounds)[0]
        if final_match.loser:
            standings.append(final_match.loser)

        remaining = [p for p in self.participants if p not in standings]
        remaining.sort(key=lambda p: (p.seed is None, p.seed or float('inf')))
        standings.extend(remaining)

        return standings

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": "single_elimination",
            "num_rounds": self.num_rounds,
            "participants": [{"id": p.id, "name": p.name, "seed": p.seed} for p in self.participants],
            "matches": [
                {
                    "id": m.id,
                    "round": m.round_num,
                    "position": m.position,
                    "participant1": m.participant1.name if m.participant1 else None,
                    "participant2": m.participant2.name if m.participant2 else None,
                    "winner": m.winner.name if m.winner else None,
                    "score": [m.score1, m.score2] if m.score1 is not None else None,
                    "status": m.status.value
                }
                for m in sorted(self.matches.values(), key=lambda x: (x.round_num, x.position))
            ],
            "completed": self.is_completed(),
            "champion": self.get_winner().name if self.is_completed() else None
        }

    def visualize(self) -> str:
        """可视化对阵表"""
        lines = []
        lines.append("🏆 单败淘汰赛对阵表")
        lines.append("=" * 50)

        for r in range(1, self.num_rounds + 1):
            round_names = {1: "第一轮", 2: "第二轮", 3: "八强", 4: "半决赛", 5: "决赛"}
            round_name = round_names.get(r, f"第{r}轮")
            if r == self.num_rounds:
                round_name = "🏅 决赛"
            elif r == self.num_rounds - 1:
                round_name = "⚔️ 半决赛"

            lines.append(f"\n{round_name}")
            lines.append("-" * 30)

            matches = sorted(self.get_round_matches(r), key=lambda x: x.position)
            for m in matches:
                if m.status == MatchStatus.BYE:
                    lines.append(f"  📍 轮空: {m.participant1.name if m.participant1 else 'TBD'}")
                elif m.status == MatchStatus.COMPLETED:
                    s1 = f"({m.score1})" if m.score1 is not None else ""
                    s2 = f"({m.score2})" if m.score2 is not None else ""
                    winner_mark = "👑" if m.round_num == self.num_rounds else "✓"
                    lines.append(f"  {m.participant1.name if m.participant1 else 'TBD'}{s1} vs {m.participant2.name if m.participant2 else 'TBD'}{s2} -> {winner_mark} {m.winner.name if m.winner else 'N/A'}")
                else:
                    lines.append(f"  ⏳ {m.participant1.name if m.participant1 else 'TBD'} vs {m.participant2.name if m.participant2 else 'TBD'}")

        if self.is_completed():
            lines.append(f"\n🏆 冠军: {self.get_winner().name}")

        return "\n".join(lines)


class DoubleElimination:
    """双败淘汰赛 - 胜者组和败者组"""

    def __init__(self, participants: List[Participant]):
        self.participants = participants
        self.winners_bracket: Dict[int, Match] = {}
        self.losers_bracket: Dict[int, Match] = {}
        self.grand_final: Optional[Match] = None
        self.grand_final_reset: Optional[Match] = None
        self.num_rounds = 0
        self.losers_rounds = 0
        self.generate_bracket()

    def generate_bracket(self):
        """生成双败淘汰赛对阵表"""
        n = len(self.participants)
        if n < 2:
            raise ValueError("至少需要2名参赛者")

        # 种子排序
        sorted_p = sorted(self.participants, key=lambda p: (p.seed is None, p.seed or 0))
        bracket_size = _next_power_of_two(n)
        positions = _get_seed_positions(bracket_size)[:n]
        seeded = [None] * n
        for i, p in enumerate(sorted_p):
            seeded[positions[i]] = p

        self.num_rounds = math.ceil(math.log2(bracket_size))
        self.losers_rounds = self.num_rounds * 2 - 2

        self._generate_winners_bracket(seeded)
        self._generate_losers_bracket()
        self._generate_grand_final()

    def _generate_winners_bracket(self, seeded: List[Participant]):
        """生成胜者组"""
        n = len(seeded)
        bracket_size = _next_power_of_two(n)

        match_id = 0
        round_matches = []

        # 第一轮
        first_round = []
        for i in range(bracket_size // 2):
            match = Match(id=match_id, round_num=1, position=i)
            first_round.append(match)
            match_id += 1
        round_matches.append(first_round)

        # 后续轮次
        for r in range(2, self.num_rounds + 1):
            matches = []
            num_matches = bracket_size // (2 ** r)
            for i in range(num_matches):
                match = Match(id=match_id, round_num=r, position=i)
                matches.append(match)
                match_id += 1
            round_matches.append(matches)

        # 连接关系
        for r in range(1, len(round_matches)):
            for i, match in enumerate(round_matches[r]):
                prev1 = round_matches[r - 1][i * 2]
                prev2 = round_matches[r - 1][i * 2 + 1]
                match.prev_match1_id = prev1.id
                match.prev_match2_id = prev2.id
                prev1.next_match_id = match.id
                prev2.next_match_id = match.id

        # 分配参赛者
        for i, match in enumerate(first_round):
            p1_idx = i * 2
            p2_idx = i * 2 + 1
            if p1_idx < n:
                match.participant1 = seeded[p1_idx]
            if p2_idx < n:
                match.participant2 = seeded[p2_idx]

            if match.participant1 and not match.participant2:
                match.status = MatchStatus.BYE
                match.winner = match.participant1

        for matches in round_matches:
            for m in matches:
                self.winners_bracket[m.id] = m

    def _generate_losers_bracket(self):
        """生成败者组"""
        match_id = 1000
        num_losers_matches = len(self.participants) - 2
        current_match_id = match_id
        round_matches = []

        for r in range(1, self.losers_rounds + 1):
            num_in_round = max(1, num_losers_matches // (2 ** (r - 1)))
            matches = []
            for i in range(num_in_round):
                match = Match(id=current_match_id, round_num=r, position=i)
                matches.append(match)
                current_match_id += 1
            round_matches.append(matches)
            if num_in_round <= 1:
                break

        for matches in round_matches:
            for m in matches:
                self.losers_bracket[m.id] = m

    def _generate_grand_final(self):
        """生成总决赛"""
        winners_final = max(self.winners_bracket.values(), key=lambda m: m.round_num)
        losers_final = max(self.losers_bracket.values(), key=lambda m: m.round_num) if self.losers_bracket else None

        self.grand_final = Match(
            id=2000,
            round_num=self.num_rounds + 1,
            position=0
        )
        self.grand_final.prev_match1_id = winners_final.id
        if losers_final:
            self.grand_final.prev_match2_id = losers_final.id

    def set_winner_winner(self, match_id: int, winner_id: int):
        """设置胜者组比赛结果"""
        match = self.winners_bracket.get(match_id)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        winner = None
        loser = None
        if match.participant1 and match.participant1.id == winner_id:
            winner = match.participant1
            loser = match.participant2
        elif match.participant2 and match.participant2.id == winner_id:
            winner = match.participant2
            loser = match.participant1
        else:
            raise ValueError(f"参赛者ID {winner_id} 不在此比赛中")

        match.winner = winner
        match.loser = loser
        match.status = MatchStatus.COMPLETED

        if match.next_match_id:
            next_match = self.winners_bracket.get(match.next_match_id)
            if next_match:
                if not next_match.participant1:
                    next_match.participant1 = winner
                else:
                    next_match.participant2 = winner

        self._send_to_losers_bracket(match)

    def _send_to_losers_bracket(self, winners_match: Match):
        """将败者送入败者组"""
        if not winners_match.loser:
            return

        for match in sorted(self.losers_bracket.values(), key=lambda m: (m.round_num, m.position)):
            if not match.participant1:
                match.participant1 = winners_match.loser
                return
            elif not match.participant2:
                match.participant2 = winners_match.loser
                return

    def set_loser_winner(self, match_id: int, winner_id: int):
        """设置败者组比赛结果"""
        match = self.losers_bracket.get(match_id)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        winner = None
        if match.participant1 and match.participant1.id == winner_id:
            winner = match.participant1
        elif match.participant2 and match.participant2.id == winner_id:
            winner = match.participant2
        else:
            raise ValueError(f"参赛者ID {winner_id} 不在此比赛中")

        match.winner = winner
        match.status = MatchStatus.COMPLETED

        next_round_matches = [m for m in self.losers_bracket.values() if m.round_num == match.round_num + 1]
        if next_round_matches:
            for next_match in sorted(next_round_matches, key=lambda m: m.position):
                if not next_match.participant1:
                    next_match.participant1 = winner
                    return
                elif not next_match.participant2:
                    next_match.participant2 = winner
                    return
        else:
            self.grand_final.participant2 = winner

    def set_grand_final_winner(self, winner_id: int):
        """设置总决赛胜者"""
        winner = None
        if self.grand_final.participant1 and self.grand_final.participant1.id == winner_id:
            winner = self.grand_final.participant1
        elif self.grand_final.participant2 and self.grand_final.participant2.id == winner_id:
            winner = self.grand_final.participant2

        if not winner:
            raise ValueError(f"参赛者ID {winner_id} 不在总决赛中")

        self.grand_final.winner = winner
        self.grand_final.status = MatchStatus.COMPLETED

    def get_winner(self) -> Optional[Participant]:
        """获取冠军"""
        if self.grand_final and self.grand_final.status == MatchStatus.COMPLETED:
            return self.grand_final.winner
        return None

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": "double_elimination",
            "participants": [{"id": p.id, "name": p.name, "seed": p.seed} for p in self.participants],
            "winners_bracket": [
                {
                    "id": m.id,
                    "round": m.round_num,
                    "p1": m.participant1.name if m.participant1 else None,
                    "p2": m.participant2.name if m.participant2 else None,
                    "winner": m.winner.name if m.winner else None,
                    "status": m.status.value
                }
                for m in sorted(self.winners_bracket.values(), key=lambda x: (x.round_num, x.position))
            ],
            "losers_bracket": [
                {
                    "id": m.id,
                    "round": m.round_num,
                    "p1": m.participant1.name if m.participant1 else None,
                    "p2": m.participant2.name if m.participant2 else None,
                    "winner": m.winner.name if m.winner else None,
                    "status": m.status.value
                }
                for m in sorted(self.losers_bracket.values(), key=lambda x: (x.round_num, x.position))
            ],
            "grand_final": {
                "p1": self.grand_final.participant1.name if self.grand_final and self.grand_final.participant1 else None,
                "p2": self.grand_final.participant2.name if self.grand_final and self.grand_final.participant2 else None,
                "winner": self.grand_final.winner.name if self.grand_final and self.grand_final.winner else None
            },
            "champion": self.get_winner().name if self.get_winner() else None
        }

    def visualize(self) -> str:
        """可视化对阵表"""
        lines = []
        lines.append("🏆 双败淘汰赛对阵表")
        lines.append("=" * 50)

        lines.append("\n📈 胜者组")
        lines.append("-" * 30)
        for r in range(1, self.num_rounds + 1):
            matches = sorted([m for m in self.winners_bracket.values() if m.round_num == r], key=lambda x: x.position)
            if matches:
                lines.append(f"  第{r}轮:")
                for m in matches:
                    if m.status == MatchStatus.BYE:
                        lines.append(f"    📍 轮空: {m.participant1.name if m.participant1 else 'TBD'}")
                    elif m.status == MatchStatus.COMPLETED:
                        lines.append(f"    ✓ {m.participant1.name if m.participant1 else 'TBD'} vs {m.participant2.name if m.participant2 else 'TBD'} -> {m.winner.name if m.winner else 'N/A'}")
                    else:
                        lines.append(f"    ⏳ {m.participant1.name if m.participant1 else 'TBD'} vs {m.participant2.name if m.participant2 else 'TBD'}")

        lines.append("\n📉 败者组")
        lines.append("-" * 30)
        for match in sorted(self.losers_bracket.values(), key=lambda x: (x.round_num, x.position)):
            if match.participant1 or match.participant2:
                p1 = match.participant1.name if match.participant1 else "TBD"
                p2 = match.participant2.name if match.participant2 else "TBD"
                w = f" -> {match.winner.name}" if match.winner else ""
                lines.append(f"  R{match.round_num}: {p1} vs {p2}{w}")

        lines.append("\n🏅 总决赛")
        lines.append("-" * 30)
        if self.grand_final:
            p1 = self.grand_final.participant1.name if self.grand_final.participant1 else "TBD"
            p2 = self.grand_final.participant2.name if self.grand_final.participant2 else "TBD"
            w = f" -> 🏆 {self.grand_final.winner.name}" if self.grand_final.winner else ""
            lines.append(f"  {p1} vs {p2}{w}")

        if self.get_winner():
            lines.append(f"\n🏆 冠军: {self.get_winner().name}")

        return "\n".join(lines)


class RoundRobin:
    """循环赛 - 每个人都与其他人对战"""

    def __init__(self, participants: List[Participant]):
        self.participants = participants
        self.matches: List[Match] = []
        self.standings: Dict[int, Dict[str, Any]] = {}
        self.generate_schedule()

    def generate_schedule(self):
        """生成循环赛赛程（圆圈算法）"""
        n = len(self.participants)
        if n < 2:
            raise ValueError("至少需要2名参赛者")

        for p in self.participants:
            self.standings[p.id] = {
                "participant": p,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "points": 0,
                "matches_played": 0
            }

        participants = list(self.participants)
        dummy = None
        if n % 2 == 1:
            dummy = Participant(id=-1, name="BYE")
            participants.append(dummy)
            n = len(participants)

        mid = n // 2
        match_id = 0

        for round_num in range(n - 1):
            for i in range(mid):
                p1 = participants[i]
                p2 = participants[n - 1 - i]

                if p1.id == -1 or p2.id == -1:
                    continue

                match = Match(
                    id=match_id,
                    round_num=round_num + 1,
                    position=i,
                    participant1=p1,
                    participant2=p2
                )
                self.matches.append(match)
                match_id += 1

            participants = [participants[0]] + [participants[-1]] + participants[1:-1]

        self.matches.sort(key=lambda m: (m.round_num, m.position))

    def set_result(self, match_id: int, score1: int, score2: int, draw: bool = False):
        """设置比赛结果"""
        match = next((m for m in self.matches if m.id == match_id), None)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        match.score1 = score1
        match.score2 = score2
        match.status = MatchStatus.COMPLETED

        if draw:
            match.winner = None
            match.loser = None
            self.standings[match.participant1.id]["draws"] += 1
            self.standings[match.participant2.id]["draws"] += 1
            self.standings[match.participant1.id]["points"] += 1
            self.standings[match.participant2.id]["points"] += 1
        elif score1 > score2:
            match.winner = match.participant1
            match.loser = match.participant2
            self.standings[match.participant1.id]["wins"] += 1
            self.standings[match.participant2.id]["losses"] += 1
            self.standings[match.participant1.id]["points"] += 3
        else:
            match.winner = match.participant2
            match.loser = match.participant1
            self.standings[match.participant2.id]["wins"] += 1
            self.standings[match.participant1.id]["losses"] += 1
            self.standings[match.participant2.id]["points"] += 3

        self.standings[match.participant1.id]["matches_played"] += 1
        self.standings[match.participant2.id]["matches_played"] += 1

    def get_standings(self) -> List[Dict]:
        """获取积分榜"""
        standings_list = list(self.standings.values())
        standings_list.sort(key=lambda x: (-x["points"], -x["wins"], x["losses"]))
        return standings_list

    def get_round_matches(self, round_num: int) -> List[Match]:
        """获取某一轮的比赛"""
        return [m for m in self.matches if m.round_num == round_num]

    def is_completed(self) -> bool:
        """是否完成所有比赛"""
        return all(m.status == MatchStatus.COMPLETED for m in self.matches)

    def get_winner(self) -> Optional[Participant]:
        """获取冠军"""
        if not self.is_completed():
            return None
        standings = self.get_standings()
        return standings[0]["participant"] if standings else None

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": "round_robin",
            "participants": [{"id": p.id, "name": p.name} for p in self.participants],
            "matches": [
                {
                    "id": m.id,
                    "round": m.round_num,
                    "p1": m.participant1.name,
                    "p2": m.participant2.name,
                    "score": [m.score1, m.score2] if m.score1 is not None else None,
                    "winner": m.winner.name if m.winner else None,
                    "status": m.status.value
                }
                for m in self.matches
            ],
            "standings": self.get_standings(),
            "completed": self.is_completed(),
            "champion": self.get_winner().name if self.is_completed() else None
        }

    def visualize(self) -> str:
        """可视化"""
        lines = []
        lines.append("🏆 循环赛")
        lines.append("=" * 50)

        total_rounds = max(m.round_num for m in self.matches) if self.matches else 0

        for r in range(1, total_rounds + 1):
            lines.append(f"\n第{r}轮")
            lines.append("-" * 30)
            matches = self.get_round_matches(r)
            for m in matches:
                if m.status == MatchStatus.COMPLETED:
                    s = f"({m.score1}-{m.score2})"
                    lines.append(f"  ✓ {m.participant1.name} {s} {m.participant2.name}")
                else:
                    lines.append(f"  ⏳ {m.participant1.name} vs {m.participant2.name}")

        lines.append("\n📊 积分榜")
        lines.append("-" * 30)
        lines.append(f"{'排名':<4} {'选手':<15} {'胜':<4} {'负':<4} {'平':<4} {'积分':<4}")
        lines.append("-" * 40)

        for i, s in enumerate(self.get_standings(), 1):
            p = s["participant"]
            lines.append(f"{i:<4} {p.name:<15} {s['wins']:<4} {s['losses']:<4} {s['draws']:<4} {s['points']:<4}")

        if self.is_completed():
            lines.append(f"\n🏆 冠军: {self.get_winner().name}")

        return "\n".join(lines)


class SwissSystem:
    """瑞士制比赛 - 固定轮次，按积分配对"""

    def __init__(self, participants: List[Participant], num_rounds: int = None):
        self.participants = participants
        self.num_rounds = num_rounds or math.ceil(math.log2(len(participants)))
        self.current_round = 0
        self.matches: List[Match] = []
        self.standings: Dict[int, Dict[str, Any]] = {}
        self.pairing_history: Dict[int, set] = {}
        self.generate_initial_standings()

    def generate_initial_standings(self):
        """初始化积分榜"""
        for p in self.participants:
            self.standings[p.id] = {
                "participant": p,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "points": 0.0,
                "matches_played": 0,
                "opponents": [],
                "buchholz": 0.0
            }
            self.pairing_history[p.id] = set()

    def generate_round_pairings(self) -> List[Match]:
        """生成下一轮配对"""
        if self.current_round >= self.num_rounds:
            raise ValueError("所有轮次已完成")

        self.current_round += 1
        new_matches = []

        sorted_standings = sorted(
            self.standings.values(),
            key=lambda x: (-x["points"], -x["buchholz"])
        )

        paired = set()
        match_id = len(self.matches)

        for i, s1 in enumerate(sorted_standings):
            if s1["participant"].id in paired:
                continue

            p1 = s1["participant"]

            for j in range(i + 1, len(sorted_standings)):
                s2 = sorted_standings[j]
                p2 = s2["participant"]

                if p2.id in paired:
                    continue

                if p2.id in self.pairing_history[p1.id]:
                    continue

                match = Match(
                    id=match_id,
                    round_num=self.current_round,
                    position=len(new_matches),
                    participant1=p1,
                    participant2=p2
                )
                new_matches.append(match)

                self.pairing_history[p1.id].add(p2.id)
                self.pairing_history[p2.id].add(p1.id)

                paired.add(p1.id)
                paired.add(p2.id)
                match_id += 1
                break

        unpaired = [p for p in self.participants if p.id not in paired]
        if unpaired:
            p = unpaired[0]
            match = Match(
                id=match_id,
                round_num=self.current_round,
                position=len(new_matches),
                participant1=p,
                status=MatchStatus.BYE
            )
            match.winner = p
            new_matches.append(match)
            self.standings[p.id]["wins"] += 1
            self.standings[p.id]["points"] += 1.0

        self.matches.extend(new_matches)
        return new_matches

    def set_result(self, match_id: int, score1: float, score2: float):
        """设置比赛结果"""
        match = next((m for m in self.matches if m.id == match_id), None)
        if not match:
            raise ValueError(f"比赛ID {match_id} 不存在")

        if match.status == MatchStatus.BYE:
            return

        match.score1 = score1
        match.score2 = score2
        match.status = MatchStatus.COMPLETED

        p1, p2 = match.participant1, match.participant2

        if score1 > score2:
            match.winner = p1
            self.standings[p1.id]["wins"] += 1
            self.standings[p1.id]["points"] += 1.0
        elif score2 > score1:
            match.winner = p2
            self.standings[p2.id]["wins"] += 1
            self.standings[p2.id]["points"] += 1.0
        else:
            match.winner = None
            self.standings[p1.id]["draws"] += 1
            self.standings[p2.id]["draws"] += 1
            self.standings[p1.id]["points"] += 0.5
            self.standings[p2.id]["points"] += 0.5

        self.standings[p1.id]["matches_played"] += 1
        self.standings[p2.id]["matches_played"] += 1
        self.standings[p1.id]["opponents"].append(p2.id)
        self.standings[p2.id]["opponents"].append(p1.id)

        self._update_buchholz()

    def _update_buchholz(self):
        """更新 Buchholz 积分"""
        for p_id, s in self.standings.items():
            s["buchholz"] = sum(
                self.standings[opp_id]["points"]
                for opp_id in s["opponents"]
                if opp_id in self.standings
            )

    def get_current_round_matches(self) -> List[Match]:
        """获取当前轮次的比赛"""
        return [m for m in self.matches if m.round_num == self.current_round]

    def get_standings(self) -> List[Dict]:
        """获取积分榜"""
        standings_list = list(self.standings.values())
        standings_list.sort(key=lambda x: (-x["points"], -x["buchholz"]))
        return standings_list

    def is_completed(self) -> bool:
        """是否完成所有轮次"""
        if self.current_round < self.num_rounds:
            return False
        current_matches = self.get_current_round_matches()
        return all(m.status == MatchStatus.COMPLETED for m in current_matches)

    def get_winners(self, top_n: int = 1) -> List[Participant]:
        """获取前N名"""
        standings = self.get_standings()
        return [s["participant"] for s in standings[:top_n]]

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": "swiss",
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "participants": [{"id": p.id, "name": p.name} for p in self.participants],
            "matches": [
                {
                    "id": m.id,
                    "round": m.round_num,
                    "p1": m.participant1.name if m.participant1 else None,
                    "p2": m.participant2.name if m.participant2 else None,
                    "score": [m.score1, m.score2] if m.score1 is not None else None,
                    "winner": m.winner.name if m.winner else None,
                    "status": m.status.value
                }
                for m in self.matches
            ],
            "standings": [
                {
                    "rank": i + 1,
                    "name": s["participant"].name,
                    "wins": s["wins"],
                    "losses": s["losses"],
                    "draws": s["draws"],
                    "points": s["points"],
                    "buchholz": s["buchholz"]
                }
                for i, s in enumerate(self.get_standings())
            ],
            "completed": self.is_completed()
        }

    def visualize(self) -> str:
        """可视化"""
        lines = []
        lines.append(f"🏆 瑞士制比赛 (共{self.num_rounds}轮)")
        lines.append("=" * 50)

        for r in range(1, self.current_round + 1):
            lines.append(f"\n第{r}轮")
            lines.append("-" * 30)
            matches = [m for m in self.matches if m.round_num == r]
            for m in matches:
                if m.status == MatchStatus.BYE:
                    lines.append(f"  📍 轮空: {m.participant1.name if m.participant1 else 'TBD'}")
                elif m.status == MatchStatus.COMPLETED:
                    s = f"({m.score1}-{m.score2})"
                    w = f" -> {m.winner.name}" if m.winner else " -> 平局"
                    lines.append(f"  ✓ {m.participant1.name} {s} {m.participant2.name}{w}")
                else:
                    lines.append(f"  ⏳ {m.participant1.name} vs {m.participant2.name}")

        lines.append(f"\n📊 积分榜 (第{self.current_round}轮后)")
        lines.append("-" * 50)
        lines.append(f"{'排名':<4} {'选手':<12} {'胜':<4} {'负':<4} {'平':<4} {'积分':<6} {'BH':<6}")
        lines.append("-" * 50)

        for i, s in enumerate(self.get_standings()):
            p = s["participant"]
            lines.append(f"{i+1:<4} {p.name:<12} {s['wins']:<4} {s['losses']:<4} {s['draws']:<4} {s['points']:<6.1f} {s['buchholz']:<6.1f}")

        return "\n".join(lines)


# 便捷函数
def create_single_elimination(participants: List[str], seeds: List[int] = None) -> SingleElimination:
    """创建单败淘汰赛（简化版）"""
    p_list = []
    for i, name in enumerate(participants):
        seed = seeds[i] if seeds and i < len(seeds) else None
        p_list.append(Participant(id=i, name=name, seed=seed))
    return SingleElimination(p_list)


def create_double_elimination(participants: List[str], seeds: List[int] = None) -> DoubleElimination:
    """创建双败淘汰赛（简化版）"""
    p_list = []
    for i, name in enumerate(participants):
        seed = seeds[i] if seeds and i < len(seeds) else None
        p_list.append(Participant(id=i, name=name, seed=seed))
    return DoubleElimination(p_list)


def create_round_robin(participants: List[str]) -> RoundRobin:
    """创建循环赛（简化版）"""
    p_list = [Participant(id=i, name=name) for i, name in enumerate(participants)]
    return RoundRobin(p_list)


def create_swiss(participants: List[str], num_rounds: int = None) -> SwissSystem:
    """创建瑞士制比赛（简化版）"""
    p_list = [Participant(id=i, name=name) for i, name in enumerate(participants)]
    return SwissSystem(p_list, num_rounds)


if __name__ == "__main__":
    print("=" * 60)
    print("🏆 锦标赛工具演示")
    print("=" * 60)

    print("\n📌 单败淘汰赛")
    print("-" * 40)
    names = ["选手A", "选手B", "选手C", "选手D", "选手E", "选手F", "选手G", "选手H"]
    seeds = [1, 8, 4, 5, 3, 6, 2, 7]
    se = create_single_elimination(names, seeds)
    print(se.visualize())

    print("\n📌 循环赛")
    print("-" * 40)
    rr = create_round_robin(["张三", "李四", "王五", "赵六"])
    for match in rr.matches:
        rr.set_result(match.id, random.randint(0, 3), random.randint(0, 3))
    print(rr.visualize())

    print("\n📌 瑞士制")
    print("-" * 40)
    swiss = create_swiss(["棋手1", "棋手2", "棋手3", "棋手4", "棋手5", "棋手6"])
    for r in range(swiss.num_rounds):
        swiss.generate_round_pairings()
        for match in swiss.get_current_round_matches():
            if match.status != MatchStatus.BYE:
                swiss.set_result(match.id, random.randint(0, 1), random.randint(0, 1))
    print(swiss.visualize())