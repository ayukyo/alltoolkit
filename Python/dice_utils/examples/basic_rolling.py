"""
AllToolkit - Dice Utilities Basic Rolling Example

Demonstrates basic dice rolling functions.
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from dice_utils import mod as dice


def main():
    print("=" * 60)
    print("Dice Utilities - Basic Rolling Example")
    print("=" * 60)
    print()
    
    # Standard dice
    print("Standard Dice:")
    print(f"  d4:  {dice.roll_d4().total}")
    print(f"  d6:  {dice.roll_d6().total}")
    print(f"  d8:  {dice.roll_d8().total}")
    print(f"  d10: {dice.roll_d10().total}")
    print(f"  d12: {dice.roll_d12().total}")
    print(f"  d20: {dice.roll_d20().total}")
    print(f"  d100: {dice.roll_d100().total}")
    print()
    
    # Multiple dice
    print("Multiple Dice:")
    result = dice.roll(6, count=3)
    print(f"  3d6: rolled {result.dice}, total = {result.total}")
    
    result = dice.roll(20, count=2)
    print(f"  2d20: rolled {result.dice}, total = {result.total}")
    print()
    
    # With modifiers
    print("With Modifiers:")
    result = dice.roll(6, count=3, modifier=5)
    print(f"  3d6+5: rolled {result.dice} + 5 = {result.total}")
    
    result = dice.roll(20, count=1, modifier=-3)
    print(f"  1d20-3: rolled {result.dice[0]} - 3 = {result.total}")
    print()
    
    # Percentile
    print("Percentile Dice:")
    result = dice.roll_percentile()
    print(f"  Percentile: {result.total}%")
    print()
    
    # Fate/Fudge dice
    print("Fate Dice (Fudge):")
    result = dice.roll_fate(4)
    symbols = ['-' if d == -1 else ' ' if d == 0 else '+' for d in result.dice]
    print(f"  4dF: [{symbols}] = {result.total}")
    print()


if __name__ == "__main__":
    main()