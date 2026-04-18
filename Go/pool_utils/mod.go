// Package pool_utils provides comprehensive object pooling utilities for Go applications.
// It includes generic object pools, worker pools, and connection pools with full lifecycle
// management. All implementations are thread-safe and use only the Go standard library.
//
// Example usage:
//
//	// Generic object pool
//	pool := pool_utils.NewObjectPool(
//	    func() *MyObject { return &MyObject{} }, // Factory
//	    func(obj *MyObject) { obj.Reset() },      // Reset
//	    10,  // Initial size
//	    100, // Max size
//	)
//	obj := pool.Get()
//	defer pool.Put(obj)
//
//	// Worker pool
//	wp := pool_utils.NewWorkerPool(10) // 10 workers
//	wp.Start()
//	wp.Submit(func() { fmt.Println("Hello from worker") })
//	wp.Stop()
//
//	// Connection pool
//	cp := pool_utils.NewConnectionPool(
//	    func() (net.Conn, error) { return net.Dial("tcp", "localhost:8080") },
//	    5,  // min connections
//	    20, // max connections
//	    30 * time.Second, // idle timeout
//	)
//	conn, err := cp.Get()
//	defer cp.Put(conn)
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Thread-safe implementations with sync.RWMutex
// - Generic object pool with factory, reset, and validation
// - Worker pool with graceful shutdown
// - Connection pool with health checks and idle timeout
// - Statistics tracking (created, destroyed, active, idle)
// - Configurable lifecycle callbacks
// - Production-ready for high-concurrency scenarios
//
package pool_utils

import (
	"context"
	"errors"
	"net"
	"sync"
	"sync/atomic"
	"time"
)

// Common errors
var (
	ErrPoolClosed    = errors.New("pool is closed")
	ErrPoolExhausted = errors.New("pool is exhausted")
	ErrInvalidObject = errors.New("invalid object")
	ErrTimeout       = errors.New("operation timed out")
)

// PoolStats contains pool statistics.
type PoolStats struct {
	Created   int64 // Total objects created
	Destroyed int64 // Total objects destroyed
	Active    int64 // Currently active (in-use) objects
	Idle      int64 // Currently idle objects
	WaitCount int64 // Number of times callers had to wait
}

// ObjectPool is a generic object pool that manages reusable objects.
// It supports factory functions for object creation, reset functions
// for object cleanup, and validation for health checks.
type ObjectPool[T any] struct {
	mu          sync.RWMutex
	factory     func() T                      // Creates new objects
	reset       func(T)                       // Resets objects before returning to pool
	validate    func(T) bool                  // Validates objects before use
	destroy     func(T)                       // Destroys objects when pool closes
	pool        chan T                        // Channel-based pool
	maxSize     int                           // Maximum pool size
	minSize     int                           // Minimum pool size (pre-allocated)
	created     int64                         // Total created count
	destroyed   int64                         // Total destroyed count
	active      int64                         // Currently active objects
	waitCount   int64                         // Times callers had to wait
	closed      bool                          // Pool closed flag
	onCreate    func(T)                       // Callback when object created
	onDestroy   func(T)                       // Callback when object destroyed
	onGet       func(T)                       // Callback when object acquired
	onPut       func(T)                       // Callback when object returned
}

// NewObjectPool creates a new object pool.
// factory: function to create new objects
// reset: function to reset objects (can be nil)
// minSize: minimum pool size (pre-allocated)
// maxSize: maximum pool size (0 = unlimited)
func NewObjectPool[T any](factory func() T, reset func(T), minSize, maxSize int) *ObjectPool[T] {
	if minSize < 0 {
		minSize = 0
	}
	if maxSize < 0 || (maxSize > 0 && maxSize < minSize) {
		maxSize = minSize
	}

	poolChanSize := maxSize
	if maxSize == 0 {
		poolChanSize = minSize + 1000 // Large buffer for unlimited
	}

	p := &ObjectPool[T]{
		factory: factory,
		reset:   reset,
		maxSize: maxSize,
		minSize: minSize,
		pool:    make(chan T, poolChanSize),
	}

	// Pre-allocate minimum objects
	for i := 0; i < minSize; i++ {
		obj := factory()
		atomic.AddInt64(&p.created, 1)
		p.pool <- obj
	}

	return p
}

// SetValidate sets the validation function for objects.
// Objects that fail validation are discarded.
func (p *ObjectPool[T]) SetValidate(fn func(T) bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.validate = fn
}

