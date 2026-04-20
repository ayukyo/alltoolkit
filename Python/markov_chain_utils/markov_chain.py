"""
马尔可夫链核心实现
"""

import random
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple


class MarkovChain:
    """
    马尔可夫链实现
    
    支持任意状态类型，可配置阶数（n-gram）
    
    Examples:
        >>> mc = MarkovChain(order=1)
        >>> mc.train(['A', 'B', 'A', 'C', 'A', 'B'])
        >>> mc.generate('A', steps=5)
        ['A', 'B', 'A', 'C', 'A']
    """
    
    def __init__(self, order: int = 1, seed: Optional[int] = None):
        """
        初始化马尔可夫链
        
        Args:
            order: 马尔可夫链阶数（1 = 一阶，使用前1个状态预测下一个状态）
            seed: 随机种子，用于可重复生成
        """
        if order < 1:
            raise ValueError("阶数必须 >= 1")
        
        self.order = order
        self.seed = seed
        self._transitions: Dict[Tuple, Dict[Any, int]] = defaultdict(lambda: defaultdict(int))
        self._state_counts: Dict[Tuple, int] = defaultdict(int)
        self._states: Set[Any] = set()
        self._start_states: List[Tuple] = []
        
        if seed is not None:
            random.seed(seed)
    
    def train(self, sequence: List[Any]) -> 'MarkovChain':
        """
        训练马尔可夫链
        
        Args:
            sequence: 状态序列
            
        Returns:
            self，支持链式调用
        """
        if len(sequence) < self.order + 1:
            raise ValueError(f"序列长度必须 >= {self.order + 1}")
        
        # 记录所有状态
        self._states.update(sequence)
        
        # 记录起始状态
        start_state = tuple(sequence[:self.order])
        self._start_states.append(start_state)
        
        # 构建转移概率
        for i in range(len(sequence) - self.order):
            current_state = tuple(sequence[i:i + self.order])
            next_state = sequence[i + self.order]
            
            self._transitions[current_state][next_state] += 1
            self._state_counts[current_state] += 1
        
        return self
    
    def train_multiple(self, sequences: List[List[Any]]) -> 'MarkovChain':
        """
        使用多个序列训练
        
        Args:
            sequences: 多个状态序列的列表
            
        Returns:
            self
        """
        for seq in sequences:
            if len(seq) >= self.order + 1:
                self.train(seq)
        return self
    
    def get_transition_probability(self, current: Tuple, next_state: Any) -> float:
        """
        获取转移概率 P(next_state | current)
        
        Args:
            current: 当前状态元组
            next_state: 下一个状态
            
        Returns:
            转移概率（0.0 - 1.0）
        """
        if current not in self._transitions:
            return 0.0
        
        if next_state not in self._transitions[current]:
            return 0.0
        
        total = self._state_counts[current]
        if total == 0:
            return 0.0
        
        return self._transitions[current][next_state] / total
    
    def get_possible_next_states(self, current: Tuple) -> List[Tuple[Any, float]]:
        """
        获取所有可能的下一状态及其概率
        
        Args:
            current: 当前状态元组
            
        Returns:
            (状态, 概率) 列表，按概率降序排列
        """
        if current not in self._transitions:
            return []
        
        total = self._state_counts[current]
        if total == 0:
            return []
        
        states_with_probs = [
            (state, count / total)
            for state, count in self._transitions[current].items()
        ]
        
        return sorted(states_with_probs, key=lambda x: x[1], reverse=True)
    
    def predict_next(self, current: Tuple) -> Optional[Any]:
        """
        预测下一个最可能的状态
        
        Args:
            current: 当前状态元组
            
        Returns:
            最可能的下一状态，如果无法预测返回 None
        """
        states = self.get_possible_next_states(current)
        return states[0][0] if states else None
    
    def sample_next(self, current: Tuple) -> Optional[Any]:
        """
        根据转移概率随机采样下一个状态
        
        Args:
            current: 当前状态元组
            
        Returns:
            随机采样的下一状态
        """
        if current not in self._transitions:
            return None
        
        total = self._state_counts[current]
        if total == 0:
            return None
        
        # 加权随机选择
        r = random.random() * total
        cumulative = 0
        
        for state, count in self._transitions[current].items():
            cumulative += count
            if r <= cumulative:
                return state
        
        # 防止浮点误差
        return list(self._transitions[current].keys())[-1]
    
    def generate(
        self, 
        start: Optional[Tuple] = None, 
        steps: int = 10,
        allow_unseen: bool = True
    ) -> List[Any]:
        """
        生成状态序列
        
        Args:
            start: 起始状态元组，如果为 None 则随机选择
            steps: 生成步数
            allow_unseen: 是否允许进入未见过的状态
            
        Returns:
            生成的状态序列
        """
        if not self._transitions:
            raise ValueError("模型未训练，请先调用 train()")
        
        # 选择起始状态
        if start is None:
            start = random.choice(self._start_states)
        elif start not in self._transitions:
            if not allow_unseen:
                raise ValueError(f"起始状态 {start} 不在训练数据中")
            # 尝试找到相似的状态
            start = random.choice(self._start_states)
        
        result = list(start)
        current = start
        
        for _ in range(steps):
            next_state = self.sample_next(current)
            
            if next_state is None:
                # 如果当前状态没有转移，尝试重新开始
                if allow_unseen:
                    current = random.choice(self._start_states)
                    result.append(current[-1])
                else:
                    break
            else:
                result.append(next_state)
                # 更新当前状态（滑动窗口）
                current = tuple(list(current[1:]) + [next_state])
        
        return result
    
    def generate_sentence(
        self, 
        start: Optional[Tuple] = None, 
        max_steps: int = 100,
        end_tokens: Optional[Set[Any]] = None
    ) -> List[Any]:
        """
        生成直到遇到结束标记的序列
        
        Args:
            start: 起始状态
            max_steps: 最大步数
            end_tokens: 结束标记集合
            
        Returns:
            生成的序列
        """
        if end_tokens is None:
            end_tokens = set()
        
        result = self.generate(start, steps=1)
        
        for _ in range(max_steps - 1):
            if result[-1] in end_tokens:
                break
            
            current = tuple(result[-self.order:])
            next_state = self.sample_next(current)
            
            if next_state is None:
                break
            
            result.append(next_state)
        
        return result
    
    @property
    def states(self) -> Set[Any]:
        """获取所有已知状态"""
        return self._states.copy()
    
    @property
    def num_states(self) -> int:
        """获取状态数量"""
        return len(self._states)
    
    def get_state_frequency(self, state: Any) -> int:
        """获取状态出现频率"""
        count = 0
        for current_state, transitions in self._transitions.items():
            if state in current_state:
                count += self._state_counts[current_state]
            if state in transitions:
                count += transitions[state]
        return count
    
    def clear(self) -> None:
        """清空模型"""
        self._transitions.clear()
        self._state_counts.clear()
        self._states.clear()
        self._start_states.clear()
    
    def __repr__(self) -> str:
        return f"MarkovChain(order={self.order}, states={self.num_states}, transitions={len(self._transitions)})"