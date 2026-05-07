"""
扑克牌工具模块 (Poker Utils)
============================

提供扑克牌相关的核心功能：
- 扑克牌表示和操作
- 牌型判断（同花顺、四条、葫芦、同花、顺子、三条、两对、一对、高牌）
- 牌型比较和评分
- 洗牌和发牌
- 德州扑克牌型评估

零外部依赖，纯 Python 实现。

Author: AllToolkit
Date: 2026-05-08
"""

import random
from enum import IntEnum
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter


class Suit(IntEnum):
    """扑克牌花色"""
    SPADES = 0    # 黑桃 ♠
    HEARTS = 1    # 红心 ♥
    DIAMONDS = 2  # 方块 ♦
    CLUBS = 3     # 梅花 ♣


class Rank(IntEnum):
    """扑克牌点数"""
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


# 花色显示符号
SUIT_SYMBOLS = {
    Suit.SPADES: '♠',
    Suit.HEARTS: '♥',
    Suit.DIAMONDS: '♦',
    Suit.CLUBS: '♣'
}

# 点数显示符号
RANK_SYMBOLS = {
    Rank.TWO: '2',
    Rank.THREE: '3',
    Rank.FOUR: '4',
    Rank.FIVE: '5',
    Rank.SIX: '6',
    Rank.SEVEN: '7',
    Rank.EIGHT: '8',
    Rank.NINE: '9',
    Rank.TEN: 'T',
    Rank.JACK: 'J',
    Rank.QUEEN: 'Q',
    Rank.KING: 'K',
    Rank.ACE: 'A'
}


@dataclass(frozen=True)
class Card:
    """扑克牌"""
    rank: Rank
    suit: Suit
    
    def __str__(self) -> str:
        return f"{RANK_SYMBOLS[self.rank]}{SUIT_SYMBOLS[self.suit]}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __lt__(self, other: 'Card') -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.suit < other.suit
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self) -> int:
        return hash((self.rank, self.suit))
    
    @classmethod
    def from_str(cls, s: str) -> 'Card':
        """从字符串创建扑克牌
        
        Args:
            s: 牌字符串，如 'Ah' (红心A), 'Ts' (黑桃T), '2d' (方块2)
        
        Returns:
            Card 对象
        """
        s = s.upper()
        rank_map = {
            '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR, '5': Rank.FIVE,
            '6': Rank.SIX, '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE,
            'T': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE
        }
        suit_map = {
            'S': Suit.SPADES, 'H': Suit.HEARTS, 'D': Suit.DIAMONDS, 'C': Suit.CLUBS
        }
        
        rank_char = s[0]
        suit_char = s[1]
        
        return cls(rank=rank_map[rank_char], suit=suit_map[suit_char])


class HandRank(IntEnum):
    """牌型等级"""
    HIGH_CARD = 0       # 高牌
    ONE_PAIR = 1        # 一对
    TWO_PAIR = 2         # 两对
    THREE_OF_A_KIND = 3  # 三条
    STRAIGHT = 4        # 顺子
    FLUSH = 5           # 同花
    FULL_HOUSE = 6      # 葫芦
    FOUR_OF_A_KIND = 7   # 四条
    STRAIGHT_FLUSH = 8   # 同花顺
    ROYAL_FLUSH = 9      # 皇家同花顺


# 牌型中文名称
HAND_RANK_NAMES = {
    HandRank.HIGH_CARD: "高牌",
    HandRank.ONE_PAIR: "一对",
    HandRank.TWO_PAIR: "两对",
    HandRank.THREE_OF_A_KIND: "三条",
    HandRank.STRAIGHT: "顺子",
    HandRank.FLUSH: "同花",
    HandRank.FULL_HOUSE: "葫芦",
    HandRank.FOUR_OF_A_KIND: "四条",
    HandRank.STRAIGHT_FLUSH: "同花顺",
    HandRank.ROYAL_FLUSH: "皇家同花顺"
}


