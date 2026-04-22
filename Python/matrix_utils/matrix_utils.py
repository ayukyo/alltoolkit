"""
Matrix Utilities - Zero-dependency matrix operations library.

Provides comprehensive matrix operations including:
- Basic operations (add, subtract, multiply, transpose)
- Advanced operations (determinant, inverse, rank)
- Decompositions (LU, QR, Cholesky)
- Solving linear systems
- Eigenvalue computation (power iteration)
- Matrix norms and properties
"""

from typing import List, Tuple, Optional, Union
import math
import random

Number = Union[int, float]


class Matrix:
    """A zero-dependency matrix class with comprehensive operations."""
    
    def __init__(self, data: List[List[Number]]):
        """
        Initialize matrix from 2D list.
        
        Args:
            data: 2D list of numbers
        
        Raises:
            ValueError: If data is empty or rows have inconsistent lengths
        """
        if not data or not data[0]:
            raise ValueError("Matrix data cannot be empty")
        
        row_len = len(data[0])
        for i, row in enumerate(data):
            if len(row) != row_len:
                raise ValueError(f"Row {i} has inconsistent length")
        
        self._data = [[float(x) for x in row] for row in data]
        self._rows = len(data)
        self._cols = row_len
    
    @property
    def rows(self) -> int:
        """Number of rows."""
        return self._rows
    
    @property
    def cols(self) -> int:
        """Number of columns."""
        return self._cols
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Matrix shape as (rows, cols)."""
        return (self._rows, self._cols)
    
    def __repr__(self) -> str:
        return f"Matrix({self._rows}x{self._cols})"
    
    def __str__(self) -> str:
        """Pretty print matrix."""
        max_width = max(len(f"{x:.6g}") for row in self._data for x in row)
        lines = []
        for row in self._data:
            line = " ".join(f"{x:>{max_width}.6g}" for x in row)
            lines.append(f"[{line}]")
        return "\n".join(lines)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return False
        return self._data == other._data
    
    def __getitem__(self, key: Union[int, Tuple[int, int]]) -> Union[List[float], float]:
        """Get element or row by index."""
        if isinstance(key, tuple):
            i, j = key
            return self._data[i][j]
        return self._data[key].copy()
    
    def __setitem__(self, key: Tuple[int, int], value: Number) -> None:
        """Set element by index."""
        i, j = key
        self._data[i][j] = float(value)
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Matrix addition."""
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} + {other.shape}")
        result = [[self._data[i][j] + other._data[i][j] 
                   for j in range(self._cols)] 
                  for i in range(self._rows)]
        return Matrix(result)
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Matrix subtraction."""
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} - {other.shape}")
        result = [[self._data[i][j] - other._data[i][j] 
                   for j in range(self._cols)] 
                  for i in range(self._rows)]
        return Matrix(result)
    
    def __mul__(self, other: Union['Matrix', Number]) -> 'Matrix':
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            result = [[self._data[i][j] * other 
                       for j in range(self._cols)] 
                      for i in range(self._rows)]
            return Matrix(result)
        
        # Matrix multiplication
        if self._cols != other._rows:
            raise ValueError(f"Cannot multiply {self.shape} by {other.shape}")
        
        result = [[sum(self._data[i][k] * other._data[k][j] 
                       for k in range(self._cols))
                   for j in range(other._cols)] 
                  for i in range(self._rows)]
        return Matrix(result)
    
    def __rmul__(self, other: Number) -> 'Matrix':
        """Right scalar multiplication."""
        return self * other
    
    def __neg__(self) -> 'Matrix':
        """Negate all elements."""
        return Matrix([[-x for x in row] for row in self._data])
    
    def __pow__(self, n: int) -> 'Matrix':
        """Matrix power (only for square matrices)."""
        if not self.is_square():
            raise ValueError("Power operation requires square matrix")
        if n < 0:
            return self.inverse() ** (-n)
        if n == 0:
            return Matrix.identity(self._rows)
        if n == 1:
            return Matrix([row.copy() for row in self._data])
        
        # Binary exponentiation
        result = Matrix.identity(self._rows)
        base = Matrix([row.copy() for row in self._data])
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        return result
    
    def copy(self) -> 'Matrix':
        """Create a deep copy of the matrix."""
        return Matrix([row.copy() for row in self._data])
    
    def to_list(self) -> List[List[float]]:
        """Convert to 2D list."""
        return [row.copy() for row in self._data]
    
    def is_square(self) -> bool:
        """Check if matrix is square."""
        return self._rows == self._cols
    
    def is_symmetric(self) -> bool:
        """Check if matrix is symmetric."""
        if not self.is_square():
            return False
        for i in range(self._rows):
            for j in range(i + 1, self._cols):
                if abs(self._data[i][j] - self._data[j][i]) > 1e-10:
                    return False
        return True
    
    def is_diagonal(self) -> bool:
        """Check if matrix is diagonal."""
        for i in range(self._rows):
            for j in range(self._cols):
                if i != j and abs(self._data[i][j]) > 1e-10:
                    return False
        return True
    
    def is_upper_triangular(self) -> bool:
        """Check if matrix is upper triangular."""
        for i in range(self._rows):
            for j in range(min(i, self._cols)):
                if abs(self._data[i][j]) > 1e-10:
                    return False
        return True
    
    def is_lower_triangular(self) -> bool:
        """Check if matrix is lower triangular."""
        for i in range(self._rows):
            for j in range(i + 1, self._cols):
                if abs(self._data[i][j]) > 1e-10:
                    return False
        return True
    
    def transpose(self) -> 'Matrix':
        """Return transpose of matrix."""
        result = [[self._data[j][i] for j in range(self._rows)] 
                  for i in range(self._cols)]
        return Matrix(result)
    
    def trace(self) -> float:
        """Calculate trace (sum of diagonal elements)."""
        if not self.is_square():
            raise ValueError("Trace requires square matrix")
        return sum(self._data[i][i] for i in range(self._rows))
    
    def determinant(self) -> float:
        """
        Calculate determinant using LU decomposition.
        
        Returns:
            Determinant value
            
        Raises:
            ValueError: If matrix is not square
        """
        if not self.is_square():
            raise ValueError("Determinant requires square matrix")
        
        n = self._rows
        if n == 1:
            return self._data[0][0]
        if n == 2:
            return self._data[0][0] * self._data[1][1] - self._data[0][1] * self._data[1][0]
        
        # Use LU decomposition
        lu, pivot = self._lu_decompose()
        det = 1.0
        for i in range(n):
            det *= lu._data[i][i]
        
        # Count row swaps parity
        # A swap of two elements changes permutation parity
        # We need to track the sign of the permutation
        visited = [False] * n
        swap_count = 0
        for i in range(n):
            if not visited[i]:
                cycle_len = 0
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = pivot[j]
                    cycle_len += 1
                if cycle_len > 1:
                    swap_count += cycle_len - 1
        
        if swap_count % 2 == 1:
            det = -det
        
        return det
    
    def _lu_decompose(self) -> Tuple['Matrix', List[int]]:
        """
        LU decomposition with partial pivoting.
        
        Returns:
            Tuple of (LU matrix, pivot indices)
        """
        n = self._rows
        lu = self.copy()
        pivot = list(range(n))
        
        for k in range(n - 1):
            # Find pivot
            max_val = abs(lu._data[k][k])
            max_idx = k
            for i in range(k + 1, n):
                if abs(lu._data[i][k]) > max_val:
                    max_val = abs(lu._data[i][k])
                    max_idx = i
            
            # Swap rows
            if max_idx != k:
                lu._data[k], lu._data[max_idx] = lu._data[max_idx], lu._data[k]
                pivot[k], pivot[max_idx] = pivot[max_idx], pivot[k]
            
            # Eliminate
            if abs(lu._data[k][k]) < 1e-15:
                continue
            
            for i in range(k + 1, n):
                factor = lu._data[i][k] / lu._data[k][k]
                lu._data[i][k] = factor
                for j in range(k + 1, n):
                    lu._data[i][j] -= factor * lu._data[k][j]
        
        return lu, pivot
    
    def inverse(self) -> 'Matrix':
        """
        Calculate matrix inverse using Gauss-Jordan elimination.
        
        Returns:
            Inverse matrix
            
        Raises:
            ValueError: If matrix is singular or not square
        """
        if not self.is_square():
            raise ValueError("Inverse requires square matrix")
        
        n = self._rows
        # Augment with identity
        aug = [row.copy() + [1.0 if i == j else 0.0 for j in range(n)] 
               for i, row in enumerate(self._data)]
        
        # Forward elimination with pivoting
        for col in range(n):
            # Find pivot
            max_val = abs(aug[col][col])
            max_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > max_val:
                    max_val = abs(aug[row][col])
                    max_row = row
            
            # Swap rows
            aug[col], aug[max_row] = aug[max_row], aug[col]
            
            if abs(aug[col][col]) < 1e-15:
                raise ValueError("Matrix is singular, cannot invert")
            
            # Scale pivot row
            pivot = aug[col][col]
            for j in range(2 * n):
                aug[col][j] /= pivot
            
            # Eliminate column
            for row in range(n):
                if row != col:
                    factor = aug[row][col]
                    for j in range(2 * n):
                        aug[row][j] -= factor * aug[col][j]
        
        # Extract inverse
        result = [[aug[i][j + n] for j in range(n)] for i in range(n)]
        return Matrix(result)
    
    def rank(self) -> int:
        """
        Calculate matrix rank using row echelon form.
        
        Returns:
            Rank of the matrix
        """
        m = self.copy()
        rows, cols = self._rows, self._cols
        rank = 0
        
        for col in range(cols):
            # Find pivot
            pivot_row = None
            for row in range(rank, rows):
                if abs(m._data[row][col]) > 1e-10:
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue
            
            # Swap rows
            m._data[rank], m._data[pivot_row] = m._data[pivot_row], m._data[rank]
            
            # Eliminate below
            for row in range(rank + 1, rows):
                if abs(m._data[row][col]) > 1e-10:
                    factor = m._data[row][col] / m._data[rank][col]
                    for j in range(col, cols):
                        m._data[row][j] -= factor * m._data[rank][j]
            
            rank += 1
        
        return rank
    
    def solve(self, b: 'Matrix') -> 'Matrix':
        """
        Solve linear system Ax = b.
        
        Args:
            b: Right-hand side column vector (n x 1)
            
        Returns:
            Solution column vector x
            
        Raises:
            ValueError: If system cannot be solved
        """
        if self._rows != self._cols:
            raise ValueError("Solve requires square matrix")
        if b._rows != self._rows or b._cols != 1:
            raise ValueError(f"b must be {self._rows}x1 matrix")
        
        n = self._rows
        lu, pivot = self._lu_decompose()
        
        # Permute b
        b_permuted = [b._data[pivot[i]][0] for i in range(n)]
        
        # Forward substitution (Ly = Pb)
        y = [0.0] * n
        for i in range(n):
            y[i] = b_permuted[i]
            for j in range(i):
                y[i] -= lu._data[i][j] * y[j]
        
        # Back substitution (Ux = y)
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= lu._data[i][j] * x[j]
            if abs(lu._data[i][i]) < 1e-15:
                raise ValueError("Matrix is singular")
            x[i] /= lu._data[i][i]
        
        return Matrix([[xi] for xi in x])
    
    def norm(self, p: int = 2) -> float:
        """
        Calculate matrix norm.
        
        Args:
            p: Norm type (1, 2, or 'fro' for Frobenius)
            
        Returns:
            Norm value
        """
        if p == 1:
            # 1-norm (max column sum)
            return max(sum(abs(self._data[i][j]) for i in range(self._rows)) 
                       for j in range(self._cols))
        
        if p == float('inf') or p == 'inf':
            # Infinity norm (max row sum)
            return max(sum(abs(x) for x in row) for row in self._data)
        
        # Frobenius norm
        return math.sqrt(sum(x * x for row in self._data for x in row))
    
    def frobenius_norm(self) -> float:
        """Calculate Frobenius norm."""
        return self.norm()
    
    def eigenvalues(self, max_iter: int = 1000, tol: float = 1e-10) -> List[float]:
        """
        Compute eigenvalues using QR algorithm.
        
        Args:
            max_iter: Maximum iterations
            tol: Convergence tolerance
            
        Returns:
            List of eigenvalues (approximate)
        """
        if not self.is_square():
            raise ValueError("Eigenvalues require square matrix")
        
        n = self._rows
        a = self.copy()
        
        for _ in range(max_iter):
            q, r = a.qr_decompose()
            a = r * q
            
            # Check convergence (off-diagonal elements)
            off_diag = sum(abs(a._data[i][j]) 
                          for i in range(n) 
                          for j in range(n) if i != j)
            if off_diag < tol:
                break
        
        return [a._data[i][i] for i in range(n)]
    
    def qr_decompose(self) -> Tuple['Matrix', 'Matrix']:
        """
        QR decomposition using Gram-Schmidt.
        
        Returns:
            Tuple of (Q, R) where A = QR
        """
        n = self._rows
        m = self._cols
        
        # Gram-Schmidt orthogonalization
        # Q will be n x min(n, m), R will be min(n, m) x m
        k = min(n, m)
        
        q_data = [[0.0] * k for _ in range(n)]
        r_data = [[0.0] * m for _ in range(k)]
        
        for j in range(k):
            # Get column j of A
            v = [self._data[i][j] for i in range(n)]
            
            for i in range(j):
                r_data[i][j] = sum(q_data[l][i] * self._data[l][j] for l in range(n))
                v = [v[l] - r_data[i][j] * q_data[l][i] for l in range(n)]
            
            r_data[j][j] = math.sqrt(sum(x * x for x in v))
            
            if r_data[j][j] > 1e-15:
                for l in range(n):
                    q_data[l][j] = v[l] / r_data[j][j]
        
        q_matrix = Matrix(q_data)
        r_matrix = Matrix(r_data)
        
        return q_matrix, r_matrix
    
    def cholesky(self) -> 'Matrix':
        """
        Cholesky decomposition for symmetric positive definite matrices.
        
        Returns:
            Lower triangular matrix L such that A = LL^T
            
        Raises:
            ValueError: If matrix is not symmetric positive definite
        """
        if not self.is_square():
            raise ValueError("Cholesky requires square matrix")
        if not self.is_symmetric():
            raise ValueError("Cholesky requires symmetric matrix")
        
        n = self._rows
        l = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1):
                s = sum(l[i][k] * l[j][k] for k in range(j))
                
                if i == j:
                    val = self._data[i][i] - s
                    if val <= 0:
                        raise ValueError("Matrix is not positive definite")
                    l[i][j] = math.sqrt(val)
                else:
                    l[i][j] = (self._data[i][j] - s) / l[j][j]
        
        return Matrix(l)
    
    def get_row(self, i: int) -> List[float]:
        """Get row i as a list."""
        return self._data[i].copy()
    
    def get_col(self, j: int) -> List[float]:
        """Get column j as a list."""
        return [self._data[i][j] for i in range(self._rows)]
    
    def set_row(self, i: int, values: List[Number]) -> None:
        """Set row i values."""
        if len(values) != self._cols:
            raise ValueError(f"Row must have {self._cols} elements")
        self._data[i] = [float(x) for x in values]
    
    def set_col(self, j: int, values: List[Number]) -> None:
        """Set column j values."""
        if len(values) != self._rows:
            raise ValueError(f"Column must have {self._rows} elements")
        for i in range(self._rows):
            self._data[i][j] = float(values[i])
    
    def submatrix(self, row_start: int, row_end: int, 
                  col_start: int, col_end: int) -> 'Matrix':
        """Extract submatrix."""
        result = [[self._data[i][j] for j in range(col_start, col_end)] 
                  for i in range(row_start, row_end)]
        return Matrix(result)
    
    def minor(self, i: int, j: int) -> 'Matrix':
        """Get matrix with row i and column j removed."""
        result = [[self._data[r][c] for c in range(self._cols) if c != j] 
                  for r in range(self._rows) if r != i]
        return Matrix(result) if result else Matrix([[0.0]])
    
    def cofactor(self, i: int, j: int) -> float:
        """Calculate cofactor C[i][j]."""
        minor_det = self.minor(i, j).determinant()
        return minor_det * ((-1) ** (i + j))
    
    def adjugate(self) -> 'Matrix':
        """Calculate adjugate (adjoint) matrix."""
        if not self.is_square():
            raise ValueError("Adjugate requires square matrix")
        
        n = self._rows
        result = [[self.cofactor(j, i) for j in range(n)] for i in range(n)]
        return Matrix(result)
    
    # Static factory methods
    @staticmethod
    def zeros(rows: int, cols: Optional[int] = None) -> 'Matrix':
        """Create zero matrix."""
        cols = cols or rows
        return Matrix([[0.0] * cols for _ in range(rows)])
    
    @staticmethod
    def ones(rows: int, cols: Optional[int] = None) -> 'Matrix':
        """Create matrix of ones."""
        cols = cols or rows
        return Matrix([[1.0] * cols for _ in range(rows)])
    
    @staticmethod
    def identity(n: int) -> 'Matrix':
        """Create n x n identity matrix."""
        return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])
    
    @staticmethod
    def diagonal(values: List[Number]) -> 'Matrix':
        """Create diagonal matrix from values."""
        n = len(values)
        return Matrix([[float(values[i]) if i == j else 0.0 for j in range(n)] 
                       for i in range(n)])
    
    @staticmethod
    def random(rows: int, cols: Optional[int] = None, 
               low: float = 0.0, high: float = 1.0) -> 'Matrix':
        """Create matrix with random values."""
        cols = cols or rows
        return Matrix([[random.uniform(low, high) for _ in range(cols)] 
                       for _ in range(rows)])
    
    @staticmethod
    def from_rows(*rows: List[Number]) -> 'Matrix':
        """Create matrix from row vectors."""
        return Matrix([list(row) for row in rows])
    
    @staticmethod
    def from_cols(*cols: List[Number]) -> 'Matrix':
        """Create matrix from column vectors."""
        n = len(cols[0])
        for col in cols:
            if len(col) != n:
                raise ValueError("All columns must have same length")
        return Matrix([[col[i] for col in cols] for i in range(n)])
    
    @staticmethod
    def hilbert(n: int) -> 'Matrix':
        """Create Hilbert matrix (H[i][j] = 1/(i+j+1))."""
        return Matrix([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
    
    @staticmethod
    def vandermonde(values: List[Number]) -> 'Matrix':
        """Create Vandermonde matrix."""
        n = len(values)
        return Matrix([[float(values[i]) ** j for j in range(n)] for i in range(n)])


# Utility functions

def dot(a: List[float], b: List[float]) -> float:
    """Dot product of two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(x * y for x, y in zip(a, b))


