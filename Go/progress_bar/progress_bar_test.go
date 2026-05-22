package progress_bar

import (
	"bytes"
	"strings"
	"testing"
	"time"
)

// ==================== Style Tests ====================

func TestStyleDefaults(t *testing.T) {
	styles := []Style{
		StyleDefault,
		StyleClassic,
		StyleArrow,
		StyleBlocks,
		StyleDots,
		StylePipe,
		StyleMinimal,
		StyleCircle,
	}

	for i, style := range styles {
		if style.Complete == "" {
			t.Errorf("Style %d: Complete should not be empty", i)
		}
		if style.Incomplete == "" {
			t.Errorf("Style %d: Incomplete should not be empty", i)
		}
		if style.Description == "" {
			t.Errorf("Style %d: Description should not be empty", i)
		}
	}
}

// ==================== New Tests ====================

func TestNew(t *testing.T) {
	pb := New(100)
	if pb == nil {
		t.Fatal("New should return non-nil ProgressBar")
	}
	if pb.config.Total != 100 {
		t.Errorf("Expected Total 100, got %d", pb.config.Total)
	}
	if pb.config.Width <= 0 {
		t.Error("Width should be positive")
	}
	if pb.current != 0 {
		t.Errorf("Initial current should be 0, got %d", pb.current)
	}
}

func TestNewWithConfig(t *testing.T) {
	buf := &bytes.Buffer{}
	config := Config{
		Total:          200,
		Width:          50,
		Style:          StyleClassic,
		Description:    "Test",
		ShowPercentage: false,
		ShowCount:      false,
		ShowETA:        false,
		ShowSpeed:      false,
		Writer:         buf,
	}

	pb := NewWithConfig(config)
	if pb.config.Total != 200 {
		t.Errorf("Expected Total 200, got %d", pb.config.Total)
	}
	if pb.config.Width != 50 {
		t.Errorf("Expected Width 50, got %d", pb.config.Width)
	}
	if pb.config.Description != "Test" {
		t.Errorf("Expected Description 'Test', got '%s'", pb.config.Description)
	}
}

func TestNewWithZeroWidth(t *testing.T) {
	config := Config{
		Total: 100,
		Width: 0,
	}
	pb := NewWithConfig(config)
	if pb.config.Width <= 0 {
		t.Error("Width should default to positive value when set to 0")
	}
}

func TestNewWithNegativeTotal(t *testing.T) {
	pb := New(-100)
	if pb.config.Total != 0 {
		t.Errorf("Negative total should be set to 0, got %d", pb.config.Total)
	}
}

// ==================== Add/Set/Increment Tests ====================

func TestAdd(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Add(10)
	if pb.current != 10 {
		t.Errorf("Expected current 10, got %d", pb.current)
	}
}

func TestAddMultiple(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Add(10)
	pb.Add(20)
	pb.Add(30)
	if pb.current != 60 {
		t.Errorf("Expected current 60, got %d", pb.current)
	}
}

func TestAddOverflow(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Add(150)
	if pb.current != 100 {
		t.Errorf("Current should cap at total, got %d", pb.current)
	}
}

func TestAddNegative(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Add(50)
	pb.Add(-30)
	if pb.current != 20 {
		t.Errorf("Current should be 20 after negative add, got %d", pb.current)
	}
}

func TestAddNegativeToZero(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Add(50)
	pb.Add(-100) // Should cap at 0
	if pb.current != 0 {
		t.Errorf("Current should be 0 after large negative add, got %d", pb.current)
	}
}

func TestSet(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(75)
	if pb.current != 75 {
		t.Errorf("Expected current 75, got %d", pb.current)
	}
}

func TestSetOverflow(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(200)
	if pb.current != 100 {
		t.Errorf("Current should cap at total, got %d", pb.current)
	}
}

func TestSetNegative(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(-50)
	if pb.current != 0 {
		t.Errorf("Current should be 0 for negative set, got %d", pb.current)
	}
}

