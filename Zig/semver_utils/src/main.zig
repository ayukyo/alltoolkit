const std = @import("std");

/// Semantic version representation
pub const SemVer = struct {
    major: u32,
    minor: u32,
    patch: u32,
    prerelease: ?[]const u8 = null,
    build_metadata: ?[]const u8 = null,
    allocator: std.mem.Allocator,

    /// Parse a semantic version string (e.g., "1.2.3", "1.0.0-alpha.1", "2.0.0+build.123")
    pub fn parse(allocator: std.mem.Allocator, version_str: []const u8) !SemVer {
        var result = SemVer{
            .major = 0,
            .minor = 0,
            .patch = 0,
            .allocator = allocator,
        };

        var remaining = std.mem.trim(u8, version_str, " \t\n\r");
        if (remaining.len == 0) return error.EmptyVersion;

        // Handle build metadata (after +)
        var version_part = remaining;
        if (std.mem.indexOf(u8, remaining, "+")) |plus_pos| {
            result.build_metadata = try allocator.dupe(u8, remaining[plus_pos + 1 ..]);
            version_part = remaining[0..plus_pos];
        }

        // Handle prerelease (after -)
        var numeric_part = version_part;
        if (std.mem.indexOf(u8, version_part, "-")) |dash_pos| {
            result.prerelease = try allocator.dupe(u8, version_part[dash_pos + 1 ..]);
            numeric_part = version_part[0..dash_pos];
        }

        // Parse major.minor.patch
        var iter = std.mem.splitScalar(u8, numeric_part, '.');
        
        const major_str = iter.next() orelse return error.InvalidFormat;
        result.major = std.fmt.parseInt(u32, major_str, 10) catch return error.InvalidMajor;

        const minor_str = iter.next() orelse return error.InvalidFormat;
        result.minor = std.fmt.parseInt(u32, minor_str, 10) catch return error.InvalidMinor;

        const patch_str = iter.next() orelse return error.InvalidFormat;
        result.patch = std.fmt.parseInt(u32, patch_str, 10) catch return error.InvalidPatch;

        if (iter.next() != null) return error.TooManyParts;

        return result;
    }

    /// Free allocated memory
    pub fn deinit(self: *SemVer) void {
        if (self.prerelease) |pre| {
            self.allocator.free(pre);
        }
        if (self.build_metadata) |build| {
            self.allocator.free(build);
        }
    }

    /// Format version back to string (caller owns returned memory)
    pub fn format(self: SemVer, allocator: std.mem.Allocator) ![]const u8 {
        var list = std.ArrayList(u8).init(allocator);
        errdefer list.deinit();

        const writer = list.writer();
        try writer.print("{}.{}.{}", .{ self.major, self.minor, self.patch });

        if (self.prerelease) |pre| {
            try writer.print("-{s}", .{pre});
        }

        if (self.build_metadata) |build| {
            try writer.print("+{s}", .{build});
        }

        return list.toOwnedSlice();
    }

    /// Compare two versions
    /// Returns: -1 if self < other, 0 if equal, 1 if self > other
    pub fn compare(self: SemVer, other: SemVer) i8 {
        if (self.major != other.major) {
            return if (self.major < other.major) -1 else 1;
        }
        if (self.minor != other.minor) {
            return if (self.minor < other.minor) -1 else 1;
        }
        if (self.patch != other.patch) {
            return if (self.patch < other.patch) -1 else 1;
        }

        // Prerelease versions have lower precedence
        if (self.prerelease == null and other.prerelease == null) {
            return 0;
        }
        if (self.prerelease == null) {
            return 1; // No prerelease > has prerelease
        }
        if (other.prerelease == null) {
            return -1; // Has prerelease < no prerelease
        }

        // Compare prerelease identifiers
        return comparePrerelease(self.prerelease.?, other.prerelease.?);
    }

    /// Check if this version satisfies a constraint
    pub fn satisfies(self: SemVer, constraint: VersionConstraint) bool {
        return switch (constraint.op) {
            .eq => self.compare(constraint.version) == 0,
            .gt => self.compare(constraint.version) > 0,
            .gte => self.compare(constraint.version) >= 0,
            .lt => self.compare(constraint.version) < 0,
            .lte => self.compare(constraint.version) <= 0,
            .caret => self.satisfiesCaret(constraint.version),
            .tilde => self.satisfiesTilde(constraint.version),
        };
    }

    fn satisfiesCaret(self: SemVer, base: SemVer) bool {
        // ^1.2.3 := >=1.2.3 <2.0.0
        // ^0.2.3 := >=0.2.3 <0.3.0
        // ^0.0.3 := >=0.0.3 <0.0.4
        if (self.major != base.major) return false;
        if (base.major == 0) {
            if (base.minor == 0) {
                return self.minor == base.minor and self.patch == base.patch;
            }
            return self.minor == base.minor and self.patch >= base.patch;
        }
        return self.minor >= base.minor and (self.minor > base.minor or self.patch >= base.patch);
    }

    fn satisfiesTilde(self: SemVer, base: SemVer) bool {
        // ~1.2.3 := >=1.2.3 <1.3.0
        return self.major == base.major and
            self.minor == base.minor and
            self.patch >= base.patch;
    }
};

