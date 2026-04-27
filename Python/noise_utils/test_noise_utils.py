"""
Tests for Noise Utils

Comprehensive tests for all noise generation algorithms.
Run from the parent directory: python -m noise_utils.test_noise_utils
"""

import unittest
import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from noise_utils.perlin import PerlinNoise, perlin_noise, perlin_noise_2d, perlin_noise_3d
from noise_utils.simplex import SimplexNoise, simplex_noise_2d, simplex_noise_3d
from noise_utils.value import ValueNoise, value_noise
from noise_utils.worley import WorleyNoise, worley_noise
from noise_utils.fractal import (
    fractal_brownian_motion, 
    turbulence, 
    ridged_noise,
    billow_noise,
    hybrid_multifractal
)
from noise_utils.warp import domain_warp, domain_warp_flow, domain_warp_color, warp_with_fbm


class TestPerlinNoise(unittest.TestCase):
    """Tests for Perlin Noise."""
    
    def test_noise_range(self):
        """Noise output should be in [-1, 1] range."""
        noise = PerlinNoise(seed=42)
        for _ in range(100):
            value = noise.noise2d(
                __import__('random').random() * 100,
                __import__('random').random() * 100
            )
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, 1.0)
    
    def test_reproducibility(self):
        """Same seed should produce same results."""
        noise1 = PerlinNoise(seed=42)
        noise2 = PerlinNoise(seed=42)
        
        for i in range(10):
            self.assertAlmostEqual(
                noise1.noise2d(i * 0.5, i * 0.3),
                noise2.noise2d(i * 0.5, i * 0.3),
                places=10
            )
    
    def test_different_seeds(self):
        """Different seeds should produce different results."""
        noise1 = PerlinNoise(seed=42)
        noise2 = PerlinNoise(seed=24)
        
        different = False
        # Use non-integer coordinates to avoid grid alignment
        for i in range(10):
            if abs(noise1.noise2d(i * 0.73, i * 0.57) - 
                   noise2.noise2d(i * 0.73, i * 0.57)) > 0.001:
                different = True
                break
        
        self.assertTrue(different)
    
    def test_continuity(self):
        """Noise should be continuous (smooth)."""
        noise = PerlinNoise(seed=42)
        
        # Small step should produce small change
        x, y = 10.0, 10.0
        step = 0.01
        
        for _ in range(10):
            v1 = noise.noise2d(x, y)
            v2 = noise.noise2d(x + step, y)
            v3 = noise.noise2d(x, y + step)
            
            # Change should be small for small step
            self.assertLess(abs(v1 - v2), 0.1)
            self.assertLess(abs(v1 - v3), 0.1)
            
            x += 0.1
            y += 0.1
    
    def test_3d_noise(self):
        """3D noise should work correctly."""
        noise = PerlinNoise(seed=42)
        value = noise.noise3d(1.5, 2.3, 0.7)
        
        self.assertIsInstance(value, float)
        self.assertGreaterEqual(value, -1.0)
        self.assertLessEqual(value, 1.0)
    
    def test_callable(self):
        """Callable interface should work."""
        noise = PerlinNoise(seed=42)
        value = noise(1.5, 2.3)
        self.assertIsInstance(value, float)
    
    def test_convenience_functions(self):
        """Convenience functions should work."""
        v1 = perlin_noise(1.5, 2.3)
        v2 = perlin_noise_2d(1.5, 2.3, scale=0.5)
        v3 = perlin_noise_3d(1.5, 2.3, 0.5)
        
        self.assertIsInstance(v1, float)
        self.assertIsInstance(v2, float)
        self.assertIsInstance(v3, float)


class TestSimplexNoise(unittest.TestCase):
    """Tests for Simplex Noise."""
    
    def test_noise_range(self):
        """Noise output should be in [-1, 1] range."""
        noise = SimplexNoise(seed=42)
        for _ in range(100):
            value = noise.noise2d(
                __import__('random').random() * 100,
                __import__('random').random() * 100
            )
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, 1.0)
    
    def test_reproducibility(self):
        """Same seed should produce same results."""
        noise1 = SimplexNoise(seed=42)
        noise2 = SimplexNoise(seed=42)
        
        for i in range(10):
            self.assertAlmostEqual(
                noise1.noise2d(i * 0.5, i * 0.3),
                noise2.noise2d(i * 0.5, i * 0.3),
                places=10
            )
    
    def test_3d_noise(self):
        """3D noise should work correctly."""
        noise = SimplexNoise(seed=42)
        value = noise.noise3d(1.5, 2.3, 0.7)
        
        self.assertIsInstance(value, float)
        self.assertGreaterEqual(value, -1.0)
        self.assertLessEqual(value, 1.0)
    
    def test_convenience_functions(self):
        """Convenience functions should work."""
        v1 = simplex_noise_2d(1.5, 2.3)
        v2 = simplex_noise_3d(1.5, 2.3, 0.5)
        
        self.assertIsInstance(v1, float)
        self.assertIsInstance(v2, float)