func TestIncrement(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	for i := 0; i < 5; i++ {
		pb.Increment()
	}
	if pb.current != 5 {
		t.Errorf("Expected current 5, got %d", pb.current)
	}
}

func TestIncrementAfterFinish(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 10, Writer: buf})
	pb.Finish()
	pb.Increment()
	if pb.current != 10 {
		t.Errorf("Should not increment after finish, got %d", pb.current)
	}
}

// ==================== Percentage Tests ====================

func TestPercentage(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 200, Writer: buf})
	pb.Set(50)
	if pb.Percentage() != 25.0 {
		t.Errorf("Expected 25%%, got %.2f%%", pb.Percentage())
	}
}

func TestPercentageZeroTotal(t *testing.T) {
	pb := New(0)
	if pb.Percentage() != 0 {
		t.Errorf("Percentage should be 0 for zero total, got %.2f", pb.Percentage())
	}
}

func TestPercentageComplete(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(100)
	if pb.Percentage() != 100.0 {
		t.Errorf("Expected 100%%, got %.2f%%", pb.Percentage())
	}
}

// ==================== ETA Tests ====================

func TestETAZeroProgress(t *testing.T) {
	pb := New(100)
	eta := pb.ETA()
	if eta != 0 {
		t.Errorf("ETA should be 0 for zero progress, got %v", eta)
	}
}

func TestETAComplete(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(100)
	eta := pb.ETA()
	if eta != 0 {
		t.Errorf("ETA should be 0 for complete progress, got %v", eta)
	}
}

// ==================== Elapsed Tests ====================

func TestElapsed(t *testing.T) {
	pb := New(100)
	elapsed := pb.Elapsed()
	if elapsed < 0 {
		t.Errorf("Elapsed should be non-negative, got %v", elapsed)
	}
}

func TestElapsedAfterWait(t *testing.T) {
	pb := New(100)
	start := pb.Elapsed()
	time.Sleep(50 * time.Millisecond)
	elapsed := pb.Elapsed()
	if elapsed <= start {
		t.Errorf("Elapsed should increase after wait")
	}
}

// ==================== Speed Tests ====================

func TestSpeedZero(t *testing.T) {
	pb := New(100)
	speed := pb.Speed()
	if speed != 0 {
		t.Errorf("Speed should be 0 initially, got %v", speed)
	}
}

func TestSpeedPositive(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 1000, Writer: buf})
	pb.Set(100)
	speed := pb.Speed()
	if speed <= 0 {
		t.Errorf("Speed should be positive after progress, got %v", speed)
	}
}

// ==================== Finish/Reset Tests ====================

func TestFinish(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(50)
	pb.Finish()
	if !pb.isFinished {
		t.Error("ProgressBar should be finished")
	}
	if pb.current != 100 {
		t.Errorf("Current should be 100 after finish, got %d", pb.current)
	}
}

func TestFinishTwice(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Finish()
	pb.Finish() // Should not panic
}

func TestReset(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(75)
	pb.Finish()
	pb.Reset()
	if pb.current != 0 {
		t.Errorf("Current should be 0 after reset, got %d", pb.current)
	}
	if pb.isFinished {
		t.Error("ProgressBar should not be finished after reset")
	}
}

// ==================== Describe Tests ====================

func TestDescribe(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Describe("New Description")
	if pb.config.Description != "New Description" {
		t.Errorf("Expected 'New Description', got '%s'", pb.config.Description)
	}
}

// ==================== Static Progress Bar Tests ====================

func TestStatic(t *testing.T) {
	bar := Static(50, 100, 20, StyleClassic)
	if bar == "" {
		t.Error("Static should return non-empty string")
	}
	if !strings.Contains(bar, "[") {
		t.Error("Classic style should contain '['")
	}
	if !strings.Contains(bar, "]") {
		t.Error("Classic style should contain ']'")
	}
}