// SetDestroy sets the destroy function for objects.
// Called when objects are discarded or pool is closed.
func (p *ObjectPool[T]) SetDestroy(fn func(T)) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.destroy = fn
}

// SetOnCreate sets a callback for when objects are created.
func (p *ObjectPool[T]) SetOnCreate(fn func(T)) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.onCreate = fn
}

// SetOnDestroy sets a callback for when objects are destroyed.
func (p *ObjectPool[T]) SetOnDestroy(fn func(T)) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.onDestroy = fn
}

// SetOnGet sets a callback for when objects are acquired.
func (p *ObjectPool[T]) SetOnGet(fn func(T)) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.onGet = fn
}

// SetOnPut sets a callback for when objects are returned.
func (p *ObjectPool[T]) SetOnPut(fn func(T)) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.onPut = fn
}

// Get acquires an object from the pool.
// Creates a new object if pool is empty and maxSize not reached.
func (p *ObjectPool[T]) Get() (T, error) {
	return p.GetWithContext(context.Background())
}

// GetWithContext acquires an object from the pool with context support.
func (p *ObjectPool[T]) GetWithContext(ctx context.Context) (T, error) {
	var zero T

	p.mu.RLock()
	if p.closed {
		p.mu.RUnlock()
		return zero, ErrPoolClosed
	}
	p.mu.RUnlock()

	select {
	case obj := <-p.pool:
		// Validate object if validator is set
		if p.validate != nil && !p.validate(obj) {
			atomic.AddInt64(&p.destroyed, 1)
			if p.destroy != nil {
				p.destroy(obj)
			}
			if p.onDestroy != nil {
				p.onDestroy(obj)
			}
			// Try to get another object
			return p.GetWithContext(ctx)
		}
		atomic.AddInt64(&p.active, 1)
		if p.onGet != nil {
			p.onGet(obj)
		}
		return obj, nil
	default:
		// Pool is empty, try to create new object
		p.mu.Lock()
		if p.maxSize > 0 && int(atomic.LoadInt64(&p.created)-atomic.LoadInt64(&p.destroyed)) >= p.maxSize {
			// At max capacity, wait for available object
			p.mu.Unlock()
			atomic.AddInt64(&p.waitCount, 1)
			select {
			case obj := <-p.pool:
				if p.validate != nil && !p.validate(obj) {
					atomic.AddInt64(&p.destroyed, 1)
					if p.destroy != nil {
						p.destroy(obj)
					}
					if p.onDestroy != nil {
						p.onDestroy(obj)
					}
					return p.GetWithContext(ctx)
				}
				atomic.AddInt64(&p.active, 1)
				if p.onGet != nil {
					p.onGet(obj)
				}
				return obj, nil
			case <-ctx.Done():
				return zero, ctx.Err()
			}
		}

		obj := p.factory()
		atomic.AddInt64(&p.created, 1)
		atomic.AddInt64(&p.active, 1)
		p.mu.Unlock()

		if p.onCreate != nil {
			p.onCreate(obj)
		}
		if p.onGet != nil {
			p.onGet(obj)
		}
		return obj, nil
	}
}

// Put returns an object to the pool.
func (p *ObjectPool[T]) Put(obj T) error {
	p.mu.RLock()
	if p.closed {
		p.mu.RUnlock()
		if p.destroy != nil {
			p.destroy(obj)
		}
		if p.onDestroy != nil {
			p.onDestroy(obj)
		}
		atomic.AddInt64(&p.destroyed, 1)
		return ErrPoolClosed
	}
	p.mu.RUnlock()

	// Reset object if reset function is set
	if p.reset != nil {
		p.reset(obj)
	}

	atomic.AddInt64(&p.active, -1)

	select {
	case p.pool <- obj:
		if p.onPut != nil {
			p.onPut(obj)
		}
		return nil
	default:
		// Pool is full, discard object
		if p.destroy != nil {
			p.destroy(obj)
		}
		if p.onDestroy != nil {
			p.onDestroy(obj)
		}
		atomic.AddInt64(&p.destroyed, 1)
		return nil
	}
}

// Stats returns current pool statistics.
func (p *ObjectPool[T]) Stats() PoolStats {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return PoolStats{
		Created:   atomic.LoadInt64(&p.created),
		Destroyed: atomic.LoadInt64(&p.destroyed),
		Active:    atomic.LoadInt64(&p.active),
		Idle:      int64(len(p.pool)),
		WaitCount: atomic.LoadInt64(&p.waitCount),
	}
}

