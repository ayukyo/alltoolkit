const std = @import("std");
const semver = @import("semver_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();

    try stdout.print("=== SemVer Utils Basic Examples ===\n\n", .{});

    // Parse versions
    try stdout.print("1. Parsing Versions:\n", .{});
    
    const versions = [_][]const u8{
        "1.0.0",
        "2.1.3",
        "0.1.0",
        "1.0.0-alpha",
        "1.0.0-beta.2",
        "2.0.0+build.123",
        "1.2.3-alpha.1+exp.sha.5114f85",
    };

    for (versions) |v| {
        var ver = try semver.SemVer.parse(allocator, v);
        defer ver.deinit();
        const formatted = try ver.format(allocator);
        defer allocator.free(formatted);
        try stdout.print("  {s} -> major={}, minor={}, patch={}", .{ v, ver.major, ver.minor, ver.patch });
        if (ver.prerelease) |pre| {
            try stdout.print(" (pre: {s})", .{pre});
        }
        if (ver.build_metadata) |build| {
            try stdout.print(" (build: {s})", .{build});
        }
        try stdout.print("\n", .{});
    }

    // Compare versions
    try stdout.print("\n2. Comparing Versions:\n", .{});
    
    const comparisons = [_]struct { []const u8, []const u8 }{
        .{ "1.0.0", "2.0.0" },
        .{ "2.1.0", "2.0.0" },
        .{ "1.0.0", "1.0.0" },
        .{ "1.0.0-alpha", "1.0.0" },
        .{ "1.0.0-alpha.1", "1.0.0-alpha.2" },
    };

    for (comparisons) |pair| {
        const result = try semver.compare(allocator, pair[0], pair[1]);
        const symbol: []const u8 = if (result < 0) "<" else if (result > 0) ">" else "=";
        try stdout.print("  {s} {s} {s}\n", .{ pair[0], symbol, pair[1] });
    }

    // Increment versions
    try stdout.print("\n3. Incrementing Versions:\n", .{});
    
    var base_ver = try semver.SemVer.parse(allocator, "1.2.3");
    defer base_ver.deinit();

    var major_inc = try semver.increment(allocator, base_ver, .major);
    defer major_inc.deinit();
    var minor_inc = try semver.increment(allocator, base_ver, .minor);
    defer minor_inc.deinit();
    var patch_inc = try semver.increment(allocator, base_ver, .patch);
    defer patch_inc.deinit();

    try stdout.print("  Base:        1.2.3\n", .{});
    try stdout.print("  Major inc:   {}.{}.{}\n", .{ major_inc.major, major_inc.minor, major_inc.patch });
    try stdout.print("  Minor inc:   {}.{}.{}\n", .{ minor_inc.major, minor_inc.minor, minor_inc.patch });
    try stdout.print("  Patch inc:   {}.{}.{}\n", .{ patch_inc.major, patch_inc.minor, patch_inc.patch });

    // Find max/min
    try stdout.print("\n4. Finding Max/Min Versions:\n", .{});
    
    const version_list = [_][]const u8{ "1.0.0", "2.0.0", "1.5.0", "0.9.0", "1.9.9" };
    const max_ver = try semver.max(allocator, &version_list);
    const min_ver = try semver.min(allocator, &version_list);
    
    try stdout.print("  Versions:  ", .{});
    for (version_list) |v| {
        try stdout.print("{s} ", .{v});
    }
    try stdout.print("\n  Max: {s}\n  Min: {s}\n", .{ max_ver, min_ver });

    // Validation
    try stdout.print("\n5. Validation:\n", .{});
    
    const test_versions = [_][]const u8{ "1.0.0", "2.3.4-alpha", "invalid", "", "1.2" };
    for (test_versions) |v| {
        const valid = semver.isValid(v);
        const status: []const u8 = if (valid) "valid" else "invalid";
        try stdout.print("  \"{s}\" -> {s}\n", .{ v, status });
    }

    try stdout.print("\n=== Done ===\n", .{});
}