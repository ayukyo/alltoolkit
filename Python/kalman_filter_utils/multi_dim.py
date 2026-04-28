"""
Multi-Dimensional Kalman Filter Implementation.

A general-purpose Kalman filter for multi-dimensional state estimation.
"""

import math
from typing import List, Optional, Tuple


class Matrix:
    """Simple matrix class for Kalman filter operations."""
    
    def __init__(self, data: List[List[float]]):
        """Initialize matrix from 2D list."""
        if not data or not data[0]:
            self.rows = 0
            self.cols = 0
            self.data = []
        else:
            self.rows = len(data)
            self.cols = len(data[0])
            self.data = [row[:] for row in data]  # Deep copy
    
    @staticmethod
    def zeros(rows: int, cols: int) -> 'Matrix':
        """Create zeros matrix."""
        return Matrix([[0.0] * cols for _ in range(rows)])
    
    @staticmethod
    def identity(n: int) -> 'Matrix':
        """Create identity matrix."""
        return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])
    
    @staticmethod
    def diagonal(values: List[float]) -> 'Matrix':
        """Create diagonal matrix."""
        n = len(values)
        return Matrix([[values[i] if i == j else 0.0 for j in range(n)] for i in range(n)])
    
    def copy(self) -> 'Matrix':
        """Create a copy of the matrix."""
        return Matrix(self.data)
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Matrix addition."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Matrix subtraction."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])
    
    def __mul__(self, other):
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            return Matrix([[other * x for x in row] for row in self.data])
        elif isinstance(other, Matrix):
            # Matrix multiplication
            if self.cols != other.rows:
                raise ValueError("Matrix dimensions incompatible for multiplication")
            result = Matrix.zeros(self.rows, other.cols)
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result.data[i][j] += self.data[i][k] * other.data[k][j]
            return result
        elif isinstance(other, Vector):
            # Matrix-vector multiplication
            if self.cols != other.dim:
                raise ValueError("Matrix columns must match Vector dimension")
            result = [0.0] * self.rows
            for i in range(self.rows):
                for j in range(self.cols):
                    result[i] += self.data[i][j] * other.data[j]
            return Vector(result)
        else:
            raise TypeError(f"Cannot multiply Matrix by {type(other)}")
    
    def __rmul__(self, scalar: float) -> 'Matrix':
        """Scalar multiplication (right side)."""
        return Matrix([[scalar * x for x in row] for row in self.data])
    
    def transpose(self) -> 'Matrix':
        """Matrix transpose."""
        return Matrix([[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)])
    
    def inverse(self) -> 'Matrix':
        """
        Matrix inverse using Gauss-Jordan elimination.
        Works for any invertible matrix.
        """
        if self.rows != self.cols:
            raise ValueError("Can only invert square matrices")
        
        n = self.rows
        # Create augmented matrix [A | I]
        aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] 
               for i, row in enumerate(self.data)]
        
        # Forward elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(aug[k][i]) > abs(aug[max_row][i]):
                    max_row = k
            aug[i], aug[max_row] = aug[max_row], aug[i]
            
            pivot = aug[i][i]
            if abs(pivot) < 1e-12:
                # Matrix is singular, use pseudo-inverse approximation
                pivot = 1e-12 if pivot >= 0 else -1e-12
            
            # Scale pivot row
            for j in range(2 * n):
                aug[i][j] /= pivot
            
            # Eliminate column
            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(2 * n):
                        aug[k][j] -= factor * aug[i][j]
        
        # Extract inverse
        return Matrix([row[n:] for row in aug])
    
    def det(self) -> float:
        """Calculate determinant using LU decomposition."""
        if self.rows != self.cols:
            raise ValueError("Determinant only defined for square matrices")
        
        n = self.rows
        # Create copy
        mat = [row[:] for row in self.data]
        
        det = 1.0
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(mat[k][i]) > abs(mat[max_row][i]):
                    max_row = k
            
            if max_row != i:
                mat[i], mat[max_row] = mat[max_row], mat[i]
                det *= -1
            
            pivot = mat[i][i]
            if abs(pivot) < 1e-12:
                return 0.0
            det *= pivot
            
            for k in range(i + 1, n):
                factor = mat[k][i] / pivot
                for j in range(i + 1, n):
                    mat[k][j] -= factor * mat[i][j]
        
        return det
    
    def trace(self) -> float:
        """Calculate trace (sum of diagonal elements)."""
        return sum(self.data[i][i] for i in range(min(self.rows, self.cols)))
    
    def get(self, i: int, j: int) -> float:
        """Get element at position."""
        return self.data[i][j]
    
    def set(self, i: int, j: int, value: float):
        """Set element at position."""
        self.data[i][j] = value
    
    def to_list(self) -> List[List[float]]:
        """Convert to 2D list."""
        return [row[:] for row in self.data]
    
    def __repr__(self) -> str:
        return f"Matrix({self.data})"


