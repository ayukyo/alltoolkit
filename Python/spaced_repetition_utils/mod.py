"""
Spaced Repetition Utilities

Implements the SM-2 algorithm (SuperMemo 2) and Leitner system for efficient
learning and memorization. Zero external dependencies.

Features:
- SM-2 Algorithm: Calculate optimal review intervals
- Leitner System: Multi-box card scheduling
- Card Management: Create, update, schedule flashcards
- Statistics: Track learning progress and retention
- Deck Management: Organize cards by topic

Reference: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
"""

import math
import random
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Optional, List, Dict, Tuple, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import json
import re


def _parse_iso_datetime(s: str) -> datetime:
    """
    Parse ISO format datetime string.
    
    Works on Python 3.6+ where datetime.fromisoformat is not available.
    Handles both 'YYYY-MM-DDTHH:MM:SS' and 'YYYY-MM-DDTHH:MM:SS.microseconds'.
    """
    if not s:
        raise ValueError("Empty datetime string")
    
    # Handle microseconds
    if '.' in s:
        # Format: YYYY-MM-DDTHH:MM:SS.ffffff
        pattern = r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)'
        match = re.match(pattern, s)
        if match:
            year, month, day, hour, minute, second, microsecond = match.groups()
            return datetime(
                int(year), int(month), int(day),
                int(hour), int(minute), int(second),
                int(microsecond[:6].ljust(6, '0'))
            )
    else:
        # Format: YYYY-MM-DDTHH:MM:SS
        pattern = r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})'
        match = re.match(pattern, s)
        if match:
            year, month, day, hour, minute, second = match.groups()
            return datetime(
                int(year), int(month), int(day),
                int(hour), int(minute), int(second)
            )
    
    # Fallback: try strptime
    try:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        # Try with microseconds
        return datetime.strptime(s.split('.')[0], '%Y-%m-%dT%H:%M:%S')


class Rating(IntEnum):
    """User rating for a review session (SM-2 algorithm)."""
    AGAIN = 1      # Complete failure, couldn't recall
    HARD = 2       # Incorrect response, but recognized when shown
    GOOD = 3       # Correct response after some hesitation
    EASY = 4       # Perfect response immediately


class LeitnerBox(IntEnum):
    """Leitner system boxes with different review intervals."""
    BOX_1 = 0   # New/difficult cards - review every session
    BOX_2 = 1   # Review every 1 day
    BOX_3 = 2   # Review every 3 days
    BOX_4 = 3   # Review every 7 days
    BOX_5 = 4   # Review every 14 days
    BOX_6 = 5   # Review every 30 days
    BOX_7 = 6   # Review every 60 days
    BOX_8 = 7   # Review every 120 days


# Default Leitner intervals (in days) for each box
LEITNER_INTERVALS = [0, 1, 3, 7, 14, 30, 60, 120]


