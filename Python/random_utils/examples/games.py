#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Games and Dice Examples

Demonstrates dice rolling, card drawing, and other game utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    roll_dice, roll_d20, coin_flip, draw_card,
    random_choice, random_shuffle, random_int
)


def roll_stats(method: str = '4d6 drop lowest') -> list:
    """
    Roll D&D character stats.
    
    Methods:
        - '3d6': Roll 3d6 for each stat
        - '4d6 drop lowest': Roll 4d6, drop lowest die
        - '2d6+6': Roll 2d6 and add 6
    """
    stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    results = {}
    
    for stat in stats:
        if method == '3d6':
            dice = roll_dice(6, 3)
            total = sum(dice)
        elif method == '4d6 drop lowest':
            dice = roll_dice(6, 4)
            dice.remove(min(dice))
            total = sum(dice)
        elif method == '2d6+6':
            dice = roll_dice(6, 2)
            total = sum(dice) + 6
        else:
            dice = roll_dice(6, 4)
            dice.remove(min(dice))
            total = sum(dice)
        
        results[stat] = {'dice': dice, 'total': total}
    
    return results


def poker_hand() -> list:
    """Draw a random 5-card poker hand."""
    deck = []
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")
    
    hand = []
    for _ in range(5):
        card = random_choice(deck)
        deck.remove(card)
        hand.append(card)
    
    return hand


def blackjack_hand() -> tuple:
    """Deal a blackjack hand (2 cards each for player and dealer)."""
    deck = []
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")
    
    player_hand = [deck.pop(random_int(0, len(deck)-1)) for _ in range(2)]
    dealer_hand = [deck.pop(random_int(0, len(deck)-1)) for _ in range(2)]
    
    return player_hand, dealer_hand


def d20_advantage() -> int:
    """Roll with advantage (take higher of 2d20)."""
    rolls = roll_dice(20, 2)
    return max(rolls), rolls


def d20_disadvantage() -> int:
    """Roll with disadvantage (take lower of 2d20)."""
    rolls = roll_dice(20, 2)
    return min(rolls), rolls


def initiative(creatures: list) -> list:
    """Roll initiative for multiple creatures."""
    results = []
    for creature in creatures:
        roll = roll_d20()
        # Simple modifier system
        modifier = random_int(-2, 5)
        total = roll + modifier
        results.append({
            'name': creature,
            'roll': roll,
            'modifier': modifier,
            'total': total
        })
    
    # Sort by initiative (highest first)
    results.sort(key=lambda x: x['total'], reverse=True)
    return results


def coin_toss_game(flips: int = 10) -> dict:
    """Simulate multiple coin flips."""
    results = {'heads': 0, 'tails': 0}
    flip_results = []
    
    for i in range(flips):
        result = coin_flip()
        results[result] += 1
        flip_results.append(result)
    
    results['sequence'] = flip_results
    return results


def main():
    print("="*60)
    print("Games and Dice Examples")
    print("="*60)
    
    # D&D Stats
    print("\n1. D&D Character Stats")
    print("-"*40)
    print("   Method: 4d6 drop lowest")
    stats = roll_stats()
    total = 0
    for stat, data in stats.items():
        print(f"   {stat}: {data['dice']} = {data['total']}")
        total += data['total']
    print(f"   Total: {total}")
    
    # Compare methods
    print("\n   Comparing methods:")
    for method in ['3d6', '4d6 drop lowest', '2d6+6']:
        s = roll_stats(method)
        avg = sum(d['total'] for d in s.values()) / 6
        print(f"   {method}: avg = {avg:.1f}")
    
    # D20 Rolls
    print("\n2. D20 Rolls")
    print("-"*40)
    print("   Normal roll:", roll_d20())
    
    result, rolls = d20_advantage()
    print(f"   Advantage: {rolls} → {result}")
    
    result, rolls = d20_disadvantage()
    print(f"   Disadvantage: {rolls} → {result}")
    
    # Initiative
    print("\n3. Initiative Order")
    print("-"*40)
    creatures = ['Fighter', 'Wizard', 'Rogue', 'Cleric', 'Goblin', 'Orc']
    init_order = initiative(creatures)
    for i, creature in enumerate(init_order, 1):
        mod_str = f"+{creature['modifier']}" if creature['modifier'] >= 0 else str(creature['modifier'])
        print(f"   {i}. {creature['name']}: {creature['roll']} {mod_str} = {creature['total']}")
    
    # Poker Hand
    print("\n4. Poker Hands")
    print("-"*40)
    for i in range(3):
        hand = poker_hand()
        print(f"   Hand {i+1}: {', '.join(hand)}")
    
    # Blackjack
    print("\n5. Blackjack")
    print("-"*40)
    player, dealer = blackjack_hand()
    print(f"   Player: {', '.join(player)}")
    print(f"   Dealer: {', '.join(dealer)} (one hidden)")
    
    # Dice Rolling
    print("\n6. Dice Rolling")
    print("-"*40)
    print("   2d6: ", roll_dice(6, 2))
    print("   3d8: ", roll_dice(8, 3))
    print("   4d10:", roll_dice(10, 4))
    print("   5d12:", roll_dice(12, 5))
    print("   1d100:", roll_dice(100, 1))
    
    # Coin Flips
    print("\n7. Coin Flips")
    print("-"*40)
    coin_result = coin_toss_game(20)
    print(f"   Sequence: {' '.join(coin_result['sequence'])}")
    print(f"   Heads: {coin_result['heads']}, Tails: {coin_result['tails']}")
    
    # Card Drawing
    print("\n8. Card Drawing")
    print("-"*40)
    print("   Standard deck:")
    for i in range(5):
        print(f"     {draw_card('standard')}")
    
    print("   Short deck (32 cards):")
    for i in range(5):
        print(f"     {draw_card('short')}")
    
    print("\n" + "="*60)
    print("Games examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
