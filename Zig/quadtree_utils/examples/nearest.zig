//! Nearest neighbor example
//! Demonstrates finding the closest points to a query location

const std = @import("std");
const quadtree = @import("quadtree");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== QuadTree Nearest Neighbor Example ===\n\n", .{});

    // Create a QuadTree
    const QT = quadtree.QuadTree(void);
    var qt = try QT.init(allocator, quadtree.Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    // Insert random-ish points
    const points = [_][2]f64{
        .{ 10, 10 },
        .{ 15, 25 },
        .{ 30, 15 },
        .{ 25, 40 },
        .{ 50, 50 },
        .{ 45, 55 },
        .{ 70, 20 },
        .{ 80, 80 },
        .{ 90, 10 },
        .{ 10, 90 },
    };

    std.debug.print("Inserting {} points:\n", .{points.len});
    for (points) |coords| {
        std.debug.print("  ({d:.0}, {d:.0})\n", .{ coords[0], coords[1] });
        _ = try qt.insertAt(coords[0], coords[1], null);
    }
    std.debug.print("\n", .{});

    // Find single nearest point
    const query_x: f64 = 20;
    const query_y: f64 = 30;

    std.debug.print("Query point: ({d:.0}, {d:.0})\n\n", .{ query_x, query_y });

    std.debug.print("Finding single nearest point:\n", .{});
    const nearest_one = try qt.findNearest(query_x, query_y, 1, false);
    defer allocator.free(nearest_one);

    if (nearest_one.len > 0) {
        std.debug.print("  Nearest: ({d:.0}, {d:.0}) at distance {d:.2}\n\n", .{
            nearest_one[0].point.x,
            nearest_one[0].point.y,
            nearest_one[0].distance,
        });
    }

    // Find k nearest points
    std.debug.print("Finding 5 nearest points:\n", .{});
    const nearest_k = try qt.findNearest(query_x, query_y, 5, false);
    defer allocator.free(nearest_k);

    for (nearest_k) |item| {
        std.debug.print("  ({d:.0}, {d:.0}) distance={d:.2}\n", .{
            item.point.x,
            item.point.y,
            item.distance,
        });
    }
    std.debug.print("\n", .{});

    // Find nearest excluding the query point itself
    // Insert the query point first
    _ = try qt.insertAt(query_x, query_y, null);

    std.debug.print("Query point now inserted. Finding nearest excluding itself:\n", .{});
    const nearest_excl = try qt.findNearest(query_x, query_y, 1, true);
    defer allocator.free(nearest_excl);

    if (nearest_excl.len > 0) {
        std.debug.print("  Nearest (excluding self): ({d:.0}, {d:.0}) at distance {d:.2}\n\n", .{
            nearest_excl[0].point.x,
            nearest_excl[0].point.y,
            nearest_excl[0].distance,
        });
    }

    std.debug.print("=== Example Complete ===\n", .{});
}