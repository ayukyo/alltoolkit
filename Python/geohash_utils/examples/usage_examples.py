#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geohash Utilities Examples
========================================
Usage examples for the geohash_utils module.

Geohash is a geocoding system that encodes geographic coordinates
into a short string of letters and digits. It's widely used in:
- Location-based services
- Spatial indexing in databases
- Nearby search optimization
- Geospatial clustering

Run this file to see comprehensive examples.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Data classes
    GeoPoint, GeoBounds, GeoCell,
    
    # Encoding/decoding
    encode, decode, decode_bounds,
    
    # Neighbor functions
    neighbors, neighbor, expand,
    
    # Distance functions
    haversine_distance, distance, distance_point_to_geohash,
    
    # Validation
    is_valid, validate,
    
    # Utilities
    get_precision, get_cell_dimensions, get_cell_area,
    common_prefix, covers_area,
    
    # Cell functions
    get_cell, children, parent,
)


def example_encoding():
    """Example: Encoding coordinates to geohash."""
    print("\n" + "=" * 60)
    print("Geohash Encoding")
    print("=" * 60)
    
    # Famous locations
    locations = [
        (40.7128, -74.0060, "New York City, USA"),
        (35.6762, 139.6503, "Tokyo, Japan"),
        (-33.8688, 151.2093, "Sydney, Australia"),
        (51.5074, -0.1278, "London, UK"),
        (48.8566, 2.3522, "Paris, France"),
        (55.7558, 37.6173, "Moscow, Russia"),
        (22.3193, 114.1694, "Hong Kong"),
        (1.3521, 103.8198, "Singapore"),
        (0, 0, "Null Island (origin)"),
    ]
    
    print("\n  Encoding at precision 6:")
    for lat, lng, name in locations:
        gh = encode(lat, lng, 6)
        print(f"    {name}: {gh}")
    
    print("\n  Different precision levels (NYC):")
    lat, lng = 40.7128, -74.0060
    for precision in [1, 2, 3, 4, 5, 6, 8, 10, 12]:
        gh = encode(lat, lng, precision)
        dims = get_cell_dimensions(precision)
        area = get_cell_area(precision)
        print(f"    Precision {precision}: {gh}")
        print(f"      Cell size: {dims[0]:.2f}km x {dims[1]:.2f}km")
        print(f"      Cell area: {area:.2f}km²")


def example_decoding():
    """Example: Decoding geohash to coordinates."""
    print("\n" + "=" * 60)
    print("Geohash Decoding")
    print("=" * 60)
    
    geohashes = [
        ('dr5ru7', "NYC area"),
        ('xn76ur', "Tokyo area"),
        ('r3gx2f', "Sydney area"),
        ('gcpvj0', "London area"),
        ('u09tvr', "Paris area"),
    ]
    
    print("\n  Decoding geohashes:")
    for gh, name in geohashes:
        lat, lng = decode(gh)
        print(f"    {gh} ({name}):")
        print(f"      Coordinates: ({lat:.5f}, {lng:.5f})")
    
    print("\n  Getting bounding boxes:")
    for gh, name in geohashes[:3]:
        bounds = decode_bounds(gh)
        print(f"    {gh}:")
        print(f"      SW: ({bounds.min_lat:.5f}, {bounds.min_lng:.5f})")
        print(f"      NE: ({bounds.max_lat:.5f}, {bounds.max_lng:.5f})")
        print(f"      Center: ({bounds.center[0]:.5f}, {bounds.center[1]:.5f})")


def example_neighbors():
    """Example: Finding neighboring geohashes."""
    print("\n" + "=" * 60)
    print("Neighbor Geohashes")
    print("=" * 60)
    
    # Start with a geohash in NYC
    gh = 'dr5ru7'
    
    print(f"\n  Center geohash: {gh}")
    lat, lng = decode(gh)
    print(f"    Location: ({lat:.5f}, {lng:.5f})")
    
    print("\n  All 8 neighbors:")
    n = neighbors(gh)
    for direction, neighbor_gh in sorted(n.items()):
        neighbor_lat, neighbor_lng = decode(neighbor_gh)
        dist = haversine_distance(lat, lng, neighbor_lat, neighbor_lng)
        print(f"    {direction:2s}: {neighbor_gh} (dist: {dist*1000:.1f}m)")
    
    print("\n  Specific direction:")
    north_gh = neighbor(gh, 'n')
    print(f"    North of {gh}: {north_gh}")


def example_distance():
    """Example: Distance calculations."""
    print("\n" + "=" * 60)
    print("Distance Calculations")
    print("=" * 60)
    
    # Calculate distances between famous cities
    cities = {
        'nyc': (40.7128, -74.0060),
        'la': (34.0522, -118.2437),
        'tokyo': (35.6762, 139.6503),
        'london': (51.5074, -0.1278),
        'sydney': (-33.8688, 151.2093),
    }
    
    print("\n  Haversine distances between cities:")
    pairs = [('nyc', 'la'), ('nyc', 'london'), ('tokyo', 'sydney'), ('london', 'tokyo')]
    for city1, city2 in pairs:
        lat1, lng1 = cities[city1]
        lat2, lng2 = cities[city2]
        dist = haversine_distance(lat1, lng1, lat2, lng2)
        print(f"    {city1} -> {city2}: {dist:.1f} km")
    
    print("\n  Distance between geohashes:")
    gh_pairs = [('dr5ru7', 'dr5ru6'), ('xn76ur', 'xn76us')]
    for gh1, gh2 in gh_pairs:
        dist = distance(gh1, gh2)
        print(f"    {gh1} -> {gh2}: {dist*1000:.1f} m")


