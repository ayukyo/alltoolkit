//! # Noise Utilities

// ============================================================================
// Permutation Table for Perlin/Simplex Noise
// ============================================================================

/// Standard permutation table used in Perlin noise.
/// Contains values 0-255 in a pseudo-random order.
const PERM: [u8; 256] = [
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
    222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180,
];

/// Extended permutation table for seamless tiling.
/// Concatenation of PERM with itself.
fn get_perm() -> Vec<u8> {
    let mut perm = PERM.to_vec();
    perm.extend_from_slice(&PERM);
    perm
}

/// Linear interpolation between two values.
///
/// # Parameters
/// - `a`: First value
/// - `b`: Second value
/// - `t`: Interpolation factor (0.0 to 1.0)
///
/// # Returns
/// Interpolated value
#[inline]
fn lerp(a: f64, b: f64, t: f64) -> f64 {
    a + t * (b - a)
}

/// Improved smoothstep (Ken Perlin's version).
///
/// # Parameters
/// - `t`: Input value (0.0 to 1.0)
///
/// # Returns
/// Smoothly interpolated value
#[inline]
fn fade(t: f64) -> f64 {
    t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
}

/// Calculate gradient for Perlin noise.
///
/// # Parameters
/// - `hash`: Hash value (0-255)
/// - `x`: X coordinate
/// - `y`: Y coordinate
///
/// # Returns
/// Gradient value
#[inline]
fn grad_2d(hash: u8, x: f64, y: f64) -> f64 {
    let h = hash & 7; // Use lower 3 bits
    let u = if h < 4 { x } else { y };
    let v = if h < 4 { y } else { x };
    (if (h & 1) == 0 { u } else { -u }) + (if (h & 2) == 0 { v } else { -v })
}

/// Calculate gradient for 3D Perlin noise.
///
/// # Parameters
/// - `hash`: Hash value (0-255)
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `z`: Z coordinate
///
/// # Returns
/// Gradient value
#[inline]
fn grad_3d(hash: u8, x: f64, y: f64, z: f64) -> f64 {
    let h = hash & 15;
    let u = if h < 8 { x } else { y };
    let v = if h < 4 { y } else if h == 12 || h == 14 { x } else { z };
    (if (h & 1) == 0 { u } else { -u }) + (if (h & 2) == 0 { v } else { -v })
}

// ============================================================================
// Perlin Noise
// ============================================================================

/// Generate 1D Perlin noise.
///
/// Perlin noise produces smooth, natural-looking random values.
/// The same seed always produces the same sequence of values.
///
/// # Parameters
/// - `x`: X coordinate (can be fractional)
/// - `seed`: Optional seed for reproducible results (default: 0)
///
/// # Returns
/// Noise value in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::perlin_noise_1d(0.5, None);
/// assert!(value >= -1.0 && value <= 1.0);
///
/// let same1 = noise_utils::perlin_noise_1d(1.0, Some(42));
/// let same2 = noise_utils::perlin_noise_1d(1.0, Some(42));
/// assert!((same1 - same2).abs() < 1e-10);
/// ```
pub fn perlin_noise_1d(x: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    let xi = x.floor() as i64;
    let xf = x - x.floor();
    
    let u = fade(xf);
    
    let p0 = perm[((xi & 255) as usize + seed) & 255] as usize;
    let p1 = perm[((xi.wrapping_add(1) & 255) as usize + seed) & 255] as usize;
    
    let n0 = grad_2d(PERM[p0], xf, 0.0);
    let n1 = grad_2d(PERM[p1], xf - 1.0, 0.0);
    
    lerp(n0, n1, u)
}

/// Generate 2D Perlin noise.
///
/// Perlin noise produces smooth, natural-looking random values.
/// The same seed always produces the same sequence of values.
///
/// # Parameters
/// - `x`: X coordinate (can be fractional)
/// - `y`: Y coordinate (can be fractional)
/// - `seed`: Optional seed for reproducible results (default: 0)
///
/// # Returns
/// Noise value in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::perlin_noise_2d(0.5, 0.5, None);
/// assert!(value >= -1.0 && value <= 1.0);
///
/// let terrain = noise_utils::perlin_noise_2d(100.0, 200.0, Some(42));
/// ```
pub fn perlin_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let u = fade(xf);
    let v = fade(yf);
    
    let aa = perm[((xi & 255) as usize + seed) & 255] as usize;
    let ab = perm[((yi & 255) as usize + seed) & 255] as usize;
    
    let p0 = PERM[(aa & 255) as usize] as usize;
    let p1 = PERM[((aa + 1) & 255) as usize] as usize;
    let p2 = PERM[(ab & 255) as usize] as usize;
    let p3 = PERM[((ab + 1) & 255) as usize] as usize;
    
    let grad_aa = grad_2d(PERM[p0], xf, yf);
    let grad_ba = grad_2d(PERM[p1], xf - 1.0, yf);
    let grad_ab = grad_2d(PERM[p2], xf, yf - 1.0);
    let grad_bb = grad_2d(PERM[p3], xf - 1.0, yf - 1.0);
    
    let x1 = lerp(grad_aa, grad_ba, u);
    let x2 = lerp(grad_ab, grad_bb, u);
    
    lerp(x1, x2, v)
}

