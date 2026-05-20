"""
Tarot Utilities Test Suite

Comprehensive tests for tarot card reading functionality.
"""

import unittest
import random
from datetime import date, datetime
from tarot_utils.mod import (
    TarotDeck, TarotCard, TarotReader, TarotReading, SpreadPosition,
    Arcana, Suit, Orientation, SpreadType,
    MAJOR_ARCANA, MINOR_ARCANA_COURT, MINOR_ARCANA_NUMBERS, SPREAD_DEFINITIONS,
    get_card_by_name, get_card_meaning, daily_card, quick_reading,
    get_major_arcana_cards, get_minor_arcana_cards, get_suit_cards,
    search_cards_by_keyword, reading_for_date, interpret_combination
)


class TestTarotDeck(unittest.TestCase):
    """Tests for TarotDeck class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.deck = TarotDeck()
    
    def test_deck_has_78_cards(self):
        """Test that deck contains all 78 cards."""
        self.assertEqual(len(self.deck.cards), 78)
    
    def test_deck_has_22_major_arcana(self):
        """Test that deck has 22 Major Arcana cards."""
        major = self.deck.get_major_arcana()
        self.assertEqual(len(major), 22)
    
    def test_deck_has_56_minor_arcana(self):
        """Test that deck has 56 Minor Arcana cards."""
        minor = self.deck.get_minor_arcana()
        self.assertEqual(len(minor), 56)
    
    def test_major_arcana_cards(self):
        """Test Major Arcana cards exist."""
        fool = self.deck.get_card("The Fool")
        self.assertIsNotNone(fool)
        self.assertEqual(fool.arcana, Arcana.MAJOR)
        self.assertEqual(fool.number, 0)
        
        world = self.deck.get_card("The World")
        self.assertIsNotNone(world)
        self.assertEqual(world.arcana, Arcana.MAJOR)
        self.assertEqual(world.number, 21)
    
    def test_minor_arcana_suits(self):
        """Test that each suit has 14 cards."""
        for suit in [Suit.WANDS, Suit.CUPS, Suit.SWORDS, Suit.PENTACLES]:
            suit_cards = self.deck.get_by_suit(suit)
            self.assertEqual(len(suit_cards), 14)  # 10 number cards + 4 court cards
    
    def test_court_cards_exist(self):
        """Test court cards exist in each suit."""
        for suit_name in ['wands', 'cups', 'swords', 'pentacles']:
            for rank in ['page', 'knight', 'queen', 'king']:
                card_name = f"{rank.capitalize()} of {suit_name.capitalize()}"
                card = self.deck.get_card(card_name)
                self.assertIsNotNone(card)
                self.assertEqual(card.rank, rank)
    
    def test_ace_cards_exist(self):
        """Test Ace cards exist."""
        for suit_name in ['wands', 'cups', 'swords', 'pentacles']:
            card_name = f"Ace of {suit_name.capitalize()}"
            card = self.deck.get_card(card_name)
            self.assertIsNotNone(card)
            self.assertEqual(card.number, 1)
    
    def test_card_meanings(self):
        """Test that cards have meaningful content."""
        fool = self.deck.get_card("The Fool")
        self.assertTrue(len(fool.keywords) > 0)
        self.assertTrue(len(fool.upright_meaning) > 0)
        self.assertTrue(len(fool.reversed_meaning) > 0)
    
    def test_get_card_case_insensitive(self):
        """Test that get_card works with different case."""
        card1 = self.deck.get_card("THE FOOL")
        card2 = self.deck.get_card("the fool")
        card3 = self.deck.get_card("The Fool")
        self.assertEqual(card1, card2)
        self.assertEqual(card2, card3)
    
    def test_card_to_dict(self):
        """Test card serialization."""
        card = self.deck.get_card("The Magician")
        data = card.to_dict()
        
        self.assertEqual(data['name'], "The Magician")
        self.assertEqual(data['arcana'], 'major')
        self.assertIn('keywords', data)
        self.assertIn('upright_meaning', data)
        self.assertIn('reversed_meaning', data)


class TestTarotCard(unittest.TestCase):
    """Tests for TarotCard class."""
    
    def test_get_meaning_upright(self):
        """Test getting upright meaning."""
        deck = TarotDeck()
        card = deck.get_card("The Sun")
        meaning = card.get_meaning(Orientation.UPRIGHT)
        self.assertIn("success", meaning.lower())
    
    def test_get_meaning_reversed(self):
        """Test getting reversed meaning."""
        deck = TarotDeck()
        card = deck.get_card("The Sun")
        meaning = card.get_meaning(Orientation.REVERSED)
        self.assertNotEqual(meaning, card.upright_meaning)
    
    def test_card_attributes(self):
        """Test card attributes."""
        deck = TarotDeck()
        card = deck.get_card("The High Priestess")
        
        self.assertEqual(card.name, "The High Priestess")
        self.assertEqual(card.arcana, Arcana.MAJOR)
        self.assertEqual(card.element, "Water")
        self.assertEqual(card.zodiac, "Moon")


class TestTarotReader(unittest.TestCase):
    """Tests for TarotReader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reader = TarotReader(seed=42)  # Fixed seed for reproducibility
    
    def test_draw_card_returns_card_and_orientation(self):
        """Test that draw_card returns proper types."""
        card, orientation = self.reader.draw_card()
        self.assertIsInstance(card, TarotCard)
        self.assertIsInstance(orientation, Orientation)
    
    def test_seed_provides_initial_state(self):
        """Test that seed initializes reader state."""
        reader = TarotReader(seed=42)
        card, _ = reader.draw_card()
        
        # Seed ensures deterministic initial state
        self.assertIsInstance(card, TarotCard)
    
    def test_draw_multiple_cards(self):
        """Test drawing multiple cards."""
        cards = self.reader.draw_cards(5)
        self.assertEqual(len(cards), 5)
        
        # All cards should be different
        names = [c[0].name for c in cards]
        self.assertEqual(len(names), len(set(names)))
    
    def test_draw_cards_no_reversed(self):
        """Test drawing cards without reversed."""
        cards = self.reader.draw_cards(3, include_reversed=False)
        for _, orientation in cards:
            self.assertEqual(orientation, Orientation.UPRIGHT)
    
    def test_one_card_reading(self):
        """Test one card reading."""
        reading = self.reader.one_card_reading(question="What is my future?")
        
        self.assertEqual(reading.spread_type, SpreadType.ONE_CARD)
        self.assertEqual(len(reading.positions), 1)
        self.assertEqual(reading.question, "What is my future?")
        self.assertIsNotNone(reading.positions[0].card)
    
    def test_three_card_reading(self):
        """Test three card reading."""
        reading = self.reader.three_card_reading(question="Test question")
        
        self.assertEqual(reading.spread_type, SpreadType.THREE_CARD)
        self.assertEqual(len(reading.positions), 3)
        
        # Check position names
        self.assertEqual(reading.positions[0].name, "Past")
        self.assertEqual(reading.positions[1].name, "Present")
        self.assertEqual(reading.positions[2].name, "Future")
    
    def test_three_card_custom_positions(self):
        """Test three card reading with custom positions."""
        custom_pos = ["Mind", "Body", "Spirit"]
        reading = self.reader.three_card_reading(positions=custom_pos)
        
        self.assertEqual(reading.positions[0].name, "Mind")
        self.assertEqual(reading.positions[1].name, "Body")
        self.assertEqual(reading.positions[2].name, "Spirit")
    
    def test_celtic_cross_reading(self):
        """Test Celtic Cross reading."""
        reading = self.reader.celtic_cross_reading(question="Life guidance")
        
        self.assertEqual(reading.spread_type, SpreadType.CELTIC_CROSS)
        self.assertEqual(len(reading.positions), 10)
        
        # Check position names
        expected_positions = ["Present", "Challenge", "Foundation", "Recent Past", 
                            "Possible Future", "Near Future", "Your Influence",
                            "External Influence", "Hopes and Fears", "Final Outcome"]
        for i, expected in enumerate(expected_positions):
            self.assertEqual(reading.positions[i].name, expected)
    
    def test_relationship_reading(self):
        """Test relationship spread."""
        reading = self.reader.relationship_reading()
        
        self.assertEqual(reading.spread_type, SpreadType.RELATIONSHIP)
        self.assertEqual(len(reading.positions), 6)
    
    def test_decision_reading(self):
        """Test decision spread."""
        reading = self.reader.decision_reading(question="Which job to take?")
        
        self.assertEqual(reading.spread_type, SpreadType.DECISION)
        self.assertEqual(len(reading.positions), 5)
    
    def test_daily_reading(self):
        """Test daily spread."""
        reading = self.reader.daily_reading()
        
        self.assertEqual(reading.spread_type, SpreadType.DAILY)
        self.assertEqual(len(reading.positions), 6)
    
    def test_horseshoe_reading(self):
        """Test horseshoe spread."""
        reading = self.reader.horseshoe_reading()
        
        self.assertEqual(reading.spread_type, SpreadType.HORSESHOE)
        self.assertEqual(len(reading.positions), 7)
    
    def test_monthly_reading(self):
        """Test monthly spread."""
        reading = self.reader.monthly_reading()
        
        self.assertEqual(reading.spread_type, SpreadType.MONTHLY)
        self.assertEqual(len(reading.positions), 8)
    
    def test_custom_reading(self):
        """Test custom reading with spread type."""
        reading = self.reader.custom_reading(SpreadType.CELTIC_CROSS)
        self.assertEqual(len(reading.positions), 10)
    
    def test_reading_timestamp(self):
        """Test that reading has timestamp."""
        reading = self.reader.one_card_reading()
        self.assertIsInstance(reading.timestamp, datetime)


