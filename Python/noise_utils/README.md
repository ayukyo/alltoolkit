# Noise Utils

A comprehensive collection of noise generation algorithms for procedural content generation, terrain synthesis, texture generation, and more.

## Features

- **Perlin Noise** - Classic gradient noise algorithm
- **Simplex Noise** - Improved noise with better performance
- **Value Noise** - Simple interpolated random values
- **Worley/Cellular Noise** - Cell-based patterns (Voronoi-like)
- **Fractal Functions** - fBm, Turbulence, Ridged, Billow
- **Domain Warping** - Organic flowing patterns

## Installation

```python
from noise_utils import (
    PerlinNoise, SimplexNoise, ValueNoise, WorleyNoise,
    fractal_brownian_motion, turbulence, ridged_noise,
    domain_warp
)
```

## Quick Start

### Perlin Noise

```python
from noise_utils import PerlinNoise

noise = PerlinNoise(seed=42)

# 2D noise
value = noise.noise2d(1.5, 2.3)  # Returns value in [-1, 1]

# 3D noise
value = noise.noise3d(1.5, 2.3, 0.5)
```

### Simplex Noise

```python
from noise_utils import SimplexNoise

noise = SimplexNoise(seed=42)

# 2D (faster than Perlin for 2D)
value = noise.noise2d(1.5, 2.3)

# 3D
value = noise.noise3d(1.5, 2.3, 0.5)
```

### Value Noise

```python
from noise_utils import ValueNoise

# Different interpolation methods
noise = ValueNoise(seed=42, interpolation='cubic')

value = noise.noise2d(1.5, 2.3)
```

### Worley/Cellular Noise

```python
from noise_utils import WorleyNoise

noise = WorleyNoise(seed=42, num_points=8, distance_metric='euclidean')

# Different modes
f1 = noise.noise2d(1.5, 2.3, mode='F1')      # Distance to nearest
f2 = noise.noise2d(1.5, 2.3, mode='F2')       # Distance to second nearest
diff = noise.noise2d(1.5, 2.3, mode='F2-F1') # Edge detection
```

### Fractal Brownian Motion (fBm)

```python
from noise_utils import PerlinNoise, fractal_brownian_motion

noise = PerlinNoise(seed=42)

# Combine multiple octaves for natural detail
value = fractal_brownian_motion(
    x, y,
    noise=noise,
    octaves=6,        # More octaves = more detail
    persistence=0.5,  # Lower = smoother
    lacunarity=2.0,   # Frequency multiplier
    scale=0.02        # Scale factor
)
```

### Turbulence

```python
from noise_utils import turbulence

# Creates turbulent patterns (uses absolute values)
value = turbulence(x, y, noise=noise, octaves=6)
```

### Ridged Noise

```python
from noise_utils import ridged_noise

# Mountain-like ridges
value = ridged_noise(x, y, noise=noise, octaves=8)
```

### Domain Warping

```python
from noise_utils import PerlinNoise, domain_warp

noise = PerlinNoise(seed=42)

# Creates organic, flowing patterns
value = domain_warp(x, y, noise=noise, warp_strength=0.5, iterations=2)

# Animated flow (for clouds, water)
from noise_utils import domain_warp_flow
value = domain_warp_flow(x, y, time, noise=noise)

# Color generation
from noise_utils import domain_warp_color
r, g, b = domain_warp_color(x, y, noise=noise)
```

## Use Cases

### Terrain Generation

```python
from noise_utils import SimplexNoise, fractal_brownian_motion, ridged_noise

noise = SimplexNoise(seed=42)

def generate_terrain(width, height, scale=0.01):
    terrain = []
    for y in range(height):
        row = []
        for x in range(width):
            # Base terrain
            base = fractal_brownian_motion(
                x * scale, y * scale, noise=noise, octaves=6
            )
            # Add ridges for mountains
            mountains = ridged_noise(
                x * scale, y * scale, noise=noise, octaves=4
            )
            height_val = base * 0.6 + mountains * 0.4
            row.append(height_val)
        terrain.append(row)
    return terrain
```

### Cloud Generation

```python
from noise_utils import SimplexNoise, turbulence

noise = SimplexNoise(seed=42)

def generate_clouds(width, height, scale=0.02):
    clouds = []
    for y in range(height):
        row = []
        for x in range(width):
            density = turbulence(
                x * scale, y * scale, 
                noise=noise, octaves=6
            )
            row.append(density)
        clouds.append(row)
    return clouds
```

### Voronoi Diagrams

```python
from noise_utils import WorleyNoise

noise = WorleyNoise(seed=42, num_points=10)

def generate_voronoi(width, height, scale=0.05):
    diagram = []
    for y in range(height):
        row = []
        for x in range(width):
            # Use F2-F1 for cell edges
            edge = noise.noise2d(x * scale, y * scale, mode='F2-F1')
            row.append(edge)
        diagram.append(row)
    return diagram
```

## API Reference

### PerlinNoise

| Method | Description |
|--------|-------------|
| `noise2d(x, y)` | 2D Perlin noise, returns [-1, 1] |
| `noise3d(x, y, z)` | 3D Perlin noise, returns [-1, 1] |

### SimplexNoise

| Method | Description |
|--------|-------------|
| `noise2d(x, y)` | 2D Simplex noise, returns [-1, 1] |
| `noise3d(x, y, z)` | 3D Simplex noise, returns [-1, 1] |

### ValueNoise

| Method | Description |
|--------|-------------|
| `noise1d(x)` | 1D value noise |
| `noise2d(x, y)` | 2D value noise |

| Parameter | Values |
|-----------|--------|
| `interpolation` | 'linear', 'cosine', 'smoothstep', 'smootherstep', 'cubic' |

### WorleyNoise

| Method | Description |
|--------|-------------|
| `noise2d(x, y, mode)` | 2D Worley noise |
| `get_distances(x, y)` | Get sorted list of distances |

| Parameter | Values |
|-----------|--------|
| `mode` | 'F1', 'F2', 'F2-F1', 'F1*F2' |
| `distance_metric` | 'euclidean', 'manhattan', 'chebyshev' |

### Fractal Functions

All take: `x, y, noise, octaves, persistence, lacunarity, scale`

| Function | Description |
|----------|-------------|
| `fractal_brownian_motion` | Layered noise for natural detail |
| `turbulence` | Absolute value layering |
| `ridged_noise` | Mountain-like ridges |
| `billow_noise` | Billowy cloud patterns |
| `hybrid_multifractal` | Mixed terrain generation |

## Zero Dependencies

Pure Python implementation - no external packages required!

## License

MIT