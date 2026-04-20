"""
转移矩阵工具
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple
import math


class TransitionMatrix:
    """
    马尔可夫链转移矩阵
    
    提供转移矩阵的构建、查询和矩阵运算
    
    Examples:
        >>> tm = TransitionMatrix()
        >>> tm.add_transition('A', 'B')
        >>> tm.add_transition('A', 'C')
        >>> tm.add_transition('B', 'A')
        >>> tm.get_probability('A', 'B')
        0.5
    """
    
    def __init__(self):
        """初始化转移矩阵"""
        self._counts: Dict[Any, Dict[Any, int]] = defaultdict(lambda: defaultdict(int))
        self._row_totals: Dict[Any, int] = defaultdict(int)
        self._states: set = set()
    
    def add_transition(
        self, 
        from_state: Any, 
        to_state: Any, 
        count: int = 1
    ) -> 'TransitionMatrix':
        """
        添加转移
        
        Args:
            from_state: 源状态
            to_state: 目标状态
            count: 转移次数
            
        Returns:
            self
        """
        self._counts[from_state][to_state] += count
        self._row_totals[from_state] += count
        self._states.add(from_state)
        self._states.add(to_state)
        return self
    
    def add_sequence(self, sequence: List[Any]) -> 'TransitionMatrix':
        """
        从序列添加转移
        
        Args:
            sequence: 状态序列
            
        Returns:
            self
        """
        for i in range(len(sequence) - 1):
            self.add_transition(sequence[i], sequence[i + 1])
        return self
    
    def get_count(self, from_state: Any, to_state: Any) -> int:
        """
        获取转移次数
        
        Args:
            from_state: 源状态
            to_state: 目标状态
            
        Returns:
            转移次数
        """
        return self._counts[from_state][to_state]
    
    def get_probability(self, from_state: Any, to_state: Any) -> float:
        """
        获取转移概率
        
        Args:
            from_state: 源状态
            to_state: 目标状态
            
        Returns:
            转移概率
        """
        total = self._row_totals[from_state]
        if total == 0:
            return 0.0
        return self._counts[from_state][to_state] / total
    
    def get_row(self, from_state: Any) -> Dict[Any, float]:
        """
        获取某状态的所有转移概率
        
        Args:
            from_state: 源状态
            
        Returns:
            {目标状态: 概率} 字典
        """
        total = self._row_totals[from_state]
        if total == 0:
            return {}
        
        return {
            to_state: count / total
            for to_state, count in self._counts[from_state].items()
        }
    
    def get_row_counts(self, from_state: Any) -> Dict[Any, int]:
        """
        获取某状态的所有转移次数
        
        Args:
            from_state: 源状态
            
        Returns:
            {目标状态: 次数} 字典
        """
        return dict(self._counts[from_state])
    
    def get_most_likely(self, from_state: Any) -> Optional[Tuple[Any, float]]:
        """
        获取最可能的转移
        
        Args:
            from_state: 源状态
            
        Returns:
            (目标状态, 概率) 或 None
        """
        if from_state not in self._counts:
            return None
        
        row = self._counts[from_state]
        if not row:
            return None
        
        total = self._row_totals[from_state]
        best_state = max(row.keys(), key=lambda s: row[s])
        
        return best_state, row[best_state] / total
    
    def get_top_transitions(
        self, 
        from_state: Any, 
        top_n: int = 5
    ) -> List[Tuple[Any, float]]:
        """
        获取前 N 个最可能的转移
        
        Args:
            from_state: 源状态
            top_n: 数量
            
        Returns:
            [(目标状态, 概率), ...] 列表
        """
        row = self.get_row(from_state)
        if not row:
            return []
        
        return sorted(row.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def get_stationary_distribution(
        self, 
        iterations: int = 100,
        tolerance: float = 1e-6
    ) -> Dict[Any, float]:
        """
        计算稳态分布（幂迭代法）
        
        Args:
            iterations: 最大迭代次数
            tolerance: 收敛阈值
            
        Returns:
            {状态: 稳态概率} 字典
        """
        if not self._states:
            return {}
        
        # 初始均匀分布
        states = list(self._states)
        n = len(states)
        state_idx = {s: i for i, s in enumerate(states)}
        
        # 初始概率向量
        pi = [1.0 / n] * n
        
        for _ in range(iterations):
            new_pi = [0.0] * n
            
            for from_state in states:
                from_idx = state_idx[from_state]
                row = self.get_row(from_state)
                
                if not row:
                    # 如果没有出边，保持在原状态
                    new_pi[from_idx] += pi[from_idx]
                else:
                    for to_state, prob in row.items():
                        to_idx = state_idx[to_state]
                        new_pi[to_idx] += pi[from_idx] * prob
            
            # 检查收敛
            diff = sum(abs(new_pi[i] - pi[i]) for i in range(n))
            pi = new_pi
            
            if diff < tolerance:
                break
        
        return {states[i]: pi[i] for i in range(n)}
    
    def is_irreducible(self) -> bool:
        """
        检查是否不可约（任意状态可达任意其他状态）
        
        Returns:
            是否不可约
        """
        if not self._states:
            return True
        
        states = list(self._states)
        
        # 对每个状态，检查能否到达所有其他状态
        for start in states:
            reachable = {start}
            frontier = [start]
            
            while frontier:
                current = frontier.pop(0)
                row = self._counts[current]
                
                for next_state in row:
                    if next_state not in reachable:
                        reachable.add(next_state)
                        frontier.append(next_state)
            
            if reachable != self._states:
                return False
        
        return True
    
    def get_absorbing_states(self) -> set:
        """
        获取吸收态（一旦进入就无法离开的状态）
        
        Returns:
            吸收态集合
        """
        absorbing = set()
        
        for state in self._states:
            # 只有自环或没有出边
            row = self._counts[state]
            if not row:
                absorbing.add(state)
            elif len(row) == 1 and state in row:
                absorbing.add(state)
        
        return absorbing
    
    def get_transient_states(self) -> set:
        """
        获取瞬态（非吸收态）
        
        Returns:
            瞬态集合
        """
        return self._states - self.get_absorbing_states()
    
    def get_communicating_classes(self) -> List[set]:
        """
        获取互通类（相互可达的状态集合）
        
        Returns:
            互通类列表
        """
        if not self._states:
            return []
        
        unvisited = set(self._states)
        classes = []
        
        while unvisited:
            start = unvisited.pop()
            
            # 找到从 start 可达的所有状态
            reachable_from_start = {start}
            frontier = [start]
            
            while frontier:
                current = frontier.pop(0)
                for next_state in self._counts[current]:
                    if next_state not in reachable_from_start:
                        reachable_from_start.add(next_state)
                        frontier.append(next_state)
            
            # 找到能到达 start 的所有状态
            can_reach_start = {start}
            # 反向图
            reverse_counts = defaultdict(set)
            for from_state in self._states:
                for to_state in self._counts[from_state]:
                    reverse_counts[to_state].add(from_state)
            
            frontier = [start]
            while frontier:
                current = frontier.pop(0)
                for prev_state in reverse_counts[current]:
                    if prev_state not in can_reach_start:
                        can_reach_start.add(prev_state)
                        frontier.append(prev_state)
            
            # 互通类 = 可达 start 且从 start 可达
            comm_class = reachable_from_start & can_reach_start
            classes.append(comm_class)
            unvisited -= comm_class
        
        return classes
    
    @property
    def states(self) -> set:
        """获取所有状态"""
        return self._states.copy()
    
    @property
    def num_states(self) -> int:
        """状态数量"""
        return len(self._states)
    
    @property
    def num_transitions(self) -> int:
        """转移总数"""
        return sum(self._row_totals.values())
    
    def to_matrix(self) -> Tuple[List[Any], List[List[float]]]:
        """
        转换为数值矩阵
        
        Returns:
            (状态列表, 概率矩阵)
        """
        states = list(self._states)
        n = len(states)
        state_idx = {s: i for i, s in enumerate(states)}
        
        matrix = [[0.0] * n for _ in range(n)]
        
        for from_state, row in self._counts.items():
            from_idx = state_idx[from_state]
            total = self._row_totals[from_state]
            
            for to_state, count in row.items():
                to_idx = state_idx[to_state]
                matrix[from_idx][to_idx] = count / total if total > 0 else 0.0
        
        return states, matrix
    
    def clear(self) -> None:
        """清空矩阵"""
        self._counts.clear()
        self._row_totals.clear()
        self._states.clear()
    
    def __repr__(self) -> str:
        return f"TransitionMatrix(states={self.num_states}, transitions={self.num_transitions})"