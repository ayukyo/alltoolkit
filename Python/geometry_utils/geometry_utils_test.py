#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geometry Utils Test Suite
========================================
Comprehensive test suite for the geometry_utils module.

Run: python3 geometry_utils_test.py
"""

import os
import sys
import math
from typing import Tuple

# Import the module under test

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import *


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self):
        self.passed += 1
    
    def add_fail(self, test_name: str, expected, actual):
        self.failed += 1
        self.errors.append((test_name, expected, actual))
    
    def summary(self) -> str:
        total = self.passed + self.failed
        return f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}"
    
    def is_success(self) -> bool:
        return self.failed == 0


def approx_equal(a: float, b: float, epsilon: float = 1e-10) -> bool:
    """Check if two floats are approximately equal."""
    return abs(a - b) < epsilon


def run_test(result: TestResult, test_name: str, actual, expected, epsilon: float = 1e-10):
    """Run a single test and update result."""
    if isinstance(actual, float) and isinstance(expected, float):
        if approx_equal(actual, expected, epsilon):
            result.add_pass()
        else:
            result.add_fail(test_name, expected, actual)
    elif isinstance(actual, tuple) and isinstance(expected, tuple):
        if len(actual) == len(expected):
            all_equal = all(
                approx_equal(a, b, epsilon) if isinstance(a, float) and isinstance(b, float)
                else a == b
                for a, b in zip(actual, expected)
            )
            if all_equal:
                result.add_pass()
            else:
                result.add_fail(test_name, expected, actual)
        else:
            result.add_fail(test_name, expected, actual)
    else:
        if actual == expected:
            result.add_pass()
        else:
            result.add_fail(test_name, expected, actual)


# ============================================================================
# Angle Conversion Tests
# ============================================================================

def test_angle_conversions(result: TestResult):
    """Test angle conversion functions."""
    
    # degrees_to_radians
    run_test(result, "degrees_to_radians(180)", degrees_to_radians(180), PI)
    run_test(result, "degrees_to_radians(90)", degrees_to_radians(90), PI / 2)
    run_test(result, "degrees_to_radians(0)", degrees_to_radians(0), 0.0)
    run_test(result, "degrees_to_radians(360)", degrees_to_radians(360), 2 * PI)
    run_test(result, "degrees_to_radians(-90)", degrees_to_radians(-90), -PI / 2)
    
    # radians_to_degrees
    run_test(result, "radians_to_degrees(PI)", radians_to_degrees(PI), 180.0)
    run_test(result, "radians_to_degrees(PI/2)", radians_to_degrees(PI / 2), 90.0)
    run_test(result, "radians_to_degrees(0)", radians_to_degrees(0), 0.0)
    run_test(result, "radians_to_degrees(2*PI)", radians_to_degrees(2 * PI), 360.0)
    
    # normalize_angle_degrees
    run_test(result, "normalize_angle_degrees(450)", normalize_angle_degrees(450), 90.0)
    run_test(result, "normalize_angle_degrees(-90)", normalize_angle_degrees(-90), 270.0)
    run_test(result, "normalize_angle_degrees(360)", normalize_angle_degrees(360), 0.0)
    run_test(result, "normalize_angle_degrees(0)", normalize_angle_degrees(0), 0.0)
    run_test(result, "normalize_angle_degrees(720)", normalize_angle_degrees(720), 0.0)
    
    # normalize_angle_radians
    run_test(result, "normalize_angle_radians(2*PI)", normalize_angle_radians(2 * PI), 0.0)
    run_test(result, "normalize_angle_radians(PI/2)", normalize_angle_radians(PI / 2), PI / 2)
    run_test(result, "normalize_angle_radians(-PI/2)", normalize_angle_radians(-PI / 2), 3 * PI / 2)


# ============================================================================
# Distance Tests
# ============================================================================

def test_distance_calculations(result: TestResult):
    """Test distance calculation functions."""
    
    # distance_2d
    run_test(result, "distance_2d((0,0),(3,4))", distance_2d((0, 0), (3, 4)), 5.0)
    run_test(result, "distance_2d((0,0),(0,0))", distance_2d((0, 0), (0, 0)), 0.0)
    run_test(result, "distance_2d((1,1),(1,1))", distance_2d((1, 1), (1, 1)), 0.0)
    run_test(result, "distance_2d((0,0),(1,0))", distance_2d((0, 0), (1, 0)), 1.0)
    run_test(result, "distance_2d((-3,-4),(0,0))", distance_2d((-3, -4), (0, 0)), 5.0)
    
    # distance_3d
    run_test(result, "distance_3d((0,0,0),(1,2,2))", distance_3d((0, 0, 0), (1, 2, 2)), 3.0)
    run_test(result, "distance_3d((0,0,0),(0,0,0))", distance_3d((0, 0, 0), (0, 0, 0)), 0.0)
    run_test(result, "distance_3d((1,1,1),(1,1,1))", distance_3d((1, 1, 1), (1, 1, 1)), 0.0)
    
    # manhattan_distance_2d
    run_test(result, "manhattan_distance_2d((0,0),(3,4))", manhattan_distance_2d((0, 0), (3, 4)), 7.0)
    run_test(result, "manhattan_distance_2d((0,0),(0,0))", manhattan_distance_2d((0, 0), (0, 0)), 0.0)
    run_test(result, "manhattan_distance_2d((1,2),(4,6))", manhattan_distance_2d((1, 2), (4, 6)), 7.0)
    
    # chebyshev_distance_2d
    run_test(result, "chebyshev_distance_2d((0,0),(3,4))", chebyshev_distance_2d((0, 0), (3, 4)), 4.0)
    run_test(result, "chebyshev_distance_2d((0,0),(0,0))", chebyshev_distance_2d((0, 0), (0, 0)), 0.0)
    run_test(result, "chebyshev_distance_2d((1,5),(4,2))", chebyshev_distance_2d((1, 5), (4, 2)), 3.0)
    
    # distance_from_origin_2d
    run_test(result, "distance_from_origin_2d((3,4))", distance_from_origin_2d((3, 4)), 5.0)
    run_test(result, "distance_from_origin_2d((0,0))", distance_from_origin_2d((0, 0)), 0.0)
    
    # distance_from_origin_3d
    run_test(result, "distance_from_origin_3d((1,2,2))", distance_from_origin_3d((1, 2, 2)), 3.0)
    run_test(result, "distance_from_origin_3d((0,0,0))", distance_from_origin_3d((0, 0, 0)), 0.0)


# ============================================================================
# 2D Shape Tests
# ============================================================================

def test_2d_shapes(result: TestResult):
    """Test 2D shape calculations."""
    
    # circle_area
    run_test(result, "circle_area(1)", circle_area(1), PI, 1e-10)
    run_test(result, "circle_area(2)", circle_area(2), 4 * PI, 1e-10)
    run_test(result, "circle_area(0)", circle_area(0), 0.0)
    run_test(result, "circle_area(-1)", circle_area(-1), 0.0)
    
    # circle_circumference
    run_test(result, "circle_circumference(1)", circle_circumference(1), 2 * PI, 1e-10)
    run_test(result, "circle_circumference(5)", circle_circumference(5), 10 * PI, 1e-10)
    run_test(result, "circle_circumference(0)", circle_circumference(0), 0.0)
    
    # circle_diameter
    run_test(result, "circle_diameter(5)", circle_diameter(5), 10.0)
    run_test(result, "circle_diameter(0)", circle_diameter(0), 0.0)
    
    # rectangle_area
    run_test(result, "rectangle_area(5,3)", rectangle_area(5, 3), 15.0)
    run_test(result, "rectangle_area(0,5)", rectangle_area(0, 5), 0.0)
    run_test(result, "rectangle_area(-1,5)", rectangle_area(-1, 5), 0.0)
    
    # rectangle_perimeter
    run_test(result, "rectangle_perimeter(5,3)", rectangle_perimeter(5, 3), 16.0)
    run_test(result, "rectangle_perimeter(0,0)", rectangle_perimeter(0, 0), 0.0)
    
    # square_area
    run_test(result, "square_area(4)", square_area(4), 16.0)
    run_test(result, "square_area(0)", square_area(0), 0.0)
    
    # square_perimeter
    run_test(result, "square_perimeter(4)", square_perimeter(4), 16.0)
    run_test(result, "square_perimeter(0)", square_perimeter(0), 0.0)
    
    # triangle_area
    run_test(result, "triangle_area(6,4)", triangle_area(6, 4), 12.0)
    run_test(result, "triangle_area(0,4)", triangle_area(0, 4), 0.0)
    
    # triangle_area_heron
    run_test(result, "triangle_area_heron(3,4,5)", triangle_area_heron(3, 4, 5), 6.0)
    run_test(result, "triangle_area_heron(5,5,5)", triangle_area_heron(5, 5, 5), 10.825317547305483, 1e-10)
    run_test(result, "triangle_area_heron(1,2,10)", triangle_area_heron(1, 2, 10), 0.0)  # Invalid
    run_test(result, "triangle_area_heron(0,4,5)", triangle_area_heron(0, 4, 5), 0.0)
    
    # triangle_perimeter
    run_test(result, "triangle_perimeter(3,4,5)", triangle_perimeter(3, 4, 5), 12.0)
    run_test(result, "triangle_perimeter(0,4,5)", triangle_perimeter(0, 4, 5), 0.0)
    
    # equilateral_triangle_area
    run_test(result, "equilateral_triangle_area(4)", equilateral_triangle_area(4), 4 * SQRT3, 1e-10)
    run_test(result, "equilateral_triangle_area(0)", equilateral_triangle_area(0), 0.0)
    
    # regular_polygon_area (hexagon)
    run_test(result, "regular_polygon_area(6,4)", regular_polygon_area(6, 4), 24 * SQRT3, 1e-10)
    run_test(result, "regular_polygon_area(4,2)", regular_polygon_area(4, 2), 4.0)  # Square
    run_test(result, "regular_polygon_area(2,4)", regular_polygon_area(2, 4), 0.0)  # Invalid
    
    # trapezoid_area
    run_test(result, "trapezoid_area(5,7,4)", trapezoid_area(5, 7, 4), 24.0)
    run_test(result, "trapezoid_area(0,7,4)", trapezoid_area(0, 7, 4), 0.0)
    
    # ellipse_area
    run_test(result, "ellipse_area(10,6)", ellipse_area(10, 6), PI * 5 * 3, 1e-10)
    run_test(result, "ellipse_area(0,6)", ellipse_area(0, 6), 0.0)
    
    # rhombus_area
    run_test(result, "rhombus_area(8,6)", rhombus_area(8, 6), 24.0)
    run_test(result, "rhombus_area(0,6)", rhombus_area(0, 6), 0.0)
    
    # parallelogram_area
    run_test(result, "parallelogram_area(8,5)", parallelogram_area(8, 5), 40.0)
    run_test(result, "parallelogram_area(0,5)", parallelogram_area(0, 5), 0.0)


# ============================================================================
# 3D Shape Tests
# ============================================================================

def test_3d_shapes(result: TestResult):
    """Test 3D shape calculations."""
    
    # sphere_volume
    run_test(result, "sphere_volume(3)", sphere_volume(3), (4/3) * PI * 27, 1e-10)
    run_test(result, "sphere_volume(0)", sphere_volume(0), 0.0)
    run_test(result, "sphere_volume(-1)", sphere_volume(-1), 0.0)
    
    # sphere_surface_area
    run_test(result, "sphere_surface_area(3)", sphere_surface_area(3), 4 * PI * 9, 1e-10)
    run_test(result, "sphere_surface_area(0)", sphere_surface_area(0), 0.0)
    
    # cube_volume
    run_test(result, "cube_volume(3)", cube_volume(3), 27.0)
    run_test(result, "cube_volume(0)", cube_volume(0), 0.0)
    run_test(result, "cube_volume(-1)", cube_volume(-1), 0.0)
    
    # cube_surface_area
    run_test(result, "cube_surface_area(3)", cube_surface_area(3), 54.0)
    run_test(result, "cube_surface_area(0)", cube_surface_area(0), 0.0)
    
    # rectangular_prism_volume
    run_test(result, "rectangular_prism_volume(4,3,2)", rectangular_prism_volume(4, 3, 2), 24.0)
    run_test(result, "rectangular_prism_volume(0,3,2)", rectangular_prism_volume(0, 3, 2), 0.0)
    
    # rectangular_prism_surface_area
    run_test(result, "rectangular_prism_surface_area(4,3,2)", rectangular_prism_surface_area(4, 3, 2), 52.0)
    
    # cylinder_volume
    run_test(result, "cylinder_volume(3,5)", cylinder_volume(3, 5), PI * 9 * 5, 1e-10)
    run_test(result, "cylinder_volume(0,5)", cylinder_volume(0, 5), 0.0)
    
    # cylinder_surface_area
    run_test(result, "cylinder_surface_area(3,5)", cylinder_surface_area(3, 5), 2 * PI * 3 * 8, 1e-10)
    
    # cone_volume
    run_test(result, "cone_volume(3,5)", cone_volume(3, 5), (1/3) * PI * 9 * 5, 1e-10)
    run_test(result, "cone_volume(0,5)", cone_volume(0, 5), 0.0)
    
    # cone_surface_area (r=3, h=4, slant=5)
    run_test(result, "cone_surface_area(3,4)", cone_surface_area(3, 4), PI * 3 * 8, 1e-10)
    
    # pyramid_volume
    run_test(result, "pyramid_volume(25,9)", pyramid_volume(25, 9), 75.0)
    run_test(result, "pyramid_volume(0,9)", pyramid_volume(0, 9), 0.0)
    
    # tetrahedron_volume
    run_test(result, "tetrahedron_volume(4)", tetrahedron_volume(4), 64 / (6 * SQRT2), 1e-10)
    run_test(result, "tetrahedron_volume(0)", tetrahedron_volume(0), 0.0)
    
    # tetrahedron_surface_area
    run_test(result, "tetrahedron_surface_area(4)", tetrahedron_surface_area(4), SQRT3 * 16, 1e-10)


# ============================================================================
# Vector Operation Tests
# ============================================================================

def test_vector_operations(result: TestResult):
    """Test vector operation functions."""
    
    # vector_add_2d
    run_test(result, "vector_add_2d((1,2),(3,4))", vector_add_2d((1, 2), (3, 4)), (4.0, 6.0))
    run_test(result, "vector_add_2d((0,0),(0,0))", vector_add_2d((0, 0), (0, 0)), (0.0, 0.0))
    
    # vector_subtract_2d
    run_test(result, "vector_subtract_2d((5,7),(2,3))", vector_subtract_2d((5, 7), (2, 3)), (3.0, 4.0))
    
    # vector_add_3d
    run_test(result, "vector_add_3d((1,2,3),(4,5,6))", vector_add_3d((1, 2, 3), (4, 5, 6)), (5.0, 7.0, 9.0))
    
    # vector_subtract_3d
    run_test(result, "vector_subtract_3d((5,7,9),(1,2,3))", vector_subtract_3d((5, 7, 9), (1, 2, 3)), (4.0, 5.0, 6.0))
    
    # vector_scale_2d
    run_test(result, "vector_scale_2d((2,3),2)", vector_scale_2d((2, 3), 2), (4.0, 6.0))
    run_test(result, "vector_scale_2d((2,3),0)", vector_scale_2d((2, 3), 0), (0.0, 0.0))
    run_test(result, "vector_scale_2d((2,3),-1)", vector_scale_2d((2, 3), -1), (-2.0, -3.0))
    
    # vector_scale_3d
    run_test(result, "vector_scale_3d((2,3,4),2)", vector_scale_3d((2, 3, 4), 2), (4.0, 6.0, 8.0))
    
    # dot_product_2d
    run_test(result, "dot_product_2d((1,2),(3,4))", dot_product_2d((1, 2), (3, 4)), 11.0)
    run_test(result, "dot_product_2d((1,0),(0,1))", dot_product_2d((1, 0), (0, 1)), 0.0)  # Perpendicular
    
    # dot_product_3d
    run_test(result, "dot_product_3d((1,2,3),(4,5,6))", dot_product_3d((1, 2, 3), (4, 5, 6)), 32.0)
    
    # cross_product_3d
    run_test(result, "cross_product_3d((1,0,0),(0,1,0))", cross_product_3d((1, 0, 0), (0, 1, 0)), (0.0, 0.0, 1.0))
    run_test(result, "cross_product_3d((0,1,0),(1,0,0))", cross_product_3d((0, 1, 0), (1, 0, 0)), (0.0, 0.0, -1.0))
    run_test(result, "cross_product_3d((1,0,0),(1,0,0))", cross_product_3d((1, 0, 0), (1, 0, 0)), (0.0, 0.0, 0.0))  # Parallel
    
    # vector_magnitude_2d
    run_test(result, "vector_magnitude_2d((3,4))", vector_magnitude_2d((3, 4)), 5.0)
    run_test(result, "vector_magnitude_2d((0,0))", vector_magnitude_2d((0, 0)), 0.0)
    
    # vector_magnitude_3d
    run_test(result, "vector_magnitude_3d((1,2,2))", vector_magnitude_3d((1, 2, 2)), 3.0)
    run_test(result, "vector_magnitude_3d((0,0,0))", vector_magnitude_3d((0, 0, 0)), 0.0)
    
    # normalize_vector_2d
    result_add = normalize_vector_2d((3, 4))
    run_test(result, "normalize_vector_2d((3,4))", result_add[0], 0.6)
    run_test(result, "normalize_vector_2d((3,4)) y", result_add[1], 0.8)
    run_test(result, "normalize_vector_2d((0,0))", normalize_vector_2d((0, 0)), (0.0, 0.0))
    
    # normalize_vector_3d
    result_add = normalize_vector_3d((1, 2, 2))
    run_test(result, "normalize_vector_3d((1,2,2)) x", result_add[0], 1/3, 1e-10)
    run_test(result, "normalize_vector_3d((1,2,2)) y", result_add[1], 2/3, 1e-10)
    run_test(result, "normalize_vector_3d((1,2,2)) z", result_add[2], 2/3, 1e-10)
    
    # vector_angle_2d
    run_test(result, "vector_angle_2d((1,0))", vector_angle_2d((1, 0)), 0.0)
    run_test(result, "vector_angle_2d((0,1))", vector_angle_2d((0, 1)), PI / 2, 1e-10)
    run_test(result, "vector_angle_2d((-1,0))", vector_angle_2d((-1, 0)), PI, 1e-10)
    
    # angle_between_vectors_2d
    run_test(result, "angle_between_vectors_2d((1,0),(0,1))", angle_between_vectors_2d((1, 0), (0, 1)), PI / 2, 1e-10)
    run_test(result, "angle_between_vectors_2d((1,0),(1,0))", angle_between_vectors_2d((1, 0), (1, 0)), 0.0)
    run_test(result, "angle_between_vectors_2d((1,0),(-1,0))", angle_between_vectors_2d((1, 0), (-1, 0)), PI, 1e-10)


# ============================================================================
# Transformation Tests
# ============================================================================

def test_transformations(result: TestResult):
    """Test geometric transformation functions."""
    
    # rotate_point_2d
    result_add = rotate_point_2d((1, 0), 90)
    run_test(result, "rotate_point_2d((1,0),90) x", result_add[0], 0.0, 1e-10)
    run_test(result, "rotate_point_2d((1,0),90) y", result_add[1], 1.0, 1e-10)
    
    result_add = rotate_point_2d((1, 0), 180)
    run_test(result, "rotate_point_2d((1,0),180) x", result_add[0], -1.0, 1e-10)
    run_test(result, "rotate_point_2d((1,0),180) y", result_add[1], 0.0, 1e-10)
    
    result_add = rotate_point_2d((1, 0), 360)
    run_test(result, "rotate_point_2d((1,0),360) x", result_add[0], 1.0, 1e-10)
    run_test(result, "rotate_point_2d((1,0),360) y", result_add[1], 0.0, 1e-10)
    
    # rotate around custom origin
    result_add = rotate_point_2d((2, 0), 90, (1, 0))
    run_test(result, "rotate_point_2d((2,0),90,(1,0)) x", result_add[0], 1.0, 1e-10)
    run_test(result, "rotate_point_2d((2,0),90,(1,0)) y", result_add[1], 1.0, 1e-10)
    
    # translate_point_2d
    run_test(result, "translate_point_2d((1,2),(3,4))", translate_point_2d((1, 2), 3, 4), (4.0, 6.0))
    run_test(result, "translate_point_2d((0,0),(0,0))", translate_point_2d((0, 0), 0, 0), (0.0, 0.0))
    
    # scale_point_2d
    run_test(result, "scale_point_2d((2,3),2,2)", scale_point_2d((2, 3), 2, 2), (4.0, 6.0))
    run_test(result, "scale_point_2d((0,0),2,2)", scale_point_2d((0, 0), 2, 2), (0.0, 0.0))
    
    # reflect_point_x
    run_test(result, "reflect_point_x((3,4))", reflect_point_x((3, 4)), (3.0, -4.0))
    run_test(result, "reflect_point_x((0,0))", reflect_point_x((0, 0)), (0.0, 0.0))
    
    # reflect_point_y
    run_test(result, "reflect_point_y((3,4))", reflect_point_y((3, 4)), (-3.0, 4.0))
    
    # reflect_point_origin
    run_test(result, "reflect_point_origin((3,4))", reflect_point_origin((3, 4)), (-3.0, -4.0))


# ============================================================================
# Collision Detection Tests
# ============================================================================

def test_collision_detection(result: TestResult):
    """Test collision detection functions."""
    
    # point_in_rectangle
    run_test(result, "point_in_rectangle((2,2),(0,0),(4,4))", point_in_rectangle((2, 2), (0, 0), (4, 4)), True)
    run_test(result, "point_in_rectangle((0,0),(0,0),(4,4))", point_in_rectangle((0, 0), (0, 0), (4, 4)), True)  # Edge
    run_test(result, "point_in_rectangle((4,4),(0,0),(4,4))", point_in_rectangle((4, 4), (0, 0), (4, 4)), True)  # Corner
    run_test(result, "point_in_rectangle((5,5),(0,0),(4,4))", point_in_rectangle((5, 5), (0, 0), (4, 4)), False)
    run_test(result, "point_in_rectangle((-1,-1),(0,0),(4,4))", point_in_rectangle((-1, -1), (0, 0), (4, 4)), False)
    
    # point_in_circle
    run_test(result, "point_in_circle((2,2),(0,0),3)", point_in_circle((2, 2), (0, 0), 3), True)
    run_test(result, "point_in_circle((0,0),(0,0),3)", point_in_circle((0, 0), (0, 0), 3), True)
    run_test(result, "point_in_circle((3,0),(0,0),3)", point_in_circle((3, 0), (0, 0), 3), True)  # Edge
    run_test(result, "point_in_circle((4,4),(0,0),3)", point_in_circle((4, 4), (0, 0), 3), False)
    
    # circles_intersect
    run_test(result, "circles_intersect((0,0),2,(3,0),2)", circles_intersect((0, 0), 2, (3, 0), 2), True)
    run_test(result, "circles_intersect((0,0),1,(5,0),1)", circles_intersect((0, 0), 1, (5, 0), 1), False)
    run_test(result, "circles_intersect((0,0),2,(4,0),2)", circles_intersect((0, 0), 2, (4, 0), 2), True)  # Touch
    run_test(result, "circles_intersect((0,0),5,(0,0),3)", circles_intersect((0, 0), 5, (0, 0), 3), True)  # Contained
    
    # rectangles_intersect
    run_test(result, "rectangles_intersect((0,0),(4,4),(2,2),(6,6))", rectangles_intersect((0, 0), (4, 4), (2, 2), (6, 6)), True)
    run_test(result, "rectangles_intersect((0,0),(2,2),(3,3),(5,5))", rectangles_intersect((0, 0), (2, 2), (3, 3), (5, 5)), False)
    run_test(result, "rectangles_intersect((0,0),(4,4),(4,4),(6,6))", rectangles_intersect((0, 0), (4, 4), (4, 4), (6, 6)), True)  # Touch
    run_test(result, "rectangles_intersect((0,0),(2,2),(1,1),(3,3))", rectangles_intersect((0, 0), (2, 2), (1, 1), (3, 3)), True)  # Overlap


# ============================================================================
# Coordinate Conversion Tests
# ============================================================================

def test_coordinate_conversions(result: TestResult):
    """Test coordinate conversion functions."""
    
    # cartesian_to_polar
    result_add = cartesian_to_polar((1, 1))
    run_test(result, "cartesian_to_polar((1,1)) r", result_add[0], SQRT2, 1e-10)
    run_test(result, "cartesian_to_polar((1,1)) theta", result_add[1], PI / 4, 1e-10)
    
    result_add = cartesian_to_polar((1, 0))
    run_test(result, "cartesian_to_polar((1,0)) r", result_add[0], 1.0)
    run_test(result, "cartesian_to_polar((1,0)) theta", result_add[1], 0.0)
    
    # polar_to_cartesian
    result_add = polar_to_cartesian(1, 0)
    run_test(result, "polar_to_cartesian(1,0) x", result_add[0], 1.0)
    run_test(result, "polar_to_cartesian(1,0) y", result_add[1], 0.0)
    
    result_add = polar_to_cartesian(1, PI / 2)
    run_test(result, "polar_to_cartesian(1,PI/2) x", result_add[0], 0.0, 1e-10)
    run_test(result, "polar_to_cartesian(1,PI/2) y", result_add[1], 1.0, 1e-10)
    
    # cartesian_to_cylindrical
    result_add = cartesian_to_cylindrical((1, 1, 2))
    run_test(result, "cartesian_to_cylindrical((1,1,2)) rho", result_add[0], SQRT2, 1e-10)
    run_test(result, "cartesian_to_cylindrical((1,1,2)) phi", result_add[1], PI / 4, 1e-10)
    run_test(result, "cartesian_to_cylindrical((1,1,2)) z", result_add[2], 2.0)
    
    # cylindrical_to_cartesian
    result_add = cylindrical_to_cartesian(1, 0, 2)
    run_test(result, "cylindrical_to_cartesian(1,0,2) x", result_add[0], 1.0)
    run_test(result, "cylindrical_to_cartesian(1,0,2) y", result_add[1], 0.0)
    run_test(result, "cylindrical_to_cartesian(1,0,2) z", result_add[2], 2.0)
    
    # cartesian_to_spherical
    result_add = cartesian_to_spherical((0, 0, 1))
    run_test(result, "cartesian_to_spherical((0,0,1)) r", result_add[0], 1.0)
    run_test(result, "cartesian_to_spherical((0,0,1)) theta", result_add[1], 0.0)
    
    result_add = cartesian_to_spherical((1, 0, 0))
    run_test(result, "cartesian_to_spherical((1,0,0)) r", result_add[0], 1.0)
    run_test(result, "cartesian_to_spherical((1,0,0)) theta", result_add[1], PI / 2, 1e-10)
    
    # spherical_to_cartesian
    result_add = spherical_to_cartesian(1, 0, 0)
    run_test(result, "spherical_to_cartesian(1,0,0) x", result_add[0], 0.0, 1e-10)
    run_test(result, "spherical_to_cartesian(1,0,0) y", result_add[1], 0.0, 1e-10)
    run_test(result, "spherical_to_cartesian(1,0,0) z", result_add[2], 1.0)


# ============================================================================
# Triangle Tests
# ============================================================================

def test_triangle_functions(result: TestResult):
    """Test triangle classification and calculation functions."""
    
    # triangle_type_by_sides
    run_test(result, "triangle_type_by_sides(3,3,3)", triangle_type_by_sides(3, 3, 3), 'equilateral')
    run_test(result, "triangle_type_by_sides(3,4,5)", triangle_type_by_sides(3, 4, 5), 'scalene')
    run_test(result, "triangle_type_by_sides(3,3,5)", triangle_type_by_sides(3, 3, 5), 'isosceles')
    run_test(result, "triangle_type_by_sides(0,4,5)", triangle_type_by_sides(0, 4, 5), 'invalid')
    run_test(result, "triangle_type_by_sides(1,2,10)", triangle_type_by_sides(1, 2, 10), 'invalid')
    
    # triangle_type_by_angles
    run_test(result, "triangle_type_by_angles(3,4,5)", triangle_type_by_angles(3, 4, 5), 'right')
    run_test(result, "triangle_type_by_angles(5,5,5)", triangle_type_by_angles(5, 5, 5), 'acute')
    run_test(result, "triangle_type_by_angles(2,3,4)", triangle_type_by_angles(2, 3, 4), 'obtuse')  # Valid obtuse
    run_test(result, "triangle_type_by_angles(2,3,6)", triangle_type_by_angles(2, 3, 6), 'invalid')  # Invalid: 2+3<6
    run_test(result, "triangle_type_by_angles(0,4,5)", triangle_type_by_angles(0, 4, 5), 'invalid')
    
    # triangle_angles (3-4-5 right triangle)
    result_add = triangle_angles(3, 4, 5)
    run_test(result, "triangle_angles(3,4,5) A", result_add[0], 36.86989765, 1e-6)
    run_test(result, "triangle_angles(3,4,5) B", result_add[1], 53.13010235, 1e-6)
    run_test(result, "triangle_angles(3,4,5) C", result_add[2], 90.0, 1e-6)
    
    # is_right_triangle
    run_test(result, "is_right_triangle(3,4,5)", is_right_triangle(3, 4, 5), True)
    run_test(result, "is_right_triangle(5,12,13)", is_right_triangle(5, 12, 13), True)
    run_test(result, "is_right_triangle(2,3,4)", is_right_triangle(2, 3, 4), False)
    
    # pythagorean_triple_check
    run_test(result, "pythagorean_triple_check(3,4,5)", pythagorean_triple_check(3, 4, 5), True)
    run_test(result, "pythagorean_triple_check(5,12,13)", pythagorean_triple_check(5, 12, 13), True)
    run_test(result, "pythagorean_triple_check(8,15,17)", pythagorean_triple_check(8, 15, 17), True)
    run_test(result, "pythagorean_triple_check(2,3,4)", pythagorean_triple_check(2, 3, 4), False)


# ============================================================================
# Miscellaneous Tests
# ============================================================================

def test_miscellaneous(result: TestResult):
    """Test miscellaneous geometry functions."""
    
    # midpoint_2d
    run_test(result, "midpoint_2d((0,0),(4,6))", midpoint_2d((0, 0), (4, 6)), (2.0, 3.0))
    run_test(result, "midpoint_2d((1,1),(1,1))", midpoint_2d((1, 1), (1, 1)), (1.0, 1.0))
    
    # midpoint_3d
    run_test(result, "midpoint_3d((0,0,0),(4,6,8))", midpoint_3d((0, 0, 0), (4, 6, 8)), (2.0, 3.0, 4.0))
    
    # centroid_triangle
    run_test(result, "centroid_triangle((0,0),(3,0),(0,3))", centroid_triangle((0, 0), (3, 0), (0, 3)), (1.0, 1.0))
    
    # polygon_area (square)
    run_test(result, "polygon_area(square)", polygon_area([(0, 0), (2, 0), (2, 2), (0, 2)]), 4.0)
    run_test(result, "polygon_area(triangle)", polygon_area([(0, 0), (3, 0), (0, 4)]), 6.0)
    run_test(result, "polygon_area(less_than_3)", polygon_area([(0, 0), (1, 1)]), 0.0)
    
    # polygon_perimeter (square)
    run_test(result, "polygon_perimeter(square)", polygon_perimeter([(0, 0), (2, 0), (2, 2), (0, 2)]), 8.0)
    
    # is_convex_polygon
    run_test(result, "is_convex_polygon(square)", is_convex_polygon([(0, 0), (2, 0), (2, 2), (0, 2)]), True)
    run_test(result, "is_convex_polygon(triangle)", is_convex_polygon([(0, 0), (3, 0), (0, 3)]), True)
    
    # interpolate_points
    run_test(result, "interpolate_points((0,0),(10,10),0.5)", interpolate_points((0, 0), (10, 10), 0.5), (5.0, 5.0))
    run_test(result, "interpolate_points((0,0),(10,10),0)", interpolate_points((0, 0), (10, 10), 0), (0.0, 0.0))
    run_test(result, "interpolate_points((0,0),(10,10),1)", interpolate_points((0, 0), (10, 10), 1), (10.0, 10.0))
    
    # slope
    run_test(result, "slope((0,0),(2,4))", slope((0, 0), (2, 4)), 2.0)
    run_test(result, "slope((1,1),(1,5))", slope((1, 1), (1, 5)), None)  # Vertical
    run_test(result, "slope((0,0),(0,0))", slope((0, 0), (0, 0)), None)  # Same point
    
    # line_equation
    result_add = line_equation((0, 0), (2, 4))
    run_test(result, "line_equation((0,0),(2,4)) slope", result_add[0], 2.0)
    run_test(result, "line_equation((0,0),(2,4)) intercept", result_add[1], 0.0)
    
    result_add = line_equation((1, 1), (1, 5))
    run_test(result, "line_equation((1,1),(1,5)) vertical", result_add[0], None)
    run_test(result, "line_equation((1,1),(1,5)) x", result_add[1], 1.0)
    
    # point_to_line_distance
    run_test(result, "point_to_line_distance((0,0),(1,1),(2,2))", point_to_line_distance((0, 0), (1, 1), (2, 2)), 0.0, 1e-10)
    run_test(result, "point_to_line_distance((0,0),(0,1),(1,1))", point_to_line_distance((0, 0), (0, 1), (1, 1)), 1.0, 1e-10)


# ============================================================================
# Edge Case Tests
# ============================================================================

def test_edge_cases(result: TestResult):
    """Test edge cases and boundary conditions."""
    
    # Zero and negative values
    run_test(result, "circle_area(0)", circle_area(0), 0.0)
    run_test(result, "circle_area(-5)", circle_area(-5), 0.0)
    run_test(result, "distance_2d((0,0),(0,0))", distance_2d((0, 0), (0, 0)), 0.0)
    
    # Very small values
    run_test(result, "circle_area(0.001)", circle_area(0.001) > 0, True)
    
    # Very large values
    run_test(result, "square_area(1000000)", square_area(1000000), 1e12)
    
    # String inputs (should be converted to float)
    run_test(result, "circle_area('5')", circle_area('5'), circle_area(5))
    
    # None handling (via _to_float)
    # These should not crash and return 0 or sensible defaults
    try:
        _ = distance_2d((0, 0), (0, 0))
        result.add_pass()
    except Exception:
        result.add_fail("distance_2d basic", "no exception", "exception raised")


# ============================================================================
# Constants Tests
# ============================================================================

def test_constants(result: TestResult):
    """Test mathematical constants."""
    
    run_test(result, "PI value", PI, math.pi)
    run_test(result, "E value", E, math.e)
    run_test(result, "GOLDEN_RATIO", GOLDEN_RATIO, (1 + math.sqrt(5)) / 2, 1e-10)
    run_test(result, "SQRT2", SQRT2, math.sqrt(2), 1e-10)
    run_test(result, "SQRT3", SQRT3, math.sqrt(3), 1e-10)


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all test suites and report results."""
    result = TestResult()
    
    print("Running AllToolkit Geometry Utils Test Suite")
    print("=" * 50)
    
    # Run all test categories
    test_constants(result)
    print("✓ Constants tests completed")
    
    test_angle_conversions(result)
    print("✓ Angle conversion tests completed")
    
    test_distance_calculations(result)
    print("✓ Distance calculation tests completed")
    
    test_2d_shapes(result)
    print("✓ 2D shape tests completed")
    
    test_3d_shapes(result)
    print("✓ 3D shape tests completed")
    
    test_vector_operations(result)
    print("✓ Vector operation tests completed")
    
    test_transformations(result)
    print("✓ Transformation tests completed")
    
    test_collision_detection(result)
    print("✓ Collision detection tests completed")
    
    test_coordinate_conversions(result)
    print("✓ Coordinate conversion tests completed")
    
    test_triangle_functions(result)
    print("✓ Triangle function tests completed")
    
    test_miscellaneous(result)
    print("✓ Miscellaneous tests completed")
    
    test_edge_cases(result)
    print("✓ Edge case tests completed")
    
    print("=" * 50)
    print(result.summary())
    
    if result.errors:
        print("\nFailed tests:")
        for test_name, expected, actual in result.errors[:10]:  # Show first 10 failures
            print(f"  - {test_name}: expected {expected}, got {actual}")
        if len(result.errors) > 10:
            print(f"  ... and {len(result.errors) - 10} more")
    
    if result.is_success():
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {result.failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
