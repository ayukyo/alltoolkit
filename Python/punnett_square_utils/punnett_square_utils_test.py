"""
AllToolkit - Punnett Square Utilities Tests

Comprehensive tests for genetic inheritance calculations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from punnett_square_utils.mod import (
    # Basic Utilities
    is_heterozygous, is_homozygous, is_dominant, is_recessive,
    get_dominant_phenotype, normalize_genotype,
    
    # Gamete Generation
    generate_gametes, generate_gametes_dihybrid,
    
    # Crosses
    monohybrid_cross, dihybrid_cross, format_punnett_square,
    
    # Blood Types
    blood_type_cross, blood_type_phenotype,
    
    # Sex-Linked
    sex_linked_cross, is_x_linked_recessive,
    
    # Incomplete Dominance
    incomplete_dominance_cross, codominance_cross,
    
    # Probability
    probability_of_genotype, probability_of_phenotype, carrier_probability,
    
    # Pedigree
    infer_parent_genotypes, is_autosomal_recessive,
    
    # Hardy-Weinberg
    hardy_weinberg_frequencies, hardy_weinberg_from_phenotype,
    
    # Exceptions
    GeneticsError, InvalidAlleleError,
)


def test_basic_utilities():
    """Test basic genetic utility functions."""
    print("Testing basic utilities...")
    
    # Test heterozygous/homozygous
    assert is_heterozygous('Aa') == True
    assert is_heterozygous('aA') == True
    assert is_heterozygous('AA') == False
    assert is_heterozygous('aa') == False
    
    assert is_homozygous('AA') == True
    assert is_homozygous('aa') == True
    assert is_homozygous('Aa') == False
    
    # Test dominant/recessive
    assert is_dominant('A') == True
    assert is_dominant('B') == True
    assert is_recessive('a') == True
    assert is_recessive('b') == True
    
    # Test phenotype
    assert get_dominant_phenotype('AA') == 'Dominant'
    assert get_dominant_phenotype('Aa') == 'Dominant'
    assert get_dominant_phenotype('aA') == 'Dominant'
    assert get_dominant_phenotype('aa') == 'Recessive'
    
    # Test normalize genotype
    assert normalize_genotype('aA') == 'Aa'
    assert normalize_genotype('Aa') == 'Aa'
    assert normalize_genotype('AA') == 'AA'
    assert normalize_genotype('aa') == 'aa'
    
    print("  ✓ Basic utilities tests passed")


def test_gamete_generation():
    """Test gamete generation functions."""
    print("Testing gamete generation...")
    
    # Monohybrid gametes
    gametes = generate_gametes('Aa')
    assert set(gametes) == {'A', 'a'}
    
    gametes = generate_gametes('AA')
    assert set(gametes) == {'A', 'A'}
    
    # Dihybrid gametes
    gametes = generate_gametes_dihybrid('Aa', 'Bb')
    assert set(gametes) == {'AB', 'Ab', 'aB', 'ab'}
    
    gametes = generate_gametes_dihybrid('AA', 'BB')
    assert set(gametes) == {'AB', 'AB', 'AB', 'AB'}
    
    print("  ✓ Gamete generation tests passed")


def test_monohybrid_cross():
    """Test monohybrid cross calculations."""
    print("Testing monohybrid cross...")
    
    # Aa x Aa (classic 3:1 ratio)
    result = monohybrid_cross('Aa', 'Aa')
    assert result['genotype_counts']['AA'] == 1
    assert result['genotype_counts']['Aa'] == 2
    assert result['genotype_counts']['aa'] == 1
    
    assert result['phenotype_counts']['Dominant'] == 3
    assert result['phenotype_counts']['Recessive'] == 1
    
    # AA x aa (all heterozygous)
    result = monohybrid_cross('AA', 'aa')
    assert result['genotype_counts']['Aa'] == 4
    assert result['phenotype_counts']['Dominant'] == 4
    
    # aa x aa (all recessive)
    result = monohybrid_cross('aa', 'aa')
    assert result['genotype_counts']['aa'] == 4
    assert result['phenotype_counts']['Recessive'] == 4
    
    # AA x AA (all dominant)
    result = monohybrid_cross('AA', 'AA')
    assert result['genotype_counts']['AA'] == 4
    assert result['phenotype_counts']['Dominant'] == 4
    
    print("  ✓ Monohybrid cross tests passed")


def test_dihybrid_cross():
    """Test dihybrid cross calculations."""
    print("Testing dihybrid cross...")
    
    # AaBb x AaBb (classic 9:3:3:1 ratio)
    result = dihybrid_cross('Aa', 'Bb', 'Aa', 'Bb')
    
    # Should have 16 offspring
    assert len(result['offspring_genotypes']) == 16
    
    # Count phenotypes
    dom_dom = 0  # Both dominant
    dom_rec = 0  # Dominant first, recessive second
    rec_dom = 0  # Recessive first, dominant second
    rec_rec = 0  # Both recessive
    
    for pheno, count in result['phenotype_counts'].items():
        if 'Dominant-Dominant' in pheno:
            dom_dom += count
        elif 'Dominant-Recessive' in pheno:
            dom_rec += count
        elif 'Recessive-Dominant' in pheno:
            rec_dom += count
        elif 'Recessive-Recessive' in pheno:
            rec_rec += count
    
    assert dom_dom == 9, f"Expected 9 Dominant-Dominant, got {dom_dom}"
    assert dom_rec == 3, f"Expected 3 Dominant-Recessive, got {dom_rec}"
    assert rec_dom == 3, f"Expected 3 Recessive-Dominant, got {rec_dom}"
    assert rec_rec == 1, f"Expected 1 Recessive-Recessive, got {rec_rec}"
    
    print("  ✓ Dihybrid cross tests passed")


def test_format_punnett_square():
    """Test Punnett square formatting."""
    print("Testing Punnett square formatting...")
    
    result = monohybrid_cross('Aa', 'Aa')
    formatted = format_punnett_square(result)
    
    # Should contain the alleles
    assert 'A' in formatted
    assert 'a' in formatted
    assert '|' in formatted  # Table separator
    
    # Should be multiple lines
    lines = formatted.split('\n')
    assert len(lines) >= 3  # Header + separator + at least 1 data row
    
    print("  ✓ Punnett square formatting tests passed")


def test_blood_type():
    """Test blood type calculations."""
    print("Testing blood type calculations...")
    
    # IAi x IAi (both parents heterozygous A)
    result = blood_type_cross('IAi', '+-', 'IAi', '+-')
    assert 'A+' in result['possible_types']
    assert 'A-' in result['possible_types']
    
    # IAIB x ii (AB parent x O parent)
    result = blood_type_cross('IAIB', '++', 'ii', '--')
    # All children should be A or B (heterozygous)
    assert 'A+' in result['possible_types'] or 'B+' in result['possible_types']
    
    # Test phenotype determination
    assert blood_type_phenotype('IAIA') == 'A'
    assert blood_type_phenotype('IAi') == 'A'
    assert blood_type_phenotype('IBIB') == 'B'
    assert blood_type_phenotype('IBi') == 'B'
    assert blood_type_phenotype('IAIB') == 'AB'
    assert blood_type_phenotype('ii') == 'O'
    
    print("  ✓ Blood type tests passed")


def test_incomplete_dominance():
    """Test incomplete dominance calculations."""
    print("Testing incomplete dominance...")
    
    # Classic snapdragon example: Rr x Rr → 1 RR : 2 Rr : 1 rr
    phenotypes = {'RR': 'Red', 'Rr': 'Pink', 'rr': 'White'}
    result = incomplete_dominance_cross('Rr', 'Rr', phenotypes)
    
    assert result['genotype_counts']['RR'] == 1
    assert result['genotype_counts']['Rr'] == 2
    assert result['genotype_counts']['rr'] == 1
    
    assert result['phenotype_counts']['Red'] == 1
    assert result['phenotype_counts']['Pink'] == 2
    assert result['phenotype_counts']['White'] == 1
    
    print("  ✓ Incomplete dominance tests passed")


def test_probability():
    """Test probability calculations."""
    print("Testing probability calculations...")
    
    # Aa x Aa → 25% AA, 50% Aa, 25% aa
    assert probability_of_genotype('Aa', 'Aa', 'AA') == 25.0
    assert probability_of_genotype('Aa', 'Aa', 'Aa') == 50.0
    assert probability_of_genotype('Aa', 'Aa', 'aa') == 25.0
    
    # Phenotype probabilities
    assert probability_of_phenotype('Aa', 'Aa', 'Dominant') == 75.0
    assert probability_of_phenotype('Aa', 'Aa', 'Recessive') == 25.0
    
    # Carrier probability
    assert carrier_probability('Aa') == True
    assert carrier_probability('AA') == False
    assert carrier_probability('aa') == False
    
    print("  ✓ Probability tests passed")


def test_pedigree_analysis():
    """Test pedigree analysis functions."""
    print("Testing pedigree analysis...")
    
    # Test autosomal recessive detection
    assert is_autosomal_recessive('aa') == True
    assert is_autosomal_recessive('AA') == False
    assert is_autosomal_recessive('Aa') == False
    
    # Test parent genotype inference
    # Offspring with recessive phenotype means both parents carry recessive
    parents = infer_parent_genotypes(['Dominant', 'Dominant', 'Recessive'])
    assert ('Aa', 'Aa') in parents
    
    # All dominant offspring - many possibilities
    parents = infer_parent_genotypes(['Dominant', 'Dominant', 'Dominant'])
    assert ('AA', 'AA') in parents
    assert ('AA', 'Aa') in parents
    
    # Test X-linked recessive analysis
    result = is_x_linked_recessive('Xx', False)  # Carrier mother, unaffected father
    assert result['mother_carrier'] == True
    assert result['sons_affected_prob'] == 50.0
    
    print("  ✓ Pedigree analysis tests passed")


def test_hardy_weinberg():
    """Test Hardy-Weinberg equilibrium calculations."""
    print("Testing Hardy-Weinberg equilibrium...")
    
    # p = 0.7, q = 0.3
    result = hardy_weinberg_frequencies(0.7, 0.3)
    
    assert abs(result['AA'] - 0.49) < 0.001  # p² = 0.49
    assert abs(result['Aa'] - 0.42) < 0.001  # 2pq = 0.42
    assert abs(result['aa'] - 0.09) < 0.001  # q² = 0.09
    
    # Test with only p
    result = hardy_weinberg_frequencies(0.6)
    assert abs(result['q'] - 0.4) < 0.001
    
    # Test from recessive phenotype frequency
    # If 16% have recessive phenotype, q² = 0.16, q = 0.4
    result = hardy_weinberg_from_phenotype(0.16)
    assert abs(result['q'] - 0.4) < 0.001
    assert abs(result['p'] - 0.6) < 0.001
    assert abs(result['aa'] - 0.16) < 0.001
    
    print("  ✓ Hardy-Weinberg tests passed")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    # Invalid allele length
    try:
        is_heterozygous('ABC')
        assert False, "Should have raised InvalidAlleleError"
    except InvalidAlleleError:
        pass
    
    # Invalid monohybrid cross
    try:
        monohybrid_cross('A', 'Aa')  # Invalid length
        assert False, "Should have raised InvalidAlleleError"
    except InvalidAlleleError:
        pass
    
    # Invalid Hardy-Weinberg frequencies
    try:
        hardy_weinberg_frequencies(1.5)  # > 1
        assert False, "Should have raised InvalidAlleleError"
    except InvalidAlleleError:
        pass
    
    print("  ✓ Error handling tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "=" * 50)
    print("Running Punnett Square Utils Tests")
    print("=" * 50 + "\n")
    
    test_basic_utilities()
    test_gamete_generation()
    test_monohybrid_cross()
    test_dihybrid_cross()
    test_format_punnett_square()
    test_blood_type()
    test_incomplete_dominance()
    test_probability()
    test_pedigree_analysis()
    test_hardy_weinberg()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    run_all_tests()