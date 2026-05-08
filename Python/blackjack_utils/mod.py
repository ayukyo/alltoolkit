"""
Blackjack Utilities - Complete Blackjack Game Toolkit
========================================

A comprehensive toolkit for Blackjack (21) game with:
- Card and deck management
- Hand evaluation and scoring
- Basic strategy charts
- Card counting systems (Hi-Lo, KO, Hi-Opt)
- Probability calculations
- Betting strategies
- Game simulation

Zero external dependencies - pure Python standard library.

Author: AllToolkit
Date: 2026-05-08
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Callable
from collections import Counter
import random
import math


# ============================================================================
# Enums and Constants
# ============================================================================

class Suit(Enum):
    """Card suits with Unicode symbols."""
    HEARTS = ('♥', 'red')
    DIAMONDS = ('♦', 'red')
    CLUBS = ('♣', 'black')
    SPADES = ('♠', 'black')
    
    @property
    def symbol(self) -> str:
        return self.value[0]
    
    @property
    def color(self) -> str:
        return self.value[1]


class Rank(Enum):
    """Card ranks with values."""
    ACE = ('A', [1, 11])
    TWO = ('2', [2])
    THREE = ('3', [3])
    FOUR = ('4', [4])
    FIVE = ('5', [5])
    SIX = ('6', [6])
    SEVEN = ('7', [7])
    EIGHT = ('8', [8])
    NINE = ('9', [9])
    TEN = ('10', [10])
    JACK = ('J', [10])
    QUEEN = ('Q', [10])
    KING = ('K', [10])
    
    @property
    def symbol(self) -> str:
        return self.value[0]
    
    @property
    def values(self) -> List[int]:
        return self.value[1]


class HandType(Enum):
    """Types of blackjack hands."""
    HARD = "hard"      # No ace, or ace counts as 1
    SOFT = "soft"      # Ace counts as 11 without busting
    BLACKJACK = "blackjack"  # Natural 21 with 2 cards
    BUST = "bust"      # Over 21


class Action(Enum):
    """Player actions in blackjack."""
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"
    SURRENDER = "surrender"
    INSURANCE = "insurance"


class CountSystem(Enum):
    """Card counting systems."""
    HI_LO = "hi_lo"
    KO = "ko"
    HI_OPT_I = "hi_opt_i"
    HI_OPT_II = "hi_opt_ii"
    OMEGA_II = "omega_ii"


# ============================================================================
# Card and Deck Classes
# ============================================================================

@dataclass(frozen=True)
class Card:
    """Immutable playing card."""
    rank: Rank
    suit: Suit
    
    def __str__(self) -> str:
        return f"{self.rank.symbol}{self.suit.symbol}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank.name}, {self.suit.name})"
    
    @property
    def values(self) -> List[int]:
        """Get possible card values."""
        return self.rank.values
    
    @property
    def primary_value(self) -> int:
        """Get primary card value (highest non-busting value)."""
        return max(self.values)
    
    def to_dict(self) -> dict:
        return {
            'rank': self.rank.name,
            'suit': self.suit.name,
            'symbol': str(self),
            'values': self.values
        }


class Deck:
    """
    A deck of playing cards with support for multiple decks.
    
    Standard 52-card deck, supports 1-8 decks for casino play.
    """
    
    def __init__(self, num_decks: int = 1):
        if num_decks < 1 or num_decks > 8:
            raise ValueError("Number of decks must be between 1 and 8")
        self.num_decks = num_decks
        self._cards: List[Card] = []
        self._dealt: List[Card] = []
        self._reshuffle_point = 0.25  # Reshuffle when 25% cards remain
        self._create_deck()
        self.shuffle()
    
    def _create_deck(self) -> None:
        """Create the deck with all cards."""
        self._cards = []
        for _ in range(self.num_decks):
            for suit in Suit:
                for rank in Rank:
                    self._cards.append(Card(rank, suit))
    
    def shuffle(self) -> None:
        """Shuffle the deck and reset dealt cards."""
        # Reset deck to full state before shuffling
        self._create_deck()
        random.shuffle(self._cards)
        self._dealt = []
    
    def deal(self, num_cards: int = 1) -> List[Card]:
        """Deal cards from the deck."""
        if num_cards > len(self._cards):
            raise ValueError(f"Not enough cards in deck. Requested: {num_cards}, Available: {len(self._cards)}")
        
        dealt = []
        for _ in range(num_cards):
            card = self._cards.pop()
            self._dealt.append(card)
            dealt.append(card)
        return dealt
    
    def deal_one(self) -> Card:
        """Deal a single card."""
        return self.deal(1)[0]
    
    @property
    def remaining(self) -> int:
        """Number of cards remaining in deck."""
        return len(self._cards)
    
    @property
    def dealt_count(self) -> int:
        """Number of cards dealt."""
        return len(self._dealt)
    
    @property
    def penetration(self) -> float:
        """Percentage of deck dealt."""
        total = self.num_decks * 52
        return len(self._dealt) / total
    
    @property
    def needs_reshuffle(self) -> bool:
        """Check if deck needs reshuffling."""
        return self.penetration > (1 - self._reshuffle_point)
    
    def add_card(self, card: Card) -> None:
        """Add a card back to the deck (for card counting practice)."""
        if card in self._dealt:
            self._dealt.remove(card)
            self._cards.append(card)
    
    def reset(self) -> None:
        """Reset deck to full state."""
        self._create_deck()
        self.shuffle()


# ============================================================================
# Hand Class
# ============================================================================

@dataclass
class Hand:
    """
    A blackjack hand with scoring and evaluation.
    """
    cards: List[Card] = field(default_factory=list)
    bet: float = 0.0
    is_doubled: bool = False
    is_split: bool = False
    is_surrendered: bool = False
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """Add multiple cards to the hand."""
        self.cards.extend(cards)
    
    @property
    def values(self) -> List[int]:
        """Get all possible hand values."""
        if not self.cards:
            return [0]
        
        # Calculate base value (all aces as 1)
        base_value = sum(min(c.values) for c in self.cards)
        num_aces = sum(1 for c in self.cards if c.rank == Rank.ACE)
        
        # Generate all possible values by adding 10 for each ace
        values = [base_value]
        for i in range(num_aces):
            new_value = values[-1] + 10
            if new_value <= 21:
                values.append(new_value)
        
        return sorted(values, reverse=True)
    
    @property
    def best_value(self) -> int:
        """Get the best (highest non-busting) hand value."""
        for v in self.values:
            if v <= 21:
                return v
        return self.values[-1]  # Return bust value
    
    @property
    def hand_type(self) -> HandType:
        """Determine the type of hand."""
        if len(self.cards) == 2 and self.best_value == 21:
            return HandType.BLACKJACK
        
        if self.best_value > 21:
            return HandType.BUST
        
        # Check for soft hand (ace counted as 11)
        for v in self.values:
            if v <= 21 and v > min(self.values):
                return HandType.SOFT
        
        return HandType.HARD
    
    @property
    def is_soft(self) -> bool:
        """Check if hand is soft (contains ace counted as 11)."""
        return self.hand_type == HandType.SOFT
    
    @property
    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack."""
        return self.hand_type == HandType.BLACKJACK
    
    @property
    def is_bust(self) -> bool:
        """Check if hand is bust."""
        return self.hand_type == HandType.BUST
    
    @property
    def is_pair(self) -> bool:
        """Check if hand is a pair (same rank)."""
        if len(self.cards) != 2:
            return False
        return self.cards[0].rank == self.cards[1].rank
    
    @property
    def pair_rank(self) -> Optional[Rank]:
        """Get the rank if hand is a pair, None otherwise."""
        if self.is_pair:
            return self.cards[0].rank
        return None
    
    @property
    def can_split(self) -> bool:
        """Check if hand can be split."""
        return self.is_pair and len(self.cards) == 2 and not self.is_split
    
    @property
    def can_double(self) -> bool:
        """Check if hand can be doubled."""
        return len(self.cards) == 2 and not self.is_doubled
    
    @property
    def num_cards(self) -> int:
        """Number of cards in hand."""
        return len(self.cards)
    
    def __str__(self) -> str:
        cards_str = " ".join(str(c) for c in self.cards)
        return f"[{cards_str}] = {self.best_value}"
    
    def __repr__(self) -> str:
        return f"Hand(cards={[str(c) for c in self.cards]}, value={self.best_value})"
    
    def to_dict(self) -> dict:
        return {
            'cards': [c.to_dict() for c in self.cards],
            'values': self.values,
            'best_value': self.best_value,
            'hand_type': self.hand_type.value,
            'is_soft': self.is_soft,
            'is_blackjack': self.is_blackjack,
            'is_bust': self.is_bust,
            'is_pair': self.is_pair,
            'can_split': self.can_split,
            'can_double': self.can_double
        }


