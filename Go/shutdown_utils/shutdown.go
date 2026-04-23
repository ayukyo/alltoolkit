// Package shutdown provides utilities for graceful shutdown of Go applications.
// It handles OS signals, manages shutdown hooks, and ensures clean resource cleanup.
package shutdown

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

// Hook represents a shutdown hook function with priority and name.
type Hook struct {
	Name     string
	Priority int // Lower numbers run first
	Func     func(ctx context.Context) error
	Timeout  time.Duration
}

// Manager manages graceful shutdown with hooks, timeouts, and signal handling.
type Manager struct {
	mu          sync.Mutex
	hooks       []*Hook
	shutdownCtx context.Context
	cancelFunc  context.CancelFunc
	shutdown    bool
	timeout     time.Duration
	logger      Logger
}

// Logger interface for custom logging.
type Logger interface {
	Info(msg string, fields ...interface{})
	Error(msg string, fields ...interface{})
}

// defaultLogger is a no-op logger.
type defaultLogger struct{}

func (l *defaultLogger) Info(msg string, fields ...interface{})  {}
func (l *defaultLogger) Error(msg string, fields ...interface{}) {}

// Option configures the Manager.
type Option func(*Manager)

// WithTimeout sets the default shutdown timeout.
func WithTimeout(timeout time.Duration) Option {
	return func(m *Manager) {
		m.timeout = timeout
	}
}

// WithLogger sets a custom logger.
func WithLogger(logger Logger) Option {
	return func(m *Manager) {
		m.logger = logger
	}
}

// New creates a new shutdown Manager.
func New(opts ...Option) *Manager {
	m := &Manager{
		timeout: 30 * time.Second,
		logger:  &defaultLogger{},
	}
	for _, opt := range opts {
		opt(m)
	}
	m.shutdownCtx, m.cancelFunc = context.WithCancel(context.Background())
	return m
}

// Register adds a shutdown hook.
// Hooks with lower priority values run first.
func (m *Manager) Register(hook *Hook) error {
	if hook == nil {
		return fmt.Errorf("hook cannot be nil")
	}
	if hook.Func == nil {
		return fmt.Errorf("hook function cannot be nil")
	}
	if hook.Timeout == 0 {
		hook.Timeout = m.timeout
	}

	m.mu.Lock()
	defer m.mu.Unlock()

	// Insert hook in priority order
	inserted := false
	for i, h := range m.hooks {
		if hook.Priority < h.Priority {
			m.hooks = append(m.hooks[:i], append([]*Hook{hook}, m.hooks[i:]...)...)
			inserted = true
			break
		}
	}
	if !inserted {
		m.hooks = append(m.hooks, hook)
	}

	m.logger.Info("Registered shutdown hook", "name", hook.Name, "priority", hook.Priority)
	return nil
}

// RegisterFunc is a convenience method to register a hook with default settings.
func (m *Manager) RegisterFunc(name string, fn func(ctx context.Context) error, opts ...HookOption) error {
	hook := &Hook{
		Name:    name,
		Priority: 100,
		Func:    fn,
	}
	for _, opt := range opts {
		opt(hook)
	}
	return m.Register(hook)
}

// HookOption configures a Hook.
type HookOption func(*Hook)

// WithPriority sets the hook priority.
func WithPriority(priority int) HookOption {
	return func(h *Hook) {
		h.Priority = priority
	}
}

// WithHookTimeout sets the hook timeout.
func WithHookTimeout(timeout time.Duration) HookOption {
	return func(h *Hook) {
		h.Timeout = timeout
	}
}

// Listen starts listening for shutdown signals (SIGINT, SIGTERM).
// It returns a channel that will be closed when shutdown is initiated.
func (m *Manager) Listen() <-chan struct{} {
	done := make(chan struct{})

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		sig := <-sigChan
		m.logger.Info("Received shutdown signal", "signal", sig.String())
		m.Shutdown()
		close(done)
	}()

	return done
}

// ListenWithContext starts listening and returns a context that will be cancelled on shutdown.
func (m *Manager) ListenWithContext() context.Context {
	m.Listen()
	return m.shutdownCtx
}

// Shutdown initiates the graceful shutdown process.
// It runs all registered hooks in priority order.
func (m *Manager) Shutdown() {
	m.mu.Lock()
	if m.shutdown {
		m.mu.Unlock()
		return
	}
	m.shutdown = true
	hooks := make([]*Hook, len(m.hooks))
	copy(hooks, m.hooks)
	m.mu.Unlock()

	m.logger.Info("Starting graceful shutdown", "hooks", len(hooks))
	m.cancelFunc()

	startTime := time.Now()
	var errors []error

	for _, hook := range hooks {
		ctx, cancel := context.WithTimeout(context.Background(), hook.Timeout)
		m.logger.Info("Running shutdown hook", "name", hook.Name)

		hookStart := time.Now()
		if err := hook.Func(ctx); err != nil {
			m.logger.Error("Shutdown hook failed", "name", hook.Name, "error", err)
			errors = append(errors, fmt.Errorf("%s: %w", hook.Name, err))
		}
		cancel()
		m.logger.Info("Shutdown hook completed", "name", hook.Name, "duration", time.Since(hookStart))
	}

	duration := time.Since(startTime)
	if len(errors) > 0 {
		m.logger.Error("Shutdown completed with errors", "duration", duration, "errors", len(errors))
	} else {
		m.logger.Info("Shutdown completed successfully", "duration", duration)
	}
}

// IsShuttingDown returns true if shutdown has been initiated.
func (m *Manager) IsShuttingDown() bool {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.shutdown
}

// Context returns the shutdown context that is cancelled when shutdown begins.
func (m *Manager) Context() context.Context {
	return m.shutdownCtx
}

// WaitForShutdown blocks until shutdown is complete.
// This is typically called in main() after Listen().
func (m *Manager) WaitForShutdown() {
	<-m.shutdownCtx.Done()
	// Give hooks time to run
	time.Sleep(100 * time.Millisecond)
}

// Clear removes all registered hooks (mainly for testing).
func (m *Manager) Clear() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.hooks = nil
	m.shutdown = false
	m.shutdownCtx, m.cancelFunc = context.WithCancel(context.Background())
}

// HookCount returns the number of registered hooks.
func (m *Manager) HookCount() int {
	m.mu.Lock()
	defer m.mu.Unlock()
	return len(m.hooks)
}

// RunHooks executes all hooks immediately without requiring a signal.
// Useful for testing or manual shutdown triggers.
func (m *Manager) RunHooks() context.Context {
	ctx, cancel := context.WithCancel(context.Background())
	
	m.mu.Lock()
	if m.shutdown {
		m.mu.Unlock()
		cancel()
		return ctx
	}
	m.shutdown = true
	hooks := make([]*Hook, len(m.hooks))
	copy(hooks, m.hooks)
	m.mu.Unlock()

	m.cancelFunc()

	go func() {
		defer cancel()
		for _, hook := range hooks {
			ctx, cancel := context.WithTimeout(context.Background(), hook.Timeout)
			hook.Func(ctx)
			cancel()
		}
	}()

	return ctx
}