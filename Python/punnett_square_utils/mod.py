"""
AllToolkit - Python Punnett Square Utilities

A zero-dependency genetics utility module for calculating genetic inheritance
probabilities using Punnett squares. Supports monohybrid crosses, dihybrid crosses,
multiple alleles, sex-linked traits, and blood type prediction.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Dict, Optional, Union
from itertools import product
from collections import Counter


class GeneticsError(Exception):
    """Base exception for genetics operations."""
    pass


class InvalidAlleleError(GeneticsError):
    """Raised when an invalid allele is provided."""
    pass


class InvalidCrossError(GeneticsError):
    """Raised when an invalid cross is attempted."""
    pass


# ============================================================================
# Basic Genetic Utilities
# ============================================================================

def is_heterozygous(genotype: str) -> bool:
    """
    Check if a genotype is heterozygous.
    
    A heterozygous genotype has one dominant allele (uppercase) and one
    recessive allele (lowercase) for the same gene type.
    
    Args:
        genotype: Two-letter genotype (e.g., 'Aa', 'Bb')
        
    Returns:
        True if heterozygous (one dominant, one recessive), False if homozygous
    """
    if len(genotype) != 2:
        raise InvalidAlleleError(f"Genotype must be 2 characters, got '{genotype}'")
    # Heterozygous = one uppercase (dominant) and one lowercase (recessive)
    # Same gene type means same letter when compared case-insensitively
    return (genotype[0].isupper() and genotype[1].islower()) or \
           (genotype[0].islower() and genotype[1].isupper())


def is_homozygous(genotype: str) -> bool:
    """
    Check if a genotype is homozygous.
    
    Args:
        genotype: Two-letter genotype (e.g., 'AA', 'aa')
        
    Returns:
        True if homozygous, False if heterozygous
    """
    return not is_heterozygous(genotype)


def is_dominant(allele: str) -> bool:
    """
    Check if an allele is dominant (uppercase).
    
    Args:
        allele: Single letter allele
        
    Returns:
        True if dominant, False if recessive
    """
    if len(allele) != 1:
        raise InvalidAlleleError(f"Allele must be single character, got '{allele}'")
    return allele.isupper()


def is_recessive(allele: str) -> bool:
    """
    Check if an allele is recessive (lowercase).
    
    Args:
        allele: Single letter allele
        
    Returns:
        True if recessive, False if dominant
    """
    return not is_dominant(allele)


def get_dominant_phenotype(genotype: str) -> str:
    """
    Get the phenotype assuming complete dominance.
    
    Args:
        genotype: Two-letter genotype
        
    Returns:
        Phenotype as dominant ('Dominant') or recessive ('Recessive')
    """
    if len(genotype) != 2:
        raise InvalidAlleleError(f"Genotype must be 2 characters, got '{genotype}'")
    
    # Sort to have consistent output
    sorted_geno = ''.join(sorted(genotype, key=lambda x: (x.islower(), x)))
    
    if any(c.isupper() for c in genotype):
        return 'Dominant'
    return 'Recessive'


def parse_genotype(genotype: str) -> Tuple[str, str]:
    """
    Parse a genotype string into allele tuple.
    
    Args:
        genotype: Genotype string
        
    Returns:
        Tuple of (allele1, allele2)
    """
    if len(genotype) != 2:
        raise InvalidAlleleError(f"Genotype must be 2 characters, got '{genotype}'")
    return (genotype[0], genotype[1])


def normalize_genotype(genotype: str) -> str:
    """
    Normalize genotype to have dominant allele first (if applicable).
    
    Args:
        genotype: Input genotype
        
    Returns:
        Normalized genotype
    """
    if len(genotype) != 2:
        raise InvalidAlleleError(f"Genotype must be 2 characters, got '{genotype}'")
    
    # Sort with dominant (uppercase) first
    return ''.join(sorted(genotype, key=lambda x: x.islower()))


# ============================================================================
# Gamete Generation
# ============================================================================

def generate_gametes(genotype: str) -> List[str]:
    """
    Generate all possible gametes from a genotype.
    
    Args:
        genotype: Two-letter genotype
        
    Returns:
        List of possible gametes
    """
    if len(genotype) != 2:
        raise InvalidAlleleError(f"Genotype must be 2 characters, got '{genotype}'")
    
    return [genotype[0], genotype[1]]


def generate_gametes_dihybrid(genotype1: str, genotype2: str) -> List[str]:
    """
    Generate all possible gametes for a dihybrid cross.
    
    Args:
        genotype1: First trait genotype (e.g., 'Aa')
        genotype2: Second trait genotype (e.g., 'Bb')
        
    Returns:
        List of possible gametes (e.g., ['AB', 'Ab', 'aB', 'ab'])
    """
    if len(genotype1) != 2 or len(genotype2) != 2:
        raise InvalidAlleleError("Both genotypes must be 2 characters")
    
    gametes1 = generate_gametes(genotype1)
    gametes2 = generate_gametes(genotype2)
    
    return [g1 + g2 for g1 in gametes1 for g2 in gametes2]


# ============================================================================
# Monohybrid Cross
# ============================================================================

def monohybrid_cross(parent1: str, parent2: str) -> Dict[str, any]:
    """
    Perform a monohybrid cross between two parents.
    
    Args:
        parent1: First parent's genotype (e.g., 'Aa')
        parent2: Second parent's genotype (e.g., 'Aa')
        
    Returns:
        Dictionary with Punnett square, genotypes, phenotypes, and ratios
    """
    if len(parent1) != 2 or len(parent2) != 2:
        raise InvalidAlleleError("Parent genotypes must be 2 characters")
    
    # Generate gametes
    gametes1 = generate_gametes(parent1)
    gametes2 = generate_gametes(parent2)
    
    # Create Punnett square
    punnett_square = []
    offspring_genotypes = []
    
    for g1 in gametes1:
        row = []
        for g2 in gametes2:
            # Sort to put dominant first
            offspring = normalize_genotype(g1 + g2)
            row.append(offspring)
            offspring_genotypes.append(offspring)
        punnett_square.append(row)
    
    # Calculate genotype ratios
    genotype_counts = Counter(offspring_genotypes)
    total = len(offspring_genotypes)
    genotype_ratios = {g: f"{c}/{total}" for g, c in genotype_counts.items()}
    genotype_percentages = {g: (c / total) * 100 for g, c in genotype_counts.items()}
    
    # Calculate phenotype ratios
    phenotypes = [get_dominant_phenotype(g) for g in offspring_genotypes]
    phenotype_counts = Counter(phenotypes)
    phenotype_ratios = {p: f"{c}/{total}" for p, c in phenotype_counts.items()}
    phenotype_percentages = {p: (c / total) * 100 for p, c in phenotype_counts.items()}
    
    return {
        'punnett_square': punnett_square,
        'gametes_parent1': gametes1,
        'gametes_parent2': gametes2,
        'offspring_genotypes': offspring_genotypes,
        'genotype_counts': dict(genotype_counts),
        'genotype_ratios': genotype_ratios,
        'genotype_percentages': genotype_percentages,
        'phenotype_counts': dict(phenotype_counts),
        'phenotype_ratios': phenotype_ratios,
        'phenotype_percentages': phenotype_percentages,
    }


def format_punnett_square(result: Dict) -> str:
    """
    Format a Punnett square result as a string table.
    
    Args:
        result: Result from monohybrid_cross or dihybrid_cross
        
    Returns:
        Formatted string table
    """
    punnett = result['punnett_square']
    gametes1 = result['gametes_parent1']
    gametes2 = result['gametes_parent2']
    
    # Calculate column widths
    cell_width = max(len(cell) for row in punnett for cell in row) + 2
    cell_width = max(cell_width, max(len(g) for g in gametes1 + gametes2) + 2)
    
    # Build header
    lines = []
    header = ' ' * cell_width + '|' + '|'.join(g.center(cell_width) for g in gametes2)
    lines.append(header)
    lines.append('-' * len(header))
    
    # Build rows
    for i, row in enumerate(punnett):
        row_str = gametes1[i].center(cell_width) + '|' + '|'.join(cell.center(cell_width) for cell in row)
        lines.append(row_str)
    
    return '\n'.join(lines)


# ============================================================================
# Dihybrid Cross
# ============================================================================

def dihybrid_cross(parent1_trait1: str, parent1_trait2: str,
                   parent2_trait1: str, parent2_trait2: str) -> Dict[str, any]:
    """
    Perform a dihybrid cross between two parents for two traits.
    
    Args:
        parent1_trait1: First parent's first trait genotype
        parent1_trait2: First parent's second trait genotype
        parent2_trait1: Second parent's first trait genotype
        parent2_trait2: Second parent's second trait genotype
        
    Returns:
        Dictionary with Punnett square, genotypes, phenotypes, and ratios
    """
    # Generate gametes
    gametes1 = generate_gametes_dihybrid(parent1_trait1, parent1_trait2)
    gametes2 = generate_gametes_dihybrid(parent2_trait1, parent2_trait2)
    
    # Create Punnett square
    punnett_square = []
    offspring_genotypes = []
    
    for g1 in gametes1:
        row = []
        for g2 in gametes2:
            # Combine alleles for each trait
            trait1_alleles = g1[0] + g2[0]
            trait2_alleles = g1[1] + g2[1]
            
            # Sort each trait
            offspring = normalize_genotype(trait1_alleles) + normalize_genotype(trait2_alleles)
            row.append(offspring)
            offspring_genotypes.append(offspring)
        punnett_square.append(row)
    
    # Calculate genotype ratios
    genotype_counts = Counter(offspring_genotypes)
    total = len(offspring_genotypes)
    genotype_ratios = {g: f"{c}/{total}" for g, c in genotype_counts.items()}
    genotype_percentages = {g: (c / total) * 100 for g, c in genotype_counts.items()}
    
    # Calculate phenotype ratios
    phenotypes = []
    for g in offspring_genotypes:
        p1 = get_dominant_phenotype(g[:2])
        p2 = get_dominant_phenotype(g[2:])
        phenotypes.append(f"{p1}-{p2}")
    
    phenotype_counts = Counter(phenotypes)
    phenotype_ratios = {p: f"{c}/{total}" for p, c in phenotype_counts.items()}
    phenotype_percentages = {p: (c / total) * 100 for p, c in phenotype_counts.items()}
    
    return {
        'punnett_square': punnett_square,
        'gametes_parent1': gametes1,
        'gametes_parent2': gametes2,
        'offspring_genotypes': offspring_genotypes,
        'genotype_counts': dict(genotype_counts),
        'genotype_ratios': genotype_ratios,
        'genotype_percentages': genotype_percentages,
        'phenotype_counts': dict(phenotype_counts),
        'phenotype_ratios': phenotype_ratios,
        'phenotype_percentages': phenotype_percentages,
    }


# ============================================================================
# Multiple Alleles (Blood Types)
# ============================================================================

# Blood type allele dominance: IA = IB > i
BLOOD_TYPE_ALLELES = {
    'IA': {'symbol': 'A', 'dominance': 2},
    'IB': {'symbol': 'B', 'dominance': 2},
    'i': {'symbol': 'O', 'dominance': 1},
}

# Blood type genotypes to phenotypes
BLOOD_TYPE_MAP = {
    ('IA', 'IA'): 'A',
    ('IA', 'i'): 'A',
    ('i', 'IA'): 'A',
    ('IB', 'IB'): 'B',
    ('IB', 'i'): 'B',
    ('i', 'IB'): 'B',
    ('IA', 'IB'): 'AB',
    ('IB', 'IA'): 'AB',
    ('i', 'i'): 'O',
}

# Rh factor
RH_FACTOR = {
    ('+', '+'): '+',
    ('+', '-'): '+',
    ('-', '+'): '+',
    ('-', '-'): '-',
}


def blood_type_cross(parent1_bt: str, parent1_rh: str,
                     parent2_bt: str, parent2_rh: str) -> Dict[str, any]:
    """
    Calculate possible blood types from parents.
    
    Args:
        parent1_bt: First parent's blood type genotype (e.g., 'IAi', 'IAIA', 'IBi', 'ii')
        parent1_rh: First parent's Rh factor (e.g., '++', '+-', '--')
        parent2_bt: Second parent's blood type genotype
        parent2_rh: Second parent's Rh factor
        
    Returns:
        Dictionary with possible blood types and probabilities
    """
    # Parse blood type alleles
    def parse_bt(bt: str) -> Tuple:
        if len(bt) == 2:
            return (bt[0], bt[1])
        elif len(bt) == 3 and bt[1:].upper() in ['IA', 'IB']:
            return (bt[:2], bt[2]) if len(bt) == 3 else (bt[0], bt[1:])
        raise InvalidAlleleError(f"Invalid blood type genotype: '{bt}'")
    
    def get_bt_alleles(bt: str) -> List[str]:
        """Extract individual alleles from blood type genotype."""
        if bt.upper() in ['IAIA', 'IBIB', 'IAIB', 'IBIA', 'IAI', 'IBI', 'II', 'II']:
            # Handle various formats
            bt = bt.upper()
            alleles = []
            i = 0
            while i < len(bt):
                if i + 1 < len(bt) and bt[i:i+2] in ['IA', 'IB']:
                    alleles.append(bt[i:i+2])
                    i += 2
                else:
                    alleles.append(bt[i])
                    i += 1
            return alleles
        # Simple format like 'Ai', 'Bi', 'ii'
        alleles = []
        i = 0
        while i < len(bt):
            if i + 1 < len(bt) and bt[i:i+2].upper() in ['IA', 'IB']:
                alleles.append(bt[i:i+2].upper())
                i += 2
            else:
                alleles.append(bt[i].upper() if bt[i].upper() == 'I' else 'i')
                i += 1
        return alleles
    
    # Get alleles for each parent
    p1_alleles = get_bt_alleles(parent1_bt)
    p2_alleles = get_bt_alleles(parent2_bt)
    
    # Get Rh alleles
    p1_rh_alleles = list(parent1_rh)
    p2_rh_alleles = list(parent2_rh)
    
    # Generate all combinations
    offspring_types = []
    for bt1 in p1_alleles:
        for bt2 in p2_alleles:
            # Determine blood type
            bt_combo = tuple(sorted([bt1, bt2], key=lambda x: (x != 'IA', x)))
            blood_type = BLOOD_TYPE_MAP.get(bt_combo) or BLOOD_TYPE_MAP.get((bt_combo[1], bt_combo[0]))
            if blood_type is None:
                # Handle IA/IB format
                if 'IA' in [bt1, bt2] and 'IB' in [bt1, bt2]:
                    blood_type = 'AB'
                elif 'IA' in [bt1, bt2] or bt1 == 'A' or bt2 == 'A':
                    blood_type = 'A'
                elif 'IB' in [bt1, bt2] or bt1 == 'B' or bt2 == 'B':
                    blood_type = 'B'
                else:
                    blood_type = 'O'
            
            for rh1 in p1_rh_alleles:
                for rh2 in p2_rh_alleles:
                    rh = RH_FACTOR.get((rh1, rh2), '+')
                    offspring_types.append(f"{blood_type}{rh}")
    
    # Calculate probabilities
    type_counts = Counter(offspring_types)
    total = len(offspring_types)
    probabilities = {bt: (count / total) * 100 for bt, count in type_counts.items()}
    
    return {
        'parent1_blood_type': parent1_bt,
        'parent1_rh': parent1_rh,
        'parent2_blood_type': parent2_bt,
        'parent2_rh': parent2_rh,
        'possible_types': list(type_counts.keys()),
        'type_counts': dict(type_counts),
        'probabilities': probabilities,
        'probabilities_formatted': {k: f"{v:.1f}%" for k, v in probabilities.items()},
    }


def blood_type_phenotype(genotype: str) -> str:
    """
    Determine blood type phenotype from genotype.
    
    Args:
        genotype: Blood type genotype (e.g., 'IAi', 'IAIB', 'ii')
        
    Returns:
        Blood type phenotype ('A', 'B', 'AB', or 'O')
    """
    genotype = genotype.upper()
    
    has_ia = 'IA' in genotype or (genotype.count('A') > 0 and 'I' in genotype)
    has_ib = 'IB' in genotype or (genotype.count('B') > 0 and 'I' in genotype)
    has_i = genotype == 'II' or genotype == 'ii' or genotype.count('i') >= 2
    
    if has_ia and has_ib:
        return 'AB'
    elif has_ia:
        return 'A'
    elif has_ib:
        return 'B'
    elif has_i or genotype.count('i') >= 1:
        if 'A' not in genotype and 'B' not in genotype:
            return 'O'
        elif 'A' in genotype:
            return 'A'
        elif 'B' in genotype:
            return 'B'
    return 'O'


# ============================================================================
# Sex-Linked Inheritance
# ============================================================================

def sex_linked_cross(mother_x1: str, mother_x2: str,
                     father_x: str, father_y: str = 'Y',
                     trait_on_x: bool = True) -> Dict[str, any]:
    """
    Calculate sex-linked inheritance (X-linked traits).
    
    Args:
        mother_x1: Mother's first X chromosome allele (e.g., 'X' or 'X^h')
        mother_x2: Mother's second X chromosome allele
        father_x: Father's X chromosome allele
        father_y: Father's Y chromosome (usually just 'Y')
        trait_on_x: Whether trait is X-linked (True) or Y-linked (False)
        
    Returns:
        Dictionary with offspring possibilities by sex
    """
    # Generate mother's gametes
    mother_gametes = [mother_x1, mother_x2]
    
    # Generate father's gametes
    father_gametes = [father_x, father_y]
    
    offspring = {
        'male': [],
        'female': [],
    }
    
    for m_gamete in mother_gametes:
        for f_gamete in father_gametes:
            if f_gamete == father_y:
                # Male offspring
                offspring['male'].append({
                    'chromosomes': f"{m_gamete}{f_gamete}",
                    'trait_allele': m_gamete,
                })
            else:
                # Female offspring
                offspring['female'].append({
                    'chromosomes': f"{m_gamete}{f_gamete}",
                    'trait_allele': f"{m_gamete}",
                })
    
    # Calculate probabilities
    male_count = len(offspring['male'])
    female_count = len(offspring['female'])
    total = male_count + female_count
    
    return {
        'offspring': offspring,
        'male_probability': (male_count / total) * 100,
        'female_probability': (female_count / total) * 100,
        'mother_gametes': mother_gametes,
        'father_gametes': father_gametes,
    }


# ============================================================================
# Incomplete Dominance & Codominance
# ============================================================================

def incomplete_dominance_cross(parent1: str, parent2: str,
                               phenotypes: Dict[str, str]) -> Dict[str, any]:
    """
    Cross with incomplete dominance (heterozygotes show intermediate phenotype).
    
    Args:
        parent1: First parent's genotype
        parent2: Second parent's genotype
        phenotypes: Dictionary mapping genotypes to phenotype names
                    (e.g., {'AA': 'Red', 'Aa': 'Pink', 'aa': 'White'})
        
    Returns:
        Dictionary with genotype and phenotype ratios
    """
    result = monohybrid_cross(parent1, parent2)
    
    # Map phenotypes
    phenotype_mapping = {}
    for genotype, count in result['genotype_counts'].items():
        phenotype = phenotypes.get(genotype, phenotypes.get(normalize_genotype(genotype), 'Unknown'))
        phenotype_mapping[genotype] = phenotype
    
    # Calculate phenotype counts
    phenotype_counts = Counter()
    for genotype, count in result['genotype_counts'].items():
        phenotype = phenotype_mapping[genotype]
        phenotype_counts[phenotype] += count
    
    result['phenotype_mapping'] = phenotype_mapping
    result['phenotype_counts'] = dict(phenotype_counts)
    
    total = sum(phenotype_counts.values())
    result['phenotype_percentages'] = {p: (c / total) * 100 for p, c in phenotype_counts.items()}
    
    return result


def codominance_cross(parent1: str, parent2: str,
                      alleles: List[str]) -> Dict[str, any]:
    """
    Cross with codominance (both alleles expressed equally).
    
    Args:
        parent1: First parent's genotype
        parent2: Second parent's genotype
        alleles: List of codominant allele symbols (e.g., ['A', 'B'] for blood type)
        
    Returns:
        Dictionary with genotype and phenotype ratios
    """
    result = monohybrid_cross(parent1, parent2)
    
    # For codominance, phenotype equals genotype (both alleles shown)
    # E.g., IA and IB are both expressed as AB blood type
    phenotype_counts = result['genotype_counts'].copy()
    
    result['codominant'] = True
    result['alleles'] = alleles
    
    return result


# ============================================================================
# Probability Calculations
# ============================================================================

def probability_of_genotype(parent1: str, parent2: str,
                            target_genotype: str) -> float:
    """
    Calculate the probability of a specific genotype from a cross.
    
    Args:
        parent1: First parent's genotype
        parent2: Second parent's genotype
        target_genotype: The genotype to find probability for
        
    Returns:
        Probability as a percentage (0-100)
    """
    result = monohybrid_cross(parent1, parent2)
    normalized_target = normalize_genotype(target_genotype)
    
    return result['genotype_percentages'].get(normalized_target, 0.0)


def probability_of_phenotype(parent1: str, parent2: str,
                             target_phenotype: str = 'Dominant') -> float:
    """
    Calculate the probability of a specific phenotype from a cross.
    
    Args:
        parent1: First parent's genotype
        parent2: Second parent's genotype
        target_phenotype: The phenotype to find probability for
        
    Returns:
        Probability as a percentage (0-100)
    """
    result = monohybrid_cross(parent1, parent2)
    return result['phenotype_percentages'].get(target_phenotype, 0.0)


def carrier_probability(parent_genotype: str) -> bool:
    """
    Check if a genotype is a carrier for a recessive trait.
    
    Args:
        parent_genotype: Parent's genotype
        
    Returns:
        True if the genotype is a carrier (heterozygous)
    """
    return is_heterozygous(parent_genotype)


# ============================================================================
# Pedigree Analysis Helpers
# ============================================================================

def infer_parent_genotypes(offspring_phenotypes: List[str],
                          dominant_phenotype: str = 'Dominant') -> List[Tuple[str, str]]:
    """
    Infer possible parent genotypes from offspring phenotypes.
    
    Args:
        offspring_phenotypes: List of offspring phenotype descriptions
        dominant_phenotype: The string representing dominant phenotype
        
    Returns:
        List of possible (parent1, parent2) genotype combinations
    """
    has_recessive = any(p != dominant_phenotype for p in offspring_phenotypes)
    all_dominant = all(p == dominant_phenotype for p in offspring_phenotypes)
    
    possible_parents = []
    
    if has_recessive:
        # At least one offspring is recessive, so both parents must carry recessive
        # Possible combinations: (Aa, Aa), (Aa, aa), (aa, Aa), (aa, aa)
        possible_parents = [
            ('Aa', 'Aa'),
            ('Aa', 'aa'),
            ('aa', 'Aa'),
            ('aa', 'aa'),
        ]
    elif all_dominant:
        # All dominant - many possibilities
        possible_parents = [
            ('AA', 'AA'),
            ('AA', 'Aa'),
            ('AA', 'aa'),
            ('Aa', 'AA'),
            ('Aa', 'Aa'),
        ]
    
    return possible_parents


def is_autosomal_recessive(genotype: str) -> bool:
    """
    Check if a genotype would show an autosomal recessive trait.
    
    Args:
        genotype: The genotype to check
        
    Returns:
        True if the trait would be expressed (homozygous recessive)
    """
    return is_homozygous(genotype) and all(c.islower() for c in genotype)


def is_x_linked_recessive(mother_genotype: str, father_affected: bool) -> Dict[str, any]:
    """
    Analyze X-linked recessive inheritance pattern.
    
    Args:
        mother_genotype: Mother's genotype (e.g., 'XX', 'Xx', 'xx' where x is mutant)
        father_affected: Whether the father has the trait
        
    Returns:
        Dictionary with inheritance analysis
    """
    # Simplified analysis
    mother_carrier = 'x' in mother_genotype.lower() and 'X' in mother_genotype
    
    results = {
        'mother_carrier': mother_carrier,
        'father_affected': father_affected,
        'sons_affected_prob': 0.0,
        'daughters_affected_prob': 0.0,
        'daughters_carrier_prob': 0.0,
    }
    
    if mother_carrier and not father_affected:
        # Carrier mother x unaffected father
        results['sons_affected_prob'] = 50.0
        results['daughters_affected_prob'] = 0.0
        results['daughters_carrier_prob'] = 50.0
    elif mother_carrier and father_affected:
        # Carrier mother x affected father
        results['sons_affected_prob'] = 50.0
        results['daughters_affected_prob'] = 50.0
        results['daughters_carrier_prob'] = 50.0
    elif not mother_carrier and father_affected:
        # Non-carrier mother x affected father
        results['sons_affected_prob'] = 0.0
        results['daughters_affected_prob'] = 0.0
        results['daughters_carrier_prob'] = 100.0
    
    return results


# ============================================================================
# Hardy-Weinberg Equilibrium
# ============================================================================

def hardy_weinberg_frequencies(p: float, q: float = None) -> Dict[str, float]:
    """
    Calculate genotype frequencies under Hardy-Weinberg equilibrium.
    
    Args:
        p: Frequency of dominant allele (A)
        q: Frequency of recessive allele (a). If None, calculated as q = 1 - p
        
    Returns:
        Dictionary with allele and genotype frequencies
    """
    if q is None:
        q = 1 - p
    
    if not (0 <= p <= 1 and 0 <= q <= 1):
        raise InvalidAlleleError("Allele frequencies must be between 0 and 1")
    
    if abs(p + q - 1) > 0.0001:
        raise InvalidAlleleError("Allele frequencies must sum to 1")
    
    # Hardy-Weinberg: p² + 2pq + q² = 1
    homozygous_dominant = p ** 2    # AA
    heterozygous = 2 * p * q        # Aa
    homozygous_recessive = q ** 2   # aa
    
    return {
        'p': p,                              # Dominant allele frequency
        'q': q,                              # Recessive allele frequency
        'AA': homozygous_dominant,           # Homozygous dominant frequency
        'Aa': heterozygous,                  # Heterozygous frequency
        'aa': homozygous_recessive,          # Homozygous recessive frequency
        'dominant_phenotype': homozygous_dominant + heterozygous,  # p² + 2pq
        'recessive_phenotype': homozygous_recessive,               # q²
    }


def hardy_weinberg_from_phenotype(recessive_frequency: float) -> Dict[str, float]:
    """
    Calculate allele frequencies from observed recessive phenotype frequency.
    
    Args:
        recessive_frequency: Observed frequency of recessive phenotype (0-1)
        
    Returns:
        Dictionary with allele and genotype frequencies
    """
    if not 0 <= recessive_frequency <= 1:
        raise InvalidAlleleError("Frequency must be between 0 and 1")
    
    # q² = recessive phenotype frequency
    # q = sqrt(q²)
    q = recessive_frequency ** 0.5
    p = 1 - q
    
    return hardy_weinberg_frequencies(p, q)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Exceptions
    'GeneticsError', 'InvalidAlleleError', 'InvalidCrossError',
    
    # Basic Utilities
    'is_heterozygous', 'is_homozygous', 'is_dominant', 'is_recessive',
    'get_dominant_phenotype', 'parse_genotype', 'normalize_genotype',
    
    # Gamete Generation
    'generate_gametes', 'generate_gametes_dihybrid',
    
    # Crosses
    'monohybrid_cross', 'dihybrid_cross', 'format_punnett_square',
    
    # Blood Types
    'blood_type_cross', 'blood_type_phenotype',
    
    # Sex-Linked
    'sex_linked_cross', 'is_x_linked_recessive',
    
    # Incomplete Dominance & Codominance
    'incomplete_dominance_cross', 'codominance_cross',
    
    # Probability
    'probability_of_genotype', 'probability_of_phenotype', 'carrier_probability',
    
    # Pedigree Analysis
    'infer_parent_genotypes', 'is_autosomal_recessive',
    
    # Hardy-Weinberg
    'hardy_weinberg_frequencies', 'hardy_weinberg_from_phenotype',
]