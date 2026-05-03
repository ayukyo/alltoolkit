"""
Elo Rating System - Elo 等级分系统工具模块

Elo 等级分系统是由 Arpad Elo 发明的评估选手实力的方法，广泛应用于：
- 国际象棋排名
- 竞技游戏匹配
- 体育比赛排名
- 在线对战系统

特点：
- 零外部依赖
- 支持经典 Elo 和改进版算法
- 支持团队 Elo 计算
- 支持匹配系统
- 支持等级分历史记录
- 支持性能统计

Author: AllToolkit
Date: 2026-05-03
"""

from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import math
from datetime import datetime


class KFactorStrategy(Enum):
    """K 因子策略"""
    CONSTANT = "constant"  # 固定值
    PROVISIONAL = "provisional"  # 新手高 K，老手低 K
    RATING_BASED = "rating_based"  # 基于等级分调整
    TIME_BASED = "time_based"  # 基于时间调整


@dataclass
class Player:
    """玩家数据类"""
    id: str
    rating: float = 1200.0
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    peak_rating: Optional[float] = None
    rating_history: List[Tuple[datetime, float]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.rating_history:
            self.rating_history = [(datetime.now(), self.rating)]
        if self.peak_rating is None:
            self.peak_rating = self.rating
    
    @property
    def win_rate(self) -> float:
        """胜率"""
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played
    
    @property
    def is_provisional(self) -> bool:
        """是否为新手（比赛场次不足）"""
        return self.games_played < 30
    
    def update_peak(self):
        """更新历史最高分"""
        if self.rating > self.peak_rating:
            self.peak_rating = self.rating


class EloRating:
    """
    Elo 等级分计算器
    
    Examples:
        >>> elo = EloRating()
        >>> player1 = Player("p1", rating=1500)
        >>> player2 = Player("p2", rating=1600)
        >>> new_ratings = elo.calculate_ratings(player1, player2, 1.0)
        >>> # player1 胜利
    """
    
    def __init__(
        self,
        k_factor: float = 32.0,
        k_strategy: KFactorStrategy = KFactorStrategy.PROVISIONAL,
        initial_rating: float = 1200.0,
        min_rating: float = 100.0,
        max_rating: float = 3000.0,
        draw_score: float = 0.5
    ):
        """
        初始化 Elo 计算器
        
        Args:
            k_factor: K 因子，决定每场比赛等级分变化的幅度
            k_strategy: K 因子策略
            initial_rating: 初始等级分
            min_rating: 最低等级分
            max_rating: 最高等级分
            draw_score: 平局得分 (0-1)
        """
        self.k_factor = k_factor
        self.k_strategy = k_strategy
        self.initial_rating = initial_rating
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.draw_score = draw_score
    
    def get_k_factor(self, player: Player) -> float:
        """
        根据策略计算玩家的 K 因子
        
        Args:
            player: 玩家对象
        
        Returns:
            K 因子值
        """
        if self.k_strategy == KFactorStrategy.CONSTANT:
            return self.k_factor
        
        elif self.k_strategy == KFactorStrategy.PROVISIONAL:
            # 新手高 K，老手低 K
            if player.games_played < 10:
                return 50.0
            elif player.games_played < 30:
                return 40.0
            else:
                return 20.0
        
        elif self.k_strategy == KFactorStrategy.RATING_BASED:
            # 高分段用低 K，低分段用高 K
            if player.rating < 1500:
                return 40.0
            elif player.rating < 2000:
                return 32.0
            elif player.rating < 2500:
                return 24.0
            else:
                return 16.0
        
        elif self.k_strategy == KFactorStrategy.TIME_BASED:
            # 根据活跃度调整（简化版：直接用场次）
            if player.games_played < 20:
                return 40.0
            else:
                return max(16.0, 32.0 - (player.games_played - 20) * 0.2)
        
        return self.k_factor
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """
        计算玩家 A 对玩家 B 的预期得分
        
        Args:
            rating_a: 玩家 A 的等级分
            rating_b: 玩家 B 的等级分
        
        Returns:
            预期得分 (0-1)
        
        Examples:
            >>> elo = EloRating()
            >>> elo.expected_score(1500, 1500)
            0.5
            >>> elo.expected_score(1600, 1400)
            0.76...
        """
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))
    
    def rating_change(
        self,
        player: Player,
        opponent_rating: float,
        actual_score: float
    ) -> float:
        """
        计算等级分变化
        
        Args:
            player: 玩家对象
            opponent_rating: 对手等级分
            actual_score: 实际得分 (0=负, 0.5=平, 1=胜)
        
        Returns:
            等级分变化值
        """
        k = self.get_k_factor(player)
        expected = self.expected_score(player.rating, opponent_rating)
        change = k * (actual_score - expected)
        return change
    
    def calculate_ratings(
        self,
        player1: Player,
        player2: Player,
        score1: float
    ) -> Tuple[float, float]:
        """
        计算比赛后两个玩家的新等级分
        
        Args:
            player1: 玩家1
            player2: 玩家2
            score1: 玩家1的得分 (0=负, 0.5=平, 1=胜)
        
        Returns:
            (新等级分1, 新等级分2)
        
        Examples:
            >>> elo = EloRating()
            >>> p1 = Player("p1", rating=1500)
            >>> p2 = Player("p2", rating=1600)
            >>> elo.calculate_ratings(p1, p2, 1.0)  # p1 胜
            (1512..., 1587...)
        """
        score2 = 1.0 - score1
        
        change1 = self.rating_change(player1, player2.rating, score1)
        change2 = self.rating_change(player2, player1.rating, score2)
        
        new_rating1 = self._clamp_rating(player1.rating + change1)
        new_rating2 = self._clamp_rating(player2.rating + change2)
        
        return (new_rating1, new_rating2)
    
    def _clamp_rating(self, rating: float) -> float:
        """限制等级分范围"""
        return max(self.min_rating, min(self.max_rating, rating))
    
    def update_players(
        self,
        player1: Player,
        player2: Player,
        score1: float
    ) -> None:
        """
        更新玩家数据（等级分、场次、胜负记录等）
        
        Args:
            player1: 玩家1
            player2: 玩家2
            score1: 玩家1的得分
        """
        new_rating1, new_rating2 = self.calculate_ratings(player1, player2, score1)
        
        # 更新玩家1
        player1.rating = new_rating1
        player1.games_played += 1
        player1.rating_history.append((datetime.now(), new_rating1))
        player1.update_peak()
        
        # 更新玩家2
        player2.rating = new_rating2
        player2.games_played += 1
        player2.rating_history.append((datetime.now(), new_rating2))
        player2.update_peak()
        
        # 更新胜负记录
        if score1 > self.draw_score:
            player1.wins += 1
            player2.losses += 1
        elif score1 < self.draw_score:
            player1.losses += 1
            player2.wins += 1
        else:
            player1.draws += 1
            player2.draws += 1
    
    def expected_score_range(self, rating: float, rating_range: float = 200) -> Dict[str, float]:
        """
        计算在给定等级分范围内的预期得分范围
        
        Args:
            rating: 玩家等级分
            rating_range: 等级分范围
        
        Returns:
            预期得分范围字典
        """
        return {
            "vs_lower": self.expected_score(rating, rating - rating_range),
            "vs_equal": 0.5,
            "vs_higher": self.expected_score(rating, rating + rating_range)
        }


