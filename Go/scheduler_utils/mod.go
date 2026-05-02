// Package scheduler_utils provides a lightweight task scheduler with zero external dependencies.
// Features: delay execution, interval execution, cron-style scheduling, task management.
package scheduler_utils

import (
	"context"
	"fmt"
	"math"
	"sync"
	"sync/atomic"
	"time"
)

// TaskStatus represents the current status of a task
type TaskStatus int

const (
	StatusPending TaskStatus = iota
	StatusRunning
	StatusCompleted
	StatusCancelled
	StatusFailed
)

func (s TaskStatus) String() string {
	switch s {
	case StatusPending:
		return "pending"
	case StatusRunning:
		return "running"
	case StatusCompleted:
		return "completed"
	case StatusCancelled:
		return "cancelled"
	case StatusFailed:
		return "failed"
	default:
		return "unknown"
	}
}

// TaskFunc is the function type for scheduled tasks
type TaskFunc func(ctx context.Context) error

// Task represents a scheduled task
type Task struct {
	ID          string
	Name        string
	Description string
	Status      TaskStatus
	CreatedAt   time.Time
	StartedAt   time.Time
	EndedAt     time.Time
	Error       error
	Result      interface{}
	tags        []string
	priority    int
}

// TaskInfo returns a summary of the task
func (t *Task) TaskInfo() string {
	return fmt.Sprintf("Task[ID=%s, Name=%s, Status=%s, Priority=%d]", t.ID, t.Name, t.Status, t.priority)
}

// TaskOption configures a task
type TaskOption func(*Task)

// WithPriority sets task priority (higher = more important)
func WithPriority(priority int) TaskOption {
	return func(t *Task) {
		t.priority = priority
	}
}

// WithTags sets task tags
func WithTags(tags ...string) TaskOption {
	return func(t *Task) {
		t.tags = tags
	}
}

// WithDescription sets task description
func WithDescription(desc string) TaskOption {
	return func(t *Task) {
		t.Description = desc
	}
}

// ScheduleType defines how a task is scheduled
type ScheduleType int

const (
	ScheduleOnce ScheduleType = iota
	ScheduleInterval
	ScheduleCron
)

// Schedule defines when a task runs
type Schedule struct {
	Type       ScheduleType
	StartAt    time.Time
	Interval   time.Duration
	CronExpr   string
	MaxRuns    int
	currentRun int
}

// Once creates a one-time schedule
func Once(at time.Time) *Schedule {
	return &Schedule{
		Type:    ScheduleOnce,
		StartAt: at,
	}
}

// After creates a one-time schedule after a duration
func After(d time.Duration) *Schedule {
	return &Schedule{
		Type:    ScheduleOnce,
		StartAt: time.Now().Add(d),
	}
}

// Every creates an interval schedule
func Every(interval time.Duration) *Schedule {
	return &Schedule{
		Type:     ScheduleInterval,
		Interval: interval,
	}
}

// EveryWithStart creates an interval schedule starting at a specific time
func EveryWithStart(interval time.Duration, start time.Time) *Schedule {
	return &Schedule{
		Type:     ScheduleInterval,
		Interval: interval,
		StartAt:  start,
	}
}

// WithMaxRuns limits the number of runs
func (s *Schedule) WithMaxRuns(max int) *Schedule {
	s.MaxRuns = max
	return s
}

// Scheduler manages scheduled tasks
type Scheduler struct {
	mu          sync.RWMutex
	tasks       map[string]*scheduledTask
	orderedIDs  []string // for priority ordering
	ctx         context.Context
	cancel      context.CancelFunc
	wg          sync.WaitGroup
	running     atomic.Bool
	now         func() time.Time // for testing
	taskCounter atomic.Int64
}

type scheduledTask struct {
	task     *Task
	fn       TaskFunc
	schedule *Schedule
	timer    *time.Timer
	stopCh   chan struct{}
}

// NewScheduler creates a new scheduler
func NewScheduler() *Scheduler {
	ctx, cancel := context.WithCancel(context.Background())
	return &Scheduler{
		tasks:  make(map[string]*scheduledTask),
		ctx:    ctx,
		cancel: cancel,
		now:    time.Now,
	}
}

// WithTimeFunc sets a custom time function (for testing)
func (s *Scheduler) WithTimeFunc(fn func() time.Time) *Scheduler {
	s.now = fn
	return s
}

