package scheduler_utils

import (
	"context"
	"errors"
	"fmt"
	"sync/atomic"
	"testing"
	"time"
)

func TestTaskStatus(t *testing.T) {
	tests := []struct {
		status   TaskStatus
		expected string
	}{
		{StatusPending, "pending"},
		{StatusRunning, "running"},
		{StatusCompleted, "completed"},
		{StatusCancelled, "cancelled"},
		{StatusFailed, "failed"},
	}

	for _, tt := range tests {
		if got := tt.status.String(); got != tt.expected {
			t.Errorf("TaskStatus.String() = %v, want %v", got, tt.expected)
		}
	}
}

func TestTaskInfo(t *testing.T) {
	task := &Task{
		ID:       "test-123",
		Name:     "Test Task",
		Status:   StatusPending,
		priority: 5,
	}

	info := task.TaskInfo()
	expected := "Task[ID=test-123, Name=Test Task, Status=pending, Priority=5]"
	if info != expected {
		t.Errorf("TaskInfo() = %v, want %v", info, expected)
	}
}

func TestScheduleOnce(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	var executed atomic.Bool
	task, err := s.ScheduleOnce("test", func(ctx context.Context) error {
		executed.Store(true)
		return nil
	}, time.Now().Add(50*time.Millisecond))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	if task.Status != StatusPending {
		t.Errorf("Initial status = %v, want pending", task.Status)
	}

	// Wait for execution
	time.Sleep(150 * time.Millisecond)

	if !executed.Load() {
		t.Error("Task was not executed")
	}
}

func TestScheduleAfter(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	var executed atomic.Bool
	start := time.Now()
	_, err := s.ScheduleAfter("test", func(ctx context.Context) error {
		executed.Store(true)
		return nil
	}, 100*time.Millisecond)

	if err != nil {
		t.Fatalf("ScheduleAfter failed: %v", err)
	}

	// Wait for execution
	time.Sleep(200 * time.Millisecond)

	if !executed.Load() {
		t.Error("Task was not executed")
	}

	elapsed := time.Since(start)
	if elapsed < 100*time.Millisecond {
		t.Errorf("Task executed too early: %v", elapsed)
	}
}

func TestScheduleInterval(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	var count atomic.Int32
	task, err := s.ScheduleInterval("interval-test", func(ctx context.Context) error {
		count.Add(1)
		return nil
	}, 50*time.Millisecond)

	if err != nil {
		t.Fatalf("ScheduleInterval failed: %v", err)
	}

	// Wait for multiple executions
	time.Sleep(200 * time.Millisecond)

	if count.Load() < 2 {
		t.Errorf("Interval task executed %d times, expected at least 2", count.Load())
	}

	// Cancel the task
	if err := s.Cancel(task.ID); err != nil {
		t.Fatalf("Cancel failed: %v", err)
	}

	// Verify task is removed
	if _, err := s.GetTask(task.ID); err == nil {
		t.Error("Task should be removed after cancel")
	}
}

func TestScheduleIntervalWithMaxRuns(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	var count atomic.Int32
	task, err := s.ScheduleTask("max-runs-test", func(ctx context.Context) error {
		count.Add(1)
		return nil
	}, Every(50*time.Millisecond).WithMaxRuns(3))

	if err != nil {
		t.Fatalf("ScheduleTask failed: %v", err)
	}

	// Wait for executions to complete
	time.Sleep(300 * time.Millisecond)

	if count.Load() != 3 {
		t.Errorf("Task executed %d times, expected 3", count.Load())
	}

	// Task should be auto-removed after max runs
	time.Sleep(50 * time.Millisecond)
	_ = task
}

func TestTaskWithPriority(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	task, err := s.ScheduleOnce("priority-test", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour), WithPriority(10))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	if task.priority != 10 {
		t.Errorf("Priority = %d, want 10", task.priority)
	}
}

func TestTaskWithTags(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	_, err := s.ScheduleOnce("tag-test", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour), WithTags("important", "production"))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	tasks := s.ListTasksByTag("important")
	if len(tasks) != 1 {
		t.Errorf("ListTasksByTag returned %d tasks, want 1", len(tasks))
	}

	tasks = s.ListTasksByTag("nonexistent")
	if len(tasks) != 0 {
		t.Errorf("ListTasksByTag for nonexistent tag returned %d tasks, want 0", len(tasks))
	}
}

