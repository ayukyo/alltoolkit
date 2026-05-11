// Package geo_distance_utils provides comprehensive geographic distance calculation utilities.
// This package offers various algorithms for calculating distances, bearings, and other
// geographic operations with zero external dependencies.
//
// Features:
//   - Haversine distance (spherical Earth approximation)
//   - Vincenty distance (ellipsoidal Earth, WGS-84)
//   - Bearing calculations (initial and final)
//   - Midpoint and destination point calculations
//   - Bounding box for radius searches
//   - Point-in-polygon detection
//   - Great circle path interpolation
//   - Distance unit conversions
//   - Coordinate validation and normalization
//   - DMS (degrees-minutes-seconds) format conversions
package geo_distance_utils

import (
	"errors"
	"fmt"
	"math"
)

// ============================================================================
// Constants
// ============================================================================

// Earth radius constants
const (
	EarthRadiusKM       = 6371.0     // Mean Earth radius in kilometers
	EarthRadiusM        = 6371000.0  // Mean Earth radius in meters
	EarthRadiusMiles    = 3958.8     // Mean Earth radius in miles
	EarthRadiusNautical = 3440.065   // Mean Earth radius in nautical miles
)

// WGS-84 Ellipsoid parameters (for Vincenty formula)
const (
	WGS84SemiMajor = 6378137.0           // Semi-major axis (a) in meters
	WGS84SemiMinor = 6356752.314245      // Semi-minor axis (b) in meters
	WGS84Flattening = 1 / 298.257223563  // Flattening (f)
)

// Conversion factors
const (
	KMToMiles    = 0.621371
	KMToNautical = 0.539957
	MilesToKM    = 1.609344
	NauticalToKM = 1.852
	MToKM        = 0.001
)

// Coordinate bounds
const (
	MaxLatitude  = 90.0
	MinLatitude  = -90.0
	MaxLongitude = 180.0
	MinLongitude = -180.0
)

// Conversion constants
const (
	degToRad = math.Pi / 180.0
	radToDeg = 180.0 / math.Pi
)

// ============================================================================
// Error Definitions
// ============================================================================

var (
	ErrInvalidLatitude   = errors.New("latitude must be between -90 and 90")
	ErrInvalidLongitude  = errors.New("longitude must be between -180 and 180")
	ErrInvalidUnit       = errors.New("unknown unit: use 'km', 'm', 'miles', or 'nautical'")
	ErrInvalidMethod     = errors.New("unknown method: use 'haversine' or 'vincenty'")
	ErrInvalidFormat     = errors.New("unknown format: use 'decimal', 'dms', or 'dm'")
	ErrVincentyConverge  = errors.New("vincenty formula failed to converge")
	ErrEmptyCandidates   = errors.New("candidates list is empty")
	ErrInvalidPolygon     = errors.New("polygon must have at least 3 vertices")
	ErrInvalidPath        = errors.New("path must have at least 1 point")
)

// ============================================================================
// Types
// ============================================================================

// Coordinate represents a geographic coordinate (latitude, longitude)
type Coordinate struct {
	Lat float64
	Lon float64
}

// Coordinate3D represents a geographic coordinate with altitude
type Coordinate3D struct {
	Lat float64
	Lon float64
	Alt float64
}

// DistanceUnit represents distance measurement units
type DistanceUnit string

const (
	UnitKM       DistanceUnit = "km"
	UnitM        DistanceUnit = "m"
	UnitMiles    DistanceUnit = "miles"
	UnitNautical DistanceUnit = "nautical"
)

// Method represents distance calculation method
type Method string

const (
	MethodHaversine Method = "haversine"
	MethodVincenty  Method = "vincenty"
)

// DMS represents degrees, minutes, seconds format
type DMS struct {
	Degrees   int
	Minutes   int
	Seconds   float64
	Direction string
}

// CoordinateDMS represents a coordinate in DMS format
type CoordinateDMS struct {
	Lat DMS
	Lon DMS
}

