#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Monte Carlo Utilities Usage Examples
===================================================
Practical examples demonstrating Monte Carlo simulation capabilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '.')
import math
import random
from mod import (
    MonteCarlo,
    MCConfig,
    estimate_pi,
    price_european_call,
    price_european_put,
    value_at_risk,
    expected_shortfall,
    probability_estimate,
    simulate_brownian_motion,
    simulate_geometric_brownian_motion,
    importance_sampling_integrate,
    compute_confidence_interval,
    convergence_diagnostics
)


def example_estimate_pi():
    """Example 1: Estimating π using Monte Carlo."""
    print("=" * 60)
    print("Example 1: Estimating π using Monte Carlo")
    print("=" * 60)
    
    # The classic "dart board" method
    # Throw random points in a unit square and count those
    # that fall inside the quarter circle
    
    print("\nSimulating random throws at dart board...")
    
    # Different sample sizes to show convergence
    sample_sizes = [1000, 10000, 100000, 1000000]
    
    for n in sample_sizes:
        result = estimate_pi(n, seed=42)
        error = abs(result.estimate - math.pi)
        print(f"\nSamples: {n}")
        print(f"  Estimate: {result.estimate:.6f}")
        print(f"  True π:   {math.pi:.6f}")
        print(f"  Error:    {error:.6f}")
        print(f"  95% CI:   ({result.confidence_interval[0]:.6f}, {result.confidence_interval[1]:.6f})")
        print(f"  π in CI:  {'Yes' if result.confidence_interval[0] < math.pi < result.confidence_interval[1] else 'No'}")


def example_integration():
    """Example 2: Monte Carlo Integration."""
    print("\n" + "=" * 60)
    print("Example 2: Monte Carlo Integration")
    print("=" * 60)
    
    mc = MonteCarlo(config=MCConfig(num_samples=100000, seed=42))
    
    # 1D integration: x^2 from 0 to 1
    print("\nIntegrating x² from 0 to 1:")
    result = mc.integrate_1d(lambda x: x**2, 0, 1)
    true_value = 1/3
    print(f"  Monte Carlo: {result.estimate:.6f}")
    print(f"  Analytical:  {true_value:.6f}")
    print(f"  Error:       {abs(result.estimate - true_value):.6f}")
    
    # 1D integration: sin(x) from 0 to π
    print("\nIntegrating sin(x) from 0 to π:")
    result = mc.integrate_1d(lambda x: math.sin(x), 0, math.pi)
    true_value = 2.0
    print(f"  Monte Carlo: {result.estimate:.6f}")
    print(f"  Analytical:  {true_value:.6f}")
    print(f"  Error:       {abs(result.estimate - true_value):.6f}")
    
    # 2D integration: x*y over [0,1]×[0,1]
    print("\nIntegrating f(x,y) = xy over [0,1]×[0,1]:")
    result = mc.integrate_nd(lambda p: p[0]*p[1], [(0, 1), (0, 1)])
    true_value = 0.25
    print(f"  Monte Carlo: {result.estimate:.6f}")
    print(f"  Analytical:  {true_value:.6f}")
    print(f"  Error:       {abs(result.estimate - true_value):.6f}")
    
    # 3D integration: sphere volume
    print("\nIntegrating to find unit sphere volume (3D):")
    # Count points inside sphere (r^2 <= 1) in cube [-1,1]×[-1,1]×[-1,1]
    def inside_sphere(p):
        r2 = p[0]**2 + p[1]**2 + p[2]**2
        return 1.0 if r2 <= 1 else 0.0
    
    result = mc.integrate_nd(inside_sphere, [(-1, 1), (-1, 1), (-1, 1)])
    true_volume = 4/3 * math.pi
    print(f"  Monte Carlo: {result.estimate:.6f}")
    print(f"  True volume: {true_volume:.6f}")
    print(f"  Error:       {abs(result.estimate - true_volume):.6f}")


