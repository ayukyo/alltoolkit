//! Noise Utilities Test Suite
//!
//! Comprehensive tests for all noise generation functions.

use std::process::Command;

// ============================================================================
// Helper functions
// ============================================================================

fn fade(t: f64) -> f64 {
    t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
}

fn lerp(a: f64, b: f64, t: f64) -> f64 {
    a + t * (b - a)
}

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

fn get_perm() -> Vec<u8> {
    let mut perm = PERM.to_vec();
    perm.extend_from_slice(&PERM);
    perm
}

fn grad_2d(hash: u8, x: f64, y: f64) -> f64 {
    let h = hash & 7;
    let u = if h < 4 { x } else { y };
    let v = if h < 4 { y } else { x };
    (if (h & 1) == 0 { u } else { -u }) + (if (h & 2) == 0 { v } else { -v })
}

fn grad_3d(hash: u8, x: f64, y: f64, z: f64) -> f64 {
    let h = hash & 15;
    let u = if h < 8 { x } else { y };
    let v = if h < 4 { y } else if h == 12 || h == 14 { x } else { z };
    (if (h & 1) == 0 { u } else { -u }) + (if (h & 2) == 0 { v } else { -v })
}

fn hash(x: i64, y: i64, seed: usize) -> usize {
    let mut h = (x as usize).wrapping_mul(374761393);
    h = h.wrapping_add((y as usize).wrapping_mul(668265263));
    h = h.wrapping_add(seed);
    (h ^ (h >> 13)).wrapping_mul(1274126177)
}

// ============================================================================
// Perlin Noise
// ============================================================================

fn perlin_noise_1d(x: f64, seed: Option<u32>) -> f64 {
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

fn perlin_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
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
    
    lerp(lerp(grad_aa, grad_ba, u), lerp(grad_ab, grad_bb, u), v)
}

fn perlin_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64 {
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
    
    let y1 = lerp(lerp(n000, n100, u), lerp(n010, n110, u), v);
    let y2 = lerp(lerp(n001, n101, u), lerp(n011, n111, u), v);
    
    lerp(y1, y2, w)
}

// ============================================================================
// Simplex Noise
// ============================================================================

const F2: f64 = 0.3660254037844386;
const G2: f64 = 0.21132486540518713;
const F3: f64 = 0.3333333333333333;
const G3: f64 = 0.16666666666666666;

fn grad_simplex_2d(gi: usize, x: f64, y: f64) -> f64 {
    let grad = [
        (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0),
        (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
        (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0),
    ];
    let (gx, gy) = grad[gi % 12];
    gx * x + gy * y
}

fn simplex_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    let s = (x + y) * F2;
    let i = (x + s).floor() as i64;
    let j = (y + s).floor() as i64;
    let t = (i + j) as f64 * G2;
    let x0 = x - (i as f64 - t);
    let y0 = y - (j as f64 - t);
    
    let (i1, j1) = if x0 > y0 { (1, 0) } else { (0, 1) };
    let x1 = x0 - i1 as f64 + G2;
    let y1 = y0 - j1 as f64 + G2;
    let x2 = x0 - 1.0 + 2.0 * G2;
    let y2 = y0 - 1.0 + 2.0 * G2;
    
    let ii = ((i & 255) as usize + seed) & 255;
    let jj = (j & 255) as usize;
    
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
    
    70.0 * (n0 + n1 + n2)
}

fn grad_simplex_3d(gi: usize, x: f64, y: f64, z: f64) -> f64 {
    let grad = [
        (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0),
        (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0),
        (0.0, 1.0, 1.0), (0.0, -1.0, 1.0), (0.0, 1.0, -1.0), (0.0, -1.0, -1.0),
    ];
    let (gx, gy, gz) = grad[gi % 12];
    gx * x + gy * y + gz * z
}

