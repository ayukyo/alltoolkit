"""
Spaced Repetition Utilities - Usage Examples

Demonstrates how to use the spaced repetition module for:
- Basic card creation and review
- SM-2 and Leitner scheduling
- Deck management and statistics
- Card creation helpers
- Export and import
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from mod import (
    Rating, Card, Deck,
    SM2Scheduler, LeitnerScheduler,
    SpacedRepetition,
    calculate_retention, predict_forgetting_curve,
    calculate_optimal_review_time, generate_review_schedule,
    calculate_card_priority, sort_cards_by_priority,
    create_question_card, create_reversable_card,
    create_cloze_card, create_type_in_card, check_type_in_answer,
)


def example_basic_usage():
    """Basic usage example with SpacedRepetition class."""
    print("\n=== Basic Usage Example ===\n")
    
    # Create spaced repetition system with SM-2 algorithm
    sr = SpacedRepetition(scheduler="sm2")
    
    # Create some flashcards
    cards = [
        sr.create_card(
            front="What is the capital of France?",
            back="Paris",
            deck="geography",
            tags=["europe", "capitals"],
        ),
        sr.create_card(
            front="What is the capital of Japan?",
            back="Tokyo",
            deck="geography",
            tags=["asia", "capitals"],
        ),
        sr.create_card(
            front="What is 2 + 2?",
            back="4",
            deck="math",
            tags=["basic"],
        ),
    ]
    
    print(f"Created {len(cards)} cards in decks:")
    for deck_name in sr.decks:
        deck = sr.decks[deck_name]
        print(f"  - {deck_name}: {len(deck.cards)} cards")
    
    # Get statistics
    stats = sr.get_statistics()
    print(f"\nOverall statistics:")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  New cards: {stats['total_new']}")
    
    # Review a card
    card = cards[0]
    print(f"\nReviewing card: '{card.front}'")
    
    # User rates the answer as "Good"
    result = sr.review_card(card, Rating.GOOD)
    
    print(f"  Rating: {Rating(result.rating).name}")
    print(f"  Previous interval: {result.previous_interval} days")
    print(f"  New interval: {result.new_interval} days")
    print(f"  Next review: {card.due.strftime('%Y-%m-%d')}")
    print(f"  Ease factor: {card.ease_factor:.2f}")
    
    # Continue reviewing with different ratings
    print("\n\nContinuing with more reviews:")
    
    for rating in [Rating.GOOD, Rating.EASY, Rating.HARD]:
        result = sr.review_card(card, rating)
        print(f"  Rating: {Rating(result.rating).name} -> Interval: {result.new_interval:.1f} days")


def example_sm2_scheduler():
    """SM-2 algorithm detailed example."""
    print("\n=== SM-2 Scheduler Example ===\n")
    
    scheduler = SM2Scheduler()
    
    # Create a new card
    card = Card(
        id="vocab-1",
        front="Bonjour",
        back="Hello (French)",
        deck="vocabulary",
        tags=["french", "greetings"],
    )
    
    print("Starting with a new card:")
    print(f"  Front: {card.front}")
    print(f"  Back: {card.back}")
    print(f"  Initial interval: {card.interval} days")
    print(f"  Ease factor: {card.ease_factor}")
    
    # Simulate a learning session
    print("\n\nSimulating learning session:")
    ratings = [Rating.AGAIN, Rating.GOOD, Rating.GOOD, Rating.GOOD, Rating.EASY]
    
    for i, rating in enumerate(ratings):
        result = scheduler.review_card(card, rating)
        print(f"\n  Review #{i+1}: Rating = {Rating(rating).name}")
        print(f"    Interval: {result.new_interval:.1f} days")
        print(f"    Repetitions: {card.repetitions}")
        print(f"    Ease factor: {card.ease_factor:.2f}")
        print(f"    Lapses: {card.lapses}")


def example_leitner_system():
    """Leitner system example."""
    print("\n=== Leitner System Example ===\n")
    
    scheduler = LeitnerScheduler()
    
    print("Leitner system intervals:")
    for box in range(8):
        interval = scheduler.get_interval_for_box(box)
        print(f"  Box {box+1}: Review every {interval} days")
    
    # Create a card and simulate progression
    card = Card(id="word-1", front="Apple", back="苹果")
    
    print("\n\nCard progression through Leitner boxes:")
    print(f"  Starting in Box 1")
    
    # Simulate correct answers
    for _ in range(7):  # Move through all boxes
        result = scheduler.review_card(card, Rating.GOOD)
        print(f"    Correct answer -> Box {card.leitner_box + 1}, next review in {card.interval} days")
    
    # Simulate a mistake
    print("\n  Making a mistake...")
    result = scheduler.review_card(card, Rating.AGAIN)
    print(f"    Wrong answer -> Back to Box 1, lapses: {card.lapses}")


def example_deck_management():
    """Deck management example."""
    print("\n=== Deck Management Example ===\n")
    
    sr = SpacedRepetition(scheduler="sm2")
    
    # Create multiple decks
    decks = ["vocabulary", "geography", "science", "history"]
    
    for deck_name in decks:
        sr.create_deck(deck_name)
    
    # Add cards to each deck
    vocabulary_cards = [
        ("Hello", "你好"),
        ("Goodbye", "再见"),
        ("Thank you", "谢谢"),
    ]
    
    for front, back in vocabulary_cards:
        sr.create_card(front, back, deck="vocabulary", tags=["chinese"])
    
    geography_cards = [
        ("Capital of USA?", "Washington D.C."),
        ("Capital of UK?", "London"),
        ("Capital of Germany?", "Berlin"),
    ]
    
    for front, back in geography_cards:
        sr.create_card(front, back, deck="geography", tags=["capitals"])
    
    print("Created decks with cards:")
    for deck_name in sr.decks:
        stats = sr.decks[deck_name].get_statistics()
        print(f"  {deck_name}: {stats['total']} cards, {stats['new']} new")
    
    # Review some cards
    print("\n\nReviewing vocabulary cards:")
    vocab_deck = sr.decks["vocabulary"]
    cards = list(vocab_deck.cards.values())
    
    for card in cards[:2]:  # Review first 2 cards
        result = sr.review_card(card, Rating.GOOD)
        print(f"  '{card.front}' -> interval: {result.new_interval:.1f} days")
    
    # Get statistics for vocabulary deck
    stats = vocab_deck.get_statistics()
    print(f"\nVocabulary deck statistics:")
    print(f"  Total: {stats['total']}")
    print(f"  New: {stats['new']}")
    print(f"  Learning: {stats['learning']}")
    print(f"  Review: {stats['review']}")
    print(f"  Average ease factor: {stats['average_ease_factor']}")


def example_card_creation_helpers():
    """Card creation helper functions example."""
    print("\n=== Card Creation Helpers ===\n")
    
    # Simple Q&A card
    card1 = create_question_card(
        question="What is the speed of light?",
        answer="299,792,458 m/s",
        deck="physics",
        tags=["constants"],
    )
    print("Q&A Card:")
    print(f"  Front: {card1.front}")
    print(f"  Back: {card1.back}")
    
    # Reversable card (for vocabulary)
    card2, card3 = create_reversable_card(
        front="Cat",
        back="猫",
        deck="vocabulary",
        tags=["animals", "chinese"],
    )
    print("\nReversable Cards:")
    print(f"  Card 1: {card2.front} -> {card2.back}")
    print(f"  Card 2: {card3.front} -> {card3.back}")
    
    # Cloze deletion cards
    text = "The Battle of Hastings occurred in 1066."
    clozes = [(34, 38)]  # "1066"
    cloze_cards = create_cloze_card(text, clozes, deck="history")
    print("\nCloze Card:")
    print(f"  Front: {cloze_cards[0].front}")
    print(f"  Back: {cloze_cards[0].back}")
    
    # Type-in answer card
    type_card = create_type_in_card(
        prompt="What is the chemical symbol for water?",
        correct_answers=["H2O", "H₂O"],
        case_sensitive=False,
        deck="chemistry",
    )
    print("\nType-in Card:")
    print(f"  Front: {type_card.front}")
    print(f"  Acceptable answers: {type_card.back}")
    
    # Check answers
    print("\n  Testing answers:")
    print(f"    'H2O' -> {check_type_in_answer(type_card, 'H2O')}")
    print(f"    'h2o' -> {check_type_in_answer(type_card, 'h2o')}")
    print(f"    'CO2' -> {check_type_in_answer(type_card, 'CO2')}")


def example_forgetting_curve():
    """Forgetting curve and optimal review time example."""
    print("\n=== Forgetting Curve Analysis ===\n")
    
    stabilities = [1, 5, 10, 30, 100]  # Days
    
    print("Recall probability over time:")
    print("Days | Stability 1 | Stability 5 | Stability 10 | Stability 30")
    print("-" * 60)
    
    for days in [0, 1, 3, 7, 14, 30]:
        probs = []
        for stability in [1, 5, 10, 30]:
            prob = predict_forgetting_curve(days, stability)
            probs.append(f"{prob:.1%}")
        print(f"{days:4} | {probs[0]:11} | {probs[1]:11} | {probs[2]:12} | {probs[3]}")
    
    # Calculate optimal review times
    print("\n\nOptimal review times for 90% retention:")
    for stability in [1, 5, 10, 30, 100]:
        days = calculate_optimal_review_time(stability, target_retention=0.9)
        print(f"  Stability {stability} days -> Review in {days} days")


def example_review_schedule():
    """Review schedule generation example."""
    print("\n=== Review Schedule Generation ===\n")
    
    now = datetime.now()
    
    # Create various cards
    cards = [
        # New cards
        Card(id="new-1", front="N1", back="A1", repetitions=0, due=now),
        Card(id="new-2", front="N2", back="A2", repetitions=0, due=now),
        Card(id="new-3", front="N3", back="A3", repetitions=0, due=now),
        
        # Due cards (overdue by different amounts)
        Card(id="due-1", front="D1", back="A1", repetitions=5, due=now - timedelta(days=2)),
        Card(id="due-2", front="D2", back="A2", repetitions=10, due=now - timedelta(days=1)),
        Card(id="due-3", front="D3", back="A3", repetitions=3, due=now - timedelta(days=5)),
        
        # Future cards
        Card(id="future-1", front="F1", back="A1", repetitions=8, due=now + timedelta(days=3)),
    ]
    
    # Generate schedule
    schedule = generate_review_schedule(cards, now=now, max_per_day=3, spread_new_cards=True)
    
    print("Generated review schedule (max 3 cards/day):")
    for date_str, card_ids in schedule.items():
        print(f"  {date_str}: {len(card_ids)} cards")
        print(f"    Card IDs: {card_ids}")


def example_card_priority():
    """Card priority calculation example."""
    print("\n=== Card Priority Example ===\n")
    
    now = datetime.now()
    
    cards = [
        # Highly overdue card
        Card(
            id="urgent-1",
            front="U1",
            back="A1",
            due=now - timedelta(days=10),
            lapses=3,
            ease_factor=1.5,
        ),
        
        # Slightly overdue card
        Card(
            id="overdue-1",
            front="O1",
            back="A1",
            due=now - timedelta(days=2),
            lapses=1,
            ease_factor=2.3,
        ),
        
        # Due today
        Card(
            id="today-1",
            front="T1",
            back="A1",
            due=now,
            repetitions=5,
            ease_factor=2.5,
        ),
        
        # New card
        Card(
            id="new-1",
            front="N1",
            back="A1",
            due=now,
            repetitions=0,
        ),
        
        # Future card
        Card(
            id="future-1",
            front="F1",
            back="A1",
            due=now + timedelta(days=5),
        ),
    ]
    
    print("Card priorities (higher = more urgent):")
    for card in cards:
        priority = calculate_card_priority(card, now)
        print(f"  {card.id}: Priority {priority:.1f}")
    
    # Sort by priority
    sorted_cards = sort_cards_by_priority(cards, now)
    
    print("\n\nSorted by priority (highest first):")
    for card in sorted_cards:
        priority = calculate_card_priority(card, now)
        print(f"  {card.id}: Priority {priority:.1f}")


def example_export_import():
    """Export and import example."""
    print("\n=== Export and Import ===\n")
    
    # Create a system with cards
    sr = SpacedRepetition(scheduler="sm2")
    
    sr.create_card("Capital of Italy?", "Rome", deck="geography")
    sr.create_card("Capital of Spain?", "Madrid", deck="geography")
    sr.create_card("What is H2O?", "Water", deck="chemistry")
    
    # Review some cards
    geo_deck = sr.decks["geography"]
    for card in list(geo_deck.cards.values()):
        sr.review_card(card, Rating.GOOD)
    
    print("Before export:")
    stats = sr.get_statistics()
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Decks: {list(sr.decks.keys())}")
    
    # Export to JSON
    json_data = sr.export_to_json()
    
    print("\n\nExported JSON (truncated):")
    print(json_data[:300] + "...\n")
    
    # Import to new system
    sr2 = SpacedRepetition()
    sr2.import_from_json(json_data)
    
    print("After import:")
    stats2 = sr2.get_statistics()
    print(f"  Total cards: {stats2['total_cards']}")
    print(f"  Decks: {list(sr2.decks.keys())}")


def example_full_workflow():
    """Complete workflow example."""
    print("\n=== Full Learning Workflow ===\n")
    
    # Initialize system
    sr = SpacedRepetition(scheduler="sm2")
    
    # Create vocabulary deck
    words = [
        ("apple", "苹果"),
        ("banana", "香蕉"),
        ("orange", "橙子"),
        ("watermelon", "西瓜"),
        ("grape", "葡萄"),
    ]
    
    for english, chinese in words:
        sr.create_card(english, chinese, deck="fruit-vocab", tags=["fruit", "chinese"])
    
    print(f"Created vocabulary deck with {len(words)} words")
    
    # Simulate a learning session
    print("\n\nSimulating daily learning session:")
    
    due_cards = sr.get_due_cards("fruit-vocab")
    print(f"Cards due today: {len(due_cards)}")
    
    # Simulate different outcomes
    ratings_sequence = [
        Rating.AGAIN, Rating.GOOD, Rating.GOOD, Rating.EASY, Rating.GOOD,
    ]
    
    for i, (card, rating) in enumerate(zip(due_cards, ratings_sequence)):
        result = sr.review_card(card, rating)
        print(f"\n  Card: '{card.front}'")
        print(f"    Rating: {Rating(rating).name}")
        print(f"    Next interval: {result.new_interval:.1f} days")
        print(f"    Next review: {card.due.strftime('%Y-%m-%d')}")
    
    # Show statistics
    stats = sr.get_statistics("fruit-vocab")
    print("\n\nDeck statistics after session:")
    print(f"  Total cards: {stats['total']}")
    print(f"  New cards remaining: {stats['new']}")
    print(f"  Cards in learning: {stats['learning']}")
    print(f"  Mature cards: {stats['review']}")
    print(f"  Total lapses: {stats['lapses']}")
    print(f"  Average ease factor: {stats['average_ease_factor']}")
    
    # Predict forgetting
    print("\n\nMemory predictions:")
    for card in list(sr.decks["fruit-vocab"].cards.values())[:3]:
        days_since = (datetime.now() - card.last_review).days if card.last_review else 0
        if card.interval > 0:
            recall_prob = predict_forgetting_curve(days_since, card.interval)
            print(f"  '{card.front}': {recall_prob:.1%} recall probability")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Spaced Repetition Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_sm2_scheduler()
    example_leitner_system()
    example_deck_management()
    example_card_creation_helpers()
    example_forgetting_curve()
    example_review_schedule()
    example_card_priority()
    example_export_import()
    example_full_workflow()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()