class TestValueNoise(unittest.TestCase):
    """Tests for Value Noise."""
    
    def test_noise_range(self):
        """Noise output should be in [-1, 1] range."""
        noise = ValueNoise(seed=42)
        for _ in range(100):
            value = noise.noise2d(
                __import__('random').random() * 100,
                __import__('random').random() * 100
            )
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, 1.0)
    
    def test_interpolation_methods(self):
        """Different interpolation methods should work."""
        methods = ['linear', 'cosine', 'smoothstep', 'smootherstep', 'cubic']
        
        for method in methods:
            noise = ValueNoise(seed=42, interpolation=method)
            value = noise.noise2d(1.5, 2.3)
            self.assertIsInstance(value, float)
    
    def test_1d_noise(self):
        """1D noise should work correctly."""
        noise = ValueNoise(seed=42)
        value = noise.noise1d(1.5)
        
        self.assertIsInstance(value, float)
        self.assertGreaterEqual(value, -1.0)
        self.assertLessEqual(value, 1.0)
    
    def test_convenience_function(self):
        """Convenience function should work."""
        v = value_noise(1.5, 2.3, seed=42)
        self.assertIsInstance(v, float)


class TestWorleyNoise(unittest.TestCase):
    """Tests for Worley/Cellular Noise."""
    
    def test_noise_positive(self):
        """F1 distance should be positive."""
        noise = WorleyNoise(seed=42)
        for _ in range(50):
            value = noise.noise2d(
                __import__('random').random() * 100,
                __import__('random').random() * 100
            )
            self.assertGreaterEqual(value, 0.0)
    
    def test_modes(self):
        """Different modes should work."""
        noise = WorleyNoise(seed=42)
        modes = ['F1', 'F2', 'F2-F1', 'F1*F2']
        
        for mode in modes:
            value = noise.noise2d(1.5, 2.3, mode=mode)
            self.assertIsInstance(value, float)
    
    def test_distance_metrics(self):
        """Different distance metrics should work."""
        metrics = ['euclidean', 'manhattan', 'chebyshev']
        
        for metric in metrics:
            noise = WorleyNoise(seed=42, distance_metric=metric)
            value = noise.noise2d(1.5, 2.3)
            self.assertIsInstance(value, float)
    
    def test_get_distances(self):
        """get_distances should return sorted distances."""
        noise = WorleyNoise(seed=42, num_points=8)
        distances = noise.get_distances(1.5, 2.3)
        
        self.assertIsInstance(distances, list)
        self.assertGreater(len(distances), 0)
        
        # Check sorted
        for i in range(len(distances) - 1):
            self.assertLessEqual(distances[i], distances[i + 1])
    
    def test_convenience_function(self):
        """Convenience function should work."""
        v = worley_noise(1.5, 2.3, seed=42)
        self.assertIsInstance(v, float)