func TestStaticZeroProgress(t *testing.T) {
	bar := Static(0, 100, 20, StyleDefault)
	if bar == "" {
		t.Error("Static should return non-empty string for zero progress")
	}
}

func TestStaticComplete(t *testing.T) {
	bar := Static(100, 100, 20, StyleDefault)
	if bar == "" {
		t.Error("Static should return non-empty string for complete progress")
	}
}

func TestStaticOverflow(t *testing.T) {
	bar := Static(200, 100, 20, StyleDefault)
	if bar == "" {
		t.Error("Static should handle overflow gracefully")
	}
}

func TestStaticPercentage(t *testing.T) {
	bar := StaticPercentage(50, 100, 20, StyleClassic)
	if !strings.Contains(bar, "50.0%") && !strings.Contains(bar, "50%") {
		t.Errorf("StaticPercentage should contain percentage, got: %s", bar)
	}
}

func TestStaticFull(t *testing.T) {
	bar := StaticFull(50, 100, 20, StyleClassic, "Progress")
	if !strings.Contains(bar, "Progress") {
		t.Errorf("StaticFull should contain description, got: %s", bar)
	}
	if !strings.Contains(bar, "50") {
		t.Errorf("StaticFull should contain count, got: %s", bar)
	}
}

func TestStaticWithConfig(t *testing.T) {
	bar := StaticWithConfig(50, 100, Config{
		Width:  20,
		Style:  StyleArrow,
	})
	if bar == "" {
		t.Error("StaticWithConfig should return non-empty string")
	}
}

func TestStaticWithColor(t *testing.T) {
	bar := StaticWithConfig(50, 100, Config{
		Width:          20,
		Style:          StyleDefault,
		ColorComplete:  ColorGreen,
		ColorIncomplete: ColorRed,
	})
	if bar == "" {
		t.Error("StaticWithConfig with color should return non-empty string")
	}
}

// ==================== MultiBar Tests ====================

func TestNewMultiBar(t *testing.T) {
	mb := NewMultiBar()
	if mb == nil {
		t.Fatal("NewMultiBar should return non-nil MultiBar")
	}
}

func TestMultiBarAddBar(t *testing.T) {
	mb := NewMultiBar()
	pb := mb.AddBar(100, "Task 1:")
	if pb == nil {
		t.Error("AddBar should return non-nil ProgressBar")
	}
	if len(mb.bars) != 1 {
		t.Errorf("Expected 1 bar, got %d", len(mb.bars))
	}
}

func TestMultiBarMultipleBars(t *testing.T) {
	mb := NewMultiBar()
	mb.AddBar(100, "Task 1:")
	mb.AddBar(200, "Task 2:")
	mb.AddBar(300, "Task 3:")
	if len(mb.bars) != 3 {
		t.Errorf("Expected 3 bars, got %d", len(mb.bars))
	}
}

// ==================== Spinner Tests ====================

func TestNewSpinner(t *testing.T) {
	s := NewSpinner("Loading")
	if s == nil {
		t.Fatal("NewSpinner should return non-nil Spinner")
	}
	if s.prefix != "Loading" {
		t.Errorf("Expected prefix 'Loading', got '%s'", s.prefix)
	}
}

func TestSpinnerSetFrames(t *testing.T) {
	s := NewSpinner("Test")
	frames := []string{"|", "/", "-", "\\"}
	s.SetFrames(frames)
	if len(s.frames) != 4 {
		t.Errorf("Expected 4 frames, got %d", len(s.frames))
	}
}

func TestSpinnerSetInterval(t *testing.T) {
	s := NewSpinner("Test")
	s.SetInterval(50 * time.Millisecond)
	if s.interval != 50*time.Millisecond {
		t.Errorf("Expected interval 50ms, got %v", s.interval)
	}
}

func TestSpinnerSetSuffix(t *testing.T) {
	s := NewSpinner("Test")
	s.SetSuffix("Processing...")
	if s.suffix != "Processing..." {
		t.Errorf("Expected suffix 'Processing...', got '%s'", s.suffix)
	}
}

