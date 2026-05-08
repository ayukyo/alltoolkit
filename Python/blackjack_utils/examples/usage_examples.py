"""
Blackjack Utilities - Usage Examples
=====================================

Comprehensive examples demonstrating all features of the blackjack_utils module.

Author: AllToolkit
Date: 2026-05-08
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from blackjack_utils.mod import (
    # Enums
    Suit, Rank, HandType, Action, CountSystem,
    # Classes
    Card, Deck, Hand, BasicStrategy, CardCounter,
    ProbabilityCalculator, GameSimulator,
    # Functions
    card, create_deck, create_hand, hand_value, is_blackjack,
    get_basic_strategy_action, simulate_games, calculate_true_count
)


def example_basic_cards():
    """Example: Basic card and deck operations."""
    print("=" * 60)
    print("Example 1: Basic Card and Deck Operations")
    print("=" * 60)
    
    # Create cards using convenience function
    ace = card('A', 'spades')
    king = card('K', 'hearts')
    ten = card('10', 'clubs')
    
    print(f"\nCreated cards:")
    print(f"  {ace} - values: {ace.values}, primary: {ace.primary_value}")
    print(f"  {king} - value: {king.primary_value}")
    print(f"  {ten} - value: {ten.primary_value}")
    
    # Create a deck
    deck = create_deck(num_decks=1)
    print(f"\nSingle deck created: {deck.remaining} cards")
    
    # Deal some cards
    dealt_cards = deck.deal(5)
    print(f"Dealt 5 cards: {[str(c) for c in dealt_cards]}")
    print(f"Remaining: {deck.remaining}, Dealt: {deck.dealt_count}")
    print(f"Penetration: {deck.penetration:.1%}")
    
    # Shuffle and reset
    deck.shuffle()
    print(f"\nAfter shuffle: {deck.remaining} cards")


def example_hand_evaluation():
    """Example: Hand creation and evaluation."""
    print("\n" + "=" * 60)
    print("Example 2: Hand Evaluation")
    print("=" * 60)
    
    # Create various hands
    hands = [
        # Blackjack
        create_hand([card('A', 'spades'), card('K', 'hearts')]),
        # Soft 17
        create_hand([card('A', 'spades'), card('6', 'hearts')]),
        # Hard 17
        create_hand([card('10', 'spades'), card('7', 'hearts')]),
        # Bust
        create_hand([card('K', 'spades'), card('K', 'hearts'), card('5', 'clubs')]),
        # Pair of 8s
        create_hand([card('8', 'spades'), card('8', 'hearts')]),
        # Two aces
        create_hand([card('A', 'spades'), card('A', 'hearts')]),
    ]
    
    print("\nHand evaluations:")
    for hand in hands:
        print(f"  {hand}")
        print(f"    Type: {hand.hand_type.value}")
        print(f"    Values: {hand.values}")
        print(f"    Best value: {hand.best_value}")
        print(f"    Is soft: {hand.is_soft}")
        print(f"    Is pair: {hand.is_pair}")
        print()


def example_basic_strategy():
    """Example: Basic strategy recommendations."""
    print("=" * 60)
    print("Example 3: Basic Strategy Recommendations")
    print("=" * 60)
    
    # Various scenarios
    scenarios = [
        # (player_hand_description, player_cards, dealer_upcard)
        ("Hard 12 vs 4", [card('10', 's'), card('2', 'h')], card('4', 'c')),
        ("Hard 10 vs 6", [card('6', 's'), card('4', 'h')], card('6', 'c')),
        ("Hard 16 vs 10", [card('10', 's'), card('6', 'h')], card('K', 'c')),
        ("Soft 17 vs 3", [card('A', 's'), card('6', 'h')], card('3', 'c')),
        ("Soft 18 vs 10", [card('A', 's'), card('7', 'h')], card('10', 'c')),
        ("Pair of 8s vs 10", [card('8', 's'), card('8', 'h')], card('10', 'c')),
        ("Pair of Aces vs 6", [card('A', 's'), card('A', 'h')], card('6', 'c')),
        ("Pair of 10s vs 6", [card('10', 's'), card('10', 'h')], card('6', 'c')),
        ("Blackjack", [card('A', 's'), card('K', 'h')], card('6', 'c')),
    ]
    
    print("\nBasic strategy recommendations:")
    for desc, player_cards, upcard in scenarios:
        hand = create_hand(player_cards)
        action = BasicStrategy.get_action(hand, upcard)
        print(f"  {desc}:")
        print(f"    Hand: {hand}, Upcard: {upcard}")
        print(f"    Recommended: {action.value}")
        print()


def example_strategy_charts():
    """Example: Display strategy charts."""
    print("=" * 60)
    print("Example 4: Strategy Charts")
    print("=" * 60)
    
    print(BasicStrategy.get_strategy_chart('hard'))
    print(BasicStrategy.get_strategy_chart('soft'))
    print(BasicStrategy.get_strategy_chart('split'))


def example_card_counting():
    """Example: Card counting systems."""
    print("=" * 60)
    print("Example 5: Card Counting")
    print("=" * 60)
    
    # Initialize counter
    counter = CardCounter(CountSystem.HI_LO, num_decks=6)
    
    print("\nHi-Lo Card Counting Demo:")
    print("Card values: 2-6 = +1, 7-9 = 0, 10-A = -1")
    
    # Simulate seeing cards
    cards_seen = [
        card('2', 'hearts'), card('3', 'diamonds'), card('5', 'clubs'),
        card('7', 'spades'), card('10', 'hearts'), card('K', 'diamonds'),
        card('A', 'clubs'), card('4', 'hearts'), card('9', 'spades'),
        card('2', 'diamonds'), card('6', 'clubs'), card('J', 'hearts'),
    ]
    
    print("\nCards seen and count progression:")
    for i, c in enumerate(cards_seen, 1):
        counter.add_card(c)
        value = CardCounter.COUNT_VALUES[CountSystem.HI_LO].get(c.rank, 0)
        print(f"  {i}. {c} (+{value}): Running = {counter.running_count}")
    
    print(f"\nSummary:")
    print(f"  Running count: {counter.running_count}")
    print(f"  Cards seen: {counter.cards_seen}")
    print(f"  Decks remaining: {counter.decks_remaining:.2f}")
    print(f"  True count: {counter.true_count:.2f}")
    print(f"  Player advantage: {counter.get_advantage():.2f}%")
    
    # Betting recommendation
    bet = counter.get_bet_size(base_bet=25, min_bet=10, max_bet=100)
    print(f"  Recommended bet: ${bet}")
    
    # Insurance decision
    print(f"  Take insurance: {counter.insurance_is_good()}")


def example_different_count_systems():
    """Example: Different card counting systems."""
    print("\n" + "=" * 60)
    print("Example 6: Different Counting Systems")
    print("=" * 60)
    
    systems = [
        (CountSystem.HI_LO, "Hi-Lo"),
        (CountSystem.KO, "KO"),
        (CountSystem.HI_OPT_I, "Hi-Opt I"),
        (CountSystem.HI_OPT_II, "Hi-Opt II"),
    ]
    
    test_cards = [
        card('2', 's'), card('3', 'h'), card('5', 'c'), 
        card('7', 's'), card('10', 'h'), card('K', 'c')
    ]
    
    print("\nComparing systems on same cards:")
    for system, name in systems:
        counter = CardCounter(system, num_decks=6)
        for c in test_cards:
            counter.add_card(c)
        
        print(f"  {name}:")
        print(f"    Running count: {counter.running_count}")
        print(f"    True count: {counter.true_count:.2f}")


def example_probability_calculations():
    """Example: Probability calculations."""
    print("\n" + "=" * 60)
    print("Example 7: Probability Calculations")
    print("=" * 60)
    
    # Blackjack probability
    print("\nNatural Blackjack Probability:")
    for decks in [1, 2, 6, 8]:
        prob = ProbabilityCalculator.blackjack_probability(num_decks=decks)
        print(f"  {decks}-deck shoe: {prob:.3%}")
    
    # Dealer outcome probabilities
    print("\nDealer Outcome Probabilities (by upcard):")
    for upcard_rank in ['2', '5', '6', '7', '9', '10', 'A']:
        upcard = card(upcard_rank, 'spades')
        probs = ProbabilityCalculator.dealer_outcome_probability(upcard, {})
        
        print(f"  Dealer {upcard_rank}:")
        bust_prob = probs.get('bust', 0)
        print(f"    Bust: {bust_prob:.1%}")
        for val in [17, 18, 19, 20, 21]:
            if val in probs:
                print(f"    {val}: {probs[val]:.1%}")


def example_game_simulation():
    """Example: Game simulation."""
    print("\n" + "=" * 60)
    print("Example 8: Game Simulation")
    print("=" * 60)
    
    # Simulate 1000 rounds
    simulator = GameSimulator(num_decks=6, blackjack_pays=1.5)
    
    print("\nSimulating 1000 rounds of blackjack...")
    stats = simulator.simulate(num_rounds=1000, bet=10)
    
    print(f"\nResults:")
    print(f"  Total games: {stats.total_games}")
    print(f"  Wins: {stats.wins}")
    print(f"  Losses: {stats.losses}")
    print(f"  Pushes: {stats.pushes}")
    print(f"  Blackjacks: {stats.blackjacks}")
    print(f"  Player busts: {stats.player_busts}")
    print(f"  Dealer busts: {stats.dealer_busts}")
    
    print(f"\nStatistics:")
    print(f"  Win rate: {stats.win_rate:.1%}")
    print(f"  Blackjack rate: {stats.blackjack_rate:.1%}")
    print(f"  Player bust rate: {stats.player_bust_rate:.1%}")
    
    print(f"\nFinancial:")
    print(f"  Total bet: ${stats.total_bet}")
    print(f"  Total return: ${stats.total_return:.2f}")
    print(f"  Return percentage: {stats.return_percentage:.2f}%")
    
    # Simulate more rounds for better statistics
    print("\nSimulating 10,000 rounds...")
    stats = simulate_games(num_rounds=10000, num_decks=6, bet=10)
    print(f"  Long-term return: {stats.return_percentage:.2f}%")
    print(f"  (Expected: ~-0.5% with basic strategy)")


def example_counting_with_simulation():
    """Example: Card counting integrated with simulation."""
    print("\n" + "=" * 60)
    print("Example 9: Counting + Simulation")
    print("=" * 60)
    
    print("\nComparing play with and without counting adjustments:")
    
    # Basic strategy only
    simulator = GameSimulator(num_decks=6)
    stats_basic = simulator.simulate(num_rounds=1000, bet=10)
    print(f"\nBasic strategy only (1000 rounds):")
    print(f"  Return: {stats_basic.return_percentage:.2f}%")
    
    # With positive count (simulate favorable conditions)
    print("\nSimulating favorable shoe (many low cards dealt):")
    simulator.reset()
    counter = CardCounter(CountSystem.HI_LO, num_decks=6)
    
    # Remove many low cards to simulate favorable shoe
    for _ in range(80):
        simulator.deck.deal_one()  # Burn cards
        counter.add_card(card('2', 's'))  # Track as low card
    
    print(f"  True count: {counter.true_count:.2f}")
    print(f"  Player advantage: {counter.get_advantage():.2f}%")
    
    stats_good = simulator.simulate(num_rounds=500, bet=counter.get_bet_size(base_bet=25, min_bet=10))
    print(f"  Return (with larger bets): {stats_good.return_percentage:.2f}%")


def example_deviations():
    """Example: Strategy deviations based on count."""
    print("\n" + "=" * 60)
    print("Example 10: Illustrious 18 Deviations")
    print("=" * 60)
    
    counter = CardCounter(CountSystem.HI_LO, num_decks=6)
    
    # Simulate high count
    for _ in range(150):
        counter.add_card(card('2', 's'))
    
    print(f"\nWith true count of {counter.true_count:.1f}:")
    
    deviations = counter.get_deviations()
    active = [d for d in deviations if d['active']]
    
    print(f"  Active deviations: {len(active)}")
    for d in active:
        print(f"    {d['description']}")


def example_custom_strategy():
    """Example: Custom player strategy."""
    print("\n" + "=" * 60)
    print("Example 11: Custom Strategy Simulation")
    print("=" * 60)
    
    # Define a simple custom strategy
    def always_stand_on_16(hand, upcard):
        """Custom strategy: Stand on 16+."""
        if hand.best_value >= 16:
            return Action.STAND
        return Action.HIT
    
    simulator = GameSimulator(num_decks=6)
    
    print("\nComparing basic strategy vs 'Stand on 16' strategy:")
    
    # Basic strategy
    stats_basic = simulator.simulate(num_rounds=500, bet=10)
    print(f"  Basic strategy return: {stats_basic.return_percentage:.2f}%")
    
    # Custom strategy
    simulator.reset()
    stats_custom = simulator.simulate(num_rounds=500, bet=10, 
                                       player_strategy=always_stand_on_16)
    print(f"  'Stand on 16' return: {stats_custom.return_percentage:.2f}%")
    
    print(f"\n  Basic strategy is mathematically optimal!")


def example_full_game_playthrough():
    """Example: Full game playthrough."""
    print("\n" + "=" * 60)
    print("Example 12: Full Game Playthrough")
    print("=" * 60)
    
    simulator = GameSimulator(num_decks=1)
    
    print("\nPlaying a single round:")
    
    # Deal
    player_hand, dealer_hand, upcard = simulator.deal_initial_cards()
    print(f"\nInitial deal:")
    print(f"  Player: {player_hand}")
    print(f"  Dealer shows: {upcard}")
    
    # Check for naturals
    if player_hand.is_blackjack:
        print(f"  PLAYER BLACKJACK!")
        if dealer_hand.is_blackjack:
            print(f"  Dealer also has blackjack - PUSH")
        else:
            print(f"  Dealer has {dealer_hand.best_value} - WIN!")
        return
    
    # Get strategy
    action = BasicStrategy.get_action(player_hand, upcard)
    print(f"\nBasic strategy: {action.value}")
    
    # Execute actions
    while action != Action.STAND and not player_hand.is_bust:
        if action == Action.HIT:
            new_card = simulator.deck.deal_one()
            player_hand.add_card(new_card)
            print(f"  Hit: received {new_card}")
            print(f"  Hand now: {player_hand}")
            
            if player_hand.is_bust:
                print(f"  BUST! Player loses")
                return
            
            action = BasicStrategy.get_action(player_hand, upcard)
            print(f"  Next action: {action.value}")
        
        elif action == Action.DOUBLE:
            new_card = simulator.deck.deal_one()
            player_hand.add_card(new_card)
            print(f"  Double: received {new_card}")
            print(f"  Hand: {player_hand}")
            break
    
    # Dealer plays
    print(f"\nDealer plays:")
    print(f"  Dealer hole card: {dealer_hand.cards[1]}")
    print(f"  Dealer total: {dealer_hand.best_value}")
    
    while True:
        if dealer_hand.best_value < 17:
            new_card = simulator.deck.deal_one()
            dealer_hand.add_card(new_card)
            print(f"  Dealer hits: {new_card}")
            print(f"  Dealer total: {dealer_hand.best_value}")
        else:
            break
    
    # Outcome
    print(f"\nFinal hands:")
    print(f"  Player: {player_hand.best_value}")
    print(f"  Dealer: {dealer_hand.best_value}")
    
    if dealer_hand.is_bust:
        print(f"  Dealer BUST - Player wins!")
    elif player_hand.best_value > dealer_hand.best_value:
        print(f"  Player wins!")
    elif player_hand.best_value < dealer_hand.best_value:
        print(f"  Dealer wins")
    else:
        print(f"  Push (tie)")


def main():
    """Run all examples."""
    example_basic_cards()
    example_hand_evaluation()
    example_basic_strategy()
    example_strategy_charts()
    example_card_counting()
    example_different_count_systems()
    example_probability_calculations()
    example_game_simulation()
    example_counting_with_simulation()
    example_deviations()
    example_custom_strategy()
    example_full_game_playthrough()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()