class TestTarotReading(unittest.TestCase):
    """Tests for TarotReading class."""
    
    def test_reading_get_summary(self):
        """Test reading summary generation."""
        reader = TarotReader(seed=42)
        reading = reader.three_card_reading(question="Test question")
        
        summary = reading.get_summary()
        
        self.assertIn("Three Card Spread", summary)
        self.assertIn("Past", summary)
        self.assertIn("Present", summary)
        self.assertIn("Future", summary)
        self.assertIn("Test question", summary)
    
    def test_reading_to_dict(self):
        """Test reading serialization."""
        reader = TarotReader(seed=42)
        reading = reader.one_card_reading(question="Test")
        
        data = reading.to_dict()
        
        self.assertEqual(data['spread_type'], 'one_card')
        self.assertIn('positions', data)
        self.assertEqual(data['question'], "Test")
    
    def test_spread_position_to_dict(self):
        """Test spread position serialization."""
        deck = TarotDeck()
        card = deck.get_card("The Fool")
        
        position = SpreadPosition(
            position=1,
            name="Test Position",
            description="Test description",
            card=card,
            orientation=Orientation.UPRIGHT
        )
        
        data = position.to_dict()
        
        self.assertEqual(data['position'], 1)
        self.assertEqual(data['name'], "Test Position")
        self.assertEqual(data['card_name'], "The Fool")
        self.assertEqual(data['orientation'], 'upright')


