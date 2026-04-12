const std = @import("std");
const hash = @import("hash-utils");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Hash Utils - Basic Examples ===\n\n", .{});

    // MD5 Examples
    try stdout.print("--- MD5 ---\n", .{});
    const md5_result = try hash.Md5.hashHex(allocator, "Hello, World!");
    defer allocator.free(md5_result);
    try stdout.print("MD5('Hello, World!') = {s}\n", .{md5_result});

    // SHA-1 Examples
    try stdout.print("\n--- SHA-1 ---\n", .{});
    const sha1_result = try hash.Sha1.hashHex(allocator, "Hello, World!");
    defer allocator.free(sha1_result);
    try stdout.print("SHA1('Hello, World!') = {s}\n", .{sha1_result});

    // SHA-256 Examples
    try stdout.print("\n--- SHA-256 ---\n", .{});
    const sha256_result = try hash.Sha256.hashHex(allocator, "Hello, World!");
    defer allocator.free(sha256_result);
    try stdout.print("SHA256('Hello, World!') = {s}\n", .{sha256_result});

    // SHA-512 Examples
    try stdout.print("\n--- SHA-512 ---\n", .{});
    const sha512_result = try hash.Sha512.hashHex(allocator, "Hello, World!");
    defer allocator.free(sha512_result);
    try stdout.print("SHA512('Hello, World!') = {s}\n", .{sha512_result});

    // Generic hashWith function
    try stdout.print("\n--- Generic hashWith ---\n", .{});
    inline for (.{
        .{ hash.HashAlgorithm.md5, "MD5" },
        .{ hash.HashAlgorithm.sha1, "SHA-1" },
        .{ hash.HashAlgorithm.sha256, "SHA-256" },
        .{ hash.HashAlgorithm.sha512, "SHA-512" },
    }) |item| {
        const algo = item[0];
        const name = item[1];
        const result = try hash.hashWith(allocator, "test data", algo);
        defer allocator.free(result);
        try stdout.print("{s}('test data') = {s}\n", .{ name, result });
    }

    try stdout.print("\n", .{});
}