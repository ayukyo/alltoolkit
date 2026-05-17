const std = @import("std");
const Allocator = std.mem.Allocator;

/// 2D Point with optional data payload
pub fn Point(comptime T: type) type {
    return struct {
        x: f64,
        y: f64,
        data: ?T,

        const Self = @This();

        /// Create a new point
        pub fn init(x: f64, y: f64) Self {
            return .{ .x = x, .y = y, .data = null };
        }

        /// Create a point with data
        pub fn initWithData(x: f64, y: f64, data: T) Self {
            return .{ .x = x, .y = y, .data = data };
        }

        /// Calculate distance to another point
        pub fn distanceTo(self: Self, other: Self) f64 {
            const dx = self.x - other.x;
            const dy = self.y - other.y;
            return @sqrt(dx * dx + dy * dy);
        }

        /// Check if two points are equal (same coordinates)
        pub fn eql(self: Self, other: Self) bool {
            return self.x == other.x and self.y == other.y;
        }
    };
}

/// Axis-Aligned Bounding Rectangle
pub const Rectangle = struct {
    x: f64, // left
    y: f64, // top
    width: f64,
    height: f64,

    const Self = @This();

    /// Create a new rectangle
    pub fn init(x: f64, y: f64, width: f64, height: f64) Self {
        return .{ .x = x, .y = y, .width = width, .height = height };
    }

    /// Left boundary
    pub fn left(self: Self) f64 {
        return self.x;
    }

    /// Right boundary
    pub fn right(self: Self) f64 {
        return self.x + self.width;
    }

    /// Top boundary
    pub fn top(self: Self) f64 {
        return self.y;
    }

    /// Bottom boundary
    pub fn bottom(self: Self) f64 {
        return self.y + self.height;
    }

    /// Center point
    pub fn center(self: Self) [2]f64 {
        return .{ self.x + self.width / 2, self.y + self.height / 2 };
    }

    /// Area
    pub fn area(self: Self) f64 {
        return self.width * self.height;
    }

    /// Check if point is contained in rectangle
    pub fn containsPoint(self: Self, x: f64, y: f64) bool {
        return x >= self.x and x < self.right() and y >= self.y and y < self.bottom();
    }

    /// Check if two rectangles intersect
    pub fn intersects(self: Self, other: Self) bool {
        return !(other.x >= self.right() or
            other.right() <= self.x or
            other.y >= self.bottom() or
            other.bottom() <= self.y);
    }

    /// Check if another rectangle is fully contained
    pub fn containsRect(self: Self, other: Self) bool {
        return other.x >= self.x and
            other.right() <= self.right() and
            other.y >= self.y and
            other.bottom() <= self.bottom();
    }
};

/// Circle region
pub const Circle = struct {
    x: f64,
    y: f64,
    radius: f64,

    const Self = @This();

    /// Create a new circle
    pub fn init(x: f64, y: f64, radius: f64) Self {
        return .{ .x = x, .y = y, .radius = radius };
    }

    /// Check if point is inside circle
    pub fn containsPoint(self: Self, x: f64, y: f64) bool {
        const dx = x - self.x;
        const dy = y - self.y;
        return dx * dx + dy * dy <= self.radius * self.radius;
    }

    /// Check if circle intersects with rectangle
    pub fn intersectsRect(self: Self, rect: Rectangle) bool {
        // Find closest point on rectangle to circle center
        const closest_x = @max(rect.x, @min(self.x, rect.right()));
        const closest_y = @max(rect.y, @min(self.y, rect.bottom()));

        const dx = self.x - closest_x;
        const dy = self.y - closest_y;

        return dx * dx + dy * dy <= self.radius * self.radius;
    }
};

/// Quadtree node quadrant indices
const Quadrant = enum(u2) {
    nw = 0, // Northwest (top-left)
    ne = 1, // Northeast (top-right)
    sw = 2, // Southwest (bottom-left)
    se = 3, // Southeast (bottom-right)
};

