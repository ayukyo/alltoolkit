"""
Unscented Kalman Filter (UKF) Implementation.

Uses the unscented transform to handle non-linear systems without
computing Jacobians.
"""

import math
from typing import Callable, List, Optional, Tuple


class UnscentedKalmanFilter:
    """
    Unscented Kalman Filter for non-linear systems.
    
    The UKF uses sigma points to propagate probability distributions
    through non-linear transformations, providing better accuracy
    than EKF for highly non-linear systems.
    
    Example:
        >>> # Track position with non-linear measurement
        >>> def state_transition(x, dt):
        ...     return [x[0] + x[1]*dt, x[1]]  # Position + velocity
        >>> 
        >>> def measurement_fn(x):
        ...     return [math.sqrt(x[0]**2 + x[1]**2)]
        >>> 
        >>> ukf = UnscentedKalmanFilter(
        ...     state=[0.0, 1.0],
        ...     process_noise=0.1,
        ...     measurement_noise=0.5,
        ...     state_transition_fn=state_transition,
        ...     measurement_fn=measurement_fn
        ... )
    """
    
    def __init__(
        self,
        state: List[float],
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        state_transition_fn: Optional[Callable] = None,
        measurement_fn: Optional[Callable] = None,
        alpha: float = 1e-3,
        beta: float = 2.0,
        kappa: float = 0.0
    ):
        """
        Initialize the Unscented Kalman Filter.
        
        Args:
            state: Initial state vector
            process_noise: Process noise variance
            measurement_noise: Measurement noise variance
            state_transition_fn: Function f(x, dt) -> x_new
            measurement_fn: Function h(x) -> z
            alpha: Spread of sigma points (typically 1e-3)
            beta: Prior knowledge parameter (2 optimal for Gaussian)
            kappa: Secondary scaling parameter (typically 0)
        """
        self.x = list(state)
        self.n = len(state)  # State dimension
        
        self.Q = process_noise
        self.R = measurement_noise
        
        # UKF parameters
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa
        
        # Compute lambda
        self.lambda_ = alpha**2 * (self.n + kappa) - self.n
        
        # Compute weights
        self._compute_weights()
        
        # Initialize covariance
        self.P = self._identity(self.n)
        for i in range(self.n):
            self.P[i][i] = 1.0
        
        # Functions
        self.f = state_transition_fn or (lambda x, dt: x)
        self.h = measurement_fn or (lambda x: x)
        
        self.measurement_dim = 1  # Will be updated in update step
    
    def _identity(self, n: int) -> List[List[float]]:
        """Create n x n identity matrix."""
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    def _zeros(self, rows: int, cols: int) -> List[List[float]]:
        """Create zeros matrix."""
        return [[0.0 for _ in range(cols)] for _ in range(rows)]
    
    def _compute_weights(self):
        """Compute UKF weights."""
        n = self.n
        lambda_ = self.lambda_
        
        # Mean weights
        self.Wm = [lambda_ / (n + lambda_)]
        self.Wm.extend([1.0 / (2 * (n + lambda_)) for _ in range(2 * n)])
        
        # Covariance weights
        self.Wc = [lambda_ / (n + lambda_) + (1 - self.alpha**2 + self.beta)]
        self.Wc.extend([1.0 / (2 * (n + lambda_)) for _ in range(2 * n)])
    
    def _sqrt_matrix(self, A: List[List[float]]) -> List[List[float]]:
        """
        Compute matrix square root using Cholesky decomposition.
        Simplified implementation for diagonal or near-diagonal matrices.
        """
        n = len(A)
        L = self._zeros(n, n)
        
        for i in range(n):
            s = A[i][i]
            for k in range(i):
                s -= L[i][k] ** 2
            if s < 0:
                s = 0  # Handle numerical issues
            L[i][i] = math.sqrt(s)
            
            for j in range(i + 1, n):
                s = A[i][j]
                for k in range(i):
                    s -= L[i][k] * L[j][k]
                if abs(L[i][i]) > 1e-10:
                    L[j][i] = s / L[i][i]
        
        return L
    
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
    
    def _vec_add(self, a: List[float], b: List[float]) -> List[float]:
        """Vector addition."""
        return [a[i] + b[i] for i in range(len(a))]
    
    def _vec_sub(self, a: List[float], b: List[float]) -> List[float]:
        """Vector subtraction."""
        return [a[i] - b[i] for i in range(len(a))]
    
    def _vec_scale(self, a: List[float], s: float) -> List[float]:
        """Vector scaling."""
        return [x * s for x in a]
    
    def _vec_outer(self, a: List[float], b: List[float]) -> List[List[float]]:
        """Outer product of two vectors."""
        return [[a[i] * b[j] for j in range(len(b))] for i in range(len(a))]
    
    def _generate_sigma_points(self) -> List[List[float]]:
        """
        Generate sigma points from current state and covariance.
        
        Returns:
            List of 2n+1 sigma points
        """
        n = self.n
        lambda_ = self.lambda_
        
        # Compute scaling matrix
        scaling = n + lambda_
        
        # Get square root of scaled covariance
        scaled_P = self._zeros(n, n)
        for i in range(n):
            for j in range(n):
                scaled_P[i][j] = scaling * self.P[i][j]
        
        sqrt_P = self._sqrt_matrix(scaled_P)
        
        # Generate sigma points
        sigma_points = [self.x.copy()]  # Mean point
        
        for i in range(n):
            # Positive direction
            point_plus = self._vec_add(self.x, [sqrt_P[j][i] for j in range(n)])
            sigma_points.append(point_plus)
            
            # Negative direction
            point_minus = self._vec_sub(self.x, [sqrt_P[j][i] for j in range(n)])
            sigma_points.append(point_minus)
        
        return sigma_points
    
    def predict(self, dt: float = 1.0) -> List[float]:
        """
        Predict step: propagate sigma points through state transition.
        
        Args:
            dt: Time step
            
        Returns:
            Predicted state
        """
        # Generate sigma points
        sigma_points = self._generate_sigma_points()
        
        # Propagate sigma points through state transition
        transformed_points = [self.f(point, dt) for point in sigma_points]
        
        # Compute predicted mean
        self.x = [0.0] * self.n
        for i, point in enumerate(transformed_points):
            weighted_point = self._vec_scale(point, self.Wm[i])
            self.x = self._vec_add(self.x, weighted_point)
        
        # Compute predicted covariance
        self.P = self._zeros(self.n, self.n)
        for i, point in enumerate(transformed_points):
            diff = self._vec_sub(point, self.x)
            outer = self._vec_outer(diff, diff)
            weighted_outer = [[outer[j][k] * self.Wc[i] for k in range(self.n)] 
                               for j in range(self.n)]
            self.P = self._mat_add(self.P, weighted_outer)
        
        # Add process noise
        Q_mat = self._identity(self.n)
        for i in range(self.n):
            Q_mat[i][i] = self.Q
        self.P = self._mat_add(self.P, Q_mat)
        
        return self.x
    
    def update(self, measurement: List[float], dt: float = 1.0) -> List[float]:
        """
        Update step: incorporate measurement.
        
        Args:
            measurement: Measurement vector
            dt: Time step
            
        Returns:
            Updated state
        """
        # Predict first
        self.predict(dt)
        
        # Generate sigma points from predicted state
        sigma_points = self._generate_sigma_points()
        
        # Transform sigma points through measurement function
        measurement_points = [self.h(point) for point in sigma_points]
        
        # Determine measurement dimension
        self.measurement_dim = len(measurement_points[0]) if measurement_points else 1
        
        # Compute predicted measurement mean
        z_pred = [0.0] * self.measurement_dim
        for i, z in enumerate(measurement_points):
            weighted_z = self._vec_scale(z, self.Wm[i])
            z_pred = self._vec_add(z_pred, weighted_z)
        
        # Compute measurement covariance and cross-covariance
        S = self._zeros(self.measurement_dim, self.measurement_dim)
        C = self._zeros(self.n, self.measurement_dim)
        
        for i, z in enumerate(measurement_points):
            z_diff = self._vec_sub(z, z_pred)
            x_diff = self._vec_sub(sigma_points[i], self.x)
            
            z_outer = self._vec_outer(z_diff, z_diff)
            weighted_z_outer = [[z_outer[j][k] * self.Wc[i] for k in range(self.measurement_dim)]
                                for j in range(self.measurement_dim)]
            S = self._mat_add(S, weighted_z_outer)
            
            cross = self._vec_outer(x_diff, z_diff)
            weighted_cross = [[cross[j][k] * self.Wc[i] for k in range(self.measurement_dim)]
                              for j in range(self.n)]
            C = self._mat_add(C, weighted_cross)
        
        # Add measurement noise
        R_mat = self._identity(self.measurement_dim)
        for i in range(self.measurement_dim):
            R_mat[i][i] = self.R
        S = self._mat_add(S, R_mat)
        
        # Compute Kalman gain: K = C * S^-1
        # Simplified inversion for small matrices
        if self.measurement_dim == 1:
            S_inv = [[1.0 / S[0][0]]] if abs(S[0][0]) > 1e-10 else [[0.0]]
        else:
            # Use diagonal approximation for larger matrices
            S_inv = self._zeros(self.measurement_dim, self.measurement_dim)
            for i in range(self.measurement_dim):
                S_inv[i][i] = 1.0 / S[i][i] if abs(S[i][i]) > 1e-10 else 0.0
        
        K = self._mat_mult(C, S_inv)
        
        # Update state
        y = self._vec_sub(measurement, z_pred)
        for i in range(self.n):
            for j in range(self.measurement_dim):
                self.x[i] += K[i][j] * y[j]
        
        # Update covariance
        KS = self._mat_mult(K, S)
        KSKT = self._mat_mult(KS, self._mat_transpose(K))
        self.P = self._mat_sub(self.P, KSKT)
        
        return self.x
    
    def get_state(self) -> List[float]:
        """Get current state estimate."""
        return self.x.copy()
    
    def get_covariance(self) -> List[List[float]]:
        """Get current error covariance matrix."""
        return [row.copy() for row in self.P]


class UKF1D(UnscentedKalmanFilter):
    """
    Simplified 1D Unscented Kalman Filter.
    """
    
    def __init__(
        self,
        state: float = 0.0,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        measurement_fn: Optional[Callable] = None
    ):
        """
        Initialize 1D UKF.
        
        Args:
            state: Initial state estimate
            process_noise: Process noise variance
            measurement_noise: Measurement noise variance
            measurement_fn: Non-linear measurement function h(x) -> [z]
        """
        super().__init__(
            state=[state],
            process_noise=process_noise,
            measurement_noise=measurement_noise,
            measurement_fn=measurement_fn
        )
    
    def update(self, measurement: float, dt: float = 1.0) -> float:
        """Update with single measurement."""
        return super().update([measurement], dt)[0]
    
    def get_estimate(self) -> float:
        """Get current estimate."""
        return self.x[0]