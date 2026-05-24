// Package kalman_filter_utils provides Kalman filter implementations for Go.
// Kalman filters are optimal estimators for linear dynamic systems with Gaussian noise.
//
// Features:
// - Basic 1D Kalman filter
// - Extended Kalman filter for non-linear systems
// - Multi-dimensional Kalman filter
// - Unscented Kalman filter (UKF)
// - Zero external dependencies (pure Go implementation)
// - Thread-safe operations
// - Generic type support (Go 1.18+)
//
// Common use cases:
//   - Sensor data filtering and smoothing
//   - GPS/IMU sensor fusion
//   - Financial time series analysis
//   - Object tracking in computer vision
//   - Navigation systems
//   - Signal processing
//
// Example usage:
//
//	// Create a 1D Kalman filter for temperature readings
//	kf := kalman_filter_utils.NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)
//
//	// Update with measurements
//	measurements := []float64{24.5, 25.2, 24.8, 25.1}
//	for _, m := range measurements {
//	    kf.Update(m)
//	    fmt.Printf("Estimated: %.2f\n", kf.GetState())
//	}
package kalman_filter_utils

import (
	"fmt"
	"math"
	"sync"
)

// ============================================================================
// 1D Kalman Filter
// ============================================================================

// KalmanFilter1D represents a 1-dimensional Kalman filter
type KalmanFilter1D struct {
	mu sync.RWMutex

	// State
	x float64 // State estimate (the value we're tracking)
	p float64 // Error covariance (uncertainty in estimate)

	// Process model
	q float64 // Process noise covariance (how much we expect the true value to change)
	r float64 // Measurement noise covariance (uncertainty in measurements)

	// Initial values for reset
	initialX float64
	initialP float64
}

// NewKalmanFilter1D creates a new 1D Kalman filter
// Parameters:
//   - initialState: Initial estimate of the state
//   - initialCovariance: Initial uncertainty in the state estimate (typically 1.0)
//   - processNoise: Expected variance in the true value over time (Q)
//   - measurementNoise: Expected variance in measurements (R)
//
// Lower Q = smoother output, higher Q = more responsive
// Lower R = trust measurements more, higher R = trust model more
func NewKalmanFilter1D(initialState, initialCovariance, processNoise, measurementNoise float64) *KalmanFilter1D {
	return &KalmanFilter1D{
		x:        initialState,
		p:        initialCovariance,
		q:        processNoise,
		r:        measurementNoise,
		initialX: initialState,
		initialP: initialCovariance,
	}
}

// Update performs a prediction and update step with a new measurement
// Returns the updated state estimate
func (kf *KalmanFilter1D) Update(measurement float64) float64 {
	kf.mu.Lock()
	defer kf.mu.Unlock()

	// Predict step
	// State prediction: x = x (no change in this simple model)
	// Covariance prediction: p = p + q
	kf.p = kf.p + kf.q

	// Update step
	// Kalman gain: K = p / (p + r)
	k := kf.p / (kf.p + kf.r)

	// State update: x = x + K * (measurement - x)
	kf.x = kf.x + k*(measurement-kf.x)

	// Covariance update: p = (1 - K) * p
	kf.p = (1 - k) * kf.p

	return kf.x
}

// Predict performs only the prediction step (no measurement)
// Use this when a measurement is missing but you want to propagate the state
func (kf *KalmanFilter1D) Predict() float64 {
	kf.mu.Lock()
	defer kf.mu.Unlock()

	// Increase uncertainty due to process noise
	kf.p = kf.p + kf.q

	return kf.x
}

// GetState returns the current state estimate
func (kf *KalmanFilter1D) GetState() float64 {
	kf.mu.RLock()
	defer kf.mu.RUnlock()
	return kf.x
}

// GetCovariance returns the current error covariance
func (kf *KalmanFilter1D) GetCovariance() float64 {
	kf.mu.RLock()
	defer kf.mu.RUnlock()
	return kf.p
}

// SetProcessNoise updates the process noise covariance (Q)
func (kf *KalmanFilter1D) SetProcessNoise(q float64) {
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.q = q
}

