"""
Tests for Matrix Utilities
"""

import math
import unittest
from matrix_utils import (
    Matrix, dot, cross, vector_norm, normalize, 
    angle_between, is_orthogonal, gram_schmidt
)


class TestMatrixCreation(unittest.TestCase):
    """Test matrix creation and basic properties."""
    
    def test_create_from_list(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 2)
        self.assertEqual(m.shape, (2, 2))
    
    def test_create_empty_raises(self):
        with self.assertRaises(ValueError):
            Matrix([])
        with self.assertRaises(ValueError):
            Matrix([[]])
    
    def test_inconsistent_rows_raises(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])
    
    def test_zeros(self):
        m = Matrix.zeros(3, 4)
        self.assertEqual(m.shape, (3, 4))
        for i in range(3):
            for j in range(4):
                self.assertEqual(m[i, j], 0.0)
    
    def test_ones(self):
        m = Matrix.ones(2, 3)
        self.assertEqual(m.shape, (2, 3))
        for i in range(2):
            for j in range(3):
                self.assertEqual(m[i, j], 1.0)
    
    def test_identity(self):
        m = Matrix.identity(3)
        self.assertEqual(m.shape, (3, 3))
        for i in range(3):
            for j in range(3):
                self.assertEqual(m[i, j], 1.0 if i == j else 0.0)
    
    def test_diagonal(self):
        m = Matrix.diagonal([1, 2, 3])
        self.assertEqual(m[0, 0], 1.0)
        self.assertEqual(m[1, 1], 2.0)
        self.assertEqual(m[2, 2], 3.0)
        self.assertEqual(m[0, 1], 0.0)
    
    def test_random(self):
        m = Matrix.random(3, 4, low=-1, high=1)
        self.assertEqual(m.shape, (3, 4))
        for i in range(3):
            for j in range(4):
                self.assertGreaterEqual(m[i, j], -1.0)
                self.assertLessEqual(m[i, j], 1.0)
    
    def test_from_rows(self):
        m = Matrix.from_rows([1, 2], [3, 4])
        self.assertEqual(m[0, 0], 1.0)
        self.assertEqual(m[0, 1], 2.0)
        self.assertEqual(m[1, 0], 3.0)
        self.assertEqual(m[1, 1], 4.0)
    
    def test_from_cols(self):
        m = Matrix.from_cols([1, 2], [3, 4])
        self.assertEqual(m[0, 0], 1.0)
        self.assertEqual(m[1, 0], 2.0)
        self.assertEqual(m[0, 1], 3.0)
        self.assertEqual(m[1, 1], 4.0)
    
    def test_hilbert(self):
        m = Matrix.hilbert(3)
        self.assertEqual(m[0, 0], 1.0)
        self.assertAlmostEqual(m[0, 1], 0.5)
        self.assertAlmostEqual(m[1, 0], 0.5)
        self.assertAlmostEqual(m[1, 1], 1.0/3.0)
    
    def test_vandermonde(self):
        m = Matrix.vandermonde([1, 2, 3])
        self.assertEqual(m[0, 0], 1.0)
        self.assertEqual(m[1, 1], 2.0)
        self.assertEqual(m[2, 2], 9.0)


