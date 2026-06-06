"""
Test suite for SVG Utils module.

Run tests with: python -m pytest test_svg_utils.py -v
Or simply: python test_svg_utils.py
"""

import math
import os
import tempfile
import unittest
from svg_utils import (
    SVG, SVGElement,
    rect, circle, ellipse, line, polyline, polygon, text,
    Path, LinearGradient, RadialGradient,
    translate, rotate, scale, skewX, skewY,
    points_to_polygon_path, arc_path, circle_path,
    rounded_rect_path, star_path, regular_polygon_path,
    rgb_to_hex, hex_to_rgb, lighten, darken,
    PALETTE, group, image, link, marker, arrow_marker
)


class TestSVGElement(unittest.TestCase):
    """Test SVGElement class."""
    
    def test_basic_element_creation(self):
        """Test creating a basic SVG element."""
        elem = SVGElement("circle", cx=50, cy=50, r=25)
        xml = elem.to_xml()
        self.assertIn("<circle", xml)
        self.assertIn('cx="50"', xml)
        self.assertIn('cy="50"', xml)
        self.assertIn('r="25"', xml)
    
    def test_element_with_children(self):
        """Test element with children."""
        parent = SVGElement("g", id="group1")
        child = SVGElement("circle", cx=10, cy=10, r=5)
        parent.add_child(child)
        xml = parent.to_xml()
        self.assertIn("<g", xml)
        self.assertIn("</g>", xml)
        self.assertIn("<circle", xml)
    
    def test_element_with_text_content(self):
        """Test element with text content."""
        elem = SVGElement("text", x=10, y=20)
        elem.set_text("Hello World")
        xml = elem.to_xml()
        self.assertIn(">Hello World<", xml)
    
    def test_attribute_escaping(self):
        """Test that special characters are escaped in text."""
        elem = SVGElement("text")
        elem.set_text('<script>alert("xss")</script>')
        xml = elem.to_xml()
        self.assertIn("&lt;", xml)
        self.assertIn("&gt;", xml)
    
    def test_underscore_to_dash_conversion(self):
        """Test that underscores in attr names become dashes."""
        elem = SVGElement("rect", stroke_width=2, fill_opacity=0.5)
        xml = elem.to_xml()
        self.assertIn('stroke-width="2"', xml)
        self.assertIn('fill-opacity="0.5"', xml)


class TestSVG(unittest.TestCase):
    """Test SVG document class."""
    
    def test_svg_creation(self):
        """Test creating an SVG document."""
        svg = SVG(100, 100)
        xml = svg.to_xml()
        self.assertIn('<?xml version="1.0"', xml)
        self.assertIn('width="100"', xml)
        self.assertIn('height="100"', xml)
        self.assertIn('viewBox="0 0 100 100"', xml)
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', xml)
    
    def test_svg_with_custom_viewbox(self):
        """Test SVG with custom viewBox."""
        svg = SVG(200, 100, viewBox="0 0 200 100")
        xml = svg.to_xml()
        self.assertIn('viewBox="0 0 200 100"', xml)
    
    def test_svg_add_element(self):
        """Test adding elements to SVG."""
        svg = SVG(100, 100)
        svg.add(circle(50, 50, 25))
        xml = svg.to_xml()
        self.assertIn("<circle", xml)
    
    def test_svg_title_and_desc(self):
        """Test SVG title and description."""
        svg = SVG(100, 100)
        svg.set_title("Test SVG").set_desc("A test SVG document")
        xml = svg.to_xml()
        self.assertIn("<title>", xml)
        self.assertIn("Test SVG", xml)
        self.assertIn("<desc>", xml)
        self.assertIn("A test SVG document", xml)
    
    def test_svg_save(self):
        """Test saving SVG to file."""
        svg = SVG(50, 50)
        svg.add(rect(10, 10, 30, 30, fill="blue"))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
            filepath = f.name
        
        try:
            svg.save(filepath)
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r') as f:
                content = f.read()
            self.assertIn("<?xml", content)
            self.assertIn("<rect", content)
        finally:
            os.unlink(filepath)


