"""
Tests for Bitmask Utils
"""

import unittest
from mod import (
    Bitmask, create_bitmask, from_bits, from_binary, from_hex,
    combine_bitmasks, intersect_bitmasks, count_bits, parity,
    reverse_bits, next_power_of_2, is_power_of_2, get_lsb, get_msb,
    gray_code, from_gray_code
)


class TestBitmaskBasicOperations(unittest.TestCase):
    """Test basic bitmask operations."""
    
    def test_create_bitmask(self):
        """Test bitmask creation."""
        mask = Bitmask()
        self.assertEqual(mask.to_int(), 0)
        self.assertEqual(len(mask), 32)
        
        mask = Bitmask(255, bits=8)
        self.assertEqual(mask.to_int(), 255)
        self.assertEqual(len(mask), 8)
    
    def test_invalid_bits(self):
        """Test invalid bit count."""
        with self.assertRaises(ValueError):
            Bitmask(bits=0)
        with self.assertRaises(ValueError):
            Bitmask(bits=-1)
    
    def test_set_bit(self):
        """Test setting bits."""
        mask = Bitmask(bits=8)
        mask.set(0)
        self.assertTrue(mask.has(0))
        self.assertEqual(mask.to_int(), 1)
        
        mask.set(7)
        self.assertTrue(mask.has(7))
        self.assertEqual(mask.to_int(), 129)
    
    def test_clear_bit(self):
        """Test clearing bits."""
        mask = Bitmask(255, bits=8)
        mask.clear(0)
        self.assertFalse(mask.has(0))
        self.assertEqual(mask.to_int(), 254)
        
        mask.clear(7)
        self.assertFalse(mask.has(7))
        self.assertEqual(mask.to_int(), 126)
    
    def test_toggle_bit(self):
        """Test toggling bits."""
        mask = Bitmask(bits=8)
        mask.toggle(0)
        self.assertTrue(mask.has(0))
        mask.toggle(0)
        self.assertFalse(mask.has(0))
    
    def test_invalid_bit_position(self):
        """Test invalid bit positions."""
        mask = Bitmask(bits=8)
        with self.assertRaises(ValueError):
            mask.set(-1)
        with self.assertRaises(ValueError):
            mask.set(8)
        with self.assertRaises(ValueError):
            mask.has(100)


class TestBitmaskMultiBitOperations(unittest.TestCase):
    """Test multi-bit operations."""
    
    def test_set_all(self):
        """Test setting multiple bits."""
        mask = Bitmask(bits=8)
        mask.set_all([0, 2, 4])
        self.assertEqual(mask.to_int(), 0b10101)
        self.assertTrue(mask.has_all([0, 2, 4]))
    
    def test_clear_all(self):
        """Test clearing multiple bits."""
        mask = Bitmask(255, bits=8)
        mask.clear_all([0, 2, 4])
        # 255 (0b11111111) - clearing bits 0, 2, 4 = 0b11101010 = 234
        self.assertEqual(mask.to_int(), 0b11101010)
    
    def test_toggle_all(self):
        """Test toggling multiple bits."""
        mask = Bitmask(0b10101010, bits=8)
        mask.toggle_all([0, 1, 2])
        # 0b10101010 (bits 1,3,5,7 set) toggle [0,1,2] -> bits 0,2,3,5,7 set = 0b10101101
        self.assertEqual(mask.to_int(), 0b10101101)
    
    def test_has_all(self):
        """Test checking all bits."""
        mask = Bitmask(0b10101, bits=8)
        self.assertTrue(mask.has_all([0, 2, 4]))
        self.assertFalse(mask.has_all([0, 2, 4, 6]))
    
    def test_has_any(self):
        """Test checking any bit."""
        mask = Bitmask(0b10101010, bits=8)  # bits 1, 3, 5, 7 are set
        self.assertFalse(mask.has_any([0, 2, 4]))  # bits 0, 2, 4 are NOT set
        self.assertTrue(mask.has_any([1]))  # bit 1 is set
        self.assertTrue(mask.has_any([1, 3]))  # bits 1, 3 are set
        self.assertFalse(mask.has_any([0, 4]))  # bits 0, 4 are NOT set
    
    def test_has_none(self):
        """Test checking no bits."""
        mask = Bitmask(0b10101010, bits=8)
        self.assertTrue(mask.has_none([0, 4, 6]))
        self.assertFalse(mask.has_none([1]))


