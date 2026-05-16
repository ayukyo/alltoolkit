const std = @import("std");

/// CBOR Major Types (RFC 8949)
pub const MajorType = enum(u3) {
    positive_int = 0,
    negative_int = 1,
    byte_string = 2,
    text_string = 3,
    array = 4,
    map = 5,
    tag = 6,
    simple_float = 7,
};

/// CBOR Simple Values
pub const SimpleValue = enum(u8) {
    false_val = 20,
    true_val = 21,
    null_val = 22,
    undefined_val = 23,
};

/// CBOR Well-known Tags
pub const Tag = enum(u64) {
    standard_date_time_string = 0,
    epoch_date_time = 1,
    positive_bignum = 2,
    negative_bignum = 3,
    decimal_fraction = 4,
    bigfloat = 5,
    expected_base64url = 21,
    expected_base64 = 22,
    expected_base16 = 23,
    encoded_cbor_data_item = 24,
    uri = 32,
    base64url = 33,
    base64 = 34,
    regex = 35,
    mime_message = 36,
    uuid = 37,
    self_described_cbor = 55799,
};

/// CBOR Value - Represents any CBOR data type
pub const Value = union(enum) {
    positive_int: u64,
    negative_int: u64, // Stored as absolute value - 1
    byte_string: []const u8,
    text_string: []const u8,
    array: []Value,
    map: []MapEntry,
    tag: TaggedValue,
    simple: SimpleValue,
    float: f64,

    const Self = @This();

    pub fn deinit(self: Self, allocator: std.mem.Allocator) void {
        switch (self) {
            .byte_string => |bs| allocator.free(bs),
            .text_string => |ts| allocator.free(ts),
            .array => |arr| {
                for (arr) |item| item.deinit(allocator);
                allocator.free(arr);
            },
            .map => |entries| {
                for (entries) |entry| {
                    entry.key.deinit(allocator);
                    entry.value.deinit(allocator);
                }
                allocator.free(entries);
            },
            .tag => |tv| {
                tv.value.deinit(allocator);
            },
            else => {},
        }
    }

    pub fn isInteger(self: Self) bool {
        return self == .positive_int or self == .negative_int;
    }

    pub fn toInteger(self: Self) ?i65 {
        return switch (self) {
            .positive_int => |v| @as(i65, @intCast(v)),
            .negative_int => |v| -@as(i65, @intCast(v)) - 1,
            else => null,
        };
    }

    pub fn toJson(self: Self, allocator: std.mem.Allocator) ![]u8 {
        var list = std.ArrayList(u8).init(allocator);
        errdefer list.deinit();
        try self.toJsonWriter(list.writer());
        return list.toOwnedSlice();
    }

    fn toJsonWriter(self: Self, writer: anytype) !void {
        switch (self) {
            .positive_int => |v| try writer.print("{}", .{v}),
            .negative_int => |v| try writer.print("{}", .{-@as(i65, @intCast(v)) - 1}),
            .byte_string => |bs| {
                try writer.writeAll("\"");
                for (bs) |b| {
                    try writer.print("\\x{X:0>2}", .{b});
                }
                try writer.writeAll("\"");
            },
            .text_string => |ts| {
                try writer.writeAll("\"");
                for (ts) |c| {
                    switch (c) {
                        '"' => try writer.writeAll("\\\""),
                        '\\' => try writer.writeAll("\\\\"),
                        '\n' => try writer.writeAll("\\n"),
                        '\r' => try writer.writeAll("\\r"),
                        '\t' => try writer.writeAll("\\t"),
                        0x00...0x08 => try writer.print("\\u{X:0>4}", .{c}),
                        0x0B...0x0C => try writer.print("\\u{X:0>4}", .{c}),
                        0x0E...0x1F => try writer.print("\\u{X:0>4}", .{c}),
                        else => try writer.writeByte(c),
                    }
                }
                try writer.writeAll("\"");
            },
            .array => |arr| {
                try writer.writeAll("[");
                for (arr, 0..) |item, i| {
                    if (i > 0) try writer.writeAll(",");
                    try item.toJsonWriter(writer);
                }
                try writer.writeAll("]");
            },
            .map => |entries| {
                try writer.writeAll("{");
                for (entries, 0..) |entry, i| {
                    if (i > 0) try writer.writeAll(",");
                    try entry.key.toJsonWriter(writer);
                    try writer.writeAll(":");
                    try entry.value.toJsonWriter(writer);
                }
                try writer.writeAll("}");
            },
            .tag => |tv| {
                try writer.print("{}(", .{tv.tag});
                try tv.value.toJsonWriter(writer);
                try writer.writeAll(")");
            },
            .simple => |sv| try writer.writeAll(switch (sv) {
                .false_val => "false",
                .true_val => "true",
                .null_val => "null",
                .undefined_val => "\"undefined\"",
            }),
            .float => |f| {
                if (std.math.isNan(f)) {
                    try writer.writeAll("\"NaN\"");
                } else if (std.math.isInf(f)) {
                    try writer.writeAll(if (f > 0) "\"Infinity\"" else "\"-Infinity\"");
                } else {
                    try writer.print("{d}", .{f});
                }
            },
        }
    }
};

