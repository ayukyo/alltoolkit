#!/usr/bin/env Rscript
# matrix_utils/mod.R - Matrix Utilities Module for R
#
# A comprehensive matrix utility module providing linear algebra operations,
# matrix decompositions, and numerical methods with zero dependencies.
#
# Author: AllToolkit
# Version: 1.0.0
# License: MIT

# ============================================================================
# Module Metadata
# ============================================================================

MATRIX_UTILS_VERSION <- "1.0.0"
MATRIX_UTILS_AUTHOR <- "AllToolkit"

# ============================================================================
# Matrix Creation and Validation
# ============================================================================

#' Create a Matrix from Vector
#'
#' @param x A numeric vector
#' @param nrow Number of rows
#' @param ncol Number of columns (optional, calculated if not provided)
#' @param byrow Fill by row? Default: FALSE
#' @return A matrix
matrix_create <- function(x, nrow, ncol = NULL, byrow = FALSE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (length(x) == 0) {
    stop("Input vector cannot be empty")
  }
  if (is.null(ncol)) {
    if (length(x) %% nrow != 0) {
      stop("Vector length must be divisible by nrow")
    }
    ncol <- length(x) / nrow
  }
  matrix(x, nrow = nrow, ncol = ncol, byrow = byrow)
}

#' Create Identity Matrix
#'
#' @param n Size of the identity matrix
#' @return An n x n identity matrix
matrix_identity <- function(n) {
  if (!is.numeric(n) || n <= 0 || n != floor(n)) {
    stop("n must be a positive integer")
  }
  diag(n)
}

#' Create Zero Matrix
#'
#' @param nrow Number of rows
#' @param ncol Number of columns (default: nrow)
#' @return A matrix of zeros
matrix_zeros <- function(nrow, ncol = nrow) {
  if (!is.numeric(nrow) || nrow <= 0 || nrow != floor(nrow)) {
    stop("nrow must be a positive integer")
  }
  if (!is.numeric(ncol) || ncol <= 0 || ncol != floor(ncol)) {
    stop("ncol must be a positive integer")
  }
  matrix(0, nrow = nrow, ncol = ncol)
}

#' Create Ones Matrix
#'
#' @param nrow Number of rows
#' @param ncol Number of columns (default: nrow)
#' @return A matrix of ones
matrix_ones <- function(nrow, ncol = nrow) {
  if (!is.numeric(nrow) || nrow <= 0 || nrow != floor(nrow)) {
    stop("nrow must be a positive integer")
  }
  if (!is.numeric(ncol) || ncol <= 0 || ncol != floor(ncol)) {
    stop("ncol must be a positive integer")
  }
  matrix(1, nrow = nrow, ncol = ncol)
}

#' Create Diagonal Matrix
#'
#' @param x A vector of diagonal elements
#' @return A diagonal matrix
matrix_diagonal <- function(x) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  diag(x)
}

#' Validate Matrix
#'
#' @param m A matrix
#' @return TRUE if valid, stops with error otherwise
matrix_validate <- function(m) {
  if (!is.matrix(m)) {
    stop("Input must be a matrix")
  }
  if (!is.numeric(m)) {
    stop("Matrix must be numeric")
  }
  if (any(is.na(m))) {
    stop("Matrix cannot contain NA values")
  }
  TRUE
}

#' Get Matrix Dimensions
#'
#' @param m A matrix
#' @return A list with nrow, ncol, and is_square
matrix_dims <- function(m) {
  matrix_validate(m)
  list(
    nrow = nrow(m),
    ncol = ncol(m),
    is_square = nrow(m) == ncol(m)
  )
}

# ============================================================================
# Basic Matrix Operations
# ============================================================================

#' Matrix Addition
#'
#' @param a First matrix
#' @param b Second matrix
#' @return Sum of matrices
matrix_add <- function(a, b) {
  matrix_validate(a)
  matrix_validate(b)
  if (!all(dim(a) == dim(b))) {
    stop("Matrices must have the same dimensions")
  }
  a + b
}