class TestShapes(unittest.TestCase):
    """Test shape factory functions."""
    
    def test_rect(self):
        """Test rectangle creation."""
        r = rect(10, 20, 100, 50, fill="red", stroke="black", stroke_width=2)
        xml = r.to_xml()
        self.assertIn("<rect", xml)
        self.assertIn('x="10"', xml)
        self.assertIn('y="20"', xml)
        self.assertIn('width="100"', xml)
        self.assertIn('height="50"', xml)
        self.assertIn('fill="red"', xml)
    
    def test_rect_with_rounded_corners(self):
        """Test rectangle with rounded corners."""
        r = rect(0, 0, 100, 50, rx=10, ry=10)
        xml = r.to_xml()
        self.assertIn('rx="10"', xml)
        self.assertIn('ry="10"', xml)
    
    def test_circle(self):
        """Test circle creation."""
        c = circle(50, 50, 25, fill="blue")
        xml = c.to_xml()
        self.assertIn("<circle", xml)
        self.assertIn('cx="50"', xml)
        self.assertIn('cy="50"', xml)
        self.assertIn('r="25"', xml)
    
    def test_ellipse(self):
        """Test ellipse creation."""
        e = ellipse(50, 50, 30, 20, fill="green")
        xml = e.to_xml()
        self.assertIn("<ellipse", xml)
        self.assertIn('rx="30"', xml)
        self.assertIn('ry="20"', xml)
    
    def test_line(self):
        """Test line creation."""
        l = line(0, 0, 100, 100, stroke="black", stroke_width=2)
        xml = l.to_xml()
        self.assertIn("<line", xml)
        self.assertIn('x1="0"', xml)
        self.assertIn('y1="0"', xml)
        self.assertIn('x2="100"', xml)
        self.assertIn('y2="100"', xml)
    
    def test_polyline(self):
        """Test polyline creation."""
        points = [(0, 0), (50, 25), (100, 0), (150, 25)]
        p = polyline(points, stroke="red", fill="none")
        xml = p.to_xml()
        self.assertIn("<polyline", xml)
        self.assertIn('points="0,0 50,25 100,0 150,25"', xml)
    
    def test_polygon(self):
        """Test polygon creation."""
        points = [(50, 0), (100, 100), (0, 100)]
        p = polygon(points, fill="blue")
        xml = p.to_xml()
        self.assertIn("<polygon", xml)
        self.assertIn('points="50,0 100,100 0,100"', xml)
    
    def test_text(self):
        """Test text creation."""
        t = text(50, 50, "Hello SVG", font_size=24, fill="black")
        xml = t.to_xml()
        self.assertIn("<text", xml)
        self.assertIn('x="50"', xml)
        self.assertIn('y="50"', xml)
        self.assertIn('font-size="24"', xml)
        self.assertIn(">Hello SVG<", xml)


class TestPath(unittest.TestCase):
    """Test Path class."""
    
    def test_path_move_line(self):
        """Test path with move and line commands."""
        p = Path()
        p.M(10, 10).L(100, 10).L(100, 100).L(10, 100).Z()
        xml = p.build().to_xml()
        self.assertIn("<path", xml)
        self.assertIn('d="M 10 10 L 100 10 L 100 100 L 10 100 Z"', xml)
    
    def test_path_relative_commands(self):
        """Test path with relative commands."""
        p = Path()
        p.M(10, 10).l(90, 0).l(0, 90).l(-90, 0).z()
        xml = p.build().to_xml()
        self.assertIn("M 10 10", xml)
        self.assertIn("l 90 0", xml)
    
    def test_path_horizontal_vertical(self):
        """Test horizontal and vertical line commands."""
        p = Path()
        p.M(0, 0).H(100).V(50).H(0).Z()
        xml = p.build().to_xml()
        self.assertIn("H 100", xml)
        self.assertIn("V 50", xml)
    
    def test_path_quadratic_bezier(self):
        """Test quadratic bezier curve."""
        p = Path()
        p.M(0, 0).Q(50, -50, 100, 0)
        xml = p.build().to_xml()
        self.assertIn("Q 50 -50 100 0", xml)
    
    def test_path_cubic_bezier(self):
        """Test cubic bezier curve."""
        p = Path()
        p.M(0, 0).C(25, -50, 75, -50, 100, 0)
        xml = p.build().to_xml()
        self.assertIn("C 25 -50 75 -50 100 0", xml)
    
    def test_path_arc(self):
        """Test arc command."""
        p = Path(fill="none", stroke="black")
        p.M(50, 0).A(50, 50, 0, 1, 1, 50, 100)
        xml = p.build().to_xml()
        self.assertIn("A 50 50 0 1 1 50 100", xml)