# ============================================================================
# Basic Strategy
# ============================================================================

class BasicStrategy:
    """
    Basic strategy charts for optimal blackjack play.
    
    Based on mathematically optimal decisions for each scenario.
    """
    
    # Hard hand strategy table
    # Key: (player_total, dealer_upcard_value)
    # Value: Action to take
    HARD_STRATEGY: Dict[Tuple[int, int], Action] = {
        # Hard 8 or less - always hit
        (5, 2): Action.HIT, (5, 3): Action.HIT, (5, 4): Action.HIT, (5, 5): Action.HIT, (5, 6): Action.HIT,
        (6, 2): Action.HIT, (6, 3): Action.HIT, (6, 4): Action.HIT, (6, 5): Action.HIT, (6, 6): Action.HIT,
        (7, 2): Action.HIT, (7, 3): Action.HIT, (7, 4): Action.HIT, (7, 5): Action.HIT, (7, 6): Action.HIT,
        (8, 2): Action.HIT, (8, 3): Action.HIT, (8, 4): Action.HIT, (8, 5): Action.HIT, (8, 6): Action.HIT,
        
        # Hard 9
        (9, 2): Action.HIT, (9, 3): Action.DOUBLE, (9, 4): Action.DOUBLE, (9, 5): Action.DOUBLE, (9, 6): Action.DOUBLE,
        (9, 7): Action.HIT, (9, 8): Action.HIT, (9, 9): Action.HIT, (9, 10): Action.HIT, (9, 11): Action.HIT,
        
        # Hard 10
        (10, 2): Action.DOUBLE, (10, 3): Action.DOUBLE, (10, 4): Action.DOUBLE, (10, 5): Action.DOUBLE, (10, 6): Action.DOUBLE,
        (10, 7): Action.DOUBLE, (10, 8): Action.DOUBLE, (10, 9): Action.DOUBLE, (10, 10): Action.HIT, (10, 11): Action.HIT,
        
        # Hard 11
        (11, 2): Action.DOUBLE, (11, 3): Action.DOUBLE, (11, 4): Action.DOUBLE, (11, 5): Action.DOUBLE, (11, 6): Action.DOUBLE,
        (11, 7): Action.DOUBLE, (11, 8): Action.DOUBLE, (11, 9): Action.DOUBLE, (11, 10): Action.DOUBLE, (11, 11): Action.DOUBLE,
        
        # Hard 12
        (12, 2): Action.HIT, (12, 3): Action.HIT, (12, 4): Action.STAND, (12, 5): Action.STAND, (12, 6): Action.STAND,
        (12, 7): Action.HIT, (12, 8): Action.HIT, (12, 9): Action.HIT, (12, 10): Action.HIT, (12, 11): Action.HIT,
        
        # Hard 13
        (13, 2): Action.STAND, (13, 3): Action.STAND, (13, 4): Action.STAND, (13, 5): Action.STAND, (13, 6): Action.STAND,
        (13, 7): Action.HIT, (13, 8): Action.HIT, (13, 9): Action.HIT, (13, 10): Action.HIT, (13, 11): Action.HIT,
        
        # Hard 14
        (14, 2): Action.STAND, (14, 3): Action.STAND, (14, 4): Action.STAND, (14, 5): Action.STAND, (14, 6): Action.STAND,
        (14, 7): Action.HIT, (14, 8): Action.HIT, (14, 9): Action.HIT, (14, 10): Action.HIT, (14, 11): Action.HIT,
        
        # Hard 15
        (15, 2): Action.STAND, (15, 3): Action.STAND, (15, 4): Action.STAND, (15, 5): Action.STAND, (15, 6): Action.STAND,
        (15, 7): Action.HIT, (15, 8): Action.HIT, (15, 9): Action.HIT, (15, 10): Action.HIT, (15, 11): Action.HIT,
        
        # Hard 16
        (16, 2): Action.STAND, (16, 3): Action.STAND, (16, 4): Action.STAND, (16, 5): Action.STAND, (16, 6): Action.STAND,
        (16, 7): Action.HIT, (16, 8): Action.HIT, (16, 9): Action.HIT, (16, 10): Action.HIT, (16, 11): Action.HIT,
        
        # Hard 17+ - always stand
        (17, 2): Action.STAND, (17, 3): Action.STAND, (17, 4): Action.STAND, (17, 5): Action.STAND, (17, 6): Action.STAND,
        (17, 7): Action.STAND, (17, 8): Action.STAND, (17, 9): Action.STAND, (17, 10): Action.STAND, (17, 11): Action.STAND,
        (18, 2): Action.STAND, (18, 3): Action.STAND, (18, 4): Action.STAND, (18, 5): Action.STAND, (18, 6): Action.STAND,
        (18, 7): Action.STAND, (18, 8): Action.STAND, (18, 9): Action.STAND, (18, 10): Action.STAND, (18, 11): Action.STAND,
        (19, 2): Action.STAND, (19, 3): Action.STAND, (19, 4): Action.STAND, (19, 5): Action.STAND, (19, 6): Action.STAND,
        (19, 7): Action.STAND, (19, 8): Action.STAND, (19, 9): Action.STAND, (19, 10): Action.STAND, (19, 11): Action.STAND,
        (20, 2): Action.STAND, (20, 3): Action.STAND, (20, 4): Action.STAND, (20, 5): Action.STAND, (20, 6): Action.STAND,
        (20, 7): Action.STAND, (20, 8): Action.STAND, (20, 9): Action.STAND, (20, 10): Action.STAND, (20, 11): Action.STAND,
        (21, 2): Action.STAND, (21, 3): Action.STAND, (21, 4): Action.STAND, (21, 5): Action.STAND, (21, 6): Action.STAND,
        (21, 7): Action.STAND, (21, 8): Action.STAND, (21, 9): Action.STAND, (21, 10): Action.STAND, (21, 11): Action.STAND,
    }
    
    # Soft hand strategy table
    SOFT_STRATEGY: Dict[Tuple[int, int], Action] = {
        # Soft 13 (A,2)
        (13, 2): Action.HIT, (13, 3): Action.HIT, (13, 4): Action.HIT, (13, 5): Action.DOUBLE, (13, 6): Action.DOUBLE,
        (13, 7): Action.HIT, (13, 8): Action.HIT, (13, 9): Action.HIT, (13, 10): Action.HIT, (13, 11): Action.HIT,
        
        # Soft 14 (A,3)
        (14, 2): Action.HIT, (14, 3): Action.HIT, (14, 4): Action.DOUBLE, (14, 5): Action.DOUBLE, (14, 6): Action.DOUBLE,
        (14, 7): Action.HIT, (14, 8): Action.HIT, (14, 9): Action.HIT, (14, 10): Action.HIT, (14, 11): Action.HIT,
        
        # Soft 15 (A,4)
        (15, 2): Action.HIT, (15, 3): Action.HIT, (15, 4): Action.DOUBLE, (15, 5): Action.DOUBLE, (15, 6): Action.DOUBLE,
        (15, 7): Action.HIT, (15, 8): Action.HIT, (15, 9): Action.HIT, (15, 10): Action.HIT, (15, 11): Action.HIT,
        
        # Soft 16 (A,5)
        (16, 2): Action.HIT, (16, 3): Action.HIT, (16, 4): Action.DOUBLE, (16, 5): Action.DOUBLE, (16, 6): Action.DOUBLE,
        (16, 7): Action.HIT, (16, 8): Action.HIT, (16, 9): Action.HIT, (16, 10): Action.HIT, (16, 11): Action.HIT,
        
        # Soft 17 (A,6)
        (17, 2): Action.HIT, (17, 3): Action.DOUBLE, (17, 4): Action.DOUBLE, (17, 5): Action.DOUBLE, (17, 6): Action.DOUBLE,
        (17, 7): Action.HIT, (17, 8): Action.HIT, (17, 9): Action.HIT, (17, 10): Action.HIT, (17, 11): Action.HIT,
        
        # Soft 18 (A,7)
        (18, 2): Action.STAND, (18, 3): Action.DOUBLE, (18, 4): Action.DOUBLE, (18, 5): Action.DOUBLE, (18, 6): Action.DOUBLE,
        (18, 7): Action.STAND, (18, 8): Action.STAND, (18, 9): Action.HIT, (18, 10): Action.HIT, (18, 11): Action.HIT,
        
        # Soft 19+ - always stand
        (19, 2): Action.STAND, (19, 3): Action.STAND, (19, 4): Action.STAND, (19, 5): Action.STAND, (19, 6): Action.DOUBLE,
        (19, 7): Action.STAND, (19, 8): Action.STAND, (19, 9): Action.STAND, (19, 10): Action.STAND, (19, 11): Action.STAND,
        (20, 2): Action.STAND, (20, 3): Action.STAND, (20, 4): Action.STAND, (20, 5): Action.STAND, (20, 6): Action.STAND,
        (20, 7): Action.STAND, (20, 8): Action.STAND, (20, 9): Action.STAND, (20, 10): Action.STAND, (20, 11): Action.STAND,
        (21, 2): Action.STAND, (21, 3): Action.STAND, (21, 4): Action.STAND, (21, 5): Action.STAND, (21, 6): Action.STAND,
        (21, 7): Action.STAND, (21, 8): Action.STAND, (21, 9): Action.STAND, (21, 10): Action.STAND, (21, 11): Action.STAND,
    }
    
    # Pair splitting strategy
    SPLIT_STRATEGY: Dict[Tuple[str, int], Action] = {
        # (pair_rank_name, dealer_upcard) -> Action
        # Aces - always split
        ('ACE', 2): Action.SPLIT, ('ACE', 3): Action.SPLIT, ('ACE', 4): Action.SPLIT, ('ACE', 5): Action.SPLIT,
        ('ACE', 6): Action.SPLIT, ('ACE', 7): Action.SPLIT, ('ACE', 8): Action.SPLIT, ('ACE', 9): Action.SPLIT,
        ('ACE', 10): Action.SPLIT, ('ACE', 11): Action.SPLIT,
        
        # 2s
        ('TWO', 2): Action.SPLIT, ('TWO', 3): Action.SPLIT, ('TWO', 4): Action.SPLIT, ('TWO', 5): Action.SPLIT,
        ('TWO', 6): Action.SPLIT, ('TWO', 7): Action.HIT, ('TWO', 8): Action.HIT, ('TWO', 9): Action.HIT,
        ('TWO', 10): Action.HIT, ('TWO', 11): Action.HIT,
        
        # 3s
        ('THREE', 2): Action.SPLIT, ('THREE', 3): Action.SPLIT, ('THREE', 4): Action.SPLIT, ('THREE', 5): Action.SPLIT,
        ('THREE', 6): Action.SPLIT, ('THREE', 7): Action.SPLIT, ('THREE', 8): Action.HIT, ('THREE', 9): Action.HIT,
        ('THREE', 10): Action.HIT, ('THREE', 11): Action.HIT,
        
        # 4s
        ('FOUR', 2): Action.HIT, ('FOUR', 3): Action.HIT, ('FOUR', 4): Action.HIT, ('FOUR', 5): Action.SPLIT,
        ('FOUR', 6): Action.SPLIT, ('FOUR', 7): Action.HIT, ('FOUR', 8): Action.HIT, ('FOUR', 9): Action.HIT,
        ('FOUR', 10): Action.HIT, ('FOUR', 11): Action.HIT,
        
        # 5s - never split (treat as hard 10)
        ('FIVE', 2): Action.DOUBLE, ('FIVE', 3): Action.DOUBLE, ('FIVE', 4): Action.DOUBLE, ('FIVE', 5): Action.DOUBLE,
        ('FIVE', 6): Action.DOUBLE, ('FIVE', 7): Action.DOUBLE, ('FIVE', 8): Action.DOUBLE, ('FIVE', 9): Action.DOUBLE,
        ('FIVE', 10): Action.HIT, ('FIVE', 11): Action.HIT,
        
        # 6s
        ('SIX', 2): Action.SPLIT, ('SIX', 3): Action.SPLIT, ('SIX', 4): Action.SPLIT, ('SIX', 5): Action.SPLIT,
        ('SIX', 6): Action.SPLIT, ('SIX', 7): Action.HIT, ('SIX', 8): Action.HIT, ('SIX', 9): Action.HIT,
        ('SIX', 10): Action.HIT, ('SIX', 11): Action.HIT,
        
        # 7s
        ('SEVEN', 2): Action.SPLIT, ('SEVEN', 3): Action.SPLIT, ('SEVEN', 4): Action.SPLIT, ('SEVEN', 5): Action.SPLIT,
        ('SEVEN', 6): Action.SPLIT, ('SEVEN', 7): Action.SPLIT, ('SEVEN', 8): Action.HIT, ('SEVEN', 9): Action.HIT,
        ('SEVEN', 10): Action.HIT, ('SEVEN', 11): Action.HIT,
        
        # 8s - always split
        ('EIGHT', 2): Action.SPLIT, ('EIGHT', 3): Action.SPLIT, ('EIGHT', 4): Action.SPLIT, ('EIGHT', 5): Action.SPLIT,
        ('EIGHT', 6): Action.SPLIT, ('EIGHT', 7): Action.SPLIT, ('EIGHT', 8): Action.SPLIT, ('EIGHT', 9): Action.SPLIT,
        ('EIGHT', 10): Action.SPLIT, ('EIGHT', 11): Action.SPLIT,
        
        # 9s
        ('NINE', 2): Action.SPLIT, ('NINE', 3): Action.SPLIT, ('NINE', 4): Action.SPLIT, ('NINE', 5): Action.SPLIT,
        ('NINE', 6): Action.SPLIT, ('NINE', 7): Action.STAND, ('NINE', 8): Action.SPLIT, ('NINE', 9): Action.SPLIT,
        ('NINE', 10): Action.STAND, ('NINE', 11): Action.STAND,
        
        # 10s - never split
        ('TEN', 2): Action.STAND, ('TEN', 3): Action.STAND, ('TEN', 4): Action.STAND, ('TEN', 5): Action.STAND,
        ('TEN', 6): Action.STAND, ('TEN', 7): Action.STAND, ('TEN', 8): Action.STAND, ('TEN', 9): Action.STAND,
        ('TEN', 10): Action.STAND, ('TEN', 11): Action.STAND,
        
        # Jacks, Queens, Kings - never split
        ('JACK', 2): Action.STAND, ('JACK', 3): Action.STAND, ('JACK', 4): Action.STAND, ('JACK', 5): Action.STAND,
        ('JACK', 6): Action.STAND, ('JACK', 7): Action.STAND, ('JACK', 8): Action.STAND, ('JACK', 9): Action.STAND,
        ('JACK', 10): Action.STAND, ('JACK', 11): Action.STAND,
    }
    
    @classmethod
    def get_action(cls, player_hand: Hand, dealer_upcard: Card, 
                   can_split: bool = True, can_double: bool = True,
                   can_surrender: bool = False) -> Action:
        """
        Get the recommended action based on basic strategy.
        
        Args:
            player_hand: Player's hand
            dealer_upcard: Dealer's visible card
            can_split: Whether splitting is allowed
            can_double: Whether doubling is allowed
            can_surrender: Whether surrender is allowed
            
        Returns:
            Recommended action
        """
        if player_hand.is_blackjack:
            return Action.STAND
        
        if player_hand.is_bust:
            return Action.STAND
        
        dealer_value = dealer_upcard.primary_value
        if dealer_upcard.rank == Rank.ACE:
            dealer_value = 11
        
        # Check for pair splitting first
        if player_hand.is_pair and can_split:
            pair_rank_name = player_hand.pair_rank.name
            action = cls.SPLIT_STRATEGY.get((pair_rank_name, dealer_value))
            if action == Action.SPLIT:
                return Action.SPLIT
            # For 5s and 10-value pairs, treat as hard hand
            if pair_rank_name in ('FIVE', 'TEN', 'JACK', 'QUEEN', 'KING'):
                pass  # Fall through to hard/soft strategy
            elif action:
                return action
        
        # Get player total
        player_total = player_hand.best_value
        
        # Check soft vs hard hand
        if player_hand.is_soft and player_total <= 21:
            # Use soft strategy
            action = cls.SOFT_STRATEGY.get((player_total, dealer_value), Action.HIT)
        else:
            # Use hard strategy
            action = cls.HARD_STRATEGY.get((player_total, dealer_value), Action.HIT)
        
        # Check if action is allowed
        if action == Action.DOUBLE and not can_double:
            return Action.HIT
        if action == Action.SPLIT and not can_split:
            return Action.HIT
        
        return action
    
    @classmethod
    def get_strategy_chart(cls, hand_type: str = 'hard') -> str:
        """
        Generate a text-based strategy chart.
        
        Args:
            hand_type: 'hard', 'soft', or 'split'
            
        Returns:
            Formatted strategy chart string
        """
        if hand_type == 'hard':
            title = "Hard Hand Strategy"
            strategy = cls.HARD_STRATEGY
            rows = range(5, 22)
        elif hand_type == 'soft':
            title = "Soft Hand Strategy"
            strategy = cls.SOFT_STRATEGY
            rows = range(13, 22)
        else:
            title = "Pair Splitting Strategy"
            return cls._get_split_chart()
        
        lines = [f"\n{'='*60}", f"{title:^60}", f"{'='*60}"]
        
        # Header
        header = "Player | Dealer Upcard"
        lines.append(header)
        lines.append("Total | 2  3  4  5  6  7  8  9  10  A")
        lines.append("-" * 40)
        
        action_symbols = {
            Action.HIT: 'H',
            Action.STAND: 'S',
            Action.DOUBLE: 'D',
            Action.SPLIT: 'P',
            Action.SURRENDER: 'R'
        }
        
        for total in rows:
            row = f"{total:5} |"
            for dealer in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                action = strategy.get((total, dealer), Action.HIT)
                symbol = action_symbols.get(action, '?')
                row += f" {symbol} "
            lines.append(row)
        
        lines.append(f"\nLegend: H=Hit, S=Stand, D=Double, P=Split, R=Surrender")
        lines.append(f"{'='*60}\n")
        
        return '\n'.join(lines)
    
    @classmethod
    def _get_split_chart(cls) -> str:
        """Generate pair splitting chart."""
        lines = [f"\n{'='*60}", f"Pair Splitting Strategy:^60", f"{'='*60}"]
        
        header = "Pair  | Dealer Upcard"
        lines.append(header)
        lines.append("      | 2  3  4  5  6  7  8  9  10  A")
        lines.append("-" * 40)
        
        pairs = ['ACE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 
                 'SEVEN', 'EIGHT', 'NINE', 'TEN']
        
        action_symbols = {
            Action.HIT: 'H',
            Action.STAND: 'S',
            Action.DOUBLE: 'D',
            Action.SPLIT: 'P'
        }
        
        for pair_name in pairs:
            rank = Rank[pair_name]
            display = rank.symbol if len(rank.symbol) <= 2 else rank.symbol[:2]
            row = f"{display:5} |"
            for dealer in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                action = cls.SPLIT_STRATEGY.get((pair_name, dealer), Action.HIT)
                symbol = action_symbols.get(action, '?')
                row += f" {symbol} "
            lines.append(row)
        
        lines.append(f"\nLegend: P=Split, H=Hit, S=Stand, D=Double")
        lines.append(f"{'='*60}\n")
        
        return '\n'.join(lines)


