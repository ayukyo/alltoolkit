//! Cities location example
//! Demonstrates using QuadTree with data payload for city locations

const std = @import("std");
const quadtree = @import("quadtree");

const City = struct {
    name: []const u8,
    population: u32,
};

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== QuadTree City Locations Example ===\n\n", .{});

    // Create a QuadTree with city data
    const QT = quadtree.QuadTree(City);
    var qt = try QT.init(allocator, quadtree.Rectangle.init(0, 0, 1000, 1000), 4, 8);
    defer qt.deinit();

    // Define some cities with coordinates
    const cities = [_]struct { x: f64, y: f64, name: []const u8, pop: u32 }{
        .{ .x = 100, .y = 200, .name = "Beijing", .pop = 21540000 },
        .{ .x = 150, .y = 180, .name = "Shanghai", .pop = 24870000 },
        .{ .x = 200, .y = 150, .name = "Guangzhou", .pop = 15300000 },
        .{ .x = 180, .y = 300, .name = "Shenzhen", .pop = 17560000 },
        .{ .x = 400, .y = 400, .name = "Wuhan", .pop = 12320000 },
        .{ .x = 500, .y = 600, .name = "Chengdu", .pop = 16330000 },
        .{ .x = 600, .y = 500, .name = "Hangzhou", .pop = 11930000 },
        .{ .x = 300, .y = 800, .name = "Xi'an", .pop = 12950000 },
        .{ .x = 700, .y = 200, .name = "Nanjing", .pop = 9420000 },
        .{ .x = 800, .y = 700, .name = "Chongqing", .pop = 32050000 },
    };

    std.debug.print("Inserting {} cities:\n", .{cities.len});
    for (cities) |city| {
        const city_data = City{ .name = city.name, .population = city.pop };
        var point = quadtree.Point(City).init(city.x, city.y);
        point.data = city_data;
        _ = try qt.insert(point);

        std.debug.print("  {s} at ({d:.0}, {d:.0}) - pop: {}\n", .{
            city.name,
            city.x,
            city.y,
            city.pop,
        });
    }
    std.debug.print("\n", .{});

    // Find cities in a region
    std.debug.print("Cities in region [100,100] to [250,350]:\n", .{});
    const region = quadtree.Rectangle.init(100, 100, 150, 250);
    const region_cities = try qt.queryRect(region);
    defer allocator.free(region_cities);

    for (region_cities) |pt| {
        if (pt.data) |city| {
            std.debug.print("  {s} (population: {})\n", .{ city.name, city.population });
        }
    }
    std.debug.print("Found {} cities\n\n", .{region_cities.len});

    // Find nearest city to a location
    std.debug.print("Nearest city to (350, 350):\n", .{});
    const nearest = try qt.findNearest(350, 350, 1, false);
    defer allocator.free(nearest);

    if (nearest.len > 0) {
        if (nearest[0].point.data) |city| {
            std.debug.print("  {s} at distance {d:.0} (population: {})\n\n", .{
                city.name,
                nearest[0].distance,
                city.population,
            });
        }
    }

    // Find cities within radius
    std.debug.print("Cities within 150 units of (200, 200):\n", .{});
    const nearby = try qt.findInRadius(200, 200, 150);
    defer allocator.free(nearby);

    for (nearby) |item| {
        if (item.point.data) |city| {
            std.debug.print("  {s} distance={d:.0}\n", .{ city.name, item.distance });
        }
    }

    std.debug.print("\n=== Example Complete ===\n", .{});
}