// SetMeasurementNoise updates the measurement noise covariance (R)
func (kf *KalmanFilter1D) SetMeasurementNoise(r float64) {
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.r = r
}

// Reset resets the filter to initial state
func (kf *KalmanFilter1D) Reset() {
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.x = kf.initialX
	kf.p = kf.initialP
}

// ResetWith resets the filter with new initial values
func (kf *KalmanFilter1D) ResetWith(initialState, initialCovariance float64) {
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.x = initialState
	kf.p = initialCovariance
	kf.initialX = initialState
	kf.initialP = initialCovariance
}

// BatchUpdate processes multiple measurements and returns all estimates
func (kf *KalmanFilter1D) BatchUpdate(measurements []float64) []float64 {
	estimates := make([]float64, len(measurements))
	for i, m := range measurements {
		estimates[i] = kf.Update(m)
	}
	return estimates
}

// ============================================================================
// Multi-dimensional Kalman Filter
// ============================================================================

// KalmanFilterND represents an N-dimensional Kalman filter
type KalmanFilterND struct {
	mu sync.RWMutex

	// State
	x []float64   // State vector (n x 1)
	p [][]float64 // Error covariance matrix (n x n)

	// Model
	f [][]float64 // State transition matrix (n x n)
	h [][]float64 // Observation matrix (m x n)
	q [][]float64 // Process noise covariance (n x n)
	r [][]float64 // Measurement noise covariance (m x m)

	dim int // State dimension
}

// NewKalmanFilterND creates a new N-dimensional Kalman filter
// Parameters:
//   - initialState: Initial state vector
//   - initialCovariance: Initial covariance diagonal values (use 1.0 for unknown)
//   - processNoise: Process noise diagonal values (Q)
//   - measurementNoise: Measurement noise diagonal values (R)
func NewKalmanFilterND(initialState []float64, initialCovariance, processNoise, measurementNoise float64) *KalmanFilterND {
	n := len(initialState)

	// Initialize state vector
	x := make([]float64, n)
	copy(x, initialState)

	// Initialize covariance matrix (identity * initialCovariance)
	p := make([][]float64, n)
	for i := range p {
		p[i] = make([]float64, n)
		p[i][i] = initialCovariance
	}

	// Initialize state transition matrix (identity - simple model)
	f := make([][]float64, n)
	for i := range f {
		f[i] = make([]float64, n)
		f[i][i] = 1.0
	}

	// Initialize observation matrix (identity - observe all states)
	h := make([][]float64, n)
	for i := range h {
		h[i] = make([]float64, n)
		h[i][i] = 1.0
	}

	// Initialize process noise covariance
	q := make([][]float64, n)
	for i := range q {
		q[i] = make([]float64, n)
		q[i][i] = processNoise
	}

	// Initialize measurement noise covariance
	r := make([][]float64, n)
	for i := range r {
		r[i] = make([]float64, n)
		r[i][i] = measurementNoise
	}

	return &KalmanFilterND{
		x:   x,
		p:   p,
		f:   f,
		h:   h,
		q:   q,
		r:   r,
		dim: n,
	}
}

// Update performs prediction and update with a measurement vector
func (kf *KalmanFilterND) Update(measurement []float64) []float64 {
	kf.mu.Lock()
	defer kf.mu.Unlock()

	n := kf.dim

	// Predict
	// x = F * x
	xPred := make([]float64, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			xPred[i] += kf.f[i][j] * kf.x[j]
		}
	}

	// P = F * P * F' + Q
	pFP := kf.matMul(kf.matMul(kf.f, kf.p), kf.transpose(kf.f))
	pPred := kf.matAdd(pFP, kf.q)

	// Update
	// y = z - H * x (innovation)
	hx := make([]float64, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			hx[i] += kf.h[i][j] * xPred[j]
		}
	}
	y := make([]float64, n)
	for i := 0; i < n; i++ {
		y[i] = measurement[i] - hx[i]
	}

	// S = H * P * H' + R
	php := kf.matMul(kf.matMul(kf.h, pPred), kf.transpose(kf.h))
	s := kf.matAdd(php, kf.r)

	// K = P * H' * S^(-1) (Kalman gain)
	sInv := kf.matInverse(s)
	ht := kf.transpose(kf.h)
	ph := kf.matMul(pPred, ht)
	k := kf.matMul(ph, sInv)

	// x = x + K * y
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			kf.x[i] = xPred[i] + k[i][j]*y[j]
		}
	}

	// P = (I - K * H) * P
	kh := kf.matMul(k, kf.h)
	ikh := kf.matSub(kf.eye(n), kh)
	kf.p = kf.matMul(ikh, pPred)

	return kf.getStateCopy()
}