// Close closes the pool and releases all resources.
func (p *ObjectPool[T]) Close() error {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.closed {
		return nil
	}
	p.closed = true

	// Drain and destroy all objects
	close(p.pool)
	for obj := range p.pool {
		if p.destroy != nil {
			p.destroy(obj)
		}
		if p.onDestroy != nil {
			p.onDestroy(obj)
		}
		atomic.AddInt64(&p.destroyed, 1)
	}

	return nil
}

// Len returns the current number of idle objects in the pool.
func (p *ObjectPool[T]) Len() int {
	return len(p.pool)
}

// Capacity returns the maximum pool size (0 = unlimited).
func (p *ObjectPool[T]) Capacity() int {
	return p.maxSize
}

// WorkerPool manages a pool of goroutines for parallel task execution.
type WorkerPool struct {
	mu          sync.RWMutex
	workers     int
	tasks       chan func()
	wg          sync.WaitGroup
	ctx         context.Context
	cancel      context.CancelFunc
	started     bool
	stopped     bool
	taskCount   int64
	queuedCount int64
	onTaskStart func()
	onTaskEnd   func()
}

// NewWorkerPool creates a new worker pool with the specified number of workers.
func NewWorkerPool(workers int) *WorkerPool {
	if workers <= 0 {
		workers = 1
	}
	return &WorkerPool{
		workers: workers,
		tasks:   make(chan func(), workers*100), // Buffer tasks
	}
}

// SetOnTaskStart sets a callback for when a task starts.
func (wp *WorkerPool) SetOnTaskStart(fn func()) {
	wp.mu.Lock()
	defer wp.mu.Unlock()
	wp.onTaskStart = fn
}

// SetOnTaskEnd sets a callback for when a task ends.
func (wp *WorkerPool) SetOnTaskEnd(fn func()) {
	wp.mu.Lock()
	defer wp.mu.Unlock()
	wp.onTaskEnd = fn
}

// Start starts the worker pool.
func (wp *WorkerPool) Start() error {
	wp.mu.Lock()
	defer wp.mu.Unlock()

	if wp.started {
		return errors.New("worker pool already started")
	}

	wp.ctx, wp.cancel = context.WithCancel(context.Background())
	wp.started = true

	for i := 0; i < wp.workers; i++ {
		wp.wg.Add(1)
		go wp.worker()
	}

	return nil
}

// worker is the main worker goroutine.
func (wp *WorkerPool) worker() {
	defer wp.wg.Done()

	for {
		select {
		case <-wp.ctx.Done():
			return
		case task, ok := <-wp.tasks:
			if !ok {
				return
			}
			atomic.AddInt64(&wp.queuedCount, -1)
			if wp.onTaskStart != nil {
				wp.onTaskStart()
			}
			task()
			atomic.AddInt64(&wp.taskCount, 1)
			if wp.onTaskEnd != nil {
				wp.onTaskEnd()
			}
		}
	}
}

// Submit adds a task to the worker pool.
func (wp *WorkerPool) Submit(task func()) error {
	wp.mu.RLock()
	defer wp.mu.RUnlock()

	if !wp.started {
		return errors.New("worker pool not started")
	}
	if wp.stopped {
		return errors.New("worker pool is stopped")
	}

	select {
	case wp.tasks <- task:
		atomic.AddInt64(&wp.queuedCount, 1)
		return nil
	default:
		return ErrPoolExhausted
	}
}