class TestGradients(unittest.TestCase):
    """Test gradient classes."""
    
    def test_linear_gradient(self):
        """Test linear gradient creation."""
        grad = LinearGradient("grad1", x1="0%", y1="0%", x2="100%", y2="0%")
        grad.add_stop("0%", "#ff0000").add_stop("100%", "#0000ff")
        xml = grad.build().to_xml()
        self.assertIn("<linearGradient", xml)
        self.assertIn('id="grad1"', xml)
        self.assertIn("<stop", xml)
        self.assertIn('offset="0%"', xml)
        self.assertIn('stop-color="#ff0000"', xml)
    
    def test_radial_gradient(self):
        """Test radial gradient creation."""
        grad = RadialGradient("grad2", cx="50%", cy="50%", r="50%")
        grad.add_stop("0%", "white").add_stop("100%", "black")
        xml = grad.build().to_xml()
        self.assertIn("<radialGradient", xml)
        self.assertIn('id="grad2"', xml)
        self.assertIn('cx="50%"', xml)
    
    def test_gradient_with_opacity(self):
        """Test gradient stop with opacity."""
        grad = LinearGradient("grad3")
        grad.add_stop("0%", "#ff0000", opacity=0.5)
        xml = grad.build().to_xml()
        self.assertIn('stop-opacity="0.5"', xml)
    
    def test_gradient_in_svg(self):
        """Test gradient used in SVG."""
        svg = SVG(100, 100)
        grad = LinearGradient("myGrad")
        grad.add_stop("0%", "red").add_stop("100%", "blue")
        svg.add_def(grad.build())
        svg.add(circle(50, 50, 25, fill="url(#myGrad)"))
        xml = svg.to_xml()
        self.assertIn("<linearGradient", xml)
        self.assertIn("url(#myGrad)", xml)


class TestTransforms(unittest.TestCase):
    """Test transform utility functions."""
    
    def test_translate(self):
        """Test translate transform."""
        t = translate(10, 20)
        self.assertEqual(t, "translate(10, 20)")
    
    def test_rotate(self):
        """Test rotate transform."""
        t = rotate(45)
        self.assertEqual(t, "rotate(45)")
        
        t = rotate(45, 50, 50)
        self.assertEqual(t, "rotate(45, 50, 50)")
    
    def test_scale(self):
        """Test scale transform."""
        t = scale(2)
        self.assertEqual(t, "scale(2)")
        
        t = scale(2, 1.5)
        self.assertEqual(t, "scale(2, 1.5)")
    
    def test_skew(self):
        """Test skew transforms."""
        self.assertEqual(skewX(30), "skewX(30)")
        self.assertEqual(skewY(15), "skewY(15)")
    
    def test_transform_on_element(self):
        """Test applying transform to element."""
        c = circle(50, 50, 25)
        c.set_attr("transform", f"{translate(10, 10)} {rotate(45)}")
        xml = c.to_xml()
        self.assertIn('transform="translate(10, 10) rotate(45)"', xml)


class TestPathUtilities(unittest.TestCase):
    """Test path utility functions."""
    
    def test_points_to_polygon_path(self):
        """Test converting points to polygon path."""
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        path = points_to_polygon_path(points)
        xml = path.build().to_xml()
        self.assertIn("M 0 0", xml)
        self.assertIn("L 100 0", xml)
        self.assertIn("Z", xml)
    
    def test_points_to_polygon_path_empty(self):
        """Test that empty points raises error."""
        with self.assertRaises(ValueError):
            points_to_polygon_path([])
    
    def test_arc_path(self):
        """Test arc path creation."""
        path = arc_path(50, 50, 40, 0, 90)
        xml = path.build().to_xml()
        self.assertIn("M", xml)
        self.assertIn("A 40 40", xml)
    
    def test_circle_path(self):
        """Test circle as path."""
        path = circle_path(50, 50, 25)
        xml = path.build().to_xml()
        self.assertIn("A 25 25", xml)
        self.assertIn("Z", xml)
    
    def test_rounded_rect_path(self):
        """Test rounded rectangle path."""
        path = rounded_rect_path(10, 10, 80, 60, 10)
        xml = path.build().to_xml()
        self.assertIn("A 10 10", xml)
        self.assertIn("Z", xml)
    
    def test_star_path(self):
        """Test star path creation."""
        path = star_path(50, 50, 40, 20, 5)
        xml = path.build().to_xml()
        self.assertIn("M", xml)
        self.assertIn("Z", xml)
        
        # 5-pointed star should have 10 lines (5 outer + 5 inner)
        self.assertEqual(xml.count("L"), 10)
    
    def test_star_path_too_few_points(self):
        """Test that star with too few points raises error."""
        with self.assertRaises(ValueError):
            star_path(50, 50, 40, 20, 2)
    
    def test_regular_polygon_path(self):
        """Test regular polygon path."""
        path = regular_polygon_path(50, 50, 40, 6)
        xml = path.build().to_xml()
        self.assertIn("M", xml)
        self.assertIn("Z", xml)
        
        # Hexagon should have 6 lines
        self.assertEqual(xml.count("L"), 6)
    
    def test_regular_polygon_too_few_sides(self):
        """Test that polygon with too few sides raises error."""
        with self.assertRaises(ValueError):
            regular_polygon_path(50, 50, 40, 2)


