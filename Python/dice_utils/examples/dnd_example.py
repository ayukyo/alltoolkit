"""
AllToolkit - Dice Utilities D&D Example

Demonstrates common D&D 5e dice mechanics.
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from dice_utils import mod as dice


def main():
    print("=" * 60)
    print("Dice Utilities - D&D 5e Example")
    print("=" * 60)
    print()
    
    # D20 attack roll with modifiers
    print("Attack Roll (D20):")
    parser = dice.DiceNotationParser()
    
    # Normal attack
    result = parser.roll("1d20+5")  # +5 proficiency bonus
    print(f"  Attack roll: {result.total} (rolled {result.dice[0]} + 5)")
    
    if result.dice[0] == 20:
        print("  NATURAL 20! Critical hit!")
    elif result.dice[0] == 1:
        print("  Natural 1... Critical miss!")
    print()
    
    # Advantage/Disadvantage
    print("Advantage and Disadvantage:")
    
    # Advantage
    result_adv = dice.roll_with_advantage(20)
    print(f"  With advantage: rolled [{result_adv.dice}], result = {result_adv.total}")
    
    # Disadvantage
    result_dis = dice.roll_with_disadvantage(20)
    print(f"  With disadvantage: rolled [{result_dis.dice}], result = {result_dis.total}")
    print()
    
    # Probability of advantage vs normal
    print("Advantage Statistics:")
    dist_normal = dice.dice_probability(1, 20)
    dist_advantage = dice.monte_carlo_simulation("2d20kh1", iterations=100000)
    
    print(f"  Normal d20 mean: {dist_normal.mean}")
    print(f"  Advantage mean: {dist_advantage['mean']:.2f}")
    
    # Probability of 20
    p20_normal = dist_normal.probability(20)
    p20_advantage = 1 - (19/20) ** 2  # Probability of at least one 20
    
    print(f"  P(20 normal): {p20_normal:.2%}")
    print(f"  P(20 with advantage): {p20_advantage:.2%}")
    print()
    
    # D&D Ability Score Generation
    print("Ability Score Generation (4d6 drop lowest):")
    abilities = {}
    total_modifiers = 0
    
    for ability in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        result = parser.roll("4d6d1")
        # Calculate modifier: (score - 10) // 2
        modifier = (result.total - 10) // 2
        mod_str = f"+{modifier}" if modifier >= 0 else str(modifier)
        abilities[ability] = (result.total, modifier)
        total_modifiers += modifier
        print(f"  {ability}: {result.total} ({mod_str})")
        print(f"    rolled {result.dice}, dropped {result.dropped}")
    
    print(f"  Total modifiers: {total_modifiers}")
    print()
    
    # Damage rolls
    print("Damage Rolls:")
    
    # Longsword (d8)
    damage = parser.roll("1d8+3")  # +3 strength modifier
    print(f"  Longsword (1d8+3): {damage.total} damage")
    
    # Greatsword (2d6)
    damage = parser.roll("2d6+3")
    print(f"  Greatsword (2d6+3): {damage.total} damage")
    
    # Fireball (8d6)
    damage = parser.roll("8d6")
    print(f"  Fireball (8d6): {damage.total} fire damage")
    print(f"    rolled: {damage.dice}")
    print()
    
    # Critical hit damage
    print("Critical Hit Damage:")
    # Longsword crit (double dice)
    crit_damage = parser.roll("2d8+3")
    print(f"  Longsword crit (2d8+3): {crit_damage.total} damage")
    
    # Greatsword crit
    crit_damage = parser.roll("4d6+3")
    print(f"  Greatsword crit (4d6+3): {crit_damage.total} damage")
    print()
    
    # Hit point rolling
    print("Hit Points (per level):")
    # Fighter with +2 CON modifier
    hp_roll = parser.roll("1d10+2")
    print(f"  Fighter level-up (1d10+2): {hp_roll.total} HP")
    
    # Wizard with +1 CON modifier
    hp_roll = parser.roll("1d6+1")
    print(f"  Wizard level-up (1d6+1): {hp_roll.total} HP")
    
    # Or take average
    print(f"  Fighter average: {dice.expected_value(1, 10) + 2:.0f} HP")
    print(f"  Wizard average: {dice.expected_value(1, 6) + 1:.0f} HP")
    print()
    
    # Skill check probability
    print("Skill Check Probabilities:")
    
    # DC 15 with +5 modifier
    # Need to roll >= 10 on d20
    p_success = dice.probability_at_least(1, 20, 15 - 5)
    # But 1 is auto-fail, 20 is auto-success
    # Adjusted probability (rolling 2-19)
    p_adjusted = (19 - (9 - 1)) / 20  # Need 10-19 or 20
    p_adjusted += 1/20  # Add probability of 20
    print(f"  DC 15 with +5 bonus: ~{p_adjusted:.0%} success rate")
    
    # DC 20 with +5
    # Need 15+ or 20
    p_success_hard = dice.probability_at_least(1, 20, 20 - 5)
    p_adjusted_hard = (19 - (14 - 1)) / 20 + 1/20
    print(f"  DC 20 with +5 bonus: ~{p_adjusted_hard:.0%} success rate")
    print()
    
    # Dice roller with history for session tracking
    print("Session Dice Roller:")
    roller = dice.DiceRoller()
    
    # Simulate a combat session
    print("  Combat session rolls:")
    roller.roll("1d20+7")  # Attack
    roller.roll("1d8+4")   # Damage
    roller.roll("1d20+5")  # Second attack
    roller.roll("2d6+4")   # Greatsword damage
    roller.roll("1d20+3")  # Opportunity attack
    
    # Analyze session
    analysis = roller.analyze_history()
    print(f"  Session stats:")
    print(f"    Total rolls: {analysis['total_rolls']}")
    print(f"    Average total: {analysis['mean_total']:.1f}")
    print(f"    Average die: {analysis['mean_die_value']:.1f}")
    print()


if __name__ == "__main__":
    main()