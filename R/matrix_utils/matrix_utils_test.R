#!/usr/bin/env Rscript
# matrix_utils/matrix_utils_test.R - Test Suite for Matrix Utilities Module
#
# Comprehensive tests for matrix operations, decompositions, and properties.
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

# Test counters
tests_passed <- 0
tests_failed <- 0
test_results <- list()

# ============================================================================
# Test Helper Functions
# ============================================================================

test_that <- function(description, expr) {
  result <- tryCatch({
    expr
    TRUE
  }, error = function(e) {
    cat("ERROR in", description, ":", e$message, "\n")
    FALSE
  })
  
  if (isTRUE(result)) {
    tests_passed <<- tests_passed + 1
    test_results[[length(test_results) + 1]] <<- list(desc = description, pass = TRUE)
    cat("✓", description, "\n")
  } else {
    tests_failed <<- tests_failed + 1
    test_results[[length(test_results) + 1]] <<- list(desc = description, pass = FALSE)
    cat("✗", description, "\n")
  }
}

approx_equal <- function(a, b, tol = 1e-8) {
  if (length(a) != length(b)) return(FALSE)
  all(abs(a - b) < tol)
}

matrix_approx_equal <- function(a, b, tol = 1e-8) {
  if (!all(dim(a) == dim(b))) return(FALSE)
  max(abs(a - b)) < tol
}

# ============================================================================
# Matrix Creation Tests
# ============================================================================

cat("\n=== Matrix Creation Tests ===\n")

test_that("matrix_create creates correct matrix", {
  m <- matrix_create(1:6, nrow = 2, ncol = 3)
  stopifnot(all(dim(m) == c(2, 3)))
  stopifnot(m[1, 1] == 1)
  stopifnot(m[2, 3] == 6)
})

test_that("matrix_create with byrow works correctly", {
  m <- matrix_create(1:6, nrow = 2, byrow = TRUE)
  stopifnot(m[1, 1] == 1)
  stopifnot(m[1, 2] == 2)
})

test_that("matrix_identity creates identity matrix", {
  m <- matrix_identity(3)
  stopifnot(all(dim(m) == c(3, 3)))
  stopifnot(matrix_approx_equal(m, diag(3)))
  stopifnot(sum(diag(m)) == 3)
})

test_that("matrix_zeros creates zero matrix", {
  m <- matrix_zeros(2, 3)
  stopifnot(all(dim(m) == c(2, 3)))
  stopifnot(all(m == 0))
})

test_that("matrix_ones creates ones matrix", {
  m <- matrix_ones(2, 3)
  stopifnot(all(dim(m) == c(2, 3)))
  stopifnot(all(m == 1))
})

test_that("matrix_diagonal creates diagonal matrix", {
  m <- matrix_diagonal(c(1, 2, 3))
  stopifnot(all(dim(m) == c(3, 3)))
  stopifnot(diag(m)[1] == 1)
  stopifnot(diag(m)[2] == 2)
  stopifnot(diag(m)[3] == 3)
})

test_that("matrix_validate accepts valid matrix", {
  m <- matrix_identity(3)
  stopifnot(matrix_validate(m))
})

# ============================================================================
# Basic Operations Tests
# ============================================================================

cat("\n=== Basic Operations Tests ===\n")

test_that("matrix_add works correctly", {
  a <- matrix_create(1:4, 2, 2)
  b <- matrix_create(5:8, 2, 2)
  result <- matrix_add(a, b)
  expected <- matrix_create(6:9, 2, 2)
  stopifnot(matrix_approx_equal(result, expected))
})

test_that("matrix_subtract works correctly", {
  a <- matrix_create(5:8, 2, 2)
  b <- matrix_create(1:4, 2, 2)
  result <- matrix_subtract(a, b)
  expected <- matrix_create(4:7, 2, 2)
  stopifnot(matrix_approx_equal(result, expected))
})

test_that("matrix_multiply_elementwise works", {
  a <- matrix_create(c(1, 2, 3, 4), 2, 2)
  b <- matrix_create(c(2, 3, 4, 5), 2, 2)
  result <- matrix_multiply_elementwise(a, b)
  stopifnot(result[1, 1] == 2)
  stopifnot(result[2, 2] == 20)
})