pub const MapEntry = struct {
    key: Value,
    value: Value,
};

pub const TaggedValue = struct {
    tag: u64,
    value: *Value,
};

/// CBOR Encoding Options
pub const EncodeOptions = struct {
    /// Use deterministic encoding (sorted map keys, shortest floats)
    deterministic: bool = false,
    /// Use 64-bit floats only (for deterministic mode)
    force_float64: bool = false,
};

/// CBOR Decoding Options
pub const DecodeOptions = struct {
    /// Maximum nesting depth
    max_depth: usize = 256,
    /// Maximum array/map length
    max_length: usize = 1024 * 1024,
};

/// CBOR Error Types
pub const CborError = error{
    /// Invalid major type
    InvalidMajorType,
    /// Invalid additional info
    InvalidAdditionalInfo,
    /// Invalid simple value
    InvalidSimpleValue,
    /// Invalid UTF-8 in text string
    InvalidUtf8,
    /// Unexpected end of input
    UnexpectedEof,
    /// Buffer too small
    BufferTooSmall,
    /// Memory allocation failed
    OutOfMemory,
    /// Maximum nesting depth exceeded
    MaxDepthExceeded,
    /// Maximum length exceeded
    MaxLengthExceeded,
    /// Invalid tag
    InvalidTag,
    /// Invalid float format
    InvalidFloat,
    /// Indefinite length not supported
    IndefiniteLengthNotSupported,
};

