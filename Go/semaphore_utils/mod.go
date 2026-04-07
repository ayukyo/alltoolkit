// Package semaphore_utils provides a semaphore implementation for Go
// with support for weighted semaphores, timeout operations, and context cancellation.
//
// A semaphore is a synchronization primitive that limits the number of concurrent
// operations. It's useful for rate limiting, connection pooling, and resource management.
//
// Example usage:
//
//	// Create a semaphore with capacity of 10
//	sem := semaphore_utils.New(10)
//
//	// Acquire a permit
//	if err := sem.Acquire(ctx); err != nil {
//	    // Handle error (context cancelled or timeout)
//	}
//
//	// Do work...
//
//	// Release the permit
//	sem.Release()
//
//	// Weighted semaphore example
//	weighted := semaphore_utils.NewWeighted(100)
//	if err := weighted.Acquire(ctx, 20); err != nil {
//	    // Handle error
//	}
//	// Do work that requires 20 units of resource...
//	weighted.Release(20)
//
// Features:
//   - Standard semaphore with fixed capacity
//   - Weighted semaphore for variable resource allocation
//   - Context-aware operations with cancellation support
//   - Timeout support for acquire operations
//   - Non-blocking try-acquire operations
//   - Thread-safe implementation
//   - Zero external dependencies (uses only Go standard library)
//
// @module semaphore_utils
// @version 1.0.0
// @license MIT
package semaphore_utils

import (
	"context"
	"errors"
	"sync"
	"time"
)

// ErrTimeout is returned when an acquire operation times out
var ErrTimeout = errors.New("semaphore acquire timeout")

// ErrCancelled is returned when the context is cancelled
var ErrCancelled = errors.New("semaphore acquire cancelled")

// Semaphore is a counting semaphore with context support.
// It limits the number of concurrent operations to a fixed capacity.
type Semaphore struct {
	capacity int
	current  int
	mu       sync.Mutex
	waiters  []chan struct{}
}

// New creates a new Semaphore with the given capacity.
//
// Parameters:
//   - capacity: maximum number of concurrent permits (must be > 0)
//
// Returns:
//   - *Semaphore: a new semaphore instance
//
// Example:
//
//	sem := semaphore_utils.New(10) // Allow up to 10 concurrent operations
func New(capacity int) *Semaphore {
	if capacity <= 0 {
		capacity = 1
	}
	return &Semaphore{
		capacity: capacity,
		current:  0,
		waiters:  make([]chan struct{}, 0),
	}
}

// Acquire acquires a permit from the semaphore, blocking until one is available
// or the context is cancelled.
//
// Parameters:
//   - ctx: context for cancellation support
//
// Returns:
//   - error: nil on success, ErrCancelled if context is cancelled
//
// Example:
//
//	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
//	defer cancel()
//
//	if err := sem.Acquire(ctx); err != nil {
//	    log.Printf("Failed to acquire: %v", err)
//	    return
//	}
//	defer sem.Release()
//	// Do work...
func (s *Semaphore) Acquire(ctx context.Context) error {
	s.mu.Lock()

	// Fast path: semaphore has available capacity
	if s.current < s.capacity {
		s.current++
		s.mu.Unlock()
		return nil
	}

	// Slow path: need to wait
	ch := make(chan struct{})
	s.waiters = append(s.waiters, ch)
	s.mu.Unlock()

	// Wait for signal or context cancellation
	select {
	case <-ch:
		return nil
	case <-ctx.Done():
		s.mu.Lock()
		// Remove ourselves from waiters
		for i, waiter := range s.waiters {
			if waiter == ch {
				s.waiters = append(s.waiters[:i], s.waiters[i+1:]...)
				break
			}
		}
		s.mu.Unlock()
		return ErrCancelled
	}
}

