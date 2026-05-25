# CoordinateUtils - Geographic Coordinate Utilities for Kotlin

A zero-dependency Kotlin library for working with geographic coordinates. Provides comprehensive utilities for distance calculations, navigation, coordinate conversions, and geometric operations.

## Features

- 📍 **Distance Calculation** - Haversine formula for accurate distance on Earth's surface
- 🧭 **Bearing Calculation** - Initial and final bearing between points
- 🗺️ **Midpoint & Destination** - Find midpoints and destinations along great circle paths
- 📦 **Bounding Box** - Generate bounding boxes for proximity searches
- 🔷 **Polygon Operations** - Area, perimeter, centroid, point-in-polygon tests
- 📝 **Coordinate Parsing** - Parse multiple coordinate formats (decimal, DMS)
- 🌐 **UTM Conversion** - Convert WGS84 to UTM coordinates
- 🎯 **Closest Point** - Find nearest location from candidates
- ✈️ **Path Interpolation** - Generate waypoints along a path

## Installation

Copy `CoordinateUtils.kt` into your Kotlin project. No external dependencies required.

## Quick Start

```kotlin
import coordinate_utils.*

fun main() {
    // Create coordinates
    val newYork = Coordinate(40.7128, -74.0060)
    val london = Coordinate(51.5074, -0.1278)
    
    // Calculate distance
    val distance = distanceInKm(newYork, london)
    println("Distance: ${"%.1f".format(distance)} km") // ~5570 km
    
    // Calculate bearing
    val bearing = bearing(newYork, london)
    println("Bearing: ${"%.1f".format(bearing)}°") // ~52°
    
    // Find midpoint
    val mid = midpoint(newYork, london)
    println("Midpoint: $mid")
    
    // Generate bounding box
    val bbox = boundingBox(newYork, 10.0) // 10km radius
    println("Bounding box: $bbox")
}
```

## Usage Examples

### Distance Calculation

```kotlin
val from = Coordinate(40.7128, -74.0060) // New York
val to = Coordinate(51.5074, -0.1278)    // London

// Distance in different units
val km = distanceInKm(from, to)
val miles = distanceInMiles(from, to)
val meters = distanceInMeters(from, to)
```

### Navigation

```kotlin
val bearing = bearing(from, to)          // Initial bearing
val finalBearing = finalBearing(from, to) // Final bearing

// Travel 500km northeast
val destination = destination(from, 45.0, 500.0)

// Interpolate waypoints
val waypoints = interpolatePath(from, to, 5)
```

### Bounding Box

```kotlin
val center = Coordinate(37.7749, -122.4194)
val bbox = boundingBox(center, 10.0) // 10km radius

// Check if point is inside
val isInside = bbox.contains(somePoint)
```

### Coordinate Parsing

```kotlin
// Multiple formats supported
val coord1 = parseCoordinate("40.7128, -74.0060")
val coord2 = parseCoordinate("40.7128 -74.0060")
val coord3 = parseCoordinate("(40.7128, -74.0060)")
val coord4 = parseCoordinate("40.7128° -74.0060°")

// Format as DMS
val dms = coord1.toDMS() // "40°42'46.01"N, 74°0'21.60"W"
```

### Polygon Operations

```kotlin
val polygon = listOf(
    Coordinate(0.0, 0.0),
    Coordinate(1.0, 0.0),
    Coordinate(1.0, 1.0),
    Coordinate(0.0, 1.0)
)

val area = polygonArea(polygon)      // km²
val perim = perimeter(polygon)       // km
val center = centroid(polygon)       // Center point
val inside = isInsidePolygon(Coordinate(0.5, 0.5), polygon) // true
```

### Find Closest Location

```kotlin
val myLocation = Coordinate(37.7749, -122.4194)
val locations = listOf(
    Coordinate(37.7820, -122.4060),
    Coordinate(37.7590, -122.4210),
    Coordinate(37.7660, -122.4250)
)

val (closest, distance) = findClosest(myLocation, locations)!!
println("Nearest is ${"%.2f".format(distance)} km away")
```

### UTM Conversion

```kotlin
val coord = Coordinate(40.7128, -74.0060)
val (zone, easting, northing) = CoordinateSystems.wgs84ToUtm(coord)
val hemisphere = CoordinateSystems.utmHemisphere(coord.latitude)

println("UTM: Zone $zone$hemisphere E:$easting N:$northing")
```

## API Reference

### Coordinate

```kotlin
data class Coordinate(val latitude: Double, val longitude: Double)
```

- `toDMS(): String` - Format as Degrees Minutes Seconds

### Distance Functions

- `distance(from, to, radius)` - Distance with custom Earth radius
- `distanceInKm(from, to)` - Distance in kilometers
- `distanceInMeters(from, to)` - Distance in meters
- `distanceInMiles(from, to)` - Distance in miles

### Navigation Functions

- `bearing(from, to)` - Initial bearing in degrees
- `finalBearing(from, to)` - Final bearing in degrees
- `midpoint(from, to)` - Midpoint coordinate
- `destination(from, bearing, distance)` - Destination point

### Geometric Functions

- `boundingBox(center, distance)` - Generate bounding box
- `polygonArea(polygon)` - Area in km²
- `perimeter(polygon)` - Perimeter in km
- `centroid(polygon)` - Center point
- `isInsidePolygon(point, polygon)` - Point-in-polygon test
- `interpolatePath(from, to, numPoints)` - Generate waypoints
- `findClosest(target, candidates)` - Find nearest point

### Parsing Functions

- `parseCoordinate(input)` - Parse from string
- `dmsToDecimal(deg, min, sec)` - Convert DMS to decimal
- `decimalToDms(decimal)` - Convert decimal to DMS components

### Constants

- `EARTH_RADIUS_KM` - 6,371 km
- `EARTH_RADIUS_M` - 6,371,000 m
- `EARTH_RADIUS_MI` - 3,958.8 mi

## Running Tests

```bash
# Using kotlinc
kotlinc -script CoordinateUtilsTest.kt

# Or compile and run
kotlinc CoordinateUtils.kt CoordinateUtilsTest.kt -include-runtime -d CoordinateUtilsTest.jar
kotlin -jar CoordinateUtilsTest.jar
```

## Running Examples

```bash
kotlinc -script Examples.kt
```

## Accuracy Notes

- Distance calculations use the Haversine formula with a spherical Earth approximation
- Accuracy is ~0.5% for most use cases
- For precise geodesic calculations, consider using a specialized geodesy library
- UTM conversion is simplified; for surveying-grade precision, use proj4j

## License

MIT License - Free for personal and commercial use.

## Author

Generated by AllToolkit - https://github.com/ayukyo/alltoolkit