func TestSpinnerStartStop(t *testing.T) {
	buf := &bytes.Buffer{}
	s := NewSpinner("Test")
	s.writer = buf
	s.Start()
	time.Sleep(150 * time.Millisecond)
	s.Stop()
	if s.stopCh != nil {
		t.Error("stopCh should be nil after stop")
	}
}

// ==================== Utility Function Tests ====================

func TestFormatBytes(t *testing.T) {
	tests := []struct {
		bytes    int64
		expected string
	}{
		{0, "0 B"},
		{500, "500 B"},
		{1024, "1.00 KB"},
		{1536, "1.50 KB"},
		{1048576, "1.00 MB"},
		{1572864, "1.50 MB"},
		{1073741824, "1.00 GB"},
		{1099511627776, "1.00 TB"},
	}

	for _, tt := range tests {
		result := FormatBytes(tt.bytes)
		if !strings.HasPrefix(result, strings.Split(tt.expected, " ")[0]) {
			t.Errorf("FormatBytes(%d) = %s, expected %s", tt.bytes, result, tt.expected)
		}
	}
}

func TestFormatNumber(t *testing.T) {
	tests := []struct {
		n        int64
		expected string
	}{
		{0, "0"},
		{100, "100"},
		{1000, "1,000"},
		{10000, "10,000"},
		{100000, "100,000"},
		{1000000, "1,000,000"},
		{1234567890, "1,234,567,890"},
	}

	for _, tt := range tests {
		result := FormatNumber(tt.n)
		if result != tt.expected {
			t.Errorf("FormatNumber(%d) = %s, expected %s", tt.n, result, tt.expected)
		}
	}
}

func TestCalculateProgress(t *testing.T) {
	tests := []struct {
		current  int64
		total    int64
		expected float64
	}{
		{0, 100, 0},
		{25, 100, 25},
		{50, 100, 50},
		{75, 100, 75},
		{100, 100, 100},
		{150, 100, 100}, // Overflow
		{50, 0, 0},      // Zero total
		{-10, 100, 0},   // Negative current
	}

	for _, tt := range tests {
		result := CalculateProgress(tt.current, tt.total)
		if result != tt.expected {
			t.Errorf("CalculateProgress(%d, %d) = %.2f, expected %.2f",
				tt.current, tt.total, result, tt.expected)
		}
	}
}

func TestEstimateTime(t *testing.T) {
	// Test zero progress
	eta := EstimateTime(100*time.Millisecond, 0, 100)
	if eta != 0 {
		t.Errorf("EstimateTime with zero current should be 0, got %v", eta)
	}

	// Test complete progress
	eta = EstimateTime(100*time.Millisecond, 100, 100)
	if eta != 0 {
		t.Errorf("EstimateTime with complete progress should be 0, got %v", eta)
	}

	// Test normal progress
	eta = EstimateTime(1*time.Second, 50, 100)
	if eta <= 0 {
		t.Errorf("EstimateTime with normal progress should be positive, got %v", eta)
	}
}

// ==================== Color Tests ====================

func TestColorConstants(t *testing.T) {
	colors := []Color{
		ColorReset,
		ColorRed,
		ColorGreen,
		ColorYellow,
		ColorBlue,
		ColorPurple,
		ColorCyan,
		ColorWhite,
		ColorBold,
	}

	for i, color := range colors {
		if color == "" {
			t.Errorf("Color %d should not be empty", i)
		}
	}
}

// ==================== Iterator Tests ====================

func TestIterate(t *testing.T) {
	items := []int{1, 2, 3, 4, 5}
	sum := 0

	err := Iterate(items, "Processing", func(i int, v int) error {
		sum += v
		return nil
	})

	if err != nil {
		t.Errorf("Iterate should not return error, got: %v", err)
	}
	if sum != 15 {
		t.Errorf("Sum should be 15, got %d", sum)
	}
}

