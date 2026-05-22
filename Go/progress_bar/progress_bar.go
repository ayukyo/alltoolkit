// Package progress_bar provides a terminal progress bar utility with zero external dependencies.
// Supports multiple styles, colors, ETA estimation, and concurrent safety.
package progress_bar

import (
	"fmt"
	"io"
	"os"
	"strings"
	"sync"
	"time"
)

// Style represents a progress bar visual style
type Style struct {
	Complete    string // Character for completed portion
	Incomplete  string // Character for incomplete portion
	LeftEnd     string // Left border character
	RightEnd    string // Right border character
	Description string // Style description
}

// Predefined progress bar styles
var (
	StyleDefault = Style{
		Complete:    "█",
		Incomplete:  "░",
		LeftEnd:     "|",
		RightEnd:    "|",
		Description: "Default block style",
	}

	StyleClassic = Style{
		Complete:    "=",
		Incomplete:  " ",
		LeftEnd:     "[",
		RightEnd:    "]",
		Description: "Classic ASCII style",
	}

	StyleArrow = Style{
		Complete:    "=",
		Incomplete:  " ",
		LeftEnd:     "[",
		RightEnd:    ">",
		Description: "Arrow style",
	}

	StyleBlocks = Style{
		Complete:    "▓",
		Incomplete:  "░",
		LeftEnd:     "",
		RightEnd:    "",
		Description: "Block style without borders",
	}

	StyleDots = Style{
		Complete:    "●",
		Incomplete:  "○",
		LeftEnd:     "",
		RightEnd:    "",
		Description: "Dots style",
	}

	StylePipe = Style{
		Complete:    "│",
		Incomplete:  " ",
		LeftEnd:     "├",
		RightEnd:    "┤",
		Description: "Pipe style",
	}

	StyleMinimal = Style{
		Complete:    "#",
		Incomplete:  "-",
		LeftEnd:     "",
		RightEnd:    "",
		Description: "Minimal style",
	}

	StyleCircle = Style{
		Complete:    "◉",
		Incomplete:  "◎",
		LeftEnd:     "",
		RightEnd:    "",
		Description: "Circle style",
	}
)

// Color represents ANSI color codes
type Color string

const (
	ColorReset  Color = "\033[0m"
	ColorRed    Color = "\033[31m"
	ColorGreen  Color = "\033[32m"
	ColorYellow Color = "\033[33m"
	ColorBlue   Color = "\033[34m"
	ColorPurple Color = "\033[35m"
	ColorCyan   Color = "\033[36m"
	ColorWhite  Color = "\033[37m"
	ColorBold   Color = "\033[1m"
)

// Config holds progress bar configuration
type Config struct {
	Total           int64   // Total work items
	Width           int     // Bar width in characters
	Style           Style   // Visual style
	Description     string  // Description text
	ShowPercentage  bool    // Show percentage
	ShowCount       bool    // Show current/total count
	ShowETA         bool    // Show estimated time remaining
	ShowSpeed       bool    // Show items per second
	ShowElapsedTime bool    // Show elapsed time
	ShowSpinner     bool    // Show animated spinner
	ColorComplete   Color   // Color for completed portion
	ColorIncomplete Color   // Color for incomplete portion
	Writer          io.Writer // Output writer (default: os.Stderr)
}

// ProgressBar represents a progress bar instance
type ProgressBar struct {
	config      Config
	current     int64
	startTime   time.Time
	lastUpdate  time.Time
	spinnerPos  int
	mu          sync.Mutex
	isFinished  bool
	lastRate    float64
	rateSamples []float64
}

// Spinner characters
var spinnerChars = []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}

// New creates a new progress bar with default configuration
func New(total int64) *ProgressBar {
	return NewWithConfig(Config{
		Total:           total,
		Width:           40,
		Style:           StyleDefault,
		ShowPercentage:  true,
		ShowCount:       true,
		ShowETA:         true,
		ShowSpeed:       true,
		ShowElapsedTime: false,
		ShowSpinner:     false,
		Writer:          os.Stderr,
	})
}

