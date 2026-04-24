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
    PokerGame,
    
    # 函数
    create_deck,
    shuffle_deck,
    deal_hands,
    evaluate_hand,
    compare_hands,
    best_hand,
    hand_probability,
    hand_combinations_count,
    cards_to_string,
    string_to_cards,
    get_all_cards,
    card_count_by_rank,
    card_count_by_suit,
    
    # 常量
    SUIT_SYMBOLS,
    SUIT_NAMES,
    RANK_SYMBOLS,
    RANK_NAMES,
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
    'PokerGame',
    
    # 函数
    'create_deck',
    'shuffle_deck',
    'deal_hands',
    'evaluate_hand',
    'compare_hands',
    'best_hand',
    'hand_probability',
    'hand_combinations_count',
    'cards_to_string',
    'string_to_cards',
    'get_all_cards',
    'card_count_by_rank',
    'card_count_by_suit',
    
    # 常量
    'SUIT_SYMBOLS',
    'SUIT_NAMES',
    'RANK_SYMBOLS',
    'RANK_NAMES',
    'HAND_RANK_NAMES',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'