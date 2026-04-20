"""
Markov Chain Utils - 马尔可夫链工具集

零外部依赖的马尔可夫链实现，支持：
- 文本生成（基于 n-gram）
- 状态转移概率计算
- 序列预测
- 随机过程模拟

Author: AllToolkit
Date: 2026-04-21
"""

from .markov_chain import MarkovChain
from .text_generator import MarkovTextGenerator
from .sequence_predictor import SequencePredictor
from .transition_matrix import TransitionMatrix

__all__ = [
    'MarkovChain',
    'MarkovTextGenerator', 
    'SequencePredictor',
    'TransitionMatrix'
]

__version__ = '1.0.0'