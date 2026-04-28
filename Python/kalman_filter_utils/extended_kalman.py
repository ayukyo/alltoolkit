"""
Extended Kalman Filter (EKF) Implementation.

For non-linear systems where the standard Kalman filter cannot be applied directly.
"""

import math
from typing import Callable, List, Tuple, Optional


class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for non-linear systems.
    
    The EKF linearizes the non-linear functions around the current estimate
    using first-order Taylor expansion (Jacobian matrices).
    
    Example:
        >>> # Track a 2D position with range measurements
        >>> def state_transition(x, dt):
        ...     return [x[0] + x[2]*dt, x[1] + x[3]*dt, x[2], x[3]]
        >>> 
        >>> def measurement_function(x):
        ...     return [math.sqrt(x[0]**2 + x[1]**2)]
        >>> 
        >>> ekf = ExtendedKalmanFilter(
        ...     state=[0, 0, 1, 0],  # x, y, vx, vy
        ...     process_noise=0.1,
        ...     measurement_noise=0.5,
        ...     state_transition_fn=state_transition,
        ...     measurement_fn=measurement_function
        ... )
    """
    
    def __init__(
        self,
        state: List[float],
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        state_transition_fn: Optional[Callable] = None,
        measurement_fn: Optional[Callable] = None,
        jacobian_state_fn: Optional[Callable] = None,
        jacobian_measurement_fn: Optional[Callable] = None,
        state_dim: Optional[int] = None,
        measurement_dim: int = 1
    ):
        """
        Initialize the Extended Kalman Filter.
        
        Args:
            state: Initial state vector
            process_noise: Process noise variance (applied uniformly)
            measurement_noise: Measurement noise variance (applied uniformly)
            state_transition_fn: Function f(x, dt) -> x_new
            measurement_fn: Function h(x) -> z
            jacobian_state_fn: Function to compute Jacobian of state transition
            jacobian_measurement_fn: Function to compute Jacobian of measurement
            state_dim: State dimension (defaults to len(state))
            measurement_dim: Measurement dimension
        """
        self.x = list(state)  # State estimate
        self.state_dim = state_dim or len(state)
        self.measurement_dim = measurement_dim
        
        self.Q = process_noise      # Process noise (scalar, will be expanded)
        self.R = measurement_noise   # Measurement noise (scalar, will be expanded)
        
        # Error covariance matrix (identity scaled)
        self.P = self._identity(self.state_dim)
        
        # Functions
        self.f = state_transition_fn or (lambda x, dt: x)  # Default: identity
        self.h = measurement_fn or (lambda x: x[:measurement_dim])  # Default: first n elements
        self.F_jacobian = jacobian_state_fn
        self.H_jacobian = jacobian_measurement_fn
        
    def _identity(self, n: int) -> List[List[float]]:
        """Create n x n identity matrix."""
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    def _zeros(self, rows: int, cols: int) -> List[List[float]]:
        """Create zeros matrix."""
        return [[0.0 for _ in range(cols)] for _ in range(rows)]
    
    def _mat_mult(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix multiplication."""
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        result = self._zeros(rows_A, cols_B)
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def _mat_add(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix addition."""
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    
    def _mat_sub(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix subtraction."""
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    
    def _mat_transpose(self, A: List[List[float]]) -> List[List[float]]:
        """Matrix transpose."""
        return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    
    def _mat_inverse_2x2(self, A: List[List[float]]) -> List[List[float]]:
        """Inverse of 2x2 matrix."""
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        if abs(det) < 1e-10:
            # Pseudo-inverse for near-singular matrices
            return [[A[1][1] / (det + 1e-10), -A[0][1] / (det + 1e-10)],
                    [-A[1][0] / (det + 1e-10), A[0][0] / (det + 1e-10)]]
        return [[A[1][1] / det, -A[0][1] / det],
                [-A[1][0] / det, A[0][0] / det]]
    
    def _compute_jacobian_numerical(self, fn: Callable, x: List[float], 
                                     output_dim: int, epsilon: float = 1e-6) -> List[List[float]]:
        """Compute Jacobian numerically using finite differences."""
        jacobian = self._zeros(output_dim, len(x))
        for j in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[j] += epsilon
            x_minus[j] -= epsilon
            f_plus = fn(x_plus)
            f_minus = fn(x_minus)
            for i in range(output_dim):
                jacobian[i][j] = (f_plus[i] - f_minus[i]) / (2 * epsilon)
        return jacobian
    
    def predict(self, dt: float = 1.0) -> List[float]:
        """
        Predict step: project state and covariance forward.
        
        Args:
            dt: Time step
            
        Returns:
            Predicted state
        """
        # State prediction
        self.x = self.f(self.x, dt)
        
        # Compute Jacobian of state transition
        if self.F_jacobian:
            F = self.F_jacobian(self.x, dt)
        else:
            # Default: identity for linear motion
            F = self._identity(self.state_dim)
            if dt != 0:
                # For position-velocity model, add dt to off-diagonal
                for i in range(self.state_dim // 2):
                    F[i][i + self.state_dim // 2] = dt
        
        # Covariance prediction: P = F * P * F^T + Q
        F_T = self._mat_transpose(F)
        FP = self._mat_mult(F, self.P)
        FPF_T = self._mat_mult(FP, F_T)
        
        # Add process noise
        Q_mat = self._identity(self.state_dim)
        for i in range(self.state_dim):
            Q_mat[i][i] = self.Q
        
        self.P = self._mat_add(FPF_T, Q_mat)
        
        return self.x
    
    def update(self, measurement: List[float], dt: float = 1.0) -> List[float]:
        """
        Update step: incorporate measurement.
        
        Args:
            measurement: Measurement vector
            dt: Time step since last update
            
        Returns:
            Updated state
        """
        # Predict first
        self.predict(dt)
        
        # Compute Jacobian of measurement function
        if self.H_jacobian:
            H = self.H_jacobian(self.x)
        else:
            # Numerical Jacobian
            H = self._compute_jacobian_numerical(
                self.h, self.x, self.measurement_dim
            )
        
        # Measurement prediction
        z_pred = self.h(self.x)
        
        # Innovation (measurement residual)
        y = [measurement[i] - z_pred[i] for i in range(self.measurement_dim)]
        
        # Innovation covariance: S = H * P * H^T + R
        H_T = self._mat_transpose(H)
        HP = self._mat_mult(H, self.P)
        HPH_T = self._mat_mult(HP, H_T)
        
        # Add measurement noise
        R_mat = self._identity(self.measurement_dim)
        for i in range(self.measurement_dim):
            R_mat[i][i] = self.R
        
        S = self._mat_add(HPH_T, R_mat)
        
        # Kalman gain: K = P * H^T * S^-1
        PH_T = self._mat_mult(self.P, H_T)
        
        # Invert S (simplified for small matrices)
        if self.measurement_dim == 1:
            S_inv = [[1.0 / S[0][0]]]
        elif self.measurement_dim == 2:
            S_inv = self._mat_inverse_2x2(S)
        else:
            # For larger matrices, use a simple approximation
            # (In practice, use numpy or similar for production)
            S_inv = self._identity(self.measurement_dim)
            for i in range(self.measurement_dim):
                S_inv[i][i] = 1.0 / S[i][i] if abs(S[i][i]) > 1e-10 else 0.0
        
        K = self._mat_mult(PH_T, S_inv)
        
        # State update: x = x + K * y
        for i in range(self.state_dim):
            for j in range(self.measurement_dim):
                self.x[i] += K[i][j] * y[j]
        
        # Covariance update: P = (I - K * H) * P
        KH = self._mat_mult(K, H)
        I_KH = self._mat_sub(self._identity(self.state_dim), KH)
        self.P = self._mat_mult(I_KH, self.P)
        
        return self.x
    
    def get_state(self) -> List[float]:
        """Get current state estimate."""
        return self.x.copy()
    
    def get_covariance(self) -> List[List[float]]:
        """Get current error covariance matrix."""
        return [row.copy() for row in self.P]


class EKF1D(ExtendedKalmanFilter):
    """
    Simplified 1D Extended Kalman Filter.
    
    A convenience class for tracking a single variable with non-linear
    measurement function.
    """
    
    def __init__(
        self,
        state: float = 0.0,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        measurement_fn: Optional[Callable] = None
    ):
        """
        Initialize 1D EKF.
        
        Args:
            state: Initial state estimate
            process_noise: Process noise variance
            measurement_noise: Measurement noise variance
            measurement_fn: Non-linear measurement function h(x) -> z
        """
        super().__init__(
            state=[state],
            process_noise=process_noise,
            measurement_noise=measurement_noise,
            measurement_fn=measurement_fn,
            state_dim=1,
            measurement_dim=1
        )
    
    def update(self, measurement: float, dt: float = 1.0) -> float:
        """Update with single measurement."""
        return super().update([measurement], dt)[0]
    
    def get_estimate(self) -> float:
        """Get current estimate."""
        return self.x[0]