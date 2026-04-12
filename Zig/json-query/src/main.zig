const std = @import("std");

// JSON Value types
pub const JsonValue = union(enum) {
    null: void,
    bool: bool,
    integer: i64,
    float: f64,
    string: []const u8,
    array: []JsonValue,
    object: std.StringHashMap(JsonValue),

    pub fn deinit(self: *JsonValue, allocator: std.mem.Allocator) void {
        switch (self.*) {
            .string => |s| allocator.free(s),
            .array => |arr| {
                for (arr) |*item| {
                    @constCast(item).deinit(allocator);
                }
                allocator.free(arr);
            },
            .object => |*obj| {
                var iter = obj.iterator();
                while (iter.next()) |entry| {
                    allocator.free(entry.key_ptr.*);
                    @constCast(entry.value_ptr).deinit(allocator);
                }
                obj.deinit();
            },
            else => {},
        }
    }

    pub fn getType(self: JsonValue) []const u8 {
        return switch (self) {
            .null => "null",
            .bool => "boolean",
            .integer => "integer",
            .float => "float",
            .string => "string",
            .array => "array",
            .object => "object",
        };
    }

    pub fn asString(self: JsonValue) ?[]const u8 {
        return switch (self) {
            .string => |s| s,
            else => null,
        };
    }

    pub fn asInt(self: JsonValue) ?i64 {
        return switch (self) {
            .integer => |i| i,
            else => null,
        };
    }

    pub fn asFloat(self: JsonValue) ?f64 {
        return switch (self) {
            .float => |f| f,
            .integer => |i| @floatFromInt(i),
            else => null,
        };
    }

    pub fn asBool(self: JsonValue) ?bool {
        return switch (self) {
            .bool => |b| b,
            else => null,
        };
    }

    pub fn asArray(self: JsonValue) ?[]JsonValue {
        return switch (self) {
            .array => |arr| arr,
            else => null,
        };
    }

    pub fn get(self: JsonValue, key: []const u8) ?JsonValue {
        return switch (self) {
            .object => |obj| obj.get(key),
            else => null,
        };
    }

    pub fn atIndex(self: JsonValue, index: usize) ?JsonValue {
        return switch (self) {
            .array => |arr| if (index < arr.len) arr[index] else null,
            else => null,
        };
    }
};

