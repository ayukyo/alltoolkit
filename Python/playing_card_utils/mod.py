"""
Playing Card Utilities - 扑克牌工具模块

提供完整的扑克牌功能，包括牌组创建、洗牌、发牌、手牌评估等。
支持德州扑克、21点、桥牌等常见扑克游戏。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

import random
from enum import Enum
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass
from collections import Counter


class Suit(Enum):
    """花色"""
    SPADES = "♠"      # 黑桃
    HEARTS = "♥"      # 红心
    DIAMONDS = "♦"    # 方块
    CLUBS = "♣"       # 梅花
    
    @property
    def name_zh(self) -> str:
        """中文名称"""
        names = {
            Suit.SPADES: "黑桃",
            Suit.HEARTS: "红心",
            Suit.DIAMONDS: "方块",
            Suit.CLUBS: "梅花",
        }
        return names[self]
    
    @property
    def color(self) -> str:
        """颜色（red/black）"""
        return "red" if self in (Suit.HEARTS, Suit.DIAMONDS) else "black"


class Rank(Enum):
    """点数"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    @property
    def numeric_value(self) -> int:
        """数值（用于比较大小）"""
        return self.value
    
    @property
    def symbol(self) -> str:
        """显示符号"""
        symbols = {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A",
        }
        return symbols[self]
    
    @property
    def name_zh(self) -> str:
        """中文名称"""
        names = {
            Rank.TWO: "二",
            Rank.THREE: "三",
            Rank.FOUR: "四",
            Rank.FIVE: "五",
            Rank.SIX: "六",
            Rank.SEVEN: "七",
            Rank.EIGHT: "八",
            Rank.NINE: "九",
            Rank.TEN: "十",
            Rank.JACK: "杰克",
            Rank.QUEEN: "皇后",
            Rank.KING: "国王",
            Rank.ACE: "王牌",
        }
        return names[self]


@dataclass(frozen=True)
class Card:
    """扑克牌"""
    suit: Suit
    rank: Rank
    
    def __str__(self) -> str:
        return f"{self.suit.value}{self.rank.symbol}"
    
    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"
    
    def __lt__(self, other: "Card") -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self.rank.value, list(Suit).index(self.suit)) < (other.rank.value, list(Suit).index(other.suit))
    
    def __le__(self, other: "Card") -> bool:
        return self == other or self < other
    
    def __gt__(self, other: "Card") -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self.rank.value, list(Suit).index(self.suit)) > (other.rank.value, list(Suit).index(other.suit))
    
    def __ge__(self, other: "Card") -> bool:
        return self == other or self > other
    
    @property
    def display(self) -> str:
        """完整显示名称"""
        return f"{self.suit.name_zh}{self.rank.symbol}"
    
    @property
    def is_face_card(self) -> bool:
        """是否是人头牌（J/Q/K）"""
        return self.rank in (Rank.JACK, Rank.QUEEN, Rank.KING)
    
    @property
    def is_ace(self) -> bool:
        """是否是A"""
        return self.rank == Rank.ACE
    
    @classmethod
    def from_string(cls, card_str: str) -> "Card":
        """
        从字符串创建牌
        
        Args:
            card_str: 牌字符串，如 "♠A", "♥K", "♦10", "♣2"
            
        Returns:
            Card 对象
        """
        if len(card_str) < 2:
            raise ValueError(f"无效的牌字符串: {card_str}")
        
        # 解析花色
        suit_map = {
            "♠": Suit.SPADES, "S": Suit.SPADES,
            "♥": Suit.HEARTS, "H": Suit.HEARTS,
            "♦": Suit.DIAMONDS, "D": Suit.DIAMONDS,
            "♣": Suit.CLUBS, "C": Suit.CLUBS,
        }
        
        suit_char = card_str[0]
        if suit_char not in suit_map:
            raise ValueError(f"未知的花色: {suit_char}")
        suit = suit_map[suit_char]
        
        # 解析点数
        rank_str = card_str[1:].upper()
        rank_map = {
            "2": Rank.TWO, "3": Rank.THREE, "4": Rank.FOUR, "5": Rank.FIVE,
            "6": Rank.SIX, "7": Rank.SEVEN, "8": Rank.EIGHT, "9": Rank.NINE,
            "10": Rank.TEN, "J": Rank.JACK, "Q": Rank.QUEEN, "K": Rank.KING, "A": Rank.ACE,
        }
        
        if rank_str not in rank_map:
            raise ValueError(f"未知的点数: {rank_str}")
        rank = rank_map[rank_str]
        
        return cls(suit, rank)


