"""
SVG Utils - Pure Python SVG Generator with Zero External Dependencies

A lightweight library for creating and manipulating SVG graphics programmatically.
Supports basic shapes, paths, text, gradients, and transformations.

Author: AllToolkit
Date: 2026-04-26
"""

import math
import re
from typing import Optional, Union, List, Dict, Any, Tuple
from xml.sax.saxutils import escape as xml_escape


class SVGElement:
    """Base class for all SVG elements."""
    
    def __init__(self, tag: str, **attrs):
        self.tag = tag
        self.attrs = attrs
        self.children: List['SVGElement'] = []
        self.text_content: str = ""
    
    def set_attr(self, name: str, value: Any) -> 'SVGElement':
        """Set an attribute on the element."""
        self.attrs[name] = value
        return self
    
    def add_child(self, child: 'SVGElement') -> 'SVGElement':
        """Add a child element."""
        self.children.append(child)
        return self
    
    def set_text(self, text: str) -> 'SVGElement':
        """Set text content."""
        self.text_content = xml_escape(str(text))
        return self
    
    def _format_attrs(self) -> str:
        """Format attributes as XML string."""
        if not self.attrs:
            return ""
        parts = []
        for key, value in self.attrs.items():
            key_xml = key.replace('_', '-')
            if value is not None:
                parts.append(f'{key_xml}="{value}"')
        return " " + " ".join(parts) if parts else ""
    
    def to_xml(self, indent: int = 0) -> str:
        """Convert element to XML string."""
        spaces = "  " * indent
        attrs_str = self._format_attrs()
        
        if self.children:
            result = f"{spaces}<{self.tag}{attrs_str}>\n"
            for child in self.children:
                result += child.to_xml(indent + 1) + "\n"
            result += f"{spaces}</{self.tag}>"
            return result
        elif self.text_content:
            return f"{spaces}<{self.tag}{attrs_str}>{self.text_content}</{self.tag}>"
        else:
            return f"{spaces}<{self.tag}{attrs_str} />"