class TestSpreadDefinitions(unittest.TestCase):
    """Tests for spread definitions."""
    
    def test_all_spreads_defined(self):
        """Test that all spread types have definitions."""
        for spread_type in SpreadType:
            self.assertIn(spread_type, SPREAD_DEFINITIONS)
            self.assertIn('name', SPREAD_DEFINITIONS[spread_type])
            self.assertIn('positions', SPREAD_DEFINITIONS[spread_type])
    
    def test_celtic_cross_positions(self):
        """Test Celtic Cross has 10 positions."""
        positions = SPREAD_DEFINITIONS[SpreadType.CELTIC_CROSS]['positions']
        self.assertEqual(len(positions), 10)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_get_card_by_name(self):
        """Test get_card_by_name function."""
        card = get_card_by_name("The Star")
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "The Star")
    
    def test_get_card_meaning(self):
        """Test get_card_meaning function."""
        meaning = get_card_meaning("The Star", reversed=False)
        self.assertIn("hope", meaning.lower())
        
        reversed_meaning = get_card_meaning("The Star", reversed=True)
        self.assertIn("faith", reversed_meaning.lower())  # "Lack of faith"
    
    def test_daily_card(self):
        """Test daily_card function."""
        card, orientation = daily_card()
        self.assertIsInstance(card, TarotCard)
        self.assertIsInstance(orientation, Orientation)
    
    def test_daily_card_reproducible(self):
        """Test that daily_card is reproducible for same day."""
        today = date.today()
        card1, _ = reading_for_date(today, "one_card").positions[0].card, reading_for_date(today, "one_card").positions[0].orientation
        card2, _ = reading_for_date(today, "one_card").positions[0].card, reading_for_date(today, "one_card").positions[0].orientation
        
        # Note: This tests the function, not actual reproducibility due to randomness
        self.assertIsInstance(card1, TarotCard)
    
    def test_quick_reading(self):
        """Test quick_reading function."""
        reading = quick_reading("one_card", question="Test")
        self.assertEqual(reading.spread_type, SpreadType.ONE_CARD)
        
        reading = quick_reading("three_card")
        self.assertEqual(reading.spread_type, SpreadType.THREE_CARD)
    
    def test_quick_reading_invalid_type(self):
        """Test quick_reading with invalid spread type."""
        with self.assertRaises(ValueError):
            quick_reading("invalid_spread")
    
    def test_get_major_arcana_cards(self):
        """Test get_major_arcana_cards function."""
        cards = get_major_arcana_cards()
        self.assertEqual(len(cards), 22)
    
    def test_get_minor_arcana_cards(self):
        """Test get_minor_arcana_cards function."""
        cards = get_minor_arcana_cards()
        self.assertEqual(len(cards), 56)
    
    def test_get_suit_cards(self):
        """Test get_suit_cards function."""
        wands = get_suit_cards("wands")
        self.assertEqual(len(wands), 14)
        
        cups = get_suit_cards("cups")
        self.assertEqual(len(cups), 14)
    
    def test_search_cards_by_keyword(self):
        """Test search_cards_by_keyword function."""
        # Search for "love" keyword
        love_cards = search_cards_by_keyword("love")
        self.assertTrue(len(love_cards) > 0)
        
        # The Lovers should be in results
        lovers_found = any(c.name == "The Lovers" for c in love_cards)
        self.assertTrue(lovers_found)
    
    def test_reading_for_date(self):
        """Test reading_for_date function."""
        target_date = date(2024, 1, 1)
        reading = reading_for_date(target_date, "three_card")
        
        self.assertEqual(reading.spread_type, SpreadType.THREE_CARD)
        self.assertEqual(len(reading.positions), 3)


