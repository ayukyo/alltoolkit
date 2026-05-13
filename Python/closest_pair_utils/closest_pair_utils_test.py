#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Closest Pair Utilities Test Suite
================================================
Comprehensive test suite for closest_pair_utils module.
"""

import math
import sys
import os
import unittest
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from closest_pair_utils.mod import (
    Point2D, Point3D, PointPair, DistanceMetric,
    ClosestPair2D, ClosestPair3D,
    euclidean_distance_2d, manhattan_distance_2d, chebyshev_distance_2d,
    euclidean_distance_3d, manhattan_distance_3d, chebyshev_distance_3d,
    find_closest_pair_2d, find_closest_pair_3d, find_nearest_neighbor_2d
)


class TestPoint2D(unittest.TestCase):
    """Test cases for Point2D class"""
    
    def test_point_creation(self):
        """Test point creation"""
        p = Point2D(3.5, 4.5)
        self.assertEqual(p.x, 3.5)
        self.assertEqual(p.y, 4.5)
        self.assertIsNone(p.id)
    
    def test_point_with_id(self):
        """Test point with ID"""
        p = Point2D(1.0, 2.0, id=5)
        self.assertEqual(p.id, 5)
    
    def test_point_equality(self):
        """Test point equality"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        p3 = Point2D(1.0, 3.0)
        
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
    
    def test_point_hash(self):
        """Test point hashing"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        
        self.assertEqual(hash(p1), hash(p2))
    
    def test_point_comparison(self):
        """Test point comparison"""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(2.0, 1.0)
        p3 = Point2D(1.0, 3.0)
        
        self.assertLess(p1, p2)
        self.assertLess(p1, p3)
    
    def test_point_to_tuple(self):
        """Test point to tuple conversion"""
        p = Point2D(3.0, 4.0)
        self.assertEqual(p.to_tuple(), (3.0, 4.0))


class TestPoint3D(unittest.TestCase):
    """Test cases for Point3D class"""
    
    def test_point_creation(self):
        """Test 3D point creation"""
        p = Point3D(1.0, 2.0, 3.0)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
        self.assertEqual(p.z, 3.0)
    
    def test_point_equality(self):
        """Test 3D point equality"""
        p1 = Point3D(1.0, 2.0, 3.0)
        p2 = Point3D(1.0, 2.0, 3.0)
        p3 = Point3D(1.0, 2.0, 4.0)
        
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)


class TestDistanceFunctions(unittest.TestCase):
    """Test cases for distance functions"""
    
    def test_euclidean_distance_2d(self):
        """Test Euclidean distance in 2D"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        
        # 3-4-5 triangle
        self.assertAlmostEqual(euclidean_distance_2d(p1, p2), 5.0)
        
        # Same point
        self.assertAlmostEqual(euclidean_distance_2d(p1, p1), 0.0)
        
        # Negative coordinates
        p3 = Point2D(-1, -1)
        self.assertAlmostEqual(euclidean_distance_2d(Point2D(0, 0), p3), math.sqrt(2))
    
    def test_manhattan_distance_2d(self):
        """Test Manhattan distance in 2D"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        
        self.assertEqual(manhattan_distance_2d(p1, p2), 7.0)
    
    def test_chebyshev_distance_2d(self):
        """Test Chebyshev distance in 2D"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        
        self.assertEqual(chebyshev_distance_2d(p1, p2), 4.0)  # max(3, 4)
    
    def test_euclidean_distance_3d(self):
        """Test Euclidean distance in 3D"""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 2)
        
        # sqrt(1 + 4 + 4) = 3
        self.assertAlmostEqual(euclidean_distance_3d(p1, p2), 3.0)
    
    def test_manhattan_distance_3d(self):
        """Test Manhattan distance in 3D"""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 3)
        
        self.assertEqual(manhattan_distance_3d(p1, p2), 6.0)
    
    def test_chebyshev_distance_3d(self):
        """Test Chebyshev distance in 3D"""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 3)
        
        self.assertEqual(chebyshev_distance_3d(p1, p2), 3.0)  # max(1, 2, 3)


