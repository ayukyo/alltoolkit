// Package bezier_curve_utils provides Bezier curve utilities
// for computing, evaluating, and manipulating Bezier curves.
// Pure Go implementation with zero external dependencies.
//
// Features:
// - Linear, Quadratic, and Cubic Bezier curves
// - Arbitrary degree Bezier curves via De Casteljau's algorithm
// - Point evaluation at parameter t
// - Derivative calculation (tangent vectors)
// - Length estimation via adaptive subdivision
// - Curve subdivision and splitting
// - Bounding box calculation
// - Intersection detection with lines and other curves
// - Curve flattening (polygon approximation)
// - Easing functions based on cubic Bezier curves
package bezier_curve_utils

import (
	"errors"
	"math"
)

// Point represents a 2D point on a Bezier curve
type Point struct {
	X float64
	Y float64
}

// BezierCurve represents a Bezier curve of arbitrary degree
type BezierCurve struct {
	Points []Point
}

// LinearBezier represents a linear Bezier curve (2 control points)
type LinearBezier struct {
	P0, P1 Point
}

// QuadraticBezier represents a quadratic Bezier curve (3 control points)
type QuadraticBezier struct {
	P0, P1, P2 Point
}

// CubicBezier represents a cubic Bezier curve (4 control points)
type CubicBezier struct {
	P0, P1, P2, P3 Point
}

// BoundingBox represents the bounding rectangle of a curve
type BoundingBox struct {
	Min Point
	Max Point
}

// NewBezierCurve creates a new Bezier curve from control points
func NewBezierCurve(points []Point) (*BezierCurve, error) {
	if len(points) < 2 {
		return nil, errors.New("bezier curve requires at least 2 control points")
	}
	return &BezierCurve{Points: points}, nil
}

// NewLinearBezier creates a new linear Bezier curve
func NewLinearBezier(p0, p1 Point) *LinearBezier {
	return &LinearBezier{P0: p0, P1: p1}
}

// NewQuadraticBezier creates a new quadratic Bezier curve
func NewQuadraticBezier(p0, p1, p2 Point) *QuadraticBezier {
	return &QuadraticBezier{P0: p0, P1: p1, P2: p2}
}

// NewCubicBezier creates a new cubic Bezier curve
func NewCubicBezier(p0, p1, p2, p3 Point) *CubicBezier {
	return &CubicBezier{P0: p0, P1: p1, P2: p2, P3: p3}
}

// EvaluateAt returns the point on the linear Bezier curve at parameter t (0 <= t <= 1)
func (lb *LinearBezier) EvaluateAt(t float64) Point {
	return Point{
		X: lb.P0.X + (lb.P1.X - lb.P0.X) * t,
		Y: lb.P0.Y + (lb.P1.Y - lb.P0.Y) * t,
	}
}

// EvaluateAt returns the point on the quadratic Bezier curve at parameter t
// B(t) = (1-t)²P0 + 2(1-t)tP1 + t²P2
func (qb *QuadraticBezier) EvaluateAt(t float64) Point {
	oneMinusT := 1 - t
	tSquared := t * t
	oneMinusTSquared := oneMinusT * oneMinusT
	twoTOneMinusT := 2 * t * oneMinusT

	return Point{
		X: oneMinusTSquared * qb.P0.X + twoTOneMinusT * qb.P1.X + tSquared * qb.P2.X,
		Y: oneMinusTSquared * qb.P0.Y + twoTOneMinusT * qb.P1.Y + tSquared * qb.P2.Y,
	}
}

// EvaluateAt returns the point on the cubic Bezier curve at parameter t
// B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
func (cb *CubicBezier) EvaluateAt(t float64) Point {
	oneMinusT := 1 - t
	tSquared := t * t
	tCubed := t * t * t
	oneMinusTSquared := oneMinusT * oneMinusT
	oneMinusTCubed := oneMinusT * oneMinusT * oneMinusT

	return Point{
		X: oneMinusTCubed * cb.P0.X + 3 * oneMinusTSquared * t * cb.P1.X + 3 * oneMinusT * tSquared * cb.P2.X + tCubed * cb.P3.X,
		Y: oneMinusTCubed * cb.P0.Y + 3 * oneMinusTSquared * t * cb.P1.Y + 3 * oneMinusT * tSquared * cb.P2.Y + tCubed * cb.P3.Y,
	}
}

// EvaluateAt uses De Casteljau's algorithm for arbitrary degree curves
func (bc *BezierCurve) EvaluateAt(t float64) Point {
	return deCasteljau(bc.Points, t)
}

// deCasteljau implements the De Casteljau algorithm for Bezier curve evaluation
func deCasteljau(points []Point, t float64) Point {
	if len(points) == 1 {
		return points[0]
	}

	newPoints := make([]Point, len(points)-1)
	for i := 0; i < len(points)-1; i++ {
		newPoints[i] = Point{
			X: points[i].X + (points[i+1].X - points[i].X) * t,
			Y: points[i].Y + (points[i+1].Y - points[i].Y) * t,
		}
	}
	return deCasteljau(newPoints, t)
}

// DerivativeAt returns the derivative (tangent vector) at parameter t for linear Bezier
func (lb *LinearBezier) DerivativeAt(t float64) Point {
	return Point{
		X: lb.P1.X - lb.P0.X,
		Y: lb.P1.Y - lb.P0.Y,
	}
}

