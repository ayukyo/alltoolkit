"""
Domain Warping

Technique that warps the domain of noise functions,
creating organic, flowing patterns.
"""

import math
from typing import Optional, Callable

from .perlin import PerlinNoise
from .simplex import SimplexNoise


def domain_warp(
    x: float,
    y: float,
    noise: Optional[PerlinNoise] = None,
    warp_strength: float = 0.5,
    warp_scale: float = 0.01,
    iterations: int = 1
) -> float:
    """
    Domain Warping
    
    Warps the input coordinates using noise before sampling,
    creating organic, flowing patterns.
    
    Args:
        x, y: Input coordinates
        noise: Noise generator (default: PerlinNoise)
        warp_strength: How much to warp coordinates
        warp_scale: Scale of warping noise
        iterations: Number of warping iterations (1-3)
        
    Returns:
        Warped noise value
        
    Example:
        noise = PerlinNoise(seed=42)
        warped = domain_warp(x, y, noise, warp_strength=0.5, iterations=2)
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    for _ in range(iterations):
        # Warp coordinates using noise
        warp_x = noise.noise2d(x * warp_scale, y * warp_scale) * warp_strength
        warp_y = noise.noise2d(
            (x + 5.2) * warp_scale, 
            (y + 1.3) * warp_scale
        ) * warp_strength
        
        x += warp_x
        y += warp_y
    
    return noise.noise2d(x, y)


def domain_warp_flow(
    x: float,
    y: float,
    time: float,
    noise: Optional[SimplexNoise] = None,
    warp_strength: float = 0.3,
    flow_speed: float = 0.5
) -> float:
    """
    Animated Domain Warping with Flow
    
    Creates flowing, animated patterns perfect for water,
    clouds, or other fluid effects.
    
    Args:
        x, y: Input coordinates
        time: Animation time/phase
        noise: Noise generator (default: SimplexNoise)
        warp_strength: How much to warp coordinates
        flow_speed: Speed of flow animation
        
    Returns:
        Animated warped noise value
        
    Example:
        noise = SimplexNoise(seed=42)
        for t in range(100):
            value = domain_warp_flow(x, y, t * 0.1, noise)
    """
    if noise is None:
        noise = SimplexNoise(seed=42)
    
    # Flow direction based on time
    flow_angle = noise.noise2d(x * 0.01 + time * flow_speed, y * 0.01) * math.pi * 2
    
    # Warp in flowing direction
    warp_x = math.cos(flow_angle) * warp_strength * time * 0.1
    warp_y = math.sin(flow_angle) * warp_strength * time * 0.1
    
    # Additional noise-based warping
    x += noise.noise2d(x * 0.02, y * 0.02 + time * 0.05) * warp_strength
    y += noise.noise2d(x * 0.02 + time * 0.05, y * 0.02) * warp_strength
    
    # Sample with warped coordinates
    return noise.noise2d(x + warp_x, y + warp_y)


def domain_warp_color(
    x: float,
    y: float,
    noise: Optional[SimplexNoise] = None,
    warp_strength: float = 0.5
) -> tuple:
    """
    Domain Warping for Color Generation
    
    Generates RGB color values using domain warping.
    Each channel has slightly different warping for color variation.
    
    Args:
        x, y: Input coordinates
        noise: Noise generator (default: SimplexNoise)
        warp_strength: How much to warp coordinates
        
    Returns:
        Tuple of (r, g, b) values in range [0, 1]
        
    Example:
        noise = SimplexNoise(seed=42)
        r, g, b = domain_warp_color(x * scale, y * scale, noise)
    """
    if noise is None:
        noise = SimplexNoise(seed=42)
    
    # Each color channel has slightly different warping
    def warp_channel(x: float, y: float, offset: float) -> float:
        wx = noise.noise2d(x + offset, y) * warp_strength
        wy = noise.noise2d(x, y + offset) * warp_strength
        return noise.noise2d(x + wx, y + wy)
    
    r = warp_channel(x, y, 0.0)
    g = warp_channel(x, y, 5.0)
    b = warp_channel(x, y, 10.0)
    
    # Normalize to [0, 1]
    r = (r + 1) / 2
    g = (g + 1) / 2
    b = (b + 1) / 2
    
    return (r, g, b)


def warp_with_fbm(
    x: float,
    y: float,
    noise: Optional[PerlinNoise] = None,
    warp_strength: float = 0.5,
    fbm_octaves: int = 4,
    fbm_persistence: float = 0.5
) -> float:
    """
    Domain Warping with fBm
    
    Combines domain warping with fractal Brownian motion
    for highly detailed, organic patterns.
    
    Args:
        x, y: Input coordinates
        noise: Noise generator (default: PerlinNoise)
        warp_strength: How much to warp coordinates
        fbm_octaves: Number of fBm octaves
        fbm_persistence: fBm persistence
        
    Returns:
        Warped fBm noise value
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    from .fractal import fractal_brownian_motion
    
    # Get warp amounts from fBm
    warp_x = fractal_brownian_motion(
        x * 0.01, y * 0.01,
        noise=noise,
        octaves=fbm_octaves,
        persistence=fbm_persistence
    ) * warp_strength
    
    warp_y = fractal_brownian_motion(
        x * 0.01 + 100, y * 0.01 + 100,
        noise=noise,
        octaves=fbm_octaves,
        persistence=fbm_persistence
    ) * warp_strength
    
    # Apply warping
    return fractal_brownian_motion(
        x + warp_x, y + warp_y,
        noise=noise,
        octaves=fbm_octaves,
        persistence=fbm_persistence
    )