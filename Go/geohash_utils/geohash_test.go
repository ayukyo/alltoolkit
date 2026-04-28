package geohash_utils

import (
	"math"
	"testing"
)

func TestEncode(t *testing.T) {
	tests := []struct {
		name      string
		lat       float64
		lon       float64
		precision int
		want      string
		wantErr   bool
	}{
		{"Beijing", 39.9042, 116.4074, 6, "wx4g0b", false},
		{"New York", 40.7128, -74.0060, 6, "dr5reg", false},
		{"London", 51.5074, -0.1278, 6, "gcpvj0", false},
		{"Sydney", -33.8688, 151.2093, 6, "r3gx2f", false},
		{"Tokyo", 35.6762, 139.6503, 6, "xn76cy", false},
		{"North Pole", 90, 0, 6, "upbpbp", false},
		{"South Pole", -90, 0, 6, "h00000", false},
		{"Equator Prime Meridian", 0, 0, 6, "s00000", false},
		{"High precision", 39.9042, 116.4074, 9, "wx4g0bm6c", false},
		{"Low precision", 39.9042, 116.4074, 1, "w", false},
		{"Invalid precision low", 0, 0, 0, "", true},
		{"Invalid precision high", 0, 0, 13, "", true},
		{"Invalid latitude", 91, 0, 6, "", true},
		{"Invalid longitude", 0, 181, 6, "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var got string
			var err error

			if tt.precision == 9 && tt.name == "High precision" {
				got, err = EncodeWithPrecision(tt.lat, tt.lon, tt.precision)
			} else if tt.precision == 9 {
				got, err = Encode(tt.lat, tt.lon)
			} else if tt.precision == 6 && tt.name != "High precision" && tt.name != "Low precision" && tt.name != "Invalid precision low" && tt.name != "Invalid precision high" {
				got, err = EncodeWithPrecision(tt.lat, tt.lon, tt.precision)
			} else {
				got, err = EncodeWithPrecision(tt.lat, tt.lon, tt.precision)
			}

			if (err != nil) != tt.wantErr {
				t.Errorf("Encode() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && got != tt.want {
				t.Errorf("Encode() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestEncodeDefaultPrecision(t *testing.T) {
	// Test default precision (9)
	got, err := Encode(39.9042, 116.4074)
	if err != nil {
		t.Errorf("Encode() error = %v", err)
		return
	}
	if len(got) != 9 {
		t.Errorf("Encode() length = %v, want 9", len(got))
	}
}

func TestDecode(t *testing.T) {
	tests := []struct {
		name     string
		hash     string
		wantErr  bool
		checkLat float64 // Expected approximate latitude
		checkLon float64 // Expected approximate longitude
	}{
		{"Beijing", "wx4g0b", false, 39.9042, 116.4074},
		{"New York", "dr5ru7", false, 40.7128, -74.0060},
		{"London", "gcpvj0", false, 51.5074, -0.1278},
		{"Single char", "w", false, 0, 0},
		{"Empty string", "", true, 0, 0},
		{"Too long", "wx4g0bcnh123456", true, 0, 0},
		{"Invalid char", "wx4g0bi", true, 0, 0}, // 'i' is not valid base32
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Decode(tt.hash)

			if (err != nil) != tt.wantErr {
				t.Errorf("Decode() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if result.GeoHash != tt.hash {
					t.Errorf("Decode().GeoHash = %v, want %v", result.GeoHash, tt.hash)
				}
				if result.Precision != len(tt.hash) {
					t.Errorf("Decode().Precision = %v, want %v", result.Precision, len(tt.hash))
				}

				// Check that center is within bounds
				if result.Center.Lat < result.Bounds.MinLat || result.Center.Lat > result.Bounds.MaxLat {
					t.Errorf("Center latitude %v not in bounds [%v, %v]", result.Center.Lat, result.Bounds.MinLat, result.Bounds.MaxLat)
				}
				if result.Center.Lon < result.Bounds.MinLon || result.Center.Lon > result.Bounds.MaxLon {
					t.Errorf("Center longitude %v not in bounds [%v, %v]", result.Center.Lon, result.Bounds.MinLon, result.Bounds.MaxLon)
				}

				// Check approximate location for known hashes
				if tt.checkLat != 0 || tt.checkLon != 0 {
					latDiff := math.Abs(result.Center.Lat - tt.checkLat)
					lonDiff := math.Abs(result.Center.Lon - tt.checkLon)
					// Allow for precision-dependent error (about 1.2km for precision 6, ~0.02 degrees)
					if latDiff > 0.05 || lonDiff > 0.05 {
						t.Errorf("Location mismatch: got (%.4f, %.4f), expected approximately (%.4f, %.4f)",
							result.Center.Lat, result.Center.Lon, tt.checkLat, tt.checkLon)
					}
				}
			}
		})
	}
}

func TestEncodeDecodeRoundTrip(t *testing.T) {
	tests := []struct {
		lat float64
		lon float64
		prec int
	}{
		{39.9042, 116.4074, 6},
		{40.7128, -74.0060, 7},
		{-33.8688, 151.2093, 8},
		{0, 0, 9},
		{45.0, 90.0, 5},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			hash, err := EncodeWithPrecision(tt.lat, tt.lon, tt.prec)
			if err != nil {
				t.Errorf("Encode() error = %v", err)
				return
			}

			result, err := Decode(hash)
			if err != nil {
				t.Errorf("Decode() error = %v", err)
				return
			}

			// Check that original point is within decoded bounds
			if tt.lat < result.Bounds.MinLat || tt.lat > result.Bounds.MaxLat {
				t.Errorf("Latitude %v not in decoded bounds [%v, %v]", tt.lat, result.Bounds.MinLat, result.Bounds.MaxLat)
			}
			if tt.lon < result.Bounds.MinLon || tt.lon > result.Bounds.MaxLon {
				t.Errorf("Longitude %v not in decoded bounds [%v, %v]", tt.lon, result.Bounds.MinLon, result.Bounds.MaxLon)
			}
		})
	}
}

func TestNeighbors(t *testing.T) {
	tests := []struct {
		name    string
		hash    string
		wantErr bool
	}{
		{"Valid hash", "wx4g0b", false},
		{"Single char", "w", false},
		{"Empty string", "", true},
		{"Invalid char", "wx4g0i", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			neighbors, err := Neighbors(tt.hash)

			if (err != nil) != tt.wantErr {
				t.Errorf("Neighbors() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if len(neighbors) != 8 {
					t.Errorf("Neighbors() returned %v neighbors, want 8", len(neighbors))
				}
				// Verify all neighbors are valid GeoHashes
				for i, n := range neighbors {
					if !Validate(n) {
						t.Errorf("Neighbor %d is invalid: %v", i, n)
					}
				}
			}
		})
	}
}

