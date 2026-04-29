"""
AllToolkit - Dice Utilities Notation Example

Demonstrates dice notation parsing and rolling.
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from dice_utils import mod as dice


def main():
    print("=" * 60)
    print("Dice Utilities - Notation Example")
    print("=" * 60)
    print()
    
    parser = dice.DiceNotationParser()
    
    # Basic notation
    print("Basic Notation:")
    result = parser.roll("d6")
    print(f"  d6 → {result.total} (rolled {result.dice})")
    
    result = parser.roll("2d6")
    print(f"  2d6 → {result.total} (rolled {result.dice})")
    
    result = parser.roll("3d10")
    print(f"  3d10 → {result.total} (rolled {result.dice})")
    print()
    
    # With modifiers
    print("With Modifiers:")
    result = parser.roll("2d6+5")
    print(f"  2d6+5 → {result.total} ({result.dice} + 5)")
    
    result = parser.roll("1d20+3")
    print(f"  1d20+3 → {result.total} ({result.dice} + 3)")
    
    result = parser.roll("2d8-2")
    print(f"  2d8-2 → {result.total} ({result.dice} - 2)")
    print()
    
    # Keep/drop mechanics
    print("Keep/Drop Mechanics (D&D Ability Scores):")
    print("  Generating 6 ability scores using 4d6k3:")
    for ability in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
        result = parser.roll("4d6k3")
        print(f"    {ability}: {result.total} (kept {result.kept}, dropped {result.dropped})")
    print()
    
    # Keep lowest
    print("Keep Lowest:")
    result = parser.roll("4d6l2")
    print(f"  4d6l2 → {result.total} (kept {result.kept}, dropped {result.dropped})")
    print()
    
    # Drop lowest
    print("Drop Lowest:")
    result = parser.roll("4d6d1")
    print(f"  4d6d1 → {result.total} (kept {result.kept}, dropped {result.dropped})")
    print()
    
    # Exploding dice
    print("Exploding Dice:")
    result = parser.roll("1d6!")
    print(f"  1d6! → {result.total} (all rolls: {result.dice})")
    
    result = parser.roll("2d6!")
    print(f"  2d6! → {result.total} (all rolls: {result.dice})")
    print()
    
    # Reroll low values
    print("Reroll Low Values:")
    result = parser.roll("4d6r1")
    print(f"  4d6r1 → {result.dice} (no 1s)")
    assert 1 not in result.dice, "Reroll should eliminate 1s"
    print()
    
    # Parsing demonstration
    print("Parsing Notation:")
    parsed = parser.parse("4d6k3+2")
    print(f"  Notation: 4d6k3+2")
    print(f"  Parsed:")
    print(f"    - Dice count: {parsed['count']}")
    print(f"    - Dice sides: {parsed['sides']}")
    print(f"    - Keep type: {parsed['keep_type']}")
    print(f"    - Keep count: {parsed['keep_count']}")
    print(f"    - Modifier: {parsed['modifier']}")
    print()
    
    # Advantage/disadvantage simulation via notation
    print("Using roll_notation function:")
    result = dice.roll_notation("2d20kh1")  # Advantage
    print(f"  2d20kh1 (advantage): kept {result.kept}, total = {result.total}")
    
    result = dice.roll_notation("2d20kl1")  # Disadvantage  
    print(f"  2d20kl1 (disadvantage): kept {result.kept}, total = {result.total}")
    print()


if __name__ == "__main__":
    main()