func TestTaskWithDescription(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	task, err := s.ScheduleOnce("desc-test", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour), WithDescription("This is a test task"))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	if task.Description != "This is a test task" {
		t.Errorf("Description = %v, want 'This is a test task'", task.Description)
	}
}

func TestTaskFailure(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	expectedErr := errors.New("task failed")
	task, err := s.ScheduleOnce("fail-test", func(ctx context.Context) error {
		return expectedErr
	}, time.Now().Add(50*time.Millisecond))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	// Wait for execution
	time.Sleep(150 * time.Millisecond)

	if task.Status != StatusFailed {
		t.Errorf("Status = %v, want failed", task.Status)
	}

	if task.Error != expectedErr {
		t.Errorf("Error = %v, want %v", task.Error, expectedErr)
	}
}

func TestCancelPendingTask(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	var executed atomic.Bool
	task, err := s.ScheduleOnce("cancel-test", func(ctx context.Context) error {
		executed.Store(true)
		return nil
	}, time.Now().Add(1*time.Hour))

	if err != nil {
		t.Fatalf("ScheduleOnce failed: %v", err)
	}

	// Cancel before execution
	if err := s.Cancel(task.ID); err != nil {
		t.Fatalf("Cancel failed: %v", err)
	}

	// Wait a bit to ensure no execution
	time.Sleep(100 * time.Millisecond)

	if executed.Load() {
		t.Error("Task should not have executed after cancel")
	}
}

func TestListTasks(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	// Add multiple tasks
	for i := 0; i < 5; i++ {
		_, err := s.ScheduleOnce(fmt.Sprintf("task-%d", i), func(ctx context.Context) error {
			return nil
		}, time.Now().Add(1*time.Hour))
		if err != nil {
			t.Fatalf("ScheduleOnce failed: %v", err)
		}
	}

	tasks := s.ListTasks()
	if len(tasks) != 5 {
		t.Errorf("ListTasks returned %d tasks, want 5", len(tasks))
	}
}

func TestListTasksByStatus(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	// Add pending task
	_, _ = s.ScheduleOnce("pending-task", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour))

	// Add task that will complete
	_, _ = s.ScheduleOnce("complete-task", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(50*time.Millisecond))

	// Wait for completion
	time.Sleep(150 * time.Millisecond)

	pending := s.ListTasksByStatus(StatusPending)
	if len(pending) != 1 {
		t.Errorf("Pending tasks = %d, want 1", len(pending))
	}

	completed := s.ListTasksByStatus(StatusCompleted)
	if len(completed) != 1 {
		t.Errorf("Completed tasks = %d, want 1", len(completed))
	}
}

func TestClear(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	// Add multiple tasks
	for i := 0; i < 5; i++ {
		_, _ = s.ScheduleOnce(fmt.Sprintf("task-%d", i), func(ctx context.Context) error {
			return nil
		}, time.Now().Add(1*time.Hour))
	}

	if s.TaskCount() != 5 {
		t.Errorf("TaskCount = %d, want 5", s.TaskCount())
	}

	s.Clear()

	if s.TaskCount() != 0 {
		t.Errorf("TaskCount after Clear = %d, want 0", s.TaskCount())
	}
}

func TestNilFunction(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	_, err := s.ScheduleOnce("nil-test", nil, time.Now().Add(1*time.Hour))
	if err == nil {
		t.Error("ScheduleOnce should fail with nil function")
	}
}

func TestNilSchedule(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	_, err := s.ScheduleTask("nil-schedule", func(ctx context.Context) error {
		return nil
	}, nil)
	if err == nil {
		t.Error("ScheduleTask should fail with nil schedule")
	}
}

// DelayQueue tests

func TestDelayQueue(t *testing.T) {
	dq := NewDelayQueue()
	defer dq.Close()

	var executed atomic.Int32
	order := make([]int, 0, 3)

	dq.Schedule(100*time.Millisecond, func() {
		executed.Add(1)
		order = append(order, 2)
	})

	dq.Schedule(50*time.Millisecond, func() {
		executed.Add(1)
		order = append(order, 1)
	})

	dq.Schedule(150*time.Millisecond, func() {
		executed.Add(1)
		order = append(order, 3)
	})

	// Wait for all to execute
	time.Sleep(250 * time.Millisecond)

	if executed.Load() != 3 {
		t.Errorf("Executed %d tasks, want 3", executed.Load())
	}

	// Check order
	expectedOrder := []int{1, 2, 3}
	for i, v := range expectedOrder {
		if order[i] != v {
			t.Errorf("Order[%d] = %d, want %d", i, order[i], v)
		}
	}
}

