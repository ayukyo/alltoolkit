# Catmull-Rom Spline Utilities

A comprehensive Catmull-Rom spline utilities module for Python with **zero external dependencies**.

## Overview

Catmull-Rom splines are a type of cubic Hermite spline that pass through all control points, making them ideal for:
- Computer graphics and curve design
- Animation path interpolation
- Font/vector graphics paths
- Game development (smooth movement paths)
- Scientific visualization

## Features

- **Multiple Parameterizations**: Uniform, Chordal, and Centripetal
- **Multi-dimensional Support**: 1D, 2D, 3D, and N-dimensional interpolation
- **Arc Length Computation**: Calculate curve length and sample at specific distances
- **Derivative Analysis**: Tangent, normal, and curvature computation
- **Path Utilities**: Smoothing, animation paths, polygon creation
- **Equidistant Sampling**: Resample curves with uniform spacing
- **Class-based API**: Easy-to-use `CatmullRomSpline2D` and `CatmullRomSpline3D` classes

## Installation

No installation required - just copy the `mod.py` file to your project.

```python
from catmull_rom_utils.mod import (
    interpolate_2d, CatmullRomSpline2D, Parameterization
)
```

## Quick Start

### Basic 2D Interpolation

```python
from catmull_rom_utils.mod import interpolate_2d, Point2D

# Define control points
points = [
    Point2D(0, 0),
    Point2D(2, 4),
    Point2D(5, 2),
    Point2D(8, 5),
    Point2D(10, 0)
]

# Interpolate with 50 points
curve = interpolate_2d(points, num_points=50)
```

### Using the Class API

```python
from catmull_rom_utils.mod import CatmullRomSpline2D, Parameterization

# Create spline
spline = CatmullRomSpline2D(
    control_points=[(0,0), (2,4), (5,2), (8,5), (10,0)],
    parameterization=Parameterization.CENTRIPETAL
)

# Query the spline
point = spline.point_at(0.5)      # Point at parameter t=0.5
tangent = spline.tangent_at(0.5)  # Tangent direction
normal = spline.normal_at(0.5)    # Perpendicular normal
length = spline.arc_length()      # Total curve length

# Sample at specific distance from start
sample = spline.sample_at_distance(15.0)
```

### Animation Paths

```python
from catmull_rom_utils.mod import create_animation_path

keyframes = [(0, 0), (5, 10), (10, 0)]

# Create 60-frame animation with easing
path = create_animation_path(keyframes, num_frames=60, easing='ease-in-out')
```

### 3D Curves

```python
from catmull_rom_utils.mod import interpolate_3d, CatmullRomSpline3D

points_3d = [(0,0,0), (2,4,2), (5,2,4), (10,0,0)]
curve_3d = interpolate_3d(points_3d, num_points=50)

# Or use the class
spline_3d = CatmullRomSpline3D(points_3d)
```

## Parameterization Types

| Type | Description | Best For |
|------|-------------|----------|
| `UNIFORM` | Standard parameterization | Simple curves, mathematical use |
| `CHORDAL` | Chord length based | Natural-looking curves |
| `CENTRIPETAL` | Square root of chord length | Avoiding cusps, general use |

**Recommended**: `CENTRIPETAL` is generally the best choice as it avoids unwanted cusps and self-intersections.

## Core Functions

### Interpolation

```python
interpolate_1d(values, num_points, parameterization, closed)
interpolate_2d(points, num_points, parameterization, closed)
interpolate_3d(points, num_points, parameterization, closed)
interpolate_nd(points, num_points, parameterization, closed)
```

### Arc Length & Sampling

```python
compute_arc_length(points, parameterization, closed, samples_per_segment)
sample_at_distance(points, distance, parameterization, closed, resolution)
resample_curve_equidistant(points, num_points, parameterization, closed)
```

### Derivatives

```python
get_tangent_2d(points, t, parameterization, closed)
get_normal_2d(points, t, parameterization, closed)
curvature_at_point(p0, p1, p2, p3, t, parameterization)
```

### Utilities

```python
smooth_path(points, iterations, parameterization, subdivisions)
create_animation_path(keyframes, num_frames, parameterization, easing)
create_smooth_polygon(vertices, corner_sharpness, num_points)
generate_font_path(points, tension, num_points)
```

## API Reference

### CatmullRomSpline2D

| Method | Description |
|--------|-------------|
| `point_at(t)` | Get point at parameter t (0-1) |
| `tangent_at(t)` | Get normalized tangent vector |
| `normal_at(t)` | Get normalized normal vector |
| `interpolate(num_points)` | Generate full curve |
| `arc_length()` | Compute curve length |
| `sample_at_distance(distance)` | Sample at arc distance |
| `curvature_at(t)` | Compute curvature |
| `smooth(iterations)` | Create smoothed copy |

### CatmullRomSpline3D

| Method | Description |
|--------|-------------|
| `point_at(t)` | Get 3D point at parameter t |
| `tangent_at(t)` | Get 3D tangent vector |
| `interpolate(num_points)` | Generate full 3D curve |

## Examples

See `examples/usage_examples.py` for comprehensive examples including:
- Basic interpolation
- Parameterization comparison
- Animation paths with easing
- Path smoothing
- Polygon smoothing
- Font path generation
- Curvature analysis

## Mathematical Background

The Catmull-Rom spline is defined by four control points P₀, P₁, P₂, P₃. The curve passes through P₁ and P₂, with P₀ and P₃ affecting the shape.

For a parameter t ∈ [0,1]:

```
q(t) = 0.5 × [1  t  t²  t³] × M × [P₀  P₁  P₂  P₃]ᵀ
```

Where M is the basis matrix:
```
M = [ 0  2  0  0]
    [-1  5  2  0]
    [ 2 -5  4 -1]
    [-1  3 -3  1]
```

## Testing

Run the test suite:

```bash
python3 catmull_rom_utils_test.py
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit Contributors