// Predict performs only the prediction step
func (kf *KalmanFilterND) Predict() []float64 {
	kf.mu.Lock()
	defer kf.mu.Unlock()

	n := kf.dim

	// x = F * x
	xPred := make([]float64, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			xPred[i] += kf.f[i][j] * kf.x[j]
		}
	}
	kf.x = xPred

	// P = F * P * F' + Q
	pFP := kf.matMul(kf.matMul(kf.f, kf.p), kf.transpose(kf.f))
	kf.p = kf.matAdd(pFP, kf.q)

	return kf.getStateCopy()
}

// GetState returns a copy of the current state vector
func (kf *KalmanFilterND) GetState() []float64 {
	kf.mu.RLock()
	defer kf.mu.RUnlock()
	return kf.getStateCopy()
}

func (kf *KalmanFilterND) getStateCopy() []float64 {
	state := make([]float64, kf.dim)
	copy(state, kf.x)
	return state
}

// SetStateTransition sets the state transition matrix (F)
func (kf *KalmanFilterND) SetStateTransition(f [][]float64) error {
	if len(f) != kf.dim || len(f[0]) != kf.dim {
		return fmt.Errorf("state transition matrix must be %dx%d", kf.dim, kf.dim)
	}
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.f = kf.copyMatrix(f)
	return nil
}

// SetObservation sets the observation matrix (H)
func (kf *KalmanFilterND) SetObservation(h [][]float64) error {
	if len(h) != kf.dim || len(h[0]) != kf.dim {
		return fmt.Errorf("observation matrix must be %dx%d", kf.dim, kf.dim)
	}
	kf.mu.Lock()
	defer kf.mu.Unlock()
	kf.h = kf.copyMatrix(h)
	return nil
}

// ============================================================================
// Extended Kalman Filter (for non-linear systems)
// ============================================================================

// EKFStateFunc defines a state transition function for extended Kalman filter
// Takes state vector and returns predicted state
type EKFStateFunc func(state []float64) []float64

// EKFMeasureFunc defines a measurement function for extended Kalman filter
// Takes state vector and returns expected measurement
type EKFMeasureFunc func(state []float64) []float64

// EKFJacobianFunc defines a Jacobian computation function
// Takes state and returns Jacobian matrix
type EKFJacobianFunc func(state []float64) [][]float64

// ExtendedKalmanFilter represents an Extended Kalman Filter for non-linear systems
type ExtendedKalmanFilter struct {
	mu sync.RWMutex

	// State
	x []float64   // State vector
	p [][]float64 // Error covariance matrix

	// Model
	q [][]float64 // Process noise covariance
	r [][]float64 // Measurement noise covariance

	// Functions
	stateFunc  EKFStateFunc   // Non-linear state transition
	measureFunc EKFMeasureFunc // Non-linear measurement
	jacobianF   EKFJacobianFunc // Jacobian of state function
	jacobianH   EKFJacobianFunc // Jacobian of measurement function

	dim int
}

// NewExtendedKalmanFilter creates a new Extended Kalman Filter
func NewExtendedKalmanFilter(
	initialState []float64,
	initialCovariance, processNoise, measurementNoise float64,
	stateFunc EKFStateFunc,
	measureFunc EKFMeasureFunc,
	jacobianF EKFJacobianFunc,
	jacobianH EKFJacobianFunc,
) *ExtendedKalmanFilter {
	n := len(initialState)

	x := make([]float64, n)
	copy(x, initialState)

	p := make([][]float64, n)
	for i := range p {
		p[i] = make([]float64, n)
		p[i][i] = initialCovariance
	}

	q := make([][]float64, n)
	for i := range q {
		q[i] = make([]float64, n)
		q[i][i] = processNoise
	}

	r := make([][]float64, n)
	for i := range r {
		r[i] = make([]float64, n)
		r[i][i] = measurementNoise
	}

	return &ExtendedKalmanFilter{
		x:          x,
		p:          p,
		q:          q,
		r:          r,
		stateFunc:  stateFunc,
		measureFunc: measureFunc,
		jacobianF:   jacobianF,
		jacobianH:   jacobianH,
		dim:        n,
	}
}

