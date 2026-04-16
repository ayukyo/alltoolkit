"""
Value Noise Implementation

Simple noise algorithm using interpolated random values.
Faster than Perlin/Simplex but less smooth.
Good for performance-critical applications.
"""

import math
import random
from typing import List, Optional, Callable


class ValueNoise:
    """
    Value Noise Generator
    
    Interpolates between random values on a grid.
    Simpler and faster than gradient noise but produces blockier results.
    
    Example:
        noise = ValueNoise(seed=42, interpolation='cubic')
        value = noise.noise2d(x=1.5, y=2.3)
    """
    
    def __init__(
        self, 
        seed: Optional[int] = None,
        interpolation: str = 'smoothstep'
    ):
        """
        Initialize Value Noise generator.
        
        Args:
            seed: Random seed for reproducibility
            interpolation: Interpolation method - 'linear', 'cosine', 
                          'smoothstep', 'smootherstep', 'cubic'
        """
        self.seed = seed
        self.interpolation = interpolation
        self._values = self._generate_values(seed)
        
        # Set interpolation function
        self._interp_func = self._get_interp_func(interpolation)
    
    def _generate_values(self, seed: Optional[int]) -> List[float]:
        """Generate random value table."""
        rng = random.Random(seed)
        return [rng.uniform(-1, 1) for _ in range(256)]
    
    def _get_interp_func(self, method: str) -> Callable[[float, float, float], float]:
        """Get interpolation function by name."""
        def linear(a: float, b: float, t: float) -> float:
            return a + t * (b - a)
        
        def cosine(a: float, b: float, t: float) -> float:
            t2 = (1 - math.cos(t * math.pi)) / 2
            return a * (1 - t2) + b * t2
        
        def smoothstep(a: float, b: float, t: float) -> float:
            t2 = t * t * (3 - 2 * t)
            return a + t2 * (b - a)
        
        def smootherstep(a: float, b: float, t: float) -> float:
            t2 = t * t * t * (t * (t * 6 - 15) + 10)
            return a + t2 * (b - a)
        
        def cubic(a: float, b: float, t: float) -> float:
            # Catmull-Rom style cubic interpolation
            t2 = t * t
            t3 = t2 * t
            return a * (2 * t3 - 3 * t2 + 1) + b * (-2 * t3 + 3 * t2)
        
        funcs = {
            'linear': linear,
            'cosine': cosine,
            'smoothstep': smoothstep,
            'smootherstep': smootherstep,
            'cubic': cubic
        }
        
        return funcs.get(method, smoothstep)
    
    def _get_value(self, i: int) -> float:
        """Get value with wrapping."""
        return self._values[i & 255]
    
    def _get_value_2d(self, i: int, j: int) -> float:
        """Get 2D value with hashing."""
        h = (i * 127 + j * 311) & 255
        return self._values[h]
    
    def noise1d(self, x: float) -> float:
        """
        Generate 1D value noise.
        
        Args:
            x: X coordinate
            
        Returns:
            Noise value in range [-1, 1]
        """
        i = int(math.floor(x))
        t = x - i
        
        v0 = self._get_value(i - 1)
        v1 = self._get_value(i)
        v2 = self._get_value(i + 1)
        v3 = self._get_value(i + 2)
        
        if self.interpolation == 'cubic':
            # Cubic interpolation
            t2 = t * t
            t3 = t2 * t
            
            return (
                v0 * (-t3 + 2 * t2 - t) +
                v1 * (3 * t3 - 5 * t2 + 2) +
                v2 * (-3 * t3 + 4 * t2 + t) +
                v3 * (t3 - t2)
            ) / 2
        else:
            return self._interp_func(v1, v2, t)
    
    def noise2d(self, x: float, y: float) -> float:
        """
        Generate 2D value noise.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Noise value in range [-1, 1]
        """
        i = int(math.floor(x))
        j = int(math.floor(y))
        
        u = x - i
        v = y - j
        
        # Get 4 corner values
        v00 = self._get_value_2d(i, j)
        v10 = self._get_value_2d(i + 1, j)
        v01 = self._get_value_2d(i, j + 1)
        v11 = self._get_value_2d(i + 1, j + 1)
        
        # Bilinear interpolation
        interp_x1 = self._interp_func(v00, v10, u)
        interp_x2 = self._interp_func(v01, v11, u)
        
        return self._interp_func(interp_x1, interp_x2, v)
    
    def __call__(self, x: float, y: float = 0) -> float:
        """Convenient callable interface."""
        if y == 0:
            return self.noise1d(x)
        return self.noise2d(x, y)


def value_noise(
    x: float, 
    y: float = 0, 
    seed: Optional[int] = None,
    interpolation: str = 'smoothstep'
) -> float:
    """
    Generate value noise.
    
    Args:
        x: X coordinate
        y: Y coordinate (0 for 1D noise)
        seed: Optional seed
        interpolation: 'linear', 'cosine', 'smoothstep', 'smootherstep', 'cubic'
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = ValueNoise(seed=seed, interpolation=interpolation)
    if y == 0:
        return noise.noise1d(x)
    return noise.noise2d(x, y)