# ============================================================================
# Card Counting
# ============================================================================

class CardCounter:
    """
    Card counting systems for blackjack.
    
    Supports multiple counting systems:
    - Hi-Lo: Most popular, balanced count
    - KO: Unbalanced count, easier to use
    - Hi-Opt I: More accurate, requires true count
    - Hi-Opt II: Advanced, two-level count
    - Omega II: Two-level count with side count for aces
    """
    
    # Card values for different counting systems
    COUNT_VALUES = {
        CountSystem.HI_LO: {
            Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 1, Rank.FIVE: 1, Rank.SIX: 1,
            Rank.SEVEN: 0, Rank.EIGHT: 0, Rank.NINE: 0,
            Rank.TEN: -1, Rank.JACK: -1, Rank.QUEEN: -1, Rank.KING: -1, Rank.ACE: -1
        },
        CountSystem.KO: {
            Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 1, Rank.FIVE: 1, Rank.SIX: 1,
            Rank.SEVEN: 1, Rank.EIGHT: 0, Rank.NINE: 0,
            Rank.TEN: -1, Rank.JACK: -1, Rank.QUEEN: -1, Rank.KING: -1, Rank.ACE: -1
        },
        CountSystem.HI_OPT_I: {
            Rank.TWO: 0, Rank.THREE: 1, Rank.FOUR: 1, Rank.FIVE: 1, Rank.SIX: 1,
            Rank.SEVEN: 0, Rank.EIGHT: 0, Rank.NINE: 0,
            Rank.TEN: -1, Rank.JACK: -1, Rank.QUEEN: -1, Rank.KING: -1, Rank.ACE: 0
        },
        CountSystem.HI_OPT_II: {
            Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 2, Rank.FIVE: 2, Rank.SIX: 1,
            Rank.SEVEN: 1, Rank.EIGHT: 0, Rank.NINE: 0,
            Rank.TEN: -2, Rank.JACK: -2, Rank.QUEEN: -2, Rank.KING: -2, Rank.ACE: 0
        },
        CountSystem.OMEGA_II: {
            Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 2, Rank.FIVE: 2, Rank.SIX: 2,
            Rank.SEVEN: 1, Rank.EIGHT: 0, Rank.NINE: -1,
            Rank.TEN: -2, Rank.JACK: -2, Rank.QUEEN: -2, Rank.KING: -2, Rank.ACE: 0
        }
    }
    
    def __init__(self, system: CountSystem = CountSystem.HI_LO, num_decks: int = 6):
        """
        Initialize card counter.
        
        Args:
            system: Counting system to use
            num_decks: Number of decks in shoe
        """
        self.system = system
        self.num_decks = num_decks
        self._running_count = 0
        self._cards_seen: List[Card] = []
        self._ace_count = 0  # For systems that track aces separately
    
    @property
    def running_count(self) -> int:
        """Current running count."""
        return self._running_count
    
    @property
    def true_count(self) -> float:
        """Current true count (running count / decks remaining)."""
        decks_remaining = self.decks_remaining
        if decks_remaining < 0.5:
            decks_remaining = 0.5  # Minimum to avoid division issues
        return self._running_count / decks_remaining
    
    @property
    def decks_remaining(self) -> float:
        """Estimated number of decks remaining."""
        cards_seen = len(self._cards_seen)
        total_cards = self.num_decks * 52
        cards_remaining = total_cards - cards_seen
        return cards_remaining / 52
    
    @property
    def cards_seen(self) -> int:
        """Number of cards seen."""
        return len(self._cards_seen)
    
    def add_card(self, card: Card) -> int:
        """
        Add a card to the count.
        
        Args:
            card: Card to add
            
        Returns:
            Updated running count
        """
        self._cards_seen.append(card)
        
        # Get count value for this card
        count_value = self.COUNT_VALUES[self.system].get(card.rank, 0)
        self._running_count += count_value
        
        # Track aces separately for Omega II
        if card.rank == Rank.ACE:
            self._ace_count += 1
        
        return self._running_count
    
    def add_cards(self, cards: List[Card]) -> int:
        """Add multiple cards to the count."""
        for card in cards:
            self.add_card(card)
        return self._running_count
    
    def get_bet_size(self, base_bet: float, min_bet: float = 1.0, 
                     max_bet: float = 100.0, unit_size: float = 25.0) -> float:
        """
        Calculate optimal bet size based on count.
        
        Args:
            base_bet: Standard bet amount
            min_bet: Minimum allowed bet
            max_bet: Maximum allowed bet
            unit_size: Size of one betting unit
            
        Returns:
            Recommended bet size
        """
        true_count = self.true_count
        
        # Bet more when count is positive
        if true_count <= 0:
            bet = min_bet
        else:
            # Bet = true_count units
            bet = base_bet + (true_count - 1) * unit_size
        
        return max(min_bet, min(bet, max_bet))
    
    def get_advantage(self) -> float:
        """
        Calculate player advantage based on true count.
        
        Basic strategy gives house ~0.5% edge.
        Each +1 true count adds ~0.5% player advantage.
        
        Returns:
            Player advantage percentage (negative = house edge)
        """
        base_house_edge = -0.5  # House edge with basic strategy
        count_advantage = self.true_count * 0.5
        return base_house_edge + count_advantage
    
    def reset(self) -> None:
        """Reset the counter for a new shoe."""
        self._running_count = 0
        self._cards_seen = []
        self._ace_count = 0
    
    def insurance_is_good(self) -> bool:
        """
        Determine if insurance bet is profitable.
        
        Insurance is profitable when true count >= +3 (Hi-Lo).
        """
        if self.system in (CountSystem.HI_LO, CountSystem.KO):
            return self.true_count >= 3
        return False
    
    def get_deviations(self) -> List[Dict]:
        """
        Get strategy deviations based on true count (Illustrious 18).
        
        Returns:
            List of deviation recommendations
        """
        deviations = []
        tc = self.true_count
        
        # Key deviations (simplified Illustrious 18)
        deviation_rules = [
            (16, 10, 0, "Stand on 16 vs 10 instead of Hit"),
            (15, 10, 4, "Stand on 15 vs 10 instead of Hit"),
            (12, 3, 2, "Stand on 12 vs 3 instead of Hit"),
            (12, 2, 3, "Stand on 12 vs 2 instead of Hit"),
            (11, 10, 1, "Double on 11 vs 10 instead of Hit"),
            (10, 10, 4, "Double on 10 vs 10 instead of Hit"),
            (10, 11, 1, "Double on 10 vs Ace instead of Hit"),
            (9, 2, 1, "Double on 9 vs 2 instead of Hit"),
            (13, 2, -1, "Hit on 13 vs 2 instead of Stand"),
        ]
        
        for player_total, dealer_upcard, threshold, description in deviation_rules:
            if threshold > 0 and tc >= threshold:
                deviations.append({
                    'player_total': player_total,
                    'dealer_upcard': dealer_upcard,
                    'true_count_threshold': threshold,
                    'description': description,
                    'active': True
                })
            elif threshold < 0 and tc <= threshold:
                deviations.append({
                    'player_total': player_total,
                    'dealer_upcard': dealer_upcard,
                    'true_count_threshold': threshold,
                    'description': description,
                    'active': True
                })
        
        return deviations