def example_validation():
    """Example: Geohash validation."""
    print("\n" + "=" * 60)
    print("Geohash Validation")
    print("=" * 60)
    
    test_geohashes = [
        ('u4pruy', True, "Valid geohash"),
        ('U4PRUY', True, "Valid uppercase"),
        ('dr5ru7', True, "Valid NYC"),
        ('u4prui', False, "Invalid 'i'"),
        ('u4prua', False, "Invalid 'a'"),
        ('u4prul', False, "Invalid 'l'"),
        ('u4pruo', False, "Invalid 'o'"),
        ('', False, "Empty string"),
        ('123456', True, "Numeric valid"),
    ]
    
    print("\n  Validating geohashes:")
    for gh, expected, description in test_geohashes:
        result = is_valid(gh)
        status = "✓" if result == expected else "✗"
        print(f"    {status} '{gh}' ({description}): valid={result}")
    
    print("\n  Normalizing geohashes:")
    raw_geohashes = ['U4PRUY', '  dr5ru7  ', 'DR5RU7']
    for gh in raw_geohashes:
        normalized = validate(gh)
        print(f"    '{gh}' -> '{normalized}'")


def example_cell_info():
    """Example: Getting detailed cell information."""
    print("\n" + "=" * 60)
    print("Cell Information")
    print("=" * 60)
    
    geohashes = ['u4', 'u4pr', 'u4pruy', 'u4pruyd']
    
    print("\n  Cell details at different precisions:")
    for gh in geohashes:
        cell = get_cell(gh)
        print(f"\n    Geohash: {gh}")
        print(f"      Precision: {cell.precision}")
        print(f"      Center: ({cell.center[0]:.5f}, {cell.center[1]:.5f})")
        print(f"      Bounds:")
        print(f"        SW: ({cell.bounds.min_lat:.5f}, {cell.bounds.min_lng:.5f})")
        print(f"        NE: ({cell.bounds.max_lat:.5f}, {cell.bounds.max_lng:.5f})")
        print(f"      Size: {cell.width_km:.4f}km x {cell.height_km:.4f}km")
        print(f"      Area: ~{cell.width_km * cell.height_km:.4f}km²")


def example_hierarchy():
    """Example: Geohash hierarchy (parent/children)."""
    print("\n" + "=" * 60)
    print("Geohash Hierarchy")
    print("=" * 60)
    
    gh = 'u4pruy'
    
    print(f"\n  Geohash: {gh}")
    
    print("\n  Parent chain:")
    current = gh
    while current:
        parent_gh = parent(current)
        if parent_gh:
            print(f"    {current} -> parent: {parent_gh}")
        else:
            print(f"    {current} -> (no parent, at precision 1)")
        current = parent_gh
    
    print("\n  Children (precision +1):")
    children_gh = children('u4pru')
    print(f"    'u4pru' has {len(children_gh)} children:")
    for i, child in enumerate(children_gh[:8]):
        lat, lng = decode(child)
        print(f"      {child}: ({lat:.5f}, {lng:.5f})")
    print(f"    ... and {len(children_gh) - 8} more")


def example_expand():
    """Example: Expanding geohash for radius search."""
    print("\n" + "=" * 60)
    print("Geohash Expansion (Radius Search)")
    print("=" * 60)
    
    gh = 'dr5ru7'  # NYC
    
    print(f"\n  Center: {gh}")
    lat, lng = decode(gh)
    print(f"    Location: ({lat:.5f}, {lng:.5f})")
    
    print("\n  Expanding for different radii:")
    radii = [0.5, 1.0, 2.0, 5.0]  # km
    
    for radius in radii:
        expanded = expand(gh, radius)
        print(f"    {radius}km radius: {len(expanded)} geohashes")
        if len(expanded) <= 9:
            print(f"      {', '.join(expanded)}")
        else:
            print(f"      {', '.join(expanded[:5])}, ... ({len(expanded)-5} more)")
    
    print("\n  Note: This is useful for radius searches in databases!")
    print("  Instead of calculating distance for every point,")
    print("  filter by geohash prefix first, then calculate exact distances.")


