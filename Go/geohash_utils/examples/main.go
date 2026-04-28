// Example usage of geohash_utils package
package main

import (
	"fmt"

	geohash "github.com/ayukyo/alltoolkit/Go/geohash_utils"
)

func main() {
	fmt.Println("=== GeoHash Utils Examples ===\n")

	// Example 1: Basic Encoding
	fmt.Println("1. Basic Encoding:")
	lat, lon := 39.9042, 116.4074 // Beijing coordinates
	hash, err := geohash.Encode(lat, lon)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   Coordinates: (%.4f, %.4f)\n", lat, lon)
	fmt.Printf("   GeoHash: %s\n\n", hash)

	// Example 2: Encoding with Custom Precision
	fmt.Println("2. Encoding with Different Precisions:")
	precisions := []int{1, 3, 5, 7, 9, 12}
	for _, prec := range precisions {
		h, _ := geohash.EncodeWithPrecision(lat, lon, prec)
		fmt.Printf("   Precision %2d: %s\n", prec, h)
	}
	fmt.Println()

	// Example 3: Decoding
	fmt.Println("3. Decoding GeoHash:")
	result, err := geohash.Decode("wx4g0b")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   GeoHash: %s\n", result.GeoHash)
	fmt.Printf("   Center: (%.6f, %.6f)\n", result.Center.Lat, result.Center.Lon)
	fmt.Printf("   Bounds:\n")
	fmt.Printf("     Latitude:  [%.6f, %.6f]\n", result.Bounds.MinLat, result.Bounds.MaxLat)
	fmt.Printf("     Longitude: [%.6f, %.6f]\n", result.Bounds.MinLon, result.Bounds.MaxLon)
	fmt.Println()

	// Example 4: Neighbors
	fmt.Println("4. Finding Neighbors:")
	neighbors, err := geohash.Neighbors("wx4g0b")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	directions := []string{"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
	for i, n := range neighbors {
		fmt.Printf("   %s: %s\n", directions[i], n)
	}
	fmt.Println()

	// Example 5: Distance Calculation
	fmt.Println("5. Distance Calculation:")
	hash1 := "wx4g0b" // Beijing area
	hash2 := "dr5ru7" // New York area
	distance, err := geohash.Distance(hash1, hash2)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	distanceKm, _ := geohash.DistanceKm(hash1, hash2)
	fmt.Printf("   From: %s (Beijing area)\n", hash1)
	fmt.Printf("   To:   %s (New York area)\n", hash2)
	fmt.Printf("   Distance: %.2f meters (%.2f km)\n\n", distance, distanceKm)

	// Example 6: Check if Point is in GeoHash Cell
	fmt.Println("6. Contains Point Check:")
	testHash := "wx4g0b"
	result, _ = geohash.Decode(testHash)
	centerLat := result.Center.Lat
	centerLon := result.Center.Lon

	contains, _ := geohash.Contains(testHash, centerLat, centerLon)
	fmt.Printf("   Does %s contain center (%.4f, %.4f)? %v\n", testHash, centerLat, centerLon, contains)

	contains, _ = geohash.Contains(testHash, 0, 0)
	fmt.Printf("   Does %s contain (0, 0)? %v\n\n", testHash, contains)

	// Example 7: Common Prefix
	fmt.Println("7. Common Prefix of GeoHashes:")
	hashes := []string{"wx4g0b", "wx4g0c", "wx4g0d", "wx4g0e"}
	common := geohash.CommonPrefix(hashes...)
	fmt.Printf("   Hashes: %v\n", hashes)
	fmt.Printf("   Common prefix: %s\n\n", common)

	// Example 8: Bounding Box Encoding
	fmt.Println("8. Bounding Box Encoding:")
	latMin, lonMin := 39.9, 116.4
	latMax, lonMax := 40.0, 116.5
	bboxHash, _ := geohash.BoundingBox(latMin, lonMin, latMax, lonMax)
	fmt.Printf("   Bounding box: [%.2f, %.2f] to [%.2f, %.2f]\n", latMin, lonMin, latMax, lonMax)
	fmt.Printf("   GeoHash: %s\n\n", bboxHash)

	// Example 9: Validation
	fmt.Println("9. GeoHash Validation:")
	testHashes := []string{"wx4g0b", "invalid!", "wx4g0bi", ""}
	for _, h := range testHashes {
		valid := geohash.Validate(h)
		fmt.Printf("   %q: valid=%v\n", h, valid)
	}
	fmt.Println()

	// Example 10: Famous Landmarks
	fmt.Println("10. Famous Landmarks:")
	landmarks := []struct {
		name string
		lat  float64
		lon  float64
	}{
		{"Eiffel Tower", 48.8584, 2.2945},
		{"Statue of Liberty", 40.6892, -74.0445},
		{"Great Wall", 40.4319, 116.5704},
		{"Sydney Opera", -33.8568, 151.2153},
		{"Machu Picchu", -13.1631, -72.5450},
	}

	for _, landmark := range landmarks {
		h, _ := geohash.EncodeWithPrecision(landmark.lat, landmark.lon, 6)
		fmt.Printf("   %-20s: %s\n", landmark.name, h)
	}
}