// JSON Parser
pub const JsonParser = struct {
    allocator: std.mem.Allocator,
    input: []const u8,
    pos: usize,

    pub fn init(allocator: std.mem.Allocator, input: []const u8) JsonParser {
        return .{
            .allocator = allocator,
            .input = input,
            .pos = 0,
        };
    }

    pub fn parse(self: *JsonParser) anyerror!JsonValue {
        self.skipWhitespace();
        return try self.parseValue();
    }

    fn parseValue(self: *JsonParser) anyerror!JsonValue {
        self.skipWhitespace();
        if (self.pos >= self.input.len) return error.UnexpectedEnd;

        const c = self.input[self.pos];
        return switch (c) {
            'n' => self.parseNull(),
            't' => self.parseTrue(),
            'f' => self.parseFalse(),
            '"' => self.parseString(),
            '[' => self.parseArray(),
            '{' => self.parseObject(),
            '-', '0'...'9' => self.parseNumber(),
            else => error.InvalidCharacter,
        };
    }

    fn parseNull(self: *JsonParser) anyerror!JsonValue {
        if (self.pos + 4 > self.input.len) return error.UnexpectedEnd;
        if (!std.mem.eql(u8, self.input[self.pos .. self.pos + 4], "null")) return error.InvalidLiteral;
        self.pos += 4;
        return .null;
    }

    fn parseTrue(self: *JsonParser) anyerror!JsonValue {
        if (self.pos + 4 > self.input.len) return error.UnexpectedEnd;
        if (!std.mem.eql(u8, self.input[self.pos .. self.pos + 4], "true")) return error.InvalidLiteral;
        self.pos += 4;
        return .{ .bool = true };
    }

    fn parseFalse(self: *JsonParser) anyerror!JsonValue {
        if (self.pos + 5 > self.input.len) return error.UnexpectedEnd;
        if (!std.mem.eql(u8, self.input[self.pos .. self.pos + 5], "false")) return error.InvalidLiteral;
        self.pos += 5;
        return .{ .bool = false };
    }

    fn parseString(self: *JsonParser) anyerror!JsonValue {
        self.pos += 1; // skip opening quote

        // Count length and parse
        var len: usize = 0;
        var temp_pos = self.pos;
        while (temp_pos < self.input.len and self.input[temp_pos] != '"') {
            if (self.input[temp_pos] == '\\') {
                temp_pos += 2;
                len += 1;
            } else {
                temp_pos += 1;
                len += 1;
            }
        }

        var result = try self.allocator.alloc(u8, len);
        var out_pos: usize = 0;

        while (self.pos < self.input.len) {
            const c = self.input[self.pos];
            if (c == '"') {
                self.pos += 1;
                return .{ .string = result[0..out_pos] };
            }
            if (c == '\\') {
                self.pos += 1;
                if (self.pos >= self.input.len) return error.UnexpectedEnd;
                const escaped = self.input[self.pos];
                result[out_pos] = switch (escaped) {
                    '"', '\\', '/' => escaped,
                    'n' => '\n',
                    'r' => '\r',
                    't' => '\t',
                    else => escaped,
                };
                out_pos += 1;
                self.pos += 1;
            } else {
                result[out_pos] = c;
                out_pos += 1;
                self.pos += 1;
            }
        }
        return error.UnexpectedEnd;
    }

    fn parseNumber(self: *JsonParser) anyerror!JsonValue {
        const start = self.pos;
        var is_float = false;

        if (self.input[self.pos] == '-') self.pos += 1;

        while (self.pos < self.input.len and self.input[self.pos] >= '0' and self.input[self.pos] <= '9') {
            self.pos += 1;
        }

        if (self.pos < self.input.len and self.input[self.pos] == '.') {
            is_float = true;
            self.pos += 1;
            while (self.pos < self.input.len and self.input[self.pos] >= '0' and self.input[self.pos] <= '9') {
                self.pos += 1;
            }
        }

        if (self.pos < self.input.len and (self.input[self.pos] == 'e' or self.input[self.pos] == 'E')) {
            is_float = true;
            self.pos += 1;
            if (self.pos < self.input.len and (self.input[self.pos] == '+' or self.input[self.pos] == '-')) {
                self.pos += 1;
            }
            while (self.pos < self.input.len and self.input[self.pos] >= '0' and self.input[self.pos] <= '9') {
                self.pos += 1;
            }
        }

        const num_str = self.input[start..self.pos];
        if (is_float) {
            const f = try std.fmt.parseFloat(f64, num_str);
            return .{ .float = f };
        } else {
            const i = try std.fmt.parseInt(i64, num_str, 10);
            return .{ .integer = i };
        }
    }

    fn parseArray(self: *JsonParser) anyerror!JsonValue {
        self.pos += 1; // skip [
        var items = std.ArrayList(JsonValue).init(self.allocator);

        self.skipWhitespace();
        if (self.pos < self.input.len and self.input[self.pos] == ']') {
            self.pos += 1;
            return JsonValue{ .array = try items.toOwnedSlice() };
        }

        while (true) {
            self.skipWhitespace();
            const item = try self.parseValue();
            try items.append(item);

            self.skipWhitespace();
            if (self.pos >= self.input.len) return error.UnexpectedEnd;

            if (self.input[self.pos] == ',') {
                self.pos += 1;
            } else if (self.input[self.pos] == ']') {
                self.pos += 1;
                break;
            } else {
                return error.InvalidCharacter;
            }
        }

        return JsonValue{ .array = try items.toOwnedSlice() };
    }

    fn parseObject(self: *JsonParser) anyerror!JsonValue {
        self.pos += 1; // skip {
        var obj = std.StringHashMap(JsonValue).init(self.allocator);

        self.skipWhitespace();
        if (self.pos < self.input.len and self.input[self.pos] == '}') {
            self.pos += 1;
            return .{ .object = obj };
        }

        while (true) {
            self.skipWhitespace();
            if (self.pos >= self.input.len or self.input[self.pos] != '"') return error.ExpectedKey;

            const key = (try self.parseString()).string;
            const key_copy = try self.allocator.dupe(u8, key);
            self.allocator.free(@constCast(key));

            self.skipWhitespace();
            if (self.pos >= self.input.len or self.input[self.pos] != ':') return error.ExpectedColon;
            self.pos += 1;

            self.skipWhitespace();
            const value = try self.parseValue();
            try obj.put(key_copy, value);

            self.skipWhitespace();
            if (self.pos >= self.input.len) return error.UnexpectedEnd;

            if (self.input[self.pos] == ',') {
                self.pos += 1;
            } else if (self.input[self.pos] == '}') {
                self.pos += 1;
                break;
            } else {
                return error.InvalidCharacter;
            }
        }

        return .{ .object = obj };
    }

    fn skipWhitespace(self: *JsonParser) void {
        while (self.pos < self.input.len) {
            switch (self.input[self.pos]) {
                ' ', '\t', '\n', '\r' => self.pos += 1,
                else => break,
            }
        }
    }
};

