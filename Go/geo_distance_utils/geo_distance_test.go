package geo_distance_utils

import (
	"math"
	"testing"
)

// ============================================================================
// Validation Tests
// ============================================================================

func TestIsValidCoordinate(t *testing.T) {
	tests := []struct {
		lat, lon float64
		expected bool
	}{
		{0, 0, true},
		{90, 180, true},
		{-90, -180, true},
		{45.5, -122.5, true},
		{91, 0, false},
		{-91, 0, false},
		{0, 181, false},
		{0, -181, false},
	}

	for _, tt := range tests {
		result := IsValidCoordinate(tt.lat, tt.lon)
		if result != tt.expected {
			t.Errorf("IsValidCoordinate(%f, %f) = %v, want %v", tt.lat, tt.lon, result, tt.expected)
		}
	}
}

func TestNormalizeCoordinate(t *testing.T) {
	tests := []struct {
		lat, lon       float64
		expectedLat    float64
		expectedLonMin float64
		expectedLonMax float64
	}{
		{0, 0, 0, -1, 1},              // Normal coordinate
		{100, 0, 90, -1, 1},           // Latitude clamped
		{-100, 0, -90, -1, 1},         // Latitude clamped
		{0, 200, 0, -180, 180},        // Longitude wrapped
		{0, -200, 0, -180, 180},       // Longitude wrapped
		{45, 370, 45, 9, 11},          // Longitude normalized (370 -> 10)
	}

	for _, tt := range tests {
		result := NormalizeCoordinate(tt.lat, tt.lon)
		if result.Lat != tt.expectedLat {
			t.Errorf("NormalizeCoordinate(%f, %f).Lat = %f, want %f", tt.lat, tt.lon, result.Lat, tt.expectedLat)
		}
		if result.Lon < tt.expectedLonMin || result.Lon > tt.expectedLonMax {
			t.Errorf("NormalizeCoordinate(%f, %f).Lon = %f, out of range [%f, %f]", tt.lat, tt.lon, result.Lon, tt.expectedLonMin, tt.expectedLonMax)
		}
	}
}

func TestNormalizeLongitude(t *testing.T) {
	tests := []struct {
		input    float64
		expected float64
	}{
		{0, 0},
		{180, 180},
		{-180, -180},
		{181, -179},
		{-181, 179},
		{360, 0},
		{-360, 0},
		{540, 180},
	}

	for _, tt := range tests {
		result := NormalizeLongitude(tt.input)
		// Allow small floating point tolerance
		if math.Abs(result-tt.expected) > 0.0001 {
			t.Errorf("NormalizeLongitude(%f) = %f, want %f", tt.input, result, tt.expected)
		}
	}
}

// ============================================================================
// Haversine Distance Tests
// ============================================================================

