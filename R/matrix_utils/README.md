# R Matrix Utilities Module

**Comprehensive matrix operations and linear algebra for R - Zero Dependencies**

## Overview

This module provides a complete suite of matrix operations, decompositions, and linear algebra functions using only R's base functionality. It covers everything from basic matrix creation and operations to advanced decompositions like LU, QR, Cholesky, and SVD.

## Features

- **Matrix Creation**: Identity, zeros, ones, diagonal, random, and special matrices
- **Basic Operations**: Addition, subtraction, multiplication, scaling, power, transpose
- **Properties**: Trace, determinant, rank, norm, condition number
- **Inversion**: Matrix inverse, pseudo-inverse (Moore-Penrose)
- **Linear Systems**: Solve Ax = b
- **Decompositions**: LU, QR, Cholesky, eigenvalue, SVD
- **Property Checks**: Symmetric, diagonal, identity, orthogonal, positive definite
- **Special Matrices**: Hilbert, Vandermonde, tridiagonal
- **Row/Column Operations**: Get, swap, extract, flatten, reshape

## Installation

```r
# Source the module directly
source("R/matrix_utils/mod.R")
```

## Quick Start

```r
# Create matrices
m <- matrix_create(1:9, nrow = 3, ncol = 3)
identity <- matrix_identity(4)
zeros <- matrix_zeros(3, 5)
diagonal <- matrix_diagonal(c(1, 2, 3))

# Basic operations
a <- matrix_create(c(1, 2, 3, 4), 2, 2)
b <- matrix_create(c(5, 6, 7, 8), 2, 2)

sum_matrix <- matrix_add(a, b)
product <- matrix_multiply(a, b)
scaled <- matrix_scale(a, 3)

# Matrix properties
trace <- matrix_trace(a)
det <- matrix_determinant(a)
rank <- matrix_rank(a)
norm <- matrix_norm(a, "fro")

# Inversion
inv <- matrix_inverse(a)

# Solve linear system
solution <- matrix_solve(a, c(1, 2))
```

## API Reference

### Matrix Creation

| Function | Description |
|----------|-------------|
| `matrix_create(x, nrow, ncol, byrow)` | Create matrix from vector |
| `matrix_identity(n)` | Create n×n identity matrix |
| `matrix_zeros(nrow, ncol)` | Create zero matrix |
| `matrix_ones(nrow, ncol)` | Create ones matrix |
| `matrix_diagonal(x)` | Create diagonal matrix |
| `matrix_random(nrow, ncol, min, max)` | Create random matrix |
| `matrix_symmetric(n, min, max)` | Create symmetric matrix |
| `matrix_positive_definite(n)` | Create positive definite matrix |
| `matrix_tridiagonal(n, main, off)` | Create tridiagonal matrix |
| `matrix_hilbert(n)` | Create Hilbert matrix |
| `matrix_vandermonde(x, n)` | Create Vandermonde matrix |

### Basic Operations

| Function | Description |
|----------|-------------|
| `matrix_add(a, b)` | Matrix addition |
| `matrix_subtract(a, b)` | Matrix subtraction |
| `matrix_multiply_elementwise(a, b)` | Element-wise multiplication |
| `matrix_multiply(a, b)` | Matrix multiplication (dot product) |
| `matrix_scale(m, scalar)` | Scalar multiplication |
| `matrix_power(m, n)` | Matrix raised to power n |
| `matrix_transpose(m)` | Matrix transpose |

### Matrix Properties

| Function | Description |
|----------|-------------|
| `matrix_trace(m)` | Sum of diagonal elements |
| `matrix_determinant(m)` | Matrix determinant |
| `matrix_rank(m)` | Matrix rank |
| `matrix_condition_number(m)` | Condition number |
| `matrix_norm(m, type)` | Matrix norm (fro, 1, inf, 2) |
| `matrix_dims(m)` | Matrix dimensions info |
| `matrix_validate(m)` | Validate matrix input |

### Inversion and Solving

| Function | Description |
|----------|-------------|
| `matrix_inverse(m)` | Matrix inverse |
| `matrix_pseudo_inverse(m)` | Moore-Penrose pseudo-inverse |
| `matrix_solve(a, b)` | Solve linear system Ax = b |

### Decompositions

