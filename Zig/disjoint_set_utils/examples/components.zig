const std = @import("std");
const DisjointSet = @import("disjoint_set").DisjointSet;

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Graph Connected Components Example ===\n\n", .{});

    // Graph with 9 vertices
    // Component 1: 0 -- 1 -- 2
    //              |
    //              3
    // Component 2: 4 -- 5
    //              |
    //              6
    // Component 3: 7    8 (isolated)

    const vertex_labels = [_][]const u8{ "A", "B", "C", "D", "E", "F", "G", "H", "I" };
    var ds = try DisjointSet(usize).initRange(allocator, vertex_labels.len);
    defer ds.deinit();

    try stdout.print("Graph with {} vertices\n\n", .{vertex_labels.len});

    // Define edges
    const edges = [_][2]usize{
        .{ 0, 1 }, // A - B
        .{ 1, 2 }, // B - C
        .{ 0, 3 }, // A - D
        .{ 4, 5 }, // E - F
        .{ 4, 6 }, // E - G
    };

    try stdout.print("Adding edges:\n", .{});
    for (edges) |edge| {
        _ = ds.unionSets(edge[0], edge[1]);
        try stdout.print("  {s} -- {s}\n", .{ vertex_labels[edge[0]], vertex_labels[edge[1]] });
    }

    // Show components
    try stdout.print("\nAnalyzing connected components...\n", .{});
    try stdout.print("Total vertices: {}\n", .{ds.size()});
    try stdout.print("Connected components: {}\n\n", .{ds.countSets()});

    // Get all components
    const components = try ds.getAllSets(allocator);
    defer {
        for (components) |comp| {
            allocator.free(comp);
        }
        allocator.free(components);
    }

    // Sort and display components
    for (components, 1..) |comp, i| {
        try stdout.print("Component {}: ", .{i});
        for (comp) |vertex| {
            try stdout.print("{s} ", .{vertex_labels[vertex]});
        }
        try stdout.print("(size: {})\n", .{comp.len});
    }

    // Component size analysis
    try stdout.print("\nComponent analysis:\n", .{});
    for (0..vertex_labels.len) |v| {
        const set_size = ds.getSetSize(v);
        try stdout.print("  Vertex {s} is in a component of size {}\n", .{ vertex_labels[v], set_size });
    }

    // Path existence queries
    try stdout.print("\nPath existence queries:\n", .{});
    const path_queries = [_][2]usize{
        .{ 0, 3 }, // A to D (same component)
        .{ 0, 6 }, // A to G (different components)
        .{ 4, 6 }, // E to G (same component)
        .{ 7, 8 }, // H to I (different components)
    };

    for (path_queries) |q| {
        const exists = ds.connected(q[0], q[1]);
        try stdout.print("  {s} -> {s}: {s}\n", .{ vertex_labels[q[0]], vertex_labels[q[1]], if (exists) "path exists" else "no path" });
    }

    // Add a bridge edge
    try stdout.print("\nAdding bridge edge: D -- E\n", .{});
    _ = ds.unionSets(3, 4);

    try stdout.print("New component count: {}\n", .{ds.countSets()});

    // Verify new connectivity
    try stdout.print("\nUpdated path existence:\n", .{});
    try stdout.print("  A -> G: {}\n", .{ds.connected(0, 6)});
    try stdout.print("  B -> F: {}\n", .{ds.connected(1, 5)});
    try stdout.print("  C -> G: {}\n", .{ds.connected(2, 6)});

    // Final component analysis
    const final_components = try ds.getAllSets(allocator);
    defer {
        for (final_components) |comp| {
            allocator.free(comp);
        }
        allocator.free(final_components);
    }

    try stdout.print("\nFinal components:\n", .{});
    for (final_components, 1..) |comp, i| {
        try stdout.print("  Component {}: ", .{i});
        for (comp) |vertex| {
            try stdout.print("{s} ", .{vertex_labels[vertex]});
        }
        try stdout.print("\n", .{});
    }
}