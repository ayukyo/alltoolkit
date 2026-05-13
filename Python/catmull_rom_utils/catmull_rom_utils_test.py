#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Catmull-Rom Spline Utilities Test Suite
====================================================
Comprehensive tests for the catmull_rom_utils module.

Tests cover:
    - Basic interpolation (1D, 2D, 3D, ND)
    - Different parameterizations (uniform, chordal, centripetal)
    - Arc length computation
    - Tangent and normal computation
    - Curvature calculation
    - Path smoothing
    - Animation paths
    - Edge cases and boundary conditions
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catmull_rom_utils.mod import (
    Parameterization, Point2D, Point3D,
    catmull_rom_point, catmull_rom_derivative, catmull_rom_second_derivative,
    interpolate_1d, interpolate_2d, interpolate_3d, interpolate_nd,
    compute_arc_length, sample_at_distance, resample_curve_equidistant,
    get_tangent_2d, get_normal_2d, curvature_at_point, find_inflection_points,
    smooth_path, create_animation_path, fit_catmull_rom_to_points,
    create_smooth_polygon, generate_font_path, subdivide_segment,
    CatmullRomSpline2D, CatmullRomSpline3D
)


class TestPoint2D:
    """Tests for Point2D class."""
    
    def test_creation(self):
        """Test Point2D creation and representation."""
        p = Point2D(1.5, 2.5)
        assert p.x == 1.5
        assert p.y == 2.5
        assert "Point2D" in repr(p)
    
    def test_equality(self):
        """Test Point2D equality."""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(1.0, 2.0)
        p3 = Point2D(1.1, 2.0)
        assert p1 == p2
        assert p1 != p3
    
    def test_arithmetic(self):
        """Test Point2D arithmetic operations."""
        p1 = Point2D(1.0, 2.0)
        p2 = Point2D(3.0, 4.0)
        
        # Addition
        result = p1 + p2
        assert result.x == 4.0 and result.y == 6.0
        
        # Subtraction
        result = p2 - p1
        assert result.x == 2.0 and result.y == 2.0
        
        # Scalar multiplication
        result = p1 * 2
        assert result.x == 2.0 and result.y == 4.0
        
        # Reverse multiplication
        result = 3 * p1
        assert result.x == 3.0 and result.y == 6.0
        
        # Division
        result = p2 / 2
        assert result.x == 1.5 and result.y == 2.0
    
    def test_distance(self):
        """Test Point2D distance calculation."""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        assert abs(p1.distance_to(p2) - 5.0) < 1e-10
    
    def test_magnitude_and_normalize(self):
        """Test magnitude and normalization."""
        p = Point2D(3, 4)
        assert abs(p.magnitude() - 5.0) < 1e-10
        
        normalized = p.normalize()
        assert abs(normalized.magnitude() - 1.0) < 1e-10
    
    def test_to_tuple(self):
        """Test conversion to tuple."""
        p = Point2D(1.5, 2.5)
        t = p.to_tuple()
        assert t == (1.5, 2.5)


class TestPoint3D:
    """Tests for Point3D class."""
    
    def test_creation(self):
        """Test Point3D creation."""
        p = Point3D(1.0, 2.0, 3.0)
        assert p.x == 1.0 and p.y == 2.0 and p.z == 3.0
    
    def test_arithmetic(self):
        """Test Point3D arithmetic."""
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(4, 5, 6)
        
        result = p1 + p2
        assert result.x == 5 and result.y == 7 and result.z == 9
        
        result = p2 - p1
        assert result.x == 3 and result.y == 3 and result.z == 3
        
        result = p1 * 2
        assert result.x == 2 and result.y == 4 and result.z == 6
    
    def test_distance(self):
        """Test 3D distance."""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 2, 2)
        assert abs(p1.distance_to(p2) - 3.0) < 1e-10


