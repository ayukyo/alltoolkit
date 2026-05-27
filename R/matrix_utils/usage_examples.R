#!/usr/bin/env Rscript
# matrix_utils/usage_examples.R - Usage Examples for Matrix Utilities Module
#
# Demonstrates various matrix operations and decompositions.
#
# Author: AllToolkit
# Version: 1.0.0

# ============================================================================
# Setup
# ============================================================================

# Get script directory and source the module
script_dir <- dirname(sys.frame(1)$ofile)
if (is.null(script_dir) || script_dir == "") {
  script_dir <- getwd()
}
source(file.path(script_dir, "mod.R"))

cat("\n========================================\n")
cat("Matrix Utils - Usage Examples\n")
cat("========================================\n\n")

# ============================================================================
# Example 1: Matrix Creation
# ============================================================================

cat("=== Example 1: Matrix Creation ===\n\n")

# Create matrices from vectors
cat("Create matrix from vector:\n")
m <- matrix_create(1:9, nrow = 3, ncol = 3)
print(m)

cat("\nCreate matrix by row:\n")
m <- matrix_create(1:6, nrow = 2, byrow = TRUE)
print(m)

# Create special matrices
cat("\nIdentity matrix (3x3):\n")
print(matrix_identity(3))

cat("\nZero matrix (2x4):\n")
print(matrix_zeros(2, 4))

cat("\nDiagonal matrix:\n")
print(matrix_diagonal(c(1, 2, 3, 4)))

# ============================================================================
# Example 2: Basic Operations
# ============================================================================

cat("\n=== Example 2: Basic Operations ===\n\n")

a <- matrix_create(c(1, 2, 3, 4), 2, 2)
b <- matrix_create(c(5, 6, 7, 8), 2, 2)

cat("Matrix A:\n")
print(a)

cat("\nMatrix B:\n")
print(b)

cat("\nA + B:\n")
print(matrix_add(a, b))

cat("\nA - B:\n")
print(matrix_subtract(a, b))

cat("\nA * B (element-wise):\n")
print(matrix_multiply_elementwise(a, b))

cat("\nA @ B (matrix multiplication):\n")
print(matrix_multiply(a, b))

cat("\nScale A by 3:\n")
print(matrix_scale(a, 3))

# ============================================================================
# Example 3: Matrix Properties
# ============================================================================

cat("\n=== Example 3: Matrix Properties ===\n\n")

m <- matrix_create(c(1, 4, 2, 3), 2, 2)
cat("Matrix:\n")
print(m)

cat("\nTranspose:\n")
print(matrix_transpose(m))

cat("\nTrace:", matrix_trace(m), "\n")
cat("Determinant:", matrix_determinant(m), "\n")
cat("Rank:", matrix_rank(m), "\n")
cat("Condition number:", matrix_condition_number(m), "\n")

cat("\nFrobenius norm:", matrix_norm(m, "fro"), "\n")
cat("1-norm:", matrix_norm(m, "1"), "\n")
cat("Infinity norm:", matrix_norm(m, "inf"), "\n")

# ============================================================================
# Example 4: Matrix Inversion
# ============================================================================

cat("\n=== Example 4: Matrix Inversion ===\n\n")

m <- matrix_create(c(4, 7, 2, 6), 2, 2)
cat("Original matrix:\n")
print(m)

cat("\nInverse:\n")
inv <- matrix_inverse(m)
print(inv)

cat("\nVerify: A * A^-1 ≈ I:\n")
print(matrix_multiply(m, inv))

# ============================================================================
# Example 5: Solving Linear Systems
# ============================================================================

cat("\n=== Example 5: Solving Linear Systems ===\n\n")

# System: 3x + 2y = 9, 1x + 1y = 4
a <- matrix_create(c(3, 1, 2, 1), 2, 2)
b <- c(9, 4)

cat("Coefficient matrix A:\n")
print(a)

cat("\nRight-hand side b:", b, "\n")

cat("\nSolution x:\n")
x <- matrix_solve(a, b)
print(x)

cat("\nVerify: A * x = b\n")
print(as.vector(matrix_multiply(a, matrix(x, ncol = 1))))

# ============================================================================
# Example 6: Matrix Decompositions
# ============================================================================

cat("\n=== Example 6: Matrix Decompositions ===\n\n")

# LU Decomposition
cat("LU Decomposition:\n")
m <- matrix_create(c(2, 1, 1, 2, 1, 1, 4, -1, 1), 3, 3)
cat("Original:\n")
print(m)

lu <- matrix_lu(m)
cat("\nL (lower triangular):\n")
print(lu$L)

cat("\nU (upper triangular):\n")
print(lu$U)

cat("\nP (permutation):\n")
print(lu$P)

# QR Decomposition
cat("\n\nQR Decomposition:\n")
m <- matrix_create(c(12, 6, -4, -51, 167, 24, 4, -68, -41), 3, 3)
qr_result <- matrix_qr(m)

cat("Q (orthogonal):\n")
print(qr_result$Q)

cat("\nR (upper triangular):\n")
print(qr_result$R)