class TeamElo:
    """
    团队 Elo 计算器
    
    用于团队比赛的等级分计算
    
    Examples:
        >>> team_elo = TeamElo()
        >>> team1 = [Player("a", 1500), Player("b", 1600)]
        >>> team2 = [Player("c", 1500), Player("d", 1400)]
        >>> team_elo.calculate_team_ratings(team1, team2, 1.0)
    """
    
    def __init__(self, k_factor: float = 32.0):
        self.k_factor = k_factor
    
    def team_rating(self, team: List[Player], method: str = "average") -> float:
        """
        计算团队等级分
        
        Args:
            team: 团队成员列表
            method: 计算方法
                - "average": 平均值
                - "sum": 总和
                - "weighted": 按场次加权
                - "best": 最高分
        
        Returns:
            团队等级分
        """
        if not team:
            return 1200.0
        
        ratings = [p.rating for p in team]
        
        if method == "average":
            return sum(ratings) / len(ratings)
        elif method == "sum":
            return sum(ratings)
        elif method == "weighted":
            weights = [max(1, p.games_played) for p in team]
            return sum(r * w for r, w in zip(ratings, weights)) / sum(weights)
        elif method == "best":
            return max(ratings)
        else:
            return sum(ratings) / len(ratings)
    
    def calculate_team_ratings(
        self,
        team1: List[Player],
        team2: List[Player],
        score1: float,
        method: str = "average"
    ) -> Tuple[List[float], List[float]]:
        """
        计算团队比赛后各成员的新等级分
        
        Args:
            team1: 队伍1
            team2: 队伍2
            score1: 队伍1得分
            method: 团队等级分计算方法
        
        Returns:
            (队伍1新等级分列表, 队伍2新等级分列表)
        """
        team1_rating = self.team_rating(team1, method)
        team2_rating = self.team_rating(team2, method)
        
        elo = EloRating(k_factor=self.k_factor)
        
        # 计算队伍预期得分
        expected1 = elo.expected_score(team1_rating, team2_rating)
        expected2 = 1.0 - expected1
        
        # 计算每个成员的等级分变化
        new_ratings1 = []
        new_ratings2 = []
        
        for player in team1:
            k = elo.get_k_factor(player)
            change = k * (score1 - expected1)
            new_rating = max(100, min(3000, player.rating + change))
            new_ratings1.append(new_rating)
        
        score2 = 1.0 - score1
        for player in team2:
            k = elo.get_k_factor(player)
            change = k * (score2 - expected2)
            new_rating = max(100, min(3000, player.rating + change))
            new_ratings2.append(new_rating)
        
        return (new_ratings1, new_ratings2)