@dataclass
class Hand:
    """手牌评估结果"""
    rank: HandRank
    cards: List[Card]
    kickers: List[Rank]  # 用于比较的 kicker
    
    def __str__(self) -> str:
        return f"{HAND_RANK_NAMES[self.rank]}: {' '.join(str(c) for c in self.cards)}"
    
    def __lt__(self, other: 'Hand') -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.kickers < other.kickers
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return False
        return self.rank == other.rank and self.kickers == other.kickers


class Deck:
    """扑克牌组"""
    
    def __init__(self):
        self._cards: List[Card] = []
        self.reset()
    
    def reset(self) -> None:
        """重置牌组为完整52张牌"""
        self._cards = [
            Card(rank=rank, suit=suit)
            for suit in Suit
            for rank in Rank
        ]
    
    def shuffle(self) -> None:
        """洗牌"""
        random.shuffle(self._cards)
    
    def deal(self, count: int = 1) -> List[Card]:
        """发牌
        
        Args:
            count: 发牌数量
        
        Returns:
            发出的牌列表
        """
        if count > len(self._cards):
            raise ValueError(f"牌组只有 {len(self._cards)} 张牌，无法发 {count} 张")
        
        dealt = self._cards[:count]
        self._cards = self._cards[count:]
        return dealt
    
    def deal_one(self) -> Card:
        """发一张牌"""
        if not self._cards:
            raise ValueError("牌组已空")
        return self._cards.pop(0)
    
    def __len__(self) -> int:
        return len(self._cards)
    
    def __str__(self) -> str:
        return f"Deck({len(self._cards)} cards)"
    
    def remove(self, card: Card) -> bool:
        """从牌组中移除指定牌
        
        Args:
            card: 要移除的牌
        
        Returns:
            是否成功移除
        """
        if card in self._cards:
            self._cards.remove(card)
            return True
        return False
    
    def remove_cards(self, cards: List[Card]) -> int:
        """从牌组中移除多张牌
        
        Args:
            cards: 要移除的牌列表
        
        Returns:
            成功移除的数量
        """
        removed = 0
        for card in cards:
            if self.remove(card):
                removed += 1
        return removed


