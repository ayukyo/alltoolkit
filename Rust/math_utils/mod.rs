//! # Math Utilities
//!
//! A collection of general-purpose mathematical utilities for Rust.
//! All functions are pure (no side effects), handle edge cases correctly,
//! and are suitable for production use.
//!
//! ## Features
//!
//! - Range clamping and mapping
//! - Linear interpolation
//! - Statistical calculations
//! - Number theory functions
//!
//! ## Usage
//!
//! ```rust
//! use math_utils::{clamp, lerp, map_range, mean, gcd};
//!
//! let bounded = clamp(150.0, 0.0, 100.0);  // 100.0
//! let interpolated = lerp(0.0, 100.0, 0.5); // 50.0
//! let avg = mean(&[1.0, 2.0, 3.0, 4.0, 5.0]); // Some(3.0)
//! let divisor = gcd(48, 18); // 6
//! ```

use std::cmp::Ordering;

/// Clamps a value within the specified inclusive range.
///
/// If the value is less than `min`, returns `min`.
/// If the value is greater than `max`, returns `max`.
/// Otherwise returns the value unchanged.
///
/// # Parameters
/// * `value` - The value to clamp
/// * `min` - The minimum bound (inclusive)
/// * `max` - The maximum bound (inclusive)
///
/// # Returns
/// The clamped value within [min, max] range.
///
/// # Examples
/// ```
/// assert_eq!(clamp(150.0, 0.0, 100.0), 100.0);
/// assert_eq!(clamp(-10.0, 0.0, 100.0), 0.0);
/// assert_eq!(clamp(50.0, 0.0, 100.0), 50.0);
/// ```
pub fn clamp<T: PartialOrd + Copy>(value: T, min: T, max: T) -> T {
    if value < min {
        min
    } else if value > max {
        max
    } else {
        value
    }
}

/// Linearly interpolates between two values.
///
/// Returns `start + (end - start) * t`.
/// When t=0, returns start. When t=1, returns end.
///
/// # Parameters
/// * `start` - The starting value (at t=0)
/// * `end` - The ending value (at t=1)
/// * `t` - The interpolation factor (typically 0.0 to 1.0)
///
/// # Returns
/// The interpolated value.
///
/// # Examples
/// ```
/// assert_eq!(lerp(0.0, 100.0, 0.5), 50.0);
/// assert_eq!(lerp(0.0, 100.0, 0.0), 0.0);
/// assert_eq!(lerp(10.0, 20.0, 0.5), 15.0);
/// ```
pub fn lerp(start: f64, end: f64, t: f64) -> f64 {
    start + (end - start) * t
}

/// Maps a value from one range to another.
///
/// Linearly transforms a value from the input range [in_min, in_max]
/// to the output range [out_min, out_max].
///
/// # Parameters
/// * `value` - The value to map
/// * `in_min` - The minimum of the input range
/// * `in_max` - The maximum of the input range
/// * `out_min` - The minimum of the output range
/// * `out_max` - The maximum of the output range
///
/// # Returns
/// The mapped value in the output range.
///
/// # Examples
/// ```
/// assert_eq!(map_range(5.0, 0.0, 10.0, 0.0, 100.0), 50.0);
/// assert_eq!(map_range(32.0, 32.0, 212.0, 0.0, 100.0), 0.0); // F to C
/// ```
pub fn map_range(value: f64, in_min: f64, in_max: f64, out_min: f64, out_max: f64) -> f64 {
    if (in_max - in_min).abs() < f64::EPSILON {
        return out_min;
    }
    out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)
}

/// Checks if two values are approximately equal within epsilon.
///
/// # Parameters
/// * `a` - First value
/// * `b` - Second value
/// * `epsilon` - The maximum allowed difference
///
/// # Returns
/// `true` if |a - b| <= epsilon.
///
/// # Examples
/// ```
/// assert!(approx_eq(1.0, 1.0001, 0.001));
/// assert!(approx_eq(0.1 + 0.2, 0.3, 1e-10));
/// ```
pub fn approx_eq(a: f64, b: f64, epsilon: f64) -> bool {
    (a - b).abs() <= epsilon
}

