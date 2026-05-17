//! Spatial query example
//! Demonstrates different query types: rectangle, circle, and radius search

const std = @import("std");
const quadtree = @import("quadtree");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== QuadTree Spatial Query Example ===\n\n", .{});

    // Create a QuadTree
    const QT = quadtree.QuadTree(void);
    var qt = try QT.init(allocator, quadtree.Rectangle.init(0, 0, 200, 200), 4, 8);
    defer qt.deinit();

    // Insert a grid of points
    std.debug.print("Inserting grid of points (20x20 spacing):\n", .{});
    var x: f64 = 10;
    while (x < 200) : (x += 20) {
        var y: f64 = 10;
        while (y < 200) : (y += 20) {
            _ = try qt.insertAt(x, y, null);
        }
    }
    std.debug.print("Total points: {}\n\n", .{qt.count()});

    // Rectangle query
    std.debug.print("Rectangle Query [50,50] to [100,100]:\n", .{});
    const rect = quadtree.Rectangle.init(50, 50, 50, 50);
    const rect_points = try qt.queryRect(rect);
    defer allocator.free(rect_points);

    std.debug.print("  Boundary: x={}, y={}, w={}, h={}\n", .{ rect.x, rect.y, rect.width, rect.height });
    std.debug.print("  Found {} points:\n", .{rect_points.len});
    for (rect_points) |pt| {
        std.debug.print("    ({d:.0}, {d:.0})\n", .{ pt.x, pt.y });
    }
    std.debug.print("\n", .{});

    // Circle query
    std.debug.print("Circle Query at (100,100) radius=30:\n", .{});
    const circle = quadtree.Circle.init(100, 100, 30);
    const circle_points = try qt.queryCircle(circle);
    defer allocator.free(circle_points);

    std.debug.print("  Center: ({d:.0}, {d:.0}), radius: {d:.0}\n", .{ circle.x, circle.y, circle.radius });
    std.debug.print("  Found {} points:\n", .{circle_points.len});
    for (circle_points) |pt| {
        std.debug.print("    ({d:.0}, {d:.0})\n", .{ pt.x, pt.y });
    }
    std.debug.print("\n", .{});

    // Find points within radius (with distance)
    std.debug.print("Radius Search at (100,100) radius=30 (with distances):\n", .{});
    const radius_points = try qt.findInRadius(100, 100, 30);
    defer allocator.free(radius_points);

    std.debug.print("  Found {} points:\n", .{radius_points.len});
    for (radius_points) |item| {
        std.debug.print("    ({d:.0}, {d:.0}) distance={d:.2}\n", .{ item.point.x, item.point.y, item.distance });
    }

    std.debug.print("\n=== Example Complete ===\n", .{});
}