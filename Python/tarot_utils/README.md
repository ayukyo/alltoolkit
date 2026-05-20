# Tarot Utilities

A comprehensive tarot card reading and divination toolkit for Python.

## Features

- **Complete 78-card tarot deck** - All Major Arcana (22 cards) and Minor Arcana (56 cards)
- **Multiple spread layouts** - Celtic Cross, Three Card, Relationship, Decision, Daily, Horseshoe, Monthly
- **Card meanings** - Detailed interpretations for both upright and reversed positions
- **Daily draws** - Reproducible daily card based on date
- **Card search** - Find cards by keywords, suits, or arcana type
- **Zero dependencies** - Pure Python implementation

## Installation

No installation needed - just import the module:

```python
from tarot_utils.mod import TarotReader, quick_reading
```

## Quick Start

### One Card Reading

```python
from tarot_utils.mod import quick_reading

# Simple one-card draw
reading = quick_reading("one_card", question="What should I focus on today?")
print(reading.get_summary())
```

### Three Card Reading

```python
# Classic Past-Present-Future spread
reading = quick_reading("three_card", question="What's my career path?")
print(reading.get_summary())

# Custom positions
reader = TarotReader()
reading = reader.three_card_reading(positions=["Mind", "Body", "Spirit"])
```

### Celtic Cross Reading

```python
# Full 10-card Celtic Cross spread
reader = TarotReader(seed=42)  # Optional seed for reproducibility
reading = reader.celtic_cross_reading(question="What are my life themes?")
print(reading.get_summary())
```

## API Reference

### Classes

#### TarotDeck

Complete 78-card tarot deck.

```python
deck = TarotDeck()

# Get cards
major = deck.get_major_arcana()  # 22 Major Arcana cards
minor = deck.get_minor_arcana()  # 56 Minor Arcana cards
wands = deck.get_by_suit(Suit.WANDS)  # All Wands cards

# Find specific card
card = deck.get_card("The Fool")
```

#### TarotCard

Represents a single tarot card.

```python
card = deck.get_card("The Magician")

# Properties
card.name           # "The Magician"
card.arcana         # Arcana.MAJOR
card.keywords       # ["manifestation", "resourcefulness", ...]
card.upright_meaning  # Full upright interpretation
card.reversed_meaning # Full reversed interpretation
card.element        # "Air"
card.zodiac         # "Mercury"

# Get meaning based on orientation
meaning = card.get_meaning(Orientation.UPRIGHT)
```

#### TarotReader

Main class for performing readings.

```python
reader = TarotReader(seed=42)  # Optional seed for reproducibility

# Available spreads
reader.one_card_reading(question="...")
reader.three_card_reading(positions=None, question="...")
reader.celtic_cross_reading(question="...")
reader.relationship_reading(question="...")
reader.decision_reading(question="...")
reader.daily_reading()
reader.horseshoe_reading(question="...")
reader.monthly_reading()

# Draw random cards
card, orientation = reader.draw_card()
cards = reader.draw_cards(count=5)
```

#### TarotReading

Represents a complete reading.

```python
reading = reader.three_card_reading()

# Properties
reading.spread_type  # SpreadType enum
reading.positions    # List of SpreadPosition objects
reading.timestamp    # datetime object
reading.question     # Optional question string

# Methods
summary = reading.get_summary()  # Human-readable summary
data = reading.to_dict()         # JSON-serializable dict
```

### Convenience Functions

```python
# Quick reading
reading = quick_reading("three_card", question="...")

# Get card by name
card = get_card_by_name("The Star")

# Get card meaning
meaning = get_card_meaning("The Star", reversed=False)

# Daily card (reproducible by date)
card, orientation = daily_card()

# Get cards by type
major = get_major_arcana_cards()
minor = get_minor_arcana_cards()
wands = get_suit_cards("wands")

# Search by keyword
cards = search_cards_by_keyword("love")

# Reading for specific date
reading = reading_for_date(date(2024, 1, 1), "three_card")

# Interpret combination
interpretation = interpret_combination([card1, card2, card3])
```

### Enums

```python
# Card arcana
Arcana.MAJOR  # Major Arcana (22 cards)
Arcana.MINOR  # Minor Arcana (56 cards)

# Minor Arcana suits
Suit.WANDS      # Fire element - creativity, career
Suit.CUPS       # Water element - emotions, relationships
Suit.SWORDS     # Air element - intellect, communication
Suit.PENTACLES  # Earth element - material, finances

# Card orientation
Orientation.UPRIGHT   # Positive interpretation
Orientation.REVERSED  # Shadow/blocked interpretation

# Spread types
SpreadType.ONE_CARD
SpreadType.THREE_CARD
SpreadType.CELTIC_CROSS
SpreadType.RELATIONSHIP
SpreadType.DECISION
SpreadType.DAILY
SpreadType.HORSESHOE
SpreadType.MONTHLY
```