/// Quadtree for efficient 2D spatial queries
pub fn QuadTree(comptime T: type) type {
    return struct {
        const Self = @This();
        const PointType = Point(T);
        const SearchResult = struct { point: PointType, distance: f64 };

        /// Node in the quadtree
        const Node = struct {
            boundary: Rectangle,
            points: []?PointType,
            point_count: usize,
            children: ?[4]*Node,
            depth: usize,
            capacity: usize,
            max_depth: usize,

            /// Initialize a new node
            fn init(allocator: Allocator, bounds: Rectangle, cap: usize, max_d: usize, d: usize) Allocator.Error!*Node {
                const node = try allocator.create(Node);
                node.* = .{
                    .boundary = bounds,
                    .points = try allocator.alloc(?PointType, cap),
                    .point_count = 0,
                    .children = null,
                    .depth = d,
                    .capacity = cap,
                    .max_depth = max_d,
                };
                @memset(node.points, null);
                return node;
            }

            /// Free node and all children
            fn deinit(self: *Node, allocator: Allocator) void {
                if (self.children) |children| {
                    for (children) |child| {
                        child.deinit(allocator);
                    }
                    allocator.free(self.points);
                } else {
                    allocator.free(self.points);
                }
                allocator.destroy(self);
            }

            /// Check if this is a leaf node
            fn isLeaf(self: *const Node) bool {
                return self.children == null;
            }

            /// Subdivide this node into four children
            fn subdivide(self: *Node, allocator: Allocator) Allocator.Error!void {
                if (!self.isLeaf()) return;

                const x = self.boundary.x;
                const y = self.boundary.y;
                const hw = self.boundary.width / 2;
                const hh = self.boundary.height / 2;
                const new_depth = self.depth + 1;

                self.children = .{
                    try Node.init(allocator, Rectangle.init(x, y, hw, hh), self.capacity, self.max_depth, new_depth), // NW
                    try Node.init(allocator, Rectangle.init(x + hw, y, hw, hh), self.capacity, self.max_depth, new_depth), // NE
                    try Node.init(allocator, Rectangle.init(x, y + hh, hw, hh), self.capacity, self.max_depth, new_depth), // SW
                    try Node.init(allocator, Rectangle.init(x + hw, y + hh, hw, hh), self.capacity, self.max_depth, new_depth), // SE
                };

                // Redistribute points to children
                for (self.points[0..self.point_count]) |maybe_point| {
                    if (maybe_point) |pt| {
                        const quadrant = self.getQuadrant(pt.x, pt.y);
                        if (quadrant) |q| {
                            _ = try self.children.?[(@intFromEnum(q))].insertInternal(allocator, pt);
                        }
                    }
                }

                // Free old points
                allocator.free(self.points);
                self.points = &[_]?PointType{};
                self.point_count = 0;
            }

            /// Determine which quadrant a point belongs to
            fn getQuadrant(self: *const Node, x: f64, y: f64) ?Quadrant {
                if (!self.boundary.containsPoint(x, y)) return null;

                const mid_x = self.boundary.x + self.boundary.width / 2;
                const mid_y = self.boundary.y + self.boundary.height / 2;

                if (x < mid_x) {
                    return if (y < mid_y) Quadrant.nw else Quadrant.sw;
                } else {
                    return if (y < mid_y) Quadrant.ne else Quadrant.se;
                }
            }

            /// Insert a point into this node or children
            fn insertInternal(self: *Node, allocator: Allocator, point: PointType) Allocator.Error!bool {
                if (!self.boundary.containsPoint(point.x, point.y)) return false;

                if (self.isLeaf()) {
                    if (self.point_count < self.capacity or self.depth >= self.max_depth) {
                        self.points[self.point_count] = point;
                        self.point_count += 1;
                        return true;
                    }

                    // Need to subdivide
                    try self.subdivide(allocator);
                }

                // Insert into appropriate child
                const quadrant = self.getQuadrant(point.x, point.y);
                if (quadrant) |q| {
                    return try self.children.?[@intFromEnum(q)].insertInternal(allocator, point);
                }
                return false;
            }

            /// Remove a point
            fn remove(self: *Node, allocator: Allocator, x: f64, y: f64) bool {
                if (!self.boundary.containsPoint(x, y)) return false;

                if (self.isLeaf()) {
                    var i: usize = 0;
                    while (i < self.point_count) : (i += 1) {
                        if (self.points[i]) |pt| {
                            if (pt.x == x and pt.y == y) {
                                // Shift remaining points
                                for (i..self.point_count - 1) |j| {
                                    self.points[j] = self.points[j + 1];
                                }
                                self.point_count -= 1;
                                self.points[self.point_count] = null;
                                return true;
                            }
                        }
                    }
                    return false;
                }

                const quadrant = self.getQuadrant(x, y);
                if (quadrant) |q| {
                    return self.children.?[@intFromEnum(q)].remove(allocator, x, y);
                }
                return false;
            }

            /// Query points in a rectangle region
            fn query(self: *const Node, region: Rectangle, result: *std.ArrayList(PointType)) Allocator.Error!void {
                if (!self.boundary.intersects(region)) return;

                if (self.isLeaf()) {
                    for (self.points[0..self.point_count]) |maybe_point| {
                        if (maybe_point) |pt| {
                            if (region.containsPoint(pt.x, pt.y)) {
                                try result.append(pt);
                            }
                        }
                    }
                } else if (self.children) |children| {
                    for (children) |child| {
                        try child.query(region, result);
                    }
                }
            }

            /// Query points in a circle region
            fn queryCircle(self: *const Node, circle: Circle, result: *std.ArrayList(PointType)) Allocator.Error!void {
                if (!circle.intersectsRect(self.boundary)) return;

                if (self.isLeaf()) {
                    for (self.points[0..self.point_count]) |maybe_point| {
                        if (maybe_point) |pt| {
                            if (circle.containsPoint(pt.x, pt.y)) {
                                try result.append(pt);
                            }
                        }
                    }
                } else if (self.children) |children| {
                    for (children) |child| {
                        try child.queryCircle(circle, result);
                    }
                }
            }

            /// Find nearest points to a given point
            fn findNearest(
                self: *const Node,
                x: f64,
                y: f64,
                k: usize,
                exclude_self: bool,
                result: *std.ArrayList(SearchResult),
            ) Allocator.Error!void {
                if (self.isLeaf()) {
                    for (self.points[0..self.point_count]) |maybe_point| {
                        if (maybe_point) |pt| {
                            if (exclude_self and pt.x == x and pt.y == y) continue;
                            const dist = pt.distanceTo(PointType.init(x, y));
                            try result.append(.{ .point = pt, .distance = dist });
                        }
                    }
                } else if (self.children) |children| {
                    // Sort children by distance to query point
                    var child_order: [4]struct { dist: f64, idx: usize } = undefined;
                    for (children, 0..) |child, i| {
                        child_order[i] = .{
                            .dist = child.minDistanceToPoint(x, y),
                            .idx = i,
                        };
                    }
                    std.mem.sort(@TypeOf(child_order[0]), &child_order, {}, struct {
                        fn lessThan(_: void, a: @TypeOf(child_order[0]), b: @TypeOf(child_order[0])) bool {
                            return a.dist < b.dist;
                        }
                    }.lessThan);

                    for (child_order) |order| {
                        // Pruning: if the closest possible distance is greater than the k-th result, skip
                        if (result.items.len >= k) {
                            std.mem.sort(SearchResult, result.items, {}, struct {
                                fn lessThan(_: void, a: SearchResult, b: SearchResult) bool {
                                    return a.distance < b.distance;
                                }
                            }.lessThan);
                            if (order.dist > result.items[k - 1].distance) continue;
                        }
                        try children[order.idx].findNearest(x, y, k, exclude_self, result);
                    }
                }
            }

            /// Calculate minimum distance from point to boundary
            fn minDistanceToPoint(self: *const Node, x: f64, y: f64) f64 {
                var dx: f64 = 0;
                if (x < self.boundary.x) {
                    dx = self.boundary.x - x;
                } else if (x > self.boundary.right()) {
                    dx = x - self.boundary.right();
                }

                var dy: f64 = 0;
                if (y < self.boundary.y) {
                    dy = self.boundary.y - y;
                } else if (y > self.boundary.bottom()) {
                    dy = y - self.boundary.bottom();
                }

                return @sqrt(dx * dx + dy * dy);
            }

            /// Count all points in this node and children
            fn count(self: *const Node) usize {
                if (self.isLeaf()) {
                    return self.point_count;
                }
                if (self.children) |children| {
                    var total: usize = 0;
                    for (children) |child| {
                        total += child.count();
                    }
                    return total;
                }
                return 0;
            }

            /// Count total nodes
            fn nodeCount(self: *const Node) usize {
                var total: usize = 1;
                if (self.children) |children| {
                    for (children) |child| {
                        total += child.nodeCount();
                    }
                }
                return total;
            }

            /// Estimate memory usage
            fn memoryUsage(self: *const Node) usize {
                var total: usize = @sizeOf(Node);
                if (self.isLeaf()) {
                    total += self.points.len * @sizeOf(?PointType);
                }
                if (self.children) |children| {
                    for (children) |child| {
                        total += child.memoryUsage();
                    }
                }
                return total;
            }
        };

        root: *Node,
        allocator: Allocator,
        capacity: usize,
        max_depth: usize,

        /// Initialize a new QuadTree
        pub fn init(allocator: Allocator, bounds: Rectangle, cap: usize, max_d: usize) Allocator.Error!Self {
            const root = try Node.init(allocator, bounds, cap, max_d, 0);
            return .{
                .root = root,
                .allocator = allocator,
                .capacity = cap,
                .max_depth = max_d,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            self.root.deinit(self.allocator);
            self.* = undefined;
        }

        /// Insert a point into the quadtree
        pub fn insert(self: *Self, point: PointType) Allocator.Error!bool {
            return try self.root.insertInternal(self.allocator, point);
        }

        /// Insert a point with coordinates
        pub fn insertAt(self: *Self, x: f64, y: f64, data: ?T) Allocator.Error!bool {
            var point = PointType.init(x, y);
            point.data = data;
            return try self.insert(point);
        }

        /// Insert multiple points
        pub fn insertBatch(self: *Self, points: []const PointType) Allocator.Error!usize {
            var inserted_count: usize = 0;
            for (points) |pt| {
                if (try self.insert(pt)) {
                    inserted_count += 1;
                }
            }
            return inserted_count;
        }

        /// Remove a point by coordinates
        pub fn remove(self: *Self, x: f64, y: f64) bool {
            return self.root.remove(self.allocator, x, y);
        }

        /// Query points in a rectangular region
        pub fn queryRect(self: *const Self, region: Rectangle) Allocator.Error![]PointType {
            var result = std.ArrayList(PointType).init(self.allocator);
            errdefer result.deinit();
            try self.root.query(region, &result);
            return result.toOwnedSlice();
        }

        /// Query points in a circle region
        pub fn queryCircle(self: *const Self, circle: Circle) Allocator.Error![]PointType {
            var result = std.ArrayList(PointType).init(self.allocator);
            errdefer result.deinit();
            try self.root.queryCircle(circle, &result);
            return result.toOwnedSlice();
        }

        /// Find k nearest points to a location
        pub fn findNearest(self: *const Self, x: f64, y: f64, k: usize, exclude_self: bool) Allocator.Error![]SearchResult {
            var result = std.ArrayList(SearchResult).init(self.allocator);
            errdefer result.deinit();
            try self.root.findNearest(x, y, k, exclude_self, &result);

            // Sort by distance
            std.mem.sort(SearchResult, result.items, {}, struct {
                fn lessThan(_: void, a: SearchResult, b: SearchResult) bool {
                    return a.distance < b.distance;
                }
            }.lessThan);

            // Trim to top k results if we have more
            if (result.items.len > k) {
                // Free excess items' memory by reallocating to exact size
                const owned = try result.toOwnedSlice();
                const trimmed = try self.allocator.realloc(owned, k);
                return trimmed;
            }

            return result.toOwnedSlice();
        }

        /// Find all points within a radius
        pub fn findInRadius(self: *const Self, x: f64, y: f64, radius: f64) Allocator.Error![]SearchResult {
            const points = try self.queryCircle(Circle.init(x, y, radius));
            defer self.allocator.free(points);

            var result = std.ArrayList(SearchResult).init(self.allocator);
            errdefer result.deinit();

            const query_point = PointType.init(x, y);
            for (points) |pt| {
                const dist = pt.distanceTo(query_point);
                if (dist <= radius) {
                    try result.append(.{ .point = pt, .distance = dist });
                }
            }

            // Sort by distance
            std.mem.sort(SearchResult, result.items, {}, struct {
                fn lessThan(_: void, a: SearchResult, b: SearchResult) bool {
                    return a.distance < b.distance;
                }
            }.lessThan);

            return result.toOwnedSlice();
        }

        /// Get total point count
        pub fn count(self: *const Self) usize {
            return self.root.count();
        }

        /// Check if empty
        pub fn isEmpty(self: *const Self) bool {
            return self.count() == 0;
        }

        /// Get total node count
        pub fn nodeCount(self: *const Self) usize {
            return self.root.nodeCount();
        }

        /// Estimate memory usage
        pub fn memoryUsage(self: *const Self) usize {
            return self.root.memoryUsage();
        }

        /// Get boundary
        pub fn getBoundary(self: *const Self) Rectangle {
            return self.root.boundary;
        }
    };
}

// Tests
const testing = std.testing;

test "Rectangle - basic operations" {
    const rect = Rectangle.init(0, 0, 100, 100);

    try testing.expectEqual(@as(f64, 0), rect.left());
    try testing.expectEqual(@as(f64, 100), rect.right());
    try testing.expectEqual(@as(f64, 0), rect.top());
    try testing.expectEqual(@as(f64, 100), rect.bottom());
    try testing.expectEqual(@as(f64, 10000), rect.area());

    try testing.expect(rect.containsPoint(50, 50));
    try testing.expect(rect.containsPoint(0, 0));
    try testing.expect(!rect.containsPoint(100, 100));
    try testing.expect(!rect.containsPoint(-1, 50));

    const rect2 = Rectangle.init(50, 50, 100, 100);
    try testing.expect(rect.intersects(rect2));

    const rect3 = Rectangle.init(200, 200, 100, 100);
    try testing.expect(!rect.intersects(rect3));
}

test "Circle - basic operations" {
    const circle = Circle.init(50, 50, 25);

    try testing.expect(circle.containsPoint(50, 50));
    try testing.expect(circle.containsPoint(50, 75));
    try testing.expect(!circle.containsPoint(50, 76));

    const rect = Rectangle.init(0, 0, 100, 100);
    try testing.expect(circle.intersectsRect(rect));

    const rect2 = Rectangle.init(100, 100, 100, 100);
    try testing.expect(!circle.intersectsRect(rect2));
}

test "QuadTree - basic insert and query" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(50, 50, null);
    _ = try qt.insertAt(90, 90, null);

    try testing.expectEqual(@as(usize, 3), qt.count());

    const points = try qt.queryRect(Rectangle.init(0, 0, 20, 20));
    defer allocator.free(points);
    try testing.expectEqual(@as(usize, 1), points.len);
}

