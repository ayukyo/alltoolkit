"""
Convex Hull Utilities - Multiple algorithms for computing convex hulls.

This module provides implementations of various convex hull algorithms:
- Graham Scan: O(n log n) - efficient for most cases
- Jarvis March (Gift Wrapping): O(nh) where h is hull size - good for small hulls
- QuickHull: O(n log n) average - often fastest in practice
- Chan's Algorithm: O(n log h) - optimal output-sensitive algorithm

Zero external dependencies - uses only Python standard library.

Author: AllToolkit
Date: 2026-05-03
"""

from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import math


class HullAlgorithm(Enum):
    """Available convex hull algorithms."""
    GRAHAM_SCAN = "graham_scan"
    JARVIS_MARCH = "jarvis_march"
    QUICKHULL = "quickhull"
    CHAN = "chan"


@dataclass
class Point:
    """2D Point representation."""
    x: float
    y: float
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Point index out of range")
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        return False
    
    def __hash__(self):
        return hash((round(self.x, 10), round(self.y, 10)))
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return Point(self.x - other, self.y - other)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def manhattan_distance_to(self, other: 'Point') -> float:
        """Calculate Manhattan distance to another point."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    @staticmethod
    def from_tuple(t: Tuple[float, float]) -> 'Point':
        """Create Point from tuple."""
        return Point(t[0], t[1])
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple."""
        return (self.x, self.y)


