# Kalman Filter Utils

A comprehensive Kalman filter toolkit for signal processing, state estimation, and noise filtering. Pure Python implementation with zero external dependencies.

## Features

- **Standard Kalman Filter**: Linear state estimation
- **Extended Kalman Filter (EKF)**: Non-linear systems with Jacobian linearization
- **Unscented Kalman Filter (UKF)**: Non-linear systems using sigma points
- **Multi-Dimensional Kalman Filter**: General N-dimensional state tracking
- **Adaptive Kalman Filter**: Auto-adjusting process noise
- **Position-Velocity Filter**: Track position with velocity estimation
- **2D Position Filter**: Convenient 2D tracking

## Installation

No installation needed - just copy the `kalman_filter_utils` folder to your project.

```python
from kalman_filter_utils import KalmanFilter
```

## Quick Start

### Basic Kalman Filter

```python
from kalman_filter_utils import KalmanFilter

# Create filter with noise parameters
kf = KalmanFilter(process_noise=0.1, measurement_noise=0.5)

# Filter noisy measurements
measurements = [10.1, 9.8, 10.2, 10.0, 9.9, 10.1]
filtered = [kf.update(m) for m in measurements]

print(f"Final estimate: {kf.get_estimate()}")
```

### Position Tracking

```python
from kalman_filter_utils import PositionKalmanFilter

# Track position with velocity estimation
kf = PositionKalmanFilter(position=0.0, velocity=1.0)

# Update with position measurements (object moving at 1 m/s)
for pos in [1.0, 2.1, 3.0, 4.2, 5.0]:
    position, velocity = kf.update(pos, dt=1.0)
    print(f"Pos: {position:.2f}, Vel: {velocity:.2f}")
```

### 2D Position Tracking

```python
from kalman_filter_utils import KalmanFilter2D

# Track 2D position
kf = KalmanFilter2D(position=(0, 0), velocity=(1, 0))

# Update with (x, y) measurements
for t in range(5):
    pos, vel = kf.update((t + 1, 0))
    print(f"Position: {pos}, Velocity: {vel}")
```

### Extended Kalman Filter (Non-Linear)

```python
from kalman_filter_utils import ExtendedKalmanFilter
import math

# Track 2D position with range measurements (non-linear)
def measurement_fn(x):
    return [math.sqrt(x[0]**2 + x[1]**2)]

ekf = ExtendedKalmanFilter(
    state=[3.0, 4.0],
    process_noise=0.1,
    measurement_noise=0.5,
    measurement_fn=measurement_fn,
    state_dim=2,
    measurement_dim=1
)

# Update with range measurement
state = ekf.update([5.0])  # Distance from origin is 5
print(f"Position estimate: ({state[0]:.2f}, {state[1]:.2f})")
```

### Multi-Dimensional Filter

```python
from kalman_filter_utils import MultiDimKalmanFilter

# State: [x, y, vx, vy]
kf = MultiDimKalmanFilter(
    state=[0.0, 0.0, 1.0, 0.0],
    state_dim=4,
    measurement_dim=2
)

# Configure constant velocity model
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

# Update with position measurements
state = kf.update([5.0, 0.0])
print(f"Position: ({state[0]}, {state[1]}), Velocity: ({state[2]}, {state[3]})")
```

## Noise Parameter Tuning

| Parameter | Effect |
|-----------|--------|
| High `process_noise` | Faster response, trusts measurements more |
| Low `process_noise` | Slower response, smoother output |
| High `measurement_noise` | Slow response, smooth output |
| Low `measurement_noise` | Fast response, trusts measurements |

### Typical Values

```python
# Sensor is accurate (low noise)
KalmanFilter(process_noise=0.01, measurement_noise=0.1)

# Sensor is noisy
KalmanFilter(process_noise=0.1, measurement_noise=1.0)

# System is rapidly changing
KalmanFilter(process_noise=0.5, measurement_noise=0.5)

# System is stable
KalmanFilter(process_noise=0.001, measurement_noise=0.5)
```

## Use Cases

- **Signal smoothing**: Filter noisy sensor readings
- **Position tracking**: GPS, motion tracking
- **Sensor fusion**: Combine multiple sensors
- **Time series prediction**: Forecast future values
- **Robotics**: State estimation, navigation
- **Finance**: Price smoothing, trend detection

## API Reference

### KalmanFilter

```python
kf = KalmanFilter(process_noise=0.01, measurement_noise=0.1)
kf.update(measurement)      # Returns filtered estimate
kf.predict()                # Predict next state
kf.filter_sequence(meas)    # Filter entire sequence
kf.get_estimate()           # Current estimate
kf.reset(estimate, cov)     # Reset to new state
```

### PositionKalmanFilter

```python
kf = PositionKalmanFilter(position, velocity)
kf.update(measurement, dt)  # Returns (position, velocity)
kf.predict(dt)              # Predict next state
kf.get_state()              # Returns (position, velocity)
```

### KalmanFilter2D

```python
kf = KalmanFilter2D(position=(x, y), velocity=(vx, vy))
kf.update(position)         # Returns (position, velocity)
kf.get_position()           # Returns (x, y)
kf.get_velocity()           # Returns (vx, vy)
```

### ExtendedKalmanFilter

```python
ekf = ExtendedKalmanFilter(
    state,
    process_noise,
    measurement_noise,
    state_transition_fn,
    measurement_fn
)
ekf.update(measurement, dt)  # Returns state vector
```

### MultiDimKalmanFilter

```python
kf = MultiDimKalmanFilter(state, state_dim, measurement_dim)
kf.set_F(F_matrix)          # Set state transition matrix
kf.set_H(H_matrix)          # Set measurement matrix
kf.update(measurement)      # Returns state vector
kf.get_uncertainty()        # Returns variance for each state
```

## Running Tests

```bash
python kalman_filter_utils/kalman_filter_utils_test.py
```

## License

MIT License - free to use in any project.