class HandRank(Enum):
    """扑克手牌等级"""
    HIGH_CARD = (1, "高牌")
    ONE_PAIR = (2, "一对")
    TWO_PAIR = (3, "两对")
    THREE_OF_A_KIND = (4, "三条")
    STRAIGHT = (5, "顺子")
    FLUSH = (6, "同花")
    FULL_HOUSE = (7, "葫芦")
    FOUR_OF_A_KIND = (8, "四条")
    STRAIGHT_FLUSH = (9, "同花顺")
    ROYAL_FLUSH = (10, "皇家同花顺")
    
    @property
    def rank(self) -> int:
        return self.value[0]
    
    @property
    def name_zh(self) -> str:
        return self.value[1]


@dataclass
class HandResult:
    """手牌评估结果"""
    rank: HandRank
    cards: List[Card]
    kickers: List[Card]
    score: int
    
    def __str__(self) -> str:
        return f"{self.rank.name_zh} ({self.cards})"
    
    def __lt__(self, other: "HandResult") -> bool:
        return self.score < other.score
    
    def __gt__(self, other: "HandResult") -> bool:
        return self.score > other.score


class Deck:
    """牌组"""
    
    def __init__(self, include_jokers: bool = False):
        """
        初始化牌组
        
        Args:
            include_jokers: 是否包含大小王
        """
        self._cards: List[Card] = []
        self._include_jokers = include_jokers
        self._build_deck()
    
    def _build_deck(self) -> None:
        """构建标准52张牌组"""
        self._cards = [
            Card(suit, rank)
            for suit in Suit
            for rank in Rank
        ]
        
        if self._include_jokers:
            # 添加大小王（用特殊标记）
            # 注意：这里简化处理，实际上大小王没有花色和点数
            pass
    
    def shuffle(self, seed: Optional[int] = None) -> "Deck":
        """
        洗牌
        
        Args:
            seed: 随机种子（可选，用于可重复的游戏）
            
        Returns:
            self（支持链式调用）
        """
        rng = random.Random(seed) if seed is not None else random.Random()
        rng.shuffle(self._cards)
        return self
    
    def deal(self, num_cards: int = 1) -> List[Card]:
        """
        发牌
        
        Args:
            num_cards: 发牌数量
            
        Returns:
            发出的牌列表
        """
        if num_cards > len(self._cards):
            raise ValueError(f"牌组中只有 {len(self._cards)} 张牌，无法发 {num_cards} 张")
        
        dealt = self._cards[:num_cards]
        self._cards = self._cards[num_cards:]
        return dealt
    
    def deal_hands(self, num_hands: int, cards_per_hand: int) -> List[List[Card]]:
        """
        发多手牌
        
        Args:
            num_hands: 手牌数量
            cards_per_hand: 每手牌的数量
            
        Returns:
            多手牌的列表
        """
        total_cards = num_hands * cards_per_hand
        if total_cards > len(self._cards):
            raise ValueError(f"牌组中只有 {len(self._cards)} 张牌，无法发 {num_hands} 手牌，每手 {cards_per_hand} 张")
        
        hands = []
        for _ in range(num_hands):
            hands.append(self.deal(cards_per_hand))
        return hands
    
    def draw(self) -> Card:
        """抽一张牌"""
        if not self._cards:
            raise ValueError("牌组已空")
        return self.deal(1)[0]
    
    def peek(self, index: int = 0) -> Card:
        """
        查看牌组顶部的牌（不移除）
        
        Args:
            index: 从顶部开始的位置（0为最顶）
        """
        if index >= len(self._cards):
            raise ValueError(f"牌组中只有 {len(self._cards)} 张牌")
        return self._cards[index]
    
    def reset(self) -> "Deck":
        """重置牌组"""
        self._build_deck()
        return self
    
    def add_card(self, card: Card) -> "Deck":
        """添加一张牌到牌组底部"""
        self._cards.append(card)
        return self
    
    def remove_card(self, card: Card) -> "Deck":
        """从牌组中移除一张牌"""
        if card in self._cards:
            self._cards.remove(card)
        return self
    
    def __len__(self) -> int:
        return len(self._cards)
    
    def __iter__(self):
        return iter(self._cards)
    
    def __str__(self) -> str:
        return f"Deck({len(self._cards)} cards)"
    
    def __repr__(self) -> str:
        return f"Deck(cards={len(self._cards)}, jokers={self._include_jokers})"
    
    @property
    def cards(self) -> List[Card]:
        """获取牌组中的所有牌"""
        return self._cards.copy()


