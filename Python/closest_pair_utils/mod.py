#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Closest Pair Utilities Module
==========================================
A comprehensive closest pair of points utilities module for Python
with zero external dependencies.

Features:
    - Find closest pair of points in 2D plane using divide and conquer
    - Brute force method for small datasets
    - Support for multiple distance metrics (Euclidean, Manhattan, Chebyshev)
    - Find k closest pairs
    - Find nearest neighbor for a query point
    - Handle duplicate points
    - Support for 3D points

Algorithms:
    - Divide and Conquer: O(n log n)
    - Brute Force: O(n²)

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import List, Tuple, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum, auto


class DistanceMetric(Enum):
    """Distance metric types"""
    EUCLIDEAN = auto()
    MANHATTAN = auto()
    CHEBYSHEV = auto()


@dataclass
class Point2D:
    """2D Point representation"""
    x: float
    y: float
    id: Optional[int] = None
    
    def __repr__(self):
        if self.id is not None:
            return f"Point2D({self.x}, {self.y}, id={self.id})"
        return f"Point2D({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass
class Point3D:
    """3D Point representation"""
    x: float
    y: float
    z: float
    id: Optional[int] = None
    
    def __repr__(self):
        if self.id is not None:
            return f"Point3D({self.x}, {self.y}, {self.z}, id={self.id})"
        return f"Point3D({self.x}, {self.y}, {self.z})"
    
    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __lt__(self, other):
        if not isinstance(other, Point3D):
            return NotImplemented
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.z < other.z


@dataclass
class PointPair:
    """Result of closest pair calculation"""
    point1: Union[Point2D, Point3D]
    point2: Union[Point2D, Point3D]
    distance: float
    
    def __repr__(self):
        return f"PointPair({self.point1}, {self.point2}, dist={self.distance:.6f})"


def euclidean_distance_2d(p1: Point2D, p2: Point2D) -> float:
    """Calculate Euclidean distance between two 2D points"""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def manhattan_distance_2d(p1: Point2D, p2: Point2D) -> float:
    """Calculate Manhattan distance between two 2D points"""
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def chebyshev_distance_2d(p1: Point2D, p2: Point2D) -> float:
    """Calculate Chebyshev distance between two 2D points"""
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y))


def euclidean_distance_3d(p1: Point3D, p2: Point3D) -> float:
    """Calculate Euclidean distance between two 3D points"""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)


def manhattan_distance_3d(p1: Point3D, p2: Point3D) -> float:
    """Calculate Manhattan distance between two 3D points"""
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


def chebyshev_distance_3d(p1: Point3D, p2: Point3D) -> float:
    """Calculate Chebyshev distance between two 3D points"""
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y), abs(p1.z - p2.z))