test_that("matrix_multiply works correctly", {
  a <- matrix_create(c(1, 2, 3, 4), 2, 2)
  b <- matrix_create(c(2, 0, 0, 2), 2, 2)
  result <- matrix_multiply(a, b)
  stopifnot(result[1, 1] == 2)
  stopifnot(result[1, 2] == 6)
  stopifnot(result[2, 1] == 4)
  stopifnot(result[2, 2] == 8)
})

test_that("matrix_scale works correctly", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_scale(m, 2)
  stopifnot(result[1, 1] == 2)
  stopifnot(result[2, 2] == 8)
})

test_that("matrix_power works for power 0", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_power(m, 0)
  stopifnot(matrix_approx_equal(result, matrix_identity(2)))
})

test_that("matrix_power works for power 1", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_power(m, 1)
  stopifnot(matrix_approx_equal(result, m))
})

test_that("matrix_power works for power 2", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_power(m, 2)
  expected <- matrix_multiply(m, m)
  stopifnot(matrix_approx_equal(result, expected))
})

test_that("matrix_transpose works correctly", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  result <- matrix_transpose(m)
  stopifnot(all(dim(result) == c(3, 2)))
  stopifnot(result[1, 1] == 1)
  stopifnot(result[3, 2] == 6)
})

test_that("matrix_trace works correctly", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6, 7, 8, 9), 3, 3)
  result <- matrix_trace(m)
  stopifnot(result == 15)  # 1 + 5 + 9
})

test_that("matrix_determinant works for 2x2", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_determinant(m)
  stopifnot(result == -2)  # 1*4 - 2*3
})

test_that("matrix_determinant works for 3x3", {
  m <- matrix_identity(3)
  result <- matrix_determinant(m)
  stopifnot(result == 1)
})

# ============================================================================
# Inversion and Solving Tests
# ============================================================================

cat("\n=== Inversion and Solving Tests ===\n")

test_that("matrix_inverse works for identity", {
  m <- matrix_identity(3)
  result <- matrix_inverse(m)
  stopifnot(matrix_approx_equal(result, m))
})

test_that("matrix_inverse works for 2x2 matrix", {
  m <- matrix_create(c(4, 7, 2, 6), 2, 2)
  inv <- matrix_inverse(m)
  result <- matrix_multiply(m, inv)
  stopifnot(matrix_approx_equal(result, matrix_identity(2)))
})

test_that("matrix_inverse works for 3x3 matrix", {
  m <- matrix_create(c(1, 2, 3, 0, 1, 4, 5, 6, 0), 3, 3)
  inv <- matrix_inverse(m)
  result <- matrix_multiply(m, inv)
  stopifnot(matrix_approx_equal(result, matrix_identity(3)))
})

test_that("matrix_pseudo_inverse works for rectangular matrix", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  pinv <- matrix_pseudo_inverse(m)
  stopifnot(all(dim(pinv) == c(3, 2)))
  # Check A * A+ * A ≈ A
  result <- matrix_multiply(matrix_multiply(m, pinv), m)
  stopifnot(matrix_approx_equal(result, m, 1e-6))
})

test_that("matrix_solve works for linear system", {
  a <- matrix_create(c(3, 2, 1, 1), 2, 2)
  b <- c(9, 4)
  result <- matrix_solve(a, b)
  stopifnot(approx_equal(result, c(1, 3)))
})

test_that("matrix_condition_number works", {
  m <- matrix_identity(3)
  cn <- matrix_condition_number(m)
  stopifnot(cn == 1)
})

# ============================================================================
# Decomposition Tests
# ============================================================================

cat("\n=== Decomposition Tests ===\n")

test_that("matrix_lu works for simple matrix", {
  m <- matrix_create(c(4, 3, 6, 3), 2, 2)
  lu <- matrix_lu(m)
  # L should be lower triangular
  stopifnot(lu$L[1, 2] == 0)
  # U should be upper triangular
  stopifnot(lu$U[2, 1] == 0)
  # L * U should equal original (with permutation)
  reconstructed <- matrix_multiply(lu$L, lu$U)
  permuted <- matrix_multiply(lu$P, m)
  stopifnot(matrix_approx_equal(reconstructed, permuted))
})