func TestHaversineDistance(t *testing.T) {
	tests := []struct {
		name     string
		c1       Coordinate
		c2       Coordinate
		unit     DistanceUnit
		expected float64
		tolerance float64
	}{
		{
			name:      "Beijing to Shanghai",
			c1:        Coordinate{Lat: 39.9042, Lon: 116.4074},
			c2:        Coordinate{Lat: 31.2304, Lon: 121.4737},
			unit:      UnitKM,
			expected:  1068.0,
			tolerance: 5.0,
		},
		{
			name:      "Same point",
			c1:        Coordinate{Lat: 40.0, Lon: -74.0},
			c2:        Coordinate{Lat: 40.0, Lon: -74.0},
			unit:      UnitKM,
			expected:  0,
			tolerance: 0.01,
		},
		{
			name:      "Equator 1 degree longitude",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			unit:      UnitKM,
			expected:  111.19,
			tolerance: 0.5,
		},
		{
			name:      "North Pole to Equator",
			c1:        Coordinate{Lat: 90, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 0},
			unit:      UnitKM,
			expected:  10000.0,
			tolerance: 100.0,
		},
		{
			name:      "Half around world",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 180},
			unit:      UnitKM,
			expected:  20015.0,
			tolerance: 50.0,
		},
		{
			name:      "New York to London",
			c1:        Coordinate{Lat: 40.7128, Lon: -74.0060},
			c2:        Coordinate{Lat: 51.5074, Lon: -0.1278},
			unit:      UnitKM,
			expected:  5570.0,
			tolerance: 20.0,
		},
		{
			name:      "Distance in miles",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			unit:      UnitMiles,
			expected:  69.1,
			tolerance: 0.5,
		},
		{
			name:      "Distance in nautical miles",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			unit:      UnitNautical,
			expected:  60.0,
			tolerance: 0.5,
		},
		{
			name:      "Distance in meters",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			unit:      UnitM,
			expected:  111190.0,
			tolerance: 500.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := HaversineDistance(tt.c1, tt.c2, tt.unit)
			if err != nil {
				t.Fatalf("HaversineDistance error: %v", err)
			}
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("HaversineDistance() = %f, want approximately %f", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Vincenty Distance Tests
// ============================================================================

func TestVincentyDistance(t *testing.T) {
	tests := []struct {
		name      string
		c1        Coordinate
		c2        Coordinate
		unit      DistanceUnit
		expected  float64
		tolerance float64
	}{
		{
			name:      "Beijing to Shanghai",
			c1:        Coordinate{Lat: 39.9042, Lon: 116.4074},
			c2:        Coordinate{Lat: 31.2304, Lon: 121.4737},
			unit:      UnitKM,
			expected:  1067.0,
			tolerance: 5.0,
		},
		{
			name:      "Same point",
			c1:        Coordinate{Lat: 40.0, Lon: -74.0},
			c2:        Coordinate{Lat: 40.0, Lon: -74.0},
			unit:      UnitKM,
			expected:  0,
			tolerance: 0.01,
		},
		{
			name:      "Equator 1 degree longitude",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			unit:      UnitKM,
			expected:  111.32,
			tolerance: 0.5,
		},
		{
			name:      "New York to London",
			c1:        Coordinate{Lat: 40.7128, Lon: -74.0060},
			c2:        Coordinate{Lat: 51.5074, Lon: -0.1278},
			unit:      UnitKM,
			expected:  5570.0,
			tolerance: 20.0,
		},
		{
			name:      "Sydney to Perth",
			c1:        Coordinate{Lat: -33.8688, Lon: 151.2093},
			c2:        Coordinate{Lat: -31.9505, Lon: 115.8605},
			unit:      UnitKM,
			expected:  3290.0,
			tolerance: 30.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := VincentyDistance(tt.c1, tt.c2, tt.unit)
			if err != nil {
				t.Fatalf("VincentyDistance error: %v", err)
			}
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("VincentyDistance() = %f, want approximately %f", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Distance Function Tests
// ============================================================================

func TestDistance(t *testing.T) {
	c1 := Coordinate{Lat: 39.9042, Lon: 116.4074}
	c2 := Coordinate{Lat: 31.2304, Lon: 121.4737}

	// Test haversine method
	haversineDist, err := Distance(c1, c2, UnitKM, MethodHaversine)
	if err != nil {
		t.Fatalf("Distance with haversine error: %v", err)
	}
	if math.Abs(haversineDist-1068) > 5 {
		t.Errorf("Distance(haversine) = %f, want approximately 1068 km", haversineDist)
	}

	// Test vincenty method
	vincentyDist, err := Distance(c1, c2, UnitKM, MethodVincenty)
	if err != nil {
		t.Fatalf("Distance with vincenty error: %v", err)
	}
	if math.Abs(vincentyDist-1067) > 5 {
		t.Errorf("Distance(vincenty) = %f, want approximately 1067 km", vincentyDist)
	}

	// Test invalid method
	_, err = Distance(c1, c2, UnitKM, "invalid")
	if err == nil {
		t.Error("Distance should return error for invalid method")
	}
}

// ============================================================================
// Bearing Tests
// ============================================================================

func TestInitialBearing(t *testing.T) {
	tests := []struct {
		name     string
		c1       Coordinate
		c2       Coordinate
		expected float64
		tolerance float64
	}{
		{
			name:      "North",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 1, Lon: 0},
			expected:  0,
			tolerance: 1,
		},
		{
			name:      "East",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: 1},
			expected:  90,
			tolerance: 1,
		},
		{
			name:      "South",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: -1, Lon: 0},
			expected:  180,
			tolerance: 1,
		},
		{
			name:      "West",
			c1:        Coordinate{Lat: 0, Lon: 0},
			c2:        Coordinate{Lat: 0, Lon: -1},
			expected:  270,
			tolerance: 1,
		},
		{
			name:      "Beijing to Shanghai",
			c1:        Coordinate{Lat: 39.9042, Lon: 116.4074},
			c2:        Coordinate{Lat: 31.2304, Lon: 121.4737},
			expected:  153,
			tolerance: 5,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := InitialBearing(tt.c1, tt.c2)
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("InitialBearing() = %f, want approximately %f", result, tt.expected)
			}
		})
	}
}

func TestFinalBearing(t *testing.T) {
	// Final bearing should be initial bearing from end to start, reversed
	c1 := Coordinate{Lat: 0, Lon: 0}
	c2 := Coordinate{Lat: 0, Lon: 1}

	finalBearing := FinalBearing(c1, c2)
	// For traveling east, final bearing should be close to 90 (east)
	if math.Abs(finalBearing-90) > 1 {
		t.Errorf("FinalBearing() = %f, want approximately 90", finalBearing)
	}
}

// ============================================================================
// Midpoint Tests
// ============================================================================

func TestMidpoint(t *testing.T) {
	tests := []struct {
		name         string
		c1           Coordinate
		c2           Coordinate
		expectedLat  float64
		expectedLon  float64
		tolerance    float64
	}{
		{
			name:        "Same longitude",
			c1:          Coordinate{Lat: 0, Lon: 0},
			c2:          Coordinate{Lat: 0, Lon: 10},
			expectedLat: 0,
			expectedLon: 5,
			tolerance:   0.1,
		},
		{
			name:        "Same latitude",
			c1:          Coordinate{Lat: 0, Lon: 0},
			c2:          Coordinate{Lat: 10, Lon: 0},
			expectedLat: 5,
			expectedLon: 0,
			tolerance:   0.1,
		},
		{
			name:        "Diagonal",
			c1:          Coordinate{Lat: 40, Lon: -74},
			c2:          Coordinate{Lat: 34, Lon: -118},
			expectedLat: 37.1,  // Actually about 37.1 for this diagonal
			expectedLon: -96,
			tolerance:   2.0,  // Increased tolerance for longer distances
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Midpoint(tt.c1, tt.c2)
			if math.Abs(result.Lat-tt.expectedLat) > tt.tolerance {
				t.Errorf("Midpoint().Lat = %f, want approximately %f", result.Lat, tt.expectedLat)
			}
			if math.Abs(result.Lon-tt.expectedLon) > tt.tolerance {
				t.Errorf("Midpoint().Lon = %f, want approximately %f", result.Lon, tt.expectedLon)
			}
		})
	}
}

// ============================================================================
// Destination Point Tests
// ============================================================================

func TestDestinationPoint(t *testing.T) {
	tests := []struct {
		name        string
		start       Coordinate
		bearing     float64
		distanceKM  float64
		expectedLat float64
		expectedLon float64
		tolerance   float64
	}{
		{
			name:        "North 1 degree",
			start:       Coordinate{Lat: 0, Lon: 0},
			bearing:     0,
			distanceKM:  111.19,
			expectedLat: 1.0,
			expectedLon: 0,
			tolerance:   0.1,
		},
		{
			name:        "East 1 degree",
			start:       Coordinate{Lat: 0, Lon: 0},
			bearing:     90,
			distanceKM:  111.19,
			expectedLat: 0,
			expectedLon: 1.0,
			tolerance:   0.1,
		},
		{
			name:        "South 1 degree",
			start:       Coordinate{Lat: 1, Lon: 0},
			bearing:     180,
			distanceKM:  111.19,
			expectedLat: 0,
			expectedLon: 0,
			tolerance:   0.1,
		},
		{
			name:        "West 1 degree",
			start:       Coordinate{Lat: 0, Lon: 1},
			bearing:     270,
			distanceKM:  111.19,
			expectedLat: 0,
			expectedLon: 0,
			tolerance:   0.1,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := DestinationPoint(tt.start, tt.bearing, tt.distanceKM)
			if math.Abs(result.Lat-tt.expectedLat) > tt.tolerance {
				t.Errorf("DestinationPoint().Lat = %f, want approximately %f", result.Lat, tt.expectedLat)
			}
			if math.Abs(result.Lon-tt.expectedLon) > tt.tolerance {
				t.Errorf("DestinationPoint().Lon = %f, want approximately %f", result.Lon, tt.expectedLon)
			}
		})
	}
}