// NewWithConfig creates a new progress bar with custom configuration
func NewWithConfig(config Config) *ProgressBar {
	if config.Width <= 0 {
		config.Width = 40
	}
	if config.Writer == nil {
		config.Writer = os.Stderr
	}
	if config.Total < 0 {
		config.Total = 0
	}

	return &ProgressBar{
		config:      config,
		current:     0,
		startTime:   time.Now(),
		lastUpdate:  time.Now(),
		spinnerPos:  0,
		rateSamples: make([]float64, 0, 10),
	}
}

// Add increments the progress by n
func (pb *ProgressBar) Add(n int64) {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	if pb.isFinished {
		return
	}

	pb.current += n
	if pb.current > pb.config.Total {
		pb.current = pb.config.Total
	}
	if pb.current < 0 {
		pb.current = 0
	}

	pb.render()
}

// Set sets the current progress value
func (pb *ProgressBar) Set(current int64) {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	if pb.isFinished {
		return
	}

	pb.current = current
	if pb.current > pb.config.Total {
		pb.current = pb.config.Total
	}
	if pb.current < 0 {
		pb.current = 0
	}

	pb.render()
}

// Increment increments the progress by 1
func (pb *ProgressBar) Increment() {
	pb.Add(1)
}

// Current returns the current progress value
func (pb *ProgressBar) Current() int64 {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	return pb.current
}

// Percentage returns the current percentage (0-100)
func (pb *ProgressBar) Percentage() float64 {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	if pb.config.Total == 0 {
		return 0
	}
	return float64(pb.current) / float64(pb.config.Total) * 100
}

// ETA returns the estimated time remaining
func (pb *ProgressBar) ETA() time.Duration {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	if pb.current == 0 || pb.current >= pb.config.Total {
		return 0
	}

	elapsed := time.Since(pb.startTime).Seconds()
	if elapsed == 0 {
		return 0
	}

	rate := float64(pb.current) / elapsed
	if rate == 0 {
		return 0
	}

	remaining := float64(pb.config.Total-pb.current) / rate
	return time.Duration(remaining) * time.Second
}

// Elapsed returns the elapsed time
func (pb *ProgressBar) Elapsed() time.Duration {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	return time.Since(pb.startTime)
}

// Speed returns the items per second rate
func (pb *ProgressBar) Speed() float64 {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	elapsed := time.Since(pb.startTime).Seconds()
	if elapsed == 0 {
		return 0
	}
	return float64(pb.current) / elapsed
}

// Finish completes the progress bar
func (pb *ProgressBar) Finish() {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	if pb.isFinished {
		return
	}

	pb.current = pb.config.Total
	pb.isFinished = true
	pb.render()
	fmt.Fprintln(pb.config.Writer)
}

// Reset resets the progress bar
func (pb *ProgressBar) Reset() {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	pb.current = 0
	pb.startTime = time.Now()
	pb.lastUpdate = time.Now()
	pb.isFinished = false
	pb.spinnerPos = 0
	pb.rateSamples = make([]float64, 0, 10)
}

// Clear clears the progress bar line
func (pb *ProgressBar) Clear() {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	fmt.Fprint(pb.config.Writer, "\r\033[K")
}

// Describe sets or updates the description
func (pb *ProgressBar) Describe(desc string) {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	pb.config.Description = desc
	pb.render()
}

// UpdateConfig updates the configuration
func (pb *ProgressBar) UpdateConfig(config Config) {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	pb.config = config
	if pb.config.Width <= 0 {
		pb.config.Width = 40
	}
	if pb.config.Writer == nil {
		pb.config.Writer = os.Stderr
	}
	pb.render()
}