class Vector:
    """Simple vector class for state representations."""
    
    def __init__(self, data: List[float]):
        """Initialize vector from list."""
        self.data = data[:]
        self.dim = len(data)
    
    @staticmethod
    def zeros(n: int) -> 'Vector':
        """Create zero vector."""
        return Vector([0.0] * n)
    
    def copy(self) -> 'Vector':
        """Create copy of vector."""
        return Vector(self.data[:])
    
    def __add__(self, other: 'Vector') -> 'Vector':
        """Vector addition."""
        if self.dim != other.dim:
            raise ValueError("Vector dimensions must match")
        return Vector([self.data[i] + other.data[i] for i in range(self.dim)])
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        """Vector subtraction."""
        if self.dim != other.dim:
            raise ValueError("Vector dimensions must match")
        return Vector([self.data[i] - other.data[i] for i in range(self.dim)])
    
    def __mul__(self, other):
        """Vector-scalar multiplication or dot product."""
        if isinstance(other, (int, float)):
            return Vector([x * other for x in self.data])
        elif isinstance(other, Vector):
            if self.dim != other.dim:
                raise ValueError("Vector dimensions must match")
            return sum(self.data[i] * other.data[i] for i in range(self.dim))
        else:
            raise TypeError("Can multiply by scalar or Vector")
    
    def __getitem__(self, index: int) -> float:
        """Get element at index."""
        return self.data[index]
    
    def __setitem__(self, index: int, value: float):
        """Set element at index."""
        self.data[index] = value
    
    def __len__(self) -> int:
        """Return vector dimension."""
        return self.dim
    
    def __rmul__(self, scalar: float) -> 'Vector':
        """Scalar multiplication."""
        return Vector([scalar * x for x in self.data])
    
    def outer(self, other: 'Vector') -> Matrix:
        """Outer product."""
        return Matrix([[self.data[i] * other.data[j] for j in range(other.dim)] 
                       for i in range(self.dim)])
    
    def norm(self) -> float:
        """Euclidean norm."""
        return math.sqrt(sum(x * x for x in self.data))
    
    def normalize(self) -> 'Vector':
        """Normalize vector."""
        n = self.norm()
        if n < 1e-12:
            return Vector([0.0] * self.dim)
        return Vector([x / n for x in self.data])
    
    def to_list(self) -> List[float]:
        """Convert to list."""
        return self.data[:]
    
    def __repr__(self) -> str:
        return f"Vector({self.data})"


