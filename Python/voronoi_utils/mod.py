"""
Voronoi Diagram Utilities - Zero External Dependencies

A comprehensive Voronoi diagram library for computational geometry applications.
Uses a direct geometric approach for robust computation.

Core Features:
- Voronoi diagram computation (direct geometric approach)
- Delaunay triangulation conversion
- Nearest neighbor queries
- Region/polygon extraction
- Distance calculations
- Bounding box clipping
- Relaxation (Lloyd's algorithm)
- Visualization helpers (ASCII/SVG output)
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any


class Point:
    """2D point representation."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Point') -> float:
        """Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def midpoint(self, other: 'Point') -> 'Point':
        """Midpoint between two points."""
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def __repr__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"
    
    def __eq__(self, other: 'Point') -> bool:
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10
    
    def __hash__(self) -> int:
        return hash((round(self.x, 6), round(self.y, 6)))
    
    def tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class Edge:
    """Edge between two points."""
    
    def __init__(self, start: Optional[Point], end: Optional[Point],
                 left_site: Optional[Point] = None, right_site: Optional[Point] = None):
        self.start = start
        self.end = end
        self.left_site = left_site
        self.right_site = right_site
    
    def is_finite(self) -> bool:
        """Check if edge has finite endpoints."""
        return self.start is not None and self.end is not None
    
    def length(self) -> float:
        """Get edge length if finite."""
        if self.is_finite():
            return self.start.distance_to(self.end)
        return float('inf')
    
    def __repr__(self) -> str:
        return f"Edge({self.start} -> {self.end})"


class VoronoiCell:
    """A Voronoi cell (region) for a single site."""
    
    def __init__(self, site: Point):
        self.site = site
        self.vertices: List[Point] = []
        self.edges: List[Edge] = []
        self.is_closed: bool = False
    
    def add_vertex(self, vertex: Point) -> None:
        """Add a vertex to the cell."""
        # Avoid duplicates
        for v in self.vertices:
            if abs(v.x - vertex.x) < 1e-10 and abs(v.y - vertex.y) < 1e-10:
                return
        self.vertices.append(vertex)
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the cell."""
        self.edges.append(edge)
    
    def area(self) -> float:
        """Calculate cell area using Shoelace formula."""
        if len(self.vertices) < 3:
            return 0.0
        
        # Order vertices by angle from centroid
        ordered = self._order_vertices()
        
        n = len(ordered)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += ordered[i].x * ordered[j].y
            area -= ordered[j].x * ordered[i].y
        return abs(area) / 2.0
    
    def centroid(self) -> Point:
        """Calculate centroid of the cell."""
        if len(self.vertices) < 1:
            return self.site
        
        cx, cy = 0.0, 0.0
        for v in self.vertices:
            cx += v.x
            cy += v.y
        return Point(cx / len(self.vertices), cy / len(self.vertices))
    
    def contains_point(self, p: Point) -> bool:
        """Check if a point is inside the cell using ray casting."""
        if len(self.vertices) < 3:
            return False
        
        ordered = self._order_vertices()
        n = len(ordered)
        inside = False
        
        for i in range(n):
            j = (i + 1) % n
            vi, vj = ordered[i], ordered[j]
            
            if ((vi.y > p.y) != (vj.y > p.y) and
                p.x < (vj.x - vi.x) * (p.y - vi.y) / (vj.y - vi.y + 1e-10) + vi.x):
                inside = not inside
        
        return inside
    
    def _order_vertices(self) -> List[Point]:
        """Order vertices by angle from centroid."""
        if len(self.vertices) < 3:
            return self.vertices
        
        centroid = self.centroid()
        
        def angle_from_center(p: Point) -> float:
            return math.atan2(p.y - centroid.y, p.x - centroid.x)
        
        return sorted(self.vertices, key=angle_from_center)


