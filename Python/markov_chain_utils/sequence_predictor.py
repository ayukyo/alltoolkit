"""
序列预测器 - 基于马尔可夫链的序列预测
"""

import random
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple


class SequencePredictor:
    """
    序列预测器
    
    用于预测离散序列的下一个元素，支持：
    - 单步预测
    - 多步预测
    - 概率分布预测
    - 异常检测
    
    Examples:
        >>> sp = SequencePredictor(order=2)
        >>> sp.train([1, 2, 3, 1, 2, 4, 1, 2, 3])
        >>> sp.predict([1, 2])
        3
        >>> sp.predict_with_probability([1, 2])
        (3, 0.66)
    """
    
    def __init__(self, order: int = 2, smoothing: float = 0.0, seed: Optional[int] = None):
        """
        初始化序列预测器
        
        Args:
            order: 预测阶数（使用前 order 个元素预测）
            smoothing: 平滑参数（Laplace 平滑）
            seed: 随机种子
        """
        if order < 1:
            raise ValueError("阶数必须 >= 1")
        
        self.order = order
        self.smoothing = smoothing
        self.seed = seed
        
        self._transitions: Dict[Tuple, Dict[Any, int]] = defaultdict(lambda: defaultdict(int))
        self._state_counts: Dict[Tuple, int] = defaultdict(int)
        self._vocabulary: set = set()
        self._sequences: List[List[Any]] = []
        
        if seed is not None:
            random.seed(seed)
    
    def train(self, sequence: List[Any]) -> 'SequencePredictor':
        """
        训练预测器
        
        Args:
            sequence: 训练序列
            
        Returns:
            self
        """
        if len(sequence) < self.order + 1:
            return self
        
        self._vocabulary.update(sequence)
        self._sequences.append(sequence)
        
        for i in range(len(sequence) - self.order):
            current = tuple(sequence[i:i + self.order])
            next_val = sequence[i + self.order]
            
            self._transitions[current][next_val] += 1
            self._state_counts[current] += 1
        
        return self
    
    def train_multiple(self, sequences: List[List[Any]]) -> 'SequencePredictor':
        """
        使用多个序列训练
        
        Args:
            sequences: 多个训练序列
            
        Returns:
            self
        """
        for seq in sequences:
            self.train(seq)
        return self
    
    def predict(self, context: List[Any]) -> Optional[Any]:
        """
        预测下一个元素
        
        Args:
            context: 上下文（前 order 个元素）
            
        Returns:
            预测的元素，无法预测时返回 None
        """
        if len(context) < self.order:
            return None
        
        state = tuple(context[-self.order:])
        
        if state not in self._transitions:
            return None
        
        # 返回最可能的元素
        return max(self._transitions[state].keys(), key=lambda x: self._transitions[state][x])
    
    def predict_with_probability(
        self, 
        context: List[Any]
    ) -> Tuple[Optional[Any], float]:
        """
        预测并返回概率
        
        Args:
            context: 上下文
            
        Returns:
            (预测元素, 概率) 元组
        """
        if len(context) < self.order:
            return None, 0.0
        
        state = tuple(context[-self.order:])
        
        if state not in self._transitions:
            return None, 0.0
        
        total = self._state_counts[state] + self.smoothing * len(self._vocabulary)
        
        best = max(
            self._transitions[state].keys(),
            key=lambda x: self._transitions[state][x]
        )
        
        count = self._transitions[state][best] + self.smoothing
        probability = count / total
        
        return best, probability
    
    def predict_distribution(
        self, 
        context: List[Any],
        top_n: Optional[int] = None
    ) -> List[Tuple[Any, float]]:
        """
        预测概率分布
        
        Args:
            context: 上下文
            top_n: 返回前 N 个结果，None 表示返回全部
            
        Returns:
            (元素, 概率) 列表，按概率降序排列
        """
        if len(context) < self.order:
            return []
        
        state = tuple(context[-self.order:])
        
        if state not in self._transitions:
            return []
        
        total = self._state_counts[state] + self.smoothing * len(self._vocabulary)
        
        distribution = []
        for val, count in self._transitions[state].items():
            prob = (count + self.smoothing) / total
            distribution.append((val, prob))
        
        distribution.sort(key=lambda x: x[1], reverse=True)
        
        if top_n is not None:
            distribution = distribution[:top_n]
        
        return distribution
    
    def predict_sequence(
        self, 
        context: List[Any], 
        steps: int = 5
    ) -> List[Any]:
        """
        多步预测
        
        Args:
            context: 初始上下文
            steps: 预测步数
            
        Returns:
            预测的序列
        """
        if len(context) < self.order:
            return []
        
        result = []
        current_context = list(context[-self.order:])
        
        for _ in range(steps):
            prediction = self.predict(current_context)
            
            if prediction is None:
                break
            
            result.append(prediction)
            current_context = current_context[1:] + [prediction]
        
        return result
    
    def sample_next(self, context: List[Any]) -> Optional[Any]:
        """
        根据概率分布随机采样
        
        Args:
            context: 上下文
            
        Returns:
            采样的元素
        """
        distribution = self.predict_distribution(context)
        
        if not distribution:
            return None
        
        r = random.random()
        cumulative = 0
        
        for val, prob in distribution:
            cumulative += prob
            if r <= cumulative:
                return val
        
        return distribution[-1][0]
    
    def evaluate(self, test_sequence: List[Any]) -> Dict[str, float]:
        """
        评估预测准确率
        
        Args:
            test_sequence: 测试序列
            
        Returns:
            评估指标字典
        """
        if len(test_sequence) < self.order + 1:
            return {'accuracy': 0.0, 'samples': 0}
        
        correct = 0
        total = 0
        total_probability = 0.0
        
        for i in range(len(test_sequence) - self.order):
            context = test_sequence[i:i + self.order]
            actual = test_sequence[i + self.order]
            
            predicted, prob = self.predict_with_probability(context)
            
            if predicted == actual:
                correct += 1
            
            total_probability += prob
            total += 1
        
        return {
            'accuracy': correct / total if total > 0 else 0.0,
            'avg_confidence': total_probability / total if total > 0 else 0.0,
            'samples': total
        }
    
    def detect_anomaly(
        self, 
        sequence: List[Any], 
        threshold: float = 0.1
    ) -> List[Tuple[int, Any, float]]:
        """
        检测序列中的异常点
        
        Args:
            sequence: 待检测序列
            threshold: 概率阈值，低于此值视为异常
            
        Returns:
            (位置, 元素, 概率) 列表
        """
        anomalies = []
        
        for i in range(self.order, len(sequence)):
            context = sequence[i - self.order:i]
            actual = sequence[i]
            
            distribution = self.predict_distribution(context)
            prob_dict = dict(distribution)
            
            prob = prob_dict.get(actual, self.smoothing / (len(self._vocabulary) or 1))
            
            if prob < threshold:
                anomalies.append((i, actual, prob))
        
        return anomalies
    
    def get_frequent_patterns(
        self, 
        min_count: int = 2
    ) -> List[Tuple[Tuple, Any, int]]:
        """
        获取频繁模式
        
        Args:
            min_count: 最小出现次数
            
        Returns:
            (上下文, 下一个元素, 次数) 列表
        """
        patterns = []
        
        for state, transitions in self._transitions.items():
            for next_val, count in transitions.items():
                if count >= min_count:
                    patterns.append((state, next_val, count))
        
        return sorted(patterns, key=lambda x: x[2], reverse=True)
    
    @property
    def vocabulary(self) -> set:
        """获取词汇表"""
        return self._vocabulary.copy()
    
    @property
    def vocabulary_size(self) -> int:
        """词汇表大小"""
        return len(self._vocabulary)
    
    def clear(self) -> None:
        """清空模型"""
        self._transitions.clear()
        self._state_counts.clear()
        self._vocabulary.clear()
        self._sequences.clear()
    
    def __repr__(self) -> str:
        return f"SequencePredictor(order={self.order}, vocab={self.vocabulary_size}, smoothing={self.smoothing})"