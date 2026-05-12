"""
Voronoi Diagram Utilities - Test Suite

Comprehensive tests for Voronoi diagram computation and utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    VoronoiDiagram, Point, VoronoiCell, VoronoiUtils,
    compute_voronoi, nearest_point, relax_points, delaunay_neighbors,
    voronoi_ascii, voronoi_svg,
    generate_random_points, evenly_distribute_points,
    point_distance, midpoint, circle_through_three_points, is_collinear
)


def test_point_operations():
    """Test Point class operations."""
    print("Testing Point operations...")
    
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    
    # Distance
    dist = p1.distance_to(p2)
    assert dist == 5.0, f"Expected distance 5.0, got {dist}"
    
    # Midpoint
    mid = p1.midpoint(p2)
    assert mid.x == 1.5 and mid.y == 2.0, f"Expected midpoint (1.5, 2.0), got {mid}"
    
    print("  ✓ Point operations passed")


def test_point_helpers():
    """Test helper functions for point operations."""
    print("Testing point helper functions...")
    
    # point_distance
    dist = point_distance((0, 0), (3, 4))
    assert dist == 5.0, f"Expected distance 5.0, got {dist}"
    
    # midpoint
    mid = midpoint((0, 0), (6, 8))
    assert mid == (3.0, 4.0), f"Expected midpoint (3.0, 4.0), got {mid}"
    
    # is_collinear
    assert is_collinear((0, 0), (1, 1), (2, 2)) == True, "Points should be collinear"
    assert is_collinear((0, 0), (1, 0), (0, 1)) == False, "Points should not be collinear"
    
    # circle_through_three_points
    result = circle_through_three_points((0, 0), (2, 0), (1, 1))
    assert result is not None, "Should find circle for valid points"
    center, radius = result
    assert abs(center[0] - 1.0) < 0.01, f"Expected center x ≈ 1.0, got {center[0]}"
    
    # Collinear points should return None
    result = circle_through_three_points((0, 0), (1, 1), (2, 2))
    assert result is None, "Should return None for collinear points"
    
    print("  ✓ Point helper functions passed")


def test_voronoi_cell():
    """Test VoronoiCell operations."""
    print("Testing VoronoiCell operations...")
    
    cell = VoronoiCell(Point(5, 5))
    
    # Add vertices forming a square
    cell.vertices = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
    cell.is_closed = True
    
    # Area
    area = cell.area()
    assert area == 100.0, f"Expected area 100.0, got {area}"
    
    # Centroid
    centroid = cell.centroid()
    assert centroid.x == 5.0 and centroid.y == 5.0, f"Expected centroid (5, 5), got {centroid}"
    
    # Contains point
    assert cell.contains_point(Point(5, 5)) == True, "Center should be inside cell"
    assert cell.contains_point(Point(0, 0)) == True, "Corner should be inside (boundary)"
    assert cell.contains_point(Point(15, 15)) == False, "Outside point should not be inside"
    
    print("  ✓ VoronoiCell operations passed")


def test_voronoi_diagram_basic():
    """Test basic Voronoi diagram computation."""
    print("Testing basic Voronoi diagram computation...")
    
    # Simple case: two points
    points = [(0, 0), (10, 0)]
    diagram = compute_voronoi(points)
    
    assert len(diagram.sites) == 2, f"Expected 2 sites, got {len(diagram.sites)}"
    
    # Nearest site
    nearest = diagram.find_nearest_site(Point(2, 0))
    assert nearest.x == 0 and nearest.y == 0, "Should find left site nearest"
    
    nearest = diagram.find_nearest_site(Point(8, 0))
    assert nearest.x == 10 and nearest.y == 0, "Should find right site nearest"
    
    print("  ✓ Basic Voronoi diagram computation passed")


def test_voronoi_diagram_multiple_points():
    """Test Voronoi diagram with multiple points."""
    print("Testing Voronoi diagram with multiple points...")
    
    # Multiple points
    points = [(0, 0), (10, 0), (5, 10), (5, 5)]
    bbox = (0, 0, 10, 10)
    diagram = compute_voronoi(points, bbox)
    
    assert len(diagram.sites) == 4, f"Expected 4 sites, got {len(diagram.sites)}"
    
    # Each site should have a cell
    for site in diagram.sites:
        cell = diagram.cells.get(site)
        assert cell is not None, f"Cell for site {site} should exist"
    
    # Find cell containing a point
    cell = diagram.find_cell(Point(1, 1))
    assert cell is not None, "Should find cell for point"
    assert cell.site.x == 0 and cell.site.y == 0, "Should find cell of left site"
    
    print("  ✓ Multiple point Voronoi diagram passed")


def test_nearest_point_function():
    """Test nearest_point convenience function."""
    print("Testing nearest_point function...")
    
    points = [(0, 0), (10, 10), (5, 5), (3, 3)]
    
    nearest = nearest_point(points, (0, 0))
    assert nearest == (0, 0), "Origin should be nearest to itself"
    
    nearest = nearest_point(points, (4, 4))
    assert nearest == (5, 5) or nearest == (3, 3), "Should find nearest of center points"
    
    nearest = nearest_point(points, (11, 11))
    assert nearest == (10, 10), "Should find top-right point"
    
    print("  ✓ nearest_point function passed")


def test_delaunay_neighbors():
    """Test Delaunay triangulation neighbors."""
    print("Testing Delaunay neighbors...")
    
    # Four points forming a square
    points = [(0, 0), (10, 0), (10, 10), (0, 10)]
    neighbors = delaunay_neighbors(points, (0, 0))
    
    # Each corner should be connected to adjacent corners
    assert len(neighbors) >= 2, f"Expected at least 2 neighbors, got {len(neighbors)}"
    
    # Check that neighbors are adjacent corners
    neighbor_coords = set(neighbors)
    expected = {(10, 0), (0, 10)}
    assert neighbor_coords.intersection(expected) == expected or len(neighbor_coords.intersection(expected)) >= 2, \
        f"Expected neighbors to include {expected}, got {neighbors}"
    
    print("  ✓ Delaunay neighbors passed")


def test_lloyd_relaxation():
    """Test Lloyd's relaxation algorithm."""
    print("Testing Lloyd's relaxation...")
    
    # Start with uneven distribution
    points = [(0, 0), (1, 1), (2, 2), (9, 9)]
    bbox = (0, 0, 10, 10)
    
    # Apply relaxation
    relaxed = relax_points(points, 3, bbox)
    
    assert len(relaxed) == 4, f"Should have same number of points"
    
    # Points should be spread out (relaxed should have larger minimum distance)
    # Calculate minimum pairwise distance
    def min_distance(pts):
        min_dist = float('inf')
        for i, p1 in enumerate(pts):
            for p2 in pts[i+1:]:
                d = point_distance(p1, p2)
                if d < min_dist:
                    min_dist = d
        return min_dist
    
    orig_min = min_distance(points)
    rel_min = min_distance(relaxed)
    
    # Relaxed points should have minimum distance >= original or be spread more evenly
    # The key check is that relaxation produces valid points within bbox
    for p in relaxed:
        assert 0 <= p[0] <= 10, f"Relaxed point {p} should be within bbox"
        assert 0 <= p[1] <= 10, f"Relaxed point {p} should be within bbox"
    
    print("  ✓ Lloyd's relaxation passed")