// DerivativeAt returns the derivative at parameter t for quadratic Bezier
// B'(t) = 2(1-t)(P1-P0) + 2t(P2-P1)
func (qb *QuadraticBezier) DerivativeAt(t float64) Point {
	return Point{
		X: 2 * (1 - t) * (qb.P1.X - qb.P0.X) + 2 * t * (qb.P2.X - qb.P1.X),
		Y: 2 * (1 - t) * (qb.P1.Y - qb.P0.Y) + 2 * t * (qb.P2.Y - qb.P1.Y),
	}
}

// DerivativeAt returns the derivative at parameter t for cubic Bezier
// B'(t) = 3(1-t)²(P1-P0) + 6(1-t)t(P2-P1) + 3t²(P3-P2)
func (cb *CubicBezier) DerivativeAt(t float64) Point {
	oneMinusT := 1 - t
	oneMinusTSquared := oneMinusT * oneMinusT
	tSquared := t * t

	return Point{
		X: 3 * oneMinusTSquared * (cb.P1.X - cb.P0.X) + 6 * oneMinusT * t * (cb.P2.X - cb.P1.X) + 3 * tSquared * (cb.P3.X - cb.P2.X),
		Y: 3 * oneMinusTSquared * (cb.P1.Y - cb.P0.Y) + 6 * oneMinusT * t * (cb.P2.Y - cb.P1.Y) + 3 * tSquared * (cb.P3.Y - cb.P2.Y),
	}
}

// DerivativeAt returns the derivative at parameter t for arbitrary degree curve
func (bc *BezierCurve) DerivativeAt(t float64) Point {
	if len(bc.Points) == 2 {
		return Point{
			X: bc.Points[1].X - bc.Points[0].X,
			Y: bc.Points[1].Y - bc.Points[0].Y,
		}
	}

	// Derivative of Bezier curve is another Bezier curve with degree n-1
	derivativePoints := make([]Point, len(bc.Points)-1)
	n := float64(len(bc.Points) - 1)
	for i := 0; i < len(bc.Points)-1; i++ {
		derivativePoints[i] = Point{
			X: n * (bc.Points[i+1].X - bc.Points[i].X),
			Y: n * (bc.Points[i+1].Y - bc.Points[i].Y),
		}
	}
	derivCurve, _ := NewBezierCurve(derivativePoints)
	return derivCurve.EvaluateAt(t)
}

// Length estimates the arc length of the curve using adaptive subdivision
func (lb *LinearBezier) Length() float64 {
	dx := lb.P1.X - lb.P0.X
	dy := lb.P1.Y - lb.P0.Y
	return math.Sqrt(dx*dx + dy*dy)
}

// Length estimates the arc length using adaptive subdivision
func (qb *QuadraticBezier) Length() float64 {
	return adaptiveLength(qb.Flatten(0.001))
}

// Length estimates the arc length using adaptive subdivision
func (cb *CubicBezier) Length() float64 {
	return adaptiveLength(cb.Flatten(0.001))
}

// Length estimates the arc length using adaptive subdivision
func (bc *BezierCurve) Length() float64 {
	return adaptiveLength(bc.Flatten(0.001))
}

// adaptiveLength calculates the length of a polygon approximation
func adaptiveLength(points []Point) float64 {
	length := 0.0
	for i := 1; i < len(points); i++ {
		dx := points[i].X - points[i-1].X
		dy := points[i].Y - points[i-1].Y
		length += math.Sqrt(dx*dx + dy*dy)
	}
	return length
}

// Flatten converts the curve to a polygon approximation
func (lb *LinearBezier) Flatten(tolerance float64) []Point {
	return []Point{lb.P0, lb.P1}
}

// Flatten converts the quadratic curve to a polygon approximation
func (qb *QuadraticBezier) Flatten(tolerance float64) []Point {
	return flattenQuadratic(qb.P0, qb.P1, qb.P2, tolerance)
}

// Flatten converts the cubic curve to a polygon approximation
func (cb *CubicBezier) Flatten(tolerance float64) []Point {
	return flattenCubic(cb.P0, cb.P1, cb.P2, cb.P3, tolerance)
}

// Flatten converts the arbitrary degree curve to a polygon approximation
func (bc *BezierCurve) Flatten(tolerance float64) []Point {
	if len(bc.Points) == 2 {
		return bc.Points
	}
	return flattenRecursive(bc.Points, tolerance)
}

// flattenQuadratic recursively subdivides quadratic Bezier
func flattenQuadratic(p0, p1, p2 Point, tolerance float64) []Point {
	// Check if the curve is flat enough
	if isFlatQuadratic(p0, p1, p2, tolerance) {
		return []Point{p0, p2}
	}

	// Subdivide at t=0.5
	mid := quadraticAt(p0, p1, p2, 0.5)
	left0, left1, left2 := p0, midpoint(p0, p1), mid
	right0, right1, right2 := mid, midpoint(p1, p2), p2

	left := flattenQuadratic(left0, left1, left2, tolerance)
	right := flattenQuadratic(right0, right1, right2, tolerance)

	// Combine results (avoid duplicating the midpoint)
	result := append(left, right[1:]...)
	return result
}

