# Noise Utilities

Noise generation utilities for Rust. Zero external dependencies, using only the standard library.

## Features

- **Perlin Noise**: Classic gradient noise algorithm (1D, 2D, 3D)
- **Simplex Noise**: Improved gradient noise with fewer artifacts (2D, 3D)
- **Value Noise**: Simple interpolated random values (1D, 2D)
- **White Noise**: Random noise with uniform frequency distribution
- **Pink Noise**: 1/f noise, natural-sounding random variations
- **Brown Noise**: Red noise, random walk integration
- **Fractal Brownian Motion (FBM)**: Layered noise for terrain generation
- **Ridged Multifractal**: Sharp ridge-like terrain features
- **Turbulence**: Absolute-value layered noise
- **Voronoi/Worley Noise**: Cell-based patterns for organic textures
- **Noise Map Generation**: 2D heightmap generation

## Installation

```rust
// Copy the mod.rs file to your project
mod noise_utils;
```

## Quick Start

```rust
use noise_utils::*;

// Perlin Noise
let value = perlin_noise_2d(0.5, 0.5, None);
assert!(value >= -1.0 && value <= 1.0);

// Simplex Noise
let value = simplex_noise_2d(0.5, 0.5, None);

// White Noise
let samples = white_noise(100, Some(42));

// Pink Noise
let samples = pink_noise(256, Some(42));

// Generate terrain heightmap
let heightmap = noise_map_2d(64, 64, 0.1, 4, Some(42));
```

## API Reference

### Perlin Noise

```rust
// 1D Perlin Noise - returns value in [-1, 1]
fn perlin_noise_1d(x: f64, seed: Option<u32>) -> f64

// 2D Perlin Noise - returns value in [-1, 1]
fn perlin_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64

// 3D Perlin Noise - returns value in [-1, 1]
fn perlin_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64
```

Perlin noise produces smooth, natural-looking random values. Useful for:
- Terrain generation
- Texture creation
- Procedural animation
- Cloud/smoke effects

### Simplex Noise

```rust
// 2D Simplex Noise - returns value in [-1, 1]
fn simplex_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64

// 3D Simplex Noise - returns value in [-1, 1]
fn simplex_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64
```

Simplex noise is an improvement over Perlin noise with:
- Better visual quality
- Fewer directional artifacts
- Better performance in higher dimensions
- More uniform gradient distribution

### Value Noise

```rust
// 1D Value Noise - returns value in [0, 1]
fn value_noise_1d(x: f64, seed: Option<u32>) -> f64

// 2D Value Noise - returns value in [0, 1]
fn value_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64
```

Value noise interpolates random values at grid points. Simpler than Perlin noise
with a different visual character. Good for:
- Simple terrain generation
- Background textures
- Quick prototyping

### White Noise

```rust
// White Noise - returns Vec<f64> in [-1, 1]
fn white_noise(count: usize, seed: Option<u64>) -> Vec<f64>

// White Noise [0,1] - returns Vec<f64> in [0, 1]
fn white_noise_01(count: usize, seed: Option<u64>) -> Vec<f64>
```

White noise has equal intensity at all frequencies. Completely random signal.
Useful for:
- Random number generation
- Audio synthesis
- Testing/simulation
- Monte Carlo methods

### Pink Noise (1/f Noise)

```rust
// Pink Noise - returns Vec<f64> in [-1, 1]
fn pink_noise(count: usize, seed: Option<u64>) -> Vec<f64>
```

Pink noise has equal power per octave, falling off at ~3dB per octave.
Common in natural phenomena. Useful for:
- Audio synthesis (sounds more natural than white noise)
- Music generation
- Natural-looking randomness

### Brown Noise (Red Noise)

```rust
// Brown Noise - returns Vec<f64> in [-1, 1]
fn brown_noise(count: usize, seed: Option<u64>) -> Vec<f64>
```

Brown noise has power spectral density proportional to 1/f². Created by
integrating white noise. Useful for:
- Low rumble effects
- Smooth random variations
- Terrain erosion simulation

### Fractal Brownian Motion (FBM)

```rust
// 2D FBM - combines multiple noise octaves
fn fbm_2d(
    x: f64,
    y: f64,
    octaves: usize,      // Number of layers (4-8 typical)
    persistence: f64,    // Amplitude decay (0.5 typical)
    lacunarity: f64,     // Frequency growth (2.0 typical)
    seed: Option<u32>
) -> f64
```