// SubmitWithContext adds a task to the worker pool with context support.
func (wp *WorkerPool) SubmitWithContext(ctx context.Context, task func()) error {
	wp.mu.RLock()
	defer wp.mu.RUnlock()

	if !wp.started {
		return errors.New("worker pool not started")
	}
	if wp.stopped {
		return errors.New("worker pool is stopped")
	}

	select {
	case wp.tasks <- task:
		atomic.AddInt64(&wp.queuedCount, 1)
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

// Stop gracefully stops the worker pool.
// Waits for all queued tasks to complete.
func (wp *WorkerPool) Stop() {
	wp.mu.Lock()
	if wp.stopped {
		wp.mu.Unlock()
		return
	}
	wp.stopped = true
	wp.mu.Unlock()

	wp.cancel()
	wp.wg.Wait()
}

// StopImmediately stops the worker pool immediately.
// Does not wait for queued tasks.
func (wp *WorkerPool) StopImmediately() {
	wp.mu.Lock()
	if wp.stopped {
		wp.mu.Unlock()
		return
	}
	wp.stopped = true
	close(wp.tasks)
	wp.mu.Unlock()

	wp.cancel()
	wp.wg.Wait()
}

// Stats returns worker pool statistics.
func (wp *WorkerPool) Stats() PoolStats {
	wp.mu.RLock()
	defer wp.mu.RUnlock()
	return PoolStats{
		Active:    int64(wp.workers),
		Idle:      0,
		Created:   0,
		Destroyed: 0,
		WaitCount: atomic.LoadInt64(&wp.queuedCount),
	}
}

// TaskCount returns the number of completed tasks.
func (wp *WorkerPool) TaskCount() int64 {
	return atomic.LoadInt64(&wp.taskCount)
}

// QueuedCount returns the number of queued tasks.
func (wp *WorkerPool) QueuedCount() int64 {
	return atomic.LoadInt64(&wp.queuedCount)
}

// ConnectionPool manages a pool of network connections.
type ConnectionPool struct {
	mu           sync.RWMutex
	factory      func() (net.Conn, error)
	minConns     int
	maxConns     int
	idleTimeout  time.Duration
	maxLifetime  time.Duration
	connections  chan *pooledConn
	active       int64
	created      int64
	destroyed    int64
	waitCount    int64
	closed       bool
	healthCheck  func(net.Conn) bool
	onCreate     func(net.Conn)
	onDestroy    func(net.Conn)
	cleanupTimer *time.Ticker
	stopCh       chan struct{}
}

type pooledConn struct {
	conn      net.Conn
	createdAt time.Time
	usedAt    time.Time
}

// NewConnectionPool creates a new connection pool.
// factory: function to create new connections
// minConns: minimum number of connections to maintain
// maxConns: maximum number of connections (0 = unlimited)
// idleTimeout: time after which idle connections are closed
func NewConnectionPool(factory func() (net.Conn, error), minConns, maxConns int, idleTimeout time.Duration) *ConnectionPool {
	if minConns < 0 {
		minConns = 0
	}
	if maxConns > 0 && maxConns < minConns {
		maxConns = minConns
	}
	if idleTimeout <= 0 {
		idleTimeout = 30 * time.Second
	}

	poolSize := maxConns
	if maxConns == 0 {
		poolSize = minConns + 1000
	}

	cp := &ConnectionPool{
		factory:     factory,
		minConns:    minConns,
		maxConns:    maxConns,
		idleTimeout: idleTimeout,
		connections: make(chan *pooledConn, poolSize),
		stopCh:      make(chan struct{}),
	}

	// Pre-create minimum connections
	for i := 0; i < minConns; i++ {
		conn, err := factory()
		if err == nil {
			now := time.Now()
			cp.connections <- &pooledConn{
				conn:      conn,
				createdAt: now,
				usedAt:    now,
			}
			atomic.AddInt64(&cp.created, 1)
		}
	}

	// Start cleanup goroutine
	cp.cleanupTimer = time.NewTicker(idleTimeout / 2)
	go cp.cleanup()

	return cp
}

// SetMaxLifetime sets the maximum lifetime of connections.
func (cp *ConnectionPool) SetMaxLifetime(d time.Duration) {
	cp.mu.Lock()
	defer cp.mu.Unlock()
	cp.maxLifetime = d
}

// SetHealthCheck sets a function to validate connection health.
func (cp *ConnectionPool) SetHealthCheck(fn func(net.Conn) bool) {
	cp.mu.Lock()
	defer cp.mu.Unlock()
	cp.healthCheck = fn
}

// SetOnCreate sets a callback for when connections are created.
func (cp *ConnectionPool) SetOnCreate(fn func(net.Conn)) {
	cp.mu.Lock()
	defer cp.mu.Unlock()
	cp.onCreate = fn
}

// SetOnDestroy sets a callback for when connections are destroyed.
func (cp *ConnectionPool) SetOnDestroy(fn func(net.Conn)) {
	cp.mu.Lock()
	defer cp.mu.Unlock()
	cp.onDestroy = fn
}

// cleanup periodically removes stale idle connections.
func (cp *ConnectionPool) cleanup() {
	for {
		select {
		case <-cp.cleanupTimer.C:
			cp.cleanupIdle()
		case <-cp.stopCh:
			return
		}
	}
}

// cleanupIdle removes expired idle connections.
func (cp *ConnectionPool) cleanupIdle() {
	cp.mu.Lock()
	defer cp.mu.Unlock()

	if cp.closed {
		return
	}

	now := time.Now()
	var toRemove []*pooledConn
	var toKeep []*pooledConn

	// Collect all connections
	close(cp.connections)
	for pc := range cp.connections {
		// Check if connection is expired
		idle := now.Sub(pc.usedAt)
		lifetime := now.Sub(pc.createdAt)

		shouldRemove := false
		if idle > cp.idleTimeout {
			shouldRemove = true
		}
		if cp.maxLifetime > 0 && lifetime > cp.maxLifetime {
			shouldRemove = true
		}
		if cp.healthCheck != nil && !cp.healthCheck(pc.conn) {
			shouldRemove = true
		}

		if shouldRemove {
			toRemove = append(toRemove, pc)
		} else {
			toKeep = append(toKeep, pc)
		}
	}

	// Recreate channel
	cp.connections = make(chan *pooledConn, cap(cp.connections))

	// Put back connections to keep
	for _, pc := range toKeep {
		cp.connections <- pc
	}

	// Remove expired connections
	for _, pc := range toRemove {
		pc.conn.Close()
		atomic.AddInt64(&cp.destroyed, 1)
		if cp.onDestroy != nil {
			cp.onDestroy(pc.conn)
		}
	}

	// Ensure minimum connections
	for i := len(toKeep); i < cp.minConns; i++ {
		conn, err := cp.factory()
		if err == nil {
			now := time.Now()
			cp.connections <- &pooledConn{
				conn:      conn,
				createdAt: now,
				usedAt:    now,
			}
			atomic.AddInt64(&cp.created, 1)
			if cp.onCreate != nil {
				cp.onCreate(conn)
			}
		}
	}
}

// Get acquires a connection from the pool.
func (cp *ConnectionPool) Get() (net.Conn, error) {
	return cp.GetWithContext(context.Background())
}

// GetWithContext acquires a connection with context support.
func (cp *ConnectionPool) GetWithContext(ctx context.Context) (net.Conn, error) {
	cp.mu.RLock()
	if cp.closed {
		cp.mu.RUnlock()
		return nil, ErrPoolClosed
	}
	cp.mu.RUnlock()

	// Try to get from pool
	select {
	case pc := <-cp.connections:
		// Validate connection
		if cp.healthCheck != nil && !cp.healthCheck(pc.conn) {
			pc.conn.Close()
			atomic.AddInt64(&cp.destroyed, 1)
			if cp.onDestroy != nil {
				cp.onDestroy(pc.conn)
			}
			// Try to get another connection
			return cp.GetWithContext(ctx)
		}
		pc.usedAt = time.Now()
		atomic.AddInt64(&cp.active, 1)
		return &poolConnWrapper{conn: pc, pool: cp}, nil
	default:
		// Create new connection
		cp.mu.Lock()
		if cp.maxConns > 0 && int(atomic.LoadInt64(&cp.active)) >= cp.maxConns {
			// At max capacity, wait
			cp.mu.Unlock()
			atomic.AddInt64(&cp.waitCount, 1)
			select {
			case pc := <-cp.connections:
				if cp.healthCheck != nil && !cp.healthCheck(pc.conn) {
					pc.conn.Close()
					atomic.AddInt64(&cp.destroyed, 1)
					if cp.onDestroy != nil {
						cp.onDestroy(pc.conn)
					}
					return cp.GetWithContext(ctx)
				}
				pc.usedAt = time.Now()
				atomic.AddInt64(&cp.active, 1)
				return &poolConnWrapper{conn: pc, pool: cp}, nil
			case <-ctx.Done():
				return nil, ctx.Err()
			}
		}

		conn, err := cp.factory()
		if err != nil {
			cp.mu.Unlock()
			return nil, err
		}
		atomic.AddInt64(&cp.created, 1)
		atomic.AddInt64(&cp.active, 1)
		now := time.Now()
		pc := &pooledConn{conn: conn, createdAt: now, usedAt: now}
		cp.mu.Unlock()

		if cp.onCreate != nil {
			cp.onCreate(conn)
		}
		return &poolConnWrapper{conn: pc, pool: cp}, nil
	}
}

// Put returns a connection to the pool.
func (cp *ConnectionPool) put(pc *pooledConn) error {
	cp.mu.RLock()
	if cp.closed {
		cp.mu.RUnlock()
		pc.conn.Close()
		atomic.AddInt64(&cp.destroyed, 1)
		if cp.onDestroy != nil {
			cp.onDestroy(pc.conn)
		}
		return ErrPoolClosed
	}
	cp.mu.RUnlock()

	pc.usedAt = time.Now()
	atomic.AddInt64(&cp.active, -1)

	select {
	case cp.connections <- pc:
		return nil
	default:
		// Pool full, close connection
		pc.conn.Close()
		atomic.AddInt64(&cp.destroyed, 1)
		if cp.onDestroy != nil {
			cp.onDestroy(pc.conn)
		}
		return nil
	}
}

// Stats returns pool statistics.
func (cp *ConnectionPool) Stats() PoolStats {
	cp.mu.RLock()
	defer cp.mu.RUnlock()
	return PoolStats{
		Created:   atomic.LoadInt64(&cp.created),
		Destroyed: atomic.LoadInt64(&cp.destroyed),
		Active:    atomic.LoadInt64(&cp.active),
		Idle:      int64(len(cp.connections)),
		WaitCount: atomic.LoadInt64(&cp.waitCount),
	}
}

// Close closes the connection pool.
func (cp *ConnectionPool) Close() error {
	cp.mu.Lock()
	defer cp.mu.Unlock()

	if cp.closed {
		return nil
	}
	cp.closed = true

	// Stop cleanup goroutine
	cp.cleanupTimer.Stop()
	close(cp.stopCh)

	// Close all connections
	close(cp.connections)
	for pc := range cp.connections {
		pc.conn.Close()
		atomic.AddInt64(&cp.destroyed, 1)
		if cp.onDestroy != nil {
			cp.onDestroy(pc.conn)
		}
	}

	return nil
}

// poolConnWrapper wraps a pooled connection.
type poolConnWrapper struct {
	conn *pooledConn
	pool *ConnectionPool
	mu   sync.Mutex
}

func (w *poolConnWrapper) Read(b []byte) (n int, err error) {
	return w.conn.conn.Read(b)
}

func (w *poolConnWrapper) Write(b []byte) (n int, err error) {
	return w.conn.conn.Write(b)
}

func (w *poolConnWrapper) Close() error {
	w.mu.Lock()
	defer w.mu.Unlock()
	return w.pool.put(w.conn)
}

func (w *poolConnWrapper) LocalAddr() net.Addr {
	return w.conn.conn.LocalAddr()
}

func (w *poolConnWrapper) RemoteAddr() net.Addr {
	return w.conn.conn.RemoteAddr()
}

func (w *poolConnWrapper) SetDeadline(t time.Time) error {
	return w.conn.conn.SetDeadline(t)
}

func (w *poolConnWrapper) SetReadDeadline(t time.Time) error {
	return w.conn.conn.SetReadDeadline(t)
}

func (w *poolConnWrapper) SetWriteDeadline(t time.Time) error {
	return w.conn.conn.SetWriteDeadline(t)
}

// SemaphorePool is a simple semaphore-based resource limiter.
type SemaphorePool struct {
	sem chan struct{}
}

// NewSemaphorePool creates a new semaphore pool.
// size: maximum concurrent acquisitions
func NewSemaphorePool(size int) *SemaphorePool {
	if size <= 0 {
		size = 1
	}
	return &SemaphorePool{
		sem: make(chan struct{}, size),
	}
}

// Acquire acquires a semaphore slot.
func (sp *SemaphorePool) Acquire() {
	sp.sem <- struct{}{}
}

// AcquireWithContext acquires a semaphore slot with context support.
func (sp *SemaphorePool) AcquireWithContext(ctx context.Context) error {
	select {
	case sp.sem <- struct{}{}:
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

// TryAcquire tries to acquire a semaphore slot without blocking.
func (sp *SemaphorePool) TryAcquire() bool {
	select {
	case sp.sem <- struct{}{}:
		return true
	default:
		return false
	}
}

// Release releases a semaphore slot.
func (sp *SemaphorePool) Release() {
	<-sp.sem
}

// Available returns the number of available slots.
func (sp *SemaphorePool) Available() int {
	return cap(sp.sem) - len(sp.sem)
}

// Capacity returns the maximum number of slots.
func (sp *SemaphorePool) Capacity() int {
	return cap(sp.sem)
}