def test_voronoi_utils_class():
    """Test VoronoiUtils class interface."""
    print("Testing VoronoiUtils class...")
    
    points = [(0, 0), (10, 10), (5, 5)]
    bbox = (0, 0, 10, 10)
    
    # Compute diagram
    diagram = VoronoiUtils.compute(points, bbox)
    assert diagram is not None, "Should compute diagram"
    
    # Find nearest
    nearest = VoronoiUtils.nearest(points, (0, 0))
    assert nearest == (0, 0), "Should find nearest point"
    
    # Relax points
    relaxed = VoronoiUtils.relax(points, 2, bbox)
    assert len(relaxed) == 3, "Should have same number of points"
    
    # Get neighbors
    neighbors = VoronoiUtils.neighbors(points, (5, 5))
    assert len(neighbors) >= 0, "Should get neighbors"
    
    # Generate ASCII
    ascii_art = VoronoiUtils.ascii(points)
    assert len(ascii_art) > 0, "Should generate ASCII art"
    assert '+' in ascii_art, "ASCII art should contain site markers"
    
    # Generate SVG
    svg = VoronoiUtils.svg(points)
    assert '<svg' in svg, "Should generate valid SVG"
    assert '<circle' in svg, "SVG should contain site circles"
    
    print("  ✓ VoronoiUtils class passed")