func TestDelayQueueCancel(t *testing.T) {
	dq := NewDelayQueue()
	defer dq.Close()

	var executed atomic.Bool
	id := dq.Schedule(100*time.Millisecond, func() {
		executed.Store(true)
	})

	// Cancel immediately
	if !dq.Cancel(id) {
		t.Error("Cancel should return true for existing task")
	}

	time.Sleep(200 * time.Millisecond)

	if executed.Load() {
		t.Error("Task should not have executed after cancel")
	}

	// Cancel again should fail
	if dq.Cancel(id) {
		t.Error("Cancel should return false for non-existent task")
	}
}

func TestDelayQueueSize(t *testing.T) {
	dq := NewDelayQueue()
	defer dq.Close()

	if dq.Size() != 0 {
		t.Errorf("Initial size = %d, want 0", dq.Size())
	}

	dq.Schedule(1*time.Hour, func() {})
	dq.Schedule(1*time.Hour, func() {})

	if dq.Size() != 2 {
		t.Errorf("Size = %d, want 2", dq.Size())
	}
}

// TokenBucket tests

func TestTokenBucket(t *testing.T) {
	tb := NewTokenBucket(2, 1) // 2 tokens, 1 per second

	// Should be able to take 2 tokens immediately
	if !tb.Take() {
		t.Error("Should be able to take first token")
	}
	if !tb.Take() {
		t.Error("Should be able to take second token")
	}

	// Third should fail
	if tb.Take() {
		t.Error("Should not be able to take third token")
	}

	// Wait for refill
	time.Sleep(1100 * time.Millisecond)

	// Should work now
	if !tb.Take() {
		t.Error("Should be able to take token after refill")
	}
}

func TestTokenBucketWait(t *testing.T) {
	tb := NewTokenBucket(1, 10) // 1 token, 10 per second

	// Take the only token
	tb.Take()

	start := time.Now()
	ctx := context.Background()
	tb.Wait(ctx)
	elapsed := time.Since(start)

	// Should have waited ~100ms (1 token / 10 per second)
	if elapsed < 50*time.Millisecond {
		t.Errorf("Wait returned too quickly: %v", elapsed)
	}
}

func TestTokenBucketWaitContextCancel(t *testing.T) {
	tb := NewTokenBucket(0, 0.1) // Very slow refill

	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := tb.Wait(ctx)
	if err != context.DeadlineExceeded {
		t.Errorf("Wait should return context error, got %v", err)
	}
}

// RateLimitScheduler tests

func TestRateLimitScheduler(t *testing.T) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	rls := NewRateLimitScheduler(s, 2, 10) // 2 tokens, 10 per second (faster refill)

	var count atomic.Int32

	// Schedule 3 tasks at the same time
	for i := 0; i < 3; i++ {
		_, err := rls.ScheduleOnce(fmt.Sprintf("rate-test-%d", i), func(ctx context.Context) error {
			count.Add(1)
			return nil
		}, time.Now().Add(50*time.Millisecond))
		if err != nil {
			t.Fatalf("ScheduleOnce failed: %v", err)
		}
	}

	// Wait for execution (with rate limiting, third task needs ~100ms for token refill)
	time.Sleep(500 * time.Millisecond)

	if count.Load() != 3 {
		t.Errorf("Executed %d tasks, want 3", count.Load())
	}
}

// Benchmark tests

func BenchmarkScheduleOnce(b *testing.B) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = s.ScheduleOnce("bench-test", func(ctx context.Context) error {
			return nil
		}, time.Now().Add(1*time.Hour))
	}
}

func BenchmarkScheduleInterval(b *testing.B) {
	s := NewScheduler()
	s.Start()
	defer s.Stop()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = s.ScheduleInterval("bench-interval", func(ctx context.Context) error {
			return nil
		}, 1*time.Hour)
	}
}

func BenchmarkTokenBucket(b *testing.B) {
	tb := NewTokenBucket(1000, 1000)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tb.Take()
	}
}

func BenchmarkDelayQueue(b *testing.B) {
	dq := NewDelayQueue()
	defer dq.Close()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		dq.Schedule(1*time.Hour, func() {})
	}
}