class TestFractalFunctions(unittest.TestCase):
    """Tests for fractal noise functions."""
    
    def test_fbm_range(self):
        """fBm should produce values roughly in [-1, 1]."""
        noise = PerlinNoise(seed=42)
        for _ in range(50):
            value = fractal_brownian_motion(
                __import__('random').random() * 10,
                __import__('random').random() * 10,
                noise=noise
            )
            self.assertGreaterEqual(value, -1.5)
            self.assertLessEqual(value, 1.5)
    
    def test_fbm_octaves(self):
        """More octaves should add detail."""
        noise = PerlinNoise(seed=42)
        
        v1 = fractal_brownian_motion(5.0, 5.0, noise=noise, octaves=2)
        v4 = fractal_brownian_motion(5.0, 5.0, noise=noise, octaves=8)
        
        # Results should be different (more detail)
        # Not testing specific values, just that it runs
        self.assertIsInstance(v1, float)
        self.assertIsInstance(v4, float)
    
    def test_turbulence_positive(self):
        """Turbulence should produce positive values."""
        noise = PerlinNoise(seed=42)
        for _ in range(20):
            value = turbulence(
                __import__('random').random() * 10,
                __import__('random').random() * 10,
                noise=noise
            )
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
    
    def test_ridged_noise(self):
        """Ridged noise should produce values in expected range."""
        noise = PerlinNoise(seed=42)
        for _ in range(20):
            value = ridged_noise(
                __import__('random').random() * 10,
                __import__('random').random() * 10,
                noise=noise
            )
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, 1.0)
    
    def test_billow_noise(self):
        """Billow noise should produce positive values."""
        noise = PerlinNoise(seed=42)
        for _ in range(20):
            value = billow_noise(
                __import__('random').random() * 10,
                __import__('random').random() * 10,
                noise=noise
            )
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
    
    def test_hybrid_multifractal(self):
        """Hybrid multifractal should work."""
        noise = PerlinNoise(seed=42)
        value = hybrid_multifractal(5.0, 5.0, noise=noise)
        self.assertIsInstance(value, float)
    
    def test_default_noise(self):
        """Functions should work with default noise."""
        v1 = fractal_brownian_motion(1.5, 2.3)
        v2 = turbulence(1.5, 2.3)
        v3 = ridged_noise(1.5, 2.3)
        
        self.assertIsInstance(v1, float)
        self.assertIsInstance(v2, float)
        self.assertIsInstance(v3, float)


class TestDomainWarp(unittest.TestCase):
    """Tests for domain warping functions."""
    
    def test_domain_warp(self):
        """Basic domain warp should work."""
        noise = PerlinNoise(seed=42)
        value = domain_warp(1.5, 2.3, noise=noise)
        
        self.assertIsInstance(value, float)
    
    def test_domain_warp_iterations(self):
        """Different iterations should work."""
        noise = PerlinNoise(seed=42)
        
        v1 = domain_warp(1.5, 2.3, noise=noise, iterations=1)
        v2 = domain_warp(1.5, 2.3, noise=noise, iterations=3)
        
        self.assertIsInstance(v1, float)
        self.assertIsInstance(v2, float)
    
    def test_domain_warp_flow(self):
        """Animated flow should work."""
        noise = SimplexNoise(seed=42)
        value = domain_warp_flow(1.5, 2.3, 0.5, noise=noise)
        
        self.assertIsInstance(value, float)
    
    def test_domain_warp_color(self):
        """Color generation should work."""
        noise = SimplexNoise(seed=42)
        r, g, b = domain_warp_color(1.5, 2.3, noise=noise)
        
        self.assertIsInstance(r, float)
        self.assertIsInstance(g, float)
        self.assertIsInstance(b, float)
        
        # Values should be in [0, 1]
        for c in [r, g, b]:
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)
    
    def test_warp_with_fbm(self):
        """fBm warping should work."""
        noise = PerlinNoise(seed=42)
        value = warp_with_fbm(1.5, 2.3, noise=noise)
        
        self.assertIsInstance(value, float)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple noise types."""
    
    def test_terrain_generation(self):
        """Test typical terrain generation use case."""
        noise = SimplexNoise(seed=42)
        
        width, height = 64, 64
        scale = 0.02
        
        # Generate height map
        height_map = []
        for y in range(height):
            row = []
            for x in range(width):
                h = fractal_brownian_motion(
                    x * scale, y * scale,
                    noise=noise,
                    octaves=6,
                    persistence=0.5
                )
                row.append(h)
            height_map.append(row)
        
        # Check dimensions
        self.assertEqual(len(height_map), height)
        self.assertEqual(len(height_map[0]), width)
        
        # Values should be in reasonable range
        for row in height_map:
            for h in row:
                self.assertGreaterEqual(h, -1.5)
                self.assertLessEqual(h, 1.5)
    
    def test_different_noise_types_consistent(self):
        """Different noise types should produce consistent results."""
        import random
        random.seed(42)
        
        coords = [(random.random() * 100, random.random() * 100) for _ in range(10)]
        
        # Each noise type should be deterministic with seed
        for noise_class in [PerlinNoise, SimplexNoise, ValueNoise]:
            n1 = noise_class(seed=42)
            n2 = noise_class(seed=42)
            
            for x, y in coords:
                v1 = n1.noise2d(x, y)
                v2 = n2.noise2d(x, y)
                self.assertAlmostEqual(v1, v2, places=10)


if __name__ == '__main__':
    unittest.main()