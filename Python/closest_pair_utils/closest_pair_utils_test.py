#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for closest_pair_utils"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Point2D, Point3D, PointPair,
    euclidean_distance_2d, manhattan_distance_2d, chebyshev_distance_2d,
    euclidean_distance_3d, manhattan_distance_3d, chebyshev_distance_3d,
    ClosestPair2D, ClosestPair3D,
    find_closest_pair_2d, find_closest_pair_3d,
    find_nearest_neighbor_2d,
    DistanceMetric
)

import unittest


class TestPoint2D(unittest.TestCase):
    def test_creation(self):
        p = Point2D(1.0, 2.0, id=1)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
        self.assertEqual(p.id, 1)

    def test_equality(self):
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        self.assertEqual(p1, p2)

    def test_to_tuple(self):
        p = Point2D(1.0, 2.0)
        self.assertEqual(p.to_tuple(), (1.0, 2.0))


class TestPoint3D(unittest.TestCase):
    def test_creation(self):
        p = Point3D(1.0, 2.0, 3.0, id=1)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
        self.assertEqual(p.z, 3.0)


class TestDistanceFunctions2D(unittest.TestCase):
    def test_euclidean(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertAlmostEqual(euclidean_distance_2d(p1, p2), 5.0, places=3)

    def test_manhattan(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(manhattan_distance_2d(p1, p2), 7)

    def test_chebyshev(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(chebyshev_distance_2d(p1, p2), 4)


class TestDistanceFunctions3D(unittest.TestCase):
    def test_euclidean_3d(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 2)
        dist = euclidean_distance_3d(p1, p2)
        self.assertAlmostEqual(dist, 3.0, places=3)

    def test_manhattan_3d(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 2)
        self.assertEqual(manhattan_distance_3d(p1, p2), 5)


class TestClosestPair2D(unittest.TestCase):
    def test_find_closest_pair(self):
        points = [Point2D(0, 0), Point2D(1, 0), Point2D(10, 10)]
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        self.assertIsNotNone(result)
        self.assertTrue(result.distance < 2.0)

    def test_find_closest_pair_single_point(self):
        points = [Point2D(0, 0)]
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        self.assertIsNone(result)

    def test_find_closest_pair_manhattan(self):
        points = [Point2D(0, 0), Point2D(1, 0), Point2D(10, 10)]
        finder = ClosestPair2D(DistanceMetric.MANHATTAN)
        result = finder.find_closest_pair(points)
        self.assertIsNotNone(result)

    def test_find_k_closest_pairs(self):
        points = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1), Point2D(10, 10)]
        finder = ClosestPair2D()
        results = finder.find_k_closest_pairs(points, 2)
        self.assertEqual(len(results), 2)

    def test_find_nearest_neighbor(self):
        points = [Point2D(0, 0), Point2D(5, 5), Point2D(10, 10)]
        finder = ClosestPair2D()
        query = Point2D(4, 4)
        nearest = finder.find_nearest_neighbor(points, query)
        self.assertIsNotNone(nearest)
        self.assertEqual(nearest.x, 5)
        self.assertEqual(nearest.y, 5)

    def test_find_points_within_radius(self):
        points = [Point2D(0, 0), Point2D(5, 5), Point2D(10, 10)]
        finder = ClosestPair2D()
        center = Point2D(0, 0)
        results = finder.find_points_within_radius(points, center, 10.0)
        self.assertEqual(len(results), 2)


class TestClosestPair3D(unittest.TestCase):
    def test_find_closest_pair_3d(self):
        points = [Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(10, 10, 10)]
        finder = ClosestPair3D()
        result = finder.find_closest_pair(points)
        self.assertIsNotNone(result)
        self.assertTrue(result.distance < 2.0)

    def test_find_nearest_neighbor_3d(self):
        points = [Point3D(0, 0, 0), Point3D(5, 5, 5), Point3D(10, 10, 10)]
        finder = ClosestPair3D()
        query = Point3D(4, 4, 4)
        nearest = finder.find_nearest_neighbor(points, query)
        self.assertIsNotNone(nearest)


class TestConvenienceFunctions(unittest.TestCase):
    def test_find_closest_pair_2d_tuples(self):
        points = [(0, 0), (1, 0), (10, 10)]
        result = find_closest_pair_2d(points)
        self.assertIsNotNone(result)

    def test_find_closest_pair_3d_tuples(self):
        points = [(0, 0, 0), (1, 0, 0), (10, 10, 10)]
        result = find_closest_pair_3d(points)
        self.assertIsNotNone(result)

    def test_find_nearest_neighbor_2d(self):
        points = [(0, 0), (5, 5), (10, 10)]
        query = (4, 4)
        result = find_nearest_neighbor_2d(points, query)
        self.assertEqual(result, (5, 5))


class TestPointPair(unittest.TestCase):
    def test_point_pair_repr(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(1, 0)
        pair = PointPair(p1, p2, 1.0)
        self.assertIn("PointPair", repr(pair))
        self.assertEqual(pair.distance, 1.0)


if __name__ == "__main__":
    unittest.main()