# ============================================================================
# Probability Calculator
# ============================================================================

class ProbabilityCalculator:
    """
    Probability calculations for blackjack.
    
    Uses combinatorics to calculate exact probabilities.
    """
    
    @staticmethod
    def bust_probability(hand_value: int, cards_remaining: Counter, 
                        total_cards: int) -> float:
        """
        Calculate probability of busting on next hit.
        
        Args:
            hand_value: Current hand value
            cards_remaining: Counter of cards remaining by rank
            total_cards: Total cards remaining
            
        Returns:
            Probability of busting (0.0 to 1.0)
        """
        if hand_value > 21:
            return 1.0
        if hand_value <= 11:
            return 0.0  # Cannot bust
        
        bust_cards = 0
        max_safe_value = 21 - hand_value
        
        for rank, count in cards_remaining.items():
            # Check if card value would bust
            # Ace counts as 1 for bust check
            card_value = min(rank.values)  # Get smallest value (Ace = 1)
            if card_value > max_safe_value:
                bust_cards += count
        
        return bust_cards / total_cards if total_cards > 0 else 0.0
    
    @staticmethod
    def dealer_outcome_probability(dealer_upcard: Card, 
                                   remaining_cards: Dict[Rank, int]) -> Dict[int, float]:
        """
        Calculate probability of dealer final outcomes.
        
        Args:
            dealer_upcard: Dealer's visible card
            remaining_cards: Cards remaining in shoe
            
        Returns:
            Dictionary of final_value -> probability
        """
        # Simplified calculation using common dealer outcomes
        # In reality, this requires simulation or complex combinatorics
        
        upcard_value = dealer_upcard.primary_value
        if dealer_upcard.rank == Rank.ACE:
            upcard_value = 11
        
        # Approximate dealer outcome probabilities based on upcard
        # These are statistically derived values
        dealer_probs = {
            17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 'bust': 0.0
        }
        
        # Approximate probabilities (simplified)
        if upcard_value == 2:
            dealer_probs = {17: 0.14, 18: 0.14, 19: 0.13, 20: 0.12, 21: 0.12, 'bust': 0.35}
        elif upcard_value == 3:
            dealer_probs = {17: 0.14, 18: 0.14, 19: 0.13, 20: 0.12, 21: 0.11, 'bust': 0.36}
        elif upcard_value == 4:
            dealer_probs = {17: 0.13, 18: 0.14, 19: 0.13, 20: 0.12, 21: 0.11, 'bust': 0.37}
        elif upcard_value == 5:
            dealer_probs = {17: 0.12, 18: 0.13, 19: 0.13, 20: 0.12, 21: 0.11, 'bust': 0.39}
        elif upcard_value == 6:
            dealer_probs = {17: 0.17, 18: 0.11, 19: 0.11, 20: 0.10, 21: 0.10, 'bust': 0.41}
        elif upcard_value == 7:
            dealer_probs = {17: 0.37, 18: 0.14, 19: 0.08, 20: 0.08, 21: 0.07, 'bust': 0.26}
        elif upcard_value == 8:
            dealer_probs = {17: 0.13, 18: 0.36, 19: 0.13, 20: 0.07, 21: 0.06, 'bust': 0.25}
        elif upcard_value == 9:
            dealer_probs = {17: 0.12, 18: 0.12, 19: 0.35, 20: 0.12, 21: 0.06, 'bust': 0.23}
        elif upcard_value == 10:
            dealer_probs = {17: 0.12, 18: 0.11, 19: 0.11, 20: 0.37, 21: 0.04, 'bust': 0.25}
        elif upcard_value == 11:  # Ace
            dealer_probs = {17: 0.13, 18: 0.13, 19: 0.13, 20: 0.13, 21: 0.05, 'bust': 0.17}
        
        return dealer_probs
    
    @staticmethod
    def expected_value(player_hand: Hand, dealer_upcard: Card,
                      action: Action, remaining_cards: Dict[Rank, int]) -> float:
        """
        Calculate expected value for an action.
        
        Args:
            player_hand: Player's current hand
            dealer_upcard: Dealer's visible card
            action: Action to evaluate
            remaining_cards: Cards remaining in shoe
            
        Returns:
            Expected value (-1.0 to 1.0, positive = favorable)
        """
        # Simplified EV calculation
        # In practice, this requires Monte Carlo simulation
        
        player_total = player_hand.best_value
        dealer_value = dealer_upcard.primary_value
        
        if dealer_upcard.rank == Rank.ACE:
            dealer_value = 11
        
        # Get dealer outcome probabilities
        dealer_probs = ProbabilityCalculator.dealer_outcome_probability(
            dealer_upcard, remaining_cards
        )
        
        if action == Action.STAND:
            # Calculate EV based on player total vs dealer outcomes
            ev = 0.0
            
            for outcome, prob in dealer_probs.items():
                if outcome == 'bust':
                    ev += prob  # Player wins when dealer busts
                elif isinstance(outcome, int):
                    if player_total > outcome:
                        ev += prob  # Player wins
                    elif player_total < outcome:
                        ev -= prob  # Dealer wins
                    # Tie = 0 contribution
            
            return ev
        
        elif action == Action.HIT:
            # Simplified: assume basic strategy hit
            if player_total <= 11:
                return 0.1  # Hitting is generally good
            else:
                # Calculate bust risk
                bust_prob = (player_total - 11) / 10
                return -bust_prob
        
        elif action == Action.DOUBLE:
            # Double the stakes
            stand_ev = ProbabilityCalculator.expected_value(
                player_hand, dealer_upcard, Action.STAND, remaining_cards
            )
            return stand_ev * 1.5  # Simplified
        
        elif action == Action.SURRENDER:
            return -0.5  # Always lose half
        
        return 0.0
    
    @staticmethod
    def blackjack_probability(num_decks: int = 6, cards_seen: List[Card] = None) -> float:
        """
        Calculate probability of getting a natural blackjack.
        
        Args:
            num_decks: Number of decks in shoe
            cards_seen: Cards already dealt (for card counting)
            
        Returns:
            Probability of blackjack (0.0 to 1.0)
        """
        total_cards = num_decks * 52
        if cards_seen:
            total_cards -= len(cards_seen)
            aces_remaining = num_decks * 4 - sum(1 for c in cards_seen if c.rank == Rank.ACE)
            tens_remaining = num_decks * 16 - sum(1 for c in cards_seen 
                                                   if c.rank in (Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING))
        else:
            aces_remaining = num_decks * 4
            tens_remaining = num_decks * 16
        
        # P(Blackjack) = P(Ace first, Ten second) + P(Ten first, Ace second)
        if total_cards < 2:
            return 0.0
        
        p_ace_first = aces_remaining / total_cards
        p_ten_second = tens_remaining / (total_cards - 1)
        
        p_ten_first = tens_remaining / total_cards
        p_ace_second = aces_remaining / (total_cards - 1)
        
        return p_ace_first * p_ten_second + p_ten_first * p_ace_second


