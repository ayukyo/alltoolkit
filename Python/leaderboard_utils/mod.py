"""
Leaderboard Utils - 排行榜工具模块

排行榜管理系统，支持：
- 多种排名方式（密集排名、竞争排名、顺序排名、分数排名）
- 平局处理与决胜规则
- 分页查询
- 历史记录追踪
- 统计分析
- 实时更新

特点：
- 零外部依赖
- 线程安全的操作
- 支持大数据量优化
- 灵活的排序规则

Author: AllToolkit
Date: 2026-05-30
"""

from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import heapq
from collections import defaultdict
import re


def _parse_iso_datetime(s: str) -> datetime:
    """解析 ISO 格式 datetime字符串（兼容 Python 3.6）"""
    if not s:
        return datetime.now()
    
    # 尝试直接解析
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        pass
    
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        pass
    
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        pass
    
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
    
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        pass
    
    return datetime.now()


class RankingMethod(Enum):
    """排名方式"""
    DENSE = "dense"              # 密集排名：1, 2, 2, 3（无间隙）
    COMPETITION = "competition"  # 竞争排名：1, 2, 2, 4（有间隙）
    ORDINAL = "ordinal"          # 顺序排名：1, 2, 3, 4（无平局）
    FRACTIONAL = "fractional"    # 分数排名：1, 2.5, 2.5, 4（平均排名）


class SortOrder(Enum):
    """排序顺序"""
    DESC = "desc"  # 降序（默认，高分在前）
    ASC = "asc"    # 升序


@dataclass
class TieBreakRule:
    """平局决胜规则"""
    field: str                    # 决胜字段名
    order: SortOrder = SortOrder.DESC  # 排序方向
    
    def compare(self, a: Any, b: Any) -> int:
        """比较两个值，返回 -1, 0, 1"""
        val_a = a.get(self.field) if isinstance(a, dict) else getattr(a, self.field, None)
        val_b = b.get(self.field) if isinstance(b, dict) else getattr(b, self.field, None)
        
        if val_a is None and val_b is None:
            return 0
        if val_a is None:
            return 1
        if val_b is None:
            return -1
            
        if val_a < val_b:
            return 1 if self.order == SortOrder.DESC else -1
        elif val_a > val_b:
            return -1 if self.order == SortOrder.DESC else 1
        return 0


@dataclass
class LeaderboardEntry:
    """排行榜条目"""
    id: str                                    # 唯一标识
    name: str                                  # 显示名称
    score: float                               # 分数
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据
    timestamp: datetime = field(default_factory=datetime.now)  # 更新时间
    previous_rank: Optional[int] = None       # 上次排名
    rank_change: Optional[int] = None         # 排名变化（正数上升，负数下降）
    score_history: List[Tuple[datetime, float]] = field(default_factory=list)  # 分数历史
    
    def __post_init__(self):
        if not self.score_history:
            self.score_history = [(self.timestamp, self.score)]
    
    def update_score(self, new_score: float, timestamp: Optional[datetime] = None):
        """更新分数"""
        self.score = new_score
        self.timestamp = timestamp or datetime.now()
        self.score_history.append((self.timestamp, new_score))
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "previous_rank": self.previous_rank,
            "rank_change": self.rank_change
        }


@dataclass
class RankedEntry:
    """已排名的条目"""
    entry: LeaderboardEntry
    rank: int
    tied: bool = False
    tied_count: int = 0


@dataclass
class LeaderboardStats:
    """排行榜统计信息"""
    total_entries: int
    total_score: float
    average_score: float
    max_score: float
    min_score: float
    median_score: float
    std_dev: float
    score_distribution: Dict[str, int]  # 分数区间分布
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_entries": self.total_entries,
            "total_score": self.total_score,
            "average_score": self.average_score,
            "max_score": self.max_score,
            "min_score": self.min_score,
            "median_score": self.median_score,
            "std_dev": self.std_dev,
            "score_distribution": self.score_distribution
        }