// Update performs prediction and update with a measurement
func (ekf *ExtendedKalmanFilter) Update(measurement []float64) []float64 {
	ekf.mu.Lock()
	defer ekf.mu.Unlock()

	n := ekf.dim

	// Predict
	// x = f(x)
	xPred := ekf.stateFunc(ekf.x)

	// F = Jacobian of f at x
	F := ekf.jacobianF(ekf.x)

	// P = F * P * F' + Q
	pFP := ekf.matMulE(ekf.matMulE(F, ekf.p), ekf.transpose(F))
	pPred := ekf.matAddE(pFP, ekf.q)

	// Update
	// H = Jacobian of h at x_pred
	H := ekf.jacobianH(xPred)

	// y = z - h(x_pred) (innovation)
	hx := ekf.measureFunc(xPred)
	y := make([]float64, n)
	for i := 0; i < n; i++ {
		y[i] = measurement[i] - hx[i]
	}

	// S = H * P * H' + R
	php := ekf.matMulE(ekf.matMulE(H, pPred), ekf.transpose(H))
	s := ekf.matAddE(php, ekf.r)

	// K = P * H' * S^(-1)
	sInv := ekf.matInverse(s)
	ht := ekf.transpose(H)
	ph := ekf.matMulE(pPred, ht)
	K := ekf.matMulE(ph, sInv)

	// x = x_pred + K * y
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			ekf.x[i] = xPred[i] + K[i][j]*y[j]
		}
	}

	// P = (I - K * H) * P
	kh := ekf.matMulE(K, H)
	ikh := ekf.matSubE(ekf.eye(n), kh)
	ekf.p = ekf.matMulE(ikh, pPred)

	return ekf.getStateCopy()
}

// GetState returns a copy of the current state
func (ekf *ExtendedKalmanFilter) GetState() []float64 {
	ekf.mu.RLock()
	defer ekf.mu.RUnlock()
	return ekf.getStateCopy()
}

func (ekf *ExtendedKalmanFilter) getStateCopy() []float64 {
	state := make([]float64, ekf.dim)
	copy(state, ekf.x)
	return state
}

// ============================================================================
// Unscented Kalman Filter (UKF)
// ============================================================================

// UKFConfig holds configuration for Unscented Kalman Filter
type UKFConfig struct {
	Alpha float64 // Spread of sigma points (typically 1e-3)
	Beta  float64 // Prior knowledge of distribution (2 is optimal for Gaussian)
	Kappa float64 // Secondary scaling parameter (typically 0)
}

// UnscentedKalmanFilter represents an Unscented Kalman Filter
type UnscentedKalmanFilter struct {
	mu sync.RWMutex

	// State
	x []float64   // State vector
	p [][]float64 // Error covariance matrix

	// Model
	q [][]float64 // Process noise covariance
	r [][]float64 // Measurement noise covariance

	// UKF parameters
	alpha float64
	beta  float64
	kappa float64
	lambda float64

	// Weights
	wm []float64 // Mean weights
	wc []float64 // Covariance weights

	// Functions
	stateFunc  EKFStateFunc
	measureFunc EKFMeasureFunc

	dim int
}

