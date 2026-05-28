// Package semaphore_utils 提供信号量并发控制工具
// 支持加权信号量、超时获取、公平调度等特性
package semaphore_utils

import (
	"context"
	"errors"
	"sync"
	"sync/atomic"
	"time"
)

var (
	ErrSemaphoreClosed  = errors.New("semaphore is closed")
	ErrInvalidWeight    = errors.New("weight must be positive")
	ErrExceedsCapacity  = errors.New("weight exceeds semaphore capacity")
	ErrNegativeCapacity = errors.New("capacity must be positive")
	ErrContextCanceled  = errors.New("context canceled")
)

// Semaphore 信号量接口
type Semaphore interface {
	// Acquire 获取指定权重的信号量
	Acquire(ctx context.Context, weight int64) error

	// TryAcquire 尝试获取信号量，不阻塞
	TryAcquire(weight int64) bool

	// TryAcquireWithTimeout 尝试在超时时间内获取信号量
	TryAcquireWithTimeout(weight int64, timeout time.Duration) bool

	// Release 释放指定权重的信号量
	Release(weight int64)

	// Available 返回当前可用的信号量数量
	Available() int64

	// Capacity 返回信号量的总容量
	Capacity() int64

	// Waiters 返回当前等待的数量
	Waiters() int32

	// Close 关闭信号量，释放所有等待者
	Close()

	// IsClosed 返回信号量是否已关闭
	IsClosed() bool
}

// semaphore 基础信号量实现
type semaphore struct {
	capacity  int64
	available int64
	waiters   int32
	closed    int32
	mu        sync.Mutex
	notify    chan struct{}
}

// NewSemaphore 创建一个新的信号量
func NewSemaphore(capacity int64) (Semaphore, error) {
	if capacity <= 0 {
		return nil, ErrNegativeCapacity
	}

	s := &semaphore{
		capacity:  capacity,
		available: capacity,
		notify:    make(chan struct{}, 1),
	}
	return s, nil
}

// Acquire 获取指定权重的信号量
func (s *semaphore) Acquire(ctx context.Context, weight int64) error {
	if weight <= 0 {
		return ErrInvalidWeight
	}
	if weight > s.capacity {
		return ErrExceedsCapacity
	}
	if atomic.LoadInt32(&s.closed) == 1 {
		return ErrSemaphoreClosed
	}

	atomic.AddInt32(&s.waiters, 1)
	defer atomic.AddInt32(&s.waiters, -1)

	for {
		s.mu.Lock()
		if s.available >= weight {
			s.available -= weight
			s.mu.Unlock()
			return nil
		}
		s.mu.Unlock()

		select {
		case <-ctx.Done():
			return ErrContextCanceled
		case <-s.notify:
			if atomic.LoadInt32(&s.closed) == 1 {
				return ErrSemaphoreClosed
			}
		}
	}
}

// TryAcquire 尝试获取信号量，不阻塞
func (s *semaphore) TryAcquire(weight int64) bool {
	if weight <= 0 || weight > s.capacity {
		return false
	}
	if atomic.LoadInt32(&s.closed) == 1 {
		return false
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	if s.available >= weight {
		s.available -= weight
		return true
	}
	return false
}

// TryAcquireWithTimeout 尝试在超时时间内获取信号量
func (s *semaphore) TryAcquireWithTimeout(weight int64, timeout time.Duration) bool {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	return s.Acquire(ctx, weight) == nil
}

// Release 释放指定权重的信号量
func (s *semaphore) Release(weight int64) {
	if weight <= 0 {
		return
	}

	s.mu.Lock()
	s.available += weight
	if s.available > s.capacity {
		s.available = s.capacity
	}
	s.mu.Unlock()

	// 通知等待者
	select {
	case s.notify <- struct{}{}:
	default:
	}
}

// Available 返回当前可用的信号量数量
func (s *semaphore) Available() int64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.available
}

// Capacity 返回信号量的总容量
func (s *semaphore) Capacity() int64 {
	return s.capacity
}

// Waiters 返回当前等待的数量
func (s *semaphore) Waiters() int32 {
	return atomic.LoadInt32(&s.waiters)
}

// Close 关闭信号量，释放所有等待者
func (s *semaphore) Close() {
	atomic.StoreInt32(&s.closed, 1)
	// 通知所有等待者
	close(s.notify)
}

// IsClosed 返回信号量是否已关闭
func (s *semaphore) IsClosed() bool {
	return atomic.LoadInt32(&s.closed) == 1
}

// ============================================
// 加权信号量（支持优先级队列）
// ============================================

// PrioritySemaphore 支持优先级的加权信号量
type PrioritySemaphore struct {
	capacity  int64
	available int64
	closed    int32
	mu        sync.Mutex

	// 优先级队列（优先级越高，值越小）
	pq priorityQueue
}

type waiter struct {
	priority int
	weight   int64
	ch       chan error
}

type priorityQueue []*waiter

func (pq priorityQueue) Len() int { return len(pq) }
func (pq priorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}
func (pq priorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }

