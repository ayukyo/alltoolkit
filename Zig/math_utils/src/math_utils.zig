const std = @import("std");

/// Math operation errors
pub const MathError = error{
    Overflow,
    Underflow,
    InvalidArgument,
    OutOfRange,
};

// ============================================================================
// Constants
// ============================================================================

pub const PI: f64 = 3.14159265358979323846;
pub const E: f64 = 2.71828182845904523536;
pub const PHI: f64 = 1.61803398874989484820; // Golden ratio
pub const SQRT2: f64 = 1.41421356237309504880;
pub const LN2: f64 = 0.69314718055994530942;
pub const LN10: f64 = 2.30258509299404568402;
pub const EPSILON: f64 = 1e-10;

// ============================================================================
// Basic Operations
// ============================================================================

/// Absolute value for integers
pub fn absInt(comptime T: type, value: T) T {
    return if (value < 0) -value else value;
}

/// Absolute value for floats
pub fn abs(value: f64) f64 {
    return if (value < 0) -value else value;
}

/// Minimum of two values
pub fn min(comptime T: type, a: T, b: T) T {
    return if (a < b) a else b;
}

/// Maximum of two values
pub fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

/// Clamp value to range
pub fn clamp(comptime T: type, value: T, lower: T, upper: T) T {
    return min(T, max(T, value, lower), upper);
}

/// Sign of a number (-1, 0, or 1)
pub fn sign(value: f64) f64 {
    if (value > 0) return 1.0;
    if (value < 0) return -1.0;
    return 0.0;
}

/// Check if value is approximately equal
pub fn approxEquals(a: f64, b: f64, tolerance: f64) bool {
    return abs(a - b) < tolerance;
}

/// Check if value is near zero
pub fn isNearZero(value: f64, tolerance: f64) bool {
    return abs(value) < tolerance;
}

// ============================================================================
// Rounding Functions
// ============================================================================

/// Floor - round down to nearest integer
pub fn floor(value: f64) f64 {
    if (value >= 0) {
        return @floatFromInt(@as(i64, @intFromFloat(value)));
    }
    const int_part: i64 = @intFromFloat(value);
    if (value == @as(f64, @floatFromInt(int_part))) {
        return value;
    }
    return @floatFromInt(int_part - 1);
}

/// Ceil - round up to nearest integer
pub fn ceil(value: f64) f64 {
    if (value <= 0) {
        return @floatFromInt(@as(i64, @intFromFloat(value)));
    }
    const int_part: i64 = @intFromFloat(value);
    if (value == @as(f64, @floatFromInt(int_part))) {
        return value;
    }
    return @floatFromInt(int_part + 1);
}

/// Round to nearest integer
pub fn round(value: f64) f64 {
    if (value >= 0) {
        return floor(value + 0.5);
    }
    return -floor(-value + 0.5);
}

/// Truncate - remove decimal part
pub fn trunc(value: f64) f64 {
    return @floatFromInt(@as(i64, @intFromFloat(value)));
}

/// Round to specified decimal places
pub fn roundTo(value: f64, places: u32) f64 {
    const factor = pow(10.0, @as(f64, @floatFromInt(places)));
    return round(value * factor) / factor;
}

// ============================================================================
// Power and Root Functions
// ============================================================================

/// Integer power
pub fn powInt(base: i64, exponent: u32) i64 {
    if (exponent == 0) return 1;
    var result: i64 = 1;
    var b = base;
    var e = exponent;
    while (e > 0) {
        if (e % 2 == 1) {
            result *= b;
        }
        b *= b;
        e /= 2;
    }
    return result;
}

