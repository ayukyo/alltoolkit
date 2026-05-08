"""
Blackjack Utilities Test Suite
===============================

Comprehensive tests for blackjack_utils module.

Run with: python blackjack_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blackjack_utils.mod import (
    # Enums
    Suit, Rank, HandType, Action, CountSystem,
    # Classes
    Card, Deck, Hand, BasicStrategy, CardCounter, 
    ProbabilityCalculator, GameSimulator, GameResult, SimulationStats,
    # Functions
    create_deck, create_hand, card, hand_value, is_blackjack,
    get_basic_strategy_action, simulate_games, calculate_true_count
)


class TestCard(unittest.TestCase):
    """Tests for Card class."""
    
    def test_card_creation(self):
        """Test card creation."""
        c = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(str(c), 'A♠')
        self.assertEqual(c.primary_value, 11)
        self.assertEqual(c.values, [1, 11])
    
    def test_card_values(self):
        """Test card value properties."""
        # Ace
        ace = Card(Rank.ACE, Suit.HEARTS)
        self.assertEqual(ace.values, [1, 11])
        
        # Ten-value cards
        for rank in [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING]:
            c = Card(rank, Suit.CLUBS)
            self.assertEqual(c.primary_value, 10)
            self.assertEqual(c.values, [10])
        
        # Number cards
        for i, rank in enumerate([Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE,
                                   Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE], start=2):
            c = Card(rank, Suit.DIAMONDS)
            self.assertEqual(c.primary_value, i)
            self.assertEqual(c.values, [i])
    
    def test_card_suits(self):
        """Test suit properties."""
        self.assertEqual(Suit.HEARTS.symbol, '♥')
        self.assertEqual(Suit.HEARTS.color, 'red')
        self.assertEqual(Suit.SPADES.symbol, '♠')
        self.assertEqual(Suit.SPADES.color, 'black')
    
    def test_card_to_dict(self):
        """Test card serialization."""
        c = Card(Rank.ACE, Suit.SPADES)
        d = c.to_dict()
        self.assertEqual(d['rank'], 'ACE')
        self.assertEqual(d['suit'], 'SPADES')
        self.assertEqual(d['symbol'], 'A♠')
    
    def test_card_frozen(self):
        """Test that cards are immutable."""
        c = Card(Rank.ACE, Suit.SPADES)
        # Should not be able to modify
        with self.assertRaises(AttributeError):
            c.rank = Rank.TWO
    
    def test_card_convenience_function(self):
        """Test card() convenience function."""
        c = card('A', 'spades')
        self.assertEqual(c.rank, Rank.ACE)
        self.assertEqual(c.suit, Suit.SPADES)
        
        c2 = card('10', 'hearts')
        self.assertEqual(c2.rank, Rank.TEN)
        self.assertEqual(c2.suit, Suit.HEARTS)
        
        # Alternative notation
        c3 = card('K', 's')
        self.assertEqual(c3.suit, Suit.SPADES)
        
        # Invalid rank
        with self.assertRaises(ValueError):
            card('X', 'hearts')
        
        # Invalid suit
        with self.assertRaises(ValueError):
            card('A', 'x')


class TestDeck(unittest.TestCase):
    """Tests for Deck class."""
    
    def test_deck_creation_single(self):
        """Test single deck creation."""
        deck = Deck(num_decks=1)
        self.assertEqual(deck.remaining, 52)
        self.assertEqual(deck.num_decks, 1)
    
    def test_deck_creation_multi(self):
        """Test multi-deck creation."""
        deck = Deck(num_decks=6)
        self.assertEqual(deck.remaining, 312)  # 6 * 52
    
    def test_deck_invalid_decks(self):
        """Test invalid deck counts."""
        with self.assertRaises(ValueError):
            Deck(num_decks=0)
        with self.assertRaises(ValueError):
            Deck(num_decks=9)
    
    def test_deck_deal(self):
        """Test dealing cards."""
        deck = Deck(num_decks=1)
        cards = deck.deal(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(deck.remaining, 50)
        self.assertEqual(deck.dealt_count, 2)
    
    def test_deck_deal_one(self):
        """Test dealing single card."""
        deck = Deck(num_decks=1)
        card = deck.deal_one()
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.remaining, 51)
    
    def test_deck_deal_too_many(self):
        """Test dealing more cards than available."""
        deck = Deck(num_decks=1)
        with self.assertRaises(ValueError):
            deck.deal(53)
    
    def test_deck_shuffle(self):
        """Test shuffle functionality."""
        deck = Deck(num_decks=1)
        deck.deal(10)
        deck.shuffle()
        self.assertEqual(deck.remaining, 52)
        self.assertEqual(deck.dealt_count, 0)
    
    def test_deck_penetration(self):
        """Test deck penetration tracking."""
        deck = Deck(num_decks=1)
        deck.deal(26)
        self.assertEqual(deck.penetration, 0.5)
    
    def test_deck_needs_reshuffle(self):
        """Test reshuffle detection."""
        deck = Deck(num_decks=1)
        deck.deal(40)  # 40 dealt, 12 remaining
        self.assertTrue(deck.needs_reshuffle)
    
    def test_deck_reset(self):
        """Test deck reset."""
        deck = Deck(num_decks=1)
        deck.deal(20)
        deck.reset()
        self.assertEqual(deck.remaining, 52)
    
    def test_deck_all_cards_dealt(self):
        """Test dealing all cards."""
        deck = Deck(num_decks=1)
        cards = deck.deal(52)
        self.assertEqual(len(cards), 52)
        self.assertEqual(deck.remaining, 0)


class TestHand(unittest.TestCase):
    """Tests for Hand class."""
    
    def test_hand_creation(self):
        """Test hand creation."""
        hand = Hand()
        self.assertEqual(len(hand.cards), 0)
        self.assertEqual(hand.best_value, 0)
    
    def test_hand_add_card(self):
        """Test adding cards to hand."""
        hand = Hand()
        hand.add_card(card('A', 'spades'))
        hand.add_card(card('K', 'hearts'))
        self.assertEqual(len(hand.cards), 2)
    
    def test_hand_hard_total(self):
        """Test hard hand values."""
        hand = Hand()
        hand.add_card(card('9', 'hearts'))
        hand.add_card(card('8', 'clubs'))
        self.assertEqual(hand.best_value, 17)
        self.assertEqual(hand.hand_type, HandType.HARD)
        self.assertFalse(hand.is_soft)
    
    def test_hand_soft_total(self):
        """Test soft hand values."""
        hand = Hand()
        hand.add_card(card('A', 'spades'))
        hand.add_card(card('6', 'hearts'))
        self.assertEqual(hand.best_value, 17)
        self.assertEqual(hand.hand_type, HandType.SOFT)
        self.assertTrue(hand.is_soft)
        self.assertEqual(hand.values, [17, 7])
    
    def test_hand_blackjack(self):
        """Test natural blackjack."""
        hand = Hand()
        hand.add_card(card('A', 'spades'))
        hand.add_card(card('K', 'hearts'))
        self.assertEqual(hand.best_value, 21)
        self.assertEqual(hand.hand_type, HandType.BLACKJACK)
        self.assertTrue(hand.is_blackjack)
    
    def test_hand_bust(self):
        """Test bust hand."""
        hand = Hand()
        hand.add_card(card('K', 'spades'))
        hand.add_card(card('K', 'hearts'))
        hand.add_card(card('5', 'clubs'))
        self.assertEqual(hand.best_value, 25)
        self.assertEqual(hand.hand_type, HandType.BUST)
        self.assertTrue(hand.is_bust)
    
    def test_hand_two_aces(self):
        """Test hand with multiple aces."""
        hand = Hand()
        hand.add_card(card('A', 'spades'))
        hand.add_card(card('A', 'hearts'))
        self.assertEqual(hand.best_value, 12)  # One as 11, one as 1
        self.assertEqual(hand.values, [12, 2])
    
    def test_hand_pair_detection(self):
        """Test pair detection."""
        hand = Hand()
        hand.add_card(card('8', 'spades'))
        hand.add_card(card('8', 'hearts'))
        self.assertTrue(hand.is_pair)
        self.assertEqual(hand.pair_rank, Rank.EIGHT)
        self.assertTrue(hand.can_split)
    
    def test_hand_not_pair(self):
        """Test non-pair hand."""
        hand = Hand()
        hand.add_card(card('8', 'spades'))
        hand.add_card(card('9', 'hearts'))
        self.assertFalse(hand.is_pair)
        self.assertFalse(hand.can_split)
    
    def test_hand_pair_after_hit(self):
        """Test pair after adding more cards."""
        hand = Hand()
        hand.add_card(card('8', 'spades'))
        hand.add_card(card('8', 'hearts'))
        hand.add_card(card('2', 'clubs'))
        self.assertFalse(hand.is_pair)  # 3 cards, not a pair
        self.assertFalse(hand.can_split)
    
    def test_hand_can_double(self):
        """Test double down eligibility."""
        hand = Hand()
        hand.add_card(card('10', 'spades'))
        hand.add_card(card('6', 'hearts'))
        self.assertTrue(hand.can_double)
        
        hand.is_doubled = True
        self.assertFalse(hand.can_double)
    
    def test_hand_values_calculation(self):
        """Test various hand value calculations."""
        # Simple values
        hand = Hand()
        hand.add_card(card('2', 's'))
        hand.add_card(card('3', 'h'))
        self.assertEqual(hand.values, [5])
        
        # Ace soft
        hand = Hand()
        hand.add_card(card('A', 's'))
        hand.add_card(card('9', 'h'))
        self.assertEqual(hand.values, [20, 10])
        
        # Ace becomes hard
        hand = Hand()
        hand.add_card(card('A', 's'))
        hand.add_card(card('9', 'h'))
        hand.add_card(card('5', 'c'))
        self.assertEqual(hand.best_value, 15)  # 9+5+1(A)
    
    def test_hand_to_dict(self):
        """Test hand serialization."""
        hand = Hand()
        hand.add_card(card('A', 'spades'))
        hand.add_card(card('K', 'hearts'))
        d = hand.to_dict()
        self.assertEqual(d['best_value'], 21)
        self.assertEqual(d['hand_type'], 'blackjack')
        self.assertTrue(d['is_blackjack'])


class TestBasicStrategy(unittest.TestCase):
    """Tests for BasicStrategy class."""
    
    def test_hard_hand_strategy(self):
        """Test hard hand strategy recommendations."""
        # Hard 10 vs 6 - should double
        hand = Hand()
        hand.add_card(card('6', 's'))
        hand.add_card(card('4', 'h'))
        upcard = card('6', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.DOUBLE)
        
        # Hard 16 vs 10 - should hit
        hand = Hand()
        hand.add_card(card('10', 's'))
        hand.add_card(card('6', 'h'))
        upcard = card('K', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.HIT)
        
        # Hard 17 vs 10 - should stand
        hand = Hand()
        hand.add_card(card('10', 's'))
        hand.add_card(card('7', 'h'))
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.STAND)
    
    def test_soft_hand_strategy(self):
        """Test soft hand strategy recommendations."""
        # Soft 18 (A,7) vs 6 - should double
        hand = Hand()
        hand.add_card(card('A', 's'))
        hand.add_card(card('7', 'h'))
        upcard = card('6', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.DOUBLE)
        
        # Soft 18 (A,7) vs 10 - should hit
        upcard = card('K', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.HIT)
    
    def test_pair_splitting_strategy(self):
        """Test pair splitting recommendations."""
        # Pair of 8s - always split
        hand = Hand()
        hand.add_card(card('8', 's'))
        hand.add_card(card('8', 'h'))
        upcard = card('K', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.SPLIT)
        
        # Pair of Aces - always split
        hand = Hand()
        hand.add_card(card('A', 's'))
        hand.add_card(card('A', 'h'))
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.SPLIT)
        
        # Pair of 10s - never split
        hand = Hand()
        hand.add_card(card('K', 's'))
        hand.add_card(card('Q', 'h'))
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.STAND)
    
    def test_blackjack_stand(self):
        """Test that blackjack always stands."""
        hand = Hand()
        hand.add_card(card('A', 's'))
        hand.add_card(card('K', 'h'))
        upcard = card('6', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.STAND)
    
    def test_bust_stand(self):
        """Test that bust hand stands."""
        hand = Hand()
        hand.add_card(card('K', 's'))
        hand.add_card(card('K', 'h'))
        hand.add_card(card('5', 'c'))
        upcard = card('6', 'c')
        action = BasicStrategy.get_action(hand, upcard)
        self.assertEqual(action, Action.STAND)
    
    def test_strategy_with_options_disabled(self):
        """Test strategy when options are disabled."""
        hand = Hand()
        hand.add_card(card('6', 's'))
        hand.add_card(card('4', 'h'))
        upcard = card('6', 'c')
        
        # Cannot double - should hit instead
        action = BasicStrategy.get_action(hand, upcard, can_double=False)
        self.assertEqual(action, Action.HIT)
    
    def test_strategy_chart_generation(self):
        """Test strategy chart generation."""
        hard_chart = BasicStrategy.get_strategy_chart('hard')
        self.assertIn('Hard Hand Strategy', hard_chart)
        self.assertIn('H', hard_chart)
        self.assertIn('S', hard_chart)
        
        soft_chart = BasicStrategy.get_strategy_chart('soft')
        self.assertIn('Soft Hand Strategy', soft_chart)
        
        split_chart = BasicStrategy.get_strategy_chart('split')
        self.assertIn('Pair Splitting', split_chart)


class TestCardCounter(unittest.TestCase):
    """Tests for CardCounter class."""
    
    def test_hi_lo_count(self):
        """Test Hi-Lo counting system."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Add low cards (increase count)
        counter.add_card(card('2', 's'))
        counter.add_card(card('3', 'h'))
        counter.add_card(card('5', 'c'))
        self.assertEqual(counter.running_count, 3)
        
        # Add high cards (decrease count)
        counter.add_card(card('K', 's'))
        counter.add_card(card('10', 'h'))
        self.assertEqual(counter.running_count, 1)
        
        # Add neutral cards
        counter.add_card(card('7', 's'))
        counter.add_card(card('8', 'h'))
        self.assertEqual(counter.running_count, 1)
    
    def test_ko_count(self):
        """Test KO counting system."""
        counter = CardCounter(CountSystem.KO, num_decks=6)
        
        # KO counts 7 as +1
        counter.add_card(card('7', 's'))
        self.assertEqual(counter.running_count, 1)
        
        # Hi-Lo counts 7 as 0
        hi_lo_counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        hi_lo_counter.add_card(card('7', 's'))
        self.assertEqual(hi_lo_counter.running_count, 0)
    
    def test_true_count_calculation(self):
        """Test true count calculation."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Add 156 cards (3 decks worth) to leave 3 decks
        for _ in range(156):
            counter.add_card(card('2', 's'))  # Each +1
        
        # Running count = 156, decks remaining ≈ 3
        # True count ≈ 156 / 3 = 52
        self.assertEqual(counter.running_count, 156)
        tc = counter.true_count
        self.assertGreater(tc, 50)
    
    def test_bet_size_calculation(self):
        """Test bet size recommendations."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Negative count - bet minimum
        counter.add_card(card('K', 's'))
        counter.add_card(card('K', 'h'))
        counter.add_card(card('K', 'c'))
        bet = counter.get_bet_size(base_bet=25, min_bet=10)
        self.assertEqual(bet, 10)
        
        # Positive count - bet more
        counter.reset()
        counter.add_card(card('2', 's'))
        counter.add_card(card('2', 'h'))
        counter.add_card(card('3', 'c'))
        # Need to add more cards to get positive true count
        for _ in range(100):
            counter.add_card(card('5', 's'))
        
        bet = counter.get_bet_size(base_bet=25, min_bet=10)
        self.assertGreater(bet, 25)
    
    def test_player_advantage(self):
        """Test advantage calculation."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Starting advantage (negative)
        adv = counter.get_advantage()
        self.assertEqual(adv, -0.5)  # House edge
        
        # Add cards for positive count
        counter.add_cards([card('2', 's'), card('3', 'h'), card('4', 'c')])
        for _ in range(100):
            counter.add_card(card('5', 's'))
        
        adv = counter.get_advantage()
        self.assertGreater(adv, 0)  # Player advantage
    
    def test_reset(self):
        """Test counter reset."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        counter.add_card(card('2', 's'))
        counter.add_card(card('K', 'h'))
        self.assertEqual(counter.running_count, 0)
        self.assertEqual(counter.cards_seen, 2)
        
        counter.reset()
        self.assertEqual(counter.running_count, 0)
        self.assertEqual(counter.cards_seen, 0)
    
    def test_count_values_table(self):
        """Test count values for all systems."""
        # Hi-Lo
        hi_lo = CardCounter.COUNT_VALUES[CountSystem.HI_LO]
        self.assertEqual(hi_lo[Rank.TWO], 1)
        self.assertEqual(hi_lo[Rank.ACE], -1)
        self.assertEqual(hi_lo[Rank.SEVEN], 0)
        
        # Hi-Opt I (ace is 0)
        hi_opt_i = CardCounter.COUNT_VALUES[CountSystem.HI_OPT_I]
        self.assertEqual(hi_opt_i[Rank.ACE], 0)
        self.assertEqual(hi_opt_i[Rank.TWO], 0)
        
        # Hi-Opt II (two-level count)
        hi_opt_ii = CardCounter.COUNT_VALUES[CountSystem.HI_OPT_II]
        self.assertEqual(hi_opt_ii[Rank.FIVE], 2)
        self.assertEqual(hi_opt_ii[Rank.TEN], -2)
    
    def test_insurance_decision(self):
        """Test insurance recommendation."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Low count - don't take insurance
        self.assertFalse(counter.insurance_is_good())
        
        # High positive count - take insurance
        for _ in range(200):
            counter.add_card(card('2', 's'))
        
        self.assertTrue(counter.insurance_is_good())
    
    def test_deviations(self):
        """Test strategy deviations."""
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # No deviations at zero count
        deviations = counter.get_deviations()
        active = [d for d in deviations if d['active']]
        self.assertEqual(len(active), 0)
        
        # High count - some deviations active
        for _ in range(200):
            counter.add_card(card('2', 's'))
        
        deviations = counter.get_deviations()
        active = [d for d in deviations if d['active']]
        self.assertGreater(len(active), 0)


class TestProbabilityCalculator(unittest.TestCase):
    """Tests for ProbabilityCalculator class."""
    
    def test_bust_probability(self):
        """Test bust probability calculation."""
        from collections import Counter
        
        # Hand value 11 - cannot bust (max hit card is 10, gives 21)
        cards = Counter({r: 4 for r in Rank})
        prob = ProbabilityCalculator.bust_probability(11, cards, 52)
        self.assertEqual(prob, 0.0)
        
        # Hand value 12 - can bust with 10-value cards
        # 16 ten-value cards out of 52 = 16/52 ≈ 0.308
        prob = ProbabilityCalculator.bust_probability(12, cards, 52)
        self.assertAlmostEqual(prob, 16/52, places=2)
        
        # Hand value 21 - max bust
        prob = ProbabilityCalculator.bust_probability(21, cards, 52)
        self.assertEqual(prob, 1.0)
    
    def test_dealer_outcome_probability(self):
        """Test dealer outcome probabilities."""
        # Weak dealer upcard (5)
        probs = ProbabilityCalculator.dealer_outcome_probability(
            card('5', 's'), {}
        )
        self.assertIn('bust', probs)
        self.assertGreater(probs['bust'], 0.35)  # High bust rate
        
        # Strong dealer upcard (10)
        probs = ProbabilityCalculator.dealer_outcome_probability(
            card('10', 's'), {}
        )
        self.assertIn(20, probs)
        self.assertGreater(probs[20], 0.3)  # Likely to make 20
    
    def test_blackjack_probability(self):
        """Test blackjack probability calculation."""
        # Standard 6-deck
        prob = ProbabilityCalculator.blackjack_probability(num_decks=6)
        self.assertGreater(prob, 0.04)  # ~4.75%
        self.assertLess(prob, 0.05)
        
        # Single deck
        prob = ProbabilityCalculator.blackjack_probability(num_decks=1)
        self.assertGreater(prob, 0.047)
        
        # After cards dealt (fewer aces available)
        prob = ProbabilityCalculator.blackjack_probability(
            num_decks=6, 
            cards_seen=[card('A', 's'), card('A', 'h')]
        )
        self.assertLess(prob, 0.0475)  # Reduced from standard 6-deck probability


class TestGameSimulator(unittest.TestCase):
    """Tests for GameSimulator class."""
    
    def test_simulator_creation(self):
        """Test simulator creation."""
        sim = GameSimulator(num_decks=6)
        self.assertEqual(sim.num_decks, 6)
        self.assertEqual(sim.blackjack_pays, 1.5)  # 3:2
    
    def test_deal_initial_cards(self):
        """Test initial card dealing."""
        sim = GameSimulator(num_decks=1)
        player_hand, dealer_hand, upcard = sim.deal_initial_cards()
        
        self.assertEqual(len(player_hand.cards), 2)
        self.assertEqual(len(dealer_hand.cards), 2)
        self.assertEqual(upcard, dealer_hand.cards[0])
    
    def test_dealer_play(self):
        """Test dealer play rules."""
        sim = GameSimulator(num_decks=1, dealer_hits_soft_17=True)
        
        # Dealer 16 - must hit
        hand = Hand()
        hand.add_card(card('10', 's'))
        hand.add_card(card('6', 'h'))
        final_hand = sim.dealer_play(hand)
        self.assertGreater(len(final_hand.cards), 2)
        
        # Dealer 17 hard - stand
        hand = Hand()
        hand.add_card(card('10', 's'))
        hand.add_card(card('7', 'h'))
        final_hand = sim.dealer_play(hand)
        self.assertEqual(len(final_hand.cards), 2)
    
    def test_play_round(self):
        """Test single round play."""
        sim = GameSimulator(num_decks=1)
        result = sim.play_round(bet=10)
        
        self.assertIn(result.outcome, ['win', 'lose', 'push', 'blackjack'])
        self.assertIsInstance(result.player_value, int)
        self.assertIsInstance(result.dealer_value, int)
    
    def test_simulate_rounds(self):
        """Test multi-round simulation."""
        sim = GameSimulator(num_decks=6)
        stats = sim.simulate(num_rounds=100, bet=10)
        
        self.assertEqual(stats.total_games, 100)
        self.assertGreater(stats.wins, 0)
        self.assertGreater(stats.losses, 0)
        self.assertIn(stats.pushes, range(100))
        self.assertGreater(stats.blackjacks, 0)
    
    def test_simulation_stats(self):
        """Test simulation statistics."""
        stats = SimulationStats()
        stats.total_games = 100
        stats.wins = 44
        stats.losses = 48
        stats.pushes = 8
        
        self.assertEqual(stats.win_rate, 0.44)
        self.assertEqual(stats.win_rate + stats.pushes/100 + stats.losses/100, 1.0)
    
    def test_simulator_deck_management(self):
        """Test deck reshuffling in simulator."""
        sim = GameSimulator(num_decks=1)
        
        # Play many rounds
        for _ in range(20):
            sim.play_round()
        
        # Deck should be reshuffled and have close to 52 cards
        self.assertGreater(sim.deck.remaining, 10)  # At least some cards after reshuffle


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_create_deck(self):
        """Test create_deck function."""
        deck = create_deck(num_decks=2)
        self.assertEqual(deck.remaining, 104)
    
    def test_create_hand(self):
        """Test create_hand function."""
        hand = create_hand()
        self.assertEqual(len(hand.cards), 0)
        
        hand = create_hand([card('A', 's'), card('K', 'h')])
        self.assertEqual(len(hand.cards), 2)
    
    def test_hand_value_function(self):
        """Test hand_value function."""
        cards = [card('9', 's'), card('8', 'h')]
        self.assertEqual(hand_value(cards), 17)
        
        cards = [card('A', 's'), card('K', 'h')]
        self.assertEqual(hand_value(cards), 21)
    
    def test_is_blackjack_function(self):
        """Test is_blackjack function."""
        cards = [card('A', 's'), card('K', 'h')]
        self.assertTrue(is_blackjack(cards))
        
        cards = [card('10', 's'), card('10', 'h')]
        self.assertFalse(is_blackjack(cards))  # 20, not blackjack
    
    def test_get_basic_strategy_function(self):
        """Test get_basic_strategy_action function."""
        # Hard 10 (6+4) vs 6 - should double
        cards = [card('6', 's'), card('4', 'h')]
        upcard = card('6', 'c')
        action = get_basic_strategy_action(cards, upcard)
        self.assertEqual(action, Action.DOUBLE)
    
    def test_simulate_games_function(self):
        """Test simulate_games function."""
        stats = simulate_games(num_rounds=50, num_decks=1, bet=5)
        self.assertEqual(stats.total_games, 50)
    
    def test_calculate_true_count_function(self):
        """Test calculate_true_count function."""
        tc = calculate_true_count(running_count=12, cards_seen=156, total_decks=6)
        # 6 decks * 52 = 312 cards, 156 seen, 156 remaining = 3 decks
        # True count = 12 / 3 = 4
        self.assertAlmostEqual(tc, 4.0, places=1)


class TestGameResult(unittest.TestCase):
    """Tests for GameResult class."""
    
    def test_game_result_creation(self):
        """Test game result creation."""
        result = GameResult(
            player_value=20, dealer_value=18,
            player_blackjack=False, dealer_blackjack=False,
            player_bust=False, dealer_bust=False,
            outcome='win', payout=10.0
        )
        
        self.assertEqual(result.player_value, 20)
        self.assertEqual(result.outcome, 'win')
    
    def test_game_result_to_dict(self):
        """Test game result serialization."""
        result = GameResult(
            player_value=21, dealer_value=21,
            player_blackjack=True, dealer_blackjack=False,
            player_bust=False, dealer_bust=False,
            outcome='blackjack', payout=15.0
        )
        
        d = result.to_dict()
        self.assertEqual(d['outcome'], 'blackjack')
        self.assertEqual(d['payout'], 15.0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios."""
    
    def test_complete_game_scenario(self):
        """Test a complete game scenario."""
        deck = create_deck(num_decks=1)
        
        # Deal cards
        player_hand = create_hand(deck.deal(2))
        dealer_cards = deck.deal(2)
        dealer_hand = create_hand(dealer_cards)
        dealer_upcard = dealer_cards[0]
        
        # Get strategy
        action = get_basic_strategy_action(player_hand.cards, dealer_upcard)
        
        # Execute strategy
        if action == Action.HIT:
            player_hand.add_card(deck.deal_one())
        elif action == Action.STAND:
            pass  # No action needed
        
        # Verify hand is valid
        self.assertIsInstance(player_hand.best_value, int)
        self.assertIn(player_hand.hand_type, [HandType.HARD, HandType.SOFT, 
                                               HandType.BLACKJACK, HandType.BUST])
    
    def test_card_counting_game_simulation(self):
        """Test card counting with simulation."""
        simulator = GameSimulator(num_decks=6)
        counter = CardCounter(CountSystem.HI_LO, num_decks=6)
        
        # Play rounds and track count
        for _ in range(10):
            result = simulator.play_round()
            # Would normally add cards to counter during play
        
        # Verify counter structure
        self.assertEqual(counter.running_count, 0)
        self.assertEqual(counter.cards_seen, 0)
    
    def test_strategy_consistency(self):
        """Test that basic strategy is consistent."""
        # Same situation should give same recommendation
        hand = Hand()
        hand.add_card(card('10', 's'))
        hand.add_card(card('6', 'h'))
        upcard = card('10', 'c')
        
        action1 = BasicStrategy.get_action(hand, upcard)
        action2 = BasicStrategy.get_action(hand, upcard)
        
        self.assertEqual(action1, action2)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCard))
    suite.addTests(loader.loadTestsFromTestCase(TestDeck))
    suite.addTests(loader.loadTestsFromTestCase(TestHand))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestCardCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestProbabilityCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestGameSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestGameResult))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()