// ============================================================================
// Bounding Box Tests
// ============================================================================

func TestBoundingBox(t *testing.T) {
	tests := []struct {
		name      string
		center    Coordinate
		radiusKM  float64
		checkLat  func(float64, float64) bool
		checkLon  func(float64, float64) bool
	}{
		{
			name:     "Equator 10km",
			center:   Coordinate{Lat: 0, Lon: 0},
			radiusKM: 10,
			checkLat: func(min, max float64) bool {
				return min < 0 && max > 0 && math.Abs(max-min) < 0.2
			},
			checkLon: func(min, max float64) bool {
				return min < 0 && max > 0 && math.Abs(max-min) < 0.2
			},
		},
		{
			name:     "Beijing 50km",
			center:   Coordinate{Lat: 39.9, Lon: 116.4},
			radiusKM: 50,
			checkLat: func(min, max float64) bool {
				return min < 39.9 && max > 39.9 && math.Abs(max-min) < 1
			},
			checkLon: func(min, max float64) bool {
				// For Beijing at 39.9° latitude, longitude spread should be larger than latitude spread
				// cos(39.9°) ≈ 0.76, so longitude offset is about 1/0.76 ≈ 1.3 times larger
				return min < 116.4 && max > 116.4 && math.Abs(max-min) > 0.5 && math.Abs(max-min) < 2
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			bounds := BoundingBox(tt.center, tt.radiusKM)
			if !tt.checkLat(bounds.MinLat, bounds.MaxLat) {
				t.Errorf("BoundingBox lat bounds invalid: min=%f, max=%f", bounds.MinLat, bounds.MaxLat)
			}
			if !tt.checkLon(bounds.MinLon, bounds.MaxLon) {
				t.Errorf("BoundingBox lon bounds invalid: min=%f, max=%f", bounds.MinLon, bounds.MaxLon)
			}
		})
	}
}

