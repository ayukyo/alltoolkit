//! # Geo Utils Examples
//!
//! Demonstrates usage of the geographic coordinate utility library.

use geo_utils::{Coordinate, GeoUtils, BoundingBox, DistanceUnit};

fn main() {
    println!("=== Geo Utils Examples ===\n");

    // Example 1: Basic coordinate operations
    println!("1. Basic Coordinate Operations:");
    let ny = Coordinate::new(40.7128, -74.0060);
    let london = Coordinate::new(51.5074, -0.1278);
    let sf = Coordinate::new(37.7749, -122.4194);
    let la = Coordinate::new(34.0522, -118.2437);

    println!("  New York: {}", ny);
    println!("  London: {}", london);
    println!("  San Francisco: {}", sf);
    println!("  Los Angeles: {}", la);

    // DMS format
    println!("  New York (DMS): {}", ny.to_dms_string());

    println!();

    // Example 2: Distance calculations
    println!("2. Distance Calculations:");
    let distance_km = GeoUtils::haversine_distance(&ny, &london);
    println!("  New York to London: {:.2} km", distance_km);
    println!("  New York to London: {:.2} miles", GeoUtils::distance(&ny, &london, DistanceUnit::Miles));
    println!("  New York to London: {:.2} nm", GeoUtils::distance(&ny, &london, DistanceUnit::NauticalMiles));

    let sf_to_la = GeoUtils::haversine_distance(&sf, &la);
    println!("  San Francisco to Los Angeles: {:.2} km", sf_to_la);

    println!();

    // Example 3: Bearing and direction
    println!("3. Bearing and Direction:");
    let bearing_ny_london = GeoUtils::bearing(&ny, &london);
    println!("  New York to London bearing: {:.2}° ({})", bearing_ny_london, GeoUtils::bearing_to_cardinal(bearing_ny_london));

    let bearing_sf_la = GeoUtils::bearing(&sf, &la);
    println!("  San Francisco to Los Angeles bearing: {:.2}° ({})", bearing_sf_la, GeoUtils::bearing_to_cardinal(bearing_sf_la));

    println!();

    // Example 4: Destination point
    println!("4. Destination Point:");
    println!("  Starting from New York, traveling NE 1000 km:");
    let dest = GeoUtils::destination(&ny, 52.0, 1000.0);
    println!("  Destination: {}", dest);
    println!("  Distance traveled: {:.2} km", ny.distance_to(&dest));

    println!();

    // Example 5: Midpoint
    println!("5. Midpoint Calculation:");
    let mid = GeoUtils::midpoint(&ny, &london);
    println!("  Midpoint between NY and London: {}", mid);

    println!();

    // Example 6: Bounding box
    println!("6. Bounding Box:");
    let bbox = BoundingBox::from_center_radius(&sf, 50.0);
    println!("  50km radius around San Francisco:");
    println!("  {}", bbox);
    println!("  Contains SF: {}", bbox.contains(&sf));
    println!("  Contains LA: {}", bbox.contains(&la));

    println!();

    // Example 7: GeoHash
    println!("7. GeoHash Encoding/Decoding:");
    let geohash_ny = GeoUtils::encode_geohash(&ny, 8);
    println!("  New York GeoHash (8 chars): {}", geohash_ny);

    let geohash_london = GeoUtils::encode_geohash(&london, 8);
    println!("  London GeoHash (8 chars): {}", geohash_london);

    let decoded = GeoUtils::decode_geohash(&geohash_ny).unwrap();
    println!("  Decoded NY GeoHash: {}", decoded);

    let bounds = GeoUtils::geohash_bounds(&geohash_ny).unwrap();
    println!("  GeoHash bounds: {}", bounds);

    let neighbors = GeoUtils::geohash_neighbors(&geohash_ny).unwrap();
    println!("  Neighbors: {:?}", neighbors);

    println!();

    // Example 8: Polygon operations
    println!("8. Polygon Operations:");
    let polygon = vec![
        Coordinate::new(35.0, -120.0),
        Coordinate::new(35.0, -117.0),
        Coordinate::new(38.0, -117.0),
        Coordinate::new(38.0, -120.0),
    ];

    println!("  Polygon vertices: {:?}", polygon);

    let area = GeoUtils::polygon_area(&polygon);
    println!("  Polygon area: {:.2} km²", area);

    let perimeter = GeoUtils::polygon_perimeter(&polygon);
    println!("  Polygon perimeter: {:.2} km", perimeter);

    let centroid = GeoUtils::polygon_centroid(&polygon).unwrap();
    println!("  Polygon centroid: {}", centroid);

    // Point in polygon
    let inside = Coordinate::new(36.5, -118.5);
    let outside = Coordinate::new(30.0, -115.0);
    println!("  {} is inside: {}", inside, GeoUtils::point_in_polygon(&inside, &polygon));
    println!("  {} is inside: {}", outside, GeoUtils::point_in_polygon(&outside, &polygon));

    println!();

    // Example 9: Interpolation
    println!("9. Path Interpolation:");
    println!("  Interpolating 3 points between NY and London:");
    let points = GeoUtils::interpolate(&ny, &london, 3);
    for (i, p) in points.iter().enumerate() {
        println!("    Point {}: {}", i + 1, p);
    }

    println!();

    // Example 10: Rhumb line
    println!("10. Rhumb Line Navigation:");
    let rhumb_bearing = GeoUtils::rhumb_bearing(&ny, &la);
    let rhumb_distance = GeoUtils::rhumb_distance(&ny, &la);
    println!("  NY to LA rhumb bearing: {:.2}° ({})", rhumb_bearing, GeoUtils::bearing_to_cardinal(rhumb_bearing));
    println!("  NY to LA rhumb distance: {:.2} km", rhumb_distance);

    println!();

    // Example 11: Coordinate from DMS
    println!("11. Coordinate from DMS:");
    // Mount Everest: 27°59'17" N, 86°55'31" E
    let everest = Coordinate::from_dms(27, 59, 17.0, 'N', 86, 55, 31.0, 'E');
    println!("  Mount Everest: {}", everest);
    println!("  Latitude DMS: {:?}", everest.lat_to_dms());
    println!("  Longitude DMS: {:?}", everest.lon_to_dms());

    println!();

    // Example 12: Path distance
    println!("12. Path Distance:");
    let route = vec![
        Coordinate::new(40.7128, -74.0060),  // NY
        Coordinate::new(37.7749, -122.4194),  // SF
        Coordinate::new(34.0522, -118.2437),  // LA
    ];
    let total_distance = GeoUtils::path_distance(&route);
    println!("  NY → SF → LA total: {:.2} km", total_distance);

    println!("\n=== All examples completed! ===");
}