def cross_product(o: Point, a: Point, b: Point) -> float:
    """
    Calculate cross product of vectors OA and OB.
    
    Returns:
        Positive: counter-clockwise turn
        Negative: clockwise turn
        Zero: collinear points
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def polar_angle(origin: Point, point: Point) -> float:
    """Calculate polar angle from origin to point."""
    return math.atan2(point.y - origin.y, point.x - origin.x)


def distance_sq(a: Point, b: Point) -> float:
    """Calculate squared distance between two points."""
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def graham_scan(points: List[Point]) -> List[Point]:
    """
    Graham Scan algorithm for convex hull.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        points: List of 2D points
        
    Returns:
        List of points forming the convex hull in counter-clockwise order
    """
    # Handle small or empty point sets
    if len(points) <= 2:
        return _remove_duplicates(points)
    
    # Find the point with lowest y (and lowest x if tied)
    start = min(points, key=lambda p: (p.y, p.x))
    
    # Sort points by polar angle with respect to start point
    # For collinear points (same angle), keep only the furthest one
    sorted_points = sorted(
        [p for p in points if p != start],
        key=lambda p: (polar_angle(start, p), distance_sq(start, p))
    )
    
    # Remove intermediate collinear points (keep only furthest for each angle)
    filtered_points = []
    for i in range(len(sorted_points)):
        if i == len(sorted_points) - 1:
            filtered_points.append(sorted_points[i])
        else:
            angle1 = polar_angle(start, sorted_points[i])
            angle2 = polar_angle(start, sorted_points[i + 1])
            if not math.isclose(angle1, angle2):
                filtered_points.append(sorted_points[i])
    
    # Initialize hull with start point and first two sorted points
    hull = [start]
    
    for point in filtered_points:
        # Remove points that create clockwise turn or are collinear
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull


def jarvis_march(points: List[Point]) -> List[Point]:
    """
    Jarvis March (Gift Wrapping) algorithm for convex hull.
    
    Time Complexity: O(nh) where h is the number of hull points
    Space Complexity: O(h)
    
    Best for: Small hull sizes (h << n)
    
    Args:
        points: List of 2D points
        
    Returns:
        List of points forming the convex hull in counter-clockwise order
    """
    # Find leftmost point
    leftmost = min(points, key=lambda p: p.x)
    
    # Handle small point sets
    if len(points) <= 2:
        return _remove_duplicates(points)
    
    hull = []
    current = leftmost
    
    while True:
        hull.append(current)
        
        # Find the most counter-clockwise point
        next_point = points[0]
        for point in points:
            if point == current:
                continue
            cp = cross_product(current, next_point, point)
            if cp < 0 or (cp == 0 and distance_sq(current, point) > distance_sq(current, next_point)):
                next_point = point
        
        current = next_point
        
        # Check if we've returned to start
        if current == leftmost:
            break
    
    return hull


def quickhull(points: List[Point]) -> List[Point]:
    """
    QuickHull algorithm for convex hull.
    
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(n)
    
    Often fastest in practice due to good cache locality.
    
    Args:
        points: List of 2D points
        
    Returns:
        List of points forming the convex hull in counter-clockwise order
    """
    # Find leftmost and rightmost points
    min_x = min(points, key=lambda p: p.x)
    max_x = max(points, key=lambda p: p.x)
    
    # Handle small point sets
    if len(points) <= 2:
        return _remove_duplicates(points)
    
    hull = set()
    hull.add(min_x)
    hull.add(max_x)
    
    # Split points into two halves
    left_set = []
    right_set = []
    
    for point in points:
        if point in hull:
            continue
        if cross_product(min_x, max_x, point) > 0:
            left_set.append(point)
        else:
            right_set.append(point)
    
    # Recursively find hull points
    _quickhull_recursive(min_x, max_x, left_set, hull)
    _quickhull_recursive(max_x, min_x, right_set, hull)
    
    # Convert to ordered list (counter-clockwise)
    return _order_hull_points(list(hull))


def _quickhull_recursive(a: Point, b: Point, points: List[Point], hull: set):
    """Recursive helper for QuickHull algorithm."""
    if not points:
        return
    
    # Find point furthest from line ab
    max_dist = -1
    furthest = None
    
    for point in points:
        dist = abs(cross_product(a, b, point))
        if dist > max_dist:
            max_dist = dist
            furthest = point
    
    if furthest is None or max_dist == 0:
        return
    
    hull.add(furthest)
    
    # Split remaining points
    left_set = []
    right_set = []
    
    for point in points:
        if point == furthest:
            continue
        if cross_product(a, furthest, point) > 0:
            left_set.append(point)
        elif cross_product(furthest, b, point) > 0:
            right_set.append(point)
    
    _quickhull_recursive(a, furthest, left_set, hull)
    _quickhull_recursive(furthest, b, right_set, hull)


def chans_algorithm(points: List[Point]) -> List[Point]:
    """
    Chan's algorithm for convex hull.
    
    Time Complexity: O(n log h) - optimal output-sensitive algorithm
    Space Complexity: O(n)
    
    Combines Graham Scan and Jarvis March for optimal performance.
    
    Args:
        points: List of 2D points
        
    Returns:
        List of points forming the convex hull in counter-clockwise order
    """
    # Handle small point sets directly with Graham scan
    if len(points) <= 20:
        return graham_scan(points)
    
    n = len(points)
    
    # Try different values of h (hull size)
    h = 1
    while True:
        result = _chan_with_h(points, h)
        if result is not None:
            return result
        h = min(n, h * 2)


def _chan_with_h(points: List[Point], h: int) -> Optional[List[Point]]:
    """Chan's algorithm with guessed hull size h."""
    n = len(points)
    m = min(h, n)
    
    # Split points into groups of size m
    groups = [points[i:i+m] for i in range(0, n, m)]
    
    # Compute partial hulls using Graham scan
    partial_hulls = [graham_scan(group) for group in groups if group]
    
    # Find the leftmost point overall
    leftmost = min(points, key=lambda p: p.x)
    
    # Jarvis march on partial hulls
    hull = []
    current = leftmost
    
    for _ in range(h):
        hull.append(current)
        next_point = None
        
        for partial_hull in partial_hulls:
            candidate = _find_tangent(current, partial_hull)
            if candidate is None:
                continue
            if next_point is None:
                next_point = candidate
            elif cross_product(current, next_point, candidate) < 0:
                next_point = candidate
            elif cross_product(current, next_point, candidate) == 0:
                if distance_sq(current, candidate) > distance_sq(current, next_point):
                    next_point = candidate
        
        if next_point is None or next_point == leftmost:
            break
        current = next_point
    
    # Check if we completed the hull (next_point was leftmost)
    # vs ran out of iterations (h too small)
    if len(hull) == h and current != leftmost and next_point != leftmost:
        return None  # h was too small
    
    return hull