/// Generate 3D Perlin noise.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `z`: Z coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::perlin_noise_3d(0.5, 0.5, 0.5, None);
/// assert!(value >= -1.0 && value <= 1.0);
/// ```
pub fn perlin_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    let zi = z.floor() as i64;
    
    let xf = x - x.floor();
    let yf = y - y.floor();
    let zf = z - z.floor();
    
    let u = fade(xf);
    let v = fade(yf);
    let w = fade(zf);
    
    let a = perm[((xi & 255) as usize + seed) & 255] as usize;
    let aa = perm[(a + (yi & 255) as usize) & 255] as usize;
    let ab = perm[(a + ((yi + 1) & 255) as usize) & 255] as usize;
    let b = perm[((xi + 1) as usize & 255) as usize] as usize;
    let ba = perm[(b + (yi & 255) as usize) & 255] as usize;
    let bb = perm[(b + ((yi + 1) & 255) as usize) & 255] as usize;
    
    let p000 = PERM[(aa + (zi & 255) as usize) & 255];
    let p001 = PERM[(aa + ((zi + 1) & 255) as usize) & 255];
    let p010 = PERM[(ab + (zi & 255) as usize) & 255];
    let p011 = PERM[(ab + ((zi + 1) & 255) as usize) & 255];
    let p100 = PERM[(ba + (zi & 255) as usize) & 255];
    let p101 = PERM[(ba + ((zi + 1) & 255) as usize) & 255];
    let p110 = PERM[(bb + (zi & 255) as usize) & 255];
    let p111 = PERM[(bb + ((zi + 1) & 255) as usize) & 255];
    
    let n000 = grad_3d(p000, xf, yf, zf);
    let n001 = grad_3d(p001, xf, yf, zf - 1.0);
    let n010 = grad_3d(p010, xf, yf - 1.0, zf);
    let n011 = grad_3d(p011, xf, yf - 1.0, zf - 1.0);
    let n100 = grad_3d(p100, xf - 1.0, yf, zf);
    let n101 = grad_3d(p101, xf - 1.0, yf, zf - 1.0);
    let n110 = grad_3d(p110, xf - 1.0, yf - 1.0, zf);
    let n111 = grad_3d(p111, xf - 1.0, yf - 1.0, zf - 1.0);
    
    let x1 = lerp(n000, n100, u);
    let x2 = lerp(n010, n110, u);
    let y1 = lerp(x1, x2, v);
    
    let x3 = lerp(n001, n101, u);
    let x4 = lerp(n011, n111, u);
    let y2 = lerp(x3, x4, v);
    
    lerp(y1, y2, w)
}

// ============================================================================
// Simplex Noise
// ============================================================================

/// Skewing factors for 2D simplex noise.
const F2: f64 = 0.3660254037844386; // (sqrt(3) - 1) / 2
const G2: f64 = 0.21132486540518713; // (3 - sqrt(3)) / 6

/// Skewing factors for 3D simplex noise.
const F3: f64 = 0.3333333333333333; // 1/3
const G3: f64 = 0.16666666666666666; // 1/6