// AcquireTimeout acquires a permit with a timeout.
//
// Parameters:
//   - timeout: maximum time to wait for a permit
//
// Returns:
//   - error: nil on success, ErrTimeout if timeout exceeded
//
// Example:
//
//	if err := sem.AcquireTimeout(3 * time.Second); err != nil {
//	    log.Printf("Timeout waiting for permit: %v", err)
//	    return
//	}
//	defer sem.Release()
func (s *Semaphore) AcquireTimeout(timeout time.Duration) error {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	err := s.Acquire(ctx)
	if err == ErrCancelled {
		return ErrTimeout
	}
	return err
}

// TryAcquire attempts to acquire a permit without blocking.
//
// Returns:
//   - bool: true if permit acquired, false if semaphore is at capacity
//
// Example:
//
//	if !sem.TryAcquire() {
//	    log.Println("Semaphore is full, skipping work")
//	    return
//	}
//	defer sem.Release()
//	// Do work...
func (s *Semaphore) TryAcquire() bool {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.current < s.capacity {
		s.current++
		return true
	}
	return false
}

// Release releases a permit back to the semaphore.
//
// Example:
//
//	sem.Acquire(context.Background())
//	defer sem.Release()
//	// Do work...
func (s *Semaphore) Release() {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.current > 0 {
		s.current--

		// Notify next waiter if any
		if len(s.waiters) > 0 {
			ch := s.waiters[0]
			s.waiters = s.waiters[1:]
			close(ch)
		}
	}
}

// Available returns the number of available permits.
//
// Returns:
//   - int: number of permits currently available
func (s *Semaphore) Available() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.capacity - s.current
}

// Capacity returns the total capacity of the semaphore.
//
// Returns:
//   - int: total capacity (maximum permits)
func (s *Semaphore) Capacity() int {
	return s.capacity
}

// InUse returns the number of permits currently in use.
//
// Returns:
//   - int: number of acquired permits
func (s *Semaphore) InUse() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.current
}

// Waiters returns the number of goroutines waiting for a permit.
//
// Returns:
//   - int: number of waiting goroutines
func (s *Semaphore) Waiters() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return len(s.waiters)
}

// WeightedSemaphore is a weighted semaphore that allows acquiring
// multiple units at once. Useful when operations require different
// amounts of resources.
type WeightedSemaphore struct {
	capacity int64
	current  int64
	mu       sync.Mutex
	waiters  []weightedWaiter
}

type weightedWaiter struct {
	n   int64
	ch  chan struct{}
}

// NewWeighted creates a new WeightedSemaphore with the given capacity.
//
// Parameters:
//   - capacity: total weight capacity (must be > 0)
//
// Returns:
//   - *WeightedSemaphore: a new weighted semaphore instance
//
// Example:
//
//	// Create a semaphore with total capacity of 100 units
//	weighted := semaphore_utils.NewWeighted(100)
func NewWeighted(capacity int64) *WeightedSemaphore {
	if capacity <= 0 {
		capacity = 1
	}
	return &WeightedSemaphore{
		capacity: capacity,
		current:  0,
		waiters:  make([]weightedWaiter, 0),
	}
}

// Acquire acquires n units from the semaphore.
//
// Parameters:
//   - ctx: context for cancellation support
//   - n: number of units to acquire (must be > 0 and <= capacity)
//
// Returns:
//   - error: nil on success, ErrCancelled if context is cancelled
//
// Example:
//
//	// Acquire 20 units of resource
//	if err := weighted.Acquire(ctx, 20); err != nil {
//	    log.Printf("Failed to acquire: %v", err)
//	    return
//	}
//	defer weighted.Release(20)
func (w *WeightedSemaphore) Acquire(ctx context.Context, n int64) error {
	if n <= 0 {
		return errors.New("acquire count must be positive")
	}
	if n > w.capacity {
		return errors.New("acquire count exceeds capacity")
	}

	w.mu.Lock()

	// Fast path: enough capacity available
	if w.current+n <= w.capacity {
		w.current += n
		w.mu.Unlock()
		return nil
	}

	// Slow path: need to wait
	ch := make(chan struct{})
	w.waiters = append(w.waiters, weightedWaiter{n: n, ch: ch})
	w.mu.Unlock()

	// Wait for signal or context cancellation
	select {
	case <-ch:
		return nil
	case <-ctx.Done():
		w.mu.Lock()
		// Remove ourselves from waiters
		for i, waiter := range w.waiters {
			if waiter.ch == ch {
				w.waiters = append(w.waiters[:i], w.waiters[i+1:]...)
				break
			}
		}
		w.mu.Unlock()
		return ErrCancelled
	}
}