// ============================================================================
// Point In Polygon Tests
// ============================================================================

func TestPointInPolygon(t *testing.T) {
	// Simple square around Beijing
	polygon := []Coordinate{
		{Lat: 39, Lon: 116},
		{Lat: 40, Lon: 116},
		{Lat: 40, Lon: 117},
		{Lat: 39, Lon: 117},
	}

	tests := []struct {
		name     string
		point    Coordinate
		expected bool
	}{
		{"Inside", Coordinate{Lat: 39.5, Lon: 116.5}, true},
		{"Outside west", Coordinate{Lat: 39.5, Lon: 115}, false},
		{"Outside north", Coordinate{Lat: 41, Lon: 116.5}, false},
		{"On edge", Coordinate{Lat: 39.5, Lon: 116}, true}, // On edge is considered inside
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := PointInPolygon(tt.point, polygon)
			if result != tt.expected {
				t.Errorf("PointInPolygon() = %v, want %v", result, tt.expected)
			}
		})
	}

	// Test with triangle
	triangle := []Coordinate{
		{Lat: 0, Lon: 0},
		{Lat: 0, Lon: 10},
		{Lat: 10, Lon: 5},
	}

	if !PointInPolygon(Coordinate{Lat: 3, Lon: 5}, triangle) {
		t.Error("Point should be inside triangle")
	}
	if PointInPolygon(Coordinate{Lat: -1, Lon: 5}, triangle) {
		t.Error("Point should be outside triangle")
	}
}

