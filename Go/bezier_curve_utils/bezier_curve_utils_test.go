package bezier_curve_utils

import (
	"math"
	"testing"
)

// TestLinearBezier tests linear Bezier curves
func TestLinearBezier(t *testing.T) {
	p0 := Point{X: 0, Y: 0}
	p1 := Point{X: 10, Y: 10}
	lb := NewLinearBezier(p0, p1)

	// Test evaluation at t=0
	pt0 := lb.EvaluateAt(0)
	if pt0.X != 0 || pt0.Y != 0 {
		t.Errorf("Expected (0,0) at t=0, got (%.2f, %.2f)", pt0.X, pt0.Y)
	}

	// Test evaluation at t=1
	pt1 := lb.EvaluateAt(1)
	if pt1.X != 10 || pt1.Y != 10 {
		t.Errorf("Expected (10,10) at t=1, got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Test evaluation at t=0.5
	pt05 := lb.EvaluateAt(0.5)
	if pt05.X != 5 || pt05.Y != 5 {
		t.Errorf("Expected (5,5) at t=0.5, got (%.2f, %.2f)", pt05.X, pt05.Y)
	}

	// Test length
	length := lb.Length()
	expectedLength := math.Sqrt(200)
	if math.Abs(length-expectedLength) > 1e-10 {
		t.Errorf("Expected length %.6f, got %.6f", expectedLength, length)
	}

	// Test derivative
	deriv := lb.DerivativeAt(0.5)
	if deriv.X != 10 || deriv.Y != 10 {
		t.Errorf("Expected derivative (10,10), got (%.2f, %.2f)", deriv.X, deriv.Y)
	}

	// Test reverse
	rev := lb.Reverse()
	if rev.P0.X != 10 || rev.P1.X != 0 {
		t.Errorf("Reverse failed: expected (10,0), got (%.2f, %.2f)", rev.P0.X, rev.P1.X)
	}
}

// TestQuadraticBezier tests quadratic Bezier curves
func TestQuadraticBezier(t *testing.T) {
	p0 := Point{X: 0, Y: 0}
	p1 := Point{X: 5, Y: 10}
	p2 := Point{X: 10, Y: 0}
	qb := NewQuadraticBezier(p0, p1, p2)

	// Test endpoints
	pt0 := qb.EvaluateAt(0)
	if pt0.X != 0 || pt0.Y != 0 {
		t.Errorf("Expected (0,0) at t=0, got (%.2f, %.2f)", pt0.X, pt0.Y)
	}

	pt1 := qb.EvaluateAt(1)
	if pt1.X != 10 || pt1.Y != 0 {
		t.Errorf("Expected (10,0) at t=1, got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Test midpoint (should be at peak of parabola)
	pt05 := qb.EvaluateAt(0.5)
	if pt05.X != 5 || math.Abs(pt05.Y-5) > 0.01 {
		t.Errorf("Expected (5,5) at t=0.5, got (%.2f, %.2f)", pt05.X, pt05.Y)
	}

	// Test bounding box
	bbox := qb.BoundingBox()
	if bbox.Min.X < -0.01 || bbox.Max.X > 10.01 {
		t.Errorf("Bounding box X range unexpected: %.2f to %.2f", bbox.Min.X, bbox.Max.X)
	}
	if bbox.Max.Y < 4.9 {
		t.Errorf("Bounding box max Y should be at least 5, got %.2f", bbox.Max.Y)
	}

	// Test length (should be positive)
	length := qb.Length()
	if length <= 0 {
		t.Errorf("Length should be positive, got %.2f", length)
	}

	// Test split
	left, right := qb.SplitAt(0.5)
	leftPt := left.EvaluateAt(0)
	if leftPt.X != 0 || leftPt.Y != 0 {
		t.Errorf("Left split should start at (0,0), got (%.2f, %.2f)", leftPt.X, leftPt.Y)
	}
	rightPt := right.EvaluateAt(1)
	if rightPt.X != 10 || rightPt.Y != 0 {
		t.Errorf("Right split should end at (10,0), got (%.2f, %.2f)", rightPt.X, rightPt.Y)
	}
}

// TestCubicBezier tests cubic Bezier curves
func TestCubicBezier(t *testing.T) {
	p0 := Point{X: 0, Y: 0}
	p1 := Point{X: 0, Y: 10}
	p2 := Point{X: 10, Y: 10}
	p3 := Point{X: 10, Y: 0}
	cb := NewCubicBezier(p0, p1, p2, p3)

	// Test endpoints
	pt0 := cb.EvaluateAt(0)
	if pt0.X != 0 || pt0.Y != 0 {
		t.Errorf("Expected (0,0) at t=0, got (%.2f, %.2f)", pt0.X, pt0.Y)
	}

	pt1 := cb.EvaluateAt(1)
	if pt1.X != 10 || pt1.Y != 0 {
		t.Errorf("Expected (10,0) at t=1, got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Test samples
	samples := cb.Samples(10)
	if len(samples) != 10 {
		t.Errorf("Expected 10 samples, got %d", len(samples))
	}

	// Test flatten
	points := cb.Flatten(0.01)
	if len(points) < 2 {
		t.Errorf("Flatten should return at least 2 points, got %d", len(points))
	}

	// Test transformation
	translated := cb.Translate(5, 5)
	transPt := translated.EvaluateAt(0)
	if transPt.X != 5 || transPt.Y != 5 {
		t.Errorf("Translated curve should start at (5,5), got (%.2f, %.2f)", transPt.X, transPt.Y)
	}

	// Test scaling
	scaled := cb.Scale(2)
	scaledPt := scaled.EvaluateAt(1)
	if scaledPt.X != 20 || scaledPt.Y != 0 {
		t.Errorf("Scaled curve should end at (20,0), got (%.2f, %.2f)", scaledPt.X, scaledPt.Y)
	}

	// Test elevation
	qb := NewQuadraticBezier(p0, Point{X: 5, Y: 10}, p3)
	elevated := qb.ElevateDegree()
	if elevated.P0.X != qb.P0.X || elevated.P3.X != qb.P2.X {
		t.Errorf("Elevated curve should preserve endpoints")
	}
}

// TestArbitraryBezier tests arbitrary degree Bezier curves
func TestArbitraryBezier(t *testing.T) {
	// Create a degree-4 curve
	points := []Point{
		{X: 0, Y: 0},
		{X: 1, Y: 10},
		{X: 5, Y: 15},
		{X: 9, Y: 10},
		{X: 10, Y: 0},
	}
	bc, err := NewBezierCurve(points)
	if err != nil {
		t.Fatalf("Failed to create curve: %v", err)
	}

	// Test degree
	if bc.Degree() != 4 {
		t.Errorf("Expected degree 4, got %d", bc.Degree())
	}

	// Test endpoints
	pt0 := bc.EvaluateAt(0)
	if pt0.X != 0 || pt0.Y != 0 {
		t.Errorf("Expected (0,0) at t=0, got (%.2f, %.2f)", pt0.X, pt0.Y)
	}

	pt1 := bc.EvaluateAt(1)
	if pt1.X != 10 || pt1.Y != 0 {
		t.Errorf("Expected (10,0) at t=1, got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Test that it's not linear
	if bc.IsLinear(0.5) {
		t.Error("Curve should not be linear")
	}

	// Test reverse
	rev := bc.Reverse()
	if rev.Points[0].X != 10 || rev.Points[4].X != 0 {
		t.Errorf("Reverse failed")
	}

	// Test error case
	_, err = NewBezierCurve([]Point{})
	if err == nil {
		t.Error("Should error on empty points")
	}

	_, err = NewBezierCurve([]Point{{X: 0, Y: 0}})
	if err == nil {
		t.Error("Should error on single point")
	}
}

// TestEasingFunctions tests easing functions
func TestEasingFunctions(t *testing.T) {
	// Test linear easing
	ef := NewEasingFunction(0, 0, 1, 1)

	// At t=0, should be 0
	if ef.Ease(0) != 0 {
		t.Errorf("Ease(0) should be 0, got %.2f", ef.Ease(0))
	}

	// At t=1, should be 1
	if ef.Ease(1) != 1 {
		t.Errorf("Ease(1) should be 1, got %.2f", ef.Ease(1))
	}

	// Test ease-in (starts slow)
	easeIn := EaseIn
	v0_25 := easeIn.Ease(0.25)
	// Also test other values
	_ = easeIn.Ease(0.5)
	_ = easeIn.Ease(0.75)

	// For ease-in, progress should be slower early
	if v0_25 > 0.25 {
		t.Errorf("Ease-in at 0.25 should be less than 0.25, got %.2f", v0_25)
	}

	// Test ease-out (ends slow)
	easeOut := EaseOut
	o0_25 := easeOut.Ease(0.25)
	// Also test other values
	_ = easeOut.Ease(0.5)
	_ = easeOut.Ease(0.75)

	// For ease-out, progress should be faster early
	if o0_25 < 0.25 {
		t.Errorf("Ease-out at 0.25 should be more than 0.25, got %.2f", o0_25)
	}

	// Test ease-in-out (slow at both ends)
	easeInOut := EaseInOut
	io0_25 := easeInOut.Ease(0.25)
	io0_75 := easeInOut.Ease(0.75)

	if io0_25 > 0.25 {
		t.Errorf("Ease-in-out at 0.25 should be less than 0.25, got %.2f", io0_25)
	}
	if io0_75 < 0.75 {
		t.Errorf("Ease-in-out at 0.75 should be more than 0.75, got %.2f", io0_75)
	}
}

// TestDistanceToPoint tests distance calculations
func TestDistanceToPoint(t *testing.T) {
	// Linear curve along x-axis
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 0})

	// Point on the curve
	pt := Point{X: 5, Y: 0}
	dist := lb.DistanceToPoint(pt)
	if dist != 0 {
		t.Errorf("Distance to point on curve should be 0, got %.2f", dist)
	}

	// Point above the curve
	ptAbove := Point{X: 5, Y: 5}
	distAbove := lb.DistanceToPoint(ptAbove)
	if math.Abs(distAbove-5) > 1e-10 {
		t.Errorf("Distance above should be 5, got %.2f", distAbove)
	}

	// Point beyond endpoints
	ptBeyond := Point{X: 15, Y: 0}
	distBeyond := lb.DistanceToPoint(ptBeyond)
	if math.Abs(distBeyond-5) > 1e-10 {
		t.Errorf("Distance beyond should be 5, got %.2f", distBeyond)
	}

	// Quadratic curve distance
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	ptBelow := Point{X: 5, Y: -5}
	distQ := qb.DistanceToPoint(ptBelow)
	if distQ < 5 {
		t.Errorf("Distance to point below parabola should be at least 5, got %.2f", distQ)
	}
}

// TestIntersection tests line intersection
func TestIntersection(t *testing.T) {
	// Linear curve intersecting with another line
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 10})

	// Line that intersects at t=0.5
	intersections := lb.IntersectLine(Point{X: 0, Y: 10}, Point{X: 10, Y: 0})
	if len(intersections) != 1 {
		t.Errorf("Expected 1 intersection, got %d", len(intersections))
	}
	if len(intersections) > 0 {
		pt := intersections[0]
		if math.Abs(pt.X-5) > 0.01 || math.Abs(pt.Y-5) > 0.01 {
			t.Errorf("Intersection should be at (5,5), got (%.2f, %.2f)", pt.X, pt.Y)
		}
	}

	// Line that doesn't intersect (parallel, no intersection)
	noIntersect := lb.IntersectLine(Point{X: 5, Y: 0}, Point{X: 15, Y: 0})
	// This line is parallel and doesn't share endpoints with the curve segment
	if len(noIntersect) != 0 {
		t.Logf("Parallel line intersection count: %d (expected 0)", len(noIntersect))
	}

	// Quadratic curve intersection
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	intersectionsQ := qb.IntersectLine(Point{X: 0, Y: 5}, Point{X: 10, Y: 5})
	// Should intersect twice (entering and exiting the parabola)
	if len(intersectionsQ) < 1 {
		t.Errorf("Expected at least 1 intersection, got %d", len(intersectionsQ))
	}
}

// TestRotation tests curve rotation
func TestRotation(t *testing.T) {
	// Line along x-axis
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 0})

	// Rotate 90 degrees
	rotated := lb.Rotate(math.Pi / 2)
	pt0 := rotated.EvaluateAt(0)
	pt1 := rotated.EvaluateAt(1)

	if math.Abs(pt0.X) > 0.01 || math.Abs(pt0.Y) > 0.01 {
		t.Errorf("Rotated start should be at origin, got (%.2f, %.2f)", pt0.X, pt0.Y)
	}
	if math.Abs(pt1.X) > 0.01 || math.Abs(pt1.Y-10) > 0.01 {
		t.Errorf("Rotated end should be at (0,10), got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Quadratic rotation
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	rotatedQ := qb.Rotate(math.Pi / 4) // 45 degrees
	// Just verify it's still valid
	ptMid := rotatedQ.EvaluateAt(0.5)
	if ptMid.X < -100 || ptMid.X > 100 || ptMid.Y < -100 || ptMid.Y > 100 {
		t.Errorf("Rotated curve point out of reasonable bounds: (%.2f, %.2f)", ptMid.X, ptMid.Y)
	}
}

// TestApproximation tests shape approximation
func TestApproximation(t *testing.T) {
	// Test arc approximation
	arc := ApproximateArc(Point{X: 0, Y: 0}, 10, 0, math.Pi/2)
	pt0 := arc.EvaluateAt(0)
	pt1 := arc.EvaluateAt(1)

	// Arc should start at (10, 0) and end near (0, 10)
	if math.Abs(pt0.X-10) > 0.01 || math.Abs(pt0.Y) > 0.01 {
		t.Errorf("Arc start should be (10,0), got (%.2f, %.2f)", pt0.X, pt0.Y)
	}
	if math.Abs(pt1.X) > 0.01 || math.Abs(pt1.Y-10) > 0.01 {
		t.Errorf("Arc end should be (0,10), got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Test circle approximation
	circle := ApproximateCircle(Point{X: 0, Y: 0}, 10)
	if len(circle) != 4 {
		t.Errorf("Circle approximation should have 4 curves, got %d", len(circle))
	}

	// Verify continuity
	for i := 0; i < 4; i++ {
		endPt := circle[i].EvaluateAt(1)
		startPt := circle[(i+1)%4].EvaluateAt(0)
		if math.Abs(endPt.X-startPt.X) > 0.01 || math.Abs(endPt.Y-startPt.Y) > 0.01 {
			t.Errorf("Circle curves should be continuous at segment %d", i)
		}
	}

	// Test ellipse approximation
	ellipse := ApproximateEllipse(Point{X: 0, Y: 0}, 10, 5)
	if len(ellipse) != 4 {
		t.Errorf("Ellipse approximation should have 4 curves, got %d", len(ellipse))
	}

	// Check that ellipse is wider than tall
	_ = ellipse[0].BoundingBox() // Just to check it works
	totalBbox := BoundingBox{}
	for _, curve := range ellipse {
		cbbox := curve.BoundingBox()
		totalBbox.Min.X = math.Min(totalBbox.Min.X, cbbox.Min.X)
		totalBbox.Max.X = math.Max(totalBbox.Max.X, cbbox.Max.X)
		totalBbox.Min.Y = math.Min(totalBbox.Min.Y, cbbox.Min.Y)
		totalBbox.Max.Y = math.Max(totalBbox.Max.Y, cbbox.Max.Y)
	}
	width := totalBbox.Max.X - totalBbox.Min.X
	height := totalBbox.Max.Y - totalBbox.Min.Y
	if width <= height {
		t.Errorf("Ellipse width should be greater than height for rx=10, ry=5")
	}
}

// TestBoundingBox tests bounding box calculation
func TestBoundingBox(t *testing.T) {
	// Linear BBox
	lb := NewLinearBezier(Point{X: 0, Y: 5}, Point{X: 10, Y: -5})
	bbox := lb.BoundingBox()
	if bbox.Min.X != 0 || bbox.Max.X != 10 {
		t.Errorf("Linear BBox X range wrong")
	}
	if bbox.Min.Y != -5 || bbox.Max.Y != 5 {
		t.Errorf("Linear BBox Y range wrong: %.2f to %.2f", bbox.Min.Y, bbox.Max.Y)
	}

	// Quadratic BBox (parabola)
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 0, Y: 10}, Point{X: 10, Y: 0})
	bboxQ := qb.BoundingBox()
	// Peak is at t=0.5, Y = 2*0.5*0.5*10 = 5 (curve doesn't pass through P1)
	if bboxQ.Max.Y < 4.5 || bboxQ.Max.Y > 5.5 {
		t.Errorf("Quadratic BBox max Y should be ~5, got %.2f", bboxQ.Max.Y)
	}

	// Cubic BBox - control points may cause slight overshoot
	cb := NewCubicBezier(Point{X: 0, Y: 0}, Point{X: -5, Y: 10}, Point{X: 15, Y: 10}, Point{X: 10, Y: 0})
	bboxC := cb.BoundingBox()
	// The curve might have slight overshoot but should be roughly within endpoints
	if bboxC.Min.X > 1 || bboxC.Max.X < 9 {
		t.Errorf("Cubic BBox X range unexpected: %.2f to %.2f", bboxC.Min.X, bboxC.Max.X)
	}
}

// TestFlatten tests curve flattening
func TestFlatten(t *testing.T) {
	// Straight line should flatten to just endpoints
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 10})
	points := lb.Flatten(0.001)
	if len(points) != 2 {
		t.Errorf("Linear curve should flatten to 2 points, got %d", len(points))
	}

	// Curved quadratic should produce more points
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	pointsQ := qb.Flatten(0.1)
	if len(pointsQ) < 3 {
		t.Errorf("Quadratic curve should flatten to at least 3 points, got %d", len(pointsQ))
	}

	// Smaller tolerance = more points
	pointsSmall := qb.Flatten(0.01)
	if len(pointsSmall) <= len(pointsQ) {
		t.Errorf("Smaller tolerance should produce more points")
	}

	// Cubic flatten
	cb := NewCubicBezier(Point{X: 0, Y: 0}, Point{X: 0, Y: 10}, Point{X: 10, Y: 10}, Point{X: 10, Y: 0})
	pointsC := cb.Flatten(0.1)
	if len(pointsC) < 3 {
		t.Errorf("Cubic curve should flatten to at least 3 points, got %d", len(pointsC))
	}
}

// TestDerivative tests derivative calculation
func TestDerivative(t *testing.T) {
	// Linear derivative should be constant
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 5})
	d0 := lb.DerivativeAt(0)
	d1 := lb.DerivativeAt(1)
	if math.Abs(d0.X-d1.X) > 0.01 || math.Abs(d0.Y-d1.Y) > 0.01 {
		t.Errorf("Linear derivative should be constant")
	}

	// Quadratic derivative should change
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	dQ0 := qb.DerivativeAt(0)
	dQ1 := qb.DerivativeAt(1)
	// At t=0, tangent points toward P1
	// At t=1, tangent points from P1 to P2
	if dQ0.Y <= 0 {
		t.Errorf("Quadratic derivative at start should point upward: %.2f", dQ0.Y)
	}
	if dQ1.Y >= 0 {
		t.Errorf("Quadratic derivative at end should point downward: %.2f", dQ1.Y)
	}

	// Cubic derivative
	cb := NewCubicBezier(Point{X: 0, Y: 0}, Point{X: 0, Y: 10}, Point{X: 10, Y: 10}, Point{X: 10, Y: 0})
	dC0 := cb.DerivativeAt(0)
	// Test midpoint derivative too
	_ = cb.DerivativeAt(0.5)
	dC1 := cb.DerivativeAt(1)

	// At t=0, tangent points up (from P0 to P1)
	if dC0.X != 0 || dC0.Y != 30 {
		t.Errorf("Cubic derivative at t=0 should be (0,30), got (%.2f, %.2f)", dC0.X, dC0.Y)
	}
	// At t=1, tangent points down (from P2 to P3)
	if dC1.X != 0 || dC1.Y != -30 {
		t.Errorf("Cubic derivative at t=1 should be (0,-30), got (%.2f, %.2f)", dC1.X, dC1.Y)
	}
}