fn simplex_noise_3d(x: f64, y: f64, z: f64, seed: Option<u32>) -> f64 {
    let perm = get_perm();
    let seed = seed.unwrap_or(0) as usize;
    
    let s = (x + y + z) * F3;
    let i = (x + s).floor() as i64;
    let j = (y + s).floor() as i64;
    let k = (z + s).floor() as i64;
    let t = (i + j + k) as f64 * G3;
    let x0 = x - (i as f64 - t);
    let y0 = y - (j as f64 - t);
    let z0 = z - (k as f64 - t);
    
    let (i1, j1, k1, i2, j2, k2) = if x0 >= y0 {
        if y0 >= z0 { (1, 0, 0, 1, 1, 0) }
        else if x0 >= z0 { (1, 0, 0, 1, 0, 1) }
        else { (0, 0, 1, 1, 0, 1) }
    } else {
        if y0 < z0 { (0, 0, 1, 0, 1, 1) }
        else if x0 < z0 { (0, 1, 0, 0, 1, 1) }
        else { (0, 1, 0, 1, 1, 0) }
    };
    
    let x1 = x0 - i1 as f64 + G3;
    let y1 = y0 - j1 as f64 + G3;
    let z1 = z0 - k1 as f64 + G3;
    let x2 = x0 - i2 as f64 + 2.0 * G3;
    let y2 = y0 - j2 as f64 + 2.0 * G3;
    let z2 = z0 - k2 as f64 + 2.0 * G3;
    let x3 = x0 - 1.0 + 3.0 * G3;
    let y3 = y0 - 1.0 + 3.0 * G3;
    let z3 = z0 - 1.0 + 3.0 * G3;
    
    let ii = ((i & 255) as usize + seed) & 255;
    let jj = (j & 255) as usize;
    let kk = (k & 255) as usize;
    
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

// ============================================================================
// Value Noise
// ============================================================================

fn value_noise_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0) as usize;
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let v00 = (hash(xi, yi, seed) % 10000) as f64 / 9999.0;
    let v10 = (hash(xi + 1, yi, seed) % 10000) as f64 / 9999.0;
    let v01 = (hash(xi, yi + 1, seed) % 10000) as f64 / 9999.0;
    let v11 = (hash(xi + 1, yi + 1, seed) % 10000) as f64 / 9999.0;
    
    lerp(lerp(v00, v10, fade(xf)), lerp(v01, v11, fade(xf)), fade(yf))
}

fn value_noise_1d(x: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0) as usize;
    let xi = x.floor() as i64;
    let v0 = (hash(xi, 0, seed) % 10000) as f64 / 9999.0;
    let v1 = (hash(xi + 1, 0, seed) % 10000) as f64 / 9999.0;
    lerp(v0, v1, fade(x - x.floor()))
}

// ============================================================================
// White, Pink, Brown Noise
// ============================================================================

struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self { Lcg { state: seed } }
    fn next(&mut self) -> u64 {
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.state
    }
    fn next_f64(&mut self) -> f64 { (self.next() >> 11) as f64 / (1u64 << 53) as f64 }
}

fn white_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    (0..count).map(|_| rng.next_f64() * 2.0 - 1.0).collect()
}

fn white_noise_01(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    (0..count).map(|_| rng.next_f64()).collect()
}

fn pink_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    let mut result = Vec::with_capacity(count);
    let mut b = [0.0; 7];
    
    for i in 0..count {
        let mut sum = 0.0;
        for j in 0..7 {
            if (i & (1 << j)) == 0 { b[j] = rng.next_f64() * 2.0 - 1.0; }
            sum += b[j];
        }
        sum += rng.next_f64() * 2.0 - 1.0;
        result.push(sum / 8.0);
    }
    
    let max = result.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let min = result.iter().cloned().fold(f64::INFINITY, f64::min);
    if max > min {
        for v in &mut result { *v = (*v - min) / (max - min) * 2.0 - 1.0; }
    }
    result
}

fn brown_noise(count: usize, seed: Option<u64>) -> Vec<f64> {
    let mut rng = Lcg::new(seed.unwrap_or(12345));
    let mut result = Vec::with_capacity(count);
    let mut sum = 0.0;
    
    for _ in 0..count {
        sum += rng.next_f64() * 2.0 - 1.0;
        sum = sum.clamp(-1.0, 1.0);
        result.push(sum);
    }
    
    let max = result.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let min = result.iter().cloned().fold(f64::INFINITY, f64::min);
    if max > min {
        for v in &mut result { *v = (*v - min) / (max - min) * 2.0 - 1.0; }
    }
    result
}

// ============================================================================
// FBM, Voronoi, etc.
// ============================================================================

fn fbm_2d(x: f64, y: f64, octaves: usize, persistence: f64, lacunarity: f64, seed: Option<u32>) -> f64 {
    let mut total = 0.0;
    let mut freq = 1.0;
    let mut amp = 1.0;
    let mut max_val = 0.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        total += perlin_noise_2d(x * freq, y * freq, Some(seed + i as u32)) * amp;
        max_val += amp;
        amp *= persistence;
        freq *= lacunarity;
    }
    total / max_val
}