def _find_tangent(point: Point, hull: List[Point]) -> Optional[Point]:
    """Find the right tangent point from external point to convex hull."""
    if not hull:
        return None
    
    # For small hulls, just iterate
    if len(hull) <= 3:
        # Find the most counter-clockwise point (smallest polar angle relative to point)
        min_angle = float('inf')
        tangent = None
        for p in hull:
            if p == point:
                continue
            angle = polar_angle(point, p)
            # Normalize to [0, 2*pi)
            while angle < 0:
                angle += 2 * math.pi
            if angle < min_angle:
                min_angle = angle
                tangent = p
        return tangent if tangent is not None else (hull[0] if hull[0] != point else None)
    
    # Binary search for tangent (assuming hull is in CCW order)
    n = len(hull)
    left = 0
    right = n - 1
    
    # Find the rightmost tangent (most clockwise from point's perspective)
    while left < right:
        mid = (left + right) // 2
        prev_idx = (mid - 1) % n
        next_idx = (mid + 1) % n
        
        # Skip the point itself
        if hull[mid] == point:
            mid = (mid + 1) % n
            prev_idx = (mid - 1) % n
            next_idx = (mid + 1) % n
        
        cp_prev = cross_product(point, hull[mid], hull[prev_idx])
        cp_next = cross_product(point, hull[mid], hull[next_idx])
        
        if cp_prev >= 0 and cp_next >= 0:
            return hull[mid]
        elif cp_prev < 0:
            right = mid
        else:
            left = mid + 1
    
    return hull[left] if hull[left] != point else None


def _remove_duplicates(points: List[Point]) -> List[Point]:
    """Remove duplicate points while preserving order."""
    seen = set()
    result = []
    for p in points:
        key = (round(p.x, 10), round(p.y, 10))
        if key not in seen:
            seen.add(key)
            result.append(p)
    return result


def _order_hull_points(points: List[Point]) -> List[Point]:
    """Order hull points in counter-clockwise order."""
    if len(points) <= 2:
        return points
    
    # Find centroid
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    centroid = Point(cx, cy)
    
    # Sort by polar angle from centroid
    return sorted(points, key=lambda p: polar_angle(centroid, p))


