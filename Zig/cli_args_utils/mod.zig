const std = @import("std");

/// Command line argument parser for Zig
/// Zero-dependency implementation using only the standard library

pub const Arg = struct {
    name: []const u8,
    short: ?u8 = null,
    long: ?[]const u8 = null,
    description: []const u8 = "",
    required: bool = false,
    has_value: bool = false,
    default_value: ?[]const u8 = null,
};

pub const ParsedArg = struct {
    name: []const u8,
    value: ?[]const u8 = null,
    present: bool = false,
    owned: bool = false, // true if value was allocated and needs to be freed
};

pub const ParseResult = struct {
    args: std.StringHashMap(ParsedArg),
    positional: std.ArrayList([]const u8),
    allocator: std.mem.Allocator,

    pub fn deinit(self: *ParseResult) void {
        // Free owned values in args
        var iter = self.args.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.owned and entry.value_ptr.value != null) {
                self.allocator.free(entry.value_ptr.value.?);
            }
        }
        self.args.deinit();

        // Free positional arguments
        for (self.positional.items) |arg| {
            self.allocator.free(arg);
        }
        self.positional.deinit();
    }

    pub fn get(self: ParseResult, name: []const u8) ?ParsedArg {
        return self.args.get(name);
    }

    pub fn getValue(self: ParseResult, name: []const u8) ?[]const u8 {
        if (self.args.get(name)) |arg| {
            return arg.value;
        }
        return null;
    }

    pub fn isPresent(self: ParseResult, name: []const u8) bool {
        if (self.args.get(name)) |arg| {
            return arg.present;
        }
        return false;
    }

    pub fn getPositional(self: ParseResult, index: usize) ?[]const u8 {
        if (index < self.positional.items.len) {
            return self.positional.items[index];
        }
        return null;
    }
};