// Bounds represents a geographic bounding box
type Bounds struct {
	MinLat float64
	MaxLat float64
	MinLon float64
	MaxLon float64
}

// PathResult contains information about nearest point on path
type PathResult struct {
	NearestPoint Coordinate
	DistanceKM   float64
	SegmentIndex int
}

// NearestResult contains information about nearest candidate
type NearestResult struct {
	Index      int
	Distance   float64
	Coordinate Coordinate
}

// ============================================================================
// Validation and Normalization
// ============================================================================

// IsValidCoordinate checks if a coordinate is valid
func IsValidCoordinate(lat, lon float64) bool {
	return lat >= MinLatitude && lat <= MaxLatitude &&
		lon >= MinLongitude && lon <= MaxLongitude
}

// NormalizeCoordinate normalizes a coordinate (clamps latitude, wraps longitude)
func NormalizeCoordinate(lat, lon float64) Coordinate {
	// Clamp latitude
	if lat < MinLatitude {
		lat = MinLatitude
	} else if lat > MaxLatitude {
		lat = MaxLatitude
	}

	// Wrap longitude to [-180, 180]
	lon = NormalizeLongitude(lon)

	return Coordinate{Lat: lat, Lon: lon}
}

// NormalizeLongitude normalizes longitude to [-180, 180] range
func NormalizeLongitude(lon float64) float64 {
	for lon < MinLongitude {
		lon += 360
	}
	for lon > MaxLongitude {
		lon -= 360
	}
	return lon
}

// Validate returns an error if coordinate is invalid
func Validate(lat, lon float64) error {
	if lat < MinLatitude || lat > MaxLatitude {
		return ErrInvalidLatitude
	}
	if lon < MinLongitude || lon > MaxLongitude {
		return ErrInvalidLongitude
	}
	return nil
}

// ============================================================================
// Distance Calculations
// ============================================================================