def example_option_pricing():
    """Example 3: Option Pricing."""
    print("\n" + "=" * 60)
    print("Example 3: European Option Pricing")
    print("=" * 60)
    
    # Parameters
    S0 = 100      # Current stock price
    K = 100       # Strike price (at-the-money)
    T = 1         # Time to maturity (1 year)
    r = 0.05      # Risk-free rate (5%)
    sigma = 0.2   # Volatility (20%)
    
    print(f"\nParameters:")
    print(f"  Stock price (S0): ${S0}")
    print(f"  Strike price (K):  ${K}")
    print(f"  Time to maturity: {T} year")
    print(f"  Risk-free rate:   {r*100}%")
    print(f"  Volatility:       {sigma*100}%")
    
    # Call option
    print("\nPricing European call option:")
    call_result = price_european_call(S0, K, T, r, sigma, num_samples=100000, seed=42)
    print(f"  Monte Carlo price: ${call_result.estimate:.4f}")
    print(f"  95% CI: (${call_result.confidence_interval[0]:.4f}, ${call_result.confidence_interval[1]:.4f})")
    
    # Put option
    print("\nPricing European put option:")
    put_result = price_european_put(S0, K, T, r, sigma, num_samples=100000, seed=42)
    print(f"  Monte Carlo price: ${put_result.estimate:.4f}")
    print(f"  95% CI: (${put_result.confidence_interval[0]:.4f}, ${put_result.confidence_interval[1]:.4f})")
    
    # Put-call parity verification
    print("\nPut-call parity check:")
    parity_diff = call_result.estimate - put_result.estimate
    theoretical_diff = S0 - K * math.exp(-r * T)
    print(f"  C - P (MC):      ${parity_diff:.4f}")
    print(f"  S0 - K*e^(-rT):  ${theoretical_diff:.4f}")
    print(f"  Parity holds:    {'Yes' if abs(parity_diff - theoretical_diff) < 0.5 else 'No'}")
    
    # Different strike prices
    print("\nCall prices for different strikes:")
    strikes = [90, 95, 100, 105, 110]
    for k in strikes:
        result = price_european_call(S0, k, T, r, sigma, num_samples=50000, seed=42)
        print(f"  K={k}: ${result.estimate:.4f}")


def example_risk_analysis():
    """Example 4: Risk Analysis."""
    print("\n" + "=" * 60)
    print("Example 4: Risk Analysis (VaR and Expected Shortfall)")
    print("=" * 60)
    
    # Simulate historical returns (e.g., daily stock returns)
    random.seed(42)
    mu = 0.0005  # Daily mean return (0.05%)
    sigma = 0.02  # Daily volatility (2%)
    n_days = 250  # 1 year of trading days
    
    historical_returns = [random.gauss(mu, sigma) for _ in range(n_days)]
    initial_value = 1000000  # $1 million portfolio
    
    print(f"\nPortfolio parameters:")
    print(f"  Initial value: ${initial_value:,}")
    print(f"  Historical returns: {n_days} days")
    print(f"  Mean daily return: {mu*100:.2f}%")
    print(f"  Daily volatility: {sigma*100:.1f}%")
    
    # Calculate VaR at different confidence levels
    print("\nValue at Risk (VaR):")
    for conf in [0.90, 0.95, 0.99]:
        var_result = value_at_risk(
            historical_returns, 
            confidence_level=conf,
            initial_value=initial_value,
            num_samples=100000,
            seed=42
        )
        print(f"  {conf*100:.0f}% VaR: ${var_result.estimate:,.2f}")
    
    # Calculate Expected Shortfall
    print("\nExpected Shortfall (CVaR):")
    for conf in [0.90, 0.95, 0.99]:
        es_result = expected_shortfall(
            historical_returns,
            confidence_level=conf,
            initial_value=initial_value,
            num_samples=100000,
            seed=42
        )
        print(f"  {conf*100:.0f}% ES:  ${es_result.estimate:,.2f}")
    
    # Compare VaR vs ES
    print("\nComparison (95% level):")
    var_95 = value_at_risk(historical_returns, 0.95, initial_value, seed=42)
    es_95 = expected_shortfall(historical_returns, 0.95, initial_value, seed=42)
    print(f"  VaR tells: worst 5% day loses at least ${var_95.estimate:,.2f}")
    print(f"  ES tells:  average loss in worst 5% is ${es_95.estimate:,.2f}")
    print(f"  ES/VaR ratio: {es_95.estimate/var_95.estimate:.2f}")