#' Matrix Subtraction
#'
#' @param a First matrix
#' @param b Second matrix
#' @return Difference of matrices
matrix_subtract <- function(a, b) {
  matrix_validate(a)
  matrix_validate(b)
  if (!all(dim(a) == dim(b))) {
    stop("Matrices must have the same dimensions")
  }
  a - b
}

#' Matrix Multiplication (Element-wise)
#'
#' @param a First matrix
#' @param b Second matrix
#' @return Element-wise product
matrix_multiply_elementwise <- function(a, b) {
  matrix_validate(a)
  matrix_validate(b)
  if (!all(dim(a) == dim(b))) {
    stop("Matrices must have the same dimensions")
  }
  a * b
}

#' Matrix Multiplication (Dot Product)
#'
#' @param a First matrix
#' @param b Second matrix
#' @return Matrix product
matrix_multiply <- function(a, b) {
  matrix_validate(a)
  matrix_validate(b)
  if (ncol(a) != nrow(b)) {
    stop("Number of columns in a must equal number of rows in b")
  }
  a %*% b
}

#' Scalar Multiplication
#'
#' @param m A matrix
#' @param scalar A scalar value
#' @return Scaled matrix
matrix_scale <- function(m, scalar) {
  matrix_validate(m)
  if (!is.numeric(scalar) || length(scalar) != 1) {
    stop("Scalar must be a single numeric value")
  }
  m * scalar
}

#' Matrix Power
#'
#' @param m A square matrix
#' @param n Power (positive integer)
#' @return Matrix raised to power n
matrix_power <- function(m, n) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  if (!is.numeric(n) || n < 0 || n != floor(n)) {
    stop("Power must be a non-negative integer")
  }
  if (n == 0) {
    return(matrix_identity(nrow(m)))
  }
  if (n == 1) {
    return(m)
  }
  result <- m
  for (i in 2:n) {
    result <- result %*% m
  }
  result
}

#' Matrix Transpose
#'
#' @param m A matrix
#' @return Transposed matrix
matrix_transpose <- function(m) {
  matrix_validate(m)
  t(m)
}

#' Matrix Trace
#'
#' @param m A square matrix
#' @return The trace (sum of diagonal elements)
matrix_trace <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  sum(diag(m))
}

#' Matrix Determinant
#'
#' @param m A square matrix
#' @return The determinant
matrix_determinant <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  det(m)
}

# ============================================================================
# Matrix Inversion and Solving
# ============================================================================

#' Matrix Inverse
#'
#' @param m A square invertible matrix
#' @return The inverse matrix
matrix_inverse <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  d <- det(m)
  if (abs(d) < 1e-10) {
    stop("Matrix is singular (determinant is zero)")
  }
  solve(m)
}

#' Pseudo-Inverse (Moore-Penrose)
#'
#' @param m A matrix
#' @return The pseudo-inverse
matrix_pseudo_inverse <- function(m) {
  matrix_validate(m)
  # Using SVD: A+ = V * diag(1/sigma) * U^T
  svd_result <- svd(m)
  # Handle small singular values
  tol <- max(dim(m)) * .Machine$double.eps * max(svd_result$d)
  singular_values <- svd_result$d
  singular_values[singular_values < tol] <- 0
  singular_values[singular_values > 0] <- 1 / singular_values[singular_values > 0]
  
  svd_result$v %*% diag(singular_values, nrow = length(singular_values)) %*% t(svd_result$u)
}