/// Float power using Newton-Raphson for fractional exponents
pub fn pow(base: f64, exponent: f64) f64 {
    if (exponent == 0) return 1.0;
    if (base == 0) return 0.0;
    if (base < 0) {
        // Handle negative base only for integer exponents
        const exp_int = @as(i64, @intFromFloat(exponent));
        if (approxEquals(exponent, @as(f64, @floatFromInt(exp_int)), EPSILON)) {
            const result = pow(@abs(base), exponent);
            return if (@rem(exp_int, 2) == 0) result else -result;
        }
        return std.math.nan(f64);
    }
    // Use exp and ln: base^exp = e^(exp * ln(base))
    return expNatural(exponent * ln(base));
}

/// Square root using Newton-Raphson method
pub fn sqrt(value: f64) f64 {
    if (value < 0) return std.math.nan(f64);
    if (value == 0) return 0.0;
    
    var x = value;
    var i: usize = 0;
    while (i < 100) : (i += 1) {
        const x_new = 0.5 * (x + value / x);
        if (abs(x_new - x) < EPSILON) {
            return x_new;
        }
        x = x_new;
    }
    return x;
}

/// Cube root
pub fn cbrt(value: f64) f64 {
    if (value >= 0) {
        return pow(value, 1.0 / 3.0);
    }
    return -pow(-value, 1.0 / 3.0);
}

/// Nth root
pub fn nthRoot(value: f64, n: u32) f64 {
    if (n == 0) return std.math.nan(f64);
    return pow(value, 1.0 / @as(f64, @floatFromInt(n)));
}

/// Check if value is a perfect square
pub fn isPerfectSquare(value: u64) bool {
    if (value == 0 or value == 1) return true;
    const root = @as(u64, @intFromFloat(sqrt(@as(f64, @floatFromInt(value)))));
    return root * root == value or (root + 1) * (root + 1) == value;
}

// ============================================================================
// Trigonometric Functions
// ============================================================================

/// Convert degrees to radians
pub fn degToRad(degrees: f64) f64 {
    return degrees * PI / 180.0;
}

/// Convert radians to degrees
pub fn radToDeg(radians: f64) f64 {
    return radians * 180.0 / PI;
}

/// Normalize angle to [0, 2*PI)
pub fn normalizeAngle(radians: f64) f64 {
    var angle = @mod(radians, 2.0 * PI);
    if (angle < 0) angle += 2.0 * PI;
    return angle;
}

/// Sine using Taylor series
pub fn sin(radians: f64) f64 {
    const x = normalizeAngle(radians);
    var result: f64 = 0.0;
    var term: f64 = x;
    var i: u32 = 1;
    while (abs(term) > EPSILON) {
        result += term;
        term *= -x * x / @as(f64, @floatFromInt((2 * i) * (2 * i + 1)));
        i += 1;
        if (i > 50) break;
    }
    return result;
}

/// Cosine using Taylor series
pub fn cos(radians: f64) f64 {
    return sin(radians + PI / 2.0);
}

/// Tangent
pub fn tan(radians: f64) f64 {
    const c = cos(radians);
    if (isNearZero(c, EPSILON)) return std.math.nan(f64);
    return sin(radians) / c;
}

/// Arcsine
pub fn arcsin(value: f64) f64 {
    if (value < -1.0 or value > 1.0) return std.math.nan(f64);
    // Use Taylor series for arcsin
    var result: f64 = value;
    var term: f64 = value;
    var i: u32 = 1;
    while (abs(term) > EPSILON and i < 50) {
        term *= value * value * @as(f64, @floatFromInt(2 * i - 1)) * @as(f64, @floatFromInt(2 * i - 1)) / @as(f64, @floatFromInt(2 * i)) / @as(f64, @floatFromInt(2 * i + 1));
        result += term;
        i += 1;
    }
    return result;
}

/// Arccosine
pub fn arccos(value: f64) f64 {
    return PI / 2.0 - arcsin(value);
}

/// Arctangent
pub fn arctan(value: f64) f64 {
    return arcsin(value / sqrt(1.0 + value * value));
}

