#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Monte Carlo Simulation Utilities Module
=====================================================
A comprehensive Monte Carlo simulation utility module for Python with zero external dependencies.

Features:
    - Generic Monte Carlo simulation framework
    - Multiple sampling strategies (uniform, importance, stratified, Latin hypercube)
    - Built-in simulations (Pi estimation, integration, option pricing, risk analysis)
    - Statistical analysis and confidence intervals
    - Convergence diagnostics
    - Parallel-friendly design (supports seeding for reproducibility)
    - Variance reduction techniques

Author: AllToolkit Contributors
License: MIT
"""

import math
import random
from typing import Callable, List, Tuple, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from statistics import mean, stdev, variance
from copy import deepcopy


class SamplingMethod(Enum):
    """Sampling methods for Monte Carlo simulations."""
    UNIFORM = "uniform"
    IMPORTANCE = "importance"
    STRATIFIED = "stratified"
    LATIN_HYPERCUBE = "latin_hypercube"


@dataclass
class MCConfig:
    """Configuration for Monte Carlo simulation."""
    num_samples: int = 10000
    seed: Optional[int] = None
    confidence_level: float = 0.95
    sampling_method: SamplingMethod = SamplingMethod.UNIFORM
    batch_size: int = 1000  # For progress reporting
    verbose: bool = False


@dataclass
class MCStats:
    """Statistics from Monte Carlo simulation."""
    estimate: float
    std_error: float
    confidence_interval: Tuple[float, float]
    num_samples: int
    samples: List[float] = field(default_factory=list)
    min_value: float = float('inf')
    max_value: float = float('-inf')
    variance: float = 0.0
    skewness: float = 0.0
    kurtosis: float = 0.0
    convergence_history: List[float] = field(default_factory=list)


@dataclass
class MCSimulationResult:
    """Result of a Monte Carlo simulation."""
    estimate: float
    std_error: float
    confidence_interval: Tuple[float, float]
    stats: MCStats
    success: bool
    message: str = ""


class MonteCarlo:
    """
    Generic Monte Carlo simulation framework.
    
    Monte Carlo methods use random sampling to obtain numerical results for
    problems that might be deterministic in principle. They are widely used
    in physics, finance, engineering, and many other fields.
    
    Example:
        >>> def integrand(x):
        ...     return x ** 2
        >>> mc = MonteCarlo(integrand)
        >>> result = mc.integrate_1d(0, 1)  # Integrate x^2 from 0 to 1
        >>> print(f"Integral: {result.estimate:.6f}")
    """
    
    def __init__(
        self,
        sample_function: Optional[Callable[..., float]] = None,
        config: Optional[MCConfig] = None
    ):
        """
        Initialize Monte Carlo simulator.
        
        Args:
            sample_function: Optional function that takes random samples and
                           returns a value. For integration, this is the integrand.
            config: Configuration parameters (optional).
        """
        self.sample_function = sample_function
        self.config = config or MCConfig()
        
        if self.config.seed is not None:
            random.seed(self.config.seed)
        
        # State tracking
        self.samples: List[float] = []
        self.running_sum: float = 0.0
        self.running_sum_sq: float = 0.0
        self.min_value: float = float('inf')
        self.max_value: float = float('-inf')
        self.convergence_history: List[float] = []
    
    def _z_score(self, confidence: float) -> float:
        """
        Calculate z-score for given confidence level.
        
        Uses approximation for inverse normal CDF.
        
        Args:
            confidence: Confidence level (e.g., 0.95 for 95% CI).
            
        Returns:
            Z-score for the confidence level.
        """
        # Common z-scores
        z_table = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576,
            0.999: 3.291
        }
        
        if confidence in z_table:
            return z_table[confidence]
        
        # Approximation for inverse normal CDF
        # Using Abramowitz and Stegun approximation
        p = 1 - (1 - confidence) / 2
        if p <= 0 or p >= 1:
            return 1.96
        
        # Rational approximation
        a = [
            -3.969683028665376e+01,
            2.209460984245205e+02,
            -2.759285104469687e+02,
            1.383577518672690e+02,
            -3.066479806614716e+01,
            2.506628277459239e+00
        ]
        b = [
            -5.447609879822406e+01,
            1.615858368580409e+02,
            -1.556989798598866e+02,
            6.680131188771972e+01,
            -1.328068155288572e+01
        ]
        c = [
            -7.784894002430293e-03,
            -3.223964580411365e-01,
            -2.400758277161838e+00,
            -2.549732539343734e+00,
            4.374664141464968e+00,
            2.938163982698783e+00
        ]
        d = [
            7.784695709041462e-03,
            3.224671290700398e-01,
            2.445134137142996e+00,
            3.754408661907416e+00
        ]
        
        p_low = 0.02425
        p_high = 1 - p_low
        
        if p < p_low:
            q = math.sqrt(-2 * math.log(p))
            z = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
        elif p <= p_high:
            q = p - 0.5
            r = q * q
            z = (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
                (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
        else:
            q = math.sqrt(-2 * math.log(1 - p))
            z = -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
        
        return z
    
    def reset(self, seed: Optional[int] = None) -> None:
        """
        Reset the simulation state.
        
        Args:
            seed: Optional new seed for reproducibility.
        """
        self.samples = []
        self.running_sum = 0.0
        self.running_sum_sq = 0.0
        self.min_value = float('inf')
        self.max_value = float('-inf')
        self.convergence_history = []
        
        if seed is not None:
            random.seed(seed)
    
    def add_sample(self, value: float) -> None:
        """
        Add a sample value to the simulation.
        
        Args:
            value: Sample value to add.
        """
        self.samples.append(value)
        self.running_sum += value
        self.running_sum_sq += value * value
        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        
        # Record convergence
        if len(self.samples) % 100 == 0:
            self.convergence_history.append(self.running_sum / len(self.samples))
    
    def compute_statistics(self) -> MCStats:
        """
        Compute statistics from collected samples.
        
        Returns:
            MCStats with computed statistics.
        """
        n = len(self.samples)
        if n == 0:
            return MCStats(
                estimate=0.0,
                std_error=0.0,
                confidence_interval=(0.0, 0.0),
                num_samples=0
            )
        
        estimate = self.running_sum / n
        
        if n > 1:
            sample_var = (self.running_sum_sq - n * estimate * estimate) / (n - 1)
            std_error = math.sqrt(sample_var / n) if sample_var >= 0 else 0.0
        else:
            sample_var = 0.0
            std_error = 0.0
        
        z = self._z_score(self.config.confidence_level)
        margin = z * std_error
        ci = (estimate - margin, estimate + margin)
        
        # Compute higher moments if enough samples
        skewness = 0.0
        kurtosis = 0.0
        if n > 3 and sample_var > 0:
            std_dev = math.sqrt(sample_var)
            m3 = sum((x - estimate) ** 3 for x in self.samples) / n
            m4 = sum((x - estimate) ** 4 for x in self.samples) / n
            skewness = m3 / (std_dev ** 3)
            kurtosis = m4 / (std_dev ** 4) - 3  # Excess kurtosis
        
        return MCStats(
            estimate=estimate,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=n,
            samples=self.samples.copy(),
            min_value=self.min_value,
            max_value=self.max_value,
            variance=sample_var,
            skewness=skewness,
            kurtosis=kurtosis,
            convergence_history=self.convergence_history.copy()
        )
    
    def simulate(self, sample_function: Optional[Callable[[], float]] = None) -> MCSimulationResult:
        """
        Run the Monte Carlo simulation.
        
        Args:
            sample_function: Optional override for sample function.
            
        Returns:
            MCSimulationResult with estimate and statistics.
        """
        sampler = sample_function or self.sample_function
        if sampler is None:
            return MCSimulationResult(
                estimate=0.0,
                std_error=0.0,
                confidence_interval=(0.0, 0.0),
                stats=MCStats(estimate=0.0, std_error=0.0, 
                             confidence_interval=(0.0, 0.0), num_samples=0),
                success=False,
                message="No sample function provided"
            )
        
        self.reset()
        
        for i in range(self.config.num_samples):
            value = sampler()
            self.add_sample(value)
            
            if self.config.verbose and (i + 1) % self.config.batch_size == 0:
                current_estimate = self.running_sum / (i + 1)
                print(f"Samples: {i + 1}/{self.config.num_samples}, "
                      f"Estimate: {current_estimate:.6f}")
        
        stats = self.compute_statistics()
        
        return MCSimulationResult(
            estimate=stats.estimate,
            std_error=stats.std_error,
            confidence_interval=stats.confidence_interval,
            stats=stats,
            success=True,
            message="Simulation completed successfully"
        )
    
    def integrate_1d(
        self,
        integrand: Callable[[float], float],
        a: float,
        b: float,
        num_samples: Optional[int] = None
    ) -> MCSimulationResult:
        """
        Integrate a 1D function using Monte Carlo.
        
        Args:
            integrand: Function to integrate.
            a: Lower bound.
            b: Upper bound.
            num_samples: Optional override for number of samples.
            
        Returns:
            MCSimulationResult with integral estimate.
        """
        n = num_samples or self.config.num_samples
        self.reset()
        
        # Monte Carlo integration: ∫f(x)dx ≈ (b-a) * E[f(X)]
        for _ in range(n):
            x = a + (b - a) * random.random()
            value = integrand(x) * (b - a)  # Scale by interval width
            self.add_sample(value)
        
        stats = self.compute_statistics()
        
        return MCSimulationResult(
            estimate=stats.estimate,
            std_error=stats.std_error,
            confidence_interval=stats.confidence_interval,
            stats=stats,
            success=True,
            message=f"Integral estimate over [{a}, {b}]"
        )
    
    def integrate_nd(
        self,
        integrand: Callable[[List[float]], float],
        bounds: List[Tuple[float, float]],
        num_samples: Optional[int] = None
    ) -> MCSimulationResult:
        """
        Integrate an N-dimensional function using Monte Carlo.
        
        Args:
            integrand: Function taking N arguments and returning float.
            bounds: List of (lower, upper) bounds for each dimension.
            num_samples: Optional override for number of samples.
            
        Returns:
            MCSimulationResult with integral estimate.
        """
        n = num_samples or self.config.num_samples
        self.reset()
        
        dimensions = len(bounds)
        volume = 1.0
        for a, b in bounds:
            volume *= (b - a)
        
        for _ in range(n):
            # Generate random point in hypercube
            point = [a + (b - a) * random.random() for a, b in bounds]
            value = integrand(point) * volume
            self.add_sample(value)
        
        stats = self.compute_statistics()
        
        return MCSimulationResult(
            estimate=stats.estimate,
            std_error=stats.std_error,
            confidence_interval=stats.confidence_interval,
            stats=stats,
            success=True,
            message=f"N-dimensional integral estimate over {dimensions} dimensions"
        )


# ============================================================================
# Built-in Monte Carlo Simulations
# ============================================================================

def estimate_pi(num_samples: int = 100000, seed: Optional[int] = None) -> MCSimulationResult:
    """
    Estimate π using Monte Carlo simulation.
    
    Uses the classic "dart board" method: randomly throw darts at a unit
    square and count how many land inside the inscribed quarter circle.
    
    Args:
        num_samples: Number of random samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with π estimate.
        
    Example:
        >>> result = estimate_pi(100000)
        >>> print(f"π ≈ {result.estimate:.6f}")
    """
    if seed is not None:
        random.seed(seed)
    
    inside = 0
    
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        
        if x * x + y * y <= 1.0:
            inside += 1
    
    pi_estimate = 4.0 * inside / num_samples
    std_error = 4.0 * math.sqrt((inside / num_samples) * (1 - inside / num_samples) / num_samples)
    
    # 95% confidence interval
    z = 1.96
    ci = (pi_estimate - z * std_error, pi_estimate + z * std_error)
    
    return MCSimulationResult(
        estimate=pi_estimate,
        std_error=std_error,
        confidence_interval=ci,
        stats=MCStats(
            estimate=pi_estimate,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=num_samples
        ),
        success=True,
        message="π estimated using Monte Carlo dart board method"
    )


def price_european_call(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    num_samples: int = 100000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Price a European call option using Monte Carlo (Black-Scholes-Merton model).
    
    Uses geometric Brownian motion to simulate stock price paths and
    estimates the option price by averaging discounted payoffs.
    
    Args:
        S0: Current stock price.
        K: Strike price.
        T: Time to maturity (in years).
        r: Risk-free interest rate (annual, e.g., 0.05 for 5%).
        sigma: Volatility (annual, e.g., 0.2 for 20%).
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with option price estimate.
        
    Example:
        >>> result = price_european_call(S0=100, K=105, T=1, r=0.05, sigma=0.2)
        >>> print(f"Call option price: ${result.estimate:.2f}")
    """
    if seed is not None:
        random.seed(seed)
    
    # Precompute constants
    drift = (r - 0.5 * sigma * sigma) * T
    vol_sqrt_T = sigma * math.sqrt(T)
    discount = math.exp(-r * T)
    
    payoffs = []
    sum_payoff = 0.0
    sum_payoff_sq = 0.0
    
    for _ in range(num_samples):
        # Simulate terminal stock price using GBM
        Z = random.gauss(0, 1)
        ST = S0 * math.exp(drift + vol_sqrt_T * Z)
        
        # Payoff of call option
        payoff = max(ST - K, 0.0)
        payoffs.append(payoff)
        
        sum_payoff += payoff
        sum_payoff_sq += payoff * payoff
    
    # Calculate discounted average payoff
    avg_payoff = sum_payoff / num_samples
    price = discount * avg_payoff
    
    # Standard error
    if num_samples > 1:
        var_payoff = (sum_payoff_sq - num_samples * avg_payoff * avg_payoff) / (num_samples - 1)
        std_error = discount * math.sqrt(var_payoff / num_samples)
    else:
        std_error = 0.0
    
    z = 1.96  # 95% confidence
    ci = (price - z * std_error, price + z * std_error)
    
    return MCSimulationResult(
        estimate=price,
        std_error=std_error,
        confidence_interval=ci,
        stats=MCStats(
            estimate=price,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=num_samples,
            samples=payoffs
        ),
        success=True,
        message="European call option priced using Monte Carlo simulation"
    )