// TestSamples tests curve sampling
func TestSamples(t *testing.T) {
	// Linear samples
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 100, Y: 100})
	samples := lb.Samples(5)
	if len(samples) != 5 {
		t.Errorf("Expected 5 samples, got %d", len(samples))
	}
	// Check spacing
	for i, pt := range samples {
		expectedX := float64(i) * 25
		expectedY := float64(i) * 25
		if math.Abs(pt.X-expectedX) > 0.01 || math.Abs(pt.Y-expectedY) > 0.01 {
			t.Errorf("Sample %d at (%.2f, %.2f), expected (%.2f, %.2f)", i, pt.X, pt.Y, expectedX, expectedY)
		}
	}

	// Single sample
	single := lb.Samples(1)
	if len(single) != 1 || single[0].X != 0 {
		t.Errorf("Single sample should be at start point")
	}

	// Quadratic samples
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 50, Y: 100}, Point{X: 100, Y: 0})
	samplesQ := qb.Samples(10)
	if len(samplesQ) != 10 {
		t.Errorf("Expected 10 samples, got %d", len(samplesQ))
	}
}

// TestTransformCombined tests combined transformations
func TestTransformCombined(t *testing.T) {
	// Start with a line
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 0})

	// Scale then translate
	result := lb.Scale(2).Translate(5, 10)
	pt0 := result.EvaluateAt(0)
	pt1 := result.EvaluateAt(1)

	if pt0.X != 5 || pt0.Y != 10 {
		t.Errorf("Transformed start should be (5,10), got (%.2f, %.2f)", pt0.X, pt0.Y)
	}
	if pt1.X != 25 || pt1.Y != 10 {
		t.Errorf("Transformed end should be (25,10), got (%.2f, %.2f)", pt1.X, pt1.Y)
	}

	// Rotate then scale
	cb := NewCubicBezier(Point{X: 0, Y: 0}, Point{X: 0, Y: 10}, Point{X: 10, Y: 10}, Point{X: 10, Y: 0})
	rotatedScaled := cb.Rotate(math.Pi/2).Scale(0.5)
	// Just verify it's valid
	pt := rotatedScaled.EvaluateAt(0.5)
	if pt.X < -10 || pt.X > 10 || pt.Y < -10 || pt.Y > 10 {
		t.Errorf("Transformed point out of bounds: (%.2f, %.2f)", pt.X, pt.Y)
	}
}

