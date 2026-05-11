// Example usage of geo_distance_utils package
package main

import (
	"fmt"
	"math"

	geo "github.com/ayukyo/alltoolkit/Go/geo_distance_utils"
)

func main() {
	fmt.Println("=== AllToolkit Geo Distance Utils Examples ===")
	fmt.Println()

	// ========================================
	// Example 1: Basic Distance Calculation
	// ========================================
	fmt.Println("--- Example 1: Distance Calculation ---")

	beijing := geo.Coordinate{Lat: 39.9042, Lon: 116.4074}
	shanghai := geo.Coordinate{Lat: 31.2304, Lon: 121.4737}
	newYork := geo.Coordinate{Lat: 40.7128, Lon: -74.0060}
	london := geo.Coordinate{Lat: 51.5074, Lon: -0.1278}

	// Haversine distance (spherical Earth)
	distHK, _ := geo.HaversineDistance(beijing, shanghai, geo.UnitKM)
	fmt.Printf("Beijing to Shanghai (Haversine): %.2f km\n", distHK)

	// Vincenty distance (ellipsoidal Earth - more accurate)
	distVK, _ := geo.VincentyDistance(beijing, shanghai, geo.UnitKM)
	fmt.Printf("Beijing to Shanghai (Vincenty): %.2f km\n", distVK)

	// Different units
	distMiles, _ := geo.HaversineDistance(beijing, shanghai, geo.UnitMiles)
	distNautical, _ := geo.HaversineDistance(beijing, shanghai, geo.UnitNautical)
	fmt.Printf("Beijing to Shanghai: %.2f miles, %.2f nautical miles\n", distMiles, distNautical)

	// New York to London
	distNYL, _ := geo.HaversineDistance(newYork, london, geo.UnitKM)
	fmt.Printf("New York to London: %.2f km\n", distNYL)

	fmt.Println()

	// ========================================
	// Example 2: Bearing Calculations
	// ========================================
	fmt.Println("--- Example 2: Bearing Calculations ---")

	bearing := geo.InitialBearing(beijing, shanghai)
	fmt.Printf("Initial bearing from Beijing to Shanghai: %.2f°\n", bearing)

	finalBearing := geo.FinalBearing(beijing, shanghai)
	fmt.Printf("Final bearing at Shanghai: %.2f°\n", finalBearing)

	// Cardinal directions
	north := geo.InitialBearing(geo.Coordinate{Lat: 0, Lon: 0}, geo.Coordinate{Lat: 1, Lon: 0})
	east := geo.InitialBearing(geo.Coordinate{Lat: 0, Lon: 0}, geo.Coordinate{Lat: 0, Lon: 1})
	fmt.Printf("North: %.0f°, East: %.0f°\n", north, east)

	fmt.Println()

	// ========================================
	// Example 3: Midpoint Calculation
	// ========================================
	fmt.Println("--- Example 3: Midpoint Calculation ---")

	mid := geo.Midpoint(beijing, shanghai)
	fmt.Printf("Midpoint: %.4f°N, %.4f°E\n", mid.Lat, mid.Lon)

	midStr := geo.CoordinateToString(mid, "decimal", 4)
	fmt.Printf("Midpoint formatted: %s\n", midStr)

	fmt.Println()

	// ========================================
	// Example 4: Destination Point
	// ========================================
	fmt.Println("--- Example 4: Destination Point ---")

	start := geo.Coordinate{Lat: 0, Lon: 0}

	// 100 km north
	destNorth := geo.DestinationPoint(start, 0, 100)
	fmt.Printf("100 km north from (0,0): %.2f°N, %.2f°E\n", destNorth.Lat, destNorth.Lon)

	// 100 km east
	destEast := geo.DestinationPoint(start, 90, 100)
	fmt.Printf("100 km east from (0,0): %.2f°N, %.2f°E\n", destEast.Lat, destEast.Lon)

	// 111.19 km east ≈ 1 degree at equator
	dest1deg := geo.DestinationPoint(start, 90, 111.19)
	fmt.Printf("1 degree east from (0,0): %.4f°N, %.4f°E\n", dest1deg.Lat, dest1deg.Lon)

	fmt.Println()

	// ========================================
	// Example 5: Bounding Box
	// ========================================
	fmt.Println("--- Example 5: Bounding Box ---")

	center := geo.Coordinate{Lat: 39.9, Lon: 116.4}
	bounds := geo.BoundingBox(center, 50)

	fmt.Printf("50 km bounding box around Beijing:\n")
	fmt.Printf("  Min: %.4f°N, %.4f°E\n", bounds.MinLat, bounds.MinLon)
	fmt.Printf("  Max: %.4f°N, %.4f°E\n", bounds.MaxLat, bounds.MaxLon)
	fmt.Printf("  Lat range: %.4f°\n", bounds.MaxLat-bounds.MinLat)
	fmt.Printf("  Lon range: %.4f°\n", bounds.MaxLon-bounds.MinLon)

	fmt.Println()

	// ========================================
	// Example 6: Point in Polygon
	// ========================================
	fmt.Println("--- Example 6: Point in Polygon ---")

	// Beijing approximate area
	beijingArea := []geo.Coordinate{
		{Lat: 39.8, Lon: 115.9},
		{Lat: 40.2, Lon: 115.9},
		{Lat: 40.2, Lon: 116.8},
		{Lat: 39.8, Lon: 116.8},
	}

	insidePoint := geo.Coordinate{Lat: 40.0, Lon: 116.4}
	outsidePoint := geo.Coordinate{Lat: 38.5, Lon: 116.4}

	fmt.Printf("Point (40.0, 116.4) in Beijing area: %v\n", geo.PointInPolygon(insidePoint, beijingArea))
	fmt.Printf("Point (38.5, 116.4) in Beijing area: %v\n", geo.PointInPolygon(outsidePoint, beijingArea))

	// Calculate polygon area
	area := geo.PolygonAreaKM2(beijingArea)
	fmt.Printf("Beijing area polygon: %.2f km²\n", area)

	fmt.Println()

	// ========================================
	// Example 7: Path Operations
	// ========================================
	fmt.Println("--- Example 7: Path Operations ---")

	// Flight path: Beijing -> Shanghai -> Guangzhou
	path := []geo.Coordinate{
		beijing,
		shanghai,
		{Lat: 23.1291, Lon: 113.2644}, // Guangzhou
	}

	totalDist, _ := geo.TotalPathDistance(path, geo.UnitKM)
	fmt.Printf("Total Beijing -> Shanghai -> Guangzhou distance: %.2f km\n", totalDist)

	// Interpolate path
	interpolated := geo.InterpolatePath(beijing, shanghai, 5)
	fmt.Printf("Interpolated points (Beijing to Shanghai, 5 segments):\n")
	for i, p := range interpolated {
		fmt.Printf("  Point %d: %.4f°N, %.4f°E\n", i, p.Lat, p.Lon)
	}

	// Nearest point on path
	testPoint := geo.Coordinate{Lat: 35, Lon: 119}
	nearest, _ := geo.NearestPointOnPath(testPoint, path)
	fmt.Printf("Nearest point on path from (35, 119): %.4f°N, %.4f°E (%.2f km away, segment %d)\n",
		nearest.NearestPoint.Lat, nearest.NearestPoint.Lon, nearest.DistanceKM, nearest.SegmentIndex)

	fmt.Println()

	// ========================================
	// Example 8: Batch Operations
	// ========================================
	fmt.Println("--- Example 8: Batch Operations ---")

	// Cities
	cities := []geo.Coordinate{
		{Lat: 40, Lon: 116},      // Beijing area
		{Lat: 35, Lon: 117},      // Near Jinan
		{Lat: 30, Lon: 120},      // Near Hangzhou
		{Lat: 25, Lon: 113},      // Guangzhou area
	}

	searchPoint := geo.Coordinate{Lat: 37, Lon: 118}

	// Find nearest city
	nearestCity, _ := geo.FindNearest(searchPoint, cities, geo.UnitKM)
	fmt.Printf("Nearest city to (37, 118): index %d, %.2f km away\n", nearestCity.Index, nearestCity.Distance)

	// Distances to all
	distances, _ := geo.DistancesToAll(searchPoint, cities, geo.UnitKM)
	fmt.Printf("Distances to all cities:\n")
	for i, d := range distances {
		fmt.Printf("  City %d: %.2f km\n", i, d)
	}

	// Cities within 500 km
	within500, _ := geo.WithinRadius(searchPoint, cities, 500, geo.UnitKM)
	fmt.Printf("Cities within 500 km: %d found\n", len(within500))
	for _, r := range within500 {
		fmt.Printf("  Index %d: %.2f km\n", r.Index, r.Distance)
	}

	fmt.Println()

	// ========================================
	// Example 9: Coordinate Formats
	// ========================================
	fmt.Println("--- Example 9: Coordinate Formats ---")

	coord := geo.Coordinate{Lat: 39.9042, Lon: 116.4074}

	// Decimal to DMS
	dms := geo.DecimalToDMS(coord.Lat, coord.Lon)
	fmt.Printf("Beijing in DMS:\n")
	fmt.Printf("  Latitude: %d°%d'%g\"%s\n", dms.Lat.Degrees, dms.Lat.Minutes, dms.Lat.Seconds, dms.Lat.Direction)
	fmt.Printf("  Longitude: %d°%d'%g\"%s\n", dms.Lon.Degrees, dms.Lon.Minutes, dms.Lon.Seconds, dms.Lon.Direction)

	// DMS back to decimal
	backDecimal := geo.DMSToDecimal(dms.Lat, dms.Lon)
	fmt.Printf("Back to decimal: %.4f°N, %.4f°E\n", backDecimal.Lat, backDecimal.Lon)

	// String formats
	fmt.Printf("Decimal format: %s\n", geo.CoordinateToString(coord, "decimal", 4))
	fmt.Printf("DMS format: %s\n", geo.CoordinateToString(coord, "dms", 0))
	fmt.Printf("DM format: %s\n", geo.CoordinateToString(coord, "dm", 0))

	fmt.Println()

	// ========================================
	// Example 10: Unit Conversions
	// ========================================
	fmt.Println("--- Example 10: Unit Conversions ---")

	km := 1000.0
	fmt.Printf("%.0f km = %.2f miles\n", km, geo.ConvertKMToMiles(km))
	fmt.Printf("%.0f km = %.2f nautical miles\n", km, geo.ConvertKMToNautical(km))
	fmt.Printf("%.0f km = %.0f meters\n", km, geo.ConvertKMToM(km))

	miles := 1000.0
	fmt.Printf("%.0f miles = %.2f km\n", miles, geo.ConvertMilesToKM(miles))

	nautical := 1000.0
	fmt.Printf("%.0f nautical miles = %.2f km\n", nautical, geo.ConvertNauticalToKM(nautical))

	// Generic conversion
	converted, _ := geo.ConvertDistance(100, geo.UnitKM, geo.UnitMiles)
	fmt.Printf("Convert 100 km to miles: %.2f\n", converted)

	fmt.Println()

	// ========================================
	// Example 11: Coordinate Validation
	// ========================================
	fmt.Println("--- Example 11: Coordinate Validation ---")

	fmt.Printf("IsValid(45, 90): %v\n", geo.IsValidCoordinate(45, 90))
	fmt.Printf("IsValid(95, 0): %v\n", geo.IsValidCoordinate(95, 0))
	fmt.Printf("IsValid(45, 200): %v\n", geo.IsValidCoordinate(45, 200))

	// Normalization
	normalized := geo.NormalizeCoordinate(100, 370)
	fmt.Printf("Normalize(100, 370): %.2f°N, %.2f°E\n", normalized.Lat, normalized.Lon)

	normalized2 := geo.NormalizeLongitude(270)
	fmt.Printf("NormalizeLongitude(270): %.2f°\n", normalized2)

	fmt.Println()

	// ========================================
	// Example 12: Compare Haversine vs Vincenty
	// ========================================
	fmt.Println("--- Example 12: Haversine vs Vincenty Comparison ---")

	// Short distance
	short1 := geo.Coordinate{Lat: 0, Lon: 0}
	short2 := geo.Coordinate{Lat: 0.01, Lon: 0.01}
	hDist, _ := geo.HaversineDistance(short1, short2, geo.UnitKM)
	vDist, _ := geo.VincentyDistance(short1, short2, geo.UnitKM)
	fmt.Printf("Short distance (0.01°): Haversine=%.4f km, Vincenty=%.4f km, diff=%.4f m\n",
		hDist, vDist, (hDist-vDist)*1000)

	// Medium distance
	hDist, _ = geo.HaversineDistance(beijing, shanghai, geo.UnitKM)
	vDist, _ = geo.VincentyDistance(beijing, shanghai, geo.UnitKM)
	fmt.Printf("Beijing-Shanghai: Haversine=%.4f km, Vincenty=%.4f km, diff=%.2f m\n",
		hDist, vDist, math.Abs(hDist-vDist)*1000)

	// Long distance
	hDist, _ = geo.HaversineDistance(newYork, london, geo.UnitKM)
	vDist, _ = geo.VincentyDistance(newYork, london, geo.UnitKM)
	fmt.Printf("NewYork-London: Haversine=%.4f km, Vincenty=%.4f km, diff=%.2f m\n",
		hDist, vDist, math.Abs(hDist-vDist)*1000)

	fmt.Println()
	fmt.Println("=== All Examples Complete ===")
}