class MultiDimKalmanFilter:
    """
    Multi-dimensional Kalman Filter for general state estimation.
    
    This is a full implementation supporting arbitrary state and measurement
    dimensions, with customizable state transition and measurement matrices.
    
    Example:
        >>> # 2D position tracking with velocity
        >>> # State: [x, y, vx, vy]
        >>> kf = MultiDimKalmanFilter(
        ...     state=[0.0, 0.0, 1.0, 0.0],  # x, y, vx, vy
        ...     state_dim=4,
        ...     measurement_dim=2
        ... )
        >>> 
        >>> # Set state transition matrix (constant velocity model)
        >>> kf.set_F([[1, 0, 1, 0],
        ...           [0, 1, 0, 1],
        ...           [0, 0, 1, 0],
        ...           [0, 0, 0, 1]])
        >>> 
        >>> # Set measurement matrix (measure position only)
        >>> kf.set_H([[1, 0, 0, 0],
        ...           [0, 1, 0, 0]])
        >>> 
        >>> kf.update([1.1, 0.1])
    """
    
    def __init__(
        self,
        state: List[float],
        state_dim: int,
        measurement_dim: int,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1
    ):
        """
        Initialize multi-dimensional Kalman filter.
        
        Args:
            state: Initial state vector
            state_dim: Number of state variables
            measurement_dim: Number of measurement variables
            process_noise: Process noise variance (applied uniformly)
            measurement_noise: Measurement noise variance (applied uniformly)
        """
        self.state_dim = state_dim
        self.measurement_dim = measurement_dim
        
        # State vector
        self.x = Vector(state)
        
        # State transition matrix (default: identity)
        self.F = Matrix.identity(state_dim)
        
        # Measurement matrix (default: first measurement_dim elements)
        H_data = [[1.0 if i == j else 0.0 for j in range(state_dim)] 
                  for i in range(measurement_dim)]
        self.H = Matrix(H_data)
        
        # Process noise covariance
        self.Q = Matrix.identity(state_dim) * process_noise
        
        # Measurement noise covariance
        self.R = Matrix.identity(measurement_dim) * measurement_noise
        
        # Error covariance
        self.P = Matrix.identity(state_dim) * 1000.0
        
        # Control input matrix (optional)
        self.B: Optional[Matrix] = None
        self.u: Optional[Vector] = None
    
    def set_F(self, F: List[List[float]]):
        """Set state transition matrix."""
        self.F = Matrix(F)
    
    def set_H(self, H: List[List[float]]):
        """Set measurement matrix."""
        self.H = Matrix(H)
    
    def set_Q(self, Q: List[List[float]]):
        """Set process noise covariance matrix."""
        self.Q = Matrix(Q)
    
    def set_R(self, R: List[List[float]]):
        """Set measurement noise covariance matrix."""
        self.R = Matrix(R)
    
    def set_P(self, P: List[List[float]]):
        """Set error covariance matrix."""
        self.P = Matrix(P)
    
    def set_control(self, B: List[List[float]], u: List[float]):
        """Set control input matrix and control vector."""
        self.B = Matrix(B)
        self.u = Vector(u)
    
    def predict(self) -> Vector:
        """
        Predict step: project state and covariance forward.
        
        Returns:
            Predicted state vector
        """
        # State prediction: x = F * x + B * u
        self.x = self.F * self.x
        if self.B is not None and self.u is not None:
            control = self.B * self.u
            self.x = self.x + control
        
        # Covariance prediction: P = F * P * F^T + Q
        FP = self.F * self.P
        FPF_T = FP * self.F.transpose()
        self.P = FPF_T + self.Q
        
        return self.x.copy()
    
    def update(self, measurement: List[float]) -> Vector:
        """
        Update step: incorporate measurement.
        
        Args:
            measurement: Measurement vector
            
        Returns:
            Updated state vector
        """
        z = Vector(measurement)
        
        # Predict
        self.predict()
        
        # Innovation: y = z - H * x
        Hx = self.H * self.x
        y = z - Hx
        
        # Innovation covariance: S = H * P * H^T + R
        HP = self.H * self.P
        HPH_T = HP * self.H.transpose()
        S = HPH_T + self.R
        
        # Kalman gain: K = P * H^T * S^-1
        PH_T = self.P * self.H.transpose()
        S_inv = S.inverse()
        K = PH_T * S_inv
        
        # State update: x = x + K * y
        Ky = K * y
        self.x = self.x + Ky
        
        # Covariance update: P = (I - K * H) * P
        I = Matrix.identity(self.state_dim)
        KH = K * self.H
        I_KH = I - KH
        self.P = I_KH * self.P
        
        return self.x.copy()
    
    def get_state(self) -> List[float]:
        """Get current state estimate."""
        return self.x.to_list()
    
    def get_covariance(self) -> List[List[float]]:
        """Get current error covariance matrix."""
        return self.P.to_list()
    
    def get_uncertainty(self) -> List[float]:
        """Get diagonal of covariance (variance for each state variable)."""
        return [self.P.data[i][i] for i in range(self.state_dim)]
    
    def get_std_deviation(self) -> List[float]:
        """Get standard deviation for each state variable."""
        return [math.sqrt(self.P.data[i][i]) for i in range(self.state_dim)]


class KalmanFilter2D:
    """
    2D Position Kalman Filter with velocity tracking.
    
    A convenience class for 2D position tracking.
    State: [x, y, vx, vy]
    """
    
    def __init__(
        self,
        position: Tuple[float, float] = (0.0, 0.0),
        velocity: Tuple[float, float] = (0.0, 0.0),
        process_noise: float = 0.1,
        measurement_noise: float = 1.0
    ):
        """
        Initialize 2D position Kalman filter.
        
        Args:
            position: Initial (x, y) position
            velocity: Initial (vx, vy) velocity
            process_noise: Process noise variance
            measurement_noise: Measurement noise variance
        """
        self.kf = MultiDimKalmanFilter(
            state=[position[0], position[1], velocity[0], velocity[1]],
            state_dim=4,
            measurement_dim=2,
            process_noise=process_noise,
            measurement_noise=measurement_noise
        )
        
        # Set up state transition matrix for constant velocity model
        self.kf.set_F([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Set up measurement matrix (measure position only)
        self.kf.set_H([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
    
    def update(self, position: Tuple[float, float]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Update with position measurement.
        
        Args:
            position: Measured (x, y) position
            
        Returns:
            Tuple of (position_estimate, velocity_estimate)
        """
        state = self.kf.update([position[0], position[1]])
        return (state[0], state[1]), (state[2], state[3])
    
    def predict(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Predict next state without measurement.
        
        Returns:
            Tuple of (position_prediction, velocity_prediction)
        """
        state = self.kf.predict().to_list()
        return (state[0], state[1]), (state[2], state[3])
    
    def get_position(self) -> Tuple[float, float]:
        """Get current position estimate."""
        return (self.kf.x.data[0], self.kf.x.data[1])
    
    def get_velocity(self) -> Tuple[float, float]:
        """Get current velocity estimate."""
        return (self.kf.x.data[2], self.kf.x.data[3])