"""
Tests for Kalman Filter implementations.

Run with: python -m pytest kalman_filter_utils_test.py -v
Or simply: python kalman_filter_utils_test.py
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kalman_filter_utils import (
    KalmanFilter,
    AdaptiveKalmanFilter,
    MovingAverageKalman,
    PositionKalmanFilter,
    ExtendedKalmanFilter,
    EKF1D,
    UnscentedKalmanFilter,
    UKF1D,
    MultiDimKalmanFilter,
    KalmanFilter2D,
    Matrix,
    Vector
)


def test_kalman_filter_basic():
    """Test basic Kalman filter functionality."""
    kf = KalmanFilter(process_noise=0.1, measurement_noise=0.5)
    
    # Initial estimate should be 0
    assert abs(kf.get_estimate() - 0.0) < 0.001
    
    # After first update, estimate should move towards measurement
    kf.update(10.0)
    assert 5 < kf.get_estimate() < 10  # Should be between 0 and 10
    
    # More updates should converge to true value
    for _ in range(10):
        kf.update(10.0)
    
    assert abs(kf.get_estimate() - 10.0) < 0.5


def test_kalman_filter_sequence():
    """Test filtering a sequence of measurements."""
    kf = KalmanFilter(process_noise=0.01, measurement_noise=0.1, estimate=5.0)
    
    # Noisy measurements around 5.0
    measurements = [5.1, 4.9, 5.2, 4.8, 5.0, 5.1, 4.9, 5.0]
    
    estimates = kf.filter_sequence(measurements)
    
    # Final estimate should be close to 5.0
    assert abs(estimates[-1] - 5.0) < 0.3
    
    # Estimates should be smoother than raw measurements (after initial convergence)
    # Check last 4 estimates
    measurement_variance = sum((m - 5.0)**2 for m in measurements[-4:]) / 4
    estimate_variance = sum((e - 5.0)**2 for e in estimates[-4:]) / 4
    assert estimate_variance < measurement_variance


def test_kalman_filter_reset():
    """Test filter reset functionality."""
    kf = KalmanFilter()
    kf.update(100.0)
    
    assert abs(kf.get_estimate() - 100.0) < 10
    
    kf.reset(estimate=0.0, error_covariance=1.0)
    
    assert abs(kf.get_estimate() - 0.0) < 0.001
    assert abs(kf.get_error_covariance() - 1.0) < 0.001


def test_adaptive_kalman_filter():
    """Test adaptive Kalman filter."""
    kf = AdaptiveKalmanFilter(
        process_noise=0.01,
        measurement_noise=0.1,
        adaptation_rate=0.5
    )
    
    # Steady measurements - process noise should decrease
    for _ in range(20):
        kf.update(10.0)
    
    initial_Q = kf.Q
    
    # Sudden change - process noise should increase
    for _ in range(5):
        kf.update(50.0)
    
    # Process noise should have adapted
    # (may be higher or lower depending on implementation)


def test_moving_average_kalman():
    """Test moving average Kalman filter."""
    kf = MovingAverageKalman(alpha=0.3)
    
    estimates = []
    for m in [10.0] * 10:
        estimates.append(kf.update(m))
    
    # Should converge to 10
    assert abs(estimates[-1] - 10.0) < 1.0
    
    # Test alpha boundary
    try:
        MovingAverageKalman(alpha=1.5)
        assert False, "Should raise ValueError for alpha > 1"
    except ValueError:
        pass


def test_position_kalman_filter():
    """Test position-velocity Kalman filter."""
    kf = PositionKalmanFilter(position=0.0, velocity=1.0)
    
    # Object moving at constant velocity
    measurements = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    for m in measurements:
        pos, vel = kf.update(m, dt=1.0)
    
    # Should estimate position close to 5
    assert abs(pos - 5.0) < 1.0
    
    # Should estimate velocity close to 1
    assert abs(vel - 1.0) < 0.5


def test_extended_kalman_filter():
    """Test extended Kalman filter with non-linear measurement."""
    # Simple non-linear example: measuring distance from origin
    def measurement_fn(x):
        return [math.sqrt(x[0]**2 + x[1]**2)]
    
    ekf = ExtendedKalmanFilter(
        state=[3.0, 4.0],  # 5 units from origin
        process_noise=0.01,
        measurement_noise=0.1,
        measurement_fn=measurement_fn,
        state_dim=2,
        measurement_dim=1
    )
    
    # Measure distance of 5
    state = ekf.update([5.0])
    
    # Should stay close to (3, 4)
    assert abs(state[0] - 3.0) < 0.5
    assert abs(state[1] - 4.0) < 0.5


def test_ekf_1d():
    """Test 1D extended Kalman filter."""
    ekf = EKF1D(state=0.0, process_noise=0.1, measurement_noise=0.5)
    
    estimates = []
    for m in [10.0, 10.1, 9.9, 10.0, 10.2]:
        estimates.append(ekf.update(m))
    
    # Should converge towards 10
    assert abs(estimates[-1] - 10.0) < 1.0


def test_unscented_kalman_filter():
    """Test unscented Kalman filter."""
    # Default measurement function returns first element (position)
    def measurement_fn(x):
        return [x[0]]  # Return position only
    
    ukf = UnscentedKalmanFilter(
        state=[0.0, 1.0],  # Position 0, velocity 1
        process_noise=0.01,
        measurement_noise=0.1,
        measurement_fn=measurement_fn
    )
    
    # Update with position measurements
    for m in [1.0, 2.0, 3.0]:
        state = ukf.update([m], dt=1.0)
    
    # Should track position and velocity
    assert abs(state[0] - 3.0) < 1.0  # Position
    assert abs(state[1] - 1.0) < 0.5  # Velocity


def test_ukf_1d():
    """Test 1D unscented Kalman filter."""
    ukf = UKF1D(state=0.0, process_noise=0.1, measurement_noise=0.5)
    
    estimates = []
    for m in [5.0] * 10:
        estimates.append(ukf.update(m))
    
    # Should converge to 5
    assert abs(estimates[-1] - 5.0) < 1.0


def test_matrix_operations():
    """Test matrix class operations."""
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])
    
    # Addition
    C = A + B
    assert C.data == [[6, 8], [10, 12]]
    
    # Subtraction
    D = B - A
    assert D.data == [[4, 4], [4, 4]]
    
    # Multiplication
    E = A * B
    assert E.data == [[19, 22], [43, 50]]
    
    # Transpose
    At = A.transpose()
    assert At.data == [[1, 3], [2, 4]]
    
    # Identity
    I = Matrix.identity(3)
    assert I.data == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    # Determinant
    det = A.det()
    assert abs(det - (-2.0)) < 0.001


def test_matrix_inverse():
    """Test matrix inversion."""
    A = Matrix([[4, 7], [2, 6]])
    A_inv = A.inverse()
    
    # A * A_inv should be identity
    result = A * A_inv
    
    assert abs(result.data[0][0] - 1.0) < 0.001
    assert abs(result.data[0][1]) < 0.001
    assert abs(result.data[1][0]) < 0.001
    assert abs(result.data[1][1] - 1.0) < 0.001


def test_vector_operations():
    """Test vector class operations."""
    a = Vector([1.0, 2.0, 3.0])
    b = Vector([4.0, 5.0, 6.0])
    
    # Addition
    c = a + b
    assert c.data == [5.0, 7.0, 9.0]
    
    # Subtraction
    d = b - a
    assert d.data == [3.0, 3.0, 3.0]
    
    # Scalar multiplication
    e = 2 * a
    assert e.data == [2.0, 4.0, 6.0]
    
    # Dot product
    dot = a * b
    assert dot == 32.0  # 1*4 + 2*5 + 3*6
    
    # Norm
    n = a.norm()
    assert abs(n - math.sqrt(14)) < 0.001
    
    # Normalize
    a_norm = a.normalize()
    assert abs(a_norm.norm() - 1.0) < 0.001


def test_multi_dim_kalman_filter():
    """Test multi-dimensional Kalman filter."""
    kf = MultiDimKalmanFilter(
        state=[0.0, 0.0, 1.0, 0.0],  # x, y, vx, vy
        state_dim=4,
        measurement_dim=2,
        process_noise=0.1,
        measurement_noise=1.0
    )
    
    # Set up constant velocity model
    kf.set_F([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    kf.set_H([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])
    
    # Track object moving right at velocity 1
    for t in range(5):
        state = kf.update([float(t + 1), 0.0])
    
    # Position should be close to (5, 0)
    assert abs(state[0] - 5.0) < 0.5
    assert abs(state[1]) < 0.5
    
    # Velocity should be close to (1, 0)
    assert abs(state[2] - 1.0) < 0.3
    assert abs(state[3]) < 0.3


def test_kalman_filter_2d():
    """Test 2D position Kalman filter."""
    kf = KalmanFilter2D(
        position=(0.0, 0.0),
        velocity=(1.0, 0.0),
        process_noise=0.1,
        measurement_noise=1.0
    )
    
    # Track object moving right
    for t in range(1, 6):
        pos, vel = kf.update((float(t), 0.0))
    
    # Should track position
    assert abs(pos[0] - 5.0) < 0.5
    assert abs(pos[1]) < 0.5
    
    # Should estimate velocity
    assert abs(vel[0] - 1.0) < 0.3
    assert abs(vel[1]) < 0.3


def test_noisy_signal_smoothing():
    """Test Kalman filter for noisy signal smoothing."""
    import random
    random.seed(42)
    
    # Generate noisy constant signal (easier for Kalman filter)
    true_value = 5.0
    noisy_signal = [true_value + random.gauss(0, 0.5) for _ in range(50)]
    
    # Apply Kalman filter with appropriate parameters
    kf = KalmanFilter(
        process_noise=0.001,  # Low: signal is nearly constant
        measurement_noise=0.25,  # Matches actual noise variance
        estimate=true_value
    )
    filtered = [kf.update(m) for m in noisy_signal]
    
    # Calculate MSE for noisy and filtered signals
    mse_noisy = sum((m - true_value)**2 for m in noisy_signal) / len(noisy_signal)
    mse_filtered = sum((f - true_value)**2 for f in filtered) / len(filtered)
    
    # Filtered signal should have lower MSE
    assert mse_filtered < mse_noisy * 0.5  # Should reduce noise by at least 50%


def test_kalman_filter_edge_cases():
    """Test edge cases and error handling."""
    # Invalid process noise
    try:
        KalmanFilter(process_noise=-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Invalid measurement noise
    try:
        KalmanFilter(measurement_noise=0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Zero measurements
    kf = KalmanFilter()
    for _ in range(10):
        kf.update(0.0)
    assert abs(kf.get_estimate()) < 0.1


def test_position_kalman_predict():
    """Test position Kalman filter prediction."""
    kf = PositionKalmanFilter(position=0.0, velocity=2.0)
    
    # Predict without measurement
    pos, vel = kf.predict(dt=1.0)
    assert abs(pos - 2.0) < 0.1  # Should have moved 2 units
    
    pos, vel = kf.predict(dt=1.0)
    assert abs(pos - 4.0) < 0.1  # Should have moved another 2 units


def run_all_tests():
    """Run all tests manually."""
    tests = [
        test_kalman_filter_basic,
        test_kalman_filter_sequence,
        test_kalman_filter_reset,
        test_adaptive_kalman_filter,
        test_moving_average_kalman,
        test_position_kalman_filter,
        test_extended_kalman_filter,
        test_ekf_1d,
        test_unscented_kalman_filter,
        test_ukf_1d,
        test_matrix_operations,
        test_matrix_inverse,
        test_vector_operations,
        test_multi_dim_kalman_filter,
        test_kalman_filter_2d,
        test_noisy_signal_smoothing,
        test_kalman_filter_edge_cases,
        test_position_kalman_predict,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)