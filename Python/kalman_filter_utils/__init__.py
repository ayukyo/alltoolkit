"""
Kalman Filter Utils - A collection of Kalman filter implementations for signal processing.

This module provides various Kalman filter implementations including:
- Standard Kalman Filter
- Extended Kalman Filter (EKF)
- Unscented Kalman Filter (UKF)
- Multi-dimensional Kalman Filter
- Adaptive Kalman Filter
- Position Kalman Filter

No external dependencies - pure Python implementation.
"""

from .kalman import (
    KalmanFilter,
    KalmanFilter1D,
    AdaptiveKalmanFilter,
    MovingAverageKalman,
    PositionKalmanFilter,
)
from .extended_kalman import ExtendedKalmanFilter, EKF1D
from .unscented_kalman import UnscentedKalmanFilter, UKF1D
from .multi_dim import (
    MultiDimKalmanFilter,
    KalmanFilter2D,
    Matrix,
    Vector,
)

__version__ = "1.0.0"
__all__ = [
    "KalmanFilter",
    "KalmanFilter1D",
    "AdaptiveKalmanFilter",
    "MovingAverageKalman",
    "PositionKalmanFilter",
    "ExtendedKalmanFilter",
    "EKF1D",
    "UnscentedKalmanFilter",
    "UKF1D",
    "MultiDimKalmanFilter",
    "KalmanFilter2D",
    "Matrix",
    "Vector",
]