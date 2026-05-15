//! # Geo Utils Examples

use geo_utils::{Coordinate, GeoUtils, BoundingBox, DistanceUnit};

fn main() {
    println!("=== Geo Utils Examples ===\n");

    // Example 1: Basic coordinate operations
    println!("1. Basic Coordinate Operations:");
    let ny = Coordinate::new(40.7128, -74.0060);
    let london = Coordinate::new(51.5074, -0.1278);
    println!("  New York: {}", ny);
    println!("  London: {}", london);
    println!("  New York (DMS): {}", ny.to_dms_string());
    println!();

    // Example 2: Distance calculations
    println!("2. Distance Calculations:");
    let distance_km = GeoUtils::haversine_distance(&ny, &london);
    println!("  New York to London: {:.2} km", distance_km);
    println!("  New York to London: {:.2} miles", GeoUtils::distance(&ny, &london, DistanceUnit::Miles));
    println!();

    // Example 3: Bearing and direction
    println!("3. Bearing and Direction:");
    let bearing = GeoUtils::bearing(&ny, &london);
    println!("  NY to London bearing: {:.2}° ({})", bearing, GeoUtils::bearing_to_cardinal(bearing));
    println!();

    // Example 4: GeoHash
    println!("4. GeoHash Encoding/Decoding:");
    let geohash = GeoUtils::encode_geohash(&ny, 8);
    println!("  New York GeoHash: {}", geohash);
    let decoded = GeoUtils::decode_geohash(&geohash).unwrap();
    println!("  Decoded: {}", decoded);
    println!();

    // Example 5: Bounding Box
    println!("5. Bounding Box:");
    let bbox = BoundingBox::from_center_radius(&ny, 50.0);
    println!("  50km radius around NY: {}", bbox);
    println!();

    // Example 6: Polygon
    println!("6. Polygon Operations:");
    let polygon = vec![
        Coordinate::new(35.0, -120.0),
        Coordinate::new(35.0, -117.0),
        Coordinate::new(38.0, -117.0),
        Coordinate::new(38.0, -120.0),
    ];
    println!("  Area: {:.2} km²", GeoUtils::polygon_area(&polygon));
    println!("  Perimeter: {:.2} km", GeoUtils::polygon_perimeter(&polygon));
    println!();

    println!("=== All examples completed! ===");
}