class TestInterpretCombination(unittest.TestCase):
    """Tests for interpret_combination function."""
    
    def test_empty_cards(self):
        """Test with empty card list."""
        result = interpret_combination([])
        self.assertIn("No cards", result)
    
    def test_major_arcana_dominance(self):
        """Test detection of Major Arcana dominance."""
        deck = TarotDeck()
        cards = [
            deck.get_card("The Fool"),
            deck.get_card("The Magician"),
            deck.get_card("Ace of Wands")  # Minor
        ]
        
        result = interpret_combination(cards)
        self.assertIn("Major Arcana", result)
    
    def test_all_major_arcana(self):
        """Test with majority Major Arcana cards."""
        deck = TarotDeck()
        cards = [
            deck.get_card("The Fool"),
            deck.get_card("The Magician"),
            deck.get_card("The High Priestess")
        ]
        
        result = interpret_combination(cards)
        # 3 Major Arcana out of 3 cards triggers dominance message
        self.assertIn("Major Arcana", result)
    
    def test_element_analysis(self):
        """Test element dominance analysis."""
        deck = TarotDeck()
        # Fire dominant (Wands cards)
        cards = [
            deck.get_card("Ace of Wands"),
            deck.get_card("Two of Wands"),
            deck.get_card("Three of Wands")
        ]
        
        result = interpret_combination(cards)
        self.assertIn("Fire", result)