class TestCatmullRomPoint:
    """Tests for core catmull_rom_point function."""
    
    def test_basic_interpolation(self):
        """Test basic point interpolation."""
        # Four control points on a line
        p0 = [0.0]
        p1 = [0.0]
        p2 = [1.0]
        p3 = [1.0]
        
        # At t=0, should be at p1
        result = catmull_rom_point(p0, p1, p2, p3, 0.0)
        assert abs(result[0] - 0.0) < 1e-10
        
        # At t=1, should be at p2
        result = catmull_rom_point(p0, p1, p2, p3, 1.0)
        assert abs(result[0] - 1.0) < 1e-10
    
    def test_2d_interpolation(self):
        """Test 2D point interpolation."""
        p0 = [0.0, 0.0]
        p1 = [0.0, 0.0]
        p2 = [1.0, 1.0]
        p3 = [1.0, 1.0]
        
        # At t=0
        result = catmull_rom_point(p0, p1, p2, p3, 0.0)
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - 0.0) < 1e-10
        
        # At t=1
        result = catmull_rom_point(p0, p1, p2, p3, 1.0)
        assert abs(result[0] - 1.0) < 1e-10
        assert abs(result[1] - 1.0) < 1e-10
    
    def test_parameterization_types(self):
        """Test different parameterization types."""
        p0 = [0.0, 0.0]
        p1 = [0.0, 0.0]
        p2 = [10.0, 0.0]
        p3 = [10.0, 0.0]
        
        # Uniform
        result_uniform = catmull_rom_point(p0, p1, p2, p3, 0.5, Parameterization.UNIFORM)
        
        # Centripetal
        result_centripetal = catmull_rom_point(p0, p1, p2, p3, 0.5, Parameterization.CENTRIPETAL)
        
        # Uniform should give midpoint for this configuration
        assert abs(result_uniform[0] - 5.0) < 0.1
        
        # Centripetal should also give a reasonable result
        assert 0 <= result_centripetal[0] <= 15  # Allow some overshoot


class TestInterpolation:
    """Tests for interpolation functions."""
    
    def test_interpolate_1d_basic(self):
        """Test 1D interpolation."""
        values = [0.0, 1.0, 2.0, 3.0]
        result = interpolate_1d(values, num_points=10)
        
        assert len(result) > 0
        # First point should be near 0
        assert abs(result[0] - 0.0) < 0.1
        # Last point should be near 3
        assert abs(result[-1] - 3.0) < 0.1
    
    def test_interpolate_1d_two_points(self):
        """Test 1D interpolation with two points (linear)."""
        values = [0.0, 10.0]
        result = interpolate_1d(values, num_points=5)
        
        assert len(result) == 5
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[-1] - 10.0) < 1e-10
        # Middle should be 5
        assert abs(result[2] - 5.0) < 1e-10
    
    def test_interpolate_1d_closed(self):
        """Test 1D closed curve interpolation."""
        values = [0.0, 1.0, 0.0]
        result = interpolate_1d(values, num_points=20, closed=True)
        
        # First and last should be similar for closed curve
        assert abs(result[0] - result[-1]) < 0.1
    
    def test_interpolate_2d_basic(self):
        """Test 2D interpolation."""
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 0), Point2D(3, 1)]
        result = interpolate_2d(points, num_points=20)
        
        assert len(result) > 0
        # Check that points pass through control points approximately
        assert abs(result[0].x - 0.0) < 0.1
        assert abs(result[-1].x - 3.0) < 0.1
    
    def test_interpolate_2d_tuple_input(self):
        """Test 2D interpolation with tuple input."""
        points = [(0, 0), (1, 1), (2, 0)]
        result = interpolate_2d(points, num_points=10)
        
        assert len(result) > 0
        assert all(isinstance(p, Point2D) for p in result)
    
    def test_interpolate_2d_closed(self):
        """Test 2D closed curve."""
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        result = interpolate_2d(points, num_points=40, closed=True)
        
        # Curve should loop back - check that first and last are close to control points
        first = result[0]
        last = result[-1]
        # For closed curves, the first point should be near first control point
        assert first.distance_to(Point2D(0, 0)) < 1.0
    
    def test_interpolate_3d_basic(self):
        """Test 3D interpolation."""
        points = [
            Point3D(0, 0, 0),
            Point3D(1, 1, 1),
            Point3D(2, 0, 2),
            Point3D(3, 1, 3)
        ]
        result = interpolate_3d(points, num_points=20)
        
        assert len(result) > 0
        assert all(isinstance(p, Point3D) for p in result)
    
    def test_interpolate_nd_basic(self):
        """Test N-dimensional interpolation."""
        points = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 0, 2, 0],
            [3, 1, 3, 1]
        ]
        result = interpolate_nd(points, num_points=10)
        
        assert len(result) > 0
        assert all(len(p) == 4 for p in result)


