"""
Test suite for De Bruijn sequence utilities.

Tests cover:
- Sequence generation for various parameters
- Validation of sequences
- Substring extraction and position finding
- Edge cases and error handling
- Convenience functions (binary, DNA, hex, etc.)
- Class-based interface
"""

import unittest
from de_bruijn import (
    de_bruijn,
    de_bruijn_generator,
    is_de_bruijn,
    get_all_substrings,
    find_substring_position,
    sequence_to_numbers,
    binary_de_bruijn,
    decimal_de_bruijn,
    hexadecimal_de_bruijn,
    dna_de_bruijn,
    alphabet_de_bruijn,
    find_shortest_containing,
    DeBruijnSequence
)


class TestDeBruijnGeneration(unittest.TestCase):
    """Tests for De Bruijn sequence generation."""
    
    def test_binary_small(self):
        """Test small binary sequences."""
        # B(2, 1): All 1-bit strings -> '01' or '10'
        seq = de_bruijn(2, 1)
        self.assertEqual(len(seq), 2)
        self.assertTrue(is_de_bruijn(seq, 1))
        
        # B(2, 2): All 2-bit strings -> length 4
        seq = de_bruijn(2, 2)
        self.assertEqual(len(seq), 4)
        self.assertTrue(is_de_bruijn(seq, 2))
        
        # B(2, 3): All 3-bit strings -> length 8
        seq = de_bruijn(2, 3)
        self.assertEqual(len(seq), 8)
        self.assertTrue(is_de_bruijn(seq, 3))
        
        # B(2, 4): All 4-bit strings -> length 16
        seq = de_bruijn(2, 4)
        self.assertEqual(len(seq), 16)
        self.assertTrue(is_de_bruijn(seq, 4))
    
    def test_custom_alphabet(self):
        """Test with custom alphabet."""
        seq = de_bruijn(2, 3, ['A', 'B'])
        self.assertEqual(len(seq), 8)
        self.assertTrue(all(c in ['A', 'B'] for c in seq))
        
        # Verify all 3-length AB strings appear
        extended = seq + seq[:2]
        substrings = {extended[i:i+3] for i in range(8)}
        expected = {'AAA', 'AAB', 'ABA', 'ABB', 'BAA', 'BAB', 'BBA', 'BBB'}
        self.assertEqual(substrings, expected)
    
    def test_trinary(self):
        """Test ternary sequences."""
        seq = de_bruijn(3, 2)
        self.assertEqual(len(seq), 9)  # 3^2 = 9
        self.assertTrue(is_de_bruijn(seq, 2))
        
        # All 2-digit ternary strings should appear
        substrings = get_all_substrings(seq, 2)
        self.assertEqual(len(substrings), 9)
    
    def test_quaternary(self):
        """Test quaternary sequences."""
        seq = de_bruijn(4, 2)
        self.assertEqual(len(seq), 16)  # 4^2 = 16
        self.assertTrue(is_de_bruijn(seq, 2))
    
    def test_invalid_parameters(self):
        """Test error handling for invalid parameters."""
        # k < 2
        with self.assertRaises(ValueError):
            de_bruijn(1, 2)
        
        # n < 1
        with self.assertRaises(ValueError):
            de_bruijn(2, 0)
        
        # alphabet mismatch
        with self.assertRaises(ValueError):
            de_bruijn(3, 2, ['A', 'B'])  # Should have 3 symbols
    
    def test_sequence_length_formula(self):
        """Verify sequence length is k^n."""
        for k in [2, 3, 4]:
            for n in [1, 2, 3]:
                seq = de_bruijn(k, n)
                self.assertEqual(len(seq), k ** n)


class TestDeBruijnGenerator(unittest.TestCase):
    """Tests for generator-based sequence production."""
    
    def test_generator_matches_function(self):
        """Generator should produce same sequence as function."""
        for k, n in [(2, 3), (2, 4), (3, 2)]:
            seq1 = de_bruijn(k, n)
            seq2 = ''.join(de_bruijn_generator(k, n))
            self.assertEqual(seq1, seq2)
    
    def test_generator_custom_alphabet(self):
        """Generator with custom alphabet."""
        gen = de_bruijn_generator(2, 3, ['X', 'Y'])
        seq = ''.join(gen)
        self.assertEqual(len(seq), 8)
        self.assertTrue(all(c in ['X', 'Y'] for c in seq))
    
    def test_generator_memory_efficiency(self):
        """Generator should not store entire sequence."""
        # For large sequences, generator is more memory efficient
        # This is a conceptual test - actual memory testing requires profiling
        gen = de_bruijn_generator(2, 5)
        first_char = next(gen)
        self.assertIn(first_char, ['0', '1'])