/// Rounds to specified decimal places.
///
/// # Parameters
/// * `value` - The value to round
/// * `decimals` - Number of decimal places
///
/// # Returns
/// The rounded value.
///
/// # Examples
/// ```
/// assert_eq!(round_to(3.14159, 2), 3.14);
/// assert_eq!(round_to(2.5, 0), 3.0);
/// ```
pub fn round_to(value: f64, decimals: u32) -> f64 {
    let multiplier = 10f64.powi(decimals as i32);
    (value * multiplier).round() / multiplier
}

/// Calculates the arithmetic mean.
///
/// # Parameters
/// * `values` - Slice of values
///
/// # Returns
/// * `Some(mean)` - The average value
/// * `None` - If slice is empty
///
/// # Examples
/// ```
/// assert_eq!(mean(&[1.0, 2.0, 3.0, 4.0, 5.0]), Some(3.0));
/// assert_eq!(mean(&[]), None);
/// ```
pub fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    Some(values.iter().sum::<f64>() / values.len() as f64)
}

/// Calculates the median value.
///
/// # Parameters
/// * `values` - Slice of values
///
/// # Returns
/// * `Some(median)` - The median value
/// * `None` - If slice is empty
///
/// # Examples
/// ```
/// assert_eq!(median(&[1.0, 2.0, 3.0, 4.0, 5.0]), Some(3.0));
/// assert_eq!(median(&[1.0, 2.0, 3.0, 4.0]), Some(2.5));
/// ```
pub fn median(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    let mut sorted = values.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    let mid = sorted.len() / 2;
    if sorted.len() % 2 == 0 {
        Some((sorted[mid - 1] + sorted[mid]) / 2.0)
    } else {
        Some(sorted[mid])
    }
}

/// Finds min and max values.
///
/// # Parameters
/// * `values` - Slice of values
///
/// # Returns
/// * `Some((min, max))` - Tuple of min and max
/// * `None` - If slice is empty
///
/// # Examples
/// ```
/// assert_eq!(min_max(&[3.0, 1.0, 4.0, 5.0]), Some((1.0, 5.0)));
/// ```
pub fn min_max(values: &[f64]) -> Option<(f64, f64)> {
    if values.is_empty() {
        return None;
    }
    let mut min = values[0];
    let mut max = values[0];
    for &v in &values[1..] {
        if v < min {
            min = v;
        }
        if v > max {
            max = v;
        }
    }
    Some((min, max))
}

/// Calculates sum of squares.
///
/// # Parameters
/// * `values` - Slice of values
///
/// # Returns
/// Sum of each value squared.
///
/// # Examples
/// ```
/// assert_eq!(sum_of_squares(&[1.0, 2.0, 3.0]), 14.0); // 1+4+9
/// ```
pub fn sum_of_squares(values: &[f64]) -> f64 {
    values.iter().map(|&v| v * v).sum()
}

/// Calculates standard deviation.
///
/// # Parameters
/// * `values` - Slice of values
///
/// # Returns
/// * `Some(stddev)` - Population standard deviation
/// * `None` - If slice is empty
///
/// # Examples
/// ```
/// let data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
/// let sd = std_dev(&data);
/// assert!(sd.unwrap() > 1.9 && sd.unwrap() < 2.1);
/// ```
pub fn std_dev(values: &[f64]) -> Option<f64> {
    let m = mean(values)?;
    let variance = values.iter().map(|&v| (v - m).powi(2)).sum::<f64>() / values.len() as f64;
    Some(variance.sqrt())
}

