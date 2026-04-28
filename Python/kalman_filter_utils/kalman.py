"""
Standard Kalman Filter Implementation.

A linear Kalman filter for state estimation and noise filtering.
"""

import math
from typing import List, Optional, Tuple


class KalmanFilter:
    """
    A one-dimensional Kalman filter for noise filtering and state estimation.
    
    The Kalman filter maintains an estimate of the true state of a system
    and updates this estimate as new measurements are made. It is optimal
    for linear systems with Gaussian noise.
    
    Example:
        >>> kf = KalmanFilter(process_noise=0.1, measurement_noise=0.5)
        >>> kf.update(10.0)  # First measurement
        10.0
        >>> kf.update(10.5)  # Second measurement
        10.25
        >>> kf.update(9.8)   # Third measurement
        10.1
    """
    
    def __init__(
        self,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        estimate: float = 0.0,
        error_covariance: float = 1.0
    ):
        """
        Initialize the Kalman filter.
        
        Args:
            process_noise: Process noise variance (Q) - how much the true state changes
            measurement_noise: Measurement noise variance (R) - measurement uncertainty
            estimate: Initial state estimate (x_hat)
            error_covariance: Initial error covariance (P)
        """
        if process_noise < 0:
            raise ValueError("Process noise must be non-negative")
        if measurement_noise <= 0:
            raise ValueError("Measurement noise must be positive")
        
        self.Q = process_noise          # Process noise covariance
        self.R = measurement_noise      # Measurement noise covariance
        self.x = estimate               # State estimate
        self.P = error_covariance       # Error covariance
        
    def predict(self) -> float:
        """
        Predict step: project the state estimate ahead.
        
        For a simple 1D Kalman filter with no control input and identity
        state transition, this just increases the uncertainty.
        
        Returns:
            The predicted state estimate
        """
        # Project the error covariance ahead
        self.P = self.P + self.Q
        return self.x
    
    def update(self, measurement: float) -> float:
        """
        Update step: incorporate a new measurement.
        
        This performs both predict and update steps for convenience.
        
        Args:
            measurement: The measured value
            
        Returns:
            The updated state estimate
        """
        # Predict
        self.predict()
        
        # Calculate Kalman gain
        K = self.P / (self.P + self.R)
        
        # Update estimate with measurement
        self.x = self.x + K * (measurement - self.x)
        
        # Update error covariance
        self.P = (1 - K) * self.P
        
        return self.x
    
    def get_estimate(self) -> float:
        """Get the current state estimate."""
        return self.x
    
    def get_error_covariance(self) -> float:
        """Get the current error covariance."""
        return self.P
    
    def reset(self, estimate: float = 0.0, error_covariance: float = 1.0):
        """Reset the filter to a new initial state."""
        self.x = estimate
        self.P = error_covariance
    
    def filter_sequence(self, measurements: List[float]) -> List[float]:
        """
        Filter a sequence of measurements.
        
        Args:
            measurements: List of measurement values
            
        Returns:
            List of filtered estimates
        """
        return [self.update(m) for m in measurements]


class KalmanFilter1D(KalmanFilter):
    """Alias for KalmanFilter for clarity."""
    pass


class AdaptiveKalmanFilter(KalmanFilter):
    """
    An adaptive Kalman filter that adjusts process noise based on 
    innovation (measurement residual) magnitude.
    
    This helps the filter adapt when the actual process noise differs
    from the assumed value.
    """
    
    def __init__(
        self,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        estimate: float = 0.0,
        error_covariance: float = 1.0,
        adaptation_rate: float = 0.1,
        min_process_noise: float = 0.001,
        max_process_noise: float = 1.0
    ):
        """
        Initialize the adaptive Kalman filter.
        
        Args:
            process_noise: Initial process noise variance
            measurement_noise: Measurement noise variance
            estimate: Initial state estimate
            error_covariance: Initial error covariance
            adaptation_rate: How quickly to adapt (0 to 1)
            min_process_noise: Minimum allowed process noise
            max_process_noise: Maximum allowed process noise
        """
        super().__init__(process_noise, measurement_noise, estimate, error_covariance)
        self.adaptation_rate = adaptation_rate
        self.min_Q = min_process_noise
        self.max_Q = max_process_noise
        self._last_innovation = 0.0
        
    def update(self, measurement: float) -> float:
        """
        Update with measurement and adapt process noise.
        
        Args:
            measurement: The measured value
            
        Returns:
            The updated state estimate
        """
        # Predict
        self.P = self.P + self.Q
        
        # Calculate innovation (measurement residual)
        innovation = measurement - self.x
        
        # Adapt process noise based on innovation magnitude
        innovation_squared = innovation ** 2
        expected_innovation = self.P + self.R
        
        # Adjust Q if innovation is larger than expected
        if innovation_squared > expected_innovation:
            adjustment = self.adaptation_rate * (innovation_squared / expected_innovation - 1)
            self.Q = min(self.max_Q, self.Q * (1 + adjustment))
        else:
            # Gradually decrease Q if innovation is small
            self.Q = max(self.min_Q, self.Q * (1 - self.adaptation_rate * 0.1))
        
        self._last_innovation = innovation
        
        # Calculate Kalman gain
        K = self.P / (self.P + self.R)
        
        # Update estimate
        self.x = self.x + K * innovation
        
        # Update error covariance
        self.P = (1 - K) * self.P
        
        return self.x