test_that("matrix_qr works for simple matrix", {
  m <- matrix_create(c(12, 6, -4, -51, 167, 24, 4, -68, -41), 3, 3)
  qr_result <- matrix_qr(m)
  # Q should be orthogonal
  stopifnot(is_orthogonal(qr_result$Q))
  # R should be upper triangular
  stopifnot(qr_result$R[2, 1] == 0)
  stopifnot(qr_result$R[3, 1] == 0)
  stopifnot(qr_result$R[3, 2] == 0)
  # Q * R should equal original
  reconstructed <- matrix_multiply(qr_result$Q, qr_result$R)
  stopifnot(matrix_approx_equal(reconstructed, m))
})

test_that("matrix_cholesky works for positive definite", {
  m <- matrix_positive_definite(3)
  L <- matrix_cholesky(m)
  # L should be lower triangular
  stopifnot(L[1, 2] == 0)
  stopifnot(L[1, 3] == 0)
  stopifnot(L[2, 3] == 0)
  # L * L^T should equal original
  reconstructed <- matrix_multiply(L, matrix_transpose(L))
  stopifnot(matrix_approx_equal(reconstructed, m))
})

test_that("matrix_eigen works for symmetric matrix", {
  m <- matrix_symmetric(3)
  eigen_result <- matrix_eigen(m)
  # Check that eigenvalues are returned
  stopifnot(length(eigen_result$values) == 3)
  # Check that eigenvectors are returned
  stopifnot(all(dim(eigen_result$vectors) == c(3, 3)))
})

test_that("matrix_svd works for rectangular matrix", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  svd_result <- matrix_svd(m)
  # Check dimensions
  stopifnot(all(dim(svd_result$U) == c(2, 2)))
  stopifnot(length(svd_result$S) == 2)
  stopifnot(all(dim(svd_result$V) == c(3, 3)))
  # Singular values should be positive and sorted
  stopifnot(all(svd_result$S > 0))
  stopifnot(svd_result$S[1] >= svd_result$S[2])
})

# ============================================================================
# Matrix Properties Tests
# ============================================================================

cat("\n=== Matrix Properties Tests ===\n")

test_that("is_symmetric returns TRUE for symmetric matrix", {
  m <- matrix_symmetric(3)
  stopifnot(is_symmetric(m))
})

test_that("is_symmetric returns FALSE for non-symmetric matrix", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  stopifnot(!is_symmetric(m))
})

test_that("is_diagonal returns TRUE for diagonal matrix", {
  m <- matrix_diagonal(c(1, 2, 3))
  stopifnot(is_diagonal(m))
})

test_that("is_diagonal returns FALSE for non-diagonal matrix", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  stopifnot(!is_diagonal(m))
})

test_that("is_identity returns TRUE for identity matrix", {
  m <- matrix_identity(3)
  stopifnot(is_identity(m))
})

test_that("is_identity returns FALSE for non-identity matrix", {
  m <- matrix_diagonal(c(1, 2, 3))
  stopifnot(!is_identity(m))
})

test_that("is_orthogonal returns TRUE for identity matrix", {
  m <- matrix_identity(3)
  stopifnot(is_orthogonal(m))
})

test_that("is_orthogonal returns FALSE for non-orthogonal matrix", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  stopifnot(!is_orthogonal(m))
})

test_that("is_positive_definite returns TRUE for PD matrix", {
  m <- matrix_positive_definite(3)
  stopifnot(is_positive_definite(m))
})

test_that("is_positive_definite returns FALSE for non-PD matrix", {
  m <- matrix_create(c(-1, 0, 0, -1), 2, 2)
  stopifnot(!is_positive_definite(m))
})

test_that("matrix_rank returns correct rank", {
  m <- matrix_identity(3)
  stopifnot(matrix_rank(m) == 3)
})

test_that("matrix_rank returns 1 for rank-1 matrix", {
  m <- matrix_ones(3, 3)
  stopifnot(matrix_rank(m) == 1)
})

