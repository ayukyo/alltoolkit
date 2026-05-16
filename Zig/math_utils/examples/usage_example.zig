const std = @import("std");
const math_utils = @import("math_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("\n=== Math Utils Demo ===\n\n", .{});

    // Basic Operations
    std.debug.print("=== Basic Operations ===\n", .{});
    std.debug.print("abs(-5) = {}\n", .{math_utils.abs(-5.0)});
    std.debug.print("min(5, 3) = {}\n", .{math_utils.min(i32, 5, 3)});
    std.debug.print("max(5, 3) = {}\n", .{math_utils.max(i32, 5, 3)});
    std.debug.print("clamp(10, 0, 5) = {}\n", .{math_utils.clamp(i32, 10, 0, 5)});
    std.debug.print("sign(-7) = {}\n", .{math_utils.sign(-7.0)});
    std.debug.print("\n", .{});

    // Rounding
    std.debug.print("=== Rounding ===\n", .{});
    std.debug.print("floor(3.7) = {}\n", .{math_utils.floor(3.7)});
    std.debug.print("ceil(3.2) = {}\n", .{math_utils.ceil(3.2)});
    std.debug.print("round(3.5) = {}\n", .{math_utils.round(3.5)});
    std.debug.print("trunc(-3.7) = {}\n", .{math_utils.trunc(-3.7)});
    std.debug.print("roundTo(3.14159, 2) = {}\n", .{math_utils.roundTo(3.14159, 2)});
    std.debug.print("\n", .{});

    // Constants
    std.debug.print("=== Constants ===\n", .{});
    std.debug.print("PI = {}\n", .{math_utils.PI});
    std.debug.print("E = {}\n", .{math_utils.E});
    std.debug.print("PHI (Golden ratio) = {}\n", .{math_utils.PHI});
    std.debug.print("SQRT2 = {}\n", .{math_utils.SQRT2});
    std.debug.print("\n", .{});

    // Power and Roots
    std.debug.print("=== Power and Roots ===\n", .{});
    std.debug.print("pow(2, 8) = {}\n", .{math_utils.pow(2.0, 8.0)});
    std.debug.print("sqrt(64) = {}\n", .{math_utils.sqrt(64.0)});
    std.debug.print("cbrt(27) = {}\n", .{math_utils.cbrt(27.0)});
    std.debug.print("nthRoot(256, 4) = {}\n", .{math_utils.nthRoot(256.0, 4)});
    std.debug.print("isPerfectSquare(144) = {}\n", .{math_utils.isPerfectSquare(144)});
    std.debug.print("powInt(3, 4) = {}\n", .{math_utils.powInt(3, 4)});
    std.debug.print("\n", .{});

    // Trigonometry
    std.debug.print("=== Trigonometry ===\n", .{});
    std.debug.print("degToRad(45) = {}\n", .{math_utils.degToRad(45.0)});
    std.debug.print("radToDeg(PI) = {}\n", .{math_utils.radToDeg(math_utils.PI)});
    std.debug.print("sin(PI/2) = {}\n", .{math_utils.sin(math_utils.PI / 2.0)});
    std.debug.print("cos(0) = {}\n", .{math_utils.cos(0.0)});
    std.debug.print("tan(PI/4) = {}\n", .{math_utils.tan(math_utils.PI / 4.0)});
    std.debug.print("\n", .{});

    // Logarithms
    std.debug.print("=== Logarithms ===\n", .{});
    std.debug.print("ln(E) = {}\n", .{math_utils.ln(math_utils.E)});
    std.debug.print("log10(1000) = {}\n", .{math_utils.log10(1000.0)});
    std.debug.print("log2(8) = {}\n", .{math_utils.log2(8.0)});
    std.debug.print("exp(1) = {}\n", .{math_utils.expNatural(1.0)});
    std.debug.print("log(2, 8) = {}\n", .{math_utils.log(2.0, 8.0)});
    std.debug.print("\n", .{});

    // Number Theory
    std.debug.print("=== Number Theory ===\n", .{});
    std.debug.print("isPrime(17) = {}\n", .{math_utils.isPrime(17)});
    std.debug.print("isPrime(18) = {}\n", .{math_utils.isPrime(18)});
    std.debug.print("gcd(48, 18) = {}\n", .{math_utils.gcd(48, 18)});
    std.debug.print("lcm(4, 6) = {}\n", .{math_utils.lcm(4, 6)});
    std.debug.print("factorial(7) = {}\n", .{math_utils.factorial(7)});
    std.debug.print("fibonacci(15) = {}\n", .{math_utils.fibonacci(15)});
    std.debug.print("binomial(5, 2) = {}\n", .{math_utils.binomial(5, 2)});
    std.debug.print("isEven(6) = {}\n", .{math_utils.isEven(6)});
    std.debug.print("isOdd(7) = {}\n", .{math_utils.isOdd(7)});
    std.debug.print("\n", .{});

    // Statistics
    std.debug.print("=== Statistics ===\n", .{});
    const data = [_]f64{ 10.0, 20.0, 30.0, 40.0, 50.0 };
    std.debug.print("data: {any}\n", .{&data});
    std.debug.print("mean = {}\n", .{math_utils.mean(&data)});
    std.debug.print("median = {}\n", .{try math_utils.median(allocator, &data)});
    std.debug.print("sum = {}\n", .{math_utils.sum(&data)});
    std.debug.print("min = {}\n", .{math_utils.minVal(&data)});
    std.debug.print("max = {}\n", .{math_utils.maxVal(&data)});
    std.debug.print("range = {}\n", .{math_utils.range(&data)});
    std.debug.print("variance = {}\n", .{math_utils.variance(&data)});
    std.debug.print("stdDev = {}\n", .{math_utils.stdDev(&data)});
    std.debug.print("\n", .{});

    // Interpolation
    std.debug.print("=== Interpolation ===\n", .{});
    std.debug.print("lerp(0, 100, 0.3) = {}\n", .{math_utils.lerp(0.0, 100.0, 0.3)});
    std.debug.print("inverseLerp(0, 100, 30) = {}\n", .{math_utils.inverseLerp(0.0, 100.0, 30.0)});
    std.debug.print("remap(5, 0-10 to 0-100) = {}\n", .{math_utils.remap(5.0, 0.0, 10.0, 0.0, 100.0)});
    std.debug.print("smoothstep(0, 1, 0.5) = {}\n", .{math_utils.smoothstep(0.0, 1.0, 0.5)});
    std.debug.print("hermite(0.5) = {}\n", .{math_utils.hermite(0.5)});
    std.debug.print("quintic(0.5) = {}\n", .{math_utils.quintic(0.5)});
    std.debug.print("\n", .{});

    // Utility Functions
    std.debug.print("=== Utility ===\n", .{});
    std.debug.print("percentage(25, 100) = {}\n", .{math_utils.percentage(25.0, 100.0)});
    std.debug.print("percentOf(25%, 200) = {}\n", .{math_utils.percentOf(25.0, 200.0)});
    std.debug.print("wrap(7, 0, 3) = {}\n", .{math_utils.wrap(7.0, 0.0, 3.0)});
    std.debug.print("pingPong(4, 3) = {}\n", .{math_utils.pingPong(4.0, 3.0)});
    std.debug.print("distance2D(0,0 to 3,4) = {}\n", .{math_utils.distance2D(0.0, 0.0, 3.0, 4.0)});
    std.debug.print("distance3D(0,0,0 to 1,2,2) = {}\n", .{math_utils.distance3D(0.0, 0.0, 0.0, 1.0, 2.0, 2.0)});
    std.debug.print("between(5, 1, 10) = {}\n", .{math_utils.between(5.0, 1.0, 10.0)});
    std.debug.print("linearToDb(0.1) = {} dB\n", .{math_utils.linearToDb(0.1)});
    std.debug.print("dbToLinear(-20) = {}\n", .{math_utils.dbToLinear(-20.0)});
    std.debug.print("inverseSquare(2) = {}\n", .{math_utils.inverseSquare(2.0)});
    std.debug.print("\n", .{});

    std.debug.print("=== Demo Complete ===\n", .{});
}