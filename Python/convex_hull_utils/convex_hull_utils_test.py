"""
Test suite for Convex Hull Utilities.
"""

import unittest
import math
from mod import (
    Point, HullAlgorithm, ConvexHull,
    graham_scan, jarvis_march, quickhull, chans_algorithm,
    convex_hull, convex_hull_area, convex_hull_perimeter,
    point_in_convex_hull, merge_convex_hulls,
    cross_product, polar_angle, distance_sq,
)


class TestPoint(unittest.TestCase):
    """Test Point class."""
    
    def test_point_creation(self):
        p = Point(3.5, 4.5)
        self.assertEqual(p.x, 3.5)
        self.assertEqual(p.y, 4.5)
    
    def test_point_equality(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(1, 3)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
    
    def test_point_iteration(self):
        p = Point(1, 2)
        x, y = list(p)
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
    
    def test_point_tuple_conversion(self):
        p = Point(1, 2)
        t = p.to_tuple()
        self.assertEqual(t, (1, 2))
        
        p2 = Point.from_tuple((3, 4))
        self.assertEqual(p2.x, 3)
        self.assertEqual(p2.y, 4)
    
    def test_point_arithmetic(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        
        self.assertEqual(p1 + p2, Point(4, 6))
        self.assertEqual(p1 - p2, Point(-2, -2))
        self.assertEqual(p1 * 2, Point(2, 4))
        self.assertEqual(2 * p1, Point(2, 4))
    
    def test_point_distance(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0)
        self.assertAlmostEqual(p1.manhattan_distance_to(p2), 7.0)
    
    def test_point_hash(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        self.assertEqual(hash(p1), hash(p2))
        
        # Can be used in set
        point_set = {p1, p2}
        self.assertEqual(len(point_set), 1)


class TestCrossProduct(unittest.TestCase):
    """Test cross product calculation."""
    
    def test_counter_clockwise(self):
        o = Point(0, 0)
        a = Point(1, 0)
        b = Point(0, 1)
        self.assertGreater(cross_product(o, a, b), 0)
    
    def test_clockwise(self):
        o = Point(0, 0)
        a = Point(0, 1)
        b = Point(1, 0)
        self.assertLess(cross_product(o, a, b), 0)
    
    def test_collinear(self):
        o = Point(0, 0)
        a = Point(1, 1)
        b = Point(2, 2)
        self.assertEqual(cross_product(o, a, b), 0)


class TestGrahamScan(unittest.TestCase):
    """Test Graham Scan algorithm."""
    
    def test_square(self):
        points = [
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 4)
    
    def test_square_with_interior(self):
        points = [
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1),
            Point(0.5, 0.5)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 4)
    
    def test_triangle(self):
        points = [
            Point(0, 0), Point(1, 0), Point(0.5, 1)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 3)
    
    def test_line(self):
        points = [Point(0, 0), Point(1, 0), Point(2, 0)]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 2)
    
    def test_single_point(self):
        points = [Point(0, 0)]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 1)
    
    def test_empty(self):
        points = []
        hull = graham_scan(points)
        self.assertEqual(len(hull), 0)
    
    def test_collinear_points(self):
        points = [
            Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 2)
    
    def test_complex_shape(self):
        points = [
            Point(0, 0), Point(2, 1), Point(4, 0), Point(4, 3),
            Point(2, 2), Point(0, 3)
        ]
        hull = graham_scan(points)
        self.assertGreaterEqual(len(hull), 3)


class TestJarvisMarch(unittest.TestCase):
    """Test Jarvis March algorithm."""
    
    def test_square(self):
        points = [
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)
        ]
        hull = jarvis_march(points)
        self.assertEqual(len(hull), 4)
    
    def test_square_with_interior(self):
        points = [
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
            Point(1, 1)
        ]
        hull = jarvis_march(points)
        self.assertEqual(len(hull), 4)
    
    def test_triangle(self):
        points = [
            Point(0, 0), Point(2, 0), Point(1, 2)
        ]
        hull = jarvis_march(points)
        self.assertEqual(len(hull), 3)