test_that("matrix_norm works for Frobenius norm", {
  m <- matrix_identity(2)
  result <- matrix_norm(m, "fro")
  stopifnot(approx_equal(result, sqrt(2)))
})

test_that("matrix_norm works for 1-norm", {
  m <- matrix_create(c(1, -2, 3, -4), 2, 2)
  result <- matrix_norm(m, "1")
  stopifnot(result == 6)  # max(1+3, 2+4) = 4, actually max(colSums)
})

test_that("matrix_norm works for infinity-norm", {
  m <- matrix_create(c(1, -2, 3, -4), 2, 2)
  result <- matrix_norm(m, "inf")
  stopifnot(result == 7)  # max(1+3, 2+4) = 4
})

# ============================================================================
# Special Matrices Tests
# ============================================================================

cat("\n=== Special Matrices Tests ===\n")

test_that("matrix_random creates matrix with correct dimensions", {
  m <- matrix_random(3, 4)
  stopifnot(all(dim(m) == c(3, 4)))
})

test_that("matrix_random creates matrix with values in range", {
  m <- matrix_random(3, 3, min = 5, max = 10)
  stopifnot(all(m >= 5))
  stopifnot(all(m <= 10))
})

test_that("matrix_symmetric creates symmetric matrix", {
  m <- matrix_symmetric(4)
  stopifnot(is_symmetric(m))
})

test_that("matrix_positive_definite creates PD matrix", {
  m <- matrix_positive_definite(4)
  stopifnot(is_positive_definite(m))
})

test_that("matrix_tridiagonal creates tridiagonal matrix", {
  m <- matrix_tridiagonal(5, 2, -1)
  stopifnot(all(diag(m) == 2))
  stopifnot(m[1, 3] == 0)  # Should be zero outside tridiagonal
  stopifnot(m[1, 2] == -1)
})

test_that("matrix_hilbert creates correct Hilbert matrix", {
  m <- matrix_hilbert(3)
  stopifnot(approx_equal(m[1, 1], 1.0))
  stopifnot(approx_equal(m[1, 2], 1/2))
  stopifnot(approx_equal(m[2, 1], 1/3))
  stopifnot(approx_equal(m[2, 2], 1/4))
})

test_that("matrix_vandermonde creates correct Vandermonde matrix", {
  x <- c(1, 2, 3)
  m <- matrix_vandermonde(x)
  stopifnot(all(dim(m) == c(3, 3)))
  stopifnot(m[1, 1] == 1)  # 1^0
  stopifnot(m[2, 2] == 2)  # 2^1
  stopifnot(m[3, 3] == 9)  # 3^2
})

# ============================================================================
# Matrix Operations Tests
# ============================================================================

cat("\n=== Matrix Operations Tests ===\n")

test_that("matrix_get_diagonal extracts diagonal", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6, 7, 8, 9), 3, 3)
  diag_vals <- matrix_get_diagonal(m)
  stopifnot(approx_equal(diag_vals, c(1, 5, 9)))
})

test_that("matrix_set_diagonal sets diagonal", {
  m <- matrix_zeros(3, 3)
  m <- matrix_set_diagonal(m, c(1, 2, 3))
  stopifnot(m[1, 1] == 1)
  stopifnot(m[2, 2] == 2)
  stopifnot(m[3, 3] == 3)
})

test_that("matrix_get_row extracts row", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  row <- matrix_get_row(m, 1)
  stopifnot(approx_equal(row, c(1, 3, 5)))
})

test_that("matrix_get_column extracts column", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  col <- matrix_get_column(m, 2)
  stopifnot(approx_equal(col, c(3, 4)))
})

test_that("matrix_swap_rows swaps rows", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_swap_rows(m, 1, 2)
  stopifnot(result[1, 1] == 2)
  stopifnot(result[2, 1] == 1)
})

test_that("matrix_swap_columns swaps columns", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  result <- matrix_swap_columns(m, 1, 2)
  stopifnot(result[1, 1] == 3)
  stopifnot(result[1, 2] == 1)
})