/// Calculates the factorial of n.
///
/// # Parameters
/// * `n` - Non-negative integer
///
/// # Returns
/// n! as u64. Returns 1 for n=0.
///
/// # Examples
/// ```
/// assert_eq!(factorial(5), 120);
/// assert_eq!(factorial(0), 1);
/// ```
pub fn factorial(n: u32) -> u64 {
    if n == 0 || n == 1 {
        return 1;
    }
    let mut result: u64 = 1;
    for i in 2..=n {
        result *= i as u64;
    }
    result
}

/// Checks if a number is prime.
///
/// # Parameters
/// * `n` - The number to check
///
/// # Returns
/// `true` if n is prime.
///
/// # Examples
/// ```
/// assert!(is_prime(17));
/// assert!(!is_prime(18));
/// assert!(!is_prime(1));
/// assert!(is_prime(2));
/// ```
pub fn is_prime(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    let limit = (n as f64).sqrt() as u64;
    for i in (3..=limit).step_by(2) {
        if n % i == 0 {
            return false;
        }
    }
    true
}

/// Calculates greatest common divisor using Euclidean algorithm.
///
/// # Parameters
/// * `a` - First number
/// * `b` - Second number
///
/// #/// Returns
/// The greatest common divisor of a and b.
///
/// # Examples
/// ```
/// assert_eq!(gcd(48, 18), 6);
/// assert_eq!(gcd(56, 98), 14);
/// ```
pub fn gcd(a: u64, b: u64) -> u64 {
    if a == 0 {
        return b;
    }
    if b == 0 {
        return a;
    }
    let mut x = a;
    let mut y = b;
    while y != 0 {
        let temp = y;
        y = x % y;
        x = temp;
    }
    x
}

/// Calculates least common multiple.
///
/// # Parameters
/// * `a` - First number
/// * `b` - Second number
///
/// # Returns
/// The least common multiple of a and b.
///
/// # Examples
/// ```
/// assert_eq!(lcm(4, 6), 12);
/// assert_eq!(lcm(5, 7), 35);
/// ```
pub fn lcm(a: u64, b: u64) -> u64 {
    if a == 0 || b == 0 {
        return 0;
    }
    (a * b) / gcd(a, b)
}

/// Converts degrees to radians.
///
/// # Parameters
/// * `degrees` - Angle in degrees
///
/// # Returns
/// Angle in radians.
pub fn to_radians(degrees: f64) -> f64 {
    degrees * std::f64::consts::PI / 180.0
}

/// Converts radians to degrees.
///
/// # Parameters
/// * `radians` - Angle in radians
///
/// # Returns
/// Angle in degrees.
pub fn to_degrees(radians: f64) -> f64 {
    radians * 180.0 / std::f64::consts::PI
}

/// Normalizes angle to [0, 360) range.
///
/// # Parameters
/// * `angle` - Angle in degrees
///
/// # Returns
/// Normalized angle in [0, 360) range.
pub fn normalize_angle_360(angle: f64) -> f64 {
    let mut result = angle % 360.0;
    if result < 0.0 {
        result += 360.0;
    }
    result
}

/// Normalizes angle to [-180, 180) range.
///
/// # Parameters
/// * `angle` - Angle in degrees
///
/// # Returns
/// Normalized angle in [-180, 180) range.
pub fn normalize_angle_180(angle: f64) -> f64 {
    let mut result = normalize_angle_360(angle);
    if result >= 180.0 {
        result -= 360.0;
    }
    result
}

/// Calculates distance between two points in 2D space.
///
/// # Parameters
/// * `x1`, `y1` - First point coordinates
/// * `x2`, `y2` - Second point coordinates
///
/// # Returns
/// Euclidean distance between the points.
pub fn distance_2d(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2)).sqrt()
}

/// Calculates distance between two points in 3D space.
///
/// # Parameters
/// * `x1`, `y1`, `z1` - First point coordinates
/// * `x2`, `y2`, `z2` - Second point coordinates
///
/// # Returns
/// Euclidean distance between the points.
pub fn distance_3d(x1: f64, y1: f64, z1: f64, x2: f64, y2: f64, z2: f64) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2) + (z2 - z1).powi(2)).sqrt()
}