class Matchmaking:
    """
    Elo 匹配系统
    
    根据等级分为玩家匹配实力相近的对手
    
    Examples:
        >>> mm = Matchmaking()
        >>> players = [Player(str(i), 1500 + i*10) for i in range(100)]
        >>> player = Player("target", 1600)
        >>> matches = mm.find_matches(player, players, max_rating_diff=200)
    """
    
    def __init__(
        self,
        max_rating_diff: float = 300.0,
        expansion_rate: float = 1.5,
        max_wait_factor: float = 3.0
    ):
        """
        初始化匹配系统
        
        Args:
            max_rating_diff: 最大等级分差
            expansion_rate: 搜索范围扩展速率
            max_wait_factor: 最大等待扩展因子
        """
        self.max_rating_diff = max_rating_diff
        self.expansion_rate = expansion_rate
        self.max_wait_factor = max_wait_factor
    
    def find_matches(
        self,
        player: Player,
        candidates: List[Player],
        max_rating_diff: Optional[float] = None,
        limit: int = 10,
        wait_time_seconds: float = 0.0
    ) -> List[Tuple[Player, float]]:
        """
        为玩家找到合适的对手
        
        Args:
            player: 待匹配玩家
            candidates: 候选玩家列表
            max_rating_diff: 最大等级分差（可选）
            limit: 返回数量限制
            wait_time_seconds: 等待时间（秒），用于扩展搜索范围
        
        Returns:
            [(对手, 匹配质量分数), ...] 按质量排序
        """
        if max_rating_diff is None:
            max_rating_diff = self.max_rating_diff
        
        # 根据等待时间扩展搜索范围
        expanded_diff = max_rating_diff * (1 + wait_time_seconds / 60 * self.expansion_rate)
        expanded_diff = min(expanded_diff, max_rating_diff * self.max_wait_factor)
        
        matches = []
        
        for candidate in candidates:
            if candidate.id == player.id:
                continue
            
            rating_diff = abs(player.rating - candidate.rating)
            
            if rating_diff <= expanded_diff:
                # 计算匹配质量分数 (0-1, 越高越好)
                quality = 1.0 - (rating_diff / expanded_diff)
                matches.append((candidate, quality))
        
        # 按匹配质量排序
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches[:limit]
    
    def balanced_teams(
        self,
        players: List[Player],
        team_size: int = 2
    ) -> Tuple[List[Player], List[Player], float]:
        """
        将玩家分成两个实力均衡的队伍
        
        Args:
            players: 玩家列表（数量必须为 team_size * 2）
            team_size: 每队人数
        
        Returns:
            (队伍1, 队伍2, 平衡分数)
        
        Raises:
            ValueError: 玩家数量不足
        """
        if len(players) < team_size * 2:
            raise ValueError(f"需要至少 {team_size * 2} 名玩家")
        
        # 按等级分排序
        sorted_players = sorted(players, key=lambda p: p.rating, reverse=True)
        
        # 贪心分配（交替选择）
        team1 = []
        team2 = []
        
        for i, player in enumerate(sorted_players[:team_size * 2]):
            if i % 2 == 0:
                team1.append(player)
            else:
                team2.append(player)
        
        # 计算平衡分数
        avg1 = sum(p.rating for p in team1) / len(team1)
        avg2 = sum(p.rating for p in team2) / len(team2)
        balance_score = 1.0 - abs(avg1 - avg2) / max(avg1, avg2)
        
        return (team1, team2, balance_score)
    
    def best_match(self, player: Player, candidates: List[Player]) -> Optional[Player]:
        """
        找到最佳匹配对手
        
        Args:
            player: 待匹配玩家
            candidates: 候选玩家列表
        
        Returns:
            最佳对手，如果没有合适对手则返回 None
        """
        matches = self.find_matches(player, candidates, limit=1)
        if matches:
            return matches[0][0]
        return None


