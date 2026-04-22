# Matrix Utilities

A zero-dependency Python library for comprehensive matrix operations, including basic arithmetic, linear algebra operations, decompositions, and eigenvalue computation.

## Features

- **Matrix Class**: Full-featured matrix implementation with intuitive API
- **Basic Operations**: Addition, subtraction, multiplication, transpose
- **Advanced Operations**: Determinant, inverse, rank, trace
- **Linear Systems**: Solve Ax = b using LU decomposition
- **Decompositions**: QR, Cholesky, LU decomposition
- **Eigenvalues**: Power iteration and QR algorithm
- **Matrix Properties**: Square, symmetric, diagonal, triangular checks
- **Vector Utilities**: Dot/cross product, norms, Gram-Schmidt

## Installation

No external dependencies required. Just copy the `matrix_utils` folder to your project.

## Quick Start

```python
from matrix_utils import Matrix

# Create matrices
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Basic operations
C = A + B           # Addition
D = A * B           # Matrix multiplication
E = A * 2           # Scalar multiplication
T = A.transpose()   # Transpose

# Determinant and inverse
det = A.determinant()
inv = A.inverse()

# Solve linear system Ax = b
A = Matrix([[2, 1], [1, 3]])
b = Matrix([[5], [10]])
x = A.solve(b)  # Solution: x = [1, 3]
```

## Matrix Creation

```python
# From list
m = Matrix([[1, 2, 3], [4, 5, 6]])

# Special matrices
zeros = Matrix.zeros(3, 4)          # 3x4 zero matrix
ones = Matrix.ones(3, 3)            # 3x3 matrix of ones
identity = Matrix.identity(4)        # 4x4 identity matrix
diag = Matrix.diagonal([1, 2, 3])    # Diagonal matrix
random = Matrix.random(3, 3)        # Random matrix

# From rows or columns
from_rows = Matrix.from_rows([1, 2], [3, 4])
from_cols = Matrix.from_cols([1, 2], [3, 4])

# Special matrices
hilbert = Matrix.hilbert(4)          # Hilbert matrix
vander = Matrix.vandermonde([1,2,3]) # Vandermonde matrix
```

## Matrix Operations

```python
# Arithmetic
A + B       # Matrix addition
A - B       # Matrix subtraction
A * B       # Matrix multiplication
A * 2       # Scalar multiplication
2 * A       # Scalar multiplication (right)
A ** 2      # Matrix power
-A          # Negation

# Properties
A.transpose()      # Transpose
A.trace()          # Trace (sum of diagonal)
A.determinant()    # Determinant
A.inverse()        # Matrix inverse
A.rank()           # Matrix rank

# Norms
A.norm()           # Frobenius norm
A.norm(1)          # 1-norm (max column sum)
A.norm('inf')      # Infinity norm (max row sum)
```

## Solving Linear Systems

```python
# Solve Ax = b
A = Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
b = Matrix([[8], [-11], [-3]])
x = A.solve(b)
```

## Matrix Decompositions

```python
# QR Decomposition: A = QR
A = Matrix([[1, 2], [3, 4], [5, 6]])
Q, R = A.qr_decompose()

# Cholesky Decomposition: A = LL^T (for symmetric positive definite)
A = Matrix([[4, 2], [2, 3]])
L = A.cholesky()

# LU Decomposition (internal, used for solve/determinant)
lu, pivot = A._lu_decompose()
```

## Eigenvalues

```python
# Compute eigenvalues using QR algorithm
A = Matrix([[2, 1], [1, 2]])
eigenvalues = A.eigenvalues()
```

## Matrix Properties

```python
A.is_square()           # Check if square
A.is_symmetric()        # Check if symmetric
A.is_diagonal()         # Check if diagonal
A.is_upper_triangular() # Check if upper triangular
A.is_lower_triangular() # Check if lower triangular
```

## Vector Utilities

```python
from matrix_utils import dot, cross, vector_norm, normalize, angle_between

# Dot product
dot([1, 2, 3], [4, 5, 6])  # Returns 32

# Cross product (3D vectors only)
cross([1, 0, 0], [0, 1, 0])  # Returns [0, 0, 1]

# Vector norms
vector_norm([3, 4])        # 2-norm: 5.0
vector_norm([3, -4], 1)    # 1-norm: 7.0
vector_norm([3, -4], 'inf') # inf-norm: 4.0

# Normalize vector
normalize([3, 4])  # Returns [0.6, 0.8]

# Angle between vectors (radians)
angle_between([1, 0, 0], [0, 1, 0])  # Returns pi/2

# Gram-Schmidt orthonormalization
gram_schmidt([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
```

## API Reference

### Matrix Class

| Method | Description |
|--------|-------------|
| `Matrix(data)` | Create from 2D list |
| `zeros(rows, cols)` | Zero matrix |
| `ones(rows, cols)` | Matrix of ones |
| `identity(n)` | Identity matrix |
| `diagonal(values)` | Diagonal matrix |
| `random(rows, cols, low, high)` | Random matrix |
| `hilbert(n)` | Hilbert matrix |
| `vandermonde(values)` | Vandermonde matrix |
| `transpose()` | Transpose |
| `trace()` | Trace |
| `determinant()` | Determinant |
| `inverse()` | Matrix inverse |
| `rank()` | Matrix rank |
| `solve(b)` | Solve linear system |
| `norm(p)` | Matrix norm |
| `qr_decompose()` | QR decomposition |
| `cholesky()` | Cholesky decomposition |
| `eigenvalues()` | Compute eigenvalues |

### Vector Functions

| Function | Description |
|----------|-------------|
| `dot(a, b)` | Dot product |
| `cross(a, b)` | Cross product (3D) |
| `vector_norm(v, p)` | Vector norm |
| `normalize(v)` | Normalize vector |
| `angle_between(a, b)` | Angle in radians |
| `is_orthogonal(a, b)` | Check orthogonality |
| `gram_schmidt(vectors)` | Orthonormalize |

## License

MIT License