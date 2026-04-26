"""
Spline Utils - 样条曲线工具库
"""

from .spline import (
    Point2D, Point3D,
    linear_spline, cubic_spline,
    catmull_rom_spline, b_spline,
    hermite_spline, hermite_spline_auto,
    sample_curve, curve_length, resample_curve, smooth_points,
    interpolate
)

__all__ = [
    'Point2D', 'Point3D',
    'linear_spline', 'cubic_spline',
    'catmull_rom_spline', 'b_spline',
    'hermite_spline', 'hermite_spline_auto',
    'sample_curve', 'curve_length', 'resample_curve', 'smooth_points',
    'interpolate'
]

__version__ = '1.0.0'