class TestColorUtilities(unittest.TestCase):
    """Test color utility functions."""
    
    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        self.assertEqual(rgb_to_hex(255, 0, 0), "#ff0000")
        self.assertEqual(rgb_to_hex(0, 255, 0), "#00ff00")
        self.assertEqual(rgb_to_hex(0, 0, 255), "#0000ff")
        self.assertEqual(rgb_to_hex(255, 255, 255), "#ffffff")
        self.assertEqual(rgb_to_hex(0, 0, 0), "#000000")
    
    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        self.assertEqual(hex_to_rgb("#ff0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("#00ff00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000ff"), (0, 0, 255))
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
    
    def test_hex_to_rgb_short_form(self):
        """Test hex short form (#fff) conversion."""
        self.assertEqual(hex_to_rgb("#fff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#f00"), (255, 0, 0))
    
    def test_hex_to_rgb_without_hash(self):
        """Test hex without hash conversion."""
        self.assertEqual(hex_to_rgb("ff0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("fff"), (255, 255, 255))
    
    def test_lighten(self):
        """Test color lightening."""
        # Black should become lighter
        light = lighten("#000000", 0.5)
        r, g, b = hex_to_rgb(light)
        self.assertEqual(r, 127)
        self.assertEqual(g, 127)
        self.assertEqual(b, 127)
        
        # White should stay white
        light = lighten("#ffffff", 0.5)
        self.assertEqual(light, "#ffffff")
    
    def test_darken(self):
        """Test color darkening."""
        # White should become darker
        dark = darken("#ffffff", 0.5)
        r, g, b = hex_to_rgb(dark)
        self.assertEqual(r, 127)
        self.assertEqual(g, 127)
        self.assertEqual(b, 127)
        
        # Black should stay black
        dark = darken("#000000", 0.5)
        self.assertEqual(dark, "#000000")


class TestPalette(unittest.TestCase):
    """Test color palette."""
    
    def test_palette_exists(self):
        """Test that palettes exist."""
        self.assertIn("primary", PALETTE)
        self.assertIn("secondary", PALETTE)
        self.assertIn("accent", PALETTE)
        self.assertIn("pastel", PALETTE)
    
    def test_palette_colors_valid(self):
        """Test that all palette colors are valid hex."""
        import re
        hex_pattern = re.compile(r'^#[0-9a-f]{6}$')
        for palette_name, colors in PALETTE.items():
            for color in colors:
                self.assertTrue(hex_pattern.match(color),
                    f"Invalid color {color} in palette {palette_name}")


class TestGroup(unittest.TestCase):
    """Test group element."""
    
    def test_group_creation(self):
        """Test group creation."""
        g = group(id="myGroup", fill="red")
        xml = g.to_xml()
        self.assertIn("<g", xml)
        self.assertIn('id="myGroup"', xml)
        self.assertIn('fill="red"', xml)
    
    def test_group_with_children(self):
        """Test group with children."""
        g = group(id="shapes")
        g.add_child(circle(10, 10, 5))
        g.add_child(rect(20, 20, 10, 10))
        xml = g.to_xml()
        self.assertIn("<circle", xml)
        self.assertIn("<rect", xml)


class TestImageAndLink(unittest.TestCase):
    """Test image and link elements."""
    
    def test_image(self):
        """Test image element."""
        img = image("photo.jpg", 0, 0, 100, 100)
        xml = img.to_xml()
        self.assertIn("<image", xml)
        self.assertIn('href="photo.jpg"', xml)
        self.assertIn('width="100"', xml)
        self.assertIn('height="100"', xml)
    
    def test_link(self):
        """Test link element."""
        a = link("https://example.com", target="_blank")
        a.add_child(text(50, 50, "Click me"))
        xml = a.to_xml()
        self.assertIn("<a", xml)
        self.assertIn('href="https://example.com"', xml)
        self.assertIn("<text", xml)


class TestMarker(unittest.TestCase):
    """Test marker elements."""
    
    def test_marker(self):
        """Test marker element."""
        m = marker("arrow", 10, 5)
        xml = m.to_xml()
        self.assertIn("<marker", xml)
        self.assertIn('id="arrow"', xml)
        self.assertIn('refX="10"', xml)
        self.assertIn('refY="5"', xml)
        self.assertIn('orient="auto"', xml)
    
    def test_arrow_marker(self):
        """Test arrow marker creation."""
        a = arrow_marker("myArrow", size=10, fill="black")
        xml = a.to_xml()
        self.assertIn("<marker", xml)
        self.assertIn("<polygon", xml)
        self.assertIn('points="0,0 10,5.0 0,10"', xml)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete SVG generation."""
    
    def test_complete_svg_with_shapes(self):
        """Test creating a complete SVG with various shapes."""
        svg = SVG(200, 200)
        svg.set_title("Test SVG")
        
        # Add a rectangle background
        svg.add(rect(0, 0, 200, 200, fill="#f0f0f0"))
        
        # Add a circle
        svg.add(circle(100, 100, 50, fill="#3498db", stroke="#2980b9", stroke_width=2))
        
        # Add text
        svg.add(text(100, 110, "Hello", font_size=20, fill="white", text_anchor="middle"))
        
        xml = svg.to_xml()
        self.assertIn("<rect", xml)
        self.assertIn("<circle", xml)
        self.assertIn("<text", xml)
        self.assertIn("Hello", xml)
    
    def test_svg_with_gradient_fill(self):
        """Test SVG with gradient-filled shapes."""
        svg = SVG(100, 100)
        
        # Create gradient
        grad = LinearGradient("myGrad", x1="0%", y1="0%", x2="100%", y2="100%")
        grad.add_stop("0%", "#ff6b6b").add_stop("100%", "#4ecdc4")
        svg.add_def(grad.build())
        
        # Use gradient
        svg.add(rect(10, 10, 80, 80, fill="url(#myGrad)"))
        
        xml = svg.to_xml()
        self.assertIn("<linearGradient", xml)
        self.assertIn("url(#myGrad)", xml)
    
    def test_svg_with_star(self):
        """Test SVG with star shape."""
        svg = SVG(100, 100)
        path = star_path(50, 50, 40, 20, 5)
        path.fill = "#f1c40f"
        path.stroke = "#f39c12"
        svg.add(path.build())
        
        xml = svg.to_xml()
        self.assertIn("<path", xml)
        self.assertIn("M", xml)
        self.assertIn("Z", xml)
    
    def test_svg_with_transformed_group(self):
        """Test SVG with transformed group."""
        svg = SVG(100, 100)
        
        g = group(id="rotated", transform=rotate(45, 50, 50))
        g.add_child(rect(40, 40, 20, 20, fill="red"))
        svg.add(g)
        
        xml = svg.to_xml()
        self.assertIn('transform="rotate(45, 50, 50)"', xml)
    
    def test_svg_with_arrow_marker(self):
        """Test SVG with arrow marker on line."""
        svg = SVG(100, 100)
        
        # Add marker definition
        svg.add_def(arrow_marker("arrowhead", size=10, fill="black"))
        
        # Add line with marker
        arrow_line = line(10, 50, 90, 50, stroke="black", stroke_width=2)
        arrow_line.set_attr("marker_end", "url(#arrowhead)")
        svg.add(arrow_line)
        
        xml = svg.to_xml()
        self.assertIn("<marker", xml)
        self.assertIn('marker-end="url(#arrowhead)"', xml)


if __name__ == "__main__":
    unittest.main(verbosity=2)