// render outputs the progress bar
func (pb *ProgressBar) render() {
	if pb.config.Writer == nil {
		return
	}

	var parts []string

	// Spinner
	if pb.config.ShowSpinner {
		parts = append(parts, spinnerChars[pb.spinnerPos]+" ")
		pb.spinnerPos = (pb.spinnerPos + 1) % len(spinnerChars)
	}

	// Description
	if pb.config.Description != "" {
		parts = append(parts, pb.config.Description+": ")
	}

	// Progress bar
	bar := pb.buildBar()
	parts = append(parts, bar)

	// Percentage (calculate directly to avoid deadlock)
	if pb.config.ShowPercentage {
		var percent float64
		if pb.config.Total > 0 {
			percent = float64(pb.current) / float64(pb.config.Total) * 100
		}
		parts = append(parts, fmt.Sprintf(" %6.2f%%", percent))
	}

	// Count
	if pb.config.ShowCount {
		parts = append(parts, fmt.Sprintf(" %d/%d", pb.current, pb.config.Total))
	}

	// Speed (calculate directly to avoid deadlock)
	if pb.config.ShowSpeed && pb.current > 0 {
		elapsed := time.Since(pb.startTime).Seconds()
		if elapsed > 0 {
			speed := float64(pb.current) / elapsed
			parts = append(parts, fmt.Sprintf(" [%s/s]", formatSpeed(speed)))
		}
	}

	// ETA (calculate directly to avoid deadlock)
	if pb.config.ShowETA && pb.current > 0 && pb.current < pb.config.Total {
		elapsed := time.Since(pb.startTime).Seconds()
		if elapsed > 0 {
			rate := float64(pb.current) / elapsed
			if rate > 0 {
				remaining := float64(pb.config.Total-pb.current) / rate
				eta := time.Duration(remaining) * time.Second
				parts = append(parts, fmt.Sprintf(" ETA: %s", formatDuration(eta)))
			}
		}
	}

	// Elapsed time (calculate directly to avoid deadlock)
	if pb.config.ShowElapsedTime {
		elapsed := time.Since(pb.startTime)
		parts = append(parts, fmt.Sprintf(" [%s]", formatDuration(elapsed)))
	}

	// Build final line
	line := strings.Join(parts, "")

	// Clear line and print
	fmt.Fprint(pb.config.Writer, "\r\033[K"+line)
}

// buildBar constructs the progress bar string
func (pb *ProgressBar) buildBar() string {
	style := pb.config.Style
	width := pb.config.Width

	var completeLen int
	if pb.config.Total > 0 {
		completeLen = int(float64(width) * float64(pb.current) / float64(pb.config.Total))
	}
	if completeLen > width {
		completeLen = width
	}
	if completeLen < 0 {
		completeLen = 0
	}

	incompleteLen := width - completeLen

	// Build bar
	complete := strings.Repeat(style.Complete, completeLen)
	incomplete := strings.Repeat(style.Incomplete, incompleteLen)

	// Apply colors
	if pb.config.ColorComplete != "" {
		complete = string(pb.config.ColorComplete) + complete + string(ColorReset)
	}
	if pb.config.ColorIncomplete != "" {
		incomplete = string(pb.config.ColorIncomplete) + incomplete + string(ColorReset)
	}

	return style.LeftEnd + complete + incomplete + style.RightEnd
}

// formatDuration formats a duration for display
func formatDuration(d time.Duration) string {
	if d < 0 {
		return "--:--:--"
	}

	hours := int(d.Hours())
	minutes := int(d.Minutes()) % 60
	seconds := int(d.Seconds()) % 60

	if hours > 0 {
		return fmt.Sprintf("%d:%02d:%02d", hours, minutes, seconds)
	}
	return fmt.Sprintf("%02d:%02d", minutes, seconds)
}

// formatSpeed formats items per second for display
func formatSpeed(speed float64) string {
	if speed >= 1e9 {
		return fmt.Sprintf("%.1fG", speed/1e9)
	} else if speed >= 1e6 {
		return fmt.Sprintf("%.1fM", speed/1e6)
	} else if speed >= 1e3 {
		return fmt.Sprintf("%.1fK", speed/1e3)
	}
	return fmt.Sprintf("%.0f", speed)
}

// ==================== Static Progress Bars ====================