#' Solve Linear System Ax = b
#'
#' @param a Coefficient matrix
#' @param b Right-hand side vector or matrix
#' @return Solution vector/matrix
matrix_solve <- function(a, b) {
  matrix_validate(a)
  if (!matrix_dims(a)$is_square) {
    stop("Coefficient matrix must be square")
  }
  if (is.vector(b)) {
    if (length(b) != nrow(a)) {
      stop("b must have same length as a rows")
    }
    b <- matrix(b, ncol = 1)
  } else {
    matrix_validate(b)
    if (nrow(b) != nrow(a)) {
      stop("b must have same number of rows as a")
    }
  }
  solve(a, b)
}

#' Condition Number
#'
#' @param m A matrix
#' @param p Norm type (2 = spectral, default)
#' @return The condition number
matrix_condition_number <- function(m, p = 2) {
  matrix_validate(m)
  if (p == 2) {
    svd_result <- svd(m)
    singular_values <- svd_result$d
    if (min(singular_values) == 0) {
      return(Inf)
    }
    max(singular_values) / min(singular_values)
  } else {
    stop("Only 2-norm condition number is supported")
  }
}

# ============================================================================
# Matrix Decompositions
# ============================================================================

#' LU Decomposition
#'
#' @param m A square matrix
#' @return A list with L (lower), U (upper), and permutation
matrix_lu <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  n <- nrow(m)
  U <- m
  L <- matrix_identity(n)
  P <- matrix_identity(n)
  
  for (k in 1:(n - 1)) {
    # Find pivot
    pivot <- which.max(abs(U[k:n, k])) + k - 1
    if (pivot != k) {
      # Swap rows in U
      temp <- U[k, ]
      U[k, ] <- U[pivot, ]
      U[pivot, ] <- temp
      # Swap rows in P
      temp <- P[k, ]
      P[k, ] <- P[pivot, ]
      P[pivot, ] <- temp
      # Swap rows in L (only columns 1 to k-1)
      if (k > 1) {
        temp <- L[k, 1:(k - 1)]
        L[k, 1:(k - 1)] <- L[pivot, 1:(k - 1)]
        L[pivot, 1:(k - 1)] <- temp
      }
    }
    
    if (U[k, k] != 0) {
      for (i in (k + 1):n) {
        L[i, k] <- U[i, k] / U[k, k]
        U[i, k:n] <- U[i, k:n] - L[i, k] * U[k, k:n]
      }
    }
  }
  
  list(L = L, U = U, P = P)
}

#' QR Decomposition
#'
#' @param m A matrix
#' @return A list with Q (orthogonal) and R (upper triangular)
matrix_qr <- function(m) {
  matrix_validate(m)
  qr_result <- qr(m)
  Q <- qr.Q(qr_result)
  R <- qr.R(qr_result)
  list(Q = Q, R = R)
}

#' Cholesky Decomposition
#'
#' @param m A symmetric positive definite matrix
#' @return Lower triangular matrix L such that m = L * L^T
matrix_cholesky <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  n <- nrow(m)
  
  # Check symmetry
  if (!is_symmetric(m)) {
    stop("Matrix must be symmetric")
  }
  
  # Perform Cholesky decomposition
  L <- matrix_zeros(n, n)
  
  for (i in 1:n) {
    for (j in 1:i) {
      sum_val <- 0
      if (j == i) {
        for (k in 1:(j - 1)) {
          sum_val <- sum_val + L[j, k]^2
        }
        val <- m[j, j] - sum_val
        if (val < 0) {
          stop("Matrix is not positive definite")
        }
        L[j, j] <- sqrt(val)
      } else {
        for (k in 1:(j - 1)) {
          sum_val <- sum_val + L[i, k] * L[j, k]
        }
        if (L[j, j] == 0) {
          stop("Matrix is not positive definite")
        }
        L[i, j] <- (m[i, j] - sum_val) / L[j, j]
      }
    }
  }
  
  L
}

#' Eigenvalue Decomposition
#'
#' @param m A square matrix
#' @return A list with values (eigenvalues) and vectors (eigenvectors)
matrix_eigen <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  eigen_result <- eigen(m)
  list(
    values = eigen_result$values,
    vectors = eigen_result$vectors
  )
}