// Start begins the scheduler
func (s *Scheduler) Start() {
	s.running.Store(true)
}

// Stop stops the scheduler and waits for running tasks
func (s *Scheduler) Stop() {
	s.cancel()
	s.running.Store(false)
	
	s.mu.Lock()
	for _, st := range s.tasks {
		if st.timer != nil {
			st.timer.Stop()
		}
		close(st.stopCh)
	}
	s.tasks = make(map[string]*scheduledTask)
	s.orderedIDs = nil
	s.mu.Unlock()
	
	s.wg.Wait()
}

// Stopper interface for clean shutdown
type Stopper interface {
	Stop()
}

// generateID creates a unique task ID
func (s *Scheduler) generateID() string {
	id := s.taskCounter.Add(1)
	return fmt.Sprintf("task_%d_%d", time.Now().UnixNano(), id)
}

// ScheduleTask schedules a task with the given schedule
func (s *Scheduler) ScheduleTask(name string, fn TaskFunc, schedule *Schedule, opts ...TaskOption) (*Task, error) {
	if fn == nil {
		return nil, fmt.Errorf("task function cannot be nil")
	}
	if schedule == nil {
		return nil, fmt.Errorf("schedule cannot be nil")
	}

	task := &Task{
		ID:        s.generateID(),
		Name:      name,
		Status:    StatusPending,
		CreatedAt: s.now(),
		priority:  0,
	}

	for _, opt := range opts {
		opt(task)
	}

	st := &scheduledTask{
		task:     task,
		fn:       fn,
		schedule: schedule,
		stopCh:   make(chan struct{}),
	}

	s.mu.Lock()
	s.tasks[task.ID] = st
	s.insertOrdered(task.ID, task.priority)
	s.mu.Unlock()

	// Calculate first run time
	s.scheduleNextRun(st)

	return task, nil
}

// insertOrdered inserts task ID maintaining priority order
func (s *Scheduler) insertOrdered(id string, priority int) {
	// Simple insertion - higher priority first
	for i, existingID := range s.orderedIDs {
		if existingTask, ok := s.tasks[existingID]; ok {
			if priority > existingTask.task.priority {
				s.orderedIDs = append(s.orderedIDs[:i], append([]string{id}, s.orderedIDs[i:]...)...)
				return
			}
		}
	}
	s.orderedIDs = append(s.orderedIDs, id)
}

// scheduleNextRun schedules the next execution of a task
func (s *Scheduler) scheduleNextRun(st *scheduledTask) {
	if !s.running.Load() {
		return
	}

	var delay time.Duration

	switch st.schedule.Type {
	case ScheduleOnce:
		delay = time.Until(st.schedule.StartAt)
		if delay < 0 {
			delay = 0
		}

	case ScheduleInterval:
		if st.schedule.StartAt.IsZero() {
			delay = st.schedule.Interval
		} else {
			delay = time.Until(st.schedule.StartAt)
			if delay < 0 {
				// Calculate next run aligned to interval
				elapsed := time.Since(st.schedule.StartAt)
				intervals := elapsed / st.schedule.Interval
				delay = st.schedule.Interval - (elapsed % st.schedule.Interval)
				if intervals == 0 {
					delay = 0
				}
			}
		}

	default:
		return
	}

	if delay < 0 {
		delay = 0
	}

	st.timer = time.AfterFunc(delay, func() {
		s.executeTask(st)
	})
}

// executeTask runs a task
func (s *Scheduler) executeTask(st *scheduledTask) {
	select {
	case <-st.stopCh:
		return
	case <-s.ctx.Done():
		return
	default:
	}

	s.wg.Add(1)
	defer s.wg.Done()

	st.task.Status = StatusRunning
	st.task.StartedAt = s.now()

	ctx, cancel := context.WithCancel(s.ctx)
	defer cancel()

	// Run the task
	err := st.fn(ctx)

	st.task.EndedAt = s.now()

	if err != nil {
		st.task.Status = StatusFailed
		st.task.Error = err
	} else {
		st.task.Status = StatusCompleted
	}

	// Handle interval scheduling
	if st.schedule.Type == ScheduleInterval && st.task.Status == StatusCompleted {
		st.schedule.currentRun++
		
		// Check max runs
		if st.schedule.MaxRuns > 0 && st.schedule.currentRun >= st.schedule.MaxRuns {
			return
		}

		// Reset status and reschedule
		st.task.Status = StatusPending
		st.task.StartedAt = time.Time{}
		st.task.EndedAt = time.Time{}
		st.task.Error = nil

		s.scheduleNextRun(st)
	}
}