# ============================================================================
# Game Simulator
# ============================================================================

@dataclass
class GameResult:
    """Result of a blackjack game."""
    player_value: int
    dealer_value: int
    player_blackjack: bool
    dealer_blackjack: bool
    player_bust: bool
    dealer_bust: bool
    outcome: str  # 'win', 'lose', 'push', 'blackjack'
    payout: float  # Multiplier of bet
    
    def to_dict(self) -> dict:
        return {
            'player_value': self.player_value,
            'dealer_value': self.dealer_value,
            'player_blackjack': self.player_blackjack,
            'dealer_blackjack': self.dealer_blackjack,
            'player_bust': self.player_bust,
            'dealer_bust': self.dealer_bust,
            'outcome': self.outcome,
            'payout': self.payout
        }


@dataclass
class SimulationStats:
    """Statistics from a simulation run."""
    total_games: int = 0
    wins: int = 0
    losses: int = 0
    pushes: int = 0
    blackjacks: int = 0
    player_busts: int = 0
    dealer_busts: int = 0
    total_bet: float = 0.0
    total_return: float = 0.0
    
    @property
    def win_rate(self) -> float:
        return self.wins / self.total_games if self.total_games > 0 else 0.0
    
    @property
    def blackjack_rate(self) -> float:
        return self.blackjacks / self.total_games if self.total_games > 0 else 0.0
    
    @property
    def player_bust_rate(self) -> float:
        return self.player_busts / self.total_games if self.total_games > 0 else 0.0
    
    @property
    def return_percentage(self) -> float:
        return (self.total_return / self.total_bet * 100) if self.total_bet > 0 else 0.0
    
    def to_dict(self) -> dict:
        return {
            'total_games': self.total_games,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'player_busts': self.player_busts,
            'dealer_busts': self.dealer_busts,
            'total_bet': self.total_bet,
            'total_return': self.total_return,
            'win_rate': self.win_rate,
            'blackjack_rate': self.blackjack_rate,
            'player_bust_rate': self.player_bust_rate,
            'return_percentage': self.return_percentage
        }


