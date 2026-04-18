const std = @import("std");
const number_utils = @import("number_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    std.debug.print("\n=== Number Utils Demo ===\n\n", .{});
    
    // Parsing
    std.debug.print("--- Parsing ---\n", .{});
    std.debug.print("parseU64(\"12345\", 10) = {}\n", .{try number_utils.parseU64("12345", 10)});
    std.debug.print("parseI64(\"-42\", 10) = {}\n", .{try number_utils.parseI64("-42", 10)});
    std.debug.print("parseU64(\"FF\", 16) = {}\n", .{try number_utils.parseU64("FF", 16)});
    std.debug.print("parseU64(\"11111111\", 2) = {}\n", .{try number_utils.parseU64("11111111", 2)});
    std.debug.print("parseFloat64(\"3.14159\") = {d:.5}\n", .{try number_utils.parseFloat64("3.14159")});
    
    // Formatting
    std.debug.print("\n--- Formatting ---\n", .{});
    const sep1 = try number_utils.formatU64WithSeparator(allocator, 1234567, ",");
    defer allocator.free(sep1);
    std.debug.print("formatU64WithSeparator(1234567) = {s}\n", .{sep1});
    
    const sep2 = try number_utils.formatI64WithSeparator(allocator, -9876543210, ",");
    defer allocator.free(sep2);
    std.debug.print("formatI64WithSeparator(-9876543210) = {s}\n", .{sep2});
    
    const float1 = try number_utils.formatFloat64(allocator, 3.14159, 2);
    defer allocator.free(float1);
    std.debug.print("formatFloat64(3.14159, precision=2) = {s}\n", .{float1});
    
    const hex1 = try number_utils.formatHex(allocator, 0xDEAD, true);
    defer allocator.free(hex1);
    std.debug.print("formatHex(0xDEAD, uppercase=true) = {s}\n", .{hex1});
    
    const bin1 = try number_utils.formatBinary(allocator, 0b10101010);
    defer allocator.free(bin1);
    std.debug.print("formatBinary(0b10101010) = {s}\n", .{bin1});
    
    const oct1 = try number_utils.formatOctal(allocator, 255);
    defer allocator.free(oct1);
    std.debug.print("formatOctal(255) = {s}\n", .{oct1});
    
    // Range operations
    std.debug.print("\n--- Range Operations ---\n", .{});
    std.debug.print("clampI64(3, 5, 10) = {}\n", .{number_utils.clampI64(3, 5, 10)});
    std.debug.print("clampI64(15, 5, 10) = {}\n", .{number_utils.clampI64(15, 5, 10)});
    std.debug.print("inRangeI64(7, 5, 10) = {}\n", .{number_utils.inRangeI64(7, 5, 10)});
    std.debug.print("lerp(0, 10, 0.5) = {d}\n", .{number_utils.lerp(0, 10, 0.5)});
    std.debug.print("mapRange(5, 0..10 -> 0..100) = {d}\n", .{number_utils.mapRange(5, 0, 10, 0, 100)});
    
    // Number utilities
    std.debug.print("\n--- Number Utilities ---\n", .{});
    std.debug.print("isEven(4) = {}\n", .{number_utils.isEven(4)});
    std.debug.print("isOdd(5) = {}\n", .{number_utils.isOdd(5)});
    std.debug.print("isPowerOfTwo(8) = {}\n", .{number_utils.isPowerOfTwo(8)});
    std.debug.print("nextPowerOfTwo(5) = {}\n", .{number_utils.nextPowerOfTwo(5)});
    std.debug.print("popcount(0b10101010) = {}\n", .{number_utils.popcount(0b10101010)});
    std.debug.print("digitCountU64(12345) = {}\n", .{number_utils.digitCountU64(12345)});
    std.debug.print("digitAtU64(12345, position=0) = {?}\n", .{number_utils.digitAtU64(12345, 0)});
    
    // Random
    std.debug.print("\n--- Random ---\n", .{});
    var rng = number_utils.SimpleRandom.init(42);
    std.debug.print("Random values with seed 42: {}, {}, {}\n", .{rng.next(), rng.next(), rng.next()});
    
    rng = number_utils.SimpleRandom.init(42);
    std.debug.print("Random int in range 0..10: {}\n", .{rng.nextI64(0, 10)});
    std.debug.print("Random float: {d:.6}\n", .{rng.nextFloat64()});
    
    var arr = [_]i64{ 1, 2, 3, 4, 5 };
    rng.shuffle(i64, &arr);
    std.debug.print("Shuffled array: {any}\n", .{arr});
    
    // Math
    std.debug.print("\n--- Math ---\n", .{});
    std.debug.print("gcd(12, 18) = {}\n", .{number_utils.gcd(12, 18)});
    std.debug.print("lcm(12, 18) = {}\n", .{number_utils.lcm(12, 18)});
    std.debug.print("factorial(5) = {?}\n", .{number_utils.factorial(5)});
    std.debug.print("fibonacci(10) = {}\n", .{number_utils.fibonacci(10)});
    std.debug.print("isPrime(97) = {}\n", .{number_utils.isPrime(97)});
    std.debug.print("isqrt(100) = {}\n", .{number_utils.isqrt(100)});
    std.debug.print("sumOfDigits(12345) = {}\n", .{number_utils.sumOfDigits(12345)});
    std.debug.print("productOfDigits(12345) = {}\n", .{number_utils.productOfDigits(12345)});
    std.debug.print("reverseDigits(12345) = {}\n", .{number_utils.reverseDigits(12345)});
    
    std.debug.print("\n=== Demo Complete ===\n", .{});
}