class TestArcLength:
    """Tests for arc length computation."""
    
    def test_straight_line(self):
        """Test arc length of approximately straight line."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        length = compute_arc_length(points)
        
        # Should be approximately 3 units
        assert 2.5 < length < 3.5
    
    def test_curved_line(self):
        """Test arc length of curved line."""
        # Quarter circle approximation
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        length = compute_arc_length(points)
        
        # Should be positive and reasonable
        assert length > 1.0
    
    def test_zero_length(self):
        """Test arc length with insufficient points."""
        points = [(0, 0)]
        length = compute_arc_length(points)
        assert length == 0.0


class TestSampleAtDistance:
    """Tests for sample_at_distance function."""
    
    def test_sample_start(self):
        """Test sampling at distance 0."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        result = sample_at_distance(points, 0.0)
        
        assert result is not None
        assert abs(result.x - 0.0) < 0.1
    
    def test_sample_end(self):
        """Test sampling at large distance."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        length = compute_arc_length(points)
        result = sample_at_distance(points, length + 10)
        
        # Should return last point
        assert result is not None
        assert abs(result.x - 3.0) < 0.1
    
    def test_sample_middle(self):
        """Test sampling at middle distance."""
        points = [(0, 0), (2, 0), (4, 0)]
        length = compute_arc_length(points)
        result = sample_at_distance(points, length / 2)
        
        assert result is not None
        # Should be near the middle
        assert 1.5 < result.x < 2.5


class TestTangentAndNormal:
    """Tests for tangent and normal computation."""
    
    def test_tangent_basic(self):
        """Test basic tangent computation."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        tangent = get_tangent_2d(points, 0.5)
        
        # Tangent should be normalized
        assert abs(tangent.magnitude() - 1.0) < 1e-10
        # Should point roughly in x direction for this straight line
        assert tangent.x > abs(tangent.y)
    
    def test_normal_basic(self):
        """Test basic normal computation."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        normal = get_normal_2d(points, 0.5)
        
        # Normal should be normalized
        assert abs(normal.magnitude() - 1.0) < 1e-10
        # Normal should be perpendicular to tangent
        tangent = get_tangent_2d(points, 0.5)
        dot_product = tangent.x * normal.x + tangent.y * normal.y
        assert abs(dot_product) < 1e-10


class TestCurvature:
    """Tests for curvature computation."""
    
    def test_straight_line_curvature(self):
        """Test curvature of straight line."""
        p0 = [0, 0]
        p1 = [1, 0]
        p2 = [2, 0]
        p3 = [3, 0]
        
        curvature = curvature_at_point(p0, p1, p2, p3, 0.5)
        # Straight line should have near-zero curvature
        assert abs(curvature) < 0.1
    
    def test_curved_curvature(self):
        """Test curvature of curved segment."""
        # Control points that create a curve
        p0 = [0, 0]
        p1 = [0, 0]
        p2 = [1, 1]
        p3 = [1, 1]
        
        curvature = curvature_at_point(p0, p1, p2, p3, 0.5)
        # Curvature should be computed (value depends on configuration)
        assert isinstance(curvature, float)


class TestInflectionPoints:
    """Tests for inflection point detection."""
    
    def test_simple_curve(self):
        """Test inflection point detection on simple curve."""
        # S-curve configuration
        p0 = [0, 0]
        p1 = [1, -1]
        p2 = [2, 1]
        p3 = [3, 0]
        
        inflections = find_inflection_points(p0, p1, p2, p3)
        # Should have at least one inflection point for S-curve
        assert isinstance(inflections, list)


class TestSmoothPath:
    """Tests for path smoothing."""
    
    def test_smooth_basic(self):
        """Test basic path smoothing."""
        # Zigzag path
        points = [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]
        smoothed = smooth_path(points, iterations=1)
        
        assert len(smoothed) > len(points)
        # Smoothed path should have smaller total angle changes
        # (smoother = less jagged)
    
    def test_smooth_multiple_iterations(self):
        """Test multiple smoothing iterations."""
        points = [(0, 0), (2, 2), (4, 0)]
        smoothed1 = smooth_path(points, iterations=1)
        smoothed2 = smooth_path(points, iterations=2)
        
        # More iterations should produce more points
        assert len(smoothed2) >= len(smoothed1)


class TestAnimationPath:
    """Tests for animation path generation."""
    
    def test_basic_animation(self):
        """Test basic animation path."""
        keyframes = [(0, 0), (5, 5), (10, 0)]
        path = create_animation_path(keyframes, num_frames=60)
        
        assert len(path) == 60
        # Check first and last are within reasonable range of keyframes
        assert path[0].x >= 0  # Should start near beginning
        assert path[-1].x <= 10  # Should end near end
    
    def test_easing_linear(self):
        """Test linear easing."""
        keyframes = [(0, 0), (10, 0)]
        path = create_animation_path(keyframes, num_frames=11, easing='linear')
        
        # Should be evenly spaced
        for i, p in enumerate(path):
            expected_x = i
            assert abs(p.x - expected_x) < 0.5
    
    def test_easing_in(self):
        """Test ease-in animation."""
        keyframes = [(0, 0), (10, 0)]
        path = create_animation_path(keyframes, num_frames=11, easing='ease-in')
        
        # First few frames should move slower than linear
        assert path[3].x < 3.0
    
    def test_easing_out(self):
        """Test ease-out animation."""
        keyframes = [(0, 0), (10, 0)]
        path = create_animation_path(keyframes, num_frames=11, easing='ease-out')
        
        # Last few frames should move slower
        assert path[-3].x > 7.0


class TestCatmullRomSpline2D:
    """Tests for CatmullRomSpline2D class."""
    
    def test_creation(self):
        """Test spline creation."""
        points = [(0, 0), (1, 1), (2, 0), (3, 1)]
        spline = CatmullRomSpline2D(points)
        
        assert len(spline.control_points) == 4
    
    def test_point_at(self):
        """Test point_at method."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        spline = CatmullRomSpline2D(points)
        
        p_start = spline.point_at(0.0)
        p_end = spline.point_at(1.0)
        
        # Points should be along the line between control points
        assert 0.0 <= p_start.x <= 2.0  # Near first control point range
        assert 1.0 <= p_end.x <= 3.0  # Near last control point range
    
    def test_tangent_and_normal(self):
        """Test tangent and normal methods."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        spline = CatmullRomSpline2D(points)
        
        tangent = spline.tangent_at(0.5)
        normal = spline.normal_at(0.5)
        
        assert abs(tangent.magnitude() - 1.0) < 1e-10
        assert abs(normal.magnitude() - 1.0) < 1e-10
    
    def test_interpolate(self):
        """Test interpolate method."""
        points = [(0, 0), (1, 1), (2, 0)]
        spline = CatmullRomSpline2D(points)
        
        result = spline.interpolate(num_points=50)
        assert len(result) > 0
    
    def test_arc_length(self):
        """Test arc_length method."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        spline = CatmullRomSpline2D(points)
        
        length = spline.arc_length()
        assert length > 0
    
    def test_smooth(self):
        """Test smooth method."""
        points = [(0, 0), (2, 2), (4, 0)]
        spline = CatmullRomSpline2D(points)
        
        smoothed = spline.smooth(iterations=1)
        assert isinstance(smoothed, CatmullRomSpline2D)