/// Generate 2D Simplex noise.
///
/// Simplex noise is an improvement over Perlin noise with:
/// - Better visual quality
/// - Fewer directional artifacts
/// - Better performance in higher dimensions
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::simplex_noise_2d(0.5, 0.5, None);
/// assert!(value >= -1.0 && value <= 1.0);
/// ```
pub fn simplex_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    // Skew input coordinates
    let s = (x + y) * F2;
    let i = (x + s).floor() as i64;
    let j = (y + s).floor() as i64;
    
    // Unskew back to (x,y) space
    let t = (i + j) as f64 * G2;
    let x0 = x - (i as f64 - t);
    let y0 = y - (j as f64 - t);
    
    // Determine simplex
    let (i1, j1) = if x0 > y0 { (1, 0) } else { (0, 1) };
    
    // Offsets for middle and last corners
    let x1 = x0 - i1 as f64 + G2;
    let y1 = y0 - j1 as f64 + G2;
    let x2 = x0 - 1.0 + 2.0 * G2;
    let y2 = y0 - 1.0 + 2.0 * G2;
    
    // Hash coordinates
    let ii = ((i & 255) as usize + seed) & 255;
    let jj = (j & 255) as usize;
    
    // Calculate contributions from three corners
    let mut n0 = 0.0;
    let mut n1 = 0.0;
    let mut n2 = 0.0;
    
    let t0 = 0.5 - x0 * x0 - y0 * y0;
    if t0 >= 0.0 {
        let gi0 = perm[(perm[ii] as usize + jj) & 255] as usize % 12;
        n0 = t0 * t0 * t0 * t0 * grad_simplex_2d(gi0, x0, y0);
    }
    
    let t1 = 0.5 - x1 * x1 - y1 * y1;
    if t1 >= 0.0 {
        let ii1 = ((i + i1) & 255) as usize;
        let jj1 = ((j + j1) & 255) as usize;
        let gi1 = perm[(perm[ii1] as usize + jj1) & 255] as usize % 12;
        n1 = t1 * t1 * t1 * t1 * grad_simplex_2d(gi1, x1, y1);
    }
    
    let t2 = 0.5 - x2 * x2 - y2 * y2;
    if t2 >= 0.0 {
        let ii2 = ((i + 1) & 255) as usize;
        let jj2 = ((j + 1) & 255) as usize;
        let gi2 = perm[(perm[ii2] as usize + jj2) & 255] as usize % 12;
        n2 = t2 * t2 * t2 * t2 * grad_simplex_2d(gi2, x2, y2);
    }
    
    // Scale to [-1, 1]
    70.0 * (n0 + n1 + n2)
}

/// Gradient function for 2D simplex noise.
#[inline]
fn grad_simplex_2d(gi: usize, x: f64, y: f64) -> f64 {
    let grad = [
        (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0),
        (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
        (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0),
    ];
    let (gx, gy) = grad[gi % 12];
    gx * x + gy * y
}

/// Generate 3D Simplex noise.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `z`: Z coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::simplex_noise_3d(0.5, 0.5, 0.5, None);
/// assert!(value >= -1.0 && value <= 1.0);
/// ```
pub fn simplex_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    // Skew input coordinates
    let s = (x + y + z) * F3;
    let i = (x + s).floor() as i64;
    let j = (y + s).floor() as i64;
    let k = (z + s).floor() as i64;
    
    // Unskew back to (x,y,z) space
    let t = (i + j + k) as f64 * G3;
    let x0 = x - (i as f64 - t);
    let y0 = y - (j as f64 - t);
    let z0 = z - (k as f64 - t);
    
    // Determine simplex
    let (i1, j1, k1, i2, j2, k2) = if x0 >= y0 {
        if y0 >= z0 {
            (1, 0, 0, 1, 1, 0)
        } else if x0 >= z0 {
            (1, 0, 0, 1, 0, 1)
        } else {
            (0, 0, 1, 1, 0, 1)
        }
    } else {
        if y0 < z0 {
            (0, 0, 1, 0, 1, 1)
        } else if x0 < z0 {
            (0, 1, 0, 0, 1, 1)
        } else {
            (0, 1, 0, 1, 1, 0)
        }
    };
    
    // Offsets for corners
    let x1 = x0 - i1 as f64 + G3;
    let y1 = y0 - j1 as f64 + G3;
    let z1 = z0 - k1 as f64 + G3;
    let x2 = x0 - i2 as f64 + 2.0 * G3;
    let y2 = y0 - j2 as f64 + 2.0 * G3;
    let z2 = z0 - k2 as f64 + 2.0 * G3;
    let x3 = x0 - 1.0 + 3.0 * G3;
    let y3 = y0 - 1.0 + 3.0 * G3;
    let z3 = z0 - 1.0 + 3.0 * G3;
    
    // Hash coordinates
    let ii = ((i & 255) as usize + seed) & 255;
    let jj = (j & 255) as usize;
    let kk = (k & 255) as usize;
    
    // Calculate contributions from four corners
    let mut n = 0.0;
    
    let t0 = 0.6 - x0 * x0 - y0 * y0 - z0 * z0;
    if t0 >= 0.0 {
        let gi0 = perm[(perm[(perm[ii] as usize + jj) & 255] as usize + kk) & 255] as usize % 12;
        n += t0 * t0 * t0 * t0 * grad_simplex_3d(gi0, x0, y0, z0);
    }
    
    let t1 = 0.6 - x1 * x1 - y1 * y1 - z1 * z1;
    if t1 >= 0.0 {
        let ii1 = ((i + i1) & 255) as usize;
        let jj1 = ((j + j1) & 255) as usize;
        let kk1 = ((k + k1) & 255) as usize;
        let gi1 = perm[(perm[(perm[ii1] as usize + jj1) & 255] as usize + kk1) & 255] as usize % 12;
        n += t1 * t1 * t1 * t1 * grad_simplex_3d(gi1, x1, y1, z1);
    }
    
    let t2 = 0.6 - x2 * x2 - y2 * y2 - z2 * z2;
    if t2 >= 0.0 {
        let ii2 = ((i + i2) & 255) as usize;
        let jj2 = ((j + j2) & 255) as usize;
        let kk2 = ((k + k2) & 255) as usize;
        let gi2 = perm[(perm[(perm[ii2] as usize + jj2) & 255] as usize + kk2) & 255] as usize % 12;
        n += t2 * t2 * t2 * t2 * grad_simplex_3d(gi2, x2, y2, z2);
    }
    
    let t3 = 0.6 - x3 * x3 - y3 * y3 - z3 * z3;
    if t3 >= 0.0 {
        let ii3 = ((i + 1) & 255) as usize;
        let jj3 = ((j + 1) & 255) as usize;
        let kk3 = ((k + 1) & 255) as usize;
        let gi3 = perm[(perm[(perm[ii3] as usize + jj3) & 255] as usize + kk3) & 255] as usize % 12;
        n += t3 * t3 * t3 * t3 * grad_simplex_3d(gi3, x3, y3, z3);
    }
    
    32.0 * n
}

