const std = @import("std");
const DisjointSet = @import("disjoint_set").DisjointSet;

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Network Connectivity Example ===\n\n", .{});

    // Simulate network nodes
    const nodes = [_][]const u8{ "Server A", "Server B", "Server C", "Server D", "Server E", "Server F" };
    var ds = try DisjointSet(usize).initRange(allocator, nodes.len);
    defer ds.deinit();

    try stdout.print("Network has {} servers\n", .{nodes.len});
    try stdout.print("Initial connected components: {}\n\n", .{ds.countSets()});

    // Define network connections
    const connections = [_][2]usize{
        .{ 0, 1 }, // A - B
        .{ 1, 2 }, // B - C
        .{ 3, 4 }, // D - E
    };

    try stdout.print("Establishing connections:\n", .{});
    for (connections) |conn| {
        const added = ds.unionSets(conn[0], conn[1]);
        if (added) {
            try stdout.print("  {s} <-> {s}: Connected\n", .{ nodes[conn[0]], nodes[conn[1]] });
        }
    }

    try stdout.print("\nConnected components: {}\n\n", .{ds.countSets()});

    // Check connectivity between servers
    const queries = [_][2]usize{
        .{ 0, 2 }, // A - C
        .{ 0, 3 }, // A - D
        .{ 3, 4 }, // D - E
        .{ 4, 5 }, // E - F
    };

    try stdout.print("Connectivity queries:\n", .{});
    for (queries) |q| {
        const connected = ds.connected(q[0], q[1]);
        try stdout.print("  {s} <-> {s}: {}\n", .{ nodes[q[0]], nodes[q[1]], connected });
    }

    // Add bridge connection
    try stdout.print("\nAdding bridge: C <-> D\n", .{});
    _ = ds.unionSets(2, 3);

    try stdout.print("Connected components: {}\n\n", .{ds.countSets()});

    // Recheck connectivity
    try stdout.print("Connectivity after bridge:\n", .{});
    for (queries) |q| {
        const connected = ds.connected(q[0], q[1]);
        try stdout.print("  {s} <-> {s}: {}\n", .{ nodes[q[0]], nodes[q[1]], connected });
    }

    // Show network segments
    const segments = try ds.getAllSets(allocator);
    defer {
        for (segments) |seg| {
            allocator.free(seg);
        }
        allocator.free(segments);
    }

    try stdout.print("\nNetwork segments:\n", .{});
    for (segments, 1..) |seg, i| {
        try stdout.print("  Segment {}: ", .{i});
        for (seg) |node_idx| {
            try stdout.print("{s} ", .{nodes[node_idx]});
        }
        try stdout.print("\n", .{});
    }
}