def example_area_coverage():
    """Example: Covering an area with geohashes."""
    print("\n" + "=" * 60)
    print("Area Coverage")
    print("=" * 60)
    
    # Manhattan area (approximate)
    print("\n  Manhattan, NYC (approximate bounds):")
    sw_lat, sw_lng = 40.70, -74.02  # Southwest corner
    ne_lat, ne_lng = 40.80, -73.96  # Northeast corner
    
    print(f"    SW: ({sw_lat}, {sw_lng})")
    print(f"    NE: ({ne_lat}, {ne_lng})")
    
    for precision in [4, 5, 6]:
        geohashes = covers_area(sw_lat, sw_lng, ne_lat, ne_lng, precision)
        print(f"\n    Precision {precision}: {len(geohashes)} geohashes")
        if len(geohashes) <= 10:
            print(f"      {', '.join(geohashes)}")
        else:
            print(f"      {', '.join(geohashes[:5])}, ... ({len(geohashes)-5} more)")


def example_common_prefix():
    """Example: Finding common prefix for nearby locations."""
    print("\n" + "=" * 60)
    print("Common Prefix (Nearby Detection)")
    print("=" * 60)
    
    print("\n  Locations in same city:")
    
    # Multiple points in NYC
    nyc_locations = [
        (40.7128, -74.0060),  # Downtown
        (40.7484, -73.9857),  # Times Square
        (40.7589, -73.9851),  # Central Park South
    ]
    
    geohashes = [encode(lat, lng, 6) for lat, lng in nyc_locations]
    prefix = common_prefix(geohashes)
    
    print(f"    Geohashes: {geohashes}")
    print(f"    Common prefix: '{prefix}'")
    print(f"    Locations share precision {len(prefix)} area")
    
    print("\n  Locations in different continents:")
    world_geohashes = ['dr5ru7', 'xn76ur', 'r3gx2f']  # NYC, Tokyo, Sydney
    prefix = common_prefix(world_geohashes)
    print(f"    Geohashes: {world_geohashes}")
    print(f"    Common prefix: '{prefix}' (no overlap)")


def example_geopoint_geobounds():
    """Example: Using GeoPoint and GeoBounds classes."""
    print("\n" + "=" * 60)
    print("GeoPoint and GeoBounds Classes")
    print("=" * 60)
    
    print("\n  Creating GeoPoint objects:")
    nyc = GeoPoint(40.7128, -74.0060)
    la = GeoPoint(34.0522, -118.2437)
    
    print(f"    NYC: {nyc}")
    print(f"    LA: {la}")
    
    print("\n  Calculating distance between points:")
    dist = nyc.distance_to(la)
    print(f"    NYC to LA: {dist:.1f} km")
    
    print("\n  Creating GeoBounds:")
    bounds = GeoBounds(40.70, 40.80, -74.02, -73.96)
    print(f"    Manhattan bounds: {bounds}")
    print(f"    Center: {bounds.center}")
    print(f"    Width: {bounds.width:.3f}°")
    print(f"    Height: {bounds.height:.3f}°")
    
    print("\n  Testing containment:")
    test_points = [
        (40.75, -74.0, "Midtown"),
        (40.85, -74.0, "Outside (north)"),
        (40.75, -74.1, "Outside (west)"),
    ]
    
    for lat, lng, name in test_points:
        contained = bounds.contains(lat, lng)
        status = "inside" if contained else "outside"
        print(f"    {name} ({lat}, {lng}): {status}")


def example_real_world_use_cases():
    """Example: Real-world use cases."""
    print("\n" + "=" * 60)
    print("Real-World Use Cases")
    print("=" * 60)
    
    print("\n  1. Store Locator (find nearby stores):")
    print("     - User location: encode to geohash")
    print("     - Search: use prefix matching in database")
    print("     - Example: user at dr5ru7, search dr5*")
    
    print("\n  2. Delivery Zone Coverage:")
    print("     - Define zones with geohash prefixes")
    print("     - dr5 covers most of Manhattan")
    print("     - Quick zone membership check")
    
    print("\n  3. Spatial Indexing:")
    print("     - Use geohash as B-tree index")
    print("     - Prefix queries for range scans")
    print("     - Much faster than lat/lng bounds queries")
    
    print("\n  4. Location Sharing:")
    print("     - Share short geohash instead of coordinates")
    print("     - u4pruy (6 chars) vs 57.64911,10.40744 (14 chars)")
    print("     - Privacy: use lower precision for fuzzy location")
    
    print("\n  5. Geospatial Clustering:")
    print("     - Group points by geohash prefix")
    print("     - u4pruy and u4pruz cluster as 'u4pru'")
    print("     - Efficient heatmap generation")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("GEOHASH UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    print("\n  Geohash is a geographic encoding system that converts")
    print("  latitude/longitude coordinates into short alphanumeric strings.")
    print("\n  Key features:")
    print("    - Precision control (1-12 characters)")
    print("    - Hierarchical structure (prefixes)")
    print("    - Efficient spatial indexing")
    print("    - Neighbor detection")
    
    example_encoding()
    example_decoding()
    example_neighbors()
    example_distance()
    example_validation()
    example_cell_info()
    example_hierarchy()
    example_expand()
    example_area_coverage()
    example_common_prefix()
    example_geopoint_geobounds()
    example_real_world_use_cases()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\n  Tip: Use higher precision (8-10) for precise locations")
    print("  Use lower precision (4-6) for city/neighborhood level")


if __name__ == '__main__':
    main()