class TestBitmaskRangeOperations(unittest.TestCase):
    """Test range operations."""
    
    def test_set_range(self):
        """Test setting a range of bits."""
        mask = Bitmask(bits=8)
        mask.set_range(2, 5)
        self.assertEqual(mask.to_int(), 0b111100)
    
    def test_clear_range(self):
        """Test clearing a range of bits."""
        mask = Bitmask(255, bits=8)
        mask.clear_range(2, 5)
        self.assertEqual(mask.to_int(), 0b11000011)
    
    def test_invalid_range(self):
        """Test invalid range."""
        mask = Bitmask(bits=8)
        with self.assertRaises(ValueError):
            mask.set_range(5, 2)


class TestBitmaskQueryOperations(unittest.TestCase):
    """Test query operations."""
    
    def test_count_set(self):
        """Test counting set bits."""
        mask = Bitmask(0b11110000, bits=8)
        self.assertEqual(mask.count_set(), 4)
        
        mask = Bitmask(255, bits=8)
        self.assertEqual(mask.count_set(), 8)
    
    def test_count_clear(self):
        """Test counting clear bits."""
        mask = Bitmask(0b11110000, bits=8)
        self.assertEqual(mask.count_clear(), 4)
    
    def test_first_set(self):
        """Test finding first set bit."""
        mask = Bitmask(0b10000, bits=8)
        self.assertEqual(mask.first_set(), 4)
        
        mask = Bitmask(0, bits=8)
        self.assertIsNone(mask.first_set())
    
    def test_last_set(self):
        """Test finding last set bit."""
        mask = Bitmask(0b10101000, bits=8)
        self.assertEqual(mask.last_set(), 7)
        
        mask = Bitmask(0, bits=8)
        self.assertIsNone(mask.last_set())
    
    def test_get_set_bits(self):
        """Test getting all set bits."""
        mask = Bitmask(0b10101, bits=8)
        self.assertEqual(mask.get_set_bits(), [0, 2, 4])
    
    def test_get_clear_bits(self):
        """Test getting all clear bits."""
        mask = Bitmask(0b10101, bits=8)
        self.assertEqual(mask.get_clear_bits(), [1, 3, 5, 6, 7])


class TestBitmaskManipulationOperations(unittest.TestCase):
    """Test manipulation operations."""
    
    def test_invert(self):
        """Test inverting bits."""
        mask = Bitmask(0b10101010, bits=8)
        mask.invert()
        self.assertEqual(mask.to_int(), 0b01010101)
    
    def test_shift_left(self):
        """Test left shift."""
        mask = Bitmask(0b00001111, bits=8)
        mask.shift_left(2)
        self.assertEqual(mask.to_int(), 0b00111100)
    
    def test_shift_right(self):
        """Test right shift."""
        mask = Bitmask(0b11110000, bits=8)
        mask.shift_right(2)
        self.assertEqual(mask.to_int(), 0b00111100)
    
    def test_rotate_left(self):
        """Test left rotation."""
        mask = Bitmask(0b10110000, bits=8)
        mask.rotate_left(4)
        self.assertEqual(mask.to_int(), 0b00001011)
    
    def test_rotate_right(self):
        """Test right rotation."""
        mask = Bitmask(0b00001011, bits=8)
        mask.rotate_right(4)
        self.assertEqual(mask.to_int(), 0b10110000)
    
    def test_reset(self):
        """Test reset."""
        mask = Bitmask(255, bits=8)
        mask.reset()
        self.assertEqual(mask.to_int(), 0)
    
    def test_fill(self):
        """Test fill."""
        mask = Bitmask(0, bits=8)
        mask.fill()
        self.assertEqual(mask.to_int(), 255)


