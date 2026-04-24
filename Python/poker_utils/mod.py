"""
扑克牌工具集 (Poker Utils)
==========================

零外部依赖的扑克牌处理工具，支持：
- 创建牌组、洗牌、发牌
- 牌型判断（高牌到皇家同花顺）
- 手牌比较和胜负判定
- 概率计算

作者: AllToolkit 自动生成
日期: 2026-04-24
"""

from typing import List, Tuple, Optional, Dict, Set
from enum import IntEnum
from collections import Counter
import random


# ==================== 常量定义 ====================

class Suit(IntEnum):
    """花色枚举"""
    CLUBS = 0      # ♣ 梅花
    DIAMONDS = 1   # ♦ 方块
    HEARTS = 2     # ♥ 红心
    SPADES = 3     # ♠ 黑桃


class Rank(IntEnum):
    """牌面大小枚举"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11      # J
    QUEEN = 12     # Q
    KING = 13      # K
    ACE = 14       # A (默认为14，A可作为1用于顺子)


class HandRank(IntEnum):
    """牌型等级"""
    HIGH_CARD = 0       # 高牌
    ONE_PAIR = 1        # 一对
    TWO_PAIR = 2        # 两对
    THREE_OF_A_KIND = 3 # 三条
    STRAIGHT = 4        # 顺子
    FLUSH = 5           # 同花
    FULL_HOUSE = 6      # 葫芦
    FOUR_OF_A_KIND = 7  # 四条
    STRAIGHT_FLUSH = 8  # 同花顺
    ROYAL_FLUSH = 9     # 皇家同花顺


# 花色符号映射
SUIT_SYMBOLS = {
    Suit.CLUBS: '♣',
    Suit.DIAMONDS: '♦',
    Suit.HEARTS: '♥',
    Suit.SPADES: '♠'
}

SUIT_NAMES = {
    Suit.CLUBS: '梅花',
    Suit.DIAMONDS: '方块',
    Suit.HEARTS: '红心',
    Suit.SPADES: '黑桃'
}

# 牌面符号映射
RANK_SYMBOLS = {
    Rank.TWO: '2',
    Rank.THREE: '3',
    Rank.FOUR: '4',
    Rank.FIVE: '5',
    Rank.SIX: '6',
    Rank.SEVEN: '7',
    Rank.EIGHT: '8',
    Rank.NINE: '9',
    Rank.TEN: '10',
    Rank.JACK: 'J',
    Rank.QUEEN: 'Q',
    Rank.KING: 'K',
    Rank.ACE: 'A'
}

RANK_NAMES = {
    Rank.TWO: '2',
    Rank.THREE: '3',
    Rank.FOUR: '4',
    Rank.FIVE: '5',
    Rank.SIX: '6',
    Rank.SEVEN: '7',
    Rank.EIGHT: '8',
    Rank.NINE: '9',
    Rank.TEN: '10',
    Rank.JACK: 'J',
    Rank.QUEEN: 'Q',
    Rank.KING: 'K',
    Rank.ACE: 'A'
}

HAND_RANK_NAMES = {
    HandRank.HIGH_CARD: '高牌',
    HandRank.ONE_PAIR: '一对',
    HandRank.TWO_PAIR: '两对',
    HandRank.THREE_OF_A_KIND: '三条',
    HandRank.STRAIGHT: '顺子',
    HandRank.FLUSH: '同花',
    HandRank.FULL_HOUSE: '葫芦',
    HandRank.FOUR_OF_A_KIND: '四条',
    HandRank.STRAIGHT_FLUSH: '同花顺',
    HandRank.ROYAL_FLUSH: '皇家同花顺'
}


# ==================== Card 类 ====================

class Card:
    """扑克牌类"""
    
    def __init__(self, suit: Suit, rank: Rank):
        """
        初始化一张牌
        
        Args:
            suit: 花色
            rank: 牌面大小
        """
        self.suit = suit
        self.rank = rank
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"{RANK_SYMBOLS[self.rank]}{SUIT_SYMBOLS[self.suit]}"
    
    def __str__(self) -> str:
        """中文字符串表示"""
        return f"{SUIT_NAMES[self.suit]}{RANK_NAMES[self.rank]}"
    
    def __eq__(self, other) -> bool:
        """判断两张牌是否相同"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __lt__(self, other) -> bool:
        """比较大小（先比牌面，再比花色）"""
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.suit < other.suit
    
    def __hash__(self) -> int:
        """哈希值"""
        return hash((self.suit, self.rank))
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'suit': self.suit.name,
            'rank': self.rank.name,
            'symbol': repr(self),
            'chinese': str(self)
        }
    
    @classmethod
    def from_string(cls, s: str) -> 'Card':
        """
        从字符串解析牌
        
        Args:
            s: 牌的字符串表示，如 "A♠" 或 "黑桃A" 或 "SA" (Spade Ace)
        
        Returns:
            Card 对象
        
        Examples:
            >>> Card.from_string("A♠")
            Card(HEARTS, ACE)  # 注意：这里实际返回黑桃A
            >>> Card.from_string("SA")  # S=Spade, A=Ace
            Card(SPADES, ACE)
        """
        s = s.strip().upper()
        
        # 尝试解析花色符号
        suit_map = {
            '♣': Suit.CLUBS, 'C': Suit.CLUBS,
            '♦': Suit.DIAMONDS, 'D': Suit.DIAMONDS,
            '♥': Suit.HEARTS, 'H': Suit.HEARTS,
            '♠': Suit.SPADES, 'S': Suit.SPADES
        }
        
        # 尝试解析牌面
        rank_map = {
            '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR,
            '5': Rank.FIVE, '6': Rank.SIX, '7': Rank.SEVEN,
            '8': Rank.EIGHT, '9': Rank.NINE, '10': Rank.TEN,
            'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE
        }
        
        suit = None
        rank = None
        
        # 解析花色
        for char in s:
            if char in suit_map:
                suit = suit_map[char]
                break
        
        # 解析牌面
        for r, rank_val in rank_map.items():
            if r in s:
                rank = rank_val
                break
        
        if suit is None or rank is None:
            raise ValueError(f"无法解析牌: {s}")
        
        return cls(suit, rank)