pub const CliParser = struct {
    allocator: std.mem.Allocator,
    args: std.ArrayList(Arg),
    program_name: []const u8 = "",
    description: []const u8 = "",

    /// Initialize a new CLI parser
    pub fn init(allocator: std.mem.Allocator) CliParser {
        return .{
            .allocator = allocator,
            .args = std.ArrayList(Arg).init(allocator),
        };
    }

    /// Clean up resources
    pub fn deinit(self: *CliParser) void {
        self.args.deinit();
    }

    /// Set program name
    pub fn setProgramName(self: *CliParser, name: []const u8) *CliParser {
        self.program_name = name;
        return self;
    }

    /// Set program description
    pub fn setDescription(self: *CliParser, desc: []const u8) *CliParser {
        self.description = desc;
        return self;
    }

    /// Add a boolean flag argument (e.g., --verbose, -v)
    pub fn addFlag(
        self: *CliParser,
        name: []const u8,
        short: ?u8,
        long: ?[]const u8,
        description: []const u8,
    ) !*CliParser {
        try self.args.append(.{
            .name = name,
            .short = short,
            .long = long,
            .description = description,
            .has_value = false,
        });
        return self;
    }

    /// Add an option argument that takes a value (e.g., --file filename.txt)
    pub fn addOption(
        self: *CliParser,
        name: []const u8,
        short: ?u8,
        long: ?[]const u8,
        description: []const u8,
        required: bool,
        default_value: ?[]const u8,
    ) !*CliParser {
        try self.args.append(.{
            .name = name,
            .short = short,
            .long = long,
            .description = description,
            .required = required,
            .has_value = true,
            .default_value = default_value,
        });
        return self;
    }

    /// Parse command line arguments from os.argv
    pub fn parse(self: *CliParser) !ParseResult {
        const args = try std.process.argsAlloc(self.allocator);
        defer std.process.argsFree(self.allocator, args);
        return self.parseFromSlice(args);
    }

    /// Parse command line arguments from a slice
    pub fn parseFromSlice(self: *CliParser, argv: []const []const u8) !ParseResult {
        var result = ParseResult{
            .args = std.StringHashMap(ParsedArg).init(self.allocator),
            .positional = std.ArrayList([]const u8).init(self.allocator),
            .allocator = self.allocator,
        };
        errdefer result.deinit();

        // Initialize all defined args with defaults (not owned)
        for (self.args.items) |arg| {
            const parsed = ParsedArg{
                .name = arg.name,
                .value = arg.default_value,
                .present = false,
                .owned = false,
            };
            try result.args.put(arg.name, parsed);
        }

        var i: usize = 1; // Skip program name
        while (i < argv.len) {
            const arg = argv[i];

            if (std.mem.startsWith(u8, arg, "--")) {
                // Long option
                const name = arg[2..];
                if (std.mem.indexOf(u8, name, "=")) |eq_pos| {
                    // --option=value format
                    const opt_name = name[0..eq_pos];
                    const value = name[eq_pos + 1 ..];
                    if (self.findArgByLong(opt_name)) |found| {
                        var parsed = result.args.get(found.name).?;
                        if (parsed.owned and parsed.value != null) {
                            self.allocator.free(parsed.value.?);
                        }
                        parsed.present = true;
                        parsed.value = try self.allocator.dupe(u8, value);
                        parsed.owned = true;
                        try result.args.put(found.name, parsed);
                    }
                } else {
                    // --option value format
                    if (self.findArgByLong(name)) |found| {
                        var parsed = result.args.get(found.name).?;
                        parsed.present = true;
                        if (found.has_value) {
                            i += 1;
                            if (i < argv.len) {
                                if (parsed.owned and parsed.value != null) {
                                    self.allocator.free(parsed.value.?);
                                }
                                parsed.value = try self.allocator.dupe(u8, argv[i]);
                                parsed.owned = true;
                            }
                        }
                        try result.args.put(found.name, parsed);
                    }
                }
            } else if (std.mem.startsWith(u8, arg, "-") and arg.len > 1) {
                // Short option(s)
                const short_chars = arg[1..];
                for (short_chars, 0..) |c, idx| {
                    if (self.findArgByShort(c)) |found| {
                        var parsed = result.args.get(found.name).?;
                        parsed.present = true;
                        if (found.has_value) {
                            // Value can be attached or next arg
                            if (idx + 1 < short_chars.len) {
                                // -fvalue format: remaining chars are the value
                                if (parsed.owned and parsed.value != null) {
                                    self.allocator.free(parsed.value.?);
                                }
                                parsed.value = try self.allocator.dupe(u8, short_chars[idx + 1 ..]);
                                parsed.owned = true;
                                try result.args.put(found.name, parsed);
                                break; // Done with this arg
                            } else {
                                // -f value format
                                i += 1;
                                if (i < argv.len and !std.mem.startsWith(u8, argv[i], "-")) {
                                    if (parsed.owned and parsed.value != null) {
                                        self.allocator.free(parsed.value.?);
                                    }
                                    parsed.value = try self.allocator.dupe(u8, argv[i]);
                                    parsed.owned = true;
                                }
                                try result.args.put(found.name, parsed);
                            }
                        } else {
                            try result.args.put(found.name, parsed);
                        }
                    }
                }
            } else {
                // Positional argument
                try result.positional.append(try self.allocator.dupe(u8, arg));
            }
            i += 1;
        }

        return result;
    }

    fn findArgByLong(self: CliParser, name: []const u8) ?Arg {
        for (self.args.items) |arg| {
            if (arg.long) |long| {
                if (std.mem.eql(u8, long, name)) {
                    return arg;
                }
            }
        }
        return null;
    }

    fn findArgByShort(self: CliParser, short: u8) ?Arg {
        for (self.args.items) |arg| {
            if (arg.short == short) {
                return arg;
            }
        }
        return null;
    }

    /// Generate help text
    pub fn generateHelp(self: CliParser, writer: anytype) !void {
        try writer.print("Usage: {s} [options]\n\n", .{self.program_name});
        if (self.description.len > 0) {
            try writer.print("{s}\n\n", .{self.description});
        }
        try writer.print("Options:\n", .{});

        for (self.args.items) |arg| {
            var buf: [64]u8 = undefined;
            var opt_str: []const u8 = "";

            if (arg.short) |s| {
                if (arg.long) |l| {
                    opt_str = try std.fmt.bufPrint(&buf, "-{c}, --{s}", .{ s, l });
                } else {
                    opt_str = try std.fmt.bufPrint(&buf, "-{c}", .{s});
                }
            } else if (arg.long) |l| {
                opt_str = try std.fmt.bufPrint(&buf, "    --{s}", .{l});
            }

            if (arg.has_value) {
                var buf2: [128]u8 = undefined;
                opt_str = try std.fmt.bufPrint(&buf2, "{s} <value>", .{opt_str});
            }

            try writer.print("  {s:<20} {s}", .{ opt_str, arg.description });
            if (arg.default_value) |d| {
                try writer.print(" (default: {s})", .{d});
            }
            if (arg.required) {
                try writer.print(" [required]", .{});
            }
            try writer.print("\n", .{});
        }
    }

    /// Validate that all required arguments are present
    pub fn validate(self: CliParser, result: ParseResult) !void {
        for (self.args.items) |arg| {
            if (arg.required) {
                const parsed = result.args.get(arg.name);
                if (parsed == null or !parsed.?.present) {
                    return error.MissingRequiredArguments;
                }
            }
        }
    }
};