// ScheduleOnce schedules a one-time task
func (s *Scheduler) ScheduleOnce(name string, fn TaskFunc, at time.Time, opts ...TaskOption) (*Task, error) {
	return s.ScheduleTask(name, fn, Once(at), opts...)
}

// ScheduleAfter schedules a task after a duration
func (s *Scheduler) ScheduleAfter(name string, fn TaskFunc, after time.Duration, opts ...TaskOption) (*Task, error) {
	return s.ScheduleTask(name, fn, After(after), opts...)
}

// ScheduleInterval schedules a repeating task
func (s *Scheduler) ScheduleInterval(name string, fn TaskFunc, interval time.Duration, opts ...TaskOption) (*Task, error) {
	return s.ScheduleTask(name, fn, Every(interval), opts...)
}

// Cancel cancels a task by ID
func (s *Scheduler) Cancel(taskID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	st, ok := s.tasks[taskID]
	if !ok {
		return fmt.Errorf("task %s not found", taskID)
	}

	if st.timer != nil {
		st.timer.Stop()
	}
	close(st.stopCh)

	st.task.Status = StatusCancelled
	delete(s.tasks, taskID)

	// Remove from ordered list
	for i, id := range s.orderedIDs {
		if id == taskID {
			s.orderedIDs = append(s.orderedIDs[:i], s.orderedIDs[i+1:]...)
			break
		}
	}

	return nil
}

// GetTask returns a task by ID
func (s *Scheduler) GetTask(taskID string) (*Task, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	st, ok := s.tasks[taskID]
	if !ok {
		return nil, fmt.Errorf("task %s not found", taskID)
	}

	return st.task, nil
}

// ListTasks returns all tasks
func (s *Scheduler) ListTasks() []*Task {
	s.mu.RLock()
	defer s.mu.RUnlock()

	tasks := make([]*Task, 0, len(s.tasks))
	for _, st := range s.tasks {
		tasks = append(tasks, st.task)
	}
	return tasks
}

// ListTasksByStatus returns tasks with a specific status
func (s *Scheduler) ListTasksByStatus(status TaskStatus) []*Task {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var tasks []*Task
	for _, st := range s.tasks {
		if st.task.Status == status {
			tasks = append(tasks, st.task)
		}
	}
	return tasks
}

// ListTasksByTag returns tasks with a specific tag
func (s *Scheduler) ListTasksByTag(tag string) []*Task {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var tasks []*Task
	for _, st := range s.tasks {
		for _, t := range st.task.tags {
			if t == tag {
				tasks = append(tasks, st.task)
				break
			}
		}
	}
	return tasks
}

// TaskCount returns the number of tasks
func (s *Scheduler) TaskCount() int {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return len(s.tasks)
}

// Clear removes all tasks
func (s *Scheduler) Clear() {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, st := range s.tasks {
		if st.timer != nil {
			st.timer.Stop()
		}
		close(st.stopCh)
	}

	s.tasks = make(map[string]*scheduledTask)
	s.orderedIDs = nil
}

// DelayQueue is a priority queue for delayed tasks
type DelayQueue struct {
	mu     sync.Mutex
	tasks  []*delayedTask
	ctx    context.Context
	cancel context.CancelFunc
	cond   *sync.Cond
	closed bool
}

type delayedTask struct {
	runAt time.Time
	id    string
	fn    func()
}

// NewDelayQueue creates a new delay queue
func NewDelayQueue() *DelayQueue {
	ctx, cancel := context.WithCancel(context.Background())
	dq := &DelayQueue{
		ctx:    ctx,
		cancel: cancel,
	}
	dq.cond = sync.NewCond(&dq.mu)
	go dq.run()
	return dq
}

// run processes tasks from the queue
func (dq *DelayQueue) run() {
	for {
		dq.mu.Lock()
		
		for len(dq.tasks) == 0 && !dq.closed {
			dq.cond.Wait()
		}

		if dq.closed {
			dq.mu.Unlock()
			return
		}

		// Peek at first task
		task := dq.tasks[0]
		now := time.Now()

		if now.Before(task.runAt) {
			// Wait until first task is ready
			waitTime := task.runAt.Sub(now)
			dq.mu.Unlock()
			time.Sleep(waitTime)
			continue
		}

		// Remove and execute
		dq.tasks = dq.tasks[1:]
		dq.mu.Unlock()

		task.fn()
	}
}