# ==================== Deck 类 ====================

class Deck:
    """牌组类"""
    
    def __init__(self, cards: Optional[List[Card]] = None):
        """
        初始化牌组
        
        Args:
            cards: 可选的初始牌列表
        """
        if cards is None:
            self.cards = self._create_standard_deck()
        else:
            self.cards = list(cards)
    
    def _create_standard_deck(self) -> List[Card]:
        """创建标准52张牌组"""
        return [Card(suit, rank) 
                for suit in Suit 
                for rank in Rank]
    
    def shuffle(self) -> 'Deck':
        """洗牌（原地修改）"""
        random.shuffle(self.cards)
        return self
    
    def draw(self, n: int = 1) -> List[Card]:
        """
        从牌组顶部抽牌
        
        Args:
            n: 抽牌数量
        
        Returns:
            抽出的牌列表
        """
        if n > len(self.cards):
            raise ValueError(f"牌组只有 {len(self.cards)} 张牌，无法抽 {n} 张")
        
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn
    
    def draw_one(self) -> Card:
        """抽一张牌"""
        if not self.cards:
            raise ValueError("牌组已空")
        return self.cards.pop(0)
    
    def add_card(self, card: Card) -> 'Deck':
        """添加一张牌到牌组底部"""
        self.cards.append(card)
        return self
    
    def add_cards(self, cards: List[Card]) -> 'Deck':
        """添加多张牌到牌组底部"""
        self.cards.extend(cards)
        return self
    
    def reset(self) -> 'Deck':
        """重置牌组为完整的52张牌"""
        self.cards = self._create_standard_deck()
        return self
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __repr__(self) -> str:
        return f"Deck({len(self.cards)} cards)"
    
    def __iter__(self):
        return iter(self.cards)
    
    def remaining(self) -> int:
        """剩余牌数"""
        return len(self.cards)
    
    def is_empty(self) -> bool:
        """牌组是否为空"""
        return len(self.cards) == 0
    
    def peek(self, n: int = 1) -> List[Card]:
        """查看牌组顶部的牌（不抽走）"""
        return self.cards[:n]
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'count': len(self.cards),
            'cards': [c.to_dict() for c in self.cards]
        }


# ==================== Hand 类 ====================