test "QuadTree - rectangle query" {
    const allocator = testing.allocator;
    const QT = QuadTree(i32);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, 1);
    _ = try qt.insertAt(20, 20, 2);
    _ = try qt.insertAt(30, 30, 3);
    _ = try qt.insertAt(40, 40, 4);
    _ = try qt.insertAt(50, 50, 5);
    _ = try qt.insertAt(60, 60, 6);

    const points = try qt.queryRect(Rectangle.init(15, 15, 40, 40));
    defer allocator.free(points);
    // Points in range [15,55]: (20,20), (30,30), (40,40), (50,50) = 4 points
    try testing.expectEqual(@as(usize, 4), points.len);
}

test "QuadTree - circle query" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(25, 25, null);
    _ = try qt.insertAt(50, 50, null);
    _ = try qt.insertAt(75, 75, null);

    const points = try qt.queryCircle(Circle.init(50, 50, 30));
    defer allocator.free(points);
    // Distance from (50,50) to (25,25) = sqrt(25^2+25^2) ≈ 35.4 > 30
    // Distance from (50,50) to (75,75) = sqrt(25^2+25^2) ≈ 35.4 > 30
    // Only (50,50) itself is within radius
    try testing.expectEqual(@as(usize, 1), points.len);
}

test "QuadTree - find nearest" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(20, 20, null);
    _ = try qt.insertAt(30, 30, null);
    _ = try qt.insertAt(40, 40, null);

    const nearest = try qt.findNearest(15, 15, 2, false);
    defer allocator.free(nearest);
    try testing.expectEqual(@as(usize, 2), nearest.len);
}

