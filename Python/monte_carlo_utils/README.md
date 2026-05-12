# Monte Carlo Simulation Utilities

A comprehensive Monte Carlo simulation module for Python with zero external dependencies.

## Features

- **Generic Monte Carlo Framework**: Flexible implementation for any simulation
- **Multiple Sampling Strategies**: Uniform, importance sampling, stratified
- **Built-in Simulations**: Pre-configured solutions for common problems
  - π Estimation (dart board method)
  - European Option Pricing (Black-Scholes-Merton)
  - Value at Risk (VaR) and Expected Shortfall (CVaR)
  - Probability Estimation
  - Brownian Motion and Geometric Brownian Motion
  - Monte Carlo Integration (1D and N-dimensional)
- **Statistical Analysis**: Confidence intervals, standard errors, convergence diagnostics
- **Variance Reduction**: Importance sampling support
- **Zero Dependencies**: Pure Python implementation using only standard library
- **Comprehensive Testing**: Full test suite with edge case coverage
- **Reproducible Results**: Seeded simulations for reproducibility

## Installation

No installation required! Simply copy the `mod.py` file to your project.

```python
from monte_carlo_utils.mod import MonteCarlo, MCConfig
```

## Quick Start

### Basic Simulation

```python
from mod import MonteCarlo, MCConfig

# Define your sample function
def sample_function():
    return random.random()

# Configure and run
config = MCConfig(num_samples=10000, seed=42)
mc = MonteCarlo(sample_function, config)
result = mc.simulate()

print(f"Estimate: {result.estimate:.6f}")
print(f"95% CI: ({result.confidence_interval[0]:.6f}, {result.confidence_interval[1]:.6f})")
```

### Estimate π

```python
from mod import estimate_pi

result = estimate_pi(100000, seed=42)
print(f"π ≈ {result.estimate:.6f}")  # Should be ~3.14159
print(f"Error: {abs(result.estimate - 3.14159):.6f}")
```

### Option Pricing

```python
from mod import price_european_call, price_european_put

# European call option
call_result = price_european_call(
    S0=100,      # Current stock price
    K=105,       # Strike price
    T=1,         # Time to maturity (1 year)
    r=0.05,      # Risk-free rate (5%)
    sigma=0.2,   # Volatility (20%)
    num_samples=100000
)
print(f"Call price: ${call_result.estimate:.2f}")

# European put option
put_result = price_european_put(S0=100, K=105, T=1, r=0.05, sigma=0.2)
print(f"Put price: ${put_result.estimate:.2f}")
```

### Monte Carlo Integration

```python
from mod import MonteCarlo

mc = MonteCarlo()

# Integrate x^2 from 0 to 1 (result should be 1/3)
result = mc.integrate_1d(lambda x: x**2, 0, 1, num_samples=100000)
print(f"Integral: {result.estimate:.6f}")

# N-dimensional integration: f(x,y) = x*y over [0,1]x[0,1]
result = mc.integrate_nd(lambda p: p[0]*p[1], [(0,1), (0,1)])
print(f"2D integral: {result.estimate:.6f}")  # Should be 0.25
```

### Risk Analysis

```python
from mod import value_at_risk, expected_shortfall

# Historical returns (daily)
returns = [0.01, -0.02, 0.03, -0.01, 0.02, -0.03, 0.01]

# Calculate 95% VaR
var_result = value_at_risk(returns, confidence_level=0.95, initial_value=1000000)
print(f"95% VaR: ${var_result.estimate:,.2f}")

# Calculate Expected Shortfall (average worst 5% loss)
es_result = expected_shortfall(returns, confidence_level=0.95, initial_value=1000000)
print(f"95% ES: ${es_result.estimate:,.2f}")
```

### Probability Estimation

```python
from mod import probability_estimate

# Probability of sum of two dice >= 10
def dice_sum_geq_10():
    return random.randint(1, 6) + random.randint(1, 6) >= 10

result = probability_estimate(dice_sum_geq_10, num_samples=100000)
print(f"P(sum >= 10) ≈ {result.estimate:.4f}")  # Should be ~0.167
```

### Brownian Motion Simulation

