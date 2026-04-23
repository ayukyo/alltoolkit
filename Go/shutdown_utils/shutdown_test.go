package shutdown

import (
	"context"
	"sync/atomic"
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	m := New()
	if m == nil {
		t.Fatal("New() returned nil")
	}
	if m.timeout != 30*time.Second {
		t.Errorf("expected default timeout 30s, got %v", m.timeout)
	}
}

func TestNewWithOptions(t *testing.T) {
	m := New(
		WithTimeout(10*time.Second),
	)
	if m.timeout != 10*time.Second {
		t.Errorf("expected timeout 10s, got %v", m.timeout)
	}
}

func TestRegisterHook(t *testing.T) {
	m := New()
	err := m.Register(&Hook{
		Name:     "test-hook",
		Priority: 1,
		Func:     func(ctx context.Context) error { return nil },
	})
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if m.HookCount() != 1 {
		t.Errorf("expected 1 hook, got %d", m.HookCount())
	}
}

func TestRegisterNilHook(t *testing.T) {
	m := New()
	err := m.Register(nil)
	if err == nil {
		t.Error("expected error for nil hook")
	}
}

func TestRegisterNilFunc(t *testing.T) {
	m := New()
	err := m.Register(&Hook{Name: "test"})
	if err == nil {
		t.Error("expected error for nil hook function")
	}
}

func TestRegisterFunc(t *testing.T) {
	m := New()
	err := m.RegisterFunc("test", func(ctx context.Context) error { return nil })
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestHookPriority(t *testing.T) {
	m := New()
	var order []int32

	m.Register(&Hook{
		Name:     "hook-3",
		Priority: 30,
		Func: func(ctx context.Context) error {
			order = append(order, 3)
			return nil
		},
	})
	m.Register(&Hook{
		Name:     "hook-1",
		Priority: 10,
		Func: func(ctx context.Context) error {
			order = append(order, 1)
			return nil
		},
	})
	m.Register(&Hook{
		Name:     "hook-2",
		Priority: 20,
		Func: func(ctx context.Context) error {
			order = append(order, 2)
			return nil
		},
	})

	m.Shutdown()

	expected := []int32{1, 2, 3}
	for i, v := range expected {
		if i >= len(order) || order[i] != v {
			t.Errorf("expected order %v, got %v", expected, order)
			break
		}
	}
}

func TestIsShuttingDown(t *testing.T) {
	m := New()
	if m.IsShuttingDown() {
		t.Error("should not be shutting down initially")
	}
	m.Shutdown()
	if !m.IsShuttingDown() {
		t.Error("should be shutting down after Shutdown()")
	}
}

func TestDoubleShutdown(t *testing.T) {
	m := New()
	var counter int32

	m.RegisterFunc("test", func(ctx context.Context) error {
		atomic.AddInt32(&counter, 1)
		return nil
	})

	m.Shutdown()
	m.Shutdown() // Should not run hooks again

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("expected hook to run once, ran %d times", counter)
	}
}

func TestHookTimeout(t *testing.T) {
	m := New()
	var completed int32

	m.Register(&Hook{
		Name:     "slow-hook",
		Priority: 1,
		Timeout:  100 * time.Millisecond,
		Func: func(ctx context.Context) error {
			select {
			case <-time.After(1 * time.Second):
				atomic.StoreInt32(&completed, 1)
			case <-ctx.Done():
				// Timeout occurred
			}
			return nil
		},
	})

	start := time.Now()
	m.Shutdown()
	elapsed := time.Since(start)

	if atomic.LoadInt32(&completed) == 1 {
		t.Error("hook should not have completed")
	}
	if elapsed > 500*time.Millisecond {
		t.Errorf("shutdown took too long: %v", elapsed)
	}
}

func TestHookError(t *testing.T) {
	m := New()
	err := m.RegisterFunc("failing-hook", func(ctx context.Context) error {
		return context.Canceled
	})
	if err != nil {
		t.Errorf("unexpected error registering hook: %v", err)
	}

	// Should not panic
	m.Shutdown()
}

func TestContext(t *testing.T) {
	m := New()
	ctx := m.Context()

	if ctx == nil {
		t.Fatal("Context() returned nil")
	}

	select {
	case <-ctx.Done():
		t.Error("context should not be done initially")
	default:
	}

	m.Shutdown()

	select {
	case <-ctx.Done():
		// Expected
	case <-time.After(1 * time.Second):
		t.Error("context should be done after shutdown")
	}
}

func TestClear(t *testing.T) {
	m := New()
	m.RegisterFunc("test", func(ctx context.Context) error { return nil })
	m.Shutdown()

	m.Clear()

	if m.HookCount() != 0 {
		t.Errorf("expected 0 hooks after Clear(), got %d", m.HookCount())
	}
	if m.IsShuttingDown() {
		t.Error("should not be shutting down after Clear()")
	}
}

func TestRunHooks(t *testing.T) {
	m := New()
	var executed int32

	m.RegisterFunc("test", func(ctx context.Context) error {
		atomic.StoreInt32(&executed, 1)
		return nil
	})

	ctx := m.RunHooks()
	<-ctx.Done()

	if atomic.LoadInt32(&executed) != 1 {
		t.Error("hook should have executed")
	}
}

func TestConcurrentRegister(t *testing.T) {
	m := New()
	done := make(chan bool)

	for i := 0; i < 100; i++ {
		go func(id int) {
			m.RegisterFunc("hook-"+string(rune('A'+id%26)), func(ctx context.Context) error {
				return nil
			})
			done <- true
		}(i)
	}

	for i := 0; i < 100; i++ {
		<-done
	}

	if m.HookCount() != 100 {
		t.Errorf("expected 100 hooks, got %d", m.HookCount())
	}
}

func TestWithPriorityOption(t *testing.T) {
	m := New()
	var order []int

	m.RegisterFunc("low", func(ctx context.Context) error {
		order = append(order, 2)
		return nil
	}, WithPriority(100))

	m.RegisterFunc("high", func(ctx context.Context) error {
		order = append(order, 1)
		return nil
	}, WithPriority(1))

	m.Shutdown()

	if order[0] != 1 || order[1] != 2 {
		t.Errorf("expected [1, 2], got %v", order)
	}
}

func TestWithHookTimeoutOption(t *testing.T) {
	m := New()
	var hookTimeout time.Duration

	m.RegisterFunc("test", func(ctx context.Context) error {
		return nil
	}, WithHookTimeout(5*time.Second))

	m.mu.Lock()
	if len(m.hooks) > 0 {
		hookTimeout = m.hooks[0].Timeout
	}
	m.mu.Unlock()

	if hookTimeout != 5*time.Second {
		t.Errorf("expected timeout 5s, got %v", hookTimeout)
	}
}

// TestLogger tests custom logger functionality
type testLogger struct {
	infos  []string
	errors []string
}

func (l *testLogger) Info(msg string, fields ...interface{}) {
	l.infos = append(l.infos, msg)
}

func (l *testLogger) Error(msg string, fields ...interface{}) {
	l.errors = append(l.errors, msg)
}

func TestWithLoggerOption(t *testing.T) {
	logger := &testLogger{}
	m := New(WithLogger(logger))

	m.RegisterFunc("test", func(ctx context.Context) error {
		return nil
	})
	m.Shutdown()

	if len(logger.infos) == 0 {
		t.Error("expected info logs")
	}
}