// Static creates a static progress bar string without animation
func Static(current, total int64, width int, style Style) string {
	return StaticWithConfig(current, total, Config{
		Width: width,
		Style: style,
	})
}

// StaticWithConfig creates a static progress bar with full configuration
func StaticWithConfig(current, total int64, config Config) string {
	if config.Width <= 0 {
		config.Width = 40
	}

	var completeLen int
	if total > 0 {
		completeLen = int(float64(config.Width) * float64(current) / float64(total))
	}
	if completeLen > config.Width {
		completeLen = config.Width
	}
	if completeLen < 0 {
		completeLen = 0
	}

	incompleteLen := config.Width - completeLen

	complete := strings.Repeat(config.Style.Complete, completeLen)
	incomplete := strings.Repeat(config.Style.Incomplete, incompleteLen)

	if config.ColorComplete != "" {
		complete = string(config.ColorComplete) + complete + string(ColorReset)
	}
	if config.ColorIncomplete != "" {
		incomplete = string(config.ColorIncomplete) + incomplete + string(ColorReset)
	}

	return config.Style.LeftEnd + complete + incomplete + config.Style.RightEnd
}

// StaticPercentage creates a progress bar with percentage text
func StaticPercentage(current, total int64, width int, style Style) string {
	bar := Static(current, total, width, style)
	percent := float64(current) / float64(total) * 100
	return fmt.Sprintf("%s %.1f%%", bar, percent)
}

// StaticFull creates a full progress bar with all info
func StaticFull(current, total int64, width int, style Style, desc string) string {
	bar := Static(current, total, width, style)
	percent := float64(current) / float64(total) * 100
	return fmt.Sprintf("%s: %s %.1f%% (%d/%d)", desc, bar, percent, current, total)
}

// ==================== MultiBar Support ====================

// MultiBar manages multiple progress bars simultaneously
type MultiBar struct {
	bars    []*ProgressBar
	prefixes []string
	mu      sync.Mutex
	writer  io.Writer
}

// NewMultiBar creates a new multi-bar manager
func NewMultiBar() *MultiBar {
	return &MultiBar{
		bars:    make([]*ProgressBar, 0),
		prefixes: make([]string, 0),
		writer:  os.Stderr,
	}
}

// AddBar adds a new progress bar to the manager
func (mb *MultiBar) AddBar(total int64, prefix string) *ProgressBar {
	mb.mu.Lock()
	defer mb.mu.Unlock()

	config := Config{
		Total:           total,
		Width:           30,
		Style:           StyleDefault,
		ShowPercentage:  true,
		ShowCount:       false,
		ShowETA:         false,
		ShowSpeed:       false,
		ShowElapsedTime: false,
		Writer:          io.Discard, // Don't write individually
	}

	pb := NewWithConfig(config)
	mb.bars = append(mb.bars, pb)
	mb.prefixes = append(mb.prefixes, prefix)

	return pb
}

// Render renders all progress bars
func (mb *MultiBar) Render() {
	mb.mu.Lock()
	defer mb.mu.Unlock()

	// Move cursor up for each bar
	for i := 0; i < len(mb.bars); i++ {
		fmt.Fprint(mb.writer, "\033[A\033[K")
	}

	// Render each bar
	for i, pb := range mb.bars {
		bar := pb.buildBar()
		percent := pb.Percentage()
		line := fmt.Sprintf("%s %s %.1f%% (%d/%d)\n", mb.prefixes[i], bar, percent, pb.current, pb.config.Total)
		fmt.Fprint(mb.writer, line)
	}
}

// ==================== Spinner ====================

// Spinner represents an animated spinner
type Spinner struct {
	frames   []string
	interval time.Duration
	current  int
	writer   io.Writer
	prefix   string
	suffix   string
	mu       sync.Mutex
	stopCh   chan struct{}
}

// NewSpinner creates a new spinner
func NewSpinner(prefix string) *Spinner {
	return &Spinner{
		frames:   spinnerChars,
		interval: 100 * time.Millisecond,
		current:  0,
		writer:   os.Stderr,
		prefix:   prefix,
		suffix:   "",
		stopCh:   nil,
	}
}