class TestQuickHull(unittest.TestCase):
    """Test QuickHull algorithm."""
    
    def test_square(self):
        points = [
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)
        ]
        hull = quickhull(points)
        self.assertEqual(len(hull), 4)
    
    def test_square_with_interior(self):
        points = [
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
            Point(1, 1)
        ]
        hull = quickhull(points)
        self.assertEqual(len(hull), 4)
    
    def test_triangle(self):
        points = [
            Point(0, 0), Point(2, 0), Point(1, 2)
        ]
        hull = quickhull(points)
        self.assertEqual(len(hull), 3)
    
    def test_diamond(self):
        points = [
            Point(0, 2), Point(2, 0), Point(4, 2), Point(2, 4),
            Point(2, 2)  # interior point
        ]
        hull = quickhull(points)
        self.assertEqual(len(hull), 4)


class TestChansAlgorithm(unittest.TestCase):
    """Test Chan's algorithm."""
    
    def test_square(self):
        points = [
            Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)
        ]
        hull = chans_algorithm(points)
        self.assertEqual(len(hull), 4)
    
    def test_complex_shape(self):
        points = [
            Point(0, 0), Point(2, 1), Point(4, 0), Point(4, 3),
            Point(2, 2), Point(0, 3)
        ]
        hull = chans_algorithm(points)
        self.assertGreaterEqual(len(hull), 3)


class TestAlgorithmsConsistency(unittest.TestCase):
    """Test that all algorithms produce consistent results."""
    
    def setUp(self):
        self.test_cases = [
            # Simple square
            [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)],
            # Square with interior points
            [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),
             Point(0.5, 0.5), Point(1, 1), Point(1.5, 1.5)],
            # Random points
            [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1),
             Point(3, 0), Point(0, 0), Point(3, 3)],
            # Triangle
            [Point(0, 0), Point(4, 0), Point(2, 3), Point(1, 1), Point(3, 1)],
        ]
    
    def test_area_consistency(self):
        """All algorithms should produce hulls with same area."""
        algorithms = [
            HullAlgorithm.GRAHAM_SCAN,
            HullAlgorithm.JARVIS_MARCH,
            HullAlgorithm.QUICKHULL,
            HullAlgorithm.CHAN,
        ]
        
        for points in self.test_cases:
            areas = []
            for algo in algorithms:
                hull_obj = ConvexHull(points.copy(), algo)
                areas.append(round(hull_obj.area, 5))
            
            # All areas should be equal
            self.assertEqual(len(set(areas)), 1, 
                            f"Areas differ for points: {[p.to_tuple() for p in points]}")


