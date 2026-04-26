#!/usr/bin/env python3
"""
SVG Utils Examples - Demonstrates the capabilities of svg_utils module.

Run this script to generate example SVG files:
    python example.py

This will create several SVG files in the examples/ directory.
"""

import os
import math
from svg_utils import (
    SVG,
    rect, circle, ellipse, line, polyline, polygon, text,
    Path, LinearGradient, RadialGradient,
    translate, rotate, scale,
    points_to_polygon_path, arc_path, circle_path,
    rounded_rect_path, star_path, regular_polygon_path,
    rgb_to_hex, hex_to_rgb, lighten, darken,
    PALETTE, group, image, arrow_marker
)


def ensure_dir(path: str):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)


def example_basic_shapes():
    """Example 1: Basic shapes."""
    svg = SVG(300, 200)
    svg.set_title("Basic Shapes Example")
    svg.set_desc("Demonstrates rectangles, circles, ellipses, and lines")
    
    # Background
    svg.add(rect(0, 0, 300, 200, fill="#f8f9fa"))
    
    # Rectangle with rounded corners
    svg.add(rect(20, 20, 80, 60, fill="#3498db", rx=10, ry=10))
    
    # Circle
    svg.add(circle(170, 50, 30, fill="#e74c3c"))
    
    # Ellipse
    svg.add(ellipse(260, 50, 30, 20, fill="#2ecc71"))
    
    # Line with stroke
    svg.add(line(20, 100, 280, 100, stroke="#34495e", stroke_width=3))
    
    # Polygon (triangle)
    svg.add(polygon([(50, 180), (100, 120), (150, 180)], fill="#9b59b6"))
    
    # Polyline (zigzag)
    points = [(180, 180), (200, 140), (220, 180), (240, 140), (260, 180)]
    svg.add(polyline(points, fill="none", stroke="#e67e22", stroke_width=3))
    
    # Text
    svg.add(text(150, 20, "Basic Shapes", font_size=14, fill="#2c3e50"))
    
    return svg


def example_gradients():
    """Example 2: Gradients."""
    svg = SVG(400, 200)
    svg.set_title("Gradient Examples")
    
    # Linear gradient (horizontal)
    linear_grad = LinearGradient("linear1", x1="0%", y1="0%", x2="100%", y2="0%")
    linear_grad.add_stop("0%", "#3498db").add_stop("100%", "#e74c3c")
    svg.add_def(linear_grad.build())
    
    # Linear gradient (vertical)
    vertical_grad = LinearGradient("linear2", x1="0%", y1="0%", x2="0%", y2="100%")
    vertical_grad.add_stop("0%", "#2ecc71").add_stop("100%", "#27ae60")
    svg.add_def(vertical_grad.build())
    
    # Radial gradient
    radial_grad = RadialGradient("radial1", cx="50%", cy="50%", r="50%")
    radial_grad.add_stop("0%", "#f1c40f").add_stop("100%", "#e67e22")
    svg.add_def(radial_grad.build())
    
    # Use gradients
    svg.add(rect(20, 20, 100, 160, fill="url(#linear1)"))
    svg.add(rect(140, 20, 100, 160, fill="url(#linear2)"))
    svg.add(circle(310, 100, 70, fill="url(#radial1)"))
    
    # Labels
    svg.add(text(70, 200, "Linear H", font_size=12, text_anchor="middle"))
    svg.add(text(190, 200, "Linear V", font_size=12, text_anchor="middle"))
    svg.add(text(310, 200, "Radial", font_size=12, text_anchor="middle"))
    
    return svg


def example_paths():
    """Example 3: Path commands."""
    svg = SVG(400, 200)
    svg.set_title("Path Examples")
    
    # Star path
    star = star_path(60, 100, 50, 25, 5)
    star.fill = "#f1c40f"
    star.stroke = "#e67e22"
    star.stroke_width = 2
    svg.add(star.build())
    
    # Regular hexagon
    hexagon = regular_polygon_path(160, 100, 50, 6)
    hexagon.fill = "#3498db"
    hexagon.stroke = "#2980b9"
    hexagon.stroke_width = 2
    svg.add(hexagon.build())
    
    # Rounded rectangle path
    rounded = rounded_rect_path(220, 50, 120, 100, 15)
    rounded.fill = "#2ecc71"
    rounded.stroke = "#27ae60"
    rounded.stroke_width = 2
    svg.add(rounded.build())
    
    # Arc path
    arc = arc_path(350, 100, 40, 0, 270)
    arc.stroke = "#e74c3c"
    arc.stroke_width = 4
    svg.add(arc.build())
    
    return svg