## Spread Layouts

### One Card (1 card)
Simple guidance for a day or question.

### Three Card (3 cards)
- Default: Past, Present, Future
- Customizable positions

### Celtic Cross (10 cards)
1. Present - Current situation
2. Challenge - Obstacle you face
3. Foundation - Root cause
4. Recent Past - Recent influences
5. Possible Future - Potential outcome
6. Near Future - Coming events
7. Your Influence - Your attitude
8. External Influence - Outside forces
9. Hopes and Fears - Expectations
10. Final Outcome - Most likely result

### Relationship (6 cards)
1. You - Your position
2. Partner - Partner's position
3. Connection - What connects you
4. Strengths - Relationship strengths
5. Challenges - Relationship challenges
6. Future - Where it's heading

### Decision (5 cards)
1. Current Situation
2. Option A outcome
3. Option B outcome
4. Hidden Factors
5. Advice

### Daily (6 cards)
Morning, Afternoon, Evening, Focus, Warning, Blessing

### Horseshoe (7 cards)
Past, Present, Hidden Influences, Obstacles, External Influences, Near Future, Outcome

### Monthly (8 cards)
Theme, Week 1-4, Opportunity, Challenge, Advice

## Examples

### Daily Card Routine

```python
from tarot_utils.mod import daily_card, Orientation

card, orientation = daily_card()
print(f"Today's card: {card.name}")
if orientation == Orientation.REVERSED:
    print("(Reversed)")
print(f"Meaning: {card.get_meaning(orientation)}")
```

### Relationship Analysis

```python
from tarot_utils.mod import TarotReader, interpret_combination

reader = TarotReader()
reading = reader.relationship_reading(question="Where is our relationship heading?")

for position in reading.positions:
    print(f"{position.name}: {position.card.name}")
    if position.orientation == Orientation.REVERSED:
        print("  (Reversed)")

# Get combined interpretation
print(interpret_combination([p.card for p in reading.positions]))
```

### Custom Three Card Spread

```python
reader = TarotReader()
reading = reader.three_card_reading(
    positions=["Situation", "Action", "Result"],
    question="Should I move to a new city?"
)
```

### Reproducible Readings

```python
# Same seed = same results
reader1 = TarotReader(seed=123)
reader2 = TarotReader(seed=123)

reading1 = reader1.one_card_reading()
reading2 = reader2.one_card_reading()

# Both readings will have the same card
```

### Search Cards

```python
# Find all cards related to love
love_cards = search_cards_by_keyword("love")
for card in love_cards:
    print(f"{card.name}: {card.keywords}")

# Get all fire element cards (Wands)
fire_cards = get_suit_cards("wands")
```

## Major Arcana Quick Reference

| # | Card | Keywords |
|---|------|----------|
| 0 | The Fool | beginnings, innocence, spontaneity |
| 1 | The Magician | manifestation, resourcefulness, power |
| 2 | The High Priestess | intuition, sacred knowledge, mystery |
| 3 | The Empress | femininity, nurturing, abundance |
| 4 | The Emperor | authority, structure, leadership |
| 5 | The Hierophant | tradition, conformity, wisdom |
| 6 | The Lovers | love, harmony, choices |
| 7 | The Chariot | victory, determination, willpower |
| 8 | Strength | courage, compassion, inner power |
| 9 | The Hermit | introspection, solitude, guidance |
| 10 | Wheel of Fortune | luck, karma, cycles |
| 11 | Justice | fairness, truth, balance |
| 12 | The Hanged Man | sacrifice, perspective, pause |
| 13 | Death | transformation, endings, change |
| 14 | Temperance | harmony, moderation, patience |
| 15 | The Devil | attachment, addiction, shadow |
| 16 | The Tower | upheaval, revelation, awakening |
| 17 | The Star | hope, faith, renewal |
| 18 | The Moon | illusion, intuition, fear |
| 19 | The Sun | joy, success, positivity |
| 20 | Judgement | rebirth, calling, reflection |
| 21 | The World | completion, achievement, integration |

## Suit Meanings

- **Wands (Fire)**: Creativity, action, career, passion
- **Cups (Water)**: Emotions, relationships, intuition, spirituality
- **Swords (Air)**: Intellect, communication, challenges, truth
- **Pentacles (Earth)**: Material matters, finances, security, work

## Testing

Run the test suite:

```bash
python -m pytest tarot_utils_test.py -v
```

Or with unittest:

```bash
python tarot_utils_test.py
```

## License

MIT License - Free to use for any purpose.

## Author

Generated by AllToolkit - 2026-05-20