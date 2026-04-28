// Package geohash_utils provides GeoHash encoding and decoding utilities.
// GeoHash is a geocoding system that encodes geographic coordinates into short strings.
// This implementation has zero external dependencies and uses only Go standard library.
package geohash_utils

import (
	"errors"
	"math"
)

// Base32 characters used for GeoHash encoding
const base32 = "0123456789bcdefghjkmnpqrstuvwxyz"

// Error definitions
var (
	ErrInvalidGeoHash   = errors.New("invalid geohash string")
	ErrInvalidPrecision = errors.New("precision must be between 1 and 12")
	ErrInvalidLatitude  = errors.New("latitude must be between -90 and 90")
	ErrInvalidLongitude = errors.New("longitude must be between -180 and 180")
)

// Bounds represents the bounding box of a GeoHash cell
type Bounds struct {
	MinLat float64
	MaxLat float64
	MinLon float64
	MaxLon float64
}

// Point represents a geographic coordinate
type Point struct {
	Lat float64
	Lon float64
}

// GeoHashResult contains the decoded GeoHash information
type GeoHashResult struct {
	Center   Point  // Center point of the GeoHash cell
	Bounds   Bounds // Bounding box
	GeoHash  string // The GeoHash string
	Precision int   // Length of the GeoHash string
}

// Encode converts latitude and longitude to a GeoHash string with default precision of 9
func Encode(lat, lon float64) (string, error) {
	return EncodeWithPrecision(lat, lon, 9)
}

// EncodeWithPrecision converts latitude and longitude to a GeoHash string with specified precision
func EncodeWithPrecision(lat, lon float64, precision int) (string, error) {
	if precision < 1 || precision > 12 {
		return "", ErrInvalidPrecision
	}
	if lat < -90 || lat > 90 {
		return "", ErrInvalidLatitude
	}
	if lon < -180 || lon > 180 {
		return "", ErrInvalidLongitude
	}

	var hash []byte
	var isEven bool = true
	var latMin, latMax float64 = -90, 90
	var lonMin, lonMax float64 = -180, 180
	var bit uint = 0
	var ch byte = 0

	for len(hash) < precision {
		if isEven {
			mid := (lonMin + lonMax) / 2
			if lon >= mid {
				ch |= 1 << (4 - bit)
				lonMin = mid
			} else {
				lonMax = mid
			}
		} else {
			mid := (latMin + latMax) / 2
			if lat >= mid {
				ch |= 1 << (4 - bit)
				latMin = mid
			} else {
				latMax = mid
			}
		}
		isEven = !isEven

		bit++
		if bit == 5 {
			hash = append(hash, base32[ch])
			bit = 0
			ch = 0
		}
	}

	return string(hash), nil
}

// Decode decodes a GeoHash string into its center point and bounds
func Decode(hash string) (*GeoHashResult, error) {
	if len(hash) < 1 || len(hash) > 12 {
		return nil, ErrInvalidGeoHash
	}

	// Validate characters
	for _, c := range hash {
		if !isValidBase32(byte(c)) {
			return nil, ErrInvalidGeoHash
		}
	}

	var isEven bool = true
	var latMin, latMax float64 = -90, 90
	var lonMin, lonMax float64 = -180, 180

	for _, c := range hash {
		cd := indexOfBase32(byte(c))
		if cd == -1 {
			return nil, ErrInvalidGeoHash
		}

		for j := 4; j >= 0; j-- {
			mask := 1 << j
			if isEven {
				if cd&mask != 0 {
					lonMin = (lonMin + lonMax) / 2
				} else {
					lonMax = (lonMin + lonMax) / 2
				}
			} else {
				if cd&mask != 0 {
					latMin = (latMin + latMax) / 2
				} else {
					latMax = (latMin + latMax) / 2
				}
			}
			isEven = !isEven
		}
	}

	result := &GeoHashResult{
		GeoHash:  hash,
		Precision: len(hash),
		Bounds: Bounds{
			MinLat: latMin,
			MaxLat: latMax,
			MinLon: lonMin,
			MaxLon: lonMax,
		},
		Center: Point{
			Lat: (latMin + latMax) / 2,
			Lon: (lonMin + lonMax) / 2,
		},
	}

	return result, nil
}

// isValidBase32 checks if a character is a valid base32 character for GeoHash
func isValidBase32(c byte) bool {
	for i := 0; i < len(base32); i++ {
		if base32[i] == c {
			return true
		}
	}
	return false
}

// indexOfBase32 returns the index of a character in the base32 alphabet
func indexOfBase32(c byte) int {
	for i := 0; i < len(base32); i++ {
		if base32[i] == c {
			return i
		}
	}
	return -1
}

// Neighbors returns all 8 neighboring GeoHash cells
func Neighbors(hash string) ([]string, error) {
	if len(hash) < 1 || len(hash) > 12 {
		return nil, ErrInvalidGeoHash
	}

	// Validate characters
	for _, c := range hash {
		if !isValidBase32(byte(c)) {
			return nil, ErrInvalidGeoHash
		}
	}

	// Directions: N, NE, E, SE, S, SW, W, NW
	directions := []struct {
		latDir, lonDir int
	}{
		{1, 0},   // N
		{1, 1},   // NE
		{0, 1},   // E
		{-1, 1},  // SE
		{-1, 0},  // S
		{-1, -1}, // SW
		{0, -1},  // W
		{1, -1},  // NW
	}

	neighbors := make([]string, 8)
	for i, dir := range directions {
		neighbor, err := neighbor(hash, dir.latDir, dir.lonDir)
		if err != nil {
			return nil, err
		}
		neighbors[i] = neighbor
	}

	return neighbors, nil
}