class VoronoiDiagram:
    """
    Voronoi Diagram computed using direct geometric approach.
    
    For each pair of sites, computes the perpendicular bisector.
    Then clips all bisectors to find cell boundaries.
    """
    
    def __init__(self, points: List[Point], bbox: Optional[Tuple[float, float, float, float]] = None):
        """
        Initialize and compute Voronoi diagram.
        
        Args:
            points: List of generator points (sites)
            bbox: Bounding box (xmin, ymin, xmax, ymax) for clipping
        """
        self.sites: List[Point] = points[:]
        self.vertices: List[Point] = []
        self.edges: List[Edge] = []
        self.cells: Dict[Point, VoronoiCell] = {}
        self.bbox = bbox
        
        if len(points) >= 2:
            self._compute()
        elif len(points) == 1:
            # Single point: the whole bbox is its cell
            self.cells[points[0]] = VoronoiCell(points[0])
            if bbox:
                xmin, ymin, xmax, ymax = bbox
                self.cells[points[0]].vertices = [
                    Point(xmin, ymin), Point(xmax, ymin),
                    Point(xmax, ymax), Point(xmin, ymax)
                ]
    
    def _compute(self) -> None:
        """Compute Voronoi diagram using direct geometric approach."""
        if not self.bbox:
            # Calculate reasonable bbox from sites
            xs = [p.x for p in self.sites]
            ys = [p.y for p in self.sites]
            margin = max(max(xs) - min(xs), max(ys) - min(ys)) * 0.5 + 1
            self.bbox = (
                min(xs) - margin, min(ys) - margin,
                max(xs) + margin, max(ys) + margin
            )
        
        xmin, ymin, xmax, ymax = self.bbox
        
        # For each site, compute its cell
        for site in self.sites:
            cell = self._compute_cell(site, xmin, ymin, xmax, ymax)
            self.cells[site] = cell
            
            # Add vertices and edges to global lists
            for v in cell.vertices:
                self.vertices.append(v)
            for e in cell.edges:
                self.edges.append(e)
    
    def _compute_cell(self, site: Point, xmin: float, ymin: float, 
                       xmax: float, ymax: float) -> VoronoiCell:
        """Compute Voronoi cell for a single site."""
        cell = VoronoiCell(site)
        
        # Start with the bounding box as the initial region
        # Then clip it by each bisector with other sites
        initial_polygon = [
            Point(xmin, ymin), Point(xmax, ymin),
            Point(xmax, ymax), Point(xmin, ymax)
        ]
        
        # Clip by each other site's bisector
        for other in self.sites:
            if other == site:
                continue
            
            # Compute perpendicular bisector between site and other
            mid = site.midpoint(other)
            
            # Direction vector from site to other
            dx = other.x - site.x
            dy = other.y - site.y
            
            # The bisector is perpendicular to this direction
            # and passes through the midpoint
            # Points on the bisector satisfy: (p - mid) dot (dx, dy) = 0
            # Which means: (p - mid) is perpendicular to (dx, dy)
            # So the bisector direction is (-dy, dx) or (dy, -dx)
            
            # Clip polygon to keep points closer to site than other
            initial_polygon = self._clip_polygon_by_bisector(
                initial_polygon, site, other, mid, dx, dy
            )
            
            if len(initial_polygon) < 3:
                break
        
        # Final polygon is the cell
        cell.vertices = initial_polygon
        cell.is_closed = len(initial_polygon) >= 3
        
        # Create edges from vertices
        if len(initial_polygon) >= 2:
            for i in range(len(initial_polygon)):
                j = (i + 1) % len(initial_polygon)
                edge = Edge(initial_polygon[i], initial_polygon[j], site, None)
                cell.edges.append(edge)
        
        return cell
    
    def _clip_polygon_by_bisector(self, polygon: List[Point], 
                                    site: Point, other: Point,
                                    mid: Point, dx: float, dy: float) -> List[Point]:
        """
        Clip polygon by the perpendicular bisector between site and other.
        Keep only points that are closer to site than other.
        """
        if len(polygon) < 3:
            return polygon
        
        result = []
        n = len(polygon)
        
        for i in range(n):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % n]
            
            # Determine which side each point is on
            # Side is determined by comparing distances to site and other
            d1_site = p1.distance_to(site)
            d1_other = p1.distance_to(other)
            d2_site = p2.distance_to(site)
            d2_other = p2.distance_to(other)
            
            # Use small epsilon for boundary cases
            eps = 1e-10
            
            side1 = d1_site < d1_other + eps  # True if closer to site
            side2 = d2_site < d2_other + eps
            
            if side1:
                # p1 is inside (closer to site)
                result.append(p1)
            
            if side1 != side2:
                # Edge crosses the bisector - find intersection point
                intersection = self._find_bisector_intersection(p1, p2, site, other)
                if intersection:
                    result.append(intersection)
        
        return result
    
    def _find_bisector_intersection(self, p1: Point, p2: Point,
                                      site: Point, other: Point) -> Optional[Point]:
        """Find intersection of edge p1-p2 with perpendicular bisector."""
        # The bisector is the set of points equidistant to site and other
        # |p - site|^2 = |p - other|^2
        # p.x^2 - 2*p.x*site.x + site.x^2 + p.y^2 - 2*p.y*site.y + site.y^2
        # = p.x^2 - 2*p.x*other.x + other.x^2 + p.y^2 - 2*p.y*other.y + other.y^2
        # Simplifying: -2*p.x*site.x + site.x^2 - 2*p.y*site.y + site.y^2
        #             = -2*p.x*other.x + other.x^2 - 2*p.y*other.y + other.y^2
        # 2*p.x*(other.x - site.x) + 2*p.y*(other.y - site.y) 
        # = other.x^2 + other.y^2 - site.x^2 - site.y^2
        
        # Let dx = other.x - site.x, dy = other.y - site.y
        # Let c = other.x^2 + other.y^2 - site.x^2 - site.y^2
        # Bisector equation: 2*dx*p.x + 2*dy*p.y = c
        
        dx = other.x - site.x
        dy = other.y - site.y
        c = other.x**2 + other.y**2 - site.x**2 - site.y**2
        
        if abs(dx) < 1e-10 and abs(dy) < 1e-10:
            return None  # Degenerate case
        
        # Edge p1-p2: param eq p = p1 + t*(p2 - p1)
        # p.x = p1.x + t*(p2.x - p1.x)
        # p.y = p1.y + t*(p2.y - p1.y)
        
        # Substitute into bisector equation:
        # 2*dx*(p1.x + t*(p2.x - p1.x)) + 2*dy*(p1.y + t*(p2.y - p1.y)) = c
        # 2*dx*p1.x + 2*dy*p1.y + t*(2*dx*(p2.x - p1.x) + 2*dy*(p2.y - p1.y)) = c
        
        A = 2 * dx * (p2.x - p1.x) + 2 * dy * (p2.y - p1.y)
        B = 2 * dx * p1.x + 2 * dy * p1.y
        
        if abs(A) < 1e-10:
            # Edge is parallel to bisector (or degenerate)
            return None
        
        t = (c - B) / A
        
        if t < -1e-10 or t > 1 + 1e-10:
            # Intersection is outside the edge segment
            return None
        
        # Clamp t to [0, 1]
        t = max(0.0, min(1.0, t))
        
        intersection_x = p1.x + t * (p2.x - p1.x)
        intersection_y = p1.y + t * (p2.y - p1.y)
        
        return Point(intersection_x, intersection_y)
    
    def find_nearest_site(self, point: Point) -> Optional[Point]:
        """Find the nearest site (generator) to a given point."""
        if not self.sites:
            return None
        
        nearest = None
        min_dist = float('inf')
        
        for site in self.sites:
            dist = point.distance_to(site)
            if dist < min_dist:
                min_dist = dist
                nearest = site
        
        return nearest
    
    def find_cell(self, point: Point) -> Optional[VoronoiCell]:
        """Find the Voronoi cell containing a given point."""
        nearest_site = self.find_nearest_site(point)
        if nearest_site:
            return self.cells.get(nearest_site)
        return None
    
    def get_delaunay_neighbors(self, site: Point) -> List[Point]:
        """Get Delaunay triangulation neighbors for a site."""
        neighbors = []
        
        # Find sites whose cells share a boundary with this site's cell
        my_cell = self.cells.get(site)
        if not my_cell:
            return neighbors
        
        # Check which other sites' cells touch our cell's edges
        my_vertices = set()
        for v in my_cell.vertices:
            my_vertices.add((round(v.x, 6), round(v.y, 6)))
        
        for other_site, other_cell in self.cells.items():
            if other_site == site:
                continue
            
            # Check for shared vertices (boundary touching)
            other_vertices = set()
            for v in other_cell.vertices:
                other_vertices.add((round(v.x, 6), round(v.y, 6)))
            
            # If they share at least 2 vertices, they're neighbors
            shared = my_vertices.intersection(other_vertices)
            if len(shared) >= 1:
                neighbors.append(other_site)
        
        return neighbors
    
    def relax(self, iterations: int = 1) -> 'VoronoiDiagram':
        """
        Apply Lloyd's relaxation algorithm.
        
        Moves each site to the centroid of its Voronoi cell.
        This results in more evenly distributed cells.
        
        Args:
            iterations: Number of relaxation iterations
        
        Returns:
            New VoronoiDiagram with relaxed sites
        """
        new_sites = []
        
        for site in self.sites:
            cell = self.cells.get(site)
            if cell and len(cell.vertices) >= 1:
                centroid = cell.centroid()
                # Keep within bbox if specified
                if self.bbox:
                    xmin, ymin, xmax, ymax = self.bbox
                    centroid = Point(
                        max(xmin, min(xmax, centroid.x)),
                        max(ymin, min(ymax, centroid.y))
                    )
                new_sites.append(centroid)
            else:
                new_sites.append(site)
        
        # Recompute diagram
        result = VoronoiDiagram(new_sites, self.bbox)
        
        if iterations > 1:
            return result.relax(iterations - 1)
        
        return result
    
    def to_ascii(self, width: int = 40, height: int = 20) -> str:
        """Generate ASCII art representation of the diagram."""
        if not self.bbox:
            return ""
        
        xmin, ymin, xmax, ymax = self.bbox
        
        # Create grid
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Mark sites
        for site in self.sites:
            sx = int((site.x - xmin) / (xmax - xmin + 1e-10) * (width - 1))
            sy = int((site.y - ymin) / (ymax - ymin + 1e-10) * (height - 1))
            sx = max(0, min(width - 1, sx))
            sy = max(0, min(height - 1, sy))
            grid[sy][sx] = '+'
        
        # Draw edges
        for site, cell in self.cells.items():
            for edge in cell.edges:
                if edge.start and edge.end:
                    self._draw_edge_ascii(grid, edge.start, edge.end, 
                                          xmin, ymin, xmax, ymax, width, height)
        
        # Convert to string
        lines = [''.join(row) for row in grid]
        return '\n'.join(lines)
    
    def _draw_edge_ascii(self, grid: List[List[str]], 
                          p1: Point, p2: Point,
                          xmin: float, ymin: float,
                          xmax: float, ymax: float,
                          width: int, height: int) -> None:
        """Draw an edge on ASCII grid using Bresenham-like algorithm."""
        x1 = int((p1.x - xmin) / (xmax - xmin + 1e-10) * (width - 1))
        y1 = int((p1.y - ymin) / (ymax - ymin + 1e-10) * (height - 1))
        x2 = int((p2.x - xmin) / (xmax - xmin + 1e-10) * (width - 1))
        y2 = int((p2.y - ymin) / (ymax - ymin + 1e-10) * (height - 1))
        
        # Clamp to grid bounds
        x1 = max(0, min(width - 1, x1))
        y1 = max(0, min(height - 1, y1))
        x2 = max(0, min(width - 1, x2))
        y2 = max(0, min(height - 1, y2))
        
        # Simple line drawing
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy, 1)
        
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            if 0 <= x < width and 0 <= y < height:
                if grid[y][x] == ' ':
                    grid[y][x] = '.'
    
    def to_svg(self, width: int = 400, height: int = 400, scale: float = 1.0) -> str:
        """Generate SVG representation of the diagram."""
        if not self.bbox:
            return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
        
        xmin, ymin, xmax, ymax = self.bbox
        
        def tx(x: float) -> float:
            return ((x - xmin) / (xmax - xmin + 1e-10)) * width
        
        def ty(y: float) -> float:
            return height - ((y - ymin) / (ymax - ymin + 1e-10)) * height
        
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<g stroke="black" stroke-width="1" fill="none">'
        ]
        
        # Draw cells with light fill
        for site, cell in self.cells.items():
            if len(cell.vertices) >= 3:
                ordered = cell._order_vertices()
                points_str = ' '.join([f'{tx(v.x):.1f},{ty(v.y):.1f}' for v in ordered])
                lines.append(f'<polygon points="{points_str}" fill="#f0f0f0" stroke="black"/>')
        
        lines.append('</g>')
        
        # Draw sites
        lines.append('<g fill="red">')
        for site in self.sites:
            sx, sy = tx(site.x), ty(site.y)
            lines.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4"/>')
        lines.append('</g>')
        
        lines.append('</svg>')
        
        return '\n'.join(lines)


