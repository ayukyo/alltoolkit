// Package weightedroundrobin provides weighted round-robin load balancing algorithms.
// It supports multiple selection strategies for distributing load across backends.
//
// Features:
//   - Weighted Round Robin: Standard weighted selection
//   - Smooth Weighted Round Robin: Nginx-style smooth distribution
//   - Weighted Random: Probability-based selection
//   - Least Connections: Select backend with fewest active connections
//
// Zero external dependencies - uses only Go standard library.
package weightedroundrobin

import (
	"errors"
	"math/rand"
	"sync"
	"sync/atomic"
)

// Backend represents a backend server with weight and connection tracking.
type Backend struct {
	Name          string
	Weight        int
	CurrentWeight int // For smooth weighted round-robin
	Connections   int64
	mu            sync.Mutex
}

// WeightedRoundRobin implements weighted round-robin load balancing.
type WeightedRoundRobin struct {
	backends []*Backend
	mu       sync.RWMutex
	index    int
	count    int // Counter for current backend
}

// NewWeightedRoundRobin creates a new weighted round-robin selector.
func NewWeightedRoundRobin(backends []*Backend) (*WeightedRoundRobin, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	for _, b := range backends {
		if b.Weight <= 0 {
			return nil, errors.New("weight must be positive")
		}
	}
	return &WeightedRoundRobin{
		backends: backends,
	}, nil
}

// Select returns the next backend using weighted round-robin.
func (w *WeightedRoundRobin) Select() *Backend {
	w.mu.Lock()
	defer w.mu.Unlock()

	// Find max weight for cycle calculation
	maxWeight := 0
	for _, b := range w.backends {
		if b.Weight > maxWeight {
			maxWeight = b.Weight
		}
	}

	for {
		w.index = (w.index + 1) % len(w.backends)
		if w.index == 0 {
			w.count--
			if w.count <= 0 {
				w.count = maxWeight
			}
		}

		if w.backends[w.index].Weight >= w.count {
			return w.backends[w.index]
		}
	}
}

// SmoothWeightedRoundRobin implements Nginx-style smooth weighted round-robin.
// This distributes backends more evenly, avoiding "thundering herd" problems.
type SmoothWeightedRoundRobin struct {
	backends []*Backend
	mu       sync.Mutex
}

// NewSmoothWeightedRoundRobin creates a new smooth weighted round-robin selector.
func NewSmoothWeightedRoundRobin(backends []*Backend) (*SmoothWeightedRoundRobin, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	for _, b := range backends {
		if b.Weight <= 0 {
			return nil, errors.New("weight must be positive")
		}
		b.CurrentWeight = 0
	}
	return &SmoothWeightedRoundRobin{
		backends: backends,
	}, nil
}

// Select returns the next backend using smooth weighted round-robin.
func (s *SmoothWeightedRoundRobin) Select() *Backend {
	s.mu.Lock()
	defer s.mu.Unlock()

	total := 0
	var selected *Backend

	// Add weight to current weight for all backends
	for _, b := range s.backends {
		b.CurrentWeight += b.Weight
		total += b.Weight
	}

	// Select backend with highest current weight
	maxWeight := -1
	for _, b := range s.backends {
		if b.CurrentWeight > maxWeight {
			maxWeight = b.CurrentWeight
			selected = b
		}
	}

	// Subtract total from selected backend's current weight
	selected.CurrentWeight -= total

	return selected
}

// WeightedRandom implements weighted random selection.
type WeightedRandom struct {
	backends  []*Backend
	weights   []int
	prefixSum []int
	total     int
	mu        sync.RWMutex
}

// NewWeightedRandom creates a new weighted random selector.
func NewWeightedRandom(backends []*Backend) (*WeightedRandom, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	weights := make([]int, len(backends))
	prefixSum := make([]int, len(backends))
	total := 0

	for i, b := range backends {
		if b.Weight <= 0 {
			return nil, errors.New("weight must be positive")
		}
		weights[i] = b.Weight
		total += b.Weight
		prefixSum[i] = total
	}

	return &WeightedRandom{
		backends:  backends,
		weights:   weights,
		prefixSum: prefixSum,
		total:     total,
	}, nil
}