class ConvexHull:
    """
    Convex Hull class with multiple algorithms and utilities.
    """
    
    def __init__(self, points: List[Point], algorithm: HullAlgorithm = HullAlgorithm.GRAHAM_SCAN):
        """
        Initialize ConvexHull with points and algorithm.
        
        Args:
            points: List of 2D points
            algorithm: Algorithm to use (default: Graham Scan)
        """
        self.input_points = points
        self.algorithm = algorithm
        self._hull: Optional[List[Point]] = None
        self._area: Optional[float] = None
        self._perimeter: Optional[float] = None
        self._centroid: Optional[Point] = None
    
    def compute(self) -> List[Point]:
        """Compute convex hull using selected algorithm."""
        if self._hull is not None:
            return self._hull
        
        if not self.input_points:
            self._hull = []
            return self._hull
        
        algorithms = {
            HullAlgorithm.GRAHAM_SCAN: graham_scan,
            HullAlgorithm.JARVIS_MARCH: jarvis_march,
            HullAlgorithm.QUICKHULL: quickhull,
            HullAlgorithm.CHAN: chans_algorithm,
        }
        
        self._hull = algorithms[self.algorithm](self.input_points)
        return self._hull
    
    @property
    def hull(self) -> List[Point]:
        """Get convex hull points."""
        return self.compute()
    
    @property
    def area(self) -> float:
        """Calculate area of convex hull using Shoelace formula."""
        if self._area is not None:
            return self._area
        
        hull = self.compute()
        if len(hull) < 3:
            self._area = 0.0
            return self._area
        
        n = len(hull)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += hull[i].x * hull[j].y
            area -= hull[j].x * hull[i].y
        
        self._area = abs(area) / 2.0
        return self._area
    
    @property
    def perimeter(self) -> float:
        """Calculate perimeter of convex hull."""
        if self._perimeter is not None:
            return self._perimeter
        
        hull = self.compute()
        if len(hull) < 2:
            self._perimeter = 0.0
            return self._perimeter
        
        n = len(hull)
        self._perimeter = sum(hull[i].distance_to(hull[(i + 1) % n]) for i in range(n))
        return self._perimeter
    
    @property
    def centroid(self) -> Optional[Point]:
        """Calculate centroid of convex hull."""
        if self._centroid is not None:
            return self._centroid
        
        hull = self.compute()
        if len(hull) < 3:
            return None
        
        n = len(hull)
        # Use proper polygon centroid formula
        cx = 0.0
        cy = 0.0
        signed_area = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            cross = hull[i].x * hull[j].y - hull[j].x * hull[i].y
            signed_area += cross
            cx += (hull[i].x + hull[j].x) * cross
            cy += (hull[i].y + hull[j].y) * cross
        
        signed_area /= 2.0
        if signed_area == 0:
            # Degenerate case - use simple average
            cx = sum(p.x for p in hull) / n
            cy = sum(p.y for p in hull) / n
        else:
            cx /= (6 * signed_area)
            cy /= (6 * signed_area)
        
        self._centroid = Point(cx, cy)
        return self._centroid
    
    def contains(self, point: Point) -> bool:
        """
        Check if point is inside or on the convex hull.
        
        Uses cross product test for convex polygon containment.
        """
        hull = self.compute()
        if len(hull) < 3:
            return False
        
        n = len(hull)
        for i in range(n):
            if cross_product(hull[i], hull[(i + 1) % n], point) < 0:
                return False
        
        return True
    
    def convex_hull_contains(self, other: 'ConvexHull') -> bool:
        """Check if another convex hull is completely contained within this one."""
        return all(self.contains(p) for p in other.compute())
    
    def intersects(self, other: 'ConvexHull') -> bool:
        """Check if this convex hull intersects with another."""
        # Check if any edge of either hull intersects with the other
        my_hull = self.compute()
        other_hull = other.compute()
        
        # Check if any point is inside the other hull
        if any(self.contains(p) for p in other_hull):
            return True
        if any(other.contains(p) for p in my_hull):
            return True
        
        # Check edge intersections
        return self._edges_intersect(my_hull, other_hull)
    
    def _edges_intersect(self, hull1: List[Point], hull2: List[Point]) -> bool:
        """Check if any edges of two hulls intersect."""
        def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
            d1 = cross_product(p3, p4, p1)
            d2 = cross_product(p3, p4, p2)
            d3 = cross_product(p1, p2, p3)
            d4 = cross_product(p1, p2, p4)
            
            if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
               ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
                return True
            return False
        
        n1, n2 = len(hull1), len(hull2)
        
        for i in range(n1):
            for j in range(n2):
                if segments_intersect(
                    hull1[i], hull1[(i + 1) % n1],
                    hull2[j], hull2[(j + 1) % n2]
                ):
                    return True
        
        return False
    
    def bounding_box(self) -> Tuple[Point, Point]:
        """Get axis-aligned bounding box of convex hull."""
        hull = self.compute()
        if not hull:
            return Point(0, 0), Point(0, 0)
        
        min_x = min(p.x for p in hull)
        max_x = max(p.x for p in hull)
        min_y = min(p.y for p in hull)
        max_y = max(p.y for p in hull)
        
        return Point(min_x, min_y), Point(max_x, max_y)
    
    def scale(self, factor: float) -> 'ConvexHull':
        """Scale convex hull by factor (around centroid)."""
        hull = self.compute()
        if not hull:
            return ConvexHull([], self.algorithm)
        
        center = self.centroid
        if center is None:
            center = Point(0, 0)
        
        scaled_points = [
            Point(center.x + (p.x - center.x) * factor, 
                  center.y + (p.y - center.y) * factor)
            for p in self.input_points
        ]
        
        return ConvexHull(scaled_points, self.algorithm)
    
    def to_tuples(self) -> List[Tuple[float, float]]:
        """Convert hull points to list of tuples."""
        return [p.to_tuple() for p in self.compute()]
    
    def __repr__(self):
        return f"ConvexHull(points={len(self.input_points)}, hull={len(self.compute())}, algorithm={self.algorithm.value})"