// flattenCubic recursively subdivides cubic Bezier
func flattenCubic(p0, p1, p2, p3 Point, tolerance float64) []Point {
	// Check if the curve is flat enough
	if isFlatCubic(p0, p1, p2, p3, tolerance) {
		return []Point{p0, p3}
	}

	// Subdivide at t=0.5 using De Casteljau
	points := []Point{p0, p1, p2, p3}
	left, right := subdivideCasteljau(points, 0.5)

	leftFlat := flattenCubic(left[0], left[1], left[2], left[3], tolerance)
	rightFlat := flattenCubic(right[0], right[1], right[2], right[3], tolerance)

	result := append(leftFlat, rightFlat[1:]...)
	return result
}

// flattenRecursive recursively flattens arbitrary degree Bezier
func flattenRecursive(points []Point, tolerance float64) []Point {
	if len(points) == 2 {
		return points
	}

	if isFlatGeneral(points, tolerance) {
		return []Point{points[0], points[len(points)-1]}
	}

	left, right := subdivideCasteljau(points, 0.5)
	leftFlat := flattenRecursive(left, tolerance)
	rightFlat := flattenRecursive(right, tolerance)

	result := append(leftFlat, rightFlat[1:]...)
	return result
}

// isFlatQuadratic checks if quadratic Bezier is flat enough
func isFlatQuadratic(p0, p1, p2 Point, tolerance float64) bool {
	// Distance from p1 to the line p0-p2
	dx := p2.X - p0.X
	dy := p2.Y - p0.Y
	length := math.Sqrt(dx*dx + dy*dy)
	if length < 1e-10 {
		return true
	}

	// Calculate perpendicular distance
	area := math.Abs((p1.X - p0.X) * (p2.Y - p0.Y) - (p1.Y - p0.Y) * (p2.X - p0.X))
	distance := area / length

	return distance < tolerance
}

// isFlatCubic checks if cubic Bezier is flat enough
func isFlatCubic(p0, p1, p2, p3 Point, tolerance float64) bool {
	// Check deviation of p1 and p2 from the line p0-p3
	dx := p3.X - p0.X
	dy := p3.Y - p0.Y
	length := math.Sqrt(dx*dx + dy*dy)
	if length < 1e-10 {
		return true
	}

	// Distance from p1 to line p0-p3
	area1 := math.Abs((p1.X - p0.X) * (p3.Y - p0.Y) - (p1.Y - p0.Y) * (p3.X - p0.X))
	distance1 := area1 / length

	// Distance from p2 to line p0-p3
	area2 := math.Abs((p2.X - p0.X) * (p3.Y - p0.Y) - (p2.Y - p0.Y) * (p3.X - p0.X))
	distance2 := area2 / length

	return distance1 < tolerance && distance2 < tolerance
}

// isFlatGeneral checks if arbitrary degree Bezier is flat enough
func isFlatGeneral(points []Point, tolerance float64) bool {
	if len(points) < 3 {
		return true
	}

	first := points[0]
	last := points[len(points)-1]
	dx := last.X - first.X
	dy := last.Y - first.Y
	length := math.Sqrt(dx*dx + dy*dy)
	if length < 1e-10 {
		return true
	}

	for i := 1; i < len(points)-1; i++ {
		area := math.Abs((points[i].X - first.X) * (last.Y - first.Y) - (points[i].Y - first.Y) * (last.X - first.X))
		distance := area / length
		if distance >= tolerance {
			return false
		}
	}
	return true
}

// quadraticAt evaluates quadratic Bezier at t
func quadraticAt(p0, p1, p2 Point, t float64) Point {
	oneMinusT := 1 - t
	return Point{
		X: oneMinusT*oneMinusT*p0.X + 2*oneMinusT*t*p1.X + t*t*p2.X,
		Y: oneMinusT*oneMinusT*p0.Y + 2*oneMinusT*t*p1.Y + t*t*p2.Y,
	}
}

// midpoint returns the midpoint between two points
func midpoint(p0, p1 Point) Point {
	return Point{X: (p0.X + p1.X) / 2, Y: (p0.Y + p1.Y) / 2}
}

// subdivideCasteljau subdivides a Bezier curve at parameter t
func subdivideCasteljau(points []Point, t float64) ([]Point, []Point) {
	n := len(points)
	left := make([]Point, n)
	right := make([]Point, n)

	// Build the De Casteljau triangle
	triangle := make([][]Point, n)
	for i := 0; i < n; i++ {
		triangle[i] = make([]Point, n-i)
		triangle[0][i] = points[i]
	}

	for r := 1; r < n; r++ {
		for i := 0; i < n-r; i++ {
			triangle[r][i] = Point{
				X: triangle[r-1][i].X + (triangle[r-1][i+1].X - triangle[r-1][i].X) * t,
				Y: triangle[r-1][i].Y + (triangle[r-1][i+1].Y - triangle[r-1][i].Y) * t,
			}
		}
	}

	// Extract left and right curves
	for i := 0; i < n; i++ {
		left[i] = triangle[i][0]
		right[i] = triangle[n-1-i][i]
	}

	return left, right
}

