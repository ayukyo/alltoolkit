"""
Voronoi Utils - Usage Examples

This file demonstrates various use cases for the Voronoi diagram utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    VoronoiDiagram, Point, VoronoiUtils,
    compute_voronoi, nearest_point, relax_points, delaunay_neighbors,
    voronoi_ascii, voronoi_svg,
    generate_random_points, evenly_distribute_points,
    point_distance, midpoint, circle_through_three_points, is_collinear
)


def example_basic_voronoi():
    """Example 1: Basic Voronoi diagram computation."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Voronoi Diagram")
    print("=" * 60)
    
    # Define generator points (sites)
    points = [(0, 0), (10, 0), (5, 10), (5, 5)]
    
    # Compute Voronoi diagram
    diagram = compute_voronoi(points, bbox=(0, 0, 15, 15))
    
    print(f"Sites (generator points): {len(diagram.sites)}")
    for site in diagram.sites:
        print(f"  {site}")
    
    print(f"\nVertices (cell corners): {len(diagram.vertices)}")
    for v in diagram.vertices:
        print(f"  {v}")
    
    print(f"\nEdges (cell boundaries): {len(diagram.edges)}")
    for edge in diagram.edges:
        if edge.is_finite():
            print(f"  {edge.start} -> {edge.end}")
    
    # ASCII visualization
    print("\nASCII Visualization:")
    print(diagram.to_ascii(width=50, height=25))


def example_nearest_point():
    """Example 2: Finding nearest generator point."""
    print("\n" + "=" * 60)
    print("Example 2: Nearest Point Queries")
    print("=" * 60)
    
    # Define cities as points
    cities = {
        (0, 0): "City A",
        (50, 50): "City B",
        (100, 0): "City C",
        (25, 75): "City D",
    }
    
    points = list(cities.keys())
    
    # Find nearest city to various locations
    locations = [(10, 10), (60, 60), (90, 10), (30, 80)]
    
    for loc in locations:
        nearest = nearest_point(points, loc)
        city_name = cities[nearest]
        dist = point_distance(loc, nearest)
        print(f"Location ({loc[0]}, {loc[1]}) -> Nearest: {city_name} at ({nearest[0]}, {nearest[1]})")
        print(f"  Distance: {dist:.2f} units")


def example_lloyd_relaxation():
    """Example 3: Lloyd's algorithm for even distribution."""
    print("\n" + "=" * 60)
    print("Example 3: Lloyd's Relaxation (Even Distribution)")
    print("=" * 60)
    
    # Start with clustered points
    initial_points = [(1, 1), (2, 2), (3, 3), (97, 97), (98, 98), (99, 99)]
    
    print("Initial points (clustered):")
    for p in initial_points:
        print(f"  ({p[0]:.1f}, {p[1]:.1f})")
    
    # Apply Lloyd's relaxation
    relaxed_points = relax_points(initial_points, iterations=10, bbox=(0, 0, 100, 100))
    
    print("\nAfter 10 iterations of Lloyd's relaxation:")
    for p in relaxed_points:
        print(f"  ({p[0]:.1f}, {p[1]:.1f})")
    
    # Calculate average pairwise distance improvement
    def avg_distance(points):
        total = sum(point_distance(p1, p2) for i, p1 in enumerate(points) for p2 in points[i+1:])
        n = len(points)
        return total / (n * (n-1) / 2)
    
    print(f"\nAverage pairwise distance:")
    print(f"  Initial: {avg_distance(initial_points):.2f}")
    print(f"  Relaxed: {avg_distance(relaxed_points):.2f}")


def example_delaunay_neighbors():
    """Example 4: Delaunay triangulation neighbors."""
    print("\n" + "=" * 60)
    print("Example 4: Delaunay Triangulation (Natural Neighbor)")
    print("=" * 60)
    
    # Define points
    points = [(0, 0), (10, 0), (20, 0), (0, 10), (10, 10), (20, 10), (10, 5)]
    
    # Find neighbors for center point
    center = (10, 5)
    neighbors = delaunay_neighbors(points, center)
    
    print(f"Point {center} has Delaunay neighbors:")
    for n in neighbors:
        dist = point_distance(center, n)
        print(f"  ({n[0]}, {n[1]}) - distance: {dist:.2f}")
    
    # Visualize
    print("\nASCII Visualization (neighbors marked with *):")
    diagram = compute_voronoi(points, bbox=(0, 0, 20, 10))
    ascii_art = diagram.to_ascii(width=40, height=20)
    
    # Mark neighbors in ASCII (just for illustration)
    print(ascii_art)