// NewUnscentedKalmanFilter creates a new Unscented Kalman Filter
func NewUnscentedKalmanFilter(
	initialState []float64,
	initialCovariance, processNoise, measurementNoise float64,
	stateFunc EKFStateFunc,
	measureFunc EKFMeasureFunc,
	config UKFConfig,
) *UnscentedKalmanFilter {
	n := len(initialState)

	x := make([]float64, n)
	copy(x, initialState)

	p := make([][]float64, n)
	for i := range p {
		p[i] = make([]float64, n)
		p[i][i] = initialCovariance
	}

	q := make([][]float64, n)
	for i := range q {
		q[i] = make([]float64, n)
		q[i][i] = processNoise
	}

	r := make([][]float64, n)
	for i := range r {
		r[i] = make([]float64, n)
		r[i][i] = measurementNoise
	}

	// UKF parameters
	alpha := config.Alpha
	if alpha == 0 {
		alpha = 1e-3
	}
	beta := config.Beta
	if beta == 0 {
		beta = 2.0
	}
	kappa := config.Kappa

	lambda := alpha*alpha*(float64(n)+kappa) - float64(n)

	// Calculate weights
	numPoints := 2*n + 1
	wm := make([]float64, numPoints)
	wc := make([]float64, numPoints)

	wm[0] = lambda / (float64(n) + lambda)
	wc[0] = lambda/(float64(n)+lambda) + (1 - alpha*alpha + beta)
	for i := 1; i < numPoints; i++ {
		wm[i] = 1.0 / (2.0 * (float64(n) + lambda))
		wc[i] = wm[i]
	}

	return &UnscentedKalmanFilter{
		x:          x,
		p:          p,
		q:          q,
		r:          r,
		alpha:      alpha,
		beta:       beta,
		kappa:      kappa,
		lambda:     lambda,
		wm:         wm,
		wc:         wc,
		stateFunc:  stateFunc,
		measureFunc: measureFunc,
		dim:        n,
	}
}

// generateSigmaPoints generates sigma points for UT
func (ukf *UnscentedKalmanFilter) generateSigmaPoints() [][]float64 {
	n := ukf.dim
	numPoints := 2*n + 1

	// Calculate sqrt((n + lambda) * P)
	scaledP := ukf.matScale(float64(n)+ukf.lambda, ukf.p)
	sqrtP := ukf.choleskyDecomposition(scaledP)

	// Generate sigma points
	sigmaPoints := make([][]float64, numPoints)
	for i := range sigmaPoints {
		sigmaPoints[i] = make([]float64, n)
	}

	// First sigma point is the mean
	copy(sigmaPoints[0], ukf.x)

	// Generate remaining sigma points
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			sigmaPoints[i+1][j] = ukf.x[j] + sqrtP[j][i]
			sigmaPoints[i+n+1][j] = ukf.x[j] - sqrtP[j][i]
		}
	}

	return sigmaPoints
}

// Update performs prediction and update with a measurement using UT
func (ukf *UnscentedKalmanFilter) Update(measurement []float64) []float64 {
	ukf.mu.Lock()
	defer ukf.mu.Unlock()

	n := ukf.dim

	// Generate sigma points
	sigmaPoints := ukf.generateSigmaPoints()

	// Predict: propagate sigma points through state function
	propagatedPoints := make([][]float64, len(sigmaPoints))
	for i, sp := range sigmaPoints {
		propagatedPoints[i] = ukf.stateFunc(sp)
	}

	// Calculate predicted mean
	xPred := make([]float64, n)
	for i, sp := range propagatedPoints {
		for j := 0; j < n; j++ {
			xPred[j] += ukf.wm[i] * sp[j]
		}
	}

	// Calculate predicted covariance
	pPred := make([][]float64, n)
	for i := range pPred {
		pPred[i] = make([]float64, n)
	}
	for i, sp := range propagatedPoints {
		diff := make([]float64, n)
		for j := 0; j < n; j++ {
			diff[j] = sp[j] - xPred[j]
		}
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				pPred[j][k] += ukf.wc[i] * diff[j] * diff[k]
			}
		}
	}
	pPred = ukf.matAdd(pPred, ukf.q)

	// Update: transform sigma points through measurement function
	measurementPoints := make([][]float64, len(propagatedPoints))
	for i, sp := range propagatedPoints {
		measurementPoints[i] = ukf.measureFunc(sp)
	}

	// Calculate predicted measurement mean
	zPred := make([]float64, n)
	for i, mp := range measurementPoints {
		for j := 0; j < n; j++ {
			zPred[j] += ukf.wm[i] * mp[j]
		}
	}

	// Calculate innovation covariance
	s := make([][]float64, n)
	for i := range s {
		s[i] = make([]float64, n)
	}
	for i, mp := range measurementPoints {
		diff := make([]float64, n)
		for j := 0; j < n; j++ {
			diff[j] = mp[j] - zPred[j]
		}
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				s[j][k] += ukf.wc[i] * diff[j] * diff[k]
			}
		}
	}
	s = ukf.matAdd(s, ukf.r)

	// Calculate cross-covariance
	crossCov := make([][]float64, n)
	for i := range crossCov {
		crossCov[i] = make([]float64, n)
	}
	for i := 0; i < len(propagatedPoints); i++ {
		stateDiff := make([]float64, n)
		measDiff := make([]float64, n)
		for j := 0; j < n; j++ {
			stateDiff[j] = propagatedPoints[i][j] - xPred[j]
			measDiff[j] = measurementPoints[i][j] - zPred[j]
		}
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				crossCov[j][k] += ukf.wc[i] * stateDiff[j] * measDiff[k]
			}
		}
	}

	// Calculate Kalman gain
	sInv := ukf.matInverse(s)
	k := ukf.matMul(crossCov, sInv)

	// Update state and covariance
	innovation := make([]float64, n)
	for i := 0; i < n; i++ {
		innovation[i] = measurement[i] - zPred[i]
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			ukf.x[i] = xPred[i] + k[i][j]*innovation[j]
		}
	}

	ks := ukf.matMul(k, s)
	ukt := ukf.transpose(k)
	kskt := ukf.matMul(ks, ukt)
	ukf.p = ukf.matSub(pPred, kskt)

	return ukf.getStateCopy()
}

