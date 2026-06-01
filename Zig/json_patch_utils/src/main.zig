const std = @import("std");
const json = std.json;

pub const PatchError = error{
    InvalidJson,
    InvalidPatch,
    InvalidPath,
    InvalidIndex,
    PathNotFound,
    OutOfMemory,
    NotAnArray,
    NotAnObject,
    TestFailed,
};

/// RFC 6902 JSON Patch operations
pub const Op = enum {
    add,
    remove,
    replace,
    move,
    copy,
    @"test",
};

/// Single patch operation. The owning `Patch` is responsible for freeing all
/// owned memory via `Patch.deinit()`. Values stored here are deep-cloned from
/// the source JSON during parsing.
pub const Operation = struct {
    op: Op,
    path: []const u8,
    from: ?[]const u8,
    value: json.Value,
};

/// JSON Patch document (ordered list of operations).
pub const Patch = struct {
    ops: []Operation,
    arena: std.heap.ArenaAllocator,

    pub fn deinit(self: *Patch) void {
        self.arena.deinit();
        self.* = undefined;
    }
};

/// Recursively free all heap memory owned by a json.Value.
pub fn jsonValueFree(allocator: std.mem.Allocator, value: json.Value) void {
    var mut: json.Value = value;
    freeInPlace(allocator, &mut);
}

fn freeInPlace(allocator: std.mem.Allocator, value: *json.Value) void {
    switch (value.*) {
        .string => |s| allocator.free(s),
        .number_string => |s| allocator.free(s),
        .array => |*arr| {
            for (arr.items) |item| freeInPlace(allocator, @constCast(&item));
            arr.deinit();
        },
        .object => |*obj| {
            var it = obj.iterator();
            while (it.next()) |entry| {
                allocator.free(entry.key_ptr.*);
                freeInPlace(allocator, @constCast(entry.value_ptr));
            }
            obj.deinit();
        },
        else => {},
    }
}

/// Deep-clone a json.Value into a fresh allocation. Strings/arrays/maps are
/// fully duplicated so the clone has independent lifetime.
pub fn deepCloneValue(allocator: std.mem.Allocator, value: json.Value) !json.Value {
    return switch (value) {
        .null => json.Value{ .null = {} },
        .bool => |b| json.Value{ .bool = b },
        .integer => |i| json.Value{ .integer = i },
        .float => |f| json.Value{ .float = f },
        .number_string => |ns| json.Value{ .number_string = try allocator.dupe(u8, ns) },
        .string => |s| json.Value{ .string = try allocator.dupe(u8, s) },
        .array => |arr| blk: {
            var new_arr = std.json.Array.init(allocator);
            errdefer new_arr.deinit();
            for (arr.items) |item| {
                const cloned = try deepCloneValue(allocator, item);
                errdefer jsonValueFree(allocator, cloned);
                try new_arr.append(cloned);
            }
            break :blk json.Value{ .array = new_arr };
        },
        .object => |obj| blk: {
            var new_obj = std.json.ObjectMap.init(allocator);
            errdefer {
                var it = new_obj.iterator();
                while (it.next()) |entry| {
                    _ = entry.key_ptr.*;
                    jsonValueFree(allocator, entry.value_ptr.*);
                }
                new_obj.deinit();
            }
            var it = obj.iterator();
            while (it.next()) |entry| {
                const key_dup = try allocator.dupe(u8, entry.key_ptr.*);
                errdefer allocator.free(key_dup);
                const val_dup = try deepCloneValue(allocator, entry.value_ptr.*);
                errdefer jsonValueFree(allocator, val_dup);
                // The hashmap does NOT take ownership of the key's memory; the
                // caller (us) must keep `key_dup` alive for the lifetime of
                // the map. We leak it here; it will be freed by
                // `jsonValueFree` -> `freeInPlace` which iterates and frees
                // each key.
                try new_obj.put(key_dup, val_dup);
            }
            break :blk json.Value{ .object = new_obj };
        },
    };
}