func (pq *priorityQueue) Push(w *waiter) {
	*pq = append(*pq, w)
	// 简单插入排序保持优先级
	for i := len(*pq) - 1; i > 0; i-- {
		if (*pq)[i].priority < (*pq)[i-1].priority {
			(*pq)[i], (*pq)[i-1] = (*pq)[i-1], (*pq)[i]
		} else {
			break
		}
	}
}

func (pq *priorityQueue) Pop() *waiter {
	if len(*pq) == 0 {
		return nil
	}
	w := (*pq)[0]
	*pq = (*pq)[1:]
	return w
}

// NewPrioritySemaphore 创建支持优先级的信号量
func NewPrioritySemaphore(capacity int64) (*PrioritySemaphore, error) {
	if capacity <= 0 {
		return nil, ErrNegativeCapacity
	}

	ps := &PrioritySemaphore{
		capacity:  capacity,
		available: capacity,
	}
	return ps, nil
}

// AcquireWithPriority 按优先级获取信号量
func (ps *PrioritySemaphore) AcquireWithPriority(ctx context.Context, weight int64, priority int) error {
	if weight <= 0 {
		return ErrInvalidWeight
	}
	if weight > ps.capacity {
		return ErrExceedsCapacity
	}
	if atomic.LoadInt32(&ps.closed) == 1 {
		return ErrSemaphoreClosed
	}

	w := &waiter{
		priority: priority,
		weight:   weight,
		ch:       make(chan error, 1),
	}

	ps.mu.Lock()

	// 如果可用且队列为空，直接获取
	if ps.available >= weight && len(ps.pq) == 0 {
		ps.available -= weight
		ps.mu.Unlock()
		return nil
	}

	// 加入等待队列
	ps.pq.Push(w)
	ps.mu.Unlock()

	select {
	case err := <-w.ch:
		return err
	case <-ctx.Done():
		ps.mu.Lock()
		// 从队列中移除
		for i, item := range ps.pq {
			if item == w {
				ps.pq = append(ps.pq[:i], ps.pq[i+1:]...)
				break
			}
		}
		ps.mu.Unlock()
		return ErrContextCanceled
	}
}

// Release 释放信号量
func (ps *PrioritySemaphore) Release(weight int64) {
	if weight <= 0 {
		return
	}

	ps.mu.Lock()
	defer ps.mu.Unlock()

	ps.available += weight
	if ps.available > ps.capacity {
		ps.available = ps.capacity
	}

	// 尝试唤醒等待者
	for len(ps.pq) > 0 && ps.available >= ps.pq[0].weight {
		w := ps.pq.Pop()
		ps.available -= w.weight
		w.ch <- nil
	}
}

// Available 返回当前可用的信号量数量
func (ps *PrioritySemaphore) Available() int64 {
	ps.mu.Lock()
	defer ps.mu.Unlock()
	return ps.available
}

// Capacity 返回信号量的总容量
func (ps *PrioritySemaphore) Capacity() int64 {
	return ps.capacity
}

// Close 关闭信号量
func (ps *PrioritySemaphore) Close() {
	atomic.StoreInt32(&ps.closed, 1)
	ps.mu.Lock()
	defer ps.mu.Unlock()

	// 通知所有等待者
	for _, w := range ps.pq {
		w.ch <- ErrSemaphoreClosed
	}
	ps.pq = nil
}

// IsClosed 返回信号量是否已关闭
func (ps *PrioritySemaphore) IsClosed() bool {
	return atomic.LoadInt32(&ps.closed) == 1
}

// ============================================
// 读写信号量（支持读写锁语义）
// ============================================

// RWSemaphore 读写信号量
type RWSemaphore struct {
	capacity    int64
	readers     int64
	writeLocked int32
	mu          sync.Mutex
	notify      chan struct{}
	closed      int32
}

// NewRWSemaphore 创建读写信号量
func NewRWSemaphore(capacity int64) (*RWSemaphore, error) {
	if capacity <= 0 {
		return nil, ErrNegativeCapacity
	}

	rw := &RWSemaphore{
		capacity: capacity,
		notify:   make(chan struct{}, 1),
	}
	return rw, nil
}

// AcquireRead 获取读锁
func (rw *RWSemaphore) AcquireRead(ctx context.Context) error {
	if atomic.LoadInt32(&rw.closed) == 1 {
		return ErrSemaphoreClosed
	}

	for {
		rw.mu.Lock()
		if atomic.LoadInt32(&rw.writeLocked) == 0 {
			rw.readers++
			rw.mu.Unlock()
			return nil
		}
		rw.mu.Unlock()

		select {
		case <-ctx.Done():
			return ErrContextCanceled
		case <-rw.notify:
			if atomic.LoadInt32(&rw.closed) == 1 {
				return ErrSemaphoreClosed
			}
		}
	}
}

// ReleaseRead 释放读锁
func (rw *RWSemaphore) ReleaseRead() {
	rw.mu.Lock()
	rw.readers--
	if rw.readers < 0 {
		rw.readers = 0
	}
	rw.mu.Unlock()

	// 通知等待者
	select {
	case rw.notify <- struct{}{}:
	default:
	}
}