def example_probability():
    """Example 5: Probability Estimation."""
    print("\n" + "=" * 60)
    print("Example 5: Probability Estimation")
    print("=" * 60)
    
    # Coin flip probability
    print("\nProbability of heads in coin flip:")
    def coin_heads():
        return random.randint(0, 1) == 1
    
    result = probability_estimate(coin_heads, num_samples=100000, seed=42)
    print(f"  Monte Carlo: {result.estimate:.4f}")
    print(f"  Analytical:  0.5000")
    
    # Dice sum probability
    print("\nProbability of sum >= 10 with two dice:")
    def dice_sum_geq_10():
        return random.randint(1, 6) + random.randint(1, 6) >= 10
    
    result = probability_estimate(dice_sum_geq_10, num_samples=100000, seed=42)
    # P(sum >= 10) = P(10) + P(11) + P(12) = 3/36 + 2/36 + 1/36 = 6/36 = 1/6
    analytical = 1/6
    print(f"  Monte Carlo: {result.estimate:.4f}")
    print(f"  Analytical:  {analytical:.4f}")
    
    # Complex probability: birthday problem
    print("\nBirthday problem: P(shared birthday in n people):")
    def birthday_shared(n_people):
        birthdays = [random.randint(1, 365) for _ in range(n_people)]
        return len(set(birthdays)) < n_people
    
    for n in [10, 20, 23, 30, 40, 50]:
        result = probability_estimate(
            lambda: birthday_shared(n),
            num_samples=10000,
            seed=42
        )
        # Analytical for n=23 is ~0.507
        print(f"  n={n}: P(shared) ≈ {result.estimate:.3f}")


def example_brownian_motion():
    """Example 6: Brownian Motion Simulation."""
    print("\n" + "=" * 60)
    print("Example 6: Brownian Motion Simulation")
    print("=" * 60)
    
    # Standard Brownian motion
    print("\nStandard Brownian Motion (Wiener process):")
    bm_result = simulate_brownian_motion(
        steps=100,
        dt=0.01,
        mu=0,
        sigma=1,
        num_paths=10000,
        seed=42
    )
    
    print(f"  Steps: {bm_result['steps']}")
    print(f"  Time horizon: {bm_result['steps'] * bm_result['dt']:.2f}")
    print(f"  Final value mean: {bm_result['final_mean']:.4f} (should be ≈ 0)")
    print(f"  Final value std:  {bm_result['final_std']:.4f} (should be ≈ sqrt(T)={math.sqrt(1.0):.4f})")
    
    # Geometric Brownian Motion for stock prices
    print("\nGeometric Brownian Motion (stock price model):")
    gbm_result = simulate_geometric_brownian_motion(
        S0=100,
        steps=252,     # Trading days in 1 year
        dt=1/252,      # Daily time step
        mu=0.08,       # 8% annual expected return
        sigma=0.20,    # 20% annual volatility
        num_paths=10000,
        seed=42
    )
    
    # Expected value of GBM: E[S_T] = S0 * exp(mu * T)
    expected_final = 100 * math.exp(0.08 * 1)
    
    print(f"  Initial price: ${gbm_result['S0']}")
    print(f"  Expected return: {gbm_result['mu']*100:.0f}%")
    print(f"  Volatility: {gbm_result['sigma']*100:.0f}%")
    print(f"  Simulated mean final price: ${gbm_result['final_mean']:.2f}")
    print(f"  Expected final price:        ${expected_final:.2f}")
    print(f"  Simulated std:               ${gbm_result['final_std']:.2f}")
    
    # Confidence bands
    print("\nPrice distribution at year end:")
    print(f"  Mean: ${gbm_result['mean_path'][-1]:.2f}")
    print(f"  95% lower band: ${gbm_result['lower_band'][-1]:.2f}")
    print(f"  95% upper band: ${gbm_result['upper_band'][-1]:.2f}")


