# Geo Utils

A comprehensive geographic coordinate utility library for Rust. Zero external dependencies.

## Features

- Haversine distance calculation
- Bearing and direction
- Destination point calculation
- GeoHash encoding/decoding
- Bounding box generation
- Polygon containment check

## Usage

```rust
use geo_utils::{Coordinate, GeoUtils};

let ny = Coordinate::new(40.7128, -74.0060);
let london = Coordinate::new(51.5074, -0.1278);

let distance = GeoUtils::haversine_distance(&ny, &london);
println!("Distance: {:.2} km", distance); // ~5570 km

let bearing = GeoUtils::bearing(&ny, &london);
println!("Bearing: {:.2}° ({})", bearing, GeoUtils::bearing_to_cardinal(bearing));
```

## Test Coverage

12 unit tests covering all core functions.

## License

MIT