class MovingAverageKalman(KalmanFilter):
    """
    A Kalman filter configured to behave like an exponentially 
    weighted moving average (EWMA).
    
    This provides a simple interface for common smoothing applications.
    """
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize with smoothing factor.
        
        Args:
            alpha: Smoothing factor between 0 and 1. 
                   Higher values = faster response, more noise.
                   Lower values = slower response, smoother output.
        """
        if not 0 < alpha < 1:
            raise ValueError("Alpha must be between 0 and 1")
        
        # Configure Kalman filter to behave like EWMA
        # The relationship is: alpha ≈ Q / (Q + R) when P is small
        super().__init__(
            process_noise=alpha * 0.001,
            measurement_noise=(1 - alpha) * 0.001,
            estimate=0.0,
            error_covariance=0.001
        )
        self.alpha = alpha
        
    def update(self, measurement: float) -> float:
        """Update with EWMA-style smoothing."""
        # For first measurement, just set it
        if self.P >= 1.0:
            self.x = measurement
            self.P = 0.001
            return self.x
        return super().update(measurement)


class PositionKalmanFilter:
    """
    A 1D position Kalman filter with velocity estimation.
    
    This filter tracks both position and velocity, making it suitable
    for tracking moving objects.
    
    State: [position, velocity]
    """
    
    def __init__(
        self,
        position: float = 0.0,
        velocity: float = 0.0,
        process_noise: float = 0.1,
        measurement_noise: float = 1.0
    ):
        """
        Initialize position-velocity Kalman filter.
        
        Args:
            position: Initial position estimate
            velocity: Initial velocity estimate
            process_noise: Process noise (acceleration variance)
            measurement_noise: Measurement noise variance
        """
        self.pos = position      # Position estimate
        self.vel = velocity      # Velocity estimate
        self.Q = process_noise
        self.R = measurement_noise
        
        # Error covariance matrix (2x2)
        self.P_pos = 1.0         # Position variance
        self.P_vel = 1.0         # Velocity variance
        self.P_cross = 0.0       # Position-velocity covariance
        
    def predict(self, dt: float = 1.0) -> Tuple[float, float]:
        """
        Predict step with time interval.
        
        Args:
            dt: Time step
            
        Returns:
            Tuple of (predicted_position, predicted_velocity)
        """
        # State transition: pos = pos + vel * dt, vel = vel
        self.pos = self.pos + self.vel * dt
        # Velocity unchanged in prediction
        
        # Covariance prediction
        self.P_pos = self.P_pos + 2 * dt * self.P_cross + dt * dt * self.P_vel + self.Q * dt * dt
        self.P_vel = self.P_vel + self.Q
        self.P_cross = self.P_cross + dt * self.P_vel
        
        return self.pos, self.vel
    
    def update(self, measurement: float, dt: float = 1.0) -> Tuple[float, float]:
        """
        Update with position measurement.
        
        Args:
            measurement: Measured position
            dt: Time step since last update
            
        Returns:
            Tuple of (updated_position, updated_velocity)
        """
        # Predict
        self.predict(dt)
        
        # Measurement relates only to position
        # Innovation
        y = measurement - self.pos
        
        # Innovation covariance
        S = self.P_pos + self.R
        
        # Kalman gain
        K_pos = self.P_pos / S
        K_vel = self.P_cross / S
        
        # State update
        self.pos = self.pos + K_pos * y
        self.vel = self.vel + K_vel * y
        
        # Covariance update
        self.P_vel = self.P_vel - K_vel * self.P_cross
        self.P_cross = self.P_cross * (1 - K_pos)
        self.P_pos = self.P_pos * (1 - K_pos)
        
        return self.pos, self.vel
    
    def get_state(self) -> Tuple[float, float]:
        """Get current state (position, velocity)."""
        return self.pos, self.vel