/// Formats a number with thousand separators.
///
/// # Parameters
/// * `n` - The number to format
///
/// # Returns
/// String with commas as thousand separators.
///
/// # Examples
/// ```
/// assert_eq!(format_with_commas(1234567), "1,234,567");
/// assert_eq!(format_with_commas(-1000), "-1,000");
/// ```
pub fn format_with_commas(n: i64) -> String {
    let s = n.to_string();
    let mut result = String::new();
    let chars: Vec<char> = s.chars().collect();
    let len = chars.len();
    for (i, c) in chars.iter().enumerate() {
        if i > 0 && (len - i) % 3 == 0 && *c != '-' {
            result.push(',');
        }
        result.push(*c);
    }
    result
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_clamp() {
        assert_eq!(clamp(150.0, 0.0, 100.0), 100.0);
        assert_eq!(clamp(-10.0, 0.0, 100.0), 0.0);
        assert_eq!(clamp(50.0, 0.0, 100.0), 50.0);
        assert_eq!(clamp(5i32, 0, 10), 5);
    }

    #[test]
    fn test_lerp() {
        assert_eq!(lerp(0.0, 100.0, 0.5), 50.0);
        assert_eq!(lerp(0.0, 100.0, 0.0), 0.0);
        assert_eq!(lerp(10.0, 20.0, 0.5), 15.0);
    }

    #[test]
    fn test_map_range() {
        assert_eq!(map_range(5.0, 0.0, 10.0, 0.0, 100.0), 50.0);
        assert_eq!(map_range(32.0, 32.0, 212.0, 0.0, 100.0), 0.0);
    }

    #[test]
    fn test_approx_eq() {
        assert!(approx_eq(1.0, 1.0001, 0.001));
        assert!(!approx_eq(1.0, 2.0, 0.001));
    }

    #[test]
    fn test_round_to() {
        assert_eq!(round_to(3.14159, 2), 3.14);
        assert_eq!(round_to(2.5, 0), 3.0);
    }

    #[test]
    fn test_mean() {
        assert_eq!(mean(&[1.0, 2.0, 3.0, 4.0, 5.0]), Some(3.0));
        assert_eq!(mean(&[]), None);
    }

    #[test]
    fn test_median() {
        assert_eq!(median(&[1.0, 2.0, 3.0, 4.0, 5.0]), Some(3.0));
        assert_eq!(median(&[1.0, 2.0, 3.0, 4.0]), Some(2.5));
    }

    #[test]
    fn test_min_max() {
        assert_eq!(min_max(&[3.0, 1.0, 4.0, 5.0]), Some((1.0, 5.0)));
    }

    #[test]
    fn test_std_dev() {
        let data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
        let sd = std_dev(&data).unwrap();
        assert!(sd > 1.9 && sd < 2.1);
    }

    #[test]
    fn test_factorial() {
        assert_eq!(factorial(5), 120);
        assert_eq!(factorial(0), 1);
    }

    #[test]
    fn test_is_prime() {
        assert!(is_prime(17));
        assert!(!is_prime(18));
        assert!(is_prime(2));
    }

    #[test]
    fn test_gcd() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(56, 98), 14);
    }

    #[test]
    fn test_lcm() {
        assert_eq!(lcm(4, 6), 12);
        assert_eq!(lcm(5, 7), 35);
    }

    #[test]
    fn test_distance_2d() {
        assert_eq!(distance_2d(0.0, 0.0, 3.0, 4.0), 5.0);
    }

    #[test]
    fn test_distance_3d() {
        assert_eq!(distance_3d(0.0, 0.0, 0.0, 1.0, 1.0, 1.0), (3.0 as f64).sqrt());
    }

    #[test]
    fn test_format_with_commas() {
        assert_eq!(format_with_commas(1234567), "1,234,567");
        assert_eq!(format_with_commas(-1000), "-1,000");
        assert_eq!(format_with_commas(0), "0");
    }
}