/// Structural equality on json.Value. Object key order-insensitive.
/// Integer and float are cross-comparable.
pub fn jsonEql(a: json.Value, b: json.Value) bool {
    const Tag = std.meta.Tag(json.Value);
    if (@as(Tag, a) != @as(Tag, b)) {
        const a_num = a == .integer or a == .float;
        const b_num = b == .integer or b == .float;
        if (!(a_num and b_num)) return false;
    }
    return switch (a) {
        .null => true,
        .bool => |av| b == .bool and av == b.bool,
        .integer => |av| switch (b) {
            .integer => av == b.integer,
            .float => @as(f64, @floatFromInt(av)) == b.float,
            else => false,
        },
        .float => |av| switch (b) {
            .float => av == b.float,
            .integer => av == @as(f64, @floatFromInt(b.integer)),
            else => false,
        },
        .number_string => |av| b == .number_string and std.mem.eql(u8, av, b.number_string),
        .string => |av| b == .string and std.mem.eql(u8, av, b.string),
        .array => |av| blk: {
            if (b != .array) break :blk false;
            if (av.items.len != b.array.items.len) break :blk false;
            for (av.items, 0..) |item, i| {
                if (!jsonEql(item, b.array.items[i])) break :blk false;
            }
            break :blk true;
        },
        .object => |av| blk: {
            if (b != .object) break :blk false;
            if (av.count() != b.object.count()) break :blk false;
            var it = av.iterator();
            while (it.next()) |entry| {
                const other = b.object.get(entry.key_ptr.*) orelse break :blk false;
                if (!jsonEql(entry.value_ptr.*, other)) break :blk false;
            }
            break :blk true;
        },
    };
}

/// Walk a JSON Pointer from root, returning the parent of the final segment
/// and the unescaped final key. The returned `last_key` is owned by `arena`
/// and freed when the arena is destroyed.
fn walkPointerArena(root: *json.Value, pointer: []const u8, arena: std.mem.Allocator) PatchError!struct {
    parent: *json.Value,
    last_key: []const u8,
} {
    if (pointer.len == 0 or pointer[0] != '/') return PatchError.InvalidPath;

    var current: *json.Value = root;
    var i: usize = 1;

    while (true) {
        var j: usize = i;
        while (j < pointer.len and pointer[j] != '/') : (j += 1) {}

        const raw = pointer[i..j];
        const unescaped = try unescapePointerSegment(arena, raw);

        if (j == pointer.len) {
            return .{ .parent = current, .last_key = unescaped };
        }

        const next = resolvePointer(current, unescaped) catch return PatchError.PathNotFound;
        current = next;
        i = j + 1;
    }
}

/// Unescape a single JSON Pointer segment: `~1` -> `/`, `~0` -> `~`.
/// Returns a slice that is exactly the right length (always <= raw.len).
fn unescapePointerSegment(allocator: std.mem.Allocator, raw: []const u8) ![]u8 {
    var out = try allocator.alloc(u8, raw.len);
    var in_i: usize = 0;
    var out_i: usize = 0;
    while (in_i < raw.len) {
        if (raw[in_i] == '~' and in_i + 1 < raw.len) {
            if (raw[in_i + 1] == '0') {
                out[out_i] = '~';
                in_i += 2;
                out_i += 1;
                continue;
            } else if (raw[in_i + 1] == '1') {
                out[out_i] = '/';
                in_i += 2;
                out_i += 1;
                continue;
            }
        }
        out[out_i] = raw[in_i];
        in_i += 1;
        out_i += 1;
    }
    return out[0..out_i];
}

/// Resolve a single key/index into the immediate parent (one level deep).
fn resolvePointer(parent: *json.Value, key: []const u8) PatchError!*json.Value {
    return switch (parent.*) {
        .object => |*obj| blk: {
            var it = obj.iterator();
            while (it.next()) |entry| {
                if (std.mem.eql(u8, entry.key_ptr.*, key)) break :blk &entry.value_ptr.*;
            }
            return PatchError.PathNotFound;
        },
        .array => |*arr| blk: {
            if (std.mem.eql(u8, key, "-")) return PatchError.PathNotFound;
            const idx = std.fmt.parseInt(usize, key, 10) catch return PatchError.InvalidIndex;
            if (idx >= arr.items.len) return PatchError.PathNotFound;
            break :blk &arr.items[idx];
        },
        else => PatchError.PathNotFound,
    };
}

/// Parse a single patch operation from a JSON object value.
fn parseOperation(allocator: std.mem.Allocator, value: json.Value) PatchError!Operation {
    if (value != .object) return PatchError.InvalidPatch;
    const obj = value.object;

    const op_val = obj.get("op") orelse return PatchError.InvalidPatch;
    if (op_val != .string) return PatchError.InvalidPatch;
    const op = std.meta.stringToEnum(Op, op_val.string) orelse return PatchError.InvalidPatch;

    const path_val = obj.get("path") orelse return PatchError.InvalidPatch;
    if (path_val != .string) return PatchError.InvalidPatch;
    const path = try allocator.dupe(u8, path_val.string);

    var from_dup: ?[]const u8 = null;
    if (obj.get("from")) |from_val| {
        if (from_val != .string) return PatchError.InvalidPatch;
        from_dup = try allocator.dupe(u8, from_val.string);
    }

    var value_clone: json.Value = .null;
    if (op == .add or op == .replace or op == .@"test") {
        const v = obj.get("value") orelse return PatchError.InvalidPatch;
        value_clone = try deepCloneValue(allocator, v);
    }

    return .{
        .op = op,
        .path = path,
        .from = from_dup,
        .value = value_clone,
    };
}

