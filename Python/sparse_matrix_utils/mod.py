"""
AllToolkit - Python Sparse Matrix Utilities

A zero-dependency, production-ready sparse matrix utility module.
Supports multiple storage formats (COO, CSR, CSC), conversions,
and efficient arithmetic operations on sparse matrices.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, Union, Iterator
from collections import defaultdict


class COOMatrix:
    """
    Sparse Matrix in COOrdinate format (COO).
    
    Also known as the 'ijv' or 'triplet' format.
    Stores non-zero elements as (row, col, value) tuples.
    
    Best for:
    - Incremental matrix construction
    - Converting between formats
    - Easy element access and modification
    
    Attributes:
        rows: List of row indices
        cols: List of column indices
        values: List of non-zero values
        shape: Tuple of (n_rows, n_cols)
    """

    def __init__(self, shape: Tuple[int, int]):
        """
        Initialize an empty COO matrix.

        Args:
            shape: Tuple of (n_rows, n_cols)
        """
        if shape[0] <= 0 or shape[1] <= 0:
            raise ValueError("Matrix dimensions must be positive")
        
        self._shape = shape
        self._rows: List[int] = []
        self._cols: List[int] = []
        self._values: List[float] = []

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape

    @property
    def rows(self) -> List[int]:
        return self._rows.copy()

    @property
    def cols(self) -> List[int]:
        return self._cols.copy()

    @property
    def values(self) -> List[float]:
        return self._values.copy()

    @property
    def nnz(self) -> int:
        """Number of non-zero elements."""
        return len(self._values)

    def add(self, row: int, col: int, value: float) -> None:
        """
        Add a non-zero element to the matrix.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            value: Non-zero value

        Raises:
            IndexError: If indices are out of bounds
            ValueError: If value is zero
        """
        if row < 0 or row >= self._shape[0]:
            raise IndexError(f"Row index {row} out of bounds")
        if col < 0 or col >= self._shape[1]:
            raise IndexError(f"Column index {col} out of bounds")
        
        if value == 0:
            return  # Don't store zeros
        
        self._rows.append(row)
        self._cols.append(col)
        self._values.append(float(value))

    def get(self, row: int, col: int) -> float:
        """
        Get the value at (row, col).

        Args:
            row: Row index
            col: Column index

        Returns:
            Value at (row, col), or 0.0 if not stored
        """
        for i, (r, c) in enumerate(zip(self._rows, self._cols)):
            if r == row and c == col:
                return self._values[i]
        return 0.0

    def set(self, row: int, col: int, value: float) -> None:
        """
        Set the value at (row, col).

        Args:
            row: Row index
            col: Column index
            value: Value to set
        """
        # Try to find existing entry
        for i, (r, c) in enumerate(zip(self._rows, self._cols)):
            if r == row and c == col:
                if value == 0:
                    # Remove entry
                    del self._rows[i]
                    del self._cols[i]
                    del self._values[i]
                else:
                    self._values[i] = float(value)
                return
        
        # Add new entry
        self.add(row, col, value)

    def to_dense(self) -> List[List[float]]:
        """Convert to dense matrix (2D list)."""
        result = [[0.0] * self._shape[1] for _ in range(self._shape[0])]
        for r, c, v in zip(self._rows, self._cols, self._values):
            result[r][c] = v
        return result

    def to_csr(self) -> 'CSRMatrix':
        """Convert to CSR format."""
        return CSRMatrix.from_coo(self)

    def to_csc(self) -> 'CSCMatrix':
        """Convert to CSC format."""
        return CSCMatrix.from_coo(self)

    def transpose(self) -> 'COOMatrix':
        """Return the transpose of the matrix."""
        result = COOMatrix((self._shape[1], self._shape[0]))
        for r, c, v in zip(self._rows, self._cols, self._values):
            result.add(c, r, v)
        return result

    def copy(self) -> 'COOMatrix':
        """Create a copy of the matrix."""
        result = COOMatrix(self._shape)
        result._rows = self._rows.copy()
        result._cols = self._cols.copy()
        result._values = self._values.copy()
        return result

    def __repr__(self) -> str:
        return f"COOMatrix(shape={self._shape}, nnz={self.nnz})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, COOMatrix):
            return False
        if self._shape != other._shape:
            return False
        return (set(zip(self._rows, self._cols, self._values)) ==
                set(zip(other._rows, other._cols, other._values)))


class CSRMatrix:
    """
    Sparse Matrix in Compressed Sparse Row format (CSR).
    
    Also known as CRS (Compressed Row Storage).
    
    Best for:
    - Row slicing
    - Matrix-vector multiplication
    - Arithmetic operations
    
    Attributes:
        indptr: Row pointer array (length = n_rows + 1)
        indices: Column indices array
        values: Non-zero values array
        shape: Tuple of (n_rows, n_cols)
    """

    def __init__(self, shape: Tuple[int, int], indptr: List[int], 
                 indices: List[int], values: List[float]):
        """
        Initialize a CSR matrix with pre-computed arrays.

        Args:
            shape: Tuple of (n_rows, n_cols)
            indptr: Row pointer array
            indices: Column indices array
            values: Non-zero values array
        """
        if len(indptr) != shape[0] + 1:
            raise ValueError("indptr length must be n_rows + 1")
        if len(indices) != len(values):
            raise ValueError("indices and values must have same length")
        
        self._shape = shape
        self._indptr = list(indptr)
        self._indices = list(indices)
        self._values = [float(v) for v in values]

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape

    @property
    def indptr(self) -> List[int]:
        return self._indptr.copy()

    @property
    def indices(self) -> List[int]:
        return self._indices.copy()

    @property
    def values(self) -> List[float]:
        return self._values.copy()

    @property
    def nnz(self) -> int:
        """Number of non-zero elements."""
        return len(self._values)

    @staticmethod
    def from_coo(coo: COOMatrix) -> 'CSRMatrix':
        """
        Create CSR matrix from COO format.

        Args:
            coo: COOMatrix to convert

        Returns:
            CSRMatrix equivalent
        """
        n_rows, n_cols = coo.shape
        
        # Group by row
        row_data = defaultdict(list)
        for r, c, v in zip(coo.rows, coo.cols, coo.values):
            row_data[r].append((c, v))
        
        # Build CSR arrays
        indptr = [0]
        indices = []
        values = []
        
        for i in range(n_rows):
            # Sort by column for each row
            row_entries = sorted(row_data[i], key=lambda x: x[0])
            for c, v in row_entries:
                indices.append(c)
                values.append(v)
            indptr.append(len(indices))
        
        return CSRMatrix((n_rows, n_cols), indptr, indices, values)

    @staticmethod
    def from_dense(matrix: List[List[float]]) -> 'CSRMatrix':
        """
        Create CSR matrix from dense matrix.

        Args:
            matrix: 2D list of values

        Returns:
            CSRMatrix equivalent
        """
        if not matrix:
            raise ValueError("Matrix cannot be empty")
        
        n_rows = len(matrix)
        n_cols = len(matrix[0]) if matrix else 0
        
        coo = COOMatrix((n_rows, n_cols))
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val != 0:
                    coo.add(i, j, val)
        
        return CSRMatrix.from_coo(coo)

    def get(self, row: int, col: int) -> float:
        """
        Get the value at (row, col).

        Args:
            row: Row index
            col: Column index

        Returns:
            Value at (row, col), or 0.0 if not stored
        """
        if row < 0 or row >= self._shape[0]:
            raise IndexError(f"Row index {row} out of bounds")
        if col < 0 or col >= self._shape[1]:
            raise IndexError(f"Column index {col} out of bounds")
        
        start = self._indptr[row]
        end = self._indptr[row + 1]
        
        # Binary search in sorted column indices
        for i in range(start, end):
            if self._indices[i] == col:
                return self._values[i]
        
        return 0.0

    def get_row(self, row: int) -> Iterator[Tuple[int, float]]:
        """
        Iterate over non-zero entries in a row.

        Args:
            row: Row index

        Yields:
            Tuples of (column, value) for non-zero entries
        """
        if row < 0 or row >= self._shape[0]:
            raise IndexError(f"Row index {row} out of bounds")
        
        start = self._indptr[row]
        end = self._indptr[row + 1]
        
        for i in range(start, end):
            yield (self._indices[i], self._values[i])

    def to_dense(self) -> List[List[float]]:
        """Convert to dense matrix (2D list)."""
        result = [[0.0] * self._shape[1] for _ in range(self._shape[0])]
        for i in range(self._shape[0]):
            for col, val in self.get_row(i):
                result[i][col] = val
        return result

    def to_coo(self) -> COOMatrix:
        """Convert to COO format."""
        result = COOMatrix(self._shape)
        for i in range(self._shape[0]):
            for col, val in self.get_row(i):
                result.add(i, col, val)
        return result

    def to_csc(self) -> 'CSCMatrix':
        """Convert to CSC format."""
        return CSCMatrix.from_csr(self)

    def matvec(self, vector: List[float]) -> List[float]:
        """
        Matrix-vector multiplication.

        Args:
            vector: Dense vector (length must equal n_cols)

        Returns:
            Result vector (length = n_rows)
        """
        if len(vector) != self._shape[1]:
            raise ValueError("Vector length must match number of columns")
        
        result = [0.0] * self._shape[0]
        for i in range(self._shape[0]):
            for col, val in self.get_row(i):
                result[i] += val * vector[col]
        
        return result

    def transpose(self) -> 'CSCMatrix':
        """
        Return the transpose of the matrix.
        
        Note: Returns CSC format as transpose of CSR is naturally CSC.
        """
        return self.to_csc()

    def __mul__(self, other: Union['CSRMatrix', List[float]]) -> Union['CSRMatrix', List[float]]:
        """Matrix multiplication with another matrix or vector."""
        if isinstance(other, list):
            return self.matvec(other)
        raise TypeError("Multiplication only supported with vectors")

    def __repr__(self) -> str:
        return f"CSRMatrix(shape={self._shape}, nnz={self.nnz})"


class CSCMatrix:
    """
    Sparse Matrix in Compressed Sparse Column format (CSC).
    
    Also known as CCS (Compressed Column Storage).
    
    Best for:
    - Column slicing
    - Matrix-vector multiplication (transpose)
    - Arithmetic operations on columns
    
    Attributes:
        indptr: Column pointer array (length = n_cols + 1)
        indices: Row indices array
        values: Non-zero values array
        shape: Tuple of (n_rows, n_cols)
    """

    def __init__(self, shape: Tuple[int, int], indptr: List[int],
                 indices: List[int], values: List[float]):
        """
        Initialize a CSC matrix with pre-computed arrays.

        Args:
            shape: Tuple of (n_rows, n_cols)
            indptr: Column pointer array
            indices: Row indices array
            values: Non-zero values array
        """
        if len(indptr) != shape[1] + 1:
            raise ValueError("indptr length must be n_cols + 1")
        if len(indices) != len(values):
            raise ValueError("indices and values must have same length")
        
        self._shape = shape
        self._indptr = list(indptr)
        self._indices = list(indices)
        self._values = [float(v) for v in values]

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape

    @property
    def indptr(self) -> List[int]:
        return self._indptr.copy()

    @property
    def indices(self) -> List[int]:
        return self._indices.copy()

    @property
    def values(self) -> List[float]:
        return self._values.copy()

    @property
    def nnz(self) -> int:
        """Number of non-zero elements."""
        return len(self._values)

    @staticmethod
    def from_coo(coo: COOMatrix) -> 'CSCMatrix':
        """
        Create CSC matrix from COO format.

        Args:
            coo: COOMatrix to convert

        Returns:
            CSCMatrix equivalent
        """
        n_rows, n_cols = coo.shape
        
        # Group by column
        col_data = defaultdict(list)
        for r, c, v in zip(coo.rows, coo.cols, coo.values):
            col_data[c].append((r, v))
        
        # Build CSC arrays
        indptr = [0]
        indices = []
        values = []
        
        for j in range(n_cols):
            # Sort by row for each column
            col_entries = sorted(col_data[j], key=lambda x: x[0])
            for r, v in col_entries:
                indices.append(r)
                values.append(v)
            indptr.append(len(indices))
        
        return CSCMatrix((n_rows, n_cols), indptr, indices, values)

    @staticmethod
    def from_csr(csr: CSRMatrix) -> 'CSCMatrix':
        """
        Create CSC matrix from CSR format.

        Args:
            csr: CSRMatrix to convert

        Returns:
            CSCMatrix equivalent
        """
        return CSCMatrix.from_coo(csr.to_coo())

    @staticmethod
    def from_dense(matrix: List[List[float]]) -> 'CSCMatrix':
        """
        Create CSC matrix from dense matrix.

        Args:
            matrix: 2D list of values

        Returns:
            CSCMatrix equivalent
        """
        if not matrix:
            raise ValueError("Matrix cannot be empty")
        
        n_rows = len(matrix)
        n_cols = len(matrix[0]) if matrix else 0
        
        coo = COOMatrix((n_rows, n_cols))
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val != 0:
                    coo.add(i, j, val)
        
        return CSCMatrix.from_coo(coo)

    def get(self, row: int, col: int) -> float:
        """
        Get the value at (row, col).

        Args:
            row: Row index
            col: Column index

        Returns:
            Value at (row, col), or 0.0 if not stored
        """
        if row < 0 or row >= self._shape[0]:
            raise IndexError(f"Row index {row} out of bounds")
        if col < 0 or col >= self._shape[1]:
            raise IndexError(f"Column index {col} out of bounds")
        
        start = self._indptr[col]
        end = self._indptr[col + 1]
        
        for i in range(start, end):
            if self._indices[i] == row:
                return self._values[i]
        
        return 0.0

    def get_col(self, col: int) -> Iterator[Tuple[int, float]]:
        """
        Iterate over non-zero entries in a column.

        Args:
            col: Column index

        Yields:
            Tuples of (row, value) for non-zero entries
        """
        if col < 0 or col >= self._shape[1]:
            raise IndexError(f"Column index {col} out of bounds")
        
        start = self._indptr[col]
        end = self._indptr[col + 1]
        
        for i in range(start, end):
            yield (self._indices[i], self._values[i])

    def to_dense(self) -> List[List[float]]:
        """Convert to dense matrix (2D list)."""
        result = [[0.0] * self._shape[1] for _ in range(self._shape[0])]
        for j in range(self._shape[1]):
            for row, val in self.get_col(j):
                result[row][j] = val
        return result

    def to_coo(self) -> COOMatrix:
        """Convert to COO format."""
        result = COOMatrix(self._shape)
        for j in range(self._shape[1]):
            for row, val in self.get_col(j):
                result.add(row, j, val)
        return result

    def to_csr(self) -> CSRMatrix:
        """Convert to CSR format."""
        return CSRMatrix.from_coo(self.to_coo())

    def transpose(self) -> CSRMatrix:
        """
        Return the transpose of the matrix.
        
        Note: Returns CSR format as transpose of CSC is naturally CSR.
        """
        return self.to_csr()

    def __repr__(self) -> str:
        return f"CSCMatrix(shape={self._shape}, nnz={self.nnz})"


class SparseMatrixUtils:
    """
    Utility class for sparse matrix operations.
    
    Provides static methods for:
    - Creating sparse matrices from various sources
    - Arithmetic operations
    - Conversions between formats
    - Matrix operations (multiply, add, transpose)
    """

    @staticmethod
    def from_dense(matrix: List[List[float]], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
        """
        Create sparse matrix from dense matrix.

        Args:
            matrix: 2D list of values
            format: Output format ('coo', 'csr', or 'csc')

        Returns:
            Sparse matrix in specified format

        Example:
            >>> matrix = [[1, 0, 2], [0, 0, 3], [4, 0, 0]]
            >>> sparse = SparseMatrixUtils.from_dense(matrix, 'csr')
            >>> sparse.nnz
            4
        """
        if not matrix:
            raise ValueError("Matrix cannot be empty")
        
        n_rows = len(matrix)
        n_cols = len(matrix[0]) if matrix else 0
        
        coo = COOMatrix((n_rows, n_cols))
        for i, row in enumerate(matrix):
            if len(row) != n_cols:
                raise ValueError("All rows must have the same length")
            for j, val in enumerate(row):
                if val != 0:
                    coo.add(i, j, val)
        
        if format == 'coo':
            return coo
        elif format == 'csr':
            return CSRMatrix.from_coo(coo)
        elif format == 'csc':
            return CSCMatrix.from_coo(coo)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def from_dict(data: dict, shape: Tuple[int, int], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
        """
        Create sparse matrix from dictionary.

        Args:
            data: Dictionary mapping (row, col) tuples to values
            shape: Tuple of (n_rows, n_cols)
            format: Output format ('coo', 'csr', or 'csc')

        Returns:
            Sparse matrix in specified format

        Example:
            >>> data = {(0, 0): 1, (0, 2): 2, (1, 1): 3}
            >>> sparse = SparseMatrixUtils.from_dict(data, (2, 3), 'csr')
        """
        coo = COOMatrix(shape)
        for (row, col), val in data.items():
            if val != 0:
                coo.add(row, col, val)
        
        if format == 'coo':
            return coo
        elif format == 'csr':
            return CSRMatrix.from_coo(coo)
        elif format == 'csc':
            return CSCMatrix.from_coo(coo)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def diagonal(values: List[float], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
        """
        Create a diagonal sparse matrix.

        Args:
            values: Diagonal values
            format: Output format ('coo', 'csr', or 'csc')

        Returns:
            Diagonal sparse matrix

        Example:
            >>> diag = SparseMatrixUtils.diagonal([1, 2, 3], 'csr')
            >>> diag.get(0, 0)
            1.0
        """
        n = len(values)
        coo = COOMatrix((n, n))
        for i, val in enumerate(values):
            if val != 0:
                coo.add(i, i, val)
        
        if format == 'coo':
            return coo
        elif format == 'csr':
            return CSRMatrix.from_coo(coo)
        elif format == 'csc':
            return CSCMatrix.from_coo(coo)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def identity(n: int, format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
        """
        Create an identity sparse matrix.

        Args:
            n: Size of the identity matrix (n x n)
            format: Output format ('coo', 'csr', or 'csc')

        Returns:
            Identity sparse matrix

        Example:
            >>> I = SparseMatrixUtils.identity(3, 'csr')
            >>> I.get(0, 0)
            1.0
        """
        return SparseMatrixUtils.diagonal([1.0] * n, format)

    @staticmethod
    def zeros(shape: Tuple[int, int], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
        """
        Create a zero sparse matrix.

        Args:
            shape: Tuple of (n_rows, n_cols)
            format: Output format ('coo', 'csr', or 'csc')

        Returns:
            Zero sparse matrix

        Example:
            >>> Z = SparseMatrixUtils.zeros((3, 3), 'csr')
            >>> Z.nnz
            0
        """
        coo = COOMatrix(shape)
        if format == 'coo':
            return coo
        elif format == 'csr':
            return CSRMatrix.from_coo(coo)
        elif format == 'csc':
            return CSCMatrix.from_coo(coo)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def add(a: Union[CSRMatrix, CSCMatrix, COOMatrix], 
            b: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> CSRMatrix:
        """
        Add two sparse matrices.

        Args:
            a: First sparse matrix
            b: Second sparse matrix

        Returns:
            Sum as CSR matrix

        Raises:
            ValueError: If shapes don't match

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 0], [0, 2]], 'csr')
            >>> B = SparseMatrixUtils.from_dense([[0, 3], [4, 0]], 'csr')
            >>> C = SparseMatrixUtils.add(A, B)
            >>> C.to_dense()
            [[1.0, 3.0], [4.0, 2.0]]
        """
        if a.shape != b.shape:
            raise ValueError("Matrix shapes must match for addition")
        
        # Convert to COO for easy addition
        a_coo = a.to_coo() if not isinstance(a, COOMatrix) else a
        b_coo = b.to_coo() if not isinstance(b, COOMatrix) else b
        
        result = COOMatrix(a.shape)
        
        # Add elements from a
        for r, c, v in zip(a_coo.rows, a_coo.cols, a_coo.values):
            result.add(r, c, v)
        
        # Add elements from b
        for r, c, v in zip(b_coo.rows, b_coo.cols, b_coo.values):
            current = result.get(r, c)
            result.set(r, c, current + v)
        
        return CSRMatrix.from_coo(result)

    @staticmethod
    def multiply(a: Union[CSRMatrix, CSCMatrix, COOMatrix],
                 b: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> CSRMatrix:
        """
        Multiply two sparse matrices.

        Args:
            a: First sparse matrix (m x k)
            b: Second sparse matrix (k x n)

        Returns:
            Product as CSR matrix (m x n)

        Raises:
            ValueError: If dimensions don't match

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
            >>> B = SparseMatrixUtils.from_dense([[5, 6], [7, 8]], 'csr')
            >>> C = SparseMatrixUtils.multiply(A, B)
            >>> C.to_dense()
            [[19.0, 22.0], [43.0, 50.0]]
        """
        if a.shape[1] != b.shape[0]:
            raise ValueError(
                f"Matrix dimensions don't match for multiplication: "
                f"{a.shape} x {b.shape}"
            )
        
        # Convert to CSR for efficient row access
        a_csr = a.to_csr() if not isinstance(a, CSRMatrix) else a
        b_csr = b.to_csr() if not isinstance(b, CSRMatrix) else b
        
        m, k, n = a.shape[0], a.shape[1], b.shape[1]
        result = COOMatrix((m, n))
        
        # For each row of a
        for i in range(m):
            # For each non-zero in row i of a
            for j, a_val in a_csr.get_row(i):
                # For each non-zero in row j of b
                for l, b_val in b_csr.get_row(j):
                    current = result.get(i, l)
                    result.set(i, l, current + a_val * b_val)
        
        return CSRMatrix.from_coo(result)

    @staticmethod
    def scale(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix], 
              scalar: float) -> CSRMatrix:
        """
        Scale a sparse matrix by a scalar.

        Args:
            matrix: Sparse matrix
            scalar: Scalar multiplier

        Returns:
            Scaled matrix as CSR

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 0], [0, 2]], 'csr')
            >>> B = SparseMatrixUtils.scale(A, 3)
            >>> B.to_dense()
            [[3.0, 0.0], [0.0, 6.0]]
        """
        coo = matrix.to_coo() if not isinstance(matrix, COOMatrix) else matrix
        result = COOMatrix(coo.shape)
        
        for r, c, v in zip(coo.rows, coo.cols, coo.values):
            result.add(r, c, v * scalar)
        
        return CSRMatrix.from_coo(result)

    @staticmethod
    def element_wise_multiply(a: Union[CSRMatrix, CSCMatrix, COOMatrix],
                              b: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> CSRMatrix:
        """
        Element-wise (Hadamard) product of two sparse matrices.

        Args:
            a: First sparse matrix
            b: Second sparse matrix

        Returns:
            Element-wise product as CSR matrix

        Raises:
            ValueError: If shapes don't match

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
            >>> B = SparseMatrixUtils.from_dense([[5, 0], [0, 6]], 'csr')
            >>> C = SparseMatrixUtils.element_wise_multiply(A, B)
            >>> C.to_dense()
            [[5.0, 0.0], [0.0, 24.0]]
        """
        if a.shape != b.shape:
            raise ValueError("Matrix shapes must match for element-wise multiplication")
        
        a_csr = a.to_csr() if not isinstance(a, CSRMatrix) else a
        b_csr = b.to_csr() if not isinstance(b, CSRMatrix) else b
        
        result = COOMatrix(a.shape)
        
        for i in range(a.shape[0]):
            # Get rows as dicts for faster lookup
            row_a = dict(a_csr.get_row(i))
            row_b = dict(b_csr.get_row(i))
            
            # Find common columns
            for col in set(row_a.keys()) & set(row_b.keys()):
                result.add(i, col, row_a[col] * row_b[col])
        
        return CSRMatrix.from_coo(result)

    @staticmethod
    def sum(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> float:
        """
        Sum all elements in the matrix.

        Args:
            matrix: Sparse matrix

        Returns:
            Sum of all elements

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
            >>> SparseMatrixUtils.sum(A)
            10.0
        """
        coo = matrix.to_coo() if not isinstance(matrix, COOMatrix) else matrix
        return sum(coo.values)

    @staticmethod
    def trace(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> float:
        """
        Compute the trace (sum of diagonal elements).

        Args:
            matrix: Sparse matrix

        Returns:
            Trace of the matrix

        Raises:
            ValueError: If matrix is not square

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 2], [3, 4]], 'csr')
            >>> SparseMatrixUtils.trace(A)
            5.0
        """
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square for trace")
        
        coo = matrix.to_coo() if not isinstance(matrix, COOMatrix) else matrix
        trace = 0.0
        for r, c, v in zip(coo.rows, coo.cols, coo.values):
            if r == c:
                trace += v
        return trace

    @staticmethod
    def frobenius_norm(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> float:
        """
        Compute the Frobenius norm of the matrix.

        Args:
            matrix: Sparse matrix

        Returns:
            Frobenius norm (square root of sum of squares)

        Example:
            >>> A = SparseMatrixUtils.from_dense([[3, 4]], 'csr')
            >>> SparseMatrixUtils.frobenius_norm(A)
            5.0
        """
        coo = matrix.to_coo() if not isinstance(matrix, COOMatrix) else matrix
        return sum(v * v for v in coo.values) ** 0.5

    @staticmethod
    def density(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> float:
        """
        Compute the density (ratio of non-zeros to total elements).

        Args:
            matrix: Sparse matrix

        Returns:
            Density between 0 and 1

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 0], [0, 0]], 'csr')
            >>> SparseMatrixUtils.density(A)
            0.25
        """
        coo = matrix.to_coo() if not isinstance(matrix, COOMatrix) else matrix
        total = coo.shape[0] * coo.shape[1]
        if total == 0:
            return 0.0
        return coo.nnz / total

    @staticmethod
    def sparsity(matrix: Union[CSRMatrix, CSCMatrix, COOMatrix]) -> float:
        """
        Compute the sparsity (ratio of zeros to total elements).

        Args:
            matrix: Sparse matrix

        Returns:
            Sparsity between 0 and 1

        Example:
            >>> A = SparseMatrixUtils.from_dense([[1, 0], [0, 0]], 'csr')
            >>> SparseMatrixUtils.sparsity(A)
            0.75
        """
        return 1.0 - SparseMatrixUtils.density(matrix)


# Convenience functions

def coo_matrix(shape: Tuple[int, int]) -> COOMatrix:
    """Create an empty COO matrix."""
    return COOMatrix(shape)


def csr_matrix(shape: Tuple[int, int]) -> CSRMatrix:
    """Create an empty CSR matrix."""
    coo = COOMatrix(shape)
    return CSRMatrix.from_coo(coo)


def csc_matrix(shape: Tuple[int, int]) -> CSCMatrix:
    """Create an empty CSC matrix."""
    coo = COOMatrix(shape)
    return CSCMatrix.from_coo(coo)


def from_dense(matrix: List[List[float]], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
    """Create sparse matrix from dense matrix."""
    return SparseMatrixUtils.from_dense(matrix, format)


def from_dict(data: dict, shape: Tuple[int, int], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
    """Create sparse matrix from dictionary."""
    return SparseMatrixUtils.from_dict(data, shape, format)


def diagonal(values: List[float], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
    """Create a diagonal sparse matrix."""
    return SparseMatrixUtils.diagonal(values, format)


def identity(n: int, format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
    """Create an identity sparse matrix."""
    return SparseMatrixUtils.identity(n, format)


def zeros(shape: Tuple[int, int], format: str = 'csr') -> Union[COOMatrix, CSRMatrix, CSCMatrix]:
    """Create a zero sparse matrix."""
    return SparseMatrixUtils.zeros(shape, format)