class Hand:
    """手牌类"""
    
    def __init__(self, cards: List[Card]):
        """
        初始化手牌
        
        Args:
            cards: 手牌列表（通常为5张）
        """
        self.cards = sorted(cards, key=lambda c: (c.rank, c.suit), reverse=True)
        self._rank_cache: Optional[Tuple[HandRank, List[int]]] = None
    
    def evaluate(self) -> Tuple[HandRank, List[int]]:
        """
        评估手牌牌型
        
        Returns:
            (牌型等级, 用于比较的关键牌值列表)
        """
        if self._rank_cache is not None:
            return self._rank_cache
        
        if len(self.cards) != 5:
            raise ValueError("必须为5张牌才能评估牌型")
        
        ranks = [c.rank for c in self.cards]
        suits = [c.suit for c in self.cards]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        # 检查是否为同花
        is_flush = len(suit_counts) == 1
        
        # 检查是否为顺子
        is_straight, straight_high = self._check_straight(ranks)
        
        # 统计牌型
        count_values = sorted(rank_counts.values(), reverse=True)
        
        # 判断牌型
        if is_straight and is_flush:
            if straight_high == Rank.ACE:
                result = (HandRank.ROYAL_FLUSH, [straight_high])
            else:
                result = (HandRank.STRAIGHT_FLUSH, [straight_high])
        elif count_values == [4, 1]:
            # 四条：4张相同 + 1张散牌
            four_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            result = (HandRank.FOUR_OF_A_KIND, [four_rank, kicker])
        elif count_values == [3, 2]:
            # 葫芦：3张相同 + 2张相同
            three_rank = [r for r, c in rank_counts.items() if c == 3][0]
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            result = (HandRank.FULL_HOUSE, [three_rank, pair_rank])
        elif is_flush:
            result = (HandRank.FLUSH, sorted(ranks, reverse=True))
        elif is_straight:
            result = (HandRank.STRAIGHT, [straight_high])
        elif count_values == [3, 1, 1]:
            # 三条：3张相同 + 2张散牌
            three_rank = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            result = (HandRank.THREE_OF_A_KIND, [three_rank] + kickers)
        elif count_values == [2, 2, 1]:
            # 两对：2对 + 1张散牌
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            result = (HandRank.TWO_PAIR, pairs + [kicker])
        elif count_values == [2, 1, 1, 1]:
            # 一对：2张相同 + 3张散牌
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            result = (HandRank.ONE_PAIR, [pair_rank] + kickers)
        else:
            # 高牌
            result = (HandRank.HIGH_CARD, sorted(ranks, reverse=True))
        
        self._rank_cache = result
        return result
    
    def _check_straight(self, ranks: List[Rank]) -> Tuple[bool, Optional[Rank]]:
        """
        检查是否为顺子
        
        Returns:
            (是否为顺子, 顺子最高牌)
        """
        unique_ranks = sorted(set(ranks))
        
        if len(unique_ranks) != 5:
            return False, None
        
        # 检查普通顺子
        if unique_ranks[-1] - unique_ranks[0] == 4:
            return True, unique_ranks[-1]
        
        # 检查 A-2-3-4-5 特殊顺子（轮子）
        if set(unique_ranks) == {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE}:
            return True, Rank.FIVE  # 轮子的最高牌是5
        
        return False, None
    
    def get_rank_name(self) -> str:
        """获取牌型名称"""
        rank, _ = self.evaluate()
        return HAND_RANK_NAMES[rank]
    
    def compare(self, other: 'Hand') -> int:
        """
        比较两手牌
        
        Returns:
            >0: 当前手牌赢
            <0: 当前手牌输
            0: 平局
        """
        my_rank, my_values = self.evaluate()
        other_rank, other_values = other.evaluate()
        
        # 先比较牌型
        if my_rank != other_rank:
            return my_rank - other_rank
        
        # 牌型相同，比较关键牌
        for my_val, other_val in zip(my_values, other_values):
            if my_val != other_val:
                return my_val - other_val
        
        return 0
    
    def __gt__(self, other: 'Hand') -> bool:
        return self.compare(other) > 0
    
    def __lt__(self, other: 'Hand') -> bool:
        return self.compare(other) < 0
    
    def __eq__(self, other: 'Hand') -> bool:
        return self.compare(other) == 0
    
    def __repr__(self) -> str:
        cards_str = ' '.join(repr(c) for c in self.cards)
        return f"Hand({cards_str})"
    
    def __str__(self) -> str:
        return f"{self.get_rank_name()}: {' '.join(str(c) for c in self.cards)}"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        rank, values = self.evaluate()
        return {
            'cards': [c.to_dict() for c in self.cards],
            'hand_rank': rank.name,
            'hand_rank_name': HAND_RANK_NAMES[rank],
            'key_values': [int(v) for v in values]
        }


# ==================== 工具函数 ====================

def create_deck() -> Deck:
    """创建新的牌组"""
    return Deck()


def shuffle_deck(deck: Deck) -> Deck:
    """洗牌"""
    return deck.shuffle()


