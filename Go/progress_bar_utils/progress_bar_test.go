package progressbar

import (
	"bytes"
	"strings"
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	pb := New(100)
	if pb.total != 100 {
		t.Errorf("Expected total 100, got %d", pb.total)
	}
	if pb.current != 0 {
		t.Errorf("Expected current 0, got %d", pb.current)
	}
	if pb.width != 40 {
		t.Errorf("Expected default width 40, got %d", pb.width)
	}
}

func TestWithOptions(t *testing.T) {
	var buf bytes.Buffer
	pb := New(100,
		WithWidth(20),
		WithCompleteChar("="),
		WithIncompleteChar("-"),
		WithWriter(&buf),
		WithPrefix("Loading"),
		WithSuffix("items"),
		WithSpeed(true),
		WithETA(true),
	)

	if pb.width != 20 {
		t.Errorf("Expected width 20, got %d", pb.width)
	}
	if pb.complete != "=" {
		t.Errorf("Expected complete char '=', got %s", pb.complete)
	}
	if pb.incomplete != "-" {
		t.Errorf("Expected incomplete char '-', got %s", pb.incomplete)
	}
	if pb.prefix != "Loading" {
		t.Errorf("Expected prefix 'Loading', got %s", pb.prefix)
	}
	if pb.suffix != "items" {
		t.Errorf("Expected suffix 'items', got %s", pb.suffix)
	}
	if !pb.showSpeed {
		t.Error("Expected showSpeed to be true")
	}
	if !pb.showETA {
		t.Error("Expected showETA to be true")
	}
}

func TestAdd(t *testing.T) {
	pb := New(100)
	pb.Add(10)
	if pb.current != 10 {
		t.Errorf("Expected current 10, got %d", pb.current)
	}
	pb.Add(100)
	if pb.current != 100 {
		t.Errorf("Expected current 100 (capped at total), got %d", pb.current)
	}
}

func TestSet(t *testing.T) {
	pb := New(100)
	pb.Set(50)
	if pb.current != 50 {
		t.Errorf("Expected current 50, got %d", pb.current)
	}
	pb.Set(150)
	if pb.current != 100 {
		t.Errorf("Expected current 100 (capped at total), got %d", pb.current)
	}
	pb.Set(-10)
	if pb.current != 0 {
		t.Errorf("Expected current 0 (floor at 0), got %d", pb.current)
	}
}

func TestIncrement(t *testing.T) {
	pb := New(100)
	pb.Increment()
	if pb.current != 1 {
		t.Errorf("Expected current 1, got %d", pb.current)
	}
}

func TestPercentage(t *testing.T) {
	pb := New(200)
	if pb.Percentage() != 0 {
		t.Errorf("Expected 0%%, got %f%%", pb.Percentage())
	}
	pb.Set(100)
	if pb.Percentage() != 50 {
		t.Errorf("Expected 50%%, got %f%%", pb.Percentage())
	}
	pb.Set(200)
	if pb.Percentage() != 100 {
		t.Errorf("Expected 100%%, got %f%%", pb.Percentage())
	}
}

func TestPercentageZeroTotal(t *testing.T) {
	pb := New(0)
	if pb.Percentage() != 0 {
		t.Errorf("Expected 0%% for zero total, got %f%%", pb.Percentage())
	}
}

func TestIsComplete(t *testing.T) {
	pb := New(100)
	if pb.IsComplete() {
		t.Error("Expected incomplete at start")
	}
	pb.Set(99)
	if pb.IsComplete() {
		t.Error("Expected incomplete at 99%")
	}
	pb.Set(100)
	if !pb.IsComplete() {
		t.Error("Expected complete at 100%")
	}
}

func TestReset(t *testing.T) {
	pb := New(100)
	pb.Set(50)
	pb.Reset()
	if pb.current != 0 {
		t.Errorf("Expected current 0 after reset, got %d", pb.current)
	}
}

func TestRender(t *testing.T) {
	var buf bytes.Buffer
	pb := New(100, WithWriter(&buf), WithWidth(10))
	pb.Set(50)
	pb.Render()

	output := buf.String()
	if !strings.Contains(output, "50.0%") {
		t.Errorf("Expected output to contain '50.0%%', got %s", output)
	}
	if !strings.Contains(output, "(50/100)") {
		t.Errorf("Expected output to contain '(50/100)', got %s", output)
	}
}

func TestRenderWithPrefixSuffix(t *testing.T) {
	var buf bytes.Buffer
	pb := New(100, 
		WithWriter(&buf), 
		WithWidth(10),
		WithPrefix("Processing"),
		WithSuffix("files"),
	)
	pb.Set(25)
	pb.Render()

	output := buf.String()
	if !strings.Contains(output, "Processing") {
		t.Errorf("Expected output to contain prefix 'Processing', got %s", output)
	}
	if !strings.Contains(output, "files") {
		t.Errorf("Expected output to contain suffix 'files', got %s", output)
	}
}

func TestFormatSpeed(t *testing.T) {
	tests := []struct {
		speed    float64
		expected string
	}{
		{500, "500.00B"},
		{1024, "1.00KB"},
		{1536, "1.50KB"},
		{1048576, "1.00MB"},
		{1073741824, "1.00GB"},
	}

	for _, tt := range tests {
		result := formatSpeed(tt.speed)
		if !strings.HasPrefix(result, strings.Split(tt.expected, ".")[0]) {
			t.Errorf("formatSpeed(%f) = %s, want prefix of %s", tt.speed, result, tt.expected)
		}
	}
}