def example_transforms():
    """Example 4: Transforms."""
    svg = SVG(400, 200)
    svg.set_title("Transform Examples")
    
    # Original rectangle
    svg.add(rect(20, 80, 50, 40, fill="#bdc3c7"))
    svg.add(text(45, 145, "Original", font_size=10, text_anchor="middle"))
    
    # Translated
    translated = rect(0, 0, 50, 40, fill="#3498db")
    translated.set_attr("transform", translate(140, 80))
    svg.add(translated)
    svg.add(text(165, 145, "Translated", font_size=10, text_anchor="middle"))
    
    # Rotated
    rotated = rect(0, 0, 50, 40, fill="#e74c3c")
    rotated.set_attr("transform", f"{translate(270, 100)} {rotate(45, 25, 20)}")
    svg.add(rotated)
    svg.add(text(295, 145, "Rotated", font_size=10, text_anchor="middle"))
    
    # Scaled
    scaled = rect(0, 0, 50, 40, fill="#2ecc71")
    scaled.set_attr("transform", f"{translate(360, 60)} {scale(0.75)}")
    svg.add(scaled)
    svg.add(text(380, 145, "Scaled", font_size=10, text_anchor="middle"))
    
    return svg


def example_complex_drawing():
    """Example 5: Complex drawing - simple house."""
    svg = SVG(400, 300)
    svg.set_title("Complex Drawing - House")
    
    # Sky gradient
    sky_grad = LinearGradient("sky", x1="0%", y1="0%", x2="0%", y2="100%")
    sky_grad.add_stop("0%", "#87CEEB").add_stop("100%", "#E0F6FF")
    svg.add_def(sky_grad.build())
    
    # Ground gradient
    ground_grad = LinearGradient("ground", x1="0%", y1="0%", x2="0%", y2="100%")
    ground_grad.add_stop("0%", "#90EE90").add_stop("100%", "#228B22")
    svg.add_def(ground_grad.build())
    
    # Draw sky
    svg.add(rect(0, 0, 400, 250, fill="url(#sky)"))
    
    # Draw ground
    svg.add(rect(0, 250, 400, 50, fill="url(#ground)"))
    
    # House body
    svg.add(rect(100, 150, 200, 100, fill="#DEB887", stroke="#8B4513", stroke_width=2))
    
    # Roof
    roof = polygon([(90, 150), (200, 50), (310, 150)], fill="#8B0000", stroke="#4a0000", stroke_width=2)
    svg.add(roof)
    
    # Door
    svg.add(rect(175, 200, 50, 50, fill="#8B4513", stroke="#5D3A1A", stroke_width=2))
    
    # Door handle
    svg.add(circle(215, 225, 4, fill="#FFD700"))
    
    # Windows
    svg.add(rect(120, 170, 40, 35, fill="#87CEEB", stroke="#4a4a4a", stroke_width=2))
    svg.add(rect(240, 170, 40, 35, fill="#87CEEB", stroke="#4a4a4a", stroke_width=2))
    
    # Window panes
    svg.add(line(140, 170, 140, 205, stroke="#4a4a4a", stroke_width=1))
    svg.add(line(120, 187, 160, 187, stroke="#4a4a4a", stroke_width=1))
    svg.add(line(260, 170, 260, 205, stroke="#4a4a4a", stroke_width=1))
    svg.add(line(240, 187, 280, 187, stroke="#4a4a4a", stroke_width=1))
    
    # Chimney
    svg.add(rect(250, 70, 25, 60, fill="#A0522D", stroke="#8B4513", stroke_width=1))
    
    # Sun
    sun_grad = RadialGradient("sun", cx="50%", cy="50%", r="50%")
    sun_grad.add_stop("0%", "#FFFF00").add_stop("100%", "#FFA500")
    svg.add_def(sun_grad.build())
    svg.add(circle(50, 50, 30, fill="url(#sun)"))
    
    # Sun rays
    for i in range(8):
        angle = i * 45 * math.pi / 180
        x1 = 50 + 35 * math.cos(angle)
        y1 = 50 + 35 * math.sin(angle)
        x2 = 50 + 50 * math.cos(angle)
        y2 = 50 + 50 * math.sin(angle)
        svg.add(line(x1, y1, x2, y2, stroke="#FFD700", stroke_width=3))
    
    return svg


