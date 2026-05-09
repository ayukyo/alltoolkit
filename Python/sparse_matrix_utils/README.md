# Sparse Matrix Utils

A zero-dependency, production-ready sparse matrix utility module for Python.

## Overview

This module provides efficient sparse matrix implementations with multiple storage formats:

- **COO (Coordinate)**: Also known as 'ijv' or 'triplet' format. Best for incremental construction.
- **CSR (Compressed Sparse Row)**: Best for row slicing and matrix-vector products.
- **CSC (Compressed Sparse Column)**: Best for column slicing and transpose operations.

## Features

### Storage Formats
- `COOMatrix`: Coordinate format with (row, col, value) tuples
- `CSRMatrix`: Compressed Sparse Row format with row pointers
- `CSCMatrix`: Compressed Sparse Column format with column pointers

### Core Operations
- Format conversions (COO ↔ CSR ↔ CSC ↔ Dense)
- Matrix arithmetic (add, multiply, scale)
- Matrix-vector multiplication
- Transpose operations
- Element-wise (Hadamard) product

### Utility Functions
- Create from dense matrices or dictionaries
- Diagonal and identity matrix generation
- Sum, trace, and Frobenius norm
- Density and sparsity calculations

## Installation

No external dependencies required. Just copy the module to your project.

```python
from sparse_matrix_utils.mod import (
    COOMatrix, CSRMatrix, CSCMatrix, SparseMatrixUtils
)
```

## Quick Start

### Creating a Sparse Matrix

```python
# From dense matrix
from mod import from_dense

dense = [[1, 0, 2], [0, 3, 0], [4, 0, 5]]
sparse = from_dense(dense, 'csr')

# Incrementally (COO format)
from mod import COOMatrix

coo = COOMatrix((100, 100))
coo.add(0, 0, 1.5)
coo.add(50, 50, 2.5)
coo.add(99, 99, 3.5)

# From dictionary
from mod import from_dict

data = {(0, 0): 1, (10, 20): 2, (50, 50): 3}
sparse = from_dict(data, (100, 100), 'csr')
```

### Special Matrices

```python
from mod import identity, diagonal, zeros

# Identity matrix
I = identity(5, 'csr')

# Diagonal matrix
D = diagonal([1, 2, 3, 4, 5], 'csr')

# Zero matrix
Z = zeros((10, 10), 'csr')
```

### Arithmetic Operations

```python
from mod import SparseMatrixUtils

A = from_dense([[1, 0, 2], [0, 3, 0]], 'csr')
B = from_dense([[0, 5], [6, 0], [0, 7]], 'csr')

# Addition (same dimensions)
C = SparseMatrixUtils.add(A, from_dense([[1, 0, 0], [0, 1, 0]], 'csr'))

# Matrix multiplication
D = SparseMatrixUtils.multiply(A, B)  # (2x3) × (3x2) = (2x2)

# Scaling
E = SparseMatrixUtils.scale(A, 2.0)

# Element-wise product
F = SparseMatrixUtils.element_wise_multiply(A, A)
```

### Matrix-Vector Multiplication

```python
from mod import CSRMatrix

csr = from_dense([[1, 0, 2], [0, 3, 0], [4, 0, 5]], 'csr')
vector = [1.0, 2.0, 3.0]

result = csr.matvec(vector)
# result = [7.0, 6.0, 19.0]
```

### Properties and Analysis

```python
from mod import SparseMatrixUtils

sparse = from_dense([[1, 0, 0], [0, 2, 0], [0, 0, 3]], 'csr')

# Statistics
print(f"Sum: {SparseMatrixUtils.sum(sparse)}")        # 6.0
print(f"Trace: {SparseMatrixUtils.trace(sparse)}")    # 6.0
print(f"Frobenius norm: {SparseMatrixUtils.frobenius_norm(sparse)}")  # 3.46...

# Sparsity analysis
print(f"Density: {SparseMatrixUtils.density(sparse):.2%}")  # 33.33%
print(f"Sparsity: {SparseMatrixUtils.sparsity(sparse):.2%}") # 66.67%
```