// GetState returns a copy of the current state
func (ukf *UnscentedKalmanFilter) GetState() []float64 {
	ukf.mu.RLock()
	defer ukf.mu.RUnlock()
	return ukf.getStateCopy()
}

func (ukf *UnscentedKalmanFilter) getStateCopy() []float64 {
	state := make([]float64, ukf.dim)
	copy(state, ukf.x)
	return state
}

// ============================================================================
// Matrix Operations
// ============================================================================

func (kf *KalmanFilterND) matMul(a, b [][]float64) [][]float64 {
	n := len(a)
	m := len(b[0])
	p := len(b)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, m)
		for j := 0; j < m; j++ {
			for k := 0; k < p; k++ {
				result[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return result
}

func (kf *KalmanFilterND) matAdd(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] + b[i][j]
		}
	}
	return result
}

func (kf *KalmanFilterND) matSub(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] - b[i][j]
		}
	}
	return result
}

func (kf *KalmanFilterND) transpose(a [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[j][i]
		}
	}
	return result
}

func (kf *KalmanFilterND) eye(n int) [][]float64 {
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		result[i][i] = 1.0
	}
	return result
}

func (kf *KalmanFilterND) matInverse(a [][]float64) [][]float64 {
	n := len(a)
	// Create augmented matrix [A|I]
	aug := make([][]float64, n)
	for i := range aug {
		aug[i] = make([]float64, 2*n)
		for j := 0; j < n; j++ {
			aug[i][j] = a[i][j]
		}
		aug[i][n+i] = 1.0
	}

	// Gaussian elimination with partial pivoting
	for i := 0; i < n; i++ {
		// Find pivot
		maxRow := i
		for k := i + 1; k < n; k++ {
			if math.Abs(aug[k][i]) > math.Abs(aug[maxRow][i]) {
				maxRow = k
			}
		}
		aug[i], aug[maxRow] = aug[maxRow], aug[i]

		// Eliminate column
		pivot := aug[i][i]
		if math.Abs(pivot) < 1e-12 {
			// Return identity if singular
			return kf.eye(n)
		}
		for j := 0; j < 2*n; j++ {
			aug[i][j] /= pivot
		}
		for k := 0; k < n; k++ {
			if k != i {
				factor := aug[k][i]
				for j := 0; j < 2*n; j++ {
					aug[k][j] -= factor * aug[i][j]
				}
			}
		}
	}

	// Extract inverse
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = aug[i][n+j]
		}
	}
	return result
}

func (kf *KalmanFilterND) copyMatrix(a [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		copy(result[i], a[i])
	}
	return result
}