fn ridged_multifractal_2d(x: f64, y: f64, octaves: usize, persistence: f64, lacunarity: f64, seed: Option<u32>) -> f64 {
    let mut total = 0.0;
    let mut freq = 1.0;
    let mut amp = 1.0;
    let mut weight = 1.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        let sig = (1.0 - perlin_noise_2d(x * freq, y * freq, Some(seed + i as u32)).abs()).powi(2) * weight;
        weight = (sig * 2.0).clamp(0.0, 1.0);
        total += sig * amp;
        amp *= persistence;
        freq *= lacunarity;
    }
    total
}

fn turbulence_2d(x: f64, y: f64, octaves: usize, seed: Option<u32>) -> f64 {
    let mut total = 0.0;
    let mut freq = 1.0;
    let mut amp = 1.0;
    let seed = seed.unwrap_or(0);
    
    for i in 0..octaves {
        total += perlin_noise_2d(x * freq, y * freq, Some(seed + i as u32)).abs() * amp;
        amp *= 0.5;
        freq *= 2.0;
    }
    total
}

fn voronoi_2d(x: f64, y: f64, seed: Option<u32>) -> f64 {
    let seed = seed.unwrap_or(0) as usize;
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let mut min_dist = f64::MAX;
    for dx in -1..=1 {
        for dy in -1..=1 {
            let h = hash(xi + dx, yi + dy, seed);
            let px = (h % 100) as f64 / 99.0;
            let py = ((h / 100) % 100) as f64 / 99.0;
            let d = ((xf - (dx as f64 + px)).powi(2) + (yf - (dy as f64 + py)).powi(2)).sqrt();
            min_dist = min_dist.min(d);
        }
    }
    min_dist
}

fn voronoi_2d_f2(x: f64, y: f64, seed: Option<u32>) -> (f64, f64) {
    let seed = seed.unwrap_or(0) as usize;
    let xi = x.floor() as i64;
    let yi = y.floor() as i64;
    let xf = x - x.floor();
    let yf = y - y.floor();
    
    let mut d1 = f64::MAX;
    let mut d2 = f64::MAX;
    for dx in -1..=1 {
        for dy in -1..=1 {
            let h = hash(xi + dx, yi + dy, seed);
            let px = (h % 100) as f64 / 99.0;
            let py = ((h / 100) % 100) as f64 / 99.0;
            let d = ((xf - (dx as f64 + px)).powi(2) + (yf - (dy as f64 + py)).powi(2)).sqrt();
            if d < d1 { d2 = d1; d1 = d; }
            else if d < d2 { d2 = d; }
        }
    }
    (d1, d2)
}

fn normalize_noise(v: f64) -> f64 { (v + 1.0) / 2.0 }

fn noise_map_2d(w: usize, h: usize, scale: f64, octaves: usize, seed: Option<u32>) -> Vec<Vec<f64>> {
    (0..h).map(|y| (0..w).map(|x| normalize_noise(fbm_2d(x as f64 * scale, y as f64 * scale, octaves, 0.5, 2.0, seed))).collect()).collect()
}

// ============================================================================
// Tests
// ============================================================================

