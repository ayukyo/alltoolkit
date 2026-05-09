"""
AllToolkit - Sparse Matrix Utilities Examples

Demonstrates various use cases for sparse matrix operations.
"""

from mod import (
    COOMatrix, CSRMatrix, CSCMatrix, SparseMatrixUtils,
    from_dense, diagonal, identity
)


def example_basic_usage():
    """Basic usage examples."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Create a COO matrix incrementally
    print("\nCreating a COO matrix (coordinate format):")
    coo = COOMatrix((4, 4))
    coo.add(0, 0, 1.0)
    coo.add(0, 3, 2.0)
    coo.add(1, 1, 3.0)
    coo.add(2, 2, 4.0)
    coo.add(3, 0, 5.0)
    
    print(f"  Shape: {coo.shape}")
    print(f"  Non-zeros: {coo.nnz}")
    print(f"  Density: {SparseMatrixUtils.density(coo):.2%}")
    
    # Convert to CSR for efficient operations
    print("\nConverting to CSR format:")
    csr = coo.to_csr()
    print(f"  {csr}")
    
    # Display as dense matrix
    print("\nDense representation:")
    dense = coo.to_dense()
    for row in dense:
        print(f"  {row}")


def example_from_dense():
    """Creating sparse matrix from dense."""
    print("\n" + "=" * 60)
    print("Example 2: From Dense Matrix")
    print("=" * 60)
    
    # A large-ish matrix with only a few non-zeros
    dense = [
        [10.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 20.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 30.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 40.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 50.0]
    ]
    
    print("\nOriginal dense matrix (5x5):")
    for row in dense:
        print(f"  {row}")
    
    # Convert to sparse
    csr = from_dense(dense, 'csr')
    
    print(f"\nSparse representation:")
    print(f"  Non-zeros: {csr.nnz}")
    print(f"  Memory saved: {(25 - csr.nnz) / 25 * 100:.1f}% fewer stored elements")


def example_matrix_operations():
    """Matrix arithmetic operations."""
    print("\n" + "=" * 60)
    print("Example 3: Matrix Operations")
    print("=" * 60)
    
    # Create two sparse matrices
    A = from_dense([[1, 0, 2], [0, 3, 0], [4, 0, 5]], 'csr')
    B = from_dense([[0, 6, 0], [7, 0, 8], [0, 9, 0]], 'csr')
    
    print("\nMatrix A:")
    for row in A.to_dense():
        print(f"  {row}")
    
    print("\nMatrix B:")
    for row in B.to_dense():
        print(f"  {row}")
    
    # Addition
    print("\nA + B:")
    C = SparseMatrixUtils.add(A, B)
    for row in C.to_dense():
        print(f"  {row}")
    
    # Multiplication
    print("\nA × B:")
    D = SparseMatrixUtils.multiply(A, B)
    for row in D.to_dense():
        print(f"  {row}")
    
    # Scaling
    print("\nA × 2:")
    E = SparseMatrixUtils.scale(A, 2)
    for row in E.to_dense():
        print(f"  {row}")


def example_diagonal_matrices():
    """Diagonal and identity matrices."""
    print("\n" + "=" * 60)
    print("Example 4: Diagonal and Identity Matrices")
    print("=" * 60)
    
    # Create identity matrix
    print("\nIdentity matrix (4x4):")
    I = identity(4, 'csr')
    for row in I.to_dense():
        print(f"  {row}")
    
    # Create diagonal matrix
    print("\nDiagonal matrix with values [1, 2, 3, 4]:")
    D = diagonal([1, 2, 3, 4], 'csr')
    for row in D.to_dense():
        print(f"  {row}")
    
    # Verify multiplication with identity
    print("\nI × D = D:")
    result = SparseMatrixUtils.multiply(I, D)
    assert result.to_dense() == D.to_dense()
    print("  Verified!")


def example_matrix_vector():
    """Matrix-vector multiplication."""
    print("\n" + "=" * 60)
    print("Example 5: Matrix-Vector Multiplication")
    print("=" * 60)
    
    # Sparse matrix
    A = from_dense([
        [1.0, 0.0, 2.0, 0.0],
        [0.0, 3.0, 0.0, 4.0],
        [5.0, 0.0, 6.0, 0.0]
    ], 'csr')
    
    print("\nSparse matrix A (3x4):")
    for row in A.to_dense():
        print(f"  {row}")
    
    print(f"\n  Non-zeros: {A.nnz}")
    print(f"  Density: {SparseMatrixUtils.density(A):.2%}")
    
    # Vector
    x = [1.0, 2.0, 3.0, 4.0]
    print(f"\nVector x: {x}")
    
    # Multiply
    y = A.matvec(x)
    print(f"\nResult y = Ax: {y}")
    
    # Verify manually
    expected = [
        1*1 + 2*3,           # row 0: 1*1 + 0*2 + 2*3 + 0*4 = 7
        3*2 + 4*4,           # row 1: 0*1 + 3*2 + 0*3 + 4*4 = 22
        5*1 + 6*3            # row 2: 5*1 + 0*2 + 6*3 + 0*4 = 23
    ]
    print(f"  Manual verification: {expected}")


def example_laplacian_matrix():
    """Graph Laplacian matrix example."""
    print("\n" + "=" * 60)
    print("Example 6: Graph Laplacian Matrix")
    print("=" * 60)
    
    # Example: 5-node graph Laplacian for a simple path graph
    # 0 -- 1 -- 2 -- 3 -- 4
    # Laplacian L = D - A where D is degree diagonal, A is adjacency
    
    print("\nPath graph: 0 -- 1 -- 2 -- 3 -- 4")
    
    # Adjacency matrix (sparse)
    A = COOMatrix((5, 5))
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    for (i, j) in edges:
        A.add(i, j, 1.0)
        A.add(j, i, 1.0)  # Undirected
    
    print("\nAdjacency matrix A:")
    A_csr = A.to_csr()
    for row in A_csr.to_dense():
        print(f"  {row}")
    
    # Degree matrix (diagonal)
    degrees = [2, 2, 2, 2, 2]  # Actually: 1, 2, 2, 2, 1 for path graph
    # Correct degrees for path graph endpoints:
    degrees = [1, 2, 2, 2, 1]
    D = diagonal(degrees, 'csr')
    
    print("\nDegree matrix D:")
    for row in D.to_dense():
        print(f"  {row}")
    
    # Laplacian L = D - A
    L = SparseMatrixUtils.add(D, SparseMatrixUtils.scale(A_csr, -1))
    
    print("\nLaplacian matrix L = D - A:")
    for row in L.to_dense():
        print(f"  {row}")
    
    # Properties
    print(f"\n  Trace (sum of degrees): {SparseMatrixUtils.trace(L)}")
    print(f"  Frobenius norm: {SparseMatrixUtils.frobenius_norm(L):.2f}")


def example_format_comparison():
    """Compare different storage formats."""
    print("\n" + "=" * 60)
    print("Example 7: Format Comparison")
    print("=" * 60)
    
    # Create a matrix
    dense = [
        [1.0, 0.0, 0.0, 2.0, 0.0],
        [0.0, 3.0, 0.0, 0.0, 4.0],
        [0.0, 0.0, 5.0, 0.0, 0.0],
        [6.0, 0.0, 0.0, 7.0, 0.0],
        [0.0, 8.0, 0.0, 0.0, 9.0]
    ]
    
    coo = from_dense(dense, 'coo')
    csr = from_dense(dense, 'csr')
    csc = from_dense(dense, 'csc')
    
    print("\nMatrix (5x5 with 9 non-zeros):")
    print(f"  COO: stores {coo.nnz} triplets (row, col, value)")
    print(f"  CSR: uses row pointers + {csr.nnz} values")
    print(f"  CSC: uses column pointers + {csc.nnz} values")
    
    print("\nStorage requirements (conceptual):")
    print(f"  COO: 3 × {coo.nnz} = {3 * coo.nnz} storage units")
    print(f"  CSR: {len(csr.indptr)} pointers + 2 × {csr.nnz} = {len(csr.indptr) + 2 * csr.nnz} storage units")
    print(f"  CSC: {len(csc.indptr)} pointers + 2 × {csc.nnz} = {len(csc.indptr) + 2 * csc.nnz} storage units")
    
    print("\nBest use cases:")
    print("  COO: Incremental construction, easy modification")
    print("  CSR: Row slicing, matrix-vector products")
    print("  CSC: Column slicing, transpose operations")


def example_element_wise_ops():
    """Element-wise operations."""
    print("\n" + "=" * 60)
    print("Example 8: Element-wise Operations")
    print("=" * 60)
    
    A = from_dense([[1, 2, 0], [0, 3, 4], [5, 0, 6]], 'csr')
    B = from_dense([[0, 2, 1], [3, 0, 4], [5, 6, 0]], 'csr')
    
    print("\nMatrix A:")
    for row in A.to_dense():
        print(f"  {row}")
    
    print("\nMatrix B:")
    for row in B.to_dense():
        print(f"  {row}")
    
    # Element-wise (Hadamard) product
    print("\nElement-wise product A ⊙ B:")
    C = SparseMatrixUtils.element_wise_multiply(A, B)
    for row in C.to_dense():
        print(f"  {row}")
    
    # Sum
    print(f"\nSum of A: {SparseMatrixUtils.sum(A)}")
    print(f"Sum of B: {SparseMatrixUtils.sum(B)}")
    print(f"Sum of A ⊙ B: {SparseMatrixUtils.sum(C)}")


def example_transpose():
    """Transpose operations."""
    print("\n" + "=" * 60)
    print("Example 9: Transpose Operations")
    print("=" * 60)
    
    # Non-symmetric matrix
    A = from_dense([[1, 2, 3], [0, 4, 0], [5, 0, 6]], 'csr')
    
    print("\nOriginal matrix A (3x3):")
    for row in A.to_dense():
        print(f"  {row}")
    
    # Transpose (returns CSC as transpose of CSR)
    A_T = A.transpose()
    
    print("\nTranspose Aᵀ (as CSC):")
    for row in A_T.to_dense():
        print(f"  {row}")
    
    # Verify A × Aᵀ is symmetric
    print("\nA × Aᵀ (should be symmetric):")
    prod = SparseMatrixUtils.multiply(A, A_T.to_csr())
    for row in prod.to_dense():
        print(f"  {row}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Sparse Matrix Utils - Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_from_dense()
    example_matrix_operations()
    example_diagonal_matrices()
    example_matrix_vector()
    example_laplacian_matrix()
    example_format_comparison()
    example_element_wise_ops()
    example_transpose()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()