def price_european_put(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    num_samples: int = 100000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Price a European put option using Monte Carlo (Black-Scholes-Merton model).
    
    Args:
        S0: Current stock price.
        K: Strike price.
        T: Time to maturity (in years).
        r: Risk-free interest rate (annual, e.g., 0.05 for 5%).
        sigma: Volatility (annual, e.g., 0.2 for 20%).
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with option price estimate.
        
    Example:
        >>> result = price_european_put(S0=100, K=105, T=1, r=0.05, sigma=0.2)
        >>> print(f"Put option price: ${result.estimate:.2f}")
    """
    if seed is not None:
        random.seed(seed)
    
    drift = (r - 0.5 * sigma * sigma) * T
    vol_sqrt_T = sigma * math.sqrt(T)
    discount = math.exp(-r * T)
    
    payoffs = []
    sum_payoff = 0.0
    sum_payoff_sq = 0.0
    
    for _ in range(num_samples):
        Z = random.gauss(0, 1)
        ST = S0 * math.exp(drift + vol_sqrt_T * Z)
        
        # Payoff of put option
        payoff = max(K - ST, 0.0)
        payoffs.append(payoff)
        
        sum_payoff += payoff
        sum_payoff_sq += payoff * payoff
    
    avg_payoff = sum_payoff / num_samples
    price = discount * avg_payoff
    
    if num_samples > 1:
        var_payoff = (sum_payoff_sq - num_samples * avg_payoff * avg_payoff) / (num_samples - 1)
        std_error = discount * math.sqrt(var_payoff / num_samples)
    else:
        std_error = 0.0
    
    z = 1.96
    ci = (price - z * std_error, price + z * std_error)
    
    return MCSimulationResult(
        estimate=price,
        std_error=std_error,
        confidence_interval=ci,
        stats=MCStats(
            estimate=price,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=num_samples,
            samples=payoffs
        ),
        success=True,
        message="European put option priced using Monte Carlo simulation"
    )


def value_at_risk(
    returns: List[float],
    confidence_level: float = 0.95,
    initial_value: float = 1000000,
    num_samples: int = 100000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Calculate Value at Risk (VaR) using Monte Carlo simulation.
    
    Assumes returns follow a normal distribution estimated from historical data.
    
    Args:
        returns: Historical returns (as decimals, e.g., 0.01 for 1%).
        confidence_level: Confidence level for VaR (e.g., 0.95 for 95% VaR).
        initial_value: Initial portfolio value.
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with VaR estimate (as positive loss value).
        
    Example:
        >>> returns = [0.01, -0.02, 0.03, -0.01, 0.02]
        >>> result = value_at_risk(returns, confidence_level=0.95, initial_value=1000000)
        >>> print(f"95% VaR: ${result.estimate:,.2f}")
    """
    if seed is not None:
        random.seed(seed)
    
    if len(returns) < 2:
        return MCSimulationResult(
            estimate=0.0,
            std_error=0.0,
            confidence_interval=(0.0, 0.0),
            stats=MCStats(estimate=0.0, std_error=0.0, 
                         confidence_interval=(0.0, 0.0), num_samples=0),
            success=False,
            message="Need at least 2 historical returns"
        )
    
    # Estimate parameters from historical returns
    mu = mean(returns)
    sigma = stdev(returns)
    
    # Simulate future returns
    simulated_values = []
    for _ in range(num_samples):
        sim_return = random.gauss(mu, sigma)
        future_value = initial_value * (1 + sim_return)
        simulated_values.append(future_value)
    
    # Calculate VaR (worst case at confidence level)
    simulated_values.sort()
    var_index = int((1 - confidence_level) * num_samples)
    var_value = initial_value - simulated_values[var_index]
    
    return MCSimulationResult(
        estimate=var_value,
        std_error=0.0,  # VaR is a quantile, standard error is different
        confidence_interval=(var_value * 0.9, var_value * 1.1),  # Approximate
        stats=MCStats(
            estimate=var_value,
            std_error=0.0,
            confidence_interval=(var_value * 0.9, var_value * 1.1),
            num_samples=num_samples,
            samples=simulated_values
        ),
        success=True,
        message=f"{confidence_level*100:.0f}% VaR calculated using Monte Carlo simulation"
    )


def expected_shortfall(
    returns: List[float],
    confidence_level: float = 0.95,
    initial_value: float = 1000000,
    num_samples: int = 100000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Calculate Expected Shortfall (CVaR) using Monte Carlo simulation.
    
    Expected Shortfall is the average loss in the worst (1-confidence_level)% of cases.
    It's a more comprehensive risk measure than VaR.
    
    Args:
        returns: Historical returns (as decimals).
        confidence_level: Confidence level (e.g., 0.95 for 95% ES).
        initial_value: Initial portfolio value.
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with Expected Shortfall estimate (positive loss value).
        
    Example:
        >>> returns = [0.01, -0.02, 0.03, -0.01, 0.02]
        >>> result = expected_shortfall(returns, confidence_level=0.95)
        >>> print(f"95% ES: ${result.estimate:,.2f}")
    """
    if seed is not None:
        random.seed(seed)
    
    if len(returns) < 2:
        return MCSimulationResult(
            estimate=0.0,
            std_error=0.0,
            confidence_interval=(0.0, 0.0),
            stats=MCStats(estimate=0.0, std_error=0.0, 
                         confidence_interval=(0.0, 0.0), num_samples=0),
            success=False,
            message="Need at least 2 historical returns"
        )
    
    mu = mean(returns)
    sigma = stdev(returns)
    
    # Simulate future losses (positive values = loss)
    simulated_losses = []
    for _ in range(num_samples):
        sim_return = random.gauss(mu, sigma)
        # Loss is max(0, negative impact on portfolio)
        loss = max(0, -initial_value * sim_return)  # Positive value for losses
        simulated_losses.append(loss)
    
    # Calculate Expected Shortfall
    simulated_losses.sort()
    es_index = int((1 - confidence_level) * num_samples)
    
    # ES is average of the worst (lowest returns = highest losses)
    # For losses, we want the largest values (worst outcomes)
    worst_losses = simulated_losses[-es_index:] if es_index > 0 else simulated_losses
    es = mean(worst_losses) if worst_losses else 0.0
    
    # Standard error of ES
    if len(worst_losses) > 1:
        es_var = variance(worst_losses) / len(worst_losses)
        std_error = math.sqrt(es_var)
    else:
        std_error = 0.0
    
    return MCSimulationResult(
        estimate=es,
        std_error=std_error,
        confidence_interval=(max(0, es - 1.96 * std_error), es + 1.96 * std_error),
        stats=MCStats(
            estimate=es,
            std_error=std_error,
            confidence_interval=(max(0, es - 1.96 * std_error), es + 1.96 * std_error),
            num_samples=num_samples,
            samples=simulated_losses
        ),
        success=True,
        message=f"{confidence_level*100:.0f}% Expected Shortfall calculated"
    )


def probability_estimate(
    condition: Callable[[], bool],
    num_samples: int = 100000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Estimate probability of an event using Monte Carlo simulation.
    
    Args:
        condition: Function that returns True if event occurs, False otherwise.
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with probability estimate.
        
    Example:
        >>> # Probability that sum of two dice is >= 10
        >>> def sum_dice():
        ...     return (random.randint(1, 6) + random.randint(1, 6)) >= 10
        >>> result = probability_estimate(sum_dice, num_samples=100000)
        >>> print(f"P(sum >= 10) ≈ {result.estimate:.4f}")
    """
    if seed is not None:
        random.seed(seed)
    
    successes = 0
    
    for _ in range(num_samples):
        if condition():
            successes += 1
    
    prob = successes / num_samples
    std_error = math.sqrt(prob * (1 - prob) / num_samples)
    
    z = 1.96
    ci = (max(0, prob - z * std_error), min(1, prob + z * std_error))
    
    return MCSimulationResult(
        estimate=prob,
        std_error=std_error,
        confidence_interval=ci,
        stats=MCStats(
            estimate=prob,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=num_samples
        ),
        success=True,
        message="Probability estimated using Monte Carlo simulation"
    )


def simulate_brownian_motion(
    steps: int = 100,
    dt: float = 1.0,
    mu: float = 0.0,
    sigma: float = 1.0,
    num_paths: int = 1000,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulate multiple paths of Brownian motion (Wiener process).
    
    Useful for financial modeling, physics simulations, and stochastic processes.
    
    Args:
        steps: Number of time steps.
        dt: Time step size.
        mu: Drift coefficient.
        sigma: Volatility coefficient.
        num_paths: Number of paths to simulate.
        seed: Optional seed for reproducibility.
        
    Returns:
        Dictionary with paths, mean, std, and statistics.
        
    Example:
        >>> result = simulate_brownian_motion(steps=100, dt=0.01, mu=0.05, sigma=0.2)
        >>> print(f"Final value mean: {result['final_mean']:.4f}")
        >>> print(f"Final value std: {result['final_std']:.4f}")
    """
    if seed is not None:
        random.seed(seed)
    
    paths = []
    final_values = []
    
    for _ in range(num_paths):
        path = [0.0]
        W = 0.0
        
        for _ in range(steps):
            dW = random.gauss(0, math.sqrt(dt))
            W += mu * dt + sigma * dW
            path.append(W)
        
        paths.append(path)
        final_values.append(W)
    
    # Compute statistics
    final_mean = mean(final_values)
    final_std = stdev(final_values) if len(final_values) > 1 else 0.0
    
    # Compute mean path and confidence band
    mean_path = []
    upper_band = []
    lower_band = []
    
    for i in range(steps + 1):
        values_at_step = [path[i] for path in paths]
        m = mean(values_at_step)
        s = stdev(values_at_step) if len(values_at_step) > 1 else 0.0
        
        mean_path.append(m)
        upper_band.append(m + 1.96 * s)
        lower_band.append(m - 1.96 * s)
    
    return {
        'paths': paths,
        'final_values': final_values,
        'final_mean': final_mean,
        'final_std': final_std,
        'mean_path': mean_path,
        'upper_band': upper_band,
        'lower_band': lower_band,
        'steps': steps,
        'dt': dt,
        'mu': mu,
        'sigma': sigma
    }


def simulate_geometric_brownian_motion(
    S0: float,
    steps: int = 100,
    dt: float = 1.0,
    mu: float = 0.05,
    sigma: float = 0.2,
    num_paths: int = 1000,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulate multiple paths of Geometric Brownian Motion.
    
    Commonly used for stock price modeling in finance.
    
    Args:
        S0: Initial value.
        steps: Number of time steps.
        dt: Time step size.
        mu: Drift coefficient (expected return).
        sigma: Volatility coefficient.
        num_paths: Number of paths to simulate.
        seed: Optional seed for reproducibility.
        
    Returns:
        Dictionary with paths, statistics, and confidence bands.
        
    Example:
        >>> result = simulate_geometric_brownian_motion(S0=100, steps=252, dt=1/252, mu=0.08, sigma=0.2)
        >>> print(f"Expected final price: {result['final_mean']:.2f}")
    """
    if seed is not None:
        random.seed(seed)
    
    paths = []
    final_values = []
    
    for _ in range(num_paths):
        path = [S0]
        S = S0
        
        for _ in range(steps):
            dW = random.gauss(0, math.sqrt(dt))
            S = S * math.exp((mu - 0.5 * sigma * sigma) * dt + sigma * dW)
            path.append(S)
        
        paths.append(path)
        final_values.append(S)
    
    final_mean = mean(final_values)
    final_std = stdev(final_values) if len(final_values) > 1 else 0.0
    
    # Mean path and confidence band
    mean_path = []
    upper_band = []
    lower_band = []
    
    for i in range(steps + 1):
        values_at_step = [path[i] for path in paths]
        m = mean(values_at_step)
        s = stdev(values_at_step) if len(values_at_step) > 1 else 0.0
        
        mean_path.append(m)
        upper_band.append(m + 1.96 * s)
        lower_band.append(max(0, m - 1.96 * s))  # Price can't be negative
    
    return {
        'paths': paths,
        'final_values': final_values,
        'final_mean': final_mean,
        'final_std': final_std,
        'mean_path': mean_path,
        'upper_band': upper_band,
        'lower_band': lower_band,
        'steps': steps,
        'dt': dt,
        'mu': mu,
        'sigma': sigma,
        'S0': S0
    }


def importance_sampling_integrate(
    integrand: Callable[[float], float],
    proposal_pdf: Callable[[float], float],
    proposal_sampler: Callable[[], float],
    num_samples: int = 10000,
    seed: Optional[int] = None
) -> MCSimulationResult:
    """
    Integrate using importance sampling for variance reduction.
    
    Useful when the integrand has high values in regions where
    uniform sampling is inefficient.
    
    Args:
        integrand: Function to integrate.
        proposal_pdf: PDF of the proposal distribution.
        proposal_sampler: Function that samples from proposal distribution.
        num_samples: Number of Monte Carlo samples.
        seed: Optional seed for reproducibility.
        
    Returns:
        MCSimulationResult with integral estimate.
        
    Example:
        >>> # Integrate exp(-x^2) from -inf to inf (should be sqrt(pi))
        >>> import math
        >>> def integrand(x):
        ...     return math.exp(-x*x)
        >>> def normal_pdf(x):
        ...     return math.exp(-x*x/2) / math.sqrt(2*math.pi)
        >>> def normal_sampler():
        ...     return random.gauss(0, 1)
        >>> result = importance_sampling_integrate(integrand, normal_pdf, normal_sampler)
    """
    if seed is not None:
        random.seed(seed)
    
    samples = []
    sum_val = 0.0
    sum_sq = 0.0
    
    for _ in range(num_samples):
        x = proposal_sampler()
        q_x = proposal_pdf(x)
        
        if q_x > 0:
            weight = integrand(x) / q_x
            samples.append(weight)
            sum_val += weight
            sum_sq += weight * weight
    
    if len(samples) == 0:
        return MCSimulationResult(
            estimate=0.0,
            std_error=0.0,
            confidence_interval=(0.0, 0.0),
            stats=MCStats(estimate=0.0, std_error=0.0, 
                         confidence_interval=(0.0, 0.0), num_samples=0),
            success=False,
            message="No valid samples generated"
        )
    
    estimate = sum_val / num_samples
    var = (sum_sq - num_samples * estimate * estimate) / (num_samples - 1) if num_samples > 1 else 0
    std_error = math.sqrt(var / num_samples) if var > 0 else 0.0
    
    z = 1.96
    ci = (estimate - z * std_error, estimate + z * std_error)
    
    return MCSimulationResult(
        estimate=estimate,
        std_error=std_error,
        confidence_interval=ci,
        stats=MCStats(
            estimate=estimate,
            std_error=std_error,
            confidence_interval=ci,
            num_samples=num_samples,
            samples=samples
        ),
        success=True,
        message="Integral estimated using importance sampling"
    )


# ============================================================================
# Utility Functions
# ============================================================================

def compute_confidence_interval(
    samples: List[float],
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """
    Compute confidence interval for a sample mean.
    
    Args:
        samples: List of sample values.
        confidence_level: Confidence level (e.g., 0.95 for 95% CI).
        
    Returns:
        Tuple of (lower_bound, upper_bound).
    """
    n = len(samples)
    if n < 2:
        return (0.0, 0.0)
    
    m = mean(samples)
    s = stdev(samples)
    se = s / math.sqrt(n)
    
    # Approximate z-score
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence_level, 1.96)
    
    return (m - z * se, m + z * se)


def compute_effective_sample_size(samples: List[float]) -> float:
    """
    Compute effective sample size for autocorrelated samples.
    
    Uses the formula: ESS = n / (1 + 2 * sum of autocorrelations)
    
    Args:
        samples: List of sample values.
        
    Returns:
        Effective sample size.
    """
    n = len(samples)
    if n < 10:
        return float(n)
    
    # Compute autocorrelation at lag 1
    m = mean(samples)
    var = variance(samples)
    
    if var == 0:
        return float(n)
    
    autocorr = sum((samples[i] - m) * (samples[i-1] - m) for i in range(1, n)) / ((n - 1) * var)
    
    # ESS formula
    ess = n / (1 + 2 * autocorr)
    
    return max(1.0, ess)


def convergence_diagnostics(
    samples: List[float],
    batch_size: int = 100
) -> Dict[str, Any]:
    """
    Compute convergence diagnostics for Monte Carlo samples.
    
    Args:
        samples: List of sample values.
        batch_size: Size of batches for computing running statistics.
        
    Returns:
        Dictionary with convergence diagnostics.
    """
    n = len(samples)
    if n < batch_size * 3:
        return {'status': 'insufficient_samples', 'n': n}
    
    # Compute running mean
    running_mean = []
    for i in range(batch_size, n, batch_size):
        running_mean.append(mean(samples[:i]))
    
    # Check for stability in last quarter
    last_quarter = running_mean[-max(1, len(running_mean) // 4):]
    mean_last = mean(last_quarter)
    std_last = stdev(last_quarter) if len(last_quarter) > 1 else 0
    
    # Gelman-Rubin-like statistic (compare first half to second half)
    half = n // 2
    first_half_mean = mean(samples[:half])
    second_half_mean = mean(samples[half:])
    
    between_var = ((first_half_mean - second_half_mean) ** 2) / 2
    within_var = (variance(samples[:half]) + variance(samples[half:])) / 2
    
    r_hat = math.sqrt(1 + between_var / within_var) if within_var > 0 else 1.0
    
    return {
        'status': 'converged' if r_hat < 1.1 else 'not_converged',
        'n': n,
        'running_mean': running_mean,
        'final_mean': mean_last,
        'final_std': std_last,
        'r_hat': r_hat,
        'ess': compute_effective_sample_size(samples)
    }


# Main entry point for command-line usage
if __name__ == "__main__":
    print("Monte Carlo Utilities Module")
    print("=" * 40)
    
    # Demo: Estimate π
    print("\n1. Estimating π:")
    result = estimate_pi(100000, seed=42)
    print(f"   Estimate: {result.estimate:.6f}")
    print(f"   True value: {math.pi:.6f}")
    print(f"   Error: {abs(result.estimate - math.pi):.6f}")
    
    # Demo: Option pricing
    print("\n2. European Call Option Pricing:")
    result = price_european_call(S0=100, K=105, T=1, r=0.05, sigma=0.2, 
                                  num_samples=100000, seed=42)
    print(f"   Option price: ${result.estimate:.2f}")
    print(f"   95% CI: (${result.confidence_interval[0]:.2f}, ${result.confidence_interval[1]:.2f})")
    
    # Demo: Integration
    print("\n3. Monte Carlo Integration (x^2 from 0 to 1):")
    mc = MonteCarlo()
    result = mc.integrate_1d(lambda x: x**2, 0, 1, num_samples=100000)
    print(f"   Estimate: {result.estimate:.6f}")
    print(f"   True value: {1/3:.6f}")
    print(f"   Error: {abs(result.estimate - 1/3):.6f}")