class HandEvaluator:
    """扑克手牌评估器"""
    
    @staticmethod
    def evaluate(cards: List[Card]) -> HandResult:
        """
        评估5张牌的手牌强度
        
        Args:
            cards: 5张牌的列表
            
        Returns:
            HandResult 评估结果
        """
        if len(cards) != 5:
            raise ValueError("德州扑克手牌评估需要正好5张牌")
        
        # 排序
        sorted_cards = sorted(cards, key=lambda c: c.rank.value, reverse=True)
        
        # 统计花色和点数
        suits = [c.suit for c in sorted_cards]
        ranks = [c.rank.value for c in sorted_cards]
        rank_counts = Counter(ranks)
        
        # 检查同花
        is_flush = len(set(suits)) == 1
        
        # 检查顺子
        is_straight = HandEvaluator._is_straight(ranks)
        
        # 检查特殊顺子 A-2-3-4-5（最小顺子）
        is_low_straight = ranks == [14, 5, 4, 3, 2]
        
        # 任何顺子（包括低顺子）
        has_straight = is_straight or is_low_straight
        
        # 获取重复牌信息
        counts = sorted(rank_counts.values(), reverse=True)
        
        # 确定牌型
        if has_straight and is_flush:
            if ranks == [14, 13, 12, 11, 10]:
                # 皇家同花顺
                return HandResult(
                    rank=HandRank.ROYAL_FLUSH,
                    cards=sorted_cards,
                    kickers=[],
                    score=HandEvaluator._calculate_score(HandRank.ROYAL_FLUSH, ranks)
                )
            else:
                # 同花顺
                return HandResult(
                    rank=HandRank.STRAIGHT_FLUSH,
                    cards=sorted_cards,
                    kickers=[],
                    score=HandEvaluator._calculate_score(HandRank.STRAIGHT_FLUSH, 
                                                         [5 if is_low_straight else max(ranks)])
                )
        
        if counts == [4, 1]:
            # 四条
            quad_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker_rank = [r for r, c in rank_counts.items() if c == 1][0]
            return HandResult(
                rank=HandRank.FOUR_OF_A_KIND,
                cards=sorted_cards,
                kickers=[Card(Suit.SPADES, Rank(quad_rank))],
                score=HandEvaluator._calculate_score(HandRank.FOUR_OF_A_KIND, [quad_rank, kicker_rank])
            )
        
        if counts == [3, 2]:
            # 葫芦
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            return HandResult(
                rank=HandRank.FULL_HOUSE,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.FULL_HOUSE, [trip_rank, pair_rank])
            )
        
        if is_flush:
            return HandResult(
                rank=HandRank.FLUSH,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.FLUSH, ranks)
            )
        
        if has_straight:
            return HandResult(
                rank=HandRank.STRAIGHT,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.STRAIGHT, 
                                                    [5 if is_low_straight else max(ranks)])
            )
        
        if counts == [3, 1, 1]:
            # 三条
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            kicker_ranks = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return HandResult(
                rank=HandRank.THREE_OF_A_KIND,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.THREE_OF_A_KIND, [trip_rank] + kicker_ranks)
            )
        
        if counts == [2, 2, 1]:
            # 两对
            pair_ranks = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker_rank = [r for r, c in rank_counts.items() if c == 1][0]
            return HandResult(
                rank=HandRank.TWO_PAIR,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.TWO_PAIR, pair_ranks + [kicker_rank])
            )
        
        if counts == [2, 1, 1, 1]:
            # 一对
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            kicker_ranks = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return HandResult(
                rank=HandRank.ONE_PAIR,
                cards=sorted_cards,
                kickers=[],
                score=HandEvaluator._calculate_score(HandRank.ONE_PAIR, [pair_rank] + kicker_ranks)
            )
        
        # 高牌
        return HandResult(
            rank=HandRank.HIGH_CARD,
            cards=sorted_cards,
            kickers=[],
            score=HandEvaluator._calculate_score(HandRank.HIGH_CARD, ranks)
        )
    
    @staticmethod
    def _is_straight(ranks: List[int]) -> bool:
        """检查是否是顺子"""
        sorted_ranks = sorted(set(ranks))
        if len(sorted_ranks) != 5:
            return False
        return sorted_ranks[-1] - sorted_ranks[0] == 4
    
    @staticmethod
    def _calculate_score(rank: HandRank, values: List[int]) -> int:
        """
        计算手牌分数（用于比较大小）
        
        分数格式: [牌型等级][高牌][第二高]...
        每个部分占2位数字
        """
        score = rank.rank * 10000000
        for i, v in enumerate(values):
            score += v * (10 ** (4 - i * 2))
        return score
    
    @staticmethod
    def compare(hand1: List[Card], hand2: List[Card]) -> int:
        """
        比较两手牌
        
        Args:
            hand1: 第一手牌
            hand2: 第二手牌
            
        Returns:
            1: hand1赢, -1: hand2赢, 0: 平局
        """
        result1 = HandEvaluator.evaluate(hand1)
        result2 = HandEvaluator.evaluate(hand2)
        
        if result1.score > result2.score:
            return 1
        elif result1.score < result2.score:
            return -1
        return 0
    
    @staticmethod
    def get_best_hand(cards: List[Card]) -> HandResult:
        """
        从7张牌中找出最佳5张牌组合
        
        Args:
            cards: 7张牌（德州扑克：2张手牌 + 5张公共牌）
            
        Returns:
            最佳手牌评估结果
        """
        from itertools import combinations
        
        if len(cards) < 5:
            raise ValueError("至少需要5张牌")
        
        best_result = None
        for combo in combinations(cards, 5):
            result = HandEvaluator.evaluate(list(combo))
            if best_result is None or result.score > best_result.score:
                best_result = result
        
        return best_result