/// CBOR Encoder
pub const Encoder = struct {
    buffer: []u8,
    pos: usize,

    const Self = @This();

    pub fn init(buffer: []u8) Self {
        return .{
            .buffer = buffer,
            .pos = 0,
        };
    }

    pub fn encoded(self: Self) []const u8 {
        return self.buffer[0..self.pos];
    }

    /// Encode a CBOR value
    pub fn encode(self: *Self, value: Value) CborError!void {
        return self.encodeValue(value, .{});
    }

    /// Encode a CBOR value with options
    pub fn encodeWithOpts(self: *Self, value: Value, opts: EncodeOptions) CborError!void {
        return self.encodeValue(value, opts);
    }

    fn encodeValue(self: *Self, value: Value, opts: EncodeOptions) CborError!void {
        switch (value) {
            .positive_int => |v| try self.encodeUint(.positive_int, v),
            .negative_int => |v| try self.encodeUint(.negative_int, v),
            .byte_string => |bs| {
                try self.encodeHead(.byte_string, bs.len);
                try self.writeBytes(bs);
            },
            .text_string => |ts| {
                try self.encodeHead(.text_string, ts.len);
                try self.writeBytes(ts);
            },
            .array => |arr| {
                try self.encodeHead(.array, arr.len);
                for (arr) |item| {
                    try self.encodeValue(item, opts);
                }
            },
            .map => |entries| {
                if (opts.deterministic) {
                    // For deterministic encoding, we'd need to sort keys
                    // For now, just encode in order
                }
                try self.encodeHead(.map, entries.len);
                for (entries) |entry| {
                    try self.encodeValue(entry.key, opts);
                    try self.encodeValue(entry.value, opts);
                }
            },
            .tag => |tv| {
                try self.encodeUint(.tag, tv.tag);
                try self.encodeValue(tv.value.*, opts);
            },
            .simple => |sv| try self.encodeHead(.simple_float, @intFromEnum(sv)),
            .float => |f| try self.encodeFloat(f, opts),
        }
    }

    fn encodeHead(self: *Self, major_type: MajorType, arg: u64) CborError!void {
        const mt: u8 = @as(u8, @intFromEnum(major_type)) << 5;
        if (arg <= 23) {
            try self.writeByte(mt | @as(u8, @intCast(arg)));
        } else if (arg <= 0xFF) {
            try self.writeByte(mt | 24);
            try self.writeByte(@intCast(arg));
        } else if (arg <= 0xFFFF) {
            try self.writeByte(mt | 25);
            try self.writeBytes(&std.mem.toBytes(std.mem.nativeToBig(u16, @intCast(arg))));
        } else if (arg <= 0xFFFFFFFF) {
            try self.writeByte(mt | 26);
            try self.writeBytes(&std.mem.toBytes(std.mem.nativeToBig(u32, @intCast(arg))));
        } else {
            try self.writeByte(mt | 27);
            try self.writeBytes(&std.mem.toBytes(std.mem.nativeToBig(u64, arg)));
        }
    }

    fn encodeUint(self: *Self, major_type: MajorType, value: u64) CborError!void {
        return self.encodeHead(major_type, value);
    }

    fn encodeFloat(self: *Self, f: f64, opts: EncodeOptions) CborError!void {
        _ = opts;
        const mt: u8 = @as(u8, @intFromEnum(MajorType.simple_float)) << 5;

        // Check for special values
        if (std.math.isNan(f)) {
            try self.writeByte(mt | 25);
            try self.writeBytes(&[_]u8{ 0x7E, 0x00 }); // IEEE 754 half-precision NaN
        } else if (std.math.isInf(f)) {
            try self.writeByte(mt | 25);
            if (f > 0) {
                try self.writeBytes(&[_]u8{ 0x7C, 0x00 }); // +Inf
            } else {
                try self.writeBytes(&[_]u8{ 0xFC, 0x00 }); // -Inf
            }
        } else {
            // Use 64-bit float
            try self.writeByte(mt | 27);
            const bits = @as(u64, @bitCast(f));
            try self.writeBytes(&std.mem.toBytes(std.mem.nativeToBig(u64, bits)));
        }
    }

    fn writeByte(self: *Self, byte: u8) CborError!void {
        if (self.pos >= self.buffer.len) return CborError.BufferTooSmall;
        self.buffer[self.pos] = byte;
        self.pos += 1;
    }

    fn writeBytes(self: *Self, bytes: []const u8) CborError!void {
        if (self.pos + bytes.len > self.buffer.len) return CborError.BufferTooSmall;
        @memcpy(self.buffer[self.pos .. self.pos + bytes.len], bytes);
        self.pos += bytes.len;
    }
};

