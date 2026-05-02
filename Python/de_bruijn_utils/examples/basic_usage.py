"""
De Bruijn Sequence Examples

This file demonstrates practical applications of De Bruijn sequences:
1. Password cracking optimization
2. DNA sequence assembly
3. Combinatorial testing
4. Efficient memory testing patterns
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from de_bruijn import (
    de_bruijn,
    binary_de_bruijn,
    dna_de_bruijn,
    hexadecimal_de_bruijn,
    decimal_de_bruijn,
    is_de_bruijn,
    get_all_substrings,
    find_substring_position,
    DeBruijnSequence
)


def example_basic_generation():
    """Basic De Bruijn sequence generation."""
    print("=" * 60)
    print("Basic De Bruijn Sequence Generation")
    print("=" * 60)
    
    # Binary sequence B(2, 3)
    print("\n1. Binary sequence B(2, 3):")
    seq = binary_de_bruijn(3)
    print(f"   Sequence: {seq}")
    print(f"   Length: {len(seq)} (expected: {2**3} = 8)")
    
    # Show all substrings
    substrings = sorted(get_all_substrings(seq, 3))
    print(f"   All 3-bit substrings: {substrings}")
    
    # Verify validity
    print(f"   Is valid: {is_de_bruijn(seq, 3)}")
    
    # Custom alphabet
    print("\n2. Custom alphabet (AB, n=3):")
    seq_ab = de_bruijn(2, 3, ['A', 'B'])
    print(f"   Sequence: {seq_ab}")
    print(f"   Substrings: {sorted(get_all_substrings(seq_ab, 3))}")
    
    # Ternary sequence
    print("\n3. Ternary sequence B(3, 2):")
    seq3 = de_bruijn(3, 2)
    print(f"   Sequence: {seq3}")
    print(f"   Length: {len(seq3)} (expected: {3**2} = 9)")


def example_password_cracking():
    """
    Demonstrate password cracking optimization.
    
    A De Bruijn sequence allows testing all password combinations
    with minimal keystrokes. For a password of length n, instead of
    entering n * k^n characters separately, we can enter just k^n + n - 1
    characters in one continuous stream.
    """
    print("\n" + "=" * 60)
    print("Password Cracking Optimization")
    print("=" * 60)
    
    # PIN codes (4 digits)
    print("\n1. 4-digit PIN codes:")
    pin_seq = decimal_de_bruijn(4)
    print(f"   Sequence length: {len(pin_seq)}")
    print(f"   Traditional approach: 4 * 10000 = 40000 keystrokes")
    print(f"   De Bruijn approach: {len(pin_seq)} + 3 = {len(pin_seq) + 3} keystrokes")
    print(f"   Efficiency gain: {40000 / (len(pin_seq) + 3):.1f}x")
    
    # Show sample positions
    print(f"   Position of '1234': {find_substring_position(pin_seq, '1234')}")
    print(f"   Position of '9999': {find_substring_position(pin_seq, '9999')}")
    
    # Binary password cracking
    print("\n2. 8-bit binary passwords:")
    binary_seq = binary_de_bruijn(8)
    print(f"   Sequence length: {len(binary_seq)}")
    print(f"   All 256 passwords covered")
    print(f"   Traditional: 8 * 256 = 2048 keystrokes")
    print(f"   De Bruijn: {len(binary_seq)} + 7 = {len(binary_seq) + 7} keystrokes")
    print(f"   Efficiency gain: {2048 / (len(binary_seq) + 7):.1f}x")


def example_dna_sequencing():
    """
    Demonstrate DNA sequence analysis.
    
    In bioinformatics, De Bruijn sequences and graphs are used for
    genome assembly from short reads.
    """
    print("\n" + "=" * 60)
    print("DNA Sequence Analysis")
    print("=" * 60)
    
    # DNA k-mers
    print("\n1. 2-base k-mers (dinucleotides):")
    dna2 = dna_de_bruijn(2)
    print(f"   Sequence: {dna2}")
    print(f"   All 16 dinucleotides covered")
    print(f"   Dinucleotides: {sorted(get_all_substrings(dna2, 2))}")
    
    print("\n2. 3-base k-mers (trinucleotides/codons):")
    dna3 = dna_de_bruijn(3)
    print(f"   Sequence length: {len(dna3)}")
    print(f"   All 64 codons covered")
    print(f"   Sample codon positions:")
    for codon in ['AAA', 'ATG', 'TAA']:
        pos = find_substring_position(dna3, codon)
        print(f"     {codon} (position {pos})")
    
    print("\n3. Practical application:")
    print("   If you sequence a genome and find overlapping reads,")
    print("   you can reconstruct the full sequence by finding the")
    print("   shortest path through a De Bruijn graph of k-mers.")


def example_testing_patterns():
    """
    Demonstrate use in combinatorial testing.
    
    De Bruijn sequences help generate efficient test patterns that
    cover all possible state combinations.
    """
    print("\n" + "=" * 60)
    print("Combinatorial Testing Patterns")
    print("=" * 60)
    
    # 2-state system over 3 time steps
    print("\n1. 2-state system (on/off), 3 time steps:")
    states = binary_de_bruijn(3)
    print(f"   Test sequence: {states}")
    print(f"   Covers all {2**3} state histories")
    
    # 4-state system (low/med/high/off) over 2 steps
    print("\n2. 4-state system, 2 transitions:")
    states4 = de_bruijn(4, 2, ['L', 'M', 'H', 'X'])
    print(f"   Test sequence: {states4}")
    print(f"   Covers all {4**2} transition patterns")
    
    # Hex values for testing
    print("\n3. Hexadecimal testing pattern (2 hex digits):")
    hex_seq = hexadecimal_de_bruijn(2)
    print(f"   Sequence length: {len(hex_seq)}")
    print(f"   Covers all 256 byte values (00-ff)")
    print(f"   First 20 chars: {hex_seq[:20]}...")


def example_class_interface():
    """Demonstrate the class-based interface."""
    print("\n" + "=" * 60)
    print("Class-Based Interface")
    print("=" * 60)
    
    # Create instance
    dbs = DeBruijnSequence(2, 4)
    print(f"\n1. Instance: {dbs}")
    print(f"   Sequence: {dbs.sequence}")
    
    # Operations
    print("\n2. Operations:")
    print(f"   Contains '0101': {dbs.contains('0101')}")
    print(f"   Position of '1111': {dbs.position('1111')}")
    print(f"   Is valid: {dbs.is_valid()}")
    
    # Rotation
    rotated = dbs.rotate(4)
    print(f"   Rotated by 4: {rotated}")
    
    # Cyclic access
    print(f"   dbs[0] = {dbs[0]}, dbs[16] = {dbs[16]} (cyclic)")
    
    # Complement
    comp = dbs.complement()
    print(f"   Complement: {comp}")


def example_real_world_applications():
    """Real-world application examples."""
    print("\n" + "=" * 60)
    print("Real-World Applications")
    print("=" * 60)
    
    print("\n1. Smart Door Lock Testing:")
    print("   - Test all 4-digit PIN combinations")
    print("   - Use decimal De Bruijn B(10, 4)")
    print("   - Type sequence into lock in one go")
    print("   - Lock accepts each 4-digit window as a PIN attempt")
    
    print("\n2. Barcode Scanner Testing:")
    print("   - Generate sequence containing all barcode patterns")
    print("   - Scan continuously, each window is a test case")
    
    print("\n3. Memory Testing:")
    print("   - Test all address patterns efficiently")
    print("   - De Bruijn sequence for memory addresses")
    
    print("\n4. Protocol Testing:")
    print("   - Test all packet header combinations")
    print("   - Generate comprehensive test sequences")
    
    print("\n5. Keyboard Testing:")
    print("   - Binary sequence for key combinations")
    print("   - Test all modifier + key combinations")


def example_sequence_properties():
    """Demonstrate mathematical properties."""
    print("\n" + "=" * 60)
    print("Mathematical Properties")
    print("=" * 60)
    
    print("\n1. Length formula: |B(k,n)| = k^n")
    for k, n in [(2, 4), (3, 3), (4, 2)]:
        seq = de_bruijn(k, n)
        print(f"   B({k},{n}): length {len(seq)} = {k}^{n} = {k**n}")
    
    print("\n2. Each substring appears exactly once:")
    seq = binary_de_bruijn(3)
    substrings = get_all_substrings(seq, 3)
    print(f"   B(2,3) has {len(substrings)} unique substrings")
    print(f"   Expected: 2^3 = 8")
    
    print("\n3. Cyclic property:")
    seq = binary_de_bruijn(3)
    extended = seq + seq[:2]
    print(f"   Original: {seq}")
    print(f"   Extended: {extended}")
    print(f"   Every 3-char window is unique")
    
    print("\n4. Multiple valid sequences exist:")
    seq1 = de_bruijn(2, 3)
    seq2 = de_bruijn(2, 3)
    # Note: algorithm produces deterministic output, but different algorithms
    # can produce different valid sequences
    print(f"   Our algorithm produces: {seq1}")
    print(f"   '00011101' is also valid for B(2,3)")
    print(f"   Validation: {is_de_bruijn('00011101', 3)}")


def main():
    """Run all examples."""
    example_basic_generation()
    example_password_cracking()
    example_dna_sequencing()
    example_testing_patterns()
    example_class_interface()
    example_real_world_applications()
    example_sequence_properties()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()