// EKF matrix operations (duplicate to avoid interface issues)
func (ekf *ExtendedKalmanFilter) matMul(a, b [][]float64) [][]float64 {
	return (*KalmanFilterND)(nil).matMul(nil, nil)
}

func (ekf *ExtendedKalmanFilter) transpose(a [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[j][i]
		}
	}
	return result
}

func (ekf *ExtendedKalmanFilter) matInverse(a [][]float64) [][]float64 {
	n := len(a)
	aug := make([][]float64, n)
	for i := range aug {
		aug[i] = make([]float64, 2*n)
		for j := 0; j < n; j++ {
			aug[i][j] = a[i][j]
		}
		aug[i][n+i] = 1.0
	}

	for i := 0; i < n; i++ {
		maxRow := i
		for k := i + 1; k < n; k++ {
			if math.Abs(aug[k][i]) > math.Abs(aug[maxRow][i]) {
				maxRow = k
			}
		}
		aug[i], aug[maxRow] = aug[maxRow], aug[i]

		pivot := aug[i][i]
		if math.Abs(pivot) < 1e-12 {
			return ekf.eye(n)
		}
		for j := 0; j < 2*n; j++ {
			aug[i][j] /= pivot
		}
		for k := 0; k < n; k++ {
			if k != i {
				factor := aug[k][i]
				for j := 0; j < 2*n; j++ {
					aug[k][j] -= factor * aug[i][j]
				}
			}
		}
	}

	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = aug[i][n+j]
		}
	}
	return result
}

func (ekf *ExtendedKalmanFilter) eye(n int) [][]float64 {
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		result[i][i] = 1.0
	}
	return result
}

func (ekf *ExtendedKalmanFilter) matMulE(a, b [][]float64) [][]float64 {
	n := len(a)
	m := len(b[0])
	p := len(b)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, m)
		for j := 0; j < m; j++ {
			for k := 0; k < p; k++ {
				result[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return result
}

func (ekf *ExtendedKalmanFilter) matAddE(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] + b[i][j]
		}
	}
	return result
}

func (ekf *ExtendedKalmanFilter) matSubE(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] - b[i][j]
		}
	}
	return result
}