class RatingCalculator:
    """
    通用等级分计算器
    
    支持多种等级分系统的计算和转换
    """
    
    # 常见等级分系统的映射
    RATING_SYSTEMS = {
        "elo": {"mean": 1200, "scale": 400},
        "glicko": {"mean": 1500, "scale": 173.7},
        "chess_com": {"mean": 1500, "scale": 400},
        "lichess": {"mean": 1500, "scale": 400},
    }
    
    @classmethod
    def convert_rating(
        cls,
        rating: float,
        from_system: str,
        to_system: str
    ) -> float:
        """
        转换不同等级分系统的分数
        
        Args:
            rating: 原始等级分
            from_system: 原系统名称
            to_system: 目标系统名称
        
        Returns:
            转换后的等级分
        """
        from_params = cls.RATING_SYSTEMS.get(from_system.lower(), {"mean": 1200, "scale": 400})
        to_params = cls.RATING_SYSTEMS.get(to_system.lower(), {"mean": 1200, "scale": 400})
        
        # 标准化到统一尺度
        normalized = (rating - from_params["mean"]) / from_params["scale"]
        
        # 转换到目标尺度
        return normalized * to_params["scale"] + to_params["mean"]
    
    @classmethod
    def percentile(cls, rating: float, system: str = "elo") -> float:
        """
        计算等级分对应的百分位
        
        Args:
            rating: 等级分
            system: 系统名称
        
        Returns:
            百分位 (0-100)
        """
        params = cls.RATING_SYSTEMS.get(system.lower(), {"mean": 1200, "scale": 400})
        
        # 使用正态分布近似
        z_score = (rating - params["mean"]) / params["scale"]
        percentile = 0.5 * (1 + math.erf(z_score / math.sqrt(2)))
        
        return percentile * 100
    
    @classmethod
    def rating_for_percentile(cls, percentile: float, system: str = "elo") -> float:
        """
        计算给定百分位对应的等级分
        
        Args:
            percentile: 百分位 (0-100)
            system: 系统名称
        
        Returns:
            等级分
        """
        params = cls.RATING_SYSTEMS.get(system.lower(), {"mean": 1200, "scale": 400})
        
        percentile = max(0.001, min(99.999, percentile)) / 100
        
        # 使用近似公式计算逆误差函数（避免依赖 scipy）
        def erfinv_approx(x: float) -> float:
            """近似逆误差函数"""
            if abs(x) >= 1:
                return float('inf') if x > 0 else float('-inf')
            
            sign = 1 if x >= 0 else -1
            x_abs = abs(x)
            
            # Winitzki 近似公式
            a = 0.147
            ln_term = math.log(1 - x_abs * x_abs)
            first = 2 / (math.pi * a) + ln_term / 2
            second = ln_term / a
            result = sign * math.sqrt(math.sqrt(first * first - second) - first)
            
            return result
        
        z_score = math.sqrt(2) * erfinv_approx(2 * percentile - 1)
        
        return z_score * params["scale"] + params["mean"]
    
    @classmethod
    def classify_rating(cls, rating: float, system: str = "elo") -> str:
        """
        等级分分类
        
        Args:
            rating: 等级分
            system: 系统名称
        
        Returns:
            分类名称
        """
        params = cls.RATING_SYSTEMS.get(system.lower(), {"mean": 1200, "scale": 400})
        mean = params["mean"]
        
        if rating < mean - 400:
            return "初学者"
        elif rating < mean - 200:
            return "新手"
        elif rating < mean + 200:
            return "普通"
        elif rating < mean + 400:
            return "熟练"
        elif rating < mean + 600:
            return "高手"
        elif rating < mean + 800:
            return "专家"
        else:
            return "大师"


