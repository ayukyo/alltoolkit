#!/usr/bin/env python3
"""
Matrix Utilities Examples

This file demonstrates various matrix operations including:
- Matrix creation and basic arithmetic
- Determinants and inverses
- Solving linear systems
- Matrix decompositions (QR, Cholesky)
- Eigenvalue computation
"""

from matrix_utils import (
    Matrix, dot, cross, vector_norm, normalize,
    angle_between, is_orthogonal, gram_schmidt
)
import math


def example_matrix_creation():
    """Various ways to create matrices."""
    print("=" * 60)
    print("Matrix Creation Examples")
    print("=" * 60)
    
    # From list
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    print(f"\nFrom list:\n{m1}")
    
    # Zero matrix
    m2 = Matrix.zeros(3, 4)
    print(f"\nZero matrix (3x4):\n{m2}")
    
    # Identity matrix
    m3 = Matrix.identity(4)
    print(f"\nIdentity matrix (4x4):\n{m3}")
    
    # Diagonal matrix
    m4 = Matrix.diagonal([1, 2, 3, 4])
    print(f"\nDiagonal matrix:\n{m4}")
    
    # Random matrix
    m5 = Matrix.random(3, 3, low=-1, high=1)
    print(f"\nRandom matrix (3x3):\n{m5}")
    
    # Hilbert matrix
    m6 = Matrix.hilbert(4)
    print(f"\nHilbert matrix (4x4):\n{m6}")
    
    # Vandermonde matrix
    m7 = Matrix.vandermonde([1, 2, 3, 4])
    print(f"\nVandermonde matrix:\n{m7}")


def example_arithmetic():
    """Matrix arithmetic operations."""
    print("\n" + "=" * 60)
    print("Arithmetic Operations")
    print("=" * 60)
    
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    
    print(f"\nMatrix A:\n{a}")
    print(f"\nMatrix B:\n{b}")
    
    print(f"\nA + B:\n{a + b}")
    print(f"\nA - B:\n{a - b}")
    print(f"\nA * B:\n{a * b}")
    print(f"\nA * 2:\n{a * 2}")
    print(f"\nA^2:\n{a ** 2}")
    
    # Matrix transpose
    print(f"\nA transpose:\n{a.transpose()}")
    
    # Matrix trace
    print(f"\nTrace of A: {a.trace()}")


def example_determinant_inverse():
    """Determinant and inverse operations."""
    print("\n" + "=" * 60)
    print("Determinant and Inverse")
    print("=" * 60)
    
    m = Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
    print(f"\nMatrix M:\n{m}")
    
    det = m.determinant()
    print(f"\nDeterminant of M: {det}")
    
    inv = m.inverse()
    print(f"\nInverse of M:\n{inv}")
    
    # Verify: M * M^-1 = I
    product = m * inv
    print(f"\nM * M^-1 (should be identity):\n{product}")
    
    # Rank
    print(f"\nRank of M: {m.rank()}")