| Function | Description |
|----------|-------------|
| `matrix_lu(m)` | LU decomposition with permutation |
| `matrix_qr(m)` | QR decomposition |
| `matrix_cholesky(m)` | Cholesky decomposition (for PD matrices) |
| `matrix_eigen(m)` | Eigenvalue decomposition |
| `matrix_svd(m)` | Singular Value Decomposition |

### Property Checks

| Function | Description |
|----------|-------------|
| `is_symmetric(m)` | Check if matrix is symmetric |
| `is_diagonal(m)` | Check if matrix is diagonal |
| `is_identity(m)` | Check if matrix is identity |
| `is_orthogonal(m)` | Check if matrix is orthogonal |
| `is_positive_definite(m)` | Check if matrix is positive definite |

### Row/Column Operations

| Function | Description |
|----------|-------------|
| `matrix_get_row(m, i)` | Extract row i |
| `matrix_get_column(m, j)` | Extract column j |
| `matrix_get_diagonal(m, k)` | Extract diagonal |
| `matrix_set_diagonal(m, values)` | Set diagonal values |
| `matrix_swap_rows(m, i, j)` | Swap rows i and j |
| `matrix_swap_columns(m, i, j)` | Swap columns i and j |
| `matrix_flatten(m, byrow)` | Flatten to vector |
| `matrix_reshape(m, nrow, ncol)` | Reshape matrix |

### Analysis

| Function | Description |
|----------|-------------|
| `matrix_summary(m)` | Comprehensive matrix properties |
| `matrix_print(m, name)` | Print matrix information |

## Examples

### Linear System Solving

```r
# Solve 2x + y = 5
#       x + 3y = 10
a <- matrix_create(c(2, 1, 1, 3), 2, 2)
b <- c(5, 10)
x <- matrix_solve(a, b)
# x = [1, 3]
```

### Matrix Decomposition

```r
# LU Decomposition
m <- matrix_create(c(4, 3, 6, 3), 2, 2)
lu <- matrix_lu(m)
# L = lower triangular, U = upper triangular, P = permutation

# QR Decomposition
qr_result <- matrix_qr(m)
# Q = orthogonal, R = upper triangular

# Cholesky (for positive definite)
pd <- matrix_positive_definite(3)
L <- matrix_cholesky(pd)
# m = L * L^T
```

### Eigenvalues and SVD

```r
# Eigenvalue decomposition
sym <- matrix_symmetric(4)
eigen <- matrix_eigen(sym)
# eigen$values: eigenvalues
# eigen$vectors: eigenvectors

# Singular Value Decomposition
rect <- matrix_create(c(1, 2, 3, 4, 5, 6), 2, 3)
svd <- matrix_svd(rect)
# U, S (singular values), V
```

### Special Matrices

```r
# Hilbert matrix (ill-conditioned)
hilbert <- matrix_hilbert(5)

# Vandermonde matrix (for polynomial fitting)
x <- c(1, 2, 3, 4)
vander <- matrix_vandermonde(x)

# Tridiagonal matrix (common in physics)
tridiag <- matrix_tridiagonal(10, 2, -1)
```

### Matrix Properties

```r
# Check matrix properties
m <- matrix_positive_definite(5)

is_symmetric(m)       # TRUE
is_positive_definite(m)  # TRUE
matrix_rank(m)        # 5
matrix_condition_number(m)  # typically moderate
```

## Testing

Run the test suite:

```r
source("R/matrix_utils/matrix_utils_test.R")
```

The test suite includes:
- 60+ comprehensive test cases
- Edge case handling
- Error handling validation
- Decomposition verification
- Large matrix operations

## Dependencies

**Zero external dependencies** - uses only R's base functionality:
- Base matrix operations
- Built-in `svd()`, `qr()`, `eigen()`
- Basic math functions

## Performance Notes

- Matrix operations use R's optimized built-in functions
- LU decomposition includes partial pivoting for stability
- Cholesky requires positive definite input
- Large matrices (>1000×1000) may be slow for complex operations

## Version

- **Version**: 1.0.0
- **Author**: AllToolkit
- **License**: MIT

## Related Modules

- `stats_utils` - Statistical operations
- `correlation_utils` - Correlation analysis
- `graph_utils` - Graph algorithms