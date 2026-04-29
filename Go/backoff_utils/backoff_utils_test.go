package backoff_utils

import (
	"context"
	"errors"
	"math"
	"testing"
	"time"
)

// Test ExponentialBackoff
func TestExponentialBackoff_Next(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   10 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewExponentialBackoff(config)

	tests := []struct {
		attempt  int
		expected time.Duration
	}{
		{0, 100 * time.Millisecond},
		{1, 200 * time.Millisecond},
		{2, 400 * time.Millisecond},
		{3, 800 * time.Millisecond},
		{4, 1600 * time.Millisecond},
	}

	for _, tt := range tests {
		result := backoff.Next(tt.attempt)
		if result != tt.expected {
			t.Errorf("ExponentialBackoff.Next(%d) = %v, want %v", tt.attempt, result, tt.expected)
		}
	}
}

func TestExponentialBackoff_MaxDelay(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   500 * time.Millisecond,
		Multiplier: 2.0,
	}

	backoff := NewExponentialBackoff(config)

	// Attempt 10 should be capped at MaxDelay
	result := backoff.Next(10)
	if result > config.MaxDelay {
		t.Errorf("ExponentialBackoff.Next(10) = %v, should be capped at %v", result, config.MaxDelay)
	}
}

func TestExponentialBackoff_NegativeAttempt(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewExponentialBackoff(config)
	result := backoff.Next(-1)
	if result != config.BaseDelay {
		t.Errorf("ExponentialBackoff.Next(-1) = %v, want %v", result, config.BaseDelay)
	}
}

// Test LinearBackoff
func TestLinearBackoff_Next(t *testing.T) {
	config := Config{
		BaseDelay: 100 * time.Millisecond,
		MaxDelay:  1 * time.Second,
	}

	backoff := NewLinearBackoff(config)

	tests := []struct {
		attempt  int
		expected time.Duration
	}{
		{0, 100 * time.Millisecond},
		{1, 200 * time.Millisecond},
		{2, 300 * time.Millisecond},
		{3, 400 * time.Millisecond},
	}

	for _, tt := range tests {
		result := backoff.Next(tt.attempt)
		if result != tt.expected {
			t.Errorf("LinearBackoff.Next(%d) = %v, want %v", tt.attempt, result, tt.expected)
		}
	}
}

func TestLinearBackoff_MaxDelay(t *testing.T) {
	config := Config{
		BaseDelay: 100 * time.Millisecond,
		MaxDelay:  500 * time.Millisecond,
	}

	backoff := NewLinearBackoff(config)

	// Attempt 10 should be capped at MaxDelay
	result := backoff.Next(10)
	if result > config.MaxDelay {
		t.Errorf("LinearBackoff.Next(10) = %v, should be capped at %v", result, config.MaxDelay)
	}
}

// Test ConstantBackoff
func TestConstantBackoff_Next(t *testing.T) {
	backoff := NewConstantBackoff(500 * time.Millisecond)

	for i := 0; i < 5; i++ {
		result := backoff.Next(i)
		if result != 500*time.Millisecond {
			t.Errorf("ConstantBackoff.Next(%d) = %v, want 500ms", i, result)
		}
	}
}

// Test FullJitterBackoff
func TestFullJitterBackoff_Next(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewFullJitterBackoff(config)

	for i := 0; i < 5; i++ {
		result := backoff.Next(i)
		// Result should be between 0 and expected delay
		// Use math.Pow to calculate expected delay
		maxExpected := time.Duration(float64(config.BaseDelay) * math.Pow(config.Multiplier, float64(i)))
		if maxExpected > config.MaxDelay {
			maxExpected = config.MaxDelay
		}
		if result < 0 || result > maxExpected {
			t.Errorf("FullJitterBackoff.Next(%d) = %v, should be between 0 and %v", i, result, maxExpected)
		}
	}
}

// Test EqualJitterBackoff
func TestEqualJitterBackoff_Next(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewEqualJitterBackoff(config)

	for i := 0; i < 5; i++ {
		result := backoff.Next(i)
		// Result should be between delay/2 and delay
		expectedDelay := time.Duration(float64(config.BaseDelay) * math.Pow(config.Multiplier, float64(i)))
		if expectedDelay > config.MaxDelay {
			expectedDelay = config.MaxDelay
		}
		minExpected := expectedDelay / 2

		if result < minExpected || result > expectedDelay {
			t.Errorf("EqualJitterBackoff.Next(%d) = %v, should be between %v and %v", i, result, minExpected, expectedDelay)
		}
	}
}

// Test DecorrelatedJitterBackoff
func TestDecorrelatedJitterBackoff_Next(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewDecorrelatedJitterBackoff(config)

	// First attempt should return base delay
	result := backoff.Next(0)
	if result != config.BaseDelay {
		t.Errorf("DecorrelatedJitterBackoff.Next(0) = %v, want %v", result, config.BaseDelay)
	}

	// Subsequent attempts should be within bounds
	for i := 1; i < 5; i++ {
		result = backoff.Next(i)
		if result < config.BaseDelay || result > config.MaxDelay {
			t.Errorf("DecorrelatedJitterBackoff.Next(%d) = %v, should be between %v and %v", i, result, config.BaseDelay, config.MaxDelay)
		}
	}
}

