#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Catmull-Rom Spline Usage Examples
==============================================
Practical examples demonstrating the catmull_rom_utils module.

Examples include:
    1. Basic 2D curve interpolation
    2. Different parameterization types
    3. 3D curve interpolation
    4. Arc length computation
    5. Animation path with easing
    6. Path smoothing
    7. Creating smooth polygons
    8. Font/vector graphics paths
    9. Equidistant sampling
    10. Curvature analysis
"""

import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catmull_rom_utils.mod import (
    Parameterization, Point2D, Point3D,
    interpolate_1d, interpolate_2d, interpolate_3d,
    compute_arc_length, sample_at_distance,
    get_tangent_2d, get_normal_2d, curvature_at_point,
    smooth_path, create_animation_path,
    create_smooth_polygon, generate_font_path,
    resample_curve_equidistant,
    CatmullRomSpline2D, CatmullRomSpline3D
)


def example_1_basic_2d_interpolation():
    """Example 1: Basic 2D curve interpolation."""
    print("=" * 60)
    print("Example 1: Basic 2D Curve Interpolation")
    print("=" * 60)
    
    # Define control points for a smooth curve
    control_points = [
        Point2D(0, 0),
        Point2D(1, 2),
        Point2D(3, 1),
        Point2D(4, 3),
        Point2D(6, 0)
    ]
    
    print(f"Control points: {len(control_points)}")
    for p in control_points:
        print(f"  {p}")
    
    # Interpolate with 50 points
    curve_points = interpolate_2d(control_points, num_points=50)
    
    print(f"\nInterpolated curve: {len(curve_points)} points")
    print("First 5 points:")
    for p in curve_points[:5]:
        print(f"  {p}")
    print("Last 5 points:")
    for p in curve_points[-5:]:
        print(f"  {p}")
    
    # The curve should pass through all control points
    print("\nNote: Curve passes through all control points smoothly")


def example_2_parameterization_types():
    """Example 2: Different parameterization types."""
    print("\n" + "=" * 60)
    print("Example 2: Parameterization Types")
    print("=" * 60)
    
    # Control points with non-uniform spacing
    control_points = [
        (0, 0),
        (0.5, 0.1),  # Very close to first point
        (4, 2),      # Far from previous
        (4.2, 2.1),  # Close again
        (8, 0)
    ]
    
    print("Control points (non-uniform spacing):")
    for i, p in enumerate(control_points):
        print(f"  P{i}: ({p[0]}, {p[1]})")
    
    # Compare parameterizations
    uniform = interpolate_2d(control_points, num_points=30, 
                             parameterization=Parameterization.UNIFORM)
    chordal = interpolate_2d(control_points, num_points=30,
                            parameterization=Parameterization.CHORDAL)
    centripetal = interpolate_2d(control_points, num_points=30,
                                 parameterization=Parameterization.CENTRIPETAL)
    
    print("\nComparison at t=0.25:")
    t_idx = 7  # Approximately 25% through the curve
    print(f"  Uniform:     {uniform[t_idx]}")
    print(f"  Chordal:     {chordal[t_idx]}")
    print(f"  Centripetal: {centripetal[t_idx]}")
    
    print("\nParameterization descriptions:")
    print("  UNIFORM:     Standard parameterization, may have cusps")
    print("  CHORDAL:     Uses chord length, smoother but can overshoot")
    print("  CENTRIPETAL: Uses sqrt of chord length, best for avoiding cusps")


def example_3_3d_curve():
    """Example 3: 3D curve interpolation."""
    print("\n" + "=" * 60)
    print("Example 3: 3D Curve Interpolation")
    print("=" * 60)
    
    # Create a 3D helix-like path
    control_points = [
        Point3D(0, 0, 0),
        Point3D(1, 1, 0.5),
        Point3D(2, 0, 1),
        Point3D(3, 1, 1.5),
        Point3D(4, 0, 2)
    ]
    
    print("3D Control points:")
    for p in control_points:
        print(f"  {p}")
    
    # Interpolate 3D curve
    curve = interpolate_3d(control_points, num_points=40)
    
    print(f"\nInterpolated 3D curve: {len(curve)} points")
    print("Sample points:")
    for i in [0, 10, 20, 30, 39]:
        print(f"  Point {i}: {curve[i]}")
    
    # Using CatmullRomSpline3D class
    print("\nUsing CatmullRomSpline3D class:")
    spline = CatmullRomSpline3D(control_points)
    
    print("Points at specific parameters:")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        p = spline.point_at(t)
        print(f"  t={t:.2f}: {p}")


def example_4_arc_length():
    """Example 4: Arc length computation and sampling."""
    print("\n" + "=" * 60)
    print("Example 4: Arc Length Computation")
    print("=" * 60)
    
    # Create a curved path
    points = [
        (0, 0),
        (2, 3),
        (5, 2),
        (7, 4),
        (10, 0)
    ]
    
    # Compute arc length
    length = compute_arc_length(points)
    print(f"Control points: {len(points)}")
    print(f"Approximate arc length: {length:.2f}")
    
    # Sample at specific distances
    print("\nSampling at specific distances:")
    distances = [0, length * 0.25, length * 0.5, length * 0.75, length]
    
    for d in distances:
        point = sample_at_distance(points, d)
        if point:
            print(f"  Distance {d:.2f}: {point}")
    
    # Compare with linear distance
    linear_dist = math.sqrt((10-0)**2 + (0-0)**2)
    print(f"\nLinear distance (start to end): {linear_dist:.2f}")
    print(f"Curve is {length/linear_dist:.2f}x longer than linear path")


def example_5_animation_path():
    """Example 5: Animation path with easing."""
    print("\n" + "=" * 60)
    print("Example 5: Animation Path with Easing")
    print("=" * 60)
    
    # Define keyframes for an animation
    keyframes = [
        (0, 0),    # Start
        (2, 5),    # Peak
        (6, 3),    # Valley
        (10, 0)    # End
    ]
    
    print("Animation keyframes:")
    for i, kf in enumerate(keyframes):
        print(f"  Keyframe {i}: ({kf[0]}, {kf[1]})")
    
    # Create animation with different easing
    num_frames = 30
    
    print(f"\nCreating {num_frames} frame animation:")
    
    # Linear
    linear = create_animation_path(keyframes, num_frames, easing='linear')
    print("\nLinear easing - positions at frames:")
    for i in [0, 5, 10, 15, 20, 25, 29]:
        print(f"  Frame {i}: {linear[i]}")
    
    # Ease-in (slow start)
    ease_in = create_animation_path(keyframes, num_frames, easing='ease-in')
    print("\nEase-in - positions at frames:")
    for i in [0, 5, 10, 15, 20, 25, 29]:
        print(f"  Frame {i}: {ease_in[i]}")
    
    # Ease-out (slow end)
    ease_out = create_animation_path(keyframes, num_frames, easing='ease-out')
    print("\nEase-out - positions at frames:")
    for i in [0, 5, 10, 15, 20, 25, 29]:
        print(f"  Frame {i}: {ease_out[i]}")
    
    # Ease-in-out (slow start and end)
    ease_in_out = create_animation_path(keyframes, num_frames, easing='ease-in-out')
    print("\nEase-in-out - positions at frames:")
    for i in [0, 5, 10, 15, 20, 25, 29]:
        print(f"  Frame {i}: {ease_in_out[i]}")


def example_6_path_smoothing():
    """Example 6: Path smoothing."""
    print("\n" + "=" * 60)
    print("Example 6: Path Smoothing")
    print("=" * 60)
    
    # Create a jagged path
    jagged_path = [
        (0, 0),
        (1, 2),
        (2, 0),
        (3, 2),
        (4, 0),
        (5, 2),
        (6, 0)
    ]
    
    print("Original jagged path:")
    for p in jagged_path:
        print(f"  {p}")
    
    # Apply smoothing with different iterations
    print("\nSmoothing with 1 iteration:")
    smoothed1 = smooth_path(jagged_path, iterations=1)
    print(f"  Result: {len(smoothed1)} points")
    for p in smoothed1[:5]:
        print(f"    {p}")
    
    print("\nSmoothing with 3 iterations:")
    smoothed3 = smooth_path(jagged_path, iterations=3)
    print(f"  Result: {len(smoothed3)} points")
    for p in smoothed3[:5]:
        print(f"    {p}")
    
    print("\nMore iterations = smoother curve with more points")


def example_7_smooth_polygon():
    """Example 7: Creating smooth polygons."""
    print("\n" + "=" * 60)
    print("Example 7: Smooth Polygon Creation")
    print("=" * 60)
    
    # Define a square
    square = [
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2)
    ]
    
    print("Square vertices:")
    for v in square:
        print(f"  {v}")
    
    # Create smooth polygon with different sharpness
    print("\nSmooth polygon (sharpness=0.0 - very smooth):")
    smooth = create_smooth_polygon(square, corner_sharpness=0.0, num_points=40)
    print(f"  {len(smooth)} points")
    for p in smooth[:8]:
        print(f"    {p}")
    
    print("\nSmooth polygon (sharpness=0.5 - moderate):")
    moderate = create_smooth_polygon(square, corner_sharpness=0.5, num_points=40)
    print(f"  {len(moderate)} points")
    for p in moderate[:8]:
        print(f"    {p}")
    
    print("\nSmooth polygon (sharpness=1.0 - sharp corners):")
    sharp = create_smooth_polygon(square, corner_sharpness=1.0, num_points=40)
    print(f"  {len(sharp)} points")
    for p in sharp[:8]:
        print(f"    {p}")


def example_8_font_path():
    """Example 8: Font/vector graphics path generation."""
    print("\n" + "=" * 60)
    print("Example 8: Font/Vector Graphics Path")
    print("=" * 60)
    
    # Define a simple letter-like shape (approximation of 'S')
    s_curve = [
        (3, 0),
        (0.5, 0.5),
        (0.5, 2),
        (3, 2.5),
        (3, 4),
        (0.5, 4.5)
    ]
    
    print("'S' shape control points:")
    for p in s_curve:
        print(f"  ({p[0]}, {p[1]})")
    
    # Generate smooth font path
    font_path = generate_font_path(s_curve, tension=0.5, num_points=50)
    
    print(f"\nGenerated font path: {len(font_path)} points")
    print("First 10 points:")
    for p in font_path[:10]:
        print(f"  {p}")
    
    print("\nFont paths use centripetal Catmull-Rom for optimal smoothness")


def example_9_equidistant_sampling():
    """Example 9: Equidistant sampling along curve."""
    print("\n" + "=" * 60)
    print("Example 9: Equidistant Sampling")
    print("=" * 60)
    
    # Create curve with varying density
    points = [
        (0, 0),
        (0.5, 0.2),
        (1, 1),
        (2, 1.5),
        (3, 0.8),
        (5, 2),
        (7, 1)
    ]
    
    # Regular interpolation (non-uniform spacing)
    regular = interpolate_2d(points, num_points=20)
    
    print("Regular interpolation distances:")
    for i in range(1, min(6, len(regular))):
        d = regular[i].distance_to(regular[i-1])
        print(f"  Segment {i}: {d:.3f}")
    
    # Equidistant resampling
    equidistant = resample_curve_equidistant(points, num_points=20)
    
    print("\nEquidistant resampling distances:")
    distances = []
    for i in range(1, len(equidistant)):
        d = equidistant[i].distance_to(equidistant[i-1])
        distances.append(d)
    
    avg_dist = sum(distances) / len(distances)
    print(f"  Average distance: {avg_dist:.3f}")
    print(f"  Min distance: {min(distances):.3f}")
    print(f"  Max distance: {max(distances):.3f}")
    print(f"  Std deviation: {math.sqrt(sum((d-avg_dist)**2 for d in distances)/len(distances)):.3f}")


def example_10_curvature_analysis():
    """Example 10: Curvature analysis."""
    print("\n" + "=" * 60)
    print("Example 10: Curvature Analysis")
    print("=" * 60)
    
    # Control points creating an S-curve
    p0 = [0, 0]
    p1 = [1, -1]
    p2 = [2, 1]
    p3 = [3, 0]
    
    print("S-curve control points:")
    print(f"  P0: {p0}")
    print(f"  P1: {p1}")
    print(f"  P2: {p2}")
    print(f"  P3: {p3}")
    
    # Compute curvature at different points
    print("\nCurvature at different parameters:")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        curv = curvature_at_point(p0, p1, p2, p3, t)
        print(f"  t={t:.2f}: curvature={curv:.4f}")
    
    # Tangent at different points
    print("\nTangent vectors:")
    # Using a spline for easier tangent computation
    points = [Point2D(p[0], p[1]) for p in [p0, p1, p2, p3]]
    
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        tangent = get_tangent_2d(points, t)
        print(f"  t={t:.2f}: tangent=({tangent.x:.3f}, {tangent.y:.3f})")
    
    # Normal vectors
    print("\nNormal vectors (perpendicular to tangent):")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        normal = get_normal_2d(points, t)
        print(f"  t={t:.2f}: normal=({normal.x:.3f}, {normal.y:.3f})")


def example_11_class_based_usage():
    """Example 11: Class-based spline usage."""
    print("\n" + "=" * 60)
    print("Example 11: Class-Based Spline Usage")
    print("=" * 60)
    
    # Create a spline using the class
    control_points = [
        Point2D(0, 0),
        Point2D(2, 4),
        Point2D(5, 2),
        Point2D(7, 5),
        Point2D(10, 0)
    ]
    
    print("Creating CatmullRomSpline2D:")
    spline = CatmullRomSpline2D(control_points, 
                                parameterization=Parameterization.CENTRIPETAL)
    
    print(f"  Control points: {len(spline.control_points)}")
    print(f"  Parameterization: {spline.parameterization}")
    
    # Various operations
    print("\nQuerying the spline:")
    
    # Point at specific parameter
    print("  Points at parameters:")
    for t in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        p = spline.point_at(t)
        print(f"    t={t}: {p}")
    
    # Arc length
    length = spline.arc_length()
    print(f"\n  Arc length: {length:.2f}")
    
    # Interpolate
    interpolated = spline.interpolate(50)
    print(f"\n  Interpolated: {len(interpolated)} points")
    
    # Sample at distance
    print("\n  Sample at distances:")
    for d in [length * 0.25, length * 0.5, length * 0.75]:
        p = spline.sample_at_distance(d)
        if p:
            print(f"    d={d:.2f}: {p}")
    
    # Curvature
    print("\n  Curvature at parameters:")
    for t in [0.1, 0.3, 0.5, 0.7, 0.9]:
        curv = spline.curvature_at(t)
        print(f"    t={t}: {curv:.4f}")
    
    # Create smoothed version
    smoothed = spline.smooth(iterations=2)
    print(f"\n  Smoothed spline: {len(smoothed.control_points)} control points")


def example_12_closed_curve():
    """Example 12: Closed (looping) curves."""
    print("\n" + "=" * 60)
    print("Example 12: Closed Curve (Loop)")
    print("=" * 60)
    
    # Define points for a heart-like shape
    heart_points = [
        (2, 4),
        (0, 2),
        (2, 0),
        (4, 2),
        (2, 4)  # Back to start for closed curve
    ]
    
    print("Heart shape points:")
    for p in heart_points:
        print(f"  {p}")
    
    # Create closed curve
    closed = interpolate_2d(heart_points[:-1], num_points=50, closed=True)
    
    print(f"\nClosed curve: {len(closed)} points")
    print("First and last points (should connect smoothly):")
    print(f"  First: {closed[0]}")
    print(f"  Last: {closed[-1]}")
    print(f"  Distance: {closed[0].distance_to(closed[-1]):.4f}")
    
    # Using spline class with closed=True
    print("\nUsing CatmullRomSpline2D with closed=True:")
    spline = CatmullRomSpline2D(
        [Point2D(p[0], p[1]) for p in heart_points[:-1]],
        closed=True
    )
    
    print("Points at parameters (0 and 1 should be same):")
    p0 = spline.point_at(0.0)
    p1 = spline.point_at(1.0)
    print(f"  t=0: {p0}")
    print(f"  t=1: {p1}")
    print(f"  Distance: {p0.distance_to(p1):.4f}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# Catmull-Rom Spline Utilities - Usage Examples")
    print("#" * 60 + "\n")
    
    example_1_basic_2d_interpolation()
    example_2_parameterization_types()
    example_3_3d_curve()
    example_4_arc_length()
    example_5_animation_path()
    example_6_path_smoothing()
    example_7_smooth_polygon()
    example_8_font_path()
    example_9_equidistant_sampling()
    example_10_curvature_analysis()
    example_11_class_based_usage()
    example_12_closed_curve()
    
    print("\n" + "#" * 60)
    print("# All examples completed successfully!")
    print("#" * 60 + "\n")


if __name__ == '__main__':
    run_all_examples()