/// Gradient function for 3D simplex noise.
#[inline]
fn grad_simplex_3d(gi: usize, x: f64, y: f64, z: f64) -> f64 {
    let grad = [
        (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0),
        (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0),
        (0.0, 1.0, 1.0), (0.0, -1.0, 1.0), (0.0, 1.0, -1.0), (0.0, -1.0, -1.0),
    ];
    let (gx, gy, gz) = grad[gi % 12];
    gx * x + gy * y + gz * z
}

// ============================================================================
// Value Noise
// ============================================================================

/// Simple hash function for value noise.
fn hash(x: i64, y: i64, seed: usize) -> usize {
    let mut h = (x as usize).wrapping_mul(374761393);
    h = h.wrapping_add((y as usize).wrapping_mul(668265263));
    h = h.wrapping_add(seed);
    h = (h ^ (h >> 13)).wrapping_mul(1274126177);
    h
}

/// Generate 2D Value noise.
///
/// Value noise is simpler than Perlin noise and produces a different
/// visual character. Good for terrain generation and textures.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [0.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::value_noise_2d(0.5, 0.5, None);
/// assert!(value >= 0.0 && value <= 1.0);
/// ```
pub fn value_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0) as usize;
    
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let u = fade(xf);
    let v = fade(yf);
    
    // Get random values at four corners
    let v00 = (hash(xi, yi, seed) % 10000) as f64 / 9999.0;
    let v10 = (hash(xi + 1, yi, seed) % 10000) as f64 / 9999.0;
    let v01 = (hash(xi, yi + 1, seed) % 10000) as f64 / 9999.0;
    let v11 = (hash(xi + 1, yi + 1, seed) % 10000) as f64 / 9999.0;
    
    // Bilinear interpolation
    let x1 = lerp(v00, v10, u);
    let x2 = lerp(v01, v11, u);
    
    lerp(x1, x2, v)
}

/// Generate 1D Value noise.
///
/// # Parameters
/// - `x`: X coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [0.0, 1.0]
pub fn value_noise_1d(x: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0) as usize;
    
    let xi = x.floor() as i64;
    let xf = x - x.floor();
    
    let u = fade(xf);
    
    let v0 = (hash(xi, 0, seed) % 10000) as f64 / 9999.0;
    let v1 = (hash(xi + 1, 0, seed) % 10000) as f64 / 9999.0;
    
    lerp(v0, v1, u)
}

// ============================================================================
// White Noise
// ============================================================================