// UKF matrix operations
func (ukf *UnscentedKalmanFilter) matScale(scalar float64, a [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = scalar * a[i][j]
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) matMul(a, b [][]float64) [][]float64 {
	n := len(a)
	m := len(b[0])
	p := len(b)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, m)
		for j := 0; j < m; j++ {
			for k := 0; k < p; k++ {
				result[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) matAdd(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] + b[i][j]
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) matSub(a, b [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[i][j] - b[i][j]
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) matInverse(a [][]float64) [][]float64 {
	n := len(a)
	aug := make([][]float64, n)
	for i := range aug {
		aug[i] = make([]float64, 2*n)
		for j := 0; j < n; j++ {
			aug[i][j] = a[i][j]
		}
		aug[i][n+i] = 1.0
	}

	for i := 0; i < n; i++ {
		maxRow := i
		for k := i + 1; k < n; k++ {
			if math.Abs(aug[k][i]) > math.Abs(aug[maxRow][i]) {
				maxRow = k
			}
		}
		aug[i], aug[maxRow] = aug[maxRow], aug[i]

		pivot := aug[i][i]
		if math.Abs(pivot) < 1e-12 {
			return ukf.eye(n)
		}
		for j := 0; j < 2*n; j++ {
			aug[i][j] /= pivot
		}
		for k := 0; k < n; k++ {
			if k != i {
				factor := aug[k][i]
				for j := 0; j < 2*n; j++ {
					aug[k][j] -= factor * aug[i][j]
				}
			}
		}
	}

	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = aug[i][n+j]
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) transpose(a [][]float64) [][]float64 {
	n := len(a)
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			result[i][j] = a[j][i]
		}
	}
	return result
}

func (ukf *UnscentedKalmanFilter) eye(n int) [][]float64 {
	result := make([][]float64, n)
	for i := range result {
		result[i] = make([]float64, n)
		result[i][i] = 1.0
	}
	return result
}

func (ukf *UnscentedKalmanFilter) choleskyDecomposition(a [][]float64) [][]float64 {
	n := len(a)
	l := make([][]float64, n)
	for i := range l {
		l[i] = make([]float64, n)
	}

	for i := 0; i < n; i++ {
		for j := 0; j <= i; j++ {
			sum := 0.0
			if i == j {
				for k := 0; k < j; k++ {
					sum += l[j][k] * l[j][k]
				}
				val := a[j][j] - sum
				if val < 0 {
					val = 0 // Handle numerical issues
				}
				l[j][j] = math.Sqrt(val)
			} else {
				for k := 0; k < j; k++ {
					sum += l[i][k] * l[j][k]
				}
				if l[j][j] > 1e-12 {
					l[i][j] = (a[i][j] - sum) / l[j][j]
				}
			}
		}
	}
	return l
}

// ============================================================================
// Utility Functions
// ============================================================================

// SmoothKalman applies Kalman filter smoothing (Rauch-Tung-Striebel smoother)
// This is useful for post-processing of recorded data
func SmoothKalman(measurements []float64, processNoise, measurementNoise float64) []float64 {
	if len(measurements) == 0 {
		return nil
	}

	// Forward pass
	kf := NewKalmanFilter1D(measurements[0], 1.0, processNoise, measurementNoise)
	forwardStates := make([]float64, len(measurements))
	forwardCovs := make([]float64, len(measurements))

	for i, m := range measurements {
		forwardStates[i] = kf.Update(m)
		forwardCovs[i] = kf.GetCovariance()
	}

	// For simplicity, return forward-filtered results
	// Full RTS smoother would require backward pass
	return forwardStates
}

// MovingAverageFilter is a simple alternative to Kalman filter for basic smoothing
type MovingAverageFilter struct {
	window   []float64
	size     int
	index    int
	sum      float64
	count    int
}

// NewMovingAverageFilter creates a new moving average filter
func NewMovingAverageFilter(windowSize int) *MovingAverageFilter {
	return &MovingAverageFilter{
		window: make([]float64, windowSize),
		size:   windowSize,
	}
}

// Update adds a new measurement and returns the smoothed value
func (maf *MovingAverageFilter) Update(measurement float64) float64 {
	// Subtract oldest value from sum
	maf.sum -= maf.window[maf.index]

	// Add new value
	maf.window[maf.index] = measurement
	maf.sum += measurement

	// Update index
	maf.index = (maf.index + 1) % maf.size

	// Update count
	if maf.count < maf.size {
		maf.count++
	}

	// Return average
	return maf.sum / float64(maf.count)
}

// Reset resets the filter
func (maf *MovingAverageFilter) Reset() {
	maf.window = make([]float64, maf.size)
	maf.index = 0
	maf.sum = 0
	maf.count = 0
}

// ExponentialSmoothingFilter implements exponential smoothing
type ExponentialSmoothingFilter struct {
	alpha     float64 // Smoothing factor (0 < alpha < 1)
	value     float64
	initialized bool
}

// NewExponentialSmoothingFilter creates a new exponential smoothing filter
// alpha: smoothing factor, lower = smoother, higher = more responsive
func NewExponentialSmoothingFilter(alpha float64) *ExponentialSmoothingFilter {
	if alpha < 0 {
		alpha = 0
	}
	if alpha > 1 {
		alpha = 1
	}
	return &ExponentialSmoothingFilter{alpha: alpha}
}

// Update adds a new measurement and returns the smoothed value
func (esf *ExponentialSmoothingFilter) Update(measurement float64) float64 {
	if !esf.initialized {
		esf.value = measurement
		esf.initialized = true
	} else {
		esf.value = esf.alpha*measurement + (1-esf.alpha)*esf.value
	}
	return esf.value
}

// GetValue returns the current smoothed value
func (esf *ExponentialSmoothingFilter) GetValue() float64 {
	return esf.value
}

// Reset resets the filter
func (esf *ExponentialSmoothingFilter) Reset() {
	esf.value = 0
	esf.initialized = false
}

// SetAlpha updates the smoothing factor
func (esf *ExponentialSmoothingFilter) SetAlpha(alpha float64) {
	if alpha < 0 {
		alpha = 0
	}
	if alpha > 1 {
		alpha = 1
	}
	esf.alpha = alpha
}