// Select returns a random backend weighted by probability.
func (w *WeightedRandom) Select() *Backend {
	w.mu.RLock()
	defer w.mu.RUnlock()

	r := rand.Intn(w.total) + 1

	// Binary search for the backend
	left, right := 0, len(w.prefixSum)-1
	for left < right {
		mid := (left + right) / 2
		if w.prefixSum[mid] < r {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return w.backends[left]
}

// LeastConnections implements least-connections load balancing.
type LeastConnections struct {
	backends []*Backend
	mu       sync.RWMutex
}

// NewLeastConnections creates a new least-connections selector.
func NewLeastConnections(backends []*Backend) (*LeastConnections, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	return &LeastConnections{
		backends: backends,
	}, nil
}

// Select returns the backend with the least active connections.
func (l *LeastConnections) Select() *Backend {
	l.mu.RLock()
	defer l.mu.RUnlock()

	var selected *Backend
	minConn := int64(-1)

	for _, b := range l.backends {
		conn := atomic.LoadInt64(&b.Connections)
		if minConn == -1 || conn < minConn {
			minConn = conn
			selected = b
		}
	}

	return selected
}

// IncrementConnection increments the connection count for a backend.
func (l *LeastConnections) IncrementConnection(b *Backend) {
	atomic.AddInt64(&b.Connections, 1)
}

// DecrementConnection decrements the connection count for a backend.
func (l *LeastConnections) DecrementConnection(b *Backend) {
	atomic.AddInt64(&b.Connections, -1)
}

// AddBackend adds a new backend to the selector.
func (l *LeastConnections) AddBackend(backend *Backend) error {
	if backend.Weight <= 0 {
		return errors.New("weight must be positive")
	}
	l.mu.Lock()
	defer l.mu.Unlock()
	l.backends = append(l.backends, backend)
	return nil
}

// RemoveBackend removes a backend by name.
func (l *LeastConnections) RemoveBackend(name string) bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	for i, b := range l.backends {
		if b.Name == name {
			l.backends = append(l.backends[:i], l.backends[i+1:]...)
			return true
		}
	}
	return false
}

// WeightedLeastConnections combines weight and connection count.
type WeightedLeastConnections struct {
	backends []*Backend
	mu       sync.RWMutex
}

// NewWeightedLeastConnections creates a new weighted least-connections selector.
func NewWeightedLeastConnections(backends []*Backend) (*WeightedLeastConnections, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	for _, b := range backends {
		if b.Weight <= 0 {
			return nil, errors.New("weight must be positive")
		}
	}
	return &WeightedLeastConnections{
		backends: backends,
	}, nil
}

// Select returns the backend with the lowest (connections / weight) ratio.
func (w *WeightedLeastConnections) Select() *Backend {
	w.mu.RLock()
	defer w.mu.RUnlock()

	var selected *Backend
	minRatio := float64(-1)

	for _, b := range w.backends {
		conn := float64(atomic.LoadInt64(&b.Connections))
		ratio := conn / float64(b.Weight)
		if minRatio == -1 || ratio < minRatio {
			minRatio = ratio
			selected = b
		}
	}

	return selected
}

// GetBackends returns all backends (for monitoring/debugging).
func (w *WeightedLeastConnections) GetBackends() []*Backend {
	w.mu.RLock()
	defer w.mu.RUnlock()
	result := make([]*Backend, len(w.backends))
	copy(result, w.backends)
	return result
}

// PowerOfTwoChoices implements the "power of two choices" algorithm.
// It picks two random backends and selects the one with fewer connections.
// This provides good load distribution with O(1) complexity.
type PowerOfTwoChoices struct {
	backends []*Backend
	mu       sync.RWMutex
}

// NewPowerOfTwoChoices creates a new power-of-two-choices selector.
func NewPowerOfTwoChoices(backends []*Backend) (*PowerOfTwoChoices, error) {
	if len(backends) == 0 {
		return nil, errors.New("backends cannot be empty")
	}
	if len(backends) < 2 {
		return nil, errors.New("need at least 2 backends for power of two choices")
	}
	return &PowerOfTwoChoices{
		backends: backends,
	}, nil
}

// Select returns a backend using power of two choices algorithm.
func (p *PowerOfTwoChoices) Select() *Backend {
	p.mu.RLock()
	defer p.mu.RUnlock()

	n := len(p.backends)

	// Pick two random indices
	i := rand.Intn(n)
	j := rand.Intn(n - 1)
	if j >= i {
		j++
	}

	b1, b2 := p.backends[i], p.backends[j]

	// Select the one with fewer connections
	if atomic.LoadInt64(&b1.Connections) <= atomic.LoadInt64(&b2.Connections) {
		return b1
	}
	return b2
}

// NewBackend creates a new backend with the given name and weight.
func NewBackend(name string, weight int) *Backend {
	return &Backend{
		Name:   name,
		Weight: weight,
	}
}

// GetConnections returns the current connection count.
func (b *Backend) GetConnections() int64 {
	return atomic.LoadInt64(&b.Connections)
}

// Incr increments the connection count.
func (b *Backend) Incr() {
	atomic.AddInt64(&b.Connections, 1)
}

// Decr decrements the connection count.
func (b *Backend) Decr() {
	atomic.AddInt64(&b.Connections, -1)
}