class TestBitmaskLogicalOperations(unittest.TestCase):
    """Test logical operations."""
    
    def test_and_with(self):
        """Test AND operation."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b10101010, bits=8)
        mask1.and_with(mask2)
        self.assertEqual(mask1.to_int(), 0b10100000)
    
    def test_or_with(self):
        """Test OR operation."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b00001111, bits=8)
        mask1.or_with(mask2)
        self.assertEqual(mask1.to_int(), 0b11111111)
    
    def test_xor_with(self):
        """Test XOR operation."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b10101010, bits=8)
        mask1.xor_with(mask2)
        self.assertEqual(mask1.to_int(), 0b01011010)


class TestBitmaskComparisonOperations(unittest.TestCase):
    """Test comparison operations."""
    
    def test_is_subset(self):
        """Test subset check."""
        mask1 = Bitmask(0b1010, bits=4)
        mask2 = Bitmask(0b1110, bits=4)
        self.assertTrue(mask1.is_subset(mask2))
        
        mask1 = Bitmask(0b1010, bits=4)
        mask2 = Bitmask(0b0110, bits=4)
        self.assertFalse(mask1.is_subset(mask2))
    
    def test_is_superset(self):
        """Test superset check."""
        mask1 = Bitmask(0b1110, bits=4)
        mask2 = Bitmask(0b1010, bits=4)
        self.assertTrue(mask1.is_superset(mask2))
    
    def test_overlaps(self):
        """Test overlap check."""
        mask1 = Bitmask(0b1100, bits=4)
        mask2 = Bitmask(0b0011, bits=4)
        self.assertFalse(mask1.overlaps(mask2))
        
        mask2 = Bitmask(0b0101, bits=4)
        self.assertTrue(mask1.overlaps(mask2))
    
    def test_is_disjoint(self):
        """Test disjoint check."""
        mask1 = Bitmask(0b1100, bits=4)
        mask2 = Bitmask(0b0011, bits=4)
        self.assertTrue(mask1.is_disjoint(mask2))
        
        mask2 = Bitmask(0b0101, bits=4)
        self.assertFalse(mask1.is_disjoint(mask2))


class TestBitmaskConversionOperations(unittest.TestCase):
    """Test conversion operations."""
    
    def test_to_int(self):
        """Test integer conversion."""
        mask = Bitmask(123, bits=8)
        self.assertEqual(mask.to_int(), 123)
    
    def test_to_bin(self):
        """Test binary string conversion."""
        mask = Bitmask(0b101, bits=8)
        self.assertEqual(mask.to_bin(), "0b00000101")
        self.assertEqual(mask.to_bin(pad=False), "0b101")
        self.assertEqual(mask.to_bin(prefix="", pad=False), "101")
    
    def test_to_hex(self):
        """Test hex string conversion."""
        mask = Bitmask(255, bits=8)
        self.assertEqual(mask.to_hex(), "0xff")
        self.assertEqual(mask.to_hex(prefix="", pad=False), "ff")
    
    def test_to_list(self):
        """Test list conversion."""
        mask = Bitmask(0b101, bits=4)
        self.assertEqual(mask.to_list(), [1, 0, 1, 0])
    
    def test_to_set(self):
        """Test set conversion."""
        mask = Bitmask(0b101, bits=4)
        self.assertEqual(mask.to_set(), {0, 2})
    
    def test_copy(self):
        """Test copy."""
        mask1 = Bitmask(255, bits=8)
        mask2 = mask1.copy()
        self.assertEqual(mask1.to_int(), mask2.to_int())
        mask2.clear(0)
        self.assertNotEqual(mask1.to_int(), mask2.to_int())


class TestBitmaskMagicMethods(unittest.TestCase):
    """Test magic methods."""
    
    def test_int_conversion(self):
        """Test int() conversion."""
        mask = Bitmask(42, bits=8)
        self.assertEqual(int(mask), 42)
    
    def test_str_conversion(self):
        """Test str() conversion."""
        mask = Bitmask(5, bits=4)
        self.assertEqual(str(mask), "0b0101")
    
    def test_repr(self):
        """Test repr."""
        mask = Bitmask(42, bits=8)
        self.assertIn("Bitmask", repr(mask))
    
    def test_len(self):
        """Test len()."""
        mask = Bitmask(bits=16)
        self.assertEqual(len(mask), 16)
    
    def test_getitem(self):
        """Test indexing."""
        mask = Bitmask(0b101, bits=4)
        self.assertEqual(mask[0], 1)
        self.assertEqual(mask[1], 0)
        self.assertEqual(mask[2], 1)
    
    def test_setitem(self):
        """Test item assignment."""
        mask = Bitmask(bits=4)
        mask[0] = 1
        mask[1] = 1
        self.assertEqual(mask.to_int(), 3)
        mask[0] = 0
        self.assertEqual(mask.to_int(), 2)
    
    def test_contains(self):
        """Test 'in' operator."""
        mask = Bitmask(0b101, bits=4)
        self.assertTrue(0 in mask)
        self.assertFalse(1 in mask)
        self.assertTrue(2 in mask)
    
    def test_bitwise_and(self):
        """Test & operator."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b10101010, bits=8)
        result = mask1 & mask2
        self.assertEqual(result.to_int(), 0b10100000)
    
    def test_bitwise_or(self):
        """Test | operator."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b00001111, bits=8)
        result = mask1 | mask2
        self.assertEqual(result.to_int(), 255)
    
    def test_bitwise_xor(self):
        """Test ^ operator."""
        mask1 = Bitmask(0b11110000, bits=8)
        mask2 = Bitmask(0b10101010, bits=8)
        result = mask1 ^ mask2
        self.assertEqual(result.to_int(), 0b01011010)
    
    def test_bitwise_not(self):
        """Test ~ operator."""
        mask = Bitmask(0b10101010, bits=8)
        result = ~mask
        self.assertEqual(result.to_int(), 0b01010101)
    
    def test_lshift(self):
        """Test << operator."""
        mask = Bitmask(0b00001111, bits=8)
        result = mask << 2
        self.assertEqual(result.to_int(), 0b00111100)
    
    def test_rshift(self):
        """Test >> operator."""
        mask = Bitmask(0b11110000, bits=8)
        result = mask >> 2
        self.assertEqual(result.to_int(), 0b00111100)
    
    def test_equality(self):
        """Test == operator."""
        mask1 = Bitmask(42, bits=8)
        mask2 = Bitmask(42, bits=8)
        mask3 = Bitmask(42, bits=16)
        self.assertEqual(mask1, mask2)
        self.assertNotEqual(mask1, mask3)
    
    def test_hash(self):
        """Test hash."""
        mask1 = Bitmask(42, bits=8)
        mask2 = Bitmask(42, bits=8)
        self.assertEqual(hash(mask1), hash(mask2))
    
    def test_bool(self):
        """Test bool conversion."""
        self.assertTrue(bool(Bitmask(1, bits=8)))
        self.assertFalse(bool(Bitmask(0, bits=8)))


class TestFunctionalAPI(unittest.TestCase):
    """Test functional API."""
    
    def test_create_bitmask(self):
        """Test create_bitmask function."""
        mask = create_bitmask(255, bits=8)
        self.assertEqual(mask.to_int(), 255)
    
    def test_from_bits(self):
        """Test from_bits function."""
        mask = from_bits([0, 2, 4], total_bits=8)
        self.assertEqual(mask.to_int(), 0b10101)
    
    def test_from_binary(self):
        """Test from_binary function."""
        mask = from_binary("10101010")
        self.assertEqual(mask.to_int(), 0b10101010)
        
        mask = from_binary("0b1010")
        self.assertEqual(mask.to_int(), 0b1010)
        
        mask = from_binary("1111", total_bits=8)
        self.assertEqual(mask.to_int(), 0b1111)
        self.assertEqual(len(mask), 8)
    
    def test_from_hex(self):
        """Test from_hex function."""
        mask = from_hex("ff")
        self.assertEqual(mask.to_int(), 255)
        
        mask = from_hex("0xab")
        self.assertEqual(mask.to_int(), 0xab)
        
        mask = from_hex("f", total_bits=8)
        self.assertEqual(mask.to_int(), 15)
        self.assertEqual(len(mask), 8)
    
    def test_combine_bitmasks(self):
        """Test combine_bitmasks function."""
        mask1 = from_bits([0, 2], total_bits=8)  # 0b101
        mask2 = from_bits([1, 3], total_bits=8)  # 0b1010
        combined = combine_bitmasks(mask1, mask2)  # OR: 0b1111 = 15
        self.assertEqual(combined.to_int(), 0b1111)
    
    def test_intersect_bitmasks(self):
        """Test intersect_bitmasks function."""
        mask1 = from_bits([0, 1, 2], total_bits=8)
        mask2 = from_bits([1, 2, 3], total_bits=8)
        intersected = intersect_bitmasks(mask1, mask2)
        self.assertEqual(intersected.to_int(), 0b110)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_count_bits(self):
        """Test count_bits function."""
        self.assertEqual(count_bits(0), 0)
        self.assertEqual(count_bits(1), 1)
        self.assertEqual(count_bits(7), 3)
        self.assertEqual(count_bits(255), 8)
    
    def test_parity(self):
        """Test parity function."""
        self.assertEqual(parity(0), 0)
        self.assertEqual(parity(1), 1)
        self.assertEqual(parity(3), 0)  # 0b11 -> 0
        self.assertEqual(parity(7), 1)  # 0b111 -> 1
    
    def test_reverse_bits(self):
        """Test reverse_bits function."""
        self.assertEqual(reverse_bits(0b11010010, 8), 0b01001011)
        self.assertEqual(reverse_bits(0b11110000, 8), 0b00001111)
    
    def test_next_power_of_2(self):
        """Test next_power_of_2 function."""
        self.assertEqual(next_power_of_2(0), 1)
        self.assertEqual(next_power_of_2(1), 1)
        self.assertEqual(next_power_of_2(2), 2)
        self.assertEqual(next_power_of_2(3), 4)
        self.assertEqual(next_power_of_2(5), 8)
        self.assertEqual(next_power_of_2(16), 16)
        self.assertEqual(next_power_of_2(17), 32)
    
    def test_is_power_of_2(self):
        """Test is_power_of_2 function."""
        self.assertFalse(is_power_of_2(0))
        self.assertTrue(is_power_of_2(1))
        self.assertTrue(is_power_of_2(2))
        self.assertTrue(is_power_of_2(4))
        self.assertTrue(is_power_of_2(256))
        self.assertFalse(is_power_of_2(3))
        self.assertFalse(is_power_of_2(5))
        self.assertFalse(is_power_of_2(255))
    
    def test_get_lsb(self):
        """Test get_lsb function."""
        self.assertEqual(get_lsb(0b10100), 2)
        self.assertEqual(get_lsb(0b10000), 4)
        self.assertEqual(get_lsb(0), -1)
        self.assertEqual(get_lsb(1), 0)
    
    def test_get_msb(self):
        """Test get_msb function."""
        self.assertEqual(get_msb(0b10100, 8), 4)
        self.assertEqual(get_msb(0b10000000, 8), 7)
        self.assertEqual(get_msb(0, 8), -1)
    
    def test_gray_code(self):
        """Test gray_code function."""
        # Gray code: 0->0, 1->1, 2->3, 3->2, 4->6, 5->7, 6->5, 7->4
        self.assertEqual(gray_code(0), 0)
        self.assertEqual(gray_code(1), 1)
        self.assertEqual(gray_code(2), 3)
        self.assertEqual(gray_code(3), 2)
        self.assertEqual(gray_code(4), 6)
        self.assertEqual(gray_code(5), 7)
    
    def test_from_gray_code(self):
        """Test from_gray_code function."""
        # Reverse of gray_code tests
        self.assertEqual(from_gray_code(0), 0)
        self.assertEqual(from_gray_code(1), 1)
        self.assertEqual(from_gray_code(3), 2)
        self.assertEqual(from_gray_code(2), 3)
        self.assertEqual(from_gray_code(6), 4)
        self.assertEqual(from_gray_code(7), 5)
    
    def test_gray_code_roundtrip(self):
        """Test gray code roundtrip."""
        for i in range(100):
            gray = gray_code(i)
            back = from_gray_code(gray)
            self.assertEqual(back, i, f"Roundtrip failed for {i}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_operations(self):
        """Test operations on empty bitmask."""
        mask = Bitmask(bits=8)
        self.assertEqual(mask.count_set(), 0)
        self.assertEqual(mask.count_clear(), 8)
        self.assertIsNone(mask.first_set())
        self.assertIsNone(mask.last_set())
        self.assertEqual(mask.get_set_bits(), [])
        self.assertEqual(mask.get_clear_bits(), list(range(8)))
    
    def test_full_operations(self):
        """Test operations on full bitmask."""
        mask = Bitmask(255, bits=8)
        self.assertEqual(mask.count_set(), 8)
        self.assertEqual(mask.count_clear(), 0)
        self.assertEqual(mask.first_set(), 0)
        self.assertEqual(mask.last_set(), 7)
        self.assertEqual(mask.get_clear_bits(), [])
    
    def test_large_bitmask(self):
        """Test operations on large bitmask."""
        mask = Bitmask(bits=64)
        mask.set(63)
        self.assertTrue(mask.has(63))
        self.assertEqual(mask.first_set(), 63)
        self.assertEqual(mask.last_set(), 63)
    
    def test_negative_shift(self):
        """Test negative shift values."""
        mask = Bitmask(0b00111100, bits=8)
        result = mask.copy().shift_left(-2)
        self.assertEqual(result.to_int(), 0b00001111)
        
        result = mask.copy().shift_right(-2)
        self.assertEqual(result.to_int(), 0b11110000)
    
    def test_rotate_zero(self):
        """Test zero rotation."""
        mask = Bitmask(0b10101010, bits=8)
        result = mask.copy().rotate_left(0)
        self.assertEqual(result.to_int(), 0b10101010)
        
        result = mask.copy().rotate_right(0)
        self.assertEqual(result.to_int(), 0b10101010)
    
    def test_rotate_full(self):
        """Test full rotation."""
        mask = Bitmask(0b10101010, bits=8)
        result = mask.copy().rotate_left(8)
        self.assertEqual(result.to_int(), 0b10101010)


if __name__ == "__main__":
    unittest.main()