/// Version comparison operators
pub const Operator = enum {
    eq,   // =
    gt,   // >
    gte,  // >=
    lt,   // <
    lte,  // <=
    caret, // ^
    tilde, // ~
};

/// Version constraint for comparison
pub const VersionConstraint = struct {
    op: Operator,
    version: SemVer,

    pub fn parse(allocator: std.mem.Allocator, constraint_str: []const u8) !VersionConstraint {
        const trimmed = std.mem.trim(u8, constraint_str, " \t\n\r");
        
        if (trimmed.len == 0) return error.EmptyConstraint;

        var op: Operator = .eq;
        var version_start: usize = 0;

        if (std.mem.startsWith(u8, trimmed, ">=")) {
            op = .gte;
            version_start = 2;
        } else if (std.mem.startsWith(u8, trimmed, "<=")) {
            op = .lte;
            version_start = 2;
        } else if (std.mem.startsWith(u8, trimmed, "^")) {
            op = .caret;
            version_start = 1;
        } else if (std.mem.startsWith(u8, trimmed, "~")) {
            op = .tilde;
            version_start = 1;
        } else if (std.mem.startsWith(u8, trimmed, ">")) {
            op = .gt;
            version_start = 1;
        } else if (std.mem.startsWith(u8, trimmed, "<")) {
            op = .lt;
            version_start = 1;
        } else if (std.mem.startsWith(u8, trimmed, "=")) {
            op = .eq;
            version_start = 1;
        }

        const version_str = trimmed[version_start..];
        const version = try SemVer.parse(allocator, version_str);

        return VersionConstraint{
            .op = op,
            .version = version,
        };
    }

    pub fn deinit(self: *VersionConstraint) void {
        self.version.deinit();
    }
};

/// Version increment type
pub const IncrementType = enum {
    major,
    minor,
    patch,
};

/// Increment a version
pub fn increment(allocator: std.mem.Allocator, version: SemVer, inc_type: IncrementType) !SemVer {
    var result = SemVer{
        .major = version.major,
        .minor = version.minor,
        .patch = version.patch,
        .allocator = allocator,
    };

    switch (inc_type) {
        .major => {
            result.major += 1;
            result.minor = 0;
            result.patch = 0;
        },
        .minor => {
            result.minor += 1;
            result.patch = 0;
        },
        .patch => {
            result.patch += 1;
        },
    }

    return result;
}

/// Validate if a string is a valid semantic version
pub fn isValid(version_str: []const u8) bool {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var ver = SemVer.parse(allocator, version_str) catch return false;
    defer ver.deinit();
    return true;
}

/// Compare two version strings
pub fn compare(allocator: std.mem.Allocator, v1: []const u8, v2: []const u8) !i8 {
    var ver1 = try SemVer.parse(allocator, v1);
    defer ver1.deinit();

    var ver2 = try SemVer.parse(allocator, v2);
    defer ver2.deinit();

    return ver1.compare(ver2);
}