// ============================================================================
// Polygon Area Tests
// ============================================================================

func TestPolygonAreaKM2(t *testing.T) {
	tests := []struct {
		name      string
		polygon   []Coordinate
		expected  float64
		tolerance float64
	}{
		{
			name: "1 degree square at equator",
			polygon: []Coordinate{
				{Lat: 0, Lon: 0},
				{Lat: 0, Lon: 1},
				{Lat: 1, Lon: 1},
				{Lat: 1, Lon: 0},
			},
			expected:  12364, // Approximately 111km x 111km
			tolerance: 200,
		},
		{
			name: "Triangle",
			polygon: []Coordinate{
				{Lat: 0, Lon: 0},
				{Lat: 0, Lon: 10},
				{Lat: 10, Lon: 5},
			},
			expected:  610000, // Approximately
			tolerance: 50000,
		},
		{
			name: "Less than 3 points",
			polygon: []Coordinate{
				{Lat: 0, Lon: 0},
				{Lat: 0, Lon: 1},
			},
			expected:  0,
			tolerance: 0.01,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := PolygonAreaKM2(tt.polygon)
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("PolygonAreaKM2() = %f, want approximately %f", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Path Interpolation Tests
// ============================================================================

func TestInterpolatePath(t *testing.T) {
	// Test simple path
	points := InterpolatePath(Coordinate{Lat: 0, Lon: 0}, Coordinate{Lat: 0, Lon: 10}, 5)

	if len(points) != 6 { // numPoints + 1
		t.Errorf("InterpolatePath returned %d points, want 6", len(points))
	}

	// First and last should match endpoints
	if points[0].Lat != 0 || points[0].Lon != 0 {
		t.Errorf("First point should be start, got %v", points[0])
	}
	if points[5].Lat != 0 || math.Abs(points[5].Lon-10) > 0.01 {
		t.Errorf("Last point should be end, got %v", points[5])
	}

	// Middle points should have longitude increasing
	for i := 1; i < 5; i++ {
		if points[i].Lat < -0.01 || points[i].Lat > 0.01 {
			t.Errorf("Middle point %d should have lat ≈ 0, got %f", i, points[i].Lat)
		}
	}
}

func TestTotalPathDistance(t *testing.T) {
	tests := []struct {
		name      string
		path      []Coordinate
		unit      DistanceUnit
		expected  float64
		tolerance float64
	}{
		{
			name: "Straight line 2 degrees",
			path: []Coordinate{
				{Lat: 0, Lon: 0},
				{Lat: 0, Lon: 1},
				{Lat: 0, Lon: 2},
			},
			unit:      UnitKM,
			expected:  222.38,
			tolerance: 1.0,
		},
		{
			name: "Single point",
			path: []Coordinate{
				{Lat: 0, Lon: 0},
			},
			unit:      UnitKM,
			expected:  0,
			tolerance: 0.01,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := TotalPathDistance(tt.path, tt.unit)
			if err != nil {
				t.Fatalf("TotalPathDistance error: %v", err)
			}
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("TotalPathDistance() = %f, want approximately %f", result, tt.expected)
			}
		})
	}
}

func TestNearestPointOnPath(t *testing.T) {
	path := []Coordinate{
		{Lat: 0, Lon: 0},
		{Lat: 0, Lon: 10},
	}

	// Point directly on the path
	result, err := NearestPointOnPath(Coordinate{Lat: 1, Lon: 5}, path)
	if err != nil {
		t.Fatalf("NearestPointOnPath error: %v", err)
	}

	// Nearest point should have longitude close to 5
	if math.Abs(result.NearestPoint.Lon-5) > 0.1 {
		t.Errorf("NearestPointOnPath().Lon = %f, want approximately 5", result.NearestPoint.Lon)
	}

	// Distance should be about 111km (1 degree latitude)
	if math.Abs(result.DistanceKM-111) > 1 {
		t.Errorf("NearestPointOnPath().DistanceKM = %f, want approximately 111", result.DistanceKM)
	}
}

// ============================================================================
// Batch Operations Tests
// ============================================================================

func TestFindNearest(t *testing.T) {
	candidates := []Coordinate{
		{Lat: 40, Lon: 116},
		{Lat: 35, Lon: 117},
		{Lat: 30, Lon: 120},
	}

	result, err := FindNearest(Coordinate{Lat: 39, Lon: 116}, candidates, UnitKM)
	if err != nil {
		t.Fatalf("FindNearest error: %v", err)
	}

	// First candidate should be nearest
	if result.Index != 0 {
		t.Errorf("FindNearest().Index = %d, want 0", result.Index)
	}
	if result.Coordinate.Lat != 40 || result.Coordinate.Lon != 116 {
		t.Errorf("FindNearest().Coordinate = %v, want {40, 116}", result.Coordinate)
	}
}

func TestDistancesToAll(t *testing.T) {
	point := Coordinate{Lat: 0, Lon: 0}
	targets := []Coordinate{
		{Lat: 0, Lon: 1},
		{Lat: 1, Lon: 0},
		{Lat: 0, Lon: 2},
	}

	distances, err := DistancesToAll(point, targets, UnitKM)
	if err != nil {
		t.Fatalf("DistancesToAll error: %v", err)
	}

	if len(distances) != 3 {
		t.Errorf("DistancesToAll returned %d distances, want 3", len(distances))
	}

	// First two should be approximately equal (1 degree)
	if math.Abs(distances[0]-distances[1]) > 1 {
		t.Errorf("distances[0] and distances[1] should be similar: %f vs %f", distances[0], distances[1])
	}

	// Third should be about double the first
	if math.Abs(distances[2]-distances[0]*2) > 5 {
		t.Errorf("distances[2] should be about double distances[0]: %f vs %f", distances[2], distances[0]*2)
	}
}

func TestWithinRadius(t *testing.T) {
	candidates := []Coordinate{
		{Lat: 0, Lon: 1},   // ~111 km
		{Lat: 0, Lon: 2},   // ~222 km
		{Lat: 0, Lon: 0.5}, // ~55.5 km
	}

	results, err := WithinRadius(Coordinate{Lat: 0, Lon: 0}, candidates, 150, UnitKM)
	if err != nil {
		t.Fatalf("WithinRadius error: %v", err)
	}

	// Should find 2 points (1 degree and 0.5 degree)
	if len(results) != 2 {
		t.Errorf("WithinRadius returned %d results, want 2", len(results))
	}
}

// ============================================================================
// Coordinate Format Tests
// ============================================================================

func TestDecimalToDMS(t *testing.T) {
	tests := []struct {
		lat, lon       float64
		expectedLatDeg int
		expectedLatMin int
		expectedLonDeg int
		expectedLonDir string
	}{
		{39.9042, 116.4074, 39, 54, 116, "E"},
		{-33.8688, -151.2093, 33, 52, 151, "W"},
		{0, 0, 0, 0, 0, "E"},
	}

	for _, tt := range tests {
		result := DecimalToDMS(tt.lat, tt.lon)
		if result.Lat.Degrees != tt.expectedLatDeg {
			t.Errorf("DecimalToDMS(%f, %f).Lat.Degrees = %d, want %d", tt.lat, tt.lon, result.Lat.Degrees, tt.expectedLatDeg)
		}
		if result.Lat.Minutes != tt.expectedLatMin {
			t.Errorf("DecimalToDMS(%f, %f).Lat.Minutes = %d, want %d", tt.lat, tt.lon, result.Lat.Minutes, tt.expectedLatMin)
		}
		if result.Lon.Degrees != tt.expectedLonDeg {
			t.Errorf("DecimalToDMS(%f, %f).Lon.Degrees = %d, want %d", tt.lat, tt.lon, result.Lon.Degrees, tt.expectedLonDeg)
		}
		if result.Lon.Direction != tt.expectedLonDir {
			t.Errorf("DecimalToDMS(%f, %f).Lon.Direction = %s, want %s", tt.lat, tt.lon, result.Lon.Direction, tt.expectedLonDir)
		}
	}
}

func TestDMSToDecimal(t *testing.T) {
	latDMS := DMS{Degrees: 39, Minutes: 54, Seconds: 15.12, Direction: "N"}
	lonDMS := DMS{Degrees: 116, Minutes: 24, Seconds: 26.64, Direction: "E"}

	result := DMSToDecimal(latDMS, lonDMS)

	expectedLat := 39.9042
	expectedLon := 116.4074

	if math.Abs(result.Lat-expectedLat) > 0.001 {
		t.Errorf("DMSToDecimal().Lat = %f, want approximately %f", result.Lat, expectedLat)
	}
	if math.Abs(result.Lon-expectedLon) > 0.001 {
		t.Errorf("DMSToDecimal().Lon = %f, want approximately %f", result.Lon, expectedLon)
	}

	// Test negative directions
	latDMS2 := DMS{Degrees: 33, Minutes: 52, Seconds: 7.68, Direction: "S"}
	lonDMS2 := DMS{Degrees: 151, Minutes: 12, Seconds: 33.48, Direction: "W"}

	result2 := DMSToDecimal(latDMS2, lonDMS2)

	if result2.Lat > 0 {
		t.Errorf("DMSToDecimal().Lat should be negative for S direction, got %f", result2.Lat)
	}
	if result2.Lon > 0 {
		t.Errorf("DMSToDecimal().Lon should be negative for W direction, got %f", result2.Lon)
	}
}

func TestCoordinateToString(t *testing.T) {
	coord := Coordinate{Lat: 39.9042, Lon: 116.4074}

	// Test decimal format
	decimalStr := CoordinateToString(coord, "decimal", 4)
	if decimalStr == "" {
		t.Error("CoordinateToString(decimal) returned empty string")
	}

	// Test DMS format
	dmsStr := CoordinateToString(coord, "dms", 0)
	if dmsStr == "" {
		t.Error("CoordinateToString(dms) returned empty string")
	}

	// Test DM format
	dmStr := CoordinateToString(coord, "dm", 0)
	if dmStr == "" {
		t.Error("CoordinateToString(dm) returned empty string")
	}

	// Test negative coordinates
	negCoord := Coordinate{Lat: -33.8688, Lon: -151.2093}
	negStr := CoordinateToString(negCoord, "decimal", 4)
	if negStr == "" {
		t.Error("CoordinateToString for negative coords returned empty string")
	}
}

// ============================================================================
// Unit Conversion Tests
// ============================================================================

func TestUnitConversions(t *testing.T) {
	tests := []struct {
		name     string
		value    float64
		fromUnit DistanceUnit
		toUnit   DistanceUnit
		expected float64
		tolerance float64
	}{
		{"km to miles", 100, UnitKM, UnitMiles, 62.1371, 0.01},
		{"km to nautical", 100, UnitKM, UnitNautical, 53.9957, 0.01},
		{"km to m", 1, UnitKM, UnitM, 1000, 0.01},
		{"miles to km", 100, UnitMiles, UnitKM, 160.9344, 0.01},
		{"nautical to km", 100, UnitNautical, UnitKM, 185.2, 0.01},
		{"m to km", 1000, UnitM, UnitKM, 1, 0.01},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ConvertDistance(tt.value, tt.fromUnit, tt.toUnit)
			if err != nil {
				t.Fatalf("ConvertDistance error: %v", err)
			}
			if math.Abs(result-tt.expected) > tt.tolerance {
				t.Errorf("ConvertDistance() = %f, want %f", result, tt.expected)
			}
		})
	}

	// Test convenience functions
	if math.Abs(ConvertKMToMiles(100)-62.1371) > 0.01 {
		t.Error("ConvertKMToMiles conversion error")
	}
	if math.Abs(ConvertKMToNautical(100)-53.9957) > 0.01 {
		t.Error("ConvertKMToNautical conversion error")
	}
	if math.Abs(ConvertKMToM(1)-1000) > 0.01 {
		t.Error("ConvertKMToM conversion error")
	}
	if math.Abs(ConvertMilesToKM(100)-160.9344) > 0.01 {
		t.Error("ConvertMilesToKM conversion error")
	}
	if math.Abs(ConvertNauticalToKM(100)-185.2) > 0.01 {
		t.Error("ConvertNauticalToKM conversion error")
	}
	if math.Abs(ConvertMToKM(1000)-1) > 0.01 {
		t.Error("ConvertMToKM conversion error")
	}
}