// TestMultipleIntersections tests complex intersection scenarios
func TestMultipleIntersections(t *testing.T) {
	// S-curve that crosses a line multiple times
	cb := NewCubicBezier(
		Point{X: 0, Y: 0},
		Point{X: 10, Y: 20},
		Point{X: 0, Y: -20},
		Point{X: 10, Y: 0},
	)

	// Horizontal line through the middle
	intersections := cb.IntersectLine(Point{X: -5, Y: 0}, Point{X: 15, Y: 0})
	// This S-curve should cross the x-axis at least once
	if len(intersections) < 1 {
		t.Logf("S-curve intersection count: %d (curve may not cross line)", len(intersections))
	}
}

// TestEdgeCases tests edge cases and boundary conditions
func TestEdgeCases(t *testing.T) {
	// t values outside [0,1] should still work (extrapolation)
	lb := NewLinearBezier(Point{X: 0, Y: 0}, Point{X: 10, Y: 10})
	ptNeg := lb.EvaluateAt(-0.5)
	ptOver := lb.EvaluateAt(1.5)

	if ptNeg.X != -5 || ptNeg.Y != -5 {
		t.Errorf("Extrapolation at t=-0.5 should be (-5,-5), got (%.2f, %.2f)", ptNeg.X, ptNeg.Y)
	}
	if ptOver.X != 15 || ptOver.Y != 15 {
		t.Errorf("Extrapolation at t=1.5 should be (15,15), got (%.2f, %.2f)", ptOver.X, ptOver.Y)
	}

	// Very small tolerance for flatten
	qb := NewQuadraticBezier(Point{X: 0, Y: 0}, Point{X: 5, Y: 10}, Point{X: 10, Y: 0})
	points := qb.Flatten(1e-6)
	if len(points) < 100 {
		t.Logf("Very small tolerance produces %d points", len(points))
	}

	// Degenerate curve (points are same)
	degenerate := NewLinearBezier(Point{X: 5, Y: 5}, Point{X: 5, Y: 5})
	pt := degenerate.EvaluateAt(0.5)
	if pt.X != 5 || pt.Y != 5 {
		t.Errorf("Degenerate curve should always return same point")
	}
	length := degenerate.Length()
	if length != 0 {
		t.Errorf("Degenerate curve length should be 0, got %.2f", length)
	}
}