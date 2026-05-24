# Haversine Utilities for R

A comprehensive, zero-dependency R library for calculating geographic distances using the Haversine formula.

## Features

- **Distance Calculation**: Calculate great-circle distance between two points on Earth
- **Bearing**: Get the initial bearing from one point to another
- **Midpoint**: Find the geographic midpoint between two coordinates
- **Destination Point**: Calculate destination given start, bearing, and distance
- **Nearest Point**: Find the closest point from a list of candidates
- **Radius Search**: Find all points within a given radius
- **Bounding Box**: Calculate bounding box for efficient database queries
- **Path Distance**: Calculate total distance along a multi-point path
- **Coordinate Validation**: Validate latitude/longitude values
- **Batch Operations**: Vectorized calculations for multiple point pairs

## Installation

Simply source the file:

```r
source("haversine.R")
```

## Quick Start

```r
source("haversine.R")

# Distance between New York and Los Angeles
dist <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "km")
print(dist)  # ~3944 km
```

## API Reference

### Distance Functions

#### `haversine_distance(lat1, lon1, lat2, lon2, unit = "km")`
Calculate distance between two points.

```r
# Kilometers
haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "km")

# Miles
haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "miles")

# Meters
haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "meters")
```

#### `haversine_distance_batch(points, unit = "km")`
Calculate distances for multiple point pairs.

```r
points <- data.frame(
  lat1 = c(40.7128, 51.5074),
  lon1 = c(-74.0060, -0.1278),
  lat2 = c(34.0522, 48.8566),
  lon2 = c(-118.2437, 2.3522)
)
distances <- haversine_distance_batch(points, "km")
```

### Search Functions

#### `find_nearest(ref_lat, ref_lon, candidates, unit = "km")`
Find nearest point from candidates.

```r
candidates <- data.frame(
  lat = c(34.05, 40.71, 41.87),
  lon = c(-118.24, -74.00, -87.62),
  name = c("LA", "NYC", "Chicago")
)
nearest <- find_nearest(41.87, -87.62, candidates, "km")
print(nearest$name)  # "Chicago"
```

#### `within_radius(ref_lat, ref_lon, candidates, radius, unit = "km")`
Find all points within a radius.

```r
nearby <- within_radius(40.71, -74.00, candidates, 1500, "km")
```

### Geographic Functions

#### `bearing(lat1, lon1, lat2, lon2)`
Get initial bearing in degrees (0-360).

```r
brng <- bearing(40.7128, -74.0060, 34.0522, -118.2437)
# ~273° (approximately West)
```

#### `bearing_to_compass(bearing)`
Convert bearing to compass direction.

```r
bearing_to_compass(273)  # "W"
```

#### `midpoint(lat1, lon1, lat2, lon2)`
Calculate geographic midpoint.

```r
mid <- midpoint(40.7128, -74.0060, 34.0522, -118.2437)
print(mid$lat, mid$lon)
```

#### `destination_point(lat, lon, bearing, distance, unit = "km")`
Calculate destination from start point, bearing, and distance.

```r
dest <- destination_point(40.7128, -74.0060, 45, 100, "km")
# 100 km northeast from NYC
```

#### `bounding_box(lat, lon, radius, unit = "km")`
Get bounding box for database queries.

```r
bbox <- bounding_box(40.7128, -74.0060, 50, "km")
# Use in SQL: WHERE lat BETWEEN bbox$min_lat AND bbox$max_lat
```

#### `path_distance(path, unit = "km")`
Calculate total distance of a path.

```r
trip <- data.frame(
  lat = c(40.71, 41.87, 34.05),
  lon = c(-74.00, -87.62, -118.24)
)
total <- path_distance(trip, "km")
```

### Utility Functions

#### `degrees_to_radians(degrees)` / `radians_to_degrees(radians)`
Convert between degrees and radians.

#### `is_valid_latitude(lat)` / `is_valid_longitude(lon)`
Validate coordinates.

```r
is_valid_latitude(45)     # TRUE
is_valid_latitude(91)    # FALSE
is_valid_longitude(180)   # TRUE
is_valid_longitude(181)   # FALSE
```

#### `normalize_longitude(lon)`
Normalize longitude to -180 to 180 range.

```r
normalize_longitude(270)  # -90
normalize_longitude(-270) # 90
```

## Constants

- `EARTH_RADIUS_KM`: 6371.0 km
- `EARTH_RADIUS_MILES`: 3958.8 miles
- `EARTH_RADIUS_METERS`: 6371000.0 meters

## Testing

Run the test suite:

```r
Rscript test_haversine.R
```

## Examples

Run the examples:

```r
Rscript examples.R
```

## Use Cases

1. **Store Locator**: Find nearest store location
2. **Delivery Routes**: Calculate distances between stops
3. **Geofencing**: Check if points are within a zone
4. **Navigation**: Calculate bearing and destination
5. **Database Optimization**: Use bounding box to narrow queries

## Algorithm

Uses the Haversine formula to calculate great-circle distance:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × arcsin(√a)
d = R × c
```

Where R is Earth's radius (6371 km).

## License

MIT License - Free for personal and commercial use.