class SVG:
    """SVG Document class for creating SVG graphics."""
    
    def __init__(self, width: int = 100, height: int = 100, viewBox: Optional[str] = None):
        """
        Initialize an SVG document.
        
        Args:
            width: Width in pixels
            height: Height in pixels
            viewBox: Optional viewBox string (e.g., "0 0 100 100")
        """
        self.width = width
        self.height = height
        self.viewBox = viewBox or f"0 0 {width} {height}"
        self.root = SVGElement("svg")
        self.root.set_attr("width", width)
        self.root.set_attr("height", height)
        self.root.set_attr("viewBox", self.viewBox)
        self.root.set_attr("xmlns", "http://www.w3.org/2000/svg")
        
        # Definitions (gradients, patterns, etc.)
        self.defs: SVGElement = SVGElement("defs")
        self.has_defs = False
    
    def add_def(self, element: SVGElement) -> 'SVG':
        """Add a definition element (gradient, pattern, etc.)."""
        self.defs.add_child(element)
        self.has_defs = True
        return self
    
    def add(self, element: SVGElement) -> 'SVG':
        """Add an element to the SVG."""
        self.root.add_child(element)
        return self
    
    def set_title(self, title: str) -> 'SVG':
        """Set the SVG title."""
        title_elem = SVGElement("title")
        title_elem.set_text(title)
        self.root.add_child(title_elem)
        return self
    
    def set_desc(self, desc: str) -> 'SVG':
        """Set the SVG description."""
        desc_elem = SVGElement("desc")
        desc_elem.set_text(desc)
        self.root.add_child(desc_elem)
        return self
    
    def to_xml(self) -> str:
        """Convert SVG to XML string."""
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        if self.has_defs:
            # Insert defs as first child after title/desc
            children = self.root.children
            self.root.children = []
            for child in children:
                if child.tag in ("title", "desc"):
                    self.root.children.append(child)
                else:
                    if self.defs not in self.root.children:
                        self.root.children.append(self.defs)
                    self.root.children.append(child)
            if self.defs not in self.root.children:
                self.root.children.insert(0, self.defs)
        
        xml += self.root.to_xml()
        return xml
    
    def save(self, filepath: str) -> None:
        """Save SVG to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_xml())
    
    def __str__(self) -> str:
        return self.to_xml()


# =============================================================================
# Shape Factory Functions
# =============================================================================

def rect(x: int, y: int, width: int, height: int, 
         fill: str = "black", stroke: str = "none", 
         stroke_width: int = 1, rx: int = 0, ry: int = 0,
         **attrs) -> SVGElement:
    """
    Create a rectangle element.
    
    Args:
        x, y: Position coordinates
        width, height: Dimensions
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        rx, ry: Corner radius for rounded rectangles
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the rectangle
    """
    elem = SVGElement("rect", **attrs)
    elem.set_attr("x", x).set_attr("y", y)
    elem.set_attr("width", width).set_attr("height", height)
    elem.set_attr("fill", fill)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    if rx:
        elem.set_attr("rx", rx)
    if ry:
        elem.set_attr("ry", ry)
    return elem


def circle(cx: int, cy: int, r: int,
           fill: str = "black", stroke: str = "none",
           stroke_width: int = 1, **attrs) -> SVGElement:
    """
    Create a circle element.
    
    Args:
        cx, cy: Center coordinates
        r: Radius
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the circle
    """
    elem = SVGElement("circle", **attrs)
    elem.set_attr("cx", cx).set_attr("cy", cy).set_attr("r", r)
    elem.set_attr("fill", fill)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    return elem


def ellipse(cx: int, cy: int, rx: int, ry: int,
            fill: str = "black", stroke: str = "none",
            stroke_width: int = 1, **attrs) -> SVGElement:
    """
    Create an ellipse element.
    
    Args:
        cx, cy: Center coordinates
        rx, ry: X and Y radii
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the ellipse
    """
    elem = SVGElement("ellipse", **attrs)
    elem.set_attr("cx", cx).set_attr("cy", cy)
    elem.set_attr("rx", rx).set_attr("ry", ry)
    elem.set_attr("fill", fill)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    return elem


def line(x1: int, y1: int, x2: int, y2: int,
         stroke: str = "black", stroke_width: int = 1, **attrs) -> SVGElement:
    """
    Create a line element.
    
    Args:
        x1, y1: Start coordinates
        x2, y2: End coordinates
        stroke: Stroke color
        stroke_width: Stroke width
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the line
    """
    elem = SVGElement("line", **attrs)
    elem.set_attr("x1", x1).set_attr("y1", y1)
    elem.set_attr("x2", x2).set_attr("y2", y2)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    return elem


def polyline(points: List[Tuple[int, int]],
             fill: str = "none", stroke: str = "black",
             stroke_width: int = 1, **attrs) -> SVGElement:
    """
    Create a polyline element (connected line segments).
    
    Args:
        points: List of (x, y) coordinate tuples
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the polyline
    """
    elem = SVGElement("polyline", **attrs)
    points_str = " ".join(f"{x},{y}" for x, y in points)
    elem.set_attr("points", points_str)
    elem.set_attr("fill", fill)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    return elem


def polygon(points: List[Tuple[int, int]],
            fill: str = "black", stroke: str = "none",
            stroke_width: int = 1, **attrs) -> SVGElement:
    """
    Create a polygon element (closed shape).
    
    Args:
        points: List of (x, y) coordinate tuples
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the polygon
    """
    elem = SVGElement("polygon", **attrs)
    points_str = " ".join(f"{x},{y}" for x, y in points)
    elem.set_attr("points", points_str)
    elem.set_attr("fill", fill)
    elem.set_attr("stroke", stroke)
    elem.set_attr("stroke_width", stroke_width)
    return elem


def text(x: int, y: int, content: str,
         font_size: int = 16, font_family: str = "Arial",
         fill: str = "black", text_anchor: str = "start",
         **attrs) -> SVGElement:
    """
    Create a text element.
    
    Args:
        x, y: Position coordinates
        content: Text content
        font_size: Font size in pixels
        font_family: Font family name
        fill: Text color
        text_anchor: Text alignment (start, middle, end)
        **attrs: Additional SVG attributes
    
    Returns:
        SVGElement representing the text
    """
    elem = SVGElement("text", **attrs)
    elem.set_attr("x", x).set_attr("y", y)
    elem.set_attr("font_size", font_size)
    elem.set_attr("font_family", font_family)
    elem.set_attr("fill", fill)
    elem.set_attr("text_anchor", text_anchor)
    elem.set_text(content)
    return elem


# =============================================================================
# Path Commands
# =============================================================================

class Path:
    """Builder for SVG path elements using command chaining."""
    
    def __init__(self, fill: str = "black", stroke: str = "none", 
                 stroke_width: int = 1, **attrs):
        self.commands: List[str] = []
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.attrs = attrs
    
    def M(self, x: float, y: float) -> 'Path':
        """Move to (absolute)."""
        self.commands.append(f"M {x} {y}")
        return self
    
    def m(self, dx: float, dy: float) -> 'Path':
        """Move to (relative)."""
        self.commands.append(f"m {dx} {dy}")
        return self
    
    def L(self, x: float, y: float) -> 'Path':
        """Line to (absolute)."""
        self.commands.append(f"L {x} {y}")
        return self
    
    def l(self, dx: float, dy: float) -> 'Path':
        """Line to (relative)."""
        self.commands.append(f"l {dx} {dy}")
        return self
    
    def H(self, x: float) -> 'Path':
        """Horizontal line to (absolute)."""
        self.commands.append(f"H {x}")
        return self
    
    def h(self, dx: float) -> 'Path':
        """Horizontal line to (relative)."""
        self.commands.append(f"h {dx}")
        return self
    
    def V(self, y: float) -> 'Path':
        """Vertical line to (absolute)."""
        self.commands.append(f"V {y}")
        return self
    
    def v(self, dy: float) -> 'Path':
        """Vertical line to (relative)."""
        self.commands.append(f"v {dy}")
        return self
    
    def C(self, x1: float, y1: float, x2: float, y2: float, 
          x: float, y: float) -> 'Path':
        """Cubic Bezier curve (absolute)."""
        self.commands.append(f"C {x1} {y1} {x2} {y2} {x} {y}")
        return self
    
    def c(self, dx1: float, dy1: float, dx2: float, dy2: float,
          dx: float, dy: float) -> 'Path':
        """Cubic Bezier curve (relative)."""
        self.commands.append(f"c {dx1} {dy1} {dx2} {dy2} {dx} {dy}")
        return self
    
    def Q(self, x1: float, y1: float, x: float, y: float) -> 'Path':
        """Quadratic Bezier curve (absolute)."""
        self.commands.append(f"Q {x1} {y1} {x} {y}")
        return self
    
    def q(self, dx1: float, dy1: float, dx: float, dy: float) -> 'Path':
        """Quadratic Bezier curve (relative)."""
        self.commands.append(f"q {dx1} {dy1} {dx} {dy}")
        return self
    
    def A(self, rx: float, ry: float, rotation: float,
          large_arc: int, sweep: int, x: float, y: float) -> 'Path':
        """Arc (absolute)."""
        self.commands.append(f"A {rx} {ry} {rotation} {large_arc} {sweep} {x} {y}")
        return self
    
    def a(self, rx: float, ry: float, rotation: float,
          large_arc: int, sweep: int, dx: float, dy: float) -> 'Path':
        """Arc (relative)."""
        self.commands.append(f"a {rx} {ry} {rotation} {large_arc} {sweep} {dx} {dy}")
        return self
    
    def Z(self) -> 'Path':
        """Close path."""
        self.commands.append("Z")
        return self
    
    def z(self) -> 'Path':
        """Close path (lowercase alias)."""
        self.commands.append("z")
        return self
    
    def build(self) -> SVGElement:
        """Build the path element."""
        elem = SVGElement("path", **self.attrs)
        elem.set_attr("d", " ".join(self.commands))
        elem.set_attr("fill", self.fill)
        elem.set_attr("stroke", self.stroke)
        elem.set_attr("stroke_width", self.stroke_width)
        return elem


# =============================================================================
# Gradient Support
# =============================================================================

class LinearGradient:
    """Linear gradient definition."""
    
    def __init__(self, id: str, x1: str = "0%", y1: str = "0%",
                 x2: str = "100%", y2: str = "0%"):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stops: List[Tuple[str, str, Optional[float]]] = []
    
    def add_stop(self, offset: str, color: str, 
                 opacity: Optional[float] = None) -> 'LinearGradient':
        """Add a gradient stop."""
        self.stops.append((offset, color, opacity))
        return self
    
    def build(self) -> SVGElement:
        """Build the gradient element."""
        grad = SVGElement("linearGradient")
        grad.set_attr("id", self.id)
        grad.set_attr("x1", self.x1).set_attr("y1", self.y1)
        grad.set_attr("x2", self.x2).set_attr("y2", self.y2)
        
        for offset, color, opacity in self.stops:
            stop = SVGElement("stop")
            stop.set_attr("offset", offset).set_attr("stop_color", color)
            if opacity is not None:
                stop.set_attr("stop_opacity", opacity)
            grad.add_child(stop)
        
        return grad


class RadialGradient:
    """Radial gradient definition."""
    
    def __init__(self, id: str, cx: str = "50%", cy: str = "50%",
                 r: str = "50%"):
        self.id = id
        self.cx = cx
        self.cy = cy
        self.r = r
        self.stops: List[Tuple[str, str, Optional[float]]] = []
    
    def add_stop(self, offset: str, color: str,
                 opacity: Optional[float] = None) -> 'RadialGradient':
        """Add a gradient stop."""
        self.stops.append((offset, color, opacity))
        return self
    
    def build(self) -> SVGElement:
        """Build the gradient element."""
        grad = SVGElement("radialGradient")
        grad.set_attr("id", self.id)
        grad.set_attr("cx", self.cx).set_attr("cy", self.cy).set_attr("r", self.r)
        
        for offset, color, opacity in self.stops:
            stop = SVGElement("stop")
            stop.set_attr("offset", offset).set_attr("stop_color", color)
            if opacity is not None:
                stop.set_attr("stop_opacity", opacity)
            grad.add_child(stop)
        
        return grad


# =============================================================================
# Transform Support
# =============================================================================

def translate(x: float, y: float = 0) -> str:
    """Create translate transform string."""
    return f"translate({x}, {y})"


def rotate(angle: float, cx: Optional[float] = None, 
           cy: Optional[float] = None) -> str:
    """Create rotate transform string."""
    if cx is not None and cy is not None:
        return f"rotate({angle}, {cx}, {cy})"
    return f"rotate({angle})"


def scale(sx: float, sy: Optional[float] = None) -> str:
    """Create scale transform string."""
    if sy is not None:
        return f"scale({sx}, {sy})"
    return f"scale({sx})"


def skewX(angle: float) -> str:
    """Create skewX transform string."""
    return f"skewX({angle})"


def skewY(angle: float) -> str:
    """Create skewY transform string."""
    return f"skewY({angle})"


# =============================================================================
# Utility Functions
# =============================================================================

def points_to_polygon_path(points: List[Tuple[float, float]]) -> Path:
    """Convert a list of points to a closed polygon path."""
    if not points:
        raise ValueError("Points list cannot be empty")
    
    path = Path()
    path.M(points[0][0], points[0][1])
    for x, y in points[1:]:
        path.L(x, y)
    path.Z()
    return path


def arc_path(cx: float, cy: float, r: float, 
             start_angle: float, end_angle: float) -> Path:
    """
    Create an arc path.
    
    Args:
        cx, cy: Center coordinates
        r: Radius
        start_angle: Start angle in degrees
        end_angle: End angle in degrees
    
    Returns:
        Path representing the arc
    """
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    x1 = cx + r * math.cos(start_rad)
    y1 = cy + r * math.sin(start_rad)
    x2 = cx + r * math.cos(end_rad)
    y2 = cy + r * math.sin(end_rad)
    
    angle_diff = end_angle - start_angle
    large_arc = 1 if abs(angle_diff) > 180 else 0
    sweep = 1 if angle_diff > 0 else 0
    
    path = Path(fill="none", stroke="black")
    path.M(x1, y1)
    path.A(r, r, 0, large_arc, sweep, x2, y2)
    return path


def circle_path(cx: float, cy: float, r: float) -> Path:
    """Create a circle as a path (two arcs)."""
    path = Path()
    path.M(cx + r, cy)
    path.A(r, r, 0, 1, 1, cx - r, cy)
    path.A(r, r, 0, 1, 1, cx + r, cy)
    path.Z()
    return path


def rounded_rect_path(x: float, y: float, width: float, height: float,
                     rx: float, ry: Optional[float] = None) -> Path:
    """Create a rounded rectangle as a path."""
    ry = ry if ry is not None else rx
    
    path = Path()
    path.M(x + rx, y)
    path.H(x + width - rx)
    path.A(rx, ry, 0, 0, 1, x + width, y + ry)
    path.V(y + height - ry)
    path.A(rx, ry, 0, 0, 1, x + width - rx, y + height)
    path.H(x + rx)
    path.A(rx, ry, 0, 0, 1, x, y + height - ry)
    path.V(y + ry)
    path.A(rx, ry, 0, 0, 1, x + rx, y)
    path.Z()
    return path


def star_path(cx: float, cy: float, outer_r: float, inner_r: float,
              points: int = 5) -> Path:
    """Create a star shape as a path."""
    if points < 3:
        raise ValueError("Star must have at least 3 points")
    
    path = Path()
    angle_step = math.pi / points
    
    # Start at top
    start_x = cx
    start_y = cy - outer_r
    path.M(start_x, start_y)
    
    for i in range(points * 2):
        angle = i * angle_step - math.pi / 2
        r = inner_r if i % 2 == 1 else outer_r
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        path.L(x, y)
    
    path.Z()
    return path


def regular_polygon_path(cx: float, cy: float, r: float, sides: int) -> Path:
    """Create a regular polygon as a path."""
    if sides < 3:
        raise ValueError("Polygon must have at least 3 sides")
    
    path = Path()
    angle_step = 2 * math.pi / sides
    
    # Start at top
    start_angle = -math.pi / 2
    start_x = cx + r * math.cos(start_angle)
    start_y = cy + r * math.sin(start_angle)
    path.M(start_x, start_y)
    
    for i in range(1, sides + 1):
        angle = start_angle + i * angle_step
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        path.L(x, y)
    
    path.Z()
    return path


# =============================================================================
# Color Utilities
# =============================================================================

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex color string."""
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def lighten(hex_color: str, amount: float = 0.2) -> str:
    """Lighten a hex color by mixing with white."""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return rgb_to_hex(min(255, r), min(255, g), min(255, b))


