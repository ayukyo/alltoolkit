"""
AllToolkit - Sparse Matrix Utilities Tests

Comprehensive test suite for sparse matrix operations.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    COOMatrix, CSRMatrix, CSCMatrix, SparseMatrixUtils,
    coo_matrix, csr_matrix, csc_matrix, from_dense, from_dict,
    diagonal, identity, zeros
)


def test_coo_basic():
    """Test basic COO matrix operations."""
    print("Testing COO basic operations...")
    
    # Create matrix
    coo = COOMatrix((3, 3))
    assert coo.shape == (3, 3)
    assert coo.nnz == 0
    
    # Add elements
    coo.add(0, 0, 1.0)
    coo.add(1, 1, 2.0)
    coo.add(2, 2, 3.0)
    assert coo.nnz == 3
    
    # Get elements
    assert coo.get(0, 0) == 1.0
    assert coo.get(1, 1) == 2.0
    assert coo.get(0, 1) == 0.0  # Not stored
    
    # Set element
    coo.set(0, 1, 4.0)
    assert coo.get(0, 1) == 4.0
    
    # Set to zero removes element
    coo.set(0, 1, 0.0)
    assert coo.get(0, 1) == 0.0
    assert coo.nnz == 3  # Still 3, zero not stored
    
    # Adding zero does nothing
    coo.add(2, 0, 0.0)
    assert coo.nnz == 3
    
    print("  ✓ COO basic operations passed")


def test_coo_to_dense():
    """Test COO to dense conversion."""
    print("Testing COO to dense conversion...")
    
    coo = COOMatrix((2, 3))
    coo.add(0, 0, 1.0)
    coo.add(0, 2, 2.0)
    coo.add(1, 1, 3.0)
    
    dense = coo.to_dense()
    expected = [
        [1.0, 0.0, 2.0],
        [0.0, 3.0, 0.0]
    ]
    assert dense == expected, f"Expected {expected}, got {dense}"
    
    print("  ✓ COO to dense conversion passed")


def test_coo_transpose():
    """Test COO transpose."""
    print("Testing COO transpose...")
    
    coo = COOMatrix((2, 3))
    coo.add(0, 1, 5.0)
    coo.add(1, 2, 7.0)
    
    transposed = coo.transpose()
    assert transposed.shape == (3, 2)
    assert transposed.get(1, 0) == 5.0
    assert transposed.get(2, 1) == 7.0
    
    print("  ✓ COO transpose passed")


def test_csr_basic():
    """Test basic CSR matrix operations."""
    print("Testing CSR basic operations...")
    
    # Create from COO
    coo = COOMatrix((3, 3))
    coo.add(0, 0, 1.0)
    coo.add(0, 2, 2.0)
    coo.add(1, 1, 3.0)
    coo.add(2, 0, 4.0)
    
    csr = CSRMatrix.from_coo(coo)
    assert csr.shape == (3, 3)
    assert csr.nnz == 4
    
    # Get elements
    assert csr.get(0, 0) == 1.0
    assert csr.get(0, 2) == 2.0
    assert csr.get(1, 1) == 3.0
    assert csr.get(2, 0) == 4.0
    assert csr.get(0, 1) == 0.0
    
    # Row iteration
    row0 = list(csr.get_row(0))
    assert row0 == [(0, 1.0), (2, 2.0)]
    
    print("  ✓ CSR basic operations passed")


def test_csr_from_dense():
    """Test CSR from dense matrix."""
    print("Testing CSR from dense...")
    
    dense = [
        [1.0, 0.0, 2.0],
        [0.0, 0.0, 3.0],
        [4.0, 0.0, 0.0]
    ]
    
    csr = CSRMatrix.from_dense(dense)
    assert csr.shape == (3, 3)
    assert csr.nnz == 4
    
    # Verify conversion back
    result = csr.to_dense()
    assert result == dense
    
    print("  ✓ CSR from dense passed")


def test_csr_matvec():
    """Test CSR matrix-vector multiplication."""
    print("Testing CSR matrix-vector multiplication...")
    
    dense = [
        [1.0, 0.0, 2.0],
        [0.0, 3.0, 0.0],
        [4.0, 0.0, 5.0]
    ]
    
    csr = CSRMatrix.from_dense(dense)
    vector = [1.0, 2.0, 3.0]
    
    result = csr.matvec(vector)
    expected = [7.0, 6.0, 19.0]  # [1*1 + 2*3, 3*2, 4*1 + 5*3]
    assert result == expected, f"Expected {expected}, got {result}"
    
    print("  ✓ CSR matrix-vector multiplication passed")


def test_csc_basic():
    """Test basic CSC matrix operations."""
    print("Testing CSC basic operations...")
    
    coo = COOMatrix((3, 3))
    coo.add(0, 0, 1.0)
    coo.add(0, 2, 2.0)
    coo.add(1, 1, 3.0)
    coo.add(2, 0, 4.0)
    
    csc = CSCMatrix.from_coo(coo)
    assert csc.shape == (3, 3)
    assert csc.nnz == 4
    
    # Get elements
    assert csc.get(0, 0) == 1.0
    assert csc.get(0, 2) == 2.0
    assert csc.get(1, 1) == 3.0
    assert csc.get(2, 0) == 4.0
    
    # Column iteration
    col0 = list(csc.get_col(0))
    assert col0 == [(0, 1.0), (2, 4.0)]
    
    print("  ✓ CSC basic operations passed")


def test_csc_from_dense():
    """Test CSC from dense matrix."""
    print("Testing CSC from dense...")
    
    dense = [
        [1.0, 0.0, 2.0],
        [0.0, 0.0, 3.0],
        [4.0, 0.0, 0.0]
    ]
    
    csc = CSCMatrix.from_dense(dense)
    assert csc.shape == (3, 3)
    assert csc.nnz == 4
    
    # Verify conversion back
    result = csc.to_dense()
    assert result == dense
    
    print("  ✓ CSC from dense passed")


def test_format_conversions():
    """Test conversions between formats."""
    print("Testing format conversions...")
    
    dense = [
        [1.0, 0.0, 2.0],
        [0.0, 3.0, 0.0],
        [4.0, 0.0, 5.0]
    ]
    
    # Dense -> COO -> CSR -> Dense
    coo = COOMatrix((3, 3))
    for i, row in enumerate(dense):
        for j, val in enumerate(row):
            if val != 0:
                coo.add(i, j, val)
    
    csr = coo.to_csr()
    csc = coo.to_csc()
    
    # CSR -> COO
    coo_from_csr = csr.to_coo()
    assert coo_from_csr.to_dense() == dense
    
    # CSC -> COO
    coo_from_csc = csc.to_coo()
    assert coo_from_csc.to_dense() == dense
    
    # CSR -> CSC
    csc_from_csr = csr.to_csc()
    assert csc_from_csr.to_dense() == dense
    
    # CSC -> CSR
    csr_from_csc = csc.to_csr()
    assert csr_from_csc.to_dense() == dense
    
    print("  ✓ Format conversions passed")


def test_sparse_matrix_utils():
    """Test SparseMatrixUtils convenience functions."""
    print("Testing SparseMatrixUtils functions...")
    
    # from_dense
    dense = [[1, 0, 2], [0, 0, 3]]
    csr = SparseMatrixUtils.from_dense(dense, 'csr')
    assert csr.nnz == 3
    
    # from_dict
    data = {(0, 0): 1, (1, 1): 2}
    csr = SparseMatrixUtils.from_dict(data, (2, 2), 'csr')
    assert csr.get(0, 0) == 1.0
    assert csr.get(1, 1) == 2.0
    
    # diagonal
    diag = SparseMatrixUtils.diagonal([1, 2, 3], 'csr')
    assert diag.get(0, 0) == 1.0
    assert diag.get(1, 1) == 2.0
    assert diag.get(2, 2) == 3.0
    assert diag.get(0, 1) == 0.0
    
    # identity
    I = SparseMatrixUtils.identity(3, 'csr')
    assert I.nnz == 3
    for i in range(3):
        assert I.get(i, i) == 1.0
    
    # zeros
    Z = SparseMatrixUtils.zeros((3, 3), 'csr')
    assert Z.nnz == 0
    
    print("  ✓ SparseMatrixUtils functions passed")


def test_matrix_addition():
    """Test sparse matrix addition."""
    print("Testing matrix addition...")
    
    A = SparseMatrixUtils.from_dense([[1, 0], [0, 2]], 'csr')
    B = SparseMatrixUtils.from_dense([[0, 3], [4, 0]], 'csr')
    
    C = SparseMatrixUtils.add(A, B)
    expected = [[1.0, 3.0], [4.0, 2.0]]
    assert C.to_dense() == expected
    
    print("  ✓ Matrix addition passed")


def test_matrix_multiplication():
    """Test sparse matrix multiplication."""
    print("Testing matrix multiplication...")
    
    A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
    B = SparseMatrixUtils.from_dense([[5, 6], [7, 8]], 'csr')
    
    C = SparseMatrixUtils.multiply(A, B)
    expected = [[19.0, 22.0], [43.0, 50.0]]
    result = C.to_dense()
    
    # Check with floating point tolerance
    for i in range(2):
        for j in range(2):
            assert abs(result[i][j] - expected[i][j]) < 1e-10
    
    print("  ✓ Matrix multiplication passed")


def test_matrix_scale():
    """Test sparse matrix scaling."""
    print("Testing matrix scaling...")
    
    A = SparseMatrixUtils.from_dense([[1, 0], [0, 2]], 'csr')
    B = SparseMatrixUtils.scale(A, 3)
    expected = [[3.0, 0.0], [0.0, 6.0]]
    assert B.to_dense() == expected
    
    print("  ✓ Matrix scaling passed")


def test_element_wise_multiply():
    """Test element-wise multiplication."""
    print("Testing element-wise multiplication...")
    
    A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
    B = SparseMatrixUtils.from_dense([[5, 0], [0, 6]], 'csr')
    
    C = SparseMatrixUtils.element_wise_multiply(A, B)
    expected = [[5.0, 0.0], [0.0, 24.0]]
    assert C.to_dense() == expected
    
    print("  ✓ Element-wise multiplication passed")


def test_sum_and_trace():
    """Test sum and trace operations."""
    print("Testing sum and trace...")
    
    A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
    
    # Sum
    total = SparseMatrixUtils.sum(A)
    assert total == 10.0
    
    # Trace
    trace = SparseMatrixUtils.trace(A)
    assert trace == 5.0
    
    print("  ✓ Sum and trace passed")


def test_norms_and_density():
    """Test Frobenius norm and density calculations."""
    print("Testing norms and density...")
    
    A = SparseMatrixUtils.from_dense([[3, 4]], 'csr')
    
    # Frobenius norm: sqrt(9 + 16) = 5
    norm = SparseMatrixUtils.frobenius_norm(A)
    assert abs(norm - 5.0) < 1e-10
    
    # Density: 2 non-zeros out of 2 elements = 1.0
    density = SparseMatrixUtils.density(A)
    assert abs(density - 1.0) < 1e-10
    
    # Sparse matrix
    B = SparseMatrixUtils.from_dense([[1, 0], [0, 0]], 'csr')
    density = SparseMatrixUtils.density(B)
    assert abs(density - 0.25) < 1e-10
    
    sparsity = SparseMatrixUtils.sparsity(B)
    assert abs(sparsity - 0.75) < 1e-10
    
    print("  ✓ Norms and density passed")


def test_convenience_functions():
    """Test module-level convenience functions."""
    print("Testing convenience functions...")
    
    # coo_matrix
    coo = coo_matrix((3, 3))
    assert coo.shape == (3, 3)
    
    # csr_matrix
    csr = csr_matrix((3, 3))
    assert csr.shape == (3, 3)
    
    # csc_matrix
    csc = csc_matrix((3, 3))
    assert csc.shape == (3, 3)
    
    # from_dense
    m = from_dense([[1, 0], [0, 1]], 'csr')
    assert m.nnz == 2
    
    # from_dict
    m = from_dict({(0, 0): 5}, (2, 2), 'csr')
    assert m.get(0, 0) == 5.0
    
    # diagonal
    m = diagonal([1, 2, 3], 'csr')
    assert m.nnz == 3
    
    # identity
    m = identity(3, 'csr')
    assert m.nnz == 3
    
    # zeros
    m = zeros((3, 3), 'csr')
    assert m.nnz == 0
    
    print("  ✓ Convenience functions passed")


def test_large_sparse_matrix():
    """Test with a larger sparse matrix."""
    print("Testing large sparse matrix...")
    
    # Create a 1000x1000 sparse matrix with 1% density
    import random
    random.seed(42)
    
    n = 1000
    coo = COOMatrix((n, n))
    
    for _ in range(10000):  # ~1% density
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        val = random.uniform(1, 10)
        coo.add(i, j, val)
    
    # Convert to CSR
    csr = coo.to_csr()
    assert csr.nnz > 0
    
    # Test matrix-vector multiplication
    vector = [1.0] * n
    result = csr.matvec(vector)
    assert len(result) == n
    
    # Test conversion back to dense (just check it doesn't crash)
    # Don't actually convert the whole thing - too large
    assert csr.to_coo().nnz == csr.nnz
    
    print("  ✓ Large sparse matrix passed")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    # Empty matrix (all zeros)
    coo = COOMatrix((3, 3))
    csr = coo.to_csr()
    assert csr.nnz == 0
    assert csr.to_dense() == [[0.0]*3 for _ in range(3)]
    
    # Single element
    coo = COOMatrix((1, 1))
    coo.add(0, 0, 5.0)
    csr = coo.to_csr()
    assert csr.get(0, 0) == 5.0
    
    # Single row
    coo = COOMatrix((1, 5))
    coo.add(0, 2, 1.0)
    csr = coo.to_csr()
    row = list(csr.get_row(0))
    assert row == [(2, 1.0)]
    
    # Single column
    coo = COOMatrix((5, 1))
    coo.add(2, 0, 1.0)
    csc = coo.to_csc()
    col = list(csc.get_col(0))
    assert col == [(2, 1.0)]
    
    # Error: invalid dimensions
    try:
        COOMatrix((0, 5))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Error: out of bounds
    coo = COOMatrix((3, 3))
    try:
        coo.add(5, 0, 1.0)
        assert False, "Should have raised IndexError"
    except IndexError:
        pass
    
    # Error: shape mismatch in add
    A = SparseMatrixUtils.from_dense([[1]], 'csr')
    B = SparseMatrixUtils.from_dense([[1, 2]], 'csr')
    try:
        SparseMatrixUtils.add(A, B)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Error: incompatible dimensions in multiply
    A = SparseMatrixUtils.from_dense([[1, 2]], 'csr')  # 1x2
    B = SparseMatrixUtils.from_dense([[1], [2], [3]], 'csr')  # 3x1
    try:
        SparseMatrixUtils.multiply(A, B)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Error: trace of non-square
    A = SparseMatrixUtils.from_dense([[1, 2, 3]], 'csr')
    try:
        SparseMatrixUtils.trace(A)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ Edge cases passed")


def test_negative_values():
    """Test matrices with negative values."""
    print("Testing negative values...")
    
    dense = [
        [1.0, -2.0, 0.0],
        [0.0, 3.0, -4.0],
        [-5.0, 0.0, 6.0]
    ]
    
    csr = CSRMatrix.from_dense(dense)
    
    # Verify all values
    assert csr.get(0, 0) == 1.0
    assert csr.get(0, 1) == -2.0
    assert csr.get(1, 2) == -4.0
    assert csr.get(2, 0) == -5.0
    
    # Test operations
    scaled = SparseMatrixUtils.scale(csr, -1)
    assert scaled.get(0, 0) == -1.0
    assert scaled.get(0, 1) == 2.0
    
    print("  ✓ Negative values passed")


def test_copy_and_equality():
    """Test copy and equality operations."""
    print("Testing copy and equality...")
    
    coo1 = COOMatrix((2, 2))
    coo1.add(0, 0, 1.0)
    coo1.add(1, 1, 2.0)
    
    coo2 = coo1.copy()
    assert coo1 == coo2
    
    # Modify copy doesn't affect original
    coo2.add(0, 1, 3.0)
    assert coo1 != coo2
    assert coo1.nnz == 2
    assert coo2.nnz == 3
    
    print("  ✓ Copy and equality passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Sparse Matrix Utils Test Suite")
    print("=" * 50 + "\n")
    
    test_coo_basic()
    test_coo_to_dense()
    test_coo_transpose()
    test_csr_basic()
    test_csr_from_dense()
    test_csr_matvec()
    test_csc_basic()
    test_csc_from_dense()
    test_format_conversions()
    test_sparse_matrix_utils()
    test_matrix_addition()
    test_matrix_multiplication()
    test_matrix_scale()
    test_element_wise_multiply()
    test_sum_and_trace()
    test_norms_and_density()
    test_convenience_functions()
    test_large_sparse_matrix()
    test_edge_cases()
    test_negative_values()
    test_copy_and_equality()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()