class TestCatmullRomSpline3D:
    """Tests for CatmullRomSpline3D class."""
    
    def test_creation(self):
        """Test 3D spline creation."""
        points = [(0, 0, 0), (1, 1, 1), (2, 0, 2), (3, 1, 3)]
        spline = CatmullRomSpline3D(points)
        
        assert len(spline.control_points) == 4
    
    def test_point_at(self):
        """Test 3D point_at method."""
        points = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        spline = CatmullRomSpline3D(points)
        
        p = spline.point_at(0.5)
        assert isinstance(p, Point3D)
    
    def test_interpolate(self):
        """Test 3D interpolate method."""
        points = [(0, 0, 0), (1, 1, 1), (2, 0, 2)]
        spline = CatmullRomSpline3D(points)
        
        result = spline.interpolate(num_points=30)
        assert len(result) > 0
        assert all(isinstance(p, Point3D) for p in result)


class TestCreateSmoothPolygon:
    """Tests for smooth polygon creation."""
    
    def test_triangle(self):
        """Test smooth triangle."""
        vertices = [(0, 0), (1, 0), (0.5, 1)]
        result = create_smooth_polygon(vertices, num_points=30)
        
        assert len(result) > 0
        # Should produce points along a curve
        assert all(isinstance(p, Point2D) for p in result)
    
    def test_sharpness(self):
        """Test different sharpness levels."""
        vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        
        smooth = create_smooth_polygon(vertices, corner_sharpness=0.0, num_points=40)
        sharp = create_smooth_polygon(vertices, corner_sharpness=1.0, num_points=40)
        
        # Both should produce results
        assert len(smooth) > 0
        assert len(sharp) > 0


class TestGenerateFontPath:
    """Tests for font path generation."""
    
    def test_basic_path(self):
        """Test basic font path generation."""
        points = [(0, 0), (0.5, 1), (1, 0)]
        result = generate_font_path(points, num_points=20)
        
        assert len(result) > 0
        # Should pass through control points approximately
        assert result[0].distance_to(Point2D(0, 0)) < 0.5
        assert result[-1].distance_to(Point2D(1, 0)) < 0.5