def example_chart():
    """Example 6: Simple bar chart."""
    svg = SVG(400, 250)
    svg.set_title("Bar Chart Example")
    
    data = [
        ("Jan", 65, "#3498db"),
        ("Feb", 40, "#2ecc71"),
        ("Mar", 80, "#e74c3c"),
        ("Apr", 55, "#f39c12"),
        ("May", 90, "#9b59b6"),
        ("Jun", 70, "#1abc9c"),
    ]
    
    chart_left = 60
    chart_bottom = 200
    chart_height = 150
    bar_width = 40
    bar_gap = 15
    
    # Background
    svg.add(rect(0, 0, 400, 250, fill="#fafafa"))
    
    # Y-axis
    svg.add(line(chart_left, 50, chart_left, chart_bottom, stroke="#333", stroke_width=2))
    
    # X-axis
    svg.add(line(chart_left, chart_bottom, 380, chart_bottom, stroke="#333", stroke_width=2))
    
    # Grid lines
    for i in range(5):
        y = chart_bottom - (i + 1) * 30
        svg.add(line(chart_left, y, 380, y, stroke="#e0e0e0", stroke_width=1))
        svg.add(text(50, y + 5, str((i + 1) * 20), font_size=10, text_anchor="end"))
    
    # Bars
    for i, (label, value, color) in enumerate(data):
        x = chart_left + bar_gap + i * (bar_width + bar_gap)
        bar_height = (value / 100) * chart_height
        y = chart_bottom - bar_height
        
        svg.add(rect(x, y, bar_width, bar_height, fill=color))
        svg.add(text(x + bar_width / 2, chart_bottom + 15, label, font_size=10, text_anchor="middle"))
    
    # Title
    svg.add(text(200, 30, "Monthly Sales", font_size=16, fill="#333", text_anchor="middle"))
    
    return svg


def example_color_palette():
    """Example 7: Using color utilities."""
    svg = SVG(500, 200)
    svg.set_title("Color Palette Example")
    
    colors = PALETTE["vibrant"]
    x = 20
    
    for i, color in enumerate(colors):
        # Original color
        svg.add(rect(x, 30, 60, 40, fill=color))
        
        # Lightened
        light = lighten(color, 0.3)
        svg.add(rect(x, 80, 60, 40, fill=light))
        
        # Darkened
        dark = darken(color, 0.3)
        svg.add(rect(x, 130, 60, 40, fill=dark))
        
        # Labels
        svg.add(text(x + 30, 25, color, font_size=8, text_anchor="middle"))
        svg.add(text(x + 30, 185, f"RGB: {hex_to_rgb(color)}", font_size=7, text_anchor="middle"))
        
        x += 80
    
    # Legend
    svg.add(text(30, 220, "Top: Original | Middle: Lightened | Bottom: Darkened", font_size=10))
    
    return svg


def example_arrows():
    """Example 8: Arrows with markers."""
    svg = SVG(400, 200)
    svg.set_title("Arrows Example")
    
    # Define arrow markers
    svg.add_def(arrow_marker("arrowRed", size=10, fill="#e74c3c"))
    svg.add_def(arrow_marker("arrowBlue", size=10, fill="#3498db"))
    svg.add_def(arrow_marker("arrowGreen", size=10, fill="#2ecc71"))
    
    # Horizontal arrows
    arrow1 = line(50, 50, 350, 50, stroke="#e74c3c", stroke_width=3)
    arrow1.set_attr("marker_end", "url(#arrowRed)")
    svg.add(arrow1)
    
    # Vertical arrow
    arrow2 = line(200, 70, 200, 180, stroke="#3498db", stroke_width=3)
    arrow2.set_attr("marker_end", "url(#arrowBlue)")
    svg.add(arrow2)
    
    # Diagonal arrows
    arrow3 = line(50, 150, 150, 100, stroke="#2ecc71", stroke_width=3)
    arrow3.set_attr("marker_end", "url(#arrowGreen)")
    svg.add(arrow3)
    
    arrow4 = line(250, 100, 350, 150, stroke="#2ecc71", stroke_width=3)
    arrow4.set_attr("marker_end", "url(#arrowGreen)")
    svg.add(arrow4)
    
    # Labels
    svg.add(text(50, 40, "Horizontal", font_size=12))
    svg.add(text(210, 80, "Vertical", font_size=12))
    svg.add(text(70, 180, "Diagonals", font_size=12))
    
    return svg


def main():
    """Generate all example SVGs."""
    output_dir = os.path.join(os.path.dirname(__file__), "examples")
    ensure_dir(output_dir)
    
    examples = [
        ("01_basic_shapes", example_basic_shapes),
        ("02_gradients", example_gradients),
        ("03_paths", example_paths),
        ("04_transforms", example_transforms),
        ("05_complex_drawing", example_complex_drawing),
        ("06_chart", example_chart),
        ("07_color_palette", example_color_palette),
        ("08_arrows", example_arrows),
    ]
    
    print("Generating SVG examples...")
    print("-" * 50)
    
    for filename, func in examples:
        svg = func()
        filepath = os.path.join(output_dir, f"{filename}.svg")
        svg.save(filepath)
        print(f"✓ {filename}.svg")
    
    print("-" * 50)
    print(f"Generated {len(examples)} SVG files in {output_dir}/")
    print("\nYou can open these SVG files in any web browser or SVG viewer.")


if __name__ == "__main__":
    main()