@dataclass
class Card:
    """
    A flashcard for spaced repetition learning.
    
    Attributes:
        id: Unique identifier for the card
        front: Front side content (question/prompt)
        back: Back side content (answer/response)
        created: Creation timestamp
        interval: Current review interval in days
        repetitions: Number of successful reviews
        ease_factor: Difficulty multiplier (SM-2)
        due: Next review date
        last_review: Last review date
        leitner_box: Current box in Leitner system (0-indexed)
        tags: Optional tags for categorization
        deck: Optional deck name
        lapses: Number of times forgotten (reset to box 1)
        stability: Memory stability (for FSRS-like models)
        difficulty: Intrinsic difficulty (0-10 scale)
    """
    id: str
    front: str
    back: str
    created: datetime = field(default_factory=datetime.now)
    interval: float = 0.0
    repetitions: int = 0
    ease_factor: float = 2.5
    due: datetime = field(default_factory=datetime.now)
    last_review: Optional[datetime] = None
    leitner_box: int = 0
    tags: List[str] = field(default_factory=list)
    deck: str = "default"
    lapses: int = 0
    stability: float = 0.0
    difficulty: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization."""
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'created': self.created.isoformat(),
            'interval': self.interval,
            'repetitions': self.repetitions,
            'ease_factor': self.ease_factor,
            'due': self.due.isoformat(),
            'last_review': self.last_review.isoformat() if self.last_review else None,
            'leitner_box': self.leitner_box,
            'tags': self.tags,
            'deck': self.deck,
            'lapses': self.lapses,
            'stability': self.stability,
            'difficulty': self.difficulty,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Card':
        """Create card from dictionary."""
        return cls(
            id=data['id'],
            front=data['front'],
            back=data['back'],
            created=_parse_iso_datetime(data['created']),
            interval=data['interval'],
            repetitions=data['repetitions'],
            ease_factor=data['ease_factor'],
            due=_parse_iso_datetime(data['due']),
            last_review=_parse_iso_datetime(data['last_review']) if data.get('last_review') else None,
            leitner_box=data.get('leitner_box', 0),
            tags=data.get('tags', []),
            deck=data.get('deck', 'default'),
            lapses=data.get('lapses', 0),
            stability=data.get('stability', 0.0),
            difficulty=data.get('difficulty', 0.0),
        )
    
    def is_due(self, now: Optional[datetime] = None) -> bool:
        """Check if card is due for review."""
        if now is None:
            now = datetime.now()
        return self.due <= now
    
    def days_overdue(self, now: Optional[datetime] = None) -> float:
        """Calculate how many days overdue the card is."""
        if now is None:
            now = datetime.now()
        delta = now - self.due
        return max(0, delta.total_seconds() / 86400)


@dataclass
class ReviewResult:
    """Result of a card review."""
    card: Card
    rating: Rating
    previous_interval: float
    new_interval: float
    previous_box: int
    new_box: int
    reviewed_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'card_id': self.card.id,
            'rating': int(self.rating),
            'previous_interval': self.previous_interval,
            'new_interval': self.new_interval,
            'previous_box': self.previous_box,
            'new_box': self.new_box,
            'reviewed_at': self.reviewed_at.isoformat(),
        }


class SM2Scheduler:
    """
    SM-2 Algorithm Implementation (SuperMemo 2).
    
    The algorithm calculates optimal review intervals based on:
    - Current ease factor (difficulty rating)
    - Number of consecutive successful reviews
    - User's response quality (1-4 rating)
    
    Default parameters:
    - Minimum ease factor: 1.3
    - Initial ease factor: 2.5
    - Easy bonus: 1.3
    - Interval modifier: 1.0
    """
    
    def __init__(
        self,
        min_ease_factor: float = 1.3,
        initial_ease_factor: float = 2.5,
        easy_bonus: float = 1.3,
        interval_modifier: float = 1.0,
        graduating_interval: float = 1.0,
        easy_interval: float = 4.0,
    ):
        self.min_ease_factor = min_ease_factor
        self.initial_ease_factor = initial_ease_factor
        self.easy_bonus = easy_bonus
        self.interval_modifier = interval_modifier
        self.graduating_interval = graduating_interval
        self.easy_interval = easy_interval
    
    def calculate_ease_factor(self, current_ef: float, rating: Rating) -> float:
        """
        Calculate new ease factor based on rating.
        
        Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        Simplified for 4-point scale (1-4).
        """
        # Map 4-point scale to SM-2's 0-5 scale
        q_map = {Rating.AGAIN: 1, Rating.HARD: 3, Rating.GOOD: 4, Rating.EASY: 5}
        q = q_map[rating]
        
        # SM-2 ease factor formula
        new_ef = current_ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        return max(self.min_ease_factor, new_ef)
    
    def calculate_interval(
        self,
        card: Card,
        rating: Rating,
        now: Optional[datetime] = None,
    ) -> Tuple[float, int, float]:
        """
        Calculate new review interval using SM-2 algorithm.
        
        Args:
            card: The card being reviewed
            rating: User's response quality
            now: Current datetime (defaults to now)
        
        Returns:
            Tuple of (new_interval, new_repetitions, new_ease_factor)
        """
        if now is None:
            now = datetime.now()
        
        interval = card.interval
        repetitions = card.repetitions
        ease_factor = card.ease_factor
        
        if rating == Rating.AGAIN:
            # Complete failure - reset
            return (0, 0, self.calculate_ease_factor(ease_factor, rating))
        
        if repetitions == 0:
            # First review
            if rating == Rating.EASY:
                interval = self.easy_interval
            else:
                interval = self.graduating_interval
            repetitions = 1
        elif repetitions == 1:
            # Second review
            if rating == Rating.EASY:
                interval = self.graduating_interval * self.easy_bonus
            else:
                interval = self.graduating_interval
            repetitions = 2
        else:
            # Subsequent reviews
            if rating == Rating.EASY:
                interval = interval * ease_factor * self.easy_bonus
            elif rating == Rating.HARD:
                interval = interval * 1.2  # Small increase
            else:
                interval = interval * ease_factor
            repetitions += 1
        
        # Apply interval modifier
        interval *= self.interval_modifier
        
        # Update ease factor
        new_ef = self.calculate_ease_factor(ease_factor, rating)
        
        return (interval, repetitions, new_ef)
    
    def review_card(
        self,
        card: Card,
        rating: Rating,
        now: Optional[datetime] = None,
    ) -> ReviewResult:
        """
        Review a card and update its scheduling.
        
        Args:
            card: The card to review
            rating: User's response quality (1-4)
            now: Current datetime
        
        Returns:
            ReviewResult with updated card information
        """
        if now is None:
            now = datetime.now()
        
        previous_interval = card.interval
        previous_box = card.leitner_box
        
        interval, repetitions, ease_factor = self.calculate_interval(card, rating, now)
        
        # Update card
        card.interval = interval
        card.repetitions = repetitions
        card.ease_factor = ease_factor
        card.last_review = now
        card.due = now + timedelta(days=interval)
        
        if rating == Rating.AGAIN:
            card.lapses += 1
        
        return ReviewResult(
            card=card,
            rating=rating,
            previous_interval=previous_interval,
            new_interval=interval,
            previous_box=previous_box,
            new_box=card.leitner_box,
            reviewed_at=now,
        )


class LeitnerScheduler:
    """
    Leitner System Implementation.
    
    A simpler spaced repetition system using boxes with fixed intervals.
    Cards move up on correct answers and down (to box 1) on failures.
    
    Features:
    - Configurable intervals per box
    - Support for up to 8 boxes (default)
    - Automatic card promotion/demotion
    """
    
    def __init__(
        self,
        intervals: Optional[List[int]] = None,
        num_boxes: int = 8,
    ):
        self.intervals = intervals or LEITNER_INTERVALS[:num_boxes]
        self.num_boxes = min(num_boxes, len(self.intervals))
    
    def get_next_box(self, current_box: int, correct: bool) -> int:
        """
        Calculate the next box for a card.
        
        Args:
            current_box: Current box (0-indexed)
            correct: Whether the answer was correct
        
        Returns:
            New box number
        """
        if correct:
            # Move up one box (capped at max box)
            return min(current_box + 1, self.num_boxes - 1)
        else:
            # Move back to box 1 (index 0)
            return 0
    
    def get_interval_for_box(self, box: int) -> int:
        """Get the review interval for a box."""
        box = min(box, len(self.intervals) - 1)
        return self.intervals[box]
    
    def get_due_date(self, box: int, now: Optional[datetime] = None) -> datetime:
        """Calculate due date for a box."""
        if now is None:
            now = datetime.now()
        interval = self.get_interval_for_box(box)
        return now + timedelta(days=interval)
    
    def review_card(
        self,
        card: Card,
        rating: Rating,
        now: Optional[datetime] = None,
    ) -> ReviewResult:
        """
        Review a card using the Leitner system.
        
        Args:
            card: The card to review
            rating: User's response quality
            now: Current datetime
        
        Returns:
            ReviewResult with updated card information
        """
        if now is None:
            now = datetime.now()
        
        previous_box = card.leitner_box
        previous_interval = card.interval
        
        # Determine if correct (Good or Easy)
        correct = rating in (Rating.GOOD, Rating.EASY)
        
        # Calculate new box
        new_box = self.get_next_box(previous_box, correct)
        new_interval = self.get_interval_for_box(new_box)
        
        # Update card
        card.leitner_box = new_box
        card.interval = new_interval
        card.last_review = now
        card.due = self.get_due_date(new_box, now)
        
        if not correct:
            card.lapses += 1
            card.repetitions = 0
        else:
            card.repetitions += 1
        
        return ReviewResult(
            card=card,
            rating=rating,
            previous_interval=previous_interval,
            new_interval=new_interval,
            previous_box=previous_box,
            new_box=new_box,
            reviewed_at=now,
        )


class Deck:
    """
    A collection of flashcards with statistics and scheduling.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.cards: Dict[str, Card] = {}
        self.review_history: List[ReviewResult] = []
        self.created = datetime.now()
    
    def add_card(self, card: Card) -> None:
        """Add a card to the deck."""
        card.deck = self.name
        self.cards[card.id] = card
    
    def remove_card(self, card_id: str) -> Optional[Card]:
        """Remove a card from the deck."""
        return self.cards.pop(card_id, None)
    
    def get_card(self, card_id: str) -> Optional[Card]:
        """Get a card by ID."""
        return self.cards.get(card_id)
    
    def get_due_cards(self, now: Optional[datetime] = None) -> List[Card]:
        """Get all cards due for review."""
        return [card for card in self.cards.values() if card.is_due(now)]
    
    def get_new_cards(self) -> List[Card]:
        """Get all new (unreviewed) cards."""
        return [card for card in self.cards.values() if card.repetitions == 0]
    
    def get_learning_cards(self) -> List[Card]:
        """Get cards currently being learned (interval < 1 day)."""
        return [card for card in self.cards.values() if 0 < card.interval < 1]
    
    def get_review_cards(self) -> List[Card]:
        """Get mature review cards (interval >= 1 day)."""
        return [card for card in self.cards.values() if card.interval >= 1]
    
    def get_cards_by_tag(self, tag: str) -> List[Card]:
        """Get all cards with a specific tag."""
        return [card for card in self.cards.values() if tag in card.tags]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate deck statistics."""
        total = len(self.cards)
        if total == 0:
            return {
                'total': 0,
                'new': 0,
                'learning': 0,
                'review': 0,
                'due': 0,
                'lapses': 0,
                'average_ease_factor': 0,
                'average_interval': 0,
                'retention_rate': 0,
            }
        
        new_cards = self.get_new_cards()
        learning_cards = self.get_learning_cards()
        review_cards = self.get_review_cards()
        due_cards = self.get_due_cards()
        
        total_lapses = sum(card.lapses for card in self.cards.values())
        avg_ef = sum(card.ease_factor for card in self.cards.values()) / total
        avg_interval = sum(card.interval for card in self.cards.values()) / total
        
        # Calculate retention rate from review history
        if self.review_history:
            successful = sum(1 for r in self.review_history if r.rating >= Rating.GOOD)
            retention = successful / len(self.review_history)
        else:
            retention = 0
        
        return {
            'total': total,
            'new': len(new_cards),
            'learning': len(learning_cards),
            'review': len(review_cards),
            'due': len(due_cards),
            'lapses': total_lapses,
            'average_ease_factor': round(avg_ef, 2),
            'average_interval': round(avg_interval, 2),
            'retention_rate': round(retention * 100, 1),
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize deck to dictionary."""
        return {
            'name': self.name,
            'cards': {cid: card.to_dict() for cid, card in self.cards.items()},
            'review_history': [r.to_dict() for r in self.review_history],
            'created': self.created.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Deck':
        """Create deck from dictionary."""
        deck = cls(name=data['name'])
        deck.created = _parse_iso_datetime(data['created'])
        deck.cards = {
            cid: Card.from_dict(cdata) 
            for cid, cdata in data['cards'].items()
        }
        # Note: review_history would need Card objects to reconstruct
        return deck


class SpacedRepetition:
    """
    Main class for spaced repetition learning.
    
    Combines SM-2 and Leitner schedulers with deck management.
    """
    
    def __init__(
        self,
        scheduler: str = "sm2",
        sm2_config: Optional[Dict[str, float]] = None,
        leitner_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize spaced repetition system.
        
        Args:
            scheduler: "sm2" or "leitner"
            sm2_config: Configuration for SM-2 scheduler
            leitner_config: Configuration for Leitner scheduler
        """
        self.decks: Dict[str, Deck] = {}
        self.scheduler_type = scheduler
        
        if scheduler == "sm2":
            config = sm2_config or {}
            self.scheduler = SM2Scheduler(**config)
        else:
            config = leitner_config or {}
            self.scheduler = LeitnerScheduler(**config)
    
    def create_deck(self, name: str) -> Deck:
        """Create a new deck."""
        deck = Deck(name=name)
        self.decks[name] = deck
        return deck
    
    def get_deck(self, name: str) -> Optional[Deck]:
        """Get a deck by name."""
        return self.decks.get(name)
    
    def delete_deck(self, name: str) -> bool:
        """Delete a deck. Returns True if deck existed."""
        return self.decks.pop(name, None) is not None
    
    def create_card(
        self,
        front: str,
        back: str,
        deck: str = "default",
        tags: Optional[List[str]] = None,
        card_id: Optional[str] = None,
    ) -> Card:
        """Create a new flashcard."""
        import uuid
        card_id = card_id or str(uuid.uuid4())
        card = Card(
            id=card_id,
            front=front,
            back=back,
            tags=tags or [],
            deck=deck,
        )
        
        if deck not in self.decks:
            self.create_deck(deck)
        
        self.decks[deck].add_card(card)
        return card
    
    def review_card(
        self,
        card: Card,
        rating: Rating,
        deck_name: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> ReviewResult:
        """
        Review a card with the configured scheduler.
        
        Args:
            card: Card to review
            rating: User's response quality
            deck_name: Deck name (uses card's deck if not specified)
            now: Current datetime
        
        Returns:
            ReviewResult with updated information
        """
        deck_name = deck_name or card.deck
        deck = self.decks.get(deck_name)
        
        result = self.scheduler.review_card(card, rating, now)
        
        if deck:
            deck.review_history.append(result)
        
        return result
    
    def get_due_cards(
        self,
        deck_name: str = "default",
        limit: Optional[int] = None,
        now: Optional[datetime] = None,
    ) -> List[Card]:
        """Get cards due for review from a deck."""
        deck = self.decks.get(deck_name)
        if not deck:
            return []
        
        due = deck.get_due_cards(now)
        
        # Sort by due date (oldest first)
        due.sort(key=lambda c: c.due)
        
        if limit:
            due = due[:limit]
        
        return due
    
    def get_all_due_cards(self, now: Optional[datetime] = None) -> Dict[str, List[Card]]:
        """Get all due cards across all decks."""
        result = {}
        for name, deck in self.decks.items():
            due = deck.get_due_cards(now)
            if due:
                result[name] = due
        return result
    
    def get_statistics(self, deck_name: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for a deck or all decks."""
        if deck_name:
            deck = self.decks.get(deck_name)
            return deck.get_statistics() if deck else {}
        
        # Aggregate all decks
        all_stats = {
            'decks': {},
            'total_cards': 0,
            'total_due': 0,
            'total_new': 0,
            'total_lapses': 0,
            'overall_retention': 0,
        }
        
        total_reviews = 0
        successful_reviews = 0
        
        for name, deck in self.decks.items():
            stats = deck.get_statistics()
            all_stats['decks'][name] = stats
            all_stats['total_cards'] += stats['total']
            all_stats['total_due'] += stats['due']
            all_stats['total_new'] += stats['new']
            all_stats['total_lapses'] += stats['lapses']
            
            # Count successful reviews
            for review in deck.review_history:
                total_reviews += 1
                if review.rating >= Rating.GOOD:
                    successful_reviews += 1
        
        if total_reviews > 0:
            all_stats['overall_retention'] = round(
                successful_reviews / total_reviews * 100, 1
            )
        
        return all_stats
    
    def export_to_json(self) -> str:
        """Export all decks to JSON."""
        data = {
            'scheduler': self.scheduler_type,
            'decks': {name: deck.to_dict() for name, deck in self.decks.items()},
        }
        return json.dumps(data, indent=2, default=str)
    
    def import_from_json(self, json_str: str) -> None:
        """Import decks from JSON."""
        data = json.loads(json_str)
        
        for name, deck_data in data.get('decks', {}).items():
            deck = Deck.from_dict(deck_data)
            self.decks[name] = deck


def calculate_retention(
    reviews: List[ReviewResult],
    period_days: Optional[int] = None,
) -> float:
    """
    Calculate retention rate over a period.
    
    Args:
        reviews: List of review results
        period_days: Number of days to consider (None = all time)
    
    Returns:
        Retention rate as percentage (0-100)
    """
    if not reviews:
        return 0.0
    
    if period_days:
        cutoff = datetime.now() - timedelta(days=period_days)
        reviews = [r for r in reviews if r.reviewed_at >= cutoff]
    
    if not reviews:
        return 0.0
    
    successful = sum(1 for r in reviews if r.rating >= Rating.GOOD)
    return round(successful / len(reviews) * 100, 1)


def predict_forgetting_curve(
    days_since_review: int,
    stability: float,
) -> float:
    """
    Predict probability of recall using exponential forgetting curve.
    
    P = e^(-t/S)
    
    Args:
        days_since_review: Days since last review
        stability: Memory stability parameter
    
    Returns:
        Probability of recall (0-1)
    """
    return math.exp(-days_since_review / max(stability, 0.1))


def calculate_optimal_review_time(
    stability: float,
    target_retention: float = 0.9,
) -> int:
    """
    Calculate optimal days until next review.
    
    Args:
        stability: Memory stability parameter
        target_retention: Target retention probability (default 90%)
    
    Returns:
        Optimal number of days until review
    """
    # Solve for t: target_retention = e^(-t/S)
    # t = -S * ln(target_retention)
    if stability <= 0 or target_retention <= 0 or target_retention >= 1:
        return 1
    
    days = -stability * math.log(target_retention)
    return max(1, round(days))


def generate_review_schedule(
    cards: List[Card],
    now: Optional[datetime] = None,
    max_per_day: int = 20,
    spread_new_cards: bool = True,
) -> Dict[str, List[str]]:
    """
    Generate a review schedule for cards.
    
    Args:
        cards: List of cards to schedule
        now: Current datetime
        max_per_day: Maximum reviews per day
        spread_new_cards: Whether to spread new cards across days
    
    Returns:
        Dictionary mapping date strings to lists of card IDs
    """
    if now is None:
        now = datetime.now()
    
    # Separate new and due cards
    new_cards = [c for c in cards if c.repetitions == 0]
    due_cards = sorted([c for c in cards if c.repetitions > 0], key=lambda c: c.due)
    
    schedule: Dict[str, List[str]] = defaultdict(list)
    current_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cards_today = 0
    day_offset = 0
    
    # Schedule due cards first
    for card in due_cards:
        if cards_today >= max_per_day:
            day_offset += 1
            cards_today = 0
        
        day_key = (current_day + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        schedule[day_key].append(card.id)
        cards_today += 1
    
    # Spread new cards
    if spread_new_cards:
        new_per_day = max(1, min(max_per_day // 4, len(new_cards)))
        new_idx = 0
        
        while new_idx < len(new_cards):
            if cards_today >= max_per_day:
                day_offset += 1
                cards_today = 0
            
            day_key = (current_day + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            
            for _ in range(min(new_per_day, len(new_cards) - new_idx)):
                if cards_today >= max_per_day:
                    break
                if new_idx < len(new_cards):
                    schedule[day_key].append(new_cards[new_idx].id)
                    new_idx += 1
                    cards_today += 1
    else:
        # Schedule all new cards today
        for card in new_cards:
            if cards_today >= max_per_day:
                day_offset += 1
                cards_today = 0
            
            day_key = (current_day + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            schedule[day_key].append(card.id)
            cards_today += 1
    
    return dict(schedule)


def calculate_card_priority(card: Card, now: Optional[datetime] = None) -> float:
    """
    Calculate priority score for a card (higher = more urgent).
    
    Factors:
    - Overdue days
    - Lapses (forgotten cards are higher priority)
    - Ease factor (harder cards are higher priority)
    - Repetitions (new cards are higher priority)
    
    Args:
        card: Card to prioritize
        now: Current datetime
    
    Returns:
        Priority score
    """
    if now is None:
        now = datetime.now()
    
    score = 0.0
    
    # Overdue factor
    if card.due <= now:
        overdue_days = (now - card.due).total_seconds() / 86400
        score += overdue_days * 10
    
    # Lapse penalty
    score += card.lapses * 5
    
    # Difficulty factor (lower ease = harder = higher priority)
    if card.ease_factor < 2.5:
        score += (2.5 - card.ease_factor) * 10
    
    # New cards get slight priority
    if card.repetitions == 0:
        score += 2
    
    return round(score, 2)


def sort_cards_by_priority(cards: List[Card], now: Optional[datetime] = None) -> List[Card]:
    """Sort cards by priority (highest first)."""
    return sorted(cards, key=lambda c: calculate_card_priority(c, now), reverse=True)


# Utility functions for creating common card types

def create_question_card(
    question: str,
    answer: str,
    deck: str = "default",
    tags: Optional[List[str]] = None,
) -> Card:
    """Create a simple Q&A flashcard."""
    import uuid
    return Card(
        id=str(uuid.uuid4()),
        front=question,
        back=answer,
        deck=deck,
        tags=tags or [],
    )


def create_reversable_card(
    front: str,
    back: str,
    deck: str = "default",
    tags: Optional[List[str]] = None,
) -> Tuple[Card, Card]:
    """Create two cards: front->back and back->front."""
    import uuid
    base_id = str(uuid.uuid4())
    
    card1 = Card(
        id=f"{base_id}_1",
        front=front,
        back=back,
        deck=deck,
        tags=tags or [],
    )
    
    card2 = Card(
        id=f"{base_id}_2",
        front=back,
        back=front,
        deck=deck,
        tags=tags or [],
    )
    
    return card1, card2


def create_cloze_card(
    text: str,
    clozes: List[Tuple[int, int]],  # List of (start, end) positions
    deck: str = "default",
    tags: Optional[List[str]] = None,
) -> List[Card]:
    """
    Create cloze deletion cards.
    
    Args:
        text: Full text
        clozes: List of (start, end) positions to hide
        deck: Deck name
        tags: Optional tags
    
    Returns:
        List of cloze cards
    """
    import uuid
    cards = []
    base_id = str(uuid.uuid4())
    
    for i, (start, end) in enumerate(clozes):
        # Create the cloze text
        cloze_text = text[:start] + "[...]" + text[end:]
        answer = text[start:end]
        
        card = Card(
            id=f"{base_id}_c{i}",
            front=cloze_text,
            back=answer,
            deck=deck,
            tags=tags or [],
        )
        cards.append(card)
    
    return cards


def create_type_in_card(
    prompt: str,
    correct_answers: List[str],
    case_sensitive: bool = False,
    deck: str = "default",
    tags: Optional[List[str]] = None,
) -> Card:
    """Create a type-in answer card."""
    import uuid
    
    # Store answers in back with a marker
    back_content = "||".join(correct_answers)
    
    card = Card(
        id=str(uuid.uuid4()),
        front=f"[Type] {prompt}",
        back=back_content,
        deck=deck,
        tags=tags or [],
    )
    
    # Store case sensitivity in a special tag
    if not case_sensitive:
        card.tags.append("case_insensitive")
    
    return card


def check_type_in_answer(card: Card, user_answer: str) -> bool:
    """Check if a type-in answer is correct."""
    correct_answers = card.back.split("||")
    case_sensitive = "case_insensitive" not in card.tags
    
    if not case_sensitive:
        user_answer = user_answer.lower()
        correct_answers = [a.lower() for a in correct_answers]
    
    return user_answer.strip() in correct_answers