class Leaderboard:
    """
    Elo 排行榜
    
    管理玩家排名和统计数据
    
    Examples:
        >>> lb = Leaderboard()
        >>> lb.add_player(Player("p1", 1800))
        >>> lb.add_player(Player("p2", 1500))
        >>> lb.get_rank("p1")
        1
    """
    
    def __init__(self, name: str = "Leaderboard"):
        self.name = name
        self.players: Dict[str, Player] = {}
    
    def add_player(self, player: Player) -> None:
        """添加玩家"""
        self.players[player.id] = player
    
    def remove_player(self, player_id: str) -> Optional[Player]:
        """移除玩家"""
        return self.players.pop(player_id, None)
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """获取玩家"""
        return self.players.get(player_id)
    
    def get_rank(self, player_id: str) -> Optional[int]:
        """
        获取玩家排名
        
        Args:
            player_id: 玩家ID
        
        Returns:
            排名（1为最高），如果玩家不存在则返回 None
        """
        if player_id not in self.players:
            return None
        
        player_rating = self.players[player_id].rating
        rank = 1
        
        for p in self.players.values():
            if p.rating > player_rating:
                rank += 1
        
        return rank
    
    def get_top_players(self, n: int = 10) -> List[Player]:
        """
        获取前 N 名玩家
        
        Args:
            n: 数量
        
        Returns:
            玩家列表（按等级分降序）
        """
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.rating,
            reverse=True
        )
        return sorted_players[:n]
    
    def get_nearby_players(
        self,
        player_id: str,
        range_size: int = 5
    ) -> List[Tuple[int, Player]]:
        """
        获取玩家附近的排名玩家
        
        Args:
            player_id: 玩家ID
            range_size: 上下范围数量
        
        Returns:
            [(排名, 玩家), ...]
        """
        if player_id not in self.players:
            return []
        
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.rating,
            reverse=True
        )
        
        # 找到目标玩家的位置
        target_idx = None
        for i, p in enumerate(sorted_players):
            if p.id == player_id:
                target_idx = i
                break
        
        if target_idx is None:
            return []
        
        # 获取附近玩家
        start = max(0, target_idx - range_size)
        end = min(len(sorted_players), target_idx + range_size + 1)
        
        return [(i + 1, sorted_players[i]) for i in range(start, end)]
    
    def get_statistics(self) -> Dict:
        """
        获取排行榜统计信息
        
        Returns:
            统计字典
        """
        if not self.players:
            return {
                "player_count": 0,
                "average_rating": 0,
                "highest_rating": 0,
                "lowest_rating": 0,
                "total_games": 0
            }
        
        ratings = [p.rating for p in self.players.values()]
        games = [p.games_played for p in self.players.values()]
        
        return {
            "player_count": len(self.players),
            "average_rating": sum(ratings) / len(ratings),
            "highest_rating": max(ratings),
            "lowest_rating": min(ratings),
            "total_games": sum(games),
            "median_rating": sorted(ratings)[len(ratings) // 2]
        }
    
    def export_rankings(self) -> List[Dict]:
        """
        导出排名数据
        
        Returns:
            排名数据列表
        """
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.rating,
            reverse=True
        )
        
        return [
            {
                "rank": i + 1,
                "id": p.id,
                "rating": p.rating,
                "games": p.games_played,
                "wins": p.wins,
                "losses": p.losses,
                "draws": p.draws,
                "win_rate": p.win_rate,
                "peak_rating": p.peak_rating
            }
            for i, p in enumerate(sorted_players)
        ]


# 辅助函数
def elo_diff_to_probability(rating_diff: float) -> float:
    """
    将等级分差转换为获胜概率
    
    Args:
        rating_diff: 等级分差（玩家A - 玩家B）
    
    Returns:
        玩家A的获胜概率
    
    Examples:
        >>> elo_diff_to_probability(0)
        0.5
        >>> elo_diff_to_probability(400)
        0.909...
    """
    return 1.0 / (1.0 + 10 ** (-rating_diff / 400.0))


def probability_to_elo_diff(probability: float) -> float:
    """
    将获胜概率转换为等级分差
    
    Args:
        probability: 获胜概率 (0-1)
    
    Returns:
        等级分差
    
    Examples:
        >>> probability_to_elo_diff(0.5)
        0.0
        >>> probability_to_elo_diff(0.9)
        381.9...
    """
    probability = max(0.001, min(0.999, probability))
    return -400 * math.log10((1 - probability) / probability)


def rating_to_title(rating: float, system: str = "chess") -> str:
    """
    将等级分转换为头衔
    
    Args:
        rating: 等级分
        system: 系统名称
    
    Returns:
        头衔名称
    """
    titles = {
        "chess": [
            (2700, "特级大师 (GM)"),
            (2500, "国际大师 (IM)"),
            (2400, "国际棋联大师 (FM)"),
            (2300, "候选大师 (CM)"),
            (2200, "专家"),
            (2000, "高手"),
            (1800, "熟练"),
            (1600, "普通"),
            (1400, "新手"),
            (0, "初学者")
        ]
    }
    
    system_titles = titles.get(system, titles["chess"])
    
    for threshold, title in system_titles:
        if rating >= threshold:
            return title
    
    return "初学者"