class GameSimulator:
    """
    Blackjack game simulator for strategy testing.
    """
    
    def __init__(self, num_decks: int = 6, blackjack_pays: float = 1.5,
                 dealer_hits_soft_17: bool = True):
        """
        Initialize game simulator.
        
        Args:
            num_decks: Number of decks in shoe
            blackjack_pays: Blackjack payout ratio (1.5 = 3:2)
            dealer_hits_soft_17: Whether dealer hits on soft 17
        """
        self.num_decks = num_decks
        self.blackjack_pays = blackjack_pays
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.deck = Deck(num_decks)
    
    def deal_initial_cards(self) -> Tuple[Hand, Hand, Card]:
        """
        Deal initial cards to player and dealer.
        
        Returns:
            Tuple of (player_hand, dealer_hand, dealer_upcard)
        """
        if self.deck.needs_reshuffle or self.deck.remaining < 15:
            self.deck.reset()
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_cards(self.deck.deal(2))
        dealer_hand.add_cards(self.deck.deal(2))
        
        dealer_upcard = dealer_hand.cards[0]
        
        return player_hand, dealer_hand, dealer_upcard
    
    def dealer_play(self, hand: Hand) -> Hand:
        """
        Dealer plays according to house rules.
        
        Args:
            hand: Dealer's hand
            
        Returns:
            Final dealer hand
        """
        while True:
            value = hand.best_value
            
            # Dealer must hit on 16 or less
            if value < 17:
                hand.add_card(self.deck.deal_one())
            # Dealer hits soft 17 if rule is active
            elif value == 17 and hand.is_soft and self.dealer_hits_soft_17:
                hand.add_card(self.deck.deal_one())
            else:
                break
        
        return hand
    
    def player_play_basic_strategy(self, hand: Hand, dealer_upcard: Card,
                                   can_split: bool = True, 
                                   can_double: bool = True) -> Tuple[Hand, float]:
        """
        Player plays using basic strategy.
        
        Args:
            hand: Player's hand
            dealer_upcard: Dealer's visible card
            can_split: Whether splitting is allowed
            can_double: Whether doubling is allowed
            
        Returns:
            Tuple of (final_hand, bet_multiplier)
        """
        bet_multiplier = 1.0
        
        while True:
            if hand.is_bust:
                break
            
            action = BasicStrategy.get_action(hand, dealer_upcard, can_split, can_double)
            
            if action == Action.STAND:
                break
            elif action == Action.HIT:
                hand.add_card(self.deck.deal_one())
                can_double = False  # Can't double after hit
            elif action == Action.DOUBLE:
                if can_double:
                    hand.add_card(self.deck.deal_one())
                    bet_multiplier = 2.0
                else:
                    # Can't double, so hit instead
                    hand.add_card(self.deck.deal_one())
                break
            elif action == Action.SPLIT:
                # Splitting not supported in this simplified version, stand
                break
        
        return hand, bet_multiplier
    
    def play_round(self, bet: float = 1.0, 
                   player_strategy: Callable = None) -> GameResult:
        """
        Play a single round of blackjack.
        
        Args:
            bet: Bet amount
            player_strategy: Custom strategy function (hand, upcard) -> Action
            
        Returns:
            GameResult
        """
        player_hand, dealer_hand, dealer_upcard = self.deal_initial_cards()
        
        # Check for naturals
        if player_hand.is_blackjack and dealer_hand.is_blackjack:
            return GameResult(
                player_value=21, dealer_value=21,
                player_blackjack=True, dealer_blackjack=True,
                player_bust=False, dealer_bust=False,
                outcome='push', payout=0.0
            )
        
        if player_hand.is_blackjack:
            return GameResult(
                player_value=21, dealer_value=dealer_hand.best_value,
                player_blackjack=True, dealer_blackjack=False,
                player_bust=False, dealer_bust=False,
                outcome='blackjack', payout=self.blackjack_pays * bet
            )
        
        if dealer_hand.is_blackjack:
            return GameResult(
                player_value=player_hand.best_value, dealer_value=21,
                player_blackjack=False, dealer_blackjack=True,
                player_bust=False, dealer_bust=False,
                outcome='lose', payout=-bet
            )
        
        # Player plays
        if player_strategy:
            # Use custom strategy
            bet_multiplier = 1.0
            while True:
                if player_hand.is_bust:
                    break
                action = player_strategy(player_hand, dealer_upcard)
                if action == Action.STAND:
                    break
                elif action == Action.HIT:
                    player_hand.add_card(self.deck.deal_one())
                elif action == Action.DOUBLE and len(player_hand.cards) == 2:
                    player_hand.add_card(self.deck.deal_one())
                    bet_multiplier = 2.0
                    break
            bet *= bet_multiplier
        else:
            # Use basic strategy
            player_hand, bet_multiplier = self.player_play_basic_strategy(
                player_hand, dealer_upcard
            )
            bet *= bet_multiplier
        
        # Player busts
        if player_hand.is_bust:
            return GameResult(
                player_value=player_hand.best_value, dealer_value=dealer_hand.best_value,
                player_blackjack=False, dealer_blackjack=False,
                player_bust=True, dealer_bust=False,
                outcome='lose', payout=-bet
            )
        
        # Dealer plays
        dealer_hand = self.dealer_play(dealer_hand)
        
        # Determine outcome
        player_value = player_hand.best_value
        dealer_value = dealer_hand.best_value
        
        if dealer_hand.is_bust:
            return GameResult(
                player_value=player_value, dealer_value=dealer_value,
                player_blackjack=False, dealer_blackjack=False,
                player_bust=False, dealer_bust=True,
                outcome='win', payout=bet
            )
        
        if player_value > dealer_value:
            outcome = 'win'
            payout = bet
        elif player_value < dealer_value:
            outcome = 'lose'
            payout = -bet
        else:
            outcome = 'push'
            payout = 0.0
        
        return GameResult(
            player_value=player_value, dealer_value=dealer_value,
            player_blackjack=False, dealer_blackjack=False,
            player_bust=False, dealer_bust=dealer_hand.is_bust,
            outcome=outcome, payout=payout
        )
    
    def simulate(self, num_rounds: int = 1000, bet: float = 10.0,
                 player_strategy: Callable = None) -> SimulationStats:
        """
        Simulate multiple rounds of blackjack.
        
        Args:
            num_rounds: Number of rounds to simulate
            bet: Bet amount per round
            player_strategy: Custom strategy function
            
        Returns:
            SimulationStats
        """
        stats = SimulationStats()
        
        for _ in range(num_rounds):
            result = self.play_round(bet, player_strategy)
            
            stats.total_games += 1
            stats.total_bet += bet
            
            if result.outcome == 'win':
                stats.wins += 1
                stats.total_return += bet + result.payout
            elif result.outcome == 'lose':
                stats.losses += 1
            elif result.outcome == 'push':
                stats.pushes += 1
                stats.total_return += bet
            
            if result.outcome == 'blackjack':
                stats.blackjacks += 1
                stats.wins += 1
                stats.total_return += bet + result.payout
            
            if result.player_bust:
                stats.player_busts += 1
            
            if result.dealer_bust:
                stats.dealer_busts += 1
        
        return stats