// SplitAt divides the curve at parameter t and returns two sub-curves
func (lb *LinearBezier) SplitAt(t float64) (*LinearBezier, *LinearBezier) {
	mid := lb.EvaluateAt(t)
	return NewLinearBezier(lb.P0, mid), NewLinearBezier(mid, lb.P1)
}

// SplitAt divides the quadratic curve at parameter t
func (qb *QuadraticBezier) SplitAt(t float64) (*QuadraticBezier, *QuadraticBezier) {
	left, right := subdivideCasteljau([]Point{qb.P0, qb.P1, qb.P2}, t)
	return NewQuadraticBezier(left[0], left[1], left[2]),
		NewQuadraticBezier(right[0], right[1], right[2])
}

// SplitAt divides the cubic curve at parameter t
func (cb *CubicBezier) SplitAt(t float64) (*CubicBezier, *CubicBezier) {
	left, right := subdivideCasteljau([]Point{cb.P0, cb.P1, cb.P2, cb.P3}, t)
	return NewCubicBezier(left[0], left[1], left[2], left[3]),
		NewCubicBezier(right[0], right[1], right[2], right[3])
}

// SplitAt divides the arbitrary degree curve at parameter t
func (bc *BezierCurve) SplitAt(t float64) (*BezierCurve, *BezierCurve) {
	left, right := subdivideCasteljau(bc.Points, t)
	leftCurve, _ := NewBezierCurve(left)
	rightCurve, _ := NewBezierCurve(right)
	return leftCurve, rightCurve
}

// BoundingBox returns the bounding rectangle of the linear Bezier
func (lb *LinearBezier) BoundingBox() BoundingBox {
	return BoundingBox{
		Min: Point{X: math.Min(lb.P0.X, lb.P1.X), Y: math.Min(lb.P0.Y, lb.P1.Y)},
		Max: Point{X: math.Max(lb.P0.X, lb.P1.X), Y: math.Max(lb.P0.Y, lb.P1.Y)},
	}
}

// BoundingBox returns the bounding rectangle of the quadratic Bezier
func (qb *QuadraticBezier) BoundingBox() BoundingBox {
	// Find extremum points by solving derivative = 0
	tX := (qb.P0.X - qb.P1.X) / (qb.P0.X - 2*qb.P1.X + qb.P2.X)
	tY := (qb.P0.Y - qb.P1.Y) / (qb.P0.Y - 2*qb.P1.Y + qb.P2.Y)

	minX, maxX := qb.P0.X, qb.P0.X
	minY, maxY := qb.P0.Y, qb.P0.Y

	// Check endpoints
	minX, maxX = updateMinMax(minX, maxX, qb.P2.X)
	minY, maxY = updateMinMax(minY, maxY, qb.P2.Y)

	// Check extremum if within [0,1]
	if tX >= 0 && tX <= 1 {
		exX := qb.EvaluateAt(tX).X
		minX, maxX = updateMinMax(minX, maxX, exX)
	}
	if tY >= 0 && tY <= 1 {
		exY := qb.EvaluateAt(tY).Y
		minY, maxY = updateMinMax(minY, maxY, exY)
	}

	return BoundingBox{
		Min: Point{X: minX, Y: minY},
		Max: Point{X: maxX, Y: maxY},
	}
}

// BoundingBox returns the bounding rectangle of the cubic Bezier
func (cb *CubicBezier) BoundingBox() BoundingBox {
	// Sample points for approximate bounding box
	points := cb.Flatten(0.001)
	return boundingBoxFromPoints(points)
}

// BoundingBox returns the bounding rectangle of the arbitrary degree curve
func (bc *BezierCurve) BoundingBox() BoundingBox {
	points := bc.Flatten(0.001)
	return boundingBoxFromPoints(points)
}

// updateMinMax helper for bounding box calculation
func updateMinMax(min, max, value float64) (float64, float64) {
	if value < min {
		min = value
	}
	if value > max {
		max = value
	}
	return min, max
}

// boundingBoxFromPoints calculates bounding box from a set of points
func boundingBoxFromPoints(points []Point) BoundingBox {
	if len(points) == 0 {
		return BoundingBox{}
	}

	minX, maxX := points[0].X, points[0].X
	minY, maxY := points[0].Y, points[0].Y

	for _, p := range points {
		minX, maxX = updateMinMax(minX, maxX, p.X)
		minY, maxY = updateMinMax(minY, maxY, p.Y)
	}

	return BoundingBox{
		Min: Point{X: minX, Y: minY},
		Max: Point{X: maxX, Y: maxY},
	}
}

// IntersectLine finds intersection points with a line
func (lb *LinearBezier) IntersectLine(lineP0, lineP1 Point) []Point {
	// Line-line intersection
	intersection := lineIntersection(lb.P0, lb.P1, lineP0, lineP1)
	if intersection != nil {
		return []Point{*intersection}
	}
	return nil
}

// IntersectLine finds intersection points with a line (quadratic)
func (qb *QuadraticBezier) IntersectLine(lineP0, lineP1 Point) []Point {
	// Flatten and check each segment
	points := qb.Flatten(0.001)
	intersections := []Point{}

	for i := 1; i < len(points); i++ {
		intersection := lineIntersection(points[i-1], points[i], lineP0, lineP1)
		if intersection != nil {
			intersections = append(intersections, *intersection)
		}
	}
	return intersections
}

