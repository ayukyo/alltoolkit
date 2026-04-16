"""
Fractal Noise Functions

Higher-order noise functions that combine multiple octaves
for more natural, detailed patterns.
"""

import math
from typing import Optional, Callable, Union

from .perlin import PerlinNoise
from .simplex import SimplexNoise
from .value import ValueNoise
from .worley import WorleyNoise


NoiseGenerator = Union[PerlinNoise, SimplexNoise, ValueNoise, WorleyNoise]


def fractal_brownian_motion(
    x: float,
    y: float,
    noise: Optional[NoiseGenerator] = None,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 1.0
) -> float:
    """
    Fractal Brownian Motion (fBm)
    
    Combines multiple octaves of noise at different frequencies
    for more natural, detailed patterns.
    
    Args:
        x, y: Coordinates
        noise: Noise generator instance (default: PerlinNoise)
        octaves: Number of noise layers to combine
        persistence: Amplitude multiplier per octave (0-1)
        lacunarity: Frequency multiplier per octave (>1)
        scale: Base scale factor
        
    Returns:
        Combined noise value, typically in range [-1, 1]
        
    Example:
        noise = SimplexNoise(seed=42)
        terrain = fractal_brownian_motion(x, y, noise, octaves=8)
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    total = 0.0
    amplitude = 1.0
    frequency = scale
    max_value = 0.0
    
    for _ in range(octaves):
        if isinstance(noise, WorleyNoise):
            total += noise.noise2d(x * frequency, y * frequency) * amplitude
        else:
            total += noise.noise2d(x * frequency, y * frequency) * amplitude
        
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    # Normalize to [-1, 1] range
    if max_value > 0:
        total /= max_value
    
    return total


def turbulence(
    x: float,
    y: float,
    noise: Optional[NoiseGenerator] = None,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 1.0
) -> float:
    """
    Turbulence Noise
    
    Similar to fBm but uses absolute values of noise.
    Creates more chaotic, turbulent patterns.
    
    Args:
        x, y: Coordinates
        noise: Noise generator instance
        octaves: Number of noise layers
        persistence: Amplitude decay per octave
        lacunarity: Frequency growth per octave
        scale: Base scale factor
        
    Returns:
        Turbulence value in range [0, 1]
        
    Example:
        noise = PerlinNoise(seed=42)
        clouds = turbulence(x, y, noise, octaves=6)
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    total = 0.0
    amplitude = 1.0
    frequency = scale
    max_value = 0.0
    
    for _ in range(octaves):
        if isinstance(noise, WorleyNoise):
            value = noise.noise2d(x * frequency, y * frequency)
        else:
            value = noise.noise2d(x * frequency, y * frequency)
        
        total += abs(value) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    # Normalize to [0, 1]
    if max_value > 0:
        total /= max_value
    
    return total


def ridged_noise(
    x: float,
    y: float,
    noise: Optional[NoiseGenerator] = None,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 1.0,
    ridge_offset: float = 1.0
) -> float:
    """
    Ridged Multifractal Noise
    
    Creates ridged patterns (inverted valleys) like mountain ridges.
    Good for terrain generation with sharp features.
    
    Args:
        x, y: Coordinates
        noise: Noise generator instance
        octaves: Number of noise layers
        persistence: Amplitude decay per octave
        lacunarity: Frequency growth per octave
        scale: Base scale factor
        ridge_offset: Offset for ridge calculation
        
    Returns:
        Ridged noise value in range [-1, 1]
        
    Example:
        noise = SimplexNoise(seed=42)
        mountains = ridged_noise(x, y, noise, octaves=8)
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    total = 0.0
    amplitude = 1.0
    frequency = scale
    weight = 1.0
    
    for _ in range(octaves):
        if isinstance(noise, WorleyNoise):
            value = noise.noise2d(x * frequency, y * frequency)
        else:
            value = noise.noise2d(x * frequency, y * frequency)
        
        # Create ridges by inverting valleys
        value = ridge_offset - abs(value)
        value *= value * weight  # Square for sharpness
        weight = max(0, min(1, value * 2))  # Spectral weight
        
        total += value * amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    # Normalize roughly to [-1, 1]
    return max(-1, min(1, total / 1.5))


def billow_noise(
    x: float,
    y: float,
    noise: Optional[NoiseGenerator] = None,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 1.0
) -> float:
    """
    Billow Noise
    
    Similar to fBm but uses absolute values, creating billowy cloud-like patterns.
    Output is in [0, 1] range.
    
    Args:
        x, y: Coordinates
        noise: Noise generator instance
        octaves: Number of noise layers
        persistence: Amplitude decay per octave
        lacunarity: Frequency growth per octave
        scale: Base scale factor
        
    Returns:
        Billow noise value in range [0, 1]
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    total = 0.0
    amplitude = 1.0
    frequency = scale
    max_value = 0.0
    
    for _ in range(octaves):
        if isinstance(noise, WorleyNoise):
            value = noise.noise2d(x * frequency, y * frequency)
        else:
            value = noise.noise2d(x * frequency, y * frequency)
        
        # Use absolute value but keep sign pattern
        total += abs(value) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    if max_value > 0:
        total /= max_value
    
    return total


def hybrid_multifractal(
    x: float,
    y: float,
    noise: Optional[NoiseGenerator] = None,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 1.0,
    offset: float = 0.25
) -> float:
    """
    Hybrid Multifractal
    
    Combines properties of fBm and ridged noise.
    Good for heterogeneous terrain.
    
    Args:
        x, y: Coordinates
        noise: Noise generator instance
        octaves: Number of noise layers
        persistence: Amplitude decay per octave
        lacunarity: Frequency growth per octave
        scale: Base scale factor
        offset: Offset value for hybrid calculation
        
    Returns:
        Hybrid multifractal value
    """
    if noise is None:
        noise = PerlinNoise(seed=42)
    
    total = 0.0
    amplitude = 1.0
    frequency = scale
    weight = 0.0
    
    for i in range(octaves):
        if isinstance(noise, WorleyNoise):
            value = noise.noise2d(x * frequency, y * frequency)
        else:
            value = noise.noise2d(x * frequency, y * frequency)
        
        value = (value + offset) * amplitude
        weight = value if i == 0 else min(1, weight * persistence + value)
        total += weight * amplitude
        frequency *= lacunarity
    
    return total