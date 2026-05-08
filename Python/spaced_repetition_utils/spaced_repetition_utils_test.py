"""
Tests for Spaced Repetition Utilities

Comprehensive tests covering:
- SM-2 Algorithm (interval calculation, ease factor)
- Leitner System (box promotion/demotion)
- Card management (creation, serialization)
- Deck management (add, remove, statistics)
- Review scheduling and priority
- Utility functions (retention, forgetting curve)
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spaced_repetition_utils.mod import (
    Rating, LeitnerBox, LEITNER_INTERVALS,
    Card, ReviewResult,
    SM2Scheduler, LeitnerScheduler,
    Deck, SpacedRepetition,
    calculate_retention, predict_forgetting_curve,
    calculate_optimal_review_time, generate_review_schedule,
    calculate_card_priority, sort_cards_by_priority,
    create_question_card, create_reversable_card,
    create_cloze_card, create_type_in_card, check_type_in_answer,
)


class TestRating(unittest.TestCase):
    """Test Rating enum."""
    
    def test_rating_values(self):
        """Test rating values are correct."""
        self.assertEqual(Rating.AGAIN, 1)
        self.assertEqual(Rating.HARD, 2)
        self.assertEqual(Rating.GOOD, 3)
        self.assertEqual(Rating.EASY, 4)
    
    def test_rating_comparison(self):
        """Test rating comparison."""
        self.assertTrue(Rating.EASY > Rating.GOOD)
        self.assertTrue(Rating.GOOD > Rating.HARD)
        self.assertTrue(Rating.HARD > Rating.AGAIN)


class TestLeitnerBox(unittest.TestCase):
    """Test LeitnerBox enum."""
    
    def test_box_values(self):
        """Test box values are 0-indexed."""
        self.assertEqual(LeitnerBox.BOX_1, 0)
        self.assertEqual(LeitnerBox.BOX_8, 7)
    
    def test_default_intervals(self):
        """Test default Leitner intervals."""
        self.assertEqual(LEITNER_INTERVALS[0], 0)   # Box 1: same day
        self.assertEqual(LEITNER_INTERVALS[1], 1)   # Box 2: 1 day
        self.assertEqual(LEITNER_INTERVALS[4], 14)  # Box 5: 14 days
        self.assertEqual(LEITNER_INTERVALS[7], 120) # Box 8: 120 days


class TestCard(unittest.TestCase):
    """Test Card class."""
    
    def test_card_creation(self):
        """Test basic card creation."""
        card = Card(
            id="test-1",
            front="What is 2+2?",
            back="4",
        )
        
        self.assertEqual(card.id, "test-1")
        self.assertEqual(card.front, "What is 2+2?")
        self.assertEqual(card.back, "4")
        self.assertEqual(card.interval, 0.0)
        self.assertEqual(card.repetitions, 0)
        self.assertEqual(card.ease_factor, 2.5)
        self.assertEqual(card.leitner_box, 0)
        self.assertEqual(card.deck, "default")
        self.assertEqual(card.tags, [])
        self.assertIsNotNone(card.created)
        self.assertIsNotNone(card.due)
    
    def test_card_is_due(self):
        """Test is_due method."""
        now = datetime.now()
        
        # Card due in the past
        past_card = Card(
            id="past",
            front="A",
            back="B",
            due=now - timedelta(days=1),
        )
        self.assertTrue(past_card.is_due(now))
        
        # Card due in the future
        future_card = Card(
            id="future",
            front="A",
            back="B",
            due=now + timedelta(days=1),
        )
        self.assertFalse(future_card.is_due(now))
        
        # Card due now
        now_card = Card(
            id="now",
            front="A",
            back="B",
            due=now,
        )
        self.assertTrue(now_card.is_due(now))
    
    def test_card_days_overdue(self):
        """Test days_overdue calculation."""
        now = datetime.now()
        
        # Not overdue
        future_card = Card(
            id="future",
            front="A",
            back="B",
            due=now + timedelta(days=2),
        )
        self.assertEqual(future_card.days_overdue(now), 0)
        
        # 3 days overdue
        overdue_card = Card(
            id="overdue",
            front="A",
            back="B",
            due=now - timedelta(days=3),
        )
        self.assertAlmostEqual(overdue_card.days_overdue(now), 3.0, places=1)
    
    def test_card_serialization(self):
        """Test card to_dict and from_dict."""
        card = Card(
            id="test-123",
            front="Question",
            back="Answer",
            interval=5.0,
            repetitions=3,
            ease_factor=2.3,
            leitner_box=2,
            tags=["math", "basic"],
            deck="math-deck",
            lapses=1,
        )
        
        data = card.to_dict()
        self.assertEqual(data['id'], "test-123")
        self.assertEqual(data['front'], "Question")
        self.assertEqual(data['back'], "Answer")
        self.assertEqual(data['interval'], 5.0)
        self.assertEqual(data['repetitions'], 3)
        self.assertEqual(data['ease_factor'], 2.3)
        self.assertEqual(data['leitner_box'], 2)
        self.assertEqual(data['tags'], ["math", "basic"])
        self.assertEqual(data['deck'], "math-deck")
        self.assertEqual(data['lapses'], 1)
        
        # Round-trip
        restored = Card.from_dict(data)
        self.assertEqual(restored.id, card.id)
        self.assertEqual(restored.front, card.front)
        self.assertEqual(restored.back, card.back)
        self.assertEqual(restored.interval, card.interval)
        self.assertEqual(restored.repetitions, card.repetitions)
        self.assertEqual(restored.ease_factor, card.ease_factor)
        self.assertEqual(restored.leitner_box, card.leitner_box)
        self.assertEqual(restored.tags, card.tags)
        self.assertEqual(restored.deck, card.deck)
        self.assertEqual(restored.lapses, card.lapses)


class TestSM2Scheduler(unittest.TestCase):
    """Test SM-2 algorithm implementation."""
    
    def test_initialization(self):
        """Test scheduler initialization with defaults."""
        scheduler = SM2Scheduler()
        
        self.assertEqual(scheduler.min_ease_factor, 1.3)
        self.assertEqual(scheduler.initial_ease_factor, 2.5)
        self.assertEqual(scheduler.easy_bonus, 1.3)
        self.assertEqual(scheduler.interval_modifier, 1.0)
        self.assertEqual(scheduler.graduating_interval, 1.0)
        self.assertEqual(scheduler.easy_interval, 4.0)
    
    def test_custom_initialization(self):
        """Test scheduler with custom parameters."""
        scheduler = SM2Scheduler(
            min_ease_factor=1.5,
            initial_ease_factor=2.8,
            easy_bonus=1.5,
            interval_modifier=0.9,
        )
        
        self.assertEqual(scheduler.min_ease_factor, 1.5)
        self.assertEqual(scheduler.initial_ease_factor, 2.8)
        self.assertEqual(scheduler.easy_bonus, 1.5)
        self.assertEqual(scheduler.interval_modifier, 0.9)
    
    def test_ease_factor_calculation(self):
        """Test ease factor changes based on rating."""
        scheduler = SM2Scheduler()
        
        # Easy rating should increase ease factor by 0.1
        ef_easy = scheduler.calculate_ease_factor(2.5, Rating.EASY)
        self.assertEqual(ef_easy, 2.6)
        
        # Good rating should keep EF the same (no change)
        ef_good = scheduler.calculate_ease_factor(2.5, Rating.GOOD)
        self.assertEqual(ef_good, 2.5)
        
        # Hard rating should decrease by 0.14
        ef_hard = scheduler.calculate_ease_factor(2.5, Rating.HARD)
        self.assertEqual(ef_hard, 2.36)
        
        # Again rating should decrease by 0.54
        ef_again = scheduler.calculate_ease_factor(2.5, Rating.AGAIN)
        self.assertEqual(ef_again, 1.96)
    
    def test_ease_factor_minimum(self):
        """Test ease factor respects minimum."""
        scheduler = SM2Scheduler(min_ease_factor=1.3)
        
        # Even with bad rating, ease factor shouldn't go below minimum
        ef = scheduler.calculate_ease_factor(1.4, Rating.AGAIN)
        self.assertGreaterEqual(ef, 1.3)
    
    def test_first_review_intervals(self):
        """Test intervals for first review."""
        scheduler = SM2Scheduler()
        now = datetime.now()
        
        card = Card(id="new", front="Q", back="A")
        
        # First review - Good
        interval, reps, ef = scheduler.calculate_interval(card, Rating.GOOD, now)
        self.assertEqual(interval, 1.0)  # Graduating interval
        self.assertEqual(reps, 1)
        self.assertEqual(ef, 2.5)  # EF unchanged for Good
        
        # First review - Easy
        card2 = Card(id="new2", front="Q", back="A")
        interval, reps, ef = scheduler.calculate_interval(card2, Rating.EASY, now)
        self.assertEqual(interval, 4.0)  # Easy interval
        self.assertEqual(reps, 1)
        self.assertEqual(ef, 2.6)  # EF increased by 0.1
    
    def test_again_resets_card(self):
        """Test that 'Again' rating resets card."""
        scheduler = SM2Scheduler()
        now = datetime.now()
        
        card = Card(
            id="test",
            front="Q",
            back="A",
            interval=10.0,
            repetitions=5,
            ease_factor=2.5,
        )
        
        interval, reps, ef = scheduler.calculate_interval(card, Rating.AGAIN, now)
        
        self.assertEqual(interval, 0)
        self.assertEqual(reps, 0)
        self.assertLess(ef, 2.5)  # Ease factor decreased
    
    def test_interval_progression(self):
        """Test that intervals increase with successful reviews."""
        scheduler = SM2Scheduler()
        now = datetime.now()
        
        card = Card(id="test", front="Q", back="A")
        
        # First review - Good (repetitions 0 -> 1)
        interval1, reps1, _ = scheduler.calculate_interval(card, Rating.GOOD, now)
        card.interval = interval1
        card.repetitions = reps1
        
        # Second review - Good (repetitions 1 -> 2)
        # After second successful review, interval starts using ease factor
        interval2, reps2, _ = scheduler.calculate_interval(card, Rating.GOOD, now)
        
        # Update card for third review
        card.interval = interval2
        card.repetitions = reps2
        
        # Third review - Good (repetitions 2 -> 3)
        interval3, reps3, _ = scheduler.calculate_interval(card, Rating.GOOD, now)
        
        # Intervals should increase after repetitions >= 2
        self.assertEqual(interval1, 1.0)  # Graduating interval
        self.assertEqual(interval2, 1.0)  # Still graduating for second review
        self.assertGreater(interval3, interval2)  # Now EF-based
        self.assertEqual(reps3, 3)
    
    def test_review_card_updates(self):
        """Test review_card updates card correctly."""
        scheduler = SM2Scheduler()
        now = datetime.now()
        
        card = Card(id="test", front="Q", back="A")
        result = scheduler.review_card(card, Rating.GOOD, now)
        
        self.assertEqual(result.rating, Rating.GOOD)
        self.assertEqual(result.previous_interval, 0)
        self.assertGreater(result.new_interval, 0)
        self.assertIsNotNone(card.last_review)
        self.assertGreater(card.due, now)


class TestLeitnerScheduler(unittest.TestCase):
    """Test Leitner system implementation."""
    
    def test_initialization(self):
        """Test scheduler initialization."""
        scheduler = LeitnerScheduler()
        
        self.assertEqual(scheduler.num_boxes, 8)
        self.assertEqual(len(scheduler.intervals), 8)
    
    def test_custom_intervals(self):
        """Test custom interval configuration."""
        custom = [0, 1, 2, 4, 8, 16]
        scheduler = LeitnerScheduler(intervals=custom)
        
        self.assertEqual(scheduler.get_interval_for_box(0), 0)
        self.assertEqual(scheduler.get_interval_for_box(1), 1)
        self.assertEqual(scheduler.get_interval_for_box(5), 16)
    
    def test_box_promotion(self):
        """Test correct answer moves card up."""
        scheduler = LeitnerScheduler()
        
        # Box 0 -> Box 1
        self.assertEqual(scheduler.get_next_box(0, correct=True), 1)
        
        # Box 3 -> Box 4
        self.assertEqual(scheduler.get_next_box(3, correct=True), 4)
        
        # Box 7 stays at 7 (max)
        self.assertEqual(scheduler.get_next_box(7, correct=True), 7)
    
    def test_box_demotion(self):
        """Test wrong answer moves card to box 0."""
        scheduler = LeitnerScheduler()
        
        # Any box -> Box 0 on failure
        self.assertEqual(scheduler.get_next_box(0, correct=False), 0)
        self.assertEqual(scheduler.get_next_box(3, correct=False), 0)
        self.assertEqual(scheduler.get_next_box(7, correct=False), 0)
    
    def test_interval_for_box(self):
        """Test interval lookup for each box."""
        scheduler = LeitnerScheduler()
        
        self.assertEqual(scheduler.get_interval_for_box(0), 0)
        self.assertEqual(scheduler.get_interval_for_box(1), 1)
        self.assertEqual(scheduler.get_interval_for_box(2), 3)
        self.assertEqual(scheduler.get_interval_for_box(3), 7)
    
    def test_due_date_calculation(self):
        """Test due date calculation."""
        scheduler = LeitnerScheduler()
        now = datetime.now()
        
        due_box0 = scheduler.get_due_date(0, now)
        self.assertEqual(due_box0, now)  # Box 0 is due immediately
        
        due_box1 = scheduler.get_due_date(1, now)
        self.assertEqual(due_box1, now + timedelta(days=1))
        
        due_box3 = scheduler.get_due_date(3, now)
        self.assertEqual(due_box3, now + timedelta(days=7))
    
    def test_review_card(self):
        """Test Leitner review updates."""
        scheduler = LeitnerScheduler()
        now = datetime.now()
        
        card = Card(id="test", front="Q", back="A", leitner_box=0)
        
        # Correct answer
        result = scheduler.review_card(card, Rating.GOOD, now)
        self.assertEqual(card.leitner_box, 1)
        self.assertEqual(result.new_box, 1)
        self.assertEqual(result.previous_box, 0)
        
        # Wrong answer
        card.leitner_box = 3
        result = scheduler.review_card(card, Rating.AGAIN, now)
        self.assertEqual(card.leitner_box, 0)
        self.assertEqual(card.lapses, 1)


class TestDeck(unittest.TestCase):
    """Test Deck class."""
    
    def test_deck_creation(self):
        """Test deck initialization."""
        deck = Deck(name="test-deck")
        
        self.assertEqual(deck.name, "test-deck")
        self.assertEqual(len(deck.cards), 0)
        self.assertEqual(len(deck.review_history), 0)
        self.assertIsNotNone(deck.created)
    
    def test_add_remove_cards(self):
        """Test adding and removing cards."""
        deck = Deck(name="test")
        
        card = Card(id="card-1", front="Q", back="A")
        deck.add_card(card)
        
        self.assertEqual(len(deck.cards), 1)
        self.assertEqual(deck.get_card("card-1"), card)
        self.assertEqual(card.deck, "test")
        
        # Remove card
        removed = deck.remove_card("card-1")
        self.assertEqual(removed, card)
        self.assertEqual(len(deck.cards), 0)
        
        # Remove non-existent
        removed = deck.remove_card("nonexistent")
        self.assertIsNone(removed)
    
    def test_get_due_cards(self):
        """Test getting due cards."""
        deck = Deck(name="test")
        now = datetime.now()
        
        # Due card
        due_card = Card(
            id="due",
            front="Q",
            back="A",
            due=now - timedelta(days=1),
        )
        
        # Future card
        future_card = Card(
            id="future",
            front="Q",
            back="A",
            due=now + timedelta(days=1),
        )
        
        deck.add_card(due_card)
        deck.add_card(future_card)
        
        due = deck.get_due_cards(now)
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0].id, "due")
    
    def test_get_new_cards(self):
        """Test getting new cards."""
        deck = Deck(name="test")
        
        new_card = Card(id="new", front="Q", back="A", repetitions=0)
        reviewed_card = Card(id="reviewed", front="Q", back="A", repetitions=3)
        
        deck.add_card(new_card)
        deck.add_card(reviewed_card)
        
        new_cards = deck.get_new_cards()
        self.assertEqual(len(new_cards), 1)
        self.assertEqual(new_cards[0].id, "new")
    
    def test_get_cards_by_tag(self):
        """Test filtering by tag."""
        deck = Deck(name="test")
        
        card1 = Card(id="1", front="Q", back="A", tags=["math", "basic"])
        card2 = Card(id="2", front="Q", back="A", tags=["science"])
        card3 = Card(id="3", front="Q", back="A", tags=["math", "advanced"])
        
        deck.add_card(card1)
        deck.add_card(card2)
        deck.add_card(card3)
        
        math_cards = deck.get_cards_by_tag("math")
        self.assertEqual(len(math_cards), 2)
        
        basic_cards = deck.get_cards_by_tag("basic")
        self.assertEqual(len(basic_cards), 1)
    
    def test_statistics(self):
        """Test deck statistics."""
        deck = Deck(name="test")
        
        # Empty deck
        stats = deck.get_statistics()
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['new'], 0)
        self.assertEqual(stats['retention_rate'], 0)
        
        # Add cards
        now = datetime.now()
        card1 = Card(id="1", front="Q", back="A", repetitions=0)
        card2 = Card(id="2", front="Q", back="A", repetitions=3, interval=5)
        card3 = Card(id="3", front="Q", back="A", repetitions=1, interval=0.5)
        card3.lapses = 2
        
        deck.add_card(card1)
        deck.add_card(card2)
        deck.add_card(card3)
        
        stats = deck.get_statistics()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['new'], 1)  # card1
        self.assertEqual(stats['learning'], 1)  # card3
        self.assertEqual(stats['review'], 1)  # card2
        self.assertEqual(stats['lapses'], 2)
    
    def test_serialization(self):
        """Test deck to_dict and from_dict."""
        deck = Deck(name="test-deck")
        card = Card(id="1", front="Q", back="A")
        deck.add_card(card)
        
        data = deck.to_dict()
        self.assertEqual(data['name'], "test-deck")
        self.assertIn('1', data['cards'])
        
        restored = Deck.from_dict(data)
        self.assertEqual(restored.name, "test-deck")
        self.assertIn('1', restored.cards)


class TestSpacedRepetition(unittest.TestCase):
    """Test main SpacedRepetition class."""
    
    def test_initialization_sm2(self):
        """Test initialization with SM-2 scheduler."""
        sr = SpacedRepetition(scheduler="sm2")
        
        self.assertEqual(sr.scheduler_type, "sm2")
        self.assertIsInstance(sr.scheduler, SM2Scheduler)
    
    def test_initialization_leitner(self):
        """Test initialization with Leitner scheduler."""
        sr = SpacedRepetition(scheduler="leitner")
        
        self.assertEqual(sr.scheduler_type, "leitner")
        self.assertIsInstance(sr.scheduler, LeitnerScheduler)
    
    def test_create_deck(self):
        """Test deck creation."""
        sr = SpacedRepetition()
        deck = sr.create_deck("vocabulary")
        
        self.assertEqual(deck.name, "vocabulary")
        self.assertIn("vocabulary", sr.decks)
    
    def test_create_card(self):
        """Test card creation."""
        sr = SpacedRepetition()
        card = sr.create_card(
            front="What is the capital of France?",
            back="Paris",
            deck="geography",
            tags=["europe", "capitals"],
        )
        
        self.assertIsNotNone(card.id)
        self.assertEqual(card.front, "What is the capital of France?")
        self.assertEqual(card.back, "Paris")
        self.assertEqual(card.deck, "geography")
        self.assertIn("europe", card.tags)
        self.assertIn("capitals", card.tags)
        self.assertIn("geography", sr.decks)
    
    def test_review_card(self):
        """Test reviewing a card."""
        sr = SpacedRepetition(scheduler="sm2")
        card = sr.create_card("Q", "A", deck="test")
        
        result = sr.review_card(card, Rating.GOOD)
        
        self.assertEqual(result.rating, Rating.GOOD)
        self.assertGreater(result.new_interval, 0)
        self.assertEqual(card.repetitions, 1)
    
    def test_get_due_cards(self):
        """Test getting due cards."""
        sr = SpacedRepetition()
        now = datetime.now()
        
        # Create due and future cards
        due_card = sr.create_card("Due", "A")
        due_card.due = now - timedelta(days=1)
        
        future_card = sr.create_card("Future", "A")
        future_card.due = now + timedelta(days=1)
        
        due = sr.get_due_cards(deck_name="default", now=now)
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0].id, due_card.id)
    
    def test_statistics(self):
        """Test overall statistics."""
        sr = SpacedRepetition()
        
        # Create multiple decks
        sr.create_card("Q1", "A1", deck="deck1")
        sr.create_card("Q2", "A2", deck="deck2")
        
        stats = sr.get_statistics()
        
        self.assertEqual(stats['total_cards'], 2)
        self.assertEqual(stats['total_new'], 2)
        self.assertIn('deck1', stats['decks'])
        self.assertIn('deck2', stats['decks'])
    
    def test_export_import(self):
        """Test JSON export and import."""
        sr = SpacedRepetition(scheduler="sm2")
        
        sr.create_card("Q1", "A1", deck="test")
        sr.create_card("Q2", "A2", deck="test")
        
        # Export
        json_str = sr.export_to_json()
        self.assertIn('"scheduler": "sm2"', json_str)
        self.assertIn('"test"', json_str)
        
        # Import to new instance
        sr2 = SpacedRepetition()
        sr2.import_from_json(json_str)
        
        self.assertIn("test", sr2.decks)
        self.assertEqual(len(sr2.decks["test"].cards), 2)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_calculate_retention(self):
        """Test retention calculation."""
        # Create mock reviews
        now = datetime.now()
        card = Card(id="test", front="Q", back="A")
        
        reviews = [
            ReviewResult(card, Rating.GOOD, 1, 2, 0, 1, now),
            ReviewResult(card, Rating.GOOD, 2, 3, 1, 2, now),
            ReviewResult(card, Rating.AGAIN, 3, 0, 2, 0, now),
            ReviewResult(card, Rating.EASY, 0, 4, 0, 1, now),
        ]
        
        retention = calculate_retention(reviews)
        # 3 out of 4 are GOOD or EASY
        self.assertEqual(retention, 75.0)
    
    def test_calculate_retention_empty(self):
        """Test retention with no reviews."""
        retention = calculate_retention([])
        self.assertEqual(retention, 0.0)
    
    def test_calculate_retention_with_period(self):
        """Test retention with time period filter."""
        now = datetime.now()
        card = Card(id="test", front="Q", back="A")
        
        # Old review (more than 7 days ago)
        old_review = ReviewResult(
            card, Rating.GOOD, 1, 2, 0, 1,
            now - timedelta(days=10),
        )
        
        # Recent review
        recent_review = ReviewResult(
            card, Rating.AGAIN, 2, 0, 1, 0,
            now - timedelta(days=2),
        )
        
        # Without period filter
        retention_all = calculate_retention([old_review, recent_review])
        self.assertEqual(retention_all, 50.0)
        
        # With 7-day period filter
        retention_recent = calculate_retention(
            [old_review, recent_review], period_days=7
        )
        self.assertEqual(retention_recent, 0.0)  # Only the AGAIN counts
    
    def test_predict_forgetting_curve(self):
        """Test forgetting curve prediction."""
        # Just reviewed - high recall
        p0 = predict_forgetting_curve(0, stability=10)
        self.assertAlmostEqual(p0, 1.0, places=2)
        
        # Half stability - ~37% recall
        p_half = predict_forgetting_curve(10, stability=10)
        self.assertAlmostEqual(p_half, 0.368, places=2)
        
        # Double stability - ~13% recall
        p_double = predict_forgetting_curve(20, stability=10)
        self.assertAlmostEqual(p_double, 0.135, places=2)
    
    def test_calculate_optimal_review_time(self):
        """Test optimal review time calculation."""
        # Stability of 10 days, 90% retention target
        days = calculate_optimal_review_time(10, target_retention=0.9)
        self.assertGreater(days, 0)
        self.assertLess(days, 10)  # Should be before stability period
        
        # Higher retention = sooner review
        days_90 = calculate_optimal_review_time(10, target_retention=0.9)
        days_80 = calculate_optimal_review_time(10, target_retention=0.8)
        self.assertLess(days_90, days_80)
    
    def test_generate_review_schedule(self):
        """Test review schedule generation."""
        now = datetime.now()
        
        cards = [
            Card(id="new1", front="Q1", back="A1", repetitions=0),
            Card(id="new2", front="Q2", back="A2", repetitions=0),
            Card(
                id="due1", front="Q3", back="A3",
                due=now - timedelta(days=1),
                repetitions=2,
            ),
        ]
        
        schedule = generate_review_schedule(cards, now=now, max_per_day=2)
        
        self.assertIsInstance(schedule, dict)
        # Should have at least one day scheduled
        self.assertGreater(len(schedule), 0)
    
    def test_calculate_card_priority(self):
        """Test card priority calculation."""
        now = datetime.now()
        
        # Overdue card
        overdue = Card(
            id="overdue",
            front="Q",
            back="A",
            due=now - timedelta(days=5),
            lapses=2,
        )
        
        # Future card
        future = Card(
            id="future",
            front="Q",
            back="A",
            due=now + timedelta(days=5),
        )
        
        # New card
        new = Card(
            id="new",
            front="Q",
            back="A",
            due=now,
            repetitions=0,
        )
        
        priority_overdue = calculate_card_priority(overdue, now)
        priority_future = calculate_card_priority(future, now)
        priority_new = calculate_card_priority(new, now)
        
        # Overdue should have highest priority
        self.assertGreater(priority_overdue, priority_future)
        self.assertGreater(priority_overdue, priority_new)
    
    def test_sort_cards_by_priority(self):
        """Test sorting cards by priority."""
        now = datetime.now()
        
        cards = [
            Card(id="low", front="Q", back="A", due=now + timedelta(days=10)),
            Card(id="high", front="Q", back="A", due=now - timedelta(days=5)),
            Card(id="medium", front="Q", back="A", due=now - timedelta(days=1)),
        ]
        
        sorted_cards = sort_cards_by_priority(cards, now)
        
        self.assertEqual(sorted_cards[0].id, "high")
        self.assertEqual(sorted_cards[1].id, "medium")
        self.assertEqual(sorted_cards[2].id, "low")


class TestCardCreationHelpers(unittest.TestCase):
    """Test card creation helper functions."""
    
    def test_create_question_card(self):
        """Test simple Q&A card creation."""
        card = create_question_card(
            question="What is 2+2?",
            answer="4",
            deck="math",
            tags=["basic"],
        )
        
        self.assertIsNotNone(card.id)
        self.assertEqual(card.front, "What is 2+2?")
        self.assertEqual(card.back, "4")
        self.assertEqual(card.deck, "math")
        self.assertIn("basic", card.tags)
    
    def test_create_reversable_card(self):
        """Test reversable card creation."""
        card1, card2 = create_reversable_card(
            front="Hello",
            back="你好",
            deck="language",
            tags=["greetings"],
        )
        
        # Card 1: front -> back
        self.assertEqual(card1.front, "Hello")
        self.assertEqual(card1.back, "你好")
        
        # Card 2: back -> front
        self.assertEqual(card2.front, "你好")
        self.assertEqual(card2.back, "Hello")
        
        # Both should have same deck and tags
        self.assertEqual(card1.deck, "language")
        self.assertEqual(card2.deck, "language")
    
    def test_create_cloze_card(self):
        """Test cloze deletion card creation."""
        text = "The capital of France is Paris."
        clozes = [(25, 30)]  # "Paris"
        
        cards = create_cloze_card(text, clozes, deck="geography")
        
        self.assertEqual(len(cards), 1)
        self.assertIn("[...]", cards[0].front)
        self.assertEqual(cards[0].back, "Paris")
    
    def test_create_type_in_card(self):
        """Test type-in answer card creation."""
        card = create_type_in_card(
            prompt="What is the capital of Japan?",
            correct_answers=["Tokyo", "とうきょう"],
            case_sensitive=False,
            deck="geography",
        )
        
        self.assertIn("[Type]", card.front)
        self.assertIn("Tokyo", card.back)
        self.assertIn("case_insensitive", card.tags)
    
    def test_check_type_in_answer(self):
        """Test type-in answer checking."""
        card = create_type_in_card(
            prompt="Capital of France?",
            correct_answers=["Paris"],
            case_sensitive=False,
        )
        
        # Correct answer
        self.assertTrue(check_type_in_answer(card, "Paris"))
        self.assertTrue(check_type_in_answer(card, "paris"))
        self.assertTrue(check_type_in_answer(card, "PARIS"))
        
        # Wrong answer
        self.assertFalse(check_type_in_answer(card, "London"))
    
    def test_check_type_in_answer_case_sensitive(self):
        """Test case-sensitive answer checking."""
        card = create_type_in_card(
            prompt="Username?",
            correct_answers=["Admin"],
            case_sensitive=True,
        )
        
        # Exact match
        self.assertTrue(check_type_in_answer(card, "Admin"))
        
        # Case mismatch
        self.assertFalse(check_type_in_answer(card, "admin"))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_empty_deck_statistics(self):
        """Test statistics on empty deck."""
        deck = Deck(name="empty")
        stats = deck.get_statistics()
        
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['average_ease_factor'], 0)
        self.assertEqual(stats['average_interval'], 0)
    
    def test_card_with_empty_tags(self):
        """Test card with no tags."""
        card = Card(id="test", front="Q", back="A", tags=[])
        self.assertEqual(card.tags, [])
    
    def test_card_with_special_characters(self):
        """Test card with special characters."""
        card = Card(
            id="special",
            front="What is π?",
            back="≈ 3.14159",
        )
        
        data = card.to_dict()
        restored = Card.from_dict(data)
        
        self.assertEqual(restored.front, "What is π?")
        self.assertEqual(restored.back, "≈ 3.14159")
    
    def test_card_with_multiline_content(self):
        """Test card with multiline content."""
        card = Card(
            id="multiline",
            front="List the planets:",
            back="1. Mercury\n2. Venus\n3. Earth\n4. Mars",
        )
        
        data = card.to_dict()
        restored = Card.from_dict(data)
        
        self.assertIn("\n", restored.back)
        self.assertIn("Mercury", restored.back)
    
    def test_zero_stability_forgetting_curve(self):
        """Test forgetting curve with zero stability."""
        # Should not raise error
        p = predict_forgetting_curve(1, stability=0)
        self.assertGreaterEqual(p, 0)
        self.assertLessEqual(p, 1)
    
    def test_negative_days_overdue(self):
        """Test days_overdue with future due date."""
        now = datetime.now()
        card = Card(
            id="future",
            front="Q",
            back="A",
            due=now + timedelta(days=5),
        )
        
        # Should return 0, not negative
        overdue = card.days_overdue(now)
        self.assertEqual(overdue, 0)
    
    def test_very_high_repetitions(self):
        """Test card with high repetition count."""
        scheduler = SM2Scheduler()
        now = datetime.now()
        
        card = Card(
            id="mature",
            front="Q",
            back="A",
            interval=365,
            repetitions=100,
            ease_factor=2.5,
        )
        
        # Should handle high repetition count
        interval, reps, ef = scheduler.calculate_interval(card, Rating.GOOD, now)
        
        self.assertGreater(interval, 365)
        self.assertEqual(reps, 101)
    
    def test_minimum_ease_factor(self):
        """Test ease factor doesn't go below minimum."""
        scheduler = SM2Scheduler(min_ease_factor=1.3)
        
        ef = 1.31  # Just above minimum
        new_ef = scheduler.calculate_ease_factor(ef, Rating.AGAIN)
        
        # Should be at least minimum
        self.assertGreaterEqual(new_ef, 1.3)