class Leaderboard:
    """
    排行榜管理器
    
    支持多种排名方式和灵活的排序规则。
    
    Examples:
        >>> lb = Leaderboard("游戏排行榜")
        >>> lb.add_entry("p1", "玩家1", 100)
        >>> lb.add_entry("p2", "玩家2", 150)
        >>> top = lb.get_top(10)
        >>> rank = lb.get_rank("p1")
    """
    
    def __init__(
        self,
        name: str = "Leaderboard",
        ranking_method: RankingMethod = RankingMethod.DENSE,
        sort_order: SortOrder = SortOrder.DESC,
        tie_break_rules: Optional[List[TieBreakRule]] = None,
        max_entries: Optional[int] = None,
        keep_history: bool = True
    ):
        """
        初始化排行榜
        
        Args:
            name: 排行榜名称
            ranking_method: 排名方式
            sort_order: 排序顺序
            tie_break_rules: 平局决胜规则列表
            max_entries: 最大条目数（None 表示无限制）
            keep_history: 是否保留历史记录
        """
        self.name = name
        self.ranking_method = ranking_method
        self.sort_order = sort_order
        self.tie_break_rules = tie_break_rules or []
        self.max_entries = max_entries
        self.keep_history = keep_history
        
        self._entries: Dict[str, LeaderboardEntry] = {}
        self._cached_ranking: Optional[List[RankedEntry]] = None
        self._dirty = True
        self._history: List[Tuple[datetime, Dict[str, Any]]] = []
    
    def add_entry(
        self,
        entry_id: str,
        name: str,
        score: float,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ) -> LeaderboardEntry:
        """
        添加或更新条目
        
        Args:
            entry_id: 条目唯一标识
            name: 显示名称
            score: 分数
            metadata: 额外元数据
            timestamp: 时间戳
            
        Returns:
            创建或更新的条目
        """
        if entry_id in self._entries:
            entry = self._entries[entry_id]
            entry.name = name
            entry.update_score(score, timestamp)
            if metadata:
                entry.metadata.update(metadata)
        else:
            entry = LeaderboardEntry(
                id=entry_id,
                name=name,
                score=score,
                metadata=metadata or {},
                timestamp=timestamp or datetime.now()
            )
            self._entries[entry_id] = entry
        
        self._dirty = True
        return entry
    
    def update_score(
        self,
        entry_id: str,
        new_score: float,
        timestamp: Optional[datetime] = None
    ) -> Optional[LeaderboardEntry]:
        """
        更新条目分数
        
        Args:
            entry_id: 条目ID
            new_score: 新分数
            timestamp: 时间戳
            
        Returns:
            更新的条目，如果不存在则返回 None
        """
        if entry_id not in self._entries:
            return None
        
        entry = self._entries[entry_id]
        entry.update_score(new_score, timestamp)
        self._dirty = True
        return entry
    
    def increment_score(
        self,
        entry_id: str,
        delta: float,
        timestamp: Optional[datetime] = None
    ) -> Optional[LeaderboardEntry]:
        """
        增量更新分数
        
        Args:
            entry_id: 条目ID
            delta: 分数增量
            timestamp: 时间戳
            
        Returns:
            更新的条目
        """
        if entry_id not in self._entries:
            return None
        
        entry = self._entries[entry_id]
        return self.update_score(entry_id, entry.score + delta, timestamp)
    
    def remove_entry(self, entry_id: str) -> bool:
        """
        移除条目
        
        Args:
            entry_id: 条目ID
            
        Returns:
            是否成功移除
        """
        if entry_id in self._entries:
            del self._entries[entry_id]
            self._dirty = True
            return True
        return False
    
    def get_entry(self, entry_id: str) -> Optional[LeaderboardEntry]:
        """获取条目"""
        return self._entries.get(entry_id)
    
    def _rebuild_ranking(self) -> List[RankedEntry]:
        """重建排名缓存"""
        entries = list(self._entries.values())
        
        # 记录旧排名
        old_ranks = {}
        if self._cached_ranking:
            for re in self._cached_ranking:
                old_ranks[re.entry.id] = re.rank
        
        # 排序
        sorted_entries = self._sort_entries(entries)
        
        # 计算排名
        ranked = self._assign_ranks(sorted_entries, old_ranks)
        
        self._cached_ranking = ranked
        self._dirty = False
        
        # 保存历史快照
        if self.keep_history:
            snapshot = {
                "timestamp": datetime.now().isoformat(),
                "entries": [(e.entry.id, e.entry.score, e.rank) for e in ranked]
            }
            self._history.append((datetime.now(), snapshot))
        
        return ranked
    
    def _sort_entries(self, entries: List[LeaderboardEntry]) -> List[LeaderboardEntry]:
        """排序条目"""
        def compare_key(entry: LeaderboardEntry):
            # 主排序键：分数
            key = [-entry.score if self.sort_order == SortOrder.DESC else entry.score]
            
            # 决胜规则
            for rule in self.tie_break_rules:
                val = entry.metadata.get(rule.field) if rule.field in entry.metadata else None
                if val is None:
                    val = float('inf') if rule.order == SortOrder.ASC else float('-inf')
                elif rule.order == SortOrder.DESC:
                    if isinstance(val, (int, float)):
                        key.append(-val)
                    else:
                        key.append(val)
                else:
                    key.append(val if isinstance(val, (int, float)) else 0)
            
            # 最终决胜：时间（先达到者优先）
            key.append(entry.timestamp)
            
            return tuple(key)
        
        return sorted(entries, key=compare_key)
    
    def _assign_ranks(
        self,
        sorted_entries: List[LeaderboardEntry],
        old_ranks: Dict[str, int]
    ) -> List[RankedEntry]:
        """分配排名"""
        if not sorted_entries:
            return []
        
        result = []
        
        if self.ranking_method == RankingMethod.ORDINAL:
            # 顺序排名：无平局
            for i, entry in enumerate(sorted_entries, 1):
                entry.previous_rank = old_ranks.get(entry.id)
                entry.rank_change = (entry.previous_rank - i) if entry.previous_rank else None
                result.append(RankedEntry(entry=entry, rank=i, tied=False, tied_count=0))
        
        elif self.ranking_method == RankingMethod.DENSE:
            # 密集排名：1, 2, 2, 3（无间隙）
            rank = 1
            i = 0
            while i < len(sorted_entries):
                # 找到相同分数的组
                j = i
                while j < len(sorted_entries) and sorted_entries[j].score == sorted_entries[i].score:
                    j += 1
                
                tied_count = j - i
                for k in range(i, j):
                    entry = sorted_entries[k]
                    entry.previous_rank = old_ranks.get(entry.id)
                    entry.rank_change = (entry.previous_rank - rank) if entry.previous_rank else None
                    result.append(RankedEntry(
                        entry=entry,
                        rank=rank,
                        tied=tied_count > 1,
                        tied_count=tied_count
                    ))
                rank += 1
                i = j
        
        elif self.ranking_method == RankingMethod.COMPETITION:
            # 竞争排名：1, 2, 2, 4（有间隙）
            i = 0
            position = 1
            while i < len(sorted_entries):
                # 找到相同分数的组
                j = i
                while j < len(sorted_entries) and sorted_entries[j].score == sorted_entries[i].score:
                    j += 1
                
                tied_count = j - i
                for k in range(i, j):
                    entry = sorted_entries[k]
                    entry.previous_rank = old_ranks.get(entry.id)
                    entry.rank_change = (entry.previous_rank - position) if entry.previous_rank else None
                    result.append(RankedEntry(
                        entry=entry,
                        rank=position,
                        tied=tied_count > 1,
                        tied_count=tied_count
                    ))
                position += tied_count
                i = j
        
        elif self.ranking_method == RankingMethod.FRACTIONAL:
            # 分数排名：1, 2.5, 2.5, 4（平均排名）
            i = 0
            while i < len(sorted_entries):
                # 找到相同分数的组
                j = i
                while j < len(sorted_entries) and sorted_entries[j].score == sorted_entries[i].score:
                    j += 1
                
                # 计算平均排名
                avg_rank = sum(range(i + 1, j + 1)) / (j - i)
                tied_count = j - i
                
                for k in range(i, j):
                    entry = sorted_entries[k]
                    entry.previous_rank = old_ranks.get(entry.id)
                    entry.rank_change = (entry.previous_rank - avg_rank) if entry.previous_rank else None
                    result.append(RankedEntry(
                        entry=entry,
                        rank=avg_rank,
                        tied=tied_count > 1,
                        tied_count=tied_count
                    ))
                i = j
        
        return result
    
    def get_ranking(self, force_refresh: bool = False) -> List[RankedEntry]:
        """
        获取完整排名列表
        
        Args:
            force_refresh: 是否强制刷新缓存
            
        Returns:
            排名列表
        """
        if self._dirty or force_refresh or self._cached_ranking is None:
            return self._rebuild_ranking()
        return self._cached_ranking
    
    def get_top(self, n: int = 10) -> List[RankedEntry]:
        """
        获取前 N 名
        
        Args:
            n: 数量
            
        Returns:
            排名列表
        """
        ranking = self.get_ranking()
        return ranking[:n]
    
    def get_bottom(self, n: int = 10) -> List[RankedEntry]:
        """
        获取后 N 名
        
        Args:
            n: 数量
            
        Returns:
            排名列表
        """
        ranking = self.get_ranking()
        return ranking[-n:] if n < len(ranking) else ranking
    
    def get_rank(self, entry_id: str) -> Optional[int]:
        """
        获取条目排名
        
        Args:
            entry_id: 条目ID
            
        Returns:
            排名（1-indexed），不存在则返回 None
        """
        ranking = self.get_ranking()
        for re in ranking:
            if re.entry.id == entry_id:
                return int(re.rank) if isinstance(re.rank, int) else re.rank
        return None
    
    def get_ranked_entry(self, entry_id: str) -> Optional[RankedEntry]:
        """获取带排名信息的条目"""
        ranking = self.get_ranking()
        for re in ranking:
            if re.entry.id == entry_id:
                return re
        return None
    
    def get_page(
        self,
        page: int,
        per_page: int = 10
    ) -> Tuple[List[RankedEntry], int, int]:
        """
        分页获取排名
        
        Args:
            page: 页码（1-indexed）
            per_page: 每页数量
            
        Returns:
            (当前页数据, 总页数, 总条目数)
        """
        ranking = self.get_ranking()
        total = len(ranking)
        total_pages = (total + per_page - 1) // per_page if total > 0 else 0
        
        start = (page - 1) * per_page
        end = start + per_page
        
        return ranking[start:end], total_pages, total
    
    def get_around(
        self,
        entry_id: str,
        radius: int = 5
    ) -> List[RankedEntry]:
        """
        获取某条目周围的排名
        
        Args:
            entry_id: 条目ID
            radius: 前后各取的数量
            
        Returns:
            排名列表
        """
        ranking = self.get_ranking()
        
        for i, re in enumerate(ranking):
            if re.entry.id == entry_id:
                start = max(0, i - radius)
                end = min(len(ranking), i + radius + 1)
                return ranking[start:end]
        
        return []
    
    def get_stats(self) -> LeaderboardStats:
        """
        获取统计信息
        
        Returns:
            统计信息对象
        """
        entries = list(self._entries.values())
        
        if not entries:
            return LeaderboardStats(
                total_entries=0,
                total_score=0,
                average_score=0,
                max_score=0,
                min_score=0,
                median_score=0,
                std_dev=0,
                score_distribution={}
            )
        
        scores = [e.score for e in entries]
        total = sum(scores)
        avg = total / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # 中位数
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        median = sorted_scores[n // 2] if n % 2 else (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
        
        # 标准差
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # 分数分布（按区间）
        if max_score > min_score:
            range_size = (max_score - min_score) / 5
            distribution = defaultdict(int)
            for s in scores:
                bucket = int((s - min_score) / range_size) if range_size > 0 else 0
                bucket = min(bucket, 4)  # 确保 max_score 落入最后一个桶
                label = f"{min_score + bucket * range_size:.0f}-{min_score + (bucket + 1) * range_size:.0f}"
                distribution[label] += 1
        else:
            distribution = {f"{min_score:.0f}": len(scores)}
        
        return LeaderboardStats(
            total_entries=len(entries),
            total_score=total,
            average_score=avg,
            max_score=max_score,
            min_score=min_score,
            median_score=median,
            std_dev=std_dev,
            score_distribution=dict(distribution)
        )
    
    def get_score_rank(self, score: float) -> int:
        """
        获取某分数的排名（即使该分数没有条目）
        
        Args:
            score: 分数
            
        Returns:
            排名
        """
        ranking = self.get_ranking()
        
        count = 0
        for re in ranking:
            if self.sort_order == SortOrder.DESC:
                if re.entry.score > score:
                    count += 1
                else:
                    break
            else:
                if re.entry.score < score:
                    count += 1
                else:
                    break
        
        return count + 1
    
    def get_entries_by_score(self, score: float) -> List[LeaderboardEntry]:
        """获取指定分数的所有条目"""
        return [e for e in self._entries.values() if e.score == score]
    
    def search(
        self,
        query: str,
        field: str = "name",
        limit: int = 10
    ) -> List[RankedEntry]:
        """
        搜索条目
        
        Args:
            query: 搜索关键词
            field: 搜索字段（name 或 metadata 中的字段）
            limit: 最大结果数
            
        Returns:
            匹配的排名条目
        """
        ranking = self.get_ranking()
        results = []
        query_lower = query.lower()
        
        for re in ranking:
            if field == "name":
                if query_lower in re.entry.name.lower():
                    results.append(re)
            elif field in re.entry.metadata:
                if query_lower in str(re.entry.metadata[field]).lower():
                    results.append(re)
            
            if len(results) >= limit:
                break
        
        return results
    
    def count(self) -> int:
        """获取条目总数"""
        return len(self._entries)
    
    def clear(self):
        """清空排行榜"""
        self._entries.clear()
        self._cached_ranking = None
        self._dirty = True
        self._history.clear()
    
    def get_history(self, limit: int = 10) -> List[Tuple[datetime, Dict[str, Any]]]:
        """获取历史快照"""
        return self._history[-limit:]
    
    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return {
            "name": self.name,
            "ranking_method": self.ranking_method.value,
            "sort_order": self.sort_order.value,
            "entries": [e.to_dict() for e in self._entries.values()],
            "stats": self.get_stats().to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Leaderboard':
        """从字典创建"""
        lb = cls(
            name=data.get("name", "Leaderboard"),
            ranking_method=RankingMethod(data.get("ranking_method", "dense")),
            sort_order=SortOrder(data.get("sort_order", "desc"))
        )
        
        for entry_data in data.get("entries", []):
            entry = LeaderboardEntry(
                id=entry_data["id"],
                name=entry_data["name"],
                score=entry_data["score"],
                metadata=entry_data.get("metadata", {}),
                timestamp=_parse_iso_datetime(entry_data["timestamp"]) if entry_data.get("timestamp") else datetime.now()
            )
            lb._entries[entry.id] = entry
        
        return lb


class MultiLeaderboard:
    """
    多排行榜管理器
    
    管理多个命名排行榜。
    
    Examples:
        >>> mlb = MultiLeaderboard()
        >>> mlb.create("daily", "每日排行榜")
        >>> mlb.add_entry("daily", "p1", "玩家1", 100)
    """
    
    def __init__(self):
        self._leaderboards: Dict[str, Leaderboard] = {}
    
    def create(
        self,
        key: str,
        name: str = "",
        ranking_method: RankingMethod = RankingMethod.DENSE,
        sort_order: SortOrder = SortOrder.DESC,
        **kwargs
    ) -> Leaderboard:
        """
        创建排行榜
        
        Args:
            key: 排行榜唯一键
            name: 排行榜名称
            ranking_method: 排名方式
            sort_order: 排序顺序
            **kwargs: 其他参数
            
        Returns:
            创建的排行榜
        """
        lb = Leaderboard(
            name=name or key,
            ranking_method=ranking_method,
            sort_order=sort_order,
            **kwargs
        )
        self._leaderboards[key] = lb
        return lb
    
    def get(self, key: str) -> Optional[Leaderboard]:
        """获取排行榜"""
        return self._leaderboards.get(key)
    
    def delete(self, key: str) -> bool:
        """删除排行榜"""
        if key in self._leaderboards:
            del self._leaderboards[key]
            return True
        return False
    
    def list(self) -> List[str]:
        """列出所有排行榜键"""
        return list(self._leaderboards.keys())
    
    def add_entry(
        self,
        leaderboard_key: str,
        entry_id: str,
        name: str,
        score: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[LeaderboardEntry]:
        """向指定排行榜添加条目"""
        lb = self.get(leaderboard_key)
        if lb:
            return lb.add_entry(entry_id, name, score, metadata)
        return None
    
    def get_top_across(
        self,
        n: int = 10,
        keys: Optional[List[str]] = None
    ) -> List[Tuple[str, RankedEntry]]:
        """
        跨排行榜获取前 N 名
        
        Args:
            n: 数量
            keys: 要查询的排行榜键列表（None 表示全部）
            
        Returns:
            (排行榜键, 排名条目) 元组列表
        """
        keys = keys or list(self._leaderboards.keys())
        all_entries = []
        
        for key in keys:
            lb = self._leaderboards.get(key)
            if lb:
                for re in lb.get_top(n):
                    all_entries.append((key, re))
        
        # 按分数排序
        reverse = True  # 默认降序
        all_entries.sort(key=lambda x: x[1].entry.score, reverse=reverse)
        
        return all_entries[:n]


class LeaderboardBuilder:
    """
    排行榜构建器
    
    流式 API 构建排行榜。
    
    Examples:
        >>> lb = (LeaderboardBuilder("游戏排行榜")
        ...     .with_ranking_method(RankingMethod.DENSE)
        ...     .with_sort_order(SortOrder.DESC)
        ...     .add_tie_breaker("level", SortOrder.DESC)
        ...     .build())
    """
    
    def __init__(self, name: str = "Leaderboard"):
        self._name = name
        self._ranking_method = RankingMethod.DENSE
        self._sort_order = SortOrder.DESC
        self._tie_break_rules: List[TieBreakRule] = []
        self._max_entries: Optional[int] = None
        self._keep_history = True
    
    def with_ranking_method(self, method: RankingMethod) -> 'LeaderboardBuilder':
        """设置排名方式"""
        self._ranking_method = method
        return self
    
    def with_sort_order(self, order: SortOrder) -> 'LeaderboardBuilder':
        """设置排序顺序"""
        self._sort_order = order
        return self
    
    def add_tie_breaker(self, field: str, order: SortOrder = SortOrder.DESC) -> 'LeaderboardBuilder':
        """添加决胜规则"""
        self._tie_break_rules.append(TieBreakRule(field=field, order=order))
        return self
    
    def with_max_entries(self, max_entries: int) -> 'LeaderboardBuilder':
        """设置最大条目数"""
        self._max_entries = max_entries
        return self
    
    def with_history(self, keep: bool = True) -> 'LeaderboardBuilder':
        """设置是否保留历史"""
        self._keep_history = keep
        return self
    
    def build(self) -> Leaderboard:
        """构建排行榜"""
        return Leaderboard(
            name=self._name,
            ranking_method=self._ranking_method,
            sort_order=self._sort_order,
            tie_break_rules=self._tie_break_rules,
            max_entries=self._max_entries,
            keep_history=self._keep_history
        )


# 便捷函数
def create_leaderboard(
    name: str = "Leaderboard",
    method: str = "dense",
    descending: bool = True
) -> Leaderboard:
    """
    快速创建排行榜
    
    Args:
        name: 排行榜名称
        method: 排名方式（"dense", "competition", "ordinal", "fractional"）
        descending: 是否降序
        
    Returns:
        排行榜实例
    """
    method_map = {
        "dense": RankingMethod.DENSE,
        "competition": RankingMethod.COMPETITION,
        "ordinal": RankingMethod.ORDINAL,
        "fractional": RankingMethod.FRACTIONAL
    }
    
    return Leaderboard(
        name=name,
        ranking_method=method_map.get(method, RankingMethod.DENSE),
        sort_order=SortOrder.DESC if descending else SortOrder.ASC
    )