// AcquireTimeout acquires n units with a timeout.
//
// Parameters:
//   - timeout: maximum time to wait
//   - n: number of units to acquire
//
// Returns:
//   - error: nil on success, ErrTimeout if timeout exceeded
func (w *WeightedSemaphore) AcquireTimeout(timeout time.Duration, n int64) error {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	err := w.Acquire(ctx, n)
	if err == ErrCancelled {
		return ErrTimeout
	}
	return err
}

// TryAcquire attempts to acquire n units without blocking.
//
// Parameters:
//   - n: number of units to acquire
//
// Returns:
//   - bool: true if units acquired, false if not enough capacity
func (w *WeightedSemaphore) TryAcquire(n int64) bool {
	if n <= 0 || n > w.capacity {
		return false
	}

	w.mu.Lock()
	defer w.mu.Unlock()

	if w.current+n <= w.capacity {
		w.current += n
		return true
	}
	return false
}

// Release releases n units back to the semaphore.
//
// Parameters:
//   - n: number of units to release
func (w *WeightedSemaphore) Release(n int64) {
	if n <= 0 {
		return
	}

	w.mu.Lock()
	defer w.mu.Unlock()

	if w.current >= n {
		w.current -= n
	} else {
		w.current = 0
	}

	// Notify waiting goroutines if possible
	for len(w.waiters) > 0 {
		waiter := w.waiters[0]
		if w.current+waiter.n <= w.capacity {
			w.waiters = w.waiters[1:]
			w.current += waiter.n
			close(waiter.ch)
		} else {
			break
		}
	}
}

// Available returns the available capacity.
//
// Returns:
//   - int64: available units
func (w *WeightedSemaphore) Available() int64 {
	w.mu.Lock()
	defer w.mu.Unlock()
	return w.capacity - w.current
}

// Capacity returns the total capacity.
//
// Returns:
//   - int64: total capacity
func (w *WeightedSemaphore) Capacity() int64 {
	return w.capacity
}

// InUse returns the number of units currently in use.
//
// Returns:
//   - int64: units in use
func (w *WeightedSemaphore) InUse() int64 {
	w.mu.Lock()
	defer w.mu.Unlock()
	return w.current
}

// Waiters returns the number of waiting goroutines.
//
// Returns:
//   - int: number of waiters
func (w *WeightedSemaphore) Waiters() int {
	w.mu.Lock()
	defer w.mu.Unlock()
	return len(w.waiters)
}

// SemaphorePool is a pool of semaphores identified by keys.
// Useful for managing different resources with separate limits.
type SemaphorePool struct {
	semaphores map[string]*Semaphore
	capacity   int
	mu         sync.RWMutex
}

// NewPool creates a new SemaphorePool with the given default capacity for each semaphore.
//
// Parameters:
//   - defaultCapacity: default capacity for each semaphore in the pool
//
// Returns:
//   - *SemaphorePool: a new semaphore pool
func NewPool(defaultCapacity int) *SemaphorePool {
	return &SemaphorePool{
		semaphores: make(map[string]*Semaphore),
		capacity:   defaultCapacity,
	}
}

// Get returns the semaphore for the given key, creating it if necessary.
//
// Parameters:
//   - key: identifier for the semaphore
//
// Returns:
//   - *Semaphore: the semaphore for the key
func (p *SemaphorePool) Get(key string) *Semaphore {
	p.mu.RLock()
	if sem, ok := p.semaphores[key]; ok {
		p.mu.RUnlock()
		return sem
	}
	p.mu.RUnlock()

	p.mu.Lock()
	defer p.mu.Unlock()

	// Double-check after acquiring write lock
	if sem, ok := p.semaphores[key]; ok {
		return sem
	}

	sem := New(p.capacity)
	p.semaphores[key] = sem
	return sem
}

