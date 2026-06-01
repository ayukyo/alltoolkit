const std = @import("std");
const json_patch = @import("json_patch");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();
    const stderr = std.io.getStdErr().writer();

    const doc =
        \\{
        \\  "name": "Alice",
        \\  "age": 30,
        \\  "email": "alice@example.com",
        \\  "tags": ["admin", "user"]
        \\}
    ;

    const patch =
        \\[{"op": "replace", "path": "/name", "value": "Bob"},
        \\ {"op": "add", "path": "/city", "value": "Paris"},
        \\ {"op": "remove", "path": "/email"},
        \\ {"op": "add", "path": "/tags/-", "value": "vip"}]
    ;

    try stdout.print("=== Basic JSON Patch Example ===\n\n", .{});
    try stdout.print("Original document:\n{s}\n\n", .{doc});
    try stdout.print("Patch operations:\n{s}\n\n", .{patch});

    const result = json_patch.apply(allocator, doc, patch) catch |err| {
        try stderr.print("Error: {any}\n", .{err});
        return err;
    };
    defer allocator.free(result);

    try stdout.print("Patched document:\n{s}\n", .{result});
}