cat("\nIs Q orthogonal:", is_orthogonal(qr_result$Q), "\n")

# Eigenvalue Decomposition
cat("\n\nEigenvalue Decomposition:\n")
m <- matrix_symmetric(3)
cat("Symmetric matrix:\n")
print(m)

eigen_result <- matrix_eigen(m)
cat("\nEigenvalues:\n")
print(eigen_result$values)

cat("\nEigenvectors:\n")
print(eigen_result$vectors)

# SVD
cat("\n\nSingular Value Decomposition:\n")
m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
cat("Original (2x3):\n")
print(m)

svd_result <- matrix_svd(m)
cat("\nU:\n")
print(svd_result$U)

cat("\nSingular values:", svd_result$S, "\n")

cat("\nV:\n")
print(svd_result$V)

# ============================================================================
# Example 7: Cholesky Decomposition
# ============================================================================

cat("\n=== Example 7: Cholesky Decomposition ===\n\n")

# Create a positive definite matrix
m <- matrix_positive_definite(3)
cat("Positive definite matrix:\n")
print(m)

cat("\nIs positive definite:", is_positive_definite(m), "\n")

L <- matrix_cholesky(m)
cat("\nCholesky factor L:\n")
print(L)

cat("\nVerify: L * L^T = original\n")
print(matrix_multiply(L, matrix_transpose(L)))

# ============================================================================
# Example 8: Special Matrices
# ============================================================================

cat("\n=== Example 8: Special Matrices ===\n\n")

cat("Hilbert matrix (4x4):\n")
print(matrix_hilbert(4))

cat("\nVandermonde matrix from x = [1, 2, 3, 4]:\n")
print(matrix_vandermonde(c(1, 2, 3, 4)))

cat("\nTridiagonal matrix (5x5):\n")
print(matrix_tridiagonal(5, 2, -1))

# ============================================================================
# Example 9: Matrix Properties Check
# ============================================================================

cat("\n=== Example 9: Matrix Properties Check ===\n\n")

matrices <- list(
  identity = matrix_identity(3),
  diagonal = matrix_diagonal(c(1, 2, 3)),
  symmetric = matrix_symmetric(3),
  pd = matrix_positive_definite(3),
  random = matrix_random(3, 3)
)

for (name in names(matrices)) {
  cat(name, "matrix:\n")
  m <- matrices[[name]]
  cat("  Symmetric:", is_symmetric(m), "\n")
  cat("  Diagonal:", is_diagonal(m), "\n")
  cat("  Identity:", is_identity(m), "\n")
  cat("  Orthogonal:", is_orthogonal(m), "\n")
  cat("  Positive definite:", is_positive_definite(m), "\n")
  cat("  Rank:", matrix_rank(m), "\n")
  cat("\n")
}

# ============================================================================
# Example 10: Matrix Power
# ============================================================================

cat("\n=== Example 10: Matrix Power ===\n\n")

m <- matrix_create(c(1, 0, 1, 1), 2, 2)
cat("Original matrix:\n")
print(m)

cat("\nPower 0 (identity):\n")
print(matrix_power(m, 0))

cat("\nPower 1:\n")
print(matrix_power(m, 1))

cat("\nPower 2:\n")
print(matrix_power(m, 2))

cat("\nPower 5:\n")
print(matrix_power(m, 5))

# ============================================================================
# Example 11: Matrix Summary
# ============================================================================

cat("\n=== Example 11: Matrix Summary ===\n\n")

m <- matrix_random(4, 4)
cat("Random matrix:\n")
print(m)

cat("\nMatrix summary:\n")
info <- matrix_summary(m)
for (key in names(info)) {
  cat("  ", key, ": ", info[[key]], "\n", sep = "")
}

# ============================================================================
# Example 12: Pseudo-Inverse for Rectangular Matrices
# ============================================================================

cat("\n=== Example 12: Pseudo-Inverse ===\n\n")

m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
cat("Rectangular matrix (2x3):\n")
print(m)

pinv <- matrix_pseudo_inverse(m)
cat("\nPseudo-inverse (3x2):\n")
print(pinv)

cat("\nVerify: A * A+ * A ≈ A\n")
result <- matrix_multiply(matrix_multiply(m, pinv), m)
print(result)

# ============================================================================
# Example 13: Matrix Row/Column Operations
# ============================================================================

cat("\n=== Example 13: Row/Column Operations ===\n\n")

m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
cat("Original matrix:\n")
print(m)

cat("\nGet row 1:", matrix_get_row(m, 1), "\n")
cat("Get row 2:", matrix_get_row(m, 2), "\n")
cat("Get column 2:", matrix_get_column(m, 2), "\n")

cat("\nSwap rows 1 and 2:\n")
print(matrix_swap_rows(m, 1, 2))

cat("\nSwap columns 1 and 3:\n")
print(matrix_swap_columns(m, 1, 3))

# ============================================================================
# Summary
# ============================================================================

cat("\n========================================\n")
cat("All examples completed successfully!\n")
cat("========================================\n")