/// Arctangent2 (handles all quadrants)
pub fn arctan2(y: f64, x: f64) f64 {
    if (x > 0) return arctan(y / x);
    if (x < 0) {
        if (y >= 0) return arctan(y / x) + PI;
        return arctan(y / x) - PI;
    }
    if (y > 0) return PI / 2.0;
    if (y < 0) return -PI / 2.0;
    return 0.0; // undefined case
}

// ============================================================================
// Logarithmic and Exponential Functions
// ============================================================================

/// Natural logarithm using Newton-Raphson
pub fn ln(value: f64) f64 {
    if (value <= 0) return std.math.nan(f64);
    if (value == 1.0) return 0.0;
    
    var x = value;
    // Normalize to [0.5, 1.5] range for better convergence
    var adjustment: f64 = 0.0;
    while (x > 1.5) {
        x /= E;
        adjustment += 1.0;
    }
    while (x < 0.5) {
        x *= E;
        adjustment -= 1.0;
    }
    
    // Newton-Raphson for ln(x)
    var result = x - 1.0; // Initial guess
    var i: usize = 0;
    while (i < 100) {
        const exp_val = expNatural(result);
        const new_result = result - (exp_val - x) / exp_val;
        if (abs(new_result - result) < EPSILON) {
            return new_result + adjustment;
        }
        result = new_result;
        i += 1;
    }
    return result + adjustment;
}

/// Exponential function e^x using Taylor series
pub fn expNatural(value: f64) f64 {
    // Handle large values
    if (value > 700) return std.math.inf(f64);
    if (value < -700) return 0.0;
    
    var result: f64 = 1.0;
    var term: f64 = 1.0;
    var i: usize = 1;
    while (i < 100) {
        term *= value / @as(f64, @floatFromInt(i));
        result += term;
        if (abs(term) < EPSILON) break;
        i += 1;
    }
    return result;
}

/// Logarithm base 10
pub fn log10(value: f64) f64 {
    return ln(value) / LN10;
}

/// Logarithm base 2
pub fn log2(value: f64) f64 {
    return ln(value) / LN2;
}

/// Logarithm with arbitrary base
pub fn log(base: f64, value: f64) f64 {
    return ln(value) / ln(base);
}

/// General exponential (base^exp)
pub fn exp(base: f64, exp_val: f64) f64 {
    return pow(base, exp_val);
}

// ============================================================================
// Number Theory
// ============================================================================

/// Check if a number is prime (deterministic for u64)
pub fn isPrime(n: u64) bool {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    if (n == 3) return true;
    if (n % 3 == 0) return false;
    
    var i: u64 = 5;
    const sqrt_n = @as(u64, @intFromFloat(sqrt(@as(f64, @floatFromInt(n)))));
    while (i <= sqrt_n) {
        if (n % i == 0 or n % (i + 2) == 0) return false;
        i += 6;
    }
    return true;
}

/// Greatest common divisor (Euclidean algorithm)
pub fn gcd(a: u64, b: u64) u64 {
    var x = a;
    var y = b;
    while (y != 0) {
        const temp = y;
        y = x % y;
        x = temp;
    }
    return x;
}

/// Least common multiple
pub fn lcm(a: u64, b: u64) u64 {
    if (a == 0 or b == 0) return 0;
    return (a / gcd(a, b)) * b;
}

/// Factorial (with overflow checking for u64)
pub fn factorial(n: u32) u64 {
    if (n > 20) return 0; // Overflow for u64
    var result: u64 = 1;
    var i: u32 = 2;
    while (i <= n) : (i += 1) {
        result *= i;
    }
    return result;
}

/// Factorial as f64 (supports larger values)
pub fn factorialF(n: u32) f64 {
    var result: f64 = 1.0;
    var i: u32 = 2;
    while (i <= n) : (i += 1) {
        result *= @as(f64, @floatFromInt(i));
    }
    return result;
}

