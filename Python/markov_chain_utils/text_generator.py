"""
基于马尔可夫链的文本生成器
"""

import random
import re
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


class MarkovTextGenerator:
    """
    马尔可夫链文本生成器
    
    支持：
    - 字符级别生成
    - 单词级别生成
    - 自定义分词
    - 温度参数控制随机性
    
    Examples:
        >>> gen = MarkovTextGenerator(order=2)
        >>> gen.train("The cat sat on the mat. The cat was happy.")
        >>> gen.generate("The cat", max_length=20)
        'The cat sat on the mat'
    """
    
    # 常见句子结束标记
    DEFAULT_END_TOKENS = {'.', '!', '?', '。', '！', '？'}
    
    def __init__(
        self, 
        order: int = 2, 
        mode: str = 'word',
        seed: Optional[int] = None
    ):
        """
        初始化文本生成器
        
        Args:
            order: n-gram 阶数
            mode: 'word' 单词级别, 'char' 字符级别
            seed: 随机种子
        """
        if order < 1:
            raise ValueError("阶数必须 >= 1")
        
        if mode not in ('word', 'char'):
            raise ValueError("mode 必须是 'word' 或 'char'")
        
        self.order = order
        self.mode = mode
        self.seed = seed
        
        self._transitions: Dict[Tuple, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._state_counts: Dict[Tuple, int] = defaultdict(int)
        self._start_states: List[Tuple] = []
        self._sentences: List[str] = []
        
        if seed is not None:
            random.seed(seed)
    
    def tokenize(self, text: str) -> List[str]:
        """
        分词
        
        Args:
            text: 输入文本
            
        Returns:
            token 列表
        """
        if self.mode == 'char':
            return list(text)
        else:
            # 单词级别：保留标点
            tokens = re.findall(r'\S+', text)
            return tokens
    
    def train(self, text: str) -> 'MarkovTextGenerator':
        """
        训练文本生成器
        
        Args:
            text: 训练文本
            
        Returns:
            self
        """
        self._sentences.append(text)
        tokens = self.tokenize(text)
        
        if len(tokens) < self.order + 1:
            return self
        
        # 记录起始状态
        start = tuple(tokens[:self.order])
        self._start_states.append(start)
        
        # 构建转移
        for i in range(len(tokens) - self.order):
            current = tuple(tokens[i:i + self.order])
            next_token = tokens[i + self.order]
            
            self._transitions[current][next_token] += 1
            self._state_counts[current] += 1
        
        return self
    
    def train_from_file(self, filepath: str, encoding: str = 'utf-8') -> 'MarkovTextGenerator':
        """
        从文件训练
        
        Args:
            filepath: 文件路径
            encoding: 文件编码
            
        Returns:
            self
        """
        with open(filepath, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if line:
                    self.train(line)
        return self
    
    def train_from_sentences(self, sentences: List[str]) -> 'MarkovTextGenerator':
        """
        从多个句子训练
        
        Args:
            sentences: 句子列表
            
        Returns:
            self
        """
        for sentence in sentences:
            self.train(sentence)
        return self
    
    def _sample_next(self, current: Tuple, temperature: float = 1.0) -> Optional[str]:
        """
        温度采样
        
        Args:
            current: 当前状态
            temperature: 温度参数（越高越随机）
            
        Returns:
            采样的下一个 token
        """
        if current not in self._transitions:
            return None
        
        transitions = self._transitions[current]
        total = sum(transitions.values())
        
        if total == 0:
            return None
        
        # 计算概率
        if temperature == 0:
            # 贪心选择
            return max(transitions.keys(), key=lambda k: transitions[k])
        
        # 温度调整的概率
        import math
        tokens = list(transitions.keys())
        counts = [transitions[t] for t in tokens]
        
        # 转换为概率并应用温度
        probs = [c / total for c in counts]
        if temperature != 1.0:
            # 简化的温度调整
            adjusted = [p ** (1 / temperature) for p in probs]
            total_adj = sum(adjusted)
            probs = [p / total_adj for p in adjusted]
        
        # 随机选择
        r = random.random()
        cumulative = 0
        for token, prob in zip(tokens, probs):
            cumulative += prob
            if r <= cumulative:
                return token
        
        return tokens[-1]
    
    def generate(
        self, 
        start: Optional[str] = None,
        max_length: int = 50,
        temperature: float = 1.0,
        end_tokens: Optional[Set[str]] = None
    ) -> str:
        """
        生成文本
        
        Args:
            start: 起始文本
            max_length: 最大 token 数量
            temperature: 温度参数（0=确定性，>1=更随机）
            end_tokens: 结束标记集合
            
        Returns:
            生成的文本
        """
        if not self._transitions:
            raise ValueError("模型未训练，请先调用 train()")
        
        if end_tokens is None:
            end_tokens = self.DEFAULT_END_TOKENS if self.mode == 'word' else set()
        
        # 处理起始文本
        if start:
            tokens = self.tokenize(start)
            if len(tokens) < self.order:
                # 补充随机 token
                if self._start_states:
                    random_start = random.choice(self._start_states)
                    tokens = list(random_start[:self.order - len(tokens)]) + tokens
            current = tuple(tokens[-self.order:])
            result = tokens
        else:
            current = random.choice(self._start_states)
            result = list(current)
        
        # 生成
        for _ in range(max_length):
            next_token = self._sample_next(current, temperature)
            
            if next_token is None:
                break
            
            result.append(next_token)
            
            # 检查结束标记
            if next_token in end_tokens:
                break
            
            # 更新当前状态
            current = tuple(result[-self.order:])
        
        # 后处理
        if self.mode == 'word':
            return ' '.join(result)
        else:
            return ''.join(result)
    
    def generate_sentence(
        self,
        start: Optional[str] = None,
        max_length: int = 50,
        temperature: float = 1.0
    ) -> str:
        """
        生成完整句子（以标点结束）
        
        Args:
            start: 起始文本
            max_length: 最大 token 数量
            temperature: 温度参数
            
        Returns:
            生成的句子
        """
        return self.generate(
            start=start,
            max_length=max_length,
            temperature=temperature,
            end_tokens=self.DEFAULT_END_TOKENS
        )
    
    def generate_paragraph(
        self,
        num_sentences: int = 3,
        start: Optional[str] = None,
        max_length_per_sentence: int = 30,
        temperature: float = 1.0
    ) -> str:
        """
        生成段落
        
        Args:
            num_sentences: 句子数量
            start: 起始文本
            max_length_per_sentence: 每句最大长度
            temperature: 温度参数
            
        Returns:
            生成的段落
        """
        sentences = []
        current_start = start
        
        for i in range(num_sentences):
            sentence = self.generate_sentence(
                start=current_start if i == 0 else None,
                max_length=max_length_per_sentence,
                temperature=temperature
            )
            sentences.append(sentence)
            
            # 用最后几个词作为下一句的开始
            tokens = self.tokenize(sentence)
            if len(tokens) >= self.order:
                current_start = ' '.join(tokens[-self.order:]) if self.mode == 'word' else ''.join(tokens[-self.order:])
        
        return ' '.join(sentences)
    
    def get_continuations(self, prefix: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        获取可能的续写及其概率
        
        Args:
            prefix: 前缀文本
            top_n: 返回数量
            
        Returns:
            (续写 token, 概率) 列表
        """
        tokens = self.tokenize(prefix)
        
        if len(tokens) < self.order:
            return []
        
        current = tuple(tokens[-self.order:])
        
        if current not in self._transitions:
            return []
        
        total = self._state_counts[current]
        if total == 0:
            return []
        
        continuations = [
            (token, count / total)
            for token, count in self._transitions[current].items()
        ]
        
        return sorted(continuations, key=lambda x: x[1], reverse=True)[:top_n]
    
    @property
    def vocabulary_size(self) -> int:
        """词汇表大小"""
        vocab = set()
        for current in self._transitions:
            vocab.update(current)
            vocab.update(self._transitions[current].keys())
        return len(vocab)
    
    def __repr__(self) -> str:
        return f"MarkovTextGenerator(order={self.order}, mode={self.mode}, vocab={self.vocabulary_size})"