### Format Conversions

```python
# COO to CSR/CSC
coo = COOMatrix((3, 3))
coo.add(0, 0, 1.0)
csr = coo.to_csr()
csc = coo.to_csc()

# CSR to Dense/CSC
dense = csr.to_dense()
csc = csr.to_csc()

# CSC to Dense/CSR
dense = csc.to_dense()
csr = csc.to_csr()
```

## API Reference

### COOMatrix

| Method | Description |
|--------|-------------|
| `add(row, col, value)` | Add a non-zero element |
| `get(row, col)` | Get value at position |
| `set(row, col, value)` | Set value at position |
| `to_dense()` | Convert to dense matrix |
| `to_csr()` | Convert to CSR format |
| `to_csc()` | Convert to CSC format |
| `transpose()` | Return transpose |
| `nnz` | Number of non-zeros |
| `shape` | Matrix dimensions |

### CSRMatrix

| Method | Description |
|--------|-------------|
| `get(row, col)` | Get value at position |
| `get_row(row)` | Iterate over row entries |
| `matvec(vector)` | Matrix-vector multiply |
| `to_dense()` | Convert to dense matrix |
| `to_coo()` | Convert to COO format |
| `to_csc()` | Convert to CSC format |
| `transpose()` | Return transpose (as CSC) |
| `nnz` | Number of non-zeros |
| `shape` | Matrix dimensions |

### CSCMatrix

| Method | Description |
|--------|-------------|
| `get(row, col)` | Get value at position |
| `get_col(col)` | Iterate over column entries |
| `to_dense()` | Convert to dense matrix |
| `to_coo()` | Convert to COO format |
| `to_csr()` | Convert to CSR format |
| `transpose()` | Return transpose (as CSR) |
| `nnz` | Number of non-zeros |
| `shape` | Matrix dimensions |

### SparseMatrixUtils

| Static Method | Description |
|---------------|-------------|
| `from_dense(matrix, format)` | Create from dense |
| `from_dict(data, shape, format)` | Create from dict |
| `diagonal(values, format)` | Create diagonal matrix |
| `identity(n, format)` | Create identity matrix |
| `zeros(shape, format)` | Create zero matrix |
| `add(a, b)` | Add two matrices |
| `multiply(a, b)` | Matrix multiplication |
| `scale(matrix, scalar)` | Scale by scalar |
| `element_wise_multiply(a, b)` | Hadamard product |
| `sum(matrix)` | Sum all elements |
| `trace(matrix)` | Sum diagonal |
| `frobenius_norm(matrix)` | Frobenius norm |
| `density(matrix)` | Non-zero ratio |
| `sparsity(matrix)` | Zero ratio |

## Performance Considerations

### When to Use Each Format

| Format | Best For | Avoid For |
|--------|----------|-----------|
| **COO** | Incremental construction, format conversion, easy element access/modification | Arithmetic operations, matrix-vector products |
| **CSR** | Row slicing, matrix-vector products, arithmetic operations | Column slicing, frequent modification |
| **CSC** | Column slicing, transpose operations | Row slicing, matrix-vector products |

### Memory Efficiency

For a matrix with `nnz` non-zeros and dimensions `(m, n)`:

- **COO**: Stores `3 × nnz` values (rows, cols, values)
- **CSR**: Stores `(m + 1) + 2 × nnz` values (indptr + indices + values)
- **CSC**: Stores `(n + 1) + 2 × nnz` values (indptr + indices + values)

Sparse storage is efficient when `nnz << m × n` (low density).

## Testing

Run the test suite:

```bash
python sparse_matrix_utils_test.py
```

## Examples

Run all examples:

```bash
python examples.py
```

## License

MIT License - Part of AllToolkit project.

## Author

AllToolkit