// IntersectLine finds intersection points with a line (cubic)
func (cb *CubicBezier) IntersectLine(lineP0, lineP1 Point) []Point {
	points := cb.Flatten(0.001)
	intersections := []Point{}

	for i := 1; i < len(points); i++ {
		intersection := lineIntersection(points[i-1], points[i], lineP0, lineP1)
		if intersection != nil {
			intersections = append(intersections, *intersection)
		}
	}
	return intersections
}

// IntersectLine finds intersection points with a line (arbitrary degree)
func (bc *BezierCurve) IntersectLine(lineP0, lineP1 Point) []Point {
	points := bc.Flatten(0.001)
	intersections := []Point{}

	for i := 1; i < len(points); i++ {
		intersection := lineIntersection(points[i-1], points[i], lineP0, lineP1)
		if intersection != nil {
			intersections = append(intersections, *intersection)
		}
	}
	return intersections
}

// lineIntersection finds the intersection of two line segments
func lineIntersection(p0, p1, p2, p3 Point) *Point {
	d1x := p1.X - p0.X
	d1y := p1.Y - p0.Y
	d2x := p3.X - p2.X
	d2y := p3.Y - p2.Y

	cross := d1x*d2y - d1y*d2x
	if math.Abs(cross) < 1e-10 {
		return nil // Parallel or coincident
	}

	dx := p2.X - p0.X
	dy := p2.Y - p0.Y

	t := (dx*d2y - dy*d2x) / cross
	u := (dx*d1y - dy*d1x) / cross

	if t >= 0 && t <= 1 && u >= 0 && u <= 1 {
		return &Point{
			X: p0.X + t*d1x,
			Y: p0.Y + t*d1y,
		}
	}
	return nil
}

// DistanceToPoint calculates the minimum distance from a point to the curve
func (lb *LinearBezier) DistanceToPoint(p Point) float64 {
	return distanceToSegment(p, lb.P0, lb.P1)
}

// DistanceToPoint calculates the minimum distance from a point to the curve
func (qb *QuadraticBezier) DistanceToPoint(p Point) float64 {
	points := qb.Flatten(0.001)
	minDist := math.Inf(1)

	for i := 1; i < len(points); i++ {
		dist := distanceToSegment(p, points[i-1], points[i])
		if dist < minDist {
			minDist = dist
		}
	}
	return minDist
}

// DistanceToPoint calculates the minimum distance from a point to the curve
func (cb *CubicBezier) DistanceToPoint(p Point) float64 {
	points := cb.Flatten(0.001)
	minDist := math.Inf(1)

	for i := 1; i < len(points); i++ {
		dist := distanceToSegment(p, points[i-1], points[i])
		if dist < minDist {
			minDist = dist
		}
	}
	return minDist
}

// DistanceToPoint calculates the minimum distance from a point to the curve
func (bc *BezierCurve) DistanceToPoint(p Point) float64 {
	points := bc.Flatten(0.001)
	minDist := math.Inf(1)

	for i := 1; i < len(points); i++ {
		dist := distanceToSegment(p, points[i-1], points[i])
		if dist < minDist {
			minDist = dist
		}
	}
	return minDist
}

// distanceToSegment calculates distance from a point to a line segment
func distanceToSegment(p, v, w Point) float64 {
	l2 := (w.X-v.X)*(w.X-v.X) + (w.Y-v.Y)*(w.Y-v.Y)
	if l2 == 0 {
		return distanceBetweenPoints(p, v)
	}

	t := math.Max(0, math.Min(1, ((p.X-v.X)*(w.X-v.X)+(p.Y-v.Y)*(w.Y-v.Y))/l2))
	projection := Point{X: v.X + t*(w.X-v.X), Y: v.Y + t*(w.Y-v.Y)}
	return distanceBetweenPoints(p, projection)
}

// distanceBetweenPoints calculates Euclidean distance between two points
func distanceBetweenPoints(p1, p2 Point) float64 {
	dx := p2.X - p1.X
	dy := p2.Y - p1.Y
	return math.Sqrt(dx*dx + dy*dy)
}

// Samples returns n evenly spaced points along the curve
func (lb *LinearBezier) Samples(n int) []Point {
	if n < 2 {
		return []Point{lb.P0}
	}
	points := make([]Point, n)
	for i := 0; i < n; i++ {
		t := float64(i) / float64(n-1)
		points[i] = lb.EvaluateAt(t)
	}
	return points
}

// Samples returns n evenly spaced points along the curve
func (qb *QuadraticBezier) Samples(n int) []Point {
	if n < 2 {
		return []Point{qb.P0}
	}
	points := make([]Point, n)
	for i := 0; i < n; i++ {
		t := float64(i) / float64(n-1)
		points[i] = qb.EvaluateAt(t)
	}
	return points
}

// Samples returns n evenly spaced points along the curve
func (cb *CubicBezier) Samples(n int) []Point {
	if n < 2 {
		return []Point{cb.P0}
	}
	points := make([]Point, n)
	for i := 0; i < n; i++ {
		t := float64(i) / float64(n-1)
		points[i] = cb.EvaluateAt(t)
	}
	return points
}