// AcquireWrite 获取写锁
func (rw *RWSemaphore) AcquireWrite(ctx context.Context) error {
	if atomic.LoadInt32(&rw.closed) == 1 {
		return ErrSemaphoreClosed
	}

	for {
		rw.mu.Lock()
		if rw.readers == 0 && atomic.LoadInt32(&rw.writeLocked) == 0 {
			atomic.StoreInt32(&rw.writeLocked, 1)
			rw.mu.Unlock()
			return nil
		}
		rw.mu.Unlock()

		select {
		case <-ctx.Done():
			return ErrContextCanceled
		case <-rw.notify:
			if atomic.LoadInt32(&rw.closed) == 1 {
				return ErrSemaphoreClosed
			}
		}
	}
}

// ReleaseWrite 释放写锁
func (rw *RWSemaphore) ReleaseWrite() {
	atomic.StoreInt32(&rw.writeLocked, 0)
	// 通知所有等待者
	select {
	case rw.notify <- struct{}{}:
	default:
	}
}

// Close 关闭信号量
func (rw *RWSemaphore) Close() {
	atomic.StoreInt32(&rw.closed, 1)
	close(rw.notify)
}

// IsClosed 返回是否已关闭
func (rw *RWSemaphore) IsClosed() bool {
	return atomic.LoadInt32(&rw.closed) == 1
}

// ============================================
// 信号量池
// ============================================

// SemaphorePool 信号量池
type SemaphorePool struct {
	semaphores map[string]Semaphore
	mu         sync.RWMutex
}

// NewSemaphorePool 创建信号量池
func NewSemaphorePool() *SemaphorePool {
	return &SemaphorePool{
		semaphores: make(map[string]Semaphore),
	}
}

// GetOrCreate 获取或创建信号量
func (p *SemaphorePool) GetOrCreate(name string, capacity int64) (Semaphore, error) {
	p.mu.RLock()
	if s, ok := p.semaphores[name]; ok {
		p.mu.RUnlock()
		return s, nil
	}
	p.mu.RUnlock()

	p.mu.Lock()
	defer p.mu.Unlock()

	if s, ok := p.semaphores[name]; ok {
		return s, nil
	}

	s, err := NewSemaphore(capacity)
	if err != nil {
		return nil, err
	}

	p.semaphores[name] = s
	return s, nil
}

// Get 获取信号量
func (p *SemaphorePool) Get(name string) Semaphore {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.semaphores[name]
}

// Remove 移除信号量
func (p *SemaphorePool) Remove(name string) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if s, ok := p.semaphores[name]; ok {
		s.Close()
		delete(p.semaphores, name)
	}
}

// CloseAll 关闭所有信号量
func (p *SemaphorePool) CloseAll() {
	p.mu.Lock()
	defer p.mu.Unlock()

	for _, s := range p.semaphores {
		s.Close()
	}
	p.semaphores = make(map[string]Semaphore)
}

// Names 返回所有信号量名称
func (p *SemaphorePool) Names() []string {
	p.mu.RLock()
	defer p.mu.RUnlock()

	names := make([]string, 0, len(p.semaphores))
	for name := range p.semaphores {
		names = append(names, name)
	}
	return names
}

// ============================================
// 限流器
// ============================================

// RateLimiter 简单的令牌桶限流器
type RateLimiter struct {
	capacity   int64
	available  int64
	refillRate int64 // 每秒补充的数量
	lastRefill time.Time
	mu         sync.Mutex
}

// NewRateLimiter 创建限流器
// capacity: 最大容量
// refillRate: 每秒补充的数量
func NewRateLimiter(capacity, refillRate int64) (*RateLimiter, error) {
	if capacity <= 0 || refillRate <= 0 {
		return nil, ErrNegativeCapacity
	}

	return &RateLimiter{
		capacity:   capacity,
		available:  capacity,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}, nil
}

// refill 补充令牌
func (r *RateLimiter) refill() {
	now := time.Now()
	elapsed := now.Sub(r.lastRefill).Seconds()
	if elapsed > 0 {
		refill := int64(elapsed * float64(r.refillRate))
		r.available += refill
		if r.available > r.capacity {
			r.available = r.capacity
		}
		r.lastRefill = now
	}
}

// TryAcquire 尝试获取令牌
func (r *RateLimiter) TryAcquire(tokens int64) bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.refill()

	if r.available >= tokens {
		r.available -= tokens
		return true
	}
	return false
}

// Wait 等待获取令牌
func (r *RateLimiter) Wait(ctx context.Context, tokens int64) error {
	for {
		r.mu.Lock()
		r.refill()

		if r.available >= tokens {
			r.available -= tokens
			r.mu.Unlock()
			return nil
		}
		r.mu.Unlock()

		select {
		case <-ctx.Done():
			return ErrContextCanceled
		case <-time.After(100 * time.Millisecond):
			continue
		}
	}
}

// Available 返回可用令牌数
func (r *RateLimiter) Available() int64 {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.refill()
	return r.available
}

// Capacity 返回容量
func (r *RateLimiter) Capacity() int64 {
	return r.capacity
}