def example_importance_sampling():
    """Example 7: Importance Sampling for Integration."""
    print("\n" + "=" * 60)
    print("Example 7: Importance Sampling Integration")
    print("=" * 60)
    
    print("\nIntegrating exp(-x²) from -∞ to ∞ (should be √π ≈ 1.772)")
    
    # Standard Monte Carlo (uniform sampling is inefficient)
    # We'll use importance sampling with a normal proposal
    
    def integrand(x):
        return math.exp(-x * x)
    
    def normal_pdf(x):
        return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    
    def normal_sampler():
        return random.gauss(0, 1)
    
    result = importance_sampling_integrate(
        integrand,
        normal_pdf,
        normal_sampler,
        num_samples=10000,
        seed=42
    )
    
    print(f"  Monte Carlo (importance sampling): {result.estimate:.6f}")
    print(f"  True value (√π):                    {math.sqrt(math.pi):.6f}")
    print(f"  Error:                              {abs(result.estimate - math.sqrt(math.pi)):.6f}")


def example_convergence_analysis():
    """Example 8: Convergence Analysis."""
    print("\n" + "=" * 60)
    print("Example 8: Convergence Diagnostics")
    print("=" * 60)
    
    random.seed(42)
    
    # Generate samples from a simulation
    samples = [random.gauss(0, 1) for _ in range(10000)]
    
    # Compute convergence diagnostics
    diagnostics = convergence_diagnostics(samples, batch_size=100)
    
    print("\nSimulation convergence analysis:")
    print(f"  Total samples: {diagnostics['n']}")
    print(f"  R-hat:         {diagnostics['r_hat']:.4f} (< 1.1 indicates convergence)")
    print(f"  ESS:           {diagnostics['ess']:.1f}")
    print(f"  Status:        {diagnostics['status']}")
    
    # Confidence interval
    ci = compute_confidence_interval(samples, 0.95)
    print(f"\n95% Confidence interval for mean:")
    print(f"  Lower: {ci[0]:.4f}")
    print(f"  Upper: {ci[1]:.4f}")
    print(f"  True mean (0) in CI: {'Yes' if ci[0] < 0 < ci[1] else 'No'}")


def example_custom_simulation():
    """Example 9: Custom Monte Carlo Simulation."""
    print("\n" + "=" * 60)
    print("Example 9: Custom Monte Carlo Simulation")
    print("=" * 60)
    
    # Simulate a complex scenario: investment outcome
    print("\nSimulating 10-year investment outcome:")
    print("  Initial investment: $10,000")
    print("  Annual return distribution: normal(mean=7%, std=15%)")
    print("  Simulation: compound growth over 10 years")
    
    def investment_outcome():
        # Compound growth with random annual returns
        value = 10000
        for _ in range(10):
            annual_return = random.gauss(0.07, 0.15)
            value *= (1 + annual_return)
        return value
    
    mc = MonteCarlo(config=MCConfig(num_samples=10000, seed=42))
    result = mc.simulate(investment_outcome)
    
    print(f"\nResults after 10 years:")
    print(f"  Expected final value: ${result.estimate:,.2f}")
    print(f"  Standard error:       ${result.std_error:,.2f}")
    print(f"  95% CI: (${result.confidence_interval[0]:,.2f}, ${result.confidence_interval[1]:,.2f})")
    print(f"  Min outcome:          ${result.stats.min_value:,.2f}")
    print(f"  Max outcome:          ${result.stats.max_value:,.2f}")
    
    # Compute probability of various outcomes
    outcomes = result.stats.samples
    prob_double = len([v for v in outcomes if v >= 20000]) / len(outcomes)
    prob_loss = len([v for v in outcomes if v < 10000]) / len(outcomes)
    
    print(f"\nOutcome probabilities:")
    print(f"  P(double investment): {prob_double:.1%}")
    print(f"  P(any loss):           {prob_loss:.1%}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Monte Carlo Utilities - Usage Examples")
    print("=" * 60)
    
    example_estimate_pi()
    example_integration()
    example_option_pricing()
    example_risk_analysis()
    example_probability()
    example_brownian_motion()
    example_importance_sampling()
    example_convergence_analysis()
    example_custom_simulation()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()