// Simple JSON Path Query (no allocation for path tokens)
pub const JsonQuery = struct {
    pub fn query(root: JsonValue, path: []const u8) ?JsonValue {
        if (path.len == 0) return root;

        var current = root;
        var pos: usize = 0;

        // Skip initial $
        if (path.len > 0 and path[0] == '$') {
            pos = 1;
        }

        while (pos < path.len) {
            if (path[pos] == '.') {
                pos += 1;
                if (pos >= path.len) break;

                // Parse key name
                const start = pos;
                while (pos < path.len and path[pos] != '.' and path[pos] != '[') {
                    pos += 1;
                }
                const key = path[start..pos];
                current = current.get(key) orelse return null;
            } else if (path[pos] == '[') {
                pos += 1;
                if (pos >= path.len) return null;

                // Parse index
                const start = pos;
                while (pos < path.len and path[pos] != ']') {
                    pos += 1;
                }
                const idx_str = path[start..pos];
                const idx = std.fmt.parseInt(usize, idx_str, 10) catch return null;
                current = current.atIndex(idx) orelse return null;
                pos += 1; // skip ]
            } else {
                pos += 1;
            }
        }

        return current;
    }
};

// Tests
test "JsonValue types" {
    const testing = std.testing;

    const null_val: JsonValue = .null;
    try testing.expectEqualStrings("null", null_val.getType());

    const bool_val: JsonValue = .{ .bool = true };
    try testing.expect(bool_val.asBool().?);

    const int_val: JsonValue = .{ .integer = 42 };
    try testing.expectEqual(@as(i64, 42), int_val.asInt().?);

    const float_val: JsonValue = .{ .float = 3.14 };
    try testing.expectApproxEqAbs(@as(f64, 3.14), float_val.asFloat().?, 0.001);

    const str_val: JsonValue = .{ .string = "hello" };
    try testing.expectEqualStrings("hello", str_val.asString().?);
}

test "JSON parse - primitives" {
    const testing = std.testing;
    const allocator = testing.allocator;

    var parser = JsonParser.init(allocator, "null");
    const val1 = try parser.parse();
    try testing.expectEqualStrings("null", val1.getType());

    parser = JsonParser.init(allocator, "true");
    const val2 = try parser.parse();
    try testing.expect(val2.asBool().?);

    parser = JsonParser.init(allocator, "42");
    const val3 = try parser.parse();
    try testing.expectEqual(@as(i64, 42), val3.asInt().?);

    parser = JsonParser.init(allocator, "3.14");
    const val4 = try parser.parse();
    try testing.expectApproxEqAbs(@as(f64, 3.14), val4.asFloat().?, 0.001);

    // String test - needs cleanup
    parser = JsonParser.init(allocator, "\"hello\"");
    var val5 = try parser.parse();
    try testing.expectEqualStrings("hello", val5.asString().?);
    val5.deinit(allocator);
}

test "JSON parse - array" {
    const testing = std.testing;
    const allocator = testing.allocator;

    var parser = JsonParser.init(allocator, "[1, 2, 3]");
    var val = try parser.parse();

    const arr = val.asArray().?;
    try testing.expectEqual(@as(usize, 3), arr.len);
    try testing.expectEqual(@as(i64, 1), arr[0].asInt().?);
    try testing.expectEqual(@as(i64, 2), arr[1].asInt().?);
    try testing.expectEqual(@as(i64, 3), arr[2].asInt().?);

    val.deinit(allocator);
}