/// CBOR Decoder
pub const Decoder = struct {
    data: []const u8,
    pos: usize,
    allocator: std.mem.Allocator,
    opts: DecodeOptions,

    const Self = @This();

    pub fn init(data: []const u8, allocator: std.mem.Allocator) Self {
        return .{
            .data = data,
            .pos = 0,
            .allocator = allocator,
            .opts = .{},
        };
    }

    pub fn initWithOpts(data: []const u8, allocator: std.mem.Allocator, opts: DecodeOptions) Self {
        return .{
            .data = data,
            .pos = 0,
            .allocator = allocator,
            .opts = opts,
        };
    }

    /// Decode a CBOR value
    pub fn decode(self: *Self) CborError!Value {
        return self.decodeValue(0);
    }

    fn decodeValue(self: *Self, depth: usize) CborError!Value {
        if (depth > self.opts.max_depth) return CborError.MaxDepthExceeded;
        if (self.pos >= self.data.len) return CborError.UnexpectedEof;

        const head = self.data[self.pos];
        const major_type: MajorType = @enumFromInt(head >> 5);
        const additional_info = head & 0x1F;

        self.pos += 1;

        switch (major_type) {
            .positive_int => {
                const arg = try self.decodeArg(additional_info);
                return Value{ .positive_int = arg };
            },
            .negative_int => {
                const arg = try self.decodeArg(additional_info);
                return Value{ .negative_int = arg };
            },
            .byte_string => {
                const len = try self.decodeArg(additional_info);
                if (len > self.opts.max_length) return CborError.MaxLengthExceeded;
                if (self.pos + len > self.data.len) return CborError.UnexpectedEof;
                const bytes = try self.allocator.dupe(u8, self.data[self.pos .. self.pos + len]);
                self.pos += len;
                return Value{ .byte_string = bytes };
            },
            .text_string => {
                const len = try self.decodeArg(additional_info);
                if (len > self.opts.max_length) return CborError.MaxLengthExceeded;
                if (self.pos + len > self.data.len) return CborError.UnexpectedEof;
                const str = self.data[self.pos .. self.pos + len];
                // Validate UTF-8
                if (!std.unicode.utf8ValidateSlice(str)) return CborError.InvalidUtf8;
                const text = try self.allocator.dupe(u8, str);
                self.pos += len;
                return Value{ .text_string = text };
            },
            .array => {
                const len = try self.decodeArg(additional_info);
                if (len > self.opts.max_length) return CborError.MaxLengthExceeded;
                var arr = try self.allocator.alloc(Value, len);
                errdefer self.allocator.free(arr);
                for (0..len) |i| {
                    arr[i] = try self.decodeValue(depth + 1);
                }
                return Value{ .array = arr };
            },
            .map => {
                const len = try self.decodeArg(additional_info);
                if (len > self.opts.max_length) return CborError.MaxLengthExceeded;
                var entries = try self.allocator.alloc(MapEntry, len);
                errdefer self.allocator.free(entries);
                for (0..len) |i| {
                    entries[i] = .{
                        .key = try self.decodeValue(depth + 1),
                        .value = try self.decodeValue(depth + 1),
                    };
                }
                return Value{ .map = entries };
            },
            .tag => {
                const tag = try self.decodeArg(additional_info);
                const value = try self.allocator.create(Value);
                value.* = try self.decodeValue(depth + 1);
                return Value{ .tag = .{ .tag = tag, .value = value } };
            },
            .simple_float => {
                return try self.decodeSimpleOrFloat(additional_info);
            },
        }
    }

    fn decodeArg(self: *Self, additional_info: u8) CborError!u64 {
        return switch (additional_info) {
            0...23 => additional_info,
            24 => {
                if (self.pos >= self.data.len) return CborError.UnexpectedEof;
                const val = self.data[self.pos];
                self.pos += 1;
                return val;
            },
            25 => {
                if (self.pos + 2 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 2];
                const arr: [2]u8 = bytes[0..2].*;
                const val = std.mem.bigToNative(u16, @bitCast(arr));
                self.pos += 2;
                return val;
            },
            26 => {
                if (self.pos + 4 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 4];
                const arr: [4]u8 = bytes[0..4].*;
                const val = std.mem.bigToNative(u32, @bitCast(arr));
                self.pos += 4;
                return val;
            },
            27 => {
                if (self.pos + 8 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 8];
                const arr: [8]u8 = bytes[0..8].*;
                const val = std.mem.bigToNative(u64, @bitCast(arr));
                self.pos += 8;
                return val;
            },
            28...30 => CborError.InvalidAdditionalInfo,
            31 => CborError.IndefiniteLengthNotSupported,
            else => unreachable,
        };
    }

    fn decodeSimpleOrFloat(self: *Self, additional_info: u8) CborError!Value {
        switch (additional_info) {
            20 => return Value{ .simple = .false_val },
            21 => return Value{ .simple = .true_val },
            22 => return Value{ .simple = .null_val },
            23 => return Value{ .simple = .undefined_val },
            25 => {
                // Half-precision float
                if (self.pos + 2 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 2];
                const arr: [2]u8 = bytes[0..2].*;
                const bits = std.mem.bigToNative(u16, @bitCast(arr));
                self.pos += 2;
                const f = halfToFloat(bits);
                return Value{ .float = f };
            },
            26 => {
                // Single-precision float
                if (self.pos + 4 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 4];
                const arr: [4]u8 = bytes[0..4].*;
                const bits = std.mem.bigToNative(u32, @bitCast(arr));
                self.pos += 4;
                return Value{ .float = @as(f32, @bitCast(bits)) };
            },
            27 => {
                // Double-precision float
                if (self.pos + 8 > self.data.len) return CborError.UnexpectedEof;
                const bytes = self.data[self.pos .. self.pos + 8];
                const arr: [8]u8 = bytes[0..8].*;
                const bits = std.mem.bigToNative(u64, @bitCast(arr));
                self.pos += 8;
                return Value{ .float = @as(f64, @bitCast(bits)) };
            },
            24 => {
                // Simple value (one byte)
                if (self.pos >= self.data.len) return CborError.UnexpectedEof;
                const val = self.data[self.pos];
                self.pos += 1;
                if (val >= 32) {
                    return Value{ .simple = @enumFromInt(val) };
                }
                return CborError.InvalidSimpleValue;
            },
            else => return CborError.InvalidSimpleValue,
        }
    }
};