# Convenience functions

def compute_voronoi(points: List[Tuple[float, float]], 
                    bbox: Optional[Tuple[float, float, float, float]] = None) -> VoronoiDiagram:
    """
    Compute Voronoi diagram from a list of points.
    
    Args:
        points: List of (x, y) coordinate tuples
        bbox: Optional bounding box (xmin, ymin, xmax, ymax)
    
    Returns:
        VoronoiDiagram object
    """
    site_points = [Point(x, y) for x, y in points]
    return VoronoiDiagram(site_points, bbox)


def nearest_point(points: List[Tuple[float, float]], target: Tuple[float, float]) -> Tuple[float, float]:
    """
    Find the nearest point in a set to a target point.
    
    Args:
        points: List of (x, y) coordinates
        target: Target (x, y) coordinates
    
    Returns:
        Nearest point coordinates
    """
    if not points:
        return (0, 0)
    
    target_point = Point(target[0], target[1])
    min_dist = float('inf')
    nearest = points[0]
    
    for p in points:
        dist = target_point.distance_to(Point(p[0], p[1]))
        if dist < min_dist:
            min_dist = dist
            nearest = p
    
    return nearest


def relax_points(points: List[Tuple[float, float]], 
                 iterations: int = 1,
                 bbox: Optional[Tuple[float, float, float, float]] = None) -> List[Tuple[float, float]]:
    """
    Apply Lloyd's relaxation to a set of points.
    
    Args:
        points: List of (x, y) coordinates
        iterations: Number of relaxation iterations
        bbox: Optional bounding box
    
    Returns:
        Relaxed point coordinates
    """
    site_points = [Point(x, y) for x, y in points]
    diagram = VoronoiDiagram(site_points, bbox)
    relaxed = diagram.relax(iterations)
    return [(p.x, p.y) for p in relaxed.sites]


