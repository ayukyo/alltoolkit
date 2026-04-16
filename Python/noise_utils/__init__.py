"""
Noise Generation Utilities

A collection of noise generation algorithms for procedural content generation,
terrain generation, texture synthesis, and more.

Features:
- Perlin Noise (2D, 3D)
- Simplex Noise (2D, 3D)
- Value Noise
- Worley/Cellular Noise
- Fractal Brownian Motion (fBm)
- Turbulence
- Ridged Noise
- Domain Warping

Zero external dependencies - pure Python implementation.
"""

from .perlin import PerlinNoise, perlin_noise, perlin_noise_2d, perlin_noise_3d
from .simplex import SimplexNoise, simplex_noise_2d, simplex_noise_3d
from .value import ValueNoise, value_noise
from .worley import WorleyNoise, worley_noise
from .fractal import fractal_brownian_motion, turbulence, ridged_noise
from .warp import domain_warp

__version__ = "1.0.0"
__all__ = [
    # Perlin Noise
    "PerlinNoise",
    "perlin_noise",
    "perlin_noise_2d",
    "perlin_noise_3d",
    # Simplex Noise
    "SimplexNoise",
    "simplex_noise_2d",
    "simplex_noise_3d",
    # Value Noise
    "ValueNoise",
    "value_noise",
    # Worley Noise
    "WorleyNoise",
    "worley_noise",
    # Fractal Functions
    "fractal_brownian_motion",
    "turbulence",
    "ridged_noise",
    # Domain Warping
    "domain_warp",
]