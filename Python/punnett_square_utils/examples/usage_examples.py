"""
AllToolkit - Punnett Square Utilities Examples

Practical examples demonstrating genetic inheritance calculations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from punnett_square_utils.mod import (
    monohybrid_cross, dihybrid_cross, format_punnett_square,
    blood_type_cross, blood_type_phenotype,
    incomplete_dominance_cross,
    sex_linked_cross, is_x_linked_recessive,
    hardy_weinberg_frequencies, hardy_weinberg_from_phenotype,
    probability_of_genotype, probability_of_phenotype,
    carrier_probability, is_heterozygous, normalize_genotype,
)


def example_1_monohybrid_cross():
    """Example 1: Basic monohybrid cross (Mendel's pea plants)."""
    print("\n" + "=" * 60)
    print("Example 1: Monohybrid Cross (Pea Plant Height)")
    print("=" * 60)
    
    print("\nCrossing: Tt (heterozygous tall) × Tt (heterozygous tall)")
    print("T = dominant (tall), t = recessive (short)")
    
    result = monohybrid_cross('Tt', 'Tt')
    
    print("\nPunnett Square:")
    print(format_punnett_square(result))
    
    print("\nGenotype Results:")
    for genotype, count in result['genotype_counts'].items():
        percentage = result['genotype_percentages'][genotype]
        print(f"  {genotype}: {count} offspring ({percentage:.1f}%)")
    
    print("\nPhenotype Results:")
    for phenotype, count in result['phenotype_counts'].items():
        percentage = result['phenotype_percentages'][phenotype]
        phenotype_name = 'Tall' if phenotype == 'Dominant' else 'Short'
        print(f"  {phenotype_name}: {count} offspring ({percentage:.1f}%)")
    
    print("\nKey insight: Classic 3:1 phenotype ratio (75% tall, 25% short)")


def example_2_dihybrid_cross():
    """Example 2: Dihybrid cross (two traits)."""
    print("\n" + "=" * 60)
    print("Example 2: Dihybrid Cross (Pea Plant Shape & Color)")
    print("=" * 60)
    
    print("\nCrossing: RrYy × RrYy")
    print("R = round seeds (dominant), r = wrinkled seeds (recessive)")
    print("Y = yellow seeds (dominant), y = green seeds (recessive)")
    
    result = dihybrid_cross('Rr', 'Yy', 'Rr', 'Yy')
    
    print("\nPossible Gametes from Each Parent:")
    print(f"  Parent 1: {result['gametes_parent1']}")
    print(f"  Parent 2: {result['gametes_parent2']}")
    
    print("\nGenotype Counts (16 possible):")
    unique_genotypes = set(result['offspring_genotypes'])
    print(f"  {len(unique_genotypes)} unique genotypes")
    
    print("\nPhenotype Results (Classic 9:3:3:1 Ratio):")
    phenotype_mapping = {
        'Dominant-Dominant': 'Round, Yellow',
        'Dominant-Recessive': 'Round, Green',
        'Recessive-Dominant': 'Wrinkled, Yellow',
        'Recessive-Recessive': 'Wrinkled, Green',
    }
    
    for phenotype, count in sorted(result['phenotype_counts'].items()):
        percentage = result['phenotype_percentages'][phenotype]
        readable = phenotype_mapping.get(phenotype, phenotype)
        print(f"  {readable}: {count} offspring ({percentage:.1f}%)")
    
    print("\nKey insight: Classic 9:3:3:1 phenotype ratio")


def example_3_blood_type():
    """Example 3: Human blood type inheritance."""
    print("\n" + "=" * 60)
    print("Example 3: Blood Type Inheritance")
    print("=" * 60)
    
    print("\nScenario: Father with A+ blood (IAi, +-)")
    print("          Mother with B+ blood (IBi, +-)")
    
    result = blood_type_cross('IAi', '+-', 'IBi', '+-')
    
    print("\nPossible Blood Types for Children:")
    for blood_type, prob in sorted(result['probabilities'].items()):
        print(f"  {blood_type}: {prob:.1f}%")
    
    print("\nAnother Example: AB+ parent × O- parent")
    result2 = blood_type_cross('IAIB', '++', 'ii', '--')
    print("\nPossible Blood Types:")
    for blood_type, prob in sorted(result2['probabilities'].items()):
        print(f"  {blood_type}: {prob:.1f}%")
    
    print("\nKey insight: Blood type involves codominance (IA and IB)")


def example_4_incomplete_dominance():
    """Example 4: Incomplete dominance (snapdragon flowers)."""
    print("\n" + "=" * 60)
    print("Example 4: Incomplete Dominance (Snapdragon Flowers)")
    print("=" * 60)
    
    print("\nScenario: Crossing two pink snapdragons (Rr × Rr)")
    print("R = Red allele, r = White allele")
    print("RR = Red flowers, Rr = Pink flowers, rr = White flowers")
    
    phenotypes = {'RR': 'Red', 'Rr': 'Pink', 'rr': 'White'}
    result = incomplete_dominance_cross('Rr', 'Rr', phenotypes)
    
    print("\nPunnett Square:")
    print(format_punnett_square(result))
    
    print("\nGenotype Results:")
    for genotype, count in result['genotype_counts'].items():
        phenotype = result['phenotype_mapping'][genotype]
        print(f"  {genotype} → {phenotype}: {count} offspring")
    
    print("\nPhenotype Results:")
    for phenotype, count in result['phenotype_counts'].items():
        percentage = result['phenotype_percentages'][phenotype]
        print(f"  {phenotype}: {count} offspring ({percentage:.1f}%)")
    
    print("\nKey insight: 1:2:1 ratio for both genotypes AND phenotypes")


def example_5_sex_linked():
    """Example 5: Sex-linked inheritance (color blindness)."""
    print("\n" + "=" * 60)
    print("Example 5: Sex-Linked Inheritance (Color Blindness)")
    print("=" * 60)
    
    print("\nScenario: Carrier mother (X^cX) × Normal father (XY)")
    print("X^c = X chromosome with color blindness allele")
    print("X = Normal X chromosome")
    
    # Note: Using simplified notation where X^c means affected allele
    result = sex_linked_cross('Xc', 'X', 'X', 'Y')
    
    print("\nMale Offspring (inherit X from mother, Y from father):")
    for male in result['offspring']['male']:
        chromosomes = male['chromosomes']
        affected = 'c' in chromosomes
        status = 'Color blind' if affected else 'Normal vision'
        print(f"  {chromosomes}: {status}")
    
    print("\nFemale Offspring (inherit X from both parents):")
    for female in result['offspring']['female']:
        chromosomes = female['chromosomes']
        carrier = 'c' in chromosomes.lower() and 'X' in chromosomes
        status = 'Carrier' if carrier else 'Normal'
        print(f"  {chromosomes}: {status}")
    
    print("\nProbabilities:")
    print(f"  Male offspring: {result['male_probability']:.1f}%")
    print(f"  Female offspring: {result['female_probability']:.1f}%")
    
    print("\nKey insight: X-linked recessive traits affect males more often")


def example_6_hardy_weinberg():
    """Example 6: Hardy-Weinberg equilibrium calculations."""
    print("\n" + "=" * 60)
    print("Example 6: Hardy-Weinberg Equilibrium")
    print("=" * 60)
    
    print("\nScenario 1: Given allele frequencies")
    print("p (dominant allele frequency) = 0.8")
    print("q (recessive allele frequency) = 0.2")
    
    result = hardy_weinberg_frequencies(0.8, 0.2)
    
    print("\nExpected Genotype Frequencies:")
    print(f"  Homozygous dominant (AA): {result['AA']:.1%}")
    print(f"  Heterozygous (Aa): {result['Aa']:.1%}")
    print(f"  Homozygous recessive (aa): {result['aa']:.1%}")
    
    print("\nExpected Phenotype Frequencies:")
    print(f"  Dominant phenotype: {result['dominant_phenotype']:.1%}")
    print(f"  Recessive phenotype: {result['recessive_phenotype']:.1%}")
    
    print("\nScenario 2: From observed recessive phenotype frequency")
    print("If 9% of population shows recessive trait (albinism example)")
    
    result2 = hardy_weinberg_from_phenotype(0.09)
    
    print("\nCalculated Allele Frequencies:")
    print(f"  p (dominant): {result2['p']:.3f}")
    print(f"  q (recessive): {result2['q']:.3f}")
    
    print("\nCalculated Genotype Frequencies:")
    print(f"  Homozygous dominant: {result2['AA']:.1%}")
    print(f"  Heterozygous (carriers): {result2['Aa']:.1%}")
    print(f"  Homozygous recessive: {result2['aa']:.1%}")
    
    print("\nKey insight: q² = recessive frequency → q = √(q²)")


def example_7_probability_calculations():
    """Example 7: Probability calculations for genetic counseling."""
    print("\n" + "=" * 60)
    print("Example 7: Genetic Counseling Probability Calculations")
    print("=" * 60)
    
    print("\nScenario: Both parents are carriers for cystic fibrosis (Aa × Aa)")
    print("A = normal allele, a = cystic fibrosis allele")
    
    # Probability of affected child
    prob_affected = probability_of_genotype('Aa', 'Aa', 'aa')
    print(f"\nProbability of affected child (aa): {prob_affected:.1f}%")
    
    # Probability of carrier child
    prob_carrier = probability_of_genotype('Aa', 'Aa', 'Aa')
    print(f"Probability of carrier child (Aa): {prob_carrier:.1f}%")
    
    # Probability of unaffected (non-carrier)
    prob_unaffected = probability_of_genotype('Aa', 'Aa', 'AA')
    print(f"Probability of unaffected non-carrier (AA): {prob_unaffected:.1f}%")
    
    # Phenotype probability
    prob_normal_phenotype = probability_of_phenotype('Aa', 'Aa', 'Dominant')
    print(f"Probability of normal phenotype: {prob_normal_phenotype:.1f}%")
    
    print("\nAnother Scenario: One carrier, one affected (Aa × aa)")
    prob_affected2 = probability_of_genotype('Aa', 'aa', 'aa')
    prob_carrier2 = probability_of_genotype('Aa', 'aa', 'Aa')
    print(f"\nProbability of affected child: {prob_affected2:.1f}%")
    print(f"Probability of carrier child: {prob_carrier2:.1f}%")
    
    print("\nKey insight: Used for genetic counseling risk assessment")


def example_8_x_linked_analysis():
    """Example 8: X-linked recessive inheritance patterns."""
    print("\n" + "=" * 60)
    print("Example 8: X-Linked Recessive Pattern Analysis")
    print("=" * 60)
    
    print("\nScenario 1: Carrier mother × Unaffected father")
    result1 = is_x_linked_recessive('Xx', False)
    print(f"  Sons affected probability: {result1['sons_affected_prob']:.1f}%")
    print(f"  Daughters affected probability: {result1['daughters_affected_prob']:.1f}%")
    print(f"  Daughters carrier probability: {result1['daughters_carrier_prob']:.1f}%")
    
    print("\nScenario 2: Carrier mother × Affected father")
    result2 = is_x_linked_recessive('Xx', True)
    print(f"  Sons affected probability: {result2['sons_affected_prob']:.1f}%")
    print(f"  Daughters affected probability: {result2['daughters_affected_prob']:.1f}%")
    print(f"  Daughters carrier probability: {result2['daughters_carrier_prob']:.1f}%")
    
    print("\nScenario 3: Non-carrier mother × Affected father")
    result3 = is_x_linked_recessive('XX', True)
    print(f"  Sons affected probability: {result3['sons_affected_prob']:.1f}%")
    print(f"  Daughters carrier probability: {result3['daughters_carrier_prob']:.1f}%")
    
    print("\nKey insight: Fathers cannot pass X-linked traits to sons")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  Punnett Square Utils - Practical Examples")
    print("  Genetics Inheritance Calculations for Education & Research")
    print("=" * 70)
    
    example_1_monohybrid_cross()
    example_2_dihybrid_cross()
    example_3_blood_type()
    example_4_incomplete_dominance()
    example_5_sex_linked()
    example_6_hardy_weinberg()
    example_7_probability_calculations()
    example_8_x_linked_analysis()
    
    print("\n" + "=" * 70)
    print("  All examples completed successfully!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    run_all_examples()