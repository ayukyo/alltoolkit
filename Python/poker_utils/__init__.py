"""
扑克牌工具集 (Poker Utils)

零外部依赖的扑克牌处理工具。
"""

from .mod import (
    # 枚举
    Suit,
    Rank,
    HandRank,
    
    # 类
    Card,
    Deck,
    Hand,
    PokerEvaluator,
    TexasHoldem,
    HandAnalyzer,
    
    # 函数
    create_deck,
    parse_cards,
    cards_to_str,
    evaluate_hand,
    compare_hands,
    get_hand_rank_name,
    simulate_win_rate,
    is_pocket_pair,
    is_suited,
    is_connected,
    get_starting_hand_strength,
    
    # 常量
    SUIT_SYMBOLS,
    RANK_SYMBOLS,
    HAND_RANK_NAMES,
)

__all__ = [
    # 枚举
    'Suit',
    'Rank',
    'HandRank',
    
    # 类
    'Card',
    'Deck',
    'Hand',
    'PokerEvaluator',
    'TexasHoldem',
    'HandAnalyzer',
    
    # 函数
    'create_deck',
    'parse_cards',
    'cards_to_str',
    'evaluate_hand',
    'compare_hands',
    'get_hand_rank_name',
    'simulate_win_rate',
    'is_pocket_pair',
    'is_suited',
    'is_connected',
    'get_starting_hand_strength',
    
    # 常量
    'SUIT_SYMBOLS',
    'RANK_SYMBOLS',
    'HAND_RANK_NAMES',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'