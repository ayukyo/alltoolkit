"""
Convex Hull Utilities - Usage Examples

This module demonstrates how to use the convex hull utilities for various applications.
"""

import sys
import os
# Add parent directory to path so we can import mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Point, HullAlgorithm, ConvexHull,
    graham_scan, jarvis_march, quickhull, chans_algorithm,
    convex_hull, convex_hull_area, convex_hull_perimeter,
    point_in_convex_hull, merge_convex_hulls,
    benchmark_algorithms,
)


def example_1_basic_usage():
    """Basic convex hull computation."""
    print("=" * 60)
    print("Example 1: Basic Convex Hull Computation")
    print("=" * 60)
    
    # Define points using tuples
    points = [
        (0, 0), (5, 0), (5, 5), (0, 5),
        (2, 2), (3, 3), (1, 4)  # Interior points
    ]
    
    # Compute convex hull using default algorithm (Graham Scan)
    hull = convex_hull(points)
    
    print(f"Input points: {len(points)}")
    print(f"Hull points: {len(hull)}")
    print(f"Hull vertices: {hull}")
    print()


def example_2_different_algorithms():
    """Compare different convex hull algorithms."""
    print("=" * 60)
    print("Example 2: Comparing Different Algorithms")
    print("=" * 60)
    
    points = [
        (0, 0), (10, 0), (10, 10), (0, 10),
        (5, 5), (3, 3), (7, 7), (2, 8), (8, 2)
    ]
    
    algorithms = [
        HullAlgorithm.GRAHAM_SCAN,
        HullAlgorithm.JARVIS_MARCH,
        HullAlgorithm.QUICKHULL,
        HullAlgorithm.CHAN,
    ]
    
    for algo in algorithms:
        hull = convex_hull(points, algo)
        area = convex_hull_area(points)
        perimeter = convex_hull_perimeter(points)
        print(f"\n{algo.value}:")
        print(f"  Hull size: {len(hull)} points")
        print(f"  Area: {area:.2f} square units")
        print(f"  Perimeter: {perimeter:.2f} units")
    
    print()


def example_3_point_class():
    """Using the Point class for more control."""
    print("=" * 60)
    print("Example 3: Using the Point Class")
    print("=" * 60)
    
    # Create Point objects
    points = [
        Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3),
        Point(2, 1.5)  # Interior point
    ]
    
    # Create ConvexHull object
    hull = ConvexHull(points, HullAlgorithm.QUICKHULL)
    
    # Access properties
    print(f"Number of input points: {len(points)}")
    print(f"Number of hull points: {len(hull.hull)}")
    print(f"Hull area: {hull.area:.2f}")
    print(f"Hull perimeter: {hull.perimeter:.2f}")
    print(f"Hull centroid: {hull.centroid}")
    
    # Point operations
    p1, p2 = points[0], points[1]
    print(f"\nDistance from {p1} to {p2}: {p1.distance_to(p2):.2f}")
    print(f"Sum: {p1} + {p2} = {p1 + p2}")
    print()


def example_4_point_containment():
    """Check if points are inside a convex hull."""
    print("=" * 60)
    print("Example 4: Point Containment Test")
    print("=" * 60)
    
    # Define hull vertices
    hull_points = [(0, 0), (5, 0), (5, 5), (0, 5)]
    
    # Points to test
    test_points = [
        (2.5, 2.5),  # Inside
        (0, 0),      # On vertex
        (2.5, 0),    # On edge
        (6, 6),      # Outside
        (-1, 2),     # Outside
    ]
    
    print(f"Hull vertices: {hull_points}")
    print("\nPoint containment tests:")
    
    for pt in test_points:
        inside = point_in_convex_hull(pt, hull_points)
        status = "INSIDE" if inside else "OUTSIDE"
        print(f"  {pt}: {status}")
    
    print()


def example_5_hull_operations():
    """Convex hull operations."""
    print("=" * 60)
    print("Example 5: Convex Hull Operations")
    print("=" * 60)
    
    # Create two hulls
    hull1 = ConvexHull([
        Point(0, 0), Point(3, 0), Point(3, 3), Point(0, 3)
    ])
    hull2 = ConvexHull([
        Point(2, 2), Point(5, 2), Point(5, 5), Point(2, 5)
    ])
    
    print(f"Hull 1 area: {hull1.area:.2f}")
    print(f"Hull 2 area: {hull2.area:.2f}")
    
    # Check intersection
    intersects = hull1.intersects(hull2)
    print(f"\nHulls intersect: {intersects}")
    
    # Check containment
    test_point = Point(1, 1)
    print(f"Point {test_point} in hull1: {hull1.contains(test_point)}")
    print(f"Point {test_point} in hull2: {hull2.contains(test_point)}")
    
    # Merge hulls
    merged = merge_convex_hulls(
        [p.to_tuple() for p in hull1.hull],
        [p.to_tuple() for p in hull2.hull]
    )
    print(f"\nMerged hull has {len(merged)} vertices")
    print(f"Merged hull vertices: {merged}")
    
    print()


