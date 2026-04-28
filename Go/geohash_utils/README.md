# GeoHash Utils

A comprehensive GeoHash encoding and decoding library for Go with zero external dependencies.

## Features

- **Encode**: Convert latitude/longitude coordinates to GeoHash strings
- **Decode**: Convert GeoHash strings back to coordinates and bounding boxes
- **Neighbors**: Find all 8 neighboring GeoHash cells
- **Distance**: Calculate distance between two GeoHash cells (Haversine formula)
- **Contains**: Check if a point is within a GeoHash cell
- **Common Prefix**: Find the longest common prefix of multiple GeoHashes
- **Bounding Box**: Encode a bounding box into a covering GeoHash
- **Validation**: Validate GeoHash strings

## Installation

```go
import geohash "github.com/ayukyo/alltoolkit/Go/geohash_utils"
```

## Usage

### Basic Encoding

```go
// Default precision (9 characters)
hash, err := geohash.Encode(39.9042, 116.4074)
// Output: "wx4g0bcnh"

// Custom precision (1-12)
hash, err := geohash.EncodeWithPrecision(39.9042, 116.4074, 6)
// Output: "wx4g0b"
```

### Decoding

```go
result, err := geohash.Decode("wx4g0b")
// result.GeoHash  - Original hash string
// result.Precision - Length of hash
// result.Center   - Center point {Lat, Lon}
// result.Bounds   - Bounding box {MinLat, MaxLat, MinLon, MaxLon}
```

### Finding Neighbors

```go
neighbors, err := geohash.Neighbors("wx4g0b")
// Returns 8 neighbors: [N, NE, E, SE, S, SW, W, NW]
```

### Distance Calculation

```go
// Distance in meters
distance, err := geohash.Distance("wx4g0b", "dr5ru7")

// Distance in kilometers
distanceKm, err := geohash.DistanceKm("wx4g0b", "dr5ru7")
```

### Check if Point is in GeoHash Cell

```go
contains, err := geohash.Contains("wx4g0b", 39.904, 116.407)
// Returns true if point is within the cell
```

### Common Prefix

```go
common := geohash.CommonPrefix("wx4g0b", "wx4g0c", "wx4g0d")
// Output: "wx4g0"
```

### Bounding Box

```go
hash, err := geohash.BoundingBox(39.9, 116.4, 40.0, 116.5)
// Returns GeoHash that covers the bounding box
```

### Validation

```go
valid := geohash.Validate("wx4g0b")
// Returns true for valid GeoHash strings
```

## GeoHash Precision

| Precision | Cell Width | Cell Height |
|-----------|------------|-------------|
| 1         | ~5000 km   | ~5000 km    |
| 2         | ~1260 km   | ~630 km     |
| 3         | ~156 km    | ~156 km     |
| 4         | ~39 km     | ~19.5 km    |
| 5         | ~4.9 km    | ~4.9 km     |
| 6         | ~1.2 km    | ~610 m      |
| 7         | ~152 m     | ~152 m      |
| 8         | ~38 m      | ~19 m       |
| 9         | ~4.8 m     | ~4.8 m      |
| 10        | ~1.2 m     | ~59 cm      |
| 11        | ~15 cm     | ~15 cm      |
| 12        | ~3.7 cm    | ~1.9 cm     |

## API Reference

### Functions

```go
func Encode(lat, lon float64) (string, error)
func EncodeWithPrecision(lat, lon float64, precision int) (string, error)
func Decode(hash string) (*GeoHashResult, error)
func Neighbors(hash string) ([]string, error)
func Distance(hash1, hash2 string) (float64, error)
func DistanceKm(hash1, hash2 string) (float64, error)
func Contains(hash string, lat, lon float64) (bool, error)
func CommonPrefix(hashes ...string) string
func BoundingBox(latMin, lonMin, latMax, lonMax float64) (string, error)
func Validate(hash string) bool
func EstimatePrecision(latMin, lonMin, latMax, lonMax float64) int
```

### Types

```go
type Bounds struct {
    MinLat float64
    MaxLat float64
    MinLon float64
    MaxLon float64
}

type Point struct {
    Lat float64
    Lon float64
}

type GeoHashResult struct {
    Center    Point
    Bounds    Bounds
    GeoHash   string
    Precision int
}
```

## Examples

```go
// Encode famous landmarks
landmarks := map[string][2]float64{
    "Eiffel Tower":    {48.8584, 2.2945},
    "Statue of Liberty": {40.6892, -74.0445},
    "Sydney Opera":    {-33.8568, 151.2153},
}

for name, coord := range landmarks {
    hash, _ := geohash.EncodeWithPrecision(coord[0], coord[1], 6)
    fmt.Printf("%s: %s\n", name, hash)
}
// Output:
// Eiffel Tower: u09tvp
// Statue of Liberty: dr5ru7
// Sydney Opera: r3gx2f
```

## License

MIT License