// ========== Utility Functions ==========

/// Simple argument parsing for common use cases
/// Returns a map of flag/value pairs
pub fn parseSimple(allocator: std.mem.Allocator, argv: []const []const u8) !std.StringHashMap(?[]const u8) {
    var result = std.StringHashMap(?[]const u8).init(allocator);
    errdefer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }

    var i: usize = 1;
    while (i < argv.len) {
        const arg = argv[i];

        if (std.mem.startsWith(u8, arg, "--")) {
            const name = arg[2..];
            if (std.mem.indexOf(u8, name, "=")) |eq_pos| {
                const key = try allocator.dupe(u8, name[0..eq_pos]);
                const value = try allocator.dupe(u8, name[eq_pos + 1 ..]);
                try result.put(key, value);
            } else {
                i += 1;
                if (i < argv.len and !std.mem.startsWith(u8, argv[i], "-")) {
                    const key = try allocator.dupe(u8, name);
                    const value = try allocator.dupe(u8, argv[i]);
                    try result.put(key, value);
                } else {
                    const key = try allocator.dupe(u8, name);
                    try result.put(key, null);
                    i -= 1;
                }
            }
        } else if (std.mem.startsWith(u8, arg, "-") and arg.len > 1) {
            const key = try allocator.dupe(u8, arg[1..]);
            try result.put(key, null);
        }
        i += 1;
    }

    return result;
}

/// Check if a flag is present in arguments
pub fn hasFlag(argv: []const []const u8, short: ?u8, long: ?[]const u8) bool {
    for (argv) |arg| {
        if (short) |s| {
            if (arg.len == 2 and arg[0] == '-' and arg[1] == s) {
                return true;
            }
        }
        if (long) |l| {
            if (std.mem.startsWith(u8, arg, "--") and std.mem.eql(u8, arg[2..], l)) {
                return true;
            }
        }
    }
    return false;
}

/// Get the value of an option
pub fn getOption(argv: []const []const u8, short: ?u8, long: ?[]const u8) ?[]const u8 {
    var i: usize = 1;
    while (i < argv.len) : (i += 1) {
        const arg = argv[i];

        // Check for --option=value format
        if (long) |l| {
            if (arg.len > l.len + 3 and
                std.mem.startsWith(u8, arg, "--") and
                std.mem.eql(u8, arg[2 .. l.len + 2], l) and
                arg[l.len + 2] == '=')
            {
                return arg[l.len + 3 ..];
            }
        }

        // Check short option
        if (short) |s| {
            if (arg.len == 2 and arg[0] == '-' and arg[1] == s) {
                if (i + 1 < argv.len) {
                    return argv[i + 1];
                }
            }
        }

        // Check long option
        if (long) |l| {
            if (arg.len == l.len + 2 and
                std.mem.startsWith(u8, arg, "--") and
                std.mem.eql(u8, arg[2..], l))
            {
                if (i + 1 < argv.len) {
                    return argv[i + 1];
                }
            }
        }
    }
    return null;
}