def convex_hull(points: List[Tuple[float, float]], 
                algorithm: HullAlgorithm = HullAlgorithm.GRAHAM_SCAN) -> List[Tuple[float, float]]:
    """
    Convenience function to compute convex hull from list of tuples.
    
    Args:
        points: List of (x, y) tuples
        algorithm: Algorithm to use
        
    Returns:
        List of (x, y) tuples forming the convex hull
    """
    point_objects = [Point(p[0], p[1]) for p in points]
    hull_obj = ConvexHull(point_objects, algorithm)
    return hull_obj.to_tuples()


def convex_hull_area(points: List[Tuple[float, float]]) -> float:
    """Calculate area of convex hull from points."""
    point_objects = [Point(p[0], p[1]) for p in points]
    hull_obj = ConvexHull(point_objects)
    return hull_obj.area


def convex_hull_perimeter(points: List[Tuple[float, float]]) -> float:
    """Calculate perimeter of convex hull from points."""
    point_objects = [Point(p[0], p[1]) for p in points]
    hull_obj = ConvexHull(point_objects)
    return hull_obj.perimeter


def point_in_convex_hull(test_point: Tuple[float, float], 
                         hull_points: List[Tuple[float, float]]) -> bool:
    """Check if a point is inside a convex hull."""
    point_obj = Point(test_point[0], test_point[1])
    hull_point_objs = [Point(p[0], p[1]) for p in hull_points]
    hull_obj = ConvexHull(hull_point_objs)
    return hull_obj.contains(point_obj)


def merge_convex_hulls(hull1: List[Tuple[float, float]], 
                       hull2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Merge two convex hulls into one."""
    all_points = [Point(p[0], p[1]) for p in hull1 + hull2]
    hull_obj = ConvexHull(all_points)
    return hull_obj.to_tuples()


# Comparison function for benchmarking
def benchmark_algorithms(points: List[Tuple[float, float]], 
                         iterations: int = 100) -> dict:
    """
    Benchmark all algorithms on given points.
    
    Returns dictionary with algorithm names and execution times.
    """
    import time
    
    point_objects = [Point(p[0], p[1]) for p in points]
    
    results = {}
    
    algorithms = [
        ("graham_scan", HullAlgorithm.GRAHAM_SCAN),
        ("jarvis_march", HullAlgorithm.JARVIS_MARCH),
        ("quickhull", HullAlgorithm.QUICKHULL),
        ("chan", HullAlgorithm.CHAN),
    ]
    
    for name, algo in algorithms:
        start = time.perf_counter()
        for _ in range(iterations):
            ConvexHull(point_objects.copy(), algo).compute()
        elapsed = time.perf_counter() - start
        results[name] = elapsed / iterations
    
    return results


if __name__ == "__main__":
    # Quick demo
    demo_points = [
        (0, 0), (10, 0), (10, 10), (0, 10),
        (5, 5), (3, 3), (7, 7), (2, 8)
    ]
    
    print("Convex Hull Demo")
    print("=" * 40)
    print(f"Input points: {demo_points}")
    
    for algo in HullAlgorithm:
        hull = convex_hull(demo_points, algo)
        area = convex_hull_area(demo_points)
        print(f"\n{algo.value}:")
        print(f"  Hull points: {hull}")
        print(f"  Area: {area:.2f}")