class TestValidation(unittest.TestCase):
    """Tests for sequence validation."""
    
    def test_valid_sequences(self):
        """Valid De Bruijn sequences should pass validation."""
        for n in [1, 2, 3, 4]:
            seq = binary_de_bruijn(n)
            self.assertTrue(is_de_bruijn(seq, n))
    
    def test_invalid_sequences(self):
        """Invalid sequences should fail validation."""
        # Wrong length
        self.assertFalse(is_de_bruijn('0001011', 3))  # Missing one char
        
        # Repeated substring
        self.assertFalse(is_de_bruijn('00000000', 3))  # All same
        
        # Missing substring - construct deliberately invalid sequence
        self.assertFalse(is_de_bruijn('00010110', 3))  # Missing 111
    
    def test_cyclic_validation(self):
        """Validation should consider cyclic nature."""
        seq = de_bruijn(2, 3)
        # Rotate the sequence - should still be valid
        rotated = seq[3:] + seq[:3]
        self.assertTrue(is_de_bruijn(rotated, 3))
    
    def test_edge_cases(self):
        """Edge cases in validation."""
        # Empty sequence
        self.assertFalse(is_de_bruijn('', 1))
        
        # n < 1
        self.assertFalse(is_de_bruijn('01', 0))


class TestSubstringOperations(unittest.TestCase):
    """Tests for substring extraction and finding."""
    
    def test_get_all_substrings(self):
        """Test substring extraction."""
        seq = binary_de_bruijn(3)
        substrings = get_all_substrings(seq, 3)
        
        # Should have exactly 8 substrings for B(2,3)
        self.assertEqual(len(substrings), 8)
        
        # All substrings should be 3 characters
        for sub in substrings:
            self.assertEqual(len(sub), 3)
    
    def test_find_substring_position(self):
        """Test substring position finding."""
        seq = binary_de_bruijn(3)
        
        # All substrings should be found
        for substring in get_all_substrings(seq, 3):
            pos = find_substring_position(seq, substring)
            self.assertGreaterEqual(pos, 0)
            self.assertLess(pos, len(seq))
        
        # Non-existent substring
        self.assertEqual(find_substring_position(seq, '222'), -1)
    
    def test_cyclic_position(self):
        """Position finding should handle cyclic wrapping."""
        seq = binary_de_bruijn(3)
        extended = seq + seq[:2]
        
        # Verify positions match actual substrings in extended sequence
        for i in range(len(seq)):
            substring = extended[i:i+3]
            pos = find_substring_position(seq, substring)
            self.assertEqual(extended[pos:pos+3], substring)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_binary_de_bruijn(self):
        """Binary convenience function."""
        for n in [1, 2, 3, 4]:
            seq = binary_de_bruijn(n)
            self.assertEqual(len(seq), 2 ** n)
            self.assertTrue(is_de_bruijn(seq, n))
    
    def test_decimal_de_bruijn(self):
        """Decimal convenience function."""
        seq = decimal_de_bruijn(2)
        self.assertEqual(len(seq), 100)
        self.assertTrue(is_de_bruijn(seq, 2))
        
        # n=3 is larger but still manageable
        seq = decimal_de_bruijn(3)
        self.assertEqual(len(seq), 1000)
    
    def test_hexadecimal_de_bruijn(self):
        """Hexadecimal convenience function."""
        seq = hexadecimal_de_bruijn(2)
        self.assertEqual(len(seq), 256)
        
        # Should contain hex digits only
        valid_chars = set('0123456789abcdef')
        self.assertTrue(all(c in valid_chars for c in seq))
    
    def test_dna_de_bruijn(self):
        """DNA convenience function."""
        seq = dna_de_bruijn(2)
        self.assertEqual(len(seq), 16)  # 4^2
        
        # Should contain DNA bases only
        valid_chars = set('ACGT')
        self.assertTrue(all(c in valid_chars for c in seq))
        
        # n=3
        seq = dna_de_bruijn(3)
        self.assertEqual(len(seq), 64)  # 4^3
    
    def test_alphabet_de_bruijn(self):
        """Alphabet convenience function."""
        seq = alphabet_de_bruijn(2)
        self.assertEqual(len(seq), 676)  # 26^2
        
        # Should contain lowercase letters only
        self.assertTrue(all(c.islower() for c in seq))