// Samples returns n evenly spaced points along the curve
func (bc *BezierCurve) Samples(n int) []Point {
	if n < 2 {
		return []Point{bc.Points[0]}
	}
	points := make([]Point, n)
	for i := 0; i < n; i++ {
		t := float64(i) / float64(n-1)
		points[i] = bc.EvaluateAt(t)
	}
	return points
}

// EasingFunction represents a cubic Bezier easing function
type EasingFunction struct {
	Curve *CubicBezier
}

// NewEasingFunction creates a new easing function from a cubic Bezier
func NewEasingFunction(p1x, p1y, p2x, p2y float64) *EasingFunction {
	// For easing, x is time (0 to 1) and y is progress (0 to 1)
	// Standard format: (0, 0), (p1x, p1y), (p2x, p2y), (1, 1)
	return &EasingFunction{
		Curve: NewCubicBezier(
			Point{X: 0, Y: 0},
			Point{X: p1x, Y: p1y},
			Point{X: p2x, Y: p2y},
			Point{X: 1, Y: 1},
		),
	}
}

// Ease returns the eased value for a given time t (0 to 1)
func (ef *EasingFunction) Ease(t float64) float64 {
	// Clamp t to [0, 1]
	if t <= 0 {
		return 0
	}
	if t >= 1 {
		return 1
	}

	// Find the t parameter that gives x = input t
	// This requires solving for t (Newton-Raphson method)
	tEstimate := t
	for i := 0; i < 8; i++ {
		xEstimate := ef.Curve.EvaluateAt(tEstimate).X
		xDerivative := ef.Curve.DerivativeAt(tEstimate).X

		if math.Abs(xEstimate - t) < 1e-6 {
			break
		}

		tEstimate -= (xEstimate - t) / xDerivative
	}

	// Return the y value at that t
	return ef.Curve.EvaluateAt(tEstimate).Y
}

// Predefined easing functions
var (
	// Linear easing (no acceleration)
	EaseLinear = &EasingFunction{Curve: NewCubicBezier(
		Point{X: 0, Y: 0},
		Point{X: 0.333, Y: 0.333},
		Point{X: 0.667, Y: 0.667},
		Point{X: 1, Y: 1},
	)}

	// Ease in (acceleration)
	EaseIn = NewEasingFunction(0.42, 0, 1, 1)

	// Ease out (deceleration)
	EaseOut = NewEasingFunction(0, 0, 0.58, 1)

	// Ease in-out (acceleration then deceleration)
	EaseInOut = NewEasingFunction(0.42, 0, 0.58, 1)

	// Ease in cubic (strong acceleration)
	EaseInCubic = NewEasingFunction(0.55, 0.055, 0.675, 0.19)

	// Ease out cubic (strong deceleration)
	EaseOutCubic = NewEasingFunction(0.215, 0.61, 0.355, 1)

	// Ease in-out cubic
	EaseInOutCubic = NewEasingFunction(0.645, 0.045, 0.355, 1)

	// Ease in quad (moderate acceleration)
	EaseInQuad = NewEasingFunction(0.55, 0.085, 0.68, 0.53)

	// Ease out quad (moderate deceleration)
	EaseOutQuad = NewEasingFunction(0.25, 0.46, 0.45, 0.94)

	// Ease in-out quad
	EaseInOutQuad = NewEasingFunction(0.455, 0.03, 0.515, 0.955)

	// Ease in sine (gentle acceleration)
	EaseInSine = NewEasingFunction(0.47, 0, 0.745, 0.715)

	// Ease out sine (gentle deceleration)
	EaseOutSine = NewEasingFunction(0.39, 0.575, 0.565, 1)

	// Ease in-out sine
	EaseInOutSine = NewEasingFunction(0.445, 0.05, 0.55, 0.95)

	// Ease in elastic
	EaseInElastic = NewEasingFunction(0.475, 0, 0.875, 0.565)

	// Ease out elastic
	EaseOutElastic = NewEasingFunction(0.175, 0.885, 0.32, 1.275)

	// Ease in bounce
	EaseInBounce = NewEasingFunction(0.6, -0.28, 0.735, 0.04)

	// Ease out bounce
	EaseOutBounce = NewEasingFunction(0.175, 0.885, 0.32, 1.275)
)

// Reverse returns a reversed curve (swapped start and end points)
func (lb *LinearBezier) Reverse() *LinearBezier {
	return NewLinearBezier(lb.P1, lb.P0)
}

// Reverse returns a reversed quadratic Bezier
func (qb *QuadraticBezier) Reverse() *QuadraticBezier {
	return NewQuadraticBezier(qb.P2, qb.P1, qb.P0)
}

// Reverse returns a reversed cubic Bezier
func (cb *CubicBezier) Reverse() *CubicBezier {
	return NewCubicBezier(cb.P3, cb.P2, cb.P1, cb.P0)
}

// Reverse returns a reversed arbitrary degree Bezier
func (bc *BezierCurve) Reverse() *BezierCurve {
	reversed := make([]Point, len(bc.Points))
	for i, p := range bc.Points {
		reversed[len(bc.Points)-1-i] = p
	}
	curve, _ := NewBezierCurve(reversed)
	return curve
}

// Transform applies an affine transformation to the curve
func (lb *LinearBezier) Transform(tx, ty, sx, sy float64) *LinearBezier {
	return NewLinearBezier(
		transformPoint(lb.P0, tx, ty, sx, sy),
		transformPoint(lb.P1, tx, ty, sx, sy),
	)
}