// ============================================================================
// Edge Cases and Error Tests
// ============================================================================

func TestInvalidUnit(t *testing.T) {
	_, err := HaversineDistance(Coordinate{Lat: 0, Lon: 0}, Coordinate{Lat: 1, Lon: 1}, "invalid")
	if err == nil {
		t.Error("HaversineDistance should return error for invalid unit")
	}
}

func TestEmptyCandidates(t *testing.T) {
	_, err := FindNearest(Coordinate{Lat: 0, Lon: 0}, []Coordinate{}, UnitKM)
	if err == nil {
		t.Error("FindNearest should return error for empty candidates")
	}
}

func TestInvalidPath(t *testing.T) {
	_, err := NearestPointOnPath(Coordinate{Lat: 0, Lon: 0}, []Coordinate{})
	if err == nil {
		t.Error("NearestPointOnPath should return error for empty path")
	}
}

func TestSmallPolygon(t *testing.T) {
	// Polygon with less than 3 vertices
	result := PointInPolygon(Coordinate{Lat: 0, Lon: 0}, []Coordinate{
		{Lat: 0, Lon: 0},
		{Lat: 1, Lon: 1},
	})
	if result {
		t.Error("PointInPolygon should return false for polygon with < 3 vertices")
	}
}

func TestZeroDistance(t *testing.T) {
	coord := Coordinate{Lat: 40.7128, Lon: -74.0060}
	dist, err := HaversineDistance(coord, coord, UnitKM)
	if err != nil {
		t.Fatalf("HaversineDistance error: %v", err)
	}
	if dist != 0 {
		t.Errorf("HaversineDistance for same point = %f, want 0", dist)
	}

	dist2, err := VincentyDistance(coord, coord, UnitKM)
	if err != nil {
		t.Fatalf("VincentyDistance error: %v", err)
	}
	if dist2 != 0 {
		t.Errorf("VincentyDistance for same point = %f, want 0", dist2)
	}
}