class TestSequenceConversion(unittest.TestCase):
    """Tests for sequence conversion utilities."""
    
    def test_sequence_to_numbers_default(self):
        """Default numeric conversion."""
        seq = binary_de_bruijn(3)
        nums = sequence_to_numbers(seq)
        
        self.assertEqual(len(nums), len(seq))
        self.assertTrue(all(n in [0, 1] for n in nums))
    
    def test_sequence_to_numbers_custom(self):
        """Custom alphabet conversion."""
        seq = de_bruijn(2, 3, ['A', 'B'])
        nums = sequence_to_numbers(seq, ['A', 'B'])
        
        self.assertTrue(all(n in [0, 1] for n in nums))
        # A should be 0, B should be 1
        for c, n in zip(seq, nums):
            if c == 'A':
                self.assertEqual(n, 0)
            else:
                self.assertEqual(n, 1)


class TestShortestContaining(unittest.TestCase):
    """Tests for shortest common superstring approximation."""
    
    def test_simple_overlap(self):
        """Test with simple overlapping strings."""
        result = find_shortest_containing(['abc', 'bcd', 'cde'])
        self.assertEqual(len(result), 5)  # Optimal is 'abcde'
        self.assertIn('abc', result)
        self.assertIn('bcd', result)
        self.assertIn('cde', result)
    
    def test_no_overlap(self):
        """Test with non-overlapping strings."""
        result = find_shortest_containing(['abc', 'xyz'])
        self.assertEqual(len(result), 6)  # Must be 'abcxyz' or 'xyzabc'
        self.assertIn('abc', result)
        self.assertIn('xyz', result)
    
    def test_single_string(self):
        """Test with single string."""
        result = find_shortest_containing(['hello'])
        self.assertEqual(result, 'hello')
    
    def test_empty_list(self):
        """Test with empty list."""
        result = find_shortest_containing([])
        self.assertEqual(result, '')