class TestClosestPair2D(unittest.TestCase):
    """Test cases for ClosestPair2D class"""
    
    def test_basic_closest_pair(self):
        """Test basic closest pair finding"""
        points = [
            Point2D(0, 0),
            Point2D(1, 1),
            Point2D(10, 10),
            Point2D(11, 11)
        ]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(2), places=5)
    
    def test_empty_list(self):
        """Test with empty list"""
        finder = ClosestPair2D()
        result = finder.find_closest_pair([])
        self.assertIsNone(result)
    
    def test_single_point(self):
        """Test with single point"""
        finder = ClosestPair2D()
        result = finder.find_closest_pair([Point2D(0, 0)])
        self.assertIsNone(result)
    
    def test_two_points(self):
        """Test with exactly two points"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair([p1, p2])
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 5.0)
    
    def test_duplicate_points(self):
        """Test with duplicate points - should return distance 0"""
        points = [
            Point2D(0, 0),
            Point2D(0, 0),
            Point2D(0, 0)  # All same point
        ]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 0.0)
    
    def test_all_same_points(self):
        """Test with all same points"""
        points = [Point2D(5, 5), Point2D(5, 5), Point2D(5, 5)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 0.0)
    
    def test_closest_pair_manhattan(self):
        """Test closest pair with Manhattan distance"""
        points = [
            Point2D(0, 0),
            Point2D(1, 2),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D(DistanceMetric.MANHATTAN)
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 3.0)  # |1-0| + |2-0| = 3
    
    def test_closest_pair_chebyshev(self):
        """Test closest pair with Chebyshev distance"""
        points = [
            Point2D(0, 0),
            Point2D(2, 3),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D(DistanceMetric.CHEBYSHEV)
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 3.0)  # max(2, 3) = 3
    
    def test_find_k_closest_pairs(self):
        """Test finding k closest pairs"""
        points = [
            Point2D(0, 0),
            Point2D(1, 0),
            Point2D(0, 1),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D()
        result = finder.find_k_closest_pairs(points, 2)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].distance <= result[1].distance)
    
    def test_find_nearest_neighbor(self):
        """Test finding nearest neighbor"""
        points = [
            Point2D(0, 0),
            Point2D(1, 0),
            Point2D(0, 1),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D()
        query = Point2D(0.5, 0)
        
        result = finder.find_nearest_neighbor(points, query)
        self.assertIsNotNone(result)
        # (0.5, 0) is equidistant to (0, 0) and (1, 0) - both are 0.5 away
        self.assertTrue(result == Point2D(0, 0) or result == Point2D(1, 0))
    
    def test_find_points_within_radius(self):
        """Test finding points within radius"""
        points = [
            Point2D(0, 0),
            Point2D(1, 0),
            Point2D(0, 1),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D()
        center = Point2D(0, 0)
        
        result = finder.find_points_within_radius(points, center, 1.5)
        self.assertEqual(len(result), 3)  # (0,0), (1,0), (0,1)
    
    def test_large_dataset(self):
        """Test with large random dataset"""
        random.seed(42)
        points = [Point2D(random.uniform(0, 1000), random.uniform(0, 1000)) 
                  for _ in range(500)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        # Verify using brute force on subset
        self.assertIsNotNone(result)
        self.assertGreater(result.distance, 0)
    
    def test_collinear_points(self):
        """Test with collinear points"""
        points = [Point2D(i, 0) for i in range(100)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 1.0)
    
    def test_grid_points(self):
        """Test with grid points"""
        points = []
        for i in range(10):
            for j in range(10):
                points.append(Point2D(i, j))
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 1.0)


class TestClosestPair3D(unittest.TestCase):
    """Test cases for ClosestPair3D class"""
    
    def test_basic_closest_pair_3d(self):
        """Test basic closest pair in 3D"""
        points = [
            Point3D(0, 0, 0),
            Point3D(1, 1, 1),
            Point3D(10, 10, 10),
            Point3D(11, 11, 11)
        ]
        
        finder = ClosestPair3D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(3), places=5)
    
    def test_empty_list_3d(self):
        """Test 3D with empty list"""
        finder = ClosestPair3D()
        result = finder.find_closest_pair([])
        self.assertIsNone(result)
    
    def test_two_points_3d(self):
        """Test 3D with exactly two points"""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 2)
        
        finder = ClosestPair3D()
        result = finder.find_closest_pair([p1, p2])
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 3.0)  # sqrt(1+4+4) = 3
    
    def test_find_nearest_neighbor_3d(self):
        """Test finding nearest neighbor in 3D"""
        points = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(0, 1, 0),
            Point3D(10, 10, 10)
        ]
        
        finder = ClosestPair3D()
        query = Point3D(0.4, 0, 0)
        
        result = finder.find_nearest_neighbor(points, query)
        self.assertIsNotNone(result)
        self.assertEqual(result, Point3D(0, 0, 0))
    
    def test_manhattan_distance_3d(self):
        """Test 3D with Manhattan distance"""
        points = [
            Point3D(0, 0, 0),
            Point3D(1, 1, 1),
            Point3D(10, 10, 10)
        ]
        
        finder = ClosestPair3D(DistanceMetric.MANHATTAN)
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 3.0)
    
    def test_large_dataset_3d(self):
        """Test 3D with large random dataset"""
        random.seed(42)
        points = [Point3D(random.uniform(0, 100), random.uniform(0, 100), 
                          random.uniform(0, 100)) for _ in range(200)]
        
        finder = ClosestPair3D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertGreater(result.distance, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions"""
    
    def test_find_closest_pair_2d_tuples(self):
        """Test find_closest_pair_2d with tuples"""
        points = [(0, 0), (1, 1), (10, 10), (11, 11)]
        
        result = find_closest_pair_2d(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(2), places=5)
    
    def test_find_closest_pair_3d_tuples(self):
        """Test find_closest_pair_3d with tuples"""
        points = [(0, 0, 0), (1, 1, 1), (10, 10, 10), (11, 11, 11)]
        
        result = find_closest_pair_3d(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(3), places=5)
    
    def test_find_nearest_neighbor_2d_tuples(self):
        """Test find_nearest_neighbor_2d with tuples"""
        points = [(0, 0), (1, 0), (0, 1), (10, 10)]
        query = (0.5, 0)
        
        result = find_nearest_neighbor_2d(points, query)
        
        self.assertIsNotNone(result)
        # (0.5, 0) is equidistant to (0, 0) and (1, 0) - both are 0.5 away
        self.assertTrue(result == (0, 0) or result == (1, 0))
    
    def test_find_closest_pair_2d_manhattan(self):
        """Test find_closest_pair_2d with Manhattan metric"""
        points = [(0, 0), (1, 2), (10, 10)]
        
        result = find_closest_pair_2d(points, DistanceMetric.MANHATTAN)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 3.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_negative_coordinates(self):
        """Test with negative coordinates"""
        points = [
            Point2D(-10, -10),
            Point2D(-9, -9),
            Point2D(10, 10)
        ]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(2), places=5)
    
    def test_very_close_points(self):
        """Test with very close points"""
        points = [
            Point2D(0, 0),
            Point2D(1e-10, 1e-10),
            Point2D(100, 100)
        ]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, math.sqrt(2) * 1e-10, places=15)
    
    def test_very_distant_points(self):
        """Test with very distant points"""
        points = [
            Point2D(0, 0),
            Point2D(1e10, 0),
            Point2D(1e10, 1)
        ]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 1.0)
    
    def test_vertical_line(self):
        """Test points on vertical line"""
        points = [Point2D(5, i) for i in range(10)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 1.0)
    
    def test_horizontal_line(self):
        """Test points on horizontal line"""
        points = [Point2D(i, 5) for i in range(10)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.distance, 1.0)


class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def test_performance_2d_small(self):
        """Test 2D performance with small dataset"""
        random.seed(12345)
        points = [Point2D(random.uniform(0, 1000), random.uniform(0, 1000)) 
                  for _ in range(100)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
    
    def test_performance_2d_medium(self):
        """Test 2D performance with medium dataset"""
        random.seed(12345)
        points = [Point2D(random.uniform(0, 1000), random.uniform(0, 1000)) 
                  for _ in range(1000)]
        
        finder = ClosestPair2D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)
    
    def test_performance_3d_small(self):
        """Test 3D performance with small dataset"""
        random.seed(12345)
        points = [Point3D(random.uniform(0, 100), random.uniform(0, 100), 
                          random.uniform(0, 100)) for _ in range(100)]
        
        finder = ClosestPair3D()
        result = finder.find_closest_pair(points)
        
        self.assertIsNotNone(result)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPoint2D))
    suite.addTests(loader.loadTestsFromTestCase(TestPoint3D))
    suite.addTests(loader.loadTestsFromTestCase(TestDistanceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestClosestPair2D))
    suite.addTests(loader.loadTestsFromTestCase(TestClosestPair3D))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)