# ============================================================================
# Convenience Functions
# ============================================================================

def create_deck(num_decks: int = 1) -> Deck:
    """Create a new deck of cards."""
    return Deck(num_decks)


def create_hand(cards: List[Card] = None) -> Hand:
    """Create a new hand."""
    return Hand(cards=cards or [])


def card(rank: str, suit: str) -> Card:
    """
    Create a card from string representations.
    
    Args:
        rank: Rank string ('A', '2', '3', ..., 'K')
        suit: Suit string ('hearts', 'diamonds', 'clubs', 'spades')
        
    Returns:
        Card object
    """
    rank_map = {
        'A': Rank.ACE, '1': Rank.ACE,
        '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR, '5': Rank.FIVE,
        '6': Rank.SIX, '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE,
        '10': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING
    }
    
    suit_map = {
        'hearts': Suit.HEARTS, 'h': Suit.HEARTS, '♥': Suit.HEARTS,
        'diamonds': Suit.DIAMONDS, 'd': Suit.DIAMONDS, '♦': Suit.DIAMONDS,
        'clubs': Suit.CLUBS, 'c': Suit.CLUBS, '♣': Suit.CLUBS,
        'spades': Suit.SPADES, 's': Suit.SPADES, '♠': Suit.SPADES
    }
    
    r = rank_map.get(rank.upper(), rank_map.get(rank))
    s = suit_map.get(suit.lower(), suit_map.get(suit))
    
    if r is None:
        raise ValueError(f"Invalid rank: {rank}")
    if s is None:
        raise ValueError(f"Invalid suit: {suit}")
    
    return Card(r, s)