/// Fibonacci number (iterative)
pub fn fibonacci(n: u32) u64 {
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    var a: u64 = 0;
    var b: u64 = 1;
    var i: u32 = 2;
    while (i <= n) : (i += 1) {
        const temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

/// Binomial coefficient (n choose k)
pub fn binomial(n: u32, k: u32) u64 {
    if (k > n) return 0;
    if (k == 0 or k == n) return 1;
    if (k > n - k) return binomial(n, n - k);
    
    var result: u64 = 1;
    var i: u32 = 0;
    while (i < k) : (i += 1) {
        result = result * @as(u64, n - i) / @as(u64, i + 1);
    }
    return result;
}

/// Check if value is even
pub fn isEven(n: i64) bool {
    return @rem(n, 2) == 0;
}

/// Check if value is odd
pub fn isOdd(n: i64) bool {
    return @rem(n, 2) != 0;
}

/// Modulo that always returns positive result
pub fn modPositive(a: i64, b: u64) u64 {
    const result = @as(u64, @mod(a, @as(i64, @intCast(b))));
    return result;
}

// ============================================================================
// Statistics
// ============================================================================

/// Calculate mean (average)
pub fn mean(values: []const f64) f64 {
    if (values.len == 0) return 0.0;
    var total: f64 = 0.0;
    for (values) |v| {
        total += v;
    }
    return total / @as(f64, @floatFromInt(values.len));
}

/// Calculate median
pub fn median(allocator: std.mem.Allocator, values: []const f64) !f64 {
    if (values.len == 0) return 0.0;
    
    const sorted = try allocator.dupe(f64, values);
    defer allocator.free(sorted);
    
    std.mem.sort(f64, sorted, {}, comptime std.sort.asc(f64));
    
    if (sorted.len % 2 == 0) {
        return (sorted[sorted.len / 2 - 1] + sorted[sorted.len / 2]) / 2.0;
    }
    return sorted[sorted.len / 2];
}

/// Calculate variance (population)
pub fn variance(values: []const f64) f64 {
    if (values.len == 0) return 0.0;
    const m = mean(values);
    var sum_sq: f64 = 0.0;
    for (values) |v| {
        const diff = v - m;
        sum_sq += diff * diff;
    }
    return sum_sq / @as(f64, @floatFromInt(values.len));
}

/// Calculate standard deviation (population)
pub fn stdDev(values: []const f64) f64 {
    return sqrt(variance(values));
}

/// Calculate sample variance (n-1 denominator)
pub fn sampleVariance(values: []const f64) f64 {
    if (values.len <= 1) return 0.0;
    const m = mean(values);
    var sum_sq: f64 = 0.0;
    for (values) |v| {
        const diff = v - m;
        sum_sq += diff * diff;
    }
    return sum_sq / @as(f64, @floatFromInt(values.len - 1));
}

/// Calculate sample standard deviation
pub fn sampleStdDev(values: []const f64) f64 {
    return sqrt(sampleVariance(values));
}

/// Find minimum value
pub fn minVal(values: []const f64) f64 {
    if (values.len == 0) return 0.0;
    var result = values[0];
    for (values[1..]) |v| {
        if (v < result) result = v;
    }
    return result;
}

/// Find maximum value
pub fn maxVal(values: []const f64) f64 {
    if (values.len == 0) return 0.0;
    var result = values[0];
    for (values[1..]) |v| {
        if (v > result) result = v;
    }
    return result;
}

/// Calculate sum
pub fn sum(values: []const f64) f64 {
    var result: f64 = 0.0;
    for (values) |v| {
        result += v;
    }
    return result;
}

/// Calculate range (max - min)
pub fn range(values: []const f64) f64 {
    return maxVal(values) - minVal(values);
}

// ============================================================================
// Interpolation
// ============================================================================

/// Linear interpolation between a and b
pub fn lerp(a: f64, b: f64, t: f64) f64 {
    return a + (b - a) * t;
}

/// Inverse linear interpolation (find t for value between a and b)
pub fn inverseLerp(a: f64, b: f64, value: f64) f64 {
    if (approxEquals(a, b, EPSILON)) return 0.0;
    return (value - a) / (b - a);
}

/// Remap value from one range to another
pub fn remap(value: f64, in_min: f64, in_max: f64, out_min: f64, out_max: f64) f64 {
    const t = inverseLerp(in_min, in_max, value);
    return lerp(out_min, out_max, t);
}

/// Smooth step interpolation
pub fn smoothstep(edge0: f64, edge1: f64, x: f64) f64 {
    const t = clamp(f64, (x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

/// Smoother step interpolation
pub fn smootherstep(edge0: f64, edge1: f64, x: f64) f64 {
    const t = clamp(f64, (x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

/// Step function
pub fn step(edge: f64, x: f64) f64 {
    return if (x < edge) 0.0 else 1.0;
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Calculate percentage
pub fn percentage(part: f64, whole: f64) f64 {
    if (whole == 0) return 0.0;
    return (part / whole) * 100.0;
}

/// Calculate percentage of
pub fn percentOf(percentage_val: f64, whole: f64) f64 {
    return (percentage_val / 100.0) * whole;
}

/// Map a value to a new range (same as remap)
pub const map = remap;

/// Constrain value to wrap around range
pub fn wrap(value: f64, min_val: f64, max_val: f64) f64 {
    const interval = max_val - min_val;
    if (interval == 0) return min_val;
    return min_val + @mod(value - min_val, interval);
}

/// Ping-pong value between min and max
pub fn pingPong(t: f64, length: f64) f64 {
    if (length == 0) return 0.0;
    const l = 2.0 * length;
    var p = @mod(t, l);
    if (p < 0) p += l;
    if (p >= length) p = l - p;
    return p;
}

/// Calculate distance between two 2D points
pub fn distance2D(x1: f64, y1: f64, x2: f64, y2: f64) f64 {
    const dx = x2 - x1;
    const dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}

/// Calculate distance between two 3D points
pub fn distance3D(x1: f64, y1: f64, z1: f64, x2: f64, y2: f64, z2: f64) f64 {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const dz = z2 - z1;
    return sqrt(dx * dx + dy * dy + dz * dz);
}

/// Check if value is between min and max (inclusive)
pub fn between(value: f64, min_val: f64, max_val: f64) bool {
    return value >= min_val and value <= max_val;
}

/// Check if value is between min and max (exclusive)
pub fn betweenExclusive(value: f64, min_val: f64, max_val: f64) bool {
    return value > min_val and value < max_val;
}

/// Inverse square (1/x^2)
pub fn inverseSquare(value: f64) f64 {
    return 1.0 / (value * value);
}

/// Linear to decibel conversion
pub fn linearToDb(linear: f64) f64 {
    if (linear <= 0) return -std.math.inf(f64);
    return 20.0 * log10(linear);
}

/// Decibel to linear conversion
pub fn dbToLinear(db: f64) f64 {
    return pow(10.0, db / 20.0);
}

/// Hermite interpolation
pub fn hermite(t: f64) f64 {
    return t * t * (3.0 - 2.0 * t);
}

/// Quintic interpolation
pub fn quintic(t: f64) f64 {
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

// ============================================================================
// Tests
// ============================================================================

test "abs and absInt" {
    try std.testing.expectEqual(@as(f64, 5.0), abs(-5.0));
    try std.testing.expectEqual(@as(f64, 5.0), abs(5.0));
    try std.testing.expectEqual(@as(i32, 5), absInt(i32, -5));
    try std.testing.expectEqual(@as(i32, 5), absInt(i32, 5));
}

test "min and max" {
    try std.testing.expectEqual(@as(i32, 3), min(i32, 5, 3));
    try std.testing.expectEqual(@as(i32, 5), max(i32, 5, 3));
    try std.testing.expectEqual(@as(f64, 2.5), min(f64, 2.5, 3.7));
    try std.testing.expectEqual(@as(f64, 3.7), max(f64, 2.5, 3.7));
}

test "clamp" {
    try std.testing.expectEqual(@as(i32, 5), clamp(i32, 10, 0, 5));
    try std.testing.expectEqual(@as(i32, 0), clamp(i32, -5, 0, 5));
    try std.testing.expectEqual(@as(i32, 3), clamp(i32, 3, 0, 5));
}

test "sign" {
    try std.testing.expectEqual(@as(f64, 1.0), sign(5.0));
    try std.testing.expectEqual(@as(f64, -1.0), sign(-5.0));
    try std.testing.expectEqual(@as(f64, 0.0), sign(0.0));
}

test "approxEquals" {
    try std.testing.expect(approxEquals(1.0, 1.0000001, 1e-6));
    try std.testing.expect(!approxEquals(1.0, 1.1, 1e-6));
}

test "floor, ceil, round, trunc" {
    try std.testing.expectEqual(@as(f64, 3.0), floor(3.7));
    try std.testing.expectEqual(@as(f64, -4.0), floor(-3.7));
    try std.testing.expectEqual(@as(f64, 4.0), ceil(3.7));
    try std.testing.expectEqual(@as(f64, -3.0), ceil(-3.7));
    try std.testing.expectEqual(@as(f64, 4.0), round(3.7));
    try std.testing.expectEqual(@as(f64, 3.0), round(3.3));
    try std.testing.expectEqual(@as(f64, 3.0), trunc(3.7));
    try std.testing.expectEqual(@as(f64, -3.0), trunc(-3.7));
}

test "roundTo" {
    try std.testing.expect(approxEquals(3.14, roundTo(3.14159, 2), 0.001));
    try std.testing.expect(approxEquals(3.142, roundTo(3.14159, 3), 0.0001));
}

test "pow and sqrt" {
    try std.testing.expect(approxEquals(8.0, pow(2.0, 3.0), EPSILON));
    try std.testing.expect(approxEquals(2.0, sqrt(4.0), EPSILON));
    try std.testing.expect(approxEquals(3.0, sqrt(9.0), EPSILON));
}

test "powInt" {
    try std.testing.expectEqual(@as(i64, 8), powInt(2, 3));
    try std.testing.expectEqual(@as(i64, 1), powInt(5, 0));
    try std.testing.expectEqual(@as(i64, 100), powInt(10, 2));
}

test "degToRad and radToDeg" {
    try std.testing.expect(approxEquals(PI / 4.0, degToRad(45.0), EPSILON));
    try std.testing.expect(approxEquals(180.0, radToDeg(PI), EPSILON));
}

test "sin, cos, tan" {
    try std.testing.expect(approxEquals(0.0, sin(0.0), 1e-6));
    try std.testing.expect(approxEquals(1.0, sin(PI / 2.0), 1e-6));
    try std.testing.expect(approxEquals(1.0, cos(0.0), 1e-6));
    try std.testing.expect(approxEquals(0.0, cos(PI / 2.0), 1e-6));
}

test "ln and expNatural" {
    try std.testing.expect(approxEquals(1.0, ln(E), 1e-6));
    try std.testing.expect(approxEquals(E, expNatural(1.0), 1e-6));
}

test "log10 and log2" {
    try std.testing.expect(approxEquals(2.0, log10(100.0), 1e-6));
    try std.testing.expect(approxEquals(3.0, log2(8.0), 1e-6));
}

test "isPrime" {
    try std.testing.expect(isPrime(2));
    try std.testing.expect(isPrime(3));
    try std.testing.expect(isPrime(17));
    try std.testing.expect(!isPrime(4));
    try std.testing.expect(!isPrime(15));
    try std.testing.expect(!isPrime(1));
}

test "gcd and lcm" {
    try std.testing.expectEqual(@as(u64, 6), gcd(12, 18));
    try std.testing.expectEqual(@as(u64, 1), gcd(7, 11));
    try std.testing.expectEqual(@as(u64, 36), lcm(12, 18));
    try std.testing.expectEqual(@as(u64, 77), lcm(7, 11));
}

test "factorial" {
    try std.testing.expectEqual(@as(u64, 1), factorial(0));
    try std.testing.expectEqual(@as(u64, 1), factorial(1));
    try std.testing.expectEqual(@as(u64, 6), factorial(3));
    try std.testing.expectEqual(@as(u64, 120), factorial(5));
    try std.testing.expectEqual(@as(u64, 3628800), factorial(10));
}

test "fibonacci" {
    try std.testing.expectEqual(@as(u64, 0), fibonacci(0));
    try std.testing.expectEqual(@as(u64, 1), fibonacci(1));
    try std.testing.expectEqual(@as(u64, 1), fibonacci(2));
    try std.testing.expectEqual(@as(u64, 2), fibonacci(3));
    try std.testing.expectEqual(@as(u64, 5), fibonacci(5));
    try std.testing.expectEqual(@as(u64, 55), fibonacci(10));
}

test "binomial" {
    try std.testing.expectEqual(@as(u64, 1), binomial(5, 0));
    try std.testing.expectEqual(@as(u64, 5), binomial(5, 1));
    try std.testing.expectEqual(@as(u64, 10), binomial(5, 2));
    try std.testing.expectEqual(@as(u64, 10), binomial(5, 3));
    try std.testing.expectEqual(@as(u64, 1), binomial(5, 5));
}

test "isEven and isOdd" {
    try std.testing.expect(isEven(4));
    try std.testing.expect(!isEven(7));
    try std.testing.expect(isOdd(7));
    try std.testing.expect(!isOdd(4));
}

test "mean" {
    const values = [_]f64{ 1.0, 2.0, 3.0, 4.0, 5.0 };
    try std.testing.expect(approxEquals(3.0, mean(&values), EPSILON));
}

test "median" {
    const allocator = std.testing.allocator;
    const values1 = [_]f64{ 1.0, 2.0, 3.0 };
    try std.testing.expect(approxEquals(2.0, try median(allocator, &values1), EPSILON));
    
    const values2 = [_]f64{ 1.0, 2.0, 3.0, 4.0 };
    try std.testing.expect(approxEquals(2.5, try median(allocator, &values2), EPSILON));
}

test "variance and stdDev" {
    const values = [_]f64{ 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0 };
    try std.testing.expect(approxEquals(4.0, variance(&values), 0.01));
    try std.testing.expect(approxEquals(2.0, stdDev(&values), 0.01));
}

test "sum, minVal, maxVal, range" {
    const values = [_]f64{ 3.0, 1.0, 4.0, 1.0, 5.0 };
    try std.testing.expect(approxEquals(14.0, sum(&values), EPSILON));
    try std.testing.expect(approxEquals(1.0, minVal(&values), EPSILON));
    try std.testing.expect(approxEquals(5.0, maxVal(&values), EPSILON));
    try std.testing.expect(approxEquals(4.0, range(&values), EPSILON));
}

test "lerp" {
    try std.testing.expect(approxEquals(5.0, lerp(0.0, 10.0, 0.5), EPSILON));
    try std.testing.expect(approxEquals(0.0, lerp(0.0, 10.0, 0.0), EPSILON));
    try std.testing.expect(approxEquals(10.0, lerp(0.0, 10.0, 1.0), EPSILON));
}

test "inverseLerp" {
    try std.testing.expect(approxEquals(0.5, inverseLerp(0.0, 10.0, 5.0), EPSILON));
    try std.testing.expect(approxEquals(0.0, inverseLerp(0.0, 10.0, 0.0), EPSILON));
    try std.testing.expect(approxEquals(1.0, inverseLerp(0.0, 10.0, 10.0), EPSILON));
}

test "remap" {
    try std.testing.expect(approxEquals(50.0, remap(5.0, 0.0, 10.0, 0.0, 100.0), EPSILON));
    try std.testing.expect(approxEquals(75.0, remap(7.5, 0.0, 10.0, 0.0, 100.0), EPSILON));
}

test "smoothstep" {
    try std.testing.expect(approxEquals(0.0, smoothstep(0.0, 1.0, 0.0), EPSILON));
    try std.testing.expect(approxEquals(1.0, smoothstep(0.0, 1.0, 1.0), EPSILON));
    try std.testing.expect(approxEquals(0.5, smoothstep(0.0, 1.0, 0.5), EPSILON));
}

test "percentage and percentOf" {
    try std.testing.expect(approxEquals(50.0, percentage(25.0, 50.0), EPSILON));
    try std.testing.expect(approxEquals(25.0, percentOf(50.0, 50.0), EPSILON));
}

test "wrap" {
    try std.testing.expect(approxEquals(2.0, wrap(5.0, 0.0, 3.0), EPSILON));
    try std.testing.expect(approxEquals(2.0, wrap(8.0, 0.0, 3.0), EPSILON));
    try std.testing.expect(approxEquals(0.5, wrap(6.5, 0.0, 3.0), EPSILON));
}

test "pingPong" {
    try std.testing.expect(approxEquals(1.0, pingPong(1.0, 3.0), EPSILON));
    try std.testing.expect(approxEquals(2.0, pingPong(4.0, 3.0), EPSILON));
}

test "distance2D and distance3D" {
    try std.testing.expect(approxEquals(5.0, distance2D(0.0, 0.0, 3.0, 4.0), EPSILON));
    try std.testing.expect(approxEquals(sqrt(29.0), distance3D(0.0, 0.0, 0.0, 2.0, 3.0, 4.0), EPSILON));
}

test "between" {
    try std.testing.expect(between(5.0, 1.0, 10.0));
    try std.testing.expect(between(1.0, 1.0, 10.0));
    try std.testing.expect(!betweenExclusive(1.0, 1.0, 10.0));
    try std.testing.expect(betweenExclusive(5.0, 1.0, 10.0));
}

test "isPerfectSquare" {
    try std.testing.expect(isPerfectSquare(4));
    try std.testing.expect(isPerfectSquare(9));
    try std.testing.expect(isPerfectSquare(16));
    try std.testing.expect(!isPerfectSquare(5));
    try std.testing.expect(!isPerfectSquare(10));
}

test "linearToDb and dbToLinear" {
    try std.testing.expect(approxEquals(-20.0, linearToDb(0.1), 0.01));
    try std.testing.expect(approxEquals(0.1, dbToLinear(-20.0), 0.001));
}

test "hermite and quintic" {
    try std.testing.expect(approxEquals(0.0, hermite(0.0), EPSILON));
    try std.testing.expect(approxEquals(1.0, hermite(1.0), EPSILON));
    try std.testing.expect(approxEquals(0.5, hermite(0.5), EPSILON));
}

test "cbrt" {
    try std.testing.expect(approxEquals(2.0, cbrt(8.0), 1e-6));
    try std.testing.expect(approxEquals(3.0, cbrt(27.0), 1e-6));
    try std.testing.expect(approxEquals(-2.0, cbrt(-8.0), 1e-6));
}

test "arctan and arctan2" {
    try std.testing.expect(approxEquals(PI / 4.0, arctan(1.0), 1e-5));
    try std.testing.expect(approxEquals(PI / 4.0, arctan2(1.0, 1.0), 1e-5));
    try std.testing.expect(approxEquals(-PI / 4.0, arctan2(-1.0, 1.0), 1e-5));
}

test "sampleVariance" {
    const values = [_]f64{ 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0 };
    try std.testing.expect(approxEquals(32.0 / 7.0, sampleVariance(&values), 0.01));
}