def deal_hands(deck: Deck, num_players: int, cards_per_hand: int = 5) -> List[Hand]:
    """
    发牌给多个玩家
    
    Args:
        deck: 牌组
        num_players: 玩家数量
        cards_per_hand: 每位玩家的牌数
    
    Returns:
        手牌列表
    """
    hands = []
    for _ in range(num_players):
        cards = deck.draw(cards_per_hand)
        hands.append(Hand(cards))
    return hands


def evaluate_hand(cards: List[Card]) -> Tuple[HandRank, List[int]]:
    """
    评估手牌牌型
    
    Args:
        cards: 5张牌的列表
    
    Returns:
        (牌型等级, 关键牌值列表)
    """
    return Hand(cards).evaluate()


def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
    """
    比较两手牌
    
    Args:
        hand1: 第一手牌
        hand2: 第二手牌
    
    Returns:
        >0: hand1赢, <0: hand2赢, 0:平局
    """
    return Hand(hand1).compare(Hand(hand2))


def best_hand(seven_cards: List[Card]) -> Hand:
    """
    从7张牌中选出最佳的5张牌组合（德州扑克场景）
    
    Args:
        seven_cards: 7张牌（2张手牌 + 5张公共牌）
    
    Returns:
        最佳的5张牌手牌
    """
    from itertools import combinations
    
    if len(seven_cards) < 5:
        raise ValueError("需要至少5张牌")
    
    if len(seven_cards) == 5:
        return Hand(seven_cards)
    
    best = None
    for combo in combinations(seven_cards, 5):
        current = Hand(list(combo))
        if best is None or current > best:
            best = current
    
    return best


def hand_probability(hand_rank: HandRank) -> float:
    """
    获取牌型概率（在5张随机牌中出现的概率）
    
    Args:
        hand_rank: 牌型等级
    
    Returns:
        概率百分比
    """
    # 标准52张牌中随机抽取5张的牌型概率
    probabilities = {
        HandRank.ROYAL_FLUSH: 0.000154,      # 约1/649,740
        HandRank.STRAIGHT_FLUSH: 0.00139,    # 约1/72,193
        HandRank.FOUR_OF_A_KIND: 0.0240,    # 约1/4,165
        HandRank.FULL_HOUSE: 0.1441,         # 约1/694
        HandRank.FLUSH: 0.1965,              # 约1/509
        HandRank.STRAIGHT: 0.3925,           # 约1/255
        HandRank.THREE_OF_A_KIND: 2.1128,    # 约1/47
        HandRank.TWO_PAIR: 4.7539,            # 约1/21
        HandRank.ONE_PAIR: 42.2569,           # 约1/2.4
        HandRank.HIGH_CARD: 50.1177,          # 约1/2
    }
    return probabilities.get(hand_rank, 0.0)


def hand_combinations_count(hand_rank: HandRank) -> int:
    """
    获取牌型的组合数
    
    Args:
        hand_rank: 牌型等级
    
    Returns:
        可能的组合数
    """
    counts = {
        HandRank.ROYAL_FLUSH: 4,           # 4种花色
        HandRank.STRAIGHT_FLUSH: 36,       # 4花色 × 9种顺子（不含皇家）
        HandRank.FOUR_OF_A_KIND: 624,
        HandRank.FULL_HOUSE: 3744,
        HandRank.FLUSH: 5108,
        HandRank.STRAIGHT: 10200,
        HandRank.THREE_OF_A_KIND: 54912,
        HandRank.TWO_PAIR: 123552,
        HandRank.ONE_PAIR: 1098240,
        HandRank.HIGH_CARD: 1302540,
    }
    return counts.get(hand_rank, 0)


def cards_to_string(cards: List[Card], chinese: bool = False) -> str:
    """
    将牌列表转换为字符串
    
    Args:
        cards: 牌列表
        chinese: 是否使用中文
    
    Returns:
        牌的字符串表示
    """
    if chinese:
        return ' '.join(str(c) for c in cards)
    return ' '.join(repr(c) for c in cards)


def string_to_cards(s: str) -> List[Card]:
    """
    从字符串解析多张牌
    
    Args:
        s: 牌的字符串，如 "A♠ K♠ Q♠ J♠ 10♠"
    
    Returns:
        Card 列表
    """
    # 按空格分割，处理10需要两位的情况
    parts = s.split()
    cards = []
    
    i = 0
    while i < len(parts):
        part = parts[i]
        # 如果是"10"后面可能跟着花色
        if part == '10' and i + 1 < len(parts):
            # 合并
            part = '10' + parts[i + 1]
            i += 2
        else:
            i += 1
        
        cards.append(Card.from_string(part))
    
    return cards


