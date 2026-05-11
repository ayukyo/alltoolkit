# geo_distance_utils

Comprehensive geographic distance calculation utilities for Go with zero external dependencies.

## Features

- **Distance Calculations**
  - Haversine distance (spherical Earth approximation)
  - Vincenty distance (ellipsoidal Earth, WGS-84 - more accurate)
  - Support for multiple units: km, m, miles, nautical miles

- **Bearing & Direction**
  - Initial bearing (azimuth) calculation
  - Final bearing calculation

- **Coordinate Operations**
  - Midpoint calculation
  - Destination point from start + bearing + distance
  - Coordinate validation and normalization
  - DMS (degrees-minutes-seconds) conversions

- **Polygon Operations**
  - Point-in-polygon detection (ray casting algorithm)
  - Polygon area calculation (spherical Earth approximation)
  - Bounding box for radius searches

- **Path Operations**
  - Great circle path interpolation
  - Total path distance
  - Nearest point on path

- **Batch Operations**
  - Find nearest candidate
  - Distances to all targets
  - Points within radius

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/geo_distance_utils"
```

## Quick Start

```go
package main

import (
    "fmt"
    geo "github.com/ayukyo/alltoolkit/Go/geo_distance_utils"
)

func main() {
    // Beijing and Shanghai coordinates
    beijing := geo.Coordinate{Lat: 39.9042, Lon: 116.4074}
    shanghai := geo.Coordinate{Lat: 31.2304, Lon: 121.4737}

    // Calculate distance
    dist, _ := geo.HaversineDistance(beijing, shanghai, geo.UnitKM)
    fmt.Printf("Distance: %.2f km\n", dist)

    // Get bearing
    bearing := geo.InitialBearing(beijing, shanghai)
    fmt.Printf("Initial bearing: %.2f°\n", bearing)

    // Get midpoint
    mid := geo.Midpoint(beijing, shanghai)
    fmt.Printf("Midpoint: %.4f, %.4f\n", mid.Lat, mid.Lon)
}
```

## Core Types

```go
// Geographic coordinate
type Coordinate struct {
    Lat float64
    Lon float64
}

// Distance units
type DistanceUnit string
const (
    UnitKM       DistanceUnit = "km"
    UnitM        DistanceUnit = "m"
    UnitMiles    DistanceUnit = "miles"
    UnitNautical DistanceUnit = "nautical"
)

// Calculation methods
type Method string
const (
    MethodHaversine Method = "haversine"
    MethodVincenty  Method = "vincenty"
)
```

## Usage Examples

### Distance Calculation

```go
c1 := geo.Coordinate{Lat: 39.9042, Lon: 116.4074}
c2 := geo.Coordinate{Lat: 31.2304, Lon: 121.4737}

// Haversine (spherical Earth)
distKM, _ := geo.HaversineDistance(c1, c2, geo.UnitKM)

// Vincenty (ellipsoidal Earth - more accurate)
distKM2, _ := geo.VincentyDistance(c1, c2, geo.UnitKM)

// Different units
distMiles, _ := geo.HaversineDistance(c1, c2, geo.UnitMiles)
distNautical, _ := geo.HaversineDistance(c1, c2, geo.UnitNautical)
distMeters, _ := geo.HaversineDistance(c1, c2, geo.UnitM)
```

### Bearing

```go
// Initial bearing (from start to end)
bearing := geo.InitialBearing(beijing, shanghai)

// Final bearing (at destination point)
final := geo.FinalBearing(beijing, shanghai)
```

### Destination Point

```go
start := geo.Coordinate{Lat: 0, Lon: 0}

// 100 km east
dest := geo.DestinationPoint(start, 90, 100)
// Result: approximately (0, 0.9°)

// 111 km north (about 1 degree)
dest := geo.DestinationPoint(start, 0, 111.19)
// Result: approximately (1, 0)
```

### Bounding Box

```go
center := geo.Coordinate{Lat: 39.9, Lon: 116.4}
bounds := geo.BoundingBox(center, 50) // 50 km radius

// bounds contains MinLat, MaxLat, MinLon, MaxLon
// Use for SQL queries: WHERE lat BETWEEN bounds.MinLat AND bounds.MaxLat
```

### Point in Polygon

```go
polygon := []geo.Coordinate{
    {Lat: 39, Lon: 116},
    {Lat: 40, Lon: 116},
    {Lat: 40, Lon: 117},
    {Lat: 39, Lon: 117},
}

point := geo.Coordinate{Lat: 39.5, Lon: 116.5}
inside := geo.PointInPolygon(point, polygon) // true