func TestIterateWithError(t *testing.T) {
	items := []int{1, 2, 3, 4, 5}
	err := Iterate(items, "Processing", func(i int, v int) error {
		if v == 3 {
			return ioError("test error")
		}
		return nil
	})

	if err == nil {
		t.Error("Iterate should return error from callback")
	}
}

func TestIterateEmpty(t *testing.T) {
	items := []int{}
	err := Iterate(items, "Processing", func(i int, v int) error {
		return nil
	})

	if err != nil {
		t.Errorf("Iterate should not return error for empty slice, got: %v", err)
	}
}

func TestIterateWithConfig(t *testing.T) {
	items := []string{"a", "b", "c"}
	result := ""

	err := IterateWithConfig(items, Config{
		Width:          20,
		Style:          StyleClassic,
		Description:    "Test",
		ShowPercentage: true,
	}, func(i int, v string) error {
		result += v
		return nil
	})

	if err != nil {
		t.Errorf("IterateWithConfig should not return error, got: %v", err)
	}
	if result != "abc" {
		t.Errorf("Result should be 'abc', got '%s'", result)
	}
}

// ==================== UpdateConfig Tests ====================

func TestUpdateConfig(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.UpdateConfig(Config{
		Total:       200,
		Description: "Updated",
		Width:       60,
	})

	if pb.config.Total != 200 {
		t.Errorf("Expected Total 200, got %d", pb.config.Total)
	}
	if pb.config.Description != "Updated" {
		t.Errorf("Expected Description 'Updated', got '%s'", pb.config.Description)
	}
}

// ==================== Current Tests ====================

func TestCurrent(t *testing.T) {
	pb := New(100)
	if pb.Current() != 0 {
		t.Errorf("Initial current should be 0, got %d", pb.Current())
	}

	pb.Add(50)
	if pb.Current() != 50 {
		t.Errorf("Current should be 50, got %d", pb.Current())
	}
}

// ==================== Clear Tests ====================

func TestClear(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 100, Writer: buf})
	pb.Set(50)
	pb.Clear()
	// Clear should output something
	if buf.Len() == 0 {
		t.Error("Clear should output to writer")
	}
}

// ==================== Concurrent Tests ====================

func TestConcurrentAdd(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{Total: 10000, Writer: buf})

	done := make(chan bool)
	for i := 0; i < 100; i++ {
		go func() {
			for j := 0; j < 100; j++ {
				pb.Increment()
			}
			done <- true
		}()
	}

	for i := 0; i < 100; i++ {
		<-done
	}

	if pb.Current() != 10000 {
		t.Errorf("Current should be 10000, got %d", pb.Current())
	}
}

// ==================== BuildBar Tests ====================

func TestBuildBar(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{
		Total:  100,
		Width:  10,
		Style:  StyleClassic,
		Writer: buf,
	})
	pb.Set(50)

	bar := pb.buildBar()
	if bar == "" {
		t.Error("buildBar should return non-empty string")
	}
	if !strings.Contains(bar, "[") || !strings.Contains(bar, "]") {
		t.Errorf("Classic style should contain brackets, got: %s", bar)
	}
}

func TestBuildBarZeroProgress(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{
		Total:  100,
		Width:  10,
		Style:  StyleClassic,
		Writer: buf,
	})

	bar := pb.buildBar()
	if !strings.Contains(bar, "[") {
		t.Error("Zero progress bar should still render")
	}
}

func TestBuildBarFullProgress(t *testing.T) {
	buf := &bytes.Buffer{}
	pb := NewWithConfig(Config{
		Total:  100,
		Width:  10,
		Style:  StyleClassic,
		Writer: buf,
	})
	pb.Set(100)

	bar := pb.buildBar()
	if !strings.Contains(bar, "=") {
		t.Errorf("Full progress bar should contain complete characters")
	}
}

// ==================== Helper ====================

type ioError string

func (e ioError) Error() string { return string(e) }