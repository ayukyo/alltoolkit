#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geographic Distance Utilities Examples
=====================================================
Practical usage examples for geo_distance_utils module.
"""

from mod import (
    haversine_distance,
    vincenty_distance,
    initial_bearing,
    final_bearing,
    midpoint_coordinate,
    destination_point,
    bounding_box,
    point_in_polygon,
    polygon_area_km2,
    interpolate_path,
    nearest_point_on_path,
    total_path_distance,
    decimal_to_dms,
    dms_to_decimal,
    coordinate_to_string,
    convert_distance,
    find_nearest,
    distances_to_all,
    within_radius,
    coordinate_to_string,
)


def example_basic_distances():
    """Basic distance calculations between cities."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Distance Calculations")
    print("=" * 60)
    
    # Major cities
    cities = {
        'Beijing': (39.9042, 116.4074),
        'Shanghai': (31.2304, 121.4737),
        'New York': (40.7128, -74.0060),
        'London': (51.5074, -0.1278),
        'Tokyo': (35.6762, 139.6503),
        'Sydney': (-33.8688, 151.2093),
    }
    
    # Calculate distances between Beijing and other cities
    beijing = cities['Beijing']
    print(f"\nDistances from Beijing ({coordinate_to_string(beijing)}):")
    
    for city, coord in cities.items():
        if city == 'Beijing':
            continue
        
        haversine = haversine_distance(beijing, coord)
        vincenty = vincenty_distance(beijing, coord)
        miles = convert_distance(haversine, 'km', 'miles')
        nautical = convert_distance(haversine, 'km', 'nautical')
        bearing = initial_bearing(beijing, coord)
        
        print(f"\n  {city} ({coordinate_to_string(coord)}):")
        print(f"    Haversine: {haversine:.2f} km")
        print(f"    Vincenty:  {vincenty:.2f} km")
        print(f"    Miles:     {miles:.2f} mi")
        print(f"    Nautical:  {nautical:.2f} nm")
        print(f"    Bearing:   {bearing:.2f}°")


def example_bearing_navigation():
    """Navigation with bearing and destination calculations."""
    print("\n" + "=" * 60)
    print("Example 2: Navigation - Bearings and Destinations")
    print("=" * 60)
    
    # Starting point: Beijing
    start = (39.9042, 116.4074)
    
    print(f"\nStarting point: {coordinate_to_string(start, format='dms')}")
    
    # Move in different directions
    directions = {
        'North': 0,
        'East': 90,
        'South': 180,
        'West': 270,
    }
    
    distance_km = 100
    
    for name, bearing in directions.items():
        dest = destination_point(start, bearing, distance_km)
        print(f"\n  {name} ({bearing}°) for {distance_km} km:")
        print(f"    Destination: {coordinate_to_string(dest)}")
    
    # Calculate bearing to Shanghai
    shanghai = (31.2304, 121.4737)
    bearing = initial_bearing(start, shanghai)
    print(f"\n  Bearing to Shanghai: {bearing:.2f}°")


def example_midpoint():
    """Calculate midpoint between cities."""
    print("\n" + "=" * 60)
    print("Example 3: Midpoint Calculation")
    print("=" * 60)
    
    beijing = (39.9042, 116.4074)
    shanghai = (31.2304, 121.4737)
    
    mid = midpoint_coordinate(beijing, shanghai)
    
    print(f"\nBeijing:  {coordinate_to_string(beijing, format='dms')}")
    print(f"Shanghai: {coordinate_to_string(shanghai, format='dms')}")
    print(f"\nMidpoint: {coordinate_to_string(mid, format='dms')}")
    print(f"Decimal:  {mid[0]:.4f}, {mid[1]:.4f}")


def example_bounding_box():
    """Bounding box for radius search."""
    print("\n" + "=" * 60)
    print("Example 4: Bounding Box for Radius Search")
    print("=" * 60)
    
    center = (39.9042, 116.4074)  # Beijing
    radius_km = 50
    
    bbox = bounding_box(center, radius_km)
    min_coord, max_coord = bbox
    
    print(f"\nCenter: {coordinate_to_string(center)}")
    print(f"Radius: {radius_km} km")
    print(f"\nBounding box:")
    print(f"  SW corner: {coordinate_to_string(min_coord)}")
    print(f"  NE corner: {coordinate_to_string(max_coord)}")
    
    # Check if a point is within the box
    test_point = (39.9, 116.5)
    lat_in = min_coord[0] <= test_point[0] <= max_coord[0]
    lng_in = min_coord[1] <= test_point[1] <= max_coord[1]
    
    print(f"\nPoint {coordinate_to_string(test_point)} within box: {lat_in and lng_in}")


def example_polygon():
    """Polygon operations - point in polygon and area."""
    print("\n" + "=" * 60)
    print("Example 5: Polygon Operations")
    print("=" * 60)
    
    # Polygon around central Beijing (rough rectangle)
    polygon = [
        (39.8, 116.2),   # SW
        (39.8, 116.6),   # SE
        (40.0, 116.6),   # NE
        (40.0, 116.2),   # NW
    ]
    
    print(f"\nPolygon vertices:")
    for i, coord in enumerate(polygon):
        print(f"  {i+1}: {coordinate_to_string(coord)}")
    
    # Calculate area
    area = polygon_area_km2(polygon)
    print(f"\nPolygon area: {area:.2f} km²")
    
    # Test points inside/outside
    test_points = [
        (39.9, 116.4),   # Inside (central Beijing)
        (39.85, 116.3),  # Inside
        (40.5, 116.4),   # Outside (north)
        (39.9, 117.0),   # Outside (east)
    ]
    
    print("\nPoint-in-polygon test:")
    for point in test_points:
        inside = point_in_polygon(point, polygon)
        status = "INSIDE" if inside else "OUTSIDE"
        print(f"  {coordinate_to_string(point)}: {status}")