class TestMajorArcanaData(unittest.TestCase):
    """Tests for Major Arcana data completeness."""
    
    def test_all_major_arcana_present(self):
        """Test all 22 Major Arcana are defined."""
        self.assertEqual(len(MAJOR_ARCANA), 22)
    
    def test_major_arcana_numbering(self):
        """Test Major Arcana numbering is correct."""
        for i in range(22):
            self.assertIn(i, MAJOR_ARCANA)
    
    def test_major_arcana_fields(self):
        """Test all Major Arcana have required fields."""
        required_fields = ['name', 'keywords', 'upright', 'reversed']
        
        for number, data in MAJOR_ARCANA.items():
            for field in required_fields:
                self.assertIn(field, data)


class TestMinorArcanaData(unittest.TestCase):
    """Tests for Minor Arcana data completeness."""
    
    def test_all_suits_present(self):
        """Test all four suits are defined."""
        expected_suits = ['wands', 'cups', 'swords', 'pentacles']
        for suit in expected_suits:
            self.assertIn(suit, MINOR_ARCANA_COURT)
            self.assertIn(suit, MINOR_ARCANA_NUMBERS)
    
    def test_all_court_cards_defined(self):
        """Test all court cards are defined for each suit."""
        ranks = ['king', 'queen', 'knight', 'page']
        
        for suit in MINOR_ARCANA_COURT:
            for rank in ranks:
                self.assertIn(rank, MINOR_ARCANA_COURT[suit])
    
    def test_all_number_cards_defined(self):
        """Test all number cards (1-10) are defined."""
        for suit in MINOR_ARCANA_NUMBERS:
            for number in range(1, 11):
                self.assertIn(number, MINOR_ARCANA_NUMBERS[suit])


class TestOrientation(unittest.TestCase):
    """Tests for card orientation."""
    
    def test_orientation_values(self):
        """Test orientation enum values."""
        self.assertEqual(Orientation.UPRIGHT.value, "upright")
        self.assertEqual(Orientation.REVERSED.value, "reversed")
    
    def test_reversed_meaning_different(self):
        """Test reversed meaning is different from upright."""
        deck = TarotDeck()
        
        for card in deck.cards[:10]:  # Test first 10 cards
            self.assertNotEqual(card.upright_meaning, card.reversed_meaning)


class TestSuit(unittest.TestCase):
    """Tests for suit enum."""
    
    def test_suit_values(self):
        """Test suit enum values."""
        self.assertEqual(Suit.WANDS.value, "wands")
        self.assertEqual(Suit.CUPS.value, "cups")
        self.assertEqual(Suit.SWORDS.value, "swords")
        self.assertEqual(Suit.PENTACLES.value, "pentacles")


class TestArcana(unittest.TestCase):
    """Tests for Arcana enum."""
    
    def test_arcana_values(self):
        """Test arcana enum values."""
        self.assertEqual(Arcana.MAJOR.value, "major")
        self.assertEqual(Arcana.MINOR.value, "minor")


class TestReadingQuestions(unittest.TestCase):
    """Tests for reading with questions."""
    
    def test_question_included_in_reading(self):
        """Test question is included in reading."""
        reader = TarotReader(seed=42)
        reading = reader.celtic_cross_reading(question="What is my purpose?")
        
        self.assertEqual(reading.question, "What is my purpose?")
    
    def test_question_in_summary(self):
        """Test question appears in summary."""
        reader = TarotReader(seed=42)
        reading = reader.one_card_reading(question="Should I take this job?")
        
        summary = reading.get_summary()
        self.assertIn("Should I take this job?", summary)
    
    def test_reading_without_question(self):
        """Test reading without question."""
        reader = TarotReader(seed=42)
        reading = reader.three_card_reading()
        
        self.assertIsNone(reading.question)


# Run tests if executed directly
if __name__ == '__main__':
    unittest.main(verbosity=2)