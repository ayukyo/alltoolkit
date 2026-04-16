"""
Perlin Noise Implementation

Classic gradient noise algorithm by Ken Perlin.
Produces smooth, natural-looking noise patterns.
"""

import math
import random
from typing import List, Tuple, Optional


class PerlinNoise:
    """
    Perlin Noise Generator
    
    Generates smooth, continuous noise with controllable frequency.
    Useful for terrain generation, texture synthesis, and procedural content.
    
    Example:
        noise = PerlinNoise(seed=42)
        value = noise.noise2d(x=1.5, y=2.3)
        # Generate terrain
        for y in range(height):
            for x in range(width):
                height_map[y][x] = noise.noise2d(x * scale, y * scale)
    """
    
    # Standard permutation table (duplicated for 512 elements)
    _PERMUTATION: List[int] = [
        151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
        140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
        247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
        57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
        74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
        60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
        65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
        200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
        52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
        207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
        119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
        129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
        218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
        81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
        184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
        222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180
    ]
    
    def __init__(self, seed: Optional[int] = None, octaves: int = 1):
        """
        Initialize Perlin Noise generator.
        
        Args:
            seed: Random seed for reproducible noise. None for random.
            octaves: Number of octaves for fractal noise (default 1).
        """
        self.octaves = octaves
        self._p = self._generate_permutation(seed)
    
    def _generate_permutation(self, seed: Optional[int]) -> List[int]:
        """Generate a shuffled permutation table."""
        perm = list(self._PERMUTATION)
        if seed is not None:
            rng = random.Random(seed)
            rng.shuffle(perm)
        # Duplicate for overflow handling
        return perm + perm
    
    def _fade(self, t: float) -> float:
        """Smoothstep function: 6t^5 - 15t^4 + 10t^3"""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation."""
        return a + t * (b - a)
    
    def _grad2d(self, hash_val: int, x: float, y: float) -> float:
        """2D gradient function."""
        h = hash_val & 7  # Use 8 gradients for 2D
        u = x if h < 4 else y
        v = y if h < 4 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
    
    def _grad3d(self, hash_val: int, x: float, y: float, z: float) -> float:
        """3D gradient function."""
        h = hash_val & 15
        u = x if h < 8 else y
        v = (y if h < 4 else (x if h == 12 or h == 14 else z))
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
    
    def noise2d(self, x: float, y: float) -> float:
        """
        Generate 2D Perlin noise value.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Noise value in range [-1, 1]
        """
        # Find unit grid cell containing point
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        
        # Relative position in cell
        xf = x - math.floor(x)
        yf = y - math.floor(y)
        
        # Fade curves
        u = self._fade(xf)
        v = self._fade(yf)
        
        # Hash coordinates of 4 corners
        aa = self._p[self._p[xi] + yi]
        ab = self._p[self._p[xi] + yi + 1]
        ba = self._p[self._p[xi + 1] + yi]
        bb = self._p[self._p[xi + 1] + yi + 1]
        
        # Gradient values
        x1 = self._lerp(
            self._grad2d(aa, xf, yf),
            self._grad2d(ba, xf - 1, yf),
            u
        )
        x2 = self._lerp(
            self._grad2d(ab, xf, yf - 1),
            self._grad2d(bb, xf - 1, yf - 1),
            u
        )
        
        return self._lerp(x1, x2, v)
    
    def noise3d(self, x: float, y: float, z: float) -> float:
        """
        Generate 3D Perlin noise value.
        
        Args:
            x: X coordinate
            y: Y coordinate  
            z: Z coordinate
            
        Returns:
            Noise value in range [-1, 1]
        """
        # Find unit grid cell
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        zi = int(math.floor(z)) & 255
        
        # Relative position
        xf = x - math.floor(x)
        yf = y - math.floor(y)
        zf = z - math.floor(z)
        
        # Fade curves
        u = self._fade(xf)
        v = self._fade(yf)
        w = self._fade(zf)
        
        # Hash coordinates of 8 corners
        aaa = self._p[self._p[self._p[xi] + yi] + zi]
        aab = self._p[self._p[self._p[xi] + yi] + zi + 1]
        aba = self._p[self._p[self._p[xi] + yi + 1] + zi]
        abb = self._p[self._p[self._p[xi] + yi + 1] + zi + 1]
        baa = self._p[self._p[self._p[xi + 1] + yi] + zi]
        bab = self._p[self._p[self._p[xi + 1] + yi] + zi + 1]
        bba = self._p[self._p[self._p[xi + 1] + yi + 1] + zi]
        bbb = self._p[self._p[self._p[xi + 1] + yi + 1] + zi + 1]
        
        # Interpolate
        x1 = self._lerp(
            self._grad3d(aaa, xf, yf, zf),
            self._grad3d(baa, xf - 1, yf, zf),
            u
        )
        x2 = self._lerp(
            self._grad3d(aba, xf, yf - 1, zf),
            self._grad3d(bba, xf - 1, yf - 1, zf),
            u
        )
        y1 = self._lerp(x1, x2, v)
        
        x1 = self._lerp(
            self._grad3d(aab, xf, yf, zf - 1),
            self._grad3d(bab, xf - 1, yf, zf - 1),
            u
        )
        x2 = self._lerp(
            self._grad3d(abb, xf, yf - 1, zf - 1),
            self._grad3d(bbb, xf - 1, yf - 1, zf - 1),
            u
        )
        y2 = self._lerp(x1, x2, v)
        
        return self._lerp(y1, y2, w)
    
    def __call__(self, x: float, y: float, z: float = 0) -> float:
        """Convenient callable interface."""
        if z == 0:
            return self.noise2d(x, y)
        return self.noise3d(x, y, z)


# Convenience functions
def perlin_noise(x: float, y: float, seed: Optional[int] = None) -> float:
    """
    Generate 2D Perlin noise value.
    
    Args:
        x: X coordinate
        y: Y coordinate
        seed: Optional seed for reproducibility
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = PerlinNoise(seed=seed)
    return noise.noise2d(x, y)


def perlin_noise_2d(
    x: float, 
    y: float, 
    scale: float = 1.0,
    seed: Optional[int] = None
) -> float:
    """
    Generate 2D Perlin noise with scale.
    
    Args:
        x: X coordinate
        y: Y coordinate
        scale: Frequency scale (higher = more detail)
        seed: Optional seed
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = PerlinNoise(seed=seed)
    return noise.noise2d(x * scale, y * scale)


def perlin_noise_3d(
    x: float,
    y: float,
    z: float,
    scale: float = 1.0,
    seed: Optional[int] = None
) -> float:
    """
    Generate 3D Perlin noise with scale.
    
    Args:
        x, y, z: Coordinates
        scale: Frequency scale
        seed: Optional seed
        
    Returns:
        Noise value in range [-1, 1]
    """
    noise = PerlinNoise(seed=seed)
    return noise.noise3d(x * scale, y * scale, z * scale)