def example_path():
    """Path interpolation and distance."""
    print("\n" + "=" * 60)
    print("Example 6: Path Operations")
    print("=" * 60)
    
    # Flight path: Beijing → Shanghai
    beijing = (39.9042, 116.4074)
    shanghai = (31.2304, 121.4737)
    
    print(f"\nFlight path: Beijing → Shanghai")
    
    # Total distance
    total = total_path_distance([beijing, shanghai])
    print(f"Total distance: {total:.2f} km ({convert_distance(total, 'km', 'miles'):.2f} miles)")
    
    # Interpolate path with 5 intermediate points
    points = interpolate_path(beijing, shanghai, 5)
    
    print(f"\nInterpolated waypoints (5 intermediate points):")
    for i, point in enumerate(points):
        label = "Start" if i == 0 else "End" if i == len(points) - 1 else f"WP{i}"
        print(f"  {label}: {coordinate_to_string(point)}")
    
    # Find nearest point on path
    nanjing = (32.0603, 118.7969)
    nearest, dist, idx = nearest_point_on_path(nanjing, points)
    
    print(f"\nNearest point to Nanjing on flight path:")
    print(f"  Nanjing: {coordinate_to_string(nanjing)}")
    print(f"  Nearest waypoint: {coordinate_to_string(nearest)}")
    print(f"  Distance: {dist:.2f} km")


def example_coordinate_formats():
    """Coordinate format conversions."""
    print("\n" + "=" * 60)
    print("Example 7: Coordinate Format Conversions")
    print("=" * 60)
    
    coord = (39.9042, 116.4074)  # Beijing
    
    print(f"\nOriginal: {coord[0]}, {coord[1]}")
    
    # Decimal to DMS
    dms = decimal_to_dms(coord)
    print(f"\nDMS format:")
    print(f"  Latitude:  {dms['lat']['degrees']}°{dms['lat']['minutes']}'{dms['lat']['seconds']:.2f}\"{dms['lat']['direction']}")
    print(f"  Longitude: {dms['lng']['degrees']}°{dms['lng']['minutes']}'{dms['lng']['seconds']:.2f}\"{dms['lng']['direction']}")
    
    # String formats
    print(f"\nString formats:")
    print(f"  Decimal: {coordinate_to_string(coord, format='decimal')}")
    print(f"  DM:      {coordinate_to_string(coord, format='dm')}")
    print(f"  DMS:     {coordinate_to_string(coord, format='dms')}")
    
    # DMS back to decimal
    back_decimal = dms_to_decimal(dms['lat'], dms['lng'])
    print(f"\nBack to decimal: {back_decimal[0]:.4f}, {back_decimal[1]:.4f}")


def example_batch_operations():
    """Batch operations for multiple points."""
    print("\n" + "=" * 60)
    print("Example 8: Batch Operations")
    print("=" * 60)
    
    # Reference point: Beijing
    center = (39.9042, 116.4074)
    
    # Cities to check
    candidates = [
        (40.0, 116.4),   # Beijing area
        (31.2, 121.5),   # Shanghai
        (35.7, 139.7),   # Tokyo
        (51.5, -0.1),    # London
    ]
    
    city_names = ['Beijing area', 'Shanghai', 'Tokyo', 'London']
    
    print(f"\nCenter point: {coordinate_to_string(center)}")
    print("\nCandidate cities:")
    
    for i, (coord, name) in enumerate(zip(candidates, city_names)):
        print(f"  {i}: {name} - {coordinate_to_string(coord)}")
    
    # Find nearest
    idx, dist, coord = find_nearest(center, candidates)
    print(f"\nNearest: {city_names[idx]} at {dist:.2f} km")
    
    # All distances
    distances = distances_to_all(center, candidates)
    print(f"\nAll distances:")
    for i, (d, name) in enumerate(zip(distances, city_names)):
        print(f"  {name}: {d:.2f} km ({convert_distance(d, 'km', 'miles'):.2f} miles)")
    
    # Within radius (1000 km)
    radius_km = 1000
    results = within_radius(center, candidates, radius_km)
    
    print(f"\nCities within {radius_km} km:")
    for idx, dist, coord in results:
        print(f"  {city_names[idx]}: {dist:.2f} km")


def example_unit_conversions():
    """Distance unit conversions."""
    print("\n" + "=" * 60)
    print("Example 9: Unit Conversions")
    print("=" * 60)
    
    distance_km = 1000
    
    print(f"\nOriginal: {distance_km} km")
    print(f"\nConverted:")
    print(f"  Miles:     {convert_distance(distance_km, 'km', 'miles'):.2f} mi")
    print(f"  Nautical:  {convert_distance(distance_km, 'km', 'nautical'):.2f} nm")
    print(f"  Meters:    {convert_distance(distance_km, 'km', 'm'):.2f} m")
    
    # Reverse conversions
    miles = 500
    print(f"\n{miles} miles = {convert_distance(miles, 'miles', 'km'):.2f} km")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit Geographic Distance Utils - Examples")
    print("=" * 60)
    
    example_basic_distances()
    example_bearing_navigation()
    example_midpoint()
    example_bounding_box()
    example_polygon()
    example_path()
    example_coordinate_formats()
    example_batch_operations()
    example_unit_conversions()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()