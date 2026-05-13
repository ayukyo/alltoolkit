#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Catmull-Rom Spline Utilities Module
================================================
A comprehensive Catmull-Rom spline utilities module for Python
with zero external dependencies.

Catmull-Rom splines are a type of cubic Hermite spline that pass through
all control points, making them ideal for interpolation in computer graphics,
animation paths, and curve design.

Features:
    - Catmull-Rom spline interpolation (1D, 2D, 3D, ND)
    - Centripetal and chordal parameterization
    - Arc length computation
    - Uniform sampling along curve
    - Curve subdivision and refinement
    - Tangent and normal computation
    - Path smoothing utilities
    - Animation easing helpers

Mathematical Background:
    The Catmull-Rom spline is defined by four control points P0, P1, P2, P3.
    The curve passes through P1 and P2, with P0 and P3 affecting the shape.
    
    Standard parameterization:
        q(t) = 0.5 * [1  t  t^2  t^3] * [ 0  2  0  0] * [P0]
                                         [-1  5  2  0]   [P1]
                                         [ 2 -5  4 -1]   [P2]
                                         [-1  3 -3  1]   [P3]
    
    Centripetal parameterization:
        Avoids cusps and self-intersections by using chord-length based parameters.

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import List, Tuple, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum, auto


class Parameterization(Enum):
    """Parameterization types for Catmull-Rom splines"""
    UNIFORM = auto()       # Standard uniform parameterization
    CHORDAL = auto()       # Chord length parameterization
    CENTRIPETAL = auto()   # Centripetal (sqrt of chord length) parameterization