// Transform applies an affine transformation to the quadratic Bezier
func (qb *QuadraticBezier) Transform(tx, ty, sx, sy float64) *QuadraticBezier {
	return NewQuadraticBezier(
		transformPoint(qb.P0, tx, ty, sx, sy),
		transformPoint(qb.P1, tx, ty, sx, sy),
		transformPoint(qb.P2, tx, ty, sx, sy),
	)
}

// Transform applies an affine transformation to the cubic Bezier
func (cb *CubicBezier) Transform(tx, ty, sx, sy float64) *CubicBezier {
	return NewCubicBezier(
		transformPoint(cb.P0, tx, ty, sx, sy),
		transformPoint(cb.P1, tx, ty, sx, sy),
		transformPoint(cb.P2, tx, ty, sx, sy),
		transformPoint(cb.P3, tx, ty, sx, sy),
	)
}

// Transform applies an affine transformation to the arbitrary degree curve
func (bc *BezierCurve) Transform(tx, ty, sx, sy float64) *BezierCurve {
	transformed := make([]Point, len(bc.Points))
	for i, p := range bc.Points {
		transformed[i] = transformPoint(p, tx, ty, sx, sy)
	}
	curve, _ := NewBezierCurve(transformed)
	return curve
}

// transformPoint applies an affine transformation to a point
func transformPoint(p Point, tx, ty, sx, sy float64) Point {
	return Point{
		X: p.X * sx + tx,
		Y: p.Y * sy + ty,
	}
}

// Scale uniformly scales the curve by a factor
func (lb *LinearBezier) Scale(factor float64) *LinearBezier {
	return lb.Transform(0, 0, factor, factor)
}

// Scale uniformly scales the quadratic Bezier
func (qb *QuadraticBezier) Scale(factor float64) *QuadraticBezier {
	return qb.Transform(0, 0, factor, factor)
}

// Scale uniformly scales the cubic Bezier
func (cb *CubicBezier) Scale(factor float64) *CubicBezier {
	return cb.Transform(0, 0, factor, factor)
}

// Scale uniformly scales the arbitrary degree curve
func (bc *BezierCurve) Scale(factor float64) *BezierCurve {
	return bc.Transform(0, 0, factor, factor)
}

// Translate moves the curve by dx and dy
func (lb *LinearBezier) Translate(dx, dy float64) *LinearBezier {
	return lb.Transform(dx, dy, 1, 1)
}

// Translate moves the quadratic Bezier by dx and dy
func (qb *QuadraticBezier) Translate(dx, dy float64) *QuadraticBezier {
	return qb.Transform(dx, dy, 1, 1)
}

// Translate moves the cubic Bezier by dx and dy
func (cb *CubicBezier) Translate(dx, dy float64) *CubicBezier {
	return cb.Transform(dx, dy, 1, 1)
}

// Translate moves the arbitrary degree curve by dx and dy
func (bc *BezierCurve) Translate(dx, dy float64) *BezierCurve {
	return bc.Transform(dx, dy, 1, 1)
}

// Rotate rotates the curve around the origin by angle (in radians)
func (lb *LinearBezier) Rotate(angle float64) *LinearBezier {
	cos := math.Cos(angle)
	sin := math.Sin(angle)
	return NewLinearBezier(
		rotatePoint(lb.P0, cos, sin),
		rotatePoint(lb.P1, cos, sin),
	)
}

// Rotate rotates the quadratic Bezier around the origin
func (qb *QuadraticBezier) Rotate(angle float64) *QuadraticBezier {
	cos := math.Cos(angle)
	sin := math.Sin(angle)
	return NewQuadraticBezier(
		rotatePoint(qb.P0, cos, sin),
		rotatePoint(qb.P1, cos, sin),
		rotatePoint(qb.P2, cos, sin),
	)
}

// Rotate rotates the cubic Bezier around the origin
func (cb *CubicBezier) Rotate(angle float64) *CubicBezier {
	cos := math.Cos(angle)
	sin := math.Sin(angle)
	return NewCubicBezier(
		rotatePoint(cb.P0, cos, sin),
		rotatePoint(cb.P1, cos, sin),
		rotatePoint(cb.P2, cos, sin),
		rotatePoint(cb.P3, cos, sin),
	)
}

// Rotate rotates the arbitrary degree curve around the origin
func (bc *BezierCurve) Rotate(angle float64) *BezierCurve {
	cos := math.Cos(angle)
	sin := math.Sin(angle)
	rotated := make([]Point, len(bc.Points))
	for i, p := range bc.Points {
		rotated[i] = rotatePoint(p, cos, sin)
	}
	curve, _ := NewBezierCurve(rotated)
	return curve
}

// rotatePoint rotates a point around the origin
func rotatePoint(p Point, cos, sin float64) Point {
	return Point{
		X: p.X * cos - p.Y * sin,
		Y: p.X * sin + p.Y * cos,
	}
}

// Degree returns the degree of the Bezier curve
func (bc *BezierCurve) Degree() int {
	return len(bc.Points) - 1
}

// IsLinear checks if a higher-degree curve is effectively linear
func (bc *BezierCurve) IsLinear(tolerance float64) bool {
	if len(bc.Points) <= 2 {
		return true
	}
	return isFlatGeneral(bc.Points, tolerance)
}