// Remove removes a semaphore from the pool.
//
// Parameters:
//   - key: identifier for the semaphore to remove
func (p *SemaphorePool) Remove(key string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	delete(p.semaphores, key)
}

// Keys returns all keys in the pool.
//
// Returns:
//   - []string: all semaphore keys
func (p *SemaphorePool) Keys() []string {
	p.mu.RLock()
	defer p.mu.RUnlock()

	keys := make([]string, 0, len(p.semaphores))
	for k := range p.semaphores {
		keys = append(keys, k)
	}
	return keys
}

// Size returns the number of semaphores in the pool.
//
// Returns:
//   - int: number of semaphores
func (p *SemaphorePool) Size() int {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return len(p.semaphores)
}

// RunWithSemaphore runs a function with a semaphore acquired.
// The semaphore is automatically released after the function completes.
//
// Parameters:
//   - ctx: context for cancellation
//   - sem: semaphore to use
//   - fn: function to run
//
// Returns:
//   - error: error from acquire or from the function
//
// Example:
//
//	err := semaphore_utils.RunWithSemaphore(ctx, sem, func() error {
//	    // Do work with semaphore held
//	    return doSomething()
//	})
func RunWithSemaphore(ctx context.Context, sem *Semaphore, fn func() error) error {
	if err := sem.Acquire(ctx); err != nil {
		return err
	}
	defer sem.Release()
	return fn()
}

// RunWithTimeout runs a function with a semaphore acquired and timeout.
//
// Parameters:
//   - timeout: maximum time to wait for semaphore
//   - sem: semaphore to use
//   - fn: function to run
//
// Returns:
//   - error: error from acquire timeout or from the function
func RunWithTimeout(timeout time.Duration, sem *Semaphore, fn func() error) error {
	if err := sem.AcquireTimeout(timeout); err != nil {
		return err
	}
	defer sem.Release()
	return fn()
}

// RunWeightedWithSemaphore runs a function with a weighted semaphore acquired.
//
// Parameters:
//   - ctx: context for cancellation
//   - sem: weighted semaphore to use
//   - n: number of units to acquire
//   - fn: function to run
//
// Returns:
//   - error: error from acquire or from the function
func RunWeightedWithSemaphore(ctx context.Context, sem *WeightedSemaphore, n int64, fn func() error) error {
	if err := sem.Acquire(ctx, n); err != nil {
		return err
	}
	defer sem.Release(n)
	return fn()
}

// BatchAcquire acquires permits for multiple operations at once.
// Either all permits are acquired or none (all-or-nothing).
//
// Parameters:
//   - ctx: context for cancellation
//   - semaphores: map of semaphores to number of permits needed
//
// Returns:
//   - func(): release function to call when done
//   - error: error if any acquire fails
//
// Example:
//
//	release, err := semaphore_utils.BatchAcquire(ctx, map[*semaphore_utils.WeightedSemaphore]int64{
//	    semA: 10,
//	    semB: 5,
//	})
//	if err != nil {
//	    return err
//	}
//	defer release()
//	// Do work with both semaphores held
func BatchAcquire(ctx context.Context, semaphores map[*WeightedSemaphore]int64) (func(), error) {
	type acquired struct {
		sem *WeightedSemaphore
		n   int64
	}

	var acquiredList []acquired

	for sem, n := range semaphores {
		if err := sem.Acquire(ctx, n); err != nil {
			// Release what we've acquired so far
			for _, a := range acquiredList {
				a.sem.Release(a.n)
			}
			return nil, err
		}
		acquiredList = append(acquiredList, acquired{sem: sem, n: n})
	}

	return func() {
		for _, a := range acquiredList {
			a.sem.Release(a.n)
		}
	}, nil
}
	