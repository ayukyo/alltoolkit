const std = @import("std");
const json_patch = @import("json_patch");
const json = std.json;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();
    const stderr = std.io.getStdErr().writer();

    try stdout.print("=== Advanced JSON Patch Example ===\n\n", .{});

    // ---- Example 1: move / copy ----
    {
        const doc =
            \\{"a": 1, "b": 2, "c": 3}
        ;
        const patch =
            \\[{"op": "copy", "from": "/a", "path": "/a_copy"},
            \\ {"op": "move", "from": "/b", "path": "/b_moved"}]
        ;
        try stdout.print("-- copy + move --\n", .{});
        try stdout.print("doc:    {s}\n", .{doc});
        try stdout.print("patch:  {s}\n", .{patch});
        const result = try json_patch.apply(allocator, doc, patch);
        defer allocator.free(result);
        try stdout.print("result: {s}\n\n", .{result});
    }

    // ---- Example 2: test (rollback on failure) ----
    {
        const doc =
            \\{"version": 1, "data": [1, 2, 3]}
        ;
        const patch =
            \\[{"op": "test", "path": "/version", "value": 1},
            \\ {"op": "replace", "path": "/version", "value": 2},
            \\ {"op": "add", "path": "/updated", "value": true}]
        ;
        try stdout.print("-- test + replace + add --\n", .{});
        const result = try json_patch.apply(allocator, doc, patch);
        defer allocator.free(result);
        try stdout.print("result: {s}\n\n", .{result});
    }

    // ---- Example 3: escaped JSON pointer (~0 = ~, ~1 = /) ----
    {
        const doc =
            \\{"a/b": "old", "c~d": "old"}
        ;
        const patch =
            \\[{"op": "replace", "path": "/a~1b", "value": "new1"},
            \\ {"op": "replace", "path": "/c~0d", "value": "new2"}]
        ;
        try stdout.print("-- escaped pointer --\n", .{});
        try stdout.print("doc:    {s}\n", .{doc});
        const result = try json_patch.apply(allocator, doc, patch);
        defer allocator.free(result);
        try stdout.print("result: {s}\n\n", .{result});
    }

    // ---- Example 4: error on failing test ----
    {
        const doc =
            \\{"x": 1}
        ;
        const patch =
            \\[{"op": "test", "path": "/x", "value": 999}]
        ;
        try stdout.print("-- test failure --\n", .{});
        if (json_patch.apply(allocator, doc, patch)) |_| {
            try stderr.print("ERROR: should have failed\n", .{});
        } else |err| {
            try stdout.print("caught expected error: {any}\n\n", .{err});
        }
    }

    // ---- Example 5: low-level parse / applyPatch with reuse ----
    {
        const doc_text =
            \\{"items": [{"id": 1}, {"id": 2}]}
        ;
        const patch_text =
            \\[{"op": "add", "path": "/items/-", "value": {"id": 3}}]
        ;
        try stdout.print("-- low-level parse/applyPatch --\n", .{});

        var doc_parsed = try json.parseFromSlice(json.Value, allocator, doc_text, .{});
        defer doc_parsed.deinit();

        var patch = try json_patch.parsePatch(allocator, patch_text);
        defer patch.deinit();

        try json_patch.applyPatch(doc_parsed.arena.allocator(), &doc_parsed.value, patch);

        var out: std.ArrayListUnmanaged(u8) = .{};
        defer out.deinit(allocator);
        try json.stringify(doc_parsed.value, .{ .whitespace = .indent_2 }, out.writer(allocator));

        try stdout.print("result: {s}\n", .{out.items});
    }
}