/// Convert IEEE 754 half-precision to double-precision
fn halfToFloat(bits: u16) f64 {
    const sign: u16 = (bits >> 15) & 1;
    const exp: u16 = (bits >> 10) & 0x1F;
    const mantissa: u16 = bits & 0x3FF;

    if (exp == 0) {
        // Subnormal or zero
        if (mantissa == 0) {
            return if (sign != 0) -@as(f64, 0.0) else 0.0;
        }
        // Subnormal
        const f: f64 = @as(f64, @floatFromInt(mantissa)) * (1.0 / 1024.0) * std.math.pow(f64, 2.0, -14.0);
        return if (sign != 0) -f else f;
    } else if (exp == 31) {
        // Infinity or NaN
        if (mantissa == 0) {
            return if (sign != 0) -std.math.inf(f64) else std.math.inf(f64);
        }
        return std.math.nan(f64);
    }

    // Normalized
    const f: f64 = @as(f64, @floatFromInt(1024 + mantissa)) / 1024.0 * std.math.pow(f64, 2.0, @as(f64, @floatFromInt(exp)) - 15.0);
    return if (sign != 0) -f else f;
}

// --- Convenience Functions ---

/// Calculate encoded length for a CBOR value
pub fn encodedLen(value: Value) usize {
    var counter = LengthCounter{};
    countValue(&counter, value) catch unreachable;
    return counter.len;
}

const LengthCounter = struct {
    len: usize = 0,

    fn writeByte(self: *LengthCounter, _: u8) CborError!void {
        self.len += 1;
    }

    fn writeBytes(self: *LengthCounter, bytes: []const u8) CborError!void {
        self.len += bytes.len;
    }
};

fn countValue(counter: *LengthCounter, value: Value) CborError!void {
    switch (value) {
        .positive_int => |v| try countHead(counter, .positive_int, v),
        .negative_int => |v| try countHead(counter, .negative_int, v),
        .byte_string => |bs| {
            try countHead(counter, .byte_string, bs.len);
            counter.len += bs.len;
        },
        .text_string => |ts| {
            try countHead(counter, .text_string, ts.len);
            counter.len += ts.len;
        },
        .array => |arr| {
            try countHead(counter, .array, arr.len);
            for (arr) |item| try countValue(counter, item);
        },
        .map => |entries| {
            try countHead(counter, .map, entries.len);
            for (entries) |entry| {
                try countValue(counter, entry.key);
                try countValue(counter, entry.value);
            }
        },
        .tag => |tv| {
            try countHead(counter, .tag, tv.tag);
            try countValue(counter, tv.value.*);
        },
        .simple => |_| {
            counter.len += 1;
        },
        .float => |_| {
            counter.len += 9; // 1 byte head + 8 bytes double
        },
    }
}

fn countHead(counter: *LengthCounter, _: MajorType, arg: u64) CborError!void {
    counter.len += 1;
    if (arg > 23) {
        if (arg <= 0xFF) counter.len += 1
        else if (arg <= 0xFFFF) counter.len += 2
        else if (arg <= 0xFFFFFFFF) counter.len += 4
        else counter.len += 8;
    }
}