test "QuadTree - find in radius" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(15, 15, null);
    _ = try qt.insertAt(50, 50, null);

    const points = try qt.findInRadius(12, 12, 10);
    defer allocator.free(points);
    try testing.expectEqual(@as(usize, 2), points.len);
}

test "QuadTree - remove" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(20, 20, null);

    try testing.expectEqual(@as(usize, 2), qt.count());

    const removed = qt.remove(10, 10);
    try testing.expect(removed);
    try testing.expectEqual(@as(usize, 1), qt.count());

    const removed2 = qt.remove(10, 10);
    try testing.expect(!removed2);
}

test "QuadTree - subdivision" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 2, 4);
    defer qt.deinit();

    // Insert more points than capacity to trigger subdivision
    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(20, 20, null);
    _ = try qt.insertAt(30, 30, null);
    _ = try qt.insertAt(40, 40, null);
    _ = try qt.insertAt(50, 50, null);

    try testing.expectEqual(@as(usize, 5), qt.count());
    try testing.expect(qt.nodeCount() > 1);
}

test "QuadTree - batch insert" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    const points = [_]Point(void){
        Point(void).init(10, 10),
        Point(void).init(20, 20),
        Point(void).init(30, 30),
        Point(void).init(40, 40),
        Point(void).init(50, 50),
    };

    const count = try qt.insertBatch(&points);
    try testing.expectEqual(@as(usize, 5), count);
    try testing.expectEqual(@as(usize, 5), qt.count());
}