```python
from mod import simulate_brownian_motion, simulate_geometric_brownian_motion

# Standard Brownian motion
bm_result = simulate_brownian_motion(steps=100, dt=0.01, mu=0, sigma=1)
print(f"Final value mean: {bm_result['final_mean']:.4f}")

# Geometric Brownian Motion (stock price model)
gbm_result = simulate_geometric_brownian_motion(
    S0=100,      # Initial price
    steps=252,   # Daily steps for 1 year
    dt=1/252,    # Daily time step
    mu=0.08,     # 8% annual drift
    sigma=0.2    # 20% volatility
)
print(f"Expected final price: ${gbm_result['final_mean']:.2f}")
```

## API Reference

### Core Classes

#### `MonteCarlo(sample_function, config)`
Main Monte Carlo simulation class.

**Parameters:**
- `sample_function`: Function that generates sample values
- `config`: `MCConfig` with simulation parameters

**Methods:**
- `simulate()`: Run simulation with sample function
- `integrate_1d(integrand, a, b, num_samples)`: 1D integration
- `integrate_nd(integrand, bounds, num_samples)`: N-dimensional integration
- `add_sample(value)`: Add a sample manually
- `compute_statistics()`: Get current statistics
- `reset(seed)`: Reset simulation state

#### `MCConfig(num_samples, seed, confidence_level, ...)`
Configuration dataclass.

**Parameters:**
- `num_samples`: Number of Monte Carlo samples (default: 10000)
- `seed`: Random seed for reproducibility
- `confidence_level`: Confidence level for CI (default: 0.95)
- `batch_size`: Progress reporting interval (default: 1000)
- `verbose`: Print progress messages

### Built-in Functions

| Function | Description |
|----------|-------------|
| `estimate_pi(num_samples, seed)` | Estimate π using dart board method |
| `price_european_call(S0, K, T, r, sigma, ...)` | Price European call option |
| `price_european_put(S0, K, T, r, sigma, ...)` | Price European put option |
| `value_at_risk(returns, confidence_level, ...)` | Calculate VaR |
| `expected_shortfall(returns, confidence_level, ...)` | Calculate CVaR |
| `probability_estimate(condition, num_samples)` | Estimate event probability |
| `simulate_brownian_motion(steps, dt, mu, sigma, ...)` | Simulate BM paths |
| `simulate_geometric_brownian_motion(S0, steps, ...)` | Simulate GBM paths |
| `importance_sampling_integrate(integrand, ...)` | Importance sampling integration |

### Utility Functions

| Function | Description |
|----------|-------------|
| `compute_confidence_interval(samples, confidence_level)` | Compute CI for sample mean |
| `compute_effective_sample_size(samples)` | ESS for autocorrelated samples |
| `convergence_diagnostics(samples, batch_size)` | Convergence statistics |

## Return Types

All simulations return `MCSimulationResult` with:
- `estimate`: Main estimate value
- `std_error`: Standard error of estimate
- `confidence_interval`: Tuple of (lower, upper) bounds
- `stats`: Detailed `MCStats` object
- `success`: Boolean indicating success
- `message`: Status message

## Mathematical Background

### Monte Carlo Integration
For function f(x) over interval [a, b]:
$$\int_a^b f(x) dx \approx (b-a) \cdot \frac{1}{n} \sum_{i=1}^n f(X_i)$$
where $X_i$ are uniform random samples in [a, b].

### π Estimation
Probability that random point (x, y) in [0,1]×[0,1] lies inside quarter circle:
$$P = \frac{\pi/4}{1} = \frac{\pi}{4}$$
Thus: $\pi \approx 4 \cdot \frac{\text{hits}}{\text{total throws}}$

### Option Pricing (Black-Scholes-Merton)
Stock price follows geometric Brownian motion:
$$S_T = S_0 \exp\left((r - \frac{\sigma^2}{2})T + \sigma\sqrt{T} Z\right)$$
Call option price: $C = e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]$

## Testing

Run tests with:
```bash
python monte_carlo_utils_test.py
```

All tests should pass. Tests cover:
- Basic simulation functionality
- Integration (1D and N-dimensional)
- Option pricing and put-call parity
- Risk measures (VaR, ES)
- Probability estimation
- Brownian motion statistics
- Edge cases and reproducibility

## Examples

See `examples/usage_examples.py` for comprehensive usage demonstrations.

## License

MIT License - Part of AllToolkit Collection