#' Singular Value Decomposition
#'
#' @param m A matrix
#' @return A list with U, S (singular values), and V
matrix_svd <- function(m) {
  matrix_validate(m)
  svd_result <- svd(m)
  list(
    U = svd_result$u,
    S = svd_result$d,
    V = svd_result$v
  )
}

# ============================================================================
# Matrix Properties
# ============================================================================

#' Check if Matrix is Symmetric
#'
#' @param m A matrix
#' @param tol Tolerance for comparison
#' @return TRUE if symmetric
is_symmetric <- function(m, tol = 1e-10) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    return(FALSE)
  }
  max(abs(m - t(m))) < tol
}

#' Check if Matrix is Diagonal
#'
#' @param m A matrix
#' @param tol Tolerance for comparison
#' @return TRUE if diagonal
is_diagonal <- function(m, tol = 1e-10) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    return(FALSE)
  }
  off_diag <- m
  diag(off_diag) <- 0
  max(abs(off_diag)) < tol
}

#' Check if Matrix is Identity
#'
#' @param m A matrix
#' @param tol Tolerance for comparison
#' @return TRUE if identity matrix
is_identity <- function(m, tol = 1e-10) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    return(FALSE)
  }
  n <- nrow(m)
  max(abs(m - diag(n))) < tol
}

#' Check if Matrix is Orthogonal
#'
#' @param m A matrix
#' @param tol Tolerance for comparison
#' @return TRUE if orthogonal
is_orthogonal <- function(m, tol = 1e-10) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    return(FALSE)
  }
  n <- nrow(m)
  max(abs(t(m) %*% m - diag(n))) < tol
}

#' Check if Matrix is Positive Definite
#'
#' @param m A matrix
#' @return TRUE if positive definite
is_positive_definite <- function(m) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    return(FALSE)
  }
  tryCatch({
    chol(m)
    TRUE
  }, error = function(e) {
    FALSE
  })
}

#' Matrix Rank
#'
#' @param m A matrix
#' @param tol Tolerance for singular values
#' @return The rank of the matrix
matrix_rank <- function(m, tol = NULL) {
  matrix_validate(m)
  svd_result <- svd(m)
  if (is.null(tol)) {
    tol <- max(dim(m)) * .Machine$double.eps * max(svd_result$d)
  }
  sum(svd_result$d > tol)
}

#' Matrix Norm
#'
#' @param m A matrix
#' @param type Norm type: "fro" (Frobenius), "1" (1-norm), "inf" (infinity-norm), "2" (spectral)
#' @return The norm value
matrix_norm <- function(m, type = "fro") {
  matrix_validate(m)
  if (type == "fro") {
    sqrt(sum(m^2))
  } else if (type == "1") {
    max(colSums(abs(m)))
  } else if (type == "inf") {
    max(rowSums(abs(m)))
  } else if (type == "2") {
    max(svd(m)$d)
  } else {
    stop("Invalid norm type. Use 'fro', '1', 'inf', or '2'")
  }
}

# ============================================================================
# Special Matrices
# ============================================================================

#' Create a Random Matrix
#'
#' @param nrow Number of rows
#' @param ncol Number of columns (default: nrow)
#' @param min Minimum value (default: 0)
#' @param max Maximum value (default: 1)
#' @return A random matrix
matrix_random <- function(nrow, ncol = nrow, min = 0, max = 1) {
  if (!is.numeric(nrow) || nrow <= 0 || nrow != floor(nrow)) {
    stop("nrow must be a positive integer")
  }
  if (!is.numeric(ncol) || ncol <= 0 || ncol != floor(ncol)) {
    stop("ncol must be a positive integer")
  }
  matrix(runif(nrow * ncol, min = min, max = max), nrow = nrow, ncol = ncol)
}