def example_cell_analysis():
    """Example 5: Analyzing Voronoi cells."""
    print("\n" + "=" * 60)
    print("Example 5: Voronoi Cell Analysis")
    print("=" * 60)
    
    # Create diagram
    points = [(0, 0), (20, 0), (10, 20), (10, 10)]
    bbox = (0, 0, 25, 25)
    diagram = compute_voronoi(points, bbox)
    
    print(f"Analyzing {len(diagram.cells)} cells:")
    
    for site, cell in diagram.cells.items():
        area = cell.area()
        centroid = cell.centroid()
        num_vertices = len(cell.vertices)
        
        print(f"\nCell centered at ({site.x:.1f}, {site.y:.1f}):")
        print(f"  Area: {area:.2f} square units")
        print(f"  Centroid: ({centroid.x:.1f}, {centroid.y:.1f})")
        print(f"  Vertices: {num_vertices}")
        
        if cell.vertices:
            print(f"  Vertex coordinates:")
            for v in cell.vertices[:min(4, len(cell.vertices))]:
                print(f"    ({v.x:.1f}, {v.y:.1f})")


def example_point_distribution():
    """Example 6: Generating evenly distributed points."""
    print("\n" + "=" * 60)
    print("Example 6: Evenly Distributed Point Generation")
    print("=" * 60)
    
    # Generate 20 evenly distributed points
    bbox = (0, 0, 50, 50)
    even_points = evenly_distribute_points(20, bbox, iterations=15)
    
    print(f"Generated {len(even_points)} evenly distributed points:")
    
    # Calculate minimum distance between any two points
    min_dist = min(point_distance(p1, p2) 
                   for i, p1 in enumerate(even_points) 
                   for p2 in even_points[i+1:])
    
    # Calculate average distance
    avg_dist = sum(point_distance(p1, p2) 
                   for i, p1 in enumerate(even_points) 
                   for p2 in even_points[i+1:]) / (20 * 19 / 2)
    
    print(f"Minimum pairwise distance: {min_dist:.2f}")
    print(f"Average pairwise distance: {avg_dist:.2f}")
    
    # Show points
    print("\nPoint coordinates:")
    for i, p in enumerate(even_points):
        print(f"  P{i+1}: ({p[0]:.2f}, {p[1]:.2f})")


def example_svg_output():
    """Example 7: SVG visualization output."""
    print("\n" + "=" * 60)
    print("Example 7: SVG Visualization")
    print("=" * 60)
    
    # Create diagram with nice points
    points = [(50, 50), (150, 50), (100, 150), (75, 100), (125, 100)]
    bbox = (0, 0, 200, 200)
    diagram = compute_voronoi(points, bbox)
    
    # Generate SVG
    svg = diagram.to_svg(width=400, height=400)
    
    print("SVG Output (first 500 chars):")
    print(svg[:500] + "...")
    
    print("\nFull SVG can be saved to file:")
    print("  svg_output = diagram.to_svg(400, 400)")
    print("  with open('voronoi.svg', 'w') as f:")
    print("      f.write(svg_output)")
    
    # Actually save it for demonstration
    example_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(example_dir, 'voronoi_example.svg')
    with open(svg_path, 'w') as f:
        f.write(svg)
    print(f"\n  Saved to: {svg_path}")


def example_geometric_helpers():
    """Example 8: Geometric helper functions."""
    print("\n" + "=" * 60)
    print("Example 8: Geometric Helper Functions")
    print("=" * 60)
    
    # Distance calculation
    p1, p2 = (0, 0), (3, 4)
    dist = point_distance(p1, p2)
    print(f"Distance between {p1} and {p2}: {dist}")
    
    # Midpoint
    mid = midpoint(p1, p2)
    print(f"Midpoint of {p1} and {p2}: {mid}")
    
    # Collinearity check
    tri1 = [(0, 0), (1, 1), (2, 2)]
    tri2 = [(0, 0), (1, 0), (0, 1)]
    print(f"\nAre {tri1} collinear? {is_collinear(*tri1)}")
    print(f"Are {tri2} collinear? {is_collinear(*tri2)}")
    
    # Circle through three points
    result = circle_through_three_points((0, 0), (4, 0), (2, 2))
    if result:
        center, radius = result
        print(f"\nCircle through (0,0), (4,0), (2,2):")
        print(f"  Center: {center}")
        print(f"  Radius: {radius:.2f}")