// ElevateDegree returns a curve with one higher degree (same shape)
func (lb *LinearBezier) ElevateDegree() *QuadraticBezier {
	// Linear to quadratic: P0, (P0+P1)/2, P1
	mid := midpoint(lb.P0, lb.P1)
	return NewQuadraticBezier(lb.P0, mid, lb.P1)
}

// ElevateDegree returns a cubic curve with the same shape as this quadratic
func (qb *QuadraticBezier) ElevateDegree() *CubicBezier {
	// Quadratic to cubic elevation
	return NewCubicBezier(
		qb.P0,
		Point{X: qb.P0.X + 2*(qb.P1.X-qb.P0.X)/3, Y: qb.P0.Y + 2*(qb.P1.Y-qb.P0.Y)/3},
		Point{X: qb.P1.X + (qb.P2.X-qb.P1.X)/3, Y: qb.P1.Y + (qb.P2.Y-qb.P1.Y)/3},
		qb.P2,
	)
}

// ApproximateArc creates a quadratic Bezier that approximates an arc
// center is the center point, radius is the radius, startAngle and endAngle are in radians
func ApproximateArc(center Point, radius, startAngle, endAngle float64) *QuadraticBezier {
	// Calculate start and end points
	p0 := Point{
		X: center.X + radius*math.Cos(startAngle),
		Y: center.Y + radius*math.Sin(startAngle),
	}
	p2 := Point{
		X: center.X + radius*math.Cos(endAngle),
		Y: center.Y + radius*math.Sin(endAngle),
	}

	// Calculate control point for arc approximation
	midAngle := (startAngle + endAngle) / 2
	p1 := Point{
		X: center.X + radius*math.Cos(midAngle),
		Y: center.Y + radius*math.Sin(midAngle),
	}

	return NewQuadraticBezier(p0, p1, p2)
}

// ApproximateCircle creates 4 cubic Bezier curves that approximate a circle
func ApproximateCircle(center Point, radius float64) []*CubicBezier {
	// Magic number for cubic Bezier circle approximation
	k := 0.5522847498 // 4 * (sqrt(2) - 1) / 3

	curves := make([]*CubicBezier, 4)
	for i := 0; i < 4; i++ {
		angle := float64(i) * math.Pi / 2
		nextAngle := float64(i+1) * math.Pi / 2

		p0 := Point{
			X: center.X + radius*math.Cos(angle),
			Y: center.Y + radius*math.Sin(angle),
		}
		p3 := Point{
			X: center.X + radius*math.Cos(nextAngle),
			Y: center.Y + radius*math.Sin(nextAngle),
		}

		// Control points offset
		dx := k * radius
		dy := k * radius

		// Adjust based on quadrant
		var p1, p2 Point
		switch i {
		case 0: // 0 to 90 degrees
			p1 = Point{X: p0.X + dx, Y: p0.Y}
			p2 = Point{X: p3.X, Y: p3.Y - dy}
		case 1: // 90 to 180 degrees
			p1 = Point{X: p0.X, Y: p0.Y + dy}
			p2 = Point{X: p3.X + dx, Y: p3.Y}
		case 2: // 180 to 270 degrees
			p1 = Point{X: p0.X - dx, Y: p0.Y}
			p2 = Point{X: p3.X, Y: p3.Y + dy}
		case 3: // 270 to 360 degrees
			p1 = Point{X: p0.X, Y: p0.Y - dy}
			p2 = Point{X: p3.X - dx, Y: p3.Y}
		}

		curves[i] = NewCubicBezier(p0, p1, p2, p3)
	}
	return curves
}

// ApproximateEllipse creates 4 cubic Bezier curves that approximate an ellipse
func ApproximateEllipse(center Point, rx, ry float64) []*CubicBezier {
	// Magic numbers for ellipse approximation
	kx := 0.5522847498 // for x-axis
	ky := 0.5522847498 // for y-axis

	curves := make([]*CubicBezier, 4)
	for i := 0; i < 4; i++ {
		angle := float64(i) * math.Pi / 2
		nextAngle := float64(i+1) * math.Pi / 2

		p0 := Point{
			X: center.X + rx*math.Cos(angle),
			Y: center.Y + ry*math.Sin(angle),
		}
		p3 := Point{
			X: center.X + rx*math.Cos(nextAngle),
			Y: center.Y + ry*math.Sin(nextAngle),
		}

		var p1, p2 Point
		switch i {
		case 0:
			p1 = Point{X: p0.X + kx*rx, Y: p0.Y}
			p2 = Point{X: p3.X, Y: p3.Y - ky*ry}
		case 1:
			p1 = Point{X: p0.X, Y: p0.Y + ky*ry}
			p2 = Point{X: p3.X + kx*rx, Y: p3.Y}
		case 2:
			p1 = Point{X: p0.X - kx*rx, Y: p0.Y}
			p2 = Point{X: p3.X, Y: p3.Y + ky*ry}
		case 3:
			p1 = Point{X: p0.X, Y: p0.Y - ky*ry}
			p2 = Point{X: p3.X - kx*rx, Y: p3.Y}
		}

		curves[i] = NewCubicBezier(p0, p1, p2, p3)
	}
	return curves
}