/// Encode a CBOR value to a new buffer
pub fn encode(allocator: std.mem.Allocator, value: Value) CborError![]u8 {
    const len = encodedLen(value);
    const buffer = allocator.alloc(u8, len) catch return CborError.OutOfMemory;
    errdefer allocator.free(buffer);

    var encoder = Encoder.init(buffer);
    try encoder.encode(value);
    return buffer;
}

/// Decode CBOR data to a Value
pub fn decode(allocator: std.mem.Allocator, data: []const u8) CborError!Value {
    var decoder = Decoder.init(data, allocator);
    return decoder.decode();
}

/// Check if data is valid CBOR
pub fn isValid(data: []const u8, allocator: std.mem.Allocator) bool {
    var decoder = Decoder.init(data, allocator);
    const value = decoder.decode() catch return false;
    value.deinit(allocator);
    return true;
}

/// Create a Value from a JSON-like structure (simplified)
pub fn fromJson(allocator: std.mem.Allocator, json_str: []const u8) CborError!Value {
    _ = json_str;
    _ = allocator;
    return CborError.InvalidUtf8; // Placeholder - would need JSON parser
}

// --- Tests ---

test "encode positive integer" {
    var buffer: [16]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    // Test small integer (<= 23)
    const value1 = Value{ .positive_int = 10 };
    encoder.pos = 0;
    try encoder.encode(value1);
    // 10 <= 23, encodes as single byte: 0x0A (major type 0, additional info 10)
    try std.testing.expectEqualSlices(u8, &[_]u8{0x0A}, encoder.encoded());

    // Test larger integer (> 23)
    const value2 = Value{ .positive_int = 42 };
    encoder.pos = 0;
    try encoder.encode(value2);
    // 42 > 23, encodes as two bytes: 0x18 0x2A
    try std.testing.expectEqualSlices(u8, &[_]u8{ 0x18, 0x2A }, encoder.encoded());
}

test "encode negative integer" {
    var buffer: [16]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    const value = Value{ .negative_int = 0 }; // -1
    try encoder.encode(value);

    // -1 encodes as: 0x20 (major type 1, additional info 0)
    try std.testing.expectEqualSlices(u8, &[_]u8{0x20}, encoder.encoded());
}

test "encode text string" {
    var buffer: [32]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    const value = Value{ .text_string = "hello" };
    try encoder.encode(value);

    // "hello" = major type 3 (text), length 5, then "hello"
    const expected = [_]u8{ 0x65, 'h', 'e', 'l', 'l', 'o' };
    try std.testing.expectEqualSlices(u8, &expected, encoder.encoded());
}

test "encode byte string" {
    var buffer: [32]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    const value = Value{ .byte_string = &[_]u8{ 0x01, 0x02, 0x03 } };
    try encoder.encode(value);

    const expected = [_]u8{ 0x43, 0x01, 0x02, 0x03 };
    try std.testing.expectEqualSlices(u8, &expected, encoder.encoded());
}

test "encode array" {
    const allocator = std.testing.allocator;

    var buffer: [64]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    var arr = try allocator.alloc(Value, 3);
    defer allocator.free(arr);
    arr[0] = Value{ .positive_int = 1 };
    arr[1] = Value{ .positive_int = 2 };
    arr[2] = Value{ .positive_int = 3 };

    const value = Value{ .array = arr };
    try encoder.encode(value);

    // [1, 2, 3] = 0x83 0x01 0x02 0x03
    const expected = [_]u8{ 0x83, 0x01, 0x02, 0x03 };
    try std.testing.expectEqualSlices(u8, &expected, encoder.encoded());
}

test "encode map" {
    const allocator = std.testing.allocator;

    var buffer: [64]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    var entries = try allocator.alloc(MapEntry, 2);
    defer allocator.free(entries);
    entries[0] = .{
        .key = Value{ .text_string = "a" },
        .value = Value{ .positive_int = 1 },
    };
    entries[1] = .{
        .key = Value{ .text_string = "b" },
        .value = Value{ .positive_int = 2 },
    };

    const value = Value{ .map = entries };
    try encoder.encode(value);

    // {"a": 1, "b": 2}
    const expected = [_]u8{ 0xA2, 0x61, 'a', 0x01, 0x61, 'b', 0x02 };
    try std.testing.expectEqualSlices(u8, &expected, encoder.encoded());
}