def example_solve_linear_system():
    """Solving linear systems Ax = b."""
    print("\n" + "=" * 60)
    print("Solving Linear Systems")
    print("=" * 60)
    
    # System:
    # 2x + y - z = 8
    # -3x - y + 2z = -11
    # -2x + y + 2z = -3
    
    A = Matrix([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    b = Matrix([[8], [-11], [-3]])
    
    print(f"\nCoefficient matrix A:\n{A}")
    print(f"\nRight-hand side b:\n{b}")
    
    x = A.solve(b)
    print(f"\nSolution x:\n{x}")
    
    # Verify: Ax = b
    result = A * x
    print(f"\nVerification A*x:\n{result}")


def example_decompositions():
    """Matrix decompositions."""
    print("\n" + "=" * 60)
    print("Matrix Decompositions")
    print("=" * 60)
    
    # QR Decomposition
    print("\n--- QR Decomposition ---")
    A = Matrix([[1, 2], [3, 4], [5, 6]])
    print(f"Matrix A (3x2):\n{A}")
    
    Q, R = A.qr_decompose()
    print(f"\nQ (orthogonal):\n{Q}")
    print(f"\nR (upper triangular):\n{R}")
    
    # Verify: Q * R = A
    print(f"\nQ*R (should equal A):\n{Q * R}")
    
    # Cholesky Decomposition
    print("\n--- Cholesky Decomposition ---")
    # Create symmetric positive definite matrix
    M = Matrix([[4, 2, 2], [2, 5, 1], [2, 1, 6]])
    print(f"Symmetric positive definite matrix M:\n{M}")
    
    L = M.cholesky()
    print(f"\nCholesky factor L (lower triangular):\n{L}")
    
    # Verify: L * L^T = M
    print(f"\nL*L^T (should equal M):\n{L * L.transpose()}")


def example_eigenvalues():
    """Eigenvalue computation."""
    print("\n" + "=" * 60)
    print("Eigenvalue Computation")
    print("=" * 60)
    
    # Diagonal matrix (eigenvalues are diagonal elements)
    D = Matrix.diagonal([1, 2, 3])
    print(f"\nDiagonal matrix:\n{D}")
    eigs = D.eigenvalues()
    print(f"Eigenvalues: {sorted([round(e, 6) for e in eigs])}")
    
    # Another example
    M = Matrix([[2, 1], [1, 2]])
    print(f"\nMatrix M:\n{M}")
    eigs = M.eigenvalues()
    print(f"Eigenvalues: {[round(e, 6) for e in sorted(eigs)]}")


def example_properties():
    """Matrix properties."""
    print("\n" + "=" * 60)
    print("Matrix Properties")
    print("=" * 60)
    
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"Matrix:\n{m}")
    print(f"Shape: {m.shape}")
    print(f"Is square: {m.is_square()}")
    print(f"Is symmetric: {m.is_symmetric()}")
    print(f"Is diagonal: {m.is_diagonal()}")
    print(f"Is upper triangular: {m.is_upper_triangular()}")
    print(f"Is lower triangular: {m.is_lower_triangular()}")
    
    sym = Matrix([[1, 2], [2, 3]])
    print(f"\nSymmetric matrix:\n{sym}")
    print(f"Is symmetric: {sym.is_symmetric()}")
    
    upper = Matrix([[1, 2, 3], [0, 4, 5], [0, 0, 6]])
    print(f"\nUpper triangular matrix:\n{upper}")
    print(f"Is upper triangular: {upper.is_upper_triangular()}")


def example_norms():
    """Matrix norms."""
    print("\n" + "=" * 60)
    print("Matrix Norms")
    print("=" * 60)
    
    m = Matrix([[1, 2], [3, 4]])
    print(f"Matrix:\n{m}")
    print(f"Frobenius norm: {m.norm():.6f}")
    print(f"1-norm (max column sum): {m.norm(1):.6f}")
    print(f"Inf-norm (max row sum): {m.norm('inf'):.6f}")


def example_vector_operations():
    """Vector operations."""
    print("\n" + "=" * 60)
    print("Vector Operations")
    print("=" * 60)
    
    # Dot product
    a = [1, 2, 3]
    b = [4, 5, 6]
    print(f"Dot product of {a} and {b}: {dot(a, b)}")
    
    # Cross product
    u = [1, 0, 0]
    v = [0, 1, 0]
    print(f"\nCross product of {u} and {v}: {cross(u, v)}")
    
    # Vector norms
    w = [3, 4]
    print(f"\nVector {w}:")
    print(f"  2-norm: {vector_norm(w)}")
    print(f"  1-norm: {vector_norm(w, 1)}")
    print(f"  Inf-norm: {vector_norm(w, 'inf')}")
    
    # Normalize
    print(f"  Normalized: {normalize(w)}")
    
    # Angle between vectors
    x = [1, 0, 0]
    y = [0, 1, 0]
    angle = angle_between(x, y)
    print(f"\nAngle between {x} and {y}: {math.degrees(angle):.2f} degrees")
    
    # Orthogonality
    print(f"Are they orthogonal? {is_orthogonal(x, y)}")
    
    # Gram-Schmidt
    print("\n--- Gram-Schmidt Orthonormalization ---")
    vectors = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    print(f"Original vectors: {vectors}")
    orthonormal = gram_schmidt(vectors)
    print(f"Orthonormal basis:")
    for i, v in enumerate(orthonormal):
        print(f"  v{i+1} = {[round(x, 6) for x in v]}")


def example_matrix_slices():
    """Matrix slicing and submatrices."""
    print("\n" + "=" * 60)
    print("Matrix Slicing and Submatrices")
    print("=" * 60)
    
    m = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(f"Original matrix:\n{m}")
    
    # Get row and column
    print(f"\nRow 1: {m.get_row(1)}")
    print(f"Column 2: {m.get_col(2)}")
    
    # Submatrix
    sub = m.submatrix(0, 2, 1, 3)
    print(f"\nSubmatrix (rows 0-2, cols 1-3):\n{sub}")
    
    # Minor
    square = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\nSquare matrix:\n{square}")
    minor = square.minor(1, 1)
    print(f"Minor after removing row 1, col 1:\n{minor}")


def example_practical_applications():
    """Practical applications."""
    print("\n" + "=" * 60)
    print("Practical Applications")
    print("=" * 60)
    
    # Example 1: Linear regression (least squares)
    print("\n--- Linear Regression (Least Squares) ---")
    # Fit line y = mx + b to points (0, 1), (1, 2), (2, 3), (3, 5)
    # This is an overdetermined system: Ax = y
    # Solution: x = (A^T A)^{-1} A^T y
    
    points = [(0, 1), (1, 2), (2, 3), (3, 5)]
    A = Matrix([[1, x] for x, _ in points])
    y = Matrix([[py] for _, py in points])
    
    print(f"Points: {points}")
    print(f"Design matrix A:\n{A}")
    
    # (A^T A)
    AtA = A.transpose() * A
    # (A^T A)^{-1}
    AtA_inv = AtA.inverse()
    # A^T y
    Aty = A.transpose() * y
    # Solution
    x = AtA_inv * Aty
    
    print(f"\nFitted line: y = {x[1,0]:.4f}x + {x[0,0]:.4f}")
    
    # Example 2: Rotation matrix
    print("\n--- Rotation Matrix ---")
    angle = math.pi / 4  # 45 degrees
    R = Matrix([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    print(f"Rotation matrix (45 degrees):\n{R}")
    
    point = Matrix([[1], [0]])
    rotated = R * point
    print(f"\nOriginal point (1, 0)")
    print(f"Rotated point: ({rotated[0,0]:.4f}, {rotated[1,0]:.4f})")
    
    # Example 3: Markov chain steady state
    print("\n--- Markov Chain Steady State ---")
    # Transition matrix
    P = Matrix([
        [0.7, 0.2, 0.1],
        [0.1, 0.8, 0.1],
        [0.1, 0.2, 0.7]
    ])
    print(f"Transition matrix P:\n{P}")
    
    # Find eigenvalue = 1
    eigs = P.eigenvalues()
    print(f"Eigenvalues: {[round(e, 6) for e in eigs]}")
    print("(One eigenvalue should be close to 1 for Markov chain)")


if __name__ == "__main__":
    example_matrix_creation()
    example_arithmetic()
    example_determinant_inverse()
    example_solve_linear_system()
    example_decompositions()
    example_eigenvalues()
    example_properties()
    example_norms()
    example_vector_operations()
    example_matrix_slices()
    example_practical_applications()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)