#' Create a Symmetric Matrix
#'
#' @param n Size of the matrix
#' @param min Minimum value (default: 0)
#' @param max Maximum value (default: 1)
#' @return A symmetric matrix
matrix_symmetric <- function(n, min = 0, max = 1) {
  if (!is.numeric(n) || n <= 0 || n != floor(n)) {
    stop("n must be a positive integer")
  }
  m <- matrix_random(n, n, min, max)
  (m + t(m)) / 2
}

#' Create a Positive Definite Matrix
#'
#' @param n Size of the matrix
#' @return A positive definite matrix
matrix_positive_definite <- function(n) {
  if (!is.numeric(n) || n <= 0 || n != floor(n)) {
    stop("n must be a positive integer")
  }
  m <- matrix_random(n, n)
  m %*% t(m) + diag(n) * 0.1
}

#' Create a Tridiagonal Matrix
#'
#' @param n Size of the matrix
#' @param main Main diagonal value (default: 2)
#' @param off Off-diagonal value (default: -1)
#' @return A tridiagonal matrix
matrix_tridiagonal <- function(n, main = 2, off = -1) {
  if (!is.numeric(n) || n <= 0 || n != floor(n)) {
    stop("n must be a positive integer")
  }
  m <- matrix_zeros(n, n)
  diag(m) <- main
  if (n > 1) {
    for (i in 1:(n - 1)) {
      m[i, i + 1] <- off
      m[i + 1, i] <- off
    }
  }
  m
}

#' Create a Hilbert Matrix
#'
#' @param n Size of the matrix
#' @return A Hilbert matrix
matrix_hilbert <- function(n) {
  if (!is.numeric(n) || n <= 0 || n != floor(n)) {
    stop("n must be a positive integer")
  }
  m <- matrix_zeros(n, n)
  for (i in 1:n) {
    for (j in 1:n) {
      m[i, j] <- 1 / (i + j - 1)
    }
  }
  m
}

#' Create a Vandermonde Matrix
#'
#' @param x A vector
#' @param n Number of columns (default: length(x))
#' @return A Vandermonde matrix
matrix_vandermonde <- function(x, n = NULL) {
  if (!is.numeric(x)) {
    stop("x must be numeric")
  }
  if (is.null(n)) {
    n <- length(x)
  }
  m <- length(x)
  result <- matrix_zeros(m, n)
  for (j in 1:n) {
    result[, j] <- x^(j - 1)
  }
  result
}

# ============================================================================
# Matrix Operations
# ============================================================================

#' Get Diagonal Elements
#'
#' @param m A matrix
#' @param k Diagonal offset (0 = main, 1 = above, -1 = below)
#' @return Vector of diagonal elements
matrix_get_diagonal <- function(m, k = 0) {
  matrix_validate(m)
  diag(m, nrow = nrow(m), ncol = ncol(m), names = FALSE)
}

#' Set Diagonal Elements
#'
#' @param m A matrix
#' @param values Vector of diagonal values
#' @return Matrix with new diagonal
matrix_set_diagonal <- function(m, values) {
  matrix_validate(m)
  if (!matrix_dims(m)$is_square) {
    stop("Matrix must be square")
  }
  if (length(values) != nrow(m)) {
    stop("values must have same length as matrix dimension")
  }
  diag(m) <- values
  m
}

#' Extract Row
#'
#' @param m A matrix
#' @param i Row index
#' @return The specified row as a vector
matrix_get_row <- function(m, i) {
  matrix_validate(m)
  if (i < 1 || i > nrow(m)) {
    stop("Row index out of range")
  }
  m[i, ]
}

#' Extract Column
#'
#' @param m A matrix
#' @param j Column index
#' @return The specified column as a vector
matrix_get_column <- function(m, j) {
  matrix_validate(m)
  if (j < 1 || j > ncol(m)) {
    stop("Column index out of range")
  }
  m[, j]
}

