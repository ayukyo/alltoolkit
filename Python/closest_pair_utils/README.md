# Closest Pair Utilities

A comprehensive closest pair of points utilities module for Python with zero external dependencies.

## Features

- **Find closest pair of points** in 2D and 3D space using divide and conquer algorithm
- **Multiple distance metrics**: Euclidean, Manhattan, Chebyshev
- **Find k closest pairs**: Get the top k closest pairs of points
- **Nearest neighbor search**: Find the nearest point to a query point
- **Radius search**: Find all points within a given radius
- **Zero external dependencies**: Uses only Python standard library

## Algorithms

| Algorithm | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Divide and Conquer (2D) | O(n log n) | O(n) |
| Divide and Conquer (3D) | O(n log² n) | O(n) |
| Brute Force | O(n²) | O(1) |

## Installation

No installation required. Simply copy the module to your project.

## Quick Start

```python
from closest_pair_utils.mod import (
    Point2D, Point3D, ClosestPair2D, ClosestPair3D,
    DistanceMetric, find_closest_pair_2d, find_closest_pair_3d
)

# Create points
points = [
    Point2D(0, 0),
    Point2D(1, 1),
    Point2D(10, 10),
    Point2D(11, 11)
]

# Find closest pair
finder = ClosestPair2D()
result = finder.find_closest_pair(points)
print(f"Closest pair: {result}")
print(f"Distance: {result.distance}")
```

## Usage Examples

### 2D Points

```python
from closest_pair_utils.mod import Point2D, ClosestPair2D, DistanceMetric

# Create points with optional IDs
points = [
    Point2D(0, 0, id=1),
    Point2D(3, 4, id=2),
    Point2D(1, 1, id=3),
    Point2D(10, 10, id=4)
]

# Using Euclidean distance (default)
finder = ClosestPair2D()
result = finder.find_closest_pair(points)
# Output: PointPair(Point2D(0, 0, id=1), Point2D(1, 1, id=3), dist=1.414214)

# Using Manhattan distance
finder_manhattan = ClosestPair2D(DistanceMetric.MANHATTAN)
result = finder_manhattan.find_closest_pair(points)

# Using Chebyshev distance
finder_chebyshev = ClosestPair2D(DistanceMetric.CHEBYSHEV)
result = finder_chebyshev.find_closest_pair(points)
```

### 3D Points

```python
from closest_pair_utils.mod import Point3D, ClosestPair3D

points_3d = [
    Point3D(0, 0, 0),
    Point3D(1, 1, 1),
    Point3D(10, 10, 10),
    Point3D(11, 11, 11)
]

finder_3d = ClosestPair3D()
result = finder_3d.find_closest_pair(points_3d)
# Output: PointPair with distance sqrt(3) ≈ 1.732
```

### Using Tuples (Convenience Functions)

```python
from closest_pair_utils.mod import find_closest_pair_2d, find_nearest_neighbor_2d

# Use tuples instead of Point2D objects
points = [(0, 0), (1, 1), (10, 10), (11, 11)]
result = find_closest_pair_2d(points)

# Find nearest neighbor
query = (5, 5)
nearest = find_nearest_neighbor_2d(points, query)
print(f"Nearest point to {query}: {nearest}")
```

### Find K Closest Pairs

```python
from closest_pair_utils.mod import Point2D, ClosestPair2D

points = [
    Point2D(0, 0), Point2D(1, 0), Point2D(0, 1),
    Point2D(10, 10), Point2D(11, 11)
]

finder = ClosestPair2D()
pairs = finder.find_k_closest_pairs(points, k=3)

for i, pair in enumerate(pairs, 1):
    print(f"{i}. {pair.point1} - {pair.point2}: {pair.distance:.4f}")
```

### Nearest Neighbor Search

```python
from closest_pair_utils.mod import Point2D, ClosestPair2D

points = [Point2D(i, i) for i in range(10)]
query = Point2D(4.5, 4.5)

finder = ClosestPair2D()
nearest = finder.find_nearest_neighbor(points, query)
print(f"Nearest to {query}: {nearest}")  # Point2D(4, 4) or Point2D(5, 5)
```

### Radius Search

```python
from closest_pair_utils.mod import Point2D, ClosestPair2D

points = [Point2D(i, 0) for i in range(20)]
center = Point2D(10, 0)

finder = ClosestPair2D()
nearby = finder.find_points_within_radius(points, center, radius=5)
print(f"Points within radius 5: {len(nearby)}")  # 11 points: (5,0) to (15,0)
```

## Distance Metrics

### Euclidean Distance
The straight-line distance between two points.
```
d = √((x2-x1)² + (y2-y1)²)
```

### Manhattan Distance
The sum of absolute differences (L1 norm).
```
d = |x2-x1| + |y2-y1|
```

### Chebyshev Distance
The maximum absolute difference in any dimension.
```
d = max(|x2-x1|, |y2-y1|)
```

## API Reference

### Point2D
```python
Point2D(x: float, y: float, id: Optional[int] = None)
```

### Point3D
```python
Point3D(x: float, y: float, z: float, id: Optional[int] = None)
```

### PointPair
```python
PointPair(point1, point2, distance)
```

### ClosestPair2D
```python
ClosestPair2D(metric: DistanceMetric = DistanceMetric.EUCLIDEAN)

find_closest_pair(points: List[Point2D]) -> Optional[PointPair]
find_k_closest_pairs(points: List[Point2D], k: int) -> List[PointPair]
find_nearest_neighbor(points: List[Point2D], query: Point2D) -> Optional[Point2D]
find_points_within_radius(points: List[Point2D], center: Point2D, radius: float) -> List[Point2D]
```

### ClosestPair3D
```python
ClosestPair3D(metric: DistanceMetric = DistanceMetric.EUCLIDEAN)

find_closest_pair(points: List[Point3D]) -> Optional[PointPair]
find_nearest_neighbor(points: List[Point3D], query: Point3D) -> Optional[Point3D]
```

### Convenience Functions
```python
find_closest_pair_2d(points: List[Tuple[float, float]], metric=DistanceMetric.EUCLIDEAN) -> Optional[PointPair]
find_closest_pair_3d(points: List[Tuple[float, float, float]], metric=DistanceMetric.EUCLIDEAN) -> Optional[PointPair]
find_nearest_neighbor_2d(points: List[Tuple[float, float]], query: Tuple[float, float], metric=DistanceMetric.EUCLIDEAN) -> Optional[Tuple[float, float]]
```

## Use Cases

1. **Computational Geometry**: Fundamental algorithm for geometric problems
2. **Clustering**: Finding closest points in cluster analysis
3. **Collision Detection**: Detecting nearby objects
4. **Network Design**: Finding nearest nodes in network topology
5. **Robotics**: Path planning and obstacle avoidance
6. **GIS Applications**: Finding nearest geographic features
7. **Computer Graphics**: Level of detail calculations

## Testing

Run the test suite:

```bash
python -m pytest closest_pair_utils_test.py -v
```

Or run directly:

```bash
python closest_pair_utils_test.py
```

## License

MIT License - Part of AllToolkit