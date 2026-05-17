# QuadTree Utilities (Zig)

A efficient QuadTree implementation for 2D spatial indexing, written in Zig with zero external dependencies.

## Features

- **Point insertion and removal** - Add/remove points dynamically
- **Rectangle query** - Find all points within a rectangular region
- **Circle query** - Find all points within a circular region  
- **Nearest neighbor search** - Find k nearest points to a location
- **Radius search** - Find all points within a given radius with distances
- **Automatic subdivision** - Nodes split when capacity exceeded
- **Generic data payload** - Points can carry arbitrary data
- **Memory tracking** - Estimate memory usage of the tree

## Time Complexity

- **Insert**: O(log n) average
- **Remove**: O(log n) average
- **Rectangle/Circle query**: O(log n + k) where k is result count
- **Nearest neighbor**: O(log n) average

## Usage

### Basic Setup

```zig
const std = @import("std");
const quadtree = @import("quadtree");

const allocator = std.heap.page_allocator;

// Create a QuadTree with 100x100 boundary
const QT = quadtree.QuadTree(void);
var qt = try QT.init(
    allocator,
    quadtree.Rectangle.init(0, 0, 100, 100),
    4, // capacity per node
    8, // max depth
);
defer qt.deinit();

// Insert points
_ = try qt.insertAt(10, 10, null);
_ = try qt.insertAt(50, 50, null);

// Query rectangle region
const points = try qt.queryRect(quadtree.Rectangle.init(0, 0, 30, 30));
defer allocator.free(points);
```

### With Data Payload

```zig
const QT = quadtree.QuadTree([]const u8);

var qt = try QT.init(allocator, quadtree.Rectangle.init(0, 0, 100, 100), 4, 8);
defer qt.deinit();

// Insert points with city names
_ = try qt.insertAt(10, 10, "Beijing");
_ = try qt.insertAt(50, 50, "Shanghai");

// Query and access data
const points = try qt.queryRect(quadtree.Rectangle.init(0, 0, 60, 60));
defer allocator.free(points);

for (points) |pt| {
    if (pt.data) |name| {
        std.debug.print("City: {s}\n", .{name});
    }
}
```

### Nearest Neighbor Search

```zig
// Find 5 nearest points to (25, 25)
const nearest = try qt.findNearest(25, 25, 5, false);
defer allocator.free(nearest);

for (nearest) |item| {
    std.debug.print("({d:.0}, {d:.0}) dist={d:.2}\n", .{
        item.point.x, item.point.y, item.distance
    });
}
```

### Circle Query

```zig
const circle = quadtree.Circle.init(50, 50, 25);
const points = try qt.queryCircle(circle);
defer allocator.free(points);

std.debug.print("Found {} points within circle\n", .{points.len});
```

## Core Types

### Rectangle

```zig
const rect = quadtree.Rectangle.init(0, 0, 100, 100);

rect.left()    // x
rect.right()   // x + width
rect.top()     // y
rect.bottom()  // y + height
rect.area()    // width * height
rect.containsPoint(x, y)  // check containment
rect.intersects(other)    // check intersection
```

### Circle

```zig
const circle = quadtree.Circle.init(50, 50, 25);

circle.containsPoint(x, y)    // check containment
circle.intersectsRect(rect)   // check rectangle intersection
```

### Point

```zig
const P = quadtree.Point(MyDataType);

var pt = P.init(10, 10);
pt.data = my_data;  // optional payload

pt.distanceTo(other)  // calculate distance
pt.eql(other)         // check equality
```

## Examples

Run examples with:

```bash
# Basic usage
zig build example-basic

# Spatial queries
zig build example-query

# Nearest neighbor
zig build example-nearest

# City locations with data
zig build example-cities

# Collision detection
zig build example-collision
```

## Testing

```bash
zig build test
```

## API Reference

### QuadTree(T)

| Method | Description |
|--------|-------------|
| `init(allocator, boundary, capacity, max_depth)` | Create new QuadTree |
| `deinit()` | Free all memory |
| `insert(point)` | Insert a Point |
| `insertAt(x, y, data)` | Insert with coordinates |
| `insertBatch(points)` | Insert multiple points |
| `remove(x, y)` | Remove point by coordinates |
| `queryRect(region)` | Query rectangle region |
| `queryCircle(circle)` | Query circle region |
| `findNearest(x, y, k, exclude_self)` | Find k nearest points |
| `findInRadius(x, y, radius)` | Find points within radius |
| `count()` | Total point count |
| `isEmpty()` | Check if empty |
| `nodeCount()` | Total node count |
| `memoryUsage()` | Estimate memory bytes |
| `boundary()` | Get boundary rectangle |

## Applications

- **Spatial indexing** - Geographic data, game maps
- **Collision detection** - 2D game physics
- **Range queries** - Find nearby objects, locations
- **Nearest neighbor** - Find closest entities
- **Image compression** - Quadtree-based image encoding
- **Frustum culling** - 3D rendering optimization

## License

MIT