class TestMultipleReviews(unittest.TestCase):
    """Test multiple review scenarios."""
    
    def test_review_sequence(self):
        """Test a sequence of reviews."""
        sr = SpacedRepetition(scheduler="sm2")
        now = datetime.now()
        
        card = sr.create_card("Capital of France?", "Paris")
        
        # Review sequence: Again, Good, Good, Good, Good, Easy
        # Again resets, then Good reviews build up
        reviews = [Rating.AGAIN, Rating.GOOD, Rating.GOOD, Rating.GOOD, Rating.GOOD, Rating.EASY]
        intervals = []
        
        for rating in reviews:
            result = sr.review_card(card, rating, now=now)
            intervals.append(result.new_interval)
            now = card.due
        
        # First interval (AGAIN) = 0 (reset)
        # Then building up intervals
        self.assertEqual(intervals[0], 0)  # Again resets
        self.assertEqual(intervals[1], 1.0)  # First good after reset
        self.assertEqual(intervals[2], 1.0)  # Second good (still graduating)
        # After that, intervals should increase
        self.assertGreater(intervals[3], intervals[2])
        self.assertGreater(intervals[4], intervals[3])
        self.assertGreater(intervals[5], intervals[4])  # Easy gives biggest boost
    
    def test_leitner_progression(self):
        """Test progression through Leitner boxes."""
        sr = SpacedRepetition(scheduler="leitner")
        
        card = sr.create_card("Q", "A")
        
        # All correct answers should progress through boxes
        for expected_box in range(8):
            self.assertEqual(card.leitner_box, expected_box)
            sr.review_card(card, Rating.GOOD)
        
        # Should stay at max box
        self.assertEqual(card.leitner_box, 7)
        sr.review_card(card, Rating.EASY)
        self.assertEqual(card.leitner_box, 7)
    
    def test_mixed_ratings(self):
        """Test mixed good and bad ratings."""
        sr = SpacedRepetition(scheduler="leitner")
        
        card = sr.create_card("Q", "A")
        
        # Good, Good, Again, Good, Good, Good
        ratings = [
            Rating.GOOD, Rating.GOOD, Rating.AGAIN,
            Rating.GOOD, Rating.GOOD, Rating.GOOD,
        ]
        
        expected_boxes = [1, 2, 0, 1, 2, 3]
        
        for rating, expected in zip(ratings, expected_boxes):
            sr.review_card(card, rating)
            self.assertEqual(card.leitner_box, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)