/// Get the highest version from a list
pub fn max(allocator: std.mem.Allocator, versions: []const []const u8) ![]const u8 {
    if (versions.len == 0) return error.EmptyList;

    var max_ver = try SemVer.parse(allocator, versions[0]);
    defer max_ver.deinit();
    var max_idx: usize = 0;

    for (versions[1..], 1..) |v, i| {
        var ver = try SemVer.parse(allocator, v);
        defer ver.deinit();

        if (ver.compare(max_ver) > 0) {
            max_ver.deinit();
            max_ver = try SemVer.parse(allocator, v);
            max_idx = i;
        }
    }

    return versions[max_idx];
}

/// Get the lowest version from a list
pub fn min(allocator: std.mem.Allocator, versions: []const []const u8) ![]const u8 {
    if (versions.len == 0) return error.EmptyList;

    var min_ver = try SemVer.parse(allocator, versions[0]);
    defer min_ver.deinit();
    var min_idx: usize = 0;

    for (versions[1..], 1..) |v, i| {
        var ver = try SemVer.parse(allocator, v);
        defer ver.deinit();

        if (ver.compare(min_ver) < 0) {
            min_ver.deinit();
            min_ver = try SemVer.parse(allocator, v);
            min_idx = i;
        }
    }

    return versions[min_idx];
}

// Internal helper to compare prerelease strings
fn comparePrerelease(pre1: []const u8, pre2: []const u8) i8 {
    var iter1 = std.mem.splitScalar(u8, pre1, '.');
    var iter2 = std.mem.splitScalar(u8, pre2, '.');

    while (true) {
        const part1 = iter1.next();
        const part2 = iter2.next();

        if (part1 == null and part2 == null) return 0;
        if (part1 == null) return -1;
        if (part2 == null) return 1;

        const p1 = part1.?;
        const p2 = part2.?;

        // Try numeric comparison first
        const num1 = std.fmt.parseInt(i32, p1, 10) catch null;
        const num2 = std.fmt.parseInt(i32, p2, 10) catch null;

        if (num1 != null and num2 != null) {
            if (num1.? < num2.?) return -1;
            if (num1.? > num2.?) return 1;
        } else if (num1 != null) {
            return -1; // Numeric < non-numeric
        } else if (num2 != null) {
            return 1; // Non-numeric > numeric
        } else {
            // Lexicographic comparison
            const order = std.mem.order(u8, p1, p2);
            if (order != .eq) return if (order == .lt) -1 else 1;
        }
    }
}

// Tests
test "parse basic version" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.2.3");
    defer ver.deinit();
    
    try std.testing.expectEqual(@as(u32, 1), ver.major);
    try std.testing.expectEqual(@as(u32, 2), ver.minor);
    try std.testing.expectEqual(@as(u32, 3), ver.patch);
}

test "parse version with prerelease" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.0.0-alpha.1");
    defer ver.deinit();
    
    try std.testing.expectEqual(@as(u32, 1), ver.major);
    try std.testing.expectEqual(@as(u32, 0), ver.minor);
    try std.testing.expectEqual(@as(u32, 0), ver.patch);
    try std.testing.expectEqualStrings("alpha.1", ver.prerelease.?);
}

test "parse version with build metadata" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.0.0+build.123");
    defer ver.deinit();
    
    try std.testing.expectEqualStrings("build.123", ver.build_metadata.?);
}

test "parse version with prerelease and build" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.0.0-beta.2+exp.sha.5114f85");
    defer ver.deinit();
    
    try std.testing.expectEqualStrings("beta.2", ver.prerelease.?);
    try std.testing.expectEqualStrings("exp.sha.5114f85", ver.build_metadata.?);
}

test "compare versions" {
    const allocator = std.testing.allocator;
    
    var v1 = try SemVer.parse(allocator, "1.0.0");
    defer v1.deinit();
    
    var v2 = try SemVer.parse(allocator, "2.0.0");
    defer v2.deinit();
    
    try std.testing.expectEqual(@as(i8, -1), v1.compare(v2));
    try std.testing.expectEqual(@as(i8, 1), v2.compare(v1));
    try std.testing.expectEqual(@as(i8, 0), v1.compare(v1));
}

