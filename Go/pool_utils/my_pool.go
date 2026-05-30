// Package pool_utils provides a generic object pool with TTL, lazy creation,
// and concurrency-safe operations.
//
// Features:
//   - Generic object pool for any type
//   - TTL (Time-To-Live) support for pooled objects
//   - Lazy creation via factory function
//   - Eviction when pool is full
//   - Thread-safe operations
//   - Zero external dependencies
//
// Example usage:
//
//     pool := pool.New(func() interface{} { return &bytes.Buffer{} }, 100)
//
//     obj := pool.Get()
//     defer pool.Put(obj)
//
//     buf := obj.(*bytes.Buffer)
//     buf.Reset()
//     buf.WriteString("hello")
//
package pool_utils

import (
	"sync"
	"time"
)

// pooledObject wraps an object with its creation timestamp for TTL tracking.
type pooledObject struct {
	obj      interface{}
	deadline time.Time
}

// Pool manages a pool of reusable objects.
type Pool struct {
	factory     func() interface{}
	maxSize     int
	ttl         time.Duration
	mu          sync.Mutex
	available   []pooledObject
	activeCount int
	created     int
}

// New creates a new Pool with the given factory and max size.
// The ttl parameter specifies how long an object can be kept in the pool
// before it is considered stale and discarded (0 = no expiration).
func New(factory func() interface{}, maxSize int, ttl time.Duration) *Pool {
	return &Pool{
		factory:   factory,
		maxSize:   maxSize,
		ttl:       ttl,
		available: make([]pooledObject, 0),
	}
}

// Get retrieves an object from the pool, creating one if needed.
func (p *Pool) Get() interface{} {
	p.mu.Lock()
	defer p.mu.Unlock()

	now := time.Now()
	for len(p.available) > 0 {
		last := len(p.available) - 1
		po := p.available[last]
		p.available = p.available[:last]

		if p.ttl > 0 && now.Sub(po.deadline) > 0 {
			// Object has expired, skip it
			continue
		}

		p.activeCount++
		return po.obj
	}

	// No available object, create new one
	p.created++
	obj := p.factory()
	p.activeCount++
	return obj
}

// Put returns an object to the pool for reuse.
func (p *Pool) Put(obj interface{}) {
	if obj == nil {
		return
	}

	p.mu.Lock()
	defer p.mu.Unlock()

	if p.activeCount <= 0 {
		return
	}
	p.activeCount--

	if len(p.available) < p.maxSize {
		deadline := time.Time{}
		if p.ttl > 0 {
			deadline = time.Now().Add(p.ttl)
		}
		p.available = append(p.available, pooledObject{obj: obj, deadline: deadline})
	}
	// If pool is full, the object is simply discarded
}

// Stats returns current pool statistics.
func (p *Pool) Stats() (available int, active int, created int) {
	p.mu.Lock()
	defer p.mu.Unlock()
	return len(p.available), p.activeCount, p.created
}

// Close clears the pool and releases all resources.
func (p *Pool) Close() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.available = p.available[:0]
	p.activeCount = 0
	p.created = 0
}

// ResetStats resets the created count.
func (p *Pool) ResetStats() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.created = 0
}

// Purge removes all expired objects from the pool.
// This is useful for periodic maintenance of TTL-enabled pools.
func (p *Pool) Purge() {
	if p.ttl <= 0 {
		return
	}

	p.mu.Lock()
	defer p.mu.Unlock()

	now := time.Now()
	kept := make([]pooledObject, 0, len(p.available))
	for _, po := range p.available {
		if now.Sub(po.deadline) <= 0 {
			kept = append(kept, po)
		}
	}
	p.available = kept
}