class TestDeBruijnSequenceClass(unittest.TestCase):
    """Tests for the DeBruijnSequence class."""
    
    def test_basic_creation(self):
        """Test class instantiation."""
        dbs = DeBruijnSequence(2, 3)
        
        self.assertEqual(dbs.k, 2)
        self.assertEqual(dbs.n, 3)
        self.assertEqual(len(dbs), 8)
    
    def test_string_representation(self):
        """Test string and repr."""
        dbs = DeBruijnSequence(2, 3)
        
        self.assertEqual(str(dbs), dbs.sequence)
        self.assertIn('DeBruijnSequence', repr(dbs))
        self.assertIn('k=2', repr(dbs))
        self.assertIn('n=3', repr(dbs))
    
    def test_cyclic_access(self):
        """Test cyclic indexing."""
        dbs = DeBruijnSequence(2, 3)
        
        # Regular access
        self.assertEqual(dbs[0], dbs.sequence[0])
        
        # Cyclic access
        self.assertEqual(dbs[len(dbs)], dbs[0])
        self.assertEqual(dbs[len(dbs) + 1], dbs[1])
        
        # Negative access
        self.assertEqual(dbs[-1], dbs[len(dbs) - 1])
    
    def test_contains(self):
        """Test contains method."""
        dbs = DeBruijnSequence(2, 3)
        
        # All valid substrings should be found
        for substring in get_all_substrings(dbs.sequence, 3):
            self.assertTrue(dbs.contains(substring))
        
        # Invalid substring
        self.assertFalse(dbs.contains('222'))
    
    def test_position(self):
        """Test position method."""
        dbs = DeBruijnSequence(2, 3)
        
        # Find existing substrings
        for substring in get_all_substrings(dbs.sequence, 3):
            pos = dbs.position(substring)
            self.assertGreaterEqual(pos, 0)
        
        # Non-existent substring
        self.assertEqual(dbs.position('xyz'), -1)
    
    def test_validation(self):
        """Test is_valid method."""
        dbs = DeBruijnSequence(2, 3)
        self.assertTrue(dbs.is_valid())
    
    def test_rotation(self):
        """Test rotate method."""
        dbs = DeBruijnSequence(2, 3)
        original = dbs.sequence
        
        # Rotate 0 -> same
        self.assertEqual(dbs.rotate(0), original)
        
        # Rotate full length -> same
        self.assertEqual(dbs.rotate(len(dbs)), original)
        
        # Rotate partial
        rotated = dbs.rotate(3)
        self.assertEqual(len(rotated), len(original))
        self.assertTrue(is_de_bruijn(rotated, dbs.n))
    
    def test_complement(self):
        """Test complement for binary sequences."""
        dbs = DeBruijnSequence(2, 3)
        comp = dbs.complement()
        
        self.assertEqual(len(comp), len(dbs))
        
        # Complement of complement should be original reversed
        comp_comp = ''.join('1' if c == '0' else '0' for c in comp[::-1])
        self.assertEqual(comp_comp, dbs.sequence)
    
    def test_complement_error(self):
        """Complement should error for non-binary."""
        dbs = DeBruijnSequence(3, 2)
        with self.assertRaises(ValueError):
            dbs.complement()
    
    def test_custom_alphabet(self):
        """Test with custom alphabet."""
        dbs = DeBruijnSequence(2, 3, ['X', 'Y'])
        
        self.assertTrue(all(c in ['X', 'Y'] for c in dbs.sequence))
        self.assertTrue(dbs.is_valid())


class TestPropertyBased(unittest.TestCase):
    """Property-based tests for mathematical properties."""
    
    def test_all_substrings_unique(self):
        """All substrings should be unique."""
        for n in [1, 2, 3, 4]:
            seq = binary_de_bruijn(n)
            substrings = get_all_substrings(seq, n)
            # Each substring should appear exactly once
            self.assertEqual(len(substrings), 2 ** n)
    
    def test_complete_coverage(self):
        """Sequence should cover all possible strings."""
        for k in [2, 3]:
            for n in [1, 2, 3]:
                seq = de_bruijn(k, n)
                substrings = get_all_substrings(seq, n)
                
                # Generate all expected strings
                alphabet = [str(i) for i in range(k)]
                expected = set()
                
                def generate(prefix: str):
                    if len(prefix) == n:
                        expected.add(prefix)
                        return
                    for s in alphabet:
                        generate(prefix + s)
                
                generate('')
                
                self.assertEqual(substrings, expected)
    
    def test_length_correctness(self):
        """Verify length formula k^n."""
        for k in [2, 3, 4, 5]:
            for n in [1, 2, 3]:
                seq = de_bruijn(k, n)
                self.assertEqual(len(seq), k ** n)


class TestPerformance(unittest.TestCase):
    """Performance tests for larger sequences."""
    
    def test_binary_10(self):
        """Test generation of B(2, 10)."""
        seq = binary_de_bruijn(10)
        self.assertEqual(len(seq), 1024)
    
    def test_binary_15(self):
        """Test generation of B(2, 15)."""
        seq = binary_de_bruijn(15)
        self.assertEqual(len(seq), 32768)
    
    def test_generator_large_sequence(self):
        """Test generator for large sequences."""
        # B(2, 16) = 65536 characters
        count = 0
        for _ in de_bruijn_generator(2, 16):
            count += 1
        self.assertEqual(count, 65536)
    
    def test_validation_speed(self):
        """Validation should be reasonably fast."""
        import time
        
        seq = binary_de_bruijn(12)  # 4096 characters
        
        start = time.time()
        result = is_de_bruijn(seq, 12)
        elapsed = time.time() - start
        
        self.assertTrue(result)
        # Should complete in reasonable time (< 1 second)
        self.assertLess(elapsed, 1.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)