// neighbor calculates a neighboring GeoHash in a given direction
func neighbor(hash string, latDir, lonDir int) (string, error) {
	// Convert hash to coordinates and then find neighbor
	result, err := Decode(hash)
	if err != nil {
		return "", err
	}

	// Calculate cell dimensions
	latStep := (result.Bounds.MaxLat - result.Bounds.MinLat)
	lonStep := (result.Bounds.MaxLon - result.Bounds.MinLon)

	// Calculate new center
	newLat := result.Center.Lat + float64(latDir)*latStep
	newLon := result.Center.Lon + float64(lonDir)*lonStep

	// Wrap around if necessary
	for newLat > 90 {
		newLat -= 180
	}
	for newLat < -90 {
		newLat += 180
	}
	for newLon > 180 {
		newLon -= 360
	}
	for newLon < -180 {
		newLon += 360
	}

	return EncodeWithPrecision(newLat, newLon, len(hash))
}

// Distance calculates the approximate distance between two GeoHash cells in meters
// Uses Haversine formula for spherical distance calculation
func Distance(hash1, hash2 string) (float64, error) {
	if len(hash1) < 1 || len(hash1) > 12 || len(hash2) < 1 || len(hash2) > 12 {
		return 0, ErrInvalidGeoHash
	}

	result1, err := Decode(hash1)
	if err != nil {
		return 0, err
	}

	result2, err := Decode(hash2)
	if err != nil {
		return 0, err
	}

	return haversine(result1.Center.Lat, result1.Center.Lon, result2.Center.Lat, result2.Center.Lon), nil
}

// haversine calculates the great-circle distance between two points in meters
func haversine(lat1, lon1, lat2, lon2 float64) float64 {
	const earthRadius = 6371000.0 // Earth's radius in meters

	lat1Rad := lat1 * math.Pi / 180
	lat2Rad := lat2 * math.Pi / 180
	deltaLat := (lat2 - lat1) * math.Pi / 180
	deltaLon := (lon2 - lon1) * math.Pi / 180

	a := math.Sin(deltaLat/2)*math.Sin(deltaLat/2) +
		math.Cos(lat1Rad)*math.Cos(lat2Rad)*
			math.Sin(deltaLon/2)*math.Sin(deltaLon/2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	return earthRadius * c
}

// DistanceKm calculates distance in kilometers
func DistanceKm(hash1, hash2 string) (float64, error) {
	d, err := Distance(hash1, hash2)
	return d / 1000, err
}

// Precision estimates the appropriate GeoHash precision for a given bounding box
func EstimatePrecision(latMin, lonMin, latMax, lonMax float64) int {
	// Each GeoHash character adds about 5 bits of precision
	// Precision 1: ~5000km, 2: ~1260km, 3: ~156km, 4: ~39km, 5: ~4.9km
	// 6: ~1.2km, 7: ~152m, 8: ~38m, 9: ~4.8m, 10: ~1.2m, 11: ~0.15m, 12: ~0.04m

	latDiff := math.Abs(latMax - latMin)
	lonDiff := math.Abs(lonMax - lonMin)
	maxDiff := math.Max(latDiff, lonDiff)

	// Estimate based on width in degrees
	switch {
	case maxDiff > 45:
		return 1
	case maxDiff > 11:
		return 2
	case maxDiff > 1.4:
		return 3
	case maxDiff > 0.35:
		return 4
	case maxDiff > 0.044:
		return 5
	case maxDiff > 0.011:
		return 6
	case maxDiff > 0.0014:
		return 7
	case maxDiff > 0.00035:
		return 8
	case maxDiff > 0.000044:
		return 9
	case maxDiff > 0.000011:
		return 10
	case maxDiff > 0.0000014:
		return 11
	default:
		return 12
	}
}

// Contains checks if a GeoHash contains the given point
func Contains(hash string, lat, lon float64) (bool, error) {
	result, err := Decode(hash)
	if err != nil {
		return false, err
	}

	return lat >= result.Bounds.MinLat &&
		lat <= result.Bounds.MaxLat &&
		lon >= result.Bounds.MinLon &&
		lon <= result.Bounds.MaxLon, nil
}

// CommonPrefix returns the longest common prefix of multiple GeoHash strings
func CommonPrefix(hashes ...string) string {
	if len(hashes) == 0 {
		return ""
	}

	minLen := len(hashes[0])
	for _, h := range hashes[1:] {
		if len(h) < minLen {
			minLen = len(h)
		}
	}

	for i := 0; i < minLen; i++ {
		c := hashes[0][i]
		for _, h := range hashes[1:] {
			if h[i] != c {
				return hashes[0][:i]
			}
		}
	}

	return hashes[0][:minLen]
}

// BoundingBox encodes a bounding box into a GeoHash that covers the entire area
func BoundingBox(latMin, lonMin, latMax, lonMax float64) (string, error) {
	precision := EstimatePrecision(latMin, lonMin, latMax, lonMax)
	centerLat := (latMin + latMax) / 2
	centerLon := (lonMin + lonMax) / 2
	return EncodeWithPrecision(centerLat, centerLon, precision)
}

// Validate checks if a string is a valid GeoHash
func Validate(hash string) bool {
	if len(hash) < 1 || len(hash) > 12 {
		return false
	}
	for _, c := range hash {
		if !isValidBase32(byte(c)) {
			return false
		}
	}
	return true
}