outside := geo.Coordinate{Lat: 38, Lon: 115}
geo.PointInPolygon(outside, polygon) // false
```

### Path Operations

```go
path := []geo.Coordinate{
    {Lat: 0, Lon: 0},
    {Lat: 0, Lon: 10},
    {Lat: 10, Lon: 10},
}

// Total distance
total, _ := geo.TotalPathDistance(path, geo.UnitKM)

// Interpolate points
points := geo.InterpolatePath(path[0], path[2], 5) // 6 points

// Find nearest point on path
point := geo.Coordinate{Lat: 1, Lon: 5}
result, _ := geo.NearestPointOnPath(point, path)
```

### Batch Operations

```go
point := geo.Coordinate{Lat: 39, Lon: 116}
candidates := []geo.Coordinate{
    {Lat: 40, Lon: 116},
    {Lat: 35, Lon: 117},
    {Lat: 30, Lon: 120},
}

// Find nearest
nearest, _ := geo.FindNearest(point, candidates, geo.UnitKM)

// All distances
dists, _ := geo.DistancesToAll(point, candidates, geo.UnitKM)

// Within radius (150 km)
within, _ := geo.WithinRadius(point, candidates, 150, geo.UnitKM)
```

### Coordinate Formats

```go
coord := geo.Coordinate{Lat: 39.9042, Lon: 116.4074}

// Decimal to DMS
dms := geo.DecimalToDMS(coord.Lat, coord.Lon)
// dms.Lat.Degrees=39, Minutes=54, Seconds=15.12, Direction="N"
// dms.Lon.Degrees=116, Minutes=24, Seconds=26.64, Direction="E"

// DMS to decimal
decimal := geo.DMSToDecimal(dms.Lat, dms.Lon)

// String formatting
str := geo.CoordinateToString(coord, "decimal", 4)
// "39.9042°N, 116.4074°E"

str := geo.CoordinateToString(coord, "dms", 0)
// "39°54'15.1"N, 116°24'26.6"E"
```

### Unit Conversions

```go
km := 100.0

miles := geo.ConvertKMToMiles(km)       // 62.14
nautical := geo.ConvertKMToNautical(km) // 54.00
meters := geo.ConvertKMToM(km)          // 100000

// Generic conversion
dist, _ := geo.ConvertDistance(100, geo.UnitKM, geo.UnitMiles)
```

## Constants

```go
// Earth radii
geo.EarthRadiusKM       = 6371.0     // km
geo.EarthRadiusM        = 6371000.0  // m
geo.EarthRadiusMiles    = 3958.8     // miles
geo.EarthRadiusNautical = 3440.065   // nautical miles

// WGS-84 ellipsoid parameters
geo.WGS84SemiMajor  = 6378137.0            // m
geo.WGS84SemiMinor  = 6356752.314245       // m
geo.WGS84Flattening = 1/298.257223563

// Conversion factors
geo.KMToMiles    = 0.621371
geo.KMToNautical = 0.539957
```

## Algorithm Details

### Haversine Formula

The Haversine formula calculates the great-circle distance between two points on a sphere:

```
a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
c = 2 * atan2(√a, √(1-a))
d = R * c
```

Time complexity: O(1)
Accuracy: ±0.5% (assumes spherical Earth)

### Vincenty Formula

Vincenty's formulae calculate distance on an ellipsoid (WGS-84):

- Iterative solution using reduced latitudes
- More accurate than Haversine (±1m accuracy)
- May not converge for nearly antipodal points
- Time complexity: O(n) where n ≈ 20-200 iterations

## Performance

Benchmarks on typical hardware:

| Operation | Time |
|-----------|------|
| HaversineDistance | ~200 ns |
| VincentyDistance | ~50 μs |
| PointInPolygon (4 vertices) | ~400 ns |
| FindNearest (1000 points) | ~200 μs |

## Test Coverage

90+ unit tests covering:
- Distance calculations (Haversine and Vincenty)
- Bearing calculations
- Coordinate operations
- Polygon operations
- Path operations
- Batch operations
- Unit conversions
- Edge cases and error handling
- Benchmark tests

## License

MIT License

## References

- [Haversine formula - Wikipedia](https://en.wikipedia.org/wiki/Haversine_formula)
- [Vincenty's formulae - Wikipedia](https://en.wikipedia.org/wiki/Vincenty%27s_formulae)
- [WGS-84 Ellipsoid](https://en.wikipedia.org/wiki/World_Geodetic_System)