def cross(a: List[float], b: List[float]) -> List[float]:
    """Cross product of two 3D vectors."""
    if len(a) != 3 or len(b) != 3:
        raise ValueError("Cross product requires 3D vectors")
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]


def vector_norm(v: List[float], p: int = 2) -> float:
    """Calculate vector norm."""
    if p == float('inf') or p == 'inf':
        return max(abs(x) for x in v)
    if p == 1:
        return sum(abs(x) for x in v)
    return sum(x ** p for x in v) ** (1.0 / p)


def normalize(v: List[float]) -> List[float]:
    """Normalize vector to unit length."""
    norm = vector_norm(v)
    if norm < 1e-15:
        raise ValueError("Cannot normalize zero vector")
    return [x / norm for x in v]


def angle_between(a: List[float], b: List[float]) -> float:
    """Calculate angle between two vectors in radians."""
    cos_angle = dot(a, b) / (vector_norm(a) * vector_norm(b))
    cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp for numerical stability
    return math.acos(cos_angle)


def is_orthogonal(a: List[float], b: List[float], tol: float = 1e-10) -> bool:
    """Check if two vectors are orthogonal."""
    return abs(dot(a, b)) < tol


def gram_schmidt(vectors: List[List[float]]) -> List[List[float]]:
    """Apply Gram-Schmidt orthogonalization to a set of vectors."""
    result = []
    for v in vectors:
        u = v.copy()
        for w in result:
            proj = dot(u, w) / dot(w, w)
            u = [ui - proj * wi for ui, wi in zip(u, w)]
        norm = vector_norm(u)
        if norm > 1e-10:
            result.append([ui / norm for ui in u])
    return result