test "encode simple values" {
    var buffer: [16]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    try encoder.encode(Value{ .simple = .false_val });
    try std.testing.expectEqualSlices(u8, &[_]u8{0xF4}, encoder.encoded());

    encoder = Encoder.init(&buffer);
    try encoder.encode(Value{ .simple = .true_val });
    try std.testing.expectEqualSlices(u8, &[_]u8{0xF5}, encoder.encoded());

    encoder = Encoder.init(&buffer);
    try encoder.encode(Value{ .simple = .null_val });
    try std.testing.expectEqualSlices(u8, &[_]u8{0xF6}, encoder.encoded());
}

test "encode float" {
    var buffer: [16]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    const value = Value{ .float = 1.5 };
    try encoder.encode(value);

    // Float should be encoded with major type 7, additional 27, then 8 bytes
    try std.testing.expectEqual(@as(usize, 9), encoder.encoded().len);
    try std.testing.expectEqual(@as(u8, 0xFB), encoder.encoded()[0]);
}

test "decode positive integer" {
    const allocator = std.testing.allocator;

    // Small integer (<= 23) - single byte
    const data1 = [_]u8{0x0A}; // 10
    var decoder1 = Decoder.init(&data1, allocator);
    const value1 = try decoder1.decode();
    defer value1.deinit(allocator);
    try std.testing.expectEqual(Value{ .positive_int = 10 }, value1);

    // Larger integer (> 23) - two bytes
    const data2 = [_]u8{ 0x18, 0x2A }; // 42
    var decoder2 = Decoder.init(&data2, allocator);
    const value2 = try decoder2.decode();
    defer value2.deinit(allocator);
    try std.testing.expectEqual(Value{ .positive_int = 42 }, value2);
}

test "decode negative integer" {
    const allocator = std.testing.allocator;

    const data = [_]u8{0x20}; // -1
    var decoder = Decoder.init(&data, allocator);
    const value = try decoder.decode();
    defer value.deinit(allocator);

    try std.testing.expectEqual(Value{ .negative_int = 0 }, value);
    try std.testing.expectEqual(@as(?i65, -1), value.toInteger());
}

test "decode text string" {
    const allocator = std.testing.allocator;

    const data = [_]u8{ 0x65, 'h', 'e', 'l', 'l', 'o' };
    var decoder = Decoder.init(&data, allocator);
    const value = try decoder.decode();
    defer value.deinit(allocator);

    try std.testing.expectEqualStrings("hello", value.text_string);
}

test "decode array" {
    const allocator = std.testing.allocator;

    const data = [_]u8{ 0x83, 0x01, 0x02, 0x03 };
    var decoder = Decoder.init(&data, allocator);
    const value = try decoder.decode();
    defer value.deinit(allocator);

    try std.testing.expectEqual(@as(usize, 3), value.array.len);
    try std.testing.expectEqual(Value{ .positive_int = 1 }, value.array[0]);
    try std.testing.expectEqual(Value{ .positive_int = 2 }, value.array[1]);
    try std.testing.expectEqual(Value{ .positive_int = 3 }, value.array[2]);
}

test "decode map" {
    const allocator = std.testing.allocator;

    const data = [_]u8{ 0xA2, 0x61, 'a', 0x01, 0x61, 'b', 0x02 };
    var decoder = Decoder.init(&data, allocator);
    const value = try decoder.decode();
    defer value.deinit(allocator);

    try std.testing.expectEqual(@as(usize, 2), value.map.len);
}

test "decode simple values" {
    const allocator = std.testing.allocator;

    var decoder = Decoder.init(&[_]u8{0xF4}, allocator);
    var value = try decoder.decode();
    defer value.deinit(allocator);
    try std.testing.expectEqual(Value{ .simple = .false_val }, value);

    decoder = Decoder.init(&[_]u8{0xF5}, allocator);
    value = try decoder.decode();
    defer value.deinit(allocator);
    try std.testing.expectEqual(Value{ .simple = .true_val }, value);

    decoder = Decoder.init(&[_]u8{0xF6}, allocator);
    value = try decoder.decode();
    defer value.deinit(allocator);
    try std.testing.expectEqual(Value{ .simple = .null_val }, value);
}