/// Simple Linear Congruential Generator for random numbers.
struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self {
        Lcg { state: seed }
    }
    
    fn next(&mut self) -> u64 {
        // Parameters from Numerical Recipes
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.state
    }
    
    fn next_f64(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

/// Generate white noise samples.
///
/// White noise has equal intensity at all frequencies, producing
/// a completely random signal.
///
/// # Parameters
/// - `count`: Number of samples to generate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Vector of noise values in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let samples = noise_utils::white_noise(100, Some(42));
/// assert_eq!(samples.len(), 100);
/// for s in &samples {
///     assert!(*s >= -1.0 && *s <= 1.0);
/// }
/// ```
pub fn white_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    (0..count).map(|_| rng.next_f64() * 2.0 - 1.0).collect()
}

/// Generate white noise samples in range [0.0, 1.0].
///
/// # Parameters
/// - `count`: Number of samples to generate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Vector of noise values in range [0.0, 1.0]
pub fn white_noise_01(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    (0..count).map(|_| rng.next_f64()).collect()
}

// ============================================================================
// Pink Noise (1/f Noise)
// ============================================================================

/// Generate pink noise (1/f noise).
///
/// Pink noise has equal power per octave, resulting in a signal that
/// falls off at 10dB per decade. Common in natural phenomena and
/// often used for audio synthesis.
///
/// Uses the Voss-McCartney algorithm.
///
/// # Parameters
/// - `count`: Number of samples to generate (should be power of 2 for best results)
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Vector of noise values in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let samples = noise_utils::pink_noise(256, Some(42));
/// assert_eq!(samples.len(), 256);
/// ```
pub fn pink_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    
    // Voss-McCartney algorithm
    let mut result = Vec::with_capacity(count);
    let mut b = [0.0; 7];
    
    for i in 0..count {
        let mut sum = 0.0;
        
        // Update random counters based on index
        for j in 0..7 {
            if (i & (1 << j)) == 0 {
                b[j] = rng.next_f64() * 2.0 - 1.0;
            }
            sum += b[j];
        }
        
        // Add white noise
        sum += rng.next_f64() * 2.0 - 1.0;
        
        // Normalize (8 sources)
        result.push(sum / 8.0);
    }
    
    // Normalize to [-1, 1]
    let max = result.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let min = result.iter().cloned().fold(f64::INFINITY, f64::min);
    let range = max - min;
    
    if range > 0.0 {
        for val in &mut result {
            *val = (*val - min) / range * 2.0 - 1.0;
        }
    }
    
    result
}

// ============================================================================
// Brown Noise (Red Noise)
// ============================================================================

/// Generate brown noise (red noise, random walk).
///
/// Brown noise has a power spectral density proportional to 1/f².
/// It sounds like a low rumble and is created by integrating white noise.
///
/// # Parameters
/// - `count`: Number of samples to generate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Vector of noise values in range [-1.0, 1.0]
///
/// # Examples
/// ```
/// let samples = noise_utils::brown_noise(256, Some(42));
/// assert_eq!(samples.len(), 256);
/// ```
pub fn brown_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    let mut result = Vec::with_capacity(count);
    let mut sum = 0.0;
    
    for _ in 0..count {
        // Add white noise
        sum += rng.next_f64() * 2.0 - 1.0;
        
        // Soft clip to prevent runaway
        sum = sum.clamp(-1.0, 1.0);
        result.push(sum);
    }
    
    // Normalize to [-1, 1]
    let max = result.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let min = result.iter().cloned().fold(f64::INFINITY, f64::min);
    let range = max - min;
    
    if range > 0.0 {
        for val in &mut result {
            *val = (*val - min) / range * 2.0 - 1.0;
        }
    }
    
    result
}

// ============================================================================
// Fractal Brownian Motion (FBM)
// ============================================================================

/// Generate 2D Fractal Brownian Motion noise.
///
/// FBM combines multiple octaves of noise at different frequencies
/// and amplitudes to create complex, natural-looking patterns.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `octaves`: Number of noise layers (typically 4-8)
/// - `persistence`: How much each octave contributes (typically 0.5)
/// - `lacunarity`: Frequency multiplier per octave (typically 2.0)
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range roughly [-1.0, 1.0]
///
/// # Examples
/// ```
/// let value = noise_utils::fbm_2d(0.5, 0.5, 4, 0.5, 2.0, None);
/// // Value typically in range [-1, 1]
/// ```
pub fn fbm_2d(
    x: f64,
    y: f64,
    octaves: usize,
    persistence: f64,
    lacunarity: f64,
    seed: Option<u32>,
) -> f64 {
    let mut total = 0.0;
    let mut frequency = 1.0;
    let mut amplitude = 1.0;
    let mut max_value = 0.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        total += perlin_noise_2d(x * frequency, y * frequency, Some(seed + i as u32)) * amplitude;
        max_value += amplitude;
        amplitude *= persistence;
        frequency *= lacunarity;
    }
    
    total / max_value
}