def get_all_cards() -> List[Card]:
    """获取所有52张牌"""
    return [Card(suit, rank) for suit in Suit for rank in Rank]


def card_count_by_rank(cards: List[Card]) -> Dict[Rank, int]:
    """统计各牌面出现的次数"""
    return dict(Counter(c.rank for c in cards))


def card_count_by_suit(cards: List[Card]) -> Dict[Suit, int]:
    """统计各花色出现的次数"""
    return dict(Counter(c.suit for c in cards))


# ==================== 游戏辅助类 ====================

class PokerGame:
    """扑克游戏辅助类"""
    
    def __init__(self, num_players: int = 2):
        """
        初始化游戏
        
        Args:
            num_players: 玩家数量
        """
        self.num_players = num_players
        self.deck = Deck()
        self.hands: List[Hand] = []
        self.community_cards: List[Card] = []
    
    def new_round(self) -> 'PokerGame':
        """开始新一轮"""
        self.deck.reset().shuffle()
        self.hands = []
        self.community_cards = []
        return self
    
    def deal_to_players(self, cards_per_player: int = 2) -> 'PokerGame':
        """给每位玩家发牌"""
        for _ in range(self.num_players):
            self.hands.append(Hand(self.deck.draw(cards_per_player)))
        return self
    
    def deal_community(self, count: int) -> List[Card]:
        """发公共牌"""
        cards = self.deck.draw(count)
        self.community_cards.extend(cards)
        return cards
    
    def flop(self) -> List[Card]:
        """翻牌（发3张公共牌）"""
        return self.deal_community(3)
    
    def turn(self) -> Card:
        """转牌（发1张公共牌）"""
        return self.deal_community(1)[0]
    
    def river(self) -> Card:
        """河牌（发1张公共牌）"""
        return self.deal_community(1)[0]
    
    def get_player_hand(self, player_index: int) -> Hand:
        """获取玩家的完整手牌（手牌+公共牌）"""
        if player_index >= len(self.hands):
            raise IndexError(f"玩家索引 {player_index} 超出范围")
        
        all_cards = list(self.hands[player_index].cards) + self.community_cards
        return best_hand(all_cards)
    
    def get_winner(self) -> Tuple[Optional[int], List[Hand]]:
        """
        获取赢家
        
        Returns:
            (赢家索引, 所有玩家的最佳手牌列表)
            如果平局返回 None
        """
        if not self.hands:
            return None, []
        
        best_hands = []
        for i in range(len(self.hands)):
            all_cards = list(self.hands[i].cards) + self.community_cards
            best_hands.append(best_hand(all_cards))
        
        # 找出最佳手牌
        winner_idx = 0
        is_tie = False
        
        for i in range(1, len(best_hands)):
            comparison = best_hands[i].compare(best_hands[winner_idx])
            if comparison > 0:
                winner_idx = i
                is_tie = False
            elif comparison == 0:
                is_tie = True
        
        if is_tie:
            return None, best_hands
        
        return winner_idx, best_hands
    
    def __repr__(self) -> str:
        return f"PokerGame(players={self.num_players}, deck={len(self.deck)} cards)"


# ==================== 示例用法 ====================

if __name__ == "__main__":
    # 创建并洗牌
    deck = create_deck()
    deck.shuffle()
    print(f"牌组: {deck}")
    
    # 发牌
    hands = deal_hands(deck, num_players=4, cards_per_hand=5)
    
    print("\n玩家手牌:")
    for i, hand in enumerate(hands):
        print(f"  玩家{i+1}: {hand} -> {hand.get_rank_name()}")
    
    # 评估特定手牌
    print("\n特定手牌测试:")
    # 皇家同花顺
    royal_flush = Hand([
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.SPADES, Rank.KING),
        Card(Suit.SPADES, Rank.QUEEN),
        Card(Suit.SPADES, Rank.JACK),
        Card(Suit.SPADES, Rank.TEN),
    ])
    print(f"  皇家同花顺: {royal_flush.get_rank_name()}")
    
    # 四条
    four_kind = Hand([
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.ACE),
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.KING),
    ])
    print(f"  四条: {four_kind.get_rank_name()}")
    
    # 牌型概率
    print("\n牌型概率:")
    for rank in HandRank:
        prob = hand_probability(rank)
        count = hand_combinations_count(rank)
        print(f"  {HAND_RANK_NAMES[rank]}: {prob:.4f}% ({count:,} 种组合)")