test_that("matrix_flatten works by column", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  result <- matrix_flatten(m)
  stopifnot(approx_equal(result, c(1, 2, 3, 4, 5, 6)))
})

test_that("matrix_flatten works by row", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  result <- matrix_flatten(m, byrow = TRUE)
  stopifnot(approx_equal(result, c(1, 3, 5, 2, 4, 6)))
})

test_that("matrix_reshape works correctly", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  result <- matrix_reshape(m, 3, 2)
  stopifnot(all(dim(result) == c(3, 2)))
  stopifnot(length(result) == 6)
})

# ============================================================================
# Matrix Analysis Tests
# ============================================================================

cat("\n=== Matrix Analysis Tests ===\n")

test_that("matrix_summary returns correct info for square matrix", {
  m <- matrix_create(c(1, 2, 3, 4), 2, 2)
  info <- matrix_summary(m)
  stopifnot(info$is_square)
  stopifnot(all(info$dimensions == c(2, 2)))
  stopifnot(info$size == 4)
})

test_that("matrix_summary returns correct info for rectangular matrix", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  info <- matrix_summary(m)
  stopifnot(!info$is_square)
  stopifnot(all(info$dimensions == c(2, 3)))
})

test_that("matrix_summary calculates correct statistics", {
  m <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
  info <- matrix_summary(m)
  stopifnot(info$min == 1)
  stopifnot(info$max == 6)
})

# ============================================================================
# Edge Cases and Error Handling Tests
# ============================================================================

cat("\n=== Edge Cases and Error Handling Tests ===\n")

test_that("matrix_inverse fails for singular matrix", {
  m <- matrix_create(c(1, 2, 2, 4), 2, 2)  # Singular
  tryCatch({
    matrix_inverse(m)
    stop("Should have thrown an error")
  }, error = function(e) {
    # Expected error
  })
})

test_that("matrix_add fails for different dimensions", {
  a <- matrix_zeros(2, 2)
  b <- matrix_zeros(3, 3)
  tryCatch({
    matrix_add(a, b)
    stop("Should have thrown an error")
  }, error = function(e) {
    # Expected error
  })
})

test_that("matrix_multiply fails for incompatible dimensions", {
  a <- matrix_zeros(2, 3)
  b <- matrix_zeros(4, 5)
  tryCatch({
    matrix_multiply(a, b)
    stop("Should have thrown an error")
  }, error = function(e) {
    # Expected error
  })
})

test_that("matrix_cholesky fails for non-positive definite", {
  m <- matrix_create(c(-1, 0, 0, -1), 2, 2)
  tryCatch({
    matrix_cholesky(m)
    stop("Should have thrown an error")
  }, error = function(e) {
    # Expected error
  })
})

test_that("large matrix operations work", {
  m <- matrix_random(100, 100)
  # Just verify it doesn't crash
  cn <- matrix_condition_number(m)
  rk <- matrix_rank(m)
  stopifnot(is.numeric(cn))
  stopifnot(is.numeric(rk))
})

test_that("identity matrix operations", {
  m <- matrix_identity(5)
  inv <- matrix_inverse(m)
  stopifnot(matrix_approx_equal(m, inv))
  stopifnot(matrix_determinant(m) == 1)
  stopifnot(matrix_trace(m) == 5)
})

test_that("matrix power consistency", {
  m <- matrix_create(c(1, 2, 0, 1), 2, 2)
  p3 <- matrix_power(m, 3)
  p2 <- matrix_power(m, 2)
  p1 <- matrix_power(m, 1)
  stopifnot(matrix_approx_equal(p1, m))
  stopifnot(matrix_approx_equal(p3, matrix_multiply(p2, m)))
})

# ============================================================================
# Test Summary
# ============================================================================

cat("\n========================================\n")
cat("Total tests:", tests_passed + tests_failed, "\n")
cat("Passed:", tests_passed, "\n")
cat("Failed:", tests_failed, "\n")
cat("Success rate:", round(tests_passed / (tests_passed + tests_failed) * 100, 1), "%\n")
cat("========================================\n")

if (tests_failed > 0) {
  quit(status = 1)
}