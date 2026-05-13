#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Closest Pair Utilities - Basic Usage Example
==============================================
Demonstrates the basic functionality of closest pair utilities.
"""

import sys
import os

# Add module directory to path
mod_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mod_dir)

# Import directly from mod
from mod import (
    Point2D, Point3D, ClosestPair2D, ClosestPair3D,
    DistanceMetric, PointPair
)


def example_basic_2d():
    """Basic 2D closest pair example"""
    print("=" * 60)
    print("Basic 2D Closest Pair Example")
    print("=" * 60)
    
    points = [
        Point2D(0, 0),
        Point2D(1, 1),
        Point2D(2, 2),
        Point2D(10, 10),
        Point2D(11, 11),
        Point2D(50, 50)
    ]
    
    print("\nPoints:")
    for p in points:
        print(f"  {p}")
    
    finder = ClosestPair2D()
    result = finder.find_closest_pair(points)
    
    print(f"\nClosest pair: {result}")
    print(f"  Point 1: {result.point1}")
    print(f"  Point 2: {result.point2}")
    print(f"  Distance: {result.distance:.6f}")


def example_distance_metrics():
    """Compare different distance metrics"""
    print("\n" + "=" * 60)
    print("Distance Metrics Comparison")
    print("=" * 60)
    
    points = [
        Point2D(0, 0),
        Point2D(2, 3),
        Point2D(1, 1),
        Point2D(10, 10)
    ]
    
    print("\nPoints:", points)
    
    # Euclidean
    finder_euclidean = ClosestPair2D(DistanceMetric.EUCLIDEAN)
    result = finder_euclidean.find_closest_pair(points)
    print(f"\nEuclidean distance:")
    print(f"  Closest pair: {result.point1}, {result.point2}")
    print(f"  Distance: {result.distance:.4f} (= sqrt(2) = 1.414)")
    
    # Manhattan
    finder_manhattan = ClosestPair2D(DistanceMetric.MANHATTAN)
    result = finder_manhattan.find_closest_pair(points)
    print(f"\nManhattan distance:")
    print(f"  Closest pair: {result.point1}, {result.point2}")
    print(f"  Distance: {result.distance:.4f} (= |1| + |1| = 2)")
    
    # Chebyshev
    finder_chebyshev = ClosestPair2D(DistanceMetric.CHEBYSHEV)
    result = finder_chebyshev.find_closest_pair(points)
    print(f"\nChebyshev distance:")
    print(f"  Closest pair: {result.point1}, {result.point2}")
    print(f"  Distance: {result.distance:.4f} (= max(1, 1) = 1)")


def example_nearest_neighbor():
    """Nearest neighbor search example"""
    print("\n" + "=" * 60)
    print("Nearest Neighbor Search Example")
    print("=" * 60)
    
    # Create a grid of points
    points = []
    for i in range(0, 100, 10):
        for j in range(0, 100, 10):
            points.append(Point2D(i, j))
    
    query = Point2D(25, 35)
    
    finder = ClosestPair2D()
    nearest = finder.find_nearest_neighbor(points, query)
    
    print(f"\nGrid points: {len(points)} points (10x10 grid)")
    print(f"Query point: {query}")
    print(f"Nearest neighbor: {nearest}")
    print(f"Distance: {finder._distance_func(query, nearest):.4f}")


def example_radius_search():
    """Radius search example"""
    print("\n" + "=" * 60)
    print("Radius Search Example")
    print("=" * 60)
    
    # Create random points
    import random
    random.seed(42)
    points = [Point2D(random.uniform(0, 100), random.uniform(0, 100)) 
              for _ in range(50)]
    
    center = Point2D(50, 50)
    radius = 20
    
    finder = ClosestPair2D()
    nearby = finder.find_points_within_radius(points, center, radius)
    
    print(f"\nTotal points: {len(points)}")
    print(f"Center: {center}")
    print(f"Search radius: {radius}")
    print(f"Points within radius: {len(nearby)}")
    
    # Sort by distance and show closest ones
    nearby.sort(key=lambda p: finder._distance_func(p, center))
    print("\nClosest points within radius:")
    for p in nearby[:5]:
        dist = finder._distance_func(p, center)
        print(f"  {p} (distance: {dist:.4f})")


def example_k_closest_pairs():
    """Find k closest pairs example"""
    print("\n" + "=" * 60)
    print("K Closest Pairs Example")
    print("=" * 60)
    
    points = [
        Point2D(0, 0), Point2D(1, 0), Point2D(0, 1), Point2D(2, 0),
        Point2D(10, 10), Point2D(11, 11), Point2D(12, 12)
    ]
    
    finder = ClosestPair2D()
    pairs = finder.find_k_closest_pairs(points, k=5)
    
    print(f"\nPoints: {len(points)}")
    print(f"Finding top 5 closest pairs:\n")
    
    for i, pair in enumerate(pairs, 1):
        print(f"{i}. {pair.point1} <-> {pair.point2}")
        print(f"   Distance: {pair.distance:.6f}")


def example_3d():
    """3D closest pair example"""
    print("\n" + "=" * 60)
    print("3D Closest Pair Example")
    print("=" * 60)
    
    points = [
        Point3D(0, 0, 0),
        Point3D(1, 1, 1),
        Point3D(2, 2, 2),
        Point3D(10, 10, 10),
        Point3D(11, 11, 11)
    ]
    
    print("\n3D Points:")
    for p in points:
        print(f"  {p}")
    
    finder = ClosestPair3D()
    result = finder.find_closest_pair(points)
    
    print(f"\nClosest pair in 3D: {result}")
    print(f"  Point 1: {result.point1}")
    print(f"  Point 2: {result.point2}")
    print(f"  Distance: {result.distance:.6f} (= sqrt(3) ≈ 1.732)")


def example_city_locations():
    """Practical example: finding closest cities"""
    print("\n" + "=" * 60)
    print("Practical Example: Closest Cities")
    print("=" * 60)
    
    # Simulated city locations (x, y coordinates)
    cities = {
        "New York": Point2D(40.7, -74.0, id=1),
        "Los Angeles": Point2D(34.0, -118.2, id=2),
        "Chicago": Point2D(41.8, -87.6, id=3),
        "Houston": Point2D(29.7, -95.3, id=4),
        "Phoenix": Point2D(33.4, -112.0, id=5),
        "San Antonio": Point2D(29.4, -98.5, id=6),
        "San Diego": Point2D(32.7, -117.2, id=7),
        "Dallas": Point2D(32.8, -96.8, id=8),
        "San Jose": Point2D(37.3, -121.9, id=9),
        "Austin": Point2D(30.3, -97.7, id=10)
    }
    
    points = list(cities.values())
    
    finder = ClosestPair2D()
    result = finder.find_closest_pair(points)
    
    # Find city names by coordinates
    name1 = [name for name, p in cities.items() if p == result.point1][0]
    name2 = [name for name, p in cities.items() if p == result.point2][0]
    
    print(f"\nClosest pair of cities:")
    print(f"  {name1} ({result.point1})")
    print(f"  {name2} ({result.point2})")
    print(f"  Distance: {result.distance:.4f} degrees")


def main():
    """Run all examples"""
    example_basic_2d()
    example_distance_metrics()
    example_nearest_neighbor()
    example_radius_search()
    example_k_closest_pairs()
    example_3d()
    example_city_locations()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()