package main

import (
	"fmt"
	"math"

	bezier "github.com/ayukyo/alltoolkit/Go/bezier_curve_utils"
)

func main() {
	fmt.Println("=== Bezier Curve Utils Examples ===")
	fmt.Println()

	// Example 1: Linear Bezier (Straight Line)
	exampleLinearBezier()

	// Example 2: Quadratic Bezier (Parabola)
	exampleQuadraticBezier()

	// Example 3: Cubic Bezier (S-Curve)
	exampleCubicBezier()

	// Example 4: Easing Functions
	exampleEasingFunctions()

	// Example 5: Curve Transformations
	exampleTransformations()

	// Example 6: Circle Approximation
	exampleCircleApproximation()

	// Example 7: Arbitrary Degree Curve
	exampleArbitraryBezier()

	// Example 8: Line Intersection
	exampleIntersection()
}

func exampleLinearBezier() {
	fmt.Println("--- Example 1: Linear Bezier ---")

	lb := bezier.NewLinearBezier(
		bezier.Point{X: 0, Y: 0},
		bezier.Point{X: 100, Y: 100},
	)

	fmt.Println("Control Points: (0,0) -> (100,100)")
	fmt.Println("Points along the curve:")
	for t := 0.0; t <= 1.0; t += 0.25 {
		pt := lb.EvaluateAt(t)
		fmt.Printf("  t=%.2f: (%.2f, %.2f)\n", t, pt.X, pt.Y)
	}

	length := lb.Length()
	fmt.Printf("Length: %.2f\n", length)
	fmt.Println()
}

func exampleQuadraticBezier() {
	fmt.Println("--- Example 2: Quadratic Bezier (Parabola) ---")

	qb := bezier.NewQuadraticBezier(
		bezier.Point{X: 0, Y: 0},
		bezier.Point{X: 50, Y: 100}, // Control point creates peak
		bezier.Point{X: 100, Y: 0},
	)

	fmt.Println("Control Points: (0,0) -> (50,100) -> (100,0)")
	fmt.Println("Points along the parabola:")
	for t := 0.0; t <= 1.0; t += 0.25 {
		pt := qb.EvaluateAt(t)
		fmt.Printf("  t=%.2f: (%.2f, %.2f)\n", t, pt.X, pt.Y)
	}

	bbox := qb.BoundingBox()
	fmt.Printf("Bounding Box: X[%.2f, %.2f], Y[%.2f, %.2f]\n",
		bbox.Min.X, bbox.Max.X, bbox.Min.Y, bbox.Max.Y)

	length := qb.Length()
	fmt.Printf("Approximate Length: %.2f\n", length)
	fmt.Println()
}

func exampleCubicBezier() {
	fmt.Println("--- Example 3: Cubic Bezier (S-Curve) ---")

	cb := bezier.NewCubicBezier(
		bezier.Point{X: 0, Y: 0},
		bezier.Point{X: 0, Y: 100},
		bezier.Point{X: 100, Y: 100},
		bezier.Point{X: 100, Y: 0},
	)

	fmt.Println("Control Points: (0,0) -> (0,100) -> (100,100) -> (100,0)")
	fmt.Println("Points along the S-curve:")
	for t := 0.0; t <= 1.0; t += 0.25 {
		pt := cb.EvaluateAt(t)
		fmt.Printf("  t=%.2f: (%.2f, %.2f)\n", t, pt.X, pt.Y)
	}

	// Split at midpoint
	left, right := cb.SplitAt(0.5)
	fmt.Println("Split at t=0.5:")
	fmt.Printf("  Left ends at: (%.2f, %.2f)\n",
		left.EvaluateAt(1).X, left.EvaluateAt(1).Y)
	fmt.Printf("  Right starts at: (%.2f, %.2f)\n",
		right.EvaluateAt(0).X, right.EvaluateAt(0).Y)
	fmt.Println()
}

func exampleEasingFunctions() {
	fmt.Println("--- Example 4: Easing Functions ---")

	fmt.Println("Progress values for different easing functions:")
	fmt.Println("t\tLinear\tEaseIn\tEaseOut\tEaseInOut")

	for t := 0.0; t <= 1.0; t += 0.25 {
		linear := bezier.EaseLinear.Ease(t)
		easeIn := bezier.EaseIn.Ease(t)
		easeOut := bezier.EaseOut.Ease(t)
		easeInOut := bezier.EaseInOut.Ease(t)
		fmt.Printf("%.2f\t%.3f\t%.3f\t%.3f\t%.3f\n",
			t, linear, easeIn, easeOut, easeInOut)
	}

	// Custom easing function (similar to CSS cubic-bezier(0.68, -0.55, 0.27, 1.55))
	customEase := bezier.NewEasingFunction(0.68, -0.55, 0.27, 1.55)
	fmt.Println("\nCustom easing (bounce effect):")
	for t := 0.0; t <= 1.0; t += 0.25 {
		fmt.Printf("  t=%.2f: %.3f\n", t, customEase.Ease(t))
	}
	fmt.Println()
}