func TestFormatDuration(t *testing.T) {
	tests := []struct {
		duration time.Duration
		contains string
	}{
		{500 * time.Millisecond, "0s"},
		{5 * time.Second, "5s"},
		{65 * time.Second, "1m 5s"},
		{3661 * time.Second, "1h 1m 1s"},
	}

	for _, tt := range tests {
		result := formatDuration(tt.duration)
		if !strings.Contains(result, tt.contains) {
			t.Errorf("formatDuration(%v) = %s, want to contain %s", tt.duration, result, tt.contains)
		}
	}
}

func TestCurrentAndTotal(t *testing.T) {
	pb := New(100)
	if pb.Total() != 100 {
		t.Errorf("Expected total 100, got %d", pb.Total())
	}
	pb.Set(42)
	if pb.Current() != 42 {
		t.Errorf("Expected current 42, got %d", pb.Current())
	}
}

func TestElapsed(t *testing.T) {
	pb := New(100)
	time.Sleep(100 * time.Millisecond)
	elapsed := pb.Elapsed()
	if elapsed < 100*time.Millisecond {
		t.Errorf("Expected elapsed >= 100ms, got %v", elapsed)
	}
}

// Spinner tests
func TestNewSpinner(t *testing.T) {
	s := NewSpinner()
	if len(s.frames) != 10 {
		t.Errorf("Expected 10 default frames, got %d", len(s.frames))
	}
}

func TestSpinnerWithCustomFrames(t *testing.T) {
	frames := []string{"-", "+", "*"}
	s := NewSpinner(WithSpinnerFrames(frames))
	if len(s.frames) != 3 {
		t.Errorf("Expected 3 frames, got %d", len(s.frames))
	}
}

func TestSpinnerNext(t *testing.T) {
	s := NewSpinner(WithSpinnerFrames([]string{"a", "b", "c"}))
	for i := 0; i < 5; i++ {
		expected := i % 3
		if s.current != expected {
			t.Errorf("Iteration %d: expected current %d, got %d", i, expected, s.current)
		}
		s.Next()
	}
}

func TestSpinnerRender(t *testing.T) {
	var buf bytes.Buffer
	s := NewSpinner(
		WithSpinnerWriter(&buf),
		WithSpinnerPrefix("Loading... "),
		WithSpinnerSuffix(" Working"),
	)
	s.Render()

	output := buf.String()
	if !strings.Contains(output, "Loading...") {
		t.Errorf("Expected prefix in output, got %s", output)
	}
	if !strings.Contains(output, "Working") {
		t.Errorf("Expected suffix in output, got %s", output)
	}
}

// MultiBar tests
func TestNewMultiBar(t *testing.T) {
	mb := NewMultiBar()
	if len(mb.bars) != 0 {
		t.Errorf("Expected empty bars, got %d", len(mb.bars))
	}
}

func TestMultiBarAdd(t *testing.T) {
	mb := NewMultiBar()
	pb1 := mb.Add(100)
	pb2 := mb.Add(200)

	if len(mb.bars) != 2 {
		t.Errorf("Expected 2 bars, got %d", len(mb.bars))
	}
	if pb1.Total() != 100 {
		t.Errorf("Expected bar1 total 100, got %d", pb1.Total())
	}
	if pb2.Total() != 200 {
		t.Errorf("Expected bar2 total 200, got %d", pb2.Total())
	}
}

// Countdown tests
func TestNewCountdown(t *testing.T) {
	c := NewCountdown(5 * time.Second)
	if c.duration != 5*time.Second {
		t.Errorf("Expected duration 5s, got %v", c.duration)
	}
}

func TestCountdownWithOptions(t *testing.T) {
	var buf bytes.Buffer
	c := NewCountdown(1*time.Second,
		WithCountdownPrefix("Timer: "),
		WithCountdownWriter(&buf),
	)

	if c.prefix != "Timer: " {
		t.Errorf("Expected prefix 'Timer: ', got %s", c.prefix)
	}
}

// Benchmark tests
func BenchmarkProgressBarRender(b *testing.B) {
	pb := New(1000000)
	pb.Set(500000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pb.Render()
	}
}

func BenchmarkProgressBarAdd(b *testing.B) {
	pb := New(int64(b.N))
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pb.Add(1)
	}
}

func TestConcurrentAdd(t *testing.T) {
	pb := New(1000)
	done := make(chan bool)

	// Start 10 goroutines, each adding 100
	for i := 0; i < 10; i++ {
		go func() {
			for j := 0; j < 100; j++ {
				pb.Add(1)
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	if pb.current != 1000 {
		t.Errorf("Expected current 1000 after concurrent adds, got %d", pb.current)
	}
}

func TestConcurrentSet(t *testing.T) {
	pb := New(1000)
	done := make(chan bool)

	// Start 10 goroutines, each setting different values
	for i := 0; i < 10; i++ {
		go func(val int64) {
			pb.Set(val)
			done <- true
		}(int64(i * 100))
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	// Current should be some value between 0 and 1000
	if pb.current < 0 || pb.current > 1000 {
		t.Errorf("Current should be between 0-1000, got %d", pb.current)
	}
}