/// Parse a JSON Patch from a JSON array string. The returned `Patch` uses
/// an internal arena allocator; call `patch.deinit()` to free.
pub fn parsePatch(allocator: std.mem.Allocator, patch_text: []const u8) PatchError!Patch {
    var arena = std.heap.ArenaAllocator.init(allocator);
    errdefer arena.deinit();
    const aa = arena.allocator();

    var parsed = json.parseFromSlice(json.Value, aa, patch_text, .{}) catch {
        return PatchError.InvalidJson;
    };
    defer parsed.deinit();

    if (parsed.value != .array) return PatchError.InvalidPatch;
    const arr = parsed.value.array;

    var ops = try aa.alloc(Operation, arr.items.len);
    for (arr.items, 0..) |item, i| {
        ops[i] = try parseOperation(aa, item);
    }

    return .{ .ops = ops, .arena = arena };
}

/// Apply a single operation to the document (mutates in place). The
/// `doc_arena` allocator is used to allocate the unescaped pointer segment
/// strings and key duplicates; these are released when the arena is
/// destroyed.
pub fn applyOp(doc_arena: std.mem.Allocator, root: *json.Value, op: Operation) PatchError!void {
    switch (op.op) {
        .add => {
            const walk = try walkPointerArena(root, op.path, doc_arena);
            switch (walk.parent.*) {
                .object => |*obj| {
                    const key_dup = try doc_arena.dupe(u8, walk.last_key);
                    try obj.put(key_dup, op.value);
                },
                .array => |*arr| {
                    if (std.mem.eql(u8, walk.last_key, "-")) {
                        try arr.append(op.value);
                    } else {
                        const idx = std.fmt.parseInt(usize, walk.last_key, 10) catch {
                            return PatchError.InvalidIndex;
                        };
                        if (idx > arr.items.len) return PatchError.InvalidIndex;
                        try arr.insert(idx, op.value);
                    }
                },
                else => return PatchError.PathNotFound,
            }
        },
        .remove => {
            const walk = try walkPointerArena(root, op.path, doc_arena);
            switch (walk.parent.*) {
                .object => |*obj| {
                    _ = obj.fetchSwapRemove(walk.last_key) orelse return PatchError.PathNotFound;
                },
                .array => |*arr| {
                    const idx = std.fmt.parseInt(usize, walk.last_key, 10) catch {
                        return PatchError.InvalidIndex;
                    };
                    if (idx >= arr.items.len) return PatchError.InvalidIndex;
                    _ = arr.orderedRemove(idx);
                },
                else => return PatchError.PathNotFound,
            }
        },
        .replace => {
            const walk = try walkPointerArena(root, op.path, doc_arena);
            switch (walk.parent.*) {
                .object => |*obj| {
                    const entry = obj.getPtr(walk.last_key) orelse return PatchError.PathNotFound;
                    entry.* = op.value;
                },
                .array => |*arr| {
                    const idx = std.fmt.parseInt(usize, walk.last_key, 10) catch {
                        return PatchError.InvalidIndex;
                    };
                    if (idx >= arr.items.len) return PatchError.InvalidIndex;
                    arr.items[idx] = op.value;
                },
                else => return PatchError.PathNotFound,
            }
        },
        .move => {
            const from_ptr = op.from orelse return PatchError.InvalidPatch;
            const walk_from = try walkPointerArena(root, from_ptr, doc_arena);
            const walk_to = try walkPointerArena(root, op.path, doc_arena);

            var val: json.Value = .null;
            switch (walk_from.parent.*) {
                .object => |*obj| {
                    const entry = obj.fetchSwapRemove(walk_from.last_key) orelse return PatchError.PathNotFound;
                    val = entry.value;
                },
                .array => |*arr| {
                    const idx = std.fmt.parseInt(usize, walk_from.last_key, 10) catch {
                        return PatchError.InvalidPatch;
                    };
                    if (idx >= arr.items.len) return PatchError.PathNotFound;
                    val = arr.orderedRemove(idx);
                },
                else => return PatchError.PathNotFound,
            }

            switch (walk_to.parent.*) {
                .object => |*obj| {
                    const key_dup = try doc_arena.dupe(u8, walk_to.last_key);
                    try obj.put(key_dup, val);
                },
                .array => |*arr| {
                    if (std.mem.eql(u8, walk_to.last_key, "-")) {
                        try arr.append(val);
                    } else {
                        const idx = std.fmt.parseInt(usize, walk_to.last_key, 10) catch {
                            return PatchError.InvalidIndex;
                        };
                        if (idx > arr.items.len) return PatchError.InvalidIndex;
                        try arr.insert(idx, val);
                    }
                },
                else => return PatchError.PathNotFound,
            }
        },
        .copy => {
            const from_ptr = op.from orelse return PatchError.InvalidPatch;
            const walk_from = try walkPointerArena(root, from_ptr, doc_arena);
            const walk_to = try walkPointerArena(root, op.path, doc_arena);

            const src = resolvePointer(walk_from.parent, walk_from.last_key) catch {
                return PatchError.PathNotFound;
            };
            // Insert a shallow reference; the document arena owns all the
            // strings/arrays/maps and will free them in one go.
            switch (walk_to.parent.*) {
                .object => |*obj| {
                    const key_dup = try doc_arena.dupe(u8, walk_to.last_key);
                    try obj.put(key_dup, src.*);
                },
                .array => |*arr| {
                    if (std.mem.eql(u8, walk_to.last_key, "-")) {
                        try arr.append(src.*);
                    } else {
                        const idx = std.fmt.parseInt(usize, walk_to.last_key, 10) catch {
                            return PatchError.InvalidIndex;
                        };
                        if (idx > arr.items.len) return PatchError.InvalidIndex;
                        try arr.insert(idx, src.*);
                    }
                },
                else => return PatchError.PathNotFound,
            }
        },
        .@"test" => {
            const walk = try walkPointerArena(root, op.path, doc_arena);
            const actual = resolvePointer(walk.parent, walk.last_key) catch {
                return PatchError.TestFailed;
            };
            if (!jsonEql(actual.*, op.value)) return PatchError.TestFailed;
        },
    }
}