def darken(hex_color: str, amount: float = 0.2) -> str:
    """Darken a hex color by mixing with black."""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r * (1 - amount))
    g = int(g * (1 - amount))
    b = int(b * (1 - amount))
    return rgb_to_hex(max(0, r), max(0, g), max(0, b))


# =============================================================================
# Pre-defined Color Palettes
# =============================================================================

PALETTE = {
    "primary": ["#3498db", "#2980b9", "#1abc9c"],
    "secondary": ["#2ecc71", "#27ae60", "#16a085"],
    "accent": ["#e74c3c", "#c0392b", "#e67e22"],
    "neutral": ["#34495e", "#7f8c8d", "#95a5a6"],
    "pastel": ["#a8e6cf", "#dcedc1", "#ffd3b6", "#ffaaa5", "#ff8b94"],
    "vibrant": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7"],
    "grayscale": ["#1a1a1a", "#4d4d4d", "#808080", "#b3b3b3", "#e6e6e6"],
}


# =============================================================================
# Group Support
# =============================================================================

def group(**attrs) -> SVGElement:
    """Create a group element for organizing elements."""
    return SVGElement("g", **attrs)


# =============================================================================
# Image and Link Support
# =============================================================================

def image(href: str, x: int, y: int, width: int, height: int,
          **attrs) -> SVGElement:
    """Create an image element."""
    elem = SVGElement("image", **attrs)
    elem.set_attr("href", href)
    elem.set_attr("x", x).set_attr("y", y)
    elem.set_attr("width", width).set_attr("height", height)
    return elem


def link(url: str, **attrs) -> SVGElement:
    """Create a link element (wraps other elements)."""
    elem = SVGElement("a", **attrs)
    elem.set_attr("href", url)
    elem.set_attr("target", attrs.get("target", "_blank"))
    return elem


# =============================================================================
# Marker Support (for arrows, etc.)
# =============================================================================

def marker(id: str, refX: float, refY: float, 
           markerWidth: float = 10, markerHeight: float = 10) -> SVGElement:
    """Create a marker definition element."""
    elem = SVGElement("marker")
    elem.set_attr("id", id)
    elem.set_attr("refX", refX).set_attr("refY", refY)
    elem.set_attr("markerWidth", markerWidth)
    elem.set_attr("markerHeight", markerHeight)
    elem.set_attr("orient", "auto")
    return elem


def arrow_marker(id: str = "arrow", size: int = 10, 
                 fill: str = "black") -> SVGElement:
    """Create a standard arrow marker."""
    m = marker(id, size, size / 2, size, size)
    arrow = polygon([(0, 0), (size, size / 2), (0, size)], fill=fill)
    m.add_child(arrow)
    return m