/// Generate 2D ridged multifractal noise.
///
/// A variation of FBM that creates ridge-like features,
/// useful for terrain with sharp ridges.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `octaves`: Number of noise layers
/// - `persistence`: How much each octave contributes
/// - `lacunarity`: Frequency multiplier per octave
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range roughly [-1.0, 1.0]
pub fn ridged_multifractal_2d(
    x: f64,
    y: f64,
    octaves: usize,
    persistence: f64,
    lacunarity: f64,
    seed: Option<u32>,
) -> f64 {
    let mut total = 0.0;
    let mut frequency = 1.0;
    let mut amplitude = 1.0;
    let mut weight = 1.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        let signal = perlin_noise_2d(x * frequency, y * frequency, Some(seed + i as u32));
        
        // Make ridges
        let signal = 1.0 - signal.abs();
        let signal = signal * signal;
        
        // Weight by previous signal
        let signal = signal * weight;
        weight = (signal * 2.0).clamp(0.0, 1.0);
        
        total += signal * amplitude;
        amplitude *= persistence;
        frequency *= lacunarity;
    }
    
    total
}

// ============================================================================
// Turbulence
// ============================================================================

/// Generate 2D turbulence noise.
///
/// Turbulence creates more chaotic patterns by using the absolute
/// value of noise at each octave.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `octaves`: Number of noise layers
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Noise value in range [0.0, ~2.0]
pub fn turbulence_2d(x: f64, y: f64, octaves: usize, seed: Option<u32>) -> f64 {
    let mut total = 0.0;
    let mut frequency = 1.0;
    let mut amplitude = 1.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        total += perlin_noise_2d(x * frequency, y * frequency, Some(seed + i as u32)).abs() * amplitude;
        amplitude *= 0.5;
        frequency *= 2.0;
    }
    
    total
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Scale noise value from [-1, 1] to [0, 1].
///
/// # Parameters
/// - `value`: Noise value in range [-1, 1]
///
/// # Returns
/// Value in range [0, 1]
pub fn normalize_noise(value: f64) -> f64 {
    (value + 1.0) / 2.0
}

/// Scale noise value from [0, 1] to [-1, 1].
///
/// # Parameters
/// - `value`: Noise value in range [0, 1]
///
/// # Returns
/// Value in range [-1, 1]
pub fn denormalize_noise(value: f64) -> f64 {
    value * 2.0 - 1.0
}

/// Generate a 2D noise map.
///
/// Creates a 2D array of noise values, useful for terrain generation,
/// texture creation, or heightmaps.
///
/// # Parameters
/// - `width`: Width of the map
/// - `height`: Height of the map
/// - `scale`: Scale factor for noise coordinates
/// - `octaves`: Number of noise layers for FBM
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// 2D vector of noise values in range [0.0, 1.0]
///
/// # Examples
/// ```
/// let map = noise_utils::noise_map_2d(64, 64, 0.1, 4, Some(42));
/// assert_eq!(map.len(), 64);
/// assert_eq!(map[0].len(), 64);
/// ```
pub fn noise_map_2d(
    width: usize,
    height: usize,
    scale: f64,
    octaves: usize,
    seed: Option<u32>,
) -> Vec<Vec<f64>> {
    (0..height)
        .map(|y| {
            (0..width)
                .map(|x| {
                    let nx = x as f64 * scale;
                    let ny = y as f64 * scale;
                    normalize_noise(fbm_2d(nx, ny, octaves, 0.5, 2.0, seed))
                })
                .collect()
        })
        .collect()
}

// ============================================================================
// Voronoi/Worley Noise
// ============================================================================