FBM combines multiple octaves of noise at different frequencies and amplitudes.
Creates complex, natural-looking patterns. Useful for:
- Terrain generation
- Cloud textures
- Natural phenomena
- Landscape features

### Ridged Multifractal

```rust
fn ridged_multifractal_2d(
    x: f64,
    y: f64,
    octaves: usize,
    persistence: f64,
    lacunarity: f64,
    seed: Option<u32>
) -> f64
```

Creates sharp ridge-like features. Useful for:
- Mountain ranges
- Canyon systems
- Ridge-based terrain

### Turbulence

```rust
fn turbulence_2d(x: f64, y: f64, octaves: usize, seed: Option<u32>) -> f64
```

Absolute-value layered noise creates chaotic patterns. Useful for:
- Fire/smoke effects
- Turbulent textures
- Marble-like patterns

### Voronoi/Worley Noise

```rust
// Voronoi Noise - distance to nearest feature point
fn voronoi_2d(x: f64, y: f64, seed: Option<u32>) -> f64

// Voronoi F2 - (distance to closest, distance to second closest)
fn voronoi_2d_f2(x: f64, y: f64, seed: Option<u32>) -> (f64, f64)
```

Creates cell-like patterns based on distance to random points. Useful for:
- Organic textures
- Cell division patterns
- Crystal structures
- Cave/tunnel networks

### Utility Functions

```rust
// Scale [-1, 1] to [0, 1]
fn normalize_noise(value: f64) -> f64

// Scale [0, 1] to [-1, 1]
fn denormalize_noise(value: f64) -> f64

// Generate 2D noise map (heightmap)
fn noise_map_2d(
    width: usize,
    height: usize,
    scale: f64,
    octaves: usize,
    seed: Option<u32>
) -> Vec<Vec<f64>>
```

## Examples

### Terrain Generation

```rust
use noise_utils::*;

// Generate heightmap for terrain
let heightmap = noise_map_2d(256, 256, 0.02, 6, Some(42));

// Or use FBM directly for more control
let height = fbm_2d(x * 0.02, y * 0.02, 6, 0.5, 2.0, Some(42));
let normalized_height = normalize_noise(height);
```

### Cave Generation

```rust
// Use Voronoi for cave network
for x in 0..width {
    for y in 0..height {
        let (d1, d2) = voronoi_2d_f2(x as f64 * 0.1, y as f64 * 0.1, Some(42));
        let edge = d2 - d1; // Distance between cells
        
        if edge < 0.1 {
            // This is a cell boundary - potential tunnel
        }
    }
}
```

### Procedural Texture

```rust
// Combine multiple noise types for rich texture
for x in 0..texture_width {
    for y in 0..texture_height {
        let nx = x as f64 / texture_width as f64;
        let ny = y as f64 / texture_height as f64;
        
        // Base layer
        let base = fbm_2d(nx * 4.0, ny * 4.0, 4, 0.5, 2.0, Some(42));
        
        // Detail layer
        let detail = perlin_noise_2d(nx * 20.0, ny * 20.0, Some(43));
        
        // Combine
        let value = normalize_noise(base * 0.8 + detail * 0.2);
    }
}
```

### Animation

```rust
// 3D noise for time-varying effects
let time = animation_time;
let value = perlin_noise_3d(x, y, time, Some(42));
```

## Performance

All functions are optimized for performance:
- Single-pass algorithms where possible
- Pre-allocated buffers
- Inline helper functions
- Minimal memory allocation

## Testing

Run the test suite:

```bash
cd Rust/noise_utils
rustc --test noise_utils_test.rs -o noise_test && ./noise_test
```

Or with Cargo (if using as a module):

```bash
cargo test
```

## Algorithm Details

### Perlin Noise

Uses Ken Perlin's improved algorithm with:
- 256-byte permutation table
- Gradient interpolation
- Smooth fade function: `t³(t(6t-15)+10)`
- 8 gradient directions in 2D

### Simplex Noise

Uses Stefan Gustavson's implementation with:
- Simplex grid structure
- Skewing/unskewing transformation
- 12 gradient directions
- Better performance in higher dimensions

### Pink Noise

Uses the Voss-McCartney algorithm:
- 7 octave bands
- Updated at different rates
- Produces natural 1/f spectrum

## License

MIT License - Part of AllToolkit project

## References

- Ken Perlin, "An Image Synthesizer", SIGGRAPH 1985
- Ken Perlin, "Improving Noise", SIGGRAPH 2002
- Stefan Gustavson, "Simplex Noise Demystified"
- Voss & McCartney, "1/f Noise"