// Schedule adds a task to be executed after a delay
func (dq *DelayQueue) Schedule(delay time.Duration, fn func()) string {
	dq.mu.Lock()
	defer dq.mu.Unlock()

	if dq.closed {
		return ""
	}

	id := fmt.Sprintf("delay_%d", time.Now().UnixNano())
	task := &delayedTask{
		runAt: time.Now().Add(delay),
		id:    id,
		fn:    fn,
	}

	// Insert in sorted order
	i := 0
	for i < len(dq.tasks) && dq.tasks[i].runAt.Before(task.runAt) {
		i++
	}

	if i == len(dq.tasks) {
		dq.tasks = append(dq.tasks, task)
	} else {
		dq.tasks = append(dq.tasks[:i], append([]*delayedTask{task}, dq.tasks[i:]...)...)
	}

	dq.cond.Broadcast()
	return id
}

// Cancel removes a scheduled task
func (dq *DelayQueue) Cancel(id string) bool {
	dq.mu.Lock()
	defer dq.mu.Unlock()

	for i, task := range dq.tasks {
		if task.id == id {
			dq.tasks = append(dq.tasks[:i], dq.tasks[i+1:]...)
			return true
		}
	}
	return false
}

// Size returns the number of pending tasks
func (dq *DelayQueue) Size() int {
	dq.mu.Lock()
	defer dq.mu.Unlock()
	return len(dq.tasks)
}

// Close stops the delay queue
func (dq *DelayQueue) Close() {
	dq.mu.Lock()
	defer dq.mu.Unlock()
	dq.closed = true
	dq.cond.Broadcast()
	dq.cancel()
}

// RateLimitScheduler wraps a scheduler with rate limiting
type RateLimitScheduler struct {
	scheduler  *Scheduler
	tokenBucket *TokenBucket
}

// TokenBucket implements a simple token bucket rate limiter
type TokenBucket struct {
	mu         sync.Mutex
	tokens     float64
	maxTokens  float64
	refillRate float64
	lastRefill time.Time
}

// NewTokenBucket creates a new token bucket
func NewTokenBucket(maxTokens, refillRate float64) *TokenBucket {
	return &TokenBucket{
		tokens:     maxTokens,
		maxTokens:  maxTokens,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

// Take attempts to take a token
func (tb *TokenBucket) Take() bool {
	tb.mu.Lock()
	defer tb.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(tb.lastRefill).Seconds()
	tb.tokens = math.Min(tb.maxTokens, tb.tokens+elapsed*tb.refillRate)
	tb.lastRefill = now

	if tb.tokens >= 1 {
		tb.tokens--
		return true
	}
	return false
}

// Wait blocks until a token is available
func (tb *TokenBucket) Wait(ctx context.Context) error {
	for {
		if tb.Take() {
			return nil
		}
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(100 * time.Millisecond):
		}
	}
}

// NewRateLimitScheduler wraps a scheduler with rate limiting
func NewRateLimitScheduler(scheduler *Scheduler, maxTokens, refillRate float64) *RateLimitScheduler {
	return &RateLimitScheduler{
		scheduler:   scheduler,
		tokenBucket: NewTokenBucket(maxTokens, refillRate),
	}
}

// ScheduleOnce schedules a one-time task with rate limiting
func (rls *RateLimitScheduler) ScheduleOnce(name string, fn TaskFunc, at time.Time, opts ...TaskOption) (*Task, error) {
	return rls.scheduler.ScheduleOnce(name, func(ctx context.Context) error {
		if err := rls.tokenBucket.Wait(ctx); err != nil {
			return err
		}
		return fn(ctx)
	}, at, opts...)
}

// ScheduleInterval schedules an interval task with rate limiting
func (rls *RateLimitScheduler) ScheduleInterval(name string, fn TaskFunc, interval time.Duration, opts ...TaskOption) (*Task, error) {
	return rls.scheduler.ScheduleInterval(name, func(ctx context.Context) error {
		if err := rls.tokenBucket.Wait(ctx); err != nil {
			return err
		}
		return fn(ctx)
	}, interval, opts...)
}