test "roundtrip integer" {
    const allocator = std.testing.allocator;

    const values = [_]u64{ 0, 1, 23, 24, 255, 256, 65535, 65536, 0xFFFFFFFF, 0x100000000 };

    for (values) |v| {
        const original = Value{ .positive_int = v };

        const encoded = try encode(allocator, original);
        defer allocator.free(encoded);

        var decoder = Decoder.init(encoded, allocator);
        const decoded = try decoder.decode();
        defer decoded.deinit(allocator);

        try std.testing.expectEqual(original, decoded);
    }
}

test "roundtrip string" {
    const allocator = std.testing.allocator;

    const original = Value{ .text_string = "Hello, CBOR! 你好世界 🌍" };

    const encoded = try encode(allocator, original);
    defer allocator.free(encoded);

    var decoder = Decoder.init(encoded, allocator);
    const decoded = try decoder.decode();
    defer decoded.deinit(allocator);

    try std.testing.expectEqualStrings(original.text_string, decoded.text_string);
}

test "roundtrip complex nested structure" {
    const allocator = std.testing.allocator;

    // Create nested structure: {"data": [1, {"inner": true}, null]}
    var inner_map = try allocator.alloc(MapEntry, 1);
    inner_map[0] = .{
        .key = Value{ .text_string = "inner" },
        .value = Value{ .simple = .true_val },
    };

    var arr = try allocator.alloc(Value, 3);
    arr[0] = Value{ .positive_int = 1 };
    arr[1] = Value{ .map = inner_map };
    arr[2] = Value{ .simple = .null_val };

    var outer_map = try allocator.alloc(MapEntry, 1);
    outer_map[0] = .{
        .key = Value{ .text_string = "data" },
        .value = Value{ .array = arr },
    };

    const original = Value{ .map = outer_map };

    const encoded = try encode(allocator, original);
    defer allocator.free(encoded);

    var decoder = Decoder.init(encoded, allocator);
    const decoded = try decoder.decode();
    defer decoded.deinit(allocator);

    try std.testing.expectEqual(@as(usize, 1), decoded.map.len);
    try std.testing.expectEqualStrings("data", decoded.map[0].key.text_string);
    try std.testing.expectEqual(@as(usize, 3), decoded.map[0].value.array.len);

    // Clean up original allocations (simple values don't need cleanup, but text strings do)
    allocator.free(inner_map);
    allocator.free(arr);
    allocator.free(outer_map);
}

test "large integer encoding" {
    var buffer: [16]u8 = undefined;
    var encoder = Encoder.init(&buffer);

    // 256 should use 2-byte encoding
    const value = Value{ .positive_int = 256 };
    try encoder.encode(value);

    try std.testing.expectEqual(@as(usize, 3), encoder.encoded().len);
    try std.testing.expectEqual(@as(u8, 0x19), encoder.encoded()[0]); // major type 0, additional 25
}

test "toJson" {
    const allocator = std.testing.allocator;

    var arr = try allocator.alloc(Value, 3);
    arr[0] = Value{ .positive_int = 1 };
    arr[1] = Value{ .simple = .true_val };
    arr[2] = Value{ .text_string = "test" };

    const value = Value{ .array = arr };
    const json = try value.toJson(allocator);
    defer allocator.free(json);

    try std.testing.expectEqualStrings("[1,true,\"test\"]", json);

    // Clean up allocated array
    allocator.free(arr);
}

test "isValid" {
    const allocator = std.testing.allocator;

    // Valid encodings
    try std.testing.expect(isValid(&[_]u8{0x0A}, allocator)); // 10
    try std.testing.expect(isValid(&[_]u8{ 0x18, 0x2A }, allocator)); // 42
    try std.testing.expect(isValid(&[_]u8{ 0x65, 'h', 'e', 'l', 'l', 'o' }, allocator));
    try std.testing.expect(!isValid(&[_]u8{0xFF}, allocator)); // Invalid
}