class Blackjack:
    """21点游戏工具"""
    
    @staticmethod
    def calculate_hand_value(cards: List[Card]) -> int:
        """
        计算21点手牌点数
        
        Args:
            cards: 手牌列表
            
        Returns:
            最佳点数值
        """
        value = 0
        aces = 0
        
        for card in cards:
            if card.rank == Rank.ACE:
                aces += 1
                value += 11
            elif card.rank.value >= 10:
                value += 10
            else:
                value += card.rank.value
        
        # 如果爆牌，将A从11转为1
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    @staticmethod
    def is_blackjack(cards: List[Card]) -> bool:
        """检查是否是 Blackjack（21点）"""
        return len(cards) == 2 and Blackjack.calculate_hand_value(cards) == 21
    
    @staticmethod
    def is_bust(cards: List[Card]) -> bool:
        """检查是否爆牌"""
        return Blackjack.calculate_hand_value(cards) > 21
    
    @staticmethod
    def should_hit(player_cards: List[Card], dealer_up_card: Card) -> bool:
        """
        基础策略建议：是否要牌
        
        Args:
            player_cards: 玩家手牌
            dealer_up_card: 庄家明牌
            
        Returns:
            True 建议要牌，False 建议停牌
        """
        player_value = Blackjack.calculate_hand_value(player_cards)
        dealer_value = dealer_up_card.rank.value if dealer_up_card.rank.value <= 10 else 10
        
        # 简化策略
        if player_value >= 17:
            return False
        if player_value <= 11:
            return True
        # 12-16点，看庄家牌
        if dealer_value >= 7:
            return True
        return False


class CardGame:
    """卡牌游戏辅助工具"""
    
    @staticmethod
    def war_compare(card1: Card, card2: Card) -> int:
        """
        战争牌比较
        
        Args:
            card1: 第一张牌
            card2: 第二张牌
            
        Returns:
            1: card1大, -1: card2大, 0: 平局
        """
        if card1.rank.value > card2.rank.value:
            return 1
        elif card1.rank.value < card2.rank.value:
            return -1
        return 0
    
    @staticmethod
    def create_hand_from_string(cards_str: str) -> List[Card]:
        """
        从字符串创建手牌
        
        Args:
            cards_str: 牌字符串，用空格分隔，如 "♠A ♥K ♦Q ♣J ♠10"
            
        Returns:
            Card 列表
        """
        cards = []
        for card_str in cards_str.split():
            cards.append(Card.from_string(card_str))
        return cards
    
    @staticmethod
    def cards_to_string(cards: List[Card]) -> str:
        """将牌列表转为字符串"""
        return " ".join(str(card) for card in cards)
    
    @staticmethod
    def get_card_name(card: Card) -> str:
        """获取牌的完整中文名称"""
        return f"{card.suit.name_zh}{card.rank.name_zh}"


# 便捷函数
def create_deck(include_jokers: bool = False) -> Deck:
    """创建并返回一个新牌组"""
    return Deck(include_jokers)


def shuffle_deck(seed: Optional[int] = None) -> Deck:
    """创建并洗好的牌组"""
    return Deck().shuffle(seed)


def deal_hand(num_cards: int = 5) -> List[Card]:
    """创建新牌组并发出一手牌"""
    deck = Deck()
    deck.shuffle()
    return deck.deal(num_cards)


def evaluate_poker_hand(cards: List[Card]) -> HandResult:
    """评估扑克手牌"""
    return HandEvaluator.evaluate(cards)


def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
    """比较两手扑克牌"""
    return HandEvaluator.compare(hand1, hand2)


def get_best_poker_hand(cards: List[Card]) -> HandResult:
    """从7张牌中找出最佳5张牌组合"""
    return HandEvaluator.get_best_hand(cards)