def example_6_scaling():
    """Scale a convex hull."""
    print("=" * 60)
    print("Example 6: Scaling Convex Hulls")
    print("=" * 60)
    
    # Original hull
    points = [
        Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)
    ]
    hull = ConvexHull(points)
    
    print(f"Original hull area: {hull.area:.2f}")
    print(f"Original hull vertices: {[p.to_tuple() for p in hull.hull]}")
    
    # Scale by 2x
    scaled_2x = hull.scale(2)
    print(f"\n2x scaled hull area: {scaled_2x.area:.2f}")
    print(f"2x scaled vertices: {scaled_2x.to_tuples()}")
    
    # Scale by 0.5x
    scaled_half = hull.scale(0.5)
    print(f"\n0.5x scaled hull area: {scaled_half.area:.2f}")
    print(f"0.5x scaled vertices: {scaled_half.to_tuples()}")
    
    print()


def example_7_bounding_box():
    """Get bounding box of convex hull."""
    print("=" * 60)
    print("Example 7: Bounding Box")
    print("=" * 60)
    
    points = [
        (2, 3), (5, 1), (8, 4), (6, 7), (3, 6)
    ]
    
    hull = ConvexHull([Point(p[0], p[1]) for p in points])
    min_pt, max_pt = hull.bounding_box()
    
    print(f"Input points: {points}")
    print(f"Hull vertices: {hull.to_tuples()}")
    print(f"\nBounding box:")
    print(f"  Min: ({min_pt.x}, {min_pt.y})")
    print(f"  Max: ({max_pt.x}, {max_pt.y})")
    print(f"  Width: {max_pt.x - min_pt.x}")
    print(f"  Height: {max_pt.y - min_pt.y}")
    
    print()


def example_8_real_world_collisions():
    """Real-world application: collision detection."""
    print("=" * 60)
    print("Example 8: Collision Detection Application")
    print("=" * 60)
    
    # Define two game objects as point sets
    spaceship = ConvexHull([
        Point(0, 10), Point(5, 0), Point(0, 3), Point(-5, 0)
    ])
    
    asteroid = ConvexHull([
        Point(8, 8), Point(12, 6), Point(14, 10), Point(11, 14), Point(7, 12)
    ])
    
    # Check for collision
    if spaceship.intersects(asteroid):
        print("COLLISION DETECTED!")
    else:
        print("No collision - safe to proceed.")
    
    print(f"\nSpaceship area: {spaceship.area:.2f}")
    print(f"Asteroid area: {asteroid.area:.2f}")
    
    # Move asteroid closer
    moved_asteroid = ConvexHull([
        Point(2, 8), Point(6, 6), Point(8, 10), Point(5, 14), Point(1, 12)
    ])
    
    if spaceship.intersects(moved_asteroid):
        print("\nCOLLISION DETECTED with moved asteroid!")
    else:
        print("\nNo collision with moved asteroid.")
    
    print()


def example_9_algorithm_benchmark():
    """Benchmark different algorithms."""
    print("=" * 60)
    print("Example 9: Algorithm Benchmark")
    print("=" * 60)
    
    # Generate random-ish points
    import math
    points = []
    n = 100
    
    # Create points in a somewhat random pattern
    for i in range(n):
        angle = i * 2.4  # Golden angle approximation
        radius = 10 + (i % 10)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # Add some interior points
        if i % 3 == 0:
            x *= 0.5
            y *= 0.5
        points.append((x, y))
    
    print(f"Testing with {len(points)} points")
    print("\nAverage execution time per iteration:")
    print("-" * 40)
    
    results = benchmark_algorithms(points, iterations=50)
    
    for algo, time in sorted(results.items(), key=lambda x: x[1]):
        print(f"  {algo:15s}: {time*1000:.4f} ms")
    
    print()


def example_10_geographic_boundary():
    """Application: Geographic boundary calculation."""
    print("=" * 60)
    print("Example 10: Geographic Boundary Application")
    print("=" * 60)
    
    # GPS coordinates of various locations in a park
    # (simplified - not real GPS data)
    park_locations = [
        (0, 0),    # Entrance
        (100, 0),  # Corner
        (100, 50), # Fountain area
        (75, 75),  # Playground
        (100, 100),# Corner
        (50, 100), # Picnic area
        (0, 100),  # Corner
        (0, 50),   # Parking
        (50, 50),  # Center (interior)
        (40, 40),  # Interior
    ]
    
    # Compute boundary (convex hull)
    boundary = convex_hull(park_locations)
    boundary_area = convex_hull_area(park_locations)
    perimeter = convex_hull_perimeter(park_locations)
    
    print(f"Total locations: {len(park_locations)}")
    print(f"Boundary vertices: {len(boundary)}")
    print(f"Boundary area: {boundary_area:.2f} sq units")
    print(f"Boundary perimeter: {perimeter:.2f} units")
    
    # Check if new location is inside park boundary
    new_location = (60, 60)
    inside = point_in_convex_hull(new_location, boundary)
    print(f"\nNew location {new_location} inside park: {inside}")
    
    outside_location = (150, 50)
    outside = point_in_convex_hull(outside_location, boundary)
    print(f"Location {outside_location} inside park: {outside}")
    
    print()


def main():
    """Run all examples."""
    example_1_basic_usage()
    example_2_different_algorithms()
    example_3_point_class()
    example_4_point_containment()
    example_5_hull_operations()
    example_6_scaling()
    example_7_bounding_box()
    example_8_real_world_collisions()
    example_9_algorithm_benchmark()
    example_10_geographic_boundary()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()