class TestMatrixArithmetic(unittest.TestCase):
    """Test matrix arithmetic operations."""
    
    def test_addition(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        c = a + b
        self.assertEqual(c[0, 0], 6.0)
        self.assertEqual(c[0, 1], 8.0)
        self.assertEqual(c[1, 0], 10.0)
        self.assertEqual(c[1, 1], 12.0)
    
    def test_subtraction(self):
        a = Matrix([[5, 6], [7, 8]])
        b = Matrix([[1, 2], [3, 4]])
        c = a - b
        self.assertEqual(c[0, 0], 4.0)
        self.assertEqual(c[0, 1], 4.0)
        self.assertEqual(c[1, 0], 4.0)
        self.assertEqual(c[1, 1], 4.0)
    
    def test_scalar_multiplication(self):
        a = Matrix([[1, 2], [3, 4]])
        b = a * 2
        self.assertEqual(b[0, 0], 2.0)
        self.assertEqual(b[1, 1], 8.0)
    
    def test_scalar_multiplication_right(self):
        a = Matrix([[1, 2], [3, 4]])
        b = 3 * a
        self.assertEqual(b[0, 0], 3.0)
        self.assertEqual(b[1, 1], 12.0)
    
    def test_matrix_multiplication(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        c = a * b
        self.assertEqual(c[0, 0], 19.0)  # 1*5 + 2*7
        self.assertEqual(c[0, 1], 22.0)  # 1*6 + 2*8
        self.assertEqual(c[1, 0], 43.0)  # 3*5 + 4*7
        self.assertEqual(c[1, 1], 50.0)  # 3*6 + 4*8
    
    def test_matrix_multiplication_non_square(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])  # 2x3
        b = Matrix([[1], [2], [3]])  # 3x1
        c = a * b
        self.assertEqual(c.shape, (2, 1))
        self.assertEqual(c[0, 0], 14.0)  # 1*1 + 2*2 + 3*3
        self.assertEqual(c[1, 0], 32.0)  # 4*1 + 5*2 + 6*3
    
    def test_negation(self):
        a = Matrix([[1, -2], [-3, 4]])
        b = -a
        self.assertEqual(b[0, 0], -1.0)
        self.assertEqual(b[0, 1], 2.0)
        self.assertEqual(b[1, 0], 3.0)
        self.assertEqual(b[1, 1], -4.0)
    
    def test_power_zero(self):
        a = Matrix([[1, 2], [3, 4]])
        b = a ** 0
        self.assertEqual(b, Matrix.identity(2))
    
    def test_power_one(self):
        a = Matrix([[1, 2], [3, 4]])
        b = a ** 1
        self.assertEqual(b, a)
    
    def test_power_two(self):
        a = Matrix([[1, 2], [3, 4]])
        b = a ** 2
        expected = a * a
        self.assertEqual(b, expected)


class TestMatrixProperties(unittest.TestCase):
    """Test matrix properties."""
    
    def test_is_square_true(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertTrue(m.is_square())
    
    def test_is_square_false(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertFalse(m.is_square())
    
    def test_is_symmetric_true(self):
        m = Matrix([[1, 2], [2, 3]])
        self.assertTrue(m.is_symmetric())
    
    def test_is_symmetric_false(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertFalse(m.is_symmetric())
    
    def test_is_diagonal_true(self):
        m = Matrix.diagonal([1, 2, 3])
        self.assertTrue(m.is_diagonal())
    
    def test_is_diagonal_false(self):
        m = Matrix([[1, 1], [0, 1]])
        self.assertFalse(m.is_diagonal())
    
    def test_is_upper_triangular_true(self):
        m = Matrix([[1, 2, 3], [0, 4, 5], [0, 0, 6]])
        self.assertTrue(m.is_upper_triangular())
    
    def test_is_upper_triangular_false(self):
        m = Matrix([[1, 0], [2, 3]])
        self.assertFalse(m.is_upper_triangular())
    
    def test_is_lower_triangular_true(self):
        m = Matrix([[1, 0], [2, 3]])
        self.assertTrue(m.is_lower_triangular())
    
    def test_is_lower_triangular_false(self):
        m = Matrix([[1, 2], [0, 3]])
        self.assertFalse(m.is_lower_triangular())


class TestMatrixOperations(unittest.TestCase):
    """Test matrix operations."""
    
    def test_transpose(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        t = m.transpose()
        self.assertEqual(t.shape, (3, 2))
        self.assertEqual(t[0, 0], 1.0)
        self.assertEqual(t[0, 1], 4.0)
        self.assertEqual(t[1, 0], 2.0)
        self.assertEqual(t[2, 1], 6.0)
    
    def test_trace(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.trace(), 5.0)
    
    def test_trace_non_square_raises(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            m.trace()
    
    def test_determinant_1x1(self):
        m = Matrix([[5]])
        self.assertEqual(m.determinant(), 5.0)
    
    def test_determinant_2x2(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.determinant(), -2.0)
    
    def test_determinant_3x3(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        # det = 1*(5*10-6*8) - 2*(4*10-6*7) + 3*(4*8-5*7)
        # = 1*(50-48) - 2*(40-42) + 3*(32-35)
        # = 2 + 4 - 9 = -3
        self.assertAlmostEqual(m.determinant(), -3.0)
    
    def test_determinant_identity(self):
        m = Matrix.identity(5)
        self.assertEqual(m.determinant(), 1.0)
    
    def test_rank_full(self):
        m = Matrix.identity(3)
        self.assertEqual(m.rank(), 3)
    
    def test_rank_deficient(self):
        m = Matrix([[1, 2], [2, 4]])  # Second row is 2x first row
        self.assertEqual(m.rank(), 1)
    
    def test_rank_non_square(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.rank(), 2)
    
    def test_inverse_2x2(self):
        m = Matrix([[1, 2], [3, 4]])
        inv = m.inverse()
        result = m * inv
        # Should be identity
        for i in range(2):
            for j in range(2):
                expected = 1.0 if i == j else 0.0
                self.assertAlmostEqual(result[i, j], expected, places=10)
    
    def test_inverse_identity(self):
        m = Matrix.identity(4)
        inv = m.inverse()
        self.assertEqual(m, inv)
    
    def test_inverse_singular_raises(self):
        m = Matrix([[1, 2], [2, 4]])  # Singular
        with self.assertRaises(ValueError):
            m.inverse()
    
    def test_solve_simple(self):
        a = Matrix([[2, 1], [1, 3]])
        b = Matrix([[5], [10]])
        x = a.solve(b)
        # Solution should be x=[1, 3]
        self.assertAlmostEqual(x[0, 0], 1.0, places=10)
        self.assertAlmostEqual(x[1, 0], 3.0, places=10)
    
    def test_solve_3x3(self):
        a = Matrix([[1, 1, 1], [0, 2, 5], [2, 5, -1]])
        b = Matrix([[6], [-4], [27]])
        x = a.solve(b)
        # Check: Ax = b
        result = a * x
        for i in range(3):
            self.assertAlmostEqual(result[i, 0], b[i, 0], places=10)
    
    def test_norm_frobenius(self):
        m = Matrix([[1, 2], [3, 4]])
        # sqrt(1+4+9+16) = sqrt(30)
        self.assertAlmostEqual(m.norm(), math.sqrt(30))
    
    def test_norm_1(self):
        m = Matrix([[1, 2], [3, 4]])
        # Max column sum: max(1+3, 2+4) = 6
        self.assertEqual(m.norm(1), 6.0)
    
    def test_norm_inf(self):
        m = Matrix([[1, 2], [3, 4]])
        # Max row sum: max(1+2, 3+4) = 7
        self.assertEqual(m.norm('inf'), 7.0)


class TestMatrixDecomposition(unittest.TestCase):
    """Test matrix decompositions."""
    
    def test_qr_decomposition(self):
        a = Matrix([[1, 2], [3, 4], [5, 6]])
        q, r = a.qr_decompose()
        # Verify: Q * R = A
        qr = q * r
        for i in range(a.rows):
            for j in range(a.cols):
                self.assertAlmostEqual(qr[i, j], a[i, j], places=10)
        
        # Q should have orthonormal columns (Q^T * Q = I for square Q part)
        qtq = q.transpose() * q
        k = qtq.rows
        for i in range(k):
            for j in range(k):
                expected = 1.0 if i == j else 0.0
                self.assertAlmostEqual(qtq[i, j], expected, places=10)
    
    def test_cholesky(self):
        # Create symmetric positive definite matrix
        a = Matrix([[4, 2], [2, 3]])
        l = a.cholesky()
        # L * L^T should equal A
        result = l * l.transpose()
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result[i, j], a[i, j], places=10)
    
    def test_cholesky_not_symmetric_raises(self):
        m = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            m.cholesky()
    
    def test_cholesky_not_positive_definite_raises(self):
        m = Matrix([[1, 2], [2, 1]])  # Not positive definite
        with self.assertRaises(ValueError):
            m.cholesky()


class TestEigenvalues(unittest.TestCase):
    """Test eigenvalue computation."""
    
    def test_eigenvalues_diagonal(self):
        m = Matrix.diagonal([1, 2, 3])
        eigs = m.eigenvalues()
        # Eigenvalues of diagonal matrix are diagonal elements
        eigs_sorted = sorted(eigs)
        expected = [1.0, 2.0, 3.0]
        for e, exp in zip(eigs_sorted, expected):
            self.assertAlmostEqual(e, exp, places=6)
    
    def test_eigenvalues_identity(self):
        m = Matrix.identity(3)
        eigs = m.eigenvalues()
        for e in eigs:
            self.assertAlmostEqual(e, 1.0, places=6)


class TestMatrixUtilities(unittest.TestCase):
    """Test matrix utility methods."""
    
    def test_get_row(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        row = m.get_row(1)
        self.assertEqual(row, [4.0, 5.0, 6.0])
    
    def test_get_col(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        col = m.get_col(1)
        self.assertEqual(col, [2.0, 5.0])
    
    def test_set_row(self):
        m = Matrix([[1, 2], [3, 4]])
        m.set_row(0, [10, 20])
        self.assertEqual(m[0, 0], 10.0)
        self.assertEqual(m[0, 1], 20.0)
    
    def test_set_col(self):
        m = Matrix([[1, 2], [3, 4]])
        m.set_col(0, [10, 30])
        self.assertEqual(m[0, 0], 10.0)
        self.assertEqual(m[1, 0], 30.0)
    
    def test_submatrix(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        sub = m.submatrix(0, 2, 1, 3)
        self.assertEqual(sub.shape, (2, 2))
        self.assertEqual(sub[0, 0], 2.0)
        self.assertEqual(sub[0, 1], 3.0)
        self.assertEqual(sub[1, 0], 5.0)
        self.assertEqual(sub[1, 1], 6.0)
    
    def test_minor(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        minor = m.minor(0, 0)
        self.assertEqual(minor.shape, (2, 2))
        self.assertEqual(minor[0, 0], 5.0)
        self.assertEqual(minor[0, 1], 6.0)
        self.assertEqual(minor[1, 0], 8.0)
        self.assertEqual(minor[1, 1], 9.0)


class TestVectorOperations(unittest.TestCase):
    """Test vector utility functions."""
    
    def test_dot_product(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        self.assertEqual(dot(a, b), 32)  # 1*4 + 2*5 + 3*6
    
    def test_dot_product_different_lengths_raises(self):
        with self.assertRaises(ValueError):
            dot([1, 2], [1, 2, 3])
    
    def test_cross_product(self):
        a = [1, 0, 0]
        b = [0, 1, 0]
        c = cross(a, b)
        self.assertEqual(c, [0.0, 0.0, 1.0])
    
    def test_cross_product_non_3d_raises(self):
        with self.assertRaises(ValueError):
            cross([1, 2], [3, 4])
    
    def test_vector_norm_2(self):
        v = [3, 4]
        self.assertEqual(vector_norm(v), 5.0)
    
    def test_vector_norm_1(self):
        v = [3, -4]
        self.assertEqual(vector_norm(v, 1), 7.0)
    
    def test_vector_norm_inf(self):
        v = [3, -5, 2]
        self.assertEqual(vector_norm(v, 'inf'), 5.0)
    
    def test_normalize(self):
        v = [3, 4]
        n = normalize(v)
        self.assertAlmostEqual(n[0], 0.6)
        self.assertAlmostEqual(n[1], 0.8)
    
    def test_normalize_zero_raises(self):
        with self.assertRaises(ValueError):
            normalize([0, 0])
    
    def test_angle_between(self):
        a = [1, 0, 0]
        b = [0, 1, 0]
        angle = angle_between(a, b)
        self.assertAlmostEqual(angle, math.pi / 2)
    
    def test_angle_between_parallel(self):
        a = [1, 2, 3]
        b = [2, 4, 6]  # Parallel to a
        angle = angle_between(a, b)
        self.assertAlmostEqual(angle, 0.0)
    
    def test_is_orthogonal_true(self):
        a = [1, 0, 0]
        b = [0, 1, 0]
        self.assertTrue(is_orthogonal(a, b))
    
    def test_is_orthogonal_false(self):
        a = [1, 1, 0]
        b = [1, 0, 0]
        self.assertFalse(is_orthogonal(a, b))
    
    def test_gram_schmidt(self):
        vectors = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
        orthonormal = gram_schmidt(vectors)
        # Check all vectors are unit vectors
        for v in orthonormal:
            self.assertAlmostEqual(vector_norm(v), 1.0, places=10)
        # Check all pairs are orthogonal
        for i in range(len(orthonormal)):
            for j in range(i + 1, len(orthonormal)):
                self.assertAlmostEqual(dot(orthonormal[i], orthonormal[j]), 0.0, places=10)


class TestMatrixEquality(unittest.TestCase):
    """Test matrix equality and comparison."""
    
    def test_equality_same(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 4]])
        self.assertEqual(a, b)
    
    def test_equality_different(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 5]])
        self.assertNotEqual(a, b)
    
    def test_equality_different_shape(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertNotEqual(a, b)


if __name__ == '__main__':
    unittest.main()