test "QuadTree - with data payload" {
    const allocator = testing.allocator;
    const QT = QuadTree([]const u8);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, "point A");
    _ = try qt.insertAt(20, 20, "point B");
    _ = try qt.insertAt(30, 30, "point C");

    const points = try qt.queryRect(Rectangle.init(0, 0, 25, 25));
    defer allocator.free(points);

    try testing.expectEqual(@as(usize, 2), points.len);
    if (points.len > 0) {
        try testing.expectEqualStrings("point A", points[0].data.?);
    }
}

test "QuadTree - empty tree" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    try testing.expect(qt.isEmpty());
    try testing.expectEqual(@as(usize, 0), qt.count());

    const points = try qt.queryRect(Rectangle.init(0, 0, 100, 100));
    defer allocator.free(points);
    try testing.expectEqual(@as(usize, 0), points.len);
}

test "QuadTree - point out of bounds" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    const inserted = try qt.insertAt(200, 200, null);
    try testing.expect(!inserted);
    try testing.expectEqual(@as(usize, 0), qt.count());
}

test "QuadTree - memory usage" {
    const allocator = testing.allocator;
    const QT = QuadTree(void);

    var qt = try QT.init(allocator, Rectangle.init(0, 0, 100, 100), 4, 8);
    defer qt.deinit();

    _ = try qt.insertAt(10, 10, null);
    _ = try qt.insertAt(20, 20, null);

    const mem = qt.memoryUsage();
    try testing.expect(mem > 0);
}

test "Point - distance calculation" {
    const P = Point(void);

    const p1 = P.init(0, 0);
    const p2 = P.init(3, 4);

    const dist = p1.distanceTo(p2);
    try testing.expectEqual(@as(f64, 5.0), dist);
}