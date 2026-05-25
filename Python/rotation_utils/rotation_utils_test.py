"""Rotation Utils 测试套件"""
import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import *

class TestArrayRotation(unittest.TestCase):
    def test_rotate_left_simple(self):
        self.assertEqual(rotate_left_simple([1,2,3,4,5], 2), [3,4,5,1,2])
    def test_rotate_left_zero(self):
        self.assertEqual(rotate_left_simple([1,2,3,4,5], 0), [1,2,3,4,5])
    def test_rotate_left_full(self):
        self.assertEqual(rotate_left_simple([1,2,3,4,5], 5), [1,2,3,4,5])
    def test_rotate_right_simple(self):
        self.assertEqual(rotate_right_simple([1,2,3,4,5], 2), [4,5,1,2,3])
    def test_rotate_empty(self):
        self.assertEqual(rotate_left_simple([], 2), [])
    def test_rotate_left_right_equivalence(self):
        self.assertEqual(rotate_left_simple([1,2,3,4,5], 2), rotate_right_simple([1,2,3,4,5], 3))
    def test_rotate_left_inplace(self):
        arr = [1,2,3,4,5]
        rotate_left_inplace(arr, 2)
        self.assertEqual(arr, [3,4,5,1,2])
    def test_rotate_right_inplace(self):
        arr = [1,2,3,4,5]
        rotate_right_inplace(arr, 2)
        self.assertEqual(arr, [4,5,1,2,3])
    def test_rotate_left_juggling(self):
        self.assertEqual(rotate_left_juggling([1,2,3,4,5,6], 2), [3,4,5,6,1,2])
    def test_rotate_left_block_swap(self):
        self.assertEqual(rotate_left_block_swap([1,2,3,4,5], 2), [3,4,5,1,2])
    def test_all_algorithms_match(self):
        arr = [1,2,3,4,5,6,7,8]
        k = 3
        self.assertEqual(rotate_left_simple(arr, k), rotate_left_juggling(arr, k))
        self.assertEqual(rotate_left_simple(arr, k), rotate_left_block_swap(arr, k))

class TestBitRotation(unittest.TestCase):
    def test_rotate_left_8bit(self):
        self.assertEqual(rotate_left_bits(0b10110011, 3, 8), 0b10011101)
    def test_rotate_right_8bit(self):
        self.assertEqual(rotate_right_bits(0b10110011, 3, 8), 0b01110110)
    def test_rotate_left_right_inverse(self):
        self.assertEqual(rotate_right_bits(rotate_left_bits(0b10110011, 3, 8), 3, 8), 0b10110011)
    def test_rotate_full_cycle(self):
        self.assertEqual(rotate_left_bits(0b10110011, 8, 8), 0b10110011)
    def test_rotate_32bit(self):
        self.assertEqual(rotate_left_bits(0x12345678, 4, 32), 0x23456781)

class TestMatrixRotation(unittest.TestCase):
    def test_rotate_90_clockwise(self):
        self.assertEqual(rotate_matrix_90_clockwise([[1,2,3],[4,5,6],[7,8,9]]), [[7,4,1],[8,5,2],[9,6,3]])
    def test_rotate_90_counterclockwise(self):
        self.assertEqual(rotate_matrix_90_counterclockwise([[1,2,3],[4,5,6],[7,8,9]]), [[3,6,9],[2,5,8],[1,4,7]])
    def test_rotate_180(self):
        self.assertEqual(rotate_matrix_180([[1,2,3],[4,5,6],[7,8,9]]), [[9,8,7],[6,5,4],[3,2,1]])
    def test_rotate_90_twice_is_180(self):
        self.assertEqual(rotate_matrix_90_clockwise(rotate_matrix_90_clockwise([[1,2,3],[4,5,6],[7,8,9]])), rotate_matrix_180([[1,2,3],[4,5,6],[7,8,9]]))
    def test_rotate_non_square_matrix(self):
        self.assertEqual(rotate_matrix_90_clockwise([[1,2,3,4],[5,6,7,8]]), [[5,1],[6,2],[7,3],[8,4]])
    def test_rotate_matrix_inplace(self):
        m = [[1,2],[3,4]]
        rotate_matrix_inplace(m, 90)
        self.assertEqual(m, [[3,1],[4,2]])
    def test_rotate_invalid_angle(self):
        self.assertRaises(ValueError, rotate_matrix, [[1,2],[3,4]], 45)

class TestStringRotation(unittest.TestCase):
    def test_rotate_string_left(self):
        self.assertEqual(rotate_string_left("hello", 2), "llohe")
    def test_rotate_string_right(self):
        self.assertEqual(rotate_string_right("hello", 2), "lohel")
    def test_is_rotation_true(self):
        self.assertTrue(is_rotation("hello", "llohe"))
        self.assertTrue(is_rotation("hello", "hello"))
    def test_is_rotation_false(self):
        self.assertFalse(is_rotation("hello", "world"))
        self.assertFalse(is_rotation("hello", "hell"))
    def test_find_rotation_distance(self):
        self.assertEqual(find_rotation_distance("hello", "llohe"), 2)
        self.assertEqual(find_rotation_distance("hello", "hello"), 0)
        self.assertEqual(find_rotation_distance("hello", "lohel"), 3)
    def test_get_all_rotations(self):
        self.assertEqual(get_all_rotations("abc"), ["abc","bca","cab"])

class TestPointRotation(unittest.TestCase):
    def test_rotate_90_degrees(self):
        x, y = rotate_2d_point(1, 0, 90)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 1.0)
    def test_rotate_180_degrees(self):
        x, y = rotate_2d_point(1, 0, 180)
        self.assertAlmostEqual(x, -1.0)
        self.assertAlmostEqual(y, 0.0)
    def test_rotate_with_center(self):
        x, y = rotate_2d_point(2, 1, 90, center=(1, 1))
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 2.0)

class TestRotatorClass(unittest.TestCase):
    def test_rotator_left(self):
        self.assertEqual(Rotator([1,2,3,4,5]).left(2).result(), [3,4,5,1,2])
    def test_rotator_right(self):
        self.assertEqual(Rotator([1,2,3,4,5]).right(2).result(), [4,5,1,2,3])
    def test_rotator_chain(self):
        self.assertEqual(Rotator([1,2,3,4,5]).left(2).right(1).result(), [2,3,4,5,1])

class TestBitRotatorClass(unittest.TestCase):
    def test_bit_rotator_left(self):
        self.assertEqual(BitRotator(0b10110011, 8).left(3).value(), 0b10011101)
    def test_bit_rotator_right(self):
        self.assertEqual(BitRotator(0b10110011, 8).right(3).value(), 0b01110110)
    def test_bit_rotator_chain(self):
        self.assertEqual(BitRotator(0b10110011, 8).left(3).right(3).value(), 0b10110011)

class TestRotateFunction(unittest.TestCase):
    def test_rotate_list(self):
        self.assertEqual(rotate([1,2,3,4,5], 2), [3,4,5,1,2])
    def test_rotate_string(self):
        self.assertEqual(rotate("hello", 2), "llohe")
    def test_rotate_int(self):
        self.assertEqual(rotate(0x12345678, 4), 0x23456781)

class TestEdgeCases(unittest.TestCase):
    def test_unicode_string_rotation(self):
        self.assertEqual(rotate_string_left("你好世界", 2), "世界你好")
    def test_large_rotation(self):
        self.assertEqual(rotate_left_simple([1,2,3], 1000), [2,3,1])

if __name__ == "__main__":
    unittest.main(verbosity=2)