#[test]
fn test_perlin_1d_basic() {
    let v = perlin_noise_1d(0.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_perlin_1d_reproducible() {
    assert!((perlin_noise_1d(1.5, Some(42)) - perlin_noise_1d(1.5, Some(42))).abs() < 1e-10);
}

#[test]
fn test_perlin_2d_basic() {
    let v = perlin_noise_2d(0.0, 0.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_perlin_2d_reproducible() {
    assert!((perlin_noise_2d(1.5, 2.5, Some(42)) - perlin_noise_2d(1.5, 2.5, Some(42))).abs() < 1e-10);
}

#[test]
fn test_perlin_2d_continuity() {
    let v1 = perlin_noise_2d(0.0, 0.0, None);
    let v2 = perlin_noise_2d(0.01, 0.01, None);
    assert!((v1 - v2).abs() < 0.5);
}

#[test]
fn test_perlin_3d_basic() {
    let v = perlin_noise_3d(0.0, 0.0, 0.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_simplex_2d_basic() {
    let v = simplex_noise_2d(0.0, 0.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_simplex_2d_reproducible() {
    assert!((simplex_noise_2d(1.5, 2.5, Some(42)) - simplex_noise_2d(1.5, 2.5, Some(42))).abs() < 1e-10);
}

#[test]
fn test_simplex_3d_basic() {
    let v = simplex_noise_3d(0.0, 0.0, 0.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_value_2d_basic() {
    let v = value_noise_2d(0.0, 0.0, None);
    assert!(v >= 0.0 && v <= 1.0);
}

#[test]
fn test_value_1d_basic() {
    let v = value_noise_1d(0.0, None);
    assert!(v >= 0.0 && v <= 1.0);
}

#[test]
fn test_white_basic() {
    let s = white_noise(100, Some(42));
    assert_eq!(s.len(), 100);
    for v in &s { assert!(*v >= -1.0 && *v <= 1.0); }
}

#[test]
fn test_white_reproducible() {
    let s1 = white_noise(10, Some(42));
    let s2 = white_noise(10, Some(42));
    for i in 0..10 { assert!((s1[i] - s2[i]).abs() < 1e-10); }
}

#[test]
fn test_white_empty() {
    assert_eq!(white_noise(0, None).len(), 0);
}

#[test]
fn test_pink_basic() {
    let s = pink_noise(256, Some(42));
    assert_eq!(s.len(), 256);
    for v in &s { assert!(*v >= -1.0 && *v <= 1.0); }
}

#[test]
fn test_brown_basic() {
    let s = brown_noise(256, Some(42));
    assert_eq!(s.len(), 256);
    for v in &s { assert!(*v >= -1.0 && *v <= 1.0); }
}

#[test]
fn test_fbm_basic() {
    let v = fbm_2d(0.0, 0.0, 4, 0.5, 2.0, None);
    assert!(v >= -2.0 && v <= 2.0);
}

#[test]
fn test_ridged_basic() {
    let v = ridged_multifractal_2d(0.0, 0.0, 4, 0.5, 2.0, None);
    assert!(v >= 0.0);
}

#[test]
fn test_turbulence_basic() {
    let v = turbulence_2d(0.0, 0.0, 4, None);
    assert!(v >= 0.0);
}

#[test]
fn test_voronoi_basic() {
    let v = voronoi_2d(0.0, 0.0, None);
    assert!(v >= 0.0);
}

#[test]
fn test_voronoi_f2_basic() {
    let (d1, d2) = voronoi_2d_f2(0.5, 0.5, None);
    assert!(d1 >= 0.0 && d2 >= 0.0 && d1 <= d2);
}

#[test]
fn test_noise_map_basic() {
    let m = noise_map_2d(64, 64, 0.1, 4, Some(42));
    assert_eq!(m.len(), 64);
    for row in &m {
        assert_eq!(row.len(), 64);
        for v in row { assert!(*v >= 0.0 && *v <= 1.0); }
    }
}

#[test]
fn test_normalize() {
    assert!((normalize_noise(-1.0) - 0.0).abs() < 1e-10);
    assert!((normalize_noise(0.0) - 0.5).abs() < 1e-10);
    assert!((normalize_noise(1.0) - 1.0).abs() < 1e-10);
}

#[test]
fn test_edge_large() {
    let v = perlin_noise_2d(1000000.0, 1000000.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_edge_negative() {
    let v = perlin_noise_2d(-100.0, -200.0, None);
    assert!(v >= -1.0 && v <= 1.0);
}

#[test]
fn test_perlin_vs_simplex() {
    let p = perlin_noise_2d(5.0, 5.0, Some(42));
    let s = simplex_noise_2d(5.0, 5.0, Some(42));
    // Different algorithms, different values
    assert!((p - s).abs() > 0.01);
}

#[test]
fn test_noise_at_origin() {
    assert!(perlin_noise_1d(0.0, None) >= -1.0);
    assert!(perlin_noise_2d(0.0, 0.0, None) >= -1.0);
    assert!(perlin_noise_3d(0.0, 0.0, 0.0, None) >= -1.0);
    assert!(simplex_noise_2d(0.0, 0.0, None) >= -1.0);
    assert!(simplex_noise_3d(0.0, 0.0, 0.0, None) >= -1.0);
    assert!(value_noise_2d(0.0, 0.0, None) >= 0.0);
    assert!(voronoi_2d(0.0, 0.0, None) >= 0.0);
}