@dataclass
class Point2D:
    """2D Point representation"""
    x: float
    y: float
    
    def __repr__(self):
        return f"Point2D({self.x:.4f}, {self.y:.4f})"
    
    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10
    
    def __add__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        return Point2D(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x - other.x, self.y - other.y)
        return Point2D(self.x - other, self.y - other)
    
    def __mul__(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Point2D(self.x / scalar, self.y / scalar)
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def distance_to(self, other: 'Point2D') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Point2D':
        mag = self.magnitude()
        if mag < 1e-10:
            return Point2D(0, 0)
        return self / mag


@dataclass
class Point3D:
    """3D Point representation"""
    x: float
    y: float
    z: float
    
    def __repr__(self):
        return f"Point3D({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"
    
    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return False
        return (abs(self.x - other.x) < 1e-10 and 
                abs(self.y - other.y) < 1e-10 and 
                abs(self.z - other.z) < 1e-10)
    
    def __add__(self, other):
        if isinstance(other, Point3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        return Point3D(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other):
        if isinstance(other, Point3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        return Point3D(self.x - other, self.y - other, self.z - other)
    
    def __mul__(self, scalar):
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Point3D(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    def distance_to(self, other: 'Point3D') -> float:
        return math.sqrt((self.x - other.x) ** 2 + 
                        (self.y - other.y) ** 2 + 
                        (self.z - other.z) ** 2)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> 'Point3D':
        mag = self.magnitude()
        if mag < 1e-10:
            return Point3D(0, 0, 0)
        return self / mag


def _get_alpha(p0: List[float], p1: List[float], parameterization: Parameterization) -> float:
    """
    Calculate the alpha value for parameterization between two points.
    
    Args:
        p0: First point coordinates
        p1: Second point coordinates
        parameterization: Type of parameterization to use
        
    Returns:
        Alpha value for parameterization
    """
    if parameterization == Parameterization.UNIFORM:
        return 1.0
    
    # Calculate chord length
    chord_length = sum((a - b) ** 2 for a, b in zip(p0, p1))
    chord_length = math.sqrt(chord_length)
    
    if parameterization == Parameterization.CHORDAL:
        return chord_length
    elif parameterization == Parameterization.CENTRIPETAL:
        return math.sqrt(chord_length)
    
    return 1.0


def catmull_rom_point(p0: List[float], p1: List[float], 
                      p2: List[float], p3: List[float],
                      t: float, 
                      parameterization: Parameterization = Parameterization.UNIFORM,
                      alpha: Optional[float] = None) -> List[float]:
    """
    Compute a point on a Catmull-Rom spline segment.
    
    Args:
        p0, p1, p2, p3: Control points (each is a list of coordinates)
        t: Parameter value (0 to 1 for segment between p1 and p2)
        parameterization: Type of parameterization to use
        alpha: Optional pre-computed alpha for non-uniform parameterization
        
    Returns:
        Point coordinates on the spline
    """
    if alpha is None:
        alpha = _get_alpha(p1, p2, parameterization)
    
    t = t * alpha
    
    t2 = t * t
    t3 = t2 * t
    
    result = []
    for i in range(len(p0)):
        # Catmull-Rom basis matrix multiplication
        a0 = -0.5 * p0[i] + 1.5 * p1[i] - 1.5 * p2[i] + 0.5 * p3[i]
        a1 = p0[i] - 2.5 * p1[i] + 2 * p2[i] - 0.5 * p3[i]
        a2 = -0.5 * p0[i] + 0.5 * p2[i]
        a3 = p1[i]
        
        result.append(a0 * t3 + a1 * t2 + a2 * t + a3)
    
    return result


def catmull_rom_derivative(p0: List[float], p1: List[float],
                          p2: List[float], p3: List[float],
                          t: float,
                          parameterization: Parameterization = Parameterization.UNIFORM,
                          alpha: Optional[float] = None) -> List[float]:
    """
    Compute the first derivative (tangent) of a Catmull-Rom spline.
    
    Args:
        p0, p1, p2, p3: Control points
        t: Parameter value (0 to 1)
        parameterization: Type of parameterization
        alpha: Optional pre-computed alpha
        
    Returns:
        Tangent vector coordinates
    """
    if alpha is None:
        alpha = _get_alpha(p1, p2, parameterization)
    
    t = t * alpha
    t2 = t * t
    
    result = []
    for i in range(len(p0)):
        a0 = -0.5 * p0[i] + 1.5 * p1[i] - 1.5 * p2[i] + 0.5 * p3[i]
        a1 = p0[i] - 2.5 * p1[i] + 2 * p2[i] - 0.5 * p3[i]
        a2 = -0.5 * p0[i] + 0.5 * p2[i]
        
        result.append((3 * a0 * t2 + 2 * a1 * t + a2) * alpha)
    
    return result


def catmull_rom_second_derivative(p0: List[float], p1: List[float],
                                  p2: List[float], p3: List[float],
                                  t: float,
                                  parameterization: Parameterization = Parameterization.UNIFORM,
                                  alpha: Optional[float] = None) -> List[float]:
    """
    Compute the second derivative of a Catmull-Rom spline.
    
    Args:
        p0, p1, p2, p3: Control points
        t: Parameter value (0 to 1)
        parameterization: Type of parameterization
        alpha: Optional pre-computed alpha
        
    Returns:
        Second derivative vector coordinates
    """
    if alpha is None:
        alpha = _get_alpha(p1, p2, parameterization)
    
    t = t * alpha
    
    result = []
    for i in range(len(p0)):
        a0 = -0.5 * p0[i] + 1.5 * p1[i] - 1.5 * p2[i] + 0.5 * p3[i]
        a1 = p0[i] - 2.5 * p1[i] + 2 * p2[i] - 0.5 * p3[i]
        
        result.append((6 * a0 * t + 2 * a1) * alpha * alpha)
    
    return result


def interpolate_1d(values: List[float], 
                   num_points: int = 100,
                   parameterization: Parameterization = Parameterization.CENTRIPETAL,
                   closed: bool = False) -> List[float]:
    """
    Interpolate a 1D sequence of values using Catmull-Rom splines.
    
    Args:
        values: List of control values
        num_points: Number of output points
        parameterization: Type of parameterization
        closed: Whether the curve is closed (loops back to start)
        
    Returns:
        List of interpolated values
    """
    if len(values) < 2:
        return values.copy()
    
    if len(values) == 2:
        # Linear interpolation for 2 points
        return [values[0] + (values[1] - values[0]) * t 
                for t in [i / (num_points - 1) for i in range(num_points)]]
    
    # Extend control points for open curve
    if not closed:
        extended = [values[0]] + list(values) + [values[-1]]
    else:
        extended = [values[-1]] + list(values) + [values[0]]
    
    result = []
    segments = len(values) - 1 if not closed else len(values)
    points_per_segment = num_points // segments
    
    for i in range(len(extended) - 3):
        for j in range(points_per_segment if i < len(extended) - 4 else points_per_segment + 1):
            t = j / points_per_segment
            point = catmull_rom_point(
                [extended[i]], [extended[i+1]], [extended[i+2]], [extended[i+3]],
                t, parameterization
            )
            result.append(point[0])
    
    return result


def interpolate_2d(points: List[Union[Point2D, Tuple[float, float]]],
                   num_points: int = 100,
                   parameterization: Parameterization = Parameterization.CENTRIPETAL,
                   closed: bool = False) -> List[Point2D]:
    """
    Interpolate a sequence of 2D points using Catmull-Rom splines.
    
    Args:
        points: List of control points (Point2D or tuple)
        num_points: Number of output points
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        List of interpolated Point2D objects
    """
    # Convert to list format
    pts = []
    for p in points:
        if isinstance(p, Point2D):
            pts.append([p.x, p.y])
        else:
            pts.append(list(p))
    
    if len(pts) < 2:
        return [Point2D(p[0], p[1]) for p in pts]
    
    if len(pts) == 2:
        return [Point2D(pts[0][0] + (pts[1][0] - pts[0][0]) * t,
                        pts[0][1] + (pts[1][1] - pts[0][1]) * t)
                for t in [i / (num_points - 1) for i in range(num_points)]]
    
    # Extend control points
    if not closed:
        extended = [pts[0]] + pts + [pts[-1]]
    else:
        extended = [pts[-1]] + pts + [pts[0]]
    
    result = []
    segments = len(pts) - 1 if not closed else len(pts)
    points_per_segment = max(1, num_points // segments)
    
    for i in range(len(extended) - 3):
        for j in range(points_per_segment if i < len(extended) - 4 else points_per_segment + 1):
            t = j / points_per_segment
            point = catmull_rom_point(
                extended[i], extended[i+1], extended[i+2], extended[i+3],
                t, parameterization
            )
            result.append(Point2D(point[0], point[1]))
    
    return result


def interpolate_3d(points: List[Union[Point3D, Tuple[float, float, float]]],
                   num_points: int = 100,
                   parameterization: Parameterization = Parameterization.CENTRIPETAL,
                   closed: bool = False) -> List[Point3D]:
    """
    Interpolate a sequence of 3D points using Catmull-Rom splines.
    
    Args:
        points: List of control points (Point3D or tuple)
        num_points: Number of output points
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        List of interpolated Point3D objects
    """
    # Convert to list format
    pts = []
    for p in points:
        if isinstance(p, Point3D):
            pts.append([p.x, p.y, p.z])
        else:
            pts.append(list(p))
    
    if len(pts) < 2:
        return [Point3D(p[0], p[1], p[2]) for p in pts]
    
    if len(pts) == 2:
        return [Point3D(pts[0][0] + (pts[1][0] - pts[0][0]) * t,
                        pts[0][1] + (pts[1][1] - pts[0][1]) * t,
                        pts[0][2] + (pts[1][2] - pts[0][2]) * t)
                for t in [i / (num_points - 1) for i in range(num_points)]]
    
    # Extend control points
    if not closed:
        extended = [pts[0]] + pts + [pts[-1]]
    else:
        extended = [pts[-1]] + pts + [pts[0]]
    
    result = []
    segments = len(pts) - 1 if not closed else len(pts)
    points_per_segment = max(1, num_points // segments)
    
    for i in range(len(extended) - 3):
        for j in range(points_per_segment if i < len(extended) - 4 else points_per_segment + 1):
            t = j / points_per_segment
            point = catmull_rom_point(
                extended[i], extended[i+1], extended[i+2], extended[i+3],
                t, parameterization
            )
            result.append(Point3D(point[0], point[1], point[2]))
    
    return result


def interpolate_nd(points: List[List[float]],
                  num_points: int = 100,
                  parameterization: Parameterization = Parameterization.CENTRIPETAL,
                  closed: bool = False) -> List[List[float]]:
    """
    Interpolate a sequence of N-dimensional points using Catmull-Rom splines.
    
    Args:
        points: List of control points (each is a list of coordinates)
        num_points: Number of output points
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        List of interpolated points
    """
    if len(points) < 2:
        return [p.copy() for p in points]
    
    if len(points) == 2:
        return [[points[0][d] + (points[1][d] - points[0][d]) * t 
                 for d in range(len(points[0]))]
                for t in [i / (num_points - 1) for i in range(num_points)]]
    
    # Extend control points
    if not closed:
        extended = [points[0]] + points + [points[-1]]
    else:
        extended = [points[-1]] + points + [points[0]]
    
    result = []
    segments = len(points) - 1 if not closed else len(points)
    points_per_segment = max(1, num_points // segments)
    
    for i in range(len(extended) - 3):
        for j in range(points_per_segment if i < len(extended) - 4 else points_per_segment + 1):
            t = j / points_per_segment
            point = catmull_rom_point(
                extended[i], extended[i+1], extended[i+2], extended[i+3],
                t, parameterization
            )
            result.append(point)
    
    return result


def compute_arc_length(points: List[Union[Point2D, Tuple[float, float]]],
                       parameterization: Parameterization = Parameterization.CENTRIPETAL,
                       closed: bool = False,
                       samples_per_segment: int = 50) -> float:
    """
    Compute the approximate arc length of a Catmull-Rom spline.
    
    Args:
        points: Control points
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        samples_per_segment: Number of samples per segment for approximation
        
    Returns:
        Approximate arc length
    """
    if len(points) < 2:
        return 0.0
    
    interpolated = interpolate_2d(points, 
                                   len(points) * samples_per_segment,
                                   parameterization, closed)
    
    length = 0.0
    for i in range(1, len(interpolated)):
        length += interpolated[i].distance_to(interpolated[i-1])
    
    return length


def sample_at_distance(points: List[Union[Point2D, Tuple[float, float]]],
                       distance: float,
                       parameterization: Parameterization = Parameterization.CENTRIPETAL,
                       closed: bool = False,
                       resolution: int = 1000) -> Optional[Point2D]:
    """
    Sample a point on the spline at a specific distance from the start.
    
    Args:
        points: Control points
        distance: Distance from the start of the curve
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        resolution: Number of sample points for interpolation
        
    Returns:
        Point2D at the specified distance, or None if distance exceeds curve length
    """
    if len(points) < 2 or distance < 0:
        return None
    
    interpolated = interpolate_2d(points, resolution, parameterization, closed)
    
    accumulated = 0.0
    for i in range(1, len(interpolated)):
        segment_length = interpolated[i].distance_to(interpolated[i-1])
        if accumulated + segment_length >= distance:
            # Interpolate within this segment
            if segment_length < 1e-10:
                return interpolated[i-1]
            t = (distance - accumulated) / segment_length
            return Point2D(
                interpolated[i-1].x + t * (interpolated[i].x - interpolated[i-1].x),
                interpolated[i-1].y + t * (interpolated[i].y - interpolated[i-1].y)
            )
        accumulated += segment_length
    
    return interpolated[-1]


def get_tangent_2d(points: List[Union[Point2D, Tuple[float, float]]],
                   t: float,
                   parameterization: Parameterization = Parameterization.CENTRIPETAL,
                   closed: bool = False) -> Point2D:
    """
    Compute the tangent vector at a parameter value t (0 to 1).
    
    Args:
        points: Control points
        t: Parameter value (0 to 1 for the entire curve)
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        Normalized tangent vector as Point2D
    """
    pts = []
    for p in points:
        if isinstance(p, Point2D):
            pts.append([p.x, p.y])
        else:
            pts.append(list(p))
    
    if len(pts) < 2:
        return Point2D(1, 0)
    
    if not closed:
        extended = [pts[0]] + pts + [pts[-1]]
    else:
        extended = [pts[-1]] + pts + [pts[0]]
    
    # Map t to segment
    segments = len(pts) - 1 if not closed else len(pts)
    segment_idx = min(int(t * segments), segments - 1)
    local_t = (t * segments) - segment_idx
    
    if segment_idx >= len(extended) - 3:
        segment_idx = len(extended) - 4
        local_t = 1.0
    
    tangent = catmull_rom_derivative(
        extended[segment_idx], extended[segment_idx+1],
        extended[segment_idx+2], extended[segment_idx+3],
        local_t, parameterization
    )
    
    return Point2D(tangent[0], tangent[1]).normalize()


def get_normal_2d(points: List[Union[Point2D, Tuple[float, float]]],
                  t: float,
                  parameterization: Parameterization = Parameterization.CENTRIPETAL,
                  closed: bool = False) -> Point2D:
    """
    Compute the normal vector at a parameter value t (0 to 1).
    The normal is perpendicular to the tangent (rotated 90 degrees counterclockwise).
    
    Args:
        points: Control points
        t: Parameter value (0 to 1)
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        Normalized normal vector as Point2D
    """
    tangent = get_tangent_2d(points, t, parameterization, closed)
    # Rotate 90 degrees counterclockwise
    return Point2D(-tangent.y, tangent.x)


def smooth_path(points: List[Union[Point2D, Tuple[float, float]]],
                iterations: int = 1,
                parameterization: Parameterization = Parameterization.CENTRIPETAL,
                subdivisions: int = 4) -> List[Point2D]:
    """
    Smooth a path using Catmull-Rom splines with iterative subdivision.
    
    Args:
        points: Original path points
        iterations: Number of smoothing iterations
        parameterization: Type of parameterization
        subdivisions: Subdivisions per segment per iteration
        
    Returns:
        Smoothed path points
    """
    if len(points) < 3:
        return [Point2D(p[0], p[1]) if isinstance(p, tuple) else p for p in points]
    
    current = points
    for _ in range(iterations):
        current = interpolate_2d(current, len(current) * subdivisions, parameterization)
    
    return current


def create_animation_path(keyframes: List[Union[Point2D, Tuple[float, float]]],
                          num_frames: int,
                          parameterization: Parameterization = Parameterization.CENTRIPETAL,
                          easing: Optional[str] = None) -> List[Point2D]:
    """
    Create an animation path with optional easing.
    
    Args:
        keyframes: Key positions for the animation
        num_frames: Total number of frames
        parameterization: Type of parameterization
        easing: Optional easing function ('linear', 'ease-in', 'ease-out', 'ease-in-out')
        
    Returns:
        List of positions for each frame
    """
    if len(keyframes) < 2:
        return [Point2D(p[0], p[1]) if isinstance(p, tuple) else p for p in keyframes] * num_frames
    
    # Interpolate at high resolution first
    high_res = interpolate_2d(keyframes, num_frames * 4, parameterization)
    
    # Apply easing to frame selection
    result = []
    for i in range(num_frames):
        t = i / (num_frames - 1) if num_frames > 1 else 0
        
        if easing == 'ease-in':
            t = t * t
        elif easing == 'ease-out':
            t = 1 - (1 - t) * (1 - t)
        elif easing == 'ease-in-out':
            if t < 0.5:
                t = 2 * t * t
            else:
                t = 1 - 2 * (1 - t) * (1 - t)
        
        idx = int(t * (len(high_res) - 1))
        result.append(high_res[min(idx, len(high_res) - 1)])
    
    return result


def curvature_at_point(p0: List[float], p1: List[float], 
                       p2: List[float], p3: List[float],
                       t: float,
                       parameterization: Parameterization = Parameterization.UNIFORM) -> float:
    """
    Compute the curvature at a point on the spline.
    
    Curvature κ = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
    
    Args:
        p0, p1, p2, p3: Control points
        t: Parameter value
        parameterization: Type of parameterization
        
    Returns:
        Curvature value
    """
    first_deriv = catmull_rom_derivative(p0, p1, p2, p3, t, parameterization)
    second_deriv = catmull_rom_second_derivative(p0, p1, p2, p3, t, parameterization)
    
    if len(first_deriv) >= 2:
        numerator = abs(first_deriv[0] * second_deriv[1] - 
                       first_deriv[1] * second_deriv[0])
        denominator = (first_deriv[0]**2 + first_deriv[1]**2) ** 1.5
        
        if denominator < 1e-10:
            return 0.0
        return numerator / denominator
    
    return 0.0


def find_inflection_points(p0: List[float], p1: List[float],
                          p2: List[float], p3: List[float],
                          parameterization: Parameterization = Parameterization.UNIFORM,
                          resolution: int = 100) -> List[float]:
    """
    Find approximate inflection points on a spline segment.
    
    Args:
        p0, p1, p2, p3: Control points
        parameterization: Type of parameterization
        resolution: Number of samples to check
        
    Returns:
        List of t values where inflection points occur
    """
    inflection_points = []
    prev_curvature = None
    
    for i in range(resolution + 1):
        t = i / resolution
        curv = curvature_at_point(p0, p1, p2, p3, t, parameterization)
        
        if prev_curvature is not None:
            # Check for sign change
            if prev_curvature * curv < 0:
                # Binary search for more precise location
                t_low = (i - 1) / resolution
                t_high = t
                
                for _ in range(10):
                    t_mid = (t_low + t_high) / 2
                    curv_mid = curvature_at_point(p0, p1, p2, p3, t_mid, parameterization)
                    if curv_mid * prev_curvature < 0:
                        t_high = t_mid
                    else:
                        t_low = t_mid
                
                inflection_points.append((t_low + t_high) / 2)
        
        prev_curvature = curv
    
    return inflection_points


def fit_catmull_rom_to_points(data_points: List[Union[Point2D, Tuple[float, float]]],
                               num_control: int,
                               parameterization: Parameterization = Parameterization.CENTRIPETAL) -> List[Point2D]:
    """
    Fit a Catmull-Rom spline to a set of data points by finding optimal control points.
    
    Uses a simple approach: sample the data uniformly to create control points.
    For more accurate fitting, consider using least-squares optimization.
    
    Args:
        data_points: Points to fit
        num_control: Number of control points to use
        parameterization: Type of parameterization
        
    Returns:
        List of control points
    """
    if len(data_points) < 2:
        return [Point2D(p[0], p[1]) if isinstance(p, tuple) else p for p in data_points]
    
    # Convert to list
    pts = []
    for p in data_points:
        if isinstance(p, Point2D):
            pts.append(p)
        else:
            pts.append(Point2D(p[0], p[1]))
    
    if num_control >= len(pts):
        return pts
    
    # Uniform sampling
    control_points = []
    for i in range(num_control):
        t = i / (num_control - 1) if num_control > 1 else 0
        idx = t * (len(pts) - 1)
        low = int(idx)
        high = min(low + 1, len(pts) - 1)
        frac = idx - low
        
        control_points.append(Point2D(
            pts[low].x + frac * (pts[high].x - pts[low].x),
            pts[low].y + frac * (pts[high].y - pts[low].y)
        ))
    
    return control_points


def subdivide_segment(p0: List[float], p1: List[float],
                      p2: List[float], p3: List[float],
                      parameterization: Parameterization = Parameterization.UNIFORM) -> Tuple[List[List[float]], List[List[float]], List[List[float]], List[List[float]], List[List[float]]]:
    """
    Subdivide a Catmull-Rom segment into two halves, returning new control points.
    
    Args:
        p0, p1, p2, p3: Original control points
        parameterization: Type of parameterization
        
    Returns:
        Tuple of (new_p0, new_p1_left, new_p2_left, new_p1_right, new_p2_right) for two new segments
    """
    # Points at t=0.5
    mid = catmull_rom_point(p0, p1, p2, p3, 0.5, parameterization)
    
    # Tangent at t=0.5
    tangent = catmull_rom_derivative(p0, p1, p2, p3, 0.5, parameterization)
    
    # Scale tangent for new control points
    scale = 0.125  # Factor for creating smooth control points
    new_control_left = [mid[i] - tangent[i] * scale for i in range(len(mid))]
    new_control_right = [mid[i] + tangent[i] * scale for i in range(len(mid))]
    
    return (p0, p1, mid, new_control_left, new_control_right)


# ============================================================================
# Convenience Classes
# ============================================================================

class CatmullRomSpline2D:
    """
    A Catmull-Rom spline class for 2D curves with convenient methods.
    """
    
    def __init__(self, control_points: List[Union[Point2D, Tuple[float, float]]],
                 parameterization: Parameterization = Parameterization.CENTRIPETAL,
                 closed: bool = False):
        """
        Initialize the spline with control points.
        
        Args:
            control_points: List of control points
            parameterization: Type of parameterization
            closed: Whether the curve is closed
        """
        self.control_points = []
        for p in control_points:
            if isinstance(p, Point2D):
                self.control_points.append(p)
            else:
                self.control_points.append(Point2D(p[0], p[1]))
        
        self.parameterization = parameterization
        self.closed = closed
        self._cached_points: Optional[List[Point2D]] = None
        self._cache_resolution: int = 0
    
    def point_at(self, t: float) -> Point2D:
        """
        Get point at parameter t (0 to 1).
        
        Args:
            t: Parameter value
            
        Returns:
            Point2D at parameter t
        """
        if len(self.control_points) < 2:
            return self.control_points[0] if self.control_points else Point2D(0, 0)
        
        pts = [[p.x, p.y] for p in self.control_points]
        
        if not self.closed:
            extended = [pts[0]] + pts + [pts[-1]]
        else:
            extended = [pts[-1]] + pts + [pts[0]]
        
        segments = len(pts) - 1 if not self.closed else len(pts)
        segment_idx = min(int(t * segments), segments - 1)
        local_t = (t * segments) - segment_idx
        
        if segment_idx >= len(extended) - 3:
            segment_idx = len(extended) - 4
            local_t = 1.0
        
        point = catmull_rom_point(
            extended[segment_idx], extended[segment_idx+1],
            extended[segment_idx+2], extended[segment_idx+3],
            local_t, self.parameterization
        )
        
        return Point2D(point[0], point[1])
    
    def tangent_at(self, t: float) -> Point2D:
        """Get normalized tangent at parameter t."""
        return get_tangent_2d(self.control_points, t, self.parameterization, self.closed)
    
    def normal_at(self, t: float) -> Point2D:
        """Get normalized normal at parameter t."""
        return get_normal_2d(self.control_points, t, self.parameterization, self.closed)
    
    def interpolate(self, num_points: int = 100) -> List[Point2D]:
        """
        Interpolate the full curve.
        
        Args:
            num_points: Number of points to generate
            
        Returns:
            List of Point2D along the curve
        """
        return interpolate_2d(self.control_points, num_points, 
                             self.parameterization, self.closed)
    
    def arc_length(self, samples_per_segment: int = 50) -> float:
        """Compute approximate arc length."""
        return compute_arc_length(self.control_points, self.parameterization, 
                                 self.closed, samples_per_segment)
    
    def sample_at_distance(self, distance: float, resolution: int = 1000) -> Optional[Point2D]:
        """Sample point at specific distance from start."""
        return sample_at_distance(self.control_points, distance, 
                                 self.parameterization, self.closed, resolution)
    
    def curvature_at(self, t: float) -> float:
        """Compute curvature at parameter t."""
        if len(self.control_points) < 2:
            return 0.0
        
        pts = [[p.x, p.y] for p in self.control_points]
        
        if not self.closed:
            extended = [pts[0]] + pts + [pts[-1]]
        else:
            extended = [pts[-1]] + pts + [pts[0]]
        
        segments = len(pts) - 1 if not self.closed else len(pts)
        segment_idx = min(int(t * segments), segments - 1)
        local_t = (t * segments) - segment_idx
        
        if segment_idx >= len(extended) - 3:
            segment_idx = len(extended) - 4
            local_t = 1.0
        
        return curvature_at_point(
            extended[segment_idx], extended[segment_idx+1],
            extended[segment_idx+2], extended[segment_idx+3],
            local_t, self.parameterization
        )
    
    def smooth(self, iterations: int = 1) -> 'CatmullRomSpline2D':
        """
        Create a smoothed version of this spline.
        
        Args:
            iterations: Number of smoothing iterations
            
        Returns:
            New smoothed CatmullRomSpline2D
        """
        smoothed = smooth_path(self.control_points, iterations, 
                              self.parameterization)
        # Sample control points from smoothed path
        num_control = len(self.control_points)
        step = len(smoothed) / num_control
        new_control = [smoothed[min(int(i * step), len(smoothed) - 1)] 
                      for i in range(num_control)]
        
        return CatmullRomSpline2D(new_control, self.parameterization, self.closed)


class CatmullRomSpline3D:
    """
    A Catmull-Rom spline class for 3D curves.
    """
    
    def __init__(self, control_points: List[Union[Point3D, Tuple[float, float, float]]],
                 parameterization: Parameterization = Parameterization.CENTRIPETAL,
                 closed: bool = False):
        """
        Initialize the spline with control points.
        
        Args:
            control_points: List of control points
            parameterization: Type of parameterization
            closed: Whether the curve is closed
        """
        self.control_points = []
        for p in control_points:
            if isinstance(p, Point3D):
                self.control_points.append(p)
            else:
                self.control_points.append(Point3D(p[0], p[1], p[2]))
        
        self.parameterization = parameterization
        self.closed = closed
    
    def point_at(self, t: float) -> Point3D:
        """Get point at parameter t (0 to 1)."""
        if len(self.control_points) < 2:
            return self.control_points[0] if self.control_points else Point3D(0, 0, 0)
        
        pts = [[p.x, p.y, p.z] for p in self.control_points]
        
        if not self.closed:
            extended = [pts[0]] + pts + [pts[-1]]
        else:
            extended = [pts[-1]] + pts + [pts[0]]
        
        segments = len(pts) - 1 if not self.closed else len(pts)
        segment_idx = min(int(t * segments), segments - 1)
        local_t = (t * segments) - segment_idx
        
        if segment_idx >= len(extended) - 3:
            segment_idx = len(extended) - 4
            local_t = 1.0
        
        point = catmull_rom_point(
            extended[segment_idx], extended[segment_idx+1],
            extended[segment_idx+2], extended[segment_idx+3],
            local_t, self.parameterization
        )
        
        return Point3D(point[0], point[1], point[2])
    
    def tangent_at(self, t: float) -> Point3D:
        """Get normalized tangent at parameter t."""
        if len(self.control_points) < 2:
            return Point3D(1, 0, 0)
        
        pts = [[p.x, p.y, p.z] for p in self.control_points]
        
        if not self.closed:
            extended = [pts[0]] + pts + [pts[-1]]
        else:
            extended = [pts[-1]] + pts + [pts[0]]
        
        segments = len(pts) - 1 if not self.closed else len(pts)
        segment_idx = min(int(t * segments), segments - 1)
        local_t = (t * segments) - segment_idx
        
        if segment_idx >= len(extended) - 3:
            segment_idx = len(extended) - 4
            local_t = 1.0
        
        tangent = catmull_rom_derivative(
            extended[segment_idx], extended[segment_idx+1],
            extended[segment_idx+2], extended[segment_idx+3],
            local_t, self.parameterization
        )
        
        return Point3D(tangent[0], tangent[1], tangent[2]).normalize()
    
    def interpolate(self, num_points: int = 100) -> List[Point3D]:
        """Interpolate the full curve."""
        return interpolate_3d(self.control_points, num_points, 
                             self.parameterization, self.closed)


# ============================================================================
# Specialized Utilities
# ============================================================================

def create_smooth_polygon(vertices: List[Union[Point2D, Tuple[float, float]]],
                          corner_sharpness: float = 0.5,
                          num_points: int = 100) -> List[Point2D]:
    """
    Create a smooth closed curve approximating a polygon.
    
    Args:
        vertices: Polygon vertices
        corner_sharpness: How sharp corners should be (0 = smooth, 1 = sharp)
        num_points: Number of output points
        
    Returns:
        Smooth polygon curve points
    """
    if len(vertices) < 3:
        return interpolate_2d(vertices, num_points, closed=True)
    
    # For smooth corners, just use standard Catmull-Rom
    if corner_sharpness < 0.1:
        return interpolate_2d(vertices, num_points, closed=True)
    
    # For sharper corners, add duplicate vertices
    if corner_sharpness > 0.9:
        # Add duplicate vertices for sharp corners
        sharp_vertices = []
        for v in vertices:
            sharp_vertices.append(v)
            sharp_vertices.append(v)
        return interpolate_2d(sharp_vertices, num_points * 2, closed=True)
    
    # Interpolate between smooth and sharp
    smooth_curve = interpolate_2d(vertices, num_points, closed=True)
    sharp_vertices = []
    for v in vertices:
        sharp_vertices.append(v)
    sharp_curve = interpolate_2d(sharp_vertices, num_points, closed=True)
    
    # Blend
    result = []
    for i in range(min(len(smooth_curve), len(sharp_curve))):
        result.append(Point2D(
            smooth_curve[i].x * (1 - corner_sharpness) + sharp_curve[i].x * corner_sharpness,
            smooth_curve[i].y * (1 - corner_sharpness) + sharp_curve[i].y * corner_sharpness
        ))
    
    return result


def generate_font_path(points: List[Union[Point2D, Tuple[float, float]]],
                       tension: float = 0.5,
                       num_points: int = 50) -> List[Point2D]:
    """
    Generate a smooth path suitable for font/vector graphics.
    Uses centripetal Catmull-Rom for optimal results.
    
    Args:
        points: Control points
        tension: Tension factor (affects curvature)
        num_points: Output points per segment
        
    Returns:
        Smooth path points
    """
    if len(points) < 2:
        return [Point2D(p[0], p[1]) if isinstance(p, tuple) else p for p in points]
    
    # Standard centripetal Catmull-Rom works well for fonts
    return interpolate_2d(points, num_points, Parameterization.CENTRIPETAL)


def resample_curve_equidistant(points: List[Union[Point2D, Tuple[float, float]]],
                               num_points: int,
                               parameterization: Parameterization = Parameterization.CENTRIPETAL,
                               closed: bool = False) -> List[Point2D]:
    """
    Resample a curve to have equidistant points.
    
    Args:
        points: Control points
        num_points: Number of output points
        parameterization: Type of parameterization
        closed: Whether the curve is closed
        
    Returns:
        List of points with equal arc length between them
    """
    if len(points) < 2:
        return [Point2D(p[0], p[1]) if isinstance(p, tuple) else p for p in points]
    
    # First interpolate at high resolution
    high_res = interpolate_2d(points, num_points * 10, parameterization, closed)
    
    # Compute cumulative arc lengths
    arc_lengths = [0.0]
    for i in range(1, len(high_res)):
        arc_lengths.append(arc_lengths[-1] + high_res[i].distance_to(high_res[i-1]))
    
    total_length = arc_lengths[-1]
    if total_length < 1e-10:
        return high_res[:num_points]
    
    # Sample at equidistant points
    result = [high_res[0]]
    for i in range(1, num_points):
        target_length = (i / (num_points - 1)) * total_length
        
        # Binary search for position
        low, high = 0, len(arc_lengths) - 1
        while high - low > 1:
            mid = (low + high) // 2
            if arc_lengths[mid] < target_length:
                low = mid
            else:
                high = mid
        
        # Interpolate between points
        if high >= len(high_res):
            result.append(high_res[-1])
        else:
            segment_length = arc_lengths[high] - arc_lengths[low]
            if segment_length < 1e-10:
                result.append(high_res[low])
            else:
                t = (target_length - arc_lengths[low]) / segment_length
                result.append(Point2D(
                    high_res[low].x + t * (high_res[high].x - high_res[low].x),
                    high_res[low].y + t * (high_res[high].y - high_res[low].y)
                ))
    
    return result


# Module exports
__all__ = [
    # Enums and data classes
    'Parameterization',
    'Point2D',
    'Point3D',
    # Core functions
    'catmull_rom_point',
    'catmull_rom_derivative',
    'catmull_rom_second_derivative',
    # Interpolation functions
    'interpolate_1d',
    'interpolate_2d',
    'interpolate_3d',
    'interpolate_nd',
    # Arc length and sampling
    'compute_arc_length',
    'sample_at_distance',
    'resample_curve_equidistant',
    # Derivatives and normals
    'get_tangent_2d',
    'get_normal_2d',
    'curvature_at_point',
    'find_inflection_points',
    # Utilities
    'smooth_path',
    'create_animation_path',
    'fit_catmull_rom_to_points',
    'create_smooth_polygon',
    'generate_font_path',
    'subdivide_segment',
    # Classes
    'CatmullRomSpline2D',
    'CatmullRomSpline3D',
]