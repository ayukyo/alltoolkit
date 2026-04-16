"""
Simplex Noise Implementation

Improved gradient noise algorithm by Ken Perlin.
Better performance and fewer artifacts than classic Perlin noise.
"""

import math
import random
from typing import List, Optional, Tuple


class SimplexNoise:
    """
    Simplex Noise Generator
    
    More efficient than Perlin noise with no directional artifacts.
    Great for real-time applications and procedural generation.
    
    Example:
        noise = SimplexNoise(seed=42)
        value = noise.noise2d(x=1.5, y=2.3)
        # Animated noise
        for t in range(frames):
            cloud[t] = noise.noise3d(x, y, t * 0.1)
    """
    
    # Gradient vectors for 2D
    _GRAD2: List[Tuple[int, int]] = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]
    
    # Gradient vectors for 3D
    _GRAD3: List[Tuple[int, int, int]] = [
        (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
        (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
        (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1)
    ]
    
    # Skew/unskew factors for 2D
    _F2 = 0.5 * (math.sqrt(3.0) - 1.0)
    _G2 = (3.0 - math.sqrt(3.0)) / 6.0
    
    # Skew/unskew factors for 3D
    _F3 = 1.0 / 3.0
    _G3 = 1.0 / 6.0
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize Simplex Noise generator.
        
        Args:
            seed: Random seed for reproducible noise.
        """
        self._perm = self._generate_permutation(seed)
    
    def _generate_permutation(self, seed: Optional[int]) -> List[int]:
        """Generate permutation table."""
        perm = list(range(256))
        if seed is not None:
            rng = random.Random(seed)
            rng.shuffle(perm)
        return perm + perm
    
    def _dot2(self, g: Tuple[int, int], x: float, y: float) -> float:
        """Dot product for 2D gradient."""
        return g[0] * x + g[1] * y
    
    def _dot3(self, g: Tuple[int, int, int], x: float, y: float, z: float) -> float:
        """Dot product for 3D gradient."""
        return g[0] * x + g[1] * y + g[2] * z
    
    def noise2d(self, x: float, y: float) -> float:
        """
        Generate 2D Simplex noise value.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Noise value in range [-1, 1]
        """
        # Skew input space
        s = (x + y) * self._F2
        i = int(math.floor(x + s))
        j = int(math.floor(y + s))
        
        t = (i + j) * self._G2
        x0 = i - t
        y0 = j - t
        x0 = x - x0
        y0 = y - y0
        
        # Determine which simplex we're in
        if x0 > y0:
            i1, j1 = 1, 0  # Lower triangle
        else:
            i1, j1 = 0, 1  # Upper triangle
        
        # Offsets for middle and last corners
        x1 = x0 - i1 + self._G2
        y1 = y0 - j1 + self._G2
        x2 = x0 - 1.0 + 2.0 * self._G2
        y2 = y0 - 1.0 + 2.0 * self._G2
        
        # Hash coordinates
        ii = i & 255
        jj = j & 255
        
        # Calculate contributions from three corners
        n0 = n1 = n2 = 0.0
        
        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 >= 0:
            t0 *= t0
            gi0 = self._perm[ii + self._perm[jj]] % 8
            n0 = t0 * t0 * self._dot2(self._GRAD2[gi0], x0, y0)
        
        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 >= 0:
            t1 *= t1
            gi1 = self._perm[ii + i1 + self._perm[jj + j1]] % 8
            n1 = t1 * t1 * self._dot2(self._GRAD2[gi1], x1, y1)
        
        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 >= 0:
            t2 *= t2
            gi2 = self._perm[ii + 1 + self._perm[jj + 1]] % 8
            n2 = t2 * t2 * self._dot2(self._GRAD2[gi2], x2, y2)
        
        # Scale to [-1, 1]
        return 70.0 * (n0 + n1 + n2)
    
    def noise3d(self, x: float, y: float, z: float) -> float:
        """
        Generate 3D Simplex noise value.
        
        Args:
            x, y, z: Coordinates
            
        Returns:
            Noise value in range [-1, 1]
        """
        # Skew input space
        s = (x + y + z) * self._F3
        i = int(math.floor(x + s))
        j = int(math.floor(y + s))
        k = int(math.floor(z + s))
        
        t = (i + j + k) * self._G3
        x0 = i - t
        y0 = j - t
        z0 = k - t
        x0 = x - x0
        y0 = y - y0
        z0 = z - z0
        
        # Determine simplex
        if x0 >= y0:
            if y0 >= z0:
                i1, j1, k1, i2, j2, k2 = 1, 0, 0, 1, 1, 0
            elif x0 >= z0:
                i1, j1, k1, i2, j2, k2 = 1, 0, 0, 1, 0, 1
            else:
                i1, j1, k1, i2, j2, k2 = 0, 0, 1, 1, 0, 1
        else:
            if y0 < z0:
                i1, j1, k1, i2, j2, k2 = 0, 0, 1, 0, 1, 1
            elif x0 < z0:
                i1, j1, k1, i2, j2, k2 = 0, 1, 0, 0, 1, 1
            else:
                i1, j1, k1, i2, j2, k2 = 0, 1, 0, 1, 1, 0
        
        # Offsets
        x1 = x0 - i1 + self._G3
        y1 = y0 - j1 + self._G3
        z1 = z0 - k1 + self._G3
        x2 = x0 - i2 + 2.0 * self._G3
        y2 = y0 - j2 + 2.0 * self._G3
        z2 = z0 - k2 + 2.0 * self._G3
        x3 = x0 - 1.0 + 3.0 * self._G3
        y3 = y0 - 1.0 + 3.0 * self._G3
        z3 = z0 - 1.0 + 3.0 * self._G3
        
        # Hash coordinates
        ii = i & 255
        jj = j & 255
        kk = k & 255
        
        # Calculate contributions from four corners
        n0 = n1 = n2 = n3 = 0.0
        
        t0 = 0.6 - x0 * x0 - y0 * y0 - z0 * z0
        if t0 >= 0:
            t0 *= t0
            gi0 = self._perm[ii + self._perm[jj + self._perm[kk]]] % 12
            n0 = t0 * t0 * self._dot3(self._GRAD3[gi0], x0, y0, z0)
        
        t1 = 0.6 - x1 * x1 - y1 * y1 - z1 * z1
        if t1 >= 0:
            t1 *= t1
            gi1 = self._perm[ii + i1 + self._perm[jj + j1 + self._perm[kk + k1]]] % 12
            n1 = t1 * t1 * self._dot3(self._GRAD3[gi1], x1, y1, z1)
        
        t2 = 0.6 - x2 * x2 - y2 * y2 - z2 * z2
        if t2 >= 0:
            t2 *= t2
            gi2 = self._perm[ii + i2 + self._perm[jj + j2 + self._perm[kk + k2]]] % 12
            n2 = t2 * t2 * self._dot3(self._GRAD3[gi2], x2, y2, z2)
        
        t3 = 0.6 - x3 * x3 - y3 * y3 - z3 * z3
        if t3 >= 0:
            t3 *= t3
            gi3 = self._perm[ii + 1 + self._perm[jj + 1 + self._perm[kk + 1]]] % 12
            n3 = t3 * t3 * self._dot3(self._GRAD3[gi3], x3, y3, z3)
        
        # Scale to [-1, 1]
        return 32.0 * (n0 + n1 + n2 + n3)
    
    def __call__(self, x: float, y: float, z: float = 0) -> float:
        """Convenient callable interface."""
        if z == 0:
            return self.noise2d(x, y)
        return self.noise3d(x, y, z)


# Convenience functions
def simplex_noise_2d(x: float, y: float, seed: Optional[int] = None) -> float:
    """
    Generate 2D Simplex noise.
    
    Args:
        x, y: Coordinates
        seed: Optional seed for reproducibility
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = SimplexNoise(seed=seed)
    return noise.noise2d(x, y)


def simplex_noise_3d(
    x: float, 
    y: float, 
    z: float, 
    seed: Optional[int] = None
) -> float:
    """
    Generate 3D Simplex noise.
    
    Args:
        x, y, z: Coordinates
        seed: Optional seed for reproducibility
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = SimplexNoise(seed=seed)
    return noise.noise3d(x, y, z)