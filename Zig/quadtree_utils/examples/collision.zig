//! Collision detection example
//! Demonstrates using QuadTree for efficient collision detection

const std = @import("std");
const quadtree = @import("quadtree");

const Entity = struct {
    id: u32,
    radius: f64,
};

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== QuadTree Collision Detection Example ===\n\n", .{});

    // Create a QuadTree for entities
    const QT = quadtree.QuadTree(Entity);
    var qt = try QT.init(allocator, quadtree.Rectangle.init(0, 0, 800, 600), 4, 10);
    defer qt.deinit();

    // Define entities with their positions and radii
    const entities = [_]struct { x: f64, y: f64, id: u32, radius: f64 }{
        .{ .x = 100, .y = 100, .id = 1, .radius = 20 },
        .{ .x = 130, .y = 110, .id = 2, .radius = 15 },
        .{ .x = 200, .y = 150, .id = 3, .radius = 25 },
        .{ .x = 300, .y = 200, .id = 4, .radius = 30 },
        .{ .x = 310, .y = 210, .id = 5, .radius = 10 },
        .{ .x = 500, .y = 300, .id = 6, .radius = 40 },
        .{ .x = 550, .y = 320, .id = 7, .radius = 35 },
        .{ .x = 700, .y = 400, .id = 8, .radius = 20 },
        .{ .x = 400, .y = 500, .id = 9, .radius = 50 },
        .{ .x = 420, .y = 510, .id = 10, .radius = 15 },
    };

    std.debug.print("Inserting {} entities:\n", .{entities.len});
    for (entities) |e| {
        const entity_data = Entity{ .id = e.id, .radius = e.radius };
        var point = quadtree.Point(Entity).init(e.x, e.y);
        point.data = entity_data;
        _ = try qt.insert(point);

        std.debug.print("  Entity {} at ({d:.0}, {d:.0}) radius={d:.0}\n", .{
            e.id,
            e.x,
            e.y,
            e.radius,
        });
    }
    std.debug.print("\n", .{});

    // Check collisions for each entity
    std.debug.print("Checking collisions:\n", .{});

    // We need to get all points first
    var all_points = std.ArrayList(quadtree.Point(Entity)).init(allocator);
    defer all_points.deinit();

    // Query entire boundary to get all points
    const boundary = qt.getBoundary();
    const points = try qt.queryRect(boundary);
    defer allocator.free(points);

    for (points) |pt| {
        try all_points.append(pt);
    }

    // Check collisions between entities
    var collision_count: u32 = 0;

    for (all_points.items) |entity1| {
        if (entity1.data) |e1| {
            // Search radius = entity radius + max possible radius (50)
            const search_radius = e1.radius + 50;

            const nearby = try qt.findInRadius(entity1.x, entity1.y, search_radius);
            defer allocator.free(nearby);

            for (nearby) |item| {
                const entity2 = item.point;

                // Skip self and already-checked pairs
                if (entity2.data) |e2| {
                    if (e2.id <= e1.id) continue;

                    // Check actual collision
                    const actual_dist = entity1.distanceTo(entity2);
                    const combined_radius = e1.radius + e2.radius;

                    if (actual_dist < combined_radius) {
                        collision_count += 1;
                        std.debug.print("  Collision: Entity {} <-> Entity {} (dist={d:.1}, combined_radius={d:.0})\n", .{
                            e1.id,
                            e2.id,
                            actual_dist,
                            combined_radius,
                        });
                    }
                }
            }
        }
    }

    std.debug.print("\nTotal collisions detected: {}\n", .{collision_count});

    // Demonstrate efficient area-based collision check
    std.debug.print("\nChecking collisions in area [300,200] to [400,350]:\n", .{});
    const area = quadtree.Rectangle.init(300, 200, 100, 150);
    const area_entities = try qt.queryRect(area);
    defer allocator.free(area_entities);

    std.debug.print("  Found {} entities in area:\n", .{area_entities.len});
    for (area_entities) |pt| {
        if (pt.data) |e| {
            std.debug.print("    Entity {} at ({d:.0}, {d:.0})\n", .{ e.id, pt.x, pt.y });
        }
    }

    std.debug.print("\n=== Example Complete ===\n", .{});
}