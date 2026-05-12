#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Monte Carlo Utilities Test Suite
==============================================
Comprehensive tests for the Monte Carlo simulation module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import math
import random
import sys
sys.path.insert(0, '.')

from mod import (
    MonteCarlo,
    MCConfig,
    MCStats,
    MCSimulationResult,
    SamplingMethod,
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
    compute_effective_sample_size,
    convergence_diagnostics
)


class TestMCConfig(unittest.TestCase):
    """Test MCConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = MCConfig()
        self.assertEqual(config.num_samples, 10000)
        self.assertEqual(config.seed, None)
        self.assertEqual(config.confidence_level, 0.95)
        self.assertEqual(config.sampling_method, SamplingMethod.UNIFORM)
        self.assertEqual(config.batch_size, 1000)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = MCConfig(
            num_samples=50000,
            seed=12345,
            confidence_level=0.99,
            verbose=True
        )
        self.assertEqual(config.num_samples, 50000)
        self.assertEqual(config.seed, 12345)
        self.assertEqual(config.confidence_level, 0.99)
        self.assertTrue(config.verbose)


class TestMonteCarlo(unittest.TestCase):
    """Test MonteCarlo class."""
    
    def test_simple_simulation(self):
        """Test basic Monte Carlo simulation."""
        def sample_func():
            return random.random()
        
        config = MCConfig(num_samples=1000, seed=42)
        mc = MonteCarlo(sample_func, config)
        result = mc.simulate()
        
        self.assertTrue(result.success)
        self.assertGreater(result.estimate, 0)
        self.assertLess(result.estimate, 1)
        self.assertEqual(result.stats.num_samples, 1000)
    
    def test_1d_integration(self):
        """Test 1D Monte Carlo integration."""
        mc = MonteCarlo(config=MCConfig(num_samples=10000, seed=42))
        result = mc.integrate_1d(lambda x: x**2, 0, 1)
        
        self.assertTrue(result.success)
        # Integral of x^2 from 0 to 1 is 1/3
        self.assertAlmostEqual(result.estimate, 1/3, places=2)
    
    def test_nd_integration(self):
        """Test N-dimensional Monte Carlo integration."""
        mc = MonteCarlo(config=MCConfig(num_samples=10000, seed=42))
        
        # Integrate f(x,y) = x + y over [0,1] x [0,1]
        # Result should be 1
        def integrand(point):
            return point[0] + point[1]
        
        result = mc.integrate_nd(integrand, [(0, 1), (0, 1)])
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, 1.0, places=1)
    
    def test_add_sample(self):
        """Test adding samples manually."""
        mc = MonteCarlo(config=MCConfig(seed=42))
        
        mc.add_sample(1.0)
        mc.add_sample(2.0)
        mc.add_sample(3.0)
        
        stats = mc.compute_statistics()
        
        self.assertEqual(stats.num_samples, 3)
        self.assertAlmostEqual(stats.estimate, 2.0)
        self.assertAlmostEqual(stats.min_value, 1.0)
        self.assertAlmostEqual(stats.max_value, 3.0)
    
    def test_statistics(self):
        """Test statistics computation."""
        mc = MonteCarlo(config=MCConfig(seed=42))
        
        for i in range(100):
            mc.add_sample(i)
        
        stats = mc.compute_statistics()
        
        self.assertEqual(stats.num_samples, 100)
        self.assertAlmostEqual(stats.estimate, 49.5, places=1)
        self.assertGreater(stats.std_error, 0)
        self.assertEqual(len(stats.confidence_interval), 2)
    
    def test_reset(self):
        """Test reset functionality."""
        mc = MonteCarlo(config=MCConfig(seed=42))
        
        mc.add_sample(1.0)
        mc.add_sample(2.0)
        self.assertEqual(len(mc.samples), 2)
        
        mc.reset()
        self.assertEqual(len(mc.samples), 0)
        self.assertEqual(mc.running_sum, 0.0)


class TestEstimatePi(unittest.TestCase):
    """Test π estimation."""
    
    def test_pi_estimation(self):
        """Test that π estimation is reasonably accurate."""
        result = estimate_pi(100000, seed=42)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, math.pi, places=2)
        self.assertIn("π", result.message)
    
    def test_pi_confidence_interval(self):
        """Test that true π is within confidence interval."""
        result = estimate_pi(100000, seed=42)
        
        lower, upper = result.confidence_interval
        self.assertLess(lower, math.pi)
        self.assertGreater(upper, math.pi)
    
    def test_pi_convergence(self):
        """Test that more samples give better estimate."""
        result_small = estimate_pi(1000, seed=42)
        result_large = estimate_pi(100000, seed=42)
        
        error_small = abs(result_small.estimate - math.pi)
        error_large = abs(result_large.estimate - math.pi)
        
        # More samples should generally give smaller error
        # (with high probability, though not guaranteed)
        self.assertGreater(result_small.std_error, result_large.std_error)


class TestOptionPricing(unittest.TestCase):
    """Test option pricing functions."""
    
    def test_call_option(self):
        """Test European call option pricing."""
        result = price_european_call(
            S0=100, K=100, T=1, r=0.05, sigma=0.2,
            num_samples=100000, seed=42
        )
        
        self.assertTrue(result.success)
        self.assertGreater(result.estimate, 0)
        
        # At-the-money call should be positive
        # Black-Scholes formula gives approximately 10.45 for these parameters
        # Monte Carlo estimate should be within reasonable range
        self.assertAlmostEqual(result.estimate, 10.45, places=0)  # Within ~1
    
    def test_put_option(self):
        """Test European put option pricing."""
        result = price_european_put(
            S0=100, K=100, T=1, r=0.05, sigma=0.2,
            num_samples=100000, seed=42
        )
        
        self.assertTrue(result.success)
        self.assertGreater(result.estimate, 0)
        
        # At-the-money put should be around 5.57 for these parameters
        self.assertAlmostEqual(result.estimate, 5.57, places=1)
    
    def test_put_call_parity(self):
        """Test put-call parity relationship."""
        S0 = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        
        call_result = price_european_call(S0, K, T, r, sigma, num_samples=100000, seed=42)
        put_result = price_european_put(S0, K, T, r, sigma, num_samples=100000, seed=42)
        
        # Put-call parity: C - P = S0 - K * e^(-rT)
        parity_diff = call_result.estimate - put_result.estimate
        theoretical_diff = S0 - K * math.exp(-r * T)
        
        # Allow for Monte Carlo noise - within ~0.5 should be fine
        self.assertAlmostEqual(parity_diff, theoretical_diff, places=0)
    
    def test_deep_in_the_money_call(self):
        """Test deep in-the-money call option."""
        result = price_european_call(
            S0=200, K=100, T=1, r=0.05, sigma=0.2,
            num_samples=100000, seed=42
        )
        
        # Deep ITM call should be close to S0 - K * e^(-rT)
        intrinsic = 200 - 100 * math.exp(-0.05)
        self.assertGreater(result.estimate, intrinsic * 0.9)


class TestValueAtRisk(unittest.TestCase):
    """Test Value at Risk functions."""
    
    def test_var_calculation(self):
        """Test VaR calculation."""
        returns = [random.gauss(0.001, 0.02) for _ in range(100)]
        result = value_at_risk(returns, confidence_level=0.95, 
                               initial_value=1000000, seed=42)
        
        self.assertTrue(result.success)
        self.assertGreater(result.estimate, 0)
        self.assertIn("VaR", result.message)
    
    def test_var_empty_returns(self):
        """Test VaR with insufficient returns."""
        result = value_at_risk([0.01])
        
        self.assertFalse(result.success)
    
    def test_expected_shortfall(self):
        """Test Expected Shortfall calculation."""
        returns = [random.gauss(0.001, 0.02) for _ in range(100)]
        result = expected_shortfall(returns, confidence_level=0.95, 
                                     initial_value=1000000, seed=42)
        
        self.assertTrue(result.success)
        self.assertGreater(result.estimate, 0)
    
    def test_es_greater_than_var(self):
        """Test that ES >= VaR."""
        random.seed(42)
        returns = [random.gauss(0.001, 0.02) for _ in range(1000)]
        
        var_result = value_at_risk(returns, confidence_level=0.95, 
                                   initial_value=1000000, seed=42)
        es_result = expected_shortfall(returns, confidence_level=0.95, 
                                       initial_value=1000000, seed=42)
        
        # ES should be >= VaR (both are positive loss values)
        self.assertGreaterEqual(es_result.estimate, var_result.estimate)


class TestProbabilityEstimate(unittest.TestCase):
    """Test probability estimation."""
    
    def test_coin_flip(self):
        """Test probability of coin flip."""
        def heads():
            return random.random() < 0.5
        
        result = probability_estimate(heads, num_samples=100000, seed=42)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, 0.5, places=2)
    
    def test_dice_sum(self):
        """Test probability of dice sum."""
        def sum_geq_10():
            return random.randint(1, 6) + random.randint(1, 6) >= 10
        
        result = probability_estimate(sum_geq_10, num_samples=100000, seed=42)
        
        # P(sum >= 10) = P(10) + P(11) + P(12) = 3/36 + 2/36 + 1/36 = 6/36 = 1/6
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, 1/6, places=2)
    
    def test_rare_event(self):
        """Test probability of rare event."""
        def rare_event():
            return random.random() < 0.01
        
        result = probability_estimate(rare_event, num_samples=100000, seed=42)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, 0.01, places=2)


class TestBrownianMotion(unittest.TestCase):
    """Test Brownian motion simulation."""
    
    def test_brownian_motion_shape(self):
        """Test that Brownian motion returns correct shape."""
        result = simulate_brownian_motion(steps=100, num_paths=1000, seed=42)
        
        self.assertEqual(len(result['paths']), 1000)
        self.assertEqual(len(result['paths'][0]), 101)  # 100 steps + initial
        self.assertEqual(len(result['mean_path']), 101)
    
    def test_brownian_motion_statistics(self):
        """Test Brownian motion statistics."""
        result = simulate_brownian_motion(
            steps=100, dt=0.01, mu=0, sigma=1, 
            num_paths=10000, seed=42
        )
        
        # For standard Brownian motion: E[W_T] = 0, Var[W_T] = T
        final_mean = result['final_mean']
        final_std = result['final_std']
        
        self.assertAlmostEqual(final_mean, 0.0, places=1)
        self.assertAlmostEqual(final_std, math.sqrt(1.0), places=1)
    
    def test_gbm_shape(self):
        """Test geometric Brownian motion returns correct shape."""
        result = simulate_geometric_brownian_motion(
            S0=100, steps=252, num_paths=1000, seed=42
        )
        
        self.assertEqual(len(result['paths']), 1000)
        self.assertEqual(len(result['paths'][0]), 253)
    
    def test_gbm_positive(self):
        """Test that GBM stays positive."""
        result = simulate_geometric_brownian_motion(
            S0=100, steps=100, num_paths=1000, seed=42
        )
        
        for path in result['paths']:
            for value in path:
                self.assertGreater(value, 0)


class TestImportanceSampling(unittest.TestCase):
    """Test importance sampling integration."""
    
    def test_normal_distribution(self):
        """Test integration using normal proposal."""
        def integrand(x):
            return math.exp(-x * x)
        
        def normal_pdf(x):
            return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
        
        def normal_sampler():
            return random.gauss(0, 1)
        
        result = importance_sampling_integrate(
            integrand, normal_pdf, normal_sampler,
            num_samples=10000, seed=42
        )
        
        # Integral of exp(-x^2) from -inf to inf is sqrt(pi)
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.estimate, math.sqrt(math.pi), places=1)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_confidence_interval(self):
        """Test confidence interval computation."""
        samples = [random.gauss(0, 1) for _ in range(100)]
        ci = compute_confidence_interval(samples, 0.95)
        
        self.assertEqual(len(ci), 2)
        self.assertLess(ci[0], ci[1])
        
        # True mean (0) should be in CI with high probability
        self.assertLess(ci[0], 0)
        self.assertGreater(ci[1], 0)
    
    def test_effective_sample_size(self):
        """Test ESS computation."""
        # Independent samples should have ESS ≈ n
        samples = [random.random() for _ in range(1000)]
        ess = compute_effective_sample_size(samples)
        
        self.assertGreater(ess, 500)  # Should be close to n
        self.assertLess(ess, 1500)
    
    def test_convergence_diagnostics(self):
        """Test convergence diagnostics."""
        samples = [random.gauss(0, 1) for _ in range(1000)]
        diagnostics = convergence_diagnostics(samples, batch_size=100)
        
        self.assertIn('status', diagnostics)
        self.assertIn('ess', diagnostics)
        self.assertIn('r_hat', diagnostics)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_no_sample_function(self):
        """Test simulation without sample function."""
        mc = MonteCarlo(config=MCConfig(num_samples=100))
        result = mc.simulate()
        
        self.assertFalse(result.success)
        self.assertIn("No sample function", result.message)
    
    def test_single_sample(self):
        """Test with single sample."""
        mc = MonteCarlo(config=MCConfig(num_samples=1, seed=42))
        mc.add_sample(5.0)
        
        stats = mc.compute_statistics()
        self.assertEqual(stats.num_samples, 1)
        self.assertEqual(stats.estimate, 5.0)
    
    def test_zero_samples(self):
        """Test with zero samples."""
        mc = MonteCarlo(config=MCConfig(num_samples=0))
        stats = mc.compute_statistics()
        
        self.assertEqual(stats.num_samples, 0)
        self.assertEqual(stats.estimate, 0.0)
    
    def test_large_values(self):
        """Test with large sample values."""
        mc = MonteCarlo(config=MCConfig(seed=42))
        
        for _ in range(100):
            mc.add_sample(1e10)
        
        stats = mc.compute_statistics()
        self.assertAlmostEqual(stats.estimate, 1e10, places=-5)
    
    def test_negative_values(self):
        """Test with negative values."""
        mc = MonteCarlo(config=MCConfig(num_samples=100, seed=42))
        
        for _ in range(50):
            mc.add_sample(-1)
        for _ in range(50):
            mc.add_sample(1)
        
        stats = mc.compute_statistics()
        self.assertAlmostEqual(stats.estimate, 0.0, places=1)


class TestReproducibility(unittest.TestCase):
    """Test reproducibility with seeds."""
    
    def test_same_seed_same_result(self):
        """Test that same seed gives same result."""
        result1 = estimate_pi(10000, seed=12345)
        result2 = estimate_pi(10000, seed=12345)
        
        self.assertEqual(result1.estimate, result2.estimate)
    
    def test_different_seeds_different_result(self):
        """Test that different seeds give different results."""
        result1 = estimate_pi(10000, seed=111)
        result2 = estimate_pi(10000, seed=222)
        
        # With different seeds, results should differ (high probability)
        self.assertNotEqual(result1.estimate, result2.estimate)


if __name__ == "__main__":
    unittest.main(verbosity=2)