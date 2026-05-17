//! Basic QuadTree usage example
//! Demonstrates insertion, query, and counting operations

const std = @import("std");
const quadtree = @import("quadtree");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== QuadTree Basic Example ===\n\n", .{});

    // Create a QuadTree with 100x100 boundary
    const QT = quadtree.QuadTree(void);
    var qt = try QT.init(
        allocator,
        quadtree.Rectangle.init(0, 0, 100, 100),
        4, // capacity per node
        8, // max depth
    );
    defer qt.deinit();

    // Insert some points
    std.debug.print("Inserting points...\n", .{});
    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(20, 20, null);
    _ = try qt.insertAt(30, 30, null);
    _ = try qt.insertAt(40, 40, null);
    _ = try qt.insertAt(50, 50, null);
    _ = try qt.insertAt(60, 60, null);
    _ = try qt.insertAt(70, 70, null);
    _ = try qt.insertAt(80, 80, null);
    _ = try qt.insertAt(90, 90, null);

    std.debug.print("Total points: {}\n", .{qt.count()});
    std.debug.print("Total nodes: {}\n", .{qt.nodeCount()});
    std.debug.print("Memory usage: {} bytes\n\n", .{qt.memoryUsage()});

    // Query a rectangular region
    std.debug.print("Querying rectangle (15,15) to (55,55):\n", .{});
    const rect_points = try qt.queryRect(quadtree.Rectangle.init(15, 15, 40, 40));
    defer allocator.free(rect_points);

    for (rect_points) |pt| {
        std.debug.print("  Point: ({}, {})\n", .{ pt.x, pt.y });
    }
    std.debug.print("Found {} points\n\n", .{rect_points.len});

    // Query a circular region
    std.debug.print("Querying circle at (50,50) with radius 25:\n", .{});
    const circle_points = try qt.queryCircle(quadtree.Circle.init(50, 50, 25));
    defer allocator.free(circle_points);

    for (circle_points) |pt| {
        std.debug.print("  Point: ({}, {})\n", .{ pt.x, pt.y });
    }
    std.debug.print("Found {} points\n\n", .{circle_points.len});

    std.debug.print("=== Example Complete ===\n", .{});
}