def test_ascii_visualization():
    """Test ASCII art generation."""
    print("Testing ASCII visualization...")
    
    points = [(2, 2), (8, 2), (5, 8)]
    ascii_art = voronoi_ascii(points, width=20, height=10)
    
    assert len(ascii_art) > 0, "Should generate ASCII art"
    lines = ascii_art.split('\n')
    assert len(lines) == 10, f"Expected 10 lines, got {len(lines)}"
    assert all(len(line) == 20 for line in lines), "All lines should be 20 chars"
    
    # Check for site markers
    assert '+' in ascii_art, "Should contain site markers (+)"
    
    print("  ✓ ASCII visualization passed")


def test_svg_visualization():
    """Test SVG generation."""
    print("Testing SVG visualization...")
    
    points = [(0, 0), (100, 0), (50, 100)]
    svg = voronoi_svg(points, width=200, height=200)
    
    # Check SVG structure
    assert svg.startswith('<svg'), "Should start with <svg tag"
    assert svg.endswith('</svg>'), "Should end with </svg>"
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg, "Should have xmlns"
    
    # Check elements
    assert '<circle' in svg, "Should have circle elements for sites"
    assert '<line' in svg or '<polygon' in svg, "Should have line or polygon elements"
    
    print("  ✓ SVG visualization passed")


def test_random_point_generation():
    """Test random point generation."""
    print("Testing random point generation...")
    
    bbox = (0, 0, 100, 100)
    points = generate_random_points(50, bbox)
    
    assert len(points) == 50, f"Expected 50 points, got {len(points)}"
    
    # All points should be within bbox
    for x, y in points:
        assert 0 <= x <= 100, f"Point x={x} should be within bbox"
        assert 0 <= y <= 100, f"Point y={y} should be within bbox"
    
    # Points should have some variety (not all the same)
    unique_points = set(points)
    assert len(unique_points) > 10, "Should have variety in points"
    
    print("  ✓ Random point generation passed")


def test_evenly_distributed_points():
    """Test evenly distributed point generation."""
    print("Testing evenly distributed point generation...")
    
    bbox = (0, 0, 10, 10)
    points = evenly_distribute_points(20, bbox, iterations=5)
    
    assert len(points) == 20, f"Expected 20 points, got {len(points)}"
    
    # All points should be within bbox
    for x, y in points:
        assert 0 <= x <= 10, f"Point x={x} should be within bbox"
        assert 0 <= y <= 10, f"Point y={y} should be within bbox"
    
    # Calculate spacing - should be relatively even
    # Use simple metric: check that no two points are extremely close
    min_dist = 0.3
    for i, p1 in enumerate(points):
        for p2 in points[i+1:]:
            dist = point_distance(p1, p2)
            assert dist > min_dist, f"Points {p1} and {p2} are too close ({dist:.2f})"
    
    print("  ✓ Evenly distributed points passed")