// HaversineDistance calculates the great-circle distance between two coordinates
// using the Haversine formula (assumes spherical Earth).
func HaversineDistance(c1, c2 Coordinate, unit DistanceUnit) (float64, error) {
	lat1 := c1.Lat * degToRad
	lat2 := c2.Lat * degToRad
	lon1 := c1.Lon * degToRad
	lon2 := c2.Lon * degToRad

	dlat := lat2 - lat1
	dlon := lon2 - lon1

	// Haversine formula
	a := math.Sin(dlat/2)*math.Sin(dlat/2) +
		math.Cos(lat1)*math.Cos(lat2)*math.Sin(dlon/2)*math.Sin(dlon/2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	distanceKM := EarthRadiusKM * c

	return convertFromKM(distanceKM, unit)
}

// VincentyDistance calculates distance using Vincenty's formulae for ellipsoidal Earth.
// More accurate than Haversine but may fail to converge for nearly antipodal points.
func VincentyDistance(c1, c2 Coordinate, unit DistanceUnit) (float64, error) {
	return VincentyDistanceWithIterations(c1, c2, unit, 200)
}

// VincentyDistanceWithIterations calculates Vincenty distance with custom max iterations.
func VincentyDistanceWithIterations(c1, c2 Coordinate, unit DistanceUnit, maxIterations int) (float64, error) {
	// Handle identical coordinates
	if c1.Lat == c2.Lat && c1.Lon == c2.Lon {
		return 0, nil
	}

	lat1 := c1.Lat * degToRad
	lat2 := c2.Lat * degToRad
	lon1 := c1.Lon * degToRad
	lon2 := c2.Lon * degToRad

	// WGS-84 parameters
	a := float64(WGS84SemiMajor)
	b := float64(WGS84SemiMinor)
	f := float64(WGS84Flattening)

	// Reduced latitudes
	U1 := math.Atan((1 - f) * math.Tan(lat1))
	U2 := math.Atan((1 - f) * math.Tan(lat2))

	L := lon2 - lon1
	lambda := L

	sinU1 := math.Sin(U1)
	cosU1 := math.Cos(U1)
	sinU2 := math.Sin(U2)
	cosU2 := math.Cos(U2)

	// Precompute common values
	cosU1cosU2 := cosU1 * cosU2
	sinU1sinU2 := sinU1 * sinU2
	cosU1sinU2 := cosU1 * sinU2
	sinU1cosU2 := sinU1 * cosU2

	// Variables needed after iteration
	var sinSigma, cosSigma, cosSqAlpha, cos2sigmaM float64

	// Iterative calculation
	var iteration int
	var lambdaPrev float64

	for iteration < maxIterations {
		iteration++

		sinLambda := math.Sin(lambda)
		cosLambda := math.Cos(lambda)

		sinSigmaSq := math.Pow(cosU2*sinLambda, 2) +
			math.Pow(cosU1sinU2-sinU1cosU2*cosLambda, 2)

		// Handle coincident points
		if sinSigmaSq < 1e-30 {
			return 0, nil
		}

		sinSigma = math.Sqrt(sinSigmaSq)
		cosSigma = sinU1sinU2 + cosU1cosU2*cosLambda

		// Prevent division by zero
		sinAlpha := cosU1cosU2 * sinLambda / sinSigma
		cosSqAlpha = 1 - sinAlpha*sinAlpha

		if cosSqAlpha > 1e-30 {
			cos2sigmaM = cosSigma - 2*sinU1sinU2/cosSqAlpha
		} else {
			cos2sigmaM = 0
		}

		C := f / 16 * cosSqAlpha * (4 + f*(4-3*cosSqAlpha))

		lambdaPrev = lambda
		lambda = L + (1-C)*f*sinAlpha*(math.Atan2(sinSigma, cosSigma)+
			C*sinSigma*(cos2sigmaM+C*cosSigma*(-1+2*cos2sigmaM*cos2sigmaM)))

		// Check convergence
		if math.Abs(lambda-lambdaPrev) < 1e-12 {
			break
		}
	}

	// Check for convergence
	if math.Abs(lambda-lambdaPrev) >= 1e-12 {
		return 0, ErrVincentyConverge
	}

	// Calculate distance
	uSq := cosSqAlpha * (a*a - b*b) / (b * b)
	A := 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
	B := uSq / 1024 * (256 + uSq*(-128+uSq*(74-47*uSq)))

	cos2sigmaM_sq := cos2sigmaM * cos2sigmaM
	sinSigma_sq := sinSigma * sinSigma
	deltaSigma := B * sinSigma * (cos2sigmaM + B/4*(cosSigma*(-1+2*cos2sigmaM_sq)-
		B/6*cos2sigmaM*(-3+4*sinSigma_sq)*(-3+4*cos2sigmaM_sq)))

	distanceM := b * A * (math.Atan2(sinSigma, cosSigma) - deltaSigma)

	// Ensure non-negative distance
	if distanceM < 0 {
		distanceM = 0
	}

	return convertFromKM(distanceM*MToKM, unit)
}

// Distance calculates distance between two coordinates using specified method.
func Distance(c1, c2 Coordinate, unit DistanceUnit, method Method) (float64, error) {
	switch method {
	case MethodHaversine:
		return HaversineDistance(c1, c2, unit)
	case MethodVincenty:
		return VincentyDistance(c1, c2, unit)
	default:
		return 0, ErrInvalidMethod
	}
}

// ============================================================================
// Bearing Calculations
// ============================================================================

// InitialBearing calculates the initial bearing from c1 to c2 in degrees [0, 360).
func InitialBearing(c1, c2 Coordinate) float64 {
	lat1 := c1.Lat * degToRad
	lat2 := c2.Lat * degToRad
	dlon := (c2.Lon - c1.Lon) * degToRad

	y := math.Sin(dlon) * math.Cos(lat2)
	x := math.Cos(lat1)*math.Sin(lat2) - math.Sin(lat1)*math.Cos(lat2)*math.Cos(dlon)

	bearing := math.Atan2(y, x) * radToDeg

	// Normalize to [0, 360)
	return math.Mod(bearing+360, 360)
}

// FinalBearing calculates the final bearing from c1 to c2.
func FinalBearing(c1, c2 Coordinate) float64 {
	// Final bearing is initial bearing from end to start, reversed
	bearing := InitialBearing(c2, c1)
	return math.Mod(bearing+180, 360)
}

// ============================================================================
// Coordinate Operations
// ============================================================================

// Midpoint calculates the geographic midpoint between two coordinates.
func Midpoint(c1, c2 Coordinate) Coordinate {
	lat1 := c1.Lat * degToRad
	lat2 := c2.Lat * degToRad
	lon1 := c1.Lon * degToRad

	dlon := (c2.Lon - c1.Lon) * degToRad

	Bx := math.Cos(lat2) * math.Cos(dlon)
	By := math.Cos(lat2) * math.Sin(dlon)

	latMid := math.Atan2(math.Sin(lat1)+math.Sin(lat2),
		math.Sqrt(math.Pow(math.Cos(lat1)+Bx, 2)+By*By))
	lonMid := lon1 + math.Atan2(By, math.Cos(lat1)+Bx)

	return Coordinate{
		Lat: latMid * radToDeg,
		Lon: NormalizeLongitude(lonMid * radToDeg),
	}
}

// DestinationPoint calculates destination point from start coordinate, bearing, and distance.
func DestinationPoint(start Coordinate, bearingDeg, distanceKM float64) Coordinate {
	lat1 := start.Lat * degToRad
	lon1 := start.Lon * degToRad
	bearingRad := bearingDeg * degToRad

	angularDist := distanceKM / EarthRadiusKM

	lat2 := math.Asin(math.Sin(lat1)*math.Cos(angularDist) +
		math.Cos(lat1)*math.Sin(angularDist)*math.Cos(bearingRad))

	lon2 := lon1 + math.Atan2(
		math.Sin(bearingRad)*math.Sin(angularDist)*math.Cos(lat1),
		math.Cos(angularDist)-math.Sin(lat1)*math.Sin(lat2))

	return Coordinate{
		Lat: lat2 * radToDeg,
		Lon: NormalizeLongitude(lon2 * radToDeg),
	}
}

// ============================================================================
// Bounding Box
// ============================================================================

// BoundingBox calculates bounding box for a radius search.
func BoundingBox(center Coordinate, radiusKM float64) Bounds {
	angularDist := radiusKM / EarthRadiusKM

	// Latitude bounds (same angular distance)
	latMin := center.Lat - angularDist*radToDeg
	latMax := center.Lat + angularDist*radToDeg

	// Longitude bounds (depends on latitude)
	latRad := center.Lat * degToRad
	var lonOffset float64
	if math.Abs(latRad) < math.Pi/2-1e-6 {
		lonOffset = angularDist / math.Cos(latRad) * radToDeg
	} else {
		lonOffset = 180 // At poles
	}

	lonMin := center.Lon - lonOffset
	lonMax := center.Lon + lonOffset

	// Clamp latitude
	if latMin < MinLatitude {
		latMin = MinLatitude
	}
	if latMax > MaxLatitude {
		latMax = MaxLatitude
	}

	return Bounds{
		MinLat: latMin,
		MaxLat: latMax,
		MinLon: NormalizeLongitude(lonMin),
		MaxLon: NormalizeLongitude(lonMax),
	}
}

// ============================================================================
// Polygon Operations
// ============================================================================

// PointInPolygon checks if a point is inside a geographic polygon using ray casting.
func PointInPolygon(point Coordinate, polygon []Coordinate) bool {
	if len(polygon) < 3 {
		return false
	}

	n := len(polygon)
	inside := false

	j := n - 1
	for i := 0; i < n; i++ {
		latI := polygon[i].Lat
		lonI := polygon[i].Lon
		latJ := polygon[j].Lat
		lonJ := polygon[j].Lon

		if (lonI > point.Lon) != (lonJ > point.Lon) &&
			point.Lat < (latJ-latI)*(point.Lon-lonI)/(lonJ-lonI)+latI {
			inside = !inside
		}

		j = i
	}

	return inside
}

// PolygonAreaKM2 calculates area of a geographic polygon on Earth's surface.
func PolygonAreaKM2(polygon []Coordinate) float64 {
	if len(polygon) < 3 {
		return 0
	}

	n := len(polygon)
	var areaRad float64

	for i := 0; i < n; i++ {
		latI := polygon[i].Lat * degToRad
		lonI := polygon[i].Lon * degToRad
		latJ := polygon[(i+1)%n].Lat * degToRad
		lonJ := polygon[(i+1)%n].Lon * degToRad

		areaRad += (lonJ - lonI) * (2 + math.Sin(latI) + math.Sin(latJ))
	}

	areaRad = math.Abs(areaRad) * EarthRadiusKM * EarthRadiusKM / 2
	return areaRad
}

// ============================================================================
// Path Operations
// ============================================================================

// InterpolatePath interpolates points along a great circle path.
func InterpolatePath(c1, c2 Coordinate, numPoints int) []Coordinate {
	if numPoints < 2 {
		return []Coordinate{c1, c2}
	}

	lat1 := c1.Lat * degToRad
	lat2 := c2.Lat * degToRad
	lon1 := c1.Lon * degToRad
	lon2 := c2.Lon * degToRad

	// Calculate angular distance
	d := math.Acos(math.Sin(lat1)*math.Sin(lat2) +
		math.Cos(lat1)*math.Cos(lat2)*math.Cos(lon2-lon1))

	if d < 1e-10 {
		// Points are essentially coincident
		result := make([]Coordinate, numPoints+1)
		for i := range result {
			result[i] = c1
		}
		return result
	}

	points := make([]Coordinate, numPoints+1)
	for i := 0; i <= numPoints; i++ {
		f := float64(i) / float64(numPoints)

		// Interpolate along great circle
		A := math.Sin((1-f)*d) / math.Sin(d)
		B := math.Sin(f*d) / math.Sin(d)

		x := A*math.Cos(lat1)*math.Cos(lon1) + B*math.Cos(lat2)*math.Cos(lon2)
		y := A*math.Cos(lat1)*math.Sin(lon1) + B*math.Cos(lat2)*math.Sin(lon2)
		z := A*math.Sin(lat1) + B*math.Sin(lat2)

		latRad := math.Atan2(z, math.Sqrt(x*x+y*y))
		lonRad := math.Atan2(y, x)

		points[i] = Coordinate{
			Lat: latRad * radToDeg,
			Lon: NormalizeLongitude(lonRad * radToDeg),
		}
	}

	return points
}

// TotalPathDistance calculates total distance along a path.
func TotalPathDistance(path []Coordinate, unit DistanceUnit) (float64, error) {
	if len(path) < 2 {
		return 0, nil
	}

	var total float64
	for i := 0; i < len(path)-1; i++ {
		d, err := HaversineDistance(path[i], path[i+1], UnitKM)
		if err != nil {
			return 0, err
		}
		total += d
	}

	return convertFromKM(total, unit)
}

// NearestPointOnPath finds the nearest point on a path to a given point.
func NearestPointOnPath(point Coordinate, path []Coordinate) (*PathResult, error) {
	if len(path) < 1 {
		return nil, ErrInvalidPath
	}

	if len(path) == 1 {
		dist, _ := HaversineDistance(point, path[0], UnitKM)
		return &PathResult{
			NearestPoint: path[0],
			DistanceKM:   dist,
			SegmentIndex: 0,
		}, nil
	}

	minDistance := math.Inf(1)
	var nearestPoint Coordinate
	var segmentIndex int

	for i := 0; i < len(path)-1; i++ {
		start := path[i]
		end := path[i+1]

		nearest := nearestOnSegment(point, start, end)
		dist, _ := HaversineDistance(point, nearest, UnitKM)

		if dist < minDistance {
			minDistance = dist
			nearestPoint = nearest
			segmentIndex = i
		}
	}

	return &PathResult{
		NearestPoint: nearestPoint,
		DistanceKM:   minDistance,
		SegmentIndex: segmentIndex,
	}, nil
}

// nearestOnSegment finds nearest point on a great circle segment
func nearestOnSegment(point, start, end Coordinate) Coordinate {
	bearingStartEnd := InitialBearing(start, end)
	bearingStartPoint := InitialBearing(start, point)
	distStartPoint, _ := HaversineDistance(start, point, UnitKM)

	// Cross-track distance
	dxt := math.Asin(math.Sin(distStartPoint/EarthRadiusKM)*
		math.Sin((bearingStartPoint-bearingStartEnd)*degToRad))

	// Along-track distance
	dat := math.Acos(math.Cos(distStartPoint/EarthRadiusKM)/math.Cos(dxt)) * EarthRadiusKM

	distStartEnd, _ := HaversineDistance(start, end, UnitKM)

	if dat < 0 {
		return start
	} else if dat > distStartEnd {
		return end
	}
	return DestinationPoint(start, bearingStartEnd, dat)
}

// ============================================================================
// Batch Operations
// ============================================================================

// FindNearest finds the nearest candidate to a point.
func FindNearest(point Coordinate, candidates []Coordinate, unit DistanceUnit) (*NearestResult, error) {
	if len(candidates) == 0 {
		return nil, ErrEmptyCandidates
	}

	minDist := math.Inf(1)
	minIdx := 0

	for i, candidate := range candidates {
		dist, err := HaversineDistance(point, candidate, unit)
		if err != nil {
			return nil, err
		}
		if dist < minDist {
			minDist = dist
			minIdx = i
		}
	}

	return &NearestResult{
		Index:      minIdx,
		Distance:   minDist,
		Coordinate: candidates[minIdx],
	}, nil
}

// DistancesToAll calculates distances from a point to all targets.
func DistancesToAll(point Coordinate, targets []Coordinate, unit DistanceUnit) ([]float64, error) {
	distances := make([]float64, len(targets))
	for i, target := range targets {
		d, err := HaversineDistance(point, target, unit)
		if err != nil {
			return nil, err
		}
		distances[i] = d
	}
	return distances, nil
}

// WithinRadius finds all candidates within a radius of a point.
func WithinRadius(point Coordinate, candidates []Coordinate, radiusKM float64, unit DistanceUnit) ([]NearestResult, error) {
	var results []NearestResult

	for i, candidate := range candidates {
		dist, err := HaversineDistance(point, candidate, unit)
		if err != nil {
			return nil, err
		}
		if dist <= radiusKM {
			results = append(results, NearestResult{
				Index:      i,
				Distance:   dist,
				Coordinate: candidate,
			})
		}
	}

	return results, nil
}

// ============================================================================
// Coordinate Format Conversions
// ============================================================================

// DecimalToDMS converts decimal degrees to degrees-minutes-seconds format.
func DecimalToDMS(lat, lon float64) CoordinateDMS {
	return CoordinateDMS{
		Lat: toDMS(lat, true),
		Lon: toDMS(lon, false),
	}
}

func toDMS(value float64, isLat bool) DMS {
	absVal := math.Abs(value)
	degrees := int(absVal)
	minutesFull := (absVal - float64(degrees)) * 60
	minutes := int(minutesFull)
	seconds := (minutesFull - float64(minutes)) * 60

	var direction string
	if isLat {
		if value >= 0 {
			direction = "N"
		} else {
			direction = "S"
		}
	} else {
		if value >= 0 {
			direction = "E"
		} else {
			direction = "W"
		}
	}

	return DMS{
		Degrees:   degrees,
		Minutes:   minutes,
		Seconds:  seconds,
		Direction: direction,
	}
}

// DMSToDecimal converts DMS to decimal degrees.
func DMSToDecimal(latDMS, lonDMS DMS) Coordinate {
	return Coordinate{
		Lat: dmsToDecimal(latDMS),
		Lon: dmsToDecimal(lonDMS),
	}
}

func dmsToDecimal(dms DMS) float64 {
	decimal := float64(dms.Degrees) + float64(dms.Minutes)/60 + dms.Seconds/3600
	if dms.Direction == "S" || dms.Direction == "W" {
		decimal = -decimal
	}
	return decimal
}

// CoordinateToString converts coordinate to human-readable string.
func CoordinateToString(coord Coordinate, format string, precision int) string {
	switch format {
	case "decimal":
		latDir := "N"
		if coord.Lat < 0 {
			latDir = "S"
		}
		lonDir := "E"
		if coord.Lon < 0 {
			lonDir = "W"
		}
		return fmt.Sprintf("%.*f°%s, %.*f°%s",
			precision, math.Abs(coord.Lat), latDir,
			precision, math.Abs(coord.Lon), lonDir)

	case "dms":
		dms := DecimalToDMS(coord.Lat, coord.Lon)
		return fmt.Sprintf("%d°%d'%.1f\"%s, %d°%d'%.1f\"%s",
			dms.Lat.Degrees, dms.Lat.Minutes, dms.Lat.Seconds, dms.Lat.Direction,
			dms.Lon.Degrees, dms.Lon.Minutes, dms.Lon.Seconds, dms.Lon.Direction)

	case "dm":
		latDir := "N"
		if coord.Lat < 0 {
			latDir = "S"
		}
		lonDir := "E"
		if coord.Lon < 0 {
			lonDir = "W"
		}
		latDeg := int(math.Abs(coord.Lat))
		latMin := (math.Abs(coord.Lat) - float64(latDeg)) * 60
		lonDeg := int(math.Abs(coord.Lon))
		lonMin := (math.Abs(coord.Lon) - float64(lonDeg)) * 60
		return fmt.Sprintf("%d°%.2f'%s, %d°%.2f'%s",
			latDeg, latMin, latDir,
			lonDeg, lonMin, lonDir)

	default:
		return ""
	}
}

// ============================================================================
// Distance Unit Conversions
// ============================================================================

// ConvertKMToMiles converts kilometers to miles.
func ConvertKMToMiles(km float64) float64 {
	return km * KMToMiles
}

// ConvertKMToNautical converts kilometers to nautical miles.
func ConvertKMToNautical(km float64) float64 {
	return km * KMToNautical
}

// ConvertKMToM converts kilometers to meters.
func ConvertKMToM(km float64) float64 {
	return km * 1000
}

// ConvertMilesToKM converts miles to kilometers.
func ConvertMilesToKM(miles float64) float64 {
	return miles * MilesToKM
}

// ConvertNauticalToKM converts nautical miles to kilometers.
func ConvertNauticalToKM(nautical float64) float64 {
	return nautical * NauticalToKM
}

// ConvertMToKM converts meters to kilometers.
func ConvertMToKM(m float64) float64 {
	return m * MToKM
}

// ConvertDistance converts distance between units.
func ConvertDistance(value float64, fromUnit, toUnit DistanceUnit) (float64, error) {
	// Convert to km first
	var kmValue float64
	switch fromUnit {
	case UnitKM:
		kmValue = value
	case UnitM:
		kmValue = value * MToKM
	case UnitMiles:
		kmValue = value * MilesToKM
	case UnitNautical:
		kmValue = value * NauticalToKM
	default:
		return 0, ErrInvalidUnit
	}

	return convertFromKM(kmValue, toUnit)
}

func convertFromKM(km float64, unit DistanceUnit) (float64, error) {
	switch unit {
	case UnitKM:
		return km, nil
	case UnitM:
		return km * 1000, nil
	case UnitMiles:
		return km * KMToMiles, nil
	case UnitNautical:
		return km * KMToNautical, nil
	default:
		return 0, ErrInvalidUnit
	}
}