//! Math Utilities Test Suite
use std::cmp::Ordering;

#[test]
fn test_clamp() {
    assert_eq!(clamp(150.0, 0.0, 100.0), 100.0);
    assert_eq!(clamp(-10.0, 0.0, 100.0), 0.0);
    assert_eq!(clamp(50.0, 0.0, 100.0), 50.0);
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
    assert_eq!(median(&[]), None);
}

#[test]
fn test_min_max() {
    assert_eq!(min_max(&[3.0, 1.0, 4.0, 5.0]), Some((1.0, 5.0)));
    assert_eq!(min_max(&[]), None);
}

#[test]
fn test_std_dev() {
    let data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
    let sd = std_dev(&data).unwrap();
    assert!(sd > 1.9 && sd < 2.1);
}

#[test]
fn test_factorial() {
    assert_eq!(factorial(0), 1);
    assert_eq!(factorial(5), 120);
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
fn test_angle_conversion() {
    assert!((to_radians(180.0) - std::f64::consts::PI).abs() < 1e-10);
    assert!((to_degrees(std::f64::consts::PI) - 180.0).abs() < 1e-10);
}

#[test]
fn test_normalize_angle() {
    assert!((normalize_angle_360(450.0) - 90.0).abs() < 1e-10);
    assert!((normalize_angle_180(270.0) - (-90.0)).abs() < 1e-10);
}

#[test]
fn test_distance() {
    assert_eq!(distance_2d(0.0, 0.0, 3.0, 4.0), 5.0);
    assert_eq!(distance_3d(0.0, 0.0, 0.0, 1.0, 1.0, 1.0), (3.0_f64).sqrt());
}

#[test]
fn test_format_with_commas() {
    assert_eq!(format_with_commas(1234567), "1,234,567");
    assert_eq!(format_with_commas(-1000), "-1,000");
}

// Implementations
fn clamp<T: PartialOrd + Copy>(value: T, min: T, max: T) -> T {
    if value < min { min } else if value > max { max } else { value }
}

fn lerp(start: f64, end: f64, t: f64) -> f64 {
    start + (end - start) * t
}

fn map_range(value: f64, in_min: f64, in_max: f64, out_min: f64, out_max: f64) -> f64 {
    if (in_max - in_min).abs() < f64::EPSILON { return out_min; }
    out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)
}

fn approx_eq(a: f64, b: f64, epsilon: f64) -> bool {
    (a - b).abs() <= epsilon
}

fn round_to(value: f64, decimals: u32) -> f64 {
    let multiplier = 10f64.powi(decimals as i32);
    (value * multiplier).round() / multiplier
}

fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() { return None; }
    Some(values.iter().sum::<f64>() / values.len() as f64)
}

fn median(values: &[f64]) -> Option<f64> {
    if values.is_empty() { return None; }
    let mut sorted = values.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    let mid = sorted.len() / 2;
    if sorted.len() % 2 == 0 {
        Some((sorted[mid - 1] + sorted[mid]) / 2.0)
    } else {
        Some(sorted[mid])
    }
}

fn min_max(values: &[f64]) -> Option<(f64, f64)> {
    if values.is_empty() { return None; }
    let (mut min, mut max) = (values[0], values[0]);
    for &v in &values[1..] {
        if v < min { min = v; }
        if v > max { max = v; }
    }
    Some((min, max))
}

fn std_dev(values: &[f64]) -> Option<f64> {
    let m = mean(values)?;
    let variance = values.iter().map(|&v| (v - m).powi(2)).sum::<f64>() / values.len() as f64;
    Some(variance.sqrt())
}

fn factorial(n: u32) -> u64 {
    if n <= 1 { return 1; }
    (2..=n as u64).product()
}

fn is_prime(n: u64) -> bool {
    if n < 2 { return false; }
    if n == 2 { return true; }
    if n % 2 == 0 { return false; }
    let limit = (n as f64).sqrt() as u64;
    for i in (3..=limit).step_by(2) {
        if n % i == 0 { return false; }
    }
    true
}

fn gcd(a: u64, b: u64) -> u64 {
    if a == 0 { return b; }
    if b == 0 { return a; }
    let (mut x, mut y) = (a, b);
    while y != 0 {
        let temp = y;
        y = x % y;
        x = temp;
    }
    x
}

fn lcm(a: u64, b: u64) -> u64 {
    if a == 0 || b == 0 { return 0; }
    (a * b) / gcd(a, b)
}

fn to_radians(degrees: f64) -> f64 {
    degrees * std::f64::consts::PI / 180.0
}

fn to_degrees(radians: f64) -> f64 {
    radians * 180.0 / std::f64::consts::PI
}

fn normalize_angle_360(angle: f64) -> f64 {
    let mut result = angle % 360.0;
    if result < 0.0 { result += 360.0; }
    result
}

fn normalize_angle_180(angle: f64) -> f64 {
    let mut result = normalize_angle_360(angle);
    if result >= 180.0 { result -= 360.0; }
    result
}

fn distance_2d(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2)).sqrt()
}

fn distance_3d(x1: f64, y1: f64, z1: f64, x2: f64, y2: f64, z2: f64) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2) + (z2 - z1).powi(2)).sqrt()
}

fn format_with_commas(n: i64) -> String {
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