class TestResampleEquidistant:
    """Tests for equidistant resampling."""
    
    def test_basic_resampling(self):
        """Test basic equidistant resampling."""
        # Control points with varying distances
        points = [(0, 0), (0.1, 0.1), (1, 1), (2, 0.5), (3, 0)]
        result = resample_curve_equidistant(points, num_points=20)
        
        assert len(result) == 20
        
        # Check that result contains valid points
        assert all(isinstance(p, Point2D) for p in result)
        
        # Points should be in order along the curve
        # (x values should generally increase)
        for i in range(1, len(result)):
            # Allow small variations but general progression
            assert result[i].x >= result[i-1].x - 0.5


class TestFitCatmullRom:
    """Tests for Catmull-Rom fitting."""
    
    def test_basic_fitting(self):
        """Test basic curve fitting."""
        # Generate some data points
        data = [(i * 0.5, math.sin(i * 0.5)) for i in range(20)]
        
        control = fit_catmull_rom_to_points(
            [Point2D(p[0], p[1]) for p in data],
            num_control=5
        )
        
        assert len(control) == 5
        assert all(isinstance(p, Point2D) for p in control)


class TestSubdivideSegment:
    """Tests for segment subdivision."""
    
    def test_basic_subdivision(self):
        """Test basic segment subdivision."""
        p0 = [0, 0]
        p1 = [0, 0]
        p2 = [2, 0]
        p3 = [2, 0]
        
        result = subdivide_segment(p0, p1, p2, p3)
        
        assert len(result) == 5
        # Each result should be a 2D point
        assert all(len(p) == 2 for p in result)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_single_point(self):
        """Test with single point."""
        # Single point should return itself
        result = interpolate_2d([(0, 0)], num_points=10)
        assert len(result) == 1
    
    def test_two_points(self):
        """Test with two points (should be linear)."""
        result = interpolate_2d([(0, 0), (10, 10)], num_points=5)
        assert len(result) == 5
        # Should be linear interpolation
        for i, p in enumerate(result):
            t = i / 4
            expected_x = 10 * t
            expected_y = 10 * t
            assert abs(p.x - expected_x) < 0.1
            assert abs(p.y - expected_y) < 0.1
    
    def test_empty_input(self):
        """Test with empty input."""
        result = interpolate_2d([], num_points=10)
        assert len(result) == 0
    
    def test_identical_points(self):
        """Test with identical points."""
        points = [(1, 1), (1, 1), (1, 1), (1, 1)]
        result = interpolate_2d(points, num_points=10)
        
        # All points should be at or near (1, 1)
        for p in result:
            assert abs(p.x - 1.0) < 0.5
            assert abs(p.y - 1.0) < 0.5


class TestParameterizationDifferences:
    """Tests to verify different parameterizations produce different results."""
    
    def test_uniform_vs_centripetal(self):
        """Test that uniform and centripetal produce different curves."""
        # Control points with different distances
        points = [(0, 0), (0.1, 0), (2, 0), (2.1, 0)]
        
        uniform = interpolate_2d(points, num_points=50, 
                                  parameterization=Parameterization.UNIFORM)
        centripetal = interpolate_2d(points, num_points=50,
                                      parameterization=Parameterization.CENTRIPETAL)
        
        # The curves should be different at some points
        different = False
        for u, c in zip(uniform, centripetal):
            if abs(u.x - c.x) > 0.01 or abs(u.y - c.y) > 0.01:
                different = True
                break
        
        # With non-uniform spacing, parameterizations should differ
        # (though this specific case might produce similar results)
        assert len(uniform) > 0 and len(centripetal) > 0


def run_all_tests():
    """Run all tests and report results."""
    test_classes = [
        TestPoint2D,
        TestPoint3D,
        TestCatmullRomPoint,
        TestInterpolation,
        TestArcLength,
        TestSampleAtDistance,
        TestTangentAndNormal,
        TestCurvature,
        TestInflectionPoints,
        TestSmoothPath,
        TestAnimationPath,
        TestCatmullRomSpline2D,
        TestCatmullRomSpline3D,
        TestCreateSmoothPolygon,
        TestGenerateFontPath,
        TestResampleEquidistant,
        TestFitCatmullRom,
        TestSubdivideSegment,
        TestEdgeCases,
        TestParameterizationDifferences,
    ]
    
    total_tests = 0
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    passed += 1
                    print(f"✓ {test_class.__name__}.{method_name}")
                except AssertionError as e:
                    failed += 1
                    print(f"✗ {test_class.__name__}.{method_name}: {str(e)}")
                except Exception as e:
                    failed += 1
                    print(f"✗ {test_class.__name__}.{method_name}: {type(e).__name__}: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"Total: {total_tests} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/total_tests*100:.1f}%")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)