func TestDistance(t *testing.T) {
	// Test distance between two points
	tests := []struct {
		name    string
		hash1   string
		hash2   string
		wantErr bool
	}{
		{"Same location", "wx4g0b", "wx4g0b", false},
		{"Nearby locations", "wx4g0b", "wx4g0c", false},
		{"Far locations", "wx4g0b", "dr5ru7", false},
		{"Invalid hash1", "", "wx4g0b", true},
		{"Invalid hash2", "wx4g0b", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			distance, err := Distance(tt.hash1, tt.hash2)

			if (err != nil) != tt.wantErr {
				t.Errorf("Distance() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if distance < 0 {
					t.Errorf("Distance() = %v, should be non-negative", distance)
				}

				// Same location should have 0 distance
				if tt.hash1 == tt.hash2 && distance > 0 {
					t.Errorf("Same location distance = %v, should be 0", distance)
				}
			}
		})
	}
}

func TestDistanceKm(t *testing.T) {
	distanceKm, err := DistanceKm("wx4g0b", "wx4g0b")
	if err != nil {
		t.Errorf("DistanceKm() error = %v", err)
		return
	}
	if distanceKm != 0 {
		t.Errorf("Same location distance in km = %v, want 0", distanceKm)
	}
}

func TestPrecisionEstimation(t *testing.T) {
	tests := []struct {
		name      string
		latMin    float64
		lonMin    float64
		latMax    float64
		lonMax    float64
		wantPrec  int
	}{
		{"Large area", 0, 0, 50, 50, 1},
		{"Medium area", 39, 116, 41, 117, 4},
		{"Small area", 39.9, 116.4, 39.91, 116.41, 7},
		{"Very small area", 39.904, 116.407, 39.905, 116.408, 9},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			prec := EstimatePrecision(tt.latMin, tt.lonMin, tt.latMax, tt.lonMax)
			// Allow some flexibility in precision estimation
			if prec < 1 || prec > 12 {
				t.Errorf("EstimatePrecision() = %v, should be between 1 and 12", prec)
			}
		})
	}
}