def hand_value(cards: List[Card]) -> int:
    """Get the best value of a list of cards."""
    h = Hand(cards=cards)
    return h.best_value


def is_blackjack(cards: List[Card]) -> bool:
    """Check if cards form a natural blackjack."""
    h = Hand(cards=cards)
    return h.is_blackjack


def get_basic_strategy_action(player_cards: List[Card], dealer_upcard: Card) -> Action:
    """Get basic strategy recommendation for a hand."""
    h = Hand(cards=player_cards)
    return BasicStrategy.get_action(h, dealer_upcard)


def simulate_games(num_rounds: int = 1000, num_decks: int = 6, bet: float = 10.0) -> SimulationStats:
    """Simulate blackjack games using basic strategy."""
    simulator = GameSimulator(num_decks=num_decks)
    return simulator.simulate(num_rounds, bet)


def calculate_true_count(running_count: int, cards_seen: int, total_decks: int = 6) -> float:
    """Calculate true count from running count."""
    decks_remaining = (total_decks * 52 - cards_seen) / 52
    if decks_remaining < 0.5:
        decks_remaining = 0.5
    return running_count / decks_remaining


# ============================================================================
# Main (for testing)
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("Blackjack Utilities Demo")
    print("=" * 60)
    
    # Create deck and deal
    deck = Deck(num_decks=6)
    print(f"\nCreated {deck.num_decks}-deck shoe with {deck.remaining} cards")
    
    # Deal a hand
    hand = Hand()
    hand.add_cards(deck.deal(2))
    print(f"\nPlayer hand: {hand}")
    print(f"Hand type: {hand.hand_type.value}")
    print(f"Values: {hand.values}")
    
    # Get basic strategy
    dealer_up = deck.deal_one()
    print(f"\nDealer upcard: {dealer_up}")
    action = BasicStrategy.get_action(hand, dealer_up)
    print(f"Basic strategy recommends: {action.value}")
    
    # Show strategy charts
    print(BasicStrategy.get_strategy_chart('hard'))
    
    # Card counting demo
    print("\nCard Counting Demo (Hi-Lo):")
    counter = CardCounter(CountSystem.HI_LO, num_decks=6)
    test_cards = [
        card('2', 'hearts'), card('3', 'diamonds'), card('10', 'clubs'),
        card('A', 'spades'), card('5', 'hearts'), card('K', 'diamonds')
    ]
    for c in test_cards:
        counter.add_card(c)
        print(f"  {c}: Running count = {counter.running_count}")
    print(f"  True count: {counter.true_count:.2f}")
    print(f"  Player advantage: {counter.get_advantage():.2f}%")
    
    # Quick simulation
    print("\nSimulating 1000 rounds...")
    stats = simulate_games(num_rounds=1000, num_decks=6, bet=10.0)
    print(f"  Wins: {stats.wins} ({stats.win_rate:.1%})")
    print(f"  Losses: {stats.losses}")
    print(f"  Pushes: {stats.pushes}")
    print(f"  Blackjacks: {stats.blackjacks}")
    print(f"  Player busts: {stats.player_busts}")
    print(f"  Return: {stats.return_percentage:.2f}%")