def delaunay_neighbors(points: List[Tuple[float, float]], 
                       target: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Find Delaunay triangulation neighbors of a point.
    
    Args:
        points: List of all points
        target: Target point to find neighbors for
    
    Returns:
        List of neighboring points
    """
    site_points = [Point(x, y) for x, y in points]
    target_point = Point(target[0], target[1])
    
    diagram = VoronoiDiagram(site_points)
    neighbors = diagram.get_delaunay_neighbors(target_point)
    
    return [(n.x, n.y) for n in neighbors]


def voronoi_ascii(points: List[Tuple[float, float]], 
                  width: int = 40, height: int = 20) -> str:
    """
    Generate ASCII art Voronoi diagram.
    
    Args:
        points: List of (x, y) coordinates
        width: Output width in characters
        height: Output height in lines
    
    Returns:
        ASCII art string
    """
    site_points = [Point(x, y) for x, y in points]
    diagram = VoronoiDiagram(site_points)
    return diagram.to_ascii(width, height)


def voronoi_svg(points: List[Tuple[float, float]], 
                width: int = 400, height: int = 400) -> str:
    """
    Generate SVG Voronoi diagram.
    
    Args:
        points: List of (x, y) coordinates
        width: SVG width in pixels
        height: SVG height in pixels
    
    Returns:
        SVG string
    """
    site_points = [Point(x, y) for x, y in points]
    diagram = VoronoiDiagram(site_points)
    return diagram.to_svg(width, height)


class VoronoiUtils:
    """
    Utility class providing all Voronoi-related operations.
    
    This class serves as a namespace for all Voronoi utilities,
    providing a consistent interface for users who prefer class-based APIs.
    """
    
    @staticmethod
    def compute(points: List[Tuple[float, float]], 
                bbox: Optional[Tuple[float, float, float, float]] = None) -> VoronoiDiagram:
        """Compute Voronoi diagram."""
        return compute_voronoi(points, bbox)
    
    @staticmethod
    def nearest(points: List[Tuple[float, float]], target: Tuple[float, float]) -> Tuple[float, float]:
        """Find nearest point."""
        return nearest_point(points, target)
    
    @staticmethod
    def relax(points: List[Tuple[float, float]], 
              iterations: int = 1,
              bbox: Optional[Tuple[float, float, float, float]] = None) -> List[Tuple[float, float]]:
        """Apply Lloyd's relaxation."""
        return relax_points(points, iterations, bbox)
    
    @staticmethod
    def neighbors(points: List[Tuple[float, float]], 
                  target: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Get Delaunay neighbors."""
        return delaunay_neighbors(points, target)
    
    @staticmethod
    def ascii(points: List[Tuple[float, float]], 
              width: int = 40, height: int = 20) -> str:
        """Generate ASCII art."""
        return voronoi_ascii(points, width, height)
    
    @staticmethod
    def svg(points: List[Tuple[float, float]], 
            width: int = 400, height: int = 400) -> str:
        """Generate SVG."""
        return voronoi_svg(points, width, height)
    
    @staticmethod
    def cell_area(cell: VoronoiCell) -> float:
        """Calculate cell area."""
        return cell.area()
    
    @staticmethod
    def cell_centroid(cell: VoronoiCell) -> Tuple[float, float]:
        """Calculate cell centroid."""
        c = cell.centroid()
        return (c.x, c.y)
    
    @staticmethod
    def point_in_cell(cell: VoronoiCell, point: Tuple[float, float]) -> bool:
        """Check if point is in cell."""
        p = Point(point[0], point[1])
        return cell.contains_point(p)


# Additional helper functions

def generate_random_points(n: int, 
                          bbox: Tuple[float, float, float, float] = (0, 0, 1, 1)) -> List[Tuple[float, float]]:
    """
    Generate n random points within a bounding box.
    
    Args:
        n: Number of points to generate
        bbox: Bounding box (xmin, ymin, xmax, ymax)
    
    Returns:
        List of random (x, y) coordinates
    """
    xmin, ymin, xmax, ymax = bbox
    
    points = []
    for _ in range(n):
        x = xmin + (xmax - xmin) * random.random()
        y = ymin + (ymax - ymin) * random.random()
        points.append((x, y))
    
    return points


def evenly_distribute_points(n: int, 
                             bbox: Tuple[float, float, float, float] = (0, 0, 1, 1),
                             iterations: int = 10) -> List[Tuple[float, float]]:
    """
    Generate n evenly distributed points using Lloyd's algorithm.
    
    Args:
        n: Number of points to generate
        bbox: Bounding box (xmin, ymin, xmax, ymax)
        iterations: Number of relaxation iterations
    
    Returns:
        List of evenly distributed (x, y) coordinates
    """
    # Generate initial random points
    points = generate_random_points(n, bbox)
    
    # Apply relaxation
    return relax_points(points, iterations, bbox)


def point_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Distance
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def midpoint(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Calculate midpoint between two points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Midpoint (x, y)
    """
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def circle_through_three_points(p1: Tuple[float, float], 
                                p2: Tuple[float, float],
                                p3: Tuple[float, float]) -> Optional[Tuple[Tuple[float, float], float]]:
    """
    Find the circle passing through three points.
    
    Args:
        p1, p2, p3: Three points (x, y)
    
    Returns:
        (center, radius) or None if points are collinear
    """
    ax, ay = p1[0], p1[1]
    bx, by = p2[0], p2[1]
    cx, cy = p3[0], p3[1]
    
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    if abs(d) < 1e-10:
        return None  # Points are collinear
    
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    
    center = (ux, uy)
    radius = math.sqrt((ax - ux)**2 + (ay - uy)**2)
    
    return (center, radius)


def is_collinear(p1: Tuple[float, float], 
                 p2: Tuple[float, float],
                 p3: Tuple[float, float]) -> bool:
    """
    Check if three points are collinear.
    
    Args:
        p1, p2, p3: Three points (x, y)
    
    Returns:
        True if collinear
    """
    # Area of triangle formed by three points
    area = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    return abs(area) < 1e-10


if __name__ == '__main__':
    # Quick demo
    print("Voronoi Diagram Utilities Demo")
    print("=" * 40)
    
    # Generate some random points
    points = generate_random_points(10, (0, 0, 10, 10))
    print(f"\nGenerated {len(points)} random points:")
    for i, p in enumerate(points):
        print(f"  Point {i+1}: ({p[0]:.2f}, {p[1]:.2f})")
    
    # Compute Voronoi diagram
    diagram = compute_voronoi(points, (0, 0, 10, 10))
    print(f"\nVoronoi diagram computed:")
    print(f"  Sites: {len(diagram.sites)}")
    print(f"  Vertices: {len(diagram.vertices)}")
    print(f"  Cells: {len(diagram.cells)}")
    
    # ASCII visualization
    print("\nASCII Visualization:")
    print(diagram.to_ascii(50, 25))
    
    # Find nearest point
    target = (5, 5)
    nearest = nearest_point(points, target)
    print(f"\nNearest point to ({target[0]}, {target[1]}): ({nearest[0]:.2f}, {nearest[1]:.2f})")
    
    # Relaxation demo
    relaxed = relax_points(points, 5, (0, 0, 10, 10))
    print(f"\nAfter 5 Lloyd relaxations:")
    for i, p in enumerate(relaxed):
        print(f"  Point {i+1}: ({p[0]:.2f}, {p[1]:.2f})")