/// Generate 2D Voronoi (Worley) noise.
///
/// Voronoi noise creates cell-like patterns based on distance to
/// random points. Useful for organic textures, terrain features,
/// and procedural generation.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Distance to nearest feature point, in range [0.0, ~1.5]
///
/// # Examples
/// ```
/// let value = noise_utils::voronoi_2d(0.5, 0.5, None);
/// assert!(value >= 0.0);
/// ```
pub fn voronoi_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0);
    
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let mut min_dist = f64::MAX;
    
    // Check 3x3 neighborhood
    for dx in -1..=1 {
        for dy in -1..=1 {
            let cell_x = xi + dx;
            let cell_y = yi + dy;
            
            // Generate random point in cell
            let hash_val = hash(cell_x, cell_y, seed as usize);
            let point_x = (hash_val % 100) as f64 / 99.0;
            let point_y = ((hash_val / 100) % 100) as f64 / 99.0;
            
            // Distance to point
            let dx = xf - (dx as f64 + point_x);
            let dy = yf - (dy as f64 + point_y);
            let dist = (dx * dx + dy * dy).sqrt();
            
            min_dist = min_dist.min(dist);
        }
    }
    
    min_dist
}

/// Generate 2D Voronoi noise with second closest distance.
///
/// Useful for creating edge detection effects.
///
/// # Parameters
/// - `x`: X coordinate
/// - `y`: Y coordinate
/// - `seed`: Optional seed for reproducible results
///
/// # Returns
/// Tuple of (distance to closest, distance to second closest)
pub fn voronoi_2d_f2(x: f64, y: f64, seed: Option<u32>) -> (f64, f64) {
    let seed = seed.unwrap_or(0);
    
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let mut dist1 = f64::MAX;
    let mut dist2 = f64::MAX;
    
    for dx in -1..=1 {
        for dy in -1..=1 {
            let cell_x = xi + dx;
            let cell_y = yi + dy;
            
            let hash_val = hash(cell_x, cell_y, seed as usize);
            let point_x = (hash_val % 100) as f64 / 99.0;
            let point_y = ((hash_val / 100) % 100) as f64 / 99.0;
            
            let dx = xf - (dx as f64 + point_x);
            let dy = yf - (dy as f64 + point_y);
            let dist = (dx * dx + dy * dy).sqrt();
            
            if dist < dist1 {
                dist2 = dist1;
                dist1 = dist;
            } else if dist < dist2 {
                dist2 = dist;
            }
        }
    }
    
    (dist1, dist2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_perlin_noise_1d() {
        let v1 = perlin_noise_1d(0.0, None);
        let v2 = perlin_noise_1d(1.0, None);
        let v3 = perlin_noise_1d(0.5, None);
        
        assert!(v1 >= -1.0 && v1 <= 1.0);
        assert!(v2 >= -1.0 && v2 <= 1.0);
        assert!(v3 >= -1.0 && v3 <= 1.0);
        
        // Same seed should produce same result
        assert!((perlin_noise_1d(1.5, Some(42)) - perlin_noise_1d(1.5, Some(42))).abs() < 1e-10);
    }

    #[test]
    fn test_perlin_noise_2d() {
        let v = perlin_noise_2d(0.0, 0.0, None);
        assert!(v >= -1.0 && v <= 1.0);
        
        // Check continuity (nearby points should be similar)
        let v1 = perlin_noise_2d(0.0, 0.0, None);
        let v2 = perlin_noise_2d(0.01, 0.01, None);
        assert!((v1 - v2).abs() < 0.5);
    }

    #[test]
    fn test_perlin_noise_3d() {
        let v = perlin_noise_3d(0.0, 0.0, 0.0, None);
        assert!(v >= -1.0 && v <= 1.0);
        
        let v1 = perlin_noise_3d(1.0, 2.0, 3.0, Some(42));
        let v2 = perlin_noise_3d(1.0, 2.0, 3.0, Some(42));
        assert!((v1 - v2).abs() < 1e-10);
    }

    #[test]
    fn test_simplex_noise_2d() {
        let v = simplex_noise_2d(0.0, 0.0, None);
        assert!(v >= -1.0 && v <= 1.0);
        
        // Same seed = same result
        let v1 = simplex_noise_2d(1.5, 2.5, Some(42));
        let v2 = simplex_noise_2d(1.5, 2.5, Some(42));
        assert!((v1 - v2).abs() < 1e-10);
    }

    #[test]
    fn test_simplex_noise_3d() {
        let v = simplex_noise_3d(0.0, 0.0, 0.0, None);
        assert!(v >= -1.0 && v <= 1.0);
    }

    #[test]
    fn test_value_noise_2d() {
        let v = value_noise_2d(0.0, 0.0, None);
        assert!(v >= 0.0 && v <= 1.0);
        
        let v1 = value_noise_2d(1.0, 2.0, Some(42));
        let v2 = value_noise_2d(1.0, 2.0, Some(42));
        assert!((v1 - v2).abs() < 1e-10);
    }

    #[test]
    fn test_white_noise() {
        let samples = white_noise(100, Some(42));
        assert_eq!(samples.len(), 100);
        
        for s in &samples {
            assert!(*s >= -1.0 && *s <= 1.0);
        }
        
        // Same seed = same sequence
        let s1 = white_noise(10, Some(42));
        let s2 = white_noise(10, Some(42));
        for i in 0..10 {
            assert!((s1[i] - s2[i]).abs() < 1e-10);
        }
    }

    #[test]
    fn test_white_noise_01() {
        let samples = white_noise_01(100, Some(42));
        assert_eq!(samples.len(), 100);
        
        for s in &samples {
            assert!(*s >= 0.0 && *s <= 1.0);
        }
    }

    #[test]
    fn test_pink_noise() {
        let samples = pink_noise(256, Some(42));
        assert_eq!(samples.len(), 256);
        
        for s in &samples {
            assert!(*s >= -1.0 && *s <= 1.0);
        }
    }

    #[test]
    fn test_brown_noise() {
        let samples = brown_noise(256, Some(42));
        assert_eq!(samples.len(), 256);
        
        for s in &samples {
            assert!(*s >= -1.0 && *s <= 1.0);
        }
    }

    #[test]
    fn test_fbm_2d() {
        let v = fbm_2d(0.0, 0.0, 4, 0.5, 2.0, None);
        // FBM value range can vary, but should be reasonable
        assert!(v >= -2.0 && v <= 2.0);
    }

    #[test]
    fn test_ridged_multifractal() {
        let v = ridged_multifractal_2d(0.0, 0.0, 4, 0.5, 2.0, None);
        assert!(v >= 0.0);
    }

    #[test]
    fn test_turbulence_2d() {
        let v = turbulence_2d(0.0, 0.0, 4, None);
        assert!(v >= 0.0);
    }

    #[test]
    fn test_voronoi_2d() {
        let v = voronoi_2d(0.0, 0.0, None);
        assert!(v >= 0.0);
    }

    #[test]
    fn test_voronoi_2d_f2() {
        let (d1, d2) = voronoi_2d_f2(0.5, 0.5, None);
        assert!(d1 >= 0.0);
        assert!(d2 >= 0.0);
        assert!(d1 <= d2); // d1 should be closest
    }

    #[test]
    fn test_noise_map_2d() {
        let map = noise_map_2d(64, 64, 0.1, 4, Some(42));
        assert_eq!(map.len(), 64);
        assert_eq!(map[0].len(), 64);
        
        for row in &map {
            for v in row {
                assert!(*v >= 0.0 && *v <= 1.0);
            }
        }
    }

    #[test]
    fn test_normalize_denormalize() {
        assert!((normalize_noise(-1.0) - 0.0).abs() < 1e-10);
        assert!((normalize_noise(0.0) - 0.5).abs() < 1e-10);
        assert!((normalize_noise(1.0) - 1.0).abs() < 1e-10);
        
        assert!((denormalize_noise(0.0) - (-1.0)).abs() < 1e-10);
        assert!((denormalize_noise(0.5) - 0.0).abs() < 1e-10);
        assert!((denormalize_noise(1.0) - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_edge_cases() {
        // Empty white noise
        let samples = white_noise(0, None);
        assert_eq!(samples.len(), 0);
        
        // Single sample
        let samples = white_noise(1, None);
        assert_eq!(samples.len(), 1);
        
        // Large values
        let v = perlin_noise_2d(1000000.0, 1000000.0, None);
        assert!(v >= -1.0 && v <= 1.0);
        
        // Negative values
        let v = perlin_noise_2d(-100.0, -200.0, None);
        assert!(v >= -1.0 && v <= 1.0);
    }

    #[test]
    fn test_noise_continuity() {
        // Perlin noise should be smooth
        let steps = 100;
        let mut max_diff = 0.0;
        
        for i in 0..steps {
            let t = i as f64 / steps as f64;
            let v1 = perlin_noise_2d(t, t, None);
            let v2 = perlin_noise_2d(t + 0.01, t + 0.01, None);
            max_diff = max_diff.max((v1 - v2).abs());
        }
        
        // Adjacent values should be close (noise is smooth)
        assert!(max_diff < 0.3);
    }

    #[test]
    fn test_value_noise_1d() {
        let v = value_noise_1d(0.0, None);
        assert!(v >= 0.0 && v <= 1.0);
        
        let v1 = value_noise_1d(1.0, Some(42));
        let v2 = value_noise_1d(1.0, Some(42));
        assert!((v1 - v2).abs() < 1e-10);
    }
}