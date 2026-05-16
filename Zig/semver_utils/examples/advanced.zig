const std = @import("std");
const semver = @import("semver_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();

    try stdout.print("=== SemVer Utils Advanced Examples ===\n\n", .{});

    // Version constraints - caret
    try stdout.print("1. Caret Constraints (^):\n", .{});
    try stdout.print("   ^1.2.3 means >=1.2.3 <2.0.0\n", .{});
    
    var caret_constraint = try semver.VersionConstraint.parse(allocator, "^1.2.3");
    defer caret_constraint.deinit();

    const caret_versions = [_][]const u8{
        "1.2.3",
        "1.2.4",
        "1.3.0",
        "1.9.9",
        "2.0.0",
        "0.9.0",
        "1.2.2",
    };

    for (caret_versions) |v| {
        var ver = try semver.SemVer.parse(allocator, v);
        defer ver.deinit();
        const satisfies = ver.satisfies(caret_constraint);
        const status: []const u8 = if (satisfies) "satisfies" else "does NOT satisfy";
        try stdout.print("   {s}: {s}\n", .{ v, status });
    }

    // Version constraints - tilde
    try stdout.print("\n2. Tilde Constraints (~):\n", .{});
    try stdout.print("   ~1.2.3 means >=1.2.3 <1.3.0\n", .{});
    
    var tilde_constraint = try semver.VersionConstraint.parse(allocator, "~1.2.3");
    defer tilde_constraint.deinit();

    const tilde_versions = [_][]const u8{
        "1.2.3",
        "1.2.4",
        "1.2.9",
        "1.3.0",
        "1.1.9",
    };

    for (tilde_versions) |v| {
        var ver = try semver.SemVer.parse(allocator, v);
        defer ver.deinit();
        const satisfies = ver.satisfies(tilde_constraint);
        const status: []const u8 = if (satisfies) "satisfies" else "does NOT satisfy";
        try stdout.print("   {s}: {s}\n", .{ v, status });
    }

    // Comparison operators
    try stdout.print("\n3. Comparison Operators:\n", .{});

    const operators = [_]struct { op: []const u8, version: []const u8 }{
        .{ .op = ">=", .version = "1.0.0" },
        .{ .op = "<", .version = "2.0.0" },
        .{ .op = "=", .version = "1.5.0" },
    };

    const test_vs = [_][]const u8{ "0.9.0", "1.0.0", "1.5.0", "1.9.0", "2.0.0" };

    for (operators) |op_spec| {
        const constraint_str = try std.fmt.allocPrint(allocator, "{s}{s}", .{ op_spec.op, op_spec.version });
        defer allocator.free(constraint_str);
        
        var constraint = try semver.VersionConstraint.parse(allocator, constraint_str);
        defer constraint.deinit();

        try stdout.print("   {s}:\n", .{constraint_str});
        for (test_vs) |v| {
            var ver = try semver.SemVer.parse(allocator, v);
            defer ver.deinit();
            const satisfies = ver.satisfies(constraint);
            const status: []const u8 = if (satisfies) "yes" else "no";
            try stdout.print("     {s}: {s}\n", .{ v, status });
        }
    }

    // Complex prerelease comparison
    try stdout.print("\n4. Prerelease Version Ordering:\n", .{});
    try stdout.print("   1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0 < 1.0.1\n", .{});

    const pre_versions = [_][]const u8{
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-alpha.beta",
        "1.0.0-beta",
        "1.0.0-beta.2",
        "1.0.0",
        "1.0.1",
    };

    try stdout.print("   Verification:\n", .{});
    for (0..pre_versions.len - 1) |i| {
        const cmp = try semver.compare(allocator, pre_versions[i], pre_versions[i + 1]);
        const valid = cmp < 0;
        const status: []const u8 = if (valid) "correct" else "ERROR";
        try stdout.print("     {s} < {s}: {s}\n", .{ pre_versions[i], pre_versions[i + 1], status });
    }

    // Practical use case: package version selection
    try stdout.print("\n5. Practical Use Case: Selecting Compatible Package\n", .{});
    
    var package_constraint = try semver.VersionConstraint.parse(allocator, "^1.4.0");
    defer package_constraint.deinit();

    const available_packages = [_][]const u8{
        "1.3.0",   // Too old
        "1.4.0",   // Exact match
        "1.4.5",   // Compatible
        "1.5.0",   // Compatible
        "1.9.9",   // Compatible
        "2.0.0",   // Breaking change
        "2.0.0-alpha", // Prerelease of next major
    };

    try stdout.print("   Constraint: ^1.4.0\n", .{});
    try stdout.print("   Available packages:\n", .{});

    var best_version: ?[]const u8 = null;
    for (available_packages) |pkg| {
        var ver = try semver.SemVer.parse(allocator, pkg);
        defer ver.deinit();
        const compatible = ver.satisfies(package_constraint);
        const status: []const u8 = if (compatible) "COMPATIBLE" else "incompatible";
        try stdout.print("     {s}: {s}\n", .{ pkg, status });
        
        if (compatible) {
            if (best_version) |best| {
                if ((try semver.compare(allocator, pkg, best)) > 0) {
                    best_version = pkg;
                }
            } else {
                best_version = pkg;
            }
        }
    }

    if (best_version) |best| {
        try stdout.print("   Best compatible version: {s}\n", .{best});
    }

    // Edge cases
    try stdout.print("\n6. Edge Cases:\n", .{});

    // Version 0.x handling
    try stdout.print("   Caret constraint ^0.5.0:\n", .{});
    var zero_constraint = try semver.VersionConstraint.parse(allocator, "^0.5.0");
    defer zero_constraint.deinit();

    const zero_versions = [_][]const u8{ "0.4.9", "0.5.0", "0.5.9", "0.6.0", "1.0.0" };
    for (zero_versions) |v| {
        var ver = try semver.SemVer.parse(allocator, v);
        defer ver.deinit();
        const satisfies = ver.satisfies(zero_constraint);
        const status: []const u8 = if (satisfies) "satisfies" else "does NOT satisfy";
        try stdout.print("     {s}: {s}\n", .{ v, status });
    }

    try stdout.print("\n=== Done ===\n", .{});
}