/// Apply a parsed patch to a parsed JSON document (mutates `doc` in place).
/// `doc_arena` is the allocator used to back the document (typically the arena
/// returned by `json.parseFromSlice`).
pub fn applyPatch(doc_arena: std.mem.Allocator, doc: *json.Value, patch: Patch) PatchError!void {
    for (patch.ops) |op| {
        try applyOp(doc_arena, doc, op);
    }
}

/// Convenience: parse doc text, parse patch text, apply, return the JSON text
/// (pretty-printed with 2-space indent). Caller owns the returned slice.
pub fn apply(allocator: std.mem.Allocator, doc_text: []const u8, patch_text: []const u8) PatchError![]u8 {
    var doc_parsed = json.parseFromSlice(json.Value, allocator, doc_text, .{}) catch {
        return PatchError.InvalidJson;
    };
    defer doc_parsed.deinit();

    var patch = try parsePatch(allocator, patch_text);
    defer patch.deinit();

    try applyPatch(doc_parsed.arena.allocator(), &doc_parsed.value, patch);

    var out: std.ArrayListUnmanaged(u8) = .{};
    errdefer out.deinit(allocator);
    try json.stringify(doc_parsed.value, .{ .whitespace = .indent_2 }, out.writer(allocator));
    return out.toOwnedSlice(allocator);
}

// ----------------------- Tests -----------------------

test "add to object" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"foo": "bar"}
    ;
    const patch_text =
        \\[{"op": "add", "path": "/baz", "value": "qux"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"baz\": \"qux\"") != null);
}

test "remove from object" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"foo": "bar", "baz": "qux"}
    ;
    const patch_text =
        \\[{"op": "remove", "path": "/baz"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "baz") == null);
}

test "replace value" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"foo": "bar"}
    ;
    const patch_text =
        \\[{"op": "replace", "path": "/foo", "value": "baz"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"foo\": \"baz\"") != null);
}

test "add to array" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\["a", "b"]
    ;
    const patch_text =
        \\[{"op": "add", "path": "/1", "value": "c"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"a\"") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"b\"") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"c\"") != null);
}

test "add append to array with -" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\["a", "b"]
    ;
    const patch_text =
        \\[{"op": "add", "path": "/-", "value": "c"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"c\"") != null);
}

test "move" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"a": 1, "b": 2}
    ;
    const patch_text =
        \\[{"op": "move", "from": "/a", "path": "/c"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"a\": 1") == null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"c\": 1") != null);
}