#' Swap Rows
#'
#' @param m A matrix
#' @param i First row index
#' @param j Second row index
#' @return Matrix with swapped rows
matrix_swap_rows <- function(m, i, j) {
  matrix_validate(m)
  if (i < 1 || i > nrow(m) || j < 1 || j > nrow(m)) {
    stop("Row indices out of range")
  }
  temp <- m[i, ]
  m[i, ] <- m[j, ]
  m[j, ] <- temp
  m
}

#' Swap Columns
#'
#' @param m A matrix
#' @param i First column index
#' @param j Second column index
#' @return Matrix with swapped columns
matrix_swap_columns <- function(m, i, j) {
  matrix_validate(m)
  if (i < 1 || i > ncol(m) || j < 1 || j > ncol(m)) {
    stop("Column indices out of range")
  }
  temp <- m[, i]
  m[, i] <- m[, j]
  m[, j] <- temp
  m
}

#' Matrix Flattening
#'
#' @param m A matrix
#' @param byrow Flatten by row? Default: FALSE
#' @return Flattened vector
matrix_flatten <- function(m, byrow = FALSE) {
  matrix_validate(m)
  if (byrow) {
    as.vector(t(m))
  } else {
    as.vector(m)
  }
}

#' Reshape Matrix
#'
#' @param m A matrix
#' @param nrow New number of rows
#' @param ncol New number of columns
#' @return Reshaped matrix
matrix_reshape <- function(m, nrow, ncol) {
  matrix_validate(m)
  if (nrow * ncol != length(m)) {
    stop("Product of nrow and ncol must equal matrix size")
  }
  matrix(as.vector(m), nrow = nrow, ncol = ncol)
}

# ============================================================================
# Matrix Analysis
# ============================================================================

#' Matrix Summary
#'
#' @param m A matrix
#' @return A list with matrix properties
matrix_summary <- function(m) {
  matrix_validate(m)
  dims <- matrix_dims(m)
  
  result <- list(
    dimensions = c(dims$nrow, dims$ncol),
    is_square = dims$is_square,
    size = length(m),
    min = min(m),
    max = max(m),
    mean = mean(m),
    sd = sd(as.vector(m))
  )
  
  if (dims$is_square) {
    result$trace <- matrix_trace(m)
    result$determinant <- matrix_determinant(m)
    result$rank <- matrix_rank(m)
    result$condition_number <- matrix_condition_number(m)
    result$is_symmetric <- is_symmetric(m)
    result$is_diagonal <- is_diagonal(m)
    result$is_orthogonal <- is_orthogonal(m)
    result$is_positive_definite <- is_positive_definite(m)
  }
  
  result
}

#' Print Matrix Info
#'
#' @param m A matrix
#' @param name Optional name for the matrix
matrix_print <- function(m, name = NULL) {
  matrix_validate(m)
  if (!is.null(name)) {
    cat(name, ":\n", sep = "")
  }
  cat("Dimensions: ", nrow(m), " x ", ncol(m), "\n", sep = "")
  cat("Type: ", ifelse(matrix_dims(m)$is_square, "Square", "Rectangular"), "\n", sep = "")
  if (matrix_dims(m)$is_square) {
    cat("Determinant: ", matrix_determinant(m), "\n", sep = "")
    cat("Rank: ", matrix_rank(m), "\n", sep = "")
    cat("Condition Number: ", round(matrix_condition_number(m), 4), "\n", sep = "")
  }
  cat("Range: [", min(m), ", ", max(m), "]\n", sep = "")
  cat("Mean: ", round(mean(m), 4), "\n", sep = "")
  invisible(m)
}

# ============================================================================
# Module Export
# ============================================================================

# Return module info when sourced
cat("R Matrix Utils Module v", MATRIX_UTILS_VERSION, " loaded\n", sep = "")
cat("Author: ", MATRIX_UTILS_AUTHOR, "\n", sep = "")