test "compare prerelease versions" {
    const allocator = std.testing.allocator;
    
    var v1 = try SemVer.parse(allocator, "1.0.0-alpha");
    defer v1.deinit();
    
    var v2 = try SemVer.parse(allocator, "1.0.0");
    defer v2.deinit();
    
    // Prerelease has lower precedence
    try std.testing.expectEqual(@as(i8, -1), v1.compare(v2));
}

test "increment version" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.2.3");
    defer ver.deinit();
    
    var maj = try increment(allocator, ver, .major);
    defer maj.deinit();
    try std.testing.expectEqual(@as(u32, 2), maj.major);
    try std.testing.expectEqual(@as(u32, 0), maj.minor);
    try std.testing.expectEqual(@as(u32, 0), maj.patch);
    
    var minor_inc = try increment(allocator, ver, .minor);
    defer minor_inc.deinit();
    try std.testing.expectEqual(@as(u32, 1), minor_inc.major);
    try std.testing.expectEqual(@as(u32, 3), minor_inc.minor);
    try std.testing.expectEqual(@as(u32, 0), minor_inc.patch);
    
    var pat = try increment(allocator, ver, .patch);
    defer pat.deinit();
    try std.testing.expectEqual(@as(u32, 1), pat.major);
    try std.testing.expectEqual(@as(u32, 2), pat.minor);
    try std.testing.expectEqual(@as(u32, 4), pat.patch);
}

test "format version" {
    const allocator = std.testing.allocator;
    
    var ver = try SemVer.parse(allocator, "1.2.3-alpha.1+build.456");
    defer ver.deinit();
    
    const formatted = try ver.format(allocator);
    defer allocator.free(formatted);
    
    try std.testing.expectEqualStrings("1.2.3-alpha.1+build.456", formatted);
}

test "version constraint caret" {
    const allocator = std.testing.allocator;
    
    var constraint = try VersionConstraint.parse(allocator, "^1.2.3");
    defer constraint.deinit();
    
    var v1 = try SemVer.parse(allocator, "1.3.0");
    defer v1.deinit();
    try std.testing.expect(v1.satisfies(constraint));
    
    var v2 = try SemVer.parse(allocator, "2.0.0");
    defer v2.deinit();
    try std.testing.expect(!v2.satisfies(constraint));
}

test "version constraint tilde" {
    const allocator = std.testing.allocator;
    
    var constraint = try VersionConstraint.parse(allocator, "~1.2.3");
    defer constraint.deinit();
    
    var v1 = try SemVer.parse(allocator, "1.2.5");
    defer v1.deinit();
    try std.testing.expect(v1.satisfies(constraint));
    
    var v2 = try SemVer.parse(allocator, "1.3.0");
    defer v2.deinit();
    try std.testing.expect(!v2.satisfies(constraint));
}

test "max version" {
    const allocator = std.testing.allocator;
    
    const versions = [_][]const u8{ "1.0.0", "2.0.0", "1.5.0", "0.9.0" };
    const max_ver = try max(allocator, &versions);
    
    try std.testing.expectEqualStrings("2.0.0", max_ver);
}

test "min version" {
    const allocator = std.testing.allocator;
    
    const versions = [_][]const u8{ "1.0.0", "2.0.0", "1.5.0", "0.9.0" };
    const min_ver = try min(allocator, &versions);
    
    try std.testing.expectEqualStrings("0.9.0", min_ver);
}

test "isValid" {
    try std.testing.expect(isValid("1.0.0"));
    try std.testing.expect(isValid("1.2.3-alpha.1"));
    try std.testing.expect(isValid("1.0.0+build.123"));
    try std.testing.expect(!isValid(""));
    try std.testing.expect(!isValid("1"));
    try std.testing.expect(!isValid("1.2"));
}

test "compare function" {
    const allocator = std.testing.allocator;
    
    try std.testing.expectEqual(@as(i8, -1), try compare(allocator, "1.0.0", "2.0.0"));
    try std.testing.expectEqual(@as(i8, 1), try compare(allocator, "2.0.0", "1.0.0"));
    try std.testing.expectEqual(@as(i8, 0), try compare(allocator, "1.0.0", "1.0.0"));
}