test "JSON parse - object" {
    const testing = std.testing;
    const allocator = testing.allocator;

    var parser = JsonParser.init(allocator, "{\"name\": \"Alice\", \"age\": 30}");
    var val = try parser.parse();

    try testing.expectEqualStrings("Alice", val.get("name").?.asString().?);
    try testing.expectEqual(@as(i64, 30), val.get("age").?.asInt().?);

    val.deinit(allocator);
}

test "JsonQuery - basic path" {
    const testing = std.testing;
    const allocator = testing.allocator;

    const input = "{\"name\": \"Alice\", \"age\": 30}";
    var parser = JsonParser.init(allocator, input);
    var val = try parser.parse();
    defer val.deinit(allocator);

    const result1 = JsonQuery.query(val, "$.name");
    try testing.expectEqualStrings("Alice", result1.?.asString().?);

    const result2 = JsonQuery.query(val, "$.age");
    try testing.expectEqual(@as(i64, 30), result2.?.asInt().?);
}

test "JsonQuery - nested path" {
    const testing = std.testing;
    const allocator = testing.allocator;

    const input = "{\"user\": {\"name\": \"Alice\", \"city\": \"Beijing\"}}";
    var parser = JsonParser.init(allocator, input);
    var val = try parser.parse();
    defer val.deinit(allocator);

    const result = JsonQuery.query(val, "$.user.name");
    try testing.expectEqualStrings("Alice", result.?.asString().?);
}

test "JsonQuery - array access" {
    const testing = std.testing;
    const allocator = testing.allocator;

    const input = "{\"items\": [\"a\", \"b\", \"c\"]}";
    var parser = JsonParser.init(allocator, input);
    var val = try parser.parse();
    defer val.deinit(allocator);

    const result1 = JsonQuery.query(val, "$.items[0]");
    try testing.expectEqualStrings("a", result1.?.asString().?);

    const result2 = JsonQuery.query(val, "$.items[2]");
    try testing.expectEqualStrings("c", result2.?.asString().?);
}

test "JsonQuery - complex nested" {
    const testing = std.testing;
    const allocator = testing.allocator;

    const input =
        \\{
        \\  "users": [
        \\    {"name": "Alice", "age": 30},
        \\    {"name": "Bob", "age": 25}
        \\  ]
        \\}
    ;

    var parser = JsonParser.init(allocator, input);
    var val = try parser.parse();
    defer val.deinit(allocator);

    const result1 = JsonQuery.query(val, "$.users[0].name");
    try testing.expectEqualStrings("Alice", result1.?.asString().?);

    const result2 = JsonQuery.query(val, "$.users[1].age");
    try testing.expectEqual(@as(i64, 25), result2.?.asInt().?);
}

// CLI Entry Point
pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    const stdout = std.io.getStdOut().writer();

    if (args.len < 2) {
        try stdout.print(
            \\JSON Query Tool - Query JSON data with path expressions
            \\
            \\Usage:
            \\  json-query <json-file> <path>
            \\
            \\Path Syntax:
            \\  $.key       - Get object key
            \\  $[0]        - Get array index
            \\  $.key[0]    - Nested access
            \\
            \\Examples:
            \\  json-query data.json $.users[0].name
            \\  json-query data.json $.items[1]
            \\
        , .{});
        return;
    }

    const file_content = std.fs.cwd().readFileAlloc(allocator, args[1], std.math.maxInt(usize)) catch |err| {
        try stdout.print("Error reading file: {}\n", .{err});
        return;
    };

    var parser = JsonParser.init(allocator, file_content);
    var val = parser.parse() catch |err| {
        try stdout.print("Error parsing JSON: {}\n", .{err});
        return;
    };
    defer val.deinit(allocator);

    const path = if (args.len >= 3) args[2] else "";
    if (JsonQuery.query(val, path)) |result| {
        switch (result) {
            .string => |s| try stdout.print("{s}\n", .{s}),
            .integer => |i| try stdout.print("{}\n", .{i}),
            .float => |f| try stdout.print("{d}\n", .{f}),
            .bool => |b| try stdout.print("{}\n", .{b}),
            .null => try stdout.print("null\n", .{}),
            else => try stdout.print("(complex value)\n", .{}),
        }
    } else {
        try stdout.print("null\n", .{});
    }
}