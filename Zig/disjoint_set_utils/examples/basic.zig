const std = @import("std");
const DisjointSet = @import("disjoint_set").DisjointSet;

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Disjoint Set (Union-Find) Basic Example ===\n\n", .{});

    // Create a disjoint set with 10 elements
    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 });
    defer ds.deinit();

    try stdout.print("Initial state: 10 separate sets\n", .{});
    try stdout.print("Set count: {}\n\n", .{ds.countSets()});

    // Union operations
    try stdout.print("Performing unions...\n", .{});

    _ = ds.unionSets(0, 1); // 1-2
    try stdout.print("  Union(1, 2): {} sets\n", .{ds.countSets()});

    _ = ds.unionSets(2, 3); // 3-4
    try stdout.print("  Union(3, 4): {} sets\n", .{ds.countSets()});

    _ = ds.unionSets(0, 2); // 1-2-3-4
    try stdout.print("  Union(1, 3): {} sets\n", .{ds.countSets()});

    _ = ds.unionSets(4, 5); // 5-6
    _ = ds.unionSets(6, 7); // 7-8
    _ = ds.unionSets(4, 6); // 5-6-7-8
    try stdout.print("  Union(5, 6, 7, 8): {} sets\n\n", .{ds.countSets()});

    // Check connectivity
    try stdout.print("Connectivity checks:\n", .{});
    try stdout.print("  1 connected to 4: {}\n", .{ds.connected(0, 3)});
    try stdout.print("  1 connected to 5: {}\n", .{ds.connected(0, 4)});
    try stdout.print("  5 connected to 8: {}\n", .{ds.connected(4, 7)});
    try stdout.print("  9 connected to 10: {}\n\n", .{ds.connected(8, 9)});

    // Get set members
    try stdout.print("Set members:\n", .{});
    const set_members = try ds.getSetMembers(allocator, 0);
    defer allocator.free(set_members);

    try stdout.print("  Set containing 1: ", .{});
    for (set_members) |val| {
        try stdout.print("{} ", .{val});
    }
    try stdout.print("\n\n", .{});

    // Show all sets
    const all_sets = try ds.getAllSets(allocator);
    defer {
        for (all_sets) |set| {
            allocator.free(set);
        }
        allocator.free(all_sets);
    }

    try stdout.print("All sets:\n", .{});
    for (all_sets, 1..) |set, i| {
        try stdout.print("  Set {}: ", .{i});
        for (set) |val| {
            try stdout.print("{} ", .{val});
        }
        try stdout.print("\n", .{});
    }

    // Reset demonstration
    try stdout.print("\nResetting all elements...\n", .{});
    ds.reset();
    try stdout.print("Set count after reset: {}\n", .{ds.countSets()});
}