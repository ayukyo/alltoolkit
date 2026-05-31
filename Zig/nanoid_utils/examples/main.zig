const std = @import("std");
const nanoid = @import("nanoid_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Initialize RNG
    var rng = std.rand.Xoshiro256.init(12345);
    
    // Create generator with default settings (21 chars, URL-safe alphabet)
    var generator = try nanoid.NanoidGenerator(@TypeOf(rng)).init(allocator, &rng, .{});
    defer generator.deinit();
    
    // Generate default ID
    const id = try generator.generate();
    defer allocator.free(id);
    std.debug.print("Default ID (21 chars): {s}\n", .{id});
    
    // Generate with custom length
    rng = std.rand.Xoshiro256.init(67890);
    generator = try nanoid.NanoidGenerator(@TypeOf(rng)).init(allocator, &rng, .{
        .length = 10,
    });
    defer generator.deinit();
    const short_id = try generator.generate();
    defer allocator.free(short_id);
    std.debug.print("Short ID (10 chars): {s}\n", .{short_id});
    
    // Generate with custom alphabet (binary)
    rng = std.rand.Xoshiro256.init(11111);
    generator = try nanoid.NanoidGenerator(@TypeOf(rng)).init(allocator, &rng, .{
        .alphabet = "01",
        .length = 32,
    });
    defer generator.deinit();
    const binary_id = try generator.generate();
    defer allocator.free(binary_id);
    std.debug.print("Binary ID (32 bits): {s}\n", .{binary_id});
    
    // Use helper function
    rng = std.rand.Xoshiro256.init(99999);
    const easy_id = try nanoid.generateDefaultNanoid(allocator, &rng, 16);
    defer allocator.free(easy_id);
    std.debug.print("Easy helper ID: {s}\n", .{easy_id});
}