def example_class_interface():
    """Example 9: Using VoronoiUtils class interface."""
    print("\n" + "=" * 60)
    print("Example 9: VoronoiUtils Class Interface")
    print("=" * 60)
    
    points = [(10, 10), (90, 10), (50, 90), (50, 50)]
    bbox = (0, 0, 100, 100)
    
    # Compute diagram using class method
    diagram = VoronoiUtils.compute(points, bbox)
    print(f"Computed diagram with {len(diagram.sites)} sites")
    
    # Find nearest point
    test_point = (30, 30)
    nearest = VoronoiUtils.nearest(points, test_point)
    print(f"Nearest to {test_point}: {nearest}")
    
    # Get neighbors
    neighbors = VoronoiUtils.neighbors(points, (50, 50))
    print(f"Neighbors of (50, 50): {neighbors}")
    
    # Relax points
    relaxed = VoronoiUtils.relax(points, 5, bbox)
    print(f"Relaxed points: {relaxed}")
    
    # Generate ASCII art
    ascii_art = VoronoiUtils.ascii(points, width=40, height=20)
    print("\nASCII Art:")
    print(ascii_art)
    
    # Generate SVG
    svg = VoronoiUtils.svg(points)
    print(f"\nSVG generated (length: {len(svg)} characters)")


def example_real_world_scenario():
    """Example 10: Real-world scenario - Store location analysis."""
    print("\n" + "=" * 60)
    print("Example 10: Real-World - Store Coverage Analysis")
    print("=" * 60)
    
    # Scenario: Analyze coverage areas for 5 stores in a city
    # City bounds: 10km x 10km
    stores = {
        (2, 3): "North Store",
        (8, 2): "East Store",
        (1, 7): "West Store",
        (9, 8): "South Store",
        (5, 5): "Central Store",
    }
    
    bbox = (0, 0, 10, 10)  # 10km x 10km area
    
    # Compute Voronoi diagram (each cell = store's coverage area)
    diagram = compute_voronoi(list(stores.keys()), bbox)
    
    print("Store Coverage Areas:")
    print("-" * 40)
    
    total_coverage = 0
    for site, cell in diagram.cells.items():
        store_name = stores[(site.x, site.y)]
        area = cell.area()
        total_coverage += area
        
        print(f"\n{store_name} at ({site.x:.1f}, {site.y:.1f}):")
        print(f"  Coverage area: {area:.1f} km²")
        
        # Find centroid (ideal location for maximum coverage)
        centroid = cell.centroid()
        print(f"  Coverage centroid: ({centroid.x:.1f}, {centroid.y:.1f})")
        
        # Distance from store to centroid
        dist_to_centroid = point_distance((site.x, site.y), (centroid.x, centroid.y))
        print(f"  Distance to centroid: {dist_to_centroid:.2f} km")
    
    print(f"\nTotal coverage: {total_coverage:.1f} km²")
    print(f"Average coverage per store: {total_coverage/len(stores):.1f} km²")
    
    # Test customer locations
    print("\nCustomer location analysis:")
    customers = [(3, 3), (7, 7), (1, 1), (9, 9)]
    
    for customer in customers:
        nearest_store_coords = nearest_point(list(stores.keys()), customer)
        store_name = stores[nearest_store_coords]
        distance = point_distance(customer, nearest_store_coords)
        print(f"  Customer at ({customer[0]}, {customer[1]}) -> {store_name}")
        print(f"    Distance to store: {distance:.2f} km")


def example_visualization_comparison():
    """Example 11: Before/After relaxation visualization."""
    print("\n" + "=" * 60)
    print("Example 11: Visualization - Before/After Relaxation")
    print("=" * 60)
    
    # Initial clustered points
    initial_points = [(2, 2), (3, 3), (4, 4), (96, 96), (97, 97), (98, 98)]
    bbox = (0, 0, 100, 100)
    
    print("\nInitial distribution (clustered):")
    initial_diagram = compute_voronoi(initial_points, bbox)
    print(initial_diagram.to_ascii(width=40, height=20))
    
    # After relaxation
    relaxed_points = relax_points(initial_points, iterations=20, bbox=bbox)
    
    print("\nAfter 20 Lloyd relaxation iterations:")
    relaxed_diagram = compute_voronoi(relaxed_points, bbox)
    print(relaxed_diagram.to_ascii(width=40, height=20))


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Voronoir Utils - Complete Usage Examples")
    print("=" * 60)
    
    examples = [
        example_basic_voronoi,
        example_nearest_point,
        example_lloyd_relaxation,
        example_delaunay_neighbors,
        example_cell_analysis,
        example_point_distribution,
        example_svg_output,
        example_geometric_helpers,
        example_class_interface,
        example_real_world_scenario,
        example_visualization_comparison,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()