class ClosestPair2D:
    """
    Closest pair of points finder for 2D points using divide and conquer.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    
    def __init__(self, metric: DistanceMetric = DistanceMetric.EUCLIDEAN):
        """
        Initialize closest pair finder.
        
        Args:
            metric: Distance metric to use
        """
        self.metric = metric
        self._distance_func = self._get_distance_func()
    
    def _get_distance_func(self) -> Callable[[Point2D, Point2D], float]:
        """Get the distance function based on metric"""
        if self.metric == DistanceMetric.EUCLIDEAN:
            return euclidean_distance_2d
        elif self.metric == DistanceMetric.MANHATTAN:
            return manhattan_distance_2d
        else:
            return chebyshev_distance_2d
    
    def find_closest_pair(self, points: List[Point2D]) -> Optional[PointPair]:
        """
        Find the closest pair of points.
        
        Args:
            points: List of 2D points
            
        Returns:
            PointPair with the two closest points and their distance,
            or None if less than 2 points
        """
        if len(points) < 2:
            return None
        
        # Remove duplicates
        unique_points = list(set(points))
        if len(unique_points) < 2:
            # All points are the same
            return PointPair(points[0], points[0], 0.0)
        
        # Sort by x-coordinate
        sorted_x = sorted(unique_points, key=lambda p: p.x)
        
        # Recursive divide and conquer
        result = self._closest_pair_recursive(sorted_x)
        return result
    
    def _closest_pair_recursive(self, points_x: List[Point2D]) -> PointPair:
        """Recursive divide and conquer algorithm"""
        n = len(points_x)
        
        # Base case: use brute force for small datasets
        if n <= 3:
            return self._brute_force(points_x)
        
        # Divide
        mid = n // 2
        mid_point = points_x[mid]
        
        left_points = points_x[:mid]
        right_points = points_x[mid:]
        
        # Conquer
        left_pair = self._closest_pair_recursive(left_points)
        right_pair = self._closest_pair_recursive(right_points)
        
        # Find minimum distance from left and right
        min_pair = left_pair if left_pair.distance < right_pair.distance else right_pair
        delta = min_pair.distance
        
        # Merge: check points within delta of the dividing line
        strip = [p for p in points_x if abs(p.x - mid_point.x) < delta]
        
        if len(strip) >= 2:
            strip_pair = self._strip_closest(strip, delta)
            if strip_pair.distance < min_pair.distance:
                min_pair = strip_pair
        
        return min_pair
    
    def _brute_force(self, points: List[Point2D]) -> PointPair:
        """Brute force O(n²) algorithm"""
        n = len(points)
        min_dist = float('inf')
        closest = PointPair(points[0], points[1], float('inf'))
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self._distance_func(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
                    closest = PointPair(points[i], points[j], dist)
        
        return closest
    
    def _strip_closest(self, strip: List[Point2D], delta: float) -> PointPair:
        """Find closest pair in the strip"""
        # Sort by y-coordinate
        strip.sort(key=lambda p: p.y)
        
        n = len(strip)
        min_dist = delta
        closest = PointPair(strip[0], strip[1], self._distance_func(strip[0], strip[1]))
        
        for i in range(n):
            for j in range(i + 1, n):
                # Break if y-distance exceeds delta
                if strip[j].y - strip[i].y >= min_dist:
                    break
                
                dist = self._distance_func(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    closest = PointPair(strip[i], strip[j], dist)
        
        return closest
    
    def find_k_closest_pairs(self, points: List[Point2D], k: int) -> List[PointPair]:
        """
        Find k closest pairs of points.
        
        Args:
            points: List of 2D points
            k: Number of pairs to find
            
        Returns:
            List of k closest PointPairs, sorted by distance
        """
        if len(points) < 2:
            return []
        
        if k >= len(points) * (len(points) - 1) // 2:
            # Return all pairs
            return self._all_pairs_sorted(points)[:k]
        
        # For k pairs, use brute force for simplicity
        # (More efficient algorithms exist but are complex)
        return self._all_pairs_sorted(points)[:k]
    
    def _all_pairs_sorted(self, points: List[Point2D]) -> List[PointPair]:
        """Get all pairs sorted by distance"""
        pairs = []
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                dist = self._distance_func(points[i], points[j])
                pairs.append(PointPair(points[i], points[j], dist))
        
        pairs.sort(key=lambda p: p.distance)
        return pairs
    
    def find_nearest_neighbor(self, points: List[Point2D], query: Point2D) -> Optional[Point2D]:
        """
        Find the nearest neighbor of a query point.
        
        Args:
            points: List of 2D points
            query: Query point
            
        Returns:
            Nearest point to query, or None if points is empty
        """
        if not points:
            return None
        
        min_dist = float('inf')
        nearest = None
        
        for point in points:
            dist = self._distance_func(point, query)
            if dist < min_dist:
                min_dist = dist
                nearest = point
        
        return nearest
    
    def find_points_within_radius(self, points: List[Point2D], center: Point2D, 
                                   radius: float) -> List[Point2D]:
        """
        Find all points within a given radius of a center point.
        
        Args:
            points: List of 2D points
            center: Center point
            radius: Search radius
            
        Returns:
            List of points within radius
        """
        result = []
        for point in points:
            if self._distance_func(point, center) <= radius:
                result.append(point)
        return result


class ClosestPair3D:
    """
    Closest pair of points finder for 3D points using divide and conquer.
    
    Time Complexity: O(n log² n)
    Space Complexity: O(n)
    """
    
    def __init__(self, metric: DistanceMetric = DistanceMetric.EUCLIDEAN):
        """
        Initialize closest pair finder.
        
        Args:
            metric: Distance metric to use
        """
        self.metric = metric
        self._distance_func = self._get_distance_func()
    
    def _get_distance_func(self) -> Callable[[Point3D, Point3D], float]:
        """Get the distance function based on metric"""
        if self.metric == DistanceMetric.EUCLIDEAN:
            return euclidean_distance_3d
        elif self.metric == DistanceMetric.MANHATTAN:
            return manhattan_distance_3d
        else:
            return chebyshev_distance_3d
    
    def find_closest_pair(self, points: List[Point3D]) -> Optional[PointPair]:
        """
        Find the closest pair of points.
        
        Args:
            points: List of 3D points
            
        Returns:
            PointPair with the two closest points and their distance,
            or None if less than 2 points
        """
        if len(points) < 2:
            return None
        
        # Remove duplicates
        unique_points = list(set(points))
        if len(unique_points) < 2:
            return PointPair(points[0], points[0], 0.0)
        
        # Sort by x-coordinate
        sorted_x = sorted(unique_points, key=lambda p: p.x)
        
        return self._closest_pair_recursive(sorted_x)
    
    def _closest_pair_recursive(self, points_x: List[Point3D]) -> PointPair:
        """Recursive divide and conquer algorithm for 3D"""
        n = len(points_x)
        
        # Base case
        if n <= 3:
            return self._brute_force(points_x)
        
        # Divide
        mid = n // 2
        mid_point = points_x[mid]
        
        left_points = points_x[:mid]
        right_points = points_x[mid:]
        
        # Conquer
        left_pair = self._closest_pair_recursive(left_points)
        right_pair = self._closest_pair_recursive(right_points)
        
        min_pair = left_pair if left_pair.distance < right_pair.distance else right_pair
        delta = min_pair.distance
        
        # Merge: check points within delta of the dividing plane
        strip = [p for p in points_x if abs(p.x - mid_point.x) < delta]
        
        if len(strip) >= 2:
            strip_pair = self._strip_closest(strip, delta)
            if strip_pair.distance < min_pair.distance:
                min_pair = strip_pair
        
        return min_pair
    
    def _brute_force(self, points: List[Point3D]) -> PointPair:
        """Brute force O(n²) algorithm for 3D"""
        n = len(points)
        min_dist = float('inf')
        closest = PointPair(points[0], points[1], float('inf'))
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self._distance_func(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
                    closest = PointPair(points[i], points[j], dist)
        
        return closest
    
    def _strip_closest(self, strip: List[Point3D], delta: float) -> PointPair:
        """Find closest pair in the strip for 3D"""
        # Sort by y-coordinate, then z
        strip.sort(key=lambda p: (p.y, p.z))
        
        n = len(strip)
        min_dist = delta
        closest = PointPair(strip[0], strip[1], self._distance_func(strip[0], strip[1]))
        
        for i in range(n):
            for j in range(i + 1, n):
                if strip[j].y - strip[i].y >= min_dist:
                    break
                
                for k in range(j, min(j + 6, n)):
                    if strip[k].z - strip[i].z >= min_dist:
                        continue
                    
                    dist = self._distance_func(strip[i], strip[k])
                    if dist < min_dist:
                        min_dist = dist
                        closest = PointPair(strip[i], strip[k], dist)
        
        return closest
    
    def find_nearest_neighbor(self, points: List[Point3D], query: Point3D) -> Optional[Point3D]:
        """Find the nearest neighbor of a query point"""
        if not points:
            return None
        
        min_dist = float('inf')
        nearest = points[0]
        
        for point in points:
            if point != query:
                dist = self._distance_func(point, query)
                if dist < min_dist:
                    min_dist = dist
                    nearest = point
        
        return nearest


# Convenience functions
def find_closest_pair_2d(points: List[Tuple[float, float]], 
                         metric: DistanceMetric = DistanceMetric.EUCLIDEAN) -> Optional[PointPair]:
    """
    Find the closest pair of 2D points.
    
    Args:
        points: List of (x, y) tuples
        metric: Distance metric to use
        
    Returns:
        PointPair with the two closest points and their distance
    """
    point_objects = [Point2D(x, y, i) for i, (x, y) in enumerate(points)]
    finder = ClosestPair2D(metric)
    return finder.find_closest_pair(point_objects)


def find_closest_pair_3d(points: List[Tuple[float, float, float]],
                         metric: DistanceMetric = DistanceMetric.EUCLIDEAN) -> Optional[PointPair]:
    """
    Find the closest pair of 3D points.
    
    Args:
        points: List of (x, y, z) tuples
        metric: Distance metric to use
        
    Returns:
        PointPair with the two closest points and their distance
    """
    point_objects = [Point3D(x, y, z, i) for i, (x, y, z) in enumerate(points)]
    finder = ClosestPair3D(metric)
    return finder.find_closest_pair(point_objects)


def find_nearest_neighbor_2d(points: List[Tuple[float, float]], 
                             query: Tuple[float, float],
                             metric: DistanceMetric = DistanceMetric.EUCLIDEAN) -> Optional[Tuple[float, float]]:
    """
    Find the nearest neighbor of a query point in 2D.
    
    Args:
        points: List of (x, y) tuples
        query: Query point (x, y)
        metric: Distance metric to use
        
    Returns:
        Nearest point as (x, y) tuple
    """
    point_objects = [Point2D(x, y, i) for i, (x, y) in enumerate(points)]
    query_point = Point2D(query[0], query[1])
    finder = ClosestPair2D(metric)
    nearest = finder.find_nearest_neighbor(point_objects, query_point)
    return (nearest.x, nearest.y) if nearest else None


if __name__ == "__main__":
    # Demo usage
    import random
    
    print("=" * 60)
    print("Closest Pair Utilities Demo")
    print("=" * 60)
    
    # Generate random 2D points
    random.seed(42)
    points_2d = [Point2D(random.uniform(0, 100), random.uniform(0, 100), i) 
                 for i in range(20)]
    
    print("\n2D Points:")
    for p in points_2d[:5]:
        print(f"  {p}")
    print(f"  ... and {len(points_2d) - 5} more")
    
    # Find closest pair
    finder_2d = ClosestPair2D()
    result = finder_2d.find_closest_pair(points_2d)
    print(f"\nClosest pair (Euclidean): {result}")
    
    # Using Manhattan distance
    finder_manhattan = ClosestPair2D(DistanceMetric.MANHATTAN)
    result_manhattan = finder_manhattan.find_closest_pair(points_2d)
    print(f"Closest pair (Manhattan): {result_manhattan}")
    
    # Find nearest neighbor
    query = Point2D(50, 50)
    nearest = finder_2d.find_nearest_neighbor(points_2d, query)
    print(f"\nNearest neighbor to {query}: {nearest}")
    
    # Find points within radius
    radius = 20
    nearby = finder_2d.find_points_within_radius(points_2d, query, radius)
    print(f"\nPoints within radius {radius} of {query}: {len(nearby)} points")
    
    # 3D example
    print("\n" + "=" * 60)
    print("3D Example")
    print("=" * 60)
    
    points_3d = [Point3D(random.uniform(0, 100), random.uniform(0, 100), 
                         random.uniform(0, 100), i) for i in range(15)]
    
    finder_3d = ClosestPair3D()
    result_3d = finder_3d.find_closest_pair(points_3d)
    print(f"\nClosest pair in 3D: {result_3d}")
    
    # Using convenience functions
    print("\n" + "=" * 60)
    print("Using Convenience Functions")
    print("=" * 60)
    
    tuple_points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(10)]
    result = find_closest_pair_2d(tuple_points)
    print(f"\nClosest pair from tuples: {result}")
    
    query_tuple = (50, 50)
    nearest = find_nearest_neighbor_2d(tuple_points, query_tuple)
    print(f"Nearest neighbor to {query_tuple}: {nearest}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)