// ============================================================================
// Benchmark Tests
// ============================================================================

func BenchmarkHaversineDistance(b *testing.B) {
	c1 := Coordinate{Lat: 39.9042, Lon: 116.4074}
	c2 := Coordinate{Lat: 31.2304, Lon: 121.4737}
	for i := 0; i < b.N; i++ {
		HaversineDistance(c1, c2, UnitKM)
	}
}

func BenchmarkVincentyDistance(b *testing.B) {
	c1 := Coordinate{Lat: 39.9042, Lon: 116.4074}
	c2 := Coordinate{Lat: 31.2304, Lon: 121.4737}
	for i := 0; i < b.N; i++ {
		VincentyDistance(c1, c2, UnitKM)
	}
}

func BenchmarkPointInPolygon(b *testing.B) {
	polygon := []Coordinate{
		{Lat: 39, Lon: 116},
		{Lat: 40, Lon: 116},
		{Lat: 40, Lon: 117},
		{Lat: 39, Lon: 117},
	}
	point := Coordinate{Lat: 39.5, Lon: 116.5}
	for i := 0; i < b.N; i++ {
		PointInPolygon(point, polygon)
	}
}

func BenchmarkFindNearest(b *testing.B) {
	point := Coordinate{Lat: 39, Lon: 116}
	candidates := make([]Coordinate, 1000)
	for i := range candidates {
		candidates[i] = Coordinate{Lat: float64(i % 90), Lon: float64(i % 180)}
	}
	for i := 0; i < b.N; i++ {
		FindNearest(point, candidates, UnitKM)
	}
}