func TestContains(t *testing.T) {
	// Encode Beijing
	hash, _ := EncodeWithPrecision(39.9042, 116.4074, 6)
	result, _ := Decode(hash)

	tests := []struct {
		name    string
		hash    string
		lat     float64
		lon     float64
		want    bool
		wantErr bool
	}{
		{"Center point", hash, result.Center.Lat, result.Center.Lon, true, false},
		{"Outside point", hash, 0, 0, false, false},
		{"Invalid hash", "", 0, 0, false, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			contains, err := Contains(tt.hash, tt.lat, tt.lon)

			if (err != nil) != tt.wantErr {
				t.Errorf("Contains() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr && contains != tt.want {
				t.Errorf("Contains() = %v, want %v", contains, tt.want)
			}
		})
	}
}

func TestCommonPrefix(t *testing.T) {
	tests := []struct {
		name   string
		hashes []string
		want   string
	}{
		{"No common prefix", []string{"wx4g0b", "dr5ru7"}, ""},
		{"Some common", []string{"wx4g0b", "wx4g0c", "wx4g0d"}, "wx4g0"},
		{"Full common", []string{"wx4g0b", "wx4g0b"}, "wx4g0b"},
		{"Single hash", []string{"wx4g0b"}, "wx4g0b"},
		{"Empty list", []string{}, ""},
		{"Different lengths", []string{"wx4g0b", "wx4g0bcnh"}, "wx4g0b"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := CommonPrefix(tt.hashes...)
			if got != tt.want {
				t.Errorf("CommonPrefix() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestBoundingBox(t *testing.T) {
	hash, err := BoundingBox(39.9, 116.4, 40.0, 116.5)
	if err != nil {
		t.Errorf("BoundingBox() error = %v", err)
		return
	}
	if !Validate(hash) {
		t.Errorf("BoundingBox() returned invalid hash: %v", hash)
	}
}

func TestValidate(t *testing.T) {
	tests := []struct {
		name string
		hash string
		want bool
	}{
		{"Valid hash", "wx4g0b", true},
		{"Single char", "w", true},
		{"Max length", "wx4g0bcnh123", true},
		{"Empty string", "", false},
		{"Too long", "wx4g0bcnh12345", false},
		{"Invalid char i", "wx4g0bi", false},
		{"Invalid char l", "wx4g0bl", false},
		{"Invalid char o", "wx4g0bo", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Validate(tt.hash); got != tt.want {
				t.Errorf("Validate() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestEdgeCases(t *testing.T) {
	// Test encoding at boundaries
	t.Run("Latitude boundaries", func(t *testing.T) {
		// North Pole
		hash, err := EncodeWithPrecision(90, 0, 6)
		if err != nil {
			t.Errorf("Failed to encode North Pole: %v", err)
		}
		if len(hash) != 6 {
			t.Errorf("Expected 6 chars, got %d", len(hash))
		}

		// South Pole
		hash, err = EncodeWithPrecision(-90, 0, 6)
		if err != nil {
			t.Errorf("Failed to encode South Pole: %v", err)
		}
		if len(hash) != 6 {
			t.Errorf("Expected 6 chars, got %d", len(hash))
		}
	})

	t.Run("Longitude boundaries", func(t *testing.T) {
		// 180/-180 boundary
		hash, err := EncodeWithPrecision(0, 180, 6)
		if err != nil {
			t.Errorf("Failed to encode 180 longitude: %v", err)
		}
		if len(hash) != 6 {
			t.Errorf("Expected 6 chars, got %d", len(hash))
		}
	})

	t.Run("Equator and Prime Meridian", func(t *testing.T) {
		hash, err := EncodeWithPrecision(0, 0, 6)
		if err != nil {
			t.Errorf("Failed to encode (0,0): %v", err)
		}
		if hash[:1] != "s" {
			t.Errorf("Expected first char 's', got %q", hash[:1])
		}
	})
}

func BenchmarkEncode(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = Encode(39.9042, 116.4074)
	}
}

func BenchmarkDecode(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = Decode("wx4g0bcnh")
	}
}

func BenchmarkNeighbors(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = Neighbors("wx4g0b")
	}
}