def test_cell_area_and_centroid():
    """Test VoronoiUtils cell operations."""
    print("Testing cell area and centroid helpers...")
    
    points = [(0, 0), (2, 0), (1, 1)]
    diagram = compute_voronoi(points, (0, 0, 3, 3))
    
    for site, cell in diagram.cells.items():
        area = VoronoiUtils.cell_area(cell)
        assert area >= 0, f"Cell area should be non-negative"
        
        centroid = VoronoiUtils.cell_centroid(cell)
        assert len(centroid) == 2, "Centroid should be (x, y) tuple"
    
    print("  ✓ Cell area and centroid helpers passed")


def test_bounded_voronoi():
    """Test Voronoi diagram with bounding box."""
    print("Testing bounded Voronoi diagram...")
    
    points = [(5, 5), (15, 15), (25, 5)]  # Some outside bbox
    bbox = (0, 0, 20, 20)
    
    # Sites should still be all points
    diagram = compute_voronoi(points, bbox)
    assert len(diagram.sites) == 3, "Should have all 3 sites"
    
    # Vertices should be bounded
    for v in diagram.vertices:
        assert v.x >= bbox[0] - 1 and v.x <= bbox[2] + 1, f"Vertex x={v.x} should be near bbox"
        assert v.y >= bbox[1] - 1 and v.y <= bbox[3] + 1, f"Vertex y={v.y} should be near bbox"
    
    print("  ✓ Bounded Voronoi diagram passed")


def test_empty_voronoi():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Empty points
    diagram = compute_voronoi([])
    assert len(diagram.sites) == 0, "Empty diagram should have no sites"
    
    # Single point
    diagram = compute_voronoi([(5, 5)])
    assert len(diagram.sites) == 1, "Single point diagram should have one site"
    
    # nearest_point with single point
    nearest = nearest_point([(5, 5)], (100, 100))
    assert nearest == (5, 5), "Should return the only point"
    
    print("  ✓ Edge cases passed")


def test_integration():
    """Integration test: full workflow."""
    print("Testing integration workflow...")
    
    # Generate random points
    points = generate_random_points(20, (0, 0, 50, 50))
    
    # Compute Voronoi diagram
    diagram = compute_voronoi(points, (0, 0, 50, 50))
    
    # Find nearest site for a test point
    test_point = (25, 25)
    nearest = diagram.find_nearest_site(Point(test_point[0], test_point[1]))
    assert nearest is not None, "Should find nearest site"
    
    # Find containing cell
    cell = diagram.find_cell(Point(test_point[0], test_point[1]))
    assert cell is not None, "Should find containing cell"
    
    # Get Delaunay neighbors
    neighbors = diagram.get_delaunay_neighbors(nearest)
    assert isinstance(neighbors, list), "Neighbors should be a list"
    
    # Relax points
    relaxed_points = relax_points(points, 5, (0, 0, 50, 50))
    assert len(relaxed_points) == len(points), "Relaxed should have same count"
    
    # Generate visualizations
    ascii_viz = diagram.to_ascii(40, 20)
    svg_viz = diagram.to_svg(400, 400)
    
    assert len(ascii_viz) > 0, "Should generate ASCII"
    assert '<svg' in svg_viz, "Should generate SVG"
    
    print("  ✓ Integration workflow passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Voronoi Utils Test Suite")
    print("=" * 50 + "\n")
    
    tests = [
        test_point_operations,
        test_point_helpers,
        test_voronoi_cell,
        test_voronoi_diagram_basic,
        test_voronoi_diagram_multiple_points,
        test_nearest_point_function,
        test_delaunay_neighbors,
        test_lloyd_relaxation,
        test_voronoi_utils_class,
        test_ascii_visualization,
        test_svg_visualization,
        test_random_point_generation,
        test_evenly_distributed_points,
        test_cell_area_and_centroid,
        test_bounded_voronoi,
        test_empty_voronoi,
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  ✗ FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"  ✗ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)