func TestDecorrelatedJitterBackoff_Reset(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	}

	backoff := NewDecorrelatedJitterBackoff(config)

	// Call Next a few times
	backoff.Next(0)
	backoff.Next(1)

	// Reset
	backoff.Reset()

	// Next call after reset should return base delay
	result := backoff.Next(0)
	if result != config.BaseDelay {
		t.Errorf("After Reset, DecorrelatedJitterBackoff.Next(0) = %v, want %v", result, config.BaseDelay)
	}
}

// Test WithJitter wrapper
func TestWithJitter_Next(t *testing.T) {
	baseBackoff := NewExponentialBackoff(Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		Multiplier: 2.0,
	})

	jitterBackoff := NewWithJitter(baseBackoff, 0.5)

	for i := 0; i < 5; i++ {
		result := jitterBackoff.Next(i)
		if result <= 0 {
			t.Errorf("WithJitter.Next(%d) = %v, should be positive", i, result)
		}
	}
}

// Test Retrier
func TestRetrier_Do_Success(t *testing.T) {
	config := Config{
		BaseDelay:  10 * time.Millisecond,
		MaxDelay:   100 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	callCount := 0
	err := retrier.Do(context.Background(), func() error {
		callCount++
		if callCount < 2 {
			return errors.New("temporary error")
		}
		return nil
	})

	if err != nil {
		t.Errorf("Retrier.Do() returned error: %v", err)
	}
	if callCount != 2 {
		t.Errorf("Expected 2 calls, got %d", callCount)
	}
}

func TestRetrier_Do_MaxRetries(t *testing.T) {
	config := Config{
		BaseDelay:  10 * time.Millisecond,
		MaxDelay:   100 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	callCount := 0
	err := retrier.Do(context.Background(), func() error {
		callCount++
		return errors.New("persistent error")
	})

	if err == nil {
		t.Error("Expected error, got nil")
	}

	var retryErr *RetryError
	if errors.As(err, &retryErr) {
		if retryErr.Attempt != config.MaxRetries {
			t.Errorf("Expected %d attempts, got %d", config.MaxRetries, retryErr.Attempt)
		}
	} else {
		t.Errorf("Expected RetryError, got %T", err)
	}
}

func TestRetrier_Do_ContextCancellation(t *testing.T) {
	config := Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   1 * time.Second,
		MaxRetries: 10,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	ctx, cancel := context.WithCancel(context.Background())
	
	go func() {
		time.Sleep(50 * time.Millisecond)
		cancel()
	}()

	err := retrier.Do(ctx, func() error {
		return errors.New("always fails")
	})

	if err == nil {
		t.Error("Expected error, got nil")
	}

	var retryErr *RetryError
	if errors.As(err, &retryErr) {
		if !errors.Is(retryErr.Err, ErrContextCanceled) {
			t.Errorf("Expected ErrContextCanceled, got %v", retryErr.Err)
		}
	}
}

func TestRetrier_RetryWithTimeout(t *testing.T) {
	config := Config{
		BaseDelay:  50 * time.Millisecond,
		MaxDelay:   100 * time.Millisecond,
		MaxRetries: 10,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	err := retrier.RetryWithTimeout(func() error {
		return errors.New("always fails")
	}, 150*time.Millisecond)

	if err == nil {
		t.Error("Expected error, got nil")
	}
}

// Test DoWithResult
func TestDoWithResult(t *testing.T) {
	config := Config{
		BaseDelay:  10 * time.Millisecond,
		MaxDelay:   100 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := NewExponentialBackoff(config)

	callCount := 0
	result, err := DoWithResult(context.Background(), backoff, config, func() (string, error) {
		callCount++
		if callCount < 2 {
			return "", errors.New("temporary error")
		}
		return "success", nil
	})

	if err != nil {
		t.Errorf("DoWithResult() returned error: %v", err)
	}
	if result != "success" {
		t.Errorf("Expected 'success', got '%s'", result)
	}
}

// Test Retrier with retryable check
func TestRetrier_DoWithRetryableCheck(t *testing.T) {
	config := Config{
		BaseDelay:  10 * time.Millisecond,
		MaxDelay:   100 * time.Millisecond,
		MaxRetries: 5,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	temporaryErr := errors.New("temporary error")
	permanentErr := errors.New("permanent error")

	isRetryable := func(err error) bool {
		return err == temporaryErr
	}

	// Test with retryable error that eventually succeeds
	callCount := 0
	err := retrier.DoWithRetryableCheck(context.Background(), func() error {
		callCount++
		if callCount < 2 {
			return temporaryErr
		}
		return nil
	}, isRetryable, config.MaxRetries)

	if err != nil {
		t.Errorf("Retrier.DoWithRetryableCheck() returned error: %v", err)
	}

	// Test with non-retryable error
	callCount = 0
	err = retrier.DoWithRetryableCheck(context.Background(), func() error {
		callCount++
		return permanentErr
	}, isRetryable, config.MaxRetries)

	if err == nil {
		t.Error("Expected error, got nil")
	}
	if callCount != 1 {
		t.Errorf("Expected 1 call for non-retryable error, got %d", callCount)
	}
}

// Test DefaultConfig
func TestDefaultConfig(t *testing.T) {
	config := DefaultConfig()

	if config.BaseDelay != 100*time.Millisecond {
		t.Errorf("DefaultConfig.BaseDelay = %v, want 100ms", config.BaseDelay)
	}
	if config.MaxDelay != 30*time.Second {
		t.Errorf("DefaultConfig.MaxDelay = %v, want 30s", config.MaxDelay)
	}
	if config.Multiplier != 2.0 {
		t.Errorf("DefaultConfig.Multiplier = %v, want 2.0", config.Multiplier)
	}
	if config.MaxRetries != 5 {
		t.Errorf("DefaultConfig.MaxRetries = %v, want 5", config.MaxRetries)
	}
}

// Test BackoffCalculator
func TestBackoffCalculator_CalculateExponential(t *testing.T) {
	calc := BackoffCalculator{}

	tests := []struct {
		base       time.Duration
		multiplier float64
		attempt    int
		expected   time.Duration
	}{
		{100 * time.Millisecond, 2.0, 0, 100 * time.Millisecond},
		{100 * time.Millisecond, 2.0, 1, 200 * time.Millisecond},
		{100 * time.Millisecond, 2.0, 2, 400 * time.Millisecond},
		{50 * time.Millisecond, 3.0, 1, 150 * time.Millisecond},
	}

	for _, tt := range tests {
		result := calc.CalculateExponential(tt.base, tt.multiplier, tt.attempt)
		if result != tt.expected {
			t.Errorf("CalculateExponential(%v, %v, %d) = %v, want %v",
				tt.base, tt.multiplier, tt.attempt, result, tt.expected)
		}
	}
}

func TestBackoffCalculator_CalculateLinear(t *testing.T) {
	calc := BackoffCalculator{}

	tests := []struct {
		base     time.Duration
		attempt  int
		expected time.Duration
	}{
		{100 * time.Millisecond, 0, 100 * time.Millisecond},
		{100 * time.Millisecond, 1, 200 * time.Millisecond},
		{100 * time.Millisecond, 2, 300 * time.Millisecond},
		{50 * time.Millisecond, 4, 250 * time.Millisecond},
	}

	for _, tt := range tests {
		result := calc.CalculateLinear(tt.base, tt.attempt)
		if result != tt.expected {
			t.Errorf("CalculateLinear(%v, %d) = %v, want %v",
				tt.base, tt.attempt, result, tt.expected)
		}
	}
}

func TestBackoffCalculator_CapDelay(t *testing.T) {
	calc := BackoffCalculator{}

	tests := []struct {
		delay    time.Duration
		maxDelay time.Duration
		expected time.Duration
	}{
		{100 * time.Millisecond, 1 * time.Second, 100 * time.Millisecond},
		{2 * time.Second, 1 * time.Second, 1 * time.Second},
		{500 * time.Millisecond, 1 * time.Second, 500 * time.Millisecond},
	}

	for _, tt := range tests {
		result := calc.CapDelay(tt.delay, tt.maxDelay)
		if result != tt.expected {
			t.Errorf("CapDelay(%v, %v) = %v, want %v",
				tt.delay, tt.maxDelay, result, tt.expected)
		}
	}
}

// Test SleepWithContext
func TestSleepWithContext(t *testing.T) {
	// Test normal sleep
	err := SleepWithContext(context.Background(), 10*time.Millisecond)
	if err != nil {
		t.Errorf("SleepWithContext() returned error: %v", err)
	}

	// Test with cancelled context
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	err = SleepWithContext(ctx, 100*time.Millisecond)
	if err == nil {
		t.Error("Expected error from cancelled context, got nil")
	}
}

// Benchmark tests
func BenchmarkExponentialBackoff_Next(b *testing.B) {
	backoff := NewExponentialBackoff(Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   10 * time.Second,
		Multiplier: 2.0,
	})

	for i := 0; i < b.N; i++ {
		backoff.Next(i % 20)
	}
}

func BenchmarkLinearBackoff_Next(b *testing.B) {
	backoff := NewLinearBackoff(Config{
		BaseDelay: 100 * time.Millisecond,
		MaxDelay:  10 * time.Second,
	})

	for i := 0; i < b.N; i++ {
		backoff.Next(i % 20)
	}
}

func BenchmarkFullJitterBackoff_Next(b *testing.B) {
	backoff := NewFullJitterBackoff(Config{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   10 * time.Second,
		Multiplier: 2.0,
	})

	for i := 0; i < b.N; i++ {
		backoff.Next(i % 20)
	}
}

func BenchmarkRetrier_Do(b *testing.B) {
	config := Config{
		BaseDelay:  1 * time.Millisecond,
		MaxDelay:   10 * time.Millisecond,
		MaxRetries: 3,
	}

	backoff := NewExponentialBackoff(config)
	retrier := NewRetrier(backoff, config)

	for i := 0; i < b.N; i++ {
		retrier.Do(context.Background(), func() error {
			return nil
		})
	}
}