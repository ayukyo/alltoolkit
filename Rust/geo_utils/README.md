# Geo Utils

A comprehensive geographic coordinate utility library for Rust. Provides distance calculation, bearing, destination point, GeoHash encoding/decoding, bounding box, and polygon containment checks. **Zero external dependencies** - uses only Rust standard library.

## Features

- **Coordinate Representation**: Latitude/longitude with validation and conversion
- **Haversine Distance**: Great-circle distance between two points
- **Bearing Calculation**: Initial and final bearing between points
- **Destination Point**: Calculate endpoint from start, bearing, and distance
- **Midpoint**: Find the midpoint along a great-circle path
- **Bounding Box**: Generate bounds around a center point
- **GeoHash**: Encode and decode up to 12-character precision
- **Polygon Operations**: Area, perimeter, centroid, containment check
- **Path Operations**: Distance, interpolation, closest point
- **Rhumb Line**: Alternative navigation calculations
- **Multiple Units**: Kilometers, meters, miles, nautical miles

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
geo_utils = "0.1.0"
```

Or use directly:

```rust
use geo_utils::{Coordinate, GeoUtils, BoundingBox, DistanceUnit};
```

## Quick Start

```rust
use geo_utils::{Coordinate, GeoUtils};

// Create coordinates
let ny = Coordinate::new(40.7128, -74.0060);  // New York
let london = Coordinate::new(51.5074, -0.1278); // London

// Calculate distance
let distance = GeoUtils::haversine_distance(&ny, &london);
println!("Distance: {:.2} km", distance); // ~5570 km

// Calculate bearing
let bearing = GeoUtils::bearing(&ny, &london);
println!("Bearing: {:.2}° ({})", bearing, GeoUtils::bearing_to_cardinal(bearing));

// Encode to GeoHash
let geohash = GeoUtils::encode_geohash(&ny, 8);
println!("GeoHash: {}", geohash); // "dr5ru7j6"
```

## API Reference

### Coordinate

```rust
// Create coordinate
let coord = Coordinate::new(latitude, longitude);

// From degrees, minutes, seconds
let coord = Coordinate::from_dms(40, 42, 46.8, 'N', 74, 0, 21.6, 'W');

// Validation
coord.is_valid()

// Conversion
coord.to_dms_string()  // "40°42'46.80\"N 74°0'21.60\"W"
coord.to_dd_string(4)  // "40.7128°, -74.0060°"

// Operations
coord.distance_to(&other)    // Haversine distance
coord.bearing_to(&other)     // Bearing angle
coord.to_geohash(8)          // GeoHash encoding
```

### GeoUtils

```rust
// Distance calculations
GeoUtils::haversine_distance(&from, &to)
GeoUtils::distance(&from, &to, DistanceUnit::Miles)
GeoUtils::rhumb_distance(&from, &to)

// Bearing calculations
GeoUtils::bearing(&from, &to)
GeoUtils::final_bearing(&from, &to)
GeoUtils::rhumb_bearing(&from, &to)
GeoUtils::bearing_to_cardinal(52.0)  // "NE"

// Path operations
GeoUtils::midpoint(&from, &to)
GeoUtils::destination(&from, bearing, distance_km)
GeoUtils::interpolate(&from, &to, num_points)
GeoUtils::path_distance(&path)

// GeoHash operations
GeoUtils::encode_geohash(&coord, precision)
GeoUtils::decode_geohash(&hash)
GeoUtils::geohash_bounds(&hash)
GeoUtils::geohash_neighbors(&hash)

// Polygon operations
GeoUtils::point_in_polygon(&point, &polygon)
GeoUtils::polygon_area(&polygon)
GeoUtils::polygon_perimeter(&polygon)
GeoUtils::polygon_centroid(&polygon)
```

### BoundingBox

```rust
// Create bounding box
let bbox = BoundingBox::from_center_radius(&center, radius_km);
let bbox = BoundingBox::from_corners(&corner1, &corner2);

// Operations
bbox.contains(&coord)
bbox.center()
bbox.width()
bbox.height()
bbox.corners()
bbox.expand(factor)
bbox.merge(&other)

// Utility
GeoUtils::bounding_boxes_intersect(&a, &b)
```

## Examples

### Calculate Route Distance

```rust
let route = vec![
    Coordinate::new(40.7128, -74.0060),  // New York
    Coordinate::new(37.7749, -122.4194),  // San Francisco
    Coordinate::new(34.0522, -118.2437),  // Los Angeles
];
let total = GeoUtils::path_distance(&route);
println!("Total route: {:.2} km", total);
```

### Find Points in Polygon

```rust
let area = vec![
    Coordinate::new(35.0, -120.0),
    Coordinate::new(35.0, -117.0),
    Coordinate::new(38.0, -117.0),
    Coordinate::new(38.0, -120.0),
];

let point = Coordinate::new(36.5, -118.5);
if GeoUtils::point_in_polygon(&point, &area) {
    println!("Point is inside the area!");
}
```

### GeoHash Neighbor Search

```rust
let hash = "dr5ru7j6";
let neighbors = GeoUtils::geohash_neighbors(hash).unwrap();
for neighbor in &neighbors {
    if !neighbor.is_empty() {
        let coord = GeoUtils::decode_geohash(neighbor).unwrap();
        println!("Neighbor {}: {}", neighbor, coord);
    }
}
```

## Test Coverage

45+ unit tests covering:
- Coordinate creation and validation
- Haversine distance calculation
- Bearing calculation (initial and final)
- Midpoint and destination point
- Bounding box operations
- GeoHash encoding and decoding
- Polygon containment, area, perimeter
- Path interpolation and distance
- Rhumb line calculations
- Unit conversions

## Performance

- All calculations use pure mathematics (no external dependencies)
- Memory-efficient with no heap allocations for basic operations
- Suitable for real-time applications and GIS systems

## License

MIT License - Free for commercial and personal use.

## Author

AllToolkit - Comprehensive collection of utility libraries for developers.