func exampleTransformations() {
	fmt.Println("--- Example 5: Curve Transformations ---")

	// Original curve
	cb := bezier.NewCubicBezier(
		bezier.Point{X: 0, Y: 0},
		bezier.Point{X: 0, Y: 50},
		bezier.Point{X: 50, Y: 50},
		bezier.Point{X: 50, Y: 0},
	)

	fmt.Println("Original curve endpoints:")
	fmt.Printf("  Start: (%.2f, %.2f)\n", cb.EvaluateAt(0).X, cb.EvaluateAt(0).Y)
	fmt.Printf("  End: (%.2f, %.2f)\n", cb.EvaluateAt(1).X, cb.EvaluateAt(1).Y)

	// Translate
	translated := cb.Translate(100, 50)
	fmt.Println("Translated (+100, +50):")
	fmt.Printf("  Start: (%.2f, %.2f)\n", translated.EvaluateAt(0).X, translated.EvaluateAt(0).Y)
	fmt.Printf("  End: (%.2f, %.2f)\n", translated.EvaluateAt(1).X, translated.EvaluateAt(1).Y)

	// Scale
	scaled := cb.Scale(2)
	fmt.Println("Scaled (x2):")
	fmt.Printf("  Start: (%.2f, %.2f)\n", scaled.EvaluateAt(0).X, scaled.EvaluateAt(0).Y)
	fmt.Printf("  End: (%.2f, %.2f)\n", scaled.EvaluateAt(1).X, scaled.EvaluateAt(1).Y)

	// Rotate
	rotated := cb.Rotate(math.Pi / 4) // 45 degrees
	fmt.Println("Rotated (45°):")
	fmt.Printf("  Start: (%.2f, %.2f)\n", rotated.EvaluateAt(0).X, rotated.EvaluateAt(0).Y)
	fmt.Printf("  End: (%.2f, %.2f)\n", rotated.EvaluateAt(1).X, rotated.EvaluateAt(1).Y)

	// Reverse
	reversed := cb.Reverse()
	fmt.Println("Reversed:")
	fmt.Printf("  Start: (%.2f, %.2f)\n", reversed.EvaluateAt(0).X, reversed.EvaluateAt(0).Y)
	fmt.Printf("  End: (%.2f, %.2f)\n", reversed.EvaluateAt(1).X, reversed.EvaluateAt(1).Y)
	fmt.Println()
}

func exampleCircleApproximation() {
	fmt.Println("--- Example 6: Circle Approximation ---")

	center := bezier.Point{X: 50, Y: 50}
	radius := 40.0

	curves := bezier.ApproximateCircle(center, radius)
	fmt.Printf("Circle approximated by %d cubic Bezier curves:\n", len(curves))

	for i, curve := range curves {
		start := curve.EvaluateAt(0)
		end := curve.EvaluateAt(1)
		fmt.Printf("  Curve %d: (%.2f, %.2f) -> (%.2f, %.2f)\n",
			i, start.X, start.Y, end.X, end.Y)
	}

	// Check continuity
	fmt.Println("Checking continuity between curves:")
	for i := 0; i < 4; i++ {
		end := curves[i].EvaluateAt(1)
		nextStart := curves[(i+1)%4].EvaluateAt(0)
		distance := math.Sqrt((end.X-nextStart.X)*(end.X-nextStart.X) + (end.Y-nextStart.Y)*(end.Y-nextStart.Y))
		fmt.Printf("  Curve %d -> %d: gap %.6f (should be ~0)\n", i, (i+1)%4, distance)
	}

	// Ellipse approximation
	fmt.Println("\nEllipse approximation (rx=40, ry=20):")
	ellipseCurves := bezier.ApproximateEllipse(center, 40, 20)
	fmt.Printf("  Number of curves: %d\n", len(ellipseCurves))
	fmt.Println()
}

func exampleArbitraryBezier() {
	fmt.Println("--- Example 7: Arbitrary Degree Bezier ---")

	// 5-degree Bezier curve (6 control points)
	points := []bezier.Point{
		{X: 0, Y: 0},
		{X: 20, Y: 80},
		{X: 40, Y: 120},
		{X: 60, Y: 80},
		{X: 80, Y: 20},
		{X: 100, Y: 60},
	}

	bc, err := bezier.NewBezierCurve(points)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("Degree-%d Bezier curve:\n", bc.Degree())
	fmt.Println("Control Points:")
	for i, p := range points {
		fmt.Printf("  P%d: (%.2f, %.2f)\n", i, p.X, p.Y)
	}

	fmt.Println("Points along the curve:")
	for t := 0.0; t <= 1.0; t += 0.25 {
		pt := bc.EvaluateAt(t)
		fmt.Printf("  t=%.2f: (%.2f, %.2f)\n", t, pt.X, pt.Y)
	}

	// Check if curve is linear
	fmt.Printf("Is linear (tolerance=5)? %v\n", bc.IsLinear(5.0))
	fmt.Println()
}

func exampleIntersection() {
	fmt.Println("--- Example 8: Line Intersection ---")

	// Parabola
	qb := bezier.NewQuadraticBezier(
		bezier.Point{X: 0, Y: 0},
		bezier.Point{X: 50, Y: 100},
		bezier.Point{X: 100, Y: 0},
	)

	// Horizontal line at y=50
	lineStart := bezier.Point{X: -10, Y: 50}
	lineEnd := bezier.Point{X: 110, Y: 50}

	fmt.Println("Parabola: (0,0) -> (50,100) -> (100,0)")
	fmt.Println("Line: y=50 (horizontal)")
	fmt.Println()

	intersections := qb.IntersectLine(lineStart, lineEnd)
	fmt.Printf("Intersections found: %d\n", len(intersections))
	for i, pt := range intersections {
		fmt.Printf("  Intersection %d: (%.2f, %.2f)\n", i, pt.X, pt.Y)
	}

	// Distance from a point to the curve
	testPoint := bezier.Point{X: 50, Y: -10}
	distance := qb.DistanceToPoint(testPoint)
	fmt.Printf("\nDistance from (50, -10) to curve: %.2f\n", distance)

	// Point on the curve
	onCurvePoint := qb.EvaluateAt(0.5)
	distanceOn := qb.DistanceToPoint(onCurvePoint)
	fmt.Printf("Distance from curve point (50, %.2f) to curve: %.6f (should be ~0)\n",
		onCurvePoint.Y, distanceOn)
	fmt.Println()
}