class TestConvexHullClass(unittest.TestCase):
    """Test ConvexHull class."""
    
    def test_basic_properties(self):
        points = [
            Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)
        ]
        hull = ConvexHull(points)
        
        # Should be a 4x3 rectangle
        self.assertEqual(hull.area, 12.0)
        self.assertEqual(hull.perimeter, 14.0)
    
    def test_contains_point(self):
        points = [
            Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)
        ]
        hull = ConvexHull(points)
        
        # Interior point
        self.assertTrue(hull.contains(Point(2, 2)))
        # Vertex
        self.assertTrue(hull.contains(Point(0, 0)))
        # Edge point
        self.assertTrue(hull.contains(Point(2, 0)))
        # Exterior point
        self.assertFalse(hull.contains(Point(5, 5)))
    
    def test_bounding_box(self):
        points = [
            Point(2, 3), Point(5, 1), Point(7, 4), Point(4, 6)
        ]
        hull = ConvexHull(points)
        min_pt, max_pt = hull.bounding_box()
        
        self.assertEqual(min_pt.x, 2)
        self.assertEqual(min_pt.y, 1)
        self.assertEqual(max_pt.x, 7)
        self.assertEqual(max_pt.y, 6)
    
    def test_scale(self):
        points = [
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)
        ]
        hull = ConvexHull(points)
        scaled = hull.scale(2)
        
        # Scaled hull should have area 4x original
        self.assertAlmostEqual(scaled.area, hull.area * 4, places=5)
    
    def test_centroid(self):
        points = [
            Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)
        ]
        hull = ConvexHull(points)
        centroid = hull.centroid
        
        self.assertAlmostEqual(centroid.x, 1, places=5)
        self.assertAlmostEqual(centroid.y, 1, places=5)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_convex_hull_from_tuples(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        hull = convex_hull(points)
        
        self.assertEqual(len(hull), 4)
        # Check it returns tuples
        for point in hull:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
    
    def test_convex_hull_area(self):
        points = [(0, 0), (4, 0), (4, 3), (0, 3)]
        area = convex_hull_area(points)
        self.assertEqual(area, 12.0)
    
    def test_convex_hull_perimeter(self):
        points = [(0, 0), (4, 0), (4, 3), (0, 3)]
        perimeter = convex_hull_perimeter(points)
        self.assertEqual(perimeter, 14.0)
    
    def test_point_in_convex_hull(self):
        hull = [(0, 0), (2, 0), (2, 2), (0, 2)]
        
        self.assertTrue(point_in_convex_hull((1, 1), hull))
        self.assertTrue(point_in_convex_hull((0, 0), hull))
        self.assertFalse(point_in_convex_hull((3, 3), hull))
    
    def test_merge_convex_hulls(self):
        hull1 = [(0, 0), (1, 0), (1, 1), (0, 1)]
        hull2 = [(2, 0), (3, 0), (3, 1), (2, 1)]
        
        merged = merge_convex_hulls(hull1, hull2)
        # Merged hull should contain all 4 corners
        self.assertIn((0, 0), merged)
        self.assertIn((3, 0), merged)
        self.assertIn((3, 1), merged)
        self.assertIn((0, 1), merged)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_collinear_points(self):
        points = [Point(i, i) for i in range(10)]
        hull = graham_scan(points)
        # Should only have 2 points (endpoints)
        self.assertEqual(len(hull), 2)
    
    def test_duplicate_points(self):
        points = [
            Point(0, 0), Point(0, 0),
            Point(1, 0), Point(1, 0),
            Point(1, 1), Point(1, 1)
        ]
        hull = graham_scan(points)
        # Should handle duplicates
        self.assertLessEqual(len(hull), 6)
    
    def test_floating_point(self):
        points = [
            Point(0.1, 0.1), Point(1.5, 0.2), Point(1.3, 1.8), Point(0.2, 1.6)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 4)
    
    def test_large_coordinates(self):
        points = [
            Point(1000000, 1000000),
            Point(1000002, 1000000),
            Point(1000002, 1000002),
            Point(1000000, 1000002)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 4)
    
    def test_negative_coordinates(self):
        points = [
            Point(-1, -1), Point(1, -1), Point(1, 1), Point(-1, 1)
        ]
        hull = graham_scan(points)
        self.assertEqual(len(hull), 4)
        self.assertEqual(convex_hull_area([p.to_tuple() for p in points]), 4.0)


class TestConvexHullOperations(unittest.TestCase):
    """Test convex hull operations."""
    
    def test_hull_intersection(self):
        # Two overlapping squares
        hull1 = ConvexHull([Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
        hull2 = ConvexHull([Point(1, 1), Point(3, 1), Point(3, 3), Point(1, 3)])
        
        self.assertTrue(hull1.intersects(hull2))
    
    def test_hull_no_intersection(self):
        # Two non-overlapping squares
        hull1 = ConvexHull([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
        hull2 = ConvexHull([Point(2, 2), Point(3, 2), Point(3, 3), Point(2, 3)])
        
        self.assertFalse(hull1.intersects(hull2))
    
    def test_hull_contains_hull(self):
        large = ConvexHull([Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)])
        small = ConvexHull([Point(1, 1), Point(3, 1), Point(3, 3), Point(1, 3)])
        
        self.assertTrue(large.convex_hull_contains(small))
        self.assertFalse(small.convex_hull_contains(large))


if __name__ == "__main__":
    unittest.main()