/// Get all positional arguments (non-flag arguments)
pub fn getPositionalArgs(allocator: std.mem.Allocator, argv: []const []const u8) ![][]const u8 {
    var result = std.ArrayList([]const u8).init(allocator);
    errdefer result.deinit();

    var i: usize = 1;
    while (i < argv.len) {
        const arg = argv[i];
        if (!std.mem.startsWith(u8, arg, "-")) {
            // Positional argument
            try result.append(try allocator.dupe(u8, arg));
        }
        i += 1;
    }

    return result.toOwnedSlice();
}

/// Count the number of positional arguments
pub fn countPositionalArgs(argv: []const []const u8) usize {
    var count: usize = 0;
    var i: usize = 1;
    while (i < argv.len) {
        const arg = argv[i];
        if (!std.mem.startsWith(u8, arg, "-")) {
            // Positional argument
            count += 1;
        }
        i += 1;
    }
    return count;
}

// Tests
test "CliParser - basic flag parsing" {
    const allocator = std.testing.allocator;

    var parser = CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("help", 'h', "help", "Show help");

    const argv = [_][]const u8{ "myprogram", "-v", "--help" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("verbose"));
    try std.testing.expect(result.isPresent("help"));
}

test "CliParser - option with value" {
    const allocator = std.testing.allocator;

    var parser = CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("file", 'f', "file", "Input file", false, null);
    _ = try parser.addOption("output", 'o', "output", "Output file", false, "out.txt");

    const argv = [_][]const u8{ "myprogram", "-f", "input.txt", "--output", "result.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("file"));
    try std.testing.expectEqualStrings("input.txt", result.getValue("file").?);

    try std.testing.expect(result.isPresent("output"));
    try std.testing.expectEqualStrings("result.txt", result.getValue("output").?);
}

test "CliParser - equals syntax" {
    const allocator = std.testing.allocator;

    var parser = CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("name", 'n', "name", "Name value", false, null);

    const argv = [_][]const u8{ "myprogram", "--name=John" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(result.isPresent("name"));
    try std.testing.expectEqualStrings("John", result.getValue("name").?);
}

test "CliParser - positional arguments" {
    const allocator = std.testing.allocator;

    var parser = CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose");

    const argv = [_][]const u8{ "myprogram", "-v", "file1.txt", "file2.txt" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expectEqual(@as(usize, 2), result.positional.items.len);
    try std.testing.expectEqualStrings("file1.txt", result.getPositional(0).?);
    try std.testing.expectEqualStrings("file2.txt", result.getPositional(1).?);
}

test "parseSimple - basic usage" {
    const allocator = std.testing.allocator;

    const argv = [_][]const u8{ "prog", "--name=Alice", "--verbose", "-d", "directory" };

    var result = try parseSimple(allocator, &argv);
    defer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }

    try std.testing.expectEqualStrings("Alice", result.get("name").?.?);
    try std.testing.expect(result.get("verbose").? == null);
    try std.testing.expect(result.get("d") != null);
}

test "hasFlag - detect flags" {
    const argv = [_][]const u8{ "prog", "-v", "--verbose", "--help" };

    try std.testing.expect(hasFlag(&argv, 'v', null));
    try std.testing.expect(hasFlag(&argv, null, "verbose"));
    try std.testing.expect(hasFlag(&argv, 'h', "help"));
    try std.testing.expect(!hasFlag(&argv, 'q', null));
}

test "countPositionalArgs - count non-flag arguments" {
    const argv1 = [_][]const u8{ "prog", "file1.txt", "file2.txt" };
    try std.testing.expectEqual(@as(usize, 2), countPositionalArgs(&argv1));

    const argv2 = [_][]const u8{ "prog", "-v", "file.txt", "--output=out.txt" };
    try std.testing.expectEqual(@as(usize, 1), countPositionalArgs(&argv2));
}

test "CliParser - default values" {
    const allocator = std.testing.allocator;

    var parser = CliParser.init(allocator);
    defer parser.deinit();

    _ = try parser.addOption("port", 'p', "port", "Port number", false, "8080");

    const argv = [_][]const u8{ "myprogram" };

    var result = try parser.parseFromSlice(&argv);
    defer result.deinit();

    try std.testing.expect(!result.isPresent("port"));
    try std.testing.expectEqualStrings("8080", result.getValue("port").?);
}