test "copy" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"a": 1}
    ;
    const patch_text =
        \\[{"op": "copy", "from": "/a", "path": "/b"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"a\": 1") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"b\": 1") != null);
}

test "test success" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"foo": "bar"}
    ;
    const patch_text =
        \\[{"op": "test", "path": "/foo", "value": "bar"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"foo\": \"bar\"") != null);
}

test "test failure" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"foo": "bar"}
    ;
    const patch_text =
        \\[{"op": "test", "path": "/foo", "value": "baz"}]
    ;
    const result = apply(allocator, doc_text, patch_text);
    try std.testing.expectError(PatchError.TestFailed, result);
}

test "escape ~0 and ~1 in pointer" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"a/b": 1, "c~d": 2}
    ;
    const patch_text =
        \\[{"op": "replace", "path": "/a~1b", "value": 10}, {"op": "replace", "path": "/c~0d", "value": 20}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"a/b\": 10") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"c~d\": 20") != null);
}

test "multiple operations in sequence" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"name": "alice", "age": 30}
    ;
    const patch_text =
        \\[{"op": "replace", "path": "/name", "value": "bob"}, {"op": "add", "path": "/city", "value": "Paris"}, {"op": "remove", "path": "/age"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"bob\"") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"Paris\"") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"age\"") == null);
}

test "nested object modifications" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"user": {"name": "alice", "tags": ["admin", "user"]}}
    ;
    const patch_text =
        \\[{"op": "replace", "path": "/user/name", "value": "bob"}, {"op": "add", "path": "/user/tags/-", "value": "vip"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"bob\"") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "\"vip\"") != null);
}

test "json equality" {
    const allocator = std.testing.allocator;
    var a_parsed = try json.parseFromSlice(json.Value, allocator, "{\"x\": 1}", .{});
    defer a_parsed.deinit();
    var b_parsed = try json.parseFromSlice(json.Value, allocator, "{\"x\": 1}", .{});
    defer b_parsed.deinit();
    try std.testing.expect(jsonEql(a_parsed.value, b_parsed.value));
}

test "json equality different types" {
    const allocator = std.testing.allocator;
    var a_parsed = try json.parseFromSlice(json.Value, allocator, "{\"x\": 1}", .{});
    defer a_parsed.deinit();
    var b_parsed = try json.parseFromSlice(json.Value, allocator, "{\"x\": \"1\"}", .{});
    defer b_parsed.deinit();
    try std.testing.expect(!jsonEql(a_parsed.value, b_parsed.value));
}

test "json equality int vs float" {
    const allocator = std.testing.allocator;
    var a_parsed = try json.parseFromSlice(json.Value, allocator, "1", .{});
    defer a_parsed.deinit();
    var b_parsed = try json.parseFromSlice(json.Value, allocator, "1.0", .{});
    defer b_parsed.deinit();
    try std.testing.expect(jsonEql(a_parsed.value, b_parsed.value));
}

test "invalid patch op" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{}
    ;
    const patch_text =
        \\[{"op": "frobnicate", "path": "/foo"}]
    ;
    const result = apply(allocator, doc_text, patch_text);
    try std.testing.expectError(PatchError.InvalidPatch, result);
}

test "add missing value" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{}
    ;
    const patch_text =
        \\[{"op": "add", "path": "/foo"}]
    ;
    const result = apply(allocator, doc_text, patch_text);
    try std.testing.expectError(PatchError.InvalidPatch, result);
}

test "remove nonexistent path" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"a": 1}
    ;
    const patch_text =
        \\[{"op": "remove", "path": "/b"}]
    ;
    const result = apply(allocator, doc_text, patch_text);
    try std.testing.expectError(PatchError.PathNotFound, result);
}

test "deep clone preserves value" {
    const allocator = std.testing.allocator;
    var parsed = try json.parseFromSlice(json.Value, allocator, "{\"x\": [1, 2, 3]}", .{});
    defer parsed.deinit();

    const cloned = try deepCloneValue(allocator, parsed.value);
    defer jsonValueFree(allocator, cloned);

    try std.testing.expect(jsonEql(parsed.value, cloned));
}

test "copy into array append" {
    const allocator = std.testing.allocator;
    const doc_text =
        \\{"a": [1, 2], "b": 99}
    ;
    const patch_text =
        \\[{"op": "copy", "from": "/b", "path": "/a/-"}]
    ;
    const result = try apply(allocator, doc_text, patch_text);
    defer allocator.free(result);
    try std.testing.expect(std.mem.indexOf(u8, result, "1") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "2") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "99") != null);
}