class PokerEvaluator:
    """扑克牌型评估器"""
    
    @staticmethod
    def evaluate(cards: List[Card]) -> Hand:
        """评估最佳5张牌型
        
        Args:
            cards: 手牌列表（可以是5-7张）
        
        Returns:
            最佳牌型的 Hand 对象
        """
        if len(cards) < 5:
            raise ValueError("至少需要5张牌才能评估牌型")
        
        if len(cards) == 5:
            return PokerEvaluator._evaluate_five(cards)
        
        # 从多张牌中找出最佳5张组合
        best_hand: Optional[Hand] = None
        from itertools import combinations
        
        for combo in combinations(cards, 5):
            hand = PokerEvaluator._evaluate_five(list(combo))
            if best_hand is None or hand > best_hand:
                best_hand = hand
        
        return best_hand
    
    @staticmethod
    def _evaluate_five(cards: List[Card]) -> Hand:
        """评估恰好5张牌的牌型"""
        ranks = sorted([c.rank for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        
        # 统计点数出现次数
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)
        
        # 判断是否同花
        is_flush = len(set(suits)) == 1
        
        # 判断是否顺子
        is_straight, straight_high = PokerEvaluator._check_straight(ranks)
        
        # 特殊情况：A-2-3-4-5 顺子（轮子）
        if not is_straight and set(ranks) == {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE}:
            is_straight = True
            straight_high = Rank.FIVE
        
        # 判断牌型
        if is_straight and is_flush:
            if straight_high == Rank.ACE:
                # 皇家同花顺
                return Hand(
                    rank=HandRank.ROYAL_FLUSH,
                    cards=cards,
                    kickers=[straight_high]
                )
            else:
                # 同花顺
                return Hand(
                    rank=HandRank.STRAIGHT_FLUSH,
                    cards=cards,
                    kickers=[straight_high]
                )
        
        if counts == [4, 1]:
            # 四条
            quad_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return Hand(
                rank=HandRank.FOUR_OF_A_KIND,
                cards=cards,
                kickers=[quad_rank, kicker]
            )
        
        if counts == [3, 2]:
            # 葫芦
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            return Hand(
                rank=HandRank.FULL_HOUSE,
                cards=cards,
                kickers=[trip_rank, pair_rank]
            )
        
        if is_flush:
            # 同花
            return Hand(
                rank=HandRank.FLUSH,
                cards=cards,
                kickers=ranks
            )
        
        if is_straight:
            # 顺子
            return Hand(
                rank=HandRank.STRAIGHT,
                cards=cards,
                kickers=[straight_high]
            )
        
        if counts == [3, 1, 1]:
            # 三条
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return Hand(
                rank=HandRank.THREE_OF_A_KIND,
                cards=cards,
                kickers=[trip_rank] + kickers
            )
        
        if counts == [2, 2, 1]:
            # 两对
            pair_ranks = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return Hand(
                rank=HandRank.TWO_PAIR,
                cards=cards,
                kickers=pair_ranks + [kicker]
            )
        
        if counts == [2, 1, 1, 1]:
            # 一对
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return Hand(
                rank=HandRank.ONE_PAIR,
                cards=cards,
                kickers=[pair_rank] + kickers
            )
        
        # 高牌
        return Hand(
            rank=HandRank.HIGH_CARD,
            cards=cards,
            kickers=ranks
        )
    
    @staticmethod
    def _check_straight(ranks: List[Rank]) -> Tuple[bool, Optional[Rank]]:
        """检查是否为顺子
        
        Args:
            ranks: 排序后的点数列表（降序）
        
        Returns:
            (是否顺子, 最高牌点数)
        """
        unique_ranks = sorted(set(ranks), reverse=True)
        if len(unique_ranks) != 5:
            return False, None
        
        # 检查连续性
        for i in range(4):
            if unique_ranks[i] - unique_ranks[i + 1] != 1:
                return False, None
        
        return True, unique_ranks[0]
    
    @staticmethod
    def compare_hands(hand1: Hand, hand2: Hand) -> int:
        """比较两手牌
        
        Args:
            hand1: 第一手牌
            hand2: 第二手牌
        
        Returns:
            1: hand1胜, -1: hand2胜, 0: 平局
        """
        if hand1 > hand2:
            return 1
        elif hand1 < hand2:
            return -1
        return 0
    
    @staticmethod
    def get_hand_description(hand: Hand) -> str:
        """获取牌型的详细描述
        
        Args:
            hand: 手牌对象
        
        Returns:
            牌型描述字符串
        """
        rank_names = {
            Rank.TWO: '2', Rank.THREE: '3', Rank.FOUR: '4', Rank.FIVE: '5',
            Rank.SIX: '6', Rank.SEVEN: '7', Rank.EIGHT: '8', Rank.NINE: '9',
            Rank.TEN: 'T', Rank.JACK: 'J', Rank.QUEEN: 'Q', Rank.KING: 'K', Rank.ACE: 'A'
        }
        
        if hand.rank == HandRank.ROYAL_FLUSH:
            suit = hand.cards[0].suit
            return f"皇家同花顺 ({SUIT_SYMBOLS[suit]})"
        
        if hand.rank == HandRank.STRAIGHT_FLUSH:
            return f"同花顺 ({rank_names[hand.kickers[0]]}高)"
        
        if hand.rank == HandRank.FOUR_OF_A_KIND:
            return f"四条 ({rank_names[hand.kickers[0]]})"
        
        if hand.rank == HandRank.FULL_HOUSE:
            return f"葫芦 ({rank_names[hand.kickers[0]]}带{rank_names[hand.kickers[1]]})"
        
        if hand.rank == HandRank.FLUSH:
            return f"同花 ({rank_names[hand.kickers[0]]}高)"
        
        if hand.rank == HandRank.STRAIGHT:
            return f"顺子 ({rank_names[hand.kickers[0]]}高)"
        
        if hand.rank == HandRank.THREE_OF_A_KIND:
            return f"三条 ({rank_names[hand.kickers[0]]})"
        
        if hand.rank == HandRank.TWO_PAIR:
            return f"两对 ({rank_names[hand.kickers[0]]}和{rank_names[hand.kickers[1]]})"
        
        if hand.rank == HandRank.ONE_PAIR:
            return f"一对 ({rank_names[hand.kickers[0]]})"
        
        return f"高牌 ({rank_names[hand.kickers[0]]}高)"


class TexasHoldem:
    """德州扑克工具类"""
    
    @staticmethod
    def evaluate_hand(hole_cards: List[Card], board: List[Card]) -> Hand:
        """评估德州扑克手牌
        
        Args:
            hole_cards: 底牌（2张）
            board: 公共牌（3-5张）
        
        Returns:
            最佳牌型
        """
        all_cards = hole_cards + board
        return PokerEvaluator.evaluate(all_cards)
    
    @staticmethod
    def calculate_outs(hole_cards: List[Card], board: List[Card], 
                        target_rank: HandRank = HandRank.ONE_PAIR) -> List[Card]:
        """计算补牌（可以改进牌型的牌）
        
        Args:
            hole_cards: 底牌
            board: 公共牌
            target_rank: 目标牌型
        
        Returns:
            能使牌型达到目标的补牌列表
        """
        current_hand = TexasHoldem.evaluate_hand(hole_cards, board)
        if current_hand.rank >= target_rank:
            return []  # 已经达到目标
        
        # 创建剩余牌组
        deck = Deck()
        used_cards = set(hole_cards + board)
        remaining = [c for c in deck._cards if c not in used_cards]
        
        outs = []
        for card in remaining:
            new_hand = TexasHoldem.evaluate_hand(hole_cards, board + [card])
            if new_hand.rank >= target_rank and new_hand.rank > current_hand.rank:
                outs.append(card)
        
        return outs
    
    @staticmethod
    def calculate_outs_count(hole_cards: List[Card], board: List[Card],
                            target_rank: HandRank = HandRank.ONE_PAIR) -> int:
        """计算补牌数量
        
        Args:
            hole_cards: 底牌
            board: 公共牌
            target_rank: 目标牌型
        
        Returns:
            补牌数量
        """
        return len(TexasHoldem.calculate_outs(hole_cards, board, target_rank))


class HandAnalyzer:
    """手牌分析器"""
    
    @staticmethod
    def get_possible_straights(cards: List[Card]) -> List[List[Rank]]:
        """获取可能的顺子补牌
        
        Args:
            cards: 当前手牌
        
        Returns:
            可能的顺子列表（每项为缺失的点数列表）
        """
        ranks = set(c.rank for c in cards)
        possible = []
        
        # 检查所有可能的顺子
        straights = [
            [Rank.ACE, Rank.KING, Rank.QUEEN, Rank.JACK, Rank.TEN],  # A-K-Q-J-T
            [Rank.KING, Rank.QUEEN, Rank.JACK, Rank.TEN, Rank.NINE],
            [Rank.QUEEN, Rank.JACK, Rank.TEN, Rank.NINE, Rank.EIGHT],
            [Rank.JACK, Rank.TEN, Rank.NINE, Rank.EIGHT, Rank.SEVEN],
            [Rank.TEN, Rank.NINE, Rank.EIGHT, Rank.SEVEN, Rank.SIX],
            [Rank.NINE, Rank.EIGHT, Rank.SEVEN, Rank.SIX, Rank.FIVE],
            [Rank.EIGHT, Rank.SEVEN, Rank.SIX, Rank.FIVE, Rank.FOUR],
            [Rank.SEVEN, Rank.SIX, Rank.FIVE, Rank.FOUR, Rank.THREE],
            [Rank.SIX, Rank.FIVE, Rank.FOUR, Rank.THREE, Rank.TWO],
            [Rank.FIVE, Rank.FOUR, Rank.THREE, Rank.TWO, Rank.ACE],  # 轮子 A-2-3-4-5
        ]
        
        for straight in straights:
            missing = [r for r in straight if r not in ranks]
            if len(missing) <= 2:  # 最多缺2张才考虑
                possible.append(missing)
        
        return possible
    
    @staticmethod
    def get_possible_flushes(cards: List[Card]) -> List[Tuple[Suit, int]]:
        """获取可能的同花补牌
        
        Args:
            cards: 当前手牌
        
        Returns:
            [(花色, 缺少张数), ...]
        """
        suit_counts = Counter(c.suit for c in cards)
        possible = [(suit, 5 - count) for suit, count in suit_counts.items() if count >= 3]
        return sorted(possible, key=lambda x: x[1])


# ============== 工具函数 ==============

def create_deck(shuffled: bool = True) -> Deck:
    """创建并返回一副牌
    
    Args:
        shuffled: 是否洗牌
    
    Returns:
        Deck 对象
    """
    deck = Deck()
    if shuffled:
        deck.shuffle()
    return deck


def parse_cards(cards_str: str) -> List[Card]:
    """解析牌字符串为 Card 列表
    
    Args:
        cards_str: 牌字符串，如 'Ah Ks Qd Jc Th'
    
    Returns:
        Card 列表
    """
    parts = cards_str.strip().split()
    return [Card.from_str(p) for p in parts]


def cards_to_str(cards: List[Card]) -> str:
    """将 Card 列表转为字符串
    
    Args:
        cards: Card 列表
    
    Returns:
        牌字符串
    """
    return ' '.join(str(c) for c in cards)


def evaluate_hand(cards: List[Card]) -> Hand:
    """评估牌型（快捷函数）
    
    Args:
        cards: 牌列表（5-7张）
    
    Returns:
        最佳牌型
    """
    return PokerEvaluator.evaluate(cards)


def compare_hands(cards1: List[Card], cards2: List[Card]) -> int:
    """比较两组牌
    
    Args:
        cards1: 第一组牌
        cards2: 第二组牌
    
    Returns:
        1: cards1胜, -1: cards2胜, 0: 平局
    """
    hand1 = PokerEvaluator.evaluate(cards1)
    hand2 = PokerEvaluator.evaluate(cards2)
    return PokerEvaluator.compare_hands(hand1, hand2)


def get_hand_rank_name(hand: Hand) -> str:
    """获取牌型名称
    
    Args:
        hand: Hand 对象
    
    Returns:
        牌型中文名称
    """
    return HAND_RANK_NAMES[hand.rank]


def simulate_win_rate(hole_cards: List[Card], board: List[Card] = None,
                     num_players: int = 2, simulations: int = 1000) -> float:
    """模拟胜率（蒙特卡洛方法）
    
    Args:
        hole_cards: 底牌
        board: 已知公共牌
        num_players: 玩家数量
        simulations: 模拟次数
    
    Returns:
        胜率（0-1之间的浮点数）
    """
    if board is None:
        board = []
    
    deck = Deck()
    used = set(hole_cards + board)
    deck._cards = [c for c in deck._cards if c not in used]
    
    wins = 0
    ties = 0
    
    for _ in range(simulations):
        deck.shuffle()
        remaining = deck._cards.copy()
        
        # 发完公共牌
        sim_board = board + remaining[:max(0, 5 - len(board))]
        board_cards_needed = 5 - len(board)
        remaining = remaining[board_cards_needed:]
        
        # 发其他玩家的底牌
        opponents = []
        for _ in range(num_players - 1):
            opponents.append(remaining[:2])
            remaining = remaining[2:]
        
        # 评估
        my_hand = TexasHoldem.evaluate_hand(hole_cards, sim_board)
        opp_hands = [TexasHoldem.evaluate_hand(opp, sim_board) for opp in opponents]
        
        best_opp = max(opp_hands) if opp_hands else None
        
        if best_opp is None or my_hand > best_opp:
            wins += 1
        elif my_hand == best_opp:
            ties += 1
    
    return (wins + ties * 0.5) / simulations


def is_pocket_pair(hole_cards: List[Card]) -> bool:
    """判断是否为口袋对子
    
    Args:
        hole_cards: 底牌（2张）
    
    Returns:
        是否为口袋对子
    """
    return len(hole_cards) == 2 and hole_cards[0].rank == hole_cards[1].rank


def is_suited(hole_cards: List[Card]) -> bool:
    """判断底牌是否同花
    
    Args:
        hole_cards: 底牌（2张）
    
    Returns:
        是否同花
    """
    return len(hole_cards) == 2 and hole_cards[0].suit == hole_cards[1].suit


def is_connected(hole_cards: List[Card], gap: int = 1) -> bool:
    """判断底牌是否相连（可用于判断顺子潜力）
    
    Args:
        hole_cards: 底牌（2张）
        gap: 允许的间隔（默认1表示相邻）
    
    Returns:
        是否相连
    """
    if len(hole_cards) != 2:
        return False
    
    r1, r2 = hole_cards[0].rank, hole_cards[1].rank
    return abs(r1 - r2) <= gap


def get_starting_hand_strength(hole_cards: List[Card]) -> str:
    """评估起手牌强度（简单版本）
    
    Args:
        hole_cards: 底牌（2张）
    
    Returns:
        牌力等级: 'premium', 'strong', 'medium', 'weak', 'trash'
    """
    if len(hole_cards) != 2:
        raise ValueError("起手牌必须是2张")
    
    ranks = sorted([c.rank for c in hole_cards], reverse=True)
    suited = is_suited(hole_cards)
    paired = is_pocket_pair(hole_cards)
    
    # Premium: AA, KK, QQ, AKs
    if paired and ranks[0] >= Rank.QUEEN:
        return 'premium'
    if ranks == [Rank.ACE, Rank.KING] and suited:
        return 'premium'
    
    # Strong: JJ, TT, AKo, AQs, KQs
    if paired and ranks[0] >= Rank.TEN:
        return 'strong'
    if ranks == [Rank.ACE, Rank.KING]:
        return 'strong'
    if ranks == [Rank.ACE, Rank.QUEEN] and suited:
        return 'strong'
    if ranks == [Rank.KING, Rank.QUEEN] and suited:
        return 'strong'
    
    # Medium: 99-22, AQo, AJs, KQo, QJs
    if paired:
        return 'medium'
    if ranks == [Rank.ACE, Rank.QUEEN]:
        return 'medium'
    if ranks == [Rank.ACE, Rank.JACK] and suited:
        return 'medium'
    if ranks == [Rank.KING, Rank.QUEEN]:
        return 'medium'
    if ranks == [Rank.QUEEN, Rank.JACK] and suited:
        return 'medium'
    
    # Weak: AXs, KJs, QTs+, connected suited
    if ranks[0] == Rank.ACE and suited:
        return 'weak'
    if ranks == [Rank.KING, Rank.JACK] and suited:
        return 'weak'
    if ranks[0] == Rank.QUEEN and ranks[1] >= Rank.TEN and suited:
        return 'weak'
    if is_connected(hole_cards, gap=1) and suited:
        return 'weak'
    
    # Trash: everything else
    return 'trash'