// SetFrames sets custom spinner frames
func (s *Spinner) SetFrames(frames []string) *Spinner {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.frames = frames
	return s
}

// SetInterval sets the animation interval
func (s *Spinner) SetInterval(d time.Duration) *Spinner {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.interval = d
	return s
}

// SetSuffix sets the suffix text
func (s *Spinner) SetSuffix(suffix string) *Spinner {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.suffix = suffix
	return s
}

// Start starts the spinner
func (s *Spinner) Start() *Spinner {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.stopCh != nil {
		return s
	}

	s.stopCh = make(chan struct{})
	go func() {
		ticker := time.NewTicker(s.interval)
		defer ticker.Stop()

		for {
			select {
			case <-s.stopCh:
				return
			case <-ticker.C:
				s.render()
			}
		}
	}()

	return s
}

// Stop stops the spinner
func (s *Spinner) Stop() {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.stopCh != nil {
		close(s.stopCh)
		s.stopCh = nil
		fmt.Fprint(s.writer, "\r\033[K")
	}
}

// Update updates the suffix text
func (s *Spinner) Update(suffix string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.suffix = suffix
}

func (s *Spinner) render() {
	s.mu.Lock()
	defer s.mu.Unlock()

	frame := s.frames[s.current]
	s.current = (s.current + 1) % len(s.frames)
	fmt.Fprintf(s.writer, "\r\033[K%s %s %s", s.prefix, frame, s.suffix)
}

// ==================== Utility Functions ====================

// FormatBytes formats bytes into human-readable string
func FormatBytes(bytes int64) string {
	const (
		KB = 1024
		MB = KB * 1024
		GB = MB * 1024
		TB = GB * 1024
	)

	switch {
	case bytes >= TB:
		return fmt.Sprintf("%.2f TB", float64(bytes)/TB)
	case bytes >= GB:
		return fmt.Sprintf("%.2f GB", float64(bytes)/GB)
	case bytes >= MB:
		return fmt.Sprintf("%.2f MB", float64(bytes)/MB)
	case bytes >= KB:
		return fmt.Sprintf("%.2f KB", float64(bytes)/KB)
	default:
		return fmt.Sprintf("%d B", bytes)
	}
}

// FormatNumber formats a number with thousands separator
func FormatNumber(n int64) string {
	s := fmt.Sprintf("%d", n)
	result := ""
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			result += ","
		}
		result += string(c)
	}
	return result
}

// CalculateProgress calculates progress percentage safely
func CalculateProgress(current, total int64) float64 {
	if total == 0 {
		return 0
	}
	percent := float64(current) / float64(total) * 100
	if percent > 100 {
		return 100
	}
	if percent < 0 {
		return 0
	}
	return percent
}

// EstimateTime estimates remaining time based on progress
func EstimateTime(elapsed time.Duration, current, total int64) time.Duration {
	if current == 0 || current >= total {
		return 0
	}

	rate := float64(current) / elapsed.Seconds()
	if rate == 0 {
		return 0
	}

	remaining := float64(total-current) / rate
	return time.Duration(remaining) * time.Second
}

// ==================== Iterator Support ====================

// Iterate creates a progress bar for iterating over a slice
func Iterate[T any](items []T, desc string, fn func(int, T) error) error {
	pb := New(int64(len(items)))
	pb.config.Description = desc
	pb.config.Width = 30

	for i, item := range items {
		if err := fn(i, item); err != nil {
			return err
		}
		pb.Increment()
	}

	pb.Finish()
	return nil
}

// IterateWithConfig creates a progress bar with config for iterating
func IterateWithConfig[T any](items []T, config Config, fn func(int, T) error) error {
	config.Total = int64(len(items))
	pb := NewWithConfig(config)

	for i, item := range items {
		if err := fn(i, item); err != nil {
			return err
		}
		pb.Increment()
	}

	pb.Finish()
	return nil
}